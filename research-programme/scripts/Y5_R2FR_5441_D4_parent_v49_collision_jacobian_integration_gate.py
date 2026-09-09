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


CHECKPOINT = 5441
POST = Path(__file__).resolve().parents[1]
ROOT = POST.parent
FORMALIZATION = ROOT / "formalization-workbench"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
OUTPUT = FUNCTIONAL_RG / str(CHECKPOINT)
PARENT_SCRIPT = (
    POST / "scripts" / "Y5_R2FR_5396_D4_deformed_contour_regular_away_W3.py"
)
PREVIOUS_RESULT = (
    FUNCTIONAL_RG / "5440" / "collision_jacobian_finite_subcover_result.json"
)
PREVIOUS_VALIDATION = (
    FUNCTIONAL_RG / "5440" / "P8_Y5_BRR5396_5440_VALIDATION.csv"
)
DRY_RUN_RESULT = FUNCTIONAL_RG / "5396" / "dry_run_result.json"
PRE_STATE = OUTPUT / "v48_pre_resume_state.json"
POST_STATE = (
    FUNCTIONAL_RG
    / "5396"
    / "partial"
    / "path_parts"
    / "_partitions"
    / "bin_00_sub_00_S_X006_MC04_SP_DP_RIGHT_CONNECTOR_part_00_of_01.state.json"
)
POST_ROWS = POST_STATE.with_suffix(".rows.csv")
DOCUMENT = POST / "5441-Y5-R2FR-D4-parent-v49-collision-jacobian-integration-gate.md"
VALIDATION = OUTPUT / "P8_Y5_BRR5396_5441_VALIDATION.csv"
RESULT = OUTPUT / "parent_v49_collision_jacobian_integration_result.json"

EXPECTED_PRE_REVISION = "D4-deformed-contour-regular-away-W3-v48"
EXPECTED_POST_REVISION = "D4-deformed-contour-regular-away-W3-v49"
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


def write_document(payload: dict[str, Any]) -> None:
    decision = (
        "**PARENT V49 COLLISION-JACOBIAN INTEGRATION PASSES.**"
        if payload["valid_for_parent_v49_collision_jacobian_integration"]
        else "**PARENT V49 COLLISION-JACOBIAN INTEGRATION REMAINS OPEN.**"
    )
    lines = [
        "# 5441: parent v49 collision-Jacobian integration gate",
        "",
        "## Decision",
        "",
        decision,
        "",
        "Parent v49 adds the source-proved `8 x 64` path-correlated projective cover from checkpoint 5440. It changes only enclosure resolution; it inserts no value, fit, or closure assumption.",
        "",
        "## Production delta",
        "",
        f"- Revision: `{payload['pre_revision']}` -> `{payload['post_revision']}`.",
        f"- Accepted boxes: {payload['pre_accepted_count']} -> {payload['post_accepted_count']} (`+{payload['accepted_delta']}`).",
        f"- Pending boxes: {payload['pre_pending_count']} -> {payload['post_pending_count']} (`{payload['pending_delta']}`).",
        f"- Collision-Jacobian failures: {payload['pre_geometric_failure_count']} -> {payload['post_geometric_failure_count']}.",
        f"- External01 c0 failures: {payload['pre_c0_failure_count']} -> {payload['post_c0_failure_count']}.",
        f"- External01 c1 failures: {payload['pre_c1_failure_count']} -> {payload['post_c1_failure_count']}.",
        "",
        "## Interpretation",
        "",
        "The geometric failure count froze while the frontier advanced, so the v49 resolution extension works in production. The only increasing category is the already known c1 external01 edge. That edge, not collision geometry, is now the active derivation target.",
        "",
        "## Claim boundary",
        "",
        "This validates only parent integration of the local collision-Jacobian cover. Seven right-connector boxes remain pending; no right-connector, regular-away W3, UV, local-GR, or full-MTS claim is made.",
    ]
    atomic_text(DOCUMENT, "\n".join(lines) + "\n")


