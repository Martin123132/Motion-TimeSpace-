from __future__ import annotations

from datetime import datetime, timezone
import json

from common import BRANCH, ROOT, configure_worker, digest, read_json, write_new_json


def main():
    configure_worker()
    output = ROOT/'results/stage-integrity.json'
    assert not output.exists()
    post = BRANCH.parent
    stages = ['axial-tides-20261004', 'pn-balance-20261004', 'orbital-backreaction-20261004',
              'companion-source-20261004', 'retarded-response-20261004', 'dynamical-tides-20261004',
              'gravitating-tides-20261004', 'quadrupole-response-20261004', 'collective-motion-20261004',
              'fixed-theory-sequence-20261003', 'radial-pulsations-20261003', 'radial-gravity-stability-20261003',
              'self-gravity-20261003', 'finite-charge-20261003', 'conserved-stress-20261003',
              'ward-remainder-20261003', 'tensor-ward-20261003', 'collective-operator-20261003',
              'tensor-response-20261003']
    seals = [BRANCH/stage/'results/stage-integrity.json' for stage in stages]+[BRANCH/'results/stage-integrity.json']
    bases = [BRANCH/stage for stage in stages]+[post]
    keys = ['parent_seal_sha256']*16+['previous_seal_sha256', 'previous_seal_sha256', 'parent_seal_sha256']
    prior = []
    for seal, base in zip(seals, bases):
        report = read_json(seal)
        assert report['state'] == 'complete', seal
        for relative, expected in report['file_hashes'].items():
            assert digest(base/relative) == expected, base/relative
        prior.append(report)
    assert len(keys) == len(seals)-1
    for index, key in enumerate(keys):
        assert prior[index][key] == digest(seals[index+1])
    prior_count = sum(len(report['file_hashes']) for report in prior)
    assert prior_count == 1188, prior_count
    manifest = post/'_checkpoints/20261003-pre-condensate-origin/manifest.json'
    assert digest(manifest) == prior[0]['checkpoint_manifest_sha256']
    for source in prior[0]['local_source_documents']:
        assert digest(source['path']) == source['sha256']
    validation = read_json(ROOT/'results/validation/status.json')
    assert validation['state'] == 'complete' and all(row['passed'] for row in validation['checks'])
    assert digest(ROOT/'validate_balance.py') == validation['script_sha256']
    assert digest(ROOT/'common.py') == validation['common_sha256']
    for source, expected in validation['input_hashes'].items():
        assert digest(source) == expected, source
    for source in read_json(ROOT/'sources/provenance.json')['sources']:
        assert digest(source['path']) == source['sha256']
    scripts = {digest(path) for path in ROOT.glob('*.py')}
    for path in ROOT.rglob('*.json'):
        report = read_json(path)
        assert report['state'] == 'complete' and report['script_sha256'] in scripts, path
    for path in ROOT.glob('*.py'):
        compile(path.read_bytes(), str(path), 'exec')
    assert not list(ROOT.rglob('__pycache__'))
    protected = post.parent/'formalization-workbench'
    start = datetime(2026, 10, 4, 19, 47, 10, tzinfo=timezone.utc)
    changed = [str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime > start.timestamp()]
    assert protected.is_dir() and not changed, changed
    hashes = {path.relative_to(ROOT).as_posix(): digest(path) for path in sorted(ROOT.rglob('*')) if path.is_file() and path != output}
    evaluation = read_json(ROOT/'results/evaluation/status.json')
    report = {'state': 'complete', 'sealed_at_utc': datetime.now(timezone.utc).isoformat(),
              'file_hashes': hashes, 'parent_seal_sha256': digest(seals[0]), 'prior_sealed_entries_unchanged': prior_count,
              'checkpoint_manifest_sha256': digest(manifest), 'full_checkpoint_payload_rehashed': False,
              'local_source_documents': prior[0]['local_source_documents'],
              'validation_checks': len(validation['checks']), 'constituent_check_counts': validation['constituent_check_counts'],
              'compiled_scripts': validation['compiled_scripts'], 'csv_counts': validation['csv_counts'],
              'primary_source_urls': validation['primary_source_urls'],
              'selected_source_pages_visually_inspected': ['BanihashemiVines2020 PDFpages9,10'],
              'body_response_coefficients': evaluation['body'],
              'generic_current_source_multipoles_reduced': True,
              'leading_combined_electric_magnetic_instantaneous_balance_derived': True,
              'magnetic_zero_recovers_electric_parent_exactly': True,
              'mass_ratio_dependent_magnetic_sign_derived': True,
              'dynamical_axial_response_is_next_target': True,
              'inherited_Einstein_Hilbert_and_G_R_retained': True,
              'new_body_coefficient_fits': 0, 'new_background_solves': 0,
              'failed_normalization_gate_preserved_and_corrected': True,
              'astrophysical_scale_or_observational_detection_claimed': False,
              'higher_order_waveform_error_bound_claimed': False,
              'protected_workbench_recent_modified_file_count': len(changed),
              'protected_check_scope': 'Modification-time scan since19:47:10UTC on4October; not a full content-hash baseline.',
              'original_parent_or_bath_modified': False, 'github_action': False, 'subagents': 0,
              'one_below_normal_single_core_numerical_worker_at_a_time': True}
    write_new_json(output, report)
    print(json.dumps({'state': 'complete', 'sealed_files': len(hashes), 'prior_entries_unchanged': prior_count,
                      'validation_checks': len(validation['checks']), 'constituent_checks': validation['constituent_check_counts'],
                      'protected_changes': len(changed)}))


if __name__ == '__main__':
    main()
