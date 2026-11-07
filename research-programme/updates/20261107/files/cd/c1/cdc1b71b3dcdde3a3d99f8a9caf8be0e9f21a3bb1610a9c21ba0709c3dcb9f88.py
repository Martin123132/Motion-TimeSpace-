from __future__ import annotations

import sympy as symbolic
from constraint_common import *


def main():
    modest()
    folder=ROOT/'results/constraint-propagation'
    folder.mkdir(parents=True,exist_ok=False)
    coordinates=symbolic.symbols('tau x y z',real=True)
    time=coordinates[0]
    scale=symbolic.Function('a')(time)
    hubble=symbolic.diff(scale,time)/scale
    hres=symbolic.Function('Hc')(*coordinates)
    mres=[symbolic.Function('M'+str(index))(*coordinates) for index in range(3)]
    metric=symbolic.diag(-scale**2,scale**2,scale**2,scale**2)
    inverse=metric.inv()
    residual=symbolic.diag(hres/2,hres/2,hres/2,hres/2)
    for index in range(3):
        residual[0,index+1]=residual[index+1,0]=-mres[index]
    mixed=inverse*residual
    connection=[[[symbolic.simplify(sum(inverse[upper,lower]*(symbolic.diff(metric[lower,right],coordinates[left])+symbolic.diff(metric[lower,left],coordinates[right])-symbolic.diff(metric[left,right],coordinates[lower])) for lower in range(4))/2) for right in range(4)] for left in range(4)] for upper in range(4)]
    divergence=[symbolic.simplify(sum(symbolic.diff(mixed[upper,lower],coordinates[upper])+sum(connection[upper][upper][middle]*mixed[middle,lower]-connection[middle][upper][lower]*mixed[upper,middle] for middle in range(4)) for upper in range(4))) for lower in range(4)]
    checks=[]
    def identity(name,expression):
        simplified=symbolic.simplify(expression)
        checks.append(dict(name=name,passed=bool(simplified==0),residual=str(simplified)))
        assert simplified==0,(name,simplified)
    energy_equation=symbolic.diff(hres,time)+4*hubble*hres+2*sum(symbolic.diff(mres[index],coordinates[index+1]) for index in range(3))
    identity('Contracted Bianchi Hamiltonian propagation',divergence[0]+energy_equation/(2*scale**2))
    for index in range(3):
        momentum_equation=symbolic.diff(mres[index],time)+2*hubble*mres[index]+symbolic.diff(hres,coordinates[index+1])/2
        identity('Contracted Bianchi momentum propagation '+str(index),divergence[index+1]-momentum_equation/scale**2)
    substitutions={symbolic.diff(hres,time):-4*hubble*hres-2*sum(symbolic.diff(mres[index],coordinates[index+1]) for index in range(3))}
    substitutions.update({symbolic.diff(mres[index],time):-2*hubble*mres[index]-symbolic.diff(hres,coordinates[index+1])/2 for index in range(3)})
    norm=hres**2+4*sum(component**2 for component in mres)
    flux=sum(symbolic.diff(hres*mres[index],coordinates[index+1]) for index in range(3))
    identity('Positive constraint-error norm obeys expanding-background balance',
        symbolic.diff(norm,time).subs(substitutions)+8*hubble*hres**2+16*hubble*sum(component**2 for component in mres)+4*flux)
    curvature,theta,theta_prime,shear2,energy,pressure=symbolic.symbols('R theta thetap sigma2 E P')
    ham=curvature+4*hubble*theta+2*theta**2/3-shear2-2*scale**2*energy
    spatial_trace=theta_prime+5*hubble*theta+theta**2+curvature-3*scale**2*(energy-pressure)/2
    normal_trace=theta_prime+hubble*theta+theta**2/3+shear2+scale**2*(energy+3*pressure)/2
    identity('Spatial trace and Raychaudhuri differ by the Hamiltonian constraint',spatial_trace-normal_trace-ham)
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=True,
        evolution_choice='spatial Ricci Einstein equations, not Raychaudhuri off the constraint surface',
        assumptions=['background and first-order Einstein equations hold','matter Ward identities hold to second order','periodic or vanishing flux for integrated norm'],
        first_order_numerical_residuals_require_source_terms=True),__file__)
    print(json.dumps(dict(identities=len(checks))),flush=True)


if __name__=='__main__':
    main()
