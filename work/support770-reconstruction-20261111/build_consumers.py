"""Build each consumer once using the actual unchanged AGP-generated source."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import zipfile

SOURCE = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--previous', type=Path, required=True)
    args = parser.parse_args()
    root, previous = args.root.resolve(), args.previous.resolve()
    build_root = root / 'build'
    build_root.mkdir(exist_ok=False)
    shutil.copytree(SOURCE, root / 'runtime-source')
    jdk = previous / 'hand/toolchains/jdk-17.0.12+7'
    env = dict(os.environ, JAVA_HOME=str(jdk), PYTHONDONTWRITEBYTECODE='1')
    sdk = root / 'sdk'
    bt = sdk / 'build-tools/35.0.0'
    platform = sdk / 'platforms/android-30/android.jar'
    generated = root / 'project/app/build/generated/ml_source_out/debug/org/example/support770/ml/LiteModelDeeplabv31Metadata2.java'
    old_lock = previous / 'round/P2/dependencies/resolved-lock.json'
    dependencies = json.loads(old_lock.read_text())
    lock = {'previous_lock_sha256': sha(old_lock), 'generated_source_sha256': sha(generated),
            'jdk_java_sha256': sha(jdk / 'bin/java'), 'jdk_javac_sha256': sha(jdk / 'bin/javac'),
            'source_files': {p.name: sha(p) for p in SOURCE.iterdir() if p.is_file()},
            'consumers': {}}
    for consumer, config in dependencies.items():
        lock['consumers'][consumer] = {}
        for group in ('classpaths', 'natives'):
            items = []
            for i, entry in enumerate(config[group]):
                old = Path(entry['path'])
                if sha(old) != entry['sha256']:
                    raise ValueError(f'Previous dependency changed: {old}')
                target = root / 'runtime-dependencies' / consumer / group / str(i) / old.name
                target.parent.mkdir(parents=True, exist_ok=False)
                shutil.copyfile(old, target)
                items.append({'path': str(target), 'sha256': sha(target), 'previous_path': str(old)})
            lock['consumers'][consumer][group] = items
    (root / 'runtime-freeze.json').write_text(json.dumps(lock, indent=2) + '\n')

    def stage(name, command, timeout=180):
        result = subprocess.run([sys.executable, '-B', str(SOURCE / 'record_command.py'),
            '--output', str(build_root / 'stages' / name), '--cwd', str(root),
            '--timeout', str(timeout), '--', *map(str, command)], env=env)
        if result.returncode:
            raise RuntimeError(f'Build stage failed: {name}')

    key = build_root / 'local-test.keystore'
    stage('keytool', [jdk / 'bin/keytool', '-genkeypair', '-keystore', key, '-storepass', 'android',
        '-alias', 'research', '-keypass', 'android', '-keyalg', 'RSA', '-keysize', '2048',
        '-validity', '3650', '-dname', 'CN=Support770 local research'])
    records = []
    for consumer, config in lock['consumers'].items():
        folder = build_root / consumer
        folder.mkdir()
        instrument = 'WrapperInstrumentation' if consumer == 'wrapper' else 'TaskInstrumentation'
        package = 'org.example.support770.' + consumer
        record = {'consumer': consumer, 'package': package, 'instrument': instrument,
                  'generated_source_modified': False if consumer == 'wrapper' else None}
        try:
            classes = folder / 'classes'; classes.mkdir()
            deps = [Path(x['path']) for x in config['classpaths']]
            sources = [SOURCE / 'EvidenceInstrumentation.java', SOURCE / (instrument + '.java')]
            if consumer == 'wrapper': sources.append(generated)
            stage(consumer + '-compile', [jdk / 'bin/javac', '--release', '8', '-cp',
                ':'.join(map(str, [platform, *deps])), '-d', classes, *sources])
            record['class_hashes'] = {str(p.relative_to(classes)): sha(p) for p in classes.rglob('*.class')}
            program = folder / 'program.jar'
            with zipfile.ZipFile(program, 'w') as archive:
                for path in sorted(classes.rglob('*.class')):
                    archive.writestr(str(path.relative_to(classes)), path.read_bytes())
            dex = folder / 'dex'; dex.mkdir()
            stage(consumer + '-dex', [bt / 'd8', '--release', '--min-api', '23', '--lib', platform,
                  '--output', dex, program, *deps])
            assets = folder / 'assets'; assets.mkdir()
            shutil.copyfile(root / 'model-download/complete.body', assets / 'lite_model_deeplabv3_1_metadata_2.tflite')
            manifest = folder / 'AndroidManifest.xml'
            manifest.write_text(f'<manifest xmlns:android="http://schemas.android.com/apk/res/android" package="{package}" android:versionCode="1" android:versionName="1.0"><uses-sdk android:minSdkVersion="23" android:targetSdkVersion="30"/><application android:label="Support770" android:debuggable="true" android:extractNativeLibs="true" android:hasCode="true"/><instrumentation android:name="org.example.support770.{instrument}" android:targetPackage="{package}" android:functionalTest="true"/></manifest>')
            unsigned = folder / 'unsigned.apk'
            stage(consumer + '-resources', [bt / 'aapt2', 'link', '-o', unsigned, '--manifest', manifest,
                  '-I', platform, '-A', assets, '-0', 'tflite'])
            with zipfile.ZipFile(unsigned, 'a', compression=zipfile.ZIP_STORED) as archive:
                for path in sorted(dex.glob('*.dex')): archive.write(path, path.name)
                for item in config['natives']:
                    path = Path(item['path']); archive.write(path, 'lib/x86_64/' + path.name)
            stage(consumer + '-align', [bt / 'zipalign', '-f', '4', unsigned, folder / 'aligned.apk'])
            stage(consumer + '-sign', [bt / 'apksigner', 'sign', '--ks', key, '--ks-key-alias', 'research',
                '--ks-pass', 'pass:android', '--key-pass', 'pass:android', '--out', folder / 'consumer.apk', folder / 'aligned.apk'])
            stage(consumer + '-verify', [bt / 'apksigner', 'verify', '--verbose', folder / 'consumer.apk'])
            record.update(status='PASS', apk_sha256=sha(folder / 'consumer.apk'))
            with zipfile.ZipFile(folder / 'consumer.apk') as archive:
                record['packaged_model_sha256'] = hashlib.sha256(archive.read('assets/lite_model_deeplabv3_1_metadata_2.tflite')).hexdigest()
            if consumer == 'wrapper' and sha(generated) != lock['generated_source_sha256']:
                raise ValueError('Generated source changed')
        except Exception as exc:
            record.update(status='FAIL', error=repr(exc))
        records.append(record)
        (root / 'build-results.json').write_text(json.dumps(records, indent=2) + '\n')
    raise SystemExit(0 if all(r['status'] == 'PASS' for r in records) else 1)


if __name__ == '__main__':
    main()
