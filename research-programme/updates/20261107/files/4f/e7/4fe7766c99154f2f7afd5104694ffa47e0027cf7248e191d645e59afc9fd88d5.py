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
    require(LABEL == "summary", "combined validation only")
    parent = check_parent()
    check("balanced parent qualified", parent["corrected_forward_qualified"])
    physical, errors = retained_observables()
    references = read(SECOND / "prediction-result.json")["reports"]
    outcomes = []
    condensed = []
    for label in ("half", "double"):
        directory = STAGE / label
        for filename in ("frozen-inputs.json", "channel-inputs.json", "evolution-inputs.json"):
            data = read(directory / filename)
            for path, expected in data["sources"].items():
                check(label + ":" + filename + ":" + path, Path(path).is_file() and digest(path) == expected)
            check(label + ":" + filename + ":numerical", data["numerical"] == GATE)
            check(label + ":" + filename + ":algebra", data["algebra"] == ALGEBRA)
        for attempt in ("assemble-01", "channel-01", "evolution-01"):
            start, end = read(directory / (attempt + ".start.json")), read(directory / (attempt + ".end.json"))
            check(label + ":" + attempt + ":identity", all(start[key] == end[key] for key in start))
            check(label + ":" + attempt + ":exit", end["exit_code"] == 0)
            check(label + ":" + attempt + ":source", digest(end["source_path"]) == end["source_sha256"])
            check(label + ":" + attempt + ":chronology", datetime.fromisoformat(end["finished"]) >= datetime.fromisoformat(start["created"]))
        assembly = read(directory / "assembly-result.json")
        channel = read(directory / "channel-result.json")
        exact = read(directory / "exact-map-input.json")
        check(label + ":exact map unchanged", digest(exact["path"]) == exact["sha256"])
        check(label + ":factor integrity", digest(directory / "coupled-factors.npz") == assembly["packet_sha256"])
        check(label + ":quintic same-grid", assembly["interpolation_order"] == 5 and assembly["points"] == 24685)
        check(label + ":probe counts", assembly["independent_probes"] == 97 and channel["probes"] == 33)
        check(label + ":native massless regime", assembly["native_signature"][12] == (0 if label == "half" else 1))
        check(label + ":native hierarchy", assembly["native_signature"][40] == (40 if label == "half" else 16))
        check(label + ":sampled inverse", 0 < assembly["maximum_native_normalized_U"] < 1)
        for group, checks in (("assembly", assembly["checks"]), ("channel", channel["checks"])):
            for name, value in checks.items():
                check(label + ":" + group + ":" + name, np.isfinite(value) and 0 <= value < GATE)
        for name, value in assembly["algebra"].items():
            check(label + ":algebra:" + name, np.isfinite(value) and 0 <= value < ALGEBRA)
        config = read(directory / "evolution-inputs.json")
        check(label + ":frozen evolution", config["rtol"] == 2e-12 and config["atol"] == 2e-14
              and config["maximum_ell"] == 192 and not config["future_perturbation_sources"])
        result = read(directory / "evolution-result.json")
        check(label + ":five completed solves", result["state"] == "complete" and result["new_evolutions"] == 5 and result["tested_label"] == label)
        check(label + ":scope", result["original_mean_failure_preserved"] and result["exact_case_is_coordinate_control"]
              and result["corrected_case_has_explicit_generator_remainder"])
        family_outcomes = []
        for family in result["reports"]:
            model, wave = family["model"], family["wave"]
            check(label + ":" + model + ":current-state source", family["independent_forward"] and not family["future_sources_used"])
            reference = next(row for row in references if row["model"] == model and row["label"] == label)
            reference_case = next(row for row in reference["cases"] if row["tag"] == "G192-full-fine")
            path = SECOND / "runs-second" / (model + "-" + label) / reference_case["file"]
            check(label + ":" + model + ":reference unchanged", digest(path) == reference_case["sha256"])
            packets = {"native": load(path)}
            case_outcomes = []
            check(label + ":" + model + ":cases", {row["case"] for row in family["rows"]} ==
                  ({"full", "exact", "corrected"} if model == "heavy" else {"full", "corrected"}))
            for row in family["rows"]:
                guard()
                case = row["case"]
                prefix = label + ":" + model + ":" + case
                check(prefix + ":packet integrity", digest(row["packet"]) == row["sha256"])
                packet = load(row["packet"])
                packets[case] = packet
                check(prefix + ":converged", row["status"]["success"])
                check(prefix + ":original grid", np.array_equal(packet["efold"], packets["native"]["efold"]))
                check(prefix + ":point count", len(packet["efold"]) == row["status"]["points"])
                for name, value in packet.items():
                    if np.issubdtype(value.dtype, np.number):
                        check(prefix + ":" + name + " finite", np.isfinite(value).all())
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
                    check(prefix + ":" + name + " reproduced", close(value, row["constraints"][name]))
                passed = max(constraints.values()) < GATE
                check(prefix + ":constraint decision", passed == row["constraints_passed"])
                check(prefix + ":actual shear", close(sigma_kin, packet["sigma_kinematic"]))
                check(prefix + ":remainder", close(float(np.max(packet["remainder"])), row["maximum_generator_remainder"]))
                case_outcomes.append(passed)
            values = {name: physical(packet, wave) for name, packet in packets.items()}
            comparison_outcomes = []
            for comparison in family["comparisons"]:
                left, right = comparison["left"], comparison["right"]
                prefix = label + ":" + model + ":" + left + "/" + right
                found = [float(np.max(errors(packets[left]["projected_state"], packets[right]["projected_state"])))]
                check(prefix + ":state", close(found[0], comparison["state_error"]))
                for name, expected in comparison["physical_errors"].items():
                    value = float(errors(values[left][name], values[right][name]))
                    check(prefix + ":" + name, close(value, expected))
                    found.append(value)
                passed = max(found) < GATE
                check(prefix + ":decision", passed == comparison["passed"])
                comparison_outcomes.append(passed)
            if model == "cold":
                check(label + ":cold exact identity", np.array_equal(packets["full"]["evolved_state"], packets["corrected"]["evolved_state"]))
                check(label + ":cold zero corrector", family["maximum_encountered_U"] == 0)
            else:
                check(label + ":runtime inverse", 0 < family["maximum_encountered_U"] < 1)
                check(label + ":generator identity", family["generator_identity_error"] < ALGEBRA)
            passed = all(case_outcomes + comparison_outcomes)
            check(label + ":" + model + ":overall", passed == family["all_passed"])
            family_outcomes.append(passed)
            condensed.append(dict(label=label, model=model, passed=passed, comparisons=family["comparisons"],
                                  constraints={row["case"]: row["constraints"] for row in family["rows"]}))
            del packets, values
        check(label + ":scientific outcome", all(family_outcomes) == result["passed"])
        outcomes.append(result["passed"])
    for path in STAGE.glob("*.py"):
        compile(path.read_text(encoding="utf-8"), str(path), "exec")
        check("syntax:" + path.name, True)
    check("no bytecode", not any(STAGE.rglob("__pycache__")))
    check("scattering unchanged", digest(BRIDGE / "final-stable-real-batch-rays037-038/common-coverage.json") ==
          "95d628bbe34ddc317e1d954d8e556271d666645e259f0eda66245be0607a0db3")
    check_parent()
    failed = [row["name"] for row in CHECKS if not row["passed"]]
    write(ROOT / "validation.json", dict(passed=not failed, count=len(CHECKS), checks=CHECKS, failed=failed,
          both_new_wavelengths_qualified=all(outcomes), balanced_parent_qualified=True, new_evolutions=10,
          parent_closeout_sha256=PARENT_SEAL,
          evidence_hashes={str(STAGE / label / name): digest(STAGE / label / name)
                           for label in ("half", "double") for name in ("assembly-result.json", "channel-result.json", "evolution-result.json")}))
    write(ROOT / "comparison-summary.json", dict(all_three_wavelengths_qualified=all(outcomes),
          balanced_parent=str(CORRECTOR / "evolution-result.json"), additional_results=condensed,
          scope="retained same-background linear regimes; not a uniform Newtonian limiting theorem"))
    print("Validation checks", len(CHECKS), "failures", failed, "new wavelengths qualified", all(outcomes), flush=True)
    require(not failed, "validation failed; preserve and inspect")


if __name__ == "__main__":
    main()

