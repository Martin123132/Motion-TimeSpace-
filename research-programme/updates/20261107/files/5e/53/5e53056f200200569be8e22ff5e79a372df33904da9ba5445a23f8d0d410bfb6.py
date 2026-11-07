import csv
import os
from datetime import datetime
from pathlib import Path
from common import ROOT, POST, SOURCE, PHASE, BRIDGE, modest, require, read, write, digest
import numpy as np
import psutil


def gone(identity):
    stamp = datetime.fromisoformat(identity["created"].replace("Z", "+00:00")).timestamp()
    try:
        return abs(psutil.Process(identity["pid"]).create_time() - stamp) >= .01
    except psutil.NoSuchProcess:
        return True


def archive(path):
    with np.load(path) as data:
        return {name: data[name].copy() for name in data.files}


def main():
    modest()
    checks = []

    def check(name, passed):
        checks.append(dict(name=name, passed=bool(passed)))
        require(passed, name)

    phase_seal = read(PHASE / "closeout.json")
    check("previous closed progress", phase_seal["state"] == "verified_closed")
    check("previous validation pinned", digest(PHASE / "validation-result.json") == "1cb5560de24ae40dd6368948b27b419a5b0ae448aedc704597f5471c348f036b")
    for row in phase_seal["artifacts"]:
        check("phase artifact: " + Path(row["path"]).name, digest(row["path"]) == row["sha256"])
    for row in phase_seal["handoff_artifacts"]:
        if Path(row["path"]).name == "MTS-PHASE-STRESS-CURRENT-AND-AVERAGING-REMAINDER.md":
            check("previous physics document", digest(row["path"]) == row["sha256"])
    original = read(SOURCE / "phase-resolved/tangent-native-result.json")
    for path, checksum in original["original_source_hashes"].items():
        check("original source: " + str(Path(path).relative_to(POST)), digest(path) == checksum)
    check("scattering unchanged", digest(BRIDGE / "final-stable-real-batch-rays037-038/common-coverage.json") == "95d628bbe34ddc317e1d954d8e556271d666645e259f0eda66245be0607a0db3")
    derivation = read(ROOT / "derivation-result.json")
    check("symbolic owner", derivation["source_sha256"] == digest(ROOT / "derive_window_feedback.py"))
    check("nine identities", derivation["passed"] and len(derivation["checks"]) == 9 and all(row["passed"] and row["residual"] == "0" for row in derivation["checks"]))
    manifest = read(ROOT / "input-manifest.json")
    config = read(ROOT / "run-config.json")
    prediction = read(ROOT / "prediction-result.json")
    corrected = ROOT / "comparison-corrected"
    result, failed = read(corrected / "comparison-result.json"), read(ROOT / "comparison-result.json")
    check("preparation owner", manifest["source_sha256"] == digest(ROOT / "prepare_window_inputs.py"))
    check("frozen protocol", manifest["frozen_protocol_sha256"] == digest(ROOT / "PROTOCOL.md"))
    check("initial symbolic linkage", manifest["symbolic_sha256"] == digest(ROOT / "derivation-result.json"))
    check("config owner", config["source_sha256"] == digest(ROOT / "run_window_feedback.py") and config["input_manifest_sha256"] == digest(ROOT / "input-manifest.json"))
    check("prediction owner", prediction["source_sha256"] == digest(ROOT / "run_window_feedback.py") and prediction["config_sha256"] == digest(ROOT / "run-config.json"))
    check("eighteen predictions completed", prediction["state"] == "complete" and prediction["error"] is None and len(prediction["reports"]) == 18)
    check("case order frozen", all([record["case"] for record in prediction["reports"] if record["model"] == model] == config["cases"] for model in ("heavy", "cold")))
    check("accepted checker owner", result["source_sha256"] == digest(ROOT / "check_window_feedback.py"))
    check("failed checker preserved", failed["passed"] is False and failed["source_sha256"] == digest(ROOT / "check_window_feedback_attempt02.py"))
    check("comparison linkage", result["prediction_sha256"] == digest(ROOT / "prediction-result.json") and result["input_manifest_sha256"] == digest(ROOT / "input-manifest.json"))
    check("acceptance gates retained", result["passed"] and result["gate"] == 2e-5 and result["algebra_gate"] == 1e-10 and failed["gate"] == result["gate"])
    model_evidence = []
    for owner in manifest["rows"]:
        model = owner["model"]
        for key, hash_key in (("original_packet", "original_sha256"), ("input_file", "input_sha256"), ("reference_file", "reference_sha256")):
            path = Path(owner[key]) if key == "original_packet" else ROOT / owner[key]
            check(model + " " + key, digest(path) == owner[hash_key])
        inputs = archive(ROOT / owner["input_file"])
        check(model + " input contains no future selected state", set(inputs) == {"times", "input_names", "inputs", "initial", "normalization", "source_scale", "wave", "boundaries", "evaluation", "probes", "model"} and inputs["initial"].shape == inputs["normalization"].shape and inputs["inputs"].shape[1] == 10)
        reference = archive(ROOT / owner["reference_file"])
        full = archive(ROOT / "predictions" / (model + "-full.npz"))
        indices = np.searchsorted(full["times"], reference["times"])
        norm = np.maximum(np.max(abs(reference["state"]), axis=0), 1e-30)
        state_errors = np.max(abs(full["state"][indices] - reference["state"]), axis=0) / norm
        row = next(item for item in result["reports"] if item["model"] == model)
        check(model + " reference score reproduced", abs(float(np.max(state_errors)) - row["state_error"]) < 1e-14 and np.max(state_errors) < 2e-5)
        check(model + " controls and source gates", row["passed"] and row["zero_direction_exact"] and row["negative_direction_error"] < 2e-5 and max(row["source_errors"].values()) < 2e-5 and max(row["algebra"].values()) < 1e-10)
        check(model + " scope explicit", row["selected_future_state_supplied"] is False and row["other_species_history_supplied"] is True)
        budget = archive(corrected / row["newton_budget"]["file"])
        check(model + " budget owner", digest(corrected / row["newton_budget"]["file"]) == row["newton_budget"]["sha256"])
        check(model + " repair did not change budget arrays", digest(ROOT / row["newton_budget"]["file"]) == digest(corrected / row["newton_budget"]["file"]))
        residual = float(np.max(abs(budget["duhamel_difference"] - budget["actual_difference"]) / budget["state_scale"]))
        check(model + " corrected Duhamel normalization independently computed", abs(residual - row["newton_budget"]["duhamel_residual_state_scaled"]) < 1e-18 and residual < 2e-5)
        violation = float(np.max((abs(budget["actual_difference"]) - budget["interpolant_bound"]) / budget["state_scale"]))
        check(model + " bound checked pointwise", violation <= 2e-5 and row["newton_budget"]["continuum_certified"] is False)
        check(model + " source refinements unchanged", all(max(item.values()) < 2e-5 for item in row["refinements"].values()))
        check(model + " window refinements", max(row["window_mean_errors_raw_source_scaled"]) < 2e-5 and all(max(item) < 2e-5 for item in row["window_mean_refinements_raw_source_scaled"].values()))
        model_evidence.append(dict(model=model, state_errors=state_errors.tolist(), independently_recomputed_duhamel_residual=residual, accepted_pressure_average_error=row["complete_window_pressure_error_pressure_scaled"]))
    for row in prediction["reports"]:
        path = ROOT / "predictions" / row["file"]
        check(row["file"] + " sealed", digest(path) == row["sha256"])
        data = archive(path)
        check(row["file"] + " finite predictions", all(np.isfinite(value).all() for value in data.values()))
        check(row["file"] + " monotone time", np.all(np.diff(data["times"]) > 0))
    check("unchanged window CSV after normalization repair", digest(ROOT / "window-comparison.csv") == result["window_csv_sha256"] == digest(corrected / "window-comparison.csv"))
    with (corrected / "window-comparison.csv").open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        rows = list(reader)
        columns = reader.fieldnames
    check("378 finite comparison rows", len(rows) == 378 and all(None not in row and None not in row.values() and all(np.isfinite(float(row[key])) for key in columns if key not in ("model", "complete_cycle")) for row in rows))
    runner = (ROOT / "run_window_feedback.py").read_text(encoding="utf-8")
    check("reviewed runner does not access reference file key", 'owner["reference_file"]' not in runner and 'reference.npz' not in runner)
    records = []
    expected = [("derivation-01", 0, "derive_window_feedback.py"), ("preparation-01", 0, "prepare_window_inputs.py"), ("forward-01", 0, "run_window_feedback.py"), ("comparison-01", 1, "check_window_feedback_attempt01.py"), ("comparison-02", 1, "check_window_feedback_attempt02.py"), ("comparison-03", 0, "check_window_feedback.py")]
    for label, exit_code, source in expected:
        start, end = read(ROOT / (label + ".start.json")), read(ROOT / (label + ".end.json"))
        check(label + " receipt", start["pid"] == end["pid"] and start["created"] == end["created"] and start["command"] == end["command"] and end["exit_code"] == exit_code)
        check(label + " code preserved", end["source_sha256"] == digest(ROOT / source))
        check(label + " exited", gone(end))
        records.append(end)
    for path in ROOT.glob("*.py"):
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
        check("compile " + path.name, True)
    check("no bytecode created", not list(ROOT.rglob("__pycache__")))
    others = []
    for process in psutil.process_iter(["pid", "create_time", "name", "cmdline"]):
        try:
            info = process.info
            if info["pid"] != os.getpid() and (info["name"] or "").lower() == "python.exe" and any(token in " ".join(info["cmdline"] or []) for token in ("mts-window-feedback-20261107", "mts-phase-stress-20261107", "source-readout-bridge-20261102")):
                others.append(info)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass
    check("no outstanding owned numerical worker", not others)
    document = POST / "MTS-WINDOW-EVOLUTION-AND-SELF-GRAVITY.md"
    check("physics handoff exists", document.is_file())
    artifacts = [dict(path=str(path), sha256=digest(path)) for path in ROOT.rglob("*") if path.is_file() and not path.name.startswith("validation-")]
    artifacts.append(dict(path=str(document), sha256=digest(document)))
    write(ROOT / "validation-result.json", dict(passed=all(row["passed"] for row in checks), pid=os.getpid(), checks=checks, accepted_comparison=str(corrected / "comparison-result.json"), accepted_sha256=digest(corrected / "comparison-result.json"), previous_failed_comparison_sha256=digest(ROOT / "comparison-result.json"), evidence=model_evidence, process_receipts=records, remaining_workers=others, source_sha256=digest(__file__), artifacts=artifacts, original_inputs_preserved=True, github_action=False, unrelated_process_action=False))
    print(dict(passed=True, checks=len(checks), evidence=model_evidence), flush=True)


if __name__ == "__main__":
    main()

