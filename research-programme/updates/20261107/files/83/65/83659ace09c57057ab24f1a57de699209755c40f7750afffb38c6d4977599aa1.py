from common import *
from adjoint_operator import open_owned, relative, sup
from physical_energy_map import PhysicalEnergyMap
from forcing_math import explicit
from comparison_math import controls
from scipy.interpolate import make_interp_spline
from scipy.linalg import expm
import numpy as np
import time


def subset(path, names):
    with np.load(path) as archive:
        return {name: archive[name].copy() for name in names}


def propagate_components(grid, comparison, forcing, initial):
    state, half = np.zeros((2, 4)), np.zeros((2, 4))
    state[:, 0] = initial
    half[:, 0] = initial
    for index, matrix in enumerate(comparison):
        if index % 256 == 0:
            guard()
        augmented = np.zeros((4, 4))
        augmented[:2, :2] = matrix
        augmented[:2, 2:] = np.eye(2)
        step = float(grid[index + 1] - grid[index])
        transition = expm(augmented * step)
        half_transition = expm(augmented * (step / 2))
        state = transition[:2, :2] @ state
        state[:, 1:] += transition[:2, 2:] @ forcing[index].T
        for division in range(2):
            half = half_transition[:2, :2] @ half
            half[:, 1:] += half_transition[:2, 2:] @ forcing[index].T
    return state, relative(state - half, state)


