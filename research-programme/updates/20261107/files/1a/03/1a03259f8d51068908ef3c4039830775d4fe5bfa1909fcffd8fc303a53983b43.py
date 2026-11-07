import csv
from common import ROOT, CLOSURE, WAVE, GATE, ALGEBRA, modest, guard, require, check_prior, read, write, digest, load
import numpy as np
from scipy.interpolate import CubicSpline
import sympy as sy


def norm(array):
    return float(np.max(abs(array)))


def scale(array):
    return max(norm(array), 1e-80)


def symbolic():
    hubble, wave, metric_z, field, velocity, field_rate, velocity_rate, mass_a, delta, delta_rate = sy.symbols("H k z phi v phip vp am d dp", real=True)
    acceleration = -2 * hubble * delta_rate - wave * metric_z * velocity - (wave ** 2 + mass_a ** 2) * delta
    density = velocity * delta_rate + mass_a ** 2 * field * delta
    pressure = velocity * delta_rate - mass_a ** 2 * field * delta
    flux = wave * velocity * delta
    density_rate = velocity_rate * delta_rate + velocity * acceleration + mass_a ** 2 * ((2 * hubble * field + field_rate) * delta + field * delta_rate)
    flux_rate = wave * (velocity_rate * delta + velocity * delta_rate)
    defect_field = field_rate - velocity
    defect_velocity = velocity_rate + 2 * hubble * velocity + mass_a ** 2 * field
    continuity = density_rate + hubble * (density + 3 * pressure) + wave * flux + wave * metric_z * velocity ** 2
    momentum = flux_rate + 2 * hubble * flux - wave * pressure
    speed, weight, monopole, dipole, quadrupole = sy.symbols("u W f0 f1 f2", nonzero=True, real=True)
    monopole_rate = -wave * (sy.Rational(4, 3) * metric_z + speed * dipole)
    dipole_rate = wave * speed * (monopole - 2 * quadrupole) / 3
    nu_density, nu_flux, nu_pressure, nu_shear = weight * monopole / speed, weight * dipole, weight * speed * monopole / 3, weight * speed * quadrupole
    nu_density_rate = weight / speed * (monopole_rate - hubble * (1 + speed ** 2) * monopole)
    nu_flux_rate = weight * (dipole_rate - 2 * hubble * dipole)
    expressions = {
        "canonical_pressure_is_kinetic_minus_potential": pressure - (density - 2 * mass_a ** 2 * field * delta),
        "scalar_continuity_defect": continuity - defect_velocity * delta_rate - mass_a ** 2 * defect_field * delta,
        "scalar_momentum_defect": momentum - wave * defect_velocity * delta,
        "on_shell_scalar_continuity": continuity.subs({field_rate: velocity, velocity_rate: -2 * hubble * velocity - mass_a ** 2 * field}),
        "on_shell_scalar_momentum": momentum.subs(velocity_rate, -2 * hubble * velocity - mass_a ** 2 * field),
        "massive_node_continuity": nu_density_rate + hubble * (nu_density + 3 * nu_pressure) + wave * nu_flux + wave * metric_z * sy.Rational(4, 3) * weight / speed,
        "massive_node_momentum": nu_flux_rate + 2 * hubble * nu_flux - wave * nu_pressure + sy.Rational(2, 3) * wave * nu_shear,
    }
    result = {name: str(sy.simplify(value)) for name, value in expressions.items()}
    require(all(value == "0" for value in result.values()), "symbolic parent identities")
    return result


