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
SOURCE = FUNCTIONAL_RG / "5316"
SHARDS = SOURCE / "shards"

SCRIPT_5312 = SCRIPTS / "Y5_R2FR_5312_resumable_pole_subtracted_outer_soft_integral.py"
SCRIPT_5315 = SCRIPTS / "Y5_R2FR_5315_squared_event_coordinate_collar_repair.py"
RESULT_5315 = FUNCTIONAL_RG / "5315" / "squared_event_coordinate_collar_repair_result.json"
VALIDATION_5315 = FUNCTIONAL_RG / "5315" / "squared_event_coordinate_collar_repair_validation.csv"
CONTRACT_5312 = FUNCTIONAL_RG / "5312" / "reduced_fixed_decay_cubature_contract.csv"
NODE_PLAN_5312 = FUNCTIONAL_RG / "5312" / "E0025_outer_soft_node_plan.csv"

DRY_RUN = SOURCE / "four_regulator_coarse_scan_dry_run.json"
PLAN = SOURCE / "four_regulator_coarse_node_plan.csv"
MANIFEST = SOURCE / "four_regulator_coarse_node_manifest.csv"
OUTER_TOTALS = SOURCE / "four_regulator_coarse_outer_totals.csv"
PANEL_CONVERGENCE = SOURCE / "four_regulator_coarse_panel_convergence.csv"
REGULATOR_SUMMARY = SOURCE / "five_regulator_fixed_decay_status.csv"
RESULT = SOURCE / "four_regulator_coarse_scan_result.json"
VALIDATION = SOURCE / "four_regulator_coarse_scan_validation.csv"
RESIDUAL_VALIDATION = RESIDUALS / "P8_Y5_BRR545_5316_VALIDATION.csv"
STATUS = SOURCE / "status.json"
DOCUMENT = POST / "5316-Y5-R2FR-four-regulator-pole-subtracted-coarse-scan.md"

CHECKPOINT = 5316
PARENT_CHECKPOINT = 5315
MARKER = "MTS_5316_FOUR_REGULATOR_POLE_SUBTRACTED_COARSE_SCAN"
REVISION = "four-regulator-pole-subtracted-coarse-scan-v2"
NODE_REVISION_PREFIX = "four-regulator-coarse-node-v2"
TARGET_REGULATORS = (
    ("E005", 0.005),
    ("E010", 0.01),
    ("E020", 0.02),
    ("E040", 0.04),
)
OUTER_CHANGE_LIMIT = 5.0e-3
INNER_ERROR_BUDGET_LIMIT = 1.0e-2
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


M5315 = load_module("mts_5315_for_5316", SCRIPT_5315)
M5312 = M5315.M5312
M5283 = M5315.M5283


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


def validation_gate(gate: str, passed: bool, detail: str) -> dict[str, Any]:
    return M5312.validation_gate(gate, passed, detail)


def base_plan() -> list[dict[str, str]]:
    return read_csv(NODE_PLAN_5312)


def expanded_plan() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for epsilon_id, epsilon in TARGET_REGULATORS:
        for node in base_plan():
            rows.append(
                {
                    "epsilon_id": epsilon_id,
                    "epsilon": epsilon,
                    **node,
                    "node_result_path": str(
                        shard_paths(epsilon_id, node["node_id"])["result"]
                    ),
                    **{field: False for field in CLAIM_FIELDS},
                }
            )
    return rows


def plan_sha256(epsilon_id: str, epsilon: float) -> str:
    payload = {
        "revision": REVISION,
        "node_revision": f"{NODE_REVISION_PREFIX}-{epsilon_id}",
        "epsilon_id": epsilon_id,
        "epsilon": epsilon,
        "contract_sha256": digest(CONTRACT_5312),
        "base_node_plan_sha256": digest(NODE_PLAN_5312),
        "kernel_revision": M5312.REVISION,
    }
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode("utf-8")).hexdigest()


def shard_paths(epsilon_id: str, node_id: str) -> dict[str, Path]:
    root = SHARDS / epsilon_id / node_id
    return {
        "root": root,
        "poles": root / "geometric_poles.csv",
        "fits": root / "pole_residue_fits.csv",
        "classifications": root / "pole_classification.csv",
        "integrals": root / "cell_integrals.csv",
        "result": root / "result.json",
    }


