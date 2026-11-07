from __future__ import annotations

from pathlib import Path
import csv
import math

from polar_source import ROOT, BRANCH, digest, modest_process, read_json, save_report


def main():
    modest_process()
    checks = []
    def check(name, passed, value=None, tolerance=None):
        checks.append({'name': name, 'passed': bool(passed), 'value': value, 'tolerance': tolerance})

    derivation_path = ROOT/'results/derivation/status.json'
    coarse_path, fine_path = ROOT/'results/coarse/status.json', ROOT/'results/fine/status.json'
    derivation, coarse, fine = map(read_json, [derivation_path, coarse_path, fine_path])
    check('all18 exact identities', len(derivation['checks']) == 18 and all(row['passed'] for row in derivation['checks']))
    check('authoritative symbolic implementation', derivation['script_sha256'] == digest(ROOT/'derive_polar_v4.py'))
    for label, report in [('coarse', coarse), ('fine', fine)]:
        check(f'source mode count {label}', len(report['rows']) == 36)
        check(f'completed {label}', report['state'] == 'complete' and (ROOT/f'results/{label}/COMPLETE').is_file())
        check(f'runner provenance {label}', report['script_sha256'] == digest(ROOT/'check_source.py'))
        for path, expected in report['input_hashes'].items():
            check(f'input {label}:{Path(path).name}', Path(path).is_file() and digest(path) == expected)
        for index, row in enumerate(report['rows']):
            check(f'jump reconstruction {label}:{index}', row['jump_delta_error'] < 2e-12, row['jump_delta_error'], 2e-12)
            for interval in ['full', 'partial']:
                for item in row[interval]:
                    for key in ['metric_reciprocity_error', 'Martel_integral_error', 'reality_error']:
                        check(f'{label}:{index}:{interval}:{item["basis"]}:{key}', item[key] < 2e-10, item[key], 2e-10)
                    if interval == 'full':
                        check(f'period boundary cancellation {label}:{index}:{item["basis"]}',
                              item['endpoint_over_scale'] < 2e-10, item['endpoint_over_scale'], 2e-10)
                        check(f'half orbit symmetry {label}:{index}:{item["basis"]}',
                              item['half_orbit_symmetry_error'] < 2e-10, item['half_orbit_symmetry_error'], 2e-10)
                        if row['eccentricity'] == 0 and row['harmonic'] != 0:
                            error = abs(complex(item['overlap_real'], item['overlap_imag']))/item['source_absolute_scale']
                            check(f'circular noncarrier vanishes {label}:{index}:{item["basis"]}', error < 2e-10, error, 2e-10)
            if row['eccentricity'] > 0 and row['azimuth'] == 0 and row['harmonic'] == 1:
                item = row['full'][0]
                ratio = abs(complex(item['overlap_real'], item['overlap_imag']))/item['source_absolute_scale']
                check(f'eccentric m0 nonstatic source present {label}:{index}', ratio > 1e-4, ratio, 1e-4)
        for row in report['finite_derivatives']:
            for key, value in row.items():
                if key != 'eccentricity':
                    check(f'finite derivative {label}:{row["eccentricity"]}:{key}', value < 2e-9, value, 2e-9)
    refinements = []
    for coarse_row, fine_row in zip(coarse['rows'], fine['rows']):
        labels = ['eccentricity', 'azimuth', 'harmonic']
        check(f'matched refinement row {len(refinements)}', all(coarse_row[key] == fine_row[key] for key in labels))
        for interval in ['full', 'partial']:
            for first, second in zip(coarse_row[interval], fine_row[interval]):
                first_overlap, second_overlap = (complex(item['overlap_real'], item['overlap_imag']) for item in [first, second])
                error = abs(second_overlap-first_overlap)/max(first['source_absolute_scale'], second['source_absolute_scale'])
                refinements.append(error)
                check(f'source refinement {len(refinements)}', error < 2e-9, error, 2e-9)
    boundaries = [item['endpoint_over_scale'] for row in fine['rows'] for item in row['partial']]
    check('partial boundary is detectably nonzero', max(boundaries) > .01, max(boundaries), .01)
    provenance_path = BRANCH/'companion-source-20261004/sources/provenance.json'
    provenance = read_json(provenance_path)
    for source in provenance['sources']:
        check('archived primary '+Path(source['path']).name, Path(source['path']).is_file() and digest(source['path']) == source['sha256'])
    source_urls = ['https://arxiv.org/abs/gr-qc/0502028', 'https://arxiv.org/pdf/gr-qc/0502028',
                  'https://doi.org/10.1103/PhysRevD.71.104003', 'https://arxiv.org/abs/gr-qc/0311017',
                  'https://arxiv.org/pdf/gr-qc/0311017', 'https://doi.org/10.1103/PhysRevD.69.044025']
    check('source URLs recorded', all(url in (ROOT/'SOURCES.md').read_text(encoding='utf-8') for url in source_urls))
    check('no bytecode directories', not list(ROOT.rglob('__pycache__')))
    output_rows = []
    for row in fine['rows']:
        for item in row['full']:
            output_rows.append({key: row[key] for key in ['eccentricity', 'azimuth', 'harmonic', 'frequency']} | item)
    csv_path = ROOT/'source-functional-checks.csv'
    with csv_path.open('x', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(output_rows[0]))
        writer.writeheader()
        writer.writerows(output_rows)
    with csv_path.open(encoding='utf-8', newline='') as handle:
        parsed = list(csv.DictReader(handle))
    check('CSV rectangular72rows', len(parsed) == 72 and all(None not in row for row in parsed))
    inputs = [derivation_path, coarse_path, fine_path, ROOT/'polar_source.py', ROOT/'SOURCES.md', provenance_path, csv_path]
    maximum_full = max(item['metric_reciprocity_error'] for row in fine['rows'] for item in row['full'])
    maximum_partial = max(item['metric_reciprocity_error'] for row in fine['rows'] for item in row['partial'])
    maximum_finite = max(value for row in fine['finite_derivatives'] for key, value in row.items() if key != 'eccentricity')
    report = save_report(ROOT/'results/validation', __file__, {'checks': checks, 'exact_checks': 18,
                'input_hashes': {str(path): digest(path) for path in inputs}, 'source_urls': source_urls,
                'primary_pdfs': provenance['sources'], 'maximum_source_refinement': max(refinements),
                'maximum_full_reciprocity_error': maximum_full, 'maximum_partial_reciprocity_error': maximum_partial,
                'maximum_partial_boundary_over_scale': max(boundaries), 'maximum_finite_derivative_error': maximum_finite,
                'checks_are_correlated_implementation_tests': True, 'new_physical_fluxes': 0})
    failed = [row for row in checks if not row['passed']]
    print({'checks': len(checks), 'failed': failed, 'max_refinement': max(refinements),
           'max_full_reciprocity': maximum_full, 'max_partial_reciprocity': maximum_partial,
           'max_partial_boundary': max(boundaries), 'max_finite_derivative_error': maximum_finite})
    assert not failed, failed


if __name__ == '__main__':
    main()
