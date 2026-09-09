import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as numerical
    from annular_coordinate_evolution_operator_20260909 import AnnularFields
    from annular_conservative_scalar_evolution_20260909 import constitutive
    from annular_gram_joint_action_20260909 import action, coefficient_jets, coefficient_pairing, gram_matrices, matter_values, potential, potential_gradient, remainder
    from sbp4_compatible_second_operator_20260909 import norm_weights
    from sbp4_derived_operator_20260909 import derivative

    root = Path(__file__).resolve().parents[1]
    intake = root / "source-intake/navier-stokes/20260909"
    destination = intake / "annular-Gram-energy-transport-derived"
    destination.mkdir(exist_ok=False)
    source = Path(__file__).read_bytes()
    (destination / "executed-script.py").write_bytes(source)
    report = {"state": "running", "started_utc": datetime.now(timezone.utc).isoformat(), "script_sha256": hashlib.sha256(source).hexdigest(), "inputs": {}, "checks": [], "samples": [], "valid_for_physics_claim": False, "scope": "Exact time-Noether virtual-work identity for the proposed action, isolated Gram-sector control, positive nodal Gram energy and antisymmetric finite-range graph current derived from existing factors. Arbitrary time paths at actual parent samples, no new evolution. Graph current is not yet a Hilbert stress or a signed Einstein-constraint completion. Full endpoint rows retained; no damping/physical pass.", "graph_formula": "rho_i=[S^T(Tchi)^2]_i/(2h), U=sum_i a_i rho_i. J_ij=sum_l (Tchi)_l [T_li q_i S_lj a_j - T_lj q_j S_li a_i]/h. e'_kin,i+e'_U,i=-sum_j J_ij+rho_i a'_i for the isolated restoring contribution. Face flux is sum of J crossing the cut."}

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

    save()
    try:
        own(Path(__file__))
        prior_path = intake / "annular-Gram-joint-action-stable/status.json"
        own(prior_path)
        prior = json.loads(prior_path.read_text())
        verify("joint_action_stable_validation_complete", prior["state"] == "complete" and prior["passed"] == prior["total"] and prior_path.with_name("COMPLETE").exists())
        verify("joint_action_all_inputs_unchanged", all(own(root / name) == digest for name, digest in prior["inputs"].items()))
        for case_name in ["canonical", "nonlinear_modulated"]:
            case_path = intake / "annular-constraint-correction-initial" / (case_name + ".json")
            own(case_path)
            evaluator = AnnularFields(json.loads(case_path.read_text()))
            constants, sigma, kappa = evaluator.constants, evaluator.sigma, evaluator.kappa
            for intervals in [32, 64, 128]:
                radii = numerical.linspace(4, 8, intervals + 1)
                spacing = 4 / intervals
                weights = spacing * norm_weights(radii.size)
                derivative_matrix = derivative(numerical.eye(radii.size), spacing).T
                factors, sampling = gram_matrices(radii.size)
                for time_value in [0, 0.1, 0.3]:
                    tag = case_name + "_N" + str(intervals) + "_T" + str(time_value)
                    report["active_job"] = tag
                    save()
                    snapshot = evaluator.evaluate(numerical.full_like(radii, time_value), radii, 0.1)
                    state = snapshot["state"][0]
                    primitive = numerical.stack([state[0], state[1], snapshot["state_space"][0, 0], state[2], state[3], numerical.zeros_like(radii)])
                    integrability = primitive[2] - derivative_matrix @ primitive[0]
                    tangent = numerical.zeros_like(primitive)
                    tangent[0] = primitive[1]
                    tangent[1] = 0.03 * numerical.cos(2 * radii)
                    tangent[2] = derivative_matrix @ primitive[1]
                    tangent[3] = snapshot["state_time"][0, 2]
                    tangent[4] = snapshot["state_time"][0, 3]
                    varied = primitive.astype(complex) + 1j * 1e-25 * tangent
                    gradient = potential_gradient(primitive, radii, constants, sigma, spacing)
                    gradient_time = potential_gradient(varied, radii, constants, sigma, spacing).imag / 1e-25
                    energy_varied = potential(varied, radii, constants, sigma, spacing) - numerical.sum(varied[1] * potential_gradient(varied, radii, constants, sigma, spacing)[1])
                    energy_rate = float(energy_varied.imag / 1e-25)
                    gram_scalar_residual = -gradient_time[1] + gradient[0] + derivative_matrix.T @ gradient[2]
                    gram_terms = numerical.array([numerical.dot(primitive[1], gram_scalar_residual), numerical.dot(tangent[3], gradient[3]), numerical.dot(tangent[4], gradient[4])])
                    verify(tag + "_isolated_Gram_time_Noether", abs(energy_rate - gram_terms.sum()) <= 1e-8 * max(abs(energy_rate), maximum(gram_terms), 1e-25) + 1e-24)
                    exponential, lapse, unused_det, radial, physical_time, kinetic, lagrangian, principal = matter_values(primitive, radii, constants, sigma)
                    current = constitutive(primitive[1], primitive[2], exponential, lapse, constants, sigma)
                    varied_exponential, varied_lapse, unused_det, varied_radial, unused_time, unused_kinetic, varied_lagrangian, unused_principal = matter_values(varied, radii, constants, sigma)
                    varied_current = constitutive(varied[1], varied[2], varied_exponential, varied_lapse, constants, sigma)
                    varied_momentum = weights * radii**2 * varied_current["momentum"] - potential_gradient(varied, radii, constants, sigma, spacing)[1]
                    momentum_time = varied_momentum.imag / 1e-25
                    gravity_momentum_time = -sigma * weights * exponential * tangent[4] / kappa
                    scalar_gradient = -weights * radii**2 * exponential * constants["m_chi"]**2 * primitive[0] - derivative_matrix.T @ (weights * radii**2 * current["flux"]) - gradient[0] - derivative_matrix.T @ gradient[2]
                    mass_gradient = derivative_matrix.T @ (weights * exponential) / kappa + weights * radii * exponential * principal * radial**2 - gradient[3]
                    shift_gradient = weights * exponential * (derivative_matrix @ primitive[3] - sigma * tangent[3]) / kappa + weights * radii**2 * exponential * (lagrangian + principal * physical_time * radial) - gradient[4]
                    full_terms = numerical.array([numerical.dot(momentum_time - scalar_gradient, primitive[1]), numerical.dot(gravity_momentum_time - mass_gradient, tangent[3]), -numerical.dot(shift_gradient, tangent[4])])
                    full_energy_varied = numerical.sum(weights * radii**2 * (varied_current["momentum"] * varied[1] - varied_exponential * varied_lagrangian)) - numerical.sum(weights * varied_exponential * (derivative_matrix @ varied[3]) / kappa) + energy_varied
                    full_energy_rate = float(full_energy_varied.imag / 1e-25)
                    verify(tag + "_whole_action_time_Noether_all_rows", abs(full_energy_rate - full_terms.sum()) <= 1e-9 * max(abs(full_energy_rate), maximum(full_terms), 1e-20) + 1e-15)
                    coefficient, coefficient_gradient, unused_hessian = coefficient_jets(primitive, radii, constants, sigma)
                    coefficient_time = numerical.sum(coefficient_gradient * tangent[1:], axis=0)
                    factor_scalar, factor_velocity = factors @ primitive[0], factors @ primitive[1]
                    dual = coefficient_pairing(primitive[0], primitive[0], spacing) / 2
                    dual_time = coefficient_pairing(primitive[0], primitive[1], spacing)
                    local_potential = coefficient * dual
                    verify(tag + "_positive_nodal_energy_and_total", numerical.all(local_potential >= 0) and abs(local_potential.sum() - potential(primitive, radii, constants, sigma, spacing)) < 1e-12 * max(float(local_potential.sum()), 1e-30))
                    directed = (factors.T * (factor_scalar / spacing)) @ sampling
                    directed *= primitive[1][:, None] * coefficient[None, :]
                    graph_current = directed - directed.T
                    force_work = -primitive[1] * remainder(primitive[0], coefficient, spacing)
                    potential_rate = coefficient * dual_time + coefficient_time * dual
                    coefficient_work = coefficient_time * dual
                    divergence = graph_current.sum(axis=1)
                    scale = max(maximum(force_work), maximum(potential_rate), maximum(divergence), 1e-30)
                    verify(tag + "_antisymmetric_graph_current", maximum(graph_current + graph_current.T) == 0)
                    verify(tag + "_local_positive_energy_balance_all_nodes", maximum(force_work + potential_rate + divergence - coefficient_work) < 1e-9 * scale + 1e-25)
                    face_flux = numerical.array([0.] + [float(graph_current[:cut, cut:].sum()) for cut in range(1, radii.size)] + [0.])
                    verify(tag + "_cut_flux_telescopes_all_cells", maximum(numerical.diff(face_flux) - divergence) < 1e-9 * scale + 1e-25)
                    distances = numerical.abs(numerical.arange(radii.size)[:, None] - numerical.arange(radii.size)[None, :])
                    verify(tag + "_finite_range_no_dense_physical_coupling", maximum(graph_current[distances > 5]) == 0)
                    artifact = destination / (tag + "_transport.npz")
                    numerical.savez_compressed(artifact, radius=radii, coefficient=coefficient, coefficient_time=coefficient_time, nodal_potential=local_potential, graph_current=graph_current, face_flux=face_flux, force_work=force_work, potential_rate=potential_rate, coefficient_work=coefficient_work)
                    report["samples"].append({"case": case_name, "intervals": intervals, "time": time_value, "artifact": artifact.name, "sha256": hashlib.sha256(artifact.read_bytes()).hexdigest(), "U": float(local_potential.sum()), "isolated_Gram_energy_rate": energy_rate, "metric_work_terms": gram_terms[1:].tolist(), "graph_current_max": maximum(graph_current), "face_flux_max": maximum(face_flux), "coefficient_work_max": maximum(coefficient_work), "joint_action_mass_time_correction_zero_in_canonical": case_name == "canonical", "local_Einstein_constraint_claim": False, "valid_for_physics_claim": False})
                    save()
        verify("all18_transport_samples", len(report["samples"]) == 18)
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
