import csv
import os
from datetime import datetime
from common import ROOT, POST, PRIOR, HIERARCHY, BRIDGE, WAVE, GATE, ALGEBRA, modest, require, check_prior, read, write, digest, load
import numpy as np
import mpmath as mp
import psutil


def gone(record):
    stamp = datetime.fromisoformat(record["created"].replace("Z", "+00:00")).timestamp()
    try:
        return abs(psutil.Process(record["pid"]).create_time() - stamp) >= .01
    except psutil.NoSuchProcess:
        return True


def score(predicted, target):
    return np.max(abs(predicted - target), axis=0) / np.maximum(np.max(abs(target), axis=0), 1e-80)


def main():
    modest()
    prior_seal = check_prior()
    checks = []
    def check(name, value):
        checks.append(dict(name=name, passed=bool(value)))
        require(value, name)
    frozen = read(ROOT / "frozen-predictions.json")
    config = read(ROOT / "control-config.json")
    control = read(ROOT / "control-result.json")
    comparison = read(ROOT / "closure-comparison-result.json")
    spectral = read(ROOT / "spectral-forcing-result.json")
    check("previous turn progress", prior_seal["previous_goal_turn_classification"] == "progress")
    check("frozen source", frozen["source_sha256"] == digest(ROOT / "freeze_free_streaming.py"))
    check("frozen before controls", frozen["state"] == "frozen_before_higher_order_controls" and datetime.fromisoformat(frozen["created_utc"]) < datetime.fromisoformat(config["created_utc"]))
    check("shared fixed protocol", config["protocol_sha256"] == frozen["protocol_sha256"] == digest(ROOT / "PROTOCOL.md"))
    check("all40 controls complete", control["state"] == "complete" and len(control["reports"]) == 40)
    check("controls pinned", control["source_sha256"] == config["source_sha256"] == digest(ROOT / "run_closure_controls.py") and control["config_sha256"] == digest(ROOT / "control-config.json"))
    check("frozen controls linkage", config["frozen_result_sha256"] == control["frozen_result_sha256"] == comparison["frozen_result_sha256"] == digest(ROOT / "frozen-predictions.json"))
    check("comparison source", comparison["source_sha256"] == digest(ROOT / "compare_closures.py") and comparison["control_result_sha256"] == digest(ROOT / "control-result.json"))
    check("fixed gates", comparison["numerical_gate"] == GATE == 2e-5 and comparison["algebra_gate"] == ALGEBRA == 1e-10)
    check("numerical success distinguished from closure failure", comparison["numerics_passed"] and not comparison["legacy_closure_adequate"])
    check("no saved parent history overwritten", comparison["no_parent_solution_overwrite"] and control["parent_histories_reused"] and not control["parent_history_changed"])
    check("spectral forcing pinned", spectral["passed"] and spectral["source_sha256"] == digest(ROOT / "spectral_forcing.py") and spectral["decision_sha256"] == digest(ROOT / "SPECTRAL-FORCING-EXTENSION.md"))
    check("spectral result conditional", spectral["source_histories_fixed"] and not spectral["coupled_corrected_solution_claimed"])
    spectra = {}
    for record in frozen["eigen_reports"]:
        maximum = record["maximum"]
        packet = load(ROOT / "predictions" / record["file"])
        check("spectrum hash " + str(maximum), record["sha256"] == digest(ROOT / "predictions" / record["file"]))
        moments = np.arange(3, maximum)
        expected = (moments + 1) / np.sqrt((2 * moments + 1) * (2 * moments + 3))
        check("Legendre recurrence " + str(maximum), np.array_equal(expected, packet["offdiagonal"]))
        matrix = np.diag(expected, 1) + np.diag(expected, -1)
        check("eigenpair residual " + str(maximum), np.max(abs(matrix @ packet["vectors"] - packet["vectors"] * packet["eigenvalues"])) < ALGEBRA)
        check("orthogonal spectral basis " + str(maximum), np.max(abs(packet["vectors"].T @ packet["vectors"] - np.eye(maximum - 2))) < ALGEBRA)
        check("positive normalized spectral measure " + str(maximum), np.min(packet["weights"]) >= 0 and abs(np.sum(packet["weights"]) - 1) < ALGEBRA and np.array_equal(packet["weights"], packet["vectors"][0] ** 2))
        check("spectrum in angular support " + str(maximum), np.max(abs(packet["eigenvalues"])) <= 1 + ALGEBRA)
        spectra[maximum] = packet
    packets = {}
    for record in control["reports"]:
        key = record["model"], record["kind"], record["release_fraction"], record["maximum"], record["rtol"]
        data = load(ROOT / "controls" / record["file"])
        packets[key] = data
        label = record["file"]
        check(label + " ownership", record["sha256"] == digest(ROOT / "controls" / label))
        check(label + " finite", all(np.isfinite(value).all() for name, value in data.items() if name != "groups"))
        check(label + " successful solver", record["success"] and record["rtol"] in (2e-11, 2e-12))
        check(label + " original five momentum nodes", data["returned"].shape[1] == 5)
    prior_inputs = read(PRIOR / "input-result.json")
    mp.mp.dps = 60
    for prediction in frozen["predictions"]:
        model, fraction = prediction["model"], prediction["release_fraction"]
        name = model + str(fraction)
        data = load(ROOT / "predictions" / prediction["file"])
        check(name + " frozen ownership", prediction["sha256"] == digest(ROOT / "predictions" / prediction["file"]))
        original = HIERARCHY / "runs-balanced" / model / "native-reference.npz"
        owner = next(row for row in prior_inputs["reports"] if row["model"] == model)
        check(name + " reference chain", prediction["native_reference_sha256"] == owner["reference_sha256"] == digest(original))
        old_path = PRIOR / "results" / model / ("impulse-" + str(int(100 * fraction)) + ".npz")
        check(name + " old impulse preserved", prediction["source_impulse_sha256"] == digest(old_path))
        old = load(old_path)
        check(name + " original probe grid", np.array_equal(data["times"], old["times"]))
        check(name + " causal streaming distance", np.count_nonzero(data["distance"][0]) == 0 and np.min(data["distance"]) >= 0 and np.min(np.diff(data["distance"], axis=0)) >= 0)
        for index, maximum in enumerate(data["levels"]):
            spectrum = spectra[int(maximum)]
            reconstructed = np.column_stack([np.cos(np.outer(data["distance"][:, node], spectrum["eigenvalues"])) @ spectrum["weights"] for node in range(5)])
            check(name + str(maximum) + " direct spectral response", np.array_equal(reconstructed, data["response"][index]))
            expected = -9 * WAVE ** 2 / 35 * data["speed"] * data["initial_speed"] * reconstructed
            check(name + str(maximum) + " returned port units/sign", np.array_equal(expected, data["kernels"][index]) and np.max(expected[0]) < 0)
            for node in range(5):
                distance = mp.mpf(float(np.max(data["distance"][:, node])))
                order = 2 * (int(maximum) - 2)
                high_precision = mp.mpf(2) if order <= distance else min(mp.mpf(2), 2 * distance ** order / mp.factorial(order) / (1 - distance / (order + 1)))
                actual = mp.mpf(float(data["analytic_shape_error"][index, node]))
                check(name + str(maximum) + str(node) + " truncation majorant evaluation", abs(actual / high_precision - 1) < mp.mpf("1e-10"))
        check(name + " uniform finest angular bound", np.max(data["analytic_shape_error"][-1]) < GATE)
        report = next(row for row in comparison["reports"] if row["model"] == model)
        target = data["kernels"][-1]
        actuals = {16: old["kernels"][:, 2:], 32: packets[model, "impulse", fraction, 32, 2e-12]["returned"], 64: packets[model, "impulse", fraction, 64, 2e-12]["returned"]}
        for maximum, actual in actuals.items():
            errors = score(actual, target)
            recorded = [row for row in report["impulses"] if row["maximum"] == maximum and row["release_fraction"] == fraction]
            check(name + str(maximum) + " all five comparison rows", len(recorded) == 5)
            for index, row in enumerate(recorded):
                check(name + str(maximum) + str(index) + " independent discrepancy", errors[index] == row["error"] and row["closure_adequate"] == bool(errors[index] < GATE))
    for report in comparison["reports"]:
        model = report["model"]
        check(model + " original inadequate and64 adequate", not report["legacy_L16_adequate"] and report["higher_L64_adequate"])
        check(model + " conditional correction only", report["source_forcing_is_frozen"] and not report["coupled_corrected_solution_claimed"])
        data = load(ROOT / report["source_correction_file"])
        check(model + " correction owner", report["source_correction_sha256"] == digest(ROOT / report["source_correction_file"]))
        check(model + " correction identity", np.array_equal(data["correction"], data["corrected_return"] - data["original_return"]))
        check(model + " forced source replay", np.array_equal(score(data["replay_return"], data["original_return"]), report["original_forcing_replay"]) and max(report["original_forcing_replay"]) < GATE)
        check(model + " higher forced convergence", np.array_equal(score(data["L64_return"], data["corrected_return"]), report["high_order_forcing_convergence"]) and max(report["high_order_forcing_convergence"]) < GATE)
        check(model + " preserved low-order forcing discrepancy", np.array_equal(score(data["original_return"], data["corrected_return"]), report["original_forced_return_error"]))
        check(model + " all integration refinements", all(row["passed"] and row["maximum_refinement"] < GATE for row in report["precision"]))
    for report in spectral["reports"]:
        model = report["model"]
        data = {}
        for run in report["runs"]:
            label = model + run["tag"]
            data[run["tag"]] = load(ROOT / "spectral-forcing" / run["file"])
            check(label + " spectral output ownership", run["sha256"] == digest(ROOT / "spectral-forcing" / run["file"]))
            check(label + " imaginary cancellation", run["imaginary_relative"] < ALGEBRA)
        control_data = load(ROOT / (model + "-forced-correction.npz"))
        check(model + " independent spectral/native forcing", np.array_equal(score(control_data["corrected_return"], data["fine"]["returned"]), report["independent_native_L128"]) and max(report["independent_native_L128"]) < GATE)
        check(model + " source interpolation control", np.array_equal(score(data["coarse-source"]["returned"], data["fine"]["returned"]), report["source_stride"]) and max(report["source_stride"]) < GATE)
        check(model + " spectral precision", np.array_equal(score(data["base"]["returned"], data["fine"]["returned"]), report["precision"]) and max(report["precision"]) < GATE)
    with (ROOT / "closure-comparison.csv").open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    check("CSV ownership", comparison["csv_sha256"] == digest(ROOT / "closure-comparison.csv"))
    check("ninety clean CSV rows", len(rows) == 90 and all(None not in row and None not in row.values() for row in rows))
    check("CSV contains explicit failures", any(row["closure_adequate"] == "False" for row in rows if row["maximum"] == "16"))
    receipts = []
    for label, script in (("freeze-01", "freeze_free_streaming.py"), ("controls-01", "run_closure_controls.py"), ("comparison-01", "compare_closures.py"), ("spectral-01", "spectral_forcing.py")):
        start, end = read(ROOT / (label + ".start.json")), read(ROOT / (label + ".end.json"))
        check(label + " exact receipt", start["pid"] == end["pid"] and start["created"] == end["created"] and start["command"] == end["command"] and end["exit_code"] == 0)
        check(label + " source preserved", end["source_sha256"] == digest(ROOT / script))
        check(label + " worker exited", gone(end))
        receipts.append(end)
    for path in ROOT.glob("*.py"):
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
        check("compile " + path.name, True)
    check("no bytecode", not list(ROOT.rglob("__pycache__")))
    check("scattering source unchanged", digest(BRIDGE / "final-stable-real-batch-rays037-038/common-coverage.json") == "95d628bbe34ddc317e1d954d8e556271d666645e259f0eda66245be0607a0db3")
    sources = [POST / "condensate-origin-20261003/native-heavy-matching-20261007/native/fortran/equations.f90", POST / "MTS-TAIL-ENERGY-AND-CAUSAL-FEEDBACK-BOUND.md"]
    for path in sources:
        check("local source exists " + str(path), path.is_file())
    document = POST / "MTS-NEUTRINO-RETURN-AND-ANGULAR-CLOSURE-REPAIR.md"
    check("physical interpretation handoff", document.is_file())
    artifacts = [dict(path=str(path), sha256=digest(path)) for path in ROOT.rglob("*") if path.is_file() and not path.name.startswith("validation-")]
    artifacts.append(dict(path=str(document), sha256=digest(document)))
    write(ROOT / "validation-result.json", dict(passed=all(row["passed"] for row in checks), checks=checks, pid=os.getpid(), source_sha256=digest(__file__), comparison_sha256=digest(ROOT / "closure-comparison-result.json"), spectral_sha256=digest(ROOT / "spectral-forcing-result.json"), prior_closeout_sha256=digest(PRIOR / "closeout.json"), artifacts=artifacts, local_sources=[dict(path=str(path), sha256=digest(path)) for path in sources], web_sources=["https://arxiv.org/html/astro-ph/9506072v1"], process_receipts=receipts, legacy_closure_adequate=False, independent_numerical_checks_pass=True, no_github_action=True, no_other_chat_process_action=True))
    print(dict(passed=True, checks=len(checks), csv_rows=len(rows), legacy_closure_adequate=False, independent_numerics_passed=True), flush=True)


if __name__ == "__main__":
    main()
