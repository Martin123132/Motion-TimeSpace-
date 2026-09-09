import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as numerical
    import sympy as symbolic
    from annular_analytic_corner_jets_20260909 import AnalyticCornerJets
    from annular_coordinate_evolution_operator_20260909 import AnnularFields
    from annular_continuum_initial_data_20260909 import constraint_gradients
    from annular_coupled_current_operator_20260909 import snapshot_coefficients
    from annular_current_corner_compatibility_20260909 import CornerCompatibility
    from annular_second_corner_initial_data_20260909 import family_lift as old_family_lift, profile_values as old_profiles
    from annular_third_corner_initial_data_20260909 import build_family, family_derivatives, initial_derivatives, lift, PROFILES

    root = Path(__file__).resolve().parents[1]
    intake = root / "source-intake/navier-stokes/20260909"
    destination = intake / "annular-analytic-third-corner-initial-data"
    destination.mkdir(exist_ok=False)
    source = Path(__file__).read_bytes()
    (destination / "executed-script.py").write_bytes(source)
    report = {"state": "running", "started_utc": datetime.now(timezone.utc).isoformat(), "script_sha256": hashlib.sha256(source).hexdigest(), "inputs": {}, "checks": [], "cases": [], "old_data_corners": [], "valid_for_physics_claim": False, "scope": "New explicitly declared C0-C3 compatible initial family for the ordinary CURRENT linearization. Analytic truncated Taylor recurrence and mass ODE jets; no finite-difference fitting of boundary amplitudes, no new physical coefficient or retroactive promotion of old tests."}

    def save():
        (destination / "status.json").write_text(json.dumps(report, indent=2) + "\n")

    def own(path):
        report["inputs"][str(path.relative_to(root))] = hashlib.sha256(path.read_bytes()).hexdigest()
        return json.loads(path.read_text()) if path.suffix == ".json" else None

    def verify(name, condition, detail=None):
        report["checks"].append({"name": name, "passed": bool(condition), "detail": detail})
        save()
        print(name + ": " + str(bool(condition)), flush=True)

    def maximum(value):
        return float(numerical.max(numerical.abs(value)))

    save()
    try:
        paths = ["annular_analytic_corner_jets_20260909.py", "annular_third_corner_initial_data_20260909.py", "derive_annular_analytic_third_corner_data_20260909.py", "annular_fifth_order_jet_20260909.py", "annular_coordinate_evolution_operator_20260909.py", "annular_evolution_operator_20260909.py", "annular_coupled_current_operator_20260909.py", "annular_second_corner_initial_data_20260909.py", "annular_current_corner_compatibility_20260909.py", "annular_continuum_initial_data_20260909.py"]
        for filename in paths:
            own(root / "scripts" / filename)
        diagnosis = own(intake / "annular-second-corner-truncation-diagnosis/status.json")
        verify("old_third_corner_diagnosis_complete", diagnosis["state"] == "complete" and diagnosis["passed"] == 26)
        distance = symbolic.Symbol("x")
        verify("exact_cutoff_join_through_order_five", all(symbolic.diff(distance**degree * (1 - distance)**6, distance, order).subs(distance, 1) == 0 for degree in [1, 2, 3, 4] for order in range(6)))
        radii = numerical.array([4., 8.])
        for case_name in ["canonical", "nonlinear_modulated"]:
            evaluator = AnnularFields(own(intake / "annular-constraint-correction-initial" / (case_name + ".json")))
            independent_engine = AnalyticCornerJets(evaluator, 1)
            snapshot = evaluator.evaluate(numerical.zeros_like(radii), radii, .1)
            current = snapshot_coefficients(snapshot, radii, evaluator)
            verify(case_name + "_independent_background_current", maximum(numerical.array([value.extract() for value in independent_engine.background]) - current["background"]) < 1e-14)
            verify(case_name + "_independent_background_defect", maximum(numerical.array([value.extract() for value in independent_engine.defect]) - current["independent_defect"]) < 2e-14)
            old = own(intake / "annular-second-corner-initial-data" / (case_name + "-degree64.json"))
            old_initial = numerical.zeros((5, 1, 4, 2))
            amplitudes = numerical.array(old["amplitudes"])
            for order in range(5):
                old_initial[order, 0] = numerical.einsum("b,bin->in", amplitudes, old_profiles(radii, order))
            old_initial[0, 0, 2] = numerical.einsum("b,bn->n", numerical.r_[1., amplitudes], old_family_lift(old, radii)[0][:, 2])
            old_corners, unused = independent_engine.evaluate(old_initial, numerical.ones(1))
            finite_difference = next(entry["C3"] for entry in diagnosis["third_corners"] if entry["case"] == case_name and entry["count"] == 9 and entry["space_step"] == .005)
            verify(case_name + "_analytic_C3_matches_independent_old_diagnosis", numerical.all(numerical.abs(old_corners[0, 3] - finite_difference) <= .002 * numerical.abs(finite_difference) + 1e-12), {"analytic": old_corners[0].tolist(), "finite_difference_C3": finite_difference})
            report["old_data_corners"].append({"case": case_name, "corners": old_corners[0].tolist()})
            engine = AnalyticCornerJets(evaluator, 10)
            previous = None
            for degree in [64, 80]:
                payload = build_family(evaluator, degree)
                initial = family_derivatives(payload, radii)
                family_corners, unused = engine.evaluate(initial, numerical.r_[1., numerical.zeros(9)])
                matrix = family_corners[1:, 1:].reshape((9, 9)).T
                right = -family_corners[0, 1:].ravel()
                row_scale = numerical.max(numerical.abs(matrix), axis=1)
                if numerical.any(row_scale == 0):
                    raise ValueError("Zero analytic corner-sensitivity row")
                normalized = matrix / row_scale[:, None]
                amplitudes = numerical.linalg.solve(normalized, right / row_scale)
                payload["amplitudes"] = amplitudes.tolist()
                payload["corner_matrix"] = matrix.tolist()
                payload["corner_right"] = right.tolist()
                payload["row_scaled_condition_number"] = float(numerical.linalg.cond(normalized))
                payload["method"] = "Nine affine parent C1-C3 conditions by analytic dual/Taylor recurrence; initial mass endpoint jets recursively differentiated from the mass ODE. No evolution score or derivative-step choice enters amplitude selection."
                direct, error_jets = independent_engine.evaluate(initial_derivatives(payload, radii), numerical.ones(1))
                label = case_name + "_degree" + str(degree)
                verify(label + "_conditioned_analytic_solve", numerical.all(numerical.isfinite(amplitudes)) and payload["row_scaled_condition_number"] < 1e8, {"condition_number": payload["row_scaled_condition_number"], "amplitudes": amplitudes.tolist()})
                verify(label + "_direct_parent_corners", maximum(direct) < 1e-12, {"C0_to_C3": direct[0].tolist()})
                holdout_radii = numerical.linspace(4, 8, 801)
                values, radial, unused = lift(payload, holdout_radii)
                snapshot = evaluator.evaluate(numerical.zeros_like(holdout_radii), holdout_radii, .1)
                gradient = constraint_gradients(snapshot, holdout_radii, evaluator)
                constraint = snapshot["initial_constraint"][0] + radial[0, 2] - numerical.einsum("in,in->n", gradient[:4], values[0]) - gradient[4] * radial[0, 0]
                verify(label + "_global_initial_mass_holdout", maximum(constraint) < 1e-16, {"max": maximum(constraint)})
                verify(label + "_zero_q_outer_mass_lapse", maximum(values[0, 1]) == 0 and abs(values[0, 2, -1]) < 1e-24 and values[0, 3, -1] == 0)
                finite = CornerCompatibility(evaluator, space_step=.005, time_step=.001, count=9).evaluate(lambda coordinates: lift(payload, coordinates), numerical.ones(1))[0]
                verify(label + "_independent_first_second_corner_check", maximum(finite[0]) < 1e-18 and maximum(finite[1]) < 1e-14 and maximum(finite[2]) < 1e-9, {"finite_C0_to_C2": finite.tolist()})
                if previous is not None:
                    difference = maximum(amplitudes - previous)
                    verify(case_name + "_independent_mass_degree_amplitudes", difference <= 1e-8 * maximum(amplitudes) + 1e-16, {"absolute_difference": difference})
                previous = amplitudes
                payload["analytic_corner_values"] = direct[0].tolist()
                payload["finite_difference_corner_values"] = finite.tolist()
                payload["mass_constraint_holdout_max"] = maximum(constraint)
                payload["initial_component_maxima"] = numerical.max(numerical.abs(values[0]), axis=1).tolist()
                filename = case_name + "-degree" + str(degree) + ".json"
                (destination / filename).write_text(json.dumps(payload, indent=2) + "\n")
                report["cases"].append({"case": case_name, "degree": degree, "path": filename, "sha256": hashlib.sha256((destination / filename).read_bytes()).hexdigest(), "analytic_corner_values": direct[0].tolist(), "initial_component_maxima": payload["initial_component_maxima"], "mass_constraint_holdout_max": maximum(constraint), "condition_number": payload["row_scaled_condition_number"], "valid_for_physics_claim": False})
                save()
                print(json.dumps(report["cases"][-1]), flush=True)
        for filename in paths:
            path = root / "scripts" / filename
            compile(path.read_bytes(), str(path), "exec")
        verify("no_bytecode_cache", not (root / "scripts/__pycache__").exists())
        report.update(passed=sum(check["passed"] for check in report["checks"]), total=len(report["checks"]), completed_utc=datetime.now(timezone.utc).isoformat())
        report["state"] = "complete" if report["passed"] == report["total"] else "failed"
        save()
    except Exception as error:
        report.update(state="failed", failure=repr(error), completed_utc=datetime.now(timezone.utc).isoformat())
        save()
        raise
    if report["state"] != "complete":
        raise SystemExit(1)
    (destination / "COMPLETE").write_text(report["completed_utc"] + "\n")


if __name__ == "__main__":
    run()
