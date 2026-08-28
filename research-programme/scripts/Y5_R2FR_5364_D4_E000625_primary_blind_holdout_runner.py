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


ROOT = Path(__file__).resolve().parents[2]
POST = Path(__file__).resolve().parents[1]
SCRIPTS = POST / "scripts"
FORMAL = ROOT / "formalization-workbench"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
RESIDUALS = POST / "source-intake" / "mts_residuals"
SCRIPT_5334 = SCRIPTS / "Y5_R2FR_5334_D4_outer_regulator_ladder_controller.py"

SOURCE_CANDIDATES = (
    FUNCTIONAL_RG / "5334" / "E0025" / "D4_outer_support_event_candidates.csv"
)
PRE_FREEZE_EVENTS = (
    FUNCTIONAL_RG / "5334" / "E000625" / "D4_outer_refined_support_events.csv"
)
SOURCE_EVENT_SCAN = FUNCTIONAL_RG / "5337" / "D4_targeted_event_regulator_scan.csv"
MIGRATION_LEDGER = (
    FUNCTIONAL_RG
    / "5347"
    / "E000625"
    / "migration"
    / "D4_E000625_event_evidence_migration.csv"
)
MIGRATION_RESULT = (
    FUNCTIONAL_RG
    / "5347"
    / "E000625"
    / "migration"
    / "D4_E000625_event_evidence_migration_result.json"
)
MIGRATION_VALIDATION = (
    FUNCTIONAL_RG
    / "5347"
    / "E000625"
    / "migration"
    / "D4_E000625_event_evidence_migration_validation.csv"
)
FREEZE_RESULT_5363 = FUNCTIONAL_RG / "5363" / "D4_complete_fixed_A_fit_result.json"
FREEZE_PREDICTIONS_5363 = (
    FUNCTIONAL_RG / "5363" / "D4_complete_fixed_A_dual_holdout_predictions.csv"
)
FREEZE_VALIDATION_5363 = (
    FUNCTIONAL_RG / "5363" / "D4_complete_fixed_A_fit_validation.csv"
)

OUTPUT = FUNCTIONAL_RG / "5364" / "E000625"
FROZEN_EVENTS = OUTPUT / "D4_E000625_preintegration_frozen_events.csv"
RESULT = OUTPUT / "D4_E000625_primary_blind_holdout_runner_result.json"
VALIDATION = OUTPUT / "D4_E000625_primary_blind_holdout_runner_validation.csv"
SOURCE_REGISTER = OUTPUT / "source_register.csv"
STATUS = OUTPUT / "status.json"
RESIDUAL_VALIDATION = RESIDUALS / "P8_Y5_BRR545_5364_VALIDATION.csv"
DOCUMENT = POST / "5364-Y5-R2FR-D4-E000625-primary-blind-holdout-runner.md"

CHECKPOINT = 5364
MARKER = "MTS_5364_D4_E000625_PRIMARY_BLIND_HOLDOUT_RUNNER"
REVISION = "D4-E000625-primary-blind-holdout-runner-v1"
EPSILON_ID = "E000625"
EPSILON = 0.000625
MAXIMUM_ADAPTIVE_DEPTH = 6
EXPECTED_EVENT_COUNT = 8
EXPECTED_INITIAL_SEGMENT_COUNT = 26
FORMAL_DIGEST = "0ec1bc6012136ffc6b28a1512aca6ce712b6decd2ff793310a9bd61775f3db1f"

CLAIM_FIELDS = (
    "valid_for_D4_outer_E000625_event_geometry",
    "valid_for_D4_outer_E000625_fixed_decay_integral",
    "valid_for_D4_E000625_complete_family_holdout_compatibility",
    "valid_for_D4_numeric_remainder_bound",
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
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


M5334 = load_module("mts_5334_for_5364", SCRIPT_5334)
M5326 = M5334.M5326
M5283 = M5334.M5283


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
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def atomic_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"empty CSV payload: {path}")
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(path)


def atomic_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def validation_row(gate: str, passed: bool, detail: Any) -> dict[str, Any]:
    return {"gate": gate, "passed": bool(passed), "detail": str(detail)}


def no_claims() -> dict[str, bool]:
    return {field: False for field in CLAIM_FIELDS}


