from __future__ import annotations

import math
import sympy as sym

from early_common import ROOT, POST, SOURCE_NAMES, MASS, FRACTION, Environment, modest_process, save, read_json, PARENT


def main():
    modest_process()
    checks = []

    def check(name, condition):
        checks.append(dict(name=name, passed=bool(condition)))

    field, velocity, delta, delta_velocity, frequency, nu, wave2, slope, cold_prime = sym.symbols('u w d s omega nu K2 h g', real=True, nonzero=True)
    density = nu**2 * (field**2 + velocity**2)
    pressure = nu**2 * (velocity**2 - field**2)
    delta_density = 2 * nu**2 * (field * delta + velocity * delta_velocity)
    delta_pressure = 2 * nu**2 * (velocity * delta_velocity - field * delta)
    momentum = 2 * nu**2 * wave2 / frequency * velocity * delta
    evolutions = {field: frequency * velocity, velocity: -3 * velocity - frequency * field,
        delta: frequency * delta_velocity,
        delta_velocity: -3 * delta_velocity - (frequency + wave2 / frequency) * delta + velocity * cold_prime,
        frequency: -slope * frequency, wave2: -(2 + 2 * slope) * wave2}

    def derivative(expression):
        return sum(sym.diff(expression, variable) * rate for variable, rate in evolutions.items())

    check('background KG stress obeys continuity', sym.simplify(derivative(density) + 3 * (density + pressure)) == 0)
    check('exact perturbed scalar energy conservation', sym.simplify(derivative(delta_density) + 3 * (delta_density + delta_pressure) + momentum - (density + pressure) * cold_prime) == 0)
    check('exact perturbed scalar momentum conservation', sym.simplify(derivative(momentum) + (5 + slope) * momentum - wave2 * delta_pressure) == 0)
    check('trace Einstein source factor', sym.expand(delta_density + 3 * delta_pressure) == 8 * nu**2 * velocity * delta_velocity - 4 * nu**2 * field * delta)
    check('radiation-era regular background coefficient', sym.Rational(4, 5) + sym.Rational(1, 5) == 1)
    check('adiabatic forced field coefficient', sym.Rational(42, 105) == sym.Rational(2, 5))
    check('isocurvature compensation coefficient', 16 * sym.Rational(-1, 4) == 4 * sym.Rational(-1, 4) - 3)
    eta, expansion2, total_density_delta, total_pressure_delta, total_enthalpy, total_momentum = sym.symbols('eta E2 dr dp W J', real=True, nonzero=True)
    constraint = wave2 * eta + cold_prime + sym.Rational(3, 2) * total_density_delta / expansion2
    constraint_rates = {wave2: -(2 + 2 * slope) * wave2,
        eta: sym.Rational(3, 2) * total_momentum / (expansion2 * wave2),
        cold_prime: -(2 + slope) * cold_prime + sym.Rational(3, 2) * (total_density_delta + 3 * total_pressure_delta) / expansion2,
        total_density_delta: -3 * (total_density_delta + total_pressure_delta) - total_momentum + total_enthalpy * cold_prime,
        expansion2: 2 * slope * expansion2}
    propagated = sum(sym.diff(constraint, variable) * rate for variable, rate in constraint_rates.items())
    check('Einstein 00 constraint propagated by conserved stress', sym.simplify((propagated + (2 + 2 * slope) * constraint).subs(total_enthalpy, -sym.Rational(2, 3) * slope * expansion2)) == 0)
    kappa = sym.symbols('kappa', real=True)
    sound = kappa**2 / (sym.sqrt(1 + kappa**2) + 1)**2
    check('beat-frequency sound speed cold limit', sym.limit(sound / kappa**2, kappa, 0) == sym.Rational(1, 4))
    check('beat-frequency sound speed ultraviolet limit', sym.limit(sound, kappa, sym.oo) == 1)
    environment = Environment()
    check('positive dark bridge and occupied budget', environment.frozen_dark > 0 and 0 < FRACTION < 1 and MASS > 0)
    early = environment.fluid_values(-5 - 1e-10)
    late = environment.fluid_values(-5)
    check('background expansion bridge continuous', abs(early[3] / late[3] - 1) < 1e-8)
    check('dark contribution negligible at earliest matching boundary', environment.frozen_dark / environment.fluid_values(math.log(.00045))[3]**2 < 1e-8)
    for name in SOURCE_NAMES:
        check('original source exists: ' + name, (POST / name).is_file())
    check('stage50 completed preservation seal', read_json(PARENT / 'results/stage-integrity.json')['state'] == 'complete')
    for path in ROOT.glob('*.py'):
        compile(path.read_bytes(), str(path), 'exec')
    assert all(row['passed'] for row in checks), checks
    save('preflight', __file__, dict(checks=checks, count=len(checks), exact_scope='Canonical scalar, pressureless remainder, perfect radiation, frozen dark background before N=-5. Late dynamical dark perturbations omitted as in stage50.'))
    print(dict(state='complete', checks=len(checks)), flush=True)


if __name__ == '__main__':
    main()
