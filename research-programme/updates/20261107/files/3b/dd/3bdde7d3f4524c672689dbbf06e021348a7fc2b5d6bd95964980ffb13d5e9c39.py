from soft_matching_common import *
from emission_rates import ALPHA


def cusp_coefficient(speed):
    speed = float(speed)
    if abs(speed) < .05:
        series = sum(speed ** (2 * power) / (2 * power + 1) for power in range(1, 10))
        return 2 * ALPHA / math.pi * series
    return 2 * ALPHA / math.pi * (np.arctanh(speed) / speed - 1)


def thermal_bracket(frequency, conjugate, temperature=1.):
    phase = frequency * conjugate
    return 1j * np.sin(phase) - 2 * np.sin(phase / 2) ** 2 / np.tanh(frequency / (2 * temperature))


def exponent(conjugate, separator, lower=0., temperature=1., amplitude=1.):
    def integrand(frequency):
        if frequency == 0:
            return 1j * conjugate - temperature * conjugate ** 2
        return thermal_bracket(frequency, conjugate, temperature) / frequency
    real = integrate.quad(lambda frequency: integrand(frequency).real, lower, separator, epsabs=1e-13, epsrel=1e-13)[0]
    imaginary = integrate.quad(lambda frequency: integrand(frequency).imag, lower, separator, epsabs=1e-13, epsrel=1e-13)[0]
    return amplitude * complex(real, imaginary)


def unresolved_bound(conjugate, lower, temperature=1., amplitude=1.):
    return amplitude * lower * (abs(conjugate) + temperature * abs(conjugate) ** 2 + lower * abs(conjugate) ** 2 / 2)


def cumulants(separator, temperature=1., amplitude=1.):
    mean = amplitude * separator
    variance = amplitude * integrate.quad(lambda frequency: 2 * temperature if frequency == 0 else frequency / np.tanh(frequency / (2 * temperature)),
        0., separator, epsabs=1e-13, epsrel=1e-13)[0]
    return mean, variance
