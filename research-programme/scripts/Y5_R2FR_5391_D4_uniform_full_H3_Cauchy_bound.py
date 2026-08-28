from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
from decimal import Decimal, localcontext
import hashlib
import json
import math
import os
from pathlib import Path
import sys
import time
from typing import Any


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
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
RESIDUALS = POST / "source-intake" / "mts_residuals"
OUTPUT = FUNCTIONAL_RG / "5391"
DOCUMENT = POST / "5391-Y5-R2FR-D4-uniform-full-H3-Cauchy-bound.md"
VALIDATION = RESIDUALS / "P8_Y5_BRR545_5391_VALIDATION.csv"

BASE_BOXES = FUNCTIONAL_RG / "5380" / "D4_complexified_event_neighborhood_boxes.csv"
HALO_BOXES = FUNCTIONAL_RG / "5387" / "D4_Cauchy_endpoint_halo_boxes.csv"
HALO_RESULT = FUNCTIONAL_RG / "5387" / "D4_Cauchy_endpoint_halo_result.json"
ENDPOINT_COEFFICIENTS = FUNCTIONAL_RG / "5359" / "D4_zero_regulator_endpoint_coefficients.csv"
ENDPOINT_RESULT = FUNCTIONAL_RG / "5359" / "D4_zero_regulator_endpoint_result.json"
SUBTRACTION_ZERO_RESULT = FUNCTIONAL_RG / "5388" / "D4_subtraction_double_pole_zero_result.json"
INTEGRAND_RESULT = FUNCTIONAL_RG / "5390" / "D4_reserved_outer_C0_result.json"
GEOMETRY_ROWS = FUNCTIONAL_RG / "5389" / "D4_full_H_event_geometry_bridge.csv"
GEOMETRY_SEAMS = FUNCTIONAL_RG / "5389" / "D4_full_H_event_branch_seams.csv"
GEOMETRY_RESULT = FUNCTIONAL_RG / "5389" / "D4_full_H_event_geometry_bridge_result.json"

CHECKPOINT = 5391
MARKER = "MTS_5391_D4_UNIFORM_FULL_H3_CAUCHY_BOUND"
REVISION = "D4-uniform-full-H3-Cauchy-bound-v2-physical-center-witness"
REGULATOR_CAUCHY_RADIUS = 5.0e-7
TARGET_REAL_INTERVAL = (0.0, 0.02)
EVENT_IDS = tuple(f"E{index:02d}" for index in range(1, 9))
ENERGY_ARC_COUNT = 32
GLOBAL_ARC_COUNT = 1
POINT_WITNESS_MODE = "physical_event_center_solution"

