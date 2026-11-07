from __future__ import annotations

from pathlib import Path

import mpmath as mp
import numpy as np
import sympy as sp

from matching_common import ROOT, PARENT, digest, read_json, save, modest_process


def main():
    modest_process()
    checks = []

    def check(name, passed, detail=None):
        assert bool(passed), (name, detail)
        checks.append(dict(name=name, passed=True, detail=detail))

    derivation = read_json(ROOT / 'results/derivation/status.json')
    replay = read_json(ROOT / 'results/replay/status.json')
    for report in [derivation, replay]:
        check('completed_report', report['state'] == 'complete')
        for source, expected in report['input_hashes'].items():
            check('input_hash:' + Path(source).name, digest(source) == expected)
    check('derivation_script_unchanged', digest(ROOT / 'derive_matching.py') == derivation['script_sha256'])
    check('replay_script_unchanged', digest(ROOT / 'test_matching.py') == replay['script_sha256'])
    check('exact_identities', len(derivation['exact_checks']) == 26 and all(row['passed'] for row in derivation['exact_checks']))
    check('existing_degrees_of_freedom_only', derivation['actual_new_fundamental_fields'] == 0)
    for key in ['condensate_candidate_identified_with_real_parent', 'physical_bath_spectrum_selected',
                'cold_state_preparation_derived', 'old_cosmology_replaced', 'exact_electric_charge_derived']:
        check('scope:' + key, not derivation[key])
    check('observed_shapes_retained', replay['SN_light_curve_rows'] == 1624 and replay['BAO_elements'] == 13)
    check('no_new_growth_fit_claim', not replay['growth_or_galaxy_likelihood_run'])
    check('no_H0_prediction_claim', not replay['H0_fitted_or_predicted'])
    for row in replay['replays']:
        check('actual_data_replay:' + row['model'], abs(row['chi2'] - row['archived_chi2']) < 1e-7)
        check('no_finite_mass_fit_claim:' + row['model'], not row['exact_finite_mass_cosmology_rerun'])
        for split in row['dust_replacement_replays']:
            check('no_double_count:' + row['model'] + ':' + str(split['heavy_share_of_existing_dust']), abs(split['delta_chi2']) < 1e-7 and split['max_relative_expansion_difference'] < 5e-15)
        check('double_count_fails:' + row['model'], row['double_count_negative_control_chi2'] - row['chi2'] > 100)
    for index, row in enumerate(replay['coupled_real_field_replays']):
        check('independent_coordinates:' + str(index), row['max_field_error'] < 2e-9 and row['max_relative_stress_error'] < 2e-8)
        check('omitting_interaction_fails:' + str(index), row['omitted_interaction_negative_control_error'] > .01)
    mp.mp.dps = 80
    hierarchy_replays = []
    for row in replay['scale_checks']:
        light = mp.mpf(str(row['fitted_light_mass_over_H0']))
        bath = mp.mpf(str(row['required_frequency_over_H0']))
        for entry in row['hierarchy_cost_examples']:
            share = mp.mpf(str(entry['motion_overlap_in_heavy_mode']))
            mixing = mp.sqrt(share / (1 - share))
            gap = bath**2 - light**2
            coupling = mixing * gap
            bare2 = light**2 + mixing**2 * gap
            trace = bare2 + bath**2
            discriminant = mp.sqrt((bare2 - bath**2)**2 + 4 * coupling**2)
            recovered = (trace - discriminant) / 2
            error = abs(recovered / light**2 - 1)
            check('high_precision_light_pole:' + row['model'] + ':' + str(share), error < mp.mpf('1e-55'))
            shift = (bare2 - light**2) / light**2
            check('hierarchy_cost:' + row['model'] + ':' + str(share), abs(float(shift) / entry['required_relative_bare_light_mass2_shift'] - 1) < 2e-14)
            hierarchy_replays.append(dict(model=row['model'], heavy_motion_overlap=str(share), relative_light_pole_error=str(error), mass2_matching_shift=str(shift)))
    general_baths = []
    for seed in range(5):
        rng = np.random.default_rng(1000 + seed)
        light2 = .8**2
        masses2 = np.array([4., 7., 11., 20.])**2
        couplings = rng.uniform(.2, 2., size=4)
        first = np.sum(couplings**2 / (masses2 - light2))
        second = np.sum(couplings**2 / (masses2 - light2)**2)
        matrix = np.diag(np.concatenate([[light2 + first], masses2]))
        matrix[0, 1:] = -couplings
        matrix[1:, 0] = -couplings
        eigenvalues, eigenvectors = np.linalg.eigh(matrix)
        residue = 1 / (1 + second)
        delta = first / light2
        bound = (masses2.min() / light2 - 1) * second
        check('many_bath_light_eigenvalue:' + str(seed), abs(eigenvalues[0] - light2) < 1e-12)
        check('many_bath_positive:' + str(seed), min(eigenvalues) > 0)
        check('many_bath_residue:' + str(seed), abs(eigenvectors[0, 0]**2 - residue) < 1e-13)
        check('many_bath_hierarchy_bound:' + str(seed), delta >= bound)
        general_baths.append(dict(seed=seed, light_eigenvalue=float(eigenvalues[0]), pole_residue=float(residue), relative_mass_shift=float(delta), lower_bound=float(bound)))
    hubble, cosmic_a, theta, perturbation, pert_dot, grav, density, mass, wave = sp.symbols('hubble cosmic_a theta perturbation pert_dot grav density mass wave', nonzero=True)
    theta_dot = -hubble * theta - 4 * sp.pi * grav * cosmic_a * density * perturbation + wave**4 * perturbation / (4 * mass**2 * cosmic_a**3)
    delta_ddot = (-theta_dot / cosmic_a + hubble * theta / cosmic_a).subs(theta, -cosmic_a * pert_dot)
    growth_residual = sp.simplify(delta_ddot + 2 * hubble * pert_dot + (wave**4 / (4 * mass**2 * cosmic_a**4) - 4 * sp.pi * grav * density) * perturbation)
    check('derived_linear_growth_equation', growth_residual == 0, str(growth_residual))
    wrong_growth_residual = sp.simplify(delta_ddot + 2 * hubble * pert_dot - 4 * sp.pi * grav * density * perturbation)
    check('omitting_wave_pressure_fails', wrong_growth_residual != 0, str(wrong_growth_residual))
    unmatched = np.array([[.88**2, -.2 * (5**2 - .88**2)], [-.2 * (5**2 - .88**2), 5**2]])
    check('unmatched_bare_mass_can_destabilize', np.linalg.eigvalsh(unmatched)[0] < 0, float(np.linalg.eigvalsh(unmatched)[0]))
    check('no_bytecode_cache', not list(ROOT.rglob('__pycache__')))
    save('validation', __file__, dict(checks=checks, count=len(checks), high_precision_poles=hierarchy_replays,
        many_bath_checks=general_baths, exact_linear_growth_residual=str(growth_residual),
        all_checks_passed=True, spectrum_or_abundance_prediction=False, previous_framework_preserved=True),
        [ROOT / 'results/derivation/status.json', ROOT / 'results/replay/status.json'])
    print(dict(state='complete', validation_checks=len(checks), high_precision_poles=len(hierarchy_replays), positive_many_bath_examples=len(general_baths)), flush=True)


if __name__ == '__main__':
    main()
