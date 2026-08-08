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
SOURCE_5262 = FUNCTIONAL_RG / "5262"
SOURCE = FUNCTIONAL_RG / "5263"
NODES = SOURCE / "nodes"
REPAIR = SOURCE / "G08_I01_T00_R96_repair"

SCRIPT_5262 = (
    SCRIPTS
    / "Y5_R2FR_5262_R64_resolution_repair_and_targeted_boundary_completion.py"
)
RESULT_5260 = SOURCE_5260 / "microbox_residue_result.json"
VALIDATION_5260 = SOURCE_5260 / "microbox_residue_validation.csv"
STATE_5262 = SOURCE_5262 / "boundary_state.json"
CONFIG_5262 = SOURCE_5262 / "R64_completion_run_config.json"
FORMAL_INVENTORY = (
    SOURCE_5261 / "formalization_workbench_start_inventory.csv"
)
FAILED_NODE_ID = "G08_I01_T00"
FAILED_NODE_ROOT = SOURCE_5262 / "nodes" / FAILED_NODE_ID

RUN_CONFIG = SOURCE / "R96_completion_run_config.json"
DRY_RUN = SOURCE / "R96_completion_dry_run.json"
STATUS = SOURCE / "status.json"
STATE = SOURCE / "boundary_state.json"
ALL_NODES = SOURCE / "targeted_boundary_nodes.csv"
FINAL_BRACKETS = SOURCE / "final_topology_transition_brackets.csv"
VALIDATION = SOURCE / "R96_completion_validation.csv"
RESULT = SOURCE / "R96_completion_result.json"
FORMAL_DIFF = SOURCE / "formalization_workbench_run_diff.csv"

REPAIR_QUADRATURE = REPAIR / "corrected_inner_quadrature_R96.csv"
REPAIR_EXTRAPOLATION = (
    REPAIR / "corrected_regulator_extrapolation_R96.csv"
)
REPAIR_COVERAGE = REPAIR / "inner_coverage_R96.csv"
REPAIR_VALIDATION = REPAIR / "resolution_repair_validation.csv"
REPAIR_RESULT = REPAIR / "resolution_repair_result.json"

CHECKPOINT = 5263
PARENT_CHECKPOINT = 5262
MARKER = (
    "MTS_5263_R96_RESOLUTION_REPAIR_AND_"
    "TARGETED_BOUNDARY_COMPLETION"
)
REVISION = "R96-resolution-repair-targeted-boundary-completion-v1"
REPAIR_ORDERS = (96, 128, 512)
ORIGINAL_ORDERS = (64, 128, 512)
LOW_ORDER_LIMIT = 5.0e-3
MID_ORDER_LIMIT = 1.0e-3
MINIMUM_RAW_IMPROVEMENT = 10.0
MAXIMUM_GENERATION = 12
INNER_ORDERS = (128, 512)


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


M5262 = load_module("mts_5262_for_5263", SCRIPT_5262)
M5261 = M5262.M5261
M5251 = M5262.M5251


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


def failed_node_paths() -> dict[str, Path]:
    return {
        "manifest": FAILED_NODE_ROOT / "node_manifest.json",
        "result": FAILED_NODE_ROOT / "node_result.json",
        "validation": FAILED_NODE_ROOT / "node_validation.csv",
        "intervals": FAILED_NODE_ROOT / "topology_intervals.csv",
    }


def required_sources() -> tuple[Path, ...]:
    failed = failed_node_paths()
    parent_generation = SOURCE_5262 / "generation_08" / "manifest.json"
    return (
        Path(__file__),
        SCRIPT_5262,
        RESULT_5260,
        VALIDATION_5260,
        STATE_5262,
        CONFIG_5262,
        FORMAL_INVENTORY,
        parent_generation,
        failed["manifest"],
        failed["result"],
        failed["validation"],
        failed["intervals"],
    )


def failed_original_gates() -> list[dict[str, str]]:
    return [
        row
        for row in read_csv(failed_node_paths()["validation"])
        if not parse_bool(row["passed"])
    ]


def configure_parent_generation8(
    state: dict[str, Any],
) -> tuple[list[dict[str, Any]], Path]:
    M5262.configure_5262_controller()
    targets = M5261.generation_targets(state, 8)
    fixed = M5261.fixed_values(state, targets)
    manifest_path = M5261.generation_paths(8)["manifest"]
    M5261.configure_node_engine(
        8,
        targets,
        manifest_path,
        fixed,
    )
    return targets, manifest_path


