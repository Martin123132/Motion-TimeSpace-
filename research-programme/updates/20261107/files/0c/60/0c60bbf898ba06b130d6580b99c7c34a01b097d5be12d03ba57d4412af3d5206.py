from sourced_emission import *


def integrated_dc_absorption_shape(frequency, order=96):
    frequency = np.asarray(frequency)
    nodes, weights = special.roots_laguerre(order)
    incident = 2 * frequency[..., None] + nodes
    fraction = frequency[..., None] / incident
    product = fraction * (1 - fraction)
    gould = (1 - 3 * product + 1.5 * product ** 2 - product ** 3) / (1 - fraction)
    integral = np.sum(weights * incident ** 4 * gould /
                      ((-np.expm1(-incident)) * (-np.expm1(-(incident - frequency[..., None])))), axis=-1)
    return np.exp(-frequency) * (-np.expm1(-frequency)) / frequency ** 3 * integral / (4 * math.pi ** 4 / 15)


class IntegratedDCEmission(SourcedEmission):
    def __init__(self, basis, background, quadrature=900, temperature_knots=81, nonrelativistic=False, gaunt_order=96):
        super().__init__(basis, background, quadrature, temperature_knots, nonrelativistic)
        shape = integrated_dc_absorption_shape(self.frequency, gaunt_order)
        self.matrices['dc'] = (self.values.T * (self.measure * shape)) @ self.values
