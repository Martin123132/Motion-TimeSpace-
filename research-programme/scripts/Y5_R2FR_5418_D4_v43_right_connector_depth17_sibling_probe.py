from __future__ import annotations

import argparse
import csv
from datetime import datetime, timezone
import hashlib
import importlib.util
import json
import math
import os
from pathlib import Path
import sys
import time
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


CHECKPOINT = 5418
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
    / "5417"
    / "v43_right_connector_frontier_expansion_result.json"
)
PREVIOUS_VALIDATION = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5417"
    / "P8_Y5_BRR5396_5417_VALIDATION.csv"
)
STATUS = SOURCE / "status.json"
RIGHT_STATE = (
    PARTITIONS
    / "bin_00_sub_00_S_X006_MC04_SP_DP_RIGHT_CONNECTOR_part_00_of_01.state.json"
)
RIGHT_ROWS = RIGHT_STATE.with_suffix(".rows.csv")
DOCUMENT = (
    POST / "5418-Y5-R2FR-D4-v43-right-connector-depth17-sibling-probe.md"
)
PROBES = OUTPUT / "v43_right_connector_depth17_sibling_probes.csv"
VALIDATION = OUTPUT / "P8_Y5_BRR5396_5418_VALIDATION.csv"
RESULT = OUTPUT / "v43_right_connector_depth17_sibling_probe_result.json"

