from __future__ import annotations

import subprocess
import traceback

from native_common import *


def main():
    modest()
    folder = ROOT / 'results' / (sys.argv[1] if len(sys.argv)>1 else 'validation')
    folder.mkdir(parents=True, exist_ok=False)
    checks = []

    def check(name, passed, value=None, limit=None):
        checks.append(dict(name=name, passed=bool(passed), value=value, limit=limit))

    backgrounds = json.loads((ROOT / 'runs/backgrounds/status.json').read_text())
    cold = json.loads((ROOT / 'runs/cold-controls/status.json').read_text())
    analysis = json.loads((ROOT / 'results/final-early-analysis/status.json').read_text())
    symbolic = json.loads((ROOT / 'results/identities/status.json').read_text())
    check('isolated_CAMB_loaded', Path(camb.__file__).resolve().is_relative_to(ROOT / 'native'))
    check('five_exact_action_and_seed_identities', symbolic['all_checks_passed'] and symbolic['count'] == 5)
    check('temporary_build_mapping_removed', not Path('R:/').exists())
    for row in backgrounds['branches']:
        check('native_background_H_F' + str(row['fraction']), row['maximum_native_H_relative_error'] < 1e-7,
            row['maximum_native_H_relative_error'], 1e-7)
        check('flatness_F' + str(row['fraction']), row['flatness_error'] < 1e-10, row['flatness_error'], 1e-10)
    for row in cold['models']:
        check(row['model'] + '_finite_transfers', row['transfer_finite'])
        check(row['model'] + '_sigma8', row['sigma8_max_relative_error'] < 1e-6, row['sigma8_max_relative_error'], 1e-6)
        check(row['model'] + '_fsigma8', row['fsigma8_max_relative_error'] < 1e-6, row['fsigma8_max_relative_error'], 1e-6)
        maximum = max(item['normalized_max_error'] for item in row['transfer_comparisons'])
        check(row['model'] + '_transfer_shapes', maximum < 1e-5, maximum, 1e-5)
    comparisons = analysis['convergence_comparisons']
    for key, limit in [('cold_ratio_relative_change', 1e-6), ('heavy_delta_relative_change', 1e-5),
        ('heavy_velocity_relative_change', 1e-5)]:
        maximum = max(row[key] for row in comparisons)
        check('resolved_' + key, maximum < limit, maximum, limit)
    matches = analysis['matches']['final-bg8-start']
    maximum = max(row['pressure_mismatch_over_mode_norm'] for row in matches)
    check('phase_averaged_pressure_consistency', maximum < 2e-6, maximum, 2e-6)
    target = .5 * previous.inherited_parameters()[0] * 3 * (previous.H0/previous.C_LIGHT)**2
    abundance_error = max(abs(row['background_comoving_density_native']/target-1) for row in matches)
    check('averaged_background_abundance', abundance_error < 2e-6, abundance_error, 2e-6)
    for label in ['final-bg4', 'final-bg8', 'final-bg8-start']:
        report = json.loads((ROOT / 'runs' / label / 'status.json').read_text())
        check(label + '_finite_complete', report['state']=='complete' and all(row['all_finite'] for row in report['rows']))
        output = np.load(ROOT / 'runs' / label / 'heavy.npz')
        actual_a = output['values'][0, :, 13]
        error = float(np.max(abs(actual_a/output['requested_scale']-1)))
        check(label + '_time_to_scale_mapping', error < 2e-8, error, 2e-8)
        log = (ROOT / 'runs' / (label + '.log')).read_text(encoding='utf-8')
        check(label + '_no_native_warning', 'Warning' not in log and 'ERROR' not in log)
    output = np.load(ROOT / 'runs/final-bg8-start/heavy.npz')
    names = output['names'].tolist()
    scales = np.ascontiguousarray(output['values'][0, :, names.index('a')])
    params = params_for(ROOT / 'runs/backgrounds/heavy.npz', accuracy=2.5)
    native = camb.get_background(params, no_thermo=True)
    densities = native.get_background_densities(scales, vars=['cdm', 'baryon', 'photon', 'neutrino', 'nu'])
    densities = {name: values / scales**2 for name, values in densities.items()}
    matter_density = densities['cdm'] + densities['baryon'] + densities['nu']
    table = np.load(ROOT / 'runs/backgrounds/heavy.npz')
    phi = interpolate.CubicSpline(table['heavy_efold'], table['phi_h'])(np.log(scales))
    velocity = interpolate.CubicSpline(table['heavy_efold'], table['phidot_h'])(np.log(scales))
    heavy_mass = float(table['heavy_mass_mpc'])
    diagnostics = []
    for mode_index, mode in enumerate(output['modes']):
        values = output['values'][mode_index]
        component_map = [('cdm', 'delta_cdm'), ('baryon', 'delta_baryon'), ('photon', 'delta_photon'),
            ('neutrino', 'delta_neutrino'), ('nu', 'delta_nu')]
        terms = [densities[component] * values[:, names.index(column)] for component, column in component_map]
        terms += [values[:, names.index('mts_drho_s')], values[:, names.index('mts_drho_h')]]
        total = sum(terms)
        reported = matter_density * values[:, names.index('delta_tot_de')]
        error = float(np.max(abs(total-reported)/np.maximum(np.sum(np.abs(terms), axis=0), 1e-30)))
        check('metric_density_assembly_k' + str(mode), error < 2e-6, error, 2e-6)
        delta = values[:, names.index('mts_dphi_h')]
        delta_velocity = values[:, names.index('mts_dphidot_h')]
        kinetic, potential = velocity * delta_velocity, (scales*heavy_mass)**2 * phi * delta
        stress_norm = np.maximum(abs(kinetic)+abs(potential), 1e-30)
        density_error = float(np.max(abs(kinetic+potential-values[:, names.index('mts_drho_h')])/stress_norm))
        check('independent_scalar_stress_k' + str(mode), density_error < 1e-6, density_error, 1e-6)
        times = output['conformal_time']
        selected = np.where((scales > .0002485) & (scales < .0002515))[0][::15]
        derivative_errors = []
        for index in selected:
            stencil = np.arange(index-5, index+6)
            offsets = times[stencil]-times[index]
            scale_time = max(abs(offsets))
            coefficients = np.polynomial.polynomial.polyfit(offsets/scale_time, delta[stencil], 7)
            derivative_errors.append(abs(coefficients[1]/scale_time-delta_velocity[index]))
        velocity_scale = float(np.max(abs(delta_velocity[(scales > .000248) & (scales < .000252)])))
        derivative_error = max(derivative_errors)/velocity_scale
        check('field_velocity_from_independent_time_difference_k' + str(mode), derivative_error < 1e-4,
            derivative_error, 1e-4)
        diagnostics.append(dict(k=float(mode), metric_density_relative_error=error,
            scalar_stress_relative_error=density_error, field_derivative_normalized_error=derivative_error))
    invalid = MTSTwoField()
    for label, nodes, first, second in [('unordered', [0., -1., -2., -3.], [1.]*4, [0.]*4),
        ('nan', [-3., -2., -1., 0.], [1., np.nan, 1., 1.], [0.]*4),
        ('wrong_length', [-3., -2., -1., 0.], [1.]*3, [0.]*4)]:
        try:
            invalid.set_table('SetSlowTable', nodes, first, second)
            rejected = False
        except ValueError:
            rejected = True
        check('reject_' + label + '_table', rejected)
    command = [sys.executable, '-B', str(ROOT / 'run_native_early.py'), 'expected-domain-rejection', '--end', '.00029']
    rejected = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, timeout=180)
    (folder / 'domain-rejection.log').write_text(rejected.stdout, encoding='utf-8')
    check('native_heavy_late_domain_rejected', rejected.returncode != 0 and 'exact domain exceeded' in rejected.stdout,
        rejected.returncode)
    write_json(ROOT / 'runs/expected-domain-rejection/status.json', dict(state='expected_failure', exit_code=rejected.returncode,
        reason='Guard prevents using an unimplemented late heavy perturbation continuation',
        evidence_log=str(folder / 'domain-rejection.log')))
    report = dict(checks=checks, count=len(checks), all_checks_passed=all(row['passed'] for row in checks),
        independent_stress_diagnostics=diagnostics, historical_underresolution_rejected=True)
    finish(folder, report, __file__, [ROOT / 'results/final-early-analysis/status.json', ROOT / 'results/identities/status.json',
        ROOT / 'runs/cold-controls/status.json', ROOT / 'runs/backgrounds/status.json'])
    print(json.dumps(dict(count=len(checks), failed=[row for row in checks if not row['passed']]), indent=2), flush=True)
    assert report['all_checks_passed']


if __name__ == '__main__':
    main()