def freeze_preintegration_events() -> None:
    if FROZEN_EVENTS.is_file():
        return
    if not PRE_FREEZE_EVENTS.is_file():
        raise FileNotFoundError(PRE_FREEZE_EVENTS)
    rows = read_csv(PRE_FREEZE_EVENTS)
    if len(rows) != EXPECTED_EVENT_COUNT:
        raise RuntimeError("pre-freeze E000625 event inventory is incomplete")
    atomic_csv(FROZEN_EVENTS, rows)


def source_geometry_is_valid() -> tuple[bool, dict[str, Any]]:
    required = (
        SOURCE_CANDIDATES,
        FROZEN_EVENTS,
        SOURCE_EVENT_SCAN,
        MIGRATION_LEDGER,
        MIGRATION_RESULT,
        MIGRATION_VALIDATION,
        FREEZE_RESULT_5363,
        FREEZE_PREDICTIONS_5363,
        FREEZE_VALIDATION_5363,
    )
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        return False, {"missing": missing}
    candidates = read_csv(SOURCE_CANDIDATES)
    events = read_csv(FROZEN_EVENTS)
    migration = {row["event_id"]: row for row in read_csv(MIGRATION_LEDGER)}
    scan = {
        row["event_id"]: row
        for row in read_csv(SOURCE_EVENT_SCAN)
        if row["epsilon_id"] == EPSILON_ID
    }
    migration_result = read_json(MIGRATION_RESULT)
    migration_validation = read_csv(MIGRATION_VALIDATION)
    freeze_result = read_json(FREEZE_RESULT_5363)
    freeze_predictions = read_csv(FREEZE_PREDICTIONS_5363)
    freeze_validation = read_csv(FREEZE_VALIDATION_5363)
    primary_predictions = [
        row for row in freeze_predictions if row["holdout_epsilon_id"] == EPSILON_ID
    ]
    expected_event_ids = [f"E{index:02d}" for index in range(1, 9)]
    topology = [row["event_type"] for row in events]
    checks = {
        "checkpoint_5363_freeze_is_valid": freeze_result.get("validation_passed")
        is True
        and freeze_result.get("primary_holdout_epsilon_id") == EPSILON_ID
        and len(primary_predictions) == 1
        and parse_bool(primary_predictions[0]["frozen_before_accepted_holdout_value"])
        and not parse_bool(
            primary_predictions[0]["comparison_to_measured_holdout_performed"]
        )
        and all(parse_bool(row["passed"]) for row in freeze_validation),
        "checkpoint_5347_migration_is_valid": migration_result.get(
            "validation_passed"
        )
        is True
        and migration_result.get("claim_boundary", {}).get(
            "valid_for_D4_outer_E000625_event_geometry"
        )
        is True
        and all(parse_bool(row["passed"]) for row in migration_validation),
        "eight_candidates_and_events_are_ordered": len(candidates)
        == len(events)
        == len(migration)
        == len(scan)
        == EXPECTED_EVENT_COUNT
        and [row["event_id"] for row in events] == expected_event_ids
        and [row["candidate_id"] for row in candidates]
        == [f"C{index:02d}" for index in range(1, 9)]
        and sorted(migration) == sorted(scan) == expected_event_ids,
        "event_topology_is_three_entries_four_deaths_one_exit": topology.count(
            "SUPPORT_ENTRY"
        )
        == 3
        and topology.count("BRANCH_DEATH") == 4
        and topology.count("SUPPORT_EXIT") == 1,
        "all_event_contracts_and_coordinates_are_source_owned": all(
            parse_bool(row["event_contract_passes"])
            and parse_bool(migration[row["event_id"]]["migrated_event_contract_passes"])
            and parse_bool(scan[row["event_id"]]["targeted_event_contract_passes"])
            and math.isclose(
                float(row["event_coordinate"]),
                float(migration[row["event_id"]]["migrated_root_coordinate"]),
                rel_tol=0.0,
                abs_tol=1.0e-15,
            )
            and math.isclose(
                float(row["event_coordinate"]),
                float(scan[row["event_id"]]["event_coordinate"]),
                rel_tol=0.0,
                abs_tol=1.0e-15,
            )
            for row in events
        ),
    }
    return all(checks.values()), checks


