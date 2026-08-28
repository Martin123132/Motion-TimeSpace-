from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
from decimal import Decimal, localcontext
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
OUTPUT = FUNCTIONAL_RG / "5388"
DOCUMENT = POST / "5388-Y5-R2FR-D4-uniform-H3-Cauchy-bound.md"
BASE_BOXES = FUNCTIONAL_RG / "5380" / "D4_complexified_event_neighborhood_boxes.csv"
HALO_BOXES = FUNCTIONAL_RG / "5387" / "D4_Cauchy_endpoint_halo_boxes.csv"
HALO_RESULT = FUNCTIONAL_RG / "5387" / "D4_Cauchy_endpoint_halo_result.json"
ENDPOINT_COEFFICIENTS = FUNCTIONAL_RG / "5359" / "D4_zero_regulator_endpoint_coefficients.csv"
ENDPOINT_RESULT = FUNCTIONAL_RG / "5359" / "D4_zero_regulator_endpoint_result.json"
SUBTRACTION_ZERO_RESULT = (
    FUNCTIONAL_RG / "5388" / "D4_subtraction_double_pole_zero_result.json"
)
INTEGRAND_RESULT = (
    FUNCTIONAL_RG / "5386" / "D4_nested_contour_integrand_result.json"
)
CAUCHY_RADIUS = 5.0e-7
TARGET_REAL_INTERVAL = (0.0, 0.02)
EVENT_IDS = tuple(f"E{index:02d}" for index in range(1, 9))
ENERGY_ARC_COUNT = 32
GLOBAL_ARC_COUNT = 1


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def atomic_json(path: Path, payload: dict[str, Any]) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def atomic_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"cannot write empty CSV {path}")
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    os.replace(temporary, path)


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


def upward(value: float) -> float:
    return math.nextafter(float(value), math.inf)


def outward_float(value: Decimal) -> float:
    candidate = float(value)
    if Decimal.from_float(candidate) < value:
        candidate = math.nextafter(candidate, math.inf)
    return candidate


def upward_average(values: list[float]) -> float:
    if not values:
        raise ValueError("cannot average an empty upper-bound sequence")
    with localcontext() as context:
        context.prec = 80
        total = sum(
            (Decimal.from_float(float(value)) for value in values),
            Decimal(0),
        )
        return outward_float(total / Decimal(len(values)))


def upward_product(values: list[float]) -> float:
    with localcontext() as context:
        context.prec = 80
        result = Decimal(1)
        for value in values:
            result *= Decimal.from_float(float(value))
        return outward_float(result)


def upward_sum(values: list[float]) -> float:
    with localcontext() as context:
        context.prec = 80
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
        context.prec = 80
        result = Decimal.from_float(float(numerator)) / Decimal.from_float(
            float(denominator)
        )
        return outward_float(result)


def cauchy_third_derivative_upper(event_sup: float, radius_lower: float) -> float:
    with localcontext() as context:
        context.prec = 80
        radius = Decimal.from_float(radius_lower)
        result = (
            Decimal(math.factorial(3))
            * Decimal.from_float(event_sup)
            / (radius * radius * radius)
        )
        return outward_float(result)


def interval_coverage(boxes: list[dict[str, str]]) -> dict[str, Any]:
    required_lower = TARGET_REAL_INTERVAL[0] - CAUCHY_RADIUS
    required_upper = TARGET_REAL_INTERVAL[1] + CAUCHY_RADIUS
    event_coverage: dict[str, Any] = {}
    for event_id in EVENT_IDS:
        event_boxes = [row for row in boxes if row["event_id"] == event_id]
        real_intervals = sorted(
            {
                (
                    float(row["epsilon_real_lower"]),
                    float(row["epsilon_real_upper"]),
                )
                for row in event_boxes
            }
        )
        merged: list[list[float]] = []
        for lower, upper in real_intervals:
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
        event_coverage[event_id] = {
            "merged_real_intervals": merged,
            "imaginary_half_width": imaginary_half_width,
            "covers_radius_rho_disks": (
                len(merged) == 1
                and merged[0][0] <= required_lower
                and merged[0][1] >= required_upper
                and imaginary_half_width >= CAUCHY_RADIUS
            ),
        }
    return {
        "event_coverage": event_coverage,
        "required_real_interval": [required_lower, required_upper],
        "covers_all_radius_rho_disks": all(
            row["covers_radius_rho_disks"]
            for row in event_coverage.values()
        ),
    }


