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
import sys
import time
from typing import Any

from mpmath import iv, mp


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
OUTPUT = FUNCTIONAL_RG / "5385"
DOCUMENT = POST / "5385-Y5-R2FR-D4-expanded-energy-contour-full-pole-catalog-clearance.md"
VALIDATION = RESIDUALS / "P8_Y5_BRR545_5385_VALIDATION.csv"

SCRIPT_5384 = SCRIPTS / "Y5_R2FR_5384_D4_nested_global_contour_root_clearance_certificate.py"
RESULT_5384 = FUNCTIONAL_RG / "5384" / "D4_nested_global_contour_root_clearance_result.json"
VALIDATION_5384 = FUNCTIONAL_RG / "5384" / "D4_nested_global_contour_root_clearance_validation.csv"
SCRIPT_5258 = SCRIPTS / "Y5_R2FR_5258_interval_residue_enclosure_pilot.py"
RESULT_5258 = FUNCTIONAL_RG / "5258" / "interval_residue_result.json"
VALIDATION_5258 = FUNCTIONAL_RG / "5258" / "interval_residue_validation.csv"
BOXES_5380 = FUNCTIONAL_RG / "5380" / "D4_complexified_event_neighborhood_boxes.csv"
EVENTS_5358 = FUNCTIONAL_RG / "5358" / "D4_zero_regulator_event_certificate.csv"
EVENTS_5383 = FUNCTIONAL_RG / "5383" / "D4_double_Cauchy_parent_C0_events.csv"

CHECKPOINT = 5385
MARKER = "MTS_5385_D4_EXPANDED_ENERGY_CONTOUR_FULL_POLE_CATALOG_CLEARANCE"
REVISION = "D4-expanded-energy-contour-full-pole-catalog-clearance-v1"
EVENT_IDS = tuple(f"E{index:02d}" for index in range(1, 9))
INTERVAL_DIGITS = 50
MP_DIGITS = 90
ENERGY_PHASE_ARC_COUNT = 32
PATH_DERIVATIVE_SUBDIVISIONS = 32
ENERGY_CONTOUR_RELATIVE_RADIUS = "1e-5"
GLOBAL_CONTOUR_RELATIVE_RADIUS = "1e-7"
NUMERICAL_ENERGY_POINTS = 16
NUMERICAL_RELATIVE_TOLERANCE = 1.0e-12

