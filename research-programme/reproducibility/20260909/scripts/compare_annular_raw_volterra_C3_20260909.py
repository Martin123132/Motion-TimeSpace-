import hashlib
import json
import math
from datetime import datetime, timezone
from pathlib import Path

from navier_stokes_source_audit_20260908 import limit_process


def run():
    limit_process()
    import numpy as numerical
    from sbp4_derived_operator_20260909 import derivative
    from annular_volterra_source_completion_20260909 import integrate_source
    from annular_volterra_source_completion_20260909 import exponential_moments
    from annular_coordinate_evolution_operator_20260909 import AnnularFields
    from annular_coupled_current_time_jets_20260909 import CoupledCurrentTimeJets

    root = Path(__file__).resolve().parents[1]
    intake = root / "source-intake/navier-stokes/20260909"
    destination = intake / "annular-raw-volterra-C3-matched-comparison"
    destination.mkdir(exist_ok=False)
    source = Path(__file__).read_bytes()
    (destination / "executed-script.py").write_bytes(source)
    report = {"state": "running", "started_utc": datetime.now(timezone.utc).isoformat(), "script_sha256": hashlib.sha256(source).hexdigest(), "inputs": {}, "checks": [], "norms": [], "refinement": [], "source_parity": [], "comparisons": [], "valid_for_physics_claim": False, "scope": "Matched original-versus-raw-source-Volterra comparison. Same C3 data, background, physical boundary data and gates; the centered scalar projection is removed. Source/bulk parity is an instantaneous diagnostic, not a proof of sole causality. Polynomial H3/H4 norms and trace lower bounds are not unknown continuum bounds."}

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

    def load_owner(name, allow_field_failure=False):
        folder = intake / name
        path = folder / "status.json"
        own(path)
        owner = json.loads(path.read_text())
        if allow_field_failure:
            verify(name + "_terminal_field_outcome_retained", owner["state"] in {"complete", "failed"} and "failure" not in owner and owner["active_job"] is None and owner["passed"] == sum(check["passed"] for check in owner["checks"]) and owner["total"] == len(owner["checks"]) and len(owner["runs"]) == 16)
            report["unprojected_field_evolution_passed"] = owner["state"] == "complete" and owner["passed"] == owner["total"]
            report["retained_field_failures"] = [check for check in owner["checks"] if not check["passed"]]
            verify(name + "_failure_not_promoted", (folder / "COMPLETE").exists() == report["unprojected_field_evolution_passed"])
        else:
            verify(name + "_complete", owner["state"] == "complete" and owner["passed"] == owner["total"] and (folder / "COMPLETE").exists())
        verify(name + "_snapshot", own(folder / "executed-script.py") == owner["script_sha256"])
        verify(name + "_inputs_unchanged", all(own(root / name) == digest for name, digest in owner["inputs"].items()))
        return folder, owner

    def load_arrays(folder, entry):
        path = folder / entry["artifact"]
        verify(path.stem + "_hash_" + folder.name, own(path) == entry["sha256"])
        with numerical.load(path, allow_pickle=False) as arrays:
            return {key: arrays[key] for key in arrays.files}

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

    def physical_norm(measured):
        return float(numerical.sqrt(numerical.sum(measured[:4, 0]**2) + numerical.sum(measured[:, [3, 4]]**2)))

    def parity(values, spacing):
        slopes = derivative(values, spacing)
        trace = slopes[:-1] + slopes[1:] - 2 * numerical.diff(values) / spacing
        return ((-1.)**numerical.arange(trace.size) * spacing * trace / 4)[8:-8]

    def rms(values):
        return float(numerical.sqrt(numerical.mean(values**2)))

    save()
    try:
        own(Path(__file__))
        derivation_path = intake / "annular-current-driving-and-passivity-qualified/status.json"
        own(derivation_path)
        derivation = json.loads(derivation_path.read_text())
        verify("source_projection_derivation_complete", derivation["state"] == "complete" and derivation["passed"] == derivation["total"] == 232 and derivation_path.with_name("COMPLETE").exists())
        verify("source_projection_derivation_inputs_unchanged", all(own(root / name) == digest for name, digest in derivation["inputs"].items()))
        own(root / "scripts/sbp4_derived_operator_20260909.py")
        own(root / "scripts/annular_volterra_source_completion_20260909.py")
        toy_radius = numerical.linspace(4, 8, 129)
        toy_spacing = float(toy_radius[1] - toy_radius[0])
        for coefficient in [-0.2, 0, 0.2]:
            constant_coefficient = numerical.full_like(toy_radius, coefficient)
            homogeneous = integrate_source(constant_coefficient, numerical.zeros_like(toy_radius), toy_spacing)
            verify("unique_zero_terminal_homogeneous_" + str(coefficient), maximum(homogeneous) == 0)
            solution = integrate_source(constant_coefficient, numerical.ones_like(toy_radius), toy_spacing)
            exact = toy_radius - 8 if coefficient == 0 else numerical.expm1(coefficient * (toy_radius - 8)) / coefficient
            verify("constant_forcing_integrating_factor_" + str(coefficient), maximum(solution - exact) < 1e-12)
            verify("isolated_mass_supnorm_bound_" + str(coefficient), maximum(solution) <= 4 * numerical.exp(4 * abs(coefficient)))
        alternating = integrate_source(numerical.zeros_like(toy_radius), (-1.)**numerical.arange(toy_radius.size), toy_spacing)
        verify("zero_coefficient_alternating_cell_average", maximum(alternating) == 0)
        load_owner("annular-trace-regularity-lower-bounds")
        load_owner("annular-centered-constraint-mode-diagnosis")
        reconstructions = {
            "original": load_owner("annular-current-normal-reconstruction"),
            "unprojected": load_owner("annular-raw-volterra-C3-normal-reconstruction"),
        }
        evolutions = {
            "original": load_owner("annular-coupled-current-analytic-third-corner"),
            "unprojected": load_owner("annular-coupled-current-third-corner-raw-volterra", allow_field_failure=True),
        }
        preflight_folder, preflight = load_owner("annular-raw-volterra-C3-time-jets-preflight")
        original_inputs, unprojected_inputs = [evolutions[branch][1]["inputs"] for branch in ["original", "unprojected"]]
        matched_initials = [name for name in original_inputs if "annular-analytic-third-corner-initial-data/" in name.replace("\\", "/") and name.endswith(".json")]
        verify("same_frozen_C3_payloads", len(matched_initials) >= 3 and all(unprojected_inputs.get(name) == original_inputs[name] for name in matched_initials))
        verify("same_evolution_parameters_except_mass_completion", all(evolutions["original"][1]["parameters"][key] == evolutions["unprojected"][1]["parameters"][key] for key in ["N", "T", "outputs_T", "epsilon", "sigma", "cfl", "time_interpolation_intervals", "dissipation", "initial_kind", "constraint_addition"]))
        verify("same_field_acceptance_gates", evolutions["original"][1]["gates"] == evolutions["unprojected"][1]["gates"])
        stored = {}
        for branch, (folder, owner) in reconstructions.items():
            for entry in owner["runs"]:
                arrays = load_arrays(folder, entry)
                spacing = float(arrays["radius"][1] - arrays["radius"][0])
                coefficients = arrays["Hermite_coefficients"][0]
                measured, control = norms(coefficients, spacing), norms(coefficients, spacing, 10)
                tag = branch + "_" + entry["artifact"]
                verify(tag + "_8vs10_quadrature", numerical.all(numerical.abs(measured - control) <= 1e-10 * numerical.maximum(measured, control) + 1e-25))
                values = arrays["normalized_current_jet_(0, 0)"]
                slopes = arrays["normalized_current_jet_(0, 1)"]
                curvatures = 2 * arrays["normalized_current_jet_(0, 2)"]
                secant = numerical.diff(values, axis=-1) / spacing
                third_trace = slopes[:, :-1] + slopes[:, 1:] - 2 * secant
                left = curvatures[:, :-1] + (4 * slopes[:, :-1] + 2 * slopes[:, 1:] - 6 * secant) / spacing
                right = curvatures[:, 1:] + (6 * secant - 2 * slopes[:, :-1] - 4 * slopes[:, 1:]) / spacing
                lower3_squared = 30 * numerical.sum(third_trace**2, axis=-1) / spacing**3
                lower4_squared = numerical.sum(30 * (left + right)**2 + 210 * (left - right)**2, axis=-1) / spacing**3
                verify(tag + "_all_cell_trace_bounds", numerical.all(lower3_squared <= measured[3]**2 * (1 + 1e-8) + 1e-30) and numerical.all(lower4_squared <= measured[4]**2 * (1 + 1e-8) + 1e-30))
                mass_trace = third_trace[3, 8:-8]
                denominator = numerical.linalg.norm(mass_trace[:-1]) * numerical.linalg.norm(mass_trace[1:])
                correlation = float(numerical.dot(mass_trace[:-1], mass_trace[1:]) / denominator) if denominator else None
                row = {key: entry[key] for key in ["case", "time", "intervals", "method"]}
                row.update(branch=branch, derivative_L2_norms_orders0to4=measured.tolist(), mass_H4_trace_lower_bound_all_cells=float(numerical.sqrt(lower4_squared[3])), physical_H3chi_H4mu_H4delta_lower_bound=float(numerical.sqrt(lower3_squared[0] + lower4_squared[3] + lower4_squared[4])), measured_physical_H3chi_H4mu_H4delta_norm=physical_norm(measured), mass_trace_lag1_cosine_excluding8_cells=correlation, mass_alternating_amplitude_RMS_diagnostic=rms(spacing * mass_trace / 4), valid_for_physics_claim=False)
                report["norms"].append(row)
                stored[branch, entry["case"], entry["time"], entry["intervals"], entry["method"]] = coefficients
        cell_engines = {}
        for branch, (folder, owner) in evolutions.items():
            for entry in owner["runs"]:
                if entry["time_refinement"] != (2 if entry["intervals"] == 512 else 1):
                    continue
                arrays = load_arrays(folder, entry)
                spacing = float(arrays["radius"][1] - arrays["radius"][0])
                mass_rhs, mass_source = arrays["current_rhs"][3], arrays["numerical_source"][3]
                bulk = mass_rhs - mass_source
                cell_key = entry["case"], entry["time"], entry["intervals"]
                if cell_key not in cell_engines:
                    case_path = intake / "annular-constraint-correction-initial" / (entry["case"] + ".json")
                    own(case_path)
                    evaluator = AnnularFields(json.loads(case_path.read_text()))
                    cell_engines[cell_key] = CoupledCurrentTimeJets(evaluator, arrays["radius"], entry["time"])
                gradient = cell_engines[cell_key].current["old_gradient"][0]
                forcing = gradient[1] * arrays["coordinate_numerical_source"][1] + gradient[3] * arrays["coordinate_numerical_source"][3]
                argument = -spacing * (gradient[2, :-1] + gradient[2, 1:]) / 2
                first_moment, weighted_moment = exponential_moments(argument)
                cell_terms = numerical.stack([mass_source[:-1], -numerical.exp(argument) * mass_source[1:], spacing * (first_moment - weighted_moment) * forcing[:-1], spacing * weighted_moment * forcing[1:]])
                cell_residual = maximum(cell_terms.sum(axis=0))
                cell_scale = maximum(cell_terms)
                if branch == "unprojected":
                    verify(entry["artifact"] + "_actual_source_cell_balance", cell_residual <= 1e-10 * cell_scale + 1e-25 and abs(float(mass_source[-1])) < 1e-25, {"residual": cell_residual, "scale": cell_scale, "full_evolved_mass_constraint_claimed": False})
                source_indicator, bulk_indicator, rhs_indicator = [parity(values, spacing) for values in [mass_source, bulk, mass_rhs]]
                verify(branch + "_" + entry["artifact"] + "_linear_parity_decomposition", maximum(source_indicator + bulk_indicator - rhs_indicator) < 1e-10 * max(rms(source_indicator), rms(bulk_indicator)) + 1e-25)
                row = {key: entry[key] for key in ["case", "time", "intervals"]}
                row.update(branch=branch, source_parity_RMS=rms(source_indicator), bulk_parity_RMS=rms(bulk_indicator), RHS_parity_RMS=rms(rhs_indicator), field_parity_RMS=rms(parity(arrays["correction_current"][3], spacing)), source_cell_balance_residual=cell_residual, source_cell_balance_scale=cell_scale, diagnostic_not_claim=True)
                if branch == "original":
                    probe = next(item for item in preflight["runs"] if all(item[key] == entry[key] for key in ["case", "time", "intervals", "time_refinement"]))
                    probe_arrays = load_arrays(preflight_folder, probe)
                    replacement = probe_arrays["coordinate_source_time_coefficients"][0, 2]
                    row["same_state_unprojected_mass_source_parity_RMS"] = rms(parity(replacement, spacing))
                    row["same_state_unprojected_counterfactual_RHS_parity_RMS"] = rms(parity(bulk + replacement, spacing))
                    row["same_state_mass_source_change_max"] = maximum(replacement - mass_source)
                report["source_parity"].append(row)
        for case_name in ["canonical", "nonlinear_modulated"]:
            for time_value in [0.1, 0.3]:
                for method in ["poly7", "poly9"]:
                    row = {"case": case_name, "time": time_value, "method": method, "branches": {}, "continuum_bound_available": False}
                    for branch in ["original", "unprojected"]:
                        differences = [norms(stored[branch, case_name, time_value, intervals, method], 4 / intervals, coarse=stored[branch, case_name, time_value, intervals // 2, method]) for intervals in [256, 512]]
                        row["branches"][branch] = {"physical_coarse_difference": physical_norm(differences[0]), "physical_fine_difference": physical_norm(differences[1]), "physical_ratio": physical_norm(differences[0]) / max(physical_norm(differences[1]), 1e-30), "derivative_L2_differences_coarse": differences[0].tolist(), "derivative_L2_differences_fine": differences[1].tolist()}
                    report["refinement"].append(row)
                original, unprojected = [next(row for row in report["norms"] if row["branch"] == branch and row["case"] == case_name and row["time"] == time_value and row["intervals"] == 512 and row["method"] == "poly7") for branch in ["original", "unprojected"]]
                field = {branch: next(row for row in evolutions[branch][1]["comparisons"] if row["case"] == case_name and row["time"] == time_value) for branch in ["original", "unprojected"]}
                curvature = {branch: next(row for row in reconstructions[branch][1]["sensitivity"] if row["case"] == case_name and row["time"] == time_value) for branch in ["original", "unprojected"]}
                report["comparisons"].append({"case": case_name, "time": time_value, "unprojected_over_original_mass_H4_trace_floor": unprojected["mass_H4_trace_lower_bound_all_cells"] / max(original["mass_H4_trace_lower_bound_all_cells"], 1e-30), "unprojected_over_original_physical_norm": unprojected["measured_physical_H3chi_H4mu_H4delta_norm"] / max(original["measured_physical_H3chi_H4mu_H4delta_norm"], 1e-30), "field": field, "curvature": curvature, "valid_for_physics_claim": False})
        verify("all_comparison_rows_present", len(report["norms"]) == 48 and len(report["source_parity"]) == 24 and len(report["refinement"]) == 8 and len(report["comparisons"]) == 4)
        report["all_unprojected_curvature_sensitivity_gates_passed"] = reconstructions["unprojected"][1]["all_curvature_sensitivity_gates_passed"]
        report["all_unprojected_strong_mesh_differences_reduced"] = all(row["branches"]["unprojected"]["physical_ratio"] >= 1.3 for row in report["refinement"])
        report["next_target"] = "Select from the actual matched source, field, curvature and strong-norm results; no physical promotion or automatic finer mesh."
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
