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

SCRIPT_5337 = (
    SCRIPTS / "Y5_R2FR_5337_D4_regulator_fold_double_scaling_and_contrast_gate.py"
)
SCRIPT_5358 = (
    SCRIPTS
    / "Y5_R2FR_5358_D4_zero_regulator_analytic_collision_and_event_continuation.py"
)
BASE_EVENTS = (
    FUNCTIONAL_RG / "5364" / "E000625" / "D4_E000625_preintegration_frozen_events.csv"
)
BASE_CANDIDATES = (
    FUNCTIONAL_RG / "5334" / "E0025" / "D4_outer_support_event_candidates.csv"
)
BASE_CONTRACT = (
    FUNCTIONAL_RG / "5334" / "E0025" / "D4_outer_reduced_MC04_cubature_contract.csv"
)
SCANNER_SOURCE_EVENTS = (
    FUNCTIONAL_RG / "5334" / "E0025" / "D4_outer_refined_support_events.csv"
)
ZERO_EVENTS = FUNCTIONAL_RG / "5358" / "D4_zero_regulator_event_certificate.csv"
ZERO_RESULT = FUNCTIONAL_RG / "5358" / "D4_zero_regulator_continuation_result.json"
ZERO_VALIDATION = FUNCTIONAL_RG / "5358" / "D4_zero_regulator_continuation_validation.csv"
FREEZE_RESULT = FUNCTIONAL_RG / "5365" / "D4_E0003125_premeasurement_freeze_result.json"
FREEZE_VALIDATION = (
    FUNCTIONAL_RG / "5365" / "D4_E0003125_premeasurement_freeze_validation.csv"
)
FIVE_RUNG_RESULT = FUNCTIONAL_RG / "5366" / "D4_five_rung_intercept_envelope_result.json"
FIVE_RUNG_VALIDATION = (
    FUNCTIONAL_RG / "5366" / "D4_five_rung_intercept_envelope_validation.csv"
)

OUTPUT = FUNCTIONAL_RG / "5367" / "E0003125"
CACHE = OUTPUT / "event-scan-cache"
SCAN_STATUS = OUTPUT / "event_scan_status.json"
SCAN = OUTPUT / "D4_E0003125_targeted_event_scan.csv"
EVENTS = OUTPUT / "D4_E0003125_refined_events.csv"
AUDIT = OUTPUT / "D4_E0003125_event_geometry_audit.csv"
ANALYTIC_AUDIT = OUTPUT / "D4_E0003125_finite_analytic_event_audit.csv"
ABSENCE_AUDIT = OUTPUT / "D4_E0003125_branch_death_absence_adapter_audit.csv"
RESULT = OUTPUT / "D4_E0003125_event_geometry_result.json"
VALIDATION = OUTPUT / "D4_E0003125_event_geometry_validation.csv"
SOURCE_REGISTER = OUTPUT / "source_register.csv"
STATUS = OUTPUT / "status.json"
RESIDUAL_VALIDATION = RESIDUALS / "P8_Y5_BRR545_5367_VALIDATION.csv"
DOCUMENT = POST / "5367-Y5-R2FR-D4-E0003125-source-complete-event-geometry.md"

CHECKPOINT = 5367
MARKER = "MTS_5367_D4_E0003125_SOURCE_COMPLETE_EVENT_GEOMETRY"
REVISION = "D4-E0003125-source-complete-event-geometry-v1"
CHECKED_DATE = "2026-08-13"
EPSILON_ID = "E0003125"
EPSILON = 0.0003125
EXPECTED_EVENT_COUNT = 8
EVENT_ROOT_WIDTH = 2.0e-11
EVENT_COORDINATE_ERROR = 1.0e-11
FORMAL_DIGEST = "0ec1bc6012136ffc6b28a1512aca6ce712b6decd2ff793310a9bd61775f3db1f"

