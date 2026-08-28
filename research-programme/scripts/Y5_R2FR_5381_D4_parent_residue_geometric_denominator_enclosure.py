from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import re
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
OUTPUT = FUNCTIONAL_RG / "5381"
DOCUMENT = POST / "5381-Y5-R2FR-D4-parent-residue-geometric-denominator-enclosure.md"
VALIDATION = RESIDUALS / "P8_Y5_BRR545_5381_VALIDATION.csv"

SCRIPT_5380 = SCRIPTS / "Y5_R2FR_5380_D4_complexified_event_neighborhood_certificate.py"
RESULT_5380 = FUNCTIONAL_RG / "5380" / "D4_complexified_event_neighborhood_result.json"
VALIDATION_5380 = FUNCTIONAL_RG / "5380" / "D4_complexified_event_neighborhood_validation.csv"
BOXES_5380 = FUNCTIONAL_RG / "5380" / "D4_complexified_event_neighborhood_boxes.csv"
EVENTS_5358 = FUNCTIONAL_RG / "5358" / "D4_zero_regulator_event_certificate.csv"

CHECKPOINT = 5381
MARKER = "MTS_5381_D4_PARENT_RESIDUE_GEOMETRIC_DENOMINATOR_ENCLOSURE"
REVISION = "D4-parent-residue-geometric-denominator-enclosure-v1"
EVENT_IDS = tuple(f"E{index:02d}" for index in range(1, 9))
INTERVAL_DIGITS = 50

CLAIM_DENOMINATORS = "valid_for_D4_parent_residue_geometric_denominator_enclosure"
OPEN_CLAIMS = (
    "valid_for_D4_finite_plus_double_pole_coefficient_enclosure",
    "valid_for_D4_endpoint_C_regulator_zero_limit",
    "valid_for_D4_numeric_H3_bound",
    "valid_for_D4_numeric_uniform_remainder_bound",
    "valid_for_D4_outer_regulator_zero_limit",
    "valid_for_decay_angle_integral",
    "valid_for_full_angular_convergence",
    "valid_for_full_phase_space_coefficient",
    "valid_for_numeric_UV_claim",
    "valid_for_local_GR_claim",
    "valid_for_full_MTS_claim",
)
BOX_PATTERN = re.compile(
    r"^\[([^,]+),([^\]]+)\]\+i\[([^,]+),([^\]]+)\]$"
)


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5380 = load_module("mts_5380_for_5381", SCRIPT_5380)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
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
    temporary.replace(path)


def atomic_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    temporary.replace(path)


def validation_row(gate: str, passed: bool, detail: Any) -> dict[str, Any]:
    return {"gate": gate, "passed": bool(passed), "detail": str(detail)}


def open_claims() -> dict[str, bool]:
    return {claim: False for claim in OPEN_CLAIMS}


def parse_complex_box(text: str) -> Any:
    match = BOX_PATTERN.fullmatch(text.strip())
    if match is None:
        raise ValueError(f"invalid complex box {text}")
    real_lower, real_upper, imaginary_lower, imaginary_upper = match.groups()
    return iv.mpc(
        iv.mpf([real_lower, real_upper]),
        iv.mpf([imaginary_lower, imaginary_upper]),
    )


def interval_real(value: Any) -> Any:
    return iv.mpf([M5380.real_lower(value), M5380.real_upper(value)])


def interval_imaginary(value: Any) -> Any:
    return iv.mpf([M5380.imaginary_lower(value), M5380.imaginary_upper(value)])


def positive_complex_sqrt(value: Any) -> Any:
    real_part = interval_real(value)
    imaginary_part = interval_imaginary(value)
    if M5380.real_lower(value) <= 0:
        raise ValueError("positive complex square-root chart crossed its cut")
    modulus = iv.sqrt(real_part * real_part + imaginary_part * imaginary_part)
    real_root = iv.sqrt((modulus + real_part) / 2)
    imaginary_root = imaginary_part / (2 * real_root)
    return iv.mpc(real_root, imaginary_root)


def modulus_lower(value: Any) -> float:
    real_lower = M5380.real_lower(value)
    real_upper = M5380.real_upper(value)
    imaginary_lower = M5380.imaginary_lower(value)
    imaginary_upper = M5380.imaginary_upper(value)
    real_distance = (
        0.0
        if real_lower <= 0 <= real_upper
        else min(abs(real_lower), abs(real_upper))
    )
    imaginary_distance = (
        0.0
        if imaginary_lower <= 0 <= imaginary_upper
        else min(abs(imaginary_lower), abs(imaginary_upper))
    )
    return math.hypot(real_distance, imaginary_distance)


