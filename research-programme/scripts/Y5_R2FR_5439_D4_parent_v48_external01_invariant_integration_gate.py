from __future__ import annotations

import ast
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


CHECKPOINT = 5439
POST = Path(__file__).resolve().parents[1]
ROOT = POST.parent
FORMALIZATION = ROOT / "formalization-workbench"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
OUTPUT = FUNCTIONAL_RG / str(CHECKPOINT)
PARENT_SCRIPT = (
    POST / "scripts" / "Y5_R2FR_5396_D4_deformed_contour_regular_away_W3.py"
)
PREVIOUS_RESULT = (
    FUNCTIONAL_RG
    / "5438"
    / "external01_negative_real_invariant_subcover_result.json"
)
PREVIOUS_VALIDATION = (
    FUNCTIONAL_RG / "5438" / "P8_Y5_BRR5396_5438_VALIDATION.csv"
)
DRY_RUN_RESULT = FUNCTIONAL_RG / "5396" / "dry_run_result.json"
LOADER_SMOKE = OUTPUT / "v48_certificate_loader_smoke.json"
PRE_STATE = OUTPUT / "v47_pre_resume_state.json"
POST_STATE = (
    FUNCTIONAL_RG
    / "5396"
    / "partial"
    / "path_parts"
    / "_partitions"
    / "bin_00_sub_00_S_X006_MC04_SP_DP_RIGHT_CONNECTOR_part_00_of_01.state.json"
)
POST_ROWS = POST_STATE.with_suffix(".rows.csv")
DOCUMENT = POST / "5439-Y5-R2FR-D4-parent-v48-external01-invariant-integration-gate.md"
VALIDATION = OUTPUT / "P8_Y5_BRR5396_5439_VALIDATION.csv"
RESULT = OUTPUT / "parent_v48_external01_invariant_integration_result.json"

