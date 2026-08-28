from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import sys
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
OUTPUT = FUNCTIONAL_RG / "5386"
DOCUMENT = POST / "5386-Y5-R2FR-D4-nested-contour-integrand-enclosure.md"
BASE_BOXES = FUNCTIONAL_RG / "5380" / "D4_complexified_event_neighborhood_boxes.csv"
HALO_BOXES = FUNCTIONAL_RG / "5387" / "D4_Cauchy_endpoint_halo_boxes.csv"
INTEGRAND_SCRIPT = (
    POST
    / "scripts"
    / "Y5_R2FR_5386_D4_nested_contour_integrand_enclosure.py"
)
RUNNER_SCRIPT = (
    POST
    / "scripts"
    / "Y5_R2FR_5386_D4_uniform_H3_contour_bound_runner.py"
)
CERTIFICATE_SCRIPT = Path(__file__).resolve()
EVENT_IDS = tuple(f"E{index:02d}" for index in range(1, 9))
ENERGY_ARC_COUNT = 32
GLOBAL_ARC_COUNT = 1


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def read_jsonl(path: Path) -> list[dict[str, Any]]:
    return [
        json.loads(line)
        for line in path.read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]


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


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def row_key(row: dict[str, Any]) -> tuple[Any, ...]:
    return (
        row["event_id"],
        int(row["epsilon_bin_index"]),
        int(row["epsilon_subdivision_index"]),
        int(row["energy_phase_arc_index"]),
        int(row["global_phase_arc_index"]),
    )


def finite_positive(row: dict[str, Any], field: str) -> bool:
    value = float(row[field])
    return value > 0 and math.isfinite(value)


def render_document(
    result: dict[str, Any], event_rows: list[dict[str, Any]]
) -> None:
    lines = [
        "# 5386 — Y5/R2FR D4 nested-contour integrand enclosure",
        "",
        "## Decision",
        "",
        f"`{result['decision']}`",
        "",
        "## Certified matrix",
        "",
        f"- contour cells: `{result['contour_row_count']}`;",
        f"- complex regulator boxes: `{result['complex_regulator_box_count']}`;",
        f"- energy arcs per box: `{result['energy_arc_count']}`;",
        f"- global enclosure arcs per energy arc: `{result['global_arc_count']}`;",
        f"- maximum numerator enclosure: `{result['maximum_value_abs_upper']}`;",
        f"- maximum event-integrand enclosure: `{result['maximum_event_integrand_abs_upper_without_physical_multiplier']}`;",
        f"- minimum recorded denominator clearance: `{result['minimum_denominator_lower']}`;",
        f"- minimum collision-Jacobian clearance: `{result['minimum_collision_jacobian_lower']}`.",
        "",
        "| event | rows | max integrand | min denominator | min Jacobian |",
        "|---|---:|---:|---:|---:|",
    ]
    for row in event_rows:
        lines.append(
            f"| {row['event_id']} | {row['row_count']} | "
            f"{row['maximum_event_integrand_abs_upper_without_physical_multiplier']} | "
            f"{row['minimum_denominator_lower']} | "
            f"{row['minimum_collision_jacobian_lower']} |"
        )
    lines.extend(
        [
            "",
            "## Exact chart repair",
            "",
            "The branch-death hard leg uses its exact energy-channel diagonal p1(active) = -DeltaE Q/2. The soft leg is put in a rational light-cone chart. The right cut spinors are i times the left spinors, so their bispinors are exactly the negated cut momenta.",
            "",
            "Edges that retain a default square-root spinor are transformed by the exact little-group factor. For the representative chart a1 = i p1_perp-minus/sqrt(-p1-plus); for the reciprocal chart a1 = i p1_perp-plus/sqrt(-p1-minus). The reciprocal first-soft square edge is desingularized by the algebraic identity -(1+q). No chart-only zero is treated as a physical pole.",
            "",
            "The collision Jacobian is enclosed by a centered mixed-derivative mean-value formula along the recoil path. Every final row also contains the independently evaluated parent point inside the nested complex interval.",
            "",
            "## Scope",
            "",
            "This certificate establishes a finite enclosure of the H-sector nested-contour integrand on the stated complex regulator neighborhood. It does not by itself establish H3, G3, W3, the complete uniform remainder, the D4 outer limit, local GR, or full MTS.",
            "",
        ]
    )
    temporary = DOCUMENT.with_suffix(DOCUMENT.suffix + ".tmp")
    temporary.write_text("\n".join(lines), encoding="utf-8")
    os.replace(temporary, DOCUMENT)


