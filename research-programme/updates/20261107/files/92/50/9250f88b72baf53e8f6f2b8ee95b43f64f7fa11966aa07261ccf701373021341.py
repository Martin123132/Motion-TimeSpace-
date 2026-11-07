import csv
import math
from pathlib import Path
from common import ROOT, SECOND, BACKGROUND, BRIDGE, ALGEBRA, GATE, modest, guard, check_parent, require, read, write, digest


def main():
    modest()
    check_parent()
    checks = []
    def check(name, passed, detail=None):
        checks.append(dict(name=name, passed=bool(passed), detail=detail))
    result = read(ROOT / "result.json")
    probe = read(ROOT / "probe-result.json")
    check("completed_all_histories", result["state"] == "complete" and result["passed"] and result["histories"] == 42)
    check("independent_derivative_probe_count", probe["passed"] and probe["probes"] == 97 and len(probe["rows"]) == 3)
    check("no_new_trajectory_or_prediction", result["new_evolutions"] == 0 and not result["independent_forward_prediction"] and not result["averaged_forward_qualification_claimed"])
    for row in probe["rows"]:
        for name, value in row["algebra"].items():
            check("probe/" + row["label"] + "/" + name, math.isfinite(value) and 0 <= value < ALGEBRA, value)
        check("probe/" + row["label"] + "/frozen_steps", [entry["step"] for entry in row["derivative_checks"]] == [1e-6, 5e-7])
        for entry in row["derivative_checks"]:
            for name in ("coefficients", "generator", "transform"):
                value = entry[name]
                check("derivative/" + row["label"] + "/" + str(entry["step"]) + "/" + name, math.isfinite(value) and 0 <= value < GATE, value)
        check("probe/" + row["label"] + "/rest_density_refinement", 0 <= row["rest_density_refinement_rate_error"] < GATE)
    for name, value in probe["node_checks"].items():
        check("background_node/" + name, math.isfinite(value) and 0 <= value < ALGEBRA, value)
    for name, value in probe["background_interpolation_checks"].items():
        check("background_interpolation/" + name, math.isfinite(value) and 0 <= value < GATE, value)
    authority = {}
    for manifest in ("frozen-inputs.json", "replay-frozen-inputs.json"):
        frozen = read(ROOT / manifest)
        check(manifest + "/tolerances", frozen["algebra"] == ALGEBRA and frozen["numerical"] == GATE)
        for path, expected in frozen["sources"].items():
            guard()
            actual = digest(path)
            check("frozen/" + manifest + "/" + Path(path).name, actual == expected)
            authority[path] = actual
    background_seal = read(BACKGROUND / "closeout.json")
    check("background_seal", background_seal["state"] == "verified_closed" and background_seal["validation_sha256"] == "d8bb334d7f0d4532073e760be03dc65ab2c1382bfdf5b63ec94658afdfb2a0c2")
    inputs = [BACKGROUND / "runs/heavy/dop-half-cap.npz", SECOND / "common.py", SECOND / "prediction-result.json"]
    for path in inputs:
        expected = [item["sha256"] for item in background_seal.get("artifacts", []) if Path(item["path"]).resolve() == path.resolve()]
        if path.parent.name == "heavy":
            require(len(expected) == 1, "background artifact ownership")
            check("background_dense_packet_integrity", digest(path) == expected[0])
        authority[str(path)] = digest(path)
    owner = read(SECOND / "prediction-result.json")
    expected_cases = {(family["model"] + "-" + family["label"], case["tag"]): case for family in owner["reports"] for case in family["cases"]}
    actual_cases = {(row["family"], row["tag"]): row for row in result["rows"]}
    check("exact_saved_case_coverage", len(result["rows"]) == len(actual_cases) == 42 and set(expected_cases) == set(actual_cases))
    for key, row in actual_cases.items():
        guard()
        name = "/".join(key)
        path = ROOT / "records" / (row["family"] + "-" + row["tag"] + ".json")
        check(name + "/record_consistency", read(path) == row)
        check(name + "/input_integrity", row["sha256"] == expected_cases[key]["sha256"] and digest(row["input"]) == row["sha256"])
        for label, value in row["algebra_checks"].items():
            check(name + "/" + label, math.isfinite(value) and 0 <= value < ALGEBRA, value)
        diagnostics = row["diagnostics"]
        check(name + "/raw_flow", max(diagnostics["raw_flow_component_errors"]) < GATE)
        check(name + "/constraints", max(diagnostics["constraints"].values()) < GATE)
        replays = diagnostics["integral_replays"]
        check(name + "/replay_strides", [entry["stride"] for entry in replays] == [1, 2, 4])
        for kind in ("raw", "accounted"):
            check(name + "/" + kind + "_finest_replay", replays[0][kind + "_maximum"] < GATE)
            check(name + "/" + kind + "_finest_change", diagnostics["replay_refinement"][kind]["medium_to_fine"] < GATE)
            check(name + "/" + kind + "_refinement_shrinks", diagnostics["replay_refinement"][kind]["change_shrinks"])
        check(name + "/qualification", row["algebra_passed"] and diagnostics["numerical_passed"] and row["passed"])
        if key[0].startswith("heavy-") and key[1] == "G192-reduced-fine":
            check(name + "/frozen_omission_detected", max(diagnostics["frozen_flow_component_errors"]) > GATE)
        if key[1].endswith("-zero"):
            check(name + "/exact_zero_control", diagnostics["zero_control"] and max(diagnostics["raw_flow_component_errors"]) == 0 and replays[0]["raw_maximum"] == 0)
        if key[0].startswith("cold-"):
            check(name + "/identity_control", row["algebra_checks"]["cold_identity"] == 0 and max(diagnostics["omitted_actual_coefficient_rate_errors"]) == 0)
    with (ROOT / "summary.csv").open(newline="", encoding="utf-8") as stream:
        csv_rows = list(csv.DictReader(stream))
    check("csv_count", len(csv_rows) == 42 and all(None not in row for row in csv_rows))
    compiled = {}
    for path in sorted(ROOT.glob("*.py")):
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
        compiled[str(path)] = digest(path)
        check("compile/" + path.name, True)
    coverage = BRIDGE / "final-stable-real-batch-rays037-038/common-coverage.json"
    check("original_scattering_coverage_unchanged", digest(coverage) == "95d628bbe34ddc317e1d954d8e556271d666645e259f0eda66245be0607a0db3")
    check("no_bytecode", not list(ROOT.rglob("__pycache__")))
    check_parent()
    passed = all(item["passed"] for item in checks)
    write(ROOT / "validation.json", dict(passed=passed, count=len(checks), checks=checks, compiled_sources=compiled,
          authority_sources=authority, result_sha256=digest(ROOT / "result.json"), probe_sha256=digest(ROOT / "probe-result.json"),
          csv_sha256=digest(ROOT / "summary.csv")))
    print("Validation", passed, len(checks), "checks", flush=True)
    for item in checks:
        if not item["passed"]:
            print("FAIL", item, flush=True)
    require(passed, "validation failure; inspect, do not retry")


if __name__ == "__main__":
    main()
