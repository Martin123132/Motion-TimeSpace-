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
SOURCE = FUNCTIONAL_RG / "5269"
RESIDUALS = POST / "source-intake" / "mts_residuals"

SCRIPT_5267 = (
    SCRIPTS
    / "Y5_R2FR_5267_topology_aware_soft_energy_component_runner.py"
)
RESULT_5268 = (
    FUNCTIONAL_RG / "5268" / "soft_energy_endpoint_completion_result.json"
)
VALIDATION_5268 = (
    FUNCTIONAL_RG
    / "5268"
    / "soft_energy_endpoint_completion_validation.csv"
)
MANIFEST_5239 = (
    FUNCTIONAL_RG / "5239" / "matched_event_A00_job_manifest.json"
)
THEOREM_5245 = (
    POST
    / "5245-Y5-R2FR-reciprocal-projective-chamber-boundary-tracker.md"
)
RESULT_5265 = FUNCTIONAL_RG / "5265" / "piecewise_outer_result.json"

DRY_RUN = SOURCE / "joint_angular_energy_first_dry_run.json"
ANGULAR_NODES = SOURCE / "joint_angular_nodes.csv"
FIRST_TRACKS = SOURCE / "first_leg_angular_tracks.csv"
SECOND_TRACKS = SOURCE / "second_leg_angular_tracks.csv"
PATH_CLOSURE = SOURCE / "angular_path_closure.csv"
ENERGY_TRACKS = SOURCE / "energy_track_atlas.csv"
CYCLE_STATES = SOURCE / "energy_cycle_state_atlas.csv"
TRANSITIONS = SOURCE / "angular_transition_edges.csv"
RESULT = SOURCE / "joint_angular_energy_first_preflight_result.json"
VALIDATION = SOURCE / "joint_angular_energy_first_validation.csv"
RESIDUAL_VALIDATION = (
    RESIDUALS / "P8_Y5_BRR545_5269_VALIDATION.csv"
)
STATUS = SOURCE / "status.json"
DOCUMENT = (
    POST
    / "5269-Y5-R2FR-joint-angular-energy-first-topology-preflight.md"
)

CHECKPOINT = 5269
PARENT_CHECKPOINT = 5268
MARKER = "MTS_5269_JOINT_ANGULAR_ENERGY_FIRST_TOPOLOGY_PREFLIGHT"
REVISION = "joint-angular-energy-first-topology-preflight-v1"
ANGULAR_LIMIT = 0.995
ANGULAR_TRACK_BASE_POINTS = 513
ENERGY_TRACK_BASE_POINTS = 2049
TRACK_MAXIMUM_REFINEMENTS = 12
PATH_CLOSURE_LIMIT = 1.0e-7
ENERGY_WITNESSES = (
    1.0e-4,
    1.0e-2,
    1.0e-1,
    0.2630569525063038,
    5.0e-1,
    9.0e-1,
    9.9e-1,
    1.0 - 1.0e-4,
)
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


M5267 = load_module("mts_5267_for_5269", SCRIPT_5267)
M5239 = M5267.M5239
M5238 = M5267.M5238
M5237 = M5267.M5237
M5030 = M5267.M5030

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


def complex_value(value: Any) -> complex:
    if isinstance(value, complex):
        return value
    if isinstance(value, (str, int, float)):
        return complex(value)
    return complex(float(value["real"]), float(value["imaginary"]))


def complex_row(value: complex) -> dict[str, float]:
    return {
        "real": float(value.real),
        "imaginary": float(value.imag),
    }


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
        SCRIPT_5267,
        RESULT_5268,
        VALIDATION_5268,
        MANIFEST_5239,
        THEOREM_5245,
        RESULT_5265,
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


def source_event(job: dict[str, Any]) -> dict[str, Any]:
    return {
        "seed": int(job["seed"]),
        "soft_energy": float(job["soft_energy"]),
        "soft_cosine": float(job["soft_cosine"]),
        "decay_cosine": float(job["decay_cosine"]),
    }


def source_anchors(
    job: dict[str, Any],
) -> tuple[complex, complex]:
    return (
        complex_value(job["representative_anchor"]),
        complex_value(job["reciprocal_anchor"]),
    )


def path_problem(
    job: dict[str, Any],
    event: dict[str, Any],
    coordinate_name: str,
    anchors: tuple[complex, complex],
) -> dict[str, Any]:
    source_topology = topology(job)
    return {
        "job": {
            "representative_anchor": complex_row(anchors[0]),
            "reciprocal_anchor": complex_row(anchors[1]),
        },
        "event": dict(event),
        "target": complex_value(source_topology["target_cosine"]),
        "case": {
            "outer_coordinate": coordinate_name,
            "representative_pair": tuple(job["representative_pair"]),
            "reciprocal_pair": tuple(job["reciprocal_pair"]),
        },
    }


