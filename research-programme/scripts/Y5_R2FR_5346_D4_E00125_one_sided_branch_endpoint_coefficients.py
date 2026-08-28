from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import math
import os
import sys
import time
from pathlib import Path
from typing import Any

sys.dont_write_bytecode = True

import numpy as np


CHECKPOINT = 5346
MARKER = "MTS_5346_D4_E00125_ONE_SIDED_BRANCH_ENDPOINT_COEFFICIENTS"
CHECKED_DATE = "2026-08-10"
EPSILON = 0.00125
EPSILON_ID = "E00125"
POST = Path(__file__).resolve().parents[1]
OUT = POST / "source-intake" / "functional_rg" / str(CHECKPOINT)
VALIDATION = (
    POST
    / "source-intake"
    / "mts_residuals"
    / f"P8_Y5_BRR545_{CHECKPOINT}_VALIDATION.csv"
)
STATUS = OUT / "status.json"
STENCIL = OUT / "D4_E00125_one_sided_branch_endpoint_stencil.csv"
COEFFICIENTS = OUT / "D4_E00125_one_sided_branch_endpoint_coefficients.csv"
TOTAL = OUT / "D4_E00125_all_eight_endpoint_log_coefficient.csv"
ALL_EVENTS = OUT / "D4_E00125_all_eight_endpoint_log_coefficient_ledger.csv"
RESULT = OUT / "D4_E00125_one_sided_branch_endpoint_result.json"
SOURCE_REGISTER = OUT / "source_provenance.csv"
SCRIPT_5342 = POST / "scripts" / "Y5_R2FR_5342_D4_E00125_generic_support_endpoint_normal_form.py"
EVENTS = POST / "source-intake" / "functional_rg" / "5334" / EPSILON_ID / "D4_outer_refined_support_events.csv"
CANDIDATES = POST / "source-intake" / "functional_rg" / "5334" / EPSILON_ID / "D4_outer_support_event_candidates.csv"
SCAN = POST / "source-intake" / "functional_rg" / "5337" / "D4_targeted_event_regulator_scan.csv"
SUPPORT_COEFFICIENTS = POST / "source-intake" / "functional_rg" / "5342" / "D4_E00125_support_endpoint_coefficients.csv"
EXPECTED_EVENT_IDS = ["E04", "E05", "E06", "E07"]
DISTANCE_MULTIPLIERS = [1.0, 2.0, 4.0, 8.0]
TRACE_LIMIT = 2.5e-5
DERIVATIVE_LIMIT = 0.05
PRIMITIVE_LIMIT = 5.0e-10
A_EVENT_DIAGNOSTIC_RELATIVE_LIMIT = 0.05


def load_module(name: str, path: Path) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise ImportError(path)
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


M5342 = load_module("mts_checkpoint_5342_for_5346", SCRIPT_5342)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def selected_digest(paths: list[Path]) -> str:
    value = hashlib.sha256()
    for path in sorted(paths):
        value.update(path.relative_to(POST).as_posix().encode("utf-8"))
        value.update(digest(path).encode("ascii"))
    return value.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        return []
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


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
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def parse_bool(value: Any) -> bool:
    return str(value).strip().lower() == "true"


def no_claims() -> dict[str, bool]:
    return {
        "valid_for_D4_E00125_all_eight_endpoint_coefficients": False,
        "valid_for_D4_outer_E00125_fixed_decay_integral": False,
        "valid_for_D4_outer_regulator_zero_limit": False,
        "valid_for_decay_angle_integral": False,
        "valid_for_full_phase_space_coefficient": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }


def tagged(row: dict[str, Any]) -> dict[str, Any]:
    return {
        **row,
        "checkpoint": CHECKPOINT,
        "checkpoint_marker": MARKER,
        "checked_date": CHECKED_DATE,
        **no_claims(),
    }


