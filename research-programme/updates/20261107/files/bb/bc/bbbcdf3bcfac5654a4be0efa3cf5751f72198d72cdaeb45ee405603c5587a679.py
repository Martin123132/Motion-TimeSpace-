from __future__ import annotations

import csv
from datetime import datetime, timezone
from fractions import Fraction
import json
import math
from pathlib import Path
import re

import numpy as np
import psutil

from acquire_source import ROOT, digest
from axial_action import reciprocal_action


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'),
                      parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)))


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    checks, inputs = [], {}

    def check(name, passed, **details):
        checks.append({'name': name, 'passed': bool(passed), **details})
        assert passed, (name, details)

    def remember(path):
        inputs[str(Path(path).resolve())] = digest(path)

    reports = {}
    for label, script in [('derivation', 'derive_action.py'), ('current/coarse', 'run_action.py'),
                          ('current/fine', 'run_action.py'), ('replay', 'replay_action.py')]:
        path = ROOT/f'results/{label}/status.json'
        report = read_json(path)
        reports[label] = report
        check(f'{label}_complete', report['state'] == 'complete')
        check(f'{label}_script_hash', report['script_sha256'] == digest(ROOT/script))
        for source, expected in report.get('input_hashes', {}).items():
            check(f'{label}_input_{source}', Path(source).is_file() and digest(source) == expected)
            remember(source)
        remember(path)
    derivation = reports['derivation']
    check('exact_symbolic_checks', derivation['exact_checks'] == 26 and len(derivation['checks']) == 26
          and all(row['passed'] for row in derivation['checks']))
    check('response_replay_80_rows', len(reports['replay']['rows']) == 80 and reports['replay']['decimal_precision'] == 80)
    maximum_replay = max(row['maximum_reconstructed_jump_error'] for row in reports['replay']['rows'])
    check('independent_reconstructed_jumps', maximum_replay < 2e-9, maximum=maximum_replay)
    check('high_precision_optical_algebra', max(row['optical_replay_error_over_component_sum'] for row in reports['replay']['rows']) < 1e-50)
    coarse, fine = reports['current/coarse'], reports['current/fine']
    previous_path = ROOT.parent/'axial-tail-balance-20261005/results/refined/status.json'
    previous = read_json(previous_path)
    remember(previous_path)
    check('same_background_and_static_response', fine['body_mass'] == previous['body_mass']
          and fine['body_radius'] == previous['body_radius'] and abs(fine['sigma_bar']/previous['sigma_bar']-1) < 1e-10)
    current_errors, cross_errors = [], []
    for label, report in [('coarse', coarse), ('fine', fine)]:
        check(f'{label}_ten_grid_points', [row['separation_over_radius'] for row in report['grid_rows']]
              == [1.1, 1.5, 2., 3., 5., 10., 20., 40., 80., 160.])
        check(f'{label}_forty_waves_six_derivatives', len(report['all_wave_rows']) == 40 and len(report['derivative_rows']) == 6)
        check(f'{label}_no_new_body_fit_or_background', report['new_fitted_coefficients'] == report['new_background_solves'] == 0)
        for index, row in enumerate(report['all_wave_rows']):
            prefix = f'{label}_wave{index}'
            current_errors.append(row['optical_identity_error_over_component_sum'])
            check(f'{prefix}_surface_current_orientation', row['surface_data']['outgoing_slope_imag'] > 0
                  and row['surface_data']['horizon_slope_imag'] < 0)
            check(f'{prefix}_source_metric_reciprocity', row['metric_overlap_relative_error'] < 1e-12
                  and row['mass_first_law_relative_error'] < 1e-12)
            check(f'{prefix}_current_work_identity', row['optical_identity_error_over_component_sum'] < 2e-10)
            check(f'{prefix}_asymptotic_currents', row['outgoing_diagnostic']['infinity_flux_normalization_error'] < 1e-12
                  and row['horizon_diagnostic']['horizon_flux_normalization_error'] < 1e-12)
            check(f'{prefix}_fundamental_solution_controls', row['outgoing_quadrature_Wronskian_error'] < 2e-9
                  and row['outgoing_current_relative_error'] < 2e-9 and row['horizon_reconstruction_relative_error'] < 2e-9)
            check(f'{prefix}_actual_BH_boundary_control', row['BH_boundary_control_action'] == 0
                  and row['BH_boundary_control_coefficient'] == 0)
            boundary, source = row['surface_data'], row['source_data']
            body = np.array([1., boundary['body_slope']], dtype=complex)
            horizon = np.array([1., complex(boundary['horizon_slope_real'], boundary['horizon_slope_imag'])])
            outgoing = np.array([1., complex(boundary['outgoing_slope_real'], boundary['outgoing_slope_imag'])])
            values = np.array([source['real_outgoing_value'], source['real_outgoing_slope']])
            quadrature = np.array([source['dirichlet_value'], source['dirichlet_slope']])
            wave = values+1j*boundary['outgoing_slope_imag']*quadrature
            overlap = source['K']*wave[0]-source['J']*wave[1]
            action, _ = reciprocal_action(body, horizon, outgoing, overlap)
            scaled, _ = reciprocal_action(body, horizon, outgoing, 2*overlap)
            check(f'{prefix}_quadratic_mass_scaling', abs(scaled/(4*action)-1) < 1e-12)
            normalization = 2+3j
            rescaled, _ = reciprocal_action(body, horizon, normalization*outgoing, normalization*overlap)
            check(f'{prefix}_normalization_independence', abs(rescaled/action-1) < 2e-12)
        for row in report['grid_rows']:
            check(f'{label}_PN_improvement_{row["separation_over_radius"]}',
                  row['first_PN_action_relative_error'] < abs(row['action_over_leading']-1))
        errors = [abs(row['inferred_first_PN_action_coefficient']-16/3) for row in report['grid_rows']]
        check(f'{label}_derived_PN_coefficient_limit', errors[-1] < .003
              and all(first > second for first, second in zip(errors, errors[1:])))
    for row, other in zip(coarse['all_wave_rows'], fine['all_wave_rows']):
        check(f'paired_wave_orbit_{row["separation_over_radius"]}', row['separation_over_radius'] == other['separation_over_radius'])
        action_error = abs(row['action_real_per_mu_squared']/other['action_real_per_mu_squared']-1)
        net_scale = abs(other['infinity_power_difference_per_mu_squared'])+other['reference_horizon_power_per_mu_squared']
        loss_error = abs(row['net_loss_difference_per_mu_squared']-other['net_loss_difference_per_mu_squared'])/net_scale
        cross_errors.append(max(action_error, loss_error))
        check(f'wave_settings_agreement_{row["separation_over_radius"]}', max(action_error, loss_error) < 2e-8,
              action_error=action_error, loss_error=loss_error)
    prior_rows = {row['separation_over_radius']: row for row in previous['rows']}
    flux_errors = []
    for row in fine['grid_rows']:
        separation = row['separation_over_radius']
        if separation not in prior_rows:
            continue
        old = prior_rows[separation]
        power_error = abs(row['infinity_power_difference_per_mu_squared']/
                          (old['reference_pair_power_infinity_per_mu_squared']*old['fractional_infinity_pair_power_excess'])-1)
        horizon_error = abs(row['reference_horizon_power_per_mu_squared']/old['reference_pair_power_horizon_per_mu_squared']-1)
        flux_errors.append(max(power_error, horizon_error))
        check(f'previous_stage_flux_regression_{separation}', max(power_error, horizon_error) < 2e-8,
              power_error=power_error, horizon_error=horizon_error)
    derivative_settings, derivative_steps = [], []
    for row, other in zip(coarse['derivative_rows'], fine['derivative_rows']):
        errors = [abs(row[key]/other[key]-1) for key in ['energy_per_mu_squared', 'angular_momentum_per_mu_squared',
                  'energy_log_frequency_slope_per_mu_squared']]
        derivative_settings.append(max(errors))
        check(f'charge_settings_{row["separation_over_radius"]}_{row["log_frequency_step"]}', max(errors) < 2e-7, maximum=max(errors))
    for report in [coarse, fine]:
        for first, second in zip(report['derivative_rows'][::2], report['derivative_rows'][1::2]):
            errors = [abs(first[key]/second[key]-1) for key in ['energy_per_mu_squared', 'angular_momentum_per_mu_squared',
                      'energy_log_frequency_slope_per_mu_squared']]
            derivative_steps.append(max(errors))
            check(f'charge_step_{report["interior_settings"]["tolerance"]}_{first["separation_over_radius"]}',
                  max(errors) < 2e-7, maximum=max(errors))
            check(f'charge_PN_improves_{report["interior_settings"]["tolerance"]}_{first["separation_over_radius"]}',
                  abs(first['energy_over_leading']-first['energy_first_PN_ratio']) < abs(first['energy_over_leading']-1)
                  and abs(first['angular_momentum_over_leading']-first['momentum_first_PN_ratio']) < abs(first['angular_momentum_over_leading']-1))
    for degree in range(7):
        first = sum(Fraction(weight, 60)*index**degree for weight, index in zip([-1, 9, -45, 0, 45, -9, 1], range(-3, 4)))
        second = sum(Fraction(weight, 180)*index**degree for weight, index in zip([2, -27, 270, -490, 270, -27, 2], range(-3, 4)))
        check(f'first_derivative_stencil_degree{degree}', first == (1 if degree == 1 else 0))
        check(f'second_derivative_stencil_degree{degree}', second == (2 if degree == 2 else 0))
    for label in ['coarse', 'fine']:
        old = read_json(ROOT/f'results/{label}/status.json')
        check(f'{label}_rejected_run_script_preserved', old['script_sha256'] == digest(ROOT/'diagnostics/phase-normalization-v1/run_action.py')
              and old['system_sha256'] == digest(ROOT/'diagnostics/phase-normalization-v1/axial_action.py'))
        check(f'{label}_rejected_run_really_fails', max(row['optical_identity_error_over_component_sum'] for row in old['all_wave_rows']) > 1e-6)
        remember(ROOT/f'results/{label}/status.json')
        for index, row in enumerate(old['all_wave_rows']):
            corrected = reports[f'current/{label}']['all_wave_rows'][index]
            check(f'{label}_real_action_unchanged_{index}', abs(row['action_real_per_mu_squared']/corrected['action_real_per_mu_squared']-1) < 1e-12)
    check('omitting_horizon_fails_control', all(row['reference_horizon_power_per_mu_squared'] /
          (abs(row['infinity_power_difference_per_mu_squared'])+row['reference_horizon_power_per_mu_squared']) > 1e-4 for row in fine['grid_rows']))
    for label in ['coarse', 'fine']:
        for name, key in [('action-grid', 'grid_rows'), ('frequency-derivatives', 'derivative_rows')]:
            path = ROOT/f'results/current/{label}/{name}.csv'
            expected_rows = reports[f'current/{label}'][key]
            with path.open(encoding='utf-8', newline='') as handle:
                reader = csv.DictReader(handle)
                fields, rows = reader.fieldnames, list(reader)
            check(f'{label}_{name}_CSV_schema', len(rows) == len(expected_rows) and len(fields) == len(set(fields))
                  and all(None not in row and all(value is not None and value != '' for value in row.values()) for row in rows))
            for index, row in enumerate(rows):
                for field, value in row.items():
                    expected = expected_rows[index][field]
                    if isinstance(expected, str):
                        assert value == expected
                    else:
                        assert math.isfinite(float(value)) and float(value) == expected
            check(f'{label}_{name}_CSV_values', True)
            remember(path)
    provenance_path = ROOT/'sources/provenance.json'
    source = read_json(provenance_path)
    check('source_script_hash', source['script_sha256'] == digest(ROOT/'acquire_source.py'))
    check('primary_source_hash', Path(source['path']).is_file() and digest(source['path']) == source['sha256'])
    check('source_page_scope', source['pdf_pages_rendered'] == [8, 9])
    for name, expected in source['output_sha256'].items():
        check(f'source_output_{name}', digest(ROOT/'sources'/name) == expected)
    remember(provenance_path)
    prose = '\n'.join(path.read_text(encoding='utf-8') for path in ROOT.glob('*.md'))
    check('primary_source_url_and_DOI', source['url'] in prose and source['doi'] in prose)
    for relative in sorted(set(re.findall(r'`([^`\n]+\.(?:py|json|csv|md|pdf))`', prose))):
        if relative in {'results/validation/status.json', 'results/stage-integrity.json'}:
            continue
        path = (ROOT/relative).resolve()
        check(f'cited_local_path_{relative}', path.is_file())
        remember(path)
    check('scope_and_failure_disclosed', all(phrase in prose for phrase in ['test-companion', 'Einstein-Hilbert',
          'Rejected candidate', 'ordinary single-history', 'finite-mass', 'not80']))
    compiled = []
    for path in ROOT.rglob('*.py'):
        compile(path.read_bytes(), str(path), 'exec')
        compiled.append(path.relative_to(ROOT).as_posix())
    check('no_python_cache', not list(ROOT.rglob('__pycache__')))
    report = {'state': 'complete', 'time_utc': datetime.now(timezone.utc).isoformat(),
              'script_sha256': digest(__file__), 'checks': checks, 'exact_checks': 26,
              'input_hashes': inputs, 'compiled_scripts': compiled, 'source_urls': [source['url']],
              'corrected_wave_count': 80, 'maximum_optical_identity_error': max(current_errors),
              'maximum_wave_settings_difference': max(cross_errors),
              'maximum_previous_flux_regression_error': max(flux_errors),
              'maximum_charge_settings_difference': max(derivative_settings),
              'maximum_charge_step_difference': max(derivative_steps),
              'maximum_replayed_source_jump_error': maximum_replay,
              'new_coefficients_fitted': 0, 'new_background_solves': 0,
              'precision_scope': 'Binary64 ODE convergence and higher-precision algebra replay; not interval certification.',
              'rejected_candidates': ['results/coarse', 'results/fine']}
    destination = ROOT/'results/validation/status.json'
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open('x', encoding='utf-8') as handle:
        json.dump(report, handle, indent=2, allow_nan=False)
    print(json.dumps({key: value for key, value in report.items() if key.startswith('maximum_')}))
    print(json.dumps({'state': 'complete', 'checks': len(checks), 'exact_checks': 26}))


if __name__ == '__main__':
    main()
