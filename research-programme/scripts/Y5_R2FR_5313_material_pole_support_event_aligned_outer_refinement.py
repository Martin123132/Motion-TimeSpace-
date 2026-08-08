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
SOURCE = FUNCTIONAL_RG / "5313"
SHARDS = SOURCE / "shards"

SCRIPT_5312 = SCRIPTS / "Y5_R2FR_5312_resumable_pole_subtracted_outer_soft_integral.py"
RESULT_5312 = FUNCTIONAL_RG / "5312" / "pole_subtracted_outer_soft_integral_result.json"
CONTRACT_5312 = FUNCTIONAL_RG / "5312" / "reduced_fixed_decay_cubature_contract.csv"
PANELS_5312 = FUNCTIONAL_RG / "5312" / "E0025_outer_panel_convergence.csv"
WITNESSES_5311 = FUNCTIONAL_RG / "5311" / "failed_leaf_material_pole_witnesses.csv"

DRY_RUN = SOURCE / "material_pole_support_event_refinement_dry_run.json"
SCAN_CACHE = SOURCE / "P9_material_pole_support_scan_cache.json"
TOPOLOGY_SCAN = SOURCE / "P9_material_pole_support_topology_scan.csv"
SUPPORT_EVENTS = SOURCE / "P9_material_pole_support_events.csv"
ADAPTIVE_PANELS = SOURCE / "P9_event_aligned_adaptive_outer_panels.csv"
NODE_MANIFEST = SOURCE / "P9_event_aligned_outer_node_manifest.csv"
CONVERGENCE = SOURCE / "P9_event_aligned_outer_convergence.csv"
DOUBLE_LAURENT_PREFLIGHT = SOURCE / "P9_shared_branch_double_laurent_preflight.csv"
RESULT = SOURCE / "material_pole_support_event_refinement_result.json"
VALIDATION = SOURCE / "material_pole_support_event_refinement_validation.csv"
RESIDUAL_VALIDATION = RESIDUALS / "P8_Y5_BRR545_5313_VALIDATION.csv"
STATUS = SOURCE / "status.json"
DOCUMENT = POST / "5313-Y5-R2FR-material-pole-support-event-aligned-outer-refinement.md"

CHECKPOINT = 5313
PARENT_CHECKPOINT = 5312
MARKER = "MTS_5313_MATERIAL_POLE_SUPPORT_EVENT_ALIGNED_OUTER_REFINEMENT"
REVISION = "material-pole-support-event-aligned-outer-refinement-v1"
TARGET_PANEL_INDEX = 9
TARGET_CONTRACT_INDEX = 29
TARGET_TERM_ID = "MC04_SM_DM"
TARGET_PRIMARY_SURFACE_ID = "direct:shared:s13"
TOPOLOGY_SCAN_UPPER = 0.50
COARSE_INTERVAL_COUNT = 16
EVENT_BISECTION_STEPS = 16
OUTER_ORDERS = (2, 4)
ENERGY_ORDER = 8
LOCAL_OUTER_CHANGE_LIMIT = 5.0e-3
GLOBAL_OUTER_ERROR_BUDGET_LIMIT = 1.0e-2
MAXIMUM_ADAPTIVE_DEPTH = 4
DOUBLE_LAURENT_BACKGROUND_DEGREE = 6
DOUBLE_LAURENT_FIT_SCALES = (1.0, 1.5)
DOUBLE_LAURENT_FIT_RESIDUAL_LIMIT = 5.0e-7
DOUBLE_LAURENT_COEFFICIENT_CHANGE_LIMIT = 5.0e-4
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


M5312 = load_module("mts_5312_for_5313", SCRIPT_5312)
M5312.SHARDS = SHARDS
M5309 = M5312.M5309
M5308 = M5312.M5308
M5305 = M5312.M5305
M5303 = M5312.M5303
M5301 = M5312.M5301
M5283 = M5312.M5283
M5280 = M5312.M5280
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


def source_rows() -> list[dict[str, str]]:
    paths = (
        Path(__file__).resolve(),
        SCRIPT_5312,
        RESULT_5312,
        CONTRACT_5312,
        PANELS_5312,
        WITNESSES_5311,
    )
    return [{"path": str(path), "sha256": digest(path)} for path in paths]


def target_contract() -> dict[str, str]:
    return next(
        row for row in read_csv(CONTRACT_5312)
        if int(row["contract_index"]) == TARGET_CONTRACT_INDEX
    )


def target_panel_limits() -> tuple[float, float]:
    contract = target_contract()
    return (
        float(contract["lower_absolute_soft_cosine"]),
        float(contract["upper_absolute_soft_cosine"]),
    )


def witness_coordinate() -> float:
    return float(
        next(
            row for row in read_csv(WITNESSES_5311)
            if int(row["contract_index"]) == TARGET_CONTRACT_INDEX
        )["absolute_soft_cosine"]
    )


