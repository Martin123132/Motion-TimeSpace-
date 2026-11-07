from adjoint_operator import AdjointOperator
from scipy.interpolate import make_interp_spline
import numpy as np


class SparseCoefficientSpline:
    def __init__(self, grid, matrices):
        self.shape = matrices.shape[1:]
        self.rows, self.columns = np.nonzero(np.any(matrices != 0., axis=0))
        self.spline = make_interp_spline(grid, matrices[:, self.rows, self.columns], k=5, axis=0)

    def __call__(self, efold):
        result = np.zeros(self.shape)
        result[self.rows, self.columns] = self.spline(efold)
        return result


class CompactAdjoint(AdjointOperator):
    def __init__(self, packet):
        self.size = int(packet["core_size"])
        self.dimension = len(packet["units"])
        self.units = packet["units"]
        self.wave = float(packet["wave"])
        self.quadrupoles = packet["quadrupoles"]
        self.degree = np.arange(3, 193)
        self.lower = self.wave * self.degree / (2 * self.degree + 1)
        self.upper = -self.wave * (self.degree + 1) / (2 * self.degree + 1)
        self.upper[-1] = 0.
        self.splines = {name: make_interp_spline(packet["efold"], packet[name], k=5, axis=0)
                        for name in ("injection", "channels", "rows", "speeds")}
        self.splines["base"] = SparseCoefficientSpline(packet["efold"], packet["base"])

