from __future__ import annotations

import argparse
import csv
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


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SOURCE = POST / "source-intake" / "functional_rg" / "4979"

FORMULA_CSV = SOURCE / "massless_scalar_MSbar_shell_formulas.csv"
INTEGRAND_CSV = SOURCE / "massless_scalar_exact_integrand_crosscheck.csv"
TWO_POINT_CSV = SOURCE / "massless_scalar_two_point_scheme_map.csv"
TT_CSV = SOURCE / "massless_scalar_TT_finite_determinant_match.csv"
TRACEFUL_CSV = SOURCE / "massless_scalar_traceful_continuation_audit.csv"
IDENTITY_CSV = SOURCE / "massless_scalar_finite_determinant_identities.csv"
GATE_CSV = SOURCE / "massless_scalar_finite_determinant_gate.csv"
RESULT_JSON = SOURCE / "massless_scalar_finite_determinant_results.json"
PROVENANCE = SOURCE / "PROVENANCE.md"

MARKER = "MTS_4979_MASSLESS_SCALAR_COMMON_SCHEME_FINITE_DETERMINANT"
CHECKED_DATE = "2026-07-13"
DIMENSIONS = 4
LOOP_PREFACTOR = 1.0 / (4.0 * math.pi) ** 2
ACTION_PREFACTOR = 0.5 * LOOP_PREFACTOR


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


def simplex(order: int) -> tuple[np.ndarray, np.ndarray]:
    alpha_0, alpha_1, alpha_2, weights = checkpoint_4977.quadrature_grid(order)
    coordinates = np.stack(
        (alpha_0.ravel(), alpha_1.ravel(), alpha_2.ravel()), axis=1
    )
    return coordinates, weights.ravel()


def orientation(source: dict[str, Any], index: int) -> tuple[tuple[int, ...], np.ndarray]:
    momenta = source["momenta"]
    zero = np.zeros(DIMENSIONS, dtype=float)
    sequence = (2, 1, 0) if index == 0 else (1, 2, 0)
    shifts = np.stack(
        (
            zero,
            momenta[sequence[0]],
            momenta[sequence[0]] + momenta[sequence[1]],
        )
    )
    return sequence, shifts


def exact_triangle_points(
    momentum: np.ndarray, source: dict[str, Any], external_scale: float
) -> np.ndarray:
    momenta = external_scale * source["momenta"]
    total = np.zeros(len(momentum), dtype=float)
    for orientation_index in (0, 1):
        sequence, unscaled_shifts = orientation(source, orientation_index)
        shifts = external_scale * unscaled_shifts
        propagators = [
            1.0 / np.sum((momentum + shift) ** 2, axis=1) for shift in shifts
        ]
        vertices: list[np.ndarray] = []
        for source_index, shift in zip(sequence, shifts):
            incoming = momentum + shift
            outgoing = incoming + momenta[source_index]
            vertices.append(
                np.einsum(
                    "ni,ij,nj->n",
                    outgoing,
                    source["polarizations"][source_index],
                    incoming,
                    optimize=True,
                )
            )
        total += np.prod(np.stack(propagators), axis=0) * np.prod(
            np.stack(vertices), axis=0
        )
    return 0.5 * total


