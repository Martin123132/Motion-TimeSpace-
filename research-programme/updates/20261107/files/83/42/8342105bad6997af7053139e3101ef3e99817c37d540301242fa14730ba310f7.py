from common import *
from poisson_driver import *
RUN = ROOT / "preflight-v2"

from scipy.interpolate import make_interp_spline
import sympy as sp
import numpy as np


def symbolic():
    wave, scale_value, potential, density = sp.symbols("wave scale potential density", nonzero=True)
    hubble, hubble_rate, alpha, phi_rate = sp.symbols("hubble hubble_rate alpha phi_rate")
    lapse_rate = potential - hubble * alpha
    eta_rate = phi_rate + hubble_rate * alpha + hubble * lapse_rate
    expansion = wave * alpha - 3 * eta_rate / wave
    density_rate = -wave * expansion - 3 * hubble_rate * alpha - 3 * hubble * lapse_rate
    action = -scale_value**2 * (wave**2 * potential**2 + density * potential)
    identities = {
        "poisson_action": sp.diff(action, potential) + scale_value**2 * (2 * wave**2 * potential + density),
        "dust_continuity": density_rate + wave**2 * alpha - 3 * phi_rate,
        "dust_euler": wave**2 * lapse_rate + hubble * wave**2 * alpha - wave**2 * potential}
    result = {name: str(sp.simplify(value)) for name, value in identities.items()}
    require(all(value == "0" for value in result.values()), "symbolic reduction")
    return result


