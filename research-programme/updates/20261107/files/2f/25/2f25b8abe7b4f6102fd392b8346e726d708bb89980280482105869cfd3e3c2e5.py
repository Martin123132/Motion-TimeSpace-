import csv
import math
from pathlib import Path
from common import ROOT, PREVIOUS, SECOND, PARENT, BRIDGE, ALGEBRA, GATE, modest, guard, check_parent, require, read, write, digest
from mean_math import Background, phase_background, polynomials, constraint_polynomial, evaluate, sup, norm, load
import numpy as np


def main():
    modest()
    check_parent()
    checks = []
    def check(name, value, detail=None):
        checks.append(dict(name=name, passed=bool(value), detail=detail))
    result = read(ROOT / "result.json")
    bounds = read(ROOT / "remainder-bounds.json")
    frozen = read(ROOT / "frozen-inputs.json")
    check("completed", result["state"] == "complete" and result["passed"])
    check("scope", result["new_trajectories"] == 0 and not result["closed_cosmological_mean_forward_qualified"])
    check("frozen_orders_and_gates", frozen["orders"] == [0, 1, 2, 3] and frozen["intended_order"] == 2 and frozen["phases"] == [32, 64] and frozen["algebra"] == ALGEBRA and frozen["numerical"] == GATE)
    check("probe_counts", result["anchors"] == 33 and result["interior_probes"] == 32 and len(result["families"]) == 3)
    authority = {}
    for source_set in (frozen["sources"], bounds["source_hashes"], read(PREVIOUS / "validation.json")["authority_sources"]):
        for path, expected in source_set.items():
            guard()
            actual = digest(path)
            check("source/" + str(path), actual == expected)
            authority[str(path)] = actual
    provider = Background("heavy")
    for family in result["families"]:
        name = family["family"]
        check(name + "/profile_integrity", digest(family["profile"]) == family["sha256"])
        profile = load(family["profile"])
        check(name + "/original_grid", np.array_equal(profile["points"], provider.efold[profile["indices"]]))
        for label, value in family["checks"].items():
            check(name + "/" + label, math.isfinite(value) and 0 <= value < ALGEBRA, value)
        for label in ("native_continuum_derivative", "hlog", "mu_rate", "amplitude_rate"):
            value = family["diagnostics"][label]
            check(name + "/" + label, math.isfinite(value) and 0 <= value < GATE, value)
        check(name + "/harmonic_degree", family["diagnostics"]["highest_harmonics"] == [6, 10, 14, 18])
        truncations = family["diagnostics"]["truncations"]
        for label in ("instantaneous_hessian", "mean_hessian", "mean_source", "mean_constraint"):
            check(name + "/" + label + "_order2", 0 <= truncations[2][label] < GATE)
        check(name + "/order_refinement", truncations[2]["mean_hessian"] < truncations[1]["mean_hessian"] < truncations[0]["mean_hessian"] and truncations[3]["mean_hessian"] < truncations[2]["mean_hessian"])
        packet_path = SECOND / "runs-second" / name / "G192-full-fine.npz"
        with np.load(packet_path) as archive:
            indices = profile["indices"]
            meta, scale_value, hubble, phase = [archive[key][indices] for key in ("metadata", "a", "H", "carrier_phase")]
        wave = family["wave"]
        original, mean, cosine, sine = phase_background(provider, profile["points"])
        polynomial = constraint_polynomial(mean, wave, profile["units"])
        analytic = evaluate(polynomial, phase)
        source_row = np.zeros((len(indices), 8))
        density_row = np.zeros_like(source_row)
        source_row[:, 0] = meta[:, 5]
        density_row[:, 0] = (scale_value * meta[:, 8])**2 * meta[:, 4]
        density_row[:, 1] = meta[:, 5] / scale_value**2
        carrier = scale_value * np.sqrt(scale_value * meta[:, 18])
        displacement = np.column_stack([np.cos(phase), np.sin(phase)]) / carrier[:, None]
        velocity = carrier[:, None] * np.column_stack([-np.sin(phase), np.cos(phase)]) / scale_value[:, None]**2
        source_row[:, 2:4] = meta[:, 15, None] * displacement
        density_row[:, 2:4] = meta[:, 15, None] * velocity + ((scale_value * meta[:, 18])**2 * meta[:, 14])[:, None] * displacement
        native = np.zeros((len(indices), 2, 8))
        native[:, 0] = 1.5 * hubble[:, None] * source_row + density_row / 2
        native[:, 0, 5] += 3 * hubble / scale_value**2
        native[:, 0, 6] += wave**2
        native[:, 0, 7] -= hubble / (2 * scale_value**2)
        native[:, 1, 5] = 1 / scale_value**2
        native *= profile["units"][:, None]
        constraint_error = sup(analytic - native) / norm(native)
        check(name + "/independent_native_constraint_rows", constraint_error < ALGEBRA, constraint_error)
    expected = {(family["model"] + "-" + family["label"], case["tag"]): case for family in read(SECOND / "prediction-result.json")["reports"] for case in family["cases"]}
    actual = {(row["family"], row["tag"]): row for row in result["histories"]}
    check("history_coverage", len(actual) == len(result["histories"]) == 42 and set(actual) == set(expected))
    for key, row in actual.items():
        guard()
        name = "/".join(key)
        check(name + "/input_integrity", row["sha256"] == expected[key]["sha256"] and digest(row["input"]) == row["sha256"])
        check(name + "/record", read(ROOT / "records" / (row["family"] + "-" + row["tag"] + ".json")) == row)
        for label, value in row["checks"].items():
            check(name + "/" + label, math.isfinite(value) and 0 <= value < ALGEBRA, value)
        check(name + "/passed", row["passed"] and row["diagnostics"]["candidate_qualified"])
        if key[0].startswith("heavy"):
            errors = row["diagnostics"]["force_truncation_errors"]
            check(name + "/orders", [entry["order"] for entry in errors] == [0, 1, 2, 3])
            check(name + "/order2_force_gate", errors[2]["maximum"] < GATE)
            check(name + "/force_refinement", errors[3]["maximum"] <= errors[2]["maximum"] <= errors[1]["maximum"] <= errors[0]["maximum"])
            if key[1].endswith("-zero"):
                check(name + "/zero_control", all(entry["maximum"] == 0 for entry in errors))
        else:
            check(name + "/cold_identity", row["diagnostics"]["identity"])
    check("bounds_complete", bounds["passed"] and bounds["order"] == 2 and len(bounds["reports"]) == 3)
    for row in bounds["reports"]:
        name = row["family"] + "/bound"
        check(name + "/integrity", digest(row["profile"]) == row["sha256"])
        check(name + "/scope", row["phase_uniform"] and row["sampled_times"] == 65)
        for label, passed in row["checks"].items():
            check(name + "/" + label, passed)
        for label, value in row["relative_bounds"].items():
            check(name + "/" + label + "_gate", value < GATE, value)
    with (ROOT / "summary.csv").open(newline="", encoding="utf-8") as stream:
        rows = list(csv.DictReader(stream))
    check("csv", len(rows) == 42 and all(None not in row for row in rows))
    compiled = {}
    for path in ROOT.glob("*.py"):
        compile(path.read_text(), str(path), "exec")
        compiled[str(path)] = digest(path)
        check("compile/" + path.name, True)
    check("no_bytecode", not list(ROOT.rglob("__pycache__")))
    coverage = BRIDGE / "final-stable-real-batch-rays037-038/common-coverage.json"
    check("scattering_untouched", digest(coverage) == "95d628bbe34ddc317e1d954d8e556271d666645e259f0eda66245be0607a0db3")
    check_parent()
    passed = all(item["passed"] for item in checks)
    write(ROOT / "validation.json", dict(passed=passed, count=len(checks), checks=checks, authority_sources=authority,
          compiled_sources=compiled, result_sha256=digest(ROOT / "result.json"), bounds_sha256=digest(ROOT / "remainder-bounds.json"),
          csv_sha256=digest(ROOT / "summary.csv")))
    print("Validation", passed, len(checks), flush=True)
    for item in checks:
        if not item["passed"]:
            print("FAIL", item, flush=True)
    require(passed, "validation failed; inspect")


if __name__ == "__main__":
    main()
