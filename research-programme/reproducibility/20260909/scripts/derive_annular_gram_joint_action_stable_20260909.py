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
    from annular_conservative_scalar_evolution_20260909 import constitutive
    from annular_gram_joint_action_20260909 import action, coefficient_jets, coefficient_pairing, gram_matrices, matter_values, potential, potential_gradient, principal_coefficient, remainder
    from annular_gram_stable_hessian_20260909 import potential_hessian_pair
    from sbp4_compatible_second_operator_20260909 import gram_parts, norm_weights, remainder_action
    from sbp4_derived_operator_20260909 import derivative

    root = Path(__file__).resolve().parents[1]
    intake = root / "source-intake/navier-stokes/20260909"
    destination = intake / "annular-Gram-joint-action-stable"
    destination.mkdir(exist_ok=False)
    source = Path(__file__).read_bytes()
    (destination / "executed-script.py").write_bytes(source)
    report = {"state": "running", "started_utc": datetime.now(timezone.utc).isoformat(), "script_sha256": hashlib.sha256(source).hexdigest(), "inputs": {}, "checks": [], "samples": [], "hessian_tests": [], "valid_for_physics_claim": False, "scope": "Full Gram field variation on the actual canonical/nonlinear annular backgrounds, and a specified proposed semidiscrete action germ through first off-gauge metric order. Exact virtual-work and global time-energy identities, not a local discrete Bianchi proof or evolved replacement. All endpoint covectors retained. Probe time paths freeze I=w-Dchi at that probe; they are arbitrary paths, not an evolved parent trajectory. Natural beta extension of the coefficient is specified rather than claimed uniquely derived from the parent."}

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
        legacy_path = intake / "annular-Gram-joint-action-derived/status.json"
        own(legacy_path)
        legacy = json.loads(legacy_path.read_text())
        verify("original_four_numeric_symmetry_failures_preserved", legacy["state"] == "failed" and legacy["passed"] == 670 and legacy["total"] == 674 and not legacy_path.with_name("COMPLETE").exists() and all("Hessian_symmetry" in check["name"] for check in legacy["checks"] if not check["passed"]))
        own(root / "scripts/annular_gram_stable_hessian_20260909.py")
        previous_path = intake / "annular-compatible-current-final-integrity.json"
        own(previous_path)
        previous = json.loads(previous_path.read_text())
        verify("previous_goal_turn_is_verified_progress", previous["state"] == "complete" and previous["compiled_scripts"] == 10 and previous["output_hashes"] == 148)
        immutable_inputs = {name: digest for name, digest in previous["inputs"].items() if name != "CURRENT_LOCAL_RESUME.md"}
        verify("previous_immutable_inputs_and_outputs_unchanged", all(own(root / name) == digest for name, digest in {**immutable_inputs, **previous["outputs"]}.items()))
        for name in ["annular_gram_joint_action_20260909.py", "annular_coordinate_evolution_operator_20260909.py", "annular_evolution_operator_20260909.py", "annular_conservative_scalar_evolution_20260909.py", "sbp4_compatible_second_operator_20260909.py", "sbp4_derived_operator_20260909.py"]:
            own(root / "scripts" / name)
        advanced, radius, theta, phi = symbolic.symbols("v r theta phi", real=True)
        coordinates = [advanced, radius, theta, phi]
        mass = symbolic.Function("mu")(advanced, radius)
        shift = symbolic.Function("delta")(advanced, radius)
        cosmological = symbolic.symbols("Lambda", real=True)
        exponential = symbolic.exp(shift)
        lapse = 1 - 2 * mass / radius - cosmological * radius**2 / 3
        metric = symbolic.Matrix([[-exponential**2 * lapse, exponential, 0, 0], [exponential, 0, 0, 0], [0, 0, radius**2, 0], [0, 0, 0, radius**2 * symbolic.sin(theta)**2]])
        inverse = metric.inv()
        connection = {}
        for upper in range(4):
            for first in range(4):
                for second in range(4):
                    connection[upper, first, second] = symbolic.simplify(sum(inverse[upper, lower] * (symbolic.diff(metric[lower, second], coordinates[first]) + symbolic.diff(metric[lower, first], coordinates[second]) - symbolic.diff(metric[first, second], coordinates[lower])) for lower in range(4)) / 2)
        ricci = symbolic.zeros(4)
        for first in range(4):
            for second in range(first, 4):
                value = sum(symbolic.diff(connection[upper, first, second], coordinates[upper]) - symbolic.diff(connection[upper, first, upper], coordinates[second]) + sum(connection[upper, first, second] * connection[lower, upper, lower] - connection[lower, first, upper] * connection[upper, second, lower] for lower in range(4)) for upper in range(4))
                ricci[first, second] = ricci[second, first] = symbolic.simplify(value)
        scalar_curvature = symbolic.simplify(sum(inverse[first, second] * ricci[first, second] for first in range(4) for second in range(4)))
        einstein = ricci - metric * scalar_curvature / 2 + cosmological * metric
        raised_rr = symbolic.simplify((inverse * einstein * inverse)[1, 1])
        expected_rr = 2 * symbolic.diff(mass, advanced) / (exponential * radius**2) - 2 * lapse * symbolic.diff(mass, radius) / radius**2 + 2 * lapse**2 * symbolic.diff(shift, radius) / radius
        verify("independent_4D_Einstein_off_gauge_coefficient", symbolic.simplify(raised_rr - expected_rr) == 0)
        report["gravity_beta_coefficient"] = "[-mu_t+E F(mu_R-sigma mu_t)-r F^2(E_R-sigma E delta_t)]/(2 kappa); follows from -E r^2 (G^{rr}+Lambda g^{rr})/(4 kappa). Linear beta germ only; endpoint total derivatives must be accounted for."
        test_radius = numerical.linspace(4, 8, 33)
        for coefficient in [1 + 0.1 * test_radius, numerical.cos(2 * test_radius)]:
            test_scalar = numerical.sin(3 * test_radius)
            factors, sampling = gram_matrices(test_radius.size)
            test_remainder = remainder(test_scalar, coefficient, 0.125)
            verify("Gram_signed_bilinear_duality_" + str(coefficient[0]), abs(numerical.dot(coefficient, coefficient_pairing(test_scalar, test_scalar, 0.125)) - numerical.dot(test_scalar, test_remainder)) < 1e-12)
            if numerical.all(coefficient > 0):
                verify("independent_positive_Gram_action", maximum(test_remainder - remainder_action(test_scalar, gram_parts(test_scalar.size, coefficient)) / 0.125) < 1e-12)
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
                for time_value in [0, 0.1, 0.3]:
                    tag = case_name + "_N" + str(intervals) + "_T" + str(time_value)
                    report["active_job"] = tag
                    save()
                    snapshot = evaluator.evaluate(numerical.full_like(radii, time_value), radii, 0.1)
                    state = snapshot["state"][0]
                    primitive = numerical.stack([state[0], state[1], snapshot["state_space"][0, 0], state[2], state[3], numerical.zeros_like(radii)])
                    mass_time, shift_time = snapshot["state_time"][0, 2:4]
                    integrability = primitive[2] - derivative_matrix @ primitive[0]
                    coefficient, coefficient_gradient, coefficient_hessian = coefficient_jets(primitive, radii, constants, sigma)
                    exponential, lapse, unused_det, radial, physical_time, kinetic, lagrangian, principal = matter_values(primitive, radii, constants, sigma)
                    current = constitutive(primitive[1], primitive[2], exponential, lapse, constants, sigma)
                    verify(tag + "_actual_constitutive_coefficient", maximum(coefficient - radii**2 * current["c"]) <= 1e-12 * maximum(coefficient))
                    verify(tag + "_healthy_sampled_branch", numerical.all(coefficient > 0) and numerical.all(current["alpha"] > 0))
                    dual = coefficient_pairing(primitive[0], primitive[0], spacing) / 2
                    potential_grad = potential_gradient(primitive, radii, constants, sigma, spacing)
                    directions = []
                    for component in range(6):
                        direction = numerical.zeros_like(primitive)
                        direction[component] = 0.1 * numerical.cos((component + 1) * radii + 0.3)
                        directions.append(direction)
                        varied = primitive.astype(complex) + 1j * 1e-25 * direction
                        measured = potential(varied, radii, constants, sigma, spacing).imag / 1e-25
                        expected = numerical.sum(potential_grad * direction)
                        verify(tag + "_potential_gradient_complex_" + str(component), abs(measured - expected) <= 1e-9 * max(abs(measured), abs(expected), 1e-24) + 1e-24)
                        if component:
                            measured_coefficient = principal_coefficient(varied, radii, constants, sigma).imag / 1e-25
                            verify(tag + "_coefficient_gradient_complex_" + str(component), maximum(measured_coefficient - coefficient_gradient[component - 1] * direction[component]) <= 1e-10 * max(maximum(coefficient), 1))
                    for first_index, second_index in [(0, 0), (0, 3), (3, 4), (1, 1), (4, 5)]:
                        first, second = directions[first_index], directions[second_index]
                        value, terms = potential_hessian_pair(primitive, first, second, radii, constants, sigma, spacing)
                        swapped = potential_hessian_pair(primitive, second, first, radii, constants, sigma, spacing)[0]
                        verify(tag + "_Hessian_symmetry_" + str((first_index, second_index)), abs(value - swapped) < 1e-11 * max(maximum(terms), 1e-25))
                        errors = []
                        for step in [0.001, 0.0005]:
                            samples = [potential(primitive + first_sign * step * first + second_sign * step * second, radii, constants, sigma, spacing) for first_sign, second_sign in [(1, 1), (1, -1), (-1, 1), (-1, -1)]]
                            measured = (samples[0] - samples[1] - samples[2] + samples[3]) / (4 * step**2)
                            tolerance = 1e-4 * max(maximum(terms), 1e-30) + 100 * numerical.finfo(float).eps * max(abs(sample) for sample in samples) / step**2
                            errors.append(float(abs(measured - value)))
                            verify(tag + "_independent_Hessian_FD_" + str((first_index, second_index, step)), abs(measured - value) <= tolerance)
                        report["hessian_tests"].append({"case": case_name, "intervals": intervals, "time": time_value, "directions": [first_index, second_index], "full_Hessian": float(value), "four_terms": terms.tolist(), "FD_errors": errors})
                    if case_name == "canonical":
                        verify(tag + "_canonical_metric_variations", maximum(coefficient_gradient[2] + 2 * radii * exponential) < 1e-12 and maximum(coefficient_gradient[3] - coefficient) < 1e-12 and maximum(coefficient_gradient[4] + radii**2 * exponential * lapse**2 / 2) < 1e-12 and maximum(coefficient_gradient[:2]) == 0)
                    mass_radial = derivative_matrix @ primitive[3] - sigma * mass_time
                    exponential_radial = derivative_matrix @ exponential - sigma * exponential * shift_time
                    expected_gradient = numerical.zeros_like(primitive)
                    expected_gradient[0] = -weights * radii**2 * exponential * constants["m_chi"]**2 * primitive[0] - derivative_matrix.T @ (weights * radii**2 * current["flux"]) - potential_grad[0] - derivative_matrix.T @ potential_grad[2]
                    expected_gradient[1] = weights * radii**2 * current["momentum"] - potential_grad[1]
                    expected_gradient[3] = derivative_matrix.T @ (weights * exponential) / kappa + weights * radii * exponential * principal * radial**2 - potential_grad[3]
                    expected_gradient[4] = weights * exponential * mass_radial / kappa + weights * radii**2 * exponential * (lagrangian + principal * physical_time * radial) - potential_grad[4]
                    expected_gradient[5] = weights * (-mass_time + exponential * lapse * mass_radial - radii * lapse**2 * exponential_radial) / (2 * kappa) + weights * radii**2 * exponential * (lapse * lagrangian + principal * (physical_time + lapse * radial)**2) / 2 - potential_grad[5]
                    for component in [0, 1, 3, 4, 5]:
                        varied = primitive.astype(complex) + 1j * 1e-25 * directions[component]
                        measured = action(varied, mass_time, shift_time, radii, constants, sigma, kappa, weights, derivative_matrix, integrability).imag / 1e-25
                        expected = numerical.sum(expected_gradient * directions[component])
                        verify(tag + "_full_action_virtual_work_" + str(component), abs(measured - expected) <= 1e-9 * max(abs(measured), abs(expected), 1e-15) + 1e-14)
                    time_direction = numerical.sin(radii)
                    measured = action(primitive.astype(complex), mass_time + 1j * 1e-25 * time_direction, shift_time, radii, constants, sigma, kappa, weights, derivative_matrix, integrability).imag / 1e-25
                    verify(tag + "_gravitational_momentum", abs(measured + numerical.sum(sigma * weights * exponential * time_direction / kappa)) < 1e-12)
                    kinetic_diagonal = weights * radii**2 * current["alpha"] - dual * coefficient_hessian[0, 0]
                    verify(tag + "_sampled_modified_Legendre_positive", numerical.all(kinetic_diagonal > 0))
                    base_radial_mass = -kappa * radii**2 * (lagrangian + principal * physical_time * radial)
                    base_lapse = kappa * radii * principal * radial**2
                    corrected_mass_radial = base_radial_mass + kappa * potential_grad[4] / (weights * exponential)
                    corrected_exponential_radial = exponential * base_lapse - kappa * potential_grad[3] / weights
                    eliminated_time = exponential * lapse * corrected_mass_radial - radii * lapse**2 * corrected_exponential_radial + kappa * exponential * radii**2 * (lapse * lagrangian + principal * (physical_time + lapse * radial)**2) - 2 * kappa * potential_grad[5] / weights
                    base_mass_time = kappa * radii**2 * primitive[1] * current["flux"] / exponential
                    derived_mass_source = kappa * (lapse * potential_grad[4] + radii * lapse**2 * potential_grad[3] - 2 * potential_grad[5]) / weights
                    verify(tag + "_joint_metric_equation_elimination", maximum(eliminated_time - base_mass_time - derived_mass_source) <= 1e-11 * max(maximum(base_mass_time), maximum(derived_mass_source), 1e-20))
                    if case_name == "canonical":
                        verify(tag + "_canonical_mass_time_correction_cancels", maximum(derived_mass_source) < 1e-12 * max(maximum(potential_grad[4] / weights), 1e-30))
                    report["samples"].append({"case": case_name, "intervals": intervals, "time": time_value, "U": float(potential(primitive, radii, constants, sigma, spacing)), "energy_addition_U_minus_qUq": float(potential(primitive, radii, constants, sigma, spacing) - numerical.sum(primitive[1] * potential_grad[1])), "minimum_modified_kinetic_diagonal": float(numerical.min(kinetic_diagonal)), "relative_kinetic_change_max": maximum(dual * coefficient_hessian[0, 0] / (weights * radii**2 * current["alpha"])), "lapse_source_change_max": maximum(kappa * potential_grad[3] / (weights * exponential)), "mass_radial_source_change_max": maximum(kappa * potential_grad[4] / (weights * exponential)), "mass_time_source_change_max": maximum(derived_mass_source), "integrability_defect_max": maximum(integrability), "parent_defect_max": maximum(snapshot["defect"][0]), "local_discrete_Noether_claim": False, "evolved": False, "valid_for_physics_claim": False})
                    save()
        verify("all18_background_samples_and90_Hessian_pairs", len(report["samples"]) == 18 and len(report["hessian_tests"]) == 90)
        verify("no_bytecode_cache", not (root / "scripts/__pycache__").exists())
        for name in [Path(__file__), root / "scripts/annular_gram_joint_action_20260909.py"]:
            compile(name.read_bytes(), str(name), "exec")
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