def main():
    modest()
    check_parent()
    require(read(ROOT / "qualification.json")["passed"], "qualified explicit forcing")
    (ROOT / "budget-contexts").mkdir(exist_ok=False)
    (ROOT / "budget").mkdir(exist_ok=False)
    write(ROOT / "budget/inputs.json", dict(sources=frozen_sources(), numerical=GATE, algebra=ALGEBRA,
                                          unchanged_parent_comparison=True, new_physical_ode_solves=0))
    reports = []
    for model in ("heavy", "cold"):
        guard()
        started = time.monotonic()
        old_path = ENVELOPE / LABEL / "bound" / model / "result.json"
        previous = read(old_path)
        require(digest(previous["packet"]) == previous["sha256"], "parent interval packet")
        parent = subset(previous["packet"], ("efold", "comparison", "forcing", "initial", "readout_norm", "terminal_boundary", "source"))
        grid = parent["efold"]
        reference_path = POISSON / "evolution" / (model + "-gr.npz")
        reference = subset(reference_path, ("efold", "H", "values", "value_names"))
        physical_path = ADJOINT / "response-v2/adjoints" / (model + "-physical-sources.npz")
        physical = subset(physical_path, ("efold", "momentum", "shear"))
        require(np.array_equal(grid, reference["efold"]) and np.array_equal(grid, physical["efold"]), "original grids unchanged")
        system = open_owned(model, "budget-contexts")
        energy = PhysicalEnergyMap(system)
        current_force = np.empty_like(parent["source"])
        shear_force = np.empty_like(current_force)
        for index, efold in enumerate(grid):
            if index % 256 == 0:
                guard()
            calculated = explicit(system, energy, float(efold))
            current_force[index] = calculated["current"] * physical["momentum"][index]
            shear_force[index] = calculated["shear"] * physical["shear"][index]
            if index == 0:
                initial_primitive = calculated["primitive"] * physical["momentum"][index]
            if index == len(grid) - 1:
                final_primitive = calculated["primitive"] * physical["momentum"][index]
            if index % 4096 == 0:
                print(LABEL, model, "explicit source nodes", index + 1, "/", len(grid), "seconds", round(time.monotonic() - started, 1), flush=True)
        residual_force = parent["source"] - current_force - shear_force
        representation = sup(residual_force) / max(sup(parent["source"]), sup(current_force), sup(shear_force), 1e-80)
        require(representation < GATE, "explicit coefficient representation gate")
        coefficients = np.stack([current_force, shear_force, residual_force], axis=1)
        curve = make_interp_spline(grid, coefficients, k=5, axis=0)
        old_curve = make_interp_spline(grid, parent["source"], k=5, axis=0)
        forcing_bounds = np.empty((len(grid) - 1, 3, 2))
        reconstruction = 0.
        envelope_shortfall = 0.
        for begin in range(0, len(grid) - 1, 256):
            guard()
            end = min(begin + 256, len(grid) - 1)
            left, right = grid[begin:end], grid[begin + 1:end + 1]
            control = controls(curve, left, right)
            heavy = np.linalg.norm(control[..., energy.heavy], axis=-1) if len(energy.heavy) else np.zeros(control.shape[:3])
            rest = np.linalg.norm(control[..., energy.rest], axis=-1)
            forcing_bounds[begin:end] = np.stack([heavy, rest], axis=-1).max(axis=1) * (1 + 64 * np.finfo(float).eps)
            total = forcing_bounds[begin:end].sum(axis=1)
            shortfall = np.max(parent["forcing"][begin:end] - total)
            envelope_shortfall = max(envelope_shortfall, float(shortfall) / max(sup(parent["forcing"][begin:end]), 1e-80))
            sample = left + .371 * (right - left)
            reconstruction = max(reconstruction, relative(curve(sample).sum(axis=1) - old_curve(sample), old_curve(sample)))
        require(reconstruction < ALGEBRA and envelope_shortfall < ALGEBRA, "preserve parent forcing with residual")
        initial_norm = np.array([np.linalg.norm(initial_primitive[energy.heavy]) if len(energy.heavy) else 0., np.linalg.norm(initial_primitive[energy.rest])])
        require(relative(initial_norm - parent["initial"], parent["initial"]) < GATE, "initial primitive restored")
        states, integration_error = propagate_components(grid, parent["comparison"], forcing_bounds, parent["initial"])
        require(integration_error < GATE and np.min(states) >= -ALGEBRA * max(sup(states), 1e-80), "positive comparison component propagation")
        contributions = np.column_stack([parent["readout_norm"] @ states, parent["terminal_boundary"]])
        total_bound = contributions.sum(axis=1)
        old_bound = np.asarray(previous["prediction"]["bound"])
        require(np.all(total_bound + ALGEBRA * max(sup(total_bound), 1e-80) >= old_bound), "source-separated envelope cannot beat original combined-source envelope")
        require(np.all(abs(np.array(previous["measured"])) <= total_bound), "independent saved forward difference covered")
        require(np.max(contributions[:, 3] / total_bound) < GATE, "representation contribution tracked and small")
        names = reference["value_names"].tolist()
        current = reference["values"][:, names.index("Q")]
        shear = reference["values"][:, names.index("Pi")]
        source_current = 3 * reference["H"] * current / (2 * system.wave**3)
        source_shear = shear / system.wave**2
        require(relative(source_current - physical["momentum"], physical["momentum"]) < ALGEBRA and
                relative(source_shear - physical["shear"], physical["shear"]) < ALGEBRA, "original stress source dictionary")
        epsilon = float(np.max(reference["H"]) / system.wave)
        conditions = {}
        for observable in ("D", "delta_c"):
            output_scale = float(np.max(abs(reference["values"][:, names.index(observable)])))
            amplitude = output_scale / reference["H"][-1]**2 if observable == "D" else output_scale
            q_star = float(np.max(abs(current) / (reference["H"]**2 * amplitude)))
            pi_star = float(np.max(abs(shear) / (reference["H"]**2 * amplitude)))
            conditions[observable] = dict(original_output_scale=output_scale, amplitude=amplitude, q_star=q_star, pi_star=pi_star,
                                          epsilon=epsilon, source_indicator=epsilon * q_star + pi_star,
                                          initial_indicator=epsilon**2 * q_star, terminal_indicator=epsilon**3 * q_star,
                                          indicator_not_complete_error_bound=True)
        packet_path = ROOT / "budget" / (model + "-source-components.npz")
        np.savez_compressed(packet_path, efold=grid, physical_current=physical["momentum"], physical_shear=physical["shear"],
                            current_force=current_force, shear_force=shear_force, representation_force=residual_force,
                            forcing_bounds=forcing_bounds, propagated_components=states,
                            initial_primitive=initial_primitive, final_primitive=final_primitive,
                            contributions=contributions, total_bound=total_bound)
        prediction = dict(output_order=["D", "delta_c"], contribution_order=["initial", "current", "shear", "representation", "terminal"],
                          contributions=contributions.tolist(), total_bound=total_bound.tolist())
        write(ROOT / "budget" / (model + "-prediction.json"), prediction)
        report = dict(model=model, passed=True, prediction=prediction, previous_combined_bound=old_bound.tolist(),
                      measured=previous["measured"], source_conditions=conditions,
                      errors=dict(representation=representation, reconstruction=reconstruction, envelope_shortfall=envelope_shortfall,
                                  integration=integration_error, representation_budget_fraction=float(np.max(contributions[:, 3] / total_bound))),
                      parent_interval_packet=previous["packet"], parent_interval_sha256=previous["sha256"],
                      source_packet=str(packet_path), source_sha256=digest(packet_path),
                      input_hashes={str(old_path): digest(old_path), str(reference_path): digest(reference_path), str(physical_path): digest(physical_path)},
                      seconds=time.monotonic() - started, new_physical_ode_solves=0,
                      scope="Separated forcing envelopes of the same parent quintic model; explicit representation residual retained")
        write(ROOT / "budget" / (model + "-result.json"), report)
        print(LABEL, model, "source/readout budget", total_bound.tolist(), "representation", representation,
              "seconds", round(report["seconds"], 1), flush=True)
        reports.append(report)
        del system, energy, reference, physical, parent, current_force, shear_force, residual_force, coefficients, curve, old_curve
    for path, expected in read(ROOT / "budget/inputs.json")["sources"].items():
        require(digest(path) == expected, "frozen budget source")
    check_parent()
    write(ROOT / "budget/result.json", dict(passed=True, reports=reports))


if __name__ == "__main__":
    main()
