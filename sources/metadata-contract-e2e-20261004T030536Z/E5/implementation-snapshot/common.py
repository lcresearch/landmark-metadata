import datetime, hashlib, json, os, pathlib, shlex, subprocess
ROOT=pathlib.Path(__file__).resolve().parents[1]
HAND=pathlib.Path('/workspace/hand-contract-repro')
JDK=HAND/'toolchains/jdk-17.0.12+7'
PYTHON=HAND/'.venv/bin/python'
def sha(data): return hashlib.sha256(data).hexdigest()
def save(path, value):
    path=pathlib.Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(value,indent=2))
def run(command, log, timeout=120, cwd=None, binary=False):
    log=pathlib.Path(log);log.parent.mkdir(parents=True,exist_ok=True)
    env=os.environ.copy();env['JAVA_HOME']=str(JDK);env['PYTHONDONTWRITEBYTECODE']='1'
    record={'command':list(map(str,command)),'cwd':str(cwd or ROOT),'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        p=subprocess.run(record['command'],cwd=cwd or ROOT,env=env,capture_output=True,timeout=timeout)
        record.update(exit_code=p.returncode)
        log.with_suffix(log.suffix+'.stdout').write_bytes(p.stdout)
        log.with_suffix(log.suffix+'.stderr').write_bytes(p.stderr)
    except subprocess.TimeoutExpired as exc:
        record.update(exit_code=None,timeout_seconds=timeout)
        log.with_suffix(log.suffix+'.stdout').write_bytes(exc.stdout or b'')
        log.with_suffix(log.suffix+'.stderr').write_bytes(exc.stderr or b'')
        save(log.with_suffix(log.suffix+'.command.json'),record)
        raise
    save(log.with_suffix(log.suffix+'.command.json'),record)
    with (ROOT/'commands-executed.sh').open('a') as out:
        out.write(f"# {record['started_utc']}; exit={p.returncode}; logs={log}\n(cd {shlex.quote(str(cwd or ROOT))} && {shlex.join(record['command'])})\n")
    return p
