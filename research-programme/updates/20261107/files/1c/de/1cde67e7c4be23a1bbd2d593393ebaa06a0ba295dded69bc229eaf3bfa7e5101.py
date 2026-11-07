from __future__ import annotations

import re
from seed_common import *


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
            assert digest(base/relative)==expected,base/relative
        prior_count+=len(report['file_hashes'])
        if cursor==BRANCH/'results/stage-integrity.json':
            break
        links=[report[key] for key in ['parent_seal_sha256','previous_seal_sha256'] if key in report]
        assert len(links)==1 and links[0] in by_hash
        cursor=by_hash[links[0]]
        edges+=1
    assert prior_count==6731,prior_count
    checkpoint=POST/'_checkpoints/20261003-pre-condensate-origin/manifest.json'
    original=POST/'.venv-score/Lib/site-packages/camb/cambdll.dll'
    native_library=NATIVE/'camb/cambdll.dll'
    assert digest(checkpoint)==parent['checkpoint_manifest_sha256']=='38f86719b0eb4c5e7fd86171a98af51918369f9daf81584a3c19c3d63222389e'
    assert digest(original)==parent['original_library_sha256']
    assert digest(native_library)==parent['native_library_sha256']
    for source in parent['local_source_documents']+parent['primary_pdfs']:
        assert digest(source['path'])==source['sha256']
    scripts=list(ROOT.glob('*.py'))
    for path in scripts:
        compile(path.read_bytes(),str(path),'exec')
    script_hashes={digest(path) for path in scripts}
    packets=list(ROOT.glob('results/*/status.json'))
    assert len(packets)==6
    for path in packets:
        packet=json.loads(path.read_text())
        assert packet['state']=='complete' and packet['script_sha256'] in script_hashes
        assert (path.parent/'COMPLETE').is_file()
        for source,expected in packet['input_hashes'].items():
            assert digest(source)==expected,(path,source)
    validation=json.loads((ROOT/'results/validation/status.json').read_text())
    exports=json.loads((ROOT/'results/geometric-seed/status.json').read_text())
    for packet in [validation,exports]:
        assert packet['all_checks_passed'] and all(row['passed'] for row in packet['checks'])
    native=json.loads((ROOT/'results/native-seed-valid/status.json').read_text())
    assert len(native['rows'])==60 and sum(row['primary'] for row in native['rows'])==45
    assert all(row['qualified'] for row in native['rows'] if row['primary'])
    assert native['new_parameters_fitted']==0 and not native['late_nonlinear_prediction']
    failure=ROOT/'results/native-seed'
    assert (failure/'FAILED.md').is_file() and not (failure/'COMPLETE').exists()
    for path in native['source_backed_seed_paths']:
        assert Path(path).parent==ROOT/'results/native-seed-valid'
    covariant=json.loads((ROOT/'results/covariant-check/status.json').read_text())
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
            assert url in [row['url'] for row in covariant['source_records']],url
    started=datetime(2026,10,7,3,48,30,tzinfo=timezone.utc)
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
    check_count=validation['count']+exports['count']
    write_json(output,dict(state='complete',sealed_at_utc=datetime.now(timezone.utc).isoformat(),
        file_hashes=file_hashes,parent_seal_sha256=digest(PARENT/'results/stage-integrity.json'),
        prior_sealed_entries_unchanged=prior_count,parent_chain_edges_verified=edges,
        checkpoint_manifest_sha256=digest(checkpoint),full_checkpoint_payload_rehashed=False,
        local_source_documents=parent['local_source_documents'],primary_pdfs=parent['primary_pdfs'],
        source_urls=parent['source_urls'],previous_primary_source_urls=parent['new_primary_source_urls'],
        new_primary_source_urls=[row['url'] for row in covariant['source_records']],
        observational_source_urls=parent['observational_source_urls'],
        local_dependencies={path:digest(path) for path in citations},
        compiled_scripts=[path.name for path in scripts],checked_result_packets=len(packets),
        validation_checks=check_count,main_validation_checks=validation['count'],export_self_checks=exports['count'],
        symbolic_identities_included=35,all_checks_passed=True,prior_goal_turn='progress',
        regular_adiabatic_curvature_seed_derived=True,
        approximation='Radiation-dominated two-gradient seed, three-gradient velocity, frozen canonical masses and subdominant matter/fields.',
        neutrino_tracefree_stress_retained=True,leading_hamiltonian_and_momentum_constraints_verified=True,
        scalar_quadratic_spatial_pullback_derived=True,primary_native_case_count=45,
        scalar_seed_packets=3,three_dimensional_geometric_seed_packets=3,
        premature_native_query_preserved_as_failed=True,primordial_curvature_statistics_derived=False,
        primordial_zeta_second_set_zero_as_choice=True,independent_isocurvature_set_zero_as_choice=True,
        full_radiation_onset_second_order_evolution=False,second_order_heavy_matching=False,
        actual_survey_refit=False,new_parameters_fitted=0,formal_model_preference=False,
        native_library_reused_read_only=True,native_library_sha256=digest(native_library),
        original_library_sha256=digest(original),protected_workbench_recent_modified_file_count=0,
        protected_check_scope='Modification-time scan since03:48:30UTC7October2026, not a full content-hash baseline.',
        maximum_active_compute_workers=1,library_threads=1,active_stage_workers=0,
        github_action=False,subagents=0,global_installation_changed=False,galaxy_work_modified=False,
        conclusion='Derived regular nonlinear curvature initial data with metric, radiation/neutrino and old scalar sources. Native linear and curved constraint controls pass. Next: propagate through radiation and heavy onset, then derive nonlinear phase matching.'))
    print(json.dumps(dict(state='complete',sealed_files=len(file_hashes),prior_entries_unchanged=prior_count,
        next_prior_count=prior_count+len(file_hashes),validation_checks=check_count,packets=len(packets))))


if __name__=='__main__':
    main()
