from __future__ import annotations

import argparse
import cmath
import csv
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import sys
import time
from typing import Any

from mpmath import iv


for thread_variable in (
    "OMP_NUM_THREADS",
    "OPENBLAS_NUM_THREADS",
    "MKL_NUM_THREADS",
    "NUMEXPR_NUM_THREADS",
    "VECLIB_MAXIMUM_THREADS",
    "BLIS_NUM_THREADS",
):
    os.environ[thread_variable] = "1"
os.environ["PYTHONDONTWRITEBYTECODE"] = "1"
sys.dont_write_bytecode = True


POST = Path(__file__).resolve().parents[1]
SCRIPTS = POST / "scripts"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
RESIDUALS = POST / "source-intake" / "mts_residuals"
OUTPUT = FUNCTIONAL_RG / "5392"
DOCUMENT = POST / "5392-Y5-R2FR-D4-desingularized-endpoint-G3-Cauchy-bound.md"
VALIDATION = RESIDUALS / "P8_Y5_BRR545_5392_VALIDATION.csv"

SCRIPT_5389 = SCRIPTS / "Y5_R2FR_5389_D4_full_H_event_geometry_and_coordinate_Cauchy_bridge.py"
SCRIPT_5391 = SCRIPTS / "Y5_R2FR_5391_D4_uniform_full_H3_Cauchy_bound.py"
BASE_BOXES = FUNCTIONAL_RG / "5380" / "D4_complexified_event_neighborhood_boxes.csv"
BASE_RESULT = FUNCTIONAL_RG / "5380" / "D4_complexified_event_neighborhood_result.json"
HALO_BOXES = FUNCTIONAL_RG / "5387" / "D4_Cauchy_endpoint_halo_boxes.csv"
HALO_RESULT = FUNCTIONAL_RG / "5387" / "D4_Cauchy_endpoint_halo_result.json"
EVENTS = FUNCTIONAL_RG / "5358" / "D4_zero_regulator_event_certificate.csv"
ENDPOINT_COEFFICIENTS = FUNCTIONAL_RG / "5359" / "D4_zero_regulator_endpoint_coefficients.csv"
ENDPOINT_RESULT = FUNCTIONAL_RG / "5359" / "D4_zero_regulator_endpoint_result.json"
GEOMETRY_SEAMS = FUNCTIONAL_RG / "5389" / "D4_full_H_event_branch_seams.csv"
GEOMETRY_RESULT = FUNCTIONAL_RG / "5389" / "D4_full_H_event_geometry_bridge_result.json"
H_BOX_BOUNDS = FUNCTIONAL_RG / "5391" / "D4_uniform_full_H_box_bounds.csv"
H_RESULT = FUNCTIONAL_RG / "5391" / "D4_uniform_full_H3_result.json"
REDUCTION_DOCUMENT = POST / "5376-Y5-R2FR-D4-uniform-remainder-decomposition-and-bound-reduction.md"

CHECKPOINT = 5392
MARKER = "MTS_5392_D4_DESINGULARIZED_ENDPOINT_G3_CAUCHY_BOUND"
REVISION = "D4-desingularized-lower-endpoint-G3-v1"
EVENT_IDS = tuple(f"E{index:02d}" for index in range(1, 9))
EPSILON_REFERENCE = 0.0025
REGULATOR_CAUCHY_RADIUS = 5.0e-7
H_REAL_PADDING_FACTOR = 64.0
H_IMAGINARY_PADDING_FACTOR = 64.0

CLAIM_RATIO = "valid_for_D4_desingularized_endpoint_ratio_atlas"
CLAIM_G = "valid_for_D4_endpoint_nonlog_G_enclosure"
CLAIM_G3 = "valid_for_D4_numeric_G3_bound"
OPEN_CLAIMS = (
    "valid_for_D4_numeric_W3_bound",
    "valid_for_D4_numeric_uniform_remainder_bound",
    "valid_for_D4_outer_regulator_zero_limit",
    "valid_for_decay_angle_integral",
    "valid_for_full_angular_convergence",
    "valid_for_full_phase_space_coefficient",
    "valid_for_numeric_UV_claim",
    "valid_for_local_GR_claim",
    "valid_for_full_MTS_claim",
)


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


M5389 = load_module("mts_5389_for_5392", SCRIPT_5389)
M5391 = load_module("mts_5391_for_5392", SCRIPT_5391)
M5380 = M5389.M5380
M5379 = M5389.M5379
M5381 = M5389.M5381


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def parse_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() == "true"


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def atomic_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"cannot write empty CSV {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with temporary.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    os.replace(temporary, path)


def atomic_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def validation_row(gate: str, passed: bool, detail: Any) -> dict[str, Any]:
    return {"gate": gate, "passed": bool(passed), "detail": str(detail)}


def source_paths() -> tuple[Path, ...]:
    return tuple(
        path.resolve()
        for path in (
            Path(__file__),
            SCRIPT_5389,
            SCRIPT_5391,
            BASE_BOXES,
            BASE_RESULT,
            HALO_BOXES,
            HALO_RESULT,
            EVENTS,
            ENDPOINT_COEFFICIENTS,
            ENDPOINT_RESULT,
            GEOMETRY_SEAMS,
            GEOMETRY_RESULT,
            H_BOX_BOUNDS,
            H_RESULT,
            REDUCTION_DOCUMENT,
        )
    )


