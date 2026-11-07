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
PARENT=BRANCH/'survey-window-forward-model-20261007'
sys.path.insert(0,str(PARENT))
import window_common as previous
SPECTRUM=BRANCH/'resolved-matter-spectrum-20261007'
HUNIT=previous.HUNIT
KIN=previous.KIN
FAMILIES=['gaussian','laplace']
VARIANCE_GRID=np.linspace(0,64,129)


def modest():
    previous.modest()


def digest(path):
    return previous.digest(path)


def write_json(path,value):
    previous.write_json(path,value)


def finish(folder,report,script,extra=()):
    paths=[Path(script),ROOT/'velocity_common.py',ROOT/'ACCEPTANCE.md',PARENT/'window_common.py',
        PARENT/'results/stage-integrity.json',*extra]
    report.update(state='complete',finished_utc=datetime.now(timezone.utc).isoformat(),
        script_sha256=digest(script),input_hashes={str(path):digest(path) for path in paths})
    write_json(folder/'status.json',report)
    (folder/'COMPLETE').write_text('complete\n')


class AngularResponse:
    def __init__(self,label,nmu=64,method='cubic'):
        self.label=label
        self.geometry=previous.geometry(label)
        cosine,weight=np.polynomial.legendre.leggauss(nmu)
        perpendicular=self.geometry['q_perp'];parallel=self.geometry['q_parallel']
        stretch=np.sqrt((1-cosine**2)/perpendicular**2+cosine**2/parallel**2)
        wave=HUNIT*KIN[:,None]*stretch[None,:]
        true_cosine=cosine/parallel/stretch
        density_fn,velocity_fn=previous.transfer(label,method)
        density=np.exp(density_fn(np.log(wave)))
        velocity=np.exp(velocity_fn(np.log(wave)))
        primordial=2*math.pi**2/wave**3*previous.previous.previous.AS*(wave/.05)**(previous.previous.previous.NS-1)
        prefactor=primordial*HUNIT**3/(perpendicular**2*parallel)
        self.terms=np.stack([density**2,2*density*velocity*true_cosine[None,:]**2,
            velocity**2*true_cosine[None,:]**4],axis=0)*prefactor
        self.los_wave_squared=(wave*true_cosine[None,:]/HUNIT)**2
        self.projectors=np.array([(2*ell+1)/2*weight*special.eval_legendre(ell,cosine) for ell in [0,2,4,6,8]])

    def poles(self,variance,family='gaussian'):
        argument=variance*self.los_wave_squared
        if family=='gaussian':
            damping=np.exp(-argument)
        elif family=='laplace':
            damping=(1+.5*argument)**-2
        else:
            raise ValueError(family)
        return np.einsum('tij,ij,lj->tli',self.terms,damping,self.projectors,optimize=True)


def convolved(poles,operator):
    base=np.array([operator@term[:3].reshape(-1) for term in poles])
    white=np.zeros(1200);white[:400]=1.
    return np.vstack([base,operator@white])


def model(basis,bias,noise):
    return bias*bias*basis[0]+bias*basis[1]+basis[2]+noise*basis[3]


def fit_response(grid,table,data,covariance):
    spline=interpolate.CubicSpline(grid,table,axis=0)
    derivative=spline.derivative()
    chol=linalg.cholesky(covariance,lower=True)
    def residual(parameters):
        bias,variance,noise=parameters
        return linalg.solve_triangular(chol,model(spline(variance),bias,noise)-data,lower=True)
    def jacobian(parameters):
        bias,variance,noise=parameters
        basis=spline(variance)
        columns=np.column_stack([2*bias*basis[0]+basis[1],model(derivative(variance),bias,noise),basis[3]])
        return linalg.solve_triangular(chol,columns,lower=True)
    starts=[[1.3,.01,0],[2.,9.,0],[2.,36.,0],[2.5,63.,0]]
    solutions=[optimize.least_squares(residual,start,jac=jacobian,
        bounds=([.5,0.,-10000.],[4.,64.,10000.]),x_scale=[1,16,1000],
        ftol=1e-11,xtol=1e-11,gtol=1e-11,max_nfev=600) for start in starts]
    successful=[value for value in solutions if value.success]
    assert successful
    solution=min(successful,key=lambda value:value.fun@value.fun)
    bias,variance,noise=map(float,solution.x)
    raw=float(solution.fun@solution.fun)
    factor=(previous.NMOCK-len(data)-2)/(previous.NMOCK-1)
    return dict(bias=bias,variance=variance,sigma_displacement=math.sqrt(variance),noise=noise,
        chi2_raw=raw,chi2_hartlap=raw*factor,bins=len(data),hartlap_factor=factor,
        prediction=model(spline(variance),bias,noise).tolist(),converged=bool(solution.success),
        lower_variance_boundary=variance<1e-5,upper_variance_boundary=variance>64-1e-5,
        other_boundary=bool(min(bias-.5,4-bias)<1e-5 or min(noise+10000,10000-noise)<.1),
        starts=[dict(success=bool(value.success),chi2=float(value.fun@value.fun),parameters=value.x.tolist()) for value in solutions])
