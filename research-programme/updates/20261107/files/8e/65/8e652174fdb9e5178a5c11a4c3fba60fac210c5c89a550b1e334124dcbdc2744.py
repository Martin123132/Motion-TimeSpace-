from __future__ import annotations

import os
import sys
os.environ['OMP_NUM_THREADS']='1'
os.environ['OPENBLAS_NUM_THREADS']='1'
os.environ['MKL_NUM_THREADS']='1'
sys.dont_write_bytecode=True
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import numpy as np
import psutil
from scipy import integrate, interpolate, linalg, optimize, special

ROOT=Path(__file__).resolve().parent
BRANCH=ROOT.parent
POST=BRANCH.parent
PARENT=BRANCH/'resolved-matter-spectrum-20261007'
sys.path.insert(0,str(PARENT))
import spectrum_common as previous
HUNIT=.7
REDSHIFT=.38
KIN=(np.arange(400)+.5)*.001
KOUT=(np.arange(40)+.5)*.01
BIAS_BOUNDS=(.5,4.)
NOISE_BOUNDS=(-10000.,10000.)
NMOCK=2048


def modest():
    process=psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])


def digest(path):
    value=hashlib.sha256()
    with Path(path).open('rb') as handle:
        for block in iter(lambda:handle.read(1024*1024),b''):
            value.update(block)
    return value.hexdigest()


def write_json(path,value):
    Path(path).write_text(json.dumps(value,indent=2,allow_nan=False),encoding='utf-8')


def finish(folder,report,script,extra=()):
    paths=[Path(script),ROOT/'window_common.py',ROOT/'ACCEPTANCE.md',PARENT/'results/stage-integrity.json',*extra]
    report.update(state='complete',finished_utc=datetime.now(timezone.utc).isoformat(),
        script_sha256=digest(script),input_hashes={str(path):digest(path) for path in paths})
    write_json(folder/'status.json',report)
    (folder/'COMPLETE').write_text('complete\n')


def select(kmax=.1,ells=(0,2)):
    return np.flatnonzero(np.repeat(np.isin(np.arange(5),ells),40)&np.tile((KOUT>.02)&(KOUT<kmax),5))


def geometry(label):
    packet=np.load(PARENT/'runs'/label/'background.npz')
    index=int(np.argmin(abs(packet['redshifts']-REDSHIFT)))
    assert abs(packet['redshifts'][index]-REDSHIFT)<1e-12
    hubble=float(packet['H_km_s_Mpc'][index])
    distance=float(packet['DM'][index])
    efid=math.sqrt(.31*(1+REDSHIFT)**3+.69)
    distance_fid=2997.92458*integrate.quad(lambda redshift:1/math.sqrt(.31*(1+redshift)**3+.69),0,REDSHIFT,epsabs=1e-10)[0]
    return dict(q_perp=HUNIT*distance/distance_fid,q_parallel=100*HUNIT*efid/hubble,
        fiducial_Omega_m=.31,fiducial_H0_header=100.,fiducial_distance_Mpc_over_h=distance_fid,
        model_distance_Mpc=distance,model_H_km_s_Mpc=hubble,h_unit=HUNIT,z=REDSHIFT)


def transfer(label,method='cubic',template=False):
    packet=np.load(PARENT/'results/spectrum'/(label+'.npz'))
    index=int(np.argmin(abs(packet['scales']-1/(1+REDSHIFT))))
    assert abs(packet['scales'][index]-1/(1+REDSHIFT))<1e-12
    constructor=interpolate.CubicSpline if method=='cubic' else interpolate.PchipInterpolator
    density=packet['delta_cb'][:,index]
    velocity=packet['velocity_cb'][:,index]
    if template:
        report=json.loads((PARENT/'results/spectrum/status.json').read_text())
        branch=next(row for row in report['branches'] if row['label']==label)
        sigma=next(row['sigma8_cb'] for row in branch['central'] if row['z']==REDSHIFT)
        density=density/sigma
        velocity=density
    return constructor(np.log(packet['modes']),np.log(density)),constructor(np.log(packet['modes']),np.log(velocity))


def multipole_basis(label,geom=None,method='cubic',nmu=64,template=False,identity=False):
    geom=geometry(label) if geom is None else geom
    perpendicular,parallel=(1.,1.) if identity else (geom['q_perp'],geom['q_parallel'])
    cosine,weight=np.polynomial.legendre.leggauss(nmu)
    stretch=np.sqrt((1-cosine**2)/perpendicular**2+cosine**2/parallel**2)
    wave=HUNIT*KIN[:,None]*stretch[None,:]
    assert wave.min()>1e-5 and wave.max()<5.
    true_cosine=cosine/parallel/stretch
    density_fn,velocity_fn=transfer(label,method,template)
    density=np.exp(density_fn(np.log(wave)))
    velocity=np.exp(velocity_fn(np.log(wave)))
    primordial=2*math.pi**2/wave**3*previous.previous.AS*(wave/.05)**(previous.previous.NS-1)
    prefactor=primordial*HUNIT**3/(perpendicular**2*parallel)
    terms=np.stack([density**2,2*density*velocity*true_cosine[None,:]**2,
        velocity**2*true_cosine[None,:]**4],axis=0)*prefactor
    poles=[]
    for ell in [0,2,4,6,8]:
        poles.append((2*ell+1)/2*np.einsum('tij,j->ti',terms,weight*special.eval_legendre(ell,cosine)))
    return np.stack(poles,axis=1)


def physical_vector(basis,bias,noise=0.,velocity_scale=1.):
    values=bias*bias*basis[0]+bias*velocity_scale*basis[1]+velocity_scale**2*basis[2]
    return values+noise*basis[3]


def fit_nuisance(basis,data,covariance,bias_bounds=BIAS_BOUNDS,noise_bounds=NOISE_BOUNDS):
    chol=linalg.cholesky(covariance,lower=True)
    whiten=lambda value:linalg.solve_triangular(chol,value,lower=True)
    whitened=whiten(basis.T).T
    target=whiten(data)
    noise=whitened[3]
    def projected(bias):
        residual=target-bias*bias*whitened[0]-bias*whitened[1]-whitened[2]
        nuisance=float(np.clip(residual@noise/(noise@noise),*noise_bounds))
        return float(np.sum((residual-nuisance*noise)**2)),nuisance
    grid=np.linspace(*bias_bounds,201)
    values=np.array([projected(bias)[0] for bias in grid])
    candidates=[(values[0],grid[0]),(values[-1],grid[-1])]
    for index in range(1,len(grid)-1):
        if values[index]<=values[index-1] and values[index]<=values[index+1]:
            result=optimize.minimize_scalar(lambda bias:projected(bias)[0],bounds=(grid[index-1],grid[index+1]),
                method='bounded',options={'xatol':1e-12})
            assert result.success
            candidates.append((float(result.fun),float(result.x)))
    chi2,bias=min(candidates)
    _,nuisance=projected(bias)
    prediction=physical_vector(basis,bias,nuisance)
    count=len(data)
    factor=(NMOCK-count-2)/(NMOCK-1)
    return dict(bias=bias,noise=nuisance,chi2_raw=chi2,chi2_hartlap=chi2*factor,hartlap_factor=factor,
        bins=count,nuisance_parameters=2,boundary_hit=bool(min(abs(bias-value) for value in bias_bounds)<1e-4 or
        min(abs(nuisance-value) for value in noise_bounds)<1.),prediction=prediction.tolist())


def covariance_norm(vector,covariance):
    return float(np.sqrt(vector@linalg.solve(covariance,vector,assume_a='pos')))
