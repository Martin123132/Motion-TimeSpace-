from functools import lru_cache

import numpy as numerical

from sbp4_compatible_second_operator_20260909 import gram_parts, remainder_action


@lru_cache(maxsize=8)
def unit_gram_template(count):
    return gram_parts(count, numerical.ones(count))


def signed_remainder_action(values, coefficient, spacing):
    count = coefficient.size
    if coefficient.shape != (count,) or values.shape[-1] != count or spacing <= 0:
        raise ValueError("Invalid signed Gram dimensions")
    if not numerical.all(numerical.isfinite(coefficient)):
        raise ValueError("Nonfinite Gram coefficient")
    margin, adjacent, extras = unit_gram_template(count)
    indices = numerical.arange(count)
    size = count - 3
    difference = numerical.diff(values, n=3, axis=-1)
    weighted = margin * numerical.interp(numerical.arange(size) + 1.5, indices, coefficient) * difference
    signed_edges = adjacent * numerical.interp(numerical.arange(size - 1) + 2, indices, coefficient)
    orientations = numerical.sign(adjacent)
    coupled = difference[..., :-1] + orientations * difference[..., 1:]
    weighted[..., :-1] += orientations * signed_edges * coupled
    weighted[..., 1:] += signed_edges * coupled
    for first, second, unit_weight in extras:
        signed_weight = unit_weight * float(numerical.interp((first + second) / 2 + 1.5, indices, coefficient))
        orientation = numerical.sign(unit_weight)
        coupled = difference[..., first] + orientation * difference[..., second]
        weighted[..., first] += orientation * signed_weight * coupled
        weighted[..., second] += signed_weight * coupled
    result = numerical.zeros_like(values)
    for offset, factor in enumerate([-1, 3, -3, 1]):
        result[..., offset:offset + weighted.shape[-1]] += factor * weighted
    return result / spacing


def restoring_coordinate_source(scalar, radii, current, weights, spacing):
    coefficient = radii**2 * current["c"]
    if numerical.any(coefficient <= 0) or numerical.any(current["alpha"] <= 0):
        raise ValueError("Restoring branch requires positive c and alpha")
    parts = gram_parts(radii.size, coefficient)
    return -remainder_action(scalar, parts) / (spacing * weights * radii**2 * current["alpha"])


def restoring_time_coefficients(scalar, coefficient, spacing):
    if scalar.shape != coefficient.shape or scalar.ndim != 2 or scalar.shape[0] != 3:
        raise ValueError("Need normalized time coefficients through degree2")
    if numerical.any(coefficient[0] <= 0):
        raise ValueError("Nonpositive leading Gram coefficient")
    result = numerical.zeros_like(scalar)
    for degree in range(3):
        for index in range(degree + 1):
            result[degree] += signed_remainder_action(scalar[degree - index], coefficient[index], spacing)
    return result
