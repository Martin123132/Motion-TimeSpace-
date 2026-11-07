import os
import sys
import hashlib
import json
from pathlib import Path
from datetime import datetime, timezone

for name in ('OMP_NUM_THREADS','OPENBLAS_NUM_THREADS','MKL_NUM_THREADS','NUMEXPR_NUM_THREADS','BLIS_NUM_THREADS'):
    os.environ[name]='1'
os.environ['PYTHONDONTWRITEBYTECODE']='1'
ROOT=Path(__file__).resolve().parent
POST=ROOT.parent
LATEST=POST/'mts-cold-adapted-metric-gain-20261107'
STRESS=POST/'mts-species-stress-suppression-20261107'
BACKGROUND=POST/'mts-background-repair-20261107'
BRANCH=POST/'condensate-origin-20261003'
CLOSURE=POST/'mts-pressure-balance-20261107'
NATIVE=BRANCH/'native-heavy-matching-20261007/native'
EARLY=BRANCH/'native-two-field-transfer-20261007'
BRIDGE=Path('C:/MTS-Data/condensate-origin-20261003/stiff-gas-dense-output-20261027/data/memory-tail-history-20261027/source-readout-bridge-20261102')
PARENT_SEAL='cd29bc225d756592906efe5c3eb8316c937af9150865fffa9a7b361e43920b5e'
BACKGROUND_SEAL='c12e8dbaedc7bb230c0448248664c0c4b4e285b567e22c499019438bb5c2b3cf'
GATE,ALGEBRA=2e-5,1e-10


def require(condition,message):
    if not condition:
        raise ValueError(message)


def guard():
    require(datetime.now(timezone.utc)<datetime(2026,11,7,21,35,tzinfo=timezone.utc),'four-hour cutoff')
    for path in (ROOT/'STOP-REQUESTED',BRIDGE/'STOP-REQUESTED',BRIDGE.parent/'STOP-REQUESTED',BRIDGE.parent/'execution-v3/STOP-REQUEST.json',BRIDGE/'final-epoch-kinematic-bank/STOP-REQUESTED'):
        require(not path.exists(),'owner hold: '+str(path))


def modest():
    import psutil
    process=psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([4])
    guard()


def digest(path):
    result=hashlib.sha256()
    with Path(path).open('rb') as stream:
        for block in iter(lambda:stream.read(1024*1024),b''):
            result.update(block)
    return result.hexdigest()


def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))


def write(path,value):
    with Path(path).open('x',encoding='utf-8') as stream:
        json.dump(value,stream,indent=2,allow_nan=False)


def load(path):
    import numpy as np
    with np.load(path) as archive:
        return {name:archive[name].copy() for name in archive.files}


def check_parent():
    for directory,expected in ((LATEST,PARENT_SEAL),(BACKGROUND,BACKGROUND_SEAL)):
        require(digest(directory/'closeout.json')==expected,'parent seal')
        seal=read(directory/'closeout.json')
        require(seal['state']=='verified_closed','parent state')
        for record in seal['artifacts']:
            guard()
            require(digest(record['path'])==record['sha256'],'changed parent: '+record['path'])
    for path,expected in read(BACKGROUND/'input-result.json')['local_sources'].items():
        require(digest(path)==expected,'changed background source')


def frozen_sources():
    return {str(path):digest(path) for path in ROOT.iterdir() if path.suffix in ('.py','.ps1','.md')}
