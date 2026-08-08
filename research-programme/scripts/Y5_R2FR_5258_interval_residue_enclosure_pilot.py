from __future__ import annotations

import argparse
import cmath
import csv
import importlib.util
import json
import math
import os
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

from mpmath import iv


WORKBENCH = Path(__file__).resolve().parents[1]
SCRIPTS = WORKBENCH / "scripts"
FUNCTIONAL_RG = WORKBENCH / "source-intake" / "functional_rg"
SOURCE_5256 = FUNCTIONAL_RG / "5256"
SOURCE_5257 = FUNCTIONAL_RG / "5257"
SOURCE = FUNCTIONAL_RG / "5258"

SCRIPT_5256_EXACT = (
    SCRIPTS / "Y5_R2FR_5256_exact_active_denominator_crosscheck.py"
)
SCRIPT_5257 = (
    SCRIPTS
    / "Y5_R2FR_5257_lower_point_factorized_active_numerator_smoke.py"
)

DENOMINATOR_ROWS = SOURCE_5256 / "exact_active_denominator_crosscheck.csv"
BRACKET_ROWS = SOURCE_5256 / "narrowed_topology_transition_brackets.csv"
ORIENTATION_ROWS = SOURCE_5257 / "factorized_active_numerator_smoke.csv"

BOX_ROWS = SOURCE / "interval_residue_boxes.csv"
TRANSITION_ROWS = SOURCE / "interval_transition_envelopes.csv"
REGULARIZATION_ROWS = SOURCE / "regularized_factorization_crosscheck.csv"
VALIDATION = SOURCE / "interval_residue_validation.csv"
RESULT = SOURCE / "interval_residue_result.json"

ACTIVE_ENDPOINTS = {
    "I01_T00": "D01A",
    "I01_T01": "D01B",
    "I06_T00": "C06A",
    "I06_T01": "D06B",
}
EPSILON_IDS = ("E020", "E040")
S_VALUE = 4.0
HALF_RESIDUE_COEFFICIENT = 0.016
ANGULAR_JACOBIAN = 0.25
MAXIMUM_PHASE_SPLIT_DEPTH = 8
MAXIMUM_X_SPLIT_DEPTH = 8

