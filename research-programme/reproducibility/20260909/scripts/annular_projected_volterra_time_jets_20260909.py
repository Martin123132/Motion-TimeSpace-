import math

import numpy as numerical

from annular_correction_time_jets_20260909 import constant, multiply
from annular_coupled_current_time_jets_20260909 import CoupledCurrentTimeJets


def integrate_source_time_coefficients(coefficient, forcing, spacing):
    if coefficient.shape != forcing.shape or coefficient.ndim != 2 or coefficient.shape[0] != 3 or spacing <= 0:
        raise ValueError("Need normalized time coefficients through degree2")
    argument = -spacing * (coefficient[:, :-1] + coefficient[:, 1:]) / 2
    if numerical.max(numerical.abs(argument[0])) >= 0.09:
        raise ValueError("Time-jet replay is only qualified inside the small-argument moment branch")
    first, weighted = numerical.zeros_like(argument), numerical.zeros_like(argument)
    power = constant(numerical.ones(argument.shape[-1]))
    for degree in range(13):
        first += power / (math.factorial(degree) * (degree + 1))
        weighted += power / (math.factorial(degree) * (degree + 2))
        power = multiply(power, argument)
    leading = numerical.exp(argument[0])
    propagation = numerical.stack([leading, leading * argument[1], leading * (argument[2] + argument[1]**2 / 2)])
    left, right = spacing * (first - weighted), spacing * weighted
    result = numerical.zeros_like(forcing)
    for position in range(forcing.shape[-1] - 2, -1, -1):
        result[:, position] = multiply(propagation[:, position], result[:, position + 1]) - multiply(left[:, position], forcing[:, position]) - multiply(right[:, position], forcing[:, position + 1])
    if not numerical.all(numerical.isfinite(result)):
        raise ValueError("Nonfinite differentiated Volterra source")
    return result


class ProjectedVolterraTimeJets(CoupledCurrentTimeJets):
    def numerical_source(self, current, values, velocity):
        unused_centered, coordinate, raw = super().numerical_source(current, values, velocity)
        gradient = current["old_gradient"]
        forcing = multiply(gradient[:, 1], coordinate[:, 1]) + multiply(gradient[:, 3], coordinate[:, 3])
        complete = coordinate.copy()
        complete[:, 2] = integrate_source_time_coefficients(gradient[:, 2], forcing, self.spacing)
        transformed = numerical.stack([complete[:, 0], numerical.zeros_like(velocity), multiply(current["alpha"], complete[:, 1]) + multiply(current["h_mu"], complete[:, 2]) + multiply(current["h_delta"], complete[:, 3]), complete[:, 2], complete[:, 3]], axis=1)
        return transformed, complete, raw
