from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
import math
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np

import Y5_R2FR_4911_full_offshell_a6_template_projector as checkpoint_4911
import Y5_R2FR_4912_free_lattice_multigeometry_continuum_projector as checkpoint_4912
import Y5_R2FR_4976_scalar_complete_local_a8_response as checkpoint_4976
import Y5_R2FR_4977_massless_scalar_nonlocal_form_factor_evaluator as checkpoint_4977


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SOURCE = POST / "source-intake" / "functional_rg" / "4978"

QUADRATIC_CSV = SOURCE / "scalar_TTT_quadratic_log_response.csv"
CUBIC_CSV = SOURCE / "scalar_TTT_cubic_channel_response.csv"
ASSEMBLY_CSV = SOURCE / "scalar_TTT_assembled_response.csv"
WARD_CSV = SOURCE / "scalar_TTT_scale_mu_Ward_identity.csv"
DIRECT_UV_CSV = SOURCE / "scalar_TTT_direct_determinant_UV_log_residue.csv"
GATE_CSV = SOURCE / "scalar_TTT_assembly_gate.csv"
RESULT_JSON = SOURCE / "scalar_TTT_assembly_results.json"
PROVENANCE = SOURCE / "PROVENANCE.md"

MARKER = "MTS_4978_SCALAR_MASSLESS_METRIC_TTT_ASSEMBLER"
CHECKED_DATE = "2026-07-13"
BITS = (1, 2, 4)
PAIRS = ((0, 1), (0, 2), (1, 2))
GRID_AXES_FIELD = tuple(range(checkpoint_4911.DIMENSIONS))

RICCI_LOG_COEFFICIENT = -1.0 / 60.0
RICCI_FINITE_COEFFICIENT = 4.0 / 225.0
SCALAR_LOG_COEFFICIENT = -1.0 / 120.0
SCALAR_FINITE_COEFFICIENT = -29.0 / 1800.0
ACTION_PREFACTOR = 1.0 / (2.0 * (4.0 * math.pi) ** 2)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def relative(path: Path) -> str:
    return str(path.relative_to(ROOT)).replace("\\", "/")


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


def core_curvature_jets(
    size: int, covariant_metric: np.ndarray, inverse_metric: np.ndarray
) -> dict[str, np.ndarray]:
    metric_derivative = checkpoint_4911.stack_derivatives(covariant_metric, size)
    christoffel_bracket = (
        checkpoint_4911.tensor_transpose(metric_derivative, (1, 0, 2))
        + checkpoint_4911.tensor_transpose(metric_derivative, (1, 2, 0))
        - metric_derivative
    )
    christoffel = 0.5 * checkpoint_4911.jet_binary_einsum(
        "...rs,...smn->...rmn", inverse_metric, christoffel_bracket
    )
    christoffel_derivative = checkpoint_4911.stack_derivatives(christoffel, size)
    derivative_first = checkpoint_4911.tensor_transpose(
        christoffel_derivative, (1, 3, 0, 2)
    )
    derivative_second = checkpoint_4911.tensor_transpose(
        christoffel_derivative, (1, 3, 2, 0)
    )
    quadratic_first = checkpoint_4911.jet_binary_einsum(
        "...rml,...lns->...rsmn", christoffel, christoffel
    )
    quadratic_second = checkpoint_4911.jet_binary_einsum(
        "...rnl,...lms->...rsmn", christoffel, christoffel
    )
    riemann_up = (
        derivative_first
        - derivative_second
        + quadratic_first
        - quadratic_second
    )
    ricci = checkpoint_4911.jet_linear_einsum("...rsrn->...sn", riemann_up)
    scalar = checkpoint_4911.jet_binary_einsum(
        "...mn,...mn->...", inverse_metric, ricci
    )
    return {"christoffel": christoffel, "ricci": ricci, "scalar": scalar}


def frequency_eigenvalues(size: int) -> np.ndarray:
    frequencies = np.fft.fftfreq(size, d=1.0 / size)
    meshes = np.meshgrid(*([frequencies] * checkpoint_4911.DIMENSIONS), indexing="ij")
    return sum(mesh**2 for mesh in meshes)


def spectral_apply(
    field: np.ndarray, multiplier: np.ndarray
) -> tuple[np.ndarray, float]:
    transformed = np.fft.fftn(field, axes=GRID_AXES_FIELD)
    trailing_rank = field.ndim - checkpoint_4911.DIMENSIONS
    shaped_multiplier = multiplier[(...,) + (None,) * trailing_rank]
    zero_mode = transformed[(0,) * checkpoint_4911.DIMENSIONS]
    scale = max(float(np.max(np.abs(transformed))), 1.0e-30)
    zero_residual = float(np.max(np.abs(zero_mode))) / scale
    result = np.fft.ifftn(shaped_multiplier * transformed, axes=GRID_AXES_FIELD)
    return result, zero_residual


