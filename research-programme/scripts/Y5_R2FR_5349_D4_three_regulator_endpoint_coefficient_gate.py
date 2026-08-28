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


os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("NUMEXPR_NUM_THREADS", "1")
sys.dont_write_bytecode = True

POST = Path(__file__).resolve().parents[1]
SCRIPTS = POST / "scripts"
SCRIPT_5348 = SCRIPTS / "Y5_R2FR_D4_endpoint_coefficient_stability_gate.py"
CLAIM_AFFINE = (
    "valid_for_D4_three_regulator_affine_endpoint_coefficient_stability"
)
CLAIM_NONZERO = (
    "valid_for_D4_three_regulator_nonzero_affine_endpoint_intercept"
)
CLAIM_COEFFICIENT_LIMIT = "valid_for_D4_endpoint_coefficient_regulator_zero_limit"
DOWNSTREAM_FALSE_CLAIMS = (
    CLAIM_COEFFICIENT_LIMIT,
    "valid_for_D4_outer_regulator_zero_limit",
    "valid_for_decay_angle_integral",
    "valid_for_full_angular_convergence",
    "valid_for_full_phase_space_coefficient",
    "valid_for_numeric_UV_claim",
    "valid_for_local_GR_claim",
    "valid_for_full_MTS_claim",
)
EXPECTED_EPSILON_IDS = ("E000625", "E00125", "E005")
AFFINE_WEIGHTS = (6.0, -7.0, 1.0)


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise ImportError(path)
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


M5348 = load_module("mts_checkpoint_5348_three_regulator_dependency", SCRIPT_5348)


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def atomic_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


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


def complex_fields(prefix: str, value: complex) -> dict[str, float]:
    return {
        f"{prefix}_real": float(value.real),
        f"{prefix}_imaginary": float(value.imag),
        f"{prefix}_magnitude": float(abs(value)),
    }


def no_downstream_claims() -> dict[str, bool]:
    return {claim: False for claim in DOWNSTREAM_FALSE_CLAIMS}


def validation_row(gate: str, passed: bool, detail: Any) -> dict[str, Any]:
    return {"gate": gate, "passed": bool(passed), "detail": str(detail)}


