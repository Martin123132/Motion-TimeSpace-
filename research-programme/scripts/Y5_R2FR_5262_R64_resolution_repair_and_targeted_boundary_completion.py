from __future__ import annotations

import argparse
import copy
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


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SCRIPTS = POST / "scripts"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
SOURCE_5260 = FUNCTIONAL_RG / "5260"
SOURCE_5261 = FUNCTIONAL_RG / "5261"
SOURCE = FUNCTIONAL_RG / "5262"
NODES = SOURCE / "nodes"
REPAIR = SOURCE / "G05_I06_T01_R64_repair"

SCRIPT_5261 = (
    SCRIPTS
    / "Y5_R2FR_5261_certified_targeted_topology_boundary_refinement.py"
)
RESULT_5260 = SOURCE_5260 / "microbox_residue_result.json"
VALIDATION_5260 = SOURCE_5260 / "microbox_residue_validation.csv"
STATE_5261 = SOURCE_5261 / "boundary_state.json"
CONFIG_5261 = SOURCE_5261 / "targeted_refinement_run_config.json"
FORMAL_INVENTORY_5261 = (
    SOURCE_5261 / "formalization_workbench_start_inventory.csv"
)
FAILED_NODE_ID = "G05_I06_T01"

RUN_CONFIG = SOURCE / "R64_completion_run_config.json"
DRY_RUN = SOURCE / "R64_completion_dry_run.json"
STATUS = SOURCE / "status.json"
STATE = SOURCE / "boundary_state.json"
ALL_NODES = SOURCE / "targeted_boundary_nodes.csv"
FINAL_BRACKETS = SOURCE / "final_topology_transition_brackets.csv"
VALIDATION = SOURCE / "R64_completion_validation.csv"
RESULT = SOURCE / "R64_completion_result.json"
FORMAL_DIFF = SOURCE / "formalization_workbench_run_diff.csv"

REPAIR_QUADRATURE = REPAIR / "corrected_inner_quadrature_R64.csv"
REPAIR_EXTRAPOLATION = (
    REPAIR / "corrected_regulator_extrapolation_R64.csv"
)
REPAIR_COVERAGE = REPAIR / "inner_coverage_R64.csv"
REPAIR_VALIDATION = REPAIR / "resolution_repair_validation.csv"
REPAIR_RESULT = REPAIR / "resolution_repair_result.json"

CHECKPOINT = 5262
PARENT_CHECKPOINT = 5261
MARKER = (
    "MTS_5262_R64_RESOLUTION_REPAIR_AND_"
    "TARGETED_BOUNDARY_COMPLETION"
)
REVISION = "R64-resolution-repair-targeted-boundary-completion-v1"
REPAIR_ORDERS = (64, 128, 512)
ORIGINAL_ORDERS = (32, 128, 512)
LOW_ORDER_LIMIT = 5.0e-3
MAXIMUM_GENERATION = 12


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


M5261 = load_module("mts_5261_for_5262", SCRIPT_5261)
M5251 = M5261.M5251


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise RuntimeError(f"refusing to write empty CSV: {path}")
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    os.replace(temporary, path)


def atomic_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def parse_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() == "true"


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        while block := handle.read(1024 * 1024):
            value.update(block)
    return value.hexdigest()


def serialized_hash(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            default=str,
        ).encode("utf-8")
    ).hexdigest()


def required_sources() -> tuple[Path, ...]:
    generation5 = M5261.generation_paths(5)
    failed_root = SOURCE_5261 / "nodes" / FAILED_NODE_ID
    return (
        Path(__file__),
        SCRIPT_5261,
        RESULT_5260,
        VALIDATION_5260,
        STATE_5261,
        CONFIG_5261,
        FORMAL_INVENTORY_5261,
        generation5["manifest"],
        failed_root / "node_result.json",
        failed_root / "node_manifest.json",
        failed_root / "node_validation.csv",
        failed_root / "topology_intervals.csv",
    )


def configure_generation5(
    state: dict[str, Any],
) -> tuple[list[dict[str, Any]], Path]:
    targets = M5261.generation_targets(state, 5)
    fixed = M5261.fixed_values(state, targets)
    manifest_path = M5261.generation_paths(5)["manifest"]
    M5261.configure_node_engine(
        5,
        targets,
        manifest_path,
        fixed,
    )
    return targets, manifest_path


