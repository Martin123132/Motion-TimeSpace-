import csv
from common import ROOT, CLOSURE, WAVE, GATE, ALGEBRA, modest, guard, require, check_prior, native_background, other_density, dense_values, read, write, digest, load
import numpy as np
from scipy.interpolate import CubicSpline


def peak(values):
    return float(np.max(abs(values)))


def relative(left, right):
    return peak(left - right) / max(peak(right), 1e-80)


def coordinates(packet, native, efold):
    values, derivatives = dense_values(packet, efold)
    physical = values * packet["units"]
    rates = derivatives * packet["units"]
    fields = packet["initial_fields"] + physical[:, [0, 2]]
    velocities = physical[:, [1, 3]]
    scale = np.exp(efold)
    density = (velocities ** 2 + (scale[:, None] * packet["masses"] * fields) ** 2) / 2
    hubble = np.sqrt((other_density(native, scale) + density.sum(axis=1)) / 3)
    return fields, velocities, rates, hubble


def checks_for(packet, reference, original_pressure, old_diagnostic, native):
    scale, hubble, masses = packet["a"], packet["H"], packet["masses"]
    fields, velocities = packet["fields"], packet["velocities"]
    field_prime = hubble[:, None] * packet["field_efold_derivative"]
    velocity_prime = hubble[:, None] * packet["velocity_efold_derivative"]
    omega2 = (scale[:, None] * masses) ** 2
    defect_phi = field_prime - velocities
    defect_v = velocity_prime + 2 * hubble[:, None] * velocities + omega2 * fields
    field_errors = []
    for index, label in enumerate(("slow", "heavy")):
        field_errors.append(dict(field=label, kinematics=peak(defect_phi[:, index]) / max(peak(velocities[:, index]), 1e-80),
                                 dynamics=peak(defect_v[:, index]) / max(peak(velocity_prime[:, index]), peak(2 * hubble * velocities[:, index]), peak(omega2[:, index] * fields[:, index]), 1e-80)))
    rho_n = velocities * packet["velocity_efold_derivative"] + omega2 * fields ** 2 + omega2 * fields * packet["field_efold_derivative"]
    background_c = rho_n + packet["scalar_density"] + 3 * packet["scalar_pressure"]
    background_scale = max(peak(rho_n.sum(axis=1)), peak((packet["scalar_density"] + 3 * packet["scalar_pressure"]).sum(axis=1)), 1e-80)
    background_error = peak(background_c.sum(axis=1)) / background_scale
    clock_error = relative(packet["clock_efold_derivative"], 1 / hubble)
    probe_c = (defect_v * reference["old_delta_rate"] + omega2 * defect_phi * reference["old_delta"]).sum(axis=1)
    probe_e = (WAVE * defect_v * reference["old_delta"]).sum(axis=1)
    bridge_c = peak(probe_c) / old_diagnostic["continuity_scale"]
    bridge_e = peak(probe_e) / old_diagnostic["momentum_scale"]
    indices = np.unique(np.linspace(1, len(scale) - 2, 11, dtype=int))
    efold = packet["efold"]
    maximum_step = float(np.min(packet["segment_end"] - packet["segment_start"])) / 16
    maximum_step = min(maximum_step, float(efold[indices[0]] - efold[0]) / 3, float(efold[-1] - efold[indices[-1]]) / 3)
    require(maximum_step > 1e-13, "independent derivative step underflow")
    steps = maximum_step / np.array([1., 2., 4., 8.])
    derived_hubble, derived_other = [], []
    for step in steps:
        plus = efold[indices] + step
        minus = efold[indices] - step
        _, _, _, plus_hubble = coordinates(packet, native, plus)
        _, _, _, minus_hubble = coordinates(packet, native, minus)
        derived_hubble.append((plus_hubble - minus_hubble) / (2 * step))
        derived_other.append((other_density(native, np.exp(plus)) - other_density(native, np.exp(minus))) / (2 * step))
    derived_hubble, derived_other = np.array(derived_hubble), np.array(derived_other)
    rich_hubble = (4 * derived_hubble[1:] - derived_hubble[:-1]) / 3
    rich_other = (4 * derived_other[1:] - derived_other[:-1]) / 3
    other_pressure = original_pressure - ((reference["velocities"] ** 2 - (scale[:, None] * masses * reference["fields"]) ** 2) / 2).sum(axis=1)
    total_pressure = other_pressure + packet["scalar_pressure"].sum(axis=1)
    expected_hubble_n = -(3 * hubble ** 2 + 3 * total_pressure) / (6 * hubble)
    expected_other_n = -packet["other_density"] - 3 * other_pressure
    hubble_errors = [relative(value, expected_hubble_n[indices]) for value in rich_hubble]
    other_errors = [relative(value, expected_other_n[indices]) for value in rich_other]
    hubble_refinement = relative(rich_hubble[-1], rich_hubble[-2])
    phase_integral = CubicSpline(efold, scale * masses[1] / hubble).antiderivative()
    old_phase = CubicSpline(efold, scale * masses[1] / reference["hubble"]).antiderivative()
    phase_change = (phase_integral(efold) - phase_integral(efold[0])) - (old_phase(efold) - old_phase(efold[0]))
    changes = dict(H=relative(hubble, reference["hubble"]), scalar_density=relative(packet["scalar_density"].sum(axis=1), ((reference["velocities"] ** 2 + (scale[:, None] * masses * reference["fields"]) ** 2) / 2).sum(axis=1)),
                   clock_increment=relative(packet["clock_increment"], reference["times"] - reference["times"][0]), maximum_clock_shift_mpc=peak(packet["times"] - reference["times"]),
                   final_clock_shift_mpc=float(packet["times"][-1] - reference["times"][-1]), maximum_phase_shift_radians=peak(phase_change), final_phase_shift_radians=float(phase_change[-1]),
                   heavy_field=relative(fields[:, 1], reference["fields"][:, 1]), heavy_velocity=relative(velocities[:, 1], reference["velocities"][:, 1]), slow_velocity=relative(velocities[:, 0], reference["velocities"][:, 0]))
    numerical = max(background_error, clock_error, bridge_c, bridge_e, *[value for row in field_errors for key, value in row.items() if key != "field"], hubble_errors[-1], other_errors[-1], hubble_refinement) < GATE
    report = dict(passed=bool(numerical), field_defects=field_errors, canonical_background_continuity=background_error, clock_consistency=clock_error,
                  probe_continuity_defect_on_old_amplitudes=bridge_c, probe_momentum_defect_on_old_amplitudes=bridge_e, independent_steps=steps.tolist(),
                  raychaudhuri_errors=hubble_errors, other_background_continuity_errors=other_errors, raychaudhuri_refinement=hubble_refinement, changes_from_old=changes,
                  positive_H=bool(np.min(hubble) > 0), monotone_clock=bool(np.all(np.diff(packet["times"]) > 0)), perturbation_recomputed=False)
    arrays = dict(efold=efold, defect_phi=defect_phi, defect_v=defect_v, scalar_background_continuity=background_c,
                  operator_probe_continuity=probe_c, operator_probe_momentum=probe_e, phase_change=phase_change, other_pressure=other_pressure,
                  probe_indices=indices, finite_hubble_derivatives=derived_hubble, finite_other_derivatives=derived_other,
                  expected_hubble_derivative=expected_hubble_n[indices], expected_other_derivative=expected_other_n[indices])
    return report, arrays


