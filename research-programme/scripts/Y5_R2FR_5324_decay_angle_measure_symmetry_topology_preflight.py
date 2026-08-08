from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import time
from pathlib import Path
from typing import Any

import numpy as np


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SCRIPTS = POST / "scripts"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
RESIDUALS = POST / "source-intake" / "mts_residuals"
SOURCE = FUNCTIONAL_RG / "5324"

SCRIPT_5240 = SCRIPTS / "Y5_R2FR_5240_two_angular_nested_A00_causal_cubature_pilot.py"
RESULT_5240 = FUNCTIONAL_RG / "5240" / "two_angular_nested_A00_result.json"
RULES_5240 = FUNCTIONAL_RG / "5240" / "two_angular_outer_rule_audit.csv"
SCRIPT_5286 = SCRIPTS / "Y5_R2FR_5286_angular_node_material_pole_atlas_preflight.py"
NODES_5286 = FUNCTIONAL_RG / "5286" / "angular_order2_nodes.csv"
SCRIPT_5291 = SCRIPTS / "Y5_R2FR_5291_order4_complete_singularity_atlas.py"
NODES_5291 = FUNCTIONAL_RG / "5291" / "angular_order4_nodes.csv"
SCRIPT_5308 = SCRIPTS / "Y5_R2FR_5308_full_fixed_decay_pair_orbit_topology.py"
RESULT_5308 = FUNCTIONAL_RG / "5308" / "full_fixed_decay_pair_topology_result.json"
VALIDATION_5308 = FUNCTIONAL_RG / "5308" / "full_fixed_decay_pair_topology_validation.csv"
EVENTS_5308 = FUNCTIONAL_RG / "5308" / "full_fixed_decay_pair_topology_events.csv"
SCRIPT_5323 = SCRIPTS / "Y5_R2FR_5323_seven_point_regulator_zero_refit.py"
RESULT_5323 = FUNCTIONAL_RG / "5323" / "seven_point_regulator_zero_refit_result.json"
VALIDATION_5323 = FUNCTIONAL_RG / "5323" / "seven_point_regulator_zero_refit_validation.csv"

MEASURE = SOURCE / "decay_angle_paired_quadrature_measure_contract.csv"
NODE_SUMMARY = SOURCE / "decay_angle_topology_node_summary.csv"
EVENTS = SOURCE / "decay_angle_topology_events.csv"
PANELS = SOURCE / "decay_angle_topology_soft_panels.csv"
CHAMBERS = SOURCE / "decay_angle_energy_chambers.csv"
REDUCTION = SOURCE / "decay_angle_sign_orbit_reduction_audit.csv"
CONTRACT = SOURCE / "decay_angle_energy_soft_cubature_contract.csv"
REPRODUCTION = SOURCE / "inherited_D4_inner_topology_reproduction.csv"
RESULT = SOURCE / "decay_angle_measure_symmetry_topology_preflight_result.json"
VALIDATION = SOURCE / "decay_angle_measure_symmetry_topology_preflight_validation.csv"
RESIDUAL_VALIDATION = RESIDUALS / "P8_Y5_BRR545_5324_VALIDATION.csv"
DOCUMENT = POST / "5324-Y5-R2FR-decay-angle-measure-symmetry-topology-preflight.md"

