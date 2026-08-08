from __future__ import annotations

import argparse
import csv
import ctypes
import hashlib
import importlib.util
import json
import math
import os
import sys
import time
from pathlib import Path
from typing import Any


for thread_variable in (
    "OMP_NUM_THREADS",
    "OPENBLAS_NUM_THREADS",
    "MKL_NUM_THREADS",
    "NUMEXPR_NUM_THREADS",
    "VECLIB_MAXIMUM_THREADS",
    "BLIS_NUM_THREADS",
):
    os.environ[thread_variable] = "1"
os.environ["PYTHONNOUSERSITE"] = "1"

import numpy as np


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SCRIPTS = POST / "scripts"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
SOURCE = FUNCTIONAL_RG / "5271"
RESIDUALS = POST / "source-intake" / "mts_residuals"

SCRIPT_5270 = (
    SCRIPTS
    / "Y5_R2FR_5270_shared_angular_root_margin_boundary_localizer.py"
)
RESULT_5270 = (
    FUNCTIONAL_RG
    / "5270"
    / "shared_angular_boundary_localization_result.json"
)
VALIDATION_5270 = (
    FUNCTIONAL_RG
    / "5270"
    / "shared_angular_boundary_localization_validation.csv"
)
MERGED_5270 = (
    FUNCTIONAL_RG / "5270" / "merged_shared_angular_boundaries.csv"
)

DRY_RUN = SOURCE / "soft_energy_surface_oracle_dry_run.json"
ENERGY_NODES = SOURCE / "soft_energy_surface_nodes.csv"
FUNCTION_SUMMARY = SOURCE / "soft_energy_root_margin_functions.csv"
RAW_BOUNDARIES = SOURCE / "soft_energy_raw_boundaries.csv"
MERGED_BOUNDARIES = SOURCE / "soft_energy_merged_boundaries.csv"
PANELS = SOURCE / "soft_energy_topology_uniform_panels.csv"
SLICE_SUMMARY = SOURCE / "soft_energy_boundary_slice_summary.csv"
BRANCH_LINKS = SOURCE / "soft_energy_boundary_branch_links.csv"
TOPOLOGY_EVENTS = SOURCE / "soft_energy_surface_topology_events.csv"
WITNESS_REPRODUCTION = SOURCE / "5270_witness_reproduction.csv"
RESULT = SOURCE / "soft_energy_boundary_surface_oracle_result.json"
VALIDATION = SOURCE / "soft_energy_boundary_surface_oracle_validation.csv"
RESIDUAL_VALIDATION = (
    RESIDUALS / "P8_Y5_BRR545_5271_VALIDATION.csv"
)
STATUS = SOURCE / "status.json"
DOCUMENT = (
    POST
    / "5271-Y5-R2FR-soft-energy-angular-boundary-surface-oracle.md"
)

