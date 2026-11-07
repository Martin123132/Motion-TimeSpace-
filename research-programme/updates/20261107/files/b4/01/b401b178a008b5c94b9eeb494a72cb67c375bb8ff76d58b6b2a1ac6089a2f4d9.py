from __future__ import annotations

from boundary_common import *


def main():
    modest()
    output=ROOT/'results/stage-integrity.json'
    assert not output.exists()
    seals=list(BRANCH.glob('*/results/stage-integrity.json'))+[BRANCH/'results/stage-integrity.json']
    by_hash={digest(path):path for path in seals}
    cursor=PARENT/'results/stage-integrity.json'
    parent=json.loads(cursor.read_text())
    seen=set()
    prior_count=0
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
    assert prior_count==7255,prior_count
    checkpoint=POST/'_checkpoints/20261003-pre-condensate-origin/manifest.json'
    original=POST/'.venv-score/Lib/site-packages/camb/cambdll.dll'
    native_library=NATIVE/'camb/cambdll.dll'
    assert digest(checkpoint)==parent['checkpoint_manifest_sha256']
    assert digest(original)==parent['original_library_sha256']
    assert digest(native_library)==parent['native_library_sha256']
    for source in parent['local_source_documents']+parent['primary_pdfs']:
        assert digest(source['path'])==source['sha256']
    scripts=list(ROOT.glob('*.py'))
    for path in scripts:
        compile(path.read_bytes(),str(path),'exec')
    script_hashes={digest(path) for path in scripts}
    packets=list(ROOT.glob('results/*/status.json'))
    assert len(packets)==8,len(packets)
    validation=json.loads((ROOT/'results/validation/status.json').read_text())
    for path in packets:
        packet=json.loads(path.read_text())
        assert packet['state']=='complete' and packet['script_sha256'] in script_hashes
        assert (path.parent/'COMPLETE').is_file()
        if path.parent.name=='validation':
            assert packet['all_current_acceptance_checks_passed'] and all(row['passed'] for row in packet['checks'])
        else:
            assert packet['all_checks_passed'] and all(row['passed'] for row in packet.get('checks',[]))
        for source,expected in packet['input_hashes'].items():
            assert digest(source)==expected,(path,source)
    started=datetime(2026,10,7,6,51,34,tzinfo=timezone.utc)
    workbench=POST.parent/'formalization-workbench'
    changed=[str(path) for path in workbench.rglob('*') if path.is_file() and path.stat().st_mtime>started.timestamp()]
    assert workbench.is_dir() and not changed,changed
    hashes={}
    for directory,directories,files in os.walk(ROOT):
        assert '__pycache__' not in directories,directory
        for name in sorted(files):
            path=Path(directory)/name
            if path!=output:
                hashes[path.relative_to(ROOT).as_posix()]=digest(path)
    write_json(output,dict(state='complete',sealed_at_utc=datetime.now(timezone.utc).isoformat(),
        file_hashes=hashes,parent_seal_sha256=digest(PARENT/'results/stage-integrity.json'),
        prior_sealed_entries_unchanged=prior_count,parent_chain_edges_verified=len(seen)-1,
        checkpoint_manifest_sha256=digest(checkpoint),full_checkpoint_payload_rehashed=False,
        local_source_documents=parent['local_source_documents'],primary_pdfs=parent['primary_pdfs'],
        source_urls=parent['source_urls'],previous_primary_source_urls=parent.get('previous_primary_source_urls',[])+parent['new_primary_source_urls'],
        new_primary_source_urls=validation['new_primary_source_urls'],observational_source_urls=parent['observational_source_urls'],
        local_dependencies={path:digest(path) for path in validation['local_citations']},
        compiled_scripts=[path.name for path in scripts],checked_result_packets=len(packets),
        validation_checks=validation['count'],all_current_acceptance_checks_passed=True,
        prior_goal_turn='progress',regular_adiabatic_gradient_boundary_derived=True,
        native_nonlinear_spatial_gauge_map_derived=True,primordial_second_order_curvature_not_assigned=True,
        matter_loading_and_photon_viscosity_correction_derived=True,
        exact_local_screen_transport_and_quadratic_rotation_derived=True,
        derived_boundary_exported_for_both_models=True,
        full_finite_k_second_order_evolution=False,finite_k1_seed_remainder_measured_not_hidden=True,
        primordial_covariance_not_derived=True,new_empirical_fit=False,
        latest_observational_authority=str(HISTORY/'results/production-primary-refit/status.json'),
        newton_G_inherited_not_derived=True,native_library_reused_read_only=True,
        native_library_sha256=digest(native_library),original_library_sha256=digest(original),
        protected_workbench_recent_modified_file_count=0,
        protected_check_scope='Modification-time scan since06:51:34UTC7October2026, not a full content-hash baseline.',
        maximum_active_compute_workers=1,library_threads=1,active_stage_workers=0,
        github_action=False,subagents=0,global_installation_changed=False,galaxy_work_modified=False,
        conclusion='Derived constrained regular adiabatic seed with neutrino shear, native nonlinear gauge map and matter/opacity corrections; exported particular and independent-primordial boundary columns for both retained models. Derived and checked exact polarization-screen transport. Next assemble and evolve the nonparallel constrained finite-wave response with start-time/constraint controls.'))
    print(json.dumps(dict(state='complete',sealed_files=len(hashes),prior_entries_unchanged=prior_count,
        next_prior_count=prior_count+len(hashes),accepted_validation_checks=validation['count'],result_packets=len(packets))),flush=True)


if __name__=='__main__':
    main()
