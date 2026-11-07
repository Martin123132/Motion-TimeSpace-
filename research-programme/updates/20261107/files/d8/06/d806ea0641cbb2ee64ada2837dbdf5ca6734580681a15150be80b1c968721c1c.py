from __future__ import annotations

import sympy as symbolic
from vertex_common import *


def main():
    modest()
    folder=ROOT/'results/volume-equation'
    folder.mkdir(parents=True,exist_ok=False)
    time,coord_x,coord_y,coord_z=symbolic.symbols('t x y z',real=True)
    coordinates=[time,coord_x,coord_y,coord_z]
    scale=symbolic.Function('a')(time)
    components=[symbolic.Function(label)(time) for label in ['C1','C2','C3']]
    metric=symbolic.diag(-scale**2,*[scale**2*component for component in components])
    inverse=metric.inv()
    connection=[[[symbolic.simplify(sum(inverse[upper,lower]*(symbolic.diff(metric[lower,right],coordinates[left])+symbolic.diff(metric[lower,left],coordinates[right])-symbolic.diff(metric[left,right],coordinates[lower])) for lower in range(4))/2) for right in range(4)] for left in range(4)] for upper in range(4)]
    ricci00=symbolic.simplify(sum(symbolic.diff(connection[upper][0][0],coordinates[upper])-symbolic.diff(connection[upper][0][upper],time)+sum(connection[upper][upper][middle]*connection[middle][0][0]-connection[upper][0][middle]*connection[middle][0][upper] for middle in range(4)) for upper in range(4)))
    theta=symbolic.log(symbolic.prod(components))/2
    hubble=symbolic.diff(scale,time)/scale
    rates=[symbolic.diff(component,time)/component for component in components]
    expected=-3*symbolic.diff(hubble,time)-symbolic.diff(theta,time,2)-hubble*symbolic.diff(theta,time)-sum(rate**2 for rate in rates)/4
    checks=[]
    def identity(name,expression):
        residual=symbolic.simplify(expression)
        checks.append(dict(name=name,passed=bool(residual==0),residual=str(residual)))
        assert residual==0,(name,residual)
    identity('R00 from direct connection equals volume/shear identity',ricci00-expected)
    trace=symbolic.symbols('trace')
    first,second,third=symbolic.symbols('h1prime h2prime h3prime')
    volume_rate=(first+second+third)/2
    shear2=sum((entry-(first+second+third)/3)**2 for entry in [first,second,third])/4
    identity('Quadratic geometric source includes volume and tracefree shear',sum(entry**2 for entry in [first,second,third])/4-volume_rate**2/3-shear2)
    epsilon=symbolic.symbols('epsilon')
    h1=symbolic.Function('h1')(time)
    h2=symbolic.Function('h2')(time)
    h3=symbolic.Function('h3')(time)
    l1=symbolic.Function('l1')(time)
    l2=symbolic.Function('l2')(time)
    l3=symbolic.Function('l3')(time)
    theta2=(l1+l2+l3)/2-(h1**2+h2**2+h3**2)/4
    volume_linear=(h1+h2+h3)/2
    exact_volume=symbolic.log(symbolic.prod([1+epsilon*hvalue+epsilon**2*lvalue for hvalue,lvalue in zip([h1,h2,h3],[l1,l2,l3])]))/2
    coefficient=symbolic.diff(exact_volume,epsilon,2).subs(epsilon,0)/2
    identity('Independent second-order volume kept in R00',coefficient-theta2)
    bprime,vprime,uprime,bfield,vfield,ufield,mass,grad2=symbolic.symbols('bp vp up b v u m grad2')
    energy=(bprime*vprime+uprime**2/2+grad2/2)/scale**2+mass**2*(bfield*vfield+ufield**2/2)
    pressure=(bprime*vprime+uprime**2/2-grad2/6)/scale**2-mass**2*(bfield*vfield+ufield**2/2)
    identity('Einstein volume split into linear field2 and pure quadratic source',
        scale**2*(energy+3*pressure)/2-(2*bprime*vprime-scale**2*mass**2*bfield*vfield+uprime**2-scale**2*mass**2*ufield**2/2))
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=True,
        direct_connection_check='homogeneous diagonal metric with three independent scale factors',
        spatially_varying_generalization='Unit-lapse zero-shift Rnn contains the same local time-extrinsic-curvature terms; no spatial Ricci contribution to Rnn.',
        ordinary_species_second_order_trace_explicit=True),__file__)
    print(json.dumps(dict(exact_checks=len(checks))),flush=True)


if __name__=='__main__':
    main()
