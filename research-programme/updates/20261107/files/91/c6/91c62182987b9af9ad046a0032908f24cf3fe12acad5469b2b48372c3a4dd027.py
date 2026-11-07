from __future__ import annotations

from pathlib import Path
import sympy as sp

from interior_common import ROOT, PARENT, modest_process, read_json, save


def main():
    modest_process()
    reduced = read_json(ROOT/'results/reduced-v2/status.json')
    local = read_json(ROOT/'results/energy-v2/status.json')
    parent = read_json(PARENT/'results/vacuum/status.json')
    symbols = sp.symbols(' '.join(reduced['symbols']), positive=True)
    radius, alpha, metric, field, gradient, rotation, potential, force, second = symbols
    mass = sp.symbols('M', nonnegative=True)
    master = sp.Function('Z')(radius)
    environment = dict(zip(reduced['symbols'], symbols))
    environment.update(M=mass, Z=sp.Function('Z'))
    parse = lambda expression: sp.sympify(expression, locals=environment)
    vacuum_values = {field:0, gradient:0, potential:0, force:0, second:0, metric:1-2*mass/radius}
    vacuum = lambda expression: sp.factor(parse(expression).subs(vacuum_values))
    gravity_gradient = vacuum(reduced['reduced_hessian'][0][0])
    gravity_mixed = vacuum(reduced['reduced_hessian'][0][1])
    gravity_value = vacuum(reduced['reduced_hessian'][1][1])
    master_coefficient = vacuum(local['coefficients']['k_Z'])
    derivative_coefficient = vacuum(local['coefficients']['k_Zprime'])
    angular = derivative_coefficient*sp.diff(master, radius)+master_coefficient*master
    contact_angular, contact_master, contact_scalar = [vacuum(value) for value in local['contact_coefficients']]
    original_contact = radius**2*(contact_angular*angular**2/2+contact_master*angular*master)
    second_contact = radius**2*gravity_mixed*master**2/2
    corrected_potential = sp.factor(gravity_value-sp.diff(radius**2*gravity_mixed, radius)/radius**2)
    checks = []

    def check(name, expression):
        residual = sp.factor(expression)
        checks.append(dict(name=name, residual=str(residual), passed=residual == 0))
        assert residual == 0, (name, residual)

    check('vacuum map derivative matches stage46', derivative_coefficient-(1-2*mass/radius))
    check('vacuum map value matches stage46', master_coefficient-parse(parent['metric_angular_coefficient']))
    check('vacuum gravitational normalization', gravity_gradient-3*(1-2*mass/radius)/(2*alpha*radius**2))
    check('vacuum matter contact vanishes', contact_scalar)
    check('vacuum potential including local mixed derivative', corrected_potential-3*parse(parent['potential'])/(2*alpha*radius**2*(1-2*mass/radius)))
    check('full surface contact matches stage46 exactly', 4*alpha*(original_contact+second_contact)-parse(parent['contact_4alpha']))
    save('vacuum-join-v2', Path(__file__), dict(exact_checks=checks,
        vacuum_mixed_coefficient=str(gravity_mixed),
        local_surface_contact=str(sp.factor(original_contact)),
        additional_surface_contact=str(sp.factor(second_contact)),
        corrected_potential=str(corrected_potential),
        identity='C_Z/(4alpha)=local_contact + r^2 B_ZZ Z^2/2 in vacuum. The added term arises only when removing the residual Zprime*Z term.',
        matching_conditions=['Continuous Z,K and metric at shell-free material surface',
            'h=h_prime=W=W_h=0 at the surface',
            'No scalar outside; do not evaluate divergent W_hh at h=0 as a physical scalar mass'],
        endpoint_rule='Join the local interior and local exterior contacts first. If the exterior is rewritten as Zerilli bulk, retain the additional inner contact; do not discard it.',
        no_frequency_equation_used=True, canonical_transformation_claimed=False),
        [ROOT/'results/reduced-v2/status.json',ROOT/'results/energy-v2/status.json',PARENT/'results/vacuum/status.json'])
    print(dict(exact_checks=len(checks), surface_match='exact'), flush=True)


if __name__ == '__main__':
    main()
