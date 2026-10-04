"""Restore the tested JDK from a recorded public URL, verifying its exact digest.

Python 3.11 and packages in requirements.lock are installed separately, see REPRODUCE.txt.
Dependency jars are included in the evidence archive.
"""
from pathlib import Path
import hashlib
import json
import tarfile
import urllib.request

ROOT=Path(__file__).resolve().parents[1]

def main():
    record=json.loads((ROOT/'downloads/jdk-download.json').read_text())
    archive=ROOT/'downloads/jdk17.tar.gz'
    if not archive.exists():
        with urllib.request.urlopen(record['url'],timeout=60) as response,archive.open('wb') as out:
            while block:=response.read(1024*1024):out.write(block)
    with archive.open('rb') as src: digest=hashlib.file_digest(src,'sha256').hexdigest()
    assert digest==record['sha256'], 'JDK download digest mismatch'
    destination=ROOT/'toolchains'
    destination.mkdir(exist_ok=True)
    with tarfile.open(archive) as tar:
        for member in tar.getmembers():
            if not (destination/member.name).resolve().is_relative_to(destination.resolve()):
                raise ValueError('Unsafe archive path')
        tar.extractall(destination,filter='data')
    print('Restored exact tested JDK:',digest)

if __name__=='__main__':
    main()
