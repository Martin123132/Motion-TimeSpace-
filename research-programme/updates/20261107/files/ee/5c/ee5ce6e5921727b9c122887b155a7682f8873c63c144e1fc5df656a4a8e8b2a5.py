import psutil
from residual_kinetic_common import *


def main():
    modest()
    output=ROOT/'results/stage-integrity.json'
    assert not output.exists()
    parent=json.loads((PARENT/'results/stage-integrity.json').read_text())
    assert digest(PARENT/'results/stage-integrity.json')==PARENT_SEAL
    validation=json.loads((ROOT/'results/validation/status.json').read_text())
    assert validation['all_checks_passed'] and validation['accepted_scope_verified']
    for mapping in [validation['input_hashes'],validation['consumed_and_immediate_rehashed']]:
        for path,sha in mapping.items():
            assert digest(path)==sha,path
    chain=ancestors()
    inherited_count=sum(len(packet['file_hashes']) for packet in chain.values())
    assert inherited_count==202515
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
    review=json.loads((ROOT/'ACCURACY-REVIEW.json').read_text())
    keys=['checkpoint_manifest_sha256','local_source_documents','primary_pdfs','source_urls',
        'observational_source_urls','original_library_sha256','native_library_sha256',
        'latest_physical_source_histories','physical_source_scope','retained_local_approximation_histories',
        'latest_driven_tail_histories','latest_observational_authority','latest_population_source_projections',
        'latest_population_spectral_source','latest_nodewise_remainder_diagnostic',
        'latest_nonmidpoint_remainder_pilot','latest_two_temperature_frequency_comparison',
        'latest_late_three_rule_frequency_comparison','latest_conditional_history_response',
        'latest_source_window_response','raw_subtraction_response_retained','raw_failed_history_response_retained',
        'latest_temperature_distortion_projection','latest_stable_physical_spectral_readout',
        'latest_mu_y_residual_comparison','latest_finite_band_moment_control','latest_residual_physical_readout']
    carry={key:parent[key] for key in keys}
    packet=dict(state='complete',sealed_at_utc=datetime.now(timezone.utc).isoformat(),file_hashes=payloads,
        parent_seal_sha256=PARENT_SEAL,parent_chain_edges_verified=len(chain)-1,
        inherited_sealed_payload_count=inherited_count,prior_archive_full_rehash_performed=False,
        prior_archive_verification_seal_sha256=parent['prior_archive_verification_seal_sha256'],
        prior_payload_verification_scope='Stage109 immediate payloads and consumed dependencies rehashed;Stage108 archive-wide check inherited through Stage109.',
        prior_files_rehashed=len(validation['consumed_and_immediate_rehashed']),
        consumed_and_immediate_rehashed=validation['consumed_and_immediate_rehashed'],full_checkpoint_payload_rehashed=False,**carry,
        previous_primary_source_urls=parent.get('previous_primary_source_urls',[])+parent['new_primary_source_urls'],
        new_primary_source_urls=['https://arxiv.org/abs/1109.6552','https://doi.org/10.1111/j.1365-2966.2011.19786.x'],
        accepted_scientific_checks=105,total_scientific_checks=111,retained_failed_checks=6,
        retained_failure_names=review['expected_failed_names'],validation_checks=validation['count'],
        checked_result_packets=5,compiled_scripts=validation['compiled_scripts'],accepted_current_scope_verified=True,
        source_scope=review['accepted_scope'],numerical_gate_scope='Matched projected photon-history,readout and energy-accounting checks;raw tiny net gas-transfer1e-6relative gate remains failed.',
        latest_residual_kinetic_drive=str(ROOT/'results/kinetic-drive/status.json'),
        latest_residual_energy_control=str(ROOT/'results/readout-controls/status.json'),
        latest_baseline_residual_refinement=str(ROOT/'results/baseline-refinement/status.json'),
        latest_residual_drive_interpretation=str(ROOT/'results/interpretation/status.json'),
        autonomous_residual_decay_valid=False,gas_net_transfer_relative_precision_upgraded=False,
        new_virtual_loop_evaluations=0,production_nodes=0,modes_removed=0,full_spectral_tests_retained=96,
        finite_source_recomputed=False,new_empirical_fit=False,new_parent_history=False,
        full_parent_history_feedback_applied=False,new_background_evolution=False,new_parent_action=False,
        newton_G_inherited_not_derived=True,electron_mass_inherited_not_derived=True,control_coefficient_fitted=False,
        source_frequency_continuum_error_bounded=False,full_source_precision_gate_closed=False,
        infrared_increment_continuation_computed=False,instrument_temperature_fit=False,
        protected_workbench_recent_modified_file_count=0,
        protected_check_scope='Modification-time scan since19:13:41UTC12October2026;not an unsaved content baseline.',
        maximum_active_compute_workers=1,active_workers_at_seal=0,library_threads=1,
        largest_direct_file_count=validation['largest_direct_file_count'],github_action=False,subagents=0,
        global_installation_changed=False,galaxy_work_modified=False,current_goal_turn='progress',
        next_target=review['next_target'],conclusion=review['conclusion'])
    write_json(output,packet)
    print(json.dumps(dict(state='complete',sealed_files=len(payloads),next_prior_count=inherited_count+len(payloads),
        science_checks=111,passing_science=105,retained_failures=6,validation_checks=validation['count'],
        seal_sha256=digest(output))),flush=True)


if __name__=='__main__':
    main()
