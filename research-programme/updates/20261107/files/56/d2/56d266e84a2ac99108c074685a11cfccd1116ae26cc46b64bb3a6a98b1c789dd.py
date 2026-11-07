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
import time
import numpy as np
from scipy import integrate,interpolate,linalg

ROOT=Path(__file__).resolve().parent
BRANCH=ROOT.parent
POST=BRANCH.parent
PARENT=BRANCH/'thomson-source-coupling-20261007'
GEOMETRY=BRANCH/'einstein-constraints-and-kinetic-response-20261007'
HISTORY=BRANCH/'full-history-source-precision-20261007'
NATIVE=BRANCH/'native-heavy-matching-20261007/native'
sys.path.insert(0,str(PARENT))
import collision_common as inherited
modest=inherited.modest
digest=inherited.digest
write_json=inherited.write_json


def finish(folder,report,script,extra=()):
    paths=[Path(script),ROOT/'boundary_common.py',ROOT/'ACCEPTANCE.md',PARENT/'results/stage-integrity.json',*extra]
    report.update(state='complete',finished_utc=datetime.now(timezone.utc).isoformat(),
        script_sha256=digest(script),input_hashes={str(path):digest(path) for path in paths})
    write_json(folder/'status.json',report)
    (folder/'COMPLETE').write_text('complete\n',encoding='utf-8')


def seed_linear(momentum):
    squared=float(momentum@momentum)
    assert squared>0
    return 2*np.eye(3)-6*np.outer(momentum,momentum)/squared


def seed_pair(momentum_p,momentum_q):
    norm_p=float(momentum_p@momentum_p)
    norm_q=float(momentum_q@momentum_q)
    assert min(norm_p,norm_q)>0
    dot=float(momentum_p@momentum_q)
    projector_p=np.outer(momentum_p,momentum_p)/norm_p
    projector_q=np.outer(momentum_q,momentum_q)/norm_q
    return (2-3*dot*(1/norm_p+1/norm_q))*np.eye(3)-6*(projector_p+projector_q)+4.5*(projector_p@projector_q+projector_q@projector_p)


def linear_ricci(metric,momentum):
    squared=float(momentum@momentum)
    projected=metric@momentum
    return .5*(squared*metric+np.outer(momentum,momentum)*np.trace(metric)-np.outer(momentum,projected)-np.outer(projected,momentum))


def quadratic_ricci(metric_p,metric_q,momentum_p,momentum_q):
    geometry=inherited.inherited
    def coefficients(metric,momentum):
        first=1j*np.einsum('a,ij->aij',momentum,metric)
        second=-np.einsum('a,b,ij->abij',momentum,momentum,metric)
        return metric,first,second
    left=coefficients(metric_p,momentum_p)
    right=coefficients(metric_q,momentum_q)
    mixed=geometry.ricci_series(*(first+second for first,second in zip(left,right)))[1]
    separate=geometry.ricci_series(*left)[1]+geometry.ricci_series(*right)[1]
    return np.real_if_close((mixed-separate)/2)


def seed_geometry(momentum_p,momentum_q,neutrino_fraction):
    metric_p=seed_linear(momentum_p)
    metric_q=seed_linear(momentum_q)
    pair=seed_pair(momentum_p,momentum_q)
    total=momentum_p+momentum_q
    curvature_p=linear_ricci(metric_p,momentum_p)
    curvature_q=linear_ricci(metric_q,momentum_q)
    curvature2=linear_ricci(pair,total)+quadratic_ricci(metric_p,metric_q,momentum_p,momentum_q)
    denominator=15+4*neutrino_fraction
    def rate(curvature):
        scalar=np.trace(curvature)
        return -5/denominator*(curvature-np.eye(3)*scalar/3)-np.eye(3)*scalar/24
    rate_p,rate_q,rate2=[rate(value) for value in [curvature_p,curvature_q,curvature2]]
    metric_correction=rate2+(metric_p@rate_q+metric_q@rate_p)/2
    return dict(seed_p=metric_p,seed_q=metric_q,seed2=pair,ricci_p=curvature_p,ricci_q=curvature_q,
        ricci2=curvature2,scalar2=np.trace(curvature2),rate_p=rate_p,rate_q=rate_q,rate2=rate2,
        metric2_time_coefficient=metric_correction)
