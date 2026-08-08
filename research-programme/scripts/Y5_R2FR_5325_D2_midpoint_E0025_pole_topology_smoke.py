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
SOURCE = FUNCTIONAL_RG / "5325"
SHARDS = SOURCE / "shards"

SCRIPT_5320 = SCRIPTS / "Y5_R2FR_5320_E00125_finite_regulator_extension.py"
SCRIPT_5324 = SCRIPTS / "Y5_R2FR_5324_decay_angle_measure_symmetry_topology_preflight.py"
RESULT_5324 = FUNCTIONAL_RG / "5324" / "decay_angle_measure_symmetry_topology_preflight_result.json"
VALIDATION_5324 = FUNCTIONAL_RG / "5324" / "decay_angle_measure_symmetry_topology_preflight_validation.csv"
FULL_CONTRACT_5324 = FUNCTIONAL_RG / "5324" / "decay_angle_energy_soft_cubature_contract.csv"
NODE_SUMMARY_5324 = FUNCTIONAL_RG / "5324" / "decay_angle_topology_node_summary.csv"

DRY_RUN = SOURCE / "D2_midpoint_E0025_pole_topology_smoke_dry_run.json"
REDUCED_CONTRACT = SOURCE / "D2_midpoint_reduced_MC04_cubature_contract.csv"
IDENTITY_AUDIT = SOURCE / "D2_midpoint_MC04_MC12_identity_audit.csv"
NODE_PLAN = SOURCE / "D2_midpoint_E0025_outer_node_plan.csv"
NODE_MANIFEST = SOURCE / "D2_midpoint_E0025_outer_node_manifest.csv"
ALL_POLES = SOURCE / "D2_midpoint_E0025_geometric_poles.csv"
ALL_FITS = SOURCE / "D2_midpoint_E0025_pole_residue_fits.csv"
ALL_CLASSIFICATIONS = SOURCE / "D2_midpoint_E0025_pole_classification.csv"
ALL_CELL_INTEGRALS = SOURCE / "D2_midpoint_E0025_cell_integrals.csv"
OUTER_TOTALS = SOURCE / "D2_midpoint_E0025_outer_totals.csv"
PANEL_CONVERGENCE = SOURCE / "D2_midpoint_E0025_panel_convergence.csv"
MATERIAL_TOPOLOGY = SOURCE / "D2_midpoint_E0025_material_pole_topology.csv"
RESULT = SOURCE / "D2_midpoint_E0025_pole_topology_smoke_result.json"
VALIDATION = SOURCE / "D2_midpoint_E0025_pole_topology_smoke_validation.csv"
RESIDUAL_VALIDATION = RESIDUALS / "P8_Y5_BRR545_5325_VALIDATION.csv"
STATUS = SOURCE / "status.json"
DOCUMENT = POST / "5325-Y5-R2FR-D2-midpoint-E0025-pole-topology-smoke.md"

