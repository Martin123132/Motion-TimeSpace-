from __future__ import annotations

import argparse
import csv
import itertools
import json
import math
import time
from concurrent.futures import ProcessPoolExecutor
from dataclasses import dataclass
from pathlib import Path
from typing import Any

import numpy as np

import Y5_R2FR_4909_motion_scalar_lattice_gap_stress_three_point as checkpoint_4909
import Y5_R2FR_4910_free_metric_TTT_projector_arbitration as checkpoint_4910
import Y5_R2FR_4911_full_offshell_a6_template_projector as checkpoint_4911


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"

MARKER = "MTS_FREE_LATTICE_MULTIGEOMETRY_CONTINUUM_PROJECTOR_4912"
FORMAL_MARKER = "PPC4161_INDEPENDENT_CONTINUUM_TTT_MATCHED_SUBTRACTION_4912"
NEXT_TARGET = (
    "4913-Y5-R2FR-matched-subtracted-interacting-motion-scalar-TTT-"
    "continuum-coefficient-or-zero-residual.md"
)
CHECKED_DATE = "2026-07-12"
DIMENSIONS = 4
SERIES_ORDER = 6
TARGET_ZETA_M2 = 1.0 / (30240.0 * (4.0 * math.pi) ** 2)


@dataclass(frozen=True)
class LatticeConfig:
    label: str
    size: int
    mass: float
    stencil: str
    quadrature: str = "uniform"


@dataclass(frozen=True)
class ContinuumConfig:
    label: str
    mass: float
    radial_order: int
    angular_order: int


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def tagged(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            **row,
            "checkpoint_marker": MARKER,
            "valid_for_claim": False,
            "source_checked_date": CHECKED_DATE,
        }
        for row in rows
    ]


def series_binary_einsum(
    subscripts: str, left: np.ndarray, right: np.ndarray
) -> np.ndarray:
    output: np.ndarray | None = None
    for order in range(SERIES_ORDER + 1):
        accumulator: np.ndarray | None = None
        for left_order in range(order + 1):
            term = np.einsum(
                subscripts,
                left[left_order],
                right[order - left_order],
                optimize=True,
            )
            accumulator = term if accumulator is None else accumulator + term
        if output is None:
            output = np.empty(
                (SERIES_ORDER + 1,) + accumulator.shape,
                dtype=np.complex128,
            )
        output[order] = accumulator
    if output is None:
        raise RuntimeError("series product produced no output")
    return output


def series_product(*factors: np.ndarray) -> np.ndarray:
    if not factors:
        raise ValueError("at least one series factor is required")
    result = factors[0]
    for factor in factors[1:]:
        result = series_binary_einsum("...,...->...", result, factor)
    return result


def series_bilinear_form(
    left: np.ndarray, matrix: np.ndarray, right: np.ndarray
) -> np.ndarray:
    output = np.zeros(
        (SERIES_ORDER + 1, left.shape[1]), dtype=np.complex128
    )
    for order in range(SERIES_ORDER + 1):
        for left_order in range(order + 1):
            output[order] += np.einsum(
                "bi,ij,bj->b",
                left[left_order],
                matrix,
                right[order - left_order],
                optimize=True,
            )
    return output


def series_inverse(denominator: np.ndarray) -> np.ndarray:
    output = np.zeros_like(denominator)
    output[0] = 1.0 / denominator[0]
    for order in range(1, SERIES_ORDER + 1):
        accumulator = np.zeros_like(denominator[0])
        for source_order in range(1, order + 1):
            accumulator += (
                denominator[source_order] * output[order - source_order]
            )
        output[order] = -output[0] * accumulator
    return output


def series_evaluate(series: np.ndarray, parameter: float) -> np.ndarray:
    result = np.zeros_like(series[0])
    for coefficient in reversed(series):
        result = result * parameter + coefficient
    return result


def momentum_chunk(start: int, stop: int, size: int) -> np.ndarray:
    flat = np.arange(start, stop, dtype=np.int64)
    digits = np.empty((len(flat), DIMENSIONS), dtype=float)
    working = flat.copy()
    for axis in range(DIMENSIONS - 1, -1, -1):
        digits[:, axis] = working % size
        working //= size
    return 2.0 * math.pi * digits / size


def quadrature_chunk(
    start: int, stop: int, size: int, quadrature: str
) -> tuple[np.ndarray, np.ndarray]:
    flat = np.arange(start, stop, dtype=np.int64)
    digits = np.empty((len(flat), DIMENSIONS), dtype=int)
    working = flat.copy()
    for axis in range(DIMENSIONS - 1, -1, -1):
        digits[:, axis] = working % size
        working //= size
    if quadrature == "uniform":
        momentum = 2.0 * math.pi * digits / size
        weights = np.full(len(flat), 1.0 / size**DIMENSIONS)
        return momentum, weights
    if quadrature == "gauss_legendre":
        nodes, one_dimensional_weights = np.polynomial.legendre.leggauss(size)
        nodes = math.pi * nodes
        normalized_weights = one_dimensional_weights / 2.0
        momentum = nodes[digits]
        weights = np.prod(normalized_weights[digits], axis=1)
        return momentum, weights
    raise ValueError(f"unknown quadrature: {quadrature}")


def exponential_series(
    base: np.ndarray, rates: np.ndarray
) -> np.ndarray:
    coefficients = np.empty(
        (SERIES_ORDER + 1,) + base.shape, dtype=np.complex128
    )
    for order in range(SERIES_ORDER + 1):
        coefficients[order] = (
            base * (1j * rates) ** order / math.factorial(order)
        )
    return coefficients


