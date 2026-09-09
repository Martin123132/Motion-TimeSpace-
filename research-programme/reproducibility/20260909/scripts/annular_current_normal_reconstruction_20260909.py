import math

import numpy as numerical

from annular_coupled_current_time_jets_20260909 import series_dot
from annular_curvature_timejet_transfer_20260909 import spatial_derivatives
from sbp4_derived_operator_20260909 import derivative


POWERS = [(time_order, radial_order) for time_order in range(3) for radial_order in range(3 - time_order)]


def spatial_lift(taylor, spacing, method, maximum=3):
    result = {}
    for time_order, values in enumerate(taylor):
        for radial_order, differentiated in enumerate(spatial_derivatives(values, spacing, maximum - time_order, method)):
            result[time_order, radial_order] = differentiated / math.factorial(radial_order)
    return result


def product(first, second, power):
    time_order, radial_order = power
    return sum(first[index, offset] * second[time_order - index, radial_order - offset] for index in range(time_order + 1) for offset in range(radial_order + 1))


def matrix_product(first, second, power):
    time_order, radial_order = power
    return sum(numerical.einsum("ijn,jn->in", first[index, offset], second[time_order - index, radial_order - offset]) for index in range(time_order + 1) for offset in range(radial_order + 1))


def construct_system(engine, time_derivatives, source_coefficients, method):
    count = engine.radii.size
    current = {key: spatial_lift(values, engine.spacing, method) for key, values in engine.current.items() if key in ["q_gradient", "flux_gradient", "V_gradient", "C_gradient", "D_gradient", "constraint_gradient", "fmu_gradient", "f_mu", "J0", "defect"]}
    normalized = time_derivatives[:3] / numerical.array([1, 1, 2])[:, None, None]
    constraint = derivative(normalized[:, 3], engine.spacing) - series_dot(engine.current["constraint_gradient"], normalized)
    constraint_lift = spatial_lift(constraint, engine.spacing, method)
    sources = spatial_lift(source_coefficients, engine.spacing, method)
    reciprocal = {(time_order, radial_order): ((-1)**radial_order / engine.radii**(radial_order + 1) if time_order == 0 else numerical.zeros(count)) for time_order, radial_order in POWERS}
    matrix, state_matrix, time_matrix, forcing = {}, {}, {}, {}
    for power in POWERS:
        time_order, radial_order = power
        leading = numerical.zeros((5, 5, count))
        state = numerical.zeros_like(leading)
        temporal = numerical.zeros_like(leading)
        source = numerical.zeros((5, count))
        if power == (0, 0):
            leading[0, 0] = leading[3, 3] = leading[4, 4] = 1
            state[0, 1] = 1
            temporal[1, 1] = temporal[2, 2] = 1
            temporal[4, 4] = engine.evaluator.sigma
        leading[1] = current["q_gradient"][power]
        leading[2] = current["flux_gradient"][power]
        leading[2, 3] -= current["f_mu"][power]
        state[1] = -(radial_order + 1) * current["q_gradient"][time_order, radial_order + 1]
        state[2] = -(radial_order + 1) * current["flux_gradient"][time_order, radial_order + 1] - 2 * product(reciprocal, current["flux_gradient"], power) + current["V_gradient"][power] - product(current["f_mu"], current["constraint_gradient"], power) + product(current["J0"], current["fmu_gradient"], power)
        state[3] = current["constraint_gradient"][power]
        state[4] = current["D_gradient"][power]
        source[1] = current["defect"][power][1] - sources[power][1]
        source[2] = current["defect"][power][2] - sources[power][2]
        source[3] = constraint_lift[power]
        source[4] = engine.evaluator.sigma * (current["defect"][power][4] - sources[power][4])
        matrix[power], state_matrix[power], time_matrix[power], forcing[power] = leading, state, temporal, source
    leading = numerical.moveaxis(matrix[0, 0], -1, 0)
    condition = numerical.linalg.cond(leading)
    determinant = numerical.linalg.det(leading)
    expected = -engine.current["c"][0] / engine.current["alpha"][0]
    if not numerical.all(numerical.isfinite(condition)) or numerical.max(condition) > 1e8 or numerical.min(numerical.abs(expected)) < 1e-12:
        raise ValueError("Radial reconstruction is unqualified at this characteristic/ill-conditioned surface")
    return {"M": matrix, "A": state_matrix, "B": time_matrix, "f": forcing, "coefficients": current, "sources": sources, "constraint": constraint_lift, "condition": condition, "determinant": determinant, "expected_determinant": expected}