CHECKPOINT = 5325
PARENT_CHECKPOINT = 5324
MARKER = "MTS_5325_D2_MIDPOINT_E0025_POLE_TOPOLOGY_SMOKE"
REVISION = "D2-midpoint-E0025-pole-topology-smoke-v1"
NODE_REVISION = "D2-midpoint-E0025-pole-topology-node-v1"
DECAY_NODE_ID = "D2_MID"
EPSILON_ID = "E0025"
EPSILON = 0.0025
EXPECTED_CELL_COUNT = 44
EXPECTED_PANEL_COUNT = 11
EXPECTED_NODE_COUNT = 66
DEFAULT_RUNTIME_LIMIT_SECONDS = 3.25 * 3600.0
CLAIM_FIELDS = (
    "valid_for_D2_E0025_fixed_decay_integral",
    "valid_for_D2_regulator_zero_limit",
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


M5320 = load_module("mts_5320_for_5325", SCRIPT_5320)
M5312 = M5320.M5318.M5312
M5283 = M5320.M5283


def read_csv(path: Path) -> list[dict[str, str]]:
    return M5320.read_csv(path)


def write_csv(
    path: Path,
    rows: list[dict[str, Any]],
    leading_fields: list[str] | None = None,
) -> None:
    M5320.write_csv(path, rows, leading_fields)


def read_json(path: Path) -> dict[str, Any]:
    return M5320.read_json(path)


def atomic_json(path: Path, value: Any) -> None:
    M5320.atomic_json(path, value)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_bool(value: Any) -> bool:
    return M5320.parse_bool(value)


def complex_fields(prefix: str, value: complex) -> dict[str, float]:
    return M5320.complex_fields(prefix, value)


def validation_gate(gate: str, passed: bool, detail: str) -> dict[str, Any]:
    return M5320.validation_gate(gate, passed, detail)


def decay_coordinate() -> float:
    row = next(
        row
        for row in read_csv(NODE_SUMMARY_5324)
        if row["decay_node_id"] == DECAY_NODE_ID
    )
    return float(row["absolute_decay_cosine"])


def configure_kernel() -> dict[str, Any]:
    old = {
        "decay": M5312.M5308.M5302.EDGE_DECAY_ABSOLUTE,
        "epsilon_id": M5312.EPSILON_ID,
        "epsilon": M5312.EPSILON,
        "shards": M5312.SHARDS,
        "node_revision": M5312.NODE_REVISION,
        "checkpoint": M5312.CHECKPOINT,
        "parent_epsilon_id": M5312.M5311.EPSILON_ID,
        "parent_epsilon": M5312.M5311.EPSILON,
    }
    M5312.M5308.M5302.EDGE_DECAY_ABSOLUTE = decay_coordinate()
    M5312.EPSILON_ID = EPSILON_ID
    M5312.EPSILON = EPSILON
    M5312.SHARDS = SHARDS
    M5312.NODE_REVISION = NODE_REVISION
    M5312.CHECKPOINT = CHECKPOINT
    M5312.M5311.EPSILON_ID = EPSILON_ID
    M5312.M5311.EPSILON = EPSILON
    M5312.set_below_normal_priority()
    M5312.mp.mp.dps = M5312.M5280.MP_DECIMAL_DIGITS
    M5312.M5301.configure_reused_pipeline()
    return old


def restore_kernel(old: dict[str, Any]) -> None:
    M5312.M5311.EPSILON_ID = old["parent_epsilon_id"]
    M5312.M5311.EPSILON = old["parent_epsilon"]
    M5312.CHECKPOINT = old["checkpoint"]
    M5312.NODE_REVISION = old["node_revision"]
    M5312.SHARDS = old["shards"]
    M5312.EPSILON = old["epsilon"]
    M5312.EPSILON_ID = old["epsilon_id"]
    M5312.M5308.M5302.EDGE_DECAY_ABSOLUTE = old["decay"]


def D2_source_contract() -> list[dict[str, str]]:
    return [
        row
        for row in read_csv(FULL_CONTRACT_5324)
        if row["decay_node_id"] == DECAY_NODE_ID
    ]


def build_reduced_contract() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in D2_source_contract():
        coefficients = M5312.reduced_coefficients(source["active_term_ids"])
        rows.append(
            {
                "decay_node_id": DECAY_NODE_ID,
                "absolute_decay_cosine": decay_coordinate(),
                "contract_index": int(source["contract_index"]),
                "x_panel_index": int(source["x_panel_index"]),
                "chamber_index": int(source["chamber_index"]),
                "lower_absolute_soft_cosine": source[
                    "lower_absolute_soft_cosine"
                ],
                "upper_absolute_soft_cosine": source[
                    "upper_absolute_soft_cosine"
                ],
                "lower_energy_boundary": source["lower_energy_boundary"],
                "upper_energy_boundary": source["upper_energy_boundary"],
                "original_active_term_ids": source["active_term_ids"],
                "parent_evaluation_term_ids": source["evaluation_term_ids"],
                "reduced_MC04_coefficients": M5312.encode_coefficients(
                    coefficients
                ),
                "reduced_MC04_term_ids": "|".join(coefficients),
                "reduced_MC04_term_count": len(coefficients),
                "algebraically_zero_cell": not coefficients,
                "zero_cell_derived_from_active_orbit": True,
                "parent_evaluation_representative_is_empty": not M5312.term_ids(
                    source["evaluation_term_ids"]
                ),
                "valid_for_MC04_MC12_identity_reduction": parse_bool(
                    source["valid_for_pair_orbit_reduction"]
                ),
                **{field: False for field in CLAIM_FIELDS},
            }
        )
    write_csv(
        REDUCED_CONTRACT,
        rows,
        ["decay_node_id", "contract_index", "x_panel_index", "chamber_index"],
    )
    return rows


def node_plan_sha256(plan: list[dict[str, Any]]) -> str:
    payload = {
        "revision": REVISION,
        "node_revision": NODE_REVISION,
        "decay_node_id": DECAY_NODE_ID,
        "absolute_decay_cosine": decay_coordinate(),
        "epsilon_id": EPSILON_ID,
        "epsilon": EPSILON,
        "contract_sha256": digest(REDUCED_CONTRACT),
        "outer_orders": M5312.OUTER_ORDERS,
        "energy_orders": M5312.ENERGY_ORDERS,
        "nodes": [
            {
                key: row[key]
                for key in (
                    "node_id",
                    "x_panel_index",
                    "outer_order",
                    "absolute_soft_cosine",
                    "mapped_outer_weight",
                )
            }
            for row in plan
        ],
    }
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True).encode("utf-8")
    ).hexdigest()


