from derive_annular_source_gravity_20260914 import EvidenceRun
from annular_live_compensation_derivative_20260928 import CompensationLoads as CoefficientCompensationLoads
import numpy as np


class CompensationLoads(CoefficientCompensationLoads):
    def source(self, labels):
        values = list(super().source(labels))
        cardinal = self.material.interpolation(np.atleast_1d(labels))
        values[0] = cardinal @ self.material.coordinates[:, -1]
        values[3] = cardinal @ self.direction[:, -1]
        values[5] = cardinal @ self.loads.rates[:, -1]
        values[7] = cardinal @ self.velocity_direction[:, -1]
        if np.ndim(labels) == 0:
            values = [np.asarray(value).item() for value in values]
        return tuple(values)
