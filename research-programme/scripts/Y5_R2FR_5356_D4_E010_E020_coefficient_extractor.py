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
PARENT_5351 = SCRIPTS / "Y5_R2FR_5351_D4_E0025_coefficient_extractor.py"
GEOMETRY_ROOT = FUNCTIONAL_RG / "5355"
GEOMETRY_OVERALL_RESULT = GEOMETRY_ROOT / "D4_higher_rung_event_geometry_result.json"
ANALYTIC_CONTRACT = (
    GEOMETRY_ROOT / "D4_endpoint_coefficient_removable_singularity_contract.csv"
)
BASE = FUNCTIONAL_RG / "5334" / "E0025"
BASE_CANDIDATES = BASE / "D4_outer_support_event_candidates.csv"
TARGETS = {"E010": 0.01, "E020": 0.02}


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise ImportError(path)
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


M5351 = load_module("mts_5356_higher_rung_parent", PARENT_5351)
SUPPORT = M5351.SUPPORT
ALL_EIGHT = M5351.ALL_EIGHT

for target_id, target_epsilon in TARGETS.items():
    SUPPORT.SUPPORTED[target_id] = target_epsilon
    ALL_EIGHT.SUPPORTED[target_id] = target_epsilon


def geometry_dir(epsilon_id: str) -> Path:
    return GEOMETRY_ROOT / epsilon_id


def geometry_events(epsilon_id: str) -> Path:
    return geometry_dir(epsilon_id) / f"D4_{epsilon_id}_5337_refined_events.csv"


def geometry_result(epsilon_id: str) -> Path:
    return geometry_dir(epsilon_id) / f"D4_{epsilon_id}_event_geometry_result.json"


def geometry_validation(epsilon_id: str) -> Path:
    return geometry_dir(epsilon_id) / f"D4_{epsilon_id}_event_geometry_validation.csv"


def support_dir(epsilon_id: str) -> Path:
    return FUNCTIONAL_RG / "5356" / epsilon_id / "support"


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def atomic_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    fields: list[str] = []
    for row in rows:
        fields.extend(field for field in row if field not in fields)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    os.replace(temporary, path)


def atomic_json(path: Path, payload: dict[str, Any]) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def patch_controller(controller: Any) -> None:
    original = controller.configure_D4_target

    def configure_target(epsilon_id: str) -> dict[str, Path]:
        paths = original(epsilon_id)
        if epsilon_id in TARGETS:
            parent = controller.M5326
            parent.EVENTS = geometry_events(epsilon_id)
            parent.EVENT_CANDIDATES = BASE_CANDIDATES
            parent.EXPECTED_EVENT_COUNT = 8
        return paths

    controller.configure_D4_target = configure_target


patch_controller(SUPPORT.M5342.M5334)
patch_controller(ALL_EIGHT.M5346.M5342.M5334)

ORIGINAL_SUPPORT_EXPECTED_PATHS = SUPPORT.expected_paths
ORIGINAL_ALL_EVENT_PATH = ALL_EIGHT.expected_event_path
ORIGINAL_ALL_CANDIDATE_PATH = ALL_EIGHT.expected_candidate_path
ORIGINAL_ALL_SOURCE_PATHS = ALL_EIGHT.source_paths


def expected_support_paths(epsilon_id: str) -> dict[str, Path]:
    if epsilon_id in TARGETS:
        return {
            "events": geometry_events(epsilon_id),
            "candidates": BASE_CANDIDATES,
            "dry_run": geometry_result(epsilon_id),
        }
    return ORIGINAL_SUPPORT_EXPECTED_PATHS(epsilon_id)


def expected_all_event_path(epsilon_id: str) -> Path:
    if epsilon_id in TARGETS:
        return geometry_events(epsilon_id)
    return ORIGINAL_ALL_EVENT_PATH(epsilon_id)


def expected_all_candidate_path(epsilon_id: str) -> Path:
    if epsilon_id in TARGETS:
        return BASE_CANDIDATES
    return ORIGINAL_ALL_CANDIDATE_PATH(epsilon_id)


