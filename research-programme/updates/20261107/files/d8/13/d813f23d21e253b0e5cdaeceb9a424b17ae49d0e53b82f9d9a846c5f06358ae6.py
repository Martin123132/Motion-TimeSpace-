from __future__ import annotations

import ast
from datetime import datetime, timezone
from pathlib import Path
import re

from common import ROOT, BRANCH, PARENT, digest, read_json, write_json, modest_process


def main():
    modest_process()
    post = BRANCH.parent
    output = ROOT/'results/stage-integrity.json'
    assert not output.exists()
    stage34 = BRANCH/'eccentric-polar-radiation-20261005'
    tree = ast.parse((stage34/'seal_waves.py').read_text(encoding='utf-8'))
    assignment = next(node for node in ast.walk(tree) if isinstance(node, ast.Assign) and
                      any(isinstance(target, ast.Name) and target.id == 'stages' for target in node.targets))
    stages = [PARENT.name, stage34.name]+ast.literal_eval(assignment.value)
    seals = [BRANCH/stage/'results/stage-integrity.json' for stage in stages]+[BRANCH/'results/stage-integrity.json']
    bases = [BRANCH/stage for stage in stages]+[post]
    keys = ['parent_seal_sha256']*29+['previous_seal_sha256']*2+['parent_seal_sha256']
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
    assert prior_count == 4267, prior_count
    manifest = post/'_checkpoints/20261003-pre-condensate-origin/manifest.json'
    assert digest(manifest) == prior[0]['checkpoint_manifest_sha256']
    assert digest(manifest) == '38f86719b0eb4c5e7fd86171a98af51918369f9daf81584a3c19c3d63222389e'
    for source in prior[0]['local_source_documents']:
        assert digest(source['path']) == source['sha256']
    validation = read_json(ROOT/'results/validation/status.json')
    assert validation['state'] == 'complete' and all(row['passed'] for row in validation['checks'])
    assert validation['script_sha256'] == digest(ROOT/'validate_inspiral.py')
    assert validation['exact_checks'] == 13 and validation['new_wave_mode_evaluations'] == 266
    for source in validation['primary_pdfs']:
        assert digest(source['path']) == source['sha256']
    script_hashes = {digest(path) for path in ROOT.glob('*.py')}
    for path in ROOT.rglob('*.json'):
        report = read_json(path)
        assert report['state'] == 'complete', path
        assert report['script_sha256'] in script_hashes, path
        for source, expected in report.get('input_hashes', {}).items():
            assert Path(source).is_file() and digest(source) == expected, (path, source)
    source_paths = [
        PARENT/'sidebands.py', PARENT/'analyze_limit.py',
        PARENT/'results/analytic-fine/status.json', PARENT/'results/analytic-coarse/status.json',
        PARENT/'results/tidal-limit/status.json', PARENT/'results/horizon-limit/status.json',
        PARENT/'results/stage-integrity.json',
        BRANCH/'dynamical-tides-20261004/results/mode-edge004/status.json',
        BRANCH/'retarded-response-20261004/18-retarded-tidal-response-residue-and-radiation-law.md',
        BRANCH/'orbital-backreaction-20261004/20-reciprocal-tidal-orbit-and-consistent-leading-inspiral.md']
    assert all(path.is_file() for path in source_paths)
    urls = set()
    for path in ROOT.glob('*.md'):
        urls.update(re.findall(r'https://[^\s]+', path.read_text(encoding='utf-8')))
    assert urls <= set(validation['source_urls']), urls-set(validation['source_urls'])
    assert not list(ROOT.rglob('__pycache__'))
    compiled = []
    for path in ROOT.glob('*.py'):
        compile(path.read_bytes(), str(path), 'exec')
        compiled.append(path.name)
    analysis = read_json(ROOT/'results/analysis/status.json')
    wave_adiabatic = max(abs(row['frequency_rate'])/row['frequency']**2 for row in analysis['adiabatic_diagnostics'])
    assert wave_adiabatic < .01
    protected = post.parent/'formalization-workbench'
    started = datetime(2026, 10, 5, 19, 31, 7, tzinfo=timezone.utc)
    changed = [str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime > started.timestamp()]
    assert protected.is_dir() and not changed, changed
    hashes = {path.relative_to(ROOT).as_posix(): digest(path) for path in sorted(ROOT.rglob('*')) if path.is_file() and path != output}
    report = dict(
        state='complete', sealed_at_utc=datetime.now(timezone.utc).isoformat(), file_hashes=hashes,
        parent_seal_sha256=digest(seals[0]), prior_sealed_entries_unchanged=prior_count,
        parent_chain_edges_verified=len(keys), checkpoint_manifest_sha256=digest(manifest),
        full_checkpoint_payload_rehashed=False, local_source_documents=prior[0]['local_source_documents'],
        primary_pdfs=validation['primary_pdfs'], source_urls=validation['source_urls'],
        local_dependencies={str(path): digest(path) for path in source_paths},
        validation_checks=len(validation['checks']), exact_checks=13, one_phase_bookkeeping_check_in_exact_count=True,
        compiled_scripts=compiled, new_wave_mode_evaluations=266, reused_endpoint_rows=28,
        new_static_or_background_solves=0, new_fitted_parameters=0,
        continuous_leading_adiabatic_trajectory_computed=True, same_source_BH_infinity_and_horizon_reference=True,
        timing_phase_eccentricity_order=0, eccentricity_squared_transport_linear=True,
        equal_time_and_equal_radius_phase_separately_computed=True,
        maximum_resolution_endpoint_error=validation['maximum_resolution_endpoint_error'],
        maximum_nested9_endpoint_error=validation['maximum_nested9_endpoint_error'],
        maximum_independent_gauss8_endpoint_error=validation['maximum_independent_gauss8_endpoint_error'],
        maximum_wave_frequency_adiabatic_indicator=wave_adiabatic,
        full_coupled_kernel_absolute_moments_bounded=False,
        arbitrary_initial_ringing_included=False,
        protected_workbench_recent_modified_file_count=len(changed),
        protected_check_scope='Modification-time scan since19:31:07UTC5October2026, not a full content-hash baseline.',
        inherited_Einstein_Hilbert_and_G_R_retained=True, original_parent_or_bath_modified=False,
        maximum_concurrent_numerical_workers=1, workers_below_normal_pinned_core2=True,
        github_action=False, subagents=0)
    write_json(output, report, exclusive=True)
    print(dict(state='complete', sealed_files=len(hashes), prior_entries_unchanged=prior_count,
               next_prior_count=prior_count+len(hashes), validation_checks=len(validation['checks']),
               protected_changes=len(changed), maximum_wave_adiabatic=wave_adiabatic), flush=True)


if __name__ == '__main__':
    main()

