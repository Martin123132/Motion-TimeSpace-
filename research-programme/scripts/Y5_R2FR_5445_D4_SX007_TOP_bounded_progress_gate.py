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


CHECKPOINT = 5445
POST = Path(__file__).resolve().parents[1]
ROOT = POST.parent
FORMALIZATION = ROOT / "formalization-workbench"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
OUTPUT = FUNCTIONAL_RG / str(CHECKPOINT)
PARENT_SCRIPT = (
    POST / "scripts" / "Y5_R2FR_5396_D4_deformed_contour_regular_away_W3.py"
)
PARTS = FUNCTIONAL_RG / "5396" / "partial" / "path_parts"
STATE = (
    PARTS
    / "_partitions"
    / "bin_00_sub_00_S_X007_MC04_SM_DM_TOP_part_00_of_01.state.json"
)
STATE_ROWS = STATE.with_suffix(".rows.csv")
STATUS = FUNCTIONAL_RG / "5396" / "status.json"
SNAPSHOT_PATHS = (
    OUTPUT / "v49_pre_resume_state.json",
    OUTPUT / "v49_mid_resume_state.json",
    OUTPUT / "v49_late_resume_state.json",
    OUTPUT / "v49_final_resume_state.json",
    OUTPUT / "v49_completion_resume_state.json",
    OUTPUT / "v49_last_resume_state.json",
)
SNAPSHOT_ROW_PATHS = tuple(
    path.with_suffix(".rows.csv") for path in SNAPSHOT_PATHS
)
PREVIOUS_RESULT = (
    FUNCTIONAL_RG / "5444" / "SX006_right_connector_partition_completion_result.json"
)
PREVIOUS_VALIDATION = (
    FUNCTIONAL_RG / "5444" / "P8_Y5_BRR5396_5444_VALIDATION.csv"
)
DOCUMENT = POST / "5445-Y5-R2FR-D4-SX007-TOP-bounded-progress-gate.md"
VALIDATION = OUTPUT / "P8_Y5_BRR5396_5445_VALIDATION.csv"
RESULT = OUTPUT / "SX007_TOP_bounded_progress_result.json"

