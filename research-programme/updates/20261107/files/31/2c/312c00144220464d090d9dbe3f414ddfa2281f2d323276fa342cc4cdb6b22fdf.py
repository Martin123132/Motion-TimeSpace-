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
PARENT=BRANCH/'shared-velocity-response-20261007'
sys.path.insert(0,str(PARENT))
import velocity_common as previous
survey=previous.previous
SPECTRUM=previous.SPECTRUM
HUNIT=previous.HUNIT
SEPARATIONS=np.array([0.,.5,1.,2.,5.,10.,20.,30.,40.,50.,60.,80.,100.,120.,150.,200.,250.,300.])
COSINES=[0.,.5,1.]
modest=previous.modest
digest=previous.digest
write_json=previous.write_json


def finish(folder,report,script,extra=()):
    paths=[Path(script),ROOT/'streaming_common.py',ROOT/'ACCEPTANCE.md',PARENT/'velocity_common.py',
        PARENT/'results/stage-integrity.json',*extra]
    report.update(state='complete',finished_utc=datetime.now(timezone.utc).isoformat(),
        script_sha256=digest(script),input_hashes={str(path):digest(path) for path in paths})
    write_json(folder/'status.json',report)
    (folder/'COMPLETE').write_text('complete\n')


def correlations(label,nodes=32769,method='cubic',upper=5.):
    density_fn,velocity_fn=survey.transfer(label,method)
    logarithm=np.linspace(math.log(1e-5),math.log(upper),nodes)
    wave=np.exp(logarithm)
    density=np.exp(density_fn(logarithm));velocity=np.exp(velocity_fn(logarithm))
    primordial=2*math.pi**2/wave**3*survey.previous.previous.AS*(wave/.05)**(survey.previous.previous.NS-1)
    density_power=primordial*density*density
    mixed_power=primordial*density*velocity
    velocity_power=primordial*velocity*velocity
    integral=lambda values:float(integrate.simpson(values,x=logarithm))
    variance_density=integral(wave**3*density_power)/(2*math.pi**2)
    variance_displacement=HUNIT**2*integral(wave*velocity_power)/(6*math.pi**2)
    rows=[]
    for separation in SEPARATIONS:
        phase=wave*separation/HUNIT
        spherical0=special.spherical_jn(0,phase)
        spherical1=special.spherical_jn(1,phase)
        spherical2=special.spherical_jn(2,phase)
        correlation=integral(wave**3*density_power*spherical0)/(2*math.pi**2)
        cross_radial=-HUNIT*integral(wave**2*mixed_power*spherical1)/(2*math.pi**2)
        for cosine in COSINES:
            kernel=1-spherical0+2*special.eval_legendre(2,cosine)*spherical2
            pair_variance=HUNIT**2*integral(wave*velocity_power*kernel)/(3*math.pi**2)
            rows.append(dict(separation_Mpc_over_h=float(separation),LOS_cosine=cosine,
                xi_cb=correlation,cross_Mpc_over_h=float(cosine*cross_radial),
                pair_variance_Mpc_over_h_squared=pair_variance))
    return dict(rows=rows,variance_density=variance_density,variance_displacement=variance_displacement,
        nodes=nodes,method=method,upper_q_Mpc_inverse=upper)


def weighted_moments(correlation,cross,variance):
    normalization=1+correlation
    assert normalization>0
    mean=2*cross/normalization
    raw_second=variance+2*cross**2/normalization
    central=raw_second-mean**2
    third=4*cross**3*(1-3*correlation)/normalization**3
    fourth=-12*cross**4*(1-6*correlation+correlation**2)/normalization**4
    return dict(pair_weight=normalization,mean=mean,raw_second=raw_second,central_variance=central,
        third_cumulant=third,fourth_cumulant=fourth)


def positivity(correlation,cross,variance):
    normalization=1+correlation
    if normalization<=0:
        return dict(normalizable_positive_pair_weight=False,nonnegative=False,negative_mass=None)
    if variance==0:
        assert cross==0
        return dict(normalizable_positive_pair_weight=True,nonnegative=True,negative_mass=0.,point_mass=True)
    if cross==0:
        return dict(normalizable_positive_pair_weight=True,nonnegative=True,negative_mass=0.,point_mass=False)
    ratio=cross/math.sqrt(variance)
    discriminant=ratio**2-correlation
    minimum=(correlation-ratio**2)/normalization
    result=dict(normalizable_positive_pair_weight=True,nonnegative=discriminant<=0,
        minimum_polynomial=minimum,vertex_in_sigma=-1/ratio,point_mass=False,
        positivity_margin=correlation-ratio**2)
    if discriminant<=0:
        result['negative_mass']=0.
        return result
    center=-1/ratio;halfwidth=math.sqrt(discriminant)/abs(ratio)
    lower=center-halfwidth;upper=center+halfwidth
    def negative_integrand(coordinate):
        polynomial=ratio**2/normalization*((coordinate-center)**2-halfwidth**2)
        return -polynomial*math.exp(-.5*coordinate**2)/math.sqrt(2*math.pi)
    edges=sorted(set([lower,upper]+[point for point in [-40.,-12.,-6.,0.,6.,12.,40.] if lower<point<upper]))
    mass=0.;error=0.
    for left,right in zip(edges[:-1],edges[1:]):
        value,uncertainty=integrate.quad(negative_integrand,left,right,epsabs=1e-16,epsrel=1e-10,limit=200)
        mass+=value;error+=uncertainty
    result.update(negative_mass=float(mass),negative_mass_quadrature_error=float(error),
        negative_interval_in_sigma=[lower,upper],underflow_possible=mass==0.)
    return result


def generating(moment_parameter,correlation,cross,variance):
    normalization=1+correlation
    return np.exp(variance*moment_parameter**2/2)*(1+2*cross*moment_parameter/normalization+cross**2*moment_parameter**2/normalization)
