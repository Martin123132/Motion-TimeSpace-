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
SOURCE = FUNCTIONAL_RG / "5320"
SHARDS = SOURCE / "shards"
BASELINE_SHARDS = SOURCE / "baseline-shards"

SCRIPT_5318 = SCRIPTS / "Y5_R2FR_5318_regulator_specific_squared_event_outer_repair.py"
RESULT_5318 = FUNCTIONAL_RG / "5318" / "regulator_specific_squared_event_outer_repair_result.json"
VALIDATION_5318 = FUNCTIONAL_RG / "5318" / "regulator_specific_squared_event_outer_repair_validation.csv"
SCRIPT_5319 = SCRIPTS / "Y5_R2FR_5319_regulator_zero_asymptotic_gate.py"
RESULT_5319 = FUNCTIONAL_RG / "5319" / "regulator_zero_asymptotic_gate_result.json"
VALIDATION_5319 = FUNCTIONAL_RG / "5319" / "regulator_zero_asymptotic_gate_validation.csv"

DRY_RUN = SOURCE / "E00125_finite_regulator_extension_dry_run.json"
EVENT_AUDIT = SOURCE / "E00125_panel_nine_events.csv"
SEGMENT_PLAN = SOURCE / "E00125_panel_nine_segment_plan.csv"
INITIAL_PLAN = SOURCE / "E00125_full_outer_initial_plan.csv"
NODE_MANIFEST = SOURCE / "E00125_outer_node_manifest.csv"
OFF_AXIS_AUDIT = SOURCE / "E00125_off_axis_raw_audit.csv"
ADAPTIVE_PANELS = SOURCE / "E00125_adaptive_outer_panel_tree.csv"
FINITE_VALUE = SOURCE / "E00125_finite_regulator_fixed_decay_convergence.csv"
RESULT = SOURCE / "E00125_finite_regulator_extension_result.json"
VALIDATION = SOURCE / "E00125_finite_regulator_extension_validation.csv"
RESIDUAL_VALIDATION = RESIDUALS / "P8_Y5_BRR545_5320_VALIDATION.csv"
STATUS = SOURCE / "status.json"
DOCUMENT = POST / "5320-Y5-R2FR-E00125-finite-regulator-extension.md"

CHECKPOINT = 5320
PARENT_CHECKPOINT = 5319
MARKER = "MTS_5320_E00125_FINITE_REGULATOR_EXTENSION"
REVISION = "E00125-finite-regulator-extension-v1"
NODE_REVISION_PREFIX = "E00125-full-outer-node-v2"
EPSILON_ID = "E00125"
EPSILON = 0.00125
TARGET_REGULATORS = ((EPSILON_ID, EPSILON),)
GLOBAL_OUTER_ERROR_BUDGET_LIMIT = 1.0e-2
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


M5318 = load_module("mts_5318_for_5320", SCRIPT_5318)
M5283 = M5318.M5283
ORIGINAL_RUN_NODE = M5318.run_node
ORIGINAL_SHARD_PATHS = M5318.shard_paths
ORIGINAL_SHARD_COMPLETE = M5318.shard_complete
ORIGINAL_EFFECTIVE_ACCEPTANCE = M5318.effective_acceptance


def read_csv(path: Path) -> list[dict[str, str]]:
    return M5318.read_csv(path)


def write_csv(
    path: Path,
    rows: list[dict[str, Any]],
    leading_fields: list[str] | None = None,
) -> None:
    M5318.write_csv(path, rows, leading_fields)


def read_json(path: Path) -> dict[str, Any]:
    return M5318.read_json(path)


def atomic_json(path: Path, value: Any) -> None:
    M5318.atomic_json(path, value)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_bool(value: Any) -> bool:
    return M5318.parse_bool(value)


def complex_fields(prefix: str, value: complex) -> dict[str, float]:
    return M5318.complex_fields(prefix, value)


def validation_gate(gate: str, passed: bool, detail: str) -> dict[str, Any]:
    return M5318.validation_gate(gate, passed, detail)


