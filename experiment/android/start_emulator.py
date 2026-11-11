import json, os, pathlib, subprocess, time
from common import ROOT, run, save
sdk=ROOT/'sdk';pre=ROOT/'prerequisites';avd=sdk/'avd/research30.avd';avd.mkdir(parents=True,exist_ok=True)
(sdk/'avd/research30.ini').write_text(f'avd.ini.encoding=UTF-8\npath={avd}\ntarget=android-30\n')
(avd/'config.ini').write_text(f'''avd.ini.encoding=UTF-8
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
command=[str(sdk/'emulator/emulator'),'-avd','research30','-port','5554','-no-window','-no-audio','-no-boot-anim','-no-snapshot','-accel','off','-gpu','swiftshader_indirect','-feature','-Vulkan','-camera-back','none','-camera-front','none']
env=os.environ.copy();env['ANDROID_SDK_ROOT']=str(sdk);env['ANDROID_AVD_HOME']=str(sdk/'avd');env['QT_QPA_PLATFORM']='offscreen'
with (pre/'emulator.stdout').open('wb') as out,(pre/'emulator.stderr').open('wb') as err:
    p=subprocess.Popen(command,env=env,stdout=out,stderr=err,start_new_session=True)
save(pre/'emulator-command.json',{'command':command,'pid':p.pid,'environment':{k:env[k] for k in ['ANDROID_SDK_ROOT','ANDROID_AVD_HOME','QT_QPA_PLATFORM']}})
adb=sdk/'platform-tools/adb';deadline=time.monotonic()+900;observations=[]
while time.monotonic()<deadline:
    if p.poll() is not None:
        save(pre/'emulator-readiness.json',{'status':'FAIL','emulator_exit_code':p.returncode,'observations':observations});raise SystemExit('Emulator exited')
    try:
        q=subprocess.run([str(adb),'-s','emulator-5554','shell','getprop','sys.boot_completed'],capture_output=True,text=True,timeout=15)
        observations.append({'elapsed':round(900-(deadline-time.monotonic()),1),'returncode':q.returncode,'stdout':q.stdout.strip(),'stderr':q.stderr.strip()})
        if q.stdout.strip()=='1':
            print('Android boot completed',flush=True)
            save(pre/'emulator-readiness.json',{'status':'PASS','observations':observations})
            run([adb,'-s','emulator-5554','shell','getprop'],pre/'android-getprop')
            break
    except subprocess.TimeoutExpired:observations.append({'status':'ADB_TIMEOUT'})
    time.sleep(5)
else:
    save(pre/'emulator-readiness.json',{'status':'FAIL','reason':'boot timeout 900 seconds','observations':observations})
    raise SystemExit('Boot timeout')