CHECKPOINT = 5324
PARENT_CHECKPOINT = 5323
MARKER = "MTS_5324_DECAY_ANGLE_MEASURE_SYMMETRY_TOPOLOGY_PREFLIGHT"
REVISION = "decay-angle-measure-symmetry-topology-preflight-v1"
ANGULAR_MEASURE_FACTOR = 0.25
MOMENT_TOLERANCE = 2.0e-12
REPRODUCTION_COORDINATE_TOLERANCE = 2.0e-10
CLAIM_FIELDS = (
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


M5308 = load_module("mts_5308_for_5324", SCRIPT_5308)
M5283 = M5308.M5283


def read_csv(path: Path) -> list[dict[str, str]]:
    return M5308.read_csv(path)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    M5308.write_csv(path, rows)


def read_json(path: Path) -> dict[str, Any]:
    return M5308.read_json(path)


def atomic_json(path: Path, value: Any) -> None:
    M5308.atomic_json(path, value)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_bool(value: Any) -> bool:
    return M5308.parse_bool(value)


def validation_gate(gate: str, passed: bool, detail: str) -> dict[str, Any]:
    return {
        "gate": gate,
        "passed": passed,
        "detail": detail,
        **{field: False for field in CLAIM_FIELDS},
    }


def historical_absolute_nodes() -> tuple[float, float, float]:
    order2 = sorted(
        {abs(float(row["decay_cosine"])) for row in read_csv(NODES_5286)}
    )
    order4 = sorted(
        {abs(float(row["decay_cosine"])) for row in read_csv(NODES_5291)}
    )
    if len(order2) != 1 or len(order4) != 2:
        raise RuntimeError("historical angular-node inventories are malformed")
    return order2[0], order4[0], order4[1]


def quadrature_contract() -> tuple[list[dict[str, Any]], dict[str, float]]:
    limit = M5308.angular_limit()
    historical = historical_absolute_nodes()
    inherited_used = float(read_json(RESULT_5308)["absolute_decay_cosine"])
    rows: list[dict[str, Any]] = []
    node_map = {
        (2, 0): ("D2_MID", historical[0], historical[0]),
        (4, 0): ("D4_INNER", historical[1], inherited_used),
        (4, 1): ("D4_OUTER", historical[2], historical[2]),
    }
    maximum_moment_residuals: dict[str, float] = {}
    for order in (2, 4):
        nodes, weights = np.polynomial.legendre.leggauss(order)
        positive = sorted(
            (float(node), float(weight))
            for node, weight in zip(nodes, weights)
            if node > 0.0
        )
        local_rows: list[dict[str, Any]] = []
        for index, (node, weight) in enumerate(positive):
            node_id, historical_coordinate, used_coordinate = node_map[(order, index)]
            exact_coordinate = limit * node
            paired_weight = limit * weight
            local_rows.append(
                {
                    "quadrature_order": order,
                    "decay_node_id": node_id,
                    "absolute_decay_cosine_exact": exact_coordinate,
                    "absolute_decay_cosine_historical": historical_coordinate,
                    "absolute_decay_cosine_used": used_coordinate,
                    "coordinate_historical_difference": abs(
                        exact_coordinate - historical_coordinate
                    ),
                    "coordinate_used_difference": abs(exact_coordinate - used_coordinate),
                    "paired_signed_gauss_weight": paired_weight,
                    "physical_phase_space_weight": (
                        ANGULAR_MEASURE_FACTOR * paired_weight
                    ),
                    "angular_measure_factor": ANGULAR_MEASURE_FACTOR,
                    "sign_orbit_definition": (
                        "G(a,b)=sum_{sigma_s=+-1,sigma_d=+-1} "
                        "F(sigma_s*a,sigma_d*b)"
                    ),
                    "measure_identity": (
                        "(1/4)int_-L^L ds int_-L^L dd F="
                        "(1/4)int_0^L da int_0^L db G(a,b)"
                    ),
                    "endpoint_cap_fraction_remaining": 1.0 - limit,
                    **{field: False for field in CLAIM_FIELDS},
                }
            )
        maximum_residual = 0.0
        for power in range(2 * order):
            predicted = sum(
                float(row["paired_signed_gauss_weight"])
                * (
                    float(row["absolute_decay_cosine_exact"]) ** power
                    + (-float(row["absolute_decay_cosine_exact"])) ** power
                )
                for row in local_rows
            )
            exact = (
                0.0
                if power % 2
                else 2.0 * limit ** (power + 1) / (power + 1)
            )
            maximum_residual = max(maximum_residual, abs(predicted - exact))
        for row in local_rows:
            row["maximum_signed_monomial_moment_residual"] = maximum_residual
            row["quadrature_measure_contract_passes"] = (
                maximum_residual <= MOMENT_TOLERANCE
                and float(row["coordinate_historical_difference"])
                <= MOMENT_TOLERANCE
                and float(row["coordinate_used_difference"])
                <= MOMENT_TOLERANCE
            )
        maximum_moment_residuals[f"order_{order}"] = maximum_residual
        rows.extend(local_rows)
    return rows, maximum_moment_residuals


def qualify_rows(
    rows: list[dict[str, Any]],
    node_id: str,
    decay: float,
) -> list[dict[str, Any]]:
    return [
        {
            "decay_node_id": node_id,
            "absolute_decay_cosine": decay,
            **row,
        }
        for row in rows
    ]


def derive_topology_node(
    node_id: str,
    decay: float,
) -> tuple[
    dict[str, Any],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
]:
    M5308.M5302.EDGE_DECAY_ABSOLUTE = decay
    grid = [
        float(value)
        for value in np.linspace(0.0, M5308.angular_limit(), M5308.SCAN_COUNT)
    ]
    branches = M5308.branch_scan_rows(grid)
    events = M5308.topology_event_rows(grid)
    panels = M5308.x_panel_rows(events)
    chambers = M5308.chamber_rows(panels)
    context = M5308.M5303.synthetic_context()
    evaluate = M5308.M5305.component_evaluator(context)
    reduction, summaries = M5308.reduction_rows(chambers, evaluate)
    contract = M5308.contract_rows(chambers, summaries)
    checks = {
        "all_surface_branches_pass": all(
            parse_bool(row["valid_for_full_fixed_decay_surface_branch"])
            for row in branches
        ),
        "events_span_absolute_soft_domain": (
            abs(float(events[0]["absolute_soft_cosine"])) <= 1.0e-14
            and abs(
                float(events[-1]["absolute_soft_cosine"])
                - M5308.angular_limit()
            )
            <= 1.0e-14
        ),
        "all_soft_panels_topology_stable": all(
            parse_bool(row["valid_for_topology_stable_x_panel"])
            for row in panels
        ),
        "all_sign_orbit_reductions_pass": all(
            parse_bool(row["valid_for_pair_orbit_reduction"])
            for row in reduction
        ),
        "all_cubature_contract_rows_pass": all(
            parse_bool(row["valid_for_chamber_aligned_cubature_contract"])
            for row in contract
        ),
    }
    summary = {
        "decay_node_id": node_id,
        "absolute_decay_cosine": decay,
        "surface_branch_count": len(branches),
        "topology_event_count": len(events),
        "topology_stable_soft_panel_count": len(panels),
        "energy_chamber_count": len(chambers),
        "reduction_probe_count": len(reduction),
        "cubature_contract_count": len(contract),
        "maximum_surface_equation_residual": max(
            float(row["equation_residual"]) for row in branches
        ),
        "maximum_sign_orbit_reduction_relative_change": max(
            float(row["final_reduction_relative_change"])
            for row in reduction
        ),
        "full_active_orbit_fallback_count": sum(
            row["reduction_type"] == "FULL_ACTIVE_ORBIT_FALLBACK"
            for row in contract
        ),
        **checks,
        "topology_node_preflight_passes": all(checks.values()),
        **{field: False for field in CLAIM_FIELDS},
    }
    return (
        summary,
        qualify_rows(branches, node_id, decay),
        qualify_rows(events, node_id, decay),
        qualify_rows(panels, node_id, decay),
        qualify_rows(chambers, node_id, decay),
        qualify_rows(reduction, node_id, decay),
        qualify_rows(contract, node_id, decay),
    )


def inherited_reproduction_rows(
    generated: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    source = read_csv(EVENTS_5308)
    generated = sorted(generated, key=lambda row: int(row["event_index"]))
    source = sorted(source, key=lambda row: int(row["event_index"]))
    count_matches = len(generated) == len(source)
    rows: list[dict[str, Any]] = []
    for index in range(max(len(generated), len(source))):
        current = generated[index] if index < len(generated) else {}
        inherited = source[index] if index < len(source) else {}
        coordinate_difference = (
            abs(
                float(current["absolute_soft_cosine"])
                - float(inherited["absolute_soft_cosine"])
            )
            if current and inherited
            else math.inf
        )
        rows.append(
            {
                "event_index": index,
                "generated_event_types": current.get("event_types", "MISSING"),
                "inherited_event_types": inherited.get("event_types", "MISSING"),
                "generated_owners": current.get("owners", "MISSING"),
                "inherited_owners": inherited.get("owners", "MISSING"),
                "coordinate_difference": coordinate_difference,
                "event_count_matches": count_matches,
                "event_identity_matches": (
                    bool(current)
                    and bool(inherited)
                    and current["event_types"] == inherited["event_types"]
                    and current["owners"] == inherited["owners"]
                ),
                "inherited_topology_reproduced": (
                    count_matches
                    and coordinate_difference <= REPRODUCTION_COORDINATE_TOLERANCE
                    and bool(current)
                    and bool(inherited)
                    and current["event_types"] == inherited["event_types"]
                    and current["owners"] == inherited["owners"]
                ),
                **{field: False for field in CLAIM_FIELDS},
            }
        )
    return rows


def source_rows() -> list[dict[str, str]]:
    paths = (
        Path(__file__).resolve(),
        SCRIPT_5240,
        RESULT_5240,
        RULES_5240,
        SCRIPT_5286,
        NODES_5286,
        SCRIPT_5291,
        NODES_5291,
        SCRIPT_5308,
        RESULT_5308,
        VALIDATION_5308,
        EVENTS_5308,
        SCRIPT_5323,
        RESULT_5323,
        VALIDATION_5323,
        MEASURE,
    )
    return [{"path": str(path), "sha256": digest(path)} for path in paths]


def execute() -> dict[str, Any]:
    started = time.perf_counter()
    SOURCE.mkdir(parents=True, exist_ok=True)
    parent = read_json(RESULT_5323)
    parent_validation = read_csv(VALIDATION_5323)
    measure, moment_residuals = quadrature_contract()
    write_csv(MEASURE, measure)
    unique_nodes: dict[str, float] = {}
    for row in measure:
        unique_nodes[row["decay_node_id"]] = float(
            row["absolute_decay_cosine_used"]
        )
    old_decay = M5308.M5302.EDGE_DECAY_ABSOLUTE
    M5308.mp.mp.dps = M5308.M5280.MP_DECIMAL_DIGITS
    M5308.M5301.configure_reused_pipeline()
    summaries: list[dict[str, Any]] = []
    branch_rows: list[dict[str, Any]] = []
    event_rows: list[dict[str, Any]] = []
    panel_rows: list[dict[str, Any]] = []
    chamber_rows: list[dict[str, Any]] = []
    reduction_rows: list[dict[str, Any]] = []
    contract_rows: list[dict[str, Any]] = []
    try:
        for node_id, decay in unique_nodes.items():
            (
                summary,
                local_branches,
                local_events,
                local_panels,
                local_chambers,
                local_reduction,
                local_contract,
            ) = derive_topology_node(node_id, decay)
            summaries.append(summary)
            branch_rows.extend(local_branches)
            event_rows.extend(local_events)
            panel_rows.extend(local_panels)
            chamber_rows.extend(local_chambers)
            reduction_rows.extend(local_reduction)
            contract_rows.extend(local_contract)
    finally:
        M5308.M5302.EDGE_DECAY_ABSOLUTE = old_decay
    reproduction = inherited_reproduction_rows(
        [row for row in event_rows if row["decay_node_id"] == "D4_INNER"]
    )
    write_csv(NODE_SUMMARY, summaries)
    write_csv(EVENTS, event_rows)
    write_csv(PANELS, panel_rows)
    write_csv(CHAMBERS, chamber_rows)
    write_csv(REDUCTION, reduction_rows)
    write_csv(CONTRACT, contract_rows)
    write_csv(REPRODUCTION, reproduction)
    formal_end = M5283.formal_inventory_digest()
    checks = {
        "parent_fixed_decay_zero_limit_accepted": (
            bool(parent["acceptance_passed"])
            and parent["decision"]
            == "SEVEN_POINT_FIXED_DECAY_ZERO_LIMIT_ACCEPTED__BUILD_DECAY_ANGLE_LADDER"
            and all(parse_bool(row["passed"]) for row in parent_validation)
        ),
        "paired_measure_identity_and_moments_pass": (
            len(measure) == 3
            and all(parse_bool(row["quadrature_measure_contract_passes"]) for row in measure)
        ),
        "all_three_absolute_decay_nodes_derived": (
            {row["decay_node_id"] for row in summaries}
            == {"D2_MID", "D4_INNER", "D4_OUTER"}
        ),
        "all_topology_node_preflights_pass": all(
            bool(row["topology_node_preflight_passes"]) for row in summaries
        ),
        "inherited_D4_inner_topology_reproduced": all(
            bool(row["inherited_topology_reproduced"]) for row in reproduction
        ),
        "formalization_workbench_unchanged": (
            formal_end == parent["formalization_workbench_end_digest"]
        ),
    }
    accepted = all(checks.values())
    result = {
        "checkpoint": CHECKPOINT,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "mode": "decay-angle-measure-symmetry-topology-preflight",
        "acceptance_passed": accepted,
        "decision": (
            "DECAY_ANGLE_MEASURE_AND_GL2_GL4_TOPOLOGIES_DERIVED__RUN_NEW_FIXED_DECAY_LADDERS"
            if accepted
            else "DECAY_ANGLE_TOPOLOGY_PREFLIGHT_REQUIRES_REPAIR"
        ),
        "checks": checks,
        "angular_limit": M5308.angular_limit(),
        "angular_endpoint_cap_fraction_remaining": 1.0 - M5308.angular_limit(),
        "angular_measure_factor": ANGULAR_MEASURE_FACTOR,
        "quadrature_row_count": len(measure),
        "unique_absolute_decay_node_count": len(summaries),
        "new_absolute_decay_node_ids": ["D2_MID", "D4_OUTER"],
        "reused_absolute_decay_node_id": "D4_INNER",
        "maximum_order2_moment_residual": moment_residuals["order_2"],
        "maximum_order4_moment_residual": moment_residuals["order_4"],
        "maximum_surface_equation_residual": max(
            float(row["maximum_surface_equation_residual"]) for row in summaries
        ),
        "maximum_sign_orbit_reduction_relative_change": max(
            float(row["maximum_sign_orbit_reduction_relative_change"])
            for row in summaries
        ),
        "formalization_workbench_reference_digest": parent[
            "formalization_workbench_end_digest"
        ],
        "formalization_workbench_end_digest": formal_end,
        "formalization_workbench_modified_file_count": (
            0 if formal_end == parent["formalization_workbench_end_digest"] else -1
        ),
        "claim_boundary": {
            **{field: False for field in CLAIM_FIELDS},
            "reason": (
                "This derives the paired decay measure and topology-safe fixed-angle "
                "contracts. The two new finite-regulator ladders, angular-order "
                "comparison, and 0.5-percent endpoint cap remain uncomputed."
            ),
        },
        "resource_contract": {
            "maximum_task_python_processes": 1,
            "worker_math_threads": 1,
            "windows_priority": "BelowNormal",
            "maximum_silent_work_hours": 4,
        },
        "source_files": source_rows(),
        "runtime_seconds": time.perf_counter() - started,
    }
    atomic_json(RESULT, result)
    return result


def render_document(result: dict[str, Any], passed: bool) -> None:
    lines = [
        "# 5324 - Decay-angle measure, symmetry, and topology preflight",
        "",
        "## Derived measure",
        "",
        "With `a=|cos(theta_soft)|`, `b=|cos(theta_decay)|`, and",
        "",
        "`G(a,b)=sum_{sigma_s,sigma_d=+-1} F(sigma_s a,sigma_d b)`,",
        "",
        "the parent Sobol map gives",
        "",
        "`(1/4) integral_-L^L ds integral_-L^L dd F = "
        "(1/4) integral_0^L da integral_0^L db G`,",
        "",
        f"with `L={result['angular_limit']}`. The fixed-decay runner already",
        "integrates `a` and sums all four signs, so only the paired decay rule",
        "and the inherited factor `1/4` remain.",
        "",
        "## Result",
        "",
        "- order-2 requires `D2_MID`;",
        "- order-4 requires `D4_INNER` and `D4_OUTER`;",
        "- `D4_INNER` is the validated 5323 slice and its topology is reproduced;",
        "- both genuinely new decay-node topology contracts pass;",
        f"- maximum sign-orbit reduction residual: "
        f"`{result['maximum_sign_orbit_reduction_relative_change']:.12g}`;",
        f"- decision: **{result['decision']}**;",
        f"- validation: **{'PASS' if passed else 'FAIL'}**.",
        "",
        "## Claim boundary",
        "",
        "The two new fixed-decay regulator ladders and the angular order-2/order-4",
        "comparison have not yet been run. The cutoff endpoint cap also remains an",
        "explicit separate bound. No full angular, UV, local-GR, or MTS claim follows.",
    ]
    DOCUMENT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def validate_outputs() -> dict[str, Any]:
    started = time.perf_counter()
    result = read_json(RESULT)
    measure = read_csv(MEASURE)
    summaries = read_csv(NODE_SUMMARY)
    reproduction = read_csv(REPRODUCTION)
    contracts = read_csv(CONTRACT)
    source_current = all(
        Path(row["path"]).exists()
        and digest(Path(row["path"])) == row["sha256"]
        for row in result["source_files"]
    )
    gates = [
        validation_gate(
            "paired_decay_measure_contract_passes",
            len(measure) == 3
            and all(parse_bool(row["quadrature_measure_contract_passes"]) for row in measure),
            f"rows={len(measure)}",
        ),
        validation_gate(
            "GL2_GL4_absolute_node_set_complete",
            {row["decay_node_id"] for row in summaries}
            == {"D2_MID", "D4_INNER", "D4_OUTER"},
            f"nodes={len(summaries)}",
        ),
        validation_gate(
            "all_decay_node_topology_contracts_pass",
            all(parse_bool(row["topology_node_preflight_passes"]) for row in summaries)
            and all(
                parse_bool(row["valid_for_chamber_aligned_cubature_contract"])
                for row in contracts
            ),
            f"contract_rows={len(contracts)}",
        ),
        validation_gate(
            "inherited_D4_inner_topology_reproduces",
            bool(reproduction)
            and all(parse_bool(row["inherited_topology_reproduced"]) for row in reproduction),
            f"events={len(reproduction)}",
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
            "angular_and_broader_claims_locked_false",
            all(not bool(result["claim_boundary"][field]) for field in CLAIM_FIELDS),
            "new fixed-decay ladders and endpoint cap remain",
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
            "VALIDATED_DECAY_ANGLE_MEASURE_SYMMETRY_TOPOLOGY_PREFLIGHT"
            if passed
            else "DECAY_ANGLE_MEASURE_SYMMETRY_TOPOLOGY_VALIDATION_FAILED"
        ),
        "runtime_seconds": time.perf_counter() - started,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("run", "validate"), required=True)
    return parser.parse_args()


def main() -> int:
    M5308.set_below_normal_priority()
    arguments = parse_args()
    result = execute() if arguments.mode == "run" else validate_outputs()
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