def target_candidate_rows() -> list[dict[str, Any]]:
    rows = [dict(row) for row in read_csv(SOURCE_CANDIDATES)]
    M5334.write_csv(
        M5326.EVENT_CANDIDATES,
        rows,
        ["candidate_id", "x_panel_index", "term_id", "primary_surface_id"],
    )
    return rows


def target_events_only() -> list[dict[str, Any]]:
    valid, detail = source_geometry_is_valid()
    if not valid:
        raise RuntimeError(f"validated E000625 source geometry failed: {detail}")
    rows = [dict(row) for row in read_csv(FROZEN_EVENTS)]
    current_contract_hash = digest(M5326.CONTRACT_5325)
    current_pole_hash = digest(M5326.POLES_5325)
    for row in rows:
        row["contract_sha256"] = current_contract_hash
        row["parent_pole_sha256"] = current_pole_hash
        row["candidate_source"] = (
            "CHECKPOINT_5347_FROZEN_5337_E000625_EVENT_GEOMETRY"
        )
        row["transfer_source_path"] = str(FROZEN_EVENTS.resolve())
        row["transfer_source_sha256"] = digest(FROZEN_EVENTS)
    M5334.write_csv(
        M5326.EVENTS,
        rows,
        ["event_id", "x_panel_index", "term_id", "primary_surface_id"],
    )
    return rows


def write_target_event_states() -> list[dict[str, Any]]:
    scan_by_id = {
        row["event_id"]: row
        for row in read_csv(SOURCE_EVENT_SCAN)
        if row["epsilon_id"] == EPSILON_ID
    }
    rows: list[dict[str, Any]] = []
    for event in read_csv(FROZEN_EVENTS):
        scanned = scan_by_id[event["event_id"]]
        rows.append(
            {
                "x_panel_index": int(event["x_panel_index"]),
                "term_id": event["term_id"],
                "primary_surface_id": event["primary_surface_id"],
                "absolute_soft_cosine": float(event["event_coordinate"]),
                "branch_exists": True,
                "pole_real": float(event["event_pole_real"]),
                "pole_imaginary": float(scanned["pole_imaginary"]),
                "support_id": f"TRANSFERRED_{event['term_id']}_SUPPORT",
                "support_energy_lower": float(event["event_support_lower"]),
                "support_energy_upper": float(event["event_support_upper"]),
                "signed_support_margin": float(
                    event["event_signed_support_margin"]
                ),
                "inside_reduced_term_support": event["event_type"]
                != "BRANCH_DEATH",
                "state_source": "CHECKPOINT_5347_FROZEN_5337_E000625_EVENT_GEOMETRY",
                **no_claims(),
            }
        )
    M5334.write_csv(
        M5326.EVENT_STATES,
        rows,
        [
            "x_panel_index",
            "term_id",
            "primary_surface_id",
            "absolute_soft_cosine",
        ],
    )
    return rows


def configure_target() -> dict[str, Path]:
    valid, detail = source_geometry_is_valid()
    if not valid:
        raise RuntimeError(f"E000625 source geometry failed: {detail}")
    M5334.configure_ladder()
    M5334.D4_TARGET_MAXIMUM_ADAPTIVE_DEPTH[EPSILON_ID] = MAXIMUM_ADAPTIVE_DEPTH
    paths = M5334.configure_D4_target(EPSILON_ID)
    expected_source = (FUNCTIONAL_RG / "5334" / EPSILON_ID).resolve()
    if paths["source"].resolve() != expected_source or M5326.SOURCE.resolve() != expected_source:
        raise RuntimeError(
            f"refusing cross-channel target routing: paths={paths['source'].resolve()}; "
            f"module={M5326.SOURCE.resolve()}; expected={expected_source}"
        )
    M5326.EXPECTED_EVENT_COUNT = EXPECTED_EVENT_COUNT
    M5326.event_candidate_rows = target_candidate_rows
    M5326.derive_events = target_events_only
    return paths


