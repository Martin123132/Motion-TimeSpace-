from __future__ import annotations

import argparse
import csv
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
SOURCE = FUNCTIONAL_RG / "5315"
SHARDS = SOURCE / "shards"

SCRIPT_5314 = (
    SCRIPTS / "Y5_R2FR_5314_refined_simple_pole_endpoint_collar_integrator.py"
)
RESULT_5314 = (
    FUNCTIONAL_RG / "5314" / "refined_simple_pole_endpoint_collar_result.json"
)
PANELS_5314 = FUNCTIONAL_RG / "5314" / "endpoint_collar_adaptive_outer_panels.csv"
MANIFEST_5314 = FUNCTIONAL_RG / "5314" / "endpoint_collar_node_manifest.csv"
EVENTS_5314 = FUNCTIONAL_RG / "5314" / "shared_branch_outer_events.csv"
SUPPORT_EVENTS_5313 = FUNCTIONAL_RG / "5313" / "P9_material_pole_support_events.csv"
CONTRACT_5312 = FUNCTIONAL_RG / "5312" / "reduced_fixed_decay_cubature_contract.csv"

DRY_RUN = SOURCE / "squared_event_coordinate_collar_repair_dry_run.json"
EVENT_AUDIT = SOURCE / "refined_support_event_linear_crossing_audit.csv"
REPAIR_PLAN = SOURCE / "squared_event_collar_repair_plan.csv"
NODE_MANIFEST = SOURCE / "squared_event_node_manifest.csv"
ALL_POLE_FITS = SOURCE / "squared_event_refined_pole_fits.csv"
ALL_CELL_INTEGRALS = SOURCE / "squared_event_cell_integrals.csv"
OFF_AXIS_AUDIT = SOURCE / "off_axis_raw_contour_contracts.csv"
SEGMENT_CONVERGENCE = SOURCE / "squared_event_segment_convergence.csv"
LEAF_CONVERGENCE = SOURCE / "squared_event_leaf_convergence.csv"
CONVERGENCE = SOURCE / "repaired_E0025_outer_convergence.csv"
RESULT = SOURCE / "squared_event_coordinate_collar_repair_result.json"
VALIDATION = SOURCE / "squared_event_coordinate_collar_repair_validation.csv"
RESIDUAL_VALIDATION = RESIDUALS / "P8_Y5_BRR545_5315_VALIDATION.csv"
STATUS = SOURCE / "status.json"
DOCUMENT = POST / "5315-Y5-R2FR-squared-event-coordinate-collar-repair.md"

CHECKPOINT = 5315
PARENT_CHECKPOINT = 5314
MARKER = "MTS_5315_SQUARED_EVENT_COORDINATE_COLLAR_REPAIR"
REVISION = "squared-event-coordinate-collar-repair-v1"
NODE_REVISION = "squared-event-coordinate-collar-node-v1"
EVENT_AUDIT_REVISION = "support-event-secant-refinement-v1"
ADJUDICATION_REVISION = "off-axis-raw-contour-contract-v1"
TRANSFORM_ORDERS = (8, 12)
LOCAL_REPAIR_CHANGE_LIMIT = 5.0e-3
GLOBAL_OUTER_ERROR_BUDGET_LIMIT = 1.0e-2
ROOT_GAP_TOLERANCE = 1.0e-12
ROOT_MAXIMUM_ITERATIONS = 10
MINIMUM_CROSSING_SLOPE = 1.0e-3
BOUNDARY_MATCH_TOLERANCE = 5.0e-13
JACOBIAN_CONSTANT_ERROR_LIMIT = 5.0e-13
MINIMUM_SEGMENT_WIDTH = 1.0e-15
OFF_AXIS_FLOAT_SEPARATION_MULTIPLIER = 100.0
OFF_AXIS_FIT_RADIUS_RATIO_MINIMUM = 100.0
OFF_AXIS_RAW_RELATIVE_CHANGE_LIMIT = 1.0e-8
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


M5314 = load_module("mts_5314_for_5315", SCRIPT_5314)
M5312 = M5314.M5312
M5283 = M5314.M5283
np = M5314.np
mp = M5314.mp


def read_json(path: Path) -> Any:
    return M5314.read_json(path)


def read_csv(path: Path) -> list[dict[str, str]]:
    return M5314.read_csv(path)


def write_csv(
    path: Path,
    rows: list[dict[str, Any]],
    fieldnames: list[str] | None = None,
) -> None:
    M5314.write_csv(path, rows, fieldnames)


def atomic_json(path: Path, value: Any) -> None:
    M5314.atomic_json(path, value)


def digest(path: Path) -> str:
    return M5314.digest(path)


def parse_bool(value: Any) -> bool:
    return M5314.parse_bool(value)


def complex_fields(prefix: str, value: complex) -> dict[str, float]:
    return M5314.complex_fields(prefix, value)


def relative_complex_change(first: complex, second: complex) -> float:
    return M5314.relative_complex_change(first, second)


def validation_gate(gate: str, passed: bool, detail: str) -> dict[str, Any]:
    return M5312.validation_gate(gate, passed, detail)


def failed_parent_leaves() -> list[dict[str, str]]:
    return [
        row
        for row in read_csv(PANELS_5314)
        if parse_bool(row["adaptive_leaf"])
        and not parse_bool(row["adaptive_gate_passes"])
    ]


def parent_is_complete() -> bool:
    result = read_json(RESULT_5314)
    manifest = read_csv(MANIFEST_5314)
    return (
        result["decision"]
        == "REFINED_POLE_COLLAR_LOCALIZES_REMAINING_OUTER_ENDPOINT_FAILURE"
        and int(result["failed_inner_node_count"]) == 0
        and bool(manifest)
        and all(row["shard_state"] == "COMPLETE_PASS" for row in manifest)
    )