GEOMETRY_CLAIM = "valid_for_D4_outer_E0003125_event_geometry"
FALSE_CLAIMS = (
    "valid_for_D4_outer_E0003125_fixed_decay_integral",
    "valid_for_D4_E0003125_complete_family_holdout_compatibility",
    "valid_for_D4_numeric_uniform_remainder_bound",
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


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def set_below_normal_priority() -> None:
    if os.name != "nt":
        return
    import ctypes

    ctypes.windll.kernel32.SetPriorityClass(
        ctypes.windll.kernel32.GetCurrentProcess(), 0x00004000
    )


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def serialized_hash(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(value, sort_keys=True, separators=(",", ":")).encode("utf-8")
    ).hexdigest()


def formal_inventory_digest() -> str:
    rows = [
        {
            "relative_path": str(path.relative_to(FORMAL)),
            "size": str(path.stat().st_size),
            "sha256": digest(path),
        }
        for path in sorted(
            (item for item in FORMAL.rglob("*") if item.is_file()),
            key=lambda item: str(item).lower(),
        )
    ]
    return serialized_hash(rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", newline="", encoding="utf-8-sig") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8-sig"))


def parse_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() == "true"


def csv_validation_passes(path: Path) -> bool:
    rows = read_csv(path)
    return bool(rows) and all(parse_bool(row["passed"]) for row in rows)


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


def no_broad_claims() -> dict[str, bool]:
    return {field: False for field in FALSE_CLAIMS}


def install_preregistered_branch_death_adapter(
    scanner: Any, records: list[dict[str, Any]]
) -> None:
    source_events = read_csv(SCANNER_SOURCE_EVENTS)
    death_windows = [
        {
            "event_id": row["event_id"],
            "term_id": row["term_id"],
            "left": float(row["source_bracket_left"]),
            "right": float(row["source_bracket_right"]),
        }
        for row in source_events
        if row["event_type"] == "BRANCH_DEATH"
    ]
    original_loader = scanner.load_module

    def load_with_absence_semantics(name: str, path: Path) -> Any:
        parent = original_loader(name, path)
        if name != "mts_5334_for_5337":
            return parent
        original_scan = parent.M5312.scan_term_poles

        def scan_term_poles(
            node: dict[str, Any], term_id: str, supports: list[dict[str, Any]]
        ) -> list[dict[str, Any]]:
            try:
                return original_scan(node, term_id, supports)
            except RuntimeError as error:
                if str(error) not in {
                    "homotopy collision branch disappeared",
                    "component collision root disappeared",
                }:
                    raise
                coordinate = float(node["absolute_soft_cosine"])
                matched = [
                    window
                    for window in death_windows
                    if window["term_id"] == term_id
                    and window["left"] <= coordinate <= window["right"]
                ]
                if not matched:
                    raise
                records.append(
                    {
                        "epsilon_id": EPSILON_ID,
                        "epsilon": EPSILON,
                        "node_id": node["node_id"],
                        "x_panel_index": node["x_panel_index"],
                        "term_id": term_id,
                        "absolute_soft_cosine": coordinate,
                        "matched_preregistered_death_event_ids": "|".join(
                            row["event_id"] for row in matched
                        ),
                        "parent_exception": str(error),
                        "semantic_resolution": (
                            "BRANCH_ABSENT_INSIDE_PREREGISTERED_BRANCH_DEATH_WINDOW"
                        ),
                        **no_broad_claims(),
                    }
                )
                return []

        parent.M5312.scan_term_poles = scan_term_poles
        return parent

    scanner.load_module = load_with_absence_semantics


def accepted_measurement_paths() -> list[str]:
    target = FUNCTIONAL_RG / "5334" / EPSILON_ID
    paths: list[str] = []
    for path in target.glob("*finite_value.csv"):
        if any(
            parse_bool(row.get("finite_regulator_fixed_decay_integral_accepted", False))
            for row in read_csv(path)
        ):
            paths.append(str(path.resolve()))
    return paths


