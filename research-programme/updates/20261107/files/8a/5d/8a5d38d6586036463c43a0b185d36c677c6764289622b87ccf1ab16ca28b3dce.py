from curvature_stage186 import *


def seal():
    assert read(ROOT / "progress.json")["state"] == "validation_complete"
    status_path = ROOT / "results/precision/status.json"
    status = read(status_path)
    assert not status["identity_failures"]
    assert not status["active_failed_checks"]
    assert status["original_status_sha256"] == saved.digest(ROOT / "results/status.json")
    assert authenticate() == status["authenticated_inputs"]
    assert (ROOT / "RESULTS.md").exists() and (ROOT / "NEXT.md").exists()
    frozen = read(ROOT / "results/frozen-curvature.json")
    assert saved.digest(ROOT / "results/frozen-curvature.npz") == frozen["sha256"]
    for path in ROOT.glob("*.py"):
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
    assert not list(ROOT.rglob("__pycache__"))
    parent = read(PARENT / "results/stage-integrity.json")
    inherited = parent["inherited_sealed_payload_count"] + len(parent["file_hashes"])
    assert inherited == 336338
    for path, checksum in read(ROOT / "configuration.json")["bookmark_hashes"].items():
        assert saved.digest(path) == checksum
    import psutil
    for process in psutil.process_iter(["pid", "name", "cmdline"]):
        if process.info["pid"] == os.getpid():
            continue
        command = " ".join(process.info["cmdline"] or [])
        assert not ("python" in (process.info["name"] or "").lower()
                    and any(name in command for name in ["curvature_stage186.py", "analyse_stage186.py", "precision_stage186.py", "finish_stage186.py"]))
    destination = ROOT / "results/stage-integrity.json"
    assert not destination.exists()
    write(ROOT / "progress.json", dict(state="complete", active_workers_after_return=0))
    hashes = {path.relative_to(ROOT).as_posix(): saved.digest(path)
              for path in sorted(ROOT.rglob("*")) if path.is_file() and path != destination}
    largest = max(sum(path.is_file() for path in folder.iterdir())
                  for folder in [ROOT, *[path for path in ROOT.rglob("*") if path.is_dir()]])
    assert largest <= 500
    carry_names = ["checkpoint_manifest_sha256", "local_source_documents", "primary_pdfs", "source_urls",
                  "observational_source_urls", "original_library_sha256", "native_library_sha256", "physical_source_scope",
                  "retained_local_approximation_histories", "raw_subtraction_response_retained", "raw_failed_history_response_retained"]
    carried = {key: value for key, value in parent.items() if key in carry_names or key.startswith("latest_")}
    write(destination, dict(state="complete", stage=186, sealed_at_utc=datetime.now(timezone.utc).isoformat(),
          parent_seal_sha256=PARENT_SHA, inherited_sealed_payload_count=inherited, file_hashes=hashes, **carried,
          consumed_and_immediate_rehashed=status["authenticated_inputs"],
          previous_primary_source_urls=parent.get("previous_primary_source_urls", []) + parent.get("new_primary_source_urls", []),
          new_primary_source_urls=[], prior_archive_full_rehash_performed=False,
          prior_archive_verification_seal_sha256=parent["prior_archive_verification_seal_sha256"],
          prior_payload_verification_scope="Immediate Stage185 and consumed paths rehashed; older archive inherited through seals",
          latest_collision_temperature_curvature=str(ROOT / "RESULTS.md"),
          final_validation=str(status_path),
          completion_qualification="Analytic fixed-membership curvature tested retrospectively against saved temperatures",
          validation_checks=status["count"], passed_validation_checks=status["passed_checks"],
          current_stage_retained_failures=len(status["failed_checks"]),
          all_current_checks_passed=status["all_current_precision_checks_passed"],
          all_stage_checks_including_retained_failure_passed=status["all_checks_passed"],
          all_raw_and_legacy_checks_passed=False,
          retained_failed_checks=parent.get("retained_failed_checks", []) + status["failed_checks"],
          original_bank_changed=False, emission_bank_changed=False, source_curve_changed=False,
          temperature_history_changed=False, tolerances_changed=False, no_fitted_coefficients=True,
          full_source_gate_retested=False, retained_anchor_curvature_integrations=1,
          attempted_anchor_curvature_integrations=2, new_target_collision_integrations=0,
          reused_temperature_targets=8, reused_gas_events=36, new_microscopic_source_events=0,
          new_virtual_integrals=0, boundary_contribution_explicit=True, global_continuum_derivative_bound=None,
          protected_workbench_recent_modified_file_count=0,
          protected_check_scope=status["protected_check_scope"],
          maximum_active_workers=1, physical_integrations_concurrent=1, active_workers_at_seal=0,
          library_threads_per_worker=1, largest_direct_file_count=largest,
          github_action=False, subagents=0, global_installation_changed=False, galaxy_work_modified=False,
          next_target=str(ROOT / "NEXT.md")))
    assert all(saved.digest(ROOT / name) == checksum for name, checksum in hashes.items())
    print(json.dumps(dict(sealed_files=len(hashes), cumulative_payloads=inherited + len(hashes),
                          seal_sha256=saved.digest(destination))), flush=True)


if __name__ == "__main__":
    source.modest()
    seal()

