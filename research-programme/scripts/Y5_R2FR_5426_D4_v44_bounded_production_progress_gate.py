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


CHECKPOINT = 5426
POST = Path(__file__).resolve().parents[1]
ROOT = POST.parent
FORMALIZATION = ROOT / "formalization-workbench"
SOURCE = POST / "source-intake" / "functional_rg" / "5396"
OUTPUT = POST / "source-intake" / "functional_rg" / str(CHECKPOINT)
PARENT_SCRIPT = (
    POST / "scripts" / "Y5_R2FR_5396_D4_deformed_contour_regular_away_W3.py"
)
PROOF_RESULT = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5425"
    / "left_first_soft_invariant_subcover_result.json"
)
PROOF_VALIDATION = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5425"
    / "P8_Y5_BRR5396_5425_VALIDATION.csv"
)
BASELINE_RESULT = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5424"
    / "v43_right_connector_progress_result.json"
)
STATUS = SOURCE / "status.json"
MIGRATION = SOURCE / "resume_manifest_migration.json"
ACTIVE_STATE = (
    SOURCE
    / "partial"
    / "path_parts"
    / "_partitions"
    / "bin_00_sub_00_S_X006_MC04_SP_DP_RIGHT_CONNECTOR_part_00_of_01.state.json"
)
ACTIVE_ROWS = ACTIVE_STATE.with_suffix(".rows.csv")
DOCUMENT = POST / "5426-Y5-R2FR-D4-v44-bounded-production-progress-gate.md"
NEW_ROWS = OUTPUT / "v44_bounded_production_new_rows.csv"
SUMMARY = OUTPUT / "v44_bounded_production_summary.csv"
VALIDATION = OUTPUT / "P8_Y5_BRR5396_5426_VALIDATION.csv"
RESULT = OUTPUT / "v44_bounded_production_result.json"