def preflight() -> dict[str, Any]:
    required = (
        Path(__file__).resolve(),
        SCRIPT_5337,
        SCRIPT_5358,
        BASE_EVENTS,
        BASE_CANDIDATES,
        BASE_CONTRACT,
        ZERO_EVENTS,
        ZERO_RESULT,
        ZERO_VALIDATION,
        FREEZE_RESULT,
        FREEZE_VALIDATION,
        FIVE_RUNG_RESULT,
        FIVE_RUNG_VALIDATION,
    )
    missing = [str(path) for path in required if not path.is_file()]
    if missing:
        return {"mode": "dry-run", "all_pass": False, "missing": missing}
    zero = read_json(ZERO_RESULT)
    freeze = read_json(FREEZE_RESULT)
    five = read_json(FIVE_RUNG_RESULT)
    measurements = accepted_measurement_paths()
    checks = {
        "zero_regulator_eight_event_continuation_passes": zero.get(
            "validation_passed"
        )
        is True
        and zero.get("claim_boundary", {}).get(
            "valid_for_D4_zero_regulator_eight_event_geometry"
        )
        is True
        and csv_validation_passes(ZERO_VALIDATION),
        "E0003125_prediction_was_frozen_before_E000625_completion": freeze.get(
            "validation_passed"
        )
        is True
        and freeze.get("decision")
        == "D4_E0003125_COMPLETE_FAMILY_HOLDOUT_FROZEN_BEFORE_E000625_RESULT"
        and csv_validation_passes(FREEZE_VALIDATION),
        "five_rung_numeric_intercept_gate_passes": five.get("validation_passed")
        is True
        and five.get("numerical_intercept_gate_passes") is True
        and five.get("claim_boundary", {}).get(
            "valid_for_D4_outer_regulator_zero_limit"
        )
        is False
        and csv_validation_passes(FIVE_RUNG_VALIDATION),
        "E0003125_measurement_absent_before_geometry": not measurements,
        "eight_source_events_and_candidates_present": len(read_csv(BASE_EVENTS))
        == len(read_csv(BASE_CANDIDATES))
        == EXPECTED_EVENT_COUNT,
        "formal_workbench_unchanged": formal_inventory_digest() == FORMAL_DIGEST,
        "scripts_cache_absent": not (SCRIPTS / "__pycache__").exists(),
    }
    return {
        "mode": "dry-run",
        "all_pass": all(checks.values()),
        "checks": checks,
        "accepted_measurement_paths": measurements,
    }


