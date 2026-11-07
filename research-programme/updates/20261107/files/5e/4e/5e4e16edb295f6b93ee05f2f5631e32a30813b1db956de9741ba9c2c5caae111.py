from spectrum_decomposition_common import *


def main():
    modest()
    output = ROOT / 'results/stage-integrity.json'
    assert not output.exists()
    chain = ancestors()
    parent = chain[PARENT / 'results/stage-integrity.json']
    validation = json.loads((ROOT / 'results/validation/status.json').read_text())
    assert validation['all_checks_passed'] and validation['accepted_scope_verified']
    for mapping in [validation['input_hashes'], validation['consumed_and_immediate_rehashed']]:
        for path, sha in mapping.items():
            assert digest(path) == sha, path
    summary = json.loads((ROOT / 'NUMERICAL-SUMMARY.json').read_text())
    assert not list(ROOT.rglob('__pycache__'))
    workbench = POST.parent / 'formalization-workbench'
    assert not [path for path in workbench.rglob('*') if path.is_file() and path.stat().st_mtime > STARTED.timestamp()]
    payloads = {path.relative_to(ROOT).as_posix(): digest(path) for path in sorted(ROOT.rglob('*'))
                if path.is_file() and path != output}
    largest = max(len(files) for directory, directories, files in os.walk(ROOT))
    assert largest < 1000
    keys = ['checkpoint_manifest_sha256', 'local_source_documents', 'primary_pdfs',
            'source_urls', 'observational_source_urls', 'original_library_sha256',
            'native_library_sha256', 'physical_source_scope', 'retained_local_approximation_histories',
            'raw_subtraction_response_retained', 'raw_failed_history_response_retained']
    carried = {key: value for key, value in parent.items() if key in keys or key.startswith('latest_')}
    packet = dict(state='complete', stage=142, sealed_at_utc=datetime.now(timezone.utc).isoformat(),
                  file_hashes=payloads, parent_seal_sha256=PARENT_SEAL,
                  parent_chain_edges_verified=len(chain) - 1,
                  inherited_sealed_payload_count=219814,
                  prior_archive_full_rehash_performed=False,
                  prior_archive_verification_seal_sha256=parent['prior_archive_verification_seal_sha256'],
                  prior_payload_verification_scope='Stage141 immediate payloads and consumed dependencies rehashed; earlier archive audit inherited through verified seals.',
                  prior_files_rehashed=validation['rehashed_prior_files'],
                  consumed_and_immediate_rehashed=validation['consumed_and_immediate_rehashed'],
                  **carried,
                  previous_primary_source_urls=parent.get('previous_primary_source_urls', []) + parent['new_primary_source_urls'],
                  new_primary_source_urls=[], total_scientific_checks=summary['scientific_checks'],
                  accepted_scientific_checks=summary['passing_scientific_checks'],
                  retained_failed_checks=summary['current_retained_flags'],
                  retained_failure_names={'decomposition-v2': [row['name'] for row in summary['failed_by_scope']['current_finer_readout_energy_input']]},
                  inherited_stage141_failure_names=parent['retained_failure_names'],
                  inherited_stage141_failed_checks=10, validation_checks=validation['count'],
                  compiled_scripts=validation['compiled_scripts'], accepted_current_scope_verified=True,
                  all_scientific_checks_passed=False, canonical_spectral_decomposition_accepted=True,
                  finer_energy_input_flags_retained=True,
                  latest_completed_spectrum_decomposition=str(ROOT / 'NUMERICAL-SUMMARY.json'),
                  physical_source_scope_this_stage='Existing .25U to .5U extra-source contribution at final a=1e-5; not a complete all-epoch MTS source.',
                  numerical_feedback_history_complete=True, physical_extra_source_history_complete=False,
                  physical_normalization_verified=True, physical_observational_fit=False,
                  weighted_norm_is_physical_energy=False, source_evaluations=0, evolution_steps=0,
                  protected_workbench_recent_modified_file_count=0,
                  protected_check_scope='Modification-time scan since19:43:19UTC15October2026; not an unsaved content baseline.',
                  maximum_active_compute_workers=1, active_workers_at_seal=0, library_threads=1,
                  largest_direct_file_count=largest, github_action=False, subagents=0,
                  global_installation_changed=False, galaxy_work_modified=False,
                  current_goal_turn='progress', next_target=summary['next_target'])
    write_json(output, packet)
    print(json.dumps(dict(sealed_files=len(payloads), cumulative_payloads=219814 + len(payloads),
                          seal_sha256=digest(output), validation_checks=validation['count'])), flush=True)


if __name__ == '__main__':
    main()
