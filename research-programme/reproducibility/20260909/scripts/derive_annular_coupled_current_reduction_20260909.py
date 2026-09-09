import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path
from types import SimpleNamespace

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as numerical
    import sympy as symbolic
    from annular_coordinate_evolution_operator_20260909 import AnnularFields
    from annular_coupled_current_operator_20260909 import maps, physical_transform, principal, snapshot_coefficients
    from annular_evolution_operator_20260909 import local_jacobians

    root = Path(__file__).resolve().parents[1]
    intake = root / "source-intake/navier-stokes/20260909"
    parser = argparse.ArgumentParser()
    parser.add_argument("--tag", default="annular-coupled-current-reduction-broadcast")
    arguments = parser.parse_args()
    if not arguments.tag or any(character not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_" for character in arguments.tag):
        raise ValueError("Unsafe output tag")
    destination = intake / arguments.tag
    destination.mkdir(exist_ok=False)
    script = Path(__file__).read_bytes()
    (destination / "executed-script.py").write_bytes(script)
    report = {"state": "running", "started_utc": datetime.now(timezone.utc).isoformat(), "script_sha256": hashlib.sha256(script).hexdigest(), "inputs": {}, "checks": [], "fixtures": [], "valid_for_physics_claim": False}

    def save():
        (destination / "status.json").write_text(json.dumps(report, indent=2) + "\n")

    def verify(name, condition, detail=None):
        report["checks"].append({"name": name, "passed": bool(condition), "detail": detail})
        save()
        print(name + ": " + str(bool(condition)), flush=True)

    def own(path):
        report["inputs"][str(path.relative_to(root))] = hashlib.sha256(path.read_bytes()).hexdigest()

    def maximum(value):
        return float(numerical.max(numerical.abs(value)))

    save()
    try:
        for name in ["annular_coupled_current_operator_20260909.py", "derive_annular_coupled_current_reduction_20260909.py", "annular_coordinate_evolution_operator_20260909.py", "annular_evolution_operator_20260909.py", "annular_conservative_scalar_evolution_20260909.py", "annular_noether_completion_20260909.py"]:
            path = root / "scripts" / name
            own(path)
            compile(path.read_bytes(), str(path), "exec")
        alpha, mixed, wave, discriminant, exponential, sigma = symbolic.symbols("alpha B c D E sigma", positive=True)
        scalar_matrix = symbolic.Matrix([[mixed, 1], [discriminant, mixed]]) / alpha
        scalar_transform = symbolic.Matrix([[sigma * exponential, 1], [exponential * (alpha - sigma * mixed), -mixed]])
        scalar_norm = symbolic.diag(discriminant, 1)
        physical_norm = scalar_transform.T * scalar_norm * scalar_transform
        verify("exact_scalar_transform_determinant", symbolic.expand(scalar_transform.det() + exponential * alpha) == 0)
        verify("exact_positive_norm_determinant", symbolic.expand(physical_norm.det() - exponential**2 * alpha**2 * discriminant) == 0)
        verify("exact_scalar_symmetry", scalar_norm * scalar_matrix == (scalar_norm * scalar_matrix).T)
        radius = symbolic.Integer(2)
        tilt = symbolic.Rational(1, 20)
        radial = symbolic.Rational(1, 50)
        raw = symbolic.Matrix([[10, 10, radial / radius, 0], [10, 10, -radial / radius, 0], [0, 0, 0, 0], [0, 0, 0, 20]])
        reduced = raw.copy()
        reduced[1, 2] += 2 * radial / radius
        verify("raw_horizon_zero_eigenvalue_has_Jordan_chain", len(raw.nullspace()) == 1 and len((raw**2).nullspace()) == 2)
        verify("reduced_horizon_zero_eigenvalue_semisimple", len(reduced.nullspace()) == 2 and len((reduced**2).nullspace()) == 2)
        for case_name in ["canonical", "nonlinear_modulated"]:
            path = intake / "annular-constraint-correction-initial" / (case_name + ".json")
            own(path)
            evaluator = AnnularFields(json.loads(path.read_text()))
            batch_radii = numerical.linspace(4, 8, 17)[None, :]
            batch = evaluator.evaluate(numerical.array([0.0, 0.1, 0.3])[:, None], batch_radii, 0.1)
            batch_current = snapshot_coefficients(batch, batch_radii, evaluator)
            verify(case_name + "_batched_shape_and_offshell_identity", batch_current["defect"].shape == (5, 3, 17) and maximum(batch_current["defect"] - batch_current["independent_defect"]) < 2e-14)
            for time in [0.0, 0.1, 0.3]:
                radii = numerical.linspace(4, 8, 65)
                snapshot = evaluator.evaluate(numerical.full_like(radii, time), radii, 0.1)
                current = snapshot_coefficients(snapshot, radii, evaluator)
                error = maximum(current["defect"] - current["independent_defect"])
                scale = maximum(current["defect"])
                verify(case_name + "_T" + str(time) + "_offshell_parent_reduction", error < 1e-10 * scale + 2e-15, {"error": error, "defect_scale": scale, "J0_max": maximum(current["J0"]), "omitted_constraint_force": maximum(current["f_mu"] * current["J0"])})
                report["fixtures"].append({"case": case_name, "time": time, "background_residual_max": scale, "mass_constraint_max": maximum(current["J0"]), "constraint_force_max": maximum(current["f_mu"] * current["J0"]), "valid_for_physics_claim": False})
            for lapse in [0.5, 0.0, -0.5]:
                radii = numerical.array([4.0])
                mass = radii * (1 - lapse - evaluator.constants["Lambda"] * radii**2 / 3) / 2
                primitive = numerical.stack([0.03 + 0 * radii, 0.01 + 0 * radii, 0.0205 + 0 * radii, mass, 0 * radii])
                data, gradients, unused, unused_transform = maps(primitive, radii, evaluator)
                transform = physical_transform(primitive, data, evaluator.sigma)[:, :, 0]
                current_principal = principal(data, gradients, evaluator.sigma)[:, :, 0]
                physical = numerical.stack([primitive[0], primitive[1] / data["E"], primitive[2] - evaluator.sigma * primitive[1], primitive[3], primitive[4]])
                physical_principal = local_jacobians(physical, numerical.zeros_like(physical), radii, evaluator.constants, evaluator.kappa, evaluator.sigma)[1][:, :, 0]
                discrepancy = maximum(current_principal @ transform - transform @ physical_principal)
                scalar_transform_numeric = transform[1:3, 1:3]
                scalar_norm_numeric = scalar_transform_numeric.T @ numerical.diag([data["P"][0] * data["Q"][0], 1]) @ scalar_transform_numeric
                norm = numerical.eye(5)
                norm[1:3, 1:3] = scalar_norm_numeric
                inverse = numerical.linalg.inv(transform)
                current_norm = inverse.T @ norm @ inverse
                symmetric_error = maximum(current_norm @ current_principal - current_principal.T @ current_norm)
                tag = case_name + "_F" + str(lapse)
                verify(tag + "_full_parent_principal_similarity", discrepancy < 1e-11, {"error": discrepancy})
                verify(tag + "_full_reduced_positive_symmetrizer", float(numerical.min(numerical.linalg.eigvalsh(current_norm))) > 0 and symmetric_error < 1e-10, {"minimum_norm_eigenvalue": float(numerical.min(numerical.linalg.eigvalsh(current_norm))), "symmetry_error": symmetric_error})
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
