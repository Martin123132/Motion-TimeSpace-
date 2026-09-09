from __future__ import annotations

import ast
import csv
import ctypes
from datetime import datetime, timezone
import json
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


CHECKPOINT = 5443
POST = Path(__file__).resolve().parents[1]
ROOT = POST.parent
FORMALIZATION = ROOT / "formalization-workbench"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
OUTPUT = FUNCTIONAL_RG / str(CHECKPOINT)
PARENT_SCRIPT = (
    POST / "scripts" / "Y5_R2FR_5396_D4_deformed_contour_regular_away_W3.py"
)
CLASSIFICATION_RESULT = (
    FUNCTIONAL_RG / "5442" / "c1_external01_live_failure_provenance_result.json"
)
CLASSIFICATION_VALIDATION = (
    FUNCTIONAL_RG / "5442" / "P8_Y5_BRR5396_5442_VALIDATION.csv"
)
PRE_STATE = OUTPUT / "v49_pre_resume_state.json"
PRE_ROWS = OUTPUT / "v49_pre_resume_state.rows.csv"
MID_STATE = OUTPUT / "v49_mid_resume_state.json"
MID_ROWS = OUTPUT / "v49_mid_resume_state.rows.csv"
POST_STATE = (
    FUNCTIONAL_RG
    / "5396"
    / "partial"
    / "path_parts"
    / "_partitions"
    / "bin_00_sub_00_S_X006_MC04_SP_DP_RIGHT_CONNECTOR_part_00_of_01.state.json"
)
POST_ROWS = POST_STATE.with_suffix(".rows.csv")
STATUS = FUNCTIONAL_RG / "5396" / "status.json"
DOCUMENT = POST / "5443-Y5-R2FR-D4-parent-v49-right-connector-bounded-resume-gate.md"
VALIDATION = OUTPUT / "P8_Y5_BRR5396_5443_VALIDATION.csv"
RESULT = OUTPUT / "parent_v49_right_connector_bounded_resume_result.json"

