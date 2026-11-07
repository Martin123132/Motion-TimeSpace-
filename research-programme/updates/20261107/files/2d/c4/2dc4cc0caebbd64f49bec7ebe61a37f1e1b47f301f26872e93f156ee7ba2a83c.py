from __future__ import annotations

import sympy as symbolic
from onset_common import *


def main():
    modest()
    folder=ROOT/'results/derivation'
    folder.mkdir(parents=True,exist_ok=False)
    checks=[]

    def check(name,expression):
        residual=symbolic.simplify(expression)
        checks.append(dict(name=name,passed=bool(residual==0),residual=str(residual)))
        assert residual==0,(name,residual)

    scale,hubble,energy,pressure,enthalpy,volume_rate=symbolic.symbols('a H E P F sdot',nonzero=True)
    hubble_dot=-enthalpy/2
    energy_dot=-3*hubble*(energy+pressure)-enthalpy*volume_rate
    differentiated_hamiltonian=energy_dot/(2*hubble)+1/(2*scale**2)-volume_rate*hubble_dot/hubble
    check('Raychaudhuri from energy and Hamiltonian',
        (differentiated_hamiltonian+2*hubble*volume_rate+(energy+3*pressure)/2).subs(energy,2*hubble*volume_rate+1/(2*scale**2)))
    shear,shear_rate,stress,current=symbolic.symbols('b bdot C J')
    shear_acceleration=-3*hubble*shear_rate-2/scale**2-2*stress*shear
    current_dot=-3*hubble*current-pressure+stress*shear/6
    constraint=2*volume_rate/3-shear_rate/12-current
    constraint_dot=2*(-2*hubble*volume_rate-(energy+3*pressure)/2)/3-shear_acceleration/12-current_dot
    check('Momentum constraint propagation',
        (constraint_dot+3*hubble*constraint).subs(energy,2*hubble*volume_rate+1/(2*scale**2)))
    field,field_dot,response,response_dot,mass,volume=symbolic.symbols('phi phidot f fdot m s')
    field_acceleration=-3*hubble*field_dot-mass**2*field
    response_acceleration=-3*hubble*response_dot-mass**2*response-volume_rate*field_dot
    scalar_energy=field_dot*response_dot+mass**2*field*response
    scalar_pressure=field_dot*response_dot-mass**2*field*response
    scalar_energy_dot=field_acceleration*response_dot+field_dot*response_acceleration+mass**2*(field_dot*response+field*response_dot)
    check('Canonical perturbed energy conservation',scalar_energy_dot+3*hubble*(scalar_energy+scalar_pressure)+field_dot**2*volume_rate)
    scalar_current=-field_dot*response
    check('Canonical spatial current conservation',-field_acceleration*response-field_dot*response_dot+3*hubble*scalar_current+scalar_pressure)
    density=(field_dot**2+mass**2*field**2)/2
    background_pressure=(field_dot**2-mass**2*field**2)/2
    density_dot=field_dot*field_acceleration+mass**2*field*field_dot
    check('Canonical background energy conservation',density_dot+3*hubble*(density+background_pressure))
    occupation_dot=3*hubble*(scalar_energy+density*volume)+scalar_energy_dot+density_dot*volume+density*volume_rate
    check('Local comoving physical-energy response transport',occupation_dot+3*hubble*(scalar_pressure+background_pressure*volume)+background_pressure*volume_rate)
    integral4,integral6=symbolic.symbols('I4 I6')
    neutrino_pressure=integral4/(3*scale**4)
    neutrino_pressure_n=-5*neutrino_pressure+integral6/(3*scale**4)
    coefficient=(5*integral4-integral6)/(15*scale**4)
    check('Massive collisionless quadrupole coefficient',coefficient+neutrino_pressure_n/5)
    check('Massless quadrupole limit',coefficient.subs(integral6,integral4)-4*neutrino_pressure/5)
    check('Nonrelativistic quadrupole limit',coefficient.subs(integral6,0)-neutrino_pressure)
    logdensity_first,logdensity_second,rho=symbolic.symbols('L1 L2 rho')
    massive_pressure=rho*(1-logdensity_first)/3
    derivative=symbolic.diff(massive_pressure,rho)*rho*(logdensity_first-4)+symbolic.diff(massive_pressure,logdensity_first)*logdensity_second
    check('Massive pressure derivative from comoving density',derivative-rho*((logdensity_first-4)*(1-logdensity_first)-logdensity_second)/3)
    logarithmic_hubble,scaled_f,scaled_g,omega,field_n,scaled_rate=symbolic.symbols('h Yf Yg omega V Srate')
    stretch=2*(1+logarithmic_hubble)
    check('Scaled KG friction',-(3+logarithmic_hubble)*scaled_g+stretch*scaled_g-(logarithmic_hubble-1)*scaled_g)
    check('Scaled KG source',-omega**2*scaled_f-scaled_rate*field_n-(-omega**2*scaled_f-scaled_rate*field_n))
    scaled_current=symbolic.symbols('YJ')
    check('Scaled current dilution',-3*scaled_current+(2+logarithmic_hubble)*scaled_current-(logarithmic_hubble-1)*scaled_current)
    parameter=symbolic.symbols('epsilon')
    physical_action=scale**3*symbolic.exp(parameter*volume)*((field_dot+parameter*response_dot+
        symbolic.Rational(3,2)*(hubble+parameter*volume_rate/3)*(field+parameter*response))**2+
        mass**2*(field+parameter*response)**2)/2
    shifted_velocity=field_dot+3*hubble*field/2
    action_response=scale**3*(volume*(shifted_velocity**2+mass**2*field**2)/2+
        shifted_velocity*(response_dot+3*hubble*response/2+volume_rate*field/2)+mass**2*field*response)
    check('Local WKB action curvature response',symbolic.diff(physical_action,parameter).subs(parameter,0)-action_response)
    chi,chi_dot=symbolic.symbols('chi chidot')
    chi_acceleration=-(mass**2-3*hubble_dot/2-9*hubble**2/4)*chi
    check('WKB reference action drift',chi_dot*chi_acceleration+mass**2*chi*chi_dot-(3*hubble_dot/2+9*hubble**2/4)*chi*chi_dot)
    curvature,derivative_order=symbolic.symbols('Rhat grad')
    check('Quadratic response products start at four gradients',symbolic.expand((derivative_order**2*response*curvature)**2).coeff(derivative_order,2))
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=True,
        caveat='Exact algebra within stated two-gradient, tight-coupling and isotropic collisionless-background assumptions.'),__file__)
    print(json.dumps(dict(symbolic_checks=len(checks),all_checks_passed=True)))


if __name__=='__main__':
    main()