def event_gap(
    coordinate: float,
    event_type: str,
    contract: list[dict[str, str]],
) -> dict[str, float]:
    cells = [
        M5312.cell_geometry(row, coordinate)
        for row in contract
        if int(row["x_panel_index"]) == M5314.TARGET_PANEL_INDEX
        and int(row["reduced_MC04_term_count"]) > 0
    ]
    branch = M5314.target_branch_row(coordinate, cells)
    if branch is None:
        raise RuntimeError(f"shared branch absent at support-event sample {coordinate}")
    pole = float(branch["pole_real"])
    if event_type == "SUPPORT_ENTRY":
        edge = float(branch["support_energy_upper"])
        edge_name = "support_energy_upper"
    elif event_type == "SUPPORT_EXIT":
        edge = float(branch["support_energy_lower"])
        edge_name = "support_energy_lower"
    else:
        raise ValueError(event_type)
    return {
        "coordinate": coordinate,
        "pole_real": pole,
        "support_edge": edge,
        "gap": pole - edge,
        "support_edge_name": edge_name,
    }


def event_audit_cache_current() -> bool:
    if not EVENT_AUDIT.exists():
        return False
    rows = read_csv(EVENT_AUDIT)
    return (
        len(rows) == 2
        and all(row.get("audit_revision") == EVENT_AUDIT_REVISION for row in rows)
        and all(row.get("contract_sha256") == digest(CONTRACT_5312) for row in rows)
        and all(
            row.get("source_support_events_sha256") == digest(SUPPORT_EVENTS_5313)
            for row in rows
        )
        and all(parse_bool(row.get("linear_crossing_contract_passes", False)) for row in rows)
    )


def refine_support_event(
    source: dict[str, str],
    contract: list[dict[str, str]],
) -> dict[str, Any]:
    event_type = source["event_type"]
    left = float(source["left_bracket_absolute_soft_cosine"])
    right = float(source["right_bracket_absolute_soft_cosine"])
    left_state = event_gap(left, event_type, contract)
    right_state = event_gap(right, event_type, contract)
    initial_left_gap = float(left_state["gap"])
    initial_right_gap = float(right_state["gap"])
    sign_change = initial_left_gap * initial_right_gap <= 0.0
    if not sign_change:
        raise RuntimeError(f"{event_type} source bracket does not straddle zero")
    evaluation_count = 2
    root_state: dict[str, float] = left_state
    for _ in range(ROOT_MAXIMUM_ITERATIONS):
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
        root_state = event_gap(candidate, event_type, contract)
        evaluation_count += 1
        root_gap = float(root_state["gap"])
        if abs(root_gap) <= ROOT_GAP_TOLERANCE:
            break
        if float(left_state["gap"]) * root_gap <= 0.0:
            right = candidate
            right_state = root_state
        else:
            left = candidate
            left_state = root_state
    crossing_slope = (
        initial_right_gap - initial_left_gap
    ) / (
        float(source["right_bracket_absolute_soft_cosine"])
        - float(source["left_bracket_absolute_soft_cosine"])
    )
    passes = (
        sign_change
        and abs(crossing_slope) >= MINIMUM_CROSSING_SLOPE
        and abs(float(root_state["gap"])) <= ROOT_GAP_TOLERANCE
    )
    return {
        "event_id": source["event_id"],
        "event_type": event_type,
        "audit_revision": EVENT_AUDIT_REVISION,
        "source_event_coordinate": source["event_absolute_soft_cosine"],
        "source_left_bracket": source["left_bracket_absolute_soft_cosine"],
        "source_right_bracket": source["right_bracket_absolute_soft_cosine"],
        "refined_event_coordinate": root_state["coordinate"],
        "refined_pole_real": root_state["pole_real"],
        "refined_support_edge": root_state["support_edge"],
        "support_edge_name": root_state["support_edge_name"],
        "refined_edge_gap": root_state["gap"],
        "initial_left_gap": initial_left_gap,
        "initial_right_gap": initial_right_gap,
        "crossing_slope": crossing_slope,
        "crossing_slope_magnitude": abs(crossing_slope),
        "evaluation_count": evaluation_count,
        "sign_change_present": sign_change,
        "linear_crossing_contract_passes": passes,
        "contract_sha256": digest(CONTRACT_5312),
        "source_support_events_sha256": digest(SUPPORT_EVENTS_5313),
        **{field: False for field in CLAIM_FIELDS},
    }


def refined_support_events() -> list[dict[str, Any]]:
    SOURCE.mkdir(parents=True, exist_ok=True)
    if event_audit_cache_current():
        return read_csv(EVENT_AUDIT)
    contract = read_csv(CONTRACT_5312)
    rows = [
        refine_support_event(row, contract)
        for row in read_csv(SUPPORT_EVENTS_5313)
        if row["event_type"] in {"SUPPORT_ENTRY", "SUPPORT_EXIT"}
    ]
    write_csv(EVENT_AUDIT, rows, ["event_id", "event_type"])
    return rows


