import numpy as numerical

from annular_conservative_scalar_evolution_20260909 import constitutive
from annular_evolution_operator_20260909 import coefficients as physical_coefficients
from annular_noether_completion_20260909 import constraint_coefficients


def primitive_data(primitive, radii, constants, kappa, sigma):
    scalar, velocity, gradient, mass, shift = primitive
    exponential = numerical.exp(shift)
    lapse = 1 - 2 * mass / radii - constants["Lambda"] * radii**2 / 3
    current = constitutive(velocity, gradient, exponential, lapse, constants, sigma)
    physical = physical_coefficients(numerical.stack([scalar, velocity / exponential, gradient - sigma * velocity, mass, shift]), radii, constants, kappa, sigma)
    return {**current, "E": exponential, "F": lapse, "D0": physical["D"], "C0": physical["C"], "G0": physical["R"] + sigma * physical["C"], "f_mu": -2 * current["flux_F"] / radii, "h_mu": -2 * current["h_F"] / radii, "h_delta": exponential * current["h_E"], "potential_force": exponential * constants["m_chi"]**2 * scalar}


def maps(primitive, radii, evaluator):
    data = primitive_data(primitive, radii, evaluator.constants, evaluator.kappa, evaluator.sigma)
    shape = primitive.shape[1:]
    transform = numerical.zeros((5, 5) + shape)
    for component in range(5):
        transform[component, component] = 1
    transform[1] = 0
    transform[1, 1] = data["B"] / data["alpha"]
    transform[1, 2] = 1 / data["alpha"]
    transform[1, 3] = -data["h_mu"] / data["alpha"]
    transform[1, 4] = -data["h_delta"] / data["alpha"]
    transform[2] = 0
    transform[2, 1] = 1
    names = ["flux", "C0", "D0", "potential_force", "f_mu"]
    jacobians = {name: [] for name in names}
    for component in range(5):
        varied = primitive.astype(complex)
        varied[component] += 1j * 1e-30
        result = primitive_data(varied, radii, evaluator.constants, evaluator.kappa, evaluator.sigma)
        for name in names:
            jacobians[name].append(result[name].imag / 1e-30)
    gradients = {name: numerical.einsum("i...,ij...->j...", numerical.stack(columns), transform) for name, columns in jacobians.items()}
    gradients["q"] = transform[1]
    state = primitive[[0, 1, 3, 4]]
    spatial = numerical.zeros_like(state)
    spatial[0] = primitive[2]
    old_gradient = constraint_coefficients(state, spatial, radii, evaluator)
    gradients["constraint"] = numerical.einsum("i...,ij...->j...", old_gradient[[0, 1, 4, 2, 3]], transform)
    return data, gradients, old_gradient, transform


def principal(data, gradients, sigma, reduced=True):
    shape = data["alpha"].shape
    matrix = numerical.zeros((5, 5) + shape)
    matrix[1] = gradients["q"]
    matrix[2] = gradients["flux"]
    if reduced:
        matrix[2, 3] -= data["f_mu"]
    matrix[4, 4] = 1 / sigma
    return matrix


def snapshot_coefficients(snapshot, radii, evaluator):
    state, spatial, second, time = [snapshot[name][0] for name in ["state", "state_space", "state_second", "state_time"]]
    primitive = numerical.stack([state[0], state[1], spatial[0], state[2], state[3]])
    primitive_space = numerical.stack([spatial[0], spatial[1], second[0], spatial[2], spatial[3]])
    data, gradients, old_gradient, transform = maps(primitive, radii, evaluator)
    perturbed = primitive_data(primitive.astype(complex) + 1j * 1e-30 * primitive_space, radii.astype(complex) + 1j * 1e-30, evaluator.constants, evaluator.kappa, evaluator.sigma)
    current_space = perturbed["flux"].imag / 1e-30
    constraint = spatial[2] - data["G0"]
    momentum_time = data["alpha"] * time[1] - data["B"] * spatial[1] + data["h_mu"] * time[2] + data["h_delta"] * time[3]
    background = numerical.stack([state[0], spatial[0], data["momentum"], state[2], state[3]])
    background_time = numerical.stack([time[0], spatial[1], momentum_time, time[2], time[3]])
    reference = numerical.stack([state[1], spatial[1], current_space + 2 * data["flux"] / radii - data["potential_force"] - data["f_mu"] * constraint, data["C0"], (spatial[3] - data["D0"]) / evaluator.sigma])
    expected = numerical.stack([snapshot["defect"][0, 0], numerical.zeros_like(state[0]), data["alpha"] * snapshot["defect"][0, 1] + data["h_mu"] * snapshot["defect"][0, 2] + data["h_delta"] * snapshot["defect"][0, 3], snapshot["defect"][0, 2], snapshot["defect"][0, 3]])
    return {"background": background, "background_time": background_time, "defect": background_time - reference, "independent_defect": expected, "J0": constraint, "old_gradient": old_gradient, "q_gradient": gradients["q"], "flux_gradient": gradients["flux"], "C_gradient": gradients["C0"], "D_gradient": gradients["D0"], "V_gradient": gradients["potential_force"], "fmu_gradient": gradients["f_mu"], "constraint_gradient": gradients["constraint"], "alpha": data["alpha"], "B": data["B"], "c": data["c"], "P": data["P"], "Q": data["Q"], "f_mu": data["f_mu"], "h_mu": data["h_mu"], "h_delta": data["h_delta"], "q0": state[1], "E": data["E"], "principal": principal(data, gradients, evaluator.sigma), "raw_principal": principal(data, gradients, evaluator.sigma, reduced=False)}


def physical_transform(primitive, data, sigma):
    scalar, velocity, gradient, mass, shift = primitive
    shape = scalar.shape
    transform = numerical.zeros((5, 5) + shape)
    transform[0, 0] = 1
    transform[1, 1] = sigma * data["E"]
    transform[1, 2] = 1
    transform[1, 4] = sigma * velocity
    transform[2, 1] = data["E"] * (data["alpha"] - sigma * data["B"])
    transform[2, 2] = -data["B"]
    transform[2, 3] = data["h_mu"]
    transform[2, 4] = velocity * (data["alpha"] - sigma * data["B"]) + data["h_delta"]
    transform[3, 3] = 1
    transform[4, 4] = 1
    return transform
