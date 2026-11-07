from common238 import *
import sympy as symbolic


def run():
    modest()
    config = protocol()
    checks = []
    for legs in (2, 3):
        photon = symbolic.symbols(f'h0:{legs}')
        forward = symbolic.symbols(f'f0:{legs}')
        reverse = symbolic.symbols(f'r0:{legs}')
        gas, score_forward, score_reverse, normalization = symbolic.symbols('g sf sr normalization')
        source = (1 + score_forward * gas + (score_forward**2 - 2 * score_forward - normalization) * gas**2 / 2)
        source *= symbolic.prod(1 + slope * value for slope, value in zip(forward, photon))
        subtraction = (1 + score_reverse * gas + (score_reverse**2 - 2 * score_reverse - normalization) * gas**2 / 2)
        subtraction *= symbolic.prod(1 + slope * value for slope, value in zip(reverse, photon))
        source -= subtraction
        variables = symbolic.Matrix([*photon, gas])
        zero = {value: 0 for value in variables}
        hessian = symbolic.hessian(source, variables).subs(zero)
        forward_shift = score_forward * gas + sum(slope * value for slope, value in zip(forward, photon))
        reverse_shift = score_reverse * gas + sum(slope * value for slope, value in zip(reverse, photon))
        retained = symbolic.Matrix([first * (forward_shift - first * value) - second * (reverse_shift - second * value)
            for first, second, value in zip(forward, reverse, photon)] + [
            (score_forward**2 - score_reverse**2 - 2 * (score_forward - score_reverse)) * gas
            + sum((score_forward * first - score_reverse * second) * value for first, second, value in zip(forward, reverse, photon))])
        residual = retained - hessian * variables
        for index, entry in enumerate(residual):
            check(checks, f'legs{legs}:microscopic statistical derivative{index}', int(symbolic.expand(entry) != 0), 0)
        quadratic = (variables.T * hessian * variables)[0] / 2
        gradient = symbolic.Matrix([symbolic.diff(quadratic, value) for value in variables])
        check(checks, f'legs{legs}:Euler density source and derivative', int(any(symbolic.expand(value) != 0 for value in gradient - retained)), 0)
        wave = symbolic.Matrix(symbolic.symbols(f'w0:{legs + 1}'))
        check(checks, f'legs{legs}:Hessian exchange', int(symbolic.expand((variables.T * hessian * wave - wave.T * hessian * variables)[0]) != 0), 0)
        check(checks, f'legs{legs}:missing half factor detected', int(all(symbolic.expand(value) == 0 for value in 2 * gradient - retained)), 0)
    heat, capacity, capacity_R, ratio, hubble, rest, energy, transfer = symbolic.symbols('chi C CR R H rest A Q', nonzero=True)
    density, temperature, velocity, photon_energy, photon_current = symbolic.symbols('b r v CE CF')
    ratio_prime = hubble * ratio - (2 * hubble * ratio + transfer / heat) / capacity
    capacity_prime = capacity_R * (ratio_prime - hubble * ratio)
    energy_prime = hubble * (energy - ratio * capacity) + capacity * ratio_prime
    inertia = rest + heat * (energy + 2 * ratio / 3)
    inertia_prime = hubble * rest + heat * (energy_prime + 2 * ratio_prime / 3)
    temperature_rhs = (hubble - 2 * hubble / capacity - capacity_prime / capacity) * temperature - (photon_energy - transfer * density) / (heat * capacity)
    velocity_rhs = (-photon_current - inertia_prime * velocity) / inertia
    for name, expression in [('capacity background derivative', symbolic.diff(temperature_rhs, transfer) - density / (heat * capacity) - capacity_R * temperature / (heat * capacity**2)),
                             ('enthalpy background derivative', symbolic.diff(velocity_rhs, transfer) - (1 + 2 / (3 * capacity)) * velocity / inertia),
                             ('one-electron density heating cancellation', (-transfer + transfer) / (heat * capacity))]:
        check(checks, name, int(symbolic.factor(expression) != 0), 0)
    for name, expression in [('omit capacity feedback', capacity_R * temperature / (heat * capacity**2)),
                             ('omit enthalpy feedback', (1 + 2 / (3 * capacity)) * velocity / inertia)]:
        check(checks, name + ' is detected', int(symbolic.factor(expression) == 0), 0)
    report = dict(state='complete', qualified=all(row['passed'] for row in checks), checks=checks,
        failed=[row for row in checks if not row['passed']], script_sha256=digest(__file__), finished_at=now(),
        scope='Exact retained statistical Taylor Hessian and existing EOS source law; no nonperturbative QFT existence claim')
    write(ROOT / 'results/algebra.json', report)
    print(json.dumps(dict(checks=len(checks), failures=report['failed'])), flush=True)


if __name__ == '__main__':
    run()