def build_repair_plan(event_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    events = {row["event_type"]: row for row in event_rows}
    approximate = {
        row["event_type"]: float(row["event_absolute_soft_cosine"])
        for row in read_csv(EVENTS_5314)
        if row["event_type"] in events
    }
    rows: list[dict[str, Any]] = []
    for leaf in failed_parent_leaves():
        lower = float(leaf["lower_absolute_soft_cosine"])
        upper = float(leaf["upper_absolute_soft_cosine"])
        matches = [
            event_type
            for event_type, coordinate in approximate.items()
            if abs(upper - coordinate) <= BOUNDARY_MATCH_TOLERANCE
        ]
        if len(matches) != 1:
            raise RuntimeError(
                f"failed leaf {leaf['adaptive_panel_id']} does not match one support event"
            )
        event_type = matches[0]
        event = events[event_type]
        refined = float(event["refined_event_coordinate"])
        if not lower < refined < upper:
            raise RuntimeError(
                f"refined {event_type} coordinate is outside {leaf['adaptive_panel_id']}"
            )
        pieces = (
            ("L", lower, refined, "EVENT_AT_UPPER", -1),
            ("R", refined, upper, "EVENT_AT_LOWER", 1),
        )
        for suffix, segment_lower, segment_upper, orientation, direction in pieces:
            width = segment_upper - segment_lower
            if width <= MINIMUM_SEGMENT_WIDTH:
                continue
            rows.append(
                {
                    "repair_id": f"{leaf['adaptive_panel_id']}_{event['event_id']}",
                    "segment_id": f"{leaf['adaptive_panel_id']}_{event['event_id']}_{suffix}",
                    "parent_leaf_id": leaf["adaptive_panel_id"],
                    "event_id": event["event_id"],
                    "event_type": event_type,
                    "source_event_coordinate": event["source_event_coordinate"],
                    "refined_event_coordinate": refined,
                    "segment_lower_absolute_soft_cosine": segment_lower,
                    "segment_upper_absolute_soft_cosine": segment_upper,
                    "segment_width": width,
                    "transform_orientation": orientation,
                    "transform_direction": direction,
                    "transform_equation": (
                        "x=x_event-t^2; dx=2t dt"
                        if direction < 0
                        else "x=x_event+t^2; dx=2t dt"
                    ),
                    "logarithmic_endpoint_derivation": (
                        "p-Eedge=kappa(x-x_event)+O((x-x_event)^2), "
                        "so R log(Eedge-p)=A log|x-x_event|+regular; "
                        "|x-x_event|=t^2 gives 2tF(x_event+/-t^2)"
                    ),
                    "valid_for_E0025_fixed_decay_outer_soft_integral": False,
                    **{field: False for field in CLAIM_FIELDS},
                }
            )
    write_csv(REPAIR_PLAN, rows, ["repair_id", "segment_id"])
    return rows


def dry_run() -> dict[str, Any]:
    started = time.perf_counter()
    required = [
        SCRIPT_5314,
        RESULT_5314,
        PANELS_5314,
        MANIFEST_5314,
        EVENTS_5314,
        SUPPORT_EVENTS_5313,
        CONTRACT_5312,
    ]
    missing = [str(path) for path in required if not path.exists()]
    event_rows = refined_support_events() if not missing else []
    repair_rows = build_repair_plan(event_rows) if event_rows else []
    failures = failed_parent_leaves() if not missing else []
    repaired_leaf_ids = {row["parent_leaf_id"] for row in repair_rows}
    failure_ids = {row["adaptive_panel_id"] for row in failures}
    accepted = (
        not missing
        and parent_is_complete()
        and len(failures) == 2
        and len(event_rows) == 2
        and all(parse_bool(row["linear_crossing_contract_passes"]) for row in event_rows)
        and repaired_leaf_ids == failure_ids
        and len(repair_rows) == 4
        and all(float(row["segment_width"]) > 0.0 for row in repair_rows)
    )
    result = {
        "checkpoint": CHECKPOINT,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "mode": "dry-run",
        "acceptance_passed": accepted,
        "decision": (
            "DRY_RUN_ACCEPTED__RUN_SQUARED_EVENT_COORDINATE_REPAIR"
            if accepted
            else "SQUARED_EVENT_COORDINATE_REPAIR_DRY_RUN_BLOCKED"
        ),
        "missing_paths": missing,
        "parent_complete": parent_is_complete() if not missing else False,
        "parent_failed_leaf_count": len(failures),
        "refined_support_event_count": len(event_rows),
        "repair_segment_count": len(repair_rows),
        "derivation": {
            "pole_edge_crossing": "p(x)-Eedge(x)=kappa(x-x_event)+O((x-x_event)^2), kappa!=0",
            "outer_singular_part": "F(x)=A log|x-x_event|+regular",
            "coordinate_map": "|x-x_event|=t^2, |dx|=2t dt",
            "transformed_limit": "2tF(x_event+/-t^2)=4A t log(t)+O(t), integrable and zero at t=0",
            "unbiasedness": "the map and Jacobian are an exact change of variables; no closure term is added",
        },
        "claim_boundary": {
            "valid_for_E0025_fixed_decay_outer_soft_integral": False,
            **{field: False for field in CLAIM_FIELDS},
        },
        "runtime_seconds": time.perf_counter() - started,
    }
    atomic_json(DRY_RUN, result)
    return result


def plan_sha256(repair_rows: list[dict[str, Any]]) -> str:
    payload = {
        "revision": REVISION,
        "node_revision": NODE_REVISION,
        "parent_result_sha256": digest(RESULT_5314),
        "contract_sha256": digest(CONTRACT_5312),
        "transform_orders": TRANSFORM_ORDERS,
        "repair_rows": [
            {
                key: row[key]
                for key in (
                    "segment_id",
                    "refined_event_coordinate",
                    "segment_lower_absolute_soft_cosine",
                    "segment_upper_absolute_soft_cosine",
                    "transform_direction",
                )
            }
            for row in repair_rows
        ],
    }
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()


def transformed_nodes(repair_rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for segment in repair_rows:
        event = float(segment["refined_event_coordinate"])
        width = float(segment["segment_width"])
        direction = int(segment["transform_direction"])
        t_max = math.sqrt(width)
        for order in TRANSFORM_ORDERS:
            nodes, weights = np.polynomial.legendre.leggauss(order)
            for index, (node, weight) in enumerate(zip(nodes, weights), start=1):
                t_coordinate = 0.5 * t_max * (1.0 + float(node))
                coordinate = event + direction * t_coordinate * t_coordinate
                mapped_weight = (
                    0.5 * t_max * float(weight) * 2.0 * t_coordinate
                )
                rows.append(
                    {
                        "node_id": (
                            f"P09_{segment['segment_id']}_SQ_"
                            f"Q{order:02d}_N{index:02d}"
                        ),
                        "x_panel_index": M5314.TARGET_PANEL_INDEX,
                        "outer_order": order,
                        "local_node_index": index,
                        "repair_id": segment["repair_id"],
                        "segment_id": segment["segment_id"],
                        "parent_leaf_id": segment["parent_leaf_id"],
                        "event_id": segment["event_id"],
                        "event_type": segment["event_type"],
                        "refined_event_coordinate": event,
                        "transform_coordinate_t": t_coordinate,
                        "transform_jacobian": 2.0 * t_coordinate,
                        "transform_direction": direction,
                        "lower_absolute_soft_cosine": segment[
                            "segment_lower_absolute_soft_cosine"
                        ],
                        "upper_absolute_soft_cosine": segment[
                            "segment_upper_absolute_soft_cosine"
                        ],
                        "absolute_soft_cosine": coordinate,
                        "mapped_outer_weight": mapped_weight,
                        **{field: False for field in CLAIM_FIELDS},
                    }
                )
    return rows


def shard_paths(node_id: str) -> dict[str, Path]:
    root = SHARDS / node_id
    return {
        "root": root,
        "fits": root / "refined_pole_fits.csv",
        "integrals": root / "cell_integrals.csv",
        "result": root / "result.json",
    }


def shard_complete(node: dict[str, Any], expected_plan_sha256: str) -> bool:
    paths = shard_paths(node["node_id"])
    if not all(path.exists() for key, path in paths.items() if key != "root"):
        return False
    try:
        result = read_json(paths["result"])
        read_csv(paths["fits"])
        read_csv(paths["integrals"])
    except Exception:
        return False
    return (
        result.get("node_revision") == NODE_REVISION
        and result.get("node_plan_sha256") == expected_plan_sha256
        and result.get("node_id") == node["node_id"]
        and bool(result.get("node_complete"))
    )


def off_axis_raw_contour_contract(
    node: dict[str, Any], result: dict[str, Any]
) -> dict[str, Any]:
    paths = shard_paths(node["node_id"])
    final_fits = [
        row
        for row in read_csv(paths["fits"])
        if row.get("fit_row_type") == "FINAL_REFINED_SIMPLE_POLE_FIT"
    ]
    kernel_passes = bool(result["acceptance_passed"])
    fit_data_present = len(final_fits) == len(M5314.FIT_SCALES)
    minimum_imaginary_separation = (
        min(abs(float(row["refined_pole_imaginary"])) for row in final_fits)
        if fit_data_present
        else 0.0
    )
    pole_scale = (
        max(1.0, max(abs(float(row["refined_pole_real"])) for row in final_fits))
        if fit_data_present
        else 1.0
    )
    floating_separation_floor = (
        OFF_AXIS_FLOAT_SEPARATION_MULTIPLIER
        * math.sqrt(float(np.finfo(float).eps))
        * pole_scale
    )
    maximum_fit_radius = (
        max(float(row["fit_radius"]) for row in final_fits)
        if fit_data_present
        else math.inf
    )
    separation_to_fit_radius_ratio = (
        minimum_imaginary_separation / maximum_fit_radius
        if maximum_fit_radius > 0.0 and math.isfinite(maximum_fit_radius)
        else 0.0
    )
    maximum_fit_residual = (
        max(float(row["fit_relative_residual"]) for row in final_fits)
        if fit_data_present
        else math.inf
    )
    maximum_residue_scale_change = (
        max(float(row["residue_fit_scale_relative_change"]) for row in final_fits)
        if fit_data_present
        else math.inf
    )
    minimum_second_order_suppression_ratio = (
        min(float(row["second_order_suppression_ratio"]) for row in final_fits)
        if fit_data_present
        else math.inf
    )
    maximum_residue_magnitude = (
        max(
            math.hypot(
                float(row["simple_residue_R1_real"]),
                float(row["simple_residue_R1_imaginary"]),
            )
            for row in final_fits
        )
        if fit_data_present
        else math.inf
    )
    branch_structure_is_single = fit_data_present and all(
        int(row["fit_mask_state_count"]) == 1
        and int(row["fit_orientation_count"]) == 1
        and int(row["fit_label_count"]) == 1
        for row in final_fits
    )
    all_non_R2_fit_gates_pass = (
        fit_data_present
        and maximum_fit_residual <= M5314.FIT_RELATIVE_RESIDUAL_LIMIT
        and maximum_residue_scale_change <= M5314.RESIDUE_SCALE_CHANGE_LIMIT
        and branch_structure_is_single
    )
    R2_gate_is_the_only_failed_fit_gate = (
        all_non_R2_fit_gates_pass
        and minimum_second_order_suppression_ratio
        > M5314.SECOND_ORDER_SUPPRESSION_LIMIT
    )
    raw_inner_convergence_passes = (
        float(result["inner_Q8_Q12_relative_change"])
        <= OFF_AXIS_RAW_RELATIVE_CHANGE_LIMIT
        and float(result["inner_energy_error_budget_relative"])
        <= OFF_AXIS_RAW_RELATIVE_CHANGE_LIMIT
    )
    contour_separation_passes = (
        minimum_imaginary_separation >= floating_separation_floor
        and separation_to_fit_radius_ratio >= OFF_AXIS_FIT_RADIUS_RATIO_MINIMUM
    )
    override_passes = (
        not kernel_passes
        and bool(result["target_branch_exists"])
        and bool(result["target_branch_inside_support"])
        and not bool(result["refined_pole_subtraction_applied"])
        and int(result["inactive_selected_term_count"]) == 0
        and R2_gate_is_the_only_failed_fit_gate
        and raw_inner_convergence_passes
        and contour_separation_passes
    )
    return {
        "node_id": node["node_id"],
        "segment_id": node["segment_id"],
        "adjudication_revision": ADJUDICATION_REVISION,
        "kernel_acceptance_passed": kernel_passes,
        "off_axis_raw_contract_evaluated": not kernel_passes,
        "fit_data_present": fit_data_present,
        "minimum_imaginary_contour_separation": minimum_imaginary_separation,
        "floating_separation_floor": floating_separation_floor,
        "maximum_fit_radius": maximum_fit_radius,
        "separation_to_fit_radius_ratio": separation_to_fit_radius_ratio,
        "maximum_fit_residual": maximum_fit_residual,
        "maximum_residue_scale_change": maximum_residue_scale_change,
        "minimum_second_order_suppression_ratio": minimum_second_order_suppression_ratio,
        "maximum_residue_magnitude": maximum_residue_magnitude,
        "simple_pole_kernel_upper_bound": (
            maximum_residue_magnitude / minimum_imaginary_separation
            if minimum_imaginary_separation > 0.0
            else math.inf
        ),
        "branch_structure_is_single": branch_structure_is_single,
        "all_non_R2_fit_gates_pass": all_non_R2_fit_gates_pass,
        "R2_gate_is_the_only_failed_fit_gate": R2_gate_is_the_only_failed_fit_gate,
        "raw_inner_Q8_Q12_relative_change": result["inner_Q8_Q12_relative_change"],
        "raw_inner_error_budget_relative": result[
            "inner_energy_error_budget_relative"
        ],
        "raw_inner_convergence_passes": raw_inner_convergence_passes,
        "contour_separation_passes": contour_separation_passes,
        "off_axis_raw_contract_passes": override_passes,
        "effective_acceptance_passed": kernel_passes or override_passes,
        "derivation": (
            "For real E and p=a+ib, |E-p|>=|b|.  The failed R2 gate is "
            "required only to justify pole subtraction; when subtraction is not "
            "used, nonzero contour separation plus direct raw Q8/Q12 convergence "
            "provides the applicable contract."
        ),
        **{field: False for field in CLAIM_FIELDS},
    }


def integrate_transformed_node(
    node: dict[str, Any],
    contract: list[dict[str, str]],
    expected_plan_sha256: str,
    branch_death: float,
    base_context: dict[str, Any],
    multiplier: float,
) -> dict[str, Any]:
    old_shards = M5314.SHARDS
    old_checkpoint = M5314.CHECKPOINT
    old_node_revision = M5314.NODE_REVISION
    try:
        M5314.SHARDS = SHARDS
        M5314.CHECKPOINT = CHECKPOINT
        M5314.NODE_REVISION = NODE_REVISION
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
                "parent_kernel_checkpoint": PARENT_CHECKPOINT,
                "repair_id": node["repair_id"],
                "segment_id": node["segment_id"],
                "parent_leaf_id": node["parent_leaf_id"],
                "event_id": node["event_id"],
                "event_type": node["event_type"],
                "refined_event_coordinate": node["refined_event_coordinate"],
                "transform_coordinate_t": node["transform_coordinate_t"],
                "transform_jacobian": node["transform_jacobian"],
                "transform_direction": node["transform_direction"],
                "decision": (
                    "SQUARED_EVENT_COORDINATE_NODE_ACCEPTED"
                    if result["acceptance_passed"]
                    else "SQUARED_EVENT_COORDINATE_NODE_REQUIRES_REFINEMENT"
                ),
            }
        )
        atomic_json(shard_paths(node["node_id"])["result"], result)
        return result
    finally:
        M5314.SHARDS = old_shards
        M5314.CHECKPOINT = old_checkpoint
        M5314.NODE_REVISION = old_node_revision