def complex_fields(prefix: str, value: complex) -> dict[str, float]:
    return {
        f"{prefix}_real": float(value.real),
        f"{prefix}_imaginary": float(value.imag),
        f"{prefix}_magnitude": float(abs(value)),
    }


def complex_from(row: dict[str, Any], prefix: str) -> complex:
    return complex(float(row[f"{prefix}_real"]), float(row[f"{prefix}_imaginary"]))


def relative_change(first: complex, second: complex) -> float:
    return abs(second - first) / max(abs(first), abs(second), 1.0e-300)


def finite_complex(value: complex) -> bool:
    return math.isfinite(value.real) and math.isfinite(value.imag)


def coordinate_disk_radius(
    coefficient0: complex,
    coefficient1: complex,
    z0: complex,
    z1: complex,
    coordinate_error: float,
) -> float:
    if abs(z1) <= 1.0e-300:
        return math.inf
    return coordinate_error * (
        abs(coefficient0) / EPSILON
        + abs(coefficient1 * z0 / (EPSILON * z1))
    )


def support_event_diagnostic(row: dict[str, str]) -> tuple[complex, float, float]:
    z0 = complex_from(row, "boundary_gap_z0")
    z1 = complex_from(row, "boundary_gap_derivative_z1")
    coefficient0 = complex_from(row, "physical_coefficient_C0")
    coefficient1 = complex_from(row, "physical_coefficient_derivative_C1")
    sign = int(row["log_sign"])
    value = -sign * coefficient0 * (z0 / EPSILON) / z1
    relative_envelope = sum(
        float(row[key])
        for key in [
            "boundary_gap_trace_relative_mismatch",
            "physical_coefficient_trace_relative_mismatch",
            "boundary_gap_derivative_relative_change_full_vs_half",
        ]
    )
    coordinate_radius = coordinate_disk_radius(
        coefficient0,
        coefficient1,
        z0,
        z1,
        float(row["event_coordinate_error_estimate"]),
    )
    diagnostic_radius = abs(value) * relative_envelope + coordinate_radius
    return value, diagnostic_radius, coordinate_radius


def source_paths() -> list[Path]:
    return [
        Path(__file__).resolve(),
        SCRIPT_5342,
        Path(M5342.M5334.__file__).resolve(),
        Path(M5342.M5326.__file__).resolve(),
        EVENTS,
        CANDIDATES,
        SCAN,
        SUPPORT_COEFFICIENTS,
        M5342.M5326.CONTRACT_5325,
        M5342.M5326.POLES_5325,
    ]


def assert_sources() -> tuple[str, list[dict[str, Any]]]:
    paths = source_paths()
    missing = [path for path in paths if not path.is_file()]
    if missing:
        raise FileNotFoundError(missing)
    signature = selected_digest(paths[1:])
    rows = [
        tagged(
            {
                "source_path": str(path.resolve()),
                "sha256": digest(path),
                "exists": True,
                "source_signature": signature,
            }
        )
        for path in paths
    ]
    return signature, rows


