import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as numerical
    import sympy as symbolic

    root = Path(__file__).resolve().parents[1]
    intake = root / "source-intake/navier-stokes/20260909"
    destination = intake / "annular-trace-regularity-lower-bounds"
    destination.mkdir(exist_ok=False)
    source = Path(__file__).read_bytes()
    (destination / "executed-script.py").write_bytes(source)
    report = {"state": "running", "started_utc": datetime.now(timezone.utc).isoformat(), "script_sha256": hashlib.sha256(source).hexdigest(), "inputs": {}, "checks": [], "runs": [], "valid_for_physics_claim": False, "scope": "Derived cellwise H3/H4 lower bounds for ANY reconstruction matching the specified nodal traces. Physical target is H3 scalar plus H4 metric, not unnecessary H4 on every auxiliary current. Finite-grid lower bounds and observed trends do not prove a continuum solution singular or absent."}

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

    save()
    try:
        folder = intake / "annular-current-normal-reconstruction"
        own(folder / "status.json")
        owner = json.loads((folder / "status.json").read_text())
        path = intake / "annular-normal-constraint-H4-diagnosis/status.json"
        own(path)
        norm_owner = json.loads(path.read_text())
        verify("reconstruction_and_norm_owners_complete", owner["state"] == "complete" and owner["passed"] == owner["total"] == 526 and norm_owner["state"] == "complete" and norm_owner["passed"] == norm_owner["total"] == 90)
        verify("norm_owner_inputs_unchanged", all(own(root / name) == digest for name, digest in norm_owner["inputs"].items()))
        own(Path(__file__))
        coordinate = symbolic.symbols("coordinate", nonnegative=True)
        left_kernel = coordinate * (1 - coordinate)**2
        right_kernel = coordinate**2 * (1 - coordinate)
        third_kernel = coordinate * (1 - coordinate)
        gram = symbolic.Matrix([[symbolic.integrate(first * second, (coordinate, 0, 1)) for second in [left_kernel, right_kernel]] for first in [left_kernel, right_kernel]])
        verify("fourth_derivative_kernel_Gram", gram == symbolic.Matrix([[symbolic.Rational(1, 105), symbolic.Rational(1, 140)], [symbolic.Rational(1, 140), symbolic.Rational(1, 105)]]))
        verify("fourth_derivative_optimal_trace_quadratic", gram.inv() == symbolic.Matrix([[240, -180], [-180, 240]]))
        verify("third_derivative_kernel_norm", symbolic.integrate(third_kernel**2, (coordinate, 0, 1)) == symbolic.Rational(1, 30))
        for degree in range(8):
            polynomial = coordinate**degree
            difference = polynomial.subs(coordinate, 1) - polynomial.subs(coordinate, 0)
            slopes = [symbolic.diff(polynomial, coordinate).subs(coordinate, endpoint) for endpoint in [0, 1]]
            curvatures = [symbolic.diff(polynomial, coordinate, 2).subs(coordinate, endpoint) for endpoint in [0, 1]]
            left_trace = curvatures[0] - 6 * difference + 4 * slopes[0] + 2 * slopes[1]
            right_trace = curvatures[1] + 6 * difference - 2 * slopes[0] - 4 * slopes[1]
            third_trace = slopes[0] + slopes[1] - 2 * difference
            verify("Peano_kernel_polynomial_degree_" + str(degree), all(symbolic.simplify(trace - symbolic.integrate(kernel * symbolic.diff(polynomial, coordinate, order), (coordinate, 0, 1))) == 0 for trace, kernel, order in [(left_trace, left_kernel, 4), (right_trace, right_kernel, 4), (third_trace, third_kernel, 3)]))
        for entry in owner["runs"]:
            path = folder / entry["artifact"]
            verify(path.stem + "_source_hash", own(path) == entry["sha256"])
            with numerical.load(path, allow_pickle=False) as arrays:
                radii = arrays["radius"]
                values = arrays["normalized_current_jet_(0, 0)"]
                slopes = arrays["normalized_current_jet_(0, 1)"]
                curvatures = 2 * arrays["normalized_current_jet_(0, 2)"]
            spacing = float(radii[1] - radii[0])
            secant = numerical.diff(values, axis=-1) / spacing
            left_trace = curvatures[:, :-1] + (4 * slopes[:, :-1] + 2 * slopes[:, 1:] - 6 * secant) / spacing
            right_trace = curvatures[:, 1:] + (6 * secant - 2 * slopes[:, :-1] - 4 * slopes[:, 1:]) / spacing
            third_trace = slopes[:, :-1] + slopes[:, 1:] - 2 * secant
            lower4_squared = numerical.sum(30 * (left_trace + right_trace)**2 + 210 * (left_trace - right_trace)**2, axis=-1) / spacing**3
            lower3_squared = 30 * numerical.sum(third_trace**2, axis=-1) / spacing**3
            selected = next(row for row in norm_owner["norms"] if all(row[key] == entry[key] for key in ["case", "time", "intervals", "method"]))
            measured = numerical.array(selected["derivative_L2_norms_orders0to4"])
            verify(path.stem + "_trace_lower_bounds_below_measured_norm", numerical.all(lower4_squared <= measured[4]**2 * (1 + 1e-8) + 1e-30) and numerical.all(lower3_squared <= measured[3]**2 * (1 + 1e-8) + 1e-30))
            floor_squared = lower3_squared[0] + lower4_squared[3] + lower4_squared[4]
            actual_squared = numerical.sum(measured[:4, 0]**2) + numerical.sum(measured[:, [3, 4]]**2)
            report["runs"].append({"case": entry["case"], "time": entry["time"], "intervals": entry["intervals"], "method": entry["method"], "derivative3_lower_bound_by_current_component": numerical.sqrt(lower3_squared).tolist(), "derivative4_lower_bound_by_current_component": numerical.sqrt(lower4_squared).tolist(), "physical_H3chi_H4mu_H4delta_lower_bound": float(numerical.sqrt(floor_squared)), "measured_physical_H3chi_H4mu_H4delta_norm": float(numerical.sqrt(actual_squared)), "fraction_of_measured_physical_norm_forced_by_traces": float(numerical.sqrt(floor_squared / max(actual_squared, 1e-300))), "valid_for_physics_claim": False})
            save()
        compile(Path(__file__).read_bytes(), str(Path(__file__)), "exec")
        verify("no_bytecode_cache", not (root / "scripts/__pycache__").exists())
        report.update(passed=sum(check["passed"] for check in report["checks"]), total=len(report["checks"]), completed_utc=datetime.now(timezone.utc).isoformat())
        report["state"] = "complete" if report["passed"] == report["total"] else "failed"
        save()
    except Exception as error:
        report.update(state="failed", failure=repr(error), completed_utc=datetime.now(timezone.utc).isoformat())
        save()
        raise
    print(json.dumps({key: report[key] for key in ["state", "passed", "total", "completed_utc"]}), flush=True)
    if report["state"] != "complete":
        raise SystemExit(1)
    (destination / "COMPLETE").write_text(report["completed_utc"] + "\n")


if __name__ == "__main__":
    run()
