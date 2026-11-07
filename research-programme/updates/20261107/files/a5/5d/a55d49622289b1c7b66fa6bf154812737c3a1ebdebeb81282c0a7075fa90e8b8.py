from wave_common import *


def leading_coefficients(first, second, initial, final, gas_temperature, theta, gamma):
    incident = 1 / np.expm1(first)
    outgoing = 1 / np.expm1(second)
    difference = first - second
    mean_gamma = special.kve(1, 1 / theta) / special.kve(2, 1 / theta) + 3 * theta
    electron_derivative = (gamma - mean_gamma) / theta
    left = gas_temperature * electron_derivative - difference * gas_temperature * incident + final * (outgoing - incident)
    right = gas_temperature * electron_derivative + difference * gas_temperature * (1 + outgoing) + initial * (incident - outgoing)
    thermal = electron_derivative * (initial - final - difference * gas_temperature)
    thermal += difference * (2 * gas_temperature - gas_temperature * (electron_derivative + difference)
                            - (1 + outgoing) * final - incident * initial)
    return left, right, thermal
