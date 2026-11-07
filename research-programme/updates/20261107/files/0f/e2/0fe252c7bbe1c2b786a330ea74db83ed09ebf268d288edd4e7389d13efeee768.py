import os
THREADS = ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS", "NUMEXPR_NUM_THREADS", "VECLIB_MAXIMUM_THREADS", "BLIS_NUM_THREADS")
for variable in THREADS:
    os.environ[variable] = "1"
os.environ["MTS_CPU"] = "2"
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
import sys
sys.dont_write_bytecode = True
sys.setrecursionlimit(3000)
import argparse
from datetime import datetime, timezone
import hashlib
import importlib
import importlib.util
import json
from pathlib import Path
import traceback
from zoneinfo import ZoneInfo

ROOT = Path(__file__).resolve().parent
PARENT = ROOT.parent
DATA = PARENT.parent
TRANSFER = DATA / "memory-tail-transfer"
DENSE = TRANSFER / "dense-transfer-sampling"
CENTERED = TRANSFER / "centered-dense-transfer"
SCIENCE = ROOT / "science-config.json"
BASE = PARENT / "execution-v2"
BASE_SCIENCE_HASH = "7259744c79c7602e8a02b407c8e43b42a332999f29a129b3106548678add3b41"
PREPARATION_HASH = "2f70d99cf361c501fb7d0ea3fae092e82269d1790301c4c5fbd9314f0179b195"
IO_HASH = "0c57242ec4cd47a03077c7b1b1b59eaf99a8ddeb0bdbc32855d1d0516abb9d83"
with (PARENT / "history_io.py").open("rb") as stream:
    assert hashlib.file_digest(stream, "sha256").hexdigest() == IO_HASH
sys.path.insert(0, str(PARENT))
from history_io import read, write, digest
from history_policy import approval_valid, reference_blocks


def protect(event, arguments):
    if event == "open":
        path, mode, flags = arguments
        writing = (isinstance(mode, str) and any(value in mode for value in "wax+")) or flags & (os.O_CREAT | os.O_TRUNC | os.O_APPEND | os.O_WRONLY | os.O_RDWR)
        if writing and not isinstance(path, int) and not Path(path).resolve().is_relative_to(ROOT):
            raise PermissionError("write outside execution-v2 denied")
    elif event in ("os.mkdir", "os.remove", "os.rmdir", "os.rename"):
        for path in arguments[:2] if event == "os.rename" else arguments[:1]:
            if not Path(path).resolve().is_relative_to(ROOT):
                raise PermissionError("mutation outside execution-v2 denied")
    elif event in ("subprocess.Popen", "os.system", "os.posix_spawn"):
        raise PermissionError("nested process prohibited")


def runtime():
    import psutil
    process = psutil.Process()
    process.nice(psutil.BELOW_NORMAL_PRIORITY_CLASS)
    process.cpu_affinity([2])
    assert process.nice() == psutil.BELOW_NORMAL_PRIORITY_CLASS and process.cpu_affinity() == [2]
    tokens = ("history_run.py", "prepare_history.py", "centered_transfer.py", "dense_transfer.py", "transfer_experiment.py", "balanced_action.py", "full244.py", "late_bank_reference.py", "recovery_launch.py", "state_reference_audit.py", "rhs_probe_audit.py")
    for owner in psutil.process_iter(["pid", "name", "cmdline"]):
        if owner.info["pid"] != os.getpid() and (owner.info["name"] or "").lower() in ("python.exe", "pythonw.exe"):
            assert not any(token in " ".join(owner.info["cmdline"] or []) for token in tokens), "existing MTS worker; no replacement"
    ZoneInfo("Europe/London")
    return {"pid": os.getpid(), "created_time": process.create_time(), "priority": "BelowNormal", "cpu_affinity": [2], "thread_environment": {name: os.environ[name] for name in THREADS}}


