from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import math
import os
import sys
from pathlib import Path
from typing import Any


WORKBENCH = Path(__file__).resolve().parents[1]
SCRIPTS = WORKBENCH / "scripts"
FUNCTIONAL_RG = WORKBENCH / "source-intake" / "functional_rg"
SOURCE_5256 = FUNCTIONAL_RG / "5256"
SOURCE_5258 = FUNCTIONAL_RG / "5258"
SOURCE = FUNCTIONAL_RG / "5260"
SHARDS = SOURCE / "shards"

SCRIPT_5258 = (
    SCRIPTS / "Y5_R2FR_5258_interval_residue_enclosure_pilot.py"
)
PARENT_BOX_ROWS = SOURCE_5258 / "interval_residue_boxes.csv"
PARENT_TRANSITION_ROWS = (
    SOURCE_5258 / "interval_transition_envelopes.csv"
)
PARENT_VALIDATION = SOURCE_5258 / "interval_residue_validation.csv"
PARENT_RESULT = SOURCE_5258 / "interval_residue_result.json"
BOUNDARY_BUDGET = SOURCE_5256 / "boundary_location_error_budget.csv"

RUN_CONFIG = SOURCE / "microbox_run_config.json"
STATUS = SOURCE / "status.json"
BOX_ROWS = SOURCE / "tightened_interval_residue_boxes.csv"
TRANSITION_ROWS = SOURCE / "tightened_transition_envelopes.csv"
VALIDATION = SOURCE / "microbox_residue_validation.csv"
RESULT = SOURCE / "microbox_residue_result.json"

DEFAULT_PIECES_PER_PARENT = 16
DEFAULT_BATCH_SIZE = 8
DEFAULT_CAUCHY_NODES = 4
DEFAULT_PHASE_ARCS = 8
TARGET_CERTIFIED_TO_SAMPLED_RATIO = 4.0
ANGULAR_JACOBIAN = 0.25
HALF_RESIDUE_COEFFICIENT = 0.016
EXPECTED_TRANSITIONS = {
    "I01_T00",
    "I01_T01",
    "I06_T00",
    "I06_T01",
}
EXPECTED_EPSILONS = {"E020", "E040"}


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    sys.modules[name] = module
    specification.loader.exec_module(module)
    return module


M5258 = load_module("mts_5258_for_5260", SCRIPT_5258)


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


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        while chunk := handle.read(1024 * 1024):
            digest.update(chunk)
    return digest.hexdigest()


def is_power_of_two(value: int) -> bool:
    return value > 0 and value & (value - 1) == 0


def required_bisections(current_width: float, target_width: float) -> int:
    if target_width <= 0.0:
        raise ValueError("target width must be positive")
    if current_width <= target_width:
        return 0
    return math.ceil(math.log2(current_width / target_width))


def run_configuration(
    pieces_per_parent: int,
    batch_size: int,
    cauchy_nodes: int,
    phase_arcs: int,
) -> dict[str, Any]:
    return {
        "marker": "MTS_5260_MICROBOX_RUN_CONFIGURATION",
        "revision": "adaptive-microbox-residue-tightening-v1",
        "source_box_sha256": sha256(PARENT_BOX_ROWS),
        "pieces_per_parent": pieces_per_parent,
        "batch_size": batch_size,
        "cauchy_nodes": cauchy_nodes,
        "phase_arcs": phase_arcs,
    }


def ensure_configuration(configuration: dict[str, Any]) -> None:
    if RUN_CONFIG.exists():
        existing = json.loads(RUN_CONFIG.read_text(encoding="utf-8"))
        if existing != configuration:
            raise RuntimeError(
                "existing checkpoint-5260 shards use a different "
                "configuration; archive the 5260 source directory before "
                "starting a changed run"
            )
        return
    atomic_json(RUN_CONFIG, configuration)


def shard_path(
    transition_id: str,
    epsilon_id: str,
    batch_index: int,
) -> Path:
    return (
        SHARDS
        / (
            f"{transition_id}__{epsilon_id}"
            f"__batch_{batch_index:04d}.csv"
        )
    )


