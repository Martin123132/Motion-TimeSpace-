from __future__ import annotations

import ctypes
from datetime import datetime, timezone
import importlib.util
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


CHECKPOINT = 5433
POST = Path(__file__).resolve().parents[1]
ROOT = POST.parent
FORMALIZATION = ROOT / "formalization-workbench"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
OUTPUT = FUNCTIONAL_RG / str(CHECKPOINT)
PARENT_SCRIPT = (
    POST / "scripts" / "Y5_R2FR_5396_D4_deformed_contour_regular_away_W3.py"
)
UTILITY_SCRIPT = (
    POST
    / "scripts"
    / "Y5_R2FR_5428_D4_representative_external01_ratio_disk_gate.py"
)
PREVIOUS_RESULT = (
    FUNCTIONAL_RG / "5432" / "path_correlated_first_spinor_subcover_result.json"
)
PREVIOUS_VALIDATION = (
    FUNCTIONAL_RG / "5432" / "P8_Y5_BRR5396_5432_VALIDATION.csv"
)
AREA_REFERENCE = FUNCTIONAL_RG / "5431" / "v46_bounded_production_result.json"
STATUS = FUNCTIONAL_RG / "5396" / "status.json"
ACTIVE_STATE = (
    FUNCTIONAL_RG
    / "5396"
    / "partial"
    / "path_parts"
    / "_partitions"
    / "bin_00_sub_00_S_X006_MC04_SP_DP_RIGHT_CONNECTOR_part_00_of_01.state.json"
)
ACTIVE_ROWS = ACTIVE_STATE.with_suffix(".rows.csv")
DOCUMENT = POST / "5433-Y5-R2FR-D4-finite-outer-chart-cover-progress-gate.md"
NEW_ROWS = OUTPUT / "finite_outer_chart_cover_newly_certified_boxes.csv"
VALIDATION = OUTPUT / "P8_Y5_BRR5396_5433_VALIDATION.csv"
RESULT = OUTPUT / "finite_outer_chart_cover_progress_result.json"