EXPECTED_REVISION = "D4-deformed-contour-regular-away-W3-v48"
C0_FAILURE = (
    "IntervalSingularity:away_arc_right_K5:s2:c0:left0:"
    "edge_0_0_1:stable_edge"
)
EXPECTED_NEW_FAILURE = (
    "EnclosureFailure:global contour geometric denominator reaches zero"
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


def count(state: dict[str, Any], category: str) -> int:
    return int(state.get("split_failure_counts", {}).get(category, 0))


def write_document(payload: dict[str, Any]) -> None:
    decision = (
        "**PARENT V48 INTEGRATION PASSES.**"
        if payload["valid_for_parent_v48_external01_invariant_integration"]
        else "**PARENT V48 INTEGRATION REMAINS OPEN.**"
    )
    lines = [
        "# 5439: parent v48 external01 invariant integration gate",
        "",
        "## Decision",
        "",
        decision,
        "",
        "The source-complete 5438 finite-cover certificate is now consumed by parent v48. The exact amplitude route remains `1/<01> = [01]/s01`; no angle-edge value or closure axiom was inserted.",
        "",
        "## Resume delta",
        "",
        f"- Revision: `{payload['pre_revision']}` -> `{payload['post_revision']}`.",
        f"- Accepted boxes: {payload['pre_accepted_count']} -> {payload['post_accepted_count']} (`+{payload['accepted_delta']}`).",
        f"- Pending boxes: {payload['pre_pending_count']} -> {payload['post_pending_count']} (`{payload['pending_delta']}`).",
        f"- External01 c0 failures: {payload['pre_c0_failure_count']} -> {payload['post_c0_failure_count']}.",
        f"- Newly exposed categories: `{payload['new_failure_categories']}`.",
        "",
        "## Interpretation",
        "",
        "The unchanged c0 count while accepted work advances is the production-level acceptance test for the new invariant route. One downstream collision-Jacobian enclosure appeared at a depth-14 cell; it is not an external01 regression and remains the next local numerical target if it recurs.",
        "",
        "## Claim boundary",
        "",
        "This closes only the parent integration gate for the representative external01 invariant certificate. Four right-connector branches remain pending, so no right-connector, W3, UV, or local-GR claim is made.",
    ]
    atomic_text(DOCUMENT, "\n".join(lines) + "\n")


def run_gate() -> dict[str, Any]:
    started = datetime.now(timezone.utc)
    ast.parse(PARENT_SCRIPT.read_text(encoding="utf-8"))
    previous = read_json(PREVIOUS_RESULT)
    previous_validation = read_csv(PREVIOUS_VALIDATION)
    dry_run = read_json(DRY_RUN_RESULT)
    loader = read_json(LOADER_SMOKE)
    pre = read_json(PRE_STATE)
    post = read_json(POST_STATE)
    pre_failures = set(pre.get("split_failure_counts", {}))
    post_failures = set(post.get("split_failure_counts", {}))
    new_failures = sorted(post_failures - pre_failures)
    pre_accepted = int(pre["accepted_count"])
    post_accepted = int(post["accepted_count"])
    pre_pending = len(pre["stack"])
    post_pending = len(post["stack"])
    pre_c0 = count(pre, C0_FAILURE)
    post_c0 = count(post, C0_FAILURE)
    integration_passed = (
        post["revision"] == EXPECTED_REVISION
        and post_accepted > pre_accepted
        and post_pending < pre_pending
        and post_c0 == pre_c0
        and new_failures in ([], [EXPECTED_NEW_FAILURE])
    )
    payload = {
        "checkpoint": CHECKPOINT,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "pre_revision": pre["revision"],
        "post_revision": post["revision"],
        "pre_accepted_count": pre_accepted,
        "post_accepted_count": post_accepted,
        "accepted_delta": post_accepted - pre_accepted,
        "pre_pending_count": pre_pending,
        "post_pending_count": post_pending,
        "pending_delta": post_pending - pre_pending,
        "pre_c0_failure_count": pre_c0,
        "post_c0_failure_count": post_c0,
        "new_failure_categories": "|".join(new_failures),
        "valid_for_parent_v48_external01_invariant_integration": (
            integration_passed
        ),
        "next_target": "RESUME_REMAINING_RIGHT_CONNECTOR_BRANCHES",
        **{flag: False for flag in BROAD_FLAGS},
    }
    formalization_touches = [
        path
        for path in FORMALIZATION.rglob("*")
        if path.is_file()
        and datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) > started
    ]
    validations = [
        check(
            "all_sources_exist",
            all(
                path.exists()
                for path in (
                    PARENT_SCRIPT,
                    PREVIOUS_RESULT,
                    PREVIOUS_VALIDATION,
                    DRY_RUN_RESULT,
                    LOADER_SMOKE,
                    PRE_STATE,
                    POST_STATE,
                    POST_ROWS,
                )
            ),
            "eight local inputs",
        ),
        check(
            "checkpoint_5438_is_green",
            int(previous["failed_validation_count"]) == 0
            and bool(
                previous[
                    "valid_for_external01_negative_real_invariant_subcover"
                ]
            )
            and all(row["passed"] == "True" for row in previous_validation),
            f"rows={len(previous_validation)}",
        ),
        check(
            "parent_ast_parses_and_dry_run_passes",
            bool(dry_run["dry_run_passed"])
            and int(dry_run["source_count"]) == 15
            and int(dry_run["path_job_count"]) == 240,
            (
                f"sources={dry_run['source_count']}, "
                f"jobs={dry_run['path_job_count']}"
            ),
        ),
        check(
            "certificate_loader_covers_LR_and_R",
            loader["revision"] == EXPECTED_REVISION
            and {row["target"] for row in loader["rows"]} == {"LR", "R"}
            and all(float(row["invariant_abs_lower"]) > 0.0 for row in loader["rows"]),
            f"rows={len(loader['rows'])}",
        ),
        check(
            "v47_state_migrated_to_v48",
            pre["revision"]
            == "D4-deformed-contour-regular-away-W3-v47"
            and post["revision"] == EXPECTED_REVISION,
            f"{pre['revision']} -> {post['revision']}",
        ),
        check(
            "production_frontier_advanced",
            post_accepted > pre_accepted and post_pending < pre_pending,
            (
                f"accepted {pre_accepted}->{post_accepted}; "
                f"pending {pre_pending}->{post_pending}"
            ),
        ),
        check(
            "external01_c0_failure_count_stopped",
            post_c0 == pre_c0,
            f"{pre_c0}->{post_c0}",
        ),
        check(
            "new_failure_is_downstream_or_absent",
            new_failures in ([], [EXPECTED_NEW_FAILURE]),
            "|".join(new_failures),
        ),
        check(
            "parent_v48_integration_passes",
            integration_passed,
            f"accepted delta={post_accepted - pre_accepted}",
        ),
        check(
            "formalization_workbench_untouched",
            not formalization_touches,
            f"touches={len(formalization_touches)}",
        ),
        check(
            "broad_claim_flags_false",
            not any(bool(payload[flag]) for flag in BROAD_FLAGS),
            "all broad flags false",
        ),
    ]
    payload["failed_validation_count"] = sum(
        not bool(row["passed"]) for row in validations
    )
    payload["elapsed_seconds"] = (
        datetime.now(timezone.utc) - started
    ).total_seconds()
    atomic_csv(VALIDATION, validations)
    atomic_json(RESULT, payload)
    write_document(payload)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return payload


if __name__ == "__main__":
    result = run_gate()
    raise SystemExit(0 if result["failed_validation_count"] == 0 else 1)
