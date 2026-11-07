import csv
import os
from common import ROOT, PHASE, modest, guard, require, read, write, digest
import numpy as np
from scipy.interpolate import CubicSpline

GATE = 2e-5
ALGEBRA = 1e-10


def load(path):
    with np.load(path) as archive:
        return {name: archive[name].copy() for name in archive.files}


def scale(values):
    return np.maximum(np.max(abs(values), axis=0), 1e-30)


def error(predicted, reference):
    return float(np.max(abs(predicted - reference) / scale(reference)))


def cell_means(packet, boundaries):
    locations = np.searchsorted(packet["times"], boundaries)
    require(np.array_equal(packet["times"][locations], boundaries), "frozen boundaries included")
    return np.diff(packet["integrals"][locations], axis=0) / np.diff(boundaries)[:, None]


def newton_budget(model, inputs, full, poisson):
    times = full["times"]
    require(np.array_equal(times, poisson["times"]), "Newton times")
    values = CubicSpline(inputs["times"], inputs["inputs"], axis=0)(times)
    hubble, enthalpy, background, speed, mu = values[:, 1], values[:, 2], values[:, 4], values[:, 5], values[:, 6]
    wave = float(inputs["wave"])
    phi_poisson_on_full = -full["Dstar_total"] / (2 * wave**2 + 3 * enthalpy)
    delta_phi = full["Phi"] - phi_poisson_on_full
    delta_psi = full["Psi"] - phi_poisson_on_full
    if model == "heavy":
        drive = np.column_stack([speed * (delta_psi + 3 * delta_phi), mu**2 * background * (3 * delta_phi - delta_psi), np.zeros_like(times), wave**2 * delta_psi])
    else:
        drive = np.column_stack([np.zeros_like(times), wave**2 * delta_psi])
    normalization = inputs["normalization"]
    transition = poisson["fundamental"]
    condition = float(np.max(np.linalg.cond(transition)))
    inverse_drive = np.linalg.solve(transition, (drive / normalization)[..., None])[..., 0]
    spline = CubicSpline(times, inverse_drive, axis=0)
    primitive = spline.antiderivative()
    inferred = np.einsum("nij,nj->ni", transition, primitive(times) - primitive(times[0])) * normalization
    actual = full["state"] - poisson["state"]
    remainder = error(inferred - actual, np.zeros_like(actual) + scale(full["state"]))
    widths = np.diff(times)
    local = sum(abs(spline.c[index]) * widths[:, None]**(4 - index) / (4 - index) for index in range(4))
    prefix = np.vstack([np.zeros(len(normalization)), np.cumsum(local, axis=0)])
    bound = np.einsum("nij,nj->ni", abs(transition), prefix) * normalization
    state_scale = scale(full["state"])
    violation = float(np.max((abs(actual) - bound) / state_scale))
    np.savez_compressed(ROOT / (model + "-newton-budget.npz"), times=times, actual_difference=actual, duhamel_difference=inferred, interpolant_bound=bound, state_scale=state_scale)
    report = dict(maximum_transition_condition=condition, duhamel_residual_state_scaled=remainder, interpolant_bound_violation_state_scaled=violation, actual_difference_state_scaled=(np.max(abs(actual), axis=0) / state_scale).tolist(), maximum_bound_state_scaled=(np.max(bound, axis=0) / state_scale).tolist(), final_difference_state_scaled=(actual[-1] / state_scale).tolist(), final_bound_state_scaled=(bound[-1] / state_scale).tolist(), passed=bool(condition < 1e10 and remainder < GATE and violation < GATE), continuum_certified=False, bound_scope="coefficientwise absolute integral bound for cubic interpolation of the transformed driving; transition matrix and continuum quadrature remain numerical")
    report["file"] = model + "-newton-budget.npz"
    report["sha256"] = digest(ROOT / report["file"])
    return report


