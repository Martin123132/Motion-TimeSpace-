from __future__ import annotations

import csv
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
from typing import Any


POST = Path(__file__).resolve().parents[1]
SOURCE = POST / "source-intake" / "functional_rg" / "5396"
OUTPUT = POST / "source-intake" / "functional_rg" / "5407"
PREVIOUS = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5406"
    / "sixth_right_adjacent_depth_trigger_gate_result.json"
)
PATH_PARTS = SOURCE / "partial" / "path_parts"
STATUS = SOURCE / "status.json"
COMPLETED_SPECS = (
    ("S_X003_MC04_SP_DM_RIGHT_CONNECTOR", 382, 0.0176739667451603),
    ("S_X004_MC04_SM_DM_LEFT_CONNECTOR", 1, 0.0073217090523498),
    ("S_X004_MC04_SM_DM_TOP", 4, 0.0073217090523498),
    ("S_X004_MC04_SM_DM_RIGHT_CONNECTOR", 1, 0.0073217090523498),
    ("S_X005_MC04_SM_DM_LEFT_CONNECTOR", 1, 0.01522842174025956),
    ("S_X005_MC04_SM_DM_TOP", 11, 0.01522842174025956),
    ("S_X005_MC04_SM_DM_RIGHT_CONNECTOR", 2, 0.01522842174025956),
    ("S_X006_MC04_SM_DM_LEFT_CONNECTOR", 4, 0.03932753620548854),
)
COMPLETED = tuple(
    PATH_PARTS / f"bin_00_sub_00_{name}.csv" for name, _, _ in COMPLETED_SPECS
)
ACTIVE_STATE = (
    PATH_PARTS
    / "_partitions"
    / "bin_00_sub_00_S_X006_MC04_SM_DM_TOP_part_00_of_01.state.json"
)
ACTIVE_ROWS = ACTIVE_STATE.with_suffix(".rows.csv")
ACTIVE_EXPECTED_AREA = 0.03932753620548854
AUDITED_RIGHT_PATHS = {
    "LDLDLDRDLDLDRU",
    "RDLDRDRDLDLDRU",
    "RDRDLDRDLDLDRU",
    "RDRDRDRDLDRDRD",
    "RDRDRDRDLDRDRU",
}


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def atomic_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(text, encoding="utf-8")
    temporary.replace(path)


def atomic_json(path: Path, payload: dict[str, Any]) -> None:
    atomic_text(path, json.dumps(payload, indent=2, sort_keys=True) + "\n")


def atomic_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(path)


def check(name: str, passed: bool, evidence: str) -> dict[str, Any]:
    return {"check": name, "passed": passed, "evidence": evidence}