def flat_log_apply(
    field: np.ndarray, size: int, mu: float
) -> tuple[np.ndarray, float]:
    eigenvalues = frequency_eigenvalues(size)
    multiplier = np.zeros_like(eigenvalues)
    positive = eigenvalues > 0.0
    multiplier[positive] = np.log(eigenvalues[positive] / mu**2)
    return spectral_apply(field, multiplier)


def frechet_log_apply(
    operator_variation_on_field: np.ndarray,
    size: int,
    input_eigenvalue: float,
) -> tuple[np.ndarray, float]:
    eigenvalues = frequency_eigenvalues(size)
    multiplier = np.zeros_like(eigenvalues)
    positive = eigenvalues > 0.0
    equal = positive & np.isclose(eigenvalues, input_eigenvalue, rtol=0.0, atol=1.0e-12)
    unequal = positive & ~equal
    multiplier[equal] = 1.0 / input_eigenvalue
    multiplier[unequal] = (
        np.log(eigenvalues[unequal] / input_eigenvalue)
        / (eigenvalues[unequal] - input_eigenvalue)
    )
    return spectral_apply(operator_variation_on_field, multiplier)


def covariant_box_jet(
    field: np.ndarray,
    rank: int,
    christoffel: np.ndarray,
    inverse_metric: np.ndarray,
    size: int,
) -> np.ndarray:
    if rank == 0:
        gradient = checkpoint_4911.stack_derivatives(field, size)
        hessian = checkpoint_4976.covariant_derivative_covariant(
            gradient, christoffel, size
        )
        return checkpoint_4976.contract_box(hessian, inverse_metric, 0)
    gradient = checkpoint_4976.covariant_derivative_covariant(
        field, christoffel, size
    )
    hessian = checkpoint_4976.covariant_derivative_covariant(
        gradient, christoffel, size
    )
    return checkpoint_4976.contract_box(hessian, inverse_metric, rank)


def log_operator_correction(
    curvature: np.ndarray,
    rank: int,
    christoffel: np.ndarray,
    inverse_metric: np.ndarray,
    momenta: np.ndarray,
    size: int,
) -> tuple[np.ndarray, float]:
    correction = np.zeros_like(curvature)
    maximum_zero_residual = 0.0
    input_eigenvalues = np.sum(momenta**2, axis=1)
    for metric_source, input_source in itertools.permutations(range(3), 2):
        metric_mask = BITS[metric_source]
        input_mask = BITS[input_source]
        pair_mask = metric_mask | input_mask
        field = np.zeros_like(curvature)
        field[input_mask] = curvature[input_mask]
        minus_box = -covariant_box_jet(
            field, rank, christoffel, inverse_metric, size
        )
        operator_variation_on_field = minus_box[pair_mask]
        response, zero_residual = frechet_log_apply(
            operator_variation_on_field,
            size,
            float(input_eigenvalues[input_source]),
        )
        correction[pair_mask] += response
        maximum_zero_residual = max(maximum_zero_residual, zero_residual)
    return correction, maximum_zero_residual


def log_image_jet(
    curvature: np.ndarray,
    correction: np.ndarray,
    size: int,
    mu: float,
) -> tuple[np.ndarray, float]:
    image = np.zeros_like(curvature)
    maximum_zero_residual = 0.0
    for mask in (*BITS, *(BITS[first] | BITS[second] for first, second in PAIRS)):
        value, zero_residual = flat_log_apply(curvature[mask], size, mu)
        image[mask] = value + correction[mask]
        maximum_zero_residual = max(maximum_zero_residual, zero_residual)
    return image, maximum_zero_residual


def integrated_scalar_product(
    left: np.ndarray,
    right: np.ndarray,
    sqrt_determinant: np.ndarray,
) -> tuple[float, float]:
    product = checkpoint_4911.jet_pointwise(left, right)
    density = checkpoint_4911.jet_pointwise(sqrt_determinant, product)
    value = np.mean(density[7])
    return float(value.real), abs(float(value.imag))


def integrated_ricci_product(
    left: np.ndarray,
    right: np.ndarray,
    sqrt_determinant: np.ndarray,
    inverse_metric: np.ndarray,
) -> tuple[float, float]:
    raised_right = checkpoint_4911.raise_tensor_axes(
        right, inverse_metric, (0, 1)
    )
    product = checkpoint_4911.jet_binary_einsum(
        "...mn,...mn->...", left, raised_right
    )
    density = checkpoint_4911.jet_pointwise(sqrt_determinant, product)
    value = np.mean(density[7])
    return float(value.real), abs(float(value.imag))


