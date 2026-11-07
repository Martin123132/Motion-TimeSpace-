import psutil
from join_common import *


def main():
    modest()
    output=ROOT/'results/stage-integrity.json'
    assert not output.exists()
    parent=json.loads((PARENT/'results/stage-integrity.json').read_text())
    assert digest(PARENT/'results/stage-integrity.json')==PARENT_SEAL
    validation=json.loads((ROOT/'results/validation/status.json').read_text())
    assert validation['all_checks_passed'] and validation['accepted_scope_verified']
    verified=set()
    for mapping in [validation['input_hashes'],validation['consumed_and_immediate_rehashed']]:
        for path,sha in mapping.items():
            if path not in verified:
                assert digest(path)==sha,path
                verified.add(path)
    chain=ancestors()
    inherited_count=sum(len(packet['file_hashes']) for packet in chain.values())
    assert inherited_count==203164
    for path,key in [(POST/'_checkpoints/20261003-pre-condensate-origin/manifest.json','checkpoint_manifest_sha256'),
        (POST/'.venv-score/Lib/site-packages/camb/cambdll.dll','original_library_sha256'),
        (BRANCH/'native-heavy-matching-20261007/native/camb/cambdll.dll','native_library_sha256')]:
        assert digest(path)==parent[key],path
    for item in parent['local_source_documents']+parent['primary_pdfs']:
        assert digest(item['path'])==item['sha256'],item['path']
    workbench=POST.parent/'formalization-workbench'
    changed=[str(path) for path in workbench.rglob('*') if path.is_file() and path.stat().st_mtime>STARTED.timestamp()]
    assert workbench.is_dir() and not changed,changed
    active=[]
    for process in psutil.process_iter(['pid','name','cmdline']):
        if process.pid==os.getpid() or 'python' not in (process.info['name'] or '').lower():
            continue
        try:
            if Path(process.cwd()).resolve()==ROOT or any(str(ROOT).lower() in word.lower() for word in (process.info['cmdline'] or [])):
                active.append(process.pid)
        except (psutil.NoSuchProcess,psutil.AccessDenied):
            pass
    assert not active,active
    payloads={}
    for directory,directories,files in os.walk(ROOT):
        assert '__pycache__' not in directories
        for name in files:
            path=Path(directory)/name
            assert path.suffix!='.tmp'
            if path!=output:
                payloads[path.relative_to(ROOT).as_posix()]=digest(path)
    review=json.loads((ROOT/'ACCURACY-REVIEW.json').read_text(encoding='utf-8'))
    keys=['checkpoint_manifest_sha256','local_source_documents','primary_pdfs','source_urls',
        'observational_source_urls','original_library_sha256','native_library_sha256',
        'physical_source_scope','retained_local_approximation_histories',
        'raw_subtraction_response_retained','raw_failed_history_response_retained']
    carry={key:value for key,value in parent.items() if key in keys or key.startswith('latest_')}
    packet=dict(state='complete',stage=114,sealed_at_utc=datetime.now(timezone.utc).isoformat(),
        file_hashes=payloads,parent_seal_sha256=PARENT_SEAL,parent_chain_edges_verified=len(chain)-1,
        inherited_sealed_payload_count=inherited_count,prior_archive_full_rehash_performed=False,
        prior_archive_verification_seal_sha256=parent['prior_archive_verification_seal_sha256'],
        prior_payload_verification_scope='Stage113 immediate payloads and consumed dependencies rehashed;Stage108 archive-wide check inherited through parent chain.',
        prior_files_rehashed=len(validation['consumed_and_immediate_rehashed']),
        consumed_and_immediate_rehashed=validation['consumed_and_immediate_rehashed'],full_checkpoint_payload_rehashed=False,**carry,
        previous_primary_source_urls=parent.get('previous_primary_source_urls',[])+parent['new_primary_source_urls'],
        new_primary_source_urls=[],
        accepted_scientific_checks=validation['passing_scientific_checks'],total_scientific_checks=validation['scientific_checks'],
        retained_failed_checks=validation['retained_failed_checks'],retained_failure_names=review['expected_failed_by_packet'],
        validation_checks=validation['count'],checked_result_packets=validation['checked_science_packets']+1,
        compiled_scripts=validation['compiled_scripts'],accepted_current_scope_verified=True,source_scope=review['accepted_scope'],
        latest_join_flux_decomposition=str(ROOT/'results/comparison/status.json'),
        authoritative_prediction_folder=str(ROOT/'results'/review['authoritative_response_packet']),
        exact_bulk_join_product_decomposition=True,join_discarded=False,window_fitted=False,
        composite_residual_identity_derived=True,common_full_frequency_overlap_closed=False,
        paired_gas_exchange=True,stored_moment_subtraction_retained=True,
        parent_gas_relative_failures_retained=True,new_parent_history=False,new_background_evolution=False,
        full_parent_history_feedback_applied=False,conditional_low_frequency_feedback_applied=True,
        iterated_closure_feedback=False,full_finite_frequency_compton_matching_complete=False,
        net_shift_is_claimable_physical_signal=False,source54_uncertainty_recomputed=False,
        new_full_recoil_amplitude_evaluations=0,new_soft_events=0,
        full_spectral_tests_retained=96,modes_removed=0,new_parent_action=False,new_empirical_fit=False,
        physical_cutoff_fitted=False,newton_G_inherited_not_derived=True,electron_mass_inherited_not_derived=True,
        protected_workbench_recent_modified_file_count=0,
        protected_check_scope='Modification-time scan since22:52:29UTC12October2026;not an unsaved content baseline.',
        maximum_active_compute_workers=1,active_workers_at_seal=0,library_threads=1,
        largest_direct_file_count=validation['largest_direct_file_count'],github_action=False,subagents=0,
        global_installation_changed=False,galaxy_work_modified=False,current_goal_turn='progress',
        next_target=review['next_target'],conclusion=review['conclusion'])
    write_json(output,packet)
    print(json.dumps(dict(state='complete',sealed_files=len(payloads),
        next_prior_count=inherited_count+len(payloads),science_checks=validation['scientific_checks'],
        passing_science=validation['passing_scientific_checks'],retained_failures=validation['retained_failed_checks'],
        validation_checks=validation['count'],seal_sha256=digest(output))),flush=True)


if __name__=='__main__':
    main()