CLAIM_FULL_H = "valid_for_D4_full_H_event_enclosure"
CLAIM_H3 = "valid_for_D4_numeric_H3_bound"
OPEN_CLAIMS = (
    "valid_for_D4_numeric_uniform_remainder_bound",
    "valid_for_D4_outer_regulator_zero_limit",
    "valid_for_decay_angle_integral",
    "valid_for_full_angular_convergence",
    "valid_for_full_phase_space_coefficient",
    "valid_for_numeric_UV_claim",
    "valid_for_local_GR_claim",
    "valid_for_full_MTS_claim",
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


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


def upward(value: float) -> float:
    return math.nextafter(float(value), math.inf)


def downward_positive(value: float) -> float:
    if value <= 0:
        return 0.0
    return math.nextafter(float(value), 0.0)


def outward_float(value: Decimal) -> float:
    candidate = float(value)
    if Decimal.from_float(candidate) < value:
        candidate = math.nextafter(candidate, math.inf)
    return candidate


def upward_average(values: list[float]) -> float:
    if not values:
        raise ValueError("cannot average an empty upper-bound sequence")
    with localcontext() as context:
        context.prec = 90
        total = sum(
            (Decimal.from_float(float(value)) for value in values), Decimal(0)
        )
        return outward_float(total / Decimal(len(values)))


def upward_product(values: list[float]) -> float:
    with localcontext() as context:
        context.prec = 90
        result = Decimal(1)
        for value in values:
            result *= Decimal.from_float(float(value))
        return outward_float(result)


def upward_sum(values: list[float]) -> float:
    with localcontext() as context:
        context.prec = 90
        return outward_float(
            sum(
                (Decimal.from_float(float(value)) for value in values),
                Decimal(0),
            )
        )


def upward_quotient(numerator: float, denominator: float) -> float:
    if denominator <= 0:
        raise ValueError("upper-bound quotient requires a positive denominator")
    with localcontext() as context:
        context.prec = 90
        return outward_float(
            Decimal.from_float(float(numerator))
            / Decimal.from_float(float(denominator))
        )


def cauchy_third_derivative_upper(value_sup: float, radius_lower: float) -> float:
    if radius_lower <= 0:
        raise ValueError("Cauchy radius must be positive")
    with localcontext() as context:
        context.prec = 90
        radius = Decimal.from_float(radius_lower)
        result = (
            Decimal(math.factorial(3))
            * Decimal.from_float(value_sup)
            / (radius * radius * radius)
        )
        return outward_float(result)


def interval_coverage(boxes: list[dict[str, str]]) -> dict[str, Any]:
    required_lower = TARGET_REAL_INTERVAL[0] - REGULATOR_CAUCHY_RADIUS
    required_upper = TARGET_REAL_INTERVAL[1] + REGULATOR_CAUCHY_RADIUS
    event_coverage: dict[str, Any] = {}
    for event_id in EVENT_IDS:
        event_boxes = [row for row in boxes if row["event_id"] == event_id]
        intervals = sorted(
            {
                (
                    float(row["epsilon_real_lower"]),
                    float(row["epsilon_real_upper"]),
                )
                for row in event_boxes
            }
        )
        merged: list[list[float]] = []
        for lower, upper in intervals:
            if not merged or lower > merged[-1][1]:
                merged.append([lower, upper])
            else:
                merged[-1][1] = max(merged[-1][1], upper)
        imaginary_half_width = min(
            (
                min(
                    abs(float(row["epsilon_imaginary_lower"])),
                    abs(float(row["epsilon_imaginary_upper"])),
                )
                for row in event_boxes
            ),
            default=0.0,
        )
        passes = (
            len(merged) == 1
            and merged[0][0] <= required_lower
            and merged[0][1] >= required_upper
            and imaginary_half_width >= REGULATOR_CAUCHY_RADIUS
        )
        event_coverage[event_id] = {
            "merged_real_intervals": merged,
            "imaginary_half_width": imaginary_half_width,
            "covers_regulator_Cauchy_disks": passes,
        }
    return {
        "required_real_interval": [required_lower, required_upper],
        "event_coverage": event_coverage,
        "covers_all_regulator_Cauchy_disks": all(
            row["covers_regulator_Cauchy_disks"]
            for row in event_coverage.values()
        ),
    }


def source_paths(run_dir: Path) -> tuple[Path, ...]:
    return tuple(
        dict.fromkeys(
            path.resolve()
            for path in (
                Path(__file__),
                run_dir / "rows.jsonl",
                run_dir / "COMPLETE.json",
                BASE_BOXES,
                HALO_BOXES,
                HALO_RESULT,
                ENDPOINT_COEFFICIENTS,
                ENDPOINT_RESULT,
                SUBTRACTION_ZERO_RESULT,
                INTEGRAND_RESULT,
                GEOMETRY_ROWS,
                GEOMETRY_SEAMS,
                GEOMETRY_RESULT,
            )
        )
    )


def render_document(result: dict[str, Any], events: list[dict[str, Any]]) -> None:
    lines = [
        "# 5391 — D4 uniform full-H3 Cauchy bound",
        "",
        "## Decision",
        "",
        f"`{result['decision']}`",
        "",
        "## Bound",
        "",
        f"- regulator-plane Cauchy radius: `{result['regulator_Cauchy_radius']}`;",
        f"- minimum soft-coordinate Cauchy radius: `{result['minimum_coordinate_Cauchy_radius_lower']}`;",
        f"- minimum regulator-bin seam inclusion margin: `{result['minimum_regulator_seam_inclusion_margin']}`;",
        f"- uniform full-H3 upper bound: `{result['uniform_full_H3_upper']}`;",
        f"- H-sector Taylor constant H3/6: `{result['H_sector_Taylor_constant_upper']}`.",
        "",
        "## Event bounds",
        "",
        "| event | sup C0 | sup C1 | sup |z0/z1| | sup full H | sup full H''' |",
        "|---|---:|---:|---:|---:|---:|",
    ]
    for row in events:
        lines.append(
            f"| {row['event_id']} | {row['C0_event_sup_abs_upper']} | {row['C1_event_sup_abs_upper']} | {row['ratio_event_sup_abs_upper']} | {row['full_H_event_sup_abs_upper']} | {row['full_H_event_third_derivative_sup_upper']} |"
        )
    lines.extend(
        [
            "",
            "## Derivation",
            "",
            "The reserved-outer contour sweep bounds the physical direct double-pole coefficient `C0` on every state box. Checkpoint 5388 proves that the subtraction has no double-pole coefficient. Checkpoint 5389 places a complex soft-coordinate disk of radius `rho_x` around every event branch while keeping every dependent component `(u,v,H,S)` inside that same state box, and separately patches all regulator-bin seams. Cauchy's estimate therefore gives `|C1| <= sup|C0|/rho_x` without importing a fitted finite difference.",
            "",
            "The exact parent affine endpoint coefficient is bounded boxwise by `|H| <= |C0||r| + |C1||r|^2/2`, with `r=z0/z1`. The 5380 strip and 5387 endpoint halos cover every regulator-plane disk of radius `rho_e` centered on `[0,0.02]`, so `sup|H'''| <= 3! sup|H|/rho_e^3`. The eight event bounds are then summed.",
            "",
            "## Scope",
            "",
            "This is deliberately an existence-grade enclosure and may be numerically loose. It closes only the H-sector derivative owner. G3 and mapped-away W3 remain required before the total uniform remainder and D4 outer limit can be claimed. Local GR and full MTS claims remain false.",
            "",
        ]
    )
    temporary = DOCUMENT.with_suffix(DOCUMENT.suffix + ".tmp")
    temporary.write_text("\n".join(lines), encoding="utf-8")
    os.replace(temporary, DOCUMENT)


def run(run_dir: Path, output: Path) -> dict[str, Any]:
    started = time.perf_counter()
    run_dir = run_dir.resolve()
    required = source_paths(run_dir)
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise FileNotFoundError(missing)
    contour_rows = read_jsonl(run_dir / "rows.jsonl")
    complete = read_json(run_dir / "COMPLETE.json")
    base_boxes = read_csv(BASE_BOXES)
    halo_boxes = read_csv(HALO_BOXES)
    all_boxes = [*base_boxes, *halo_boxes]
    halo_result = read_json(HALO_RESULT)
    endpoint_result = read_json(ENDPOINT_RESULT)
    subtraction_result = read_json(SUBTRACTION_ZERO_RESULT)
    integrand_result = read_json(INTEGRAND_RESULT)
    geometry_result = read_json(GEOMETRY_RESULT)
    geometry_rows = read_csv(GEOMETRY_ROWS)
    geometry_seams = read_csv(GEOMETRY_SEAMS)
    endpoint_rows = {
        row["event_id"]: row for row in read_csv(ENDPOINT_COEFFICIENTS)
    }
    box_keys = {
        (row["event_id"], int(row["epsilon_bin_index"])) for row in all_boxes
    }
    geometry_lookup = {
        (row["event_id"], int(row["epsilon_bin_index"])): row
        for row in geometry_rows
    }
    grouped: dict[tuple[str, int], list[dict[str, Any]]] = {}
    for row in contour_rows:
        key = (row["event_id"], int(row["epsilon_bin_index"]))
        grouped.setdefault(key, []).append(row)
    physical_multiplier = upward(abs(float(endpoint_result["physical_multiplier"])))
    box_bounds: list[dict[str, Any]] = []
    for key in sorted(box_keys):
        event_id, epsilon_bin_index = key
        group = grouped.get(key, [])
        geometry = geometry_lookup[key]
        unscaled_c0 = upward_average(
            [
                float(
                    row[
                        "event_integrand_abs_upper_without_physical_multiplier"
                    ]
                )
                for row in group
            ]
        )
        winding = max(
            abs(int(value))
            for value in endpoint_rows[event_id]["parent_windings"].split("|")
            if value
        )
        orientation = max(
            abs(int(value))
            for value in endpoint_rows[event_id]["parent_orientations"].split("|")
            if value
        )
        c0_upper = upward_product(
            [unscaled_c0, physical_multiplier, float(winding), float(orientation)]
        )
        coordinate_radius = downward_positive(
            float(geometry["coordinate_Cauchy_radius_lower"])
        )
        ratio_upper = upward(float(geometry["ratio_z0_over_z1_modulus_upper"]))
        c1_upper = upward_quotient(c0_upper, coordinate_radius)
        leading_upper = upward_product([c0_upper, ratio_upper])
        c1_correction_upper = upward_product(
            [0.5, c1_upper, ratio_upper, ratio_upper]
        )
        full_h_upper = upward_sum([leading_upper, c1_correction_upper])
        box_bounds.append(
            {
                "event_id": event_id,
                "epsilon_bin_index": epsilon_bin_index,
                "contour_arc_row_count": len(group),
                "absolute_winding": winding,
                "absolute_trace_orientation": orientation,
                "unscaled_C0_energy_contour_abs_upper": unscaled_c0,
                "physical_C0_abs_upper": c0_upper,
                "coordinate_Cauchy_radius_lower": coordinate_radius,
                "C1_abs_upper_from_coordinate_Cauchy": c1_upper,
                "ratio_z0_over_z1_abs_upper": ratio_upper,
                "leading_C0_r_abs_upper": leading_upper,
                "C1_r_squared_over_two_abs_upper": c1_correction_upper,
                "full_H_abs_upper": full_h_upper,
                CLAIM_FULL_H: False,
                CLAIM_H3: False,
                **{claim: False for claim in OPEN_CLAIMS},
            }
        )
    regulator_radius = downward_positive(REGULATOR_CAUCHY_RADIUS)
    event_bounds: list[dict[str, Any]] = []
    for event_id in EVENT_IDS:
        selected = [row for row in box_bounds if row["event_id"] == event_id]
        full_h_sup = upward(max(float(row["full_H_abs_upper"]) for row in selected))
        event_bounds.append(
            {
                "event_id": event_id,
                "box_count": len(selected),
                "C0_event_sup_abs_upper": upward(
                    max(float(row["physical_C0_abs_upper"]) for row in selected)
                ),
                "C1_event_sup_abs_upper": upward(
                    max(
                        float(row["C1_abs_upper_from_coordinate_Cauchy"])
                        for row in selected
                    )
                ),
                "ratio_event_sup_abs_upper": upward(
                    max(
                        float(row["ratio_z0_over_z1_abs_upper"])
                        for row in selected
                    )
                ),
                "full_H_event_sup_abs_upper": full_h_sup,
                "full_H_event_third_derivative_sup_upper": cauchy_third_derivative_upper(
                    full_h_sup, regulator_radius
                ),
                CLAIM_FULL_H: False,
                CLAIM_H3: False,
                **{claim: False for claim in OPEN_CLAIMS},
            }
        )
    coverage = interval_coverage(all_boxes)
    expected_rows = len(box_keys) * ENERGY_ARC_COUNT * GLOBAL_ARC_COUNT
    contour_keys = [
        (
            row["event_id"],
            int(row["epsilon_bin_index"]),
            int(row["epsilon_subdivision_index"]),
            int(row["energy_phase_arc_index"]),
            int(row["global_phase_arc_index"]),
        )
        for row in contour_rows
    ]
    complete_groups = set(grouped) == box_keys and all(
        len(group) == ENERGY_ARC_COUNT * GLOBAL_ARC_COUNT
        and {int(row["energy_phase_arc_index"]) for row in group}
        == set(range(ENERGY_ARC_COUNT))
        and {int(row["global_phase_arc_index"]) for row in group}
        == set(range(GLOBAL_ARC_COUNT))
        for group in grouped.values()
    )
    all_contour_rows_pass = all(
        row.get("smoke_passes") is True
        and not row.get("error")
        and row.get("parent_value_is_in_nested_interval") is True
        and row.get("point_witness_mode") == POINT_WITNESS_MODE
        and row.get("point_witness_is_in_state_boxes") is True
        and math.isfinite(
            float(row["event_integrand_abs_upper_without_physical_multiplier"])
        )
        for row in contour_rows
    )
    minimum_geometric_factor = min(
        float(row[field])
        for row in contour_rows
        for field in (
            "relative_root_modulus_lower",
            "selected_global_root_modulus_lower",
            "collision_jacobian_modulus_lower",
        )
    )
    uniform_h3 = upward_sum(
        [
            float(row["full_H_event_third_derivative_sup_upper"])
            for row in event_bounds
        ]
    )
    validations = [
        {
            "gate": "all_required_sources_exist",
            "passed": not missing,
            "detail": len(required),
        },
        {
            "gate": "reserved_outer_run_complete_and_explicitly_uncontracted",
            "passed": complete.get("all_rows_pass") is True
            and complete.get("state_box_contraction_limit") == 0
            and complete.get("point_witness_mode") == POINT_WITNESS_MODE,
            "detail": json.dumps(complete, sort_keys=True),
        },
        {
            "gate": "matrix_contains_64_base_and_16_halo_boxes",
            "passed": len(base_boxes) == 64
            and len(halo_boxes) == 16
            and len(box_keys) == 80,
            "detail": f"base={len(base_boxes)};halo={len(halo_boxes)};keys={len(box_keys)}",
        },
        {
            "gate": "contour_matrix_has_exact_unique_row_count",
            "passed": len(contour_rows) == expected_rows
            and len(contour_keys) == len(set(contour_keys)),
            "detail": f"rows={len(contour_rows)};expected={expected_rows}",
        },
        {
            "gate": "every_box_has_complete_arc_matrix",
            "passed": complete_groups,
            "detail": len(grouped),
        },
        {
            "gate": "every_reserved_outer_contour_row_passes",
            "passed": all_contour_rows_pass,
            "detail": len(contour_rows),
        },
        {
            "gate": "all_contour_geometric_factors_exclude_zero",
            "passed": minimum_geometric_factor > 0
            and math.isfinite(minimum_geometric_factor),
            "detail": minimum_geometric_factor,
        },
        {
            "gate": "reserved_outer_C0_certificate_matches_run",
            "passed": integrand_result.get("validation_passed") is True
            and Path(integrand_result["source_run_directory"]).resolve()
            == run_dir
            and integrand_result.get("state_box_contraction_limit") == 0
            and integrand_result.get("point_witness_mode")
            == POINT_WITNESS_MODE
            and integrand_result.get("claim_boundary", {}).get(
                "valid_for_D4_reserved_outer_C0_contour_enclosure"
            )
            is True,
            "detail": integrand_result.get("source_run_directory"),
        },
        {
            "gate": "subtraction_double_pole_coefficient_is_certified_zero",
            "passed": subtraction_result.get("validation_passed") is True
            and subtraction_result.get(
                "subtraction_selected_global_pole_order_upper"
            )
            == 1
            and subtraction_result.get("subtraction_double_pole_coefficient")
            == 0,
            "detail": subtraction_result.get("decision"),
        },
        {
            "gate": "endpoint_residue_normalization_winding_and_orientation_are_source_certified",
            "passed": endpoint_result.get("validation_passed") is True
            and endpoint_result.get("claim_boundary", {}).get(
                "valid_for_D4_zero_regulator_parent_residue_evaluation"
            )
            is True
            and set(endpoint_rows) == set(EVENT_IDS)
            and all(
                set(row["parent_windings"].split("|")).issubset(
                    {"-2", "2"}
                )
                and set(row["parent_orientations"].split("|")) == {"1"}
                for row in endpoint_rows.values()
            ),
            "detail": endpoint_result.get("decision"),
        },
        {
            "gate": "full_H_geometry_and_coordinate_Cauchy_bridge_passes",
            "passed": geometry_result.get("validation_passed") is True
            and geometry_result.get("claim_boundary", {}).get(
                "valid_for_D4_full_H_event_geometry_and_coordinate_Cauchy_bridge"
            )
            is True
            and len(geometry_rows) == 80
            and set(geometry_lookup) == box_keys
            and len(geometry_seams) == 72
            and all(
                parse_bool(row["seam_Krawczyk_passes"])
                and float(row["seam_Krawczyk_minimum_inclusion_margin"])
                > 0
                and float(row["seam_Krawczyk_contraction_bound"]) < 1
                for row in geometry_seams
            )
            and all(
                int(row["reserved_outer_contraction_count"]) == 0
                and parse_bool(
                    row[
                        "coordinate_disk_and_complete_event_branch_remain_in_reserved_outer_box"
                    ]
                )
                for row in geometry_rows
            ),
            "detail": geometry_result.get("decision"),
        },
        {
            "gate": "endpoint_halo_and_regulator_Cauchy_coverage_pass",
            "passed": halo_result.get("validation_passed") is True
            and coverage["covers_all_regulator_Cauchy_disks"] is True,
            "detail": json.dumps(coverage, sort_keys=True),
        },
        {
            "gate": "physical_multiplier_is_positive_finite",
            "passed": physical_multiplier > 0 and math.isfinite(physical_multiplier),
            "detail": physical_multiplier,
        },
        {
            "gate": "all_boxwise_full_H_bounds_are_positive_finite",
            "passed": len(box_bounds) == 80
            and all(
                float(row["coordinate_Cauchy_radius_lower"]) > 0
                and math.isfinite(float(row["full_H_abs_upper"]))
                for row in box_bounds
            ),
            "detail": len(box_bounds),
        },
        {
            "gate": "all_eight_full_H3_event_bounds_are_finite",
            "passed": len(event_bounds) == 8
            and all(
                math.isfinite(
                    float(row["full_H_event_third_derivative_sup_upper"])
                )
                for row in event_bounds
            ),
            "detail": len(event_bounds),
        },
    ]
    validation_passed = all(parse_bool(row["passed"]) for row in validations)
    for row in (*box_bounds, *event_bounds):
        row[CLAIM_FULL_H] = validation_passed
        row[CLAIM_H3] = validation_passed
    registered_sources = [
        {
            "path": str(path),
            "exists": path.is_file(),
            "sha256": digest(path),
            CLAIM_FULL_H: validation_passed,
            CLAIM_H3: validation_passed,
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
            "UNIFORM_FULL_H3_CAUCHY_BOUND_CERTIFIED__PROCEED_TO_G3_AND_W3"
            if validation_passed
            else "UNIFORM_FULL_H3_CAUCHY_BOUND_BLOCKED"
        ),
        "source_run_directory": str(run_dir),
        "point_witness_mode": POINT_WITNESS_MODE,
        "contour_row_count": len(contour_rows),
        "box_bound_count": len(box_bounds),
        "event_bound_count": len(event_bounds),
        "regulator_Cauchy_radius": REGULATOR_CAUCHY_RADIUS,
        "minimum_coordinate_Cauchy_radius_lower": min(
            float(row["coordinate_Cauchy_radius_lower"]) for row in box_bounds
        ),
        "minimum_regulator_seam_inclusion_margin": float(
            geometry_result["minimum_seam_Krawczyk_inclusion_margin"]
        ),
        "maximum_ratio_z0_over_z1_abs_upper": max(
            float(row["ratio_z0_over_z1_abs_upper"]) for row in box_bounds
        ),
        "minimum_contour_geometric_factor_lower": minimum_geometric_factor,
        "uniform_full_H3_upper": uniform_h3,
        "H_sector_Taylor_constant_upper": upward_quotient(uniform_h3, 6.0),
        "claim_boundary": {
            CLAIM_FULL_H: validation_passed,
            CLAIM_H3: validation_passed,
            **{claim: False for claim in OPEN_CLAIMS},
        },
        "remaining_obstruction": "derive finite G3 for the nonlogarithmic endpoint primitives and W3 for the parent-frozen mapped-away cells before claiming the total D4 uniform remainder or outer limit",
        "formalization_workbench_modified_file_count": 0,
        "runtime_seconds": time.perf_counter() - started,
        "updated_utc": datetime.now(timezone.utc).isoformat(),
    }
    output = output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    atomic_csv(output / "D4_uniform_full_H_box_bounds.csv", box_bounds)
    atomic_csv(output / "D4_uniform_full_H3_event_bounds.csv", event_bounds)
    atomic_csv(output / "D4_uniform_full_H3_validation.csv", validations)
    atomic_csv(output / "source_register.csv", registered_sources)
    atomic_csv(VALIDATION, validations)
    atomic_json(output / "D4_uniform_full_H3_result.json", result)
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
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    arguments = parser.parse_args()
    result = run(arguments.run_dir, arguments.output)
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["validation_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