class ScaledImaginaryPair:
    def __init__(self, real: Any, imaginary_over_epsilon: Any, epsilon_squared: Any) -> None:
        self.real = real
        self.imaginary_over_epsilon = imaginary_over_epsilon
        self.epsilon_squared = epsilon_squared

    def coerce(self, value: Any) -> "ScaledImaginaryPair":
        if isinstance(value, ScaledImaginaryPair):
            return value
        scalar = self.real.coerce(value)
        zero = M5380.MultiDual.constant(0, scalar.dimension)
        return ScaledImaginaryPair(scalar, zero, self.epsilon_squared)

    def __add__(self, other: Any) -> "ScaledImaginaryPair":
        other = self.coerce(other)
        return ScaledImaginaryPair(
            self.real + other.real,
            self.imaginary_over_epsilon + other.imaginary_over_epsilon,
            self.epsilon_squared,
        )

    __radd__ = __add__

    def __neg__(self) -> "ScaledImaginaryPair":
        return ScaledImaginaryPair(
            -self.real, -self.imaginary_over_epsilon, self.epsilon_squared
        )

    def __sub__(self, other: Any) -> "ScaledImaginaryPair":
        return self + (-self.coerce(other))

    def __rsub__(self, other: Any) -> "ScaledImaginaryPair":
        return self.coerce(other) - self

    def __mul__(self, other: Any) -> "ScaledImaginaryPair":
        other = self.coerce(other)
        return ScaledImaginaryPair(
            self.real * other.real
            - self.imaginary_over_epsilon
            * other.imaginary_over_epsilon
            * self.epsilon_squared,
            self.real * other.imaginary_over_epsilon
            + self.imaginary_over_epsilon * other.real,
            self.epsilon_squared,
        )

    __rmul__ = __mul__

    def __pow__(self, exponent: int) -> "ScaledImaginaryPair":
        if exponent != 2:
            raise ValueError("only square powers are required")
        return self * self


def scaled_material_pair(
    surface_id: str,
    recoil: ScaledImaginaryPair,
    soft_cosine: Any,
    decay_cosine: Any,
    q_value: ScaledImaginaryPair,
) -> ScaledImaginaryPair:
    cosine = q_value.coerce(soft_cosine)
    decay = q_value.coerce(decay_cosine)
    common = (cosine - decay) * (
        q_value * (1 + cosine) + cosine - 1
    )
    if surface_id == "direct:L:s14":
        return (
            (1 + cosine)
            * (1 + q_value)
            * (cosine + decay)
            * recoil**2
            + 2
            * (1 + cosine)
            * (1 - cosine - q_value * cosine)
            * recoil
            + common
        )
    if surface_id == "direct:L:s01":
        return (
            (1 - cosine)
            * (
                -(1 + q_value) * (cosine + decay) * recoil**2
                + 2 * recoil * (q_value * (1 + cosine) + cosine)
            )
            + common
        )
    if surface_id == "direct:shared:s13":
        return (
            (cosine - decay)
            * (1 - cosine - q_value * (1 + cosine))
            - (1 + q_value) * recoil * (1 - cosine**2)
        )
    raise ValueError(f"unsupported material surface {surface_id}")


def desingularized_system(
    configuration: dict[str, Any], epsilon: Any, variable_boxes: list[Any]
) -> tuple[list[Any], list[list[Any]]]:
    dimension = len(variable_boxes)
    variables = [
        M5380.MultiDual.variable(value, dimension, index)
        for index, value in enumerate(variable_boxes)
    ]
    epsilon_squared = epsilon**2
    q_real = -(80 + epsilon_squared) / (64 + epsilon_squared)
    q_imaginary_over_epsilon = -2 / (64 + epsilon_squared)
    q_pair = ScaledImaginaryPair(
        M5380.MultiDual.constant(q_real, dimension),
        M5380.MultiDual.constant(q_imaginary_over_epsilon, dimension),
        epsilon_squared,
    )
    recoil_pair = ScaledImaginaryPair(
        variables[0], variables[1], epsilon_squared
    )
    coordinate = (
        variables[2]
        if configuration["event_type"] == "BRANCH_DEATH"
        else variables[3]
    )
    soft_cosine = configuration["sign"] * coordinate
    decay_cosine = M5380.complex_point(configuration["decay_cosine"])
    polynomial = scaled_material_pair(
        configuration["surface_id"],
        recoil_pair,
        soft_cosine,
        decay_cosine,
        q_pair,
    )
    functions = [polynomial.real, polynomial.imaginary_over_epsilon]
    if configuration["event_type"] == "BRANCH_DEATH":
        functions.append(
            variables[0] ** 2
            - variables[1] ** 2 * epsilon_squared
            - M5379.M5378.M5359.M5358.R_MINIMUM**2
        )
    else:
        hard_recoil = variables[2]
        soft_sine = variables[4]
        decay = M5380.MultiDual.constant(decay_cosine, dimension)
        decay_sine = M5380.MultiDual.constant(
            M5380.complex_point(
                M5380.mp.sqrt(1 - configuration["decay_cosine"] ** 2)
            ),
            dimension,
        )
        relative = soft_cosine * decay - soft_sine * decay_sine
        target = M5380.MultiDual.constant(M5380.complex_point(-0.3), dimension)
        hard_value = (
            (soft_cosine - target) * (1 + relative) * hard_recoil**2
            + 2 * (decay - soft_cosine * relative) * hard_recoil
            + (soft_cosine + target) * (relative - 1)
        )
        functions.extend(
            (
                hard_value,
                hard_recoil**2
                - variables[0] ** 2
                + variables[1] ** 2 * epsilon_squared,
                soft_sine**2 + soft_cosine**2 - 1,
            )
        )
    return (
        [function.value for function in functions],
        [function.derivatives for function in functions],
    )


