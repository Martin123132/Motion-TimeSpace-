from functools import lru_cache
from control_common import *


@lru_cache(maxsize=16)
def gauss_rule(order):
    nodes, weights = np.polynomial.legendre.leggauss(order)
    nodes.flags.writeable = weights.flags.writeable = False
    return nodes, weights


class PanelRule:
    def __init__(self, maximum_log_width=.5):
        assert maximum_log_width > 0
        self.maximum_log_width = maximum_log_width

    def __call__(self, order, lower, upper):
        if not 0 < lower < upper:
            raise ValueError('Positive ordered energy interval required')
        logarithm = math.log(upper / lower)
        count = max(1, math.ceil(logarithm / self.maximum_log_width))
        edges = np.linspace(math.log(lower), math.log(upper), count + 1)
        middle, halfwidth = .5 * (edges[1:] + edges[:-1]), .5 * np.diff(edges)
        nodes, weights = gauss_rule(order)
        values = np.exp(middle[:, None] + halfwidth[:, None] * nodes)
        measure = halfwidth[:, None] * weights * values
        return values.ravel(), measure.ravel()
