from common import *
from adjoint_operator import open_owned, relative, sup
from compact_adjoint import CompactAdjoint
from scipy.interpolate import make_interp_spline
import numpy as np


class MetricPrimitive:
    def __init__(self, system, reference):
        self.system = system
        self.grid = reference["efold"]
        self.quadrature = make_interp_spline(self.grid, reference["diagnostics"][:, 3], k=5)
        self.size = len(system.core)

    def direct_quadrature(self, efold):
        point = self.system.context["point"](efold)
        terms, metadata = self.system.context["stress"](point[11], self.system.zero_native)
        return float(terms[:, 5].sum() - terms[4, 5] + metadata[3])

    def vector(self, efold, factor, direct=False):
        system = self.system
        point = system.context["point"](efold)
        quadrature = self.direct_quadrature(efold) if direct else float(self.quadrature(efold))
        denominator = 1 + 3 * factor * quadrature / (2 * system.wave**2)
        denominator_rate = 3 * factor * float(self.quadrature(efold, 1)) / (2 * system.wave**2)
        expansion = system.metric_kernels(efold)[0]
        expansion_rate = np.zeros(system.context["dimension"])
        expansion_rate[system.owner.scalar_positions[1]] = -system.wave * point[6]
        if system.model == "heavy":
            expansion_rate[system.owner.scalar_positions[3]] = -system.wave * point[8]
        normal = 3 / (system.wave * denominator * system.units[:self.size])
        vector = normal * expansion[system.core]
        rate = normal * (expansion_rate[system.core] - expansion[system.core] * denominator_rate / denominator)
        vector[system.alpha_slot], rate[system.alpha_slot] = 0., 0.
        if system.model == "heavy":
            phase, mu = system.owner.phase(efold)
            omega = point[10] * system.background["masses"][1]
            coefficient = -3j * point[10] * np.exp(1j * phase) / (denominator * np.sqrt(omega))
            value = coefficient * point[3]
            derivative = coefficient * (point[8] + (.5 + 1j * mu - denominator_rate / denominator) * point[3])
            vector[system.slots] = np.array([value.real, value.imag]) / system.units[system.slots]
            rate[system.slots] = np.array([derivative.real, derivative.imag]) / system.units[system.slots]
        return vector, rate, denominator


def primitive_sources(system, reference, physical):
    names = reference["value_names"].tolist()
    values = {name: reference["values"][:, names.index(name)] for name in ("Phi", "D", "Q")}
    grid, hubble = reference["efold"], reference["H"]
    wave = system.wave
    derivatives = system.background_spline(grid, 1)
    enthalpy, alpha = reference["diagnostics"][:, 2], reference["diagnostics"][:, 6]
    gravity = 3 * hubble * enthalpy / (2 * wave**2)
    synchronous_current = reference["terms"][:, :, 1].sum(axis=1)
    synchronous_rate = reference["terms"][:, :, 4].sum(axis=1)
    alpha_rate = reference["rates"][:, 2] / (wave**2 * hubble)
    momentum = 3 * hubble * values["Q"] / (2 * wave**3)
    momentum_rate = 3 * (derivatives[:, 0] * synchronous_current + synchronous_rate) / (2 * wave**3)
    momentum_rate += derivatives[:, 1] * alpha + gravity * alpha_rate
    poisson = -values["D"] / (2 * wave**2)
    primitive = np.column_stack([-momentum, values["Phi"]])
    rate = np.column_stack([-momentum_rate, reference["rates"][:, 4] / hubble])
    denominator = np.column_stack([1 + 3 * reference["diagnostics"][:, 3] / (2 * wave**2), np.ones(len(grid))])
    predicted = 3 * hubble[:, None] * rate / (wave * denominator)
    identities = dict(constraint_primitive=relative(values["Phi"] - poisson + momentum, values["Phi"]),
                      prospective_temporal=relative(predicted - physical["temporal"], physical["temporal"]),
                      source_momentum=relative(momentum - physical["momentum"], momentum))
    require(max(identities.values()) < ALGEBRA, "physical primitive identity")
    return dict(primitive=primitive, primitive_rate=rate, denominator=denominator), identities