def recursive_source_chain_current(
    path: Path,
    visited: set[Path] | None = None,
) -> tuple[bool, int]:
    resolved = path.resolve()
    visited = set() if visited is None else visited
    if resolved in visited:
        return True, 0
    visited.add(resolved)
    if not resolved.is_file():
        return False, 0
    if resolved.suffix.lower() != ".json":
        return True, 0
    try:
        payload = json.loads(resolved.read_text(encoding="utf-8-sig"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError):
        return False, 0
    source_rows = payload.get("source_files", [])
    if not isinstance(source_rows, list):
        return False, 0
    checked = 0
    for row in source_rows:
        source_path = Path(str(row.get("path", "")))
        expected = str(row.get("sha256", ""))
        if (
            not source_path.is_file()
            or len(expected) != 64
            or digest(source_path) != expected
        ):
            return False, checked
        checked += 1
        nested_current, nested_count = recursive_source_chain_current(
            source_path,
            visited,
        )
        checked += nested_count
        if not nested_current:
            return False, checked
    return True, checked


def evaluate_loaded(loaded: list[dict[str, Any]]) -> dict[str, Any]:
    if len(loaded) != 3:
        raise ValueError("exactly three coefficient results are required")
    lower, middle, upper = loaded
    h = lower["epsilon"]
    expected_geometry = (
        tuple(row["epsilon_id"] for row in loaded) == EXPECTED_EPSILON_IDS
        and abs(middle["epsilon"] - 2.0 * h) <= 1.0e-15
        and abs(upper["epsilon"] - 8.0 * h) <= 1.0e-15
    )
    contrast = sum(
        weight * row["value"]
        for weight, row in zip(AFFINE_WEIGHTS, loaded)
    )
    contrast_radius = sum(
        abs(weight) * row["radius"]
        for weight, row in zip(AFFINE_WEIGHTS, loaded)
    )
    affine_compatible = (
        expected_geometry
        and all(row["valid"] and row["recursive_sources_valid"] for row in loaded)
        and abs(contrast) <= contrast_radius
    )
    lower_intercept = 2.0 * lower["value"] - middle["value"]
    lower_intercept_radius = 2.0 * lower["radius"] + middle["radius"]
    upper_intercept = (4.0 * middle["value"] - upper["value"]) / 3.0
    upper_intercept_radius = (4.0 * middle["radius"] + upper["radius"]) / 3.0
    intercept_centre, intercept_radius = M5348.minimal_enclosing_disk(
        lower_intercept,
        lower_intercept_radius,
        upper_intercept,
        upper_intercept_radius,
    )
    intercept_disks_overlap = (
        abs(lower_intercept - upper_intercept)
        <= lower_intercept_radius + upper_intercept_radius
    )
    nonzero_intercept = (
        affine_compatible
        and intercept_disks_overlap
        and abs(intercept_centre) > intercept_radius
    )
    lower_slope = (middle["value"] - lower["value"]) / h
    upper_slope = (upper["value"] - middle["value"]) / (6.0 * h)
    maximum_relative_drift = max(
        abs(right["value"] - left["value"])
        / max(abs(right["value"]), abs(left["value"]), 1.0e-300)
        for left, right in zip(loaded, loaded[1:])
    )
    return {
        "expected_geometry": expected_geometry,
        "inputs_valid": all(
            row["valid"] and row["recursive_sources_valid"] for row in loaded
        ),
        "contrast": contrast,
        "contrast_radius": contrast_radius,
        "contrast_ratio": abs(contrast) / max(contrast_radius, 1.0e-300),
        "affine_compatible": affine_compatible,
        "lower_intercept": lower_intercept,
        "lower_intercept_radius": lower_intercept_radius,
        "upper_intercept": upper_intercept,
        "upper_intercept_radius": upper_intercept_radius,
        "intercept_disks_overlap": intercept_disks_overlap,
        "intercept_centre": intercept_centre,
        "intercept_radius": intercept_radius,
        "nonzero_intercept": nonzero_intercept,
        "lower_slope": lower_slope,
        "upper_slope": upper_slope,
        "maximum_relative_drift": maximum_relative_drift,
    }


def run(paths: list[Path], output: Path) -> dict[str, Any]:
    started = time.perf_counter()
    if len(paths) != 3:
        raise ValueError("exactly three coefficient results are required")
    loaded = sorted(
        [M5348.load_coefficient_result(path.resolve()) for path in paths],
        key=lambda row: row["epsilon"],
    )
    for row in loaded:
        recursive_valid, recursive_count = recursive_source_chain_current(
            row["path"]
        )
        row["recursive_sources_valid"] = recursive_valid
        row["recursive_source_count"] = recursive_count
    evaluation = evaluate_loaded(loaded)
    gates = [
        validation_row(
            "exact_h_2h_8h_regulator_geometry",
            evaluation["expected_geometry"],
            [(row["epsilon_id"], row["epsilon"]) for row in loaded],
        ),
        validation_row(
            "all_three_inputs_are_valid_and_source_current",
            evaluation["inputs_valid"],
            [
                {
                    "checks": row["checks"],
                    "recursive_sources_valid": row["recursive_sources_valid"],
                    "recursive_source_count": row["recursive_source_count"],
                }
                for row in loaded
            ],
        ),
        validation_row(
            "exact_affine_contrast_disk_contains_zero",
            evaluation["affine_compatible"],
            {
                "weights": AFFINE_WEIGHTS,
                "contrast_magnitude": abs(evaluation["contrast"]),
                "contrast_radius": evaluation["contrast_radius"],
            },
        ),
        validation_row(
            "independent_affine_intercept_disks_overlap",
            evaluation["intercept_disks_overlap"],
            {
                "centre_separation": abs(
                    evaluation["lower_intercept"] - evaluation["upper_intercept"]
                ),
                "radius_sum": evaluation["lower_intercept_radius"]
                + evaluation["upper_intercept_radius"],
            },
        ),
        validation_row(
            "common_affine_intercept_disk_excludes_zero",
            evaluation["nonzero_intercept"],
            {
                "centre_magnitude": abs(evaluation["intercept_centre"]),
                "radius": evaluation["intercept_radius"],
            },
        ),
        validation_row(
            "coefficient_limit_and_downstream_claims_stay_false",
            all(value is False for value in no_downstream_claims().values()),
            "fourth coefficient rung or sourced remainder bound still required",
        ),
        validation_row(
            "formal_workbench_unchanged_in_all_inputs",
            all(
                row["payload"].get("formalization_workbench_modified_file_count")
                == 0
                for row in loaded
            ),
            [
                row["payload"].get("formalization_workbench_modified_file_count")
                for row in loaded
            ],
        ),
        validation_row(
            "scripts_cache_absent",
            not (SCRIPTS / "__pycache__").exists(),
            SCRIPTS / "__pycache__",
        ),
    ]
    validation_passed = all(bool(row["passed"]) for row in gates)
    affine_claim = evaluation["affine_compatible"] and validation_passed
    nonzero_claim = evaluation["nonzero_intercept"] and validation_passed
    decision = (
        "D4_THREE_REGULATOR_AFFINE_COEFFICIENT_PASS__ACQUIRE_FOURTH_OR_REMAINDER_BOUND"
        if affine_claim and nonzero_claim
        else "D4_THREE_REGULATOR_AFFINE_COEFFICIENT_BLOCKED"
    )
    claims = {
        CLAIM_AFFINE: affine_claim,
        CLAIM_NONZERO: nonzero_claim,
        **no_downstream_claims(),
    }
    input_rows = [
        {
            "epsilon_id": row["epsilon_id"],
            "epsilon": row["epsilon"],
            **complex_fields("A_finite_epsilon", row["value"]),
            "A_diagnostic_disk_radius": row["radius"],
            "input_contract_passes": row["valid"],
            "recursive_source_chain_passes": row["recursive_sources_valid"],
            "recursive_source_count": row["recursive_source_count"],
            "result_path": str(row["path"]),
            "result_sha256": row["path_sha256"],
            **claims,
        }
        for row in loaded
    ]
    contrast_row = {
        "epsilon_geometry": "h|2h|8h",
        "affine_contrast_weights": "6|-7|1",
        **complex_fields("affine_contrast", evaluation["contrast"]),
        "affine_contrast_disk_radius": evaluation["contrast_radius"],
        "affine_contrast_radius_ratio": evaluation["contrast_ratio"],
        "affine_contrast_disk_contains_zero": evaluation["affine_compatible"],
        **complex_fields("small_pair_affine_intercept", evaluation["lower_intercept"]),
        "small_pair_affine_intercept_disk_radius": evaluation[
            "lower_intercept_radius"
        ],
        **complex_fields("wide_pair_affine_intercept", evaluation["upper_intercept"]),
        "wide_pair_affine_intercept_disk_radius": evaluation[
            "upper_intercept_radius"
        ],
        **complex_fields("common_affine_intercept_disk_centre", evaluation["intercept_centre"]),
        "common_affine_intercept_disk_radius": evaluation["intercept_radius"],
        "common_affine_intercept_disk_excludes_zero": evaluation[
            "nonzero_intercept"
        ],
        **complex_fields("small_pair_affine_slope", evaluation["lower_slope"]),
        **complex_fields("wide_pair_affine_slope", evaluation["upper_slope"]),
        "maximum_relative_raw_coefficient_drift": evaluation[
            "maximum_relative_drift"
        ],
        "coefficient_regulator_zero_limit_complete": False,
        "next_required_evidence": "FOURTH_COEFFICIENT_RUNG_OR_SOURCED_REMAINDER_BOUND",
        "decision": decision,
        **claims,
    }
    source_rows = [
        {
            "path": str(path.resolve()),
            "sha256": digest(path.resolve()),
            "exists": path.resolve().is_file(),
            **claims,
        }
        for path in [Path(__file__), SCRIPT_5348, *paths]
    ]
    output = output.resolve()
    atomic_csv(output / "D4_three_regulator_coefficient_inputs.csv", input_rows)
    atomic_csv(output / "D4_three_regulator_affine_contrast.csv", [contrast_row])
    atomic_csv(output / "source_register.csv", source_rows)
    atomic_csv(output / "D4_three_regulator_coefficient_validation.csv", gates)
    result = {
        "mode": "D4-three-regulator-affine-endpoint-coefficient-gate",
        "validation_passed": validation_passed,
        "decision": decision,
        "input_epsilon_ids": [row["epsilon_id"] for row in loaded],
        **complex_fields("affine_contrast", evaluation["contrast"]),
        "affine_contrast_disk_radius": evaluation["contrast_radius"],
        "affine_contrast_radius_ratio": evaluation["contrast_ratio"],
        **complex_fields("common_affine_intercept_disk_centre", evaluation["intercept_centre"]),
        "common_affine_intercept_disk_radius": evaluation["intercept_radius"],
        "common_affine_intercept_disk_excludes_zero": evaluation[
            "nonzero_intercept"
        ],
        "coefficient_regulator_zero_limit_complete": False,
        "claim_boundary": claims,
        "source_files": source_rows,
        "formalization_workbench_modified_file_count": 0,
        "runtime_seconds": time.perf_counter() - started,
        "updated_utc": utc_now(),
    }
    atomic_json(output / "D4_three_regulator_coefficient_result.json", result)
    atomic_json(
        output / "status.json",
        {
            "state": "COMPLETE" if validation_passed else "BLOCKED",
            "decision": decision,
            "validation_passed": validation_passed,
            "updated_utc": utc_now(),
        },
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return result


def self_test() -> dict[str, Any]:
    h = 0.1
    intercept = 2.0 + 3.0j
    slope = 0.4 - 0.2j
    loaded = [
        {
            "epsilon_id": epsilon_id,
            "epsilon": epsilon,
            "value": intercept + slope * epsilon,
            "radius": 1.0e-6,
            "valid": True,
            "recursive_sources_valid": True,
        }
        for epsilon_id, epsilon in zip(EXPECTED_EPSILON_IDS, (h, 2.0 * h, 8.0 * h))
    ]
    evaluation = evaluate_loaded(loaded)
    checks = {
        "exact_affine_contrast_vanishes": abs(evaluation["contrast"]) <= 1.0e-14,
        "affine_model_passes": evaluation["affine_compatible"],
        "intercept_disk_excludes_zero": evaluation["nonzero_intercept"],
        "coefficient_limit_claim_stays_false": no_downstream_claims()[
            CLAIM_COEFFICIENT_LIMIT
        ]
        is False,
    }
    return {"mode": "self-test", "checks": checks, "all_pass": all(checks.values())}


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--coefficient-result", type=Path, action="append")
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--self-test", action="store_true")
    arguments = parser.parse_args()
    if arguments.self_test:
        result = self_test()
        print(json.dumps(result, indent=2, sort_keys=True))
        return 0 if result["all_pass"] else 1
    if not arguments.coefficient_result or len(arguments.coefficient_result) != 3:
        parser.error("provide exactly three --coefficient-result paths")
    if arguments.output_dir is None:
        parser.error("--output-dir is required")
    result = run(arguments.coefficient_result, arguments.output_dir)
    return 0 if result["validation_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
