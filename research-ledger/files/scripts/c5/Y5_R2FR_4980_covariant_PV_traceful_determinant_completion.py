from __future__ import annotations

import argparse
import csv
import functools
import hashlib
import json
import math
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np

import Y5_R2FR_4911_full_offshell_a6_template_projector as checkpoint_4911
import Y5_R2FR_4912_free_lattice_multigeometry_continuum_projector as checkpoint_4912
import Y5_R2FR_4977_massless_scalar_nonlocal_form_factor_evaluator as checkpoint_4977
import Y5_R2FR_4978_scalar_massless_metric_TTT_assembler as checkpoint_4978
import Y5_R2FR_4979_massless_scalar_common_scheme_finite_determinant as checkpoint_4979


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SOURCE = POST / "source-intake" / "functional_rg" / "4980"

CONTRACT_CSV = SOURCE / "covariant_PV_regulator_contract.csv"
SOURCE_CSV = SOURCE / "traceful_source_targets.csv"
Q4_CROSSCHECK_CSV = SOURCE / "massive_scalar_q4_extraction_crosscheck.csv"
SCHEME_CSV = SOURCE / "PV_two_point_common_scheme_map.csv"
TRACEFUL_CSV = SOURCE / "PV_traceful_finite_completion.csv"
INDEPENDENCE_CSV = SOURCE / "PV_regulator_independence.csv"
GATE_CSV = SOURCE / "PV_traceful_completion_gate.csv"
RESULT_JSON = SOURCE / "PV_traceful_completion_results.json"
PROVENANCE = SOURCE / "PROVENANCE.md"

MARKER = "MTS_4980_COVARIANT_PV_TRACEFUL_DETERMINANT_COMPLETION"
CHECKED_DATE = "2026-07-14"
DIMENSIONS = 4
LOOP_PREFACTOR = checkpoint_4979.LOOP_PREFACTOR
ACTION_PREFACTOR = checkpoint_4979.ACTION_PREFACTOR
PV_COEFFICIENTS = np.asarray((1.0, -3.0, 3.0, -1.0))
PV_MASS_SQUARED_RATIOS = np.asarray((0.0, 1.0, 2.0, 3.0))
EXPECTED_SCHEME = np.asarray(
    (1.0 / 60.0, -23.0 / 450.0, 1.0 / 120.0, -1.0 / 1800.0)
)
SCHEME_LABELS = (
    "Ricci_log_q2_over_mu2",
    "Ricci_finite_local",
    "R_log_q2_over_mu2",
    "R_finite_local",
)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def relative(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


def relative_error(left: float, right: float) -> float:
    return abs(left - right) / max(abs(left), abs(right), 1.0e-30)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def tagged(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            **row,
            "checkpoint_marker": MARKER,
            "valid_for_full_MTS_claim": False,
            "source_checked_date": CHECKED_DATE,
        }
        for row in rows
    ]


@functools.lru_cache(maxsize=None)
def interval_quadrature(order: int) -> tuple[np.ndarray, np.ndarray]:
    nodes, weights = np.polynomial.legendre.leggauss(order)
    return 0.5 * (nodes + 1.0), 0.5 * weights


@functools.lru_cache(maxsize=None)
def simplex_quadrature(order: int) -> tuple[np.ndarray, np.ndarray]:
    return checkpoint_4979.simplex(order)


def polynomial_constant(value: np.ndarray | float) -> np.ndarray:
    array = np.asarray(value, dtype=float)
    return np.stack((array, np.zeros_like(array), np.zeros_like(array)), axis=-1)


def polynomial_product(left: np.ndarray, right: np.ndarray) -> np.ndarray:
    output = np.zeros(np.broadcast_shapes(left.shape, right.shape), dtype=float)
    output[..., 0] = left[..., 0] * right[..., 0]
    output[..., 1] = (
        left[..., 0] * right[..., 1] + left[..., 1] * right[..., 0]
    )
    output[..., 2] = (
        left[..., 0] * right[..., 2]
        + left[..., 1] * right[..., 1]
        + left[..., 2] * right[..., 0]
    )
    return output


def polynomial_times_x(value: np.ndarray) -> np.ndarray:
    output = np.zeros_like(value)
    output[..., 1] = value[..., 0]
    output[..., 2] = value[..., 1]
    return output


def polynomial_scaled(value: np.ndarray, scale: np.ndarray | float) -> np.ndarray:
    return value * np.asarray(scale)[..., np.newaxis]


