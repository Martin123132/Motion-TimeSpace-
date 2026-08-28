from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
from decimal import Decimal, localcontext
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
OUTPUT = FUNCTIONAL_RG / "5389"
DOCUMENT = POST / "5389-Y5-R2FR-D4-full-H-event-geometry-and-coordinate-Cauchy-bridge.md"
VALIDATION = RESIDUALS / "P8_Y5_BRR545_5389_VALIDATION.csv"

SCRIPT_5386 = SCRIPTS / "Y5_R2FR_5386_D4_nested_contour_integrand_enclosure.py"
BASE_BOXES = FUNCTIONAL_RG / "5380" / "D4_complexified_event_neighborhood_boxes.csv"
BASE_RESULT = FUNCTIONAL_RG / "5380" / "D4_complexified_event_neighborhood_result.json"
HALO_BOXES = FUNCTIONAL_RG / "5387" / "D4_Cauchy_endpoint_halo_boxes.csv"
HALO_RESULT = FUNCTIONAL_RG / "5387" / "D4_Cauchy_endpoint_halo_result.json"
EVENTS = FUNCTIONAL_RG / "5358" / "D4_zero_regulator_event_certificate.csv"

CHECKPOINT = 5389
MARKER = "MTS_5389_D4_FULL_H_EVENT_GEOMETRY_AND_COORDINATE_CAUCHY_BRIDGE"
REVISION = "D4-full-H-event-geometry-and-coordinate-Cauchy-bridge-v2-complete-event-branch"
EVENT_IDS = tuple(f"E{index:02d}" for index in range(1, 9))
CONTRACTION_COUNT = 6
CAUCHY_SAFETY_FACTOR = 0.25