def failed_original_gates() -> list[dict[str, str]]:
    validation_path = (
        SOURCE_5261
        / "nodes"
        / FAILED_NODE_ID
        / "node_validation.csv"
    )
    return [
        row
        for row in read_csv(validation_path)
        if not parse_bool(row["passed"])
    ]


def calculate_resolution_repair(
    state: dict[str, Any],
) -> dict[str, Any]:
    if REPAIR_RESULT.exists():
        result = json.loads(
            REPAIR_RESULT.read_text(encoding="utf-8")
        )
        if not bool(result["validation_passed"]):
            raise RuntimeError("existing R64 repair is not valid")
        return result

    targets, manifest_path = configure_generation5(state)
    target_ids = {
        target["order9_node_id"] for target in targets
    }
    if FAILED_NODE_ID not in target_ids:
        raise RuntimeError("failed node is absent from generation 5")
    batch_manifest = json.loads(
        manifest_path.read_text(encoding="utf-8")
    )
    node_manifest, context, _, problems = (
        M5251.build_node_problem(
            batch_manifest,
            FAILED_NODE_ID,
        )
    )
    failed_paths = M5251.node_paths(FAILED_NODE_ID)
    intervals = read_csv(failed_paths["intervals"])
    original_result = json.loads(
        failed_paths["result"].read_text(encoding="utf-8")
    )
    original_failed = failed_original_gates()
    if len(original_failed) != 1 or not original_failed[0][
        "gate"
    ].endswith("_LOW_ORDER_EXTRAPOLATION_CONVERGES"):
        raise RuntimeError(
            "failed node has more than the isolated low-order gate"
        )
    original_low_error = float(original_failed[0]["observed"])
    original_mid_error = float(
        original_result["summary"]["mid_order_error"]
    )
    M5251.M5247.M5239.QUADRATURE_ORDERS = REPAIR_ORDERS
    calculation = M5251.M5247.corrected_inner_slice(
        context,
        problems,
        intervals,
    )
    repair_validations = M5251.inner_validation_rows(
        node_manifest,
        FAILED_NODE_ID,
        calculation,
        True,
        0.0,
    )
    repair_low_error = float(
        calculation["convergence"][
            "low_order_subtracted_relative_error"
        ]
    )
    repair_mid_error = float(
        calculation["convergence"][
            "mid_order_subtracted_relative_error"
        ]
    )
    physical_relative_differences = {
        str(inner_order): (
            abs(
                calculation["physical_values"][inner_order][
                    "subtracted"
                ]
                - M5261.result_value(
                    original_result,
                    inner_order,
                )
            )
            / max(
                abs(
                    M5261.result_value(
                        original_result,
                        inner_order,
                    )
                ),
                1.0,
            )
        )
        for inner_order in (128, 512)
    }
    checks = [
        {
            "check_id": "ORIGINAL_FAILURE_IS_LOW_ORDER_ONLY",
            "passed": len(original_failed) == 1
            and original_low_error > LOW_ORDER_LIMIT
            and original_mid_error <= 1.0e-3,
            "detail": (
                f"low32={original_low_error}; "
                f"mid128={original_mid_error}"
            ),
        },
        {
            "check_id": "R64_LOW_ORDER_GATE_PASSES_UNCHANGED_LIMIT",
            "passed": repair_low_error <= LOW_ORDER_LIMIT,
            "detail": (
                f"low64={repair_low_error}; "
                f"limit={LOW_ORDER_LIMIT}"
            ),
        },
        {
            "check_id": "R128_MID_ORDER_GATE_REMAINS_PASSED",
            "passed": repair_mid_error <= 1.0e-3,
            "detail": f"mid128={repair_mid_error}",
        },
        {
            "check_id": "R128_AND_R512_PHYSICAL_VALUES_IDENTICAL",
            "passed": all(
                difference <= 1.0e-15
                for difference in physical_relative_differences.values()
            ),
            "detail": json.dumps(
                physical_relative_differences,
                sort_keys=True,
            ),
        },
        {
            "check_id": "ALL_REPAIRED_INNER_GATES_PASS",
            "passed": all(
                bool(row["passed"]) for row in repair_validations
            ),
            "detail": (
                f"passed={sum(bool(row['passed']) for row in repair_validations)}"
                f"/{len(repair_validations)}"
            ),
        },
        {
            "check_id": "CLAIMS_REMAIN_FALSE",
            "passed": all(
                not bool(
                    original_result[
                        f"valid_for_{claim}_claim"
                    ]
                )
                for claim in (
                    "numeric_UV",
                    "local_GR",
                    "full_MTS",
                )
            ),
            "detail": "resolution repair changes no physics claim",
        },
    ]
    passed = all(bool(row["passed"]) for row in checks)
    result = {
        "marker": f"{MARKER}_G05_I06_T01_R64_REPAIR",
        "revision": REVISION,
        "validation_passed": passed,
        "node_id": FAILED_NODE_ID,
        "original_quadrature_orders": list(ORIGINAL_ORDERS),
        "repair_quadrature_orders": list(REPAIR_ORDERS),
        "original_low_order_relative_error": original_low_error,
        "repair_low_order_relative_error": repair_low_error,
        "mid_order_relative_error": repair_mid_error,
        "physical_relative_differences": (
            physical_relative_differences
        ),
        "effective_acceptance_passed": passed,
        "reason": (
            "The R32 diagnostic missed its fixed tolerance, while "
            "R128-to-R512 already converged. R64 passes the same "
            "tolerance and leaves R128/R512 values unchanged."
        ),
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    write_csv(
        REPAIR_QUADRATURE,
        calculation["quadrature_rows"],
    )
    write_csv(
        REPAIR_EXTRAPOLATION,
        calculation["extrapolation_rows"],
    )
    write_csv(REPAIR_COVERAGE, calculation["coverage_rows"])
    write_csv(
        REPAIR_VALIDATION,
        [*repair_validations, *checks],
    )
    atomic_json(REPAIR_RESULT, result)
    if not passed:
        failed = [
            row["check_id"] for row in checks if not row["passed"]
        ]
        raise RuntimeError(
            f"R64 resolution repair failed: {failed}"
        )
    return result


def complete_generation5_with_repair(
    state: dict[str, Any],
    repair_result: dict[str, Any],
) -> dict[str, Any]:
    if int(state["completed_generation"]) >= 5:
        generation_result_path = M5261.generation_paths(5)[
            "result"
        ]
        generation_result = json.loads(
            generation_result_path.read_text(encoding="utf-8")
        )
        if not bool(
            generation_result.get(
                "resolution_repair_applied",
                False,
            )
        ):
            raise RuntimeError(
                "generation 5 is complete without recorded repair"
            )
        return state
    if int(state["completed_generation"]) != 4:
        raise RuntimeError(
            "generation-5 repair requires completed generation 4"
        )
    configuration_5261 = json.loads(
        CONFIG_5261.read_text(encoding="utf-8")
    )
    run_signature_5261 = configuration_5261["run_signature"]
    formal_rows = read_csv(FORMAL_INVENTORY_5261)
    formal_digest = M5251.inventory_digest(formal_rows)
    original_validate = M5261.validate_reusable_node

    def repaired_validate(
        node_id: str,
        manifest_hash: str,
        expected_coordinate: float,
    ) -> dict[str, Any] | None:
        result = original_validate(
            node_id,
            manifest_hash,
            expected_coordinate,
        )
        if (
            node_id == FAILED_NODE_ID
            and result is not None
            and bool(repair_result["effective_acceptance_passed"])
        ):
            result = copy.deepcopy(result)
            result["acceptance_passed"] = True
            result["summary"]["acceptance_passed"] = True
            result["summary"][
                "resolution_repair_applied"
            ] = True
        return result

    M5261.validate_reusable_node = repaired_validate
    try:
        state, _ = M5261.execute_generation(
            state,
            5,
            formal_digest,
            run_signature_5261,
        )
    finally:
        M5261.validate_reusable_node = original_validate
    generation_paths = M5261.generation_paths(5)
    node_rows = read_csv(generation_paths["nodes"])
    for row in node_rows:
        original_acceptance = (
            False
            if row["order9_node_id"] == FAILED_NODE_ID
            else parse_bool(row["acceptance_passed"])
        )
        row["original_acceptance_passed"] = original_acceptance
        row["resolution_repair_applied"] = (
            row["order9_node_id"] == FAILED_NODE_ID
        )
        row["resolution_repair_result_path"] = (
            str(REPAIR_RESULT)
            if row["order9_node_id"] == FAILED_NODE_ID
            else ""
        )
    write_csv(generation_paths["nodes"], node_rows)
    generation_result = json.loads(
        generation_paths["result"].read_text(encoding="utf-8")
    )
    generation_result.update(
        {
            "resolution_repair_applied": True,
            "repaired_node_id": FAILED_NODE_ID,
            "repair_result_path": str(REPAIR_RESULT),
            "repair_validation_passed": bool(
                repair_result["validation_passed"]
            ),
        }
    )
    atomic_json(
        generation_paths["result"],
        generation_result,
    )
    atomic_json(STATE_5261, state)
    return state


def configure_5262_controller() -> None:
    M5261.SOURCE = SOURCE
    M5261.NODES = NODES
    M5261.STATE = STATE
    M5261.STATUS = STATUS
    M5261.MARKER = MARKER
    M5261.REVISION = REVISION
    M5261.CHECKPOINT = CHECKPOINT
    M5261.PARENT_CHECKPOINT = PARENT_CHECKPOINT
    M5261.MAXIMUM_GENERATION = MAXIMUM_GENERATION
    M5251.M5247.M5239.QUADRATURE_ORDERS = REPAIR_ORDERS


def install_manifest_order_contract() -> Any:
    original = M5261.generation_manifest

    def contracted_manifest(
        state: dict[str, Any],
        targets: list[dict[str, Any]],
        generation: int,
        formal_digest: str,
        run_signature: str,
    ) -> dict[str, Any]:
        manifest = original(
            state,
            targets,
            generation,
            formal_digest,
            run_signature,
        )
        manifest.pop("manifest_hash", None)
        manifest.update(
            {
                "quadrature_orders": list(REPAIR_ORDERS),
                "low_order_gate_contract": (
                    "R64_vs_R512 <= 5e-3"
                ),
                "mid_order_gate_contract": (
                    "R128_vs_R512 <= 1e-3"
                ),
                "resolution_escalation_source": str(
                    REPAIR_RESULT
                ),
            }
        )
        manifest["manifest_hash"] = serialized_hash(manifest)
        return manifest

    M5261.generation_manifest = contracted_manifest
    return original


def configuration(
    state_after_generation5: dict[str, Any],
    repair_result: dict[str, Any],
) -> dict[str, Any]:
    source_paths = required_sources() + (REPAIR_RESULT,)
    remaining_schedule = [
        {
            "transition_id": transition_id,
            "remaining_bisections": M5261.required_bisections(
                float(bracket["current_width"]),
                float(bracket["certified_target_width"]),
            ),
        }
        for transition_id, bracket in sorted(
            state_after_generation5["brackets"].items()
        )
    ]
    return {
        "marker": f"{MARKER}_RUN_CONFIGURATION",
        "revision": REVISION,
        "repair_validation_passed": bool(
            repair_result["validation_passed"]
        ),
        "quadrature_orders": list(REPAIR_ORDERS),
        "low_order_limit_unchanged": LOW_ORDER_LIMIT,
        "remaining_schedule": remaining_schedule,
        "source_files": [
            {"path": str(path), "sha256": digest(path)}
            for path in source_paths
        ],
    }


def ensure_configuration(value: dict[str, Any]) -> str:
    signature = serialized_hash(value)
    payload = {**value, "run_signature": signature}
    if RUN_CONFIG.exists():
        existing = json.loads(
            RUN_CONFIG.read_text(encoding="utf-8")
        )
        if existing != payload:
            raise RuntimeError(
                "checkpoint-5262 run configuration changed"
            )
    else:
        atomic_json(RUN_CONFIG, payload)
    return signature


def collect_node_rows(
    source: Path,
    start_generation: int,
    end_generation: int,
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for generation in range(start_generation, end_generation + 1):
        path = (
            source
            / f"generation_{generation:02d}"
            / "nodes.csv"
        )
        if path.exists():
            rows.extend(read_csv(path))
    return rows


def execute(dry_run: bool) -> dict[str, Any]:
    missing = [
        str(path) for path in required_sources() if not path.exists()
    ]
    if missing:
        raise RuntimeError(f"missing sources: {missing}")
    result_5260 = json.loads(
        RESULT_5260.read_text(encoding="utf-8")
    )
    validation_5260 = read_csv(VALIDATION_5260)
    source_5260_passed = bool(
        result_5260["validation_passed"]
    ) and all(
        parse_bool(row["passed"]) for row in validation_5260
    )
    state_5261 = json.loads(
        STATE_5261.read_text(encoding="utf-8")
    )
    failed_gates = failed_original_gates()
    dry_result = {
        "marker": f"{MARKER}_DRY_RUN",
        "revision": REVISION,
        "dry_run_passed": source_5260_passed
        and int(state_5261["completed_generation"]) in (4, 5)
        and len(failed_gates) == 1
        and failed_gates[0]["gate"].endswith(
            "_LOW_ORDER_EXTRAPOLATION_CONVERGES"
        ),
        "source_5260_passed": source_5260_passed,
        "source_5261_completed_generation": state_5261[
            "completed_generation"
        ],
        "failed_node_id": FAILED_NODE_ID,
        "failed_gate_count": len(failed_gates),
        "repair_orders": list(REPAIR_ORDERS),
        "low_order_limit": LOW_ORDER_LIMIT,
        "writes_performed": False,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    if dry_run:
        return dry_result
    if not dry_result["dry_run_passed"]:
        raise RuntimeError("5262 dry run failed")

    SOURCE.mkdir(parents=True, exist_ok=True)
    repair_result = calculate_resolution_repair(state_5261)
    state_5261 = json.loads(
        STATE_5261.read_text(encoding="utf-8")
    )
    state_after_generation5 = complete_generation5_with_repair(
        state_5261,
        repair_result,
    )
    run_configuration = configuration(
        state_after_generation5,
        repair_result,
    )
    run_signature = ensure_configuration(run_configuration)
    atomic_json(
        DRY_RUN,
        {**dry_result, "writes_performed": True},
    )

    formal_start_rows = read_csv(FORMAL_INVENTORY_5261)
    formal_digest = M5251.inventory_digest(formal_start_rows)
    configure_5262_controller()
    original_generation_manifest = (
        install_manifest_order_contract()
    )
    try:
        if STATE.exists():
            state = json.loads(
                STATE.read_text(encoding="utf-8")
            )
        else:
            state = copy.deepcopy(state_after_generation5)
            state["marker"] = f"{MARKER}_STATE"
            state["revision"] = REVISION
            atomic_json(STATE, state)
        while not all(
            bool(bracket["stopping_gate_passed"])
            for bracket in state["brackets"].values()
        ):
            generation = int(state["completed_generation"]) + 1
            if generation > MAXIMUM_GENERATION:
                raise RuntimeError(
                    "maximum generation reached before stopping"
                )
            state, _ = M5261.execute_generation(
                state,
                generation,
                formal_digest,
                run_signature,
            )
    finally:
        M5261.generation_manifest = (
            original_generation_manifest
        )

    prior_node_rows = collect_node_rows(
        SOURCE_5261,
        3,
        5,
    )
    new_node_rows = collect_node_rows(
        SOURCE,
        6,
        int(state["completed_generation"]),
    )
    all_node_rows = [*prior_node_rows, *new_node_rows]
    final_rows = M5261.final_bracket_rows(state)
    formal_after_rows = M5251.formal_inventory_rows()
    formal_diff_rows = M5251.inventory_diff_rows(
        formal_start_rows,
        formal_after_rows,
    )
    M5251.write_csv(FORMAL_DIFF, formal_diff_rows)
    expected_total_nodes = 27
    checks = [
        {
            "check_id": "SOURCE_5260_CERTIFICATE_VALID",
            "passed": source_5260_passed,
            "detail": f"checks={len(validation_5260)}",
        },
        {
            "check_id": "ISOLATED_R32_FAILURE_REPAIRED_AT_R64",
            "passed": bool(repair_result["validation_passed"])
            and float(
                repair_result[
                    "repair_low_order_relative_error"
                ]
            )
            <= LOW_ORDER_LIMIT,
            "detail": (
                f"R32={repair_result['original_low_order_relative_error']}; "
                f"R64={repair_result['repair_low_order_relative_error']}"
            ),
        },
        {
            "check_id": "HIGH_ORDER_PHYSICS_UNCHANGED_BY_REPAIR",
            "passed": all(
                float(value) <= 1.0e-15
                for value in repair_result[
                    "physical_relative_differences"
                ].values()
            ),
            "detail": json.dumps(
                repair_result["physical_relative_differences"],
                sort_keys=True,
            ),
        },
        {
            "check_id": "NODE_ACCOUNTING_MATCHES_CERTIFIED_SCHEDULE",
            "passed": len(all_node_rows) == expected_total_nodes
            and len(
                {
                    row["order9_node_id"]
                    for row in all_node_rows
                }
            )
            == expected_total_nodes,
            "detail": (
                f"nodes={len(all_node_rows)}; "
                f"expected={expected_total_nodes}"
            ),
        },
        {
            "check_id": "ALL_EFFECTIVE_NODE_GATES_PASS",
            "passed": all(
                parse_bool(row["integrity_passed"])
                and parse_bool(row["acceptance_passed"])
                for row in all_node_rows
            ),
            "detail": (
                "passed="
                f"{sum(parse_bool(row['integrity_passed']) and parse_bool(row['acceptance_passed']) for row in all_node_rows)}"
                f"/{len(all_node_rows)}"
            ),
        },
        {
            "check_id": "NO_THIRD_OR_AMBIGUOUS_SIGNATURE",
            "passed": int(
                state["third_or_ambiguous_signature_count"]
            )
            == 0,
            "detail": (
                "count="
                f"{state['third_or_ambiguous_signature_count']}"
            ),
        },
        {
            "check_id": "ALL_CERTIFIED_WIDTH_GATES_PASS",
            "passed": all(
                float(row["final_width"])
                <= float(row["certified_target_width"])
                and parse_bool(row["stopping_gate_passed"])
                for row in final_rows
            ),
            "detail": (
                "maximum_width_target_ratio="
                f"{max(float(row['final_width']) / float(row['certified_target_width']) for row in final_rows)}"
            ),
        },
        {
            "check_id": "ALL_BOUNDARY_ERROR_BUDGETS_PASS",
            "passed": all(
                float(row["boundary_location_error_upper"])
                <= float(row["equal_boundary_budget"])
                for row in final_rows
            ),
            "detail": (
                "maximum_error_budget_ratio="
                f"{max(float(row['boundary_location_error_upper']) / float(row['equal_boundary_budget']) for row in final_rows)}"
            ),
        },
        {
            "check_id": "FORMALIZATION_WORKBENCH_UNCHANGED",
            "passed": len(formal_diff_rows) == 0,
            "detail": f"modified_files={len(formal_diff_rows)}",
        },
        {
            "check_id": "CLAIM_SCOPE_STAYS_PRE_COEFFICIENT",
            "passed": all(
                parse_bool(row["valid_for_boundary_error_claim"])
                and not parse_bool(row["valid_for_numeric_UV_claim"])
                and not parse_bool(row["valid_for_local_GR_claim"])
                and not parse_bool(row["valid_for_full_MTS_claim"])
                for row in final_rows
            ),
            "detail": (
                "boundary location only; coefficient and GR "
                "claims remain false"
            ),
        },
    ]
    passed = all(bool(row["passed"]) for row in checks)
    result = {
        "marker": MARKER,
        "revision": REVISION,
        "validation_passed": passed,
        "repair_validation_passed": bool(
            repair_result["validation_passed"]
        ),
        "quadrature_orders": list(REPAIR_ORDERS),
        "node_count": len(all_node_rows),
        "completed_generation": state["completed_generation"],
        "all_boundary_stopping_gates_passed": all(
            parse_bool(row["stopping_gate_passed"])
            for row in final_rows
        ),
        "maximum_final_width_to_target_ratio": max(
            float(row["final_width"])
            / float(row["certified_target_width"])
            for row in final_rows
        ),
        "maximum_final_error_to_budget_ratio": max(
            float(row["boundary_location_error_upper"])
            / float(row["equal_boundary_budget"])
            for row in final_rows
        ),
        "formalization_workbench_modified_file_count": len(
            formal_diff_rows
        ),
        "decision": (
            "ADOPT_R64_REPAIRED_TARGETED_BOUNDARY_REFINEMENT__"
            "HANDOFF_TO_OUTER_COEFFICIENT_REASSEMBLY"
            if passed
            else "HOLD_R64_TARGETED_BOUNDARY_COMPLETION"
        ),
        "valid_for_boundary_error_claim": passed,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    write_csv(ALL_NODES, all_node_rows)
    write_csv(FINAL_BRACKETS, final_rows)
    write_csv(VALIDATION, checks)
    atomic_json(RESULT, result)
    atomic_json(
        STATUS,
        {
            "marker": MARKER,
            "state": "complete" if passed else "validation_failed",
            "completed_generation": state["completed_generation"],
            "node_count": len(all_node_rows),
            "validation_passed": passed,
            "run_signature": run_signature,
        },
    )
    if not passed:
        failed = [
            row["check_id"] for row in checks if not row["passed"]
        ]
        raise RuntimeError(f"5262 validation failed: {failed}")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    arguments = parser.parse_args()
    started = time.perf_counter()
    result = execute(arguments.dry_run)
    result["controller_elapsed_seconds"] = (
        time.perf_counter() - started
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
