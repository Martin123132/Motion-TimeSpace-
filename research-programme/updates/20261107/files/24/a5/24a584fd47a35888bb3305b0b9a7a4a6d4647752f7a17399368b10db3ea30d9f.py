from nonlocal_common import *


def gould(fraction):
    product = fraction * (1 - fraction)
    return (1 - 3 * product + 1.5 * product**2 - product**3) / (1 - fraction)


def frequency_nodes(order, minimum, maximum):
    nodes, weights = np.polynomial.legendre.leggauss(order)
    halfwidth = math.log(maximum / minimum) / 2
    frequency = np.exp(math.log(minimum * maximum) / 2 + halfwidth * nodes)
    return frequency, halfwidth * weights * frequency


def build_matrix(basis, soft_order, seed_order):
    soft, soft_weights = frequency_nodes(soft_order, basis.minimum, basis.maximum / 2)
    extra, extra_weights = special.roots_laguerre(seed_order)
    full, local = np.zeros_like(basis.mass), np.zeros_like(basis.mass)
    discarded_weight, retained_weight = 0., 0.
    maximum_null = 0.
    for soft_frequency, soft_measure in zip(soft, soft_weights):
        seed = 2 * soft_frequency + extra
        hard = seed - soft_frequency
        density = seed**4 * gould(soft_frequency / seed) * np.exp(-2 * soft_frequency)
        density /= ((-np.expm1(-seed)) * (-np.expm1(-hard))
                    * (-np.expm1(-soft_frequency)) * soft_frequency * I3 * I4)
        weights = soft_measure * extra_weights * density
        inside = seed <= basis.maximum
        discarded_weight += float(weights[~inside].sum())
        retained_weight += float(weights[inside].sum())
        if not np.any(inside):
            continue
        seed, hard, weights = seed[inside], hard[inside], weights[inside]
        soft_values = basis.evaluate(np.array([soft_frequency]))[0]
        delta = soft_values + basis.evaluate(hard) - basis.evaluate(seed)
        delta[:, 0] = 1 / basis.norms[0]
        delta[:, 1] = -basis.mean / basis.norms[1]
        maximum_null = max(maximum_null, float(np.max(abs(delta @ basis.temperature))))
        full += (delta.T * weights) @ delta
        local += float(weights.sum()) * np.outer(soft_values, soft_values)
    return full, local, dict(maximum_event_temperature_null=maximum_null,
                             unweighted_discarded_rate_fraction=discarded_weight / retained_weight)


def soft_slope_row(basis, order=192):
    nodes, weights = special.roots_laguerre(order)
    inside = nodes <= basis.maximum
    nodes, weights = nodes[inside], weights[inside]
    weighted = weights * nodes**4 / (-np.expm1(-nodes))**2 / I4
    return weighted @ basis.derivative(nodes)


class NonlocalEmission(DerivedEmission):
    def __init__(self, basis, background, mode, matrix_folder):
        super().__init__(basis, background, mode in ['local-derived', 'nonlocal-soft-gaunt'])
        self.mode = mode
        self.matrix_folder = Path(matrix_folder)
        with np.load(self.matrix_folder / 'matrix.npz') as saved:
            self.nonlocal_matrix = saved['nonlocal_matrix'].copy()
        self.inputs.extend([self.matrix_folder / 'matrix.npz', self.matrix_folder / 'status.json'])

    def at(self, theta, variant):
        original = super().at(theta, variant)
        if variant not in ['dc', 'dcbr', 'dcbrnr']:
            return original
        inverse = 1 / (1 + 14.16 * theta)
        if self.mode == 'local-derived':
            return original
        if self.mode in ['local-leading', 'nonlocal-leading']:
            original += integrated_dc.DC_CONSTANT * theta**2 * (1 - inverse) * self.matrices['dc']
            factor = 1.
        elif self.mode == 'nonlocal-soft-gaunt':
            coordinate = math.log(theta)
            factor = float(self.gaunt_interpolator(coordinate))
            if not np.isfinite(factor):
                raise ValueError('Gaunt extrapolation forbidden')
        else:
            raise ValueError(self.mode)
        if self.mode.startswith('nonlocal'):
            original += integrated_dc.DC_CONSTANT * theta**2 * factor * (self.nonlocal_matrix - self.matrices['dc'])
        return original