def analyze(packet):
    terms, meta, times = packet["terms"], packet["metadata"], packet["times"]
    density, flux, pressure, density_rate, flux_rate, enthalpy, shear = [terms[:, :, index] for index in range(7)]
    hubble, metric_z = meta[:, 1, None], meta[:, 2, None]
    continuity_terms = np.array([density_rate, hubble * (density + 3 * pressure), WAVE * flux, WAVE * metric_z * enthalpy])
    momentum_terms = np.array([flux_rate, 2 * hubble * flux, -WAVE * pressure, 2 * WAVE / 3 * shear])
    continuity, momentum = continuity_terms.sum(axis=0), momentum_terms.sum(axis=0)
    predicted_c, predicted_e = np.zeros_like(continuity), np.zeros_like(momentum)
    predicted_c[:, 1] = 3 * hubble[:, 0] * pressure[:, 1]
    predicted_c[:, 4] = WAVE * metric_z[:, 0] * (enthalpy[:, 4] - meta[:, 3])
    field_defects = []
    for species, offset in ((5, 4), (6, 14)):
        field, velocity, field_rate, velocity_rate, mass, delta, delta_rate = [meta[:, offset + index] for index in range(7)]
        defect_field = field_rate - velocity
        defect_velocity = velocity_rate + 2 * hubble[:, 0] * velocity + (meta[:, 0] * mass) ** 2 * field
        predicted_c[:, species] = defect_velocity * delta_rate + (meta[:, 0] * mass) ** 2 * defect_field * delta
        predicted_e[:, species] = WAVE * defect_velocity * delta
        field_defects.append(dict(species=packet["species"][species].item(), field_rate_relative=norm(defect_field) / scale(velocity), acceleration_relative=norm(defect_velocity) / max(norm(velocity_rate), norm(2 * hubble[:, 0] * velocity), norm((meta[:, 0] * mass) ** 2 * field), 1e-80)))
    total_c, total_e = continuity.sum(axis=1), momentum.sum(axis=1)
    predicted_total_c, predicted_total_e = predicted_c.sum(axis=1), predicted_e.sum(axis=1)
    scale_c, scale_e = scale(continuity_terms.sum(axis=2)), scale(momentum_terms.sum(axis=2))
    algebra_c = norm(total_c - predicted_total_c) / scale_c
    algebra_e = norm(total_e - predicted_total_e) / scale_e
    c_species = {str(packet["species"][index]): norm(continuity[:, index] - predicted_c[:, index]) / scale(continuity_terms[:, :, index]) for index in range(7)}
    e_groups = {}
    for label, selected in (("cdm", [0]), ("photon_baryon", [1, 2]), ("massless", [3]), ("massive_neutrino", [4]), ("slow_scalar", [5]), ("heavy_scalar", [6])):
        e_groups[label] = norm((momentum - predicted_e)[:, selected].sum(axis=1)) / scale(momentum_terms[:, :, selected].sum(axis=2))
    base = packet["observer"]
    old_errors = dict(D=norm(density.sum(axis=1) - base[:, 2]) / scale(base[:, 2]),
                      Q=norm(flux.sum(axis=1) - base[:, 3]) / scale(base[:, 3]),
                      Pi=norm(shear.sum(axis=1) - base[:, 4]) / scale(base[:, 4]),
                      enthalpy=norm(enthalpy.sum(axis=1) - base[:, 0] - base[:, 1]) / scale(base[:, 0] + base[:, 1]),
                      massive_pressure=norm(pressure[:, 4] - meta[:, 24]) / scale(pressure[:, 4]))
    for species, offset in ((5, 4), (6, 14)):
        for index, label in ((0, "D"), (2, "P"), (1, "Q")):
            diagnostic_index = offset + {"D": 7, "P": 8, "Q": 9}[label]
            old_errors[str(packet["species"][species]) + label] = norm(terms[:, species, index] - meta[:, diagnostic_index]) / scale(terms[:, species, index])
    indices = packet["derivative_indices"]
    direct = terms[indices][:, :, [3, 4]].sum(axis=1)
    finite = packet["directional"].sum(axis=2)
    total_rates = terms[:, :, [3, 4]].sum(axis=1)
    rate_scale = np.maximum(np.max(abs(total_rates), axis=0), 1e-80)
    differences = np.max(abs(finite - direct[:, None, :]), axis=0) / rate_scale
    richardson = (4 * finite[:, 1:, :] - finite[:, :-1, :]) / 3
    richardson_errors = np.max(abs(richardson - direct[:, None, :]), axis=0) / rate_scale
    richardson_change = np.max(abs(richardson[:, -1] - richardson[:, -2]), axis=0) / rate_scale
    physical_scale_rate = meta[indices, 0] * meta[indices, 1]
    scale_errors = np.max(abs(packet["scale_rates"] - physical_scale_rate[:, None]), axis=0) / scale(physical_scale_rate)
    states = np.column_stack([density.sum(axis=1), flux.sum(axis=1)])
    rhs = np.column_stack([-continuity_terms[1:].sum(axis=(0, 2)), -momentum_terms[1:].sum(axis=(0, 2))])
    defects = np.column_stack([predicted_total_c, predicted_total_e])
    state_scale = np.maximum(np.max(abs(states), axis=0), 1e-80)
    integral_reports, integral_packets = [], []
    for stride in (1, 2, 4):
        keep = np.unique(np.r_[np.arange(0, len(times), stride), len(times) - 1])
        raw_integral = CubicSpline(times[keep], rhs[keep]).antiderivative()
        accounted_integral = CubicSpline(times[keep], (rhs + defects)[keep]).antiderivative()
        raw = states[0] + raw_integral(times) - raw_integral(times[0])
        accounted = states[0] + accounted_integral(times) - accounted_integral(times[0])
        integral_reports.append(dict(stride=stride, raw_error=(np.max(abs(raw - states), axis=0) / state_scale).tolist(), defect_accounted_error=(np.max(abs(accounted - states), axis=0) / state_scale).tolist()))
        integral_packets.append(accounted)
    integral_refinement = np.max(abs(integral_packets[-1] - integral_packets[0]), axis=0) / state_scale
    contributions = {str(packet["species"][index]): dict(continuity=norm(predicted_c[:, index]) / scale_c, momentum=norm(predicted_e[:, index]) / scale_e) for index in range(7)}
    numerical = max(algebra_c, algebra_e, *old_errors.values(), *c_species.values(), *e_groups.values()) < ALGEBRA and max(*richardson_errors[-1], *richardson_change, scale_errors[-1], *integral_reports[0]["defect_accounted_error"], *integral_refinement) < GATE
    report = dict(numerical_passed=bool(numerical), raw_continuity=float(norm(total_c) / scale_c), raw_momentum=float(norm(total_e) / scale_e),
                  raw_balance_within_gate=bool(max(norm(total_c) / scale_c, norm(total_e) / scale_e) < GATE),
                  decomposition_continuity=algebra_c, decomposition_momentum=algebra_e, species_continuity=c_species, grouped_momentum=e_groups,
                  original_source_errors=old_errors, independent_rate_difference=differences.tolist(), richardson_errors=richardson_errors.tolist(), richardson_change=richardson_change.tolist(),
                  thermal_scale_derivative_errors=scale_errors.tolist(), integrals=integral_reports, integral_refinement=integral_refinement.tolist(), field_defects=field_defects, predicted_defect_contributions=contributions,
                  maximum_neutrino_enthalpy_mismatch=norm(enthalpy[:, 4] - meta[:, 3]) / scale(enthalpy[:, 4]),
                  pressure_peak=norm(pressure.sum(axis=1)), continuity_scale=scale_c, momentum_scale=scale_e)
    arrays = dict(times=times, density=states[:, 0], momentum=states[:, 1], pressure=pressure.sum(axis=1), continuity_residual=total_c, momentum_residual=total_e,
                  predicted_continuity=predicted_total_c, predicted_momentum=predicted_total_e, source_rhs=rhs, defect_contributions_c=predicted_c, defect_contributions_e=predicted_e,
                  integrated_with_defects=integral_packets[0])
    return report, arrays


