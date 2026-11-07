from common import *
import numpy as np


def main():
    modest()
    check_parent()
    require(LABEL == "summary", "aggregate only")
    checks = []
    def check(name, passed, detail=None):
        checks.append(dict(name=name, passed=bool(passed), detail=detail))
    controls = {}
    comparisons = []
    evidence = {}
    for family in ("half", "double"):
        root = STAGE / family
        expected_wave = dict(read(WAVELENGTH / "inventory-config.json")["waves"])[family]
        evidence_paths = ["evolution-result.json", "evolution-validation.json", "build-result.json",
                          "response-v2/adjoint-result.json", "response-v2/validation.json",
                          "primitive/primitive-result.json", "primitive/validation.json", "volume/volume-result.json"]
        records = {}
        for name in evidence_paths:
            path = root / name
            row = read(path)
            check(family + ":stage:" + name, row["passed"])
            evidence[str(path)] = digest(path)
            records[name] = row
        for name in ("preflight-v2/frozen-inputs.json", "evolution-v2-inputs.json", "frozen-inputs.json",
                     "response-v2/adjoint-inputs.json", "primitive/frozen-inputs.json"):
            for path, expected in read(root / name)["sources"].items():
                check(family + ":frozen:" + name + ":" + path, digest(path) == expected)
        for name in ("evolution-validation.json", "response-v2/validation.json", "primitive/validation.json"):
            check(family + ":all-rows:" + name, all(item["passed"] for item in records[name]["checks"]))
        check(family + ":volume-rows", all(item["passed"] for item in records["volume/volume-result.json"]["checks"]))
        evolution = records["evolution-result.json"]
        adjoint = records["response-v2/adjoint-result.json"]
        primitive = records["primitive/primitive-result.json"]
        check(family + ":solve-count", sum(len(item["rows"]) for item in evolution["reports"]) == 6 and adjoint["new_backward_solves"] == 8 and adjoint["reused_backward_solves"] == 0 and primitive["new_ode_solves"] == 0)
        family_controls = []
        for model in ("heavy", "cold"):
            captures = []
            for folder in ("preflight-v2/contexts", "evolution-contexts-v2", "contexts", "adjoint-contexts-v2", "primitive-contexts"):
                path = root / folder / (model + "-" + family) / "capture-check.json"
                capture = read(path)
                captures.append(capture)
                evidence[str(path)] = digest(path)
                check(family + ":" + model + ":capture:" + folder, all(capture[name] for name in ("same_seed", "zero_unselected", "source_preserved", "exact_initial_rate", "exact_initial_observer")))
            signature = captures[0]["signature"]
            check(family + ":" + model + ":native-regime", signature[12] == (0 if family == "half" else 1) and signature[30] == 5 and signature[40] == (40 if family == "half" else 16))
            check(family + ":" + model + ":same-regime-every-phase", all(item["signature"] == signature for item in captures))
            build = next(item for item in records["build-result.json"]["reports"] if item["model"] == model)
            check(family + ":" + model + ":packing", build["packing"]["every_node_roundtrip"] and build["packing"]["exact_zero_only"])
            check(family + ":" + model + ":operator-hash", digest(build["packet"]) == build["sha256"])
            for chunk in build["chunks"]:
                check(family + ":" + model + ":chunk:" + str(chunk["start"]), digest(chunk["path"]) == chunk["sha256"])
            evolved = next(item for item in evolution["reports"] if item["model"] == model)
            gr = next(item for item in evolved["rows"] if item["branch"] == "gr")
            check(family + ":" + model + ":gr-control", gr["control_passed"])
            family_controls.append(dict(model=model, wave=expected_wave, core_size=build["core_size"], native_order=signature[40],
                                        massless_regime=signature[12], packing=build["packing"],
                                        gr_state_error=gr["control"]["state_error"], gr_physical_errors=gr["control"]["physical_errors"],
                                        operator_offnode_max=max(build["numerical"].values())))
            for row in evolved["rows"]:
                check(family + ":" + model + ":forward-hash:" + row["branch"], digest(row["packet"]) == row["sha256"])
                with np.load(row["packet"]) as packet:
                    check(family + ":" + model + ":actual-wave:" + row["branch"], float(packet["wave"]) == expected_wave)
            model_primitive = next(item for item in primitive["reports"] if item["model"] == model)
            for branch in model_primitive["branches"]:
                label = branch["branch"]
                check(family + ":" + model + ":primitive:" + label, branch["passed"])
                for case in branch["cases"]:
                    check(family + ":" + model + ":primitive-packet:" + label + ":" + case["tag"], digest(case["packet"]) == case["sha256"])
                model_adjoint = next(item for item in adjoint["reports"] if item["model"] == model)
                adjoint_branch = next(item for item in model_adjoint["reports"] if item["branch"] == label)
                for case in adjoint_branch["cases"]:
                    check(family + ":" + model + ":adjoint-packet:" + label + ":" + case["tag"], digest(case["packet"]) == case["sha256"])
                comparisons.append(dict(family=family, wave=expected_wave, model=model, branch=label,
                                        measured=branch["measured"], prediction=branch["prediction"], prediction_error=branch["prediction_error"],
                                        old_bound=branch["old_bound"], transformed_bound=branch["transformed_bound"],
                                        selected_bound=branch["selected_bound"], improvement_factor=branch["improvement_factor"],
                                        temporal_bound=branch["cases"][1]["temporal_bound"],
                                        quadrature_budget=branch["cases"][1]["quadrature_budget"],
                                        full_history_errors=next(item for item in evolved["rows"] if item["branch"] == label)["comparison"]["physical_errors"]))
        controls[family] = family_controls
    balanced = read(ORIGINAL_PRIMITIVE / "primitive-result.json")
    for model in balanced["reports"]:
        for branch in model["branches"]:
            comparisons.append(dict(family="balanced", wave=dict(read(WAVELENGTH / "inventory-config.json")["waves"])["balanced"],
                                    model=model["model"], branch=branch["branch"], measured=branch["measured"],
                                    prediction=branch["prediction"], prediction_error=branch["prediction_error"],
                                    old_bound=branch["old_bound"], transformed_bound=branch["transformed_bound"],
                                    selected_bound=branch["selected_bound"], improvement_factor=branch["improvement_factor"],
                                    temporal_bound=branch["cases"][1]["temporal_bound"],
                                    quadrature_budget=branch["cases"][1]["quadrature_budget"], reused_parent=True))
    check_parent()
    passed = all(row["passed"] for row in checks)
    write(ROOT / "comparison-summary.json", dict(passed=passed, controls=controls, comparisons=comparisons,
          prospective_new_waves=["half", "double"], new_forward_solves=12, new_adjoint_solves=16,
          balanced_reused=True, no_fit_or_physical_parameter_change=True, numerical_terminal_scope=True,
          uniform_limit_theorem_claimed=False, evidence_hashes=evidence))
    write(ROOT / "validation.json", dict(passed=passed, count=len(checks), checks=checks, evidence_hashes=evidence))
    print("two new wavenumbers", "aggregate checks", len(checks), "passed", passed, flush=True)
    for row in checks:
        if not row["passed"]:
            print(row, flush=True)
    require(passed, "aggregate evidence failure")

if __name__ == "__main__":
    main()

