from common import *
from forward import retained_observables, ratios
import numpy as np

CHECKS = []


def check(name, condition):
    CHECKS.append(dict(name=name, passed=bool(condition)))


def close(left, right):
    return bool(np.allclose(left, right, rtol=1e-11, atol=1e-24))


def main():
    modest()
    parent = check_parent()
    check("parent seal and all artifacts", parent["state"] == "verified_closed")
    for filename in ("preflight-inputs.json", "preflight-v2-inputs.json", "coefficient-inputs.json", "forward-inputs.json"):
        packet = read(ROOT / filename)
        for path, expected in packet["sources"].items():
            check(filename + ":" + path, Path(path).is_file() and digest(path) == expected)
        check(filename + ":fixed numerical gate", packet["numerical"] == GATE)
        if "algebra" in packet:
            check(filename + ":fixed algebra gate", packet["algebra"] == ALGEBRA)
    attempts = ("preflight-01", "preflight-v2-01", "coefficients-01", "forward-01", "diagnostic-01")
    for label in attempts:
        start = read(ROOT / (label + ".start.json"))
        end = read(ROOT / (label + ".end.json"))
        check(label + ":matching worker", all(start[key] == end[key] for key in start))
        check(label + ":exit", end["exit_code"] == (1 if label == "preflight-01" else 0))
        check(label + ":chronology", datetime.fromisoformat(end["finished"]) >= datetime.fromisoformat(start["created"]))
    check("first rejected adapter retained", "unowned approximation or thermal perturbation" in (ROOT / "preflight-01.stderr.log").read_text())
    check("regime repair documented", (ROOT / "REGIME-REPAIR.md").is_file())

    preflight = read(ROOT / "preflight-v2-result.json")
    check("six native families", {(row["model"], row["label"]) for row in preflight["reports"]} ==
          {(model, label) for model in ("heavy", "cold") for label in ("half", "balanced", "double")})
    for row in preflight["reports"]:
        family = row["model"] + "-" + row["label"]
        directory = "native-contexts" if family == "heavy-half" else "native-contexts-v2"
        check(family + ":owned receipt", read(ROOT / directory / family / "feedback-check.json") == row)
        for name, value in row["checks"].items():
            check(family + ":" + name, np.isfinite(value) and 0 <= value < ALGEBRA)
        check(family + ":G192 and probes", row["retained_order"] == 192 and row["probes"] == 17)
    check("no new native compilation or future forcing", not preflight["compiled_native_code"] and not preflight["future_sources_used"])

    coefficients = read(ROOT / "coefficient-result.json")
    coefficient_path = ROOT / "heavy-balanced-coefficients.npz"
    check("coefficient packet intact", digest(coefficient_path) == coefficients["sha256"])
    check("coefficient probe count", coefficients["probes"] == 97 and coefficients["points"] == 24685)
    check("background-only construction", coefficients["future_perturbations_used"] is False)
    for label in ("checks", "refinement"):
        for name, value in coefficients[label].items():
            check("coefficients:" + label + ":" + name, np.isfinite(value) and 0 <= value < GATE)
    candidate = load(coefficient_path)
    operators = load(TIMECHAIN / "operators/balanced.npz")
    check("original coefficient grid", np.array_equal(candidate["efold"], operators["efold"]))
    del candidate, operators

    result = read(ROOT / "forward-result.json")
    configuration = read(ROOT / "forward-inputs.json")
    check("unchanged G192 solver controls", configuration["rtol"] == 2e-12 and configuration["atol"] == 2e-14
          and configuration["maximum_ell"] == 192 and configuration["galerkin"])
    check("overall mean failure remains recorded", result["passed"] is False and result["state"] == "complete")
    check("current-state prospective scope", result["current_state_rest_feedback"] and result["no_future_sources"]
          and result["prospective_equations"] and not result["further_wavelengths_started"])
    physical, errors = retained_observables()
    original_reports = read(SECOND / "prediction-result.json")["reports"]
    for report in result["reports"]:
        model, wave = report["model"], report["wave"]
        original = next(row for row in original_reports if row["model"] == model and row["label"] == "balanced")
        original_case = next(row for row in original["cases"] if row["tag"] == "G192-full-fine")
        path = SECOND / "runs-second" / (model + "-balanced") / original_case["file"]
        check(model + ":original unchanged", digest(path) == original_case["sha256"])
        packets = {"native": load(path)}
        check(model + ":current-state source declaration", report["future_sources_used"] is False and report["independent_forward"])
        for row in report["rows"]:
            guard()
            case = row["case"]
            check(model + "-" + case + ":packet integrity", digest(row["packet"]) == row["sha256"])
            packet = load(row["packet"])
            packets[case] = packet
            check(model + "-" + case + ":convergence", row["status"]["success"] and len(packet["efold"]) == row["status"]["points"])
            check(model + "-" + case + ":original grid", np.array_equal(packet["efold"], packets["native"]["efold"]))
            for name, value in packet.items():
                if np.issubdtype(value.dtype, np.number):
                    check(model + "-" + case + ":" + name + " finite", np.isfinite(value).all())
            state, rates = packet["canonical_state"], packet["canonical_state_rate"]
            terms, hubble, scale = packet["terms"], packet["H"], packet["a"]
            geometry = packet["canonical_geometry"]
            z_kin = hubble * rates[:, 4] / (2 * wave)
            eta_kin = hubble * rates[:, 6]
            sigma_kin = z_kin + 3 * eta_kin / wave
            values = dict(
                Hamiltonian_canonical=ratios([wave**2 * state[:, 6], -hubble * wave * geometry[:, 0], terms[:, :, 0].sum(axis=1) / 2]),
                momentum_canonical=ratios([state[:, 5] / scale**2, -terms[:, :5, 1].sum(axis=1) / (2 * wave)]),
                Hamiltonian_kinematic=ratios([wave**2 * state[:, 6], -hubble * wave * z_kin, terms[:, :, 0].sum(axis=1) / 2]),
                momentum_kinematic=ratios([eta_kin, -terms[:, :, 1].sum(axis=1) / (2 * wave)]))
            for name, value in values.items():
                check(model + "-" + case + ":recomputed " + name, close(value, row["constraints"][name]))
            check(model + "-" + case + ":derived shear", close(sigma_kin, packet["sigma_kinematic"]))
            expected = model == "cold" or case == "full"
            check(model + "-" + case + ":constraint outcome preserved", row["constraints_passed"] == expected)
            check(model + "-" + case + ":constraint outcome reproduced", (max(values.values()) < GATE) == expected)
        physical_packets = {name: physical(packet, wave) for name, packet in packets.items()}
        for comparison in report["comparisons"]:
            left, right = comparison["left"], comparison["right"]
            state_error = float(np.max(errors(packets[left]["projected_state"], packets[right]["projected_state"])))
            check(model + ":" + left + "/" + right + " state error", close(state_error, comparison["state_error"]))
            actual = [state_error]
            for name, value in comparison["physical_errors"].items():
                found = float(errors(physical_packets[left][name], physical_packets[right][name]))
                check(model + ":" + left + "/" + right + ":" + name, close(found, value))
                actual.append(found)
            check(model + ":" + left + "/" + right + " outcome", (max(actual) < GATE) == comparison["passed"])
        if model == "cold":
            check("cold exact full/mean state identity", np.array_equal(packets["full"]["evolved_state"], packets["mean"]["evolved_state"]))
        del packets, physical_packets

    diagnostic = read(ROOT / "projection-diagnostic.json")
    for path, expected in diagnostic["source_hashes"].items():
        check("diagnostic source:" + path, Path(path).is_file() and digest(path) == expected)
    for name, value in diagnostic["checks"].items():
        check("diagnostic:" + name, np.isfinite(value) and 0 <= value < ALGEBRA)
    heavy = next(report for report in result["reports"] if report["model"] == "heavy")
    mean_row = next(row for row in heavy["rows"] if row["case"] == "mean")
    momentum = diagnostic["momentum"]
    check("diagnostic same forward failure", close(momentum["measured_momentum_residual"], mean_row["constraints"]["momentum_kinematic"]))
    check("localized action contribution", abs(momentum["measured_momentum_residual"] - momentum["action_part"]) < ALGEBRA
          and momentum["source_part"] < ALGEBRA and momentum["inherited_canonical_part"] < ALGEBRA)
    check("no repaired trajectory claimed", not diagnostic["corrective_rates_overwritten"] and not diagnostic["new_trajectory_claimed"])
    primitive = load(ROOT / "next-coupled-corrector-native-phase.npz")
    check("corrector original 65 samples", len(primitive["efold"]) == 65)
    for name, value in primitive.items():
        check("corrector:" + name + " finite", np.isfinite(value).all())

    for path in ROOT.glob("*.py"):
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
        check("syntax:" + path.name, True)
    coverage = BRIDGE / "final-stable-real-batch-rays037-038/common-coverage.json"
    check("scattering coverage untouched", digest(coverage) == "95d628bbe34ddc317e1d954d8e556271d666645e259f0eda66245be0607a0db3")
    check("no generated bytecode", not any(ROOT.rglob("__pycache__")))
    check_parent()
    failed = [row["name"] for row in CHECKS if not row["passed"]]
    write(ROOT / "validation.json", dict(passed=not failed, checks=CHECKS, count=len(CHECKS), failed=failed,
          scope="source integrity, retained numerical outcome reproduction, diagnosed failure preserved; not mean-model qualification",
          full_coupled_controls_pass=True, mean_forward_qualified=False, new_forward_solves=4,
          parent_closeout_sha256=PARENT_SEAL))
    print("Validation checks", len(CHECKS), "failures", failed, flush=True)
    require(not failed, "validation failure; inspect, no automatic rerun")


if __name__ == "__main__":
    main()