def configure_parent_module() -> None:
    M5318.SOURCE = SOURCE
    M5318.SHARDS = SHARDS
    M5318.EVENT_AUDIT = EVENT_AUDIT
    M5318.SEGMENT_PLAN = SEGMENT_PLAN
    M5318.STATUS = STATUS
    M5318.CHECKPOINT = CHECKPOINT
    M5318.REVISION = REVISION
    M5318.NODE_REVISION_PREFIX = NODE_REVISION_PREFIX
    M5318.target_regulators = lambda: TARGET_REGULATORS
    M5318.panel_nodes = generic_panel_nodes
    M5318.split_panel = generic_split_panel
    M5318.run_node = generic_run_node
    M5318.shard_paths = generic_shard_paths
    M5318.shard_complete = generic_shard_complete
    M5318.effective_acceptance = generic_effective_acceptance
    M5318.M5312.SHARDS = BASELINE_SHARDS / EPSILON_ID
    M5318.M5312.CHECKPOINT = CHECKPOINT
    M5318.M5312.NODE_REVISION = f"{NODE_REVISION_PREFIX}-{EPSILON_ID}"
    M5318.M5312.EPSILON_ID = EPSILON_ID
    M5318.M5312.EPSILON = EPSILON
    precision_module = M5318.M5314.M5303.M5280.M5275
    precision_module.mp.mp.dps = max(
        precision_module.mp.mp.dps,
        precision_module.MP_DECIMAL_DIGITS,
    )


def generic_run_node(
    epsilon_id: str,
    node: dict[str, Any],
    contract: list[dict[str, str]],
    expected_plan_sha256: str,
    branch_death: float,
    base_context: dict[str, Any],
    multiplier: float,
) -> dict[str, Any]:
    if int(node["x_panel_index"]) <= 8:
        result = M5318.M5312.run_node(
            node,
            contract,
            expected_plan_sha256,
            base_context,
            multiplier,
        )
        result.update(
            {
                "epsilon_id": epsilon_id,
                "epsilon": EPSILON,
                "initial_segment_id": node["initial_segment_id"],
                "adaptive_panel_id": node["adaptive_panel_id"],
                "adaptive_depth": node["adaptive_depth"],
                "event_type": node["event_type"],
                "transform_direction": node["transform_direction"],
                "transform_coordinate": node["transform_coordinate"],
                "transform_jacobian": node["transform_jacobian"],
                "selected_inner_energy_real": result["inner_energy_Q8_real"],
                "selected_inner_energy_imaginary": result[
                    "inner_energy_Q8_imaginary"
                ],
                "selected_inner_energy_magnitude": result[
                    "inner_energy_Q8_magnitude"
                ],
            }
        )
        atomic_json(generic_shard_paths(epsilon_id, node["node_id"])["result"], result)
        return result
    previous_panel_index = M5318.M5314.TARGET_PANEL_INDEX
    M5318.M5314.TARGET_PANEL_INDEX = int(node["x_panel_index"])
    try:
        return ORIGINAL_RUN_NODE(
            epsilon_id,
            node,
            contract,
            expected_plan_sha256,
            branch_death,
            base_context,
            multiplier,
        )
    finally:
        M5318.M5314.TARGET_PANEL_INDEX = previous_panel_index


def generic_shard_paths(epsilon_id: str, node_id: str) -> dict[str, Path]:
    if node_id.startswith("P09_"):
        return ORIGINAL_SHARD_PATHS(epsilon_id, node_id)
    root = BASELINE_SHARDS / epsilon_id / node_id
    return {
        "root": root,
        "poles": root / "geometric_poles.csv",
        "fits": root / "pole_residue_fits.csv",
        "classifications": root / "pole_classification.csv",
        "integrals": root / "cell_integrals.csv",
        "result": root / "result.json",
    }


