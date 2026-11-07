from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re

import numpy as np
import psutil
from scipy.interpolate import PPoly


ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
POST = BRANCH.parent
OUTPUT = ROOT/'results/stage-integrity.json'


def digest(path):
    hasher = hashlib.sha256()
    with path.open('rb') as handle:
        for block in iter(lambda: handle.read(1024*1024), b''):
            hasher.update(block)
    return hasher.hexdigest()


def strict_json(path):
    def unique(pairs):
        result = {}
        for key, value in pairs:
            if key in result:
                raise ValueError(f'Duplicate key {key} in {path}')
            result[key] = value
        return result
    def reject(value):
        raise ValueError(f'Nonfinite JSON constant {value} in {path}')
    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=unique, parse_constant=reject)


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    assert not OUTPUT.exists()
    stages = ['finite-charge-20261003', 'conserved-stress-20261003', 'ward-remainder-20261003',
              'tensor-ward-20261003', 'collective-operator-20261003', 'tensor-response-20261003']
    paths = [BRANCH/stage/'results/stage-integrity.json' for stage in stages]+[BRANCH/'results/stage-integrity.json']
    bases = [BRANCH/stage for stage in stages]+[POST]
    keys = ['parent_seal_sha256', 'parent_seal_sha256', 'parent_seal_sha256', 'previous_seal_sha256', 'previous_seal_sha256', 'parent_seal_sha256']
    reports = []
    for path, base in zip(paths, bases):
        report = strict_json(path)
        assert report['state'] == 'complete'
        for relative, expected in report['file_hashes'].items():
            source = base/relative
            assert source.is_file() and digest(source) == expected, str(source)
        reports.append(report)
    for index, key in enumerate(keys):
        assert reports[index][key] == digest(paths[index+1])
    manifest = POST/'_checkpoints/20261003-pre-condensate-origin/manifest.json'
    assert digest(manifest) == reports[0]['checkpoint_manifest_sha256']
    source_documents = reports[0]['local_source_documents']
    for row in source_documents:
        assert Path(row['path']).is_file() and digest(Path(row['path'])) == row['sha256']

    derivation_path = ROOT/'results/derivation/status.json'
    derivation = strict_json(derivation_path)
    validation_path = ROOT/'results/validation/status.json'
    validation = strict_json(validation_path)
    assert derivation['state'] == validation['state'] == 'complete'
    assert derivation['exact_check_count'] == len(derivation['checks']) == 18
    assert all(row['passed'] for row in derivation['checks'])
    assert derivation['script_sha256'] == digest(ROOT/'derive_gravitating_body.py')
    assert derivation['parent_seal_sha256'] == digest(paths[0])
    assert validation['script_sha256'] == digest(ROOT/'validate_weak_gravity.py')
    for name, expected in validation['input_hashes'].items():
        assert digest(ROOT/name) == expected
    run_reports = {}
    for label, count in [('pilot', 4), ('coarse', 21), ('fine', 21), ('third-resolution', 2)]:
        report = strict_json(ROOT/f'results/{label}/status.json')
        assert report['state'] == 'complete' and len(report['rows']) == count
        assert report['script_sha256'] == digest(ROOT/'solve_self_gravity.py')
        assert report['parent_seal_sha256'] == digest(paths[0])
        assert report['derivation_sha256'] == digest(derivation_path)
        assert all(row['converged'] and row['minimum_F'] > .95 and row['min_amplitude_interior'] > 0 for row in report['rows'])
        assert all((ROOT/f'results/{label}'/row['archive']).is_file() for row in report['rows'])
        run_reports[label] = report
    fine = run_reports['fine']['rows']
    max_charge_error = max(row['charge_relative_error'] for row in fine)
    max_mass_error = max(row['mass_quadrature_relative_error'] for row in fine)
    max_komar_error = max(row['komar_adm_relative_error_without_tiny_tail'] for row in fine)
    max_scalar_error = max(row['scalar_collocation_relative_residual'] for row in fine)
    max_angular_error = max(row['angular_Einstein_relative_residual'] for row in fine)
    assert max_charge_error < 8.88e-14 and max_mass_error < 1.24e-13 and max_komar_error < 1.66e-13
    assert max_scalar_error < 4.56e-6 and max_angular_error < 6.49e-5
    assert len(validation['coarse_fine_comparisons']) == 21
    max_change = max(max(row['relative_observable_differences'].values()) for row in validation['coarse_fine_comparisons'])
    assert max_change < 3.43e-9
    assert len(validation['weak_binding_tests']) == 3
    max_binding_error = max(row['full_stress_prediction_relative_error'] for row in validation['weak_binding_tests'])
    assert max_binding_error < 5e-10
    for row in validation['weak_binding_tests']:
        assert row['density_only_Newton_relative_error'] > 100*row['full_stress_prediction_relative_error']
        assert all(item['full_stress_binding_coefficient'] < item['density_only_Newton_coefficient'] < 0
                   for item in row['independent_flat_quadratures'])
    assert len(validation['first_law_tests']) == 3
    first_law_branches = [branch for row in validation['first_law_tests'] for level in row['levels'] for branch in level['branches']]
    assert len(first_law_branches) == 12
    assert all((ROOT/'results/validation'/row['archive']).is_file() for row in first_law_branches)
    assert all(row['charge_error'] < 1e-10 and row['komar_error'] < 1e-10 for row in first_law_branches)
    max_first_law_error = max(row['levels'][-1]['relative_error'] for row in validation['first_law_tests'])
    assert max_first_law_error < 2.32e-9
    for row in validation['first_law_tests']:
        assert row['levels'][-1]['relative_error'] < row['levels'][0]['relative_error']/2
    third = validation['third_resolution_check']
    assert third['angular_relative_error_third'] < 1.03e-6
    assert third['angular_relative_error_third'] < third['angular_relative_error_fine']/20
    example = validation['largest_body_gravity_example']
    assert 0 < example['adm_energy_per_charge'] < 1
    assert 0 < example['radius_contraction_fraction'] < .02 and 0 < example['energy_reduction_fraction'] < .02
    assert example['frequency_infinity'] < 1 < example['frequency_center_proper']

    archives = []
    for path in sorted(ROOT.rglob('*.npz')):
        with np.load(path, allow_pickle=False) as archive:
            assert all(np.all(np.isfinite(archive[name])) for name in archive.files)
            coefficients, knots = archive['spline_coefficients'], archive['spline_knots']
            assert coefficients.shape == (4, len(knots)-1, 5) and np.all(np.diff(knots) > 0)
            assert np.all(archive['parameters'] > 0) and float(archive['alpha']) >= 0
            spline = PPoly.construct_fast(coefficients, knots, axis=1)
            assert spline(np.array([knots[0], .5, 1.])).shape == (5, 3)
            assert np.all(np.isfinite(spline(np.array([knots[0], .5, 1.]))))
        archives.append(path.relative_to(ROOT).as_posix())
    assert len(archives) == 60
    required = [ROOT/'10-self-gravity-and-weak-binding-law.md', ROOT/'RESULTS.md', ROOT/'RESUME.md',
                derivation_path, validation_path, manifest, *paths,
                *[Path(row['path']) for row in source_documents]]
    prose = '\n'.join(path.read_text(encoding='utf-8') for path in ROOT.glob('*.md'))
    for relative in set(re.findall(r'`([^`\n]+\.(?:md|json))`', prose)):
        path = (ROOT/relative).resolve()
        if path != OUTPUT.resolve():
            required.append(path)
    assert all(path.is_file() for path in required)
    urls = ['https://arxiv.org/abs/1202.5809', 'https://arxiv.org/abs/1310.3632']
    assert all(url in prose for url in urls)
    parsed, compiled = [], []
    for path in sorted(ROOT.rglob('*.json')):
        document = strict_json(path)
        if isinstance(document, dict) and 'state' in document:
            assert document['state'] == 'complete'
        parsed.append(path.relative_to(ROOT).as_posix())
    for path in sorted(ROOT.glob('*.py')):
        compile(path.read_bytes(), str(path), 'exec')
        compiled.append(path.name)
    assert not list(ROOT.rglob('__pycache__'))
    protected = POST.parent/'formalization-workbench'
    start = datetime(2026, 10, 3, 19, 39, 10, tzinfo=timezone.utc)
    assert protected.is_dir()
    changed = [str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime > start.timestamp()]
    assert not changed, changed
    hashes = {path.relative_to(ROOT).as_posix(): digest(path) for path in sorted(ROOT.rglob('*'))
              if path.is_file() and path != OUTPUT}
    report = {'state': 'complete', 'sealed_at': datetime.now(timezone.utc).isoformat(), 'file_hashes': hashes,
              'parent_seal_sha256': digest(paths[0]), 'prior_sealed_entries_unchanged': sum(len(row['file_hashes']) for row in reports),
              'checkpoint_manifest_sha256': digest(manifest), 'full_checkpoint_payload_rehashed': False,
              'exact_check_count': 18, 'coarse_fine_profiles': 42, 'nearby_charge_profiles': 12,
              'pilot_profiles': 4, 'third_resolution_profiles': 2, 'total_archives_reconstructed': len(archives),
              'max_coarse_fine_observable_change': max_change, 'max_fine_charge_error': max_charge_error,
              'max_fine_mass_quadrature_error': max_mass_error, 'max_fine_Komar_ADM_error': max_komar_error,
              'max_fine_scalar_relative_residual': max_scalar_error, 'max_fine_angular_relative_residual': max_angular_error,
              'worst_angular_case_third_resolution_residual': third['angular_relative_error_third'],
              'max_weak_binding_prediction_relative_error': max_binding_error,
              'max_mass_charge_first_law_relative_error': max_first_law_error,
              'protected_workbench_recent_modified_file_count': len(changed),
              'protected_check_scope': 'Modification-time scan since 19:39:10 UTC; not a full content-hash baseline.',
              'required_paths': sorted(set(str(path.resolve()) for path in required)), 'local_source_documents': source_documents,
              'primary_source_urls_checked_2026_10_03': urls, 'parsed_json_files': parsed, 'compiled_scripts': compiled,
              'self_gravitating_stationary_solutions_numerically_supported': True,
              'fixed_charge_weak_binding_coefficient_derived': True,
              'gravitational_dynamical_stability_proved': False,
              'Einstein_sector_retained_not_derived_from_acoustic_metric': True,
              'Newton_constant_or_physical_condensate_scale_derived': False,
              'original_parent_or_bath_modified': False, 'github_action': False, 'subagents': 0,
              'largest_example': example}
    OUTPUT.write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
    print(json.dumps({'state': 'complete', 'sealed_files': len(hashes), 'prior_unchanged': report['prior_sealed_entries_unchanged'],
                      'profiles_verified': len(archives), 'exact_checks': 18, 'protected_changes': len(changed),
                      'binding_prediction_error': max_binding_error, 'first_law_error': max_first_law_error}))


if __name__ == '__main__':
    main()