def source_rows() -> list[dict[str, str]]:
    paths = (
        Path(__file__).resolve(),
        SCRIPT_5320,
        SCRIPT_5324,
        RESULT_5324,
        VALIDATION_5324,
        FULL_CONTRACT_5324,
        NODE_SUMMARY_5324,
        DRY_RUN,
        REDUCED_CONTRACT,
        IDENTITY_AUDIT,
        NODE_PLAN,
    )
    return [{"path": str(path), "sha256": digest(path)} for path in paths]


def dry_run() -> dict[str, Any]:
    started = time.perf_counter()
    SOURCE.mkdir(parents=True, exist_ok=True)
    old = configure_kernel()
    try:
        parent = read_json(RESULT_5324)
        parent_validation = read_csv(VALIDATION_5324)
        node_summary = next(
            row
            for row in read_csv(NODE_SUMMARY_5324)
            if row["decay_node_id"] == DECAY_NODE_ID
        )
        contract = build_reduced_contract()
        plan = M5312.build_node_plan(contract)
        write_csv(NODE_PLAN, plan, ["x_panel_index", "outer_order", "node_id"])
        evaluate = M5312.M5305.component_evaluator(M5312.M5303.synthetic_context())
        identity = M5312.identity_audit_rows(contract, evaluate)
        write_csv(
            IDENTITY_AUDIT,
            identity,
            ["contract_index", "epsilon_id", "MC12_term_id"],
        )
        panel_ids = sorted({int(row["x_panel_index"]) for row in contract})
        checks = {
            "parent_5324_accepted": bool(parent["acceptance_passed"]),
            "parent_5324_validation_passes": all(
                parse_bool(row["passed"]) for row in parent_validation
            ),
            "D2_midpoint_topology_preflight_passes": parse_bool(
                node_summary["topology_node_preflight_passes"]
            ),
            "D2_contract_has_expected_cells_and_panels": (
                len(contract) == EXPECTED_CELL_COUNT
                and panel_ids == list(range(1, EXPECTED_PANEL_COUNT + 1))
            ),
            "all_reduced_cells_are_derived_and_parent_topology_safe": all(
                parse_bool(row["zero_cell_derived_from_active_orbit"])
                and parse_bool(row["valid_for_MC04_MC12_identity_reduction"])
                for row in contract
            ),
            "MC04_MC12_identity_transfers_at_D2": bool(identity)
            and all(
                parse_bool(row["valid_for_MC04_MC12_identity_transfer"])
                for row in identity
            ),
            "Q2_Q4_plan_covers_all_eleven_panels": (
                len(plan) == EXPECTED_NODE_COUNT
                and {int(row["x_panel_index"]) for row in plan}
                == set(range(1, EXPECTED_PANEL_COUNT + 1))
                and all(
                    parse_bool(row["valid_for_resumable_outer_soft_node"])
                    for row in plan
                )
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
            "decision": (
                "DRY_RUN_ACCEPTED__RUN_D2_E0025_POLE_TOPOLOGY_SMOKE"
                if accepted
                else "D2_E0025_POLE_TOPOLOGY_SMOKE_DRY_RUN_BLOCKED"
            ),
            "decay_node_id": DECAY_NODE_ID,
            "absolute_decay_cosine": decay_coordinate(),
            "reduced_contract_cell_count": len(contract),
            "soft_panel_count": len(panel_ids),
            "planned_node_count": len(plan),
            "identity_audit_row_count": len(identity),
            "contract_sha256": digest(REDUCED_CONTRACT),
            "node_plan_sha256": node_plan_sha256(plan),
            "runtime_seconds": time.perf_counter() - started,
            **{field: False for field in CLAIM_FIELDS},
        }
        atomic_json(DRY_RUN, result)
        return result
    finally:
        restore_kernel(old)


def load_validated_dry_run() -> dict[str, Any]:
    required = (DRY_RUN, REDUCED_CONTRACT, IDENTITY_AUDIT, NODE_PLAN)
    if not all(path.exists() for path in required):
        return dry_run()
    cached = read_json(DRY_RUN)
    plan = read_csv(NODE_PLAN)
    identity = read_csv(IDENTITY_AUDIT)
    current = (
        bool(cached.get("acceptance_passed"))
        and cached.get("decision")
        == "DRY_RUN_ACCEPTED__RUN_D2_E0025_POLE_TOPOLOGY_SMOKE"
        and cached.get("contract_sha256") == digest(REDUCED_CONTRACT)
        and cached.get("node_plan_sha256") == node_plan_sha256(plan)
        and len(plan) == EXPECTED_NODE_COUNT
        and bool(identity)
        and all(
            parse_bool(row["valid_for_MC04_MC12_identity_transfer"])
            for row in identity
        )
        and all(
            parse_bool(row["passed"]) for row in read_csv(VALIDATION_5324)
        )
    )
    return cached if current else dry_run()


def aggregate_outer_integrals(
    plan: list[dict[str, str]],
    node_results: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    result_lookup = {row["node_id"]: row for row in node_results}
    outer_rows: list[dict[str, Any]] = []
    panel_values: dict[tuple[int, int, int], complex] = {}
    for outer_order in M5312.OUTER_ORDERS:
        selected = [
            row for row in plan if int(row["outer_order"]) == outer_order
        ]
        for energy_order in M5312.ENERGY_ORDERS:
            total = 0.0j
            for node in selected:
                result = result_lookup[node["node_id"]]
                value = complex(
                    float(result[f"inner_energy_Q{energy_order}_real"]),
                    float(result[f"inner_energy_Q{energy_order}_imaginary"]),
                )
                contribution = float(node["mapped_outer_weight"]) * value
                total += contribution
                key = (
                    int(node["x_panel_index"]),
                    outer_order,
                    energy_order,
                )
                panel_values[key] = panel_values.get(key, 0.0j) + contribution
            outer_rows.append(
                {
                    "decay_node_id": DECAY_NODE_ID,
                    "absolute_decay_cosine": decay_coordinate(),
                    "epsilon_id": EPSILON_ID,
                    "epsilon": EPSILON,
                    "outer_order": outer_order,
                    "energy_order": energy_order,
                    "node_count": len(selected),
                    **complex_fields("fixed_decay_outer_soft_integral", total),
                    **{field: False for field in CLAIM_FIELDS},
                }
            )
    outer_lookup = {
        (int(row["outer_order"]), int(row["energy_order"])): complex(
            float(row["fixed_decay_outer_soft_integral_real"]),
            float(row["fixed_decay_outer_soft_integral_imaginary"]),
        )
        for row in outer_rows
    }
    selected_energy_order = max(M5312.ENERGY_ORDERS)
    selected_outer_order = max(M5312.OUTER_ORDERS)
    comparison_outer_order = min(M5312.OUTER_ORDERS)
    selected_value = outer_lookup[(selected_outer_order, selected_energy_order)]
    outer_change = M5312.relative_complex_change(
        outer_lookup[(comparison_outer_order, selected_energy_order)],
        selected_value,
    )
    inner_budget = sum(
        abs(float(node["mapped_outer_weight"]))
        * float(result_lookup[node["node_id"]]["inner_energy_error_budget_absolute"])
        for node in plan
        if int(node["outer_order"]) == selected_outer_order
    )
    inner_budget_relative = inner_budget / max(abs(selected_value), 1.0e-12)
    panel_rows: list[dict[str, Any]] = []
    panel_ids = sorted({int(row["x_panel_index"]) for row in plan})
    for panel_index in panel_ids:
        low = panel_values[
            (panel_index, comparison_outer_order, selected_energy_order)
        ]
        high = panel_values[
            (panel_index, selected_outer_order, selected_energy_order)
        ]
        change = M5312.relative_complex_change(low, high)
        panel_rows.append(
            {
                "x_panel_index": panel_index,
                **complex_fields(
                    f"outer_Q{comparison_outer_order}_energy_Q{selected_energy_order}",
                    low,
                ),
                **complex_fields(
                    f"outer_Q{selected_outer_order}_energy_Q{selected_energy_order}",
                    high,
                ),
                f"outer_Q{comparison_outer_order}_Q{selected_outer_order}_relative_change": change,
                "passes_outer_panel_gate": (
                    change <= M5312.OUTER_RELATIVE_CHANGE_LIMIT
                ),
                **{field: False for field in CLAIM_FIELDS},
            }
        )
    metrics = {
        "outer_relative_change": outer_change,
        "inner_error_budget_absolute": inner_budget,
        "inner_error_budget_relative": inner_budget_relative,
        **complex_fields("selected_D2_E0025_fixed_decay_integral", selected_value),
    }
    return outer_rows, panel_rows, metrics


def material_topology_rows(
    poles: list[dict[str, str]],
    classifications: list[dict[str, str]],
) -> list[dict[str, Any]]:
    classification_lookup = {
        (row["node_id"], row["term_id"], row["pole_id"]): row
        for row in classifications
    }
    groups: dict[tuple[Any, ...], list[tuple[dict[str, str], dict[str, str]]]] = {}
    for pole in poles:
        classification = classification_lookup.get(
            (pole["node_id"], pole["term_id"], pole["pole_id"]), {}
        )
        key = (
            int(pole["x_panel_index"]),
            pole["term_id"],
            pole["primary_surface_id"],
            parse_bool(pole["inside_reduced_term_support"]),
            parse_bool(classification.get("material_simple_pole", False)),
            parse_bool(classification.get("removable_zero_residue_pole", False)),
        )
        groups.setdefault(key, []).append((pole, classification))
    rows: list[dict[str, Any]] = []
    for key, members in sorted(groups.items(), key=lambda item: item[0]):
        panel, term, surface, inside, material, removable = key
        coordinates = [float(pole["absolute_soft_cosine"]) for pole, _ in members]
        residue_magnitudes = [
            float(classification["selected_residue_magnitude"])
            for _, classification in members
            if classification.get("selected_residue_magnitude") not in (None, "")
        ]
        rows.append(
            {
                "x_panel_index": panel,
                "term_id": term,
                "primary_surface_id": surface,
                "inside_reduced_term_support": inside,
                "material_simple_pole": material,
                "removable_zero_residue_pole": removable,
                "sample_count": len(members),
                "minimum_absolute_soft_cosine": min(coordinates),
                "maximum_absolute_soft_cosine": max(coordinates),
                "maximum_selected_residue_magnitude": (
                    max(residue_magnitudes) if residue_magnitudes else ""
                ),
                **{field: False for field in CLAIM_FIELDS},
            }
        )
    return rows


def execute(runtime_limit_seconds: float) -> dict[str, Any]:
    started = time.perf_counter()
    old = configure_kernel()
    try:
        dry = load_validated_dry_run()
        if not dry["acceptance_passed"]:
            raise RuntimeError("5325 dry run did not pass")
        contract = read_csv(REDUCED_CONTRACT)
        plan = read_csv(NODE_PLAN)
        expected = str(dry["node_plan_sha256"])
        base_context = M5312.M5303.synthetic_context()
        multiplier = M5312.M5309.physical_multiplier()
        paused = False
        for node_index, node in enumerate(plan, start=1):
            if M5312.shard_is_complete(node, expected):
                continue
            if time.perf_counter() - started >= runtime_limit_seconds:
                paused = True
                break
            M5312.run_node(node, contract, expected, base_context, multiplier)
            atomic_json(
                STATUS,
                {
                    "checkpoint": CHECKPOINT,
                    "state": "RUNNING",
                    "stage": "D2_E0025_Q2_Q4_POLE_TOPOLOGY_SMOKE",
                    "completed_plan_position": node_index,
                    "planned_node_count": len(plan),
                },
            )
        manifest = M5312.node_manifest_rows(plan, expected)
        write_csv(NODE_MANIFEST, manifest, ["x_panel_index", "outer_order", "node_id"])
        node_results, poles, fits, classifications, integrals = (
            M5312.collect_shard_rows(plan, expected)
        )
        write_csv(ALL_POLES, poles, ["x_panel_index", "node_id", "term_id", "pole_id"])
        write_csv(ALL_FITS, fits, ["x_panel_index", "node_id", "term_id", "pole_id"])
        write_csv(
            ALL_CLASSIFICATIONS,
            classifications,
            ["x_panel_index", "node_id", "term_id", "pole_id"],
        )
        write_csv(
            ALL_CELL_INTEGRALS,
            integrals,
            ["x_panel_index", "node_id", "contract_index", "energy_order"],
        )
        topology = material_topology_rows(poles, classifications)
        write_csv(
            MATERIAL_TOPOLOGY,
            topology,
            ["x_panel_index", "term_id", "primary_surface_id"],
        )
        complete_count = sum(row["shard_state"] != "PENDING" for row in manifest)
        complete = complete_count == len(plan)
        all_nodes_pass = complete and all(
            row["shard_state"] == "COMPLETE_PASS" for row in manifest
        )
        formal_end = M5283.formal_inventory_digest()
        parent = read_json(RESULT_5324)
        if not complete:
            result = {
                "checkpoint": CHECKPOINT,
                "parent_checkpoint": PARENT_CHECKPOINT,
                "marker": MARKER,
                "revision": REVISION,
                "mode": "D2-midpoint-E0025-pole-topology-smoke-partial",
                "acceptance_passed": False,
                "decision": "D2_E0025_SMOKE_PAUSED__RESUME_SAVED_SHARDS",
                "decay_node_id": DECAY_NODE_ID,
                "absolute_decay_cosine": decay_coordinate(),
                "completed_node_count": complete_count,
                "planned_node_count": len(plan),
                "remaining_node_count": len(plan) - complete_count,
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
                    "reason": "The resumable E0025 node scan is incomplete.",
                },
                "source_files": source_rows(),
                "runtime_seconds": time.perf_counter() - started,
            }
            atomic_json(RESULT, result)
            atomic_json(
                STATUS,
                {
                    "checkpoint": CHECKPOINT,
                    "state": "PAUSED_RESUMABLE",
                    "decision": result["decision"],
                    "completed_node_count": complete_count,
                    "planned_node_count": len(plan),
                },
            )
            return result
        outer_rows, panel_rows, metrics = aggregate_outer_integrals(
            plan, node_results
        )
        write_csv(
            OUTER_TOTALS,
            outer_rows,
            ["decay_node_id", "epsilon_id", "outer_order", "energy_order"],
        )
        write_csv(PANEL_CONVERGENCE, panel_rows, ["x_panel_index"])
        unresolved_count = sum(
            not parse_bool(row["pole_classification_resolved"])
            for row in classifications
        )
        fixed_decay_accepted = (
            all_nodes_pass
            and float(metrics["outer_relative_change"])
            <= M5312.OUTER_RELATIVE_CHANGE_LIMIT
            and float(metrics["inner_error_budget_relative"])
            <= M5312.INNER_ERROR_BUDGET_LIMIT
        )
        diagnostic_accepted = (
            all_nodes_pass
            and unresolved_count == 0
            and formal_end == parent["formalization_workbench_end_digest"]
        )
        failed_panels = [
            int(row["x_panel_index"])
            for row in panel_rows
            if not parse_bool(row["passes_outer_panel_gate"])
        ]
        decision = (
            "D2_E0025_COARSE_FIXED_DECAY_ACCEPTED__BUILD_D2_REGULATOR_LADDER"
            if fixed_decay_accepted
            else (
                "D2_E0025_POLE_TOPOLOGY_LOCALIZED__BUILD_EVENT_ALIGNED_REFINEMENT"
                if diagnostic_accepted
                else "D2_E0025_INNER_KERNEL_FAILURES_LOCALIZED__REPAIR_BEFORE_REFINEMENT"
            )
        )
        result = {
            "checkpoint": CHECKPOINT,
            "parent_checkpoint": PARENT_CHECKPOINT,
            "marker": MARKER,
            "revision": REVISION,
            "mode": "D2-midpoint-E0025-pole-topology-smoke",
            "acceptance_passed": diagnostic_accepted,
            "finite_regulator_fixed_decay_integral_accepted": fixed_decay_accepted,
            "decision": decision,
            "decay_node_id": DECAY_NODE_ID,
            "absolute_decay_cosine": decay_coordinate(),
            "completed_node_count": complete_count,
            "planned_node_count": len(plan),
            "all_inner_nodes_pass": all_nodes_pass,
            "geometric_pole_count": len(poles),
            "material_simple_pole_count": sum(
                parse_bool(row["material_simple_pole"])
                for row in classifications
            ),
            "in_support_material_simple_pole_count": sum(
                parse_bool(row["material_simple_pole"])
                and any(
                    pole["node_id"] == row["node_id"]
                    and pole["term_id"] == row["term_id"]
                    and pole["pole_id"] == row["pole_id"]
                    and parse_bool(pole["inside_reduced_term_support"])
                    for pole in poles
                )
                for row in classifications
            ),
            "unresolved_pole_count": unresolved_count,
            "failed_outer_panel_indices": failed_panels,
            **metrics,
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
                "valid_for_D2_E0025_fixed_decay_integral": fixed_decay_accepted,
                **{
                    field: False
                    for field in CLAIM_FIELDS
                    if field != "valid_for_D2_E0025_fixed_decay_integral"
                },
                "reason": (
                    "This checkpoint evaluates one finite regulator at the D2 midpoint. "
                    "It neither takes epsilon to zero nor performs the decay-angle integral."
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
                "state": "COMPLETE_DIAGNOSTIC",
                "decision": decision,
                "completed_node_count": complete_count,
                "planned_node_count": len(plan),
            },
        )
        return result
    finally:
        restore_kernel(old)


def render_document(result: dict[str, Any], passed: bool) -> None:
    failed = result.get("failed_outer_panel_indices", [])
    lines = [
        "# 5325 - D2 midpoint E0025 pole-topology smoke",
        "",
        "## Purpose",
        "",
        "This is the first new numerical decay-angle node after the inherited",
        "D4-inner calculation.  It rebuilds the 44-cell, 11-panel contract at",
        f"`|d|={result['absolute_decay_cosine']:.16g}` and evaluates E0025 without",
        "assuming that the old panel-nine material-pole topology transfers.",
        "",
        "## Result",
        "",
        f"- completed nodes: `{result.get('completed_node_count', 0)}` / "
        f"`{result.get('planned_node_count', 0)}`;",
        f"- all inner nodes pass: `{result.get('all_inner_nodes_pass', False)}`;",
        f"- geometric poles: `{result.get('geometric_pole_count', 0)}`;",
        f"- material simple poles: `{result.get('material_simple_pole_count', 0)}`;",
        f"- failed outer panels: `{failed}`;",
        f"- fixed-decay value: `{result.get('selected_D2_E0025_fixed_decay_integral_real', '')}` "
        f"`{float(result.get('selected_D2_E0025_fixed_decay_integral_imaginary', 0.0)):+.12g} i`;",
        f"- coarse fixed-decay acceptance: "
        f"`{result.get('finite_regulator_fixed_decay_integral_accepted', False)}`;",
        f"- decision: **{result['decision']}**;",
        f"- validation: **{'PASS' if passed else 'FAIL'}**.",
        "",
        "## Claim boundary",
        "",
        "A pass is evidence for at most one E0025 fixed-decay value at D2_MID.",
        "The regulator-zero limit, GL2/GL4 decay-angle integral, endpoint cap,",
        "full phase space, UV coefficient, local GR, and full MTS remain separate.",
    ]
    DOCUMENT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def validate_outputs() -> dict[str, Any]:
    started = time.perf_counter()
    old = configure_kernel()
    try:
        result = read_json(RESULT)
        dry = read_json(DRY_RUN)
        contract = read_csv(REDUCED_CONTRACT)
        identity = read_csv(IDENTITY_AUDIT)
        plan = read_csv(NODE_PLAN)
        manifest = read_csv(NODE_MANIFEST)
        panels = read_csv(PANEL_CONVERGENCE)
        source_current = all(
            Path(row["path"]).exists()
            and digest(Path(row["path"])) == row["sha256"]
            for row in result["source_files"]
        )
        broad_claims = [
            field
            for field in CLAIM_FIELDS
            if field != "valid_for_D2_E0025_fixed_decay_integral"
        ]
        gates = [
            validation_gate(
                "D2_preflight_and_identity_pass",
                bool(dry["acceptance_passed"])
                and len(contract) == EXPECTED_CELL_COUNT
                and bool(identity)
                and all(
                    parse_bool(row["valid_for_MC04_MC12_identity_transfer"])
                    for row in identity
                ),
                f"cells={len(contract)} identity_rows={len(identity)}",
            ),
            validation_gate(
                "all_planned_E0025_nodes_complete_and_pass",
                len(plan) == len(manifest) == EXPECTED_NODE_COUNT
                and all(row["shard_state"] == "COMPLETE_PASS" for row in manifest)
                and bool(result["all_inner_nodes_pass"]),
                f"nodes={len(manifest)}",
            ),
            validation_gate(
                "all_eleven_panel_diagnostics_present",
                len(panels) == EXPECTED_PANEL_COUNT
                and {int(row["x_panel_index"]) for row in panels}
                == set(range(1, EXPECTED_PANEL_COUNT + 1)),
                f"panels={len(panels)}",
            ),
            validation_gate(
                "pole_classification_resolved",
                int(result["unresolved_pole_count"]) == 0,
                f"unresolved={result['unresolved_pole_count']}",
            ),
            validation_gate(
                "finite_integral_flag_matches_numerical_gates",
                bool(result["finite_regulator_fixed_decay_integral_accepted"])
                == (
                    float(result["outer_relative_change"])
                    <= M5312.OUTER_RELATIVE_CHANGE_LIMIT
                    and float(result["inner_error_budget_relative"])
                    <= M5312.INNER_ERROR_BUDGET_LIMIT
                    and bool(result["all_inner_nodes_pass"])
                )
                and bool(
                    result["claim_boundary"][
                        "valid_for_D2_E0025_fixed_decay_integral"
                    ]
                )
                == bool(result["finite_regulator_fixed_decay_integral_accepted"]),
                str(result["finite_regulator_fixed_decay_integral_accepted"]),
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
                all(not bool(result["claim_boundary"][field]) for field in broad_claims),
                "epsilon-zero and angular claims remain false",
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
                "VALIDATED_D2_MIDPOINT_E0025_POLE_TOPOLOGY_SMOKE"
                if passed
                else "D2_MIDPOINT_E0025_POLE_TOPOLOGY_SMOKE_VALIDATION_FAILED"
            ),
            "runtime_seconds": time.perf_counter() - started,
        }
    finally:
        restore_kernel(old)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode", choices=("dry-run", "run", "validate"), required=True
    )
    parser.add_argument(
        "--max-runtime-hours",
        type=float,
        default=DEFAULT_RUNTIME_LIMIT_SECONDS / 3600.0,
    )
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
