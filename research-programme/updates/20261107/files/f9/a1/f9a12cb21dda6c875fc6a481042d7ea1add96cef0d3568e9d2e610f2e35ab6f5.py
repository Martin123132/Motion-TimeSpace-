import csv
import os
from datetime import datetime
from pathlib import Path
from common import ROOT, CLOSURE, NATIVE, EARLY, POST, BRIDGE, GATE, ALGEBRA, modest, guard, require, check_prior, native_background, dense_values, read, write, digest, load
from check_background import checks_for, relative, peak
import numpy as np
from numpy.polynomial import Polynomial
import psutil


def gone(record):
    stamp = datetime.fromisoformat(record["created"].replace("Z", "+00:00")).timestamp()
    try:
        return abs(psutil.Process(record["pid"]).create_time() - stamp) >= .01
    except psutil.NoSuchProcess:
        return True


def polynomial_audit(packet):
    chosen = np.unique(np.linspace(0, len(packet["segment_start"]) - 1, 9, dtype=int))
    value_error, rate_error = 0., 0.
    for segment in chosen:
        start, end = packet["segment_start"][segment], packet["segment_end"][segment]
        width = end - start
        points = start + width * np.array([.13, .51, .89])
        local = (points - start) / width
        values, rates = dense_values(packet, points)
        reference_values, reference_rates = [], []
        for component in range(5):
            coefficients = packet["coefficients"][segment, :, component]
            polynomial = Polynomial([0.])
            if str(packet["method"]) == "DOP853":
                for degree, coefficient in enumerate(coefficients[::-1]):
                    polynomial += coefficient
                    polynomial *= Polynomial([0., 1.]) if degree % 2 == 0 else Polynomial([1., -1.])
            else:
                polynomial = Polynomial(np.r_[0., width * coefficients])
            polynomial += packet["segment_initial"][segment, component]
            reference_values.append(polynomial(local))
            reference_rates.append(polynomial.deriv()(local) / width)
        value_error = max(value_error, relative(values, np.array(reference_values).T))
        rate_error = max(rate_error, relative(rates, np.array(reference_rates).T))
    return dict(value_error=value_error, derivative_error=rate_error, independent_polynomial_segments=len(chosen))