def build_dry_run() -> dict[str, Any]:
    freeze_preintegration_events()
    configure_target()
    dry = M5334.d4_refinement_dry_run()
    write_target_event_states()
    dry["event_source_mode"] = "CHECKPOINT_5347_FROZEN_5337_E000625_EVENT_GEOMETRY"
    dry["event_source_path"] = str(FROZEN_EVENTS.resolve())
    dry["event_source_sha256"] = digest(FROZEN_EVENTS)
    dry["maximum_adaptive_depth"] = MAXIMUM_ADAPTIVE_DEPTH
    dry["checks"]["checkpoint_5347_E000625_event_geometry_passes"] = (
        source_geometry_is_valid()[0]
    )
    dry["checks"]["checkpoint_5363_primary_holdout_was_frozen"] = True
    dry["acceptance_passed"] = all(dry["checks"].values())
    dry["decision"] = (
        "DRY_RUN_ACCEPTED__RUN_D4_OUTER_E000625_PRIMARY_BLIND_HOLDOUT"
        if dry["acceptance_passed"]
        else "D4_OUTER_E000625_PRIMARY_BLIND_HOLDOUT_DRY_RUN_BLOCKED"
    )
    M5334.atomic_json(M5326.DRY_RUN, dry)
    return dry


def direct_sources() -> tuple[Path, ...]:
    return (
        Path(__file__).resolve(),
        SCRIPT_5334,
        SOURCE_CANDIDATES,
        FROZEN_EVENTS,
        SOURCE_EVENT_SCAN,
        MIGRATION_LEDGER,
        MIGRATION_RESULT,
        MIGRATION_VALIDATION,
        FREEZE_RESULT_5363,
        FREEZE_PREDICTIONS_5363,
        FREEZE_VALIDATION_5363,
    )


