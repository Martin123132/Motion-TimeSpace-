from spatial_defect_common import *
import psutil


def main():
    modest()
    output=ROOT/'results/stage-integrity.json'
    assert not output.exists()
    parent=json.loads((PARENT/'results/stage-integrity.json').read_text())
    assert digest(PARENT/'results/stage-integrity.json')==PARENT_SEAL
    validation=json.loads((ROOT/'results/validation/status.json').read_text())
    summary=json.loads((ROOT/'NUMERICAL-SUMMARY.json').read_text())
    assert validation['all_checks_passed'] and validation['accepted_scope_verified']
    verified=set()
    for mapping in [validation['input_hashes'],validation['consumed_and_immediate_rehashed']]:
        for path,sha in mapping.items():
            if path not in verified:
                assert digest(path)==sha,path
                verified.add(path)
    chain=ancestors()
    inherited_count=sum(len(packet['file_hashes']) for packet in chain.values())
    assert inherited_count==206301
    for path,key in [(POST/'_checkpoints/20261003-pre-condensate-origin/manifest.json','checkpoint_manifest_sha256'),
        (POST/'.venv-score/Lib/site-packages/camb/cambdll.dll','original_library_sha256'),
        (BRANCH/'native-heavy-matching-20261007/native/camb/cambdll.dll','native_library_sha256')]:
        assert digest(path)==parent[key],path
    for item in parent['local_source_documents']+parent['primary_pdfs']:
        assert digest(item['path'])==item['sha256'],item['path']
    for process in psutil.process_iter(['pid','name','cmdline']):
        if process.pid==os.getpid() or 'python' not in (process.info['name'] or '').lower():
            continue
        try:
            assert Path(process.cwd()).resolve()!=ROOT,process.info
        except (psutil.NoSuchProcess,psutil.AccessDenied):
            pass
    workbench=POST.parent/'formalization-workbench'
    assert not [path for path in workbench.rglob('*') if path.is_file() and path.stat().st_mtime>STARTED.timestamp()]
    payloads={}
    for directory,directories,files in os.walk(ROOT):
        assert '__pycache__' not in directories
        for name in files:
            path=Path(directory)/name
            assert path.suffix!='.tmp'
            if path!=output:
                payloads[path.relative_to(ROOT).as_posix()]=digest(path)
    keys=['checkpoint_manifest_sha256','local_source_documents','primary_pdfs','source_urls',
        'observational_source_urls','original_library_sha256','native_library_sha256',
        'physical_source_scope','retained_local_approximation_histories',
        'raw_subtraction_response_retained','raw_failed_history_response_retained']
    carry={key:value for key,value in parent.items() if key in keys or key.startswith('latest_')}
    packet=dict(state='complete',stage=131,sealed_at_utc=datetime.now(timezone.utc).isoformat(),
        file_hashes=payloads,parent_seal_sha256=PARENT_SEAL,parent_chain_edges_verified=len(chain)-1,
        inherited_sealed_payload_count=inherited_count,prior_archive_full_rehash_performed=False,
        prior_archive_verification_seal_sha256=parent['prior_archive_verification_seal_sha256'],
        prior_payload_verification_scope='Stage130 immediate payloads and consumed dependencies rehashed;Stage108 archive-wide audit inherited through chain.',
        prior_files_rehashed=validation['rehashed_prior_files'],
        consumed_and_immediate_rehashed=validation['consumed_and_immediate_rehashed'],
        full_checkpoint_payload_rehashed=False,**carry,
        previous_primary_source_urls=parent.get('previous_primary_source_urls',[])+parent['new_primary_source_urls'],
        new_primary_source_urls=[],accepted_scientific_checks=summary['passing_scientific_checks'],
        total_scientific_checks=summary['scientific_checks'],retained_failed_checks=summary['retained_failed_checks'],
        retained_failure_names=summary['failed_by_packet'],validation_checks=validation['count'],
        checked_result_packets=10,compiled_scripts=validation['compiled_scripts'],accepted_current_scope_verified=True,
        latest_spatial_shape_defect_correction=str(ROOT/'NUMERICAL-SUMMARY.json'),
        source_scope='Derived second/third central-moment weak correction on33 temperatures,two windows;paired full and residual response;exact inner adjoint and finite boundary/window contract.',
        completed_backgrounds=['heavy','cold'],pending_backgrounds=[],fixed_frequency_nodes=5265,
        inner_steps=40960,response_steps=2048,original_source_epochs=65,hybrid_source_epochs=139,
        sampled_intervals=[0],changed_candidate_sites=33,full_parent_history_rerun=False,
        inner_evolution_recomputed=False,replayed_inner_steps=0,new_physical_temperature_integrals=0,
        saved_events_and_inner_histories_reused=True,analytic_basis_jets=True,independent_derivative_precision_digits=80,
        full_discrete_adjoint_identity_derived=True,inner_derivative_correction_derived=True,
        inner_derivative_correction_implemented=False,positivity_or_boundary_stability_claim=False,
        sampled_inner_symbols_tested=True,source_correction_uses_measured_error=False,normalization_fitted=False,
        new_high_precision_trajectory=False,full_physical_boundary_flux_budget=False,later_history_carried=False,
        inherited_stage130_failures=17,net_shift_is_claimable_physical_signal=False,
        new_parent_action=False,new_empirical_fit=False,physical_cutoff_fitted=False,
        protected_workbench_recent_modified_file_count=0,
        protected_check_scope='Modification-time scan since10:58:13UTC14October2026,not an unsaved content baseline.',
        maximum_active_compute_workers=1,active_workers_at_seal=0,library_threads=1,
        largest_direct_file_count=validation['largest_direct_file_count'],
        github_action=False,subagents=0,global_installation_changed=False,galaxy_work_modified=False,
        current_goal_turn='progress',next_target=summary['next_target'])
    write_json(output,packet)
    print(json.dumps(dict(state='complete',sealed_files=len(payloads),next_prior_count=inherited_count+len(payloads),
        science_checks=summary['scientific_checks'],passing_science=summary['passing_scientific_checks'],
        retained_failures=summary['retained_failed_checks'],validation_checks=validation['count'],
        seal_sha256=digest(output))),flush=True)


if __name__=='__main__':
    main()