def render_document(result: dict[str, Any], rows: list[dict[str, Any]]) -> None:
    lines = [
        "# 5388 — Y5/R2FR D4 uniform H3 Cauchy bound",
        "",
        "## Decision",
        "",
        f"`{result['decision']}`",
        "",
        "## Bound",
        "",
        f"- Cauchy radius rho: `{result['Cauchy_radius']}`;",
        f"- physical multiplier upper enclosure: `{result['physical_multiplier_upper']}`;",
        f"- uniform H3 bound: `{result['uniform_H3_upper']}`;",
        f"- corresponding H-sector Taylor constant H3/6: `{result['H_sector_Taylor_constant_upper']}`;",
        f"- minimum geometric factor lower bound: `{result['minimum_geometric_factor_lower']}`.",
        "",
        "## Event bounds",
        "",
        "| event | winding | sup abs H_k | sup abs H_k''' |",
        "|---|---:|---:|---:|",
    ]
    for row in rows:
        lines.append(
            f"| {row['event_id']} | {row['absolute_winding']} | {row['H_event_sup_abs_upper']} | {row['H_event_third_derivative_sup_upper']} |"
        )
    lines.extend(
        [
            "",
            "## Derivation",
            "",
            "For each event and complex regulator box, the continuous outer energy-contour average is bounded by the equal-arc average of the 32 interval arc bounds. The global inner contour has already been regularized by its exact double-zero factor. The separate 5388 subtraction certificate combines the checkpoint-5019 simple-pole theorem, the checkpoint-5385 base pole catalog, and endpoint-halo root clearance to prove that the subtraction has no double-pole Laurent coefficient. The direct term therefore owns H_k.",
            "",
            "The 5380 strip plus the 5387 overlapping endpoint halos contains every closed rho-disk centered on the real interval [0,0.02]. Cauchy's estimate therefore gives sup|H_k'''| <= 3! sup|H_k|/rho^3. Summing these eight event bounds gives H3.",
            "",
            "## Scope",
            "",
            "This closes the finite H-sector derivative bound. The number is deliberately loose and is an existence certificate, not a precision estimate. G3 and W3 are still required before the complete uniform remainder constant and D4 outer limit can be claimed. Local GR and full MTS claims remain false.",
            "",
        ]
    )
    temporary = DOCUMENT.with_suffix(DOCUMENT.suffix + ".tmp")
    temporary.write_text("\n".join(lines), encoding="utf-8")
    temporary.replace(DOCUMENT)


