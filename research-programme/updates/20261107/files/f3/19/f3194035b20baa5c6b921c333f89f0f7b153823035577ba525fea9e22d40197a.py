from __future__ import annotations

from feedback_common import *
import sympy as sp


def main():
    modest()
    folder=ROOT/'results/mode-kernels'
    folder.mkdir(parents=True,exist_ok=False)
    checks=[]
    def identity(name,expression):
        residual=sp.factor(expression)
        checks.append(dict(name=name,passed=residual==0,residual=str(residual)))
        assert residual==0,(name,residual)
    psq,qsq,dot,mass,scale,hubble=sp.symbols('psq qsq dot mass scale hubble',positive=True)
    ksq=psq+qsq+2*dot
    alpha=1+dot*(1/psq+1/qsq)/2
    beta=ksq*dot/(2*psq*qsq)
    pressure_kernel=ksq*(psq+qsq+dot)/(8*mass**2*scale**2*hubble**2)
    density_kernel=5*alpha/7+2*beta/7
    velocity_kernel=3*alpha/7+4*beta/7
    identity('cold EdS continuity kernel',2*density_kernel-velocity_kernel-alpha)
    identity('cold EdS Euler kernel',sp.Rational(5,2)*velocity_kernel-sp.Rational(3,2)*density_kernel-beta)
    for name,expression in [('alpha',alpha),('beta',beta),('quantum',pressure_kernel)]:
        identity(name+' exchange symmetry',expression-expression.xreplace({psq:qsq,qsq:psq}))
        identity(name+' folded zero mode',expression.subs({qsq:psq,dot:-psq}))
    identity('plane-wave density amplitude matches Stage61',density_kernel.subs({qsq:psq,dot:psq})/2-1)
    identity('plane-wave velocity amplitude matches Stage61',velocity_kernel.subs({qsq:psq,dot:psq})/2-1)
    jeans=psq**2/(4*mass**2*scale**2*hubble**2)
    identity('quantum convolution gives factor three not independent parameter',
        pressure_kernel.subs({qsq:psq,dot:psq})/2-3*jeans)
    identity('second-harmonic Jeans gives factor sixteen',
        (4*psq)**2/(4*mass**2*scale**2*hubble**2)-16*jeans)
    cosine,ratio=sp.symbols('cosine ratio',real=True,positive=True)
    known=sp.Rational(5,7)+cosine*(ratio+1/ratio)/2+sp.Rational(2,7)*cosine**2
    identity('standard cold F2 angular form',density_kernel.subs({psq:ratio**2,qsq:1,dot:ratio*cosine})-known)
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=True,
        quantum_kernel=str(pressure_kernel),alpha_symmetrized=str(alpha),beta=str(beta),
        cold_density_kernel=str(density_kernel),cold_velocity_kernel=str(velocity_kernel),
        full_mode_coupled_cosmological_solution=False),
        __file__,[ROOT/'results/derivation/status.json'])
    print(json.dumps(dict(state='complete',kernel_identities=len(checks))))


if __name__=='__main__':
    main()