def branch_preflight() -> dict[str, Any]:
    signature, sources = assert_sources()
    events = [row for row in read_csv(EVENTS) if row["event_type"] == "BRANCH_DEATH"]
    candidates = {
        row["candidate_id"]: row for row in read_csv(CANDIDATES)
    }
    scans = [
        row
        for row in read_csv(SCAN)
        if row["epsilon_id"] == EPSILON_ID and row["event_type"] == "BRANCH_DEATH"
    ]
    event_ids = sorted(row["event_id"] for row in events)
    scan_ids = sorted(row["event_id"] for row in scans)
    support_ids = sorted(row["event_id"] for row in read_csv(SUPPORT_COEFFICIENTS))
    checks = {
        "exactly_four_branch_events": event_ids == EXPECTED_EVENT_IDS,
        "scan_matches_branch_events": scan_ids == EXPECTED_EVENT_IDS,
        "all_branch_events_upper_contacts": all(row["contact_boundary"] == "UPPER" for row in scans),
        "all_branch_events_one_sided": all(row["normal_form_class"] == "ONE_SIDED_TRANSVERSE_SUPPORT_CONTACT" for row in scans),
        "all_opposite_sides_absent": all(parse_bool(row["opposite_side_branch_absence_witness"]) for row in scans),
        "all_event_contracts_pass": all(parse_bool(row["event_contract_passes"]) for row in events),
        "all_scan_contracts_pass": all(parse_bool(row["targeted_event_contract_passes"]) for row in scans),
        "every_branch_event_has_one_candidate_active_side": all(
            event["candidate_id"] in candidates
            and parse_bool(candidates[event["candidate_id"]]["left_inside_support"])
            != parse_bool(candidates[event["candidate_id"]]["right_inside_support"])
            for event in events
        ),
        "four_support_events_are_disjoint": support_ids == ["E01", "E02", "E03", "E08"],
        "source_signature_present": len(signature) == 64,
    }
    if not all(checks.values()):
        raise RuntimeError(f"branch preflight failed: {checks}")
    return {
        "checkpoint": CHECKPOINT,
        "marker": MARKER,
        "mode": "preflight",
        "checks": checks,
        "source_signature": signature,
        "source_count": len(sources),
        "event_ids": event_ids,
        "inside_directions": {
            event["event_id"]: (
                "x=x_event-d"
                if parse_bool(candidates[event["candidate_id"]]["left_inside_support"])
                else "x=x_event+d"
            )
            for event in events
        },
        "distance_multipliers": DISTANCE_MULTIPLIERS,
        **no_claims(),
    }


def polynomial_estimate(
    distances: list[float],
    values: list[complex],
    scale: float,
    indices: list[int],
) -> tuple[complex, complex]:
    normalized = np.asarray([distances[index] / scale for index in indices], dtype=float)
    design = np.column_stack([np.ones_like(normalized), normalized, normalized**2])
    selected = np.asarray([values[index] for index in indices], dtype=complex)
    coefficients = np.linalg.solve(design, selected)
    return complex(coefficients[0]), complex(coefficients[1] / scale)


