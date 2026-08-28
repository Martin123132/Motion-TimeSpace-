from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import math
import os
from pathlib import Path
import sys
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
WRAPPER_5351 = SCRIPTS / "Y5_R2FR_5351_D4_E0025_coefficient_extractor.py"
REFINEMENT_SCRIPT = SCRIPTS / "Y5_R2FR_5352_D4_E0025_branch_coordinate_refinement.py"

MIGRATION_RESULT = (
    FUNCTIONAL_RG
    / "5350"
    / "E0025"
    / "D4_E0025_affine_holdout_preregistration_result.json"
)
MIGRATION_VALIDATION = (
    FUNCTIONAL_RG
    / "5350"
    / "E0025"
    / "D4_E0025_affine_holdout_preregistration_validation.csv"
)
SUPPORT = FUNCTIONAL_RG / "5351" / "E0025" / "support"
ENDPOINT_RESULT = SUPPORT / "D4_E0025_support_endpoint_result.json"
ENDPOINT_COEFFICIENTS = SUPPORT / "D4_E0025_support_endpoint_coefficients.csv"
ENDPOINT_VALIDATION = SUPPORT / "D4_E0025_support_endpoint_validation.csv"
REFINEMENT = FUNCTIONAL_RG / "5352" / "E0025" / "branch-geometry"
REFINED_EVENTS = REFINEMENT / "D4_E0025_bracket_refined_events.csv"
REFINEMENT_AUDIT = REFINEMENT / "D4_E0025_branch_coordinate_refinement_audit.csv"
REFINEMENT_RESULT = REFINEMENT / "D4_E0025_branch_coordinate_refinement_result.json"
REFINEMENT_VALIDATION = (
    REFINEMENT / "D4_E0025_branch_coordinate_refinement_validation.csv"
)
REFINEMENT_SOURCE_REGISTER = REFINEMENT / "source_register.csv"

EPSILON_ID = "E0025"
EPSILON = 0.0025
ALL_EVENT_IDS = [f"E{index:02d}" for index in range(1, 9)]
BRANCH_EVENT_IDS = ["E04", "E05", "E06", "E07"]
REFINEMENT_METHOD = "CHECKPOINT_5337_BRANCH_EXISTENCE_BISECTION_MIDPOINT"
REFINEMENT_ERROR_BOUND = 1.0e-11
REFINEMENT_ITERATIONS = 27
CLAIM = "valid_for_D4_E0025_branch_event_coordinate_refinement"


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise ImportError(path)
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


M5351 = load_module("mts_5353_E0025_parent", WRAPPER_5351)
PARENT = M5351.ALL_EIGHT
ORIGINAL_SOURCE_PATHS = PARENT.source_paths
ORIGINAL_PREFLIGHT = PARENT.preflight


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def parse_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() in {"1", "true", "yes"}


def expected_event_path(epsilon_id: str) -> Path:
    if epsilon_id == EPSILON_ID:
        return REFINED_EVENTS
    return PARENT.FUNCTIONAL_RG / "5334" / epsilon_id / "D4_outer_refined_support_events.csv"


def refined_source_paths(
    epsilon_id: str,
    migration_result: Path,
    migration_validation: Path,
    endpoint_result: Path,
    endpoint_coefficients: Path,
    endpoint_validation: Path,
) -> list[Path]:
    paths = ORIGINAL_SOURCE_PATHS(
        epsilon_id,
        migration_result,
        migration_validation,
        endpoint_result,
        endpoint_coefficients,
        endpoint_validation,
    )
    paths.extend(
        [
            Path(__file__).resolve(),
            REFINEMENT_SCRIPT,
            REFINEMENT_AUDIT,
            REFINEMENT_RESULT,
            REFINEMENT_VALIDATION,
            REFINEMENT_SOURCE_REGISTER,
        ]
    )
    unique: list[Path] = []
    seen: set[Path] = set()
    for path in paths:
        resolved = path.resolve()
        if resolved not in seen:
            seen.add(resolved)
            unique.append(resolved)
    return unique


