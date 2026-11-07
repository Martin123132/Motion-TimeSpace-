from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
import re

import psutil

from validate_response_v3 import digest, strict_json


ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
POST = BRANCH.parent
OUTPUT = ROOT/'results/stage-integrity.json'


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    assert not OUTPUT.exists()
    stages = ['dynamical-tides-20261004', 'gravitating-tides-20261004', 'quadrupole-response-20261004',
              'collective-motion-20261004', 'fixed-theory-sequence-20261003', 'radial-pulsations-20261003',
              'radial-gravity-stability-20261003', 'self-gravity-20261003', 'finite-charge-20261003',
              'conserved-stress-20261003', 'ward-remainder-20261003', 'tensor-ward-20261003',
              'collective-operator-20261003', 'tensor-response-20261003']
    seals = [BRANCH/stage/'results/stage-integrity.json' for stage in stages]+[BRANCH/'results/stage-integrity.json']
    bases = [BRANCH/stage for stage in stages]+[POST]
    keys = ['parent_seal_sha256']*11+['previous_seal_sha256', 'previous_seal_sha256', 'parent_seal_sha256']
    previous = []
    for path, base in zip(seals, bases):
        report = strict_json(path)
        assert report['state'] == 'complete'
        for relative, expected in report['file_hashes'].items():
            assert digest(base/relative) == expected, base/relative
        previous.append(report)
    for index, key in enumerate(keys):
        assert previous[index][key] == digest(seals[index+1])
    prior_count = sum(len(row['file_hashes']) for row in previous)
    assert prior_count == 884, prior_count
    manifest = POST/'_checkpoints/20261003-pre-condensate-origin/manifest.json'
    assert digest(manifest) == previous[0]['checkpoint_manifest_sha256']
    local_sources = previous[0]['local_source_documents']
    for row in local_sources:
        assert Path(row['path']).is_file() and digest(row['path']) == row['sha256']
    validation_path = ROOT/'results/validation-v3/status.json'
    validation = strict_json(validation_path)
    assert validation['state'] == 'complete' and all(row['passed'] for row in validation['checks'])
    assert validation['script_sha256'] == digest(ROOT/'validate_response_v3.py')
    assert len(validation['checks']) == 96 and validation['accepted_interior_evaluations'] == 66
    assert validation['near_pole_value_identity_excluded_evaluations'] == 2
    for relative, expected in validation['input_hashes'].items():
        assert digest(ROOT/relative) == expected, relative
    assert digest(validation['static_source_path']) == validation['static_source_sha256']
    script_hashes = {digest(path) for path in ROOT.glob('*.py')}
    parsed = []
    for path in sorted(ROOT.rglob('*.json')):
        report = strict_json(path)
        assert report['state'] == 'complete' and report['script_sha256'] in script_hashes, path
        parsed.append(path.relative_to(ROOT).as_posix())
    for label in ['validation', 'validation-v2']:
        assert (ROOT/f'results/{label}/FAILED.md').is_file()
        assert (ROOT/f'results/{label}-console.txt').is_file()
    assert (ROOT/'results/pilot/LOW_FREQUENCY_IMAGINARY_PRECISION.md').is_file()
    prose = '\n'.join(path.read_text(encoding='utf-8') for path in ROOT.glob('*.md'))
    required = [manifest, *seals, *[Path(row['path']) for row in local_sources], Path(validation['static_source_path'])]
    for relative in set(re.findall(r'`([^`\n]+\.(?:md|json|py|npz))`', prose)):
        path = (ROOT/relative).resolve()
        if path != OUTPUT.resolve():
            required.append(path)
    assert all(path.is_file() for path in required), [str(path) for path in required if not path.is_file()]
    urls = ['https://arxiv.org/abs/1307.4812', 'https://doi.org/10.1103/PhysRevD.88.064046',
            'https://arxiv.org/abs/2606.19446', 'https://arxiv.org/abs/2511.12580', 'https://doi.org/10.1103/4ql9-mgj5']
    assert all(url in prose for url in urls)
    compiled = []
    for path in sorted(ROOT.glob('*.py')):
        compile(path.read_bytes(), str(path), 'exec')
        compiled.append(path.name)
    assert not list(ROOT.rglob('__pycache__'))
    protected = POST.parent/'formalization-workbench'
    start = datetime(2026, 10, 4, 2, 23, 41, tzinfo=timezone.utc)
    assert protected.is_dir()
    changed = [str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime > start.timestamp()]
    assert not changed, changed
    hashes = {path.relative_to(ROOT).as_posix(): digest(path) for path in sorted(ROOT.rglob('*')) if path.is_file() and path != OUTPUT}
    report = {'state': 'complete', 'sealed_at_utc': datetime.now(timezone.utc).isoformat(), 'file_hashes': hashes,
              'parent_seal_sha256': digest(seals[0]), 'prior_sealed_entries_unchanged': prior_count,
              'checkpoint_manifest_sha256': digest(manifest), 'full_checkpoint_payload_rehashed': False,
              'local_source_documents': local_sources, 'required_paths': sorted(set(str(path.resolve()) for path in required)),
              'primary_source_urls_checked_2026_10_04_london': urls,
              'recent_dynamic_response_papers_read_to_abstract_only': True,
              'parsed_json_files': parsed, 'compiled_scripts': compiled, 'validation_check_count': len(validation['checks']),
              'recorded_algebra_checks': 17, 'substantive_algebra_checks': 14, 'elementary_bookkeeping_checks': 3,
              'accepted_interior_evaluations': 66, 'retained_pilot_interior_evaluations': 11,
              'near_pole_value_identity_excluded_evaluations': 2,
              'preserved_validation_attempts': ['results/validation/FAILED.md', 'results/validation-v2/FAILED.md'],
              'pole': validation['pole'], 'surface_Green_residue': validation['surface_Green_residue'],
              'static_limit_relative_error': validation['static_limit_relative_error'],
              'recentered_derivative_contour_relative_errors': validation['recentered_derivative_contour_relative_errors'],
              'protected_workbench_recent_modified_file_count': len(changed),
              'protected_check_scope': 'Modification-time scan since02:23:41UTC on4October; not a full content-hash baseline.',
              'retarded_Green_response_and_source_jump_derived': True,
              'pole_residue_and_nonpole_response_computed': True,
              'leading_fifth_power_radiation_law_derived': True,
              'scheme_independent_finite_frequency_worldline_coefficient_claimed': False,
              'companion_stress_or_binary_force_bound_derived': False,
              'physical_scale_or_Newton_constant_fitted': False,
              'original_parent_or_bath_modified': False, 'github_action': False, 'subagents': 0,
              'one_below_normal_single_core_numerical_worker_at_a_time': True}
    OUTPUT.write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
    print(json.dumps({'state': 'complete', 'sealed_files': len(hashes), 'prior_unchanged': prior_count,
                      'validation_checks': len(validation['checks']), 'interior_evaluations': 66,
                      'protected_changes': len(changed), 'preserved_validation_attempts': 2}))


if __name__ == '__main__':
    main()
