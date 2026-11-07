from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re

import numpy as np
import psutil


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
            assert key not in result, (path, key)
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
    stages = ['self-gravity-20261003', 'finite-charge-20261003', 'conserved-stress-20261003',
              'ward-remainder-20261003', 'tensor-ward-20261003', 'collective-operator-20261003',
              'tensor-response-20261003']
    paths = [BRANCH/stage/'results/stage-integrity.json' for stage in stages]+[BRANCH/'results/stage-integrity.json']
    bases = [BRANCH/stage for stage in stages]+[POST]
    keys = ['parent_seal_sha256', 'parent_seal_sha256', 'parent_seal_sha256', 'parent_seal_sha256',
            'previous_seal_sha256', 'previous_seal_sha256', 'parent_seal_sha256']
    previous = []
    for path, base in zip(paths, bases):
        report = strict_json(path)
        assert report['state'] == 'complete'
        for relative, expected in report['file_hashes'].items():
            source = base/relative
            assert source.is_file() and digest(source) == expected, source
        previous.append(report)
    for index, key in enumerate(keys):
        assert previous[index][key] == digest(paths[index+1])
    manifest = POST/'_checkpoints/20261003-pre-condensate-origin/manifest.json'
    assert digest(manifest) == previous[0]['checkpoint_manifest_sha256']
    source_documents = previous[0]['local_source_documents']
    for row in source_documents:
        assert Path(row['path']).is_file() and digest(Path(row['path'])) == row['sha256']
    derivation_path = ROOT/'results/derivation/status.json'
    derivation = strict_json(derivation_path)
    assert derivation['state'] == 'complete' and derivation['exact_check_count'] == 18
    assert len(derivation['checks']) == 18 and all(row['passed'] for row in derivation['checks'])
    assert derivation['script_sha256'] == digest(ROOT/'derive_radial_hamiltonian.py')
    assert derivation['parent_seal_sha256'] == digest(paths[0])
    spectral_rows = []
    for label, count in [('pilot', 6), ('convergence', 27), ('large-body-refinement', 3), ('quadrature', 9)]:
        report = strict_json(ROOT/f'results/{label}/status.json')
        assert report['state'] == 'complete' and len(report['rows']) == count
        assert report['script_sha256'] == digest(ROOT/'test_radial_energy.py')
        assert report['parent_seal_sha256'] == digest(paths[0])
        assert report['derivation_sha256'] == digest(derivation_path)
        for row in report['rows']:
            assert Path(row['profile_path']).is_file() and digest(Path(row['profile_path'])) == row['profile_sha256']
            assert row['lowest_fixed_charge_energy_eigenvalues'][0] > 0 and row['momentum_block_minimum'] > .8
            assert (ROOT/f'results/{label}'/row['archive']).is_file()
        spectral_rows.extend(report['rows'])
    validation_path = ROOT/'results/validation-v2/status.json'
    validation = strict_json(validation_path)
    assert validation['state'] == 'complete'
    assert validation['script_sha256'] == digest(ROOT/'validate_radial_energy_v2.py')
    for source, expected in validation['input_hashes'].items():
        assert digest(Path(source)) == expected
    assert validation['spectral_runs'] == 45 and validation['fixed_charge_cases'] == 9
    assert validation['finite_steps'] == 72 and validation['adaptive_ODE_checks'] == 6
    assert len(validation['comparisons']) == len(validation['finest_spectra']) == 9
    assert len(validation['finite_variations']) == 18
    max_mesh_change = max(row['last_relative_mesh_change'] for row in validation['comparisons'])
    max_quadrature_change = max(row['quadrature_relative_difference'] for row in validation['comparisons'])
    max_routhian_error = max(row['steps'][-1]['Routhian_relative_error'] for row in validation['finite_variations'])
    max_fixed_error = max(row['steps'][-1]['fixed_charge_relative_error'] for row in validation['finite_variations'])
    max_ode_error = max(row['independent_adaptive_mass_ODE']['relative_difference'] for row in validation['finite_variations'] if row['independent_adaptive_mass_ODE'])
    assert max_mesh_change < .00313 and max_quadrature_change < 9.1e-12
    assert max_routhian_error < 1.83e-7 and max_fixed_error < 1.90e-6 and max_ode_error < 4.06e-13
    assert all(row['charge_tangent_relative_error'] < 1e-12 for row in spectral_rows)
    assert all(row['schur_rayleigh_relative_error'] < 1e-7 for row in spectral_rows)
    assert all(row['lapse_constraint_max_absolute_error'] < 1e-9 for row in spectral_rows)
    assert all(row['mass_constraint_max_relative_error'] < 1e-9 for row in spectral_rows)
    attempt_path = ROOT/'results/validation/finite-progress.json'
    attempt = strict_json(attempt_path)
    assert len(attempt['rows']) == 6 and attempt['state'] == 'running'
    assert validation['previous_attempt']['sha256'] == digest(attempt_path)
    assert 'AssertionError' in (ROOT/'results/validation-console.txt').read_text(encoding='utf-8-sig')
    archives = []
    for path in sorted(ROOT.rglob('*.npz')):
        with np.load(path, allow_pickle=False) as archive:
            assert all(np.all(np.isfinite(archive[name])) for name in archive.files)
            assert np.all(archive['lowest_eigenvalues'] > 0)
            assert np.all(np.diff(archive['nodal_position']) > 0)
            assert archive['amplitude_mode'].shape == archive['momentum_mode'].shape == archive['nodal_position'].shape
            assert archive['amplitude_mode'][0] == archive['amplitude_mode'][-1] == 0
        archives.append(path.relative_to(ROOT).as_posix())
    assert len(archives) == 45
    prose = '\n'.join(path.read_text(encoding='utf-8') for path in ROOT.glob('*.md'))
    required = [manifest, *paths, derivation_path, validation_path, *[Path(row['path']) for row in source_documents]]
    for relative in set(re.findall(r'`([^`\n]+\.(?:md|json|py))`', prose)):
        path = (ROOT/relative).resolve()
        if path != OUTPUT.resolve():
            required.append(path)
    assert all(path.is_file() for path in required), [str(path) for path in required if not path.is_file()]
    urls = ['https://arxiv.org/abs/1202.5809', 'https://arxiv.org/abs/2103.15012', 'https://doi.org/10.1088/1361-6382/ac0160']
    assert all(url in prose for url in urls)
    parsed, compiled = [], []
    for path in sorted(ROOT.rglob('*.json')):
        report = strict_json(path)
        if path != attempt_path and isinstance(report, dict) and 'state' in report:
            assert report['state'] == 'complete', (path, report['state'])
        parsed.append(path.relative_to(ROOT).as_posix())
    for path in sorted(ROOT.glob('*.py')):
        compile(path.read_bytes(), str(path), 'exec')
        compiled.append(path.name)
    assert not list(ROOT.rglob('__pycache__'))
    protected = POST.parent/'formalization-workbench'
    start = datetime(2026, 10, 3, 20, 9, 46, tzinfo=timezone.utc)
    changed = [str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime > start.timestamp()]
    assert not changed, changed
    hashes = {path.relative_to(ROOT).as_posix(): digest(path) for path in sorted(ROOT.rglob('*')) if path.is_file() and path != OUTPUT}
    report = {'state': 'complete', 'sealed_at': datetime.now(timezone.utc).isoformat(), 'file_hashes': hashes,
              'parent_seal_sha256': digest(paths[0]), 'prior_sealed_entries_unchanged': sum(len(row['file_hashes']) for row in previous),
              'checkpoint_manifest_sha256': digest(manifest), 'full_checkpoint_payload_rehashed': False,
              'local_source_documents': source_documents, 'required_paths': sorted(set(str(path.resolve()) for path in required)),
              'primary_source_urls_checked_2026_10_03': urls, 'parsed_json_files': parsed, 'compiled_scripts': compiled,
              'exact_check_count': 18, 'spectral_calculations': 45, 'physical_configurations': 9,
              'nonlinear_finite_directions': 18, 'finite_step_tests': 72, 'independent_adaptive_ODE_checks': 6,
              'maximum_last_mesh_relative_change': max_mesh_change, 'maximum_quadrature_relative_change': max_quadrature_change,
              'maximum_nonlinear_Routhian_hessian_relative_error': max_routhian_error,
              'maximum_fixed_charge_ADM_hessian_relative_error': max_fixed_error,
              'maximum_independent_mass_ODE_relative_error': max_ode_error,
              'incomplete_attempt_preserved': validation['previous_attempt'],
              'protected_workbench_recent_modified_file_count': len(changed),
              'protected_check_scope': 'Modification-time scan since 20:09:46 UTC; not a full content-hash baseline.',
              'coupled_radial_hamiltonian_and_constraint_response_derived': True,
              'positive_fixed_charge_radial_energy_numerically_supported': True,
              'phase_block_nonnegative_under_documented_domain_assumptions': True,
              'continuum_spectral_lower_bound_certified': False, 'nonlinear_or_nonspherical_stability_proved': False,
              'radial_oscillation_frequencies_computed': False, 'new_physical_parameter_fitted': False,
              'original_parent_or_bath_modified': False, 'github_action': False, 'subagents': 0,
              'one_below_normal_priority_single_core_worker_at_a_time': True}
    OUTPUT.write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
    print(json.dumps({'state': 'complete', 'sealed_files': len(hashes), 'prior_unchanged': report['prior_sealed_entries_unchanged'],
                      'exact_checks': 18, 'spectra': 45, 'finite_steps': 72, 'protected_changes': len(changed)}))


if __name__ == '__main__':
    main()