def solve_jets(system, time_derivatives):
    values = {(degree, 0): value / math.factorial(degree) for degree, value in enumerate(time_derivatives)}
    leading = numerical.moveaxis(system["M"][0, 0], -1, 0)
    for radial_order in range(3):
        for time_order in range(3 - radial_order):
            power = time_order, radial_order
            temporal = {(index, offset): (index + 1) * values[index + 1, offset] for index in range(time_order + 1) for offset in range(radial_order + 1)}
            target = matrix_product(system["A"], values, power) + matrix_product(system["B"], temporal, power) + system["f"][power]
            for index in range(time_order + 1):
                for offset in range(radial_order + 1):
                    if (index, offset) != (0, 0):
                        target -= numerical.einsum("ijn,jn->in", system["M"][index, offset], (radial_order - offset + 1) * values[time_order - index, radial_order - offset + 1])
            values[time_order, radial_order + 1] = numerical.linalg.solve(leading, target.T[..., None])[..., 0].T / (radial_order + 1)
    return values


def system_residuals(system, values):
    radial = {(time_order, radial_order): (radial_order + 1) * values[time_order, radial_order + 1] for time_order, radial_order in POWERS}
    temporal = {(time_order, radial_order): (time_order + 1) * values[time_order + 1, radial_order] for time_order, radial_order in POWERS}
    normal = {power: matrix_product(system["M"], radial, power) - matrix_product(system["A"], values, power) - matrix_product(system["B"], temporal, power) - system["f"][power] for power in POWERS}
    mass = {}
    coefficients = system["coefficients"]
    for power in POWERS:
        source = coefficients["defect"][power][3] - system["sources"][power][3]
        mass[power] = temporal[power][3] - numerical.sum(product(coefficients["C_gradient"], values, power), axis=0) + source
    return normal, mass


def physical_mixed(values):
    return {(time_order, radial_order): value[[0, 3, 4]] * math.factorial(time_order) * math.factorial(radial_order) for (time_order, radial_order), value in values.items()}


def hermite_coefficients(values, spacing):
    matrix = numerical.zeros((8, 8))
    for endpoint in range(2):
        for degree in range(4):
            for power in range(degree, 8):
                matrix[4 * endpoint + degree, power] = math.factorial(power) / math.factorial(power - degree) * endpoint**(power - degree)
    shape = (4, 8) + values[0, 0].shape[:-1] + (values[0, 0].shape[-1] - 1,)
    data = numerical.zeros(shape)
    for time_order in range(4):
        target = []
        for endpoint in range(2):
            for degree in range(4):
                value = values.get((time_order, degree), numerical.zeros_like(values[0, 0]))
                target.append(math.factorial(degree) * spacing**degree * (value[:, :-1] if endpoint == 0 else value[:, 1:]))
        data[time_order] = numerical.linalg.solve(matrix, numerical.array(target).reshape(8, -1)).reshape(shape[1:])
    return data


def evaluate_hermite(coefficients, radii, fractions):
    spacing = float(radii[1] - radii[0])
    fractions = numerical.asarray(fractions)
    locations = (radii[:-1, None] + spacing * fractions).ravel()
    mixed = {}
    for time_order in range(4):
        for radial_order in range(4 - time_order):
            result = numerical.zeros((coefficients.shape[2], radii.size - 1, fractions.size))
            for power in range(radial_order, 8):
                factor = math.factorial(power) / math.factorial(power - radial_order) / spacing**radial_order
                result += coefficients[time_order, power, :, :, None] * (factor * fractions**(power - radial_order))
            mixed[time_order, radial_order] = math.factorial(time_order) * result.reshape(coefficients.shape[2], -1)
    return locations, mixed
