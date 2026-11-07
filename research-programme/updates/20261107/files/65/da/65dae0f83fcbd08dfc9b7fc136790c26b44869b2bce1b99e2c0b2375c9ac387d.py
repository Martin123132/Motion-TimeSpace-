import csv
import os
from datetime import datetime, timezone

from common import ROOT, SOURCE, EARLY, guard, modest, require, digest, read, write
import numpy as np
from scipy.interpolate import CubicSpline, PchipInterpolator
from scipy.optimize import brentq
from probe_analysis import fields, physical, norm_error

GATE = 2e-5
ALGEBRA = 1e-10


def norm(value):
    return max(float(np.max(np.abs(value))), 1e-30)


def full_packet(model):
    path = SOURCE / f"phase-resolved/packets/{model}-3-one.npz"
    owner = read(SOURCE / "phase-resolved/tangent-native-result.json")
    record = next(row for row in owner["reports"] if row["model"] == model and row["tag"] == "one")
    require(digest(path) == record["sha256"], "packet owner")
    with np.load(path) as archive:
        data = {key: archive[key].copy() for key in archive.files}
    first, last = int(data["original_indices"][0]), int(data["original_indices"][-1])
    data["times"] = data["full_times"][first:last + 1]
    data["standard"] = data["full_standard"][first:last + 1]
    data["observer"] = data["full_observer"][first:last + 1]
    return data, dict(path=str(path), sha256=record["sha256"], first=first, last=last)


def cells(times, frequency):
    phase_integral = CubicSpline(times, frequency).antiderivative()
    origin = float(phase_integral(times[0]))
    total = float(phase_integral(times[-1]) - origin)
    complete = int(np.floor(total / (2 * np.pi)))
    boundaries = [float(times[0])]
    for cycle in range(1, complete + 1):
        target = 2 * np.pi * cycle
        boundaries.append(float(brentq(lambda stamp: phase_integral(stamp) - origin - target, boundaries[-1], times[-1], xtol=1e-12)))
    if times[-1] - boundaries[-1] > 1e-10:
        boundaries.append(float(times[-1]))
    return np.asarray(boundaries), complete, total


def integrals(times, arrays, boundaries, stride=1, positive=False):
    indices = np.unique(np.r_[np.arange(0, len(times), stride), len(times) - 1])
    values = np.column_stack([arrays[name] for name in arrays])
    interpolator = (PchipInterpolator if positive else CubicSpline)(times[indices], values[indices], axis=0)
    primitive = interpolator.antiderivative()
    integral = np.diff(primitive(boundaries), axis=0)
    endpoint = interpolator(boundaries)
    return {name: integral[:, index] for index, name in enumerate(arrays)}, {name: endpoint[:, index] for index, name in enumerate(arrays)}


