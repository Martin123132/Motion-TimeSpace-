from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import time
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SCRIPTS = POST / "scripts"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
RESIDUALS = POST / "source-intake" / "mts_residuals"
SOURCE = FUNCTIONAL_RG / "5322"
SHARDS = SOURCE / "shards"
BASELINE_SHARDS = SOURCE / "baseline-shards"

SCRIPT_5320 = SCRIPTS / "Y5_R2FR_5320_E00125_finite_regulator_extension.py"
RESULT_5320 = FUNCTIONAL_RG / "5320" / "E00125_finite_regulator_extension_result.json"
VALIDATION_5320 = FUNCTIONAL_RG / "5320" / "E00125_finite_regulator_extension_validation.csv"
SCRIPT_5321 = SCRIPTS / "Y5_R2FR_5321_six_point_regulator_zero_refit.py"
RESULT_5321 = FUNCTIONAL_RG / "5321" / "six_point_regulator_zero_refit_result.json"
VALIDATION_5321 = FUNCTIONAL_RG / "5321" / "six_point_regulator_zero_refit_validation.csv"

DRY_RUN = SOURCE / "E000625_finite_regulator_extension_dry_run.json"
EVENT_AUDIT = SOURCE / "E000625_panel_nine_events.csv"
SEGMENT_PLAN = SOURCE / "E000625_panel_nine_segment_plan.csv"
INITIAL_PLAN = SOURCE / "E000625_full_outer_initial_plan.csv"
NODE_MANIFEST = SOURCE / "E000625_outer_node_manifest.csv"
OFF_AXIS_AUDIT = SOURCE / "E000625_off_axis_raw_audit.csv"
ADAPTIVE_PANELS = SOURCE / "E000625_adaptive_outer_panel_tree.csv"
FINITE_VALUE = SOURCE / "E000625_finite_regulator_fixed_decay_convergence.csv"
TARGETED_NODE_REPAIR = SOURCE / "E000625_targeted_energy_partition_repair.csv"
RESULT = SOURCE / "E000625_finite_regulator_extension_result.json"
VALIDATION = SOURCE / "E000625_finite_regulator_extension_validation.csv"
RESIDUAL_VALIDATION = RESIDUALS / "P8_Y5_BRR545_5322_VALIDATION.csv"
STATUS = SOURCE / "status.json"
DOCUMENT = POST / "5322-Y5-R2FR-E000625-finite-regulator-extension.md"

CHECKPOINT = 5322
PARENT_CHECKPOINT = 5321
MARKER = "MTS_5322_E000625_FINITE_REGULATOR_EXTENSION"
REVISION = "E000625-finite-regulator-extension-v1"
NODE_REVISION_PREFIX = "E000625-full-outer-node-v1"
EPSILON_ID = "E000625"
EPSILON = 0.000625
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


M5320 = load_module("mts_5320_for_5322", SCRIPT_5320)
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


def validation_gate(gate: str, passed: bool, detail: str) -> dict[str, Any]:
    return M5320.validation_gate(gate, passed, detail)


def configure_extension() -> None:
    M5320.SOURCE = SOURCE
    M5320.SHARDS = SHARDS
    M5320.BASELINE_SHARDS = BASELINE_SHARDS
    M5320.DRY_RUN = DRY_RUN
    M5320.EVENT_AUDIT = EVENT_AUDIT
    M5320.SEGMENT_PLAN = SEGMENT_PLAN
    M5320.INITIAL_PLAN = INITIAL_PLAN
    M5320.NODE_MANIFEST = NODE_MANIFEST
    M5320.OFF_AXIS_AUDIT = OFF_AXIS_AUDIT
    M5320.ADAPTIVE_PANELS = ADAPTIVE_PANELS
    M5320.FINITE_VALUE = FINITE_VALUE
    M5320.RESULT = RESULT
    M5320.VALIDATION = VALIDATION
    M5320.RESIDUAL_VALIDATION = RESIDUAL_VALIDATION
    M5320.STATUS = STATUS
    M5320.DOCUMENT = DOCUMENT
    M5320.CHECKPOINT = CHECKPOINT
    M5320.PARENT_CHECKPOINT = PARENT_CHECKPOINT
    M5320.MARKER = MARKER
    M5320.REVISION = REVISION
    M5320.NODE_REVISION_PREFIX = NODE_REVISION_PREFIX
    M5320.EPSILON_ID = EPSILON_ID
    M5320.EPSILON = EPSILON
    M5320.TARGET_REGULATORS = TARGET_REGULATORS
    M5320.RESULT_5319 = RESULT_5321
    M5320.VALIDATION_5319 = VALIDATION_5321
    M5320.dry_run = dry_run
    M5320.source_rows = source_rows
    M5320.configure_parent_module()


