from common import *
from compact_adjoint import CompactAdjoint
from adjoint_operator import open_owned, relative, sup
from physical_energy_map import PhysicalEnergyMap
from primitive_math import MetricPrimitive
from metric_channels import derive, symbolic
import numpy as np
import time


def coefficients(model):
    report = read(LATEST / LABEL / (model + "-central-packing.json")) if LABEL == "balanced" else read(ADJOINT / (model + "-build.json"))
    require(digest(report["packet"]) == report["sha256"], "saved coefficient packet")
    return load(report["packet"]), dict(path=report["packet"], sha256=report["sha256"])


def main():
    modest()
    check_parent()
    (ROOT / "contexts").mkdir(exist_ok=False)
    write(ROOT / "inputs.json", dict(sources=frozen_sources(), parent_seal=PARENT_SEAL,
                                    gates=dict(numerical=GATE, algebra=ALGEBRA),
                                    physical_ode_solves=0, prediction_frozen_before_run=True))
    write(ROOT / "symbolic.json", symbolic())
    reports = []
    for model in ("heavy", "cold"):
        started = time.monotonic()
        packet, provenance = coefficients(model)
        operator = CompactAdjoint(packet)
        system = open_owned(model, "contexts")
        energy = PhysicalEnergyMap(system)
        reference = load(POISSON / "evolution" / (model + "-gr.npz"))
        primitive = MetricPrimitive(system, reference)
        errors, algebra, rows = {}, {}, []
        def record(name, value, exact=False):
            target = algebra if exact else errors
            target[name] = max(target.get(name, 0.), float(value))
        for count, index in enumerate(np.unique(np.linspace(2, len(packet["efold"]) - 4, 97, dtype=int))):
            guard()
            grid = packet["efold"]
            efold = float(grid[index] + .43 * (grid[index + 1] - grid[index]))
            derived = derive(system, energy, efold)
            core, _, _, _, injection, _ = operator.blocks(efold, 0)
            transform, inverse = derived["transform"], derived["inverse"]
            matrix = transform @ core @ inverse + derived["derivative"]
            density, free_density = derived["density"], derived["free_density"]
            drive_psi, drive_phi = derived["psi_injection"], derived["phi_injection"]
            metric = np.outer(drive_psi, derived["psi"]) + np.outer(drive_phi, derived["phi_rate"])
            free = matrix - metric
            actual_density = operator.splines["rows"](efold)[0] @ inverse
            record("density_dictionary", relative(density - actual_density, actual_density))
            actual_rate = derived["density_rate"] + density @ matrix
            predicted_rate = free_density + 3 * derived["defect"] * derived["psi"] + 3 * derived["quadrature"] * derived["phi_rate"]
            record("density_evolution", relative(actual_rate - predicted_rate, predicted_rate))
            for label, drive, expected in (("psi", drive_psi, 3 * derived["defect"]), ("phi", drive_phi, 3 * derived["quadrature"])):
                scale = max(np.linalg.norm(density) * np.linalg.norm(drive), 1e-80)
                record("density_injection_" + label, abs(density @ drive - expected) / scale, True)
            record("free_density_reconstruction", relative(derived["density_rate"] + density @ free - free_density, free_density))
            direction, _, denominator = primitive.vector(efold, 1.)
            record("primitive_dictionary", relative(transform @ direction + drive_phi / denominator, drive_phi / denominator))
            record("denominator", abs(denominator - derived["denominator"] / (2 * system.wave**2)) / denominator)
            hubble = derived["hubble"]
            enthalpy = system.context["observe"](system.context["point"](efold)[11], system.zero_native)[:2].sum()
            mixing = -3 * (hubble + 3 * hubble * enthalpy / (2 * system.wave**2)) / (system.wave * denominator)
            actual_gravity = transform @ (injection[:, 0] + mixing * injection[:, 1])
            expected_gravity = drive_psi - 3 * derived["defect"] / derived["denominator"] * drive_phi
            record("physical_gravity_drive", relative(actual_gravity - expected_gravity, expected_gravity))
            for seed in range(3):
                vector = np.sin(np.arange(energy.size) * (seed + 1) + count + .2)
                state = np.zeros(len(system.units))
                state[:energy.size] = inverse @ vector
                _, values, rates, info, _, _ = system.evaluate(efold, state * system.units, "poisson-spatial")
                for label, key in (("density", "D"), ("current", "Q"), ("shear", "Pi"), ("psi", "Psi")):
                    expected = derived[label] @ vector
                    scale = max(np.linalg.norm(derived[label]) * np.linalg.norm(vector), abs(values[key]), 1e-80)
                    record("native_" + label, abs(expected - values[key]) / scale)
                expected = derived["phi_rate"] @ vector
                scale = max(np.linalg.norm(derived["phi_rate"]) * np.linalg.norm(vector), abs(rates["Phi"] / hubble), 1e-80)
                record("native_phi_rate", abs(expected - rates["Phi"] / hubble) / scale)
                record("quadrature_dictionary", abs(derived["quadrature"] - info["quadrature_enthalpy"]) / max(abs(info["quadrature_enthalpy"]), 1e-80))
            for scalar in derived["scalars"]:
                selected = scalar["slots"]
                rest = np.array([slot for slot in range(energy.size) if slot not in selected])
                actual_self = matrix[np.ix_(selected, selected)]
                expected_self = scalar["internal"] + metric[np.ix_(selected, selected)]
                record("scalar_" + str(scalar["species"]) + "_self", relative(actual_self - expected_self, expected_self))
                coupling_values = []
                for label, destination, origin in (("to_scalar", selected, rest), ("from_scalar", rest, selected)):
                    actual = matrix[np.ix_(destination, origin)]
                    expected = metric[np.ix_(destination, origin)]
                    scale = max(np.linalg.norm(expected, ord=2), np.linalg.norm(actual, ord=2), 1e-80)
                    record("scalar_" + str(scalar["species"]) + "_" + label, np.linalg.norm(actual - expected, ord=2) / scale)
                    density_norm = np.linalg.norm(density[origin])
                    free_norm = np.linalg.norm(free_density[origin])
                    phi_bound = (free_norm + 3 * abs(derived["defect"]) * density_norm / (2 * system.wave**2)) / derived["denominator"]
                    psi_term = np.linalg.norm(drive_psi[destination]) * density_norm / (2 * system.wave**2)
                    phi_term = np.linalg.norm(drive_phi[destination]) * phi_bound
                    upper = psi_term + phi_term
                    exact_norm = np.linalg.norm(expected, ord=2)
                    record("triangle_inequality", max(0., exact_norm - upper) / max(upper, 1e-80), True)
                    coupling_values.append(dict(direction=label, exact=exact_norm, upper=upper, psi_term=psi_term, phi_term=phi_term))
                scalar_density_norm = np.linalg.norm(density[selected])
                scalar_free_norm = np.linalg.norm(free_density[selected])
                amplitude = scalar["stress_amplitude"]
                density_upper = amplitude
                free_upper = 4 * amplitude + system.wave**2 * abs(scalar["velocity"]) / (hubble * scalar["full_frequency"])
                record("scalar_density_upper", max(0., scalar_density_norm - density_upper) / max(density_upper, 1e-80), True)
                record("scalar_free_upper", max(0., scalar_free_norm - free_upper) / max(free_upper, 1e-80), True)
                if scalar["species"] == (1 if model == "heavy" else 0):
                    rows.append(dict(efold=efold, scalar_species=scalar["species"], wave=system.wave,
                                     hubble=hubble, omega=scalar["omega"],
                                     epsilon_H_over_k=hubble / system.wave, delta_k_over_am=system.wave / scalar["omega"],
                                     kappa_amH_over_k2=scalar["omega"] * hubble / system.wave**2,
                                     relative_quadrature_defect=derived["defect"] / derived["quadrature"],
                                     coupling=coupling_values,
                                     triangle_feedback_product=coupling_values[0]["upper"] * coupling_values[1]["upper"],
                                     exact_feedback_product=coupling_values[0]["exact"] * coupling_values[1]["exact"],
                                     scalar_density_norm=scalar_density_norm, scalar_density_upper=density_upper,
                                     scalar_free_norm=scalar_free_norm, scalar_free_upper=free_upper))
            if count % 32 == 0:
                print(LABEL, model, "channel samples", count + 1, "seconds", round(time.monotonic() - started, 1), flush=True)
        passed = max(errors.values()) < GATE and max(algebra.values()) < ALGEBRA
        report = dict(model=model, passed=passed, errors=errors, algebra=algebra, rows=rows,
                      coefficient_input=provenance, seconds=time.monotonic() - started,
                      new_physical_ode_solves=0, fixed_original_data=True)
        write(ROOT / (model + "-channels.json"), report)
        print(LABEL, model, "passed", passed, "errors", errors, "algebra", algebra, flush=True)
        require(passed, "preserve channel discrepancy before changing anything")
        reports.append(report)
        del system, energy, operator, reference, packet
    for path, expected in read(ROOT / "inputs.json")["sources"].items():
        require(digest(path) == expected, "frozen source")
    check_parent()
    write(ROOT / "result.json", dict(passed=True, reports=reports, new_physical_ode_solves=0))


if __name__ == "__main__":
    main()
