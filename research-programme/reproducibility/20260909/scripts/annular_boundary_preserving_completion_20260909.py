import numpy as numerical
from scipy.linalg import solve_banded

from annular_noether_completion_20260909 import complete_mass
from annular_noether_source_projection_20260909 import transpose_band


def project_interior_scalar_and_complete(sources, gradient, band, outer_derivative, scalar_energy_weight):
    anchored = band.copy()
    anchored[3] -= gradient[2]
    anchored[3, -1] = 1
    full_outer = outer_derivative.copy()
    full_outer[-1] -= gradient[2, -1]
    normal = solve_banded((3, 3), transpose_band(anchored), full_outer, check_finite=False)
    normal[-1] = -1
    normal /= numerical.max(numerical.abs(normal))
    full_covector = normal * gradient[1]
    covector = full_covector.copy()
    covector[[0, -1]] = 0
    denominator = float(numerical.sum(covector**2 / scalar_energy_weight))
    mismatch = numerical.sum(normal * (gradient[1] * sources[:, 1] + gradient[3] * sources[:, 3]), axis=-1)
    projected = sources.copy()
    if denominator > 0:
        projected[:, 1] -= mismatch[:, None] * covector / (denominator * scalar_energy_weight)
    elif numerical.max(numerical.abs(mismatch)) != 0:
        raise ValueError("Interior scalar source cannot satisfy the boundary-fixed compatibility condition")
    return complete_mass(projected, gradient, band)

