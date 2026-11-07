from __future__ import annotations

import re
from feedback_common import *


def main():
    modest()
    output=ROOT/'results/stage-integrity.json'
    assert not output.exists()
    seals=list(BRANCH.glob('*/results/stage-integrity.json'))+[BRANCH/'results/stage-integrity.json']
    by_hash={digest(path):path for path in seals}
    cursor=PARENT/'results/stage-integrity.json'
    seen=set()
    prior_count=0
    edges=0
    parent=json.loads(cursor.read_text())
    while True:
        assert cursor not in seen
        seen.add(cursor)
        report=json.loads(cursor.read_text())
        assert report['state']=='complete'
        base=POST if cursor==BRANCH/'results/stage-integrity.json' else cursor.parent.parent
        for relative,expected in report['file_hashes'].items():
            assert digest(base/relative)==expected,(base/relative)
        prior_count+=len(report['file_hashes'])
        if cursor==BRANCH/'results/stage-integrity.json':
            break
        links=[report[key] for key in ['parent_seal_sha256','previous_seal_sha256'] if key in report]
        assert len(links)==1 and links[0] in by_hash
        cursor=by_hash[links[0]]
        edges+=1
    assert prior_count==6698,prior_count
    checkpoint=POST/'_checkpoints/20261003-pre-condensate-origin/manifest.json'
    original=POST/'.venv-score/Lib/site-packages/camb/cambdll.dll'
    native=NATIVE/'camb/cambdll.dll'
    assert digest(checkpoint)==parent['checkpoint_manifest_sha256']=='38f86719b0eb4c5e7fd86171a98af51918369f9daf81584a3c19c3d63222389e'
    assert digest(original)==parent['original_library_sha256']
    assert digest(native)==parent['native_library_sha256']
    for source in parent['local_source_documents']+parent['primary_pdfs']:
        assert digest(source['path'])==source['sha256']
    scripts=list(ROOT.glob('*.py'))
    for path in scripts:
        compile(path.read_bytes(),str(path),'exec')
    script_hashes={digest(path) for path in scripts}
    packets=list(ROOT.glob('results/*/status.json'))
    assert len(packets)==5
    for path in packets:
        packet=json.loads(path.read_text())
        assert packet['state']=='complete' and packet['script_sha256'] in script_hashes
        assert (path.parent/'COMPLETE').is_file()
        for source,expected in packet['input_hashes'].items():
            assert digest(source)==expected,(path,source)
    validation=json.loads((ROOT/'results/validation/status.json').read_text())
    assert validation['all_checks_passed'] and all(row['passed'] for row in validation['checks'])
    feedback=json.loads((ROOT/'results/feedback/status.json').read_text())
    assert len(feedback['rows'])==9 and len(feedback['periodic_checks'])==12
    assert all(row['linear_projection_qualified'] and row['interpolation_qualified'] for row in feedback['rows'])
    assert not feedback['actual_survey_refit'] and feedback['new_parameters_fitted']==0
    projection=json.loads((ROOT/'results/source-projection/status.json').read_text())
    citations=set()
    for path in ROOT.glob('*.md'):
        content=path.read_text(encoding='utf-8')
        for reference in re.findall(r'`([^`\n]+)`',content):
            if reference.endswith(('.md','.py','.npz','.json','.f90')):
                target=(ROOT/reference).resolve()
                assert target==output or target.is_file(),(path,reference)
                if target!=output:
                    citations.add(str(target))
        for url in re.findall(r'https://[^\s)]+',content):
            assert url in [row['url'] for row in projection['source_records']],url
    started=datetime(2026,10,7,3,31,24,tzinfo=timezone.utc)
    protected=POST.parent/'formalization-workbench'
    changed=[str(path) for path in protected.rglob('*') if path.is_file() and path.stat().st_mtime>started.timestamp()]
    assert protected.is_dir() and not changed,changed
    file_hashes={}
    for directory,directories,files in os.walk(ROOT):
        assert '__pycache__' not in directories,directory
        for name in sorted(files):
            path=Path(directory)/name
            if path!=output:
                file_hashes[path.relative_to(ROOT).as_posix()]=digest(path)
    write_json(output,dict(state='complete',sealed_at_utc=datetime.now(timezone.utc).isoformat(),
        file_hashes=file_hashes,parent_seal_sha256=digest(PARENT/'results/stage-integrity.json'),
        prior_sealed_entries_unchanged=prior_count,parent_chain_edges_verified=edges,
        checkpoint_manifest_sha256=digest(checkpoint),full_checkpoint_payload_rehashed=False,
        local_source_documents=parent['local_source_documents'],primary_pdfs=parent['primary_pdfs'],
        source_urls=parent['source_urls'],previous_primary_source_urls=parent['new_primary_source_urls'],
        new_primary_source_urls=[row['url'] for row in projection['source_records']],
        observational_source_urls=parent['observational_source_urls'],
        local_dependencies={path:digest(path) for path in citations},
        compiled_scripts=[path.name for path in scripts],checked_result_packets=len(packets),
        validation_checks=validation['count'],symbolic_identities_included=37,all_checks_passed=True,
        prior_goal_turn='progress',exact_canonical_ADM_source_derived=True,
        nonlinear_heavy_reduction_scope='Leading weak-field NR Gaussian canonical specialization',
        hilbert_and_improved_flux_distinguished=True,second_order_planar_feedback_integrated=True,
        general_quadratic_mode_sources_derived=True,full_mixed_mode_solution=False,
        cold_F2_G2_limit_verified=True,second_order_primordial_initial_matching=False,
        full_native_second_order_gravity=False,actual_survey_refit=False,new_parameters_fitted=0,
        scalar_exact_particle_number_asserted=False,formal_model_preference=False,
        native_library_reused_read_only=True,native_library_sha256=digest(native),
        original_library_sha256=digest(original),protected_workbench_recent_modified_file_count=0,
        protected_check_scope='Modification-time scan since03:31:24UTC7October2026, not a full content-hash baseline.',
        maximum_active_compute_workers=1,library_threads=1,active_stage_workers=0,
        github_action=False,subagents=0,global_installation_changed=False,galaxy_work_modified=False,
        conclusion='Derived canonical quadratic stress and leading nonlinear heavy force/kernel. Native-seeded gravitational feedback and periodic controls verified. Next: second-order initial matching and mixed-mode cumulant evolution.'))
    print(json.dumps(dict(state='complete',sealed_files=len(file_hashes),prior_entries_unchanged=prior_count,
        next_prior_count=prior_count+len(file_hashes),validation_checks=validation['count'],packets=len(packets))))


if __name__=='__main__':
    main()