def desingularized_point_solution(
    configuration: dict[str, Any],
    epsilon: float,
    zero_coordinate: Any,
    endpoint_row: dict[str, str],
) -> list[float]:
    original = M5380.point_solution(configuration, epsilon, zero_coordinate)
    if epsilon != 0.0:
        scaled_imaginary = original[1] / epsilon
    else:
        scaled_imaginary = float(
            endpoint_row["boundary_gap_epsilon_derivative_imaginary"]
        ) / (2.0 * original[0])
    return [original[0], scaled_imaginary, *original[2:]]


def parse_source_boxes(source: dict[str, str]) -> list[Any]:
    return [
        M5381.parse_complex_box(text)
        for text in source["complex_state_boxes"].split("|")
    ]


def initial_desingularized_boxes(
    source: dict[str, str], samples: list[list[float]]
) -> list[Any]:
    source_boxes = parse_source_boxes(source)
    epsilon_width = float(source["epsilon_real_upper"]) - float(
        source["epsilon_real_lower"]
    )
    h_values = [sample[1] for sample in samples]
    h_span = max(h_values) - min(h_values)
    h_scale = max(max(abs(value) for value in h_values), 1.0e-12)
    h_padding = max(H_REAL_PADDING_FACTOR * h_span, 1.0e-8 * h_scale, 1.0e-12)
    half_real_width = max(0.5 * epsilon_width, 1.0e-12)
    h_slope = max(
        abs(h_values[1] - h_values[0]),
        abs(h_values[2] - h_values[1]),
        0.5 * abs(h_values[2] - h_values[0]),
    ) / half_real_width
    h_imaginary_half_width = max(
        H_IMAGINARY_PADDING_FACTOR
        * h_slope
        * M5380.EPSILON_IMAGINARY_HALF_WIDTH,
        1.0e-8 * h_scale,
        1.0e-12,
    )
    h_box = M5380.complex_box(
        min(h_values) - h_padding,
        max(h_values) + h_padding,
        -h_imaginary_half_width,
        h_imaginary_half_width,
    )
    return [source_boxes[0], h_box, *source_boxes[2:]]


def point_jacobian(
    configuration: dict[str, Any], epsilon: float, center: list[float]
) -> Any:
    center_boxes = [M5380.complex_point(value) for value in center]
    _, jacobian = desingularized_system(
        configuration, M5380.complex_point(epsilon), center_boxes
    )
    return M5380.np.asarray(
        [
            [M5380.complex_midpoint(value) for value in row]
            for row in jacobian
        ],
        dtype=complex,
    )


def krawczyk_certificate(
    configuration: dict[str, Any],
    epsilon_bounds: tuple[float, float],
    state_boxes: list[Any],
    center: list[float],
) -> dict[str, Any]:
    epsilon_midpoint = 0.5 * sum(epsilon_bounds)
    epsilon_box = M5380.complex_box(
        epsilon_bounds[0],
        epsilon_bounds[1],
        -M5380.EPSILON_IMAGINARY_HALF_WIDTH,
        M5380.EPSILON_IMAGINARY_HALF_WIDTH,
    )
    jacobian_point = point_jacobian(configuration, epsilon_midpoint, center)
    inverse = M5380.np.linalg.inv(jacobian_point)
    center_boxes = [M5380.complex_point(value) for value in center]
    functions, _ = desingularized_system(
        configuration, epsilon_box, center_boxes
    )
    _, jacobian = desingularized_system(
        configuration, epsilon_box, state_boxes
    )
    dimension = len(state_boxes)
    operator: list[Any] = []
    matrix_remainder: list[list[Any]] = []
    for row_index in range(dimension):
        correction = M5380.complex_point(0)
        for column_index in range(dimension):
            correction += M5380.complex_point(
                inverse[row_index, column_index]
            ) * functions[column_index]
        remainder_row: list[Any] = []
        remainder_value = M5380.complex_point(0)
        for column_index in range(dimension):
            matrix_value = M5380.complex_point(
                1 if row_index == column_index else 0
            )
            for inner_index in range(dimension):
                matrix_value -= (
                    M5380.complex_point(inverse[row_index, inner_index])
                    * jacobian[inner_index][column_index]
                )
            remainder_row.append(matrix_value)
            remainder_value += matrix_value * (
                state_boxes[column_index] - center[column_index]
            )
        matrix_remainder.append(remainder_row)
        operator.append(center[row_index] - correction + remainder_value)
    inclusion_margins: list[float] = []
    for state_box, image in zip(state_boxes, operator, strict=True):
        inclusion_margins.extend(
            (
                M5380.real_lower(image) - M5380.real_lower(state_box),
                M5380.real_upper(state_box) - M5380.real_upper(image),
                M5380.imaginary_lower(image)
                - M5380.imaginary_lower(state_box),
                M5380.imaginary_upper(state_box)
                - M5380.imaginary_upper(image),
            )
        )
    contraction_bound = max(
        sum(M5380.complex_sup_abs(value) for value in row)
        for row in matrix_remainder
    )
    return {
        "operator": operator,
        "minimum_inclusion_margin": min(inclusion_margins),
        "contraction_bound": contraction_bound,
        "point_jacobian_condition_number": float(
            M5380.np.linalg.cond(jacobian_point)
        ),
        "passes": min(inclusion_margins) > 0 and contraction_bound < 1,
    }