iv.dps = 40


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5256X = load_module("mts_5256_exact_for_5258", SCRIPT_5256_EXACT)
M5257 = load_module("mts_5257_for_5258", SCRIPT_5257)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def atomic_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(text, encoding="utf-8")
    os.replace(temporary, path)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise RuntimeError(f"refusing to write empty CSV: {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    os.replace(temporary, path)


class IntervalSingularity(RuntimeError):
    pass


@dataclass
class IntervalDiagnostics:
    denominator_lowers: list[float] = field(default_factory=list)
    denominator_labels: list[str] = field(default_factory=list)

    def record(self, value: Any, label: str) -> None:
        lower = lower_abs(value)
        self.denominator_lowers.append(lower)
        self.denominator_labels.append(label)
        if not math.isfinite(lower) or lower <= 0.0:
            raise IntervalSingularity(
                f"interval denominator reaches zero: {label}"
            )

    @property
    def minimum_denominator_lower(self) -> float:
        return (
            min(self.denominator_lowers)
            if self.denominator_lowers
            else math.inf
        )


def cpoint(value: complex | float | int) -> Any:
    converted = complex(value)
    return iv.mpc(
        [converted.real, converted.real],
        [converted.imag, converted.imag],
    )


def cbox(
    real_lower: float,
    real_upper: float,
    imaginary_lower: float = 0.0,
    imaginary_upper: float = 0.0,
) -> Any:
    return iv.mpc(
        [real_lower, real_upper],
        [imaginary_lower, imaginary_upper],
    )


def lower_abs(value: Any) -> float:
    return float(abs(value).a)


def upper_abs(value: Any) -> float:
    return float(abs(value).b)


def real_bounds(value: Any) -> tuple[float, float]:
    return float(value.real.a), float(value.real.b)


def imaginary_bounds(value: Any) -> tuple[float, float]:
    return float(value.imag.a), float(value.imag.b)


def midpoint(value: Any) -> complex:
    real_lower, real_upper = real_bounds(value)
    imaginary_lower, imaginary_upper = imaginary_bounds(value)
    return complex(
        0.5 * (real_lower + real_upper),
        0.5 * (imaginary_lower + imaginary_upper),
    )


def expanded(value: Any, error: float) -> Any:
    real_lower, real_upper = real_bounds(value)
    imaginary_lower, imaginary_upper = imaginary_bounds(value)
    return cbox(
        math.nextafter(real_lower - error, -math.inf),
        math.nextafter(real_upper + error, math.inf),
        math.nextafter(imaginary_lower - error, -math.inf),
        math.nextafter(imaginary_upper + error, math.inf),
    )


def intersect_complex_boxes(left: Any, right: Any, label: str) -> Any:
    left_real = real_bounds(left)
    right_real = real_bounds(right)
    left_imaginary = imaginary_bounds(left)
    right_imaginary = imaginary_bounds(right)
    real_lower = max(left_real[0], right_real[0])
    real_upper = min(left_real[1], right_real[1])
    imaginary_lower = max(left_imaginary[0], right_imaginary[0])
    imaginary_upper = min(left_imaginary[1], right_imaginary[1])
    if real_lower > real_upper or imaginary_lower > imaginary_upper:
        raise IntervalSingularity(f"empty interval intersection: {label}")
    return cbox(
        math.nextafter(real_lower, -math.inf),
        math.nextafter(real_upper, math.inf),
        math.nextafter(imaginary_lower, -math.inf),
        math.nextafter(imaginary_upper, math.inf),
    )


def complex_box_width(value: Any) -> float:
    real_lower, real_upper = real_bounds(value)
    imaginary_lower, imaginary_upper = imaginary_bounds(value)
    return max(
        real_upper - real_lower,
        imaginary_upper - imaginary_lower,
    )


def safe_divide(
    numerator: Any,
    denominator: Any,
    diagnostics: IntervalDiagnostics,
    label: str,
) -> Any:
    diagnostics.record(denominator, label)
    return numerator / denominator


def vector_add(left: list[Any], right: list[Any]) -> list[Any]:
    return [left[index] + right[index] for index in range(len(left))]


def vector_negate(vector: list[Any]) -> list[Any]:
    return [-value for value in vector]


def minkowski(left: list[Any], right: list[Any]) -> Any:
    return (
        left[0] * right[0]
        - left[1] * right[1]
        - left[2] * right[2]
        - left[3] * right[3]
    )


def massless_spinors(
    momentum: list[Any],
    diagnostics: IntervalDiagnostics,
    label: str,
    allow_transverse_chart: bool = True,
) -> tuple[list[Any], list[Any]]:
    energy, px, py, pz = momentum
    plus = energy + pz
    minus = energy - pz
    transverse_minus = px - cpoint(1.0j) * py
    transverse_plus = px + cpoint(1.0j) * py
    diagonal_lowers = (lower_abs(plus), lower_abs(minus))
    if max(diagonal_lowers) > 0.0 or not allow_transverse_chart:
        chart = "plus" if diagonal_lowers[0] >= diagonal_lowers[1] else "minus"
    else:
        transverse_lowers = (
            lower_abs(transverse_minus),
            lower_abs(transverse_plus),
        )
        chart = (
            "transverse_minus"
            if transverse_lowers[0] >= transverse_lowers[1]
            else "transverse_plus"
        )
    selected = {
        "plus": plus,
        "minus": minus,
        "transverse_minus": transverse_minus,
        "transverse_plus": transverse_plus,
    }[chart]
    diagnostics.record(selected, f"{label}:spinor_chart")
    root = selected ** 0.5
    diagnostics.record(root, f"{label}:spinor_root")
    if chart == "plus":
        angle = [
            root,
            safe_divide(
                transverse_plus,
                root,
                diagnostics,
                f"{label}:angle_plus",
            ),
        ]
        square = [
            root,
            safe_divide(
                transverse_minus,
                root,
                diagnostics,
                f"{label}:square_plus",
            ),
        ]
    elif chart == "minus":
        angle = [
            safe_divide(
                transverse_minus,
                root,
                diagnostics,
                f"{label}:angle_minus",
            ),
            root,
        ]
        square = [
            safe_divide(
                transverse_plus,
                root,
                diagnostics,
                f"{label}:square_minus",
            ),
            root,
        ]
    elif chart == "transverse_minus":
        angle = [
            root,
            safe_divide(
                minus,
                root,
                diagnostics,
                f"{label}:angle_transverse_minus",
            ),
        ]
        square = [
            safe_divide(
                plus,
                root,
                diagnostics,
                f"{label}:square_transverse_minus",
            ),
            root,
        ]
    else:
        angle = [
            safe_divide(
                plus,
                root,
                diagnostics,
                f"{label}:angle_transverse_plus",
            ),
            root,
        ]
        square = [
            root,
            safe_divide(
                minus,
                root,
                diagnostics,
                f"{label}:square_transverse_plus",
            ),
        ]
    return angle, square


def spinor_bracket(left: list[Any], right: list[Any]) -> Any:
    return left[0] * right[1] - left[1] * right[0]


def bispinor_to_vector(matrix: list[list[Any]]) -> list[Any]:
    return [
        (matrix[0][0] + matrix[1][1]) / cpoint(2.0),
        (matrix[0][1] + matrix[1][0]) / cpoint(2.0),
        (matrix[1][0] - matrix[0][1]) / cpoint(2.0j),
        (matrix[0][0] - matrix[1][1]) / cpoint(2.0),
    ]


def polarization(
    momentum: list[Any],
    reference: list[Any],
    helicity: int,
    diagnostics: IntervalDiagnostics,
    label: str,
) -> list[Any]:
    angle_momentum, square_momentum = massless_spinors(
        momentum,
        diagnostics,
        f"{label}:momentum",
    )
    angle_reference, square_reference = massless_spinors(
        reference,
        diagnostics,
        f"{label}:reference",
    )
    if helicity == 1:
        denominator = spinor_bracket(
            angle_reference,
            angle_momentum,
        )
        diagnostics.record(denominator, f"{label}:polarization_plus")
        matrix = [
            [
                cpoint(math.sqrt(2.0))
                * angle_reference[row]
                * square_momentum[column]
                / denominator
                for column in range(2)
            ]
            for row in range(2)
        ]
    elif helicity == -1:
        denominator = spinor_bracket(
            square_momentum,
            square_reference,
        )
        diagnostics.record(denominator, f"{label}:polarization_minus")
        matrix = [
            [
                cpoint(math.sqrt(2.0))
                * angle_momentum[row]
                * square_reference[column]
                / denominator
                for column in range(2)
            ]
            for row in range(2)
        ]
    else:
        raise ValueError("helicity must be +1 or -1")
    return bispinor_to_vector(matrix)


def field_strength_contraction(
    left: list[Any],
    momentum: list[Any],
    polarization_vector: list[Any],
    right: list[Any],
) -> Any:
    return (
        minkowski(left, momentum)
        * minkowski(polarization_vector, right)
        - minkowski(left, polarization_vector)
        * minkowski(momentum, right)
    )


def subtracted_invariant(*momenta: list[Any]) -> Any:
    total = [cpoint(0.0) for _ in range(4)]
    for momentum in momenta:
        total = vector_add(total, momentum)
    return minkowski(total, total) - sum(
        (minkowski(momentum, momentum) for momentum in momenta),
        cpoint(0.0),
    )


def ordered_shuffles(
    left: list[int],
    right: list[int],
) -> list[list[int]]:
    if not left:
        return [list(right)]
    if not right:
        return [list(left)]
    return [
        [left[0], *remainder]
        for remainder in ordered_shuffles(left[1:], right)
    ] + [
        [right[0], *remainder]
        for remainder in ordered_shuffles(left, right[1:])
    ]


def canonical_gauge_four(
    momenta: list[list[Any]],
    polarizations: list[list[Any]],
    diagnostics: IntervalDiagnostics,
    label: str,
) -> Any:
    scalar_left, graviton_two, graviton_three, scalar_right = (
        momenta
    )
    epsilon_two, epsilon_three = polarizations
    s_23 = subtracted_invariant(graviton_two, graviton_three)
    s_12 = subtracted_invariant(scalar_left, graviton_two)
    numerator_23 = (
        cpoint(2.0)
        * minkowski(epsilon_two, scalar_left)
        * minkowski(epsilon_three, graviton_two)
        - cpoint(2.0)
        * field_strength_contraction(
            epsilon_two,
            graviton_three,
            epsilon_three,
            scalar_left,
        )
    )
    numerator_12 = (
        -cpoint(2.0)
        * minkowski(epsilon_two, scalar_left)
        * minkowski(epsilon_three, scalar_right)
    )
    return safe_divide(
        numerator_23,
        s_23,
        diagnostics,
        f"{label}:s23",
    ) + safe_divide(
        numerator_12,
        s_12,
        diagnostics,
        f"{label}:s12",
    )


def gauge_four_ordered(
    order: list[int],
    momenta: list[list[Any]],
    polarizations: dict[int, list[Any]],
    diagnostics: IntervalDiagnostics,
    label: str,
) -> Any:
    rotated = list(order)
    scalar_start = rotated.index(0)
    rotated = rotated[scalar_start:] + rotated[:scalar_start]
    scalar_end = rotated.index(4)
    alpha = rotated[1:scalar_end]
    beta = rotated[scalar_end + 1 :]
    result = cpoint(0.0)
    for index, shuffle in enumerate(
        ordered_shuffles(alpha, list(reversed(beta)))
    ):
        result += canonical_gauge_four(
            [
                momenta[0],
                *[momenta[item] for item in shuffle],
                momenta[4],
            ],
            [polarizations[item] for item in shuffle],
            diagnostics,
            f"{label}:shuffle{index}",
        )
    return cpoint((-1) ** len(beta)) * result


def covariant_scalar_klt_four(
    momenta: list[list[Any]],
    helicities: dict[int, int],
    diagnostics: IntervalDiagnostics,
    label: str,
) -> Any:
    polarizations = {
        index: polarization(
            momenta[index],
            momenta[4],
            helicities[index],
            diagnostics,
            f"{label}:polarization{index}",
        )
        for index in (1, 2)
    }
    left = gauge_four_ordered(
        [0, 1, 2, 4],
        momenta,
        polarizations,
        diagnostics,
        f"{label}:left",
    )
    right = gauge_four_ordered(
        [2, 4, 1, 0],
        momenta,
        polarizations,
        diagnostics,
        f"{label}:right",
    )
    return -left * invariant(momenta, 0, 1) * right


def spinor_table(
    momenta: list[list[Any]],
    indices: tuple[int, ...],
    diagnostics: IntervalDiagnostics,
    label: str,
    allow_transverse_chart: bool = True,
) -> dict[int, tuple[list[Any], list[Any]]]:
    return {
        index: massless_spinors(
            momenta[index],
            diagnostics,
            f"{label}:p{index}",
            allow_transverse_chart,
        )
        for index in indices
    }


def spinor_exponent_table(
    momenta: list[list[Any]],
    indices: tuple[int, ...],
    rotated_indices: set[int],
) -> dict[int, tuple[list[int], list[int]]]:
    result: dict[int, tuple[list[int], list[int]]] = {}
    for index in indices:
        if index not in rotated_indices:
            result[index] = ([0, 0], [0, 0])
            continue
        energy, _, _, pz = momenta[index]
        plus = energy + pz
        minus = energy - pz
        if lower_abs(plus) >= lower_abs(minus):
            result[index] = ([0, 1], [0, -1])
        else:
            result[index] = ([-1, 0], [1, 0])
    return result


def active_bracket_quotient(
    left_index: int,
    right_index: int,
    selected_spinors: dict[int, list[Any]],
    selected_exponents: dict[int, list[int]],
    unit_circle: Any,
    active_center: Any,
    diagnostics: IntervalDiagnostics,
    label: str,
) -> Any:
    left = selected_spinors[left_index]
    right = selected_spinors[right_index]
    left_exponents = selected_exponents[left_index]
    right_exponents = selected_exponents[right_index]
    first_term = left[0] * right[1]
    second_term = -left[1] * right[0]
    first_exponent = left_exponents[0] + right_exponents[1]
    second_exponent = left_exponents[1] + right_exponents[0]
    terms = (
        (first_term, first_exponent),
        (second_term, second_exponent),
    )
    varying = [item for item in terms if item[1] != 0]
    fixed = [item for item in terms if item[1] == 0]
    if len(varying) != 1 or len(fixed) != 1:
        raise IntervalSingularity(
            f"active spinor factor is not affine Laurent: {label}"
        )
    varying_term, exponent = varying[0]
    if exponent == 1:
        coefficient = safe_divide(
            varying_term,
            unit_circle,
            diagnostics,
            f"{label}:unit_circle",
        )
        quotient = coefficient
    elif exponent == -1:
        coefficient = varying_term * unit_circle
        quotient = safe_divide(
            -coefficient,
            unit_circle * active_center,
            diagnostics,
            f"{label}:reciprocal_unit_centers",
        )
    else:
        raise IntervalSingularity(
            f"unsupported active Laurent exponent {exponent}: {label}"
        )
    diagnostics.record(quotient, f"{label}:active_factor_quotient")
    return quotient


def scalar_mhv(
    order: list[int],
    special: int,
    spinors: dict[int, tuple[list[Any], list[Any]]],
    chirality: int,
    diagnostics: IntervalDiagnostics,
    label: str,
) -> Any:
    selected = {
        index: spinors[index][chirality] for index in spinors
    }
    numerator_pairs = {
        frozenset((special, endpoint)): {
            "ordered_pair": (special, endpoint),
            "factor": spinor_bracket(
                selected[special],
                selected[endpoint],
            ),
            "remaining": 2,
        }
        for endpoint in (0, 4)
    }
    value = cpoint(1.0)
    for index, left in enumerate(order):
        right = order[(index + 1) % len(order)]
        pair = frozenset((left, right))
        numerator_data = numerator_pairs.get(pair)
        if (
            numerator_data is not None
            and numerator_data["remaining"] > 0
        ):
            orientation = (
                1
                if (left, right) == numerator_data["ordered_pair"]
                else -1
            )
            value *= cpoint(orientation)
            numerator_data["remaining"] -= 1
            continue
        edge = spinor_bracket(
            selected[left],
            selected[right],
        )
        value = safe_divide(
            value,
            edge,
            diagnostics,
            f"{label}:parketaylor_edge_{index}_{left}_{right}",
        )
    for numerator_data in numerator_pairs.values():
        value *= numerator_data["factor"] ** numerator_data["remaining"]
    return value


def regularized_scalar_mhv(
    order: list[int],
    special: int,
    spinors: dict[int, tuple[list[Any], list[Any]]],
    spinor_exponents: dict[int, tuple[list[int], list[int]]],
    chirality: int,
    unit_circle: Any,
    active_center: Any,
    active_pairs: set[frozenset[int]],
    diagnostics: IntervalDiagnostics,
    label: str,
) -> tuple[Any, int]:
    selected = {
        index: spinors[index][chirality] for index in spinors
    }
    selected_exponents = {
        index: spinor_exponents[index][chirality]
        for index in spinor_exponents
    }
    numerator_pairs = {
        frozenset((special, endpoint)): {
            "ordered_pair": (special, endpoint),
            "factor": spinor_bracket(
                selected[special],
                selected[endpoint],
            ),
            "remaining": 2,
        }
        for endpoint in (0, 4)
    }
    value = cpoint(1.0)
    cancelled = 0
    for index, left in enumerate(order):
        right = order[(index + 1) % len(order)]
        pair = frozenset((left, right))
        numerator_data = numerator_pairs.get(pair)
        if (
            numerator_data is not None
            and numerator_data["remaining"] > 0
        ):
            orientation = (
                1
                if (left, right) == numerator_data["ordered_pair"]
                else -1
            )
            value *= cpoint(orientation)
            numerator_data["remaining"] -= 1
            continue
        if pair in active_pairs:
            denominator = active_bracket_quotient(
                left,
                right,
                selected,
                selected_exponents,
                unit_circle,
                active_center,
                diagnostics,
                f"{label}:active_edge_{index}_{left}_{right}",
            )
            cancelled += 1
        else:
            denominator = spinor_bracket(
                selected[left],
                selected[right],
            )
        value = safe_divide(
            value,
            denominator,
            diagnostics,
            f"{label}:parketaylor_edge_{index}_{left}_{right}",
        )
    for numerator_data in numerator_pairs.values():
        value *= numerator_data["factor"] ** numerator_data["remaining"]
    return value, cancelled


def invariant(momenta: list[list[Any]], left: int, right: int) -> Any:
    return cpoint(2.0) * minkowski(momenta[left], momenta[right])


def scalar_klt_four(
    momenta: list[list[Any]],
    special: int,
    chirality: int,
    diagnostics: IntervalDiagnostics,
    label: str,
) -> Any:
    spinors = spinor_table(
        momenta,
        (0, 1, 2, 4),
        diagnostics,
        label,
    )
    left = scalar_mhv(
        [0, 1, 2, 4],
        special,
        spinors,
        chirality,
        diagnostics,
        f"{label}:left",
    )
    right = scalar_mhv(
        [2, 4, 1, 0],
        special,
        spinors,
        chirality,
        diagnostics,
        f"{label}:right",
    )
    return -left * invariant(momenta, 0, 1) * right


def momentum_kernel(
    alpha_reversed: int,
    beta_reversed: int,
    momenta: list[list[Any]],
) -> Any:
    s_21 = invariant(momenta, 1, 0)
    s_31 = invariant(momenta, 2, 0)
    s_23 = invariant(momenta, 1, 2)
    if alpha_reversed == 0 and beta_reversed == 0:
        return s_21 * s_31
    if alpha_reversed == 0 and beta_reversed == 1:
        return (s_21 + s_23) * s_31
    if alpha_reversed == 1 and beta_reversed == 0:
        return (s_31 + s_23) * s_21
    return s_31 * s_21


def regularized_scalar_klt_five(
    momenta: list[list[Any]],
    special: int,
    chirality: int,
    hard_index: int,
    unit_circle: Any,
    active_center: Any,
    displacement: Any,
    diagnostics: IntervalDiagnostics,
    label: str,
) -> Any:
    spinors = spinor_table(
        momenta,
        (0, 1, 2, 3, 4),
        diagnostics,
        label,
        False,
    )
    spinor_exponents = spinor_exponent_table(
        momenta,
        (0, 1, 2, 3, 4),
        {1, 2, 3},
    )
    active_pairs = (
        {
            frozenset((0, 3)),
            frozenset((4, hard_index)),
        }
        if chirality == 0
        else set()
    )
    result = cpoint(0.0)
    for sigma_reversed in range(2):
        sigma = [1, 2] if sigma_reversed == 0 else [2, 1]
        left, left_cancelled = regularized_scalar_mhv(
            [0, *sigma, 3, 4],
            special,
            spinors,
            spinor_exponents,
            chirality,
            unit_circle,
            active_center,
            active_pairs,
            diagnostics,
            f"{label}:left{sigma_reversed}",
        )
        for gamma_reversed in range(2):
            gamma = [1, 2] if gamma_reversed == 0 else [2, 1]
            right, right_cancelled = regularized_scalar_mhv(
                [3, 4, *gamma, 0],
                special,
                spinors,
                spinor_exponents,
                chirality,
                unit_circle,
                active_center,
                active_pairs,
                diagnostics,
                f"{label}:right{gamma_reversed}",
            )
            remaining_power = (
                2 - left_cancelled - right_cancelled
            )
            if remaining_power < 0:
                raise IntervalSingularity(
                    f"more than two active factors in {label}"
                )
            result += (
                displacement ** remaining_power
                * left
                * momentum_kernel(
                    gamma_reversed,
                    sigma_reversed,
                    momenta,
                )
                * right
            )
    return result


def external_complex(target: complex) -> list[list[Any]]:
    transverse = cpoint(1.0 - target * target) ** 0.5
    return [
        [cpoint(1.0), cpoint(0.0), cpoint(0.0), cpoint(1.0)],
        [cpoint(1.0), cpoint(0.0), cpoint(0.0), cpoint(-1.0)],
        [cpoint(1.0), transverse, cpoint(0.0), cpoint(target)],
        [cpoint(1.0), -transverse, cpoint(0.0), cpoint(-target)],
    ]


def cut_momenta(
    internal: list[list[Any]],
    target: complex,
) -> tuple[list[list[Any]], list[list[Any]]]:
    external = external_complex(target)
    zero = [cpoint(0.0) for _ in range(4)]
    left = [list(zero) for _ in range(5)]
    right = [list(zero) for _ in range(5)]
    left[0] = vector_negate(external[0])
    left[4] = vector_negate(external[1])
    right[0] = external[2]
    right[4] = external[3]
    for index in range(3):
        left[index + 1] = internal[index]
        right[index + 1] = vector_negate(internal[index])
    return left, right


def helicity(index: int, special: int, chirality: int) -> int:
    if chirality == 0:
        return -1 if index == special else 1
    return 1 if index == special else -1


def factorized_d_hhh(
    internal: list[list[Any]],
    target: complex,
    hard_index: int,
    unit_circle: Any,
    active_center: Any,
    displacement: Any,
    diagnostics: IntervalDiagnostics,
) -> Any:
    left, right = cut_momenta(internal, target)
    result = cpoint(0.0)
    remaining = [
        index for index in (1, 2, 3) if index != hard_index
    ]
    for special in (1, 2, 3):
        if special == hard_index:
            continue
        special_reduced = 1 if remaining[0] == special else 2
        for chirality in (0, 1):
            hard_polarization = polarization(
                left[hard_index],
                left[4],
                helicity(hard_index, special, chirality),
                diagnostics,
                f"M3:s{special}:c{chirality}",
            )
            gravity_three = (
                cpoint(2.0)
                * minkowski(hard_polarization, left[0]) ** 2
            )
            reduced = [
                vector_add(left[0], left[hard_index]),
                left[remaining[0]],
                left[remaining[1]],
                [cpoint(0.0) for _ in range(4)],
                left[4],
            ]
            reduced_helicities = {
                reduced_index: helicity(
                    original_index,
                    special,
                    chirality,
                )
                for reduced_index, original_index in (
                    (1, remaining[0]),
                    (2, remaining[1]),
                )
            }
            gravity_four = scalar_klt_four(
                reduced,
                special_reduced,
                chirality,
                diagnostics,
                f"K4:s{special}:c{chirality}",
            )
            gravity_five = regularized_scalar_klt_five(
                right,
                special,
                1 - chirality,
                hard_index,
                unit_circle,
                active_center,
                displacement,
                diagnostics,
                f"K5:s{special}:c{chirality}",
            )
            result += gravity_three * gravity_four * gravity_five
    return result / cpoint(6.0)


def rotate_vector(vector: list[Any], unit_circle: Any) -> list[Any]:
    transverse_plus = vector[0] + cpoint(1.0j) * vector[1]
    transverse_minus = vector[0] - cpoint(1.0j) * vector[1]
    rotated_plus = unit_circle * transverse_plus
    rotated_minus = transverse_minus / unit_circle
    return [
        (rotated_plus + rotated_minus) / cpoint(2.0),
        (rotated_plus - rotated_minus) / cpoint(2.0j),
        vector[2],
    ]


def rotate_internal(
    internal: list[list[Any]],
    unit_circle: Any,
) -> list[list[Any]]:
    return [
        [momentum[0], *rotate_vector(momentum[1:], unit_circle)]
        for momentum in internal
    ]


def rotate_internal_lightcone(
    internal_lightcone: list[dict[str, Any]],
    unit_circle: Any,
) -> list[list[Any]]:
    rotated: list[list[Any]] = []
    for momentum in internal_lightcone:
        transverse_plus = (
            unit_circle * momentum["transverse_plus"]
        )
        transverse_minus = (
            momentum["transverse_minus"] / unit_circle
        )
        rotated.append(
            [
                momentum["energy"],
                (transverse_plus + transverse_minus)
                / cpoint(2.0),
                (transverse_plus - transverse_minus)
                / cpoint(2.0j),
                momentum["pz"],
            ]
        )
    return rotated


def branch_sign(endpoint_row: dict[str, str]) -> int:
    coefficients = M5256X.quadratic_coefficients(
        endpoint_row["component_id"],
        float(endpoint_row["decay_cosine"]),
        (
            2.0 - float(endpoint_row["soft_energy"])
        )
        / (
            2.0
            * math.sqrt(1.0 - float(endpoint_row["soft_energy"]))
        ),
        float(endpoint_row["soft_energy"])
        / (
            2.0
            * math.sqrt(1.0 - float(endpoint_row["soft_energy"]))
        ),
        (
            (2.0 - float(endpoint_row["soft_energy"]))
            / (
                2.0
                * math.sqrt(
                    1.0 - float(endpoint_row["soft_energy"])
                )
            )
            - 1.0
        ),
        complex(
            float(endpoint_row["kappa_real"]),
            float(endpoint_row["kappa_imaginary"]),
        ),
    )
    first, second, _ = M5256X.quadratic_roots(*coefficients)
    expected = complex(
        float(endpoint_row["exact_pole_real"]),
        float(endpoint_row["exact_pole_imaginary"]),
    )
    return 1 if abs(first - expected) <= abs(second - expected) else -1


def interval_state(
    endpoint_row: dict[str, str],
    x_lower: float,
    x_upper: float,
    selected_branch_sign: int,
    diagnostics: IntervalDiagnostics,
) -> dict[str, Any]:
    component_id = endpoint_row["component_id"]
    energy = float(endpoint_row["soft_energy"])
    recoil_root = math.sqrt(1.0 - energy)
    gamma = (2.0 - energy) / (2.0 * recoil_root)
    gamma_beta = energy / (2.0 * recoil_root)
    h = gamma - 1.0
    kappa_value = complex(
        float(endpoint_row["kappa_real"]),
        float(endpoint_row["kappa_imaginary"]),
    )
    kappa = cpoint(kappa_value)
    x = cbox(x_lower, x_upper)
    coefficient_2 = cpoint(h) * (cpoint(1.0) + kappa)
    if component_id == "MC12":
        coefficient_1 = -(
            cpoint(h)
            - cpoint(gamma_beta) * x
            - kappa * cpoint(gamma_beta) * (cpoint(1.0) + x)
        )
        coefficient_0 = (
            -cpoint(gamma_beta) * x
            + kappa * (cpoint(1.0) + cpoint(gamma) * x)
        )
        hard_sign = -1.0
        derivative_sign = -1.0
    elif component_id == "MC04":
        coefficient_1 = -(
            cpoint(h)
            + cpoint(gamma_beta) * x
            - kappa * cpoint(gamma_beta) * (cpoint(1.0) - x)
        )
        coefficient_0 = (
            cpoint(gamma_beta) * x
            + kappa * (cpoint(1.0) - cpoint(gamma) * x)
        )
        hard_sign = 1.0
        derivative_sign = 1.0
    else:
        raise RuntimeError(f"unsupported component: {component_id}")
    discriminant = (
        coefficient_1 * coefficient_1
        - cpoint(4.0) * coefficient_2 * coefficient_0
    )
    discriminant_root = discriminant ** 0.5
    natural_pole = safe_divide(
        -coefficient_1
        + cpoint(selected_branch_sign) * discriminant_root,
        cpoint(2.0) * coefficient_2,
        diagnostics,
        "quadratic_leading_coefficient",
    )
    x_middle_value = 0.5 * (x_lower + x_upper)
    x_middle = cpoint(x_middle_value)
    if component_id == "MC12":
        coefficient_1_middle = -(
            cpoint(h)
            - cpoint(gamma_beta) * x_middle
            - kappa
            * cpoint(gamma_beta)
            * (cpoint(1.0) + x_middle)
        )
        coefficient_0_middle = (
            -cpoint(gamma_beta) * x_middle
            + kappa
            * (cpoint(1.0) + cpoint(gamma) * x_middle)
        )
        coefficient_1_derivative = (
            cpoint(gamma_beta) * (cpoint(1.0) + kappa)
        )
        coefficient_0_derivative = (
            -cpoint(gamma_beta) + kappa * cpoint(gamma)
        )
    else:
        coefficient_1_middle = -(
            cpoint(h)
            + cpoint(gamma_beta) * x_middle
            - kappa
            * cpoint(gamma_beta)
            * (cpoint(1.0) - x_middle)
        )
        coefficient_0_middle = (
            cpoint(gamma_beta) * x_middle
            + kappa
            * (cpoint(1.0) - cpoint(gamma) * x_middle)
        )
        coefficient_1_derivative = -(
            cpoint(gamma_beta) * (cpoint(1.0) + kappa)
        )
        coefficient_0_derivative = (
            cpoint(gamma_beta) - kappa * cpoint(gamma)
        )
    middle_discriminant = (
        coefficient_1_middle * coefficient_1_middle
        - cpoint(4.0) * coefficient_2 * coefficient_0_middle
    )
    middle_pole = safe_divide(
        -coefficient_1_middle
        + cpoint(selected_branch_sign) * middle_discriminant ** 0.5,
        cpoint(2.0) * coefficient_2,
        diagnostics,
        "quadratic_middle_leading_coefficient",
    )
    pole = natural_pole
    for contraction_index in range(4):
        branch_jacobian = (
            cpoint(2.0) * coefficient_2 * pole + coefficient_1
        )
        pole_derivative = safe_divide(
            -(
                coefficient_1_derivative * pole
                + coefficient_0_derivative
            ),
            branch_jacobian,
            diagnostics,
            f"quadratic_branch_jacobian_{contraction_index}",
        )
        centered_pole = middle_pole + (
            x - x_middle
        ) * pole_derivative
        pole = intersect_complex_boxes(
            pole,
            centered_pole,
            f"quadratic_branch_contraction_{contraction_index}",
        )
    denominator = cpoint(h) * pole + cpoint(gamma_beta)
    diagnostics.record(denominator, "hard_channel_denominator_factor")
    if component_id == "MC12":
        relative_cosine = safe_divide(
            -(
                cpoint(gamma)
                + x
                + cpoint(gamma_beta) * pole
            ),
            denominator,
            diagnostics,
            "relative_cosine_MC12",
        )
        q0 = (
            cpoint(gamma)
            - x
            - cpoint(gamma_beta) * pole
            - kappa
            * cpoint(gamma_beta)
            * (cpoint(1.0) + pole)
        )
        partial_l_z = -(
            cpoint(1.0) + kappa
        ) * (
            cpoint(gamma_beta) + cpoint(h) * relative_cosine
        )
        derivative_offset = (
            cpoint(gamma_beta) + cpoint(h) * relative_cosine
        )
    else:
        relative_cosine = safe_divide(
            cpoint(gamma)
            + cpoint(gamma_beta) * pole
            - x,
            denominator,
            diagnostics,
            "relative_cosine_MC04",
        )
        q0 = (
            -cpoint(gamma)
            - x
            + cpoint(gamma_beta) * pole
            + kappa
            * cpoint(gamma_beta)
            * (cpoint(1.0) + pole)
        )
        partial_l_z = (
            cpoint(1.0) + kappa
        ) * (
            cpoint(gamma_beta) - cpoint(h) * relative_cosine
        )
        derivative_offset = (
            -cpoint(gamma_beta) + cpoint(h) * relative_cosine
        )
    q1 = (
        cpoint(gamma_beta)
        - cpoint(h) * pole
        - kappa * cpoint(h) * (cpoint(1.0) + pole)
    )
    linear = q0 + q1 * relative_cosine
    soft_transverse = (cpoint(1.0) - pole * pole) ** 0.5
    decay_transverse = (cpoint(1.0) - x * x) ** 0.5
    relative_root = safe_divide(
        soft_transverse * linear,
        kappa
        * (cpoint(1.0) + pole)
        * decay_transverse,
        diagnostics,
        "relative_root",
    )
    global_root = safe_divide(
        kappa ** 0.5 * (cpoint(1.0) + pole),
        soft_transverse,
        diagnostics,
        "global_root",
    )

    collision_partial_c = (
        cpoint(2.0)
        * (cpoint(1.0) - pole)
        * linear
        * q1
        - cpoint(2.0)
        * kappa
        * (
            linear
            + (relative_cosine - pole * x) * q1
        )
    )
    collision_partial_z = (
        -linear * linear
        + cpoint(2.0)
        * (cpoint(1.0) - pole)
        * linear
        * partial_l_z
        + cpoint(2.0) * kappa * x * linear
        - cpoint(2.0)
        * kappa
        * (relative_cosine - pole * x)
        * partial_l_z
        + (cpoint(1.0) - x * x) * kappa * kappa
    )
    relative_cosine_derivative = safe_divide(
        -collision_partial_z,
        collision_partial_c,
        diagnostics,
        "collision_partial_c",
    )
    channel_derivative = (
        cpoint(derivative_sign * 2.0 * recoil_root)
        * (
            derivative_offset
            + denominator * relative_cosine_derivative
        )
    )

    relative_derivative = (
        soft_transverse
        * decay_transverse
        * (cpoint(1.0) - cpoint(1.0) / (relative_root**2))
        / cpoint(2.0)
    )
    energy_plus_pz = cpoint(recoil_root) * (
        cpoint(gamma)
        + cpoint(hard_sign) * x
        - cpoint(gamma_beta) * pole
        + cpoint(hard_sign)
        * (
            cpoint(h) * pole - cpoint(gamma_beta)
        )
        * relative_cosine
    )
    p_plus = cpoint(recoil_root) * (
        cpoint(hard_sign) * decay_transverse * relative_root
        + cpoint(hard_sign * h)
        * soft_transverse
        * relative_cosine
        - cpoint(gamma_beta) * soft_transverse
    )
    energy_plus_pz_derivative = (
        cpoint(recoil_root * hard_sign)
        * (cpoint(h) * pole - cpoint(gamma_beta))
        * relative_derivative
    )
    p_plus_derivative = (
        cpoint(recoil_root * hard_sign)
        * (
            decay_transverse
            + cpoint(h)
            * soft_transverse
            * relative_derivative
        )
    )
    collision_jacobian = safe_divide(
        -(
            energy_plus_pz_derivative * p_plus
            - energy_plus_pz * p_plus_derivative
        ),
        kappa ** 0.5 * p_plus * p_plus,
        diagnostics,
        "collision_jacobian",
    )

    azimuth_cosine = (
        relative_root + cpoint(1.0) / relative_root
    ) / cpoint(2.0)
    azimuth_sine = (
        relative_root - cpoint(1.0) / relative_root
    ) / cpoint(2.0j)
    soft_direction = [
        soft_transverse,
        cpoint(0.0),
        pole,
    ]
    decay_direction = [
        decay_transverse * azimuth_cosine,
        decay_transverse * azimuth_sine,
        x,
    ]
    relative_dot = sum(
        (
            soft_direction[index] * decay_direction[index]
            for index in range(3)
        ),
        cpoint(0.0),
    )
    internal: list[list[Any]] = []
    internal_lightcone: list[dict[str, Any]] = []
    for sign in (1.0, -1.0):
        momentum_energy = cpoint(gamma * recoil_root) * (
            cpoint(1.0)
            - cpoint(sign * energy / (2.0 - energy))
            * relative_dot
        )
        longitudinal_coefficient = (
            cpoint(sign * h) * relative_dot
            - cpoint(gamma_beta)
        )
        transverse_plus = cpoint(recoil_root) * (
            cpoint(sign)
            * decay_transverse
            * relative_root
            + longitudinal_coefficient * soft_transverse
        )
        transverse_minus = cpoint(recoil_root) * (
            cpoint(sign)
            * decay_transverse
            / relative_root
            + longitudinal_coefficient * soft_transverse
        )
        pz = cpoint(recoil_root) * (
            cpoint(sign) * x
            + longitudinal_coefficient * pole
        )
        internal_lightcone.append(
            {
                "energy": momentum_energy,
                "transverse_plus": transverse_plus,
                "transverse_minus": transverse_minus,
                "pz": pz,
            }
        )
        internal.append(
            [
                momentum_energy,
                (transverse_plus + transverse_minus)
                / cpoint(2.0),
                (transverse_plus - transverse_minus)
                / cpoint(2.0j),
                pz,
            ]
        )
    soft_transverse_momentum = cpoint(energy) * soft_transverse
    internal_lightcone.append(
        {
            "energy": cpoint(energy),
            "transverse_plus": soft_transverse_momentum,
            "transverse_minus": soft_transverse_momentum,
            "pz": cpoint(energy) * pole,
        }
    )
    internal.append(
        [
            cpoint(energy),
            soft_transverse_momentum,
            cpoint(0.0),
            cpoint(energy) * pole,
        ]
    )
    return {
        "x": x,
        "pole": pole,
        "relative_root": relative_root,
        "global_root": global_root,
        "collision_jacobian": collision_jacobian,
        "channel_derivative": channel_derivative,
        "internal": internal,
        "internal_lightcone": internal_lightcone,
        "energy": energy,
        "target": complex(-9.0, float(endpoint_row["epsilon"])),
        "hard_index": (
            2 if component_id == "MC12" else 1
        ),
        "discriminant": discriminant,
        "natural_pole_box_width": complex_box_width(natural_pole),
        "tightened_pole_box_width": complex_box_width(pole),
    }


def d_times_direct(
    state: dict[str, Any],
    unit_circle: Any,
    displacement: Any,
    diagnostics: IntervalDiagnostics,
) -> Any:
    rotated = rotate_internal_lightcone(
        state["internal_lightcone"],
        unit_circle,
    )
    inverse_energy_square_sum = cpoint(0.0)
    for index, momentum in enumerate(rotated):
        inverse_energy_square_sum += safe_divide(
            cpoint(1.0),
            momentum[0] * momentum[0],
            diagnostics,
            f"multiplier_energy_{index}",
        )
    multiplier = safe_divide(
        safe_divide(
            cpoint(3.0),
            rotated[2][0] * rotated[2][0],
            diagnostics,
            "multiplier_soft_energy",
        ),
        inverse_energy_square_sum,
        diagnostics,
        "multiplier_inverse_energy_sum",
    )
    return (
        cpoint(state["energy"])
        * multiplier
        * factorized_d_hhh(
            rotated,
            state["target"],
            state["hard_index"],
            unit_circle,
            state["global_root"],
            displacement,
            diagnostics,
        )
        / cpoint(S_VALUE * S_VALUE)
    )


def numeric_safe_radius(
    endpoint_row: dict[str, str],
    x_value: float,
) -> float:
    energy = float(endpoint_row["soft_energy"])
    recoil_root = math.sqrt(1.0 - energy)
    gamma = (2.0 - energy) / (2.0 * recoil_root)
    gamma_beta = energy / (2.0 * recoil_root)
    h = gamma - 1.0
    kappa = complex(
        float(endpoint_row["kappa_real"]),
        float(endpoint_row["kappa_imaginary"]),
    )
    coefficients = M5256X.quadratic_coefficients(
        endpoint_row["component_id"],
        x_value,
        gamma,
        gamma_beta,
        h,
        kappa,
    )
    first, second, _ = M5256X.quadratic_roots(*coefficients)
    expected = complex(
        float(endpoint_row["exact_pole_real"]),
        float(endpoint_row["exact_pole_imaginary"]),
    )
    pole = min((first, second), key=lambda root: abs(root - expected))
    synthetic = dict(endpoint_row)
    synthetic["decay_cosine"] = str(x_value)
    synthetic["exact_pole_real"] = str(pole.real)
    synthetic["exact_pole_imaginary"] = str(pole.imag)
    branch = M5257.exact_branch(synthetic)
    soft_direction, decay_direction, internal = M5257.M5028.event_geometry(
        float(branch["soft_energy"]),
        complex(branch["soft_cosine"]),
        complex(branch["decay_cosine"]),
        complex(branch["relative_root"]),
    )
    return M5257.coefficient_radius(
        internal,
        soft_direction,
        decay_direction,
        complex(-9.0, float(endpoint_row["epsilon"])),
        complex(branch["global_root"]),
    )


def interval_factor_roots(
    momentum: dict[str, Any],
    external_stereographic: Any,
    diagnostics: IntervalDiagnostics,
    label: str,
) -> dict[str, Any]:
    longitudinal_plus = momentum["energy"] + momentum["pz"]
    plus_u = safe_divide(
        external_stereographic * longitudinal_plus,
        momentum["transverse_plus"],
        diagnostics,
        f"{label}:plus_u_transverse",
    )
    plus_v = safe_divide(
        momentum["transverse_minus"],
        external_stereographic * longitudinal_plus,
        diagnostics,
        f"{label}:plus_v_longitudinal",
    )
    minus_u = safe_divide(
        -longitudinal_plus,
        external_stereographic * momentum["transverse_plus"],
        diagnostics,
        f"{label}:minus_u_transverse",
    )
    minus_v = safe_divide(
        -external_stereographic * momentum["transverse_minus"],
        longitudinal_plus,
        diagnostics,
        f"{label}:minus_v_longitudinal",
    )
    return {
        "plus_u": plus_u,
        "plus_v": plus_v,
        "minus_u": minus_u,
        "minus_v": minus_v,
    }


def interval_root_separation(
    state: dict[str, Any],
) -> dict[str, Any]:
    diagnostics = IntervalDiagnostics()
    target = cpoint(state["target"])
    external_stereographic = (
        safe_divide(
            cpoint(1.0) - target,
            cpoint(1.0) + target,
            diagnostics,
            "external_stereographic_ratio",
        )
        ** 0.5
    )
    diagnostics.record(
        external_stereographic,
        "external_stereographic_root",
    )
    soft_transverse = (
        cpoint(1.0) - state["pole"] * state["pole"]
    ) ** 0.5
    decay_transverse = (
        cpoint(1.0) - state["x"] * state["x"]
    ) ** 0.5
    sources = {
        **{
            f"g{index + 1}": momentum
            for index, momentum in enumerate(
                state["internal_lightcone"]
            )
        },
        "soft": {
            "energy": cpoint(1.0),
            "transverse_plus": soft_transverse,
            "transverse_minus": soft_transverse,
            "pz": state["pole"],
        },
        "decay": {
            "energy": cpoint(1.0),
            "transverse_plus": (
                decay_transverse * state["relative_root"]
            ),
            "transverse_minus": safe_divide(
                decay_transverse,
                state["relative_root"],
                diagnostics,
                "decay_relative_root",
            ),
            "pz": state["x"],
        },
    }
    active_labels = {
        f"g{state['hard_index']}:minus_u",
        "g3:plus_u",
        "soft:plus_u",
    }
    rows: list[dict[str, Any]] = []
    separation_lowers = [lower_abs(state["global_root"])]
    active_identity_residual_upper = 0.0
    for source, momentum in sources.items():
        roots = interval_factor_roots(
            momentum,
            external_stereographic,
            diagnostics,
            source,
        )
        for root_label, root in roots.items():
            label = f"{source}:{root_label}"
            natural_residual = root - state["global_root"]
            if label in active_labels:
                active_identity_residual_upper = max(
                    active_identity_residual_upper,
                    upper_abs(natural_residual),
                )
                rows.append(
                    {
                        "label": label,
                        "active_identity": True,
                        "separation_lower": 0.0,
                        "natural_identity_residual_upper": upper_abs(
                            natural_residual
                        ),
                    }
                )
                continue
            separation_lower = lower_abs(natural_residual)
            separation_lowers.append(separation_lower)
            rows.append(
                {
                    "label": label,
                    "active_identity": False,
                    "separation_lower": separation_lower,
                    "natural_identity_residual_upper": "",
                }
            )
    minimum_separation = min(separation_lowers)
    if not math.isfinite(minimum_separation) or minimum_separation <= 0.0:
        raise IntervalSingularity(
            "non-active interval root reaches active center"
        )
    catalog_radius = 0.02 * minimum_separation
    return {
        "minimum_root_separation_lower": minimum_separation,
        "catalog_radius": catalog_radius,
        "root_count": len(rows),
        "active_root_count": sum(
            bool(row["active_identity"]) for row in rows
        ),
        "active_identity_residual_upper": (
            active_identity_residual_upper
        ),
        "minimum_catalog_denominator_lower": (
            diagnostics.minimum_denominator_lower
        ),
    }


def regularized_factorization_crosscheck(
    endpoint_row: dict[str, str],
) -> dict[str, Any]:
    x_value = float(endpoint_row["decay_cosine"])
    diagnostics = IntervalDiagnostics()
    state = interval_state(
        endpoint_row,
        x_value,
        x_value,
        branch_sign(endpoint_row),
        diagnostics,
    )
    branch = M5257.exact_branch(endpoint_row)
    _, _, numeric_internal = M5257.M5028.event_geometry(
        float(branch["soft_energy"]),
        complex(branch["soft_cosine"]),
        complex(branch["decay_cosine"]),
        complex(branch["relative_root"]),
    )
    displacement_value = 1.0e-4 * cmath.exp(0.317j)
    displacement = cpoint(displacement_value)
    unit_circle = state["global_root"] + displacement
    rotated_interval = rotate_internal_lightcone(
        state["internal_lightcone"],
        unit_circle,
    )
    interval_diagnostics = IntervalDiagnostics()
    regularized = factorized_d_hhh(
        rotated_interval,
        state["target"],
        state["hard_index"],
        unit_circle,
        state["global_root"],
        displacement,
        interval_diagnostics,
    )
    numeric_global_root = complex(branch["global_root"])
    rotated_numeric = M5257.M5024.rotate_internal(
        numeric_internal,
        numeric_global_root + displacement_value,
    )
    parent_value = (
        displacement_value
        * displacement_value
        * M5257.factorized_d_hhh(
            rotated_numeric,
            complex(-9.0, float(endpoint_row["epsilon"])),
            state["hard_index"],
        )
    )
    regularized_value = midpoint(regularized)
    relative_error = abs(
        regularized_value - parent_value
    ) / max(abs(parent_value), 1.0)
    return {
        "node_id": endpoint_row["node_id"],
        "epsilon_id": endpoint_row["epsilon_id"],
        "component_id": endpoint_row["component_id"],
        "decay_cosine": x_value,
        "displacement_real": displacement_value.real,
        "displacement_imaginary": displacement_value.imag,
        "parent_regularized_real": parent_value.real,
        "parent_regularized_imaginary": parent_value.imag,
        "interval_regularized_midpoint_real": regularized_value.real,
        "interval_regularized_midpoint_imaginary": (
            regularized_value.imag
        ),
        "relative_error": relative_error,
        "crosscheck_passed": relative_error <= 1.0e-8,
        "valid_for_boundary_error_claim": False,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }


def cauchy_coefficient_enclosure(
    state: dict[str, Any],
    endpoint_row: dict[str, str],
    x_lower: float,
    x_upper: float,
    cauchy_nodes: int,
    phase_arcs: int,
) -> tuple[Any, dict[str, Any]]:
    numeric_safe_radii = [
        numeric_safe_radius(endpoint_row, value)
        for value in (
            x_lower,
            0.5 * (x_lower + x_upper),
            x_upper,
        )
    ]
    root_separation = interval_root_separation(state)
    outer_radius = 0.2 * root_separation["catalog_radius"]
    inner_radius = 0.5 * outer_radius
    sample_diagnostics = IntervalDiagnostics()
    total = cpoint(0.0)
    for index in range(cauchy_nodes):
        phase = cmath.exp(
            2.0j * math.pi * (index + 0.317) / cauchy_nodes
        )
        displacement = cpoint(inner_radius * phase)
        try:
            total += d_times_direct(
                state,
                state["global_root"] + displacement,
                displacement,
                sample_diagnostics,
            )
        except IntervalSingularity as error:
            raise IntervalSingularity(
                f"inner_sample={index}: {error}"
            ) from error
    coefficient = total / cpoint(cauchy_nodes)

    def enclose_outer_arc(
        lower: float,
        upper: float,
        depth: int,
        arc_label: str,
        minimum_depth: int = 0,
    ) -> tuple[float, float, int, int]:
        angle = iv.mpf([lower, upper])
        displacement = iv.mpc(
            outer_radius * iv.cos(angle),
            outer_radius * iv.sin(angle),
        )
        arc_diagnostics = IntervalDiagnostics()
        try:
            value = d_times_direct(
                state,
                state["global_root"] + displacement,
                displacement,
                arc_diagnostics,
            )
        except IntervalSingularity as error:
            if depth >= MAXIMUM_PHASE_SPLIT_DEPTH:
                raise IntervalSingularity(
                    f"outer_arc={arc_label} depth={depth}: {error}"
                ) from error
            middle = 0.5 * (lower + upper)
            child_minimum_depth = min(
                MAXIMUM_PHASE_SPLIT_DEPTH,
                max(minimum_depth, depth + 2),
            )
            left = enclose_outer_arc(
                lower,
                middle,
                depth + 1,
                f"{arc_label}L",
                child_minimum_depth,
            )
            right = enclose_outer_arc(
                middle,
                upper,
                depth + 1,
                f"{arc_label}R",
                child_minimum_depth,
            )
            return (
                max(left[0], right[0]),
                min(left[1], right[1]),
                left[2] + right[2],
                max(left[3], right[3]),
            )
        if depth < minimum_depth:
            middle = 0.5 * (lower + upper)
            left = enclose_outer_arc(
                lower,
                middle,
                depth + 1,
                f"{arc_label}L",
                minimum_depth,
            )
            right = enclose_outer_arc(
                middle,
                upper,
                depth + 1,
                f"{arc_label}R",
                minimum_depth,
            )
            return (
                max(left[0], right[0]),
                min(left[1], right[1]),
                left[2] + right[2],
                max(left[3], right[3]),
            )
        return (
            upper_abs(value),
            arc_diagnostics.minimum_denominator_lower,
            1,
            depth,
        )

    outer_maximum = 0.0
    outer_minimum_denominator = math.inf
    outer_arc_leaf_count = 0
    outer_arc_maximum_depth = 0
    for arc_index in range(phase_arcs):
        lower = 2.0 * math.pi * arc_index / phase_arcs
        upper = 2.0 * math.pi * (arc_index + 1) / phase_arcs
        arc_result = enclose_outer_arc(
            lower,
            upper,
            0,
            str(arc_index),
        )
        outer_maximum = max(outer_maximum, arc_result[0])
        outer_minimum_denominator = min(
            outer_minimum_denominator,
            arc_result[1],
        )
        outer_arc_leaf_count += arc_result[2]
        outer_arc_maximum_depth = max(
            outer_arc_maximum_depth,
            arc_result[3],
        )
    ratio_power = (inner_radius / outer_radius) ** cauchy_nodes
    tail_bound = (
        outer_maximum
        * ratio_power
        / (1.0 - ratio_power)
    )
    return expanded(coefficient, tail_bound), {
        "inner_radius": inner_radius,
        "outer_radius": outer_radius,
        "minimum_numeric_safe_radius": min(numeric_safe_radii),
        "minimum_interval_root_separation_lower": (
            root_separation["minimum_root_separation_lower"]
        ),
        "interval_catalog_radius": root_separation["catalog_radius"],
        "interval_root_count": root_separation["root_count"],
        "interval_active_root_count": (
            root_separation["active_root_count"]
        ),
        "active_identity_natural_residual_upper": (
            root_separation["active_identity_residual_upper"]
        ),
        "minimum_catalog_denominator_lower": (
            root_separation["minimum_catalog_denominator_lower"]
        ),
        "outer_to_catalog_radius_ratio": (
            outer_radius / root_separation["catalog_radius"]
        ),
        "outer_circle_maximum": outer_maximum,
        "outer_arc_leaf_count": outer_arc_leaf_count,
        "outer_arc_maximum_depth": outer_arc_maximum_depth,
        "cauchy_tail_bound": tail_bound,
        "minimum_sample_denominator_lower": (
            sample_diagnostics.minimum_denominator_lower
        ),
        "minimum_outer_denominator_lower": (
            outer_minimum_denominator
        ),
    }


def interval_box(
    endpoint_row: dict[str, str],
    orientation_row: dict[str, str],
    transition_id: str,
    box_index: int,
    x_lower: float,
    x_upper: float,
    cauchy_nodes: int,
    phase_arcs: int,
    base_box_index: int | None = None,
    x_refinement_depth: int = 0,
    x_refinement_path: str = "",
) -> dict[str, Any]:
    diagnostics = IntervalDiagnostics()
    selected_branch_sign = branch_sign(endpoint_row)
    state = interval_state(
        endpoint_row,
        x_lower,
        x_upper,
        selected_branch_sign,
        diagnostics,
    )
    coefficient, cauchy = cauchy_coefficient_enclosure(
        state,
        endpoint_row,
        x_lower,
        x_upper,
        cauchy_nodes,
        phase_arcs,
    )
    orientation = int(orientation_row["local_residue_orientation"])
    winding = int(orientation_row["winding_difference"])
    numerator = safe_divide(
        cpoint(orientation * winding) * coefficient,
        state["relative_root"]
        * state["global_root"]
        * state["collision_jacobian"],
        diagnostics,
        "factorized_numerator_projection",
    )
    residue = safe_divide(
        numerator,
        state["channel_derivative"],
        diagnostics,
        "outer_residue_channel_derivative",
    )
    pole_real_lower, pole_real_upper = real_bounds(state["pole"])
    pole_imaginary_lower, pole_imaginary_upper = imaginary_bounds(
        state["pole"]
    )
    residue_real_lower, residue_real_upper = real_bounds(residue)
    residue_imaginary_lower, residue_imaginary_upper = (
        imaginary_bounds(residue)
    )
    return {
        "transition_id": transition_id,
        "active_endpoint_id": endpoint_row["node_id"],
        "component_id": endpoint_row["component_id"],
        "epsilon_id": endpoint_row["epsilon_id"],
        "box_index": box_index,
        "base_box_index": (
            box_index if base_box_index is None else base_box_index
        ),
        "x_refinement_depth": x_refinement_depth,
        "x_refinement_path": x_refinement_path,
        "x_lower": x_lower,
        "x_upper": x_upper,
        "box_width": x_upper - x_lower,
        "quadratic_branch_sign": selected_branch_sign,
        "pole_real_lower": pole_real_lower,
        "pole_real_upper": pole_real_upper,
        "pole_imaginary_lower": pole_imaginary_lower,
        "pole_imaginary_upper": pole_imaginary_upper,
        "natural_pole_box_width": state["natural_pole_box_width"],
        "tightened_pole_box_width": state["tightened_pole_box_width"],
        "quadratic_discriminant_abs_lower": lower_abs(
            state["discriminant"]
        ),
        "channel_derivative_abs_lower": lower_abs(
            state["channel_derivative"]
        ),
        "collision_jacobian_abs_lower": lower_abs(
            state["collision_jacobian"]
        ),
        "relative_root_abs_lower": lower_abs(
            state["relative_root"]
        ),
        "global_root_abs_lower": lower_abs(state["global_root"]),
        "numerator_abs_upper": upper_abs(numerator),
        "residue_abs_upper": upper_abs(residue),
        "residue_real_lower": residue_real_lower,
        "residue_real_upper": residue_real_upper,
        "residue_imaginary_lower": residue_imaginary_lower,
        "residue_imaginary_upper": residue_imaginary_upper,
        "minimum_interval_denominator_lower": (
            diagnostics.minimum_denominator_lower
        ),
        "cauchy_nodes": cauchy_nodes,
        "phase_arcs": phase_arcs,
        **cauchy,
        "interval_arithmetic_complete": True,
        "active_root_identities_parent_derived": True,
        "analytic_disk_root_separation_interval_proved": True,
        "valid_for_boundary_error_claim": True,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }


def execute(
    subdivisions: int,
    cauchy_nodes: int,
    phase_arcs: int,
    selected_transitions: set[str] | None,
    selected_epsilons: set[str] | None,
    dry_run: bool,
) -> dict[str, Any]:
    if subdivisions < 1:
        raise ValueError("subdivisions must be positive")
    if cauchy_nodes < 4:
        raise ValueError("cauchy nodes must be at least four")
    if phase_arcs < 8:
        raise ValueError("phase arcs must be at least eight")
    for required in (
        DENOMINATOR_ROWS,
        BRACKET_ROWS,
        ORIENTATION_ROWS,
    ):
        if not required.exists():
            raise RuntimeError(f"missing source: {required}")
    denominator_lookup = {
        (row["node_id"], row["epsilon_id"]): row
        for row in read_csv(DENOMINATOR_ROWS)
    }
    orientation_lookup = {
        (row["node_id"], row["epsilon_id"]): row
        for row in read_csv(ORIENTATION_ROWS)
    }
    brackets = {
        row["transition_id"]: row for row in read_csv(BRACKET_ROWS)
    }
    transitions = (
        sorted(selected_transitions)
        if selected_transitions is not None
        else sorted(ACTIVE_ENDPOINTS)
    )
    epsilons = (
        sorted(selected_epsilons)
        if selected_epsilons is not None
        else list(EPSILON_IDS)
    )
    regularization_rows = [
        regularized_factorization_crosscheck(
            denominator_lookup[
                (ACTIVE_ENDPOINTS[transition_id], epsilon_id)
            ]
        )
        for transition_id in transitions
        for epsilon_id in epsilons
    ]
    box_rows: list[dict[str, Any]] = []
    for transition_id in transitions:
        endpoint_id = ACTIVE_ENDPOINTS[transition_id]
        bracket = brackets[transition_id]
        lower = float(bracket["new_left_decay_cosine"])
        upper = float(bracket["new_right_decay_cosine"])
        step = (upper - lower) / subdivisions
        for epsilon_id in epsilons:
            endpoint_row = denominator_lookup[
                (endpoint_id, epsilon_id)
            ]
            orientation_row = orientation_lookup[
                (endpoint_id, epsilon_id)
            ]

            def evaluate_adaptive_box(
                base_index: int,
                x_lower: float,
                x_upper: float,
                depth: int = 0,
                path: str = "",
            ) -> list[dict[str, Any]]:
                box_label = f"{base_index}{path}"
                try:
                    return [
                        interval_box(
                            endpoint_row,
                            orientation_row,
                            transition_id,
                            box_label,
                            x_lower,
                            x_upper,
                            cauchy_nodes,
                            phase_arcs,
                            base_index,
                            depth,
                            path,
                        )
                    ]
                except IntervalSingularity as error:
                    if depth >= MAXIMUM_X_SPLIT_DEPTH:
                        raise IntervalSingularity(
                            f"transition={transition_id} "
                            f"epsilon={epsilon_id} box={box_label} "
                            f"x=[{x_lower},{x_upper}] depth={depth}: "
                            f"{error}"
                        ) from error
                    middle = 0.5 * (x_lower + x_upper)
                    return [
                        *evaluate_adaptive_box(
                            base_index,
                            x_lower,
                            middle,
                            depth + 1,
                            f"{path}L",
                        ),
                        *evaluate_adaptive_box(
                            base_index,
                            middle,
                            x_upper,
                            depth + 1,
                            f"{path}R",
                        ),
                    ]

            for index in range(subdivisions):
                x_lower = lower + index * step
                x_upper = lower + (index + 1) * step
                box_rows.extend(
                    evaluate_adaptive_box(
                        index,
                        x_lower,
                        x_upper,
                    )
                )

    transition_rows: list[dict[str, Any]] = []
    for transition_id in transitions:
        selected = [
            row
            for row in box_rows
            if row["transition_id"] == transition_id
        ]
        maxima = {
            epsilon_id: max(
                float(row["residue_abs_upper"])
                for row in selected
                if row["epsilon_id"] == epsilon_id
            )
            for epsilon_id in epsilons
        }
        if set(maxima) == set(EPSILON_IDS):
            envelope = HALF_RESIDUE_COEFFICIENT * (
                2.0 * maxima["E020"] + maxima["E040"]
            )
        else:
            envelope = math.nan
        width = (
            float(brackets[transition_id]["new_right_decay_cosine"])
            - float(brackets[transition_id]["new_left_decay_cosine"])
        )
        interval_complete = all(
            bool(row["interval_arithmetic_complete"])
            for row in selected
        )
        root_separation_complete = all(
            bool(row["analytic_disk_root_separation_interval_proved"])
            for row in selected
        )
        continuous_envelope_certified = (
            interval_complete
            and root_separation_complete
            and math.isfinite(envelope)
        )
        transition_rows.append(
            {
                "transition_id": transition_id,
                "active_endpoint_id": ACTIVE_ENDPOINTS[transition_id],
                "subdivision_count": subdivisions,
                "adaptive_box_count": len(selected),
                "maximum_x_refinement_depth": max(
                    int(row["x_refinement_depth"]) for row in selected
                ),
                "R20_abs_upper": maxima.get("E020", ""),
                "R40_abs_upper": maxima.get("E040", ""),
                "half_residue_triangle_envelope": envelope,
                "bracket_width": width,
                "boundary_location_error_upper": (
                    ANGULAR_JACOBIAN * width * envelope
                    if math.isfinite(envelope)
                    else ""
                ),
                "interval_arithmetic_complete": interval_complete,
                "active_root_identities_parent_derived": all(
                    bool(row["active_root_identities_parent_derived"])
                    for row in selected
                ),
                "analytic_disk_root_separation_interval_proved": (
                    root_separation_complete
                ),
                "continuous_envelope_certified": (
                    continuous_envelope_certified
                ),
                "valid_for_boundary_error_claim": (
                    continuous_envelope_certified
                ),
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )

    checks = [
        {
            "check_id": "REGULARIZED_FACTORIZATION_MATCHES_PARENT",
            "passed": all(
                bool(row["crosscheck_passed"])
                for row in regularization_rows
            ),
            "detail": (
                "maximum_relative_error="
                f"{max(float(row['relative_error']) for row in regularization_rows)}"
            ),
        },
        {
            "check_id": "ADAPTIVE_BOX_COVERAGE_COMPLETE",
            "passed": all(
                math.isclose(
                    sum(
                        float(row["x_upper"]) - float(row["x_lower"])
                        for row in box_rows
                        if row["transition_id"] == transition_id
                        and row["epsilon_id"] == epsilon_id
                    ),
                    float(brackets[transition_id]["new_right_decay_cosine"])
                    - float(brackets[transition_id]["new_left_decay_cosine"]),
                    rel_tol=0.0,
                    abs_tol=1.0e-14,
                )
                for transition_id in transitions
                for epsilon_id in epsilons
            ),
            "detail": (
                f"base_boxes={len(transitions) * len(epsilons) * subdivisions}; "
                f"adaptive_rows={len(box_rows)}"
            ),
        },
        {
            "check_id": "ALL_INTERVAL_DENOMINATORS_SEPARATED",
            "passed": all(
                float(row["minimum_interval_denominator_lower"]) > 0.0
                and float(row["minimum_sample_denominator_lower"]) > 0.0
                and float(row["minimum_outer_denominator_lower"]) > 0.0
                and float(row["minimum_catalog_denominator_lower"]) > 0.0
                for row in box_rows
            ),
            "detail": (
                "minimum_amplitude="
                f"{min(float(row['minimum_interval_denominator_lower']) for row in box_rows)}; "
                "minimum_catalog="
                f"{min(float(row['minimum_catalog_denominator_lower']) for row in box_rows)}"
            ),
        },
        {
            "check_id": "ALL_QUADRATIC_BRANCHES_SEPARATED",
            "passed": all(
                float(row["quadratic_discriminant_abs_lower"]) > 0.0
                for row in box_rows
            ),
            "detail": (
                f"minimum={min(float(row['quadratic_discriminant_abs_lower']) for row in box_rows)}"
            ),
        },
        {
            "check_id": "CAUCHY_TAIL_BOUNDS_FINITE",
            "passed": all(
                math.isfinite(float(row["cauchy_tail_bound"]))
                and float(row["cauchy_tail_bound"]) >= 0.0
                for row in box_rows
            ),
            "detail": (
                f"maximum={max(float(row['cauchy_tail_bound']) for row in box_rows)}"
            ),
        },
        {
            "check_id": "ANALYTIC_DISK_ROOT_SEPARATION_CERTIFIED",
            "passed": all(
                bool(
                    row[
                        "analytic_disk_root_separation_interval_proved"
                    ]
                )
                and float(
                    row["minimum_interval_root_separation_lower"]
                )
                > 0.0
                and int(row["interval_root_count"]) == 20
                and int(row["interval_active_root_count"]) == 3
                and float(row["outer_to_catalog_radius_ratio"])
                <= 0.2 + 1.0e-15
                for row in box_rows
            ),
            "detail": (
                "minimum_nonactive_root_separation="
                f"{min(float(row['minimum_interval_root_separation_lower']) for row in box_rows)}"
            ),
        },
        {
            "check_id": "BOUNDARY_ONLY_CLAIM_SCOPE",
            "passed": (
                all(
                    bool(row["valid_for_boundary_error_claim"])
                    and not bool(row["valid_for_numeric_UV_claim"])
                    and not bool(row["valid_for_local_GR_claim"])
                    and not bool(row["valid_for_full_MTS_claim"])
                    for row in box_rows
                )
                and all(
                    bool(row["valid_for_boundary_error_claim"])
                    == (set(epsilons) == set(EPSILON_IDS))
                    and not bool(row["valid_for_numeric_UV_claim"])
                    and not bool(row["valid_for_local_GR_claim"])
                    and not bool(row["valid_for_full_MTS_claim"])
                    for row in transition_rows
                )
            ),
            "detail": (
                "continuous boundary envelope is certified; "
                "UV, local-GR, and full-MTS claims remain false"
            ),
        },
    ]
    passed = all(bool(row["passed"]) for row in checks)
    boundary_claim_complete = (
        passed and set(epsilons) == set(EPSILON_IDS)
    )
    result = {
        "marker": "MTS_5258_CONTINUOUS_RESIDUE_ENCLOSURE_CERTIFICATE",
        "revision": "continuous-residue-enclosure-certificate-v2",
        "validation_passed": passed,
        "transition_count": len(transitions),
        "epsilon_count": len(epsilons),
        "box_count": len(box_rows),
        "subdivisions": subdivisions,
        "cauchy_nodes": cauchy_nodes,
        "phase_arcs": phase_arcs,
        "maximum_regularization_crosscheck_relative_error": max(
            float(row["relative_error"])
            for row in regularization_rows
        ),
        "maximum_x_refinement_depth": max(
            int(row["x_refinement_depth"]) for row in box_rows
        ),
        "minimum_quadratic_discriminant_abs_lower": min(
            float(row["quadratic_discriminant_abs_lower"])
            for row in box_rows
        ),
        "minimum_channel_derivative_abs_lower": min(
            float(row["channel_derivative_abs_lower"])
            for row in box_rows
        ),
        "minimum_interval_root_separation_lower": min(
            float(row["minimum_interval_root_separation_lower"])
            for row in box_rows
        ),
        "active_root_identities_parent_derived": passed,
        "maximum_residue_abs_upper": max(
            float(row["residue_abs_upper"]) for row in box_rows
        ),
        "maximum_cauchy_tail_bound": max(
            float(row["cauchy_tail_bound"]) for row in box_rows
        ),
        "interval_arithmetic_complete": passed,
        "analytic_disk_root_separation_interval_proved": passed,
        "continuous_residue_envelope_complete": (
            boundary_claim_complete
        ),
        "valid_for_boundary_error_claim": boundary_claim_complete,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    if not dry_run:
        write_csv(BOX_ROWS, box_rows)
        write_csv(TRANSITION_ROWS, transition_rows)
        write_csv(REGULARIZATION_ROWS, regularization_rows)
        write_csv(VALIDATION, checks)
        atomic_text(
            RESULT,
            json.dumps(result, indent=2, sort_keys=True) + "\n",
        )
    if not passed:
        failed = [
            row["check_id"] for row in checks if not row["passed"]
        ]
        raise RuntimeError(
            f"5258 interval pilot validation failed: {failed}"
        )
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--subdivisions", type=int, default=4)
    parser.add_argument("--cauchy-nodes", type=int, default=16)
    parser.add_argument("--phase-arcs", type=int, default=32)
    parser.add_argument("--transition-id", action="append")
    parser.add_argument("--epsilon-id", action="append")
    parser.add_argument("--dry-run", action="store_true")
    arguments = parser.parse_args()
    transitions = (
        set(arguments.transition_id)
        if arguments.transition_id
        else None
    )
    epsilons = (
        set(arguments.epsilon_id)
        if arguments.epsilon_id
        else None
    )
    print(
        json.dumps(
            execute(
                arguments.subdivisions,
                arguments.cauchy_nodes,
                arguments.phase_arcs,
                transitions,
                epsilons,
                arguments.dry_run,
            ),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