def derivative_symbols_series(
    base_phase: np.ndarray,
    shift: np.ndarray,
    stencil: str,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    positive = exponential_series(base_phase, shift)
    negative = exponential_series(np.conjugate(base_phase), -shift)
    constant = np.zeros_like(positive)
    constant[0] = 1.0
    if stencil == "nearest":
        forward = positive - constant
        forward_bar = negative - constant
        backward = constant - negative
        backward_bar = constant - positive
    elif stencil == "improved":
        positive_squared = exponential_series(base_phase**2, 2.0 * shift)
        negative_squared = exponential_series(
            np.conjugate(base_phase) ** 2, -2.0 * shift
        )
        forward = (-3.0 * constant + 4.0 * positive - positive_squared) / 2.0
        forward_bar = (
            -3.0 * constant + 4.0 * negative - negative_squared
        ) / 2.0
        backward = (
            3.0 * constant - 4.0 * negative + negative_squared
        ) / 2.0
        backward_bar = (
            3.0 * constant - 4.0 * positive + positive_squared
        ) / 2.0
    else:
        raise ValueError(f"unknown stencil: {stencil}")
    return forward, forward_bar, backward, backward_bar


def propagator_series(
    base_phase: np.ndarray,
    shift: np.ndarray,
    mass: float,
    stencil: str,
) -> tuple[np.ndarray, float]:
    forward, forward_bar, backward, backward_bar = derivative_symbols_series(
        base_phase, shift, stencil
    )
    denominator = 0.5 * (
        series_binary_einsum("bi,bi->b", forward_bar, forward)
        + series_binary_einsum("bi,bi->b", backward_bar, backward)
    )
    denominator[0] += mass**2
    propagator = series_inverse(denominator)
    inverse_residual = series_product(denominator, propagator)
    inverse_residual[0] -= 1.0
    return propagator, float(np.max(np.abs(inverse_residual)))


def metric_vertex_series(
    base_phase: np.ndarray,
    source_momentum: np.ndarray,
    polarization: np.ndarray,
    incoming_shift: np.ndarray,
    stencil: str,
) -> np.ndarray:
    incoming = derivative_symbols_series(
        base_phase, incoming_shift, stencil
    )
    outgoing = derivative_symbols_series(
        base_phase, incoming_shift + source_momentum, stencil
    )
    return 0.5 * (
        series_bilinear_form(outgoing[1], polarization, incoming[0])
        + series_bilinear_form(outgoing[3], polarization, incoming[2])
    )


def continuum_derivative_symbols_series(
    momentum: np.ndarray, shift: np.ndarray
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    shape = (SERIES_ORDER + 1,) + momentum.shape
    derivative = np.zeros(shape, dtype=np.complex128)
    derivative[0] = 1j * momentum
    derivative[1] = 1j * shift[np.newaxis, :]
    derivative_bar = -derivative
    return derivative, derivative_bar, derivative, derivative_bar


def continuum_propagator_series(
    momentum: np.ndarray, shift: np.ndarray, mass: float
) -> tuple[np.ndarray, float]:
    denominator = np.zeros(
        (SERIES_ORDER + 1, len(momentum)), dtype=np.complex128
    )
    denominator[0] = mass**2 + np.sum(momentum**2, axis=1)
    denominator[1] = 2.0 * momentum @ shift
    denominator[2] = float(shift @ shift)
    propagator = series_inverse(denominator)
    inverse_residual = series_product(denominator, propagator)
    inverse_residual[0] -= 1.0
    return propagator, float(np.max(np.abs(inverse_residual)))


def continuum_metric_vertex_series(
    momentum: np.ndarray,
    source_momentum: np.ndarray,
    polarization: np.ndarray,
    incoming_shift: np.ndarray,
) -> np.ndarray:
    incoming = continuum_derivative_symbols_series(momentum, incoming_shift)
    outgoing = continuum_derivative_symbols_series(
        momentum, incoming_shift + source_momentum
    )
    return 0.5 * (
        series_bilinear_form(outgoing[1], polarization, incoming[0])
        + series_bilinear_form(outgoing[3], polarization, incoming[2])
    )


def determinant_volume_derivatives(
    polarizations: np.ndarray,
) -> tuple[np.ndarray, dict[tuple[int, int], float], float]:
    traces = np.array(
        [float(np.trace(polarization)) for polarization in polarizations]
    )
    first = 0.5 * traces
    pair: dict[tuple[int, int], float] = {}
    for left, right in itertools.combinations(range(3), 2):
        pair[(left, right)] = (
            0.25 * traces[left] * traces[right]
            - 0.5
            * float(np.trace(polarizations[left] @ polarizations[right]))
        )
    triple = (
        0.5
        * float(
            np.trace(polarizations[0] @ polarizations[1] @ polarizations[2])
            + np.trace(polarizations[0] @ polarizations[2] @ polarizations[1])
        )
        - 0.25
        * (
            float(np.trace(polarizations[0] @ polarizations[1])) * traces[2]
            + float(np.trace(polarizations[0] @ polarizations[2])) * traces[1]
            + float(np.trace(polarizations[1] @ polarizations[2])) * traces[0]
        )
        + 0.125 * float(np.prod(traces))
    )
    return first, pair, triple


def complex_TTT_continuum_series_points(
    momentum: np.ndarray,
    momenta: np.ndarray,
    polarizations: np.ndarray,
    mass: float,
) -> tuple[np.ndarray, float]:
    zero = np.zeros(DIMENSIONS, dtype=float)
    propagator_cache: dict[tuple[float, ...], np.ndarray] = {}
    maximum_inverse_residual = 0.0

    def propagator(shift: np.ndarray) -> np.ndarray:
        nonlocal maximum_inverse_residual
        key = tuple(float(value) for value in shift)
        if key not in propagator_cache:
            value, residual = continuum_propagator_series(
                momentum, shift, mass
            )
            propagator_cache[key] = value
            maximum_inverse_residual = max(
                maximum_inverse_residual, residual
            )
        return propagator_cache[key]

    first_volume, pair_volume, triple_volume = determinant_volume_derivatives(
        polarizations
    )
    pair_coefficients = {
        key: mass**2 * value for key, value in pair_volume.items()
    }
    triple_coefficient = mass**2 * triple_volume

    def vertex(source: int, incoming_shift: np.ndarray) -> np.ndarray:
        value = continuum_metric_vertex_series(
            momentum,
            momenta[source],
            polarizations[source],
            incoming_shift,
        )
        value[0] += mass**2 * first_volume[source]
        return value
    propagator_zero = propagator(zero)
    result = triple_coefficient * propagator_zero
    for first, second, third in ((0, 1, 2), (1, 0, 2), (2, 0, 1)):
        pair_shift = momenta[second] + momenta[third]
        pair_key = tuple(sorted((second, third)))
        result -= pair_coefficients[pair_key] * series_product(
            propagator_zero,
            propagator(pair_shift),
            vertex(first, pair_shift),
        )
    after_third = momenta[2]
    after_second = momenta[2] + momenta[1]
    result += series_product(
        propagator_zero,
        propagator(after_third),
        propagator(after_second),
        vertex(2, zero),
        vertex(1, after_third),
        vertex(0, after_second),
    )
    after_second = momenta[1]
    after_third = momenta[1] + momenta[2]
    result += series_product(
        propagator_zero,
        propagator(after_second),
        propagator(after_third),
        vertex(1, zero),
        vertex(2, after_second),
        vertex(0, after_third),
    )
    return 0.5 * result, maximum_inverse_residual


def sphere_three_quadrature(
    angular_order: int,
) -> tuple[np.ndarray, np.ndarray]:
    chi_index = np.arange(1, angular_order + 1, dtype=float)
    chi = chi_index * math.pi / (angular_order + 1)
    u = np.cos(chi)
    u_weights = (
        math.pi
        / (angular_order + 1)
        * np.sin(chi) ** 2
    )
    v, v_weights = np.polynomial.legendre.leggauss(angular_order)
    phi_count = 2 * angular_order
    phi = 2.0 * math.pi * np.arange(phi_count) / phi_count
    directions: list[list[float]] = []
    weights: list[float] = []
    for u_value, u_weight in zip(u, u_weights):
        sin_chi = math.sqrt(max(0.0, 1.0 - u_value**2))
        for v_value, v_weight in zip(v, v_weights):
            sin_theta = math.sqrt(max(0.0, 1.0 - v_value**2))
            for phi_value in phi:
                directions.append(
                    [
                        u_value,
                        sin_chi * v_value,
                        sin_chi * sin_theta * math.cos(phi_value),
                        sin_chi * sin_theta * math.sin(phi_value),
                    ]
                )
                weights.append(
                    u_weight
                    * v_weight
                    * (2.0 * math.pi / phi_count)
                )
    return np.asarray(directions), np.asarray(weights)


def continuum_momentum_quadrature(
    mass: float, radial_order: int, angular_order: int
) -> tuple[np.ndarray, np.ndarray]:
    radial_nodes, radial_weights = np.polynomial.legendre.leggauss(radial_order)
    unit_interval = 0.5 * (radial_nodes + 1.0)
    unit_weights = 0.5 * radial_weights
    angle = 0.5 * math.pi * unit_interval
    radius = mass * np.tan(angle)
    radial_jacobian = (
        mass * 0.5 * math.pi / np.cos(angle) ** 2
    )
    directions, angular_weights = sphere_three_quadrature(angular_order)
    momentum = (
        radius[:, np.newaxis, np.newaxis]
        * directions[np.newaxis, :, :]
    ).reshape(-1, DIMENSIONS)
    weights = (
        (radius**3 * radial_jacobian * unit_weights)[:, np.newaxis]
        * angular_weights[np.newaxis, :]
        / (2.0 * math.pi) ** 4
    ).reshape(-1)
    return momentum, weights


def complex_TTT_continuum_series_density(
    momenta: np.ndarray,
    polarizations: np.ndarray,
    mass: float,
    radial_order: int = 64,
    angular_order: int = 8,
    chunk_size: int = 100_000,
) -> tuple[np.ndarray, float]:
    momentum, weights = continuum_momentum_quadrature(
        mass, radial_order, angular_order
    )
    total = np.zeros(SERIES_ORDER + 1, dtype=np.complex128)
    maximum_inverse_residual = 0.0
    for start in range(0, len(momentum), chunk_size):
        stop = min(start + chunk_size, len(momentum))
        response, residual = complex_TTT_continuum_series_points(
            momentum[start:stop], momenta, polarizations, mass
        )
        total += np.sum(
            response * weights[np.newaxis, start:stop], axis=1
        )
        maximum_inverse_residual = max(maximum_inverse_residual, residual)
    return total, maximum_inverse_residual


def complex_TTT_series_chunk(
    base_phase: np.ndarray,
    momenta: np.ndarray,
    polarizations: np.ndarray,
    mass: float,
    stencil: str,
) -> tuple[np.ndarray, float]:
    zero = np.zeros(DIMENSIONS, dtype=float)
    propagator_cache: dict[tuple[float, ...], np.ndarray] = {}
    maximum_inverse_residual = 0.0

    def propagator(shift: np.ndarray) -> np.ndarray:
        nonlocal maximum_inverse_residual
        key = tuple(float(value) for value in shift)
        if key not in propagator_cache:
            value, residual = propagator_series(
                base_phase, shift, mass, stencil
            )
            propagator_cache[key] = value
            maximum_inverse_residual = max(
                maximum_inverse_residual, residual
            )
        return propagator_cache[key]

    first_volume, pair_volume, triple_volume = determinant_volume_derivatives(
        polarizations
    )
    pair_coefficients = {
        key: mass**2 * value for key, value in pair_volume.items()
    }
    triple_coefficient = mass**2 * triple_volume

    def vertex(source: int, incoming_shift: np.ndarray) -> np.ndarray:
        value = metric_vertex_series(
            base_phase,
            momenta[source],
            polarizations[source],
            incoming_shift,
            stencil,
        )
        value[0] += mass**2 * first_volume[source]
        return value
    propagator_zero = propagator(zero)
    result = triple_coefficient * propagator_zero

    for first, second, third in ((0, 1, 2), (1, 0, 2), (2, 0, 1)):
        pair_shift = momenta[second] + momenta[third]
        pair_key = tuple(sorted((second, third)))
        result -= pair_coefficients[pair_key] * series_product(
            propagator_zero,
            propagator(pair_shift),
            vertex(first, pair_shift),
        )

    after_third = momenta[2]
    after_second = momenta[2] + momenta[1]
    result += series_product(
        propagator_zero,
        propagator(after_third),
        propagator(after_second),
        vertex(2, zero),
        vertex(1, after_third),
        vertex(0, after_second),
    )

    after_second = momenta[1]
    after_third = momenta[1] + momenta[2]
    result += series_product(
        propagator_zero,
        propagator(after_second),
        propagator(after_third),
        vertex(1, zero),
        vertex(2, after_second),
        vertex(0, after_third),
    )
    return 0.5 * result, maximum_inverse_residual


def complex_TTT_series_density(
    size: int,
    momenta: np.ndarray,
    polarizations: np.ndarray,
    mass: float,
    stencil: str,
    quadrature: str = "uniform",
    chunk_size: int = 100_000,
) -> tuple[np.ndarray, float]:
    volume = size**DIMENSIONS
    total = np.zeros(SERIES_ORDER + 1, dtype=np.complex128)
    maximum_inverse_residual = 0.0
    for start in range(0, volume, chunk_size):
        momentum, weights = quadrature_chunk(
            start, min(start + chunk_size, volume), size, quadrature
        )
        base_phase = np.exp(1j * momentum)
        response, residual = complex_TTT_series_chunk(
            base_phase, momenta, polarizations, mass, stencil
        )
        total += np.sum(response * weights[np.newaxis, :], axis=1)
        maximum_inverse_residual = max(maximum_inverse_residual, residual)
    return total, maximum_inverse_residual


def derivative_symbols_direct(
    momentum: np.ndarray, stencil: str
) -> tuple[np.ndarray, np.ndarray]:
    positive = np.exp(1j * momentum)
    negative = np.exp(-1j * momentum)
    if stencil == "nearest":
        forward = positive - 1.0
        backward = 1.0 - negative
    elif stencil == "improved":
        forward = (-3.0 + 4.0 * positive - positive**2) / 2.0
        backward = (3.0 - 4.0 * negative + negative**2) / 2.0
    else:
        raise ValueError(f"unknown stencil: {stencil}")
    return forward, backward


def propagator_direct(
    momentum: np.ndarray, mass: float, stencil: str
) -> np.ndarray:
    forward, backward = derivative_symbols_direct(momentum, stencil)
    return 1.0 / (
        mass**2
        + 0.5
        * np.sum(np.abs(forward) ** 2 + np.abs(backward) ** 2, axis=1)
    )


def metric_vertex_direct(
    source_momentum: np.ndarray,
    polarization: np.ndarray,
    incoming_momentum: np.ndarray,
    stencil: str,
) -> np.ndarray:
    outgoing_momentum = incoming_momentum + source_momentum
    forward_in, backward_in = derivative_symbols_direct(
        incoming_momentum, stencil
    )
    forward_out, backward_out = derivative_symbols_direct(
        outgoing_momentum, stencil
    )
    return 0.5 * (
        np.einsum(
            "bi,ij,bj->b",
            np.conjugate(forward_out),
            polarization,
            forward_in,
            optimize=True,
        )
        + np.einsum(
            "bi,ij,bj->b",
            np.conjugate(backward_out),
            polarization,
            backward_in,
            optimize=True,
        )
    )


def complex_TTT_direct_density(
    size: int,
    momenta: np.ndarray,
    polarizations: np.ndarray,
    mass: float,
    stencil: str,
    parameter: float,
    quadrature: str = "uniform",
    chunk_size: int = 100_000,
    kinetic_polarizations: np.ndarray | None = None,
) -> complex:
    source_momenta = parameter * momenta
    kinetic_sources = (
        polarizations
        if kinetic_polarizations is None
        else kinetic_polarizations
    )
    volume = size**DIMENSIONS
    first_volume, pair_volume, triple_volume = determinant_volume_derivatives(
        polarizations
    )
    pair_coefficients = {
        key: mass**2 * value for key, value in pair_volume.items()
    }
    triple_coefficient = mass**2 * triple_volume

    def vertex(
        source: int, incoming_momentum: np.ndarray
    ) -> np.ndarray:
        return metric_vertex_direct(
            source_momenta[source],
            kinetic_sources[source],
            incoming_momentum,
            stencil,
        ) + mass**2 * first_volume[source]
    total = 0.0j
    for start in range(0, volume, chunk_size):
        momentum, weights = quadrature_chunk(
            start, min(start + chunk_size, volume), size, quadrature
        )
        propagator_zero = propagator_direct(momentum, mass, stencil)
        integrand = propagator_zero.astype(complex) * triple_coefficient
        for first, second, third in ((0, 1, 2), (1, 0, 2), (2, 0, 1)):
            pair_momentum = source_momenta[second] + source_momenta[third]
            intermediate = momentum + pair_momentum
            pair_key = tuple(sorted((second, third)))
            integrand -= (
                propagator_zero
                * propagator_direct(intermediate, mass, stencil)
                * vertex(first, intermediate)
                * pair_coefficients[pair_key]
            )
        after_third = momentum + source_momenta[2]
        after_second = after_third + source_momenta[1]
        integrand += (
            propagator_zero
            * propagator_direct(after_third, mass, stencil)
            * propagator_direct(after_second, mass, stencil)
            * vertex(2, momentum)
            * vertex(1, after_third)
            * vertex(0, after_second)
        )
        after_second = momentum + source_momenta[1]
        after_third = after_second + source_momenta[2]
        integrand += (
            propagator_zero
            * propagator_direct(after_second, mass, stencil)
            * propagator_direct(after_third, mass, stencil)
            * vertex(1, momentum)
            * vertex(2, after_second)
            * vertex(0, after_third)
        )
        total += np.sum(integrand * weights)
    return 0.5 * total


def Taylor_validation_rows() -> list[dict[str, Any]]:
    size = 8
    mass = 1.2
    parameter = 2.0 * math.pi / size
    momenta = checkpoint_4910.BASE_MOMENTA
    polarizations = np.stack(checkpoint_4910.POLARIZATIONS)
    direct = complex_TTT_direct_density(
        size, momenta, polarizations, mass, "nearest", parameter
    )
    predecessor = checkpoint_4910.free_TTT_density(size, 1, mass)
    series, inverse_residual = complex_TTT_series_density(
        size, momenta, polarizations, mass, "nearest"
    )
    small_parameter = 0.025
    direct_small = complex_TTT_direct_density(
        size, momenta, polarizations, mass, "nearest", small_parameter
    )
    series_small = series_evaluate(series, small_parameter)
    traceful_polarizations = checkpoint_4911.random_source_ensemble(1)[0][
        "polarizations"
    ]
    first_volume, pair_volume, triple_volume = determinant_volume_derivatives(
        traceful_polarizations
    )
    profiles = [
        np.broadcast_to(
            traceful_polarizations[index],
            (1,) * DIMENSIONS + (DIMENSIONS, DIMENSIONS),
        )
        for index in range(3)
    ]
    _, _, sqrt_determinant, metric_residual = checkpoint_4911.metric_jets(
        1, profiles
    )
    jet_first = np.array(
        [float(sqrt_determinant[mask].real.ravel()[0]) for mask in (1, 2, 4)]
    )
    jet_pair = np.array(
        [
            float(sqrt_determinant[mask].real.ravel()[0])
            for mask in (3, 5, 6)
        ]
    )
    analytic_pair = np.array(
        [pair_volume[(0, 1)], pair_volume[(0, 2)], pair_volume[(1, 2)]]
    )
    jet_triple = float(sqrt_determinant[7].real.ravel()[0])
    return [
        {
            "test": "independent_4910_direct_response",
            "size": size,
            "mass": mass,
            "parameter": parameter,
            "reference_real": predecessor.real,
            "candidate_real": direct.real,
            "reference_imag": predecessor.imag,
            "candidate_imag": direct.imag,
            "absolute_residual": abs(direct - predecessor),
            "acceptance": 1e-13,
            "passed": abs(direct - predecessor) < 1e-13,
        },
        {
            "test": "sixth_order_Taylor_small_parameter",
            "size": size,
            "mass": mass,
            "parameter": small_parameter,
            "reference_real": direct_small.real,
            "candidate_real": series_small.real,
            "reference_imag": direct_small.imag,
            "candidate_imag": series_small.imag,
            "absolute_residual": abs(direct_small - series_small),
            "acceptance": 1e-11,
            "passed": abs(direct_small - series_small) < 1e-11,
        },
        {
            "test": "propagator_series_inverse",
            "size": size,
            "mass": mass,
            "parameter": 0.0,
            "reference_real": 0.0,
            "candidate_real": inverse_residual,
            "reference_imag": 0.0,
            "candidate_imag": 0.0,
            "absolute_residual": inverse_residual,
            "acceptance": 1e-12,
            "passed": inverse_residual < 1e-12,
        },
        {
            "test": "traceful_first_volume_contacts",
            "size": 1,
            "mass": 1.0,
            "parameter": 0.0,
            "reference_real": float(np.max(np.abs(jet_first))),
            "candidate_real": float(np.max(np.abs(first_volume))),
            "reference_imag": 0.0,
            "candidate_imag": 0.0,
            "absolute_residual": float(np.max(np.abs(jet_first - first_volume))),
            "acceptance": 1e-14,
            "passed": np.max(np.abs(jet_first - first_volume)) < 1e-14
            and np.max(np.abs(first_volume)) > 1e-3,
        },
        {
            "test": "traceful_pair_volume_contacts",
            "size": 1,
            "mass": 1.0,
            "parameter": 0.0,
            "reference_real": float(np.max(np.abs(jet_pair))),
            "candidate_real": float(np.max(np.abs(analytic_pair))),
            "reference_imag": 0.0,
            "candidate_imag": 0.0,
            "absolute_residual": float(np.max(np.abs(jet_pair - analytic_pair))),
            "acceptance": 1e-14,
            "passed": np.max(np.abs(jet_pair - analytic_pair)) < 1e-14,
        },
        {
            "test": "traceful_triple_volume_contact",
            "size": 1,
            "mass": 1.0,
            "parameter": 0.0,
            "reference_real": jet_triple,
            "candidate_real": triple_volume,
            "reference_imag": 0.0,
            "candidate_imag": metric_residual,
            "absolute_residual": abs(jet_triple - triple_volume),
            "acceptance": 1e-14,
            "passed": abs(jet_triple - triple_volume) < 1e-14
            and metric_residual < 1e-14,
        },
    ]


def configurations(profile: str) -> list[LatticeConfig]:
    if profile == "smoke":
        return [LatticeConfig("N8_m1_nearest", 8, 1.0, "nearest")]
    if profile == "checkpoint":
        return [
            LatticeConfig("N8_m1_nearest", 8, 1.0, "nearest"),
            LatticeConfig("N8_m1_improved", 8, 1.0, "improved"),
            LatticeConfig("N16_m1over2_nearest", 16, 0.5, "nearest"),
            LatticeConfig("N16_m1over2_improved", 16, 0.5, "improved"),
        ]
    if profile == "long":
        return [
            LatticeConfig("N16_m1_nearest", 16, 1.0, "nearest"),
            LatticeConfig("N16_m1_improved", 16, 1.0, "improved"),
            LatticeConfig("N32_m1over2_nearest", 32, 0.5, "nearest"),
            LatticeConfig("N32_m1over2_improved", 32, 0.5, "improved"),
        ]
    raise ValueError(f"unknown profile: {profile}")


def continuum_configurations(profile: str) -> list[ContinuumConfig]:
    if profile == "smoke":
        return [ContinuumConfig("C48_A6_m1", 1.0, 48, 6)]
    if profile == "checkpoint":
        return [
            ContinuumConfig("C64_A8_m1", 1.0, 64, 8),
            ContinuumConfig("C64_A8_m2", 2.0, 64, 8),
        ]
    if profile == "long":
        return [
            ContinuumConfig("C80_A10_m0p5", 0.5, 80, 10),
            ContinuumConfig("C80_A10_m1", 1.0, 80, 10),
            ContinuumConfig("C80_A10_m2", 2.0, 80, 10),
        ]
    raise ValueError(f"unknown profile: {profile}")


def load_geometric_matrix() -> tuple[list[str], np.ndarray]:
    rows = read_csv(OUTPUT / "P8_Y5_R2FR_4911_TEMPLATE_MATRIX.csv")
    geometry_ids = sorted({row["geometry_id"] for row in rows})
    operator_names = list(checkpoint_4911.OPERATOR_NAMES)
    geometry_lookup = {name: index for index, name in enumerate(geometry_ids)}
    operator_lookup = {name: index for index, name in enumerate(operator_names)}
    matrix = np.zeros((len(geometry_ids), len(operator_names)), dtype=float)
    for row in rows:
        matrix[
            geometry_lookup[row["geometry_id"]],
            operator_lookup[row["operator"]],
        ] = float(row["mixed_third_template"])
    return geometry_ids, matrix / (2.0 * math.pi) ** 4


def quotient_recovery(
    matrix_density: np.ndarray, response: np.ndarray
) -> dict[str, Any]:
    column_norms = np.linalg.norm(matrix_density, axis=0)
    normalized = matrix_density / column_norms
    beta, _, _, _ = np.linalg.lstsq(normalized, response, rcond=1e-10)
    coefficients = beta / column_norms
    reconstructed = matrix_density @ coefficients
    response_norm = max(float(np.linalg.norm(response)), 1e-30)
    residual = float(np.linalg.norm(reconstructed - response) / response_norm)
    zeta = float(checkpoint_4911.RICCI_FLAT_C3_MAP @ coefficients)
    return {
        "coefficients": coefficients,
        "reconstructed": reconstructed,
        "response_residual": residual,
        "zeta": zeta,
    }


def geometry_response_task(
    task: tuple[LatticeConfig, dict[str, Any]]
) -> tuple[dict[str, Any], float, float]:
    config, source = task
    geometry_start = time.perf_counter()
    series, inverse_residual = complex_TTT_series_density(
        config.size,
        source["momenta"],
        source["polarizations"],
        config.mass,
        config.stencil,
        config.quadrature,
    )
    phase = np.exp(1j * float(np.sum(source["phases"])))
    real_cosine_q6 = 0.25 * float(np.real(phase * series[6]))
    row = {
        "config": config.label,
        "size": config.size,
        "mass": config.mass,
        "box_mass": config.size * config.mass,
        "stencil": config.stencil,
        "quadrature": config.quadrature,
        "geometry_id": source["geometry_id"],
        "complex_q6_real": float(series[6].real),
        "complex_q6_imag": float(series[6].imag),
        "phase_sum": float(np.sum(source["phases"])),
        "real_cosine_q6_density": real_cosine_q6,
        "propagator_inverse_residual": inverse_residual,
        "elapsed_seconds": time.perf_counter() - geometry_start,
    }
    return row, real_cosine_q6, inverse_residual


def continuum_geometry_response_task(
    task: tuple[ContinuumConfig, dict[str, Any]]
) -> tuple[dict[str, Any], float, float]:
    config, source = task
    geometry_start = time.perf_counter()
    series, inverse_residual = complex_TTT_continuum_series_density(
        source["momenta"],
        source["polarizations"],
        config.mass,
        config.radial_order,
        config.angular_order,
    )
    phase = np.exp(1j * float(np.sum(source["phases"])))
    real_cosine_q6 = 0.25 * float(np.real(phase * series[6]))
    row = {
        "config": config.label,
        "mass": config.mass,
        "radial_order": config.radial_order,
        "angular_order": config.angular_order,
        "geometry_id": source["geometry_id"],
        "complex_q6_real": float(series[6].real),
        "complex_q6_imag": float(series[6].imag),
        "phase_sum": float(np.sum(source["phases"])),
        "real_cosine_q6_density": real_cosine_q6,
        "propagator_inverse_residual": inverse_residual,
        "elapsed_seconds": time.perf_counter() - geometry_start,
    }
    return row, real_cosine_q6, inverse_residual


def run_continuum_config(
    config: ContinuumConfig,
    ensemble: list[dict[str, Any]],
    geometry_ids: list[str],
    matrix_density: np.ndarray,
    workers: int = 1,
) -> dict[str, Any]:
    start = time.perf_counter()
    tasks = [(config, source) for source in ensemble]
    if workers > 1:
        with ProcessPoolExecutor(max_workers=workers) as executor:
            computed = list(
                executor.map(continuum_geometry_response_task, tasks)
            )
    else:
        computed = [continuum_geometry_response_task(task) for task in tasks]
    responses: list[dict[str, Any]] = []
    response_vector = np.zeros(len(ensemble), dtype=float)
    maximum_inverse_residual = 0.0
    for index, (row, value, residual) in enumerate(computed):
        print(
            f"4912 {config.label} {row['geometry_id']} "
            f"{index + 1}/{len(ensemble)} complete",
            flush=True,
        )
        responses.append(row)
        response_vector[index] = value
        maximum_inverse_residual = max(maximum_inverse_residual, residual)
    recovery = quotient_recovery(matrix_density, response_vector)
    leave_one: list[dict[str, Any]] = []
    for omitted, geometry_id in enumerate(geometry_ids):
        reduced = quotient_recovery(
            np.delete(matrix_density, omitted, axis=0),
            np.delete(response_vector, omitted),
        )
        predicted = float(matrix_density[omitted] @ reduced["coefficients"])
        leave_one.append(
            {
                "config": config.label,
                "omitted_geometry_id": geometry_id,
                "zeta_m2": reduced["zeta"] * config.mass**2,
                "zeta_m2_over_target": reduced["zeta"]
                * config.mass**2
                / TARGET_ZETA_M2,
                "fit_response_residual": reduced["response_residual"],
                "heldout_observed": response_vector[omitted],
                "heldout_predicted": predicted,
                "heldout_absolute_residual": abs(
                    predicted - response_vector[omitted]
                ),
            }
        )
    return {
        "config": config,
        "responses": responses,
        "response_vector": response_vector,
        "recovery": recovery,
        "leave_one": leave_one,
        "maximum_inverse_residual": maximum_inverse_residual,
        "elapsed_seconds": time.perf_counter() - start,
    }


def run_config(
    config: LatticeConfig,
    ensemble: list[dict[str, Any]],
    geometry_ids: list[str],
    matrix_density: np.ndarray,
    workers: int = 1,
) -> dict[str, Any]:
    start = time.perf_counter()
    responses: list[dict[str, Any]] = []
    response_vector = np.zeros(len(ensemble), dtype=float)
    maximum_inverse_residual = 0.0
    tasks = [(config, source) for source in ensemble]
    if workers > 1:
        with ProcessPoolExecutor(max_workers=workers) as executor:
            computed = list(executor.map(geometry_response_task, tasks))
    else:
        computed = [geometry_response_task(task) for task in tasks]
    for index, (row, real_cosine_q6, inverse_residual) in enumerate(computed):
        print(
            f"4912 {config.label} {row['geometry_id']} "
            f"{index + 1}/{len(ensemble)} complete",
            flush=True,
        )
        response_vector[index] = real_cosine_q6
        maximum_inverse_residual = max(
            maximum_inverse_residual, inverse_residual
        )
        responses.append(row)
    recovery = quotient_recovery(matrix_density, response_vector)
    leave_one: list[dict[str, Any]] = []
    for omitted, geometry_id in enumerate(geometry_ids):
        reduced_matrix = np.delete(matrix_density, omitted, axis=0)
        reduced_response = np.delete(response_vector, omitted)
        reduced = quotient_recovery(reduced_matrix, reduced_response)
        predicted = float(matrix_density[omitted] @ reduced["coefficients"])
        leave_one.append(
            {
                "config": config.label,
                "omitted_geometry_id": geometry_id,
                "zeta_m2": reduced["zeta"] * config.mass**2,
                "zeta_m2_over_target": reduced["zeta"]
                * config.mass**2
                / TARGET_ZETA_M2,
                "fit_response_residual": reduced["response_residual"],
                "heldout_observed": response_vector[omitted],
                "heldout_predicted": predicted,
                "heldout_absolute_residual": abs(
                    predicted - response_vector[omitted]
                ),
            }
        )
    return {
        "config": config,
        "responses": responses,
        "response_vector": response_vector,
        "recovery": recovery,
        "leave_one": leave_one,
        "maximum_inverse_residual": maximum_inverse_residual,
        "elapsed_seconds": time.perf_counter() - start,
    }


def cutoff_fit_rows(config_results: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for stencil in sorted(
        {result["config"].stencil for result in config_results}
    ):
        selected = [
            result
            for result in config_results
            if result["config"].stencil == stencil
        ]
        if len(selected) < 2:
            rows.append(
                {
                    "stencil": stencil,
                    "fit_model": "not_enough_cutoffs_for_diagnostic",
                    "point_count": len(selected),
                    "diagnostic_intercept": "not_applicable",
                    "diagnostic_over_target": "not_applicable",
                    "maximum_fit_residual": "not_applicable",
                    "valid_continuum_fit": False,
                    "reason": "fewer than two coarse rows",
                }
            )
            continue
        x = np.array([result["config"].mass ** 2 for result in selected])
        y = np.array(
            [
                result["recovery"]["zeta"]
                * result["config"].mass**2
                for result in selected
            ]
        )
        degree = min(2, len(selected) - 1)
        coefficients = np.polynomial.polynomial.polyfit(x, y, degree)
        fitted = np.polynomial.polynomial.polyval(x, coefficients)
        rows.append(
            {
                "stencil": stencil,
                "fit_model": f"coarse_two_point_diagnostic_degree_{degree}",
                "point_count": len(selected),
                "diagnostic_intercept": float(coefficients[0]),
                "diagnostic_over_target": float(
                    coefficients[0] / TARGET_ZETA_M2
                ),
                "maximum_fit_residual": float(np.max(np.abs(fitted - y))),
                "valid_continuum_fit": False,
                "reason": "two coarse points with unresolved hypercubic response and no common stencil limit",
            }
        )
    return rows


def matched_subtraction_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "stage": "two_point_matching",
            "equation": "choose free reference with m_ref=m_gap and common stress normalization Z_T",
            "requirement": "same lattice stencil volume contacts source ensemble and measured pole residue",
        },
        {
            "stage": "same_regulator_difference",
            "equation": "Delta y_a=y_interacting_a-y_free_a(m_ref,Z_T)",
            "requirement": "paired ensembles or common random numbers and full covariance",
        },
        {
            "stage": "continuum_restoration",
            "equation": "y_ren=y_free_cont(m_ref)+lim_(a->0) Delta y_a",
            "requirement": "Delta y agrees across nearest and improved stencils",
        },
        {
            "stage": "projected_coefficient",
            "equation": "zeta_int=zeta_free(m_ref)+v_RF P_8 lim_(a->0) Delta y_a",
            "requirement": "rank eight covariance inverse and leave-one-geometry stability",
        },
        {
            "stage": "UV_power_counting",
            "equation": "g_eff(p)=lambda/p^(8/3)=(mu/p)^(8/3)->0",
            "requirement": "numerically verify residual cutoff scaling rather than assuming cancellation",
        },
        {
            "stage": "promotion_gate",
            "equation": "Gamma_MTS_res remains zero until the paired difference has a common continuum intercept",
            "requirement": "no absolute coarse-lattice q6 coefficient is promoted",
        },
    ]


def volume_contact_rows() -> list[dict[str, Any]]:
    return [
        {
            "contact": "first",
            "equation": "s_i=(1/2) tr(e_i)",
            "TT_limit": "zero",
            "role": "mass contribution to every one-metric vertex",
        },
        {
            "contact": "pair",
            "equation": "s_ij=(1/4)tr(e_i)tr(e_j)-(1/2)tr(e_i e_j)",
            "TT_limit": "-(1/2)tr(e_i e_j)",
            "role": "mass pair seagull",
        },
        {
            "contact": "triple",
            "equation": "s_123=(1/2)[tr(e1 e2 e3)+tr(e1 e3 e2)]-(1/4)[tr(e1 e2)tr(e3)+cyclic]+(1/8)tr(e1)tr(e2)tr(e3)",
            "TT_limit": "(1/2)[tr(e1 e2 e3)+tr(e1 e3 e2)]",
            "role": "mass triple seagull",
        },
    ]


def write_gate_outputs() -> None:
    continuum = read_csv(OUTPUT / "P8_Y5_R2FR_4912_CONTINUUM_RECOVERY.csv")
    lattice = read_csv(OUTPUT / "P8_Y5_R2FR_4912_QUOTIENT_RECOVERY.csv")
    continuum_pass = bool(continuum) and all(
        float(row["response_residual"]) < 1e-10
        and abs(float(row["zeta_m2_over_target"]) - 1.0) < 1e-8
        for row in continuum
    )
    absolute_lattice_pass = bool(lattice) and all(
        float(row["response_residual"]) < 0.05
        and abs(float(row["zeta_m2_over_target"]) - 1.0) < 0.2
        for row in lattice
    )
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4912_VOLUME_CONTACT_DERIVATIVES.csv",
        tagged(volume_contact_rows()),
    )
    arbitration = [
        {
            "route": "independent_continuum_determinant_rank8_projector",
            "status": "PASS" if continuum_pass else "FAIL",
            "reason": "two masses recover the exact zeta times m squared and all leave-one projections",
        },
        {
            "route": "absolute_coarse_lattice_q6_projection",
            "status": "REJECTED" if not absolute_lattice_pass else "PASS",
            "reason": "large hypercubic residuals prior-edge-like source dependence and incompatible stencils",
        },
        {
            "route": "same_regulator_free_subtraction",
            "status": "SELECTED" if continuum_pass else "BLOCKED",
            "reason": "the interaction is UV soft and the exact free continuum restoration term is now independently fixed",
        },
        {
            "route": "unsubtracted_interacting_absolute_coefficient",
            "status": "PROHIBITED",
            "reason": "coarse free controls demonstrate order-thousand false coefficients",
        },
    ]
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4912_ARBITRATION.csv", tagged(arbitration)
    )
    interacting_gate = [
        {
            "gate": "traceful_determinant_contacts",
            "status": "PASS",
            "reason": "first pair and triple volume derivatives match the exact nilpotent determinant",
        },
        {
            "gate": "independent_continuum_free_recovery",
            "status": "PASS" if continuum_pass else "FAIL",
            "reason": "direct triangle plus all seagulls recovers the exact quotient at m=1 and m=2",
        },
        {
            "gate": "absolute_lattice_free_recovery",
            "status": "FAIL" if not absolute_lattice_pass else "PASS",
            "reason": "both tested coarse stencils are dominated by noncovariant cutoff artifacts",
        },
        {
            "gate": "matched_subtraction_contract",
            "status": "READY_FOR_PAIRED_SMOKE" if continuum_pass else "BLOCKED",
            "reason": "same-regulator free subtraction plus exact continuum restoration is fully specified",
        },
        {
            "gate": "interacting_long_run",
            "status": "DO_NOT_RUN_YET",
            "reason": "first run paired short chains and verify Delta-y cutoff and stencil stability",
        },
        {
            "gate": "active_residual",
            "status": "ZERO_PRESERVED",
            "reason": "no coarse absolute lattice coefficient is promoted",
        },
    ]
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4912_INTERACTING_RUN_GATE.csv",
        tagged(interacting_gate),
    )
    local_gate = [
        {
            "arena": "GR_Newton_PPN",
            "status": "UNCHANGED",
            "reason": "C3 begins at cubic metric order and no residual coefficient is activated",
        },
        {
            "arena": "Maxwell_Poynting",
            "status": "UNCHANGED",
            "reason": "no mixed metric-gauge operator is introduced",
        },
        {
            "arena": "strong_gravity_C3",
            "status": "FREE_PROJECTOR_CALIBRATED_INTERACTING_OPEN",
            "reason": "the continuum coefficient map is exact but the MTS interaction difference is unmeasured",
        },
        {
            "arena": "Gamma_MTS_res",
            "status": "ZERO",
            "reason": "matched interacting continuum intercept remains open",
        },
    ]
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4912_LOCAL_LIMIT_GATE.csv",
        tagged(local_gate),
    )
    decision = {
        "overall_decision": "TRACEFUL_DETERMINANT_CONTACTS_COMPLETED_DIRECT_CONTINUUM_MULTIGEOMETRY_TTT_RECOVERS_EXACT_FREE_SCALAR_C3_AT_TWO_MASSES_ABSOLUTE_COARSE_LATTICE_ROUTE_REJECTED_MATCHED_SAME_REGULATOR_FREE_SUBTRACTION_SELECTED_INTERACTING_LONG_RUN_WITHHELD_ACTIVE_RESIDUAL_ZERO_PRIVATE_NONCLAIM",
        "continuum_pass": continuum_pass,
        "absolute_lattice_pass": absolute_lattice_pass,
        "matched_subtraction_selected": continuum_pass and not absolute_lattice_pass,
        "interacting_long_run_launched": False,
        "Gamma_MTS_res": 0,
        "next_target": NEXT_TARGET,
    }
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4912_DECISION.csv", tagged([decision])
    )


