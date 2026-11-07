from stage160_common import *
import psutil


def main():
    modest()
    seal_path=ROOT/'results/stage-integrity.json'
    assert not seal_path.exists()
    parent=ancestors()[PARENT/'results/stage-integrity.json']
    analysis=verify_packet(ROOT/'results/analysis')
    validation=verify_packet(ROOT/'results/validation')
    assert validation['all_checks_passed'] and validation['accepted_scope_verified']
    for filename,sha in analysis['consumed_prior_hashes'].items():
        assert digest(filename)==sha,filename
    for process in psutil.process_iter(['pid','name','cmdline']):
        if process.pid==os.getpid() or 'python' not in (process.info['name'] or '').lower():
            continue
        command=' '.join(process.info['cmdline'] or []).replace(chr(92),'/')
        assert str(ROOT).replace(chr(92),'/') not in command,(process.pid,command)
    assert (ROOT/'RESULTS.md').is_file() and not list(ROOT.rglob('__pycache__'))
    summary=json.loads((ROOT/'NUMERICAL-SUMMARY.json').read_text())
    workbench=POST.parent/'formalization-workbench'
    assert not [path for path in workbench.rglob('*') if path.is_file() and path.stat().st_mtime>STARTED.timestamp()]
    payloads={path.relative_to(ROOT).as_posix():digest(path) for path in sorted(ROOT.rglob('*')) if path.is_file() and path!=seal_path}
    keys=['checkpoint_manifest_sha256','local_source_documents','primary_pdfs','source_urls',
        'observational_source_urls','original_library_sha256','native_library_sha256','physical_source_scope',
        'retained_local_approximation_histories','raw_subtraction_response_retained','raw_failed_history_response_retained']
    carry={key:value for key,value in parent.items() if key in keys or key.startswith('latest_')}
    packet=dict(state='complete',stage=160,sealed_at_utc=datetime.now(timezone.utc).isoformat(),
        file_hashes=payloads,parent_seal_sha256=PARENT_SEAL,inherited_sealed_payload_count=INHERITED_PAYLOADS,
        prior_archive_full_rehash_performed=False,
        prior_archive_verification_seal_sha256=parent['prior_archive_verification_seal_sha256'],
        prior_payload_verification_scope='Immediate Stage159 and consumed older inputs rehashed;earlier archive inherited by seals.',
        consumed_and_immediate_rehashed=analysis['consumed_prior_hashes'],
        prior_files_rehashed=validation['rehashed_prior_files'],**carry,
        previous_primary_source_urls=parent.get('previous_primary_source_urls',[])+parent['new_primary_source_urls'],
        new_primary_source_urls=[],total_scientific_checks=validation['scientific_checks'],
        accepted_scientific_checks=validation['passing_scientific_checks'],
        retained_failed_checks=len(validation['retained_failure_names']),
        retained_failure_names=validation['retained_failure_names'],validation_checks=validation['count'],
        compiled_scripts=4,accepted_current_scope_verified=True,
        accepted_scope='Saved order6–8 mixed-panel sensitivity allowances;full saved D/V/S reconstruction;paired unchanged baseline/MTS',
        latest_integration_allowance=str(ROOT/'NUMERICAL-SUMMARY.json'),
        new_physical_event_nodes=0,new_virtual_coefficients=0,new_response_evolutions=0,
        reused_order5_6_event_records=8316,frequency_modes=96,
        mixed_incoming_orders=[6,6,6,8,7,6,6],temperature_curve_changed=False,
        baseline_inner_history_refined=False,incoming_continuum_error_certified=False,
        pure_latest_cubic_defect_response_available=False,global_numerical_error_bound=None,
        protected_workbench_recent_modified_file_count=0,
        protected_check_scope='Modification-time scan since19:22UTC18October2026,not a content baseline.',
        maximum_active_compute_workers=1,active_workers_at_seal=0,library_threads_per_worker=1,
        largest_direct_file_count=validation['largest_direct_file_count'],github_action=False,subagents=0,
        global_installation_changed=False,galaxy_work_modified=False,next_target=summary['next_target'])
    write_json(seal_path,packet)
    print(json.dumps(dict(sealed_files=len(payloads),cumulative_payloads=INHERITED_PAYLOADS+len(payloads),
        seal_sha256=digest(seal_path))),flush=True)


if __name__=='__main__':
    main()