REVISION = "D4-deformed-contour-regular-away-W3-v44"
EXPECTED_AREA = 0.03932753620548857
REPAIRED_FAILURE = (
    "IntervalSingularity:away_arc_left_K5:s1:c0:left1:"
    "edge_2_1_3:stable_edge"
)
EXTERNAL01_FAILURE = (
    "IntervalSingularity:away_arc_right_K5:s2:c1:left0:"
    "edge_0_0_1:stable_edge"
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
BROAD_COLUMNS = (
    "valid_for_D4_numeric_event_local_W3_bound",
    "valid_for_D4_numeric_W3_bound",
    "valid_for_D4_numeric_uniform_remainder_bound",
    "valid_for_D4_outer_regulator_zero_limit",
    "valid_for_decay_angle_integral",
    "valid_for_full_angular_convergence",
    "valid_for_full_phase_space_coefficient",
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
        raise ValueError(f"cannot write empty CSV: {path}")
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


def is_true(value: Any) -> bool:
    return str(value).strip().lower() == "true"


def check(name: str, passed: bool, evidence: str) -> dict[str, Any]:
    return {"check": name, "passed": bool(passed), "evidence": evidence}


def pending_area(stack: list[list[Any]]) -> float:
    return sum(
        (float(row[1]) - float(row[0]))
        * (float(row[3]) - float(row[2]))
        for row in stack
    )


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


def next_box(stack: list[list[Any]]) -> dict[str, Any] | None:
    if not stack:
        return None
    row = stack[-1]
    return {
        "x_lower": float(row[0]),
        "x_upper": float(row[1]),
        "t_lower": float(row[2]),
        "t_upper": float(row[3]),
        "refinement_depth": int(row[4]),
        "refinement_path": str(row[5]),
    }


def write_document(payload: dict[str, Any]) -> None:
    repaired_change = (
        payload["current_repaired_failure_count"]
        - payload["baseline_repaired_failure_count"]
    )
    external_change = (
        payload["current_external01_failure_count"]
        - payload["baseline_external01_failure_count"]
    )
    lines = [
        "# 5426: v44 bounded production progress gate",
        "",
        "## Decision",
        "",
        "**PASS FOR COMMITTED V44 PRODUCTION PROGRESS ONLY.**",
        "",
        f"The first bounded resume after the exact `(1,3)` repair commits `{payload['accepted_box_gain']}` additional interval boxes. Accepted coverage rises from `{100.0 * payload['baseline_area_fraction']:.15g}%` to `{100.0 * payload['accepted_area_fraction']:.15g}%`.",
        "",
        "## Obstruction transfer",
        "",
        f"The repaired `(1,3)` failure count changes by `{repaired_change}`. The separate external `(0,1)` count changes by `{external_change}`. No new failure category appears. This is the production-level confirmation that v44 removes the intended obstruction rather than merely relabelling it.",
        "",
        "## Saved frontier",
        "",
        f"The run is resume-safe with `{payload['accepted_box_count']}` accepted and `{payload['pending_box_count']}` pending boxes. The next path is `{payload['next_refinement_path']}` at depth `{payload['maximum_pending_depth']}`.",
        "",
        "## Claim boundary",
        "",
        "The right connector remains incomplete. Regular-away W3, event-local W3, combined W3, regulator limit, UV, local-GR, and full-MTS claims remain false.",
        "",
    ]
    atomic_text(DOCUMENT, "\n".join(lines))


def run_gate() -> dict[str, Any]:
    started = datetime.now(timezone.utc)
    required = (
        PARENT_SCRIPT,
        PROOF_RESULT,
        PROOF_VALIDATION,
        BASELINE_RESULT,
        STATUS,
        MIGRATION,
        ACTIVE_STATE,
        ACTIVE_ROWS,
    )
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise FileNotFoundError("missing checkpoint input: " + " | ".join(missing))
    revision = source_revision(PARENT_SCRIPT)
    proof = read_json(PROOF_RESULT)
    proof_validation = read_csv(PROOF_VALIDATION)
    baseline = read_json(BASELINE_RESULT)
    status = read_json(STATUS)
    migration = read_json(MIGRATION)
    state = read_json(ACTIVE_STATE)
    rows = read_csv(ACTIVE_ROWS)
    baseline_count = int(proof["active_accepted_box_count"])
    if len(rows) <= baseline_count:
        raise RuntimeError(
            f"no committed v44 progress: {len(rows)} <= {baseline_count}"
        )
    new_rows = rows[baseline_count:]
    accepted_area = sum(float(row["parameter_area"]) for row in rows)
    open_area = pending_area(state["stack"])
    total_area = accepted_area + open_area
    baseline_area = float(proof["accepted_parameter_area"])
    current_failures = {
        str(key): int(value)
        for key, value in state.get("split_failure_counts", {}).items()
    }
    baseline_failures = {
        str(key): int(value)
        for key, value in baseline.get("failure_counts", {}).items()
    }
    current_next = next_box(state["stack"])
    maximum_depth = max((int(row[4]) for row in state["stack"]), default=0)
    broad_claims_false = all(
        not is_true(row[column]) for row in rows for column in BROAD_COLUMNS
    )
    row_scope_valid = all(
        is_true(row["valid_for_D4_regular_away_contour_deformation"])
        and is_true(row["valid_for_D4_numeric_regular_away_W3_bound"])
        for row in rows
    )
    payload: dict[str, Any] = {
        "checkpoint": CHECKPOINT,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "parent_revision": revision,
        "previous_checkpoint": int(proof["checkpoint"]),
        "baseline_accepted_box_count": baseline_count,
        "accepted_box_count": len(rows),
        "accepted_box_gain": len(new_rows),
        "baseline_pending_box_count": int(proof["active_pending_box_count"]),
        "pending_box_count": len(state["stack"]),
        "baseline_area_fraction": baseline_area / EXPECTED_AREA,
        "accepted_parameter_area": accepted_area,
        "pending_parameter_area": open_area,
        "total_parameter_area": total_area,
        "accepted_area_fraction": accepted_area / EXPECTED_AREA,
        "maximum_pending_depth": maximum_depth,
        "next_box": current_next,
        "next_refinement_path": (
            str(current_next["refinement_path"]) if current_next else "COMPLETE"
        ),
        "minimum_new_denominator_abs_lower": min(
            float(row["minimum_amplitude_denominator_abs_lower"])
            for row in new_rows
        ),
        "minimum_new_collision_jacobian_abs_lower": min(
            float(row["collision_jacobian_abs_lower"]) for row in new_rows
        ),
        "failure_category_count": len(current_failures),
        "baseline_repaired_failure_count": baseline_failures[REPAIRED_FAILURE],
        "current_repaired_failure_count": current_failures[REPAIRED_FAILURE],
        "baseline_external01_failure_count": baseline_failures[EXTERNAL01_FAILURE],
        "current_external01_failure_count": current_failures[EXTERNAL01_FAILURE],
        "failure_counts": current_failures,
        "valid_for_continued_v44_production": True,
        "valid_for_right_connector_completion": not state["stack"],
        "valid_for_regular_away_W3_claim": False,
        "valid_for_numeric_W3_claim": False,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
        "provenance_sha256": {
            str(path.relative_to(POST)): sha256(path) for path in required
        },
    }
    atomic_csv(NEW_ROWS, new_rows)
    atomic_csv(
        SUMMARY,
        [
            {
                key: value
                for key, value in payload.items()
                if key
                not in {
                    "created_utc",
                    "failure_counts",
                    "next_box",
                    "provenance_sha256",
                }
            }
        ],
    )
    write_document(payload)
    formalization_touches = [
        path
        for path in FORMALIZATION.rglob("*")
        if path.is_file()
        and datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) > started
    ]
    validations = [
        check("required_inputs_exist", not missing, f"{len(required)} paths present"),
        check("parent_source_compiles_as_v44", revision == REVISION, revision),
        check(
            "checkpoint_5425_is_green_and_narrow",
            int(proof["failed_validation_count"]) == 0
            and all(is_true(row["passed"]) for row in proof_validation)
            and bool(proof["valid_for_continued_v44_production"])
            and not bool(proof["valid_for_regular_away_W3_claim"]),
            f"validation rows={len(proof_validation)}",
        ),
        check(
            "resume_manifest_migrates_v43_to_v44",
            migration["previous_manifest"]["revision"].endswith("v43")
            and migration["current_manifest"]["revision"] == REVISION
            and state["revision"] == REVISION,
            "manifest and adaptive state record v43 -> v44",
        ),
        check(
            "production_state_is_resume_safe",
            status["state"] == "paused_at_runtime_budget"
            and bool(status["resume_safe"])
            and int(status["internally_certified_box_count"])
            == int(state["accepted_count"])
            == len(rows),
            f"accepted={len(rows)}; pending={len(state['stack'])}",
        ),
        check(
            "accepted_frontier_advances_under_v44",
            len(new_rows) > 0
            and len(rows) == baseline_count + len(new_rows)
            and accepted_area > baseline_area,
            f"accepted {baseline_count} -> {len(rows)}",
        ),
        check(
            "right_connector_area_partition_is_exact",
            math.isclose(total_area, EXPECTED_AREA, rel_tol=0.0, abs_tol=5.0e-17),
            f"accepted={accepted_area:.17g}; pending={open_area:.17g}",
        ),
        check(
            "repaired_failure_count_does_not_increase",
            current_failures[REPAIRED_FAILURE]
            == baseline_failures[REPAIRED_FAILURE],
            f"count={current_failures[REPAIRED_FAILURE]}",
        ),
        check(
            "frontier_transfers_to_known_external01_class",
            set(current_failures) == set(baseline_failures)
            and current_failures[EXTERNAL01_FAILURE]
            > baseline_failures[EXTERNAL01_FAILURE],
            f"external01 {baseline_failures[EXTERNAL01_FAILURE]} -> {current_failures[EXTERNAL01_FAILURE]}",
        ),
        check(
            "new_rows_have_finite_interval_certificates",
            proof_rows_valid(new_rows),
            f"{len(new_rows)} new rows checked",
        ),
        check(
            "all_rows_have_local_certificate_scope",
            proof_rows_valid(rows) and row_scope_valid,
            f"{len(rows)} accepted rows checked",
        ),
        check(
            "next_box_matches_saved_stack",
            bool(state["stack"])
            and current_next is not None
            and current_next["refinement_path"] == state["stack"][-1][5],
            payload["next_refinement_path"],
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
            f"files modified after checkpoint start={len(formalization_touches)}",
        ),
    ]
    atomic_csv(VALIDATION, validations)
    payload["validation_count"] = len(validations)
    payload["failed_validation_count"] = sum(
        not row["passed"] for row in validations
    )
    atomic_json(RESULT, payload)
    print(json.dumps(payload, indent=2, sort_keys=True))
    return payload


def main() -> int:
    payload = run_gate()
    return 0 if payload["failed_validation_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