def model_history(model):
    data, owner = full_packet(model)
    names = data["observer_names"].tolist()
    value = lambda name: data["observer"][:, names.index(name)]
    state = physical(data, model)
    wave = float(data["k"])
    times = data["times"]
    scale, hubble = value("a_native"), value("H_native")
    total_enthalpy = value("R") + value("Pbar")
    phi, psi = state["Phi"], state["Psi"]
    phip = -hubble * psi + state["Q"] / (2 * wave)
    psip = 2 * value("Weyl_prime") - phip
    hubblep = hubble**2 - total_enthalpy / 2
    potential = 2 * hubble**2 - total_enthalpy / 2
    background, speed, mass = fields("heavy")
    mu = scale * mass
    omega = np.sqrt(wave**2 + mu**2)
    boundaries, complete, total_phase = cells(times, mu + omega)
    quantities, budgets, fast_endpoints, identities = {}, {}, {}, {}
    if model == "cold":
        alpha = value("sigma") / wave
        density = value("R_cdm") * (value("delta_cdm64") - 3 * hubble * alpha)
        pressure = np.zeros_like(density)
        momentum = value("R_cdm") * wave * alpha
        enthalpy = value("R_cdm")
    else:
        field = background(np.log(scale))
        velocity = speed(np.log(scale))
        perturbation = state["u"]
        perturbationp = state["p"] + velocity * (psi + 3 * phi)
        density = velocity * perturbationp - velocity**2 * psi + mu**2 * field * perturbation
        pressure = velocity * perturbationp - velocity**2 * psi - mu**2 * field * perturbation
        momentum = wave * velocity * perturbation
        enthalpy = velocity**2
        chi, chip = scale * field, scale * (velocity + hubble * field)
        xi, xip = scale * perturbation, scale * (perturbationp + hubble * perturbation)
        oscillator = (mu * chi + 1j * chip) / np.sqrt(2 * mu)
        response = (omega * xi + 1j * xip) / np.sqrt(2 * omega)
        mup, omegap = hubble * mu, hubble * mu**2 / omega
        drive = scale * velocity * (psip + 3 * phip) - 2 * scale * mu**2 * field * psi
        oscillator_slow_rate = hubble * oscillator.conjugate() / 2 + 1j * potential * chi / np.sqrt(2 * mu)
        response_slow_rate = omegap * response.conjugate() / (2 * omega) + 1j * (potential * xi + drive) / np.sqrt(2 * omega)
        gb, gc = 1 / (scale * np.sqrt(2 * mu)), 1 / (scale * np.sqrt(2 * omega))
        gbp, gcp = -1.5 * hubble * gb, gc * (-hubble - omegap / (2 * omega))
        fb, fc = gb * (-hubble - 1j * mu), gc * (-hubble - 1j * omega)
        fbp = gbp * (-hubble - 1j * mu) + gb * (-hubblep - 1j * mup)
        fcp = gcp * (-hubble - 1j * omega) + gc * (-hubblep - 1j * omegap)
        product = oscillator * response
        difference = oscillator * response.conjugate()
        coefficients = dict(D=fb * fc + mu**2 * gb * gc, P=fb * fc - mu**2 * gb * gc, Q=wave * fb * gc)
        mass_rate = 2 * mu * mup * gb * gc + mu**2 * (gbp * gc + gb * gcp)
        coefficient_rates = dict(D=fbp * fc + fb * fcp + mass_rate, P=fbp * fc + fb * fcp - mass_rate, Q=wave * (fbp * gc + fb * gcp))
        slow_coefficients = dict(D=fb * fc.conjugate() + mu**2 * gb * gc, P=fb * fc.conjugate() - mu**2 * gb * gc, Q=wave * fb * gc)
        lapse_slow = -2 * psi * abs(fb * oscillator)**2
        lapse_coefficient = -psi * fb**2
        lapse_rate = -psip * fb**2 - 2 * psi * fb * fbp
        lapse_fast = 2 * np.real(lapse_coefficient * oscillator**2)
        frequency = mu + omega
        frequencyp = mup + omegap
        for name in ("D", "P", "Q"):
            coefficient = coefficients[name]
            quantities[name + "_slow"] = 2 * np.real(slow_coefficients[name] * difference)
            quantities[name + "_fast"] = 2 * np.real(coefficient * product)
            derivative = coefficient_rates[name] * product + coefficient * (oscillator_slow_rate * response + oscillator * response_slow_rate) - frequencyp / frequency * coefficient * product
            budgets[name] = np.abs(2 * derivative / frequency)
            fast_endpoints[name] = 2 * coefficient * product / frequency
        quantities["lapse_slow"], quantities["lapse_fast"] = lapse_slow, lapse_fast
        budgets["lapse"] = np.abs((lapse_rate * oscillator**2 + 2 * lapse_coefficient * oscillator * oscillator_slow_rate - hubble * lapse_coefficient * oscillator**2) / mu)
        fast_endpoints["lapse"] = lapse_coefficient * oscillator**2 / mu
        for name, actual in dict(D=density, P=pressure, Q=momentum).items():
            reconstruction = quantities[name + "_slow"] + quantities[name + "_fast"]
            if name != "Q":
                reconstruction += lapse_slow + lapse_fast
            identities[name + "_reconstruction"] = norm_error(reconstruction - actual, actual)
        denominator = mu * (omega + mu) + hubble**2 * omega / mu
        density_coefficient = 1 - 2 * mu**2 / denominator
        current_coefficient = 2 * mu * hubble * (omega - mu) / denominator
        projected_density = quantities["D_slow"] + lapse_slow
        projected_pressure = quantities["P_slow"] + lapse_slow
        relation = density_coefficient * projected_density + current_coefficient * quantities["Q_slow"] / wave + (1 - density_coefficient) * lapse_slow
        identities["projected_pressure"] = norm_error(projected_pressure - relation, pressure)
        require(np.all(denominator > 0), "regular denominator")
        beat_coefficient = wave**2 / (omega + mu)**2
        quantities["P_projected"] = projected_pressure
        quantities["P_leading_closure"] = beat_coefficient * (density + 3 * hubble * momentum / wave)
        quantities["P_expansion_current_lapse_remainder"] = (density_coefficient - beat_coefficient) * projected_density + (current_coefficient - 3 * hubble * beat_coefficient) * quantities["Q_slow"] / wave + (1 - density_coefficient) * lapse_slow
        quantities["P_fast_closure_remainder"] = quantities["P_fast"] - beat_coefficient * quantities["D_fast"] - 3 * hubble * beat_coefficient * quantities["Q_fast"] / wave + (1 - beat_coefficient) * lapse_fast
        identities["closure_remainder_split"] = norm_error(pressure - quantities["P_leading_closure"] - quantities["P_expansion_current_lapse_remainder"] - quantities["P_fast_closure_remainder"], pressure)
        action = abs(oscillator)**2
        action_rate = hubble * np.real(oscillator**2) + potential / mu * np.imag(oscillator**2)
        energy_mass = scale * (velocity**2 + mu**2 * field**2) / (2 * mass)
        action_energy = action - hubble / mu * chi * chip + hubble**2 * chi**2 / (2 * mu)
        identities["action_energy"] = norm_error(energy_mass - action_energy, energy_mass)
        quantities.update(action=action, action_rate=action_rate, comoving_energy_over_mass=energy_mass)
    quantities.update(D=density, P=pressure, Q=momentum)
    quantities["D_rate"] = -hubble * (density + 3 * pressure) - wave * momentum + 3 * enthalpy * phip
    quantities["Q_rate"] = -2 * hubble * momentum + wave * (pressure + enthalpy * psi)
    require(all(np.isfinite(array).all() for array in quantities.values()), "finite physical source")
    integral, endpoint = integrals(times, quantities, boundaries)
    widths = np.diff(boundaries)
    means = {name: array / widths for name, array in integral.items()}
    conservation = {}
    for name in ("D", "Q") + (("action",) if model == "heavy" else ()):
        residual = np.diff(endpoint[name]) - integral[name + "_rate"]
        conservation[name] = float(np.max(abs(residual)) / norm(quantities[name]))
    refinements = []
    for stride in (2, 4):
        coarse, coarse_end = integrals(times, quantities, boundaries, stride)
        errors = {name: float(np.max(abs((coarse[name] - integral[name]) / widths)) / norm(quantities[name])) for name in quantities if not name.endswith("_rate")}
        refinements.append(dict(stride=stride, maximum=max(errors.values()), errors=errors))
    budget_reports = []
    if model == "heavy":
        budget_integral, _ = integrals(times, budgets, boundaries, positive=True)
        fast_parts = dict(D=quantities["D_fast"], P=quantities["P_fast"], Q=quantities["Q_fast"], lapse=quantities["lapse_fast"])
        _, fast_boundary = integrals(times, fast_endpoints, boundaries)
        for name, array in fast_parts.items():
            actual = means["lapse_fast" if name == "lapse" else name + "_fast"]
            endpoint_budget = abs(np.diff(fast_boundary[name])) / widths
            bound = endpoint_budget + budget_integral[name] / widths
            numerical_envelope = np.zeros_like(bound)
            budget_errors = {}
            for stride in (2, 4):
                coarse_budget, _ = integrals(times, budgets, boundaries, stride, positive=True)
                _, coarse_boundary = integrals(times, fast_endpoints, boundaries, stride)
                coarse_bound = abs(np.diff(coarse_boundary[name])) / widths + coarse_budget[name] / widths
                change = abs(coarse_bound - bound)
                numerical_envelope = np.maximum(numerical_envelope, change)
                budget_errors[str(stride)] = float(np.max(change) / norm(array))
            slack = bound - abs(actual)
            budget_reports.append(dict(component=name, minimum_slack_source_scaled=float(np.min(slack) / norm(array)), max_bound_source_scaled=float(np.max(bound) / norm(array)), max_observed_average_source_scaled=float(np.max(abs(actual)) / norm(array)), refinement_source_scaled=budget_errors, bounded_with_sampled_envelope=bool(np.all(slack >= -numerical_envelope - GATE * norm(array))), continuum_certified=False))
            means[name + "_fast_budget"] = bound
            means[name + "_fast_budget_quadrature_difference"] = numerical_envelope
    groups = []
    for size in (1, 2, 4):
        rows = []
        for first in range(0, complete - size + 1, size):
            last = first + size
            duration = boundaries[last] - boundaries[first]
            rows.append({name: float(np.sum(integral[name][first:last]) / duration) for name in quantities if not name.endswith("_rate")})
        report = dict(cycles=size, groups=len(rows))
        if rows:
            averaged = {name: np.array([row[name] for row in rows]) for name in rows[0]}
            report["pressure_over_density_sup_norm"] = norm(averaged["P"]) / norm(averaged["D"]) if model == "heavy" else 0.
            if model == "heavy":
                closure_difference = averaged["P"] - averaged["P_leading_closure"]
                report["leading_closure_error_density_scaled"] = norm(closure_difference) / norm(averaged["D"])
                report["leading_closure_error_pressure_scaled"] = norm(closure_difference) / norm(averaged["P"])
                report["projection_error_density_scaled"] = norm(averaged["P"] - averaged["P_projected"]) / norm(averaged["D"])
                report["fast_plus_lapse_pressure_density_scaled"] = norm(averaged["P_fast"] + averaged["lapse_fast"]) / norm(averaged["D"])
            groups.append(report)
    path = ROOT / f"{model}-phase-cells.csv"
    with path.open("x", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=["cell", "left_tau_mpc", "right_tau_mpc", "complete_cycle"] + list(means))
        writer.writeheader()
        for index in range(len(widths)):
            writer.writerow(dict(cell=index + 1, left_tau_mpc=boundaries[index], right_tau_mpc=boundaries[index + 1], complete_cycle=index < complete, **{name: float(array[index]) for name, array in means.items()}))
    algebra_pass = all(error < ALGEBRA for error in identities.values())
    conservation_pass = all(error < GATE for error in conservation.values())
    refinement_pass = all(row["maximum"] < GATE for row in refinements)
    budget_pass = all(row["bounded_with_sampled_envelope"] and max(row["refinement_source_scaled"].values()) < GATE for row in budget_reports)
    report = dict(model=model, packet=owner, points=len(times), wave_mpc=wave, interval_tau_mpc=[float(times[0]), float(times[-1])], a_interval=[float(scale[0]), float(scale[-1])], H_over_mu=[float(np.min(hubble / mu)), float(np.max(hubble / mu))], k_over_mu=[float(np.min(wave / mu)), float(np.max(wave / mu))], complete_cycles=complete, total_phase=total_phase, final_partial_cell=len(widths) > complete, identities=identities, conservation=conservation, refinements=refinements, fast_budgets=budget_reports, window_dependence=groups, algebra_passed=algebra_pass, conservation_passed=conservation_pass, refinement_passed=refinement_pass, sampled_budget_passed=budget_pass, passed=algebra_pass and conservation_pass and refinement_pass and budget_pass, cell_file=str(path), cell_sha256=digest(path), background_file=str(EARLY / f"runs/backgrounds/{model}.npz"), background_sha256=digest(EARLY / f"runs/backgrounds/{model}.npz"))
    return report


def main():
    modest()
    require(read(ROOT / "derivation-result.json")["passed"], "symbolic derivation")
    reports = []
    for model in ("heavy", "cold"):
        guard()
        report = model_history(model)
        reports.append(report)
        print(model, {name: report[name] for name in ("complete_cycles", "identities", "conservation", "window_dependence", "passed")}, flush=True)
    result = dict(passed=all(row["passed"] for row in reports), pid=os.getpid(), finished=datetime.now(timezone.utc).isoformat(), algebra_gate=ALGEBRA, numerical_gate=GATE, reports=reports, source_sha256=digest(__file__), symbolic_sha256=digest(ROOT / "derivation-result.json"), prior_validation_sha256=digest(SOURCE / "validation-result.json"), comparison="retained heavy field response and CDM control; both direct tangents at k=5", averaging_scope="finite saved source interval; no fitted closure, no native rerun; quadrature differences are diagnostics, not rigorous continuum enclosures")
    write(ROOT / "analysis-result.json", result)
    require(result["passed"], "one or more unchanged numerical gates failed; preserve for inspection")
    print("phase stress analysis passed", flush=True)


if __name__ == "__main__":
    main()