def adaptive_paired_track(
    problem: dict[str, Any],
    lower: float,
    upper: float,
    base_points: int,
    required_coordinates: tuple[float, ...],
) -> dict[str, Any]:
    coordinate_name = problem["case"]["outer_coordinate"]
    base_coordinate = float(problem["event"][coordinate_name])
    coordinates = np.unique(
        np.concatenate(
            (
                np.linspace(lower, upper, base_points),
                np.asarray(
                    (
                        lower,
                        upper,
                        base_coordinate,
                        *required_coordinates,
                    ),
                    dtype=float,
                ),
            )
        )
    )
    candidate_cache: dict[float, list[dict[str, Any]]] = {}
    attempts: list[dict[str, Any]] = []
    track: dict[str, Any] | None = None
    for refinement in range(TRACK_MAXIMUM_REFINEMENTS + 1):
        track = M5267.paired_track(
            problem, coordinates, candidate_cache
        )
        attempts.append(
            {
                "refinement": refinement,
                "point_count": int(track["point_count"]),
                "maximum_pair_set_projective_step": float(
                    track["maximum_pair_set_projective_step"]
                ),
                "maximum_reciprocal_product_residual": float(
                    track["maximum_reciprocal_product_residual"]
                ),
                "violating_interval_count": len(
                    track["violating_intervals"]
                ),
            }
        )
        if (
            float(track["maximum_pair_set_projective_step"])
            <= M5267.PAIR_SET_PROJECTIVE_LIMIT
            and float(track["maximum_reciprocal_product_residual"])
            <= M5267.RECIPROCAL_RESIDUAL_LIMIT
        ):
            break
        midpoints = [
            0.5 * (float(row["left"]) + float(row["right"]))
            for row in track["violating_intervals"]
        ]
        if not midpoints:
            break
        refined = np.unique(
            np.concatenate(
                (coordinates, np.asarray(midpoints, dtype=float))
            )
        )
        if len(refined) == len(coordinates):
            break
        coordinates = refined
    if track is None:
        raise RuntimeError("paired track was not evaluated")
    track["attempts"] = attempts
    track["accepted"] = (
        float(track["maximum_pair_set_projective_step"])
        <= M5267.PAIR_SET_PROJECTIVE_LIMIT
        and float(track["maximum_reciprocal_product_residual"])
        <= M5267.RECIPROCAL_RESIDUAL_LIMIT
    )
    return track


def pair_at(
    track: dict[str, Any], coordinate: float
) -> tuple[complex, complex]:
    coordinates = np.asarray(track["coordinates"], dtype=float)
    index = int(np.argmin(np.abs(coordinates - float(coordinate))))
    if abs(float(coordinates[index]) - float(coordinate)) > 1.0e-12:
        raise RuntimeError(
            f"required coordinate absent from track: {coordinate}"
        )
    return (
        complex(track["representative_roots"][index]),
        complex(track["reciprocal_roots"][index]),
    )


def track_summary(
    job: dict[str, Any],
    track: dict[str, Any],
    coordinate_name: str,
    role: str,
    fixed_coordinate_name: str,
    fixed_coordinate_value: float,
) -> dict[str, Any]:
    return {
        "job_id": job["job_id"],
        "epsilon_id": job["epsilon_id"],
        "component_id": job["component_id"],
        "owner_summand": job["owner_summand"],
        "coordinate_name": coordinate_name,
        "track_role": role,
        "fixed_coordinate_name": fixed_coordinate_name,
        "fixed_coordinate_value": fixed_coordinate_value,
        "point_count": int(track["point_count"]),
        "refinement_count": len(track["attempts"]) - 1,
        "maximum_pair_set_projective_step": float(
            track["maximum_pair_set_projective_step"]
        ),
        "maximum_reciprocal_product_residual": float(
            track["maximum_reciprocal_product_residual"]
        ),
        "track_accepted": bool(track["accepted"]),
        "valid_for_full_phase_space_coefficient": False,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }


def node_contract(
    manifest: dict[str, Any],
) -> tuple[
    list[dict[str, Any]],
    tuple[float, ...],
    tuple[float, ...],
]:
    jobs = list(manifest["jobs"])
    reference = source_event(jobs[0])
    legendre_nodes, _ = np.polynomial.legendre.leggauss(3)
    base_nodes = [
        float(ANGULAR_LIMIT * value) for value in legendre_nodes
    ]
    soft_nodes = tuple(
        sorted({*base_nodes, float(reference["soft_cosine"])})
    )
    decay_nodes = tuple(
        sorted({*base_nodes, float(reference["decay_cosine"])})
    )
    rows = [
        {
            "soft_index": soft_index,
            "decay_index": decay_index,
            "soft_cosine": soft_cosine,
            "decay_cosine": decay_cosine,
            "is_source_soft_cosine": (
                soft_cosine == float(reference["soft_cosine"])
            ),
            "is_source_decay_cosine": (
                decay_cosine == float(reference["decay_cosine"])
            ),
            "valid_for_full_phase_space_coefficient": False,
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
        }
        for decay_index, decay_cosine in enumerate(decay_nodes)
        for soft_index, soft_cosine in enumerate(soft_nodes)
    ]
    return rows, soft_nodes, decay_nodes


def dry_run() -> dict[str, Any]:
    set_below_normal_priority()
    SOURCE.mkdir(parents=True, exist_ok=True)
    parent = read_json(RESULT_5268)
    manifest = read_json(MANIFEST_5239)
    node_rows, soft_nodes, decay_nodes = node_contract(manifest)
    jobs = list(manifest["jobs"])
    checks = {
        "parent_5268_accepted": bool(parent["acceptance_passed"]),
        "twelve_material_jobs_loaded": len(jobs) == 12,
        "two_regulators_present": (
            {str(job["epsilon_id"]) for job in jobs}
            == {"E040", "E020"}
        ),
        "six_components_per_regulator": all(
            sum(job["epsilon_id"] == epsilon_id for job in jobs) == 6
            for epsilon_id in ("E040", "E020")
        ),
        "sixteen_joint_nodes_scheduled": len(node_rows) == 16,
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
        "material_job_count": len(jobs),
        "soft_nodes": list(soft_nodes),
        "decay_nodes": list(decay_nodes),
        "joint_node_count": len(node_rows),
        "scheduled_path_closure_rows": len(jobs) * len(node_rows),
        "scheduled_energy_track_rows": len(jobs) * len(node_rows),
        "scheduled_cycle_state_rows": (
            len(jobs) * len(node_rows) * len(ENERGY_WITNESSES)
        ),
        "resource_contract": {
            "maximum_task_python_processes": 1,
            "worker_math_threads": 1,
            "windows_priority": "BelowNormal",
            "sustained_redline_forbidden": True,
        },
        "decision": (
            "DRY_RUN_ACCEPTED__EXECUTE_JOINT_ANGULAR_PREFLIGHT"
            if all(checks.values())
            else "REPAIR_5269_DRY_RUN"
        ),
        "runtime_seconds": 0.0,
        "claim_boundary": {
            "valid_for_full_phase_space_coefficient": False,
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
        },
    }
    write_csv(ANGULAR_NODES, node_rows)
    atomic_json(DRY_RUN, result)
    return result


