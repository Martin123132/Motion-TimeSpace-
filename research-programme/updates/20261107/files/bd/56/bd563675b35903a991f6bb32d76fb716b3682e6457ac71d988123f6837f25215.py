from __future__ import annotations

from datetime import datetime, timezone
import json

import psutil

from validate_companion import ROOT, digest, read_json


def main():
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    branch = ROOT.parent
    post = branch.parent
    output = ROOT/'results/stage-integrity.json'
    assert not output.exists()
    stages = ['dynamical-axial-20261004', 'magnetic-balance-20261004', 'axial-tides-20261004', 'pn-balance-20261004',
              'orbital-backreaction-20261004', 'companion-source-20261004', 'retarded-response-20261004',
              'dynamical-tides-20261004', 'gravitating-tides-20261004', 'quadrupole-response-20261004',
              'collective-motion-20261004', 'fixed-theory-sequence-20261003', 'radial-pulsations-20261003',
              'radial-gravity-stability-20261003', 'self-gravity-20261003', 'finite-charge-20261003',
              'conserved-stress-20261003', 'ward-remainder-20261003', 'tensor-ward-20261003',
              'collective-operator-20261003', 'tensor-response-20261003']
    seals = [branch/stage/'results/stage-integrity.json' for stage in stages]+[branch/'results/stage-integrity.json']
    bases = [branch/stage for stage in stages]+[post]
    keys = ['parent_seal_sha256']*18+['previous_seal_sha256', 'previous_seal_sha256', 'parent_seal_sha256']
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
    assert prior_count == 1234, prior_count
    manifest = post/'_checkpoints/20261003-pre-condensate-origin/manifest.json'
    assert digest(manifest) == prior[0]['checkpoint_manifest_sha256']
    for source in prior[0]['local_source_documents']:
        assert digest(source['path']) == source['sha256']
    validation = read_json(ROOT/'results/validation/status.json')
    assert validation['state'] == 'complete' and all(row['passed'] for row in validation['checks'])
    assert validation['script_sha256'] == digest(ROOT/'validate_companion.py')
    for path, expected in validation['input_hashes'].items():
        assert digest(path) == expected, path
    scripts = {digest(path) for path in ROOT.glob('*.py')}
    for path in ROOT.rglob('*.json'):
        report = read_json(path)
        assert report['state'] == 'complete' and report['script_sha256'] in scripts, path
    assert not list(ROOT.rglob('__pycache__'))
    for path in ROOT.glob('*.py'):
        compile(path.read_bytes(), str(path), 'exec')
    protected = post.parent/'formalization-workbench'
    start = datetime(2026, 10, 4, 23, 8, 50, tzinfo=timezone.utc)
    changed = [str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime > start.timestamp()]
    assert protected.is_dir() and not changed, changed
    hashes = {path.relative_to(ROOT).as_posix(): digest(path) for path in sorted(ROOT.rglob('*')) if path.is_file() and path != output}
    report = {'state': 'complete', 'sealed_at_utc': datetime.now(timezone.utc).isoformat(),
              'file_hashes': hashes, 'parent_seal_sha256': digest(seals[0]), 'prior_sealed_entries_unchanged': prior_count,
              'checkpoint_manifest_sha256': digest(manifest), 'full_checkpoint_payload_rehashed': False,
              'local_source_documents': prior[0]['local_source_documents'],
              'validation_checks': len(validation['checks']), 'exact_checks': validation['exact_checks'],
              'compiled_scripts': validation['compiled_scripts'], 'source_urls': validation['source_urls'],
              'source_pages_visually_inspected': 'Martel-Poisson2005 PDFpages6,7,9,16',
              'conserved_test_companion_source_derived': True, 'metric_contact_term_derived': True,
              'outgoing_axial_power_and_same_mass_BH_baseline': True,
              'wide_orbit_stage23_test_mass_magnetic_flux_recovered': True,
              'first_relative_PN_magnetic_infinity_flux_coefficient': '173/84',
              'tail_coefficient_not_yet_derived_here': True, 'finite_mass_ratio_claimed': False,
              'reference_absorption_reported_separately': True,
              'roundoff_limited_rows': validation['roundoff_limited_remainder_rows'],
              'interval_arithmetic_or_total_waveform_error_bound_claimed': False,
              'new_body_coefficients_fitted': 0, 'new_background_solves': 0,
              'protected_workbench_recent_modified_file_count': len(changed),
              'protected_check_scope': 'Modification-time scan since23:08:50UTC on4October; not a full content-hash baseline.',
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
