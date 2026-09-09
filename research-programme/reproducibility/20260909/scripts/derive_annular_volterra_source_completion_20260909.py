import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as numerical
    import sympy as symbolic
    from scipy.integrate import quad
    from annular_volterra_source_completion_20260909 import exponential_moments, integrate_source, residual_bound, derivative_moments, complete_without_scalar_projection
    from annular_coordinate_evolution_operator_20260909 import AnnularFields
    from annular_coupled_current_operator_20260909 import snapshot_coefficients
    from sbp4_derived_operator_20260909 import derivative

    root = Path(__file__).resolve().parents[1]
    intake = root / "source-intake/navier-stokes/20260909"
    destination = intake / "annular-volterra-source-completion-derived"
    destination.mkdir(exist_ok=False)
    source = Path(__file__).read_bytes()
    (destination / "executed-script.py").write_bytes(source)
    report = {"state": "running", "started_utc": datetime.now(timezone.utc).isoformat(), "script_sha256": hashlib.sha256(source).hexdigest(), "inputs": {}, "checks": [], "controls": [], "source_replays": [], "valid_for_physics_claim": False, "bound_scope": "Analytic all-row bound for the exact piecewise-constant-coefficient, piecewise-linear-forcing Volterra reconstruction. Floating evaluation is checked, not outward-rounded interval arithmetic; original smooth-coefficient and parent/background errors remain separate."}

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
        argument, coordinate = symbolic.symbols("z x", real=True)
        verify("exact_exponential_first_moment", symbolic.simplify(symbolic.integrate(symbolic.exp(argument * coordinate), (coordinate, 0, 1), conds="none") - (symbolic.exp(argument) - 1) / argument) == 0)
        verify("exact_exponential_linear_moment", symbolic.simplify(symbolic.integrate(coordinate * symbolic.exp(argument * coordinate), (coordinate, 0, 1), conds="none") - ((argument - 1) * symbolic.exp(argument) + 1) / argument**2) == 0)
        sample = numerical.array([-2., -0.1, -0.099, -1e-12, 0., 1e-12, 0.099, 0.1, 2.])
        first, weighted = exponential_moments(sample)
        first_exact = numerical.array([quad(lambda value: numerical.exp(entry * value), 0, 1, epsabs=1e-13)[0] for entry in sample])
        weighted_exact = numerical.array([quad(lambda value: value * numerical.exp(entry * value), 0, 1, epsabs=1e-13)[0] for entry in sample])
        verify("independent_quadrature_moments", maximum(first - first_exact) < 2e-14 and maximum(weighted - weighted_exact) < 2e-14)
        for count in [17, 33, 65, 129]:
            radii = numerical.linspace(4, 8, count)
            spacing = radii[1] - radii[0]
            moments = derivative_moments(count)
            coefficient = 0 * radii
            forcing = 0.01 * radii + 0.02
            actual = integrate_source(coefficient, forcing, spacing)
            exact = 0.005 * (radii**2 - 64) + 0.02 * (radii - 8)
            verify("zero_coefficient_linear_forcing_N" + str(count - 1), maximum(actual - exact) < 2e-14)
            for kind in ["constant", "varying", "boundary_spike"]:
                coefficient = 0.07 + (0.02 * numerical.sin(radii) if kind == "varying" else 0 * radii)
                forcing = 0.1 * numerical.cos(0.7 * radii)
                if kind == "boundary_spike":
                    forcing = numerical.zeros_like(radii)
                    forcing[0], forcing[-1] = 0.1, -0.2
                solution = integrate_source(coefficient, forcing, spacing)
                residual = derivative(solution, spacing) - coefficient * solution - forcing
                bound, constants = residual_bound(coefficient, forcing, spacing, moments=moments)
                verify(kind + "_all_row_bound_N" + str(count - 1), numerical.all(numerical.abs(residual) <= bound + 2e-13) and maximum(solution) <= constants["amplitude_bound"] + 2e-14 and solution[-1] == 0)
                report["controls"].append({"kind": kind, "intervals": count - 1, "residual_max": maximum(residual), "bound_max": maximum(bound), **constants})
        owner_path = intake / "annular-coupled-current-correction-refined/status.json"
        owner = json.loads(owner_path.read_text())
        own(owner_path)
        verify("failed_owner_preserved", owner["state"] == "failed" and owner["passed"] == 126 and owner["total"] == 127)
        for case_name in ["canonical", "nonlinear_modulated"]:
            path = intake / "annular-constraint-correction-initial" / (case_name + ".json")
            own(path)
            evaluator = AnnularFields(json.loads(path.read_text()))
            for entry in owner["runs"]:
                if entry["case"] != case_name or entry["intervals"] != 512 or entry["time_refinement"] != 2:
                    continue
                path = owner_path.parent / entry["artifact"]
                verify(entry["artifact"] + "_hash", own(path) == entry["sha256"])
                with numerical.load(path, allow_pickle=False) as arrays:
                    radii = arrays["radius"]
                    prior = arrays["coordinate_numerical_source"]
                raw = numerical.zeros_like(prior)
                raw[1, [0, -1]] = prior[1, [0, -1]]
                raw[3, -1] = prior[3, -1]
                snapshot = evaluator.evaluate(numerical.full_like(radii, entry["time"]), radii, 0.1)
                current = snapshot_coefficients(snapshot, radii, evaluator)
                candidate, diagnostics = complete_without_scalar_projection(raw, current["old_gradient"], radii[1] - radii[0])
                verify(entry["artifact"] + "_scalar_lapse_unchanged", numerical.array_equal(candidate[[0, 1, 3]], raw[[0, 1, 3]]) and candidate[2, -1] == 0)
                verify(entry["artifact"] + "_all_row_residual_bounded_not_zeroed", numerical.all(numerical.abs(diagnostics["residual"]) <= diagnostics["bound"] + 1e-25) and maximum(diagnostics["residual"]) > 0)
                report["source_replays"].append({"case": case_name, "time": entry["time"], "old_interior_q_source_max": maximum(prior[1, 1:-1]), "new_interior_q_source_max": maximum(candidate[1, 1:-1]), "mass_source_change_max": maximum(candidate[2] - prior[2]), "source_constraint_residual_max": maximum(diagnostics["residual"]), "derived_bound_max": maximum(diagnostics["bound"]), "valid_for_physics_claim": False})
                save()
        for name in ["annular_volterra_source_completion_20260909.py", "derive_annular_volterra_source_completion_20260909.py", "annular_coupled_current_operator_20260909.py", "annular_coordinate_evolution_operator_20260909.py", "annular_evolution_operator_20260909.py", "sbp4_derived_operator_20260909.py"]:
            path = root / "scripts" / name
            own(path)
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