def modulus_upper(value: Any) -> float:
    real_radius = max(abs(M5380.real_lower(value)), abs(M5380.real_upper(value)))
    imaginary_radius = max(
        abs(M5380.imaginary_lower(value)), abs(M5380.imaginary_upper(value))
    )
    return math.hypot(real_radius, imaginary_radius)


def contains_zero(value: Any) -> bool:
    return (
        M5380.real_lower(value) <= 0 <= M5380.real_upper(value)
        and M5380.imaginary_lower(value) <= 0 <= M5380.imaginary_upper(value)
    )


class IntervalDual:
    __slots__ = ("value", "derivative")

    def __init__(self, value: Any, derivative: Any = 0) -> None:
        self.value = value
        self.derivative = derivative

    @staticmethod
    def coerce(value: Any) -> "IntervalDual":
        return value if isinstance(value, IntervalDual) else IntervalDual(value)

    def __add__(self, other: Any) -> "IntervalDual":
        other = self.coerce(other)
        return IntervalDual(
            self.value + other.value, self.derivative + other.derivative
        )

    __radd__ = __add__

    def __neg__(self) -> "IntervalDual":
        return IntervalDual(-self.value, -self.derivative)

    def __sub__(self, other: Any) -> "IntervalDual":
        return self + (-self.coerce(other))

    def __rsub__(self, other: Any) -> "IntervalDual":
        return self.coerce(other) - self

    def __mul__(self, other: Any) -> "IntervalDual":
        other = self.coerce(other)
        return IntervalDual(
            self.value * other.value,
            self.derivative * other.value + self.value * other.derivative,
        )

    __rmul__ = __mul__

    def __truediv__(self, other: Any) -> "IntervalDual":
        other = self.coerce(other)
        inverse = 1 / other.value
        quotient = self.value * inverse
        return IntervalDual(
            quotient,
            (self.derivative - quotient * other.derivative) * inverse,
        )

    def __rtruediv__(self, other: Any) -> "IntervalDual":
        return self.coerce(other) / self


def relative_root_geometry(
    configuration: dict[str, Any], epsilon: Any, state_boxes: list[Any]
) -> dict[str, Any]:
    recoil = state_boxes[0] + 1j * state_boxes[1]
    coordinate_index = 2 if configuration["event_type"] == "BRANCH_DEATH" else 3
    coordinate = state_boxes[coordinate_index]
    soft_cosine = configuration["sign"] * coordinate
    if configuration["event_type"] == "BRANCH_DEATH":
        soft_sine = positive_complex_sqrt(1 - soft_cosine**2)
    else:
        soft_sine = state_boxes[4]
    decay_cosine = iv.mpc(configuration["decay_cosine"])
    decay_sine = iv.mpc(math.sqrt(1 - float(configuration["decay_cosine"]) ** 2))
    epsilon_squared = epsilon**2
    q_real = -(80 + epsilon_squared) / (64 + epsilon_squared)
    q_imaginary = -2 * epsilon / (64 + epsilon_squared)
    q_value = q_real + 1j * q_imaginary
    factor_f1 = (
        q_value * recoil * soft_cosine
        + q_value * recoil
        - q_value * soft_cosine
        - q_value
        + recoil * soft_cosine
        + recoil
        - soft_cosine
        + 1
    )
    factor_f2 = (
        q_value * recoil * soft_cosine
        - q_value * recoil
        - q_value * soft_cosine
        - q_value
        + recoil * soft_cosine
        - recoil
        - soft_cosine
        + 1
    )
    relative_denominator = decay_sine * (1 + soft_cosine) * factor_f2
    representative = (
        soft_sine * (1 + decay_cosine) * factor_f1 / relative_denominator
    )
    relative = 1 / representative if configuration["role"] == "reciprocal" else representative
    return {
        "recoil": recoil,
        "energy": 1 - recoil**2,
        "soft_cosine": soft_cosine,
        "soft_sine": soft_sine,
        "decay_cosine": decay_cosine,
        "decay_sine": decay_sine,
        "q_value": q_value,
        "relative_formula_denominator": relative_denominator,
        "representative_relative_root": representative,
        "relative_root": relative,
    }


