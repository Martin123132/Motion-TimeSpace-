from interpolation_common import *
import psutil


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
    assert inherited_count==205877
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
    assert workbench.is_dir() and not [path for path in workbench.rglob('*') if path.is_file() and path.stat().st_mtime>STARTED.timestamp()]
    payloads={}
    for directory,directories,files in os.walk(ROOT):
        assert '__pycache__' not in directories
        for name in files:
            path=Path(directory)/name
            assert path.suffix!='.tmp'
            if path!=output:
                payloads[path.relative_to(ROOT).as_posix()]=digest(path)
    review=json.loads((ROOT/'ACCURACY-REVIEW.json').read_text())
    keys=['checkpoint_manifest_sha256','local_source_documents','primary_pdfs','source_urls',
        'observational_source_urls','original_library_sha256','native_library_sha256',
        'physical_source_scope','retained_local_approximation_histories',
        'raw_subtraction_response_retained','raw_failed_history_response_retained']
    carry={key:value for key,value in parent.items() if key in keys or key.startswith('latest_')}
    packet=dict(state='complete',stage=128,sealed_at_utc=datetime.now(timezone.utc).isoformat(),
        file_hashes=payloads,parent_seal_sha256=PARENT_SEAL,parent_chain_edges_verified=len(chain)-1,
        inherited_sealed_payload_count=inherited_count,prior_archive_full_rehash_performed=False,
        prior_archive_verification_seal_sha256=parent['prior_archive_verification_seal_sha256'],
        prior_payload_verification_scope='Stage127 immediate payloads and consumed dependencies rehashed;Stage108 archive-wide audit inherited through sealed chain.',
        prior_files_rehashed=len(validation['consumed_and_immediate_rehashed']),
        consumed_and_immediate_rehashed=validation['consumed_and_immediate_rehashed'],full_checkpoint_payload_rehashed=False,**carry,
        previous_primary_source_urls=parent.get('previous_primary_source_urls',[])+parent['new_primary_source_urls'],new_primary_source_urls=[],
        accepted_scientific_checks=validation['passing_scientific_checks'],total_scientific_checks=validation['scientific_checks'],
        retained_failed_checks=validation['retained_failed_checks'],retained_failure_names=review['expected_failed_by_packet'],
        combined_original_response_failures=review['combined_original_response_failures'],validation_checks=validation['count'],
        checked_result_packets=5,compiled_scripts=validation['compiled_scripts'],accepted_current_scope_verified=True,
        source_scope=review['accepted_scope'],completed_backgrounds=['heavy','cold'],pending_backgrounds=[],
        latest_temperature_source_interpolation=str(ROOT/'NUMERICAL-SUMMARY.json'),
        fixed_frequency_nodes=5265,inner_steps=40960,response_steps=2048,original_source_epochs=65,hybrid_source_epochs=138,
        sampled_intervals=[0],changed_candidate_sites=31,saved_state_sites=33,new_source_points=0,
        full_parent_history_rerun=False,full_history_source_refinement=False,inner_coefficients_resampled=False,
        inner_evolution_recomputed=False,replayed_inner_steps=0,source_operators_reused=True,new_temperature_integrals=0,
        energy_moment_normalization_derived=True,normalization_fitted=False,operator_and_state_product_terms_retained=True,
        direct_energy_row_retained=True,initial_matching_tuned=False,other_source_intervals_changed=False,
        paired_conditional_response_recalculated=True,inner_source_consistency_established=False,
        new_high_precision_solves=False,inherited_stage118_precision_stress_results=True,
        precision_scope='No new high-precision trajectory;Stage127 paired arithmetic reference and Stage118 response stress tests are inherited.',
        full_parent_history_feedback_applied=False,new_background_evolution=False,
        full_finite_frequency_compton_matching_complete=False,net_shift_is_claimable_physical_signal=False,
        new_parent_action=False,new_empirical_fit=False,physical_cutoff_fitted=False,
        newton_G_inherited_not_derived=True,electron_mass_inherited_not_derived=True,
        protected_workbench_recent_modified_file_count=0,
        protected_check_scope='Modification-time scan since09:39:15UTC14October2026;not an unsaved content baseline.',
        maximum_active_compute_workers=1,active_workers_at_seal=0,library_threads=1,
        largest_direct_file_count=validation['largest_direct_file_count'],github_action=False,subagents=0,
        global_installation_changed=False,galaxy_work_modified=False,current_goal_turn='progress',
        next_target=review['next_target'],conclusion=review['conclusion'])
    write_json(output,packet)
    print(json.dumps(dict(state='complete',sealed_files=len(payloads),next_prior_count=inherited_count+len(payloads),
        science_checks=validation['scientific_checks'],passing_science=validation['passing_scientific_checks'],
        retained_failures=validation['retained_failed_checks'],validation_checks=validation['count'],seal_sha256=digest(output))),flush=True)


if __name__=='__main__':
    main()
