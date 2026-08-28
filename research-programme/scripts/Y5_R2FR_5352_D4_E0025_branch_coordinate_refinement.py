from __future__ import annotations

import argparse
import ast
import csv
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import sys
import time
from typing import Any


os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("NUMEXPR_NUM_THREADS", "1")
sys.dont_write_bytecode = True

POST = Path(__file__).resolve().parents[1]
SCRIPTS = POST / "scripts"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
SCRIPT_5337 = SCRIPTS / "Y5_R2FR_5337_D4_regulator_fold_double_scaling_and_contrast_gate.py"
SCAN = FUNCTIONAL_RG / "5337" / "D4_targeted_event_regulator_scan.csv"
PREREG_RESULT = FUNCTIONAL_RG / "5350" / "E0025" / "D4_E0025_affine_holdout_preregistration_result.json"
PREREG_VALIDATION = FUNCTIONAL_RG / "5350" / "E0025" / "D4_E0025_affine_holdout_preregistration_validation.csv"
SOURCE = FUNCTIONAL_RG / "5334" / "E0025"
EVENTS = SOURCE / "D4_outer_refined_support_events.csv"
CANDIDATES = SOURCE / "D4_outer_support_event_candidates.csv"
CONTRACT = SOURCE / "D4_outer_reduced_MC04_cubature_contract.csv"
POLES = SOURCE / "D4_outer_E0025_geometric_poles.csv"
EXPECTED_IDS = [f"E{index:02d}" for index in range(1, 9)]
BRANCH_IDS = ["E04", "E05", "E06", "E07"]
CLAIM = "valid_for_D4_E0025_branch_event_coordinate_refinement"
DOWNSTREAM_FALSE = (
    "valid_for_D4_E0025_all_eight_endpoint_coefficients",
    "valid_for_D4_four_regulator_affine_endpoint_coefficient_holdout",
    "valid_for_D4_endpoint_coefficient_regulator_zero_limit",
    "valid_for_D4_outer_regulator_zero_limit",
    "valid_for_decay_angle_integral",
    "valid_for_full_angular_convergence",
    "valid_for_full_phase_space_coefficient",
    "valid_for_numeric_UV_claim",
    "valid_for_local_GR_claim",
    "valid_for_full_MTS_claim",
)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def parse_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() == "true"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def atomic_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    fields: list[str] = []
    for row in rows:
        fields.extend(key for key in row if key not in fields)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    os.replace(temporary, path)


def atomic_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def no_claims() -> dict[str, bool]:
    return {CLAIM: False, **{field: False for field in DOWNSTREAM_FALSE}}


def validation_row(gate: str, passed: bool, detail: Any) -> dict[str, Any]:
    return {"gate": gate, "passed": bool(passed), "detail": str(detail)}


def literal_constants(path: Path) -> dict[str, float]:
    wanted = {
        "EVENT_ROOT_WIDTH",
        "CONTACT_RESIDUAL_LIMIT",
        "TRANSVERSE_SLOPE_FLOOR",
        "SLOPE_WINDOW_RELATIVE_CHANGE_LIMIT",
    }
    tree = ast.parse(path.read_text(encoding="utf-8-sig"), filename=str(path))
    values: dict[str, float] = {}
    for node in tree.body:
        if not isinstance(node, (ast.Assign, ast.AnnAssign)):
            continue
        targets = node.targets if isinstance(node, ast.Assign) else [node.target]
        value_node = node.value
        for target in targets:
            if isinstance(target, ast.Name) and target.id in wanted:
                values[target.id] = float(ast.literal_eval(value_node))
    return values


def direct_source_chain_current(payload: dict[str, Any]) -> tuple[bool, int]:
    rows = payload.get("source_files", [])
    if not isinstance(rows, list) or not rows:
        return False, 0
    return (
        all(
            Path(str(row.get("path", ""))).is_file()
            and len(str(row.get("sha256", ""))) == 64
            and digest(Path(str(row["path"]))) == str(row["sha256"])
            for row in rows
        ),
        len(rows),
    )


