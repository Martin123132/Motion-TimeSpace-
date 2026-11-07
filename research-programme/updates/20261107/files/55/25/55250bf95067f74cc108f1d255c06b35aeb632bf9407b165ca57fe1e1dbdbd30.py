from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import sys

os.environ['OMP_NUM_THREADS']='1'
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['MKL_NUM_THREADS']='1'
sys.dont_write_bytecode=True

import numpy as np
import psutil
from scipy import integrate, interpolate, linalg

ROOT=Path(__file__).resolve().parent
BRANCH=ROOT.parent
POST=BRANCH.parent
PARENT=BRANCH/'native-heavy-matching-20261007'
EARLY=BRANCH/'native-two-field-transfer-20261007'
sys.path.insert(0,str(PARENT))
import matching_common as inherited
from prepare_matching import project

camb=inherited.camb
previous=inherited.previous
BACKGROUND=EARLY/'runs/backgrounds/heavy.npz'
TARGET_REDSHIFTS=np.array([10.,2.,1.48,1.,.698,.51,.38,0.])


def digest(path):
    hasher=hashlib.sha256()
    with Path(path).open('rb') as handle:
        for block in iter(lambda:handle.read(1024*1024),b''):
            hasher.update(block)
    return hasher.hexdigest()


def modest():
    process=psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])


def write_json(path,value):
    Path(path).write_text(json.dumps(value,indent=2,allow_nan=False),encoding='utf-8')


def inputs():
    paths=[ROOT/'spectrum_common.py',PARENT/'results/stage-integrity.json',PARENT/'prepare_matching.py',
        PARENT/'stage_common.py',*inherited.native_hashes()]
    return paths


def finish(folder,report,script,extra=()):
    paths=[Path(script),*inputs(),*extra]
    report.update(state='complete',finished_utc=datetime.now(timezone.utc).isoformat(),
        script_sha256=digest(script),input_hashes={str(path):digest(path) for path in paths})
    write_json(folder/'status.json',report)
    (folder/'COMPLETE').write_text('complete\n',encoding='utf-8')


def modes(refinement):
    logarithmic=np.geomspace(1e-5,10.,128*refinement+1)
    acoustic=np.linspace(.02,.4,76*refinement+1)
    return np.array(sorted({float(format(value,'.13g')) for value in [*logarithmic,*acoustic,.03,.1,1.,5.]}))


def late_scales():
    values=[.0003,.0005,.001,.003,.01]
    for redshift in TARGET_REDSHIFTS:
        center=-math.log1p(redshift)
        for step in [.002,.001]:
            offsets=np.arange(-4,1) if redshift==0 else np.arange(-2,3)
            values.extend(np.exp(center+offsets*step))
    return np.unique(values)


def load_evolution(label):
    folder=ROOT/'runs'/label
    packets=[np.load(path) for path in sorted(folder.glob('chunk-*.npz'))]
    return dict(modes=np.concatenate([packet['modes'] for packet in packets]),
        values=np.concatenate([packet['values'] for packet in packets]),
        names=packets[0]['names'].tolist(),scales=packets[0]['requested_scale'],
        times=packets[0]['conformal_time'])


def top_hat(argument):
    argument=np.asarray(argument)
    result=np.empty_like(argument)
    small=abs(argument)<.05
    squared=argument[small]**2
    result[small]=1-squared/10+squared**2/280-squared**3/15120
    chosen=argument[~small]
    result[~small]=3*(np.sin(chosen)-chosen*np.cos(chosen))/chosen**3
    return result
