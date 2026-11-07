from mixed_common import *


def thermal_weights(first, second, theta, gamma, shift):
    electron_theta = theta * (1 + shift)
    normalization = -math.log1p(shift) + math.log(special.kve(2, 1 / theta) / special.kve(2, 1 / electron_theta))
    logarithm = (gamma - 1) * shift / (theta * (1 + shift)) + normalization
    reverse_log = logarithm + (first - second) * shift / (1 + shift)
    forward, reverse = np.exp(logarithm), np.exp(reverse_log)
    difference = -forward * np.expm1(reverse_log - logarithm)
    mean_gamma = special.kve(1, 1 / electron_theta) / special.kve(2, 1 / electron_theta) + 3 * electron_theta
    logarithmic_derivative = (gamma - mean_gamma) / (theta * (1 + shift) ** 2)
    return forward, reverse, difference, logarithm, reverse_log, logarithmic_derivative


def coefficients(first, second, initial, final, heat, shift, theta, gamma):
    incident_planck, outgoing_planck = 1 / np.expm1(first), 1 / np.expm1(second)
    initial_shift, final_shift = heat * initial, heat * final
    forward, reverse, difference, logarithm, reverse_log, logarithmic_derivative = thermal_weights(first, second, theta, gamma, shift)
    delta_left = (np.expm1(logarithm) + difference * incident_planck
                  + final_shift * (forward * (outgoing_planck - incident_planck)
                                   + difference * incident_planck * (1 + outgoing_planck)))
    delta_right = (np.expm1(reverse_log) - difference * outgoing_planck
                   + initial_shift * (reverse * (incident_planck - outgoing_planck)
                                      - difference * outgoing_planck * (1 + incident_planck)))
    backward_change = ((1 + outgoing_planck) * final_shift + incident_planck * initial_shift
                       + incident_planck * (1 + outgoing_planck) * initial_shift * final_shift)
    occupation_difference = initial_shift - final_shift + (outgoing_planck - incident_planck) * initial_shift * final_shift
    flux = forward * occupation_difference + difference * (1 + backward_change)
    backward_weight_change = np.expm1(reverse_log) + reverse * backward_change
    temperature_defect = (logarithmic_derivative * flux
                          + (first - second) * (2 * shift + shift ** 2 - backward_weight_change) / (1 + shift) ** 2)
    linear_flux = initial_shift - final_shift - (first - second) * shift
    flux_defect = flux - linear_flux
    return delta_left, delta_right, temperature_defect, flux, flux_defect