def calculate_resolution_repair(
    parent_state: dict[str, Any],
) -> dict[str, Any]:
    if REPAIR_RESULT.exists():
        result = json.loads(
            REPAIR_RESULT.read_text(encoding="utf-8")
        )
        if not bool(result["validation_passed"]):
            raise RuntimeError("existing R96 repair is invalid")
        return result

    targets, manifest_path = configure_parent_generation8(
        parent_state
    )
    if FAILED_NODE_ID not in {
        target["order9_node_id"] for target in targets
    }:
        raise RuntimeError("failed node is absent from generation 8")
    batch_manifest = json.loads(
        manifest_path.read_text(encoding="utf-8")
    )
    node_manifest, context, _, problems = (
        M5251.build_node_problem(
            batch_manifest,
            FAILED_NODE_ID,
        )
    )
    failed = failed_node_paths()
    intervals = read_csv(failed["intervals"])
    original_result = json.loads(
        failed["result"].read_text(encoding="utf-8")
    )
    failed_gates = failed_original_gates()
    if len(failed_gates) != 1 or not failed_gates[0][
        "gate"
    ].endswith("_LOW_ORDER_EXTRAPOLATION_CONVERGES"):
        raise RuntimeError(
            "generation-8 failure is not isolated to low order"
        )
    original_low_error = float(failed_gates[0]["observed"])
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
    convergence = calculation["convergence"]
    repair_low_error = float(
        convergence["low_order_subtracted_relative_error"]
    )
    repair_mid_error = float(
        convergence["mid_order_subtracted_relative_error"]
    )
    raw_low_error = float(
        convergence["low_order_raw_relative_error"]
    )
    improvement = float(
        convergence["low_order_improvement_factor"]
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
        for inner_order in INNER_ORDERS
    }
    checks = [
        {
            "check_id": "ORIGINAL_FAILURE_IS_LOW_ORDER_ONLY",
            "passed": len(failed_gates) == 1
            and original_low_error > LOW_ORDER_LIMIT
            and original_mid_error <= MID_ORDER_LIMIT,
            "detail": (
                f"R64={original_low_error}; "
                f"R128={original_mid_error}"
            ),
        },
        {
            "check_id": "R96_LOW_ORDER_GATE_PASSES_UNCHANGED_LIMIT",
            "passed": repair_low_error <= LOW_ORDER_LIMIT,
            "detail": (
                f"R96={repair_low_error}; "
                f"limit={LOW_ORDER_LIMIT}"
            ),
        },
        {
            "check_id": "R128_MID_ORDER_GATE_REMAINS_PASSED",
            "passed": repair_mid_error <= MID_ORDER_LIMIT,
            "detail": (
                f"R128={repair_mid_error}; "
                f"limit={MID_ORDER_LIMIT}"
            ),
        },
        {
            "check_id": "R96_SUBTRACTION_IMPROVES_RAW_LOW_ORDER",
            "passed": improvement >= MINIMUM_RAW_IMPROVEMENT,
            "detail": (
                f"raw={raw_low_error}; "
                f"subtracted={repair_low_error}; "
                f"improvement={improvement}"
            ),
        },
        {
            "check_id": "R128_AND_R512_PHYSICS_UNCHANGED",
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
        "marker": f"{MARKER}_G08_I01_T00_R96_REPAIR",
        "revision": REVISION,
        "validation_passed": passed,
        "node_id": FAILED_NODE_ID,
        "original_quadrature_orders": list(ORIGINAL_ORDERS),
        "repair_quadrature_orders": list(REPAIR_ORDERS),
        "original_low_order_relative_error": original_low_error,
        "repair_low_order_raw_relative_error": raw_low_error,
        "repair_low_order_relative_error": repair_low_error,
        "repair_mid_order_relative_error": repair_mid_error,
        "repair_low_order_improvement_factor": improvement,
        "physical_relative_differences": (
            physical_relative_differences
        ),
        "effective_acceptance_passed": passed,
        "reason": (
            "R64 missed the unchanged low-order limit while R128 "
            "already passed. R96 passes both the unchanged error "
            "limit and the raw-to-subtracted improvement gate, "
            "without changing R128 or R512."
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
        failed_checks = [
            row["check_id"] for row in checks if not row["passed"]
        ]
        raise RuntimeError(
            f"R96 resolution repair failed: {failed_checks}"
        )
    return result


def configure_5263_controller() -> None:
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
                    "R96_vs_R512 <= 5e-3"
                ),
                "mid_order_gate_contract": (
                    "R128_vs_R512 <= 1e-3"
                ),
                "minimum_low_order_improvement": (
                    MINIMUM_RAW_IMPROVEMENT
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


def run_configuration(
    parent_state: dict[str, Any],
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
            parent_state["brackets"].items()
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
        "mid_order_limit_unchanged": MID_ORDER_LIMIT,
        "minimum_raw_improvement": MINIMUM_RAW_IMPROVEMENT,
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
                "checkpoint-5263 run configuration changed"
            )
    else:
        atomic_json(RUN_CONFIG, payload)
    return signature


def effective_node_row(
    target: dict[str, Any],
    result: dict[str, Any],
    result_path: Path,
    signature: tuple[str, ...],
    generation: int,
    reused: bool,
    external_repair: bool,
) -> dict[str, Any]:
    values = {
        inner_order: M5261.result_value(
            result,
            inner_order,
        )
        for inner_order in INNER_ORDERS
    }
    return {
        **target,
        "generation": generation,
        "active_pole_count": len(signature),
        "active_pole_signature": json.dumps(signature),
        "order128_subtracted_real": values[128].real,
        "order128_subtracted_imaginary": values[128].imag,
        "order512_subtracted_real": values[512].real,
        "order512_subtracted_imaginary": values[512].imag,
        "integrity_passed": True,
        "acceptance_passed": True,
        "original_acceptance_passed": bool(
            result["acceptance_passed"]
        ),
        "resolution_repair_applied": external_repair,
        "resolution_repair_result_path": (
            str(REPAIR_RESULT) if external_repair else ""
        ),
        "elapsed_seconds": result["elapsed_seconds"],
        "reused_completed_node": reused,
        "result_path": str(result_path),
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }


def apply_generation_rows(
    state: dict[str, Any],
    node_rows: list[dict[str, Any]],
    generation: int,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    bracket_rows: list[dict[str, Any]] = []
    third_signature_count = 0
    for node_row in node_rows:
        transition_id = node_row["transition_id"]
        bracket = state["brackets"][transition_id]
        midpoint_signature = tuple(
            json.loads(node_row["active_pole_signature"])
        )
        left_signature = tuple(
            bracket["left_active_signature"]
        )
        right_signature = tuple(
            bracket["right_active_signature"]
        )
        matches_left = midpoint_signature == left_signature
        matches_right = midpoint_signature == right_signature
        if matches_left == matches_right:
            third_signature_count += 1
            bracket_rows.append(
                {
                    **bracket,
                    "generation": generation,
                    "bisection_node_id": node_row[
                        "order9_node_id"
                    ],
                    "update_status": (
                        "THIRD_OR_AMBIGUOUS_SIGNATURE"
                    ),
                }
            )
            continue
        update_status = (
            "MIDPOINT_MATCHES_LEFT"
            if matches_left
            else "MIDPOINT_MATCHES_RIGHT"
        )
        point_id = node_row["order9_node_id"]
        state["points"][point_id] = {
            "point_id": point_id,
            "generation": generation,
            "decay_cosine": float(node_row["decay_cosine"]),
            "active_signature": list(midpoint_signature),
            "active_pole_count": len(midpoint_signature),
            "result_path": node_row["result_path"],
            "integrity_passed": True,
            "acceptance_passed": True,
            "resolution_repair_applied": parse_bool(
                node_row["resolution_repair_applied"]
            ),
            "values": {
                str(inner_order): {
                    "real": float(
                        node_row[
                            f"order{inner_order}_subtracted_real"
                        ]
                    ),
                    "imaginary": float(
                        node_row[
                            f"order{inner_order}_subtracted_imaginary"
                        ]
                    ),
                }
                for inner_order in INNER_ORDERS
            },
        }
        old_width = float(bracket["current_width"])
        if matches_left:
            bracket["left_point_id"] = point_id
            bracket["left_decay_cosine"] = float(
                node_row["decay_cosine"]
            )
            bracket["left_active_signature"] = list(
                midpoint_signature
            )
        else:
            bracket["right_point_id"] = point_id
            bracket["right_decay_cosine"] = float(
                node_row["decay_cosine"]
            )
            bracket["right_active_signature"] = list(
                midpoint_signature
            )
        new_width = (
            float(bracket["right_decay_cosine"])
            - float(bracket["left_decay_cosine"])
        )
        envelope = float(
            bracket["certified_half_residue_envelope"]
        )
        bracket["generation"] = generation
        bracket["current_width"] = new_width
        bracket["boundary_location_error_upper"] = (
            M5261.ANGULAR_JACOBIAN * new_width * envelope
        )
        bracket[
            "completed_bisections_after_generation2"
        ] = (
            int(
                bracket[
                    "completed_bisections_after_generation2"
                ]
            )
            + 1
        )
        bracket["stopping_gate_passed"] = (
            new_width
            <= float(bracket["certified_target_width"])
        )
        bracket_rows.append(
            {
                **bracket,
                "bisection_node_id": point_id,
                "update_status": update_status,
                "old_bracket_width": old_width,
                "width_reduction_factor": (
                    new_width / old_width
                ),
                "next_bisection_coordinate": 0.5
                * (
                    float(bracket["left_decay_cosine"])
                    + float(bracket["right_decay_cosine"])
                ),
            }
        )
    if third_signature_count:
        raise RuntimeError(
            f"generation {generation} produced "
            f"{third_signature_count} third signatures"
        )
    state["completed_generation"] = generation
    state["all_node_ids"].extend(
        row["order9_node_id"] for row in node_rows
    )
    return state, bracket_rows


def execute_generation8(
    state: dict[str, Any],
    formal_digest: str,
    run_signature: str,
    repair_result: dict[str, Any],
) -> dict[str, Any]:
    if int(state["completed_generation"]) >= 8:
        return state
    if int(state["completed_generation"]) != 7:
        raise RuntimeError(
            "custom generation 8 requires completed generation 7"
        )
    generation = 8
    targets = M5261.generation_targets(state, generation)
    paths = M5261.generation_paths(generation)
    fixed = M5261.fixed_values(state, targets)
    manifest = M5261.generation_manifest(
        state,
        targets,
        generation,
        formal_digest,
        run_signature,
    )
    M5261.ensure_generation_manifest(
        paths["manifest"],
        manifest,
    )
    M5261.configure_node_engine(
        generation,
        targets,
        paths["manifest"],
        fixed,
    )
    node_rows: list[dict[str, Any]] = []
    for target_index, target in enumerate(targets, start=1):
        node_id = target["order9_node_id"]
        if node_id == FAILED_NODE_ID:
            result_path = failed_node_paths()["result"]
            result = json.loads(
                result_path.read_text(encoding="utf-8")
            )
            if not bool(repair_result["validation_passed"]):
                raise RuntimeError("external R96 repair is invalid")
            signature = M5261.active_signature(result_path)
            node_rows.append(
                effective_node_row(
                    target,
                    result,
                    result_path,
                    signature,
                    generation,
                    True,
                    True,
                )
            )
        else:
            result = M5261.validate_reusable_node(
                node_id,
                manifest["manifest_hash"],
                float(target["decay_cosine"]),
            )
            reused = result is not None
            if result is None:
                result = M5251.run_node(node_id)
            if not bool(result["integrity_passed"]):
                raise RuntimeError(
                    f"node integrity failed: {node_id}"
                )
            if not bool(result["acceptance_passed"]):
                raise RuntimeError(
                    f"node acceptance failed: {node_id}"
                )
            result_path = M5251.node_paths(node_id)["result"]
            signature = M5261.active_signature(result_path)
            node_rows.append(
                effective_node_row(
                    target,
                    result,
                    result_path,
                    signature,
                    generation,
                    reused,
                    False,
                )
            )
        atomic_json(
            STATUS,
            {
                "marker": MARKER,
                "state": "running",
                "generation": generation,
                "completed_nodes_in_generation": target_index,
                "total_nodes_in_generation": len(targets),
                "last_node_id": node_id,
                "run_signature": run_signature,
            },
        )
        print(
            f"5263 generation=8 "
            f"node={target_index}/{len(targets)} "
            f"id={node_id}",
            flush=True,
        )
    state, bracket_rows = apply_generation_rows(
        state,
        node_rows,
        generation,
    )
    write_csv(paths["nodes"], node_rows)
    write_csv(paths["brackets"], bracket_rows)
    atomic_json(
        paths["result"],
        {
            "marker": manifest["marker"],
            "generation": generation,
            "node_count": len(node_rows),
            "resolution_repair_applied": True,
            "repaired_node_id": FAILED_NODE_ID,
            "repair_result_path": str(REPAIR_RESULT),
            "all_brackets_halved": all(
                math.isclose(
                    float(row["width_reduction_factor"]),
                    0.5,
                    rel_tol=0.0,
                    abs_tol=2.0e-12,
                )
                for row in bracket_rows
            ),
            "stopped_transition_count": sum(
                bool(bracket["stopping_gate_passed"])
                for bracket in state["brackets"].values()
            ),
            "remaining_transition_count": sum(
                not bool(bracket["stopping_gate_passed"])
                for bracket in state["brackets"].values()
            ),
            "decision": "CONTINUE_TARGETED_BISECTION",
        },
    )
    atomic_json(STATE, state)
    return state


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
    parent_state = json.loads(
        STATE_5262.read_text(encoding="utf-8")
    )
    failed_gates = failed_original_gates()
    dry_result = {
        "marker": f"{MARKER}_DRY_RUN",
        "revision": REVISION,
        "dry_run_passed": source_5260_passed
        and int(parent_state["completed_generation"]) == 7
        and len(failed_gates) == 1
        and failed_gates[0]["gate"].endswith(
            "_LOW_ORDER_EXTRAPOLATION_CONVERGES"
        ),
        "source_5260_passed": source_5260_passed,
        "source_5262_completed_generation": parent_state[
            "completed_generation"
        ],
        "failed_node_id": FAILED_NODE_ID,
        "failed_gate_count": len(failed_gates),
        "repair_orders": list(REPAIR_ORDERS),
        "low_order_limit": LOW_ORDER_LIMIT,
        "mid_order_limit": MID_ORDER_LIMIT,
        "minimum_raw_improvement": MINIMUM_RAW_IMPROVEMENT,
        "writes_performed": False,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    if dry_run:
        return dry_result
    if not dry_result["dry_run_passed"]:
        raise RuntimeError("5263 dry run failed")

    SOURCE.mkdir(parents=True, exist_ok=True)
    repair_result = calculate_resolution_repair(parent_state)
    configuration = run_configuration(
        parent_state,
        repair_result,
    )
    run_signature = ensure_configuration(configuration)
    atomic_json(
        DRY_RUN,
        {**dry_result, "writes_performed": True},
    )
    formal_start_rows = read_csv(FORMAL_INVENTORY)
    formal_digest = M5251.inventory_digest(formal_start_rows)
    configure_5263_controller()
    original_manifest_function = install_manifest_order_contract()
    try:
        if STATE.exists():
            state = json.loads(
                STATE.read_text(encoding="utf-8")
            )
        else:
            state = copy.deepcopy(parent_state)
            state["marker"] = f"{MARKER}_STATE"
            state["revision"] = REVISION
            atomic_json(STATE, state)
        state = execute_generation8(
            state,
            formal_digest,
            run_signature,
            repair_result,
        )
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
            original_manifest_function
        )

    prior_5261 = collect_node_rows(SOURCE_5261, 3, 5)
    prior_5262 = collect_node_rows(SOURCE_5262, 6, 7)
    new_rows = collect_node_rows(
        SOURCE,
        8,
        int(state["completed_generation"]),
    )
    all_node_rows = [*prior_5261, *prior_5262, *new_rows]
    final_rows = M5261.final_bracket_rows(state)
    formal_after_rows = M5251.formal_inventory_rows()
    formal_diff_rows = M5251.inventory_diff_rows(
        formal_start_rows,
        formal_after_rows,
    )
    M5251.write_csv(FORMAL_DIFF, formal_diff_rows)
    checks = [
        {
            "check_id": "SOURCE_5260_CERTIFICATE_VALID",
            "passed": source_5260_passed,
            "detail": f"checks={len(validation_5260)}",
        },
        {
            "check_id": "ISOLATED_R64_FAILURE_REPAIRED_AT_R96",
            "passed": bool(repair_result["validation_passed"])
            and float(
                repair_result[
                    "repair_low_order_relative_error"
                ]
            )
            <= LOW_ORDER_LIMIT,
            "detail": (
                f"R64={repair_result['original_low_order_relative_error']}; "
                f"R96={repair_result['repair_low_order_relative_error']}"
            ),
        },
        {
            "check_id": "R96_RAW_IMPROVEMENT_GATE_PASSES",
            "passed": float(
                repair_result[
                    "repair_low_order_improvement_factor"
                ]
            )
            >= MINIMUM_RAW_IMPROVEMENT,
            "detail": (
                "improvement="
                f"{repair_result['repair_low_order_improvement_factor']}"
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
            "check_id": "NODE_ACCOUNTING_MATCHES_SCHEDULE",
            "passed": len(all_node_rows) == 27
            and len(
                {
                    row["order9_node_id"]
                    for row in all_node_rows
                }
            )
            == 27,
            "detail": f"nodes={len(all_node_rows)}; expected=27",
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
            "ADOPT_R96_REPAIRED_TARGETED_BOUNDARY_REFINEMENT__"
            "HANDOFF_TO_OUTER_COEFFICIENT_REASSEMBLY"
            if passed
            else "HOLD_R96_TARGETED_BOUNDARY_COMPLETION"
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
        failed_checks = [
            row["check_id"] for row in checks if not row["passed"]
        ]
        raise RuntimeError(
            f"5263 validation failed: {failed_checks}"
        )
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
