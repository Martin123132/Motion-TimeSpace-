from __future__ import annotations

import csv
from datetime import datetime, timezone
import json
import math
import re
from pathlib import Path

import sympy as sp

from common import BRANCH, ROOT, configure_worker, digest, read_json, write_new_json


def main():
    configure_worker()
    checks = []

    def check(name, passed, **details):
        checks.append({'name': name, 'passed': bool(passed), **details})
        assert passed, (name, details)

    constituents = [('derivation', 'derive_magnetic_moments.py', 51),
                    ('combined', 'combined_balance.py', 83),
                    ('evaluation', 'evaluate_balance.py', 58)]
    input_hashes = {}
    for label, script, count in constituents:
        path = ROOT/f'results/{label}/status.json'
        report = read_json(path)
        check(f'{label}_checks_pass', report['state'] == 'complete' and len(report['checks']) == count
              and all(row['passed'] for row in report['checks']), check_count=len(report['checks']))
        check(f'{label}_script_unchanged', report['script_sha256'] == digest(ROOT/script))
        check(f'{label}_common_unchanged', report['common_sha256'] == digest(ROOT/'common.py'))
        for source, expected in report.get('input_hashes', {}).items():
            check(f'{label}_input_{Path(source).name}', Path(source).is_file() and digest(source) == expected)
        input_hashes[str(path)] = digest(path)
    derivation = read_json(ROOT/'results/derivation/status.json')
    combined = read_json(ROOT/'results/combined/status.json')
    evaluation = read_json(ROOT/'results/evaluation/status.json')
    provenance_path = ROOT/'sources/provenance.json'
    provenance = read_json(provenance_path)
    check('source_provenance_bound_to_derivation', digest(provenance_path) == derivation['source_provenance_sha256'])
    check('source_extractor_unchanged', provenance['script_sha256'] == digest(ROOT/'read_sources.py'))
    for index, source in enumerate(provenance['sources']):
        check(f'source_pdf_{index}', Path(source['path']).is_file() and digest(source['path']) == source['sha256'])
        check(f'source_url_{index}', source['url'].startswith('https://arxiv.org/pdf/'))
        for render in source['selected_page_renders']:
            check(f'source_render_{Path(render).name}', Path(render).is_file() and Path(render).read_bytes().startswith(b'\x89PNG\r\n\x1a\n'))
    csv_counts = {}
    for filename, expected_count in [('predictions', 20), ('phase-bands', 10), ('independent-controls', 12)]:
        relative = f'results/{filename}.csv'
        path = ROOT/relative
        with path.open(encoding='utf-8', newline='') as handle:
            reader = csv.DictReader(handle)
            fields = reader.fieldnames
            rows = list(reader)
        check(f'csv_{filename}_shape', len(rows) == expected_count and len(fields) == len(set(fields))
              and all(None not in row and all(value is not None for value in row.values()) for row in rows))
        check(f'csv_{filename}_finite', all(math.isfinite(float(value)) for row in rows for value in row.values()))
        check(f'csv_{filename}_digest', digest(path) == evaluation['csv_hashes'][relative])
        csv_counts[relative] = len(rows)
        input_hashes[str(path)] = digest(path)
    chi, epsilon = sp.symbols('chi epsilon')
    coefficient = {name: sp.sympify(value) for name, value in derivation['coefficients'].items()}
    for name, expected in [('flux', (113*epsilon-1)/3), ('chirp', (1037*epsilon-1)/3), ('energy', 22*epsilon)]:
        check(f'simple_mass_ratio_identity_{name}', sp.factor(coefficient[name].subs(chi, 1/(1+epsilon))-expected) == 0)
    check('negative_controls_present', combined['negative_control_count'] == 5
          and sum(row['name'].startswith('reject_') for row in combined['checks']) == 5)
    check('numerical_error_bound', max(row['max_absolute_error'] for row in evaluation['independent_controls']) < 1e-18)
    check('phase_quadrature_bound', max(row['quadrature_relative_error'] for row in evaluation['phase_bands']) < 2e-12)
    archived = ROOT/'failures/normalization-regression'
    check('failed_gate_preserved', all((archived/name).is_file() for name in ['evaluate_balance.py', 'predictions.csv', 'phase-bands.csv', 'independent-controls.csv', 'README.md']))
    with (archived/'predictions.csv').open(encoding='utf-8', newline='') as handle:
        old_predictions = list(csv.DictReader(handle))
    with (ROOT/'results/predictions.csv').open(encoding='utf-8', newline='') as handle:
        new_predictions = list(csv.DictReader(handle))
    check('normalization_fix_did_not_change_predictions', len(old_predictions) == len(new_predictions)
          and all(all(old[key] == new[key] for key in old) for old, new in zip(old_predictions, new_predictions)))
    compiled = []
    for path in sorted(ROOT.glob('*.py')):
        compile(path.read_bytes(), str(path), 'exec')
        compiled.append(path.name)
    check('scripts_compile_without_cache', not list(ROOT.rglob('__pycache__')), compiled_scripts=compiled)
    prose = '\n'.join(path.read_text(encoding='utf-8') for path in ROOT.glob('*.md'))
    required_paths = set(re.findall(r'`([^`\n]+\.(?:md|json|py|csv|pdf))`', prose))
    generated_later = {'results/validation/status.json', 'results/stage-integrity.json'}
    for relative in sorted(required_paths-generated_later):
        path = (ROOT/relative).resolve()
        check(f'documented_path_{relative}', path.is_file())
        input_hashes[str(path)] = digest(path)
    urls = ['https://arxiv.org/abs/1805.07266', 'https://doi.org/10.1103/PhysRevD.101.064003',
            'https://arxiv.org/abs/1101.1673']
    check('primary_urls_recorded', all(url in prose for url in urls))
    report = {'state': 'complete', 'script_sha256': digest(__file__), 'common_sha256': digest(ROOT/'common.py'),
              'completed_at_utc': datetime.now(timezone.utc).isoformat(), 'checks': checks,
              'constituent_check_counts': {label: count for label, script, count in constituents},
              'input_hashes': input_hashes, 'csv_counts': csv_counts, 'compiled_scripts': compiled,
              'primary_source_urls': urls, 'same_source_formula_checks_not_independent_evidence': True,
              'failed_normalization_gate_preserved': True, 'new_body_coefficient_fits': 0,
              'dynamical_axial_response_is_next_target': True}
    write_new_json(ROOT/'results/validation/status.json', report)
    print(json.dumps({'state': 'complete', 'validation_checks': len(checks), 'constituent_checks': report['constituent_check_counts'],
                      'csv_counts': csv_counts, 'scripts_compiled': len(compiled)}))


if __name__ == '__main__':
    main()
