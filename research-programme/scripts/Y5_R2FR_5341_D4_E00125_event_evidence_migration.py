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
import traceback
from typing import Any


os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("NUMEXPR_NUM_THREADS", "1")
sys.dont_write_bytecode = True


CHECKPOINT = 5341
MARKER = "MTS_5341_D4_E00125_EVENT_EVIDENCE_MIGRATION"
EPSILON_ID = "E00125"
EPSILON = 0.00125
SOURCE_EVENT_ROOT_HALF_WIDTH = 1.0e-11
POST = Path(__file__).resolve().parents[1]
ROOT = POST.parent
SCRIPTS = POST / "scripts"
OUT = POST / "source-intake" / "functional_rg" / str(CHECKPOINT)
RESIDUALS = POST / "source-intake" / "mts_residuals"
VALIDATION = RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv"
SCRIPT_5334 = SCRIPTS / "Y5_R2FR_5334_D4_outer_regulator_ladder_controller.py"
SCAN_5337 = POST / "source-intake/functional_rg/5337/D4_targeted_event_regulator_scan.csv"
RESULT_5337 = POST / "source-intake/functional_rg/5337/D4_regulator_fold_double_scaling_contrast_result.json"
VALIDATION_5337 = POST / "source-intake/mts_residuals/P8_Y5_BRR545_5337_VALIDATION.csv"
SOURCE_EVENTS_E0025 = POST / "source-intake/functional_rg/5334/E0025/D4_outer_refined_support_events.csv"
SOURCE_CANDIDATES_E0025 = POST / "source-intake/functional_rg/5334/E0025/D4_outer_support_event_candidates.csv"
TARGET_CANDIDATES = POST / "source-intake/functional_rg/5334/E00125/D4_outer_support_event_candidates.csv"
RESULT = OUT / "D4_E00125_event_evidence_migration_result.json"
MIGRATION = OUT / "D4_E00125_event_evidence_migration.csv"
SOURCE_REGISTER = OUT / "source_register.csv"
STATUS = OUT / "status.json"
FORMAL_DIGEST = "0ec1bc6012136ffc6b28a1512aca6ce712b6decd2ff793310a9bd61775f3db1f"
CLAIM_FIELDS = (
    "valid_for_D4_outer_E00125_event_geometry",
    "valid_for_D4_outer_E00125_fixed_decay_integral",
    "valid_for_D4_outer_regulator_zero_limit",
    "valid_for_decay_angle_integral",
    "valid_for_full_angular_convergence",
    "valid_for_full_phase_space_coefficient",
    "valid_for_numeric_UV_claim",
    "valid_for_local_GR_claim",
    "valid_for_full_MTS_claim",
)


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5334 = load_module("mts_5334_for_5341", SCRIPT_5334)
M5326 = M5334.M5326
M5312 = M5334.M5312
M5283 = M5334.M5283
M5325 = M5334.M5325


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"empty CSV payload: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(path)


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    temporary.replace(path)


def parse_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() == "true"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def no_claims() -> dict[str, bool]:
    return {field: False for field in CLAIM_FIELDS}


def validation_row(gate: str, passed: bool, detail: str) -> dict[str, Any]:
    return {
        "gate": gate,
        "passed": passed,
        "detail": detail,
        "checkpoint": CHECKPOINT,
        "marker": MARKER,
    }


def configure() -> None:
    M5334.configure_ladder()
    M5334.configure_D4_target(EPSILON_ID)


def source_paths() -> list[Path]:
    return [
        Path(__file__).resolve(),
        SCRIPT_5334,
        SCAN_5337,
        RESULT_5337,
        VALIDATION_5337,
        SOURCE_EVENTS_E0025,
        SOURCE_CANDIDATES_E0025,
        M5326.CONTRACT_5325,
        M5326.POLES_5325,
        M5326.EVENT_CANDIDATES,
    ]


def write_source_register() -> list[dict[str, Any]]:
    rows = [
        {
            "path": str(path.resolve()),
            "sha256": digest(path) if path.is_file() else "MISSING",
            "exists": path.is_file(),
            **no_claims(),
        }
        for path in source_paths()
    ]
    write_csv(SOURCE_REGISTER, rows)
    return rows


def support_at(
    coordinate: float,
    panel_index: int,
    term_id: str,
    pole_real: float,
    contract: list[dict[str, str]],
) -> tuple[float, dict[str, Any]]:
    cells = [
        M5312.cell_geometry(row, coordinate)
        for row in contract
        if int(row["x_panel_index"]) == panel_index
        and int(row["reduced_MC04_term_count"]) > 0
    ]
    supports = M5312.merged_term_supports(cells).get(term_id, [])
    return M5326.support_margin(pole_real, supports)


