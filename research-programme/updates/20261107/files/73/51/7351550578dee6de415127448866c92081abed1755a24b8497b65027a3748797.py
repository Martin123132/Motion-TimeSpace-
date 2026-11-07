from __future__ import annotations

import ast
from datetime import datetime, timezone
from pathlib import Path
import re

from interior_common import ROOT, BRANCH, PARENT, digest, read_json, modest_process
from polar_energy import write_json


def main():
    modest_process()
    output=ROOT/'results/stage-integrity.json'
    assert not output.exists()
    post=BRANCH.parent
    stage34=BRANCH/'eccentric-polar-radiation-20261005'
    tree=ast.parse((stage34/'seal_waves.py').read_text(encoding='utf-8'))
    assignment=next(node for node in ast.walk(tree) if isinstance(node,ast.Assign) and any(isinstance(target,ast.Name) and target.id=='stages' for target in node.targets))
    stages=[PARENT.name,'polar-hamiltonian-20261006','interior-storage-20261006','transient-energy-20261006',
        'surface-susceptibility-20261006','response-budget-20261006','matched-inspiral-20261006',
        'finite-mass-tidal-balance-20261006','conservative-eccentric-action-20261005','postcircular-clock-20261005',
        'near-circular-inspiral-20261005','near-circular-quadrupole-20261005',stage34.name]+ast.literal_eval(assignment.value)
    seals=[BRANCH/stage/'results/stage-integrity.json' for stage in stages]+[BRANCH/'results/stage-integrity.json']
    bases=[BRANCH/stage for stage in stages]+[post]
    prior=[]
    for seal,base in zip(seals,bases):
        report=read_json(seal)
        assert report['state']=='complete'
        for relative,expected in report['file_hashes'].items():
            assert digest(base/relative)==expected,base/relative
        prior.append(report)
    for index,report in enumerate(prior[:-1]):
        assert sum(report.get(key)==digest(seals[index+1]) for key in ['parent_seal_sha256','previous_seal_sha256'])==1,seals[index]
    prior_count=sum(len(report['file_hashes']) for report in prior)
    assert prior_count==5438,prior_count
    manifest=post/'_checkpoints/20261003-pre-condensate-origin/manifest.json'
    assert digest(manifest)==prior[0]['checkpoint_manifest_sha256']=='38f86719b0eb4c5e7fd86171a98af51918369f9daf81584a3c19c3d63222389e'
    for source in prior[0]['local_source_documents']+prior[0]['primary_pdfs']:
        assert digest(source['path'])==source['sha256']
    validation=read_json(ROOT/'results/validation/status.json')
    assert len(validation['checks'])==validation['validation_checks'] and all(row['passed'] for row in validation['checks'])
    assert validation['exact_checks']==30 and validation['coupled_principal_positivity_derived']
    assert not validation['full_joint_even_energy_positive_proved']
    assert set(validation['accepted_result_labels']).isdisjoint(validation['rejected_result_labels'])
    script_hashes={digest(path) for path in ROOT.glob('*.py')}
    for path in ROOT.rglob('*.json'):
        report=read_json(path)
        assert report['state']=='complete' and report['script_sha256'] in script_hashes,path
        for source,expected in report.get('input_hashes',{}).items():
            assert Path(source).is_file() and digest(source)==expected,(path,source)
    cited=set()
    for path in ROOT.glob('*.md'):
        for reference in re.findall(r'`([^`\n]+)`',path.read_text(encoding='utf-8')):
            if reference.endswith(('.md','.py','.json','.csv','.pdf')):
                target=(ROOT/reference).resolve()
                assert target==output or target.is_file(),(path,reference)
                if target!=output:
                    cited.add(target)
    compiled=[]
    for path in ROOT.rglob('*.py'):
        compile(path.read_bytes(),str(path),'exec')
        compiled.append(path.relative_to(ROOT).as_posix())
    assert sorted(compiled)==sorted(validation['compiled_scripts'])
    assert not list(ROOT.rglob('__pycache__'))
    protected=post.parent/'formalization-workbench'
    started=datetime(2026,10,6,17,7,0,tzinfo=timezone.utc)
    changed=[str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime>started.timestamp()]
    assert protected.is_dir() and not changed,changed
    hashes={path.relative_to(ROOT).as_posix():digest(path) for path in sorted(ROOT.rglob('*')) if path.is_file() and path!=output}
    report=dict(state='complete',sealed_at_utc=datetime.now(timezone.utc).isoformat(),file_hashes=hashes,
        parent_seal_sha256=digest(seals[0]),prior_sealed_entries_unchanged=prior_count,parent_chain_edges_verified=len(seals)-1,
        checkpoint_manifest_sha256=digest(manifest),full_checkpoint_payload_rehashed=False,
        local_source_documents=prior[0]['local_source_documents'],primary_pdfs=prior[0]['primary_pdfs'],source_urls=prior[0]['source_urls'],
        local_dependencies={str(path):digest(path) for path in sorted(cited)},compiled_scripts=compiled,
        accepted_result_labels=validation['accepted_result_labels'],rejected_result_labels=validation['rejected_result_labels'],
        rejected_attempt_retained_and_detected=True,exact_checks=30,extra_documented_contact_identity_verified=True,
        validation_gates=validation['validation_checks'],new_phase_coefficient_lower=validation['phase_uniform_lower'],
        coupled_gradient_positive_squares_derived=True,exterior_contact_matched_exactly=True,
        entire_even_energy_positive_proved=False,canonical_variable_change_proved=False,
        simple_potential_deformations_tried=3,new_background_or_wave_solves=0,fitted_parameters=0,
        inherited_Einstein_Hilbert_and_G_R_retained=True,original_parent_or_bath_modified=False,
        protected_workbench_recent_modified_file_count=len(changed),
        protected_check_scope='Modification-time scan since17:07UTC6October2026,not a full content-hash baseline.',
        maximum_concurrent_python_workers=2,worker_overlap_note='One brief symbolic/inspection overlap; otherwise serial below-normal CPU2 workers, numerical-library threads=1.',
        github_action=False,subagents=0)
    write_json(output,report)
    print(dict(state='complete',sealed_files=len(hashes),prior_entries_unchanged=prior_count,next_prior_count=prior_count+len(hashes),
        exact_checks=30,validation_gates=validation['validation_checks'],protected_changes=len(changed)),flush=True)


if __name__ == '__main__':
    main()
