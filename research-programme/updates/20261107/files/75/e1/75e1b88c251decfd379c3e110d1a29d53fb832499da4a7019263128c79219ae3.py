import psutil
from rectangular_common import *


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
    assert count == 18082, count
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
    carry = {key: parent[key] for key in ['checkpoint_manifest_sha256', 'local_source_documents', 'primary_pdfs',
        'source_urls', 'observational_source_urls', 'original_library_sha256', 'native_library_sha256',
        'latest_physical_source_histories', 'physical_source_scope', 'retained_local_approximation_histories',
        'latest_driven_tail_histories', 'latest_observational_authority', 'latest_population_source_projections']}
    report = dict(state='complete', sealed_at_utc=datetime.now(timezone.utc).isoformat(), file_hashes=payloads,
        parent_seal_sha256=digest(PARENT / 'results/stage-integrity.json'),
        prior_sealed_entries_unchanged=count, parent_chain_edges_verified=len(seen) - 1,
        full_checkpoint_payload_rehashed=False, **carry,
        previous_primary_source_urls=parent.get('previous_primary_source_urls', []) + parent['new_primary_source_urls'],
        new_primary_source_urls=validation['recorded_web_urls'],
        local_dependencies={path: digest(path) for path in validation['local_citations']},
        accepted_scientific_checks=validation['passing_scientific_checks'],
        total_scientific_checks=validation['scientific_checks'],
        retained_failed_checks=validation['retained_failed_scientific_checks'],
        retained_failure_records=validation['retained_failure_records'],
        validation_checks=validation['count'], checked_result_packets=validation['checked_packets'] + 1,
        compiled_scripts=validation['compiled_scripts'],
        operational_diagnostics=['operational-print-diagnostic.json'],
        accepted_current_scope_verified=True, full_source_precision_gate_closed=True,
        finite_remainder_response_precision_closed=False,
        numerical_gate_scope=review['numerical_gate_scope'], source_scope=review['accepted_scope'],
        previous_goal_turn='progress', current_goal_turn='progress',
        latest_population_spectral_source=str(ROOT / 'controls/refined-leading-control/source.npz'),
        full_spectral_tests_retained=96, new_virtual_loop_evaluations=0,
        leading_control_coefficient=1., control_coefficient_fitted=False, modes_removed=0,
        conditional_frozen_parent_response_computed=True,
        full_parent_history_feedback_applied=False, new_background_evolution=False, new_empirical_fit=False,
        full_finite_recoil_virtual_remainder_bounded=False,
        complete_finite_temperature_polarized_operator=False,
        perturbed_emission_finite_k_wave_evolution=False, full_observable_CMB_spectrum=False,
        new_parent_action=False, newton_G_inherited_not_derived=True, electron_mass_inherited_not_derived=True,
        native_library_reused_read_only=True, protected_workbench_recent_modified_file_count=0,
        protected_check_scope='Modification-time scan since10:02:38UTC8October2026, not a full content-hash baseline.',
        maximum_active_compute_workers=1, active_workers_at_seal=0, library_threads=1,
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
