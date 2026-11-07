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
    seal = check_parent()
    check("previous scientific failure intact", seal["mean_forward_qualified"] is False)
    for filename in ("frozen-inputs.json", "representation-v2-inputs.json", "evolution-inputs.json"):
        data = read(ROOT / filename)
        for path, expected in data["sources"].items():
            check(filename + ":" + path, Path(path).is_file() and digest(path) == expected)
        check(filename + ":numerical gate", data["numerical"] == GATE)
        check(filename + ":algebra gate", data["algebra"] == ALGEBRA)
    for label, expected in (("assemble-01", 1), ("representation-v2-01", 0), ("evolution-01", 0)):
        start, end = read(ROOT / (label + ".start.json")), read(ROOT / (label + ".end.json"))
        check(label + ":identity", all(start[key] == end[key] for key in start))
        check(label + ":expected exit", end["exit_code"] == expected)
        check(label + ":chronology", datetime.fromisoformat(end["finished"]) >= datetime.fromisoformat(start["created"]))
    original = read(ROOT / "assembly-result.json")
    check("cubic failure retained", not original["passed"])
    check("cubic diagnosed failures only", {key for key, value in original["checks"].items() if value >= GATE} ==
          {"grid_derivative_U_A", "grid_derivative_U_B", "grid_derivative_U_C"})
    representation = read(ROOT / "representation-v2-result.json")
    check("factor bank retained", digest(ROOT / "coupled-factors.npz") == original["packet_sha256"] == representation["packet_sha256"])
    check("unchanged physical grid", not representation["grid_changed"] and representation["original_points"] == 24685)
    check("representation scope", representation["interpolation_order"] == 5 and representation["independent_probes"] == 97 and not representation["continuous_time_certificate"])
    for name, value in representation["checks"].items():
        check("representation:" + name, np.isfinite(value) and 0 <= value < GATE)
    for name, value in representation["algebra"].items():
        check("algebra:" + name, np.isfinite(value) and 0 <= value < ALGEBRA)
    check("sampled inverse bound", 0 < representation["maximum_sampled_U"] < 1
          and close(representation["sampled_inverse_bound"], 1 / (1 - representation["maximum_sampled_U"])))
    config = read(ROOT / "evolution-inputs.json")
    check("original evolution controls", config["rtol"] == 2e-12 and config["atol"] == 2e-14
          and config["maximum_ell"] == 192 and not config["future_perturbation_sources"])
    result = read(ROOT / "evolution-result.json")
    check("completed four solutions", result["state"] == "complete" and result["new_evolutions"] == 4)
    check("no expanded claim", result["exact_case_is_coordinate_control"] and result["corrected_case_has_explicit_generator_remainder"]
          and result["original_mean_failure_preserved"] and not result["new_wavelengths"])
    check("two matched models", {row["model"] for row in result["reports"]} == {"heavy", "cold"})
    physical, errors = retained_observables()
    parent_reports = read(SEALED / "forward-result.json")["reports"]
    family_outcomes = []
    for family in result["reports"]:
        model, wave = family["model"], family["wave"]
        check(model + ":scope", family["independent_forward"] and not family["future_sources_used"])
        parent_report = next(row for row in parent_reports if row["model"] == model)
        parent_case = next(row for row in parent_report["rows"] if row["case"] == "full")
        check(model + ":reference unchanged", digest(parent_case["packet"]) == parent_case["sha256"])
        packets = {"parent-full": load(parent_case["packet"])}
        case_outcomes = []
        for row in family["rows"]:
            guard()
            case = row["case"]
            check(model + "-" + case + ":integrity", digest(row["packet"]) == row["sha256"])
            packet = load(row["packet"])
            packets[case] = packet
            check(model + "-" + case + ":converged", row["status"]["success"])
            check(model + "-" + case + ":original grid", np.array_equal(packet["efold"], packets["parent-full"]["efold"]))
            check(model + "-" + case + ":point count", len(packet["efold"]) == row["status"]["points"])
            for name, value in packet.items():
                if np.issubdtype(value.dtype, np.number):
                    check(model + "-" + case + ":" + name + " finite", np.isfinite(value).all())
            state, rates, terms = packet["canonical_state"], packet["canonical_state_rate"], packet["terms"]
            hubble, scale_value, geometry = packet["H"], packet["a"], packet["canonical_geometry"]
            z_kin = hubble * rates[:, 4] / (2 * wave)
            eta_kin = hubble * rates[:, 6]
            sigma_kin = z_kin + 3 * eta_kin / wave
            constraints = dict(
                Hamiltonian_canonical=ratios([wave**2 * state[:, 6], -hubble * wave * geometry[:, 0], terms[:, :, 0].sum(axis=1) / 2]),
                momentum_canonical=ratios([state[:, 5] / scale_value**2, -terms[:, :5, 1].sum(axis=1) / (2 * wave)]),
                Hamiltonian_kinematic=ratios([wave**2 * state[:, 6], -hubble * wave * z_kin, terms[:, :, 0].sum(axis=1) / 2]),
                momentum_kinematic=ratios([eta_kin, -terms[:, :, 1].sum(axis=1) / (2 * wave)]),
                shear_velocity_difference=float(np.max(abs(sigma_kin - geometry[:, 1]))) / max(float(np.max(abs(geometry[:, 1]))), 1e-30))
            for name, value in constraints.items():
                check(model + "-" + case + ":" + name + " reproduced", close(value, row["constraints"][name]))
            passed = max(constraints.values()) < GATE
            check(model + "-" + case + ":constraint outcome preserved", passed == row["constraints_passed"])
            check(model + "-" + case + ":generator remainder preserved", close(float(np.max(packet["remainder"])), row["maximum_generator_remainder"]))
            check(model + "-" + case + ":actual shear preserved", close(sigma_kin, packet["sigma_kinematic"]))
            case_outcomes.append(passed)
        values = {name: physical(packet, wave) for name, packet in packets.items()}
        comparison_outcomes = []
        for comparison in family["comparisons"]:
            left, right = comparison["left"], comparison["right"]
            found = [float(np.max(errors(packets[left]["projected_state"], packets[right]["projected_state"])))]
            check(model + ":" + left + "/" + right + " state", close(found[0], comparison["state_error"]))
            for name, expected in comparison["physical_errors"].items():
                value = float(errors(values[left][name], values[right][name]))
                check(model + ":" + left + "/" + right + ":" + name, close(value, expected))
                found.append(value)
            passed = max(found) < GATE
            check(model + ":" + left + "/" + right + " outcome preserved", passed == comparison["passed"])
            comparison_outcomes.append(passed)
        if model == "cold":
            check("cold corrected exact identity", np.array_equal(packets["full"]["evolved_state"], packets["corrected"]["evolved_state"]))
            check("cold no phantom corrector", family["maximum_encountered_U"] == 0)
        else:
            check("heavy runtime inverse gate", 0 < family["maximum_encountered_U"] < 1)
            check("generator identity", family["generator_identity_error"] < ALGEBRA)
        family_passed = all(case_outcomes + comparison_outcomes)
        check(model + ":overall outcome", family_passed == family["all_passed"])
        family_outcomes.append(family_passed)
        del packets, values
    check("overall scientific outcome reproduced", all(family_outcomes) == result["passed"])
    for path in ROOT.glob("*.py"):
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
        check("syntax:" + path.name, True)
    check("no bytecode", not any(ROOT.rglob("__pycache__")))
    check("scattering coverage unchanged", digest(BRIDGE / "final-stable-real-batch-rays037-038/common-coverage.json") ==
          "95d628bbe34ddc317e1d954d8e556271d666645e259f0eda66245be0607a0db3")
    check_parent()
    failed = [row["name"] for row in CHECKS if not row["passed"]]
    write(ROOT / "validation.json", dict(passed=not failed, count=len(CHECKS), checks=CHECKS, failed=failed,
          corrected_forward_qualified=result["passed"], parent_mean_forward_qualified=False,
          scope="same-background balanced-wavelength forward test and retained integrity; no universal GR or data-fit claim",
          evolution_sha256=digest(ROOT / "evolution-result.json"), representation_sha256=digest(ROOT / "representation-v2-result.json"),
          parent_closeout_sha256=PARENT_SEAL))
    print("Validation", len(CHECKS), "failures", failed, "corrected forward qualified", result["passed"], flush=True)
    require(not failed, "validation failed; inspect")


if __name__ == "__main__":
    main()

