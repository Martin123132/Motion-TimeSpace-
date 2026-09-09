import argparse
import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as numerical
    from annular_coordinate_evolution_operator_20260909 import AnnularFields
    from annular_coupled_current_time_jets_20260909 import series_dot
    from annular_projected_volterra_time_jets_20260909 import integrate_source_time_coefficients
    from annular_compatible_current_time_jets_20260909 import CompatibleCurrentTimeJets
    from annular_compatible_current_rhs_20260909 import compatible_current_rhs
    from annular_compatible_current_restoring_20260909 import signed_remainder_action, restoring_time_coefficients
    from sbp4_compatible_second_operator_20260909 import gram_parts, remainder_action
    from annular_volterra_source_completion_20260909 import complete_without_scalar_projection
    from annular_boundary_preserving_completion_20260909 import project_interior_scalar_and_complete
    from annular_volterra_source_completion_20260909 import integrate_source, residual_bound
    from annular_correction_time_jets_20260909 import constant
    from sbp4_derived_operator_20260909 import derivative

    root = Path(__file__).resolve().parents[1]
    intake = root / "source-intake/navier-stokes/20260909"
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=["preflight", "trajectory"], default="preflight")
    arguments = parser.parse_args()
    destination = intake / ("annular-compatible-current-time-jets-" + arguments.mode)
    destination.mkdir(exist_ok=False)
    source = Path(__file__).read_bytes()
    (destination / "executed-script.py").write_bytes(source)
    report = {"state": "running", "started_utc": datetime.now(timezone.utc).isoformat(), "script_sha256": hashlib.sha256(source).hexdigest(), "inputs": {}, "checks": [], "runs": [], "valid_for_physics_claim": False, "scope": "Compatible Gram restoring source plus raw scalar/lapse SAT on SAME C3 data. Differentiate signed Gram time coefficients with fixed edge orientations, then complete ALL sources with Volterra. No global scalar projection. Differentiate the actual cell-exponential recurrence through time degree2, then actual RHS through derivative3. Diagnostic trajectory replay retains any failed field gates; numerical time-jet validation is not field acceptance. Nonzero source Noether residual retained, not exact source identity or physical claim."}

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

    def direct_rhs(engine, offset, state):
        current = {key: values[0] for key, values in engine.interpolate(offset).items()}
        return compatible_current_rhs(current, state, engine.radii, engine.weights, engine.spacing, engine.evaluator.sigma)

    save()
    try:
        path = intake / "annular-compatible-current-restoring-source-derived/status.json"
        own(path)
        static_owner = json.loads(path.read_text())
        verify("previous_goal_turn_progress_and_static_restoring_derivation", static_owner["state"] == "complete" and static_owner["passed"] == static_owner["total"] == 84 and path.with_name("COMPLETE").exists())
        verify("static_restoring_inputs_unchanged", all(own(root / name) == digest for name, digest in static_owner["inputs"].items()))
        test_radius = numerical.linspace(4, 8, 33)
        test_scalar = numerical.stack([numerical.sin(test_radius), 0.2 * numerical.cos(test_radius), -0.1 * test_radius])
        test_coefficient = numerical.stack([1 + 0.1 * test_radius, numerical.cos(2 * test_radius), -0.4 * numerical.sin(test_radius)])
        test_restoring = restoring_time_coefficients(test_scalar, test_coefficient, 0.125)
        direct_zero = remainder_action(test_scalar[0], gram_parts(33, test_coefficient[0])) / 0.125
        verify("signed_Gram_leading_positive_operator", maximum(test_restoring[0] - direct_zero) < 1e-12)
        verify("signed_Gram_coefficient_linearity", maximum(signed_remainder_action(test_scalar[0], test_coefficient[1] - 2 * test_coefficient[2], 0.125) - signed_remainder_action(test_scalar[0], test_coefficient[1], 0.125) + 2 * signed_remainder_action(test_scalar[0], test_coefficient[2], 0.125)) < 1e-12)
        for step in [0.001, 0.0005]:
            samples = []
            for offset in [-step, 0, step]:
                value = sum(test_scalar[degree] * offset**degree for degree in range(3))
                coefficient = sum(test_coefficient[degree] * offset**degree for degree in range(3))
                samples.append(remainder_action(value, gram_parts(33, coefficient)) / 0.125)
            first = (samples[2] - samples[0]) / (2 * step)
            second = (samples[2] - 2 * samples[1] + samples[0]) / step**2
            verify("independent_signed_Gram_time_control_" + str(step), maximum(first - test_restoring[1]) < 1e-5 and maximum(second - 2 * test_restoring[2]) < 1e-5)
        bound_path = intake / "annular-volterra-source-completion-derived/status.json"
        own(bound_path)
        bound_owner = json.loads(bound_path.read_text())
        verify("Volterra_bound_owner_complete", bound_owner["state"] == "complete" and bound_owner["passed"] == bound_owner["total"] == 33 and bound_path.with_name("COMPLETE").exists())
        verify("Volterra_bound_inputs_unchanged", all(own(root / name) == digest for name, digest in bound_owner["inputs"].items()))
        test_radius = numerical.linspace(4, 8, 33)
        test_coefficient = numerical.stack([0.03 + 0.002 * test_radius, 0.001 * test_radius, -0.0003 * test_radius])
        test_forcing = numerical.stack([numerical.sin(test_radius), 0.04 * test_radius, 0.001 * test_radius**2])
        test_series = integrate_source_time_coefficients(test_coefficient, test_forcing, 0.125)
        verify("Volterra_moment_degree0_replay", maximum(test_series[0] - integrate_source(test_coefficient[0], test_forcing[0], 0.125)) < 1e-13)
        for step in [0.001, 0.0005]:
            sampled = [integrate_source(sum(test_coefficient[degree] * offset**degree for degree in range(3)), sum(test_forcing[degree] * offset**degree for degree in range(3)), 0.125) for offset in [-step, 0, step]]
            first = (sampled[2] - sampled[0]) / (2 * step)
            second = (sampled[2] - 2 * sampled[1] + sampled[0]) / step**2
            verify("independent_moment_finite_time_" + str(step), maximum(first - test_series[1]) < 1e-6 and maximum(second - 2 * test_series[2]) < 1e-6)
        rejected = False
        try:
            integrate_source_time_coefficients(constant(numerical.ones(9)), constant(numerical.ones(9)), 0.2)
        except ValueError:
            rejected = True
        verify("unqualified_large_argument_time_branch_rejected", rejected)
        folder = intake / ("annular-coupled-current-analytic-third-corner" if arguments.mode == "preflight" else "annular-compatible-current-restoring-smoke")
        path = folder / "status.json"
        own(path)
        owner = json.loads(path.read_text())
        field_passed = owner["state"] == "complete" and owner["passed"] == owner["total"]
        report["field_evolution_passed"] = field_passed
        report["retained_field_failures"] = [check for check in owner["checks"] if not check["passed"]]
        verify("field_evolution_terminal_and_fully_reported", owner["state"] in {"complete", "failed"} and "failure" not in owner and owner["active_job"] is None and owner["passed"] == sum(check["passed"] for check in owner["checks"]) and owner["total"] == len(owner["checks"]) and len(owner["runs"]) == 16 and len(owner["comparisons"]) == 4)
        verify("field_failure_not_promoted", (folder / "COMPLETE").exists() == field_passed)
        verify("owner_source_snapshot", own(folder / "executed-script.py") == owner["script_sha256"])
        verify("owner_inputs_unchanged", all(own(root / name) == digest for name, digest in owner["inputs"].items()))
        verify("exact_operator_configuration", owner["parameters"]["source_completion"] == ("projected" if arguments.mode == "preflight" else "compatible_volterra") and owner["parameters"]["dissipation"] == 0 and owner["parameters"]["initial_kind"] == "third_corner")
        for name in ["derive_annular_compatible_current_time_jets_20260909.py", "annular_compatible_current_restoring_20260909.py", "annular_compatible_current_time_jets_20260909.py", "annular_compatible_current_rhs_20260909.py", "sbp4_compatible_second_operator_20260909.py", "derive_annular_raw_volterra_C3_time_jets_20260909.py", "annular_raw_volterra_time_jets_20260909.py", "replay_annular_projected_volterra_time_jets_20260909.py", "annular_projected_volterra_source_20260909.py", "annular_projected_volterra_time_jets_20260909.py", "derive_annular_projected_volterra_time_jets_20260909.py", "annular_boundary_preserving_completion_20260909.py", "annular_volterra_source_completion_20260909.py", "annular_coupled_current_time_jets_20260909.py", "derive_annular_coupled_current_time_jets_20260909.py", "annular_correction_time_jets_20260909.py", "annular_coupled_current_operator_20260909.py", "annular_coordinate_evolution_operator_20260909.py", "annular_evolution_operator_20260909.py", "annular_fifth_order_jet_20260909.py", "annular_noether_completion_20260909.py", "annular_noether_source_projection_20260909.py", "sbp4_compatible_second_operator_20260909.py", "sbp4_derived_operator_20260909.py", "navier_stokes_source_audit_20260908.py"]:
            own(root / "scripts" / name)
        for case_name in ["canonical", "nonlinear_modulated"]:
            path = intake / "annular-constraint-correction-initial" / (case_name + ".json")
            own(path)
            evaluator = AnnularFields(json.loads(path.read_text()))
            for entry in owner["runs"]:
                if entry["case"] != case_name or entry["time_refinement"] != (2 if entry["intervals"] == max(owner["parameters"]["N"]) else 1):
                    continue
                path = folder / entry["artifact"]
                label = path.stem
                verify(label + "_artifact_hash", own(path) == entry["sha256"])
                with numerical.load(path, allow_pickle=False) as arrays:
                    radii, correction, saved_rhs, saved_source, saved_defect, saved_coordinate_source = [arrays[key] for key in ["radius", "correction_current", "current_rhs", "numerical_source", "background_defect", "coordinate_numerical_source"]]
                engine = CompatibleCurrentTimeJets(evaluator, radii, entry["time"])
                derivatives = engine.time_derivatives(correction)
                values = derivatives[:3].copy()
                values[2] /= 2
                output, sources, coordinate_sources, raw = engine.rhs(engine.current, values)
                direct, direct_source, direct_coordinate, projected_reference, source_diagnostics = direct_rhs(engine, 0, correction)
                verify(label + "_unprojected_scalar_lapse_source_law", numerical.array_equal(direct_coordinate[[0, 1, 3]], projected_reference[[0, 1, 3]]))
                if arguments.mode == "preflight":
                    expected_rhs = saved_rhs - saved_source + direct_source
                else:
                    expected_rhs = saved_rhs
                    verify(label + "_new_trajectory_source_replay", maximum(direct_source - saved_source) < 1e-8 * max(maximum(saved_source), 1e-20) + 1e-22)
                rhs_error = numerical.max(numerical.abs(derivatives[1] - expected_rhs), axis=-1)
                rhs_scale = numerical.maximum(numerical.max(numerical.abs(expected_rhs), axis=-1), 1e-20)
                verify(label + "_saved_RHS_replay", numerical.all(rhs_error < 1e-8 * rhs_scale + 1e-22), {"error": rhs_error.tolist(), "scale": rhs_scale.tolist()})
                verify(label + "_saved_source_replay", maximum(sources[0] - direct_source) < 1e-8 * max(maximum(direct_source), 1e-20) + 1e-22)
                verify(label + "_saved_coordinate_source_replay", maximum(coordinate_sources[0] - direct_coordinate) < 1e-8 * max(maximum(direct_coordinate), 1e-20) + 1e-22)
                defect_error = maximum(engine.current["defect"][0] - saved_defect)
                verify(label + "_saved_nonzero_forcing_replay", defect_error < 1e-8 * maximum(saved_defect) + 1e-22 and maximum(saved_defect) > 0, {"error": defect_error, "scale": maximum(saved_defect)})
                verify(label + "_source_endpoint_and_lapse_preserved", maximum(coordinate_sources[:, 1, [0, -1]] - raw[:, 1, [0, -1]]) == 0 and maximum(coordinate_sources[:, 3] - raw[:, 3]) == 0 and maximum(coordinate_sources[:, 2, -1]) == 0)
                velocity = series_dot(engine.current["q_gradient"], values)
                verify(label + "_scalar_kinematic_recurrence", maximum(output[:, 0] - velocity + engine.current["defect"][:, 0]) < 1e-22)
                verify(label + "_integrability_time_recurrence", maximum(output[:, 1] - derivative(output[:, 0], engine.spacing)) < 1e-18)
                source_errors = derivative(sources[:, 3], engine.spacing) - series_dot(engine.current["constraint_gradient"], sources)
                verify(label + "_bounded_nonzero_source_residual", numerical.all(numerical.abs(source_errors[0]) <= source_diagnostics["bound"] + 1e-24), {"residual_max": maximum(source_errors[0]), "bound_max": maximum(source_diagnostics["bound"]), "exact_zero_claimed": False})
                verify(label + "_higher_Noether_coefficients_recorded_not_zeroed", numerical.all(numerical.isfinite(source_errors)), {"max_by_time_degree": numerical.max(numerical.abs(source_errors), axis=-1).tolist()})
                controls = []
                for step in [0.00025, 0.000125]:
                    samples = []
                    for node in range(5):
                        offset = -node * step
                        state = correction + offset * derivatives[1] + offset**2 * derivatives[2] / 2
                        samples.append(direct_rhs(engine, offset, state)[0])
                    samples = numerical.array(samples)
                    first = numerical.tensordot([25 / 12, -4, 3, -4 / 3, 1 / 4], samples, axes=(0, 0)) / step
                    second = numerical.tensordot([35 / 12, -26 / 3, 19 / 2, -14 / 3, 11 / 12], samples, axes=(0, 0)) / step**2
                    errors = numerical.max(numerical.abs(numerical.stack([first, second]) - derivatives[2:]), axis=-1)
                    scales = numerical.maximum(numerical.max(numerical.abs(derivatives[2:]), axis=-1), 1e-20)
                    controls.append({"step": step, "errors": errors.tolist(), "scales": scales.tolist()})
                    verify(label + "_finite_time_control_" + str(step), numerical.all(errors < 1e-4 * scales + numerical.array([1e-18, 1e-15])[:, None]), controls[-1])
                side_change = None
                if entry["time"] == 0.1:
                    other = CompatibleCurrentTimeJets(evaluator, radii, entry["time"], side="right")
                    changed = other.time_derivatives(correction)
                    errors = numerical.max(numerical.abs(changed - derivatives), axis=-1)
                    scales = numerical.maximum(numerical.max(numerical.abs(derivatives), axis=-1), 1e-20)
                    side_change = {"absolute_by_order_component": errors.tolist(), "relative_by_order_component": (errors / scales).tolist()}
                    verify(label + "_cache_side_control", numerical.all(errors < 0.01 * scales + 1e-18), side_change)
                filename = label + "_time_jets.npz"
                numerical.savez(destination / filename, radius=radii, current_time_derivatives=derivatives, numerical_source_time_coefficients=sources, coordinate_source_time_coefficients=coordinate_sources, Noether_time_coefficients=source_errors)
                report["runs"].append({"source_residual_max": maximum(source_errors[0]), "source_bound_max": maximum(source_diagnostics["bound"]), "mass_source_max": maximum(direct_coordinate[2]), "mode": arguments.mode, "case": case_name, "intervals": entry["intervals"], "time": entry["time"], "time_refinement": entry["time_refinement"], "artifact": filename, "sha256": hashlib.sha256((destination / filename).read_bytes()).hexdigest(), "source_artifact": entry["artifact"], "cache_first": engine.first, "controls": controls, "side_change": side_change, "component_maxima_by_time_order": numerical.max(numerical.abs(derivatives), axis=-1).tolist(), "valid_for_physics_claim": False})
                save()
        verify("all_twelve_snapshots_processed", len(report["runs"]) == 12)
        for name in ["annular_projected_volterra_source_20260909.py", "annular_projected_volterra_time_jets_20260909.py", "derive_annular_projected_volterra_time_jets_20260909.py"]:
            path = root / "scripts" / name
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
    print(json.dumps({key: report[key] for key in ["state", "passed", "total", "completed_utc"]}), flush=True)


if __name__ == "__main__":
    run()
