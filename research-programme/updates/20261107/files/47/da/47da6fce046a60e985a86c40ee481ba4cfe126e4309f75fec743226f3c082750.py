from __future__ import annotations

from seed_common import *
import sympy as sp


def main():
    modest()
    folder=ROOT/'results/derivation'
    folder.mkdir(parents=True,exist_ok=False)
    checks=[]
    def identity(name,expression):
        residual=sp.simplify(sp.expand_trig(expression))
        checks.append(dict(name=name,passed=residual==0,residual=str(residual)))
        assert residual==0,(name,residual)
    fraction,volume_coeff,shear_coeff,nu_coeff=sp.symbols('fraction volume_coeff shear_coeff nu_coeff')
    equations=[1-16*volume_coeff,1-3*shear_coeff-3*fraction*nu_coeff,2*nu_coeff-sp.Rational(8,15)*shear_coeff]
    solved=sp.solve(equations,[volume_coeff,shear_coeff,nu_coeff],dict=True)[0]
    volume=solved[volume_coeff]
    shear=solved[shear_coeff]
    nu=solved[nu_coeff]
    for name,expression in zip(['Hamiltonian coefficient','tracefree Einstein coefficient','collisionless quadrupole coefficient'],equations):
        identity(name,expression.subs(solved))
    identity('cold seed curvature coefficient',volume-sp.Rational(1,16))
    response=1+4*fraction/15
    identity('neutrino shear denominator',shear-1/(3*response))
    identity('neutrino stress normalization',nu-4/(45*response))
    photon_velocity=volume/9
    neutrino_velocity=photon_velocity+nu/24
    identity('photon Euler coefficient',3*photon_velocity-volume/3)
    identity('neutrino Euler coefficient',3*neutrino_velocity-volume/3-nu/8)
    identity('momentum constraint via contracted spatial Bianchi identity',
        -4*volume/3+shear/6+4*((1-fraction)*photon_velocity+fraction*neutrino_velocity))
    identity('native radiation velocity ratio',neutrino_velocity/photon_velocity-(23+4*fraction)/(15+4*fraction))
    identity('native eta coefficient',(sp.Rational(1,2)-shear)/6-(5+4*fraction)/(12*(15+4*fraction)))
    identity('native neutrino shear coefficient',-nu/2+2/(3*(15+4*fraction)))
    field_coeff=sp.solve(42*sp.Symbol('field_coeff')+2*volume/5,sp.Symbol('field_coeff'))[0]
    identity('frozen scalar factor105',field_coeff/volume+sp.Rational(1,105))
    identity('frozen scalar curvature coefficient',field_coeff+sp.Rational(1,1680))
    coefficients=[sp.Integer(1)]
    responses=[sp.Integer(0)]
    for order in range(1,5):
        coefficients.append(-coefficients[-1]/(4*order*(4*order+1)))
        responses.append((sp.Rational(order,2)*coefficients[-1]-responses[-1])/((4*order+2)*(4*order+3)))
        identity('regular scalar recurrence '+str(order),
            (4*order+2)*(4*order+3)*responses[-1]+responses[-2]-sp.Rational(order,2)*coefficients[-1])
    epsilon,phase=sp.symbols('epsilon phase',real=True)
    zeta=epsilon*sp.cos(phase)
    curvature=sp.exp(-2*zeta)*(-4*sp.diff(zeta,phase,2)-2*sp.diff(zeta,phase)**2)
    second=sp.series(curvature,epsilon,0,3).removeO().expand().coeff(epsilon,2)
    identity('quadratic intrinsic curvature includes zero mode',second+5+3*sp.cos(2*phase))
    first_density=sp.cos(phase)/4
    displacement=-3*sp.sin(phase)
    transformed=second/16+displacement*sp.diff(first_density,phase)
    identity('native-chart quadratic density pullback',transformed-(1-9*sp.cos(2*phase))/16)
    identity('first-order spatial gauge sets native trace to zero',6*sp.cos(phase)+2*sp.diff(displacement,phase))
    identity('weighted integrated curvature is not zero',
        sp.integrate(second+3*sp.cos(phase)*4*sp.cos(phase),(phase,0,2*sp.pi))/(2*sp.pi)-1)
    psq,qsq,dot=sp.symbols('psq qsq dot',positive=True)
    kernel=-(psq+qsq)/4+dot/8
    pulled=kernel-3*dot*(psq/qsq+qsq/psq)/8
    identity('seed kernel symmetry',pulled-pulled.xreplace({psq:qsq,qsq:psq}))
    identity('seed kernel plane double mode',pulled.subs({qsq:psq,dot:psq})/2+9*psq/16)
    identity('seed kernel folded mode retained',pulled.subs({qsq:psq,dot:-psq})/2-psq/16)
    density,velocity,friction,pressure,gravity_first,gravity_second=sp.symbols('density velocity friction pressure gravity_first gravity_second')
    derived_velocity_derivative=velocity**2+density*(-friction*velocity+gravity_first-pressure*density)
    substituted_rhs=-friction*density*velocity+gravity_second-16*pressure*density**2+velocity**2+3*pressure*density**2
    identity('dust growing-seed residual in unequal multi-fluid system',
        derived_velocity_derivative-substituted_rhs-(density*gravity_first-gravity_second+12*pressure*density**2))
    coordinate=sp.symbols('coordinate',real=True)
    growing=sp.exp(coordinate)
    seedless=growing**2-growing
    identity('EdS zero-seed fractional deficit',(growing**2-seedless)/growing**2-sp.exp(-coordinate))
    sources=[BRANCH/'early-adiabatic-matching-20261006/51-early-adiabatic-onset-and-existing-growth-handoff.md',
        BRANCH/'native-two-field-transfer-20261007/54-native-canonical-fields-and-radiation.md',
        NATIVE/'fortran/MTSTwoField.f90']
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=True,
        solved_coefficients={str(key):str(value) for key,value in solved.items()},
        field_curvature_coefficient=str(field_coeff),
        scalar_background_series=[str(value) for value in coefficients],
        scalar_curvature_series=[str(value) for value in responses],
        seed_scope='Radiation dominated, regular adiabatic branch, second spatial-gradient order and velocity third-gradient order.',
        primordial_curvature_statistics_derived=False,full_radiation_onset_propagation=False),
        __file__,sources)
    print(json.dumps(dict(state='complete',identities=len(checks),coefficients={str(key):str(value) for key,value in solved.items()})))


if __name__=='__main__':
    main()