def deep_sources(science=None):
    assert digest(PARENT / "experiment.json") == PREPARATION_HASH
    prepared = read(PARENT / "experiment.json")
    assert digest(prepared["input_map"]) == prepared["input_map_sha256"]
    inputs = read(prepared["input_map"])
    expected = dict(inputs["direct"])
    for path, checksum in inputs["inherited_registry_anchors"].items():
        assert digest(path) == checksum, path
        for source, record in read(path)["files"].items():
            source = str(Path(source).resolve())
            assert source not in expected or expected[source] == record["sha256"]
            expected[source] = record["sha256"]
    if science:
        assert science["preparation_sha256"] == PREPARATION_HASH
        assert digest(science["preserved_v2"]) == science["preserved_v2_sha256"]
        preservation = read(science["preserved_v2"])
        assert {str(path.resolve()) for path in BASE.rglob("*") if path.is_file()} == set(preservation["files"]), "v2 file inventory changed"
        for path, row in preservation["files"].items():
            expected[path] = row["sha256"]
        assert science["input_map_sha256"] == prepared["input_map_sha256"]
        for name, checksum in science["code_hashes"].items():
            expected[str(ROOT / name)] = checksum
        for key in ("execution_grids", "references"):
            expected[science[key]] = science[key + "_sha256"]
    for path, checksum in expected.items():
        assert digest(path) == checksum, "frozen source changed: " + path
    return prepared, {str(Path(path).resolve()): checksum for path, checksum in expected.items()}


def shared_framework():
    sys.path.insert(0, str(DENSE))
    shared = importlib.import_module("dense_transfer")
    shared.ROOT, shared.CONFIG = ROOT, SCIENCE
    old, previous, loader = shared.inherited()
    return shared, old, previous, loader


def full_integrity(prepared, loader):
    import numpy as np
    path = DATA / "delegation-trial/verify_full_outputs.py"
    assert digest(path) == "7c7c30711a1f72d53c113fa2619f6610f51f1156fd03b62ce195fa35174daa23"
    spec = importlib.util.spec_from_file_location("verified_full_integrity", path)
    verifier = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(verifier)
    settings, initial = read(loader.STAGE / "full-configuration.json"), read(loader.STAGE / "configuration.json")
    with np.load(prepared["grids"], allow_pickle=False) as packet:
        grids = {"coarse": packet["coarse"]}
    result = []
    for case in prepared["cases"]:
        row = verifier.verify_case(case["model"], case["kind"], case["subdivision"], settings, initial, grids)
        assert row["availability"] == "complete" and row["passed"], row["errors"]
        result.append({"case": case["id"], "blocks": row["blocks"], "steps": row["committed_steps"], "passed": True})
    return result


def controls():
    from control_tests import run_tests
    from serialization_safety import serialization_controls
    return {"restart_controls": run_tests(), "serialization": serialization_controls(ROOT)}


