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


CHECKPOINT = 5340
MARKER = "MTS_5340_D4_E0025_LOG_CORRECTED_CANONICALIZER"
POST = Path(__file__).resolve().parents[1]
ROOT = POST.parent
SCRIPTS = POST / "scripts"
OUT = POST / "source-intake" / "functional_rg" / str(CHECKPOINT)
RESIDUALS = POST / "source-intake" / "mts_residuals"
VALIDATION = RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv"
SCRIPT_5339 = SCRIPTS / "Y5_R2FR_5339_D4_E08_support_exit_log_subtraction.py"
RESULT = OUT / "D4_E0025_log_corrected_canonical_result.json"
FINITE_VALUE = OUT / "D4_E0025_log_corrected_finite_value.csv"
PANELS = OUT / "D4_E0025_log_corrected_adaptive_panels.csv"
LEAF_AUDIT = OUT / "D4_E0025_log_corrected_leaf_audit.csv"
AGGREGATION = OUT / "D4_E0025_log_corrected_aggregation.csv"
SOURCE_REGISTER = OUT / "source_register.csv"
STATUS = OUT / "status.json"
TARGET_PANEL = "P12S02LLLL"
LOCAL_OUTER_CHANGE_LIMIT = 5.0e-3
GLOBAL_ERROR_BUDGET_LIMIT = 1.0e-2
FORMAL_DIGEST = "0ec1bc6012136ffc6b28a1512aca6ce712b6decd2ff793310a9bd61775f3db1f"
CLAIM_FIELDS = (
    "valid_for_D4_outer_E0025_fixed_decay_integral",
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


M5339 = load_module("mts_5339_for_5340", SCRIPT_5339)
M5334 = M5339.M5334
M5326 = M5339.M5326
M5312 = M5339.M5312
M5283 = M5339.M5283


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


def complex_fields(prefix: str, value: complex) -> dict[str, float]:
    return {
        f"{prefix}_real": float(value.real),
        f"{prefix}_imaginary": float(value.imag),
        f"{prefix}_magnitude": float(abs(value)),
    }


def complex_from(row: dict[str, Any], prefix: str) -> complex:
    return complex(float(row[f"{prefix}_real"]), float(row[f"{prefix}_imaginary"]))


def relative_complex_change(first: complex, second: complex) -> float:
    return abs(second - first) / max(abs(first), abs(second), 1.0e-300)


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
    M5334.configure_refinement("E0025")
    M5326.MAXIMUM_ADAPTIVE_DEPTH = 4


def source_paths() -> list[Path]:
    return [
        Path(__file__).resolve(),
        SCRIPT_5339,
        POST / "5340-Y5-R2FR-D4-E0025-log-corrected-canonical-finite-rung.md",
        POST / "5339-Y5-R2FR-D4-E08-support-exit-log-subtraction.md",
        POST / "source-intake/functional_rg/5339/D4_E08_support_exit_log_subtraction_result.json",
        POST / "source-intake/functional_rg/5339/E08_log_subtracted_quadrature.csv",
        POST / "source-intake/mts_residuals/P8_Y5_BRR545_5339_VALIDATION.csv",
        M5326.RESULT,
        M5326.FINITE_VALUE,
        M5326.ADAPTIVE_PANELS,
        M5326.NODE_MANIFEST,
        M5326.EVENTS,
        M5326.VALIDATION,
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


def quadrature_values() -> dict[int, complex]:
    rows = read_csv(M5339.QUADRATURE)
    values = {
        int(row["outer_order"]): complex_from(
            row, "reconstructed_panel_integral"
        )
        for row in rows
    }
    if set(values) != {4, 8}:
        raise RuntimeError(f"unexpected corrected quadrature orders: {sorted(values)}")
    return values


def corrected_panel_rows(
    corrected: dict[int, complex],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    rows = [dict(row) for row in read_csv(M5326.ADAPTIVE_PANELS)]
    targets = [row for row in rows if row["adaptive_panel_id"] == TARGET_PANEL]
    if len(targets) != 1:
        raise RuntimeError(f"expected one {TARGET_PANEL}, found {len(targets)}")
    target = targets[0]
    raw_target = dict(target)
    absolute_change = abs(corrected[8] - corrected[4])
    relative_change = relative_complex_change(corrected[4], corrected[8])
    for order in (4, 8):
        target.update(complex_fields(f"outer_Q{order}_inner_Q8", corrected[order]))
    target["outer_Q4_Q8_absolute_change"] = absolute_change
    target["outer_Q4_Q8_relative_change"] = relative_change
    target["adaptive_gate_passes"] = (
        parse_bool(target["all_inner_nodes_pass"])
        and parse_bool(target["exact_change_of_variables_gate_passes"])
        and relative_change <= LOCAL_OUTER_CHANGE_LIMIT
    )
    target["failure_reason"] = "" if target["adaptive_gate_passes"] else "LOG_CORRECTED_GATE_FAILURE"
    target["endpoint_correction_method"] = "E08_PARENT_AFFINE_COMPLEX_LOG_SUBTRACTION"
    target["endpoint_correction_checkpoint"] = CHECKPOINT
    target["raw_outer_Q4_Q8_relative_change"] = raw_target[
        "outer_Q4_Q8_relative_change"
    ]
    target["valid_for_D4_outer_E0025_fixed_decay_integral"] = False
    write_csv(PANELS, rows)
    leaves = [row for row in rows if parse_bool(row["adaptive_leaf"])]
    leaf_audit = []
    for row in leaves:
        leaf_audit.append(
            {
                "adaptive_panel_id": row["adaptive_panel_id"],
                "adaptive_depth": row["adaptive_depth"],
                "event_type": row["event_type"],
                "outer_Q4_Q8_absolute_change": row["outer_Q4_Q8_absolute_change"],
                "outer_Q4_Q8_relative_change": row["outer_Q4_Q8_relative_change"],
                "all_inner_nodes_pass": row["all_inner_nodes_pass"],
                "exact_change_of_variables_gate_passes": row[
                    "exact_change_of_variables_gate_passes"
                ],
                "adaptive_gate_passes": row["adaptive_gate_passes"],
                "endpoint_correction_method": row.get(
                    "endpoint_correction_method", "NONE"
                ),
                **no_claims(),
            }
        )
    write_csv(LEAF_AUDIT, leaf_audit)
    return rows, leaves, raw_target


def aggregate(
    leaves: list[dict[str, Any]],
    coordinate_error: float,
) -> dict[str, Any]:
    high = sum(
        (
            complex(
                float(row["outer_Q8_inner_Q8_real"]),
                float(row["outer_Q8_inner_Q8_imaginary"]),
            )
            for row in leaves
        ),
        0.0j,
    )
    outer_error = sum(
        float(row["outer_Q4_Q8_absolute_change"]) for row in leaves
    )
    inner_error = sum(
        float(row["selected_inner_error_budget_absolute"]) for row in leaves
    )
    total_error = outer_error + inner_error + coordinate_error
    relative_error = total_error / max(abs(high), 1.0e-300)
    all_leaf_gates = all(parse_bool(row["adaptive_gate_passes"]) for row in leaves)
    accepted = (
        len(leaves) == 32
        and all_leaf_gates
        and relative_error <= GLOBAL_ERROR_BUDGET_LIMIT
    )
    return {
        "high": high,
        "outer_error": outer_error,
        "inner_error": inner_error,
        "coordinate_error": coordinate_error,
        "total_error": total_error,
        "relative_error": relative_error,
        "all_leaf_gates": all_leaf_gates,
        "accepted": accepted,
    }


def aggregation_rows(
    raw_parent: dict[str, Any],
    raw_target: dict[str, Any],
    corrected: dict[int, complex],
    aggregate_value: dict[str, Any],
) -> list[dict[str, Any]]:
    raw_high = complex(
        float(raw_parent["fixed_decay_integral_real"]),
        float(raw_parent["fixed_decay_integral_imaginary"]),
    )
    raw_target_q8 = complex(
        float(raw_target["outer_Q8_inner_Q8_real"]),
        float(raw_target["outer_Q8_inner_Q8_imaginary"]),
    )
    predicted = raw_high + corrected[8] - raw_target_q8
    return [
        {
            "row_type": "RAW_PARENT",
            **complex_fields("fixed_decay_integral", raw_high),
            "outer_error_absolute_conservative": raw_parent[
                "outer_error_absolute_conservative"
            ],
            "inner_error_absolute_conservative": raw_parent[
                "inner_error_absolute_conservative"
            ],
            "event_coordinate_error_absolute_conservative": 0.0,
            "total_error_absolute_conservative": raw_parent[
                "total_error_absolute_conservative"
            ],
            "total_error_relative_conservative": raw_parent[
                "total_error_relative_conservative"
            ],
            **no_claims(),
        },
        {
            "row_type": "TARGET_REPLACEMENT_IDENTITY",
            **complex_fields("raw_target_Q8", raw_target_q8),
            **complex_fields("corrected_target_Q8", corrected[8]),
            **complex_fields("predicted_corrected_integral", predicted),
            **no_claims(),
        },
        {
            "row_type": "LOG_CORRECTED_CANONICAL",
            **complex_fields("fixed_decay_integral", aggregate_value["high"]),
            "outer_error_absolute_conservative": aggregate_value["outer_error"],
            "inner_error_absolute_conservative": aggregate_value["inner_error"],
            "event_coordinate_error_absolute_conservative": aggregate_value[
                "coordinate_error"
            ],
            "total_error_absolute_conservative": aggregate_value["total_error"],
            "total_error_relative_conservative": aggregate_value["relative_error"],
            **no_claims(),
        },
    ]


def execute() -> dict[str, Any]:
    started = time.perf_counter()
    M5312.set_below_normal_priority()
    configure()
    OUT.mkdir(parents=True, exist_ok=True)
    sources = write_source_register()
    parent = read_json(M5326.RESULT)
    parent_finite = read_csv(M5326.FINITE_VALUE)
    manifest = read_csv(M5326.NODE_MANIFEST)
    method = read_json(M5339.RESULT)
    method_validation = read_csv(M5339.VALIDATION)
    corrected = quadrature_values()
    panel_rows, leaves, raw_target = corrected_panel_rows(corrected)
    coordinate_error = float(
        method["endpoint_coordinate_error_absolute_conservative"]
    )
    aggregate_value = aggregate(leaves, coordinate_error)
    aggregation = aggregation_rows(parent, raw_target, corrected, aggregate_value)
    write_csv(AGGREGATION, aggregation)
    predicted = complex_from(aggregation[1], "predicted_corrected_integral")
    method_predicted = complex_from(method, "corrected_fixed_decay_integral")
    parent_high = complex(
        float(parent["fixed_decay_integral_real"]),
        float(parent["fixed_decay_integral_imaginary"]),
    )
    raw_leaf_sum = sum(
        (
            complex(
                float(row["outer_Q8_inner_Q8_real"]),
                float(row["outer_Q8_inner_Q8_imaginary"]),
            )
            for row in read_csv(M5326.ADAPTIVE_PANELS)
            if parse_bool(row["adaptive_leaf"])
        ),
        0.0j,
    )
    corrected_claims = no_claims()
    corrected_claims["valid_for_D4_outer_E0025_fixed_decay_integral"] = bool(
        aggregate_value["accepted"]
    )
    finite = {
        "decay_node_id": "D4_OUTER",
        "epsilon_id": "E0025",
        "epsilon": 0.0025,
        "method": "EIGHT_SUPPORT_EVENTS_SQUARED_Q4_Q8_ADAPTIVE_WITH_E08_AFFINE_LOG_SUBTRACTION",
        **complex_fields("fixed_decay_integral", aggregate_value["high"]),
        "outer_error_absolute_conservative": aggregate_value["outer_error"],
        "inner_error_absolute_conservative": aggregate_value["inner_error"],
        "event_coordinate_error_absolute_conservative": aggregate_value[
            "coordinate_error"
        ],
        "total_error_absolute_conservative": aggregate_value["total_error"],
        "total_error_relative_conservative": aggregate_value["relative_error"],
        "finite_regulator_fixed_decay_integral_accepted": aggregate_value[
            "accepted"
        ],
        **corrected_claims,
    }
    write_csv(FINITE_VALUE, [finite])
    broader_false = all(
        not value
        for field, value in corrected_claims.items()
        if field != "valid_for_D4_outer_E0025_fixed_decay_integral"
    )
    gates = [
        validation_row(
            "all_source_paths_exist_and_are_hashed",
            len(sources) == 13
            and all(parse_bool(row["exists"]) for row in sources)
            and all(row["sha256"] != "MISSING" for row in sources),
            f"rows={len(sources)}",
        ),
        validation_row(
            "checkpoint_5339_method_and_all_gates_pass",
            method.get("validation_passed") is True
            and bool(method_validation)
            and all(parse_bool(row["passed"]) for row in method_validation)
            and method["claim_boundary"]["valid_for_E08_log_subtraction"] is True,
            str(method.get("decision")),
        ),
        validation_row(
            "raw_parent_aggregation_is_reproduced",
            relative_complex_change(parent_high, raw_leaf_sum) <= 5.0e-15,
            str(relative_complex_change(parent_high, raw_leaf_sum)),
        ),
        validation_row(
            "all_456_parent_nodes_complete_and_pass",
            len(manifest) == 456
            and all(row["shard_state"] == "COMPLETE_PASS" for row in manifest)
            and int(parent["failed_inner_node_count"]) == 0,
            f"nodes={len(manifest)}",
        ),
        validation_row(
            "exactly_one_leaf_receives_source_owned_correction",
            len(panel_rows) == 38
            and len(leaves) == 32
            and sum(
                row.get("endpoint_correction_method", "")
                == "E08_PARENT_AFFINE_COMPLEX_LOG_SUBTRACTION"
                for row in leaves
            )
            == 1,
            f"panels={len(panel_rows)};leaves={len(leaves)}",
        ),
        validation_row(
            "corrected_target_leaf_passes_unchanged_local_gate",
            relative_complex_change(corrected[4], corrected[8])
            <= LOCAL_OUTER_CHANGE_LIMIT
            and next(
                parse_bool(row["adaptive_gate_passes"])
                for row in leaves
                if row["adaptive_panel_id"] == TARGET_PANEL
            ),
            str(relative_complex_change(corrected[4], corrected[8])),
        ),
        validation_row(
            "all_32_log_corrected_adaptive_leaves_pass",
            bool(aggregate_value["all_leaf_gates"])
            and all(parse_bool(row["all_inner_nodes_pass"]) for row in leaves)
            and all(
                parse_bool(row["exact_change_of_variables_gate_passes"])
                for row in leaves
            ),
            f"leaves={len(leaves)}",
        ),
        validation_row(
            "complete_corrected_integral_matches_replacement_identity",
            relative_complex_change(aggregate_value["high"], predicted) <= 5.0e-15
            and relative_complex_change(aggregate_value["high"], method_predicted)
            <= 5.0e-15,
            (
                f"replacement={relative_complex_change(aggregate_value['high'], predicted)};"
                f"method={relative_complex_change(aggregate_value['high'], method_predicted)}"
            ),
        ),
        validation_row(
            "complete_corrected_global_budget_passes",
            float(aggregate_value["relative_error"])
            <= GLOBAL_ERROR_BUDGET_LIMIT,
            str(aggregate_value["relative_error"]),
        ),
        validation_row(
            "narrow_E0025_finite_rung_is_accepted",
            bool(aggregate_value["accepted"])
            and finite["finite_regulator_fixed_decay_integral_accepted"] is True
            and corrected_claims[
                "valid_for_D4_outer_E0025_fixed_decay_integral"
            ]
            is True,
            str(aggregate_value["accepted"]),
        ),
        validation_row(
            "all_regulator_zero_and_broader_claims_remain_false",
            broader_false,
            "regulator-zero, angular, phase-space, UV, local-GR and full-MTS remain false",
        ),
        validation_row(
            "raw_parent_and_historical_finite_artifacts_remain_nonclaim",
            parent.get("acceptance_passed") is False
            and len(parent_finite) == 1
            and not parse_bool(
                parent_finite[0]["finite_regulator_fixed_decay_integral_accepted"]
            ),
            str(parent.get("decision")),
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
    result_claims = no_claims()
    result_claims["valid_for_D4_outer_E0025_fixed_decay_integral"] = passed
    value = {
        "checkpoint": CHECKPOINT,
        "marker": MARKER,
        "mode": "D4-E0025-log-corrected-canonical-aggregation",
        "validation_passed": passed,
        "acceptance_passed": passed,
        "decision": (
            "D4_OUTER_E0025_LOG_CORRECTED_FINITE_RUNG_ACCEPTED__RUN_ADJACENT_REGULATORS"
            if passed
            else "D4_OUTER_E0025_LOG_CORRECTED_CANONICALIZATION_BLOCKED"
        ),
        "completed_full_run": True,
        "encountered_node_count": len(manifest),
        "completed_node_count": len(manifest),
        "failed_inner_node_count": 0,
        "adaptive_panel_count": len(panel_rows),
        "adaptive_leaf_count": len(leaves),
        "all_adaptive_leaf_gates_pass": aggregate_value["all_leaf_gates"],
        "endpoint_correction_panel_id": TARGET_PANEL,
        "endpoint_correction_method": "E08_PARENT_AFFINE_COMPLEX_LOG_SUBTRACTION",
        **complex_fields("fixed_decay_integral", aggregate_value["high"]),
        "outer_error_absolute_conservative": aggregate_value["outer_error"],
        "inner_error_absolute_conservative": aggregate_value["inner_error"],
        "event_coordinate_error_absolute_conservative": aggregate_value[
            "coordinate_error"
        ],
        "total_error_absolute_conservative": aggregate_value["total_error"],
        "total_error_relative_conservative": aggregate_value["relative_error"],
        "claim_boundary": {
            **result_claims,
            "reason": (
                "This is one accepted D4_OUTER finite-regulator fixed-decay value. "
                "The D4 regulator-zero and decay-angle limits remain separate."
            ),
        },
        "source_files": sources,
        "formalization_workbench_modified_file_count": 0,
        "next_action": (
            "RUN_E00125_WITH_GENERIC_E08_LOG_SUBTRACTION"
            if passed
            else "AUDIT_LOG_CORRECTED_AGGREGATION_FAILURE"
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
