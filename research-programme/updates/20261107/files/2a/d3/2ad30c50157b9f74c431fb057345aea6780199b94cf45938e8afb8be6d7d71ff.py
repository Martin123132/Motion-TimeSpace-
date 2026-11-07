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
from scipy import interpolate

ROOT=Path(__file__).resolve().parent
BRANCH=ROOT.parent
POST=BRANCH.parent
PARENT=BRANCH/'full-history-source-precision-20261007'
NATIVE=BRANCH/'native-heavy-matching-20261007/native'
sys.path.insert(0,str(PARENT))
import precision_common as inherited
modest=inherited.modest
digest=inherited.digest
write_json=inherited.write_json


def finish(folder,report,script,extra=()):
    paths=[Path(script),ROOT/'vertex_common.py',ROOT/'ACCEPTANCE.md',PARENT/'results/stage-integrity.json',*extra]
    report.update(state='complete',finished_utc=datetime.now(timezone.utc).isoformat(),
        script_sha256=digest(script),input_hashes={str(path):digest(path) for path in paths})
    write_json(folder/'status.json',report)
    (folder/'COMPLETE').write_text('complete\n',encoding='utf-8')


def metric(mode,direction,names,values,baryon_fraction):
    columns={name:values[:,index] for index,name in enumerate(names)}
    trace=-2*columns['delta_cdm']
    eta=columns['etak']/mode
    volume=trace/2
    cb=(1-baryon_fraction)*columns['delta_cdm']+baryon_fraction*columns['delta_baryon']
    volume_prime=-columns['H']*columns['growth']*cb-baryon_fraction*mode*columns['v_baryon_cdm']
    projector=np.outer(direction,direction)-np.eye(3)/3
    spatial=trace[:,None,None]*np.eye(3)/3+(trace+6*eta)[:,None,None]*projector
    tracefree_prime=-2*columns['H'][:,None,None]*columns['v_newtonian_cdm'][:,None,None]*projector
    return volume,volume_prime,spatial,tracefree_prime


def vertices(momentum_p,momentum_q,metric_p,metric_q,field_p,field_q,prime_p,prime_q,scale,mass):
    total=momentum_p+momentum_q
    dot=float(momentum_p@momentum_q)
    volume_p,rate_p,spatial_p,shear_p=metric_p
    volume_q,rate_q,spatial_q,shear_q=metric_q
    temporal=-(rate_p*prime_q+rate_q*prime_p)/2
    spatial=((np.einsum('i,tij,j->t',total,spatial_p,momentum_q)-dot*volume_p)*field_q+
        (np.einsum('i,tij,j->t',total,spatial_q,momentum_p)-dot*volume_q)*field_p)/2
    product=field_p*field_q
    kinetic=prime_p*prime_q
    energy=(kinetic+(scale**2*mass**2-dot)*product)/(2*scale**2)
    pressure=(kinetic-(scale**2*mass**2-dot/3)*product)/(2*scale**2)
    momentum_imaginary=-(prime_p[:,None]*field_q[:,None]*momentum_q+prime_q[:,None]*field_p[:,None]*momentum_p)/(2*scale[:,None])
    tensor=(np.outer(momentum_p,momentum_q)+np.outer(momentum_q,momentum_p))/2-np.eye(3)*dot/3
    anisotropy=-product[:,None,None]*tensor/scale[:,None,None]**2
    geometric_trace=-rate_p*rate_q/3-np.einsum('tij,tij->t',shear_p,shear_q)/4
    canonical_trace=-kinetic+scale**2*mass**2*product/2
    return dict(KG_temporal=temporal,KG_spatial=spatial,KG_total=temporal+spatial,
        E_quadratic=energy,P_quadratic=pressure,j_quadratic_imaginary=momentum_imaginary,
        anisotropic_stress=anisotropy,Einstein_volume_geometric=geometric_trace,
        Einstein_volume_canonical=canonical_trace)