def event_geometry(
    energy: Any,
    recoil: Any,
    soft_cosine: Any,
    soft_sine: Any,
    decay_cosine: Any,
    decay_sine: Any,
    relative_root: IntervalDual,
) -> tuple[list[IntervalDual], list[IntervalDual], list[list[IntervalDual]]]:
    azimuth_cosine = (relative_root + 1 / relative_root) / 2
    azimuth_sine = (relative_root - 1 / relative_root) / (2j)
    soft_direction = [
        IntervalDual(soft_sine),
        IntervalDual(iv.mpc(0)),
        IntervalDual(soft_cosine),
    ]
    decay_direction = [
        azimuth_cosine * decay_sine,
        azimuth_sine * decay_sine,
        IntervalDual(decay_cosine),
    ]
    relative_cosine = sum(
        (
            soft_direction[index] * decay_direction[index]
            for index in range(3)
        ),
        IntervalDual(iv.mpc(0)),
    )
    beta = energy / (2 - energy)
    gamma = (2 - energy) / (2 * recoil)
    gamma_beta = energy / (2 * recoil)
    internal: list[list[IntervalDual]] = []
    for sign in (1, -1):
        local_energy = (1 - relative_cosine * (sign * beta)) * (gamma * recoil)
        spatial = [
            (
                sign * decay_direction[index]
                + (
                    relative_cosine * (sign * (gamma - 1)) - gamma_beta
                )
                * soft_direction[index]
            )
            * recoil
            for index in range(3)
        ]
        internal.append([local_energy, *spatial])
    internal.append(
        [
            IntervalDual(energy),
            *[direction * energy for direction in soft_direction],
        ]
    )
    return soft_direction, decay_direction, internal


def preferred_chart(
    primary_numerator: IntervalDual,
    primary_denominator: IntervalDual,
    alternate_numerator: IntervalDual,
    alternate_denominator: IntervalDual,
) -> tuple[IntervalDual, IntervalDual, str]:
    if modulus_lower(alternate_denominator.value) > modulus_lower(primary_denominator.value):
        return (
            alternate_numerator,
            alternate_denominator,
            "opposite_stereographic_chart",
        )
    return (
        primary_numerator,
        primary_denominator,
        "primary_stereographic_chart",
    )


def preferred_inverse_chart(
    primary_numerator: IntervalDual,
    primary_denominator: IntervalDual,
    alternate_numerator: IntervalDual,
    alternate_denominator: IntervalDual,
) -> tuple[IntervalDual, IntervalDual, str]:
    if modulus_lower(alternate_numerator.value) > modulus_lower(primary_numerator.value):
        return (
            alternate_numerator,
            alternate_denominator,
            "opposite_stereographic_chart",
        )
    return (
        primary_numerator,
        primary_denominator,
        "primary_stereographic_chart",
    )


def global_root(
    momentum: list[IntervalDual], label: str, external_root: Any
) -> tuple[IntervalDual, list[Any], str, Any]:
    energy, momentum_x, momentum_y, momentum_z = momentum
    primary_denominator = energy + momentum_z
    holomorphic_numerator, holomorphic_denominator, holomorphic_chart = preferred_inverse_chart(
        momentum_x + 1j * momentum_y,
        primary_denominator,
        energy - momentum_z,
        momentum_x - 1j * momentum_y,
    )
    antiholomorphic_numerator, antiholomorphic_denominator, antiholomorphic_chart = preferred_chart(
        momentum_x - 1j * momentum_y,
        primary_denominator,
        energy - momentum_z,
        momentum_x + 1j * momentum_y,
    )
    denominators: list[Any] = []
    if label == "plus_u":
        denominators.append(holomorphic_numerator.value)
        root = (holomorphic_denominator / holomorphic_numerator) * external_root
        chart = holomorphic_chart
    elif label == "plus_v":
        denominators.extend((antiholomorphic_denominator.value, external_root))
        root = (antiholomorphic_numerator / antiholomorphic_denominator) / external_root
        chart = antiholomorphic_chart
    elif label == "minus_u":
        denominators.extend((external_root, holomorphic_numerator.value))
        root = (-(holomorphic_denominator / holomorphic_numerator)) / external_root
        chart = holomorphic_chart
    elif label == "minus_v":
        denominators.append(antiholomorphic_denominator.value)
        root = (antiholomorphic_numerator / antiholomorphic_denominator) * (-external_root)
        chart = antiholomorphic_chart
    else:
        raise ValueError(f"unsupported global-root label {label}")
    null_residual = (
        energy * energy
        - momentum_x * momentum_x
        - momentum_y * momentum_y
        - momentum_z * momentum_z
    )
    return root, denominators, chart, null_residual.value


def preferred_root_ratio(
    primary_numerator: IntervalDual,
    primary_denominator: IntervalDual,
    primary_name: str,
    alternate_numerator: IntervalDual,
    alternate_denominator: IntervalDual,
    alternate_name: str,
) -> tuple[IntervalDual, Any, str]:
    if modulus_lower(alternate_denominator.value) > modulus_lower(
        primary_denominator.value
    ):
        return (
            alternate_numerator / alternate_denominator,
            alternate_denominator.value,
            alternate_name,
        )
    return (
        primary_numerator / primary_denominator,
        primary_denominator.value,
        primary_name,
    )