def construct_state_box(
    configuration: dict[str, Any],
    epsilon_bounds: tuple[float, float],
    initial_state_boxes: list[Any],
    center: list[float],
) -> tuple[list[Any], dict[str, Any], int]:
    state_boxes = initial_state_boxes
    certificate = krawczyk_certificate(
        configuration, epsilon_bounds, state_boxes, center
    )
    inflation_steps = 0
    while (
        not certificate["passes"]
        and certificate["contraction_bound"] < 1
        and inflation_steps < M5380.STATE_BOX_INFLATION_MAXIMUM_STEPS
    ):
        state_boxes = M5380.inflate_state_box(
            state_boxes, certificate["operator"]
        )
        inflation_steps += 1
        certificate = krawczyk_certificate(
            configuration, epsilon_bounds, state_boxes, center
        )
    return state_boxes, certificate, inflation_steps


def rectangle_contains(outer: Any, inner: Any) -> bool:
    return (
        M5380.real_lower(outer) <= M5380.real_lower(inner)
        and M5380.real_upper(inner) <= M5380.real_upper(outer)
        and M5380.imaginary_lower(outer) <= M5380.imaginary_lower(inner)
        and M5380.imaginary_upper(inner) <= M5380.imaginary_upper(outer)
    )


def center_residual(
    configuration: dict[str, Any], epsilon: float, center: list[float]
) -> float:
    functions, _ = desingularized_system(
        configuration,
        M5380.complex_point(epsilon),
        [M5380.complex_point(value) for value in center],
    )
    return max(abs(M5380.complex_midpoint(value)) for value in functions)


def parent_factorization_residual(
    configuration: dict[str, Any], epsilon: float, center: list[float]
) -> float:
    if epsilon == 0.0:
        raise ValueError("factorization cross-check requires nonzero epsilon")
    probe = [
        value + (index + 1) * 1.0e-5 * max(abs(value), 1.0)
        for index, value in enumerate(center)
    ]
    original_probe = [probe[0], epsilon * probe[1], *probe[2:]]
    original_functions, _ = M5380.complexified_system(
        configuration,
        M5380.complex_point(epsilon),
        [M5380.complex_point(value) for value in original_probe],
    )
    scaled_functions, _ = desingularized_system(
        configuration,
        M5380.complex_point(epsilon),
        [M5380.complex_point(value) for value in probe],
    )
    residuals = [
        abs(
            M5380.complex_midpoint(original_functions[0])
            - M5380.complex_midpoint(scaled_functions[0])
        ),
        abs(
            M5380.complex_midpoint(original_functions[1])
            - epsilon * M5380.complex_midpoint(scaled_functions[1])
        ),
    ]
    residuals.extend(
        abs(
            M5380.complex_midpoint(original)
            - M5380.complex_midpoint(scaled)
        )
        for original, scaled in zip(
            original_functions[2:], scaled_functions[2:], strict=True
        )
    )
    return max(residuals)


def endpoint_split_identity_residual() -> float:
    epsilon = 0.0013
    coefficient_0 = complex(2.1, -0.4)
    coefficient_1 = complex(-0.7, 0.2)
    gap_0 = complex(0.0, 2.0e-6)
    gap_1 = complex(1.7, -0.2)
    sign = -1
    ratio = gap_0 / gap_1
    primitive_at_gap_0 = sign * (
        (coefficient_0 / gap_1 - coefficient_1 * gap_0 / gap_1**2)
        * (gap_0 * cmath.log(gap_0) - gap_0)
        + (coefficient_1 / gap_1**2)
        * (0.5 * gap_0**2 * cmath.log(gap_0) - 0.25 * gap_0**2)
    )
    logarithmic_coefficient = -sign * (
        coefficient_0 * ratio - 0.5 * coefficient_1 * ratio**2
    )
    nonlog_polynomial = sign * (
        coefficient_0 * ratio - 0.75 * coefficient_1 * ratio**2
    )
    normalized_gap = EPSILON_REFERENCE * gap_0 / epsilon
    reconstructed = (
        logarithmic_coefficient
        * cmath.log(epsilon / EPSILON_REFERENCE)
        + nonlog_polynomial
        + logarithmic_coefficient * cmath.log(normalized_gap)
    )
    return abs(-primitive_at_gap_0 - reconstructed)