def source_rows() -> list[dict[str, str]]:
    paths = (
        Path(__file__).resolve(),
        SCRIPT_5320,
        RESULT_5320,
        VALIDATION_5320,
        SCRIPT_5321,
        RESULT_5321,
        VALIDATION_5321,
        M5320.M5318.CONTRACT_5312,
        M5320.M5318.SUPPORT_EVENTS_5313,
        M5320.M5318.EVENTS_5314,
        DRY_RUN,
        EVENT_AUDIT,
        SEGMENT_PLAN,
        INITIAL_PLAN,
        TARGETED_NODE_REPAIR,
    )
    return [{"path": str(path), "sha256": digest(path)} for path in paths]


def dry_run() -> dict[str, Any]:
    started = time.perf_counter()
    configure_extension()
    SOURCE.mkdir(parents=True, exist_ok=True)
    parent = read_json(RESULT_5321)
    parent_validation = read_csv(VALIDATION_5321)
    events = M5320.M5318.derive_regulator_events()
    segments = M5320.M5318.build_segment_plan(events)
    initial = M5320.build_initial_plan(segments)
    acceptance = (
        parent["decision"]
        == "SIX_POINT_LIMIT_STABLE__ADD_E000625_TO_CLOSE_REMAINDER_ENVELOPE"
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
            "DRY_RUN_ACCEPTED__RUN_E000625_FULL_OUTER_INTEGRAL"
            if acceptance
            else "E000625_FINITE_REGULATOR_EXTENSION_DRY_RUN_BLOCKED"
        ),
        "event_count": len(events),
        "initial_panel_count": len(initial),
        "plan_sha256": M5320.plan_sha256(initial),
        "runtime_seconds": time.perf_counter() - started,
    }
    atomic_json(DRY_RUN, result)
    return result


def load_validated_dry_run() -> dict[str, Any]:
    required = (DRY_RUN, EVENT_AUDIT, SEGMENT_PLAN, INITIAL_PLAN)
    if not all(path.exists() for path in required):
        return dry_run()
    cached = read_json(DRY_RUN)
    events = read_csv(EVENT_AUDIT)
    segments = read_csv(SEGMENT_PLAN)
    initial = read_csv(INITIAL_PLAN)
    parent = read_json(RESULT_5321)
    parent_validation = read_csv(VALIDATION_5321)
    cache_passes = (
        bool(cached.get("acceptance_passed"))
        and cached.get("decision")
        == "DRY_RUN_ACCEPTED__RUN_E000625_FULL_OUTER_INTEGRAL"
        and int(cached.get("event_count", -1)) == len(events) == 3
        and int(cached.get("initial_panel_count", -1)) == len(initial) == 13
        and len(segments) == 5
        and cached.get("plan_sha256") == M5320.plan_sha256(initial)
        and all(parse_bool(row["event_contract_passes"]) for row in events)
        and parent["decision"]
        == "SIX_POINT_LIMIT_STABLE__ADD_E000625_TO_CLOSE_REMAINDER_ENVELOPE"
        and parent["required_next_regulator_id"] == EPSILON_ID
        and float(parent["required_next_regulator_epsilon"]) == EPSILON
        and all(parse_bool(row["passed"]) for row in parent_validation)
        and M5283.formal_inventory_digest()
        == parent["formalization_workbench_end_digest"]
    )
    return cached if cache_passes else dry_run()


