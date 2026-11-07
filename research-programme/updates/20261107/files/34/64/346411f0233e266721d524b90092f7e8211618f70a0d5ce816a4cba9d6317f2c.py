from __future__ import annotations

from pathlib import Path
import sympy as sp

from interior_common import ROOT, modest_process, read_json, save


def main():
    modest_process()
    report = read_json(ROOT/'results/energy-v2/status.json')
    symbols = sp.symbols(' '.join(report['symbols']), positive=True)
    environment = dict(zip(report['symbols'], symbols))
    parse = lambda expression: sp.sympify(expression, locals=environment)
    base = [[parse(value) for value in row] for row in report['base_hessian']]
    coefficients = {name:parse(value) for name,value in report['coefficients'].items()}
    mapping = [coefficients[name] for name in ['k_Zprime','k_Z','k_wprime','k_w','k_pibar']]
    matrix = [[base[left][right]+base[left][5]*mapping[right]+base[right][5]*mapping[left]+base[5][5]*mapping[left]*mapping[right] for right in range(5)] for left in range(5)]
    checks = []

    def check(name, expression):
        residual = sp.factor(expression)
        checks.append(dict(name=name, residual=str(residual), passed=residual == 0))
        assert residual == 0, (name, residual)

    phase = sp.factor(matrix[4][4])
    rejected_guess = sp.factor(phase-coefficients['beta']/coefficients['omega'])
    guess_is_identity = rejected_guess == 0
    print(dict(phase_coefficient=str(phase), beta_over_omega_identity=guess_is_identity), flush=True)
    phase_cross = [sp.factor(matrix[index][4]) for index in range(4)]
    reduced = [[None]*4 for _ in range(4)]
    for left in range(4):
        for right in range(left, 4):
            value = sp.factor(matrix[left][right]-phase_cross[left]*phase_cross[right]/phase)
            reduced[left][right] = reduced[right][left] = value
        print('Reduced row '+str(left)+' derived', flush=True)
    radius, alpha, metric, field, gradient, rotation, potential, force, second = symbols
    angular_kinetic = sp.factor(reduced[0][0]*2*alpha*radius**2/3)
    scalar_kinetic = sp.factor(reduced[2][2])
    mixed_kinetic = sp.factor(reduced[0][2])
    determinant = sp.factor(reduced[0][0]*reduced[2][2]-reduced[0][2]**2)
    vacuum = {field:0, gradient:0, potential:0, force:0, second:0}
    check('vacuum gravitational derivative energy', angular_kinetic.subs(vacuum)-metric)
    check('vacuum mixed derivative decoupling', mixed_kinetic.subs(vacuum))
    source = read_json(ROOT/'results/map-v2/status.json')
    map_normalization = parse(source['constraint_normalization'])
    check('map denominator matches beta omega', map_normalization-coefficients['omega']/coefficients['beta'])
    save('reduced-v2', Path(__file__), dict(exact_checks=checks, symbols=report['symbols'], phase_coefficient=str(sp.factor(phase)),
        phase_cross=[str(value) for value in phase_cross], reduced_hessian=[[str(value) for value in row] for row in reduced],
        phase_coefficient_comparison='beta/omega', comparison_is_identity=guess_is_identity, comparison_residual=str(rejected_guess),
        reduced_coordinates=['Zprime','Z','wprime','w'], normalized_gravity_kinetic=str(angular_kinetic),
        scalar_kinetic=str(scalar_kinetic), mixed_kinetic=str(mixed_kinetic), gradient_determinant=str(determinant),
        map_beta_lower_bound='1004/625 under stage46 box', omega_exceeds_beta=True,
        canonical_transformation_claimed=False, full_energy_positive_claimed=False),
        [ROOT/'results/energy-v2/status.json', ROOT/'results/map-v2/status.json'])
    print(dict(checks=len(checks), gravity_kinetic=str(angular_kinetic), scalar_kinetic=str(scalar_kinetic), mixed_kinetic=str(mixed_kinetic), determinant=str(determinant)), flush=True)


if __name__ == '__main__':
    main()