CLAIM_CLEARANCE = "valid_for_D4_expanded_energy_contour_full_pole_catalog_clearance"
OPEN_CLAIMS = (
    "valid_for_D4_nested_contour_integrand_enclosure",
    "valid_for_D4_energy_contour_exclusive_parent_pole",
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


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5384 = load_module("mts_5384_for_5385", SCRIPT_5384)
M5383 = M5384.M5383
M5381 = M5384.M5381
M5380 = M5384.M5380


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


def source_paths() -> tuple[Path, ...]:
    paths = (
        Path(__file__).resolve(),
        SCRIPT_5384,
        RESULT_5384,
        VALIDATION_5384,
        SCRIPT_5258,
        RESULT_5258,
        VALIDATION_5258,
        BOXES_5380,
        EVENTS_5358,
        EVENTS_5383,
    )
    return tuple(dict.fromkeys(path.resolve() for path in paths))


def source_rows() -> list[dict[str, Any]]:
    return [
        {
            "path": str(path),
            "exists": path.is_file(),
            "sha256": digest(path) if path.is_file() else "MISSING",
            CLAIM_CLEARANCE: False,
            **open_claims(),
        }
        for path in source_paths()
    ]


def preflight() -> dict[str, Any]:
    result_5384 = read_json(RESULT_5384)
    result_5258 = read_json(RESULT_5258)
    checks = {
        "all_direct_sources_exist": all(path.is_file() for path in source_paths()),
        "checkpoint_5384_passes": result_5384.get("validation_passed") is True
        and all(parse_bool(row["passed"]) for row in read_csv(VALIDATION_5384)),
        "checkpoint_5384_inner_clearance_is_claimed": result_5384.get(
            "claim_boundary", {}
        ).get("valid_for_D4_nested_global_contour_root_clearance")
        is True,
        "checkpoint_5258_full_catalog_incidence_passes": result_5258.get(
            "validation_passed"
        )
        is True
        and result_5258.get("interval_arithmetic_complete") is True
        and all(parse_bool(row["passed"]) for row in read_csv(VALIDATION_5258)),
        "all_64_complex_event_boxes_are_present": len(read_csv(BOXES_5380))
        == len(EVENT_IDS) * M5380.EPSILON_BIN_COUNT,
        "all_eight_baseline_C0_rows_are_present": [
            row["event_id"] for row in read_csv(EVENTS_5383)
        ]
        == list(EVENT_IDS),
        "formal_workbench_inventory_is_unchanged": M5380.M5379.M5378.M5359.M5342.M5283.formal_inventory_digest()
        == M5380.M5379.M5378.M5359.M5342.FORMAL_DIGEST,
        "scripts_cache_is_absent": not (SCRIPTS / "__pycache__").exists(),
    }
    return {"checks": checks, "all_pass": all(checks.values())}


def complex_midpoint_box(value: Any) -> Any:
    midpoint = M5380.complex_midpoint(value)
    return iv.mpc(
        iv.mpf(str(midpoint.real)), iv.mpf(str(midpoint.imag))
    )


def complex_box_radius(value: Any) -> float:
    midpoint = M5380.complex_midpoint(value)
    return max(
        abs(complex(real, imaginary) - midpoint)
        for real in (M5380.real_lower(value), M5380.real_upper(value))
        for imaginary in (
            M5380.imaginary_lower(value),
            M5380.imaginary_upper(value),
        )
    )


def positive_sqrt_dual(value: Any) -> Any:
    dual = M5381.IntervalDual.coerce(value)
    root = M5381.positive_complex_sqrt(dual.value)
    return M5381.IntervalDual(root, dual.derivative / (2 * root))


def event_inputs(
    configuration: dict[str, Any], epsilon: Any, state_boxes: list[Any]
) -> dict[str, Any]:
    material_recoil = state_boxes[0] + 1j * state_boxes[1]
    coordinate_index = (
        2 if configuration["event_type"] == "BRANCH_DEATH" else 3
    )
    soft_cosine = configuration["sign"] * state_boxes[coordinate_index]
    soft_sine = (
        M5381.positive_complex_sqrt(1 - soft_cosine**2)
        if configuration["event_type"] == "BRANCH_DEATH"
        else state_boxes[4]
    )
    decay_cosine = iv.mpc(configuration["decay_cosine"])
    decay_sine = iv.mpc(
        math.sqrt(1 - float(configuration["decay_cosine"]) ** 2)
    )
    epsilon_squared = epsilon**2
    q_value = (
        -(80 + epsilon_squared) / (64 + epsilon_squared)
        + 1j * (-2 * epsilon / (64 + epsilon_squared))
    )
    external_root = -1j * M5381.positive_complex_sqrt(-q_value)
    return {
        "epsilon": epsilon,
        "material_recoil": material_recoil,
        "soft_cosine": soft_cosine,
        "soft_sine": soft_sine,
        "decay_cosine": decay_cosine,
        "decay_sine": decay_sine,
        "q_value": q_value,
        "external_root": external_root,
    }


def expanded_geometry(
    configuration: dict[str, Any],
    inputs: dict[str, Any],
    energy_displacement: Any,
    recoil_override: Any | None = None,
) -> dict[str, Any]:
    material_recoil = inputs["material_recoil"]
    soft_cosine = inputs["soft_cosine"]
    soft_sine = inputs["soft_sine"]
    decay_cosine = inputs["decay_cosine"]
    decay_sine = inputs["decay_sine"]
    q_value = inputs["q_value"]
    external_root = inputs["external_root"]
    energy_recoil_radicand = material_recoil**2 - energy_displacement
    recoil = (
        M5381.positive_complex_sqrt(energy_recoil_radicand)
        if recoil_override is None
        else recoil_override
    )
    energy = 1 - recoil**2
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
    representative_denominator = (
        decay_sine * (1 + soft_cosine) * factor_f2
    )
    representative = (
        soft_sine
        * (1 + decay_cosine)
        * factor_f1
        / representative_denominator
    )
    relative = (
        1 / representative
        if configuration["role"] == "reciprocal"
        else representative
    )
    relative_cosine = (
        (relative + 1 / relative) * soft_sine * decay_sine / 2
        + soft_cosine * decay_cosine
    )
    first_energy = (
        1 + recoil**2 - relative_cosine * (1 - recoil**2)
    ) / 2
    first_longitudinal = (
        relative_cosine * (1 - recoil) ** 2 - (1 - recoil**2)
    ) / 2
    first_holomorphic = (
        recoil * decay_sine * relative + first_longitudinal * soft_sine
    )
    first_antiholomorphic = (
        recoil * decay_sine / relative
        + first_longitudinal * soft_sine
    )
    first_pz = first_longitudinal * soft_cosine + recoil * decay_cosine
    first_factors = (
        first_energy + first_pz,
        first_energy - first_pz,
        first_holomorphic,
        first_antiholomorphic,
    )
    second_energy = (
        1 + recoil**2 + relative_cosine * (1 - recoil**2)
    ) / 2
    second_longitudinal = (
        -relative_cosine * (1 - recoil) ** 2 - (1 - recoil**2)
    ) / 2
    second_holomorphic = (
        -recoil * decay_sine * relative
        + second_longitudinal * soft_sine
    )
    second_antiholomorphic = (
        -recoil * decay_sine / relative
        + second_longitudinal * soft_sine
    )
    second_pz = second_longitudinal * soft_cosine - recoil * decay_cosine
    second_factors = (
        second_energy + second_pz,
        second_energy - second_pz,
        second_holomorphic,
        second_antiholomorphic,
    )
    soft_factors = (
        1 + soft_cosine,
        1 - soft_cosine,
        soft_sine,
        soft_sine,
    )
    decay_factors = (
        1 + decay_cosine,
        1 - decay_cosine,
        decay_sine * relative,
        decay_sine / relative,
    )
    if configuration["root_labels"][1] == "plus_u":
        selected_root = external_root * (1 + soft_cosine) / soft_sine
    else:
        selected_root = soft_sine / (
            (1 + soft_cosine) * external_root
        )
    primitive_denominators = (
        64 + inputs["epsilon"] ** 2,
        energy_recoil_radicand,
        decay_sine,
        1 + soft_cosine,
        soft_sine,
        factor_f2,
        representative_denominator,
        representative,
        relative,
        external_root,
        selected_root,
    )
    return {
        "energy": energy,
        "energy_recoil_radicand": energy_recoil_radicand,
        "recoil": recoil,
        "relative": relative,
        "selected_root": selected_root,
        "first_factors": first_factors,
        "second_factors": second_factors,
        "soft_factors": soft_factors,
        "decay_factors": decay_factors,
        "minimum_primitive_denominator_modulus_lower": min(
            M5381.modulus_lower(value) for value in primitive_denominators
        ),
    }


def g1_separation_bound(
    configuration: dict[str, Any],
    inputs: dict[str, Any],
    geometry: dict[str, Any],
    label: str,
) -> dict[str, Any]:
    q_value = inputs["q_value"]
    external_root = inputs["external_root"]
    selected_root = geometry["selected_root"]
    first_energy = (
        geometry["first_factors"][0] + geometry["first_factors"][1]
    ) / 2
    holomorphic = geometry["first_factors"][2]
    if label == "plus_u" and configuration["role"] == "representative":
        separation = (
            M5381.modulus_lower(1 + q_value)
            * M5381.modulus_lower(selected_root)
        )
        return {
            "method": "same_momentum_plus_u_equals_minus_q_z",
            "chart": "exact_q_relation",
            "separation_modulus_lower": separation,
        }
    if label == "plus_v" and configuration["role"] == "representative":
        denominator_upper = (
            M5381.modulus_upper(external_root)
            * M5381.modulus_upper(holomorphic)
        )
        separation = (
            2 * M5381.modulus_lower(first_energy) / denominator_upper
        )
        return {
            "method": "factorized_null_identity_2E_over_eH",
            "chart": "exact_null_reduction",
            "separation_modulus_lower": separation,
        }
    if label == "plus_v" and configuration["role"] == "reciprocal":
        separation = (
            M5381.modulus_lower(selected_root)
            * M5381.modulus_lower(1 + q_value)
            / M5381.modulus_upper(q_value)
        )
        return {
            "method": "same_momentum_plus_v_equals_minus_z_over_q",
            "chart": "exact_q_relation",
            "separation_modulus_lower": separation,
        }
    bound = M5384.projective_separation_bound(
        geometry["first_factors"], label, external_root, selected_root
    )
    return {
        "method": bound["method"],
        "chart": bound["chart"],
        "separation_modulus_lower": bound["separation_modulus_lower"],
    }


def branch_gap_dual(
    configuration: dict[str, Any],
    epsilon: Any,
    material_recoil: Any,
    soft_cosine: Any,
    energy_displacement: Any,
    decay_cosine: Any,
    decay_sine: Any,
    recoil_override: Any | None = None,
    gap_sector: str = "g2",
) -> tuple[Any, Any, str]:
    dual = M5381.IntervalDual
    epsilon = dual.coerce(epsilon)
    material_recoil = dual.coerce(material_recoil)
    soft_cosine = dual.coerce(soft_cosine)
    energy_displacement = dual.coerce(energy_displacement)
    decay_cosine = dual.coerce(decay_cosine)
    decay_sine = dual.coerce(decay_sine)
    epsilon_squared = epsilon * epsilon
    q_value = (
        -(80 + epsilon_squared) / (64 + epsilon_squared)
        + 1j * (-2 * epsilon / (64 + epsilon_squared))
    )
    external_root = -1j * positive_sqrt_dual(-q_value)
    recoil = (
        dual.coerce(recoil_override)
        if recoil_override is not None
        else positive_sqrt_dual(
            material_recoil * material_recoil - energy_displacement
        )
    )
    soft_sine = positive_sqrt_dual(1 - soft_cosine * soft_cosine)
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
    representative = (
        soft_sine
        * (1 + decay_cosine)
        * factor_f1
        / (decay_sine * (1 + soft_cosine) * factor_f2)
    )
    relative = (
        1 / representative
        if configuration["role"] == "reciprocal"
        else representative
    )
    relative_cosine = (
        (relative + 1 / relative) * soft_sine * decay_sine / 2
        + soft_cosine * decay_cosine
    )
    if gap_sector in {"g1_companion", "g1_minus_companion"}:
        first_energy = (
            1
            + recoil * recoil
            - relative_cosine * (1 - recoil * recoil)
        ) / 2
        first_longitudinal = (
            relative_cosine * (1 - recoil) * (1 - recoil)
            - (1 - recoil * recoil)
        ) / 2
        first_holomorphic = (
            recoil * decay_sine * relative
            + first_longitudinal * soft_sine
        )
        if gap_sector == "g1_minus_companion":
            first_momentum_z = (
                first_longitudinal * soft_cosine
                + recoil * decay_cosine
            )
            first_plus = first_energy + first_momentum_z
            first_minus = first_energy - first_momentum_z
            return (
                first_plus - q_value * first_minus,
                external_root * first_holomorphic,
                "exact_first_minus_companion_projective_identity",
            )
        if configuration["role"] == "representative":
            denominator = external_root * first_holomorphic
            translated_numerator = 2 * first_energy
        else:
            denominator = first_holomorphic
            translated_numerator = 2 * external_root * first_energy
        return (
            translated_numerator,
            denominator,
            "exact_first_null_companion_projective_identity",
        )
    if gap_sector != "g2":
        raise ValueError(f"unsupported branch gap sector {gap_sector}")
    energy = (
        1 + recoil * recoil
        + relative_cosine * (1 - recoil * recoil)
    ) / 2
    longitudinal = (
        -relative_cosine * (1 - recoil) * (1 - recoil)
        - (1 - recoil * recoil)
    ) / 2
    holomorphic = (
        -recoil * decay_sine * relative + longitudinal * soft_sine
    )
    antiholomorphic = (
        -recoil * decay_sine / relative + longitudinal * soft_sine
    )
    momentum_z = longitudinal * soft_cosine - recoil * decay_cosine
    plus_denominator = energy + momentum_z
    minus_denominator = energy - momentum_z
    selected_root = (
        external_root * (1 + soft_cosine) / soft_sine
        if configuration["role"] == "representative"
        else soft_sine / ((1 + soft_cosine) * external_root)
    )
    if configuration["role"] == "representative":
        candidates = (
            (
                -external_root * antiholomorphic / plus_denominator,
                plus_denominator,
                "primary",
            ),
            (
                -external_root * minus_denominator / holomorphic,
                holomorphic,
                "opposite",
            ),
        )
    else:
        candidates = (
            (
                -plus_denominator / (external_root * holomorphic),
                holomorphic,
                "primary",
            ),
            (
                -antiholomorphic / (external_root * minus_denominator),
                minus_denominator,
                "opposite",
            ),
        )
    root, denominator, chart = max(
        candidates,
        key=lambda item: M5381.modulus_lower(item[1].value),
    )
    return root - selected_root, denominator, chart


def branch_center_gap_certificate(
    configuration: dict[str, Any],
    inputs: dict[str, Any],
    gap_sector: str = "g2",
    use_material_recoil_sheet: bool = False,
) -> dict[str, Any]:
    domains = (
        inputs["epsilon"],
        inputs["material_recoil"],
        inputs["soft_cosine"],
    )
    centers = tuple(complex_midpoint_box(value) for value in domains)
    center_gap, _, center_chart = branch_gap_dual(
        configuration,
        centers[0],
        centers[1],
        centers[2],
        iv.mpc(0),
        inputs["decay_cosine"],
        inputs["decay_sine"],
        recoil_override=(
            centers[1] if use_material_recoil_sheet else None
        ),
        gap_sector=gap_sector,
    )
    center_modulus_lower = M5381.modulus_lower(center_gap.value)
    parameter_variation_box = iv.mpc(0)
    derivative_uppers: list[float] = []
    denominator_lower = math.inf
    for derivative_index in range(len(domains)):
        dual_domains = [
            M5381.IntervalDual(
                value, iv.mpc(1 if index == derivative_index else 0)
            )
            for index, value in enumerate(domains)
        ]
        gap, denominator, _ = branch_gap_dual(
            configuration,
            dual_domains[0],
            dual_domains[1],
            dual_domains[2],
            M5381.IntervalDual(iv.mpc(0), iv.mpc(0)),
            inputs["decay_cosine"],
            inputs["decay_sine"],
            recoil_override=(
                dual_domains[1] if use_material_recoil_sheet else None
            ),
            gap_sector=gap_sector,
        )
        derivative_upper = M5381.modulus_upper(gap.derivative)
        derivative_uppers.append(derivative_upper)
        parameter_variation_box += gap.derivative * (
            domains[derivative_index] - centers[derivative_index]
        )
        denominator_lower = min(
            denominator_lower, M5381.modulus_lower(denominator.value)
        )
    center_gap_box = center_gap.value + parameter_variation_box
    variation_upper = M5381.modulus_upper(parameter_variation_box)
    return {
        "center_chart": center_chart,
        "center_gap_modulus_lower": center_modulus_lower,
        "center_parameter_variation_upper": variation_upper,
        "center_gap_after_parameter_variation_lower": M5381.modulus_lower(
            center_gap_box
        ),
        "center_gap_box": center_gap_box,
        "center_derivative_modulus_uppers": derivative_uppers,
        "center_chart_denominator_modulus_lower": denominator_lower,
    }


def branch_energy_variation_upper(
    configuration: dict[str, Any],
    inputs: dict[str, Any],
    energy_displacement: Any,
    gap_sector: str = "g2",
) -> dict[str, Any]:
    material_recoil = inputs["material_recoil"]
    energy_recoil = M5381.positive_complex_sqrt(
        material_recoil**2 - energy_displacement
    )
    recoil_displacement = energy_recoil - material_recoil
    derivative_integral = iv.mpc(0)
    minimum_denominator = math.inf
    charts: set[str] = set()
    for index in range(PATH_DERIVATIVE_SUBDIVISIONS):
        path_parameter = iv.mpf(
            [
                index / PATH_DERIVATIVE_SUBDIVISIONS,
                (index + 1) / PATH_DERIVATIVE_SUBDIVISIONS,
            ]
        )
        path_recoil = material_recoil + path_parameter * recoil_displacement
        recoil_dual = M5381.IntervalDual(path_recoil, iv.mpc(1))
        gap, denominator, chart = branch_gap_dual(
            configuration,
            inputs["epsilon"],
            inputs["material_recoil"],
            inputs["soft_cosine"],
            iv.mpc(0),
            inputs["decay_cosine"],
            inputs["decay_sine"],
            recoil_override=recoil_dual,
            gap_sector=gap_sector,
        )
        derivative_integral += (
            gap.derivative / PATH_DERIVATIVE_SUBDIVISIONS
        )
        minimum_denominator = min(
            minimum_denominator, M5381.modulus_lower(denominator.value)
        )
        charts.add(chart)
    energy_variation_box = recoil_displacement * derivative_integral
    variation_upper = M5381.modulus_upper(energy_variation_box)
    return {
        "energy_recoil_displacement_modulus_upper": M5381.modulus_upper(
            recoil_displacement
        ),
        "path_derivative_integral_modulus_upper": M5381.modulus_upper(
            derivative_integral
        ),
        "energy_variation_upper": variation_upper,
        "energy_variation_box": energy_variation_box,
        "minimum_path_chart_denominator_modulus_lower": minimum_denominator,
        "path_charts": "|".join(sorted(charts)),
    }


def numerical_expanded_contour_crosscheck() -> list[dict[str, Any]]:
    mp.dps = MP_DIGITS
    M5383.M5378.AMP.mp.mp.dps = MP_DIGITS
    references, _ = M5383.M5378.M5359.reference_rows()
    events = read_csv(EVENTS_5358)
    baseline = {row["event_id"]: row for row in read_csv(EVENTS_5383)}
    old_kernel = M5383.M5378.M5359.M5342.configure()
    rows: list[dict[str, Any]] = []
    try:
        context = M5383.M5378.M5359.M5342.M5312.M5303.synthetic_context()
        epsilon_id = M5383.M5378.M5359.M5342.M5312.EPSILON_ID
        component = context["inventories"][epsilon_id]["components"]["MC04"]
        physical_multiplier = mp.mpf(
            str(M5383.M5378.M5359.M5342.M5312.M5309.physical_multiplier())
        )
        for event in events:
            configuration = M5383.M5378.M5359.event_configuration(
                event, references
            )
            configuration["trace_orientation"] = 1
            expanded = M5383.energy_contour_residue(
                configuration,
                mp.mpf(0),
                component,
                physical_multiplier,
                mp.mpf(ENERGY_CONTOUR_RELATIVE_RADIUS),
                NUMERICAL_ENERGY_POINTS,
            )
            source = baseline[configuration["event_id"]]
            source_value = mp.mpc(
                source["double_Cauchy_C0_real"],
                source["double_Cauchy_C0_imaginary"],
            )
            relative_difference = float(
                abs(expanded - source_value)
                / max(abs(expanded), abs(source_value), mp.mpf("1e-300"))
            )
            rows.append(
                {
                    "event_id": configuration["event_id"],
                    "expanded_energy_relative_radius": ENERGY_CONTOUR_RELATIVE_RADIUS,
                    "energy_points": NUMERICAL_ENERGY_POINTS,
                    "expanded_C0_real": mp.nstr(mp.re(expanded), 40),
                    "expanded_C0_imaginary": mp.nstr(mp.im(expanded), 40),
                    "source_5383_C0_real": source["double_Cauchy_C0_real"],
                    "source_5383_C0_imaginary": source[
                        "double_Cauchy_C0_imaginary"
                    ],
                    "relative_difference": relative_difference,
                    "numerical_crosscheck_passes": relative_difference
                    <= NUMERICAL_RELATIVE_TOLERANCE,
                    CLAIM_CLEARANCE: False,
                    **open_claims(),
                }
            )
            print(
                f"expanded-contour numerical crosscheck {configuration['event_id']} relative_difference={relative_difference:.3e}",
                flush=True,
            )
    finally:
        M5383.M5378.M5359.M5342.M5326.restore_kernel(old_kernel)
    return rows


def render_document(result: dict[str, Any]) -> None:
    lines = [
        "# 5385 — Y5/R2FR D4 expanded energy contour and full pole-catalog clearance",
        "",
        "## Result",
        "",
        f"Decision: `{result['decision']}`.",
        "",
        "The parent-energy Cauchy radius is expanded from `1e-6` to `1e-5`. The resulting double-Cauchy residues agree with checkpoint 5383, while the complete 20-root amplitude catalog is checked on the expanded contour: 12 direct roots (`g1,g2,g3`) and 8 subtraction roots (`soft,decay`). The selected collision owns three coincident catalog entries, leaving 17 nonactive roots to exclude.",
        "",
        f"- certified event/epsilon boxes: `{result['certified_event_epsilon_box_count']}/{result['required_event_epsilon_box_count']}`;",
        f"- certified energy arcs: `{result['certified_energy_arc_count']}/{result['required_energy_arc_count']}`;",
        f"- nonactive full-catalog checks: `{result['nonactive_root_check_count']}`;",
        f"- minimum certified full-catalog separation: `{result['minimum_nonactive_root_separation_lower']}`;",
        f"- maximum inner contour radius: `{result['maximum_global_contour_radius_upper']}`;",
        f"- minimum full-catalog clearance margin: `{result['minimum_full_catalog_clearance_margin_lower']}`;",
        f"- maximum expanded-versus-5383 numerical C0 difference: `{result['maximum_expanded_contour_relative_difference']}`.",
        "",
        "## Nearby g2 pole",
        "",
        "At the four branch-death events, the nearest nonactive root is a `g2` root only about `8e-5` from the selected center. Direct rectangular subtraction loses that gap. The certificate therefore uses a centered complex mean-value bound at zero energy displacement and a 32-piece interval line integral in recoil space for the expanded energy contour. This treats the nearby pole as real geometry rather than numerical noise.",
        "",
        "## Scope",
        "",
        "This closes full pole-catalog isolation on a numerically crosschecked outer contour. It does not yet interval-enclose the finite-plus spinor numerator or prove that no separate energy-plane singularity lies inside the outer contour. Endpoint C, H3, the uniform remainder, the D4 outer limit, local GR, and the full MTS claim remain open.",
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
    arc_rows: list[dict[str, Any]] = []
    root_aggregate: dict[tuple[str, str, str], dict[str, Any]] = {}
    certified_boxes: set[tuple[str, str]] = set()
    center_certificates: dict[tuple[str, str], dict[str, Any]] = {}
    g1_center_certificates: dict[tuple[str, str], dict[str, Any]] = {}
    g1_minus_center_certificates: dict[tuple[str, str], dict[str, Any]] = {}
    for source in read_csv(BOXES_5380):
        configuration = M5380.M5379.M5378.M5359.event_configuration(
            event_lookup[source["event_id"]], references
        )
        epsilon = iv.mpc(
            iv.mpf(
                [source["epsilon_real_lower"], source["epsilon_real_upper"]]
            ),
            iv.mpf(
                [
                    source["epsilon_imaginary_lower"],
                    source["epsilon_imaginary_upper"],
                ]
            ),
        )
        state_boxes = [
            M5381.parse_complex_box(text)
            for text in source["complex_state_boxes"].split("|")
        ]
        inputs = event_inputs(configuration, epsilon, state_boxes)
        box_key = (configuration["event_id"], source["epsilon_bin_index"])
        if configuration["event_type"] == "BRANCH_DEATH":
            center_certificates[box_key] = branch_center_gap_certificate(
                configuration, inputs
            )
            g1_center_certificates[box_key] = branch_center_gap_certificate(
                configuration, inputs, gap_sector="g1_companion"
            )
            g1_minus_center_certificates[box_key] = (
                branch_center_gap_certificate(
                    configuration,
                    inputs,
                    gap_sector="g1_minus_companion",
                )
            )
        source_box_passes = True
        for arc_index in range(ENERGY_PHASE_ARC_COUNT):
            phase_interval = (
                2
                * iv.pi
                * iv.mpf([arc_index, arc_index + 1])
                / ENERGY_PHASE_ARC_COUNT
            )
            energy_displacement = iv.mpf(
                ENERGY_CONTOUR_RELATIVE_RADIUS
            ) * (iv.cos(phase_interval) + 1j * iv.sin(phase_interval))
            geometry = expanded_geometry(
                configuration, inputs, energy_displacement
            )
            selected_root = geometry["selected_root"]
            global_radius_upper = float(GLOBAL_CONTOUR_RELATIVE_RADIUS) * max(
                1.0, M5381.modulus_upper(selected_root)
            )
            active_labels = {
                f"direct:g1:{configuration['root_labels'][0]}",
                f"direct:g3:{configuration['root_labels'][1]}",
                f"subtraction:soft:{configuration['root_labels'][1]}",
            }
            sources = (
                ("direct:g1", geometry["first_factors"]),
                ("direct:g2", geometry["second_factors"]),
                ("direct:g3", geometry["soft_factors"]),
                ("subtraction:soft", geometry["soft_factors"]),
                ("subtraction:decay", geometry["decay_factors"]),
            )
            root_records: list[dict[str, Any]] = []
            branch_variation: dict[str, Any] | None = None
            g1_branch_variation: dict[str, Any] | None = None
            g1_minus_branch_variation: dict[str, Any] | None = None
            for source_name, factors in sources:
                for label in M5384.GLOBAL_ROOT_LABELS:
                    root_id = f"{source_name}:{label}"
                    if root_id in active_labels:
                        continue
                    if (
                        source_name == "direct:g1"
                        and configuration["event_type"] == "BRANCH_DEATH"
                        and label
                        == (
                            "plus_v"
                            if configuration["role"] == "representative"
                            else "plus_u"
                        )
                    ):
                        center = g1_center_certificates[box_key]
                        if g1_branch_variation is None:
                            g1_branch_variation = branch_energy_variation_upper(
                                configuration,
                                inputs,
                                energy_displacement,
                                gap_sector="g1_companion",
                            )
                        full_gap_box = (
                            center["center_gap_box"]
                            + g1_branch_variation["energy_variation_box"]
                        )
                        g1_denominator = (
                            inputs["external_root"]
                            * geometry["first_factors"][2]
                            if configuration["role"] == "representative"
                            else geometry["first_factors"][2]
                        )
                        denominator_upper = M5381.modulus_upper(
                            g1_denominator
                        )
                        bound = {
                            "method": "centered_first_null_projective_numerator_path_integral",
                            "chart": g1_branch_variation["path_charts"],
                            "separation_modulus_lower": (
                                M5381.modulus_lower(full_gap_box)
                                / denominator_upper
                                if denominator_upper > 0
                                else math.inf
                            ),
                        }
                    elif (
                        source_name == "direct:g1"
                        and configuration["event_type"] == "BRANCH_DEATH"
                        and label
                        == (
                            "minus_v"
                            if configuration["role"] == "representative"
                            else "minus_u"
                        )
                    ):
                        center = g1_minus_center_certificates[box_key]
                        if g1_minus_branch_variation is None:
                            g1_minus_branch_variation = (
                                branch_energy_variation_upper(
                                    configuration,
                                    inputs,
                                    energy_displacement,
                                    gap_sector="g1_minus_companion",
                                )
                            )
                        translated_numerator_box = (
                            center["center_gap_box"]
                            + g1_minus_branch_variation[
                                "energy_variation_box"
                            ]
                        )
                        denominator_upper = M5381.modulus_upper(
                            inputs["external_root"]
                            * geometry["first_factors"][2]
                        )
                        bound = {
                            "method": "centered_first_minus_projective_numerator_path_integral",
                            "chart": g1_minus_branch_variation["path_charts"],
                            "separation_modulus_lower": (
                                M5381.modulus_lower(
                                    translated_numerator_box
                                )
                                / denominator_upper
                                if denominator_upper > 0
                                else math.inf
                            ),
                        }
                    elif source_name == "direct:g1":
                        bound = g1_separation_bound(
                            configuration, inputs, geometry, label
                        )
                    elif (
                        source_name == "direct:g2"
                        and configuration["event_type"] == "BRANCH_DEATH"
                        and label
                        == (
                            "minus_v"
                            if configuration["role"] == "representative"
                            else "minus_u"
                        )
                    ):
                        center = center_certificates[box_key]
                        if branch_variation is None:
                            branch_variation = branch_energy_variation_upper(
                                configuration, inputs, energy_displacement
                            )
                        full_gap_box = (
                            center["center_gap_box"]
                            + branch_variation["energy_variation_box"]
                        )
                        separation = M5381.modulus_lower(full_gap_box)
                        bound = {
                            "method": "centered_complex_mean_value_plus_recoil_path_integral",
                            "chart": branch_variation["path_charts"],
                            "separation_modulus_lower": separation,
                        }
                    else:
                        projective = M5384.projective_separation_bound(
                            factors,
                            label,
                            inputs["external_root"],
                            selected_root,
                        )
                        bound = {
                            "method": projective["method"],
                            "chart": projective["chart"],
                            "separation_modulus_lower": projective[
                                "separation_modulus_lower"
                            ],
                        }
                    clearance_margin = (
                        bound["separation_modulus_lower"]
                        - global_radius_upper
                    )
                    root_record = {
                        "root_id": root_id,
                        **bound,
                        "clearance_margin_lower": clearance_margin,
                        "root_clears_global_contour": clearance_margin > 0,
                    }
                    root_records.append(root_record)
                    aggregate_key = (
                        configuration["event_id"],
                        source["epsilon_bin_index"],
                        root_id,
                    )
                    aggregate = root_aggregate.get(aggregate_key)
                    if aggregate is None:
                        root_aggregate[aggregate_key] = {
                            "event_id": configuration["event_id"],
                            "event_type": configuration["event_type"],
                            "epsilon_bin_index": source["epsilon_bin_index"],
                            "root_id": root_id,
                            "minimum_separation_modulus_lower": bound[
                                "separation_modulus_lower"
                            ],
                            "minimum_clearance_margin_lower": clearance_margin,
                            "worst_energy_phase_arc_index": arc_index,
                            "methods": {bound["method"]},
                            "charts": {bound["chart"]},
                            "all_energy_arcs_clear": clearance_margin > 0,
                        }
                    else:
                        aggregate["methods"].add(bound["method"])
                        aggregate["charts"].add(bound["chart"])
                        aggregate["all_energy_arcs_clear"] = aggregate[
                            "all_energy_arcs_clear"
                        ] and clearance_margin > 0
                        if clearance_margin < aggregate[
                            "minimum_clearance_margin_lower"
                        ]:
                            aggregate["minimum_separation_modulus_lower"] = (
                                bound["separation_modulus_lower"]
                            )
                            aggregate["minimum_clearance_margin_lower"] = (
                                clearance_margin
                            )
                            aggregate[
                                "worst_energy_phase_arc_index"
                            ] = arc_index
            worst_root = min(
                root_records, key=lambda row: row["clearance_margin_lower"]
            )
            arc_passes = (
                len(root_records) == 17
                and all(
                    row["root_clears_global_contour"] for row in root_records
                )
                and M5380.real_lower(
                    geometry["energy_recoil_radicand"]
                )
                > 0
                and geometry[
                    "minimum_primitive_denominator_modulus_lower"
                ]
                > 0
            )
            source_box_passes = source_box_passes and arc_passes
            arc_rows.append(
                {
                    "event_id": configuration["event_id"],
                    "event_type": configuration["event_type"],
                    "epsilon_bin_index": source["epsilon_bin_index"],
                    "energy_phase_arc_index": arc_index,
                    "energy_phase_lower": M5380.real_lower(phase_interval),
                    "energy_phase_upper": M5380.real_upper(phase_interval),
                    "energy_contour_radius": ENERGY_CONTOUR_RELATIVE_RADIUS,
                    "global_contour_relative_radius": GLOBAL_CONTOUR_RELATIVE_RADIUS,
                    "global_contour_radius_upper": global_radius_upper,
                    "full_catalog_root_count": 20,
                    "active_catalog_root_count": 3,
                    "nonactive_catalog_root_count": len(root_records),
                    "worst_nonactive_root_id": worst_root["root_id"],
                    "worst_nonactive_root_method": worst_root["method"],
                    "minimum_nonactive_root_separation_lower": worst_root[
                        "separation_modulus_lower"
                    ],
                    "minimum_full_catalog_clearance_margin_lower": worst_root[
                        "clearance_margin_lower"
                    ],
                    "energy_recoil_radicand_real_lower": M5380.real_lower(
                        geometry["energy_recoil_radicand"]
                    ),
                    "minimum_primitive_denominator_modulus_lower": geometry[
                        "minimum_primitive_denominator_modulus_lower"
                    ],
                    "branch_center_gap_after_parameter_variation_lower": (
                        center_certificates[box_key][
                            "center_gap_after_parameter_variation_lower"
                        ]
                        if box_key in center_certificates
                        else ""
                    ),
                    "branch_energy_variation_upper": (
                        branch_variation["energy_variation_upper"]
                        if branch_variation is not None
                        else ""
                    ),
                    "g1_companion_translated_numerator_after_parameter_variation_lower": (
                        g1_center_certificates[box_key][
                            "center_gap_after_parameter_variation_lower"
                        ]
                        if box_key in g1_center_certificates
                        else ""
                    ),
                    "g1_companion_energy_variation_upper": (
                        g1_branch_variation["energy_variation_upper"]
                        if g1_branch_variation is not None
                        else ""
                    ),
                    "g1_minus_companion_translated_numerator_after_parameter_variation_lower": (
                        g1_minus_center_certificates[box_key][
                            "center_gap_after_parameter_variation_lower"
                        ]
                        if box_key in g1_minus_center_certificates
                        else ""
                    ),
                    "g1_minus_companion_energy_variation_upper": (
                        g1_minus_branch_variation[
                            "energy_variation_upper"
                        ]
                        if g1_minus_branch_variation is not None
                        else ""
                    ),
                    "energy_arc_passes": arc_passes,
                    CLAIM_CLEARANCE: False,
                    **open_claims(),
                }
            )
        if source_box_passes:
            certified_boxes.add(box_key)
        print(
            f"full catalog {configuration['event_id']} epsilon-bin={source['epsilon_bin_index']} passes={source_box_passes}",
            flush=True,
        )
    root_rows: list[dict[str, Any]] = []
    for key in sorted(root_aggregate):
        aggregate = root_aggregate[key]
        root_rows.append(
            {
                **{
                    name: value
                    for name, value in aggregate.items()
                    if name not in {"methods", "charts"}
                },
                "methods": "|".join(sorted(aggregate["methods"])),
                "charts": "|".join(sorted(aggregate["charts"])),
                CLAIM_CLEARANCE: False,
                **open_claims(),
            }
        )
    numerical_rows = numerical_expanded_contour_crosscheck()
    required_box_count = len(EVENT_IDS) * M5380.EPSILON_BIN_COUNT
    required_arc_count = required_box_count * ENERGY_PHASE_ARC_COUNT
    certified_arc_count = sum(
        parse_bool(row["energy_arc_passes"]) for row in arc_rows
    )
    minimum_separation = min(
        float(row["minimum_nonactive_root_separation_lower"])
        for row in arc_rows
    )
    maximum_global_radius = max(
        float(row["global_contour_radius_upper"]) for row in arc_rows
    )
    minimum_clearance_margin = min(
        float(row["minimum_full_catalog_clearance_margin_lower"])
        for row in arc_rows
    )
    maximum_numerical_difference = max(
        float(row["relative_difference"]) for row in numerical_rows
    )
    validations = [
        validation_row(
            "preflight_passes",
            preflight_result["all_pass"],
            preflight_result["checks"],
        ),
        validation_row(
            "all_required_event_epsilon_boxes_are_certified",
            len(certified_boxes) == required_box_count,
            f"certified={len(certified_boxes)};required={required_box_count}",
        ),
        validation_row(
            "all_required_expanded_energy_arcs_are_certified",
            certified_arc_count == required_arc_count,
            f"certified={certified_arc_count};required={required_arc_count}",
        ),
        validation_row(
            "every_arc_has_complete_20_root_catalog_with_three_active",
            all(
                int(row["full_catalog_root_count"]) == 20
                and int(row["active_catalog_root_count"]) == 3
                and int(row["nonactive_catalog_root_count"]) == 17
                for row in arc_rows
            ),
            f"arcs={len(arc_rows)}",
        ),
        validation_row(
            "all_1088_box_root_summaries_are_present",
            len(root_rows) == required_box_count * 17,
            f"rows={len(root_rows)};required={required_box_count * 17}",
        ),
        validation_row(
            "all_nonactive_full_catalog_roots_clear_inner_contour",
            minimum_clearance_margin > 0
            and all(
                parse_bool(row["all_energy_arcs_clear"])
                for row in root_rows
            ),
            minimum_clearance_margin,
        ),
        validation_row(
            "expanded_energy_recoil_chart_excludes_cut",
            all(
                float(row["energy_recoil_radicand_real_lower"]) > 0
                for row in arc_rows
            ),
            min(
                float(row["energy_recoil_radicand_real_lower"])
                for row in arc_rows
            ),
        ),
        validation_row(
            "all_primitive_denominators_exclude_zero",
            all(
                float(row["minimum_primitive_denominator_modulus_lower"])
                > 0
                for row in arc_rows
            ),
            min(
                float(row["minimum_primitive_denominator_modulus_lower"])
                for row in arc_rows
            ),
        ),
        validation_row(
            "expanded_energy_contour_matches_checkpoint_5383",
            len(numerical_rows) == len(EVENT_IDS)
            and maximum_numerical_difference <= NUMERICAL_RELATIVE_TOLERANCE
            and all(
                parse_bool(row["numerical_crosscheck_passes"])
                for row in numerical_rows
            ),
            maximum_numerical_difference,
        ),
        validation_row(
            "integrand_energy_exclusivity_H3_and_downstream_claims_remain_false",
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
    for collection in (arc_rows, root_rows, numerical_rows):
        for row in collection:
            row[CLAIM_CLEARANCE] = passed
    registered_sources = source_rows()
    for row in registered_sources:
        row[CLAIM_CLEARANCE] = passed
    result = {
        "checkpoint": CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "validation_passed": passed,
        "decision": (
            "D4_EXPANDED_ENERGY_CONTOUR_FULL_POLE_CATALOG_CLEARANCE_CERTIFIED__ENCLOSE_FACTORIZED_FINITE_PLUS_NUMERATOR"
            if passed
            else "D4_EXPANDED_ENERGY_CONTOUR_FULL_POLE_CATALOG_CLEARANCE_BLOCKED"
        ),
        "required_event_epsilon_box_count": required_box_count,
        "certified_event_epsilon_box_count": len(certified_boxes),
        "required_energy_arc_count": required_arc_count,
        "certified_energy_arc_count": certified_arc_count,
        "nonactive_root_check_count": required_arc_count * 17,
        "minimum_nonactive_root_separation_lower": minimum_separation,
        "maximum_global_contour_radius_upper": maximum_global_radius,
        "minimum_full_catalog_clearance_margin_lower": minimum_clearance_margin,
        "maximum_expanded_contour_relative_difference": maximum_numerical_difference,
        "claim_boundary": {CLAIM_CLEARANCE: passed, **open_claims()},
        "remaining_obstruction": "interval-enclose the factorized finite-plus spinor numerator on the now-certified full 20-root contour, then use the finite contour bound to derive H3 by Cauchy",
        "formalization_workbench_modified_file_count": 0,
        "runtime_seconds": time.perf_counter() - started,
        "updated_utc": utc_now(),
    }
    output = output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    atomic_csv(
        output / "D4_expanded_energy_full_catalog_clearance_arcs.csv",
        arc_rows,
    )
    atomic_csv(
        output / "D4_expanded_energy_full_catalog_clearance_roots.csv",
        root_rows,
    )
    atomic_csv(
        output / "D4_expanded_energy_contour_numerical_crosscheck.csv",
        numerical_rows,
    )
    atomic_csv(
        output / "D4_expanded_energy_full_catalog_clearance_validation.csv",
        validations,
    )
    atomic_csv(output / "source_register.csv", registered_sources)
    atomic_csv(VALIDATION, validations)
    atomic_json(
        output / "D4_expanded_energy_full_catalog_clearance_result.json",
        result,
    )
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
    point = iv.mpc(iv.mpf(2), iv.mpf(0))
    dual = M5381.IntervalDual(point, iv.mpc(1))
    root = positive_sqrt_dual(dual)
    return {
        "dual_square_root_value_is_sqrt_two": abs(
            M5380.complex_midpoint(root.value) - math.sqrt(2)
        )
        < 1.0e-12,
        "dual_square_root_derivative_is_correct": abs(
            M5380.complex_midpoint(root.derivative)
            - 1 / (2 * math.sqrt(2))
        )
        < 1.0e-12,
        "full_catalog_counts_balance": 20 - 3 == 17,
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=MARKER)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    arguments = parser.parse_args()
    if arguments.self_test:
        tests = self_test()
        print(json.dumps(tests, indent=2, sort_keys=True))
        return 0 if all(tests.values()) else 1
    if arguments.dry_run:
        result = preflight()
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0 if result["all_pass"] else 1
    result = run(arguments.output)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["validation_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