def main():
    modest()
    check_prior()
    frozen, owner = read(ROOT / "input-result.json"), read(ROOT / "run-result.json")
    require(owner["state"] == "complete", "completed background solves required")
    output = ROOT / "comparison"
    output.mkdir(exist_ok=False)
    previous = read(CLOSURE / "balance-corrected/balance-result.json")
    reports, csv_rows = [], []
    for model_owner in owner["reports"]:
        guard()
        model = model_owner["model"]
        input_owner = next(row for row in frozen["reports"] if row["model"] == model)
        reference_path = ROOT / "inputs" / input_owner["reference"]
        require(digest(reference_path) == input_owner["reference_sha256"], "held-back scalar reference owner")
        reference = load(reference_path)
        require(digest(input_owner["source"]) == input_owner["source_sha256"], "pressure owner unchanged")
        original_pressure = load(input_owner["source"])["observer"][:, 1]
        old_case = next(row for row in next(row for row in previous["reports"] if row["model"] == model)["cases"] if row["tag"] == "G192-fine")
        native = native_background(model)
        packets, cases = {}, []
        for case_owner in model_owner["cases"]:
            tag = case_owner["tag"]
            source = ROOT / "runs" / model / case_owner["file"]
            require(digest(source) == case_owner["sha256"], "background output ownership")
            packet = load(source)
            packets[tag] = packet
            report, arrays = checks_for(packet, reference, original_pressure, old_case, native)
            path = output / (model + "-" + tag + "-checks.npz")
            np.savez_compressed(path, **arrays)
            report.update(tag=tag, source_sha256=digest(source), file=path.name, sha256=digest(path))
            cases.append(report)
            csv_rows.append(dict(model=model, tag=tag, passed=report["passed"], background_continuity=report["canonical_background_continuity"], clock=report["clock_consistency"],
                                 operator_continuity=report["probe_continuity_defect_on_old_amplitudes"], operator_momentum=report["probe_momentum_defect_on_old_amplitudes"],
                                 raychaudhuri=report["raychaudhuri_errors"][-1], H_change=report["changes_from_old"]["H"], clock_shift_mpc=report["changes_from_old"]["maximum_clock_shift_mpc"]))
            print(model, tag, report["passed"], "background", report["canonical_background_continuity"], "source probe", report["probe_continuity_defect_on_old_amplitudes"], "clock", report["clock_consistency"], "Raychaudhuri", report["raychaudhuri_errors"][-1], flush=True)
        comparisons = []
        for left, right in (("dop-base", "dop-fine"), ("dop-fine", "dop-half-cap"), ("rk-independent", "dop-half-cap")):
            values = {name: relative(packets[left][name], packets[right][name]) for name in ("normalized", "fields", "velocities", "scalar_density", "scalar_pressure", "H", "clock_increment")}
            for name in ("normalized", "fields", "velocities", "scalar_density", "scalar_pressure"):
                for index in range(packets[right][name].shape[1]):
                    values[name + "_" + str(index)] = relative(packets[left][name][:, index], packets[right][name][:, index])
            comparisons.append(dict(left=left, right=right, errors=values, passed=max(values.values()) < GATE))
        report = dict(model=model, cases=cases, comparisons=comparisons, passed=bool(all(row["passed"] for row in cases + comparisons)), original_initial_fields_preserved=True, no_fitted_correction=True)
        reports.append(report)
        print(model, "comparisons", comparisons, flush=True)
        del native
    csv_path = ROOT / "background-comparison.csv"
    with csv_path.open("x", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(csv_rows[0]))
        writer.writeheader()
        writer.writerows(csv_rows)
    result = dict(passed=all(row["passed"] for row in reports), reports=reports, source_sha256=digest(__file__), run_result_sha256=digest(ROOT / "run-result.json"), input_result_sha256=digest(ROOT / "input-result.json"),
                  csv_sha256=digest(csv_path), numerical_gate=GATE, algebra_gate=ALGEBRA, no_perturbation_rerun=True, source_probe_scope="operator defect evaluated on held-fixed old amplitudes, not a new perturbation trajectory")
    write(ROOT / "comparison-result.json", result)
    print(dict(passed=result["passed"], cases=len(csv_rows)), flush=True)


if __name__ == "__main__":
    main()