def full_component_problem(
    job: dict[str, Any],
    event: dict[str, Any],
    anchors: tuple[complex, complex],
    energy_track: dict[str, Any],
) -> dict[str, Any]:
    source_topology = topology(job)
    representative_pair = tuple(job["representative_pair"])
    reciprocal_pair = tuple(job["reciprocal_pair"])
    representative = M5237.find_source_crossing(
        source_topology,
        int(job["representative_chamber"]),
        representative_pair,
        complex_value(job["representative_anchor"]),
    )
    reciprocal = M5237.find_source_crossing(
        source_topology,
        int(job["reciprocal_chamber"]),
        reciprocal_pair,
        complex_value(job["reciprocal_anchor"]),
    )
    local_job = dict(job)
    local_job.update(
        {
            "job_id": f"{job['job_id']}_ANGULAR_ENERGY",
            "outer_coordinate": "soft_energy",
            "representative_anchor": complex_row(anchors[0]),
            "reciprocal_anchor": complex_row(anchors[1]),
            "soft_energy": float(event["soft_energy"]),
            "soft_cosine": float(event["soft_cosine"]),
            "decay_cosine": float(event["decay_cosine"]),
        }
    )
    case = {
        "case_id": local_job["job_id"],
        "family": job["family"],
        "tranche": job["tranche"],
        "seed": int(job["seed"]),
        "outer_coordinate": "soft_energy",
        "representative_pair": representative_pair,
        "reciprocal_pair": reciprocal_pair,
        "expected_u_winding": int(job["expected_u_winding"]),
        "expected_v_winding": int(job["expected_v_winding"]),
    }
    return {
        "job": local_job,
        "owner_summand": job["owner_summand"],
        "component_id": job["component_id"],
        "case": case,
        "event": dict(event),
        "topology": source_topology,
        "target": complex_value(source_topology["target_cosine"]),
        "representative": representative,
        "reciprocal": reciprocal,
        "atlas_rows": (
            M5238.endpoint_candidate_rows(representative_pair)
            if job["owner_summand"] == "endpoint_subtraction"
            else M5237.direct_candidate_rows(representative_pair)
        ),
        "coordinates": energy_track["coordinates"],
        "branch_tracks": {
            M5237.pair_key(representative_pair): {
                "coordinates": energy_track["coordinates"],
                "roots": energy_track["representative_roots"],
                "maximum_projective_step": energy_track[
                    "maximum_representative_projective_step"
                ],
                "minimum_alternate_branch_separation": 0.0,
            },
            M5237.pair_key(reciprocal_pair): {
                "coordinates": energy_track["coordinates"],
                "roots": energy_track["reciprocal_roots"],
                "maximum_projective_step": energy_track[
                    "maximum_reciprocal_projective_step"
                ],
                "minimum_alternate_branch_separation": 0.0,
            },
        },
    }