def main():
    modest()
    prior = check_prior()
    checks = []
    def check(name, value):
        checks.append(dict(name=name, passed=bool(value)))
        require(value, name)
    check("previous verified progress", prior["state"] == "verified_closed" and prior["previous_goal_turn_classification"] == "progress")
    old_build = read(CLOSURE / "build/build-result.json")
    for group in ("original_input_hashes", "reused_object_module_hashes", "copied_package_hashes"):
        for path, checksum in old_build[group].items():
            check(group + " unchanged " + path, digest(path) == checksum)
    frozen, run, config, comparison = read(ROOT / "input-result.json"), read(ROOT / "run-result.json"), read(ROOT / "run-config.json"), read(ROOT / "comparison-result.json")
    for path, checksum in frozen["local_sources"].items():
        check("retained local source " + path, digest(path) == checksum)
    check("SciPy dense implementation pinned", digest(frozen["dense_source_path"]) == frozen["dense_source_sha256"])
    check("frozen configuration", frozen["state"] == "frozen" and frozen["source_sha256"] == digest(ROOT / "prepare_background.py") and frozen["protocol_sha256"] == digest(ROOT / "PROTOCOL.md"))
    check("frozen before evolution", datetime.fromisoformat(frozen["created_utc"]) < datetime.fromisoformat(config["created_utc"]))
    check("previous seal unchanged", frozen["previous_closeout_sha256"] == digest(CLOSURE / "closeout.json"))
    check("complete owned evolution", run["state"] == "complete" and run["error"] is None and run["source_sha256"] == config["source_sha256"] == digest(ROOT / "run_background.py"))
    check("input and config links", run["frozen_sha256"] == config["frozen_sha256"] == comparison["input_result_sha256"] == digest(ROOT / "input-result.json") and run["run_config_sha256"] == digest(ROOT / "run-config.json"))
    check("comparison pinned", comparison["source_sha256"] == digest(ROOT / "check_background.py") and comparison["run_result_sha256"] == digest(ROOT / "run-result.json"))
    check("fixed gates", comparison["numerical_gate"] == GATE == 2e-5 and comparison["algebra_gate"] == ALGEBRA == 1e-10)
    check("not a perturbation rerun", run["no_perturbation_rerun"] and comparison["no_perturbation_rerun"])
    check("paired backgrounds", len(run["reports"]) == 2 and {row["model"] for row in run["reports"]} == {"heavy", "cold"})
    expected = [["dop-base", "DOP853", 2e-10, 1.], ["dop-fine", "DOP853", 2e-12, 1.], ["dop-half-cap", "DOP853", 2e-12, .5], ["rk-independent", "RK45", 2e-11, 1.]]
    check("original declared cases", config["cases"] == expected)
    old_balance = read(CLOSURE / "balance-corrected/balance-result.json")
    polynomials, rows = [], []
    for model_owner in run["reports"]:
        guard()
        model = model_owner["model"]
        input_owner = next(row for row in frozen["reports"] if row["model"] == model)
        original = load(ROOT / "inputs" / input_owner["input"])
        reference = load(ROOT / "inputs" / input_owner["reference"])
        raw = load(input_owner["source"])
        saved_model = next(row for row in comparison["reports"] if row["model"] == model)
        check(model + " inputs owned", input_owner["input_sha256"] == model_owner["input_sha256"] == digest(ROOT / "inputs" / input_owner["input"]))
        check(model + " reference held and owned", input_owner["reference_sha256"] == digest(ROOT / "inputs" / input_owner["reference"]) and input_owner["source_sha256"] == digest(input_owner["source"]))
        check(model + " parameters unchanged", input_owner["original_parameter_sha256"] == model_owner["original_parameter_sha256"] == digest(input_owner["original_parameter_table"]))
        check(model + " exact initial fields", np.array_equal(original["initial_fields"], raw["metadata"][0, [4, 14]]))
        check(model + " exact physical grid", np.array_equal(original["original_scale"], raw["metadata"][:, 0]) and np.array_equal(original["efold"], np.log(raw["metadata"][:, 0])))
        check(model + " original source reproduction", max(input_owner["native_other_error"], input_owner["reconstructed_hubble_error"]) < ALGEBRA)
        check(model + " no future scalar solution input", not model_owner["future_scalar_reference_used_in_rhs"] and model_owner["scalar_initial_data_unchanged"])
        old_case = next(row for row in next(row for row in old_balance["reports"] if row["model"] == model)["cases"] if row["tag"] == "G192-fine")
        native = native_background(model)
        packets = {}
        for record in model_owner["cases"]:
            label = model + " " + record["tag"]
            path = ROOT / "runs" / model / record["file"]
            packet = load(path)
            packets[record["tag"]] = packet
            saved = next(row for row in saved_model["cases"] if row["tag"] == record["tag"])
            check(label + " solver output owned", record["sha256"] == saved["source_sha256"] == digest(path))
            status = read(ROOT / "runs" / model / (record["tag"] + "-status.json"))
            check(label + " solver completed interval", status["success"] and status["last_efold"] == original["efold"][-1] and status["nfev"] == record["nfev"] and status["steps"] == record["steps"])
            check(label + " same physical grid", np.array_equal(packet["efold"], original["efold"]))
            check(label + " unchanged initial state", np.array_equal(packet["normalized"][0], original["initial"]) and np.array_equal(packet["initial_fields"], original["initial_fields"]) and packet["times"][0] == original["initial_time"])
            check(label + " unchanged normalization/masses", np.array_equal(packet["units"], original["units"]) and np.array_equal(packet["masses"], original["masses"]))
            check(label + " positive inherited cap", record["max_step"] == float(original["step_cap"]) * record["cap_factor"] > 0 and record["atol"] == record["rtol"] / 100)
            check(label + " finite outputs", all(np.isfinite(value).all() for name, value in packet.items() if name != "method"))
            check(label + " valid expanding clock", np.min(packet["H"]) > 0 and np.all(np.diff(packet["times"]) > 0))
            check(label + " serialized interval coverage", packet["segment_start"][0] == packet["efold"][0] and packet["segment_end"][-1] == packet["efold"][-1] and np.array_equal(packet["segment_start"][1:], packet["segment_end"][:-1]))
            reconstructed, derivatives = dense_values(packet, packet["efold"])
            check(label + " exact dense replay", np.array_equal(reconstructed, packet["normalized"]) and np.array_equal(derivatives, packet["normalized_derivative"]) and record["dense_replay_error"] < ALGEBRA)
            node_values, _ = dense_values(packet, packet["solver_nodes"])
            check(label + " solver node agreement", relative(node_values, packet["solver_node_states"]) < ALGEBRA)
            polynomial = polynomial_audit(packet)
            polynomial.update(model=model, tag=record["tag"])
            polynomials.append(polynomial)
            check(label + " independently expanded polynomial", max(polynomial["value_error"], polynomial["derivative_error"]) < ALGEBRA)
            check(label + " displacement retained", np.array_equal(packet["displacements"], packet["normalized"][:, [0, 2]] * packet["units"][[0, 2]]) and np.array_equal(packet["fields"], packet["initial_fields"] + packet["displacements"]))
            check(label + " independently stored clock", np.array_equal(packet["clock_increment"], packet["normalized"][:, 4] * packet["units"][4]) and np.array_equal(packet["times"], original["initial_time"] + packet["clock_increment"]))
            report, arrays = checks_for(packet, reference, raw["observer"][:, 1], old_case, native)
            check(label + " full result independently reread", all(report[key] == saved[key] for key in report) and report["passed"])
            checked_path = ROOT / "comparison" / saved["file"]
            checked = load(checked_path)
            check(label + " check arrays owned", saved["sha256"] == digest(checked_path))
            check(label + " check arrays reproduced", set(arrays) == set(checked) and all(np.array_equal(value, checked[key]) for key, value in arrays.items()))
            check(label + " probe limitation explicit", saved["perturbation_recomputed"] is False)
            if model == "cold":
                check(label + " no spurious heavy field", np.count_nonzero(packet["fields"][:, 1]) == np.count_nonzero(packet["velocities"][:, 1]) == 0)
            rows.append(dict(model=model, tag=record["tag"], passed=saved["passed"], background_continuity=saved["canonical_background_continuity"], clock=saved["clock_consistency"],
                             operator_continuity=saved["probe_continuity_defect_on_old_amplitudes"], operator_momentum=saved["probe_momentum_defect_on_old_amplitudes"],
                             raychaudhuri=saved["raychaudhuri_errors"][-1], H_change=saved["changes_from_old"]["H"], clock_shift_mpc=saved["changes_from_old"]["maximum_clock_shift_mpc"]))
        for pair in saved_model["comparisons"]:
            left, right = pair["left"], pair["right"]
            errors = {name: relative(packets[left][name], packets[right][name]) for name in ("normalized", "fields", "velocities", "scalar_density", "scalar_pressure", "H", "clock_increment")}
            for name in ("normalized", "fields", "velocities", "scalar_density", "scalar_pressure"):
                for index in range(packets[right][name].shape[1]):
                    errors[name + "_" + str(index)] = relative(packets[left][name][:, index], packets[right][name][:, index])
            check(model + left + right + " matched comparison", pair["passed"] and errors == pair["errors"] and max(errors.values()) < GATE)
        check(model + " full background test passing", saved_model["passed"])
        del native
    csv_path = ROOT / "background-comparison.csv"
    with csv_path.open(encoding="utf-8", newline="") as stream:
        actual = list(csv.DictReader(stream))
    check("eight clean CSV cases", len(actual) == 8 and all(None not in row and None not in row.values() for row in actual))
    check("exact CSV ownership/content", comparison["csv_sha256"] == digest(csv_path) and actual == [{key: str(value) for key, value in row.items()} for row in rows])
    check("all fixed checks pass", comparison["passed"])
    receipts = []
    for label, script in (("inputs-01", "prepare_background.py"), ("evolution-01", "run_background.py"), ("comparison-01", "check_background.py")):
        start, end = read(ROOT / (label + ".start.json")), read(ROOT / (label + ".end.json"))
        check(label + " exact receipt", all(start[key] == end[key] for key in start) and end["exit_code"] == 0)
        check(label + " source unchanged", end["source_sha256"] == digest(ROOT / script))
        check(label + " worker exited", gone(end))
        receipts.append(end)
    for path in ROOT.glob("*.py"):
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
        check("compile " + path.name, True)
    check("no bytecode", not list(ROOT.rglob("__pycache__")))
    check("scattering coverage unchanged", digest(BRIDGE / "final-stable-real-batch-rays037-038/common-coverage.json") == "95d628bbe34ddc317e1d954d8e556271d666645e259f0eda66245be0607a0db3")
    document = POST / "MTS-CANONICAL-BACKGROUND-REPAIR-AND-CLOCK.md"
    check("physical handoff exists", document.is_file())
    artifacts = [dict(path=str(path), sha256=digest(path)) for path in ROOT.rglob("*") if path.is_file() and not path.name.startswith("validation-")]
    artifacts.append(dict(path=str(document), sha256=digest(document)))
    write(ROOT / "validation-result.json", dict(passed=True, checks=checks, source_sha256=digest(__file__), pid=os.getpid(), comparison_sha256=digest(ROOT / "comparison-result.json"), run_sha256=digest(ROOT / "run-result.json"), inputs_sha256=digest(ROOT / "input-result.json"), prior_closeout_sha256=digest(CLOSURE / "closeout.json"), artifacts=artifacts, independent_polynomial_checks=polynomials, process_receipts=receipts, web_sources=["https://docs.scipy.org/doc/scipy/reference/generated/scipy.integrate.DOP853.html"], numerical_background_repair_pass=True, no_perturbation_recompute=True, no_github_action=True, no_other_chat_process_action=True))
    print(dict(passed=True, checks=len(checks), cases=len(rows), maximum_polynomial_derivative_error=max(row["derivative_error"] for row in polynomials)), flush=True)


if __name__ == "__main__":
    main()