def shard_complete(
    epsilon_id: str,
    node: dict[str, Any],
    expected_plan_sha256: str,
) -> bool:
    paths = shard_paths(epsilon_id, str(node["node_id"]))
    if not all(path.exists() for key, path in paths.items() if key != "root"):
        return False
    try:
        result = read_json(paths["result"])
        for key in ("poles", "fits", "classifications", "integrals"):
            read_csv(paths[key])
    except Exception:
        return False
    return (
        result.get("node_revision") == f"{NODE_REVISION_PREFIX}-{epsilon_id}"
        and result.get("node_plan_sha256") == expected_plan_sha256
        and result.get("node_id") == node["node_id"]
        and result.get("epsilon_id") == epsilon_id
        and bool(result.get("node_complete"))
    )


def set_kernel_globals(epsilon_id: str, epsilon: float) -> dict[str, Any]:
    old = {
        "EPSILON_ID": M5312.EPSILON_ID,
        "EPSILON": M5312.EPSILON,
        "SHARDS": M5312.SHARDS,
        "NODE_REVISION": M5312.NODE_REVISION,
        "CHECKPOINT": M5312.CHECKPOINT,
        "M5311_EPSILON_ID": M5312.M5311.EPSILON_ID,
        "M5311_EPSILON": M5312.M5311.EPSILON,
    }
    M5312.EPSILON_ID = epsilon_id
    M5312.EPSILON = epsilon
    M5312.SHARDS = SHARDS / epsilon_id
    M5312.NODE_REVISION = f"{NODE_REVISION_PREFIX}-{epsilon_id}"
    M5312.CHECKPOINT = CHECKPOINT
    M5312.M5311.EPSILON_ID = epsilon_id
    M5312.M5311.EPSILON = epsilon
    return old


def restore_kernel_globals(old: dict[str, Any]) -> None:
    M5312.M5311.EPSILON_ID = old.pop("M5311_EPSILON_ID")
    M5312.M5311.EPSILON = old.pop("M5311_EPSILON")
    for key, value in old.items():
        setattr(M5312, key, value)


def run_kernel_node(
    epsilon_id: str,
    epsilon: float,
    node: dict[str, Any],
    contract: list[dict[str, Any]],
    expected_plan_sha256: str,
    base_context: dict[str, Any],
    multiplier: float,
) -> dict[str, Any]:
    old = set_kernel_globals(epsilon_id, epsilon)
    try:
        result = M5312.run_node(
            node,
            contract,
            expected_plan_sha256,
            base_context,
            multiplier,
        )
        result.update(
            {
                "epsilon_id": epsilon_id,
                "epsilon": epsilon,
                "parent_kernel_checkpoint": 5312,
            }
        )
        atomic_json(shard_paths(epsilon_id, node["node_id"])["result"], result)
        return result
    finally:
        restore_kernel_globals(old)


def dry_run() -> dict[str, Any]:
    started = time.perf_counter()
    required = [
        SCRIPT_5312,
        SCRIPT_5315,
        RESULT_5315,
        VALIDATION_5315,
        CONTRACT_5312,
        NODE_PLAN_5312,
    ]
    missing = [str(path) for path in required if not path.exists()]
    validation_rows = read_csv(VALIDATION_5315) if not missing else []
    parent_passes = (
        not missing
        and bool(read_json(RESULT_5315)["acceptance_passed"])
        and bool(validation_rows)
        and all(parse_bool(row["passed"]) for row in validation_rows)
    )
    plan = expanded_plan() if parent_passes else []
    if plan:
        write_csv(PLAN, plan, ["epsilon_id", "node_id"])
    accepted = (
        parent_passes
        and len(read_csv(CONTRACT_5312)) == 32
        and len(base_plan()) == 54
        and len(plan) == len(TARGET_REGULATORS) * len(base_plan())
        and dict(M5312.M5303.REGULATORS)["E0025"] == 0.0025
    )
    result = {
        "checkpoint": CHECKPOINT,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "mode": "dry-run",
        "acceptance_passed": accepted,
        "decision": (
            "DRY_RUN_ACCEPTED__RUN_FOUR_REGULATOR_COARSE_SCAN"
            if accepted
            else "FOUR_REGULATOR_COARSE_SCAN_DRY_RUN_BLOCKED"
        ),
        "missing_paths": missing,
        "parent_E0025_validation_passes": parent_passes,
        "target_regulator_count": len(TARGET_REGULATORS),
        "nodes_per_regulator": len(base_plan()) if parent_passes else 0,
        "planned_node_count": len(plan),
        "claim_boundary": {
            "valid_for_five_finite_regulator_fixed_decay_integrals": False,
            **{field: False for field in CLAIM_FIELDS},
        },
        "runtime_seconds": time.perf_counter() - started,
    }
    atomic_json(DRY_RUN, result)
    return result