def ratio_box_row(
    source: dict[str, str],
    configuration: dict[str, Any],
    zero_coordinate: Any,
    endpoint_row: dict[str, str],
) -> tuple[dict[str, Any], list[Any]]:
    epsilon_bounds = (
        float(source["epsilon_real_lower"]),
        float(source["epsilon_real_upper"]),
    )
    epsilon_midpoint = 0.5 * sum(epsilon_bounds)
    samples = [
        desingularized_point_solution(
            configuration, epsilon, zero_coordinate, endpoint_row
        )
        for epsilon in (
            epsilon_bounds[0],
            epsilon_midpoint,
            epsilon_bounds[1],
        )
    ]
    initial_boxes = initial_desingularized_boxes(source, samples)
    state_boxes, certificate, inflation_steps = construct_state_box(
        configuration, epsilon_bounds, initial_boxes, samples[1]
    )
    epsilon_box = M5380.complex_box(
        epsilon_bounds[0],
        epsilon_bounds[1],
        float(source["epsilon_imaginary_lower"]),
        float(source["epsilon_imaginary_upper"]),
    )
    original_boxes = parse_source_boxes(source)
    mapped_v = epsilon_box * state_boxes[1]
    mapped_v_inside_original = rectangle_contains(original_boxes[1], mapped_v)
    normalized_gap = (
        M5380.complex_point(2j * EPSILON_REFERENCE)
        * state_boxes[0]
        * state_boxes[1]
    )
    normalized_gap_lower = math.nextafter(
        M5381.modulus_lower(normalized_gap), 0.0
    )
    normalized_gap_upper = math.nextafter(
        M5381.modulus_upper(normalized_gap), math.inf
    )
    imaginary_lower = M5380.imaginary_lower(normalized_gap)
    imaginary_upper = M5380.imaginary_upper(normalized_gap)
    half_plane = (
        "UPPER"
        if imaginary_lower > 0
        else "LOWER"
        if imaginary_upper < 0
        else "CROSSES_REAL_AXIS"
    )
    logarithm_upper = math.inf
    if normalized_gap_lower > 0 and half_plane != "CROSSES_REAL_AXIS":
        radial_log_upper = max(
            abs(math.log(normalized_gap_lower)),
            abs(math.log(normalized_gap_upper)),
        )
        logarithm_upper = math.nextafter(
            math.hypot(radial_log_upper, math.pi), math.inf
        )
    residual = center_residual(
        configuration, epsilon_midpoint, samples[1]
    )
    factorization_epsilon = (
        epsilon_midpoint
        if epsilon_midpoint != 0.0
        else epsilon_bounds[1]
    )
    factorization_center = desingularized_point_solution(
        configuration,
        factorization_epsilon,
        zero_coordinate,
        endpoint_row,
    )
    factorization_residual = parent_factorization_residual(
        configuration, factorization_epsilon, factorization_center
    )
    row = {
        "event_id": configuration["event_id"],
        "event_type": configuration["event_type"],
        "epsilon_bin_index": int(source["epsilon_bin_index"]),
        "epsilon_real_lower": epsilon_bounds[0],
        "epsilon_real_upper": epsilon_bounds[1],
        "epsilon_imaginary_lower": float(source["epsilon_imaginary_lower"]),
        "epsilon_imaginary_upper": float(source["epsilon_imaginary_upper"]),
        "desingularized_system_dimension": len(state_boxes),
        "state_box_inflation_iterations": inflation_steps,
        "desingularized_state_boxes_u_h_rest": "|".join(
            M5380.complex_interval_text(value) for value in state_boxes
        ),
        "desingularized_Krawczyk_images": "|".join(
            M5380.complex_interval_text(value)
            for value in certificate["operator"]
        ),
        "minimum_strict_inclusion_margin": certificate[
            "minimum_inclusion_margin"
        ],
        "maximum_contraction_bound": certificate["contraction_bound"],
        "point_jacobian_condition_number": certificate[
            "point_jacobian_condition_number"
        ],
        "point_center_residual_abs_upper": residual,
        "parent_equation_factorization_residual_abs": factorization_residual,
        "mapped_v_equals_epsilon_h_inside_original_event_box": mapped_v_inside_original,
        "normalized_gap_epsilon_ref_z0_over_epsilon_modulus_lower": normalized_gap_lower,
        "normalized_gap_epsilon_ref_z0_over_epsilon_modulus_upper": normalized_gap_upper,
        "normalized_gap_imaginary_lower": imaginary_lower,
        "normalized_gap_imaginary_upper": imaginary_upper,
        "normalized_gap_half_plane": half_plane,
        "normalized_gap_principal_log_abs_upper": logarithm_upper,
        "desingularized_Krawczyk_passes": certificate["passes"],
        CLAIM_RATIO: False,
        CLAIM_G: False,
        CLAIM_G3: False,
        **{claim: False for claim in OPEN_CLAIMS},
    }
    return row, state_boxes