def parent_key(row: dict[str, Any]) -> tuple[str, str, str]:
    return (
        str(row["transition_id"]),
        str(row["epsilon_id"]),
        str(row["box_index"]),
    )


def validate_existing_shard(
    path: Path,
    expected_parents: list[dict[str, str]],
    pieces_per_parent: int,
    run_signature: str,
) -> list[dict[str, str]]:
    rows = read_csv(path)
    expected_count = len(expected_parents) * pieces_per_parent
    if len(rows) != expected_count:
        raise RuntimeError(
            f"incomplete existing shard {path}: "
            f"rows={len(rows)} expected={expected_count}"
        )
    if any(row.get("run_signature") != run_signature for row in rows):
        raise RuntimeError(f"run signature mismatch in {path}")
    expected_keys = {parent_key(row) for row in expected_parents}
    observed_keys = {
        (
            row["transition_id"],
            row["epsilon_id"],
            row["parent_box_index"],
        )
        for row in rows
    }
    if observed_keys != expected_keys:
        raise RuntimeError(f"parent coverage mismatch in {path}")
    return rows


def refine_parent(
    parent: dict[str, str],
    endpoint_row: dict[str, str],
    orientation_row: dict[str, str],
    pieces_per_parent: int,
    cauchy_nodes: int,
    phase_arcs: int,
    run_signature: str,
) -> list[dict[str, Any]]:
    transition_id = parent["transition_id"]
    parent_lower = float(parent["x_lower"])
    parent_upper = float(parent["x_upper"])
    parent_width = parent_upper - parent_lower
    micro_depth = int(math.log2(pieces_per_parent))
    rows: list[dict[str, Any]] = []
    for micro_index in range(pieces_per_parent):
        micro_lower = (
            parent_lower
            + parent_width * micro_index / pieces_per_parent
        )
        micro_upper = (
            parent_lower
            + parent_width * (micro_index + 1) / pieces_per_parent
        )
        microbox = M5258.interval_box(
            endpoint_row,
            orientation_row,
            transition_id,
            f"{parent['box_index']}m{micro_index:02d}",
            micro_lower,
            micro_upper,
            cauchy_nodes,
            phase_arcs,
            parent["base_box_index"],
            int(parent["x_refinement_depth"]) + micro_depth,
            (
                f"{parent['x_refinement_path']}"
                f"M{micro_index:02d}"
            ),
        )
        rows.append(
            {
                **microbox,
                "parent_box_index": parent["box_index"],
                "parent_x_lower": parent_lower,
                "parent_x_upper": parent_upper,
                "parent_box_width": parent_width,
                "parent_residue_abs_upper_5258": float(
                    parent["residue_abs_upper"]
                ),
                "microbox_index": micro_index,
                "pieces_per_parent": pieces_per_parent,
                "run_signature": run_signature,
            }
        )
    return rows


