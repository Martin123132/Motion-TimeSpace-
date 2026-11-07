import psutil
from radial_common import *


def main():
    modest()
    output = ROOT / 'results/stage-integrity.json'
    assert not output.exists()
    seals = [*BRANCH.glob('*/results/stage-integrity.json'), BRANCH / 'results/stage-integrity.json']
    by_hash = {digest(path): path for path in seals}
    cursor = PARENT / 'results/stage-integrity.json'
    parent = json.loads(cursor.read_text())
    seen, count = set(), 0
    while True:
        assert cursor not in seen
        seen.add(cursor)
        packet = json.loads(cursor.read_text())
        assert packet['state'] == 'complete'
        base = POST if cursor == BRANCH / 'results/stage-integrity.json' else cursor.parent.parent
        for name, expected in packet['file_hashes'].items():
            assert digest(base / name) == expected, base / name
        count += len(packet['file_hashes'])
        if cursor == BRANCH / 'results/stage-integrity.json':
            break
        links = [packet[key] for key in ['parent_seal_sha256', 'previous_seal_sha256'] if key in packet]
        assert len(links) == 1 and links[0] in by_hash
        cursor = by_hash[links[0]]
    assert count == 119351, count
    protected = [
        (POST / '_checkpoints/20261003-pre-condensate-origin/manifest.json', 'checkpoint_manifest_sha256'),
        (POST / '.venv-score/Lib/site-packages/camb/cambdll.dll', 'original_library_sha256'),
        (BRANCH / 'native-heavy-matching-20261007/native/camb/cambdll.dll', 'native_library_sha256')]
    for path, key in protected:
        assert digest(path) == parent[key], path
    for item in parent['local_source_documents'] + parent['primary_pdfs']:
        assert digest(item['path']) == item['sha256'], item['path']
    validation = json.loads((ROOT / 'results/validation/status.json').read_text())
    assert validation['all_checks_passed'] and validation['accepted_current_scope_verified']
    for path, expected in validation['input_hashes'].items():
        assert digest(path) == expected, path
    workbench = POST.parent / 'formalization-workbench'
    assert workbench.is_dir()
    changed = [str(path) for path in workbench.rglob('*') if path.is_file() and path.stat().st_mtime > STARTED.timestamp()]
    assert not changed, changed
    active = []
    for process in psutil.process_iter(['pid', 'name', 'cmdline']):
        if process.pid == os.getpid() or 'python' not in (process.info['name'] or '').lower():
            continue
        try:
            if Path(process.cwd()).resolve() == ROOT or any(str(ROOT).lower() in word.lower() for word in (process.info['cmdline'] or [])):
                active.append(process.pid)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    assert not active, active
    payloads = {}
    for directory, directories, files in os.walk(ROOT):
        assert '__pycache__' not in directories
        for filename in sorted(files):
            path = Path(directory) / filename
            assert path.suffix != '.tmp'
            if path != output:
                payloads[path.relative_to(ROOT).as_posix()] = digest(path)
    review = json.loads((ROOT / 'ACCURACY-REVIEW.json').read_text())
    carry_keys = ['checkpoint_manifest_sha256', 'local_source_documents', 'primary_pdfs',
        'source_urls', 'observational_source_urls', 'original_library_sha256', 'native_library_sha256',
        'latest_physical_source_histories', 'physical_source_scope', 'retained_local_approximation_histories',
        'latest_driven_tail_histories', 'latest_observational_authority', 'latest_population_source_projections',
        'latest_population_spectral_source']
    carry = {key: parent[key] for key in carry_keys}
    report = dict(state='complete', sealed_at_utc=datetime.now(timezone.utc).isoformat(), file_hashes=payloads,
        parent_seal_sha256=digest(PARENT / 'results/stage-integrity.json'),
        prior_sealed_entries_unchanged=count, parent_chain_edges_verified=len(seen) - 1,
        full_checkpoint_payload_rehashed=False, **carry,
        previous_primary_source_urls=parent.get('previous_primary_source_urls', []) + parent['new_primary_source_urls'],
        new_primary_source_urls=[], local_dependencies={path: digest(path) for path in validation['local_citations']},
        accepted_scientific_checks=validation['passing_scientific_checks'],
        total_scientific_checks=validation['scientific_checks'],
        retained_failed_checks=validation['retained_failed_scientific_checks'],
        retained_failure_records=validation['retained_failure_records'],
        validation_checks=validation['count'], checked_result_packets=validation['checked_packets'] + 1,
        compiled_scripts=validation['compiled_scripts'],
        operational_diagnostics=review.get('operational_diagnostics', []),
        accepted_current_scope_verified=True, numerical_gate_scope=review['numerical_gate_scope'],
        source_scope=review['accepted_scope'], current_goal_turn='progress', previous_goal_turn='progress',
        latest_nodewise_remainder_diagnostic=str(ROOT / review['preferred_diagnostic']),
        full_source_precision_gate_closed=False,
        finite_remainder_response_precision_closed=review['all_dimension_remainder_gate_closed'],
        fixed_angular_radial_gate_closed=parent['fixed_angular_radial_gate_closed'],
        soft_angular_gate_closed=parent['soft_angular_gate_closed'],
        inherited_inner_gates_are_fixed_population_scope=True,
        full16_electron_compact_source_computed=True,
        combined_observed_source_budget=review['source_observed_budget_max'],
        combined_observed_response_budget=review['response_observed_budget_max'],
        combined_observed_gas_budget=review['gas_observed_budget_max'],
        inherited_inner_extreme_probe_count=40, inner_extreme_probes_are_global_bound=False,
        incoming_frequency_gate_closed=parent['incoming_frequency_gate_closed'],
        incoming_evidence_hard_order=3,
        hard_direction_observed_budget_passed=parent['hard_direction_observed_budget_passed'],
        inherited_hard_electron_count=16, current_electron_count=72, current_electron_azimuth=8, current_electron_polar=3, current_electron_radial=3, scalar_representatives=45,
        electron_azimuth_observed_budget_passed=parent['electron_azimuth_observed_budget_passed'],
        electron_polar_observed_budget_passed=parent['electron_polar_observed_budget_passed'],
        electron_radial_observed_budget_passed=review['electron_radial_gate_closed'],
        azimuth_observed_source_budget=parent['azimuth_observed_source_budget'],
        polar_observed_source_budget=parent['polar_observed_source_budget'],
        radial_observed_source_budget=review['radial_observed_budget_max'],
        conditional_gas_moment_identities_derived=True, equilibrium_newly_derived_from_parent=False,
        scalar_reflection_reduction_derived=True, full_polarized_reflection_reuse_claimed=False,
        transverse_fourth_moment_alias_removed=True, mixed_electron_frequency_angle_difference_tested=False,
        expensive_mixed_angle_frequency_difference_tested=False,
        latest_compact_control_pilot=parent['latest_compact_control_pilot'],
        compact_control_pilot_is_not_full_thermal_population=True,
        compact_control_pilot_last_relative_change=parent['compact_control_pilot_last_relative_change'],
        separate_resolution_identity_derived=True, mixed_estimator_computed=True,
        next_target=review['next_target'],
        rigorous_continuum_error_bound=False, outer_population_refinement_complete=False,
        full_spectral_tests_retained=96, new_virtual_loop_evaluations=review['new_virtual_loop_evaluations'],
        leading_control_coefficient=1., control_coefficient_fitted=False, modes_removed=0,
        inherited_leading_angular_tensor_and_factorization_reused=True,
        exact_nine_angular_tensor_factorization_derived=True, energy_expansion_truncated=False,
        every_new_virtual_scalar_owned_by_actual_node=True,
        expensive_source_owner=[str(ROOT / 'runs' / ('expensive-r3-shard'+str(shard)) / 'source.npz') for shard in [0,1]],
        expensive_terms_use_their_own_grid_not_interpolated_coefficients=True,
        exact_kinematics_amplitude_and_counterterm_split_verified=True,
        conditional_frozen_parent_response_computed=True,
        full_parent_history_feedback_applied=False, new_background_evolution=False, new_empirical_fit=False,
        full_finite_recoil_virtual_remainder_bounded=False,
        complete_finite_temperature_polarized_operator=False, full_observable_CMB_spectrum=False,
        new_parent_action=False, newton_G_inherited_not_derived=True, electron_mass_inherited_not_derived=True,
        native_library_reused_read_only=True, protected_workbench_recent_modified_file_count=0,
        protected_check_scope='Modification-time scan since23:42:26UTC9October2026, not a full content-hash baseline.',
        maximum_active_compute_workers=2, active_workers_at_seal=0, library_threads=1,
        largest_direct_file_count=validation['largest_direct_file_count'],
        github_action=False, subagents=0, global_installation_changed=False, galaxy_work_modified=False,
        conclusion=review['conclusion'])
    write_json(output, report)
    print(json.dumps(dict(state='complete', sealed_files=len(payloads), prior_entries_unchanged=count,
        next_prior_count=count + len(payloads), passing_scientific=validation['passing_scientific_checks'],
        retained_failed=validation['retained_failed_scientific_checks'], validation_checks=validation['count'],
        seal_sha256=digest(output))), flush=True)


if __name__ == '__main__':
    main()
