import os
os.environ["OPENBLAS_NUM_THREADS"] = "1"
os.environ["OMP_NUM_THREADS"] = "1"
os.environ["MKL_NUM_THREADS"] = "1"
import run_temperature_validation
from hybrid_reference_common import *


def main():
    modest()
    destination = ROOT / "results/stage-integrity.json"
    assert not destination.exists()
    validation = verify_packet(ROOT / "results/validation-final")
    assert validation["all_checks_passed"]
    assert validation["failed_reconstruction_checks_retained"] == 60
    assert validation["original_equations_passed_in_direct_sample"]
    assert not validation["original_equations_verified_at_every_step"]
    for filename, checksum in validation["consumed_and_immediate_rehashed"].items():
        assert digest(filename) == checksum, filename
    parent = json.loads((PARENT / "results/stage-integrity.json").read_text())
    assert digest(PARENT / "results/stage-integrity.json") == PARENT_SEAL
    assert (ROOT / "RESULTS.md").exists() and (ROOT / "RUN-NOTES.md").exists()
    assert not list(ROOT.rglob("__pycache__"))
    inherited_count = parent["inherited_sealed_payload_count"] + len(parent["file_hashes"])
    assert inherited_count == 332839
    carried_names = ["checkpoint_manifest_sha256", "local_source_documents", "primary_pdfs", "source_urls",
                     "observational_source_urls", "original_library_sha256", "native_library_sha256",
                     "physical_source_scope", "retained_local_approximation_histories",
                     "raw_subtraction_response_retained", "raw_failed_history_response_retained"]
    carried = {key: value for key, value in parent.items() if key in carried_names or key.startswith("latest_")}
    payloads = {path.relative_to(ROOT).as_posix(): digest(path)
                for path in sorted(ROOT.rglob("*")) if path.is_file() and path != destination}
    directories = [ROOT, *[path for path in ROOT.rglob("*") if path.is_dir()]]
    largest = max(sum(path.is_file() for path in folder.iterdir()) for folder in directories)
    assert largest <= 500
    packet = dict(state="complete", stage=169, sealed_at_utc=datetime.now(timezone.utc).isoformat(),
                  file_hashes=payloads, parent_seal_sha256=PARENT_SEAL, inherited_sealed_payload_count=inherited_count,
                  prior_archive_full_rehash_performed=False,
                  prior_archive_verification_seal_sha256=parent["prior_archive_verification_seal_sha256"],
                  prior_payload_verification_scope="Immediate Stage168 and consumed inputs rehashed; older archive inherited through seals.",
                  consumed_and_immediate_rehashed=validation["consumed_and_immediate_rehashed"],
                  prior_files_rehashed=validation["rehashed_prior_files"], **carried,
                  previous_primary_source_urls=parent.get("previous_primary_source_urls", []) + parent["new_primary_source_urls"],
                  new_primary_source_urls=[], validation_checks=validation["count"],
                  compiled_scripts=validation["compiled_scripts"], accepted_current_scope_verified=True,
                  accepted_scope=validation["accepted_scope"], final_validation=str(ROOT / "results/validation-final/status.json"),
                  latest_temperature_law=str(ROOT / "HYBRID-SUMMARY.json"),
                  conditional_resolved_temperature_prediction=True, microscopic_source_temperature_law_derived=False,
                  unresolved_carrier_forecast=False, source_curve_changed=False, temperature_curve_changed=False,
                  tolerances_changed=False, frequency_modes=96, spectral_readout_nodes=700, response_steps=[128, 256],
                  current_history_replaced=False, reference_history_adopted=False,
                  new_physical_event_evaluations=0, new_expensive_virtual_coefficients=0,
                  baseline_inner_history_rerun=False, baseline_preserved=True,
                  independent_raw_physical_source_qualified=False, raw_source_failures=40,
                  retained_failed_checks=parent.get("retained_failed_checks", []) + validation["retained_failed_checks"],
                  failed_derivative_reconstruction_checks=60, original_equation_audit_sampled_only=True,
                  reference_replay_is_not_gas_error_certificate=True,
                  incoming_continuum_error_certified=False, global_numerical_error_bound=None,
                  protected_workbench_recent_modified_file_count=0,
                  protected_check_scope=validation["protected_check_scope"],
                  maximum_active_compute_workers=1, active_workers_at_seal=0,
                  library_threads_per_production_worker=1, startup_thread_issue_retained_in_run_notes=True,
                  largest_direct_file_count=largest, largest_payload_bytes=max((ROOT / name).stat().st_size for name in payloads),
                  github_action=False, subagents=0, global_installation_changed=False, galaxy_work_modified=False,
                  next_target="Differentiate the finite real/virtual/state collision source with respect to log temperature, including subtraction and evolving incident state; freeze a source prediction before a separate physical temperature calculation.")
    write_json(destination, packet)
    assert {path.relative_to(ROOT).as_posix() for path in ROOT.rglob("*") if path.is_file() and path != destination} == set(payloads)
    assert all(digest(ROOT / name) == checksum for name, checksum in payloads.items())
    print(json.dumps(dict(sealed_files=len(payloads), cumulative_payloads=inherited_count + len(payloads),
                          seal_sha256=digest(destination))), flush=True)


if __name__ == "__main__":
    main()
