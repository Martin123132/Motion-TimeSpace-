from adjacent_source_common import *
import psutil


def main():
    modest()
    path=ROOT/'results/stage-integrity.json'
    assert not path.exists()
    chain=ancestors()
    parent=chain[PARENT/'results/stage-integrity.json']
    validation=verify_packet(ROOT/'results/validation')
    assert validation['all_checks_passed'] and validation['accepted_scope_verified']
    for filename,sha in validation['consumed_and_immediate_rehashed'].items():
        assert digest(filename)==sha,filename
    summary=json.loads((ROOT/'NUMERICAL-SUMMARY.json').read_text())
    for process in psutil.process_iter(['pid','name','cmdline']):
        if process.pid==os.getpid():
            continue
        command=process.info['cmdline'] or []
        assert not any(str(ROOT/'evaluate_adjacent_events.py').lower()==str(item).lower() for item in command),process.pid
    workbench=POST.parent/'formalization-workbench'
    assert not [item for item in workbench.rglob('*') if item.is_file() and item.stat().st_mtime>STARTED.timestamp()]
    assert not list(ROOT.rglob('__pycache__'))
    payloads={}
    for item in sorted(ROOT.rglob('*')):
        if item.is_file() and item!=path:
            assert item.suffix!='.tmp',item
            payloads[item.relative_to(ROOT).as_posix()]=digest(item)
    keys=['checkpoint_manifest_sha256','local_source_documents','primary_pdfs','source_urls',
          'observational_source_urls','original_library_sha256','native_library_sha256',
          'physical_source_scope','retained_local_approximation_histories',
          'raw_subtraction_response_retained','raw_failed_history_response_retained']
    carry={key:value for key,value in parent.items() if key in keys or key.startswith('latest_')}
    packet=dict(state='complete',stage=143,sealed_at_utc=datetime.now(timezone.utc).isoformat(),
                file_hashes=payloads,parent_seal_sha256=PARENT_SEAL,
                parent_chain_edges_verified=len(chain)-1,inherited_sealed_payload_count=219863,
                prior_archive_full_rehash_performed=False,
                prior_archive_verification_seal_sha256=parent['prior_archive_verification_seal_sha256'],
                prior_payload_verification_scope='Stage142 immediate payloads and consumed dependencies rehashed;archive-wide verification inherited through the seal chain.',
                prior_files_rehashed=validation['rehashed_prior_files'],
                consumed_and_immediate_rehashed=validation['consumed_and_immediate_rehashed'],**carry,
                previous_primary_source_urls=parent.get('previous_primary_source_urls',[])+parent['new_primary_source_urls'],
                new_primary_source_urls=[],total_scientific_checks=summary['scientific_checks'],
                accepted_scientific_checks=summary['passing_scientific_checks'],
                retained_failed_checks=summary['retained_failed_checks'],
                retained_failure_names=summary['failed_by_packet'],
                inherited_stage142_energy_input_flags=16,inherited_stage141_response_flags=10,
                validation_checks=validation['count'],compiled_scripts=validation['compiled_scripts'],
                accepted_current_scope_verified=True,latest_adjacent_physical_source_window=str(ROOT/'NUMERICAL-SUMMARY.json'),
                newly_evaluated_temperature_fractions=[.625,.75],reused_temperature_fraction=.5,
                new_physical_event_nodes=11232,new_virtual_coefficients=2016,
                extra_source_window_this_stage=[.5,.75],represented_source_union=[.25,.75],
                full_extra_source_history_complete=False,final_epoch_scale=1e-5,
                new_window_inner_feedback_recomputed=False,event_quadrature_error_bounded=False,
                new_empirical_fit=False,source_replaced_by_temperature_scaling=False,
                weighted_norm_is_physical_energy=False,baseline_and_old_mts_preserved=True,
                protected_workbench_recent_modified_file_count=0,
                protected_check_scope='Modification-time scan since20:32:11UTC15October2026,not an unsaved content baseline.',
                maximum_active_compute_workers=2,active_workers_at_seal=0,library_threads=1,
                largest_direct_file_count=validation['largest_direct_file_count'],
                github_action=False,subagents=0,global_installation_changed=False,
                galaxy_work_modified=False,current_goal_turn='progress',next_target=summary['next_target'])
    write_json(path,packet)
    print(json.dumps(dict(sealed_files=len(payloads),cumulative_payloads=219863+len(payloads),
                          seal_sha256=digest(path),validation_checks=validation['count'])),flush=True)


if __name__=='__main__':
    main()
