from __future__ import annotations

import json
import numpy as np
from scipy import interpolate

from radiation_common import *


def main():
    modest_process()
    checks = []

    def check(name, passed, value=None):
        checks.append(dict(name=name, passed=bool(passed), value=value))

    thermal = read_json(ROOT / 'results/thermal-v3/status.json')
    profile = read_json(ROOT / 'results/physical-bao-profile/status.json')
    preflight = read_json(ROOT / 'results/preflight/status.json')
    sources = read_json(ROOT / 'results/sources/status.json')
    check('preflight clean', preflight['all_checks_passed'])
    check('primary DESI values unchanged', sources['all_inherited_values_verified'])
    check('thermal stage complete', thermal['state'] == 'complete')
    check('same native solver retained', thermal['camb_version'] == '1.6.6')
    for row in thermal['branches']:
        name = str((row['fraction'], row['switch_a']))
        check('flatness:' + name, row['flatness_error'] < 1e-9, row['flatness_error'])
        check('native expansion matches direct background:' + name, row['maximum_native_H_relative_difference'] < 1e-6, row['maximum_native_H_relative_difference'])
        check('independent acoustic integral:' + name, row['sound_horizon_relative_difference'] < 2e-5, row['sound_horizon_relative_difference'])
        check('early slow-field freezing controlled:' + name, row['early_frozen_slow_density_relative_change'] < 1e-8, row['early_frozen_slow_density_relative_change'])
        check('thermal outputs finite and positive:' + name, all(np.all(np.isfinite(values)) and np.min(values) > 0 for values in row['thermal_values'].values()))
        check('all measured BAO rows scored:' + name, len(row['bao']['rows']) == 13)
        check('physical-ruler constraint cannot outperform free ruler:' + name, row['bao']['chi2_fixed_physical_rd'] >= row['bao']['chi2_profiled_rd_shape_only'] - 1e-8)
        check('combined-background table not used as heavy perturbations:' + name, not row['heavy_perturbations_computed'])
    heavy_rows = [row for row in thermal['branches'] if row['fraction']]
    drag_values = [row['bao']['physical_rd_Mpc'] for row in heavy_rows]
    switch_spread = float(np.ptp(drag_values) / np.mean(drag_values))
    check('three acoustic averaging switches agree', switch_spread < 1e-5, switch_spread)
    controls = thermal['native_cold_transfer_rows']
    reference = np.array(controls[0]['fsigma8'])
    floor_difference = float(np.max(abs(np.array(controls[1]['fsigma8']) / reference - 1)))
    ppf_difference = float(np.max(abs(np.array(controls[2]['fsigma8']) / reference - 1)))
    check('all control transfer matrices finite', all(row['all_finite'] for row in controls))
    check('canonical slow-fluid floor sensitivity bounded', floor_difference < 1e-4, floor_difference)
    check('PPF cross-check of control growth bounded', ppf_difference < 1e-4, ppf_difference)
    check('failed smaller floor preserved as numerical failure', read_json(ROOT / 'runs/thermal-v2/status.json')['state'] == 'failed')
    check('first API-name error preserved', read_json(ROOT / 'runs/thermal/status.json')['state'] == 'failed')
    check('profiles converged without prior edges', all(row['converged'] and not row['edge_hit'] for row in profile['fits']))
    check('same H0 bounds for every fitted branch', all(row['bounds'] == [55., 85.] for row in profile['fits']))
    mass_residuals = []
    for row in profile['evaluations']:
        if row['mu_over_H0'] is not None:
            mass_residuals.append(abs(row['mu_over_H0'] * row['H0'] / (70 * profile['reference_slow_mass_over_H0']) - 1))
        if row['M_over_H0'] is not None:
            mass_residuals.append(abs(row['M_over_H0'] * row['H0'] / (70 * profile['reference_heavy_mass_over_H0']) - 1))
    check('physical scalar masses held fixed during profile', profile['physical_scalar_masses_held_fixed'] and max(mass_residuals) < 1e-13, max(mass_residuals))
    check('no joint or held-out result claimed', not profile['full_joint_SN_BAO_CMB_fit'] and not profile['independent_holdout'])
    check('no two-field power spectrum claimed', not profile['full_two_field_Boltzmann_prediction'])
    check('all profile budgets close', all(row['flatness_error'] < 1e-9 and row['heavy_abundance_relative_error'] < 3e-8 for row in profile['evaluations']))
    cases = []
    omega_m, slow_mass = inherited_parameters()
    for stem, fraction in [('cold-slow', 0.), ('heavy-slow', .5)]:
        data = np.load(ROOT / 'runs/thermal-v3' / (stem + '-background.npz'))
        table = {name: data[name] for name in data.files}
        species = StandardSpecies(omega_m, fraction)
        _, refined = native_background(species, table, accuracy=2.)
        original = next(row for row in thermal['branches'] if row['fraction'] == fraction and (not fraction or row['switch_a'] == .0002))
        refined_rd = refined.get_derived_params()['rdrag']
        error = abs(refined_rd / original['bao']['physical_rd_Mpc'] - 1)
        check('native thermal accuracy refinement:' + stem, error < 1e-5, error)
        scalar_density = interpolate.CubicSpline(table['efold'], table['slow_density'])
        probe = np.linspace(-4., -.01, 901)
        gradient = scalar_density(probe, 1)
        field = interpolate.CubicSpline(table['efold'], table['slow_field'])(probe)
        velocity = interpolate.CubicSpline(table['efold'], table['slow_velocity'])(probe)
        expansion2 = np.exp(interpolate.CubicSpline(table['efold'], np.log(table['expansion2']))(probe))
        conservation = float(np.max(abs(gradient + 6 * expansion2 * velocity**2) / scalar_density(probe)))
        check('independent slow-sector continuity:' + stem, conservation < 1e-5, conservation)
        if fraction:
            total_equality = lambda efold: species.matter * np.exp(-3 * efold) + fraction * omega_m * np.exp(-3 * efold) + np.exp(species.nu_log(efold) - 4 * efold) * species.nu_log(efold, 1) - species.radiation * np.exp(-4 * efold) - np.exp(species.nu_log(efold) - 4 * efold) * (1 - species.nu_log(efold, 1))
            equality_a = math.exp(optimize.brentq(total_equality, -10., -6.))
            equality_z = 1 / equality_a - 1
        else:
            equality_z = original['native_derived']['zeq']
        cases.append(dict(model=stem, refined_rd_Mpc=refined_rd, relative_rd_change=error,
            slow_continuity_relative_residual=conservation, physical_equality_z=equality_z,
            native_standard_component_zeq=original['native_derived']['zeq'],
            native_zeq_is_physical_total=not bool(fraction)))
    heavy_main = next(row for row in heavy_rows if row['switch_a'] == .0002)
    cold = thermal['branches'][0]
    fractional_rd_change = heavy_main['bao']['physical_rd_Mpc'] / cold['bao']['physical_rd_Mpc'] - 1
    check('tiny acoustic shift not promoted above absolute numerical agreement', abs(fractional_rd_change) < max(row['sound_horizon_relative_difference'] for row in thermal['branches']))
    passed = all(row['passed'] for row in checks)
    save('validation', __file__, dict(checks=checks, count=len(checks), all_checks_passed=passed,
        acoustic_switch_fractional_spread=switch_spread, native_floor_fsigma8_fractional_spread=floor_difference,
        native_ppf_fsigma8_fractional_difference=ppf_difference,
        tiny_acoustic_fractional_shift=fractional_rd_change, acoustic_shift_resolved_as_physical_signal=False,
        refinements=cases, continuation_target='Native two-component perturbation module; use separate scalar stress and matched heavy-fluid transfer, not the combined background fluid.'),
        [ROOT / 'results' / label / 'status.json' for label in ['thermal-v3', 'physical-bao-profile', 'preflight', 'sources']])
    print(json.dumps(dict(checks=len(checks), passed=passed, failed=[row for row in checks if not row['passed']])), flush=True)
    assert passed


if __name__ == '__main__':
    main()

