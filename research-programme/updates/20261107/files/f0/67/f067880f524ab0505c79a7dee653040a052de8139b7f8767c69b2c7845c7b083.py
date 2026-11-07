import psutil
from withheld_source_common import *


def main():
    modest()
    output=ROOT/'results/stage-integrity.json'
    assert not output.exists()
    ancestors=sealed_ancestors()
    count=0
    for seal,packet in ancestors.items():
        owner=POST if seal==BRANCH/'results/stage-integrity.json' else seal.parent.parent
        for name,expected in packet['file_hashes'].items():
            assert digest(owner/name)==expected,owner/name
        count+=len(packet['file_hashes'])
    assert count==176987,count
    parent=json.loads((PARENT/'results/stage-integrity.json').read_text())
    for path,key in [(POST/'_checkpoints/20261003-pre-condensate-origin/manifest.json','checkpoint_manifest_sha256'),
        (POST/'.venv-score/Lib/site-packages/camb/cambdll.dll','original_library_sha256'),
        (BRANCH/'native-heavy-matching-20261007/native/camb/cambdll.dll','native_library_sha256')]:
        assert digest(path)==parent[key],path
    for item in parent['local_source_documents']+parent['primary_pdfs']:
        assert digest(item['path'])==item['sha256'],item['path']
    validation=json.loads((ROOT/'results/validation/status.json').read_text())
    assert validation['all_checks_passed'] and validation['accepted_current_scope_verified']
    for path,expected in validation['input_hashes'].items():
        assert digest(path)==expected,path
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
    carry_keys=['checkpoint_manifest_sha256','local_source_documents','primary_pdfs','source_urls',
        'observational_source_urls','original_library_sha256','native_library_sha256',
        'latest_physical_source_histories','physical_source_scope','retained_local_approximation_histories',
        'latest_driven_tail_histories','latest_observational_authority','latest_population_source_projections',
        'latest_population_spectral_source','latest_nodewise_remainder_diagnostic']
    carry={key:parent[key] for key in carry_keys}
    report=dict(state='complete',sealed_at_utc=datetime.now(timezone.utc).isoformat(),file_hashes=payloads,
        parent_seal_sha256=PARENT_SEAL,prior_sealed_entries_unchanged=count,parent_chain_edges_verified=len(ancestors)-1,
        full_checkpoint_payload_rehashed=False,**carry,
        previous_primary_source_urls=parent.get('previous_primary_source_urls',[])+parent['new_primary_source_urls'],
        new_primary_source_urls=[],local_dependencies={path:digest(path) for path in validation['local_citations']},
        accepted_scientific_checks=validation['passing_scientific_checks'],total_scientific_checks=validation['scientific_checks'],
        retained_failed_checks=validation['retained_failed_scientific_checks'],retained_failure_records=validation['retained_failure_records'],
        validation_checks=validation['count'],checked_result_packets=validation['checked_packets']+1,
        compiled_scripts=validation['compiled_scripts'],accepted_current_scope_verified=True,
        source_scope=review['accepted_scope'],numerical_gate_scope=review['numerical_gate_scope'],
        latest_nonmidpoint_remainder_pilot=str(ROOT/'results/anchor-source/source.npz'),
        latest_conditional_history_response=str(ROOT/'results/withheld-response/status.json'),
        raw_failed_history_response_retained=str(PARENT/'results/history-response/status.json'),
        energy_coordinate_repair_derived_in_stage102=True,number_source_unchanged=True,
        conservative_energy_work_relative=review['conservative_energy_work_relative'],
        maximum_source_moment_reconstruction=review['maximum_source_moment_reconstruction'],
        temperature_history_chain_rule_derived=True,profile_gas_linearity_derived=True,
        first_order_fixed_geometry_transfer_law_derived=True,independent_gas_and_expansion_work_retained=True,
        new_epoch_fraction=FRACTION,new_epoch_pilot_resolution=True,quarter_precision_gate_closed=False,
        withheld_precision_gate_closed=False,frozen_forecast_test_performed=True,
        withheld_source_relative_error_max=review['withheld_source_relative_error_max'],
        conditional_response_change_max=review['conditional_response_change_max'],
        frozen_prediction_sha256=digest(ROOT/'results/frozen-prediction/prediction.npz'),
        triangular_hat_superposition_derived=True,
        source_interpolation='Three-anchor piecewise linear in log-expansion;withheld source tested against frozen two-anchor forecast.',
        source_interpolation_error_bounded=False,full_source_precision_gate_closed=False,
        finite_remainder_response_precision_closed=False,rigorous_continuum_error_bound=False,
        midpoint_fine_source_unchanged=True,new_virtual_loop_evaluations=review['new_virtual_loop_evaluations'],
        production_nodes=5616,modes_removed=0,full_spectral_tests_retained=96,profile_columns=4,
        new_empirical_fit=False,new_parent_history=False,full_parent_history_feedback_applied=False,
        new_background_evolution=False,new_parent_action=False,newton_G_inherited_not_derived=True,
        electron_mass_inherited_not_derived=True,control_coefficient_fitted=False,
        protected_workbench_recent_modified_file_count=0,
        protected_check_scope='Modification-time scan since19:43:15UTC11October2026,not an unsaved content baseline.',
        maximum_active_compute_workers=2,active_workers_at_seal=0,library_threads=1,
        largest_direct_file_count=validation['largest_direct_file_count'],github_action=False,subagents=0,
        global_installation_changed=False,galaxy_work_modified=False,
        current_goal_turn='progress',next_target=review['next_target'],conclusion=review['conclusion'],
        operational_diagnostics=review.get('operational_diagnostics',[]))
    write_json(output,report)
    print(json.dumps(dict(state='complete',sealed_files=len(payloads),prior_entries_unchanged=count,
        next_prior_count=count+len(payloads),passing_scientific=validation['passing_scientific_checks'],
        validation_checks=validation['count'],seal_sha256=digest(output))),flush=True)


if __name__=='__main__':
    main()