def write_checkpoint(dry: dict[str, Any]) -> dict[str, Any]:
    valid, source_checks = source_geometry_is_valid()
    measurement_result = (
        FUNCTIONAL_RG
        / "5334"
        / EPSILON_ID
        / "D4_outer_event_aligned_E000625_result.json"
    )
    validations = [
        validation_row("source_geometry_passes", valid, source_checks),
        validation_row(
            "dry_run_passes_with_eight_events",
            dry.get("acceptance_passed") is True
            and int(dry.get("refined_event_count", -1)) == EXPECTED_EVENT_COUNT
            and int(dry.get("initial_segment_count", -1))
            == EXPECTED_INITIAL_SEGMENT_COUNT,
            dry.get("decision"),
        ),
        validation_row(
            "depth_six_is_preregistered_before_E000625_integration",
            int(dry.get("maximum_adaptive_depth", -1)) == MAXIMUM_ADAPTIVE_DEPTH,
            dry.get("node_plan_sha256"),
        ),
        validation_row(
            "E000625_measurement_is_absent_at_runner_freeze",
            not measurement_result.is_file(),
            measurement_result,
        ),
        validation_row(
            "D4_target_is_routed_only_to_5334_E000625",
            M5326.SOURCE.resolve()
            == (FUNCTIONAL_RG / "5334" / EPSILON_ID).resolve(),
            M5326.SOURCE.resolve(),
        ),
        validation_row(
            "all_holdout_and_broad_claims_remain_false",
            all(value is False for value in no_claims().values()),
            no_claims(),
        ),
        validation_row(
            "formal_workbench_unchanged",
            M5283.formal_inventory_digest() == FORMAL_DIGEST,
            M5283.formal_inventory_digest(),
        ),
        validation_row(
            "scripts_cache_absent",
            not (SCRIPTS / "__pycache__").exists(),
            SCRIPTS / "__pycache__",
        ),
    ]
    passed = all(parse_bool(row["passed"]) for row in validations)
    source_rows = [
        {
            "path": str(path.resolve()),
            "sha256": digest(path),
            "exists": path.is_file(),
            **no_claims(),
        }
        for path in direct_sources()
    ]
    result = {
        "mode": "D4-E000625-primary-blind-holdout-runner",
        "checkpoint": CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "epsilon_id": EPSILON_ID,
        "epsilon": EPSILON,
        "validation_passed": passed,
        "decision": (
            "D4_E000625_PRIMARY_BLIND_HOLDOUT_DEPTH6_PREREGISTERED__RUN_RESUMABLE_INTEGRAL"
            if passed
            else "D4_E000625_SOURCE_GEOMETRY_OR_DRY_RUN_BLOCKED"
        ),
        "event_count": dry.get("refined_event_count"),
        "initial_segment_count": dry.get("initial_segment_count"),
        "maximum_adaptive_depth": dry.get("maximum_adaptive_depth"),
        "node_plan_sha256": dry.get("node_plan_sha256"),
        "frozen_prediction_source_path": str(FREEZE_PREDICTIONS_5363.resolve()),
        "frozen_prediction_source_sha256": digest(FREEZE_PREDICTIONS_5363),
        "claim_boundary": no_claims(),
        "formalization_workbench_modified_file_count": 0,
        "updated_utc": utc_now(),
    }
    OUTPUT.mkdir(parents=True, exist_ok=True)
    atomic_csv(VALIDATION, validations)
    atomic_csv(RESIDUAL_VALIDATION, validations)
    atomic_csv(SOURCE_REGISTER, source_rows)
    atomic_json(RESULT, result)
    atomic_json(
        STATUS,
        {
            "state": "complete" if passed else "blocked",
            "decision": result["decision"],
            "updated_utc": result["updated_utc"],
        },
    )
    DOCUMENT.write_text(
        "\n".join(
            [
                "# 5364 - D4 E000625 primary blind holdout runner",
                "",
                "## Decision",
                "",
                f"`{result['decision']}`",
                "",
                "Checkpoint 5363 froze the complete-family E000625 prediction before this finite-rung measurement. Checkpoint 5347's validated eight-event geometry is copied into an immutable pre-integration source and installed into the resumable D4 pipeline.",
                "",
                f"- events: `{result['event_count']}`;",
                f"- initial segments: `{result['initial_segment_count']}`;",
                f"- preregistered maximum adaptive depth: `{result['maximum_adaptive_depth']}`;",
                f"- plan hash: `{result['node_plan_sha256']}`.",
                "",
                "No holdout compatibility, remainder, regulator-zero, angular, UV, local-GR, or full-MTS claim is made by this setup checkpoint.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    return result


def run_integral(runtime_seconds: float) -> dict[str, Any]:
    configure_target()
    dry = M5334.d4_load_validated_refinement_dry_run()
    if dry.get("event_source_mode") != "CHECKPOINT_5347_FROZEN_5337_E000625_EVENT_GEOMETRY":
        dry = build_dry_run()
    write_target_event_states()
    raw = M5326.execute(runtime_seconds)
    source_paths = {
        Path(row["path"])
        for row in raw.get("source_files", [])
        if Path(row["path"]).is_file()
    }
    source_paths.update(direct_sources())
    raw["source_files"] = [
        {"path": str(path.resolve()), "sha256": digest(path)}
        for path in sorted(source_paths, key=lambda path: str(path).lower())
    ]
    result = M5334.canonicalize_refinement_result(raw)
    print(
        json.dumps(
            {
                "mode": "run",
                "epsilon_id": EPSILON_ID,
                "acceptance_passed": result["acceptance_passed"],
                "decision": result["decision"],
                "completed_full_run": result["completed_full_run"],
                "encountered_node_count": result["encountered_node_count"],
                "completed_node_count": result["completed_node_count"],
                "runtime_seconds": result["runtime_seconds"],
            },
            sort_keys=True,
        )
    )
    return result


def validate_integral() -> dict[str, Any]:
    configure_target()
    return M5334.validate_refinement_outputs()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("dry-run", "run", "validate"), required=True)
    parser.add_argument("--max-runtime-hours", type=float, default=4.0)
    arguments = parser.parse_args()
    M5334.M5312.set_below_normal_priority()
    started = time.perf_counter()
    if arguments.mode == "dry-run":
        dry = build_dry_run()
        payload = write_checkpoint(dry)
        payload["runtime_seconds"] = time.perf_counter() - started
        print(json.dumps(payload, indent=2, sort_keys=True))
    elif arguments.mode == "run":
        payload = run_integral(max(arguments.max_runtime_hours, 0.0) * 3600.0)
    else:
        payload = validate_integral()
        print(json.dumps(payload, indent=2, sort_keys=True))
    accepted = payload.get("validation_passed", payload.get("acceptance_passed", False))
    paused = "PAUSED" in str(payload.get("decision", ""))
    return 0 if accepted or paused else 1


if __name__ == "__main__":
    raise SystemExit(main())