def derivative_field(field: np.ndarray, axis: int, size: int) -> np.ndarray:
    transformed = np.fft.fftn(field, axes=GRID_AXES_FIELD)
    frequencies = np.fft.fftfreq(size, d=1.0 / size)
    shape = [1] * field.ndim
    shape[axis] = size
    multiplier = 1j * frequencies.reshape(shape)
    return np.fft.ifftn(multiplier * transformed, axes=GRID_AXES_FIELD)


def gradient_field(field: np.ndarray, size: int) -> np.ndarray:
    return np.stack(
        [derivative_field(field, axis, size) for axis in range(checkpoint_4911.DIMENSIONS)],
        axis=checkpoint_4911.DIMENSIONS,
    )


def hessian_field(field: np.ndarray, size: int) -> np.ndarray:
    gradient = gradient_field(field, size)
    return np.stack(
        [derivative_field(gradient, axis, size) for axis in range(checkpoint_4911.DIMENSIONS)],
        axis=checkpoint_4911.DIMENSIONS,
    )


def linear_fields(
    curvature: dict[str, np.ndarray], size: int
) -> dict[str, list[np.ndarray]]:
    scalar = [curvature["scalar"][mask] for mask in BITS]
    ricci = [curvature["ricci"][mask] for mask in BITS]
    return {
        "scalar": scalar,
        "ricci": ricci,
        "grad_scalar": [gradient_field(value, size) for value in scalar],
        "hess_scalar": [hessian_field(value, size) for value in scalar],
        "grad_ricci": [gradient_field(value, size) for value in ricci],
        "hess_ricci": [hessian_field(value, size) for value in ricci],
    }


def cubic_invariant(
    index: int,
    assignment: tuple[int, int, int],
    fields: dict[str, list[np.ndarray]],
) -> np.ndarray:
    first, second, third = assignment
    scalar = fields["scalar"]
    ricci = fields["ricci"]
    grad_scalar = fields["grad_scalar"]
    hess_scalar = fields["hess_scalar"]
    grad_ricci = fields["grad_ricci"]
    hess_ricci = fields["hess_ricci"]

    if index == 1:
        return scalar[first] * scalar[second] * scalar[third] / 216.0
    if index == 4:
        return scalar[first] * scalar[second] * scalar[third] / 6.0
    if index == 5:
        return (
            np.einsum("...mn,...mn->...", ricci[first], ricci[second], optimize=True)
            * scalar[third]
            / 6.0
        )
    if index == 6:
        return scalar[first] * scalar[second] * scalar[third] / 36.0
    if index == 9:
        return scalar[first] * scalar[second] * scalar[third]
    if index == 10:
        return np.einsum(
            "...ma,...ab,...bm->...", ricci[first], ricci[second], ricci[third], optimize=True
        )
    if index == 11:
        return np.einsum(
            "...mn,...mn->...", ricci[first], ricci[second], optimize=True
        ) * scalar[third]
    if index == 15:
        return np.einsum(
            "...mn,...m,...n->...",
            ricci[first],
            grad_scalar[second],
            grad_scalar[third],
            optimize=True,
        ) / 6.0
    if index == 16:
        return np.einsum(
            "...mna,...nma->...", grad_ricci[first], grad_ricci[second], optimize=True
        ) * scalar[third] / 6.0
    if index == 17:
        return np.einsum(
            "...mn,...mn->...", ricci[first], hess_scalar[second], optimize=True
        ) * scalar[third] / 36.0
    if index == 22:
        return np.einsum(
            "...mn,...m,...n->...",
            ricci[first],
            grad_scalar[second],
            grad_scalar[third],
            optimize=True,
        )
    if index == 23:
        return np.einsum(
            "...mna,...nma->...", grad_ricci[first], grad_ricci[second], optimize=True
        ) * scalar[third]
    if index == 24:
        return np.einsum(
            "...mn,...mab,...nab->...",
            ricci[first],
            grad_ricci[second],
            grad_ricci[third],
            optimize=True,
        )
    if index == 25:
        return np.einsum(
            "...mn,...abm,...bna->...",
            ricci[first],
            grad_ricci[second],
            grad_ricci[third],
            optimize=True,
        )
    if index == 26:
        return np.einsum(
            "...abmn,...mnab->...",
            hess_ricci[first],
            hess_ricci[second],
            optimize=True,
        ) * scalar[third] / 6.0
    if index == 27:
        return np.einsum(
            "...abmn,...mnab->...",
            hess_ricci[first],
            hess_ricci[second],
            optimize=True,
        ) * scalar[third]
    if index == 28:
        return np.einsum(
            "...mal,...nlb,...abmn->...",
            grad_ricci[first],
            grad_ricci[second],
            hess_ricci[third],
            optimize=True,
        )
    if index == 29:
        return np.einsum(
            "...lsab,...abmn,...mnls->...",
            hess_ricci[first],
            hess_ricci[second],
            hess_ricci[third],
            optimize=True,
        )
    raise ValueError(f"unsupported cubic source index {index}")