def event_coefficient(
    event: dict[str, str],
    scan: dict[str, str],
    candidate: dict[str, str],
    contract: list[dict[str, str]],
    base_context: dict[str, Any],
    multiplier: float,
    signature: str,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    coordinate = float(event["event_coordinate"])
    coordinate_error = float(event["event_coordinate_error_estimate"])
    boundary_scale = float(scan["regulator_contact_width"])
    left_active = parse_bool(candidate["left_inside_support"])
    right_active = parse_bool(candidate["right_inside_support"])
    if left_active == right_active:
        raise RuntimeError(
            f"{event['event_id']} candidate does not select exactly one active side"
        )
    inside_direction = -1.0 if left_active else 1.0
    sampling_direction = (
        "x_event_minus_distance" if inside_direction < 0.0 else "x_event_plus_distance"
    )
    integration_coordinate = (
        "d=x_event-x" if inside_direction < 0.0 else "d=x-x_event"
    )
    scale = max(boundary_scale, 256.0 * coordinate_error)
    distances = [multiplier_value * scale for multiplier_value in DISTANCE_MULTIPLIERS]
    states: list[dict[str, Any]] = []
    for index, distance in enumerate(distances):
        state = M5342.endpoint_state(
            event,
            scan,
            coordinate + inside_direction * distance,
            contract,
            base_context,
            multiplier,
            f"IN{index + 1}",
        )
        state["inward_distance"] = distance
        state["inward_distance_over_boundary_scale"] = distance / boundary_scale
        state["source_signature"] = signature
        state["sampling_direction"] = sampling_direction
        state["candidate_left_inside_support"] = left_active
        state["candidate_right_inside_support"] = right_active
        states.append(tagged(state))

    gaps = [complex_from(row, "boundary_gap") for row in states]
    physical_coefficients = [
        complex_from(row, "physical_endpoint_coefficient") for row in states
    ]
    z0_inner, z1_inner = polynomial_estimate(distances, gaps, scale, [0, 1, 2])
    z0_outer, z1_outer = polynomial_estimate(distances, gaps, scale, [1, 2, 3])
    coefficient0_inner, coefficient1_inner = polynomial_estimate(
        distances,
        physical_coefficients,
        scale,
        [0, 1, 2],
    )
    coefficient0_outer, coefficient1_outer = polynomial_estimate(
        distances,
        physical_coefficients,
        scale,
        [1, 2, 3],
    )
    z_trace_change = relative_change(z0_inner, z0_outer)
    coefficient_trace_change = relative_change(
        coefficient0_inner,
        coefficient0_outer,
    )
    z_derivative_change = relative_change(z1_inner, z1_outer)
    coefficient_derivative_change = relative_change(
        coefficient1_inner,
        coefficient1_outer,
    )
    log_sign = -1 if scan["contact_boundary"] == "LOWER" else 1
    primitive_error = M5342.primitive_derivative_error(
        scale,
        log_sign,
        coefficient0_inner,
        coefficient1_inner,
        z0_inner,
        z1_inner,
    )
    gap_resolved = abs(z0_inner.imag) > 0.0 and abs(z0_inner) > (
        100.0 * coordinate_error * abs(z1_inner)
    )
    coefficient_contract = (
        parse_bool(event["event_contract_passes"])
        and parse_bool(scan["targeted_event_contract_passes"])
        and parse_bool(scan["opposite_side_branch_absence_witness"])
        and left_active != right_active
        and all(parse_bool(row["fit_contract_passes"]) for row in states)
        and len({row["support_id"] for row in states}) == 1
        and primitive_error <= PRIMITIVE_LIMIT
        and gap_resolved
    )
    a_estimator = z0_inner / EPSILON
    log_coefficient = -log_sign * coefficient0_inner * a_estimator / z1_inner
    outer_log_coefficient = (
        -log_sign * coefficient0_outer * (z0_outer / EPSILON) / z1_outer
    )
    stencil_disk_radius = abs(log_coefficient - outer_log_coefficient)
    coordinate_radius = coordinate_disk_radius(
        coefficient0_inner,
        coefficient1_inner,
        z0_inner,
        z1_inner,
        coordinate_error,
    )
    diagnostic_disk_radius = stencil_disk_radius + coordinate_radius
    diagnostic_relative_radius = diagnostic_disk_radius / max(
        abs(log_coefficient),
        abs(outer_log_coefficient),
        1.0e-300,
    )
    coefficient_contract = (
        coefficient_contract
        and log_sign == 1
        and finite_complex(log_coefficient)
        and finite_complex(outer_log_coefficient)
        and math.isfinite(diagnostic_disk_radius)
        and diagnostic_relative_radius <= A_EVENT_DIAGNOSTIC_RELATIVE_LIMIT
    )
    coefficient_row = tagged(
        {
            "event_id": event["event_id"],
            "event_type": event["event_type"],
            "x_panel_index": event["x_panel_index"],
            "term_id": event["term_id"],
            "primary_surface_id": event["primary_surface_id"],
            "contact_boundary": scan["contact_boundary"],
            "log_sign": log_sign,
            "event_coordinate": coordinate,
            "event_coordinate_error_estimate": coordinate_error,
            "boundary_layer_scale": boundary_scale,
            "one_sided_stencil_scale": scale,
            "candidate_left_inside_support": left_active,
            "candidate_right_inside_support": right_active,
            "inside_coordinate_direction_sign": int(inside_direction),
            "sampling_direction": sampling_direction,
            "source_signature": signature,
            **complex_fields("boundary_gap_z0", z0_inner),
            **complex_fields("boundary_gap_z0_outer_check", z0_outer),
            **complex_fields("boundary_gap_derivative_z1", z1_inner),
            **complex_fields("physical_coefficient_C0", coefficient0_inner),
            **complex_fields("physical_coefficient_C0_outer_check", coefficient0_outer),
            **complex_fields("physical_coefficient_derivative_C1", coefficient1_inner),
            **complex_fields("a_estimator", a_estimator),
            **complex_fields("A_event", log_coefficient),
            **complex_fields("A_event_outer_check", outer_log_coefficient),
            "A_event_stencil_disk_radius": stencil_disk_radius,
            "A_event_coordinate_disk_radius": coordinate_radius,
            "A_event_diagnostic_disk_radius": diagnostic_disk_radius,
            "A_event_diagnostic_relative_radius": diagnostic_relative_radius,
            "A_event_diagnostic_relative_limit": A_EVENT_DIAGNOSTIC_RELATIVE_LIMIT,
            "A_event_zero_outside_diagnostic_disk": abs(log_coefficient)
            > diagnostic_disk_radius,
            "boundary_gap_trace_relative_mismatch": z_trace_change,
            "physical_coefficient_trace_relative_mismatch": coefficient_trace_change,
            "boundary_gap_derivative_relative_change": z_derivative_change,
            "physical_coefficient_derivative_relative_change": coefficient_derivative_change,
            "primitive_derivative_relative_error": primitive_error,
            "endpoint_coordinate_sensitivity_absolute": abs(coefficient0_inner)
            * abs(z1_inner / z0_inner)
            * coordinate_error,
            "all_four_parent_fits_pass": all(
                parse_bool(row["fit_contract_passes"]) for row in states
            ),
            "support_id_is_stable": len({row["support_id"] for row in states}) == 1,
            "opposite_side_branch_absence_witness": scan[
                "opposite_side_branch_absence_witness"
            ],
            "one_sided_integration_coordinate": integration_coordinate,
            "parent_primitive_log_sign_derived_from_boundary": True,
            "endpoint_gap_is_regulator_resolved": gap_resolved,
            "coefficient_contract_passes": coefficient_contract,
        }
    )
    return states, coefficient_row


def run_extraction() -> dict[str, Any]:
    started = time.perf_counter()
    preflight = branch_preflight()
    signature, source_rows = assert_sources()
    OUT.mkdir(parents=True, exist_ok=True)
    atomic_csv(SOURCE_REGISTER, source_rows)
    atomic_json(
        STATUS,
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "state": "RUNNING",
            "completed_event_ids": [],
            "source_signature": signature,
        },
    )
    M5342.M5312.set_below_normal_priority()
    old = M5342.configure()
    try:
        events = {
            row["event_id"]: row
            for row in read_csv(EVENTS)
            if row["event_type"] == "BRANCH_DEATH"
        }
        scans = {
            row["event_id"]: row
            for row in read_csv(SCAN)
            if row["epsilon_id"] == EPSILON_ID
            and row["event_type"] == "BRANCH_DEATH"
        }
        candidates = {
            row["candidate_id"]: row for row in read_csv(CANDIDATES)
        }
        contract = read_csv(M5342.M5326.CONTRACT_5325)
        base_context = M5342.M5312.M5303.synthetic_context()
        multiplier = float(M5342.M5312.M5309.physical_multiplier())
        stencil_rows: list[dict[str, Any]] = []
        coefficient_rows: list[dict[str, Any]] = []
        completed: list[str] = []
        for event_id in EXPECTED_EVENT_IDS:
            event_stencil, coefficient = event_coefficient(
                events[event_id],
                scans[event_id],
                candidates[events[event_id]["candidate_id"]],
                contract,
                base_context,
                multiplier,
                signature,
            )
            stencil_rows.extend(event_stencil)
            coefficient_rows.append(coefficient)
            completed.append(event_id)
            atomic_csv(STENCIL, stencil_rows)
            atomic_csv(COEFFICIENTS, coefficient_rows)
            atomic_json(
                STATUS,
                {
                    "checkpoint": CHECKPOINT,
                    "marker": MARKER,
                    "state": "RUNNING",
                    "completed_event_ids": completed,
                    "source_signature": signature,
                },
            )
    finally:
        M5342.M5326.restore_kernel(old)

    support_rows = read_csv(SUPPORT_COEFFICIENTS)
    all_coefficients: list[tuple[str, complex, float]] = []
    all_event_rows: list[dict[str, Any]] = []
    for row in support_rows:
        value, diagnostic_radius, coordinate_radius = support_event_diagnostic(row)
        all_coefficients.append((row["event_id"], value, diagnostic_radius))
        all_event_rows.append(
            tagged(
                {
                    "event_id": row["event_id"],
                    "event_type": row["event_type"],
                    "contact_boundary": row["contact_boundary"],
                    "log_sign": int(row["log_sign"]),
                    "coefficient_source_class": "TWO_SIDED_SUPPORT_TRACE_5342",
                    **complex_fields("A_event", value),
                    "A_event_coordinate_disk_radius": coordinate_radius,
                    "A_event_diagnostic_disk_radius": diagnostic_radius,
                    "A_event_zero_outside_diagnostic_disk": abs(value)
                    > diagnostic_radius,
                    "coefficient_contract_passes": parse_bool(
                        row["coefficient_contract_passes"]
                    ),
                }
            )
        )
    for row in coefficient_rows:
        value = complex_from(row, "A_event")
        diagnostic_radius = float(row["A_event_diagnostic_disk_radius"])
        all_coefficients.append((row["event_id"], value, diagnostic_radius))
        all_event_rows.append(
            tagged(
                {
                    "event_id": row["event_id"],
                    "event_type": row["event_type"],
                    "contact_boundary": row["contact_boundary"],
                    "log_sign": int(row["log_sign"]),
                    "coefficient_source_class": "ONE_SIDED_BRANCH_TRACE_5346",
                    **complex_fields("A_event", value),
                    "A_event_coordinate_disk_radius": float(
                        row["A_event_coordinate_disk_radius"]
                    ),
                    "A_event_diagnostic_disk_radius": diagnostic_radius,
                    "A_event_zero_outside_diagnostic_disk": parse_bool(
                        row["A_event_zero_outside_diagnostic_disk"]
                    ),
                    "coefficient_contract_passes": parse_bool(
                        row["coefficient_contract_passes"]
                    ),
                }
            )
        )
    all_coefficients.sort(key=lambda item: item[0])
    all_event_rows.sort(key=lambda row: row["event_id"])
    total_coefficient = sum((value for _, value, _ in all_coefficients), 0.0j)
    sum_magnitudes = sum(abs(value) for _, value, _ in all_coefficients)
    total_diagnostic_disk_radius = sum(radius for _, _, radius in all_coefficients)
    all_contracts_pass = all(
        parse_bool(row["coefficient_contract_passes"])
        for row in [*support_rows, *coefficient_rows]
    )
    total_row = tagged(
        {
            "epsilon_id": EPSILON_ID,
            "epsilon": EPSILON,
            "event_ids": "|".join(event_id for event_id, _, _ in all_coefficients),
            "event_count": len(all_coefficients),
            **complex_fields("A_total_finite_epsilon_estimator", total_coefficient),
            "sum_event_magnitudes": sum_magnitudes,
            "A_total_diagnostic_disk_radius": total_diagnostic_disk_radius,
            "A_total_zero_outside_diagnostic_disk": abs(total_coefficient)
            > total_diagnostic_disk_radius,
            "coherent_sum_ratio": abs(total_coefficient)
            / max(sum_magnitudes, 1.0e-300),
            "all_one_sided_coefficient_contracts_pass": all_contracts_pass,
            "total_A_two_regulator_limit_complete": False,
            "role": "ALL_EIGHT_FINITE_EPSILON_ESTIMATOR_NOT_ZERO_LIMIT",
        }
    )
    atomic_csv(COEFFICIENTS, coefficient_rows)
    atomic_csv(ALL_EVENTS, all_event_rows)
    atomic_csv(TOTAL, [total_row])
    result = {
        "checkpoint": CHECKPOINT,
        "marker": MARKER,
        "checked_date": CHECKED_DATE,
        "decision": (
            "D4_E00125_ALL_EIGHT_ENDPOINT_COEFFICIENTS_COMPUTED__VALIDATION_PENDING"
            if all_contracts_pass
            else "D4_E00125_ONE_SIDED_COEFFICIENT_CONTRACT_BLOCKED"
        ),
        "preflight": preflight,
        "one_sided_event_count": len(coefficient_rows),
        "all_eight_event_count": len(all_coefficients),
        "all_one_sided_coefficient_contracts_pass": all_contracts_pass,
        "A_total_finite_epsilon_estimator_real": total_coefficient.real,
        "A_total_finite_epsilon_estimator_imaginary": total_coefficient.imag,
        "A_total_finite_epsilon_estimator_magnitude": abs(total_coefficient),
        "A_total_diagnostic_disk_radius": total_diagnostic_disk_radius,
        "A_total_zero_outside_diagnostic_disk": abs(total_coefficient)
        > total_diagnostic_disk_radius,
        "total_A_two_regulator_limit_complete": False,
        "runtime_seconds": time.perf_counter() - started,
        "source_signature": signature,
        **no_claims(),
    }
    result["valid_for_D4_E00125_all_eight_endpoint_coefficients"] = False
    atomic_json(RESULT, result)
    atomic_json(
        STATUS,
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "state": "PENDING_VALIDATION" if all_contracts_pass else "BLOCKED",
            "completed_event_ids": EXPECTED_EVENT_IDS,
            "source_signature": signature,
            "decision": result["decision"],
        },
    )
    return result