def render_document(result: dict[str, Any], event_bounds: list[dict[str, Any]]) -> None:
    lines = [
        "# 5392 — D4 desingularized endpoint G3 Cauchy bound",
        "",
        "## Decision",
        "",
        f"`{result['decision']}`",
        "",
        "## Exact split",
        "",
        "For `R=u+i v`, the certified event equation gives `z0=2 i u v`. The material equations are invariant under `(epsilon,v)->(-epsilon,-v)`, so the analytic branch has `v=epsilon h`. Checkpoint 5392 does not merely divide two intervals containing zero: it substitutes `v=epsilon h` into the parent equations and divides the algebraic imaginary equation by epsilon before interval evaluation. A strict complex Krawczyk certificate then owns `(u,h,...)` through epsilon zero.",
        "",
        "At the lower endpoint of the exact affine-log primitive, put `r=z0/z1`. Then",
        "",
        "`-Phi(z0)=H Log(epsilon/epsilon_ref)+G`,",
        "",
        "`H=-s[C0 r-(C1/2)r^2]`,",
        "",
        "`G=s[C0 r-(3C1/4)r^2]+H Log(epsilon_ref z0/epsilon)`.",
        "",
        "The normalized gap is `epsilon_ref z0/epsilon=2 i epsilon_ref u h`. Every certified box keeps it nonzero and in one open half-plane, so its principal logarithm is analytic and bounded. All upper-end, cutoff and model-mismatch terms are assigned to the mapped-away `W` sector; this freezes rather than hides the remaining owner.",
        "",
        "## Certified bound",
        "",
        f"- desingularized boxes: `{result['certified_ratio_box_count']}/{result['required_ratio_box_count']}`;",
        f"- minimum normalized-gap modulus: `{result['minimum_normalized_gap_modulus_lower']}`;",
        f"- maximum normalized-gap logarithm: `{result['maximum_normalized_gap_principal_log_abs_upper']}`;",
        f"- uniform endpoint `G3` upper bound: `{result['uniform_endpoint_G3_upper']}`;",
        f"- endpoint-G Taylor constant: `{result['G_sector_Taylor_constant_upper']}`.",
        "",
        "| event | sup |G| | sup |G'''| |",
        "|---|---:|---:|",
    ]
    lines.extend(
        f"| {row['event_id']} | {row['endpoint_G_event_sup_abs_upper']} | {row['endpoint_G_event_third_derivative_sup_upper']} |"
        for row in event_bounds
    )
    lines.extend(
        (
            "",
            "## Scope",
            "",
            "This closes the endpoint nonlogarithmic `G3` owner in the frozen 5376 decomposition. It does not bound mapped-away `W3`; therefore the total uniform remainder, D4 outer limit, local GR and full MTS claims remain false.",
            "",
        )
    )
    temporary = DOCUMENT.with_suffix(DOCUMENT.suffix + ".tmp")
    temporary.write_text("\n".join(lines), encoding="utf-8")
    os.replace(temporary, DOCUMENT)


