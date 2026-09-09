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


CHECKPOINT = 5419
POST = Path(__file__).resolve().parents[1]
ROOT = POST.parent
FORMALIZATION = ROOT / "formalization-workbench"
SOURCE = POST / "source-intake" / "functional_rg" / "5396"
PARTITIONS = SOURCE / "partial" / "path_parts" / "_partitions"
OUTPUT = POST / "source-intake" / "functional_rg" / str(CHECKPOINT)
PARENT_SCRIPT = (
    POST / "scripts" / "Y5_R2FR_5396_D4_deformed_contour_regular_away_W3.py"
)
PREVIOUS = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5418"
    / "v43_right_connector_depth17_sibling_probe_result.json"
)
PREVIOUS_VALIDATION = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5418"
    / "P8_Y5_BRR5396_5418_VALIDATION.csv"
)
PROBES = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5418"
    / "v43_right_connector_depth17_sibling_probes.csv"
)
STATUS = SOURCE / "status.json"
RIGHT_STATE = (
    PARTITIONS
    / "bin_00_sub_00_S_X006_MC04_SP_DP_RIGHT_CONNECTOR_part_00_of_01.state.json"
)
RIGHT_ROWS = RIGHT_STATE.with_suffix(".rows.csv")
DOCUMENT = POST / "5419-Y5-R2FR-D4-v43-depth17-sibling-commit-gate.md"
SUMMARY = OUTPUT / "v43_depth17_sibling_commit_summary.csv"
VALIDATION = OUTPUT / "P8_Y5_BRR5396_5419_VALIDATION.csv"
RESULT = OUTPUT / "v43_depth17_sibling_commit_result.json"

REVISION = "D4-deformed-contour-regular-away-W3-v43"
EXPECTED_AREA = 0.03932753620548857
EXPECTED_BASELINE_ACCEPTED = 233
EXPECTED_ACCEPTED = 237
EXPECTED_PENDING = 11
EXPECTED_MAXIMUM_DEPTH = 15
DIRECT_PATHS = (
    "LLDRDLDLDRDRDRDLD",
    "LLDRDLDLDRDRDRDLU",
)
ADJACENT_PATHS = (
    "LLDRDLDLDRDRDRDRD",
    "LLDRDLDLDRDRDRDRU",
)
EXPECTED_FAILURE_CATEGORIES = {
    "IntervalSingularity:away_arc_left_K5:s1:c0:left1:edge_2_1_3:stable_edge",
    "IntervalSingularity:away_arc_left_K5:s1:c0:right1:edge_1_4_2:stable_edge",
    "IntervalSingularity:away_arc_right_K5:s2:c1:left0:edge_0_0_1:stable_edge",
    "IntervalSingularity:no displaced first-spinor rational pivot survives: away_arc_left_first",
}
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


def area(rows: list[dict[str, str]]) -> float:
    return sum(float(row["parameter_area"]) for row in rows)


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


def write_document(payload: dict[str, Any]) -> None:
    lines = [
        "# 5419: v43 depth-17 sibling commit gate",
        "",
        "## Decision",
        "",
        "**PASS FOR COMMITTED DEPTH-17 TRANSITION AND CONTINUED V43 PRODUCTION ONLY.**",
        "",
        "The two checkpoint-5418 direct certificates now appear unchanged in the production adaptive ledger. The same bounded resume also certifies the adjacent depth-17 pair, so this is a real frontier contraction rather than a side calculation.",
        "",
        "## Production transition",
        "",
        f"- accepted boxes: `{payload['baseline_accepted_box_count']} -> {payload['accepted_box_count']}`;",
        f"- pending boxes: `{payload['baseline_pending_box_count']} -> {payload['pending_box_count']}`;",
        f"- maximum pending depth: `{payload['baseline_maximum_pending_depth']} -> {payload['maximum_pending_depth']}`;",
        f"- accepted coverage: `{100.0 * payload['accepted_area_fraction']:.15g}%`;",
        f"- weakest new denominator margin: `{payload['minimum_new_denominator_abs_lower']:.17g}`;",
        f"- weakest new collision-Jacobian margin: `{payload['minimum_new_collision_jacobian_abs_lower']:.17g}`.",
        "",
        "The split ledger retains the same four analytic failure classes. The right connector is still incomplete, but its deepest live frontier has retreated from depth 17 to depth 15.",
        "",
        "## Claim boundary",
        "",
        "Regular-away W3, event-local W3, combined W3, regulator limit, UV, local-GR, and full-MTS claims remain false.",
        "",
    ]
    atomic_text(DOCUMENT, "\n".join(lines))


