from next_intervals_common import *
import psutil


def main():
    modest()
    output=ROOT/'results/stage-integrity.json'
    assert not output.exists()
    assert digest(PARENT/'results/stage-integrity.json')==PARENT_SEAL
    parent=json.loads((PARENT/'results/stage-integrity.json').read_text())
    validation=local_packet(ROOT/'results/validation')
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
    assert inherited_count==209951
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
    packet=dict(state='complete',stage=136,sealed_at_utc=datetime.now(timezone.utc).isoformat(),
        file_hashes=payloads,parent_seal_sha256=PARENT_SEAL,parent_chain_edges_verified=len(chain)-1,
        inherited_sealed_payload_count=inherited_count,prior_archive_full_rehash_performed=False,
        prior_archive_verification_seal_sha256=parent['prior_archive_verification_seal_sha256'],
        prior_payload_verification_scope='Stage135 immediate payloads and consumed dependencies rehashed;Stage108 archive-wide audit inherited through chain.',
        prior_files_rehashed=validation['rehashed_prior_files'],consumed_and_immediate_rehashed=validation['consumed_and_immediate_rehashed'],
        full_checkpoint_payload_rehashed=False,**carry,
        previous_primary_source_urls=parent.get('previous_primary_source_urls',[])+parent['new_primary_source_urls'],new_primary_source_urls=[],
        accepted_scientific_checks=summary['passing_scientific_checks'],total_scientific_checks=summary['scientific_checks'],
        retained_failed_checks=summary['retained_failed_checks'],retained_failure_names=summary['failed_by_packet'],
        validation_checks=validation['count'],checked_result_packets=len(summary['packet_names'])+1,
        compiled_scripts=validation['compiled_scripts'],accepted_current_scope_verified=True,
        latest_next_eight_interval_cubic_carry=str(ROOT/'NUMERICAL-SUMMARY.json'),
        source_scope='Corrected two-level carry from10240 to15360;cached common source and independent physical events at all257 new-block sites in both windows.',
        completed_backgrounds=['heavy','cold'],pending_backgrounds=[],fixed_frequency_nodes=5265,
        inner_steps=40960,response_steps=2048,original_source_epochs=65,hybrid_source_epochs=summary['source_knots'],
        sampled_intervals=list(range(LAST_STEP//640)),continuous_source_sites=LAST_STEP//20+1,new_source_sites=(LAST_STEP-FIRST_STEP)//20,full_parent_history_rerun=False,
        inner_evolution_recomputed=True,replayed_inner_steps=2*(LAST_STEP-FIRST_STEP),continuous_inner_stop=LAST_STEP,
        corrected_steps_per_background=LAST_STEP-FIRST_STEP,new_physical_temperature_event_evaluations=248,saved_endpoint_events_reused=9,
        accepted_candidate_resets_changed_endpoint=False,both_bdf_levels_retained=True,new_memory_reset_diagnostic=False,independent_physical_sites_per_window=len(SOURCE_STEPS),
        source_restore_step=LAST_STEP+20,full_later_state_history_carried=False,weighted_norm_is_physical_energy=False,
        source_correction_uses_measured_error=False,normalization_fitted=False,formal_interval_arithmetic_certificate=False,
        inherited_stage135_failures=46,net_shift_is_claimable_physical_signal=False,new_parent_action=False,new_empirical_fit=False,
        physical_cutoff_fitted=False,protected_workbench_recent_modified_file_count=0,
        protected_check_scope='Modification-time scan since18:06:34UTC14October2026,not an unsaved content baseline.',
        maximum_active_compute_workers=1,active_workers_at_seal=0,library_threads=1,
        largest_direct_file_count=validation['largest_direct_file_count'],github_action=False,subagents=0,
        global_installation_changed=False,galaxy_work_modified=False,previous_goal_turn='progress',current_goal_turn='progress',
        next_target=summary['next_target'])
    write_json(output,packet)
    print(json.dumps(dict(state='complete',sealed_files=len(payloads),next_prior_count=inherited_count+len(payloads),
        science_checks=summary['scientific_checks'],passing_science=summary['passing_scientific_checks'],
        retained_failures=summary['retained_failed_checks'],validation_checks=validation['count'],seal_sha256=digest(output))),flush=True)


if __name__=='__main__':
    main()
