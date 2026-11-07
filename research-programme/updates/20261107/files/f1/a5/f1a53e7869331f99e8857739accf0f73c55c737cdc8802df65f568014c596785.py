from source_stage193 import *


def seal():
    assert read(ROOT/"progress.json")["state"]=="validated"
    status=read(ROOT/"results/status.json")
    assert not status["identity_failures"]
    config=protocol()
    for path,value in status["authenticated_inputs"].items():
        assert saved.digest(path)==value,path
    for path,value in config["bookmark_hashes"].items():
        assert saved.digest(path)==value,path
    for path in ROOT.glob("*.py"):
        compile(path.read_text(encoding="utf-8"),str(path),"exec")
    assert not list(ROOT.rglob("__pycache__")) and not list(ROOT.rglob("*.partial"))
    for name in ("RESULTS.md","NEXT.md"):
        assert (ROOT/name).is_file()
    assert len(list((ROOT/"events").rglob("electron-*.npz")))==180
    for tag in TAGS:
        for node in config["selected"]:
            path=event_path(ROOT,tag,node)
            metadata=read(path.with_suffix(".json"))
            assert saved.digest(path)==metadata["sha256"] and not metadata["failed_checks"]
    import psutil
    for process in psutil.process_iter(["pid","name","cmdline"]):
        if process.info["pid"]==os.getpid():
            continue
        command=" ".join(process.info["cmdline"] or [])
        assert not ("python" in (process.info["name"] or "").lower() and any(
            name in command for name in ("source_stage193.py","assess_stage193.py","finish_stage193.py")))
    parent=read(PARENT/"results/stage-integrity.json")
    inherited=parent["inherited_sealed_payload_count"]+len(parent["file_hashes"])
    assert inherited==337858
    destination=ROOT/"results/stage-integrity.json"
    assert not destination.exists()
    write(ROOT/"progress.json",dict(state="complete",active_workers_after_return=0))
    hashes={path.relative_to(ROOT).as_posix():saved.digest(path)
        for path in sorted(ROOT.rglob("*")) if path.is_file() and path!=destination}
    largest=max(sum(path.is_file() for path in folder.iterdir())
        for folder in [ROOT,*[path for path in ROOT.rglob("*") if path.is_dir()]])
    assert largest<=500
    names=["checkpoint_manifest_sha256","local_source_documents","primary_pdfs","source_urls",
        "observational_source_urls","original_library_sha256","native_library_sha256","physical_source_scope",
        "retained_local_approximation_histories","raw_subtraction_response_retained","raw_failed_history_response_retained"]
    carried={key:value for key,value in parent.items() if key in names or key.startswith("latest_")}
    write(destination,dict(state="complete",stage=193,sealed_at_utc=datetime.now(timezone.utc).isoformat(),
        parent_seal_sha256=PARENT_SHA,inherited_sealed_payload_count=inherited,file_hashes=hashes,**carried,
        consumed_and_immediate_rehashed=status["authenticated_inputs"],
        previous_primary_source_urls=parent.get("previous_primary_source_urls",[])+parent.get("new_primary_source_urls",[]),
        new_primary_source_urls=[],prior_archive_full_rehash_performed=False,
        prior_archive_verification_seal_sha256=parent["prior_archive_verification_seal_sha256"],
        prior_payload_verification_scope="Immediate Stage192 and consumed paths rehashed; older archive inherited through seals",
        latest_lower_adjacent_repaired_source_combination=str(ROOT/"RESULTS.md"),final_validation=str(ROOT/"results/status.json"),
        validation_checks=status["count"],passed_validation_checks=status["passed_checks"],
        all_current_checks_passed=status["all_checks_passed"],all_raw_and_legacy_checks_passed=False,
        retained_failed_checks=parent.get("retained_failed_checks",[])+status["failed_checks"],
        current_stage_retained_failures=len(status["failed_checks"]),identity_failures=status["identity_failures"],
        source_scope=status["source_scope"],infrared_tail_changed=False,original_bank_changed=False,
        candidate_coefficients_changed=False,original_histories_changed=False,source_curve_changed=False,tolerances_changed=False,
        full_source_gate_retested_at_four_saved_nodes=True,full_population_integral=False,new_observational_test=False,
        repaired_source_events=180,reused_parent_events=540,original_event_replay=2,
        inherited_state_overlay_events=status['inherited_state_overlay_events'],
        new_virtual_integrations=0,reused_virtual_scalars=180,frequency_weights_reapplied=False,
        real_history_actions_reevaluated=True,physical_event_quadrature_changed=False,
        protected_workbench_recent_modified_file_count=status["protected_workbench_recent_modified_file_count"],
        protected_check_scope="Recent mtime since preparation; consumed paths hashed, not a full older archive rehash",
        maximum_active_workers=1,active_workers_at_seal=0,library_threads_per_worker=1,
        largest_direct_file_count=largest,github_action=False,subagents=0,global_installation_changed=False,
        galaxy_work_modified=False,next_target=str(ROOT/"NEXT.md")))
    assert all(saved.digest(ROOT/name)==value for name,value in hashes.items())
    print(json.dumps(dict(sealed_files=len(hashes),cumulative_payloads=inherited+len(hashes),
        seal_sha256=saved.digest(destination))),flush=True)


if __name__=="__main__":
    seal()
