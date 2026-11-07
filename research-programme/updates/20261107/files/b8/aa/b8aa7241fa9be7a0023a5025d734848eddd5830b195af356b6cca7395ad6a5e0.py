from __future__ import annotations

import math

import numpy as np
from scipy import integrate, special
import sympy as sp

from growth_common import Background, modest_process, save, solve_response


def main():
    modest_process()
    checks = []

    def check(name, condition, detail=None):
        assert bool(condition), (name, detail)
        checks.append(dict(name=name, passed=True, detail=detail))

    friction, source, share, quantum, cold, heavy = sp.symbols('friction source share quantum cold heavy')
    cold_prime, heavy_prime = sp.symbols('cold_prime heavy_prime')
    total = (1 - share) * cold + share * heavy
    total_prime = (1 - share) * cold_prime + share * heavy_prime
    cold_second = -friction * cold_prime + source * total
    heavy_second = -friction * heavy_prime + source * total - quantum * heavy
    residual = sp.expand((1 - share) * cold_second + share * heavy_second + friction * total_prime - source * total + share * quantum * heavy)
    check('total_equation_has_fraction_times_pressure', residual == 0, str(residual))
    check('relative_equation', sp.expand(heavy_second - cold_second + friction * (heavy_prime - cold_prime) + quantum * heavy) == 0)
    power = (-1 + sp.sqrt(25 - 24 * share)) / 4
    check('smooth_heavy_EdS_exponent', sp.simplify(power**2 + power / 2 - sp.Rational(3, 2) * (1 - share)) == 0)
    bessel_rows = []
    for pressure_today in [.001, .1, 10.]:
        start = -math.log(100)
        grid = np.linspace(start, 0., 1201)

        def analytic_basis(efold):
            argument = 2 * math.sqrt(pressure_today) * np.exp(-np.asarray(efold) / 2)
            regular = special.spherical_jn(2, argument)
            singular = special.spherical_yn(2, argument)
            regular_prime = special.spherical_jn(2, argument, derivative=True)
            singular_prime = special.spherical_yn(2, argument, derivative=True)
            return np.array([argument * regular, argument * singular,
                             -.5 * argument * (regular + argument * regular_prime),
                             -.5 * argument * (singular + argument * singular_prime)])

        initial_basis = analytic_basis(start)
        constants = np.linalg.solve(initial_basis.reshape(2, 2), [1., 1.])
        whole_basis = analytic_basis(grid)
        exact = np.vstack([constants @ whole_basis[:2], constants @ whole_basis[2:]])

        def rhs(efold, state):
            return [state[1], -.5 * state[1] + (1.5 - pressure_today * math.exp(-efold)) * state[0]]

        solution = integrate.solve_ivp(rhs, (start, 0.), [1., 1.], t_eval=grid, method='DOP853', rtol=2e-11, atol=2e-13, max_step=.03)
        error = float(np.max(abs(solution.y - exact)) / max(1., float(np.max(abs(exact)))))
        check('independent_EdS_Bessel:' + str(pressure_today), error < 2e-9, error)
        bessel_rows.append(dict(pressure_today=pressure_today, error=error))
    background = Background('ParentScalar_Lambda_zero')
    check('background_constraint', background.diagnostics['max_constraint_residual'] < 2e-6)
    check('background_derivative', background.diagnostics['max_dlogE_interpolation_difference'] < 2e-6)
    reference = solve_response(background, 1e8, .5, 0., pressure=False)
    for share_value in [0., .1, .5, .8, 1.]:
        result = solve_response(background, 1e8, share_value, 0.)
        check('zero_wave_control:' + str(share_value), np.max(abs(result.y[:, -1] / reference.y[:, -1] - 1)) < 1e-10)
    result = solve_response(background, 1e6, 0., .1)
    check('zero_occupation_control', abs(result.y[0, -1] / reference.y[0, -1] - 1) < 2e-7)
    result = solve_response(background, 1e16, .8, 10.)
    check('infinite_mass_control', np.max(abs(result.y[:, -1] / reference.y[:, -1] - 1)) < 2e-7)
    save('preflight', __file__, dict(checks=checks, count=len(checks), EdS_Bessel_replays=bessel_rows,
        scan_authorized=True, units='k physical numeric unit Mpc^-1 (comoving), M/H0 angular frequency',
        conditional_late_response_only=True, primordial_transfer_claim=False))
    print(dict(state='complete', preflight_checks=len(checks)), flush=True)


if __name__ == '__main__':
    main()
