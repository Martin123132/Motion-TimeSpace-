import argparse
import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as numerical
    from annular_coordinate_evolution_operator_20260909 import AnnularFields
    from annular_compatible_current_time_jets_20260909 import CompatibleCurrentTimeJets
    from annular_coupled_current_time_jets_20260909 import CoupledCurrentTimeJets
    from annular_coupled_curvature_transfer_20260909 import transform_mixed
    from annular_current_corner_compatibility_20260909 import continuous_operator
    from annular_current_normal_reconstruction_20260909 import POWERS, construct_system, evaluate_hermite, hermite_coefficients, matrix_product, physical_mixed, solve_jets, system_residuals
    from annular_curvature_timejet_transfer_20260909 import along_segment, background_fields, geometry, radius_field

    root = Path(__file__).resolve().parents[1]
    intake = root / "source-intake/navier-stokes/20260909"
    parser = argparse.ArgumentParser()
    parser.add_argument("--branch", choices=["candidate", "baseline"], default="candidate")
    arguments = parser.parse_args()
    engine_class = CompatibleCurrentTimeJets if arguments.branch == "candidate" else CoupledCurrentTimeJets
    destination = intake / ("annular-compatible-smoke-normal-" + arguments.branch)
    destination.mkdir(exist_ok=False)
    source = Path(__file__).read_bytes()
    (destination / "executed-script.py").write_bytes(source)
    report = {"state": "running", "started_utc": datetime.now(timezone.utc).isoformat(), "script_sha256": hashlib.sha256(source).hexdigest(), "inputs": {}, "checks": [], "runs": [], "sensitivity": [], "valid_for_physics_claim": False, "scope": "Existing derived noncharacteristic radial normal form using branch-correct actual compatible or projected-baseline time jets at N32/64/128, numerical sources and nonzero discrete mass constraint. Piecewise C3 septic Hermite realization; intercell defects and overdetermined mass transport are retained. No continuum/source-bound or characteristic-horizon extension claim.", "completion": "Mixed orders above total3 are set to zero only to define a C3 spacetime Hermite representative; not claims about the solution's higher derivatives.", "sensitivity_gate": "Unchanged10% larger-correction-norm+1e-25 for Z AND K1 on every nodal row; additionally test every quarter/mid/three-quarter cell point. No deletion of original failures."}

    def save():
        (destination / "status.json").write_text(json.dumps(report, indent=2) + "\n")

    def own(path):
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        report["inputs"][str(path.relative_to(root))] = digest
        return digest

    def verify(name, condition, detail=None):
        report["checks"].append({"name": name, "passed": bool(condition), "detail": detail})
        save()
        print(name + ": " + str(bool(condition)), flush=True)

    def maximum(value):
        return float(numerical.max(numerical.abs(value)))

    save()
    try:
        folder = intake / ("annular-compatible-current-time-jets-trajectory" if arguments.branch == "candidate" else "annular-compatible-baseline-time-jets")
        own(folder / "status.json")
        owner = json.loads((folder / "status.json").read_text())
        verify("time_jet_owner_passed", owner["state"] == "complete" and owner["passed"] == owner["total"] and (folder / "COMPLETE").exists())
        verify("time_jet_owner_snapshot", own(folder / "executed-script.py") == owner["script_sha256"])
        verify("time_jet_inputs_unchanged", all(own(root / name) == digest for name, digest in owner["inputs"].items()))
        old_folder = intake / "annular-coupled-current-curvature-transfer"
        own(old_folder / "status.json")
        old = json.loads((old_folder / "status.json").read_text())
        verify("all_four_old_curvature_failures_preserved", not old["all_curvature_sensitivity_gates_passed"] and len(old["sensitivity"]) == 4 and all(not row["curvature_sensitivity_gate_passed"] for row in old["sensitivity"]))
        for name in ["derive_annular_compatible_smoke_normal_reconstruction_20260909.py", "annular_compatible_current_time_jets_20260909.py", "annular_coupled_current_time_jets_20260909.py", "annular_raw_volterra_time_jets_20260909.py", "derive_annular_raw_volterra_C3_normal_reconstruction_20260909.py", "annular_projected_volterra_time_jets_20260909.py", "derive_annular_projected_volterra_normal_reconstruction_20260909.py", "annular_current_normal_reconstruction_20260909.py", "derive_annular_current_normal_reconstruction_20260909.py", "annular_coupled_curvature_transfer_20260909.py", "annular_curvature_timejet_transfer_20260909.py", "annular_current_corner_compatibility_20260909.py"]:
            own(root / "scripts" / name)
        stored = {}
        for case_name in ["canonical", "nonlinear_modulated"]:
            path = intake / "annular-constraint-correction-initial" / (case_name + ".json")
            own(path)
            evaluator = AnnularFields(json.loads(path.read_text()))
            for entry in owner["runs"]:
                if entry["case"] != case_name:
                    continue
                path = folder / entry["artifact"]
                label = path.stem
                verify(label + "_time_artifact_hash", own(path) == entry["sha256"])
                with numerical.load(path, allow_pickle=False) as arrays:
                    radii, time_derivatives, source_coefficients = [arrays[key] for key in ["radius", "current_time_derivatives", "numerical_source_time_coefficients"]]
                engine = engine_class(evaluator, radii, entry["time"])
                fractions = numerical.array([0.25, 0.5, 0.75])
                subradii = (radii[:-1, None] + engine.spacing * fractions).ravel()
                backgrounds = {"nodes": background_fields(evaluator, entry["time"], radii), "subcells": background_fields(evaluator, entry["time"], subradii)}
                snapshot = evaluator.evaluate(numerical.full_like(subradii, entry["time"]), subradii, 0.1)
                zero, principal, defect, current, unused_data, unused_derivative = continuous_operator(snapshot, subradii, evaluator)
                source_extension = ((1 - fractions) * source_coefficients[0, :, :-1, None] + fractions * source_coefficients[0, :, 1:, None]).reshape(5, -1)
                for method in ["poly7", "poly9"]:
                    tag = label + "_" + method
                    system = construct_system(engine, time_derivatives, source_coefficients, method)
                    verify(tag + "_normal_determinant", maximum(system["determinant"] - system["expected_determinant"]) < 1e-10 * maximum(system["expected_determinant"]), {"condition_max": maximum(system["condition"]), "minimum_abs_determinant": float(numerical.min(numerical.abs(system["determinant"])))})
                    values = solve_jets(system, time_derivatives)
                    normal_residual, mass_residual = system_residuals(system, values)
                    normal_max = max(maximum(value) for value in normal_residual.values())
                    scale = max(maximum(value) for value in system["f"].values()) + max(maximum(value) for value in values.values())
                    verify(tag + "_normal_form_recurrence", normal_max < 1e-9 * scale + 1e-22, {"residual_max": normal_max, "scale": scale})
                    verify(tag + "_saved_time_jets_unchanged", all(maximum(values[degree, 0] - time_derivatives[degree] / math.factorial(degree)) == 0 for degree in range(4)))
                    verify(tag + "_kinematic_spatial_recurrence", all(maximum((radial_order + 1) * values[time_order, radial_order + 1][0] - values[time_order, radial_order][1]) < 1e-18 for time_order, radial_order in POWERS))
                    measured_constraint = values[0, 1][3] - numerical.sum(engine.current["constraint_gradient"][0] * values[0, 0], axis=0)
                    verify(tag + "_nonzero_constraint_retained", maximum(measured_constraint - system["constraint"][0, 0]) < 1e-18 and maximum(system["constraint"][0, 0]) > 0)
                    if entry["intervals"] == 32 and entry["time"] == 0.1:
                        target = {(time_order, radial_order): numerical.stack([(component + 1) * (radii / 8)**(3 - time_order - radial_order) / (10**(time_order + radial_order + 3)) for component in range(5)]) for time_order in range(4) for radial_order in range(4 - time_order)}
                        synthetic = system.copy()
                        synthetic["f"] = {}
                        target_r = {power: (power[1] + 1) * target[power[0], power[1] + 1] for power in POWERS}
                        target_t = {power: (power[0] + 1) * target[power[0] + 1, power[1]] for power in POWERS}
                        for power in POWERS:
                            synthetic["f"][power] = matrix_product(system["M"], target_r, power) - matrix_product(system["A"], target, power) - matrix_product(system["B"], target_t, power)
                        recovered = solve_jets(synthetic, numerical.stack([math.factorial(degree) * target[degree, 0] for degree in range(4)]))
                        verify(tag + "_independent_prescribed_jet_inverse_control", max(maximum(recovered[key] - target[key]) for key in target) < 1e-12)
                    coefficients = hermite_coefficients(values, engine.spacing)
                    endpoint_radii, endpoint_mixed = evaluate_hermite(coefficients, radii, [0, 1])
                    endpoint_errors = {}
                    for power in values:
                        expected = math.factorial(power[0]) * math.factorial(power[1]) * values[power]
                        observed = endpoint_mixed[power].reshape(5, -1, 2)
                        endpoint_errors[str(power)] = max(maximum(observed[:, :, 0] - expected[:, :-1]), maximum(observed[:, :, 1] - expected[:, 1:]))
                        verify(tag + "_C3_endpoint_" + str(power), endpoint_errors[str(power)] < 1e-7 * max(maximum(expected), 1e-20) + 1e-18)
                    positions, submixed = evaluate_hermite(coefficients, radii, fractions)
                    verify(tag + "_subcell_positions", maximum(positions - subradii) == 0)
                    required_source = submixed[1, 0] - numerical.einsum("ijn,jn->in", zero, submixed[0, 0]) - numerical.einsum("ijn,jn->in", principal, submixed[0, 1]) + defect
                    reconstruction_defect = required_source - source_extension
                    integrability = submixed[0, 1][0] - submixed[0, 0][1]
                    verify(tag + "_finite_retained_reconstruction_defects", numerical.all(numerical.isfinite(reconstruction_defect)) and numerical.all(numerical.isfinite(integrability)) and all(numerical.all(numerical.isfinite(value)) for value in mass_residual.values()))
                    saved = {"radius": radii, "subcell_radius": subradii, "Hermite_coefficients": coefficients, "original_numerical_source_coefficients": source_coefficients, "subcell_declared_linear_source_extension": source_extension, "subcell_required_source": required_source, "subcell_reconstruction_defect": reconstruction_defect, "subcell_integrability_defect": integrability, "retained_mass_constraint": system["constraint"][0, 0]}
                    metrics = {"normal_matrix_condition_max": maximum(system["condition"]), "mass_time_compatibility_residual_coefficients": {str(power): maximum(value) for power, value in mass_residual.items()}, "endpoint_matching_errors": endpoint_errors, "subcell_PDE_defect_by_component": numerical.max(numerical.abs(reconstruction_defect), axis=-1).tolist(), "subcell_integrability_defect": maximum(integrability)}
                    for scope, locations, selected in [("nodes", radii, physical_mixed(values)), ("subcells", subradii, {power: value[[0, 3, 4]] for power, value in submixed.items()})]:
                        errors = transform_mixed(selected, locations, evaluator.sigma)
                        result = geometry(along_segment(backgrounds[scope], errors, 0), radius_field(locations), evaluator.constants, evaluator.kappa)
                        for quantity, proxy, residual in [("Z", "Zalg", "defect"), ("K1", "K1alg", "K1residual")]:
                            difference = (result[quantity] - result[proxy] - result[residual]).extract(1)
                            scale = max(maximum(result[quantity].extract(1)), maximum(result[proxy].extract(1)), 1e-30)
                            verify(tag + "_" + scope + "_offshell_" + quantity, maximum(difference) < 1e-9 * scale + 1e-25)
                        metrics[scope] = {key: maximum(result[key].extract(1)) for key in ["Z", "K1", "M1", "Weyl2", "Rm", "Dl", "Fchi"]}
                        for key in metrics[scope]:
                            saved[scope + "_" + key + "_variation"] = result[key].extract(1)
                    for power, value in values.items():
                        saved["normalized_current_jet_" + str(power)] = value
                    filename = tag + "_normal_curvature.npz"
                    numerical.savez(destination / filename, **saved)
                    report["runs"].append({"case": case_name, "time": entry["time"], "intervals": entry["intervals"], "method": method, "artifact": filename, "sha256": hashlib.sha256((destination / filename).read_bytes()).hexdigest(), "metrics": metrics, "valid_for_physics_claim": False})
                    stored[case_name, entry["time"], entry["intervals"], method] = saved
                    save()
        for case_name in ["canonical", "nonlinear_modulated"]:
            for time_value in [0.1, 0.3]:
                first, second = [stored[case_name, time_value, 128, method] for method in ["poly7", "poly9"]]
                row = {"case": case_name, "time": time_value, "scopes": {}, "refinement": {}}
                for scope in ["nodes", "subcells"]:
                    comparisons = {}
                    for quantity in ["Z", "K1"]:
                        key = scope + "_" + quantity + "_variation"
                        difference = maximum(first[key] - second[key])
                        scale = max(maximum(first[key]), maximum(second[key]), 1e-30)
                        comparisons[quantity] = {"difference": difference, "larger_correction_norm": scale, "relative_difference": difference / scale, "ten_percent_gate": difference <= 0.1 * scale + 1e-25}
                    row["scopes"][scope] = comparisons
                for method in ["poly7", "poly9"]:
                    for quantity in ["Z", "K1"]:
                        low, middle, high = [stored[case_name, time_value, intervals, method]["nodes_" + quantity + "_variation"] for intervals in [32, 64, 128]]
                        coarse, fine = maximum(low - middle[::2]), maximum(middle - high[::2])
                        row["refinement"][method + "_" + quantity] = {"coarse_difference": coarse, "fine_difference": fine, "ratio": coarse / max(fine, 1e-30)}
                row["all_nodal_and_subcell_sensitivity_gates_passed"] = all(values[quantity]["ten_percent_gate"] for values in row["scopes"].values() for quantity in ["Z", "K1"])
                row["continuum_bound_available"] = False
                report["sensitivity"].append(row)
        report["all_curvature_sensitivity_gates_passed"] = all(row["all_nodal_and_subcell_sensitivity_gates_passed"] for row in report["sensitivity"])
        verify("all24_reconstructions_saved", len(report["runs"]) == 24)
        for name in ["annular_current_normal_reconstruction_20260909.py", "derive_annular_current_normal_reconstruction_20260909.py"]:
            path = root / "scripts" / name
            compile(path.read_bytes(), str(path), "exec")
        verify("no_bytecode_cache", not (root / "scripts/__pycache__").exists())
        report.update(passed=sum(check["passed"] for check in report["checks"]), total=len(report["checks"]), completed_utc=datetime.now(timezone.utc).isoformat())
        report["state"] = "complete" if report["passed"] == report["total"] else "failed"
        save()
    except Exception as error:
        report.update(state="failed", failure=repr(error), completed_utc=datetime.now(timezone.utc).isoformat())
        save()
        raise
    print(json.dumps({key: report[key] for key in ["state", "passed", "total", "completed_utc", "all_curvature_sensitivity_gates_passed"]}), flush=True)
    if report["state"] != "complete":
        raise SystemExit(1)
    (destination / "COMPLETE").write_text(report["completed_utc"] + "\n")


if __name__ == "__main__":
    run()