def reduced_collision_roots(
    relative: dict[str, Any],
    relative_dual: IntervalDual,
    root_labels: tuple[str, str],
    external_root: Any,
) -> tuple[IntervalDual, IntervalDual, list[Any], list[Any], str, str, Any, Any]:
    recoil = relative["recoil"]
    soft_cosine = relative["soft_cosine"]
    soft_sine = relative["soft_sine"]
    decay_cosine = relative["decay_cosine"]
    decay_sine = relative["decay_sine"]
    azimuth_cosine = (relative_dual + 1 / relative_dual) / 2
    relative_cosine = (
        azimuth_cosine * (soft_sine * decay_sine)
        + soft_cosine * decay_cosine
    )
    recoil_squared = recoil**2
    first_energy = (
        IntervalDual(1 + recoil_squared)
        - relative_cosine * (1 - recoil_squared)
    ) / 2
    longitudinal_coefficient = (
        relative_cosine * (1 - recoil) ** 2 - (1 - recoil_squared)
    ) / 2
    holomorphic_numerator = (
        relative_dual * (recoil * decay_sine)
        + longitudinal_coefficient * soft_sine
    )
    antiholomorphic_numerator = (
        (1 / relative_dual) * (recoil * decay_sine)
        + longitudinal_coefficient * soft_sine
    )
    longitudinal_momentum = (
        longitudinal_coefficient * soft_cosine
        + recoil * decay_cosine
    )
    plus_denominator = first_energy + longitudinal_momentum
    minus_denominator = first_energy - longitudinal_momentum
    first_label, second_label = root_labels
    if first_label == "minus_u":
        first_ratio, first_denominator, first_chart = preferred_root_ratio(
            plus_denominator,
            holomorphic_numerator,
            "primary_stereographic_chart",
            antiholomorphic_numerator,
            minus_denominator,
            "opposite_stereographic_chart",
        )
        first_root = (-first_ratio) / external_root
        first_denominators = [first_denominator, external_root]
    elif first_label == "minus_v":
        first_ratio, first_denominator, first_chart = preferred_root_ratio(
            antiholomorphic_numerator,
            plus_denominator,
            "primary_stereographic_chart",
            minus_denominator,
            holomorphic_numerator,
            "opposite_stereographic_chart",
        )
        first_root = first_ratio * (-external_root)
        first_denominators = [first_denominator]
    else:
        raise ValueError(f"unsupported first collision label {first_label}")
    if second_label == "plus_u":
        second_root = IntervalDual(
            external_root * (1 + soft_cosine) / soft_sine
        )
        second_denominators = [soft_sine]
        second_chart = "soft_direction_closed_form"
    elif second_label == "plus_v":
        second_root = IntervalDual(
            soft_sine / ((1 + soft_cosine) * external_root)
        )
        second_denominators = [1 + soft_cosine, external_root]
        second_chart = "soft_direction_closed_form"
    else:
        raise ValueError(f"unsupported second collision label {second_label}")
    first_null_residual = (
        plus_denominator * minus_denominator
        - holomorphic_numerator * antiholomorphic_numerator
    ).value
    second_null_residual = soft_sine**2 + soft_cosine**2 - 1
    return (
        first_root,
        second_root,
        first_denominators,
        second_denominators,
        first_chart,
        second_chart,
        first_null_residual,
        second_null_residual,
    )