def run(run_dir: Path, output: Path) -> dict[str, Any]:
    rows_path = run_dir / "rows.jsonl"
    complete_path = run_dir / "COMPLETE.json"
    source_paths = (
        rows_path,
        complete_path,
        BASE_BOXES,
        HALO_BOXES,
        INTEGRAND_SCRIPT,
        RUNNER_SCRIPT,
        CERTIFICATE_SCRIPT,
    )
    missing_sources = [str(path) for path in source_paths if not path.is_file()]
    if missing_sources:
        raise FileNotFoundError("missing certificate sources: " + " | ".join(missing_sources))
    rows = read_jsonl(rows_path)
    complete = json.loads(complete_path.read_text(encoding="utf-8"))
    boxes = [*read_csv(BASE_BOXES), *read_csv(HALO_BOXES)]
    box_keys = {
        (row["event_id"], int(row["epsilon_bin_index"])) for row in boxes
    }
    expected_row_keys = {
        (event_id, epsilon_bin, 0, energy_arc, global_arc)
        for event_id, epsilon_bin in box_keys
        for energy_arc in range(ENERGY_ARC_COUNT)
        for global_arc in range(GLOBAL_ARC_COUNT)
    }
    row_keys = [row_key(row) for row in rows]
    positive_fields = (
        "minimum_denominator_lower",
        "energy_channel_quotient_abs_lower",
        "left_active_invariant_abs_lower",
        "relative_root_modulus_lower",
        "selected_global_root_modulus_lower",
        "collision_jacobian_modulus_lower",
    )
    validations = {
        "all_required_sources_exist": not missing_sources,
        "run_complete_marker_passes": complete.get("all_rows_pass") is True,
        "box_matrix_contains_64_base_and_16_halo_boxes": len(boxes) == 80
        and len(box_keys) == 80,
        "row_count_matches_80_box_32_arc_matrix": len(rows)
        == len(expected_row_keys),
        "row_keys_are_unique": len(row_keys) == len(set(row_keys)),
        "row_keys_match_required_matrix": set(row_keys) == expected_row_keys,
        "all_rows_report_success": all(
            row.get("smoke_passes") is True and not row.get("error")
            for row in rows
        ),
        "all_parent_points_are_included": all(
            row.get("parent_value_is_in_nested_interval") is True
            for row in rows
        ),
        "all_denominator_and_geometry_factors_exclude_zero": all(
            finite_positive(row, field)
            for row in rows
            for field in positive_fields
        ),
        "all_numerator_and_integrand_bounds_are_finite": all(
            math.isfinite(float(row["value_abs_upper"]))
            and math.isfinite(
                float(
                    row[
                        "event_integrand_abs_upper_without_physical_multiplier"
                    ]
                )
            )
            for row in rows
        ),
    }
    validation_passed = all(validations.values())
    event_rows: list[dict[str, Any]] = []
    for event_id in EVENT_IDS:
        event = [row for row in rows if row["event_id"] == event_id]
        event_rows.append(
            {
                "event_id": event_id,
                "row_count": len(event),
                "maximum_value_abs_upper": max(
                    float(row["value_abs_upper"]) for row in event
                ),
                "maximum_event_integrand_abs_upper_without_physical_multiplier": max(
                    float(
                        row[
                            "event_integrand_abs_upper_without_physical_multiplier"
                        ]
                    )
                    for row in event
                ),
                "minimum_denominator_lower": min(
                    float(row["minimum_denominator_lower"]) for row in event
                ),
                "minimum_relative_root_lower": min(
                    float(row["relative_root_modulus_lower"]) for row in event
                ),
                "minimum_selected_global_root_lower": min(
                    float(row["selected_global_root_modulus_lower"])
                    for row in event
                ),
                "minimum_collision_jacobian_lower": min(
                    float(row["collision_jacobian_modulus_lower"])
                    for row in event
                ),
                "valid_for_D4_nested_contour_integrand_enclosure": validation_passed,
                "valid_for_D4_numeric_H3_bound": False,
                "valid_for_D4_numeric_uniform_remainder_bound": False,
                "valid_for_D4_outer_regulator_zero_limit": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    validation_rows = [
        {"gate": gate, "passed": passed, "detail": str(passed)}
        for gate, passed in validations.items()
    ]
    source_rows = [
        {
            "path": str(path.resolve()),
            "sha256": sha256_file(path),
            "exists": True,
        }
        for path in source_paths
    ]
    result = {
        "checkpoint": 5386,
        "updated_utc": datetime.now(timezone.utc).isoformat(),
        "source_run_directory": str(run_dir.resolve()),
        "complex_regulator_box_count": len(box_keys),
        "contour_row_count": len(rows),
        "expected_contour_row_count": len(expected_row_keys),
        "energy_arc_count": ENERGY_ARC_COUNT,
        "global_arc_count": GLOBAL_ARC_COUNT,
        "maximum_value_abs_upper": max(
            float(row["value_abs_upper"]) for row in rows
        ),
        "maximum_event_integrand_abs_upper_without_physical_multiplier": max(
            float(
                row["event_integrand_abs_upper_without_physical_multiplier"]
            )
            for row in rows
        ),
        "minimum_denominator_lower": min(
            float(row["minimum_denominator_lower"]) for row in rows
        ),
        "minimum_collision_jacobian_lower": min(
            float(row["collision_jacobian_modulus_lower"]) for row in rows
        ),
        "validation_passed": validation_passed,
        "validation": validations,
        "decision": (
            "NESTED_CONTOUR_INTEGRAND_ENCLOSURE_CERTIFIED__PROCEED_TO_H3"
            if validation_passed
            else "NESTED_CONTOUR_INTEGRAND_ENCLOSURE_BLOCKED"
        ),
        "claim_boundary": {
            "valid_for_D4_nested_contour_integrand_enclosure": validation_passed,
            "valid_for_D4_numeric_H3_bound": False,
            "valid_for_D4_numeric_uniform_remainder_bound": False,
            "valid_for_D4_outer_regulator_zero_limit": False,
            "valid_for_decay_angle_integral": False,
            "valid_for_full_angular_convergence": False,
            "valid_for_full_phase_space_coefficient": False,
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
        },
        "source_files": source_rows,
    }
    output.mkdir(parents=True, exist_ok=True)
    atomic_csv(output / "D4_nested_contour_integrand_event_bounds.csv", event_rows)
    atomic_csv(output / "D4_nested_contour_integrand_validation.csv", validation_rows)
    atomic_csv(output / "D4_nested_contour_integrand_sources.csv", source_rows)
    atomic_json(output / "D4_nested_contour_integrand_result.json", result)
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
