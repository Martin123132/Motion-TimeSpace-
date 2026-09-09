import hashlib
import json
from datetime import datetime, timezone
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as numerical
    import sympy as symbolic
    from sbp4_derived_operator_20260909 import derivative

    root = Path(__file__).resolve().parents[1]
    intake = root / "source-intake/navier-stokes/20260909"
    destination = intake / "annular-centered-constraint-mode-diagnosis"
    destination.mkdir(exist_ok=False)
    source = Path(__file__).read_bytes()
    (destination / "executed-script.py").write_bytes(source)
    report = {"state": "running", "started_utc": datetime.now(timezone.utc).isoformat(), "script_sha256": hashlib.sha256(source).hexdigest(), "inputs": {}, "checks": [], "runs": [], "valid_for_physics_claim": False, "scope": "Interior centered-derivative blind-mode theorem plus parity diagnostics of actual mass reconstruction traces. Not a claim of a global nullspace with SBP boundary closures; not proof that this is the sole producer of numerical error."}

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

    save()
    try:
        own(Path(__file__))
        own(root / "scripts/sbp4_derived_operator_20260909.py")
        phase, spacing_symbol = symbolic.symbols("phase spacing", real=True, nonzero=True)
        stencil = (symbolic.exp(-2 * symbolic.I * phase) - 8 * symbolic.exp(-symbolic.I * phase) + 8 * symbolic.exp(symbolic.I * phase) - symbolic.exp(2 * symbolic.I * phase)) / (12 * spacing_symbol)
        expected = symbolic.I * symbolic.sin(phase) * (4 - symbolic.cos(phase)) / (3 * spacing_symbol)
        verify("symbolic_centered_D4_symbol", symbolic.simplify(symbolic.expand_complex(stencil - expected)) == 0)
        verify("Nyquist_symbol_zero", symbolic.simplify(expected.subs(phase, symbolic.pi)) == 0)
        for intervals in [128, 256, 512, 1024]:
            mode = (-1.)**numerical.arange(intervals + 1)
            observed = derivative(mode, 4 / intervals)
            verify("N" + str(intervals) + "_interior_blind_boundary_not_blind", numerical.max(numerical.abs(observed[4:-4])) == 0 and numerical.max(numerical.abs(observed)) > 0)
        amplitude, spacing, length = symbolic.symbols("amplitude spacing length", positive=True)
        trace3, left, right = 4 * amplitude / spacing, 12 * amplitude / spacing**2, -12 * amplitude / spacing**2
        floor3 = length / spacing * 30 * trace3**2 / spacing**3
        floor4 = length / spacing * (30 * (left + right)**2 + 210 * (left - right)**2) / spacing**3
        verify("checkerboard_H3_trace_floor", symbolic.simplify(floor3 - 480 * length * amplitude**2 / spacing**6) == 0)
        verify("checkerboard_H4_trace_floor", symbolic.simplify(floor4 - 120960 * length * amplitude**2 / spacing**8) == 0)
        for owner_name in ["annular-current-normal-reconstruction", "annular-normal-spatial-refinement-validation"]:
            folder = intake / owner_name
            own(folder / "status.json")
            owner = json.loads((folder / "status.json").read_text())
            verify(owner_name + "_software_complete", owner["state"] == "complete" and owner["passed"] == owner["total"])
            for entry in owner["runs"]:
                if entry["method"] != "poly7":
                    continue
                path = folder / entry["artifact"]
                verify(path.stem + "_hash", own(path) == entry["sha256"])
                with numerical.load(path, allow_pickle=False) as arrays:
                    radii, coefficients = arrays["radius"], arrays["Hermite_coefficients"][0]
                spacing = float(radii[1] - radii[0])
                values = numerical.c_[coefficients[0], numerical.sum(coefficients[:, :, -1], axis=0)]
                slopes = numerical.c_[coefficients[1], numerical.sum(numerical.arange(8)[:, None] * coefficients[:, :, -1], axis=0)] / spacing
                curvatures = numerical.c_[2 * coefficients[2], numerical.sum((numerical.arange(8) * (numerical.arange(8) - 1))[:, None] * coefficients[:, :, -1], axis=0)] / spacing**2
                secant = numerical.diff(values, axis=-1) / spacing
                third_trace = slopes[:, :-1] + slopes[:, 1:] - 2 * secant
                mass_trace = third_trace[3, 8:-8]
                denominator = numerical.linalg.norm(mass_trace[:-1]) * numerical.linalg.norm(mass_trace[1:])
                correlation = float(numerical.dot(mass_trace[:-1], mass_trace[1:]) / denominator) if denominator else None
                alternating_amplitude = (-1.)**numerical.arange(len(mass_trace)) * spacing * mass_trace / 4
                left = curvatures[:, :-1] + (4 * slopes[:, :-1] + 2 * slopes[:, 1:] - 6 * secant) / spacing
                right = curvatures[:, 1:] + (6 * secant - 2 * slopes[:, :-1] - 4 * slopes[:, 1:]) / spacing
                lower4 = numerical.sqrt(numerical.sum(30 * (left + right)**2 + 210 * (left - right)**2, axis=-1) / spacing**3)
                lower3 = numerical.sqrt(30 * numerical.sum(third_trace**2, axis=-1) / spacing**3)
                report["runs"].append({"case": entry["case"], "time": entry["time"], "intervals": entry["intervals"], "mass_trace_lag1_cosine_excluding8_cells": correlation, "mass_alternating_amplitude_RMS_diagnostic": float(numerical.sqrt(numerical.mean(alternating_amplitude**2))), "mass_amplitude_diagnostic_max": float(numerical.max(numerical.abs(alternating_amplitude))), "mass_H4_trace_lower_bound_all_cells": float(lower4[3]), "physical_H3chi_H4mu_H4delta_lower_bound_all_cells": float(numerical.sqrt(lower3[0]**2 + lower4[3]**2 + lower4[4]**2)), "parity_diagnostic_is_not_a_claim_gate": True, "valid_for_physics_claim": False})
                save()
        compile(Path(__file__).read_bytes(), str(Path(__file__)), "exec")
        verify("no_bytecode_cache", not (root / "scripts/__pycache__").exists())
        report.update(passed=sum(check["passed"] for check in report["checks"]), total=len(report["checks"]), completed_utc=datetime.now(timezone.utc).isoformat())
        report["state"] = "complete" if report["passed"] == report["total"] else "failed"
        save()
    except Exception as error:
        report.update(state="failed", failure=repr(error), completed_utc=datetime.now(timezone.utc).isoformat())
        save()
        raise
    print(json.dumps({key: report[key] for key in ["state", "passed", "total", "completed_utc"]}), flush=True)
    if report["state"] != "complete":
        raise SystemExit(1)
    (destination / "COMPLETE").write_text(report["completed_utc"] + "\n")


if __name__ == "__main__":
    run()
