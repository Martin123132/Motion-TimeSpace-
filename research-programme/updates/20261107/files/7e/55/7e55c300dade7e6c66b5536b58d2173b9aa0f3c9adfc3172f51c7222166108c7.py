from stage150_colder_common import *
import psutil


def main():
    modest()
    seal_path=ROOT/'results/stage-integrity.json'
    assert not seal_path.exists()
    parent_packet=ancestors()[PARENT/'results/stage-integrity.json']
    validation=verify_packet(ROOT/'results/validation')
    assert validation['all_checks_passed'] and validation['accepted_scope_verified']
    for filename,sha in validation['consumed_and_immediate_rehashed'].items():
        assert digest(filename)==sha,filename
    for process in psutil.process_iter(['pid','name','cmdline']):
        if process.pid==os.getpid() or 'python' not in (process.info['name'] or '').lower():
            continue
        command=' '.join(process.info['cmdline'] or []).replace('\\','/')
        assert str(ROOT).replace('\\','/') not in command,(process.pid,command)
    assert not list(ROOT.rglob('__pycache__'))
    summary=json.loads((ROOT/'NUMERICAL-SUMMARY.json').read_text())
    assert (ROOT/'RESULTS.md').exists()
    workbench=POST.parent/'formalization-workbench'
    assert not [path for path in workbench.rglob('*') if path.is_file() and path.stat().st_mtime>STARTED.timestamp()]
    payloads={path.relative_to(ROOT).as_posix():digest(path) for path in sorted(ROOT.rglob('*'))
              if path.is_file() and path!=seal_path}
    keys=['checkpoint_manifest_sha256','local_source_documents','primary_pdfs','source_urls',
          'observational_source_urls','original_library_sha256','native_library_sha256',
          'physical_source_scope','retained_local_approximation_histories',
          'raw_subtraction_response_retained','raw_failed_history_response_retained']
    carry={key:value for key,value in parent_packet.items() if key in keys or key.startswith('latest_')}
    packet=dict(state='complete',stage=150,sealed_at_utc=datetime.now(timezone.utc).isoformat(),
        file_hashes=payloads,parent_seal_sha256=PARENT_SEAL,inherited_sealed_payload_count=INHERITED_PAYLOADS,
        prior_archive_full_rehash_performed=False,
        prior_archive_verification_seal_sha256=parent_packet['prior_archive_verification_seal_sha256'],
        prior_payload_verification_scope='Immediate Stage149 and consumed sources rehashed; earlier archive verification inherited through immutable seals.',
        consumed_and_immediate_rehashed=validation['consumed_and_immediate_rehashed'],
        prior_files_rehashed=validation['rehashed_prior_files'],**carry,
        previous_primary_source_urls=parent_packet.get('previous_primary_source_urls',[])+parent_packet['new_primary_source_urls'],
        new_primary_source_urls=[],total_scientific_checks=summary['scientific_checks'],
        accepted_scientific_checks=summary['passing_scientific_checks'],
        retained_failed_checks=summary['retained_failed_checks'],retained_failure_names=summary['failed_by_packet'],
        validation_checks=validation['count'],compiled_scripts=validation['compiled_scripts'],
        accepted_current_scope_verified=True,accepted_scope=summary['accepted_scope'],
        latest_terminal_colder_temperature_holdout=str(ROOT/'NUMERICAL-SUMMARY.json'),
        primary_prediction_passed=summary['primary_prediction_passed'],prediction_passed=summary['prediction_passed'],
        allowed_routes=summary['allowed_routes'],
        convergence_passed=summary['convergence_passed'],frequency_modes=96,response_steps_per_phase=COUNTS,
        new_physical_event_nodes=5616,new_virtual_coefficients=1008,holdout_fraction=.9375,
        extra_source_interval=[.75,1.],represented_source_union=[.25,1.],final_epoch_scale=1e-5,
        baseline_and_old_mts_readout_preserved=True,baseline_inner_history_refined=False,
        new_window_inner_feedback_recomputed=False,event_quadrature_error_bounded=False,
        full_extra_source_history_complete=False,interpolation_choices_are_error_bounds=False,
        protected_workbench_recent_modified_file_count=0,
        protected_check_scope='Modification-time scan since23:16:57UTC16October2026,not a content baseline.',
        maximum_active_compute_workers=2,active_workers_at_seal=0,library_threads=1,
        largest_direct_file_count=validation['largest_direct_file_count'],github_action=False,subagents=0,
        global_installation_changed=False,galaxy_work_modified=False,current_goal_turn='progress',
        next_target=summary['next_target'])
    write_json(seal_path,packet)
    print(json.dumps(dict(sealed_files=len(payloads),cumulative_payloads=INHERITED_PAYLOADS+len(payloads),
        seal_sha256=digest(seal_path),primary_prediction_passed=summary['primary_prediction_passed'],
        convergence_passed=summary['convergence_passed'])),flush=True)


if __name__=='__main__':
    main()