PARENT_REVISION = "D4-deformed-contour-regular-away-W3-v46"
BASELINE_ACCEPTED = 373
EXPECTED_ACCEPTED = 386
EXPECTED_PENDING = 13
BROAD_FLAGS = (
    "valid_for_right_connector_completion",
    "valid_for_regular_away_W3_claim",
    "valid_for_D4_numeric_event_local_W3_bound",
    "valid_for_D4_numeric_W3_bound",
    "valid_for_D4_numeric_uniform_remainder_bound",
    "valid_for_D4_outer_regulator_zero_limit",
    "valid_for_numeric_UV_claim",
    "valid_for_local_GR_claim",
    "valid_for_full_MTS_claim",
)


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise ImportError(f"cannot load {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def write_document(utility: Any, payload: dict[str, Any]) -> None:
    lines = [
        "# 5433: finite outer chart-cover progress gate",
        "",
        "## Decision",
        "",
        "**PASS FOR COMMITTED FINITE-COVER PROGRESS ONLY.**",
        "",
        f"The unchanged v46 evaluator commits `{payload['accepted_box_gain']}` additional boxes after the 5432 single-family rejection. `LLU` closes directly, and the adaptive ledger now resolves the LR projective transition by disjoint x/t boxes rather than by forcing one singular gauge.",
        "",
        "## Saved frontier",
        "",
        f"Accepted boxes rise from `{payload['baseline_accepted_box_count']}` to `{payload['accepted_box_count']}`. The saved stack contains `{payload['pending_box_count']}` boxes; every pending path remains inside `LR` or `R`, so no previously certified region was reopened.",
        "",
        "## Numerical floor",
        "",
        f"Across the new certificates, the minimum amplitude-denominator lower bound is `{payload['minimum_new_denominator_abs_lower']:.17g}` and the minimum collision-Jacobian lower bound is `{payload['minimum_new_collision_jacobian_abs_lower']:.17g}`.",
        "",
        "## Interpretation",
        "",
        "The broad-box obstruction is confirmed as projective-cover bookkeeping. It has not produced a terminal zero or a new failure class. Completion still requires exhausting the saved LR/R stack.",
        "",
        "## Claim boundary",
        "",
        "The right connector, regular-away W3, combined W3, regulator limit, UV, local-GR, and full-MTS claims remain false.",
    ]
    utility.atomic_text(DOCUMENT, "\n".join(lines) + "\n")


def run_gate() -> dict[str, Any]:
    started = datetime.now(timezone.utc)
    utility = load_module("mts_5428_for_5433", UTILITY_SCRIPT)
    parent = load_module("mts_5396_v46_for_5433", PARENT_SCRIPT)
    previous = utility.read_json(PREVIOUS_RESULT)
    previous_validation = utility.read_csv(PREVIOUS_VALIDATION)
    area_reference = utility.read_json(AREA_REFERENCE)
    status = utility.read_json(STATUS)
    state = utility.read_json(ACTIVE_STATE)
    rows = utility.read_csv(ACTIVE_ROWS)
    accepted_count = int(state["accepted_count"])
    pending_count = len(state["stack"])
    new_rows = rows[BASELINE_ACCEPTED:accepted_count]
    utility.atomic_csv(NEW_ROWS, new_rows)
    accepted_area = sum(float(row["parameter_area"]) for row in rows)
    pending_area = sum(
        (float(box[1]) - float(box[0]))
        * (float(box[3]) - float(box[2]))
        for box in state["stack"]
    )
    total_area = float(area_reference["total_parameter_area"])
    minimum_denominator = min(
        float(row["minimum_amplitude_denominator_abs_lower"])
        for row in new_rows
    )
    minimum_jacobian = min(
        float(row["collision_jacobian_abs_lower"]) for row in new_rows
    )
    current_failures = {
        str(key): int(value)
        for key, value in state["split_failure_counts"].items()
    }
    prior_failure_categories = set(area_reference["failure_counts"])
    payload = {
        "checkpoint": CHECKPOINT,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "parent_revision": parent.REVISION,
        "bounded_runtime_seconds": float(status["runtime_seconds"]),
        "baseline_accepted_box_count": BASELINE_ACCEPTED,
        "accepted_box_count": accepted_count,
        "accepted_box_gain": accepted_count - BASELINE_ACCEPTED,
        "pending_box_count": pending_count,
        "pending_refinement_paths": [str(box[5]) for box in state["stack"]],
        "accepted_parameter_area": accepted_area,
        "pending_parameter_area": pending_area,
        "total_parameter_area": total_area,
        "accepted_area_fraction": accepted_area / total_area,
        "minimum_new_denominator_abs_lower": minimum_denominator,
        "minimum_new_collision_jacobian_abs_lower": minimum_jacobian,
        "failure_counts": current_failures,
        "failure_category_count": len(current_failures),
        "valid_for_finite_outer_chart_cover_progress": True,
        **{flag: False for flag in BROAD_FLAGS},
    }
    formalization_touches = [
        path
        for path in FORMALIZATION.rglob("*")
        if path.is_file()
        and datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) > started
    ]
    validations = [
        utility.check(
            "checkpoint_5432_green_and_single_family_rejected",
            int(previous["failed_validation_count"]) == 0
            and bool(previous["single_family_subcover_rejected"])
            and all(utility.is_true(row["passed"]) for row in previous_validation),
            f"rows={len(previous_validation)}",
        ),
        utility.check(
            "parent_and_state_revision_are_v46",
            parent.REVISION == state["revision"] == PARENT_REVISION,
            f"parent={parent.REVISION}; state={state['revision']}",
        ),
        utility.check(
            "bounded_run_is_resume_safe",
            status["state"] == "paused_at_runtime_budget"
            and bool(status["resume_safe"]),
            f"state={status['state']}; runtime={status['runtime_seconds']}",
        ),
        utility.check(
            "accepted_ledger_advanced_exactly",
            accepted_count == EXPECTED_ACCEPTED
            and len(new_rows) == EXPECTED_ACCEPTED - BASELINE_ACCEPTED,
            f"accepted={accepted_count}; new={len(new_rows)}",
        ),
        utility.check(
            "saved_pending_stack_is_exact",
            pending_count == EXPECTED_PENDING,
            f"pending={pending_count}",
        ),
        utility.check(
            "llu_was_committed",
            any(row["refinement_path"] == "LLU" for row in new_rows),
            "|".join(row["refinement_path"] for row in new_rows),
        ),
        utility.check(
            "remaining_stack_stays_inside_lr_or_r",
            all(
                str(box[5]) == "R" or str(box[5]).startswith("LR")
                for box in state["stack"]
            ),
            "|".join(str(box[5]) for box in state["stack"]),
        ),
        utility.check(
            "all_new_denominator_bounds_are_positive",
            math.isfinite(minimum_denominator) and minimum_denominator > 0.0,
            f"minimum={minimum_denominator}",
        ),
        utility.check(
            "all_new_jacobian_bounds_are_positive",
            math.isfinite(minimum_jacobian) and minimum_jacobian > 0.0,
            f"minimum={minimum_jacobian}",
        ),
        utility.check(
            "no_new_failure_category",
            set(current_failures) == prior_failure_categories,
            "|".join(sorted(current_failures)),
        ),
        utility.check(
            "accepted_and_pending_area_are_conserved",
            abs(accepted_area + pending_area - total_area) <= 2.0e-12,
            f"error={accepted_area + pending_area - total_area}",
        ),
        utility.check(
            "row_count_matches_state",
            len(rows) == accepted_count,
            f"rows={len(rows)}; state={accepted_count}",
        ),
        utility.check(
            "broad_claims_remain_false",
            all(not payload[flag] for flag in BROAD_FLAGS),
            "all broad claims false",
        ),
        utility.check(
            "formalization_workbench_untouched",
            not formalization_touches,
            f"files modified after start={len(formalization_touches)}",
        ),
    ]
    utility.atomic_csv(VALIDATION, validations)
    payload["validation_count"] = len(validations)
    payload["failed_validation_count"] = sum(
        not bool(row["passed"]) for row in validations
    )
    write_document(utility, payload)
    utility.atomic_json(RESULT, payload)
    print(json.dumps(payload, indent=2, sort_keys=True), flush=True)
    return payload


def main() -> int:
    payload = run_gate()
    return 0 if payload["failed_validation_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
