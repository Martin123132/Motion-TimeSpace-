import os
import psutil
from weak_common import *


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
        for relative_path, expected in packet['file_hashes'].items():
            assert digest(base / relative_path) == expected, base / relative_path
        prior_count += len(packet['file_hashes'])
        if cursor == BRANCH / 'results/stage-integrity.json':
            break
        links = [packet[key] for key in ['parent_seal_sha256', 'previous_seal_sha256'] if key in packet]
        assert len(links) == 1 and links[0] in by_hash
        cursor = by_hash[links[0]]
    assert prior_count == 10974, prior_count
    checkpoint = POST / '_checkpoints/20261003-pre-condensate-origin/manifest.json'
    original = POST / '.venv-score/Lib/site-packages/camb/cambdll.dll'
    native = BRANCH / 'native-heavy-matching-20261007/native/camb/cambdll.dll'
    assert digest(checkpoint) == parent['checkpoint_manifest_sha256']
    assert digest(original) == parent['original_library_sha256']
    assert digest(native) == parent['native_library_sha256']
    for item in parent['local_source_documents'] + parent['primary_pdfs']:
        assert digest(item['path']) == item['sha256'], item['path']
    validation = json.loads((ROOT / 'results/validation/status.json').read_text())
    assert validation['all_current_acceptance_checks_passed']
    for path, expected in validation['input_hashes'].items():
        assert digest(path) == expected, path
    workbench = POST.parent / 'formalization-workbench'
    assert workbench.is_dir()
    changed = [str(path) for path in workbench.rglob('*')
               if path.is_file() and path.stat().st_mtime > STARTED.timestamp()]
    assert not changed, changed
    active = []
    for process in psutil.process_iter(['pid', 'name', 'cmdline']):
        if process.pid == os.getpid() or 'python' not in (process.info['name'] or '').lower():
            continue
        try:
            if Path(process.cwd()).resolve() == ROOT or any(str(ROOT).lower() in word.lower()
                    for word in (process.info['cmdline'] or [])):
                active.append(process.pid)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    assert not active, active
    payloads = {}
    for directory, directories, files in os.walk(ROOT):
        assert '__pycache__' not in directories
        for name in sorted(files):
            path = Path(directory) / name
            if path != output:
                payloads[path.relative_to(ROOT).as_posix()] = digest(path)
    review = json.loads((ROOT / 'ACCURACY-REVIEW.json').read_text())
    carry = {key: parent[key] for key in ['checkpoint_manifest_sha256', 'local_source_documents',
             'primary_pdfs', 'source_urls', 'observational_source_urls', 'original_library_sha256',
             'native_library_sha256', 'latest_physical_source_histories']}
    report = dict(state='complete', sealed_at_utc=datetime.now(timezone.utc).isoformat(),
        file_hashes=payloads, parent_seal_sha256=digest(PARENT / 'results/stage-integrity.json'),
        prior_sealed_entries_unchanged=prior_count, parent_chain_edges_verified=len(seen) - 1,
        full_checkpoint_payload_rehashed=False, **carry,
        previous_primary_source_urls=parent.get('previous_primary_source_urls', []) + parent['new_primary_source_urls'],
        new_primary_source_urls=validation['recorded_web_urls'],
        local_dependencies={path: digest(path) for path in validation['local_citations']},
        accepted_scientific_checks=validation['accepted_scientific_checks'],
        validation_checks=validation['count'], checked_result_packets=validation['checked_packets'] + 1,
        compiled_scripts=validation['compiled_scripts'], retained_failed_checks=0,
        all_current_acceptance_checks_passed=True,
        all_requested_numerical_gates_closed=review['all_requested_numerical_gates_closed'],
        numerical_gate_scope=review['numerical_gate_scope'], source_scope=review['accepted_scope'],
        previous_goal_turn='progress', current_goal_turn='progress',
        finite_virtual_weak_scalar_projection_completed=True,
        full_thermal_gas_collision_source=False, complete_finite_temperature_polarized_operator=False,
        physical_photon_number_source_projected_to_zero=False,
        actual_nonthermal_infrared_occupation_derived=False,
        new_background_evolution=False, new_empirical_fit=False,
        perturbed_emission_finite_k_wave_evolution=False, full_observable_CMB_spectrum=False,
        latest_observational_authority=str(BRANCH / 'full-history-source-precision-20261007/results/production-primary-refit/status.json'),
        native_library_reused_read_only=True, newton_G_inherited_not_derived=True, electron_mass_inherited_not_derived=True,
        raw_unaccepted_accuracy_trials=review['coarse_chemical_trials_not_production_accuracy'],
        protected_workbench_recent_modified_file_count=0,
        protected_check_scope='Modification-time scan since04:30:49UTC8October2026, not a full content-hash baseline.',
        maximum_active_compute_workers=1, active_workers_at_seal=0, library_threads=1,
        github_action=False, subagents=0, global_installation_changed=False, galaxy_work_modified=False,
        conclusion=review['conclusion'])
    write_json(output, report)
    print(json.dumps(dict(state='complete', sealed_files=len(payloads), prior_entries_unchanged=prior_count,
        next_prior_count=prior_count + len(payloads), scientific_checks=validation['accepted_scientific_checks'],
        validation_checks=validation['count'], seal_sha256=digest(output))), flush=True)


if __name__ == '__main__':
    main()