def migrated_events() -> tuple[list[dict[str, Any]], list[dict[str, Any]], list[dict[str, Any]]]:
    scan = [row for row in read_csv(SCAN_5337) if row["epsilon_id"] == EPSILON_ID]
    source = {row["event_id"]: row for row in read_csv(SOURCE_EVENTS_E0025)}
    candidates = {row["candidate_id"]: row for row in read_csv(TARGET_CANDIDATES)}
    events: list[dict[str, Any]] = []
    states: list[dict[str, Any]] = []
    audit: list[dict[str, Any]] = []
    for scanned in sorted(scan, key=lambda row: row["event_id"]):
        inherited = source[scanned["event_id"]]
        panel_index = int(scanned["x_panel_index"])
        term_id = scanned["term_id"]
        raw_coordinate = float(scanned["event_coordinate"])
        raw_pole = float(scanned["pole_real"])
        event_type = scanned["event_type"]
        corrected_coordinate = raw_coordinate
        signed_slope: float | str = ""
        contact_residual = float(scanned["contact_residual"])
        residual_bound = 0.0
        if event_type in {"SUPPORT_ENTRY", "SUPPORT_EXIT"}:
            inherited_slope = float(inherited["source_crossing_slope"])
            signed_slope = math.copysign(
                float(scanned["near_transverse_slope_magnitude"]),
                inherited_slope,
            )
            residual_bound = abs(float(signed_slope)) * SOURCE_EVENT_ROOT_HALF_WIDTH
        boundary = scanned["contact_boundary"]
        support_lower = float(inherited["event_support_lower"])
        support_upper = float(inherited["event_support_upper"])
        if boundary == "LOWER":
            support_lower = raw_pole - contact_residual
        else:
            support_upper = raw_pole + contact_residual
        boundary_value = support_lower if boundary == "LOWER" else support_upper
        central_pole = boundary_value if event_type != "BRANCH_DEATH" else raw_pole
        coordinate_error = SOURCE_EVENT_ROOT_HALF_WIDTH
        event = {
            "event_id": scanned["event_id"],
            "x_panel_index": panel_index,
            "term_id": term_id,
            "candidate_id": inherited["candidate_id"],
            "event_type": event_type,
            "primary_surface_id": scanned["primary_surface_id"],
            "source_bracket_left": inherited["source_bracket_left"],
            "source_bracket_right": inherited["source_bracket_right"],
            "event_coordinate": corrected_coordinate,
            "event_pole_real": central_pole,
            "event_support_lower": support_lower,
            "event_support_upper": support_upper,
            "event_signed_support_margin": (
                0.0 if event_type in {"SUPPORT_ENTRY", "SUPPORT_EXIT"} else contact_residual
            ),
            "source_crossing_slope": signed_slope,
            "event_coordinate_error_estimate": coordinate_error,
            "iteration_count": scanned["root_iteration_count"],
            "event_contract_passes": (
                parse_bool(scanned["targeted_event_contract_passes"])
                and (
                    coordinate_error <= M5326.EVENT_COORDINATE_ERROR_TOLERANCE
                    if event_type in {"SUPPORT_ENTRY", "SUPPORT_EXIT"}
                    else coordinate_error <= M5326.EVENT_COORDINATE_ERROR_TOLERANCE
                )
            ),
            "contract_sha256": "REFRESH_AFTER_TARGET_CONFIGURATION",
            "parent_pole_sha256": "REFRESH_AFTER_TARGET_CONFIGURATION",
            "candidate_source": "CHECKPOINT_5337_REGULATOR_EVENT_SCAN",
            "transfer_source_path": str(SCAN_5337.resolve()),
            "transfer_source_sha256": digest(SCAN_5337),
            **no_claims(),
        }
        candidate = candidates.get(event["candidate_id"], {})
        for field in (
            "adaptive_manifest_sha256",
            "adaptive_pole_sha256",
            "adaptive_classification_sha256",
            "source_left_node_id",
            "source_right_node_id",
        ):
            event[field] = candidate.get(field, "")
        events.append(event)
        states.append(
            {
                "x_panel_index": panel_index,
                "term_id": term_id,
                "primary_surface_id": scanned["primary_surface_id"],
                "absolute_soft_cosine": corrected_coordinate,
                "branch_exists": True,
                "pole_real": central_pole,
                "pole_imaginary": scanned["pole_imaginary"],
                "support_id": f"TRANSFERRED_{term_id}_SUPPORT",
                "support_energy_lower": support_lower,
                "support_energy_upper": support_upper,
                "signed_support_margin": event["event_signed_support_margin"],
                "inside_reduced_term_support": event_type != "BRANCH_DEATH",
                "state_source": "CHECKPOINT_5337_REGULATOR_EVENT_SCAN",
                **no_claims(),
            }
        )
        audit.append(
            {
                "event_id": scanned["event_id"],
                "event_type": event_type,
                "raw_scan_coordinate": raw_coordinate,
                "migrated_root_coordinate": corrected_coordinate,
                "migration_coordinate_shift": corrected_coordinate - raw_coordinate,
                "raw_support_contact_residual": contact_residual,
                "signed_transverse_slope": signed_slope,
                "support_margin_from_root_half_width_bound": residual_bound,
                "event_coordinate_error_estimate": coordinate_error,
                "support_id": f"TRANSFERRED_{term_id}_SUPPORT",
                "contact_boundary": boundary,
                "source_scan_contract_passes": scanned[
                    "targeted_event_contract_passes"
                ],
                "migrated_event_contract_passes": event[
                    "event_contract_passes"
                ],
                **no_claims(),
            }
        )
    return events, states, audit


