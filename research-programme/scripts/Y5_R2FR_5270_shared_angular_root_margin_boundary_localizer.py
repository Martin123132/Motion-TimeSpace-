from __future__ import annotations

import argparse
import cmath
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
from typing import Any, Callable


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
SOURCE = FUNCTIONAL_RG / "5270"
RESIDUALS = POST / "source-intake" / "mts_residuals"

SCRIPT_5269 = (
    SCRIPTS
    / "Y5_R2FR_5269_joint_angular_energy_first_topology_preflight.py"
)
RESULT_5269 = (
    FUNCTIONAL_RG
    / "5269"
    / "joint_angular_energy_first_preflight_result.json"
)
VALIDATION_5269 = (
    FUNCTIONAL_RG
    / "5269"
    / "joint_angular_energy_first_validation.csv"
)
TRANSITIONS_5269 = (
    FUNCTIONAL_RG / "5269" / "angular_transition_edges.csv"
)
MANIFEST_5239 = (
    FUNCTIONAL_RG / "5239" / "matched_event_A00_job_manifest.json"
)

DRY_RUN = SOURCE / "root_margin_localization_dry_run.json"
DESCRIPTORS = SOURCE / "shared_cycle_boundary_descriptors.csv"
FUNCTION_SUMMARY = SOURCE / "root_margin_function_summary.csv"
RAW_BOUNDARIES = SOURCE / "localized_root_margin_boundaries.csv"
MERGED_BOUNDARIES = SOURCE / "merged_shared_angular_boundaries.csv"
PANELS = SOURCE / "topology_uniform_angular_panels.csv"
COARSE_COVERAGE = SOURCE / "coarse_transition_coverage.csv"
RESULT = SOURCE / "shared_angular_boundary_localization_result.json"
VALIDATION = SOURCE / "shared_angular_boundary_localization_validation.csv"
RESIDUAL_VALIDATION = (
    RESIDUALS / "P8_Y5_BRR545_5270_VALIDATION.csv"
)
STATUS = SOURCE / "status.json"
DOCUMENT = (
    POST
    / "5270-Y5-R2FR-shared-angular-root-margin-boundary-localization.md"
)

CHECKPOINT = 5270
PARENT_CHECKPOINT = 5269
MARKER = "MTS_5270_SHARED_ANGULAR_ROOT_MARGIN_BOUNDARY_LOCALIZER"
REVISION = "shared-angular-root-margin-boundary-localizer-v1"
ANGULAR_LIMIT = 0.995
SCAN_POINTS = 1025
BOUNDARY_WIDTH_LIMIT = 2.0e-10
BOUNDARY_RESIDUAL_LIMIT = 2.0e-8
MERGE_COORDINATE_TOLERANCE = 5.0e-8
MIDPOINT_MARGIN_MINIMUM = 1.0e-8
MAXIMUM_BISECTIONS = 64
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


M5269 = load_module("mts_5269_for_5270", SCRIPT_5269)
M5267 = M5269.M5267
M5239 = M5269.M5239
M5237 = M5269.M5237
M5231 = M5239.M5231
M5028 = M5231.M5028
M5024 = M5028.M5024

TOPOLOGY_CACHE: dict[str, dict[str, Any]] = {}


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
        SCRIPT_5269,
        RESULT_5269,
        VALIDATION_5269,
        TRANSITIONS_5269,
        MANIFEST_5239,
    )
    return [
        {"path": str(path), "sha256": digest(path)}
        for path in paths
    ]


def topology(job: dict[str, Any]) -> dict[str, Any]:
    path = str(job["source_topology"])
    if path not in TOPOLOGY_CACHE:
        TOPOLOGY_CACHE[path] = read_json(Path(path))
    return TOPOLOGY_CACHE[path]


def source_jobs() -> tuple[
    list[dict[str, Any]], list[dict[str, Any]]
]:
    jobs = list(read_json(MANIFEST_5239)["jobs"])
    E040 = sorted(
        (
            job
            for job in jobs
            if str(job["epsilon_id"]) == "E040"
        ),
        key=lambda job: str(job["component_id"]),
    )
    E020 = sorted(
        (
            job
            for job in jobs
            if str(job["epsilon_id"]) == "E020"
        ),
        key=lambda job: str(job["component_id"]),
    )
    return E040, E020