CHECKPOINT = 5271
PARENT_CHECKPOINT = 5270
MARKER = "MTS_5271_SOFT_ENERGY_ANGULAR_BOUNDARY_SURFACE_ORACLE"
REVISION = "soft-energy-angular-boundary-surface-oracle-v1"
CHEBYSHEV_NODE_COUNT = 25
ANGULAR_SCAN_POINTS = 1025
WITNESS_REPRODUCTION_TOLERANCE = 1.0e-10
ENDPOINT_EVENT_DISTANCE = 5.0e-2
CLAIM_FIELDS = (
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


M5270 = load_module("mts_5270_for_5271", SCRIPT_5270)
M5269 = M5270.M5269
M5267 = M5270.M5267


def set_below_normal_priority() -> None:
    if os.name != "nt":
        return
    handle = ctypes.windll.kernel32.GetCurrentProcess()
    ctypes.windll.kernel32.SetPriorityClass(handle, 0x00004000)


def json_default(value: Any) -> Any:
    if isinstance(value, complex):
        return {"real": float(value.real), "imaginary": float(value.imag)}
    if isinstance(value, np.generic):
        return value.item()
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, Path):
        return str(value)
    raise TypeError(f"cannot serialize {type(value)!r}")


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(
            value,
            indent=2,
            sort_keys=True,
            default=json_default,
        )
        + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise RuntimeError(f"refusing to write empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    os.replace(temporary, path)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def serialized_hash(value: Any) -> str:
    return hashlib.sha256(
        json.dumps(
            value,
            sort_keys=True,
            separators=(",", ":"),
            default=json_default,
        ).encode("utf-8")
    ).hexdigest()


def formal_inventory_digest() -> str:
    rows = [
        {
            "relative_path": str(path.relative_to(FORMAL)),
            "size": str(path.stat().st_size),
            "sha256": digest(path),
        }
        for path in sorted(
            (item for item in FORMAL.rglob("*") if item.is_file()),
            key=lambda item: str(item).lower(),
        )
    ]
    return serialized_hash(rows)


def source_rows() -> list[dict[str, str]]:
    paths = (
        Path(__file__).resolve(),
        SCRIPT_5270,
        RESULT_5270,
        VALIDATION_5270,
        MERGED_5270,
    )
    return [
        {"path": str(path), "sha256": digest(path)}
        for path in paths
    ]


def energy_nodes() -> tuple[float, ...]:
    lower = float(M5267.ENERGY_MINIMUM)
    upper = float(M5267.ENERGY_MAXIMUM)
    chebyshev = [
        lower
        + (upper - lower)
        * 0.5
        * (
            1.0
            - math.cos(
                math.pi
                * index
                / (CHEBYSHEV_NODE_COUNT - 1)
            )
        )
        for index in range(CHEBYSHEV_NODE_COUNT)
    ]
    return tuple(
        sorted(
            {
                *chebyshev,
                *(
                    float(value)
                    for value in M5269.ENERGY_WITNESSES
                ),
            }
        )
    )


def energy_node_rows(nodes: tuple[float, ...]) -> list[dict[str, Any]]:
    witnesses = {
        float(value) for value in M5269.ENERGY_WITNESSES
    }
    return [
        {
            "energy_index": index,
            "soft_energy": value,
            "is_5270_witness": value in witnesses,
            "valid_for_full_phase_space_coefficient": False,
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
        }
        for index, value in enumerate(nodes)
    ]


def slice_summary_rows(
    merged_rows: list[dict[str, Any]],
    panel_rows: list[dict[str, Any]],
    nodes: tuple[float, ...],
    soft_nodes: tuple[float, ...],
    decay_nodes: tuple[float, ...],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for energy in nodes:
        for direction, fixed_values in (
            ("soft_cosine", decay_nodes),
            ("decay_cosine", soft_nodes),
        ):
            for fixed in fixed_values:
                boundaries = [
                    row
                    for row in merged_rows
                    if row["direction"] == direction
                    and float(row["energy_witness"]) == energy
                    and float(row["fixed_coordinate"]) == fixed
                ]
                panels = [
                    row
                    for row in panel_rows
                    if row["direction"] == direction
                    and float(row["energy_witness"]) == energy
                    and float(row["fixed_coordinate"]) == fixed
                ]
                rows.append(
                    {
                        "direction": direction,
                        "soft_energy": energy,
                        "fixed_coordinate": fixed,
                        "boundary_count": len(boundaries),
                        "panel_count": len(panels),
                        "minimum_boundary_coordinate": min(
                            (
                                float(row["boundary_coordinate"])
                                for row in boundaries
                            ),
                            default="",
                        ),
                        "maximum_boundary_coordinate": max(
                            (
                                float(row["boundary_coordinate"])
                                for row in boundaries
                            ),
                            default="",
                        ),
                        "panel_coverage_residual": abs(
                            sum(
                                float(row["panel_width"])
                                for row in panels
                            )
                            - 2.0 * M5270.ANGULAR_LIMIT
                        ),
                        "valid_for_full_phase_space_coefficient": False,
                        "valid_for_numeric_UV_claim": False,
                        "valid_for_local_GR_claim": False,
                        "valid_for_full_MTS_claim": False,
                    }
                )
    return rows


def greedy_links(
    left_rows: list[dict[str, Any]],
    right_rows: list[dict[str, Any]],
) -> tuple[
    list[tuple[dict[str, Any], dict[str, Any]]],
    list[dict[str, Any]],
    list[dict[str, Any]],
]:
    pairs = sorted(
        (
            (
                abs(
                    float(left["boundary_coordinate"])
                    - float(right["boundary_coordinate"])
                ),
                left_index,
                right_index,
            )
            for left_index, left in enumerate(left_rows)
            for right_index, right in enumerate(right_rows)
        ),
        key=lambda row: row[0],
    )
    used_left: set[int] = set()
    used_right: set[int] = set()
    links: list[tuple[dict[str, Any], dict[str, Any]]] = []
    for _, left_index, right_index in pairs:
        if left_index in used_left or right_index in used_right:
            continue
        used_left.add(left_index)
        used_right.add(right_index)
        links.append(
            (left_rows[left_index], right_rows[right_index])
        )
    unmatched_left = [
        row
        for index, row in enumerate(left_rows)
        if index not in used_left
    ]
    unmatched_right = [
        row
        for index, row in enumerate(right_rows)
        if index not in used_right
    ]
    return links, unmatched_left, unmatched_right


def branch_links_and_events(
    merged_rows: list[dict[str, Any]],
    nodes: tuple[float, ...],
    soft_nodes: tuple[float, ...],
    decay_nodes: tuple[float, ...],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    by_slice: dict[
        tuple[str, float, float], list[dict[str, Any]]
    ] = {}
    for row in merged_rows:
        key = (
            str(row["direction"]),
            float(row["energy_witness"]),
            float(row["fixed_coordinate"]),
        )
        by_slice.setdefault(key, []).append(row)
    links: list[dict[str, Any]] = []
    events: list[dict[str, Any]] = []
    for direction, fixed_values in (
        ("soft_cosine", decay_nodes),
        ("decay_cosine", soft_nodes),
    ):
        for fixed in fixed_values:
            for slab_index, (left_energy, right_energy) in enumerate(
                zip(nodes[:-1], nodes[1:])
            ):
                left_rows = sorted(
                    by_slice.get(
                        (direction, left_energy, fixed), []
                    ),
                    key=lambda row: float(
                        row["boundary_coordinate"]
                    ),
                )
                right_rows = sorted(
                    by_slice.get(
                        (direction, right_energy, fixed), []
                    ),
                    key=lambda row: float(
                        row["boundary_coordinate"]
                    ),
                )
                matched, unmatched_left, unmatched_right = (
                    greedy_links(left_rows, right_rows)
                )
                for link_index, (left, right) in enumerate(matched):
                    left_coordinate = float(
                        left["boundary_coordinate"]
                    )
                    right_coordinate = float(
                        right["boundary_coordinate"]
                    )
                    links.append(
                        {
                            "direction": direction,
                            "fixed_coordinate": fixed,
                            "slab_index": slab_index,
                            "left_energy": left_energy,
                            "right_energy": right_energy,
                            "link_index": link_index,
                            "left_coordinate": left_coordinate,
                            "right_coordinate": right_coordinate,
                            "coordinate_shift": (
                                right_coordinate - left_coordinate
                            ),
                            "absolute_coordinate_shift": abs(
                                right_coordinate - left_coordinate
                            ),
                            "left_owner_count": int(
                                left["owner_count"]
                            ),
                            "right_owner_count": int(
                                right["owner_count"]
                            ),
                            "owner_signature_changed": (
                                left["labels"] != right["labels"]
                            ),
                            "valid_for_full_phase_space_coefficient": False,
                            "valid_for_numeric_UV_claim": False,
                            "valid_for_local_GR_claim": False,
                            "valid_for_full_MTS_claim": False,
                        }
                    )
                for side, unmatched in (
                    ("left_only", unmatched_left),
                    ("right_only", unmatched_right),
                ):
                    for row in unmatched:
                        coordinate = float(
                            row["boundary_coordinate"]
                        )
                        event_type = (
                            "angular_endpoint_entry_or_exit"
                            if min(
                                abs(
                                    coordinate
                                    + M5270.ANGULAR_LIMIT
                                ),
                                abs(
                                    coordinate
                                    - M5270.ANGULAR_LIMIT
                                ),
                            )
                            <= ENDPOINT_EVENT_DISTANCE
                            else "interior_birth_death_or_merge"
                        )
                        events.append(
                            {
                                "event_type": event_type,
                                "direction": direction,
                                "fixed_coordinate": fixed,
                                "slab_index": slab_index,
                                "left_energy": left_energy,
                                "right_energy": right_energy,
                                "unmatched_side": side,
                                "boundary_coordinate": coordinate,
                                "owner_count": int(row["owner_count"]),
                                "labels": row["labels"],
                                "event_energy_bracket_width": (
                                    right_energy - left_energy
                                ),
                                "event_classified": True,
                                "valid_for_full_phase_space_coefficient": False,
                                "valid_for_numeric_UV_claim": False,
                                "valid_for_local_GR_claim": False,
                                "valid_for_full_MTS_claim": False,
                            }
                        )
                if (
                    len(left_rows) == len(right_rows)
                    and any(
                        left["labels"] != right["labels"]
                        for left, right in matched
                    )
                ):
                    events.append(
                        {
                            "event_type": (
                                "owner_merge_split_or_order_exchange"
                            ),
                            "direction": direction,
                            "fixed_coordinate": fixed,
                            "slab_index": slab_index,
                            "left_energy": left_energy,
                            "right_energy": right_energy,
                            "unmatched_side": "",
                            "boundary_coordinate": "",
                            "owner_count": "",
                            "labels": "",
                            "event_energy_bracket_width": (
                                right_energy - left_energy
                            ),
                            "event_classified": True,
                            "valid_for_full_phase_space_coefficient": False,
                            "valid_for_numeric_UV_claim": False,
                            "valid_for_local_GR_claim": False,
                            "valid_for_full_MTS_claim": False,
                        }
                    )
    if not events:
        events.append(
            {
                "event_type": "none_on_energy_ladder",
                "direction": "ALL",
                "fixed_coordinate": "",
                "slab_index": "",
                "left_energy": "",
                "right_energy": "",
                "unmatched_side": "",
                "boundary_coordinate": "",
                "owner_count": "",
                "labels": "",
                "event_energy_bracket_width": "",
                "event_classified": True,
                "valid_for_full_phase_space_coefficient": False,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    return links, events


def witness_reproduction_rows(
    merged_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    prior_rows = read_csv(MERGED_5270)
    rows: list[dict[str, Any]] = []
    for prior in prior_rows:
        candidates = [
            row
            for row in merged_rows
            if row["direction"] == prior["direction"]
            and float(row["energy_witness"])
            == float(prior["energy_witness"])
            and float(row["fixed_coordinate"])
            == float(prior["fixed_coordinate"])
        ]
        residual = min(
            (
                abs(
                    float(row["boundary_coordinate"])
                    - float(prior["boundary_coordinate"])
                )
                for row in candidates
            ),
            default=math.inf,
        )
        rows.append(
            {
                "direction": prior["direction"],
                "energy_witness": prior["energy_witness"],
                "fixed_coordinate": prior["fixed_coordinate"],
                "prior_boundary_coordinate": prior[
                    "boundary_coordinate"
                ],
                "nearest_surface_coordinate_residual": residual,
                "reproduced": (
                    residual <= WITNESS_REPRODUCTION_TOLERANCE
                ),
                "valid_for_full_phase_space_coefficient": False,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    return rows


def dry_run() -> dict[str, Any]:
    set_below_normal_priority()
    SOURCE.mkdir(parents=True, exist_ok=True)
    parent = read_json(RESULT_5270)
    nodes = energy_nodes()
    E040, E020 = M5270.source_jobs()
    descriptors, _, mismatches = M5270.descriptor_rows(E040, E020)
    checks = {
        "parent_5270_accepted": bool(parent["acceptance_passed"]),
        "energy_domain_endpoints_present": (
            nodes[0] == M5267.ENERGY_MINIMUM
            and nodes[-1] == M5267.ENERGY_MAXIMUM
        ),
        "all_5270_witnesses_present": set(
            float(value) for value in M5269.ENERGY_WITNESSES
        ).issubset(set(nodes)),
        "twenty_four_descriptors_loaded": len(descriptors) == 24,
        "regulator_descriptors_match": mismatches == 0,
        "source_paths_exist": all(
            Path(row["path"]).exists() for row in source_rows()
        ),
        "resource_contract_is_single_process": True,
        "claims_locked_false": True,
    }
    result = {
        "checkpoint": CHECKPOINT,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "mode": "dry-run",
        "checks": checks,
        "acceptance_passed": all(checks.values()),
        "energy_node_count": len(nodes),
        "energy_nodes": list(nodes),
        "scheduled_boundary_function_count": (
            len(descriptors) * len(nodes) * 8
        ),
        "angular_scan_points": ANGULAR_SCAN_POINTS,
        "resource_contract": {
            "maximum_task_python_processes": 1,
            "worker_math_threads": 1,
            "windows_priority": "BelowNormal",
            "sustained_redline_forbidden": True,
        },
        "decision": (
            "DRY_RUN_ACCEPTED__EXECUTE_SOFT_ENERGY_SURFACE_ORACLE"
            if all(checks.values())
            else "REPAIR_5271_DRY_RUN"
        ),
        "runtime_seconds": 0.0,
        "claim_boundary": {
            field: False for field in CLAIM_FIELDS
        },
    }
    write_csv(ENERGY_NODES, energy_node_rows(nodes))
    atomic_json(DRY_RUN, result)
    return result


def execute() -> dict[str, Any]:
    started = time.perf_counter()
    set_below_normal_priority()
    dry = dry_run()
    if not dry["acceptance_passed"]:
        raise RuntimeError("5271 dry run did not pass")
    parent = read_json(RESULT_5270)
    parent_5269 = read_json(M5270.RESULT_5269)
    nodes = energy_nodes()
    soft_nodes = tuple(
        float(value) for value in parent_5269["soft_nodes"]
    )
    decay_nodes = tuple(
        float(value) for value in parent_5269["decay_nodes"]
    )
    E040, E020 = M5270.source_jobs()
    descriptors, by_component, descriptor_mismatches = (
        M5270.descriptor_rows(E040, E020)
    )
    angular_coordinates = np.linspace(
        -M5270.ANGULAR_LIMIT,
        M5270.ANGULAR_LIMIT,
        ANGULAR_SCAN_POINTS,
    )
    function_rows: list[dict[str, Any]] = []
    raw_rows: list[dict[str, Any]] = []
    for descriptor in descriptors:
        for energy in nodes:
            for fixed_decay in decay_nodes:
                summary, boundaries = (
                    M5270.scan_boundary_function(
                        "soft_cosine",
                        energy,
                        fixed_decay,
                        descriptor,
                        angular_coordinates,
                    )
                )
                function_rows.append(summary)
                raw_rows.extend(boundaries)
            for fixed_soft in soft_nodes:
                summary, boundaries = (
                    M5270.scan_boundary_function(
                        "decay_cosine",
                        energy,
                        fixed_soft,
                        descriptor,
                        angular_coordinates,
                    )
                )
                function_rows.append(summary)
                raw_rows.extend(boundaries)
    merged_rows = M5270.merge_boundaries(raw_rows)
    original_energy_contract = M5269.ENERGY_WITNESSES
    M5269.ENERGY_WITNESSES = nodes
    try:
        panels = M5270.panel_rows(
            merged_rows,
            by_component,
            soft_nodes,
            decay_nodes,
        )
    finally:
        M5269.ENERGY_WITNESSES = original_energy_contract
    slice_rows = slice_summary_rows(
        merged_rows,
        panels,
        nodes,
        soft_nodes,
        decay_nodes,
    )
    link_rows, event_rows = branch_links_and_events(
        merged_rows,
        nodes,
        soft_nodes,
        decay_nodes,
    )
    reproduction_rows = witness_reproduction_rows(merged_rows)
    event_types = {
        str(row["event_type"])
        for row in event_rows
        if row["event_type"] != "none_on_energy_ladder"
    }
    maximum_shift = max(
        (
            float(row["absolute_coordinate_shift"])
            for row in link_rows
        ),
        default=0.0,
    )
    maximum_panel_residual = max(
        float(row["panel_coverage_residual"])
        for row in slice_rows
    )
    checks = {
        "parent_5270_accepted": bool(parent["acceptance_passed"]),
        "regulator_descriptors_match": descriptor_mismatches == 0,
        "all_boundary_functions_finite": all(
            bool(row["all_values_finite"]) for row in function_rows
        ),
        "all_boundaries_tight": (
            bool(raw_rows)
            and max(
                float(row["bracket_width"]) for row in raw_rows
            )
            <= M5270.BOUNDARY_WIDTH_LIMIT
            and max(
                abs(float(row["root_margin"])) for row in raw_rows
            )
            <= M5270.BOUNDARY_RESIDUAL_LIMIT
        ),
        "all_5270_witnesses_reproduced": all(
            bool(row["reproduced"]) for row in reproduction_rows
        ),
        "every_energy_slice_panelized": (
            len(slice_rows) == len(nodes) * 8
            and maximum_panel_residual <= 1.0e-12
        ),
        "all_surface_events_classified": all(
            bool(row["event_classified"]) for row in event_rows
        ),
        "all_branch_links_finite": all(
            math.isfinite(
                float(row["absolute_coordinate_shift"])
            )
            for row in link_rows
        ),
        "formalization_workbench_unchanged": (
            formal_inventory_digest()
            == str(parent["formalization_workbench_end_digest"])
        ),
        "claims_locked_false": True,
    }
    accepted = all(checks.values())
    formal_end = formal_inventory_digest()
    result = {
        "checkpoint": CHECKPOINT,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "mode": "soft-energy-angular-boundary-surface-oracle",
        "checks": checks,
        "acceptance_passed": accepted,
        "energy_node_count": len(nodes),
        "energy_nodes": list(nodes),
        "energy_slab_count": len(nodes) - 1,
        "boundary_function_count": len(function_rows),
        "raw_boundary_count": len(raw_rows),
        "merged_boundary_count": len(merged_rows),
        "panel_count": len(panels),
        "slice_count": len(slice_rows),
        "branch_link_count": len(link_rows),
        "surface_event_count": sum(
            row["event_type"] != "none_on_energy_ladder"
            for row in event_rows
        ),
        "surface_event_types": sorted(event_types),
        "maximum_link_coordinate_shift": maximum_shift,
        "maximum_panel_coverage_residual": maximum_panel_residual,
        "witness_reproduction_count": sum(
            bool(row["reproduced"]) for row in reproduction_rows
        ),
        "witness_reference_count": len(reproduction_rows),
        "surface_oracle_contract": {
            "boundary_equation": "log|z_label(x,c)|=0",
            "energy_sampling": (
                "Chebyshev-Lobatto ladder plus every 5270 witness"
            ),
            "angular_scan_points_per_function": (
                ANGULAR_SCAN_POINTS
            ),
            "branch_matching": (
                "nearest-coordinate links between adjacent energy slices"
            ),
            "topology_events": (
                "unmatched boundaries and owner-signature exchanges "
                "are explicitly bracketed by energy slabs"
            ),
            "regulator_independent": True,
        },
        "resource_contract": {
            "maximum_task_python_processes": 1,
            "worker_math_threads": 1,
            "windows_priority": "BelowNormal",
            "sustained_redline_forbidden": True,
        },
        "source_files": source_rows(),
        "formalization_workbench_reference_digest": str(
            parent["formalization_workbench_end_digest"]
        ),
        "formalization_workbench_end_digest": formal_end,
        "formalization_workbench_modified_file_count": (
            0
            if formal_end
            == str(parent["formalization_workbench_end_digest"])
            else -1
        ),
        "runtime_seconds": time.perf_counter() - started,
        "decision": (
            "ADOPT_SOFT_ENERGY_BOUNDARY_SURFACE_ORACLE__"
            "LOCALIZE_CLASSIFIED_TOPOLOGY_EVENTS"
            if accepted
            else "REPAIR_SOFT_ENERGY_BOUNDARY_SURFACE_ORACLE"
        ),
        "claim_boundary": {
            "valid_for_discrete_energy_surface_oracle": accepted,
            "valid_for_classified_surface_event_brackets": accepted,
            "valid_for_exact_surface_event_locations": False,
            "valid_for_full_phase_space_coefficient": False,
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
            "reason": (
                "Surface topology events are classified and bracketed "
                "but not yet solved to exact energy coordinates."
            ),
        },
    }
    write_csv(ENERGY_NODES, energy_node_rows(nodes))
    write_csv(FUNCTION_SUMMARY, function_rows)
    write_csv(RAW_BOUNDARIES, raw_rows)
    write_csv(MERGED_BOUNDARIES, merged_rows)
    write_csv(PANELS, panels)
    write_csv(SLICE_SUMMARY, slice_rows)
    write_csv(BRANCH_LINKS, link_rows)
    write_csv(TOPOLOGY_EVENTS, event_rows)
    write_csv(WITNESS_REPRODUCTION, reproduction_rows)
    atomic_json(RESULT, result)
    atomic_json(
        STATUS,
        {
            "checkpoint": CHECKPOINT,
            "mode": result["mode"],
            "state": "COMPLETED",
            "acceptance_passed": accepted,
            "decision": result["decision"],
            "runtime_seconds": result["runtime_seconds"],
        },
    )
    return result


def validation_gate(
    gate_id: str, passed: bool, detail: str
) -> dict[str, Any]:
    return {
        "gate_id": gate_id,
        "passed": bool(passed),
        "detail": detail,
    }


def render_document(
    result: dict[str, Any], validation_passed: bool
) -> None:
    text = f"""# 5271 - Soft-energy angular-boundary surface oracle

## Construction

Checkpoint 5270 derived the shared angular boundary equation

`log|z_label(x,c)| = 0`

at eight soft-energy witnesses. This checkpoint evaluates the same equation on
a `{int(result['energy_node_count'])}`-node Chebyshev-Lobatto energy ladder that
also contains every checkpoint-5270 witness. At every energy and transverse
angular node, all labelled roots are rescanned over the complete angular
domain, localized, merged, and converted into topology-uniform panels. No
surface interpolation is used to decide occupation.

Adjacent energy slices are linked by nearest boundary coordinate. Unmatched
boundaries and owner-signature exchanges are retained as explicit topology
event brackets rather than silently interpolated through.

## Result

- Energy nodes: `{int(result['energy_node_count'])}`.
- Energy slabs: `{int(result['energy_slab_count'])}`.
- Boundary functions: `{int(result['boundary_function_count'])}`.
- Raw boundaries: `{int(result['raw_boundary_count'])}`.
- Merged boundaries: `{int(result['merged_boundary_count'])}`.
- Topology-uniform panels: `{int(result['panel_count'])}`.
- Boundary branch links: `{int(result['branch_link_count'])}`.
- Classified surface-event brackets: `{int(result['surface_event_count'])}`.
- Event types: `{", ".join(result['surface_event_types']) or "none"}`.
- Maximum adjacent-slice coordinate shift: `{float(result['maximum_link_coordinate_shift']):.12g}`.
- Maximum panel coverage residual: `{float(result['maximum_panel_coverage_residual']):.12g}`.
- Checkpoint-5270 witnesses reproduced: `{int(result['witness_reproduction_count'])}/{int(result['witness_reference_count'])}`.

## Decision

`{result['decision']}`

Validation passed: `{str(validation_passed).lower()}`.

This accepts an independently rescanned boundary oracle over soft energy and
classifies every detected surface-topology event. It does not yet solve those
event locations exactly, authorize interpolation through them, produce a full
phase-space coefficient, establish a numeric UV value, derive local GR, or
complete MTS.

## Next derivation

For every classified event slab, solve either the angular-endpoint equation or
the interior double-root system

`m_label(x,c)=0`, `partial_c m_label(x,c)=0`.

Insert those exact event energies into the ladder, reconnect boundary families,
and require stable three-dimensional cell counts before angular cubature.

## Artifacts

- Runner: `{Path(__file__).resolve()}`
- Result: `{RESULT}`
- Energy nodes: `{ENERGY_NODES}`
- Merged boundaries: `{MERGED_BOUNDARIES}`
- Boundary links: `{BRANCH_LINKS}`
- Surface events: `{TOPOLOGY_EVENTS}`
- Witness reproduction: `{WITNESS_REPRODUCTION}`
- Validation: `{VALIDATION}`
"""
    temporary = DOCUMENT.with_suffix(DOCUMENT.suffix + ".tmp")
    temporary.write_text(text, encoding="utf-8")
    os.replace(temporary, DOCUMENT)


def validate_outputs() -> dict[str, Any]:
    result = read_json(RESULT)
    parent = read_json(RESULT_5270)
    required_csvs = (
        ENERGY_NODES,
        FUNCTION_SUMMARY,
        RAW_BOUNDARIES,
        MERGED_BOUNDARIES,
        PANELS,
        SLICE_SUMMARY,
        BRANCH_LINKS,
        TOPOLOGY_EVENTS,
        WITNESS_REPRODUCTION,
    )
    csv_rows = {
        str(path): read_csv(path)
        for path in required_csvs
        if path.exists()
    }
    source_files = result["source_files"]
    current_formal_digest = formal_inventory_digest()
    reference_formal_digest = str(
        result["formalization_workbench_reference_digest"]
    )
    serialized = json.dumps(
        {"result": result, "csvs": csv_rows},
        default=json_default,
    )
    claim_rows = [
        row
        for rows in csv_rows.values()
        for row in rows
        if any(field in row for field in CLAIM_FIELDS)
    ]
    rows = [
        validation_gate(
            "SOURCE_PATHS_EXIST",
            all(Path(row["path"]).exists() for row in source_files),
            f"{len(source_files)} source paths",
        ),
        validation_gate(
            "SOURCE_HASHES_MATCH",
            all(
                digest(Path(row["path"])) == row["sha256"]
                for row in source_files
            ),
            "all recorded source hashes reproduce",
        ),
        validation_gate(
            "PARENT_5270_ACCEPTED",
            bool(parent["acceptance_passed"]),
            str(parent["decision"]),
        ),
        validation_gate(
            "SURFACE_ORACLE_ACCEPTED",
            bool(result["acceptance_passed"]),
            str(result["decision"]),
        ),
        validation_gate(
            "REQUIRED_CSVS_PARSE",
            (
                len(csv_rows) == len(required_csvs)
                and all(csv_rows.values())
            ),
            f"{len(csv_rows)}/{len(required_csvs)} non-empty CSVs",
        ),
        validation_gate(
            "WITNESS_SLICES_REPRODUCE_5270",
            int(result["witness_reproduction_count"])
            == int(result["witness_reference_count"]),
            (
                f"{result['witness_reproduction_count']}/"
                f"{result['witness_reference_count']}"
            ),
        ),
        validation_gate(
            "EVERY_ENERGY_SLICE_PANELIZED",
            float(result["maximum_panel_coverage_residual"])
            <= 1.0e-12,
            (
                "maximum residual="
                f"{result['maximum_panel_coverage_residual']}"
            ),
        ),
        validation_gate(
            "SURFACE_EVENTS_CLASSIFIED",
            bool(result["claim_boundary"][
                "valid_for_classified_surface_event_brackets"
            ]),
            (
                f"events={result['surface_event_count']}; "
                f"types={result['surface_event_types']}"
            ),
        ),
        validation_gate(
            "EXACT_EVENT_CLAIM_REMAINS_FALSE",
            not result["claim_boundary"][
                "valid_for_exact_surface_event_locations"
            ],
            "event energies remain bracketed, not claimed exact",
        ),
        validation_gate(
            "NO_MISSING_MARKERS",
            "MISSING_" not in serialized,
            "no MISSING_ token in checkpoint artifacts",
        ),
        validation_gate(
            "CLAIMS_LOCKED_FALSE",
            (
                all(
                    not result["claim_boundary"][field]
                    for field in CLAIM_FIELDS
                )
                and all(
                    row.get(field, "false").lower() == "false"
                    for row in claim_rows
                    for field in CLAIM_FIELDS
                    if field in row
                )
            ),
            "phase-space, UV, local-GR, and full-MTS claims false",
        ),
        validation_gate(
            "FORMALIZATION_WORKBENCH_UNCHANGED",
            current_formal_digest == reference_formal_digest,
            (
                f"reference={reference_formal_digest}; "
                f"current={current_formal_digest}"
            ),
        ),
        validation_gate(
            "RESOURCE_CONTRACT_RECORDED",
            (
                result["resource_contract"][
                    "maximum_task_python_processes"
                ]
                == 1
                and result["resource_contract"]["worker_math_threads"]
                == 1
            ),
            "one below-normal single-thread process",
        ),
    ]
    passed = all(row["passed"] for row in rows)
    write_csv(VALIDATION, rows)
    write_csv(RESIDUAL_VALIDATION, rows)
    render_document(result, passed)
    atomic_json(
        STATUS,
        {
            "checkpoint": CHECKPOINT,
            "mode": "validation",
            "state": "COMPLETED",
            "validation_passed": passed,
            "validation_gate_count": len(rows),
            "decision": result["decision"],
        },
    )
    return {
        "checkpoint": CHECKPOINT,
        "mode": "validation",
        "acceptance_passed": passed,
        "decision": (
            "VALIDATED_SOFT_ENERGY_BOUNDARY_SURFACE_ORACLE"
            if passed
            else "VALIDATION_REQUIRES_REPAIR"
        ),
        "runtime_seconds": 0.0,
        "validation_gate_count": len(rows),
        "failed_gates": [
            row["gate_id"] for row in rows if not row["passed"]
        ],
        "valid_for_full_phase_space_coefficient": False,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=("dry-run", "run", "validate"),
        default="dry-run",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.mode == "dry-run":
        result = dry_run()
    elif args.mode == "run":
        result = execute()
    elif args.mode == "validate":
        result = validate_outputs()
    else:
        raise RuntimeError(f"unsupported mode: {args.mode}")
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