def manifest_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for epsilon_id, epsilon in TARGET_REGULATORS:
        expected = plan_sha256(epsilon_id, epsilon)
        for node in base_plan():
            complete = shard_complete(epsilon_id, node, expected)
            result = (
                read_json(shard_paths(epsilon_id, node["node_id"])["result"])
                if complete
                else {}
            )
            rows.append(
                {
                    "epsilon_id": epsilon_id,
                    "epsilon": epsilon,
                    **node,
                    "shard_state": (
                        "COMPLETE_PASS"
                        if complete and bool(result["acceptance_passed"])
                        else ("COMPLETE_FAIL" if complete else "PENDING")
                    ),
                    "runtime_seconds": result.get("runtime_seconds", ""),
                    "node_result_path": str(
                        shard_paths(epsilon_id, node["node_id"])["result"]
                    ),
                    **{field: False for field in CLAIM_FIELDS},
                }
            )
    return rows


def regulator_aggregation(
    epsilon_id: str, epsilon: float
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]] | None:
    expected = plan_sha256(epsilon_id, epsilon)
    plan = base_plan()
    if not all(shard_complete(epsilon_id, node, expected) for node in plan):
        return None
    results = [
        read_json(shard_paths(epsilon_id, node["node_id"])["result"])
        for node in plan
    ]
    old = set_kernel_globals(epsilon_id, epsilon)
    try:
        outer, panels, metrics = M5312.aggregate_outer_integrals(plan, results)
    finally:
        restore_kernel_globals(old)
    for row in outer:
        row["scan_checkpoint"] = CHECKPOINT
    for row in panels:
        row["epsilon_id"] = epsilon_id
        row["epsilon"] = epsilon
    return outer, panels, {"results": results, **metrics}


def E0025_summary() -> dict[str, Any]:
    result = read_json(RESULT_5315)
    return {
        "epsilon_id": "E0025",
        "epsilon": 0.0025,
        "method": "REFINED_SIMPLE_POLE_PLUS_SQUARED_EVENT_COORDINATE",
        "all_nodes_complete": True,
        "all_nodes_pass": True,
        "coarse_outer_gate_passes": False,
        "finite_regulator_integral_accepted": True,
        "failing_panel_ids": "",
        "outer_error_relative": result[
            "panel_nine_outer_error_relative_conservative"
        ],
        "inner_error_budget_relative": "",
        "fixed_decay_integral_real": result[
            "reassembled_E0025_fixed_decay_integral_real"
        ],
        "fixed_decay_integral_imaginary": result[
            "reassembled_E0025_fixed_decay_integral_imaginary"
        ],
        "source_result_path": str(RESULT_5315),
        **{field: False for field in CLAIM_FIELDS},
    }


def source_rows() -> list[dict[str, str]]:
    paths = [
        Path(__file__).resolve(),
        SCRIPT_5312,
        SCRIPT_5315,
        RESULT_5315,
        VALIDATION_5315,
        CONTRACT_5312,
        NODE_PLAN_5312,
    ]
    return [{"path": str(path), "sha256": digest(path)} for path in paths]


