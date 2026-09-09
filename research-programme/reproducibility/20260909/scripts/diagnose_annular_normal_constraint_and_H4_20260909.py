import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as numerical
    import sympy as symbolic
    from annular_coordinate_evolution_operator_20260909 import AnnularFields
    from annular_coupled_current_time_jets_20260909 import CoupledCurrentTimeJets
    from annular_current_normal_reconstruction_20260909 import construct_system, solve_jets

    root = Path(__file__).resolve().parents[1]
    intake = root / "source-intake/navier-stokes/20260909"
    destination = intake / "annular-normal-constraint-H4-diagnosis"
    destination.mkdir(exist_ok=False)
    source = Path(__file__).read_bytes()
    (destination / "executed-script.py").write_bytes(source)
    report = {"state": "running", "started_utc": datetime.now(timezone.utc).isoformat(), "script_sha256": hashlib.sha256(source).hexdigest(), "inputs": {}, "checks": [], "cases": [], "norms": [], "refinement": [], "valid_for_physics_claim": False, "scope": "Symbolic radial invertibility, retained-constraint contribution to the normal-reconstruction Z discrepancy, exact-degree polynomial quadrature of reconstructed H0..H4 norms and nested-grid differences. No unknown continuum-error bound; no nodal-gate pass promoted to physical regularity."}

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

    def polynomial_derivative(coefficients, spacing, order, locations):
        result = numerical.zeros((coefficients.shape[1],) + locations.shape)
        for power in range(order, coefficients.shape[0]):
            result += coefficients[power, :, :, None] * (math.factorial(power) / math.factorial(power - order) / spacing**order) * locations**(power - order)
        return result

    def norms(coefficients, spacing, quadrature=8, coarse=None):
        nodes, weights = numerical.polynomial.legendre.leggauss(quadrature)
        nodes, weights = (nodes + 1) / 2, weights / 2
        locations = numerical.broadcast_to(nodes, (coefficients.shape[-1], quadrature))
        if coarse is not None:
            indices = numerical.arange(coefficients.shape[-1])
            other_coefficients = numerical.take(coarse, indices // 2, axis=-1)
            other_locations = (indices[:, None] % 2 + locations) / 2
        result = []
        for order in range(5):
            values = polynomial_derivative(coefficients, spacing, order, locations)
            if coarse is not None:
                values -= polynomial_derivative(other_coefficients, 2 * spacing, order, other_locations)
            result.append(numerical.sqrt(spacing * numerical.sum(values**2 * weights, axis=(-1, -2))))
        return numerical.array(result)

    save()
    try:
        folder = intake / "annular-current-normal-reconstruction"
        own(folder / "status.json")
        owner = json.loads((folder / "status.json").read_text())
        verify("normal_reconstruction_owner_complete", owner["state"] == "complete" and owner["passed"] == owner["total"] == 526 and (folder / "COMPLETE").exists())
        verify("normal_execution_snapshot", own(folder / "executed-script.py") == owner["script_sha256"])
        verify("normal_inputs_unchanged", all(own(root / name) == digest for name, digest in owner["inputs"].items()))
        own(Path(__file__))
        alpha, mixed, wave, momentum_mass, momentum_shift, flux_mass, flux_shift = symbolic.symbols("alpha mixed wave momentum_mass momentum_shift flux_mass flux_shift", nonzero=True)
        velocity = symbolic.Matrix([[0, mixed / alpha, 1 / alpha, -momentum_mass / alpha, -momentum_shift / alpha]])
        flux = mixed * velocity + symbolic.Matrix([[0, wave, 0, flux_mass, flux_shift]])
        reduced_flux = flux - symbolic.Matrix([[0, 0, 0, flux_mass, 0]])
        matrix = symbolic.Matrix.vstack(symbolic.Matrix([[1, 0, 0, 0, 0]]), velocity, reduced_flux, symbolic.Matrix([[0, 0, 0, 1, 0]]), symbolic.Matrix([[0, 0, 0, 0, 1]]))
        determinant = symbolic.factor(matrix.det())
        verify("symbolic_normal_determinant_minus_c_over_alpha", symbolic.simplify(determinant + wave / alpha) == 0, str(determinant))
        verify("characteristic_c_zero_is_not_invertible", symbolic.simplify(determinant.subs(wave, 0)) == 0)
        stored = {}
        for entry in owner["runs"]:
            path = folder / entry["artifact"]
            verify(path.stem + "_hash", own(path) == entry["sha256"])
            with numerical.load(path, allow_pickle=False) as arrays:
                radii, coefficients = arrays["radius"], arrays["Hermite_coefficients"][0]
                saved_z = arrays["nodes_Z_variation"]
            spacing = float(radii[1] - radii[0])
            first, second = norms(coefficients, spacing, 8), norms(coefficients, spacing, 10)
            verify(path.stem + "_H4_polynomial_quadrature_8_vs10", numerical.all(numerical.abs(first - second) <= 1e-10 * numerical.maximum(first, second) + 1e-25))
            verify(path.stem + "_finite_H4_norms", numerical.all(numerical.isfinite(first)))
            report["norms"].append({"case": entry["case"], "time": entry["time"], "intervals": entry["intervals"], "method": entry["method"], "component_order": ["chi", "w", "h", "mu", "delta"], "derivative_L2_norms_orders0to4": first.tolist(), "H4_norm_by_component": numerical.sqrt(numerical.sum(first**2, axis=0)).tolist()})
            stored[entry["case"], entry["time"], entry["intervals"], entry["method"]] = (coefficients, saved_z)
        time_folder = intake / "annular-coupled-current-time-jets"
        own(time_folder / "status.json")
        time_owner = json.loads((time_folder / "status.json").read_text())
        for case_name in ["canonical", "nonlinear_modulated"]:
            path = intake / "annular-constraint-correction-initial" / (case_name + ".json")
            own(path)
            evaluator = AnnularFields(json.loads(path.read_text()))
            for time_value in [0.1, 0.3]:
                label = case_name + "_T" + str(time_value)
                entry = next(row for row in time_owner["runs"] if row["case"] == case_name and row["time"] == time_value and row["intervals"] == 512)
                path = time_folder / entry["artifact"]
                verify(label + "_time_hash", own(path) == entry["sha256"])
                with numerical.load(path, allow_pickle=False) as arrays:
                    radii, derivatives, sources = [arrays[key] for key in ["radius", "current_time_derivatives", "numerical_source_time_coefficients"]]
                engine = CoupledCurrentTimeJets(evaluator, radii, time_value)
                systems = {method: construct_system(engine, derivatives, sources, method) for method in ["poly7", "poly9"]}
                jets = {method: solve_jets(system, derivatives) for method, system in systems.items()}
                lower, upper = systems["poly7"], systems["poly9"]
                delta_radial = jets["poly9"][0, 1] - jets["poly7"][0, 1]
                state = jets["poly7"][0, 0]
                constraint_gradient = engine.current["constraint_gradient"][0]
                delta_gradient_radial = upper["coefficients"]["constraint_gradient"][0, 1] - lower["coefficients"]["constraint_gradient"][0, 1]
                mass_channels = numerical.stack([upper["constraint"][0, 1] - lower["constraint"][0, 1], numerical.sum(delta_gradient_radial * state, axis=0), numerical.sum(constraint_gradient * delta_radial, axis=0)])
                actual_mass_second = 2 * (jets["poly9"][0, 2][3] - jets["poly7"][0, 2][3])
                verify(label + "_mass_second_jet_constraint_decomposition", maximum(mass_channels.sum(axis=0) - actual_mass_second) < 1e-9 * maximum(actual_mass_second) + 1e-24)
                background = engine.current["background"][0]
                lapse = 1 - 2 * background[3] / radii - evaluator.constants["Lambda"] * radii**2 / 3
                shift_second = 2 * (jets["poly9"][0, 2][4] - jets["poly7"][0, 2][4])
                channels = numerical.concatenate([2 * mass_channels / radii, (-2 * lapse * shift_second)[None]], axis=0)
                actual_z = stored[case_name, time_value, 512, "poly9"][1] - stored[case_name, time_value, 512, "poly7"][1]
                verify(label + "_normal_Z_four_channel_identity", maximum(channels.sum(axis=0) - actual_z) < 1e-7 * maximum(actual_z) + 1e-23)
                report["cases"].append({"case": case_name, "time": time_value, "Z_difference_max": maximum(actual_z), "channel_names": ["retained_constraint_radial", "constraint_coefficient_radial", "changed_current_radial", "lapse_second_radial"], "channel_maxima": numerical.max(numerical.abs(channels), axis=-1).tolist(), "all_row_triangle_max": maximum(numerical.abs(channels).sum(axis=0)), "remainder_max": maximum(channels.sum(axis=0) - actual_z)})
                for method in ["poly7", "poly9"]:
                    differences = []
                    for intervals in [256, 512]:
                        high = stored[case_name, time_value, intervals, method][0]
                        low = stored[case_name, time_value, intervals // 2, method][0]
                        difference = norms(high, 4 / intervals, 8, low)
                        differences.append(difference)
                    combined = [numerical.sqrt(numerical.sum(value**2, axis=0)) for value in differences]
                    report["refinement"].append({"case": case_name, "time": time_value, "method": method, "N128_to256_derivative_L2_differences": differences[0].tolist(), "N256_to512_derivative_L2_differences": differences[1].tolist(), "H4_difference_ratio_by_component": (combined[0] / numerical.maximum(combined[1], 1e-30)).tolist(), "H4_fine_difference_by_component": combined[1].tolist(), "unknown_continuum_bound": False})
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
