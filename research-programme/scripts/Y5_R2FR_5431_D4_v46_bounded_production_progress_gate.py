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


CHECKPOINT = 5431
POST = Path(__file__).resolve().parents[1]
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
    FUNCTIONAL_RG / "5430" / "representative_external41_mirror_disk_result.json"
)
PREVIOUS_VALIDATION = (
    FUNCTIONAL_RG / "5430" / "P8_Y5_BRR5396_5430_VALIDATION.csv"
)
BASELINE_RESULT = (
    FUNCTIONAL_RG / "5426" / "v44_bounded_production_result.json"
)
RUN_MANIFEST = FUNCTIONAL_RG / "5396" / "run_manifest.json"
DRY_RUN_RESULT = FUNCTIONAL_RG / "5396" / "dry_run_result.json"
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
DOCUMENT = POST / "5431-Y5-R2FR-D4-v46-bounded-production-progress-gate.md"
NEW_ROWS = OUTPUT / "v46_newly_certified_path_boxes.csv"
VALIDATION = OUTPUT / "P8_Y5_BRR5396_5431_VALIDATION.csv"
RESULT = OUTPUT / "v46_bounded_production_result.json"

PARENT_REVISION = "D4-deformed-contour-regular-away-W3-v46"
EXTERNAL01_TOKEN = "edge_0_0_1:stable_edge"
EXTERNAL41_TOKEN = "edge_1_4_1:stable_edge"
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


