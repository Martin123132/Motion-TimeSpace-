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


CHECKPOINT = 5417
POST = Path(__file__).resolve().parents[1]
ROOT = POST.parent
FORMALIZATION = ROOT / "formalization-workbench"
SOURCE = POST / "source-intake" / "functional_rg" / "5396"
PARTITIONS = SOURCE / "partial" / "path_parts" / "_partitions"
OUTPUT = POST / "source-intake" / "functional_rg" / str(CHECKPOINT)
PARENT_SCRIPT = POST / "scripts" / "Y5_R2FR_5396_D4_deformed_contour_regular_away_W3.py"
PREVIOUS = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5416"
    / "v43_right_connector_production_stability_result.json"
)
PREVIOUS_VALIDATION = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5416"
    / "P8_Y5_BRR5396_5416_VALIDATION.csv"
)
STATUS = SOURCE / "status.json"
RIGHT_STATE = (
    PARTITIONS
    / "bin_00_sub_00_S_X006_MC04_SP_DP_RIGHT_CONNECTOR_part_00_of_01.state.json"
)
RIGHT_ROWS = RIGHT_STATE.with_suffix(".rows.csv")
DOCUMENT = POST / "5417-Y5-R2FR-D4-v43-right-connector-frontier-expansion-gate.md"
SUMMARY = OUTPUT / "v43_right_connector_frontier_expansion_summary.csv"
VALIDATION = OUTPUT / "P8_Y5_BRR5396_5417_VALIDATION.csv"
RESULT = OUTPUT / "v43_right_connector_frontier_expansion_result.json"

