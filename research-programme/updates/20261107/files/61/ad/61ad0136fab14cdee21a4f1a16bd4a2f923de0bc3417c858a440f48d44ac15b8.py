from __future__ import annotations

import sympy as symbolic
from boundary_common import *


def coefficients(fraction,baryon_share):
    denominator=15+4*fraction
    shear0=-5/denominator
    shear_matter=3*(4*fraction-5)*shear0/(8*(15+2*fraction))
    shear_collision=-8*(1-fraction)*shear0/(15+2*fraction)
    loading=3*baryon_share/(4*(1-fraction))
    photon0=-1/144
    photon_matter=1/960+loading/144
    photon_collision=shear0/45
    neutrino0=-1/144+shear0/90
    neutrino_matter=1/960+shear_matter/180
    neutrino_collision=shear_collision/180
    return dict(shear0=shear0,shear_matter=shear_matter,shear_collision=shear_collision,
        photon0=photon0,photon_matter=photon_matter,photon_collision=photon_collision,
        neutrino0=neutrino0,neutrino_matter=neutrino_matter,neutrino_collision=neutrino_collision)


def main():
    modest()
    folder=ROOT/'results/matter-correction'
    folder.mkdir(parents=True,exist_ok=False)
    fraction,baryon_share,tau,matter,collision,curvature,field_strength=symbolic.symbols('f B tau mu lambda R bphi',positive=True)
    denominator=15+4*fraction
    shear0=-5/denominator
    shear_matter=3*(4*fraction-5)*shear0/(8*(15+2*fraction))
    shear_collision=-8*(1-fraction)*shear0/(15+2*fraction)
    loading=3*baryon_share/(4*(1-fraction))
    photon0=-symbolic.Rational(1,144)
    photon_matter=symbolic.Rational(1,960)+loading/144
    photon_collision=shear0/45
    neutrino0=-symbolic.Rational(1,144)+shear0/90
    neutrino_matter=symbolic.Rational(1,960)+shear_matter/180
    neutrino_collision=shear_collision/180
    theta=curvature*(-tau/8+3*matter*tau**2/80)
    density=curvature*tau**2/16*(1-matter*tau/5)
    hubble=1/tau+matter/4
    shear=shear0*tau+(matter*shear_matter+collision*shear_collision)*tau**2
    stress_nu=-4*shear0*tau**2/15-8*(matter*shear_matter+collision*shear_collision)*tau**3/45
    stress_gamma=-32*collision*shear0*tau**3/45
    photon=photon0*tau**3+(matter*photon_matter+collision*photon_collision)*tau**4
    neutrino=neutrino0*tau**3+(matter*neutrino_matter+collision*neutrino_collision)*tau**4
    def first_order(expression):
        expanded=symbolic.expand(expression)
        polynomial=symbolic.Poly(expanded,matter,collision)
        return symbolic.factor(sum(coefficient*matter**powers[0]*collision**powers[1] for powers,coefficient in polynomial.terms() if sum(powers)<=1))
    checks=[]
    def identity(name,expression):
        residual=first_order(expression)
        checks.append(dict(name=name,passed=residual==0,residual=str(residual)))
        assert residual==0,(name,residual)
    identity('Matter-corrected Hamiltonian',curvature+4*hubble*theta-6/tau**2*(1-matter*tau/2)*4*density/3-6*matter*density/tau)
    identity('Matter-corrected comoving continuity',symbolic.diff(density,tau)+theta)
    identity('Matter and finite-opacity shear evolution',symbolic.diff(shear,tau)+2*hubble*shear+1-3/tau**2*(1-matter*tau/2)*(fraction*stress_nu+(1-fraction)*stress_gamma))
    identity('Neutrino anisotropic stress with matter and photon viscosity',symbolic.diff(stress_nu,tau)+8*shear/15)
    identity('Tightly-coupled baryon-loaded Euler equation',(1+loading*matter*tau)*symbolic.diff(photon,tau)+hubble*loading*matter*tau*photon+density/(3*curvature)+stress_gamma/8)
    identity('Neutrino Euler with matter and photon-viscosity response',symbolic.diff(neutrino,tau)+density/(3*curvature)+stress_nu/8)
    geometric=2*theta/(3*curvature)-shear/6
    momentum=4/tau**2*(1-matter*tau/2)*((1-fraction)*photon+fraction*neutrino)+3*matter*baryon_share*photon/tau
    identity('Matter/opacity corrected momentum constraint',geometric-momentum)
    background_prime=-field_strength*(tau**3/5+matter*tau**4/15)
    response=-curvature*field_strength*tau**6/1680*(1-matter*tau/35)
    identity('Matter-corrected frozen-field curvature response',symbolic.diff(response,tau,2)+2*hubble*symbolic.diff(response,tau)+theta*background_prime)
    finish(folder,dict(checks=checks,count=len(checks),all_checks_passed=True,
        correction_order='First order in mu*tau and tau/kappa0 at leading curvature gradient order; cross products and squares omitted',
        baryon_loading_derived=True,finite_photon_viscosity_backreaction_derived=True,
        finite_mass_next_order_not_included=True,primordial_curvature_not_fixed=True),__file__)
    print(json.dumps(dict(checks=len(checks))),flush=True)


if __name__=='__main__':
    main()
