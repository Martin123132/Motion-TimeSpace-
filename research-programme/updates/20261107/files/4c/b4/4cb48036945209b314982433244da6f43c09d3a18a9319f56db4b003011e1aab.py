from scaled_common import *


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
    assert prior_count == 9617, prior_count
    checkpoint = POST / '_checkpoints/20261003-pre-condensate-origin/manifest.json'
    original = POST / '.venv-score/Lib/site-packages/camb/cambdll.dll'
    native_library = NATIVE / 'camb/cambdll.dll'
    assert digest(checkpoint) == parent['checkpoint_manifest_sha256']
    assert digest(original) == parent['original_library_sha256']
    assert digest(native_library) == parent['native_library_sha256']
    for source in parent['local_source_documents'] + parent['primary_pdfs']:
        assert digest(source['path']) == source['sha256']
    scripts = sorted(ROOT.glob('*.py'))
    for path in scripts:
        compile(path.read_bytes(), str(path), 'exec')
    script_hashes = {digest(path) for path in scripts}
    validation = json.loads((ROOT / 'results/validation/status.json').read_text())
    review = json.loads((ROOT / 'ACCURACY-REVIEW.json').read_text())
    excluded = review['retained_unaccepted_accuracy_trials']
    packets = sorted(path for category in ['results', 'waves'] for path in (ROOT / category).glob('*/status.json'))
    assert len(packets) == validation['checked_packets'] + 1
    for path in packets:
        packet = json.loads(path.read_text())
        assert packet['state'] == 'complete' and packet['script_sha256'] in script_hashes
        assert (path.parent / 'COMPLETE').is_file()
        if path.relative_to(ROOT).as_posix() not in excluded:
            assert packet['all_checks_passed'] and all(row['passed'] for row in packet['checks']), path
        else:
            assert not packet['all_checks_passed'], path
        for source, expected in packet['input_hashes'].items():
            assert digest(source) == expected, (path, source)
    assert validation['all_current_acceptance_checks_passed']
    started = datetime(2026, 10, 7, 20, 12, 32, tzinfo=timezone.utc)
    workbench = POST.parent / 'formalization-workbench'
    changed = [str(path) for path in workbench.rglob('*') if path.is_file() and path.stat().st_mtime > started.timestamp()]
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
        compiled_scripts=[path.name for path in scripts], checked_result_packets=len(packets),
        validation_checks=validation['count'], all_current_acceptance_checks_passed=True,
        all_requested_numerical_gates_closed=review['all_requested_numerical_gates_closed'],
        open_numerical_gate=review['open_numerical_gate'], raw_unaccepted_accuracy_trials=excluded,
        previous_goal_turn='progress', current_goal_turn='progress',
        physical_baryon_clock_and_rest_tetrad_readout_inherited=True,
        distorted_dilation_and_boundary_terms_retained=True,
        temperature_shape_decomposition_reconstructible=True,
        full_gauge_transformed_metric_re_evolution=False,
        coherent_total_response_accuracy_reviewed=True,
        heat_scaled_photon_shape_and_gas_slip_evolution_implemented=True,
        original_coupled_operator_equivalence_tested=True,
        independent_high_precision_small_readout_checked=True,
        spectrum_dependent_soft_emission_jacobian_derived=True,
        approximate_emission_energy_moment_paired=True,
        full_double_compton_redistribution_included=False, photon_production_evolved=False,
        source_scope=review['accepted_scope'], established_QED_input_not_MTS_discovery=True,
        full_observable_CMB_spectrum=False, new_empirical_fit=False,
        latest_observational_authority=str(HISTORY / 'results/production-primary-refit/status.json'),
        newton_G_inherited_not_derived=True, electron_mass_inherited_not_derived=True,
        native_library_reused_read_only=True, native_library_sha256=digest(native_library),
        original_library_sha256=digest(original), protected_workbench_recent_modified_file_count=0,
        protected_check_scope='Modification-time scan since20:12:32UTC7October2026, not a full content-hash baseline.',
        maximum_active_compute_workers=1, library_threads=1, other_stage_workers_at_validation=0,
        github_action=False, subagents=0, global_installation_changed=False, galaxy_work_modified=False,
        conclusion=review['conclusion']))
    print(json.dumps(dict(state='complete', sealed_files=len(hashes), prior_entries_unchanged=prior_count,
        next_prior_count=prior_count + len(hashes), validation_checks=validation['count'],
        result_packets=len(packets), retained_unaccepted_accuracy_trials=len(excluded))), flush=True)


if __name__ == '__main__':
    main()
