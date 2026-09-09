import numpy as numerical

from annular_evolution_operator_20260909 import AnnularFields as PhysicalFields
from annular_evolution_operator_20260909 import coefficients as physical_coefficients
from annular_evolution_operator_20260909 import reference_rhs as physical_rhs


def coefficients(state, spatial, radius, constants, kappa, sigma):
    scalar, time_derivative, mass, shift = state
    physical = numerical.stack([scalar, time_derivative * numerical.exp(-shift), spatial[0] - sigma * time_derivative, mass, shift])
    return physical_coefficients(physical, radius, constants, kappa, sigma)


def reference_rhs(state, spatial, second, radius, constants, kappa, sigma):
    scalar, time_derivative, mass, shift = state
    exponential = numerical.exp(shift)
    physical = numerical.stack([scalar, time_derivative / exponential, spatial[0] - sigma * time_derivative, mass, shift])
    physical_space = numerical.stack([spatial[0], (spatial[1] - spatial[3] * time_derivative) / exponential, second[0] - sigma * spatial[1], spatial[2], spatial[3]])
    derivative = physical_rhs(physical, physical_space, radius, constants, kappa, sigma)
    return numerical.stack([time_derivative, exponential * derivative[1] + time_derivative * derivative[4], derivative[3], derivative[4]])


def local_jacobians(state, spatial, second, radius, constants, kappa, sigma):
    matrices = []
    step = 1e-30
    for selected in range(3):
        columns = []
        for component in range(4):
            arguments = [state, spatial, second]
            arguments[selected] = arguments[selected].astype(complex)
            arguments[selected][component] += 1j * step
            columns.append(reference_rhs(*arguments, radius, constants, kappa, sigma).imag / step)
        matrices.append(numerical.stack(columns, axis=1))
    return matrices


def multiply(first, second):
    return numerical.stack([first[0] * second[0], first[0] * second[1] + first[1] * second[0]])


class AnnularFields(PhysicalFields):
    def evaluate(self, times, radii, epsilon):
        original = super().evaluate(times, radii, epsilon)
        state, time, spatial, defect = [original[key] for key in ["state", "state_time", "state_space", "defect"]]
        exponential = numerical.stack([numerical.exp(state[0, 4]), numerical.exp(state[0, 4]) * state[1, 4]])
        coordinate_velocity = multiply(exponential, state[:, 1])
        velocity_time = multiply(exponential, time[:, 1] + multiply(state[:, 1], time[:, 4]))
        velocity_space = multiply(exponential, spatial[:, 1] + multiply(state[:, 1], spatial[:, 4]))
        velocity_defect = multiply(exponential, defect[:, 1]) + multiply(coordinate_velocity, defect[:, 4])
        result = {
            "state": numerical.stack([state[:, 0], coordinate_velocity, state[:, 3], state[:, 4]], axis=1),
            "state_time": numerical.stack([time[:, 0], velocity_time, time[:, 3], time[:, 4]], axis=1),
            "state_space": numerical.stack([spatial[:, 0], velocity_space, spatial[:, 3], spatial[:, 4]], axis=1),
            "defect": numerical.stack([defect[:, 0], velocity_defect, defect[:, 3], defect[:, 4]], axis=1),
            "initial_constraint": original["initial_constraint"],
        }
        result["state_second"] = numerical.zeros_like(result["state"])
        result["state_second"][:, 0] = spatial[:, 2] + self.sigma * velocity_space
        return result