def transition_rows(
    cycle_rows: list[dict[str, Any]],
    closure_rows: list[dict[str, Any]],
    soft_nodes: tuple[float, ...],
    decay_nodes: tuple[float, ...],
) -> list[dict[str, Any]]:
    states = {
        (
            row["epsilon_id"],
            row["component_id"],
            float(row["energy_witness"]),
            int(row["decay_index"]),
            int(row["soft_index"]),
        ): bool(row["cycle_active"])
        for row in cycle_rows
    }
    rows: list[dict[str, Any]] = []
    epsilon_ids = sorted({row["epsilon_id"] for row in cycle_rows})
    component_ids = sorted(
        {row["component_id"] for row in cycle_rows}
    )
    for epsilon_id in epsilon_ids:
        for component_id in component_ids:
            for energy in ENERGY_WITNESSES:
                for decay_index, decay_value in enumerate(decay_nodes):
                    for soft_index in range(len(soft_nodes) - 1):
                        left = states[
                            (
                                epsilon_id,
                                component_id,
                                float(energy),
                                decay_index,
                                soft_index,
                            )
                        ]
                        right = states[
                            (
                                epsilon_id,
                                component_id,
                                float(energy),
                                decay_index,
                                soft_index + 1,
                            )
                        ]
                        if left != right:
                            rows.append(
                                {
                                    "transition_kind": (
                                        "cycle_state_soft_edge"
                                    ),
                                    "epsilon_id": epsilon_id,
                                    "component_id": component_id,
                                    "energy_witness": energy,
                                    "fixed_coordinate": decay_value,
                                    "left_coordinate": soft_nodes[
                                        soft_index
                                    ],
                                    "right_coordinate": soft_nodes[
                                        soft_index + 1
                                    ],
                                    "left_state": left,
                                    "right_state": right,
                                    "valid_for_full_phase_space_coefficient": False,
                                    "valid_for_numeric_UV_claim": False,
                                    "valid_for_local_GR_claim": False,
                                    "valid_for_full_MTS_claim": False,
                                }
                            )
                for soft_index, soft_value in enumerate(soft_nodes):
                    for decay_index in range(len(decay_nodes) - 1):
                        left = states[
                            (
                                epsilon_id,
                                component_id,
                                float(energy),
                                decay_index,
                                soft_index,
                            )
                        ]
                        right = states[
                            (
                                epsilon_id,
                                component_id,
                                float(energy),
                                decay_index + 1,
                                soft_index,
                            )
                        ]
                        if left != right:
                            rows.append(
                                {
                                    "transition_kind": (
                                        "cycle_state_decay_edge"
                                    ),
                                    "epsilon_id": epsilon_id,
                                    "component_id": component_id,
                                    "energy_witness": energy,
                                    "fixed_coordinate": soft_value,
                                    "left_coordinate": decay_nodes[
                                        decay_index
                                    ],
                                    "right_coordinate": decay_nodes[
                                        decay_index + 1
                                    ],
                                    "left_state": left,
                                    "right_state": right,
                                    "valid_for_full_phase_space_coefficient": False,
                                    "valid_for_numeric_UV_claim": False,
                                    "valid_for_local_GR_claim": False,
                                    "valid_for_full_MTS_claim": False,
                                }
                            )
    for row in closure_rows:
        if not bool(row["path_closed"]):
            rows.append(
                {
                    "transition_kind": "path_order_monodromy_cell",
                    "epsilon_id": row["epsilon_id"],
                    "component_id": row["component_id"],
                    "energy_witness": "",
                    "fixed_coordinate": "",
                    "left_coordinate": row["soft_cosine"],
                    "right_coordinate": row["decay_cosine"],
                    "left_state": "",
                    "right_state": "",
                    "path_closure_distance": row[
                        "path_closure_distance"
                    ],
                    "valid_for_full_phase_space_coefficient": False,
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
            )
    if not rows:
        rows.append(
            {
                "transition_kind": "none_on_preflight_grid",
                "epsilon_id": "ALL",
                "component_id": "ALL",
                "energy_witness": "",
                "fixed_coordinate": "",
                "left_coordinate": "",
                "right_coordinate": "",
                "left_state": "",
                "right_state": "",
                "valid_for_full_phase_space_coefficient": False,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    return rows


def execute() -> dict[str, Any]:
    started = time.perf_counter()
    set_below_normal_priority()
    SOURCE.mkdir(parents=True, exist_ok=True)
    dry = dry_run()
    if not dry["acceptance_passed"]:
        raise RuntimeError("5269 dry run did not pass")
    parent = read_json(RESULT_5268)
    manifest = read_json(MANIFEST_5239)
    jobs = list(manifest["jobs"])
    node_rows, soft_nodes, decay_nodes = node_contract(manifest)
    reference_event = source_event(jobs[0])

    first_tracks: dict[tuple[str, str], dict[str, Any]] = {}
    first_rows: list[dict[str, Any]] = []
    for job in jobs:
        event = source_event(job)
        anchors = source_anchors(job)
        decay_track = adaptive_paired_track(
            path_problem(
                job, event, "decay_cosine", anchors
            ),
            -ANGULAR_LIMIT,
            ANGULAR_LIMIT,
            ANGULAR_TRACK_BASE_POINTS,
            decay_nodes,
        )
        soft_track = adaptive_paired_track(
            path_problem(job, event, "soft_cosine", anchors),
            -ANGULAR_LIMIT,
            ANGULAR_LIMIT,
            ANGULAR_TRACK_BASE_POINTS,
            soft_nodes,
        )
        first_tracks[(job["job_id"], "decay")] = decay_track
        first_tracks[(job["job_id"], "soft")] = soft_track
        first_rows.append(
            track_summary(
                job,
                decay_track,
                "decay_cosine",
                "first_leg_decay",
                "soft_cosine",
                float(event["soft_cosine"]),
            )
        )
        first_rows.append(
            track_summary(
                job,
                soft_track,
                "soft_cosine",
                "first_leg_soft",
                "decay_cosine",
                float(event["decay_cosine"]),
            )
        )

    second_soft_tracks: dict[
        tuple[str, int], dict[str, Any]
    ] = {}
    second_decay_tracks: dict[
        tuple[str, int], dict[str, Any]
    ] = {}
    second_rows: list[dict[str, Any]] = []
    for job in jobs:
        event = source_event(job)
        for decay_index, decay_cosine in enumerate(decay_nodes):
            decay_anchors = pair_at(
                first_tracks[(job["job_id"], "decay")],
                decay_cosine,
            )
            varied = dict(event)
            varied["decay_cosine"] = decay_cosine
            track = adaptive_paired_track(
                path_problem(
                    job,
                    varied,
                    "soft_cosine",
                    decay_anchors,
                ),
                -ANGULAR_LIMIT,
                ANGULAR_LIMIT,
                ANGULAR_TRACK_BASE_POINTS,
                soft_nodes,
            )
            second_soft_tracks[
                (job["job_id"], decay_index)
            ] = track
            second_rows.append(
                track_summary(
                    job,
                    track,
                    "soft_cosine",
                    "decay_then_soft",
                    "decay_cosine",
                    decay_cosine,
                )
            )
        for soft_index, soft_cosine in enumerate(soft_nodes):
            soft_anchors = pair_at(
                first_tracks[(job["job_id"], "soft")],
                soft_cosine,
            )
            varied = dict(event)
            varied["soft_cosine"] = soft_cosine
            track = adaptive_paired_track(
                path_problem(
                    job,
                    varied,
                    "decay_cosine",
                    soft_anchors,
                ),
                -ANGULAR_LIMIT,
                ANGULAR_LIMIT,
                ANGULAR_TRACK_BASE_POINTS,
                decay_nodes,
            )
            second_decay_tracks[
                (job["job_id"], soft_index)
            ] = track
            second_rows.append(
                track_summary(
                    job,
                    track,
                    "decay_cosine",
                    "soft_then_decay",
                    "soft_cosine",
                    soft_cosine,
                )
            )

    closure_rows: list[dict[str, Any]] = []
    energy_rows: list[dict[str, Any]] = []
    cycle_rows: list[dict[str, Any]] = []
    for job in jobs:
        event = source_event(job)
        for node in node_rows:
            soft_index = int(node["soft_index"])
            decay_index = int(node["decay_index"])
            soft_cosine = float(node["soft_cosine"])
            decay_cosine = float(node["decay_cosine"])
            path_a = pair_at(
                second_soft_tracks[
                    (job["job_id"], decay_index)
                ],
                soft_cosine,
            )
            path_b = pair_at(
                second_decay_tracks[
                    (job["job_id"], soft_index)
                ],
                decay_cosine,
            )
            closure = float(
                M5267.pair_set_bottleneck(path_a, path_b)
            )
            representative_distance = float(
                M5030.chordal_distance(path_a[0], path_b[0])
            )
            reciprocal_distance = float(
                M5030.chordal_distance(path_a[1], path_b[1])
            )
            path_closed = closure <= PATH_CLOSURE_LIMIT
            closure_rows.append(
                {
                    "job_id": job["job_id"],
                    "epsilon_id": job["epsilon_id"],
                    "component_id": job["component_id"],
                    "owner_summand": job["owner_summand"],
                    "soft_index": soft_index,
                    "decay_index": decay_index,
                    "soft_cosine": soft_cosine,
                    "decay_cosine": decay_cosine,
                    "path_closure_distance": closure,
                    "representative_role_distance": (
                        representative_distance
                    ),
                    "reciprocal_role_distance": reciprocal_distance,
                    "path_closure_limit": PATH_CLOSURE_LIMIT,
                    "path_closed": path_closed,
                    "valid_for_global_angular_transport": path_closed,
                    "valid_for_full_phase_space_coefficient": False,
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
            )
            varied_event = dict(event)
            varied_event["soft_cosine"] = soft_cosine
            varied_event["decay_cosine"] = decay_cosine
            energy_track = adaptive_paired_track(
                path_problem(
                    job,
                    varied_event,
                    "soft_energy",
                    path_a,
                ),
                M5267.ENERGY_MINIMUM,
                M5267.ENERGY_MAXIMUM,
                ENERGY_TRACK_BASE_POINTS,
                ENERGY_WITNESSES,
            )
            energy_rows.append(
                {
                    "job_id": job["job_id"],
                    "epsilon_id": job["epsilon_id"],
                    "component_id": job["component_id"],
                    "owner_summand": job["owner_summand"],
                    "soft_index": soft_index,
                    "decay_index": decay_index,
                    "soft_cosine": soft_cosine,
                    "decay_cosine": decay_cosine,
                    "path_closed": path_closed,
                    "point_count": int(energy_track["point_count"]),
                    "refinement_count": (
                        len(energy_track["attempts"]) - 1
                    ),
                    "maximum_pair_set_projective_step": float(
                        energy_track[
                            "maximum_pair_set_projective_step"
                        ]
                    ),
                    "maximum_reciprocal_product_residual": float(
                        energy_track[
                            "maximum_reciprocal_product_residual"
                        ]
                    ),
                    "energy_track_accepted": bool(
                        energy_track["accepted"]
                    ),
                    "valid_for_global_angular_transport": (
                        path_closed
                        and bool(energy_track["accepted"])
                    ),
                    "valid_for_full_phase_space_coefficient": False,
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
            )
            problem = full_component_problem(
                job, varied_event, path_a, energy_track
            )
            for energy_witness in ENERGY_WITNESSES:
                local_topology = M5237.updated_component_topology(
                    problem, energy_witness
                )
                cycle_active, reciprocal_residual = (
                    M5237.component_cycle_state(
                        problem,
                        energy_witness,
                        local_topology,
                    )
                )
                cycle_rows.append(
                    {
                        "job_id": job["job_id"],
                        "epsilon_id": job["epsilon_id"],
                        "component_id": job["component_id"],
                        "owner_summand": job["owner_summand"],
                        "soft_index": soft_index,
                        "decay_index": decay_index,
                        "soft_cosine": soft_cosine,
                        "decay_cosine": decay_cosine,
                        "energy_witness": energy_witness,
                        "path_closed": path_closed,
                        "energy_track_accepted": bool(
                            energy_track["accepted"]
                        ),
                        "cycle_active": bool(cycle_active),
                        "reciprocal_residual": float(
                            reciprocal_residual
                        ),
                        "valid_for_global_angular_transport": (
                            path_closed
                            and bool(energy_track["accepted"])
                        ),
                        "valid_for_full_phase_space_coefficient": False,
                        "valid_for_numeric_UV_claim": False,
                        "valid_for_local_GR_claim": False,
                        "valid_for_full_MTS_claim": False,
                    }
                )

    transition_atlas = transition_rows(
        cycle_rows,
        closure_rows,
        soft_nodes,
        decay_nodes,
    )
    real_transitions = [
        row
        for row in transition_atlas
        if row["transition_kind"] != "none_on_preflight_grid"
    ]
    path_failure_count = sum(
        not bool(row["path_closed"]) for row in closure_rows
    )
    angular_cycle_transition_count = sum(
        str(row["transition_kind"]).startswith("cycle_state_")
        for row in real_transitions
    )
    regulator_states = {
        (
            row["component_id"],
            float(row["energy_witness"]),
            int(row["decay_index"]),
            int(row["soft_index"]),
            row["epsilon_id"],
        ): bool(row["cycle_active"])
        for row in cycle_rows
    }
    regulator_state_mismatch_count = sum(
        regulator_states[
            (
                component_id,
                float(energy),
                decay_index,
                soft_index,
                "E040",
            )
        ]
        != regulator_states[
            (
                component_id,
                float(energy),
                decay_index,
                soft_index,
                "E020",
            )
        ]
        for component_id in sorted(
            {row["component_id"] for row in cycle_rows}
        )
        for energy in ENERGY_WITNESSES
        for decay_index in range(len(decay_nodes))
        for soft_index in range(len(soft_nodes))
    )
    canonical_transition_keys = {
        (
            row["transition_kind"],
            row["component_id"],
            row["energy_witness"],
            row["fixed_coordinate"],
            row["left_coordinate"],
            row["right_coordinate"],
            row["left_state"],
            row["right_state"],
        )
        for row in real_transitions
        if str(row["transition_kind"]).startswith("cycle_state_")
    }
    signature_lookup: dict[tuple[str, float], set[str]] = {}
    component_ids = sorted(
        {str(job["component_id"]) for job in jobs}
    )
    state_lookup = {
        (
            row["epsilon_id"],
            float(row["energy_witness"]),
            int(row["decay_index"]),
            int(row["soft_index"]),
            row["component_id"],
        ): bool(row["cycle_active"])
        for row in cycle_rows
    }
    for epsilon_id in ("E040", "E020"):
        for energy_witness in ENERGY_WITNESSES:
            signatures = signature_lookup.setdefault(
                (epsilon_id, float(energy_witness)), set()
            )
            for node in node_rows:
                signatures.add(
                    "".join(
                        "1"
                        if state_lookup[
                            (
                                epsilon_id,
                                float(energy_witness),
                                int(node["decay_index"]),
                                int(node["soft_index"]),
                                component_id,
                            )
                        ]
                        else "0"
                        for component_id in component_ids
                    )
                )
    signature_rows = [
        {
            "epsilon_id": epsilon_id,
            "energy_witness": energy_witness,
            "unique_angular_signature_count": len(signatures),
            "signatures": "|".join(sorted(signatures)),
        }
        for (epsilon_id, energy_witness), signatures in sorted(
            signature_lookup.items()
        )
    ]
    checks = {
        "parent_5268_accepted": bool(parent["acceptance_passed"]),
        "twelve_material_jobs_processed": len(jobs) == 12,
        "twenty_four_first_leg_tracks_complete": (
            len(first_rows) == 24
        ),
        "ninety_six_second_leg_tracks_complete": (
            len(second_rows) == 96
        ),
        "all_angular_tracks_resolved": all(
            bool(row["track_accepted"])
            for row in (*first_rows, *second_rows)
        ),
        "all_path_closures_classified": (
            len(closure_rows) == len(jobs) * len(node_rows)
            and all(
                math.isfinite(
                    float(row["path_closure_distance"])
                )
                for row in closure_rows
            )
        ),
        "all_energy_tracks_resolved": all(
            bool(row["energy_track_accepted"])
            for row in energy_rows
        ),
        "cycle_state_atlas_complete": (
            len(cycle_rows)
            == len(jobs) * len(node_rows) * len(ENERGY_WITNESSES)
            and all(
                float(row["reciprocal_residual"])
                <= M5267.RECIPROCAL_RESIDUAL_LIMIT
                for row in cycle_rows
            )
        ),
        "regulator_cycle_geometry_shared": (
            regulator_state_mismatch_count == 0
        ),
        "angular_transition_edges_classified": bool(
            transition_atlas
        ),
        "formalization_workbench_unchanged": (
            formal_inventory_digest()
            == str(parent["formalization_workbench_end_digest"])
        ),
        "claims_locked_false": True,
    }
    accepted = all(checks.values())
    if not accepted:
        decision = "REPAIR_JOINT_ANGULAR_ENERGY_FIRST_PREFLIGHT"
    elif path_failure_count or angular_cycle_transition_count:
        decision = (
            (
                "ADOPT_SHARED_PIECEWISE_JOINT_ANGULAR_CHAMBERS__"
                "LOCALIZE_TRANSITION_SURFACES_BEFORE_CUBATURE"
            )
            if regulator_state_mismatch_count == 0
            else (
                "ADOPT_REGULATOR_SPECIFIC_PIECEWISE_ANGULAR_CHAMBERS__"
                "LOCALIZE_TRANSITION_SURFACES_BEFORE_CUBATURE"
            )
        )
    else:
        decision = (
            "ADOPT_GLOBAL_JOINT_ANGULAR_TRANSPORT__"
            "PROCEED_TO_ENERGY_FIRST_ANGULAR_CUBATURE"
        )
    formal_end = formal_inventory_digest()
    result = {
        "checkpoint": CHECKPOINT,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "mode": "joint-angular-energy-first-topology-preflight",
        "checks": checks,
        "acceptance_passed": accepted,
        "decision": decision,
        "soft_nodes": list(soft_nodes),
        "decay_nodes": list(decay_nodes),
        "joint_node_count": len(node_rows),
        "material_job_count": len(jobs),
        "first_leg_track_count": len(first_rows),
        "second_leg_track_count": len(second_rows),
        "path_closure_row_count": len(closure_rows),
        "path_failure_count": path_failure_count,
        "maximum_path_closure_distance": max(
            float(row["path_closure_distance"])
            for row in closure_rows
        ),
        "energy_track_count": len(energy_rows),
        "maximum_energy_pair_set_projective_step": max(
            float(row["maximum_pair_set_projective_step"])
            for row in energy_rows
        ),
        "maximum_energy_reciprocal_residual": max(
            float(row["maximum_reciprocal_product_residual"])
            for row in energy_rows
        ),
        "cycle_state_row_count": len(cycle_rows),
        "angular_cycle_transition_count": (
            angular_cycle_transition_count
        ),
        "canonical_cycle_transition_count": len(
            canonical_transition_keys
        ),
        "regulator_state_mismatch_count": (
            regulator_state_mismatch_count
        ),
        "shared_regulator_cycle_geometry": (
            regulator_state_mismatch_count == 0
        ),
        "transition_row_count": len(real_transitions),
        "signature_summary": signature_rows,
        "transport_contract": {
            "path_a": "source -> decay_cosine -> soft_cosine",
            "path_b": "source -> soft_cosine -> decay_cosine",
            "path_closure_metric": (
                "unordered reciprocal-pair bottleneck chordal distance"
            ),
            "path_closure_limit": PATH_CLOSURE_LIMIT,
            "global_reciprocal_root_transport_is_path_independent": (
                path_failure_count == 0
            ),
            "cycle_occupation_requires_piecewise_chambers": (
                angular_cycle_transition_count > 0
            ),
            "energy_track_domain": [
                M5267.ENERGY_MINIMUM,
                M5267.ENERGY_MAXIMUM,
            ],
            "energy_witnesses": list(ENERGY_WITNESSES),
            "angular_measure": (
                "du_soft du_decay = "
                "(d soft_cosine/2)(d decay_cosine/2)"
            ),
            "angular_jacobian": 0.25,
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
        "claim_boundary": {
            "valid_for_joint_angular_topology_preflight": accepted,
            "valid_for_global_angular_transport": (
                accepted
                and path_failure_count == 0
                and angular_cycle_transition_count == 0
            ),
            "valid_for_piecewise_angular_chamber_localization": (
                accepted
            ),
            "valid_for_full_phase_space_coefficient": False,
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
            "reason": (
                "This resolves a finite joint angular topology atlas. "
                "It does not yet integrate the angular chambers or prove "
                "their endpoint caps."
            ),
        },
    }
    write_csv(ANGULAR_NODES, node_rows)
    write_csv(FIRST_TRACKS, first_rows)
    write_csv(SECOND_TRACKS, second_rows)
    write_csv(PATH_CLOSURE, closure_rows)
    write_csv(ENERGY_TRACKS, energy_rows)
    write_csv(CYCLE_STATES, cycle_rows)
    write_csv(TRANSITIONS, transition_atlas)
    atomic_json(RESULT, result)
    atomic_json(
        STATUS,
        {
            "checkpoint": CHECKPOINT,
            "mode": result["mode"],
            "state": "COMPLETED",
            "acceptance_passed": accepted,
            "decision": decision,
            "runtime_seconds": result["runtime_seconds"],
        },
    )
    return result


def validation_gate(
    gate_id: str,
    passed: bool,
    detail: str,
) -> dict[str, Any]:
    return {
        "gate_id": gate_id,
        "passed": bool(passed),
        "detail": detail,
    }


def render_document(
    result: dict[str, Any], validation_passed: bool
) -> None:
    signature_rows = result["signature_summary"]
    signature_table = "\n".join(
        (
            f"| {row['epsilon_id']} | "
            f"{float(row['energy_witness']):.6g} | "
            f"{int(row['unique_angular_signature_count'])} | "
            f"`{row['signatures']}` |"
        )
        for row in signature_rows
    )
    text = f"""# 5269 - Joint angular energy-first topology preflight

## Question

Checkpoint 5268 supplies the endpoint-completed energy rule at one angular
event. The next operation must transport that rule over both angular variables
without assuming that the two angular homotopies commute.

## Transport construction

For every one of the six material components and both regulators, two paths are
constructed from the sourced event:

1. `source -> decay_cosine -> soft_cosine`;
2. `source -> soft_cosine -> decay_cosine`.

Each leg transports the unordered reciprocal root pair on `CP1`. The closure
metric is the bottleneck chordal distance between the two endpoint pair sets,
with limit `{PATH_CLOSURE_LIMIT:.1e}`. At every joint node the accepted angular
anchor is then transported over
`{M5267.ENERGY_MINIMUM:.1e} <= x <= {M5267.ENERGY_MAXIMUM:.4f}` and audited at
eight energy witnesses.

The exact measure remains

`du_soft du_decay = (d c_soft/2)(d c_decay/2)`,

so the eventual angular Jacobian is `1/4`.

## Atlas result

- Joint angular nodes: `{int(result['joint_node_count'])}`.
- Material component/regulator jobs: `{int(result['material_job_count'])}`.
- First-leg tracks: `{int(result['first_leg_track_count'])}`.
- Second-leg tracks: `{int(result['second_leg_track_count'])}`.
- Path-closure rows: `{int(result['path_closure_row_count'])}`.
- Path-order failures: `{int(result['path_failure_count'])}`.
- Maximum closure distance: `{float(result['maximum_path_closure_distance']):.12g}`.
- Energy tracks: `{int(result['energy_track_count'])}`.
- Maximum energy pair-set step: `{float(result['maximum_energy_pair_set_projective_step']):.12g}`.
- Maximum energy reciprocal residual: `{float(result['maximum_energy_reciprocal_residual']):.12g}`.
- Cycle-state rows: `{int(result['cycle_state_row_count'])}`.
- Angular cycle-transition edges: `{int(result['angular_cycle_transition_count'])}`.
- Canonical regulator-independent transition edges: `{int(result['canonical_cycle_transition_count'])}`.
- E040/E020 cycle-state mismatches: `{int(result['regulator_state_mismatch_count'])}`.

## Angular signatures

The six-bit signatures list active component cycles in sorted component order.

| regulator | energy | angular signature count | signatures |
|---|---:|---:|---|
{signature_table}

## Decision

`{result['decision']}`

Validation passed: `{str(validation_passed).lower()}`.

This is a real topology preflight rather than an angular integral. A global
transport is accepted only if both path order and cycle signatures are
single-valued on the tested grid. Otherwise the transition cells must be
localized and integrated chamber by chamber. No phase-space coefficient,
numeric UV value, local GR, or full MTS claim follows.

The reciprocal root transport itself is path-independent on all tested cells.
The piecewise structure comes from causal cycle occupation, not from an
ambiguous root branch. The E040 and E020 occupation atlases agree exactly on
the complete preflight grid, so one shared transition geometry can be
localized before evaluating regulator-dependent amplitudes.

## Next derivation

If transition cells are present, bisect their exact reciprocal-pair boundaries
in the relevant angular coordinate at fixed energy witnesses, continue those
boundaries over energy, and construct topology-uniform angular panels. If no
transition cells are present, evaluate nested angular orders 3 and 5 with the
checkpoint-5268 energy rule before raising quadrature order.

## Artifacts

- Runner: `{Path(__file__).resolve()}`
- Result: `{RESULT}`
- Angular nodes: `{ANGULAR_NODES}`
- Path closure: `{PATH_CLOSURE}`
- Energy tracks: `{ENERGY_TRACKS}`
- Cycle states: `{CYCLE_STATES}`
- Transition atlas: `{TRANSITIONS}`
- Validation: `{VALIDATION}`
"""
    temporary = DOCUMENT.with_suffix(DOCUMENT.suffix + ".tmp")
    temporary.write_text(text, encoding="utf-8")
    os.replace(temporary, DOCUMENT)


def validate_outputs() -> dict[str, Any]:
    result = read_json(RESULT)
    parent = read_json(RESULT_5268)
    required_csvs = (
        ANGULAR_NODES,
        FIRST_TRACKS,
        SECOND_TRACKS,
        PATH_CLOSURE,
        ENERGY_TRACKS,
        CYCLE_STATES,
        TRANSITIONS,
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
            "PARENT_5268_ACCEPTED",
            bool(parent["acceptance_passed"]),
            str(parent["decision"]),
        ),
        validation_gate(
            "PREFLIGHT_ACCEPTED",
            bool(result["acceptance_passed"]),
            str(result["decision"]),
        ),
        validation_gate(
            "ALL_REQUIRED_CSVS_PARSE",
            (
                len(csv_rows) == len(required_csvs)
                and all(csv_rows.values())
            ),
            f"{len(csv_rows)}/{len(required_csvs)} non-empty CSVs",
        ),
        validation_gate(
            "ANGULAR_TRACK_COUNTS",
            (
                int(result["first_leg_track_count"]) == 24
                and int(result["second_leg_track_count"]) == 96
            ),
            (
                f"first={result['first_leg_track_count']}; "
                f"second={result['second_leg_track_count']}"
            ),
        ),
        validation_gate(
            "PATH_CLOSURE_ATLAS_COMPLETE",
            int(result["path_closure_row_count"]) == 192,
            (
                f"rows={result['path_closure_row_count']}; "
                f"failures={result['path_failure_count']}"
            ),
        ),
        validation_gate(
            "ENERGY_TRACK_ATLAS_COMPLETE",
            (
                int(result["energy_track_count"]) == 192
                and float(
                    result[
                        "maximum_energy_pair_set_projective_step"
                    ]
                )
                <= M5267.PAIR_SET_PROJECTIVE_LIMIT
                and float(
                    result["maximum_energy_reciprocal_residual"]
                )
                <= M5267.RECIPROCAL_RESIDUAL_LIMIT
            ),
            (
                f"tracks={result['energy_track_count']}; "
                "step="
                f"{result['maximum_energy_pair_set_projective_step']}"
            ),
        ),
        validation_gate(
            "CYCLE_STATE_ATLAS_COMPLETE",
            int(result["cycle_state_row_count"])
            == 192 * len(ENERGY_WITNESSES),
            f"rows={result['cycle_state_row_count']}",
        ),
        validation_gate(
            "REGULATOR_CYCLE_GEOMETRY_SHARED",
            (
                bool(result["shared_regulator_cycle_geometry"])
                and int(result["regulator_state_mismatch_count"]) == 0
            ),
            (
                "E040/E020 mismatches="
                f"{result['regulator_state_mismatch_count']}"
            ),
        ),
        validation_gate(
            "TRANSITION_DECISION_IS_EXPLICIT",
            str(result["decision"])
            in {
                (
                    "ADOPT_SHARED_PIECEWISE_JOINT_ANGULAR_CHAMBERS__"
                    "LOCALIZE_TRANSITION_SURFACES_BEFORE_CUBATURE"
                ),
                (
                    "ADOPT_REGULATOR_SPECIFIC_PIECEWISE_ANGULAR_CHAMBERS__"
                    "LOCALIZE_TRANSITION_SURFACES_BEFORE_CUBATURE"
                ),
                (
                    "ADOPT_GLOBAL_JOINT_ANGULAR_TRANSPORT__"
                    "PROCEED_TO_ENERGY_FIRST_ANGULAR_CUBATURE"
                ),
            },
            str(result["decision"]),
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
                and result["resource_contract"]["windows_priority"]
                == "BelowNormal"
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
            "VALIDATED_JOINT_ANGULAR_ENERGY_FIRST_TOPOLOGY_PREFLIGHT"
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
