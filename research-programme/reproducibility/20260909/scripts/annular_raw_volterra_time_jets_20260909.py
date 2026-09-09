import numpy as numerical

from annular_correction_time_jets_20260909 import divide, multiply
from annular_coupled_current_time_jets_20260909 import CoupledCurrentTimeJets, square_root
from annular_projected_volterra_time_jets_20260909 import integrate_source_time_coefficients


class RawVolterraTimeJets(CoupledCurrentTimeJets):
    def numerical_source(self, current, values, velocity):
        fixed_velocity = velocity - multiply(current["q0"], values[:, 4])
        fixed_gradient = values[:, 1] - self.evaluator.sigma * multiply(current["q0"], values[:, 4])
        flux = multiply(current["B"], fixed_velocity) + multiply(current["c"], fixed_gradient)
        impedance = square_root(multiply(current["P"], current["Q"]))
        raw = numerical.zeros((3, 4, self.radii.size))
        for endpoint, orientation in [(0, 1), (-1, -1)]:
            raw[:, 1, endpoint] = divide(orientation * flux[:, endpoint] - multiply(impedance, fixed_velocity)[:, endpoint], current["alpha"][:, endpoint]) / self.weights[endpoint]
        raw[:, 3, -1] = -values[:, 4, -1] / (self.evaluator.sigma * self.weights[-1])
        gradient = current["old_gradient"]
        forcing = multiply(gradient[:, 1], raw[:, 1]) + multiply(gradient[:, 3], raw[:, 3])
        complete = raw.copy()
        complete[:, 2] = integrate_source_time_coefficients(gradient[:, 2], forcing, self.spacing)
        transformed = numerical.stack([complete[:, 0], numerical.zeros_like(velocity), multiply(current["alpha"], complete[:, 1]) + multiply(current["h_mu"], complete[:, 2]) + multiply(current["h_delta"], complete[:, 3]), complete[:, 2], complete[:, 3]], axis=1)
        return transformed, complete, raw
