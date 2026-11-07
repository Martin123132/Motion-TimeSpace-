from __future__ import annotations

import ast
import csv
from datetime import datetime, timezone
from pathlib import Path
import re

from inspiral import ROOT, BRANCH, PARENT, digest, read_json, write_json, modest_process


def main():
    modest_process()
    output = ROOT/'results/stage-integrity.json'
    assert not output.exists()
    post = BRANCH.parent
    stage34 = BRANCH/'eccentric-polar-radiation-20261005'
    tree = ast.parse((stage34/'seal_waves.py').read_text(encoding='utf-8'))
    assignment = next(node for node in ast.walk(tree) if isinstance(node, ast.Assign) and
                      any(isinstance(target, ast.Name) and target.id == 'stages' for target in node.targets))
    stages = [PARENT.name, 'conservative-eccentric-action-20261005', 'postcircular-clock-20261005',
        'near-circular-inspiral-20261005', 'near-circular-quadrupole-20261005', stage34.name]+ast.literal_eval(assignment.value)
    seals = [BRANCH/stage/'results/stage-integrity.json' for stage in stages]+[BRANCH/'results/stage-integrity.json']
    bases = [BRANCH/stage for stage in stages]+[post]
    previous = []
    for seal, base in zip(seals, bases):
        report = read_json(seal)
        assert report['state'] == 'complete', seal
        for relative, expected in report['file_hashes'].items():
            assert digest(base/relative) == expected, base/relative
        previous.append(report)
    for index, report in enumerate(previous[:-1]):
        assert sum(report.get(key) == digest(seals[index+1]) for key in ['parent_seal_sha256', 'previous_seal_sha256']) == 1, seals[index]
    prior_count = sum(len(report['file_hashes']) for report in previous)
    assert prior_count == 5215, prior_count
    manifest = post/'_checkpoints/20261003-pre-condensate-origin/manifest.json'
    assert digest(manifest) == previous[0]['checkpoint_manifest_sha256']
    assert digest(manifest) == '38f86719b0eb4c5e7fd86171a98af51918369f9daf81584a3c19c3d63222389e'
    for source in previous[0]['local_source_documents']:
        assert digest(source['path']) == source['sha256']
    validation = read_json(ROOT/'results/validation/status.json')
    assert validation['state'] == 'complete' and all(row['passed'] for row in validation['checks'])
    assert validation['script_sha256'] == digest(ROOT/'validate_inspiral.py')
    assert len(validation['checks']) == 158
    exact_count = 0
    for name, count in [('derivation', 26), ('testmass', 3)]:
        report = read_json(ROOT/'results'/name/'status.json')
        assert report['exact_checks'] == len(report['checks']) == count
        assert all(row['passed'] and row['residual'] == '0' for row in report['checks'])
        exact_count += count
    for source in validation['primary_pdfs']:
        assert digest(source['path']) == source['sha256']
    script_hashes = {digest(path) for path in ROOT.glob('*.py')}
    for path in ROOT.rglob('*.json'):
        report = read_json(path)
        assert report['state'] == 'complete', path
        assert report['script_sha256'] in script_hashes, path
        for source, expected in report.get('input_hashes', {}).items():
            assert Path(source).is_file() and digest(source) == expected, (path, source)
        for relative, expected in report.get('output_hashes', {}).items():
            assert digest(path.parent/relative) == expected, (path, relative)
    csv_rows = 0
    for path in ROOT.rglob('*.csv'):
        with path.open(newline='', encoding='utf-8') as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)
            assert rows and len(set(reader.fieldnames)) == len(reader.fieldnames)
            assert all(None not in row and None not in row.values() for row in rows)
            csv_rows += len(rows)
    assert csv_rows == 132
    cited, urls = set(), set()
    for document in ROOT.glob('*.md'):
        contents = document.read_text(encoding='utf-8')
        urls.update(re.findall(r'https://[^\s]+', contents))
        for reference in re.findall(r'`([^`]+)`', contents):
            if reference.endswith(('.md', '.py', '.json', '.csv', '.pdf')):
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
    started = datetime(2026, 10, 6, 1, 29, 0, tzinfo=timezone.utc)
    changed = [str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime > started.timestamp()]
    assert protected.is_dir() and not changed, changed
    hashes = {path.relative_to(ROOT).as_posix():digest(path) for path in sorted(ROOT.rglob('*')) if path.is_file() and path != output}
    assert len(hashes) == 20, len(hashes)
    report = dict(state='complete', sealed_at_utc=datetime.now(timezone.utc).isoformat(), file_hashes=hashes,
        parent_seal_sha256=digest(seals[0]), prior_sealed_entries_unchanged=prior_count,
        parent_chain_edges_verified=len(seals)-1, checkpoint_manifest_sha256=digest(manifest),
        full_checkpoint_payload_rehashed=False, local_source_documents=previous[0]['local_source_documents'],
        local_dependencies={str(path):digest(path) for path in sorted(cited)},
        primary_pdfs=validation['primary_pdfs'], source_urls=validation['source_urls'],
        validation_checks=len(validation['checks']), exact_checks=exact_count, compiled_scripts=compiled,
        physical_illustrative_trajectories=4, trajectory_csv_rows=csv_rows, coefficient_integrations=8,
        resummed_order_controls=9, signed_mixed_sensitivity_controls=24,
        new_background_solves=0, new_interior_or_wave_solves=0, new_fitted_parameters=0,
        new_observational_data=False, eccentricity_transport_and_mixed_clock_phase_derived=True,
        endpoint_matching='Common initial/final azimuthal frequency, initial z=2Jr/Jphi, masses; not radial frequency or turning radius.',
        perturbative_order='First order in lambda and initial zi with lambda*zi retained.',
        testmass_outgoing_and_circular_phase_limits_recovered=True,
        full_eccentric_waveform_or_detection_forecast=False, astrophysical_mass_calibration=False,
        maximum_coefficient_scaled_error=validation['maximum_coefficient_error'],
        maximum_numerical_resolution=validation['maximum_resolution'],
        maximum_circular_phase_error=validation['maximum_circular_phase_error'],
        protected_workbench_recent_modified_file_count=len(changed),
        protected_check_scope='Modification-time scan since01:29UTC6October2026,not a full content-hash baseline.',
        inherited_Einstein_Hilbert_and_G_R_retained=True, original_parent_or_bath_modified=False,
        maximum_concurrent_numerical_workers=1, workers_below_normal_pinned_core2=True,
        github_action=False, subagents=0)
    write_json(output, report, exclusive=True)
    print(dict(state='complete', sealed_files=len(hashes), prior_entries_unchanged=prior_count,
        next_prior_count=prior_count+len(hashes), validation_checks=len(validation['checks']),
        exact_checks=exact_count, protected_changes=len(changed)), flush=True)


if __name__ == '__main__':
    main()