CLAIM_BRIDGE = "valid_for_D4_full_H_event_geometry_and_coordinate_Cauchy_bridge"
OPEN_CLAIMS = (
    "valid_for_D4_full_H_event_enclosure",
    "valid_for_D4_numeric_H3_bound",
    "valid_for_D4_numeric_uniform_remainder_bound",
    "valid_for_D4_outer_regulator_zero_limit",
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


M5386 = load_module("mts_5386_for_5389", SCRIPT_5386)
M5385 = M5386.M5385
M5381 = M5385.M5381
M5380 = M5385.M5380
M5379 = M5380.M5379


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


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


def open_claims() -> dict[str, bool]:
    return {claim: False for claim in OPEN_CLAIMS}


def source_paths() -> tuple[Path, ...]:
    return tuple(
        dict.fromkeys(
            path.resolve()
            for path in (
                Path(__file__),
                SCRIPT_5386,
                BASE_BOXES,
                BASE_RESULT,
                HALO_BOXES,
                HALO_RESULT,
                EVENTS,
            )
        )
    )


def source_rows() -> list[dict[str, Any]]:
    return [
        {
            "path": str(path),
            "exists": path.is_file(),
            "sha256": digest(path) if path.is_file() else "MISSING",
            CLAIM_BRIDGE: False,
            **open_claims(),
        }
        for path in source_paths()
    ]


def epsilon_box(source: dict[str, str]) -> Any:
    return iv.mpc(
        iv.mpf([source["epsilon_real_lower"], source["epsilon_real_upper"]]),
        iv.mpf(
            [
                source["epsilon_imaginary_lower"],
                source["epsilon_imaginary_upper"],
            ]
        ),
    )


def q_value(epsilon: Any) -> Any:
    epsilon_squared = epsilon**2
    return (
        -(80 + epsilon_squared) / (64 + epsilon_squared)
        + 1j * (-2 * epsilon / (64 + epsilon_squared))
    )


def coordinate_index(configuration: dict[str, Any]) -> int:
    return 2 if configuration["event_type"] == "BRANCH_DEATH" else 3


def inward_float(value: Decimal) -> float:
    candidate = float(value)
    if Decimal.from_float(candidate) > value:
        candidate = math.nextafter(candidate, -math.inf)
    return candidate


def outward_float(value: Decimal) -> float:
    candidate = float(value)
    if Decimal.from_float(candidate) < value:
        candidate = math.nextafter(candidate, math.inf)
    return candidate


def downward_product(first: float, second: float) -> float:
    with localcontext() as context:
        context.prec = 90
        return inward_float(
            Decimal.from_float(first) * Decimal.from_float(second)
        )


def downward_quotient(numerator: float, denominator: float) -> float:
    if numerator <= 0 or denominator <= 0:
        return 0.0
    with localcontext() as context:
        context.prec = 90
        return inward_float(
            Decimal.from_float(numerator) / Decimal.from_float(denominator)
        )


def upward_quotient(numerator: float, denominator: float) -> float:
    if denominator <= 0:
        return math.inf
    with localcontext() as context:
        context.prec = 90
        return outward_float(
            Decimal.from_float(numerator) / Decimal.from_float(denominator)
        )


def rectangle_margin(outer: Any, inner: Any) -> float:
    endpoint_pairs = (
        (M5380.real_lower(inner), M5380.real_lower(outer)),
        (M5380.real_upper(outer), M5380.real_upper(inner)),
        (M5380.imaginary_lower(inner), M5380.imaginary_lower(outer)),
        (M5380.imaginary_upper(outer), M5380.imaginary_upper(inner)),
    )
    with localcontext() as context:
        context.prec = 90
        margins = [
            Decimal.from_float(first) - Decimal.from_float(second)
            for first, second in endpoint_pairs
        ]
        return inward_float(min(margins))


def rectangle_hull(first: Any, second: Any) -> Any:
    return M5380.complex_box(
        min(M5380.real_lower(first), M5380.real_lower(second)),
        max(M5380.real_upper(first), M5380.real_upper(second)),
        min(M5380.imaginary_lower(first), M5380.imaginary_lower(second)),
        max(M5380.imaginary_upper(first), M5380.imaginary_upper(second)),
    )


def material_derivative(
    configuration: dict[str, Any], epsilon: Any, state_boxes: list[Any]
) -> dict[str, Any]:
    recoil = state_boxes[0] + 1j * state_boxes[1]
    index = coordinate_index(configuration)
    absolute_coordinate = state_boxes[index]
    sign = int(configuration["sign"])
    soft_cosine = sign * absolute_coordinate
    decay_cosine = iv.mpc(str(configuration["decay_cosine"]))
    dual = M5379.Dual
    polynomial_recoil = M5379.material_polynomial_dual(
        configuration["surface_id"],
        dual(recoil, 1),
        dual(soft_cosine),
        decay_cosine,
        dual(q_value(epsilon)),
    ).derivative
    polynomial_coordinate = M5379.material_polynomial_dual(
        configuration["surface_id"],
        dual(recoil),
        dual(soft_cosine, sign),
        decay_cosine,
        dual(q_value(epsilon)),
    ).derivative
    recoil_coordinate_derivative = -polynomial_coordinate / polynomial_recoil
    _, system_jacobian = M5380.complexified_system(
        configuration, epsilon, state_boxes
    )
    jacobian_uu = system_jacobian[0][0]
    jacobian_uv = system_jacobian[0][1]
    jacobian_vu = system_jacobian[1][0]
    jacobian_vv = system_jacobian[1][1]
    equation_u_coordinate = system_jacobian[0][index]
    equation_v_coordinate = system_jacobian[1][index]
    component_determinant = (
        jacobian_uu * jacobian_vv - jacobian_uv * jacobian_vu
    )
    recoil_real_coordinate_derivative = (
        -equation_u_coordinate * jacobian_vv
        + jacobian_uv * equation_v_coordinate
    ) / component_determinant
    recoil_imaginary_coordinate_derivative = (
        equation_u_coordinate * jacobian_vu
        - jacobian_uu * equation_v_coordinate
    ) / component_determinant
    component_recoil_coordinate_derivative = (
        recoil_real_coordinate_derivative
        + 1j * recoil_imaginary_coordinate_derivative
    )
    return {
        "recoil": recoil,
        "absolute_coordinate": absolute_coordinate,
        "soft_cosine": soft_cosine,
        "polynomial_recoil_derivative": polynomial_recoil,
        "polynomial_coordinate_derivative": polynomial_coordinate,
        "single_complex_polynomial_recoil_coordinate_derivative": recoil_coordinate_derivative,
        "material_component_jacobian_determinant": component_determinant,
        "recoil_real_coordinate_derivative": recoil_real_coordinate_derivative,
        "recoil_imaginary_coordinate_derivative": recoil_imaginary_coordinate_derivative,
        "recoil_coordinate_derivative": component_recoil_coordinate_derivative,
    }


def support_boundary_derivative(
    configuration: dict[str, Any], state_boxes: list[Any]
) -> dict[str, Any]:
    if configuration["event_type"] == "BRANCH_DEATH":
        raise ValueError("branch death has a fixed hard-energy boundary")
    dual = M5381.IntervalDual
    sign = int(configuration["sign"])
    hard_recoil = state_boxes[2]
    absolute_coordinate = state_boxes[3]
    soft_cosine = sign * absolute_coordinate
    soft_sine = state_boxes[4]
    decay_cosine = iv.mpc(str(configuration["decay_cosine"]))
    decay_sine = iv.mpc(
        str(math.sqrt(1 - float(configuration["decay_cosine"]) ** 2))
    )
    target = iv.mpc("-0.3")

    def boundary(hard: Any, cosine: Any, sine: Any) -> Any:
        decay = dual(decay_cosine)
        target_value = dual(target)
        relative = cosine * decay_cosine - sine * decay_sine
        return (
            (cosine - target_value) * (1 + relative) * hard * hard
            + 2 * (decay - cosine * relative) * hard
            + (cosine + target_value) * (relative - 1)
        )

    cosine_path = dual(soft_cosine, sign)
    sine_path = dual(soft_sine, -soft_cosine * sign / soft_sine)
    boundary_coordinate = boundary(
        dual(hard_recoil), cosine_path, sine_path
    ).derivative
    boundary_recoil = boundary(
        dual(hard_recoil, 1), dual(soft_cosine), dual(soft_sine)
    ).derivative
    hard_recoil_coordinate_derivative = -boundary_coordinate / boundary_recoil
    return {
        "hard_recoil": hard_recoil,
        "boundary_recoil_derivative": boundary_recoil,
        "boundary_coordinate_derivative": boundary_coordinate,
        "hard_recoil_coordinate_derivative": hard_recoil_coordinate_derivative,
        "soft_sine_modulus_lower": M5381.modulus_lower(soft_sine),
    }


def gap_geometry(
    configuration: dict[str, Any], epsilon: Any, state_boxes: list[Any]
) -> dict[str, Any]:
    material = material_derivative(configuration, epsilon, state_boxes)
    recoil = material["recoil"]
    recoil_coordinate_derivative = material["recoil_coordinate_derivative"]
    sigma = (
        int(configuration["inside_coordinate_direction_sign"])
        if configuration["event_type"] == "BRANCH_DEATH"
        else 1
    )
    if configuration["event_type"] == "BRANCH_DEATH":
        gap_coordinate_derivative = 2 * recoil * recoil_coordinate_derivative
        hard_derivative_lower = math.inf
        soft_sine_lower = M5381.modulus_lower(
            M5381.positive_complex_sqrt(1 - material["soft_cosine"] ** 2)
        )
    else:
        hard = support_boundary_derivative(configuration, state_boxes)
        gap_coordinate_derivative = (
            2 * recoil * recoil_coordinate_derivative
            - 2
            * hard["hard_recoil"]
            * hard["hard_recoil_coordinate_derivative"]
        )
        hard_derivative_lower = math.nextafter(
            M5381.modulus_lower(hard["boundary_recoil_derivative"]),
            0.0,
        )
        soft_sine_lower = hard["soft_sine_modulus_lower"]
    z1 = sigma * gap_coordinate_derivative
    z0 = 2j * state_boxes[0] * state_boxes[1]
    z1_lower = math.nextafter(M5381.modulus_lower(z1), 0.0)
    z0_upper = math.nextafter(M5381.modulus_upper(z0), math.inf)
    return {
        **material,
        "z0": z0,
        "z1": z1,
        "z0_modulus_upper": z0_upper,
        "z1_modulus_lower": z1_lower,
        "z1_modulus_upper": math.nextafter(
            M5381.modulus_upper(z1), math.inf
        ),
        "ratio_modulus_upper": (
            upward_quotient(z0_upper, z1_lower)
            if z1_lower > 0
            else math.inf
        ),
        "material_polynomial_recoil_derivative_modulus_lower": math.nextafter(
            M5381.modulus_lower(material["polynomial_recoil_derivative"]),
            0.0,
        ),
        "material_component_jacobian_determinant_modulus_lower": math.nextafter(
            M5381.modulus_lower(
                material["material_component_jacobian_determinant"]
            ),
            0.0,
        ),
        "hard_boundary_recoil_derivative_modulus_lower": hard_derivative_lower,
        "soft_sine_modulus_lower": math.nextafter(soft_sine_lower, 0.0),
    }


def contracted_boxes(
    configuration: dict[str, Any], source: dict[str, str], zero_coordinate: Any
) -> dict[str, Any]:
    epsilon_lower = float(source["epsilon_real_lower"])
    epsilon_upper = float(source["epsilon_real_upper"])
    center = M5380.point_solution(
        configuration,
        0.5 * (epsilon_lower + epsilon_upper),
        zero_coordinate,
    )
    source_boxes = [
        M5381.parse_complex_box(text)
        for text in source["complex_Krawczyk_images"].split("|")
    ]
    state_sequence = [source_boxes]
    contractions: list[dict[str, Any]] = []
    for _ in range(CONTRACTION_COUNT):
        certificate = M5380.krawczyk_certificate(
            configuration,
            (epsilon_lower, epsilon_upper),
            state_sequence[-1],
            center,
        )
        contractions.append(certificate)
        if not certificate["passes"]:
            break
        state_sequence.append(certificate["operator"])
    successful_contractions = len(state_sequence) - 1
    if successful_contractions < 1:
        raise RuntimeError(
            f"{configuration['event_id']} has no successful reserve contraction"
        )
    outer = state_sequence[0]
    inner = state_sequence[1]
    reserve_certificate = contractions[0]
    return {
        "outer": outer,
        "inner": inner,
        "reserve_certificate": reserve_certificate,
        "successful_contraction_count": successful_contractions,
        "reserved_outer_contraction_count": 0,
        "production_5386_contraction_count": successful_contractions,
        "next_contraction_passes": (
            contractions[successful_contractions]["passes"]
            if successful_contractions < len(contractions)
            else None
        ),
        "minimum_successful_contraction_margin": min(
            row["minimum_inclusion_margin"]
            for row in contractions[:successful_contractions]
        ),
        "maximum_successful_contraction_bound": max(
            row["contraction_bound"]
            for row in contractions[:successful_contractions]
        ),
    }


def bridge_row(
    source: dict[str, str],
    configuration: dict[str, Any],
    zero_coordinate: Any,
) -> dict[str, Any]:
    epsilon = epsilon_box(source)
    contraction = contracted_boxes(configuration, source, zero_coordinate)
    outer = contraction["outer"]
    inner = contraction["inner"]
    index = coordinate_index(configuration)
    outer_recoil = outer[0] + 1j * outer[1]
    inner_recoil = inner[0] + 1j * inner[1]
    coordinate_margin = rectangle_margin(outer[index], inner[index])
    recoil_margin = rectangle_margin(outer_recoil, inner_recoil)
    recoil_real_margin = rectangle_margin(outer[0], inner[0])
    recoil_imaginary_margin = rectangle_margin(outer[1], inner[1])
    outer_material = material_derivative(configuration, epsilon, outer)
    outer_material_derivative_lower = math.nextafter(
        M5381.modulus_lower(
            outer_material["polynomial_recoil_derivative"]
        ),
        0.0,
    )
    recoil_slope_upper = math.nextafter(
        M5381.modulus_upper(outer_material["recoil_coordinate_derivative"]),
        math.inf,
    )
    recoil_limited_radius = downward_quotient(recoil_margin, recoil_slope_upper)
    material_component_determinant_lower = math.nextafter(
        M5381.modulus_lower(
            outer_material["material_component_jacobian_determinant"]
        ),
        0.0,
    )
    recoil_real_slope_upper = math.nextafter(
        M5381.modulus_upper(
            outer_material["recoil_real_coordinate_derivative"]
        ),
        math.inf,
    )
    recoil_imaginary_slope_upper = math.nextafter(
        M5381.modulus_upper(
            outer_material["recoil_imaginary_coordinate_derivative"]
        ),
        math.inf,
    )
    recoil_real_limited_radius = downward_quotient(
        recoil_real_margin, recoil_real_slope_upper
    )
    recoil_imaginary_limited_radius = downward_quotient(
        recoil_imaginary_margin, recoil_imaginary_slope_upper
    )
    hard_recoil_margin = math.inf
    hard_recoil_slope_upper = 0.0
    hard_recoil_limited_radius = math.inf
    soft_sine_margin = math.inf
    soft_sine_slope_upper = 0.0
    soft_sine_limited_radius = math.inf
    outer_hard_derivative_lower = math.inf
    support_component_passes = True
    if configuration["event_type"] == "BRANCH_DEATH":
        outer_soft_sine_lower = math.nextafter(
            M5381.modulus_lower(
                M5381.positive_complex_sqrt(
                    1 - outer_material["soft_cosine"] ** 2
                )
            ),
            0.0,
        )
    else:
        hard_recoil_margin = rectangle_margin(outer[2], inner[2])
        soft_sine_margin = rectangle_margin(outer[4], inner[4])
        outer_support = support_boundary_derivative(configuration, outer)
        outer_hard_derivative_lower = math.nextafter(
            M5381.modulus_lower(
                outer_support["boundary_recoil_derivative"]
            ),
            0.0,
        )
        hard_recoil_slope_upper = math.nextafter(
            M5381.modulus_upper(
                outer_support["hard_recoil_coordinate_derivative"]
            ),
            math.inf,
        )
        outer_soft_sine_lower = math.nextafter(
            outer_support["soft_sine_modulus_lower"], 0.0
        )
        soft_sine_slope_upper = math.nextafter(
            M5381.modulus_upper(
                -outer_material["soft_cosine"]
                * int(configuration["sign"])
                / outer[4]
            ),
            math.inf,
        )
        hard_recoil_limited_radius = downward_quotient(
            hard_recoil_margin, hard_recoil_slope_upper
        )
        soft_sine_limited_radius = downward_quotient(
            soft_sine_margin, soft_sine_slope_upper
        )
        support_component_passes = (
            hard_recoil_margin > 0
            and soft_sine_margin > 0
            and outer_hard_derivative_lower > 0
            and outer_soft_sine_lower > 0
            and math.isfinite(hard_recoil_slope_upper)
            and math.isfinite(soft_sine_slope_upper)
            and hard_recoil_limited_radius > 0
            and soft_sine_limited_radius > 0
        )
    raw_radius = min(
        coordinate_margin,
        recoil_real_limited_radius,
        recoil_imaginary_limited_radius,
        hard_recoil_limited_radius,
        soft_sine_limited_radius,
    )
    coordinate_cauchy_radius = downward_product(
        CAUCHY_SAFETY_FACTOR, raw_radius
    )
    geometry = gap_geometry(configuration, epsilon, inner)
    bridge_passes = (
        contraction["successful_contraction_count"] >= 1
        and contraction["reserve_certificate"]["passes"]
        and coordinate_margin > 0
        and recoil_real_margin > 0
        and recoil_imaginary_margin > 0
        and outer_material_derivative_lower > 0
        and material_component_determinant_lower > 0
        and recoil_slope_upper < math.inf
        and math.isfinite(recoil_real_slope_upper)
        and math.isfinite(recoil_imaginary_slope_upper)
        and recoil_real_limited_radius > 0
        and recoil_imaginary_limited_radius > 0
        and outer_soft_sine_lower > 0
        and support_component_passes
        and coordinate_cauchy_radius > 0
        and geometry["material_polynomial_recoil_derivative_modulus_lower"] > 0
        and geometry[
            "material_component_jacobian_determinant_modulus_lower"
        ]
        > 0
        and geometry["z1_modulus_lower"] > 0
        and geometry["soft_sine_modulus_lower"] > 0
        and (
            configuration["event_type"] == "BRANCH_DEATH"
            or geometry["hard_boundary_recoil_derivative_modulus_lower"] > 0
        )
        and math.isfinite(geometry["ratio_modulus_upper"])
    )
    return {
        "event_id": configuration["event_id"],
        "event_type": configuration["event_type"],
        "epsilon_bin_index": int(source["epsilon_bin_index"]),
        "epsilon_real_lower": source["epsilon_real_lower"],
        "epsilon_real_upper": source["epsilon_real_upper"],
        "epsilon_imaginary_lower": source["epsilon_imaginary_lower"],
        "epsilon_imaginary_upper": source["epsilon_imaginary_upper"],
        "box_origin": (
            "endpoint_Cauchy_halo"
            if int(source["epsilon_bin_index"]) < 0
            or int(source["epsilon_bin_index"]) >= M5380.EPSILON_BIN_COUNT
            else "base_complex_event_strip"
        ),
        "production_5386_contraction_count": contraction[
            "production_5386_contraction_count"
        ],
        "reserved_outer_contraction_count": contraction[
            "reserved_outer_contraction_count"
        ],
        "reserved_strict_inner_contraction_pass": contraction[
            "reserve_certificate"
        ]["passes"],
        "next_production_contraction_passes": contraction[
            "next_contraction_passes"
        ],
        "minimum_successful_contraction_margin": contraction[
            "minimum_successful_contraction_margin"
        ],
        "reserved_strict_inner_contraction_margin": contraction[
            "reserve_certificate"
        ][
            "minimum_inclusion_margin"
        ],
        "maximum_successful_contraction_bound": contraction[
            "maximum_successful_contraction_bound"
        ],
        "reserved_strict_inner_contraction_bound": contraction[
            "reserve_certificate"
        ][
            "contraction_bound"
        ],
        "inner_to_outer_coordinate_margin_lower": coordinate_margin,
        "inner_to_outer_material_recoil_margin_lower": recoil_margin,
        "inner_to_outer_recoil_real_component_margin_lower": recoil_real_margin,
        "inner_to_outer_recoil_imaginary_component_margin_lower": recoil_imaginary_margin,
        "material_polynomial_recoil_derivative_modulus_lower_on_reserved_outer_box": outer_material_derivative_lower,
        "material_component_jacobian_determinant_modulus_lower_on_reserved_outer_box": material_component_determinant_lower,
        "material_recoil_coordinate_derivative_abs_upper_on_outer_box": recoil_slope_upper,
        "recoil_limited_coordinate_radius_lower": recoil_limited_radius,
        "recoil_real_component_coordinate_derivative_abs_upper_on_outer_box": recoil_real_slope_upper,
        "recoil_imaginary_component_coordinate_derivative_abs_upper_on_outer_box": recoil_imaginary_slope_upper,
        "recoil_real_component_limited_coordinate_radius_lower": recoil_real_limited_radius,
        "recoil_imaginary_component_limited_coordinate_radius_lower": recoil_imaginary_limited_radius,
        "inner_to_outer_hard_recoil_margin_lower": hard_recoil_margin,
        "hard_boundary_recoil_derivative_modulus_lower_on_reserved_outer_box": outer_hard_derivative_lower,
        "hard_recoil_coordinate_derivative_abs_upper_on_outer_box": hard_recoil_slope_upper,
        "hard_recoil_limited_coordinate_radius_lower": hard_recoil_limited_radius,
        "inner_to_outer_soft_sine_margin_lower": soft_sine_margin,
        "soft_sine_modulus_lower_on_reserved_outer_box": outer_soft_sine_lower,
        "soft_sine_coordinate_derivative_abs_upper_on_outer_box": soft_sine_slope_upper,
        "soft_sine_limited_coordinate_radius_lower": soft_sine_limited_radius,
        "coordinate_Cauchy_safety_factor": CAUCHY_SAFETY_FACTOR,
        "coordinate_Cauchy_radius_lower": coordinate_cauchy_radius,
        "material_polynomial_recoil_derivative_modulus_lower": geometry[
            "material_polynomial_recoil_derivative_modulus_lower"
        ],
        "material_component_jacobian_determinant_modulus_lower": geometry[
            "material_component_jacobian_determinant_modulus_lower"
        ],
        "hard_boundary_recoil_derivative_modulus_lower": geometry[
            "hard_boundary_recoil_derivative_modulus_lower"
        ],
        "soft_sine_modulus_lower": geometry["soft_sine_modulus_lower"],
        "boundary_gap_z0_modulus_upper": geometry["z0_modulus_upper"],
        "boundary_gap_derivative_z1_modulus_lower": geometry[
            "z1_modulus_lower"
        ],
        "boundary_gap_derivative_z1_modulus_upper": geometry[
            "z1_modulus_upper"
        ],
        "ratio_z0_over_z1_modulus_upper": geometry["ratio_modulus_upper"],
        "coordinate_disk_and_material_root_remain_in_reserved_outer_box": bridge_passes,
        "coordinate_disk_and_complete_event_branch_remain_in_reserved_outer_box": bridge_passes,
        CLAIM_BRIDGE: False,
        **open_claims(),
    }


def seam_row(
    left_source: dict[str, str],
    right_source: dict[str, str],
    configuration: dict[str, Any],
    zero_coordinate: Any,
) -> dict[str, Any]:
    overlap_lower = max(
        float(left_source["epsilon_real_lower"]),
        float(right_source["epsilon_real_lower"]),
    )
    overlap_upper = min(
        float(left_source["epsilon_real_upper"]),
        float(right_source["epsilon_real_upper"]),
    )
    if overlap_lower > overlap_upper:
        raise RuntimeError(
            f"nonoverlapping adjacent epsilon boxes for {configuration['event_id']}: "
            f"{left_source['epsilon_bin_index']}->{right_source['epsilon_bin_index']}"
        )
    left_contraction = contracted_boxes(
        configuration, left_source, zero_coordinate
    )
    right_contraction = contracted_boxes(
        configuration, right_source, zero_coordinate
    )
    seam_hull = [
        rectangle_hull(left_value, right_value)
        for left_value, right_value in zip(
            left_contraction["inner"],
            right_contraction["inner"],
            strict=True,
        )
    ]
    center = M5380.point_solution(
        configuration,
        0.5 * (overlap_lower + overlap_upper),
        zero_coordinate,
    )
    certificate = M5380.krawczyk_certificate(
        configuration,
        (overlap_lower, overlap_upper),
        seam_hull,
        center,
    )
    inflation_steps = 0
    while (
        not certificate["passes"]
        and certificate["contraction_bound"] < 1
        and inflation_steps < M5380.STATE_BOX_INFLATION_MAXIMUM_STEPS
    ):
        seam_hull = M5380.inflate_state_box(
            seam_hull, certificate["operator"]
        )
        inflation_steps += 1
        certificate = M5380.krawczyk_certificate(
            configuration,
            (overlap_lower, overlap_upper),
            seam_hull,
            center,
        )
    return {
        "event_id": configuration["event_id"],
        "event_type": configuration["event_type"],
        "left_epsilon_bin_index": int(left_source["epsilon_bin_index"]),
        "right_epsilon_bin_index": int(right_source["epsilon_bin_index"]),
        "epsilon_overlap_real_lower": overlap_lower,
        "epsilon_overlap_real_upper": overlap_upper,
        "epsilon_overlap_has_positive_width": overlap_upper > overlap_lower,
        "seam_hull_dimension": len(seam_hull),
        "seam_hull_inflation_steps": inflation_steps,
        "seam_Krawczyk_contraction_bound": certificate["contraction_bound"],
        "seam_Krawczyk_minimum_inclusion_margin": certificate[
            "minimum_inclusion_margin"
        ],
        "seam_Krawczyk_passes": certificate["passes"],
        "seam_branch_identity_statement": (
            "the left and right unique branch roots lie in one seam hull; "
            "the strict seam Krawczyk image proves that hull has one root"
        ),
        CLAIM_BRIDGE: False,
        **open_claims(),
    }


def render_document(result: dict[str, Any]) -> None:
    lines = [
        "# 5389 — D4 full-H event geometry and coordinate-Cauchy bridge",
        "",
        "## Decision",
        "",
        f"`{result['decision']}`",
        "",
        "## Derived bridge",
        "",
        "The production 5386 sweep contracts each already-certified 5380 image as far as strict inclusion permits. For the full-H proof, its first additional contraction is deliberately held in reserve: `C0` is evaluated on the uncontracted 5386 source box, while the first strict image contains the complete event branch. The componentwise gap between those two boxes is therefore usable rather than decorative.",
        "",
        "The regulator proof uses the holomorphic two-component material system `(P_u,P_v)=0`, not an illicit real/imaginary conjugacy assumption. Its `2x2` Jacobian in `(u,v)` is inverted interval-wise to enclose `u_x` and `v_x`; the older shorthand `R_x=-P_x/P_R` is retained only as a cross-check. At support contacts the other dependent coordinates obey `S_x=-sigma x/S` and `H_x=-B_x/B_H`. Each coordinate radius is chosen below the inner-to-outer coordinate margin and below every dependent-component margin divided by its derivative supremum. A first-exit argument then keeps the complete analytic event branch `(u,v,H,S)` inside the exact outer box already used by checkpoint 5386; branch-death rows require only `(u,v)`, with the nonvanishing square-root branch checked separately.",
        "",
        "On the event branch, the algebraic contact equation removes the correlated real part of the boundary gap exactly, giving `z0=2 i u v` for `R=u+i v`. The boundary-gap derivative is",
        "",
        "- branch death: `z1=sigma 2 R R_x`;",
        "- support contact: `z1=2 R R_x-2 H H_x`, with `H_x=-B_x/B_H`.",
        "",
        f"All `{result['row_count']}` base/endpoint-halo boxes exclude `P_R=0`, `z1=0`, the soft-sine zero, and (where present) `B_H=0` on the reserved outer boxes. The minimum certified complete-branch coordinate-Cauchy radius is `{result['minimum_coordinate_Cauchy_radius_lower']}` and the maximum `|z0/z1|` bound is `{result['maximum_ratio_z0_over_z1_modulus_upper']}`.",
        "",
        f"The `{result['seam_row_count']}` adjacent-bin seams are separately patched: the two strict branch images are enclosed in one hull and a new strict Krawczyk certificate proves that hull contains one root. This identifies the left and right local branches, including the finite-width endpoint-halo overlaps, so the regulator strip is one analytic branch rather than an unproved union of boxes. The minimum seam inclusion margin is `{result['minimum_seam_Krawczyk_inclusion_margin']}`.",
        "",
        "## Consequence",
        "",
        "Once a reserved-outer 5386 arc sweep is grouped into a physical `C0` bound `M0` for each box, the same outer enclosure and the radius `rho_x` give `|C1| <= M0/rho_x`. The full affine endpoint coefficient is then bounded without a fitted derivative by `|H| <= M0 |z0/z1| + (M0/(2 rho_x)) |z0/z1|^2`.",
        "",
        "This checkpoint certifies that bridge only. It does not claim the full-H or H3 bound until the completed 5386 rows are consumed, and it does not claim the total uniform remainder, D4 outer limit, local GR, or full MTS.",
        "",
    ]
    temporary = DOCUMENT.with_suffix(DOCUMENT.suffix + ".tmp")
    temporary.write_text("\n".join(lines), encoding="utf-8")
    os.replace(temporary, DOCUMENT)


def run(output: Path) -> dict[str, Any]:
    started = time.perf_counter()
    iv.dps = M5386.INTERVAL_DIGITS
    required = source_paths()
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise FileNotFoundError(missing)
    base_result = read_json(BASE_RESULT)
    halo_result = read_json(HALO_RESULT)
    base_boxes = read_csv(BASE_BOXES)
    halo_boxes = read_csv(HALO_BOXES)
    all_boxes = [*base_boxes, *halo_boxes]
    events = {row["event_id"]: row for row in read_csv(EVENTS)}
    references, _ = M5379.M5378.M5359.reference_rows()
    rows: list[dict[str, Any]] = []
    for source in all_boxes:
        event = events[source["event_id"]]
        configuration = M5379.M5378.M5359.event_configuration(event, references)
        zero_coordinate = M5380.mp.mpf(
            event["zero_regulator_absolute_soft_cosine"]
        )
        rows.append(bridge_row(source, configuration, zero_coordinate))
    seam_rows: list[dict[str, Any]] = []
    for event_id in EVENT_IDS:
        event = events[event_id]
        configuration = M5379.M5378.M5359.event_configuration(
            event, references
        )
        zero_coordinate = M5380.mp.mpf(
            event["zero_regulator_absolute_soft_cosine"]
        )
        event_sources = sorted(
            (row for row in all_boxes if row["event_id"] == event_id),
            key=lambda row: int(row["epsilon_bin_index"]),
        )
        for left_source, right_source in zip(
            event_sources, event_sources[1:]
        ):
            seam_rows.append(
                seam_row(
                    left_source,
                    right_source,
                    configuration,
                    zero_coordinate,
                )
            )
    keys = [(row["event_id"], row["epsilon_bin_index"]) for row in rows]
    all_bridge_rows_pass = all(
        parse_bool(
            row[
                "coordinate_disk_and_complete_event_branch_remain_in_reserved_outer_box"
            ]
        )
        for row in rows
    )
    minimum_radius = min(float(row["coordinate_Cauchy_radius_lower"]) for row in rows)
    maximum_ratio = max(
        float(row["ratio_z0_over_z1_modulus_upper"]) for row in rows
    )
    minimum_z1 = min(
        float(row["boundary_gap_derivative_z1_modulus_lower"]) for row in rows
    )
    minimum_material_derivative = min(
        float(
            row[
                "material_polynomial_recoil_derivative_modulus_lower_on_reserved_outer_box"
            ]
        )
        for row in rows
    )
    minimum_material_component_determinant = min(
        float(
            row[
                "material_component_jacobian_determinant_modulus_lower_on_reserved_outer_box"
            ]
        )
        for row in rows
    )
    support_hard_derivatives = [
        float(
            row[
                "hard_boundary_recoil_derivative_modulus_lower_on_reserved_outer_box"
            ]
        )
        for row in rows
        if row["event_type"] != "BRANCH_DEATH"
    ]
    support_rows = [
        row for row in rows if row["event_type"] != "BRANCH_DEATH"
    ]
    minimum_support_hard_radius = min(
        float(row["hard_recoil_limited_coordinate_radius_lower"])
        for row in support_rows
    )
    minimum_support_sine_radius = min(
        float(row["soft_sine_limited_coordinate_radius_lower"])
        for row in support_rows
    )
    minimum_outer_soft_sine = min(
        float(row["soft_sine_modulus_lower_on_reserved_outer_box"])
        for row in rows
    )
    seam_pass_count = sum(
        parse_bool(row["seam_Krawczyk_passes"]) for row in seam_rows
    )
    minimum_seam_margin = min(
        float(row["seam_Krawczyk_minimum_inclusion_margin"])
        for row in seam_rows
    )
    maximum_seam_contraction = max(
        float(row["seam_Krawczyk_contraction_bound"])
        for row in seam_rows
    )
    validations = [
        validation_row("all_direct_sources_exist", not missing, len(required)),
        validation_row(
            "parent_complex_strip_and_endpoint_halo_pass",
            base_result.get("validation_passed") is True
            and halo_result.get("validation_passed") is True,
            f"base={base_result.get('validation_passed')};halo={halo_result.get('validation_passed')}",
        ),
        validation_row(
            "matrix_contains_64_base_and_16_halo_boxes",
            len(base_boxes) == 64 and len(halo_boxes) == 16 and len(rows) == 80,
            f"base={len(base_boxes)};halo={len(halo_boxes)};total={len(rows)}",
        ),
        validation_row(
            "all_event_box_keys_are_unique",
            len(keys) == len(set(keys)),
            len(keys),
        ),
        validation_row(
            "all_eight_events_are_present",
            {row["event_id"] for row in rows} == set(EVENT_IDS),
            sorted({row["event_id"] for row in rows}),
        ),
        validation_row(
            "all_72_adjacent_bin_seams_have_unique_branch_patching_certificates",
            len(seam_rows) == len(EVENT_IDS) * 9
            and seam_pass_count == len(seam_rows)
            and minimum_seam_margin > 0
            and maximum_seam_contraction < 1,
            f"rows={len(seam_rows)};passes={seam_pass_count};"
            f"minimum_margin={minimum_seam_margin};"
            f"maximum_contraction={maximum_seam_contraction}",
        ),
        validation_row(
            "every_box_has_a_successful_contraction_held_in_reserve",
            all(
                int(row["production_5386_contraction_count"]) >= 1
                and parse_bool(row["reserved_strict_inner_contraction_pass"])
                for row in rows
            ),
            len(rows),
        ),
        validation_row(
            "material_implicit_derivative_denominators_exclude_zero",
            minimum_material_derivative > 0
            and minimum_material_component_determinant > 0,
            f"single_complex_P_R={minimum_material_derivative};"
            f"complexified_component_determinant={minimum_material_component_determinant}",
        ),
        validation_row(
            "support_boundary_implicit_derivative_denominators_exclude_zero",
            min(support_hard_derivatives) > 0,
            min(support_hard_derivatives),
        ),
        validation_row(
            "soft_sine_branches_exclude_zero_on_reserved_outer_boxes",
            minimum_outer_soft_sine > 0,
            minimum_outer_soft_sine,
        ),
        validation_row(
            "support_hard_recoil_and_soft_sine_path_radii_are_positive_finite",
            minimum_support_hard_radius > 0
            and minimum_support_sine_radius > 0
            and all(
                math.isfinite(
                    float(row["hard_recoil_limited_coordinate_radius_lower"])
                )
                and math.isfinite(
                    float(row["soft_sine_limited_coordinate_radius_lower"])
                )
                for row in support_rows
            ),
            f"hard={minimum_support_hard_radius};sine={minimum_support_sine_radius}",
        ),
        validation_row(
            "all_boundary_gap_derivatives_exclude_zero",
            minimum_z1 > 0,
            minimum_z1,
        ),
        validation_row(
            "all_coordinate_Cauchy_radii_are_positive_finite",
            minimum_radius > 0
            and all(
                math.isfinite(float(row["coordinate_Cauchy_radius_lower"]))
                for row in rows
            ),
            minimum_radius,
        ),
        validation_row(
            "all_coordinate_disks_and_complete_event_branches_remain_inside_reserved_outer_boxes",
            all_bridge_rows_pass,
            len(rows),
        ),
        validation_row(
            "all_ratio_bounds_are_finite",
            math.isfinite(maximum_ratio),
            maximum_ratio,
        ),
        validation_row(
            "formalization_workbench_remains_unchanged",
            M5379.M5378.M5359.M5342.M5283.formal_inventory_digest()
            == M5379.M5378.M5359.M5342.FORMAL_DIGEST,
            M5379.M5378.M5359.M5342.M5283.formal_inventory_digest(),
        ),
    ]
    passed = all(parse_bool(row["passed"]) for row in validations)
    for row in rows:
        row[CLAIM_BRIDGE] = passed
    for row in seam_rows:
        row[CLAIM_BRIDGE] = passed
    registered_sources = source_rows()
    for row in registered_sources:
        row[CLAIM_BRIDGE] = passed
    result = {
        "checkpoint": CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "validation_passed": passed,
        "decision": (
            "FULL_H_EVENT_GEOMETRY_AND_COORDINATE_CAUCHY_BRIDGE_CERTIFIED__RUN_RESERVED_OUTER_C0_SWEEP"
            if passed
            else "FULL_H_EVENT_GEOMETRY_AND_COORDINATE_CAUCHY_BRIDGE_BLOCKED"
        ),
        "row_count": len(rows),
        "seam_row_count": len(seam_rows),
        "minimum_seam_Krawczyk_inclusion_margin": minimum_seam_margin,
        "maximum_seam_Krawczyk_contraction_bound": maximum_seam_contraction,
        "minimum_coordinate_Cauchy_radius_lower": minimum_radius,
        "maximum_ratio_z0_over_z1_modulus_upper": maximum_ratio,
        "minimum_boundary_gap_derivative_z1_modulus_lower": minimum_z1,
        "minimum_material_polynomial_recoil_derivative_modulus_lower": minimum_material_derivative,
        "minimum_material_component_jacobian_determinant_modulus_lower": minimum_material_component_determinant,
        "minimum_support_boundary_recoil_derivative_modulus_lower": min(
            support_hard_derivatives
        ),
        "minimum_support_hard_recoil_limited_coordinate_radius_lower": minimum_support_hard_radius,
        "minimum_support_soft_sine_limited_coordinate_radius_lower": minimum_support_sine_radius,
        "minimum_soft_sine_modulus_lower_on_reserved_outer_box": minimum_outer_soft_sine,
        "claim_boundary": {CLAIM_BRIDGE: passed, **open_claims()},
        "remaining_obstruction": "run checkpoint 5390's reserved-outer C0 contour matrix, combine those C0 bounds with the certified coordinate radii and z0/z1 bounds, then apply regulator-plane Cauchy to full H",
        "formalization_workbench_modified_file_count": 0,
        "runtime_seconds": time.perf_counter() - started,
        "updated_utc": utc_now(),
    }
    output = output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    atomic_csv(output / "D4_full_H_event_geometry_bridge.csv", rows)
    atomic_csv(output / "D4_full_H_event_branch_seams.csv", seam_rows)
    atomic_csv(output / "D4_full_H_event_geometry_bridge_validation.csv", validations)
    atomic_csv(output / "source_register.csv", registered_sources)
    atomic_csv(VALIDATION, validations)
    atomic_json(output / "D4_full_H_event_geometry_bridge_result.json", result)
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


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", type=Path, default=OUTPUT)
    arguments = parser.parse_args()
    result = run(arguments.output)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["validation_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
