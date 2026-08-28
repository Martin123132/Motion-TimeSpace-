from __future__ import annotations

import argparse
import cmath
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


CHECKPOINT = 5342
MARKER = "MTS_5342_D4_E00125_GENERIC_SUPPORT_ENDPOINT_NORMAL_FORM"
EPSILON_ID = "E00125"
EPSILON = 0.00125
POST = Path(__file__).resolve().parents[1]
SCRIPTS = POST / "scripts"
OUT = POST / "source-intake" / "functional_rg" / str(CHECKPOINT)
RESIDUALS = POST / "source-intake" / "mts_residuals"
VALIDATION = RESIDUALS / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv"
SCRIPT_5339 = SCRIPTS / "Y5_R2FR_5339_D4_E08_support_exit_log_subtraction.py"
RESULT_5341 = (
    POST
    / "source-intake/functional_rg/5341/D4_E00125_event_evidence_migration_result.json"
)
VALIDATION_5341 = RESIDUALS / "P8_Y5_BRR545_5341_VALIDATION.csv"
SCAN_5337 = POST / "source-intake/functional_rg/5337/D4_targeted_event_regulator_scan.csv"
STENCIL = OUT / "D4_E00125_support_endpoint_stencil.csv"
COEFFICIENTS = OUT / "D4_E00125_support_endpoint_coefficients.csv"
SOURCE_REGISTER = OUT / "source_register.csv"
RESULT = OUT / "D4_E00125_support_endpoint_normal_form_result.json"
STATUS = OUT / "status.json"
FORMAL_DIGEST = "0ec1bc6012136ffc6b28a1512aca6ce712b6decd2ff793310a9bd61775f3db1f"
TRACE_LIMIT = 1.0e-5
DERIVATIVE_LIMIT = 2.5e-2
PRIMITIVE_DERIVATIVE_LIMIT = 2.5e-6
CLAIM_FIELDS = (
    "valid_for_D4_E00125_support_endpoint_coefficients",
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


M5339 = load_module("mts_5339_for_5342", SCRIPT_5339)
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


def configure() -> Any:
    M5334.configure_ladder()
    M5334.configure_D4_target(EPSILON_ID)
    return M5326.configure_kernel()


def source_paths() -> list[Path]:
    return [
        Path(__file__).resolve(),
        SCRIPT_5339,
        Path(M5334.__file__).resolve(),
        RESULT_5341,
        VALIDATION_5341,
        SCAN_5337,
        M5326.EVENTS,
        M5326.CONTRACT_5325,
        M5326.POLES_5325,
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


def endpoint_state(
    event: dict[str, str],
    scan: dict[str, str],
    coordinate: float,
    contract: list[dict[str, str]],
    base_context: dict[str, Any],
    multiplier: float,
    label: str,
) -> dict[str, Any]:
    panel_index = int(event["x_panel_index"])
    term_id = event["term_id"]
    surface_id = event["primary_surface_id"]
    boundary = scan["contact_boundary"]
    cells = [
        M5312.cell_geometry(row, coordinate)
        for row in contract
        if int(row["x_panel_index"]) == panel_index
        and int(row["reduced_MC04_term_count"]) > 0
    ]
    supports = M5312.merged_term_supports(cells).get(term_id, [])
    node = {
        "node_id": f"{event['event_id']}_ENDPOINT_{label}",
        "x_panel_index": panel_index,
        "outer_order": 0,
        "absolute_soft_cosine": coordinate,
    }
    poles = [
        row
        for row in M5312.scan_term_poles(node, term_id, supports)
        if row["primary_surface_id"] == surface_id
    ]
    if len(poles) != 1:
        raise RuntimeError(
            f"expected one {event['event_id']} pole at {coordinate}, found {len(poles)}"
        )
    geometric = poles[0]
    _, support = M5326.support_margin(float(geometric["pole_real"]), supports)
    source = {
        **geometric,
        "support_id": support["support_id"],
        "support_energy_lower": support["lower"],
        "support_energy_upper": support["upper"],
        "support_contract_indices": "|".join(
            str(value) for value in support["contracts"]
        ),
    }
    evaluator = M5326.near_support_unmasked_evaluator(base_context, term_id)
    selected, fits = M5326.refine_near_support_simple_pole(
        coordinate, source, evaluator
    )
    pole = complex(selected["refined_pole"])
    residue = complex(selected["selected_residue"])
    coefficient = multiplier * residue
    lower = float(selected["support_energy_lower"])
    upper = float(selected["support_energy_upper"])
    boundary_energy = lower if boundary == "LOWER" else upper
    gap = complex(boundary_energy, 0.0) - pole
    return {
        "event_id": event["event_id"],
        "event_type": event["event_type"],
        "x_panel_index": panel_index,
        "term_id": term_id,
        "primary_surface_id": surface_id,
        "contact_boundary": boundary,
        "log_sign": -1 if boundary == "LOWER" else 1,
        "stencil_label": label,
        "absolute_soft_cosine": coordinate,
        "support_id": source["support_id"],
        "fit_contract_passes": bool(selected["fit_contract_passes"]),
        "fit_relative_residual": float(selected["fit_relative_residual"]),
        "residue_scale_relative_change": float(
            selected["residue_fit_scale_relative_change"]
        ),
        "second_order_suppression_ratio": float(
            selected["second_order_suppression_ratio"]
        ),
        "fit_row_count": len(fits),
        "support_energy_lower": lower,
        "support_energy_upper": upper,
        **complex_fields("refined_pole", pole),
        **complex_fields("endpoint_residue", residue),
        **complex_fields("physical_endpoint_coefficient", coefficient),
        **complex_fields("boundary_gap", gap),
        **no_claims(),
    }


def affine_log_value(
    delta: float,
    log_sign: int,
    coefficient0: complex,
    coefficient1: complex,
    z0: complex,
    z1: complex,
) -> complex:
    return log_sign * (coefficient0 + coefficient1 * delta) * cmath.log(
        z0 + z1 * delta
    )


def affine_log_primitive(
    upper: float,
    log_sign: int,
    coefficient0: complex,
    coefficient1: complex,
    z0: complex,
    z1: complex,
) -> complex:
    if abs(z1) <= 1.0e-300:
        raise ZeroDivisionError("endpoint boundary-gap derivative vanishes")
    affine_z_coefficient = coefficient1 / z1
    constant_z_coefficient = coefficient0 - affine_z_coefficient * z0

    def primitive_z(z: complex) -> complex:
        return (
            constant_z_coefficient * (z * cmath.log(z) - z)
            + affine_z_coefficient
            * (0.5 * z * z * cmath.log(z) - 0.25 * z * z)
        ) / z1

    return log_sign * (primitive_z(z0 + z1 * upper) - primitive_z(z0))


def primitive_derivative_error(
    derivative_step: float,
    log_sign: int,
    coefficient0: complex,
    coefficient1: complex,
    z0: complex,
    z1: complex,
) -> float:
    probe = 0.37 * derivative_step
    difference_step = max(1.0e-5 * derivative_step, 1.0e-12)
    numerical = (
        affine_log_primitive(
            probe + difference_step,
            log_sign,
            coefficient0,
            coefficient1,
            z0,
            z1,
        )
        - affine_log_primitive(
            probe - difference_step,
            log_sign,
            coefficient0,
            coefficient1,
            z0,
            z1,
        )
    ) / (2.0 * difference_step)
    expected = affine_log_value(
        probe, log_sign, coefficient0, coefficient1, z0, z1
    )
    return relative_complex_change(expected, numerical)


def event_normal_form(
    event: dict[str, str],
    scan: dict[str, str],
    contract: list[dict[str, str]],
    base_context: dict[str, Any],
    multiplier: float,
    cached_stencil: list[dict[str, str]],
    cached_coefficients: list[dict[str, str]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    coordinate = float(event["event_coordinate"])
    slope = float(event["source_crossing_slope"])
    gamma = abs(float(scan["pole_imaginary"]))
    boundary_scale = gamma / abs(slope)
    coordinate_error = float(event["event_coordinate_error_estimate"])
    prior_coefficients = [
        row
        for row in cached_coefficients
        if row.get("event_id") == event["event_id"]
    ]
    stencil_scale = 0.5
    if len(prior_coefficients) == 1 and not parse_bool(
        prior_coefficients[0]["coefficient_contract_passes"]
    ):
        prior_step = float(prior_coefficients[0]["derivative_step"])
        stencil_scale = min(1.0, 2.0 * prior_step / boundary_scale)
    derivative_step = max(stencil_scale * boundary_scale, 64.0 * coordinate_error)
    half_step = 0.5 * derivative_step
    offsets = (
        ("M1", -derivative_step),
        ("MH", -half_step),
        ("C0", 0.0),
        ("PH", half_step),
        ("P1", derivative_step),
    )
    rows: list[dict[str, Any]] = []
    event_cache = [
        row for row in cached_stencil if row.get("event_id") == event["event_id"]
    ]
    for label, offset in offsets:
        matches = [
            row
            for row in event_cache
            if abs(float(row["delta_from_event"]) - offset)
            <= max(1.0e-15, 1.0e-8 * abs(offset))
        ]
        if len(matches) == 1 and parse_bool(matches[0]["fit_contract_passes"]):
            row: dict[str, Any] = dict(matches[0])
            row["stencil_label"] = label
            row["stencil_source"] = "REUSED_PRIOR_GOOD_PARENT_FIT"
        else:
            row = endpoint_state(
                event,
                scan,
                coordinate + offset,
                contract,
                base_context,
                multiplier,
                label,
            )
            row["stencil_source"] = "DIRECT_PARENT_REEVALUATION"
        rows.append(row)
    for row, (_, offset) in zip(rows, offsets):
        row["delta_from_event"] = offset
        row["physical_multiplier"] = multiplier
        row["geometric_event_slope"] = slope
        row["geometric_gamma_seed"] = gamma
        row["boundary_layer_scale_seed"] = boundary_scale
    by_label = {row["stencil_label"]: row for row in rows}
    minus = by_label["M1"]
    minus_half = by_label["MH"]
    center = by_label["C0"]
    plus_half = by_label["PH"]
    plus = by_label["P1"]
    z0_left = 2.0 * complex_from(minus_half, "boundary_gap") - complex_from(
        minus, "boundary_gap"
    )
    z0_right = 2.0 * complex_from(plus_half, "boundary_gap") - complex_from(
        plus, "boundary_gap"
    )
    coefficient0_left = 2.0 * complex_from(
        minus_half, "physical_endpoint_coefficient"
    ) - complex_from(minus, "physical_endpoint_coefficient")
    coefficient0_right = 2.0 * complex_from(
        plus_half, "physical_endpoint_coefficient"
    ) - complex_from(plus, "physical_endpoint_coefficient")
    z0 = 0.5 * (z0_left + z0_right)
    coefficient0 = 0.5 * (coefficient0_left + coefficient0_right)
    z1_full = (
        complex_from(plus, "boundary_gap") - complex_from(minus, "boundary_gap")
    ) / (2.0 * derivative_step)
    z1_half = (
        complex_from(plus_half, "boundary_gap")
        - complex_from(minus_half, "boundary_gap")
    ) / derivative_step
    coefficient1_full = (
        complex_from(plus, "physical_endpoint_coefficient")
        - complex_from(minus, "physical_endpoint_coefficient")
    ) / (2.0 * derivative_step)
    coefficient1_half = (
        complex_from(plus_half, "physical_endpoint_coefficient")
        - complex_from(minus_half, "physical_endpoint_coefficient")
    ) / derivative_step
    center_coefficient = complex_from(center, "physical_endpoint_coefficient")
    selector_ratio = abs(center_coefficient) / max(abs(coefficient0), 1.0e-300)
    selector_trace_change = relative_complex_change(center_coefficient, coefficient0)
    if selector_ratio <= 1.0e-8:
        selector_class = "MASK_SUPPRESSED_MEASURE_ZERO"
    elif selector_trace_change <= TRACE_LIMIT:
        selector_class = "TRACE_CONSISTENT"
    else:
        selector_class = "UNCLASSIFIED_CENTER_SELECTOR"
    log_sign = int(center["log_sign"])
    primitive_error = primitive_derivative_error(
        derivative_step,
        log_sign,
        coefficient0,
        coefficient1_half,
        z0,
        z1_half,
    )
    z_trace_mismatch = relative_complex_change(z0_left, z0_right)
    coefficient_trace_mismatch = relative_complex_change(
        coefficient0_left, coefficient0_right
    )
    z_derivative_change = relative_complex_change(z1_full, z1_half)
    coefficient_derivative_change = relative_complex_change(
        coefficient1_full, coefficient1_half
    )
    gap_resolved = abs(z0.imag) > 0.0 and abs(z0) > 100.0 * coordinate_error * abs(
        z1_half
    )
    coefficient_contract = (
        parse_bool(event["event_contract_passes"])
        and all(parse_bool(row["fit_contract_passes"]) for row in rows)
        and len({row["support_id"] for row in rows}) == 1
        and z_trace_mismatch <= TRACE_LIMIT
        and coefficient_trace_mismatch <= TRACE_LIMIT
        and z_derivative_change <= DERIVATIVE_LIMIT
        and coefficient_derivative_change <= DERIVATIVE_LIMIT
        and selector_class != "UNCLASSIFIED_CENTER_SELECTOR"
        and gap_resolved
        and primitive_error <= PRIMITIVE_DERIVATIVE_LIMIT
    )
    coefficient_row = {
        "event_id": event["event_id"],
        "event_type": event["event_type"],
        "x_panel_index": event["x_panel_index"],
        "term_id": event["term_id"],
        "primary_surface_id": event["primary_surface_id"],
        "contact_boundary": scan["contact_boundary"],
        "log_sign": log_sign,
        "event_coordinate": coordinate,
        "event_coordinate_error_estimate": coordinate_error,
        "derivative_step": derivative_step,
        "stencil_boundary_scale_multiplier": stencil_scale,
        "boundary_layer_scale": abs(z0.imag)
        / max(abs(z1_half.real), 1.0e-300),
        **complex_fields("boundary_gap_z0", z0),
        **complex_fields("boundary_gap_derivative_z1", z1_half),
        **complex_fields("physical_coefficient_C0", coefficient0),
        **complex_fields("physical_coefficient_derivative_C1", coefficient1_half),
        "boundary_gap_trace_relative_mismatch": z_trace_mismatch,
        "physical_coefficient_trace_relative_mismatch": coefficient_trace_mismatch,
        "boundary_gap_derivative_relative_change_full_vs_half": z_derivative_change,
        "physical_coefficient_derivative_relative_change_full_vs_half": coefficient_derivative_change,
        "center_selector_to_trace_ratio": selector_ratio,
        "center_selector_trace_relative_change": selector_trace_change,
        "center_selector_class": selector_class,
        "primitive_derivative_relative_error": primitive_error,
        "endpoint_coordinate_sensitivity_absolute": abs(coefficient0)
        * abs(z1_half / z0)
        * coordinate_error,
        "all_five_fit_contracts_pass": all(
            parse_bool(row["fit_contract_passes"]) for row in rows
        ),
        "support_id_is_stable": len({row["support_id"] for row in rows}) == 1,
        "endpoint_gap_is_regulator_resolved": gap_resolved,
        "coefficient_contract_passes": coefficient_contract,
        **no_claims(),
    }
    return rows, coefficient_row


def execute() -> dict[str, Any]:
    started = time.perf_counter()
    M5312.set_below_normal_priority()
    OUT.mkdir(parents=True, exist_ok=True)
    old = configure()
    try:
        sources = write_source_register()
        events = [
            row
            for row in read_csv(M5326.EVENTS)
            if row["event_type"] in {"SUPPORT_ENTRY", "SUPPORT_EXIT"}
        ]
        scans = {
            row["event_id"]: row
            for row in read_csv(SCAN_5337)
            if row["epsilon_id"] == EPSILON_ID
            and row["event_type"] in {"SUPPORT_ENTRY", "SUPPORT_EXIT"}
        }
        contract = read_csv(M5326.CONTRACT_5325)
        base_context = M5312.M5303.synthetic_context()
        multiplier = float(M5312.M5309.physical_multiplier())
        cached_stencil = read_csv(STENCIL) if STENCIL.exists() else []
        cached_coefficients = read_csv(COEFFICIENTS) if COEFFICIENTS.exists() else []
        stencil_rows: list[dict[str, Any]] = []
        coefficient_rows: list[dict[str, Any]] = []
        for event in sorted(events, key=lambda row: row["event_id"]):
            rows, coefficient = event_normal_form(
                event,
                scans[event["event_id"]],
                contract,
                base_context,
                multiplier,
                cached_stencil,
                cached_coefficients,
            )
            stencil_rows.extend(rows)
            coefficient_rows.append(coefficient)
    finally:
        M5326.restore_kernel(old)
    parent = read_json(RESULT_5341)
    parent_validation = read_csv(VALIDATION_5341)
    event_ids = [row["event_id"] for row in coefficient_rows]
    gates = [
        validation_row(
            "all_source_paths_exist_and_are_hashed",
            len(sources) == 9
            and all(parse_bool(row["exists"]) for row in sources)
            and all(row["sha256"] != "MISSING" for row in sources),
            f"rows={len(sources)}",
        ),
        validation_row(
            "checkpoint_5341_event_geometry_passes",
            parent.get("validation_passed") is True
            and parent.get("claim_boundary", {}).get(
                "valid_for_D4_outer_E00125_event_geometry"
            )
            is True
            and all(parse_bool(row["passed"]) for row in parent_validation),
            str(parent.get("decision")),
        ),
        validation_row(
            "exactly_four_support_endpoints_are_derived",
            event_ids == ["E01", "E02", "E03", "E08"]
            and len(stencil_rows) == 20,
            f"events={'|'.join(event_ids)};stencil={len(stencil_rows)}",
        ),
        validation_row(
            "all_twenty_parent_endpoint_fits_pass",
            all(parse_bool(row["fit_contract_passes"]) for row in stencil_rows),
            f"rows={len(stencil_rows)}",
        ),
        validation_row(
            "one_sided_boundary_gap_and_coefficient_traces_agree",
            all(
                float(row["boundary_gap_trace_relative_mismatch"]) <= TRACE_LIMIT
                and float(row["physical_coefficient_trace_relative_mismatch"])
                <= TRACE_LIMIT
                for row in coefficient_rows
            ),
            ";".join(
                f"{row['event_id']}:z={row['boundary_gap_trace_relative_mismatch']},C={row['physical_coefficient_trace_relative_mismatch']}"
                for row in coefficient_rows
            ),
        ),
        validation_row(
            "boundary_gap_and_coefficient_derivatives_are_stable",
            all(
                float(
                    row[
                        "boundary_gap_derivative_relative_change_full_vs_half"
                    ]
                )
                <= DERIVATIVE_LIMIT
                and float(
                    row[
                        "physical_coefficient_derivative_relative_change_full_vs_half"
                    ]
                )
                <= DERIVATIVE_LIMIT
                for row in coefficient_rows
            ),
            f"limit={DERIVATIVE_LIMIT}",
        ),
        validation_row(
            "center_selector_convention_is_classified",
            all(
                row["center_selector_class"]
                in {"MASK_SUPPRESSED_MEASURE_ZERO", "TRACE_CONSISTENT"}
                for row in coefficient_rows
            ),
            "|".join(
                f"{row['event_id']}:{row['center_selector_class']}"
                for row in coefficient_rows
            ),
        ),
        validation_row(
            "all_endpoint_gaps_are_regulator_resolved",
            all(parse_bool(row["endpoint_gap_is_regulator_resolved"]) for row in coefficient_rows),
            f"events={len(coefficient_rows)}",
        ),
        validation_row(
            "generic_affine_log_primitive_differentiates_to_integrand",
            all(
                float(row["primitive_derivative_relative_error"])
                <= PRIMITIVE_DERIVATIVE_LIMIT
                for row in coefficient_rows
            ),
            f"limit={PRIMITIVE_DERIVATIVE_LIMIT}",
        ),
        validation_row(
            "all_four_endpoint_coefficient_contracts_pass",
            all(parse_bool(row["coefficient_contract_passes"]) for row in coefficient_rows),
            f"events={len(coefficient_rows)}",
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
    for row in coefficient_rows:
        row["valid_for_D4_E00125_support_endpoint_coefficients"] = bool(
            passed and parse_bool(row["coefficient_contract_passes"])
        )
    write_csv(STENCIL, stencil_rows)
    write_csv(COEFFICIENTS, coefficient_rows)
    write_csv(VALIDATION, gates)
    claims = no_claims()
    claims["valid_for_D4_E00125_support_endpoint_coefficients"] = passed
    value = {
        "checkpoint": CHECKPOINT,
        "marker": MARKER,
        "mode": "D4-E00125-generic-support-endpoint-normal-form",
        "validation_passed": passed,
        "decision": (
            "D4_E00125_FOUR_SUPPORT_ENDPOINT_NORMAL_FORMS_PASS__BUILD_CORRECTED_RUNNER"
            if passed
            else "D4_E00125_SUPPORT_ENDPOINT_NORMAL_FORM_BLOCKED"
        ),
        "epsilon_id": EPSILON_ID,
        "epsilon": EPSILON,
        "support_endpoint_count": len(coefficient_rows),
        "stencil_fit_count": len(stencil_rows),
        "maximum_boundary_gap_trace_relative_mismatch": max(
            float(row["boundary_gap_trace_relative_mismatch"])
            for row in coefficient_rows
        ),
        "maximum_physical_coefficient_trace_relative_mismatch": max(
            float(row["physical_coefficient_trace_relative_mismatch"])
            for row in coefficient_rows
        ),
        "maximum_primitive_derivative_relative_error": max(
            float(row["primitive_derivative_relative_error"])
            for row in coefficient_rows
        ),
        "endpoint_coordinate_sensitivity_absolute_sum": sum(
            float(row["endpoint_coordinate_sensitivity_absolute"])
            for row in coefficient_rows
        ),
        "claim_boundary": claims,
        "source_files": sources,
        "formalization_workbench_modified_file_count": 0,
        "next_action": (
            "RUN_BOUNDED_E00125_D4_REFINEMENT_WITH_GENERIC_ENDPOINT_SUBTRACTION"
            if passed
            else "REFINE_ONLY_FAILED_ENDPOINT_NORMAL_FORM"
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
