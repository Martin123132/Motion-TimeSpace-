from __future__ import annotations

import ast
from datetime import datetime,timezone
from pathlib import Path
import re

from cosmology_common import ROOT,BRANCH,POST,PARENT,digest,read_json,write_json,modest_process


def main():
    modest_process()
    output=ROOT/'results/stage-integrity.json'
    assert not output.exists()
    stage34=BRANCH/'eccentric-polar-radiation-20261005'
    tree=ast.parse((stage34/'seal_waves.py').read_text(encoding='utf-8'))
    assignment=next(node for node in ast.walk(tree) if isinstance(node,ast.Assign) and any(isinstance(target,ast.Name) and target.id=='stages' for target in node.targets))
    stages=[PARENT.name,'polar-energy-bound-20261006','polar-hamiltonian-20261006','interior-storage-20261006','transient-energy-20261006',
        'surface-susceptibility-20261006','response-budget-20261006','matched-inspiral-20261006','finite-mass-tidal-balance-20261006',
        'conservative-eccentric-action-20261005','postcircular-clock-20261005','near-circular-inspiral-20261005',
        'near-circular-quadrupole-20261005',stage34.name]+ast.literal_eval(assignment.value)
    seals=[BRANCH/stage/'results/stage-integrity.json' for stage in stages]+[BRANCH/'results/stage-integrity.json']
    bases=[BRANCH/stage for stage in stages]+[POST]
    prior=[]
    for path,base in zip(seals,bases):
        report=read_json(path)
        assert report['state']=='complete'
        for relative,expected in report['file_hashes'].items():
            assert digest(base/relative)==expected,base/relative
        prior.append(report)
    for index,report in enumerate(prior[:-1]):
        assert sum(report.get(key)==digest(seals[index+1]) for key in ['parent_seal_sha256','previous_seal_sha256'])==1,seals[index]
    prior_count=sum(len(report['file_hashes']) for report in prior)
    assert prior_count==5490,prior_count
    manifest=POST/'_checkpoints/20261003-pre-condensate-origin/manifest.json'
    assert digest(manifest)==prior[0]['checkpoint_manifest_sha256']=='38f86719b0eb4c5e7fd86171a98af51918369f9daf81584a3c19c3d63222389e'
    for source in prior[0]['local_source_documents']+prior[0]['primary_pdfs']:
        assert digest(source['path'])==source['sha256']
    compiled=[]
    for path in sorted(ROOT.glob('*.py')):
        compile(path.read_bytes(),str(path),'exec')
        compiled.append(path.name)
    script_hashes={digest(ROOT/name) for name in compiled}
    for path in ROOT.glob('results/*/status.json'):
        report=read_json(path)
        assert report['state']=='complete' and report['script_sha256'] in script_hashes,path
        for source,expected in report['input_hashes'].items():
            assert Path(source).is_file() and digest(source)==expected,(path,source)
    validation=read_json(ROOT/'results/validation/status.json')
    assert validation['validation_checks']==90 and all(row['passed'] for row in validation['checks'])
    assert validation['all_models_converged'] and validation['dataset_is_actual_observations']
    assert not validation['parent_framework_replaced'] and not validation['closed_candidate_bath_matching_proved']
    cited=set()
    for path in ROOT.glob('*.md'):
        for reference in re.findall(r'`([^`\n]+)`',path.read_text(encoding='utf-8')):
            if reference.endswith(('.md','.py','.json','.txt')):
                target=(ROOT/reference).resolve()
                assert target==output or target.is_file(),(path,reference)
                if target!=output:
                    cited.add(target)
    assert not list(ROOT.rglob('__pycache__'))
    assert (ROOT/'runs/observational-smoke/COMPLETE').is_file()
    protected=POST.parent/'formalization-workbench'
    started=datetime(2026,10,6,19,25,0,tzinfo=timezone.utc)
    changed=[str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime>started.timestamp()]
    assert protected.is_dir() and not changed,changed
    hashes={path.relative_to(ROOT).as_posix():digest(path) for path in sorted(ROOT.rglob('*')) if path.is_file() and path!=output}
    write_json(output,dict(state='complete',sealed_at_utc=datetime.now(timezone.utc).isoformat(),file_hashes=hashes,
        parent_seal_sha256=digest(seals[0]),prior_sealed_entries_unchanged=prior_count,parent_chain_edges_verified=len(seals)-1,
        checkpoint_manifest_sha256=digest(manifest),full_checkpoint_payload_rehashed=False,
        local_source_documents=prior[0]['local_source_documents'],primary_pdfs=prior[0]['primary_pdfs'],source_urls=prior[0]['source_urls'],
        observational_source_urls=read_json(ROOT/'results/preflight/status.json')['source_web_urls'],
        local_dependencies={str(path):digest(path) for path in sorted(cited)},compiled_scripts=compiled,
        preflight_checks=38,validation_gates=90,SN_light_curve_rows=1624,BAO_elements=13,
        primary_models=8,fixed_fraction_profiles=7,no_Lambda_grid_evaluations=357,
        all_primary_models_have_converged_attempts=True,comparison_is_actual_observations=True,
        conclusion='Tested preferred homogeneous charge-tracking state returns to zero fraction with Lambda; noLambda version fits poorly. Earlier parent cosmology remains competitive. Dilute-body dust limit is background-degenerate, not detected.',
        homogeneous_state_exclusion_is_not_full_action_exclusion=True,full_framework_integration_proved=False,
        protected_workbench_recent_modified_file_count=len(changed),
        protected_check_scope='Modification-time scan since19:25UTC6October2026,not a full content-hash baseline.',
        maximum_concurrent_python_workers=1,workers_below_normal_pinned_core2=True,library_threads=1,
        new_background_solves_scope='Short homogeneous FLRW reduction checks only; no new isolated-body or radiation jobs.',
        original_parent_or_bath_modified=False,github_action=False,subagents=0))
    print(dict(state='complete',sealed_files=len(hashes),prior_entries_unchanged=prior_count,next_prior_count=prior_count+len(hashes),
        observations=1637,validation=90,protected_changes=len(changed)),flush=True)


if __name__=='__main__':
    main()
