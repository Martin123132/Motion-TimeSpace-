from sourced_emission import *


def cubic_weights(coordinate):
    weights, derivatives = [], []
    for node in range(4):
        others = [index for index in range(4) if index != node]
        denominator = math.prod(node - index for index in others)
        weights.append(math.prod(coordinate - index for index in others) / denominator)
        derivatives.append(sum(math.prod(coordinate - index for index in others if index != removed) for removed in others) / denominator)
    return np.array(weights), np.array(derivatives)


def gaunt_with_log_derivatives(table, gamma_squared, frequency):
    column_coordinate = (math.log10(gamma_squared) - table.gamma_start) / table.step
    row_coordinate = (math.log10(frequency) - table.u_start) / table.step
    if not 0 <= column_coordinate <= table.columns - 1 or not 0 <= row_coordinate <= table.rows - 1:
        raise ValueError('Gaunt derivative extrapolation is not permitted')
    column = int(np.clip(math.floor(column_coordinate) - 1, 0, table.columns - 4))
    row = int(np.clip(math.floor(row_coordinate) - 1, 0, table.rows - 4))
    column_weights, column_derivative = cubic_weights(column_coordinate - column)
    row_weights, row_derivative = cubic_weights(row_coordinate - row)
    block = table.values[row:row + 4, column:column + 4]
    scale = 1 / (table.step * math.log(10))
    return (float(row_weights @ block @ column_weights),
            float(row_weights @ block @ column_derivative * scale),
            float(row_derivative @ block @ column_weights * scale))


def br_coefficient(theta_star, ratio, frequency, densities, tables):
    values, derivatives = [], []
    for charge, density, table in zip([1, 2], densities, tables):
        gaunt, gamma_derivative, frequency_derivative = gaunt_with_log_derivatives(
            table, charge ** 2 * ALPHA ** 2 / (2 * theta_star * ratio), frequency / ratio)
        values.append(charge ** 2 * density * gaunt)
        derivatives.append(charge ** 2 * density * (-.5 * gaunt - gamma_derivative - frequency_derivative))
    scale = ratio ** (-.5)
    return scale * sum(values), scale * sum(derivatives) / ratio