def repair_failed_event_node() -> dict[str, Any]:
    started = time.perf_counter()
    configure_extension()
    load_validated_dry_run()
    manifest = read_csv(NODE_MANIFEST)
    failed = [
        dict(row)
        for row in manifest
        if row["shard_state"] == "COMPLETE_FAIL"
        and int(row["x_panel_index"]) == 9
    ]
    if len(failed) != 1:
        raise RuntimeError(f"expected one failed panel-nine node, found {len(failed)}")
    node = failed[0]
    paths = M5320.generic_shard_paths(EPSILON_ID, node["node_id"])
    before = read_json(paths["result"])
    initial = read_csv(INITIAL_PLAN)
    events = read_csv(EVENT_AUDIT)
    contract = read_csv(M5320.M5318.CONTRACT_5312)
    expected = M5320.plan_sha256(initial)
    branch_death = float(
        next(row for row in events if row["event_type"] == "SHARED_BRANCH_DEATH")[
            "event_coordinate"
        ]
    )
    base_context = M5320.extended_base_context()
    multiplier = M5320.M5318.M5314.M5309.physical_multiplier()
    module = M5320.M5318.M5314
    rows = [
        {
            "node_id": node["node_id"],
            "energy_panel_subdivisions": module.ENERGY_PANEL_SUBDIVISIONS,
            "inner_Q8_Q12_relative_change": before["inner_Q8_Q12_relative_change"],
            "inner_energy_error_budget_relative": before[
                "inner_energy_error_budget_relative"
            ],
            "effective_acceptance_passed": False,
            "stage": "PRE_REPAIR_BASELINE",
            **{field: False for field in CLAIM_FIELDS},
        }
    ]
    old_context = M5320.M5318.kernel_context(EPSILON_ID, EPSILON)
    old_subdivisions = module.ENERGY_PANEL_SUBDIVISIONS
    final_result = before
    final_audit: dict[str, Any] = {}
    try:
        for subdivisions in (64, 96, 128):
            module.ENERGY_PANEL_SUBDIVISIONS = subdivisions
            final_result = M5320.M5318.run_node(
                EPSILON_ID,
                node,
                contract,
                expected,
                branch_death,
                base_context,
                multiplier,
            )
            final_audit = M5320.M5318.effective_acceptance(
                EPSILON_ID, node, final_result
            )
            rows.append(
                {
                    "node_id": node["node_id"],
                    "energy_panel_subdivisions": subdivisions,
                    "inner_Q8_Q12_relative_change": final_result[
                        "inner_Q8_Q12_relative_change"
                    ],
                    "inner_energy_error_budget_relative": final_result[
                        "inner_energy_error_budget_relative"
                    ],
                    "effective_acceptance_passed": final_audit[
                        "effective_acceptance_passed"
                    ],
                    "stage": "REFINED_ENERGY_PARTITION",
                    **{field: False for field in CLAIM_FIELDS},
                }
            )
            if bool(final_audit["effective_acceptance_passed"]):
                break
    finally:
        module.ENERGY_PANEL_SUBDIVISIONS = old_subdivisions
        M5320.M5318.restore_kernel_context(old_context)
    accepted = bool(final_audit.get("effective_acceptance_passed"))
    final_result["targeted_energy_partition_repair_applied"] = True
    final_result["targeted_energy_panel_subdivisions"] = rows[-1][
        "energy_panel_subdivisions"
    ]
    final_result["targeted_energy_partition_repair_passes"] = accepted
    final_result["targeted_energy_partition_repair_reason"] = (
        "The endpoint-safe Laurent collar is narrower than the pole's imaginary "
        "separation, so subtraction is not identified. The unchanged raw-contour "
        "Q8/Q12 gate is retested on successively finer energy partitions."
    )
    atomic_json(paths["result"], final_result)
    write_csv(
        TARGETED_NODE_REPAIR,
        rows,
        ["node_id", "stage", "energy_panel_subdivisions"],
    )
    return {
        "checkpoint": CHECKPOINT,
        "mode": "targeted-event-node-energy-partition-repair",
        "acceptance_passed": accepted,
        "decision": (
            "E000625_TARGETED_EVENT_NODE_REPAIR_ACCEPTED"
            if accepted
            else "E000625_TARGETED_EVENT_NODE_REPAIR_FAILED"
        ),
        "node_id": node["node_id"],
        "tested_energy_panel_subdivisions": [
            int(row["energy_panel_subdivisions"]) for row in rows
        ],
        "runtime_seconds": time.perf_counter() - started,
    }