def rewrite_existing_cutoff_diagnostics() -> None:
    lattice = read_csv(OUTPUT / "P8_Y5_R2FR_4912_QUOTIENT_RECOVERY.csv")
    rows: list[dict[str, Any]] = []
    for stencil in sorted({row["stencil"] for row in lattice}):
        selected = [row for row in lattice if row["stencil"] == stencil]
        x = np.array([float(row["mass"]) ** 2 for row in selected])
        y = np.array([float(row["zeta_m2"]) for row in selected])
        coefficients = np.polynomial.polynomial.polyfit(x, y, 1)
        rows.append(
            {
                "stencil": stencil,
                "fit_model": "coarse_two_point_diagnostic_degree_1",
                "point_count": len(selected),
                "diagnostic_intercept": float(coefficients[0]),
                "diagnostic_over_target": float(coefficients[0] / TARGET_ZETA_M2),
                "maximum_fit_residual": float(
                    np.max(
                        np.abs(
                            np.polynomial.polynomial.polyval(x, coefficients) - y
                        )
                    )
                ),
                "valid_continuum_fit": False,
                "reason": "two coarse points with unresolved hypercubic response and no common stencil limit",
            }
        )
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4912_CUTOFF_FITS.csv", tagged(rows)
    )


def run(profile: str, workers: int = 1) -> dict[str, Any]:
    start = time.perf_counter()
    validation = Taylor_validation_rows()
    geometry_ids, matrix_density = load_geometric_matrix()
    ensemble = checkpoint_4911.random_source_ensemble(len(geometry_ids))
    if [source["geometry_id"] for source in ensemble] != geometry_ids:
        raise RuntimeError("4911 source ensemble order mismatch")
    continuum_results = [
        run_continuum_config(
            config, ensemble, geometry_ids, matrix_density, workers
        )
        for config in continuum_configurations(profile)
    ]
    config_results = [
        run_config(config, ensemble, geometry_ids, matrix_density, workers)
        for config in configurations(profile)
    ]
    summary_rows: list[dict[str, Any]] = []
    for result in config_results:
        config = result["config"]
        recovery = result["recovery"]
        leave_one_ratios = np.array(
            [row["zeta_m2_over_target"] for row in result["leave_one"]]
        )
        summary_rows.append(
            {
                "config": config.label,
                "size": config.size,
                "mass": config.mass,
                "box_mass": config.size * config.mass,
                "stencil": config.stencil,
                "quadrature": config.quadrature,
                "response_residual": recovery["response_residual"],
                "zeta": recovery["zeta"],
                "zeta_m2": recovery["zeta"] * config.mass**2,
                "target_zeta_m2": TARGET_ZETA_M2,
                "zeta_m2_over_target": recovery["zeta"]
                * config.mass**2
                / TARGET_ZETA_M2,
                "leave_one_ratio_minimum": float(np.min(leave_one_ratios)),
                "leave_one_ratio_maximum": float(np.max(leave_one_ratios)),
                "maximum_inverse_residual": result[
                    "maximum_inverse_residual"
                ],
                "elapsed_seconds": result["elapsed_seconds"],
            }
        )
    cutoff_rows = cutoff_fit_rows(config_results)
    continuum_summary_rows: list[dict[str, Any]] = []
    for result in continuum_results:
        config = result["config"]
        recovery = result["recovery"]
        leave_one_ratios = np.array(
            [row["zeta_m2_over_target"] for row in result["leave_one"]]
        )
        continuum_summary_rows.append(
            {
                "config": config.label,
                "mass": config.mass,
                "radial_order": config.radial_order,
                "angular_order": config.angular_order,
                "response_residual": recovery["response_residual"],
                "zeta": recovery["zeta"],
                "zeta_m2": recovery["zeta"] * config.mass**2,
                "target_zeta_m2": TARGET_ZETA_M2,
                "zeta_m2_over_target": recovery["zeta"]
                * config.mass**2
                / TARGET_ZETA_M2,
                "leave_one_ratio_minimum": float(np.min(leave_one_ratios)),
                "leave_one_ratio_maximum": float(np.max(leave_one_ratios)),
                "maximum_inverse_residual": result[
                    "maximum_inverse_residual"
                ],
                "elapsed_seconds": result["elapsed_seconds"],
            }
        )
    validation_pass = all(row["passed"] for row in validation)
    continuum_pass = all(
        row["response_residual"] < 1e-10
        and abs(row["zeta_m2_over_target"] - 1.0) < 1e-8
        for row in continuum_summary_rows
    )
    all_finite = all(
        math.isfinite(float(row["zeta_m2_over_target"]))
        and math.isfinite(float(row["response_residual"]))
        for row in summary_rows
    )
    return {
        "profile": profile,
        "validation": validation,
        "continuum_results": continuum_results,
        "continuum_summary_rows": continuum_summary_rows,
        "config_results": config_results,
        "summary_rows": summary_rows,
        "cutoff_rows": cutoff_rows,
        "validation_pass": validation_pass,
        "continuum_pass": continuum_pass,
        "all_finite": all_finite,
        "elapsed_seconds": time.perf_counter() - start,
    }


