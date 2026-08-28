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
OUTPUT = POST / "source-intake" / "functional_rg" / "5403"
PREVIOUS = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5402"
    / "sixth_right_depth_trigger_gate_result.json"
)
STATE = (
    SOURCE
    / "partial"
    / "path_parts"
    / "_partitions"
    / "bin_00_sub_00_S_X003_MC04_SP_DM_RIGHT_CONNECTOR_part_00_of_01.state.json"
)
ROWS = STATE.with_suffix(".rows.csv")
STATUS = SOURCE / "status.json"
AUDITED_PATH = "LDLDLDRDLDLDRU"
EXPECTED_AREA = 0.0176739667451603


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
    required = (PREVIOUS, STATE, ROWS, STATUS)
    missing = [str(path) for path in required if not path.exists()]
    if missing:
        raise FileNotFoundError("missing checkpoint input: " + " | ".join(missing))

    previous = read_json(PREVIOUS)
    state = read_json(STATE)
    status = read_json(STATUS)
    rows = read_csv(ROWS)
    pending_depths = [int(row[4]) for row in state["stack"]]
    accepted_area = sum(float(row["parameter_area"]) for row in rows)
    pending_area = sum(
        (float(row[1]) - float(row[0])) * (float(row[3]) - float(row[2]))
        for row in state["stack"]
    )
    total_area = accepted_area + pending_area
    coverage_fraction = accepted_area / total_area
    audited_rows = [row for row in rows if row["refinement_path"] == AUDITED_PATH]

    validations = [
        check("required_inputs_exist", not missing, f"{len(required)} paths present"),
        check(
            "checkpoint_5402_authorizes_continuation",
            bool(previous["valid_for_continued_sixth_right_connector_production"])
            and previous["valid_for_global_univalence_claim"] is False
            and previous["valid_for_regular_away_W3_claim"] is False,
            "previous checkpoint authorizes continuation without broad claims",
        ),
        check(
            "accepted_rows_match_state",
            len(rows) == 164 and int(state["accepted_count"]) == len(rows),
            f"{len(rows)} stored rows and state accepted_count agree",
        ),
        check(
            "parameter_partition_is_complete",
            math.isclose(total_area, EXPECTED_AREA, rel_tol=1.0e-12, abs_tol=1.0e-12),
            f"accepted plus pending area {total_area:.17g}",
        ),
        check(
            "frontier_is_below_audit_trigger",
            len(state["stack"]) == 6
            and max(pending_depths, default=-1) == 8,
            "6 pending boxes; maximum depth 8",
        ),
        check(
            "audited_leaf_remains_committed",
            len(audited_rows) == 1
            and float(audited_rows[0]["minimum_amplitude_denominator_abs_lower"])
            > 0.0,
            "checkpoint-5402 depth-fourteen row remains in production state",
        ),
        check(
            "state_is_v40_resume_safe",
            state["revision"] == "D4-deformed-contour-regular-away-W3-v40"
            and bool(status["resume_safe"])
            and int(status["active_internal_path_state_count"]) == 1,
            "one crash-safe revision-v40 active state",
        ),
        check(
            "atlas_claim_remains_incomplete",
            int(status["completed_path_jobs"]) == 17,
            "17/240 path jobs complete",
        ),
    ]
    failed = [row for row in validations if not bool(row["passed"])]
    payload = {
        "checkpoint": 5403,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "validation_count": len(validations),
        "failed_validation_count": len(failed),
        "valid_for_continued_sixth_right_connector_production": not failed,
        "valid_for_global_univalence_claim": False,
        "valid_for_regular_away_W3_claim": False,
        "accepted_box_count": int(state["accepted_count"]),
        "pending_box_count": len(state["stack"]),
        "maximum_pending_depth": max(pending_depths, default=-1),
        "accepted_parameter_area": accepted_area,
        "pending_parameter_area": pending_area,
        "coverage_fraction": coverage_fraction,
        "provenance_sha256": {
            str(path.relative_to(POST)): sha256(path) for path in required
        },
    }
    atomic_csv(OUTPUT / "P8_Y5_BRR5396_5403_VALIDATION.csv", validations)
    atomic_json(OUTPUT / "sixth_right_bounded_progress_gate_result.json", payload)
    print(json.dumps(payload, indent=2, sort_keys=True))
    if failed:
        raise RuntimeError(
            "checkpoint 5403 validation failed: "
            + " | ".join(str(row["check"]) for row in failed)
        )
    return payload


if __name__ == "__main__":
    run_gate()
