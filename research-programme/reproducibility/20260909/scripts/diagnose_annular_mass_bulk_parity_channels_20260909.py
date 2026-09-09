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
    from sbp4_derived_operator_20260909 import derivative

    root = Path(__file__).resolve().parents[1]
    intake = root / "source-intake/navier-stokes/20260909"
    destination = intake / "annular-mass-bulk-parity-channels"
    destination.mkdir(exist_ok=False)
    source = Path(__file__).read_bytes()
    (destination / "executed-script.py").write_bytes(source)
    report = {"state": "running", "started_utc": datetime.now(timezone.utc).isoformat(), "script_sha256": hashlib.sha256(source).hexdigest(), "inputs": {}, "checks": [], "runs": [], "valid_for_physics_claim": False, "scope": "Resolve actual mass bulk parity into five C_gradient*e response terms and the nonzero parent defect, retaining every term. Products are formed BEFORE applying the linear parity diagnostic. Instantaneous source attribution is not a continuum error certificate or permission to delete forcing."}

    def save():
        (destination / "status.json").write_text(json.dumps(report, indent=2) + "\n")

    def own(path):
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        report["inputs"][str(path.relative_to(root))] = digest
        return digest

    def verify(name, condition, detail=None):
        report["checks"].append({"name": name, "passed": bool(condition), "detail": detail})
        save()

    def maximum(values):
        return float(numerical.max(numerical.abs(values)))

    def parity(values, spacing):
        slopes = derivative(values, spacing)
        trace = slopes[..., :-1] + slopes[..., 1:] - 2 * numerical.diff(values, axis=-1) / spacing
        return ((-1.)**numerical.arange(trace.shape[-1]) * spacing * trace / 4)[..., 8:-8]

    save()
    try:
        own(Path(__file__))
        comparison_path = intake / "annular-projected-volterra-matched-comparison-portable/status.json"
        own(comparison_path)
        comparison = json.loads(comparison_path.read_text())
        verify("matched_comparison_complete", comparison["state"] == "complete" and comparison["passed"] == comparison["total"] == 244 and comparison_path.with_name("COMPLETE").exists())
        verify("comparison_inputs_unchanged", all(own(root / name) == digest for name, digest in comparison["inputs"].items()))
        verify("hybrid_failure_retained", not comparison["hybrid_field_evolution_passed"] and not comparison["all_hybrid_curvature_sensitivity_gates_passed"] and not comparison["all_hybrid_strong_mesh_differences_reduced"])
        for name in ["annular_coupled_current_time_jets_20260909.py", "annular_coordinate_evolution_operator_20260909.py", "sbp4_derived_operator_20260909.py"]:
            own(root / "scripts" / name)
        for case_name in ["canonical", "nonlinear_modulated"]:
            path = intake / "annular-constraint-correction-initial" / (case_name + ".json")
            own(path)
            evaluator = AnnularFields(json.loads(path.read_text()))
            for branch, folder_name in [("original", "annular-coupled-current-analytic-third-corner"), ("hybrid", "annular-projected-volterra-third-corner")]:
                folder = intake / folder_name
                own(folder / "status.json")
                owner = json.loads((folder / "status.json").read_text())
                for entry in owner["runs"]:
                    if entry["case"] != case_name or entry["time_refinement"] != (2 if entry["intervals"] == 512 else 1):
                        continue
                    path = folder / entry["artifact"]
                    verify(branch + "_" + path.stem + "_hash", own(path) == entry["sha256"])
                    with numerical.load(path, allow_pickle=False) as arrays:
                        radii, state, rhs, added, defect = [arrays[key] for key in ["radius", "correction_current", "current_rhs", "numerical_source", "background_defect"]]
                    engine = CoupledCurrentTimeJets(evaluator, radii, entry["time"])
                    terms = numerical.concatenate([engine.current["C_gradient"][0] * state, -defect[3][None]], axis=0)
                    bulk = rhs[3] - added[3]
                    error = maximum(terms.sum(axis=0) - bulk)
                    verify(branch + "_" + path.stem + "_actual_mass_bulk_decomposition", error < 1e-8 * max(maximum(bulk), 1e-20) + 1e-22, {"error": error, "scale": maximum(bulk)})
                    indicators = parity(terms, engine.spacing)
                    actual = parity(bulk, engine.spacing)
                    verify(branch + "_" + path.stem + "_linear_parity_decomposition", maximum(indicators.sum(axis=0) - actual) < 1e-8 * max(maximum(actual), 1e-20) + 1e-22)
                    rms = numerical.sqrt(numerical.mean(indicators**2, axis=-1))
                    total_rms = float(numerical.sqrt(numerical.mean(actual**2)))
                    coefficients = numerical.sum(indicators * actual, axis=-1) / max(float(numerical.sum(actual**2)), 1e-300)
                    row = {key: entry[key] for key in ["case", "time", "intervals"]}
                    row.update(branch=branch, term_names=["C_chi*e_chi", "C_w*e_w", "C_h*e_h", "C_mu*e_mu", "C_delta*e_delta", "-parent_mass_defect"], term_maxima=numerical.max(numerical.abs(terms), axis=-1).tolist(), term_parity_RMS=rms.tolist(), bulk_parity_RMS=total_rms, alignment_fraction_with_total_bulk=coefficients.tolist(), dominant_RMS_term=int(numerical.argmax(rms)), diagnostic_not_claim=True)
                    report["runs"].append(row)
                    save()
        verify("all24_states_decomposed", len(report["runs"]) == 24)
        compile(Path(__file__).read_bytes(), str(Path(__file__)), "exec")
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