def execute(runtime_limit_seconds: float) -> dict[str, Any]:
    configure_extension()
    cached_dry = load_validated_dry_run()
    M5320.dry_run = lambda: cached_dry
    try:
        result = M5320.execute(runtime_limit_seconds)
    finally:
        M5320.dry_run = dry_run
    if result["acceptance_passed"]:
        decision = "E000625_FINITE_REGULATOR_CONVERGED__REFIT_ZERO_LIMIT"
    elif read_json(STATUS).get("state") == "PAUSED_RESUMABLE":
        decision = "E000625_FULL_OUTER_INTEGRAL_PAUSED__RESUME_SAVED_SHARDS"
    else:
        decision = "E000625_FINITE_REGULATOR_LOCALIZES_REMAINING_FAILURES"
    result["mode"] = "E000625-full-outer-finite-regulator-extension"
    result["decision"] = decision
    result["claim_boundary"]["reason"] = (
        "This is one additional finite regulator at one fixed decay angle. "
        "The regulator-zero refit and every broader claim remain separate."
    )
    atomic_json(RESULT, result)
    status = read_json(STATUS)
    status["decision"] = decision
    atomic_json(STATUS, status)
    return result


def render_document(result: dict[str, Any], validation_passed: bool) -> None:
    lines = [
        "# 5322 - E000625 finite-regulator extension",
        "",
        "## Method",
        "",
        "The validated six-point remainder envelope remains 1.0297%, just outside",
        "the inherited one-percent gate.  E000625 is therefore computed directly.",
        "Panels 1-8 use the all-term geometric-pole subtraction kernel; panel 9",
        "derives regulator-owned support events and uses squared-event coordinates.",
        "Arbitrary-precision root refinement remains at the authored 80 digits.",
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
        "A passing result adds one finite-regulator fixed-decay point only.  The",
        "seven-point regulator-zero refit and all broader claims remain separate.",
    ]
    DOCUMENT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def validate_outputs() -> dict[str, Any]:
    started = time.perf_counter()
    configure_extension()
    result = read_json(RESULT)
    dry = read_json(DRY_RUN)
    manifest = read_csv(NODE_MANIFEST)
    panels = read_csv(ADAPTIVE_PANELS)
    finite = read_csv(FINITE_VALUE)
    repair = read_csv(TARGETED_NODE_REPAIR)
    leaves = [row for row in panels if parse_bool(row["adaptive_leaf"])]
    source_current = all(
        Path(row["path"]).exists()
        and digest(Path(row["path"])) == row["sha256"]
        for row in result["source_files"]
    )
    gates = [
        validation_gate(
            "E000625_geometry_and_full_plan_pass",
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
            "E000625_full_conservative_budget_passes",
            len(finite) == 1
            and finite[0]["epsilon_id"] == EPSILON_ID
            and parse_bool(finite[0]["finite_regulator_fixed_decay_integral_accepted"])
            and float(finite[0]["fixed_decay_error_relative_conservative"])
            <= GLOBAL_OUTER_ERROR_BUDGET_LIMIT
            and bool(result["acceptance_passed"]),
            str(result["fixed_decay_error_relative_conservative"]),
        ),
        validation_gate(
            "targeted_event_node_repair_strengthens_resolution_without_relaxing_gate",
            bool(repair)
            and repair[0]["stage"] == "PRE_REPAIR_BASELINE"
            and any(
                parse_bool(row["effective_acceptance_passed"])
                for row in repair[1:]
            )
            and all(
                int(row["energy_panel_subdivisions"]) >= 64
                for row in repair[1:]
            ),
            f"rows={len(repair)}",
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
            "VALIDATED_E000625_FINITE_REGULATOR_EXTENSION"
            if passed
            else "E000625_FINITE_REGULATOR_EXTENSION_VALIDATION_FAILED"
        ),
        "runtime_seconds": time.perf_counter() - started,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=("dry-run", "repair-node", "run", "validate"),
        required=True,
    )
    parser.add_argument("--max-runtime-hours", type=float, default=1.5)
    return parser.parse_args()


def main() -> int:
    configure_extension()
    M5320.M5318.M5312.set_below_normal_priority()
    arguments = parse_args()
    if arguments.mode == "dry-run":
        result = dry_run()
    elif arguments.mode == "repair-node":
        result = repair_failed_event_node()
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