def validation_rows(result: dict[str, Any]) -> list[dict[str, Any]]:
    coefficients = read_csv(COEFFICIENTS)
    all_events = read_csv(ALL_EVENTS)
    totals = read_csv(TOTAL)
    rows: list[dict[str, Any]] = []

    def add(gate: str, passed: bool, detail: Any) -> None:
        rows.append(
            {
                "checkpoint": CHECKPOINT,
                "marker": MARKER,
                "gate": gate,
                "passed": bool(passed),
                "detail": json.dumps(detail, sort_keys=True)
                if isinstance(detail, (dict, list))
                else str(detail),
            }
        )

    add("preflight_all_pass", all(result["preflight"]["checks"].values()), result["preflight"])
    add("four_one_sided_coefficients_present", len(coefficients) == 4, len(coefficients))
    add("event_ids_exact", [row["event_id"] for row in coefficients] == EXPECTED_EVENT_IDS, [row["event_id"] for row in coefficients])
    add("all_parent_fits_pass", all(parse_bool(row["all_four_parent_fits_pass"]) for row in coefficients), coefficients)
    add("all_coefficient_contracts_pass", all(parse_bool(row["coefficient_contract_passes"]) for row in coefficients), coefficients)
    add("all_endpoint_gaps_resolved", all(parse_bool(row["endpoint_gap_is_regulator_resolved"]) for row in coefficients), coefficients)
    add("all_primitive_checks_pass", all(float(row["primitive_derivative_relative_error"]) <= PRIMITIVE_LIMIT for row in coefficients), coefficients)
    add("upper_boundary_log_signs_derived", all(row["contact_boundary"] == "UPPER" and int(row["log_sign"]) == 1 and parse_bool(row["parent_primitive_log_sign_derived_from_boundary"]) for row in coefficients), coefficients)
    add("all_event_ledger_complete", len(all_events) == 8 and [row["event_id"] for row in all_events] == [f"E{index:02d}" for index in range(1, 9)], [row.get("event_id") for row in all_events])
    add("all_diagnostic_disks_finite", all(math.isfinite(float(row["A_event_diagnostic_disk_radius"])) and float(row["A_event_diagnostic_disk_radius"]) >= 0.0 for row in all_events), all_events)
    add("total_row_present", len(totals) == 1 and int(totals[0]["event_count"]) == 8, totals)
    add("finite_epsilon_total_is_numeric", len(totals) == 1 and all(math.isfinite(float(totals[0][key])) for key in ["A_total_finite_epsilon_estimator_real", "A_total_finite_epsilon_estimator_imaginary", "A_total_finite_epsilon_estimator_magnitude"]), totals)
    add("total_diagnostic_disk_is_finite", len(totals) == 1 and math.isfinite(float(totals[0]["A_total_diagnostic_disk_radius"])) and float(totals[0]["A_total_diagnostic_disk_radius"]) >= 0.0, totals)
    add("two_regulator_total_limit_stays_false", result["total_A_two_regulator_limit_complete"] is False, result["total_A_two_regulator_limit_complete"])
    add("broad_claims_false", all(not result[key] for key in ["valid_for_D4_outer_E00125_fixed_decay_integral", "valid_for_D4_outer_regulator_zero_limit", "valid_for_local_GR_claim", "valid_for_full_MTS_claim"]), no_claims())
    add("source_signature_current", result["source_signature"] == selected_digest(source_paths()[1:]), result["source_signature"])
    add("no_script_pycache", not (POST / "scripts" / "__pycache__").exists(), str(POST / "scripts" / "__pycache__"))
    return rows


