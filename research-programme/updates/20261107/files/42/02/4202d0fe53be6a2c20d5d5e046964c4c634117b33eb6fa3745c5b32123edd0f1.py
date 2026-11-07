from common import *
from math import comb
import numpy as np
from scipy.linalg import expm
import sympy as sp

NODES = np.linspace(0., 1., 6)
VANDERMONDE = np.array([[comb(5, degree) * node**degree * (1 - node)**(5 - degree) for degree in range(6)] for node in NODES])
INVERSE = np.linalg.inv(VANDERMONDE)


def controls(spline, left, right):
    locations = left[:, None] + (right - left)[:, None] * NODES
    values = spline(locations)
    return np.einsum("ij,bj...->bi...", INVERSE, values)


def norm_last_two(values):
    return np.sqrt(np.sum(values**2, axis=(-2, -1)))


def spectral_cross(values):
    gram = values @ np.swapaxes(values, -1, -2)
    return np.sqrt(np.maximum(0., .5 * (gram[..., 0, 0] + gram[..., 1, 1]
                       + np.sqrt((gram[..., 0, 0] - gram[..., 1, 1])**2 + 4 * gram[..., 0, 1]**2))))


def comparison_envelope(matrices, forcing, heavy, rest):
    remainder = matrices[..., rest[:, None], rest]
    symmetric = (remainder + np.swapaxes(remainder, -1, -2)) / 2
    rest_rate = np.maximum(-.5, np.linalg.eigvalsh(symmetric)[..., -1])
    if len(heavy):
        block = matrices[..., heavy[:, None], heavy]
        symmetric_heavy = (block + np.swapaxes(block, -1, -2)) / 2
        heavy_rate = np.linalg.eigvalsh(symmetric_heavy)[..., -1]
        to_heavy = spectral_cross(matrices[..., heavy[:, None], rest])
        to_rest = spectral_cross(np.swapaxes(matrices[..., rest[:, None], heavy], -1, -2))
        force_heavy = np.linalg.norm(forcing[..., heavy], axis=-1)
    else:
        heavy_rate = np.zeros_like(rest_rate)
        to_heavy = np.zeros_like(rest_rate)
        to_rest = np.zeros_like(rest_rate)
        force_heavy = np.zeros_like(rest_rate)
    force_rest = np.linalg.norm(forcing[..., rest], axis=-1)
    padding = 64 * np.finfo(float).eps * np.max(norm_last_two(matrices), axis=1)
    matrix = np.stack([heavy_rate, to_heavy, to_rest, rest_rate], axis=-1).max(axis=1).reshape(-1, 2, 2)
    if len(heavy):
        matrix += padding[:, None, None]
    else:
        matrix[:, 1, 1] += padding
    source = np.stack([force_heavy, force_rest], axis=-1).max(axis=1)
    source *= 1 + 64 * np.finfo(float).eps
    return matrix, source, padding


def propagate(grid, matrices, forcing, initial, group=1, subdivide=1):
    state = np.asarray(initial).copy()
    homogeneous = np.eye(2)
    for begin in range(0, len(matrices), group):
        if begin % 256 == 0:
            guard()
        end = min(begin + group, len(matrices))
        matrix = np.max(matrices[begin:end], axis=0)
        source = np.max(forcing[begin:end], axis=0)
        step = float(grid[end] - grid[begin]) / subdivide
        augmented = np.zeros((3, 3))
        augmented[:2, :2] = matrix
        augmented[:2, 2] = source
        transition = expm(augmented * step)
        require(np.isfinite(transition).all() and np.min(transition) >= -ALGEBRA, "positive finite comparison transition")
        for division in range(subdivide):
            state = transition[:2, :2] @ state + transition[:2, 2]
            homogeneous = transition[:2, :2] @ homogeneous
    return state, homogeneous


def symbolic():
    degree = sp.symbols("l", integer=True, positive=True)
    weight = lambda value: (2 * value + 1) * (value + 1) * (value + 2) / (value * (value - 1))
    upper = (degree + 3) * (degree - 1) / ((degree + 1) * (2 * degree + 1))
    lower_next = (degree + 1) / (2 * degree + 3)
    radiation, baryon, opacity, velocity, heat = sp.symbols("Rg Rb opacity v q", positive=True)
    drag = radiation * opacity * (velocity * (heat - sp.Rational(4, 3) * velocity)
                                  + sp.Rational(3, 4) * heat * (sp.Rational(4, 3) * velocity - heat))
    checks = dict(polarization_stream=sp.simplify(weight(degree) * upper - weight(degree + 1) * lower_next),
                  photon_baryon_drag=sp.simplify(drag + sp.Rational(4, 3) * opacity * radiation * (velocity - sp.Rational(3, 4) * heat)**2),
                  polarization_collision=sp.simplify(5 * sp.Rational(3, 5) - 30 * sp.Rational(1, 10)))
    require(all(value == 0 for value in checks.values()), "derived matter energy identities")
    return {name: str(value) for name, value in checks.items()}


def unit_checks():
    coefficients = np.array([1., -.2, .8, -.9, 2., -.4])
    samples = VANDERMONDE @ coefficients
    require(np.max(abs(INVERSE @ samples - coefficients)) < 1e-12, "Bernstein control recovery")
    matrix = np.array([[.3, .7], [.2, -.4]])
    source = np.array([.1, .3])
    grid = np.linspace(0., .4, 9)
    initial = np.array([.2, .4])
    fine, propagator = propagate(grid, np.tile(matrix, (8, 1, 1)), np.tile(source, (8, 1)), initial)
    half, _ = propagate(grid, np.tile(matrix, (8, 1, 1)), np.tile(source, (8, 1)), initial, subdivide=2)
    augmented = np.zeros((3, 3))
    augmented[:2, :2], augmented[:2, 2] = matrix, source
    exact = expm(.4 * augmented) @ np.r_[initial, 1.]
    require(np.max(abs(fine - exact[:2])) < 1e-12 and np.max(abs(fine - half)) < 1e-12, "affine comparison integral")
    return dict(passed=True, controls_error=float(np.max(abs(INVERSE @ samples - coefficients))),
                comparison_error=float(np.max(abs(fine - exact[:2]))), symbolic=symbolic())

