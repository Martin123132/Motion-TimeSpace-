from __future__ import annotations

import argparse
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
SOURCE_5256 = FUNCTIONAL_RG / "5256"
SOURCE_5260 = FUNCTIONAL_RG / "5260"
SOURCE = FUNCTIONAL_RG / "5261"
NODES = SOURCE / "nodes"

SCRIPT_5256 = (
    SCRIPTS
    / "Y5_R2FR_5256_outer_topology_bisection_generation2_and_half_residue_bound.py"
)
BRACKETS_5256 = SOURCE_5256 / "narrowed_topology_transition_brackets.csv"
RESULT_5256 = SOURCE_5256 / "boundary_bisection_generation2_result.json"
TRANSITIONS_5260 = SOURCE_5260 / "tightened_transition_envelopes.csv"
VALIDATION_5260 = SOURCE_5260 / "microbox_residue_validation.csv"
RESULT_5260 = SOURCE_5260 / "microbox_residue_result.json"

RUN_CONFIG = SOURCE / "targeted_refinement_run_config.json"
DRY_RUN = SOURCE / "targeted_refinement_dry_run.json"
STATUS = SOURCE / "status.json"
STATE = SOURCE / "boundary_state.json"
SCHEDULE = SOURCE / "certified_stopping_schedule.csv"
ALL_NODES = SOURCE / "targeted_boundary_nodes.csv"
FINAL_BRACKETS = SOURCE / "final_topology_transition_brackets.csv"
VALIDATION = SOURCE / "targeted_boundary_validation.csv"
RESULT = SOURCE / "targeted_boundary_result.json"
FORMAL_INVENTORY = SOURCE / "formalization_workbench_start_inventory.csv"
FORMAL_DIFF = SOURCE / "formalization_workbench_run_diff.csv"

CHECKPOINT = 5261
PARENT_CHECKPOINT = 5260
MARKER = "MTS_5261_CERTIFIED_TARGETED_TOPOLOGY_BOUNDARY_REFINEMENT"
REVISION = "certified-targeted-topology-boundary-refinement-v1"
ANGULAR_JACOBIAN = 0.25
MAXIMUM_GENERATION = 12
INNER_ORDERS = (128, 512)
EXPECTED_TRANSITIONS = {
    "I01_T00",
    "I01_T01",
    "I06_T00",
    "I06_T01",
}


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


M5256 = load_module("mts_5256_for_5261", SCRIPT_5256)
M5251 = M5256.M5251
M5254 = M5256.M5254


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
    payload = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        default=str,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def complex_record(value: complex) -> dict[str, float]:
    return {"real": value.real, "imaginary": value.imag}


def record_complex(value: dict[str, Any]) -> complex:
    return complex(
        float(value["real"]),
        float(value["imaginary"]),
    )


def result_value(
    result: dict[str, Any],
    inner_order: int,
) -> complex:
    value = result["physical_values"][str(inner_order)]
    return complex(
        float(value["subtracted_real"]),
        float(value["subtracted_imaginary"]),
    )


def required_bisections(current_width: float, target_width: float) -> int:
    if target_width <= 0.0:
        raise ValueError("target width must be positive")
    if current_width <= target_width:
        return 0
    return math.ceil(math.log2(current_width / target_width))


def resolve_historic_result(point_id: str) -> Path:
    candidates = [
        FUNCTIONAL_RG
        / str(checkpoint)
        / "nodes"
        / point_id
        / "node_result.json"
        for checkpoint in range(5256, 5240, -1)
    ]
    matches = [path for path in candidates if path.exists()]
    if len(matches) != 1:
        raise RuntimeError(
            f"historic point {point_id} resolved to {len(matches)} paths"
        )
    return matches[0]


def active_signature(result_path: Path) -> tuple[str, ...]:
    return M5254.active_signature_from_catalog(
        M5254.result_catalog_path(result_path)
    )


def point_record(
    point_id: str,
    decay_cosine: float,
    signature: tuple[str, ...],
    result_path: Path,
    generation: int,
) -> dict[str, Any]:
    result = json.loads(result_path.read_text(encoding="utf-8"))
    observed_signature = active_signature(result_path)
    if observed_signature != signature:
        raise RuntimeError(
            f"signature mismatch for seed point {point_id}: "
            f"recorded={signature}, observed={observed_signature}"
        )
    return {
        "point_id": point_id,
        "generation": generation,
        "decay_cosine": decay_cosine,
        "active_signature": list(signature),
        "active_pole_count": len(signature),
        "result_path": str(result_path),
        "integrity_passed": bool(result["integrity_passed"]),
        "acceptance_passed": bool(result["acceptance_passed"]),
        "values": {
            str(inner_order): complex_record(
                result_value(result, inner_order)
            )
            for inner_order in INNER_ORDERS
        },
    }