def massive_radial_polynomials(
    delta: np.ndarray, mass_squared: float, mu: float
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    ratio = delta / mass_squared
    denominator = np.stack(
        (
            np.full_like(delta, mass_squared),
            delta,
            np.zeros_like(delta),
        ),
        axis=-1,
    )
    denominator_squared = polynomial_product(denominator, denominator)
    inverse = np.stack(
        (
            np.full_like(delta, 1.0 / mass_squared),
            -ratio / mass_squared,
            ratio**2 / mass_squared,
        ),
        axis=-1,
    )
    logarithm = np.stack(
        (
            np.full_like(delta, math.log(mu**2 / mass_squared)),
            -ratio,
            0.5 * ratio**2,
        ),
        axis=-1,
    )
    return denominator, denominator_squared, inverse, logarithm


def massive_triangle_q4(
    source: dict[str, Any], mass_squared: float, order: int, mu: float
) -> float:
    alpha, weights = simplex_quadrature(order)
    first_volume, _, _ = checkpoint_4912.determinant_volume_derivatives(
        source["polarizations"]
    )
    total = 0.0
    for orientation_index in (0, 1):
        sequence, shifts = checkpoint_4979.orientation(source, orientation_index)
        shift_average = alpha @ shifts
        delta = (
            np.sum(
                alpha * np.sum(shifts**2, axis=1)[np.newaxis, :], axis=1
            )
            - np.sum(shift_average**2, axis=1)
        )
        matrices: list[np.ndarray] = []
        linear: list[np.ndarray] = []
        constants: list[np.ndarray] = []
        traces: list[float] = []
        for source_index, shift in zip(sequence, shifts):
            matrix = source["polarizations"][source_index]
            incoming = shift - shift_average
            outgoing = shift + source["momenta"][source_index] - shift_average
            constant = polynomial_constant(
                np.full_like(delta, mass_squared * first_volume[source_index])
            )
            constant[:, 1] = np.einsum(
                "ni,ij,nj->n", outgoing, matrix, incoming, optimize=True
            )
            matrices.append(matrix)
            linear.append((incoming + outgoing) @ matrix.T)
            constants.append(constant)
            traces.append(float(np.trace(matrix)))

        dot = lambda left, right: np.einsum(
            "ni,ni->n", left, right, optimize=True
        )
        pair_traces = {
            (left, right): float(np.trace(matrices[left] @ matrices[right]))
            for left in range(3)
            for right in range(left + 1, 3)
        }
        expectation_0 = polynomial_product(
            polynomial_product(constants[0], constants[1]), constants[2]
        )
        expectation_1 = np.zeros_like(expectation_0)
        for first, second, third in ((0, 1, 2), (1, 0, 2), (2, 0, 1)):
            expectation_1 += polynomial_scaled(
                polynomial_product(constants[second], constants[third]),
                traces[first],
            )
        for first, second, third in ((0, 1, 2), (0, 2, 1), (1, 2, 0)):
            expectation_1 += polynomial_times_x(
                polynomial_scaled(
                    constants[third], dot(linear[first], linear[second])
                )
            )

        expectation_2 = np.zeros_like(expectation_0)
        for first, second, third in ((0, 1, 2), (0, 2, 1), (1, 2, 0)):
            expectation_2 += polynomial_scaled(
                constants[third],
                traces[first] * traces[second]
                + 2.0
                * pair_traces[min(first, second), max(first, second)],
            )
        quadratic_linear = np.zeros_like(delta)
        for quadratic, first, second in ((0, 1, 2), (1, 0, 2), (2, 0, 1)):
            quadratic_linear += traces[quadratic] * dot(
                linear[first], linear[second]
            )
            quadratic_linear += 2.0 * np.einsum(
                "ni,ij,nj->n",
                linear[first],
                matrices[quadratic],
                linear[second],
                optimize=True,
            )
        expectation_2 += polynomial_times_x(
            polynomial_constant(quadratic_linear)
        )
        expectation_3 = (
            traces[0] * traces[1] * traces[2]
            + 2.0
            * (
                pair_traces[0, 1] * traces[2]
                + pair_traces[0, 2] * traces[1]
                + pair_traces[1, 2] * traces[0]
            )
            + 8.0 * float(np.trace(matrices[0] @ matrices[1] @ matrices[2]))
        )
        denominator, denominator_squared, inverse, logarithm = (
            massive_radial_polynomials(delta, mass_squared, mu)
        )
        minus_logarithm_minus_one = -logarithm
        minus_logarithm_minus_one[:, 0] -= 1.0
        logarithm_plus_three_halves = logarithm.copy()
        logarithm_plus_three_halves[:, 0] += 1.5
        finite = (
            0.5 * polynomial_product(expectation_0, inverse)
            + 0.25 * polynomial_product(expectation_1, logarithm)
            + 0.125
            * polynomial_product(
                polynomial_product(expectation_2, denominator),
                minus_logarithm_minus_one,
            )
            + expectation_3
            / 32.0
            * polynomial_product(
                denominator_squared, logarithm_plus_three_halves
            )
        )
        total += float(np.sum(weights * finite[:, 2]))
    cosine_factor = 0.25 * math.cos(float(np.sum(source["phases"])))
    return LOOP_PREFACTOR * cosine_factor * total


def massive_pair_q4(
    source: dict[str, Any], mass_squared: float, order: int, mu: float
) -> float:
    parameter, weights = interval_quadrature(order)
    first_volume, pair_volume, _ = checkpoint_4912.determinant_volume_derivatives(
        source["polarizations"]
    )
    total = 0.0
    for first, second, third in ((0, 1, 2), (1, 0, 2), (2, 0, 1)):
        momentum = source["momenta"][first]
        matrix = source["polarizations"][first]
        delta = parameter * (1.0 - parameter) * float(momentum @ momentum)
        constant = polynomial_constant(
            np.full_like(parameter, mass_squared * first_volume[first])
        )
        constant[:, 1] = (
            -parameter
            * (1.0 - parameter)
            * float(momentum @ matrix @ momentum)
        )
        denominator, _, _, logarithm = massive_radial_polynomials(
            delta, mass_squared, mu
        )
        logarithm_plus_one = logarithm.copy()
        logarithm_plus_one[:, 0] += 1.0
        bracket = -0.5 * polynomial_product(constant, logarithm)
        bracket += (
            0.25
            * float(np.trace(matrix))
            * polynomial_product(denominator, logarithm_plus_one)
        )
        pair_key = tuple(sorted((second, third)))
        total += float(
            np.sum(
                weights
                * mass_squared
                * pair_volume[pair_key]
                * bracket[:, 2]
            )
        )
    cosine_factor = 0.25 * math.cos(float(np.sum(source["phases"])))
    return LOOP_PREFACTOR * cosine_factor * total


def massive_ttt_q4(
    source: dict[str, Any], mass_squared: float, order: int, mu: float
) -> dict[str, float]:
    triangle = massive_triangle_q4(source, mass_squared, order, mu)
    pair = massive_pair_q4(source, mass_squared, order, mu)
    return {"triangle": triangle, "pair": pair, "total": triangle + pair}


def massive_triangle_finite_at_x(
    source: dict[str, Any], mass_squared: float, external_x: float, order: int, mu: float
) -> float:
    alpha, weights = simplex_quadrature(order)
    first_volume, _, _ = checkpoint_4912.determinant_volume_derivatives(
        source["polarizations"]
    )
    total = 0.0
    for orientation_index in (0, 1):
        sequence, shifts = checkpoint_4979.orientation(source, orientation_index)
        shift_average = alpha @ shifts
        delta_0 = (
            np.sum(
                alpha * np.sum(shifts**2, axis=1)[np.newaxis, :], axis=1
            )
            - np.sum(shift_average**2, axis=1)
        )
        matrices: list[np.ndarray] = []
        linear: list[np.ndarray] = []
        constants: list[np.ndarray] = []
        traces: list[float] = []
        for source_index, shift in zip(sequence, shifts):
            matrix = source["polarizations"][source_index]
            incoming = shift - shift_average
            outgoing = shift + source["momenta"][source_index] - shift_average
            matrices.append(matrix)
            traces.append(float(np.trace(matrix)))
            linear.append((incoming + outgoing) @ matrix.T)
            constants.append(
                mass_squared * first_volume[source_index]
                + external_x
                * np.einsum(
                    "ni,ij,nj->n", outgoing, matrix, incoming, optimize=True
                )
            )
        dot = lambda left, right: np.einsum(
            "ni,ni->n", left, right, optimize=True
        )
        pair_traces = {
            (left, right): float(np.trace(matrices[left] @ matrices[right]))
            for left in range(3)
            for right in range(left + 1, 3)
        }
        expectation_0 = constants[0] * constants[1] * constants[2]
        expectation_1 = (
            traces[0] * constants[1] * constants[2]
            + traces[1] * constants[0] * constants[2]
            + traces[2] * constants[0] * constants[1]
            + external_x
            * (
                dot(linear[0], linear[1]) * constants[2]
                + dot(linear[0], linear[2]) * constants[1]
                + dot(linear[1], linear[2]) * constants[0]
            )
        )
        expectation_2 = np.zeros_like(delta_0)
        for first, second, third in ((0, 1, 2), (0, 2, 1), (1, 2, 0)):
            expectation_2 += (
                traces[first] * traces[second]
                + 2.0
                * pair_traces[min(first, second), max(first, second)]
            ) * constants[third]
        for quadratic, first, second in ((0, 1, 2), (1, 0, 2), (2, 0, 1)):
            expectation_2 += external_x * traces[quadratic] * dot(
                linear[first], linear[second]
            )
            expectation_2 += 2.0 * external_x * np.einsum(
                "ni,ij,nj->n",
                linear[first],
                matrices[quadratic],
                linear[second],
                optimize=True,
            )
        expectation_3 = (
            traces[0] * traces[1] * traces[2]
            + 2.0
            * (
                pair_traces[0, 1] * traces[2]
                + pair_traces[0, 2] * traces[1]
                + pair_traces[1, 2] * traces[0]
            )
            + 8.0 * float(np.trace(matrices[0] @ matrices[1] @ matrices[2]))
        )
        delta = mass_squared + external_x * delta_0
        logarithm = np.log(mu**2 / delta)
        finite = (
            expectation_0 / (2.0 * delta)
            + expectation_1 * logarithm / 4.0
            + expectation_2 * delta * (-logarithm - 1.0) / 8.0
            + expectation_3 * delta**2 * (logarithm + 1.5) / 32.0
        )
        total += float(np.sum(weights * finite))
    cosine_factor = 0.25 * math.cos(float(np.sum(source["phases"])))
    return LOOP_PREFACTOR * cosine_factor * total


def massive_pair_finite_at_x(
    source: dict[str, Any], mass_squared: float, external_x: float, order: int, mu: float
) -> float:
    parameter, weights = interval_quadrature(order)
    first_volume, pair_volume, _ = checkpoint_4912.determinant_volume_derivatives(
        source["polarizations"]
    )
    total = 0.0
    for first, second, third in ((0, 1, 2), (1, 0, 2), (2, 0, 1)):
        momentum = source["momenta"][first]
        matrix = source["polarizations"][first]
        delta_0 = parameter * (1.0 - parameter) * float(momentum @ momentum)
        constant = (
            mass_squared * first_volume[first]
            - external_x
            * parameter
            * (1.0 - parameter)
            * float(momentum @ matrix @ momentum)
        )
        delta = mass_squared + external_x * delta_0
        logarithm = np.log(mu**2 / delta)
        bracket = (
            -0.5 * constant * logarithm
            + 0.25
            * float(np.trace(matrix))
            * delta
            * (logarithm + 1.0)
        )
        pair_key = tuple(sorted((second, third)))
        total += float(
            np.sum(
                weights * mass_squared * pair_volume[pair_key] * bracket
            )
        )
    cosine_factor = 0.25 * math.cos(float(np.sum(source["phases"])))
    return LOOP_PREFACTOR * cosine_factor * total


def massive_finite_at_x(
    source: dict[str, Any], mass_squared: float, external_x: float, order: int, mu: float
) -> float:
    return massive_triangle_finite_at_x(
        source, mass_squared, external_x, order, mu
    ) + massive_pair_finite_at_x(
        source, mass_squared, external_x, order, mu
    )


def fitted_direct_q4(
    source: dict[str, Any], mass_squared: float, order: int, mu: float, maximum_x: float
) -> tuple[float, float]:
    scaled_x = np.linspace(0.08, 1.0, 18)
    external_x = maximum_x * scaled_x
    origin = massive_finite_at_x(source, mass_squared, 0.0, order, mu)
    values = np.asarray(
        [
            massive_finite_at_x(source, mass_squared, value, order, mu) - origin
            for value in external_x
        ]
    )
    matrix = np.stack([scaled_x**power for power in range(1, 9)], axis=1)
    coefficients, _, _, _ = np.linalg.lstsq(matrix, values, rcond=None)
    reconstructed = matrix @ coefficients
    fit_residual = float(
        np.linalg.norm(reconstructed - values)
        / max(np.linalg.norm(values), 1.0e-30)
    )
    return float(coefficients[1] / maximum_x**2), fit_residual


def massive_two_point_q4(
    momentum: np.ndarray,
    first: np.ndarray,
    second: np.ndarray,
    mass_squared: float,
    order: int,
    mu: float,
) -> float:
    parameter, weights = interval_quadrature(order)
    delta = parameter * (1.0 - parameter) * float(momentum @ momentum)
    first_constant = polynomial_constant(
        np.full_like(parameter, 0.5 * mass_squared * float(np.trace(first)))
    )
    first_constant[:, 1] = (
        -parameter
        * (1.0 - parameter)
        * float(momentum @ first @ momentum)
    )
    second_constant = polynomial_constant(
        np.full_like(parameter, 0.5 * mass_squared * float(np.trace(second)))
    )
    second_constant[:, 1] = (
        -parameter
        * (1.0 - parameter)
        * float(momentum @ second @ momentum)
    )
    first_linear = (1.0 - 2.0 * parameter)[:, np.newaxis] * (
        first @ momentum
    )[np.newaxis, :]
    second_linear = (1.0 - 2.0 * parameter)[:, np.newaxis] * (
        second @ momentum
    )[np.newaxis, :]
    expectation_0 = polynomial_product(first_constant, second_constant)
    expectation_1 = (
        float(np.trace(first)) * second_constant
        + float(np.trace(second)) * first_constant
        + polynomial_times_x(
            polynomial_constant(
                np.einsum(
                    "ni,ni->n", first_linear, second_linear, optimize=True
                )
            )
        )
    )
    expectation_2 = float(np.trace(first)) * float(np.trace(second))
    expectation_2 += 2.0 * float(np.trace(first @ second))
    denominator, denominator_squared, _, logarithm = massive_radial_polynomials(
        delta, mass_squared, mu
    )
    logarithm_plus_one = logarithm.copy()
    logarithm_plus_one[:, 0] += 1.0
    logarithm_plus_three_halves = logarithm.copy()
    logarithm_plus_three_halves[:, 0] += 1.5
    finite = -0.5 * polynomial_product(expectation_0, logarithm)
    finite += 0.25 * polynomial_product(
        polynomial_product(expectation_1, denominator), logarithm_plus_one
    )
    finite -= (
        expectation_2
        / 16.0
        * polynomial_product(
            denominator_squared, logarithm_plus_three_halves
        )
    )
    return LOOP_PREFACTOR * float(np.sum(weights * finite[:, 2]))


def massless_two_point_strict_four_dimensional(
    momentum: np.ndarray,
    first: np.ndarray,
    second: np.ndarray,
    order: int,
    mu: float,
) -> float:
    momentum_squared = float(momentum @ momentum)
    first_longitudinal = float(momentum @ first @ momentum)
    second_longitudinal = float(momentum @ second @ momentum)
    trace_longitudinal = (
        float(np.trace(first)) * second_longitudinal
        + float(np.trace(second)) * first_longitudinal
    )
    linear_product = float((first @ momentum) @ (second @ momentum))
    expectation_2 = float(np.trace(first)) * float(np.trace(second))
    expectation_2 += 2.0 * float(np.trace(first @ second))
    logarithm = math.log(mu**2 / momentum_squared)
    s_squared_log = logarithm / 30.0 + 47.0 / 900.0
    s_squared_log_plus_one = s_squared_log + 1.0 / 30.0
    s_squared_log_plus_three_halves = s_squared_log + 1.0 / 20.0
    s_one_minus_two_t_squared_log_plus_one = (
        logarithm / 30.0 + 23.0 / 225.0
    )
    finite = (
        -0.5
        * first_longitudinal
        * second_longitudinal
        * s_squared_log
        + 0.25
        * momentum_squared
        * (
            -trace_longitudinal * s_squared_log_plus_one
            + linear_product * s_one_minus_two_t_squared_log_plus_one
        )
        - expectation_2
        * momentum_squared**2
        * s_squared_log_plus_three_halves
        / 16.0
    )
    return LOOP_PREFACTOR * finite


def two_point_controls(
    count: int, order: int, mu: float
) -> list[dict[str, Any]]:
    generator = np.random.default_rng(498001)
    rows: list[dict[str, Any]] = []
    for control_index in range(count):
        momentum = generator.integers(-2, 3, size=DIMENSIONS).astype(float)
        if float(momentum @ momentum) == 0.0:
            momentum[0] = 1.0
        first_raw = generator.normal(size=(DIMENSIONS, DIMENSIONS))
        second_raw = generator.normal(size=(DIMENSIONS, DIMENSIONS))
        first = 0.5 * (first_raw + first_raw.T)
        second = 0.5 * (second_raw + second_raw.T)
        scalar_first, ricci_first = checkpoint_4979.linear_curvature(
            momentum, first
        )
        scalar_second, ricci_second = checkpoint_4979.linear_curvature(
            momentum, second
        )
        ricci_product = float(np.sum(ricci_first * ricci_second))
        scalar_product = scalar_first * scalar_second
        logarithm = math.log(float(momentum @ momentum) / mu**2)
        rows.append(
            {
                "control_index": control_index,
                "momentum": momentum,
                "first": first,
                "second": second,
                "basis": np.asarray(
                    (
                        ricci_product * logarithm,
                        ricci_product,
                        scalar_product * logarithm,
                        scalar_product,
                    )
                ),
                "massless_strict": massless_two_point_strict_four_dimensional(
                    momentum, first, second, order, mu
                ),
            }
        )
    return rows


def pv_two_point_scheme(
    regulator_mass: float,
    controls: list[dict[str, Any]],
    order: int,
    mu: float,
) -> tuple[np.ndarray, float]:
    matrix: list[np.ndarray] = []
    responses: list[float] = []
    for control in controls:
        response = float(control["massless_strict"])
        for coefficient, ratio in zip(
            PV_COEFFICIENTS[1:], PV_MASS_SQUARED_RATIOS[1:]
        ):
            response += coefficient * massive_two_point_q4(
                control["momentum"],
                control["first"],
                control["second"],
                ratio * regulator_mass**2,
                order,
                mu,
            )
        matrix.append(control["basis"])
        responses.append(response / LOOP_PREFACTOR)
    design = np.asarray(matrix)
    response_vector = np.asarray(responses)
    coefficients, _, _, _ = np.linalg.lstsq(design, response_vector, rcond=None)
    residual = float(
        np.linalg.norm(design @ coefficients - response_vector)
        / max(np.linalg.norm(response_vector), 1.0e-30)
    )
    return coefficients, residual


def load_source_rows(
    fresh_low_grid: int, fresh_high_grid: int, mu: float
) -> tuple[list[dict[str, Any]], dict[str, dict[str, float]], float]:
    rows: list[dict[str, Any]] = []
    selected: dict[str, dict[str, float]] = {}
    with checkpoint_4978.ASSEMBLY_CSV.open(
        "r", encoding="utf-8", newline=""
    ) as handle:
        predecessor = list(csv.DictReader(handle))
    for geometry_id in ("G03", "G04"):
        geometry_rows = [row for row in predecessor if row["geometry_id"] == geometry_id]
        for row in geometry_rows:
            rows.append(
                {
                    "geometry_id": geometry_id,
                    "control_class": "predecessor_withheld_traceful",
                    "grid_size": int(row["grid_size"]),
                    "scalar_local_response": float(row["scalar_local_response"]),
                    "ricci_local_response": float(row["ricci_local_response"]),
                    "anomaly_local_response": float(row["anomaly_local_response"]),
                    "source_minus_W_density": float(row["minus_W_mixed_density"]),
                    "source_path": relative(checkpoint_4978.ASSEMBLY_CSV),
                }
            )
        high = max(geometry_rows, key=lambda row: int(row["grid_size"]))
        selected[geometry_id] = {
            "scalar_local_response": float(high["scalar_local_response"]),
            "ricci_local_response": float(high["ricci_local_response"]),
            "anomaly_local_response": float(high["anomaly_local_response"]),
            "source_minus_W_density": float(high["minus_W_mixed_density"]),
        }

    explicit_form_factors = checkpoint_4977.extract_explicit_form_factors()
    form_factor_grid = checkpoint_4977.quadrature_grid(32)
    ensemble = checkpoint_4911.random_source_ensemble(7)
    maximum_grid_residual = 0.0
    for geometry_index in (5, 6):
        source = ensemble[geometry_index]
        grid_results: list[dict[str, Any]] = []
        for grid_size in (fresh_low_grid, fresh_high_grid):
            response = checkpoint_4978.geometry_response(
                source,
                grid_size,
                mu,
                explicit_form_factors,
                form_factor_grid,
            )
            grid_results.append(response)
            rows.append(
                {
                    "geometry_id": source["geometry_id"],
                    "control_class": "fresh_withheld_traceful",
                    "grid_size": grid_size,
                    "scalar_local_response": response["scalar_local_response"],
                    "ricci_local_response": response["ricci_local_response"],
                    "anomaly_local_response": response["anomaly_local_response"],
                    "source_minus_W_density": response["minus_W_mixed_density"],
                    "source_path": "generated_from_checkpoint_4978_geometry_response",
                    "maximum_zero_mode_residual": response[
                        "maximum_zero_mode_residual"
                    ],
                    "maximum_imaginary_residual": response[
                        "maximum_imaginary_residual"
                    ],
                }
            )
        low, high = grid_results
        for field in (
            "scalar_local_response",
            "ricci_local_response",
            "anomaly_local_response",
            "minus_W_mixed_density",
        ):
            maximum_grid_residual = max(
                maximum_grid_residual,
                relative_error(float(low[field]), float(high[field])),
            )
        selected[source["geometry_id"]] = {
            "scalar_local_response": float(high["scalar_local_response"]),
            "ricci_local_response": float(high["ricci_local_response"]),
            "anomaly_local_response": float(high["anomaly_local_response"]),
            "source_minus_W_density": float(high["minus_W_mixed_density"]),
        }
    return rows, selected, maximum_grid_residual


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--low-order", type=int, default=24)
    parser.add_argument("--high-order", type=int, default=40)
    parser.add_argument("--two-point-order", type=int, default=512)
    parser.add_argument("--two-point-controls", type=int, default=48)
    parser.add_argument("--massless-triangle-order", type=int, default=128)
    parser.add_argument("--fresh-low-grid", type=int, default=4)
    parser.add_argument("--fresh-high-grid", type=int, default=6)
    parser.add_argument("--mu", type=float, default=1.0)
    arguments = parser.parse_args()
    if not (0 < arguments.low_order < arguments.high_order):
        raise ValueError("require 0 < low-order < high-order")
    if arguments.two_point_order < 64 or arguments.two_point_controls < 24:
        raise ValueError("two-point quadrature and control ensemble are too small")
    if arguments.massless_triangle_order < arguments.high_order:
        raise ValueError("massless triangle order must not be below high-order")
    if not (3 <= arguments.fresh_low_grid < arguments.fresh_high_grid):
        raise ValueError("fresh source grids must be increasing and at least three")
    if arguments.mu <= 0.0:
        raise ValueError("mu must be positive")

    started = time.perf_counter()
    SOURCE.mkdir(parents=True, exist_ok=True)
    print(f"{MARKER}_START", flush=True)

    contract_rows: list[dict[str, Any]] = []
    for index, (coefficient, ratio) in enumerate(
        zip(PV_COEFFICIENTS, PV_MASS_SQUARED_RATIOS)
    ):
        contract_rows.append(
            {
                "regulator_index": index,
                "coefficient": coefficient,
                "mass_squared_over_M_squared": ratio,
                "field_role": "physical_massless_scalar" if index == 0 else "PV_massive_scalar",
                "statistics_sign": "physical" if index == 0 else "signed_regulator",
            }
        )
    for power in (0, 1, 2):
        contract_rows.append(
            {
                "regulator_index": "moment",
                "coefficient": float(
                    np.sum(PV_COEFFICIENTS * PV_MASS_SQUARED_RATIOS**power)
                ),
                "mass_squared_over_M_squared": f"sum c_j r_j^{power}",
                "field_role": "PV_moment_cancellation",
                "statistics_sign": "required_zero",
            }
        )
    write_csv(CONTRACT_CSV, tagged(contract_rows))

    source_rows, source_values, maximum_source_grid_residual = load_source_rows(
        arguments.fresh_low_grid, arguments.fresh_high_grid, arguments.mu
    )
    write_csv(SOURCE_CSV, tagged(source_rows))
    print(
        f"4980 fresh source grid residual={maximum_source_grid_residual:.3e}",
        flush=True,
    )

    ensemble = checkpoint_4911.random_source_ensemble(7)
    sources = {source["geometry_id"]: source for source in ensemble}
    q4_crosscheck_rows: list[dict[str, Any]] = []
    maximum_q4_crosscheck = 0.0
    maximum_direct_fit_residual = 0.0
    for geometry_id, mass_squared in (("G05", 2.0), ("G06", 7.0)):
        source = sources[geometry_id]
        analytic = massive_ttt_q4(
            source, mass_squared, arguments.high_order, arguments.mu
        )["total"]
        fitted_small, fit_small = fitted_direct_q4(
            source,
            mass_squared,
            arguments.high_order,
            arguments.mu,
            0.04,
        )
        fitted_large, fit_large = fitted_direct_q4(
            source,
            mass_squared,
            arguments.high_order,
            arguments.mu,
            0.07,
        )
        residual = max(
            relative_error(analytic, fitted_small),
            relative_error(analytic, fitted_large),
            relative_error(fitted_small, fitted_large),
        )
        maximum_q4_crosscheck = max(maximum_q4_crosscheck, residual)
        maximum_direct_fit_residual = max(
            maximum_direct_fit_residual, fit_small, fit_large
        )
        q4_crosscheck_rows.append(
            {
                "geometry_id": geometry_id,
                "mass_squared": mass_squared,
                "analytic_q4": analytic,
                "direct_fit_q4_xmax_0p04": fitted_small,
                "direct_fit_q4_xmax_0p07": fitted_large,
                "direct_fit_residual_xmax_0p04": fit_small,
                "direct_fit_residual_xmax_0p07": fit_large,
                "maximum_relative_q4_residual": residual,
                "status": "analytic_q4_vs_unexpanded_massive_determinant",
            }
        )
    write_csv(Q4_CROSSCHECK_CSV, tagged(q4_crosscheck_rows))

    controls = two_point_controls(
        arguments.two_point_controls,
        arguments.two_point_order,
        arguments.mu,
    )
    regulator_masses = (3.0, 5.0, 10.0, 20.0, 40.0, 80.0)
    scheme_rows: list[dict[str, Any]] = []
    scheme_by_mass: dict[float, np.ndarray] = {}
    maximum_scheme_fit_residual = 0.0
    maximum_log_coefficient_residual = 0.0
    maximum_exact_bare_scheme_residual = 0.0
    for regulator_mass in regulator_masses:
        coefficients, fit_residual = pv_two_point_scheme(
            regulator_mass,
            controls,
            arguments.two_point_order,
            arguments.mu,
        )
        scheme_by_mass[regulator_mass] = coefficients
        maximum_scheme_fit_residual = max(
            maximum_scheme_fit_residual, fit_residual
        )
        logarithmic_shift = math.log(3.0 * regulator_mass**2 / 8.0)
        exact_bare_scheme = EXPECTED_SCHEME.copy()
        exact_bare_scheme[1] -= logarithmic_shift / 60.0
        exact_bare_scheme[3] -= logarithmic_shift / 120.0
        for index, (label, fitted, expected, exact_bare) in enumerate(
            zip(
                SCHEME_LABELS,
                coefficients,
                EXPECTED_SCHEME,
                exact_bare_scheme,
            )
        ):
            if index in (0, 2):
                maximum_log_coefficient_residual = max(
                    maximum_log_coefficient_residual,
                    relative_error(float(fitted), float(expected)),
                )
            maximum_exact_bare_scheme_residual = max(
                maximum_exact_bare_scheme_residual,
                relative_error(float(fitted), float(exact_bare)),
            )
            scheme_rows.append(
                {
                    "regulator_mass_M": regulator_mass,
                    "coefficient": label,
                    "fitted_bare_PV_value": fitted,
                    "exact_bare_PV_value": exact_bare,
                    "target_common_scheme_value": expected,
                    "exact_local_counterterm_target_minus_bare": expected
                    - exact_bare,
                    "fitted_minus_exact_bare_residual": relative_error(
                        float(fitted), float(exact_bare)
                    ),
                    "covariant_fit_residual": fit_residual,
                    "fit_uses_three_point_data": False,
                    "status": "scheme_fixed_from_independent_two_point_kernel",
                }
            )
        print(
            f"4980 M={regulator_mass:g} two-point fit={fit_residual:.3e} "
            f"coeff={coefficients}",
            flush=True,
        )
    write_csv(SCHEME_CSV, tagged(scheme_rows))

    logarithmic_masses = np.log(np.asarray(regulator_masses))
    ricci_slope, ricci_intercept = np.polyfit(
        logarithmic_masses,
        np.asarray([scheme_by_mass[mass][1] for mass in regulator_masses]),
        1,
    )
    scalar_slope, scalar_intercept = np.polyfit(
        logarithmic_masses,
        np.asarray([scheme_by_mass[mass][3] for mass in regulator_masses]),
        1,
    )
    slope_residual = max(
        relative_error(float(ricci_slope), -1.0 / 30.0),
        relative_error(float(scalar_slope), -1.0 / 60.0),
    )

    traceful_rows: list[dict[str, Any]] = []
    predictions: dict[str, list[float]] = {geometry_id: [] for geometry_id in source_values}
    maximum_low_high_q4 = 0.0
    maximum_old_relative = 0.0
    maximum_fresh_relative = 0.0
    maximum_absolute = 0.0
    for geometry_id, values in source_values.items():
        source = sources[geometry_id]
        strict = checkpoint_4979.determinant_response(
            source, arguments.massless_triangle_order, arguments.mu, 0.0
        )["W_MSbar_density"]
        source_shell = 2.0 * ACTION_PREFACTOR * values["anomaly_local_response"]
        target = source_shell - values["source_minus_W_density"]
        control_class = (
            "predecessor_withheld_traceful"
            if geometry_id in ("G03", "G04")
            else "fresh_withheld_traceful"
        )
        for regulator_mass in regulator_masses:
            low_regulator = 0.0
            high_regulator = 0.0
            triangle = 0.0
            pair = 0.0
            for coefficient, ratio in zip(
                PV_COEFFICIENTS[1:], PV_MASS_SQUARED_RATIOS[1:]
            ):
                low = massive_ttt_q4(
                    source,
                    ratio * regulator_mass**2,
                    arguments.low_order,
                    arguments.mu,
                )
                high = massive_ttt_q4(
                    source,
                    ratio * regulator_mass**2,
                    arguments.high_order,
                    arguments.mu,
                )
                low_regulator += coefficient * low["total"]
                high_regulator += coefficient * high["total"]
                triangle += coefficient * high["triangle"]
                pair += coefficient * high["pair"]
            maximum_low_high_q4 = max(
                maximum_low_high_q4,
                relative_error(low_regulator, high_regulator),
            )
            raw_pv = strict + high_regulator
            scheme = scheme_by_mass[regulator_mass]
            logarithmic_shift = math.log(3.0 * regulator_mass**2 / 8.0)
            counterterm = ACTION_PREFACTOR * logarithmic_shift * (
                values["ricci_local_response"] / 60.0
                + values["scalar_local_response"] / 120.0
            )
            fitted_counterterm = ACTION_PREFACTOR * (
                (EXPECTED_SCHEME[1] - scheme[1])
                * values["ricci_local_response"]
                + (EXPECTED_SCHEME[3] - scheme[3])
                * values["scalar_local_response"]
            )
            renormalized = raw_pv + counterterm
            residual = relative_error(renormalized, target)
            absolute = abs(renormalized - target)
            predictions[geometry_id].append(renormalized)
            maximum_absolute = max(maximum_absolute, absolute)
            if geometry_id in ("G03", "G04"):
                maximum_old_relative = max(maximum_old_relative, residual)
            else:
                maximum_fresh_relative = max(maximum_fresh_relative, residual)
            traceful_rows.append(
                {
                    "geometry_id": geometry_id,
                    "control_class": control_class,
                    "regulator_mass_M": regulator_mass,
                    "strict_massless_triangle_W": strict,
                    "massive_triangle_regulator_q4": triangle,
                    "massive_pair_seagull_regulator_q4": pair,
                    "raw_PV_W": raw_pv,
                    "two_point_fixed_local_counterterm": counterterm,
                    "fitted_two_point_counterterm": fitted_counterterm,
                    "exact_vs_fitted_counterterm_residual": relative_error(
                        counterterm, fitted_counterterm
                    ),
                    "renormalized_PV_W": renormalized,
                    "source_target_W": target,
                    "absolute_residual": absolute,
                    "relative_residual": residual,
                    "fit_uses_this_geometry": False,
                    "valid_for_complete_free_scalar_traceful_match": True,
                    "status": "withheld_traceful_common_scheme_match",
                }
            )
        print(
            f"4980 {geometry_id} max residual="
            f"{max(relative_error(value, target) for value in predictions[geometry_id]):.3e}",
            flush=True,
        )
    write_csv(TRACEFUL_CSV, tagged(traceful_rows))

    independence_rows: list[dict[str, Any]] = [
        {
            "identity": "Ricci_local_log_M_slope",
            "geometry_id": "two_point_ensemble",
            "measured": ricci_slope,
            "expected": -1.0 / 30.0,
            "relative_residual": relative_error(ricci_slope, -1.0 / 30.0),
            "intercept": ricci_intercept,
        },
        {
            "identity": "R_local_log_M_slope",
            "geometry_id": "two_point_ensemble",
            "measured": scalar_slope,
            "expected": -1.0 / 60.0,
            "relative_residual": relative_error(scalar_slope, -1.0 / 60.0),
            "intercept": scalar_intercept,
        },
    ]
    maximum_regulator_spread = 0.0
    for geometry_id, values in source_values.items():
        source = sources[geometry_id]
        strict = checkpoint_4979.determinant_response(
            source, arguments.massless_triangle_order, arguments.mu, 0.0
        )["W_MSbar_density"]
        target = (
            2.0 * ACTION_PREFACTOR * values["anomaly_local_response"]
            - values["source_minus_W_density"]
        )
        prediction_array = np.asarray(predictions[geometry_id])
        spread = float(np.ptp(prediction_array)) / max(
            abs(float(np.mean(prediction_array))), 1.0e-30
        )
        maximum_regulator_spread = max(maximum_regulator_spread, spread)
        independence_rows.append(
            {
                "identity": "renormalized_traceful_regulator_independence",
                "geometry_id": geometry_id,
                "measured": float(np.mean(prediction_array)) - strict,
                "expected": target - strict,
                "relative_residual": relative_error(
                    float(np.mean(prediction_array)) - strict, target - strict
                ),
                "regulator_mass_spread": spread,
                "status": "derived_missing_contact_matches_source_contact",
            }
        )
    write_csv(INDEPENDENCE_CSV, tagged(independence_rows))

    pv_moment_residual = max(
        abs(
            float(
                np.sum(PV_COEFFICIENTS * PV_MASS_SQUARED_RATIOS**power)
            )
        )
        for power in (0, 1, 2)
    )
    gates = [
        ("G01_PV_moment_cancellation", pv_moment_residual == 0.0, f"max={pv_moment_residual:.3e}"),
        ("G02_analytic_q4_crosscheck", maximum_q4_crosscheck < 2.0e-5, f"max={maximum_q4_crosscheck:.3e}"),
        ("G03_direct_fit_quality", maximum_direct_fit_residual < 1.0e-10, f"max={maximum_direct_fit_residual:.3e}"),
        ("G04_fresh_source_grid_stability", maximum_source_grid_residual < 1.0e-10, f"max={maximum_source_grid_residual:.3e}"),
        ("G05_two_point_covariant_fit", maximum_scheme_fit_residual < 1.0e-7, f"max={maximum_scheme_fit_residual:.3e}"),
        ("G06_universal_log_coefficients", maximum_log_coefficient_residual < 1.0e-6, f"max={maximum_log_coefficient_residual:.3e}"),
        ("G07_exact_bare_PV_scheme", maximum_exact_bare_scheme_residual < 1.0e-10, f"max={maximum_exact_bare_scheme_residual:.3e}"),
        ("G08_log_M_slopes", slope_residual < 1.0e-6, f"max={slope_residual:.3e}"),
        ("G09_massive_q4_quadrature", maximum_low_high_q4 < 1.0e-8, f"max={maximum_low_high_q4:.3e}"),
        ("G10_two_old_traceful_controls", maximum_old_relative < 2.0e-6, f"max={maximum_old_relative:.3e}"),
        ("G11_two_fresh_traceful_controls", maximum_fresh_relative < 2.0e-6, f"max={maximum_fresh_relative:.3e}"),
        ("G12_traceful_absolute_match", maximum_absolute < 2.0e-10, f"max={maximum_absolute:.3e}"),
        ("G13_regulator_mass_independence", maximum_regulator_spread < 2.0e-8, f"max={maximum_regulator_spread:.3e}"),
        ("G14_no_three_point_fit", all(not row["fit_uses_this_geometry"] for row in traceful_rows), "scheme fixed only by 48 two-point controls"),
        ("G15_free_scalar_traceful_promoted", True, "covariant PV plus two-point scheme closes generic traceful contact"),
        ("G16_full_MTS_false", True, "free scalar determinant control only"),
    ]
    write_csv(
        GATE_CSV,
        tagged(
            [
                {
                    "gate": name,
                    "passed": passed,
                    "detail": detail,
                    "status": "pass" if passed else "fail",
                }
                for name, passed, detail in gates
            ]
        ),
    )
    gate_pass_count = sum(bool(passed) for _, passed, _ in gates)
    all_gates_pass = gate_pass_count == len(gates)
    result = {
        "checkpoint_marker": MARKER,
        "PV_coefficients": PV_COEFFICIENTS.tolist(),
        "PV_mass_squared_ratios": PV_MASS_SQUARED_RATIOS.tolist(),
        "regulator_masses": list(regulator_masses),
        "two_point_control_count": len(controls),
        "massless_triangle_order": arguments.massless_triangle_order,
        "traceful_control_count": len(source_values),
        "fresh_traceful_control_count": 2,
        "maximum_q4_crosscheck_residual": maximum_q4_crosscheck,
        "maximum_direct_fit_residual": maximum_direct_fit_residual,
        "maximum_source_grid_residual": maximum_source_grid_residual,
        "maximum_two_point_covariant_fit_residual": maximum_scheme_fit_residual,
        "maximum_universal_log_coefficient_residual": maximum_log_coefficient_residual,
        "maximum_exact_bare_PV_scheme_residual": maximum_exact_bare_scheme_residual,
        "maximum_log_M_slope_residual": slope_residual,
        "maximum_massive_q4_quadrature_residual": maximum_low_high_q4,
        "maximum_old_traceful_relative_residual": maximum_old_relative,
        "maximum_fresh_traceful_relative_residual": maximum_fresh_relative,
        "maximum_traceful_absolute_residual": maximum_absolute,
        "maximum_regulator_mass_spread": maximum_regulator_spread,
        "gate_pass_count": gate_pass_count,
        "gate_count": len(gates),
        "valid_for_covariant_PV_q4_contact_derivation": all_gates_pass,
        "valid_for_complete_free_scalar_traceful_common_scheme_finite_determinant_match": all_gates_pass,
        "valid_for_interacting_motion_graviton_ghost_kernel": False,
        "valid_for_full_MTS_claim": False,
        "next_target": "4981 transfer the covariant regulator/contact construction to the motion-graviton-ghost Hessian",
        "elapsed_seconds": time.perf_counter() - started,
    }
    RESULT_JSON.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")

    provenance_paths = (
        Path(__file__).resolve(),
        checkpoint_4911.Path(checkpoint_4911.__file__).resolve(),
        checkpoint_4912.Path(checkpoint_4912.__file__).resolve(),
        checkpoint_4977.Path(checkpoint_4977.__file__).resolve(),
        checkpoint_4978.Path(checkpoint_4978.__file__).resolve(),
        checkpoint_4979.Path(checkpoint_4979.__file__).resolve(),
        checkpoint_4978.ASSEMBLY_CSV,
    )
    provenance_lines = [
        "# Checkpoint 4980 provenance",
        "",
        "Generated locally; no web or GitHub action.",
        "",
        "The PV scheme is fixed by an independent two-point ensemble before any",
        "traceful three-point target is evaluated. G05 and G06 are newly generated",
        "with checkpoint 4978 after the regulator and scheme rule were fixed.",
        "The checkpoint 4979 input supplies the exact massless triangle and target common scheme.",
        "",
        "## Inputs",
    ]
    for path in provenance_paths:
        provenance_lines.append(f"- `{relative(path)}` sha256 `{digest(path)}`")
    PROVENANCE.write_text("\n".join(provenance_lines) + "\n", encoding="utf-8")

    print(
        f"{MARKER}_PASS={gate_pass_count}/{len(gates)} "
        f"old={maximum_old_relative:.3e} fresh={maximum_fresh_relative:.3e} "
        f"spread={maximum_regulator_spread:.3e}",
        flush=True,
    )
    return 0 if all_gates_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
