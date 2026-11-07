from stage162_common import *
import psutil


def main():
    modest()
    path=ROOT/'results/stage-integrity.json'
    assert not path.exists()
    validation=verify_packet(ROOT/'results/validation')
    assert validation['all_checks_passed'] and validation['accepted_scope_verified']
    for filename,sha in validation['consumed_and_immediate_rehashed'].items():
        assert digest(filename)==sha,filename
    for process in psutil.process_iter(['pid','name','cmdline']):
        if process.pid==os.getpid() or 'python' not in (process.info['name'] or '').lower():
            continue
        command=' '.join(process.info['cmdline'] or []).replace(chr(92),'/')
        assert str(ROOT).replace(chr(92),'/') not in command,(process.pid,command)
    assert (ROOT/'RESULTS.md').exists() and (ROOT/'RUN-NOTES.md').exists()
    assert not list(ROOT.rglob('__pycache__'))
    parent=ancestors()[PARENT/'results/stage-integrity.json']
    keys=['checkpoint_manifest_sha256','local_source_documents','primary_pdfs','source_urls',
        'observational_source_urls','original_library_sha256','native_library_sha256','physical_source_scope',
        'retained_local_approximation_histories','raw_subtraction_response_retained','raw_failed_history_response_retained']
    carry={key:value for key,value in parent.items() if key in keys or key.startswith('latest_')}
    payloads={file.relative_to(ROOT).as_posix():digest(file) for file in sorted(ROOT.rglob('*')) if file.is_file() and file!=path}
    summary=json.loads((ROOT/'NUMERICAL-SUMMARY.json').read_text())
    packet=dict(state='complete',stage=162,sealed_at_utc=datetime.now(timezone.utc).isoformat(),
        file_hashes=payloads,parent_seal_sha256=PARENT_SEAL,inherited_sealed_payload_count=INHERITED_PAYLOADS,
        prior_archive_full_rehash_performed=False,
        prior_archive_verification_seal_sha256=parent['prior_archive_verification_seal_sha256'],
        prior_payload_verification_scope='ImmediateStage161 and consumed inputs rehashed;older archive inherited through seals.',
        consumed_and_immediate_rehashed=validation['consumed_and_immediate_rehashed'],
        prior_files_rehashed=validation['rehashed_prior_files'],**carry,
        previous_primary_source_urls=parent.get('previous_primary_source_urls',[])+parent['new_primary_source_urls'],
        new_primary_source_urls=[],total_scientific_checks=validation['scientific_checks'],
        accepted_scientific_checks=validation['passing_scientific_checks'],
        retained_failed_checks=len(validation['retained_failure_names']),retained_failure_names=validation['retained_failure_names'],
        validation_checks=validation['count'],compiled_scripts=validation['compiled_scripts'],
        accepted_current_scope_verified=True,
        accepted_scope='Completed endpoint incoming4/5/6 accuracy experiment;retained failed full-source moment gates;derived stable-jump repair passes four event probes;paired saved baseline/MTS preserved.',
        latest_endpoint_accuracy=str(ROOT/'NUMERICAL-SUMMARY.json'),
        new_physical_event_nodes=5544,new_virtual_coefficients=len(list((ROOT/'virtual-cache').rglob('*.json'))),
        reused_reference_events=2016,new_response_evolutions=0,stable_jump_probe_events=4,
        response_propagation_allowed=False,moment_readiness_passed=False,response_steps=COUNTS,frequency_modes=96,
        endpoint_orders=[4,5,6],interior_orders=[6,6,6,8,7,7,6],
        lower_bands_changed=False,temperature_curve_changed=False,baseline_inner_history_refined=False,
        earlier_window_history_fixed=True,incoming_continuum_error_certified=False,global_numerical_error_bound=None,
        protected_workbench_recent_modified_file_count=0,protected_check_scope=validation['protected_check_scope'],
        maximum_active_compute_workers=2,active_workers_at_seal=0,library_threads_per_worker=1,
        largest_direct_file_count=validation['largest_direct_file_count'],github_action=False,subagents=0,
        global_installation_changed=False,galaxy_work_modified=False,next_target=summary['next_target'])
    write_json(path,packet)
    print(json.dumps(dict(sealed_files=len(payloads),cumulative_payloads=INHERITED_PAYLOADS+len(payloads),seal_sha256=digest(path))),flush=True)


if __name__=='__main__':
    main()