def initial_state() -> dict[str, Any]:
    bracket_rows = read_csv(BRACKETS_5256)
    envelope_rows = read_csv(TRANSITIONS_5260)
    if {
        row["transition_id"] for row in bracket_rows
    } != EXPECTED_TRANSITIONS:
        raise RuntimeError("checkpoint-5256 transition set is incomplete")
    if {
        row["transition_id"] for row in envelope_rows
    } != EXPECTED_TRANSITIONS:
        raise RuntimeError("checkpoint-5260 transition set is incomplete")
    envelope_lookup = {
        row["transition_id"]: row for row in envelope_rows
    }
    points: dict[str, dict[str, Any]] = {}
    brackets: dict[str, dict[str, Any]] = {}
    for bracket in bracket_rows:
        transition_id = bracket["transition_id"]
        left_id = bracket["new_left_point_id"]
        right_id = bracket["new_right_point_id"]
        left_signature = tuple(
            json.loads(bracket["new_left_active_signature"])
        )
        right_signature = tuple(
            json.loads(bracket["new_right_active_signature"])
        )
        if left_signature == right_signature:
            raise RuntimeError(
                f"seed signatures do not bracket {transition_id}"
            )
        left_coordinate = float(
            bracket["new_left_decay_cosine"]
        )
        right_coordinate = float(
            bracket["new_right_decay_cosine"]
        )
        for point_id, coordinate, signature in (
            (left_id, left_coordinate, left_signature),
            (right_id, right_coordinate, right_signature),
        ):
            if point_id not in points:
                points[point_id] = point_record(
                    point_id,
                    coordinate,
                    signature,
                    resolve_historic_result(point_id),
                    2,
                )
        envelope = envelope_lookup[transition_id]
        width = right_coordinate - left_coordinate
        envelope_value = float(
            envelope["half_residue_triangle_envelope"]
        )
        budget = float(envelope["equal_boundary_budget"])
        target_width = float(envelope["certified_target_width"])
        brackets[transition_id] = {
            "transition_id": transition_id,
            "interval_id": bracket["interval_id"],
            "left_point_id": left_id,
            "right_point_id": right_id,
            "left_decay_cosine": left_coordinate,
            "right_decay_cosine": right_coordinate,
            "left_active_signature": list(left_signature),
            "right_active_signature": list(right_signature),
            "generation": 2,
            "initial_width": width,
            "current_width": width,
            "certified_half_residue_envelope": envelope_value,
            "equal_boundary_budget": budget,
            "certified_target_width": target_width,
            "boundary_location_error_upper": (
                ANGULAR_JACOBIAN * width * envelope_value
            ),
            "required_bisections_from_generation2": (
                required_bisections(width, target_width)
            ),
            "completed_bisections_after_generation2": 0,
            "stopping_gate_passed": width <= target_width,
        }
    return {
        "marker": f"{MARKER}_STATE",
        "revision": REVISION,
        "completed_generation": 2,
        "points": points,
        "brackets": brackets,
        "third_or_ambiguous_signature_count": 0,
        "all_node_ids": [],
    }


