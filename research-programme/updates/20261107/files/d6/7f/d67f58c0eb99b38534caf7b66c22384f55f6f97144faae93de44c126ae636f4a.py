from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re

import psutil

from validate_tides import strict_json


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
    stages = ['quadrupole-response-20261004', 'collective-motion-20261004', 'fixed-theory-sequence-20261003',
              'radial-pulsations-20261003', 'radial-gravity-stability-20261003', 'self-gravity-20261003',
              'finite-charge-20261003', 'conserved-stress-20261003', 'ward-remainder-20261003',
              'tensor-ward-20261003', 'collective-operator-20261003', 'tensor-response-20261003']
    seals = [BRANCH/stage/'results/stage-integrity.json' for stage in stages]+[BRANCH/'results/stage-integrity.json']
    bases = [BRANCH/stage for stage in stages]+[POST]
    keys = ['parent_seal_sha256']*9+['previous_seal_sha256', 'previous_seal_sha256', 'parent_seal_sha256']
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
    assert validation['script_sha256'] == digest(ROOT/'validate_tides.py')
    for relative, expected in validation['input_hashes'].items():
        assert digest(ROOT/relative) == expected
    assert validation['exact_identity_checks'] == 28
    assert validation['primary_fine_solutions'] == 7 and validation['all_tidal_solutions_including_pilot'] == 19
    assert validation['exterior_extraction_controls'] == 76 and validation['finite_perturbation_curvature_tests'] == 48
    assert not validation['global_gravitational_frequency_gap_claimed']
    assert not validation['nonradial_time_evolution_or_resonance_spectrum_computed']
    script_hashes = {digest(path) for path in ROOT.glob('*.py')}
    parsed = []
    for path in sorted(ROOT.rglob('*.json')):
        report = strict_json(path)
        assert report['state'] == 'complete' and report['script_sha256'] in script_hashes, path
        parsed.append(path.relative_to(ROOT).as_posix())
    prose = '\n'.join(path.read_text(encoding='utf-8') for path in ROOT.glob('*.md'))
    required = [manifest, *seals, *[Path(row['path']) for row in local_sources],
                ROOT/'results/edge-weak/INTERRUPTED.md', ROOT/'results/curvature/FAILED.md']
    for relative in set(re.findall(r'`([^`\n]+\.(?:md|json|py))`', prose)):
        path = (ROOT/relative).resolve()
        if path != OUTPUT.resolve():
            required.append(path)
    assert all(path.is_file() for path in required), [str(path) for path in required if not path.is_file()]
    urls = ['https://arxiv.org/abs/1704.08651', 'https://arxiv.org/pdf/1704.08651',
            'https://doi.org/10.1103/PhysRevD.96.024002', 'https://arxiv.org/abs/1608.01907',
            'https://arxiv.org/pdf/1608.01907', 'https://doi.org/10.1103/PhysRevD.94.104028']
    assert all(url in prose for url in urls)
    compiled = []
    for path in sorted(ROOT.glob('*.py')):
        compile(path.read_bytes(), str(path), 'exec')
        compiled.append(path.name)
    assert len(compiled) == 10 and len(parsed) == 10
    assert not list(ROOT.rglob('__pycache__'))
    protected = POST.parent/'formalization-workbench'
    start = datetime(2026, 10, 4, 0, 21, 6, tzinfo=timezone.utc)
    assert protected.is_dir()
    changed = [str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime > start.timestamp()]
    assert not changed, changed
    hashes = {path.relative_to(ROOT).as_posix(): digest(path) for path in sorted(ROOT.rglob('*')) if path.is_file() and path != OUTPUT}
    prior_count = sum(len(row['file_hashes']) for row in previous)
    assert prior_count == 735
    report = {'state': 'complete', 'sealed_at_utc': datetime.now(timezone.utc).isoformat(),
              'user_facing_date_europe_london': '2026-10-04', 'file_hashes': hashes,
              'parent_seal_sha256': digest(seals[0]), 'prior_sealed_entries_unchanged': prior_count,
              'checkpoint_manifest_sha256': digest(manifest), 'full_checkpoint_payload_rehashed': False,
              'local_source_documents': local_sources, 'required_paths': sorted(set(str(path.resolve()) for path in required)),
              'primary_source_urls_checked_2026_10_04_london': urls,
              'parsed_json_files': parsed, 'compiled_scripts': compiled,
              'exact_identity_checks': 28, 'primary_fine_tidal_solutions': 7, 'total_tidal_solutions_with_controls': 19,
              'exterior_extraction_controls': 76, 'finite_perturbation_curvature_tests': 48,
              'static_worldline_examples': 4, 'preserved_excluded_attempts': validation['preserved_excluded_attempts'],
              'weak_limit_relative_extrapolation_difference': validation['weak_limit_relative_extrapolation_difference'],
              'maximum_local_small_step_einstein_residual': validation['maximum_small_step_nonlinear_ricci_test_residual'],
              'protected_workbench_recent_modified_file_count': len(changed),
              'protected_check_scope': 'Modification-time scan since00:21:06UTC on4October; not a full content-hash baseline.',
              'static_einstein_scalar_quadrupole_deformability_derived_and_computed': True,
              'zero_frequency_finite_size_worldline_coefficient_matched': True,
              'gravitational_quadrupole_resonances_or_time_evolution_computed': False,
              'newton_constant_or_physical_scale_fitted': False,
              'original_parent_or_bath_modified': False, 'github_action': False, 'subagents': 0,
              'one_below_normal_priority_single_core_numerical_worker_at_a_time': True}
    OUTPUT.write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
    print(json.dumps({'state': 'complete', 'sealed_files': len(hashes), 'prior_unchanged': prior_count,
                      'exact_checks': 28, 'fine_solutions': 7, 'all_solutions': 19,
                      'protected_changes': len(changed), 'excluded_attempts_preserved': 2}))


if __name__ == '__main__':
    main()
