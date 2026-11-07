import psutil
from turnover_common import *


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
    assert inherited_count==202558
    for path,key in [(POST/'_checkpoints/20261003-pre-condensate-origin/manifest.json','checkpoint_manifest_sha256'),
        (POST/'.venv-score/Lib/site-packages/camb/cambdll.dll','original_library_sha256'),
        (BRANCH/'native-heavy-matching-20261007/native/camb/cambdll.dll','native_library_sha256')]:
        assert digest(path)==parent[key],path
    for item in parent['local_source_documents']+parent['primary_pdfs']:
        assert digest(item['path'])==item['sha256'],item['path']
    workbench=POST.parent/'formalization-workbench'
    assert workbench.is_dir()
    changed=[str(path) for path in workbench.rglob('*') if path.is_file() and path.stat().st_mtime>STARTED.timestamp()]
    assert not changed,changed
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
    packet=dict(state='complete',stage=111,sealed_at_utc=datetime.now(timezone.utc).isoformat(),
        file_hashes=payloads,parent_seal_sha256=PARENT_SEAL,parent_chain_edges_verified=len(chain)-1,
        inherited_sealed_payload_count=inherited_count,prior_archive_full_rehash_performed=False,
        prior_archive_verification_seal_sha256=parent['prior_archive_verification_seal_sha256'],
        prior_payload_verification_scope='Stage110 immediate payloads and consumed dependencies rehashed;Stage108 archive-wide check inherited through signed parents.',
        prior_files_rehashed=len(validation['consumed_and_immediate_rehashed']),
        consumed_and_immediate_rehashed=validation['consumed_and_immediate_rehashed'],
        full_checkpoint_payload_rehashed=False,**carry,
        previous_primary_source_urls=parent.get('previous_primary_source_urls',[])+parent['new_primary_source_urls'],
        new_primary_source_urls=['https://arxiv.org/html/1109.6552v1','https://doi.org/10.1111/j.1365-2966.2011.19786.x'],
        accepted_scientific_checks=validation['passing_scientific_checks'],
        total_scientific_checks=validation['scientific_checks'],
        retained_failed_checks=validation['retained_failed_checks'],
        retained_failure_names=review['expected_failed_by_packet'],validation_checks=validation['count'],
        checked_result_packets=validation['checked_science_packets']+1,
        compiled_scripts=validation['compiled_scripts'],accepted_current_scope_verified=True,
        source_scope=review['accepted_scope'],
        numerical_gate_scope='Conditional core-band prediction at frozen5percent peak-normalized gate;old coarse baseline failures retained,not erased.',
        latest_driven_low_frequency_turnover=str(ROOT/'results/turnover-comparison/status.json'),
        latest_turnover_scale_diagnostic=str(ROOT/'results/turnover-scales/status.json'),
        latest_invariant_soft_transport=str(ROOT/'results/invariant-banks/status.json'),
        authoritative_prediction_folder=str(ROOT/'invariant-half-time2-prediction/runs'),
        autonomous_residual_decay_valid=False,gas_net_transfer_relative_precision_upgraded=False,
        source_frequency_continuum_error_bounded=False,full_source_precision_gate_closed=False,
        conditional_low_frequency_prediction=True,new_driven_reconstructions=20,
        new_soft_velocity_temperature_nodes=65,new_finite_frequency_source_evaluations=0,
        old_interpolation_bias_measured_and_corrected=True,old_predictions_retained=True,
        physical_cutoff_fitted=False,future_core_values_used_in_forcing=False,
        full_spectral_tests_retained=96,modes_removed=0,
        new_parent_history=False,new_empirical_fit=False,new_background_evolution=False,new_parent_action=False,
        full_parent_history_feedback_applied=False,newton_G_inherited_not_derived=True,
        electron_mass_inherited_not_derived=True,control_coefficient_fitted=False,
        infrared_increment_continuation_computed=True,
        infrared_increment_continuation_scope='Conditional downstream soft-domain response only;no matching or feedback into parent history.',
        protected_workbench_recent_modified_file_count=0,
        protected_check_scope='Modification-time scan since19:29:10UTC12October2026;not an unsaved content baseline.',
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
