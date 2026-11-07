from stage168_common import *


def main():
    modest()
    path=ROOT/'results/stage-integrity.json'
    assert not path.exists()
    validation=verify_packet(ROOT/'results/validation')
    assert validation['all_checks_passed'] and validation['accepted_scope_verified']
    for filename,sha in validation['consumed_and_immediate_rehashed'].items():
        assert digest(filename)==sha,filename
    for filename,sha in validation['input_hashes'].items():
        assert digest(filename)==sha,filename
    assert (ROOT/'RESULTS.md').exists() and (ROOT/'RUN-NOTES.md').exists()
    assert not list(ROOT.rglob('__pycache__'))
    parent=ancestors()[PARENT/'results/stage-integrity.json']
    keys=['checkpoint_manifest_sha256','local_source_documents','primary_pdfs','source_urls','observational_source_urls',
        'original_library_sha256','native_library_sha256','physical_source_scope','retained_local_approximation_histories',
        'raw_subtraction_response_retained','raw_failed_history_response_retained']
    carry={key:value for key,value in parent.items() if key in keys or key.startswith('latest_')}
    payloads={file.relative_to(ROOT).as_posix():digest(file) for file in sorted(ROOT.rglob('*')) if file.is_file() and file!=path}
    summary=json.loads((ROOT/'NUMERICAL-SUMMARY.json').read_text())
    largest=max(sum(file.is_file() for file in directory.iterdir()) for directory in [ROOT,*[value for value in ROOT.rglob('*') if value.is_dir()]])
    assert largest<=500
    packet=dict(state='complete',stage=168,sealed_at_utc=datetime.now(timezone.utc).isoformat(),file_hashes=payloads,
        parent_seal_sha256=PARENT_SEAL,inherited_sealed_payload_count=INHERITED_PAYLOADS,
        prior_archive_full_rehash_performed=False,prior_archive_verification_seal_sha256=parent['prior_archive_verification_seal_sha256'],
        prior_payload_verification_scope='ImmediateStage167 and consumed inputs rehashed;older archive inherited through seals.',
        consumed_and_immediate_rehashed=validation['consumed_and_immediate_rehashed'],prior_files_rehashed=validation['rehashed_prior_files'],**carry,
        previous_primary_source_urls=parent.get('previous_primary_source_urls',[])+parent['new_primary_source_urls'],new_primary_source_urls=[],
        validation_checks=validation['count'],compiled_scripts=validation['compiled_scripts'],accepted_current_scope_verified=True,
        latest_heldout_final_spectrum=str(ROOT/'NUMERICAL-SUMMARY.json'),
        reference_history_adopted=False,new_response_evolutions=8,new_event_evaluations=0,new_expensive_virtual_coefficients=0,
        baseline_inner_history_rerun=False,baseline_preserved=True,arithmetic_reference_separate=True,
        response_steps=COUNTS,frequency_modes=96,interior_orders=[6,6,6,8,7,7,6],lower_bands_changed=False,
        temperature_curve_changed=False,tolerances_changed=False,incoming_continuum_error_certified=False,global_numerical_error_bound=None,
        independent_raw_physical_source_qualified=False,raw_source_failures=validation['raw_source_failures'],
        retained_failed_checks=parent['retained_failed_checks']+validation['retained_smoke_failures'],
        raw_difference_legacy_gate_retained=True,raw_difference_backward_error_gate=1e-7,
        protected_workbench_recent_modified_file_count=0,protected_check_scope=validation['protected_check_scope'],
        maximum_active_compute_workers=1,active_workers_at_seal=0,library_threads_per_worker=1,
        largest_direct_file_count=largest,largest_payload_bytes=max((ROOT/name).stat().st_size for name in payloads),
        github_action=False,subagents=0,global_installation_changed=False,galaxy_work_modified=False,next_target=summary['next_target'])
    write_json(path,packet)
    assert {file.relative_to(ROOT).as_posix() for file in ROOT.rglob('*') if file.is_file() and file!=path}==set(payloads)
    assert all(digest(ROOT/name)==sha for name,sha in payloads.items())
    print(json.dumps(dict(sealed_files=len(payloads),cumulative_payloads=INHERITED_PAYLOADS+len(payloads),seal_sha256=digest(path))),flush=True)


if __name__=='__main__':
    main()
