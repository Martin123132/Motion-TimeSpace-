from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path

import psutil

from validate_action import ROOT, digest, read_json


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    branch, post = ROOT.parent, ROOT.parent.parent
    output = ROOT/'results/stage-integrity.json'
    assert not output.exists()
    stages = ['axial-tail-balance-20261005', 'axial-companion-20261005', 'dynamical-axial-20261004',
              'magnetic-balance-20261004', 'axial-tides-20261004', 'pn-balance-20261004',
              'orbital-backreaction-20261004', 'companion-source-20261004', 'retarded-response-20261004',
              'dynamical-tides-20261004', 'gravitating-tides-20261004', 'quadrupole-response-20261004',
              'collective-motion-20261004', 'fixed-theory-sequence-20261003', 'radial-pulsations-20261003',
              'radial-gravity-stability-20261003', 'self-gravity-20261003', 'finite-charge-20261003',
              'conserved-stress-20261003', 'ward-remainder-20261003', 'tensor-ward-20261003',
              'collective-operator-20261003', 'tensor-response-20261003']
    seals = [branch/stage/'results/stage-integrity.json' for stage in stages]+[branch/'results/stage-integrity.json']
    bases = [branch/stage for stage in stages]+[post]
    keys = ['parent_seal_sha256']*20+['previous_seal_sha256']*2+['parent_seal_sha256']
    prior = []
    for seal, base in zip(seals, bases):
        report = read_json(seal)
        assert report['state'] == 'complete'
        for relative, expected in report['file_hashes'].items():
            assert digest(base/relative) == expected, base/relative
        prior.append(report)
    assert len(keys) == len(seals)-1
    for index, key in enumerate(keys):
        assert prior[index][key] == digest(seals[index+1])
    prior_count = sum(len(report['file_hashes']) for report in prior)
    assert prior_count == 1292, prior_count
    manifest = post/'_checkpoints/20261003-pre-condensate-origin/manifest.json'
    assert digest(manifest) == prior[0]['checkpoint_manifest_sha256']
    for source in prior[0]['local_source_documents']:
        assert digest(source['path']) == source['sha256']
    validation = read_json(ROOT/'results/validation/status.json')
    assert validation['state'] == 'complete' and all(row['passed'] for row in validation['checks'])
    assert validation['script_sha256'] == digest(ROOT/'validate_action.py')
    for path, expected in validation['input_hashes'].items():
        assert digest(path) == expected, path
    script_hashes = {digest(path) for path in ROOT.rglob('*.py')}
    for path in ROOT.rglob('*.json'):
        report = read_json(path)
        assert report['state'] == 'complete' and report['script_sha256'] in script_hashes, path
        for source, expected in report.get('input_hashes', {}).items():
            actual = Path(source)
            if path in [ROOT/'results/coarse/status.json', ROOT/'results/fine/status.json'] and actual == ROOT/'axial_action.py':
                actual = ROOT/'diagnostics/phase-normalization-v1/axial_action.py'
            assert digest(actual) == expected, (path, actual)
    assert not list(ROOT.rglob('__pycache__'))
    compiled = []
    for path in ROOT.rglob('*.py'):
        compile(path.read_bytes(), str(path), 'exec')
        compiled.append(path.relative_to(ROOT).as_posix())
    protected = post.parent/'formalization-workbench'
    start = datetime(2026, 10, 4, 23, 57, 42, tzinfo=timezone.utc)
    changed = [str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime > start.timestamp()]
    assert protected.is_dir() and not changed, changed
    hashes = {path.relative_to(ROOT).as_posix(): digest(path) for path in sorted(ROOT.rglob('*')) if path.is_file() and path != output}
    report = {'state': 'complete', 'sealed_at_utc': datetime.now(timezone.utc).isoformat(),
              'file_hashes': hashes, 'parent_seal_sha256': digest(seals[0]), 'prior_sealed_entries_unchanged': prior_count,
              'checkpoint_manifest_sha256': digest(manifest), 'full_checkpoint_payload_rehashed': False,
              'local_source_documents': prior[0]['local_source_documents'],
              'validation_checks': len(validation['checks']), 'exact_checks': validation['exact_checks'],
              'compiled_scripts': compiled, 'source_urls': validation['source_urls'],
              'source_pages_visually_inspected': 'Banihashemi-Vines2020 PDF pages8-9, Eqs36 and41',
              'reciprocal_axial_source_action_derived': True,
              'leading_magnetic_action_recovered_without_fitting': '6*sigma_bar*mu^2*Omega^2/D^4',
              'conservative_circular_charges_derived': True,
              'first_relative_PN_coefficients': {'action': '16/3', 'energy': '208/33', 'angular_momentum': '128/21'},
              'source_work_identity': '2*Omega*Im(F_ret)=DeltaP_infinity-P_BH_horizon',
              'surface_phase_normalization_defect_fixed_in_new_daughter_only': True,
              'rejected_candidates_preserved': validation['rejected_candidates'],
              'corrected_wave_count': validation['corrected_wave_count'],
              'maximum_optical_identity_error': validation['maximum_optical_identity_error'],
              'maximum_wave_settings_difference': validation['maximum_wave_settings_difference'],
              'maximum_charge_settings_difference': validation['maximum_charge_settings_difference'],
              'maximum_charge_step_difference': validation['maximum_charge_step_difference'],
              'full_waveform_or_arbitrary_mass_ratio_completion_claimed': False,
              'new_body_coefficients_fitted': 0, 'new_background_solves': 0,
              'protected_workbench_recent_modified_file_count': len(changed),
              'protected_check_scope': 'Modification-time scan since23:57:42UTC4October2026; not a full content-hash baseline.',
              'inherited_Einstein_Hilbert_and_G_R_retained': True,
              'original_parent_or_bath_modified': False, 'github_action': False, 'subagents': 0,
              'one_below_normal_single_core_numerical_worker_at_a_time': True}
    with output.open('x', encoding='utf-8') as handle:
        json.dump(report, handle, indent=2, allow_nan=False)
    print(json.dumps({'state': 'complete', 'sealed_files': len(hashes), 'prior_entries_unchanged': prior_count,
                      'validation_checks': len(validation['checks']), 'exact_checks': validation['exact_checks'], 'protected_changes': len(changed)}))


if __name__ == '__main__':
    main()
