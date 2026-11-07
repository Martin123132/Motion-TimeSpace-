from __future__ import annotations

import csv
import json
from pathlib import Path
import re

import mpmath as mp
import numpy as np

from eccentric_radiation import ROOT, BRANCH, digest, modest_process, save_json, report_header, paired_flux


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'),
                      parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)))


def main():
    modest_process()
    checks, inputs, reports = [], {}, {}

    def check(name, passed, **details):
        checks.append({'name': name, 'passed': bool(passed), **details})
        assert passed, (name, details)

    def remember(path):
        inputs[str(Path(path).resolve())] = digest(path)

    expected_counts = {'coarse': 179, 'fine': 179, 'quadrature': 179, 'extension': 64}
    for label, script in [('derivation', 'derive_flux.py'), ('newtonian-control', 'derive_newtonian_control.py'),
                          ('coarse', 'run_radiation.py'), ('fine', 'run_radiation.py'),
                          ('quadrature', 'run_radiation.py'), ('extension', 'run_radiation.py'),
                          ('analysis', 'analyze_spectrum.py')]:
        path = ROOT/f'results/{label}/status.json'
        report = read_json(path)
        reports[label] = report
        check(f'{label}_complete', report['state'] == 'complete')
        check(f'{label}_script_hash', report['script_sha256'] == digest(ROOT/script))
        for source, expected in report['input_hashes'].items():
            check(f'{label}_input_{source}', Path(source).is_file() and digest(source) == expected)
            remember(source)
        remember(path)
        if label in ['derivation', 'newtonian-control']:
            check(f'{label}_exact_checks', len(report['checks']) == report['exact_checks']
                  and all(row['passed'] for row in report['checks']))
        if label not in expected_counts:
            continue
        check(f'{label}_mode_count', len(report['rows']) == expected_counts[label])
        check(f'{label}_scope', report['new_background_solves'] == report['new_fitted_parameters'] == 0
              and report['sector'] == 'odd ell2 m+/-1 only' and not report['self_force_or_inspiral_integrated'])
        for saved in report['saved_archives']:
            path = Path(saved['path'])
            check(f'{label}_{path.name}_hash', digest(path) == saved['sha256'])
            with np.load(path, allow_pickle=False) as archive:
                check(f'{label}_{path.name}_finite', all(np.isfinite(archive[key]).all() for key in archive.files))
                wronskian = archive['real_outgoing'][:, 0]*archive['dirichlet'][:, 1]-archive['real_outgoing'][:, 1]*archive['dirichlet'][:, 0]
                check(f'{label}_{path.name}_saved_Wronskian', np.max(np.abs(wronskian-1)) < 1e-9)
            remember(path)
        for index, row in enumerate(report['rows']):
            prefix = f'{label}_{index}'
            scalar = [value for value in row.values() if isinstance(value, (float, int))]
            check(prefix+'_finite', all(np.isfinite(scalar)))
            check(prefix+'_positive_energy', row['BH_infinity_energy'] >= 0 and row['body_infinity_energy'] >= 0
                  and row['BH_horizon_energy'] >= 0)
            check(prefix+'_signed_currents', row['frequency']*row['beta_out'] > 0 and row['frequency']*row['beta_horizon'] < 0)
            check(prefix+'_source_controls', row['full_source_integral_error_over_absolute_scale'] < 1e-10
                  and row['direct_body_amplitude_error_over_source_scale'] < 1e-10)
            check(prefix+'_radial_controls', row['Wronskian_error'] < 1e-9 and row['BH_reconstruction_relative_error'] < 1e-9)
            check(prefix+'_optical_identity', row['optical_error_over_component_sum'] < 2e-10)
            for key in ['outgoing_diagnostic', 'horizon_diagnostic']:
                error_key = 'infinity_flux_normalization_error' if key == 'outgoing_diagnostic' else 'horizon_flux_normalization_error'
                check(prefix+'_'+error_key, row[key][error_key] < 1e-10)
            amplitude = complex(row['reference_amplitude_real'], row['reference_amplitude_imag'])
            energy, angular = paired_flux(row['frequency'], amplitude)
            check(prefix+'_flux_replay', abs(energy/row['BH_infinity_energy']-1) < 2e-14
                  and abs(angular/row['BH_infinity_angular']-1) < 2e-14)
            horizon_boundary = complex(row['alpha_horizon'], row['beta_horizon'])
            outgoing_boundary = complex(row['alpha_out'], row['beta_out'])
            overlap_out = complex(row['source_real_basis'], row['beta_out']*row['source_Dirichlet_basis'])
            body_boundary = horizon_boundary
            matched_reference_difference = -(horizon_boundary-body_boundary)*overlap_out/((outgoing_boundary-body_boundary)*(outgoing_boundary-horizon_boundary))
            check(prefix+'_actual_absorbing_BH_boundary_substitution', matched_reference_difference == 0 and horizon_boundary.imag != 0)
        csv_path = ROOT/f'results/{label}/spectrum.csv'
        with csv_path.open(encoding='utf-8', newline='') as handle:
            csv_rows = list(csv.DictReader(handle))
        check(f'{label}_CSV_complete', len(csv_rows) == len(report['rows'])
              and all(None not in row and None not in row.values() for row in csv_rows))
        remember(csv_path)
        check(f'{label}_completion_marker', (ROOT/f'results/{label}/COMPLETE').is_file())
    analysis = reports['analysis']
    check('nineteen_exact_checks', reports['derivation']['exact_checks']+reports['newtonian-control']['exact_checks'] == 19)
    check('circular_old_result_recovered', max(analysis['circular_regression_relative_errors'].values()) < 1e-9)
    check('weighted_refinements', analysis['maximum_refinement_change'] < 1e-6)
    check('scope_not_all_multipoles_or_certified_tail', not analysis['spectrum_is_total_gravitational_radiation']
          and not analysis['infinite_harmonic_tail_certified'])
    for row in analysis['totals']:
        check(f'Newtonian_current_e{row["eccentricity"]}', .95 < row['BH_infinity_to_leading_Newtonian_current'] < 1.05)
        if row['eccentricity'] > 0:
            check(f'negative_frequency_omission_detectable_e{row["eccentricity"]}', row['negative_frequency_BH_infinity_fraction'] > 1e-5)
        omission = abs((row['difference_infinity_energy']-row['difference_total_energy'])/row['difference_infinity_energy'])
        check(f'horizon_omission_detectable_e{row["eccentricity"]}', omission > 1e-4)
    for eccentricity, cutoff in [(.3, 16), (.6, 64)]:
        row = next(row for row in analysis['tails'] if row['eccentricity'] == eccentricity and row['cutoff'] == cutoff)
        check(f'tested_tail_e{eccentricity}', max(value for key, value in row.items() if key.endswith('tail_fraction')) < 1e-6)
    for name in ['totals', 'tails', 'refinements']:
        path = ROOT/f'results/analysis/{name}.csv'
        with path.open(encoding='utf-8', newline='') as handle:
            records = list(csv.DictReader(handle))
        check(f'analysis_{name}_CSV_valid', records and all(None not in row and None not in row.values() for row in records))
        remember(path)
    mp.mp.dps = 90
    high_precision_errors = []
    selected = [row for label in ['fine', 'extension'] for row in reports[label]['rows']
                if row['harmonic'] in [-96, -2, -1, 0, 5, 16, 64, 96]]
    for row in selected:
        number = lambda key: mp.mpf(str(row[key]))
        body_slope = number('body_Y')/mp.mpf(str(reports['fine']['orbits'][0]['radius']))
        outgoing = mp.mpc(number('alpha_out'), number('beta_out'))
        horizon = mp.mpc(number('alpha_horizon'), number('beta_horizon'))
        integral_out = mp.mpc(number('source_real_basis'), number('beta_out')*number('source_Dirichlet_basis'))
        integral_horizon = mp.mpc(number('source_real_basis')+(number('alpha_horizon')-number('alpha_out'))*number('source_Dirichlet_basis'),
                                  number('beta_horizon')*number('source_Dirichlet_basis'))
        delta = -(horizon-body_slope)*integral_out/((outgoing-body_slope)*(outgoing-horizon))
        reference = integral_horizon/(outgoing-horizon)
        signed_infinity = number('beta_out')*(2*mp.re(mp.conj(reference)*delta)+abs(delta)**2)
        signed_horizon = -number('beta_horizon')*abs(integral_out/(outgoing-horizon))**2
        optical = -mp.im(delta*integral_out)
        error = abs(optical-signed_infinity+signed_horizon)/(abs(signed_infinity)+abs(signed_horizon))
        high_precision_errors.append(float(error))
    check('ninety_digit_optical_algebra_replay', max(high_precision_errors) < 1e-70)
    check('zero_frequency_flux_branch', paired_flux(0., 1+2j) == (0., 0.))
    pilot_path = ROOT/'results/pilot/status.json'
    pilot = read_json(pilot_path)
    check('pilot_is_retained_failed_quadrature_control', max(row['full_source_integral_error_over_absolute_scale'] for row in pilot['rows']) > 1e-10
          and (pilot_path.parent/'DIAGNOSTIC.md').is_file())
    check('pilot_original_runner_preserved', pilot['script_sha256'] == digest(pilot_path.parent/'run_radiation_v1.py'))
    for source, expected in pilot['input_hashes'].items():
        path = pilot_path.parent/'eccentric_radiation_v1.py' if Path(source).name == 'eccentric_radiation.py' else Path(source)
        check(f'pilot_original_input_{path.name}', digest(path) == expected)
        remember(path)
    for saved in pilot['saved_archives']:
        check(f'pilot_primitive_{Path(saved["path"]).name}', digest(saved['path']) == saved['sha256'])
    remember(pilot_path)
    for name in ['31-eccentric-axial-radiation-and-modal-work.md', 'RESULTS.md', 'RESUME.md']:
        path = ROOT/name
        check(f'document_{name}', path.is_file())
        remember(path)
        for relative in re.findall(r'`((?:\.\./|results/)[^`]+)`', path.read_text(encoding='utf-8')):
            if relative != 'results/validation/status.json':
                check(f'citation_{relative}', (ROOT/relative).exists())
    compiled = []
    for path in ROOT.rglob('*.py'):
        compile(path.read_bytes(), str(path), 'exec')
        compiled.append(path.relative_to(ROOT).as_posix())
        remember(path)
    check('no_python_cache', not list(ROOT.rglob('__pycache__')))
    output = ROOT/'results/validation'
    output.mkdir(parents=True, exist_ok=False)
    report = {**report_header(__file__), 'checks': checks, 'exact_checks': 19, 'input_hashes': inputs,
              'compiled_scripts': compiled, 'maximum_weighted_flux_refinement': analysis['maximum_refinement_change'],
              'maximum_ninety_digit_optical_error': max(high_precision_errors),
              'ninety_digit_scope': 'Algebra replay using binary64 ODE outputs, not 90-digit radial solutions.',
              'maximum_full_source_scaled_error': analysis['maximum_source_identity_scaled_error'],
              'circular_regression_maximum_error': max(analysis['circular_regression_relative_errors'].values()),
              'source_urls': ['https://arxiv.org/abs/gr-qc/0502028', 'https://arxiv.org/pdf/gr-qc/0502028',
                              'https://doi.org/10.1103/PhysRevD.71.104003'],
              'web_verified_utc_date': '2026-10-05', 'sector': 'odd ell2 m+/-1 only',
              'actual_eccentric_wave_fluxes_and_source_work_computed': True,
              'infinite_harmonic_tail_certified': False, 'full_orbital_evolution_integrated': False}
    save_json(output/'status.json', report)
    print(json.dumps({'state': 'complete', 'validation_checks': len(checks), 'exact_checks': 19,
                      'maximum_refinement': analysis['maximum_refinement_change'],
                      'maximum_90digit_error': max(high_precision_errors)}))


if __name__ == '__main__':
    main()