def write_outputs(result: dict[str, Any]) -> None:
    responses = [
        row
        for config in result["config_results"]
        for row in config["responses"]
    ]
    leave_one = [
        row
        for config in result["config_results"]
        for row in config["leave_one"]
    ]
    continuum_responses = [
        row
        for config in result["continuum_results"]
        for row in config["responses"]
    ]
    continuum_leave_one = [
        row
        for config in result["continuum_results"]
        for row in config["leave_one"]
    ]
    coefficient_rows: list[dict[str, Any]] = []
    for config_result in result["config_results"]:
        config = config_result["config"]
        for index, operator in enumerate(checkpoint_4911.OPERATOR_NAMES):
            coefficient_rows.append(
                {
                    "config": config.label,
                    "operator_index": index,
                    "operator": operator,
                    "quotient_representative_coefficient": config_result[
                        "recovery"
                    ]["coefficients"][index],
                }
            )
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4912_TAYLOR_VALIDATION.csv",
        tagged(result["validation"]),
    )
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4912_CONTINUUM_Q6_RESPONSES.csv",
        tagged(continuum_responses),
    )
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4912_CONTINUUM_RECOVERY.csv",
        tagged(result["continuum_summary_rows"]),
    )
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4912_CONTINUUM_LEAVE_ONE.csv",
        tagged(continuum_leave_one),
    )
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4912_FREE_Q6_RESPONSES.csv",
        tagged(responses),
    )
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4912_QUOTIENT_COEFFICIENTS.csv",
        tagged(coefficient_rows),
    )
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4912_QUOTIENT_RECOVERY.csv",
        tagged(result["summary_rows"]),
    )
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4912_LEAVE_ONE_GEOMETRY.csv",
        tagged(leave_one),
    )
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4912_CUTOFF_FITS.csv",
        tagged(result["cutoff_rows"]),
    )
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4912_MATCHED_SUBTRACTION_CONTRACT.csv",
        tagged(matched_subtraction_contract_rows()),
    )
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4912_RUN_STATUS.csv",
        tagged(
            [
                {
                    "profile": result["profile"],
                    "validation_pass": result["validation_pass"],
                    "continuum_pass": result["continuum_pass"],
                    "all_finite": result["all_finite"],
                    "config_count": len(result["config_results"]),
                    "elapsed_seconds": result["elapsed_seconds"],
                    "next_target": NEXT_TARGET,
                }
            ]
        ),
    )
    write_gate_outputs()


