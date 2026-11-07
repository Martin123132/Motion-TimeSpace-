from rectangular_weak import *


def logarithmic_rule(order, lower, upper):
    if not 0 < lower < upper:
        raise ValueError('Logarithmic matched quadrature requires a positive ordered interval')
    nodes, weights = np.polynomial.legendre.leggauss(order)
    halfwidth = .5 * math.log(upper / lower)
    values = np.exp(.5 * math.log(upper * lower) + halfwidth * nodes)
    return values, halfwidth * weights * values


class LogRectangular(Rectangular):
    @contextmanager
    def real_context(self):
        with super().real_context():
            saved = weak.quadrature
            weak.quadrature = logarithmic_rule
            try:
                yield
            finally:
                weak.quadrature = saved
