import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as numerical
    import sympy as symbolic
    from annular_clock_connection_20260909 import ScalarReferenceClockProfile, clock_from_connection, clock_hessian, clock_offsets, clock_remainder_bound, exact_clock_potential, graph_flux, quadratic_clock_potential
    from annular_coordinate_evolution_operator_20260909 import AnnularFields
    from annular_gram_joint_action_20260909 import coefficient_jets, coefficient_pairing, gram_matrices, remainder

    root = Path(__file__).resolve().parents[1]
    intake = root / "source-intake/navier-stokes/20260909"
    destination = intake / "annular-clock-coframe-current-derived"
    destination.mkdir(exist_ok=False)
    source = Path(__file__).read_bytes()
    (destination / "executed-script.py").write_bytes(source)
    report = {"state": "running", "started_utc": datetime.now(timezone.utc).isoformat(), "script_sha256": hashlib.sha256(source).hexdigest(), "inputs": {}, "checks": [], "samples": [], "valid_for_physics_claim": False, "scope": "Derive the missing Gram energy-current covector from an explicit relative clock/coframe action germ, not by inserting a flux. Actual canonical/nonlinear parent reference profiles and changing coefficients. First local-clock Ward identity, full clock Hessian, bounded Taylor remainder and isolated metric-gradient source normalization. Still no unified face/nodal gravitational action, fully background-covariant finite link transport, physical boundary coupling or evolution. a is a time-density, not a separately delayed scalar.", "formula": "omega_li=S_li a_i/(Sa)_l, theta_li=xi_i-sum_j omega_lj xi_j. U_clock=sum_l (Sa)_l [sum_i T_li chi_i(t-theta_li)]^2/(2h). At xi=0, U_xi=-div J and U_Aedge=h J_cut when Delta xi=h Delta A. With A=g_tR/g_tt=sigma-1/(EF), (F partial_delta+rF^2 partial_mu-2 partial_beta)A=-1/E. Thus isolated connection covector gives the previously derived -kappa J_cut/E with face gravity normalization kappa/h, conditional on a consistent face geometry action."}

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
        own(root / "scripts/annular_clock_connection_20260909.py")
        previous_path = intake / "annular-joint-action-transport-final-integrity.json"
        own(previous_path)
        previous = json.loads(previous_path.read_text())
        verify("previous_goal_turn_verified_progress", previous["state"] == "complete" and previous["output_hashes"] == 30 and previous["compiled_scripts"] == 6)
        verify("previous_immutable_sources_and_outputs_unchanged", all(own(root / name) == digest for name, digest in {**previous["inputs"], **previous["outputs"]}.items()))
        velocity, gradient, exponential, lapse, radius, sigma_symbol, quartic, sextic = symbolic.symbols("q w E F r sigma b2 b3", nonzero=True, real=True)
        radial = gradient - sigma_symbol * velocity
        physical_time = velocity / exponential
        kinetic = 2 * physical_time * radial + lapse * radial**2
        principal = 1 - 4 * quartic * kinetic - 6 * sextic * kinetic**2
        slope, second_slope = -4 * quartic - 12 * sextic * kinetic, -12 * sextic
        raised = physical_time + lapse * radial
        coefficient = radius**2 * exponential * (lapse * principal + 2 * slope * raised**2)
        beta_derivative = radius**2 * exponential * (-lapse**2 * principal / 2 - 4 * lapse * slope * raised**2 - 2 * second_slope * raised**4)
        velocity_derivative, gradient_derivative, exponential_derivative, lapse_derivative = [symbolic.diff(coefficient, variable) for variable in [velocity, gradient, exponential, lapse]]
        time_density = velocity * velocity_derivative - 2 * sigma_symbol * exponential * lapse**2 * lapse_derivative + (1 + sigma_symbol * exponential * lapse) * exponential * exponential_derivative - 2 * sigma_symbol * exponential * beta_derivative
        radial_scalar = velocity * gradient_derivative + 2 * exponential * lapse**2 * lapse_derivative - exponential**2 * lapse * exponential_derivative + 2 * exponential * beta_derivative
        verify("symbolic_nonlinear_principal_is_time_density", symbolic.factor(time_density - coefficient) == 0)
        verify("symbolic_nonlinear_spatial_clock_gradient_cancels", symbolic.factor(radial_scalar) == 0)
        metric_generator = lapse * exponential * exponential_derivative - 2 * lapse**2 * lapse_derivative - 2 * beta_derivative
        verify("symbolic_existing_metric_source_is_qUw_over_E", symbolic.factor(metric_generator - velocity * gradient_derivative / exponential) == 0)
        connection = sigma_symbol - 1 / (exponential * lapse)
        connection_generator = lapse * exponential * symbolic.diff(connection, exponential) - 2 * lapse**2 * symbolic.diff(connection, lapse)
        verify("symbolic_connection_metric_generator_normalization", symbolic.simplify(connection_generator + 1 / exponential) == 0)
        prior_transport_path = intake / "annular-Gram-energy-transport-derived/status.json"
        own(prior_transport_path)
        prior_transport = json.loads(prior_transport_path.read_text())
        for case_name in ["canonical", "nonlinear_modulated"]:
            case_path = intake / "annular-constraint-correction-initial" / (case_name + ".json")
            own(case_path)
            case = json.loads(case_path.read_text())
            evaluator = AnnularFields(case)
            profile = ScalarReferenceClockProfile(case)
            constants, sigma, kappa = evaluator.constants, evaluator.sigma, evaluator.kappa
            for intervals in [32, 64, 128]:
                radii = numerical.linspace(4, 8, intervals + 1)
                spacing = 4 / intervals
                factors, sampling = gram_matrices(radii.size)
                first_clock = numerical.sin(1.3 * radii) + 0.2 * numerical.cos(2.1 * radii)
                second_clock = numerical.cos(0.7 * radii) - 0.1 * numerical.sin(3 * radii)
                for time_value in [0.1, 0.15, 0.2]:
                    tag = case_name + "_N" + str(intervals) + "_T" + str(time_value)
                    report["active_job"] = tag
                    save()
                    snapshot = evaluator.evaluate(numerical.full_like(radii, time_value), radii, 0.1)
                    state = snapshot["state"][0]
                    primitive = numerical.stack([state[0], state[1], snapshot["state_space"][0, 0], state[2], state[3], numerical.zeros_like(radii)])
                    coefficient, coefficient_gradient, coefficient_hessian = coefficient_jets(primitive, radii, constants, sigma)
                    scalar, velocity, acceleration = [profile.evaluate(time_value, radii, order) for order in range(3)]
                    verify(tag + "_independent_parent_time_profiles", maximum(scalar - state[0]) < 1e-12 and maximum(velocity - state[1]) < 1e-12 and maximum(acceleration - snapshot["state_time"][0, 1]) < 1e-10)
                    tangent = numerical.stack([snapshot["state_time"][0, 1], snapshot["state_space"][0, 1], snapshot["state_time"][0, 2], snapshot["state_time"][0, 3], numerical.zeros_like(radii)])
                    coefficient_time = numerical.sum(coefficient_gradient * tangent, axis=0)
                    graph, faces = graph_flux(scalar, velocity, coefficient, spacing)
                    divergence = graph.sum(axis=1)
                    offsets, factor_coefficient, allocation = clock_offsets(coefficient, first_clock)
                    verify(tag + "_energy_weighted_clock_partition", numerical.all(allocation >= 0) and maximum(allocation.sum(axis=1) - 1) < 1e-14)
                    factor_q = factors @ velocity
                    factor_scalar = factors @ scalar
                    clock_covector = -velocity * (factors.T @ (factor_coefficient * factor_scalar) / spacing) + allocation.T @ (factor_coefficient * factor_scalar * factor_q / spacing)
                    scale = max(maximum(clock_covector), maximum(divergence), 1e-25)
                    verify(tag + "_clock_variation_equals_local_energy_current", maximum(clock_covector + divergence) < 1e-9 * scale + 1e-24)
                    edge_covector = spacing * numerical.cumsum(clock_covector[::-1])[::-1][1:]
                    verify(tag + "_every_edge_covector_is_h_times_cut_flux", maximum(edge_covector - spacing * faces[1:-1]) < 1e-9 * max(maximum(edge_covector), spacing * maximum(faces), 1e-25) + 1e-24)
                    for direction_index, direction in enumerate([first_clock, second_clock, numerical.ones_like(radii)]):
                        measured = quadratic_clock_potential(scalar, velocity, acceleration, coefficient, 1j * 1e-25 * direction, spacing).imag / 1e-25
                        expected = numerical.dot(clock_covector, direction)
                        tolerance = 1e-8 * max(abs(measured), abs(expected), scale * maximum(direction), 1e-25) + 1e-24
                        verify(tag + "_independent_clock_gradient_" + str(direction_index), abs(measured - expected) < tolerance)
                    constant_clock = numerical.full_like(radii, 0.001)
                    zero = numerical.zeros_like(radii)
                    verify(tag + "_common_clock_shift_is_exact_germ_symmetry", abs(quadratic_clock_potential(scalar, velocity, acceleration, coefficient, constant_clock, spacing) - quadratic_clock_potential(scalar, velocity, acceleration, coefficient, zero, spacing)) < 1e-11 * max(abs(quadratic_clock_potential(scalar, velocity, acceleration, coefficient, zero, spacing)), 1e-30))
                    epsilon_clock = first_clock
                    epsilon_time = 0.3 * second_clock
                    density_variation = epsilon_clock * coefficient_time + epsilon_time * coefficient
                    varied_coefficient = coefficient.astype(complex) + 1j * 1e-25 * density_variation
                    varied_scalar = scalar.astype(complex) + 1j * 1e-25 * epsilon_clock * velocity
                    varied_velocity = velocity.astype(complex) + 1j * 1e-25 * (epsilon_clock * acceleration + epsilon_time * velocity)
                    measured_ward = quadratic_clock_potential(varied_scalar, varied_velocity, acceleration, varied_coefficient, 1j * 1e-25 * epsilon_clock, spacing).imag / 1e-25
                    density = coefficient_pairing(scalar, scalar, spacing) / 2
                    density_time = coefficient_pairing(scalar, velocity, spacing)
                    ward_terms = numerical.stack([epsilon_clock * coefficient * density_time, epsilon_clock * coefficient_time * density, epsilon_time * coefficient * density])
                    expected_ward = float(ward_terms.sum())
                    verify(tag + "_local_clock_Ward_with_metric_work", abs(measured_ward - expected_ward) < 1e-8 * max(abs(measured_ward), abs(expected_ward), float(numerical.sum(numerical.abs(ward_terms))), 1e-25) + 1e-22)
                    hessian = clock_hessian(scalar, velocity, acceleration, coefficient, first_clock, second_clock, spacing)
                    swapped = clock_hessian(scalar, velocity, acceleration, coefficient, second_clock, first_clock, spacing)
                    verify(tag + "_full_clock_Hessian_symmetry", abs(hessian - swapped) < 1e-10 * max(abs(hessian), 1e-25) + 1e-23)
                    hessian_errors = []
                    for step in [0.001, 0.0005]:
                        values = [quadratic_clock_potential(scalar, velocity, acceleration, coefficient, step * (first_sign * first_clock + second_sign * second_clock), spacing) for first_sign, second_sign in [(1, 1), (1, -1), (-1, 1), (-1, -1)]]
                        measured = (values[0] - values[1] - values[2] + values[3]) / (4 * step**2)
                        tolerance = 1e-9 * max(abs(hessian), 1e-25) + 256 * numerical.finfo(float).eps * max(abs(value) for value in values) / step**2
                        hessian_errors.append(float(abs(measured - hessian)))
                        verify(tag + "_independent_clock_Hessian_FD_" + str(step), abs(measured - hessian) <= tolerance)
                    remainder_results = []
                    for size in [0.001, 0.0005]:
                        clock = size * first_clock
                        exact = exact_clock_potential(profile, time_value, radii, coefficient, clock, spacing)
                        germ = quadratic_clock_potential(scalar, velocity, acceleration, coefficient, clock, spacing)
                        bound, arithmetic_scale, max_shift = clock_remainder_bound(profile, time_value, radii, coefficient, clock, spacing)
                        roundoff = 256 * numerical.finfo(float).eps * arithmetic_scale
                        verify(tag + "_analytic_clock_remainder_bound_" + str(size), abs(exact - germ) <= bound + roundoff)
                        remainder_results.append({"clock_amplitude": size, "max_actual_time_shift": max_shift, "error": float(abs(exact - germ)), "analytic_bound": bound, "floating_allowance": roundoff, "interval_certified": False})
                    face_radii = (radii[:-1] + radii[1:]) / 2
                    face_snapshot = evaluator.evaluate(numerical.full_like(face_radii, time_value), face_radii, 0.1)
                    face_mass, face_delta = face_snapshot["state"][0, 2:4]
                    face_exponential = numerical.exp(face_delta)
                    face_lapse = 1 - 2 * face_mass / face_radii - constants["Lambda"] * face_radii**2 / 3
                    verify(tag + "_time_connection_branch_is_regular", numerical.all(face_lapse > 0) and numerical.all(face_exponential > 0))
                    connection = sigma - 1 / (face_exponential * face_lapse)
                    direction = numerical.cos(1.1 * face_radii)
                    varied_mass = face_mass.astype(complex) + 1j * 1e-25 * face_radii * face_lapse**2 * direction
                    varied_exponential = numerical.exp(face_delta.astype(complex) + 1j * 1e-25 * face_lapse * direction)
                    varied_lapse = 1 - 2 * varied_mass / face_radii - constants["Lambda"] * face_radii**2 / 3
                    varied_connection = sigma - 1 / (varied_exponential * varied_lapse)
                    varied_clock = clock_from_connection(varied_connection - connection, numerical.diff(radii))
                    measured = quadratic_clock_potential(scalar, velocity, acceleration, coefficient, varied_clock, spacing).imag / 1e-25
                    expected = -numerical.sum(spacing * faces[1:-1] * direction / face_exponential)
                    verify(tag + "_metric_generator_produces_derived_flux_covector", abs(measured - expected) <= 1e-8 * max(abs(expected), spacing * maximum(faces), 1e-25) + 1e-23)
                    if time_value == 0.1:
                        old_entry = next(row for row in prior_transport["samples"] if row["case"] == case_name and row["intervals"] == intervals and row["time"] == time_value)
                        old_path = prior_transport_path.parent / old_entry["artifact"]
                        verify(tag + "_prior_transport_array_hash", own(old_path) == old_entry["sha256"])
                        with numerical.load(old_path, allow_pickle=False) as old:
                            verify(tag + "_same_previously_derived_flux", maximum(faces - old["face_flux"]) < 1e-8 * max(maximum(faces), 1e-25) + 1e-22)
                    artifact = destination / (tag + "_clock_coframe.npz")
                    numerical.savez_compressed(artifact, radius=radii, coefficient=coefficient, coefficient_time=coefficient_time, scalar=scalar, velocity=velocity, acceleration=acceleration, clock_covector=clock_covector, graph_current=graph, face_flux=faces, edge_covector=edge_covector, face_radius=face_radii, face_exponential=face_exponential, connection=connection, isolated_connection_mass_source=-kappa * faces[1:-1] / face_exponential)
                    report["samples"].append({"case": case_name, "intervals": intervals, "time": time_value, "artifact": artifact.name, "sha256": hashlib.sha256(artifact.read_bytes()).hexdigest(), "face_flux_max": maximum(faces), "coefficient_time_max": maximum(coefficient_time), "retained_coefficient_work_max": maximum(density * coefficient_time), "clock_Hessian_pair": float(hessian), "clock_Hessian_FD_errors": hessian_errors, "remainder_checks": remainder_results, "face_geometry_sampled_from_actual_parent_not_interpolated": True, "isolated_connection_current_only": True, "full_face_metric_action_signed": False, "valid_for_physics_claim": False})
                    save()
        verify("all18_clock_coframe_samples", len(report["samples"]) == 18)
        verify("no_bytecode_cache", not (root / "scripts/__pycache__").exists())
        for path in [Path(__file__), root / "scripts/annular_clock_connection_20260909.py"]:
            compile(path.read_bytes(), str(path), "exec")
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