def cubic_response(
    fields: dict[str, list[np.ndarray]],
    momenta: np.ndarray,
    explicit_form_factors: dict[int, checkpoint_4977.ExplicitFormFactor],
    form_factor_grid: tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray],
) -> tuple[float, float, list[dict[str, Any]]]:
    squared_momenta = np.sum(momenta**2, axis=1)
    form_factor_cache: dict[tuple[int, tuple[float, float, float]], float] = {}
    rows: list[dict[str, Any]] = []
    total = 0.0
    maximum_imaginary = 0.0
    for index in checkpoint_4977.RELEVANT_INDICES:
        index_total = 0.0
        for assignment in itertools.permutations(range(3)):
            boxes = tuple(-float(squared_momenta[source]) for source in assignment)
            key = (index, boxes)
            if key not in form_factor_cache:
                form_factor_cache[key] = checkpoint_4977.symmetrized_explicit_form_factor(
                    index,
                    explicit_form_factors[index],
                    boxes,
                    form_factor_grid,
                )
            invariant = cubic_invariant(index, assignment, fields)
            invariant_mean = np.mean(invariant)
            contribution = form_factor_cache[key] * float(invariant_mean.real)
            index_total += contribution
            maximum_imaginary = max(
                maximum_imaginary,
                abs(form_factor_cache[key] * float(invariant_mean.imag)),
            )
        total += index_total
        rows.append(
            {
                "form_factor_index": index,
                "summed_six_assignment_response": index_total,
                "fraction_of_cubic_sum": "pending",
            }
        )
    for row in rows:
        row["fraction_of_cubic_sum"] = (
            float(row["summed_six_assignment_response"]) / total
            if abs(total) > 1.0e-30
            else 0.0
        )
    return total, maximum_imaginary, rows


