from __future__ import annotations

import argparse
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
RESIDUALS = POST / "source-intake" / "mts_residuals"
BASELINE_RESULT = FUNCTIONAL_RG / "5349" / "D4_three_regulator_coefficient_result.json"
BASELINE_INPUTS = FUNCTIONAL_RG / "5349" / "D4_three_regulator_coefficient_inputs.csv"
BASELINE_VALIDATION = FUNCTIONAL_RG / "5349" / "D4_three_regulator_coefficient_validation.csv"
CANONICAL_E0025 = FUNCTIONAL_RG / "5340" / "D4_E0025_log_corrected_canonical_result.json"
CANONICAL_E0025_VALIDATION = RESIDUALS / "P8_Y5_BRR545_5340_VALIDATION.csv"
E0025_SOURCE = FUNCTIONAL_RG / "5334" / "E0025"
EVENTS = E0025_SOURCE / "D4_outer_refined_support_events.csv"
CANDIDATES = E0025_SOURCE / "D4_outer_support_event_candidates.csv"
DRY_RUN = E0025_SOURCE / "D4_outer_event_aligned_E0025_dry_run.json"
CONTRACT = E0025_SOURCE / "D4_outer_reduced_MC04_cubature_contract.csv"
POLES = E0025_SOURCE / "D4_outer_E0025_geometric_poles.csv"
SCAN = FUNCTIONAL_RG / "5337" / "D4_targeted_event_regulator_scan.csv"
SCAN_RESULT = FUNCTIONAL_RG / "5337" / "D4_regulator_fold_double_scaling_contrast_result.json"
SCAN_VALIDATION = RESIDUALS / "P8_Y5_BRR545_5337_VALIDATION.csv"
FUTURE_HOLDOUT = FUNCTIONAL_RG / "5351" / "E0025" / "all-eight" / "D4_E0025_all_eight_endpoint_result.json"
EPSILON_ID = "E0025"
EPSILON = 0.0025
EXPECTED_IDS = [f"E{index:02d}" for index in range(1, 9)]
SUPPORT_IDS = ["E01", "E02", "E03", "E08"]
BRANCH_IDS = ["E04", "E05", "E06", "E07"]
CLAIM_GEOMETRY = "valid_for_D4_outer_E0025_event_geometry"
CLAIM_PREREGISTERED = "valid_for_D4_E0025_affine_holdout_preregistration"
CLAIM_HOLDOUT = "valid_for_D4_four_regulator_affine_endpoint_coefficient_holdout"
DOWNSTREAM_FALSE = (
    CLAIM_HOLDOUT,
    "valid_for_D4_endpoint_coefficient_regulator_zero_limit",
    "valid_for_D4_outer_regulator_zero_limit",
    "valid_for_decay_angle_integral",
    "valid_for_full_angular_convergence",
    "valid_for_full_phase_space_coefficient",
    "valid_for_numeric_UV_claim",
    "valid_for_local_GR_claim",
    "valid_for_full_MTS_claim",
)
PREDICTIONS = (
    ("WIDE_BRACKET_2H_8H", {"E00125": 2.0 / 3.0, "E005": 1.0 / 3.0}),
    ("SMALL_EXTRAPOLATION_H_2H", {"E000625": -2.0, "E00125": 3.0}),
    ("OUTER_BRACKET_H_8H", {"E000625": 4.0 / 7.0, "E005": 3.0 / 7.0}),
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
    return {
        CLAIM_GEOMETRY: False,
        CLAIM_PREREGISTERED: False,
        **{claim: False for claim in DOWNSTREAM_FALSE},
    }


def validation_row(gate: str, passed: bool, detail: Any) -> dict[str, Any]:
    return {"gate": gate, "passed": bool(passed), "detail": str(detail)}


def recursive_source_chain_current(
    result_path: Path,
    visited: set[Path] | None = None,
) -> tuple[bool, int, list[str]]:
    resolved = result_path.resolve()
    visited = set() if visited is None else visited
    if resolved in visited:
        return True, 0, []
    visited.add(resolved)
    if not resolved.is_file():
        return False, 0, [f"missing:{resolved}"]
    try:
        payload = read_json(resolved)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return True, 0, []
    rows = payload.get("source_files", [])
    if not isinstance(rows, list):
        return False, 0, [f"malformed_source_files:{resolved}"]
    if not rows:
        return True, 0, []
    current = True
    count = 0
    failures: list[str] = []
    for row in rows:
        location = str(row.get("path", ""))
        expected = str(row.get("sha256", ""))
        source = Path(location)
        count += 1
        if not source.is_file() or len(expected) != 64 or digest(source) != expected:
            current = False
            failures.append(f"stale_or_missing:{location}")
            continue
        if source.suffix.lower() == ".json":
            nested_current, nested_count, nested_failures = recursive_source_chain_current(
                source, visited
            )
            current = current and nested_current
            count += nested_count
            failures.extend(nested_failures)
    return current, count, failures


def direct_source_chain_current(payload: dict[str, Any]) -> tuple[bool, int, list[str]]:
    rows = payload.get("source_files", [])
    if not isinstance(rows, list) or not rows:
        return False, 0, ["missing_or_malformed_direct_source_files"]
    failures: list[str] = []
    for row in rows:
        location = str(row.get("path", ""))
        expected = str(row.get("sha256", ""))
        source = Path(location)
        if not source.is_file() or len(expected) != 64 or digest(source) != expected:
            failures.append(f"stale_or_missing:{location}")
    return not failures, len(rows), failures


def coefficient_inputs() -> dict[str, dict[str, Any]]:
    rows = read_csv(BASELINE_INPUTS)
    values: dict[str, dict[str, Any]] = {}
    for row in rows:
        epsilon_id = row["epsilon_id"]
        values[epsilon_id] = {
            "epsilon": float(row["epsilon"]),
            "value": complex(
                float(row["A_finite_epsilon_real"]),
                float(row["A_finite_epsilon_imaginary"]),
            ),
            "radius": float(row["A_diagnostic_disk_radius"]),
            "result_path": Path(row["result_path"]),
            "result_sha256": row["result_sha256"],
            "input_contract_passes": parse_bool(row["input_contract_passes"]),
            "recursive_source_chain_passes": parse_bool(
                row["recursive_source_chain_passes"]
            ),
        }
    return values


def prediction_rows(inputs: dict[str, dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for prediction_id, weights in PREDICTIONS:
        centre = sum(
            (weight * inputs[epsilon_id]["value"] for epsilon_id, weight in weights.items()),
            0j,
        )
        radius = sum(
            abs(weight) * inputs[epsilon_id]["radius"]
            for epsilon_id, weight in weights.items()
        )
        rows.append(
            {
                "prediction_id": prediction_id,
                "target_epsilon_id": EPSILON_ID,
                "target_epsilon": EPSILON,
                "source_weights": "|".join(
                    f"{epsilon_id}:{weight:.17g}"
                    for epsilon_id, weight in weights.items()
                ),
                "predicted_A_real": centre.real,
                "predicted_A_imaginary": centre.imag,
                "predicted_A_magnitude": abs(centre),
                "predicted_A_disk_radius": radius,
                "future_contrast_definition": (
                    "A_E0025_minus_preregistered_prediction"
                ),
                "future_acceptance_rule": (
                    "abs(contrast)<=E0025_radius+predicted_A_disk_radius"
                ),
                **no_claims(),
            }
        )
    return rows


def run(output: Path) -> dict[str, Any]:
    started = time.perf_counter()
    output = output.resolve()
    result_path = output / "D4_E0025_affine_holdout_preregistration_result.json"
    prediction_path = output / "D4_E0025_affine_holdout_predictions.csv"
    validation_path = output / "D4_E0025_affine_holdout_preregistration_validation.csv"
    source_register = output / "source_register.csv"
    status_path = output / "status.json"
    source_paths = [
        Path(__file__).resolve(),
        BASELINE_RESULT,
        BASELINE_INPUTS,
        BASELINE_VALIDATION,
        CANONICAL_E0025,
        CANONICAL_E0025_VALIDATION,
        EVENTS,
        CANDIDATES,
        DRY_RUN,
        CONTRACT,
        POLES,
        SCAN,
        SCAN_RESULT,
        SCAN_VALIDATION,
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
    baseline = read_json(BASELINE_RESULT)
    baseline_validation = read_csv(BASELINE_VALIDATION)
    canonical = read_json(CANONICAL_E0025)
    canonical_validation = read_csv(CANONICAL_E0025_VALIDATION)
    scan_result = read_json(SCAN_RESULT)
    scan_validation = read_csv(SCAN_VALIDATION)
    events = read_csv(EVENTS)
    candidates = {row["candidate_id"]: row for row in read_csv(CANDIDATES)}
    scans = {
        row["event_id"]: row
        for row in read_csv(SCAN)
        if row["epsilon_id"] == EPSILON_ID
    }
    dry_run = read_json(DRY_RUN)
    inputs = coefficient_inputs()
    predictions = prediction_rows(inputs)
    baseline_current, baseline_source_count, baseline_failures = (
        recursive_source_chain_current(BASELINE_RESULT)
    )
    canonical_current, canonical_source_count, canonical_failures = (
        recursive_source_chain_current(CANONICAL_E0025)
    )
    canonical_direct_current, canonical_direct_count, canonical_direct_failures = (
        direct_source_chain_current(canonical)
    )
    expected_epsilons = {
        "E000625": 0.000625,
        "E00125": 0.00125,
        "E005": 0.005,
    }
    input_hashes_current = all(
        value["result_path"].is_file()
        and digest(value["result_path"]) == value["result_sha256"]
        and value["input_contract_passes"]
        and value["recursive_source_chain_passes"]
        for value in inputs.values()
    )
    current_contract_hash = digest(CONTRACT)
    current_pole_hash = digest(POLES)
    event_ids = [row["event_id"] for row in events]
    support_ids = [
        row["event_id"]
        for row in events
        if row["event_type"] in {"SUPPORT_ENTRY", "SUPPORT_EXIT"}
    ]
    branch_ids = [
        row["event_id"] for row in events if row["event_type"] == "BRANCH_DEATH"
    ]
    source_coordinates_match = all(
        event["event_id"] in scans
        and abs(
            float(scans[event["event_id"]]["source_E0025_event_coordinate"])
            - float(event["event_coordinate"])
        )
        <= 1.0e-14
        for event in events
    )
    gates = [
        validation_row(
            "all_sources_exist_and_are_hashed",
            all(row["exists"] and row["sha256"] != "MISSING" for row in sources),
            len(sources),
        ),
        validation_row(
            "three_regulator_training_gate_is_current_and_passes",
            baseline.get("validation_passed") is True
            and baseline.get("decision")
            == "D4_THREE_REGULATOR_AFFINE_COEFFICIENT_PASS__ACQUIRE_FOURTH_OR_REMAINDER_BOUND"
            and baseline.get("claim_boundary", {}).get(
                "valid_for_D4_three_regulator_affine_endpoint_coefficient_stability"
            )
            is True
            and baseline_current
            and baseline_source_count > 0
            and not baseline_failures
            and bool(baseline_validation)
            and all(parse_bool(row["passed"]) for row in baseline_validation),
            {"source_count": baseline_source_count, "failures": baseline_failures},
        ),
        validation_row(
            "training_inputs_are_exact_source_current_h_2h_8h_rows",
            set(inputs) == set(expected_epsilons)
            and all(
                abs(inputs[key]["epsilon"] - epsilon) <= 1.0e-15
                for key, epsilon in expected_epsilons.items()
            )
            and input_hashes_current,
            sorted((key, value["epsilon"]) for key, value in inputs.items()),
        ),
        validation_row(
            "accepted_E0025_fixed_rung_direct_chain_is_current",
            canonical.get("validation_passed") is True
            and canonical.get("acceptance_passed") is True
            and canonical.get("claim_boundary", {}).get(
                "valid_for_D4_outer_E0025_fixed_decay_integral"
            )
            is True
            and canonical_direct_current
            and canonical_direct_count > 0
            and not canonical_direct_failures
            and bool(canonical_validation)
            and all(parse_bool(row["passed"]) for row in canonical_validation),
            {
                "direct_source_count": canonical_direct_count,
                "direct_failures": canonical_direct_failures,
                "historical_recursive_source_count": canonical_source_count,
                "historical_recursive_chain_current": canonical_current,
                "historical_recursive_failures": canonical_failures,
            },
        ),
        validation_row(
            "E0025_geometry_has_exact_ordered_topology",
            event_ids == EXPECTED_IDS
            and support_ids == SUPPORT_IDS
            and branch_ids == BRANCH_IDS
            and sorted(scans) == EXPECTED_IDS
            and set(candidates) == {row["candidate_id"] for row in events},
            {"events": event_ids, "support": support_ids, "branch": branch_ids},
        ),
        validation_row(
            "E0025_event_and_scan_contracts_pass",
            all(parse_bool(row["event_contract_passes"]) for row in events)
            and all(parse_bool(row["targeted_event_contract_passes"]) for row in scans.values())
            and source_coordinates_match
            and all(
                row["contract_sha256"] == current_contract_hash
                and row["parent_pole_sha256"] == current_pole_hash
                for row in events
            ),
            {"source_coordinates_match": source_coordinates_match},
        ),
        validation_row(
            "E0025_one_sided_branch_candidates_are_unambiguous",
            all(
                parse_bool(candidates[event["candidate_id"]]["left_inside_support"])
                != parse_bool(candidates[event["candidate_id"]]["right_inside_support"])
                for event in events
                if event["event_id"] in BRANCH_IDS
            ),
            BRANCH_IDS,
        ),
        validation_row(
            "E0025_dry_run_and_regulator_scan_pass",
            dry_run.get("acceptance_passed") is True
            and int(dry_run.get("refined_event_count", -1)) == 8
            and int(dry_run.get("event_candidate_count", -1)) == 8
            and scan_result.get("validation_passed") is True
            and bool(scan_validation)
            and all(parse_bool(row["passed"]) for row in scan_validation),
            {"dry_run": dry_run.get("decision"), "scan": scan_result.get("decision")},
        ),
        validation_row(
            "three_holdout_predictions_are_finite_and_frozen",
            len(predictions) == 3
            and all(
                math.isfinite(float(row["predicted_A_real"]))
                and math.isfinite(float(row["predicted_A_imaginary"]))
                and math.isfinite(float(row["predicted_A_disk_radius"]))
                and float(row["predicted_A_disk_radius"]) >= 0.0
                for row in predictions
            ),
            [row["prediction_id"] for row in predictions],
        ),
        validation_row(
            "holdout_coefficient_was_absent_at_preregistration",
            not FUTURE_HOLDOUT.exists(),
            FUTURE_HOLDOUT,
        ),
        validation_row(
            "scripts_cache_absent",
            not (SCRIPTS / "__pycache__").exists(),
            SCRIPTS / "__pycache__",
        ),
    ]
    passed = all(parse_bool(row["passed"]) for row in gates)
    claims = no_claims()
    claims[CLAIM_GEOMETRY] = passed
    claims[CLAIM_PREREGISTERED] = passed
    for row in predictions:
        row[CLAIM_GEOMETRY] = passed
        row[CLAIM_PREREGISTERED] = passed
    atomic_csv(prediction_path, predictions)
    atomic_csv(validation_path, gates)
    atomic_csv(source_register, sources)
    result = {
        "mode": "D4-E0025-read-only-affine-holdout-preregistration",
        "epsilon_id": EPSILON_ID,
        "epsilon": EPSILON,
        "validation_passed": passed,
        "decision": (
            "D4_E0025_READ_ONLY_GEOMETRY_AND_AFFINE_HOLDOUT_PREREGISTERED__RUN_COEFFICIENT_EXTRACTION"
            if passed
            else "D4_E0025_HOLDOUT_PREREGISTRATION_BLOCKED"
        ),
        "training_epsilon_ids": ["E000625", "E00125", "E005"],
        "holdout_epsilon_id": EPSILON_ID,
        "prediction_count": len(predictions),
        "future_acceptance_rule": (
            "all three preregistered propagated contrast disks must contain zero"
        ),
        "source_geometry_is_read_only": True,
        "future_holdout_path": str(FUTURE_HOLDOUT.resolve()),
        "historical_recursive_E0025_source_chain_current": canonical_current,
        "historical_recursive_E0025_source_drift_count": len(canonical_failures),
        "historical_recursive_E0025_source_drifts": canonical_failures,
        "holdout_uses_revalidated_current_event_contracts_not_historical_deep_chain": True,
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
    inputs = {
        "E000625": {"value": 2.0 + 3.0j, "radius": 0.1},
        "E00125": {"value": 3.0 + 5.0j, "radius": 0.2},
        "E005": {"value": 9.0 + 17.0j, "radius": 0.3},
    }
    rows = prediction_rows(inputs)
    expected = 5.0 + 9.0j
    checks = {
        "all_affine_predictions_equal_holdout": all(
            abs(
                complex(row["predicted_A_real"], row["predicted_A_imaginary"])
                - expected
            )
            <= 1.0e-14
            for row in rows
        ),
        "three_prediction_rules_present": len(rows) == 3,
        "all_claims_start_false": all(
            not parse_bool(row[CLAIM_HOLDOUT]) for row in rows
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
