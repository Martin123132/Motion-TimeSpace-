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
    checks = []
    inputs = {}

    def check(name, passed, **details):
        checks.append({'name': name, 'passed': bool(passed), **details})
        assert passed, (name, details)

    def remember(path):
        inputs[str(Path(path).resolve())] = digest(path)

    for label, script, count in [('derivation', 'derive_source.py', 31), ('matching', 'analyze_matching.py', 12)]:
        path = ROOT/f'results/{label}/status.json'
        report = read_json(path)
        check(f'{label}_exact_checks', report['state'] == 'complete' and report['exact_checks'] == count
              and len(report['checks']) == count and all(row['passed'] for row in report['checks']))
        check(f'{label}_script_hash', report['script_sha256'] == digest(ROOT/script))
        for source, expected in report.get('input_hashes', {}).items():
            check(f'{label}_source_{source}', Path(source).is_file() and digest(source) == expected)
        remember(path)
    coarse = read_json(ROOT/'results/coarse/status.json')
    fine = read_json(ROOT/'results/fine/status.json')
    matching = read_json(ROOT/'results/matching/status.json')
    for label, report in [('coarse', coarse), ('fine', fine)]:
        check(f'{label}_complete', report['state'] == 'complete' and len(report['rows']) == 6 and (ROOT/f'results/{label}/COMPLETE').is_file())
        check(f'{label}_script_hash', report['script_sha256'] == digest(ROOT/'run_companion.py'))
        check(f'{label}_system_hash', report['system_sha256'] == digest(ROOT/'axial_binary.py'))
        for source, expected in report['input_hashes'].items():
            check(f'{label}_source_{source}', Path(source).is_file() and digest(source) == expected)
        with (ROOT/f'results/{label}/rows.csv').open(encoding='utf-8', newline='') as handle:
            reader = csv.DictReader(handle)
            fields = reader.fieldnames
            rows = list(reader)
        check(f'{label}_csv_shape', len(rows) == 6 and len(fields) == len(set(fields))
              and all(None not in row and all(value is not None and value != '' for value in row.values()) for row in rows))
        check(f'{label}_csv_finite_and_matches_json', all(math.isfinite(float(value)) and float(value) == report['rows'][index][key]
              for index, row in enumerate(rows) for key, value in row.items()))
        check(f'{label}_no_fit', report['asymptotic_normalization_input_to_wave_solve'] is False)
        check(f'{label}_flat_outgoing_controls', all(row['outgoing_amplitude_error'] < 2e-8 and row['flux_normalization_error'] < 2e-12 for row in report['flat_checks']),
              maximum_error=max(row['outgoing_amplitude_error'] for row in report['flat_checks']))
        remember(ROOT/f'results/{label}/rows.csv')
        remember(ROOT/f'results/{label}/status.json')
        remember(ROOT/f'results/{label}/progress.json')
    check('same_background_and_static_sigma', coarse['body_radius'] == fine['body_radius'] and coarse['body_mass'] == fine['body_mass']
          and abs(fine['sigma_bar']/(-270.0740921927915)-1) < 2e-10)
    resolution = []
    roundoff = []
    resolved_bounds = []
    previous = None
    for rough, precise, analysis in zip(coarse['rows'], fine['rows'], matching['rows']):
        separation = precise['separation_over_radius']
        check(f'matching_orbit_{separation}', rough['separation_over_radius'] == separation == analysis['separation_over_radius'])
        error = abs(rough['infinity_increment_to_leading_magnetic']-precise['infinity_increment_to_leading_magnetic'])
        check(f'coarse_fine_increment_{separation}', error < 2e-8, normalized_increment_difference=error)
        check(f'correct_forcing_frequency_{separation}', abs(precise['frequency']**2*precise['orbit']**3/fine['body_mass']-1) < 1e-14)
        check(f'direct_stable_source_jumps_{separation}', precise['direct_to_stable_amplitude_relative_error'] < 2e-10 and
              max(precise[key] for key in ['value_jump_relative_error', 'slope_jump_relative_error', 'reference_value_jump_relative_error', 'reference_slope_jump_relative_error']) < 2e-9)
        check(f'positive_flux_and_ingoing_reference_{separation}', precise['reference_pair_power_infinity_per_mu_squared'] > 0
              and precise['body_pair_power_infinity_per_mu_squared'] > 0 and precise['reference_pair_power_horizon_per_mu_squared'] > 0
              and precise['Y_BH_imag'] < 0)
        check(f'asymptotic_flux_normalization_{separation}', max(precise['outgoing_diagnostic']['infinity_flux_normalization_error'],
                                                              precise['horizon_diagnostic']['horizon_flux_normalization_error']) < 2e-11)
        check(f'BH_boundary_control_{separation}', precise['negative_control_BH_boundary_excess'] == 0)
        check(f'absorption_separate_{separation}', abs(precise['total_infinity_plus_absorption_increment_over_Newtonian']
              -(precise['infinity_increment_over_Newtonian']-precise['reference_horizon_power_over_Newtonian'])) < 1e-25)
        check(f'first_PN_improves_{separation}', abs(analysis['residual_beyond_1PN']) < abs(analysis['observed_magnetic_ratio']-1))
        if previous is not None:
            check(f'wide_limit_approaches_{separation}', 0 < precise['infinity_increment_to_leading_magnetic']-1 < previous['infinity_increment_to_leading_magnetic']-1)
        previous = precise
        boundary_allowance = max(1e-13, 10*abs(rough['Y_body']-precise['Y_body']))
        transfer = precise['quadratic_boundary_amplitude_error_bound']/precise['boundary_remainder_bound']
        numerical_allowance = transfer*boundary_allowance+2e-15*abs(precise['amplitude_excess_real'])
        check(f'remainder_with_explicit_numerical_resolution_{separation}', precise['quadratic_boundary_amplitude_error']
              <= precise['quadratic_boundary_amplitude_error_bound']+numerical_allowance,
              analytic_bound=precise['quadratic_boundary_amplitude_error_bound'], numerical_allowance=numerical_allowance,
              measured_difference=precise['quadratic_boundary_amplitude_error'])
        if not analysis['quadratic_boundary_error_resolved']:
            roundoff.append(separation)
        else:
            resolved_bounds.append(separation)
            check(f'resolved_analytic_bound_{separation}', precise['quadratic_boundary_amplitude_error'] <= precise['quadratic_boundary_amplitude_error_bound'])
        resolution.append({'separation_over_radius': separation, 'normalized_increment_difference': error,
                           'boundary_resolution_allowance': boundary_allowance, 'amplitude_resolution_allowance': numerical_allowance})
    check('wide_orbit_leading_recovery', abs(fine['rows'][-1]['infinity_increment_to_leading_magnetic']-1) < 2.1e-4)
    check('point_current_STF_recovery', abs(fine['rows'][-1]['reference_power_to_STF_leading']-1) < 1.2e-4)
    check('first_PN_fraction_not_fitted', matching['derived_first_PN_coefficient'] == '173/84' and matching['new_coefficients_fitted'] == 0)
    check('uncomputed_tail_not_promoted', matching['tail_coefficient_derived_or_claimed'] is False)
    check('boundary_roundoff_explicit', roundoff == [20., 40., 80., 160.] and resolved_bounds == [5., 10.])
    source_path = ROOT/'sources/provenance.json'
    source = read_json(source_path)
    check('source_PDF_and_script_hash', Path(source['path']).is_file() and digest(source['path']) == source['sha256']
          and source['script_sha256'] == digest(ROOT/'acquire_source.py'))
    for name, expected in source['output_sha256'].items():
        check(f'source_render_or_extract_{name}', (ROOT/'sources'/name).is_file() and digest(ROOT/'sources'/name) == expected)
    check('four_primary_PDF_pages', source['pdf_pages_rendered'] == [6, 7, 9, 16])
    remember(source_path)
    prose = '\n'.join(path.read_text(encoding='utf-8') for path in ROOT.glob('*.md'))
    for relative in sorted(set(re.findall(r'`([^`\n]+\.(?:py|csv|json|md|pdf))`', prose))):
        if relative in {'results/validation/status.json', 'results/stage-integrity.json'}:
            continue
        path = (ROOT/relative).resolve()
        check(f'cited_local_path_{relative}', path.is_file())
        remember(path)
    check('primary_source_urls_in_prose', source['url'] in prose and 'https://doi.org/'+source['doi'] in prose)
    compiled = []
    for path in ROOT.glob('*.py'):
        compile(path.read_bytes(), str(path), 'exec')
        compiled.append(path.name)
    check('no_python_cache', not list(ROOT.rglob('__pycache__')))
    report = {'state': 'complete', 'completed_at_utc': datetime.now(timezone.utc).isoformat(),
              'script_sha256': digest(__file__), 'checks': checks, 'input_hashes': inputs, 'exact_checks': 43,
              'compiled_scripts': sorted(compiled), 'resolution_rows': resolution,
              'roundoff_limited_remainder_rows': roundoff, 'numerically_resolved_bound_rows': resolved_bounds,
              'source_urls': [source['url'], 'https://doi.org/'+source['doi']],
              'new_body_fits': 0, 'new_background_solves': 0, 'finite_mass_ratio_or_total_waveform_claim': False}
    destination = ROOT/'results/validation/status.json'
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open('x', encoding='utf-8') as handle:
        json.dump(report, handle, indent=2, allow_nan=False)
    print(json.dumps({'state': 'complete', 'checks': len(checks), 'exact_checks': 43,
                      'maximum_normalized_increment_resolution_difference': max(row['normalized_increment_difference'] for row in resolution),
                      'roundoff_limited_rows': roundoff}))


if __name__ == '__main__':
    main()