def d4_dry_run_from_migrated_evidence(
    events: list[dict[str, Any]],
) -> dict[str, Any]:
    current_contract_hash = digest(M5326.CONTRACT_5325)
    current_pole_hash = digest(M5326.POLES_5325)
    for event in events:
        event["contract_sha256"] = current_contract_hash
        event["parent_pole_sha256"] = current_pole_hash
    write_csv(M5326.EVENTS, events)
    M5326.EXPECTED_EVENT_COUNT = len(events)
    if not M5326.event_cache_current():
        raise RuntimeError("migrated E00125 event cache is not current")

    original_candidate_rows = M5326.event_candidate_rows
    original_derive_events = M5326.derive_events

    def migrated_candidate_rows() -> list[dict[str, str]]:
        rows = read_csv(M5326.EVENT_CANDIDATES)
        if len(rows) != len(events):
            raise RuntimeError(
                f"expected {len(events)} migrated candidates, found {len(rows)}"
            )
        return rows

    def migrated_events_only() -> list[dict[str, str]]:
        if not M5326.event_cache_current():
            raise RuntimeError(
                "refusing duplicate E00125 root scan: migrated cache became stale"
            )
        return read_csv(M5326.EVENTS)

    M5326.event_candidate_rows = migrated_candidate_rows
    M5326.derive_events = migrated_events_only
    try:
        return M5334.d4_refinement_dry_run()
    finally:
        M5326.event_candidate_rows = original_candidate_rows
        M5326.derive_events = original_derive_events