def freeze(limits):
    assert not SCIENCE.exists(), "immutable science freeze already exists"
    assert digest(BASE / "science-config.json") == BASE_SCIENCE_HASH
    base = read(BASE / "science-config.json")
    for name, expected in base["code_hashes"].items():
        assert digest(BASE / name) == expected, name
    for name in ("history_policy.py", "io_v2.py", "history_metrics.py", "control_tests.py", "SCIENCE-EXECUTION-CONTRACT.md"):
        assert (ROOT / name).read_text().rstrip() == (BASE / name).read_text().rstrip(), "unapproved helper change: " + name
    old_tiny = 'tiny = local["rate"] * duration <= science["tiny_pulse_tau_max"]'
    new_tiny = 'tiny = bool(local["rate"] * duration <= science["tiny_pulse_tau_max"])'
    original_step = (BASE / "history_step.py").read_text().rstrip()
    assert original_step.count(old_tiny) == 1
    assert (ROOT / "history_step.py").read_text().rstrip() == original_step.replace(old_tiny, new_tiny), "step changed beyond source bool cast"
    exit_path = BASE / "run-20261027T225130881Z.exit.json"
    actual_exit = read(exit_path)
    assert actual_exit["pid"] == 20920 and actual_exit["exit_code"] == 1 and actual_exit["elapsed_seconds"] == 41.7604184
    assert not list((BASE / "checkpoints").rglob("*")) and not list((BASE / "paired").rglob("*")), "v2 has unexpected committed/orphan coarse outputs"
    preserved = {"base_science_sha256": BASE_SCIENCE_HASH, "actual_exit": actual_exit,
                 "actual_exit_record": str(exit_path), "committed_extension_cells": 0,
                 "failed_attempt_not_a_commit": True,
                 "files": {str(path.resolve()): {"sha256": digest(path), "bytes": path.stat().st_size}
                           for path in sorted(BASE.rglob("*")) if path.is_file()}}
    preserved_path = ROOT / "v2-preserved-files.json"
    write(preserved_path, preserved)
    prepared, allowed = deep_sources()
    shared, old, previous, loader = shared_framework()
    fail_fast = shared.control_test()
    tests = controls()
    full = full_integrity(prepared, loader)
    names = ("history_run.py", "history_policy.py", "history_step.py", "history_metrics.py", "io_v2.py",
             "control_tests.py", "SCIENCE-EXECUTION-CONTRACT.md", "serialization_safety.py",
             "REPAIR-AUTHORIZATION.md", "JSON-SERIALIZATION-REPAIR.md")
    science = dict(base)
    science.update(version="centered-history-science-v3-serialization-only",
                   code_hashes={name: digest(ROOT / name) for name in names},
                   preserved_v2=str(preserved_path), preserved_v2_sha256=digest(preserved_path),
                   frozen_utc=datetime.now(timezone.utc).isoformat(),
                   repair_provenance={"base_science_sha256": BASE_SCIENCE_HASH, "actual_exit_pid": 20920,
                                      "actual_exit_code": 1, "committed_cells": 0,
                                      "direct_repair_authorization": str(ROOT / "REPAIR-AUTHORIZATION.md"),
                                      "new_execution_approval_required": True, "prior_attempt_promoted_to_commit": False})
    for key in ("execution_grids", "execution_grids_sha256", "references", "references_sha256", "cases",
                "joins", "thresholds", "radau_tolerances", "tiny_pulse_tau_max", "reference_rule", "startup_manifest_sha256"):
        assert science[key] == base[key], "scientific configuration changed: " + key
    for key in ("execution_grids", "references"):
        assert digest(science[key]) == science[key + "_sha256"]
    write(SCIENCE, science)
    science_hash = digest(SCIENCE)
    from io_v2 import Store
    store = Store(science, science_hash)
    assert store.paired_head["cell"] == 0 and all(row["cell"] == 0 for row in store.heads.values())
    template = {"approved": False, "science_config_sha256": science_hash, "attempt_id": "REPLACE-WITH-UNIQUE-V3-ATTEMPT",
                "first_cell": 1, "last_cell": 8, "allowed_cases": list(store.cases), "existing_heads": store.snapshot(),
                "issued_utc": datetime.now(timezone.utc).isoformat(), "turn_started_utc": "2026-10-27T22:13:00Z",
                "stop_new_work_utc": "2026-10-28T01:50:00Z", "save_report_utc": "2026-10-28T02:00:00Z",
                "acknowledged_prior_attempts": {}, "coordination_release": "Outside music priority window; no deliberate pause overridden. V2 failed attempt remains provenance, not a commit; v3 replay requires this separate approval."}
    write(ROOT / "APPROVAL-TEMPLATE.json", template)
    deep_sources(science)
    write(ROOT / "FREEZE-REPORT.json", {"science_config_sha256": science_hash, "runtime": limits, "tests": tests,
          "fail_fast_controls": fail_fast, "full_integrity": full, "verified_preparation_source_paths": len(allowed),
          "v2_files_preserved": len(preserved["files"]), "v2_actual_exit": actual_exit,
          "only_numerical_step_text_change": "Python bool cast of tiny_pulse diagnostic",
          "exact_grids_references_seeds_reused": True, "evolution_performed": False, "heads": store.snapshot()})
    print(json.dumps({"science_config": str(SCIENCE), "sha256": science_hash, "v2_files_preserved": len(preserved["files"]),
                      "same_grids_references_seeds": True, "evolution_performed": False, "approval_template": str(ROOT / "APPROVAL-TEMPLATE.json")}), flush=True)


