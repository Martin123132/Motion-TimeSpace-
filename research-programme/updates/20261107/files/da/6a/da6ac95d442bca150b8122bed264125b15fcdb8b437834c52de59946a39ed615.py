from stage146_precision_common import *
import psutil


def main():
    modest()
    seal_path=ROOT/'results/stage-integrity.json'
    assert not seal_path.exists()
    chain=ancestors()
    parent_packet=chain[PARENT/'results/stage-integrity.json']
    validation=verify_packet(ROOT/'results/validation')
    assert validation['all_checks_passed'] and validation['accepted_scope_verified']
    for filename,sha in validation['consumed_and_immediate_rehashed'].items():
        assert digest(filename)==sha,filename
    for process in psutil.process_iter(['pid','name','cmdline']):
        if process.pid==os.getpid() or 'python' not in (process.info['name'] or '').lower():
            continue
        command=process.info['cmdline'] or []
        assert not any(str(ROOT).lower() in str(item).lower() for item in command)
    assert not list(ROOT.rglob('__pycache__'))
    workbench=POST.parent/'formalization-workbench'
    assert not [path for path in workbench.rglob('*') if path.is_file() and path.stat().st_mtime>STARTED.timestamp()]
    summary=json.loads((ROOT/'NUMERICAL-SUMMARY.json').read_text())
    assert (ROOT/'RESULTS.md').exists()
    payloads={}
    for path in sorted(ROOT.rglob('*')):
        if path.is_file() and path!=seal_path:
            assert path.suffix!='.tmp'
            payloads[path.relative_to(ROOT).as_posix()]=digest(path)
    keys=['checkpoint_manifest_sha256','local_source_documents','primary_pdfs','source_urls',
          'observational_source_urls','original_library_sha256','native_library_sha256',
          'physical_source_scope','retained_local_approximation_histories',
          'raw_subtraction_response_retained','raw_failed_history_response_retained']
    carry={key:value for key,value in parent_packet.items() if key in keys or key.startswith('latest_')}
    packet=dict(state='complete',stage=146,sealed_at_utc=datetime.now(timezone.utc).isoformat(),
        file_hashes=payloads,parent_seal_sha256=PARENT_SEAL,
        parent_chain_edges_verified=len(chain)-1,inherited_sealed_payload_count=INHERITED_PAYLOADS,
        prior_archive_full_rehash_performed=False,
        prior_archive_verification_seal_sha256=parent_packet['prior_archive_verification_seal_sha256'],
        prior_payload_verification_scope='Stage145 immediate payloads and all consumed dependencies rehashed; older archive-wide verification inherited through immutable seal chain.',
        consumed_and_immediate_rehashed=validation['consumed_and_immediate_rehashed'],
        prior_files_rehashed=validation['rehashed_prior_files'],**carry,
        previous_primary_source_urls=parent_packet.get('previous_primary_source_urls',[])+parent_packet['new_primary_source_urls'],
        new_primary_source_urls=[],total_scientific_checks=summary['scientific_checks'],
        accepted_scientific_checks=summary['passing_scientific_checks'],
        retained_failed_checks=summary['retained_failed_checks'],retained_failure_names=summary['failed_by_packet'],
        inherited_stage145_flags=6,validation_checks=validation['count'],compiled_scripts=validation['compiled_scripts'],
        accepted_current_scope_verified=True,accepted_scope=summary['accepted_scope'],
        allowed_routes=summary['allowed_routes'],latest_saved_event_precision_repair=str(ROOT/'NUMERICAL-SUMMARY.json'),
        reused_event_nodes=29952,new_physical_event_nodes=0,new_virtual_coefficients=0,
        frequency_modes=96,response_steps_per_phase=1024,extra_source_interval=[.5,.75],
        represented_source_union=[.25,.75],final_epoch_scale=1e-5,
        new_window_inner_feedback_recomputed=False,event_quadrature_error_bounded=False,
        full_extra_source_history_complete=False,interpolation_choices_are_error_bounds=False,
        literal_frozen_forecasts_preserved=True,baseline_and_old_mts_preserved=True,
        protected_workbench_recent_modified_file_count=0,
        protected_check_scope='Modification-time scan since13:35:45UTC16October2026,not a content baseline.',
        maximum_active_compute_workers=2,active_workers_at_seal=0,library_threads=1,
        largest_direct_file_count=validation['largest_direct_file_count'],github_action=False,
        subagents=0,global_installation_changed=False,galaxy_work_modified=False,
        current_goal_turn='progress',next_target=summary['next_target'])
    write_json(seal_path,packet)
    print(json.dumps(dict(sealed_files=len(payloads),cumulative_payloads=INHERITED_PAYLOADS+len(payloads),
        seal_sha256=digest(seal_path),validation_checks=validation['count'])),flush=True)


if __name__=='__main__':
    main()