def run_gate() -> dict[str, Any]:
    required = (PREVIOUS, STATUS, *COMPLETED, ACTIVE_STATE, ACTIVE_ROWS)
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError("missing checkpoint input: " + " | ".join(missing))

    previous = read_json(PREVIOUS)
    status = read_json(STATUS)
    completed_rows = [read_csv(path) for path in COMPLETED]
    active_state = read_json(ACTIVE_STATE)
    active_rows = read_csv(ACTIVE_ROWS)
    completed_checks = []
    completed_summaries = []
    for (name, expected_count, expected_area), rows in zip(
        COMPLETED_SPECS, completed_rows
    ):
        area = sum(float(row["parameter_area"]) for row in rows)
        minimum_margin = min(
            float(row["minimum_amplitude_denominator_abs_lower"]) for row in rows
        )
        passed = (
            len(rows) == expected_count
            and math.isclose(area, expected_area, rel_tol=1.0e-12, abs_tol=1.0e-12)
            and minimum_margin > 0.0
            and all(
                row["valid_for_D4_numeric_regular_away_W3_bound"] == "True"
                for row in rows
            )
        )
        completed_checks.append(passed)
        completed_summaries.append(
            {
                "path_job": name,
                "box_count": len(rows),
                "parameter_area": area,
                "minimum_amplitude_denominator_abs_lower": minimum_margin,
                "maximum_refinement_depth": max(
                    int(row["refinement_depth"]) for row in rows
                ),
            }
        )

    right_rows = completed_rows[0]
    right_paths = {row["refinement_path"] for row in right_rows}
    pending_depths = [int(row[4]) for row in active_state["stack"]]
    active_accepted_area = sum(float(row["parameter_area"]) for row in active_rows)
    active_pending_area = sum(
        (float(row[1]) - float(row[0])) * (float(row[3]) - float(row[2]))
        for row in active_state["stack"]
    )
    active_total_area = active_accepted_area + active_pending_area
    active_coverage_fraction = active_accepted_area / active_total_area

    validations = [
        check("required_inputs_exist", not missing, f"{len(required)} paths present"),
        check(
            "checkpoint_5406_authorizes_continuation",
            bool(previous["valid_for_continued_sixth_right_connector_production"])
            and previous["valid_for_global_univalence_claim"] is False
            and previous["valid_for_regular_away_W3_claim"] is False,
            "previous gate authorizes continued production only",
        ),
        check(
            "sixth_right_connector_is_complete",
            completed_checks[0]
            and AUDITED_RIGHT_PATHS.issubset(right_paths),
            "382 certified boxes cover the complete connector and retain all audited leaves",
        ),
        check(
            "x004_three_paths_are_complete",
            all(completed_checks[1:4]),
            "X004 SM left/top/right paths are finite and area-complete",
        ),
        check(
            "x005_three_paths_are_complete",
            all(completed_checks[4:7]),
            "X005 SM left/top/right paths are finite and area-complete",
        ),
        check(
            "x006_left_path_is_complete",
            completed_checks[7],
            "X006 SM left connector is finite and area-complete",
        ),
        check(
            "x006_top_active_partition_is_complete",
            len(active_rows) == 25
            and int(active_state["accepted_count"]) == len(active_rows)
            and len(active_state["stack"]) == 4
            and max(pending_depths, default=-1) == 6
            and math.isclose(
                active_total_area,
                ACTIVE_EXPECTED_AREA,
                rel_tol=1.0e-12,
                abs_tol=1.0e-12,
            )
            and all(
                float(row["minimum_amplitude_denominator_abs_lower"]) > 0.0
                for row in active_rows
            ),
            "25 accepted plus 4 pending boxes partition the complete X006 top rectangle",
        ),
        check(
            "production_advanced_eight_path_jobs",
            int(status["completed_path_jobs"]) == 25
            and int(status["total_path_jobs"]) == 240,
            "production advances 17/240 -> 25/240 completed path jobs",
        ),
        check(
            "state_is_v40_resume_safe",
            active_state["revision"] == "D4-deformed-contour-regular-away-W3-v40"
            and bool(status["resume_safe"])
            and int(status["active_internal_path_state_count"]) == 1,
            "one shallow crash-safe v40 active state remains",
        ),
    ]
    failed = [row for row in validations if not bool(row["passed"])]
    payload = {
        "checkpoint": 5407,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "validation_count": len(validations),
        "failed_validation_count": len(failed),
        "valid_for_continued_v40_production": not failed,
        "valid_for_global_univalence_claim": False,
        "valid_for_regular_away_W3_claim": False,
        "completed_path_jobs": int(status["completed_path_jobs"]),
        "newly_frozen_path_job_count": len(COMPLETED_SPECS),
        "completed_path_summaries": completed_summaries,
        "active_mapped_path_job": "S_X006_MC04_SM_DM_TOP",
        "active_accepted_box_count": len(active_rows),
        "active_pending_box_count": len(active_state["stack"]),
        "active_maximum_pending_depth": max(pending_depths, default=-1),
        "active_coverage_fraction": active_coverage_fraction,
        "provenance_sha256": {
            str(path.relative_to(POST)): sha256(path) for path in required
        },
    }
    atomic_csv(OUTPUT / "P8_Y5_BRR5396_5407_VALIDATION.csv", validations)
    atomic_json(
        OUTPUT / "sixth_right_and_next_supports_completion_gate_result.json",
        payload,
    )
    print(json.dumps(payload, indent=2, sort_keys=True))
    if failed:
        raise RuntimeError(
            "checkpoint 5407 validation failed: "
            + " | ".join(str(row["check"]) for row in failed)
        )
    return payload


if __name__ == "__main__":
    run_gate()
