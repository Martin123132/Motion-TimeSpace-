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


CHECKPOINT = 5343
MARKER = "MTS_5343_D4_E00125_LOG_CORRECTED_RESUMABLE_RUNNER"
EPSILON_ID = "E00125"
EPSILON = 0.00125
MAXIMUM_ADAPTIVE_DEPTH = 4
ENDPOINT_CORRECTION_MINIMUM_DEPTH = 4
DEFAULT_RUNTIME_HOURS = 4.0
POST = Path(__file__).resolve().parents[1]
SCRIPTS = POST / "scripts"
OUT = POST / "source-intake" / "functional_rg" / str(CHECKPOINT)
RESIDUALS = POST / "source-intake" / "mts_residuals"
VALIDATION = RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv"
SCRIPT_5342 = SCRIPTS / "Y5_R2FR_5342_D4_E00125_generic_support_endpoint_normal_form.py"
RESULT_5342 = (
    POST
    / "source-intake/functional_rg/5342/D4_E00125_support_endpoint_normal_form_result.json"
)
COEFFICIENTS_5342 = (
    POST
    / "source-intake/functional_rg/5342/D4_E00125_support_endpoint_coefficients.csv"
)
VALIDATION_5342 = RESIDUALS / "P8_Y5_BRR545_5342_VALIDATION.csv"
RESULT_5341 = (
    POST
    / "source-intake/functional_rg/5341/D4_E00125_event_evidence_migration_result.json"
)
PREFLIGHT = OUT / "D4_E00125_endpoint_correction_preflight.csv"
CORRECTION_AUDIT = OUT / "D4_E00125_endpoint_correction_runtime_audit.csv"
SOURCE_REGISTER = OUT / "source_register.csv"
RESULT = OUT / "D4_E00125_log_corrected_resumable_runner_result.json"
STATUS = OUT / "status.json"
FORMAL_DIGEST = "0ec1bc6012136ffc6b28a1512aca6ce712b6decd2ff793310a9bd61775f3db1f"
SUPPORT_EVENT_TYPES = {"SUPPORT_ENTRY", "SUPPORT_EXIT"}
CLAIM_FIELDS = (
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


M5342 = load_module("mts_5342_for_5343", SCRIPT_5342)
M5334 = M5342.M5334
M5326 = M5342.M5326
M5312 = M5342.M5312
M5283 = M5342.M5283


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
    M5326.MAXIMUM_ADAPTIVE_DEPTH = MAXIMUM_ADAPTIVE_DEPTH


def coefficient_rows() -> list[dict[str, str]]:
    rows = read_csv(COEFFICIENTS_5342)
    if [row["event_id"] for row in rows] != ["E01", "E02", "E03", "E08"]:
        raise RuntimeError("unexpected E00125 support-endpoint coefficient inventory")
    if not all(
        parse_bool(row["coefficient_contract_passes"])
        and parse_bool(row["valid_for_D4_E00125_support_endpoint_coefficients"])
        for row in rows
    ):
        raise RuntimeError("checkpoint-5342 endpoint coefficient contract is not valid")
    return rows


def source_paths() -> list[Path]:
    return [
        Path(__file__).resolve(),
        SCRIPT_5342,
        RESULT_5342,
        COEFFICIENTS_5342,
        VALIDATION_5342,
        RESULT_5341,
        M5326.DRY_RUN,
        M5326.EVENTS,
        M5326.INITIAL_PLAN,
        M5326.CONTRACT_5325,
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


def principal_log_cut_crossed(
    lower_delta: float,
    upper_delta: float,
    z0: complex,
    z1: complex,
) -> bool:
    endpoints = (z0 + z1 * lower_delta, z0 + z1 * upper_delta)
    if min(abs(value) for value in endpoints) <= 1.0e-14 * max(abs(z0), 1.0):
        return True
    imaginary_scale = max(abs(value.imag) for value in endpoints) + abs(z0.imag)
    tolerance = max(1.0e-16, 1.0e-13 * imaginary_scale)
    if abs(z1.imag) <= tolerance:
        return abs(z0.imag) <= tolerance and min(value.real for value in endpoints) <= 0.0
    crossing_delta = -z0.imag / z1.imag
    if lower_delta <= crossing_delta <= upper_delta:
        crossing = z0 + z1 * crossing_delta
        return crossing.real <= 0.0
    return False


def coefficient_for_coordinate(
    coordinate: float,
    coefficients: list[dict[str, str]],
) -> dict[str, str]:
    matches = sorted(
        coefficients,
        key=lambda row: abs(float(row["event_coordinate"]) - coordinate),
    )
    if not matches:
        raise RuntimeError("support panel has no endpoint coefficient")
    selected = matches[0]
    tolerance = 2.0 * float(selected["event_coordinate_error_estimate"])
    if abs(float(selected["event_coordinate"]) - coordinate) > tolerance:
        raise RuntimeError(
            f"support panel coordinate {coordinate} does not identify a 5342 event"
        )
    return selected


def depth_four_endpoint_interval(row: dict[str, str]) -> tuple[float, float]:
    lower = float(row["lower_absolute_soft_cosine"])
    upper = float(row["upper_absolute_soft_cosine"])
    event = float(row["event_coordinate"])
    width = (upper - lower) / (2**MAXIMUM_ADAPTIVE_DEPTH)
    if abs(event - lower) <= abs(event - upper):
        return lower, lower + width
    return upper - width, upper


def correction_preflight(
    coefficients: list[dict[str, str]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for segment in read_csv(M5326.INITIAL_PLAN):
        if segment["event_type"] not in SUPPORT_EVENT_TYPES:
            continue
        coordinate = float(segment["event_coordinate"])
        coefficient = coefficient_for_coordinate(coordinate, coefficients)
        lower, upper = depth_four_endpoint_interval(segment)
        x0 = float(coefficient["event_coordinate"])
        lower_delta = lower - x0
        upper_delta = upper - x0
        z0 = complex_from(coefficient, "boundary_gap_z0")
        z1 = complex_from(coefficient, "boundary_gap_derivative_z1")
        cut_crossed = principal_log_cut_crossed(lower_delta, upper_delta, z0, z1)
        exact_model = M5342.affine_log_primitive(
            upper_delta,
            int(coefficient["log_sign"]),
            complex_from(coefficient, "physical_coefficient_C0"),
            complex_from(coefficient, "physical_coefficient_derivative_C1"),
            z0,
            z1,
        ) - M5342.affine_log_primitive(
            lower_delta,
            int(coefficient["log_sign"]),
            complex_from(coefficient, "physical_coefficient_C0"),
            complex_from(coefficient, "physical_coefficient_derivative_C1"),
            z0,
            z1,
        )
        rows.append(
            {
                "event_id": coefficient["event_id"],
                "initial_segment_id": segment["initial_segment_id"],
                "event_type": segment["event_type"],
                "depth_four_lower": lower,
                "depth_four_upper": upper,
                "lower_delta": lower_delta,
                "upper_delta": upper_delta,
                "principal_log_cut_crossed": cut_crossed,
                **complex_fields("exact_affine_log_model_integral", exact_model),
                "preflight_passes": not cut_crossed and math.isfinite(abs(exact_model)),
                **no_claims(),
            }
        )
    write_csv(PREFLIGHT, rows)
    return rows


def validated_cached_dry_run_only() -> dict[str, Any]:
    required = (
        M5326.DRY_RUN,
        M5326.EVENTS,
        M5326.INITIAL_PLAN,
        M5326.VALIDATION_5325,
    )
    if not all(path.is_file() for path in required):
        missing = [str(path) for path in required if not path.is_file()]
        raise RuntimeError(f"missing cached dry-run inputs: {missing}")
    dry = read_json(M5326.DRY_RUN)
    events = read_csv(M5326.EVENTS)
    initial = read_csv(M5326.INITIAL_PLAN)
    M5326.EXPECTED_EVENT_COUNT = len(events)
    checks = {
        "accepted": dry.get("acceptance_passed") is True,
        "decision": dry.get("decision")
        == "DRY_RUN_ACCEPTED__RUN_D4_OUTER_EVENT_ALIGNED_REFINEMENT",
        "candidate_count": int(dry.get("event_candidate_count", -1))
        == len(events)
        == 8,
        "event_count": int(dry.get("refined_event_count", -1)) == len(events),
        "event_cache_current": M5326.event_cache_current(),
        "initial_count": len(initial)
        == M5326.expected_initial_segment_count(events),
        "plan_hash": dry.get("node_plan_sha256")
        == read_json(RESULT_5341).get("node_plan_sha256"),
        "parent_validation": all(
            parse_bool(row["passed"]) for row in read_csv(M5326.VALIDATION_5325)
        ),
    }
    if not all(checks.values()):
        raise RuntimeError(
            "saved E00125 dry-run is stale; refusing automatic event re-derivation: "
            + json.dumps(checks, sort_keys=True)
        )
    return dry


def dry_run() -> dict[str, Any]:
    started = time.perf_counter()
    configure()
    M5312.set_below_normal_priority()
    OUT.mkdir(parents=True, exist_ok=True)
    sources = write_source_register()
    coefficients = coefficient_rows()
    parent_5342 = read_json(RESULT_5342)
    validation_5342 = read_csv(VALIDATION_5342)
    M5326.EXPECTED_EVENT_COUNT = len(read_csv(M5326.EVENTS))
    cache_current = M5326.event_cache_current()
    if not cache_current:
        raise RuntimeError("E00125 event cache is stale; refusing a root rescan")
    parent_dry = validated_cached_dry_run_only()
    preflight = correction_preflight(coefficients)
    gates = [
        validation_row(
            "all_source_paths_exist_and_are_hashed",
            len(sources) == 10
            and all(parse_bool(row["exists"]) for row in sources)
            and all(row["sha256"] != "MISSING" for row in sources),
            f"rows={len(sources)}",
        ),
        validation_row(
            "checkpoint_5342_four_endpoint_normal_forms_pass",
            parent_5342.get("validation_passed") is True
            and all(parse_bool(row["passed"]) for row in validation_5342)
            and len(coefficients) == 4,
            str(parent_5342.get("decision")),
        ),
        validation_row(
            "E00125_event_cache_is_current_without_root_rescan",
            cache_current
            and int(parent_dry.get("refined_event_count", -1)) == 8
            and int(parent_dry.get("event_candidate_count", -1)) == 8,
            str(parent_dry.get("decision")),
        ),
        validation_row(
            "eight_depth_four_event_sides_have_cut_safe_models",
            len(preflight) == 8
            and all(parse_bool(row["preflight_passes"]) for row in preflight),
            f"rows={len(preflight)}",
        ),
        validation_row(
            "unchanged_local_and_global_gates_are_active",
            M5326.LOCAL_OUTER_CHANGE_LIMIT == 5.0e-3
            and M5326.GLOBAL_ERROR_BUDGET_LIMIT == 1.0e-2
            and M5326.MAXIMUM_ADAPTIVE_DEPTH == MAXIMUM_ADAPTIVE_DEPTH,
            (
                f"local={M5326.LOCAL_OUTER_CHANGE_LIMIT};"
                f"global={M5326.GLOBAL_ERROR_BUDGET_LIMIT};"
                f"depth={M5326.MAXIMUM_ADAPTIVE_DEPTH}"
            ),
        ),
        validation_row(
            "dry_run_promotes_no_integral_claim",
            all(not value for value in no_claims().values()),
            "preflight only",
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
    value = {
        "checkpoint": CHECKPOINT,
        "marker": MARKER,
        "mode": "D4-E00125-log-corrected-runner-dry-run",
        "validation_passed": passed,
        "decision": (
            "D4_E00125_LOG_CORRECTED_RUNNER_PREFLIGHT_PASSES__LAUNCH_BOUNDED_RUN"
            if passed
            else "D4_E00125_LOG_CORRECTED_RUNNER_PREFLIGHT_BLOCKED"
        ),
        "epsilon_id": EPSILON_ID,
        "epsilon": EPSILON,
        "preflight_event_side_count": len(preflight),
        "maximum_adaptive_depth": MAXIMUM_ADAPTIVE_DEPTH,
        "runtime_limit_hours_for_next_run": DEFAULT_RUNTIME_HOURS,
        "claim_boundary": no_claims(),
        "source_files": sources,
        "formalization_workbench_modified_file_count": 0,
        "next_action": "RUN_RESUMABLE_E00125_WORKER" if passed else "FIX_PREFLIGHT",
        "runtime_seconds": time.perf_counter() - started,
        "updated_utc": utc_now(),
    }
    atomic_json(RESULT, value)
    atomic_json(
        STATUS,
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "state": "PREFLIGHT_COMPLETE" if passed else "PREFLIGHT_BLOCKED",
            "decision": value["decision"],
            "validation_passed": passed,
            "worker_pid": os.getpid(),
            "updated_utc": utc_now(),
        },
    )
    return value


def corrected_panel_wrapper(
    coefficients: list[dict[str, str]],
    audit: list[dict[str, Any]],
) -> tuple[Any, Any]:
    original = M5326.evaluate_panel

    def evaluate(
        panel: dict[str, Any],
        contract: list[dict[str, str]],
        expected_plan_sha256: str,
        base_context: dict[str, Any],
        multiplier: float,
        started: float,
        runtime_limit_seconds: float,
        encountered: dict[str, dict[str, Any]],
    ) -> dict[str, Any] | None:
        raw = original(
            panel,
            contract,
            expected_plan_sha256,
            base_context,
            multiplier,
            started,
            runtime_limit_seconds,
            encountered,
        )
        if raw is None or str(panel.get("event_type", "")) not in SUPPORT_EVENT_TYPES:
            return raw
        coordinate_text = str(panel.get("event_coordinate", "")).strip()
        if not coordinate_text:
            return raw
        coefficient = coefficient_for_coordinate(float(coordinate_text), coefficients)
        x0 = float(coefficient["event_coordinate"])
        z0 = complex_from(coefficient, "boundary_gap_z0")
        z1 = complex_from(coefficient, "boundary_gap_derivative_z1")
        coefficient0 = complex_from(coefficient, "physical_coefficient_C0")
        coefficient1 = complex_from(
            coefficient, "physical_coefficient_derivative_C1"
        )
        log_sign = int(coefficient["log_sign"])
        nodes = M5326.panel_nodes(panel)
        totals = {
            order: {"raw": 0.0j, "model": 0.0j, "regular": 0.0j}
            for order in M5326.OUTER_ORDERS
        }
        selected_energy_order = max(M5312.ENERGY_ORDERS)
        for node in nodes:
            shard = read_json(M5312.shard_paths(node["node_id"])["result"])
            value = complex(
                float(shard[f"inner_energy_Q{selected_energy_order}_real"]),
                float(shard[f"inner_energy_Q{selected_energy_order}_imaginary"]),
            )
            delta = float(node["absolute_soft_cosine"]) - x0
            model = M5342.affine_log_value(
                delta, log_sign, coefficient0, coefficient1, z0, z1
            )
            weight = float(node["mapped_outer_weight"])
            order = int(node["outer_order"])
            totals[order]["raw"] += weight * value
            totals[order]["model"] += weight * model
            totals[order]["regular"] += weight * (value - model)
        lower_delta = float(panel["lower_absolute_soft_cosine"]) - x0
        upper_delta = float(panel["upper_absolute_soft_cosine"]) - x0
        cut_crossed = principal_log_cut_crossed(lower_delta, upper_delta, z0, z1)
        exact_model = M5342.affine_log_primitive(
            upper_delta, log_sign, coefficient0, coefficient1, z0, z1
        ) - M5342.affine_log_primitive(
            lower_delta, log_sign, coefficient0, coefficient1, z0, z1
        )
        reconstructed = {
            order: totals[order]["regular"] + exact_model
            for order in M5326.OUTER_ORDERS
        }
        raw_q4 = complex_from(raw, "outer_Q4_inner_Q8")
        raw_q8 = complex_from(raw, "outer_Q8_inner_Q8")
        raw_reproduction_error = max(
            relative_complex_change(raw_q4, totals[4]["raw"]),
            relative_complex_change(raw_q8, totals[8]["raw"]),
        )
        raw_change = relative_complex_change(totals[4]["raw"], totals[8]["raw"])
        regular_change = relative_complex_change(
            totals[4]["regular"], totals[8]["regular"]
        )
        reconstructed_change = relative_complex_change(
            reconstructed[4], reconstructed[8]
        )
        model_q8_error = relative_complex_change(totals[8]["model"], exact_model)
        correction_applied = (
            int(panel["adaptive_depth"]) >= ENDPOINT_CORRECTION_MINIMUM_DEPTH
            and raw_change > M5326.LOCAL_OUTER_CHANGE_LIMIT
            and not cut_crossed
            and raw_reproduction_error <= 5.0e-13
            and model_q8_error < raw_change
            and regular_change <= M5326.LOCAL_OUTER_CHANGE_LIMIT
            and reconstructed_change <= M5326.LOCAL_OUTER_CHANGE_LIMIT
            and reconstructed_change < raw_change
        )
        if correction_applied:
            raw.update(complex_fields("raw_outer_Q4_inner_Q8", totals[4]["raw"]))
            raw.update(complex_fields("raw_outer_Q8_inner_Q8", totals[8]["raw"]))
            raw.update(
                complex_fields("outer_Q4_inner_Q8", reconstructed[4])
            )
            raw.update(
                complex_fields("outer_Q8_inner_Q8", reconstructed[8])
            )
            raw["raw_outer_Q4_Q8_relative_change"] = raw_change
            raw["outer_Q4_Q8_absolute_change"] = abs(
                reconstructed[8] - reconstructed[4]
            )
            raw["outer_Q4_Q8_relative_change"] = reconstructed_change
            raw["adaptive_gate_passes"] = (
                parse_bool(raw["all_inner_nodes_pass"])
                and parse_bool(raw["exact_change_of_variables_gate_passes"])
                and reconstructed_change <= M5326.LOCAL_OUTER_CHANGE_LIMIT
            )
        raw["endpoint_correction_applied"] = correction_applied
        raw["endpoint_correction_event_id"] = coefficient["event_id"]
        raw["endpoint_correction_method"] = (
            "PARENT_AFFINE_COMPLEX_LOG_ADD_SUBTRACT"
            if correction_applied
            else "DIAGNOSTIC_ONLY"
        )
        raw["endpoint_regular_remainder_Q4_Q8_relative_change"] = regular_change
        raw["endpoint_reconstructed_Q4_Q8_relative_change"] = reconstructed_change
        raw["endpoint_model_Q8_relative_error"] = model_q8_error
        raw["endpoint_raw_reproduction_relative_error"] = raw_reproduction_error
        raw["endpoint_principal_log_cut_crossed"] = cut_crossed
        audit.append(
            {
                "adaptive_panel_id": panel["adaptive_panel_id"],
                "adaptive_depth": panel["adaptive_depth"],
                "event_id": coefficient["event_id"],
                "event_type": panel["event_type"],
                "lower_absolute_soft_cosine": panel[
                    "lower_absolute_soft_cosine"
                ],
                "upper_absolute_soft_cosine": panel[
                    "upper_absolute_soft_cosine"
                ],
                "raw_Q4_Q8_relative_change": raw_change,
                "regular_remainder_Q4_Q8_relative_change": regular_change,
                "reconstructed_Q4_Q8_relative_change": reconstructed_change,
                "model_Q8_relative_error": model_q8_error,
                "raw_reproduction_relative_error": raw_reproduction_error,
                "principal_log_cut_crossed": cut_crossed,
                "correction_applied": correction_applied,
                **complex_fields("exact_log_model_integral", exact_model),
                **no_claims(),
            }
        )
        return raw

    M5326.evaluate_panel = evaluate
    return original, evaluate


def add_coordinate_budget_and_sources(
    raw_result: dict[str, Any],
    coefficients: list[dict[str, str]],
) -> dict[str, Any]:
    coordinate_error = sum(
        float(row["endpoint_coordinate_sensitivity_absolute"])
        for row in coefficients
    )
    value = dict(raw_result)
    outer_error = float(value["outer_error_absolute_conservative"])
    inner_error = float(value["inner_error_absolute_conservative"])
    high = complex_from(value, "fixed_decay_integral")
    total_error = outer_error + inner_error + coordinate_error
    relative_error = total_error / max(abs(high), 1.0e-300)
    accepted = (
        parse_bool(value.get("completed_full_run", False))
        and parse_bool(value.get("all_adaptive_leaf_gates_pass", False))
        and relative_error <= M5326.GLOBAL_ERROR_BUDGET_LIMIT
    )
    value["event_coordinate_error_absolute_conservative"] = coordinate_error
    value["total_error_absolute_conservative"] = total_error
    value["total_error_relative_conservative"] = relative_error
    value["acceptance_passed"] = accepted
    value["finite_regulator_fixed_decay_integral_accepted"] = accepted
    canonical = M5334.canonicalize_refinement_result(value)
    fixed_claim = M5334.d4_fixed_decay_claim_field()
    canonical["claim_boundary"][fixed_claim] = accepted
    canonical["endpoint_correction_checkpoint"] = CHECKPOINT
    canonical["endpoint_correction_method"] = (
        "PARENT_AFFINE_COMPLEX_LOG_ADD_SUBTRACT_AT_FAILED_DEPTH4_EVENT_LEAVES"
    )
    canonical["event_coordinate_error_absolute_conservative"] = coordinate_error
    canonical["total_error_absolute_conservative"] = total_error
    canonical["total_error_relative_conservative"] = relative_error
    canonical["acceptance_passed"] = accepted
    canonical["finite_regulator_fixed_decay_integral_accepted"] = accepted
    extra_sources = {
        Path(__file__).resolve(),
        SCRIPT_5342.resolve(),
        RESULT_5342.resolve(),
        COEFFICIENTS_5342.resolve(),
        VALIDATION_5342.resolve(),
    }
    source_paths = {
        Path(row["path"]).resolve()
        for row in canonical.get("source_files", [])
        if Path(row["path"]).exists()
    } | extra_sources
    canonical["source_files"] = [
        {"path": str(path), "sha256": digest(path)}
        for path in sorted(source_paths, key=str)
    ]
    atomic_json(M5326.RESULT, canonical)
    finite = read_csv(M5326.FINITE_VALUE)
    if len(finite) != 1:
        raise RuntimeError(f"expected one E00125 finite row, found {len(finite)}")
    row = finite[0]
    row["event_coordinate_error_absolute_conservative"] = coordinate_error
    row["total_error_absolute_conservative"] = total_error
    row["total_error_relative_conservative"] = relative_error
    row["finite_regulator_fixed_decay_integral_accepted"] = accepted
    row[fixed_claim] = accepted
    row["endpoint_correction_checkpoint"] = CHECKPOINT
    row["endpoint_correction_method"] = canonical["endpoint_correction_method"]
    for field in CLAIM_FIELDS:
        if field != fixed_claim:
            row[field] = False
    write_csv(M5326.FINITE_VALUE, finite)
    M5334.canonicalize_refinement_status(canonical)
    return canonical


def run(runtime_hours: float) -> dict[str, Any]:
    started = time.perf_counter()
    configure()
    M5312.set_below_normal_priority()
    OUT.mkdir(parents=True, exist_ok=True)
    preflight_result = dry_run()
    if not preflight_result["validation_passed"]:
        raise RuntimeError("5343 preflight did not pass")
    atomic_json(
        STATUS,
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "state": "RUNNING",
            "stage": "D4_E00125_LOG_CORRECTED_RESUMABLE_REFINEMENT",
            "worker_pid": os.getpid(),
            "runtime_limit_hours": runtime_hours,
            "updated_utc": utc_now(),
        },
    )
    coefficients = coefficient_rows()
    M5326.EXPECTED_EVENT_COUNT = len(read_csv(M5326.EVENTS))
    if not M5326.event_cache_current():
        raise RuntimeError("E00125 event cache is stale; refusing a root rescan")
    correction_audit: list[dict[str, Any]] = []
    original_evaluate, _ = corrected_panel_wrapper(coefficients, correction_audit)
    original_derive_events = M5326.derive_events
    original_load_validated_dry_run = M5326.load_validated_dry_run

    def cached_events_only() -> list[dict[str, str]]:
        if not M5326.event_cache_current():
            raise RuntimeError("refusing duplicate E00125 root derivation")
        return read_csv(M5326.EVENTS)

    M5326.derive_events = cached_events_only
    M5326.load_validated_dry_run = validated_cached_dry_run_only
    try:
        parent_raw = M5326.execute(runtime_hours * 3600.0)
    finally:
        M5326.evaluate_panel = original_evaluate
        M5326.derive_events = original_derive_events
        M5326.load_validated_dry_run = original_load_validated_dry_run
    if correction_audit:
        write_csv(CORRECTION_AUDIT, correction_audit)
    canonical = add_coordinate_budget_and_sources(parent_raw, coefficients)
    completed = parse_bool(canonical.get("completed_full_run", False))
    parent_validation: dict[str, Any] | None = None
    if completed:
        parent_validation = M5334.validate_refinement_outputs()
    sources = write_source_register()
    manifest = read_csv(M5326.NODE_MANIFEST) if M5326.NODE_MANIFEST.exists() else []
    panels = read_csv(M5326.ADAPTIVE_PANELS) if M5326.ADAPTIVE_PANELS.exists() else []
    leaves = [row for row in panels if parse_bool(row.get("adaptive_leaf", False))]
    applied = [row for row in correction_audit if parse_bool(row["correction_applied"])]
    fixed_claim = M5334.d4_fixed_decay_claim_field()
    accepted = parse_bool(canonical.get("acceptance_passed", False))
    state_consistent = (
        completed
        and accepted
        and parent_validation is not None
        and parse_bool(parent_validation.get("acceptance_passed", False))
        or (
            not completed
            and not accepted
            and not parse_bool(canonical["claim_boundary"].get(fixed_claim, False))
        )
    )
    gates = [
        validation_row(
            "all_source_paths_exist_and_are_hashed",
            len(sources) == 10
            and all(parse_bool(row["exists"]) for row in sources)
            and all(row["sha256"] != "MISSING" for row in sources),
            f"rows={len(sources)}",
        ),
        validation_row(
            "checkpoint_5342_endpoint_coefficients_remain_valid",
            read_json(RESULT_5342).get("validation_passed") is True
            and all(
                parse_bool(row["valid_for_D4_E00125_support_endpoint_coefficients"])
                for row in coefficients
            ),
            f"events={len(coefficients)}",
        ),
        validation_row(
            "all_completed_inner_nodes_pass",
            bool(manifest)
            and all(row["shard_state"] != "COMPLETE_FAIL" for row in manifest)
            and int(canonical.get("failed_inner_node_count", 0)) == 0,
            f"encountered={len(manifest)};completed={canonical.get('completed_node_count')}",
        ),
        validation_row(
            "every_applied_endpoint_correction_passes_safety_contract",
            all(
                not parse_bool(row["principal_log_cut_crossed"])
                and float(row["raw_reproduction_relative_error"]) <= 5.0e-13
                and float(row["regular_remainder_Q4_Q8_relative_change"])
                <= M5326.LOCAL_OUTER_CHANGE_LIMIT
                and float(row["reconstructed_Q4_Q8_relative_change"])
                <= M5326.LOCAL_OUTER_CHANGE_LIMIT
                and float(row["reconstructed_Q4_Q8_relative_change"])
                < float(row["raw_Q4_Q8_relative_change"])
                for row in applied
            ),
            f"applied={len(applied)};diagnostics={len(correction_audit)}",
        ),
        validation_row(
            "four_event_coordinate_sensitivity_terms_are_in_budget",
            abs(
                float(canonical["event_coordinate_error_absolute_conservative"])
                - sum(
                    float(row["endpoint_coordinate_sensitivity_absolute"])
                    for row in coefficients
                )
            )
            <= 1.0e-15,
            str(canonical["event_coordinate_error_absolute_conservative"]),
        ),
        validation_row(
            "resumable_or_complete_claim_state_is_consistent",
            state_consistent,
            (
                f"completed={completed};accepted={accepted};"
                f"decision={canonical.get('decision')}"
            ),
        ),
        validation_row(
            "complete_run_requires_all_leaves_and_global_budget",
            not completed
            or (
                bool(leaves)
                and all(parse_bool(row["adaptive_gate_passes"]) for row in leaves)
                and float(canonical["total_error_relative_conservative"])
                <= M5326.GLOBAL_ERROR_BUDGET_LIMIT
            ),
            (
                f"complete={completed};leaves={len(leaves)};"
                f"relative={canonical.get('total_error_relative_conservative')}"
            ),
        ),
        validation_row(
            "broader_claims_remain_false",
            not parse_bool(
                canonical["claim_boundary"][
                    "valid_for_D4_outer_regulator_zero_limit"
                ]
            )
            and all(
                not parse_bool(canonical["claim_boundary"].get(field, False))
                for field in M5326.CLAIM_FIELDS
            ),
            "regulator-zero and broader claims are separate",
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
    claims["valid_for_D4_outer_E00125_fixed_decay_integral"] = bool(
        completed and accepted and passed
    )
    value = {
        "checkpoint": CHECKPOINT,
        "marker": MARKER,
        "mode": "D4-E00125-log-corrected-resumable-run",
        "validation_passed": passed,
        "decision": (
            "D4_E00125_LOG_CORRECTED_FIXED_DECAY_RUNG_ACCEPTED"
            if claims["valid_for_D4_outer_E00125_fixed_decay_integral"]
            else "D4_E00125_LOG_CORRECTED_RUN_PAUSED__RESUME_SAVED_SHARDS"
            if not completed
            else "D4_E00125_LOG_CORRECTED_COMPLETE_BUT_BLOCKED"
        ),
        "epsilon_id": EPSILON_ID,
        "epsilon": EPSILON,
        "completed_full_run": completed,
        "encountered_node_count": len(manifest),
        "completed_node_count": canonical.get("completed_node_count"),
        "adaptive_leaf_count": len(leaves),
        "endpoint_correction_diagnostic_count": len(correction_audit),
        "endpoint_correction_applied_count": len(applied),
        **complex_fields("fixed_decay_integral", complex_from(canonical, "fixed_decay_integral")),
        "outer_error_absolute_conservative": canonical[
            "outer_error_absolute_conservative"
        ],
        "inner_error_absolute_conservative": canonical[
            "inner_error_absolute_conservative"
        ],
        "event_coordinate_error_absolute_conservative": canonical[
            "event_coordinate_error_absolute_conservative"
        ],
        "total_error_absolute_conservative": canonical[
            "total_error_absolute_conservative"
        ],
        "total_error_relative_conservative": canonical[
            "total_error_relative_conservative"
        ],
        "claim_boundary": claims,
        "source_files": sources,
        "formalization_workbench_modified_file_count": 0,
        "next_action": (
            "BUILD_TWO_RUNG_REGULATOR_CONTRAST"
            if claims["valid_for_D4_outer_E00125_fixed_decay_integral"]
            else "RESUME_E00125_SAVED_SHARDS"
            if not completed
            else "AUDIT_FAILED_E00125_LEAVES"
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
            "state": "COMPLETE" if completed else "PAUSED_RESUMABLE",
            "decision": value["decision"],
            "validation_passed": passed,
            "worker_pid": os.getpid(),
            "completed_node_count": canonical.get("completed_node_count"),
            "encountered_node_count": len(manifest),
            "updated_utc": utc_now(),
        },
    )
    return value


def validate_saved() -> dict[str, Any]:
    configure()
    if not RESULT.exists():
        raise FileNotFoundError(RESULT)
    value = read_json(RESULT)
    rows = read_csv(VALIDATION)
    current = all(
        Path(row["path"]).exists()
        and digest(Path(row["path"])) == row["sha256"]
        for row in value["source_files"]
    )
    value["validation_passed"] = bool(rows) and all(
        parse_bool(row["passed"]) for row in rows
    ) and current
    return value


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("dry-run", "run", "validate"), required=True)
    parser.add_argument("--max-runtime-hours", type=float, default=DEFAULT_RUNTIME_HOURS)
    arguments = parser.parse_args()
    M5312.set_below_normal_priority()
    try:
        if arguments.mode == "dry-run":
            value = dry_run()
        elif arguments.mode == "run":
            if arguments.max_runtime_hours <= 0.0:
                raise ValueError("--max-runtime-hours must be positive")
            value = run(arguments.max_runtime_hours)
        else:
            value = validate_saved()
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
                "worker_pid": os.getpid(),
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
                "runtime_seconds": value.get("runtime_seconds"),
            },
            sort_keys=True,
        ),
        flush=True,
    )
    return 0 if value["validation_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