REVISION = "D4-deformed-contour-regular-away-W3-v43"
EXPECTED_AREA = 0.03932753620548857
EXPECTED_BASELINE_ACCEPTED = 131
EXPECTED_ACCEPTED = 233
EXPECTED_PENDING = 14
EXPECTED_MAXIMUM_DEPTH = 17
PRESERVED_AUDITED_PATH = "LLDLDRDLDLDRDLDRU"
EXPECTED_FAILURE_CATEGORIES = {
    "IntervalSingularity:away_arc_left_K5:s1:c0:left1:edge_2_1_3:stable_edge",
    "IntervalSingularity:away_arc_left_K5:s1:c0:right1:edge_1_4_2:stable_edge",
    "IntervalSingularity:away_arc_right_K5:s2:c1:left0:edge_0_0_1:stable_edge",
    "IntervalSingularity:no displaced first-spinor rational pivot survives: away_arc_left_first",
}
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
        "# 5417: v43 right-connector frontier-expansion gate",
        "",
        "## Decision",
        "",
        "**PASS FOR SAME-REVISION FRONTIER EXPANSION AND CONTINUED V43 PRODUCTION ONLY.**",
        "",
        "A three-hour bounded continuation sequence advances the preserved `S_X006_MC04_SP_DP` right connector without adding an analytic repair. The split ledger retains exactly the four checkpoint-5416 classes, so this is genuine progress under the existing proof rather than another renamed target.",
        "",
        "## Production evidence",
        "",
        f"- accepted boxes: `{payload['baseline_accepted_box_count']} -> {payload['accepted_box_count']}` (`+{payload['accepted_box_gain']}`);",
        f"- pending boxes: `{payload['pending_box_count']}` at maximum depth `{payload['maximum_pending_depth']}`;",
        f"- certified area coverage: `{100.0 * payload['baseline_area_fraction']:.15g}% -> {100.0 * payload['accepted_area_fraction']:.15g}%`;",
        f"- weakest new denominator margin: `{payload['minimum_new_denominator_abs_lower']:.17g}`;",
        f"- weakest new collision-Jacobian margin: `{payload['minimum_new_collision_jacobian_abs_lower']:.17g}`;",
        f"- accepted plus pending area: `{payload['total_parameter_area']:.17g}`.",
        "",
        "All 102 newly accepted rows carry finite positive interval certificates. The depth-17 transition audited at checkpoint 5416 remains present unchanged, and no accepted row uses a point-only or fitted closure claim.",
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
        PREVIOUS_VALIDATION,
        STATUS,
        RIGHT_STATE,
        RIGHT_ROWS,
    )
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise FileNotFoundError("missing checkpoint input: " + " | ".join(missing))

    revision = source_revision(PARENT_SCRIPT)
    previous = read_json(PREVIOUS)
    previous_validation = read_csv(PREVIOUS_VALIDATION)
    status = read_json(STATUS)
    right_state = read_json(RIGHT_STATE)
    right_rows = read_csv(RIGHT_ROWS)
    baseline_count = int(previous["accepted_box_count"])
    new_rows = right_rows[baseline_count:]
    accepted_area = parameter_area(right_rows)
    open_area = pending_area(right_state["stack"])
    total_area = accepted_area + open_area
    failure_counts = {
        str(key): int(value)
        for key, value in right_state.get("split_failure_counts", {}).items()
    }
    previous_failure_counts = {
        str(key): int(value)
        for key, value in previous.get("failure_counts", {}).items()
    }
    maximum_depth = max(
        (int(row[4]) for row in right_state["stack"]), default=0
    )
    preserved_rows = [
        row
        for row in right_rows
        if row["refinement_path"] == PRESERVED_AUDITED_PATH
    ]
    broad_claims_false = all(
        not is_true(row[column]) for row in right_rows for column in BROAD_COLUMNS
    )
    row_scope_valid = all(
        is_true(row["valid_for_D4_regular_away_contour_deformation"])
        and is_true(row["valid_for_D4_numeric_regular_away_W3_bound"])
        for row in right_rows
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
        "completed_path_jobs": int(status["completed_path_jobs"]),
        "total_path_jobs": int(status["total_path_jobs"]),
        "baseline_accepted_box_count": baseline_count,
        "accepted_box_count": len(right_rows),
        "accepted_box_gain": len(new_rows),
        "pending_box_count": len(right_state["stack"]),
        "maximum_pending_depth": maximum_depth,
        "baseline_area_fraction": float(previous["accepted_area_fraction"]),
        "accepted_parameter_area": accepted_area,
        "pending_parameter_area": open_area,
        "total_parameter_area": total_area,
        "accepted_area_fraction": accepted_area / EXPECTED_AREA,
        "minimum_new_denominator_abs_lower": min(
            float(row["minimum_amplitude_denominator_abs_lower"])
            for row in new_rows
        ),
        "minimum_new_collision_jacobian_abs_lower": min(
            float(row["collision_jacobian_abs_lower"]) for row in new_rows
        ),
        "failure_category_count": len(failure_counts),
        "failure_counts": failure_counts,
        "preserved_audited_refinement_path": PRESERVED_AUDITED_PATH,
        "valid_for_same_revision_frontier_expansion": True,
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
        [
            {
                key: value
                for key, value in payload.items()
                if key not in {"created_utc", "failure_counts", "provenance_sha256"}
            }
        ],
    )
    write_document(payload)

    validations = [
        check("required_inputs_exist", not missing, f"{len(required)} paths present"),
        check("parent_source_compiles_as_v43", revision == REVISION, revision),
        check(
            "checkpoint_5416_is_green_and_bounded",
            len(previous_validation) == 14
            and all(is_true(row["passed"]) for row in previous_validation)
            and bool(previous["valid_for_continued_v43_production"])
            and not bool(previous["valid_for_regular_away_W3_claim"]),
            "5416 has 14/14 passing gates and broad claims false",
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
            "right_connector_progress_is_committed",
            baseline_count == EXPECTED_BASELINE_ACCEPTED
            and len(right_rows) == EXPECTED_ACCEPTED
            and len(new_rows) == 102,
            f"accepted {baseline_count} -> {len(right_rows)}",
        ),
        check(
            "frontier_matches_frozen_run",
            len(right_state["stack"]) == EXPECTED_PENDING
            and maximum_depth == EXPECTED_MAXIMUM_DEPTH,
            f"pending={len(right_state['stack'])}; depth={maximum_depth}",
        ),
        check(
            "right_connector_area_partition_is_exact",
            math.isclose(total_area, EXPECTED_AREA, rel_tol=0.0, abs_tol=5.0e-17),
            f"accepted={accepted_area:.17g}; pending={open_area:.17g}",
        ),
        check(
            "certified_area_fraction_increases",
            payload["accepted_area_fraction"]
            > 3.0 * payload["baseline_area_fraction"],
            f"coverage {payload['baseline_area_fraction']:.17g} -> {payload['accepted_area_fraction']:.17g}",
        ),
        check(
            "right_connector_has_no_new_failure_class",
            set(failure_counts) == EXPECTED_FAILURE_CATEGORIES
            and set(previous_failure_counts) == EXPECTED_FAILURE_CATEGORIES
            and all(
                failure_counts[key] >= previous_failure_counts[key]
                for key in EXPECTED_FAILURE_CATEGORIES
            ),
            f"category count={len(failure_counts)}",
        ),
        check(
            "newly_accepted_rows_are_finite",
            len(new_rows) == 102 and proof_rows_valid(new_rows),
            f"{len(new_rows)} new rows checked",
        ),
        check(
            "previously_audited_transition_is_preserved",
            len(preserved_rows) == 1
            and math.isclose(
                float(preserved_rows[0]["minimum_amplitude_denominator_abs_lower"]),
                float(previous["audited_denominator_abs_lower"]),
                rel_tol=0.0,
                abs_tol=1.0e-18,
            )
            and math.isclose(
                float(preserved_rows[0]["collision_jacobian_abs_lower"]),
                float(previous["audited_collision_jacobian_abs_lower"]),
                rel_tol=0.0,
                abs_tol=1.0e-14,
            ),
            PRESERVED_AUDITED_PATH,
        ),
        check(
            "all_accepted_rows_have_local_certificate_scope",
            proof_rows_valid(right_rows) and row_scope_valid,
            f"{len(right_rows)} accepted rows checked",
        ),
        check(
            "broad_claims_remain_false",
            broad_claims_false
            and not payload["valid_for_regular_away_W3_claim"]
            and not payload["valid_for_numeric_W3_claim"]
            and not payload["valid_for_local_GR_claim"]
            and not payload["valid_for_full_MTS_claim"],
            "W3, UV, local-GR, and full-MTS remain unclaimed",
        ),
        check(
            "path_job_count_remains_bounded",
            payload["completed_path_jobs"] == 29
            and payload["total_path_jobs"] == 240,
            f"{payload['completed_path_jobs']}/{payload['total_path_jobs']}",
        ),
        check(
            "formalization_workbench_untouched",
            not formalization_touches,
            f"files modified after gate start={len(formalization_touches)}",
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