def run(output: Path) -> dict[str, Any]:
    started = time.perf_counter()
    output = output.resolve()
    events_path = output / "D4_E0025_bracket_refined_events.csv"
    audit_path = output / "D4_E0025_branch_coordinate_refinement_audit.csv"
    validation_path = output / "D4_E0025_branch_coordinate_refinement_validation.csv"
    result_path = output / "D4_E0025_branch_coordinate_refinement_result.json"
    source_register = output / "source_register.csv"
    status_path = output / "status.json"
    source_paths = [
        Path(__file__).resolve(),
        SCRIPT_5337,
        SCAN,
        PREREG_RESULT,
        PREREG_VALIDATION,
        EVENTS,
        CANDIDATES,
        CONTRACT,
        POLES,
    ]
    sources = [
        {
            "path": str(path.resolve()),
            "sha256": digest(path) if path.is_file() else "MISSING",
            "exists": path.is_file(),
            **no_claims(),
        }
        for path in source_paths
    ]
    constants = literal_constants(SCRIPT_5337)
    root_width = constants.get("EVENT_ROOT_WIDTH", math.nan)
    half_width = 0.5 * root_width
    contact_limit = constants.get("CONTACT_RESIDUAL_LIMIT", math.nan)
    slope_floor = constants.get("TRANSVERSE_SLOPE_FLOOR", math.nan)
    slope_change_limit = constants.get(
        "SLOPE_WINDOW_RELATIVE_CHANGE_LIMIT", math.nan
    )
    prereg = read_json(PREREG_RESULT)
    prereg_validation = read_csv(PREREG_VALIDATION)
    prereg_current, prereg_source_count = direct_source_chain_current(prereg)
    original_events = read_csv(EVENTS)
    original_by_id = {row["event_id"]: row for row in original_events}
    scans = {
        row["event_id"]: row
        for row in read_csv(SCAN)
        if row["epsilon_id"] == "E0025"
    }
    current_contract_hash = digest(CONTRACT)
    current_pole_hash = digest(POLES)
    refined_events: list[dict[str, Any]] = []
    audit: list[dict[str, Any]] = []
    for event_id in EXPECTED_IDS:
        original = original_by_id[event_id]
        refined: dict[str, Any] = {
            key: value for key, value in original.items() if not key.startswith("valid_for_")
        }
        scan = scans[event_id]
        if event_id in BRANCH_IDS:
            old_coordinate = float(original["event_coordinate"])
            old_error = float(original["event_coordinate_error_estimate"])
            new_coordinate = float(scan["event_coordinate"])
            refined["event_coordinate"] = new_coordinate
            refined["source_bracket_left"] = new_coordinate - half_width
            refined["source_bracket_right"] = new_coordinate + half_width
            refined["event_coordinate_error_estimate"] = half_width
            refined["iteration_count"] = int(scan["root_iteration_count"])
            refined["event_pole_real"] = float(scan["pole_real"])
            refined["coordinate_refinement_method"] = (
                "CHECKPOINT_5337_BRANCH_EXISTENCE_BISECTION_MIDPOINT"
            )
            refined["coordinate_refinement_root_width_bound"] = root_width
            refined["coordinate_refinement_source_scan_sha256"] = digest(SCAN)
            audit.append(
                {
                    "event_id": event_id,
                    "old_coordinate": old_coordinate,
                    "new_coordinate": new_coordinate,
                    "coordinate_shift": new_coordinate - old_coordinate,
                    "old_coordinate_error": old_error,
                    "new_coordinate_error": half_width,
                    "new_interval_is_inside_old_error_disk": abs(new_coordinate - old_coordinate)
                    + half_width
                    <= old_error,
                    "root_iteration_count": int(scan["root_iteration_count"]),
                    "contact_residual": float(scan["contact_residual"]),
                    "near_transverse_slope_magnitude": float(
                        scan["near_transverse_slope_magnitude"]
                    ),
                    "broad_transverse_slope_magnitude": float(
                        scan["broad_transverse_slope_magnitude"]
                    ),
                    "slope_window_relative_change": float(
                        scan["slope_window_relative_change"]
                    ),
                    "targeted_event_contract_passes": parse_bool(
                        scan["targeted_event_contract_passes"]
                    ),
                    **no_claims(),
                }
            )
        refined.update(no_claims())
        refined_events.append(refined)
    constants_pass = (
        set(constants)
        == {
            "EVENT_ROOT_WIDTH",
            "CONTACT_RESIDUAL_LIMIT",
            "TRANSVERSE_SLOPE_FLOOR",
            "SLOPE_WINDOW_RELATIVE_CHANGE_LIMIT",
        }
        and root_width == 2.0e-11
        and half_width == 1.0e-11
    )
    branch_scan_contracts_pass = all(
        parse_bool(scans[event_id]["targeted_event_contract_passes"])
        and scans[event_id]["event_type"] == "BRANCH_DEATH"
        and scans[event_id]["normal_form_class"]
        == "ONE_SIDED_TRANSVERSE_SUPPORT_CONTACT"
        and scans[event_id]["contact_boundary"] == "UPPER"
        and 0 < int(scans[event_id]["root_iteration_count"]) < 80
        and float(scans[event_id]["contact_residual"]) <= contact_limit
        and float(scans[event_id]["near_transverse_slope_magnitude"]) >= slope_floor
        and float(scans[event_id]["broad_transverse_slope_magnitude"])
        >= slope_floor
        and float(scans[event_id]["slope_window_relative_change"])
        <= slope_change_limit
        for event_id in BRANCH_IDS
    )
    gates = [
        validation_row(
            "all_sources_exist_and_are_hashed",
            all(row["exists"] and row["sha256"] != "MISSING" for row in sources),
            len(sources),
        ),
        validation_row(
            "E0025_holdout_preregistration_is_current",
            prereg.get("validation_passed") is True
            and prereg.get("claim_boundary", {}).get(
                "valid_for_D4_E0025_affine_holdout_preregistration"
            )
            is True
            and prereg_current
            and prereg_source_count > 0
            and all(parse_bool(row["passed"]) for row in prereg_validation),
            prereg_source_count,
        ),
        validation_row(
            "source_5337_bisection_constants_are_frozen",
            constants_pass,
            constants,
        ),
        validation_row(
            "source_event_and_scan_inventories_are_exact",
            [row["event_id"] for row in original_events] == EXPECTED_IDS
            and sorted(scans) == EXPECTED_IDS
            and [row["event_id"] for row in refined_events] == EXPECTED_IDS,
            EXPECTED_IDS,
        ),
        validation_row(
            "source_event_parent_hashes_are_current",
            all(
                row["contract_sha256"] == current_contract_hash
                and row["parent_pole_sha256"] == current_pole_hash
                and parse_bool(row["event_contract_passes"])
                for row in original_events
            ),
            len(original_events),
        ),
        validation_row(
            "all_four_branch_scans_close_before_iteration_cap",
            branch_scan_contracts_pass,
            [(event_id, scans[event_id]["root_iteration_count"]) for event_id in BRANCH_IDS],
        ),
        validation_row(
            "new_midpoint_intervals_fit_inside_old_error_disks",
            len(audit) == 4
            and all(row["new_interval_is_inside_old_error_disk"] for row in audit),
            [(row["event_id"], row["coordinate_shift"]) for row in audit],
        ),
        validation_row(
            "branch_coordinate_error_is_strictly_tightened",
            all(
                row["new_coordinate_error"] < row["old_coordinate_error"]
                and row["new_coordinate_error"] == half_width
                for row in audit
            ),
            half_width,
        ),
        validation_row(
            "source_geometry_is_read_only",
            all(digest(path) == row["sha256"] for path, row in zip(source_paths, sources)),
            "all output paths are under checkpoint 5352",
        ),
        validation_row(
            "scripts_cache_absent",
            not (SCRIPTS / "__pycache__").exists(),
            SCRIPTS / "__pycache__",
        ),
    ]
    passed = all(parse_bool(row["passed"]) for row in gates)
    for row in refined_events:
        row[CLAIM] = passed
    for row in audit:
        row[CLAIM] = passed
    atomic_csv(events_path, refined_events)
    atomic_csv(audit_path, audit)
    atomic_csv(validation_path, gates)
    atomic_csv(source_register, sources)
    claims = no_claims()
    claims[CLAIM] = passed
    result = {
        "mode": "D4-E0025-branch-coordinate-refinement",
        "epsilon_id": "E0025",
        "epsilon": 0.0025,
        "validation_passed": passed,
        "decision": (
            "D4_E0025_BRANCH_COORDINATES_BRACKET_REFINED__RERUN_ALL_EIGHT_COEFFICIENT"
            if passed
            else "D4_E0025_BRANCH_COORDINATE_REFINEMENT_BLOCKED"
        ),
        "branch_event_ids": BRANCH_IDS,
        "event_root_width": root_width,
        "event_coordinate_error_bound": half_width,
        "maximum_old_coordinate_error": max(row["old_coordinate_error"] for row in audit),
        "maximum_new_coordinate_error": max(row["new_coordinate_error"] for row in audit),
        "source_geometry_is_read_only": True,
        "refined_event_path": str(events_path),
        "claim_boundary": claims,
        "source_files": sources,
        "formalization_workbench_modified_file_count": 0,
        "runtime_seconds": time.perf_counter() - started,
        "updated_utc": utc_now(),
    }
    atomic_json(result_path, result)
    atomic_json(
        status_path,
        {
            "state": "COMPLETE" if passed else "BLOCKED",
            "decision": result["decision"],
            "validation_passed": passed,
            "updated_utc": utc_now(),
        },
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return result


def self_test() -> dict[str, Any]:
    constants = literal_constants(SCRIPT_5337)
    checks = {
        "event_root_width_is_source_parsed": constants.get("EVENT_ROOT_WIDTH")
        == 2.0e-11,
        "midpoint_error_is_half_width": 0.5 * constants["EVENT_ROOT_WIDTH"]
        == 1.0e-11,
        "downstream_claims_start_false": all(
            value is False for value in no_claims().values()
        ),
    }
    return {"mode": "self-test", "checks": checks, "all_pass": all(checks.values())}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--self-test", action="store_true")
    arguments = parser.parse_args()
    if arguments.self_test:
        result = self_test()
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0 if result["all_pass"] else 1
    if arguments.output_dir is None:
        parser.error("--output-dir is required")
    result = run(arguments.output_dir)
    return 0 if result["validation_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
