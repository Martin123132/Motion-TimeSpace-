import argparse
import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as numerical
    from annular_coordinate_evolution_operator_20260909 import AnnularFields
    from annular_continuum_initial_data_20260909 import lift
    from annular_coupled_current_operator_20260909 import snapshot_coefficients
    from annular_noether_completion_20260909 import derivative_band
    from annular_boundary_preserving_completion_20260909 import project_interior_scalar_and_complete
    from sbp4_derived_operator_20260909 import derivative
    from sbp4_compatible_second_operator_20260909 import norm_weights
    from annular_volterra_source_completion_20260909 import complete_without_scalar_projection, derivative_moments

    parser = argparse.ArgumentParser()
    parser.add_argument("--tag", default="annular-coupled-current-correction-initial")
    parser.add_argument("--max-grid", type=int, choices=[128, 256, 512], default=256)
    parser.add_argument("--cfl", type=float, default=0.15)
    parser.add_argument("--dissipation", type=float, choices=[0, 1 / 64], default=0)
    parser.add_argument("--source-completion", choices=["projected", "volterra", "discrete_chain"], default="projected")
    parser.add_argument("--initial-kind", choices=["legacy", "second_corner", "third_corner"], default="legacy")
    arguments = parser.parse_args()
    if not arguments.tag or any(character not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789-_" for character in arguments.tag) or not 0 < arguments.cfl <= 0.15:
        raise ValueError("Unsafe output tag or CFL")
    root = Path(__file__).resolve().parents[1]
    intake = root / "source-intake/navier-stokes/20260909"
    destination = intake / arguments.tag
    destination.mkdir(exist_ok=False)
    source = Path(__file__).read_bytes()
    (destination / "executed-script.py").write_bytes(source)
    grids = [arguments.max_grid // 4, arguments.max_grid // 2, arguments.max_grid]
    report = {"state": "running", "started_utc": datetime.now(timezone.utc).isoformat(), "script_sha256": hashlib.sha256(source).hexdigest(), "inputs": {}, "checks": [], "runs": [], "comparisons": [], "valid_for_physics_claim": False, "scope": "Ordinary linearized coupled scalar/mass/lapse correction about the saved approximate parent. Constraint-reduced current formulation, actual nonzero parent defects, fixed continuum initial lift, coupled scalar characteristic boundary and outer lapse boundary. No manufactured solution/forcing, no first-u or full nonlinear claim.", "parameters": {"N": grids, "T": 0.3, "outputs_T": [0.1, 0.3], "epsilon": 0.1, "sigma": 0.05, "cfl": arguments.cfl, "time_interpolation_intervals": 192, "dissipation": 0, "mass_completion": "interior q-source projection, fixed endpoint q/lapse sources, then exact transformation to current h", "constraint_addition": "-f_mu*delta_J-delta_f_mu*J_background retained explicitly"}, "gates": {"spatial_reduction": 1.3, "absolute_refinement_floor": 1e-16, "time_halving_fraction_of_mesh_difference": 0.1, "boundary_relative": 0.01, "boundary_floor": 1e-22, "mass_constraint_fraction_of_background": 0.05, "mass_constraint_floor": 1e-16}}
    report["parameters"]["dissipation"] = arguments.dissipation
    report["parameters"]["filter_scope"] = "Optional existing third-difference Gram filter on coordinate q/lapse before Noether completion. Negative work in the declared unprojected source norm; not proof of negative completed/full coupled work. Vanishes with mesh refinement; not a physical coefficient."
    report["parameters"]["source_completion"] = arguments.source_completion
    report["parameters"]["source_identity_exact_required"] = arguments.source_completion == "projected"
    report["parameters"]["initial_kind"] = arguments.initial_kind
    if arguments.source_completion == "volterra":
        report["parameters"]["mass_completion"] = "Backward cell-exponential Volterra solve: raw q/lapse sources unchanged everywhere, outer mass source zero, nonzero all-row source residual explicitly bounded. Physical/field accuracy gates unchanged; exact source identity is NOT claimed."
    if arguments.source_completion == "discrete_chain":
        from annular_discrete_chain_completion_20260909 import bulk_commutator, chain_coefficients, complete_with_target
        report["parameters"]["mass_completion"] = "Derived full discrete chain correction: N(S)=-K_product, fixed endpoint q/all lapse/outer mass sources. Only the explicit bulk product-rule commutator is canceled; physical background, H*e, forcing derivative error and the constraint itself are retained."
        report["parameters"]["source_residual_quantity"] = "N(S)+K_product, NOT N(S) alone"
        report["parameters"]["full_discrete_chain_identity_required"] = True

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

    def interpolate(cache, time):
        coordinate = time * 640
        first = max(0, min(187, int(math.floor(coordinate)) - 2))
        nodes = numerical.arange(first, first + 6)
        weights = numerical.ones(6)
        for position in range(6):
            for other in range(6):
                if position != other:
                    weights[position] *= (coordinate - nodes[other]) / (nodes[position] - nodes[other])
        return {key: values[first] + numerical.tensordot(weights, values[nodes] - values[first], axes=(0, 0)) for key, values in cache.items()}

    def dot(coefficient, values):
        return numerical.einsum("in,in->n", coefficient, values)

    save()
    try:
        path = intake / "annular-coupled-current-reduction-broadcast/status.json"
        owner = json.loads(path.read_text())
        own(path)
        verify("parent_reduction_derivation_complete", owner["state"] == "complete" and owner["passed"] == owner["total"] and path.with_name("COMPLETE").exists())
        verify("parent_reduction_inputs_unchanged", all(own(root / name) == digest for name, digest in owner["inputs"].items()))
        if arguments.source_completion == "volterra":
            path = intake / "annular-volterra-source-completion-derived/status.json"
            source_owner = json.loads(path.read_text())
            own(path)
            verify("Volterra_source_derivation_complete", source_owner["state"] == "complete" and source_owner["passed"] == source_owner["total"] and path.with_name("COMPLETE").exists())
            verify("Volterra_source_inputs_unchanged", all(own(root / name) == digest for name, digest in source_owner["inputs"].items()))
        own(root / "scripts/annular_volterra_source_completion_20260909.py")
        if arguments.source_completion == "discrete_chain":
            path = intake / "annular-discrete-chain-completion-derived/status.json"
            chain_owner = json.loads(path.read_text())
            own(path)
            verify("discrete_chain_derivation_complete", chain_owner["state"] == "complete" and chain_owner["passed"] == chain_owner["total"] and path.with_name("COMPLETE").exists())
            verify("discrete_chain_derivation_inputs_unchanged", all(own(root / name) == digest for name, digest in chain_owner["inputs"].items()))
        for name in ["run_annular_coupled_current_correction_20260909.py", "annular_continuum_initial_data_20260909.py", "annular_boundary_preserving_completion_20260909.py", "annular_noether_source_projection_20260909.py", "sbp4_derived_operator_20260909.py", "sbp4_compatible_second_operator_20260909.py"]:
            own(root / "scripts" / name)
        initial_directory = {"legacy": "annular-continuum-data-initial", "second_corner": "annular-second-corner-initial-data", "third_corner": "annular-analytic-third-corner-initial-data"}[arguments.initial_kind]
        initial_path = intake / initial_directory / "status.json"
        initial_owner = json.loads(initial_path.read_text())
        own(initial_path)
        verify("initial_data_owner_complete", initial_owner["state"] == "complete" and initial_owner["passed"] == initial_owner["total"] and initial_path.with_name("COMPLETE").exists())
        if arguments.initial_kind == "second_corner":
            from annular_second_corner_initial_data_20260909 import lift
            own(root / "scripts/annular_second_corner_initial_data_20260909.py")
            verify("second_corner_inputs_unchanged", all(own(root / name) == digest for name, digest in initial_owner["inputs"].items()))
        if arguments.initial_kind == "third_corner":
            from annular_third_corner_initial_data_20260909 import lift
            own(root / "scripts/annular_third_corner_initial_data_20260909.py")
            verify("analytic_third_corner_inputs_unchanged", all(own(root / name) == digest for name, digest in initial_owner["inputs"].items()))
        stored = {}
        keys = ["background", "defect", "J0", "old_gradient", "q_gradient", "flux_gradient", "C_gradient", "D_gradient", "V_gradient", "fmu_gradient", "constraint_gradient", "alpha", "B", "c", "P", "Q", "f_mu", "h_mu", "h_delta", "q0", "E"]
        if arguments.source_completion == "discrete_chain":
            keys += ["mass_flux_radial", "velocity_radial", "weighted_flux_radial"]
        for case_name in ["canonical", "nonlinear_modulated"]:
            path = intake / "annular-constraint-correction-initial" / (case_name + ".json")
            own(path)
            evaluator = AnnularFields(json.loads(path.read_text()))
            selected = next(entry for entry in initial_owner["cases"] if entry["case"] == case_name and entry["degree"] == 64)
            path = initial_path.parent / selected["path"]
            verify(case_name + "_frozen_initial_lift", own(path) == selected["sha256"])
            payload = json.loads(path.read_text())
            for intervals in grids:
                label = case_name + "_N" + str(intervals)
                report["active_job"] = label
                save()
                print("Precomputing " + label, flush=True)
                radii = numerical.linspace(4, 8, intervals + 1)
                spacing = float(radii[1] - radii[0])
                weights = spacing * norm_weights(radii.size)
                band = derivative_band(radii.size, spacing)
                outer = derivative(numerical.eye(radii.size), spacing).T[-1]
                source_moments = derivative_moments(radii.size)
                pieces = {key: [] for key in keys}
                independent_defect_error = 0.0
                minimum_alpha, minimum_P, minimum_Q = math.inf, math.inf, math.inf
                maximum_speed = 20.0
                times = numerical.linspace(0, 0.3, 193)
                for first in range(0, len(times), 8):
                    selected_times = times[first:first + 8]
                    snapshot = evaluator.evaluate(selected_times[:, None], radii[None, :], 0.1)
                    current = snapshot_coefficients(snapshot, radii[None, :], evaluator)
                    if arguments.source_completion == "discrete_chain":
                        current.update(chain_coefficients(snapshot, radii[None, :], evaluator))
                    independent_defect_error = max(independent_defect_error, maximum(current["defect"] - current["independent_defect"]))
                    current["defect"] = current["independent_defect"]
                    current["J0"] = snapshot["initial_constraint"][0]
                    for key in keys:
                        pieces[key].append(numerical.moveaxis(current[key], -2, 0))
                    minimum_alpha = min(minimum_alpha, float(numerical.min(current["alpha"])))
                    minimum_P = min(minimum_P, float(numerical.min(current["P"])))
                    minimum_Q = min(minimum_Q, float(numerical.min(current["Q"])))
                    maximum_speed = max(maximum_speed, maximum((numerical.abs(current["B"]) + numerical.sqrt(current["P"] * current["Q"])) / current["alpha"]))
                cache = {key: numerical.concatenate(values, axis=0) for key, values in pieces.items()}
                verify(label + "_independent_offshell_defect", independent_defect_error < 2e-14, {"absolute_difference": independent_defect_error, "stable_residual_source": "frozen exact-jet parent residual transformed to h; not zeroed"})
                verify(label + "_healthy_sampled_branch", min(minimum_alpha, minimum_P, minimum_Q) > 0, {"alpha": minimum_alpha, "P": minimum_P, "Q": minimum_Q})
                for holdout in [0.037123, 0.271234]:
                    snapshot = evaluator.evaluate(numerical.full_like(radii, holdout), radii, 0.1)
                    direct = snapshot_coefficients(snapshot, radii, evaluator)
                    current = interpolate(cache, holdout)
                    error = maximum(current["defect"] - direct["independent_defect"])
                    scale = maximum(direct["independent_defect"])
                    verify(label + "_forcing_interpolation_" + str(holdout), error < 1e-5 * scale + 1e-18, {"error": error, "scale": scale})
                first_current = interpolate(cache, 0)
                initial, initial_radial, unused_second = lift(payload, radii)
                initial = initial[0]
                initial_radial = initial_radial[0]
                lifted = numerical.stack([initial[0], initial_radial[0], first_current["alpha"] * initial[1] - first_current["B"] * initial_radial[0] + first_current["h_mu"] * initial[2] + first_current["h_delta"] * initial[3], initial[2], initial[3]])
                initial_integrability = lifted[1] - derivative(lifted[0], spacing)

                def numerical_source(current, values):
                    velocity = dot(current["q_gradient"], values)
                    fixed_metric_velocity = velocity - current["q0"] * values[4]
                    fixed_metric_gradient = values[1] - evaluator.sigma * current["q0"] * values[4]
                    fixed_metric_flux = current["B"] * fixed_metric_velocity + current["c"] * fixed_metric_gradient
                    impedance = numerical.sqrt(current["P"] * current["Q"])
                    raw = numerical.zeros((1, 4, radii.size))
                    raw[0, 1, 0] = (fixed_metric_flux[0] - impedance[0] * fixed_metric_velocity[0]) / (current["alpha"][0] * weights[0])
                    raw[0, 1, -1] = (-fixed_metric_flux[-1] - impedance[-1] * fixed_metric_velocity[-1]) / (current["alpha"][-1] * weights[-1])
                    raw[0, 3, -1] = -values[4, -1] / (evaluator.sigma * weights[-1])
                    if arguments.dissipation:
                        selected_values = numerical.stack([velocity, values[4]])
                        difference = numerical.diff(selected_values, n=3, axis=-1)
                        adjoint = numerical.zeros_like(selected_values)
                        for offset, coefficient in enumerate([-1, 3, -3, 1]):
                            adjoint[:, offset:offset + difference.shape[-1]] += coefficient * difference
                        source_weight = weights * numerical.stack([radii**2 * current["alpha"], numerical.ones_like(radii)])
                        raw[0, [1, 3]] -= arguments.dissipation * adjoint / source_weight
                    if arguments.source_completion == "volterra":
                        complete, source_diagnostics = complete_without_scalar_projection(raw[0], current["old_gradient"], spacing, moments=source_moments)
                    elif arguments.source_completion == "discrete_chain":
                        target = -bulk_commutator(current, values, spacing, radii)
                        complete, source_diagnostics = complete_with_target(raw[0], current["old_gradient"], band, outer, weights * radii**2 * current["alpha"], target)
                        source_diagnostics.update(bound=numerical.zeros_like(radii), target=target)
                    else:
                        complete = project_interior_scalar_and_complete(raw, current["old_gradient"], band, outer, weights * radii**2 * current["alpha"])[0]
                        source_diagnostics = {"bound": numerical.zeros_like(radii)}
                    transformed = numerical.stack([complete[0], numerical.zeros_like(radii), current["alpha"] * complete[1] + current["h_mu"] * complete[2] + current["h_delta"] * complete[3], complete[2], complete[3]])
                    return transformed, complete, raw[0], source_diagnostics

                def rhs(current, values, diagnostics=False):
                    velocity = dot(current["q_gradient"], values)
                    flux = dot(current["flux_gradient"], values)
                    delta_constraint = derivative(values[3], spacing) - dot(current["constraint_gradient"], values)
                    constraint_force = -current["f_mu"] * delta_constraint - dot(current["fmu_gradient"], values) * current["J0"]
                    result = numerical.stack([velocity, derivative(velocity, spacing), derivative(radii**2 * flux, spacing) / radii**2 - dot(current["V_gradient"], values) + constraint_force, dot(current["C_gradient"], values), (derivative(values[4], spacing) - dot(current["D_gradient"], values)) / evaluator.sigma]) - current["defect"]
                    added, coordinate_added, raw, source_diagnostics = numerical_source(current, values)
                    result += added
                    if not diagnostics:
                        return result
                    full_constraint = current["J0"] + delta_constraint
                    source_constraint = derivative(added[3], spacing) - dot(current["constraint_gradient"], added)
                    target = source_diagnostics.get("target", numerical.zeros_like(radii))
                    return result, {"velocity": velocity, "full_constraint": full_constraint, "constraint_force": constraint_force, "numerical_source": added, "coordinate_numerical_source": coordinate_added, "raw_coordinate_numerical_source": raw, "numerical_constraint_drift": source_constraint - target, "raw_source_constraint": source_constraint, "bulk_product_commutator": -target, "source_residual_bound": source_diagnostics["bound"]}

                for time_refinement in ([1, 2] if intervals == grids[-1] else [1]):
                    tag = label + "_dt" + str(time_refinement)
                    report["active_job"] = tag
                    save()
                    print("Evolving " + tag, flush=True)
                    per_segment = math.ceil(0.1 * maximum_speed * 1.05 / (arguments.cfl * spacing)) * time_refinement
                    timestep = 0.1 / per_segment
                    values = lifted.copy()
                    current = first_current
                    for segment in range(3):
                        for step in range(per_segment):
                            time = segment * 0.1 + step * timestep
                            middle = interpolate(cache, time + timestep / 2)
                            following = interpolate(cache, time + timestep)
                            first_rhs = rhs(current, values)
                            second_rhs = rhs(middle, values + timestep * first_rhs / 2)
                            third_rhs = rhs(middle, values + timestep * second_rhs / 2)
                            fourth_rhs = rhs(following, values + timestep * third_rhs)
                            values += timestep * (first_rhs + 2 * second_rhs + 2 * third_rhs + fourth_rhs) / 6
                            current = following
                        if not numerical.all(numerical.isfinite(values)):
                            raise ValueError("Nonfinite coupled correction")
                        if segment == 1:
                            continue
                        output_time = 0.1 if segment == 0 else 0.3
                        output_tag = tag + "_T" + str(output_time)
                        actual_rhs, diagnostics = rhs(current, values, diagnostics=True)
                        velocity = diagnostics["velocity"]
                        coordinate = numerical.stack([values[0], velocity, values[3], values[4]])
                        impedance = numerical.sqrt(current["P"] * current["Q"])
                        boundary_k = numerical.stack([-(current["B"] - impedance) / current["c"], -(current["B"] + impedance) / current["c"]])
                        indices = [0, -1]
                        slopes = boundary_k[[0, 1], indices]
                        legacy_boundary = values[1, indices] - slopes * velocity[indices]
                        physical_boundary = legacy_boundary + (slopes - evaluator.sigma) * current["q0"][indices] * values[4, indices]
                        boundary_scale = max(maximum(values[1]), maximum(boundary_k * velocity), maximum((boundary_k - evaluator.sigma) * current["q0"] * values[4]), 1e-30)
                        mass_scale = max(maximum(current["J0"]), 1e-30)
                        integrability_change = maximum(values[1] - derivative(values[0], spacing) - initial_integrability)
                        verify(output_tag + "_finite_coupled_fields", numerical.all(numerical.isfinite(coordinate)))
                        verify(output_tag + "_integrability_preserved", integrability_change < 1e-18, {"initial_defect": maximum(initial_integrability), "change": integrability_change})
                        if arguments.source_completion == "volterra":
                            verify(output_tag + "_all_row_source_residual_bound", numerical.all(numerical.abs(diagnostics["numerical_constraint_drift"]) <= diagnostics["source_residual_bound"] + 1e-24), {"residual": maximum(diagnostics["numerical_constraint_drift"]), "bound": maximum(diagnostics["source_residual_bound"]), "exact_zero_claimed": False})
                            verify(output_tag + "_all_scalar_lapse_sources_unchanged", numerical.array_equal(diagnostics["coordinate_numerical_source"][[0, 1, 3]], diagnostics["raw_coordinate_numerical_source"][[0, 1, 3]]))
                        else:
                            verify(output_tag + "_all_row_source_Noether_identity", maximum(diagnostics["numerical_constraint_drift"]) < 1e-19, {"residual": maximum(diagnostics["numerical_constraint_drift"])})
                        verify(output_tag + "_boundary_source_transform", maximum(diagnostics["coordinate_numerical_source"][[1, 3]][:, indices] - diagnostics["raw_coordinate_numerical_source"][[1, 3]][:, indices]) == 0 and abs(diagnostics["numerical_source"][3, -1]) < 1e-24)
                        scalar_gate = maximum(physical_boundary) < 0.01 * boundary_scale + 1e-22
                        lapse_gate = abs(values[4, -1]) < 0.01 * maximum(values[4]) + 1e-22
                        mass_gate = maximum(diagnostics["full_constraint"]) < 0.05 * mass_scale + 1e-16
                        if intervals == grids[-1]:
                            verify(output_tag + "_physical_scalar_boundary_gate", scalar_gate, {"error": maximum(physical_boundary), "scale": boundary_scale, "legacy_boundary_error": maximum(legacy_boundary)})
                            verify(output_tag + "_lapse_boundary_gate", lapse_gate, {"error": abs(float(values[4, -1])), "scale": maximum(values[4])})
                            verify(output_tag + "_mass_constraint_gate", mass_gate, {"error": maximum(diagnostics["full_constraint"]), "background_scale": mass_scale})
                        filename = output_tag + ".npz"
                        numerical.savez(destination / filename, radius=radii, correction_current=values, correction_coordinate=coordinate, current_rhs=actual_rhs, numerical_source=diagnostics["numerical_source"], coordinate_numerical_source=diagnostics["coordinate_numerical_source"], full_mass_constraint=diagnostics["full_constraint"], constraint_force=diagnostics["constraint_force"], background=current["background"], background_defect=current["defect"], physical_boundary=physical_boundary, legacy_boundary=legacy_boundary)
                        residual_filename = output_tag + "_source_residual.npz"
                        numerical.savez(destination / residual_filename, radius=radii, source_constraint_residual=diagnostics["numerical_constraint_drift"], derived_bound=diagnostics["source_residual_bound"], raw_source_constraint=diagnostics["raw_source_constraint"], bulk_product_commutator=diagnostics["bulk_product_commutator"])
                        report["runs"].append({"case": case_name, "intervals": intervals, "time_refinement": time_refinement, "time": output_time, "artifact": filename, "sha256": hashlib.sha256((destination / filename).read_bytes()).hexdigest(), "dt": timestep, "steps": (segment + 1) * per_segment, "coordinate_component_maxima": numerical.max(numerical.abs(coordinate), axis=-1).tolist(), "current_component_maxima": numerical.max(numerical.abs(values), axis=-1).tolist(), "mass_constraint_max": maximum(diagnostics["full_constraint"]), "background_constraint_max": mass_scale, "scalar_boundary_error": maximum(physical_boundary), "legacy_scalar_boundary_error": maximum(legacy_boundary), "scalar_boundary_scale": boundary_scale, "lapse_boundary_error": abs(float(values[4, -1])), "constraint_addition_max": maximum(diagnostics["constraint_force"]), "numerical_source_maxima": numerical.max(numerical.abs(diagnostics["numerical_source"]), axis=-1).tolist(), "scalar_boundary_gate": bool(scalar_gate), "lapse_boundary_gate": bool(lapse_gate), "mass_constraint_gate": bool(mass_gate), "valid_for_physics_claim": False})
                        stored[case_name, intervals, time_refinement, output_time] = coordinate.copy()
                        report["runs"][-1].update(source_residual_artifact=residual_filename, source_residual_sha256=hashlib.sha256((destination / residual_filename).read_bytes()).hexdigest(), source_constraint_residual_max=maximum(diagnostics["numerical_constraint_drift"]), source_residual_bound_max=maximum(diagnostics["source_residual_bound"]), exact_source_identity_claimed=arguments.source_completion == "projected")
                        if arguments.source_completion == "discrete_chain":
                            report["runs"][-1].update(full_discrete_chain_identity_claimed=True, source_residual_quantity="N(S)+K_product", raw_source_constraint_max=maximum(diagnostics["raw_source_constraint"]), bulk_product_commutator_max=maximum(diagnostics["bulk_product_commutator"]))
                        save()
            for output_time in [0.1, 0.3]:
                coarse, medium, fine, half_time = [stored[case_name, intervals, refinement, output_time] for intervals, refinement in [(grids[0], 1), (grids[1], 1), (grids[2], 1), (grids[2], 2)]]
                first_difference = numerical.max(numerical.abs(coarse - medium[:, ::2]), axis=-1)
                second_difference = numerical.max(numerical.abs(medium - fine[:, ::2]), axis=-1)
                time_difference = numerical.max(numerical.abs(fine - half_time), axis=-1)
                spatial_pass = numerical.all(second_difference <= first_difference / 1.3 + 1e-16)
                temporal_pass = numerical.all(time_difference <= 0.1 * second_difference + 1e-16)
                detail = {"coarse_difference": first_difference.tolist(), "fine_difference": second_difference.tolist(), "time_difference": time_difference.tolist()}
                verify(case_name + "_T" + str(output_time) + "_spatial_refinement", spatial_pass, detail)
                verify(case_name + "_T" + str(output_time) + "_temporal_refinement", temporal_pass, detail)
                report["comparisons"].append({"case": case_name, "time": output_time, "spatial_pass": bool(spatial_pass), "temporal_pass": bool(temporal_pass), **detail})
        verify("all_expected_outputs_saved", len(report["runs"]) == 16 and len(report["comparisons"]) == 4)
        verify("metric_corrections_evolved_not_prescribed", all(entry["coordinate_component_maxima"][2] > 0 and entry["coordinate_component_maxima"][3] > 0 for entry in report["runs"]))
        compile(Path(__file__).read_bytes(), str(Path(__file__)), "exec")
        verify("no_bytecode_cache", not (root / "scripts/__pycache__").exists())
        report.update(passed=sum(check["passed"] for check in report["checks"]), total=len(report["checks"]), completed_utc=datetime.now(timezone.utc).isoformat(), active_job=None)
        report["state"] = "complete" if report["passed"] == report["total"] else "failed"
        save()
    except Exception as error:
        report.update(state="failed", failure=repr(error), completed_utc=datetime.now(timezone.utc).isoformat())
        save()
        raise
    print(json.dumps({key: value for key, value in report.items() if key not in {"inputs", "checks", "runs", "comparisons"}}, indent=2), flush=True)
    if report["state"] != "complete":
        raise SystemExit(1)
    (destination / "COMPLETE").write_text(report["completed_utc"] + "\n")


if __name__ == "__main__":
    run()