def finalize_claim_state(result: dict[str, Any], passed: bool) -> dict[str, Any]:
    claim = "valid_for_D4_E00125_all_eight_endpoint_coefficients"
    coefficients = read_csv(COEFFICIENTS)
    all_events = read_csv(ALL_EVENTS)
    totals = read_csv(TOTAL)
    for row in coefficients:
        row[claim] = passed
    for row in all_events:
        row[claim] = passed
    for row in totals:
        row[claim] = passed
    atomic_csv(COEFFICIENTS, coefficients)
    atomic_csv(ALL_EVENTS, all_events)
    atomic_csv(TOTAL, totals)
    result["validation_passed"] = passed
    result[claim] = passed
    result["decision"] = (
        "D4_E00125_ALL_EIGHT_ENDPOINT_COEFFICIENTS_PASS__REPEAT_AT_SECOND_REGULATOR"
        if passed
        else "D4_E00125_ONE_SIDED_COEFFICIENT_VALIDATION_BLOCKED"
    )
    atomic_json(RESULT, result)
    atomic_json(
        STATUS,
        {
            "checkpoint": CHECKPOINT,
            "marker": MARKER,
            "state": "COMPLETE" if passed else "BLOCKED",
            "completed_event_ids": EXPECTED_EVENT_IDS,
            "source_signature": result["source_signature"],
            "decision": result["decision"],
            "validation_passed": passed,
        },
    )
    return result


def validate_saved() -> int:
    if not RESULT.is_file():
        raise FileNotFoundError(RESULT)
    result = json.loads(RESULT.read_text(encoding="utf-8"))
    rows = validation_rows(result)
    passed = all(row["passed"] for row in rows)
    atomic_csv(VALIDATION, rows)
    finalize_claim_state(result, passed)
    print(json.dumps({"mode": "validate-saved", "checks": rows}, indent=2))
    return 0 if passed else 1


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--validate-saved", action="store_true")
    args = parser.parse_args()
    if args.dry_run and args.validate_saved:
        parser.error("choose at most one mode")
    if args.dry_run:
        preflight = branch_preflight()
        print(json.dumps(preflight, indent=2))
        return 0
    if args.validate_saved:
        return validate_saved()
    result = run_extraction()
    rows = validation_rows(result)
    passed = all(row["passed"] for row in rows)
    atomic_csv(VALIDATION, rows)
    result = finalize_claim_state(result, passed)
    print(json.dumps({"mode": "run", "result": result, "checks": rows}, indent=2))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
