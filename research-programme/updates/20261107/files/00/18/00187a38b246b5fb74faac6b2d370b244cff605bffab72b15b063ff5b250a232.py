from __future__ import annotations

from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import re

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
    stages = ['fixed-theory-sequence-20261003', 'radial-pulsations-20261003', 'radial-gravity-stability-20261003',
              'self-gravity-20261003', 'finite-charge-20261003', 'conserved-stress-20261003', 'ward-remainder-20261003',
              'tensor-ward-20261003', 'collective-operator-20261003', 'tensor-response-20261003']
    seals = [BRANCH/stage/'results/stage-integrity.json' for stage in stages]+[BRANCH/'results/stage-integrity.json']
    bases = [BRANCH/stage for stage in stages]+[POST]
    keys = ['parent_seal_sha256']*7+['previous_seal_sha256', 'previous_seal_sha256', 'parent_seal_sha256']
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
        assert Path(row['path']).is_file() and digest(Path(row['path'])) == row['sha256']
    validation = strict_json(ROOT/'results/validation/status.json')
    assert validation['state'] == 'complete' and validation['script_sha256'] == digest(ROOT/'validate_motion.py')
    for relative, expected in validation['input_hashes'].items():
        assert digest(ROOT/relative) == expected
    assert validation['exact_identity_checks'] == 23
    assert validation['flat_boost_checks'] == validation['extended_source_exchange_checks'] == 30
    assert validation['adm_surface_integrals'] == 28 and validation['binary_scale_examples'] == 4
    assert validation['maximum_flat_boost_normalized_error'] < 7.6e-14
    assert validation['maximum_fine_extended_source_error'] < 2.9e-13
    assert validation['maximum_adm_extrapolated_normalized_error'] < 1.9e-12
    assert not validation['binary_evolution_performed']
    assert not validation['tidal_response_coefficient_or_nonradial_stability_established']
    parsed = []
    script_hashes = {digest(path) for path in ROOT.glob('*.py')}
    for path in sorted(ROOT.rglob('*.json')):
        report = strict_json(path)
        assert report['state'] == 'complete'
        if 'script_sha256' in report:
            assert report['script_sha256'] in script_hashes
        parsed.append(path.relative_to(ROOT).as_posix())
    flat = strict_json(ROOT/'results/flat-motion/status.json')
    assert flat['source_seal_sha256'] == digest(BRANCH/'self-gravity-20261003/results/stage-integrity.json')
    for row in flat['sources']:
        assert digest(Path(row['path'])) == row['sha256']
    prose = '\n'.join(path.read_text(encoding='utf-8') for path in ROOT.glob('*.md'))
    required = [manifest, *seals, *[Path(row['path']) for row in local_sources]]
    for relative in set(re.findall(r'`([^`\n]+\.(?:md|json|py))`', prose)):
        path = (ROOT/relative).resolve()
        if path != OUTPUT.resolve():
            required.append(path)
    assert all(path.is_file() for path in required), [str(path) for path in required if not path.is_file()]
    urls = ['https://arxiv.org/abs/1808.09320', 'https://arxiv.org/pdf/1808.09320',
            'https://arxiv.org/abs/hep-th/0409156', 'https://arxiv.org/html/hep-th/0409156v2']
    assert all(url in prose for url in urls)
    compiled = []
    for path in sorted(ROOT.glob('*.py')):
        compile(path.read_bytes(), str(path), 'exec')
        compiled.append(path.name)
    assert len(compiled) == 7 and len(parsed) == 6
    assert not list(ROOT.rglob('__pycache__'))
    protected = POST.parent/'formalization-workbench'
    start = datetime(2026, 10, 3, 23, 6, 59, tzinfo=timezone.utc)
    assert protected.is_dir()
    changed = [str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime > start.timestamp()]
    assert not changed, changed
    hashes = {path.relative_to(ROOT).as_posix(): digest(path) for path in sorted(ROOT.rglob('*')) if path.is_file() and path != OUTPUT}
    prior_count = sum(len(row['file_hashes']) for row in previous)
    assert prior_count == 658
    report = {'state': 'complete', 'sealed_at_utc': datetime.now(timezone.utc).isoformat(),
              'user_facing_date_europe_london': '2026-10-04', 'file_hashes': hashes,
              'parent_seal_sha256': digest(seals[0]), 'prior_sealed_entries_unchanged': prior_count,
              'checkpoint_manifest_sha256': digest(manifest), 'full_checkpoint_payload_rehashed': False,
              'local_source_documents': local_sources, 'required_paths': sorted(set(str(path.resolve()) for path in required)),
              'primary_source_urls_checked_2026_10_04_london': urls, 'parsed_json_files': parsed, 'compiled_scripts': compiled,
              'exact_identity_checks': 23, 'flat_profiles': 3, 'flat_boost_checks': 30,
              'extended_source_exchange_checks': 30, 'adm_surface_evaluations': 28, 'leading_binary_scale_examples': 4,
              'maximum_flat_boost_normalized_error': validation['maximum_flat_boost_normalized_error'],
              'maximum_fine_extended_source_error': validation['maximum_fine_extended_source_error'],
              'maximum_adm_extrapolated_normalized_error': validation['maximum_adm_extrapolated_normalized_error'],
              'protected_workbench_recent_modified_file_count': len(changed),
              'protected_check_scope': 'Modification-time scan since23:06:59UTC on3October; not a full content-hash baseline.',
              'fixed_charge_collective_action_matched': True,
              'active_inertial_passive_monopole_mass_matched': True,
              'newton_interaction_derived_from_retained_einstein_sector': True,
              'new_gravitational_constant_or_physical_scale_fitted': False,
              'nonradial_gap_or_tidal_coefficient_derived': False,
              'binary_evolution_or_unconditional_error_bound_claimed': False,
              'original_parent_or_bath_modified': False, 'github_action': False, 'subagents': 0,
              'one_below_normal_priority_single_core_numerical_worker_at_a_time': True}
    OUTPUT.write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
    print(json.dumps({'state': 'complete', 'sealed_files': len(hashes), 'prior_unchanged': prior_count,
                      'exact_checks': 23, 'boosts': 30, 'source_interactions': 30, 'adm_surfaces': 28,
                      'protected_changes': len(changed)}))


if __name__ == '__main__':
    main()