REVISION = "D4-deformed-contour-regular-away-W3-v43"
TERM_ID = "MC04_SP_DP"
MAPPED_CELL_ID = "S_X006_MC04_SP_DP"
PATH_SEGMENT = "RIGHT_CONNECTOR"
GLOBAL_ARC_COUNT = 4
EXPECTED_ACCEPTED = 233
EXPECTED_PENDING = 14
EXPECTED_PATH_JOBS = 29
TARGETS = (
    {
        "refinement_path": "LLDRDLDLDRDRDRDLD",
        "x_lower": 0.32121972608406446,
        "x_upper": 0.3212965376782158,
        "t_lower": 0.0,
        "t_upper": 0.00390625,
        "refinement_depth": 17,
    },
    {
        "refinement_path": "LLDRDLDLDRDRDRDLU",
        "x_lower": 0.32121972608406446,
        "x_upper": 0.3212965376782158,
        "t_lower": 0.00390625,
        "t_upper": 0.0078125,
        "refinement_depth": 17,
    },
)
POSITIVE_RESULT_FIELDS = (
    "parameter_area",
    "minimum_amplitude_denominator_abs_lower",
    "relative_root_abs_lower",
    "selected_global_root_abs_lower",
    "collision_jacobian_abs_lower",
)
BROAD_RESULT_FLAGS = (
    "valid_for_regular_away_W3_claim",
    "valid_for_numeric_W3_claim",
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


def load_parent() -> Any:
    specification = importlib.util.spec_from_file_location("mts_5396", PARENT_SCRIPT)
    if specification is None or specification.loader is None:
        raise ImportError(f"cannot load {PARENT_SCRIPT}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def is_true(value: Any) -> bool:
    return str(value).strip().lower() == "true"


def check(name: str, passed: bool, evidence: str) -> dict[str, Any]:
    return {"check": name, "passed": bool(passed), "evidence": evidence}


def target_tuple(row: dict[str, Any] | list[Any]) -> tuple[Any, ...]:
    if isinstance(row, dict):
        return (
            float(row["x_lower"]),
            float(row["x_upper"]),
            float(row["t_lower"]),
            float(row["t_upper"]),
            int(row["refinement_depth"]),
            str(row["refinement_path"]),
        )
    return (
        float(row[0]),
        float(row[1]),
        float(row[2]),
        float(row[3]),
        int(row[4]),
        str(row[5]),
    )


def epsilon_and_cell(parent: Any) -> tuple[dict[str, Any], dict[str, Any]]:
    cell = next(
        row
        for row in parent.away_term_support_cells()
        if row["mapped_cell_id"] == MAPPED_CELL_ID
    )
    arguments = argparse.Namespace(
        combined_regulator_box=True,
        combined_regulator_slab_count=2,
        epsilon_subdivisions=1,
    )
    return cell, parent.epsilon_boxes(arguments)[0]


def empty_probe(target: dict[str, Any]) -> dict[str, Any]:
    return {
        "checkpoint": CHECKPOINT,
        **target,
        "probe_status": "",
        "failure_category": "",
        "failure_message": "",
        "elapsed_seconds": "",
        "parameter_area": "",
        "raw_integrand_abs_upper": "",
        "regular_integrand_abs_upper": "",
        "integrated_regular_path_abs_upper": "",
        "minimum_amplitude_denominator_abs_lower": "",
        "relative_root_abs_lower": "",
        "selected_global_root_abs_lower": "",
        "collision_jacobian_abs_lower": "",
        "collision_jacobian_enclosure_method": "",
        "path_integral_enclosure_method": "",
        "valid_for_direct_depth17_box_certificate": False,
        "valid_for_committed_production_transition": False,
        **{flag: False for flag in BROAD_RESULT_FLAGS},
    }


def evaluate_target(
    parent: Any,
    cell: dict[str, Any],
    epsilon_row: dict[str, Any],
    target: dict[str, Any],
) -> dict[str, Any]:
    probe = empty_probe(target)
    started = time.perf_counter()
    print(
        json.dumps(
            {
                "state": "depth17_sibling_probe_started",
                "refinement_path": target["refinement_path"],
            }
        ),
        flush=True,
    )
    try:
        row = parent.evaluate_path_box(
            cell,
            TERM_ID,
            parent.configuration_variants(TERM_ID),
            epsilon_row,
            PATH_SEGMENT,
            float(target["x_lower"]),
            float(target["x_upper"]),
            float(target["t_lower"]),
            float(target["t_upper"]),
            int(target["refinement_depth"]),
            str(target["refinement_path"]),
            parent.material_support_segments(),
            parent.material_branch_data(),
            GLOBAL_ARC_COUNT,
        )
        for field in (
            "parameter_area",
            "raw_integrand_abs_upper",
            "regular_integrand_abs_upper",
            "integrated_regular_path_abs_upper",
            "minimum_amplitude_denominator_abs_lower",
            "relative_root_abs_lower",
            "selected_global_root_abs_lower",
            "collision_jacobian_abs_lower",
            "collision_jacobian_enclosure_method",
            "path_integral_enclosure_method",
        ):
            probe[field] = row[field]
        probe["probe_status"] = "PASS"
        probe["valid_for_direct_depth17_box_certificate"] = True
    except Exception as error:
        probe["probe_status"] = "FAIL"
        probe["failure_category"] = parent.enclosure_failure_category(error)
        probe["failure_message"] = (
            str(error).replace("\r", " ").replace("\n", " | ")[:2000]
        )
    probe["elapsed_seconds"] = time.perf_counter() - started
    print(
        json.dumps(
            {
                "state": "depth17_sibling_probe_finished",
                "refinement_path": target["refinement_path"],
                "probe_status": probe["probe_status"],
                "failure_category": probe["failure_category"],
                "elapsed_seconds": probe["elapsed_seconds"],
            }
        ),
        flush=True,
    )
    return probe


def passed_probe_is_finite(row: dict[str, Any]) -> bool:
    if row["probe_status"] != "PASS":
        return True
    return all(
        math.isfinite(float(row[field])) and float(row[field]) > 0.0
        for field in POSITIVE_RESULT_FIELDS
    )


def write_document(payload: dict[str, Any], probes: list[dict[str, Any]]) -> None:
    if payload["all_depth17_siblings_certified"]:
        decision = "**PASS FOR BOTH DIRECT DEPTH-17 BOX CERTIFICATES ONLY.**"
        interpretation = (
            "Both pending siblings close under the unchanged v43 production evaluator. "
            "They are now eligible for a short resume run that commits them into the "
            "adaptive ledger; this probe does not mutate or replace that ledger."
        )
    else:
        decision = "**NO TRANSITION COMMIT; THE SURVIVING FAILURE IS RECORDED.**"
        failures = "; ".join(
            f"`{row['refinement_path']}` -> `{row['failure_category']}`"
            for row in probes
            if row["probe_status"] == "FAIL"
        )
        interpretation = (
            "At least one exact sibling still fails the production interval proof. "
            f"The next derivation target is the named factor rather than another blind run: {failures}."
        )
    lines = [
        "# 5418: v43 right-connector depth-17 sibling probe",
        "",
        "## Decision",
        "",
        decision,
        "",
        interpretation,
        "",
        "## Exact probes",
        "",
    ]
    for row in probes:
        if row["probe_status"] == "PASS":
            detail = (
                f"denominator `{float(row['minimum_amplitude_denominator_abs_lower']):.17g}`, "
                f"Jacobian `{float(row['collision_jacobian_abs_lower']):.17g}`"
            )
        else:
            detail = f"failure `{row['failure_category']}`"
        lines.append(
            f"- `{row['refinement_path']}`: **{row['probe_status']}**, {detail}; "
            f"elapsed `{float(row['elapsed_seconds']):.3f} s`."
        )
    lines.extend(
        [
            "",
            "## State discipline",
            "",
            "The production status, adaptive state, and accepted-row ledger are hash-identical before and after both probes. No probe row is represented as a committed production transition.",
            "",
            "## Claim boundary",
            "",
            "Regular-away W3, event-local W3, combined W3, regulator limit, UV, local-GR, and full-MTS claims remain false.",
            "",
        ]
    )
    atomic_text(DOCUMENT, "\n".join(lines))


def run_probe() -> dict[str, Any]:
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

    hashes_before = {str(path.relative_to(POST)): sha256(path) for path in required}
    previous = read_json(PREVIOUS)
    previous_validation = read_csv(PREVIOUS_VALIDATION)
    status = read_json(STATUS)
    state = read_json(RIGHT_STATE)
    accepted_rows = read_csv(RIGHT_ROWS)
    expected_targets = {target_tuple(row) for row in TARGETS}
    state_depth17 = {
        target_tuple(row) for row in state["stack"] if int(row[4]) == 17
    }

    parent = load_parent()
    parent.set_below_normal_priority()
    parent.iv.dps = parent.INTERVAL_DIGITS
    cell, epsilon_row = epsilon_and_cell(parent)
    probes: list[dict[str, Any]] = []
    for target in TARGETS:
        probes.append(evaluate_target(parent, cell, epsilon_row, target))
        atomic_csv(PROBES, probes)

    hashes_after = {str(path.relative_to(POST)): sha256(path) for path in required}
    passed = [row for row in probes if row["probe_status"] == "PASS"]
    failed = [row for row in probes if row["probe_status"] == "FAIL"]
    failure_categories = sorted({str(row["failure_category"]) for row in failed})
    payload: dict[str, Any] = {
        "checkpoint": CHECKPOINT,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "parent_revision": parent.REVISION,
        "target_count": len(TARGETS),
        "passed_target_count": len(passed),
        "failed_target_count": len(failed),
        "failure_categories": failure_categories,
        "elapsed_seconds": sum(float(row["elapsed_seconds"]) for row in probes),
        "all_depth17_siblings_certified": len(passed) == len(TARGETS),
        "production_state_unchanged": hashes_before == hashes_after,
        "next_action": (
            "RUN_SHORT_BOUNDED_V43_RESUME_TO_COMMIT_TRANSITION"
            if len(passed) == len(TARGETS)
            else "DERIVE_EXACT_SURVIVING_FACTOR_SUBCOVER"
        ),
        "valid_for_direct_depth17_sibling_certificate": len(passed) == len(TARGETS),
        "valid_for_committed_depth17_transition": False,
        **{flag: False for flag in BROAD_RESULT_FLAGS},
        "provenance_sha256": hashes_before,
    }
    write_document(payload, probes)

    formalization_touches = [
        path
        for path in FORMALIZATION.rglob("*")
        if path.is_file()
        and datetime.fromtimestamp(path.stat().st_mtime, timezone.utc) > started
    ]
    validations = [
        check("required_inputs_exist", not missing, f"{len(required)} paths present"),
        check("parent_revision_is_v43", parent.REVISION == REVISION, parent.REVISION),
        check(
            "checkpoint_5417_is_green_and_bounded",
            len(previous_validation) == 15
            and all(is_true(row["passed"]) for row in previous_validation)
            and bool(previous["valid_for_continued_v43_production"])
            and not bool(previous["valid_for_regular_away_W3_claim"]),
            "5417 has 15/15 passing gates with broad claims false",
        ),
        check(
            "production_state_matches_checkpoint_5417",
            status["state"] == "paused_at_runtime_budget"
            and bool(status["resume_safe"])
            and int(state["accepted_count"]) == len(accepted_rows) == EXPECTED_ACCEPTED
            and len(state["stack"]) == EXPECTED_PENDING
            and int(status["completed_path_jobs"]) == EXPECTED_PATH_JOBS,
            f"accepted={len(accepted_rows)}; pending={len(state['stack'])}; jobs={status['completed_path_jobs']}/240",
        ),
        check(
            "exact_depth17_siblings_are_in_saved_frontier",
            state_depth17 == expected_targets,
            "|".join(sorted(row[-1] for row in state_depth17)),
        ),
        check(
            "both_probes_complete",
            len(probes) == len(TARGETS)
            and all(row["probe_status"] in {"PASS", "FAIL"} for row in probes),
            f"pass={len(passed)}; fail={len(failed)}",
        ),
        check(
            "pass_certificates_are_finite_and_positive",
            all(passed_probe_is_finite(row) for row in probes),
            f"{len(passed)} passing rows checked",
        ),
        check(
            "failures_are_exactly_classified",
            all(row["probe_status"] == "PASS" or row["failure_category"] for row in probes),
            "|".join(failure_categories) if failure_categories else "no failures",
        ),
        check(
            "production_inputs_are_hash_immutable",
            hashes_before == hashes_after,
            f"{len(required)} input hashes checked",
        ),
        check(
            "probe_does_not_claim_production_commit",
            not payload["valid_for_committed_depth17_transition"],
            "direct probe is separate from adaptive ledger",
        ),
        check(
            "broad_claims_remain_false",
            all(not payload[flag] for flag in BROAD_RESULT_FLAGS),
            "W3, UV, local-GR, and full-MTS remain unclaimed",
        ),
        check(
            "formalization_workbench_untouched",
            not formalization_touches,
            f"files modified after probe start={len(formalization_touches)}",
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
    payload = run_probe()
    return 0 if payload["failed_validation_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
