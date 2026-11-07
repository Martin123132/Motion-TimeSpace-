from stage159_common import *
import psutil


def main():
    modest()
    seal_path=ROOT/'results/stage-integrity.json'
    assert not seal_path.exists()
    parent=ancestors()[PARENT/'results/stage-integrity.json']
    validation=verify_packet(ROOT/'results/validation')
    assert validation['all_checks_passed'] and validation['accepted_scope_verified']
    for filename,sha in validation['consumed_and_immediate_rehashed'].items():
        assert digest(filename)==sha,filename
    for process in psutil.process_iter(['pid','name','cmdline']):
        if process.pid==os.getpid() or 'python' not in (process.info['name'] or '').lower():
            continue
        command=' '.join(process.info['cmdline'] or []).replace('\\','/')
        assert str(ROOT).replace('\\','/') not in command,(process.pid,command)
    assert (ROOT/'RESULTS.md').is_file() and not list(ROOT.rglob('__pycache__'))
    summary=json.loads((ROOT/'NUMERICAL-SUMMARY.json').read_text())
    workbench=POST.parent/'formalization-workbench'
    assert not [path for path in workbench.rglob('*') if path.is_file() and path.stat().st_mtime>STARTED.timestamp()]
    payloads={path.relative_to(ROOT).as_posix():digest(path) for path in sorted(ROOT.rglob('*')) if path.is_file() and path!=seal_path}
    keys=['checkpoint_manifest_sha256','local_source_documents','primary_pdfs','source_urls',
        'observational_source_urls','original_library_sha256','native_library_sha256','physical_source_scope',
        'retained_local_approximation_histories','raw_subtraction_response_retained','raw_failed_history_response_retained']
    carry={key:value for key,value in parent.items() if key in keys or key.startswith('latest_')}
    packet=dict(state='complete',stage=159,sealed_at_utc=datetime.now(timezone.utc).isoformat(),
        file_hashes=payloads,parent_seal_sha256=PARENT_SEAL,inherited_sealed_payload_count=INHERITED_PAYLOADS,
        prior_archive_full_rehash_performed=False,
        prior_archive_verification_seal_sha256=parent['prior_archive_verification_seal_sha256'],
        prior_payload_verification_scope='Immediate Stage158 and consumed sources rehashed;earlier archive inherited through immutable seals.',
        consumed_and_immediate_rehashed=validation['consumed_and_immediate_rehashed'],
        prior_files_rehashed=validation['rehashed_prior_files'],**carry,
        previous_primary_source_urls=parent.get('previous_primary_source_urls',[])+parent['new_primary_source_urls'],
        new_primary_source_urls=[],total_scientific_checks=validation['scientific_checks'],
        accepted_scientific_checks=validation['passing_scientific_checks'],
        retained_failed_checks=len(validation['retained_failure_names']),
        retained_failure_names=validation['retained_failure_names'],validation_checks=validation['count'],
        compiled_scripts=validation['compiled_scripts'],accepted_current_scope_verified=True,
        accepted_scope='Matched order8 replacement of incoming1–3 at H/W/C;3–8 retained atorder7;full D/V/S;paired baseline/MTS response sensitivity',
        latest_incoming_band13_order8=str(ROOT/'NUMERICAL-SUMMARY.json'),
        new_physical_event_nodes=864,new_virtual_coefficients=864,reused_reference_events=756,
        new_response_evolutions=8,response_steps=COUNTS,frequency_modes=96,
        refined_incoming_panels=[[1.,3.]],refined_order=8,retained_band38_order=7,other_panel_order=6,
        temperature_curve_changed=False,baseline_and_old_mts_readout_preserved=True,
        baseline_inner_history_refined=False,incoming_continuum_error_certified=False,
        new_window_inner_feedback_recomputed=False,full_extra_source_history_complete=False,
        interpolation_choices_are_error_bounds=False,protected_workbench_recent_modified_file_count=0,
        protected_check_scope='Modification-time scan since18:13:59UTC18October2026,not a content baseline.',
        maximum_active_compute_workers=2,active_workers_at_seal=0,library_threads_per_worker=1,
        largest_direct_file_count=validation['largest_direct_file_count'],github_action=False,subagents=0,
        global_installation_changed=False,galaxy_work_modified=False,current_goal_turn='progress',
        next_target=summary['next_target'])
    write_json(seal_path,packet)
    print(json.dumps(dict(sealed_files=len(payloads),cumulative_payloads=INHERITED_PAYLOADS+len(payloads),
        seal_sha256=digest(seal_path))),flush=True)


if __name__=='__main__':
    main()