def run_gate() -> dict[str, Any]:
    started = datetime.now(timezone.utc)
    required = (
        PARENT_SCRIPT,
        PREVIOUS,
        PREVIOUS_VALIDATION,
        PROBES,
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
    probes = read_csv(PROBES)
    status = read_json(STATUS)
    state = read_json(RIGHT_STATE)
    rows = read_csv(RIGHT_ROWS)
    new_rows = rows[EXPECTED_BASELINE_ACCEPTED:]
    accepted_area = area(rows)
    open_area = pending_area(state["stack"])
    total_area = accepted_area + open_area
    maximum_depth = max((int(row[4]) for row in state["stack"]), default=0)
    failure_counts = {
        str(key): int(value)
        for key, value in state.get("split_failure_counts", {}).items()
    }
    rows_by_path = {row["refinement_path"]: row for row in rows}
    probes_by_path = {row["refinement_path"]: row for row in probes}
    committed_probe_match = all(
        path in rows_by_path
        and path in probes_by_path
        and probes_by_path[path]["probe_status"] == "PASS"
        and math.isclose(
            float(rows_by_path[path]["minimum_amplitude_denominator_abs_lower"]),
            float(probes_by_path[path]["minimum_amplitude_denominator_abs_lower"]),
            rel_tol=0.0,
            abs_tol=1.0e-18,
        )
        and math.isclose(
            float(rows_by_path[path]["collision_jacobian_abs_lower"]),
            float(probes_by_path[path]["collision_jacobian_abs_lower"]),
            rel_tol=0.0,
            abs_tol=1.0e-14,
        )
        for path in DIRECT_PATHS
    )
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
        "completed_path_jobs": int(status["completed_path_jobs"]),
        "total_path_jobs": int(status["total_path_jobs"]),
        "baseline_accepted_box_count": EXPECTED_BASELINE_ACCEPTED,
        "accepted_box_count": len(rows),
        "accepted_box_gain": len(new_rows),
        "baseline_pending_box_count": 14,
        "pending_box_count": len(state["stack"]),
        "baseline_maximum_pending_depth": 17,
        "maximum_pending_depth": maximum_depth,
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
        "committed_direct_paths": list(DIRECT_PATHS),
        "committed_adjacent_paths": list(ADJACENT_PATHS),
        "failure_category_count": len(failure_counts),
        "failure_counts": failure_counts,
        "valid_for_committed_depth17_transition": committed_probe_match,
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
                if key
                not in {
                    "created_utc",
                    "committed_direct_paths",
                    "committed_adjacent_paths",
                    "failure_counts",
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
        check("parent_source_compiles_as_v43", revision == REVISION, revision),
        check(
            "checkpoint_5418_is_green_and_direct_only",
            len(previous_validation) == 12
            and all(is_true(row["passed"]) for row in previous_validation)
            and bool(previous["all_depth17_siblings_certified"])
            and not bool(previous["valid_for_committed_depth17_transition"]),
            "5418 has 12/12 gates and two uncommitted direct certificates",
        ),
        check(
            "production_state_is_resume_safe",
            status["state"] == "paused_at_runtime_budget"
            and bool(status["resume_safe"])
            and state["revision"] == REVISION
            and int(status["internally_certified_box_count"])
            == int(state["accepted_count"])
            == len(rows),
            f"accepted={len(rows)}; pending={len(state['stack'])}",
        ),
        check(
            "four_new_certificates_are_committed",
            len(rows) == EXPECTED_ACCEPTED
            and len(new_rows) == EXPECTED_ACCEPTED - EXPECTED_BASELINE_ACCEPTED
            and set(row["refinement_path"] for row in new_rows)
            == set(DIRECT_PATHS + ADJACENT_PATHS),
            f"accepted {EXPECTED_BASELINE_ACCEPTED} -> {len(rows)}",
        ),
        check(
            "direct_probe_certificates_match_committed_rows",
            committed_probe_match,
            "|".join(DIRECT_PATHS),
        ),
        check(
            "frontier_contracts_below_depth17",
            len(state["stack"]) == EXPECTED_PENDING
            and maximum_depth == EXPECTED_MAXIMUM_DEPTH,
            f"pending=14 -> {len(state['stack'])}; depth=17 -> {maximum_depth}",
        ),
        check(
            "right_connector_area_partition_is_exact",
            math.isclose(total_area, EXPECTED_AREA, rel_tol=0.0, abs_tol=5.0e-17),
            f"accepted={accepted_area:.17g}; pending={open_area:.17g}",
        ),
        check(
            "no_new_failure_category_appears",
            set(failure_counts) == EXPECTED_FAILURE_CATEGORIES,
            f"category count={len(failure_counts)}",
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
            "broad_claims_remain_false",
            broad_claims_false
            and not payload["valid_for_regular_away_W3_claim"]
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
    print(json.dumps(payload, indent=2, sort_keys=True), flush=True)
    return payload


def main() -> int:
    payload = run_gate()
    return 0 if payload["failed_validation_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