def execute(runtime_limit_seconds: float) -> dict[str, Any]:
    M5312.set_below_normal_priority()
    M5312.mp.mp.dps = M5312.M5280.MP_DECIMAL_DIGITS
    M5312.M5301.configure_reused_pipeline()
    started = time.perf_counter()
    dry = dry_run()
    if not dry["acceptance_passed"]:
        raise RuntimeError("5316 dry run did not pass")
    contract = read_csv(CONTRACT_5312)
    base_context = M5312.M5303.synthetic_context()
    multiplier = M5312.M5309.physical_multiplier()
    paused = False
    for epsilon_id, epsilon in TARGET_REGULATORS:
        expected = plan_sha256(epsilon_id, epsilon)
        for node in base_plan():
            if shard_complete(epsilon_id, node, expected):
                continue
            if time.perf_counter() - started >= runtime_limit_seconds:
                paused = True
                break
            result = run_kernel_node(
                epsilon_id,
                epsilon,
                node,
                contract,
                expected,
                base_context,
                multiplier,
            )
            atomic_json(
                STATUS,
                {
                    "checkpoint": CHECKPOINT,
                    "state": "RUNNING",
                    "epsilon_id": epsilon_id,
                    "last_completed_node_id": node["node_id"],
                    "last_node_acceptance_passed": result["acceptance_passed"],
                },
            )
        if paused:
            break
    manifest = manifest_rows()
    write_csv(MANIFEST, manifest, ["epsilon_id", "node_id", "shard_state"])
    outer_rows: list[dict[str, Any]] = []
    panel_rows: list[dict[str, Any]] = []
    summaries = [E0025_summary()]
    for epsilon_id, epsilon in TARGET_REGULATORS:
        aggregate = regulator_aggregation(epsilon_id, epsilon)
        regulator_manifest = [
            row for row in manifest if row["epsilon_id"] == epsilon_id
        ]
        if aggregate is None:
            summaries.append(
                {
                    "epsilon_id": epsilon_id,
                    "epsilon": epsilon,
                    "method": "POLE_SUBTRACTED_COARSE_SCAN",
                    "all_nodes_complete": False,
                    "all_nodes_pass": False,
                    "coarse_outer_gate_passes": False,
                    "finite_regulator_integral_accepted": False,
                    "failing_panel_ids": "PENDING",
                    "outer_error_relative": math.inf,
                    "inner_error_budget_relative": math.inf,
                    "fixed_decay_integral_real": 0.0,
                    "fixed_decay_integral_imaginary": 0.0,
                    "source_result_path": "",
                    **{field: False for field in CLAIM_FIELDS},
                }
            )
            continue
        local_outer, local_panels, metrics = aggregate
        outer_rows.extend(local_outer)
        panel_rows.extend(local_panels)
        all_nodes_pass = all(
            row["shard_state"] == "COMPLETE_PASS" for row in regulator_manifest
        )
        failing_panels = [
            str(row["x_panel_index"])
            for row in local_panels
            if float(row["outer_Q2_Q4_relative_change"]) > OUTER_CHANGE_LIMIT
        ]
        outer_gate = (
            all_nodes_pass
            and float(metrics["outer_Q2_Q4_relative_change"])
            <= OUTER_CHANGE_LIMIT
            and float(metrics["outer_Q4_inner_energy_error_budget_relative"])
            <= INNER_ERROR_BUDGET_LIMIT
        )
        selected = complex(
            float(metrics["selected_E0025_fixed_decay_outer_soft_integral_real"]),
            float(metrics["selected_E0025_fixed_decay_outer_soft_integral_imaginary"]),
        )
        summaries.append(
            {
                "epsilon_id": epsilon_id,
                "epsilon": epsilon,
                "method": "POLE_SUBTRACTED_COARSE_SCAN",
                "all_nodes_complete": True,
                "all_nodes_pass": all_nodes_pass,
                "coarse_outer_gate_passes": outer_gate,
                "finite_regulator_integral_accepted": outer_gate,
                "failing_panel_ids": "|".join(failing_panels),
                "outer_error_relative": metrics["outer_Q2_Q4_relative_change"],
                "inner_error_budget_relative": metrics[
                    "outer_Q4_inner_energy_error_budget_relative"
                ],
                **complex_fields("fixed_decay_integral", selected),
                "source_result_path": str(RESULT),
                **{field: False for field in CLAIM_FIELDS},
            }
        )
    write_csv(OUTER_TOTALS, outer_rows, ["epsilon_id", "outer_order", "energy_order"])
    write_csv(PANEL_CONVERGENCE, panel_rows, ["epsilon_id", "x_panel_index"])
    write_csv(REGULATOR_SUMMARY, summaries, ["epsilon_id"])
    all_complete = all(row["shard_state"] != "PENDING" for row in manifest)
    all_nodes_pass = all_complete and all(
        row["shard_state"] == "COMPLETE_PASS" for row in manifest
    )
    accepted_regulators = sum(
        parse_bool(row["finite_regulator_integral_accepted"]) for row in summaries
    )
    all_five_accepted = accepted_regulators == 5
    if paused or not all_complete:
        decision = "FOUR_REGULATOR_COARSE_SCAN_PAUSED__RESUME_SAVED_SHARDS"
    elif not all_nodes_pass:
        decision = "FOUR_REGULATOR_COARSE_SCAN_LOCALIZES_INNER_NODE_FAILURES"
    elif all_five_accepted:
        decision = "FIVE_FINITE_REGULATORS_CONVERGED__FIT_REGULATOR_ZERO_LIMIT"
    else:
        decision = "FOUR_REGULATOR_COARSE_SCAN_LOCALIZES_REQUIRED_OUTER_REPAIRS"
    formal_end = M5283.formal_inventory_digest()
    parent = read_json(RESULT_5315)
    result = {
        "checkpoint": CHECKPOINT,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "mode": "four-regulator-pole-subtracted-coarse-scan",
        "acceptance_passed": all_complete and all_nodes_pass,
        "decision": decision,
        "planned_node_count": len(manifest),
        "completed_node_count": sum(
            row["shard_state"] != "PENDING" for row in manifest
        ),
        "failed_inner_node_count": sum(
            row["shard_state"] == "COMPLETE_FAIL" for row in manifest
        ),
        "coarse_accepted_finite_regulator_count_including_E0025": accepted_regulators,
        "all_five_finite_regulators_accepted": all_five_accepted,
        "regulator_summary_rows": summaries,
        "formalization_workbench_reference_digest": parent[
            "formalization_workbench_end_digest"
        ],
        "formalization_workbench_end_digest": formal_end,
        "formalization_workbench_modified_file_count": (
            0 if formal_end == parent["formalization_workbench_end_digest"] else -1
        ),
        "claim_boundary": {
            "valid_for_five_finite_regulator_fixed_decay_integrals": all_five_accepted,
            **{field: False for field in CLAIM_FIELDS},
            "reason": (
                "This coarse scan accepts only regulators satisfying all node and "
                "outer gates. Failed coarse outer panels require the already-derived "
                "event-coordinate repair before a regulator-zero fit is allowed."
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
            "state": "COMPLETE_DIAGNOSTIC" if all_complete else "PAUSED_RESUMABLE",
            "decision": decision,
            "completed_node_count": result["completed_node_count"],
            "planned_node_count": len(manifest),
        },
    )
    return result


def render_document(result: dict[str, Any], passed: bool) -> None:
    lines = [
        "# 5316 - Four-regulator pole-subtracted coarse scan",
        "",
        "## Result",
        "",
        "The validated E0025 result is retained. The same 54-node, pole-subtracted",
        "topology plan is evaluated independently at E005, E010, E020, and E040.",
        "A coarse failure is not extrapolated away: its exact panels are handed to",
        "the event-coordinate repair before any regulator-zero fit.",
        "",
        f"- completed nodes: `{result['completed_node_count']}` / `{result['planned_node_count']}`;",
        f"- failed inner nodes: `{result['failed_inner_node_count']}`;",
        f"- accepted finite regulators: `{result['coarse_accepted_finite_regulator_count_including_E0025']}` / 5;",
        f"- decision: **{result['decision']}**;",
        f"- validation: **{'PASS' if passed else 'FAIL'}**.",
        "",
        "| regulator | nodes | coarse gate | failing panels | value |",
        "|---|---:|---:|---|---:|",
    ]
    for row in result["regulator_summary_rows"]:
        lines.append(
            "| {epsilon_id} | {complete} | {gate} | {panels} | {real:.9g} {imag:+.9g} i |".format(
                epsilon_id=row["epsilon_id"],
                complete="yes" if row["all_nodes_complete"] else "no",
                gate="yes" if row["finite_regulator_integral_accepted"] else "no",
                panels=row["failing_panel_ids"] or "-",
                real=float(row["fixed_decay_integral_real"]),
                imag=float(row["fixed_decay_integral_imaginary"]),
            )
        )
    lines.extend(
        [
            "",
            "## Claim boundary",
            "",
            "No regulator-zero, decay-angle, phase-space, UV, local-GR, or full-MTS",
            "claim follows from this coarse scan.",
        ]
    )
    DOCUMENT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def validate_outputs() -> dict[str, Any]:
    started = time.perf_counter()
    result = read_json(RESULT)
    dry = read_json(DRY_RUN)
    manifest = read_csv(MANIFEST)
    summaries = read_csv(REGULATOR_SUMMARY)
    source_current = all(
        Path(row["path"]).exists()
        and digest(Path(row["path"])) == row["sha256"]
        for row in result["source_files"]
    )
    gates = [
        validation_gate(
            "dry_run_and_diagnostic_complete",
            bool(dry["acceptance_passed"])
            and int(result["completed_node_count"]) == int(result["planned_node_count"]),
            result["decision"],
        ),
        validation_gate(
            "all_kernel_nodes_pass",
            bool(manifest)
            and all(row["shard_state"] == "COMPLETE_PASS" for row in manifest)
            and int(result["failed_inner_node_count"]) == 0,
            f"nodes={len(manifest)}",
        ),
        validation_gate(
            "five_regulators_have_explicit_status",
            len(summaries) == 5
            and {row["epsilon_id"] for row in summaries}
            == {"E040", "E020", "E010", "E005", "E0025"},
            f"rows={len(summaries)}",
        ),
        validation_gate(
            "failed_coarse_regulators_are_not_claimed",
            all(
                parse_bool(row["finite_regulator_integral_accepted"])
                or bool(row["failing_panel_ids"])
                for row in summaries
            ),
            "every nonaccepted row names pending or failing panels",
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
            "no broad claim",
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
            "VALIDATED_FOUR_REGULATOR_COARSE_LOCALIZATION"
            if passed
            else "FOUR_REGULATOR_COARSE_SCAN_VALIDATION_FAILED"
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