def geometric_denominator_certificate(
    configuration: dict[str, Any], epsilon: Any, state_boxes: list[Any]
) -> dict[str, Any]:
    relative = relative_root_geometry(configuration, epsilon, state_boxes)
    target = -9 + 1j * epsilon
    q_value = relative["q_value"]
    external_root = -1j * positive_complex_sqrt(-q_value)
    relative_dual = IntervalDual(relative["relative_root"], iv.mpc(1))
    (
        first_root,
        second_root,
        first_denominators,
        second_denominators,
        first_chart,
        second_chart,
        first_null_residual,
        second_null_residual,
    ) = reduced_collision_roots(
        relative,
        relative_dual,
        configuration["root_labels"],
        external_root,
    )
    selected_global_root = (first_root.value + second_root.value) / 2
    collision_root_difference = first_root.value - second_root.value
    collision_jacobian = first_root.derivative - second_root.derivative
    geometric_denominator = (
        relative["relative_root"] * selected_global_root * collision_jacobian
    )
    relative_root_lower = modulus_lower(relative["relative_root"])
    selected_global_root_lower = modulus_lower(selected_global_root)
    collision_jacobian_lower = modulus_lower(collision_jacobian)
    geometric_denominator_factorized_lower = (
        relative_root_lower
        * selected_global_root_lower
        * collision_jacobian_lower
    )
    primitive_denominators = [
        64 + epsilon**2,
        relative["recoil"],
        2 - relative["energy"],
        relative["relative_formula_denominator"],
        relative["representative_relative_root"],
        relative["relative_root"],
        external_root,
        *first_denominators,
        *second_denominators,
        selected_global_root,
        collision_jacobian,
    ]
    denominator_lower_bounds = [modulus_lower(value) for value in primitive_denominators]
    return {
        **relative,
        "target": target,
        "external_root": external_root,
        "first_global_root": first_root.value,
        "second_global_root": second_root.value,
        "selected_global_root": selected_global_root,
        "collision_root_difference": collision_root_difference,
        "collision_jacobian": collision_jacobian,
        "geometric_denominator": geometric_denominator,
        "first_global_root_chart": first_chart,
        "second_global_root_chart": second_chart,
        "first_internal_null_residual": first_null_residual,
        "second_internal_null_residual": second_null_residual,
        "minimum_primitive_denominator_modulus_lower": min(
            denominator_lower_bounds
        ),
        "relative_formula_denominator_modulus_lower": modulus_lower(
            relative["relative_formula_denominator"]
        ),
        "representative_relative_root_modulus_lower": modulus_lower(
            relative["representative_relative_root"]
        ),
        "relative_root_modulus_lower": relative_root_lower,
        "external_root_modulus_lower": modulus_lower(external_root),
        "minimum_global_chart_denominator_modulus_lower": min(
            modulus_lower(value)
            for value in (*first_denominators, *second_denominators)
        ),
        "selected_global_root_modulus_lower": selected_global_root_lower,
        "collision_jacobian_modulus_lower": collision_jacobian_lower,
        "geometric_denominator_modulus_lower": geometric_denominator_factorized_lower,
        "raw_rectangular_geometric_product_modulus_lower": modulus_lower(
            geometric_denominator
        ),
        "collision_root_difference_modulus_upper": modulus_upper(
            collision_root_difference
        ),
        "collision_root_difference_contains_zero": contains_zero(
            collision_root_difference
        ),
        "both_internal_null_residuals_contain_zero": contains_zero(
            first_null_residual
        )
        and contains_zero(second_null_residual),
        "all_required_denominators_exclude_zero": all(
            lower_bound > 0 for lower_bound in denominator_lower_bounds
        )
        and geometric_denominator_factorized_lower > 0,
    }


def source_paths() -> tuple[Path, ...]:
    paths = (
        Path(__file__).resolve(),
        SCRIPT_5380,
        RESULT_5380,
        VALIDATION_5380,
        BOXES_5380,
        EVENTS_5358,
        Path(M5380.M5379.M5378.__file__).resolve(),
        Path(M5380.M5379.M5378.M5359.__file__).resolve(),
        Path(M5380.M5379.M5378.AMP.__file__).resolve(),
    )
    return tuple(dict.fromkeys(path.resolve() for path in paths))


def source_rows() -> list[dict[str, Any]]:
    return [
        {
            "path": str(path),
            "exists": path.is_file(),
            "sha256": digest(path) if path.is_file() else "MISSING",
            CLAIM_DENOMINATORS: False,
            **open_claims(),
        }
        for path in source_paths()
    ]


def preflight() -> dict[str, Any]:
    paths = source_paths()
    result_5380 = read_json(RESULT_5380)
    boxes = read_csv(BOXES_5380)
    checks = {
        "all_direct_sources_exist": all(path.is_file() for path in paths),
        "checkpoint_5380_passes": result_5380.get("validation_passed") is True
        and all(parse_bool(row["passed"]) for row in read_csv(VALIDATION_5380)),
        "complex_event_neighborhood_is_claimed": result_5380.get(
            "claim_boundary", {}
        ).get("valid_for_D4_common_closed_complex_event_neighborhood")
        is True,
        "all_64_source_boxes_pass": len(boxes) == 64
        and all(parse_bool(row["complex_neighborhood_box_passes"]) for row in boxes),
        "formal_workbench_inventory_is_unchanged": M5380.M5379.M5378.M5359.M5342.M5283.formal_inventory_digest()
        == M5380.M5379.M5378.M5359.M5342.FORMAL_DIGEST,
        "scripts_cache_is_absent": not (SCRIPTS / "__pycache__").exists(),
    }
    return {"checks": checks, "all_pass": all(checks.values())}