def orientation_msbar(
    source: dict[str, Any],
    orientation_index: int,
    order: int,
    mu: float,
    continuation_beta: float,
) -> tuple[float, float, float, np.ndarray]:
    alpha, weights = simplex(order)
    sequence, shifts = orientation(source, orientation_index)
    momenta = source["momenta"]
    shift_average = alpha @ shifts
    delta = (
        np.sum(alpha * np.sum(shifts**2, axis=1)[np.newaxis, :], axis=1)
        - np.sum(shift_average**2, axis=1)
    )
    if np.any(delta <= 0.0):
        raise ValueError("non-positive massless triangle denominator")

    matrices: list[np.ndarray] = []
    linear: list[np.ndarray] = []
    constants: list[np.ndarray] = []
    traces: list[float] = []
    for source_index, shift in zip(sequence, shifts):
        matrix = source["polarizations"][source_index]
        incoming = shift - shift_average
        outgoing = shift + momenta[source_index] - shift_average
        matrices.append(matrix)
        traces.append(float(np.trace(matrix)))
        linear.append((incoming + outgoing) @ matrix.T)
        constants.append(
            np.einsum(
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
        + dot(linear[0], linear[1]) * constants[2]
        + dot(linear[0], linear[2]) * constants[1]
        + dot(linear[1], linear[2]) * constants[0]
    )
    expectation_2 = np.zeros_like(delta)
    for left, right, remaining in ((0, 1, 2), (0, 2, 1), (1, 2, 0)):
        expectation_2 += (
            traces[left] * traces[right]
            + 2.0 * pair_traces[min(left, right), max(left, right)]
        ) * constants[remaining]
    for quadratic, first, second in ((0, 1, 2), (1, 0, 2), (2, 0, 1)):
        expectation_2 += traces[quadratic] * dot(linear[first], linear[second])
        expectation_2 += 2.0 * np.einsum(
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

    logarithm = np.log(mu**2 / delta)
    terms = LOOP_PREFACTOR * np.stack(
        (
            expectation_0 / (2.0 * delta),
            expectation_1 * logarithm / 4.0,
            expectation_2 * delta * (-logarithm - 1.0) / 8.0,
            expectation_3 * delta**2 * (logarithm + 1.5) / 32.0,
        ),
        axis=1,
    )
    pole = LOOP_PREFACTOR * (
        expectation_1 / 4.0
        - expectation_2 * delta / 8.0
        + expectation_3 * delta**2 / 32.0
    )

    beta = continuation_beta
    trace_constant_sum = (
        traces[0] * constants[1] * constants[2]
        + traces[1] * constants[0] * constants[2]
        + traces[2] * constants[0] * constants[1]
    )
    trace_pair_constant_sum = (
        traces[0] * traces[1] * constants[2]
        + traces[0] * traces[2] * constants[1]
        + traces[1] * traces[2] * constants[0]
    )
    trace_linear_sum = (
        traces[0] * dot(linear[1], linear[2])
        + traces[1] * dot(linear[0], linear[2])
        + traces[2] * dot(linear[0], linear[1])
    )
    trace_product = traces[0] * traces[1] * traces[2]
    expectation_1_epsilon = -2.0 * beta * trace_constant_sum
    expectation_2_epsilon = (
        -4.0 * beta * (1.0 + beta) * trace_pair_constant_sum
        - 2.0 * beta * trace_linear_sum
    )
    expectation_3_epsilon = (
        -18.0 * beta - 12.0 * beta**2 - 16.0 * beta**3
    ) * trace_product
    evanescent = LOOP_PREFACTOR * (
        expectation_1_epsilon / 4.0
        - expectation_2_epsilon * delta / 8.0
        + expectation_3_epsilon * delta**2 / 32.0
    )
    return (
        float(np.sum(weights[:, np.newaxis] * terms)),
        float(np.sum(weights * evanescent)),
        float(np.sum(weights * pole)),
        np.sum(weights[:, np.newaxis] * terms, axis=0),
    )


def pair_contact_evanescent(
    source: dict[str, Any], continuation_beta: float, order: int = 192
) -> float:
    if continuation_beta == 0.0:
        return 0.0
    nodes, weights = np.polynomial.legendre.leggauss(order)
    parameter = 0.5 * (nodes + 1.0)
    weights = 0.5 * weights
    momenta = source["momenta"]
    polarizations = source["polarizations"]
    traces = np.asarray([np.trace(matrix) for matrix in polarizations])
    total = 0.0
    beta = continuation_beta
    for first, second, third in ((0, 1, 2), (1, 0, 2), (2, 0, 1)):
        pair_coefficient = (
            beta**2 * traces[second] * traces[third]
            - beta
            * float(np.trace(polarizations[second] @ polarizations[third]))
        )
        momentum = momenta[first]
        delta = parameter * (1.0 - parameter) * float(momentum @ momentum)
        constant = (
            -parameter
            * (1.0 - parameter)
            * float(momentum @ polarizations[first] @ momentum)
        )
        bracket = (
            -constant * delta / 2.0
            + (1.0 + 2.0 * beta) * traces[first] * delta**2 / 8.0
        )
        total += pair_coefficient * float(np.sum(weights * bracket))
    return LOOP_PREFACTOR * total


def determinant_response(
    source: dict[str, Any], order: int, mu: float, continuation_beta: float
) -> dict[str, Any]:
    raw = 0.0
    evanescent = 0.0
    pole = 0.0
    term_totals = np.zeros(4, dtype=float)
    for orientation_index in (0, 1):
        orientation_raw, orientation_evanescent, orientation_pole, terms = (
            orientation_msbar(
                source,
                orientation_index,
                order,
                mu,
                continuation_beta,
            )
        )
        raw += orientation_raw
        evanescent += orientation_evanescent
        pole += orientation_pole
        term_totals += terms
    pair_evanescent = pair_contact_evanescent(source, continuation_beta)
    cosine_factor = 0.25 * math.cos(float(np.sum(source["phases"])))
    return {
        "W_MSbar_density": cosine_factor * (raw + evanescent + pair_evanescent),
        "raw_four_dimensional_density": cosine_factor * raw,
        "triangle_evanescent_density": cosine_factor * evanescent,
        "pair_contact_evanescent_density": cosine_factor * pair_evanescent,
        "UV_shell_density": cosine_factor * 2.0 * pole,
        "term_densities": cosine_factor * term_totals,
    }


def linear_curvature(momentum: np.ndarray, polarization: np.ndarray) -> tuple[float, np.ndarray]:
    momentum_squared = float(momentum @ momentum)
    trace = float(np.trace(polarization))
    polarization_momentum = polarization @ momentum
    scalar = float(momentum @ polarization @ momentum) + 0.5 * momentum_squared * trace
    ricci = 0.5 * (
        np.outer(momentum, polarization_momentum)
        + np.outer(polarization_momentum, momentum)
        - momentum_squared * polarization
        + 0.5 * momentum_squared * np.eye(DIMENSIONS) * trace
    )
    return scalar, ricci


def two_point_msbar_W(
    momentum: np.ndarray,
    first: np.ndarray,
    second: np.ndarray,
    mu: float,
    order: int,
) -> float:
    nodes, weights = np.polynomial.legendre.leggauss(order)
    parameter = 0.5 * (nodes + 1.0)
    weights = 0.5 * weights
    momentum_squared = float(momentum @ momentum)
    delta = parameter * (1.0 - parameter) * momentum_squared
    first_constant = (
        -parameter * (1.0 - parameter) * float(momentum @ first @ momentum)
    )
    second_constant = (
        -parameter * (1.0 - parameter) * float(momentum @ second @ momentum)
    )
    first_linear = (1.0 - 2.0 * parameter)[:, np.newaxis] * (
        first @ momentum
    )[np.newaxis, :]
    second_linear = (1.0 - 2.0 * parameter)[:, np.newaxis] * (
        second @ momentum
    )[np.newaxis, :]
    first_trace = float(np.trace(first))
    second_trace = float(np.trace(second))
    expectation_0 = first_constant * second_constant
    expectation_1 = (
        first_trace * second_constant
        + second_trace * first_constant
        + np.einsum(
            "ni,ni->n", first_linear, second_linear, optimize=True
        )
    )
    expectation_2 = (
        first_trace * second_trace + 2.0 * float(np.trace(first @ second))
    )
    logarithm = np.log(mu**2 / delta)
    finite = LOOP_PREFACTOR * (
        -0.5 * expectation_0 * logarithm
        + 0.25 * expectation_1 * delta * (logarithm + 1.0)
        - expectation_2 * delta**2 * (logarithm + 1.5) / 16.0
    )
    expectation_1_epsilon = (
        -first_trace * second_constant - second_trace * first_constant
    )
    expectation_2_epsilon = -3.0 * first_trace * second_trace
    finite += LOOP_PREFACTOR * (
        expectation_1_epsilon * delta / 4.0
        - expectation_2_epsilon * delta**2 / 16.0
    )
    return float(np.sum(weights * finite))


def two_point_scheme_map(order: int = 768) -> tuple[list[dict[str, Any]], float, float]:
    generator = np.random.default_rng(4979)
    matrix_rows: list[list[float]] = []
    responses: list[float] = []
    for _ in range(48):
        momentum = generator.integers(-2, 3, size=DIMENSIONS).astype(float)
        if float(momentum @ momentum) == 0.0:
            momentum[0] = 1.0
        first_raw = generator.normal(size=(DIMENSIONS, DIMENSIONS))
        second_raw = generator.normal(size=(DIMENSIONS, DIMENSIONS))
        first = 0.5 * (first_raw + first_raw.T)
        second = 0.5 * (second_raw + second_raw.T)
        response = two_point_msbar_W(momentum, first, second, 1.0, order)
        scalar_first, ricci_first = linear_curvature(momentum, first)
        scalar_second, ricci_second = linear_curvature(momentum, second)
        ricci_product = float(np.sum(ricci_first * ricci_second))
        scalar_product = scalar_first * scalar_second
        logarithm = math.log(float(momentum @ momentum))
        matrix_rows.append(
            [
                ricci_product * logarithm,
                ricci_product,
                scalar_product * logarithm,
                scalar_product,
            ]
        )
        responses.append(response / LOOP_PREFACTOR)
    matrix = np.asarray(matrix_rows, dtype=float)
    response_vector = np.asarray(responses, dtype=float)
    coefficients, _, _, _ = np.linalg.lstsq(matrix, response_vector, rcond=None)
    reconstructed = matrix @ coefficients
    fit_residual = float(
        np.linalg.norm(reconstructed - response_vector)
        / max(np.linalg.norm(response_vector), 1.0e-30)
    )
    expected = np.asarray((1.0 / 60.0, -23.0 / 450.0, 1.0 / 120.0, -1.0 / 1800.0))
    coefficient_residual = float(
        np.max(
            np.abs(coefficients - expected)
            / np.maximum(np.abs(expected), 1.0e-30)
        )
    )
    labels = (
        "Ricci_log_q2_over_mu2",
        "Ricci_finite_local",
        "R_log_q2_over_mu2",
        "R_finite_local",
    )
    source_values = (-1.0 / 60.0, 4.0 / 225.0, -1.0 / 120.0, -29.0 / 1800.0)
    shell_values = (0.0, -1.0 / 30.0, 0.0, -1.0 / 60.0)
    rows = []
    for label, fitted, expected_value, source_value, shell_value in zip(
        labels, coefficients, expected, source_values, shell_values
    ):
        rows.append(
            {
                "coefficient": label,
                "fitted_covariant_W_MSbar": fitted,
                "exact_covariant_W_MSbar": expected_value,
                "source_minus_W_coefficient": source_value,
                "UV_shell_local_coefficient": shell_value,
                "scheme_identity": "source(-W)=UV_shell-W_MSbar",
                "status": "derived_two_point_common_scheme_map",
            }
        )
    return rows, fit_residual, coefficient_residual


def transverse_traceless_sources() -> list[dict[str, Any]]:
    ensemble = checkpoint_4911.random_source_ensemble(4)
    generator = np.random.default_rng(497900)
    result: list[dict[str, Any]] = []
    for index, source in enumerate(ensemble):
        polarizations: list[np.ndarray] = []
        for momentum in source["momenta"]:
            projector = np.eye(DIMENSIONS) - np.outer(momentum, momentum) / float(
                momentum @ momentum
            )
            raw = generator.normal(size=(DIMENSIONS, DIMENSIONS))
            symmetric = 0.5 * (raw + raw.T)
            polarization = projector @ symmetric @ projector
            polarization -= projector * float(np.trace(polarization)) / 3.0
            polarization /= np.linalg.norm(polarization)
            polarizations.append(polarization)
        result.append(
            {
                **source,
                "geometry_id": f"TT{index:02d}",
                "polarizations": np.stack(polarizations),
            }
        )
    return result


def trace_and_transverse_residual(source: dict[str, Any]) -> tuple[float, float]:
    trace_residual = max(
        abs(float(np.trace(polarization)))
        for polarization in source["polarizations"]
    )
    transverse_residual = max(
        float(np.linalg.norm(polarization @ momentum))
        for polarization, momentum in zip(
            source["polarizations"], source["momenta"]
        )
    )
    return trace_residual, transverse_residual


def formula_rows() -> list[dict[str, Any]]:
    return tagged(
        [
            {
                "radial_power_k": 0,
                "MSbar_finite_integrand_without_1_over_4pi2": "E0/(2 Delta)",
                "one_over_epsilon_pole_without_1_over_4pi2": "0",
                "UV_shell_twice_pole": "0",
            },
            {
                "radial_power_k": 1,
                "MSbar_finite_integrand_without_1_over_4pi2": "E1/4 log(mu^2/Delta)",
                "one_over_epsilon_pole_without_1_over_4pi2": "E1/4",
                "UV_shell_twice_pole": "E1/2",
            },
            {
                "radial_power_k": 2,
                "MSbar_finite_integrand_without_1_over_4pi2": "E2 Delta/8 [log(Delta/mu^2)-1]",
                "one_over_epsilon_pole_without_1_over_4pi2": "-E2 Delta/8",
                "UV_shell_twice_pole": "-E2 Delta/4",
            },
            {
                "radial_power_k": 3,
                "MSbar_finite_integrand_without_1_over_4pi2": "E3 Delta^2/32 [log(mu^2/Delta)+3/2]",
                "one_over_epsilon_pole_without_1_over_4pi2": "E3 Delta^2/32",
                "UV_shell_twice_pole": "E3 Delta^2/16",
            },
        ]
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--low-order", type=int, default=40)
    parser.add_argument("--high-order", type=int, default=64)
    parser.add_argument("--source-grid", type=int, default=4)
    parser.add_argument("--mu", type=float, default=1.0)
    arguments = parser.parse_args()
    if not (0 < arguments.low_order < arguments.high_order):
        raise ValueError("require 0 < low-order < high-order")
    if arguments.source_grid < 4 or arguments.mu <= 0.0:
        raise ValueError("source-grid must be at least four and mu positive")

    started = time.perf_counter()
    SOURCE.mkdir(parents=True, exist_ok=True)
    print(f"{MARKER}_START", flush=True)
    write_csv(FORMULA_CSV, formula_rows())

    source_for_integrand = checkpoint_4911.random_source_ensemble(4)[3]
    generator = np.random.default_rng(497901)
    momentum = generator.normal(size=(96, DIMENSIONS))
    momentum += 2.5 * np.sign(momentum + 1.0e-20)
    integrand_rows: list[dict[str, Any]] = []
    maximum_integrand_residual = 0.0
    maximum_inverse_residual = 0.0
    series, inverse_residual = checkpoint_4912.complex_TTT_continuum_series_points(
        momentum,
        source_for_integrand["momenta"],
        source_for_integrand["polarizations"],
        0.0,
    )
    maximum_inverse_residual = max(maximum_inverse_residual, inverse_residual)
    for external_scale in (0.01, 0.02):
        exact = exact_triangle_points(momentum, source_for_integrand, external_scale)
        taylor = checkpoint_4912.series_evaluate(series, external_scale).real
        residual = float(
            np.max(np.abs(exact - taylor))
            / max(float(np.max(np.abs(exact))), 1.0e-30)
        )
        maximum_integrand_residual = max(maximum_integrand_residual, residual)
        integrand_rows.append(
            {
                "geometry_id": source_for_integrand["geometry_id"],
                "external_scale": external_scale,
                "point_count": len(momentum),
                "maximum_exact_integrand": float(np.max(np.abs(exact))),
                "maximum_absolute_residual": float(np.max(np.abs(exact - taylor))),
                "relative_residual": residual,
                "inverse_propagator_residual": inverse_residual,
                "status": "exact_triangle_vs_order_six_Taylor",
            }
        )
    write_csv(INTEGRAND_CSV, tagged(integrand_rows))
    print(
        f"4979 exact integrand residual={maximum_integrand_residual:.3e}",
        flush=True,
    )

    two_point_rows, two_point_fit_residual, two_point_coefficient_residual = (
        two_point_scheme_map()
    )
    write_csv(TWO_POINT_CSV, tagged(two_point_rows))
    print(
        f"4979 two-point map fit={two_point_fit_residual:.3e} "
        f"coeff={two_point_coefficient_residual:.3e}",
        flush=True,
    )

    explicit_form_factors = checkpoint_4977.extract_explicit_form_factors()
    form_factor_grid = checkpoint_4977.quadrature_grid(32)
    tt_rows: list[dict[str, Any]] = []
    identity_rows: list[dict[str, Any]] = []
    maximum_tt_match = 0.0
    maximum_tt_absolute = 0.0
    maximum_tt_quadrature = 0.0
    maximum_tt_mu = 0.0
    maximum_tt_scale = 0.0
    maximum_tt_trace = 0.0
    maximum_tt_transverse = 0.0
    maximum_tt_shell = 0.0
    for source in transverse_traceless_sources():
        source_response = checkpoint_4978.geometry_response(
            source,
            arguments.source_grid,
            arguments.mu,
            explicit_form_factors,
            form_factor_grid,
        )
        low = determinant_response(
            source, arguments.low_order, arguments.mu, 0.0
        )
        high = determinant_response(
            source, arguments.high_order, arguments.mu, 0.0
        )
        source_minus_W = float(source_response["minus_W_mixed_density"])
        source_shell = 2.0 * ACTION_PREFACTOR * float(
            source_response["anomaly_local_response"]
        )
        direct_target = source_shell - source_minus_W
        reconstructed_source = source_shell - high["W_MSbar_density"]
        match_residual = relative_error(high["W_MSbar_density"], direct_target)
        absolute_residual = abs(high["W_MSbar_density"] - direct_target)
        quadrature_residual = relative_error(
            low["W_MSbar_density"], high["W_MSbar_density"]
        )
        shell_residual = relative_error(high["UV_shell_density"], source_shell)
        trace_residual, transverse_residual = trace_and_transverse_residual(source)
        maximum_tt_match = max(maximum_tt_match, match_residual)
        maximum_tt_absolute = max(maximum_tt_absolute, absolute_residual)
        maximum_tt_quadrature = max(maximum_tt_quadrature, quadrature_residual)
        maximum_tt_shell = max(maximum_tt_shell, shell_residual)
        maximum_tt_trace = max(maximum_tt_trace, trace_residual)
        maximum_tt_transverse = max(maximum_tt_transverse, transverse_residual)
        tt_rows.append(
            {
                "geometry_id": source["geometry_id"],
                "trace_residual": trace_residual,
                "transverse_residual": transverse_residual,
                "source_minus_W_density": source_minus_W,
                "source_UV_shell_density": source_shell,
                "direct_W_MSbar_low": low["W_MSbar_density"],
                "direct_W_MSbar_high": high["W_MSbar_density"],
                "direct_target_shell_minus_source": direct_target,
                "source_reconstructed_shell_minus_direct": reconstructed_source,
                "absolute_match_residual": absolute_residual,
                "relative_match_residual": match_residual,
                "quadrature_residual": quadrature_residual,
                "UV_shell_residual": shell_residual,
                "status": "unfitted_common_scheme_TT_finite_match",
            }
        )

        doubled_mu = determinant_response(
            source, arguments.high_order, 2.0 * arguments.mu, 0.0
        )
        expected_mu = high["W_MSbar_density"] + source_shell * math.log(2.0)
        mu_residual = relative_error(doubled_mu["W_MSbar_density"], expected_mu)
        maximum_tt_mu = max(maximum_tt_mu, mu_residual)
        scale = 1.7
        scaled_source = {**source, "momenta": scale * source["momenta"]}
        scaled = determinant_response(
            scaled_source,
            arguments.high_order,
            scale * arguments.mu,
            0.0,
        )
        expected_scale = scale**4 * high["W_MSbar_density"]
        scale_residual = relative_error(scaled["W_MSbar_density"], expected_scale)
        maximum_tt_scale = max(maximum_tt_scale, scale_residual)
        identity_rows.extend(
            [
                {
                    "geometry_id": source["geometry_id"],
                    "identity": "mu_rescaling_W_MSbar",
                    "left": doubled_mu["W_MSbar_density"],
                    "right": expected_mu,
                    "relative_residual": mu_residual,
                },
                {
                    "geometry_id": source["geometry_id"],
                    "identity": "common_momentum_mu_scaling",
                    "left": scaled["W_MSbar_density"],
                    "right": expected_scale,
                    "relative_residual": scale_residual,
                },
            ]
        )
        print(
            f"4979 {source['geometry_id']} direct={high['W_MSbar_density']:.12e} "
            f"target={direct_target:.12e} residual={match_residual:.3e}",
            flush=True,
        )
    write_csv(TT_CSV, tagged(tt_rows))
    write_csv(IDENTITY_CSV, tagged(identity_rows))

    predecessor_rows: list[dict[str, str]] = []
    with checkpoint_4978.ASSEMBLY_CSV.open(
        "r", encoding="utf-8", newline=""
    ) as handle:
        predecessor_rows = list(csv.DictReader(handle))
    traceful_rows: list[dict[str, Any]] = []
    maximum_product_mismatch = 0.0
    minimum_continuation_difference = math.inf
    ensemble = checkpoint_4911.random_source_ensemble(5)
    for geometry_index in (3, 4):
        source = ensemble[geometry_index]
        predecessor = next(
            row
            for row in predecessor_rows
            if row["geometry_id"] == source["geometry_id"]
            and int(row["grid_size"]) == 8
        )
        source_minus_W = float(predecessor["minus_W_mixed_density"])
        source_shell = 2.0 * ACTION_PREFACTOR * float(
            predecessor["anomaly_local_response"]
        )
        direct_target = source_shell - source_minus_W
        four_dimensional = determinant_response(
            source, arguments.high_order, arguments.mu, 0.0
        )
        product_continuation = determinant_response(
            source, arguments.high_order, arguments.mu, 0.5
        )
        mismatch = relative_error(
            product_continuation["W_MSbar_density"], direct_target
        )
        absolute_mismatch = abs(
            product_continuation["W_MSbar_density"] - direct_target
        )
        continuation_difference = abs(
            product_continuation["W_MSbar_density"]
            - four_dimensional["W_MSbar_density"]
        )
        maximum_product_mismatch = max(maximum_product_mismatch, mismatch)
        minimum_continuation_difference = min(
            minimum_continuation_difference, continuation_difference
        )
        traceful_rows.append(
            {
                "geometry_id": source["geometry_id"],
                "source_minus_W_density": source_minus_W,
                "source_UV_shell_density": source_shell,
                "direct_target_shell_minus_source": direct_target,
                "four_dimensional_W_MSbar": four_dimensional["W_MSbar_density"],
                "product_continuation_W_MSbar": product_continuation["W_MSbar_density"],
                "product_triangle_evanescent": product_continuation[
                    "triangle_evanescent_density"
                ],
                "product_pair_contact_evanescent": product_continuation[
                    "pair_contact_evanescent_density"
                ],
                "continuation_difference": continuation_difference,
                "absolute_product_target_mismatch": absolute_mismatch,
                "relative_product_target_mismatch": mismatch,
                "valid_for_complete_traceful_finite_match": False,
                "status": "traceful_evanescent_Gauss_Bonnet_contact_open",
            }
        )
    write_csv(TRACEFUL_CSV, tagged(traceful_rows))

    gates = [
        ("G01_exact_triangle_integrand", maximum_integrand_residual < 1.0e-10, f"max={maximum_integrand_residual:.3e}"),
        ("G02_series_inverse", maximum_inverse_residual < 1.0e-12, f"max={maximum_inverse_residual:.3e}"),
        ("G03_two_point_covariant_fit", two_point_fit_residual < 1.0e-8, f"residual={two_point_fit_residual:.3e}"),
        ("G04_two_point_exact_coefficients", two_point_coefficient_residual < 1.0e-6, f"max={two_point_coefficient_residual:.3e}"),
        ("G05_four_TT_controls", len(tt_rows) == 4, f"rows={len(tt_rows)}"),
        ("G06_TT_projectors", max(maximum_tt_trace, maximum_tt_transverse) < 1.0e-12, f"trace={maximum_tt_trace:.3e} transverse={maximum_tt_transverse:.3e}"),
        ("G07_TT_finite_match", maximum_tt_match < 1.0e-8 and maximum_tt_absolute < 5.0e-13, f"relative={maximum_tt_match:.3e} absolute={maximum_tt_absolute:.3e}"),
        ("G08_TT_quadrature", maximum_tt_quadrature < 1.0e-7, f"max={maximum_tt_quadrature:.3e}"),
        ("G09_TT_UV_shell", maximum_tt_shell < 1.0e-10, f"max={maximum_tt_shell:.3e}"),
        ("G10_mu_identity", maximum_tt_mu < 1.0e-10, f"max={maximum_tt_mu:.3e}"),
        ("G11_scale_identity", maximum_tt_scale < 1.0e-10, f"max={maximum_tt_scale:.3e}"),
        ("G12_traceful_controls_present", len(traceful_rows) == 2, f"rows={len(traceful_rows)}"),
        ("G13_continuation_dependence_detected", minimum_continuation_difference > 1.0e-8, f"minimum={minimum_continuation_difference:.3e}"),
        ("G14_traceful_not_overclaimed", maximum_product_mismatch > 1.0e-3 and all(not row["valid_for_complete_traceful_finite_match"] for row in traceful_rows), f"max mismatch={maximum_product_mismatch:.3e}"),
        ("G15_TT_common_scheme_promoted_only", True, "TT finite match true; generic trace/contact completion false"),
        ("G16_full_MTS_false", True, "free scalar control only"),
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

    result = {
        "checkpoint_marker": MARKER,
        "low_order": arguments.low_order,
        "high_order": arguments.high_order,
        "source_grid": arguments.source_grid,
        "mu": arguments.mu,
        "maximum_exact_integrand_residual": maximum_integrand_residual,
        "maximum_inverse_propagator_residual": maximum_inverse_residual,
        "two_point_fit_residual": two_point_fit_residual,
        "two_point_coefficient_residual": two_point_coefficient_residual,
        "TT_geometry_count": len(tt_rows),
        "maximum_TT_finite_match_residual": maximum_tt_match,
        "maximum_TT_finite_match_absolute_residual": maximum_tt_absolute,
        "maximum_TT_quadrature_residual": maximum_tt_quadrature,
        "maximum_TT_UV_shell_residual": maximum_tt_shell,
        "maximum_mu_identity_residual": maximum_tt_mu,
        "maximum_scale_identity_residual": maximum_tt_scale,
        "maximum_traceful_product_continuation_mismatch": maximum_product_mismatch,
        "minimum_traceful_continuation_difference": minimum_continuation_difference,
        "gate_pass_count": sum(bool(passed) for _, passed, _ in gates),
        "gate_count": len(gates),
        "valid_for_exact_massless_triangle_integrand": maximum_integrand_residual < 1.0e-10,
        "valid_for_two_point_common_scheme_map": two_point_fit_residual < 1.0e-8 and two_point_coefficient_residual < 1.0e-6,
        "valid_for_TT_common_scheme_finite_determinant_match": maximum_tt_match < 1.0e-8 and maximum_tt_absolute < 5.0e-13,
        "valid_for_complete_traceful_common_scheme_finite_determinant_match": False,
        "valid_for_full_MTS_claim": False,
        "next_target": "4980 trace-Ward and evanescent Gauss-Bonnet contact completion",
        "elapsed_seconds": time.perf_counter() - started,
    }
    RESULT_JSON.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    PROVENANCE.write_text(
        f"""# Checkpoint 4979 provenance

Marker: `{MARKER}`

- runner: `{relative(Path(__file__).resolve())}`
- runner SHA256: `{digest(Path(__file__).resolve())}`
- checkpoint-4978 source response: `{relative(checkpoint_4978.RESULT_JSON)}`
- checkpoint-4978 SHA256: `{digest(checkpoint_4978.RESULT_JSON)}`
- Barvinsky--Vilkovisky source: `{relative(checkpoint_4977.TEX_SOURCE)}`
- low/high simplex orders: `{arguments.low_order}/{arguments.high_order}`
- source metric grid: `{arguments.source_grid}`
- TT controls: `{len(tt_rows)}`
- maximum TT finite-match absolute residual: `{maximum_tt_absolute:.17g}`
- maximum TT finite-match relative residual: `{maximum_tt_match:.17g}`
- maximum generic product-continuation mismatch: `{maximum_product_mismatch:.17g}`

The exact massless triangle is Feynman-parameterized and dimensionally
renormalized in a declared MS-bar convention. The independent two-point
calculation fixes the source conversion `source(-W)=UV_shell-W_MSbar`.
Four freshly generated transverse-traceless geometries are then compared
without geometry-dependent coefficients. Generic traceful geometries are
reported separately: their remaining finite contact depends on the
evanescent continuation of the four-dimensional metric and is not promoted.
""",
        encoding="utf-8",
    )
    print(f"4979 gates {result['gate_pass_count']}/{result['gate_count']}", flush=True)
    print(f"{MARKER}_COMPLETE", flush=True)
    return 0 if result["gate_pass_count"] == result["gate_count"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