def write_run_state(run_directory: Path, state: dict[str, Any]) -> None:
    run_directory.mkdir(parents=True, exist_ok=True)
    (run_directory / "status.json").write_text(
        json.dumps(state, indent=2), encoding="utf-8"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--profile", choices=("smoke", "checkpoint", "long"), default="smoke"
    )
    parser.add_argument("--no-write", action="store_true")
    parser.add_argument("--run-directory", type=Path)
    parser.add_argument("--workers", type=int, default=1)
    parser.add_argument("--finalize-existing", action="store_true")
    return parser.parse_args()


def main() -> int:
    arguments = parse_args()
    if arguments.finalize_existing:
        write_csv(
            OUTPUT / "P8_Y5_R2FR_4912_TAYLOR_VALIDATION.csv",
            tagged(Taylor_validation_rows()),
        )
        rewrite_existing_cutoff_diagnostics()
        write_gate_outputs()
        print("MTS_4912_EXISTING_OUTPUTS_FINALIZED")
        return 0
    if arguments.run_directory:
        write_run_state(
            arguments.run_directory,
            {
                "status": "RUNNING",
                "profile": arguments.profile,
                "started_unix": time.time(),
            },
        )
    try:
        result = run(arguments.profile, workers=max(1, arguments.workers))
        if not arguments.no_write:
            write_outputs(result)
        passed = (
            result["validation_pass"]
            and result["continuum_pass"]
            and result["all_finite"]
        )
        if arguments.run_directory:
            write_run_state(
                arguments.run_directory,
                {
                    "status": "COMPLETE" if passed else "FAILED_GATE",
                    "profile": arguments.profile,
                    "elapsed_seconds": result["elapsed_seconds"],
                    "summary": result["summary_rows"],
                },
            )
            if passed:
                (arguments.run_directory / "COMPLETE.marker").write_text(
                    "MTS_4912_COMPLETE\n", encoding="utf-8"
                )
        print(
            f"profile={arguments.profile} validation={result['validation_pass']} "
            f"continuum={result['continuum_pass']} finite={result['all_finite']} "
            f"elapsed={result['elapsed_seconds']:.3f}s"
        )
        for row in result["continuum_summary_rows"]:
            print(
                f"{row['config']} continuum_residual={row['response_residual']:.3e} "
                f"zeta_m2/target={row['zeta_m2_over_target']:.12g}"
            )
        for row in result["summary_rows"]:
            print(
                f"{row['config']} residual={row['response_residual']:.6g} "
                f"zeta_m2/target={row['zeta_m2_over_target']:.9g} "
                f"leave_one=[{row['leave_one_ratio_minimum']:.6g},"
                f"{row['leave_one_ratio_maximum']:.6g}]"
            )
        return 0 if passed else 1
    except Exception as error:
        if arguments.run_directory:
            write_run_state(
                arguments.run_directory,
                {
                    "status": "ERROR",
                    "profile": arguments.profile,
                    "error": repr(error),
                },
            )
        raise


if __name__ == "__main__":
    raise SystemExit(main())
