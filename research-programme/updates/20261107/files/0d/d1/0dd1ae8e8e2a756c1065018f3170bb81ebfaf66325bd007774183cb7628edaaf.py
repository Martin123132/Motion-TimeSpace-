from __future__ import annotations

import ast
import csv
from datetime import datetime, timezone
from pathlib import Path
import re

from balance import ROOT, BRANCH, PARENT, digest, read_json, write_json, modest_process


def main():
    modest_process()
    output = ROOT/'results/stage-integrity.json'
    assert not output.exists()
    post = BRANCH.parent
    stage34 = BRANCH/'eccentric-polar-radiation-20261005'
    tree = ast.parse((stage34/'seal_waves.py').read_text(encoding='utf-8'))
    assignment = next(node for node in ast.walk(tree) if isinstance(node, ast.Assign) and
                      any(isinstance(target, ast.Name) and target.id == 'stages' for target in node.targets))
    stages = [PARENT.name, 'postcircular-clock-20261005', 'near-circular-inspiral-20261005',
              'near-circular-quadrupole-20261005', stage34.name]+ast.literal_eval(assignment.value)
    seals = [BRANCH/stage/'results/stage-integrity.json' for stage in stages]+[BRANCH/'results/stage-integrity.json']
    bases = [BRANCH/stage for stage in stages]+[post]
    previous = []
    for seal, base in zip(seals, bases):
        report = read_json(seal)
        assert report['state'] == 'complete'
        for relative, expected in report['file_hashes'].items():
            assert digest(base/relative) == expected, base/relative
        previous.append(report)
    for index, report in enumerate(previous[:-1]):
        assert sum(report.get(key) == digest(seals[index+1]) for key in ['parent_seal_sha256', 'previous_seal_sha256']) == 1, seals[index]
    prior_count = sum(len(report['file_hashes']) for report in previous)
    assert prior_count == 5142, prior_count
    manifest = post/'_checkpoints/20261003-pre-condensate-origin/manifest.json'
    assert digest(manifest) == previous[0]['checkpoint_manifest_sha256']
    assert digest(manifest) == '38f86719b0eb4c5e7fd86171a98af51918369f9daf81584a3c19c3d63222389e'
    for source in previous[0]['local_source_documents']:
        assert digest(source['path']) == source['sha256']
    validation = read_json(ROOT/'results/validation/status.json')
    assert validation['state'] == 'complete' and all(row['passed'] for row in validation['checks'])
    assert validation['script_sha256'] == digest(ROOT/'validate_balance.py')
    assert validation['exact_checks'] == 36 and len(validation['checks']) == 214
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
    cited = set()
    urls = set()
    for document in ROOT.glob('*.md'):
        contents = document.read_text(encoding='utf-8')
        urls.update(re.findall(r'https://[^\s]+', contents))
        for reference in re.findall(r'`([^`]+)`', contents):
            if reference.endswith(('.md', '.py', '.json', '.csv')):
                path = (ROOT/reference).resolve()
                assert path == output or path.is_file(), (document, reference)
                if path != output:
                    cited.add(path)
    assert urls <= set(validation['source_urls']), urls-set(validation['source_urls'])
    assert not list(ROOT.rglob('__pycache__'))
    compiled = []
    for path in ROOT.glob('*.py'):
        compile(path.read_bytes(), str(path), 'exec')
        compiled.append(path.name)
    protected = post.parent/'formalization-workbench'
    started = datetime(2026, 10, 6, 1, 1, 0, tzinfo=timezone.utc)
    changed = [str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime > started.timestamp()]
    assert protected.is_dir() and not changed, changed
    hashes = {path.relative_to(ROOT).as_posix():digest(path) for path in sorted(ROOT.rglob('*')) if path.is_file() and path != output}
    report = dict(state='complete', sealed_at_utc=datetime.now(timezone.utc).isoformat(), file_hashes=hashes,
        parent_seal_sha256=digest(seals[0]), prior_sealed_entries_unchanged=prior_count,
        parent_chain_edges_verified=len(seals)-1, checkpoint_manifest_sha256=digest(manifest), full_checkpoint_payload_rehashed=False,
        local_source_documents=previous[0]['local_source_documents'], local_dependencies={str(path):digest(path) for path in sorted(cited)},
        primary_pdfs=validation['primary_pdfs'], source_urls=validation['source_urls'],
        validation_checks=len(validation['checks']), exact_checks=36, independent_finite_amplitude_control_orbits=54,
        compiled_scripts=compiled, new_background_solves=0, new_interior_or_wave_solves=0, new_fitted_parameters=0,
        new_observational_data=False, matched_static_electric_tidal_balance_derived=True,
        finite_companion_mass_factors_retained=True, mixed_lambda_eccentricity_squared_retained=True,
        eccentricity_variable='z=2Jr/Jphi, not an exact geometric turning-point eccentricity',
        action_radius='d=(Jphi/mu_red)^2/MT', frequency_radius='D=(MT/Omega_phi^2)^(1/3)',
        circular_stage20_and_testmass_stage35_stage37_limits_recovered=True,
        absorption_or_full_finite_frequency_chirp_claimed=False, new_accumulated_trajectory_claimed=False,
        maximum_coefficient_scaled_error=validation['maximum_coefficient_scaled_error'],
        maximum_damping_coefficient_error=validation['maximum_damping_coefficient_error'],
        maximum_numerical_resolution=validation['maximum_numerical_resolution'],
        protected_workbench_recent_modified_file_count=len(changed),
        protected_check_scope='Modification-time scan since01:01:00UTC6October2026,not a full content-hash baseline.',
        inherited_Einstein_Hilbert_and_G_R_retained=True, original_parent_or_bath_modified=False,
        maximum_concurrent_numerical_workers=1, workers_below_normal_pinned_core2=True, github_action=False, subagents=0)
    write_json(output, report, exclusive=True)
    print(dict(state='complete', sealed_files=len(hashes), prior_entries_unchanged=prior_count,
               next_prior_count=prior_count+len(hashes), validation_checks=len(validation['checks']), protected_changes=len(changed)), flush=True)


if __name__ == '__main__':
    main()