def compute_shards(
    parent_rows: list[dict[str, str]],
    pieces_per_parent: int,
    batch_size: int,
    cauchy_nodes: int,
    phase_arcs: int,
    run_signature: str,
) -> list[Path]:
    denominator_lookup = {
        (row["node_id"], row["epsilon_id"]): row
        for row in read_csv(M5258.DENOMINATOR_ROWS)
    }
    orientation_lookup = {
        (row["node_id"], row["epsilon_id"]): row
        for row in read_csv(M5258.ORIENTATION_ROWS)
    }
    groups = sorted(
        {
            (row["transition_id"], row["epsilon_id"])
            for row in parent_rows
        }
    )
    total_batches = sum(
        math.ceil(
            len(
                [
                    row
                    for row in parent_rows
                    if (
                        row["transition_id"],
                        row["epsilon_id"],
                    )
                    == group
                ]
            )
            / batch_size
        )
        for group in groups
    )
    completed_batches = 0
    expected_shards: list[Path] = []
    for transition_id, epsilon_id in groups:
        group_parents = [
            row
            for row in parent_rows
            if row["transition_id"] == transition_id
            and row["epsilon_id"] == epsilon_id
        ]
        endpoint_id = M5258.ACTIVE_ENDPOINTS[transition_id]
        endpoint_row = denominator_lookup[(endpoint_id, epsilon_id)]
        orientation_row = orientation_lookup[(endpoint_id, epsilon_id)]
        for batch_index, offset in enumerate(
            range(0, len(group_parents), batch_size)
        ):
            batch_parents = group_parents[offset : offset + batch_size]
            path = shard_path(
                transition_id,
                epsilon_id,
                batch_index,
            )
            expected_shards.append(path)
            if path.exists():
                validate_existing_shard(
                    path,
                    batch_parents,
                    pieces_per_parent,
                    run_signature,
                )
            else:
                shard_rows: list[dict[str, Any]] = []
                for parent in batch_parents:
                    shard_rows.extend(
                        refine_parent(
                            parent,
                            endpoint_row,
                            orientation_row,
                            pieces_per_parent,
                            cauchy_nodes,
                            phase_arcs,
                            run_signature,
                        )
                    )
                write_csv(path, shard_rows)
            completed_batches += 1
            status = {
                "marker": "MTS_5260_MICROBOX_RUN_STATUS",
                "state": (
                    "running"
                    if completed_batches < total_batches
                    else "aggregating"
                ),
                "completed_batches": completed_batches,
                "total_batches": total_batches,
                "completed_fraction": (
                    completed_batches / total_batches
                ),
                "last_transition_id": transition_id,
                "last_epsilon_id": epsilon_id,
                "last_batch_index": batch_index,
                "run_signature": run_signature,
            }
            atomic_json(STATUS, status)
            print(
                "5260 progress "
                f"{completed_batches}/{total_batches} "
                f"{transition_id} {epsilon_id} "
                f"batch={batch_index}",
                flush=True,
            )
    return expected_shards


def coverage_audit(
    parent_rows: list[dict[str, str]],
    refined_rows: list[dict[str, str]],
    pieces_per_parent: int,
) -> dict[str, Any]:
    refined_lookup: dict[
        tuple[str, str, str],
        list[dict[str, str]],
    ] = {}
    for row in refined_rows:
        key = (
            row["transition_id"],
            row["epsilon_id"],
            row["parent_box_index"],
        )
        refined_lookup.setdefault(key, []).append(row)
    maximum_endpoint_error = 0.0
    maximum_gap = 0.0
    maximum_width_error = 0.0
    maximum_child_to_parent_upper_ratio = 0.0
    complete = True
    for parent in parent_rows:
        key = parent_key(parent)
        children = sorted(
            refined_lookup.get(key, []),
            key=lambda row: float(row["x_lower"]),
        )
        if len(children) != pieces_per_parent:
            complete = False
            continue
        parent_lower = float(parent["x_lower"])
        parent_upper = float(parent["x_upper"])
        maximum_endpoint_error = max(
            maximum_endpoint_error,
            abs(float(children[0]["x_lower"]) - parent_lower),
            abs(float(children[-1]["x_upper"]) - parent_upper),
        )
        for left, right in zip(children, children[1:]):
            maximum_gap = max(
                maximum_gap,
                abs(
                    float(left["x_upper"])
                    - float(right["x_lower"])
                ),
            )
        summed_width = sum(
            float(child["box_width"]) for child in children
        )
        maximum_width_error = max(
            maximum_width_error,
            abs(summed_width - (parent_upper - parent_lower)),
        )
        maximum_child_to_parent_upper_ratio = max(
            maximum_child_to_parent_upper_ratio,
            max(
                float(child["residue_abs_upper"])
                for child in children
            )
            / float(parent["residue_abs_upper"]),
        )
    tolerance = 5.0e-13
    return {
        "parent_count": len(parent_rows),
        "refined_parent_count": len(refined_lookup),
        "coverage_complete": complete
        and len(refined_lookup) == len(parent_rows)
        and maximum_endpoint_error <= tolerance
        and maximum_gap <= tolerance
        and maximum_width_error <= tolerance,
        "maximum_endpoint_error": maximum_endpoint_error,
        "maximum_gap": maximum_gap,
        "maximum_width_error": maximum_width_error,
        "maximum_child_to_parent_upper_ratio": (
            maximum_child_to_parent_upper_ratio
        ),
    }


