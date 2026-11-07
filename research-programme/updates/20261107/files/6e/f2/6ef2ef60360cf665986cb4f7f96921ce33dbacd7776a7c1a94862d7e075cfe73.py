import csv
import json
import os
from datetime import datetime
from pathlib import Path
from common import ROOT, POST, CLOSURE, HIERARCHY, SOURCE, BRIDGE, NATIVE, EARLY, WAVE, GATE, ALGEBRA, modest, guard, require, check_prior, read, write, digest, load
from check_coupled_extension_serialized import physical, constraints, errors, newton_budget
import numpy as np
import psutil


def gone(record):
    stamp = record["created"]
    if isinstance(stamp, str):
        stamp = datetime.fromisoformat(stamp.replace("Z", "+00:00")).timestamp()
    try:
        return abs(psutil.Process(record["pid"]).create_time() - stamp) >= .01
    except psutil.NoSuchProcess:
        return True


def main():
    modest()
    prior = check_prior()
    checks = []
    def check(name, value):
        checks.append(dict(name=name, passed=bool(value)))
        require(value, name)
    build = read(ROOT / "build/build-result.json")
    prediction = read(ROOT / "prediction-result.json")
    config = read(ROOT / "run-config.json")
    comparison = read(ROOT / "comparison-corrected/comparison-result.json")
    check("previous stage closed", prior["state"] == "verified_closed")
    check("build complete", build["state"] == "complete")
    for group in ("original_input_hashes", "reused_object_module_hashes", "copied_package_hashes"):
        for path, checksum in build[group].items():
            check(group + " " + path, digest(path) == checksum)
    check("adapter pinned", build["source_sha256"] == digest(ROOT / "build/camb_python.f90"))
    check("isolated library pinned", build["dll_sha256"] == digest(ROOT / "build/native/camb/cambdll.dll"))
    check("compiler pinned", build["compiler_sha256"] == digest(EARLY / "toolchain/mingw64/bin/gfortran.exe"))
    imports = read(ROOT / "build/import-data.json")
    check("data copy identical", imports["sha256"] == digest(imports["source"]) == digest(ROOT / "build/native/fortran/HighLExtrapTemplate_lenspotentialCls.dat"))
    check("original adapter unchanged", imports["original_adapter_sha256"] == digest(imports["original_adapter"]))
    check("retained builder unchanged", imports["builder_sha256"] == digest(imports["reused_builder"]))
    check("wrapper unchanged", imports["wrapper_sha256"] == digest(ROOT / "build_extension.py"))
    check("temporary mappings removed", build["temporary_mappings_removed"] and all(not Path(drive + ":/").exists() for drive in ("T", "R", "S")))
    for record in build["processes"]:
        check("compiler successful " + str(record["pid"]), record["exit_code"] == 0)
        for process in [record, *record["children"]]:
            check("compiler identity exited " + str(process["pid"]), gone(process))
    for name in ("ccBAyeyI.fii", "ccytLt4f.s", "ccdRSt2J.res"):
        check("observed compiler temporary absent " + name, not (Path("D:/Temp") / name).exists())
    check("prediction complete", prediction["state"] == "complete" and prediction["error"] is None and prediction["mutually_coupled"] and prediction["original_parent_unchanged"])
    check("prediction code pinned", prediction["source_sha256"] == config["source_sha256"] == digest(ROOT / "run_coupled_extension.py"))
    check("configuration pinned", prediction["config_sha256"] == digest(ROOT / "run-config.json") and config["protocol_sha256"] == digest(ROOT / "PROTOCOL.md"))
    check("build linked", prediction["build_sha256"] == digest(ROOT / "build/build-result.json"))
    check("no future perturbations", config["no_future_perturbation_history_supplied"])
    check("comparison pinned", comparison["prediction_result_sha256"] == digest(ROOT / "prediction-result.json") and comparison["source_sha256"] == digest(ROOT / "check_coupled_extension_serialized.py"))
    check("fixed tolerances", comparison["numerical_gate"] == GATE == 2e-5 and comparison["algebra_gate"] == ALGEBRA == 1e-10)
    check("paired models", {row["model"] for row in prediction["reports"]} == {"heavy", "cold"} and len(prediction["reports"]) == 2)
    expected_cases = [("L16-base", 16, False, 2e-11, 1.), ("L64-base", 64, False, 2e-11, 1.), ("L64-fine", 64, False, 2e-12, 1.), ("L128-base", 128, False, 2e-11, 1.), ("L128-fine", 128, False, 2e-12, 1.), ("G192-fine", 192, True, 2e-12, 1.), ("L64-zero", 64, False, 2e-11, 0.), ("L64-negative", 64, False, 2e-11, -1.)]
    check("same frozen cases", config["cases"] == [list(case) for case in expected_cases])
    csv_expected = []
    source_owner = read(SOURCE / "phase-resolved/tangent-native-result.json")
    for owner in prediction["reports"]:
        guard()
        model = owner["model"]
        folder = ROOT / "runs" / model
        old = HIERARCHY / "runs-balanced" / model
        original = load(old / "native-reference.npz")
        report = next(row for row in comparison["reports"] if row["model"] == model)
        check(model + " local owner", owner == read(folder / "result.json"))
        check(model + " original reference preserved", owner["reference_sha256"] == digest(old / "native-reference.npz"))
        check(model + " initial context pinned", owner["initial_context_sha256"] == digest(folder / "initial-context.npz"))
        check(model + " original signature", np.array_equal(owner["inherited_regime"], original["signature"]))
        check(model + " mutual evolution", owner["current_species_evolved"] and not owner["future_species_histories_supplied"])
        context = load(folder / "initial-context.npz")
        for key, expected in (("initial", original["initial"]), ("initial_rate", original["derivative"][0]), ("mapping", original["mapping"]), ("signature", original["signature"])):
            check(model + " exact initial " + key, np.array_equal(context[key], expected))
        capture = read(folder / "capture-check.json")
        check(model + " single initial capture", all(capture[key] for key in ("single_capture", "exact_state", "exact_rate", "exact_observer", "exact_signature")) and not capture["future_reference_evolution_recomputed"])
        check(model + " exact window", capture["captured_time"] == original["times"][0] and capture["authorized_last_time"] == original["times"][-1])
        initial_source = next(row for row in source_owner["reports"] if row["model"] == model and row["tag"] == "one")
        check(model + " prefix ownership", capture["source_sha256"] == initial_source["sha256"] == digest(SOURCE / "phase-resolved/packets" / initial_source["file"]) and capture["initial_owner_sha256"] == owner["reference_sha256"])
        audit = read(folder / "operator-check.json")
        audit_arrays = load(folder / "operator-check.npz")
        check(model + " operator owner", audit["original_operator_sha256"] == digest(old / "operator-audit.npz"))
        check(model + " unchanged native operator", audit["maximum_operator_error"] == owner["original_operator_error"] == np.max(audit_arrays["old_operator_errors"]) == 0)
        check(model + " original16 embedding", audit["maximum16_embedding_error"] == owner["embedding16_error"] == np.max(audit_arrays["exact16_embedding_errors"]) < ALGEBRA)
        check(model + " physical speeds", np.all(audit_arrays["speeds"][:, 2:] > 0) and np.all(audit_arrays["speeds"][:, 2:] <= 1))
        check(model + " complete eight cases", [(row["tag"], row["maximum"], row["galerkin"], row["rtol"], row["amplitude"]) for row in owner["cases"]] == expected_cases)
        packets, values = {}, {}
        for case in owner["cases"]:
            tag = case["tag"]
            label = model + " " + tag
            packet = load(folder / case["file"])
            packets[tag] = packet
            values[tag] = physical(packet)
            check(label + " file ownership", case["sha256"] == digest(folder / case["file"]) and case == read(folder / (tag + ".json")))
            status = read(folder / (tag + "-solver-status.json"))
            check(label + " solver completed", status["success"] and status["returned_points"] == len(original["times"]) and status["last_time"] == original["times"][-1] and status["evaluations"] == case["evaluations"])
            check(label + " finite arrays", all(np.isfinite(array).all() for name, array in packet.items() if name != "observer_names"))
            check(label + " unchanged phase grid", np.array_equal(packet["times"], original["times"]))
            check(label + " unchanged mapping", np.array_equal(packet["mapping"], original["mapping"]))
            check(label + " expected dimensions", case["dimension"] == owner["core_dimension"] + 5 * (case["maximum"] - 2) == len(packet["units"]) and packet["projected_state"].shape == original["state"].shape)
            check(label + " identical initial data", np.array_equal(packet["projected_state"][0], case["amplitude"] * original["initial"]))
            check(label + " initial tail zero", np.count_nonzero(packet["initial_extended"][owner["core_dimension"]:]) == 0 and np.count_nonzero(packet["terminal"][0]) == 0)
            check(label + " original core and nodes", np.array_equal(packet["core"], context["core"]) and np.array_equal(packet["tail_slots"], context["tail_slots"]) and np.array_equal(packet["low_slots"], context["low_slots"]) and packet["tail_norms"].shape == (len(original["times"]), 5))
            check(label + " inherited state normalization", np.array_equal(packet["units"][:owner["core_dimension"]], context["old_normalization"][context["core"]]) and np.array_equal(packet["units"][owner["core_dimension"]:], np.tile(context["tail_units"], case["maximum"] - 2)))
            check(label + " native linearity", case["linearity"] < ALGEBRA)
            identities = constraints(values[tag])
            check(label + " independently reread metric identities", identities == report["algebra"][tag] and max(identities.values()) < ALGEBRA)
        inherited = physical(original)
        names = [name for name in inherited if name not in ("a", "H", "R")]
        replay_state = float(np.max(errors(packets["L16-base"]["projected_state"], original["state"])))
        check(model + " old finite16 state replay", replay_state == report["finite16_state_replay"] and replay_state < GATE)
        for name in names:
            check(model + " old physical replay " + name, float(errors(values["L16-base"][name], inherited[name])) == report["finite16_physical_replay"][name] < GATE)
            change = float(errors(inherited[name], values["G192-fine"][name]))
            check(model + " physical correction " + name, change == report["physical_change_from_original"][name])
        for pair in report["comparisons"]:
            left, right = pair["left"], pair["right"]
            actual = float(np.max(errors(packets[left]["projected_state"], packets[right]["projected_state"])))
            check(model + pair["label"] + " state", actual == pair["state_error"] and actual < GATE and pair["passed"])
            for name in names:
                check(model + pair["label"] + name, float(errors(values[left][name], values[right][name])) == pair["physical_errors"][name] < GATE)
        check(model + " zero response", report["zero_state"] is True and report["zero_sources"] is True and np.count_nonzero(packets["L64-zero"]["projected_state"]) == 0 and all(np.count_nonzero(values["L64-zero"][name]) == 0 for name in names))
        check(model + " sign reversal", np.array_equal(-packets["L64-negative"]["projected_state"], packets["L64-base"]["projected_state"]) and report["negative_state_error"] == 0)
        for tag, budget in report["newton"].items():
            fresh, arrays = newton_budget(packets[tag], original["probes"])
            saved = load(ROOT / budget["file"])
            check(model + tag + " budget ownership", budget["sha256"] == digest(ROOT / budget["file"]))
            check(model + tag + " budget reproduced", all(fresh[key] == budget[key] for key in fresh) and fresh["passed"])
            check(model + tag + " original Newton arrays identical", set(saved) == set(arrays) and all(np.array_equal(saved[key], array) for key, array in arrays.items()))
            check(model + tag + " saved velocity bound", np.max(np.maximum(abs(saved["theta_replayed"] - saved["theta_poisson"]) - saved["absolute_velocity_bound"], 0)) <= ALGEBRA * max(np.max(abs(saved["theta"])), 1e-30))
        for name in names:
            csv_expected.append(dict(model=model, observable=name, old_to_corrected_change=report["physical_change_from_original"][name], old16_replay=report["finite16_physical_replay"][name], precision64=report["comparisons"][0]["physical_errors"][name], precision128=report["comparisons"][1]["physical_errors"][name], angular64_128=report["comparisons"][2]["physical_errors"][name], angular128_G192=report["comparisons"][3]["physical_errors"][name]))
        check(model + " report passed", report["passed"])
    with (ROOT / "physical-comparison.csv").open(encoding="utf-8", newline="") as stream:
        rows = list(csv.DictReader(stream))
    check("CSV22 clean paired rows", len(rows) == 22 and all(None not in row and None not in row.values() for row in rows))
    check("CSV exact saved comparisons", rows == [{key: str(value) for key, value in row.items()} for row in csv_expected] and comparison["csv_sha256"] == digest(ROOT / "physical-comparison.csv"))
    partial_invalid = False
    try:
        read(ROOT / "comparison-result.json")
    except json.JSONDecodeError:
        partial_invalid = True
    check("partial failed serialization preserved and excluded", partial_invalid)
    check("accepted result separate and passing", comparison["passed"] is True)
    receipts = []
    for label, script, exit_code in (("build-01", "build_extension.py", 0), ("coupled-01", "run_coupled_extension.py", 0), ("comparison-01", "check_coupled_extension.py", 1), ("comparison-02", "check_coupled_extension_serialized.py", 0)):
        start, end = read(ROOT / (label + ".start.json")), read(ROOT / (label + ".end.json"))
        check(label + " exact receipt", all(start[key] == end[key] for key in start) and end["exit_code"] == exit_code)
        check(label + " source unchanged", end["source_sha256"] == digest(ROOT / script))
        check(label + " worker exited", gone(end))
        receipts.append(end)
    check("original failed checker preserved", digest(ROOT / "check_coupled_extension.py") == "8858d7e26c7bb731d83e87eec33da1123c400bbce0ab59c555fa5d008873907e")
    check("failure was serialization only", "not JSON serializable" in (ROOT / "comparison-01.stderr.log").read_text())
    for path in ROOT.glob("*.py"):
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
        check("compile " + path.name, True)
    check("no bytecode", not list(ROOT.rglob("__pycache__")))
    check("scattering coverage untouched", digest(BRIDGE / "final-stable-real-batch-rays037-038/common-coverage.json") == "95d628bbe34ddc317e1d954d8e556271d666645e259f0eda66245be0607a0db3")
    document = POST / "MTS-COUPLED-NEUTRINO-REPAIR-AND-NEWTON-BUDGET.md"
    sources = [NATIVE / "fortran/equations.f90", NATIVE / "fortran/MTSTwoField.f90", POST / "MTS-NEUTRINO-RETURN-AND-ANGULAR-CLOSURE-REPAIR.md", POST / "MTS-TAIL-ENERGY-AND-CAUSAL-FEEDBACK-BOUND.md"]
    for path in [document, *sources]:
        check("source exists " + str(path), path.is_file())
    artifacts = [dict(path=str(path), sha256=digest(path)) for path in ROOT.rglob("*") if path.is_file() and not path.name.startswith("validation-")]
    artifacts.append(dict(path=str(document), sha256=digest(document)))
    write(ROOT / "validation-result.json", dict(passed=True, checks=checks, pid=os.getpid(), source_sha256=digest(__file__), comparison_sha256=digest(ROOT / "comparison-corrected/comparison-result.json"), prediction_sha256=digest(ROOT / "prediction-result.json"), prior_closeout_sha256=digest(CLOSURE / "closeout.json"), artifacts=artifacts, local_sources=[dict(path=str(path), sha256=digest(path)) for path in sources], process_receipts=receipts, original_closure_failure_preserved=True, no_github_action=True, no_other_chat_process_action=True))
    print(dict(passed=True, checks=len(checks), paired_cases=16, csv_rows=len(rows)), flush=True)


if __name__ == "__main__":
    main()

