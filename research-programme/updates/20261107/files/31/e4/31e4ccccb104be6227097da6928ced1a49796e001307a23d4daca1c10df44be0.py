from __future__ import annotations

import json
from pathlib import Path

import sympy as sp


def main():
    root = Path(__file__).resolve().parent
    folder = root / 'results/identities'
    folder.mkdir(parents=True, exist_ok=False)
    scale, hubble, mass, mode, metric = sp.symbols('a H m k z', real=True)
    field, velocity, delta, delta_velocity = sp.symbols('phi velocity delta delta_velocity', real=True)
    variables = [scale, field, velocity, delta, delta_velocity]
    derivatives = [hubble * scale, velocity, -2 * hubble * velocity - scale**2 * mass**2 * field,
        delta_velocity, -2 * hubble * delta_velocity - mode * metric * velocity
        - (mode**2 + scale**2 * mass**2) * delta]

    def time_derivative(expression):
        return sp.expand(sum(sp.diff(expression, variable) * derivative for variable, derivative in zip(variables, derivatives)))

    density = velocity * delta_velocity + scale**2 * mass**2 * field * delta
    pressure = velocity * delta_velocity - scale**2 * mass**2 * field * delta
    momentum = mode * velocity * delta
    background_density = (velocity**2 + scale**2 * mass**2 * field**2) / 2
    background_pressure = (velocity**2 - scale**2 * mass**2 * field**2) / 2
    identities = {
        'canonical_continuity': time_derivative(density) + hubble * (density + 3 * pressure) + mode * momentum + mode * metric * velocity**2,
        'canonical_momentum': time_derivative(momentum) + 2 * hubble * momentum - mode * pressure,
        'background_continuity': time_derivative(background_density) + hubble * (background_density + 3 * background_pressure),
    }
    tau, beta, cold_coefficient, initial = sp.symbols('tau beta C phi0', positive=True)
    background_velocity = -mass**2 * beta**2 * initial * tau**3 / 5
    cold = cold_coefficient * tau**2
    seed = -initial * (mass * beta * tau**2)**2 * cold / 105
    identities['radiation_seed_leading_equation'] = sp.diff(seed, tau, 2) + 2 / tau * sp.diff(seed, tau) - sp.diff(cold, tau) * background_velocity
    identities['radiation_seed_velocity'] = sp.diff(seed, tau) - 6 * seed / tau
    rows = [dict(name=name, residual=str(sp.simplify(value)), passed=sp.simplify(value) == 0) for name, value in identities.items()]
    assert all(row['passed'] for row in rows)
    (folder / 'status.json').write_text(json.dumps(dict(state='complete', exact_identities=rows,
        count=len(rows), all_checks_passed=True, scope='Quadratic canonical modes and leading regular radiation series, not empirical validation'), indent=2), encoding='utf-8')
    (folder / 'COMPLETE').write_text('complete\n', encoding='utf-8')
    print('Exact symbolic identities:', len(rows), flush=True)


if __name__ == '__main__':
    main()