def make_journal(shared, previous, science, approval, approval_path, limits):
    from serialization_safety import json_safe, save_terminal
    class Journal(shared.Journal):
        def __init__(self):
            self.approval, self.approval_hash = approval, digest(approval_path)
            self.science_hash = digest(SCIENCE)
            self.attempt = ROOT / "attempts" / approval["attempt_id"]
            self.attempt.mkdir(parents=True, exist_ok=False)
            with (self.attempt / "approval.json").open("xb") as stream:
                stream.write(Path(approval_path).read_bytes())
                stream.flush()
                os.fsync(stream.fileno())
            assert digest(self.attempt / "approval.json") == self.approval_hash
            self.root = self.attempt / "packets"
            self.root.mkdir()
            self.config, self.safe_json = science, json_safe
            self.checks, self.packets, self.active = shared.FailFastChecks(), [], None
            self.start = {"runtime": {**limits, "mutex_owned": True}, "config_sha256": self.science_hash, "approval": str(approval_path), "approval_sha256": self.approval_hash}
            write(self.attempt / "start.json", {**self.binding(), "state": "started", "existing_heads": approval["existing_heads"], "music_priority": science["music_priority"]})

        def binding(self):
            return {"science_config_sha256": self.science_hash, "input_map_sha256": science["input_map_sha256"], "attempt_id": approval["attempt_id"], "attempt_approval_sha256": self.approval_hash, "runtime": self.start["runtime"], "saved_utc": datetime.now(timezone.utc).isoformat()}

        def guard(self):
            from history_policy import utc
            now = datetime.now(timezone.utc)
            if now >= utc(approval["stop_new_work_utc"]):
                raise shared.PlannedSave("attempt stop-new-work deadline; no automatic restart")
            if (ROOT / "STOP-REQUEST.json").exists():
                raise shared.PlannedSave("persistent operational coordination pause; do not remove/relaunch")
            london = now.astimezone(ZoneInfo("Europe/London"))
            if 3 <= london.hour < 14:
                raise shared.PlannedSave("music-priority hours; operational pause, no numerical failure")

        def terminal(self, state, store, error=None):
            return save_terminal(self, state, store, error, science)
    return Journal()


