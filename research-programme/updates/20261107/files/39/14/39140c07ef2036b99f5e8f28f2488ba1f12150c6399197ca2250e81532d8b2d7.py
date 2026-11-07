from __future__ import annotations

from pathlib import Path
import sympy as sp

from bound_common import modest_process, save


def main():
    modest_process()
    radius, mass = sp.symbols('r M', positive=True)
    master = sp.Function('Z')(radius)
    metric = 1-2*mass/radius
    denominator = 2+3*mass/radius
    coefficient = (6*mass**2+6*mass*radius+6*radius**2)/(radius**2*(2*radius+3*mass))
    angular = metric*sp.diff(master, radius)+coefficient*master
    difference = denominator/metric*(3*master/radius-angular)
    radial = radius*sp.diff(angular, radius)+difference
    checks = []

    def check(name, expression):
        residual = sp.factor(expression)
        checks.append(dict(name=name, residual=str(residual), passed=residual == 0))
        assert residual == 0, (name, residual)

    check('master definition inverted', radius/3*(angular+metric/denominator*(radial-radius*sp.diff(angular, radius)))-master)
    curvature = 2*metric*sp.diff(radial, radius)/radius+((6+2*metric)/radius**2+2*sp.diff(metric, radius)/radius)*radial+4*angular/radius**2-(6*metric/radius+sp.diff(metric, radius))*sp.diff(angular, radius)-2*metric*sp.diff(angular, radius, 2)
    check('arbitrary master solves vacuum spatial constraint', curvature)
    scaled_energy = -radial**2/2-2*radial*angular+(radius-mass)*radial*sp.diff(angular, radius)-metric*radius**2*sp.diff(angular, radius)**2/2
    master_value, master_first, master_second = sp.symbols('Z Zp Zpp')
    replacements = {sp.diff(master, radius, 2):master_second, sp.diff(master, radius):master_first, master:master_value}
    polynomial = sp.Poly(sp.expand(scaled_energy.subs(replacements)), master_second)
    check('no second derivative squared survives constraint', polynomial.coeff_monomial(master_second**2))
    second_coefficient = sp.factor(polynomial.coeff_monomial(master_second))
    first_square = sp.diff(second_coefficient, master_first)/2
    mixed = sp.diff(second_coefficient, master_value)
    partial_contact = first_square*sp.diff(master, radius)**2+mixed*master*sp.diff(master, radius)
    remaining = sp.factor(scaled_energy-sp.diff(partial_contact, radius))
    remaining_poly = sp.Poly(sp.expand(remaining.subs(replacements)), master_value, master_first, master_second)
    value_square = sp.factor(remaining_poly.coeff_monomial(master_value*master_first)/2)
    contact = sp.factor(partial_contact+value_square*master**2)
    reduced = sp.factor(scaled_energy-sp.diff(contact, radius))
    reduced_poly = sp.Poly(sp.expand(reduced.subs(replacements)), master_value, master_first, master_second)
    derived_gradient = sp.factor(reduced_poly.coeff_monomial(master_first**2))
    derived_potential = sp.factor(reduced_poly.coeff_monomial(master_value**2))
    check('canonical positive gradient coefficient', derived_gradient-3*metric)
    potential = metric*(24*radius**3+24*mass*radius**2+36*mass**2*radius+18*mass**3)/(radius**3*(2*radius+3*mass)**2)
    check('derived Zerilli potential normalization', derived_potential-3*potential/metric)
    check('off shell vacuum energy plus exact contact', scaled_energy-3*(metric*sp.diff(master, radius)**2+potential/metric*master**2)-sp.diff(contact, radius))
    flat_contact = 9*master**2/radius-radius*(sp.diff(master, radius)+3*master/radius)**2
    check('flat contact limit', contact.subs(mass, 0)-flat_contact)
    check('flat angular barrier', potential.subs(mass, 0)-6/radius**2)
    save('vacuum', Path(__file__), dict(exact_checks=checks, metric_angular_coefficient=str(coefficient),
         master_definition='Z=r/3*[K+F/(2+3M/r)*(H-r K_prime)]',
         contact_4alpha=str(contact), potential=str(potential),
         energy_identity='E_vacuum = 3/(4alpha) integral [F Z_prime^2+V_Z/F Z^2] dr + [contact_4alpha/(4alpha)]_endpoints',
         positivity_domain='M>=0,r>2M,alpha>0; bulk positive, retain finite inner-surface contact',
         wave_equation_used=False, continuum_gap_claimed=False,
         isolated_exterior_ADM_energy_without_surface_contact_positive_claimed=False))
    print(dict(exact_checks=len(checks), contact=str(contact)), flush=True)


if __name__ == '__main__':
    main()
