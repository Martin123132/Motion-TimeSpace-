from __future__ import annotations

import ast
import re
from stage_common import *


def main():
    modest()
    output=ROOT/'results/stage-integrity.json'
    assert not output.exists()
    branch=ROOT.parent
    stage34=branch/'eccentric-polar-radiation-20261005'
    tree=ast.parse((stage34/'seal_waves.py').read_text(encoding='utf-8'))
    assignment=next(node for node in ast.walk(tree) if isinstance(node,ast.Assign)
        and any(isinstance(target,ast.Name) and target.id=='stages' for target in node.targets))
    stages=[PARENT.name,'radiation-and-slow-field-transfer-20261007','heavy-interaction-and-condensate-bridge-20261007',
        'early-adiabatic-matching-20261006','matter-growth-response-20261006',
        'motion-bath-matching-20261006','cosmology-reconnection-20261006',
        'polar-interior-schur-20261006','polar-energy-bound-20261006','polar-hamiltonian-20261006',
        'interior-storage-20261006','transient-energy-20261006','surface-susceptibility-20261006',
        'response-budget-20261006','matched-inspiral-20261006','finite-mass-tidal-balance-20261006',
        'conservative-eccentric-action-20261005','postcircular-clock-20261005',
        'near-circular-inspiral-20261005','near-circular-quadrupole-20261005',stage34.name]+ast.literal_eval(assignment.value)
    assert len(stages)==len(set(stages))
    seals=[branch/stage/'results/stage-integrity.json' for stage in stages]+[branch/'results/stage-integrity.json']
    bases=[branch/stage for stage in stages]+[POST]
    reports=[]
    for path,base in zip(seals,bases):
        report=json.loads(path.read_text())
        assert report['state']=='complete'
        for relative,expected in report['file_hashes'].items():
            assert digest(base/relative)==expected,base/relative
        reports.append(report)
    for index,report in enumerate(reports[:-1]):
        assert sum(report.get(key)==digest(seals[index+1]) for key in ['parent_seal_sha256','previous_seal_sha256'])==1
    prior_count=sum(len(report['file_hashes']) for report in reports)
    assert prior_count==5941,prior_count
    manifest=POST/'_checkpoints/20261003-pre-condensate-origin/manifest.json'
    assert digest(manifest)==reports[0]['checkpoint_manifest_sha256']=='38f86719b0eb4c5e7fd86171a98af51918369f9daf81584a3c19c3d63222389e'
    for source in reports[0]['local_source_documents']+reports[0]['primary_pdfs']:
        assert digest(source['path'])==source['sha256']
    original_library=POST/'.venv-score/Lib/site-packages/camb/cambdll.dll'
    assert digest(original_library)=='dacec802377123147f336c37218cdf871b293f1de2b87019c8726b7290082bef'
    build=json.loads((ROOT/'runs/build-1/status.json').read_text())
    assert build['state']=='complete' and build['bounds_checking'] and build['temporary_drive_mapping_removed']
    assert digest(ROOT/'native/camb/cambdll.dll')==build['dll_sha256']
    assert digest(PARENT/'toolchain/mingw64/bin/gfortran.exe')==build['compiler_sha256']
    for source,expected in build['input_hashes'].items():
        assert digest(source)==expected
    scripts=list(ROOT.glob('*.py'))+[ROOT/'native/camb/mts.py',ROOT/'native/camb/model.py']
    for path in scripts:
        compile(path.read_bytes(),str(path),'exec')
    producer_hashes={digest(path) for path in scripts}
    packets=list(ROOT.glob('runs/*/status.json'))+list(ROOT.glob('results/*/status.json'))+list(ROOT.glob('sources/*/status.json'))
    checked=0
    for path in packets:
        report=json.loads(path.read_text())
        assert report['state']=='complete',path
        if 'script_sha256' in report:
            assert report['script_sha256'] in producer_hashes,path
            assert (path.parent/'COMPLETE').is_file(),path
            for source,expected in report['input_hashes'].items():
                assert digest(source)==expected,(path,source)
            checked+=1
    validation=json.loads((ROOT/'results/validation/status.json').read_text())
    assert validation['count']==110 and validation['all_checks_passed']
    stability=json.loads((ROOT/'results/trajectory-stability/status.json').read_text())
    assert len(stability['rows'])==5 and stability['all_checks_passed']
    identities=json.loads((ROOT/'results/identities/status.json').read_text())
    assert identities['count']==7 and identities['all_checks_passed']
    protected=POST.parent/'formalization-workbench'
    started=datetime(2026,10,7,1,14,53,tzinfo=timezone.utc)
    changed=[str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime>started.timestamp()]
    assert protected.is_dir() and not changed,changed
    cited=set()
    for path in ROOT.glob('*.md'):
        for reference in re.findall(r'`([^`\n]+)`',path.read_text(encoding='utf-8')):
            if reference.endswith(('.py','.md','.json','.npz','.zip','.png')):
                target=(ROOT/reference).resolve()
                assert target==output or target.is_file(),(path,reference)
                if target!=output:
                    cited.add(str(target))
    excluded={'native/fortran/WinMTS','runs/matplotlib-cache'}
    hashes={}
    for directory,directories,files in os.walk(ROOT):
        directories[:]=[name for name in directories if (Path(directory)/name).relative_to(ROOT).as_posix() not in excluded]
        assert '__pycache__' not in directories,directory
        for name in sorted(files):
            path=Path(directory)/name
            if path!=output:
                hashes[path.relative_to(ROOT).as_posix()]=digest(path)
    assert not Path('R:/').exists()
    write_json(output,dict(state='complete',sealed_at_utc=datetime.now(timezone.utc).isoformat(),
        file_hashes=hashes,parent_seal_sha256=digest(seals[0]),prior_sealed_entries_unchanged=prior_count,
        parent_chain_edges_verified=len(seals)-1,checkpoint_manifest_sha256=digest(manifest),
        full_checkpoint_payload_rehashed=False,local_source_documents=reports[0]['local_source_documents'],
        primary_pdfs=reports[0]['primary_pdfs'],source_urls=reports[0]['source_urls'],
        previous_primary_source_urls=reports[0]['new_primary_source_urls'],
        new_primary_source_urls=['https://arxiv.org/abs/2201.10238','https://arxiv.org/abs/astro-ph/9506072',
            'https://github.com/cmbant/CAMB/tree/3ef0272d6f7ba1231128872e56e6d4c12af8267b'],
        observational_source_urls=reports[0]['observational_source_urls'],
        local_dependencies={path:digest(path) for path in cited},compiled_scripts=[str(path.relative_to(ROOT)) for path in scripts],
        checked_result_packets=checked,validation_checks=110,extra_trajectory_tests=5,exact_symbolic_identities=7,
        all_checks_passed=True,native_full_state_handoff=True,slow_field_exact=True,
        heavy_average_order='Leading w=0 background plus dispersion-derived rest-frame pressure; finite matching remainder.',
        physical_late_heavy_transfer_samples=True,full_matter_spectrum=False,new_observational_fit=False,
        sourced_k_Mpc_inverse=[.03,.1,1.,5.],unknown_modes_fail_closed=True,
        excluded_reproducible_dependency_caches=sorted(excluded),
        compiler_executable_sha256=build['compiler_sha256'],native_library_sha256=build['dll_sha256'],
        compiler_reused_read_only=True,original_library_sha256=digest(original_library),
        protected_workbench_recent_modified_file_count=0,
        protected_check_scope='Modification-time scan since01:14:53UTC7October2026, not a full content-hash baseline.',
        maximum_concurrent_compute_workers=2,heavy_workers_below_normal_pinned_core2=True,library_threads=1,
        active_stage_workers=0,github_action=False,subagents=0,global_installation_changed=False,
        original_parent_modified=False,galaxy_work_modified=False,
        conclusion='Exact early heavy modes now hand off inside the native hierarchy to averaged late matter evolution. Four physical transfer samples and both controls validated. Next: sourced dense k grid and real structure/growth comparison.'))
    print(json.dumps(dict(state='complete',sealed_files=len(hashes),prior_entries_unchanged=prior_count,
        next_prior_count=prior_count+len(hashes),checked_packets=checked,protected_recent_changes=0)),flush=True)


if __name__=='__main__':
    main()
