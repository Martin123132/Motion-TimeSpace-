from stage166_common import *
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
    keys=['checkpoint_manifest_sha256','local_source_documents','primary_pdfs','source_urls','observational_source_urls',
        'original_library_sha256','native_library_sha256','physical_source_scope','retained_local_approximation_histories',
        'raw_subtraction_response_retained','raw_failed_history_response_retained']
    carry={key:value for key,value in parent.items() if key in keys or key.startswith('latest_')}
    payloads={file.relative_to(ROOT).as_posix():digest(file) for file in sorted(ROOT.rglob('*')) if file.is_file() and file!=path}
    summary=json.loads((ROOT/'NUMERICAL-SUMMARY.json').read_text())
    packet=dict(state='complete',stage=166,sealed_at_utc=datetime.now(timezone.utc).isoformat(),file_hashes=payloads,
        parent_seal_sha256=PARENT_SEAL,inherited_sealed_payload_count=INHERITED_PAYLOADS,
        prior_archive_full_rehash_performed=False,prior_archive_verification_seal_sha256=parent['prior_archive_verification_seal_sha256'],
        prior_payload_verification_scope='ImmediateStage165 and consumed inputs rehashed;older archive inherited through seals.',
        consumed_and_immediate_rehashed=validation['consumed_and_immediate_rehashed'],prior_files_rehashed=validation['rehashed_prior_files'],**carry,
        previous_primary_source_urls=parent.get('previous_primary_source_urls',[])+parent['new_primary_source_urls'],new_primary_source_urls=[],
        validation_checks=validation['count'],compiled_scripts=validation['compiled_scripts'],accepted_current_scope_verified=True,
        latest_endpoint_twofold_response=str(ROOT/'NUMERICAL-SUMMARY.json'),source_qualified=summary['source_qualified'],
        numerical_integrity_passed=summary['numerical_integrity_passed'],response_convergence_passed=summary['convergence_passed'],
        reference_history_replayed=True,reference_history_adopted=False,new_response_evolutions=16,
        new_event_evaluations=0,new_expensive_virtual_coefficients=0,high_low_response_retained=True,
        baseline_inner_history_rerun=False,baseline_preserved=True,arithmetic_reference_separate=True,
        response_steps=COUNTS,frequency_modes=96,interior_orders=[6,6,6,8,7,7,6],lower_bands_changed=False,
        temperature_curve_changed=False,tolerances_changed=False,incoming_continuum_error_certified=False,global_numerical_error_bound=None,
        retained_failed_checks=validation['retained_failed_checks'],corrected_inherited_test_denominator=True,
        protected_workbench_recent_modified_file_count=0,protected_check_scope=validation['protected_check_scope'],
        maximum_active_compute_workers=2,active_workers_at_seal=0,library_threads_per_worker=1,largest_direct_file_count=validation['largest_direct_file_count'],
        largest_payload_bytes=max((ROOT/name).stat().st_size for name in payloads),publication_requires_packaging=True,
        github_action=False,subagents=0,global_installation_changed=False,galaxy_work_modified=False,next_target=summary['next_target'])
    write_json(path,packet)
    print(json.dumps(dict(sealed_files=len(payloads),cumulative_payloads=INHERITED_PAYLOADS+len(payloads),seal_sha256=digest(path))),flush=True)


if __name__=='__main__':
    main()
