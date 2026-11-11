"""Boot one fresh software AVD; preserve readiness failure and owned PID."""
import argparse
import hashlib
import json
import os
from pathlib import Path
import shutil
import socket
import subprocess
import time


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, required=True)
    parser.add_argument('--previous', type=Path, required=True)
    args = parser.parse_args()
    root = args.root.resolve()
    sdk = root / 'sdk'
    boot = root / 'boot'; boot.mkdir(exist_ok=False)
    if not all(r['status'] == 'PASS' for r in json.loads((root / 'build-results.json').read_text())):
        raise ValueError('Builds incomplete')
    for port in (5556, 5557):
        with socket.socket() as sock:
            sock.bind(('127.0.0.1', port))
    for relative in ('emulator', 'platform-tools', 'system-images/android-30'):
        shutil.copytree(args.previous / 'android/sdk' / relative, sdk / relative)
    avd = root / 'avd/support770.avd'; avd.mkdir(parents=True)
    (avd.parent / 'support770.ini').write_text(f'avd.ini.encoding=UTF-8\npath={avd}\ntarget=android-30\n')
    (avd / 'config.ini').write_text(f'''avd.ini.encoding=UTF-8
abi.type=x86_64
hw.cpu.arch=x86_64
image.sysdir.1={sdk}/system-images/android-30/default/x86_64/
tag.id=default
tag.display=Default
hw.ramSize=2048
hw.cpu.ncore=2
hw.lcd.width=480
hw.lcd.height=640
hw.lcd.density=160
hw.gpu.enabled=yes
hw.gpu.mode=swiftshader_indirect
disk.dataPartition.size=2G
hw.keyboard=yes
showDeviceFrame=no
''')
    command = [str(sdk / 'emulator/emulator'), '-avd', 'support770', '-port', '5556',
        '-no-window', '-no-audio', '-no-boot-anim', '-no-snapshot', '-accel', 'off',
        '-gpu', 'swiftshader_indirect', '-feature', '-Vulkan', '-camera-back', 'none', '-camera-front', 'none']
    env = dict(os.environ, ANDROID_SDK_ROOT=str(sdk), ANDROID_AVD_HOME=str(avd.parent),
               ANDROID_USER_HOME=str(root / 'android-user'), QT_QPA_PLATFORM='offscreen')
    with (boot / 'emulator.stdout').open('wb') as out, (boot / 'emulator.stderr').open('wb') as err:
        process = subprocess.Popen(command, env=env, stdout=out, stderr=err, start_new_session=True)
    record = {'command': command, 'pid': process.pid, 'serial': 'emulator-5556',
              'source_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'environment': {k: env[k] for k in ('ANDROID_SDK_ROOT','ANDROID_AVD_HOME','ANDROID_USER_HOME','QT_QPA_PLATFORM')}}
    (boot / 'launch.json').write_text(json.dumps(record, indent=2) + '\n')
    deadline = time.monotonic() + 900
    observations = []
    status = 'FAIL'
    adb = str(sdk / 'platform-tools/adb')
    while time.monotonic() < deadline and process.poll() is None:
        try:
            result = subprocess.run([adb, '-s', 'emulator-5556', 'shell', 'getprop', 'sys.boot_completed'],
                capture_output=True, timeout=15)
            observations.append({'elapsed_seconds': 900 - (deadline - time.monotonic()),
                                 'exit_code': result.returncode, 'stdout': result.stdout.decode(errors='replace'),
                                 'stderr': result.stderr.decode(errors='replace')})
            if result.returncode == 0 and result.stdout.strip() == b'1':
                status = 'PASS'; break
        except subprocess.TimeoutExpired:
            observations.append({'timeout': True})
        (boot / 'readiness.json').write_text(json.dumps({'status': 'RUNNING', 'observations': observations}, indent=2) + '\n')
        time.sleep(5)
    (boot / 'readiness.json').write_text(json.dumps({'status': status, 'observations': observations,
        'emulator_exit_code': process.poll()}, indent=2) + '\n')
    if status != 'PASS':
        process.terminate()
        try: process.wait(timeout=10)
        except subprocess.TimeoutExpired: process.kill()
    else:
        props = subprocess.run([adb, '-s', 'emulator-5556', 'shell', 'getprop'], capture_output=True, timeout=30)
        (boot / 'getprop.stdout').write_bytes(props.stdout)
        (boot / 'getprop.stderr').write_bytes(props.stderr)
    print(status, flush=True)
    raise SystemExit(0 if status == 'PASS' else 1)


if __name__ == '__main__':
    main()