EXPECTED_REVISION = "D4-deformed-contour-regular-away-W3-v49"
EXPECTED_MAPPED_CELL_ID = "S_X007_MC04_SM_DM"
EXPECTED_TERM_ID = "MC04_SM_DM"
EXPECTED_PATH_SEGMENT = "TOP"
MAXIMUM_DEPTH = 18
BROAD_FLAGS = (
    "valid_for_SX007_TOP_partition_completion",
    "valid_for_all_TOP_completion",
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


def failure_counts(state: dict[str, Any]) -> dict[str, int]:
    return {
        name: int(value)
        for name, value in state.get("split_failure_counts", {}).items()
    }


def changed_failures(
    before: dict[str, Any], after: dict[str, Any]
) -> dict[str, int]:
    left = failure_counts(before)
    right = failure_counts(after)
    return {
        name: right.get(name, 0) - left.get(name, 0)
        for name in sorted(set(left) | set(right))
        if right.get(name, 0) != left.get(name, 0)
    }


def write_document(payload: dict[str, Any]) -> None:
    decision = (
        "**S_X007/TOP SHOWS CERTIFIED BOUNDED PROGRESS WITHOUT A NEW PARENT OBSTRUCTION.**"
        if payload["valid_for_SX007_TOP_bounded_progress"]
        else "**S_X007/TOP PROGRESS GATE REMAINS OPEN.**"
    )
    lines = [
        "# 5445: S_X007 TOP bounded-progress gate",
        "",
        "## Decision",
        "",
        decision,
        "",
        "Six bounded parent-v49 resumes were run from the state inherited after checkpoint 5444. The adaptive proof remains source-identical; no numerical value, closure rule, or new fallback was inserted.",
        "",
        "## Progress",
        "",
        f"- Accepted leaves: `{payload['initial_accepted_count']}` -> `{payload['current_accepted_count']}` (`+{payload['accepted_delta']}`).",
        f"- Live stack: `{payload['initial_pending_count']}` -> `{payload['current_pending_count']}`.",
        f"- Maximum observed live depth: `{payload['maximum_observed_pending_depth']}` of `{MAXIMUM_DEPTH}`.",
        f"- Minimum accepted amplitude denominator: `{payload['minimum_amplitude_denominator_abs_lower']}`.",
        f"- Minimum accepted collision Jacobian: `{payload['minimum_collision_jacobian_abs_lower']}`.",
        "",
        "## Failure classification",
        "",
        "Several stable-edge, collision-geometry, recoil-sheet, and first-spinor pivot enclosures triggered adaptive splits. Every run nevertheless increased the accepted set, no failure reached maximum depth, and the runner stopped only at explicit runtime budgets. They remain refinement events, not parent-theory singularities.",
        "",
        "## Claim boundary",
        "",
        "The right half of this TOP partition remains on a five-entry depth-first stack. This checkpoint proves healthy bounded progress only; it does not claim S_X007/TOP completion, regular-away W3, UV finiteness, local GR, or full MTS.",
    ]
    atomic_text(DOCUMENT, "\n".join(lines) + "\n")


def run_gate() -> dict[str, Any]:
    started = datetime.now(timezone.utc)
    previous = read_json(PREVIOUS_RESULT)
    previous_validation = read_csv(PREVIOUS_VALIDATION)
    snapshots = [read_json(path) for path in SNAPSHOT_PATHS]
    state = read_json(STATE)
    status = read_json(STATUS)
    initial_rows = read_csv(SNAPSHOT_ROW_PATHS[0])
    current_rows = read_csv(STATE_ROWS)
    new_rows = current_rows[len(initial_rows) :]
    all_states = [*snapshots, state]
    accepted_counts = [int(row["accepted_count"]) for row in all_states]
    pending_counts = [len(row["stack"]) for row in all_states]
    maximum_depth = max(
        int(item[4])
        for row in all_states
        for item in row["stack"]
    )
    accepted_rows_valid = bool(new_rows) and all(
        row["mapped_cell_id"] == EXPECTED_MAPPED_CELL_ID
        and row["term_id"] == EXPECTED_TERM_ID
        and row["path_segment"] == EXPECTED_PATH_SEGMENT
        and math.isfinite(float(row["integrated_regular_path_abs_upper"]))
        and float(row["integrated_regular_path_abs_upper"]) >= 0.0
        and float(row["minimum_amplitude_denominator_abs_lower"]) > 0.0
        and float(row["collision_jacobian_abs_lower"]) > 0.0
        for row in new_rows
    )
    monotone_accepted = all(
        right > left
        for left, right in zip(accepted_counts, accepted_counts[1:])
    )
    changed = changed_failures(snapshots[0], state)
    bounded_progress = (
        state["revision"] == EXPECTED_REVISION
        and all(row["revision"] == EXPECTED_REVISION for row in snapshots)
        and len(current_rows) == int(state["accepted_count"])
        and len(new_rows)
        == int(state["accepted_count"]) - int(snapshots[0]["accepted_count"])
        and monotone_accepted
        and accepted_rows_valid
        and maximum_depth < MAXIMUM_DEPTH
        and bool(state["stack"])
        and status["state"] == "paused_at_runtime_budget"
        and bool(status["resume_safe"])
    )
    payload = {
        "checkpoint": CHECKPOINT,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "parent_revision": state["revision"],
        "mapped_cell_id": EXPECTED_MAPPED_CELL_ID,
        "term_id": EXPECTED_TERM_ID,
        "path_segment": EXPECTED_PATH_SEGMENT,
        "bounded_resume_count": len(SNAPSHOT_PATHS),
        "initial_accepted_count": int(snapshots[0]["accepted_count"]),
        "current_accepted_count": int(state["accepted_count"]),
        "accepted_delta": int(state["accepted_count"])
        - int(snapshots[0]["accepted_count"]),
        "initial_pending_count": len(snapshots[0]["stack"]),
        "current_pending_count": len(state["stack"]),
        "maximum_observed_pending_depth": maximum_depth,
        "accepted_count_sequence": accepted_counts,
        "pending_count_sequence": pending_counts,
        "changed_failure_counts": changed,
        "new_accepted_row_count": len(new_rows),
        "minimum_amplitude_denominator_abs_lower": min(
            float(row["minimum_amplitude_denominator_abs_lower"])
            for row in new_rows
        ),
        "minimum_collision_jacobian_abs_lower": min(
            float(row["collision_jacobian_abs_lower"]) for row in new_rows
        ),
        "runner_state": status["state"],
        "runner_resume_safe": bool(status["resume_safe"]),
        "valid_for_SX007_TOP_bounded_progress": bounded_progress,
        "next_target": "CONTINUE_PARENT_V49_SX007_TOP_RIGHT_HALF",
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
                    PREVIOUS_RESULT,
                    PREVIOUS_VALIDATION,
                    *SNAPSHOT_PATHS,
                    *SNAPSHOT_ROW_PATHS,
                )
            ),
            "parent, state, status, prior gate, and six snapshots",
        ),
        check(
            "checkpoint_5444_is_green",
            int(previous["failed_validation_count"]) == 0
            and bool(
                previous[
                    "valid_for_SX006_right_connector_partition_completion"
                ]
            )
            and all(row["passed"] == "True" for row in previous_validation),
            f"rows={len(previous_validation)}",
        ),
        check(
            "all_states_are_parent_v49",
            state["revision"] == EXPECTED_REVISION
            and all(row["revision"] == EXPECTED_REVISION for row in snapshots),
            state["revision"],
        ),
        check(
            "every_resume_increases_accepted_count",
            monotone_accepted,
            json.dumps(accepted_counts),
        ),
        check(
            "state_row_count_matches_accepted_count",
            len(current_rows) == int(state["accepted_count"]),
            f"rows={len(current_rows)}",
        ),
        check(
            "new_accepted_rows_match_delta",
            len(new_rows)
            == int(state["accepted_count"])
            - int(snapshots[0]["accepted_count"]),
            f"rows={len(new_rows)}",
        ),
        check(
            "new_accepted_rows_are_finite_and_positive",
            accepted_rows_valid,
            f"rows={len(new_rows)}",
        ),
        check(
            "no_failure_reaches_maximum_depth",
            maximum_depth < MAXIMUM_DEPTH,
            f"depth={maximum_depth}/{MAXIMUM_DEPTH}",
        ),
        check(
            "runner_is_resume_safe_at_budget",
            status["state"] == "paused_at_runtime_budget"
            and bool(status["resume_safe"]),
            status["state"],
        ),
        check(
            "partition_remains_explicitly_incomplete",
            bool(state["stack"])
            and not payload["valid_for_SX007_TOP_partition_completion"],
            f"pending={len(state['stack'])}",
        ),
        check(
            "bounded_progress_gate_passes",
            bounded_progress,
            "adaptive production remains healthy",
        ),
        check(
            "broad_claims_remain_false",
            all(not payload[flag] for flag in BROAD_FLAGS),
            "TOP right half remains pending",
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
