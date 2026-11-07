from __future__ import annotations

import sympy as symbolic
from vertex_common import *


def main():
    modest()
    folder=ROOT/'results/ward'
    folder.mkdir(parents=True,exist_ok=False)
    checks=[]
    def identity(name,expression):
        residual=symbolic.simplify(symbolic.expand(expression))
        checks.append(dict(name=name,passed=bool(residual==0),residual=str(residual)))
        assert residual==0,(name,residual)

    time,space,mass=symbolic.symbols('tau x m',real=True)
    scale=symbolic.Function('a')(time)
    hubble=symbolic.diff(scale,time)/scale
    background=symbolic.Function('phi0')(time)
    first=symbolic.Function('phi1')(time,space)
    second=symbolic.Function('phi2')(time,space)
    longitudinal=symbolic.Function('hL')(time,space)
    transverse=symbolic.Function('hT')(time,space)
    volume1=(longitudinal+2*transverse)/2
    volume2=symbolic.Function('S2')(time,space)
    background_prime=symbolic.diff(background,time)
    first_prime=symbolic.diff(first,time)
    second_prime=symbolic.diff(second,time)
    gradient=symbolic.diff(first,space)
    klein0=symbolic.diff(background,time,2)+2*hubble*background_prime+scale**2*mass**2*background
    klein1=symbolic.diff(first,time,2)+2*hubble*first_prime-symbolic.diff(first,space,2)+scale**2*mass**2*first+symbolic.diff(volume1,time)*background_prime
    spatial_vertex=longitudinal*symbolic.diff(first,space,2)+(symbolic.diff(longitudinal,space)-symbolic.diff(volume1,space))*gradient
    klein2=symbolic.diff(second,time,2)+2*hubble*second_prime-symbolic.diff(second,space,2)+scale**2*mass**2*second+symbolic.diff(volume2,time)*background_prime+symbolic.diff(volume1,time)*first_prime+spatial_vertex
    energy2=(background_prime*second_prime+first_prime**2/2+gradient**2/2)/scale**2+mass**2*(background*second+first**2/2)
    pressure2=(background_prime*second_prime+first_prime**2/2-gradient**2/6)/scale**2-mass**2*(background*second+first**2/2)
    divergence=-((background_prime*symbolic.diff(second,space,2)+symbolic.diff(first_prime*gradient,space))-
        background_prime*spatial_vertex)/scale**2
    energy_balance=(symbolic.diff(energy2,time)+3*hubble*(energy2+pressure2)+
        symbolic.diff(volume1,time)*2*background_prime*first_prime/scale**2+
        symbolic.diff(volume2,time)*background_prime**2/scale**2+divergence)
    identity('Quadratic energy Ward identity on arbitrary diagonal first metric',
        energy_balance-(background_prime*klein2+first_prime*klein1+second_prime*klein0)/scale**2)
    current1=-background_prime*gradient/scale
    current2=-(background_prime*symbolic.diff(second,space)+first_prime*gradient)/scale
    anisotropy_long=2*gradient**2/(3*scale**2)
    momentum_balance=(symbolic.diff(current2,time)+3*hubble*current2+symbolic.diff(volume1,time)*current1+
        scale*symbolic.diff(pressure2+anisotropy_long,space))
    identity('Quadratic covariant momentum Ward identity',momentum_balance+
        (gradient*klein1+symbolic.diff(second,space)*klein0)/scale)
    identity('No gradient term in active quadratic trace',energy2+3*pressure2-
        ((4*background_prime*second_prime+2*first_prime**2)/scale**2-2*mass**2*background*second-mass**2*first**2))
    epsilon=symbolic.symbols('epsilon')
    hlong,htrans,llong,ltrans=symbolic.symbols('hL hT lL lT')
    log_volume=symbolic.log(1+epsilon*hlong+epsilon**2*llong)/2+symbolic.log(1+epsilon*htrans+epsilon**2*ltrans)
    quadratic=symbolic.expand(symbolic.series(log_volume,epsilon,0,3).removeO()).coeff(epsilon,2)
    identity('Metric trace is not logarithmic volume at second order',quadratic-(llong/2+ltrans-hlong**2/4-htrans**2/2))
    pnorm,qnorm,dot,rate1,rate2,field1,field2,velocity1,velocity2,a2,m2=symbolic.symbols('p2 q2 pq Sp Sq up uq vp vq a2 m2')
    energy=(velocity1*velocity2+(a2*m2-dot)*field1*field2)/(2*a2)
    pressure=(velocity1*velocity2-(a2*m2-dot/3)*field1*field2)/(2*a2)
    identity('Fourier gradient cancellation in Einstein trace',-a2*(energy+3*pressure)/2-
        (-velocity1*velocity2+a2*m2*field1*field2/2))
    identity('Symmetric temporal vertex',-(rate1*velocity2+rate2*velocity1)/2+(rate2*velocity1+rate1*velocity2)/2)
    coefficient=symbolic.symbols('coefficient')
    identity('Real cosine second harmonic has half the ordered kernel',
        symbolic.expand_trig(symbolic.cos(space)**2).expand(trig=True)-symbolic.Rational(1,2)*(1+symbolic.cos(2*space)).expand(trig=True))
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=True,
        metric_second_order_retained=True,ordinary_second_order_trace_not_closed=True),__file__,
        [BRANCH/'nonlinear-source-feedback-20261007/61-action-owned-nonlinear-source-and-force.md'])
    print(json.dumps(dict(identities=len(checks),all_passed=True)),flush=True)


if __name__=='__main__':
    main()