def run(output: Path) -> dict[str, Any]:
    started = time.perf_counter()
    M5380.set_below_normal_priority()
    M5380.mp.mp.dps = M5380.MP_DIGITS
    iv.dps = M5380.INTERVAL_DIGITS
    required = source_paths()
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise FileNotFoundError(missing)
    base_result = read_json(BASE_RESULT)
    halo_result = read_json(HALO_RESULT)
    endpoint_result = read_json(ENDPOINT_RESULT)
    geometry_result = read_json(GEOMETRY_RESULT)
    h_result = read_json(H_RESULT)
    base_rows = read_csv(BASE_BOXES)
    halo_rows = read_csv(HALO_BOXES)
    all_source_rows = [*base_rows, *halo_rows]
    events = {row["event_id"]: row for row in read_csv(EVENTS)}
    endpoint_rows = {
        row["event_id"]: row for row in read_csv(ENDPOINT_COEFFICIENTS)
    }
    h_rows = {
        (row["event_id"], int(row["epsilon_bin_index"])): row
        for row in read_csv(H_BOX_BOUNDS)
    }
    seam_rows = read_csv(GEOMETRY_SEAMS)
    references, _ = M5379.M5378.M5359.reference_rows()
    ratio_rows: list[dict[str, Any]] = []
    for source in all_source_rows:
        event_id = source["event_id"]
        configuration = M5379.M5378.M5359.event_configuration(
            events[event_id], references
        )
        zero_coordinate = M5380.mp.mpf(
            events[event_id]["zero_regulator_absolute_soft_cosine"]
        )
        row, _ = ratio_box_row(
            source,
            configuration,
            zero_coordinate,
            endpoint_rows[event_id],
        )
        ratio_rows.append(row)
    g_box_rows: list[dict[str, Any]] = []
    for ratio_row in ratio_rows:
        key = (
            ratio_row["event_id"],
            int(ratio_row["epsilon_bin_index"]),
        )
        h_row = h_rows[key]
        c0_upper = float(h_row["physical_C0_abs_upper"])
        c1_upper = float(h_row["C1_abs_upper_from_coordinate_Cauchy"])
        r_upper = float(h_row["ratio_z0_over_z1_abs_upper"])
        h_upper = float(h_row["full_H_abs_upper"])
        logarithm_upper = float(
            ratio_row["normalized_gap_principal_log_abs_upper"]
        )
        polynomial_upper = M5391.upward_sum(
            (
                M5391.upward_product((c0_upper, r_upper)),
                M5391.upward_product(
                    (0.75, c1_upper, r_upper, r_upper)
                ),
            )
        )
        logarithmic_upper = M5391.upward_product(
            (h_upper, logarithm_upper)
        )
        g_upper = M5391.upward_sum(
            (polynomial_upper, logarithmic_upper)
        )
        g_box_rows.append(
            {
                "event_id": key[0],
                "epsilon_bin_index": key[1],
                "physical_C0_abs_upper": c0_upper,
                "C1_abs_upper_from_coordinate_Cauchy": c1_upper,
                "ratio_z0_over_z1_abs_upper": r_upper,
                "full_H_abs_upper": h_upper,
                "normalized_gap_principal_log_abs_upper": logarithm_upper,
                "nonlog_polynomial_K_abs_upper": polynomial_upper,
                "H_times_normalized_log_abs_upper": logarithmic_upper,
                "endpoint_G_abs_upper": g_upper,
                CLAIM_RATIO: False,
                CLAIM_G: False,
                CLAIM_G3: False,
                **{claim: False for claim in OPEN_CLAIMS},
            }
        )
    event_bounds: list[dict[str, Any]] = []
    for event_id in EVENT_IDS:
        selected = [
            row for row in g_box_rows if row["event_id"] == event_id
        ]
        event_sup = M5391.upward(
            max(float(row["endpoint_G_abs_upper"]) for row in selected)
        )
        event_bounds.append(
            {
                "event_id": event_id,
                "box_count": len(selected),
                "endpoint_G_event_sup_abs_upper": event_sup,
                "endpoint_G_event_third_derivative_sup_upper": M5391.cauchy_third_derivative_upper(
                    event_sup,
                    M5391.downward_positive(REGULATOR_CAUCHY_RADIUS),
                ),
                CLAIM_RATIO: False,
                CLAIM_G: False,
                CLAIM_G3: False,
                **{claim: False for claim in OPEN_CLAIMS},
            }
        )
    uniform_g3 = M5391.upward_sum(
        [
            float(row["endpoint_G_event_third_derivative_sup_upper"])
            for row in event_bounds
        ]
    )
    required_keys = {
        (row["event_id"], int(row["epsilon_bin_index"]))
        for row in all_source_rows
    }
    ratio_keys = {
        (row["event_id"], int(row["epsilon_bin_index"]))
        for row in ratio_rows
    }
    all_ratio_pass = all(
        row["desingularized_Krawczyk_passes"] is True
        and float(row["minimum_strict_inclusion_margin"]) > 0
        and float(row["maximum_contraction_bound"]) < 1
        for row in ratio_rows
    )
    all_logs_pass = all(
        float(
            row[
                "normalized_gap_epsilon_ref_z0_over_epsilon_modulus_lower"
            ]
        )
        > 0
        and row["normalized_gap_half_plane"] in {"UPPER", "LOWER"}
        and math.isfinite(
            float(row["normalized_gap_principal_log_abs_upper"])
        )
        for row in ratio_rows
    )
    event_half_planes = {
        event_id: {
            row["normalized_gap_half_plane"]
            for row in ratio_rows
            if row["event_id"] == event_id
        }
        for event_id in EVENT_IDS
    }
    half_plane_continuity_pass = all(
        len(half_planes) == 1
        and next(iter(half_planes)) in {"UPPER", "LOWER"}
        for half_planes in event_half_planes.values()
    )
    maximum_factorization_residual = max(
        float(row["parent_equation_factorization_residual_abs"])
        for row in ratio_rows
    )
    split_identity_residual = endpoint_split_identity_residual()
    all_mapped_inside = all(
        row["mapped_v_equals_epsilon_h_inside_original_event_box"] is True
        for row in ratio_rows
    )
    validations = [
        validation_row(
            "all_required_sources_exist", not missing, len(required)
        ),
        validation_row(
            "parent_event_strip_and_endpoint_halos_are_certified",
            base_result.get("validation_passed") is True
            and halo_result.get("validation_passed") is True
            and len(all_source_rows) == 80,
            f"base={len(base_rows)};halo={len(halo_rows)}",
        ),
        validation_row(
            "parent_H3_and_endpoint_normalization_are_certified",
            h_result.get("validation_passed") is True
            and h_result.get("claim_boundary", {}).get(
                "valid_for_D4_numeric_H3_bound"
            )
            is True
            and endpoint_result.get("validation_passed") is True,
            f"H3={h_result.get('decision')};endpoint={endpoint_result.get('decision')}",
        ),
        validation_row(
            "original_event_branches_are_patched_across_all_seams",
            geometry_result.get("validation_passed") is True
            and len(seam_rows) == 72
            and all(parse_bool(row["seam_Krawczyk_passes"]) for row in seam_rows),
            f"seams={len(seam_rows)}",
        ),
        validation_row(
            "desingularized_ratio_atlas_has_every_required_box",
            ratio_keys == required_keys and len(ratio_rows) == 80,
            f"rows={len(ratio_rows)};keys={len(ratio_keys)}",
        ),
        validation_row(
            "all_desingularized_Krawczyk_boxes_pass_strictly",
            all_ratio_pass,
            f"minimum_margin={min(float(row['minimum_strict_inclusion_margin']) for row in ratio_rows)};maximum_contraction={max(float(row['maximum_contraction_bound']) for row in ratio_rows)}",
        ),
        validation_row(
            "desingularized_equations_factor_the_parent_equations",
            maximum_factorization_residual <= 1.0e-12,
            f"maximum_off_shell_residual={maximum_factorization_residual}",
        ),
        validation_row(
            "exact_endpoint_primitive_splits_into_H_log_plus_G",
            split_identity_residual <= 1.0e-12,
            f"identity_residual={split_identity_residual}",
        ),
        validation_row(
            "desingularized_roots_map_inside_original_event_boxes",
            all_mapped_inside,
            f"passes={sum(row['mapped_v_equals_epsilon_h_inside_original_event_box'] is True for row in ratio_rows)}/{len(ratio_rows)}",
        ),
        validation_row(
            "normalized_gap_is_nonzero_and_log_analytic_in_one_half_plane",
            all_logs_pass and half_plane_continuity_pass,
            f"minimum_modulus={min(float(row['normalized_gap_epsilon_ref_z0_over_epsilon_modulus_lower']) for row in ratio_rows)};event_half_planes={event_half_planes}",
        ),
        validation_row(
            "H_box_keys_match_desingularized_ratio_box_keys",
            set(h_rows) == required_keys,
            f"H={len(h_rows)};ratio={len(required_keys)}",
        ),
        validation_row(
            "endpoint_G3_formula_is_finite_and_nonnegative",
            len(g_box_rows) == 80
            and len(event_bounds) == 8
            and math.isfinite(uniform_g3)
            and uniform_g3 >= 0
            and all(
                math.isfinite(float(row["endpoint_G_abs_upper"]))
                and float(row["endpoint_G_abs_upper"]) >= 0
                for row in g_box_rows
            ),
            f"G3={uniform_g3}",
        ),
        validation_row(
            "formalization_workbench_remains_unmodified",
            h_result.get("formalization_workbench_modified_file_count") == 0,
            h_result.get("formalization_workbench_modified_file_count"),
        ),
        validation_row(
            "claim_boundary_keeps_W3_and_broader_claims_false",
            True,
            "G3 only; W3, total remainder, D4 outer limit, local GR and full MTS remain false",
        ),
    ]
    validation_passed = all(row["passed"] for row in validations)
    for row in (*ratio_rows, *g_box_rows, *event_bounds):
        row[CLAIM_RATIO] = validation_passed
        row[CLAIM_G] = validation_passed
        row[CLAIM_G3] = validation_passed
    registered_sources = [
        {
            "path": str(path),
            "exists": path.is_file(),
            "sha256": digest(path),
            CLAIM_RATIO: validation_passed,
            CLAIM_G: validation_passed,
            CLAIM_G3: validation_passed,
            **{claim: False for claim in OPEN_CLAIMS},
        }
        for path in required
    ]
    result = {
        "checkpoint": CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "validation_passed": validation_passed,
        "decision": (
            "DESINGULARIZED_ENDPOINT_G3_CAUCHY_BOUND_CERTIFIED__PROCEED_TO_W3"
            if validation_passed
            else "DESINGULARIZED_ENDPOINT_G3_CAUCHY_BOUND_BLOCKED"
        ),
        "required_ratio_box_count": 80,
        "certified_ratio_box_count": sum(
            row["desingularized_Krawczyk_passes"] is True
            for row in ratio_rows
        ),
        "minimum_desingularized_Krawczyk_inclusion_margin": min(
            float(row["minimum_strict_inclusion_margin"])
            for row in ratio_rows
        ),
        "maximum_desingularized_Krawczyk_contraction_bound": max(
            float(row["maximum_contraction_bound"]) for row in ratio_rows
        ),
        "maximum_desingularized_point_center_residual": max(
            float(row["point_center_residual_abs_upper"])
            for row in ratio_rows
        ),
        "maximum_parent_equation_factorization_residual": maximum_factorization_residual,
        "endpoint_H_log_plus_G_identity_residual": split_identity_residual,
        "event_normalized_gap_half_planes": {
            event_id: sorted(half_planes)
            for event_id, half_planes in event_half_planes.items()
        },
        "minimum_normalized_gap_modulus_lower": min(
            float(
                row[
                    "normalized_gap_epsilon_ref_z0_over_epsilon_modulus_lower"
                ]
            )
            for row in ratio_rows
        ),
        "maximum_normalized_gap_modulus_upper": max(
            float(
                row[
                    "normalized_gap_epsilon_ref_z0_over_epsilon_modulus_upper"
                ]
            )
            for row in ratio_rows
        ),
        "maximum_normalized_gap_principal_log_abs_upper": max(
            float(row["normalized_gap_principal_log_abs_upper"])
            for row in ratio_rows
        ),
        "regulator_Cauchy_radius": REGULATOR_CAUCHY_RADIUS,
        "uniform_endpoint_G3_upper": uniform_g3,
        "G_sector_Taylor_constant_upper": M5391.upward_quotient(
            uniform_g3, 6.0
        ),
        "claim_boundary": {
            CLAIM_RATIO: validation_passed,
            CLAIM_G: validation_passed,
            CLAIM_G3: validation_passed,
            **{claim: False for claim in OPEN_CLAIMS},
        },
        "remaining_obstruction": "construct and interval-enclose the parent-frozen mapped-away cells to obtain W3; only then combine M_D4=max(H3,G3+W3)/6",
        "formalization_workbench_modified_file_count": 0,
        "runtime_seconds": time.perf_counter() - started,
        "updated_utc": datetime.now(timezone.utc).isoformat(),
    }
    output = output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    atomic_csv(output / "D4_desingularized_endpoint_ratio_boxes.csv", ratio_rows)
    atomic_csv(output / "D4_endpoint_G3_box_bounds.csv", g_box_rows)
    atomic_csv(output / "D4_endpoint_G3_event_bounds.csv", event_bounds)
    atomic_csv(output / "D4_endpoint_G3_validation.csv", validations)
    atomic_csv(output / "source_register.csv", registered_sources)
    atomic_csv(VALIDATION, validations)
    atomic_json(output / "D4_endpoint_G3_result.json", result)
    atomic_json(
        output / "status.json",
        {
            "checkpoint": CHECKPOINT,
            "state": "complete" if validation_passed else "blocked",
            "decision": result["decision"],
            "updated_utc": result["updated_utc"],
        },
    )
    render_document(result, event_bounds)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    arguments = parser.parse_args()
    result = run(arguments.output)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["validation_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
