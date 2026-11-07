from __future__ import annotations

import ast
from datetime import datetime, timezone
from pathlib import Path
import re

from sidebands import ROOT, BRANCH, digest, read_json, write_json, modest_process


def main():
    modest_process()
    post = BRANCH.parent
    output = ROOT/'results/stage-integrity.json'
    assert not output.exists()
    parent_root = BRANCH/'eccentric-polar-radiation-20261005'
    tree = ast.parse((parent_root/'seal_waves.py').read_text(encoding='utf-8'))
    assignment = next(node for node in ast.walk(tree) if isinstance(node, ast.Assign)
                      and any(isinstance(target, ast.Name) and target.id == 'stages' for target in node.targets))
    stages = [parent_root.name]+ast.literal_eval(assignment.value)
    seals = [BRANCH/stage/'results/stage-integrity.json' for stage in stages]+[BRANCH/'results/stage-integrity.json']
    bases = [BRANCH/stage for stage in stages]+[post]
    keys = ['parent_seal_sha256']*28+['previous_seal_sha256']*2+['parent_seal_sha256']
    prior = []
    for seal, base in zip(seals, bases):
        report = read_json(seal)
        assert report['state'] == 'complete', seal
        for relative, expected in report['file_hashes'].items():
            assert digest(base/relative) == expected, base/relative
        prior.append(report)
    assert len(keys) == len(seals)-1
    for index, key in enumerate(keys):
        assert prior[index][key] == digest(seals[index+1]), seals[index]
    prior_count = sum(len(report['file_hashes']) for report in prior)
    assert prior_count == 3988, prior_count
    manifest = post/'_checkpoints/20261003-pre-condensate-origin/manifest.json'
    assert digest(manifest) == prior[0]['checkpoint_manifest_sha256']
    assert digest(manifest) == '38f86719b0eb4c5e7fd86171a98af51918369f9daf81584a3c19c3d63222389e'
    for source in prior[0]['local_source_documents']:
        assert digest(source['path']) == source['sha256']
    validation = read_json(ROOT/'results/validation/status.json')
    assert validation['state'] == 'complete' and all(row['passed'] for row in validation['checks'])
    assert validation['script_sha256'] == digest(ROOT/'validate_limit.py')
    assert validation['exact_checks'] == 30 and validation['wave_mode_evaluations'] == 242
    for source in validation['primary_pdfs']:
        assert digest(source['path']) == source['sha256']
    script_hashes = {digest(path) for path in ROOT.glob('*.py')}
    for path in ROOT.rglob('*.json'):
        report = read_json(path)
        assert report['state'] == 'complete', path
        assert report['script_sha256'] in script_hashes, path
        for source, expected in report.get('input_hashes', {}).items():
            assert Path(source).is_file() and digest(source) == expected, (path, source)
    local_sources = [
        'eccentric-polar-radiation-20261005/results/stage-integrity.json',
        'eccentric-polar-radiation-20261005/validate_waves.py',
        'eccentric-polar-radiation-20261005/analyze_waves.py',
        'eccentric-polar-source-20261005/polar_source.py',
        'eccentric-source-20261005/eccentric_source.py',
        'secular-actions-20261005/secular.py',
        'secular-actions-20261005/run_small_e.py',
        'secular-actions-20261005/results/small-e-fine/status.json',
        'secular-actions-20261005/results/small-e-coarse/status.json',
        'companion-source-20261004/companion_system.py',
        'companion-source-20261004/results/fine/status.json',
        'companion-source-20261004/sources/provenance.json',
        'eccentric-radiation-20261005/eccentric_radiation.py',
        'eccentric-radiation-20261005/results/fine/status.json',
        'retarded-response-20261004/response_system_v3.py',
        'retarded-response-20261004/response_system_v2.py',
        'orbital-backreaction-20261004/20-reciprocal-tidal-orbit-and-consistent-leading-inspiral.md',
        'self-gravity-20261003/results/fine/R20-C0p03.npz']
    assert all((BRANCH/path).is_file() for path in local_sources)
    document_urls = set()
    for path in ROOT.glob('*.md'):
        document_urls.update(re.findall(r'https://[^\s]+', path.read_text(encoding='utf-8')))
    assert document_urls <= set(validation['source_urls']), document_urls-set(validation['source_urls'])
    assert not list(ROOT.rglob('__pycache__'))
    compiled = []
    for path in ROOT.glob('*.py'):
        compile(path.read_bytes(), str(path), 'exec')
        compiled.append(path.name)
    protected = post.parent/'formalization-workbench'
    started = datetime(2026, 10, 5, 18, 56, 37, tzinfo=timezone.utc)
    changed = [str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime > started.timestamp()]
    assert protected.is_dir() and not changed, changed
    hashes = {path.relative_to(ROOT).as_posix(): digest(path) for path in sorted(ROOT.rglob('*')) if path.is_file() and path != output}
    report = dict(
        state='complete', sealed_at_utc=datetime.now(timezone.utc).isoformat(), file_hashes=hashes,
        parent_seal_sha256=digest(seals[0]), prior_sealed_entries_unchanged=prior_count,
        parent_chain_edges_verified=len(keys), checkpoint_manifest_sha256=digest(manifest),
        full_checkpoint_payload_rehashed=False, local_source_documents=prior[0]['local_source_documents'],
        primary_pdfs=validation['primary_pdfs'], source_urls=validation['source_urls'],
        local_dependencies={path: digest(BRANCH/path) for path in local_sources},
        validation_checks=len(validation['checks']), exact_checks=30, compiled_scripts=compiled,
        new_wave_mode_evaluations=242, inherited_odd_mode_rows=102, new_static_or_background_solves=0,
        new_fitted_parameters=0, analytic_first_sidebands_derived=True,
        analytic_near_circular_action_law_derived=True, outgoing_tidal_coefficient='459/19',
        horizon_absorption_coefficient='54/19', distinct_asymptotic_powers_retained=True,
        same_source_BH_infinity_and_horizon_reference=True, continuous_inspiral_computed=False,
        maximum_damping_refinement=validation['maximum_damping_refinement'],
        maximum_small_pair_damping_error=validation['maximum_small_pair_damping_error'],
        maximum_amplitude_extrapolation_error=validation['maximum_amplitude_extrapolation_error'],
        inherited_finite_odd_archive_has_full_interior=False,
        protected_workbench_recent_modified_file_count=len(changed),
        protected_check_scope='Modification-time scan since18:56:37UTC5October2026, not a full content-hash baseline.',
        inherited_Einstein_Hilbert_and_G_R_retained=True, original_parent_or_bath_modified=False,
        maximum_concurrent_numerical_workers=2, workers_below_normal_pinned_core2=True,
        github_action=False, subagents=0)
    write_json(output, report, exclusive=True)
    print(dict(state='complete', sealed_files=len(hashes), prior_entries_unchanged=prior_count,
               next_prior_count=prior_count+len(hashes), validation_checks=len(validation['checks']),
               protected_changes=len(changed)), flush=True)


if __name__ == '__main__':
    main()