def finite_analytic_events() -> list[dict[str, Any]]:
    module = load_module("mts_5358_for_5367", SCRIPT_5358)
    mp = module.mp
    mp.mp.dps = max(mp.mp.dps, 80)
    decay_absolute = mp.mpf(str(module.d4_decay_absolute()))
    zero_by_id = {row["event_id"]: row for row in read_csv(ZERO_EVENTS)}

    def solve(source: dict[str, str], epsilon: Any) -> dict[str, Any]:
        event_id = source["event_id"]
        event_type = source["event_type"]
        surface_id = source["primary_surface_id"]
        sign, decay_sign = module.term_signs(source["term_id"])
        if sign != decay_sign:
            raise RuntimeError(f"unequal D4 signs for {event_id}")
        target = mp.mpc(str(module.SCATTERING_TARGET_REAL), epsilon)
        q_value = (1 - target) / (1 + target)
        zero_coordinate = mp.mpf(
            zero_by_id[event_id]["zero_regulator_absolute_soft_cosine"]
        )

        def material_root(coordinate: Any) -> Any:
            soft_cosine = sign * coordinate
            decay_cosine = sign * decay_absolute
            coefficient_a, coefficient_b, coefficient_c = module.material_coefficients(
                surface_id, soft_cosine, decay_cosine, q_value
            )
            if abs(coefficient_a) <= mp.mpf("1e-60"):
                candidates = [-coefficient_c / coefficient_b]
            else:
                discriminant = coefficient_b**2 - 4 * coefficient_a * coefficient_c
                square_root = mp.sqrt(discriminant)
                candidates = [
                    (-coefficient_b - square_root) / (2 * coefficient_a),
                    (-coefficient_b + square_root) / (2 * coefficient_a),
                ]
            zero_root = module.physical_material_root(
                surface_id, coordinate, sign, decay_absolute
            )
            return min(candidates, key=lambda value: abs(value - zero_root))

        def boundary_energy(coordinate: Any) -> Any:
            if event_type == "BRANCH_DEATH":
                return mp.mpf(str(source["event_support_upper"]))
            roots = module.hard_boundary_roots(
                sign * coordinate, sign * decay_absolute
            )
            return 1 - roots[-1] ** 2

        def scalar(coordinate: Any) -> Any:
            recoil = material_root(coordinate)
            return mp.re(1 - recoil**2) - boundary_energy(coordinate)

        bracket = module.bracket_and_bisect(scalar, zero_coordinate)
        coordinate = bracket["root"]
        recoil = material_root(coordinate)
        pole = 1 - recoil**2
        boundary = boundary_energy(coordinate)
        polynomial_residual = abs(
            module.material_polynomial(
                surface_id,
                recoil,
                sign * coordinate,
                sign * decay_absolute,
                q_value,
            )
        )
        return {
            "coordinate": coordinate,
            "bracket_lower": bracket["lower"],
            "bracket_upper": bracket["upper"],
            "bracket_width": bracket["upper"] - bracket["lower"],
            "iterations": bracket["iterations"],
            "pole": pole,
            "boundary_energy": boundary,
            "event_residual": abs(scalar(coordinate)),
            "material_polynomial_residual": polynomial_residual,
            "event_derivative": mp.diff(scalar, coordinate),
            "q_value": q_value,
            "zero_coordinate": zero_coordinate,
        }

    rows: list[dict[str, Any]] = []
    for source in read_csv(BASE_EVENTS):
        half = solve(source, mp.mpf(str(EPSILON)))
        full = solve(source, mp.mpf(str(2 * EPSILON)))
        half_shift = half["coordinate"] - half["zero_coordinate"]
        full_shift = full["coordinate"] - full["zero_coordinate"]
        ratio = half_shift / full_shift
        contract_passes = (
            half["event_residual"] <= mp.mpf("1e-40")
            and half["material_polynomial_residual"] <= mp.mpf("1e-40")
            and half["bracket_width"] <= mp.mpf("1e-45")
            and abs(half["event_derivative"]) >= mp.mpf("1e-3")
            and 0 < ratio < 1
            and abs(ratio - mp.mpf("0.25")) <= mp.mpf("1e-6")
        )
        rows.append(
            {
                "epsilon_id": EPSILON_ID,
                "epsilon": EPSILON,
                "event_id": source["event_id"],
                "event_type": source["event_type"],
                "term_id": source["term_id"],
                "primary_surface_id": source["primary_surface_id"],
                "analytic_event_coordinate": module.mp_text(half["coordinate"]),
                "analytic_coordinate_bracket_lower": module.mp_text(
                    half["bracket_lower"]
                ),
                "analytic_coordinate_bracket_upper": module.mp_text(
                    half["bracket_upper"]
                ),
                "analytic_coordinate_bracket_width": module.mp_text(
                    half["bracket_width"]
                ),
                "analytic_pole_real": module.mp_text(mp.re(half["pole"])),
                "analytic_pole_imaginary": module.mp_text(mp.im(half["pole"])),
                "analytic_support_boundary_energy": module.mp_text(
                    half["boundary_energy"]
                ),
                "analytic_event_residual": module.mp_text(half["event_residual"]),
                "analytic_material_polynomial_residual": module.mp_text(
                    half["material_polynomial_residual"]
                ),
                "analytic_event_derivative": module.mp_text(
                    half["event_derivative"]
                ),
                "analytic_q_real": module.mp_text(mp.re(half["q_value"])),
                "analytic_q_imaginary": module.mp_text(mp.im(half["q_value"])),
                "zero_regulator_event_coordinate": module.mp_text(
                    half["zero_coordinate"]
                ),
                "analytic_E000625_event_coordinate": module.mp_text(
                    full["coordinate"]
                ),
                "E0003125_shift_from_zero": module.mp_text(half_shift),
                "analytic_E000625_shift_from_zero": module.mp_text(full_shift),
                "half_step_shift_ratio": module.mp_text(ratio),
                "analytic_root_iteration_count": half["iterations"],
                "analytic_finite_event_contract_passes": contract_passes,
                **no_broad_claims(),
            }
        )
    return rows