def node_manifest(
    nodes: list[dict[str, Any]], expected_plan_sha256: str
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for node in nodes:
        complete = shard_complete(node, expected_plan_sha256)
        result = read_json(shard_paths(node["node_id"])["result"]) if complete else {}
        audit = off_axis_raw_contour_contract(node, result) if complete else {}
        rows.append(
            {
                **node,
                "shard_state": (
                    "COMPLETE_PASS"
                    if complete and bool(audit["effective_acceptance_passed"])
                    else ("COMPLETE_FAIL" if complete else "PENDING")
                ),
                "kernel_acceptance_passed": audit.get(
                    "kernel_acceptance_passed", False
                ),
                "off_axis_raw_contract_passes": audit.get(
                    "off_axis_raw_contract_passes", False
                ),
                "effective_acceptance_passed": audit.get(
                    "effective_acceptance_passed", False
                ),
                "runtime_seconds": result.get("runtime_seconds", ""),
                "node_result_path": str(shard_paths(node["node_id"])["result"]),
            }
        )
    return rows


def aggregate_shards(
    manifest: list[dict[str, Any]],
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    fits: list[dict[str, str]] = []
    integrals: list[dict[str, str]] = []
    for row in manifest:
        if not str(row["shard_state"]).startswith("COMPLETE"):
            continue
        paths = shard_paths(str(row["node_id"]))
        fits.extend(read_csv(paths["fits"]))
        integrals.extend(read_csv(paths["integrals"]))
    return fits, integrals


def convergence_rows(
    repair_rows: list[dict[str, Any]],
    nodes: list[dict[str, Any]],
    manifest: list[dict[str, Any]],
    expected_plan_sha256: str,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    node_lookup = {node["node_id"]: node for node in nodes}
    results = {
        node_id: read_json(shard_paths(node_id)["result"])
        for node_id, node in node_lookup.items()
        if shard_complete(node, expected_plan_sha256)
    }
    effective = {
        row["node_id"]: parse_bool(row["effective_acceptance_passed"])
        for row in manifest
    }
    segment_rows: list[dict[str, Any]] = []
    for segment in repair_rows:
        segment_nodes = [
            node for node in nodes if node["segment_id"] == segment["segment_id"]
        ]
        complete = all(node["node_id"] in results for node in segment_nodes)
        totals: dict[int, complex] = {}
        for order in TRANSFORM_ORDERS:
            order_nodes = [
                node for node in segment_nodes if int(node["outer_order"]) == order
            ]
            totals[order] = (
                sum(
                    (
                        float(node["mapped_outer_weight"])
                        * complex(
                            float(results[node["node_id"]]["selected_inner_energy_real"]),
                            float(results[node["node_id"]]["selected_inner_energy_imaginary"]),
                        )
                        for node in order_nodes
                    ),
                    0.0j,
                )
                if complete
                else 0.0j
            )
        width = float(segment["segment_width"])
        jacobian_errors = []
        for order in TRANSFORM_ORDERS:
            weight_sum = sum(
                float(node["mapped_outer_weight"])
                for node in segment_nodes
                if int(node["outer_order"]) == order
            )
            jacobian_errors.append(abs(weight_sum - width) / max(width, 1.0e-30))
        all_nodes_pass = complete and all(
            effective[node["node_id"]]
            for node in segment_nodes
        )
        segment_rows.append(
            {
                **segment,
                "all_nodes_complete": complete,
                "all_inner_nodes_pass": all_nodes_pass,
                "off_axis_raw_contract_node_count": sum(
                    parse_bool(row["off_axis_raw_contract_passes"])
                    for row in manifest
                    if row["segment_id"] == segment["segment_id"]
                ),
                **complex_fields("transformed_Q8", totals[8]),
                **complex_fields("transformed_Q12", totals[12]),
                "Q8_Q12_absolute_change": abs(totals[12] - totals[8]),
                "Q8_Q12_relative_change": relative_complex_change(
                    totals[8], totals[12]
                ) if complete else math.inf,
                "maximum_constant_jacobian_relative_error": max(jacobian_errors),
                "exact_change_of_variables_gate_passes": (
                    max(jacobian_errors) <= JACOBIAN_CONSTANT_ERROR_LIMIT
                ),
                "segment_kernel_passes": (
                    all_nodes_pass
                    and max(jacobian_errors) <= JACOBIAN_CONSTANT_ERROR_LIMIT
                ),
                **{field: False for field in CLAIM_FIELDS},
            }
        )
    leaf_rows: list[dict[str, Any]] = []
    for parent_leaf_id in sorted({row["parent_leaf_id"] for row in segment_rows}):
        segments = [
            row for row in segment_rows if row["parent_leaf_id"] == parent_leaf_id
        ]
        low = sum(
            complex(float(row["transformed_Q8_real"]), float(row["transformed_Q8_imaginary"]))
            for row in segments
        )
        high = sum(
            complex(float(row["transformed_Q12_real"]), float(row["transformed_Q12_imaginary"]))
            for row in segments
        )
        error = sum(float(row["Q8_Q12_absolute_change"]) for row in segments)
        conservative_relative = error / max(abs(high), 1.0e-12)
        passes = (
            all(bool(row["segment_kernel_passes"]) for row in segments)
            and conservative_relative <= LOCAL_REPAIR_CHANGE_LIMIT
        )
        leaf_rows.append(
            {
                "parent_leaf_id": parent_leaf_id,
                "repair_segment_count": len(segments),
                **complex_fields("repaired_outer_Q8", low),
                **complex_fields("repaired_outer_Q12", high),
                "repaired_outer_error_absolute_conservative": error,
                "repaired_outer_error_relative_conservative": conservative_relative,
                "repaired_leaf_gate_passes": passes,
                **{field: False for field in CLAIM_FIELDS},
            }
        )
    return segment_rows, leaf_rows


def source_rows() -> list[dict[str, str]]:
    paths = [
        Path(__file__).resolve(),
        SCRIPT_5314,
        RESULT_5314,
        PANELS_5314,
        MANIFEST_5314,
        EVENTS_5314,
        SUPPORT_EVENTS_5313,
        CONTRACT_5312,
        EVENT_AUDIT,
        REPAIR_PLAN,
        OFF_AXIS_AUDIT,
    ]
    return [{"path": str(path), "sha256": digest(path)} for path in paths]


def execute(runtime_limit_seconds: float) -> dict[str, Any]:
    M5312.set_below_normal_priority()
    mp.mp.dps = M5314.M5280.MP_DECIMAL_DIGITS
    M5314.M5301.configure_reused_pipeline()
    started = time.perf_counter()
    dry = dry_run()
    if not dry["acceptance_passed"]:
        raise RuntimeError("5315 dry run did not pass")
    repair_rows = read_csv(REPAIR_PLAN)
    nodes = transformed_nodes(repair_rows)
    expected_plan_sha256 = plan_sha256(repair_rows)
    contract = read_csv(CONTRACT_5312)
    events = read_csv(EVENTS_5314)
    branch_death = next(
        float(row["event_absolute_soft_cosine"])
        for row in events
        if row["event_type"] == "SHARED_BRANCH_DEATH"
    )
    base_context = M5314.M5303.synthetic_context()
    multiplier = M5314.M5309.physical_multiplier()
    paused = False
    for node in nodes:
        if shard_complete(node, expected_plan_sha256):
            continue
        if time.perf_counter() - started >= runtime_limit_seconds:
            paused = True
            break
        integrate_transformed_node(
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
                "stage": "SQUARED_EVENT_COORDINATE_NODES",
                "last_completed_node_id": node["node_id"],
            },
        )
    manifest = node_manifest(nodes, expected_plan_sha256)
    write_csv(NODE_MANIFEST, manifest, ["node_id", "shard_state"])
    off_axis_rows = [
        off_axis_raw_contour_contract(
            node, read_json(shard_paths(node["node_id"])["result"])
        )
        for node in nodes
        if shard_complete(node, expected_plan_sha256)
    ]
    write_csv(OFF_AXIS_AUDIT, off_axis_rows, ["node_id", "segment_id"])
    fits, integrals = aggregate_shards(manifest)
    write_csv(ALL_POLE_FITS, fits, ["node_id", "fit_row_type", "fit_scale"])
    write_csv(
        ALL_CELL_INTEGRALS,
        integrals,
        ["node_id", "contract_index", "energy_order"],
    )
    segment_rows, leaf_rows = convergence_rows(
        repair_rows, nodes, manifest, expected_plan_sha256
    )
    write_csv(SEGMENT_CONVERGENCE, segment_rows, ["repair_id", "segment_id"])
    write_csv(LEAF_CONVERGENCE, leaf_rows, ["parent_leaf_id"])
    parent_panels = read_csv(PANELS_5314)
    standard_leaves = [
        row
        for row in parent_panels
        if parse_bool(row["adaptive_leaf"])
        and parse_bool(row["adaptive_gate_passes"])
    ]
    repair_failure_ids = {row["adaptive_panel_id"] for row in failed_parent_leaves()}
    repaired_ids = {row["parent_leaf_id"] for row in leaf_rows}
    all_nodes_pass = (
        not paused
        and all(row["shard_state"] == "COMPLETE_PASS" for row in manifest)
    )
    all_repairs_pass = (
        not paused
        and repaired_ids == repair_failure_ids
        and all(bool(row["repaired_leaf_gate_passes"]) for row in leaf_rows)
    )
    if all_nodes_pass and all_repairs_pass:
        standard_low = sum(
            complex(
                float(row["outer_Q2_energy_Q12_real"]),
                float(row["outer_Q2_energy_Q12_imaginary"]),
            )
            for row in standard_leaves
        )
        standard_high = sum(
            complex(
                float(row["outer_Q4_energy_Q12_real"]),
                float(row["outer_Q4_energy_Q12_imaginary"]),
            )
            for row in standard_leaves
        )
        repair_low = sum(
            complex(
                float(row["repaired_outer_Q8_real"]),
                float(row["repaired_outer_Q8_imaginary"]),
            )
            for row in leaf_rows
        )
        repair_high = sum(
            complex(
                float(row["repaired_outer_Q12_real"]),
                float(row["repaired_outer_Q12_imaginary"]),
            )
            for row in leaf_rows
        )
        panel_nine_low = standard_low + repair_low
        panel_nine_high = standard_high + repair_high
        error = sum(
            float(row["outer_Q2_Q4_absolute_change"])
            for row in standard_leaves
        ) + sum(
            float(row["repaired_outer_error_absolute_conservative"])
            for row in leaf_rows
        )
        baseline = M5314.M5313.baseline_panels_one_to_eight()
        full_value = baseline + panel_nine_high
        panel_nine_error_relative = error / max(abs(panel_nine_high), 1.0e-12)
        full_error_relative = error / max(abs(full_value), 1.0e-12)
    else:
        panel_nine_low = panel_nine_high = full_value = 0.0j
        error = panel_nine_error_relative = full_error_relative = math.inf
    accepted = (
        all_nodes_pass
        and all_repairs_pass
        and panel_nine_error_relative <= GLOBAL_OUTER_ERROR_BUDGET_LIMIT
    )
    if paused:
        decision = "SQUARED_EVENT_COORDINATE_REPAIR_PAUSED__RESUME_SAVED_SHARDS"
    elif not all_nodes_pass:
        decision = "SQUARED_EVENT_COORDINATE_REPAIR_INNER_NODE_FAILURE"
    elif not all_repairs_pass:
        decision = "SQUARED_EVENT_COORDINATE_REPAIR_LOCAL_GATE_FAILED"
    elif not accepted:
        decision = "SQUARED_EVENT_COORDINATE_REPAIR_GLOBAL_BUDGET_FAILED"
    else:
        decision = (
            "E0025_SQUARED_EVENT_COORDINATE_REPAIR_CONVERGED__"
            "VALIDATE_THEN_EXTEND_REGULATOR_LADDER"
        )
    formal_end = M5283.formal_inventory_digest()
    parent_result = read_json(RESULT_5314)
    result = {
        "checkpoint": CHECKPOINT,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "mode": "squared-event-coordinate-collar-repair",
        "acceptance_passed": accepted,
        "decision": decision,
        "parent_standard_passing_leaf_count": len(standard_leaves),
        "parent_replaced_failing_leaf_count": len(repair_failure_ids),
        "repair_segment_count": len(repair_rows),
        "planned_transformed_node_count": len(nodes),
        "completed_transformed_node_count": sum(
            str(row["shard_state"]).startswith("COMPLETE") for row in manifest
        ),
        "failed_transformed_inner_node_count": sum(
            row["shard_state"] == "COMPLETE_FAIL" for row in manifest
        ),
        "off_axis_raw_contour_contract_node_count": sum(
            parse_bool(row["off_axis_raw_contract_passes"])
            for row in manifest
        ),
        "all_transformed_nodes_pass": all_nodes_pass,
        "all_repaired_leaves_pass": all_repairs_pass,
        "maximum_repaired_leaf_error_relative_conservative": (
            max(
                float(row["repaired_outer_error_relative_conservative"])
                for row in leaf_rows
            )
            if leaf_rows
            else math.inf
        ),
        **complex_fields("panel_nine_outer_low", panel_nine_low),
        **complex_fields("panel_nine_outer_high", panel_nine_high),
        "panel_nine_outer_error_absolute_conservative": error,
        "panel_nine_outer_error_relative_conservative": panel_nine_error_relative,
        **complex_fields("reassembled_E0025_fixed_decay_integral", full_value),
        "reassembled_outer_error_relative_conservative": full_error_relative,
        "formalization_workbench_reference_digest": parent_result[
            "formalization_workbench_end_digest"
        ],
        "formalization_workbench_end_digest": formal_end,
        "formalization_workbench_modified_file_count": (
            0
            if formal_end == parent_result["formalization_workbench_end_digest"]
            else -1
        ),
        "claim_boundary": {
            "valid_for_E0025_fixed_decay_outer_soft_integral": accepted,
            **{field: False for field in CLAIM_FIELDS},
            "reason": (
                "Only E0025 at one fixed absolute decay angle is addressed. "
                "The regulator-zero ladder and decay-angle integration remain."
            ),
        },
        "resource_contract": {
            "maximum_task_python_processes": 1,
            "worker_math_threads": 1,
            "windows_priority": "BelowNormal",
            "maximum_silent_work_hours": 4,
            "runtime_limit_seconds_per_invocation": runtime_limit_seconds,
        },
        "node_plan_sha256": expected_plan_sha256,
        "source_files": source_rows(),
        "runtime_seconds": time.perf_counter() - started,
    }
    atomic_json(RESULT, result)
    write_csv(
        CONVERGENCE,
        [
            {
                "epsilon_id": M5312.EPSILON_ID,
                "epsilon": M5312.EPSILON,
                **complex_fields("panel_nine_outer_low", panel_nine_low),
                **complex_fields("panel_nine_outer_high", panel_nine_high),
                "panel_nine_outer_error_relative_conservative": panel_nine_error_relative,
                **complex_fields("reassembled_E0025_integral", full_value),
                "reassembled_outer_error_relative_conservative": full_error_relative,
                "convergence_passed": accepted,
                **{field: False for field in CLAIM_FIELDS},
            }
        ],
    )
    atomic_json(
        STATUS,
        {
            "checkpoint": CHECKPOINT,
            "state": (
                "COMPLETE"
                if accepted
                else ("PAUSED_RESUMABLE" if paused else "REFINEMENT_REQUIRED")
            ),
            "decision": decision,
            "completed_transformed_node_count": result[
                "completed_transformed_node_count"
            ],
            "planned_transformed_node_count": len(nodes),
        },
    )
    return result


def render_document(result: dict[str, Any], passed: bool) -> None:
    text = f"""# 5315 - Squared-event-coordinate collar repair

## Derivation

At both failed 5314 leaves, the shared pole crosses a support edge with a
nonzero slope.  Locally,

`p(x)-E_edge(x) = kappa (x-x_event) + O((x-x_event)^2)`, with `kappa != 0`.

The exact energy-space pole primitive therefore contributes
`A log|x-x_event| + regular` to the outer integrand.  This is integrable but
converges slowly under ordinary Gauss-Legendre quadrature at an endpoint.
The exact coordinate change

`|x-x_event| = t^2`,  `|dx| = 2t dt`

maps it to `4 A t log(t) + O(t)`, which is integrable and vanishes at `t=0`.
No term, coefficient, or closure is added.  The Jacobian is included in every
quadrature weight and its constant-integrand identity is validated.

## Result

- parent passing leaves retained: `{result['parent_standard_passing_leaf_count']}`;
- failed parent leaves replaced: `{result['parent_replaced_failing_leaf_count']}`;
- transformed segments: `{result['repair_segment_count']}`;
- transformed nodes: `{result['completed_transformed_node_count']}` / `{result['planned_transformed_node_count']}`;
- failed transformed inner nodes: `{result['failed_transformed_inner_node_count']}`;
- off-axis raw-contour nodes: `{result['off_axis_raw_contour_contract_node_count']}`;
- maximum conservative repaired-leaf Q8/Q12 error:
  `{result['maximum_repaired_leaf_error_relative_conservative']:.12g}`;
- panel-nine conservative error:
  `{result['panel_nine_outer_error_relative_conservative']:.12g}`;
- reassembled `E0025` fixed-decay integral:
  `{result['reassembled_E0025_fixed_decay_integral_real']:.12g}`
  `{result['reassembled_E0025_fixed_decay_integral_imaginary']:+.12g} i`.

Decision: **{result['decision']}**.

Validation: **{'PASS' if passed else 'FAIL'}**.

## Claim boundary

This closes only the `E0025` outer-soft integral at one fixed absolute decay
angle if validation passes.  It does not establish the regulator-zero limit,
decay-angle integral, full phase-space coefficient, UV prediction, local GR,
or the full MTS theory.
"""
    DOCUMENT.write_text(text, encoding="utf-8")


def validate_outputs() -> dict[str, Any]:
    started = time.perf_counter()
    result = read_json(RESULT)
    dry = read_json(DRY_RUN)
    event_rows = read_csv(EVENT_AUDIT)
    repair_rows = read_csv(REPAIR_PLAN)
    manifest = read_csv(NODE_MANIFEST)
    off_axis_rows = read_csv(OFF_AXIS_AUDIT)
    integrals = read_csv(ALL_CELL_INTEGRALS)
    segments = read_csv(SEGMENT_CONVERGENCE)
    leaves = read_csv(LEAF_CONVERGENCE)
    convergence = read_csv(CONVERGENCE)
    source_files_current = all(
        Path(row["path"]).exists()
        and digest(Path(row["path"])) == row["sha256"]
        for row in result["source_files"]
    )
    jacobian_gate = bool(segments) and all(
        parse_bool(row["exact_change_of_variables_gate_passes"])
        and float(row["maximum_constant_jacobian_relative_error"])
        <= JACOBIAN_CONSTANT_ERROR_LIMIT
        for row in segments
    )
    gates = [
        validation_gate(
            "dry_run_and_result_accepted",
            bool(dry["acceptance_passed"]) and bool(result["acceptance_passed"]),
            result["decision"],
        ),
        validation_gate(
            "parent_baseline_complete_and_failures_exactly_replaced",
            parent_is_complete()
            and len(failed_parent_leaves()) == 2
            and {row["adaptive_panel_id"] for row in failed_parent_leaves()}
            == {row["parent_leaf_id"] for row in leaves},
            f"repairs={len(leaves)}",
        ),
        validation_gate(
            "support_event_linear_crossings_refined",
            len(event_rows) == 2
            and all(parse_bool(row["linear_crossing_contract_passes"]) for row in event_rows)
            and all(abs(float(row["refined_edge_gap"])) <= ROOT_GAP_TOLERANCE for row in event_rows)
            and all(float(row["crossing_slope_magnitude"]) >= MINIMUM_CROSSING_SLOPE for row in event_rows),
            f"events={len(event_rows)}",
        ),
        validation_gate(
            "squared_coordinate_jacobian_exact_for_constants",
            jacobian_gate,
            f"segments={len(segments)}",
        ),
        validation_gate(
            "off_axis_raw_contour_contract_is_derived_not_threshold_relaxed",
            len(off_axis_rows) == len(manifest)
            and all(
                parse_bool(row["kernel_acceptance_passed"])
                or (
                    parse_bool(row["off_axis_raw_contract_passes"])
                    and parse_bool(row["R2_gate_is_the_only_failed_fit_gate"])
                    and parse_bool(row["raw_inner_convergence_passes"])
                    and parse_bool(row["contour_separation_passes"])
                    and float(row["minimum_imaginary_contour_separation"])
                    >= float(row["floating_separation_floor"])
                )
                for row in off_axis_rows
            ),
            f"off_axis_overrides={result['off_axis_raw_contour_contract_node_count']}",
        ),
        validation_gate(
            "all_transformed_nodes_and_repaired_leaves_pass",
            bool(manifest)
            and all(row["shard_state"] == "COMPLETE_PASS" for row in manifest)
            and bool(leaves)
            and all(parse_bool(row["repaired_leaf_gate_passes"]) for row in leaves)
            and bool(result["all_transformed_nodes_pass"])
            and bool(result["all_repaired_leaves_pass"]),
            f"nodes={len(manifest)}; leaves={len(leaves)}",
        ),
        validation_gate(
            "transformed_energy_integral_artifacts_complete",
            bool(integrals) and len(integrals) == 2 * 2 * len(manifest),
            f"integrals={len(integrals)}",
        ),
        validation_gate(
            "E0025_fixed_decay_outer_integral_converges",
            len(convergence) == 1
            and parse_bool(convergence[0]["convergence_passed"])
            and float(result["panel_nine_outer_error_relative_conservative"])
            <= GLOBAL_OUTER_ERROR_BUDGET_LIMIT
            and bool(result["claim_boundary"][
                "valid_for_E0025_fixed_decay_outer_soft_integral"
            ]),
            f"relative={result['panel_nine_outer_error_relative_conservative']}",
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
            "recorded_source_paths_and_hashes_current",
            source_files_current,
            f"rows={len(result['source_files'])}",
        ),
        validation_gate(
            "scripts_cache_absent",
            not (SCRIPTS / "__pycache__").exists(),
            str(SCRIPTS / "__pycache__"),
        ),
        validation_gate(
            "broader_claims_locked_false",
            all(
                not bool(result["claim_boundary"][field])
                for field in CLAIM_FIELDS
            ),
            "no regulator-zero, decay-angle, phase-space, UV, local-GR, or full-MTS claim",
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
            "VALIDATED_E0025_SQUARED_EVENT_COORDINATE_REPAIR"
            if passed
            else "SQUARED_EVENT_COORDINATE_REPAIR_VALIDATION_FAILED"
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