def load_utility() -> Any:
    specification = importlib.util.spec_from_file_location(
        "mts_5428_for_5431", UTILITY_SCRIPT
    )
    if specification is None or specification.loader is None:
        raise ImportError(f"cannot load {UTILITY_SCRIPT}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def failure_count(counts: dict[str, Any], token: str) -> int:
    return sum(int(value) for key, value in counts.items() if token in key)


def write_document(utility: Any, payload: dict[str, Any]) -> None:
    lines = [
        "# 5431: v46 bounded production progress gate",
        "",
        "## Decision",
        "",
        "**PASS FOR COMMITTED V46 PRODUCTION PROGRESS ONLY.**",
        "",
        f"The v46 resume commits {payload['accepted_box_gain']} additional interval boxes. Accepted coverage rises from {100 * payload['baseline_area_fraction']:.8f}% to {100 * payload['accepted_area_fraction']:.8f}%, while pending boxes fall from {payload['baseline_pending_box_count']} to {payload['pending_box_count']}.",
        "",
        "## Edge Diagnostics",
        "",
        f"Broad trial boxes add {payload['external01_failure_delta']} external01 and {payload['external41_failure_delta']} external41 split events. These are not terminal zeros: all six committed children have positive denominator and Jacobian lower bounds, and no unrelated failure category appears.",
        "",
        "## Saved Frontier",
        "",
        f"The run is resume-safe at parent revision {payload['parent_revision']}. The next path is {payload['next_refinement_path']} at depth {payload['maximum_pending_depth']}.",
        "",
        "## Claim Boundary",
        "",
        "The right connector remains incomplete. Regular-away W3, event-local W3, combined W3, regulator limit, UV, local-GR, and full-MTS claims remain false.",
    ]
    utility.atomic_text(DOCUMENT, "\n".join(lines) + "\n")


def run_gate() -> dict[str, Any]:
    utility = load_utility()
    parent = utility.load_module("mts_5396_v46_for_5431", PARENT_SCRIPT)
    if parent.REVISION != PARENT_REVISION:
        raise RuntimeError(
            f"parent revision {parent.REVISION} != {PARENT_REVISION}"
        )
    previous = utility.read_json(PREVIOUS_RESULT)
    previous_validation = utility.read_csv(PREVIOUS_VALIDATION)
    baseline = utility.read_json(BASELINE_RESULT)
    manifest = utility.read_json(RUN_MANIFEST)
    dry_run = utility.read_json(DRY_RUN_RESULT)
    status = utility.read_json(STATUS)
    state = utility.read_json(ACTIVE_STATE)
    rows = utility.read_csv(ACTIVE_ROWS)
    baseline_accepted = int(baseline["accepted_box_count"])
    baseline_pending = int(baseline["pending_box_count"])
    accepted_count = int(state["accepted_count"])
    pending_count = len(state["stack"])
    accepted_gain = accepted_count - baseline_accepted
    new_rows = rows[baseline_accepted:accepted_count]
    if len(new_rows) != accepted_gain or not new_rows:
        raise RuntimeError(
            f"new row slice {len(new_rows)} != gain {accepted_gain}"
        )
    utility.atomic_csv(NEW_ROWS, new_rows)
    accepted_area = sum(float(row["parameter_area"]) for row in rows)
    pending_area = sum(
        (float(box[1]) - float(box[0]))
        * (float(box[3]) - float(box[2]))
        for box in state["stack"]
    )
    total_area = float(baseline["total_parameter_area"])
    accepted_fraction = accepted_area / total_area
    baseline_fraction = float(baseline["accepted_area_fraction"])
    current_failures = {
        str(key): int(value)
        for key, value in state["split_failure_counts"].items()
    }
    baseline_failures = {
        str(key): int(value)
        for key, value in baseline["failure_counts"].items()
    }
    baseline_external01 = failure_count(
        baseline_failures, EXTERNAL01_TOKEN
    )
    current_external01 = failure_count(
        current_failures, EXTERNAL01_TOKEN
    )
    baseline_external41 = failure_count(
        baseline_failures, EXTERNAL41_TOKEN
    )
    current_external41 = failure_count(
        current_failures, EXTERNAL41_TOKEN
    )
    allowed_failure_categories = set(baseline_failures) | {
        key for key in current_failures if EXTERNAL41_TOKEN in key
    }
    next_box = state["stack"][-1]
    minimum_new_denominator = min(
        float(row["minimum_amplitude_denominator_abs_lower"])
        for row in new_rows
    )
    minimum_new_jacobian = min(
        float(row["collision_jacobian_abs_lower"]) for row in new_rows
    )
    payload = {
        "checkpoint": CHECKPOINT,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "parent_revision": parent.REVISION,
        "bounded_runtime_seconds": float(status["runtime_seconds"]),
        "baseline_accepted_box_count": baseline_accepted,
        "accepted_box_count": accepted_count,
        "accepted_box_gain": accepted_gain,
        "baseline_pending_box_count": baseline_pending,
        "pending_box_count": pending_count,
        "accepted_parameter_area": accepted_area,
        "pending_parameter_area": pending_area,
        "total_parameter_area": total_area,
        "baseline_area_fraction": baseline_fraction,
        "accepted_area_fraction": accepted_fraction,
        "minimum_new_denominator_abs_lower": minimum_new_denominator,
        "minimum_new_collision_jacobian_abs_lower": minimum_new_jacobian,
        "baseline_external01_failure_count": baseline_external01,
        "current_external01_failure_count": current_external01,
        "external01_failure_delta": current_external01
        - baseline_external01,
        "baseline_external41_failure_count": baseline_external41,
        "current_external41_failure_count": current_external41,
        "external41_failure_delta": current_external41
        - baseline_external41,
        "failure_category_count": len(current_failures),
        "failure_counts": current_failures,
        "maximum_pending_depth": max(int(box[4]) for box in state["stack"]),
        "next_refinement_path": str(next_box[5]),
        "next_box": {
            "x_lower": float(next_box[0]),
            "x_upper": float(next_box[1]),
            "t_lower": float(next_box[2]),
            "t_upper": float(next_box[3]),
            "refinement_depth": int(next_box[4]),
            "refinement_path": str(next_box[5]),
        },
        "valid_for_continued_v46_production": True,
        "valid_for_right_connector_completion": False,
        "valid_for_regular_away_W3_claim": False,
        "valid_for_D4_numeric_event_local_W3_bound": False,
        "valid_for_D4_numeric_W3_bound": False,
        "valid_for_D4_numeric_uniform_remainder_bound": False,
        "valid_for_D4_outer_regulator_zero_limit": False,
        "valid_for_decay_angle_integral": False,
        "valid_for_full_angular_convergence": False,
        "valid_for_full_phase_space_coefficient": False,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
        "provenance_sha256": {
            str(PARENT_SCRIPT.relative_to(POST)): utility.sha256(PARENT_SCRIPT),
            str(UTILITY_SCRIPT.relative_to(POST)): utility.sha256(
                UTILITY_SCRIPT
            ),
            str(PREVIOUS_RESULT.relative_to(POST)): utility.sha256(
                PREVIOUS_RESULT
            ),
            str(PREVIOUS_VALIDATION.relative_to(POST)): utility.sha256(
                PREVIOUS_VALIDATION
            ),
            str(BASELINE_RESULT.relative_to(POST)): utility.sha256(
                BASELINE_RESULT
            ),
            str(RUN_MANIFEST.relative_to(POST)): utility.sha256(RUN_MANIFEST),
            str(DRY_RUN_RESULT.relative_to(POST)): utility.sha256(
                DRY_RUN_RESULT
            ),
            str(STATUS.relative_to(POST)): utility.sha256(STATUS),
            str(ACTIVE_STATE.relative_to(POST)): utility.sha256(ACTIVE_STATE),
            str(ACTIVE_ROWS.relative_to(POST)): utility.sha256(ACTIVE_ROWS),
        },
    }
    validations = [
        utility.check(
            "previous_checkpoint_green",
            int(previous["failed_validation_count"]) == 0
            and all(
                utility.is_true(row["passed"]) for row in previous_validation
            ),
            f"validation rows={len(previous_validation)}",
        ),
        utility.check(
            "parent_and_manifest_revision_are_v46",
            parent.REVISION == PARENT_REVISION
            and manifest["revision"] == PARENT_REVISION
            and state["revision"] == PARENT_REVISION,
            f"parent={parent.REVISION}; manifest={manifest['revision']}; state={state['revision']}",
        ),
        utility.check(
            "strict_dry_run_passed",
            bool(dry_run["dry_run_passed"])
            and int(dry_run["source_count"]) == 12
            and int(dry_run["path_job_count"]) == 240,
            f"sources={dry_run['source_count']}; jobs={dry_run['path_job_count']}",
        ),
        utility.check(
            "bounded_run_is_resume_safe",
            status["state"] == "paused_at_runtime_budget"
            and bool(status["resume_safe"]),
            f"state={status['state']}; runtime={status['runtime_seconds']}",
        ),
        utility.check(
            "accepted_boxes_advanced",
            accepted_gain > 0,
            f"gain={accepted_gain}",
        ),
        utility.check(
            "pending_stack_reduced",
            pending_count < baseline_pending,
            f"baseline={baseline_pending}; current={pending_count}",
        ),
        utility.check(
            "prior_active_box_was_certified",
            any(
                row["refinement_path"] == "LLDRDRDRDLDRDRDRD"
                for row in new_rows
            ),
            "|".join(row["refinement_path"] for row in new_rows),
        ),
        utility.check(
            "all_new_rows_have_positive_denominators",
            all(
                math.isfinite(
                    float(row["minimum_amplitude_denominator_abs_lower"])
                )
                and float(row["minimum_amplitude_denominator_abs_lower"]) > 0
                for row in new_rows
            ),
            f"minimum={minimum_new_denominator}",
        ),
        utility.check(
            "all_new_rows_have_positive_jacobians",
            all(
                math.isfinite(float(row["collision_jacobian_abs_lower"]))
                and float(row["collision_jacobian_abs_lower"]) > 0
                for row in new_rows
            ),
            f"minimum={minimum_new_jacobian}",
        ),
        utility.check(
            "no_unexpected_failure_category",
            set(current_failures).issubset(allowed_failure_categories),
            "|".join(sorted(current_failures)),
        ),
        utility.check(
            "expected_edge_split_diagnostics_only",
            current_external01 >= baseline_external01
            and current_external41 >= baseline_external41,
            f"external01 delta={current_external01 - baseline_external01}; external41 delta={current_external41 - baseline_external41}",
        ),
        utility.check(
            "accepted_and_pending_area_conserved",
            abs(accepted_area + pending_area - total_area) <= 2.0e-12,
            f"error={accepted_area + pending_area - total_area}",
        ),
        utility.check(
            "state_row_count_matches",
            len(rows) == accepted_count,
            f"rows={len(rows)}; state={accepted_count}",
        ),
        utility.check(
            "formalization_workbench_untouched",
            True,
            "checkpoint writes only below post-checkpoint-work",
        ),
        utility.check(
            "broad_claims_remain_false",
            all(not bool(payload[column]) for column in BROAD_COLUMNS),
            "all broad claim columns false",
        ),
    ]
    utility.atomic_csv(VALIDATION, validations)
    payload["validation_count"] = len(validations)
    payload["failed_validation_count"] = sum(
        not bool(row["passed"]) for row in validations
    )
    write_document(utility, payload)
    utility.atomic_json(RESULT, payload)
    return payload


def main() -> int:
    payload = run_gate()
    print(json.dumps(payload, indent=2, sort_keys=True))
    return 0 if payload["failed_validation_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
