from __future__ import annotations

import ast
import csv
from datetime import datetime, timezone
from pathlib import Path
import re

from carrier import ROOT, BRANCH, PARENT, PRIOR, digest, read_json, write_json, modest_process


def main():
    modest_process()
    post=BRANCH.parent
    output=ROOT/'results/stage-integrity.json'
    assert not output.exists()
    stage34=BRANCH/'eccentric-polar-radiation-20261005'
    tree=ast.parse((stage34/'seal_waves.py').read_text(encoding='utf-8'))
    assignment=next(node for node in ast.walk(tree) if isinstance(node,ast.Assign) and
                    any(isinstance(target,ast.Name) and target.id=='stages' for target in node.targets))
    stages=[PARENT.name,PRIOR.name,stage34.name]+ast.literal_eval(assignment.value)
    seals=[BRANCH/stage/'results/stage-integrity.json' for stage in stages]+[BRANCH/'results/stage-integrity.json']
    bases=[BRANCH/stage for stage in stages]+[post]
    keys=['parent_seal_sha256']*30+['previous_seal_sha256']*2+['parent_seal_sha256']
    prior=[]
    for seal,base in zip(seals,bases):
        report=read_json(seal)
        assert report['state']=='complete',seal
        for relative,expected in report['file_hashes'].items():
            assert digest(base/relative)==expected,base/relative
        prior.append(report)
    assert len(keys)==len(seals)-1
    for index,key in enumerate(keys):
        assert prior[index][key]==digest(seals[index+1]),seals[index]
    prior_count=sum(len(report['file_hashes']) for report in prior)
    assert prior_count==4561,prior_count
    manifest=post/'_checkpoints/20261003-pre-condensate-origin/manifest.json'
    assert digest(manifest)==prior[0]['checkpoint_manifest_sha256']
    assert digest(manifest)=='38f86719b0eb4c5e7fd86171a98af51918369f9daf81584a3c19c3d63222389e'
    for source in prior[0]['local_source_documents']:
        assert digest(source['path'])==source['sha256']
    validation=read_json(ROOT/'results/validation/status.json')
    assert validation['state']=='complete' and all(row['passed'] for row in validation['checks'])
    assert validation['script_sha256']==digest(ROOT/'validate_clock.py')
    assert validation['exact_checks']==20 and validation['wave_mode_evaluations']==476
    for source in validation['primary_pdfs']:
        assert digest(source['path'])==source['sha256']
    script_hashes={digest(path) for path in ROOT.glob('*.py')}
    for path in ROOT.rglob('*.json'):
        report=read_json(path)
        assert report['state']=='complete',path
        assert report['script_sha256'] in script_hashes,path
        for source,expected in report.get('input_hashes',{}).items():
            assert Path(source).is_file() and digest(source)==expected,(path,source)
    for path in ROOT.rglob('*.csv'):
        with path.open(newline='',encoding='utf-8') as handle:
            reader=csv.DictReader(handle)
            rows=list(reader)
            assert rows and len(reader.fieldnames)==len(set(reader.fieldnames))
            assert all(None not in row and all(value is not None for value in row.values()) for row in rows),path
    local_sources=[
        PARENT/'results/stage-integrity.json',PARENT/'analyze_inspiral.py',PARENT/'results/analysis/status.json',
        PRIOR/'sidebands.py',PRIOR/'analyze_limit.py',
        PRIOR/'results/finite-fine/status.json',PRIOR/'results/finite-coarse/status.json',PRIOR/'results/analysis/status.json',
        BRANCH/'secular-actions-20261005/results/small-e-fine/status.json',
        BRANCH/'secular-actions-20261005/results/small-e-coarse/status.json',
        BRANCH/'eccentric-source-20261005/eccentric_source.py',
        BRANCH/'eccentric-polar-source-20261005/polar_source.py',
        BRANCH/'secular-actions-20261005/secular.py',
        BRANCH/'orbital-backreaction-20261004/20-reciprocal-tidal-orbit-and-consistent-leading-inspiral.md']
    assert all(path.is_file() for path in local_sources)
    urls=set()
    for path in ROOT.glob('*.md'):
        urls.update(re.findall(r'https://[^\s]+',path.read_text(encoding='utf-8')))
    assert urls<=set(validation['source_urls']),urls-set(validation['source_urls'])
    assert not list(ROOT.rglob('__pycache__'))
    compiled=[]
    for path in ROOT.glob('*.py'):
        compile(path.read_bytes(),str(path),'exec')
        compiled.append(path.name)
    protected=post.parent/'formalization-workbench'
    started=datetime(2026,10,5,20,26,53,tzinfo=timezone.utc)
    changed=[str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime>started.timestamp()]
    assert protected.is_dir() and not changed,changed
    hashes={path.relative_to(ROOT).as_posix():digest(path) for path in sorted(ROOT.rglob('*')) if path.is_file() and path!=output}
    report=dict(state='complete',sealed_at_utc=datetime.now(timezone.utc).isoformat(),file_hashes=hashes,
        parent_seal_sha256=digest(seals[0]),prior_sealed_entries_unchanged=prior_count,parent_chain_edges_verified=len(keys),
        checkpoint_manifest_sha256=digest(manifest),full_checkpoint_payload_rehashed=False,
        local_source_documents=prior[0]['local_source_documents'],local_dependencies={str(path):digest(path) for path in local_sources},
        primary_pdfs=validation['primary_pdfs'],source_urls=validation['source_urls'],
        validation_checks=len(validation['checks']),exact_checks=20,compiled_scripts=compiled,
        new_frequency_wave_evaluations=476,new_static_or_background_solves=0,new_fitted_parameters=0,
        source_carrier_order_e2_derived=True,frequency_response_derivative='five-point centered numerical, two step controls',
        P2_from_energy_and_angular_actions_agree=True,clock_phase_order_initial_e_squared=1,
        new_equal_time_phase_inversion=False,tidal_P2_coefficient='315/4',absorption_P2_coefficient='6',
        maximum_P2_resolution=validation['maximum_P2_resolution'],
        maximum_frequency_step_change=validation['maximum_frequency_step_change'],
        maximum_finite_P2_error=validation['maximum_finite_P2_error'],
        maximum_finite_amplitude_error=validation['maximum_finite_amplitude_error'],
        maximum_clock_resolution=validation['maximum_clock_resolution'],
        protected_workbench_recent_modified_file_count=len(changed),
        protected_check_scope='Modification-time scan since20:26:53UTC5October2026,not a full content-hash baseline.',
        inherited_Einstein_Hilbert_and_G_R_retained=True,original_parent_or_bath_modified=False,
        maximum_concurrent_numerical_workers=2,workers_below_normal_pinned_core2=True,
        github_action=False,subagents=0)
    write_json(output,report,exclusive=True)
    print(dict(state='complete',sealed_files=len(hashes),prior_entries_unchanged=prior_count,
               next_prior_count=prior_count+len(hashes),validation_checks=len(validation['checks']),protected_changes=len(changed)),flush=True)


if __name__=='__main__':
    main()

