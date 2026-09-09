import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as numerical
    import sympy as symbolic
    from annular_coordinate_evolution_operator_20260909 import AnnularFields
    from annular_coupled_current_time_jets_20260909 import CoupledCurrentTimeJets
    from annular_volterra_source_completion_20260909 import complete_without_scalar_projection
    from sbp4_compatible_second_operator_20260909 import flux_second, gram_action, gram_parts, remainder_action, surface_derivative
    from sbp4_derived_operator_20260909 import derivative

    root = Path(__file__).resolve().parents[1]
    intake = root / "source-intake/navier-stokes/20260909"
    destination = intake / "annular-compatible-current-restoring-source-derived"
    destination.mkdir(exist_ok=False)
    source = Path(__file__).read_bytes()
    (destination / "executed-script.py").write_bytes(source)
    report = {"state": "running", "started_utc": datetime.now(timezone.utc).isoformat(), "script_sha256": hashlib.sha256(source).hexdigest(), "inputs": {}, "checks": [], "runs": [], "valid_for_physics_claim": False, "scope": "Construct the parameter-free compatible current restoring source as the combined variable-coefficient second-derivative AND boundary-SAT change, retaining w-Dchi. Its scalar work cancels the derivative of a positive Gram energy. Complete the entire changed source by unprojected Volterra and keep its nonzero nodal residual bound. Static identities on saved states, NOT a new evolved solution or full coupled energy theorem."}

    def save():
        (destination / "status.json").write_text(json.dumps(report, indent=2) + "\n")

    def own(path):
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        report["inputs"][str(path.relative_to(root))] = digest
        return digest

    def verify(name, condition, detail=None):
        report["checks"].append({"name": name, "passed": bool(condition), "detail": detail})
        save()

    def maximum(values):
        return float(numerical.max(numerical.abs(values)))

    save()
    try:
        own(Path(__file__))
        for name in ["sbp4_compatible_second_operator_20260909.py", "sbp4_derived_operator_20260909.py", "annular_volterra_source_completion_20260909.py", "annular_coupled_current_time_jets_20260909.py"]:
            own(root / "scripts" / name)
        for name in ["sbp4-second-derivative-derived", "annular-current-driving-and-passivity-qualified", "annular-raw-volterra-C3-matched-comparison"]:
            path = intake / name / "status.json"
            own(path)
            owner = json.loads(path.read_text())
            verify(name + "_complete", owner["state"] == "complete" and owner["passed"] == owner["total"] and path.with_name("COMPLETE").exists())
            verify(name + "_inputs_unchanged", all(own(root / relative) == digest for relative, digest in owner.get("inputs", {}).items()))
        sine_squared = symbolic.symbols("sine_squared", nonnegative=True)
        centered_symbol_squared = 4 * sine_squared * (1 - sine_squared) * (3 + 2 * sine_squared)**2 / 9
        compatible_symbol = 4 * sine_squared * (1 + sine_squared / 3)
        remainder_symbol = 16 * sine_squared**3 * (2 + sine_squared) / 9
        verify("exact_interior_compatible_symbol_decomposition", symbolic.expand(compatible_symbol - centered_symbol_squared - remainder_symbol) == 0)
        verify("Nyquist_restoring_not_blind", centered_symbol_squared.subs(sine_squared, 1) == 0 and compatible_symbol.subs(sine_squared, 1) == symbolic.Rational(16, 3))
        verify("smooth_interior_fourth_order_correction", symbolic.limit(remainder_symbol / sine_squared**3, sine_squared, 0) == symbolic.Rational(32, 9))
        folder = intake / "annular-coupled-current-third-corner-raw-volterra"
        own(folder / "status.json")
        evolution = json.loads((folder / "status.json").read_text())
        verify("failed_raw_C3_evolution_retained", evolution["state"] == "failed" and evolution["passed"] == 145 and evolution["total"] == 147 and not (folder / "COMPLETE").exists())
        for case_name in ["canonical", "nonlinear_modulated"]:
            path = intake / "annular-constraint-correction-initial" / (case_name + ".json")
            own(path)
            evaluator = AnnularFields(json.loads(path.read_text()))
            for entry in evolution["runs"]:
                if entry["case"] != case_name or entry["time_refinement"] != (2 if entry["intervals"] == 512 else 1):
                    continue
                path = folder / entry["artifact"]
                tag = path.stem
                verify(tag + "_hash", own(path) == entry["sha256"])
                with numerical.load(path, allow_pickle=False) as arrays:
                    radii, state, coordinate_source = [arrays[key] for key in ["radius", "correction_current", "coordinate_numerical_source"]]
                engine = CoupledCurrentTimeJets(evaluator, radii, entry["time"])
                current = {key: value[0] for key, value in engine.current.items()}
                coefficient = radii**2 * current["c"]
                parts = gram_parts(radii.size, coefficient)
                scalar = state[0]
                velocity = numerical.sum(current["q_gradient"] * state, axis=0)
                spatial = derivative(scalar, engine.spacing)
                retained_integrability = state[1] - spatial
                remainder = remainder_action(scalar, parts) / engine.spacing
                weight = engine.weights * radii**2 * current["alpha"]
                source_q = -remainder / weight
                changed_bulk = (flux_second(scalar, coefficient, engine.spacing, parts) + derivative(coefficient * retained_integrability, engine.spacing) - derivative(coefficient * state[1], engine.spacing)) / (radii**2 * current["alpha"])
                boundary_change = numerical.zeros_like(radii)
                surface_difference = surface_derivative(scalar, engine.spacing) - spatial[[0, -1]]
                for endpoint, orientation, position in [(0, 1, 0), (-1, -1, 1)]:
                    boundary_change[endpoint] = orientation * current["c"][endpoint] * surface_difference[position] / (current["alpha"][endpoint] * engine.weights[endpoint])
                verify(tag + "_bulk_plus_boundary_equals_Gram_restoring_source", maximum(changed_bulk + boundary_change - source_q) < 1e-8 * max(maximum(source_q), 1e-20) + 1e-21)
                difference = numerical.diff(scalar, n=3)
                gram_energy = float(numerical.dot(difference, gram_action(difference, parts)) / (2 * engine.spacing))
                direct_energy = float(numerical.dot(scalar, remainder) / 2)
                source_work = float(numerical.sum(weight * velocity * source_q))
                potential_work = float(numerical.dot(velocity, remainder))
                verify(tag + "_positive_Gram_energy", gram_energy >= 0 and abs(gram_energy - direct_energy) < 1e-8 * max(gram_energy, 1e-40) + 1e-35)
                verify(tag + "_restoring_work_exact_cancellation", abs(source_work + potential_work) < 1e-10 * max(abs(source_work), abs(potential_work), 1e-40) + 1e-35)
                total_raw = coordinate_source.copy()
                total_raw[2] = 0
                total_raw[1] += source_q
                complete, diagnostics = complete_without_scalar_projection(total_raw, current["old_gradient"], engine.spacing)
                verify(tag + "_whole_changed_source_scalar_lapse_preserved", numerical.array_equal(complete[[0, 1, 3]], total_raw[[0, 1, 3]]) and complete[2, -1] == 0)
                verify(tag + "_whole_changed_source_nonzero_Noether_bound", numerical.all(numerical.abs(diagnostics["residual"]) <= diagnostics["bound"] + 1e-24))
                coefficients_dot = radii**2 * engine.current["c"][1]
                time_ratio = float(numerical.max(numerical.abs(coefficients_dot / coefficient)))
                positive_energy_time_bound = time_ratio * gram_energy
                filename = tag + "_restoring_source.npz"
                numerical.savez(destination / filename, radius=radii, source_q=source_q, completed_coordinate_source=complete, source_Noether_residual=diagnostics["residual"], source_Noether_bound=diagnostics["bound"], retained_integrability=retained_integrability, remainder_action=remainder)
                report["runs"].append({"case": case_name, "time": entry["time"], "intervals": entry["intervals"], "artifact": filename, "sha256": hashlib.sha256((destination / filename).read_bytes()).hexdigest(), "Gram_energy": gram_energy, "restoring_source_work": source_work, "canceled_potential_work": potential_work, "positive_energy_coefficient_time_bound": positive_energy_time_bound, "nonzero_kinematic_defect_work": -float(numerical.dot(current["defect"][0], remainder)), "restoring_source_max": maximum(source_q), "completed_source_residual_max": maximum(diagnostics["residual"]), "completed_source_bound_max": maximum(diagnostics["bound"]), "evolved_candidate": False, "valid_for_physics_claim": False})
                save()
        verify("all12_static_states_checked", len(report["runs"]) == 12)
        compile(Path(__file__).read_bytes(), str(Path(__file__)), "exec")
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
    print(json.dumps({key: report[key] for key in ["state", "passed", "total", "completed_utc"]}), flush=True)


if __name__ == "__main__":
    run()