def role_crossing(
    job: dict[str, Any], role: str
) -> tuple[dict[str, Any], dict[str, Any]]:
    source_topology = topology(job)
    pair = tuple(job[f"{role}_pair"])
    crossing = M5237.find_source_crossing(
        source_topology,
        int(job[f"{role}_chamber"]),
        pair,
        M5269.complex_value(job[f"{role}_anchor"]),
    )
    chamber = source_topology["chambers"][
        int(job[f"{role}_chamber"])
    ]
    return crossing, chamber


def descriptor_rows(
    E040: list[dict[str, Any]],
    E020: list[dict[str, Any]],
) -> tuple[
    list[dict[str, Any]],
    dict[str, list[dict[str, Any]]],
    int,
]:
    by_component: dict[str, list[dict[str, Any]]] = {}
    rows: list[dict[str, Any]] = []
    mismatch_count = 0
    E020_by_component = {
        str(job["component_id"]): job for job in E020
    }
    for job in E040:
        component_id = str(job["component_id"])
        local: list[dict[str, Any]] = []
        comparison = E020_by_component[component_id]
        for role in ("representative", "reciprocal"):
            crossing, chamber = role_crossing(job, role)
            other_crossing, other_chamber = role_crossing(
                comparison, role
            )
            labels = tuple(crossing["representing_pairs"][0])
            other_labels = tuple(
                other_crossing["representing_pairs"][0]
            )
            midpoint = 0.5 * (
                float(chamber["start_physical_angle"])
                + float(chamber["end_physical_angle"])
            )
            other_midpoint = 0.5 * (
                float(other_chamber["start_physical_angle"])
                + float(other_chamber["end_physical_angle"])
            )
            descriptor_match = (
                labels == other_labels
                and abs(midpoint - other_midpoint) <= 1.0e-14
            )
            mismatch_count += not descriptor_match
            for label_index, label in enumerate(labels):
                source_name, root_label = label.rsplit(":", 1)
                row = {
                    "component_id": component_id,
                    "owner_summand": job["owner_summand"],
                    "role": role,
                    "label_index": label_index,
                    "full_label": label,
                    "source_name": source_name,
                    "root_label": root_label,
                    "chamber_index": int(job[f"{role}_chamber"]),
                    "chamber_midpoint": midpoint,
                    "paired_label": labels[1 - label_index],
                    "E040_E020_descriptor_match": descriptor_match,
                    "valid_for_full_phase_space_coefficient": False,
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
                rows.append(row)
                local.append(row)
        by_component[component_id] = local
    return rows, by_component, mismatch_count


def event_root_margins(
    energy: float,
    soft_cosine: float,
    decay_cosine: float,
    descriptor: dict[str, Any],
) -> tuple[float, float]:
    relative_circle = cmath.exp(
        1.0j * float(descriptor["chamber_midpoint"])
    )
    soft_direction, decay_direction, internal = (
        M5028.event_geometry(
            float(energy),
            complex(float(soft_cosine), 0.0),
            complex(float(decay_cosine), 0.0),
            relative_circle,
        )
    )
    directions = M5028.source_directions(
        internal, soft_direction, decay_direction
    )
    roots = M5024.all_factor_roots(
        directions[str(descriptor["source_name"])],
        M5028.REFERENCE_COSINE,
    )
    root = complex(roots[str(descriptor["root_label"])])
    magnitude = abs(root)
    margin = math.log(max(magnitude, 1.0e-300))
    return margin, magnitude


def coordinate_margin_function(
    direction: str,
    energy: float,
    fixed_coordinate: float,
    descriptor: dict[str, Any],
) -> Callable[[float], tuple[float, float]]:
    if direction == "soft_cosine":
        return lambda coordinate: event_root_margins(
            energy,
            coordinate,
            fixed_coordinate,
            descriptor,
        )
    if direction == "decay_cosine":
        return lambda coordinate: event_root_margins(
            energy,
            fixed_coordinate,
            coordinate,
            descriptor,
        )
    raise ValueError(f"unsupported angular direction: {direction}")


def bisect_margin_zero(
    function: Callable[[float], tuple[float, float]],
    left: float,
    right: float,
    left_margin: float,
    right_margin: float,
) -> dict[str, Any]:
    if left_margin == 0.0:
        return {
            "left": left,
            "right": left,
            "coordinate": left,
            "margin": left_margin,
            "magnitude": 1.0,
            "bisections": 0,
        }
    if right_margin == 0.0:
        return {
            "left": right,
            "right": right,
            "coordinate": right,
            "margin": right_margin,
            "magnitude": 1.0,
            "bisections": 0,
        }
    if left_margin * right_margin > 0.0:
        raise RuntimeError("root-margin bracket does not change sign")
    lower = float(left)
    upper = float(right)
    f_lower = float(left_margin)
    f_upper = float(right_margin)
    midpoint = 0.5 * (lower + upper)
    f_midpoint, magnitude = function(midpoint)
    bisections = 0
    while (
        upper - lower > BOUNDARY_WIDTH_LIMIT
        and bisections < MAXIMUM_BISECTIONS
    ):
        midpoint = 0.5 * (lower + upper)
        f_midpoint, magnitude = function(midpoint)
        if f_midpoint == 0.0:
            lower = midpoint
            upper = midpoint
            break
        if f_lower * f_midpoint <= 0.0:
            upper = midpoint
            f_upper = f_midpoint
        else:
            lower = midpoint
            f_lower = f_midpoint
        bisections += 1
    midpoint = 0.5 * (lower + upper)
    f_midpoint, magnitude = function(midpoint)
    return {
        "left": lower,
        "right": upper,
        "coordinate": midpoint,
        "margin": f_midpoint,
        "magnitude": magnitude,
        "bisections": bisections,
        "left_margin": f_lower,
        "right_margin": f_upper,
    }


def scan_boundary_function(
    direction: str,
    energy: float,
    fixed_coordinate: float,
    descriptor: dict[str, Any],
    coordinates: np.ndarray,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    function = coordinate_margin_function(
        direction, energy, fixed_coordinate, descriptor
    )
    margins: list[float] = []
    magnitudes: list[float] = []
    for coordinate in coordinates:
        margin, magnitude = function(float(coordinate))
        margins.append(float(margin))
        magnitudes.append(float(magnitude))
    boundaries: list[dict[str, Any]] = []
    for index, (left_margin, right_margin) in enumerate(
        zip(margins[:-1], margins[1:])
    ):
        if left_margin == 0.0 or left_margin * right_margin < 0.0:
            root = bisect_margin_zero(
                function,
                float(coordinates[index]),
                float(coordinates[index + 1]),
                left_margin,
                right_margin,
            )
            boundaries.append(
                {
                    "direction": direction,
                    "energy_witness": energy,
                    "fixed_coordinate": fixed_coordinate,
                    "component_id": descriptor["component_id"],
                    "owner_summand": descriptor["owner_summand"],
                    "role": descriptor["role"],
                    "full_label": descriptor["full_label"],
                    "paired_label": descriptor["paired_label"],
                    "chamber_midpoint": descriptor[
                        "chamber_midpoint"
                    ],
                    "boundary_coordinate": root["coordinate"],
                    "bracket_left": root["left"],
                    "bracket_right": root["right"],
                    "bracket_width": root["right"] - root["left"],
                    "root_margin": root["margin"],
                    "root_magnitude": root["magnitude"],
                    "bisection_count": root["bisections"],
                    "valid_for_full_phase_space_coefficient": False,
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
            )
    summary = {
        "direction": direction,
        "energy_witness": energy,
        "fixed_coordinate": fixed_coordinate,
        "component_id": descriptor["component_id"],
        "role": descriptor["role"],
        "full_label": descriptor["full_label"],
        "scan_point_count": len(coordinates),
        "minimum_margin": min(margins),
        "maximum_margin": max(margins),
        "minimum_absolute_margin": min(abs(value) for value in margins),
        "minimum_root_magnitude": min(magnitudes),
        "maximum_root_magnitude": max(magnitudes),
        "sign_change_count": len(boundaries),
        "all_values_finite": all(
            math.isfinite(value)
            for value in (*margins, *magnitudes)
        ),
        "valid_for_full_phase_space_coefficient": False,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    return summary, boundaries


def merge_boundaries(
    raw_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    groups: dict[
        tuple[str, float, float], list[dict[str, Any]]
    ] = {}
    for row in raw_rows:
        key = (
            str(row["direction"]),
            float(row["energy_witness"]),
            float(row["fixed_coordinate"]),
        )
        groups.setdefault(key, []).append(row)
    merged: list[dict[str, Any]] = []
    for (direction, energy, fixed), rows in sorted(
        groups.items()
    ):
        ordered = sorted(
            rows, key=lambda row: float(row["boundary_coordinate"])
        )
        clusters: list[list[dict[str, Any]]] = []
        for row in ordered:
            if (
                not clusters
                or abs(
                    float(row["boundary_coordinate"])
                    - float(
                        clusters[-1][-1]["boundary_coordinate"]
                    )
                )
                > MERGE_COORDINATE_TOLERANCE
            ):
                clusters.append([row])
            else:
                clusters[-1].append(row)
        for boundary_index, cluster in enumerate(clusters):
            coordinates = [
                float(row["boundary_coordinate"]) for row in cluster
            ]
            merged.append(
                {
                    "direction": direction,
                    "energy_witness": energy,
                    "fixed_coordinate": fixed,
                    "boundary_index": boundary_index,
                    "boundary_coordinate": float(
                        sum(coordinates) / len(coordinates)
                    ),
                    "coordinate_spread": max(coordinates)
                    - min(coordinates),
                    "owner_count": len(cluster),
                    "component_ids": "|".join(
                        sorted(
                            {
                                str(row["component_id"])
                                for row in cluster
                            }
                        )
                    ),
                    "roles": "|".join(
                        sorted(
                            {str(row["role"]) for row in cluster}
                        )
                    ),
                    "labels": "|".join(
                        sorted(
                            {
                                str(row["full_label"])
                                for row in cluster
                            }
                        )
                    ),
                    "maximum_bracket_width": max(
                        float(row["bracket_width"])
                        for row in cluster
                    ),
                    "maximum_absolute_root_margin": max(
                        abs(float(row["root_margin"]))
                        for row in cluster
                    ),
                    "valid_for_full_phase_space_coefficient": False,
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
            )
    return merged


def component_cycle_active(
    energy: float,
    soft_cosine: float,
    decay_cosine: float,
    descriptors: list[dict[str, Any]],
) -> tuple[bool, float]:
    role_states: dict[str, list[bool]] = {
        "representative": [],
        "reciprocal": [],
    }
    minimum_margin = math.inf
    for descriptor in descriptors:
        margin, _ = event_root_margins(
            energy,
            soft_cosine,
            decay_cosine,
            descriptor,
        )
        role_states[str(descriptor["role"])].append(margin < 0.0)
        minimum_margin = min(minimum_margin, abs(margin))
    active = all(
        len(states) == 2 and sum(states) == 1
        for states in role_states.values()
    )
    return active, minimum_margin


def panel_rows(
    merged_rows: list[dict[str, Any]],
    descriptors_by_component: dict[str, list[dict[str, Any]]],
    soft_nodes: tuple[float, ...],
    decay_nodes: tuple[float, ...],
) -> list[dict[str, Any]]:
    groups: dict[
        tuple[str, float, float], list[dict[str, Any]]
    ] = {}
    for row in merged_rows:
        key = (
            str(row["direction"]),
            float(row["energy_witness"]),
            float(row["fixed_coordinate"]),
        )
        groups.setdefault(key, []).append(row)
    for energy in M5269.ENERGY_WITNESSES:
        for fixed_decay in decay_nodes:
            groups.setdefault(
                ("soft_cosine", float(energy), fixed_decay), []
            )
        for fixed_soft in soft_nodes:
            groups.setdefault(
                ("decay_cosine", float(energy), fixed_soft), []
            )
    components = sorted(descriptors_by_component)
    panels: list[dict[str, Any]] = []
    for (direction, energy, fixed), boundaries in sorted(
        groups.items()
    ):
        split_points = [
            -ANGULAR_LIMIT,
            *[
                float(row["boundary_coordinate"])
                for row in sorted(
                    boundaries,
                    key=lambda row: float(
                        row["boundary_coordinate"]
                    ),
                )
            ],
            ANGULAR_LIMIT,
        ]
        for panel_index, (left, right) in enumerate(
            zip(split_points[:-1], split_points[1:])
        ):
            if right - left <= 1.0e-12:
                continue
            midpoint = 0.5 * (left + right)
            signature_bits: list[str] = []
            margins: list[float] = []
            for component_id in components:
                if direction == "soft_cosine":
                    soft_cosine = midpoint
                    decay_cosine = fixed
                else:
                    soft_cosine = fixed
                    decay_cosine = midpoint
                active, minimum_margin = component_cycle_active(
                    energy,
                    soft_cosine,
                    decay_cosine,
                    descriptors_by_component[component_id],
                )
                signature_bits.append("1" if active else "0")
                margins.append(minimum_margin)
            panels.append(
                {
                    "direction": direction,
                    "energy_witness": energy,
                    "fixed_coordinate": fixed,
                    "panel_index": panel_index,
                    "panel_left": left,
                    "panel_right": right,
                    "panel_width": right - left,
                    "panel_midpoint": midpoint,
                    "cycle_signature": "".join(signature_bits),
                    "minimum_midpoint_root_margin": min(margins),
                    "topology_uniform_by_boundary_construction": True,
                    "valid_for_full_phase_space_coefficient": False,
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
            )
    return panels


def coarse_transition_coverage(
    raw_boundaries: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    canonical = [
        row
        for row in read_csv(TRANSITIONS_5269)
        if row["epsilon_id"] == "E040"
        and str(row["transition_kind"]).startswith(
            "cycle_state_"
        )
    ]
    rows: list[dict[str, Any]] = []
    for coarse in canonical:
        direction = (
            "soft_cosine"
            if coarse["transition_kind"]
            == "cycle_state_soft_edge"
            else "decay_cosine"
        )
        lower = min(
            float(coarse["left_coordinate"]),
            float(coarse["right_coordinate"]),
        )
        upper = max(
            float(coarse["left_coordinate"]),
            float(coarse["right_coordinate"]),
        )
        matches = [
            row
            for row in raw_boundaries
            if row["direction"] == direction
            and row["component_id"] == coarse["component_id"]
            and abs(
                float(row["energy_witness"])
                - float(coarse["energy_witness"])
            )
            <= 1.0e-14
            and abs(
                float(row["fixed_coordinate"])
                - float(coarse["fixed_coordinate"])
            )
            <= 1.0e-14
            and lower - BOUNDARY_WIDTH_LIMIT
            <= float(row["boundary_coordinate"])
            <= upper + BOUNDARY_WIDTH_LIMIT
        ]
        rows.append(
            {
                "transition_kind": coarse["transition_kind"],
                "component_id": coarse["component_id"],
                "energy_witness": coarse["energy_witness"],
                "fixed_coordinate": coarse["fixed_coordinate"],
                "left_coordinate": coarse["left_coordinate"],
                "right_coordinate": coarse["right_coordinate"],
                "localized_boundary_count": len(matches),
                "localized_coordinates": "|".join(
                    f"{float(row['boundary_coordinate']):.17g}"
                    for row in matches
                ),
                "coarse_transition_explained": bool(matches),
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
    parent = read_json(RESULT_5269)
    E040, E020 = source_jobs()
    descriptors, _, mismatches = descriptor_rows(E040, E020)
    checks = {
        "parent_5269_accepted": bool(parent["acceptance_passed"]),
        "six_E040_jobs_loaded": len(E040) == 6,
        "six_E020_jobs_loaded": len(E020) == 6,
        "twenty_four_root_descriptors_built": (
            len(descriptors) == 24
        ),
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
        "descriptor_count": len(descriptors),
        "scheduled_boundary_function_count": (
            len(descriptors)
            * len(M5269.ENERGY_WITNESSES)
            * 4
            * 2
        ),
        "scan_points_per_function": SCAN_POINTS,
        "resource_contract": {
            "maximum_task_python_processes": 1,
            "worker_math_threads": 1,
            "windows_priority": "BelowNormal",
            "sustained_redline_forbidden": True,
        },
        "decision": (
            "DRY_RUN_ACCEPTED__LOCALIZE_SHARED_ROOT_MARGIN_BOUNDARIES"
            if all(checks.values())
            else "REPAIR_5270_DRY_RUN"
        ),
        "runtime_seconds": 0.0,
        "claim_boundary": {
            field: False for field in CLAIM_FIELDS
        },
    }
    write_csv(DESCRIPTORS, descriptors)
    atomic_json(DRY_RUN, result)
    return result


def execute() -> dict[str, Any]:
    started = time.perf_counter()
    set_below_normal_priority()
    dry = dry_run()
    if not dry["acceptance_passed"]:
        raise RuntimeError("5270 dry run did not pass")
    parent = read_json(RESULT_5269)
    E040, E020 = source_jobs()
    descriptors, by_component, descriptor_mismatches = (
        descriptor_rows(E040, E020)
    )
    soft_nodes = tuple(float(value) for value in parent["soft_nodes"])
    decay_nodes = tuple(
        float(value) for value in parent["decay_nodes"]
    )
    coordinates = np.linspace(
        -ANGULAR_LIMIT, ANGULAR_LIMIT, SCAN_POINTS
    )
    function_rows: list[dict[str, Any]] = []
    boundary_rows: list[dict[str, Any]] = []
    for descriptor in descriptors:
        for energy in M5269.ENERGY_WITNESSES:
            for fixed_decay in decay_nodes:
                summary, boundaries = scan_boundary_function(
                    "soft_cosine",
                    float(energy),
                    fixed_decay,
                    descriptor,
                    coordinates,
                )
                function_rows.append(summary)
                boundary_rows.extend(boundaries)
            for fixed_soft in soft_nodes:
                summary, boundaries = scan_boundary_function(
                    "decay_cosine",
                    float(energy),
                    fixed_soft,
                    descriptor,
                    coordinates,
                )
                function_rows.append(summary)
                boundary_rows.extend(boundaries)
    merged_rows = merge_boundaries(boundary_rows)
    panels = panel_rows(
        merged_rows, by_component, soft_nodes, decay_nodes
    )
    coverage_rows = coarse_transition_coverage(boundary_rows)
    panel_groups: dict[
        tuple[str, float, float], list[dict[str, Any]]
    ] = {}
    for row in panels:
        key = (
            str(row["direction"]),
            float(row["energy_witness"]),
            float(row["fixed_coordinate"]),
        )
        panel_groups.setdefault(key, []).append(row)
    coverage_residuals = [
        abs(
            sum(float(row["panel_width"]) for row in rows)
            - 2.0 * ANGULAR_LIMIT
        )
        for rows in panel_groups.values()
    ]
    maximum_width = max(
        float(row["bracket_width"]) for row in boundary_rows
    )
    maximum_residual = max(
        abs(float(row["root_margin"])) for row in boundary_rows
    )
    maximum_merge_spread = max(
        float(row["coordinate_spread"]) for row in merged_rows
    )
    minimum_panel_margin = min(
        float(row["minimum_midpoint_root_margin"])
        for row in panels
    )
    newly_detected_boundary_count = sum(
        int(row["sign_change_count"]) for row in function_rows
    ) - sum(
        int(row["localized_boundary_count"]) for row in coverage_rows
    )
    checks = {
        "parent_5269_accepted": bool(parent["acceptance_passed"]),
        "regulator_descriptors_match": descriptor_mismatches == 0,
        "all_boundary_functions_finite": all(
            bool(row["all_values_finite"]) for row in function_rows
        ),
        "all_boundaries_localized": (
            bool(boundary_rows)
            and maximum_width <= BOUNDARY_WIDTH_LIMIT
            and maximum_residual <= BOUNDARY_RESIDUAL_LIMIT
        ),
        "all_5269_coarse_transitions_explained": all(
            bool(row["coarse_transition_explained"])
            for row in coverage_rows
        ),
        "merged_boundaries_are_tight": (
            maximum_merge_spread
            <= MERGE_COORDINATE_TOLERANCE
        ),
        "panels_cover_each_angular_domain": (
            len(panel_groups)
            == 2 * len(M5269.ENERGY_WITNESSES) * 4
            and max(coverage_residuals, default=math.inf)
            <= 1.0e-12
        ),
        "panel_midpoints_avoid_boundaries": (
            minimum_panel_margin >= MIDPOINT_MARGIN_MINIMUM
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
        "mode": "shared-angular-root-margin-boundary-localization",
        "checks": checks,
        "acceptance_passed": accepted,
        "descriptor_count": len(descriptors),
        "boundary_function_count": len(function_rows),
        "raw_boundary_count": len(boundary_rows),
        "merged_boundary_count": len(merged_rows),
        "panel_count": len(panels),
        "panel_group_count": len(panel_groups),
        "coarse_transition_count": len(coverage_rows),
        "coarse_transition_coverage_count": sum(
            bool(row["coarse_transition_explained"])
            for row in coverage_rows
        ),
        "newly_detected_boundary_count": (
            newly_detected_boundary_count
        ),
        "maximum_boundary_bracket_width": maximum_width,
        "maximum_boundary_root_margin": maximum_residual,
        "maximum_merged_coordinate_spread": maximum_merge_spread,
        "minimum_panel_midpoint_root_margin": minimum_panel_margin,
        "maximum_panel_coverage_residual": max(
            coverage_residuals, default=math.inf
        ),
        "boundary_law": {
            "definition": (
                "m_label(c)=log|z_label(c)| at the sourced "
                "relative-chamber midpoint"
            ),
            "boundary_condition": "m_label(c)=0",
            "inside_condition": "m_label(c)<0",
            "pair_cycle_condition": (
                "exactly one label in each representing pair has "
                "m_label<0"
            ),
            "component_cycle_condition": (
                "representative and reciprocal pair-cycle conditions "
                "both hold"
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
            "ADOPT_LOCALIZED_SHARED_ANGULAR_BOUNDARIES__"
            "CONTINUE_BOUNDARY_SURFACES_OVER_SOFT_ENERGY"
            if accepted
            else "REPAIR_SHARED_ANGULAR_BOUNDARY_LOCALIZATION"
        ),
        "claim_boundary": {
            "valid_for_shared_witness_energy_boundary_atlas": accepted,
            "valid_for_topology_uniform_witness_energy_panels": (
                accepted
            ),
            "valid_for_continuous_energy_boundary_surfaces": False,
            "valid_for_full_phase_space_coefficient": False,
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
            "reason": (
                "Angular boundaries are localized only at eight energy "
                "witnesses and four transverse angular nodes."
            ),
        },
    }
    write_csv(DESCRIPTORS, descriptors)
    write_csv(FUNCTION_SUMMARY, function_rows)
    write_csv(RAW_BOUNDARIES, boundary_rows)
    write_csv(MERGED_BOUNDARIES, merged_rows)
    write_csv(PANELS, panels)
    write_csv(COARSE_COVERAGE, coverage_rows)
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
    text = f"""# 5270 - Shared angular root-margin boundary localization

## Derived boundary law

Checkpoint 5269 showed that reciprocal root transport is path-independent but
causal cycle occupation changes across the angular plane. This checkpoint
replaces the boolean occupation jump by its continuous parent function.

For a labelled global root evaluated at the sourced relative-chamber midpoint,

`m_label(c) = log |z_label(c)|`.

The ownership boundary is exactly

`m_label(c) = 0`.

A representing pair is active when its two margins have opposite signs. A
material component is active when this condition holds for both its
representative and reciprocal pairs. The source crossing labels and chamber
midpoints are identical for E040 and E020, so this boundary geometry is shared
by both regulators.

## Localization

Every one of the 24 labelled root margins is scanned in both angular
directions, at eight soft-energy witnesses and four fixed values of the
transverse angle. All sign changes are bisected to bracket width at most
`{BOUNDARY_WIDTH_LIMIT:.1e}`.

- Boundary functions: `{int(result['boundary_function_count'])}`.
- Raw labelled boundaries: `{int(result['raw_boundary_count'])}`.
- Merged shared boundaries: `{int(result['merged_boundary_count'])}`.
- Topology-uniform panels: `{int(result['panel_count'])}`.
- Coarse checkpoint-5269 transitions explained: `{int(result['coarse_transition_coverage_count'])}/{int(result['coarse_transition_count'])}`.
- Additional labelled crossings exposed by dense scans: `{int(result['newly_detected_boundary_count'])}`.
- Maximum boundary bracket width: `{float(result['maximum_boundary_bracket_width']):.12g}`.
- Maximum root-margin residual: `{float(result['maximum_boundary_root_margin']):.12g}`.
- Maximum merged-coordinate spread: `{float(result['maximum_merged_coordinate_spread']):.12g}`.
- Maximum panel coverage residual: `{float(result['maximum_panel_coverage_residual']):.12g}`.

## Decision

`{result['decision']}`

Validation passed: `{str(validation_passed).lower()}`.

This accepts localized, topology-uniform angular panels at the eight witness
energies. It does not yet prove continuous boundary surfaces between those
energies and therefore does not yet authorize full angular cubature, a
phase-space coefficient, numeric UV value, local GR, or full MTS.

## Next derivation

Continue each merged boundary in soft energy using the same equation
`log|z_label|=0`, detect births/mergers, and construct three-dimensional
topology-uniform cells in `(x,c_soft,c_decay)`. Only then evaluate the
checkpoint-5268 energy-first rule on nested angular panels.

## Artifacts

- Runner: `{Path(__file__).resolve()}`
- Result: `{RESULT}`
- Root descriptors: `{DESCRIPTORS}`
- Raw boundaries: `{RAW_BOUNDARIES}`
- Merged boundaries: `{MERGED_BOUNDARIES}`
- Angular panels: `{PANELS}`
- Coarse-edge coverage: `{COARSE_COVERAGE}`
- Validation: `{VALIDATION}`
"""
    temporary = DOCUMENT.with_suffix(DOCUMENT.suffix + ".tmp")
    temporary.write_text(text, encoding="utf-8")
    os.replace(temporary, DOCUMENT)


def validate_outputs() -> dict[str, Any]:
    result = read_json(RESULT)
    parent = read_json(RESULT_5269)
    required_csvs = (
        DESCRIPTORS,
        FUNCTION_SUMMARY,
        RAW_BOUNDARIES,
        MERGED_BOUNDARIES,
        PANELS,
        COARSE_COVERAGE,
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
            "PARENT_5269_ACCEPTED",
            bool(parent["acceptance_passed"]),
            str(parent["decision"]),
        ),
        validation_gate(
            "LOCALIZATION_ACCEPTED",
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
            "ALL_COARSE_TRANSITIONS_EXPLAINED",
            int(result["coarse_transition_coverage_count"])
            == int(result["coarse_transition_count"]),
            (
                f"{result['coarse_transition_coverage_count']}/"
                f"{result['coarse_transition_count']}"
            ),
        ),
        validation_gate(
            "BOUNDARY_BRACKETS_TIGHT",
            (
                float(result["maximum_boundary_bracket_width"])
                <= BOUNDARY_WIDTH_LIMIT
                and float(result["maximum_boundary_root_margin"])
                <= BOUNDARY_RESIDUAL_LIMIT
            ),
            (
                f"width={result['maximum_boundary_bracket_width']}; "
                f"margin={result['maximum_boundary_root_margin']}"
            ),
        ),
        validation_gate(
            "PANELS_COVER_DOMAIN",
            float(result["maximum_panel_coverage_residual"])
            <= 1.0e-12,
            (
                "maximum residual="
                f"{result['maximum_panel_coverage_residual']}"
            ),
        ),
        validation_gate(
            "BOUNDARY_LAW_RECORDED",
            (
                result["boundary_law"]["boundary_condition"]
                == "m_label(c)=0"
                and bool(
                    result["boundary_law"]["regulator_independent"]
                )
            ),
            str(result["boundary_law"]),
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
            "VALIDATED_SHARED_ANGULAR_ROOT_MARGIN_BOUNDARIES"
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