def all_source_paths(
    epsilon_id: str,
    migration_result: Path,
    migration_validation: Path,
    endpoint_result: Path,
    endpoint_coefficients: Path,
    endpoint_validation: Path,
) -> list[Path]:
    paths = ORIGINAL_ALL_SOURCE_PATHS(
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
            PARENT_5351,
            GEOMETRY_OVERALL_RESULT,
            ANALYTIC_CONTRACT,
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


SUPPORT.expected_paths = expected_support_paths
ALL_EIGHT.expected_event_path = expected_all_event_path
ALL_EIGHT.expected_candidate_path = expected_all_candidate_path
ALL_EIGHT.source_paths = all_source_paths


def augment_output(
    epsilon_id: str,
    result_path: Path,
    validation_path: Path,
    source_register: Path,
) -> dict[str, Any]:
    result = read_json(result_path)
    claims = (
        SUPPORT.no_claims(epsilon_id)
        if result.get("mode") == "D4-dyadic-support-endpoint-normal-form"
        else ALL_EIGHT.no_claims(epsilon_id)
    )
    wrapper = Path(__file__).resolve()
    additions = [wrapper, PARENT_5351, GEOMETRY_OVERALL_RESULT, ANALYTIC_CONTRACT]
    source_rows = list(result.get("source_files", []))
    register_rows = read_csv(source_register)
    existing_result = {Path(str(row["path"])).resolve() for row in source_rows}
    existing_register = {Path(str(row["path"])).resolve() for row in register_rows}
    for path in additions:
        resolved = path.resolve()
        row = {
            "path": str(resolved),
            "sha256": digest(resolved),
            "exists": True,
            **claims,
        }
        if resolved not in existing_result:
            source_rows.append(row)
            existing_result.add(resolved)
        if resolved not in existing_register:
            register_rows.append(row)
            existing_register.add(resolved)
    validation_rows = [
        row
        for row in read_csv(validation_path)
        if row.get("gate") != "higher_rung_wrapper_and_geometry_are_registered"
    ]
    validation_rows.append(
        {
            "gate": "higher_rung_wrapper_and_geometry_are_registered",
            "passed": True,
            "detail": f"{epsilon_id}|{digest(wrapper)}|{digest(GEOMETRY_OVERALL_RESULT)}",
        }
    )
    result["source_files"] = source_rows
    result["higher_rung_wrapper"] = str(wrapper)
    result["higher_rung_wrapper_sha256"] = digest(wrapper)
    result["event_geometry_source"] = str(geometry_events(epsilon_id).resolve())
    result["source_geometry_was_not_rewritten"] = True
    result["validation_passed"] = bool(result.get("validation_passed")) and all(
        str(row["passed"]).strip().lower() == "true" for row in validation_rows
    )
    result["updated_utc"] = utc_now()
    atomic_csv(source_register, register_rows)
    atomic_csv(validation_path, validation_rows)
    atomic_json(result_path, result)
    return result


def support_arguments(epsilon_id: str, output: Path | None, dry_run: bool) -> argparse.Namespace:
    return argparse.Namespace(
        epsilon_id=epsilon_id,
        migration_result=geometry_result(epsilon_id),
        migration_validation=geometry_validation(epsilon_id),
        output_dir=output,
        dry_run=dry_run,
    )


def all_arguments(epsilon_id: str, output: Path | None, dry_run: bool) -> argparse.Namespace:
    endpoint = support_dir(epsilon_id)
    return argparse.Namespace(
        epsilon_id=epsilon_id,
        geometry_result=geometry_result(epsilon_id),
        geometry_validation=geometry_validation(epsilon_id),
        endpoint_result=endpoint / f"D4_{epsilon_id}_support_endpoint_result.json",
        endpoint_coefficients=endpoint / f"D4_{epsilon_id}_support_endpoint_coefficients.csv",
        endpoint_validation=endpoint / f"D4_{epsilon_id}_support_endpoint_validation.csv",
        output_dir=output,
        dry_run=dry_run,
    )


def run_support(epsilon_id: str, output: Path | None, dry_run: bool) -> dict[str, Any]:
    arguments = support_arguments(epsilon_id, output, dry_run)
    if dry_run:
        return SUPPORT.preflight(
            epsilon_id,
            arguments.migration_result,
            arguments.migration_validation,
        )
    if output is None:
        raise ValueError("--output-dir is required")
    result = SUPPORT.run(
        epsilon_id,
        arguments.migration_result,
        arguments.migration_validation,
        output,
    )
    resolved = output.resolve()
    return augment_output(
        epsilon_id,
        resolved / f"D4_{epsilon_id}_support_endpoint_result.json",
        resolved / f"D4_{epsilon_id}_support_endpoint_validation.csv",
        resolved / "source_register.csv",
    )


def run_all_eight(epsilon_id: str, output: Path | None, dry_run: bool) -> dict[str, Any]:
    arguments = all_arguments(epsilon_id, output, dry_run)
    if dry_run:
        return ALL_EIGHT.preflight(
            epsilon_id,
            arguments.geometry_result,
            arguments.geometry_validation,
            arguments.endpoint_result,
            arguments.endpoint_coefficients,
            arguments.endpoint_validation,
        )
    if output is None:
        raise ValueError("--output-dir is required")
    result = ALL_EIGHT.run(
        epsilon_id,
        arguments.geometry_result,
        arguments.geometry_validation,
        arguments.endpoint_result,
        arguments.endpoint_coefficients,
        arguments.endpoint_validation,
        output,
    )
    resolved = output.resolve()
    return augment_output(
        epsilon_id,
        resolved / f"D4_{epsilon_id}_all_eight_endpoint_result.json",
        resolved / f"D4_{epsilon_id}_all_eight_endpoint_validation.csv",
        resolved / "source_register.csv",
    )


def self_test() -> dict[str, Any]:
    checks = {
        "two_higher_rungs_are_exact": TARGETS == {"E010": 0.01, "E020": 0.02},
        "support_paths_are_patched": all(
            SUPPORT.expected_paths(epsilon_id)["events"].resolve()
            == geometry_events(epsilon_id).resolve()
            for epsilon_id in TARGETS
        ),
        "all_eight_paths_are_patched": all(
            ALL_EIGHT.expected_event_path(epsilon_id).resolve()
            == geometry_events(epsilon_id).resolve()
            for epsilon_id in TARGETS
        ),
        "downstream_claims_start_false": all(
            value is False
            for epsilon_id in TARGETS
            for value in ALL_EIGHT.no_claims(epsilon_id).values()
        ),
    }
    return {"mode": "self-test", "checks": checks, "all_pass": all(checks.values())}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--epsilon-id", choices=sorted(TARGETS))
    parser.add_argument("--stage", choices=("support", "all-eight"))
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    arguments = parser.parse_args()
    if arguments.self_test:
        result = self_test()
    else:
        if arguments.epsilon_id is None or arguments.stage is None:
            parser.error("--epsilon-id and --stage are required")
        if arguments.output_dir is None and not arguments.dry_run:
            parser.error("--output-dir is required unless --dry-run is used")
        if arguments.stage == "support":
            result = run_support(
                arguments.epsilon_id, arguments.output_dir, arguments.dry_run
            )
        else:
            result = run_all_eight(
                arguments.epsilon_id, arguments.output_dir, arguments.dry_run
            )
    print(json.dumps(result, indent=2, sort_keys=True))
    passed = result.get("all_pass", result.get("validation_passed", False))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