def generic_shard_complete(
    epsilon_id: str,
    node: dict[str, Any],
    expected_plan_sha256: str,
) -> bool:
    if int(node["x_panel_index"]) == 9:
        return ORIGINAL_SHARD_COMPLETE(epsilon_id, node, expected_plan_sha256)
    return M5318.M5312.shard_is_complete(node, expected_plan_sha256)


def generic_effective_acceptance(
    epsilon_id: str,
    node: dict[str, Any],
    result: dict[str, Any],
) -> dict[str, Any]:
    if int(node["x_panel_index"]) == 9:
        return ORIGINAL_EFFECTIVE_ACCEPTANCE(epsilon_id, node, result)
    accepted = bool(result["acceptance_passed"])
    return {
        "epsilon_id": epsilon_id,
        "node_id": node["node_id"],
        "adaptive_panel_id": node["adaptive_panel_id"],
        "kernel_acceptance_passed": accepted,
        "off_axis_raw_contract_passes": False,
        "effective_acceptance_passed": accepted,
        "geometric_pole_count": result["geometric_pole_count"],
        "in_support_pole_count": result["in_support_pole_count"],
        "material_simple_pole_count": result["material_simple_pole_count"],
        "removable_zero_residue_pole_count": result[
            "removable_zero_residue_pole_count"
        ],
        "unresolved_pole_count": result["unresolved_pole_count"],
        "raw_inner_Q4_Q8_relative_change": result["inner_Q4_Q8_relative_change"],
        "raw_inner_error_budget_relative": result[
            "inner_energy_error_budget_relative"
        ],
        "reason": (
            "Panels 1-8 use the 5312 all-term geometric-pole scan, two-scale "
            "Laurent classification, material-pole subtraction, and exact analytic "
            "restoration. Panel 9 alone uses the 5318 named-branch collar repair."
        ),
        **{field: False for field in CLAIM_FIELDS},
    }


def generic_panel_nodes(panel: dict[str, Any]) -> list[dict[str, Any]]:
    lower = float(panel["lower_absolute_soft_cosine"])
    upper = float(panel["upper_absolute_soft_cosine"])
    direction = int(panel["transform_direction"])
    panel_index = int(panel["x_panel_index"])
    rows: list[dict[str, Any]] = []
    for order in M5318.OUTER_ORDERS:
        nodes, weights = M5318.np.polynomial.legendre.leggauss(order)
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
                maximum_t = math.sqrt(upper - lower)
                local_t = 0.5 * maximum_t * (1.0 + float(local_node))
                coordinate = event + direction * local_t**2
                mapped_weight = 0.5 * maximum_t * float(weight) * 2.0 * local_t
                transform_coordinate = local_t
                transform_jacobian = 2.0 * local_t
            rows.append(
                {
                    "node_id": (
                        f"P{panel_index:02d}_{panel['adaptive_panel_id']}_"
                        f"Q{order:02d}_N{index:02d}"
                    ),
                    "x_panel_index": panel_index,
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
                    **{field: False for field in M5318.CLAIM_FIELDS},
                }
            )
    return rows


