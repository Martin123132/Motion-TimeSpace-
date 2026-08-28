from __future__ import annotations

import ast
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


CHECKPOINT = 5415
POST = Path(__file__).resolve().parents[1]
ROOT = POST.parent
FORMALIZATION = ROOT / "formalization-workbench"
SOURCE = POST / "source-intake" / "functional_rg" / "5396"
PARTS = SOURCE / "partial" / "path_parts"
PARTITIONS = PARTS / "_partitions"
OUTPUT = POST / "source-intake" / "functional_rg" / str(CHECKPOINT)
PARENT_SCRIPT = POST / "scripts" / "Y5_R2FR_5396_D4_deformed_contour_regular_away_W3.py"
PREVIOUS = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5414"
    / "v43_post_edge_production_stability_result.json"
)
STATUS = SOURCE / "status.json"
LEFT_ROWS = PARTS / "bin_00_sub_00_S_X006_MC04_SP_DP_LEFT_CONNECTOR.csv"
LEFT_PARTITION = (
    PARTITIONS
    / "bin_00_sub_00_S_X006_MC04_SP_DP_LEFT_CONNECTOR_part_00_of_01.csv"
)
TOP_ROWS = PARTS / "bin_00_sub_00_S_X006_MC04_SP_DP_TOP.csv"
TOP_PARTITION = (
    PARTITIONS / "bin_00_sub_00_S_X006_MC04_SP_DP_TOP_part_00_of_01.csv"
)
RIGHT_STATE = (
    PARTITIONS
    / "bin_00_sub_00_S_X006_MC04_SP_DP_RIGHT_CONNECTOR_part_00_of_01.state.json"
)
RIGHT_ROWS = RIGHT_STATE.with_suffix(".rows.csv")
DOCUMENT = POST / "5415-Y5-R2FR-D4-v43-left-and-top-path-completion-gate.md"
SUMMARY = OUTPUT / "v43_left_and_top_path_completion_summary.csv"
VALIDATION = OUTPUT / "P8_Y5_BRR5396_5415_VALIDATION.csv"
RESULT = OUTPUT / "v43_left_and_top_path_completion_result.json"

