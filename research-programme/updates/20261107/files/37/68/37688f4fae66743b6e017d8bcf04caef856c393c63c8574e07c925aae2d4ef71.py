from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path
import re

import numpy as np
import psutil

from validate_axial_v2 import digest, strict_json


ROOT = Path(__file__).resolve().parent
BRANCH = ROOT.parent
POST = BRANCH.parent
OUTPUT = ROOT/'results/stage-integrity.json'


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    assert not OUTPUT.exists()
    stages = ['pn-balance-20261004', 'orbital-backreaction-20261004', 'companion-source-20261004',
              'retarded-response-20261004', 'dynamical-tides-20261004',
              'gravitating-tides-20261004', 'quadrupole-response-20261004',
              'collective-motion-20261004', 'fixed-theory-sequence-20261003',
              'radial-pulsations-20261003', 'radial-gravity-stability-20261003',
              'self-gravity-20261003', 'finite-charge-20261003', 'conserved-stress-20261003',
              'ward-remainder-20261003', 'tensor-ward-20261003',
              'collective-operator-20261003', 'tensor-response-20261003']
    seals = [BRANCH/stage/'results/stage-integrity.json' for stage in stages]+[BRANCH/'results/stage-integrity.json']
    bases = [BRANCH/stage for stage in stages]+[POST]
    keys = ['parent_seal_sha256']*15+['previous_seal_sha256', 'previous_seal_sha256', 'parent_seal_sha256']
    previous = []
    for path, base in zip(seals, bases):
        report = strict_json(path)
        assert report['state'] == 'complete'
        for relative, expected in report['file_hashes'].items():
            assert digest(base/relative) == expected, base/relative
        previous.append(report)
    assert len(keys) == len(seals)-1
    for index, key in enumerate(keys):
        assert previous[index][key] == digest(seals[index+1])
    prior_count = sum(len(row['file_hashes']) for row in previous)
    assert prior_count == 1124, prior_count
    manifest = POST/'_checkpoints/20261003-pre-condensate-origin/manifest.json'
    assert digest(manifest) == previous[0]['checkpoint_manifest_sha256']
    local_sources = previous[0]['local_source_documents']
    for row in local_sources:
        assert Path(row['path']).is_file() and digest(row['path']) == row['sha256']
    validation = strict_json(ROOT/'results/validation-v2/status.json')
    assert validation['state'] == 'complete' and len(validation['checks']) == 137 and all(row['passed'] for row in validation['checks'])
    assert validation['script_sha256'] == digest(ROOT/'validate_axial_v2.py')
    for relative, expected in validation['input_hashes'].items():
        assert digest(ROOT/relative) == expected, relative
    exact_count = sum(len(strict_json(ROOT/f'results/{name}/status.json')['checks'])
                      for name in ['derivation', 'matching', 'convention-crosswalk'])
    assert exact_count == 62
    script_hashes = {digest(path) for path in ROOT.glob('*.py')}
    parsed = []
    for path in sorted(ROOT.rglob('*.json')):
        report = strict_json(path)
        assert report['state'] == 'complete' and report['script_sha256'] in script_hashes, path
        parsed.append(path.relative_to(ROOT).as_posix())
    for name in ['coarse', 'fine']:
        old = strict_json(ROOT/f'results/{name}/status.json')
        new = strict_json(ROOT/f'results/{name}-v2/status.json')
        for first, second in zip(old['rows'], new['rows']):
            for key in ['response', 'response_over_alpha', 'geometric_sigma_bar', 'geometric_sigma_BV']:
                assert first[key] == second[key]
            assert first['k2B_radius_normalized'] == second['sigma_bar_over_R5']
            assert second['Cardoso_k2B_radius_normalized'] == 2*second['sigma_bar_over_R5']
    archives = []
    for path in sorted(ROOT.rglob('*.npz')):
        with np.load(path, allow_pickle=False) as arrays:
            assert all(np.all(np.isfinite(arrays[key])) for key in arrays.files)
        archives.append(path.relative_to(ROOT).as_posix())
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
    urls = ['https://arxiv.org/abs/1701.01116', 'https://doi.org/10.1103/PhysRevD.95.084014',
            'https://arxiv.org/abs/1504.06606', 'https://doi.org/10.1103/PhysRevD.91.104026',
            'https://arxiv.org/abs/1805.07266', 'https://doi.org/10.1103/PhysRevD.101.064003']
    assert all(url in prose for url in urls)
    compiled = []
    for path in sorted(ROOT.glob('*.py')):
        compile(path.read_bytes(), str(path), 'exec')
        compiled.append(path.name)
    assert not list(ROOT.rglob('__pycache__'))
    protected = POST.parent/'formalization-workbench'
    start = datetime(2026, 10, 4, 18, 19, 10, tzinfo=timezone.utc)
    changed = [str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime > start.timestamp()]
    assert protected.is_dir() and not changed, changed
    hashes = {path.relative_to(ROOT).as_posix(): digest(path) for path in sorted(ROOT.rglob('*')) if path.is_file() and path != OUTPUT}
    fine = strict_json(ROOT/'results/fine-v2/status.json')
    report = {'state': 'complete', 'sealed_at_utc': datetime.now(timezone.utc).isoformat(),
              'file_hashes': hashes, 'parent_seal_sha256': digest(seals[0]),
              'prior_sealed_entries_unchanged': prior_count, 'checkpoint_manifest_sha256': digest(manifest),
              'full_checkpoint_payload_rehashed': False, 'local_source_documents': local_sources,
              'required_paths': sorted(set(str(path.resolve()) for path in required)),
              'primary_source_urls_checked_2026_10_04_london': urls,
              'selected_source_pages_visually_inspected': ['Cardoso2017 PDFpages4,20,22',
                  'LandryPoisson2015 PDFpage7', 'BanihashemiVines2020 PDFpages6,7,8'],
              'parsed_json_files': parsed, 'compiled_scripts': compiled, 'finite_archives': archives,
              'validation_checks': 137, 'exact_checks': 62, 'authoritative_axial_profiles': 14,
              'legacy_labelled_profiles_preserved': 14, 'independent_authoritative_Riccati_profiles': 7,
              'new_background_solves': 0, 'reference_body_response': fine['rows'][-1]['response'],
              'reference_geometric_sigma_bar': fine['rows'][-1]['geometric_sigma_bar'],
              'reference_geometric_sigma_BV': fine['rows'][-1]['geometric_sigma_BV'],
              'static_scalar_axial_response_derived': True, 'weak_potential_moment_law_derived': True,
              'positive_static_uniqueness_proved_under_stated_conditions': True,
              'matched_conservative_magnetic_term_derived': True,
              'complete_combined_magnetic_radiation_balance_derived': False,
              'new_body_parameter_fitted': False, 'perfect_fluid_state_assumed': False,
              'factor_two_label_error_preserved_and_repaired': True,
              'observational_detection_or_physical_scale_claimed': False,
              'protected_workbench_recent_modified_file_count': len(changed),
              'protected_check_scope': 'Modification-time scan since18:19:10UTC on4October; not a full content-hash baseline.',
              'original_parent_or_bath_modified': False, 'github_action': False, 'subagents': 0,
              'one_below_normal_single_core_numerical_worker_at_a_time': True}
    OUTPUT.write_text(json.dumps(report, indent=2, allow_nan=False), encoding='utf-8')
    print(json.dumps({'state': 'complete', 'sealed_files': len(hashes), 'prior_unchanged': prior_count,
                      'validation_checks': 137, 'exact_checks': exact_count, 'protected_changes': len(changed),
                      'compiled_scripts': len(compiled)}))


if __name__ == '__main__':
    main()