def run(run_dir: Path, output: Path) -> dict[str, Any]:
    raise RuntimeError(
        "retired C0-only H3 aggregator: the exact endpoint coefficient also requires "
        "r=z0/z1 and C1; use checkpoint 5389 plus the reserved-outer C0 sweep "
        "and Y5_R2FR_5391_D4_uniform_full_H3_Cauchy_bound.py"
    )
    started = time.perf_counter()
    rows_path = run_dir / "rows.jsonl"
    complete_path = run_dir / "COMPLETE.json"
    contour_rows = read_jsonl(rows_path)
    complete = json.loads(complete_path.read_text(encoding="utf-8"))
    base_boxes = read_csv(BASE_BOXES)
    halo_boxes = read_csv(HALO_BOXES)
    all_boxes = [*base_boxes, *halo_boxes]
    halo_result = json.loads(HALO_RESULT.read_text(encoding="utf-8"))
    endpoint_result = json.loads(ENDPOINT_RESULT.read_text(encoding="utf-8"))
    subtraction_zero_result = json.loads(
        SUBTRACTION_ZERO_RESULT.read_text(encoding="utf-8")
    )
    integrand_result = json.loads(INTEGRAND_RESULT.read_text(encoding="utf-8"))
    endpoint_rows = {
        row["event_id"]: row for row in read_csv(ENDPOINT_COEFFICIENTS)
    }
    box_keys = {
        (row["event_id"], int(row["epsilon_bin_index"]))
        for row in all_boxes
    }
    energy_arc_counts = {
        int(row["energy_phase_arc_count"]) for row in contour_rows
    }
    global_arc_counts = {
        int(row["global_phase_arc_count"]) for row in contour_rows
    }
    expected_rows = ENERGY_ARC_COUNT * GLOBAL_ARC_COUNT * len(box_keys)
    coverage = interval_coverage(all_boxes)
    physical_multiplier = upward(abs(float(endpoint_result["physical_multiplier"])))
    radius_lower = math.nextafter(CAUCHY_RADIUS, 0.0)
    grouped: dict[tuple[str, int, int], list[dict[str, Any]]] = {}
    for row in contour_rows:
        key = (
            row["event_id"],
            int(row["epsilon_bin_index"]),
            int(row["epsilon_subdivision_index"]),
        )
        grouped.setdefault(key, []).append(row)
    expected_group_keys = {
        (event_id, epsilon_bin_index, 0)
        for event_id, epsilon_bin_index in box_keys
    }
    event_rows: list[dict[str, Any]] = []
    for event_id in EVENT_IDS:
        box_bounds: list[float] = []
        for key, group in grouped.items():
            if key[0] != event_id:
                continue
            bounds = [
                float(
                    row[
                        "event_integrand_abs_upper_without_physical_multiplier"
                    ]
                )
                for row in group
            ]
            box_bounds.append(upward_average(bounds))
        unscaled_sup = upward(max(box_bounds))
        winding_values = [
            abs(int(value))
            for value in endpoint_rows[event_id]["parent_windings"].split("|")
            if value
        ]
        orientation_values = [
            abs(int(value))
            for value in endpoint_rows[event_id]["parent_orientations"].split(
                "|"
            )
            if value
        ]
        absolute_winding = max(winding_values)
        absolute_orientation = max(orientation_values)
        event_sup = upward_product(
            [
                unscaled_sup,
                physical_multiplier,
                float(absolute_winding),
                float(absolute_orientation),
            ]
        )
        derivative_sup = cauchy_third_derivative_upper(
            event_sup, radius_lower
        )
        event_rows.append(
            {
                "event_id": event_id,
                "box_count": len(box_bounds),
                "absolute_winding": absolute_winding,
                "absolute_trace_orientation": absolute_orientation,
                "unscaled_energy_contour_sup_abs_upper": unscaled_sup,
                "H_event_sup_abs_upper": event_sup,
                "H_event_third_derivative_sup_upper": derivative_sup,
                "valid_for_D4_numeric_H3_bound": False,
                "valid_for_D4_numeric_uniform_remainder_bound": False,
                "valid_for_D4_outer_regulator_zero_limit": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    all_rows_pass = all(
        row.get("smoke_passes") is True
        and not row.get("error")
        and row.get("parent_value_is_in_nested_interval") is True
        and math.isfinite(
            float(
                row[
                    "event_integrand_abs_upper_without_physical_multiplier"
                ]
            )
        )
        for row in contour_rows
    )
    geometric_fields = (
        "relative_root_modulus_lower",
        "selected_global_root_modulus_lower",
        "collision_jacobian_modulus_lower",
    )
    minimum_geometric_factor = min(
        float(row[field]) for row in contour_rows for field in geometric_fields
    )
    uniform_h3 = upward_sum(
        [
            float(row["H_event_third_derivative_sup_upper"])
            for row in event_rows
        ]
    )
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
    complete_group_matrix = (
        set(grouped) == expected_group_keys
        and all(
            len(group) == ENERGY_ARC_COUNT * GLOBAL_ARC_COUNT
            and {
                int(row["energy_phase_arc_index"]) for row in group
            }
            == set(range(ENERGY_ARC_COUNT))
            and {
                int(row["global_phase_arc_index"]) for row in group
            }
            == set(range(GLOBAL_ARC_COUNT))
            for group in grouped.values()
        )
    )
    validations = {
        "all_required_sources_exist": all(
            path.is_file()
            for path in (
                rows_path,
                complete_path,
                BASE_BOXES,
                HALO_BOXES,
                HALO_RESULT,
                ENDPOINT_COEFFICIENTS,
                ENDPOINT_RESULT,
                SUBTRACTION_ZERO_RESULT,
                INTEGRAND_RESULT,
            )
        ),
        "run_complete_marker_passes": complete.get("all_rows_pass") is True,
        "box_matrix_contains_64_base_and_16_halo_boxes": len(base_boxes) == 64
        and len(halo_boxes) == 16
        and len(box_keys) == 80,
        "checkpoint_5386_integrand_certificate_passes": integrand_result.get(
            "validation_passed"
        )
        is True
        and Path(integrand_result["source_run_directory"]).resolve()
        == run_dir.resolve(),
        "arc_counts_match_certified_matrix": energy_arc_counts
        == {ENERGY_ARC_COUNT}
        and global_arc_counts == {GLOBAL_ARC_COUNT},
        "row_count_matches_full_core_plus_halo_matrix": len(contour_rows)
        == expected_rows,
        "contour_row_keys_are_unique": len(contour_keys)
        == len(set(contour_keys)),
        "every_box_has_complete_arc_matrix": complete_group_matrix,
        "all_contour_rows_pass": all_rows_pass,
        "all_geometric_factors_exclude_zero": minimum_geometric_factor > 0
        and math.isfinite(minimum_geometric_factor),
        "endpoint_halo_certificate_passes": halo_result.get(
            "validation_passed"
        )
        is True,
        "endpoint_coefficient_source_passes": endpoint_result.get(
            "validation_passed"
        )
        is True,
        "physical_multiplier_is_positive_finite": physical_multiplier > 0
        and math.isfinite(physical_multiplier),
        "subtraction_double_pole_coefficient_is_certified_zero": (
            subtraction_zero_result.get("validation_passed") is True
            and subtraction_zero_result.get(
                "subtraction_selected_global_pole_order_upper"
            )
            == 1
            and subtraction_zero_result.get(
                "subtraction_double_pole_coefficient"
            )
            == 0
        ),
        "Cauchy_disks_are_covered": coverage["covers_all_radius_rho_disks"]
        is True,
        "all_eight_event_bounds_are_finite": len(event_rows) == 8
        and all(
            math.isfinite(float(row["H_event_third_derivative_sup_upper"]))
            for row in event_rows
        ),
    }
    validation_passed = all(validations.values())
    for row in event_rows:
        row["valid_for_D4_numeric_H3_bound"] = validation_passed
    validation_rows = [
        {
            "gate": gate,
            "passed": passed,
            "detail": json.dumps(
                coverage if gate == "Cauchy_disks_are_covered" else passed,
                sort_keys=True,
            ),
        }
        for gate, passed in validations.items()
    ]
    result = {
        "checkpoint": 5388,
        "updated_utc": datetime.now(timezone.utc).isoformat(),
        "runtime_seconds": time.perf_counter() - started,
        "source_run_directory": str(run_dir.resolve()),
        "contour_row_count": len(contour_rows),
        "expected_contour_row_count": expected_rows,
        "Cauchy_radius": CAUCHY_RADIUS,
        "Cauchy_coverage": coverage,
        "physical_multiplier_upper": physical_multiplier,
        "subtraction_double_pole_coefficient": 0,
        "minimum_geometric_factor_lower": minimum_geometric_factor,
        "uniform_H3_upper": uniform_h3,
        "H_sector_Taylor_constant_upper": upward_quotient(uniform_h3, 6.0),
        "validation_passed": validation_passed,
        "validation": validations,
        "decision": (
            "UNIFORM_H3_CAUCHY_BOUND_CERTIFIED__PROCEED_TO_G3_AND_W3"
            if validation_passed
            else "UNIFORM_H3_CAUCHY_BOUND_BLOCKED"
        ),
        "claim_boundary": {
            "valid_for_D4_nested_contour_integrand_enclosure": validation_passed,
            "valid_for_D4_finite_plus_double_pole_coefficient_enclosure": validation_passed,
            "valid_for_D4_numeric_H3_bound": validation_passed,
            "valid_for_D4_numeric_uniform_remainder_bound": False,
            "valid_for_D4_outer_regulator_zero_limit": False,
            "valid_for_decay_angle_integral": False,
            "valid_for_full_angular_convergence": False,
            "valid_for_full_phase_space_coefficient": False,
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
        },
    }
    output.mkdir(parents=True, exist_ok=True)
    atomic_csv(output / "D4_uniform_H3_event_bounds.csv", event_rows)
    atomic_csv(output / "D4_uniform_H3_validation.csv", validation_rows)
    atomic_json(output / "D4_uniform_H3_result.json", result)
    atomic_json(
        output / "status.json",
        {
            "state": "complete" if validation_passed else "blocked",
            "updated_utc": result["updated_utc"],
            "decision": result["decision"],
        },
    )
    render_document(result, event_rows)
    return result


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--run-dir", type=Path, required=True)
    parser.add_argument("--output", type=Path, default=OUTPUT)
    arguments = parser.parse_args()
    result = run(arguments.run_dir.resolve(), arguments.output.resolve())
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0 if result["validation_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
