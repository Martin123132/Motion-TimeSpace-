from __future__ import annotations

import ast
from datetime import datetime, timezone
import os
import re

from native_common import *


def main():
    modest()
    output = ROOT / 'results/stage-integrity.json'
    assert not output.exists()
    branch = ROOT.parent
    stage34 = branch / 'eccentric-polar-radiation-20261005'
    tree = ast.parse((stage34 / 'seal_waves.py').read_text(encoding='utf-8'))
    assignment = next(node for node in ast.walk(tree) if isinstance(node, ast.Assign)
        and any(isinstance(target, ast.Name) and target.id=='stages' for target in node.targets))
    stages = [PARENT.name, 'heavy-interaction-and-condensate-bridge-20261007',
        'early-adiabatic-matching-20261006', 'matter-growth-response-20261006',
        'motion-bath-matching-20261006', 'cosmology-reconnection-20261006',
        'polar-interior-schur-20261006', 'polar-energy-bound-20261006', 'polar-hamiltonian-20261006',
        'interior-storage-20261006', 'transient-energy-20261006', 'surface-susceptibility-20261006',
        'response-budget-20261006', 'matched-inspiral-20261006', 'finite-mass-tidal-balance-20261006',
        'conservative-eccentric-action-20261005', 'postcircular-clock-20261005',
        'near-circular-inspiral-20261005', 'near-circular-quadrupole-20261005', stage34.name] + ast.literal_eval(assignment.value)
    assert len(stages)==len(set(stages))
    seals = [branch / stage / 'results/stage-integrity.json' for stage in stages] + [branch / 'results/stage-integrity.json']
    bases = [branch / stage for stage in stages] + [POST]
    reports = []
    for path, base in zip(seals, bases):
        report = json.loads(path.read_text())
        assert report['state']=='complete'
        for relative, expected in report['file_hashes'].items():
            assert digest(base / relative)==expected, base / relative
        reports.append(report)
    for index, report in enumerate(reports[:-1]):
        assert sum(report.get(key)==digest(seals[index+1]) for key in ['parent_seal_sha256', 'previous_seal_sha256'])==1
    prior_count = sum(len(report['file_hashes']) for report in reports)
    assert prior_count==5619, prior_count
    manifest = POST / '_checkpoints/20261003-pre-condensate-origin/manifest.json'
    assert digest(manifest)==reports[0]['checkpoint_manifest_sha256']=='38f86719b0eb4c5e7fd86171a98af51918369f9daf81584a3c19c3d63222389e'
    for source in reports[0]['local_source_documents'] + reports[0]['primary_pdfs']:
        assert digest(source['path'])==source['sha256'], source['path']
    acquisition = json.loads((ROOT / 'sources/acquisition.json').read_text())
    for source in acquisition['sources']:
        assert digest(source['path'])==source['sha256']
    assert acquisition['compiler_publisher_sha256_verified']
    build = json.loads((ROOT / 'runs/build-7/status.json').read_text())
    assert build['state']=='complete' and build['bounds_checking'] and build['temporary_drive_mapping_removed']
    assert digest(ROOT / 'native/camb/cambdll.dll')==build['dll_sha256']
    assert digest(ROOT / 'toolchain/mingw64/bin/gfortran.exe')==build['compiler_sha256']
    for path, expected in build['input_hashes'].items():
        assert digest(path)==expected, path
    for relative, expected in build['object_hashes'].items():
        assert digest(ROOT / 'native/fortran' / relative)==expected, relative
    archives = list((ROOT / 'sources').glob('*-v*.py')) + [ROOT / 'runs/build-6/cambdll.dll', ROOT / 'runs/build-6/camb_python.f90']
    archival_hashes = {digest(path): str(path) for path in archives}
    compiled = []
    for path in list(ROOT.glob('*.py')) + [ROOT / 'native/camb/mts.py']:
        compile(path.read_bytes(), str(path), 'exec')
        compiled.append(path)
    producer_hashes = {digest(path) for path in compiled} | set(archival_hashes)
    historical_resolutions = []
    checked_packets = 0
    for path in list(ROOT.glob('runs/*/status.json')) + list(ROOT.glob('results/*/status.json')):
        report = json.loads(path.read_text())
        if 'script_sha256' not in report:
            continue
        assert report['script_sha256'] in producer_hashes, path
        assert (path.parent / 'COMPLETE').is_file(), path
        for source, expected in report['input_hashes'].items():
            assert Path(source).is_file(), source
            if digest(source)!=expected:
                assert expected in archival_hashes, (path, source, expected)
                historical_resolutions.append(dict(packet=str(path), historical_input=source,
                    preserved_copy=archival_hashes[expected], sha256=expected))
        checked_packets += 1
    validation = json.loads((ROOT / 'results/validation-final/status.json').read_text())
    assert validation['all_checks_passed'] and validation['count']==51
    assert all(row['passed'] for row in validation['checks'])
    symbolic = json.loads((ROOT / 'results/identities/status.json').read_text())
    assert symbolic['count']==5 and symbolic['all_checks_passed']
    failed_gate = json.loads((ROOT / 'results/validation-v2/status.json').read_text())
    assert not failed_gate['all_checks_passed']
    assert [row['name'] for row in failed_gate['checks'] if not row['passed']]==['phase_averaged_pressure_consistency']
    cited = set()
    for path in ROOT.glob('*.md'):
        for reference in re.findall(r'`([^`\n]+)`', path.read_text(encoding='utf-8')):
            if reference.endswith(('.py', '.md', '.json', '.npz', '.zip')):
                target = (ROOT / reference).resolve()
                assert target.is_file(), (path, reference)
                cited.add(str(target))
    protected = POST.parent / 'formalization-workbench'
    started = datetime(2026, 10, 7, 0, 26, 40, tzinfo=timezone.utc)
    changed = [str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime>started.timestamp()]
    assert protected.is_dir() and not changed, changed
    excluded = {'toolchain', 'native/fortran/WinMTS', 'runs/matplotlib-cache'}
    hashes = {}
    for directory, directories, files in os.walk(ROOT):
        directories[:] = [name for name in directories if (Path(directory)/name).relative_to(ROOT).as_posix() not in excluded]
        assert '__pycache__' not in directories, directory
        for name in sorted(files):
            path = Path(directory) / name
            if path != output:
                hashes[path.relative_to(ROOT).as_posix()] = digest(path)
    assert not Path('R:/').exists()
    write_json(output, dict(state='complete', sealed_at_utc=datetime.now(timezone.utc).isoformat(),
        file_hashes=hashes, parent_seal_sha256=digest(seals[0]), prior_sealed_entries_unchanged=prior_count,
        parent_chain_edges_verified=len(seals)-1, checkpoint_manifest_sha256=digest(manifest),
        full_checkpoint_payload_rehashed=False, local_source_documents=reports[0]['local_source_documents'],
        primary_pdfs=reports[0]['primary_pdfs'], source_urls=reports[0]['source_urls'],
        previous_primary_source_urls=reports[0]['new_primary_source_urls'],
        new_primary_source_urls=[source['url'] for source in acquisition['sources']] + [
            'https://github.com/cmbant/CAMB/tree/3ef0272d6f7ba1231128872e56e6d4c12af8267b',
            'https://github.com/cmbant/forutils/tree/841f06d5356877e90437f94b2d976dd98f7f923c'],
        observational_source_urls=reports[0]['observational_source_urls'],
        local_dependencies={path: digest(path) for path in cited},
        compiled_scripts=[str(path.relative_to(ROOT)) for path in compiled],
        checked_result_packets=checked_packets, historical_input_resolutions=historical_resolutions,
        validation_checks=51, exact_symbolic_identities=5, all_checks_passed=True,
        native_cold_limit_verified=True, native_two_field_early_hierarchy=True,
        native_heavy_late_matching=False, physical_late_heavy_spectrum=False, new_observational_fit=False,
        early_scale_factors=[.0002,.000225,.00025], k_Mpc_inverse=[.03,.1,1.,5.],
        failed_initial_pressure_gate_preserved=True, pressure_gate_threshold_unchanged=2e-6,
        excluded_reproducible_dependency_caches=sorted(excluded),
        dependency_cache_policy='Compiler archive and publisher checksum sealed; extracted compiler/cache not individually sealed. Final source inputs, object hashes, native library, and compact six-file source delta verified.',
        compiler_executable_sha256=build['compiler_sha256'], native_library_sha256=build['dll_sha256'],
        protected_workbench_recent_modified_file_count=0,
        protected_check_scope='Modification-time scan since00:26:40UTC7October2026, not a full content-hash baseline.',
        maximum_concurrent_compute_workers=2, heavy_workers_below_normal_pinned_core2=True, library_threads=1,
        active_stage_workers=0, github_action=False, subagents=0, global_installation_changed=False,
        original_parent_modified=False, galaxy_work_modified=False,
        conclusion='Canonical slow and heavy perturbations now source the native radiation hierarchy. The slow cold control is recovered; resolved early heavy scale-dependent growth survives. Next: explicit full-state native matching and late spectra.'))
    print(json.dumps(dict(state='complete', sealed_files=len(hashes), prior_entries_unchanged=prior_count,
        next_prior_count=prior_count+len(hashes), checked_packets=checked_packets,
        preserved_historical_input_resolutions=len(historical_resolutions), protected_recent_changes=0)), flush=True)


if __name__ == '__main__':
    main()