def run(approval_path, limits):
    science = read(SCIENCE)
    prepared, allowed = deep_sources(science)
    shared, old, previous, loader = shared_framework()
    with loader.exclusive():
        runtime()
        approval_path = Path(approval_path).resolve()
        assert approval_path.is_relative_to(PARENT)
        approval = read(approval_path)
        from io_v2 import Store, prior_attempts
        store = Store(science, digest(SCIENCE))
        approval_valid(approval, digest(SCIENCE), list(store.cases), store.snapshot(), science["last_cell"])
        assert approval["acknowledged_prior_attempts"] == prior_attempts(), "unacknowledged prior attempt; no automatic retry"
        assert not (ROOT / "STOP-REQUEST.json").exists(), "coordination pause still owned; no restart"
        assert not 3 <= datetime.now(timezone.utc).astimezone(ZoneInfo("Europe/London")).hour < 14
        full = full_integrity(prepared, loader)
        journal = make_journal(shared, previous, science, approval, approval_path, limits)
        caches = {}
        try:
            audit_config = {"inputs": allowed, "preparation_sources": old["preparation_sources"]}
            authenticated = shared.authenticate_imports(audit_config, loader)
            sys.path.insert(0, str(loader.STAGE))
            sys.path.insert(0, str(loader.PRIOR))
            sys.path.insert(0, str(CENTERED))
            import tail243
            import transfer_math as original
            from owner_cache import OwnedCache
            import history_step
            import history_metrics
            sources = loader.Sources()
            sources.finish()
            comparator = shared.comparator(old, loader)
            tail243.mp.mp.dps = 80
            np = original.np
            reference_plan = read(science["references"])[f"{approval['first_cell']}:{approval['last_cell']}"]
            for cell in range(store.paired_head["cell"] + 1, approval["last_cell"] + 1):
                journal.guard()
                for case in science["cases"]:
                    if store.heads[case["id"]]["cell"] == cell:
                        continue
                    journal.guard()
                    model, subdivision = case["model"], case["subdivision"]
                    if model not in caches:
                        with np.load(case["snapshot"], allow_pickle=False) as packet:
                            snapshot = {name: packet[name].copy() for name in packet.files}
                        caches[model] = OwnedCache(model, sources.full_settings, snapshot, loader, sources)
                    cache, driver = caches[model], store.drivers[case["id"]]
                    carried = np.asarray(store.histories[case["id"]][1][-1]).copy()
                    times, tails = [], []
                    first_check, first_packet = len(journal.checks), len(journal.packets)
                    for ordinal in range(cell * subdivision, (cell + 1) * subdivision):
                        queries = reference_plan[str(subdivision)].get(str(ordinal), {}).get("times", [])
                        points, values, carried = history_step.advance(cache, case, cell, ordinal, driver, carried, store.grids, queries, science, journal, original)
                        times.extend(points[1:] if times else points)
                        tails.extend(values[1:] if tails else values)
                    lookup = {float(value): position for position, value in enumerate(times)}
                    wanted = store.grids["comparison_union"]
                    wanted = wanted[(wanted >= store.grids["coarse"][cell]) & (wanted <= store.grids["coarse"][cell + 1])]
                    indices = [lookup[float(value)] for value in wanted]
                    endpoint = (cell + 1) * subdivision
                    arrays = {"times": wanted.copy(), "tail": np.asarray(tails)[indices], "endpoint_tail": carried,
                              "profile": driver["profiles"][endpoint].copy(), "gas": np.asarray(driver["gas"][endpoint]), "work": np.asarray(driver["work"][endpoint])}
                    store.commit_case(case, cell, arrays, list(journal.checks[first_check:]), list(journal.packets[first_packet:]), journal)
                    cache.end_cell()
                history_metrics.compare(cell, store, journal, comparator, original)
            sources.finish()
            deep_sources(science)
            write(journal.attempt / "source-verification.json", {"full_integrity": full, "authenticated_imports": sorted(authenticated), "all_frozen_source_hashes_passed": True})
            terminal_state = journal.terminal("approved_batch_complete_checks_passed", store)
            return 0 if terminal_state == "approved_batch_complete_checks_passed" else 1
        except BaseException as error:
            state = "operational_pause" if isinstance(error, shared.PlannedSave) else "failed"
            terminal_state = journal.terminal(state, store, {"error": repr(error), "traceback": traceback.format_exc()})
            print(json.dumps({"state": terminal_state, "primary_state": state, "error": repr(error), "no_retry": True}), file=sys.stderr, flush=True)
            return 2 if terminal_state == "operational_pause" else 1
        finally:
            for cache in caches.values():
                cache.close()


def check():
    from io_v2 import Store, prior_attempts
    science = read(SCIENCE)
    prepared, allowed = deep_sources(science)
    store = Store(science, digest(SCIENCE))
    report = {"science_config_sha256": digest(SCIENCE), "verified_source_paths": len(allowed), "heads": store.snapshot(), "prior_attempts": prior_attempts(), "tests": controls(), "evolution_performed": False}
    write(ROOT / ("check-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ") + ".json"), report)
    print(json.dumps({"science_config_sha256": digest(SCIENCE), "verified_source_paths": len(allowed), "tests": report["tests"], "evolution_performed": False}), flush=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("mode", choices=("freeze", "check", "run"))
    parser.add_argument("--approval")
    args = parser.parse_args()
    sys.addaudithook(protect)
    try:
        limits = runtime()
        if args.mode == "freeze":
            freeze(limits)
        elif args.mode == "check":
            check()
        else:
            assert args.approval, "separate supervisor approval required"
            raise SystemExit(run(args.approval, limits))
    except Exception as error:
        write(ROOT / ("startup-failure-" + datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S%fZ") + ".json"), {"pid": os.getpid(), "phase": args.mode, "error": repr(error), "traceback": traceback.format_exc(), "no_retry": True})
        raise
