from common import *
from adjoint_operator import relative
import numpy as np


def physical_sources(system, reference, source_channels):
    names = reference["value_names"].tolist()
    values = {name: reference["values"][:, names.index(name)] for name in ("Q", "Pi")}
    grid, hubble = reference["efold"], reference["H"]
    alpha = reference["diagnostics"][:, 6]
    enthalpy = reference["diagnostics"][:, 2]
    quadrature = reference["diagnostics"][:, 3]
    rates = reference["rates"]
    wave = system.wave
    momentum = 3 * hubble * values["Q"] / (2 * wave**3)
    shear = values["Pi"] / wave**2
    lapse = momentum + shear
    gravity = 3 * hubble * enthalpy / (2 * wave**2)
    gravity_rate = hubble * system.background_spline(grid, 1)[:, 1]
    poisson_rate_gr = -rates[:, 0] / (2 * wave**2) + gravity_rate * alpha + gravity * rates[:, 2] / wave**2
    denominator = 1 + 3 * quadrature / (2 * wave**2)
    temporal = np.column_stack([3 * (rates[:, 4] - poisson_rate_gr) / (wave * denominator), 3 * rates[:, 4] / wave])
    mixing = np.column_stack([-3 * (hubble + gravity) / (wave * denominator), -3 * hubble / wave])
    predicted = np.stack([np.tile(lapse[:, None], (1, 2)), temporal + mixing * lapse[:, None]], axis=2)
    errors = {branch + "_" + name: relative(predicted[:, index, channel] - source_channels[:, index, channel], source_channels[:, index, channel])
              for index, branch in enumerate(("poisson-spatial", "newton-dust-force"))
              for channel, name in enumerate(("lapse", "expansion"))}
    require(max(errors.values()) < ALGEBRA, "physical omitted-source decomposition")
    return dict(momentum=momentum, shear=shear, temporal=temporal, mixing=mixing, predicted_channels=predicted), errors

