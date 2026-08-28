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
SCRIPTS = POST / "scripts"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
RESIDUALS = POST / "source-intake" / "mts_residuals"
OUTPUT = FUNCTIONAL_RG / "5390"
DOCUMENT = POST / "5390-Y5-R2FR-D4-reserved-outer-C0-contour-enclosure.md"
VALIDATION = RESIDUALS / "P8_Y5_BRR545_5390_VALIDATION.csv"

BASE_BOXES = FUNCTIONAL_RG / "5380" / "D4_complexified_event_neighborhood_boxes.csv"
HALO_BOXES = FUNCTIONAL_RG / "5387" / "D4_Cauchy_endpoint_halo_boxes.csv"
INTEGRAND_SCRIPT = SCRIPTS / "Y5_R2FR_5386_D4_nested_contour_integrand_enclosure.py"
RUNNER_SCRIPT = SCRIPTS / "Y5_R2FR_5390_D4_reserved_outer_C0_contour_runner.py"
CERTIFICATE_SCRIPT = Path(__file__).resolve()
PRELIMINARY_STOP_MARKER = (
    POST
    / "runs"
    / "20260820-5390-reserved-outer-C0-full-v1"
    / "PRELIMINARY_STOPPED.json"
)

CHECKPOINT = 5390
MARKER = "MTS_5390_D4_RESERVED_OUTER_C0_CONTOUR_ENCLOSURE"
REVISION = "D4-reserved-outer-C0-contour-enclosure-v2-physical-center-witness"
EVENT_IDS = tuple(f"E{index:02d}" for index in range(1, 9))
ENERGY_ARC_COUNT = 32
GLOBAL_ARC_COUNT = 1
STATE_BOX_CONTRACTION_LIMIT = 0
POINT_WITNESS_MODE = "physical_event_center_solution"

CLAIM_C0 = "valid_for_D4_reserved_outer_C0_contour_enclosure"
OPEN_CLAIMS = (
    "valid_for_D4_full_H_event_enclosure",
    "valid_for_D4_numeric_H3_bound",
    "valid_for_D4_numeric_uniform_remainder_bound",
    "valid_for_D4_outer_regulator_zero_limit",
    "valid_for_local_GR_claim",
    "valid_for_full_MTS_claim",
)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


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


def render_document(result: dict[str, Any], events: list[dict[str, Any]]) -> None:
    lines = [
        "# 5390 — D4 reserved-outer C0 contour enclosure",
        "",
        "## Decision",
        "",
        f"`{result['decision']}`",
        "",
        "## Certified matrix",
        "",
        f"- contour cells: `{result['contour_row_count']}`;",
        f"- complex regulator boxes: `{result['complex_regulator_box_count']}`;",
        f"- state-box contraction limit: `{result['state_box_contraction_limit']}`;",
        f"- maximum unscaled C0 integrand enclosure: `{result['maximum_event_integrand_abs_upper_without_physical_multiplier']}`;",
        f"- minimum denominator clearance: `{result['minimum_denominator_lower']}`;",
        f"- minimum collision-Jacobian clearance: `{result['minimum_collision_jacobian_lower']}`.",
        "",
        "| event | rows | max C0 integrand | min denominator | min Jacobian |",
        "|---|---:|---:|---:|---:|",
    ]
    for row in events:
        lines.append(
            f"| {row['event_id']} | {row['row_count']} | {row['maximum_event_integrand_abs_upper_without_physical_multiplier']} | {row['minimum_denominator_lower']} | {row['minimum_collision_jacobian_lower']} |"
        )
    lines.extend(
        [
            "",
            "## Why this second enclosure exists",
            "",
            "Checkpoint 5386 contracts each certified event box for a tight C0 bound. That is useful for C0 itself but consumes the strict Krawczyk margin needed for a soft-coordinate Cauchy disk. This run deliberately evaluates the identical contour formula on the uncontracted, already-certified 5380 image. Its first additional strict Krawczyk image is held in reserve by checkpoint 5389.",
            "",
            "Every row records contraction limit zero and exactly one sentinel call that stops before the first additional contraction. The independent parent-code witness is evaluated at the physical event-center solution, not at the generally off-shell midpoint of the broad outer state box. Every such physical witness lies inside its input box and its parent value lies inside the nested interval enclosure; all contour denominators remain separated from zero.",
            "",
            "This witness choice is substantive: a preliminary run rejected ten `E01` endpoint-halo arcs because the uncontracted box midpoint does not satisfy the event equations. Re-evaluating those same arcs at the enclosed physical center made all ten pass without changing any contour interval, denominator clearance, or C0 upper bound. The failed preliminary run is retained under `runs/` as an audit artifact and is not a claim source.",
            "",
            "## Scope",
            "",
            "This certifies the reserved-outer C0 enclosure required by the 5389 coordinate-Cauchy bridge. It does not alone claim full H, H3, the total uniform remainder, the D4 outer limit, local GR, or full MTS.",
            "",
        ]
    )
    temporary = DOCUMENT.with_suffix(DOCUMENT.suffix + ".tmp")
    temporary.write_text("\n".join(lines), encoding="utf-8")
    os.replace(temporary, DOCUMENT)