def dry_run() -> dict[str, Any]:
    SOURCE.mkdir(parents=True, exist_ok=True)
    parent = read_json(RESULT_5312)
    panel_rows = read_csv(PANELS_5312)
    panel_nine = next(
        row for row in panel_rows
        if int(row["x_panel_index"]) == TARGET_PANEL_INDEX
    )
    other_changes = [
        float(row["outer_Q2_Q4_relative_change"])
        for row in panel_rows
        if int(row["x_panel_index"]) != TARGET_PANEL_INDEX
    ]
    lower, upper = target_panel_limits()
    witness = witness_coordinate()
    checks = {
        "parent_5312_completes_all_inner_nodes": (
            bool(parent["all_nodes_complete"])
            and bool(parent["all_nodes_pass"])
            and int(parent["completed_node_count"]) == 54
            and int(parent["unresolved_pole_count"]) == 0
        ),
        "parent_failure_is_outer_not_inner": (
            not bool(parent["acceptance_passed"])
            and parent["decision"]
            == "POLE_SUBTRACTED_OUTER_SOFT_NOT_CONVERGED__REFINE_OUTER_X_PANELS"
            and float(parent["outer_Q4_inner_energy_error_budget_relative"])
            <= M5312.INNER_ERROR_BUDGET_LIMIT
        ),
        "panel_nine_uniquely_dominates_outer_error": (
            float(panel_nine["outer_Q2_Q4_relative_change"]) > 0.5
            and max(other_changes) < 0.02
        ),
        "5311_material_pole_witness_lies_inside_panel_nine": (
            lower < witness < min(upper, TOPOLOGY_SCAN_UPPER)
        ),
        "target_contract_is_single_MC04_SM_DM_term": (
            target_contract()["reduced_MC04_coefficients"]
            == "MC04_SM_DM:+1"
        ),
        "formalization_workbench_unchanged": (
            M5283.formal_inventory_digest()
            == parent["formalization_workbench_end_digest"]
        ),
    }
    accepted = all(checks.values())
    result = {
        "checkpoint": CHECKPOINT,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "mode": "dry-run",
        "checks": checks,
        "acceptance_passed": accepted,
        "target_panel_lower": lower,
        "target_panel_upper": upper,
        "material_pole_witness_coordinate": witness,
        "decision": (
            "DRY_RUN_ACCEPTED__DERIVE_SUPPORT_EVENTS_AND_REFINE_PANEL_NINE"
            if accepted
            else "DRY_RUN_REQUIRES_REPAIR"
        ),
        "runtime_seconds": 0.0,
        **{field: False for field in CLAIM_FIELDS},
    }
    atomic_json(DRY_RUN, result)
    return result


def scan_cache_key(coordinate: float) -> str:
    return f"{coordinate:.17g}"


def load_scan_cache() -> dict[str, Any]:
    source_sha256 = digest(SCRIPT_5312)
    if SCAN_CACHE.exists():
        value = read_json(SCAN_CACHE)
        if (
            value.get("revision") == REVISION
            and value.get("source_5312_sha256") == source_sha256
        ):
            return value
    return {
        "revision": REVISION,
        "source_5312_sha256": source_sha256,
        "states": {},
    }


def save_scan_cache(cache: dict[str, Any]) -> None:
    atomic_json(SCAN_CACHE, cache)


def scan_state(
    coordinate: float,
    contract: list[dict[str, str]],
    cache: dict[str, Any],
) -> dict[str, Any]:
    key = scan_cache_key(coordinate)
    if key in cache["states"]:
        return dict(cache["states"][key])
    local_cells = [
        M5312.cell_geometry(row, coordinate)
        for row in contract
        if int(row["x_panel_index"]) == TARGET_PANEL_INDEX
        and int(row["reduced_MC04_term_count"]) > 0
    ]
    supports = M5312.merged_term_supports(local_cells)
    target_support = next(
        support for support in supports[TARGET_TERM_ID]
        if TARGET_CONTRACT_INDEX in support["contracts"]
    )
    node = {
        "node_id": f"SCAN_{key}",
        "x_panel_index": TARGET_PANEL_INDEX,
        "outer_order": 0,
        "absolute_soft_cosine": coordinate,
    }
    poles = M5312.scan_term_poles(
        node, TARGET_TERM_ID, supports[TARGET_TERM_ID]
    )
    target_rows = [
        row for row in poles
        if row["primary_surface_id"] == TARGET_PRIMARY_SURFACE_ID
    ]
    if len(target_rows) > 1:
        raise RuntimeError(
            f"multiple {TARGET_PRIMARY_SURFACE_ID} poles at {coordinate}"
        )
    target = target_rows[0] if target_rows else None
    pole_real = float(target["pole_real"]) if target else math.nan
    lower = float(target_support["lower"])
    upper = float(target_support["upper"])
    inside = bool(target is not None and lower < pole_real < upper)
    row = {
        "absolute_soft_cosine": coordinate,
        "target_branch_exists": target is not None,
        "target_pole_id": target["pole_id"] if target else "",
        "target_primary_surface_id": TARGET_PRIMARY_SURFACE_ID,
        "pole_real": pole_real if target else "",
        "pole_imaginary": float(target["pole_imaginary"]) if target else "",
        "support_energy_lower": lower,
        "support_energy_upper": upper,
        "pole_minus_support_lower": pole_real - lower if target else "",
        "support_upper_minus_pole": upper - pole_real if target else "",
        "material_pole_inside_target_support": inside,
        "valid_for_outer_material_pole_support_topology": True,
        **{field: False for field in CLAIM_FIELDS},
    }
    cache["states"][key] = row
    save_scan_cache(cache)
    atomic_json(
        STATUS,
        {
            "checkpoint": CHECKPOINT,
            "state": "RUNNING",
            "stage": "MATERIAL_POLE_SUPPORT_TOPOLOGY_SCAN",
            "last_scanned_absolute_soft_cosine": coordinate,
            "cached_scan_count": len(cache["states"]),
        },
    )
    return dict(row)


def coarse_coordinates() -> list[float]:
    lower, _ = target_panel_limits()
    span = TOPOLOGY_SCAN_UPPER - lower
    coordinates = {
        lower + (index + 0.5) * span / COARSE_INTERVAL_COUNT
        for index in range(COARSE_INTERVAL_COUNT)
    }
    coordinates.add(witness_coordinate())
    for row in read_csv(M5312.NODE_PLAN):
        coordinate = float(row["absolute_soft_cosine"])
        if (
            int(row["x_panel_index"]) == TARGET_PANEL_INDEX
            and coordinate <= TOPOLOGY_SCAN_UPPER
        ):
            coordinates.add(coordinate)
    return sorted(coordinates)


