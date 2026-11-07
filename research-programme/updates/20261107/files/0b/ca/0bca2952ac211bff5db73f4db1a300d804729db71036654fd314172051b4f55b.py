from __future__ import annotations

import csv
import json
from pathlib import Path
import re

import numpy as np

from eccentric_source import ROOT, BRANCH, digest, modest_process, write_report


def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8'),
                      parse_constant=lambda value: (_ for _ in ()).throw(ValueError(value)))


def main():
    modest_process()
    checks, inputs, reports, kernel_rows = [], {}, {}, {}

    def check(name, passed, **details):
        checks.append({'name': name, 'passed': bool(passed), **details})
        assert passed, (name, details)

    def remember(path):
        inputs[str(Path(path).resolve())] = digest(path)

    for label, script in [('derivation', 'derive_eccentric.py'), ('coarse', 'run_source.py'), ('fine', 'run_source.py')]:
        path = ROOT/f'results/{label}/status.json'
        report = read_json(path)
        reports[label] = report
        check(f'{label}_complete', report['state'] == 'complete')
        check(f'{label}_script_hash', report['script_sha256'] == digest(ROOT/script))
        check(f'{label}_checks_pass', all(row['passed'] for row in report['checks']))
        for source, expected in report['input_hashes'].items():
            check(f'{label}_input_{source}', Path(source).is_file() and digest(source) == expected)
            remember(source)
        remember(path)
        if label == 'derivation':
            check('37_exact_checks', report['exact_checks'] == len(report['checks']) == 37)
            continue
        check(f'{label}_scope', report['new_background_solves'] == report['new_fitted_parameters'] == 0
              and not report['orbital_radiation_reaction_derived']
              and report['radial_probes_are_not_finite_frequency_wave_solutions'])
        check(f'{label}_three_orbits', [row['eccentricity'] for row in report['orbits']] == [0., .3, .6])
        for saved in report['files']:
            path = Path(saved['path'])
            check(f'{label}_{path.name}_hash', path.is_file() and digest(path) == saved['sha256'])
            remember(path)
            if path.suffix != '.npz':
                continue
            with np.load(path, allow_pickle=False) as archive:
                data = {key: archive[key] for key in archive.files}
            check(f'{label}_{path.name}_finite', all(np.isfinite(value).all() for value in data.values()))
            check(f'{label}_{path.name}_time_order', np.all(np.diff(data['time']) > 0)
                  and np.all(np.diff(data['proper_time']) > 0))
            check(f'{label}_{path.name}_shapes', all(value.shape == (report['settings']['samples'],)
                  for key, value in data.items() if key != 'independent_geodesic')
                  and data['independent_geodesic'].shape == (4, report['settings']['samples']))
            scale = np.max(np.abs(data['strength']))
            margin = 1-data['tortoise_velocity']**2
            replay = margin*data['derivative_jump']+2*data['tortoise_velocity']*data['jump_dot']+data['tortoise_acceleration']*data['jump']-data['delta']
            check(f'{label}_{path.name}_saved_jump_replay', np.max(np.abs(replay))/scale < 2e-13)
            phase_removed = data['strength']*data['radius']**2*np.exp(1j*data['phase'])
            check(f'{label}_{path.name}_constant_angular_momentum_source',
                  np.max(np.abs(phase_removed/phase_removed[0]-1)) < 2e-14)
        with (ROOT/f'results/{label}/kernels.csv').open(encoding='utf-8', newline='') as handle:
            rows = list(csv.DictReader(handle))
        check(f'{label}_csv_42_rows', len(rows) == 42 and all(None not in row and None not in row.values() for row in rows))
        check(f'{label}_csv_no_flux_claim', all(row['physical_wave_amplitude'] == 'False' for row in rows))
        check(f'{label}_csv_finite', all(np.isfinite(float(row[key])) for row in rows for key in
              ['eccentricity', 'frequency', 'raw_real', 'raw_imag', 'weak_real', 'weak_imag', 'scale', 'weak_identity_error']))
        kernel_rows[label] = rows
    refinement_rows = []
    for coarse, fine in zip(kernel_rows['coarse'], kernel_rows['fine']):
        keys = ['eccentricity', 'probe', 'radial_harmonic']
        check(f'kernel_order_{len(refinement_rows)}', all(coarse[key] == fine[key] for key in keys))
        first = complex(float(coarse['weak_real']), float(coarse['weak_imag']))
        second = complex(float(fine['weak_real']), float(fine['weak_imag']))
        scaled = abs(second-first)/float(fine['scale'])
        check(f'kernel_refinement_{len(refinement_rows)}', scaled < 2e-10, scaled_error=scaled)
        refinement_rows.append({**{key: fine[key] for key in keys}, 'scaled_change': scaled})
    improved = reports['fine']['orbits'][-1]['geodesic_comparison_maximum_scaled_error']
    coarse_error = reports['coarse']['orbits'][-1]['geodesic_comparison_maximum_scaled_error']
    check('eccentric_independent_geodesic_refines', improved < coarse_error and improved < 2e-10,
          coarse_error=coarse_error, fine_error=improved)
    for label in ['coarse', 'fine']:
        accepted = reports[label]['checks']
        for fragment, expected in [('circular_jump_shortcut_rejected', 2), ('omitted_Pr_rejected', 2),
                                   ('windowed_source_not_conserved', 2), ('endpoint_omission_rejected', 4)]:
            selected = [row for row in accepted if fragment in row['name']]
            check(f'{label}_{fragment}_present', len(selected) == expected and all(row['passed'] for row in selected))
    notes = ROOT/'results/attempt1-endpoint-gate/ATTEMPT.md'
    check('rejected_attempt_preserved', notes.is_file() and (notes.parent/'run_source_v1.py').is_file()
          and (notes.parent/'e0p0.npz').is_file() and not (notes.parent/'status.json').exists())
    remember(notes)
    compiled = []
    for path in ROOT.glob('*.py'):
        compile(path.read_bytes(), str(path), 'exec')
        compiled.append(path.name)
        remember(path)
    documents = [ROOT/'30-conserved-eccentric-source-and-moving-jumps.md', ROOT/'RESULTS.md', ROOT/'RESUME.md']
    cited = 0
    for path in documents:
        check(f'document_{path.name}_exists', path.is_file())
        remember(path)
        for relative in re.findall(r'`((?:\.\./|results/)[^`]+)`', path.read_text(encoding='utf-8')):
            if relative == 'results/validation/status.json':
                check('validation_self_reference_reserved_for_this_run', not (ROOT/relative).exists())
            else:
                check(f'local_citation_{relative}', (ROOT/relative).exists())
            cited += 1
    check('local_source_paths_cited', cited >= 5)
    check('primary_source_url_in_document', 'https://arxiv.org/abs/gr-qc/0502028' in documents[0].read_text(encoding='utf-8'))
    check('no_cache', not list(ROOT.rglob('__pycache__')))
    output = ROOT/'results/validation'
    output.mkdir(parents=True, exist_ok=True)
    with (output/'kernel-refinement.csv').open('x', encoding='utf-8', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(refinement_rows[0]))
        writer.writeheader()
        writer.writerows(refinement_rows)
    remember(output/'kernel-refinement.csv')
    largest_weak_error = max(float(row['weak_identity_error']) for row in kernel_rows['fine'])
    result = {'checks': checks, 'exact_checks': reports['derivation']['exact_checks'],
              'accepted_run_checks': sum(len(reports[label]['checks']) for label in ['coarse', 'fine']),
              'input_hashes': inputs, 'compiled_scripts': compiled,
              'maximum_scaled_kernel_refinement': max(row['scaled_change'] for row in refinement_rows),
              'maximum_fine_scaled_weak_source_identity_error': largest_weak_error,
              'maximum_fine_independent_geodesic_scaled_error': max(row['geodesic_comparison_maximum_scaled_error'] for row in reports['fine']['orbits']),
              'source_urls': ['https://arxiv.org/abs/gr-qc/0502028', 'https://arxiv.org/pdf/gr-qc/0502028',
                              'https://doi.org/10.1103/PhysRevD.71.104003'],
              'web_source_verified_utc_date': '2026-10-05', 'cached_source_read_only': True,
              'complete_conserved_test_geodesic_source_derived': True,
              'eccentric_radiation_flux_or_self_force_computed': False}
    write_report(output, __file__, result)
    assert (output/'status.json').is_file()
    print(json.dumps({key: value for key, value in result.items() if key not in
                      ['checks', 'input_hashes', 'compiled_scripts', 'source_urls']} | {'validation_checks': len(checks)}))


if __name__ == '__main__':
    main()
