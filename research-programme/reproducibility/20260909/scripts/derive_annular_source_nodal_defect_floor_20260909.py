import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as numerical
    from annular_coordinate_evolution_operator_20260909 import AnnularFields
    from annular_coupled_current_time_jets_20260909 import CoupledCurrentTimeJets
    from annular_volterra_source_completion_20260909 import integrate_source
    from sbp4_derived_operator_20260909 import derivative

    root = Path(__file__).resolve().parents[1]
    intake = root / "source-intake/navier-stokes/20260909"
    destination = intake / "annular-source-nodal-defect-floor"
    destination.mkdir(exist_ok=False)
    source = Path(__file__).read_bytes()
    (destination / "executed-script.py").write_bytes(source)
    report = {"state": "running", "started_utc": datetime.now(timezone.utc).isoformat(), "script_sha256": hashlib.sha256(source).hexdigest(), "inputs": {}, "checks": [], "rows": [], "valid_for_physics_claim": False, "scope": "Exact finite-dimensional minimax formula, evaluated in floating point on fixed-source snapshots. Not interval-certified numeric lower bounds, not an evolved alternative, not a continuum or physical no-go. Same scalar/lapse source and zero outer mass source retained. Original projected baseline is tested with its own already-projected forcing, not confused with the candidate raw forcing.", "formula": "A=(D_h-diag(a))[:,:-1], A^T n=0, rank(A)=N. min_u ||Au-f||inf=|n^T f|/||n||1; attained by residual r=-(n^T f) sign(n)/||n||1 and Au=f+r. Interior a=0 Volterra/D4 transfer is 1-x/3-2x^2/3, x=sin(theta/2)^2; its residual is -x(1+2x)/3."}

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
        for name in ["annular_volterra_source_completion_20260909.py", "annular_coupled_current_time_jets_20260909.py", "sbp4_derived_operator_20260909.py"]:
            own(root / "scripts" / name)
        previous_path = intake / "annular-compatible-current-smoke-comparison/status.json"
        own(previous_path)
        previous = json.loads(previous_path.read_text())
        verify("matched_comparison_complete", previous["state"] == "complete" and previous["passed"] == previous["total"] == 289 and previous_path.with_name("COMPLETE").exists())
        verify("comparison_sources_unchanged", all(own(root / name) == digest for name, digest in previous["inputs"].items()))
        verify("candidate_failure_preserved", not previous["candidate_field_evolution_passed"] and len(previous["retained_field_failures"]) == 7)
        count, spacing = 129, 1 / 32
        positions = numerical.arange(count)
        for frequency in [numerical.pi / 8, numerical.pi / 2, 3 * numerical.pi / 4, numerical.pi]:
            forcing = numerical.cos(frequency * positions)
            response = integrate_source(numerical.zeros(count), forcing, spacing)
            residual = derivative(response, spacing) - forcing
            argument = numerical.sin(frequency / 2)**2
            exact_residual = -argument * (1 + 2 * argument) / 3 * forcing
            verify("interior_transfer_symbol_" + str(frequency), maximum(residual[4:-4] - exact_residual[4:-4]) < 1e-12)
        alternating = (-1.)**positions
        zero_response = integrate_source(numerical.zeros(count), alternating, spacing)
        verify("alternating_source_entirely_lost_not_global_D_null_claim", maximum(zero_response) == 0 and maximum(derivative(zero_response, spacing) - alternating) == 1)
        inverse_costs = []
        for distance in [0.1, 0.01, 0.001]:
            frequency = numerical.pi - distance
            inverse_costs.append(spacing / abs(numerical.sin(frequency) * (4 - numerical.cos(frequency)) / 3))
        verify("interior_exact_inverse_diverges_near_Nyquist", inverse_costs[1] > 9 * inverse_costs[0] and inverse_costs[2] > 9 * inverse_costs[1], inverse_costs)
        engines = {}
        for branch, owner_name in [("baseline", "annular-compatible-current-matched-baseline"), ("candidate", "annular-compatible-current-restoring-smoke")]:
            folder = intake / owner_name
            own(folder / "status.json")
            owner = json.loads((folder / "status.json").read_text())
            verify(branch + "_terminal_state_retained", owner["state"] == ("complete" if branch == "baseline" else "failed") and owner["active_job"] is None)
            for entry in owner["runs"]:
                if entry["time_refinement"] != (2 if entry["intervals"] == 128 else 1):
                    continue
                path = folder / entry["artifact"]
                tag = branch + "_" + path.stem
                verify(tag + "_saved_array_hash", own(path) == entry["sha256"])
                with numerical.load(path, allow_pickle=False) as loaded:
                    arrays = {key: loaded[key] for key in loaded.files}
                key = entry["case"], entry["time"], entry["intervals"]
                if key not in engines:
                    case_path = intake / "annular-constraint-correction-initial" / (entry["case"] + ".json")
                    own(case_path)
                    evaluator = AnnularFields(json.loads(case_path.read_text()))
                    engine = CoupledCurrentTimeJets(evaluator, arrays["radius"], entry["time"])
                    coefficient = engine.current["old_gradient"][0, 2]
                    matrix = derivative(numerical.eye(coefficient.size), engine.spacing).T - numerical.diag(coefficient)
                    anchored = matrix[:, :-1]
                    left, singular, right = numerical.linalg.svd(anchored, full_matrices=True)
                    normal = left[:, -1]
                    engines[key] = engine, anchored, left, singular, right, normal
                engine, anchored, left, singular, right, normal = engines[key]
                gradient = engine.current["old_gradient"][0]
                sources = arrays["coordinate_numerical_source"]
                forcing = gradient[1] * sources[1] + gradient[3] * sources[3]
                mass_source = sources[2]
                verify(tag + "_zero_outer_source", mass_source[-1] == 0)
                verify(tag + "_full_rank_and_left_null", singular[-1] > 1e-12 * singular[0] and maximum(normal @ anchored) < 1e-12 * singular[0])
                projection = float(normal @ forcing)
                floor = abs(projection) / float(numerical.sum(numerical.abs(normal)))
                target_residual = -projection * numerical.sign(normal) / numerical.sum(numerical.abs(normal))
                minimax = right.T @ ((left[:, :-1].T @ (forcing + target_residual)) / singular)
                measured_residual = anchored @ minimax - forcing
                actual_residual = anchored @ mass_source[:-1] - forcing
                scale = max(maximum(forcing), maximum(anchored) * maximum(minimax), 1e-25)
                tolerance = 1e-10 * scale + 1e-25
                verify(tag + "_constructive_minimax_attainment", maximum(measured_residual - target_residual) <= tolerance and abs(maximum(measured_residual) - floor) <= tolerance)
                verify(tag + "_actual_residual_above_floor", maximum(actual_residual) + tolerance >= floor)
                verify(tag + "_dual_identity", abs(float(normal @ actual_residual) + projection) <= tolerance)
                current_source = arrays["numerical_source"]
                current_gradient = engine.current["constraint_gradient"][0]
                current_residual = derivative(current_source[3], engine.spacing) - numerical.sum(current_gradient * current_source, axis=0)
                verify(tag + "_coordinate_current_residual_agreement", maximum(actual_residual - current_residual) <= tolerance)
                row = {key: entry[key] for key in ["case", "intervals", "time"]}
                row.update(branch=branch, source_forcing_max=maximum(forcing), observed_source_nodal_residual=maximum(actual_residual), best_possible_fixed_source_nodal_residual=floor, observed_over_optimal=maximum(actual_residual) / floor if floor > 1e-25 else None, residual_floor_over_forcing=floor / maximum(forcing) if maximum(forcing) else None, original_mass_source_max=maximum(mass_source), minimax_mass_source_max=maximum(minimax), matrix_condition=float(singular[0] / singular[-1]), numerical_rank_threshold=1e-12, numerical_verification_tolerance=tolerance, minimax_evolved=False, interval_certified=False, valid_for_physics_claim=False)
                report["rows"].append(row)
        verify("all24_saved_states_processed", len(report["rows"]) == 24)
        verify("no_bytecode_cache", not (root / "scripts/__pycache__").exists())
        compile(Path(__file__).read_bytes(), str(Path(__file__)), "exec")
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
