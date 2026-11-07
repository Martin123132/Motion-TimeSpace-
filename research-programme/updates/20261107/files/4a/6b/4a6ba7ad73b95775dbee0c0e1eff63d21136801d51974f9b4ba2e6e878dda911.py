from __future__ import annotations

import csv
from datetime import datetime, timezone
import json
import math
from pathlib import Path
import re

import psutil

from acquire_source import ROOT, digest


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
    for name, script in [('derivation', 'derive_tail_balance.py'), ('refined', 'run_refinement.py'),
                         ('extended-control', 'run_extended_control.py'), ('balance', 'evaluate_balance.py')]:
        path = ROOT/f'results/{name}/status.json'
        report = read_json(path)
        reports[name] = report
        check(f'{name}_complete', report['state'] == 'complete')
        check(f'{name}_script_hash', report['script_sha256'] == digest(ROOT/script))
        for source, expected in report.get('input_hashes', {}).items():
            check(f'{name}_input_{source}', Path(source).is_file() and digest(source) == expected)
            remember(source)
        remember(path)
    derivation = reports['derivation']
    check('exact_symbolic_identities', derivation['exact_checks'] == 33 and len(derivation['checks']) == 33
          and all(row['passed'] for row in derivation['checks']))
    check('four_direct_tail_quadratures', len(derivation['direct_complex_integral_quadratures']) == 4
          and all(float(row['relative_error']) < 1e-35 for row in derivation['direct_complex_integral_quadratures']))
    for row in derivation['damping_checks']:
        errors = row['relative_errors']
        check(f'Abel_limit_{row["frequency"]}', errors[-1] < 1e-5 and all(first > second for first, second in zip(errors, errors[1:])))
    check('current_and_mass_tails_distinguished', derivation['flux_tail_m1'] == '2*pi*x^(3/2)' and derivation['flux_tail_m2'] == '4*pi*x^(3/2)')
    point_path = Path(derivation['point_PN_reference_source'])
    point_text = point_path.read_text(encoding='utf-8')
    check('inherited_point_reference_exists', point_path.is_file() and '1247/336' in point_text and '4pi' in point_text.replace('*', '').replace(' ', ''))
    remember(point_path)
    refined, balance = reports['refined'], reports['balance']
    check('nine_refined_orbits', [row['separation_over_radius'] for row in refined['rows']] == [5., 10., 20., 40., 80., 160., 320., 640., 1280.])
    check('three_extended_controls', [row['separation_over_radius'] for row in reports['extended-control']['rows']] == [320., 640., 1280.])
    check('no_new_body_fit_or_background_solve', balance['new_coefficients_fitted'] == refined['new_body_fits'] == 0
          and balance['new_background_solves'] == refined['new_background_solves'] == 0)
    previous_body = read_json(ROOT.parent/'axial-companion-20261005/results/fine/status.json')
    check('same_body_M_R_sigma', refined['body_mass'] == previous_body['body_mass'] and refined['body_radius'] == previous_body['body_radius']
          and abs(refined['sigma_bar']/previous_body['sigma_bar']-1) < 1e-10)
    resolution_marginal = []
    for row in balance['tail_controls']:
        label = f'{row["sector"]}_{row["separation_over_radius"]}'
        check(f'tail_coefficient_{label}', row['derived_tail_coefficient'] == 2*math.pi)
        check(f'tail_improves_{label}', row['tail_corrected_error'] < row['first_PN_error'])
        check(f'wrong_frequency_rejected_{label}', row['wrong_m2_frequency_error'] > 10*row['tail_corrected_error'])
        check(f'resolution_{label}', row['resolution_difference'] < 2e-8 and row['resolution_difference'] < row['first_PN_error']/100)
        if row['tail_corrected_error'] < 10*row['resolution_difference']:
            resolution_marginal.append(label)
    for sector in ['point_current', 'magnetic_infinity_increment']:
        rows = [row for row in balance['tail_controls'] if row['sector'] == sector]
        check(f'decreasing_remainder_{sector}', all(first['tail_corrected_error'] > second['tail_corrected_error'] for first, second in zip(rows, rows[1:])))
    for row, wave in zip(balance['chirp_contributions'], refined['rows']):
        separation = row['separation_over_radius']
        check(f'stable_geodesic_energy_slope_{separation}', 0 < row['x'] < 1/6 and row['geodesic_energy_slope'] > 0)
        check(f'sourced_jump_control_{separation}', max(wave[key] for key in ['value_jump_relative_error', 'slope_jump_relative_error',
              'reference_value_jump_relative_error', 'reference_slope_jump_relative_error']) < 2e-9 and wave['direct_to_stable_amplitude_relative_error'] < 2e-10)
        check(f'split_chirp_identity_{separation}', abs(row['delta_chirp_total_axial_over_Newtonian']
              -(wave['infinity_increment_over_Newtonian']-wave['reference_horizon_power_over_Newtonian'])/row['geodesic_energy_slope']) < 1e-25)
        check(f'opposite_flux_contributions_{separation}', row['delta_chirp_infinity_over_Newtonian'] > 0
              and row['delta_chirp_absent_BH_absorption_over_Newtonian'] < 0)
        check(f'balanced_resolution_{separation}', row['total_axial_resolution_fraction_of_component_sum'] < 2e-8)
        check(f'horizon_low_frequency_law_{separation}', abs(row['horizon_power_to_derived_leading']-row['horizon_power_first_PN_prediction']) < 25*row['x']**2)
    selected = {row['separation_over_radius']: row for row in balance['chirp_contributions']}
    check('leading_crossover_bracket', 320 < balance['leading_axial_loss_crossover_D_over_R'] < 640
          and selected[320.]['delta_chirp_total_axial_over_Newtonian'] > 0 and selected[640.]['delta_chirp_total_axial_over_Newtonian'] < 0)
    check('three_phase_bands', len(balance['phase_bands']) == 3)
    for row in balance['phase_bands']:
        check(f'phase_quadrature_{row["start_D_over_R"]}', float(row['maximum_primitive_quadrature_relative_error']) < 1e-45)
        check(f'phase_signs_{row["start_D_over_R"]}', float(row['q_times_delta_Phi_magnetic_radians']) < 0
              and float(row['q_times_delta_Phi_absent_axial_absorption_radians']) > 0)
    csv_reports = [(ROOT/'results/refined/rows.csv', refined['rows']),
                   (ROOT/'results/balance/tail-controls.csv', balance['tail_controls']),
                   (ROOT/'results/balance/chirp-contributions.csv', balance['chirp_contributions']),
                   (ROOT/'results/balance/phase-bands.csv', balance['phase_bands'])]
    for path, expected_rows in csv_reports:
        with path.open(encoding='utf-8', newline='') as handle:
            reader = csv.DictReader(handle)
            fields, rows = reader.fieldnames, list(reader)
        check(f'CSV_schema_{path.name}', len(rows) == len(expected_rows) and len(fields) == len(set(fields))
              and all(None not in row and all(value is not None and value != '' for value in row.values()) for row in rows))
        for index, row in enumerate(rows):
            for key, value in row.items():
                expected = expected_rows[index][key]
                if isinstance(expected, str):
                    assert value == expected, (path, key)
                else:
                    assert math.isfinite(float(value)) and float(value) == expected, (path, key)
        check(f'CSV_values_{path.name}', True)
        remember(path)
    source_path = ROOT/'sources/provenance.json'
    source = read_json(source_path)
    check('primary_source_hash', Path(source['path']).is_file() and digest(source['path']) == source['sha256'])
    check('source_script_hash', source['script_sha256'] == digest(ROOT/'acquire_source.py'))
    for name, expected in source['output_sha256'].items():
        check(f'source_file_{name}', (ROOT/'sources'/name).is_file() and digest(ROOT/'sources'/name) == expected)
    check('source_page_scope', source['page_count'] == 8 and source['pdf_pages_rendered'] == [3])
    remember(source_path)
    prose = '\n'.join(path.read_text(encoding='utf-8') for path in ROOT.glob('*.md'))
    check('primary_url_in_prose', source['url'] in prose)
    for relative in sorted(set(re.findall(r'`([^`\n]+\.(?:py|json|csv|md|pdf))`', prose))):
        if relative in {'results/validation/status.json', 'results/stage-integrity.json'}:
            continue
        path = (ROOT/relative).resolve()
        check(f'cited_local_path_{relative}', path.is_file())
        remember(path)
    check('scope_explicit_in_prose', 'test-companion' in prose and 'Other sectors' in prose and 'finite-mass' in prose)
    compiled = []
    for path in ROOT.glob('*.py'):
        compile(path.read_bytes(), str(path), 'exec')
        compiled.append(path.name)
    check('no_python_cache', not list(ROOT.rglob('__pycache__')))
    report = {'state': 'complete', 'time_utc': datetime.now(timezone.utc).isoformat(),
              'script_sha256': digest(__file__), 'checks': checks, 'exact_checks': 33,
              'input_hashes': inputs, 'compiled_scripts': compiled, 'source_urls': [source['url']],
              'subleading_remainder_resolution_marginal_rows': resolution_marginal,
              'maximum_tail_control_resolution_difference': max(row['resolution_difference'] for row in balance['tail_controls']),
              'precision_scope': 'Changed numerical settings, not interval bounds or a total-waveform error estimate.',
              'new_coefficients_fitted': 0, 'new_background_solves': 0}
    destination = ROOT/'results/validation/status.json'
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open('x', encoding='utf-8') as handle:
        json.dump(report, handle, indent=2, allow_nan=False)
    print(json.dumps({'state': 'complete', 'checks': len(checks), 'exact_checks': 33,
                      'maximum_resolution_difference': report['maximum_tail_control_resolution_difference'],
                      'marginal_subleading_rows': resolution_marginal}))


if __name__ == '__main__':
    main()
