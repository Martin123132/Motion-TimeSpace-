import hashlib
import json
from fractions import Fraction
from pathlib import Path

import numpy as numerical

from sbp4_derived_operator_20260909 import derivative


DIRECTORY = Path(__file__).resolve().parents[1] / "source-intake/navier-stokes/20260909/sbp4-second-derivative-derived"
OWNER = json.loads((DIRECTORY / "status.json").read_text())
PAYLOAD = (DIRECTORY / "coefficients.json").read_bytes()
if OWNER["state"] != "complete" or OWNER["passed"] != 18 or not (DIRECTORY / "COMPLETE").is_file() or hashlib.sha256(PAYLOAD).hexdigest() != OWNER["coefficient_sha256"]:
    raise ValueError("Unverified compatible second derivative")
DATA = json.loads(PAYLOAD)
LEFT = numerical.array([[float(Fraction(value)) for value in row] for row in DATA["left_second"]])
SURFACE = numerical.array([float(Fraction(value)) for value in DATA["left_surface"]])
LEFT_NORM = numerical.array([float(Fraction(value)) for value in DATA["norm_weights"]])


def norm_weights(count):
    if count < 17:
        raise ValueError("Disjoint compatible closures require at least 17 nodes")
    values = numerical.ones(count)
    values[:4], values[-4:] = LEFT_NORM, LEFT_NORM[::-1]
    return values


def surface_derivative(values, spacing):
    return numerical.stack([numerical.einsum("j,...j->...", SURFACE, values[..., :4]), -numerical.einsum("j,...j->...", SURFACE, values[..., -1:-5:-1])], axis=-1) / spacing


def second_derivative(values, spacing):
    norm_weights(values.shape[-1])
    result = numerical.empty_like(values)
    result[..., 4:-4] = (-values[..., 2:-6] + 16 * values[..., 3:-5] - 30 * values[..., 4:-4] + 16 * values[..., 5:-3] - values[..., 6:-2]) / (12 * spacing**2)
    result[..., :4] = numerical.einsum("ij,...j->...i", LEFT, values[..., :6]) / spacing**2
    result[..., -4:] = numerical.einsum("ij,...j->...i", LEFT, values[..., -1:-7:-1])[..., ::-1] / spacing**2
    return result


def gram_parts(count, coefficient):
    if coefficient.shape != (count,) or numerical.any(coefficient <= 0):
        raise ValueError("Positive one-dimensional principal coefficient required")
    norm_weights(count)
    size = count - 3
    diagonal = numerical.full(size, 5 / 72)
    diagonal[:3] = [59097 / 573104, 1825 / 25284, 491 / 7056]
    diagonal[-3:] = diagonal[:3][::-1]
    adjacent = numerical.full(size - 1, -1 / 144)
    adjacent[:2] = [253 / 50568, -3 / 392]
    adjacent[-2:] = adjacent[:2][::-1]
    extra_left, extra_right = (0, 2, -1 / 392), (size - 3, size - 1, -1 / 392)
    margins = diagonal.copy()
    margins[:-1] -= numerical.abs(adjacent)
    margins[1:] -= numerical.abs(adjacent)
    for first, second, weight in [extra_left, extra_right]:
        margins[first] -= abs(weight)
        margins[second] -= abs(weight)
    if numerical.any(margins <= 0):
        raise ValueError("Lost positive Gram decomposition")
    centers = numerical.arange(size) + 1.5
    weighted_margin = margins * numerical.interp(centers, numerical.arange(count), coefficient)
    edge_coefficient = numerical.interp(numerical.arange(size - 1) + 2.0, numerical.arange(count), coefficient)
    extras = [(first, second, weight * float(numerical.interp((first + second) / 2 + 1.5, numerical.arange(count), coefficient))) for first, second, weight in [extra_left, extra_right]]
    return weighted_margin, adjacent * edge_coefficient, extras


def gram_action(values, parts):
    margin, adjacent, extras = parts
    result = margin * values
    coupled = values[..., :-1] + numerical.sign(adjacent) * values[..., 1:]
    result[..., :-1] += numerical.abs(adjacent) * coupled
    result[..., 1:] += adjacent * coupled
    for first, second, weight in extras:
        coupled = values[..., first] + numerical.sign(weight) * values[..., second]
        result[..., first] += abs(weight) * coupled
        result[..., second] += weight * coupled
    return result


def remainder_action(values, parts):
    difference = numerical.diff(values, n=3, axis=-1)
    weighted = gram_action(difference, parts)
    result = numerical.zeros_like(values)
    for offset, coefficient in enumerate([-1, 3, -3, 1]):
        result[..., offset:offset + weighted.shape[-1]] += coefficient * weighted
    return result


def flux_second(values, coefficient, spacing, parts=None):
    norm = norm_weights(values.shape[-1])
    if parts is None:
        parts = gram_parts(values.shape[-1], coefficient)
    gradient = derivative(values, spacing)
    result = derivative(coefficient * gradient, spacing) - remainder_action(values, parts) / (spacing**2 * norm)
    difference = surface_derivative(values, spacing) - gradient[..., [0, -1]]
    result[..., 0] -= coefficient[0] * difference[..., 0] / (spacing * norm[0])
    result[..., -1] += coefficient[-1] * difference[..., 1] / (spacing * norm[-1])
    return result