def main():
    modest()
    check_parent()
    RUN.mkdir(exist_ok=False)
    write(RUN / "frozen-inputs.json", dict(sources={str(path): digest(path) for path in STAGE.iterdir()
                                                if path.suffix in (".py", ".md", ".ps1")}, algebra=ALGEBRA, numerical=GATE,
          branches=["gr", "poisson-spatial", "newton-dust-force"], no_future_perturbation_sources=True))
    write(RUN / "symbolic-identities.json", symbolic())
    (RUN / "contexts").mkdir(exist_ok=False)
    (RUN / "backgrounds").mkdir(exist_ok=False)
    reports = []
    for model in ("heavy", "cold"):
        guard()
        system = open_system(model, "preflight-v2/contexts")
        grid = system.background["efold"]
        values = np.array([system.background_values(float(efold)) for efold in grid])
        packet = dict(efold=grid, values=values)
        system.install_background(packet)
        path = RUN / "backgrounds" / (model + ".npz")
        np.savez_compressed(path, **packet)
        indices = np.unique(np.linspace(2, len(grid) - 4, 97, dtype=int))
        points = grid[indices] + .43 * (grid[indices + 1] - grid[indices])
        direct = np.array([system.background_values(float(efold)) for efold in points])
        fine = system.background_spline(points)
        keep = np.unique(np.r_[np.arange(0, len(grid), 2), len(grid) - 1])
        coarse = make_interp_spline(grid[keep], values[keep], k=5, axis=0)
        difference = {}
        for step in (1e-6, 5e-7):
            samples = {offset: np.array([system.background_values(float(efold + offset * step)) for efold in points])
                       for offset in (-2, -1, 1, 2)}
            difference[step] = (samples[-2] - 8 * samples[-1] + 8 * samples[1] - samples[2]) / (12 * step)
        numerical = {}
        for column, name in enumerate(("H", "g")):
            denominator = max(float(np.max(abs(difference[5e-7][:, column]))), 1e-80)
            numerical["background_value_" + name] = float(np.max(abs(fine[:, column] - direct[:, column])) / max(np.max(abs(direct[:, column])), 1e-80))
            numerical["background_derivative_" + name] = float(np.max(abs(system.background_spline(points, 1)[:, column] - difference[5e-7][:, column])) / denominator)
            numerical["background_fd_refinement_" + name] = float(np.max(abs(difference[1e-6][:, column] - difference[5e-7][:, column])) / denominator)
            numerical["background_grid_derivative_" + name] = float(np.max(abs(system.background_spline(points, 1)[:, column] - coarse(points, 1)[:, column])) / denominator)
        algebra = {}
        rates_expected, rates_actual = [], []
        density_expected, density_actual = [], []
        eta_expected, eta_actual = [], []
        source_mismatch = []
        random = np.random.default_rng(20261107)
        for probe_index, efold in enumerate(points):
            guard()
            efold = float(efold)
            raw = np.sin(np.arange(len(system.raw_units)) + 1 + probe_index) * system.raw_units
            state = system.encode(efold, raw)
            physical = system.project(raw)
            old_rate, point = system.native_extended_rhs(efold, raw)
            observed = system.context["observe"](point[11], physical)
            expected = old_rate / point[12]
            expected[system.alpha_slot] = observed[6] / (system.wave * point[12])
            if model == "heavy":
                phase, mu = system.owner.phase(efold)
                omega = point[10] * system.background["masses"][1]
                amplitude = complex(*state[system.slots])
                direct_rate = point[10] * np.exp(1j * phase) * (
                    np.sqrt(omega) * (1.5 * raw[system.slots[0]] + old_rate[system.slots[0]] / point[12])
                    + 1j / np.sqrt(omega) * (.5 * raw[system.slots[1]] + old_rate[system.slots[1]] / point[12])) + 1j * mu * amplitude
                expected[system.slots] = [direct_rate.real, direct_rate.imag]
            actual = system.evaluate(efold, state, "gr")[0]
            rates_expected.append(expected / system.units)
            rates_actual.append(actual / system.units)
            eta_basis = np.zeros(system.context["dimension"])
            eta_basis[system.context["position"](1)] = 1.
            zero = np.zeros_like(eta_basis)
            original = system.context["original_rhs"](point[11], eta_basis)
            source_observer = system.context["observe"](point[11], eta_basis)
            source_terms, source_meta = system.context["stress"](point[11], eta_basis)
            expansion, shear = system.metric_kernels(efold)
            metric_z = source_observer[5] - 1.5 * source_observer[3] / system.wave**2
            predicted = expansion * metric_z + shear * source_observer[5]
            core_positions = np.array([index for index in range(len(zero)) if index != system.context["position"](1)])
            source_mismatch.append(float(np.max(abs(original[core_positions] - predicted[core_positions])) / max(np.max(abs(original[core_positions])), 1e-80)))
            effective_enthalpy = source_terms[:, 5].sum() - source_terms[4, 5] + source_meta[3]
            algebra["density_metric_kernel"] = max(algebra.get("density_metric_kernel", 0.),
                float(abs(source_terms[:, 3].sum() + system.wave * effective_enthalpy * metric_z) /
                      max(abs(system.wave * effective_enthalpy * metric_z), 1e-80)))
            algebra["current_metric_silence"] = max(algebra.get("current_metric_silence", 0.), float(np.max(abs(source_terms[:, 4]))))
            if probe_index % 3:
                continue
            for branch in ("gr", "poisson-spatial", "newton-dust-force"):
                derivative, observables, rates, diagnostics, projected, terms = system.evaluate(efold, state, branch)
                theta = observables["theta_c"]
                scale_value = max(abs(theta), abs(rates["delta_c"]), abs(3 * rates["Phi"]), 1e-80)
                algebra[branch + "_continuity"] = max(algebra.get(branch + "_continuity", 0.), abs(rates["delta_c"] + theta - 3 * rates["Phi"]) / scale_value)
                scale_value = max(abs(rates["theta_c"]), abs(diagnostics["H"] * theta), abs(system.wave**2 * observables["Psi"]), 1e-80)
                algebra[branch + "_euler"] = max(algebra.get(branch + "_euler", 0.), abs(rates["theta_c"] + diagnostics["H"] * theta - system.wave**2 * observables["Psi"]) / scale_value)
                scale_value = max(abs(diagnostics["z"]), abs(system.wave * diagnostics["alpha"]), abs(3 * rates["eta"] / system.wave), 1e-80)
                algebra[branch + "_kinematics"] = max(algebra.get(branch + "_kinematics", 0.), abs(diagnostics["z"] - system.wave * diagnostics["alpha"] + 3 * rates["eta"] / system.wave) / scale_value)
                step = 5e-7
                density_samples = {}
                eta_samples = {}
                for offset in (-2, -1, 1, 2):
                    moved = state + offset * step * derivative
                    moved_efold = efold + offset * step
                    density_samples[offset] = system.density(moved_efold, moved)
                    eta_samples[offset] = system.evaluate(moved_efold, moved, branch)[3]["eta"]
                density_actual.append((density_samples[-2] - 8 * density_samples[-1] + 8 * density_samples[1] - density_samples[2]) / (12 * step))
                density_expected.append(rates["density_sync"] / diagnostics["H"])
                eta_actual.append((eta_samples[-2] - 8 * eta_samples[-1] + 8 * eta_samples[1] - eta_samples[2]) / (12 * step))
                eta_expected.append(rates["eta"] / diagnostics["H"])
                require(np.count_nonzero(system.evaluate(efold, np.zeros_like(state), branch)[0]) == 0, "zero solution")
        rates_actual, rates_expected = np.array(rates_actual), np.array(rates_expected)
        selections = dict(alpha=[system.alpha_slot], cdm=[system.cdm_slot], core=list(range(len(system.core))), tail=list(range(len(system.core), len(system.units))))
        if model == "heavy":
            selections["heavy"] = system.slots
        for name, selection in selections.items():
            numerical["gr_rhs_" + name] = float(np.max(abs(rates_actual[:, selection] - rates_expected[:, selection])) /
                                                     max(np.max(abs(rates_expected[:, selection])), 1e-80))
        for name, actual, expected in (("density_total_derivative", density_actual, density_expected), ("eta_total_derivative", eta_actual, eta_expected)):
            numerical[name] = float(np.max(abs(np.array(actual) - expected)) / max(np.max(abs(np.asarray(expected))), 1e-80))
        algebra["complete_metric_kernel"] = max(source_mismatch)
        passed = all(np.isfinite(value) and value < ALGEBRA for value in algebra.values()) and all(np.isfinite(value) and value < GATE for value in numerical.values())
        report = dict(model=model, passed=bool(passed), numerical=numerical, algebra=algebra, points=len(grid), probes=len(points),
                      units_sha256=digest(path), background_path=str(path), no_future_sources=True)
        reports.append(report)
        write(RUN / (model + "-preflight.json"), report)
        print(model, "preflight", numerical, algebra, "passed", passed, flush=True)
        require(passed, "preflight failed; inspect before further models or evolution")
    check_parent()
    write(RUN / "preflight-result.json", dict(passed=all(row["passed"] for row in reports), reports=reports, branches=["gr", "poisson-spatial", "newton-dust-force"]))
    print("Poisson source and gauge-driver preflight complete", flush=True)


if __name__ == "__main__":
    main()
