import math

import numpy as numerical
from scipy.linalg import solve_banded

from annular_coordinate_evolution_operator_20260909 import coefficients
from annular_evolution_operator_20260909 import equations
from annular_fifth_order_jet_20260909 import Jet, KEYS, INDEX, MAX_ORDER
from sbp4_derived_operator_20260909 import derivative


def constraint_coefficients(state, spatial, radius, evaluator):
    data = coefficients(state, spatial, radius, evaluator.constants, evaluator.kappa, evaluator.sigma)
    scalar, coordinate_velocity = state[:2]
    velocity = coordinate_velocity / data["E"]
    radial = spatial[0] - evaluator.sigma * coordinate_velocity
    raised = velocity + data["F"] * radial
    scalar_coefficient = evaluator.kappa * radius**2 * evaluator.constants["m_chi"]**2 * scalar
    velocity_coefficient = -evaluator.kappa * velocity * data["at"]
    mass_coefficient = -data["D"] - evaluator.kappa * velocity * (data["jmu_v"] - evaluator.sigma * data["jmu_r"])
    lapse_coefficient = evaluator.kappa * velocity * coordinate_velocity * (data["a"] - evaluator.sigma * data["b"])
    radial_coefficient = evaluator.kappa * radius**2 * (data["P"] * data["F"] * radial - 2 * data["Px"] * velocity * radial * raised) + evaluator.sigma * evaluator.kappa * radius**2 * data["E"] * velocity * (data["P"] * data["F"] + 2 * data["Px"] * raised**2)
    return numerical.stack([scalar_coefficient, velocity_coefficient, mass_coefficient, lapse_coefficient, radial_coefficient])


def rate(state, spatial, radius, evaluator):
    data = coefficients(state, spatial, radius, evaluator.constants, evaluator.kappa, evaluator.sigma)
    return evaluator.kappa * state[1] * data["jmu_r"] / data["E"]


def derivative_band(count, spacing):
    matrix = derivative(numerical.eye(count), spacing).T
    matrix[-1] = 0
    matrix[-1, -1] = 1
    rows, columns = numerical.nonzero(matrix)
    if numerical.any(numerical.abs(rows - columns) > 3):
        raise ValueError("Unexpected SBP bandwidth")
    band = numerical.zeros((7, count))
    band[3 + rows - columns, columns] = matrix[rows, columns]
    return band


def complete_mass(sources, gradient, band):
    matrix = band.copy()
    matrix[3] -= gradient[2]
    matrix[3, -1] = 1
    forcing = gradient[1] * sources[:, 1] + gradient[3] * sources[:, 3]
    forcing[:, -1] = 0
    result = sources.copy()
    result[:, 2] = solve_banded((3, 3), matrix, forcing.T, check_finite=False).T
    return result


def constraint_action(gradient, values, spacing):
    return derivative(values[:, 2], spacing) - numerical.einsum("in,bin->bn", gradient[:4], values) - gradient[4] * derivative(values[:, 0], spacing)


def constraint_source_time(evaluator, times, radii, epsilon):
    times, radii = numerical.broadcast_arrays(times, radii)
    shape = times.shape
    Jet.numpy, Jet.count = numerical, times.size
    advanced = times.ravel() + evaluator.sigma * (radii.ravel() - 4)
    time_jet, radius_jet = Jet.variable(advanced, 1), Jet.variable(radii.ravel(), 2)
    coupling = Jet.variable(0, 0)
    coefficient_values = [value if isinstance(value, Jet) else Jet.constant(value) for value in evaluator.evaluator(time_jet, radius_jet)]
    harmonics = {}
    for kind, mode in set((entry[2], entry[3]) for entry in evaluator.metadata):
        data = numerical.zeros((len(KEYS), Jet.count))
        active = []
        for degree in range(MAX_ORDER + 1):
            position = INDEX[0, degree, 0]
            angle = mode * advanced / epsilon + degree * numerical.pi / 2
            data[position] = (numerical.cos(angle) if kind == "cos" else numerical.sin(angle)) * (mode / epsilon)**degree / math.factorial(degree)
            active.append(position)
        harmonics[kind, mode] = Jet(data, active)
    fields = {field: Jet.constant(0) for field in evaluator.case["fields"]}
    for (field, order, kind, mode), value in zip(evaluator.metadata, coefficient_values):
        fields[field] += epsilon**order * value * harmonics[kind, mode]
    residuals, unused_lapse, unused_weyl = equations(fields, radius_jet, coupling, evaluator.case)
    constraint = residuals["mass_radial"] + evaluator.sigma * residuals["mass_time"]
    return numerical.stack([constraint.extract(degree).reshape(shape) for degree in [0, 1]]), numerical.stack([constraint.derivative(1).extract(degree).reshape(shape) for degree in [0, 1]])


def background_bias(snapshot, correction, correction_radial, radius, evaluator):
    base, spatial = snapshot["state"][0], snapshot["state_space"][0]
    step = 1e-30
    varied_spatial = spatial.astype(complex)
    varied_spatial[0] += 1j * step * correction_radial[0, 0]
    varied_rate = rate(base.astype(complex) + 1j * step * correction[0], varied_spatial, radius, evaluator).imag / step
    second_gradient = constraint_coefficients(base.astype(complex) + 1j * step * snapshot["defect"][0], spatial, radius, evaluator).imag / step
    return varied_rate * snapshot["initial_constraint"][0] - numerical.einsum("in,in->n", second_gradient[:4], correction[0]) - second_gradient[4] * correction_radial[0, 0]