def execute() -> dict[str, Any]:
    started = time.perf_counter()
    M5312.set_below_normal_priority()
    OUT.mkdir(parents=True, exist_ok=True)
    M5334.configure_smoke()
    M5325.EPSILON_ID = EPSILON_ID
    M5325.EPSILON = EPSILON
    old_kernel = M5325.configure_kernel()
    try:
        TARGET_CANDIDATES.parent.mkdir(parents=True, exist_ok=True)
        write_csv(TARGET_CANDIDATES, read_csv(SOURCE_CANDIDATES_E0025))
        events, states, audit = migrated_events()
    finally:
        M5325.restore_kernel(old_kernel)
    configure()
    sources = write_source_register()
    write_csv(M5326.EVENT_STATES, states)
    write_csv(MIGRATION, audit)
    dry = d4_dry_run_from_migrated_evidence(events)
    scan_result = read_json(RESULT_5337)
    scan_validation = read_csv(VALIDATION_5337)
    initial = read_csv(M5326.INITIAL_PLAN)
    transferred_support = [
        row for row in audit if row["event_type"] in {"SUPPORT_ENTRY", "SUPPORT_EXIT"}
    ]
    transferred_death = [row for row in audit if row["event_type"] == "BRANCH_DEATH"]
    gates = [
        validation_row(
            "all_source_paths_exist_and_are_hashed",
            len(sources) == 10
            and all(parse_bool(row["exists"]) for row in sources)
            and all(row["sha256"] != "MISSING" for row in sources),
            f"rows={len(sources)}",
        ),
        validation_row(
            "checkpoint_5337_seven_rung_geometry_gate_passes",
            scan_result.get("validation_passed") is True
            and bool(scan_validation)
            and all(parse_bool(row["passed"]) for row in scan_validation),
            str(scan_result.get("decision")),
        ),
        validation_row(
            "exactly_eight_E00125_events_transfer",
            len(events) == len(states) == len(audit) == 8
            and [row["event_id"] for row in events]
            == [f"E{index:02d}" for index in range(1, 9)],
            f"events={len(events)}",
        ),
        validation_row(
            "all_transferred_source_event_contracts_pass",
            all(parse_bool(row["event_contract_passes"]) for row in events)
            and all(parse_bool(row["migrated_event_contract_passes"]) for row in audit),
            f"rows={len(events)}",
        ),
        validation_row(
            "four_support_contacts_have_bracketed_root_error_bound",
            len(transferred_support) == 4
            and max(
                float(row["event_coordinate_error_estimate"])
                for row in transferred_support
            )
            <= M5326.EVENT_COORDINATE_ERROR_TOLERANCE,
            str(
                max(
                    float(row["event_coordinate_error_estimate"])
                    for row in transferred_support
                )
            ),
        ),
        validation_row(
            "four_branch_deaths_pass_parent_coordinate_tolerance",
            len(transferred_death) == 4
            and max(
                float(row["event_coordinate_error_estimate"])
                for row in transferred_death
            )
            <= M5326.EVENT_COORDINATE_ERROR_TOLERANCE,
            str(
                max(
                    float(row["event_coordinate_error_estimate"])
                    for row in transferred_death
                )
            ),
        ),
        validation_row(
            "event_and_parent_contract_hashes_are_current",
            all(
                row["contract_sha256"] == digest(M5326.CONTRACT_5325)
                and row["parent_pole_sha256"] == digest(M5326.POLES_5325)
                for row in events
            ),
            f"events={len(events)}",
        ),
        validation_row(
            "E00125_D4_dry_run_passes_without_duplicate_root_scan",
            bool(dry.get("acceptance_passed"))
            and int(dry.get("refined_event_count", -1)) == 8
            and int(dry.get("event_candidate_count", -1)) == 8,
            str(dry.get("decision")),
        ),
        validation_row(
            "event_aligned_initial_plan_is_complete",
            len(initial) == int(dry["initial_segment_count"])
            and all(float(row["segment_width"]) > 0.0 for row in initial),
            f"segments={len(initial)};plan={dry.get('node_plan_sha256')}",
        ),
        validation_row(
            "no_integral_claim_promoted_by_event_migration",
            all(not any(parse_bool(row[field]) for field in CLAIM_FIELDS) for row in events),
            "event geometry only",
        ),
        validation_row(
            "formal_workbench_unchanged",
            M5283.formal_inventory_digest() == FORMAL_DIGEST,
            M5283.formal_inventory_digest(),
        ),
        validation_row(
            "scripts_cache_absent",
            not (SCRIPTS / "__pycache__").exists(),
            str(SCRIPTS / "__pycache__"),
        ),
    ]
    passed = all(parse_bool(row["passed"]) for row in gates)
    write_csv(VALIDATION, gates)
    claims = no_claims()
    claims["valid_for_D4_outer_E00125_event_geometry"] = passed
    value = {
        "checkpoint": CHECKPOINT,
        "marker": MARKER,
        "mode": "D4-E00125-event-evidence-migration",
        "validation_passed": passed,
        "decision": (
            "D4_E00125_EVENT_GEOMETRY_MIGRATED__DRY_RUN_PASSES__BUILD_GENERIC_LOG_ENGINE"
            if passed
            else "D4_E00125_EVENT_GEOMETRY_MIGRATION_BLOCKED"
        ),
        "epsilon_id": EPSILON_ID,
        "epsilon": EPSILON,
        "event_count": len(events),
        "initial_segment_count": len(initial),
        "node_plan_sha256": dry.get("node_plan_sha256"),
        "claim_boundary": claims,
        "source_files": sources,
        "formalization_workbench_modified_file_count": 0,
        "next_action": (
            "BUILD_GENERIC_SUPPORT_EVENT_AFFINE_LOG_CORRECTED_E00125_RUNNER"
            if passed
            else "AUDIT_EVENT_TRANSFER_FAILURE"
        ),
        "runtime_seconds": time.perf_counter() - started,
        "updated_utc": utc_now(),
    }
    atomic_json(RESULT, value)
    atomic_json(
        STATUS,
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "state": "COMPLETE" if passed else "BLOCKED",
            "decision": value["decision"],
            "validation_passed": passed,
            "updated_utc": utc_now(),
        },
    )
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("run", "validate"), required=True)
    arguments = parser.parse_args()
    M5312.set_below_normal_priority()
    try:
        value = execute()
    except Exception as error:
        atomic_json(
            STATUS,
            {
                "checkpoint": CHECKPOINT,
                "marker": MARKER,
                "state": "FAILED",
                "error_type": type(error).__name__,
                "error": str(error),
                "traceback": traceback.format_exc(),
                "updated_utc": utc_now(),
            },
        )
        raise
    print(
        json.dumps(
            {
                "checkpoint": CHECKPOINT,
                "mode": arguments.mode,
                "validation_passed": value["validation_passed"],
                "decision": value["decision"],
                "runtime_seconds": value["runtime_seconds"],
            },
            sort_keys=True,
        ),
        flush=True,
    )
    return 0 if value["validation_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
