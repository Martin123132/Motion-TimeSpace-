from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
import re

import psutil

from validate_orbit import digest, strict_json


ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
POST = BRANCH.parent
OUTPUT = ROOT/'results/stage-integrity.json'


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    assert not OUTPUT.exists()
    stages = ['companion-source-20261004', 'retarded-response-20261004', 'dynamical-tides-20261004',
              'gravitating-tides-20261004', 'quadrupole-response-20261004', 'collective-motion-20261004',
              'fixed-theory-sequence-20261003', 'radial-pulsations-20261003', 'radial-gravity-stability-20261003',
              'self-gravity-20261003', 'finite-charge-20261003', 'conserved-stress-20261003',
              'ward-remainder-20261003', 'tensor-ward-20261003', 'collective-operator-20261003', 'tensor-response-20261003']
    seals = [BRANCH/stage/'results/stage-integrity.json' for stage in stages]+[BRANCH/'results/stage-integrity.json']
    bases = [BRANCH/stage for stage in stages]+[POST]
    keys = ['parent_seal_sha256']*13+['previous_seal_sha256', 'previous_seal_sha256', 'parent_seal_sha256']
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
    assert prior_count == 1014, prior_count
    manifest = POST/'_checkpoints/20261003-pre-condensate-origin/manifest.json'
    assert digest(manifest) == previous[0]['checkpoint_manifest_sha256']
    local_sources = previous[0]['local_source_documents']
    for row in local_sources:
        assert Path(row['path']).is_file() and digest(row['path']) == row['sha256']
    validation = strict_json(ROOT/'results/validation/status.json')
    assert validation['state'] == 'complete' and all(row['passed'] for row in validation['checks'])
    assert len(validation['checks']) == 252 and validation['symbolic_checks'] == 28
    assert validation['new_saved_interiors_replayed'] == 44 and validation['inherited_wave_rows_reconstructed'] == 20
    assert validation['script_sha256'] == digest(ROOT/'validate_orbit.py')
    for relative, expected in validation['input_hashes'].items():
        assert digest(ROOT/relative) == expected, relative
    script_hashes = {digest(path) for path in ROOT.glob('*.py')}
    parsed = []
    for path in sorted(ROOT.rglob('*.json')):
        report = strict_json(path)
        assert report['state'] == 'complete' and report['script_sha256'] in script_hashes, path
        parsed.append(path.relative_to(ROOT).as_posix())
    acquisition = strict_json(ROOT/'sources/provenance.json')
    for row in acquisition['sources']:
        assert digest(row['path']) == row['sha256']
    prose = '\n'.join(path.read_text(encoding='utf-8') for path in ROOT.glob('*.md'))
    required = [manifest, *seals, *[Path(row['path']) for row in local_sources], *[Path(row['path']) for row in acquisition['sources']]]
    for relative in set(re.findall(r'`([^`\n]+\.(?:md|json|py|npz|pdf|csv))`', prose)):
        path = (ROOT/relative).resolve()
        if path != OUTPUT.resolve():
            required.append(path)
    assert all(path.is_file() for path in required), [str(path) for path in required if not path.is_file()]
    urls = ['https://arxiv.org/abs/gr-qc/0311017', 'https://doi.org/10.1103/PhysRevD.69.044025',
            'https://arxiv.org/abs/1101.1673', 'https://doi.org/10.1103/PhysRevD.83.084051',
            'https://arxiv.org/abs/1612.02504', 'https://doi.org/10.1088/1361-6382/aa7342']
    assert all(url in prose for url in urls)
    compiled = []
    for path in sorted(ROOT.glob('*.py')):
        compile(path.read_bytes(), str(path), 'exec')
        compiled.append(path.name)
    assert not list(ROOT.rglob('__pycache__'))
    protected = POST.parent/'formalization-workbench'
    start = datetime(2026, 10, 4, 14, 34, 17, tzinfo=timezone.utc)
    changed = [str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime > start.timestamp()]
    assert protected.is_dir() and not changed, changed
    hashes = {path.relative_to(ROOT).as_posix(): digest(path) for path in sorted(ROOT.rglob('*')) if path.is_file() and path != OUTPUT}
    report = {'state': 'complete', 'sealed_at_utc': datetime.now(timezone.utc).isoformat(), 'file_hashes': hashes,
              'parent_seal_sha256': digest(seals[0]), 'prior_sealed_entries_unchanged': prior_count,
              'checkpoint_manifest_sha256': digest(manifest), 'full_checkpoint_payload_rehashed': False,
              'local_source_documents': local_sources, 'required_paths': sorted(set(str(path.resolve()) for path in required)),
              'primary_source_urls_checked_2026_10_04_london': urls,
              'selected_source_pages_visually_inspected': ['Martel2004p17', 'VinesFlanaganHinderer2011p4p6', 'FujitaEtAl2017p2p3'],
              'parsed_json_files': parsed, 'compiled_scripts': compiled,
              'validation_checks': len(validation['checks']), 'symbolic_checks': 28,
              'new_saved_interiors_replayed': 44, 'inherited_wave_rows_reconstructed': 20,
              'maximum_action_precision_difference': validation['maximum_action_precision_difference'],
              'derivative_controls': validation['derivative_controls'],
              'protected_workbench_recent_modified_file_count': len(changed),
              'protected_check_scope': 'Modification-time scan since14:34:17UTC on4October; not a full content-hash baseline.',
              'same_source_conservative_polar_quadrupole_action_derived': True,
              'static_and_first_relative_PN_conservative_limit_checked': True,
              'compatible_leading_Newtonian_adiabatic_inspiral_derived': True,
              'finite_frequency_complete_postadiabatic_inspiral_derived': False,
              'astrophysical_scale_fitted_or_observational_detection_claimed': False,
              'original_parent_or_bath_modified': False, 'github_action': False, 'subagents': 0,
              'one_below_normal_single_core_numerical_worker_at_a_time': True}
    OUTPUT.write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
    print(json.dumps({'state': 'complete', 'sealed_files': len(hashes), 'prior_unchanged': prior_count,
                      'validation_checks': len(validation['checks']), 'symbolic_checks': 28, 'saved_interiors': 44,
                      'protected_changes': len(changed)}))


if __name__ == '__main__':
    main()
