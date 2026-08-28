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
PREVIOUS = POST / "source-intake" / "functional_rg" / "5400"
OUTPUT = POST / "source-intake" / "functional_rg" / "5401"
PATH_PARTS = SOURCE / "partial" / "path_parts"
LEFT = PATH_PARTS / "bin_00_sub_00_S_X003_MC04_SP_DM_LEFT_CONNECTOR.csv"
TOP = PATH_PARTS / "bin_00_sub_00_S_X003_MC04_SP_DM_TOP.csv"
RIGHT_STATE = (
    PATH_PARTS
    / "_partitions"
    / "bin_00_sub_00_S_X003_MC04_SP_DM_RIGHT_CONNECTOR_part_00_of_01.state.json"
)
STATUS = SOURCE / "status.json"
PREVIOUS_GATE = PREVIOUS / "generalized_depth_trigger_audit_gate_result.json"
AUDITED_PATH = "RDRDRDRDRDLDRU"
SCOPE = "S_X003_MC04_SP_DM_LEFT_CONNECTOR_d14_RDRDRDRDRDLDRU"
CENTERED = SOURCE / f"external01_centered_jacobian_{SCOPE}_result.json"
ANGLE = SOURCE / f"external41_frontier_angle_{SCOPE}_audit_result.json"


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
    required = (LEFT, TOP, RIGHT_STATE, STATUS, PREVIOUS_GATE, CENTERED, ANGLE)
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError("missing checkpoint input: " + " | ".join(missing))

    left_rows = read_csv(LEFT)
    top_rows = read_csv(TOP)
    right_state = read_json(RIGHT_STATE)
    status = read_json(STATUS)
    previous = read_json(PREVIOUS_GATE)
    centered = read_json(CENTERED)
    angle = read_json(ANGLE)
    audited_rows = [
        row for row in left_rows if row["refinement_path"] == AUDITED_PATH
    ]
    expected_area = max(float(row["x_upper"]) for row in left_rows) - min(
        float(row["x_lower"]) for row in left_rows
    )
    left_area = sum(float(row["parameter_area"]) for row in left_rows)
    top_area = sum(float(row["parameter_area"]) for row in top_rows)
    angle_schemes = list(angle["schemes"])
    pending_depths = [int(row[4]) for row in right_state["stack"]]
    audited_margin = (
        float(audited_rows[0]["minimum_amplitude_denominator_abs_lower"])
        if len(audited_rows) == 1
        else 0.0
    )

    validations = [
        check("required_inputs_exist", not missing, f"{len(required)} paths present"),
        check(
            "previous_gate_authorizes_continuation_only",
            bool(previous["valid_for_continued_v40_production"])
            and previous["valid_for_global_univalence_claim"] is False
            and previous["valid_for_regular_away_W3_claim"] is False,
            "checkpoint 5400 passed without promoting broad claims",
        ),
        check(
            "second_centered_identity_passes",
            bool(centered["all_identities_passed"])
            and int(centered["row_count"]) == 108
            and float(centered["maximum_centered_to_direct_relative_error"])
            <= 5.0e-12,
            "108 derivative rows satisfy the parent-identity tolerance",
        ),
        check(
            "second_closed_angle_cover_passes",
            angle["selected_scheme"] is not None
            and all(
                bool(row["all_nonzero_half_plane_passed"])
                for row in angle_schemes
            )
            and min(
                float(row["minimum_imaginary_lower"])
                for row in angle_schemes
            )
            > 0.0,
            "all schemes remain in the positive-imaginary half-plane",
        ),
        check(
            "second_audited_leaf_is_committed",
            len(audited_rows) == 1
            and int(audited_rows[0]["refinement_depth"]) == 14
            and audited_margin > 0.0,
            f"stored production margin {audited_margin:.17g}",
        ),
        check(
            "sixth_left_connector_is_complete",
            len(left_rows) == 110
            and math.isclose(left_area, expected_area, rel_tol=1.0e-12, abs_tol=1.0e-12),
            f"110 rows; area {left_area:.17g}; expected {expected_area:.17g}",
        ),
        check(
            "sixth_top_path_is_complete",
            len(top_rows) == 1
            and math.isclose(top_area, expected_area, rel_tol=1.0e-12, abs_tol=1.0e-12),
            f"1 row; area {top_area:.17g}; expected {expected_area:.17g}",
        ),
        check(
            "right_connector_frontier_is_shallow_and_resume_safe",
            right_state["revision"]
            == "D4-deformed-contour-regular-away-W3-v40"
            and int(right_state["accepted_count"]) == 0
            and len(right_state["stack"]) == 4
            and max(pending_depths, default=-1) == 3,
            "right connector starts at 0 accepted, 4 pending, maximum depth 3",
        ),
        check(
            "production_advanced_to_17_paths",
            int(status["completed_path_jobs"]) == 17
            and int(status["active_internal_path_state_count"]) == 1
            and bool(status["resume_safe"]),
            "17/240 paths complete with one crash-safe active state",
        ),
    ]
    failed = [row for row in validations if not bool(row["passed"])]
    payload = {
        "checkpoint": 5401,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "validation_count": len(validations),
        "failed_validation_count": len(failed),
        "valid_for_resuming_sixth_right_connector": not failed,
        "valid_for_global_univalence_claim": False,
        "valid_for_regular_away_W3_claim": False,
        "completed_path_jobs": int(status["completed_path_jobs"]),
        "sixth_left_connector_box_count": len(left_rows),
        "sixth_top_box_count": len(top_rows),
        "right_connector_pending_box_count": len(right_state["stack"]),
        "right_connector_maximum_pending_depth": max(pending_depths, default=-1),
        "second_audited_leaf_amplitude_denominator_lower": audited_margin,
        "second_maximum_centered_derivative_relative_error": float(
            centered["maximum_centered_to_direct_relative_error"]
        ),
        "second_minimum_closed_angle_imaginary_lower": min(
            float(row["minimum_imaginary_lower"]) for row in angle_schemes
        ),
        "provenance_sha256": {
            str(path.relative_to(POST)): sha256(path) for path in required
        },
    }
    atomic_csv(OUTPUT / "P8_Y5_BRR5396_5401_VALIDATION.csv", validations)
    atomic_json(OUTPUT / "sixth_support_left_top_completion_gate_result.json", payload)
    print(json.dumps(payload, indent=2, sort_keys=True))
    if failed:
        raise RuntimeError(
            "checkpoint 5401 validation failed: "
            + " | ".join(str(row["check"]) for row in failed)
        )
    return payload


if __name__ == "__main__":
    run_gate()
