from __future__ import annotations

import ast
import csv
from datetime import datetime, timezone
from pathlib import Path
import re

from conservative import ROOT, BRANCH, PARENT, digest, read_json, write_json, modest_process


def main():
    modest_process()
    output = ROOT/'results/stage-integrity.json'
    assert not output.exists()
    post = BRANCH.parent
    stage34 = BRANCH/'eccentric-polar-radiation-20261005'
    tree = ast.parse((stage34/'seal_waves.py').read_text(encoding='utf-8'))
    assignment = next(node for node in ast.walk(tree) if isinstance(node, ast.Assign) and
                      any(isinstance(target, ast.Name) and target.id == 'stages' for target in node.targets))
    stages = [PARENT.name, 'near-circular-inspiral-20261005', 'near-circular-quadrupole-20261005', stage34.name]+ast.literal_eval(assignment.value)
    seals = [BRANCH/stage/'results/stage-integrity.json' for stage in stages]+[BRANCH/'results/stage-integrity.json']
    bases = [BRANCH/stage for stage in stages]+[post]
    prior = []
    for seal, base in zip(seals, bases):
        report = read_json(seal)
        assert report['state'] == 'complete'
        for relative, expected in report['file_hashes'].items():
            assert digest(base/relative) == expected, base/relative
        prior.append(report)
    for index, report in enumerate(prior[:-1]):
        link_keys = [key for key in ['parent_seal_sha256', 'previous_seal_sha256']
                     if report.get(key) == digest(seals[index+1])]
        assert len(link_keys) == 1, seals[index]
    prior_count = sum(len(report['file_hashes']) for report in prior)
    assert prior_count == 5069, prior_count
    manifest = post/'_checkpoints/20261003-pre-condensate-origin/manifest.json'
    assert digest(manifest) == prior[0]['checkpoint_manifest_sha256']
    assert digest(manifest) == '38f86719b0eb4c5e7fd86171a98af51918369f9daf81584a3c19c3d63222389e'
    for source in prior[0]['local_source_documents']:
        assert digest(source['path']) == source['sha256']
    validation = read_json(ROOT/'results/validation/status.json')
    assert validation['state'] == 'complete' and all(row['passed'] for row in validation['checks'])
    assert validation['script_sha256'] == digest(ROOT/'validate_action.py')
    assert validation['exact_checks'] == 22 and len(validation['checks']) == 1118
    for source in validation['primary_pdfs']:
        assert digest(source['path']) == source['sha256']
    script_hashes = {digest(path) for path in ROOT.glob('*.py')}
    for path in ROOT.rglob('*.json'):
        report = read_json(path)
        assert report['state'] == 'complete', path
        assert report['script_sha256'] in script_hashes, path
        for source, expected in report.get('input_hashes', {}).items():
            assert Path(source).is_file() and digest(source) == expected, (path, source)
    for path in ROOT.rglob('*.csv'):
        with path.open(newline='', encoding='utf-8') as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)
            assert rows and len(set(reader.fieldnames)) == len(reader.fieldnames)
            assert all(None not in row and None not in row.values() for row in rows)
    paths = [PARENT/'carrier.py', PARENT/'results/stage-integrity.json',
        BRANCH/'near-circular-quadrupole-20261005/sidebands.py',
        BRANCH/'near-circular-quadrupole-20261005/results/finite-fine/status.json',
        BRANCH/'near-circular-quadrupole-20261005/results/finite-coarse/status.json',
        BRANCH/'near-circular-inspiral-20261005/results/nodes-fine/status.json',
        BRANCH/'near-circular-inspiral-20261005/results/nodes-coarse/status.json',
        BRANCH/'secular-actions-20261005/results/small-e-fine/status.json',
        BRANCH/'secular-actions-20261005/results/small-e-coarse/status.json',
        BRANCH/'eccentric-polar-source-20261005/polar_source.py',
        BRANCH/'secular-actions-20261005/secular.py',
        BRANCH/'orbital-backreaction-20261004/20-reciprocal-tidal-orbit-and-consistent-leading-inspiral.md',
        BRANCH/'orbital-backreaction-20261004/results/fine/status.json',
        BRANCH/'orbital-backreaction-20261004/sources/fujita-et-al-2017.pdf']
    assert all(path.is_file() for path in paths)
    urls = set()
    for path in ROOT.glob('*.md'):
        urls.update(re.findall(r'https://[^\s]+', path.read_text(encoding='utf-8')))
    assert urls <= set(validation['source_urls']), urls-set(validation['source_urls'])
    assert not list(ROOT.rglob('__pycache__'))
    compiled = []
    for path in ROOT.glob('*.py'):
        compile(path.read_bytes(), str(path), 'exec')
        compiled.append(path.name)
    protected = post.parent/'formalization-workbench'
    started = datetime(2026, 10, 5, 22, 52, 0, tzinfo=timezone.utc)
    changed = [str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime > started.timestamp()]
    assert protected.is_dir() and not changed, changed
    hashes = {path.relative_to(ROOT).as_posix():digest(path) for path in sorted(ROOT.rglob('*')) if path.is_file() and path != output}
    report = dict(state='complete', sealed_at_utc=datetime.now(timezone.utc).isoformat(), file_hashes=hashes,
        parent_seal_sha256=digest(seals[0]), prior_sealed_entries_unchanged=prior_count,
        parent_chain_edges_verified=len(seals)-1, checkpoint_manifest_sha256=digest(manifest),
        full_checkpoint_payload_rehashed=False, local_source_documents=prior[0]['local_source_documents'],
        local_dependencies={str(path):digest(path) for path in paths}, primary_pdfs=validation['primary_pdfs'],
        source_urls=validation['source_urls'], validation_checks=len(validation['checks']), exact_checks=22,
        compiled_scripts=compiled, new_static_interior_solves=2, new_circular_wave_evaluations=48,
        new_background_solves=0, new_fitted_parameters=0, new_observational_data=False,
        conservative_action_e_squared_derived=True, nonradiative_static_tide_included=True,
        canonical_frequency_derivative_includes_dispersion=True, frequencies_are_circular_limits=True,
        finite_e_squared_radial_frequency_claimed=False, fixed_action_and_fixed_frequency_distinguished=True,
        weak_periapsis_coefficient='45/2', matched_postadiabatic_trajectory_claimed=False,
        maximum_finite_action_error=validation['maximum_finite_action_error'],
        maximum_frequency_resolution=validation['maximum_frequency_resolution'],
        maximum_independent_radial_derivative_error=validation['maximum_independent_radial_derivative_error'],
        protected_workbench_recent_modified_file_count=len(changed),
        protected_check_scope='Modification-time scan since22:52:00UTC5October2026,not full content-hash baseline.',
        inherited_Einstein_Hilbert_and_G_R_retained=True, original_parent_or_bath_modified=False,
        maximum_concurrent_numerical_workers=1, workers_below_normal_pinned_core2=True,
        github_action=False, subagents=0)
    write_json(output, report, exclusive=True)
    print(dict(state='complete', sealed_files=len(hashes), prior_entries_unchanged=prior_count,
               next_prior_count=prior_count+len(hashes), validation_checks=len(validation['checks']), protected_changes=len(changed)), flush=True)


if __name__ == '__main__':
    main()
