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
        document = {}
        for key, value in pairs:
            assert key not in document, (path, key)
            document[key] = value
        return document

    def reject(value):
        raise ValueError(f'Nonfinite JSON constant {value} in {path}')

    return json.loads(path.read_text(encoding='utf-8'), object_pairs_hook=unique, parse_constant=reject)


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    assert not OUTPUT.exists()
    stages = ['radial-pulsations-20261003', 'radial-gravity-stability-20261003', 'self-gravity-20261003',
              'finite-charge-20261003', 'conserved-stress-20261003', 'ward-remainder-20261003',
              'tensor-ward-20261003', 'collective-operator-20261003', 'tensor-response-20261003']
    paths = [BRANCH/stage/'results/stage-integrity.json' for stage in stages]+[BRANCH/'results/stage-integrity.json']
    bases = [BRANCH/stage for stage in stages]+[POST]
    keys = ['parent_seal_sha256']*6+['previous_seal_sha256', 'previous_seal_sha256', 'parent_seal_sha256']
    previous = []
    for path, base in zip(paths, bases):
        report = strict_json(path)
        assert report['state'] == 'complete'
        for relative, expected in report['file_hashes'].items():
            assert digest(base/relative) == expected, base/relative
        previous.append(report)
    for index, key in enumerate(keys):
        assert previous[index][key] == digest(paths[index+1])
    manifest = POST/'_checkpoints/20261003-pre-condensate-origin/manifest.json'
    assert digest(manifest) == previous[0]['checkpoint_manifest_sha256']
    sources = previous[0]['local_source_documents']
    for row in sources:
        assert Path(row['path']).is_file() and digest(Path(row['path'])) == row['sha256']
    validation = strict_json(ROOT/'results/validation/status.json')
    assert validation['state'] == 'complete'
    assert validation['script_sha256'] == digest(ROOT/'validate_sequence.py')
    for relative, expected in validation['input_hashes'].items():
        assert digest(ROOT/relative) == expected, relative
    assert validation['accepted_equilibrium_rows'] == 49
    assert len(validation['failed_attempts_preserved']) == 6
    assert all(not row['used_for_prediction'] for row in validation['failed_attempts_preserved'])
    assert validation['refinement_spectral_calculations'] == 18
    assert validation['turning_tangent_spectral_calculations'] == 4
    fine_rows = []
    for label in ['clean-mesh-critical', 'turning-window', 'tangent-window']:
        report = strict_json(ROOT/f'results/{label}/status.json')
        assert report['arguments']['tol'] == 2e-9 and report['arguments']['floor'] == 1e-11
        assert report['helper_sha256'] == digest(ROOT/'sequence_tools_v4.py')
        assert report['base_helper_sha256'] == digest(ROOT/'sequence_tools.py')
        fine_rows.extend(report['rows'])
    assert len(fine_rows) == 16
    angular = max(row['angular_Einstein_relative_residual'] for row in fine_rows)
    scalar = max(row['scalar_collocation_relative_residual'] for row in fine_rows)
    assert angular < 3.73e-5 and scalar < 4e-6
    derivation = strict_json(ROOT/'results/derivation/status.json')
    assert derivation['state'] == 'complete' and derivation['exact_check_count'] == len(derivation['checks']) == 5
    assert all(row['passed'] for row in derivation['checks'])
    assert derivation['script_sha256'] == digest(ROOT/'derive_turning_relation.py')
    parsed = []
    failures = {row['run'] for row in validation['failed_attempts_preserved']}
    script_hashes = {digest(path) for path in ROOT.glob('*.py')}
    for path in sorted(ROOT.rglob('*.json')):
        report = strict_json(path)
        if isinstance(report, dict) and 'state' in report:
            assert report['state'] == 'complete' or (report['state'] == 'failed' and path.parent.name in failures)
        if isinstance(report, dict) and 'script_sha256' in report:
            assert report['script_sha256'] in script_hashes
        if isinstance(report, dict) and 'parent_seal_sha256' in report:
            assert report['parent_seal_sha256'] == digest(paths[0])
        parsed.append(path.relative_to(ROOT).as_posix())
    archives = []
    for path in sorted(ROOT.rglob('*.npz')):
        with np.load(path, allow_pickle=False) as archive:
            assert all(np.all(np.isfinite(archive[name])) for name in archive.files), path
            if 'frequency_squared' in archive:
                assert archive['frequency_squared'].shape == (4,)
        archives.append(path.relative_to(ROOT).as_posix())
    assert len(archives) == 131
    prose = '\n'.join(path.read_text(encoding='utf-8') for path in ROOT.glob('*.md'))
    required = [manifest, *paths, *[Path(row['path']) for row in sources]]
    for relative in set(re.findall(r'`([^`\n]+\.(?:md|json|py))`', prose)):
        path = (ROOT/relative).resolve()
        if path != OUTPUT.resolve():
            required.append(path)
    assert all(path.is_file() for path in required), [str(path) for path in required if not path.is_file()]
    urls = ['https://arxiv.org/abs/2103.15012', 'https://doi.org/10.1088/1361-6382/ac0160']
    assert all(url in prose for url in urls)
    compiled = []
    for path in sorted(ROOT.glob('*.py')):
        compile(path.read_bytes(), str(path), 'exec')
        compiled.append(path.name)
    assert not list(ROOT.rglob('__pycache__'))
    protected = POST.parent/'formalization-workbench'
    start = datetime(2026, 10, 3, 22, 9, 31, tzinfo=timezone.utc)
    assert protected.is_dir()
    changed = [str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime > start.timestamp()]
    assert not changed, changed
    hashes = {path.relative_to(ROOT).as_posix(): digest(path) for path in sorted(ROOT.rglob('*')) if path.is_file() and path != OUTPUT}
    prior_count = sum(len(row['file_hashes']) for row in previous)
    assert prior_count == 471
    report = {'state': 'complete', 'sealed_at': datetime.now(timezone.utc).isoformat(), 'file_hashes': hashes,
              'parent_seal_sha256': digest(paths[0]), 'prior_sealed_entries_unchanged': prior_count,
              'checkpoint_manifest_sha256': digest(manifest), 'full_checkpoint_payload_rehashed': False,
              'local_source_documents': sources, 'required_paths': sorted(set(str(path.resolve()) for path in required)),
              'primary_source_urls_checked_2026_10_03': urls, 'parsed_json_files': parsed, 'compiled_scripts': compiled,
              'exact_check_count': 5, 'converged_integral_gated_equilibrium_rows': 49,
              'authoritative_clean_fine_critical_window_rows': 16, 'exploratory_predecessor_rows': 33,
              'failed_BVP_attempts_preserved_and_excluded': 6,
              'signed_spectral_calculations_including_controls': 71,
              'first_order_generator_checks': 1, 'archives_verified': len(archives),
              'maximum_fine_critical_scalar_second_derivative_residual': scalar,
              'maximum_fine_critical_angular_second_derivative_residual': angular,
              'mass_charge_turning_center': validation['mass_charge_turning_center'],
              'resolved_signed_spectral_bracket': validation['resolved_spectral_bracket'],
              'finest_tangent_overlap': validation['finest_tangent_check']['overlap_with_lowest_mode'],
              'protected_workbench_recent_modified_file_count': len(changed),
              'protected_check_scope': 'Modification-time scan since22:09:31UTC; not a full content-hash baseline.',
              'fixed_theory_first_law_and_conditional_tangent_zero_derived': True,
              'radial_instability_numerically_resolved': True,
              'continuum_error_bound_or_strong_tangent_convergence_certified': False,
              'nonlinear_collapse_or_black_hole_endpoint_claimed': False,
              'new_physical_parameter_fitted': False, 'original_parent_or_bath_modified': False,
              'github_action': False, 'subagents': 0, 'one_below_normal_priority_single_core_worker_at_a_time': True}
    OUTPUT.write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
    print(json.dumps({'state': 'complete', 'sealed_files': len(hashes), 'prior_unchanged': prior_count,
                      'equilibria': 49, 'fine_critical_rows': 16, 'failed_attempts_retained': 6,
                      'signed_spectra': 71, 'exact_checks': 5, 'protected_changes': len(changed)}))


if __name__ == '__main__':
    main()