def refinement_checks() -> dict[str, bool]:
    required = [
        REFINED_EVENTS,
        REFINEMENT_AUDIT,
        REFINEMENT_RESULT,
        REFINEMENT_VALIDATION,
        REFINEMENT_SOURCE_REGISTER,
        REFINEMENT_SCRIPT,
    ]
    if not all(path.is_file() for path in required):
        return {"refinement_inputs_exist": False}
    result = read_json(REFINEMENT_RESULT)
    validations = read_csv(REFINEMENT_VALIDATION)
    events = read_csv(REFINED_EVENTS)
    audit = read_csv(REFINEMENT_AUDIT)
    result_sources_current, result_source_count = PARENT.source_chain_current(result)
    branch = [row for row in events if row.get("event_type") == "BRANCH_DEATH"]
    return {
        "refinement_inputs_exist": True,
        "refinement_result_passes": result.get("validation_passed") is True
        and result.get("claim_boundary", {}).get(CLAIM) is True
        and result.get("decision")
        == "D4_E0025_BRANCH_COORDINATES_BRACKET_REFINED__RERUN_ALL_EIGHT_COEFFICIENT",
        "refinement_identity_matches": result.get("epsilon_id") == EPSILON_ID
        and math.isclose(float(result.get("epsilon", math.nan)), EPSILON, abs_tol=1.0e-15)
        and Path(str(result.get("refined_event_path", ""))).resolve()
        == REFINED_EVENTS.resolve(),
        "refinement_validation_passes": bool(validations)
        and all(parse_bool(row.get("passed")) for row in validations),
        "refinement_source_chain_is_current": result_sources_current
        and result_source_count > 0,
        "all_eight_refined_events_present": [row.get("event_id") for row in events]
        == ALL_EVENT_IDS,
        "four_refined_branch_events_present": [row.get("event_id") for row in branch]
        == BRANCH_EVENT_IDS,
        "branch_coordinates_use_frozen_bisection": all(
            row.get("coordinate_refinement_method") == REFINEMENT_METHOD
            and float(row.get("coordinate_refinement_root_width_bound", math.inf))
            == 2.0 * REFINEMENT_ERROR_BOUND
            and float(row.get("event_coordinate_error_estimate", math.inf))
            <= REFINEMENT_ERROR_BOUND
            and int(row.get("iteration_count", -1)) == REFINEMENT_ITERATIONS
            and parse_bool(row.get("event_contract_passes"))
            and parse_bool(row.get(CLAIM))
            for row in branch
        ),
        "refinement_audit_passes": [row.get("event_id") for row in audit]
        == BRANCH_EVENT_IDS
        and all(
            parse_bool(row.get("new_interval_is_inside_old_error_disk"))
            and parse_bool(row.get("targeted_event_contract_passes"))
            and float(row.get("new_coordinate_error", math.inf))
            < float(row.get("old_coordinate_error", -math.inf))
            for row in audit
        ),
    }


def refined_preflight(
    epsilon_id: str,
    migration_result: Path,
    migration_validation: Path,
    endpoint_result: Path,
    endpoint_coefficients: Path,
    endpoint_validation: Path,
) -> dict[str, Any]:
    base = ORIGINAL_PREFLIGHT(
        epsilon_id,
        migration_result,
        migration_validation,
        endpoint_result,
        endpoint_coefficients,
        endpoint_validation,
    )
    checks = {**base["checks"], **refinement_checks()}
    base["checks"] = checks
    base["all_pass"] = all(checks.values())
    base["branch_event_coordinate_source"] = str(REFINED_EVENTS.resolve())
    base["branch_event_coordinate_error_bound"] = REFINEMENT_ERROR_BOUND
    return base


PARENT.expected_event_path = expected_event_path
PARENT.source_paths = refined_source_paths
PARENT.preflight = refined_preflight


def arguments(output_dir: Path | None, dry_run: bool) -> argparse.Namespace:
    return argparse.Namespace(
        stage="all-eight",
        geometry_result=MIGRATION_RESULT,
        geometry_validation=MIGRATION_VALIDATION,
        endpoint_result=ENDPOINT_RESULT,
        endpoint_coefficients=ENDPOINT_COEFFICIENTS,
        endpoint_validation=ENDPOINT_VALIDATION,
        output_dir=output_dir,
        dry_run=dry_run,
    )


def run(output_dir: Path | None, dry_run: bool) -> dict[str, Any]:
    result = M5351.run_all_eight(arguments(output_dir, dry_run))
    if dry_run:
        return result
    assert output_dir is not None
    output = output_dir.resolve()
    result_path = output / "D4_E0025_all_eight_endpoint_result.json"
    result["branch_event_coordinate_source"] = str(REFINED_EVENTS.resolve())
    result["branch_event_coordinate_error_bound"] = REFINEMENT_ERROR_BOUND
    result["branch_event_coordinate_refinement_claim_verified"] = True
    result["refined_runner"] = str(Path(__file__).resolve())
    result["refined_runner_sha256"] = M5351.digest(Path(__file__).resolve())
    M5351.atomic_json(result_path, result)
    return result


def self_test() -> dict[str, Any]:
    claims = PARENT.no_claims(EPSILON_ID)
    sources = refined_source_paths(
        EPSILON_ID,
        MIGRATION_RESULT,
        MIGRATION_VALIDATION,
        ENDPOINT_RESULT,
        ENDPOINT_COEFFICIENTS,
        ENDPOINT_VALIDATION,
    )
    checks = {
        "refined_event_path_is_installed": PARENT.expected_event_path(EPSILON_ID).resolve()
        == REFINED_EVENTS.resolve(),
        "refinement_sources_are_registered": all(
            path.resolve() in sources
            for path in [
                Path(__file__),
                REFINEMENT_SCRIPT,
                REFINEMENT_RESULT,
                REFINEMENT_VALIDATION,
                REFINED_EVENTS,
            ]
        ),
        "downstream_claims_start_false": all(value is False for value in claims.values()),
    }
    return {"mode": "self-test", "checks": checks, "all_pass": all(checks.values())}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parsed = parser.parse_args()
    if parsed.self_test:
        result = self_test()
    else:
        if parsed.output_dir is None and not parsed.dry_run:
            parser.error("--output-dir is required unless --dry-run is used")
        result = run(parsed.output_dir, parsed.dry_run)
    print(json.dumps(result, indent=2, sort_keys=True))
    passed = result.get("all_pass", result.get("validation_passed", False))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