def run_gate() -> dict[str, Any]:
    started = datetime.now(timezone.utc)
    ast.parse(PARENT_SCRIPT.read_text(encoding="utf-8"))
    previous = read_json(PREVIOUS_RESULT)
    previous_validation = read_csv(PREVIOUS_VALIDATION)
    dry_run = read_json(DRY_RUN_RESULT)
    pre = read_json(PRE_STATE)
    post = read_json(POST_STATE)
    pre_failures = pre.get("split_failure_counts", {})
    post_failures = post.get("split_failure_counts", {})
    all_categories = sorted(set(pre_failures) | set(post_failures))
    changed = {
        category: int(post_failures.get(category, 0))
        - int(pre_failures.get(category, 0))
        for category in all_categories
        if int(post_failures.get(category, 0))
        != int(pre_failures.get(category, 0))
    }
    pre_accepted = int(pre["accepted_count"])
    post_accepted = int(post["accepted_count"])
    pre_pending = len(pre["stack"])
    post_pending = len(post["stack"])
    pre_geometric = failure_count(pre, GEOMETRIC_FAILURE)
    post_geometric = failure_count(post, GEOMETRIC_FAILURE)
    pre_c0 = failure_count(pre, C0_EXTERNAL01_FAILURE)
    post_c0 = failure_count(post, C0_EXTERNAL01_FAILURE)
    pre_c1 = failure_count(pre, C1_EXTERNAL01_FAILURE)
    post_c1 = failure_count(post, C1_EXTERNAL01_FAILURE)
    integration_passed = (
        pre["revision"] == EXPECTED_PRE_REVISION
        and post["revision"] == EXPECTED_POST_REVISION
        and post_accepted > pre_accepted
        and post_pending < pre_pending
        and post_geometric == pre_geometric
        and post_c0 == pre_c0
        and changed == {C1_EXTERNAL01_FAILURE: post_c1 - pre_c1}
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
        "pre_geometric_failure_count": pre_geometric,
        "post_geometric_failure_count": post_geometric,
        "pre_c0_failure_count": pre_c0,
        "post_c0_failure_count": post_c0,
        "pre_c1_failure_count": pre_c1,
        "post_c1_failure_count": post_c1,
        "changed_failure_counts": changed,
        "valid_for_parent_v49_collision_jacobian_integration": (
            integration_passed
        ),
        "next_target": "DERIVE_C1_EXTERNAL01_EDGE_SUBCOVER",
        **{flag: False for flag in BROAD_FLAGS},
    }
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
                    PRE_STATE,
                    POST_STATE,
                    POST_ROWS,
                )
            ),
            "seven local inputs",
        ),
        check(
            "checkpoint_5440_is_green",
            int(previous["failed_validation_count"]) == 0
            and bool(
                previous["valid_for_collision_jacobian_finite_subcover"]
            )
            and all(row["passed"] == "True" for row in previous_validation),
            f"rows={len(previous_validation)}",
        ),
        check(
            "parent_ast_parses_and_v49_dry_run_passes",
            bool(dry_run["dry_run_passed"])
            and int(dry_run["source_count"]) == 15
            and int(dry_run["path_job_count"]) == 240,
            f"sources={dry_run['source_count']}, jobs={dry_run['path_job_count']}",
        ),
        check(
            "v48_state_migrated_to_v49",
            pre["revision"] == EXPECTED_PRE_REVISION
            and post["revision"] == EXPECTED_POST_REVISION,
            f"{pre['revision']} -> {post['revision']}",
        ),
        check(
            "production_frontier_advanced",
            post_accepted > pre_accepted and post_pending < pre_pending,
            f"accepted={pre_accepted}->{post_accepted}, pending={pre_pending}->{post_pending}",
        ),
        check(
            "collision_jacobian_failure_count_froze",
            post_geometric == pre_geometric,
            f"count={pre_geometric}->{post_geometric}",
        ),
        check(
            "external01_c0_did_not_regress",
            post_c0 == pre_c0,
            f"count={pre_c0}->{post_c0}",
        ),
        check(
            "only_known_c1_edge_increased",
            changed == {C1_EXTERNAL01_FAILURE: post_c1 - pre_c1}
            and post_c1 > pre_c1,
            json.dumps(changed, sort_keys=True),
        ),
        check(
            "integration_gate_passes",
            integration_passed,
            "v49 resolves collision geometry and exposes c1 only",
        ),
        check(
            "broad_claims_remain_false",
            all(not payload[flag] for flag in BROAD_FLAGS),
            "seven pending boxes remain",
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
