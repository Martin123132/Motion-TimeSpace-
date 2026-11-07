import psutil
from projection_common import *


def main():
    modest()
    output=ROOT/'results/stage-integrity.json'
    assert not output.exists()
    chain=ancestors()
    count=0
    for seal,packet in chain.items():
        owner=POST if seal==BRANCH/'results/stage-integrity.json' else seal.parent.parent
        for name,expected in packet['file_hashes'].items():
            assert digest(owner/name)==expected,owner/name
        count+=len(packet['file_hashes'])
    assert count==202412,count
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
    keys=['checkpoint_manifest_sha256','local_source_documents','primary_pdfs','source_urls',
        'observational_source_urls','original_library_sha256','native_library_sha256',
        'latest_physical_source_histories','physical_source_scope','retained_local_approximation_histories',
        'latest_driven_tail_histories','latest_observational_authority','latest_population_source_projections',
        'latest_population_spectral_source','latest_nodewise_remainder_diagnostic',
        'latest_nonmidpoint_remainder_pilot','latest_two_temperature_frequency_comparison',
        'latest_late_three_rule_frequency_comparison','latest_conditional_history_response',
        'latest_source_window_response','raw_subtraction_response_retained','raw_failed_history_response_retained']
    carry={key:parent[key] for key in keys}
    report=dict(state='complete',sealed_at_utc=datetime.now(timezone.utc).isoformat(),file_hashes=payloads,
        parent_seal_sha256=PARENT_SEAL,prior_sealed_entries_unchanged=count,parent_chain_edges_verified=len(chain)-1,
        full_checkpoint_payload_rehashed=False,**carry,
        previous_primary_source_urls=parent.get('previous_primary_source_urls',[])+parent['new_primary_source_urls'],
        new_primary_source_urls=URLS,local_dependencies={path:digest(path) for path in validation['local_citations']},
        accepted_scientific_checks=validation['passing_scientific_checks'],total_scientific_checks=validation['scientific_checks'],
        retained_failed_checks=3,retained_failure_records=validation['retained_failure_records'],
        validation_checks=validation['count'],checked_result_packets=3,compiled_scripts=validation['compiled_scripts'],
        accepted_current_scope_verified=True,source_scope=review['accepted_scope'],
        numerical_gate_scope=review['numerical_gate_scope'],
        latest_temperature_distortion_projection=str(ROOT/'results/projection/status.json'),
        latest_stable_physical_spectral_readout=str(ROOT/'results/stable-readout/status.json'),
        energy_matching_convention_derived=True,physical_chi_normalization_traced=True,
        pure_temperature_and_reference_shift_controls=True,raw_roundoff_failures_retained=True,
        independent_saved_energy_used=True,final_saved_scale=1e-5,
        known_interval_contribution_only=True,outside_window_source_assumed_physically_zero=False,
        new_virtual_loop_evaluations=0,production_nodes=0,modes_removed=0,full_spectral_tests_retained=96,
        finite_source_recomputed=False,new_empirical_fit=False,new_parent_history=False,
        full_parent_history_feedback_applied=False,new_background_evolution=False,new_parent_action=False,
        newton_G_inherited_not_derived=True,electron_mass_inherited_not_derived=True,control_coefficient_fitted=False,
        source_frequency_continuum_error_bounded=False,full_source_precision_gate_closed=False,
        infrared_increment_continuation_computed=False,instrument_temperature_fit=False,
        protected_workbench_recent_modified_file_count=0,
        protected_check_scope='Modification-time scan since17:11:56UTC12October2026,not an unsaved content baseline.',
        maximum_active_compute_workers=1,active_workers_at_seal=0,library_threads=1,
        largest_direct_file_count=validation['largest_direct_file_count'],github_action=False,subagents=0,
        global_installation_changed=False,galaxy_work_modified=False,current_goal_turn='progress',
        next_target=review['next_target'],conclusion=review['conclusion'],
        operational_diagnostics=review['operational_diagnostics'])
    write_json(output,report)
    print(json.dumps(dict(state='complete',sealed_files=len(payloads),prior_entries_unchanged=count,
        next_prior_count=count+len(payloads),passing_scientific=validation['passing_scientific_checks'],
        retained_failures=3,validation_checks=validation['count'],seal_sha256=digest(output))),flush=True)


if __name__=='__main__':
    main()