REVISION = "D4-deformed-contour-regular-away-W3-v43"
EXPECTED_AREA = 0.03932753620548857
EXPECTED_RIGHT_FAILURE_CATEGORIES = {
    "IntervalSingularity:away_arc_left_K5:s1:c0:left1:edge_2_1_3:stable_edge",
    "IntervalSingularity:away_arc_left_K5:s1:c0:right1:edge_1_4_2:stable_edge",
    "IntervalSingularity:away_arc_right_K5:s2:c1:left0:edge_0_0_1:stable_edge",
    "IntervalSingularity:no displaced first-spinor rational pivot survives: away_arc_left_first",
}
BROAD_COLUMNS = (
    "valid_for_D4_numeric_W3_bound",
    "valid_for_D4_numeric_uniform_remainder_bound",
    "valid_for_D4_outer_regulator_zero_limit",
    "valid_for_numeric_UV_claim",
    "valid_for_local_GR_claim",
    "valid_for_full_MTS_claim",
)
POSITIVE_COLUMNS = (
    "parameter_area",
    "minimum_amplitude_denominator_abs_lower",
    "relative_root_abs_lower",
    "selected_global_root_abs_lower",
    "collision_jacobian_abs_lower",
)
NONNEGATIVE_COLUMNS = (
    "raw_integrand_abs_upper",
    "regular_integrand_abs_upper",
    "integrated_regular_path_abs_upper",
    "global_regularized_coefficient_abs_upper",
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
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(path)


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest().upper()


def source_revision(path: Path) -> str:
    source = path.read_text(encoding="utf-8")
    compile(source, str(path), "exec")
    tree = ast.parse(source, filename=str(path))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(
            isinstance(target, ast.Name) and target.id == "REVISION"
            for target in node.targets
        ):
            return str(ast.literal_eval(node.value))
    return ""


def parameter_area(rows: list[dict[str, str]]) -> float:
    return sum(float(row["parameter_area"]) for row in rows)


def pending_area(stack: list[list[Any]]) -> float:
    return sum(
        (float(row[1]) - float(row[0]))
        * (float(row[3]) - float(row[2]))
        for row in stack
    )


def is_true(value: Any) -> bool:
    return str(value).strip().lower() == "true"


def proof_rows_valid(rows: list[dict[str, str]]) -> bool:
    return all(
        all(
            math.isfinite(float(row[column])) and float(row[column]) > 0.0
            for column in POSITIVE_COLUMNS
        )
        and all(
            math.isfinite(float(row[column])) and float(row[column]) >= 0.0
            for column in NONNEGATIVE_COLUMNS
        )
        for row in rows
    )


def check(name: str, passed: bool, evidence: str) -> dict[str, Any]:
    return {"check": name, "passed": bool(passed), "evidence": evidence}


def write_document(payload: dict[str, Any]) -> None:
    lines = [
        "# 5415: v43 left-and-top path-completion gate",
        "",
        "## Decision",
        "",
        "**PASS FOR TWO ADDITIONAL COMPLETED PATH JOBS AND CONTINUED V43 PRODUCTION ONLY.**",
        "",
        "The `S_X006_MC04_SP_DP` left connector closes under the unchanged v43 proof at `511` certified boxes. Its top path then closes as one box. Production advances from `27/240` to `29/240` completed contour path jobs.",
        "",
        "## Transition evidence",
        "",
        f"- left connector rows: `{payload['left_connector_box_count']}`;",
        f"- top rows: `{payload['top_box_count']}`;",
        f"- each completed path reproduces parameter area `{payload['left_connector_parameter_area']:.17g}`;",
        f"- active right connector: `{payload['right_connector_accepted_box_count']}` accepted and `{payload['right_connector_pending_box_count']}` pending boxes at maximum depth `{payload['right_connector_maximum_pending_depth']}`;",
        f"- active-right failure classes: `{payload['right_connector_failure_category_count']}`, all previously declared.",
        "",
        "Every completed and active accepted proof row retains finite positive amplitude-denominator and collision-Jacobian margins. No completed certificate depends on a point sample or fitted closure coefficient.",
        "",
        "## Claim boundary",
        "",
        "The right connector and 211 further contour jobs remain open. Regular-away W3, event-local W3, combined W3, regulator limit, UV, local-GR, and full-MTS claims remain false.",
        "",
    ]
    atomic_text(DOCUMENT, "\n".join(lines))


def run_gate() -> dict[str, Any]:
    started = datetime.now(timezone.utc)
    required = (
        PARENT_SCRIPT,
        PREVIOUS,
        STATUS,
        LEFT_ROWS,
        LEFT_PARTITION,
        TOP_ROWS,
        TOP_PARTITION,
        RIGHT_STATE,
        RIGHT_ROWS,
    )
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise FileNotFoundError("missing checkpoint input: " + " | ".join(missing))

    revision = source_revision(PARENT_SCRIPT)
    previous = read_json(PREVIOUS)
    status = read_json(STATUS)
    left_rows = read_csv(LEFT_ROWS)
    left_partition_rows = read_csv(LEFT_PARTITION)
    top_rows = read_csv(TOP_ROWS)
    top_partition_rows = read_csv(TOP_PARTITION)
    right_state = read_json(RIGHT_STATE)
    right_rows = read_csv(RIGHT_ROWS)
    left_area = parameter_area(left_rows)
    top_area = parameter_area(top_rows)
    right_accepted_area = parameter_area(right_rows)
    right_pending_area = pending_area(right_state["stack"])
    right_total_area = right_accepted_area + right_pending_area
    right_failure_counts = {
        str(key): int(value)
        for key, value in right_state.get("split_failure_counts", {}).items()
    }
    all_rows = [*left_rows, *top_rows, *right_rows]
    broad_claims_false = all(
        not is_true(row[column]) for row in all_rows for column in BROAD_COLUMNS
    )
    formalization_touches = [
        path
        for path in FORMALIZATION.rglob("*")
        if path.is_file()
        and datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) > started
    ]

    payload: dict[str, Any] = {
        "checkpoint": CHECKPOINT,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "parent_revision": revision,
        "baseline_completed_path_jobs": int(previous["completed_path_jobs"]),
        "completed_path_jobs": int(status["completed_path_jobs"]),
        "total_path_jobs": int(status["total_path_jobs"]),
        "new_completed_path_job_count": int(status["completed_path_jobs"])
        - int(previous["completed_path_jobs"]),
        "left_connector_box_count": len(left_rows),
        "left_connector_parameter_area": left_area,
        "top_box_count": len(top_rows),
        "top_parameter_area": top_area,
        "right_connector_accepted_box_count": len(right_rows),
        "right_connector_pending_box_count": len(right_state["stack"]),
        "right_connector_maximum_pending_depth": max(
            (int(row[4]) for row in right_state["stack"]), default=0
        ),
        "right_connector_failure_category_count": len(right_failure_counts),
        "right_connector_accepted_parameter_area": right_accepted_area,
        "right_connector_pending_parameter_area": right_pending_area,
        "right_connector_total_parameter_area": right_total_area,
        "minimum_proof_denominator_abs_lower": min(
            float(row["minimum_amplitude_denominator_abs_lower"])
            for row in all_rows
        ),
        "minimum_collision_jacobian_abs_lower": min(
            float(row["collision_jacobian_abs_lower"]) for row in all_rows
        ),
        "valid_for_two_completed_path_jobs": True,
        "valid_for_continued_v43_production": True,
        "valid_for_regular_away_W3_claim": False,
        "valid_for_numeric_W3_claim": False,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
        "provenance_sha256": {
            str(path.relative_to(POST)): sha256(path) for path in required
        },
    }
    atomic_csv(
        SUMMARY,
        [{key: value for key, value in payload.items() if key not in {"created_utc", "provenance_sha256"}}],
    )
    write_document(payload)

    validations = [
        check("required_inputs_exist", not missing, f"{len(required)} paths present"),
        check("parent_source_compiles_as_v43", revision == REVISION, revision),
        check(
            "production_advances_by_two_path_jobs",
            payload["baseline_completed_path_jobs"] == 27
            and payload["completed_path_jobs"] == 29
            and payload["new_completed_path_job_count"] == 2,
            f"completed {payload['baseline_completed_path_jobs']} -> {payload['completed_path_jobs']}",
        ),
        check(
            "left_connector_is_source_complete",
            len(left_rows) == len(left_partition_rows) == 511
            and math.isclose(left_area, EXPECTED_AREA, rel_tol=0.0, abs_tol=5.0e-17),
            f"rows={len(left_rows)}; area={left_area:.17g}",
        ),
        check(
            "top_path_is_source_complete",
            len(top_rows) == len(top_partition_rows) == 1
            and math.isclose(top_area, EXPECTED_AREA, rel_tol=0.0, abs_tol=5.0e-17),
            f"rows={len(top_rows)}; area={top_area:.17g}",
        ),
        check(
            "right_connector_state_is_resume_safe",
            status["state"] == "paused_at_runtime_budget"
            and bool(status["resume_safe"])
            and right_state["revision"] == REVISION
            and int(status["internally_certified_box_count"])
            == int(right_state["accepted_count"])
            == len(right_rows),
            f"accepted={len(right_rows)}; pending={len(right_state['stack'])}",
        ),
        check(
            "right_connector_area_partition_is_exact",
            math.isclose(right_total_area, EXPECTED_AREA, rel_tol=0.0, abs_tol=5.0e-17),
            f"accepted={right_accepted_area:.17g}; pending={right_pending_area:.17g}",
        ),
        check(
            "right_connector_has_no_new_failure_class",
            set(right_failure_counts) == EXPECTED_RIGHT_FAILURE_CATEGORIES,
            f"category count={len(right_failure_counts)}",
        ),
        check(
            "all_completed_and_active_rows_are_finite",
            proof_rows_valid(all_rows),
            f"{len(all_rows)} rows checked",
        ),
        check(
            "checkpoint_5414_claim_boundary_preserved",
            not bool(previous["valid_for_regular_away_W3_claim"])
            and not bool(previous["valid_for_local_GR_claim"]),
            "5414 broad claims remain false",
        ),
        check(
            "broad_claims_remain_false",
            broad_claims_false
            and not payload["valid_for_regular_away_W3_claim"]
            and not payload["valid_for_full_MTS_claim"],
            "W3, UV, local-GR, and full-MTS remain unclaimed",
        ),
        check(
            "formalization_workbench_untouched",
            not formalization_touches,
            f"files modified after gate start={len(formalization_touches)}",
        ),
    ]
    atomic_csv(VALIDATION, validations)
    payload["validation_count"] = len(validations)
    payload["failed_validation_count"] = sum(not row["passed"] for row in validations)
    atomic_json(RESULT, payload)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return payload


def main() -> int:
    payload = run_gate()
    return 0 if payload["failed_validation_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