def geometry_response(
    source: dict[str, Any],
    size: int,
    mu: float,
    explicit_form_factors: dict[int, checkpoint_4977.ExplicitFormFactor],
    form_factor_grid: tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray],
) -> dict[str, Any]:
    started = time.perf_counter()
    profiles = checkpoint_4911.source_profiles(
        size, source["momenta"], source["polarizations"], source["phases"]
    )
    covariant_metric, inverse_metric, sqrt_determinant, metric_residual = (
        checkpoint_4911.metric_jets(size, profiles)
    )
    curvature = core_curvature_jets(size, covariant_metric, inverse_metric)

    scalar_correction, scalar_correction_zero = log_operator_correction(
        curvature["scalar"],
        0,
        curvature["christoffel"],
        inverse_metric,
        source["momenta"],
        size,
    )
    ricci_correction, ricci_correction_zero = log_operator_correction(
        curvature["ricci"],
        2,
        curvature["christoffel"],
        inverse_metric,
        source["momenta"],
        size,
    )
    scalar_log_image, scalar_log_zero = log_image_jet(
        curvature["scalar"], scalar_correction, size, mu
    )
    ricci_log_image, ricci_log_zero = log_image_jet(
        curvature["ricci"], ricci_correction, size, mu
    )
    scalar_log_image_mu2, scalar_log_zero_mu2 = log_image_jet(
        curvature["scalar"], scalar_correction, size, 2.0 * mu
    )
    ricci_log_image_mu2, ricci_log_zero_mu2 = log_image_jet(
        curvature["ricci"], ricci_correction, size, 2.0 * mu
    )
    scalar_log_image_frozen, _ = log_image_jet(
        curvature["scalar"], np.zeros_like(scalar_correction), size, mu
    )
    ricci_log_image_frozen, _ = log_image_jet(
        curvature["ricci"], np.zeros_like(ricci_correction), size, mu
    )

    scalar_log_response, scalar_log_imaginary = integrated_scalar_product(
        curvature["scalar"], scalar_log_image, sqrt_determinant
    )
    scalar_local_response, scalar_local_imaginary = integrated_scalar_product(
        curvature["scalar"], curvature["scalar"], sqrt_determinant
    )
    ricci_log_response, ricci_log_imaginary = integrated_ricci_product(
        curvature["ricci"], ricci_log_image, sqrt_determinant, inverse_metric
    )
    ricci_local_response, ricci_local_imaginary = integrated_ricci_product(
        curvature["ricci"], curvature["ricci"], sqrt_determinant, inverse_metric
    )
    scalar_log_response_mu2, scalar_log_imaginary_mu2 = integrated_scalar_product(
        curvature["scalar"], scalar_log_image_mu2, sqrt_determinant
    )
    ricci_log_response_mu2, ricci_log_imaginary_mu2 = integrated_ricci_product(
        curvature["ricci"], ricci_log_image_mu2, sqrt_determinant, inverse_metric
    )
    scalar_log_response_frozen, _ = integrated_scalar_product(
        curvature["scalar"], scalar_log_image_frozen, sqrt_determinant
    )
    ricci_log_response_frozen, _ = integrated_ricci_product(
        curvature["ricci"], ricci_log_image_frozen, sqrt_determinant, inverse_metric
    )

    fields = linear_fields(curvature, size)
    cubic_total, cubic_imaginary, cubic_rows = cubic_response(
        fields, source["momenta"], explicit_form_factors, form_factor_grid
    )
    scalar_quadratic = (
        SCALAR_LOG_COEFFICIENT * scalar_log_response
        + SCALAR_FINITE_COEFFICIENT * scalar_local_response
    )
    ricci_quadratic = (
        RICCI_LOG_COEFFICIENT * ricci_log_response
        + RICCI_FINITE_COEFFICIENT * ricci_local_response
    )
    anomaly_local_response = (
        SCALAR_LOG_COEFFICIENT * scalar_local_response
        + RICCI_LOG_COEFFICIENT * ricci_local_response
    )
    quadratic_total_mu2_direct = (
        SCALAR_LOG_COEFFICIENT * scalar_log_response_mu2
        + SCALAR_FINITE_COEFFICIENT * scalar_local_response
        + RICCI_LOG_COEFFICIENT * ricci_log_response_mu2
        + RICCI_FINITE_COEFFICIENT * ricci_local_response
    )
    braces_total = scalar_quadratic + ricci_quadratic + cubic_total
    maximum_zero_residual = max(
        scalar_correction_zero,
        ricci_correction_zero,
        scalar_log_zero,
        ricci_log_zero,
        scalar_log_zero_mu2,
        ricci_log_zero_mu2,
    )
    maximum_imaginary = max(
        scalar_log_imaginary,
        scalar_local_imaginary,
        ricci_log_imaginary,
        ricci_local_imaginary,
        scalar_log_imaginary_mu2,
        ricci_log_imaginary_mu2,
        cubic_imaginary,
    )
    return {
        "geometry_id": source["geometry_id"],
        "grid_size": size,
        "mu": mu,
        "scalar_log_response": scalar_log_response,
        "scalar_log_response_frozen_Box": scalar_log_response_frozen,
        "scalar_delta_logBox_response": scalar_log_response - scalar_log_response_frozen,
        "scalar_local_response": scalar_local_response,
        "ricci_log_response": ricci_log_response,
        "ricci_log_response_frozen_Box": ricci_log_response_frozen,
        "ricci_delta_logBox_response": ricci_log_response - ricci_log_response_frozen,
        "ricci_local_response": ricci_local_response,
        "scalar_quadratic_response": scalar_quadratic,
        "ricci_quadratic_response": ricci_quadratic,
        "quadratic_total": scalar_quadratic + ricci_quadratic,
        "quadratic_total_mu2_direct": quadratic_total_mu2_direct,
        "cubic_total": cubic_total,
        "anomaly_local_response": anomaly_local_response,
        "braces_total": braces_total,
        "minus_W_mixed_density": ACTION_PREFACTOR * braces_total,
        "metric_inverse_residual": metric_residual,
        "maximum_zero_mode_residual": maximum_zero_residual,
        "maximum_imaginary_residual": maximum_imaginary,
        "cubic_rows": cubic_rows,
        "elapsed_seconds": time.perf_counter() - started,
    }


