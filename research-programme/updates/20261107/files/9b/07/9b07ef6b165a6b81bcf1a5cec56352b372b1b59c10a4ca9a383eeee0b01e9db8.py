from wave_common import *


def main():
    modest()
    output = ROOT / 'results/stage-integrity.json'
    assert not output.exists()
    seals = list(BRANCH.glob('*/results/stage-integrity.json')) + [BRANCH / 'results/stage-integrity.json']
    by_hash = {digest(path): path for path in seals}
    cursor = PARENT / 'results/stage-integrity.json'
    parent = json.loads(cursor.read_text())
    seen, prior_count = set(), 0
    while True:
        assert cursor not in seen
        seen.add(cursor)
        packet = json.loads(cursor.read_text())
        assert packet['state'] == 'complete'
        base = POST if cursor == BRANCH / 'results/stage-integrity.json' else cursor.parent.parent
        for relative, expected in packet['file_hashes'].items():
            assert digest(base / relative) == expected, base / relative
        prior_count += len(packet['file_hashes'])
        if cursor == BRANCH / 'results/stage-integrity.json':
            break
        links = [packet[key] for key in ['parent_seal_sha256', 'previous_seal_sha256'] if key in packet]
        assert len(links) == 1 and links[0] in by_hash
        cursor = by_hash[links[0]]
    assert prior_count == 10265, prior_count
    checkpoint = POST / '_checkpoints/20261003-pre-condensate-origin/manifest.json'
    original = POST / '.venv-score/Lib/site-packages/camb/cambdll.dll'
    native_library = NATIVE / 'camb/cambdll.dll'
    assert digest(checkpoint) == parent['checkpoint_manifest_sha256']
    assert digest(original) == parent['original_library_sha256']
    assert digest(native_library) == parent['native_library_sha256']
    for source in parent['local_source_documents'] + parent['primary_pdfs']:
        assert digest(source['path']) == source['sha256']
    validation = json.loads((ROOT / 'results/validation/status.json').read_text())
    for source, expected in validation['input_hashes'].items():
        assert digest(source) == expected, source
    review = json.loads((ROOT / 'ACCURACY-REVIEW.json').read_text())
    assert validation['all_current_acceptance_checks_passed']
    workbench = POST.parent / 'formalization-workbench'
    changed = [str(path) for path in workbench.rglob('*') if path.is_file() and path.stat().st_mtime > STARTED.timestamp()]
    assert workbench.is_dir() and not changed, changed
    hashes = {}
    for directory, directories, files in os.walk(ROOT):
        assert '__pycache__' not in directories, directory
        for name in sorted(files):
            path = Path(directory) / name
            if path != output:
                hashes[path.relative_to(ROOT).as_posix()] = digest(path)
    write_json(output, dict(state='complete', sealed_at_utc=datetime.now(timezone.utc).isoformat(),
        file_hashes=hashes, parent_seal_sha256=digest(PARENT / 'results/stage-integrity.json'),
        prior_sealed_entries_unchanged=prior_count, parent_chain_edges_verified=len(seen) - 1,
        checkpoint_manifest_sha256=digest(checkpoint), full_checkpoint_payload_rehashed=False,
        local_source_documents=parent['local_source_documents'], primary_pdfs=parent['primary_pdfs'],
        source_urls=parent['source_urls'],
        previous_primary_source_urls=parent.get('previous_primary_source_urls', []) + parent['new_primary_source_urls'],
        new_primary_source_urls=validation['recorded_web_urls'], observational_source_urls=parent['observational_source_urls'],
        local_dependencies={path: digest(path) for path in validation['local_citations']},
        compiled_scripts=[path.name for path in sorted(ROOT.glob('*.py'))], checked_result_packets=validation['checked_packets'] + 1,
        validation_checks=validation['count'], accepted_scientific_checks=validation['accepted_scientific_checks'],
        retained_failed_checks=validation['retained_failed_checks'], all_current_acceptance_checks_passed=True,
        all_requested_numerical_gates_closed=review['all_requested_numerical_gates_closed'],
        numerical_gate_scope=review['numerical_gate_scope'], raw_unaccepted_accuracy_trials=review['retained_unaccepted_accuracy_trials'],
        previous_goal_turn='progress', current_goal_turn='progress',
        derived_emission_density_tangent=True, tangent_verified_against_separate_density_histories=True,
        common_temperature_emission_column_derived=True, source_four_force_pairing_tested=True,
        finite_shift_Compton_heat_derivative_derived=True, no_photon_number_conservation_projection=True,
        source_scope=review['accepted_scope'], arbitrary_angular_DC_projection_derived=False,
        perturbed_emission_finite_k_wave_evolution=False, full_observable_CMB_spectrum=False, new_empirical_fit=False,
        latest_observational_authority=str(HISTORY / 'results/production-primary-refit/status.json'),
        newton_G_inherited_not_derived=True, electron_mass_inherited_not_derived=True,
        native_library_reused_read_only=True, native_library_sha256=digest(native_library),
        original_library_sha256=digest(original), protected_workbench_recent_modified_file_count=0,
        protected_check_scope='Modification-time scan since00:02:43UTC8October2026, not a full content-hash baseline.',
        maximum_active_compute_workers=1, library_threads=1,
        github_action=False, subagents=0, global_installation_changed=False, galaxy_work_modified=False,
        conclusion=review['conclusion']))
    print(json.dumps(dict(state='complete', sealed_files=len(hashes), prior_entries_unchanged=prior_count,
        next_prior_count=prior_count + len(hashes), accepted_scientific_checks=validation['accepted_scientific_checks'],
        validation_checks=validation['count'], result_packets=validation['checked_packets'] + 1,
        retained_failed_checks=validation['retained_failed_checks'], seal_sha256=digest(output))), flush=True)


if __name__ == '__main__':
    main()