def render_document(result: dict[str, Any]) -> None:
    lines = [
        "# 5381 — Y5/R2FR D4 parent-residue geometric denominator enclosure",
        "",
        "## Result",
        "",
        f"Decision: `{result['decision']}`.",
        "",
        "The 5380 complex event boxes are mapped through the actual analytic parent geometry. The calculation reconstructs the physical recoil and regulator ratio, relative-circle root, both colliding global roots, their derivative with respect to the relative circle, and the complete explicit geometric residue denominator `y z J`.",
        "",
        f"- certified boxes: `{result['certified_box_count']}/{result['required_box_count']}`;",
        f"- minimum primitive denominator modulus lower bound: `{result['minimum_primitive_denominator_modulus_lower']}`;",
        f"- minimum collision-Jacobian modulus lower bound: `{result['minimum_collision_jacobian_modulus_lower']}`;",
        f"- minimum full `|y z J|` lower bound: `{result['minimum_geometric_denominator_modulus_lower']}`;",
        f"- maximum colliding-root mismatch enclosure radius: `{result['maximum_collision_root_difference_modulus_upper']}`.",
        "",
        "## Meaning",
        "",
        "No relative-root, regulator, recoil, stereographic-chart, global-root, collision-Jacobian, or combined geometric denominator crosses zero anywhere in the common complex strip. Opposite stereographic charts are used where the primary chart meets a pole; the interval null identities certify the chart transition. The collision-root difference enclosure contains zero on every box, tying the denominator evaluation to the certified event branch rather than an unrelated nearby configuration.",
        "",
        "## Scope",
        "",
        "This is the geometric denominator half of the parent residue. The finite-plus spinor amplitude and its double-pole coefficient are not yet interval-enclosed, so endpoint C, H3, the uniform remainder, the D4 outer limit, and broader MTS/GR claims remain false.",
        "",
    ]
    temporary = DOCUMENT.with_suffix(DOCUMENT.suffix + ".tmp")
    temporary.write_text("\n".join(lines), encoding="utf-8")
    temporary.replace(DOCUMENT)