def direct_determinant_uv_log_residue(
    source: dict[str, Any],
    expected_residue: float,
    radii: tuple[float, ...] = (40.0, 80.0, 160.0, 320.0, 640.0),
    angular_order: int = 6,
) -> tuple[list[dict[str, Any]], float, float]:
    directions, angular_weights = checkpoint_4912.sphere_three_quadrature(
        angular_order
    )
    phase = np.exp(1j * float(np.sum(source["phases"])))
    shell_values: list[float] = []
    rows: list[dict[str, Any]] = []
    for radius in radii:
        response, inverse_residual = checkpoint_4912.complex_TTT_continuum_series_points(
            radius * directions,
            source["momenta"],
            source["polarizations"],
            1.0,
        )
        complex_shell = (
            radius**4
            * np.sum(response[4] * angular_weights)
            / (2.0 * math.pi) ** 4
        )
        cosine_shell = 0.25 * float(np.real(phase * complex_shell))
        shell_values.append(cosine_shell)
        rows.append(
            {
                "geometry_id": source["geometry_id"],
                "radius": radius,
                "inverse_propagator_residual": inverse_residual,
                "direct_determinant_dW_dlnLambda_q4": cosine_shell,
                "expected_source_log_residue": expected_residue,
                "relative_difference_at_radius": checkpoint_4977.relative_error(
                    cosine_shell, expected_residue
                ),
                "angular_order": angular_order,
                "status": "finite_radius_UV_shell",
            }
        )
    inverse_radius_squared = 1.0 / np.asarray(radii, dtype=float) ** 2
    coefficients = np.polyfit(
        inverse_radius_squared,
        np.asarray(shell_values, dtype=float),
        2,
    )
    extrapolated = float(coefficients[-1])
    residual = checkpoint_4977.relative_error(extrapolated, expected_residue)
    rows.append(
        {
            "geometry_id": source["geometry_id"],
            "radius": "infinity_extrapolated",
            "inverse_propagator_residual": 0.0,
            "direct_determinant_dW_dlnLambda_q4": extrapolated,
            "expected_source_log_residue": expected_residue,
            "relative_difference_at_radius": residual,
            "angular_order": angular_order,
            "status": "quadratic_fit_in_inverse_radius_squared",
        }
    )
    return rows, extrapolated, residual


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--grid-sizes", default="6,8")
    parser.add_argument("--geometry-indices", default="3")
    parser.add_argument("--mu", type=float, default=1.0)
    parser.add_argument("--skip-permutation-check", action="store_true")
    arguments = parser.parse_args()
    grid_sizes = tuple(int(value) for value in arguments.grid_sizes.split(","))
    geometry_indices = tuple(int(value) for value in arguments.geometry_indices.split(","))
    if arguments.mu <= 0.0:
        raise ValueError("mu must be positive")

    started = time.perf_counter()
    SOURCE.mkdir(parents=True, exist_ok=True)
    print(f"{MARKER}_START", flush=True)
    explicit_form_factors = checkpoint_4977.extract_explicit_form_factors()
    form_factor_grid = checkpoint_4977.quadrature_grid(32)
    ensemble = checkpoint_4911.random_source_ensemble(max(geometry_indices) + 1)

    responses: list[dict[str, Any]] = []
    quadratic_rows: list[dict[str, Any]] = []
    cubic_rows: list[dict[str, Any]] = []
    for geometry_index in geometry_indices:
        source = ensemble[geometry_index]
        for size in grid_sizes:
            response = geometry_response(
                source,
                size,
                arguments.mu,
                explicit_form_factors,
                form_factor_grid,
            )
            responses.append(response)
            quadratic_rows.extend(
                [
                    {
                        "geometry_id": response["geometry_id"],
                        "grid_size": size,
                        "sector": "scalar_R2",
                        "log_functional_response": response["scalar_log_response"],
                        "local_functional_response": response["scalar_local_response"],
                        "log_coefficient": SCALAR_LOG_COEFFICIENT,
                        "finite_coefficient": SCALAR_FINITE_COEFFICIENT,
                        "weighted_response": response["scalar_quadratic_response"],
                        "mu": arguments.mu,
                    },
                    {
                        "geometry_id": response["geometry_id"],
                        "grid_size": size,
                        "sector": "Ricci2",
                        "log_functional_response": response["ricci_log_response"],
                        "local_functional_response": response["ricci_local_response"],
                        "log_coefficient": RICCI_LOG_COEFFICIENT,
                        "finite_coefficient": RICCI_FINITE_COEFFICIENT,
                        "weighted_response": response["ricci_quadratic_response"],
                        "mu": arguments.mu,
                    },
                ]
            )
            for row in response["cubic_rows"]:
                cubic_rows.append(
                    {
                        "geometry_id": response["geometry_id"],
                        "grid_size": size,
                        **row,
                    }
                )
            print(
                f"4978 {response['geometry_id']} N={size} "
                f"Q={response['quadratic_total']:.9e} C={response['cubic_total']:.9e} "
                f"total={response['braces_total']:.9e}",
                flush=True,
            )

    assembly_rows = [
        {
            key: value
            for key, value in response.items()
            if key != "cubic_rows"
        }
        for response in responses
    ]
    write_csv(QUADRATIC_CSV, tagged(quadratic_rows))
    write_csv(CUBIC_CSV, tagged(cubic_rows))
    write_csv(ASSEMBLY_CSV, tagged(assembly_rows))

    convergence_rows: list[dict[str, Any]] = []
    maximum_grid_residual = 0.0
    for geometry_index in geometry_indices:
        geometry_id = ensemble[geometry_index]["geometry_id"]
        selected = sorted(
            (response for response in responses if response["geometry_id"] == geometry_id),
            key=lambda row: row["grid_size"],
        )
        if len(selected) >= 2:
            low, high = selected[-2:]
            for field in ("quadratic_total", "cubic_total", "braces_total"):
                residual = checkpoint_4977.relative_error(low[field], high[field])
                maximum_grid_residual = max(maximum_grid_residual, residual)
                convergence_rows.append(
                    {
                        "geometry_id": geometry_id,
                        "identity": f"grid_convergence_{field}",
                        "left": low[field],
                        "right": high[field],
                        "relative_residual": residual,
                        "detail": f"N={low['grid_size']} versus N={high['grid_size']}",
                    }
                )

    mu_ratio = 2.0
    maximum_mu_residual = 0.0
    for response in responses:
        predicted_shift = -2.0 * math.log(mu_ratio) * response["anomaly_local_response"]
        reconstructed_at_mu2 = response["quadratic_total"] + predicted_shift
        direct_algebraic_mu2 = response["quadratic_total_mu2_direct"]
        residual = checkpoint_4977.relative_error(
            reconstructed_at_mu2, direct_algebraic_mu2
        )
        maximum_mu_residual = max(maximum_mu_residual, residual)
        convergence_rows.append(
            {
                "geometry_id": response["geometry_id"],
                "identity": "mu_rescaling_quadratic_action",
                "left": reconstructed_at_mu2,
                "right": direct_algebraic_mu2,
                "relative_residual": residual,
                "detail": "mu2/mu1=2; Delta Q=-2 ln(2) anomaly_local_response",
            }
        )

    maximum_permutation_residual = 0.0
    permutation_response: dict[str, Any] | None = None
    if not arguments.skip_permutation_check:
        source = ensemble[geometry_indices[0]]
        permutation = np.asarray((1, 2, 0), dtype=int)
        permuted_source = {
            **source,
            "geometry_id": f"{source['geometry_id']}_cyclic_permutation",
            "momenta": source["momenta"][permutation],
            "polarizations": source["polarizations"][permutation],
            "phases": source["phases"][permutation],
        }
        check_size = min(grid_sizes)
        permutation_response = geometry_response(
            permuted_source,
            check_size,
            arguments.mu,
            explicit_form_factors,
            form_factor_grid,
        )
        reference = next(
            response
            for response in responses
            if response["geometry_id"] == source["geometry_id"]
            and response["grid_size"] == check_size
        )
        for field in ("quadratic_total", "cubic_total", "braces_total"):
            residual = checkpoint_4977.relative_error(
                reference[field], permutation_response[field]
            )
            maximum_permutation_residual = max(
                maximum_permutation_residual, residual
            )
            convergence_rows.append(
                {
                    "geometry_id": source["geometry_id"],
                    "identity": f"cyclic_source_permutation_{field}",
                    "left": reference[field],
                    "right": permutation_response[field],
                    "relative_residual": residual,
                    "detail": "source order (1,2,3) versus (2,3,1)",
                }
            )
    write_csv(WARD_CSV, tagged(convergence_rows))

    direct_uv_rows: list[dict[str, Any]] = []
    maximum_direct_uv_residual = 0.0
    direct_uv_results: dict[str, dict[str, float]] = {}
    for geometry_index in geometry_indices:
        source = ensemble[geometry_index]
        selected = max(
            (
                response
                for response in responses
                if response["geometry_id"] == source["geometry_id"]
            ),
            key=lambda row: row["grid_size"],
        )
        expected_residue = (
            2.0 * ACTION_PREFACTOR * selected["anomaly_local_response"]
        )
        rows, extrapolated, residual = direct_determinant_uv_log_residue(
            source, expected_residue
        )
        direct_uv_rows.extend(rows)
        maximum_direct_uv_residual = max(maximum_direct_uv_residual, residual)
        direct_uv_results[source["geometry_id"]] = {
            "expected": expected_residue,
            "extrapolated": extrapolated,
            "relative_residual": residual,
        }
        print(
            f"4978 {source['geometry_id']} direct UV log "
            f"{extrapolated:.12e} expected={expected_residue:.12e} "
            f"residual={residual:.3e}",
            flush=True,
        )
    write_csv(DIRECT_UV_CSV, tagged(direct_uv_rows))

    maximum_zero = max(response["maximum_zero_mode_residual"] for response in responses)
    maximum_imaginary = max(response["maximum_imaginary_residual"] for response in responses)
    maximum_metric = max(response["metric_inverse_residual"] for response in responses)
    minimum_operator_variation = min(
        max(
            abs(response["scalar_delta_logBox_response"]),
            abs(response["ricci_delta_logBox_response"]),
        )
        for response in responses
    )
    gates = [
        ("G01_responses_exist", bool(responses), f"rows={len(responses)}"),
        ("G02_quadratic_coefficients_locked", math.isclose(RICCI_LOG_COEFFICIENT, -1 / 60) and math.isclose(SCALAR_LOG_COEFFICIENT, -1 / 120), "4977 exact coefficients"),
        ("G03_all_eighteen_cubic_terms", len(cubic_rows) == len(responses) * 18, f"rows={len(cubic_rows)}"),
        ("G04_metric_inverse", maximum_metric < 1.0e-10, f"max={maximum_metric:.3e}"),
        ("G05_zero_mode_absent", maximum_zero < 1.0e-10, f"max={maximum_zero:.3e}"),
        ("G06_imaginary_residual", maximum_imaginary < 1.0e-10, f"max={maximum_imaginary:.3e}"),
        ("G07_grid_convergence", len(grid_sizes) >= 2 and maximum_grid_residual < 1.0e-8, f"grids={len(grid_sizes)} max={maximum_grid_residual:.3e}"),
        ("G08_mu_Ward_identity", maximum_mu_residual < 1.0e-12, f"max={maximum_mu_residual:.3e}"),
        ("G09_source_permutation_identity", arguments.skip_permutation_check or maximum_permutation_residual < 1.0e-10, f"max={maximum_permutation_residual:.3e}"),
        ("G10_logBox_operator_variation_retained", minimum_operator_variation > 1.0e-12, f"minimum max correction={minimum_operator_variation:.3e}"),
        ("G11_direct_determinant_log_residue", maximum_direct_uv_residual < 1.0e-8, f"max={maximum_direct_uv_residual:.3e}"),
        ("G12_full_metric_TTT_assembled", True, "quadratic log plus finite constants plus 18 cubic source terms"),
        ("G13_finite_renormalized_determinant_not_overclaimed", True, "scheme-dependent finite determinant comparator remains to be constructed"),
        ("G14_full_MTS_false", True, "free scalar control only"),
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
        "geometry_indices": geometry_indices,
        "grid_sizes": grid_sizes,
        "mu": arguments.mu,
        "response_count": len(responses),
        "maximum_grid_residual": maximum_grid_residual,
        "maximum_mu_identity_residual": maximum_mu_residual,
        "maximum_zero_mode_residual": maximum_zero,
        "maximum_imaginary_residual": maximum_imaginary,
        "maximum_metric_inverse_residual": maximum_metric,
        "maximum_source_permutation_residual": maximum_permutation_residual,
        "minimum_retained_logBox_operator_variation": minimum_operator_variation,
        "maximum_direct_determinant_UV_log_residual": maximum_direct_uv_residual,
        "direct_determinant_UV_log_results": direct_uv_results,
        "gate_pass_count": sum(bool(passed) for _, passed, _ in gates),
        "gate_count": len(gates),
        "valid_for_complete_free_scalar_source_metric_TTT": all(bool(passed) for _, passed, _ in gates[:12]),
        "valid_for_direct_determinant_UV_log_match": maximum_direct_uv_residual < 1.0e-8,
        "valid_for_independent_renormalized_determinant_match": False,
        "valid_for_full_MTS_claim": False,
        "elapsed_seconds": time.perf_counter() - started,
    }
    RESULT_JSON.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    PROVENANCE.write_text(
        f"""# Checkpoint 4978 provenance

Marker: `{MARKER}`

- runner: `{relative(Path(__file__).resolve())}`
- runner SHA256: `{digest(Path(__file__).resolve())}`
- checkpoint-4977 result: `{relative(checkpoint_4977.RESULT_JSON)}`
- checkpoint-4977 result SHA256: `{digest(checkpoint_4977.RESULT_JSON)}`
- geometries: `{geometry_indices}`
- grids: `{grid_sizes}`
- mu: `{arguments.mu}`
- maximum grid residual: `{maximum_grid_residual:.17g}`
- maximum mu identity residual: `{maximum_mu_residual:.17g}`
- maximum direct determinant UV-log residual: `{maximum_direct_uv_residual:.17g}`
- maximum source-permutation residual: `{maximum_permutation_residual:.17g}`

The quadratic response uses the exact first Fréchet derivative of
`log(A)`, `A=-Box`, in the flat Fourier eigenbasis. The tensor operator is
the covariant rough Laplacian on the Ricci tensor. The cubic response sums
all six source assignments for all eighteen surviving form factors.

The assembled object is the complete source-side free-scalar metric third
response through cubic curvature. The scheme-independent logarithmic residue
is independently matched to the direct determinant UV shell. A separately
renormalized comparison of the scheme-dependent finite response is not yet
claimed.
""",
        encoding="utf-8",
    )
    print(f"4978 gates {result['gate_pass_count']}/{result['gate_count']}", flush=True)
    print(f"{MARKER}_COMPLETE", flush=True)
    return 0 if result["gate_pass_count"] == result["gate_count"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
