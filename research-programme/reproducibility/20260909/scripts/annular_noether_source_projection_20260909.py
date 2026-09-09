import numpy as numerical
from scipy.linalg import solve_banded

from annular_noether_completion_20260909 import complete_mass


def transpose_band(band):
    result = numerical.zeros_like(band)
    count = band.shape[1]
    for offset in range(-3, 4):
        columns = numerical.arange(max(0, -offset), min(count, count - offset))
        rows = columns + offset
        result[3 - offset, rows] = band[3 + offset, columns]
    return result


def project_and_complete(sources, gradient, band, outer_derivative, energy_weights):
    anchored = band.copy()
    anchored[3] -= gradient[2]
    anchored[3, -1] = 1
    full_outer = outer_derivative.copy()
    full_outer[-1] -= gradient[2, -1]
    normal = solve_banded((3, 3), transpose_band(anchored), full_outer, check_finite=False)
    normal[-1] = -1
    normal /= numerical.max(numerical.abs(normal))
    covector = numerical.stack([normal * gradient[1], normal * gradient[3]])
    denominator = float(numerical.sum(covector**2 / energy_weights))
    original = sources[:, [1, 3]]
    mismatch = numerical.einsum("in,bin->b", covector, original)
    projected = sources.copy()
    if denominator > 0:
        projected[:, [1, 3]] -= mismatch[:, None, None] * covector[None, :, :] / (denominator * energy_weights)
    elif numerical.max(numerical.abs(mismatch)) != 0:
        raise ValueError("Incompatible source without an adjustable scalar/lapse direction")
    completed = complete_mass(projected, gradient, band)
    return completed
