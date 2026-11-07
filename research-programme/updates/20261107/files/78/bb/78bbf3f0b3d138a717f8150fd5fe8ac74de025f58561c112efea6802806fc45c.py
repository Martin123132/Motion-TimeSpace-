from __future__ import annotations

from datetime import datetime, timezone
import json
from pathlib import Path

from secular import ROOT, BRANCH, PARENT, digest, read_json, modest_process


def main():
    modest_process()
    post = BRANCH.parent
    output = ROOT/'results/stage-integrity.json'
    assert not output.exists()
    stages = ['eccentric-radiation-20261005', 'eccentric-source-20261005', 'causal-exterior-20261005',
              'causal-axial-20261005', 'axial-reciprocity-20261005', 'axial-tail-balance-20261005',
              'axial-companion-20261005', 'dynamical-axial-20261004', 'magnetic-balance-20261004',
              'axial-tides-20261004', 'pn-balance-20261004', 'orbital-backreaction-20261004',
              'companion-source-20261004', 'retarded-response-20261004', 'dynamical-tides-20261004',
              'gravitating-tides-20261004', 'quadrupole-response-20261004', 'collective-motion-20261004',
              'fixed-theory-sequence-20261003', 'radial-pulsations-20261003', 'radial-gravity-stability-20261003',
              'self-gravity-20261003', 'finite-charge-20261003', 'conserved-stress-20261003',
              'ward-remainder-20261003', 'tensor-ward-20261003', 'collective-operator-20261003', 'tensor-response-20261003']
    seals = [BRANCH/stage/'results/stage-integrity.json' for stage in stages]+[BRANCH/'results/stage-integrity.json']
    bases = [BRANCH/stage for stage in stages]+[post]
    keys = ['parent_seal_sha256']*25+['previous_seal_sha256']*2+['parent_seal_sha256']
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
    assert prior_count == 1512, prior_count
    manifest = post/'_checkpoints/20261003-pre-condensate-origin/manifest.json'
    assert digest(manifest) == prior[0]['checkpoint_manifest_sha256']
    assert digest(manifest) == '38f86719b0eb4c5e7fd86171a98af51918369f9daf81584a3c19c3d63222389e'
    for source in prior[0]['local_source_documents']:
        assert digest(source['path']) == source['sha256']
    validation = read_json(ROOT/'results/validation/status.json')
    physical = read_json(ROOT/'results/physical-limits/status.json')
    assert len(validation['checks']) == 481 and len(physical['checks']) == 36
    assert all(row['passed'] for row in validation['checks']+physical['checks'])
    assert validation['exact_checks'] == 17
    script_hashes = {digest(path) for path in ROOT.glob('*.py')}
    for path in ROOT.rglob('*.json'):
        report = read_json(path)
        assert report['state'] == 'complete', path
        assert report['script_sha256'] in script_hashes, path
        for source, expected in report.get('input_hashes', {}).items():
            assert Path(source).is_file() and digest(source) == expected, (path, source)
    assert not list(ROOT.rglob('__pycache__'))
    compiled = []
    for path in ROOT.rglob('*.py'):
        compile(path.read_bytes(), str(path), 'exec')
        compiled.append(path.relative_to(ROOT).as_posix())
    protected = post.parent/'formalization-workbench'
    started = datetime(2026, 10, 5, 3, 24, 22, tzinfo=timezone.utc)
    changed = [str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime > started.timestamp()]
    assert protected.is_dir() and not changed, changed
    hashes = {path.relative_to(ROOT).as_posix(): digest(path) for path in sorted(ROOT.rglob('*'))
              if path.is_file() and path != output}
    report = {'state': 'complete', 'sealed_at_utc': datetime.now(timezone.utc).isoformat(),
              'file_hashes': hashes, 'parent_seal_sha256': digest(seals[0]),
              'prior_sealed_entries_unchanged': prior_count, 'parent_chain_edges_verified': len(keys),
              'checkpoint_manifest_sha256': digest(manifest), 'full_checkpoint_payload_rehashed': False,
              'local_source_documents': prior[0]['local_source_documents'],
              'source_urls': validation['source_urls'], 'web_verified_utc_date': '2026-10-05',
              'validation_checks': len(validation['checks'])+len(physical['checks']), 'exact_checks': 17,
              'compiled_scripts': compiled, 'sector': 'odd ell2 m+/-1 only',
              'two_action_secular_response_derived_and_evaluated': True,
              'regular_circular_limit_derived': True, 'new_small_e_mode_evaluations': 102,
              'maximum_concurrent_numerical_workers': 1, 'workers_below_normal_pinned_core2': True,
              'new_background_solves': 0, 'new_fitted_response_parameters': 0,
              'circular_limit_numerical_extrapolation_is_not_a_fitted_response_parameter': True,
              'full_orbital_evolution_integrated': False, 'infinite_harmonic_tail_certified': False,
              'comparison_maxima': validation['comparison_maxima'],
              'maximum_high_precision_action_derivative_error': validation['maximum_high_precision_action_derivative_error'],
              'protected_workbench_recent_modified_file_count': len(changed),
              'protected_check_scope': 'Modification-time scan since03:24:22UTC5October2026, not a full content-hash baseline.',
              'inherited_Einstein_Hilbert_and_G_R_retained': True,
              'original_parent_or_bath_modified': False, 'github_action': False, 'subagents': 0}
    with output.open('x', encoding='utf-8') as handle:
        json.dump(report, handle, indent=2, allow_nan=False)
    print(json.dumps({'state': 'complete', 'sealed_files': len(hashes), 'prior_entries_unchanged': prior_count,
                      'next_prior_count': prior_count+len(hashes), 'validation_checks': report['validation_checks'],
                      'exact_checks': 17, 'protected_changes': len(changed)}))


if __name__ == '__main__':
    main()
