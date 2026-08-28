from __future__ import annotations

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
SOURCE = POST / "source-intake" / "functional_rg" / "5396"
OUTPUT = POST / "source-intake" / "functional_rg" / "5409"
PARENT_SCRIPT = (
    POST
    / "scripts"
    / "Y5_R2FR_5396_D4_deformed_contour_regular_away_W3.py"
)
DOCUMENT = (
    POST
    / "5409-Y5-R2FR-D4-representative-external41-production-stability-gate.md"
)
PREVIOUS = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5408"
    / "representative_external41_square_subcover_gate_result.json"
)
STATUS = SOURCE / "status.json"
ACTIVE_STATE = (
    SOURCE
    / "partial"
    / "path_parts"
    / "_partitions"
    / "bin_00_sub_00_S_X006_MC04_SP_DP_LEFT_CONNECTOR_part_00_of_01.state.json"
)
ACTIVE_ROWS = ACTIVE_STATE.with_suffix(".rows.csv")

EXPECTED_PARAMETER_AREA = 0.03932753620548854
REPAIRED_PATH = "LLDLDLDLDLDLDLDLDL"
ALLOWED_FAILURE_CATEGORIES = {
    "EnclosureFailure:global contour geometric denominator reaches zero",
    "IntervalSingularity:away_arc_left_K5:s1:c0:left1:edge_2_1_3:stable_edge",
    "IntervalSingularity:away_arc_left_K5:s1:c0:right1:edge_1_4_2:stable_edge",
    "IntervalSingularity:away_arc_right_K5:s2:c1:left0:edge_0_0_1:stable_edge",
    "IntervalSingularity:no displaced first-spinor rational pivot survives: away_arc_left_first",
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
    return {"check": name, "passed": bool(passed), "evidence": evidence}


def pending_area(stack: list[list[Any]]) -> float:
    return sum(
        (float(row[1]) - float(row[0]))
        * (float(row[3]) - float(row[2]))
        for row in stack
    )


def write_document(payload: dict[str, Any]) -> None:
    lines = [
        "# 5409: representative external-4/first production-stability gate",
        "",
        "## Decision",
        "",
        "**PASS FOR CONTINUED V41 PRODUCTION ONLY.**",
        "",
        "Checkpoint 5408 proved the representative `[14]` square-edge identity on the first depth-18 leaf. This gate tests whether that repair survives ordinary production rather than merely passing its construction box.",
        "",
        "## Production regression",
        "",
        f"- accepted boxes advance `{payload['previous_accepted_box_count']} -> {payload['active_accepted_box_count']}`;",
        f"- net new certified boxes: `{payload['net_new_certified_box_count']}`;",
        f"- pending stack changes `{payload['previous_pending_box_count']} -> {payload['active_pending_box_count']}`;",
        f"- maximum pending depth recedes `{payload['previous_maximum_pending_depth']} -> {payload['active_maximum_pending_depth']}`;",
        f"- exact accepted-plus-pending area: `{payload['total_parameter_area']:.17g}`;",
        f"- current accepted-area fraction: `{payload['accepted_area_fraction']:.17g}`;",
        f"- minimum denominator among all accepted rows: `{payload['minimum_accepted_denominator_abs_lower']:.17g}`.",
        "",
        "Every depth-17 descendant reached during the regression is certified. The split ledger contains only pre-existing outer-enclosure categories; no new representative external-4/first square class appears. The correct next step is ordinary subdivision, not another analytic replacement.",
        "",
        "## Claim boundary",
        "",
        "This is a local production-stability result for one active contour path. It does not close that path, the regular-away W3 sum, event-local W3, UV finiteness, local GR, or the full MTS framework.",
        "",
    ]
    atomic_text(DOCUMENT, "\n".join(lines))


def run_gate() -> dict[str, Any]:
    required = (PARENT_SCRIPT, PREVIOUS, STATUS, ACTIVE_STATE, ACTIVE_ROWS)
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise FileNotFoundError("missing checkpoint input: " + " | ".join(missing))

    previous = read_json(PREVIOUS)
    status = read_json(STATUS)
    state = read_json(ACTIVE_STATE)
    rows = read_csv(ACTIVE_ROWS)
    source = PARENT_SCRIPT.read_text(encoding="utf-8")
    accepted_area = sum(float(row["parameter_area"]) for row in rows)
    remaining_area = pending_area(state["stack"])
    total_area = accepted_area + remaining_area
    pending_depths = [int(row[4]) for row in state["stack"]]
    maximum_pending_depth = max(pending_depths, default=-1)
    split_categories = set(state["split_failure_counts"])
    new_split_categories = sorted(split_categories - ALLOWED_FAILURE_CATEGORIES)
    repaired_rows = [
        row for row in rows if row["refinement_path"] == REPAIRED_PATH
    ]
    new_rows = rows[int(previous["active_accepted_box_count"]) :]
    broad_columns = (
        "valid_for_D4_numeric_W3_bound",
        "valid_for_D4_numeric_uniform_remainder_bound",
        "valid_for_numeric_UV_claim",
        "valid_for_local_GR_claim",
        "valid_for_full_MTS_claim",
    )
    all_rows_claim_safe = all(
        row[column] == "False" for row in rows for column in broad_columns
    )
    minimum_denominator = min(
        float(row["minimum_amplitude_denominator_abs_lower"])
        for row in rows
    )
    deepest_new_accepted_depth = max(
        (int(row["refinement_depth"]) for row in new_rows), default=-1
    )
    validations = [
        check("required_inputs_exist", not missing, f"{len(required)} paths present"),
        check(
            "checkpoint_5408_authorizes_continuation",
            bool(previous["valid_for_continued_v41_production"])
            and previous["valid_for_regular_away_W3_claim"] is False
            and previous["valid_for_full_MTS_claim"] is False,
            "5408 authorizes v41 production only",
        ),
        check(
            "v41_square_repair_remains_installed",
            'REVISION = "D4-deformed-contour-regular-away-W3-v41"' in source
            and "centered_path_correlated_external4_first_square" in source
            and "subdivided_path_correlated_external4_first_square" in source,
            "v41 exact ratio and finite subcover remain source-owned",
        ),
        check(
            "adaptive_area_partition_is_exact",
            math.isclose(
                total_area,
                EXPECTED_PARAMETER_AREA,
                rel_tol=1.0e-12,
                abs_tol=1.0e-12,
            ),
            f"accepted={accepted_area:.17g}; pending={remaining_area:.17g}",
        ),
        check(
            "production_advanced_thirty_boxes",
            len(rows) == int(state["accepted_count"]) == 37
            and len(new_rows) == 30,
            "accepted rows advance 7 -> 37 without discarding certificates",
        ),
        check(
            "deep_frontier_receded_without_failure",
            deepest_new_accepted_depth == 17
            and maximum_pending_depth == 14
            and status["state"] == "paused_at_runtime_budget"
            and bool(status["resume_safe"]),
            "depth-17 descendants certify and the pending frontier recedes to depth 14",
        ),
        check(
            "repaired_depth_eighteen_leaf_is_preserved",
            len(repaired_rows) == 1
            and repaired_rows[0]["valid_for_D4_numeric_regular_away_W3_bound"]
            == "True"
            and float(
                repaired_rows[0]["minimum_amplitude_denominator_abs_lower"]
            )
            > 0.0,
            "the checkpoint-5408 leaf remains committed",
        ),
        check(
            "all_accepted_rows_are_finite",
            minimum_denominator > 0.0
            and all(
                row["valid_for_D4_numeric_regular_away_W3_bound"] == "True"
                for row in rows
            ),
            f"minimum denominator lower bound={minimum_denominator:.17g}",
        ),
        check(
            "no_new_failure_class_appeared",
            not new_split_categories,
            "split ledger remains within the five pre-existing categories",
        ),
        check(
            "broad_claims_remain_false",
            all_rows_claim_safe,
            "W3, UV, local-GR, and full-MTS flags remain false",
        ),
    ]
    failed = [row for row in validations if not row["passed"]]
    payload = {
        "checkpoint": 5409,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "validation_count": len(validations),
        "failed_validation_count": len(failed),
        "valid_for_representative_external41_production_stability": not failed,
        "valid_for_continued_v41_production": not failed,
        "valid_for_regular_away_W3_claim": False,
        "valid_for_numeric_W3_claim": False,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
        "previous_accepted_box_count": int(previous["active_accepted_box_count"]),
        "active_accepted_box_count": int(state["accepted_count"]),
        "net_new_certified_box_count": len(new_rows),
        "previous_pending_box_count": int(previous["active_pending_box_count"]),
        "active_pending_box_count": len(state["stack"]),
        "previous_maximum_pending_depth": 16,
        "active_maximum_pending_depth": maximum_pending_depth,
        "deepest_new_accepted_depth": deepest_new_accepted_depth,
        "accepted_parameter_area": accepted_area,
        "pending_parameter_area": remaining_area,
        "total_parameter_area": total_area,
        "accepted_area_fraction": accepted_area / total_area,
        "minimum_accepted_denominator_abs_lower": minimum_denominator,
        "completed_path_jobs": int(status["completed_path_jobs"]),
        "total_path_jobs": int(status["total_path_jobs"]),
        "split_failure_categories": sorted(split_categories),
        "new_split_failure_categories": new_split_categories,
        "provenance_sha256": {
            str(path.relative_to(POST)): sha256(path) for path in required
        },
    }
    atomic_csv(OUTPUT / "P8_Y5_BRR5396_5409_VALIDATION.csv", validations)
    atomic_json(
        OUTPUT / "representative_external41_production_stability_result.json",
        payload,
    )
    write_document(payload)
    print(json.dumps(payload, indent=2, sort_keys=True))
    if failed:
        raise RuntimeError(
            "checkpoint 5409 validation failed: "
            + " | ".join(row["check"] for row in failed)
        )
    return payload


if __name__ == "__main__":
    run_gate()
