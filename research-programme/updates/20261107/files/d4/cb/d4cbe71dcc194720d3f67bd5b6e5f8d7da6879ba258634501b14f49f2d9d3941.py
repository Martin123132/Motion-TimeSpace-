from __future__ import annotations

import os
import sys
os.environ['OMP_NUM_THREADS']='1'
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['MKL_NUM_THREADS']='1'
sys.dont_write_bytecode=True
from datetime import datetime, timezone
from pathlib import Path
import json
import math
import numpy as np
from scipy import integrate, interpolate, linalg, special

ROOT=Path(__file__).resolve().parent
BRANCH=ROOT.parent
POST=BRANCH.parent
PARENT=BRANCH/'density-weighted-pair-streaming-20261007'
sys.path.insert(0,str(PARENT))
import streaming_common as previous
SPECTRUM=previous.SPECTRUM
sys.path.insert(0,str(SPECTRUM))
import spectrum_common as evolution
NATIVE=BRANCH/'native-heavy-matching-20261007/native'
modest=previous.modest
digest=previous.digest
write_json=previous.write_json


def finish(folder,report,script,extra=()):
    paths=[Path(script),ROOT/'transport_common.py',ROOT/'ACCEPTANCE.md',PARENT/'results/stage-integrity.json',
        SPECTRUM/'spectrum_common.py',NATIVE/'fortran/equations.f90',NATIVE/'fortran/camb_python.f90',NATIVE/'camb/symbolic.py',*extra]
    report.update(state='complete',finished_utc=datetime.now(timezone.utc).isoformat(),
        script_sha256=digest(script),input_hashes={str(path):digest(path) for path in paths})
    write_json(folder/'status.json',report)
    (folder/'COMPLETE').write_text('complete\n')


def fields(label):
    packet=evolution.load_evolution(label)
    values=packet['values'];names=packet['names']
    background=np.load(SPECTRUM/'runs'/label/'background.npz')
    baryon_fraction=background['baryon']/(background['baryon']+background['cdm'])
    density=(1-baryon_fraction)*values[:,:,names.index('delta_cdm')]+baryon_fraction*values[:,:,names.index('delta_baryon')]
    velocity_cdm=values[:,:,names.index('v_newtonian_cdm')]
    velocity=(1-baryon_fraction)*velocity_cdm+baryon_fraction*values[:,:,names.index('v_newtonian_baryon')]
    wave=packet['modes'][:,None];hubble=values[:,:,names.index('H')]
    eta=values[:,:,names.index('etak')]/wave
    shear=-hubble*velocity_cdm/wave
    density_newtonian=density-3*hubble*shear/wave
    potential=eta-hubble*shear/wave
    conserved=density_newtonian-3*potential
    return packet,dict(density_sync=density,density_newtonian=density_newtonian,velocity=velocity,
        velocity_cdm=velocity_cdm,eta=eta,shear=shear,potential=potential,conserved=conserved,hubble=hubble,
        baryon_fraction=baryon_fraction,actual_scale=values[:,:,names.index('a')])


def derivative(values,requested,actual,redshift,step):
    center=-math.log1p(redshift)
    offsets=np.arange(-4,1) if redshift==0 else np.arange(-2,3)
    indices=np.array([int(np.argmin(abs(np.log(requested)-(center+offset*step)))) for offset in offsets])
    assert np.max(abs(np.log(requested[indices])-(center+offsets*step)))<1e-11
    weights=np.linalg.solve(np.vander(offsets,5,increasing=True).T,np.array([0.,1.,0.,0.,0.]))/step
    fixed=values[:,indices]@weights
    physical=[]
    for mode_index in range(len(values)):
        coordinate=(np.log(actual[mode_index,indices])-center)/step
        actual_weights=np.linalg.solve(np.vander(coordinate,5,increasing=True).T,np.array([0.,1.,0.,0.,0.]))/step
        physical.append(float(values[mode_index,indices]@actual_weights))
    return fixed,np.array(physical)


def flow_map(initial_phase,integrated_amplitude):
    decay=np.exp(-integrated_amplitude)
    half=initial_phase/2
    mapped=2*np.arctan2(decay*np.sin(half),np.cos(half))
    jacobian=decay/(np.cos(half)**2+decay**2*np.sin(half)**2)
    return mapped,jacobian