def build_events(
    scans: list[dict[str, Any]], analytic_rows: list[dict[str, Any]]
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    scan_by_id = {row["event_id"]: row for row in scans}
    analytic_by_id = {row["event_id"]: row for row in analytic_rows}
    events: list[dict[str, Any]] = []
    audit: list[dict[str, Any]] = []
    for source in read_csv(BASE_EVENTS):
        scanned = scan_by_id[source["event_id"]]
        analytic = analytic_by_id[source["event_id"]]
        coordinate = float(analytic["analytic_event_coordinate"])
        event_type = scanned["event_type"]
        contact_residual = float(analytic["analytic_event_residual"])
        pole_real = float(analytic["analytic_pole_real"])
        boundary_energy = float(analytic["analytic_support_boundary_energy"])
        support_lower = float(source["event_support_lower"])
        support_upper = float(source["event_support_upper"])
        if scanned["contact_boundary"] == "LOWER":
            support_lower = boundary_energy
        else:
            support_upper = boundary_energy
        near_slope = float(scanned["near_transverse_slope_magnitude"])
        scanner_coordinate_error = max(
            EVENT_COORDINATE_ERROR,
            float(scanned["contact_residual"]) / max(near_slope, 1.0e-300),
        )
        scanner_coordinate_difference = abs(
            coordinate - float(scanned["event_coordinate"])
        )
        scanner_consistent = scanner_coordinate_difference <= scanner_coordinate_error
        source_slope_text = source.get("source_crossing_slope", "")
        source_slope = float(source_slope_text) if source_slope_text else 1.0
        signed_slope: float | str = ""
        if event_type != "BRANCH_DEATH":
            signed_slope = math.copysign(
                float(scanned["near_transverse_slope_magnitude"]), source_slope
            )
        event = dict(source)
        event.update(
            {
                "source_bracket_left": coordinate - EVENT_COORDINATE_ERROR,
                "source_bracket_right": coordinate + EVENT_COORDINATE_ERROR,
                "event_coordinate": coordinate,
                "event_pole_real": pole_real,
                "event_pole_imaginary": float(analytic["analytic_pole_imaginary"]),
                "event_support_lower": support_lower,
                "event_support_upper": support_upper,
                "event_signed_support_margin": (
                    contact_residual if event_type == "BRANCH_DEATH" else 0.0
                ),
                "source_crossing_slope": signed_slope,
                "event_coordinate_error_estimate": EVENT_COORDINATE_ERROR,
                "iteration_count": int(analytic["analytic_root_iteration_count"]),
                "event_contract_passes": parse_bool(
                    scanned["targeted_event_contract_passes"]
                )
                and parse_bool(analytic["analytic_finite_event_contract_passes"])
                and scanner_consistent,
                "candidate_source": "CHECKPOINT_5367_FINITE_ANALYTIC_EVENT_EQUATION_WITH_PARENT_SCAN_CROSS_CHECK",
                "coordinate_refinement_method": "FINITE_Q_MATERIAL_POLYNOMIAL_AND_SUPPORT_BOUNDARY_BISECTION",
                "coordinate_refinement_root_width_bound": analytic[
                    "analytic_coordinate_bracket_width"
                ],
                "coordinate_refinement_source_scan_sha256": "SET_AFTER_SCAN_WRITE",
                GEOMETRY_CLAIM: True,
                **no_broad_claims(),
            }
        )
        events.append(event)
        audit.append(
            {
                "epsilon_id": EPSILON_ID,
                "epsilon": EPSILON,
                "event_id": event["event_id"],
                "event_type": event_type,
                "event_coordinate": coordinate,
                "coordinate_error_bound": EVENT_COORDINATE_ERROR,
                "analytic_coordinate_bracket_width": analytic[
                    "analytic_coordinate_bracket_width"
                ],
                "analytic_event_residual": analytic["analytic_event_residual"],
                "analytic_material_polynomial_residual": analytic[
                    "analytic_material_polynomial_residual"
                ],
                "analytic_event_derivative": analytic["analytic_event_derivative"],
                "half_step_shift_ratio": analytic["half_step_shift_ratio"],
                "parent_scanner_event_coordinate": scanned["event_coordinate"],
                "parent_scanner_coordinate_difference": scanner_coordinate_difference,
                "parent_scanner_residual_implied_coordinate_error": scanner_coordinate_error,
                "parent_scanner_coordinate_consistent": scanner_consistent,
                "root_iteration_count": int(analytic["analytic_root_iteration_count"]),
                "contact_residual": contact_residual,
                "near_transverse_slope_magnitude": near_slope,
                "slope_window_relative_change": float(
                    scanned["slope_window_relative_change"]
                ),
                "normal_form_class": scanned["normal_form_class"],
                "opposite_side_branch_absence_witness": parse_bool(
                    scanned["opposite_side_branch_absence_witness"]
                ),
                "targeted_event_contract_passes": parse_bool(
                    scanned["targeted_event_contract_passes"]
                )
                and parse_bool(analytic["analytic_finite_event_contract_passes"])
                and scanner_consistent,
                GEOMETRY_CLAIM: True,
                **no_broad_claims(),
            }
        )
    return events, audit


def run_geometry() -> dict[str, Any]:
    started = time.perf_counter()
    state = preflight()
    if not state["all_pass"]:
        raise RuntimeError(f"preflight failed: {state}")
    OUTPUT.mkdir(parents=True, exist_ok=True)
    module = load_module("mts_5337_for_5367", SCRIPT_5337)
    module.EPSILON_VALUES = {EPSILON_ID: EPSILON}
    module.RUNG_CACHE = CACHE
    module.SCAN_STATUS = SCAN_STATUS
    absence_records: list[dict[str, Any]] = []
    install_preregistered_branch_death_adapter(module, absence_records)
    scans, summaries, scan_checks = module.d4_targeted_event_scan()
    if not absence_records and ABSENCE_AUDIT.is_file():
        absence_records = read_csv(ABSENCE_AUDIT)
    atomic_csv(SCAN, scans)
    analytic_rows = finite_analytic_events()
    events, audit = build_events(scans, analytic_rows)
    atomic_csv(ANALYTIC_AUDIT, analytic_rows)
    scan_hash = digest(SCAN)
    for event in events:
        event["coordinate_refinement_source_scan_sha256"] = scan_hash
        event["transfer_source_path"] = str(SCAN.resolve())
        event["transfer_source_sha256"] = scan_hash
    atomic_csv(EVENTS, events)
    atomic_csv(AUDIT, audit)

    analytic_by_id = {row["event_id"]: row for row in analytic_rows}
    maximum_relative_continuation_distance = max(
        abs(float(row["half_step_shift_ratio"]))
        for row in analytic_rows
    )
    maximum_quadratic_ratio_deviation = max(
        abs(float(row["half_step_shift_ratio"]) - 0.25)
        for row in analytic_rows
    )
    maximum_scanner_normalized_coordinate_difference = max(
        float(row["parent_scanner_coordinate_difference"])
        / max(
            float(row["parent_scanner_residual_implied_coordinate_error"]),
            1.0e-300,
        )
        for row in audit
    )
    maximum_analytic_residual = max(
        max(
            float(row["analytic_event_residual"]),
            float(row["analytic_material_polynomial_residual"]),
        )
        for row in analytic_rows
    )
    analytic_contracts_pass = all(
        parse_bool(row["analytic_finite_event_contract_passes"])
        for row in analytic_rows
    )
    analytic_half_step_is_between = all(
        0.0 < float(analytic_by_id[event["event_id"]]["half_step_shift_ratio"]) < 1.0
        for event in events
    )
    topology = [event["event_type"] for event in events]
    order = "|".join(
        event["event_id"]
        for event in sorted(events, key=lambda row: float(row["event_coordinate"]))
    )
    validations = [
        validation_row("preflight_passes", True, state["checks"]),
        validation_row(
            "targeted_scan_returns_exactly_eight_events",
            len(scans) == len(events) == len(audit) == EXPECTED_EVENT_COUNT
            and [event["event_id"] for event in events]
            == [f"E{index:02d}" for index in range(1, 9)],
            len(events),
        ),
        validation_row(
            "all_targeted_parent_kernel_event_contracts_pass",
            all(parse_bool(row["targeted_event_contract_passes"]) for row in scans)
            and all(parse_bool(row["event_contract_passes"]) for row in events),
            scan_checks,
        ),
        validation_row(
            "finite_q_analytic_event_equations_pass",
            analytic_contracts_pass and maximum_analytic_residual <= 1.0e-40,
            {
                "maximum_residual": maximum_analytic_residual,
                "maximum_half_step_ratio_deviation_from_one_quarter": maximum_quadratic_ratio_deviation,
            },
        ),
        validation_row(
            "analytic_events_agree_with_parent_scanner_within_residual_implied_error",
            all(parse_bool(row["parent_scanner_coordinate_consistent"]) for row in audit),
            maximum_scanner_normalized_coordinate_difference,
        ),
        validation_row(
            "homotopy_absence_is_confined_to_preregistered_branch_death_windows",
            all(
                row["semantic_resolution"]
                == "BRANCH_ABSENT_INSIDE_PREREGISTERED_BRANCH_DEATH_WINDOW"
                and bool(row["matched_preregistered_death_event_ids"])
                for row in absence_records
            ),
            {
                "count": len(absence_records),
                "event_ids": sorted(
                    {
                        event_id
                        for row in absence_records
                        for event_id in str(
                            row["matched_preregistered_death_event_ids"]
                        ).split("|")
                    }
                ),
            },
        ),
        validation_row(
            "event_topology_is_three_entries_four_deaths_one_exit",
            topology.count("SUPPORT_ENTRY") == 3
            and topology.count("BRANCH_DEATH") == 4
            and topology.count("SUPPORT_EXIT") == 1,
            topology,
        ),
        validation_row(
            "event_order_matches_zero_and_positive_regulator_continuation",
            order == "E01|E02|E03|E05|E04|E06|E07|E08",
            order,
        ),
        validation_row(
            "E0003125_events_lie_between_zero_and_analytic_E000625_continuations",
            analytic_half_step_is_between
            and maximum_relative_continuation_distance <= 1.0 + 1.0e-12
            and maximum_quadratic_ratio_deviation <= 1.0e-6,
            {
                "maximum_continuation_distance": maximum_relative_continuation_distance,
                "maximum_quadratic_ratio_deviation": maximum_quadratic_ratio_deviation,
            },
        ),
        validation_row(
            "all_broad_claims_remain_false",
            all(value is False for value in no_broad_claims().values()),
            no_broad_claims(),
        ),
        validation_row(
            "formal_workbench_unchanged",
            formal_inventory_digest() == FORMAL_DIGEST,
            formal_inventory_digest(),
        ),
        validation_row(
            "scripts_cache_absent",
            not (SCRIPTS / "__pycache__").exists(),
            SCRIPTS / "__pycache__",
        ),
    ]
    passed = all(parse_bool(row["passed"]) for row in validations)
    claims = {GEOMETRY_CLAIM: passed, **no_broad_claims()}
    for row in events:
        row.update(claims)
    for row in audit:
        row.update(claims)
    for row in absence_records:
        row.update(claims)
    atomic_csv(EVENTS, events)
    atomic_csv(AUDIT, audit)
    atomic_csv(ABSENCE_AUDIT, absence_records)
    direct_sources = (
        Path(__file__).resolve(),
        SCRIPT_5337,
        SCRIPT_5358,
        BASE_EVENTS,
        BASE_CANDIDATES,
        BASE_CONTRACT,
        SCANNER_SOURCE_EVENTS,
        ZERO_EVENTS,
        ZERO_RESULT,
        ZERO_VALIDATION,
        FREEZE_RESULT,
        FREEZE_VALIDATION,
        FIVE_RUNG_RESULT,
        FIVE_RUNG_VALIDATION,
        SCAN,
        ANALYTIC_AUDIT,
        ABSENCE_AUDIT,
    )
    source_rows = [
        {
            "path": str(path.resolve()),
            "sha256": digest(path),
            "exists": path.is_file(),
            **claims,
        }
        for path in direct_sources
    ]
    result = {
        "mode": "D4-E0003125-source-complete-event-geometry",
        "checkpoint": CHECKPOINT,
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "checked_date": CHECKED_DATE,
        "epsilon_id": EPSILON_ID,
        "epsilon": EPSILON,
        "validation_passed": passed,
        "decision": (
            "D4_E0003125_EVENT_GEOMETRY_SOURCE_COMPLETE__BUILD_BLIND_HOLDOUT_RUNNER"
            if passed
            else "D4_E0003125_EVENT_GEOMETRY_BLOCKED"
        ),
        "event_count": len(events),
        "event_order_signature": order,
        "maximum_relative_zero_to_E000625_continuation_distance": maximum_relative_continuation_distance,
        "maximum_half_step_quadratic_ratio_deviation": maximum_quadratic_ratio_deviation,
        "maximum_parent_scanner_normalized_coordinate_difference": maximum_scanner_normalized_coordinate_difference,
        "maximum_finite_analytic_event_residual": maximum_analytic_residual,
        "scan_checks": scan_checks,
        "scan_summary": summaries,
        "preregistered_branch_death_absence_count": len(absence_records),
        "preregistered_branch_death_absence_event_ids": sorted(
            {
                event_id
                for row in absence_records
                for event_id in str(
                    row["matched_preregistered_death_event_ids"]
                ).split("|")
            }
        ),
        "event_path": str(EVENTS.resolve()),
        "event_sha256": digest(EVENTS),
        "claim_boundary": claims,
        "formalization_workbench_modified_file_count": 0,
        "runtime_seconds": time.perf_counter() - started,
        "updated_utc": utc_now(),
    }
    atomic_csv(VALIDATION, validations)
    atomic_csv(RESIDUAL_VALIDATION, validations)
    atomic_csv(SOURCE_REGISTER, source_rows)
    atomic_json(RESULT, result)
    atomic_json(
        STATUS,
        {
            "checkpoint": CHECKPOINT,
            "state": "complete" if passed else "blocked",
            "decision": result["decision"],
            "updated_utc": result["updated_utc"],
        },
    )
    DOCUMENT.write_text(
        "\n".join(
            [
                "# 5367 - D4 E0003125 source-complete event geometry",
                "",
                "## Decision",
                "",
                f"`{result['decision']}`",
                "",
                "The already-frozen E0003125 asymptotic holdout now has eight finite-Q analytic event roots, independently cross-checked against the parent scanner. The exact material-polynomial/support equations remove the E01/E04 double-root tracker noise without altering topology.",
                "",
                f"- event count: `{result['event_count']}`;",
                f"- order: `{result['event_order_signature']}`;",
                f"- maximum normalized zero-to-analytic-E000625 continuation distance: `{result['maximum_relative_zero_to_E000625_continuation_distance']:.17g}`;",
                f"- maximum deviation of the half-step shift ratio from `1/4`: `{result['maximum_half_step_quadratic_ratio_deviation']:.17g}`;",
                f"- maximum analytic-to-parent-scan offset in residual-implied error units: `{result['maximum_parent_scanner_normalized_coordinate_difference']:.17g}`.",
                f"- parent homotopy absences resolved only inside preregistered branch-death windows: `{result['preregistered_branch_death_absence_count']}` evaluations across `{result['preregistered_branch_death_absence_event_ids']}`.",
                "",
                "No E0003125 integral, holdout compatibility, uniform remainder, regulator-zero, angular, UV, local-GR, or full-MTS claim is made.",
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True, allow_nan=False))
    return result


def validate_saved() -> dict[str, Any]:
    result = read_json(RESULT) if RESULT.is_file() else {}
    source_rows = read_csv(SOURCE_REGISTER) if SOURCE_REGISTER.is_file() else []
    drifts = [
        row["path"]
        for row in source_rows
        if not Path(row["path"]).is_file()
        or digest(Path(row["path"])) != row["sha256"]
    ]
    checks = {
        "result_validation_passes": result.get("validation_passed") is True,
        "validation_file_passes": VALIDATION.is_file()
        and csv_validation_passes(VALIDATION),
        "residual_validation_passes": RESIDUAL_VALIDATION.is_file()
        and csv_validation_passes(RESIDUAL_VALIDATION),
        "registered_sources_are_current": bool(source_rows) and not drifts,
        "event_hash_is_current": EVENTS.is_file()
        and result.get("event_sha256") == digest(EVENTS),
        "document_exists": DOCUMENT.is_file(),
        "formal_workbench_unchanged": formal_inventory_digest() == FORMAL_DIGEST,
        "scripts_cache_absent": not (SCRIPTS / "__pycache__").exists(),
    }
    return {
        "mode": "validate-saved",
        "checks": checks,
        "source_drifts": drifts,
        "all_pass": all(checks.values()),
    }


def main() -> int:
    set_below_normal_priority()
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--validate-saved", action="store_true")
    arguments = parser.parse_args()
    if arguments.dry_run:
        payload = preflight()
    elif arguments.validate_saved:
        payload = validate_saved()
    else:
        payload = run_geometry()
    if arguments.dry_run or arguments.validate_saved:
        print(json.dumps(payload, indent=2, sort_keys=True, allow_nan=False))
    return 0 if payload.get("all_pass", payload.get("validation_passed", False)) else 1


if __name__ == "__main__":
    raise SystemExit(main())
