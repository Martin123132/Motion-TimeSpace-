from mixed_common import *


def exponential_remainder(value):
    value = np.asarray(value)
    series = value ** 2 * (.5 + value * (1 / 6 + value * (1 / 24 + value * (1 / 120 + value / 720))))
    return np.where(abs(value) < .001, series, np.expm1(value) - value)


def electron_weights(first, second, theta, gamma, shift):
    nodes, weights = np.polynomial.legendre.leggauss(4)
    offsets = .5 * shift * (nodes + 1)
    local_theta = theta * (1 + offsets)
    mean_gamma = special.kve(1, 1 / local_theta) / special.kve(2, 1 / local_theta) + 3 * local_theta
    normalization = -.5 * shift * np.dot(weights, (mean_gamma - 1) / (theta * (1 + offsets) ** 2))
    logarithm = (gamma - 1) * shift / (theta * (1 + shift)) + normalization
    log_ratio = (first - second) * shift / (1 + shift)
    forward, reverse = np.exp(logarithm), np.exp(logarithm + log_ratio)
    difference = -forward * np.expm1(log_ratio)
    electron_theta = theta * (1 + shift)
    mean_gamma = special.kve(1, 1 / electron_theta) / special.kve(2, 1 / electron_theta) + 3 * electron_theta
    derivative = (gamma - mean_gamma) / (theta * (1 + shift) ** 2)
    return forward, reverse, difference, logarithm, log_ratio, derivative


def coefficients(first, second, initial, final, heat, shift, theta, gamma):
    incident_planck, outgoing_planck = 1 / np.expm1(first), 1 / np.expm1(second)
    initial_shift, final_shift = heat * initial, heat * final
    forward, reverse, difference, logarithm, log_ratio, derivative = electron_weights(first, second, theta, gamma, shift)
    left = (np.expm1(logarithm) + difference * incident_planck
            + final_shift * (forward * (outgoing_planck - incident_planck)
                             + difference * incident_planck * (1 + outgoing_planck)))
    right = (np.expm1(logarithm + log_ratio) - difference * outgoing_planck
             + initial_shift * (reverse * (incident_planck - outgoing_planck)
                                - difference * outgoing_planck * (1 + incident_planck)))
    backward_change = ((1 + outgoing_planck) * final_shift + incident_planck * initial_shift
                       + incident_planck * (1 + outgoing_planck) * initial_shift * final_shift)
    flux_defect = (np.expm1(logarithm) * (initial_shift - final_shift - np.expm1(log_ratio))
                   + forward * (outgoing_planck - incident_planck) * initial_shift * final_shift
                   - exponential_remainder(log_ratio) + (first - second) * shift ** 2 / (1 + shift)
                   + difference * backward_change)
    linear_flux = heat * (initial - final) - (first - second) * shift
    flux = linear_flux + flux_defect
    reverse_weight_change = np.expm1(logarithm + log_ratio) + reverse * backward_change
    temperature = derivative * flux + (first - second) * (2 * shift + shift ** 2 - reverse_weight_change) / (1 + shift) ** 2
    return left, right, temperature, flux_defect
