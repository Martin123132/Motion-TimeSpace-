from __future__ import annotations

from datetime import datetime, timezone
import json

from eccentric_source import ROOT, digest, modest_process
from validate_eccentric import read_json


def main():
    modest_process()
    branch, post = ROOT.parent, ROOT.parent.parent
    output = ROOT/'results/stage-integrity.json'
    assert not output.exists()
    stages = ['causal-exterior-20261005', 'causal-axial-20261005', 'axial-reciprocity-20261005',
              'axial-tail-balance-20261005', 'axial-companion-20261005', 'dynamical-axial-20261004',
              'magnetic-balance-20261004', 'axial-tides-20261004', 'pn-balance-20261004',
              'orbital-backreaction-20261004', 'companion-source-20261004', 'retarded-response-20261004',
              'dynamical-tides-20261004', 'gravitating-tides-20261004', 'quadrupole-response-20261004',
              'collective-motion-20261004', 'fixed-theory-sequence-20261003', 'radial-pulsations-20261003',
              'radial-gravity-stability-20261003', 'self-gravity-20261003', 'finite-charge-20261003',
              'conserved-stress-20261003', 'ward-remainder-20261003', 'tensor-ward-20261003',
              'collective-operator-20261003', 'tensor-response-20261003']
    seals = [branch/stage/'results/stage-integrity.json' for stage in stages]+[branch/'results/stage-integrity.json']
    bases = [branch/stage for stage in stages]+[post]
    keys = ['parent_seal_sha256']*23+['previous_seal_sha256']*2+['parent_seal_sha256']
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
    assert prior_count == 1408, prior_count
    manifest = post/'_checkpoints/20261003-pre-condensate-origin/manifest.json'
    assert digest(manifest) == prior[0]['checkpoint_manifest_sha256']
    assert digest(manifest) == '38f86719b0eb4c5e7fd86171a98af51918369f9daf81584a3c19c3d63222389e'
    for source in prior[0]['local_source_documents']:
        assert digest(source['path']) == source['sha256']
    validation = read_json(ROOT/'results/validation/status.json')
    assert validation['state'] == 'complete' and all(row['passed'] for row in validation['checks'])
    assert validation['script_sha256'] == digest(ROOT/'validate_eccentric.py')
    assert len(validation['checks']) == 183 and validation['exact_checks'] == 37
    for source, expected in validation['input_hashes'].items():
        assert digest(source) == expected, source
    script_hashes = {digest(path) for path in ROOT.glob('*.py')}
    for path in ROOT.rglob('*.json'):
        report = read_json(path)
        assert report['state'] == 'complete', path
        assert report['script_sha256'] in script_hashes, path
        for source, expected in report.get('input_hashes', {}).items():
            assert digest(source) == expected, (path, source)
    assert not list(ROOT.rglob('__pycache__'))
    compiled = []
    for path in ROOT.rglob('*.py'):
        compile(path.read_bytes(), str(path), 'exec')
        compiled.append(path.relative_to(ROOT).as_posix())
    protected = post.parent/'formalization-workbench'
    start = datetime(2026, 10, 5, 1, 55, 44, tzinfo=timezone.utc)
    changed = [str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime > start.timestamp()]
    assert protected.is_dir() and not changed, changed
    hashes = {path.relative_to(ROOT).as_posix(): digest(path) for path in sorted(ROOT.rglob('*'))
              if path.is_file() and path != output}
    report = {'state': 'complete', 'sealed_at_utc': datetime.now(timezone.utc).isoformat(),
              'file_hashes': hashes, 'parent_seal_sha256': digest(seals[0]),
              'prior_sealed_entries_unchanged': prior_count,
              'checkpoint_manifest_sha256': digest(manifest), 'full_checkpoint_payload_rehashed': False,
              'local_source_documents': prior[0]['local_source_documents'],
              'source_urls': validation['source_urls'], 'web_source_verified_utc_date': '2026-10-05',
              'validation_checks': len(validation['checks']), 'exact_checks': validation['exact_checks'],
              'accepted_run_checks': validation['accepted_run_checks'], 'compiled_scripts': compiled,
              'complete_conserved_test_geodesic_source_derived': True,
              'moving_source_jumps_and_both_metric_contacts_derived': True,
              'worldline_metric_pullback_continuity_and_smooth_difference': True,
              'acceleration_free_Fourier_source_and_stable_wave_amplitude_difference_derived': True,
              'circular_regression_against_original_source': True,
              'eccentricities_checked': [0., .3, .6],
              'maximum_fine_independent_geodesic_scaled_error': validation['maximum_fine_independent_geodesic_scaled_error'],
              'maximum_scaled_kernel_refinement': validation['maximum_scaled_kernel_refinement'],
              'maximum_fine_scaled_weak_source_identity_error': validation['maximum_fine_scaled_weak_source_identity_error'],
              'first_attempt_test_design_repair_retained': True,
              'radial_probe_tests_are_not_wave_amplitudes': True,
              'eccentric_radiation_flux_or_self_force_computed': False,
              'new_background_solves': 0, 'new_fitted_response_parameters': 0,
              'protected_workbench_recent_modified_file_count': len(changed),
              'protected_check_scope': 'Modification-time scan since01:55:44UTC5October2026, not a full content-hash baseline.',
              'inherited_Einstein_Hilbert_and_G_R_retained': True,
              'original_parent_or_bath_modified': False, 'github_action': False, 'subagents': 0,
              'one_below_normal_single_core_numerical_worker_at_a_time': True}
    with output.open('x', encoding='utf-8') as handle:
        json.dump(report, handle, indent=2, allow_nan=False)
    print(json.dumps({'state': 'complete', 'sealed_files': len(hashes), 'prior_entries_unchanged': prior_count,
                      'validation_checks': len(validation['checks']), 'exact_checks': validation['exact_checks'],
                      'protected_changes': len(changed)}))


if __name__ == '__main__':
    main()
