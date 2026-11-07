from __future__ import annotations

import ast
from datetime import datetime, timezone
from pathlib import Path
import re
import sys

import numpy as np
import scipy
import sympy

from bridge_common import ROOT, BRANCH, POST, PARENT, SOURCE_PATHS, COMMIT, digest, read_json, write_json, modest_process


def main():
    modest_process()
    output = ROOT / 'results/stage-integrity.json'
    assert not output.exists()
    stage34 = BRANCH / 'eccentric-polar-radiation-20261005'
    tree = ast.parse((stage34 / 'seal_waves.py').read_text(encoding='utf-8'))
    assignment = next(node for node in ast.walk(tree) if isinstance(node, ast.Assign) and any(isinstance(target, ast.Name) and target.id == 'stages' for target in node.targets))
    stages = [PARENT.name, 'matter-growth-response-20261006', 'motion-bath-matching-20261006',
        'cosmology-reconnection-20261006', 'polar-interior-schur-20261006',
        'polar-energy-bound-20261006', 'polar-hamiltonian-20261006',
        'interior-storage-20261006', 'transient-energy-20261006',
        'surface-susceptibility-20261006', 'response-budget-20261006',
        'matched-inspiral-20261006', 'finite-mass-tidal-balance-20261006',
        'conservative-eccentric-action-20261005', 'postcircular-clock-20261005',
        'near-circular-inspiral-20261005', 'near-circular-quadrupole-20261005',
        stage34.name] + ast.literal_eval(assignment.value)
    assert len(stages) == len(set(stages))
    seals = [BRANCH / stage / 'results/stage-integrity.json' for stage in stages] + [BRANCH / 'results/stage-integrity.json']
    bases = [BRANCH / stage for stage in stages] + [POST]
    reports = []
    for path, base in zip(seals, bases):
        report = read_json(path)
        assert report['state'] == 'complete'
        for relative, expected in report['file_hashes'].items():
            assert digest(base / relative) == expected, base / relative
        reports.append(report)
    for index, report in enumerate(reports[:-1]):
        assert sum(report.get(key) == digest(seals[index + 1]) for key in ['parent_seal_sha256', 'previous_seal_sha256']) == 1, seals[index]
    prior_count = sum(len(report['file_hashes']) for report in reports)
    assert prior_count == 5558, prior_count
    manifest = POST / '_checkpoints/20261003-pre-condensate-origin/manifest.json'
    assert digest(manifest) == reports[0]['checkpoint_manifest_sha256'] == '38f86719b0eb4c5e7fd86171a98af51918369f9daf81584a3c19c3d63222389e'
    local_sources = list(reports[0]['local_source_documents'])
    known = {str(Path(row['path']).resolve()) for row in local_sources}
    for path in SOURCE_PATHS:
        path = path.resolve()
        if str(path) not in known:
            local_sources.append(dict(path=str(path), sha256=digest(path)))
            known.add(str(path))
    for source in local_sources + reports[0]['primary_pdfs']:
        assert digest(source['path']) == source['sha256']
    compiled = []
    for path in sorted(ROOT.glob('*.py')):
        compile(path.read_bytes(), str(path), 'exec')
        compiled.append(path.name)
    producers = {digest(ROOT / name) for name in compiled}
    for path in ROOT.glob('results/*/status.json'):
        report = read_json(path)
        assert report['state'] == 'complete' and report['script_sha256'] in producers
        for source, expected in report['input_hashes'].items():
            assert digest(source) == expected, (path, source)
        assert (path.parent / 'COMPLETE').is_file()
    sources = read_json(ROOT / 'results/sources/status.json')
    assert sources['commit'] == COMMIT and len(sources['source_rows']) == 4
    assert not sources['source_code_executed'] and not sources['lean_independently_compiled']
    for source in sources['source_rows']:
        path = Path(source['local_path'])
        assert path.is_relative_to(ROOT) and path.stat().st_size == source['bytes']
        assert digest(path) == source['sha256'] and not source['executed']
        assert source['url'] == 'https://raw.githubusercontent.com/openai/math/' + COMMIT + '/' + source['repository_path']
    assert sum(row['bytes'] for row in sources['source_rows']) == 17897
    assert 'without a positive-temperature assertion' in (ROOT / 'sources/openai-math/formalization-267.md').read_text(encoding='utf-8')
    derivation = read_json(ROOT / 'results/derivation/status.json')
    assert derivation['count'] == len(derivation['checks']) == 65
    assert derivation['all_checks_passed'] and all(row['passed'] for row in derivation['checks'])
    assert len(derivation['exact_identities']) == 19
    assert all(row['residual'] == '0' for row in derivation['exact_identities'])
    assert len(derivation['independent_oscillator_checks']) == 8
    assert all(row['energy_relative_drift'] < 1e-9 for row in derivation['independent_oscillator_checks'])
    assert derivation['covariance_reconstruction_error'] < 1e-13
    assert not derivation['contact_numeric_parent_value_supplied']
    assert not derivation['thermodynamic_BEC_proved']
    assert not derivation['existing_coherent_wave_route_rejected']
    assert not derivation['observations_changed']
    assert all(not row['valid_for_observational_claim'] for row in derivation['conditional_lifetime_rows'])
    cited = set()
    for path in ROOT.glob('*.md'):
        for reference in re.findall(r'`([^`\n]+)`', path.read_text(encoding='utf-8')):
            if reference.endswith(('.md', '.py', '.json', '.txt', '.tex', '.npz')):
                target = (ROOT / reference).resolve()
                assert target == output or target.is_file(), (path, reference)
                if target != output:
                    cited.add(target)
    assert not list(ROOT.rglob('__pycache__'))
    protected = POST.parent / 'formalization-workbench'
    started = datetime(2026, 10, 6, 23, 30, 32, tzinfo=timezone.utc)
    changed = [str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime > started.timestamp()]
    assert protected.is_dir() and not changed, changed
    hashes = {path.relative_to(ROOT).as_posix(): digest(path) for path in sorted(ROOT.rglob('*')) if path.is_file() and path != output}
    write_json(output, dict(state='complete', sealed_at_utc=datetime.now(timezone.utc).isoformat(),
        file_hashes=hashes, parent_seal_sha256=digest(seals[0]),
        prior_sealed_entries_unchanged=prior_count, parent_chain_edges_verified=len(seals) - 1,
        checkpoint_manifest_sha256=digest(manifest), full_checkpoint_payload_rehashed=False,
        local_source_documents=local_sources, primary_pdfs=reports[0]['primary_pdfs'],
        source_urls=reports[0]['source_urls'],
        previous_primary_source_urls=reports[0]['new_primary_source_urls'],
        new_primary_source_urls=[row['url'] for row in sources['source_rows']] + sources['additional_primary_urls'],
        observational_source_urls=reports[0]['observational_source_urls'],
        external_commit=COMMIT, external_source_rows=sources['source_rows'],
        external_code_executed=False, lean_independently_compiled=False,
        local_dependencies={str(path): digest(path) for path in sorted(cited)},
        compiled_scripts=compiled, validation_checks=derivation['count'],
        exact_identities_included_in_validation_count=19,
        direct_oscillator_integrations=8, all_checks_passed=True,
        contact_numeric_parent_value_supplied=False, thermodynamic_BEC_proved=False,
        existing_coherent_wave_route_rejected=False, observations_changed=False,
        conclusion='Derived conditional elastic/conversion relation and canonical coherence diagnostic in the retained real motion/bath architecture. Resume complete radiation and slow-scalar perturbations with Stage51 early matching.',
        python_version=sys.version, numpy_version=np.__version__, scipy_version=scipy.__version__,
        sympy_version=sympy.__version__, protected_workbench_recent_modified_file_count=len(changed),
        protected_check_scope='Modification-time scan since23:30:32UTC6October2026,not a full content-hash baseline.',
        maximum_concurrent_python_workers=1, workers_below_normal_pinned_core2=True,
        library_threads=1, github_action=False, subagents=0, original_parent_modified=False,
        galaxy_work_modified=False))
    print(dict(state='complete', sealed_files=len(hashes), prior_entries_unchanged=prior_count,
        next_prior_count=prior_count + len(hashes), protected_recent_changes=len(changed)), flush=True)


if __name__ == '__main__':
    main()