def main():
    modest()
    check_prior()
    output = ROOT / "balance-corrected"
    output.mkdir(exist_ok=False)
    identities = symbolic()
    owner = read(ROOT / "readout-result.json")
    require(owner["state"] == "complete", "completed readout required")
    reports, rows = [], []
    for model_owner in owner["reports"]:
        model, records, packets = model_owner["model"], [], {}
        for case in model_owner["cases"]:
            guard()
            source = ROOT / "runs" / model / case["file"]
            require(digest(source) == case["sha256"], "readout ownership")
            packet = load(source)
            packets[case["tag"]] = packet
            report, arrays = analyze(packet)
            path = output / (model + "-" + case["tag"] + ".npz")
            np.savez_compressed(path, **arrays)
            report.update(tag=case["tag"], file=path.name, sha256=digest(path), input_sha256=digest(source))
            records.append(report)
            rows.append(dict(model=model, tag=case["tag"], numerical_passed=report["numerical_passed"], raw_continuity=report["raw_continuity"], raw_momentum=report["raw_momentum"], raw_balance_within_gate=report["raw_balance_within_gate"], decomposition_continuity=report["decomposition_continuity"], decomposition_momentum=report["decomposition_momentum"], fine_integral_D=report["integrals"][0]["defect_accounted_error"][0], fine_integral_Q=report["integrals"][0]["defect_accounted_error"][1]))
            print(model, case["tag"], report["numerical_passed"], "raw", report["raw_continuity"], report["raw_momentum"], "decomposition", report["decomposition_continuity"], report["decomposition_momentum"], flush=True)
        columns = [0, 1, 2, 3, 4, 6]
        zero = bool(np.count_nonzero(packets["L64-zero"]["terms"][:, :, columns]) == 0)
        negative = float(np.max(abs(packets["L64-base"]["terms"][:, :, columns] + packets["L64-negative"]["terms"][:, :, columns])) / scale(packets["L64-base"]["terms"][:, :, columns]))
        reports.append(dict(model=model, cases=records, zero=zero, sign_error=negative, numerical_passed=bool(zero and negative < ALGEBRA and all(row["numerical_passed"] for row in records))))
    csv_path = output / "pressure-balance.csv"
    with csv_path.open("x", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    result = dict(numerical_passed=all(report["numerical_passed"] for report in reports), symbolic=identities, reports=reports, source_sha256=digest(__file__), readout_sha256=digest(ROOT / "readout-result.json"), csv_sha256=digest(csv_path), numerical_gate=GATE, algebra_gate=ALGEBRA, original_trajectories_unchanged=True, physical_residuals_reported_without_redefining_tolerance=True)
    write(output / "balance-result.json", result)
    print(dict(numerical_passed=result["numerical_passed"], symbolic_identities=len(identities), cases=len(rows)), flush=True)


if __name__ == "__main__":
    main()
