from __future__ import annotations

import csv
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
from typing import Any


POST = Path(__file__).resolve().parents[1]
SOURCE = POST / "source-intake" / "functional_rg" / "5396"
OUTPUT = POST / "source-intake" / "functional_rg" / "5402"
PREVIOUS = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5401"
    / "sixth_support_left_top_completion_gate_result.json"
)
PATH_PARTS = SOURCE / "partial" / "path_parts"
STATE = (
    PATH_PARTS
    / "_partitions"
    / "bin_00_sub_00_S_X003_MC04_SP_DM_RIGHT_CONNECTOR_part_00_of_01.state.json"
)
ROWS = STATE.with_suffix(".rows.csv")
STATUS = SOURCE / "status.json"
AUDITED_PATH = "LDLDLDRDLDLDRU"
SCOPE = "S_X003_MC04_SP_DM_RIGHT_CONNECTOR_d14_LDLDLDRDLDLDRU"
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
    required = (PREVIOUS, STATE, ROWS, STATUS, CENTERED, ANGLE)
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError("missing checkpoint input: " + " | ".join(missing))

    previous = read_json(PREVIOUS)
    state = read_json(STATE)
    status = read_json(STATUS)
    centered = read_json(CENTERED)
    angle = read_json(ANGLE)
    production_rows = read_csv(ROWS)
    audited_rows = [
        row for row in production_rows if row["refinement_path"] == AUDITED_PATH
    ]
    audited_margin = (
        float(audited_rows[0]["minimum_amplitude_denominator_abs_lower"])
        if len(audited_rows) == 1
        else 0.0
    )
    angle_schemes = list(angle["schemes"])
    pending_depths = [int(row[4]) for row in state["stack"]]

    validations = [
        check("required_inputs_exist", not missing, f"{len(required)} paths present"),
        check(
            "checkpoint_5401_authorizes_right_connector",
            bool(previous["valid_for_resuming_sixth_right_connector"])
            and previous["valid_for_global_univalence_claim"] is False
            and previous["valid_for_regular_away_W3_claim"] is False,
            "previous gate authorizes only the right-connector continuation",
        ),
        check(
            "right_centered_identity_passes",
            bool(centered["all_identities_passed"])
            and int(centered["row_count"]) == 108
            and float(centered["maximum_centered_to_direct_relative_error"])
            <= 5.0e-12,
            "108 right-connector derivative comparisons pass",
        ),
        check(
            "right_closed_angle_cover_passes",
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
            "all right-connector angle schemes lie in one open half-plane",
        ),
        check(
            "right_audited_leaf_is_committed",
            len(audited_rows) == 1
            and int(audited_rows[0]["refinement_depth"]) == 14
            and audited_margin > 0.0,
            f"stored production margin {audited_margin:.17g}",
        ),
        check(
            "right_frontier_advanced_after_trigger",
            int(state["accepted_count"]) == 34
            and len(state["stack"]) == 12
            and max(pending_depths, default=-1) == 13
            and AUDITED_PATH not in {str(row[5]) for row in state["stack"]},
            "34 accepted, 12 pending, maximum depth 13",
        ),
        check(
            "right_state_is_v40_resume_safe",
            state["revision"] == "D4-deformed-contour-regular-away-W3-v40"
            and bool(status["resume_safe"])
            and int(status["active_internal_path_state_count"]) == 1,
            "one revision-v40 active state remains crash-safe",
        ),
        check(
            "broad_claims_remain_locked",
            int(status["completed_path_jobs"]) == 17,
            "17/240 path jobs complete; atlas-wide claim remains incomplete",
        ),
    ]
    failed = [row for row in validations if not bool(row["passed"])]
    payload = {
        "checkpoint": 5402,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "validation_count": len(validations),
        "failed_validation_count": len(failed),
        "valid_for_continued_sixth_right_connector_production": not failed,
        "valid_for_global_univalence_claim": False,
        "valid_for_regular_away_W3_claim": False,
        "accepted_box_count": int(state["accepted_count"]),
        "pending_box_count": len(state["stack"]),
        "maximum_pending_depth": max(pending_depths, default=-1),
        "audited_leaf_amplitude_denominator_lower": audited_margin,
        "maximum_centered_derivative_relative_error": float(
            centered["maximum_centered_to_direct_relative_error"]
        ),
        "minimum_closed_angle_imaginary_lower": min(
            float(row["minimum_imaginary_lower"]) for row in angle_schemes
        ),
        "provenance_sha256": {
            str(path.relative_to(POST)): sha256(path) for path in required
        },
    }
    atomic_csv(OUTPUT / "P8_Y5_BRR5396_5402_VALIDATION.csv", validations)
    atomic_json(OUTPUT / "sixth_right_depth_trigger_gate_result.json", payload)
    print(json.dumps(payload, indent=2, sort_keys=True))
    if failed:
        raise RuntimeError(
            "checkpoint 5402 validation failed: "
            + " | ".join(str(row["check"]) for row in failed)
        )
    return payload


if __name__ == "__main__":
    run_gate()