def main():
    modest()
    manifest = read(ROOT / "input-manifest.json")
    prediction = read(ROOT / "prediction-result.json")
    require(prediction["state"] == "complete" and len(prediction["reports"]) == 18, "complete frozen forward runs")
    require(prediction["source_sha256"] == digest(ROOT / "run_window_feedback.py"), "runner source")
    for record in prediction["reports"]:
        require(record["sha256"] == digest(ROOT / "predictions" / record["file"]), "prediction owner")
    reports = []
    csv_rows = []
    for owner in manifest["rows"]:
        guard()
        model = owner["model"]
        require(digest(ROOT / owner["reference_file"]) == owner["reference_sha256"], "reference owner")
        require(digest(ROOT / owner["input_file"]) == owner["input_sha256"], "input owner")
        inputs, reference = load(ROOT / owner["input_file"]), load(ROOT / owner["reference_file"])
        packets = {record["case"]["tag"]: load(ROOT / "predictions" / record["file"]) for record in prediction["reports"] if record["model"] == model}
        full = packets["full"]
        indices = np.searchsorted(full["times"], reference["times"])
        require(np.array_equal(full["times"][indices], reference["times"]), "reference times")
        state_error = error(full["state"][indices], reference["state"])
        source_errors = {name: error(full[name][indices], reference[name]) for name in ("D", "P", "Q", "Phi", "Psi")}
        refinements = {}
        for tag in ("source2", "source4", "precision"):
            candidate = packets[tag]
            refinements[tag] = dict(state=error(candidate["state"], full["state"]), **{name: error(candidate[name], full[name]) for name in ("D", "P", "Q", "Phi", "Psi")})
        algebra = {}
        values = CubicSpline(inputs["times"], inputs["inputs"], axis=0)(full["times"])
        wave = float(inputs["wave"])
        hubble, enthalpy, shear = values[:, 1], values[:, 2], values[:, 9]
        for name, terms in dict(Hamiltonian=[2 * wave**2 * full["Phi"], full["D_total"], 3 * hubble * full["Q_total"] / wave], slip=[full["Phi"], -full["Psi"], -shear / wave**2]).items():
            algebra[name] = float(np.max(abs(np.sum(terms, axis=0))) / max(float(np.max(abs(terms))), 1e-30))
        momentum_rate = -hubble * full["Psi"] + full["Q_total"] / (2 * wave)
        momentum_integral = CubicSpline(full["times"], momentum_rate).antiderivative()
        momentum_prediction = full["Phi"][0] + momentum_integral(full["times"]) - momentum_integral(full["times"][0])
        momentum_error = error(momentum_prediction, full["Phi"])
        boundaries = inputs["boundaries"]
        means = cell_means(full, boundaries)
        with (PHASE / (model + "-phase-cells.csv")).open(newline="", encoding="utf-8") as stream:
            old_cells = list(csv.DictReader(stream))
        expected_means = np.array([[float(row[name]) for name in ("D", "P", "Q")] for row in old_cells])
        raw_scales = np.array([scale(reference[name]) for name in ("D", "P", "Q")])
        mean_errors = np.max(abs(means - expected_means), axis=0) / raw_scales
        complete = np.array([row["complete_cycle"] == "True" for row in old_cells])
        complete_pressure_error = float(np.max(abs(means[complete, 1] - expected_means[complete, 1])) / max(float(np.max(abs(expected_means[complete, 1]))), 1e-30))
        mean_refinements = {tag: (np.max(abs(cell_means(packets[tag], boundaries) - means), axis=0) / raw_scales).tolist() for tag in ("source2", "source4", "precision")}
        negative_error = max(error(-packets["negative"]["state"], full["state"]), max(error(-packets["negative"][name], full[name]) for name in ("D", "P", "Q", "Phi", "Psi")))
        zero_exact = all(np.count_nonzero(packets["zero"][name]) == 0 for name in ("state", "integrals", "D", "P", "Q", "Phi", "Psi"))
        feedback_change = dict(state=(np.max(abs(packets["feedback-off"]["state"] - full["state"]), axis=0) / scale(full["state"])).tolist(), metric=error(packets["feedback-off"]["Psi"], full["Psi"]))
        poisson = packets["poisson"]
        poisson_refinement = error(packets["poisson-precision"]["state"], poisson["state"])
        poisson_identity = float(np.max(abs(2 * wave**2 * poisson["Psi"] + poisson["D_total"])) / max(float(np.max(abs(poisson["D_total"]))), 1e-30))
        budget = newton_budget(model, inputs, full, poisson)
        toleranced = [state_error, momentum_error, negative_error, poisson_refinement, *source_errors.values(), *mean_errors.tolist()]
        toleranced += [value for row in refinements.values() for value in row.values()]
        toleranced += [value for row in mean_refinements.values() for value in row]
        passed = max(toleranced) < GATE and max(algebra.values()) < ALGEBRA and poisson_identity < ALGEBRA and zero_exact and budget["passed"]
        report = dict(model=model, passed=bool(passed), state_error=state_error, source_errors=source_errors, refinements=refinements, algebra=algebra, integrated_momentum_constraint_error=momentum_error, window_mean_errors_raw_source_scaled=mean_errors.tolist(), complete_window_pressure_error_pressure_scaled=complete_pressure_error, window_mean_refinements_raw_source_scaled=mean_refinements, negative_direction_error=negative_error, zero_direction_exact=zero_exact, feedback_off_difference=feedback_change, poisson_precision_difference=poisson_refinement, poisson_density_identity=poisson_identity, newton_budget=budget, selected_future_state_supplied=False, other_species_history_supplied=True)
        reports.append(report)
        for index, row in enumerate(old_cells):
            csv_rows.append(dict(model=model, cell=index + 1, left_tau_mpc=boundaries[index], right_tau_mpc=boundaries[index + 1], complete_cycle=row["complete_cycle"], D_predicted=means[index, 0], D_saved=expected_means[index, 0], P_predicted=means[index, 1], P_saved=expected_means[index, 1], Q_predicted=means[index, 2], Q_saved=expected_means[index, 2]))
        print(report, flush=True)
    output = ROOT / "window-comparison.csv"
    with output.open("x", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(csv_rows[0]))
        writer.writeheader()
        writer.writerows(csv_rows)
    result = dict(passed=all(row["passed"] for row in reports), pid=os.getpid(), reports=reports, gate=GATE, algebra_gate=ALGEBRA, source_sha256=digest(__file__), prediction_sha256=digest(ROOT / "prediction-result.json"), input_manifest_sha256=digest(ROOT / "input-manifest.json"), window_csv_sha256=digest(output), physical_scope="conditional selected-matter self-gravity and exact pressure; other species prescribed, no fitted closure")
    write(ROOT / "comparison-result.json", result)
    require(result["passed"], "unchanged gate failed; preserve and diagnose")


if __name__ == "__main__":
    main()