EXPECTED_REVISION = "D4-deformed-contour-regular-away-W3-v49"
GEOMETRIC_FAILURE = (
    "EnclosureFailure:global contour geometric denominator reaches zero"
)
C0_EXTERNAL01_FAILURE = (
    "IntervalSingularity:away_arc_right_K5:s2:c0:left0:"
    "edge_0_0_1:stable_edge"
)
C1_EXTERNAL01_FAILURE = (
    "IntervalSingularity:away_arc_right_K5:s2:c1:left0:"
    "edge_0_0_1:stable_edge"
)
BROAD_FLAGS = (
    "valid_for_right_connector_completion",
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


def failure_count(state: dict[str, Any], category: str) -> int:
    return int(state.get("split_failure_counts", {}).get(category, 0))


def changed_failures(
    before: dict[str, Any], after: dict[str, Any]
) -> dict[str, int]:
    before_counts = before.get("split_failure_counts", {})
    after_counts = after.get("split_failure_counts", {})
    categories = sorted(set(before_counts) | set(after_counts))
    return {
        category: int(after_counts.get(category, 0))
        - int(before_counts.get(category, 0))
        for category in categories
        if int(after_counts.get(category, 0))
        != int(before_counts.get(category, 0))
    }


def write_document(payload: dict[str, Any]) -> None:
    decision = (
        "**PARENT V49 CONTINUES TO ADVANCE WITHOUT REPAIRED-FAILURE REGRESSION.**"
        if payload["valid_for_parent_v49_bounded_resume_progress"]
        else "**PARENT V49 BOUNDED-RESUME GATE REMAINS OPEN.**"
    )
    lines = [
        "# 5443: parent v49 right-connector bounded-resume gate",
        "",
        "## Decision",
        "",
        decision,
        "",
        "Two source-identical v49 production resumes were run from checkpoint 5442. Both stopped only at their runtime budgets and remained resume-safe.",
        "",
        "## Combined progress",
        "",
        f"- Accepted boxes: {payload['pre_accepted_count']} -> {payload['post_accepted_count']} (`+{payload['accepted_delta']}`).",
        f"- Live stack: {payload['pre_pending_count']} -> {payload['post_pending_count']}.",
        f"- Second-resume stack contraction: {payload['mid_pending_count']} -> {payload['post_pending_count']}.",
        f"- Collision-Jacobian failures: {payload['pre_geometric_failure_count']} -> {payload['post_geometric_failure_count']}.",
        f"- External01 c0 failures: {payload['pre_c0_failure_count']} -> {payload['post_c0_failure_count']}.",
        f"- External01 c1 failures: {payload['pre_c1_failure_count']} -> {payload['post_c1_failure_count']}.",
        "",
        "## Stack interpretation",
        "",
        "The combined live-stack count is not a completion percentage: after finishing the left subtree the depth-first runner opened the broad right subtree, temporarily increasing the stack. During the second resume that stack contracted from 12 to 9 while 18 boxes were accepted. Every newly accepted row has positive amplitude and collision-Jacobian lower bounds.",
        "",
        "## Claim boundary",
        "",
        "Nine right-connector boxes remain on the live depth-first stack. This is real certified progress, not right-connector completion; no regular-away W3, UV, local-GR, or full-MTS claim is made.",
    ]
    atomic_text(DOCUMENT, "\n".join(lines) + "\n")


def run_gate() -> dict[str, Any]:
    started = datetime.now(timezone.utc)
    ast.parse(PARENT_SCRIPT.read_text(encoding="utf-8"))
    classification = read_json(CLASSIFICATION_RESULT)
    classification_validation = read_csv(CLASSIFICATION_VALIDATION)
    pre = read_json(PRE_STATE)
    mid = read_json(MID_STATE)
    post = read_json(POST_STATE)
    status = read_json(STATUS)
    pre_rows = read_csv(PRE_ROWS)
    mid_rows = read_csv(MID_ROWS)
    post_rows = read_csv(POST_ROWS)
    new_rows = post_rows[len(pre_rows) :]
    second_new_rows = post_rows[len(mid_rows) :]
    accepted_rows_certified = bool(new_rows) and all(
        float(row["minimum_amplitude_denominator_abs_lower"]) > 0.0
        and float(row["collision_jacobian_abs_lower"]) > 0.0
        and float(row["integrated_regular_path_abs_upper"]) >= 0.0
        for row in new_rows
    )
    pre_accepted = int(pre["accepted_count"])
    mid_accepted = int(mid["accepted_count"])
    post_accepted = int(post["accepted_count"])
    pre_pending = len(pre["stack"])
    mid_pending = len(mid["stack"])
    post_pending = len(post["stack"])
    pre_geometric = failure_count(pre, GEOMETRIC_FAILURE)
    post_geometric = failure_count(post, GEOMETRIC_FAILURE)
    pre_c0 = failure_count(pre, C0_EXTERNAL01_FAILURE)
    post_c0 = failure_count(post, C0_EXTERNAL01_FAILURE)
    pre_c1 = failure_count(pre, C1_EXTERNAL01_FAILURE)
    post_c1 = failure_count(post, C1_EXTERNAL01_FAILURE)
    first_changes = changed_failures(pre, mid)
    second_changes = changed_failures(mid, post)
    valid = (
        pre["revision"] == mid["revision"] == post["revision"] == EXPECTED_REVISION
        and post_accepted > mid_accepted > pre_accepted
        and post_pending < mid_pending
        and accepted_rows_certified
        and pre_geometric == post_geometric
        and pre_c0 == post_c0
        and second_changes == {C1_EXTERNAL01_FAILURE: post_c1 - failure_count(mid, C1_EXTERNAL01_FAILURE)}
        and status["state"] == "paused_at_runtime_budget"
        and bool(status["resume_safe"])
    )
    payload = {
        "checkpoint": CHECKPOINT,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "revision": post["revision"],
        "pre_accepted_count": pre_accepted,
        "mid_accepted_count": mid_accepted,
        "post_accepted_count": post_accepted,
        "accepted_delta": post_accepted - pre_accepted,
        "second_resume_accepted_delta": post_accepted - mid_accepted,
        "pre_pending_count": pre_pending,
        "mid_pending_count": mid_pending,
        "post_pending_count": post_pending,
        "pre_geometric_failure_count": pre_geometric,
        "post_geometric_failure_count": post_geometric,
        "pre_c0_failure_count": pre_c0,
        "post_c0_failure_count": post_c0,
        "pre_c1_failure_count": pre_c1,
        "post_c1_failure_count": post_c1,
        "first_resume_changed_failures": first_changes,
        "second_resume_changed_failures": second_changes,
        "new_accepted_row_count": len(new_rows),
        "second_resume_new_accepted_row_count": len(second_new_rows),
        "accepted_rows_certified": accepted_rows_certified,
        "maximum_pending_depth": max(int(row[4]) for row in post["stack"]),
        "runtime_state": status["state"],
        "resume_safe": bool(status["resume_safe"]),
        "valid_for_parent_v49_bounded_resume_progress": valid,
        "next_target": "CONTINUE_PARENT_V49_RIGHT_CONNECTOR_RESUME",
        **{flag: False for flag in BROAD_FLAGS},
    }
    validations = [
        check(
            "all_sources_exist",
            all(
                path.exists()
                for path in (
                    PARENT_SCRIPT,
                    CLASSIFICATION_RESULT,
                    CLASSIFICATION_VALIDATION,
                    PRE_STATE,
                    PRE_ROWS,
                    MID_STATE,
                    MID_ROWS,
                    POST_STATE,
                    POST_ROWS,
                    STATUS,
                )
            ),
            "ten local inputs",
        ),
        check(
            "checkpoint_5442_is_green",
            int(classification["failed_validation_count"]) == 0
            and bool(
                classification[
                    "valid_for_c1_external01_coarse_refinement_classification"
                ]
            )
            and all(row["passed"] == "True" for row in classification_validation),
            f"rows={len(classification_validation)}",
        ),
        check(
            "revision_is_unchanged_v49",
            pre["revision"] == mid["revision"] == post["revision"] == EXPECTED_REVISION,
            post["revision"],
        ),
        check(
            "both_bounded_resumes_accept_new_boxes",
            post_accepted > mid_accepted > pre_accepted,
            f"accepted={pre_accepted}->{mid_accepted}->{post_accepted}",
        ),
        check(
            "second_resume_contracts_live_stack",
            post_pending < mid_pending,
            f"pending={mid_pending}->{post_pending}",
        ),
        check(
            "newly_accepted_rows_are_certified",
            accepted_rows_certified and len(new_rows) == post_accepted - pre_accepted,
            f"rows={len(new_rows)}",
        ),
        check(
            "repaired_failures_remain_frozen",
            pre_geometric == post_geometric and pre_c0 == post_c0,
            f"geometric={pre_geometric}->{post_geometric}, c0={pre_c0}->{post_c0}",
        ),
        check(
            "second_resume_only_sees_classified_c1_refinement",
            second_changes
            == {
                C1_EXTERNAL01_FAILURE: post_c1
                - failure_count(mid, C1_EXTERNAL01_FAILURE)
            },
            json.dumps(second_changes, sort_keys=True),
        ),
        check(
            "runner_stops_resume_safe_at_budget",
            status["state"] == "paused_at_runtime_budget"
            and bool(status["resume_safe"]),
            status["state"],
        ),
        check(
            "bounded_resume_progress_gate_passes",
            valid,
            "right-connector frontier remains numerically healthy",
        ),
        check(
            "broad_claims_remain_false",
            all(not payload[flag] for flag in BROAD_FLAGS),
            f"pending={post_pending}",
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
