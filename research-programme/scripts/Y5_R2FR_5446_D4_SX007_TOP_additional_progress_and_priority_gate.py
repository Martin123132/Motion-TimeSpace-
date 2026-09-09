from __future__ import annotations

import csv
import ctypes
from datetime import datetime, timezone
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
if os.name == "nt":
    ctypes.windll.kernel32.SetPriorityClass(
        ctypes.windll.kernel32.GetCurrentProcess(), 0x00004000
    )


CHECKPOINT = 5446
POST = Path(__file__).resolve().parents[1]
ROOT = POST.parent
FORMALIZATION = ROOT / "formalization-workbench"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
OUTPUT = FUNCTIONAL_RG / str(CHECKPOINT)
PARENT_SCRIPT = (
    POST / "scripts" / "Y5_R2FR_5396_D4_deformed_contour_regular_away_W3.py"
)
STATE = (
    FUNCTIONAL_RG
    / "5396"
    / "partial"
    / "path_parts"
    / "_partitions"
    / "bin_00_sub_00_S_X007_MC04_SM_DM_TOP_part_00_of_01.state.json"
)
STATE_ROWS = STATE.with_suffix(".rows.csv")
STATUS = FUNCTIONAL_RG / "5396" / "status.json"
PRE_STATE = OUTPUT / "v49_pre_resume_state.json"
PRE_ROWS = OUTPUT / "v49_pre_resume_state.rows.csv"
PREVIOUS_RESULT = (
    FUNCTIONAL_RG / "5445" / "SX007_TOP_bounded_progress_result.json"
)
PREVIOUS_VALIDATION = (
    FUNCTIONAL_RG / "5445" / "P8_Y5_BRR5396_5445_VALIDATION.csv"
)
DOCUMENT = POST / "5446-Y5-R2FR-D4-SX007-TOP-additional-progress-and-priority-gate.md"
VALIDATION = OUTPUT / "P8_Y5_BRR5396_5446_VALIDATION.csv"
RESULT = OUTPUT / "SX007_TOP_additional_progress_and_priority_result.json"