def run(run_dir: Path, output: Path) -> dict[str, Any]:
    run_dir = run_dir.resolve()
    rows_path = run_dir / "rows.jsonl"
    complete_path = run_dir / "COMPLETE.json"
    sources = (
        rows_path,
        complete_path,
        BASE_BOXES,
        HALO_BOXES,
        INTEGRAND_SCRIPT,
        RUNNER_SCRIPT,
        CERTIFICATE_SCRIPT,
        PRELIMINARY_STOP_MARKER,
    )
    missing = [str(path) for path in sources if not path.is_file()]
    if missing:
        raise FileNotFoundError(missing)
    rows = read_jsonl(rows_path)
    complete = json.loads(complete_path.read_text(encoding="utf-8"))
    preliminary = json.loads(
        PRELIMINARY_STOP_MARKER.read_text(encoding="utf-8")
    )
    boxes = [*read_csv(BASE_BOXES), *read_csv(HALO_BOXES)]
    box_keys = {
        (row["event_id"], int(row["epsilon_bin_index"])) for row in boxes
    }
    expected_keys = {
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
    validations = [
        {
            "gate": "all_required_sources_exist",
            "passed": not missing,
            "detail": len(sources),
        },
        {
            "gate": "run_complete_marker_passes_with_zero_contraction_limit",
            "passed": complete.get("all_rows_pass") is True
            and complete.get("state_box_contraction_limit")
            == STATE_BOX_CONTRACTION_LIMIT
            and complete.get("point_witness_mode") == POINT_WITNESS_MODE,
            "detail": json.dumps(complete, sort_keys=True),
        },
        {
            "gate": "preliminary_off_shell_midpoint_run_is_retained_as_nonclaim_audit_only",
            "passed": preliminary.get("state")
            == "stopped_after_root_cause_reproduction"
            and preliminary.get("failure_count") == 10
            and preliminary.get("interval_or_denominator_failure") is False
            and preliminary.get("valid_for_claim") is False,
            "detail": json.dumps(preliminary, sort_keys=True),
        },
        {
            "gate": "matrix_contains_64_base_and_16_halo_boxes",
            "passed": len(boxes) == 80 and len(box_keys) == 80,
            "detail": len(box_keys),
        },
        {
            "gate": "row_keys_match_unique_80_box_32_arc_matrix",
            "passed": len(row_keys) == len(set(row_keys))
            and set(row_keys) == expected_keys,
            "detail": f"rows={len(rows)};expected={len(expected_keys)}",
        },
        {
            "gate": "every_row_uses_reserved_outer_state_box",
            "passed": all(
                int(row["state_box_contraction_limit"])
                == STATE_BOX_CONTRACTION_LIMIT
                and int(row["contraction_sentinel_calls"]) == 1
                and row["row_origin"]
                == "5389_reserved_outer_state_box_physical_center_witness_full_contour_evaluation"
                for row in rows
            ),
            "detail": len(rows),
        },
        {
            "gate": "every_parent_cross_check_uses_the_physical_event_center_inside_the_outer_box",
            "passed": all(
                row.get("point_witness_mode") == POINT_WITNESS_MODE
                and row.get("point_witness_is_in_state_boxes") is True
                for row in rows
            ),
            "detail": len(rows),
        },
        {
            "gate": "all_rows_report_success_and_include_parent_point",
            "passed": all(
                row.get("smoke_passes") is True
                and not row.get("error")
                and row.get("parent_value_is_in_nested_interval") is True
                for row in rows
            ),
            "detail": len(rows),
        },
        {
            "gate": "all_denominator_and_geometry_factors_exclude_zero",
            "passed": all(
                finite_positive(row, field)
                for row in rows
                for field in positive_fields
            ),
            "detail": len(rows),
        },
        {
            "gate": "all_C0_integrand_bounds_are_finite",
            "passed": all(
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
            "detail": len(rows),
        },
    ]
    passed = all(parse_bool(row["passed"]) for row in validations)
    event_rows: list[dict[str, Any]] = []
    for event_id in EVENT_IDS:
        selected = [row for row in rows if row["event_id"] == event_id]
        event_rows.append(
            {
                "event_id": event_id,
                "row_count": len(selected),
                "maximum_value_abs_upper": max(
                    float(row["value_abs_upper"]) for row in selected
                ),
                "maximum_event_integrand_abs_upper_without_physical_multiplier": max(
                    float(
                        row[
                            "event_integrand_abs_upper_without_physical_multiplier"
                        ]
                    )
                    for row in selected
                ),
                "minimum_denominator_lower": min(
                    float(row["minimum_denominator_lower"]) for row in selected
                ),
                "minimum_collision_jacobian_lower": min(
                    float(row["collision_jacobian_modulus_lower"])
                    for row in selected
                ),
                CLAIM_C0: passed,
                **{claim: False for claim in OPEN_CLAIMS},
            }
        )
    source_rows = [
        {
            "path": str(path.resolve()),
            "exists": True,
            "sha256": digest(path),
            CLAIM_C0: passed,
            **{claim: False for claim in OPEN_CLAIMS},
        }
        for path in sources
    ]
    result = {
        "checkpoint": CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "validation_passed": passed,
        "decision": (
            "RESERVED_OUTER_C0_CONTOUR_ENCLOSURE_CERTIFIED__APPLY_FULL_H_BRIDGE"
            if passed
            else "RESERVED_OUTER_C0_CONTOUR_ENCLOSURE_BLOCKED"
        ),
        "source_run_directory": str(run_dir),
        "state_box_contraction_limit": STATE_BOX_CONTRACTION_LIMIT,
        "point_witness_mode": POINT_WITNESS_MODE,
        "preliminary_off_shell_witness_audit_marker": str(
            PRELIMINARY_STOP_MARKER.resolve()
        ),
        "complex_regulator_box_count": len(box_keys),
        "contour_row_count": len(rows),
        "expected_contour_row_count": len(expected_keys),
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
        "claim_boundary": {CLAIM_C0: passed, **{claim: False for claim in OPEN_CLAIMS}},
        "remaining_obstruction": "combine this reserved-outer C0 bound with checkpoint 5389's coordinate-Cauchy radii and z0/z1 bounds to enclose full H and H3",
        "formalization_workbench_modified_file_count": 0,
        "updated_utc": datetime.now(timezone.utc).isoformat(),
    }
    output = output.resolve()
    output.mkdir(parents=True, exist_ok=True)
    atomic_csv(output / "D4_reserved_outer_C0_event_bounds.csv", event_rows)
    atomic_csv(output / "D4_reserved_outer_C0_validation.csv", validations)
    atomic_csv(output / "source_register.csv", source_rows)
    atomic_csv(VALIDATION, validations)
    atomic_json(output / "D4_reserved_outer_C0_result.json", result)
    atomic_json(
        output / "status.json",
        {
            "checkpoint": CHECKPOINT,
            "state": "complete" if passed else "blocked",
            "decision": result["decision"],
            "updated_utc": result["updated_utc"],
        },
    )
    render_document(result, event_rows)
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