def run(output: Path) -> dict[str, Any]:
    started = time.perf_counter()
    M5380.set_below_normal_priority()
    iv.dps = INTERVAL_DIGITS
    preflight_result = preflight()
    if not preflight_result["all_pass"]:
        raise RuntimeError(f"preflight failed: {preflight_result}")
    references, _ = M5380.M5379.M5378.M5359.reference_rows()
    events = read_csv(EVENTS_5358)
    event_lookup = {row["event_id"]: row for row in events}
    rows: list[dict[str, Any]] = []
    for source in read_csv(BOXES_5380):
        event = event_lookup[source["event_id"]]
        configuration = M5380.M5379.M5378.M5359.event_configuration(
            event, references
        )
        epsilon = iv.mpc(
            iv.mpf([source["epsilon_real_lower"], source["epsilon_real_upper"]]),
            iv.mpf(
                [
                    source["epsilon_imaginary_lower"],
                    source["epsilon_imaginary_upper"],
                ]
            ),
        )
        state_boxes = [
            parse_complex_box(text)
            for text in source["complex_state_boxes"].split("|")
        ]
        certificate = geometric_denominator_certificate(
            configuration, epsilon, state_boxes
        )
        box_passes = (
            certificate["all_required_denominators_exclude_zero"]
            and certificate["collision_root_difference_contains_zero"]
            and certificate["both_internal_null_residuals_contain_zero"]
        )
        rows.append(
            {
                "event_id": configuration["event_id"],
                "event_type": configuration["event_type"],
                "epsilon_bin_index": source["epsilon_bin_index"],
                "epsilon_real_lower": source["epsilon_real_lower"],
                "epsilon_real_upper": source["epsilon_real_upper"],
                "epsilon_imaginary_lower": source["epsilon_imaginary_lower"],
                "epsilon_imaginary_upper": source["epsilon_imaginary_upper"],
                "selected_role": configuration["role"],
                "selected_root_labels": "|".join(configuration["root_labels"]),
                "first_global_root_chart": certificate["first_global_root_chart"],
                "second_global_root_chart": certificate["second_global_root_chart"],
                "q_box": M5380.complex_interval_text(certificate["q_value"]),
                "recoil_box": M5380.complex_interval_text(certificate["recoil"]),
                "soft_cosine_box": M5380.complex_interval_text(
                    certificate["soft_cosine"]
                ),
                "soft_sine_box": M5380.complex_interval_text(
                    certificate["soft_sine"]
                ),
                "representative_relative_root_box": M5380.complex_interval_text(
                    certificate["representative_relative_root"]
                ),
                "relative_root_box": M5380.complex_interval_text(
                    certificate["relative_root"]
                ),
                "first_global_root_box": M5380.complex_interval_text(
                    certificate["first_global_root"]
                ),
                "second_global_root_box": M5380.complex_interval_text(
                    certificate["second_global_root"]
                ),
                "selected_global_root_box": M5380.complex_interval_text(
                    certificate["selected_global_root"]
                ),
                "collision_root_difference_box": M5380.complex_interval_text(
                    certificate["collision_root_difference"]
                ),
                "first_internal_null_residual_box": M5380.complex_interval_text(
                    certificate["first_internal_null_residual"]
                ),
                "second_internal_null_residual_box": M5380.complex_interval_text(
                    certificate["second_internal_null_residual"]
                ),
                "collision_jacobian_box": M5380.complex_interval_text(
                    certificate["collision_jacobian"]
                ),
                "geometric_denominator_box": M5380.complex_interval_text(
                    certificate["geometric_denominator"]
                ),
                "minimum_primitive_denominator_modulus_lower": certificate[
                    "minimum_primitive_denominator_modulus_lower"
                ],
                "relative_formula_denominator_modulus_lower": certificate[
                    "relative_formula_denominator_modulus_lower"
                ],
                "representative_relative_root_modulus_lower": certificate[
                    "representative_relative_root_modulus_lower"
                ],
                "relative_root_modulus_lower": certificate[
                    "relative_root_modulus_lower"
                ],
                "external_root_modulus_lower": certificate[
                    "external_root_modulus_lower"
                ],
                "minimum_global_chart_denominator_modulus_lower": certificate[
                    "minimum_global_chart_denominator_modulus_lower"
                ],
                "selected_global_root_modulus_lower": certificate[
                    "selected_global_root_modulus_lower"
                ],
                "collision_jacobian_modulus_lower": certificate[
                    "collision_jacobian_modulus_lower"
                ],
                "geometric_denominator_modulus_lower": certificate[
                    "geometric_denominator_modulus_lower"
                ],
                "raw_rectangular_geometric_product_modulus_lower": certificate[
                    "raw_rectangular_geometric_product_modulus_lower"
                ],
                "collision_root_difference_modulus_upper": certificate[
                    "collision_root_difference_modulus_upper"
                ],
                "collision_root_difference_contains_zero": certificate[
                    "collision_root_difference_contains_zero"
                ],
                "both_internal_null_residuals_contain_zero": certificate[
                    "both_internal_null_residuals_contain_zero"
                ],
                "all_required_denominators_exclude_zero": certificate[
                    "all_required_denominators_exclude_zero"
                ],
                "geometric_denominator_box_passes": box_passes,
                CLAIM_DENOMINATORS: False,
                **open_claims(),
            }
        )
    required_count = len(EVENT_IDS) * M5380.EPSILON_BIN_COUNT
    certified_count = sum(
        parse_bool(row["geometric_denominator_box_passes"]) for row in rows
    )
    minimum_primitive = min(
        float(row["minimum_primitive_denominator_modulus_lower"])
        for row in rows
    )
    minimum_collision_jacobian = min(
        float(row["collision_jacobian_modulus_lower"]) for row in rows
    )
    minimum_geometric = min(
        float(row["geometric_denominator_modulus_lower"]) for row in rows
    )
    maximum_collision_mismatch = max(
        float(row["collision_root_difference_modulus_upper"]) for row in rows
    )
    validations = [
        validation_row(
            "preflight_passes", preflight_result["all_pass"], preflight_result["checks"]
        ),
        validation_row(
            "all_required_boxes_are_present",
            len(rows) == required_count,
            f"rows={len(rows)};required={required_count}",
        ),
        validation_row(
            "every_parent_geometric_denominator_box_passes",
            certified_count == required_count,
            f"certified={certified_count};required={required_count}",
        ),
        validation_row(
            "all_primitive_denominators_exclude_zero",
            minimum_primitive > 0,
            minimum_primitive,
        ),
        validation_row(
            "all_collision_jacobians_exclude_zero",
            minimum_collision_jacobian > 0,
            minimum_collision_jacobian,
        ),
        validation_row(
            "all_full_geometric_denominators_exclude_zero",
            minimum_geometric > 0,
            minimum_geometric,
        ),
        validation_row(
            "all_collision_root_differences_enclose_zero",
            all(
                parse_bool(row["collision_root_difference_contains_zero"])
                for row in rows
            ),
            f"boxes={len(rows)}",
        ),
        validation_row(
            "all_internal_null_residuals_enclose_zero",
            all(
                parse_bool(row["both_internal_null_residuals_contain_zero"])
                for row in rows
            ),
            f"boxes={len(rows)}",
        ),
        validation_row(
            "finite_plus_H3_and_downstream_claims_remain_false",
            all(value is False for value in open_claims().values()),
            open_claims(),
        ),
        validation_row(
            "formal_workbench_remains_unchanged",
            M5380.M5379.M5378.M5359.M5342.M5283.formal_inventory_digest()
            == M5380.M5379.M5378.M5359.M5342.FORMAL_DIGEST,
            M5380.M5379.M5378.M5359.M5342.M5283.formal_inventory_digest(),
        ),
        validation_row(
            "scripts_cache_remains_absent",
            not (SCRIPTS / "__pycache__").exists(),
            SCRIPTS / "__pycache__",
        ),
    ]
    passed = all(parse_bool(row["passed"]) for row in validations)
    for row in rows:
        row[CLAIM_DENOMINATORS] = passed
    registered_sources = source_rows()
    for row in registered_sources:
        row[CLAIM_DENOMINATORS] = passed
    result = {
        "checkpoint": CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "validation_passed": passed,
        "decision": (
            "D4_PARENT_RESIDUE_GEOMETRIC_DENOMINATORS_CERTIFIED__ENCLOSE_FINITE_PLUS_DOUBLE_POLE_COEFFICIENT"
            if passed
            else "D4_PARENT_RESIDUE_GEOMETRIC_DENOMINATOR_ENCLOSURE_BLOCKED"
        ),
        "required_box_count": required_count,
        "certified_box_count": certified_count,
        "minimum_primitive_denominator_modulus_lower": minimum_primitive,
        "minimum_collision_jacobian_modulus_lower": minimum_collision_jacobian,
        "minimum_geometric_denominator_modulus_lower": minimum_geometric,
        "maximum_collision_root_difference_modulus_upper": maximum_collision_mismatch,
        "claim_boundary": {CLAIM_DENOMINATORS: passed, **open_claims()},
        "remaining_obstruction": "interval-enclose the finite-plus spinor amplitude double-pole coefficient on the certified geometry, then bound endpoint H derivatives by Cauchy or direct interval jets",
        "formalization_workbench_modified_file_count": 0,
        "runtime_seconds": time.perf_counter() - started,
        "updated_utc": utc_now(),
    }
    output = output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    atomic_csv(output / "D4_parent_residue_geometric_denominator_boxes.csv", rows)
    atomic_csv(output / "D4_parent_residue_geometric_denominator_validation.csv", validations)
    atomic_csv(output / "source_register.csv", registered_sources)
    atomic_csv(VALIDATION, validations)
    atomic_json(output / "D4_parent_residue_geometric_denominator_result.json", result)
    atomic_json(
        output / "status.json",
        {
            "checkpoint": CHECKPOINT,
            "state": "complete" if passed else "blocked",
            "decision": result["decision"],
            "updated_utc": result["updated_utc"],
        },
    )
    render_document(result)
    return result