def generic_split_panel(panel: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    lower = float(panel["lower_absolute_soft_cosine"])
    upper = float(panel["upper_absolute_soft_cosine"])
    midpoint = 0.5 * (lower + upper)
    direction = int(panel["transform_direction"])
    common = {
        "epsilon_id": panel["epsilon_id"],
        "epsilon": panel["epsilon"],
        "x_panel_index": panel["x_panel_index"],
        "initial_segment_id": panel["initial_segment_id"],
        "adaptive_depth": int(panel["adaptive_depth"]) + 1,
        "parent_adaptive_panel_id": panel["adaptive_panel_id"],
        "event_type": panel["event_type"],
        **{field: False for field in M5318.CLAIM_FIELDS},
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


def build_initial_plan(segments: list[dict[str, Any]]) -> list[dict[str, Any]]:
    contract = read_csv(M5318.CONTRACT_5312)
    rows: list[dict[str, Any]] = []
    for panel_index in range(1, 9):
        local = [row for row in contract if int(row["x_panel_index"]) == panel_index]
        lower = min(float(row["lower_absolute_soft_cosine"]) for row in local)
        upper = max(float(row["upper_absolute_soft_cosine"]) for row in local)
        rows.append(
            {
                "epsilon_id": EPSILON_ID,
                "epsilon": EPSILON,
                "x_panel_index": panel_index,
                "initial_segment_id": f"B{panel_index:02d}",
                "adaptive_panel_id": f"B{panel_index:02d}",
                "adaptive_depth": 0,
                "parent_adaptive_panel_id": "",
                "lower_absolute_soft_cosine": lower,
                "upper_absolute_soft_cosine": upper,
                "segment_width": upper - lower,
                "transform_direction": 0,
                "event_coordinate": "",
                "event_type": "SMOOTH_BASELINE_PANEL",
                **{field: False for field in CLAIM_FIELDS},
            }
        )
    for segment in segments:
        row = dict(segment)
        row["x_panel_index"] = 9
        rows.append(row)
    write_csv(INITIAL_PLAN, rows, ["x_panel_index", "initial_segment_id"])
    return rows


def plan_sha256(initial: list[dict[str, Any]]) -> str:
    existing = sorted((SHARDS / EPSILON_ID).glob("*/result.json")) + sorted(
        (BASELINE_SHARDS / EPSILON_ID).glob("*/result.json")
    )
    for path in existing:
        try:
            result = read_json(path)
        except Exception:
            continue
        if result.get("node_revision") == f"{NODE_REVISION_PREFIX}-{EPSILON_ID}":
            return str(result["node_plan_sha256"])
    payload = {
        "revision": REVISION,
        "node_revision": f"{NODE_REVISION_PREFIX}-{EPSILON_ID}",
        "node_kernel_contract": "5318-normalized-Laurent-Q8-Q12-full-outer-v1",
        "parent_result_sha256": digest(RESULT_5319),
        "contract_sha256": digest(M5318.CONTRACT_5312),
        "outer_orders": M5318.OUTER_ORDERS,
        "maximum_adaptive_depth": M5318.MAXIMUM_ADAPTIVE_DEPTH,
        "mp_decimal_digits": M5318.M5314.M5303.M5280.M5275.mp.mp.dps,
        "initial_geometry": [
            {
                key: row[key]
                for key in (
                    "x_panel_index",
                    "initial_segment_id",
                    "lower_absolute_soft_cosine",
                    "upper_absolute_soft_cosine",
                    "transform_direction",
                    "event_coordinate",
                )
            }
            for row in initial
        ],
    }
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()


def extended_base_context() -> dict[str, Any]:
    context = M5318.M5314.M5303.synthetic_context()
    inventories = dict(context["inventories"])
    target = complex(-9.0, EPSILON)
    inventories[EPSILON_ID] = {
        "target": target,
        "high_precision_target": (
            M5318.M5314.M5303.M5280.M5275.target_as_mp(target)
        ),
        "components": inventories["E0025"]["components"],
    }
    context["inventories"] = inventories
    return context


def dry_run() -> dict[str, Any]:
    started = time.perf_counter()
    configure_parent_module()
    SOURCE.mkdir(parents=True, exist_ok=True)
    parent = read_json(RESULT_5319)
    parent_validation = read_csv(VALIDATION_5319)
    events = M5318.derive_regulator_events()
    segments = M5318.build_segment_plan(events)
    initial = build_initial_plan(segments)
    acceptance = (
        parent["decision"]
        == "LEADING_ZERO_LIMIT_STABLE__ADD_E00125_TO_CLOSE_REMAINDER_ENVELOPE"
        and parent["required_next_regulator_id"] == EPSILON_ID
        and float(parent["required_next_regulator_epsilon"]) == EPSILON
        and all(parse_bool(row["passed"]) for row in parent_validation)
        and len(events) == 3
        and all(parse_bool(row["event_contract_passes"]) for row in events)
        and len(segments) == 5
        and len(initial) == 13
        and {int(row["x_panel_index"]) for row in initial} == set(range(1, 10))
        and all(float(row["segment_width"]) > 0.0 for row in initial)
        and M5283.formal_inventory_digest()
        == parent["formalization_workbench_end_digest"]
    )
    result = {
        "checkpoint": CHECKPOINT,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "mode": "dry-run",
        "acceptance_passed": acceptance,
        "decision": (
            "DRY_RUN_ACCEPTED__RUN_E00125_FULL_OUTER_INTEGRAL"
            if acceptance
            else "E00125_FINITE_REGULATOR_EXTENSION_DRY_RUN_BLOCKED"
        ),
        "event_count": len(events),
        "initial_panel_count": len(initial),
        "plan_sha256": plan_sha256(initial),
        "runtime_seconds": time.perf_counter() - started,
    }
    atomic_json(DRY_RUN, result)
    return result


def source_rows() -> list[dict[str, str]]:
    paths = (
        Path(__file__).resolve(),
        SCRIPT_5318,
        RESULT_5318,
        VALIDATION_5318,
        SCRIPT_5319,
        RESULT_5319,
        VALIDATION_5319,
        M5318.CONTRACT_5312,
        M5318.SUPPORT_EVENTS_5313,
        M5318.EVENTS_5314,
        DRY_RUN,
        EVENT_AUDIT,
        SEGMENT_PLAN,
        INITIAL_PLAN,
    )
    return [{"path": str(path), "sha256": digest(path)} for path in paths]


def execute(runtime_limit_seconds: float) -> dict[str, Any]:
    started = time.perf_counter()
    configure_parent_module()
    dry = dry_run()
    if not dry["acceptance_passed"]:
        raise RuntimeError("5320 dry run did not pass")
    events = read_csv(EVENT_AUDIT)
    initial = read_csv(INITIAL_PLAN)
    contract = read_csv(M5318.CONTRACT_5312)
    branch_death = float(
        next(row for row in events if row["event_type"] == "SHARED_BRANCH_DEATH")[
            "event_coordinate"
        ]
    )
    expected = plan_sha256(initial)
    base_context = extended_base_context()
    multiplier = M5318.M5314.M5309.physical_multiplier()
    old = M5318.kernel_context(EPSILON_ID, EPSILON)
    configure_parent_module()
    try:
        panel_rows, leaves, encountered, audits, paused = M5318.refine_regulator(
            EPSILON_ID,
            [dict(row) for row in initial],
            contract,
            expected,
            branch_death,
            base_context,
            multiplier,
            started,
            runtime_limit_seconds,
        )
    finally:
        M5318.restore_kernel_context(old)
    for row in panel_rows:
        row["epsilon_id"] = EPSILON_ID
        row["epsilon"] = EPSILON
    for row in leaves:
        row["epsilon_id"] = EPSILON_ID
        row["epsilon"] = EPSILON
    manifest_rows: list[dict[str, Any]] = []
    for node_id, node in encountered.items():
        complete = M5318.shard_complete(EPSILON_ID, node, expected)
        node_result = (
            read_json(M5318.shard_paths(EPSILON_ID, node_id)["result"])
            if complete
            else {}
        )
        audit = audits.get(node_id, {})
        manifest_rows.append(
            {
                "epsilon_id": EPSILON_ID,
                **node,
                "shard_state": (
                    "COMPLETE_PASS"
                    if complete and bool(audit.get("effective_acceptance_passed"))
                    else ("COMPLETE_FAIL" if complete else "PENDING")
                ),
                "kernel_acceptance_passed": audit.get("kernel_acceptance_passed", False),
                "off_axis_raw_contract_passes": audit.get(
                    "off_axis_raw_contract_passes", False
                ),
                "effective_acceptance_passed": audit.get(
                    "effective_acceptance_passed", False
                ),
                "runtime_seconds": node_result.get("runtime_seconds", ""),
                "node_result_path": str(
                    M5318.shard_paths(EPSILON_ID, node_id)["result"]
                ),
                **{field: False for field in CLAIM_FIELDS},
            }
        )
    write_csv(NODE_MANIFEST, manifest_rows, ["epsilon_id", "node_id"])
    write_csv(OFF_AXIS_AUDIT, list(audits.values()), ["epsilon_id", "node_id"])
    write_csv(ADAPTIVE_PANELS, panel_rows, ["x_panel_index", "adaptive_panel_id"])
    complete = not paused and len(leaves) >= 13
    all_leaf_gates = complete and all(bool(row["adaptive_gate_passes"]) for row in leaves)
    low = (
        sum(
            complex(
                float(row["outer_Q8_inner_Q12_real"]),
                float(row["outer_Q8_inner_Q12_imaginary"]),
            )
            for row in leaves
        )
        if complete
        else 0.0j
    )
    high = (
        sum(
            complex(
                float(row["outer_Q12_inner_Q12_real"]),
                float(row["outer_Q12_inner_Q12_imaginary"]),
            )
            for row in leaves
        )
        if complete
        else 0.0j
    )
    error = (
        sum(float(row["outer_Q8_Q12_absolute_change"]) for row in leaves)
        if complete
        else math.inf
    )
    relative_error = error / max(abs(high), 1.0e-12)
    accepted = complete and all_leaf_gates and relative_error <= GLOBAL_OUTER_ERROR_BUDGET_LIMIT
    if paused:
        decision = "E00125_FULL_OUTER_INTEGRAL_PAUSED__RESUME_SAVED_SHARDS"
    elif accepted:
        decision = "E00125_FINITE_REGULATOR_CONVERGED__REFIT_ZERO_LIMIT"
    else:
        decision = "E00125_FINITE_REGULATOR_LOCALIZES_REMAINING_FAILURES"
    finite_rows = [
        {
            "epsilon_id": EPSILON_ID,
            "epsilon": EPSILON,
            "method": "FULL_OUTER_EVENT_ALIGNED_Q8_Q12_ADAPTIVE_REPAIR",
            "fixed_decay_integral_real": high.real if complete else "",
            "fixed_decay_integral_imaginary": high.imag if complete else "",
            "fixed_decay_error_absolute_conservative": error if complete else "",
            "fixed_decay_error_relative_conservative": relative_error if complete else "",
            "finite_regulator_fixed_decay_integral_accepted": accepted,
            **{field: False for field in CLAIM_FIELDS},
        }
    ]
    write_csv(FINITE_VALUE, finite_rows, ["epsilon_id"])
    parent = read_json(RESULT_5319)
    formal_end = M5283.formal_inventory_digest()
    result = {
        "checkpoint": CHECKPOINT,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "mode": "E00125-full-outer-finite-regulator-extension",
        "acceptance_passed": accepted,
        "decision": decision,
        "encountered_outer_node_count": len(encountered),
        "completed_outer_node_count": sum(
            row["shard_state"] != "PENDING" for row in manifest_rows
        ),
        "failed_outer_inner_node_count": sum(
            row["shard_state"] == "COMPLETE_FAIL" for row in manifest_rows
        ),
        "adaptive_panel_count": len(panel_rows),
        "adaptive_leaf_count": len(leaves),
        "all_adaptive_leaf_gates_pass": all_leaf_gates,
        **complex_fields("fixed_decay_integral", high),
        "fixed_decay_error_absolute_conservative": error,
        "fixed_decay_error_relative_conservative": relative_error,
        "formalization_workbench_reference_digest": parent[
            "formalization_workbench_end_digest"
        ],
        "formalization_workbench_end_digest": formal_end,
        "formalization_workbench_modified_file_count": (
            0
            if formal_end == parent["formalization_workbench_end_digest"]
            else -1
        ),
        "claim_boundary": {
            **{field: False for field in CLAIM_FIELDS},
            "reason": (
                "This is one additional finite regulator at one fixed decay angle. "
                "The regulator-zero refit and every broader claim remain separate."
            ),
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


def render_document(result: dict[str, Any], validation_passed: bool) -> None:
    lines = [
        "# 5320 - E00125 finite-regulator extension",
        "",
        "## Method",
        "",
        "The 5319 complete logarithmic remainder envelope missed the inherited",
        "one-percent zero-limit gate by a narrow margin.  This checkpoint therefore",
        "computes the requested `epsilon=0.00125` value directly.  Panels 1-8 use",
        "adaptive Q8/Q12 outer quadrature; panel 9 derives its own support-entry,",
        "support-exit, and branch-death geometry and uses exact squared-event Jacobians.",
        "Every inner integral uses the normalized Laurent/raw-contour contract from 5318.",
        "",
        "## Result",
        "",
        f"- encountered nodes: `{result['encountered_outer_node_count']}`;",
        f"- completed nodes: `{result['completed_outer_node_count']}`;",
        f"- failed inner nodes: `{result['failed_outer_inner_node_count']}`;",
        f"- fixed-decay value: `{result['fixed_decay_integral_real']:.12g}` "
        f"`{result['fixed_decay_integral_imaginary']:+.12g} i`;",
        f"- conservative relative error: `{result['fixed_decay_error_relative_conservative']:.12g}`;",
        f"- decision: **{result['decision']}**;",
        f"- validation: **{'PASS' if validation_passed else 'FAIL'}**.",
        "",
        "## Claim boundary",
        "",
        "A passing result adds one finite-regulator fixed-decay point only.  It does not",
        "itself establish the regulator-zero limit, decay-angle integration, full",
        "phase-space coefficient, UV behavior, local GR, or the full MTS theory.",
    ]
    DOCUMENT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def validate_outputs() -> dict[str, Any]:
    started = time.perf_counter()
    configure_parent_module()
    result = read_json(RESULT)
    dry = read_json(DRY_RUN)
    manifest = read_csv(NODE_MANIFEST)
    panels = read_csv(ADAPTIVE_PANELS)
    finite = read_csv(FINITE_VALUE)
    leaves = [row for row in panels if parse_bool(row["adaptive_leaf"])]
    source_current = all(
        Path(row["path"]).exists()
        and digest(Path(row["path"])) == row["sha256"]
        for row in result["source_files"]
    )
    gates = [
        validation_gate(
            "E00125_geometry_and_full_plan_pass",
            bool(dry["acceptance_passed"])
            and int(dry["event_count"]) == 3
            and int(dry["initial_panel_count"]) == 13,
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
            "all_adaptive_leaves_pass",
            len(leaves) >= 13
            and all(parse_bool(row["adaptive_gate_passes"]) for row in leaves),
            f"leaves={len(leaves)}",
        ),
        validation_gate(
            "E00125_full_conservative_budget_passes",
            len(finite) == 1
            and parse_bool(finite[0]["finite_regulator_fixed_decay_integral_accepted"])
            and float(finite[0]["fixed_decay_error_relative_conservative"])
            <= GLOBAL_OUTER_ERROR_BUDGET_LIMIT
            and bool(result["acceptance_passed"]),
            str(result["fixed_decay_error_relative_conservative"]),
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
            "finite-regulator fixed-decay point only",
        ),
    ]
    passed = all(bool(row["passed"]) for row in gates)
    write_csv(VALIDATION, gates, ["gate"])
    write_csv(RESIDUAL_VALIDATION, gates, ["gate"])
    render_document(result, passed)
    return {
        "checkpoint": CHECKPOINT,
        "mode": "validation",
        "acceptance_passed": passed,
        "decision": (
            "VALIDATED_E00125_FINITE_REGULATOR_EXTENSION"
            if passed
            else "E00125_FINITE_REGULATOR_EXTENSION_VALIDATION_FAILED"
        ),
        "runtime_seconds": time.perf_counter() - started,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("dry-run", "run", "validate"), required=True)
    parser.add_argument("--max-runtime-hours", type=float, default=1.5)
    return parser.parse_args()


def main() -> int:
    configure_parent_module()
    M5318.M5312.set_below_normal_priority()
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
