from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parent
POST = ROOT.parent
CHECKPOINT = POST / '_checkpoints' / '20261003-pre-condensate-origin'
OUTPUT = ROOT / 'results' / 'stage-integrity.json'


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    if OUTPUT.exists():
        raise RuntimeError('Do not overwrite a sealed stage.')
    verification = json.loads((ROOT / 'results/checkpoint-validation/status.json').read_text())
    assert verification['state'] == 'complete'
    assert not verification['original_snapshot_sources_changed']
    assert not verification['protected_workbench_files_modified_since_turn_start']
    manifest = json.loads((CHECKPOINT / 'manifest.json').read_text())
    assert sha256(CHECKPOINT / 'manifest.json') == (CHECKPOINT / 'manifest.sha256').read_text().strip()
    assert verification['full_snapshot_dry_run']['files'] == manifest['file_count'] == 17373
    reports = [json.loads((ROOT / 'results' / name / 'status.json').read_text()) for name in ['first-candidate', 'repair-independent-check', 'tensor-response']]
    for report in reports:
        assert report['state'] == 'complete'
        assert all(row['passed'] for row in report['checks'])
    count = sum(report['exact_identity_checks'] for report in reports)
    assert count == 139
    sample_count = len(reports[0]['numeric_spectrum_samples']) + reports[1]['sample_count']
    assert sample_count == 51
    for name, expected in reports[0]['source_hashes'].items():
        assert sha256(POST / name) == expected, name
    scripts = list(ROOT.glob('*.py')) + list(CHECKPOINT.glob('*.py'))
    for path in scripts:
        compile(path.read_bytes(), str(path), 'exec')
    files = [path for path in ROOT.rglob('*') if path.is_file() and path != OUTPUT]
    files += [path for path in CHECKPOINT.iterdir() if path.is_file()]
    files.append(POST / 'CHECKPOINT-20261003-BEFORE-CONDENSATE.md')
    assert not any('__pycache__' in path.parts or path.suffix == '.pyc' for path in files)
    records = {path.relative_to(POST).as_posix(): sha256(path) for path in sorted(files)}
    result = {
        'state': 'complete', 'sealed_at': datetime.now(timezone.utc).isoformat(),
        'file_hashes': records, 'snapshot_manifest_sha256': sha256(CHECKPOINT / 'manifest.json'),
        'snapshot_file_count': manifest['file_count'], 'snapshot_bytes': manifest['total_bytes'],
        'parent_authority_hashes_verified': manifest['parent_hashes_verified'],
        'original_sources_changed_before_final_bookmark_update': [],
        'mutable_resume_change_permitted_after_seal': True,
        'exact_identity_checks': count, 'spectrum_samples': sample_count,
        'scripts_compiled': len(scripts), 'restore_dry_run_payloads_verified': manifest['file_count'],
        'actual_restore_fixture_files': verification['fixture_execute']['files'],
        'restore_safety_refusals': len(verification['fixture_refusals']),
        'protected_workbench_changes': 0, 'github_action': False, 'subagents': 0,
        'candidate_adopted_into_original_framework': False,
        'original_real_scalar_instability_claim': False,
        'new_complex_original_power_instability_detected': True,
        'new_repulsive_operator_stability_condition_derived': True,
        'spacetime_or_standard_model_origin_solved': False,
    }
    OUTPUT.write_text(json.dumps(result, indent=2), encoding='utf-8')
    print(json.dumps({key: result[key] for key in ['state', 'snapshot_file_count', 'snapshot_bytes', 'exact_identity_checks', 'spectrum_samples', 'scripts_compiled', 'actual_restore_fixture_files', 'restore_safety_refusals', 'protected_workbench_changes']}))


if __name__ == '__main__':
    main()
