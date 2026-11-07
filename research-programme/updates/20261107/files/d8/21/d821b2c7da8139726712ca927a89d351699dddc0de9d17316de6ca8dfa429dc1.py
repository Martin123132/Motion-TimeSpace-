from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
import re

import psutil

from validate_dynamics import digest, strict_json


ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
POST = BRANCH.parent
OUTPUT = ROOT/'results/stage-integrity.json'


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    assert not OUTPUT.exists()
    stages = ['gravitating-tides-20261004', 'quadrupole-response-20261004', 'collective-motion-20261004', 'fixed-theory-sequence-20261003',
              'radial-pulsations-20261003', 'radial-gravity-stability-20261003', 'self-gravity-20261003', 'finite-charge-20261003',
              'conserved-stress-20261003', 'ward-remainder-20261003', 'tensor-ward-20261003', 'collective-operator-20261003', 'tensor-response-20261003']
    seals = [BRANCH/stage/'results/stage-integrity.json' for stage in stages]+[BRANCH/'results/stage-integrity.json']
    bases = [BRANCH/stage for stage in stages]+[POST]
    keys = ['parent_seal_sha256']*10+['previous_seal_sha256', 'previous_seal_sha256', 'parent_seal_sha256']
    previous = []
    for path, base in zip(seals, bases):
        report = strict_json(path)
        assert report['state'] == 'complete'
        for relative, expected in report['file_hashes'].items():
            assert digest(base/relative) == expected, base/relative
        previous.append(report)
    for index, key in enumerate(keys):
        assert previous[index][key] == digest(seals[index+1])
    manifest = POST/'_checkpoints/20261003-pre-condensate-origin/manifest.json'
    assert digest(manifest) == previous[0]['checkpoint_manifest_sha256']
    local_sources = previous[0]['local_source_documents']
    for row in local_sources:
        assert Path(row['path']).is_file() and digest(row['path']) == row['sha256']
    validation_path = ROOT/'results/validation/status.json'
    validation = strict_json(validation_path)
    assert validation['state'] == 'complete' and all(row['passed'] for row in validation['checks'])
    assert validation['script_sha256'] == digest(ROOT/'validate_dynamics.py')
    for relative, expected in validation['input_hashes'].items():
        assert digest(ROOT/relative) == expected, relative
    assert validation['exact_identity_checks'] == 30 and validation['accepted_outgoing_mode_controls'] == 6
    assert validation['finite_nonlinear_tests'] == 96 and validation['vacuum_outgoing_controls'] == 13
    script_hashes = {digest(path) for path in ROOT.glob('*.py')}
    parsed, failed = [], []
    for path in sorted(ROOT.rglob('*.json')):
        report = strict_json(path)
        assert report['script_sha256'] in script_hashes, path
        if report['state'] == 'failed':
            assert path.parent.name in validation['preserved_excluded_attempts'] and (path.parent/'FAILED.md').is_file()
            failed.append(path.relative_to(ROOT).as_posix())
        else:
            assert report['state'] == 'complete', path
        parsed.append(path.relative_to(ROOT).as_posix())
    required = [manifest, *seals, *[Path(row['path']) for row in local_sources]]
    prose = '\n'.join(path.read_text(encoding='utf-8') for path in ROOT.glob('*.md'))
    for relative in set(re.findall(r'`([^`\n]+\.(?:md|json|py|npz))`', prose)):
        path = (ROOT/relative).resolve()
        if path != OUTPUT.resolve():
            required.append(path)
    assert all(path.is_file() for path in required), [str(path) for path in required if not path.is_file()]
    urls = ['https://arxiv.org/abs/1307.4812', 'https://arxiv.org/pdf/1307.4812', 'https://doi.org/10.1103/PhysRevD.88.064046']
    assert all(url in prose for url in urls)
    compiled = []
    for path in sorted(ROOT.glob('*.py')):
        compile(path.read_bytes(), str(path), 'exec')
        compiled.append(path.name)
    assert not list(ROOT.rglob('__pycache__'))
    protected = POST.parent/'formalization-workbench'
    start = datetime(2026, 10, 4, 1, 31, 16, tzinfo=timezone.utc)
    assert protected.is_dir()
    changed = [str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime > start.timestamp()]
    assert not changed, changed
    hashes = {path.relative_to(ROOT).as_posix(): digest(path) for path in sorted(ROOT.rglob('*')) if path.is_file() and path != OUTPUT}
    prior_count = sum(len(row['file_hashes']) for row in previous)
    assert prior_count == 791, prior_count
    report = {'state': 'complete', 'sealed_at_utc': datetime.now(timezone.utc).isoformat(), 'file_hashes': hashes,
              'parent_seal_sha256': digest(seals[0]), 'prior_sealed_entries_unchanged': prior_count,
              'checkpoint_manifest_sha256': digest(manifest), 'full_checkpoint_payload_rehashed': False,
              'local_source_documents': local_sources, 'required_paths': sorted(set(str(path.resolve()) for path in required)),
              'primary_source_urls_checked_2026_10_04_london': urls, 'parsed_json_files': parsed, 'failed_json_files_preserved': failed,
              'compiled_scripts': compiled, 'validation_check_count': len(validation['checks']),
              'symbolic_identity_checks': 29, 'flat_closed_series_arithmetic_check': 1,
              'accepted_interior_real_frequency_solutions': 11, 'accepted_outgoing_mode_controls': 6,
              'accepted_mode_solver_evaluations': 38, 'finite_nonlinear_curvature_field_tests': 96,
              'main_outgoing_mode': validation['main_mode'], 'static_limit_relative_difference': validation['static_limit_relative_difference'],
              'weak_extrapolation_relative_difference': validation['weak_extrapolation_relative_difference'],
              'preserved_excluded_attempts': validation['preserved_excluded_attempts'],
              'protected_workbench_recent_modified_file_count': len(changed),
              'protected_check_scope': 'Modification-time scan since01:31:16UTC on4October; not a full content-hash baseline.',
              'coupled_time_dependent_quadrupole_and_surface_current_law_derived': True,
              'outgoing_matter_led_quadrupole_pole_computed': True, 'global_gravitational_gap_claimed': False,
              'finite_frequency_Love_residue_or_binary_response_bound_completed': False,
              'physical_scale_or_Newton_constant_fitted': False, 'original_parent_or_bath_modified': False,
              'github_action': False, 'subagents': 0, 'one_below_normal_single_core_numerical_worker_at_a_time': True}
    OUTPUT.write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
    print(json.dumps({'state': 'complete', 'sealed_files': len(hashes), 'prior_unchanged': prior_count,
                      'validation_checks': len(validation['checks']), 'accepted_pole_controls': 6,
                      'protected_changes': len(changed), 'preserved_excluded_attempt_groups': len(validation['preserved_excluded_attempts'])}))


if __name__ == '__main__':
    main()
