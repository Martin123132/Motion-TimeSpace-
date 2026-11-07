from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re

import psutil

from validate_shape import strict_json


ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
POST = BRANCH.parent
OUTPUT = ROOT/'results/stage-integrity.json'


def digest(path):
    hasher = hashlib.sha256()
    with Path(path).open('rb') as handle:
        for block in iter(lambda: handle.read(1024*1024), b''):
            hasher.update(block)
    return hasher.hexdigest()


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    assert not OUTPUT.exists()
    stages = ['collective-motion-20261004', 'fixed-theory-sequence-20261003', 'radial-pulsations-20261003',
              'radial-gravity-stability-20261003', 'self-gravity-20261003', 'finite-charge-20261003',
              'conserved-stress-20261003', 'ward-remainder-20261003', 'tensor-ward-20261003',
              'collective-operator-20261003', 'tensor-response-20261003']
    seals = [BRANCH/stage/'results/stage-integrity.json' for stage in stages]+[BRANCH/'results/stage-integrity.json']
    bases = [BRANCH/stage for stage in stages]+[POST]
    keys = ['parent_seal_sha256']*8+['previous_seal_sha256', 'previous_seal_sha256', 'parent_seal_sha256']
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
    validation = strict_json(ROOT/'results/validation/status.json')
    assert validation['state'] == 'complete'
    assert validation['script_sha256'] == digest(ROOT/'validate_shape.py')
    for relative, expected in validation['input_hashes'].items():
        assert digest(ROOT/relative) == expected
    assert validation['exact_identity_checks'] == 13
    assert validation['primary_quadratic_spectral_rows'] == 12
    assert validation['primary_static_bvp_rows'] == 9
    assert validation['independent_quadratic_gyro_checks'] == 3
    assert validation['finite_energy_tests'] == 24
    assert not validation['computed_full_self_gravitating_love_number']
    assert not validation['computed_self_gravitating_quadrupole_frequency']
    assert validation['excluded_tight_attempt']['state'] == 'failed_at_R80'
    script_hashes = {digest(path) for path in ROOT.glob('*.py')}
    parsed = []
    for path in sorted(ROOT.rglob('*.json')):
        report = strict_json(path)
        expected_state = 'failed' if path == ROOT/'results/static-bvp-tight/status.json' else 'complete'
        assert report['state'] == expected_state, path
        assert report['script_sha256'] in script_hashes
        parsed.append(path.relative_to(ROOT).as_posix())
    prose = '\n'.join(path.read_text(encoding='utf-8') for path in ROOT.glob('*.md'))
    required = [manifest, *seals, *[Path(row['path']) for row in local_sources]]
    for relative in set(re.findall(r'`([^`\n]+\.(?:md|json|py))`', prose)):
        path = (ROOT/relative).resolve()
        if path != OUTPUT.resolve():
            required.append(path)
    assert all(path.is_file() for path in required), [str(path) for path in required if not path.is_file()]
    urls = ['https://arxiv.org/abs/1704.08651', 'https://arxiv.org/pdf/1704.08651',
            'https://doi.org/10.1103/PhysRevD.96.024002']
    assert all(url in prose for url in urls)
    compiled = []
    for path in sorted(ROOT.glob('*.py')):
        compile(path.read_bytes(), str(path), 'exec')
        compiled.append(path.name)
    assert len(compiled) == 9 and len(parsed) == 10
    assert not list(ROOT.rglob('__pycache__'))
    protected = POST.parent/'formalization-workbench'
    start = datetime(2026, 10, 3, 23, 32, 43, tzinfo=timezone.utc)
    assert protected.is_dir()
    changed = [str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime > start.timestamp()]
    assert not changed, changed
    hashes = {path.relative_to(ROOT).as_posix(): digest(path) for path in sorted(ROOT.rglob('*')) if path.is_file() and path != OUTPUT}
    prior_count = sum(len(row['file_hashes']) for row in previous)
    assert prior_count == 674
    report = {'state': 'complete', 'sealed_at_utc': datetime.now(timezone.utc).isoformat(),
              'user_facing_date_europe_london': '2026-10-04', 'file_hashes': hashes,
              'parent_seal_sha256': digest(seals[0]), 'prior_sealed_entries_unchanged': prior_count,
              'checkpoint_manifest_sha256': digest(manifest), 'full_checkpoint_payload_rehashed': False,
              'local_source_documents': local_sources, 'required_paths': sorted(set(str(path.resolve()) for path in required)),
              'primary_source_urls_checked_2026_10_04_london': urls,
              'parsed_json_files': parsed, 'compiled_scripts': compiled,
              'exact_identity_checks': 13, 'flat_profiles': 3, 'primary_spectral_rows': 12,
              'primary_static_bvp_rows': 9, 'independent_generator_checks': 3, 'finite_energy_tests': 24,
              'preserved_excluded_tight_attempt': validation['excluded_tight_attempt'],
              'maximum_finite_element_bvp_relative_difference': max(row['finite_element_bvp_relative_difference'] for row in validation['numerical_checks']),
              'maximum_last_frequency_mesh_relative_change': max(row['last_frequency_mesh_relative_change'] for row in validation['numerical_checks']),
              'protected_workbench_recent_modified_file_count': len(changed),
              'protected_check_scope': 'Modification-time scan since23:32:43UTC on3October; not a full content-hash baseline.',
              'conditional_analytic_flat_angular_bound_derived': True,
              'flat_weak_metric_relaxation_response_derived_and_computed': True,
              'same_potential_large_charge_surface_limit_compared_without_fit': True,
              'full_self_gravitating_love_number_computed': False,
              'self_gravitating_quadrupole_gap_computed': False,
              'original_parent_or_bath_modified': False, 'github_action': False, 'subagents': 0,
              'one_below_normal_priority_single_core_numerical_worker_at_a_time': True}
    OUTPUT.write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
    print(json.dumps({'state': 'complete', 'sealed_files': len(hashes), 'prior_unchanged': prior_count,
                      'exact_checks': 13, 'primary_spectra': 12, 'static_bvp': 9,
                      'protected_changes': len(changed), 'excluded_attempts_preserved': 1}))


if __name__ == '__main__':
    main()
