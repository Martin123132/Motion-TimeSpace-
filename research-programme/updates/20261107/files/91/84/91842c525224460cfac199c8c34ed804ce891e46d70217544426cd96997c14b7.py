from emission_common import *


ALPHA = 7.2973525643e-3
DC_CONSTANT = 4 * ALPHA / (3 * math.pi) * 4 * math.pi ** 4 / 15


def dc_absorption_shape(frequency, variant):
    frequency = np.asarray(frequency)
    shape = (-np.expm1(-frequency)) / frequency ** 3
    if variant == 'dc':
        polynomial = 1 + 1.5 * frequency + 29 / 24 * frequency ** 2 + 11 / 16 * frequency ** 3 + 5 / 12 * frequency ** 4
        shape *= np.exp(-frequency) * polynomial
    elif variant not in ['soft', 'none']:
        raise ValueError(variant)
    return shape


class EmissionMatrices:
    def __init__(self, basis, quadrature=600):
        self.basis = basis
        self.frequency, self.measure = thermal_wave.frequency_quadrature(quadrature, basis.minimum, basis.maximum)
        self.values = basis.evaluate(self.frequency)
        self.matrices = {variant: (self.values.T * (self.measure * dc_absorption_shape(self.frequency, variant))) @ self.values
                         for variant in ['soft', 'dc']}
        self.matrices['none'] = np.zeros_like(basis.mass)

    def at(self, theta, variant):
        correction = 1 / (1 + 14.16 * theta) if variant == 'dc' else 1.
        return DC_CONSTANT * theta ** 2 * correction * self.matrices[variant]