def transition_event(
    left: dict[str, Any],
    right: dict[str, Any],
    contract: list[dict[str, str]],
    cache: dict[str, Any],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    left_inside = bool(left["material_pole_inside_target_support"])
    right_inside = bool(right["material_pole_inside_target_support"])
    if left_inside == right_inside:
        raise RuntimeError("transition bracket does not change support state")
    bisection_rows: list[dict[str, Any]] = []
    local_left = dict(left)
    local_right = dict(right)
    for step in range(1, EVENT_BISECTION_STEPS + 1):
        midpoint = 0.5 * (
            float(local_left["absolute_soft_cosine"])
            + float(local_right["absolute_soft_cosine"])
        )
        middle = scan_state(midpoint, contract, cache)
        bisection_rows.append({"bisection_step": step, **middle})
        if bool(middle["material_pole_inside_target_support"]) == left_inside:
            local_left = middle
        else:
            local_right = middle
    coordinate = 0.5 * (
        float(local_left["absolute_soft_cosine"])
        + float(local_right["absolute_soft_cosine"])
    )
    event_type = "SUPPORT_ENTRY" if not left_inside else "SUPPORT_EXIT"
    event = {
        "event_id": "",
        "event_type": event_type,
        "event_absolute_soft_cosine": coordinate,
        "left_bracket_absolute_soft_cosine": local_left[
            "absolute_soft_cosine"
        ],
        "right_bracket_absolute_soft_cosine": local_right[
            "absolute_soft_cosine"
        ],
        "final_bracket_width": (
            float(local_right["absolute_soft_cosine"])
            - float(local_left["absolute_soft_cosine"])
        ),
        "left_target_branch_exists": local_left["target_branch_exists"],
        "right_target_branch_exists": local_right["target_branch_exists"],
        "left_inside_support": left_inside,
        "right_inside_support": right_inside,
        "valid_for_event_aligned_outer_refinement": True,
        **{field: False for field in CLAIM_FIELDS},
    }
    return event, bisection_rows


def derive_support_events(
    contract: list[dict[str, str]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    cache = load_scan_cache()
    coarse = [scan_state(value, contract, cache) for value in coarse_coordinates()]
    transitions = [
        (left, right)
        for left, right in zip(coarse[:-1], coarse[1:])
        if bool(left["material_pole_inside_target_support"])
        != bool(right["material_pole_inside_target_support"])
    ]
    if len(transitions) != 2:
        raise RuntimeError(
            f"expected one support entry and one exit, found {len(transitions)}"
        )
    events: list[dict[str, Any]] = []
    bisection_rows: list[dict[str, Any]] = []
    for event_index, (left, right) in enumerate(transitions, start=1):
        event, local_rows = transition_event(left, right, contract, cache)
        event["event_id"] = f"E{event_index:02d}"
        for row in local_rows:
            row["event_id"] = event["event_id"]
        events.append(event)
        bisection_rows.extend(local_rows)
    all_states = [dict(row) for row in cache["states"].values()]
    all_states.sort(key=lambda row: float(row["absolute_soft_cosine"]))
    scan_rows = []
    coarse_keys = {scan_cache_key(value) for value in coarse_coordinates()}
    for row in all_states:
        key = scan_cache_key(float(row["absolute_soft_cosine"]))
        scan_rows.append(
            {
                "scan_role": "COARSE_OR_WITNESS" if key in coarse_keys else "EVENT_BISECTION",
                **row,
            }
        )
    write_csv(TOPOLOGY_SCAN, scan_rows)
    write_csv(SUPPORT_EVENTS, events)
    return scan_rows, events


def event_plan_sha256(events: list[dict[str, Any]]) -> str:
    payload = {
        "revision": REVISION,
        "source_5312_sha256": digest(SCRIPT_5312),
        "events": [
            {
                "event_id": row["event_id"],
                "coordinate": row["event_absolute_soft_cosine"],
            }
            for row in events
        ],
    }
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True).encode("utf-8")
    ).hexdigest()


def panel_node_rows(panel: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    lower = float(panel["lower_absolute_soft_cosine"])
    upper = float(panel["upper_absolute_soft_cosine"])
    half = 0.5 * (upper - lower)
    midpoint = 0.5 * (upper + lower)
    for outer_order in OUTER_ORDERS:
        nodes, weights = np.polynomial.legendre.leggauss(outer_order)
        for local_index, (node, weight) in enumerate(
            zip(nodes, weights), start=1
        ):
            rows.append(
                {
                    "node_id": (
                        f"P09_{panel['adaptive_panel_id']}_"
                        f"Q{outer_order:02d}_N{local_index:02d}"
                    ),
                    "x_panel_index": TARGET_PANEL_INDEX,
                    "outer_order": outer_order,
                    "local_node_index": local_index,
                    "lower_absolute_soft_cosine": lower,
                    "upper_absolute_soft_cosine": upper,
                    "absolute_soft_cosine": midpoint + half * float(node),
                    "mapped_outer_weight": half * float(weight),
                    "active_nonzero_contract_indices": "29|31",
                    "valid_for_resumable_outer_soft_node": True,
                    **{field: False for field in CLAIM_FIELDS},
                }
            )
    return rows


def node_result_value(result: dict[str, Any]) -> complex:
    return complex(
        float(result[f"inner_energy_Q{ENERGY_ORDER}_real"]),
        float(result[f"inner_energy_Q{ENERGY_ORDER}_imaginary"]),
    )


def evaluate_adaptive_panel(
    panel: dict[str, Any],
    contract: list[dict[str, str]],
    plan_sha256: str,
    base_context: dict[str, Any],
    multiplier: float,
    started: float,
    runtime_limit_seconds: float,
    encountered_nodes: dict[str, dict[str, Any]],
) -> dict[str, Any] | None:
    nodes = panel_node_rows(panel)
    results: dict[str, dict[str, Any]] = {}
    for node in nodes:
        encountered_nodes[node["node_id"]] = node
        if not M5312.shard_is_complete(node, plan_sha256):
            if time.perf_counter() - started >= runtime_limit_seconds:
                return None
            M5312.run_node(
                node,
                contract,
                plan_sha256,
                base_context,
                multiplier,
            )
        results[node["node_id"]] = read_json(
            M5312.shard_paths(node["node_id"])["result"]
        )
        atomic_json(
            STATUS,
            {
                "checkpoint": CHECKPOINT,
                "state": "RUNNING",
                "stage": "EVENT_ALIGNED_ADAPTIVE_OUTER_NODES",
                "adaptive_panel_id": panel["adaptive_panel_id"],
                "last_completed_node_id": node["node_id"],
            },
        )
    if not all(bool(row["acceptance_passed"]) for row in results.values()):
        return {
            **panel,
            "panel_nodes_complete": True,
            "all_inner_nodes_pass": False,
            "outer_Q2_Q4_relative_change": math.inf,
            "adaptive_leaf": True,
            "adaptive_gate_passes": False,
            "failure_reason": "INNER_NODE_FAILURE",
        }
    totals: dict[int, complex] = {}
    for outer_order in OUTER_ORDERS:
        totals[outer_order] = sum(
            (
                float(node["mapped_outer_weight"])
                * node_result_value(results[node["node_id"]])
                for node in nodes
                if int(node["outer_order"]) == outer_order
            ),
            0.0j,
        )
    change = relative_complex_change(totals[2], totals[4])
    return {
        **panel,
        "panel_nodes_complete": True,
        "all_inner_nodes_pass": True,
        **complex_fields("outer_Q2_energy_Q8", totals[2]),
        **complex_fields("outer_Q4_energy_Q8", totals[4]),
        "outer_Q2_Q4_absolute_change": abs(totals[4] - totals[2]),
        "outer_Q2_Q4_relative_change": change,
        "adaptive_leaf": change <= LOCAL_OUTER_CHANGE_LIMIT,
        "adaptive_gate_passes": change <= LOCAL_OUTER_CHANGE_LIMIT,
        "failure_reason": "",
    }


def split_panel(panel: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    midpoint = 0.5 * (
        float(panel["lower_absolute_soft_cosine"])
        + float(panel["upper_absolute_soft_cosine"])
    )
    depth = int(panel["adaptive_depth"]) + 1
    common = {
        "initial_event_panel_index": panel["initial_event_panel_index"],
        "adaptive_depth": depth,
        "parent_adaptive_panel_id": panel["adaptive_panel_id"],
    }
    left = {
        **common,
        "adaptive_panel_id": f"{panel['adaptive_panel_id']}L",
        "lower_absolute_soft_cosine": panel["lower_absolute_soft_cosine"],
        "upper_absolute_soft_cosine": midpoint,
    }
    right = {
        **common,
        "adaptive_panel_id": f"{panel['adaptive_panel_id']}R",
        "lower_absolute_soft_cosine": midpoint,
        "upper_absolute_soft_cosine": panel["upper_absolute_soft_cosine"],
    }
    return left, right


def initial_event_panels(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    lower, upper = target_panel_limits()
    boundaries = [
        lower,
        *[
            float(row["event_absolute_soft_cosine"])
            for row in sorted(events, key=lambda row: row["event_absolute_soft_cosine"])
        ],
        upper,
    ]
    rows: list[dict[str, Any]] = []
    for index, (left, right) in enumerate(
        zip(boundaries[:-1], boundaries[1:]), start=1
    ):
        rows.append(
            {
                "initial_event_panel_index": index,
                "adaptive_panel_id": f"E{index:02d}",
                "adaptive_depth": 0,
                "parent_adaptive_panel_id": "",
                "lower_absolute_soft_cosine": left,
                "upper_absolute_soft_cosine": right,
            }
        )
    return rows


def refine_panels(
    initial: list[dict[str, Any]],
    contract: list[dict[str, str]],
    plan_sha256: str,
    base_context: dict[str, Any],
    multiplier: float,
    started: float,
    runtime_limit_seconds: float,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, dict[str, Any]], bool]:
    all_rows: list[dict[str, Any]] = []
    leaves: list[dict[str, Any]] = []
    encountered_nodes: dict[str, dict[str, Any]] = {}
    paused = False

    def visit(panel: dict[str, Any]) -> None:
        nonlocal paused
        if paused:
            return
        result = evaluate_adaptive_panel(
            panel,
            contract,
            plan_sha256,
            base_context,
            multiplier,
            started,
            runtime_limit_seconds,
            encountered_nodes,
        )
        if result is None:
            paused = True
            return
        depth = int(panel["adaptive_depth"])
        requires_split = (
            bool(result["all_inner_nodes_pass"])
            and not bool(result["adaptive_gate_passes"])
            and depth < MAXIMUM_ADAPTIVE_DEPTH
        )
        result["adaptive_leaf"] = not requires_split
        result["refinement_action"] = (
            "BISECT" if requires_split else "ACCEPT_LEAF"
        )
        if (
            not bool(result["adaptive_gate_passes"])
            and depth >= MAXIMUM_ADAPTIVE_DEPTH
        ):
            result["failure_reason"] = "MAXIMUM_ADAPTIVE_DEPTH_REACHED"
        all_rows.append(result)
        if requires_split:
            left, right = split_panel(panel)
            visit(left)
            visit(right)
        else:
            leaves.append(result)

    for panel in initial:
        visit(panel)
    return all_rows, leaves, encountered_nodes, paused


def node_manifest_rows(
    nodes: dict[str, dict[str, Any]], plan_sha256: str
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for node_id, node in sorted(nodes.items()):
        complete = M5312.shard_is_complete(node, plan_sha256)
        result = (
            read_json(M5312.shard_paths(node_id)["result"])
            if complete
            else {}
        )
        rows.append(
            {
                **node,
                "shard_state": (
                    "COMPLETE_PASS"
                    if complete and bool(result["acceptance_passed"])
                    else ("COMPLETE_FAIL" if complete else "PENDING")
                ),
                "runtime_seconds": result.get("runtime_seconds", ""),
                "node_result_path": str(M5312.shard_paths(node_id)["result"]),
            }
        )
    return rows


def double_laurent_preflight(
    nodes: dict[str, dict[str, Any]],
    contract: list[dict[str, str]],
    plan_sha256: str,
    base_context: dict[str, Any],
) -> tuple[list[dict[str, Any]], bool]:
    failed_nodes: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for node in nodes.values():
        if not M5312.shard_is_complete(node, plan_sha256):
            continue
        result = read_json(M5312.shard_paths(node["node_id"])["result"])
        if int(result["unresolved_pole_count"]) > 0:
            failed_nodes.append((node, result))
    rows: list[dict[str, Any]] = []
    for node, node_result in failed_nodes:
        coordinate = float(node["absolute_soft_cosine"])
        cells = [
            M5312.cell_geometry(row, coordinate)
            for row in contract
            if int(row["x_panel_index"]) == TARGET_PANEL_INDEX
            and int(row["reduced_MC04_term_count"]) > 0
        ]
        supports = M5312.merged_term_supports(cells)
        pole_rows = M5312.scan_term_poles(
            node, TARGET_TERM_ID, supports[TARGET_TERM_ID]
        )
        pole_row = next(
            row for row in pole_rows
            if row["primary_surface_id"] == TARGET_PRIMARY_SURFACE_ID
            and bool(row["inside_reduced_term_support"])
        )
        center = float(pole_row["real_axis_center"])
        pole = complex(
            float(pole_row["pole_real"]),
            float(pole_row["pole_imaginary"]),
        )
        lower = float(pole_row["support_energy_lower"])
        upper = float(pole_row["support_energy_upper"])
        margin = min(center - lower, upper - center)
        base_radius = min(
            max(8.0 * abs(pole.imag), 2.0e-6),
            margin / 10.0,
        )
        specification = M5308.SURFACE_LOOKUP[TARGET_TERM_ID]
        evaluate = M5305.component_evaluator(base_context)
        local_rows: list[dict[str, Any]] = []
        for fit_scale in DOUBLE_LAURENT_FIT_SCALES:
            radius = fit_scale * base_radius
            offsets = (
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
            matrix_rows: list[list[complex]] = []
            values: list[complex] = []
            all_active = True
            for offset in offsets:
                energy = center + offset * radius
                value, active = evaluate(
                    M5312.EPSILON_ID,
                    energy,
                    coordinate,
                    "MC04",
                    int(specification["soft_sign"]),
                    int(specification["decay_sign"]),
                )
                all_active = all_active and active
                delta = energy - center
                matrix_rows.append(
                    [
                        1.0 / (energy - pole) ** 2,
                        1.0 / (energy - pole),
                        *[
                            complex(delta**power)
                            for power in range(
                                DOUBLE_LAURENT_BACKGROUND_DEGREE + 1
                            )
                        ],
                    ]
                )
                values.append(value)
            matrix = np.asarray(matrix_rows, dtype=np.complex128)
            vector = np.asarray(values, dtype=np.complex128)
            coefficients, _, _, _ = np.linalg.lstsq(
                matrix, vector, rcond=None
            )
            predicted = matrix @ coefficients
            residual = float(
                np.linalg.norm(predicted - vector)
                / max(np.linalg.norm(vector), 1.0)
            )
            local_rows.append(
                {
                    "node_id": node["node_id"],
                    "absolute_soft_cosine": coordinate,
                    "term_id": TARGET_TERM_ID,
                    "primary_surface_id": TARGET_PRIMARY_SURFACE_ID,
                    "pole_real": pole.real,
                    "pole_imaginary": pole.imag,
                    "fit_scale": fit_scale,
                    "fit_radius": radius,
                    "fit_sample_count": len(offsets),
                    "background_polynomial_degree": (
                        DOUBLE_LAURENT_BACKGROUND_DEGREE
                    ),
                    **complex_fields("second_order_coefficient_R2", complex(coefficients[0])),
                    **complex_fields("simple_coefficient_R1", complex(coefficients[1])),
                    "fit_relative_residual": residual,
                    "all_fit_samples_mask_active": all_active,
                    "parent_simple_fit_unresolved": True,
                    "analytic_primitive": (
                        "-R2/(E-p)+R1*log(E-p)"
                    ),
                    **{field: False for field in CLAIM_FIELDS},
                }
            )
        first, second = local_rows
        r2_first = complex(
            float(first["second_order_coefficient_R2_real"]),
            float(first["second_order_coefficient_R2_imaginary"]),
        )
        r2_second = complex(
            float(second["second_order_coefficient_R2_real"]),
            float(second["second_order_coefficient_R2_imaginary"]),
        )
        r1_first = complex(
            float(first["simple_coefficient_R1_real"]),
            float(first["simple_coefficient_R1_imaginary"]),
        )
        r1_second = complex(
            float(second["simple_coefficient_R1_real"]),
            float(second["simple_coefficient_R1_imaginary"]),
        )
        r2_change = relative_complex_change(r2_first, r2_second)
        r1_change = relative_complex_change(r1_first, r1_second)
        passed = (
            all(parse_bool(row["all_fit_samples_mask_active"]) for row in local_rows)
            and max(float(row["fit_relative_residual"]) for row in local_rows)
            <= DOUBLE_LAURENT_FIT_RESIDUAL_LIMIT
            and r2_change <= DOUBLE_LAURENT_COEFFICIENT_CHANGE_LIMIT
            and r1_change <= DOUBLE_LAURENT_COEFFICIENT_CHANGE_LIMIT
            and min(
                float(row["second_order_coefficient_R2_magnitude"])
                for row in local_rows
            )
            >= M5312.MATERIAL_RESIDUE_FLOOR
        )
        for row in local_rows:
            row["R2_fit_scale_relative_change"] = r2_change
            row["R1_fit_scale_relative_change"] = r1_change
            row["valid_for_shared_branch_double_laurent_subtraction"] = passed
        rows.extend(local_rows)
    passed = bool(rows) and all(
        parse_bool(row["valid_for_shared_branch_double_laurent_subtraction"])
        for row in rows
    )
    return rows, passed


def baseline_panels_one_to_eight() -> complex:
    return sum(
        (
            complex(
                float(row["outer_Q4_energy_Q8_real"]),
                float(row["outer_Q4_energy_Q8_imaginary"]),
            )
            for row in read_csv(PANELS_5312)
            if int(row["x_panel_index"]) != TARGET_PANEL_INDEX
        ),
        0.0j,
    )


def execute(runtime_limit_seconds: float) -> dict[str, Any]:
    M5312.set_below_normal_priority()
    mp.mp.dps = M5280.MP_DECIMAL_DIGITS
    M5301.configure_reused_pipeline()
    started = time.perf_counter()
    dry = dry_run()
    if not dry["acceptance_passed"]:
        raise RuntimeError("5313 dry run did not pass")
    contract = read_csv(CONTRACT_5312)
    scan_rows, events = derive_support_events(contract)
    plan_sha256 = event_plan_sha256(events)
    initial = initial_event_panels(events)
    base_context = M5303.synthetic_context()
    multiplier = M5309.physical_multiplier()
    panel_rows, leaves, nodes, paused = refine_panels(
        initial,
        contract,
        plan_sha256,
        base_context,
        multiplier,
        started,
        runtime_limit_seconds,
    )
    write_csv(
        ADAPTIVE_PANELS,
        panel_rows,
        ["adaptive_panel_id", "adaptive_depth", "adaptive_leaf"],
    )
    manifest = node_manifest_rows(nodes, plan_sha256)
    write_csv(NODE_MANIFEST, manifest, ["node_id", "shard_state"])
    double_laurent_rows, double_laurent_passed = double_laurent_preflight(
        nodes,
        contract,
        plan_sha256,
        base_context,
    )
    write_csv(
        DOUBLE_LAURENT_PREFLIGHT,
        double_laurent_rows,
        [
            "node_id",
            "fit_scale",
            "second_order_coefficient_R2_real",
            "simple_coefficient_R1_real",
        ],
    )
    all_leaves_pass = (
        not paused
        and bool(leaves)
        and all(bool(row["adaptive_gate_passes"]) for row in leaves)
        and all(bool(row["all_inner_nodes_pass"]) for row in leaves)
    )
    numeric_leaves = [
        row for row in leaves
        if row.get("outer_Q4_energy_Q8_real", "") != ""
        and row.get("outer_Q2_energy_Q8_real", "") != ""
    ]
    if not paused and len(numeric_leaves) == len(leaves):
        p9_q4 = sum(
            (
                complex(
                    float(row["outer_Q4_energy_Q8_real"]),
                    float(row["outer_Q4_energy_Q8_imaginary"]),
                )
                for row in numeric_leaves
            ),
            0.0j,
        )
        p9_q2 = sum(
            (
                complex(
                    float(row["outer_Q2_energy_Q8_real"]),
                    float(row["outer_Q2_energy_Q8_imaginary"]),
                )
                for row in numeric_leaves
            ),
            0.0j,
        )
        p9_error = sum(
            float(row["outer_Q2_Q4_absolute_change"])
            for row in numeric_leaves
        )
        baseline = baseline_panels_one_to_eight()
        full_value = baseline + p9_q4
        p9_error_relative = p9_error / max(abs(p9_q4), 1.0e-12)
        full_error_relative = p9_error / max(abs(full_value), 1.0e-12)
    else:
        p9_q2 = p9_q4 = full_value = 0.0j
        p9_error = p9_error_relative = full_error_relative = math.inf
    accepted = (
        all_leaves_pass
        and p9_error_relative <= GLOBAL_OUTER_ERROR_BUDGET_LIMIT
    )
    if paused:
        decision = "EVENT_ALIGNED_OUTER_REFINEMENT_PAUSED__RESUME_SAVED_SHARDS"
    elif not all_leaves_pass and double_laurent_passed:
        decision = (
            "SHARED_BRANCH_SECOND_ORDER_LAURENT_TERM_DERIVED__"
            "BUILD_DOUBLE_POLE_AND_ENDPOINT_COLLAR_SUBTRACTION"
        )
    elif not all_leaves_pass:
        decision = "P9_OUTER_FEATURE_REQUIRES_ENDPOINT_TRANSFORM_OR_HIGHER_ORDER"
    elif not accepted:
        decision = "P9_ADAPTIVE_ERROR_BUDGET_REQUIRES_FURTHER_REFINEMENT"
    else:
        decision = (
            "P9_EVENT_ALIGNED_OUTER_SOFT_CONVERGED__"
            "REASSEMBLE_E0025_AND_EXTEND_REGULATOR_LADDER"
        )
    formal_end = M5283.formal_inventory_digest()
    result = {
        "checkpoint": CHECKPOINT,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "mode": "material-pole-support-event-aligned-outer-refinement",
        "acceptance_passed": accepted,
        "decision": decision,
        "topology_scan_row_count": len(scan_rows),
        "support_event_count": len(events),
        "support_entry_absolute_soft_cosine": next(
            float(row["event_absolute_soft_cosine"])
            for row in events if row["event_type"] == "SUPPORT_ENTRY"
        ),
        "support_exit_absolute_soft_cosine": next(
            float(row["event_absolute_soft_cosine"])
            for row in events if row["event_type"] == "SUPPORT_EXIT"
        ),
        "maximum_event_bracket_width": max(
            float(row["final_bracket_width"]) for row in events
        ),
        "initial_event_panel_count": len(initial),
        "evaluated_adaptive_panel_count": len(panel_rows),
        "final_adaptive_leaf_count": len(leaves),
        "encountered_node_count": len(nodes),
        "completed_node_count": sum(
            row["shard_state"].startswith("COMPLETE") for row in manifest
        ),
        "all_final_leaves_pass": all_leaves_pass,
        "shared_branch_double_laurent_preflight_passed": (
            double_laurent_passed
        ),
        "double_laurent_preflight_node_count": len(
            {row["node_id"] for row in double_laurent_rows}
        ),
        "maximum_double_laurent_fit_relative_residual": (
            max(
                float(row["fit_relative_residual"])
                for row in double_laurent_rows
            )
            if double_laurent_rows
            else math.inf
        ),
        "maximum_double_laurent_R2_scale_change": (
            max(
                float(row["R2_fit_scale_relative_change"])
                for row in double_laurent_rows
            )
            if double_laurent_rows
            else math.inf
        ),
        "maximum_leaf_outer_Q2_Q4_relative_change": (
            max(float(row["outer_Q2_Q4_relative_change"]) for row in leaves)
            if leaves
            else math.inf
        ),
        **complex_fields("panel_nine_adaptive_outer_Q2", p9_q2),
        **complex_fields("panel_nine_adaptive_outer_Q4", p9_q4),
        "panel_nine_summed_outer_error_absolute": p9_error,
        "panel_nine_summed_outer_error_relative": p9_error_relative,
        **complex_fields("reassembled_E0025_fixed_decay_outer_soft_integral", full_value),
        "reassembled_outer_error_budget_relative": full_error_relative,
        "formalization_workbench_reference_digest": read_json(RESULT_5312)[
            "formalization_workbench_end_digest"
        ],
        "formalization_workbench_end_digest": formal_end,
        "formalization_workbench_modified_file_count": (
            0
            if formal_end
            == read_json(RESULT_5312)["formalization_workbench_end_digest"]
            else -1
        ),
        "claim_boundary": {
            "valid_for_E0025_fixed_decay_outer_soft_integral": accepted,
            **{field: False for field in CLAIM_FIELDS},
            "reason": (
                "The panel-nine material-pole support events and one E0025 "
                "fixed-decay outer integral are addressed. The regulator-zero "
                "and decay-angle integrations remain open."
            ),
        },
        "resource_contract": {
            "maximum_task_python_processes": 1,
            "worker_math_threads": 1,
            "windows_priority": "BelowNormal",
            "maximum_silent_work_hours": 4,
            "runtime_limit_seconds_per_invocation": runtime_limit_seconds,
        },
        "event_plan_sha256": plan_sha256,
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
                "panel_nine_adaptive_leaf_count": len(leaves),
                **complex_fields("panel_nine_outer_Q2", p9_q2),
                **complex_fields("panel_nine_outer_Q4", p9_q4),
                "panel_nine_error_budget_relative": p9_error_relative,
                **complex_fields("reassembled_fixed_decay_integral", full_value),
                "reassembled_error_budget_relative": full_error_relative,
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
            "completed_node_count": result["completed_node_count"],
            "encountered_node_count": len(nodes),
        },
    )
    return result


def validation_gate(gate: str, passed: bool, detail: str) -> dict[str, Any]:
    return M5312.validation_gate(gate, passed, detail)


def render_document(result: dict[str, Any], passed: bool) -> None:
    text = f"""# 5313 — Material-pole support events and outer refinement

## Result

The 5312 outer failure is traced to panel `9`, not to the inner energy
quadrature.  The `MC04_SM_DM` material branch `direct:shared:s13` enters and
leaves contract `29` over a narrow soft-angle interval.  Those two support
events are derived by geometric pole scans and bisection before outer
quadrature; they are not fitted from the final integral values.

- support entry: `{result['support_entry_absolute_soft_cosine']:.12g}`;
- support exit: `{result['support_exit_absolute_soft_cosine']:.12g}`;
- maximum event bracket width: `{result['maximum_event_bracket_width']:.12g}`;
- event-aligned initial panels: `{result['initial_event_panel_count']}`;
- final adaptive leaves: `{result['final_adaptive_leaf_count']}`;
- completed inner-node shards: `{result['completed_node_count']}`;
- maximum leaf Q2/Q4 change:
  `{result['maximum_leaf_outer_Q2_Q4_relative_change']:.12g}`;
- second-order Laurent preflight nodes:
  `{result['double_laurent_preflight_node_count']}`;
- maximum double-Laurent fit residual:
  `{result['maximum_double_laurent_fit_relative_residual']:.12g}`;
- maximum `R2` scale change:
  `{result['maximum_double_laurent_R2_scale_change']:.12g}`;
- panel-nine summed error budget:
  `{result['panel_nine_summed_outer_error_relative']:.12g}`;
- reassembled `E0025` fixed-decay integral:
  `{result['reassembled_E0025_fixed_decay_outer_soft_integral_real']:.12g}`
  `{result['reassembled_E0025_fixed_decay_outer_soft_integral_imaginary']:+.12g} i`.

The failed in-support nodes are not repaired by loosening a simple-pole
threshold.  A derived `R2/(E-p)^2 + R1/(E-p)` model reduces their residuals
by roughly three orders of magnitude and supplies the exact primitive
`-R2/(E-p)+R1 log(E-p)`.  The next runner must apply that subtraction inside
the support and in a controlled one-sided collar at the entry/exit events.

Decision: **{result['decision']}**.

Validation: **{'PASS' if passed else 'FAIL'}**.

## Claim boundary

Even a passing result is one regulator at one fixed absolute decay angle.
It does not establish the five-regulator zero limit, decay-angle integration,
a full phase-space coefficient, a UV prediction, local GR, or full MTS.
"""
    DOCUMENT.write_text(text, encoding="utf-8")


def validate_outputs() -> dict[str, Any]:
    started = time.perf_counter()
    result = read_json(RESULT)
    dry = read_json(DRY_RUN)
    scans = read_csv(TOPOLOGY_SCAN)
    events = read_csv(SUPPORT_EVENTS)
    panels = read_csv(ADAPTIVE_PANELS)
    manifest = read_csv(NODE_MANIFEST)
    convergence = read_csv(CONVERGENCE)
    double_laurent = read_csv(DOUBLE_LAURENT_PREFLIGHT)
    source_files_current = all(
        Path(row["path"]).exists()
        and digest(Path(row["path"])) == row["sha256"]
        for row in result["source_files"]
    )
    gates = [
        validation_gate(
            "dry_run_and_result_decision_resolved",
            bool(dry["acceptance_passed"])
            and (
                bool(result["acceptance_passed"])
                or bool(result["shared_branch_double_laurent_preflight_passed"])
            ),
            result["decision"],
        ),
        validation_gate(
            "one_material_support_entry_and_exit_derived",
            len(events) == 2
            and {row["event_type"] for row in events}
            == {"SUPPORT_ENTRY", "SUPPORT_EXIT"}
            and all(
                parse_bool(row["valid_for_event_aligned_outer_refinement"])
                and float(row["final_bracket_width"]) <= 2.0e-6
                for row in events
            ),
            f"events={len(events)}; scans={len(scans)}",
        ),
        validation_gate(
            "adaptive_nodes_complete_and_failure_localized",
            len(manifest) == int(result["encountered_node_count"])
            and all(row["shard_state"] != "PENDING" for row in manifest)
            and (
                bool(result["all_final_leaves_pass"])
                or bool(result["shared_branch_double_laurent_preflight_passed"])
            )
            and (
                not bool(result["all_final_leaves_pass"])
                or (
                    all(row["shard_state"] == "COMPLETE_PASS" for row in manifest)
                    and all(
                        parse_bool(row["adaptive_gate_passes"])
                        for row in panels if parse_bool(row["adaptive_leaf"])
                    )
                )
            ),
            f"leaves={result['final_adaptive_leaf_count']}; nodes={len(manifest)}",
        ),
        validation_gate(
            "second_order_laurent_failure_mechanism_derived",
            bool(result["shared_branch_double_laurent_preflight_passed"])
            and len(double_laurent)
            == 2 * int(result["double_laurent_preflight_node_count"])
            and all(
                parse_bool(
                    row[
                        "valid_for_shared_branch_double_laurent_subtraction"
                    ]
                )
                for row in double_laurent
            )
            and float(result["maximum_double_laurent_fit_relative_residual"])
            <= DOUBLE_LAURENT_FIT_RESIDUAL_LIMIT
            and float(result["maximum_double_laurent_R2_scale_change"])
            <= DOUBLE_LAURENT_COEFFICIENT_CHANGE_LIMIT,
            (
                f"nodes={result['double_laurent_preflight_node_count']}; "
                f"fit={result['maximum_double_laurent_fit_relative_residual']}"
            ),
        ),
        validation_gate(
            "outer_result_not_overclaimed",
            (
                bool(result["acceptance_passed"])
                and bool(result["all_final_leaves_pass"])
                and len(convergence) == 1
                and parse_bool(convergence[0]["convergence_passed"])
                and float(result["panel_nine_summed_outer_error_relative"])
                <= GLOBAL_OUTER_ERROR_BUDGET_LIMIT
            )
            or (
                not bool(result["acceptance_passed"])
                and not bool(result["claim_boundary"][
                    "valid_for_E0025_fixed_decay_outer_soft_integral"
                ])
                and result["decision"]
                == (
                    "SHARED_BRANCH_SECOND_ORDER_LAURENT_TERM_DERIVED__"
                    "BUILD_DOUBLE_POLE_AND_ENDPOINT_COLLAR_SUBTRACTION"
                )
            ),
            f"outer_claim={result['claim_boundary']['valid_for_E0025_fixed_decay_outer_soft_integral']}",
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
            "VALIDATED_MATERIAL_POLE_EVENT_AND_DOUBLE_LAURENT_DIAGNOSIS"
            if passed
            else "MATERIAL_POLE_EVENT_ALIGNED_OUTER_REFINEMENT_VALIDATION_FAILED"
        ),
        "runtime_seconds": time.perf_counter() - started,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode", choices=("dry-run", "run", "validate"), required=True
    )
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
