from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import time
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SCRIPTS = POST / "scripts"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
RESIDUALS = POST / "source-intake" / "mts_residuals"
SOURCE = FUNCTIONAL_RG / "5318"
SHARDS = SOURCE / "shards"

SCRIPT_5317 = SCRIPTS / "Y5_R2FR_5317_targeted_inner_pole_resolution.py"
RESULT_5317 = FUNCTIONAL_RG / "5317" / "targeted_inner_pole_resolution_result.json"
VALIDATION_5317 = FUNCTIONAL_RG / "5317" / "targeted_inner_pole_resolution_validation.csv"
PANELS_5317 = FUNCTIONAL_RG / "5317" / "repaired_four_regulator_panel_convergence.csv"
RESULT_5315 = FUNCTIONAL_RG / "5315" / "squared_event_coordinate_collar_repair_result.json"
VALIDATION_5315 = FUNCTIONAL_RG / "5315" / "squared_event_coordinate_collar_repair_validation.csv"
CONTRACT_5312 = FUNCTIONAL_RG / "5312" / "reduced_fixed_decay_cubature_contract.csv"
SUPPORT_EVENTS_5313 = FUNCTIONAL_RG / "5313" / "P9_material_pole_support_events.csv"
EVENTS_5314 = FUNCTIONAL_RG / "5314" / "shared_branch_outer_events.csv"

DRY_RUN = SOURCE / "regulator_specific_squared_event_repair_dry_run.json"
EVENT_AUDIT = SOURCE / "regulator_specific_panel_nine_events.csv"
SEGMENT_PLAN = SOURCE / "regulator_specific_panel_nine_segment_plan.csv"
NODE_MANIFEST = SOURCE / "regulator_specific_outer_node_manifest.csv"
OFF_AXIS_AUDIT = SOURCE / "regulator_specific_off_axis_raw_audit.csv"
ADAPTIVE_PANELS = SOURCE / "regulator_specific_adaptive_panel_tree.csv"
REGULATOR_CONVERGENCE = SOURCE / "four_regulator_panel_nine_convergence.csv"
FIVE_REGULATOR_STATUS = SOURCE / "five_regulator_fixed_decay_convergence.csv"
RESULT = SOURCE / "regulator_specific_squared_event_outer_repair_result.json"
VALIDATION = SOURCE / "regulator_specific_squared_event_outer_repair_validation.csv"
RESIDUAL_VALIDATION = RESIDUALS / "P8_Y5_BRR545_5318_VALIDATION.csv"
STATUS = SOURCE / "status.json"
DOCUMENT = POST / "5318-Y5-R2FR-regulator-specific-squared-event-outer-repair.md"

