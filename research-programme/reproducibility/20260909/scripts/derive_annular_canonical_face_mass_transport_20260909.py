import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as numerical
    from annular_gram_joint_action_20260909 import coefficient_pairing, gram_matrices, remainder
    from sbp4_compatible_second_operator_20260909 import norm_weights
    from sbp4_derived_operator_20260909 import derivative

    root = Path(__file__).resolve().parents[1]
    intake = root / "source-intake/navier-stokes/20260909"
    destination = intake / "annular-canonical-face-mass-transport-derived"
    destination.mkdir(exist_ok=False)
    source = Path(__file__).read_bytes()
    (destination / "executed-script.py").write_bytes(source)
    report = {"state": "running", "started_utc": datetime.now(timezone.utc).isoformat(), "script_sha256": hashlib.sha256(source).hexdigest(), "inputs": {}, "checks": [], "samples": [], "refinement": [], "valid_for_physics_claim": False, "scope": "Constructive canonical fixed-flat-metric leading-stress correspondence: E=F=1, sigma=.05, kappa=.1. Same action-derived graph transport with and without Gram remainder. Exact finite-dimensional semidiscrete energy/cell-mass identity; not the old nodal D constraint, not full dynamic geometry or an evolved MTS result. Compact endpoint-zero probe velocities; no open-boundary or nonlinear-P(X) promotion.", "predeclared_flux_refinement_ratio": 2.5, "formula": "M=H r^2 alpha, N=H r^2 B, C=H r^2 c. M q_t=(N D-D^T N)q-(D^T C D+R_a)chi. Positive nodal energy e_i=(M_i q_i^2+C_i(Dchi)_i^2)/2+a_i rho_i. J=J_advection+J_gradient+J_Gram; dot e_i=-sum_j J_ij. With cut flux F, Delta mu_face=kappa e/E and mu_face,t=-kappa F/E, the cell constraint derivative vanishes identically. Continuum target mu_t=kappa r^2 q[(1-sigma)q+chi_R] for E=F=1."}

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

    def maximum(values):
        return float(numerical.max(numerical.abs(values)))

    def packet(radius, kind):
        angle = numerical.pi * (radius - 4) / 4
        amplitude = numerical.sin(angle)**4
        slope = numerical.pi * numerical.sin(angle)**3 * numerical.cos(angle)
        if kind == "symmetric":
            return 0.02 * amplitude, 0.03 * amplitude * numerical.cos(angle), 0.02 * slope
        modulation = 1 + 0.2 * numerical.sin(2 * angle)
        modulation_slope = 0.1 * numerical.pi * numerical.cos(2 * angle)
        return 0.02 * amplitude * modulation, 0.03 * amplitude * (0.4 + numerical.cos(2 * angle)), 0.02 * (slope * modulation + amplitude * modulation_slope)

    save()
    try:
        own(Path(__file__))
        prior_path = intake / "annular-Gram-energy-transport-derived/status.json"
        own(prior_path)
        prior = json.loads(prior_path.read_text())
        verify("joint_energy_transport_complete", prior["state"] == "complete" and prior["passed"] == prior["total"] == 130 and prior_path.with_name("COMPLETE").exists())
        verify("joint_energy_sources_unchanged", all(own(root / name) == digest for name, digest in prior["inputs"].items()))
        sigma, kappa = 0.05, 0.1
        alpha, mixed = sigma * (2 - sigma), 1 - sigma
        for kind in ["symmetric", "asymmetric"]:
            for intervals in [32, 64, 128]:
                radii = numerical.linspace(4, 8, intervals + 1)
                spacing = 4 / intervals
                weights = spacing * norm_weights(radii.size)
                derivative_matrix = derivative(numerical.eye(radii.size), spacing).T
                scalar, velocity, unused_slope = packet(radii, kind)
                gradient = derivative_matrix @ scalar
                mass_matrix = weights * radii**2 * alpha
                cross_matrix = weights * radii**2 * mixed
                gradient_matrix = weights * radii**2
                skew = cross_matrix[:, None] * derivative_matrix - derivative_matrix.T * cross_matrix[None, :]
                factors, sampling = gram_matrices(radii.size)
                coefficient = radii**2
                for include_gram in [False, True]:
                    branch = "Gram" if include_gram else "baseline"
                    tag = kind + "_N" + str(intervals) + "_" + branch
                    restoring = remainder(scalar, coefficient, spacing) if include_gram else numerical.zeros_like(scalar)
                    velocity_time = (skew @ velocity - derivative_matrix.T @ (gradient_matrix * gradient) - restoring) / mass_matrix
                    gradient_time = derivative_matrix @ velocity
                    dual = coefficient_pairing(scalar, scalar, spacing) / 2 if include_gram else numerical.zeros_like(scalar)
                    dual_time = coefficient_pairing(scalar, velocity, spacing) if include_gram else numerical.zeros_like(scalar)
                    local_energy = (mass_matrix * velocity**2 + gradient_matrix * gradient**2) / 2 + coefficient * dual
                    local_energy_time = mass_matrix * velocity * velocity_time + gradient_matrix * gradient * gradient_time + coefficient * dual_time
                    advective = -skew * velocity[:, None] * velocity[None, :]
                    directed_gradient = derivative_matrix.T * velocity[:, None] * (gradient_matrix * gradient)[None, :]
                    gradient_current = directed_gradient - directed_gradient.T
                    gram_current = numerical.zeros_like(skew)
                    if include_gram:
                        directed = ((factors.T * ((factors @ scalar) / spacing)) @ sampling) * velocity[:, None] * coefficient[None, :]
                        gram_current = directed - directed.T
                    graph_current = advective + gradient_current + gram_current
                    divergence = graph_current.sum(axis=1)
                    scale = max(maximum(local_energy_time), maximum(divergence), 1e-20)
                    verify(tag + "_positive_energy_and_skew_transport", numerical.all(local_energy >= 0) and maximum(graph_current + graph_current.T) < 1e-14)
                    verify(tag + "_full_action_local_energy_identity", maximum(local_energy_time + divergence) <= 1e-10 * scale + 1e-16)
                    face_flux = numerical.array([0.] + [float(graph_current[:cut, cut:].sum()) for cut in range(1, radii.size)] + [0.])
                    mass_faces = numerical.concatenate(([1.], 1 + kappa * numerical.cumsum(local_energy)))
                    mass_face_time = -kappa * face_flux
                    cell_constraint = numerical.diff(mass_faces) - kappa * local_energy
                    cell_constraint_time = numerical.diff(mass_face_time) - kappa * local_energy_time
                    verify(tag + "_constructed_mass_cell_constraint", maximum(cell_constraint) < 1e-14)
                    verify(tag + "_mass_constraint_time_identity", maximum(cell_constraint_time) <= 1e-10 * kappa * scale + 1e-16)
                    face_radius = numerical.concatenate(([4.], 4 + numerical.cumsum(weights)))
                    unused_scalar, exact_velocity, exact_gradient = packet(face_radius, kind)
                    continuum = kappa * face_radius**2 * exact_velocity * (mixed * exact_velocity + exact_gradient)
                    error = maximum(mass_face_time - continuum)
                    artifact = destination / (tag + "_face_transport.npz")
                    numerical.savez_compressed(artifact, radius=radii, face_radius=face_radius, scalar=scalar, velocity=velocity, velocity_time=velocity_time, local_energy=local_energy, local_energy_time=local_energy_time, graph_current=graph_current, face_flux=face_flux, mass_faces=mass_faces, mass_face_time=mass_face_time, continuum_mass_time=continuum, cell_constraint=cell_constraint, cell_constraint_time=cell_constraint_time)
                    report["samples"].append({"case": kind, "intervals": intervals, "branch": branch, "artifact": artifact.name, "sha256": hashlib.sha256(artifact.read_bytes()).hexdigest(), "all_face_mass_flux_error": error, "continuum_mass_flux_max": maximum(continuum), "max_cell_constraint": maximum(cell_constraint), "max_cell_constraint_time": maximum(cell_constraint_time), "endpoint_velocities": velocity[[0, -1]].tolist(), "mass_anchor_is_arbitrary_diagnostic_not_background": True, "valid_for_physics_claim": False})
        for kind in ["symmetric", "asymmetric"]:
            for branch in ["baseline", "Gram"]:
                selected = sorted([row for row in report["samples"] if row["case"] == kind and row["branch"] == branch], key=lambda row: row["intervals"])
                errors = [row["all_face_mass_flux_error"] for row in selected]
                ratios = [errors[position] / errors[position + 1] for position in range(2)]
                verify(kind + "_" + branch + "_all_face_continuum_flux_refinement", all(ratio >= report["predeclared_flux_refinement_ratio"] for ratio in ratios), {"errors": errors, "ratios": ratios})
                report["refinement"].append({"case": kind, "branch": branch, "errors": errors, "ratios": ratios, "gates_passed": all(ratio >= report["predeclared_flux_refinement_ratio"] for ratio in ratios), "continuum_error_bound": False})
        verify("all12_same_probe_controls", len(report["samples"]) == 12 and len(report["refinement"]) == 4)
        verify("no_bytecode_cache", not (root / "scripts/__pycache__").exists())
        compile(Path(__file__).read_bytes(), str(Path(__file__)), "exec")
        report.update(passed=sum(check["passed"] for check in report["checks"]), total=len(report["checks"]), completed_utc=datetime.now(timezone.utc).isoformat(), active_job=None)
        report["state"] = "complete" if report["passed"] == report["total"] else "failed"
        save()
    except Exception as error:
        report.update(state="failed", failure=repr(error), completed_utc=datetime.now(timezone.utc).isoformat(), active_job=None)
        save()
        raise
    print(json.dumps({key: report[key] for key in ["state", "passed", "total", "completed_utc"]}), flush=True)
    if report["state"] != "complete":
        raise SystemExit(1)
    (destination / "COMPLETE").write_text(report["completed_utc"] + "\n")


if __name__ == "__main__":
    run()
