import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as numerical
    from scipy.linalg import cholesky, eigvalsh, expm, solve_triangular
    from annular_coordinate_evolution_operator_20260909 import AnnularFields
    from annular_coupled_current_time_jets_20260909 import CoupledCurrentTimeJets
    from annular_compatible_current_rhs_20260909 import compatible_current_rhs
    from sbp4_compatible_second_operator_20260909 import gram_parts, remainder_action

    root = Path(__file__).resolve().parents[1]
    intake = root / "source-intake/navier-stokes/20260909"
    destination = intake / "annular-compatible-current-timestep-qualified"
    destination.mkdir(exist_ok=False)
    source = Path(__file__).read_bytes()
    (destination / "executed-script.py").write_bytes(source)
    report = {"state": "running", "started_utc": datetime.now(timezone.utc).isoformat(), "script_sha256": hashlib.sha256(source).hexdigest(), "inputs": {}, "checks": [], "samples": [], "dt_caps": [], "valid_for_physics_claim": False, "scope": "Frozen FULL coupled finite-grid Jacobian, in a positive augmented-scalar plus metric-L2 diagnostic norm. RK4 polynomial/exponential comparison with proved matrix-series remainder. Three time samples per grid are a conservative smoke timestep selector, NOT a continuum, full-time nonautonomous stability or uniform-grid theorem. Affine parent forcing is excluded only from its Jacobian and retained in evolution.", "grids": [32, 64, 128], "sample_times": [0, 0.15, 0.3], "eta_max": 0.25, "analytic_bound": "||P4(dt B)-exp(dt B)||2 <= exp(eta)*eta^5/120, eta=dt||B||2. Hence ||P4||2 <= exp(dt nu)+remainder, nu=lambda_max((B+B^T)/2). Positive nu is reported, not erased."}

    def save():
        (destination / "status.json").write_text(json.dumps(report, indent=2) + "\n")

    def own(path):
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        report["inputs"][str(path.relative_to(root))] = digest
        return digest

    def verify(name, condition, detail=None):
        report["checks"].append({"name": name, "passed": bool(condition), "detail": detail})
        save()

    save()
    try:
        own(Path(__file__))
        path = intake / "annular-compatible-current-time-jets-preflight/status.json"
        own(path)
        preflight = json.loads(path.read_text())
        verify("actual_time_jet_preflight_complete", preflight["state"] == "complete" and preflight["passed"] == preflight["total"] and path.with_name("COMPLETE").exists())
        verify("preflight_inputs_unchanged", all(own(root / name) == digest for name, digest in preflight["inputs"].items()))
        for name in ["annular_compatible_current_rhs_20260909.py", "annular_compatible_current_restoring_20260909.py", "sbp4_compatible_second_operator_20260909.py"]:
            own(root / "scripts" / name)
        for case_name in ["canonical", "nonlinear_modulated"]:
            path = intake / "annular-constraint-correction-initial" / (case_name + ".json")
            own(path)
            evaluator = AnnularFields(json.loads(path.read_text()))
            for intervals in report["grids"]:
                caps = []
                for time_value in report["sample_times"]:
                    tag = case_name + "_N" + str(intervals) + "_T" + str(time_value)
                    report["active_job"] = tag
                    save()
                    print(tag, flush=True)
                    radii = numerical.linspace(4, 8, intervals + 1)
                    count = radii.size
                    engine = CoupledCurrentTimeJets(evaluator, radii, time_value)
                    current = {key: values[0] for key, values in engine.current.items()}
                    size = 5 * count
                    matrix = numerical.empty((size, size))
                    for column in range(size):
                        direction = numerical.zeros((5, count))
                        direction.flat[column] = 1
                        matrix[:, column] = compatible_current_rhs(current, direction, radii, engine.weights, engine.spacing, evaluator.sigma, include_forcing=False)[0].ravel()
                    direction = numerical.sin(numerical.arange(size) + 0.3).reshape(5, count)
                    affine = compatible_current_rhs(current, direction, radii, engine.weights, engine.spacing, evaluator.sigma)[0]
                    zero = compatible_current_rhs(current, numerical.zeros_like(direction), radii, engine.weights, engine.spacing, evaluator.sigma)[0]
                    verify(tag + "_affine_Jacobian_control", numerical.max(numerical.abs(matrix @ direction.ravel() - (affine - zero).ravel())) < 1e-10 * max(numerical.max(numerical.abs(affine - zero)), 1e-20))
                    velocity_map = numerical.concatenate([numerical.diag(current["q_gradient"][component]) for component in range(5)], axis=1)
                    energy = velocity_map.T @ ((engine.weights * radii**2 * current["alpha"])[:, None] * velocity_map)
                    diagonal = numerical.concatenate([engine.weights * radii**2, engine.weights * radii**2 * current["c"], numerical.zeros(count), engine.weights, engine.weights])
                    energy += numerical.diag(diagonal)
                    parts = gram_parts(count, radii**2 * current["c"])
                    remainder = remainder_action(numerical.eye(count), parts).T / engine.spacing
                    energy[:count, :count] += remainder
                    verify(tag + "_diagnostic_energy_symmetry", numerical.max(numerical.abs(energy - energy.T)) < 1e-10 * numerical.max(numerical.abs(energy)))
                    factor = cholesky(energy, lower=True)
                    balanced = solve_triangular(factor, (factor.T @ matrix).T, lower=True).T
                    operator_norm = float(numerical.linalg.norm(balanced, 2))
                    logarithmic_norm = float(eigvalsh((balanced + balanced.T) / 2, subset_by_index=[size - 1, size - 1])[0])
                    wave_speed = max(20.0, float(numerical.max((numerical.abs(current["B"]) + numerical.sqrt(current["P"] * current["Q"])) / current["alpha"])))
                    cfl_step = 0.1 / math.ceil(0.1 * wave_speed * 1.05 / (0.15 * engine.spacing))
                    dt = min(cfl_step, report["eta_max"] / operator_norm)
                    caps.append(dt)
                    eta = dt * operator_norm
                    argument = dt * balanced
                    power = numerical.eye(size)
                    polynomial = power.copy()
                    for degree in range(1, 5):
                        power = power @ argument
                        polynomial += power / math.factorial(degree)
                    exact = expm(argument)
                    remainder_bound = math.exp(eta) * eta**5 / math.factorial(5)
                    error = float(numerical.linalg.norm(polynomial - exact, 2))
                    amplification = float(numerical.linalg.norm(polynomial, 2))
                    upper = math.exp(dt * logarithmic_norm) + remainder_bound
                    verify(tag + "_eta_and_frozen_series_bound", eta <= 0.2500000001 and error <= remainder_bound * (1 + 1e-8) + 1e-12, {"eta": eta, "error": error, "bound": remainder_bound})
                    verify(tag + "_full_matrix_amplification_bound", amplification <= upper * (1 + 1e-10), {"measured": amplification, "upper": upper, "logarithmic_norm": logarithmic_norm})
                    report["samples"].append({"case": case_name, "intervals": intervals, "time": time_value, "dimension": size, "balanced_operator_norm": operator_norm, "diagnostic_logarithmic_norm": logarithmic_norm, "positive_growth_retained": logarithmic_norm > 0, "cfl_step": cfl_step, "qualified_dt": dt, "eta": eta, "matrix_exponential_error": error, "series_remainder_bound": remainder_bound, "RK4_amplification": amplification, "upper_bound": upper, "valid_for_physics_claim": False})
                    save()
                report["dt_caps"].append({"case": case_name, "intervals": intervals, "dt_cap": min(caps), "scope": "minimum of three qualified frozen-time samples, plus ordinary CFL cap in the actual runner; use unchanged time-halving checks"})
        verify("all18_samples_and6_caps", len(report["samples"]) == 18 and len(report["dt_caps"]) == 6)
        compile(Path(__file__).read_bytes(), str(Path(__file__)), "exec")
        verify("no_bytecode_cache", not (root / "scripts/__pycache__").exists())
        report.update(passed=sum(check["passed"] for check in report["checks"]), total=len(report["checks"]), completed_utc=datetime.now(timezone.utc).isoformat(), active_job=None)
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