def transition_envelopes(
    refined_rows: list[dict[str, str]],
    parent_transitions: list[dict[str, str]],
    budget_rows: list[dict[str, str]],
    pieces_per_parent: int,
) -> list[dict[str, Any]]:
    parent_lookup = {
        row["transition_id"]: row for row in parent_transitions
    }
    budget_lookup = {
        row["transition_id"]: row for row in budget_rows
    }
    rows: list[dict[str, Any]] = []
    for transition_id in sorted(EXPECTED_TRANSITIONS):
        selected = [
            row
            for row in refined_rows
            if row["transition_id"] == transition_id
        ]
        maxima = {
            epsilon_id: max(
                float(row["residue_abs_upper"])
                for row in selected
                if row["epsilon_id"] == epsilon_id
            )
            for epsilon_id in EXPECTED_EPSILONS
        }
        envelope = HALF_RESIDUE_COEFFICIENT * (
            2.0 * maxima["E020"] + maxima["E040"]
        )
        parent = parent_lookup[transition_id]
        parent_envelope = float(
            parent["half_residue_triangle_envelope"]
        )
        bracket_width = float(parent["bracket_width"])
        boundary_error = (
            ANGULAR_JACOBIAN * bracket_width * envelope
        )
        budget = float(
            budget_lookup[transition_id]["equal_boundary_budget"]
        )
        sampled_envelope = float(
            budget_lookup[transition_id][
                "sampled_half_residue_triangle_envelope"
            ]
        )
        target_width = budget / (
            ANGULAR_JACOBIAN * envelope
        )
        rows.append(
            {
                "transition_id": transition_id,
                "active_endpoint_id": parent["active_endpoint_id"],
                "pieces_per_parent": pieces_per_parent,
                "microbox_count": len(selected),
                "R20_abs_upper": maxima["E020"],
                "R40_abs_upper": maxima["E040"],
                "half_residue_triangle_envelope": envelope,
                "parent_half_residue_triangle_envelope_5258": (
                    parent_envelope
                ),
                "envelope_reduction_factor": (
                    parent_envelope / envelope
                ),
                "sampled_half_residue_envelope_5256": (
                    sampled_envelope
                ),
                "certified_to_sampled_envelope_ratio": (
                    envelope / sampled_envelope
                ),
                "bracket_width": bracket_width,
                "boundary_location_error_upper": boundary_error,
                "equal_boundary_budget": budget,
                "certified_error_to_budget_ratio": (
                    boundary_error / budget
                ),
                "certified_target_width": target_width,
                "additional_binary_bisections_if_envelope_fixed": (
                    required_bisections(
                        bracket_width,
                        target_width,
                    )
                ),
                "boundary_budget_met": boundary_error <= budget,
                "continuous_envelope_certified": True,
                "valid_for_boundary_error_claim": True,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    for row in rows:
        row["raw_R20_abs_upper"] = row["R20_abs_upper"]
        row["raw_R40_abs_upper"] = row["R40_abs_upper"]
        row["raw_half_residue_triangle_envelope"] = row[
            "half_residue_triangle_envelope"
        ]
        row["reflection_union_bound_applied"] = False
    reflected_pair = [
        next(
            row
            for row in rows
            if row["transition_id"] == transition_id
        )
        for transition_id in ("I01_T00", "I06_T01")
    ]
    shared_r20 = max(
        float(row["R20_abs_upper"]) for row in reflected_pair
    )
    shared_r40 = max(
        float(row["R40_abs_upper"]) for row in reflected_pair
    )
    shared_envelope = HALF_RESIDUE_COEFFICIENT * (
        2.0 * shared_r20 + shared_r40
    )
    for row in reflected_pair:
        parent_envelope = float(
            row["parent_half_residue_triangle_envelope_5258"]
        )
        bracket_width = float(row["bracket_width"])
        budget = float(row["equal_boundary_budget"])
        sampled_envelope = float(
            row["sampled_half_residue_envelope_5256"]
        )
        boundary_error = (
            ANGULAR_JACOBIAN * bracket_width * shared_envelope
        )
        target_width = budget / (
            ANGULAR_JACOBIAN * shared_envelope
        )
        row.update(
            {
                "R20_abs_upper": shared_r20,
                "R40_abs_upper": shared_r40,
                "half_residue_triangle_envelope": shared_envelope,
                "envelope_reduction_factor": (
                    parent_envelope / shared_envelope
                ),
                "certified_to_sampled_envelope_ratio": (
                    shared_envelope / sampled_envelope
                ),
                "boundary_location_error_upper": boundary_error,
                "certified_error_to_budget_ratio": (
                    boundary_error / budget
                ),
                "certified_target_width": target_width,
                "additional_binary_bisections_if_envelope_fixed": (
                    required_bisections(
                        bracket_width,
                        target_width,
                    )
                ),
                "boundary_budget_met": boundary_error <= budget,
                "reflection_union_bound_applied": True,
            }
        )
    return rows


def execute(
    pieces_per_parent: int,
    batch_size: int,
    cauchy_nodes: int,
    phase_arcs: int,
    dry_run: bool,
) -> dict[str, Any]:
    if not is_power_of_two(pieces_per_parent):
        raise ValueError("pieces per parent must be a power of two")
    if batch_size < 1:
        raise ValueError("batch size must be positive")
    if cauchy_nodes < 2 or phase_arcs < 4:
        raise ValueError("Cauchy nodes and phase arcs are too small")
    required_sources = (
        SCRIPT_5258,
        PARENT_BOX_ROWS,
        PARENT_TRANSITION_ROWS,
        PARENT_VALIDATION,
        PARENT_RESULT,
        BOUNDARY_BUDGET,
        M5258.DENOMINATOR_ROWS,
        M5258.ORIENTATION_ROWS,
    )
    missing = [
        str(path) for path in required_sources if not path.exists()
    ]
    if missing:
        raise RuntimeError(f"missing sources: {missing}")

    parent_rows = read_csv(PARENT_BOX_ROWS)
    parent_transitions = read_csv(PARENT_TRANSITION_ROWS)
    parent_validation = read_csv(PARENT_VALIDATION)
    parent_result = json.loads(
        PARENT_RESULT.read_text(encoding="utf-8")
    )
    budget_rows = read_csv(BOUNDARY_BUDGET)
    configuration = run_configuration(
        pieces_per_parent,
        batch_size,
        cauchy_nodes,
        phase_arcs,
    )
    run_signature = hashlib.sha256(
        json.dumps(configuration, sort_keys=True).encode("utf-8")
    ).hexdigest()
    estimated_microboxes = len(parent_rows) * pieces_per_parent
    if dry_run:
        return {
            "marker": "MTS_5260_MICROBOX_DRY_RUN",
            "source_parent_box_count": len(parent_rows),
            "estimated_microbox_count": estimated_microboxes,
            "pieces_per_parent": pieces_per_parent,
            "batch_size": batch_size,
            "cauchy_nodes": cauchy_nodes,
            "phase_arcs": phase_arcs,
            "source_5258_validation_passed": all(
                parse_bool(row["passed"])
                for row in parent_validation
            )
            and bool(parent_result["validation_passed"]),
            "run_signature": run_signature,
            "writes_performed": False,
        }

    ensure_configuration(configuration)
    expected_shards = compute_shards(
        parent_rows,
        pieces_per_parent,
        batch_size,
        cauchy_nodes,
        phase_arcs,
        run_signature,
    )
    refined_rows: list[dict[str, str]] = []
    for path in expected_shards:
        refined_rows.extend(read_csv(path))
    coverage = coverage_audit(
        parent_rows,
        refined_rows,
        pieces_per_parent,
    )
    transitions = transition_envelopes(
        refined_rows,
        parent_transitions,
        budget_rows,
        pieces_per_parent,
    )
    reflected_left = next(
        row
        for row in transitions
        if row["transition_id"] == "I01_T00"
    )
    reflected_right = next(
        row
        for row in transitions
        if row["transition_id"] == "I06_T01"
    )
    raw_reflection_relative_error = abs(
        float(
            reflected_left[
                "raw_half_residue_triangle_envelope"
            ]
        )
        - float(
            reflected_right[
                "raw_half_residue_triangle_envelope"
            ]
        )
    ) / max(
        abs(
            float(
                reflected_left[
                    "raw_half_residue_triangle_envelope"
                ]
            )
        ),
        1.0,
    )
    reflection_relative_error = abs(
        float(
            reflected_left["half_residue_triangle_envelope"]
        )
        - float(
            reflected_right["half_residue_triangle_envelope"]
        )
    ) / max(
        abs(
            float(
                reflected_left[
                    "half_residue_triangle_envelope"
                ]
            )
        ),
        1.0,
    )
    maximum_certified_to_sampled = max(
        float(row["certified_to_sampled_envelope_ratio"])
        for row in transitions
    )
    checks = [
        {
            "check_id": "SOURCE_5258_CERTIFICATE_VALID",
            "passed": all(
                parse_bool(row["passed"])
                for row in parent_validation
            )
            and bool(parent_result["validation_passed"])
            and bool(
                parent_result[
                    "continuous_residue_envelope_complete"
                ]
            ),
            "detail": (
                f"source_checks={len(parent_validation)}; "
                f"source_boxes={len(parent_rows)}"
            ),
        },
        {
            "check_id": "MICROBOX_PARTITION_COVERS_EVERY_PARENT",
            "passed": bool(coverage["coverage_complete"]),
            "detail": (
                f"parents={coverage['parent_count']}; "
                f"refined={coverage['refined_parent_count']}; "
                f"endpoint_error={coverage['maximum_endpoint_error']}; "
                f"gap={coverage['maximum_gap']}; "
                f"width_error={coverage['maximum_width_error']}"
            ),
        },
        {
            "check_id": "ALL_MICROBOX_INTERVALS_VALID",
            "passed": len(refined_rows) == estimated_microboxes
            and all(
                parse_bool(row["interval_arithmetic_complete"])
                and parse_bool(
                    row[
                        "analytic_disk_root_separation_interval_proved"
                    ]
                )
                and float(
                    row["minimum_interval_denominator_lower"]
                )
                > 0.0
                and math.isfinite(
                    float(row["residue_abs_upper"])
                )
                for row in refined_rows
            ),
            "detail": (
                f"rows={len(refined_rows)}; "
                f"expected={estimated_microboxes}"
            ),
        },
        {
            "check_id": "ENCLOSURE_TIGHTENING_MONOTONE",
            "passed": all(
                float(row["envelope_reduction_factor"]) >= 1.0
                for row in transitions
            )
            and float(
                coverage["maximum_child_to_parent_upper_ratio"]
            )
            <= 1.000001,
            "detail": (
                "minimum_transition_reduction="
                f"{min(float(row['envelope_reduction_factor']) for row in transitions)}; "
                "maximum_child_parent_ratio="
                f"{coverage['maximum_child_to_parent_upper_ratio']}"
            ),
        },
        {
            "check_id": "CERTIFIED_TO_SAMPLED_TARGET_MET",
            "passed": maximum_certified_to_sampled
            <= TARGET_CERTIFIED_TO_SAMPLED_RATIO,
            "detail": (
                f"maximum_ratio={maximum_certified_to_sampled}; "
                f"target={TARGET_CERTIFIED_TO_SAMPLED_RATIO}"
            ),
        },
        {
            "check_id": "REFLECTED_ENVELOPES_USE_SAFE_UNION_BOUND",
            "passed": reflection_relative_error <= 1.0e-15
            and all(
                bool(row["reflection_union_bound_applied"])
                and float(
                    row["half_residue_triangle_envelope"]
                )
                >= float(
                    row[
                        "raw_half_residue_triangle_envelope"
                    ]
                )
                for row in (reflected_left, reflected_right)
            ),
            "detail": (
                f"union_relative_error={reflection_relative_error}; "
                "raw_relative_error="
                f"{raw_reflection_relative_error}"
            ),
        },
        {
            "check_id": "CLAIM_SCOPE_REMAINS_BOUNDARY_ONLY",
            "passed": all(
                bool(row["valid_for_boundary_error_claim"])
                and not bool(row["valid_for_numeric_UV_claim"])
                and not bool(row["valid_for_local_GR_claim"])
                and not bool(row["valid_for_full_MTS_claim"])
                for row in transitions
            ),
            "detail": (
                "continuous boundary envelope only; "
                "UV, local-GR, and full-MTS remain false"
            ),
        },
    ]
    passed = all(bool(row["passed"]) for row in checks)
    result = {
        "marker": "MTS_5260_ADAPTIVE_MICROBOX_RESIDUE_TIGHTENING",
        "revision": "adaptive-microbox-residue-tightening-v1",
        "validation_passed": passed,
        "source_parent_box_count": len(parent_rows),
        "microbox_count": len(refined_rows),
        "pieces_per_parent": pieces_per_parent,
        "maximum_child_to_parent_upper_ratio": coverage[
            "maximum_child_to_parent_upper_ratio"
        ],
        "minimum_transition_envelope_reduction_factor": min(
            float(row["envelope_reduction_factor"])
            for row in transitions
        ),
        "maximum_transition_envelope_reduction_factor": max(
            float(row["envelope_reduction_factor"])
            for row in transitions
        ),
        "maximum_certified_to_sampled_envelope_ratio": (
            maximum_certified_to_sampled
        ),
        "minimum_certified_error_to_budget_ratio": min(
            float(row["certified_error_to_budget_ratio"])
            for row in transitions
        ),
        "maximum_certified_error_to_budget_ratio": max(
            float(row["certified_error_to_budget_ratio"])
            for row in transitions
        ),
        "maximum_additional_bisections_if_envelope_fixed": max(
            int(
                row[
                    "additional_binary_bisections_if_envelope_fixed"
                ]
            )
            for row in transitions
        ),
        "reflection_relative_error": reflection_relative_error,
        "raw_reflection_relative_error": (
            raw_reflection_relative_error
        ),
        "continuous_residue_envelope_complete": passed,
        "all_boundary_budgets_met": all(
            bool(row["boundary_budget_met"]) for row in transitions
        ),
        "decision": (
            "USE_TIGHTENED_CERTIFICATE_FOR_TARGETED_"
            "TOPOLOGY_BISECTION"
            if passed
            else "HOLD_AND_REPAIR_MICROBOX_TIGHTENING"
        ),
        "valid_for_boundary_error_claim": passed,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    write_csv(BOX_ROWS, refined_rows)
    write_csv(TRANSITION_ROWS, transitions)
    write_csv(VALIDATION, checks)
    atomic_json(RESULT, result)
    atomic_json(
        STATUS,
        {
            "marker": "MTS_5260_MICROBOX_RUN_STATUS",
            "state": "complete" if passed else "validation_failed",
            "completed_batches": len(expected_shards),
            "total_batches": len(expected_shards),
            "completed_fraction": 1.0,
            "run_signature": run_signature,
            "validation_passed": passed,
        },
    )
    if not passed:
        failed = [
            row["check_id"] for row in checks if not row["passed"]
        ]
        raise RuntimeError(f"5260 validation failed: {failed}")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--pieces-per-parent",
        type=int,
        default=DEFAULT_PIECES_PER_PARENT,
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=DEFAULT_BATCH_SIZE,
    )
    parser.add_argument(
        "--cauchy-nodes",
        type=int,
        default=DEFAULT_CAUCHY_NODES,
    )
    parser.add_argument(
        "--phase-arcs",
        type=int,
        default=DEFAULT_PHASE_ARCS,
    )
    parser.add_argument("--dry-run", action="store_true")
    arguments = parser.parse_args()
    print(
        json.dumps(
            execute(
                arguments.pieces_per_parent,
                arguments.batch_size,
                arguments.cauchy_nodes,
                arguments.phase_arcs,
                arguments.dry_run,
            ),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
