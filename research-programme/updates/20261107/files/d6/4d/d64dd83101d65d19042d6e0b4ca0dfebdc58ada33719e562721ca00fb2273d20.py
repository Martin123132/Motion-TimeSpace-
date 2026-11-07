from step_common import *


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
        report = json.loads(cursor.read_text())
        assert report['state'] == 'complete'
        base = POST if cursor == BRANCH / 'results/stage-integrity.json' else cursor.parent.parent
        for relative, expected in report['file_hashes'].items():
            assert digest(base / relative) == expected, base / relative
        prior_count += len(report['file_hashes'])
        if cursor == BRANCH / 'results/stage-integrity.json':
            break
        links = [report[key] for key in ['parent_seal_sha256', 'previous_seal_sha256'] if key in report]
        assert len(links) == 1 and links[0] in by_hash
        cursor = by_hash[links[0]]
    assert prior_count == 7513, prior_count
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
    packets = sorted(ROOT.glob('results/*/status.json')) + sorted(ROOT.glob('runs/*/status.json'))
    assert len(packets) == 33, len(packets)
    validation = json.loads((ROOT / 'results/validation/status.json').read_text())
    for path in packets:
        packet = json.loads(path.read_text())
        assert packet['state'] == 'complete' and packet['script_sha256'] in script_hashes
        assert (path.parent / 'COMPLETE').is_file()
        assert packet['all_checks_passed'] and all(row['passed'] for row in packet['checks'])
        for source, expected in packet['input_hashes'].items():
            assert digest(source) == expected, (path, source)
    assert validation['all_current_acceptance_checks_passed']
    started = datetime(2026, 10, 7, 9, 39, 59, tzinfo=timezone.utc)
    workbench = POST.parent / 'formalization-workbench'
    changed = [str(path) for path in workbench.rglob('*')
               if path.is_file() and path.stat().st_mtime > started.timestamp()]
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
        new_primary_source_urls=validation['new_primary_source_urls'],
        observational_source_urls=parent['observational_source_urls'],
        local_dependencies={path: digest(path) for path in validation['local_citations']},
        compiled_scripts=[path.name for path in scripts], checked_result_packets=len(packets),
        validation_checks=validation['count'], all_current_acceptance_checks_passed=True,
        previous_goal_turn='progress', conservative_spectral_plasma_step_derived_and_evolved=True,
        positive_finite_heat_capacity_not_algebraic_temperature_closure=True,
        coupled_quadratic_entropy_and_midpoint_identity_derived=True,
        both_saved_parent_models_and_independent_nonthermal_fixture_evolved=True,
        thermal_minus_elastic_response_itself_refined=True,
        excluded_high_frequency_FP_instability_retained=True,
        uniform_continuum_stability_of_truncated_anisotropic_FP=False,
        finite_Gaussian_shift_principal_part_nonpositive=True,
        reciprocal_polarized_pair_square_identity_derived=True,
        naive_complete_kernel_candidate_rejected=True,
        physical_moving_electron_kernel_36_scalar_coefficients_recovered_without_fitting=True,
        full_polarized_finite_shift_kernel_completed=False,
        full_angular_spectral_cosmological_evolution=False, new_empirical_fit=False,
        established_Compton_physics_not_MTS_discovery=True,
        latest_observational_authority=str(HISTORY / 'results/production-primary-refit/status.json'),
        newton_G_inherited_not_derived=True, electron_mass_inherited_not_derived=True,
        native_library_reused_read_only=True, native_library_sha256=digest(native_library),
        original_library_sha256=digest(original), protected_workbench_recent_modified_file_count=0,
        protected_check_scope='Modification-time scan since09:39:59UTC7October2026, not a full content-hash baseline.',
        maximum_active_compute_workers=1, library_threads=1, active_stage_workers=0,
        github_action=False, subagents=0, global_installation_changed=False, galaxy_work_modified=False,
        conclusion='Conservative spectral/plasma evolution now passes bounded-domain response refinements. A true fine-grid failure of the truncated anisotropic expansion is retained and derived. The finite-shift principal part and reciprocal polarized exchange structure repair its mechanism; physical moving-electron scalar coefficients match independently. Next complete polarized reciprocal finite-shift discretization and return it to coupled gravity evolution.'))
    print(json.dumps(dict(state='complete', sealed_files=len(hashes), prior_entries_unchanged=prior_count,
        next_prior_count=prior_count + len(hashes), accepted_validation_checks=validation['count'],
        result_packets=len(packets))), flush=True)


if __name__ == '__main__':
    main()
