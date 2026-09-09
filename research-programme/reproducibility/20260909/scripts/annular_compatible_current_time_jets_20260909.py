import numpy as numerical

from annular_compatible_current_restoring_20260909 import restoring_time_coefficients
from annular_correction_time_jets_20260909 import divide, multiply
from annular_projected_volterra_time_jets_20260909 import integrate_source_time_coefficients
from annular_raw_volterra_time_jets_20260909 import RawVolterraTimeJets


class CompatibleCurrentTimeJets(RawVolterraTimeJets):
    def numerical_source(self, current, values, velocity):
        unused_source, unused_complete, raw = super().numerical_source(current, values, velocity)
        restoring = restoring_time_coefficients(values[:, 0], self.radii**2 * current["c"], self.spacing)
        raw[:, 1] -= divide(restoring, current["alpha"]) / (self.weights * self.radii**2)
        gradient = current["old_gradient"]
        forcing = multiply(gradient[:, 1], raw[:, 1]) + multiply(gradient[:, 3], raw[:, 3])
        complete = raw.copy()
        complete[:, 2] = integrate_source_time_coefficients(gradient[:, 2], forcing, self.spacing)
        transformed = numerical.stack([complete[:, 0], numerical.zeros_like(velocity), multiply(current["alpha"], complete[:, 1]) + multiply(current["h_mu"], complete[:, 2]) + multiply(current["h_delta"], complete[:, 3]), complete[:, 2], complete[:, 3]], axis=1)
        return transformed, complete, raw