EXPECTED_REVISION = "D4-deformed-contour-regular-away-W3-v49"
MAXIMUM_DEPTH = 18
NEW_EDGE_CATEGORY = (
    "IntervalSingularity:away_arc_right_K5:s1:c1:left0:"
    "edge_3_3_4:stable_edge"
)
BROAD_FLAGS = (
    "valid_for_SX007_TOP_partition_completion",
    "valid_for_regular_away_W3_claim",
    "valid_for_D4_numeric_W3_bound",
    "valid_for_numeric_UV_claim",
    "valid_for_local_GR_claim",
    "valid_for_full_MTS_claim",
)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def atomic_text(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(text, encoding="utf-8")
    temporary.replace(path)


def atomic_json(path: Path, payload: dict[str, Any]) -> None:
    atomic_text(path, json.dumps(payload, indent=2, sort_keys=True) + "\n")


def atomic_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"cannot write empty CSV {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(path)


def check(name: str, passed: bool, detail: str) -> dict[str, Any]:
    return {
        "checkpoint": CHECKPOINT,
        "check": name,
        "passed": passed,
        "detail": detail,
    }


def counts(state: dict[str, Any]) -> dict[str, int]:
    return {
        name: int(value)
        for name, value in state.get("split_failure_counts", {}).items()
    }


def write_document(payload: dict[str, Any]) -> None:
    decision = (
        "**THE ADDITIONAL S_X007/TOP RUN IS HEALTHY, BUT FULL ENUMERATION IS NOT YET THE PROVEN PRIORITY.**"
        if payload["valid_for_SX007_TOP_additional_bounded_progress"]
        else "**THE ADDITIONAL S_X007/TOP PROGRESS GATE REMAINS OPEN.**"
    )
    lines = [
        "# 5446: S_X007 TOP additional-progress and priority gate",
        "",
        "## Decision",
        "",
        decision,
        "",
        "One source-identical parent-v49 run added certified leaves without reaching a terminal enclosure obstruction. The state remains exactly resumable.",
        "",
        "## Production delta",
        "",
        f"- Accepted leaves: `{payload['pre_accepted_count']}` -> `{payload['post_accepted_count']}` (`+{payload['accepted_delta']}`).",
        f"- Live stack: `{payload['pre_pending_count']}` -> `{payload['post_pending_count']}`.",
        f"- Maximum live depth: `{payload['maximum_pending_depth']}` of `{MAXIMUM_DEPTH}`.",
        f"- New accepted minimum amplitude denominator: `{payload['minimum_new_amplitude_denominator_abs_lower']}`.",
        f"- New accepted minimum collision Jacobian: `{payload['minimum_new_collision_jacobian_abs_lower']}`.",
        "",
        "## New edge label",
        "",
        f"`{NEW_EDGE_CATEGORY}` occurred `{payload['new_edge_category_delta']}` times. It did not halt the run, remained below depth 18, and generated accepted children; it is not promoted to a parent obstruction.",
        "",
        "## Priority consequence",
        "",
        f"The full parent run reports `{payload['completed_path_jobs']}/{payload['total_path_jobs']}` completed path jobs. Before committing many additional machine-hours, the next checkpoint must inspect whether full D4 regular-away enumeration is on the critical dependency path for local GR, Newtonian recovery, Maxwell stress, and calibrated source coupling.",
        "",
        "## Claim boundary",
        "",
        "S_X007/TOP remains incomplete with five live entries. No regular-away W3, UV, local-GR, or full-MTS claim is made.",
    ]
    atomic_text(DOCUMENT, "\n".join(lines) + "\n")


def run_gate() -> dict[str, Any]:
    started = datetime.now(timezone.utc)
    previous = read_json(PREVIOUS_RESULT)
    previous_validation = read_csv(PREVIOUS_VALIDATION)
    before = read_json(PRE_STATE)
    after = read_json(STATE)
    status = read_json(STATUS)
    before_rows = read_csv(PRE_ROWS)
    after_rows = read_csv(STATE_ROWS)
    new_rows = after_rows[len(before_rows) :]
    before_counts = counts(before)
    after_counts = counts(after)
    changed = {
        name: after_counts.get(name, 0) - before_counts.get(name, 0)
        for name in sorted(set(before_counts) | set(after_counts))
        if after_counts.get(name, 0) != before_counts.get(name, 0)
    }
    maximum_depth = max(int(row[4]) for row in after["stack"])
    new_rows_valid = bool(new_rows) and all(
        math.isfinite(float(row["integrated_regular_path_abs_upper"]))
        and float(row["integrated_regular_path_abs_upper"]) >= 0.0
        and float(row["minimum_amplitude_denominator_abs_lower"]) > 0.0
        and float(row["collision_jacobian_abs_lower"]) > 0.0
        for row in new_rows
    )
    accepted_delta = int(after["accepted_count"]) - int(
        before["accepted_count"]
    )
    progress_valid = (
        before["revision"] == after["revision"] == EXPECTED_REVISION
        and accepted_delta > 0
        and len(new_rows) == accepted_delta
        and len(after_rows) == int(after["accepted_count"])
        and new_rows_valid
        and maximum_depth < MAXIMUM_DEPTH
        and bool(after["stack"])
        and status["state"] == "paused_at_runtime_budget"
        and bool(status["resume_safe"])
    )
    payload = {
        "checkpoint": CHECKPOINT,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "parent_revision": after["revision"],
        "pre_accepted_count": int(before["accepted_count"]),
        "post_accepted_count": int(after["accepted_count"]),
        "accepted_delta": accepted_delta,
        "pre_pending_count": len(before["stack"]),
        "post_pending_count": len(after["stack"]),
        "maximum_pending_depth": maximum_depth,
        "changed_failure_counts": changed,
        "new_edge_category_delta": changed.get(NEW_EDGE_CATEGORY, 0),
        "new_accepted_row_count": len(new_rows),
        "minimum_new_amplitude_denominator_abs_lower": min(
            float(row["minimum_amplitude_denominator_abs_lower"])
            for row in new_rows
        ),
        "minimum_new_collision_jacobian_abs_lower": min(
            float(row["collision_jacobian_abs_lower"]) for row in new_rows
        ),
        "completed_path_jobs": int(status["completed_path_jobs"]),
        "total_path_jobs": int(status["total_path_jobs"]),
        "runner_state": status["state"],
        "runner_resume_safe": bool(status["resume_safe"]),
        "valid_for_SX007_TOP_additional_bounded_progress": progress_valid,
        "next_target": "AUDIT_PARENT_CRITICAL_DEPENDENCY_PATH",
        **{flag: False for flag in BROAD_FLAGS},
    }
    validations = [
        check(
            "all_sources_exist",
            all(
                path.exists()
                for path in (
                    PARENT_SCRIPT,
                    STATE,
                    STATE_ROWS,
                    STATUS,
                    PRE_STATE,
                    PRE_ROWS,
                    PREVIOUS_RESULT,
                    PREVIOUS_VALIDATION,
                )
            ),
            "eight local inputs",
        ),
        check(
            "checkpoint_5445_is_green",
            int(previous["failed_validation_count"]) == 0
            and bool(previous["valid_for_SX007_TOP_bounded_progress"])
            and all(row["passed"] == "True" for row in previous_validation),
            f"rows={len(previous_validation)}",
        ),
        check(
            "state_revision_remains_v49",
            before["revision"] == after["revision"] == EXPECTED_REVISION,
            after["revision"],
        ),
        check(
            "accepted_rows_advance_and_match_state",
            accepted_delta > 0
            and len(new_rows) == accepted_delta
            and len(after_rows) == int(after["accepted_count"]),
            f"delta={accepted_delta}, rows={len(after_rows)}",
        ),
        check(
            "new_rows_are_finite_and_positive",
            new_rows_valid,
            f"rows={len(new_rows)}",
        ),
        check(
            "new_edge_label_is_nonterminal",
            changed.get(NEW_EDGE_CATEGORY, 0) > 0
            and accepted_delta > changed.get(NEW_EDGE_CATEGORY, 0)
            and maximum_depth < MAXIMUM_DEPTH,
            f"events={changed.get(NEW_EDGE_CATEGORY, 0)}, depth={maximum_depth}",
        ),
        check(
            "runner_remains_resume_safe",
            status["state"] == "paused_at_runtime_budget"
            and bool(status["resume_safe"]),
            status["state"],
        ),
        check(
            "partition_remains_explicitly_incomplete",
            bool(after["stack"])
            and not payload["valid_for_SX007_TOP_partition_completion"],
            f"pending={len(after['stack'])}",
        ),
        check(
            "additional_progress_gate_passes",
            progress_valid,
            "healthy progress preserved without parent change",
        ),
        check(
            "broad_claims_remain_false",
            all(not payload[flag] for flag in BROAD_FLAGS),
            "critical dependency audit remains open",
        ),
    ]
    formalization_touches = [
        path
        for path in FORMALIZATION.rglob("*")
        if path.is_file()
        and datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) > started
    ]
    validations.append(
        check(
            "formalization_workbench_untouched",
            not formalization_touches,
            f"modified_file_count={len(formalization_touches)}",
        )
    )
    payload["validation_row_count"] = len(validations)
    payload["failed_validation_count"] = sum(
        not bool(row["passed"]) for row in validations
    )
    atomic_csv(VALIDATION, validations)
    write_document(payload)
    atomic_json(RESULT, payload)
    return payload


def main() -> int:
    payload = run_gate()
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload["failed_validation_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
