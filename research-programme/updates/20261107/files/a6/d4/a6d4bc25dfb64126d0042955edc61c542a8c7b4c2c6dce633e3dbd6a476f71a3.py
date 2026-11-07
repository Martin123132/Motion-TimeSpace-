from __future__ import annotations

import os
import sys
os.environ['OMP_NUM_THREADS']='1'
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['MKL_NUM_THREADS']='1'
sys.dont_write_bytecode=True
from pathlib import Path
from datetime import datetime, timezone
import json
import math
import numpy as np
from scipy import integrate, interpolate

ROOT=Path(__file__).resolve().parent
BRANCH=ROOT.parent
POST=BRANCH.parent
PARENT=BRANCH/'nonlinear-source-feedback-20261007'
sys.path.insert(0,str(PARENT))
import feedback_common as inherited
modest=inherited.modest
digest=inherited.digest
write_json=inherited.write_json
SPECTRUM=inherited.SPECTRUM
NATIVE=inherited.NATIVE
BACKGROUND=BRANCH/'native-two-field-transfer-20261007/runs/backgrounds/heavy.npz'


def finish(folder,report,script,extra=()):
    paths=[Path(script),ROOT/'seed_common.py',ROOT/'ACCEPTANCE.md',
        PARENT/'results/stage-integrity.json',PARENT/'feedback_common.py',*extra]
    report.update(state='complete',finished_utc=datetime.now(timezone.utc).isoformat(),
        script_sha256=digest(script),input_hashes={str(path):digest(path) for path in paths})
    write_json(folder/'status.json',report)
    (folder/'COMPLETE').write_text('complete\n',encoding='utf-8')


def derivative(values,order=1):
    count=values.shape[-1]
    frequency=np.fft.fftfreq(count,d=1/count)
    frequency[count//2]=0
    return np.fft.ifft(np.fft.fft(values,axis=-1)*(1j*frequency)**order,axis=-1).real


def planar_geometry(amplitude,count=512):
    phase=2*math.pi*np.arange(count)/count
    zeta=amplitude*(np.cos(phase)+.2*np.cos(2*phase+.3))
    first=-amplitude*(np.sin(phase)+.4*np.sin(2*phase+.3))
    second=-amplitude*(np.cos(phase)+.8*np.cos(2*phase+.3))
    curvature=np.exp(-2*zeta)*(-4*second-2*first**2)
    tracefree_x=np.exp(-2*zeta)*(-2*second/3+2*first**2/3)
    return phase,zeta,curvature,tracefree_x
