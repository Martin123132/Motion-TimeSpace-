from __future__ import annotations

import sympy as symbolic
from boundary_common import *


def main():
    modest()
    folder=ROOT/'results/regular-seed'
    folder.mkdir(parents=True,exist_ok=False)
    fraction,tau,curvature,beta,mass,field0=symbolic.symbols('f tau R beta mass phi0',positive=True)
    denominator=15+4*fraction
    trace_rate=-curvature*tau/8
    radiation=curvature*tau**2/12
    dust=curvature*tau**2/16
    shear_coefficient=-5*tau/denominator
    neutrino_stress=4*tau**2/(3*denominator)
    photon_velocity=-tau**3/144
    neutrino_velocity=-tau**3*(denominator+8)/(144*denominator)
    scalar_background_prime=-beta**2*mass**2*field0*tau**3/5
    scalar_response=-curvature*beta**2*mass**2*field0*tau**6/1680
    checks=[]
    def identity(name,expression):
        residual=symbolic.factor(expression)
        checks.append(dict(name=name,passed=residual==0,residual=str(residual)))
        assert residual==0,(name,residual)
    identity('Radiation gradient2 Hamiltonian constraint',curvature+4*trace_rate/tau-6*radiation/tau**2)
    identity('Radiation gradient2 continuity',symbolic.diff(radiation,tau)+4*trace_rate/3)
    identity('Comoving dust gradient2 continuity',symbolic.diff(dust,tau)+trace_rate)
    identity('Radiation entropy relative to dust vanishes',radiation-4*dust/3)
    identity('Trace spatial-Ricci evolution',symbolic.diff(trace_rate,tau)+5*trace_rate/tau+curvature-3*radiation/tau**2)
    identity('Neutrino shear moment',symbolic.diff(neutrino_stress,tau)+8*shear_coefficient/15)
    identity('Tracefree Einstein evolution with neutrino anisotropy',symbolic.diff(shear_coefficient,tau)+2*shear_coefficient/tau+1-3*fraction*neutrino_stress/tau**2)
    identity('Photon gradient3 Euler response',symbolic.diff(photon_velocity,tau)+tau**2/48)
    identity('Neutrino gradient3 Euler response',symbolic.diff(neutrino_velocity,tau)+tau**2/48+symbolic.Rational(3,4)*neutrino_stress/6)
    geometric_momentum=-tau/12-shear_coefficient/6
    matter_momentum=4*((1-fraction)*photon_velocity+fraction*neutrino_velocity)/tau**2
    identity('Gradient3 momentum constraint uses Bianchi divergence of Ricci',geometric_momentum-matter_momentum)
    identity('Frozen canonical background leading KG',symbolic.diff(scalar_background_prime,tau)+2*scalar_background_prime/tau+beta**2*tau**2*mass**2*field0)
    identity('Regular canonical curvature response leading KG',symbolic.diff(scalar_response,tau,2)+2*symbolic.diff(scalar_response,tau)/tau+trace_rate*scalar_background_prime)
    gradient_phi,gradient_lap=symbolic.symbols('gradPhi gradLaplacian')
    flux_from_brightness=-tau**3/symbolic.Integer(108)-2*tau**3/(27*denominator)
    identity('Covariant brightness gradient3 reproduces neutrino dipole',symbolic.Rational(3,4)*flux_from_brightness-neutrino_velocity)
    identity('Single-mode native regular density normalization',radiation.subs(curvature,4)-tau**2/3)
    identity('Field response agrees with inherited105 regular coefficient',scalar_response+field0*(mass*beta*tau**2)**2*dust/105)
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=True,
        expansion='Radiation-dominated leading gradient2 metric/density, gradient3 momentum; arbitrary scalar amplitude before perturbative extraction',
        neutrino_fraction_symbolic=True,primordial_curvature_function_not_predicted=True,
        additional_independent_isocurvature_modes_not_fixed=True,
        retained_scalar_coefficient=str(scalar_response),neutrino_shear_denominator=str(denominator)),__file__)
    print(json.dumps(dict(checks=len(checks))),flush=True)


if __name__=='__main__':
    main()