def self_test() -> dict[str, Any]:
    iv.dps = 30
    variable = IntervalDual(iv.mpc(2), iv.mpc(1))
    expression = variable + 1 / variable
    root = positive_complex_sqrt(iv.mpc(iv.mpf([1.21, 1.21]), iv.mpf([0, 0])))
    checks = {
        "dual_value_is_two_point_five": abs(
            M5380.complex_midpoint(expression.value) - 2.5
        )
        <= 1.0e-14,
        "dual_derivative_is_three_quarters": abs(
            M5380.complex_midpoint(expression.derivative) - 0.75
        )
        <= 1.0e-14,
        "positive_complex_square_root_is_one_point_one": abs(
            M5380.complex_midpoint(root) - 1.1
        )
        <= 1.0e-14,
        "nonzero_box_has_positive_modulus_lower": modulus_lower(
            iv.mpc(iv.mpf([2, 3]), iv.mpf([-1, 1]))
        )
        >= 2,
    }
    return {"checks": checks, "all_pass": all(checks.values())}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--output", type=Path, default=OUTPUT)
    arguments = parser.parse_args()
    if arguments.self_test:
        result = self_test()
    elif arguments.dry_run:
        result = preflight()
    else:
        result = run(arguments.output)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result.get("all_pass", result.get("validation_passed", False)) else 1


if __name__ == "__main__":
    raise SystemExit(main())