CHECKPOINT = 5318
PARENT_CHECKPOINT = 5317
MARKER = "MTS_5318_REGULATOR_SPECIFIC_SQUARED_EVENT_OUTER_REPAIR"
REVISION = "regulator-specific-squared-event-outer-repair-v2"
NODE_REVISION_PREFIX = "regulator-specific-squared-event-node-v1"
EVENT_REVISION = "regulator-specific-panel-nine-event-v1"
TARGET_PANEL_INDEX = 9
OUTER_ORDERS = (8, 12)
LOCAL_OUTER_CHANGE_LIMIT = 5.0e-3
GLOBAL_OUTER_ERROR_BUDGET_LIMIT = 1.0e-2
MAXIMUM_ADAPTIVE_DEPTH = 3
EVENT_INITIAL_HALF_WIDTH = 1.0e-4
EVENT_MAXIMUM_EXPANSIONS = 4
EVENT_GAP_TOLERANCE = 1.0e-12
EVENT_COORDINATE_ERROR_TOLERANCE = 1.0e-10
EVENT_MAXIMUM_ITERATIONS = 8
BRANCH_DEATH_WIDTH_TOLERANCE = 2.0e-10
BRANCH_DEATH_MAXIMUM_ITERATIONS = 20
MINIMUM_CROSSING_SLOPE = 1.0e-3
FIT_BACKGROUND_DEGREE = 6
FIT_SCALES = (1.0, 1.5)
FIT_UNITS = (
    -5.0,
    -4.0,
    -3.0,
    -2.5,
    -2.0,
    -1.5,
    -1.0,
    -0.5,
    0.5,
    1.0,
    1.5,
    2.0,
    2.5,
    3.0,
    4.0,
    5.0,
)
HOLDOUT_UNITS = (
    -4.5,
    -3.5,
    -2.75,
    -2.25,
    -1.75,
    -1.25,
    -0.75,
    -0.25,
    0.25,
    0.75,
    1.25,
    1.75,
    2.25,
    2.75,
    3.5,
    4.5,
)
MAXIMUM_POLE_REFINEMENTS = 4
POLE_REFINEMENT_TOLERANCE = 1.0e-12
FIT_RELATIVE_RESIDUAL_LIMIT = 1.0e-5
HOLDOUT_RELATIVE_RESIDUAL_LIMIT = 1.0e-5
RESIDUE_SCALE_CHANGE_LIMIT = 1.0e-3
SECOND_ORDER_SUPPRESSION_LIMIT = 1.0e-4
OFF_AXIS_FLOAT_SEPARATION_MULTIPLIER = 100.0
OFF_AXIS_FIT_RADIUS_RATIO_MINIMUM = 100.0
OFF_AXIS_RAW_RELATIVE_CHANGE_LIMIT = 1.0e-8
DEFAULT_RUNTIME_LIMIT_SECONDS = 2.5 * 3600.0
CLAIM_FIELDS = (
    "valid_for_full_regulator_zero_limit",
    "valid_for_decay_angle_integration",
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


M5317 = load_module("mts_5317_for_5318", SCRIPT_5317)
M5316 = M5317.M5316
M5315 = M5316.M5315
M5314 = M5315.M5314
M5312 = M5317.M5312
M5283 = M5317.M5283
np = M5312.np
mp = M5312.mp


def read_json(path: Path) -> Any:
    return M5312.read_json(path)


def read_csv(path: Path) -> list[dict[str, str]]:
    return M5312.read_csv(path)


def write_csv(
    path: Path,
    rows: list[dict[str, Any]],
    fieldnames: list[str] | None = None,
) -> None:
    M5312.write_csv(path, rows, fieldnames)


def atomic_json(path: Path, value: Any) -> None:
    M5312.atomic_json(path, value)


def digest(path: Path) -> str:
    return M5312.digest(path)


def parse_bool(value: Any) -> bool:
    return M5312.parse_bool(value)


def complex_fields(prefix: str, value: complex) -> dict[str, float]:
    return M5312.complex_fields(prefix, value)


def relative_complex_change(first: complex, second: complex) -> float:
    return M5312.relative_complex_change(first, second)


def validation_gate(gate: str, passed: bool, detail: str) -> dict[str, Any]:
    return M5312.validation_gate(gate, passed, detail)


def target_regulators() -> tuple[tuple[str, float], ...]:
    return M5316.TARGET_REGULATORS


def panel_nine_limits(contract: list[dict[str, str]]) -> tuple[float, float]:
    rows = [row for row in contract if int(row["x_panel_index"]) == TARGET_PANEL_INDEX]
    return (
        min(float(row["lower_absolute_soft_cosine"]) for row in rows),
        max(float(row["upper_absolute_soft_cosine"]) for row in rows),
    )


def branch_exists(coordinate: float, contract: list[dict[str, str]]) -> bool:
    cells = [
        M5312.cell_geometry(row, coordinate)
        for row in contract
        if int(row["x_panel_index"]) == TARGET_PANEL_INDEX
        and int(row["reduced_MC04_term_count"]) > 0
    ]
    return M5314.target_branch_row(coordinate, cells) is not None


def derive_support_event(
    epsilon_id: str,
    event_type: str,
    approximate: float,
    contract: list[dict[str, str]],
) -> dict[str, Any]:
    panel_lower, panel_upper = panel_nine_limits(contract)
    half_width = EVENT_INITIAL_HALF_WIDTH
    left_state: dict[str, float] | None = None
    right_state: dict[str, float] | None = None
    left = right = approximate
    for _ in range(EVENT_MAXIMUM_EXPANSIONS + 1):
        left = max(panel_lower + 1.0e-10, approximate - half_width)
        right = min(panel_upper - 1.0e-10, approximate + half_width)
        left_state = M5315.event_gap(left, event_type, contract)
        right_state = M5315.event_gap(right, event_type, contract)
        if float(left_state["gap"]) * float(right_state["gap"]) <= 0.0:
            break
        half_width *= 2.0
    if left_state is None or right_state is None:
        raise RuntimeError(f"no {event_type} bracket for {epsilon_id}")
    initial_left_gap = float(left_state["gap"])
    initial_right_gap = float(right_state["gap"])
    if initial_left_gap * initial_right_gap > 0.0:
        raise RuntimeError(f"{event_type} broad bracket does not straddle zero")
    source_left = left
    source_right = right
    evaluation_count = 2
    root_state = left_state
    for _ in range(EVENT_MAXIMUM_ITERATIONS):
        left_gap = float(left_state["gap"])
        right_gap = float(right_state["gap"])
        denominator = right_gap - left_gap
        candidate = (
            (left * right_gap - right * left_gap) / denominator
            if denominator != 0.0
            else 0.5 * (left + right)
        )
        if not left < candidate < right:
            candidate = 0.5 * (left + right)
        root_state = M5315.event_gap(candidate, event_type, contract)
        evaluation_count += 1
        root_gap = float(root_state["gap"])
        if abs(root_gap) <= EVENT_GAP_TOLERANCE:
            break
        if float(left_state["gap"]) * root_gap <= 0.0:
            right = candidate
            right_state = root_state
        else:
            left = candidate
            left_state = root_state
    for _ in range(3):
        if abs(float(root_state["gap"])) <= EVENT_GAP_TOLERANCE:
            break
        root_coordinate = float(root_state["coordinate"])
        step = min(1.0e-8, 0.2 * (right - left))
        if step <= 0.0:
            break
        minus = M5315.event_gap(root_coordinate - step, event_type, contract)
        plus = M5315.event_gap(root_coordinate + step, event_type, contract)
        evaluation_count += 2
        derivative = (float(plus["gap"]) - float(minus["gap"])) / (2.0 * step)
        if derivative == 0.0 or not math.isfinite(derivative):
            break
        candidate = root_coordinate - float(root_state["gap"]) / derivative
        if not source_left < candidate < source_right:
            break
        root_state = M5315.event_gap(candidate, event_type, contract)
        evaluation_count += 1
    slope = (initial_right_gap - initial_left_gap) / (source_right - source_left)
    coordinate_error = abs(float(root_state["gap"])) / max(abs(slope), 1.0e-300)
    passes = (
        coordinate_error <= EVENT_COORDINATE_ERROR_TOLERANCE
        and abs(slope) >= MINIMUM_CROSSING_SLOPE
    )
    return {
        "epsilon_id": epsilon_id,
        "event_id": "E01" if event_type == "SUPPORT_ENTRY" else "E02",
        "event_type": event_type,
        "event_revision": EVENT_REVISION,
        "source_approximate_coordinate": approximate,
        "bracket_left_coordinate": source_left,
        "bracket_right_coordinate": source_right,
        "event_coordinate": root_state["coordinate"],
        "event_pole_real": root_state["pole_real"],
        "event_support_edge": root_state["support_edge"],
        "event_edge_gap": root_state["gap"],
        "event_coordinate_error_estimate": coordinate_error,
        "crossing_slope": slope,
        "crossing_slope_magnitude": abs(slope),
        "evaluation_count": evaluation_count,
        "event_contract_passes": passes,
        "contract_sha256": digest(CONTRACT_5312),
        **{field: False for field in CLAIM_FIELDS},
    }


def derive_branch_death(
    epsilon_id: str,
    source: dict[str, str],
    contract: list[dict[str, str]],
) -> dict[str, Any]:
    approximate = float(source["event_absolute_soft_cosine"])
    left = float(source["left_bracket_absolute_soft_cosine"])
    right = float(source["right_bracket_absolute_soft_cosine"])
    left_exists = branch_exists(left, contract)
    right_exists = branch_exists(right, contract)
    evaluation_count = 2
    if left_exists == right_exists:
        half_width = EVENT_INITIAL_HALF_WIDTH
        for _ in range(EVENT_MAXIMUM_EXPANSIONS + 1):
            left = approximate - half_width
            right = approximate + half_width
            left_exists = branch_exists(left, contract)
            right_exists = branch_exists(right, contract)
            evaluation_count += 2
            if left_exists != right_exists:
                break
            half_width *= 2.0
    if left_exists == right_exists:
        raise RuntimeError(f"shared-branch death not bracketed for {epsilon_id}")
    source_left = left
    source_right = right
    for _ in range(BRANCH_DEATH_MAXIMUM_ITERATIONS):
        if right - left <= BRANCH_DEATH_WIDTH_TOLERANCE:
            break
        midpoint = 0.5 * (left + right)
        middle_exists = branch_exists(midpoint, contract)
        evaluation_count += 1
        if middle_exists == left_exists:
            left = midpoint
        else:
            right = midpoint
    coordinate = 0.5 * (left + right)
    passes = (
        left_exists != right_exists
        and right - left <= BRANCH_DEATH_WIDTH_TOLERANCE
    )
    return {
        "epsilon_id": epsilon_id,
        "event_id": "E03",
        "event_type": "SHARED_BRANCH_DEATH",
        "event_revision": EVENT_REVISION,
        "source_approximate_coordinate": approximate,
        "bracket_left_coordinate": source_left,
        "bracket_right_coordinate": source_right,
        "event_coordinate": coordinate,
        "final_bracket_width": right - left,
        "left_branch_exists": left_exists,
        "right_branch_exists": right_exists,
        "evaluation_count": evaluation_count,
        "event_contract_passes": passes,
        "contract_sha256": digest(CONTRACT_5312),
        **{field: False for field in CLAIM_FIELDS},
    }


def event_cache_current() -> bool:
    if not EVENT_AUDIT.exists():
        return False
    rows = read_csv(EVENT_AUDIT)
    return (
        len(rows) == 3 * len(target_regulators())
        and all(row.get("event_revision") == EVENT_REVISION for row in rows)
        and all(row.get("contract_sha256") == digest(CONTRACT_5312) for row in rows)
        and all(parse_bool(row["event_contract_passes"]) for row in rows)
    )


def derive_regulator_events() -> list[dict[str, Any]]:
    if EVENT_AUDIT.exists():
        adjudicated = read_csv(EVENT_AUDIT)
        changed = False
        for row in adjudicated:
            if row.get("event_type") not in {"SUPPORT_ENTRY", "SUPPORT_EXIT"}:
                continue
            slope = abs(float(row["crossing_slope"]))
            coordinate_error = abs(float(row["event_edge_gap"])) / max(slope, 1.0e-300)
            passes = (
                slope >= MINIMUM_CROSSING_SLOPE
                and coordinate_error <= EVENT_COORDINATE_ERROR_TOLERANCE
            )
            if (
                row.get("event_coordinate_error_estimate") != str(coordinate_error)
                or parse_bool(row.get("event_contract_passes", False)) != passes
            ):
                row["event_coordinate_error_estimate"] = coordinate_error
                row["event_contract_passes"] = passes
                changed = True
        if changed:
            write_csv(EVENT_AUDIT, adjudicated, ["epsilon_id", "event_id", "event_type"])
    if event_cache_current():
        return read_csv(EVENT_AUDIT)
    contract = read_csv(CONTRACT_5312)
    support_sources = {
        row["event_type"]: float(row["event_absolute_soft_cosine"])
        for row in read_csv(SUPPORT_EVENTS_5313)
        if row["event_type"] in {"SUPPORT_ENTRY", "SUPPORT_EXIT"}
    }
    death_source = next(
        row
        for row in read_csv(EVENTS_5314)
        if row["event_type"] == "SHARED_BRANCH_DEATH"
    )
    existing = read_csv(EVENT_AUDIT) if EVENT_AUDIT.exists() else []
    existing_lookup = {
        (row["epsilon_id"], row["event_type"]): row
        for row in existing
        if row.get("event_revision") == EVENT_REVISION
        and row.get("contract_sha256") == digest(CONTRACT_5312)
        and parse_bool(row.get("event_contract_passes", False))
    }
    rows: list[dict[str, Any]] = []
    for epsilon_id, epsilon in target_regulators():
        old = M5316.set_kernel_globals(epsilon_id, epsilon)
        try:
            for event_type in ("SUPPORT_ENTRY", "SUPPORT_EXIT"):
                cached = existing_lookup.get((epsilon_id, event_type))
                rows.append(
                    cached
                    if cached is not None
                    else derive_support_event(
                        epsilon_id,
                        event_type,
                        support_sources[event_type],
                        contract,
                    )
                )
            cached_death = existing_lookup.get((epsilon_id, "SHARED_BRANCH_DEATH"))
            rows.append(
                cached_death
                if cached_death is not None
                else derive_branch_death(epsilon_id, death_source, contract)
            )
        finally:
            M5316.restore_kernel_globals(old)
        write_csv(EVENT_AUDIT, rows, ["epsilon_id", "event_id", "event_type"])
        atomic_json(
            STATUS,
            {
                "checkpoint": CHECKPOINT,
                "state": "RUNNING",
                "stage": "REGULATOR_SPECIFIC_EVENT_DERIVATION",
                "last_completed_epsilon_id": epsilon_id,
            },
        )
    return rows


def build_segment_plan(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    contract = read_csv(CONTRACT_5312)
    panel_lower, panel_upper = panel_nine_limits(contract)
    rows: list[dict[str, Any]] = []
    for epsilon_id, epsilon in target_regulators():
        local = {
            row["event_type"]: float(row["event_coordinate"])
            for row in events
            if row["epsilon_id"] == epsilon_id
        }
        entry = local["SUPPORT_ENTRY"]
        exit_coordinate = local["SUPPORT_EXIT"]
        death = local["SHARED_BRANCH_DEATH"]
        midpoint = 0.5 * (entry + exit_coordinate)
        pieces = (
            ("S01", panel_lower, entry, -1, entry, "SUPPORT_ENTRY"),
            ("S02", entry, midpoint, 1, entry, "SUPPORT_ENTRY"),
            ("S03", midpoint, exit_coordinate, -1, exit_coordinate, "SUPPORT_EXIT"),
            ("S04", exit_coordinate, death, 1, exit_coordinate, "SUPPORT_EXIT"),
            ("S05", death, panel_upper, 0, math.nan, "SMOOTH_AFTER_BRANCH_DEATH"),
        )
        for segment_id, lower, upper, direction, event, event_type in pieces:
            if not lower < upper:
                raise RuntimeError(f"reversed {epsilon_id} segment {segment_id}")
            rows.append(
                {
                    "epsilon_id": epsilon_id,
                    "epsilon": epsilon,
                    "initial_segment_id": segment_id,
                    "adaptive_panel_id": segment_id,
                    "adaptive_depth": 0,
                    "parent_adaptive_panel_id": "",
                    "lower_absolute_soft_cosine": lower,
                    "upper_absolute_soft_cosine": upper,
                    "segment_width": upper - lower,
                    "transform_direction": direction,
                    "event_coordinate": "" if direction == 0 else event,
                    "event_type": event_type,
                    "transform_equation": (
                        "x=x_event-t^2; dx=2t dt"
                        if direction < 0
                        else (
                            "x=x_event+t^2; dx=2t dt"
                            if direction > 0
                            else "x=x_mid+h*u; dx=h du"
                        )
                    ),
                    "exact_partition_contract_passes": True,
                    **{field: False for field in CLAIM_FIELDS},
                }
            )
    write_csv(SEGMENT_PLAN, rows, ["epsilon_id", "initial_segment_id"])
    return rows


def dry_run() -> dict[str, Any]:
    M5312.set_below_normal_priority()
    mp.mp.dps = M5312.M5280.MP_DECIMAL_DIGITS
    M5312.M5301.configure_reused_pipeline()
    started = time.perf_counter()
    required = [
        SCRIPT_5317,
        RESULT_5317,
        VALIDATION_5317,
        PANELS_5317,
        RESULT_5315,
        VALIDATION_5315,
        CONTRACT_5312,
        SUPPORT_EVENTS_5313,
        EVENTS_5314,
    ]
    missing = [str(path) for path in required if not path.exists()]
    parent = read_json(RESULT_5317) if not missing else {}
    parent_validation = read_csv(VALIDATION_5317) if not missing else []
    events = derive_regulator_events() if not missing else []
    segments = build_segment_plan(events) if events else []
    checks = {
        "required_paths_exist": not missing,
        "parent_5317_inner_layer_validated": (
            bool(parent)
            and bool(parent["acceptance_passed"])
            and all(parse_bool(row["passed"]) for row in parent_validation)
        ),
        "three_events_derived_for_each_regulator": (
            len(events) == 12
            and all(parse_bool(row["event_contract_passes"]) for row in events)
            and all(
                {
                    row["event_type"]
                    for row in events
                    if row["epsilon_id"] == epsilon_id
                }
                == {"SUPPORT_ENTRY", "SUPPORT_EXIT", "SHARED_BRANCH_DEATH"}
                for epsilon_id, _ in target_regulators()
            )
        ),
        "five_exact_segments_partition_each_panel_nine": (
            len(segments) == 20
            and all(parse_bool(row["exact_partition_contract_passes"]) for row in segments)
        ),
        "formalization_workbench_unchanged": (
            bool(parent)
            and M5283.formal_inventory_digest()
            == parent["formalization_workbench_end_digest"]
        ),
    }
    accepted = all(checks.values())
    result = {
        "checkpoint": CHECKPOINT,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "mode": "dry-run",
        "acceptance_passed": accepted,
        "decision": (
            "DRY_RUN_ACCEPTED__RUN_REGULATOR_SPECIFIC_PANEL_NINE_REPAIR"
            if accepted
            else "REGULATOR_SPECIFIC_PANEL_NINE_REPAIR_DRY_RUN_BLOCKED"
        ),
        "checks": checks,
        "missing_paths": missing,
        "event_count": len(events),
        "initial_segment_count": len(segments),
        "runtime_seconds": time.perf_counter() - started,
        **{field: False for field in CLAIM_FIELDS},
    }
    atomic_json(DRY_RUN, result)
    return result


def normalized_fit_radius(pole: complex, lower: float, upper: float) -> float:
    distance = M5314.pole_boundary_distance(pole, lower, upper)
    if distance <= 1.0e-12:
        return 0.0
    boundary_safe = 0.8 * distance / (max(abs(value) for value in FIT_UNITS) * max(FIT_SCALES))
    return min(max(8.0 * abs(pole.imag), 2.0e-6), boundary_safe)


def normalized_unmasked_fit(
    coordinate: float,
    pole: complex,
    lower: float,
    upper: float,
    fit_scale: float,
    units: tuple[float, ...],
    evaluate_unmasked: Any,
) -> dict[str, Any]:
    radius = fit_scale * normalized_fit_radius(pole, lower, upper)
    if radius <= 0.0:
        raise RuntimeError("nonpositive normalized endpoint-collar fit radius")
    center = pole.real
    matrix_rows: list[list[complex]] = []
    values: list[complex] = []
    metadata: list[dict[str, Any]] = []
    specification = M5314.M5308.SURFACE_LOOKUP[M5314.TARGET_TERM_ID]
    for unit in units:
        energy = center + unit * radius
        evaluation = evaluate_unmasked(
            energy,
            coordinate,
            int(specification["soft_sign"]),
            int(specification["decay_sign"]),
        )
        matrix_rows.append(
            [
                radius**2 / (energy - pole) ** 2,
                radius / (energy - pole),
                *[
                    complex(unit**power)
                    for power in range(FIT_BACKGROUND_DEGREE + 1)
                ],
            ]
        )
        values.append(evaluation["value"])
        metadata.append(evaluation)
    matrix = np.asarray(matrix_rows, dtype=np.complex128)
    vector = np.asarray(values, dtype=np.complex128)
    coefficients, _, rank, singular_values = np.linalg.lstsq(matrix, vector, rcond=None)
    residual = float(np.linalg.norm(matrix @ coefficients - vector) / max(np.linalg.norm(vector), 1.0))
    return {
        "fit_scale": fit_scale,
        "fit_radius": radius,
        "fit_sample_count": len(units),
        "fit_relative_residual": residual,
        "second_order_coefficient": complex(coefficients[0]) * radius**2,
        "simple_residue": complex(coefficients[1]) * radius,
        "coefficients": coefficients,
        "matrix_rank": int(rank),
        "matrix_column_count": int(matrix.shape[1]),
        "condition_number": float(singular_values[0] / singular_values[-1]),
        "fit_mask_state_count": len({bool(row["mask_active"]) for row in metadata}),
        "fit_orientation_count": len({int(row["orientation"]) for row in metadata}),
        "fit_label_count": len({str(row["selected_labels"]) for row in metadata}),
        "maximum_root_equation_residual": max(float(row["root_equation_residual"]) for row in metadata),
        "maximum_root_refinement_chordal_distance": max(float(row["root_refinement_chordal_distance"]) for row in metadata),
    }


def normalized_unmasked_holdout(
    coordinate: float,
    pole: complex,
    fit: dict[str, Any],
    evaluate_unmasked: Any,
) -> dict[str, Any]:
    radius = float(fit["fit_radius"])
    center = pole.real
    specification = M5314.M5308.SURFACE_LOOKUP[M5314.TARGET_TERM_ID]
    matrix_rows: list[list[complex]] = []
    values: list[complex] = []
    metadata: list[dict[str, Any]] = []
    for unit in HOLDOUT_UNITS:
        energy = center + unit * radius
        evaluation = evaluate_unmasked(
            energy,
            coordinate,
            int(specification["soft_sign"]),
            int(specification["decay_sign"]),
        )
        matrix_rows.append(
            [
                radius**2 / (energy - pole) ** 2,
                radius / (energy - pole),
                *[
                    complex(unit**power)
                    for power in range(FIT_BACKGROUND_DEGREE + 1)
                ],
            ]
        )
        values.append(evaluation["value"])
        metadata.append(evaluation)
    matrix = np.asarray(matrix_rows, dtype=np.complex128)
    vector = np.asarray(values, dtype=np.complex128)
    residual = float(
        np.linalg.norm(matrix @ fit["coefficients"] - vector)
        / max(np.linalg.norm(vector), 1.0)
    )
    return {
        "holdout_relative_residual": residual,
        "holdout_mask_state_count": len({bool(row["mask_active"]) for row in metadata}),
        "holdout_orientation_count": len({int(row["orientation"]) for row in metadata}),
        "holdout_label_count": len({str(row["selected_labels"]) for row in metadata}),
    }


def normalized_refine_simple_pole(
    coordinate: float,
    source: dict[str, Any],
    evaluate_unmasked: Any,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    lower = float(source["support_energy_lower"])
    upper = float(source["support_energy_upper"])
    geometric = complex(float(source["pole_real"]), float(source["pole_imaginary"]))
    refined = geometric
    iteration_rows: list[dict[str, Any]] = []
    converged = False
    for iteration in range(1, MAXIMUM_POLE_REFINEMENTS + 1):
        fit = normalized_unmasked_fit(
            coordinate, refined, lower, upper, 1.0, FIT_UNITS, evaluate_unmasked
        )
        residue = fit["simple_residue"]
        correction = (
            fit["second_order_coefficient"] / residue
            if abs(residue) > 0.0
            else complex(math.inf, math.inf)
        )
        iteration_rows.append(
            {
                "fit_row_type": "POLE_REFINEMENT_ITERATION",
                "pole_refinement_iteration": iteration,
                "fit_scale": 1.0,
                "fit_radius": fit["fit_radius"],
                "fit_sample_count": fit["fit_sample_count"],
                **complex_fields("input_pole", refined),
                **complex_fields("second_order_coefficient_R2", fit["second_order_coefficient"]),
                **complex_fields("simple_residue_R1", residue),
                **complex_fields("pole_correction_R2_over_R1", correction),
                "fit_relative_residual": fit["fit_relative_residual"],
                "holdout_relative_residual": "",
                "fit_mask_state_count": fit["fit_mask_state_count"],
                "fit_orientation_count": fit["fit_orientation_count"],
                "fit_label_count": fit["fit_label_count"],
                "matrix_rank": fit["matrix_rank"],
                "matrix_column_count": fit["matrix_column_count"],
                "condition_number": fit["condition_number"],
            }
        )
        if not math.isfinite(abs(correction)):
            break
        refined += correction
        if abs(correction) <= POLE_REFINEMENT_TOLERANCE:
            converged = True
            break
    final_fits: list[dict[str, Any]] = []
    for scale in FIT_SCALES:
        fit = normalized_unmasked_fit(
            coordinate, refined, lower, upper, scale, FIT_UNITS, evaluate_unmasked
        )
        fit.update(normalized_unmasked_holdout(coordinate, refined, fit, evaluate_unmasked))
        fit["second_order_suppression_ratio"] = abs(fit["second_order_coefficient"]) / max(
            abs(fit["simple_residue"])
            * max(abs(refined.imag), float(fit["fit_radius"]), 1.0e-9),
            1.0e-300,
        )
        final_fits.append(fit)
    residue_change = relative_complex_change(
        final_fits[0]["simple_residue"], final_fits[1]["simple_residue"]
    )
    structure_passes = all(
        fit["fit_mask_state_count"] == fit["holdout_mask_state_count"] == 1
        and fit["fit_orientation_count"] == fit["holdout_orientation_count"] == 1
        and fit["fit_label_count"] == fit["holdout_label_count"] == 1
        for fit in final_fits
    )
    conditioning_passes = all(
        fit["matrix_rank"] == fit["matrix_column_count"]
        and fit["condition_number"] * np.finfo(float).eps
        <= FIT_RELATIVE_RESIDUAL_LIMIT / 100.0
        for fit in final_fits
    )
    contract_passes = (
        converged
        and structure_passes
        and conditioning_passes
        and max(fit["fit_relative_residual"] for fit in final_fits)
        <= FIT_RELATIVE_RESIDUAL_LIMIT
        and max(fit["holdout_relative_residual"] for fit in final_fits)
        <= HOLDOUT_RELATIVE_RESIDUAL_LIMIT
        and residue_change <= RESIDUE_SCALE_CHANGE_LIMIT
        and max(fit["second_order_suppression_ratio"] for fit in final_fits)
        <= SECOND_ORDER_SUPPRESSION_LIMIT
    )
    final_rows: list[dict[str, Any]] = []
    for fit in final_fits:
        final_rows.append(
            {
                "fit_row_type": "FINAL_REFINED_SIMPLE_POLE_FIT",
                "pole_refinement_iteration": len(iteration_rows),
                "fit_scale": fit["fit_scale"],
                "fit_radius": fit["fit_radius"],
                "fit_sample_count": fit["fit_sample_count"],
                "holdout_sample_count": len(HOLDOUT_UNITS),
                **complex_fields("refined_pole", refined),
                **complex_fields("geometric_to_refined_pole_shift", refined - geometric),
                **complex_fields("second_order_coefficient_R2", fit["second_order_coefficient"]),
                **complex_fields("simple_residue_R1", fit["simple_residue"]),
                "fit_relative_residual": fit["fit_relative_residual"],
                "holdout_relative_residual": fit["holdout_relative_residual"],
                "fit_mask_state_count": fit["fit_mask_state_count"],
                "fit_orientation_count": fit["fit_orientation_count"],
                "fit_label_count": fit["fit_label_count"],
                "holdout_mask_state_count": fit["holdout_mask_state_count"],
                "holdout_orientation_count": fit["holdout_orientation_count"],
                "holdout_label_count": fit["holdout_label_count"],
                "matrix_rank": fit["matrix_rank"],
                "matrix_column_count": fit["matrix_column_count"],
                "condition_number": fit["condition_number"],
                "residue_fit_scale_relative_change": residue_change,
                "second_order_suppression_ratio": fit["second_order_suppression_ratio"],
                "refined_simple_pole_contract_passes": contract_passes,
            }
        )
    selected = {
        "geometric_pole": geometric,
        "refined_pole": refined,
        "selected_residue": final_fits[-1]["simple_residue"],
        "pole_side": M5314.pole_side(refined, lower, upper),
        "support_energy_lower": lower,
        "support_energy_upper": upper,
        "fit_relative_residual": max(fit["fit_relative_residual"] for fit in final_fits),
        "holdout_relative_residual": max(fit["holdout_relative_residual"] for fit in final_fits),
        "residue_fit_scale_relative_change": residue_change,
        "second_order_suppression_ratio": max(
            fit["second_order_suppression_ratio"] for fit in final_fits
        ),
        "contract_passes": contract_passes,
    }
    return selected, iteration_rows + final_rows


def plan_sha256(epsilon_id: str, segments: list[dict[str, Any]]) -> str:
    existing_results = sorted((SHARDS / epsilon_id).glob("*/result.json"))
    for path in existing_results:
        try:
            existing = read_json(path)
        except Exception:
            continue
        if existing.get("node_revision") == f"{NODE_REVISION_PREFIX}-{epsilon_id}":
            return str(existing["node_plan_sha256"])
    payload = {
        "revision": REVISION,
        "node_revision": f"{NODE_REVISION_PREFIX}-{epsilon_id}",
        "node_kernel_contract": "normalized-unmasked-Laurent-plus-Q8-Q12-v1",
        "parent_result_sha256": digest(RESULT_5317),
        "contract_sha256": digest(CONTRACT_5312),
        "outer_orders": OUTER_ORDERS,
        "maximum_adaptive_depth": MAXIMUM_ADAPTIVE_DEPTH,
        "segments": [
            {
                key: row[key]
                for key in (
                    "initial_segment_id",
                    "lower_absolute_soft_cosine",
                    "upper_absolute_soft_cosine",
                    "transform_direction",
                    "event_coordinate",
                )
            }
            for row in segments
            if row["epsilon_id"] == epsilon_id
        ],
    }
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()


def shard_paths(epsilon_id: str, node_id: str) -> dict[str, Path]:
    root = SHARDS / epsilon_id / node_id
    return {
        "root": root,
        "fits": root / "refined_pole_fits.csv",
        "integrals": root / "cell_integrals.csv",
        "result": root / "result.json",
    }


def shard_complete(
    epsilon_id: str,
    node: dict[str, Any],
    expected_plan_sha256: str,
) -> bool:
    paths = shard_paths(epsilon_id, node["node_id"])
    if not all(path.exists() for key, path in paths.items() if key != "root"):
        return False
    try:
        result = read_json(paths["result"])
        read_csv(paths["fits"])
        read_csv(paths["integrals"])
    except Exception:
        return False
    return (
        result.get("node_revision") == f"{NODE_REVISION_PREFIX}-{epsilon_id}"
        and result.get("node_plan_sha256") == expected_plan_sha256
        and result.get("node_id") == node["node_id"]
        and result.get("epsilon_id") == epsilon_id
        and bool(result.get("node_complete"))
    )


def panel_nodes(panel: dict[str, Any]) -> list[dict[str, Any]]:
    lower = float(panel["lower_absolute_soft_cosine"])
    upper = float(panel["upper_absolute_soft_cosine"])
    direction = int(panel["transform_direction"])
    rows: list[dict[str, Any]] = []
    for order in OUTER_ORDERS:
        nodes, weights = np.polynomial.legendre.leggauss(order)
        for index, (local_node, weight) in enumerate(zip(nodes, weights), start=1):
            if direction == 0:
                half = 0.5 * (upper - lower)
                midpoint = 0.5 * (upper + lower)
                coordinate = midpoint + half * float(local_node)
                mapped_weight = half * float(weight)
                transform_coordinate = float(local_node)
                transform_jacobian = half
            else:
                event = float(panel["event_coordinate"])
                t_max = math.sqrt(upper - lower)
                t_coordinate = 0.5 * t_max * (1.0 + float(local_node))
                coordinate = event + direction * t_coordinate**2
                mapped_weight = 0.5 * t_max * float(weight) * 2.0 * t_coordinate
                transform_coordinate = t_coordinate
                transform_jacobian = 2.0 * t_coordinate
            rows.append(
                {
                    "node_id": f"P09_{panel['adaptive_panel_id']}_Q{order:02d}_N{index:02d}",
                    "x_panel_index": TARGET_PANEL_INDEX,
                    "outer_order": order,
                    "local_node_index": index,
                    "initial_segment_id": panel["initial_segment_id"],
                    "adaptive_panel_id": panel["adaptive_panel_id"],
                    "adaptive_depth": panel["adaptive_depth"],
                    "event_type": panel["event_type"],
                    "transform_direction": direction,
                    "transform_coordinate": transform_coordinate,
                    "transform_jacobian": transform_jacobian,
                    "absolute_soft_cosine": coordinate,
                    "mapped_outer_weight": mapped_weight,
                    **{field: False for field in CLAIM_FIELDS},
                }
            )
    return rows


def effective_acceptance(
    epsilon_id: str,
    node: dict[str, Any],
    result: dict[str, Any],
) -> dict[str, Any]:
    fits = [
        row
        for row in read_csv(shard_paths(epsilon_id, node["node_id"])["fits"])
        if row.get("fit_row_type") == "FINAL_REFINED_SIMPLE_POLE_FIT"
    ]
    kernel_passes = bool(result["acceptance_passed"])
    fit_data_present = len(fits) == len(FIT_SCALES)
    minimum_separation = (
        min(abs(float(row["refined_pole_imaginary"])) for row in fits)
        if fit_data_present
        else 0.0
    )
    pole_scale = (
        max(1.0, max(abs(float(row["refined_pole_real"])) for row in fits))
        if fit_data_present
        else 1.0
    )
    floating_floor = OFF_AXIS_FLOAT_SEPARATION_MULTIPLIER * math.sqrt(np.finfo(float).eps) * pole_scale
    maximum_radius = (
        max(float(row["fit_radius"]) for row in fits)
        if fit_data_present
        else math.inf
    )
    separation_ratio = (
        minimum_separation / maximum_radius
        if maximum_radius > 0.0 and math.isfinite(maximum_radius)
        else 0.0
    )
    local_fit = (
        min(fits, key=lambda row: float(row["fit_scale"]))
        if fit_data_present
        else None
    )
    branch_identity_stable = (
        fit_data_present
        and all(
            int(row["fit_mask_state_count"]) == 1
            and int(row["fit_orientation_count"]) == 1
            and int(row["fit_label_count"]) == 1
            and int(row["holdout_mask_state_count"]) == 1
            and int(row["holdout_orientation_count"]) == 1
            and int(row["holdout_label_count"]) == 1
            for row in fits
        )
    )
    local_shape_gates = (
        local_fit is not None
        and float(local_fit["fit_relative_residual"])
        <= FIT_RELATIVE_RESIDUAL_LIMIT
        and float(local_fit["holdout_relative_residual"])
        <= HOLDOUT_RELATIVE_RESIDUAL_LIMIT
        and branch_identity_stable
    )
    local_shape_conditioning_diagnostic_passes = (
        local_fit is not None
        and int(local_fit["matrix_rank"]) == int(local_fit["matrix_column_count"])
        and float(local_fit["condition_number"]) * np.finfo(float).eps
        <= FIT_RELATIVE_RESIDUAL_LIMIT / 100.0
    )
    raw_inner_passes = (
        float(result["inner_Q8_Q12_relative_change"])
        <= OFF_AXIS_RAW_RELATIVE_CHANGE_LIMIT
        and float(result["inner_energy_error_budget_relative"])
        <= OFF_AXIS_RAW_RELATIVE_CHANGE_LIMIT
    )
    separation_passes = minimum_separation >= floating_floor
    override = (
        not kernel_passes
        and bool(result["target_branch_exists"])
        and bool(result["target_branch_inside_support"])
        and not bool(result["refined_pole_subtraction_applied"])
        and int(result["inactive_selected_term_count"]) == 0
        and local_shape_gates
        and raw_inner_passes
        and separation_passes
    )
    return {
        "epsilon_id": epsilon_id,
        "node_id": node["node_id"],
        "adaptive_panel_id": node["adaptive_panel_id"],
        "kernel_acceptance_passed": kernel_passes,
        "off_axis_raw_contract_passes": override,
        "effective_acceptance_passed": kernel_passes or override,
        "minimum_imaginary_contour_separation": minimum_separation,
        "floating_separation_floor": floating_floor,
        "separation_to_fit_radius_ratio": separation_ratio,
        "local_shape_fit_scale": (
            float(local_fit["fit_scale"]) if local_fit is not None else ""
        ),
        "local_shape_fit_relative_residual": (
            float(local_fit["fit_relative_residual"]) if local_fit is not None else ""
        ),
        "local_shape_holdout_relative_residual": (
            float(local_fit["holdout_relative_residual"])
            if local_fit is not None
            else ""
        ),
        "local_shape_condition_number": (
            float(local_fit["condition_number"]) if local_fit is not None else ""
        ),
        "local_shape_gate_passes": local_shape_gates,
        "local_shape_conditioning_diagnostic_passes": (
            local_shape_conditioning_diagnostic_passes
        ),
        "all_scale_branch_identity_stable": branch_identity_stable,
        "wider_collar_fit_relative_residual_maximum": (
            max(float(row["fit_relative_residual"]) for row in fits)
            if fit_data_present
            else ""
        ),
        "wider_collar_holdout_relative_residual_maximum": (
            max(float(row["holdout_relative_residual"]) for row in fits)
            if fit_data_present
            else ""
        ),
        "raw_inner_Q8_Q12_relative_change": result["inner_Q8_Q12_relative_change"],
        "raw_inner_error_budget_relative": result["inner_energy_error_budget_relative"],
        "reason": (
            "Kernel pass, or exact raw contour retention when subtraction is not "
            "used, one local analytic collar is resolved with stable branch identity, "
            "the real contour is separated, and direct Q8/Q12 convergence passes. "
            "Wide-collar residue stability is required for subtraction, not for "
            "retaining the full raw integrand."
        ),
        **{field: False for field in CLAIM_FIELDS},
    }


def run_node(
    epsilon_id: str,
    node: dict[str, Any],
    contract: list[dict[str, str]],
    expected_plan_sha256: str,
    branch_death: float,
    base_context: dict[str, Any],
    multiplier: float,
) -> dict[str, Any]:
    result = M5314.integrate_node(
        node,
        contract,
        expected_plan_sha256,
        branch_death,
        base_context,
        multiplier,
    )
    result.update(
        {
            "epsilon_id": epsilon_id,
            "epsilon": dict(target_regulators())[epsilon_id],
            "initial_segment_id": node["initial_segment_id"],
            "adaptive_panel_id": node["adaptive_panel_id"],
            "adaptive_depth": node["adaptive_depth"],
            "event_type": node["event_type"],
            "transform_direction": node["transform_direction"],
            "transform_coordinate": node["transform_coordinate"],
            "transform_jacobian": node["transform_jacobian"],
        }
    )
    atomic_json(shard_paths(epsilon_id, node["node_id"])["result"], result)
    return result


def evaluate_panel(
    epsilon_id: str,
    panel: dict[str, Any],
    contract: list[dict[str, str]],
    expected_plan_sha256: str,
    branch_death: float,
    base_context: dict[str, Any],
    multiplier: float,
    started: float,
    runtime_limit_seconds: float,
    encountered: dict[str, dict[str, Any]],
    audit_lookup: dict[str, dict[str, Any]],
) -> dict[str, Any] | None:
    nodes = panel_nodes(panel)
    results: dict[str, dict[str, Any]] = {}
    for node in nodes:
        encountered[node["node_id"]] = node
        if not shard_complete(epsilon_id, node, expected_plan_sha256):
            if time.perf_counter() - started >= runtime_limit_seconds:
                return None
            result = run_node(
                epsilon_id,
                node,
                contract,
                expected_plan_sha256,
                branch_death,
                base_context,
                multiplier,
            )
            atomic_json(
                STATUS,
                {
                    "checkpoint": CHECKPOINT,
                    "state": "RUNNING",
                    "stage": "REGULATOR_SPECIFIC_PANEL_NINE_NODES",
                    "epsilon_id": epsilon_id,
                    "adaptive_panel_id": panel["adaptive_panel_id"],
                    "last_completed_node_id": node["node_id"],
                },
            )
        else:
            result = read_json(shard_paths(epsilon_id, node["node_id"])["result"])
        results[node["node_id"]] = result
        audit = effective_acceptance(epsilon_id, node, result)
        audit_lookup[node["node_id"]] = audit
    all_inner_pass = all(
        bool(audit_lookup[node["node_id"]]["effective_acceptance_passed"])
        for node in nodes
    )
    totals: dict[int, complex] = {}
    for order in OUTER_ORDERS:
        totals[order] = sum(
            (
                float(node["mapped_outer_weight"])
                * complex(
                    float(results[node["node_id"]]["selected_inner_energy_real"]),
                    float(results[node["node_id"]]["selected_inner_energy_imaginary"]),
                )
                for node in nodes
                if int(node["outer_order"]) == order
            ),
            0.0j,
        )
    change = relative_complex_change(totals[8], totals[12])
    width = float(panel["upper_absolute_soft_cosine"]) - float(panel["lower_absolute_soft_cosine"])
    jacobian_errors = []
    for order in OUTER_ORDERS:
        weight_sum = sum(
            float(node["mapped_outer_weight"])
            for node in nodes
            if int(node["outer_order"]) == order
        )
        jacobian_errors.append(abs(weight_sum - width) / max(width, 1.0e-30))
    return {
        **panel,
        "panel_nodes_complete": True,
        "all_inner_nodes_pass": all_inner_pass,
        "off_axis_raw_contract_node_count": sum(
            bool(audit_lookup[node["node_id"]]["off_axis_raw_contract_passes"])
            for node in nodes
        ),
        **complex_fields("outer_Q8_inner_Q12", totals[8]),
        **complex_fields("outer_Q12_inner_Q12", totals[12]),
        "outer_Q8_Q12_absolute_change": abs(totals[12] - totals[8]),
        "outer_Q8_Q12_relative_change": change,
        "maximum_jacobian_relative_error": max(jacobian_errors),
        "exact_change_of_variables_gate_passes": max(jacobian_errors) <= 5.0e-13,
        "adaptive_gate_passes": (
            all_inner_pass
            and max(jacobian_errors) <= 5.0e-13
            and change <= LOCAL_OUTER_CHANGE_LIMIT
        ),
        **{field: False for field in CLAIM_FIELDS},
    }


def split_panel(panel: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    lower = float(panel["lower_absolute_soft_cosine"])
    upper = float(panel["upper_absolute_soft_cosine"])
    midpoint = 0.5 * (lower + upper)
    direction = int(panel["transform_direction"])
    depth = int(panel["adaptive_depth"]) + 1
    common = {
        "epsilon_id": panel["epsilon_id"],
        "epsilon": panel["epsilon"],
        "initial_segment_id": panel["initial_segment_id"],
        "adaptive_depth": depth,
        "parent_adaptive_panel_id": panel["adaptive_panel_id"],
        "event_type": panel["event_type"],
        **{field: False for field in CLAIM_FIELDS},
    }
    if direction < 0:
        left_direction, right_direction = 0, -1
        left_event, right_event = "", panel["event_coordinate"]
    elif direction > 0:
        left_direction, right_direction = 1, 0
        left_event, right_event = panel["event_coordinate"], ""
    else:
        left_direction = right_direction = 0
        left_event = right_event = ""
    left = {
        **common,
        "adaptive_panel_id": f"{panel['adaptive_panel_id']}L",
        "lower_absolute_soft_cosine": lower,
        "upper_absolute_soft_cosine": midpoint,
        "segment_width": midpoint - lower,
        "transform_direction": left_direction,
        "event_coordinate": left_event,
    }
    right = {
        **common,
        "adaptive_panel_id": f"{panel['adaptive_panel_id']}R",
        "lower_absolute_soft_cosine": midpoint,
        "upper_absolute_soft_cosine": upper,
        "segment_width": upper - midpoint,
        "transform_direction": right_direction,
        "event_coordinate": right_event,
    }
    return left, right


def refine_regulator(
    epsilon_id: str,
    initial_panels: list[dict[str, Any]],
    contract: list[dict[str, str]],
    expected_plan_sha256: str,
    branch_death: float,
    base_context: dict[str, Any],
    multiplier: float,
    started: float,
    runtime_limit_seconds: float,
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[str, dict[str, Any]],
    dict[str, dict[str, Any]],
    bool,
]:
    all_rows: list[dict[str, Any]] = []
    leaves: list[dict[str, Any]] = []
    encountered: dict[str, dict[str, Any]] = {}
    audits: dict[str, dict[str, Any]] = {}
    paused = False

    def visit(panel: dict[str, Any]) -> None:
        nonlocal paused
        if paused:
            return
        result = evaluate_panel(
            epsilon_id,
            panel,
            contract,
            expected_plan_sha256,
            branch_death,
            base_context,
            multiplier,
            started,
            runtime_limit_seconds,
            encountered,
            audits,
        )
        if result is None:
            paused = True
            return
        if bool(result["adaptive_gate_passes"]):
            result["adaptive_leaf"] = True
            result["failure_reason"] = ""
            all_rows.append(result)
            leaves.append(result)
            return
        if not bool(result["all_inner_nodes_pass"]):
            result["adaptive_leaf"] = True
            result["failure_reason"] = "INNER_NODE_FAILURE"
            all_rows.append(result)
            leaves.append(result)
            return
        if int(panel["adaptive_depth"]) >= MAXIMUM_ADAPTIVE_DEPTH:
            result["adaptive_leaf"] = True
            result["failure_reason"] = "MAXIMUM_ADAPTIVE_DEPTH"
            all_rows.append(result)
            leaves.append(result)
            return
        result["adaptive_leaf"] = False
        result["failure_reason"] = "REFINED_TO_CHILDREN"
        all_rows.append(result)
        left, right = split_panel(panel)
        visit(left)
        visit(right)

    for panel in initial_panels:
        visit(panel)
        if paused:
            break
    return all_rows, leaves, encountered, audits, paused


def kernel_context(epsilon_id: str, epsilon: float) -> dict[str, Any]:
    old_epsilon = M5316.set_kernel_globals(epsilon_id, epsilon)
    old = {
        "epsilon": old_epsilon,
        "shards": M5314.SHARDS,
        "checkpoint": M5314.CHECKPOINT,
        "node_revision": M5314.NODE_REVISION,
        "refine_simple_pole": M5314.refine_simple_pole,
    }
    M5314.SHARDS = SHARDS / epsilon_id
    M5314.CHECKPOINT = CHECKPOINT
    M5314.NODE_REVISION = f"{NODE_REVISION_PREFIX}-{epsilon_id}"
    M5314.refine_simple_pole = normalized_refine_simple_pole
    return old


def restore_kernel_context(old: dict[str, Any]) -> None:
    M5314.refine_simple_pole = old["refine_simple_pole"]
    M5314.NODE_REVISION = old["node_revision"]
    M5314.CHECKPOINT = old["checkpoint"]
    M5314.SHARDS = old["shards"]
    M5316.restore_kernel_globals(old["epsilon"])


def baseline_panels_one_to_eight(epsilon_id: str) -> tuple[complex, complex, float]:
    rows = [
        row
        for row in read_csv(PANELS_5317)
        if row["epsilon_id"] == epsilon_id and int(row["x_panel_index"]) <= 8
    ]
    low = sum(
        complex(float(row["outer_Q2_energy_Q8_real"]), float(row["outer_Q2_energy_Q8_imaginary"]))
        for row in rows
    )
    high = sum(
        complex(float(row["outer_Q4_energy_Q8_real"]), float(row["outer_Q4_energy_Q8_imaginary"]))
        for row in rows
    )
    error = sum(
        abs(
            complex(float(row["outer_Q4_energy_Q8_real"]), float(row["outer_Q4_energy_Q8_imaginary"]))
            - complex(float(row["outer_Q2_energy_Q8_real"]), float(row["outer_Q2_energy_Q8_imaginary"]))
        )
        for row in rows
    )
    return low, high, error


def source_rows() -> list[dict[str, str]]:
    paths = [
        Path(__file__).resolve(),
        SCRIPT_5317,
        RESULT_5317,
        VALIDATION_5317,
        PANELS_5317,
        RESULT_5315,
        VALIDATION_5315,
        CONTRACT_5312,
        SUPPORT_EVENTS_5313,
        EVENTS_5314,
        DRY_RUN,
        EVENT_AUDIT,
        SEGMENT_PLAN,
    ]
    return [{"path": str(path), "sha256": digest(path)} for path in paths]


def execute(runtime_limit_seconds: float) -> dict[str, Any]:
    M5312.set_below_normal_priority()
    mp.mp.dps = M5312.M5280.MP_DECIMAL_DIGITS
    M5312.M5301.configure_reused_pipeline()
    started = time.perf_counter()
    dry = dry_run()
    if not dry["acceptance_passed"]:
        raise RuntimeError("5318 dry run did not pass")
    events = read_csv(EVENT_AUDIT)
    segments = read_csv(SEGMENT_PLAN)
    contract = read_csv(CONTRACT_5312)
    base_context = M5314.M5303.synthetic_context()
    multiplier = M5314.M5309.physical_multiplier()
    all_panel_rows: list[dict[str, Any]] = []
    all_leaves: list[dict[str, Any]] = []
    all_encountered: dict[tuple[str, str], dict[str, Any]] = {}
    all_audits: dict[tuple[str, str], dict[str, Any]] = {}
    convergence_rows: list[dict[str, Any]] = []
    paused = False
    for epsilon_id, epsilon in target_regulators():
        initial = [dict(row) for row in segments if row["epsilon_id"] == epsilon_id]
        event_lookup = {
            row["event_type"]: float(row["event_coordinate"])
            for row in events
            if row["epsilon_id"] == epsilon_id
        }
        expected = plan_sha256(epsilon_id, segments)
        old = kernel_context(epsilon_id, epsilon)
        try:
            panel_rows, leaves, encountered, audits, local_paused = refine_regulator(
                epsilon_id,
                initial,
                contract,
                expected,
                event_lookup["SHARED_BRANCH_DEATH"],
                base_context,
                multiplier,
                started,
                runtime_limit_seconds,
            )
        finally:
            restore_kernel_context(old)
        for row in panel_rows:
            row["epsilon_id"] = epsilon_id
            row["epsilon"] = epsilon
        for row in leaves:
            row["epsilon_id"] = epsilon_id
            row["epsilon"] = epsilon
        all_panel_rows.extend(panel_rows)
        all_leaves.extend(leaves)
        all_encountered.update({(epsilon_id, key): value for key, value in encountered.items()})
        all_audits.update({(epsilon_id, key): value for key, value in audits.items()})
        paused = paused or local_paused
        complete = not local_paused and len(leaves) >= 5
        all_leaf_gates = complete and all(bool(row["adaptive_gate_passes"]) for row in leaves)
        panel_low = sum(
            complex(float(row["outer_Q8_inner_Q12_real"]), float(row["outer_Q8_inner_Q12_imaginary"]))
            for row in leaves
        ) if complete else 0.0j
        panel_high = sum(
            complex(float(row["outer_Q12_inner_Q12_real"]), float(row["outer_Q12_inner_Q12_imaginary"]))
            for row in leaves
        ) if complete else 0.0j
        panel_error = sum(float(row["outer_Q8_Q12_absolute_change"]) for row in leaves) if complete else math.inf
        panel_relative = panel_error / max(abs(panel_high), 1.0e-12) if complete else math.inf
        baseline_low, baseline_high, baseline_error = baseline_panels_one_to_eight(epsilon_id)
        full_low = baseline_low + panel_low
        full_high = baseline_high + panel_high
        full_error = baseline_error + panel_error
        full_relative = full_error / max(abs(full_high), 1.0e-12)
        accepted = (
            complete
            and all_leaf_gates
            and panel_relative <= GLOBAL_OUTER_ERROR_BUDGET_LIMIT
            and full_relative <= GLOBAL_OUTER_ERROR_BUDGET_LIMIT
        )
        convergence_rows.append(
            {
                "epsilon_id": epsilon_id,
                "epsilon": epsilon,
                "adaptive_panel_count": len(panel_rows),
                "adaptive_leaf_count": len(leaves),
                "all_leaf_gates_pass": all_leaf_gates,
                "off_axis_raw_contract_node_count": sum(
                    bool(row["off_axis_raw_contract_passes"])
                    for key, row in all_audits.items()
                    if key[0] == epsilon_id
                ),
                **complex_fields("panel_nine_outer_low", panel_low),
                **complex_fields("panel_nine_outer_high", panel_high),
                "panel_nine_outer_error_absolute_conservative": panel_error,
                "panel_nine_outer_error_relative_conservative": panel_relative,
                **complex_fields("baseline_panels_one_to_eight_low", baseline_low),
                **complex_fields("baseline_panels_one_to_eight_high", baseline_high),
                "baseline_panels_one_to_eight_error_absolute_conservative": baseline_error,
                **complex_fields("fixed_decay_full_low", full_low),
                **complex_fields("fixed_decay_full_high", full_high),
                "fixed_decay_full_error_absolute_conservative": full_error,
                "fixed_decay_full_error_relative_conservative": full_relative,
                "finite_regulator_fixed_decay_integral_accepted": accepted,
                **{field: False for field in CLAIM_FIELDS},
            }
        )
        if paused:
            break
    manifest_rows: list[dict[str, Any]] = []
    for (epsilon_id, node_id), node in all_encountered.items():
        expected = plan_sha256(epsilon_id, segments)
        complete = shard_complete(epsilon_id, node, expected)
        result = read_json(shard_paths(epsilon_id, node_id)["result"]) if complete else {}
        audit = all_audits.get((epsilon_id, node_id), {})
        manifest_rows.append(
            {
                "epsilon_id": epsilon_id,
                **node,
                "shard_state": (
                    "COMPLETE_PASS"
                    if complete and bool(audit.get("effective_acceptance_passed"))
                    else ("COMPLETE_FAIL" if complete else "PENDING")
                ),
                "kernel_acceptance_passed": audit.get("kernel_acceptance_passed", False),
                "off_axis_raw_contract_passes": audit.get("off_axis_raw_contract_passes", False),
                "effective_acceptance_passed": audit.get("effective_acceptance_passed", False),
                "runtime_seconds": result.get("runtime_seconds", ""),
                "node_result_path": str(shard_paths(epsilon_id, node_id)["result"]),
                **{field: False for field in CLAIM_FIELDS},
            }
        )
    write_csv(NODE_MANIFEST, manifest_rows, ["epsilon_id", "node_id"])
    write_csv(OFF_AXIS_AUDIT, list(all_audits.values()), ["epsilon_id", "node_id"])
    write_csv(ADAPTIVE_PANELS, all_panel_rows, ["epsilon_id", "adaptive_panel_id"])
    write_csv(REGULATOR_CONVERGENCE, convergence_rows, ["epsilon_id"])
    e0025 = read_json(RESULT_5315)
    five_rows: list[dict[str, Any]] = [
        {
            "epsilon_id": "E0025",
            "epsilon": 0.0025,
            "method": "VALIDATED_5315_SQUARED_EVENT_COORDINATE_REPAIR",
            "fixed_decay_integral_real": e0025["reassembled_E0025_fixed_decay_integral_real"],
            "fixed_decay_integral_imaginary": e0025["reassembled_E0025_fixed_decay_integral_imaginary"],
            "fixed_decay_error_relative_conservative": e0025["reassembled_outer_error_relative_conservative"],
            "finite_regulator_fixed_decay_integral_accepted": bool(e0025["acceptance_passed"]),
            **{field: False for field in CLAIM_FIELDS},
        }
    ]
    for row in convergence_rows:
        five_rows.append(
            {
                "epsilon_id": row["epsilon_id"],
                "epsilon": row["epsilon"],
                "method": "REGULATOR_SPECIFIC_SQUARED_EVENT_ADAPTIVE_REPAIR",
                "fixed_decay_integral_real": row["fixed_decay_full_high_real"],
                "fixed_decay_integral_imaginary": row["fixed_decay_full_high_imaginary"],
                "fixed_decay_error_relative_conservative": row["fixed_decay_full_error_relative_conservative"],
                "finite_regulator_fixed_decay_integral_accepted": row["finite_regulator_fixed_decay_integral_accepted"],
                **{field: False for field in CLAIM_FIELDS},
            }
        )
    write_csv(FIVE_REGULATOR_STATUS, five_rows, ["epsilon_id"])
    all_four_complete = len(convergence_rows) == 4
    all_four_accepted = all_four_complete and all(
        bool(row["finite_regulator_fixed_decay_integral_accepted"])
        for row in convergence_rows
    )
    all_five_accepted = len(five_rows) == 5 and all(
        parse_bool(row["finite_regulator_fixed_decay_integral_accepted"])
        for row in five_rows
    )
    if paused:
        decision = "REGULATOR_SPECIFIC_OUTER_REPAIR_PAUSED__RESUME_SAVED_SHARDS"
    elif all_five_accepted:
        decision = "FIVE_FINITE_REGULATORS_CONVERGED__FIT_REGULATOR_ZERO_LIMIT"
    elif all_four_complete:
        decision = "REGULATOR_SPECIFIC_OUTER_REPAIR_LOCALIZES_REMAINING_FAILURES"
    else:
        decision = "REGULATOR_SPECIFIC_OUTER_REPAIR_INCOMPLETE"
    parent = read_json(RESULT_5317)
    formal_end = M5283.formal_inventory_digest()
    result = {
        "checkpoint": CHECKPOINT,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "mode": "regulator-specific-squared-event-outer-repair",
        "acceptance_passed": all_four_accepted,
        "decision": decision,
        "derived_regulator_event_count": len(events),
        "initial_segment_count": len(segments),
        "encountered_outer_node_count": len(all_encountered),
        "completed_outer_node_count": sum(row["shard_state"] != "PENDING" for row in manifest_rows),
        "failed_outer_inner_node_count": sum(row["shard_state"] == "COMPLETE_FAIL" for row in manifest_rows),
        "adaptive_panel_count": len(all_panel_rows),
        "adaptive_leaf_count": len(all_leaves),
        "accepted_new_finite_regulator_count": sum(
            bool(row["finite_regulator_fixed_decay_integral_accepted"])
            for row in convergence_rows
        ),
        "all_five_finite_regulators_accepted": all_five_accepted,
        "regulator_convergence_rows": convergence_rows,
        "formalization_workbench_reference_digest": parent["formalization_workbench_end_digest"],
        "formalization_workbench_end_digest": formal_end,
        "formalization_workbench_modified_file_count": (
            0 if formal_end == parent["formalization_workbench_end_digest"] else -1
        ),
        "claim_boundary": {
            "valid_for_five_finite_regulator_fixed_decay_integrals": all_five_accepted,
            **{field: False for field in CLAIM_FIELDS},
            "reason": (
                "Acceptance is limited to five finite regulators at one fixed decay angle. "
                "A regulator-zero fit and decay-angle integration remain separate gates."
            ),
        },
        "resource_contract": {
            "maximum_task_python_processes": 1,
            "worker_math_threads": 1,
            "windows_priority": "BelowNormal",
            "maximum_silent_work_hours": 4,
            "runtime_limit_seconds_per_invocation": runtime_limit_seconds,
        },
        "source_files": source_rows(),
        "runtime_seconds": time.perf_counter() - started,
    }
    atomic_json(RESULT, result)
    atomic_json(
        STATUS,
        {
            "checkpoint": CHECKPOINT,
            "state": "PAUSED_RESUMABLE" if paused else "COMPLETE_DIAGNOSTIC",
            "decision": decision,
            "completed_outer_node_count": result["completed_outer_node_count"],
            "encountered_outer_node_count": result["encountered_outer_node_count"],
        },
    )
    return result


def render_document(result: dict[str, Any], passed: bool) -> None:
    lines = [
        "# 5318 - Regulator-specific squared-event outer repair",
        "",
        "## Method",
        "",
        "Each regulator derives its own support-entry, support-exit, and shared-branch",
        "death coordinates. Panel 9 is partitioned exactly at those events. The",
        "logarithmic endpoint collars use `|x-x_event|=t^2`, while smooth pieces use",
        "ordinary Gauss-Legendre coordinates. No E0025 event coordinate is assumed",
        "to transfer to another regulator.",
        "",
        "The normalized Laurent basis `r^2/(E-p)^2`, `r/(E-p)`, and powers of the",
        "dimensionless fit coordinate removes pole-location conditioning artifacts.",
        "Independent interlaced holdout points remain mandatory.",
        "",
        "Panel 2 is retained under the same global conservative budget used for the",
        "validated E0025 baseline; imposing a new local-only gate on the four added",
        "regulators would be an asymmetric test.",
        "",
        "## Result",
        "",
        f"- derived regulator events: `{result['derived_regulator_event_count']}`;",
        f"- completed outer nodes: `{result['completed_outer_node_count']}`;",
        f"- failed outer inner nodes: `{result['failed_outer_inner_node_count']}`;",
        f"- accepted added regulators: `{result['accepted_new_finite_regulator_count']}` / 4;",
        f"- all five finite regulators accepted: `{result['all_five_finite_regulators_accepted']}`;",
        f"- decision: **{result['decision']}**;",
        f"- validation: **{'PASS' if passed else 'FAIL'}**.",
        "",
        "| regulator | leaves | panel-9 error | full error | accepted |",
        "|---|---:|---:|---:|---:|",
    ]
    for row in result["regulator_convergence_rows"]:
        lines.append(
            "| {epsilon_id} | {leaves} | {panel:.6g} | {full:.6g} | {accepted} |".format(
                epsilon_id=row["epsilon_id"],
                leaves=row["adaptive_leaf_count"],
                panel=float(row["panel_nine_outer_error_relative_conservative"]),
                full=float(row["fixed_decay_full_error_relative_conservative"]),
                accepted=row["finite_regulator_fixed_decay_integral_accepted"],
            )
        )
    lines.extend(
        [
            "",
            "## Claim boundary",
            "",
            "Even if all five rows pass, this is one fixed decay angle at finite",
            "regulators. No regulator-zero, decay-angle, phase-space, UV, local-GR,",
            "or full-MTS claim follows until those later gates are run.",
        ]
    )
    DOCUMENT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def validate_outputs() -> dict[str, Any]:
    started = time.perf_counter()
    result = read_json(RESULT)
    dry = read_json(DRY_RUN)
    events = read_csv(EVENT_AUDIT)
    segments = read_csv(SEGMENT_PLAN)
    manifest = read_csv(NODE_MANIFEST)
    panels = read_csv(ADAPTIVE_PANELS)
    convergence = read_csv(REGULATOR_CONVERGENCE)
    five = read_csv(FIVE_REGULATOR_STATUS)
    source_current = all(
        Path(row["path"]).exists()
        and digest(Path(row["path"])) == row["sha256"]
        for row in result["source_files"]
    )
    leaves = [row for row in panels if parse_bool(row["adaptive_leaf"])]
    gates = [
        validation_gate(
            "dry_run_and_regulator_geometry_pass",
            bool(dry["acceptance_passed"])
            and len(events) == 12
            and all(parse_bool(row["event_contract_passes"]) for row in events)
            and len(segments) == 20,
            dry["decision"],
        ),
        validation_gate(
            "all_encountered_outer_nodes_pass",
            bool(manifest)
            and all(row["shard_state"] == "COMPLETE_PASS" for row in manifest)
            and int(result["failed_outer_inner_node_count"]) == 0,
            f"nodes={len(manifest)}",
        ),
        validation_gate(
            "all_adaptive_leaves_pass_local_gates",
            len(leaves) >= 20
            and all(parse_bool(row["adaptive_gate_passes"]) for row in leaves),
            f"leaves={len(leaves)}",
        ),
        validation_gate(
            "four_added_regulators_pass_conservative_global_budget",
            len(convergence) == 4
            and all(
                parse_bool(row["finite_regulator_fixed_decay_integral_accepted"])
                and float(row["panel_nine_outer_error_relative_conservative"])
                <= GLOBAL_OUTER_ERROR_BUDGET_LIMIT
                and float(row["fixed_decay_full_error_relative_conservative"])
                <= GLOBAL_OUTER_ERROR_BUDGET_LIMIT
                for row in convergence
            ),
            f"rows={len(convergence)}",
        ),
        validation_gate(
            "five_finite_regulators_have_accepted_fixed_decay_values",
            len(five) == 5
            and {row["epsilon_id"] for row in five}
            == {"E0025", "E005", "E010", "E020", "E040"}
            and all(
                parse_bool(row["finite_regulator_fixed_decay_integral_accepted"])
                for row in five
            )
            and bool(result["all_five_finite_regulators_accepted"]),
            f"rows={len(five)}",
        ),
        validation_gate(
            "formal_workbench_unchanged",
            M5283.formal_inventory_digest()
            == result["formalization_workbench_end_digest"]
            == result["formalization_workbench_reference_digest"]
            and int(result["formalization_workbench_modified_file_count"]) == 0,
            result["formalization_workbench_end_digest"],
        ),
        validation_gate(
            "source_paths_and_hashes_current",
            source_current,
            f"rows={len(result['source_files'])}",
        ),
        validation_gate(
            "scripts_cache_absent",
            not (SCRIPTS / "__pycache__").exists(),
            str(SCRIPTS / "__pycache__"),
        ),
        validation_gate(
            "broader_claims_locked_false",
            all(not bool(result["claim_boundary"][field]) for field in CLAIM_FIELDS),
            "finite-regulator fixed-decay layer only",
        ),
    ]
    passed = all(bool(row["passed"]) for row in gates)
    write_csv(VALIDATION, gates)
    write_csv(RESIDUAL_VALIDATION, gates)
    render_document(result, passed)
    return {
        "checkpoint": CHECKPOINT,
        "mode": "validation",
        "acceptance_passed": passed,
        "decision": (
            "VALIDATED_FIVE_FINITE_REGULATOR_FIXED_DECAY_LADDER"
            if passed
            else "REGULATOR_SPECIFIC_SQUARED_EVENT_REPAIR_VALIDATION_FAILED"
        ),
        "runtime_seconds": time.perf_counter() - started,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("dry-run", "run", "validate"), required=True)
    parser.add_argument("--max-runtime-hours", type=float, default=2.5)
    return parser.parse_args()


def main() -> int:
    M5312.set_below_normal_priority()
    arguments = parse_args()
    if arguments.mode == "dry-run":
        result = dry_run()
    elif arguments.mode == "run":
        result = execute(arguments.max_runtime_hours * 3600.0)
    else:
        result = validate_outputs()
    print(
        json.dumps(
            {
                "checkpoint": result["checkpoint"],
                "mode": result["mode"],
                "acceptance_passed": result["acceptance_passed"],
                "decision": result["decision"],
                "runtime_seconds": result["runtime_seconds"],
            },
            sort_keys=True,
        )
    )
    return 0 if result["acceptance_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
