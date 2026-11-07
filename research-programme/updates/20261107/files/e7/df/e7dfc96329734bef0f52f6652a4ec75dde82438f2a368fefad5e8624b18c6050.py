from source_tangent import *


def main():
    modest()
    destination = ROOT / "results/stage-integrity.json"
    assert not destination.exists()
    validation = verify(ROOT / "results/validation")
    assert validation["all_checks_passed"] and validation["protocol_validation_only"]
    for filename, checksum in validation["consumed_and_immediate_rehashed"].items():
        assert digest(filename) == checksum, filename
    parent = json.loads((PARENT / "results/stage-integrity.json").read_text())
    assert digest(PARENT / "results/stage-integrity.json") == PARENT_SHA
    assert (ROOT / "RESULTS.md").exists() and (ROOT / "RUN-NOTES.md").exists()
    assert not list(ROOT.rglob("__pycache__"))
    inherited_count = parent["inherited_sealed_payload_count"]+len(parent["file_hashes"])
    assert inherited_count == 332963
    carried_names = ["checkpoint_manifest_sha256", "local_source_documents", "primary_pdfs", "source_urls",
                    "observational_source_urls", "original_library_sha256", "native_library_sha256",
                    "physical_source_scope", "retained_local_approximation_histories",
                    "raw_subtraction_response_retained", "raw_failed_history_response_retained"]
    carried = {key: value for key, value in parent.items() if key in carried_names or key.startswith("latest_")}
    payloads = {path.relative_to(ROOT).as_posix(): digest(path)
                for path in sorted(ROOT.rglob("*")) if path.is_file() and path != destination}
    largest = max(sum(path.is_file() for path in folder.iterdir())
                  for folder in [ROOT, *[path for path in ROOT.rglob("*") if path.is_dir()]])
    assert largest <= 500
    event_files = sorted((ROOT / "events").rglob("event-*.npz"))
    reused = 0
    for path in event_files:
        with np.load(path) as values:
            reused += int(bool(values["loop_reused"]))
    prediction = verify(ROOT / "results/prediction-test")
    retained = json.loads((ROOT / "results/validation/retained-failures.json").read_text())
    packet = dict(state="complete", stage=170, sealed_at_utc=datetime.now(timezone.utc).isoformat(),
                  file_hashes=payloads, parent_seal_sha256=PARENT_SHA,
                  inherited_sealed_payload_count=inherited_count, **carried,
                  previous_primary_source_urls=parent.get("previous_primary_source_urls", [])+parent["new_primary_source_urls"],
                  new_primary_source_urls=[], prior_archive_full_rehash_performed=False,
                  prior_archive_verification_seal_sha256=parent["prior_archive_verification_seal_sha256"],
                  prior_payload_verification_scope="Immediate Stage169 and consumed inputs rehashed; older archive inherited through seals.",
                  consumed_and_immediate_rehashed=validation["consumed_and_immediate_rehashed"],
                  prior_files_rehashed=validation["rehashed_prior_files"],
                  validation_checks=validation["count"], compiled_scripts=validation["compiled_scripts"],
                  accepted_current_scope_verified=True,
                  accepted_scope="Functional source derivatives and a frozen 12-event microscopic temperature test; all prediction/stability failures retained.",
                  final_validation=str(ROOT / "results/validation/status.json"),
                  latest_microscopic_temperature_tangent=str(ROOT / "RESULTS.md"),
                  microscopic_source_functional_temperature_derivatives_derived=True,
                  derivative_numbers_are_finite_difference_evaluations=True,
                  full_population_source_temperature_law_certified=False,
                  prediction_summary=prediction["summary"],
                  primary_second_order_predictions_pass=validation["primary_second_order_predictions_pass"],
                  primary_derivative_stability_pass=validation["primary_derivative_stability_pass"],
                  current_event_identity_pass=validation["current_event_identity_pass"],
                  production_event_temperature_combinations=len(event_files),
                  production_virtual_coefficients_reused=reused,
                  production_virtual_coefficients_new=len(event_files)-reused,
                  paired_histories=2, source_history_columns_per_branch=4,
                  target_frozen_before_evaluation=True, target_fraction=TARGET,
                  full_population_integral=False, native_incident_histories_are_inputs=True,
                  source_curve_changed=False, temperature_curve_changed=False, current_history_replaced=False,
                  tolerances_changed=False, baseline_preserved=True,
                  independent_raw_physical_source_qualified=False, raw_source_failures=40,
                  retained_failed_checks=parent.get("retained_failed_checks", [])+retained,
                  current_stage_retained_failures=len(retained),
                  incoming_continuum_error_certified=False, global_numerical_error_bound=None,
                  protected_workbench_recent_modified_file_count=validation["protected_modified_file_count"],
                  protected_check_scope=validation["protected_check_scope"],
                  maximum_active_compute_workers=1, active_workers_at_seal=0,
                  library_threads_per_production_worker=1, largest_direct_file_count=largest,
                  largest_payload_bytes=max((ROOT / name).stat().st_size for name in payloads),
                  github_action=False, subagents=0, global_installation_changed=False, galaxy_work_modified=False,
                  next_target_file=str(ROOT / "RESULTS.md"))
    write_json(destination, packet)
    assert all(digest(ROOT / name) == checksum for name, checksum in payloads.items())
    print(json.dumps(dict(sealed_files=len(payloads), cumulative_payloads=inherited_count+len(payloads),
                          seal_sha256=digest(destination))), flush=True)


if __name__ == "__main__":
    main()
