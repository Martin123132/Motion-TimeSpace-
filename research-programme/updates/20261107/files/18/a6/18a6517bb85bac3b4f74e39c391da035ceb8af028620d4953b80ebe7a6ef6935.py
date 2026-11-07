from emission_angular_common import *


def legendre_coefficients(fraction):
    fraction = np.asarray(fraction)
    first = 2 * (1 - fraction) ** 2 * (3 - 7 * fraction + 13 * fraction ** 2 - 7 * fraction ** 3 + 3 * fraction ** 4)
    second = 11 - 21 * fraction + 30 * fraction ** 3 - 21 * fraction ** 5 + 11 * fraction ** 6
    return np.array([first + 2 * second / 3 + 20 * fraction ** 3 / 3,
                     -16 * fraction ** 3, -2 * second / 3 + 40 * fraction ** 3 / 3, -4 * fraction ** 3])


def marginal_eigenvalue(fraction, degree):
    coefficients = legendre_coefficients(fraction)
    if degree > 3:
        return np.zeros_like(np.asarray(fraction))
    return coefficients[degree] / ((2 * degree + 1) * coefficients[0])


def angle_polynomial(fraction, cosine):
    first = 2 * (1 - fraction) ** 2 * (3 - 7 * fraction + 13 * fraction ** 2 - 7 * fraction ** 3 + 3 * fraction ** 4)
    second = 11 - 21 * fraction + 30 * fraction ** 3 - 21 * fraction ** 5 + 11 * fraction ** 6
    return first + second * (1 - cosine ** 2) - 10 * fraction ** 3 * cosine * (1 - cosine) ** 2


def correlations(fraction, degree):
    incident_soft = marginal_eigenvalue(fraction, degree)
    incident_companion = marginal_eigenvalue(1 - fraction, degree)
    companion_soft = marginal_eigenvalue(-fraction / (1 - fraction), degree)
    return incident_companion, incident_soft, companion_soft


def soft_differential(incident_companion, incident_soft, companion_soft):
    return (1 + incident_companion ** 2) * (1 - incident_companion - .5 * (companion_soft - incident_soft) ** 2)
