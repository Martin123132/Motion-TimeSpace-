from __future__ import annotations

import ast
import csv
from datetime import datetime, timezone
from pathlib import Path
import re

from interior_energy import ROOT, BRANCH, PARENT, digest, read_json, write_json, modest_process


def main():
    modest_process()
    output = ROOT/'results/stage-integrity.json'
    assert not output.exists()
    post = BRANCH.parent
    stage34 = BRANCH/'eccentric-polar-radiation-20261005'
    tree = ast.parse((stage34/'seal_waves.py').read_text(encoding='utf-8'))
    assignment = next(node for node in ast.walk(tree) if isinstance(node, ast.Assign) and
        any(isinstance(target, ast.Name) and target.id == 'stages' for target in node.targets))
    stages = [PARENT.name, 'surface-susceptibility-20261006', 'response-budget-20261006',
        'matched-inspiral-20261006', 'finite-mass-tidal-balance-20261006',
        'conservative-eccentric-action-20261005', 'postcircular-clock-20261005',
        'near-circular-inspiral-20261005', 'near-circular-quadrupole-20261005',
        stage34.name]+ast.literal_eval(assignment.value)
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
        assert sum(report.get(key) == digest(seals[index+1]) for key in
                   ['parent_seal_sha256', 'previous_seal_sha256']) == 1, seals[index]
    prior_count = sum(len(report['file_hashes']) for report in previous)
    assert prior_count == 5314, prior_count
    manifest = post/'_checkpoints/20261003-pre-condensate-origin/manifest.json'
    assert digest(manifest) == previous[0]['checkpoint_manifest_sha256']
    assert digest(manifest) == '38f86719b0eb4c5e7fd86171a98af51918369f9daf81584a3c19c3d63222389e'
    for source in previous[0]['local_source_documents']:
        assert digest(source['path']) == source['sha256']
    validation = read_json(ROOT/'results/validation/status.json')
    assert len(validation['checks']) == validation['validation_checks'] == 70
    assert all(row['passed'] for row in validation['checks'])
    exact = read_json(ROOT/'results/action-derivation/status.json')
    assert len(exact['checks']) == exact['exact_checks'] == 19
    assert all(row['passed'] and row['residual'] == '0' for row in exact['checks'])
    vacuum = read_json(ROOT/'results/vacuum-canonical/status.json')
    assert vacuum['residual'] == '0' and vacuum['canonical_normalization_times_alpha'] == '3/2'
    constraints = read_json(ROOT/'results/constraint-replay/status.json')
    assert len(constraints['exact_checks']) == 2 and all(row['passed'] and row['residual'] == '0' for row in constraints['exact_checks'])
    assert len(constraints['rows']) == 6 and constraints['numerical_checks'] == 12
    assert all(row['scaled_momentum_constraint_error'] < 1e-10 and row['scaled_phase_equation_error'] < 1e-10
               for row in constraints['rows'])
    for source in validation['primary_pdfs']:
        assert digest(source['path']) == source['sha256']
    script_hashes = {digest(path) for path in ROOT.rglob('*.py')}
    for path in ROOT.rglob('*.json'):
        report = read_json(path)
        assert report['state'] == 'complete' and report['script_sha256'] in script_hashes, path
        for source, expected in report.get('input_hashes', {}).items():
            assert Path(source).is_file() and digest(source) == expected, (path, source)
        for relative, expected in report.get('output_hashes', {}).items():
            assert digest(path.parent/relative) == expected, (path, relative)
    csv_rows = 0
    for path in ROOT.rglob('*.csv'):
        with path.open(newline='', encoding='utf-8') as handle:
            reader = csv.DictReader(handle)
            rows = list(reader)
            assert rows and len(reader.fieldnames) == len(set(reader.fieldnames))
            assert all(None not in row and None not in row.values() for row in rows)
            csv_rows += len(rows)
    assert csv_rows == validation['csv_rows'] == 4
    cited = set()
    for path in ROOT.glob('*.md'):
        for reference in re.findall(r'`([^`]+)`', path.read_text(encoding='utf-8')):
            if reference.endswith(('.md', '.py', '.json', '.csv', '.pdf')):
                target = (ROOT/reference).resolve()
                assert target == output or target.is_file(), (path, reference)
                if target != output:
                    cited.add(target)
    compiled = []
    for path in ROOT.rglob('*.py'):
        compile(path.read_bytes(), str(path), 'exec')
        compiled.append(path.relative_to(ROOT).as_posix())
    assert len(compiled) == 9
    assert not list(ROOT.rglob('__pycache__'))
    protected = post.parent/'formalization-workbench'
    started = datetime(2026, 10, 6, 15, 0, 0, tzinfo=timezone.utc)
    changed = [str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime > started.timestamp()]
    assert protected.is_dir() and not changed, changed
    hashes = {path.relative_to(ROOT).as_posix():digest(path) for path in sorted(ROOT.rglob('*'))
              if path.is_file() and path != output}
    assert len(hashes) == 28, len(hashes)
    report = dict(state='complete', sealed_at_utc=datetime.now(timezone.utc).isoformat(), file_hashes=hashes,
        parent_seal_sha256=digest(seals[0]), prior_sealed_entries_unchanged=prior_count,
        parent_chain_edges_verified=len(seals)-1, checkpoint_manifest_sha256=digest(manifest),
        full_checkpoint_payload_rehashed=False, local_source_documents=previous[0]['local_source_documents'],
        local_dependencies={str(path):digest(path) for path in sorted(cited)},
        primary_pdfs=validation['primary_pdfs'], source_urls=validation['source_urls'], compiled_scripts=compiled,
        exact_checks=22, validation_gates=70, parent_constraint_flow_replays=12, csv_rows=csv_rows,
        new_interior_or_background_solves=0, new_wave_solves=0, fitted_parameters=0, new_observational_data=False,
        interior_action_to_surface_storage_match_derived=True,
        canonical_normalization=validation['canonical_normalization'],
        largest_action_response_mismatch=validation['largest_action_response_mismatch'],
        largest_finest_nonlinear_density_error=validation['largest_finest_nonlinear_density_error'],
        edge_halving_mismatch_ratio=validation['edge_halving_mismatch_ratio'],
        energy_convention=validation['energy_convention'],
        all_polar_mode_positive_energy_claimed=False, pointwise_ADM_density_positive=False,
        protected_workbench_recent_modified_file_count=len(changed),
        protected_check_scope='Modification-time scan since15:00UTC6October2026,not a full content-hash baseline.',
        inherited_Einstein_Hilbert_and_G_R_retained=True, original_parent_or_bath_modified=False,
        maximum_concurrent_numerical_workers=1, workers_below_normal_pinned_core2=True,
        github_action=False, subagents=0)
    write_json(output, report, exclusive=True)
    print(dict(state='complete', sealed_files=len(hashes), prior_entries_unchanged=prior_count,
        next_prior_count=prior_count+len(hashes), exact_checks=22, validation_gates=70,
        constraint_replays=12, protected_changes=len(changed)), flush=True)


if __name__ == '__main__':
    main()

