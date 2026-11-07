from __future__ import annotations

import csv
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import re

import psutil


ROOT = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


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

    for name, script, count in [('derivation', 'derive_master.py', 31), ('bounds', 'derive_response_bounds.py', 7)]:
        path = ROOT/f'results/{name}/status.json'
        report = read_json(path)
        check(f'{name}_complete', report['state'] == 'complete' and len(report['checks']) == count and all(row['passed'] for row in report['checks']))
        check(f'{name}_script_hash', report['script_sha256'] == digest(ROOT/script))
        inputs[str(path)] = digest(path)
    coarse = read_json(ROOT/'results/coarse/status.json')
    fine = read_json(ROOT/'results/fine/status.json')
    for label, report in [('coarse', coarse), ('fine', fine)]:
        check(f'{label}_complete', report['state'] == 'complete')
        check(f'{label}_script_hash', report['script_sha256'] == digest(ROOT/'run_response.py'))
        check(f'{label}_system_hash', report['system_sha256'] == digest(ROOT/'axial_wave.py'))
        for source, expected in report['input_hashes'].items():
            check(f'{label}_input_{Path(source).name}', Path(source).is_file() and digest(source) == expected)
        csv_path = ROOT/f'results/{label}/response.csv'
        with csv_path.open(encoding='utf-8', newline='') as handle:
            reader = csv.DictReader(handle)
            fields = reader.fieldnames
            rows = list(reader)
        check(f'{label}_csv_shape', len(rows) == 8 and len(fields) == len(set(fields)) and all(None not in row and all(value is not None for value in row.values()) for row in rows))
        check(f'{label}_csv_finite', all(math.isfinite(float(value)) for row in rows for key, value in row.items() if key != 'label' and value != ''))
        check(f'{label}_csv_hash', digest(csv_path) == report['csv_sha256'])
        inputs[str(csv_path)] = digest(csv_path)
        inputs[str(ROOT/f'results/{label}/status.json')] = digest(ROOT/f'results/{label}/status.json')
    for row in fine['static_rows']:
        check(f'static_recovery_C{row["nominal"]}', row['response_relative_error'] < 2e-9, difference=row['response_relative_error'])
        check(f'norm_variational_identity_C{row["nominal"]}', row['integral_variational_identity_error'] < 2e-12,
              absolute_error=row['integral_variational_identity_error'])
    flat = fine['static_rows'][0]
    check('flat_norm_one_seventh', abs(flat['I_over_R']-1/7) < 1e-13)
    check('flat_quartic_minus_one_over_441', abs(flat['Y_frequency_fourth_coefficient']+1/441) < 1e-13)
    background = fine['background']
    check('positive_background_and_pressure', background['minimum_sampled_F'] > 0 and background['minimum_sampled_lapse'] >= background['central_lapse']-1e-10 and background['minimum_sampled_pr'] > -1e-12)
    check('potential_exceeds_analytic_floor', background['minimum_sampled_dimensionless_V'] >= background['dimensionless_Dirichlet_spectral_floor'])
    resolution_rows = []
    roundoff_rows = []
    for rough, precise in zip(coarse['rows'], fine['rows']):
        assert rough['label'] == precise['label']
        label = precise['label']
        error = max(abs(rough[key]-precise[key]) for key in ['Y', 'Y_out_real', 'Y_out_imag', 'Y_BH_real', 'Y_BH_imag'])
        contrast_error = abs(rough['body_minus_BH_kernel_ratio_to_static_real']-precise['body_minus_BH_kernel_ratio_to_static_real'])
        check(f'coarse_fine_{label}', error < 2e-9 and contrast_error < 2e-8, maximum_impedance_error=error, contrast_ratio_error=contrast_error)
        allowance = max(1e-13, 10*abs(rough['Y']-precise['Y']))
        check(f'resolvent_remainder_{label}', -allowance <= precise['signed_remainder'] <= precise['quadratic_remainder_bound']+allowance,
              signed_remainder=precise['signed_remainder'], analytic_bound=precise['quadratic_remainder_bound'], floating_point_allowance=allowance)
        kernel_allowance = allowance/precise['retarded_denominator_abs']**2+2e-15
        check(f'kernel_error_transfer_{label}', precise['quadratic_kernel_absolute_error'] <= precise['quadratic_kernel_absolute_error_bound']+kernel_allowance,
              numeric_absolute_error=precise['quadratic_kernel_absolute_error'], analytic_bound=precise['quadratic_kernel_absolute_error_bound'], floating_point_allowance=kernel_allowance)
        check(f'causal_and_gap_signs_{label}', precise['Y_out_imag'] > 0 and precise['Y_BH_imag'] < 0
              and precise['surface_kernel_imag'] > 0 and 0 < precise['spectral_frequency_ratio'] < 1)
        resolution_rows.append({'label': label, 'maximum_impedance_difference': error, 'contrast_ratio_difference': contrast_error})
        if precise['quadratic_remainder_bound'] < allowance:
            roundoff_rows.append(label)
    for row in fine['flat_controls']:
        check(f'flat_analytic_wave_k{row["frequency_R"]}', max(row['interior_error'], row['outgoing_error'], row['full_kernel_error']) < 1e-10)
        check(f'reject_frozen_total_flat_impedance_k{row["frequency_R"]}', row['spurious_contrast_when_freezing_full_Y'] > 1e4*max(row['full_kernel_error'], 1e-16))
    orbital = [row for row in fine['rows'] if row['label'].startswith('orbital_')]
    check('orbital_denominators_nonresonant_at_samples', min(row['retarded_denominator_abs'] for row in orbital) > 4.8)
    check('orbital_frequencies_below_interior_gap', max(row['spectral_frequency_ratio'] for row in orbital) < 1e-4)
    check('higher_frequency_control_does_not_force_static_agreement', fine['rows'][-1]['body_minus_BH_kernel_ratio_to_static_real'] > 1.3)
    source_path = ROOT/'sources/provenance.json'
    source = read_json(source_path)
    check('source_pdf_hash', Path(source['path']).is_file() and digest(source['path']) == source['sha256'])
    check('source_acquisition_hash', digest(ROOT/'acquire_source.py') == source['script_sha256'])
    check('source_render_exists', all(Path(path).is_file() and Path(path).read_bytes().startswith(b'\x89PNG\r\n\x1a\n') for path in source['selected_page_renders']))
    inputs[str(source_path)] = digest(source_path)
    prose = '\n'.join(path.read_text(encoding='utf-8') for path in ROOT.glob('*.md'))
    deferred = {'results/validation/status.json', 'results/stage-integrity.json'}
    paths = set(re.findall(r'`([^`\n]+\.(?:py|csv|json|md|pdf))`', prose))-deferred
    for relative in sorted(paths):
        path = (ROOT/relative).resolve()
        check(f'cited_path_{relative}', path.is_file())
        inputs[str(path)] = digest(path)
    check('primary_urls_recorded', all(url in prose for url in [source['landing_url'], 'https://doi.org/'+source['doi']]))
    compiled = []
    for path in ROOT.glob('*.py'):
        compile(path.read_bytes(), str(path), 'exec')
        compiled.append(path.name)
    check('no_python_cache', not list(ROOT.rglob('__pycache__')))
    report = {'state': 'complete', 'script_sha256': digest(__file__), 'completed_at_utc': datetime.now(timezone.utc).isoformat(),
              'checks': checks, 'input_hashes': inputs, 'compiled_scripts': sorted(compiled), 'exact_checks': 38,
              'resolution_rows': resolution_rows, 'roundoff_limited_remainder_rows': roundoff_rows,
              'roundoff_policy': 'Reported analytic bounds remain unchanged. Numerical residual checks allow explicit resolution/subtraction noise; not interval certification.',
              'source_urls': [source['url'], source['landing_url'], 'https://doi.org/'+source['doi']],
              'body_coefficient_fits': 0, 'new_background_solves': 0, 'kernel_not_relabelled_dynamic_Love': True}
    destination = ROOT/'results/validation/status.json'
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open('x', encoding='utf-8') as handle:
        json.dump(report, handle, indent=2, allow_nan=False)
    print(json.dumps({'state': 'complete', 'checks': len(checks), 'exact_checks': 38,
                      'maximum_impedance_resolution_difference': max(row['maximum_impedance_difference'] for row in resolution_rows),
                      'roundoff_limited_rows': roundoff_rows}))


if __name__ == '__main__':
    main()