def schedule_rows(state: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for transition_id in sorted(state["brackets"]):
        bracket = state["brackets"][transition_id]
        required = int(
            bracket["required_bisections_from_generation2"]
        )
        rows.append(
            {
                "transition_id": transition_id,
                "generation2_width": bracket["initial_width"],
                "certified_half_residue_envelope": bracket[
                    "certified_half_residue_envelope"
                ],
                "equal_boundary_budget": bracket[
                    "equal_boundary_budget"
                ],
                "certified_target_width": bracket[
                    "certified_target_width"
                ],
                "required_bisections": required,
                "predicted_stopping_generation": 2 + required,
                "valid_for_boundary_error_claim": True,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    return rows


def run_configuration(state: dict[str, Any]) -> dict[str, Any]:
    source_paths = (
        Path(__file__),
        SCRIPT_5256,
        BRACKETS_5256,
        RESULT_5256,
        TRANSITIONS_5260,
        VALIDATION_5260,
        RESULT_5260,
    )
    return {
        "marker": f"{MARKER}_RUN_CONFIGURATION",
        "revision": REVISION,
        "maximum_generation": MAXIMUM_GENERATION,
        "angular_jacobian": ANGULAR_JACOBIAN,
        "source_files": [
            {"path": str(path), "sha256": digest(path)}
            for path in source_paths
        ],
        "schedule": schedule_rows(state),
    }


def ensure_run_configuration(configuration: dict[str, Any]) -> str:
    signature = serialized_hash(configuration)
    payload = {**configuration, "run_signature": signature}
    if RUN_CONFIG.exists():
        existing = json.loads(RUN_CONFIG.read_text(encoding="utf-8"))
        if existing != payload:
            raise RuntimeError(
                "checkpoint-5261 run configuration changed; "
                "archive the existing 5261 source directory before rerun"
            )
    else:
        atomic_json(RUN_CONFIG, payload)
    return signature


def state_point_value(
    state: dict[str, Any],
    point_id: str,
    inner_order: int,
) -> complex:
    return record_complex(
        state["points"][point_id]["values"][str(inner_order)]
    )


def generation_targets(
    state: dict[str, Any],
    generation: int,
) -> list[dict[str, Any]]:
    targets: list[dict[str, Any]] = []
    active = [
        bracket
        for bracket in state["brackets"].values()
        if not bool(bracket["stopping_gate_passed"])
    ]
    for index, bracket in enumerate(
        sorted(active, key=lambda row: row["transition_id"])
    ):
        transition_id = bracket["transition_id"]
        targets.append(
            {
                "order9_node_id": (
                    f"G{generation:02d}_{transition_id}"
                ),
                "execution_node_id": (
                    f"R{generation:02d}_{index:02d}"
                ),
                "master_index": index,
                "decay_cosine": 0.5
                * (
                    float(bracket["left_decay_cosine"])
                    + float(bracket["right_decay_cosine"])
                ),
                "transition_id": transition_id,
                "parent_interval_id": bracket["interval_id"],
                "left_point_id": bracket["left_point_id"],
                "right_point_id": bracket["right_point_id"],
                "old_bracket_lower": bracket[
                    "left_decay_cosine"
                ],
                "old_bracket_upper": bracket[
                    "right_decay_cosine"
                ],
                "old_bracket_width": bracket["current_width"],
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    return targets


def fixed_values(
    state: dict[str, Any],
    targets: list[dict[str, Any]],
) -> dict[str, dict[int, complex]]:
    return {
        target["order9_node_id"]: {
            inner_order: 0.5
            * (
                state_point_value(
                    state,
                    target["left_point_id"],
                    inner_order,
                )
                + state_point_value(
                    state,
                    target["right_point_id"],
                    inner_order,
                )
            )
            for inner_order in INNER_ORDERS
        }
        for target in targets
    }


def generation_manifest(
    state: dict[str, Any],
    targets: list[dict[str, Any]],
    generation: int,
    formal_digest: str,
    run_signature: str,
) -> dict[str, Any]:
    manifest = {
        "marker": f"{MARKER}_GENERATION_{generation:02d}",
        "revision": f"{REVISION}-generation-{generation:02d}",
        "parent_checkpoint": PARENT_CHECKPOINT,
        "parent_decision": (
            "USE_TIGHTENED_CERTIFICATE_FOR_TARGETED_"
            "TOPOLOGY_BISECTION"
        ),
        "generation": generation,
        "target_node_ids": [
            target["order9_node_id"] for target in targets
        ],
        "outer_nodes": targets,
        "formalization_workbench_start_digest": formal_digest,
        "run_signature": run_signature,
        "state_before_generation_hash": serialized_hash(state),
        "claim_boundary": {
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
            "reason": (
                "Boundary-location refinement alone does not "
                "establish the outer coefficient or local GR."
            ),
        },
    }
    manifest["manifest_hash"] = serialized_hash(manifest)
    return manifest


def generation_paths(generation: int) -> dict[str, Path]:
    root = SOURCE / f"generation_{generation:02d}"
    return {
        "root": root,
        "manifest": root / "manifest.json",
        "nodes": root / "nodes.csv",
        "brackets": root / "brackets.csv",
        "result": root / "result.json",
    }


def ensure_generation_manifest(
    path: Path,
    manifest: dict[str, Any],
) -> None:
    if path.exists():
        existing = json.loads(path.read_text(encoding="utf-8"))
        if existing != manifest:
            raise RuntimeError(
                f"generation manifest changed: {path}"
            )
    else:
        atomic_json(path, manifest)


def configure_node_engine(
    generation: int,
    targets: list[dict[str, Any]],
    manifest_path: Path,
    fixed: dict[str, dict[int, complex]],
) -> None:
    node_ids = tuple(
        target["order9_node_id"] for target in targets
    )
    M5251.SOURCE = SOURCE
    M5251.NODES = NODES
    M5251.MANIFEST = manifest_path
    M5251.MANIFEST_5241 = manifest_path
    M5251.MARKER = f"{MARKER}_G{generation:02d}"
    M5251.REVISION = (
        f"{REVISION}-generation-{generation:02d}"
    )
    M5251.TRANSPORT_CACHE_REVISION = (
        f"{REVISION}-generation-{generation:02d}"
    )
    M5251.CHECKPOINT = CHECKPOINT
    M5251.PARENT_CHECKPOINT = PARENT_CHECKPOINT
    M5251.TARGET_NODE_IDS = node_ids
    M5251.RESULT_5250 = RESULT_5256
    M5251.MAXIMUM_NODE_RUNTIME_SECONDS = (
        M5256.MAXIMUM_NODE_RUNTIME_SECONDS
    )
    M5251.fixed_node_values = lambda: fixed
    M5251.M5243.compare_intervals = (
        M5254.M5253.no_same_coordinate_legacy_comparison
    )


def validate_reusable_node(
    node_id: str,
    manifest_hash: str,
    expected_coordinate: float,
) -> dict[str, Any] | None:
    paths = M5251.node_paths(node_id)
    if not paths["result"].exists():
        return None
    if not paths["manifest"].exists():
        raise RuntimeError(
            f"node result lacks manifest: {node_id}"
        )
    node_manifest = json.loads(
        paths["manifest"].read_text(encoding="utf-8")
    )
    result = json.loads(
        paths["result"].read_text(encoding="utf-8")
    )
    if node_manifest["batch_manifest_hash"] != manifest_hash:
        raise RuntimeError(
            f"batch manifest mismatch for completed node {node_id}"
        )
    if result["manifest_hash"] != node_manifest["manifest_hash"]:
        raise RuntimeError(
            f"node manifest mismatch for completed node {node_id}"
        )
    if not math.isclose(
        float(result["summary"]["decay_cosine"]),
        expected_coordinate,
        rel_tol=0.0,
        abs_tol=2.0e-15,
    ):
        raise RuntimeError(
            f"coordinate mismatch for completed node {node_id}"
        )
    return result


def execute_generation(
    state: dict[str, Any],
    generation: int,
    formal_digest: str,
    run_signature: str,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    targets = generation_targets(state, generation)
    if not targets:
        return state, []
    paths = generation_paths(generation)
    fixed = fixed_values(state, targets)
    manifest = generation_manifest(
        state,
        targets,
        generation,
        formal_digest,
        run_signature,
    )
    ensure_generation_manifest(paths["manifest"], manifest)
    configure_node_engine(
        generation,
        targets,
        paths["manifest"],
        fixed,
    )
    node_rows: list[dict[str, Any]] = []
    results: dict[str, dict[str, Any]] = {}
    for target_index, target in enumerate(targets, start=1):
        node_id = target["order9_node_id"]
        result = validate_reusable_node(
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
        signature = active_signature(result_path)
        values = {
            inner_order: result_value(result, inner_order)
            for inner_order in INNER_ORDERS
        }
        results[node_id] = result
        node_rows.append(
            {
                **target,
                "generation": generation,
                "active_pole_count": len(signature),
                "active_pole_signature": json.dumps(signature),
                "order128_subtracted_real": values[128].real,
                "order128_subtracted_imaginary": values[128].imag,
                "order512_subtracted_real": values[512].real,
                "order512_subtracted_imaginary": values[512].imag,
                "integrity_passed": result["integrity_passed"],
                "acceptance_passed": result["acceptance_passed"],
                "elapsed_seconds": result["elapsed_seconds"],
                "reused_completed_node": reused,
                "result_path": str(result_path),
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
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
            f"5261 generation={generation} "
            f"node={target_index}/{len(targets)} "
            f"id={node_id} reused={reused}",
            flush=True,
        )

    third_signature_count = 0
    bracket_rows: list[dict[str, Any]] = []
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
            update_status = "THIRD_OR_AMBIGUOUS_SIGNATURE"
        elif matches_left:
            update_status = "MIDPOINT_MATCHES_LEFT"
        else:
            update_status = "MIDPOINT_MATCHES_RIGHT"
        if update_status == "THIRD_OR_AMBIGUOUS_SIGNATURE":
            bracket_rows.append(
                {
                    **bracket,
                    "generation": generation,
                    "bisection_node_id": node_row[
                        "order9_node_id"
                    ],
                    "update_status": update_status,
                }
            )
            continue

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
            ANGULAR_JACOBIAN * new_width * envelope
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

    state["third_or_ambiguous_signature_count"] = (
        int(state["third_or_ambiguous_signature_count"])
        + third_signature_count
    )
    if third_signature_count:
        write_csv(paths["nodes"], node_rows)
        write_csv(paths["brackets"], bracket_rows)
        atomic_json(
            paths["result"],
            {
                "marker": manifest["marker"],
                "generation": generation,
                "decision": "HOLD_THIRD_OR_AMBIGUOUS_SIGNATURE",
                "third_or_ambiguous_signature_count": (
                    third_signature_count
                ),
            },
        )
        raise RuntimeError(
            f"generation {generation} produced "
            f"{third_signature_count} third/ambiguous signatures"
        )
    state["completed_generation"] = generation
    state["all_node_ids"].extend(
        row["order9_node_id"] for row in node_rows
    )
    write_csv(paths["nodes"], node_rows)
    write_csv(paths["brackets"], bracket_rows)
    atomic_json(
        paths["result"],
        {
            "marker": manifest["marker"],
            "generation": generation,
            "node_count": len(node_rows),
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
            "decision": (
                "ALL_BOUNDARY_GATES_CLOSED"
                if all(
                    bool(bracket["stopping_gate_passed"])
                    for bracket in state["brackets"].values()
                )
                else "CONTINUE_TARGETED_BISECTION"
            ),
        },
    )
    atomic_json(STATE, state)
    return state, node_rows


def final_bracket_rows(
    state: dict[str, Any],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for transition_id in sorted(state["brackets"]):
        bracket = state["brackets"][transition_id]
        rows.append(
            {
                "transition_id": transition_id,
                "interval_id": bracket["interval_id"],
                "final_generation": bracket["generation"],
                "left_point_id": bracket["left_point_id"],
                "right_point_id": bracket["right_point_id"],
                "left_decay_cosine": bracket[
                    "left_decay_cosine"
                ],
                "right_decay_cosine": bracket[
                    "right_decay_cosine"
                ],
                "left_active_signature": json.dumps(
                    bracket["left_active_signature"]
                ),
                "right_active_signature": json.dumps(
                    bracket["right_active_signature"]
                ),
                "initial_width_generation2": bracket[
                    "initial_width"
                ],
                "final_width": bracket["current_width"],
                "certified_target_width": bracket[
                    "certified_target_width"
                ],
                "certified_half_residue_envelope": bracket[
                    "certified_half_residue_envelope"
                ],
                "equal_boundary_budget": bracket[
                    "equal_boundary_budget"
                ],
                "boundary_location_error_upper": bracket[
                    "boundary_location_error_upper"
                ],
                "completed_bisections_after_generation2": bracket[
                    "completed_bisections_after_generation2"
                ],
                "stopping_gate_passed": bracket[
                    "stopping_gate_passed"
                ],
                "valid_for_boundary_error_claim": True,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    return rows


def execute(dry_run: bool) -> dict[str, Any]:
    required_sources = (
        SCRIPT_5256,
        BRACKETS_5256,
        RESULT_5256,
        TRANSITIONS_5260,
        VALIDATION_5260,
        RESULT_5260,
    )
    missing = [
        str(path) for path in required_sources if not path.exists()
    ]
    if missing:
        raise RuntimeError(f"missing sources: {missing}")
    validation_5260 = read_csv(VALIDATION_5260)
    result_5260 = json.loads(
        RESULT_5260.read_text(encoding="utf-8")
    )
    source_gate = all(
        parse_bool(row["passed"]) for row in validation_5260
    ) and bool(result_5260["validation_passed"])
    if not source_gate:
        raise RuntimeError("checkpoint-5260 source gate is not valid")

    seed_state = initial_state()
    configuration = run_configuration(seed_state)
    run_signature = serialized_hash(configuration)
    dry_result = {
        "marker": f"{MARKER}_DRY_RUN",
        "revision": REVISION,
        "dry_run_passed": source_gate
        and all(
            Path(row["path"]).exists()
            and digest(Path(row["path"])) == row["sha256"]
            for row in configuration["source_files"]
        )
        and sum(
            int(row["required_bisections"])
            for row in configuration["schedule"]
        )
        == 27
        and max(
            int(row["predicted_stopping_generation"])
            for row in configuration["schedule"]
        )
        <= MAXIMUM_GENERATION,
        "source_5260_validation_passed": source_gate,
        "predicted_node_count": sum(
            int(row["required_bisections"])
            for row in configuration["schedule"]
        ),
        "maximum_predicted_stopping_generation": max(
            int(row["predicted_stopping_generation"])
            for row in configuration["schedule"]
        ),
        "run_signature": run_signature,
        "writes_performed": False,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    if dry_run:
        return dry_result
    if not dry_result["dry_run_passed"]:
        raise RuntimeError("5261 dry run failed")

    SOURCE.mkdir(parents=True, exist_ok=True)
    run_signature = ensure_run_configuration(configuration)
    atomic_json(
        DRY_RUN,
        {**dry_result, "writes_performed": True},
    )
    write_csv(SCHEDULE, schedule_rows(seed_state))
    formal_start_rows = (
        read_csv(FORMAL_INVENTORY)
        if FORMAL_INVENTORY.exists()
        else M5251.formal_inventory_rows()
    )
    if not FORMAL_INVENTORY.exists():
        M5251.write_csv(FORMAL_INVENTORY, formal_start_rows)
    formal_digest = M5251.inventory_digest(formal_start_rows)
    if STATE.exists():
        state = json.loads(STATE.read_text(encoding="utf-8"))
    else:
        state = seed_state
        atomic_json(STATE, state)

    all_new_node_rows: list[dict[str, Any]] = []
    while not all(
        bool(bracket["stopping_gate_passed"])
        for bracket in state["brackets"].values()
    ):
        generation = int(state["completed_generation"]) + 1
        if generation > MAXIMUM_GENERATION:
            raise RuntimeError(
                "maximum generation reached before stopping gates"
            )
        state, generation_node_rows = execute_generation(
            state,
            generation,
            formal_digest,
            run_signature,
        )
        all_new_node_rows.extend(generation_node_rows)

    all_node_rows: list[dict[str, str]] = []
    for generation in range(3, int(state["completed_generation"]) + 1):
        path = generation_paths(generation)["nodes"]
        if path.exists():
            all_node_rows.extend(read_csv(path))
    final_rows = final_bracket_rows(state)
    formal_after_rows = M5251.formal_inventory_rows()
    formal_diff_rows = M5251.inventory_diff_rows(
        formal_start_rows,
        formal_after_rows,
    )
    M5251.write_csv(FORMAL_DIFF, formal_diff_rows)
    checks = [
        {
            "check_id": "SOURCE_5260_CERTIFICATE_VALID",
            "passed": source_gate,
            "detail": (
                f"checks={len(validation_5260)}; "
                f"result={result_5260['validation_passed']}"
            ),
        },
        {
            "check_id": "NODE_ACCOUNTING_MATCHES_SCHEDULE",
            "passed": len(all_node_rows)
            == sum(
                int(row["required_bisections"])
                for row in schedule_rows(seed_state)
            )
            == 27
            and len(
                {
                    row["order9_node_id"]
                    for row in all_node_rows
                }
            )
            == len(all_node_rows),
            "detail": f"nodes={len(all_node_rows)}; expected=27",
        },
        {
            "check_id": "ALL_NODE_GATES_PASS",
            "passed": all(
                parse_bool(row["integrity_passed"])
                and parse_bool(row["acceptance_passed"])
                for row in all_node_rows
            ),
            "detail": (
                "passed="
                f"{sum(parse_bool(row['integrity_passed']) and parse_bool(row['acceptance_passed']) for row in all_node_rows)}"
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
                "maximum_width_ratio="
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
                "boundary location only; coefficient, local-GR, "
                "and full-MTS remain false"
            ),
        },
    ]
    passed = all(bool(row["passed"]) for row in checks)
    result = {
        "marker": MARKER,
        "revision": REVISION,
        "validation_passed": passed,
        "node_count": len(all_node_rows),
        "completed_generation": state["completed_generation"],
        "transition_count": len(final_rows),
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
            "ADOPT_CERTIFIED_TARGETED_BOUNDARY_REFINEMENT__"
            "HANDOFF_TO_OUTER_COEFFICIENT_REASSEMBLY"
            if passed
            else "HOLD_TARGETED_BOUNDARY_REFINEMENT"
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
        raise RuntimeError(f"5261 validation failed: {failed}")
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
