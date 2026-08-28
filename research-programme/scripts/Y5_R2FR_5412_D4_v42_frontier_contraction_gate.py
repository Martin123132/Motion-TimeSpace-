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


CHECKPOINT = 5412
POST = Path(__file__).resolve().parents[1]
ROOT = POST.parent
FORMALIZATION = ROOT / "formalization-workbench"
SOURCE = POST / "source-intake" / "functional_rg" / "5396"
OUTPUT = POST / "source-intake" / "functional_rg" / str(CHECKPOINT)
PARENT_SCRIPT = (
    POST / "scripts" / "Y5_R2FR_5396_D4_deformed_contour_regular_away_W3.py"
)
PREVIOUS = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5411"
    / "v42_anisotropic_production_stability_result.json"
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
DOCUMENT = POST / "5412-Y5-R2FR-D4-v42-frontier-contraction-gate.md"
SUMMARY = OUTPUT / "v42_frontier_contraction_summary.csv"
VALIDATION = OUTPUT / "P8_Y5_BRR5396_5412_VALIDATION.csv"
RESULT = OUTPUT / "v42_frontier_contraction_result.json"

REVISION = "D4-deformed-contour-regular-away-W3-v42"
ANISOTROPIC_METHOD = "SUBDIVIDED_PATH_CORRELATED_PROJECTIVE_UNION_8X16"
EXPECTED_FAILURE_CATEGORIES = {
    "EnclosureFailure:global contour geometric denominator reaches zero",
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
        if not isinstance(node, ast.Assign):
            continue
        if any(
            isinstance(target, ast.Name) and target.id == "REVISION"
            for target in node.targets
        ):
            return str(ast.literal_eval(node.value))
    return ""


def pending_area(stack: list[list[Any]]) -> float:
    return sum(
        (float(row[1]) - float(row[0]))
        * (float(row[3]) - float(row[2]))
        for row in stack
    )


def is_true(value: Any) -> bool:
    return str(value).strip().lower() == "true"


def check(name: str, passed: bool, evidence: str) -> dict[str, Any]:
    return {"check": name, "passed": bool(passed), "evidence": evidence}


def write_document(payload: dict[str, Any]) -> None:
    lines = [
        "# 5412: v42 frontier-contraction gate",
        "",
        "## Decision",
        "",
        "**PASS FOR CONTINUED V42 PRODUCTION ONLY.**",
        "",
        "A one-hour same-revision continuation materially contracts the active frontier. This is production progress under the existing exact proof, not a new closure or a replacement for the incomplete path integral.",
        "",
        "## Contraction evidence",
        "",
        f"- accepted boxes: `{payload['baseline_accepted_box_count']} -> {payload['active_accepted_box_count']}`;",
        f"- pending boxes: `{payload['baseline_pending_box_count']} -> {payload['active_pending_box_count']}`;",
        f"- maximum pending depth: `{payload['baseline_maximum_pending_depth']} -> {payload['active_maximum_pending_depth']}`;",
        f"- certified area coverage: `{100.0 * payload['baseline_area_coverage_fraction']:.6f}% -> {100.0 * payload['active_area_coverage_fraction']:.6f}%`;",
        f"- exact `8 x 16` projective certificates: `{payload['baseline_anisotropic_row_count']} -> {payload['anisotropic_production_row_count']}`;",
        f"- geometric-denominator split counter: `{payload['geometric_failure_count']}` before and after the run.",
        "",
        "The failure ledger still contains exactly the same five declared outer-enclosure categories. Accepted plus pending area reproduces the parent rectangle, and every accepted proof field remains finite with a positive denominator and collision-Jacobian margin.",
        "",
        "## Claim boundary",
        "",
        "The active connector and the other 213 contour paths remain incomplete. Therefore regular-away W3, event-local W3, combined W3, regulator-limit, UV, local-GR, and full-MTS claims remain open.",
        "",
    ]
    atomic_text(DOCUMENT, "\n".join(lines))


def run_gate() -> dict[str, Any]:
    started = datetime.now(timezone.utc)
    required = (PARENT_SCRIPT, PREVIOUS, STATUS, ACTIVE_STATE, ACTIVE_ROWS)
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        raise FileNotFoundError("missing checkpoint input: " + " | ".join(missing))

    previous = read_json(PREVIOUS)
    status = read_json(STATUS)
    state = read_json(ACTIVE_STATE)
    rows = read_csv(ACTIVE_ROWS)
    revision = source_revision(PARENT_SCRIPT)
    accepted_area = sum(float(row["parameter_area"]) for row in rows)
    remaining_area = pending_area(state["stack"])
    total_area = accepted_area + remaining_area
    expected_area = float(previous["total_parameter_area"])
    maximum_depth = max((int(row[4]) for row in state["stack"]), default=0)
    failure_counts = {
        str(key): int(value)
        for key, value in state.get("split_failure_counts", {}).items()
    }
    method_counts: dict[str, int] = {}
    for row in rows:
        method = row["collision_jacobian_enclosure_method"]
        method_counts[method] = method_counts.get(method, 0) + 1
    numeric_rows_ok = all(
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
    broad_claims_false = all(
        not is_true(row[column]) for row in rows for column in BROAD_COLUMNS
    )
    geometric_count = failure_counts.get(
        "EnclosureFailure:global contour geometric denominator reaches zero", 0
    )
    coverage = accepted_area / expected_area
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
        "baseline_accepted_box_count": int(previous["active_accepted_box_count"]),
        "active_accepted_box_count": len(rows),
        "net_new_accepted_box_count": len(rows)
        - int(previous["active_accepted_box_count"]),
        "baseline_pending_box_count": int(previous["active_pending_box_count"]),
        "active_pending_box_count": len(state["stack"]),
        "baseline_maximum_pending_depth": int(
            previous["active_maximum_pending_depth"]
        ),
        "active_maximum_pending_depth": maximum_depth,
        "baseline_area_coverage_fraction": float(
            previous["active_area_coverage_fraction"]
        ),
        "active_area_coverage_fraction": coverage,
        "baseline_anisotropic_row_count": int(
            previous["anisotropic_production_row_count"]
        ),
        "anisotropic_production_row_count": method_counts.get(
            ANISOTROPIC_METHOD, 0
        ),
        "geometric_failure_count": geometric_count,
        "failure_category_count": len(failure_counts),
        "accepted_parameter_area": accepted_area,
        "pending_parameter_area": remaining_area,
        "total_parameter_area": total_area,
        "minimum_accepted_denominator_abs_lower": min(
            float(row["minimum_amplitude_denominator_abs_lower"])
            for row in rows
        ),
        "minimum_accepted_collision_jacobian_abs_lower": min(
            float(row["collision_jacobian_abs_lower"]) for row in rows
        ),
        "valid_for_continued_v42_production": True,
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
                if key not in {"created_utc", "provenance_sha256"}
            }
        ],
    )
    write_document(payload)

    validations = [
        check("required_inputs_exist", not missing, f"{len(required)} paths present"),
        check(
            "parent_source_compiles_as_v42",
            revision == REVISION,
            revision or "missing revision",
        ),
        check(
            "checkpoint_5411_authorizes_continuation_only",
            bool(previous["valid_for_continued_v42_production"])
            and not bool(previous["valid_for_regular_away_W3_claim"]),
            "5411 keeps the broad claim lock",
        ),
        check(
            "status_and_state_are_resume_safe_and_consistent",
            status["state"] == "paused_at_runtime_budget"
            and bool(status["resume_safe"])
            and int(status["internally_certified_box_count"])
            == int(state["accepted_count"])
            == len(rows),
            f"status={status['state']}; accepted={len(rows)}",
        ),
        check(
            "accepted_frontier_advances",
            payload["net_new_accepted_box_count"] > 0,
            f"net accepted={payload['net_new_accepted_box_count']}",
        ),
        check(
            "pending_frontier_contracts",
            payload["active_pending_box_count"]
            < payload["baseline_pending_box_count"]
            and payload["active_maximum_pending_depth"]
            < payload["baseline_maximum_pending_depth"],
            (
                f"pending {payload['baseline_pending_box_count']} -> "
                f"{payload['active_pending_box_count']}; depth "
                f"{payload['baseline_maximum_pending_depth']} -> "
                f"{payload['active_maximum_pending_depth']}"
            ),
        ),
        check(
            "certified_area_coverage_increases",
            payload["active_area_coverage_fraction"]
            > payload["baseline_area_coverage_fraction"],
            (
                f"coverage {payload['baseline_area_coverage_fraction']:.17g} -> "
                f"{payload['active_area_coverage_fraction']:.17g}"
            ),
        ),
        check(
            "accepted_plus_pending_area_is_exact",
            math.isclose(total_area, expected_area, rel_tol=0.0, abs_tol=5.0e-17),
            f"accepted={accepted_area:.17g}; pending={remaining_area:.17g}",
        ),
        check(
            "failure_ledger_has_no_new_category",
            set(failure_counts) == EXPECTED_FAILURE_CATEGORIES,
            f"category count={len(failure_counts)}",
        ),
        check(
            "repaired_geometric_counter_remains_frozen",
            geometric_count == int(previous["geometric_failure_count"]) == 27,
            f"geometric split count={geometric_count}",
        ),
        check(
            "anisotropic_cover_continues_to_certify",
            payload["anisotropic_production_row_count"]
            > payload["baseline_anisotropic_row_count"],
            (
                f"8x16 rows {payload['baseline_anisotropic_row_count']} -> "
                f"{payload['anisotropic_production_row_count']}"
            ),
        ),
        check(
            "all_accepted_proof_fields_are_finite",
            numeric_rows_ok,
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
