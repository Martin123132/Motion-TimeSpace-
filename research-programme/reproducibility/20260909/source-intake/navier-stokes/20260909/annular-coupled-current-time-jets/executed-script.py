import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as numerical
    from annular_coordinate_evolution_operator_20260909 import AnnularFields
    from annular_coupled_current_time_jets_20260909 import CoupledCurrentTimeJets, series_dot
    from sbp4_derived_operator_20260909 import derivative

    root = Path(__file__).resolve().parents[1]
    intake = root / "source-intake/navier-stokes/20260909"
    destination = intake / "annular-coupled-current-time-jets"
    destination.mkdir(exist_ok=False)
    source = Path(__file__).read_bytes()
    (destination / "executed-script.py").write_bytes(source)
    report = {"state": "running", "started_utc": datetime.now(timezone.utc).isoformat(), "script_sha256": hashlib.sha256(source).hexdigest(), "inputs": {}, "checks": [], "runs": [], "valid_for_physics_claim": False, "scope": "Actual ordinary coupled current RHS and projected numerical source Taylor recurrence through third time derivative. Frozen original cache times, independent nonzero defect, no filter, no first-u branch. Software/finite-difference checks are not continuum derivative error bounds."}

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
        folder = intake / "annular-coupled-current-analytic-third-corner"
        path = folder / "status.json"
        own(path)
        owner = json.loads(path.read_text())
        verify("ordinary_evolution_owner_passed", owner["state"] == "complete" and owner["passed"] == owner["total"] == 129 and (folder / "COMPLETE").exists())
        verify("owner_source_snapshot", own(folder / "executed-script.py") == owner["script_sha256"])
        verify("owner_inputs_unchanged", all(own(root / name) == digest for name, digest in owner["inputs"].items()))
        verify("exact_operator_configuration", owner["parameters"]["source_completion"] == "projected" and owner["parameters"]["dissipation"] == 0 and owner["parameters"]["initial_kind"] == "third_corner")
        for name in ["annular_coupled_current_time_jets_20260909.py", "derive_annular_coupled_current_time_jets_20260909.py", "annular_correction_time_jets_20260909.py", "annular_coupled_current_operator_20260909.py", "annular_coordinate_evolution_operator_20260909.py", "annular_evolution_operator_20260909.py", "annular_fifth_order_jet_20260909.py", "annular_noether_completion_20260909.py", "annular_noether_source_projection_20260909.py", "sbp4_compatible_second_operator_20260909.py", "sbp4_derived_operator_20260909.py", "navier_stokes_source_audit_20260908.py"]:
            own(root / "scripts" / name)
        for case_name in ["canonical", "nonlinear_modulated"]:
            path = intake / "annular-constraint-correction-initial" / (case_name + ".json")
            own(path)
            evaluator = AnnularFields(json.loads(path.read_text()))
            for entry in owner["runs"]:
                if entry["case"] != case_name or entry["time_refinement"] != (2 if entry["intervals"] == 512 else 1):
                    continue
                path = folder / entry["artifact"]
                label = path.stem
                verify(label + "_artifact_hash", own(path) == entry["sha256"])
                with numerical.load(path, allow_pickle=False) as arrays:
                    radii, correction, saved_rhs, saved_source, saved_defect, saved_coordinate_source = [arrays[key] for key in ["radius", "correction_current", "current_rhs", "numerical_source", "background_defect", "coordinate_numerical_source"]]
                engine = CoupledCurrentTimeJets(evaluator, radii, entry["time"])
                derivatives = engine.time_derivatives(correction)
                values = derivatives[:3].copy()
                values[2] /= 2
                output, sources, coordinate_sources, raw = engine.rhs(engine.current, values)
                rhs_error = numerical.max(numerical.abs(derivatives[1] - saved_rhs), axis=-1)
                rhs_scale = numerical.maximum(numerical.max(numerical.abs(saved_rhs), axis=-1), 1e-20)
                verify(label + "_saved_RHS_replay", numerical.all(rhs_error < 1e-8 * rhs_scale + 1e-22), {"error": rhs_error.tolist(), "scale": rhs_scale.tolist()})
                verify(label + "_saved_source_replay", maximum(sources[0] - saved_source) < 1e-8 * max(maximum(saved_source), 1e-20) + 1e-22)
                verify(label + "_saved_coordinate_source_replay", maximum(coordinate_sources[0] - saved_coordinate_source) < 1e-8 * max(maximum(saved_coordinate_source), 1e-20) + 1e-22)
                defect_error = maximum(engine.current["defect"][0] - saved_defect)
                verify(label + "_saved_nonzero_forcing_replay", defect_error < 1e-8 * maximum(saved_defect) + 1e-22 and maximum(saved_defect) > 0, {"error": defect_error, "scale": maximum(saved_defect)})
                verify(label + "_source_endpoint_and_lapse_preserved", maximum(coordinate_sources[:, 1, [0, -1]] - raw[:, 1, [0, -1]]) == 0 and maximum(coordinate_sources[:, 3] - raw[:, 3]) == 0 and maximum(coordinate_sources[:, 2, -1]) == 0)
                velocity = series_dot(engine.current["q_gradient"], values)
                verify(label + "_scalar_kinematic_recurrence", maximum(output[:, 0] - velocity + engine.current["defect"][:, 0]) < 1e-22)
                verify(label + "_integrability_time_recurrence", maximum(output[:, 1] - derivative(output[:, 0], engine.spacing)) < 1e-18)
                source_errors = derivative(sources[:, 3], engine.spacing) - series_dot(engine.current["constraint_gradient"], sources)
                for degree in range(3):
                    scale = max(maximum(derivative(sources[degree, 3], engine.spacing)), maximum(series_dot(engine.current["constraint_gradient"], sources)[degree]), 1e-30)
                    verify(label + "_Noether_time_coefficient_" + str(degree), maximum(source_errors[degree]) < 1e-10 * scale + 1e-22, {"error": maximum(source_errors[degree]), "scale": scale})
                controls = []
                for step in [0.00025, 0.000125]:
                    samples = []
                    for node in range(5):
                        offset = -node * step
                        state = correction + offset * derivatives[1] + offset**2 * derivatives[2] / 2
                        samples.append(engine.evaluate_rhs(offset, state))
                    samples = numerical.array(samples)
                    first = numerical.tensordot([25 / 12, -4, 3, -4 / 3, 1 / 4], samples, axes=(0, 0)) / step
                    second = numerical.tensordot([35 / 12, -26 / 3, 19 / 2, -14 / 3, 11 / 12], samples, axes=(0, 0)) / step**2
                    errors = numerical.max(numerical.abs(numerical.stack([first, second]) - derivatives[2:]), axis=-1)
                    scales = numerical.maximum(numerical.max(numerical.abs(derivatives[2:]), axis=-1), 1e-20)
                    controls.append({"step": step, "errors": errors.tolist(), "scales": scales.tolist()})
                    verify(label + "_finite_time_control_" + str(step), numerical.all(errors < 1e-4 * scales + numerical.array([1e-18, 1e-15])[:, None]), controls[-1])
                side_change = None
                if entry["time"] == 0.1:
                    other = CoupledCurrentTimeJets(evaluator, radii, entry["time"], side="right")
                    changed = other.time_derivatives(correction)
                    errors = numerical.max(numerical.abs(changed - derivatives), axis=-1)
                    scales = numerical.maximum(numerical.max(numerical.abs(derivatives), axis=-1), 1e-20)
                    side_change = {"absolute_by_order_component": errors.tolist(), "relative_by_order_component": (errors / scales).tolist()}
                    verify(label + "_cache_side_control", numerical.all(errors < 0.01 * scales + 1e-18), side_change)
                filename = label + "_time_jets.npz"
                numerical.savez(destination / filename, radius=radii, current_time_derivatives=derivatives, numerical_source_time_coefficients=sources, coordinate_source_time_coefficients=coordinate_sources, Noether_time_coefficients=source_errors)
                report["runs"].append({"case": case_name, "intervals": entry["intervals"], "time": entry["time"], "time_refinement": entry["time_refinement"], "artifact": filename, "sha256": hashlib.sha256((destination / filename).read_bytes()).hexdigest(), "source_artifact": entry["artifact"], "cache_first": engine.first, "controls": controls, "side_change": side_change, "component_maxima_by_time_order": numerical.max(numerical.abs(derivatives), axis=-1).tolist(), "valid_for_physics_claim": False})
                save()
        verify("all_twelve_snapshots_processed", len(report["runs"]) == 12)
        for name in ["annular_coupled_current_time_jets_20260909.py", "derive_annular_coupled_current_time_jets_20260909.py"]:
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
