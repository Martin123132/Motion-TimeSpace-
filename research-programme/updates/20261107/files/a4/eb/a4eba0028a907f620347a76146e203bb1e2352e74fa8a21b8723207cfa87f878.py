from __future__ import annotations

import math
from pathlib import Path

import numpy as np
from scipy import integrate
import sympy as sp

from growth_common import ROOT, Background, MODELS, SCALE_MASS, C_KM_S, H0_KM_S_MPC, digest, read_json, save, modest_process, solve_response, summary, initial_state


def main():
    modest_process()
    checks = []

    def check(name, passed, detail=None):
        assert bool(passed), (name, detail)
        checks.append(dict(name=name, passed=True, detail=detail))

    scan = read_json(ROOT / 'results/scan/status.json')
    preflight = read_json(ROOT / 'results/preflight/status.json')
    for label, report, script in [('scan', scan, 'run_growth_scan.py'), ('preflight', preflight, 'preflight_growth.py')]:
        check(label + ':script_unchanged', report['script_sha256'] == digest(ROOT / script))
        for source, expected in report['input_hashes'].items():
            check(label + ':source:' + Path(source).name, digest(source) == expected)
    check('all_requested_cases_accounted', scan['accepted_cases'] + scan['excluded_cases'] == scan['total_requested_cases'] == 486)
    check('all_accepted_regime_gates', all(row['accepted'] for row in scan['rows']))
    check('outside_domain_not_scored', all(not row['accepted'] for row in scan['excluded_outside_domain']))
    check('no_invented_growth_likelihood', all(row['growth_likelihood_chi2'] is None for row in scan['rows']))
    check('not_primordial_transfer', not scan['primordial_transfer_function_computed'])
    check('no_refit', not scan['background_parameters_refitted'])
    check('galaxy_route_preserved', not scan['galaxy_repo_modified'])
    check('no_mass_bound', not scan['observed_mass_constraint_claim'])
    convergence = []
    for model in MODELS:
        background = Background(model)
        cold = solve_response(background, 1e8, .5, 0., pressure=False, tolerance=2e-11, max_step=.025)
        zero_share = solve_response(background, 1e6, 0., .1, tolerance=2e-11, max_step=.025)
        check('matched_zero_fraction:' + model, abs(zero_share.y[0, -1] / cold.y[0, -1] - 1) < 1e-8)
        for mass, wave in [(1e6, .1), (SCALE_MASS, 1.), (SCALE_MASS, 5.), (1e8, 10.)]:
            original = next(row for row in scan['rows'] if row['model'] == model and row['mass_over_H0'] == mass and row['k_Mpc_inverse'] == wave and row['heavy_fraction'] == .5)
            refined = solve_response(background, mass, .5, wave, tolerance=2e-11, max_step=.025)
            changed = summary(background, mass, .5, wave, refined, cold)
            difference = abs(changed['total_density_ratio'] - original['total_density_ratio'])
            check('step_and_tolerance:' + model + ':' + str(wave) + ':' + str(mass), difference < 2e-7, difference)
            convergence.append(dict(model=model, mass=mass, wave=wave, density_ratio_change=difference))
    background = Background('ParentScalar_Lambda_zero', points=8001)
    refined = solve_response(background, SCALE_MASS, .5, 5., tolerance=2e-11, max_step=.025)
    control = solve_response(background, SCALE_MASS, .5, 0., pressure=False, tolerance=2e-11, max_step=.025)
    changed = summary(background, SCALE_MASS, .5, 5., refined, control)
    original = next(row for row in scan['rows'] if row['model'] == background.model and row['mass_over_H0'] == SCALE_MASS and row['k_Mpc_inverse'] == 5. and row['heavy_fraction'] == .5)
    check('doubled_background_resolution', abs(changed['total_density_ratio'] - original['total_density_ratio']) < 2e-7)
    equal_pressure_pairs = [(1e6, .02, 1e8, .2), (1e6, .05, 1e8, .5), (1e6, .1, 1e8, 1.)]
    for first_mass, first_wave, second_mass, second_wave in equal_pressure_pairs:
        pair = [next(row for row in scan['rows'] if row['model'] == background.model and row['heavy_fraction'] == .5 and row['mass_over_H0'] == mass and row['k_Mpc_inverse'] == wave) for mass, wave in [(first_mass, first_wave), (second_mass, second_wave)]]
        check('k_squared_over_mass_similarity:' + str(first_wave), abs(pair[0]['total_density_ratio'] - pair[1]['total_density_ratio']) < 1e-12)
    matrices = []
    initial_efold = -math.log(100)
    for wave in [.1, 1., 5.]:
        pressure_zero = (C_KM_S * wave / H0_KM_S_MPC)**4 / (4 * SCALE_MASS**2)

        def matrix_rhs(efold, flattened):
            expansion2, slope, omega_m = background.values(efold)
            source = 1.5 * omega_m
            pressure = pressure_zero * math.exp(-4 * efold) / expansion2
            evolution = np.array([[0., 1., 0., 0.],
                                  [.5 * source, -(2 + slope), .5 * source, 0.],
                                  [0., 0., 0., 1.],
                                  [.5 * source, 0., .5 * source - pressure, -(2 + slope)]])
            return (evolution @ flattened.reshape(4, 4)).ravel()

        propagated = integrate.solve_ivp(matrix_rhs, (initial_efold, 0.), np.eye(4).ravel(), method='Radau', rtol=2e-10, atol=2e-12, max_step=.03)
        check('Radau_propagator_completed:' + str(wave), propagated.success)
        propagator = propagated.y[:, -1].reshape(4, 4)
        for preparation in ['equal', 'heavy_unperturbed']:
            state = propagator @ initial_state(background, .5, 99., preparation)
            direct = solve_response(background, SCALE_MASS, .5, wave, preparation=preparation, tolerance=2e-11, max_step=.025)
            error = float(np.max(abs(state - direct.y[:, -1])) / max(1., float(np.max(abs(direct.y[:, -1])))))
            check('independent_matrix_method:' + str(wave) + ':' + preparation, error < 2e-7, error)
        matrices.append(dict(k_Mpc_inverse=wave, mass_over_H0=SCALE_MASS, fraction=.5,
                             N_start=initial_efold, N_end=0., state_order=['delta_c', 'dN_delta_c', 'delta_h', 'dN_delta_h'],
                             propagator=propagator.tolist()))
    source, pressure, fraction, eigenvalue = sp.symbols('source pressure fraction eigenvalue')
    gravity_matrix = sp.Matrix([[source * (1 - fraction), source * fraction],
                                [source * (1 - fraction), source * fraction - pressure]])
    characteristic = sp.expand((eigenvalue * sp.eye(2) - gravity_matrix).det())
    check('two_component_characteristic', sp.expand(characteristic - eigenvalue**2 - (pressure - source) * eigenvalue + source * (1 - fraction) * pressure) == 0)
    selected = [row for row in scan['rows'] if row['model'] == background.model and row['mass_over_H0'] == SCALE_MASS and row['heavy_fraction'] == .5]
    selected_all_f = [row for row in scan['rows'] if row['model'] == background.model and row['mass_over_H0'] == SCALE_MASS and row['k_Mpc_inverse'] in [.1, 1., 2., 5.]]
    check('large_small_scale_separation', max(abs(1 - row['total_density_ratio']) for row in selected if row['k_Mpc_inverse'] <= .1) < 2e-6 and min(row['total_density_ratio'] for row in selected if row['k_Mpc_inverse'] >= 5.) < .3)
    sensitivity = [row['total_density_ratio'] for row in scan['initial_state_sensitivity'] if row['k_Mpc_inverse'] == 5.]
    check('initial_state_sensitivity_not_hidden', max(sensitivity) - min(sensitivity) > .3)
    check('no_cache', not list(ROOT.rglob('__pycache__')))
    save('validation', __file__, dict(checks=checks, count=len(checks), convergence=convergence,
        selected_half_fraction_rows=selected, selected_fraction_dependence=selected_all_f,
        finite_time_response_matrices=matrices, maximum_refinement_change=max(row['density_ratio_change'] for row in convergence),
        selected_initial_state_range=[min(sensitivity), max(sensitivity)], all_checks_passed=True),
        [ROOT / 'results/scan/status.json', ROOT / 'results/preflight/status.json'])
    print(dict(state='complete', checks=len(checks), max_refinement=max(row['density_ratio_change'] for row in convergence), initial_state_range=[min(sensitivity), max(sensitivity)]), flush=True)


if __name__ == '__main__':
    main()
