"""Stage the frozen AGP project outside Git after verifying asset/tool downloads."""
import argparse
import hashlib
import json
from pathlib import Path
import shutil
import zipfile


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--previous', type=Path, required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    if not json.loads((root / 'model-inspection/inspection.json').read_text())['linkage_pass']:
        raise ValueError('Model linkage failed')
    distribution = root / 'gradle-download/complete.body'
    expected = (root / 'gradle-checksum/complete.body').read_text().strip()
    if len(expected) != 64 or sha(distribution) != expected:
        raise ValueError('Gradle publisher checksum mismatch')
    toolchain = root / 'toolchain'
    toolchain.mkdir(exist_ok=False)
    with zipfile.ZipFile(distribution) as archive:
        for member in archive.infolist():
            target = (toolchain / member.filename).resolve()
            if not target.is_relative_to(toolchain):
                raise ValueError('Archive path escapes destination')
        archive.extractall(toolchain)
    (toolchain / 'gradle-7.5.1/bin/gradle').chmod(0o755)
    sdk = root / 'sdk'
    for relative in ('platforms/android-30', 'build-tools/35.0.0'):
        shutil.copytree(args.previous / 'android/sdk' / relative, sdk / relative)
    project = root / 'project'
    (project / 'app/src/main/ml').mkdir(parents=True, exist_ok=False)
    model = project / 'app/src/main/ml/lite_model_deeplabv3_1_metadata_2.tflite'
    shutil.copyfile(root / 'model-download/complete.body', model)
    (project / 'settings.gradle').write_text("rootProject.name = 'Support770'\ninclude ':app'\n")
    (project / 'build.gradle').write_text("""buildscript {
    repositories { google(); mavenCentral() }
    dependencies { classpath 'com.android.tools.build:gradle:7.4.2' }
}
allprojects { repositories { google(); mavenCentral() } }
""")
    (project / 'app/build.gradle').write_text("""apply plugin: 'com.android.application'
android {
    namespace 'org.example.support770'
    compileSdk 30
    buildToolsVersion '35.0.0'
    defaultConfig {
        applicationId 'org.example.support770'
        minSdk 23
        targetSdk 30
        versionCode 1
        versionName '1.0'
        ndk { abiFilters 'x86_64' }
    }
    buildFeatures { mlModelBinding true }
    compileOptions {
        sourceCompatibility JavaVersion.VERSION_1_8
        targetCompatibility JavaVersion.VERSION_1_8
    }
}
dependencies {
    implementation 'org.tensorflow:tensorflow-lite:2.13.0'
    implementation 'org.tensorflow:tensorflow-lite-support:0.4.4'
}
""")
    (project / 'app/src/main/AndroidManifest.xml').write_text(
        '<manifest xmlns:android="http://schemas.android.com/apk/res/android">'
        '<application android:label="Support770" android:debuggable="true"/></manifest>\n')
    (project / 'gradle.properties').write_text(
        'org.gradle.jvmargs=-Xmx1536m\norg.gradle.workers.max=2\nandroid.useAndroidX=true\n')
    (project / 'local.properties').write_text(f'sdk.dir={sdk}\n')
    sources = Path(__file__).resolve().parent
    shutil.copytree(sources, root / 'generation-source')
    record = {'gradle_distribution_sha256': expected, 'model_sha256': sha(model),
              'project_files': {str(p.relative_to(project)): sha(p)
                                for p in project.rglob('*') if p.is_file()},
              'sdk_copies': {str(p.relative_to(sdk)): sha(p)
                            for p in sdk.rglob('*') if p.is_file()},
              'jdk_release': (args.previous / 'hand/toolchains/jdk-17.0.12+7/release').read_text(),
              'source_files': {p.name: sha(p) for p in sources.iterdir() if p.is_file()}}
    (root / 'generation-freeze.json').write_text(json.dumps(record, indent=2) + '\n')
    print(json.dumps({'project': str(project), 'sdk_files': len(record['sdk_copies']),
                      'gradle_sha256': expected, 'model_sha256': sha(model)}))


if __name__ == '__main__':
    main()
