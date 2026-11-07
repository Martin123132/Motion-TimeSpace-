from common241 import *
import sympy as symbolic


def run():
    modest()
    protocol()
    assert not (ROOT / 'results/metric-jet-derivation.json').exists()
    duration = symbolic.symbols('t')
    scale, scale_rate, hubble, hubble_rate, wave_number = symbolic.symbols('a adot H Hdot k')
    energy_rate, transverse_rate, longitudinal_rate = symbolic.symbols('EF STF SLF')
    energy_curvature, transverse_curvature, longitudinal_curvature = symbolic.symbols('E2 ST2 SL2')
    metric_T_coefficients = symbolic.symbols('hT1:4')
    metric_L_coefficients = symbolic.symbols('hL1:4')
    rate_T_coefficients = symbolic.symbols('sT1:3')
    rate_L_coefficients = symbolic.symbols('sL1:3')
    metric_T = sum(value * duration**power for power, value in enumerate(metric_T_coefficients, 1))
    metric_L = sum(value * duration**power for power, value in enumerate(metric_L_coefficients, 1))
    rate_T = sum(value * duration**power for power, value in enumerate(rate_T_coefficients, 1))
    rate_L = sum(value * duration**power for power, value in enumerate(rate_L_coefficients, 1))
    local_scale = scale + scale_rate * duration
    local_hubble = hubble + hubble_rate * duration
    energy = energy_rate * duration + energy_curvature * duration**2
    transverse = transverse_rate * duration + transverse_curvature * duration**2
    longitudinal = longitudinal_rate * duration + longitudinal_curvature * duration**2
    metric_residuals = (symbolic.diff(metric_T, duration) - 2 * rate_T, symbolic.diff(metric_L, duration) - 2 * rate_L)
    rate_residuals = (
        symbolic.diff(rate_T, duration) - local_scale**2 * (energy - longitudinal) / 2
            + wave_number**2 * metric_T / 2 + local_hubble * (4 * rate_T + rate_L),
        symbolic.diff(rate_L, duration) - local_scale**2 * (energy + longitudinal - 2 * transverse) / 2
            + wave_number**2 * metric_T + local_hubble * (2 * rate_T + 3 * rate_L))
    equations = [symbolic.expand(value).coeff(duration, power) for value in metric_residuals for power in range(3)]
    equations.extend(symbolic.expand(value).coeff(duration, power) for value in rate_residuals for power in range(2))
    unknowns = (*metric_T_coefficients, *metric_L_coefficients, *rate_T_coefficients, *rate_L_coefficients)
    solution = symbolic.solve(equations, unknowns, dict=True)
    assert len(solution) == 1
    solution = solution[0]
    checks = []
    for index, expression in enumerate(equations):
        check(checks, f'native time-series equation{index}', int(symbolic.simplify(expression.subs(solution)) != 0), 0)
    expected_T = scale**2 * (energy_rate - longitudinal_rate) / 6
    expected_L = scale**2 * (energy_rate + longitudinal_rate - 2 * transverse_rate) / 6
    for name, actual, expected in [('transverse cubic', solution[metric_T_coefficients[2]], expected_T),
            ('longitudinal cubic', solution[metric_L_coefficients[2]], expected_L)]:
        check(checks, name + ':derived from full local metric equations', int(symbolic.simplify(actual - expected) != 0), 0)
        for variable in (scale_rate, hubble_rate, hubble, wave_number, energy_curvature, transverse_curvature, longitudinal_curvature):
            check(checks, name + ':independent at this order of ' + str(variable), int(symbolic.diff(actual, variable) != 0), 0)
    for variable in (*metric_T_coefficients[:2], *metric_L_coefficients[:2], rate_T_coefficients[0], rate_L_coefficients[0]):
        check(checks, str(variable) + ':zero before first forced order', int(solution[variable] != 0), 0)
    report = dict(stage=241, qualified=all(row['passed'] for row in checks), checks=checks,
        failed=[row for row in checks if not row['passed']], solution={str(key): str(value) for key, value in solution.items()},
        script_sha256=digest(__file__), native_source_path=str(BRANCH / 'expanding-thermal-gravity-20261007/thermal_wave_system.py'),
        native_source_sha256=digest(BRANCH / 'expanding-thermal-gravity-20261007/thermal_wave_system.py'), finished_at=now(),
        scope='Coefficient-matched differentiation of native metric equations with arbitrary time-dependent background and stress curvature; zero incoming difference, no finite-time approximation certified')
    write(ROOT / 'results/metric-jet-derivation.json', report)
    print(json.dumps(dict(checks=len(checks), failures=report['failed'], solution=report['solution'])), flush=True)


if __name__ == '__main__':
    run()
