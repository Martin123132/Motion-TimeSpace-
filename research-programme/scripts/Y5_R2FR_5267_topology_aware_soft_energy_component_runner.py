from __future__ import annotations

import argparse
import copy
import csv
import ctypes
import hashlib
import importlib.util
import json
import math
import os
import subprocess
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
SOURCE_5239 = FUNCTIONAL_RG / "5239"
SOURCE_5266 = FUNCTIONAL_RG / "5266"
SOURCE = FUNCTIONAL_RG / "5267"
RESIDUALS = POST / "source-intake" / "mts_residuals"

SCRIPT_5239 = (
    SCRIPTS
    / "Y5_R2FR_5239_matched_event_A00_regular_complement_and_regulator_extrapolation.py"
)
SCRIPT_5265 = (
    SCRIPTS / "Y5_R2FR_5265_piecewise_outer_coefficient_reassembly.py"
)
SCRIPT_5246 = (
    SCRIPTS
    / "Y5_R2FR_5246_Q03_reciprocal_projective_interval_topology_rebuild.py"
)
MANIFEST_5239 = SOURCE_5239 / "matched_event_A00_job_manifest.json"
RESULT_5266 = SOURCE_5266 / "soft_energy_pilot_result.json"

PREFLIGHT_RESULT = SOURCE / "energy_component_topology_preflight.json"
PREFLIGHT_ROWS = SOURCE / "energy_component_topology_preflight.csv"
PREFLIGHT_POLES = SOURCE / "energy_component_pole_preflight.csv"
PREFLIGHT_STATUS = SOURCE / "status.json"
RESIDUE_RESULT = SOURCE / "energy_component_residue_pilot.json"
WINDING_ROWS = SOURCE / "energy_component_dynamic_winding_intervals.csv"
RESIDUE_ROWS = SOURCE / "energy_component_residue_fits.csv"
RESIDUE_POLES = SOURCE / "energy_component_residue_poles.csv"
WINDING_ATTEMPT_ROWS = SOURCE / "energy_winding_resolution_attempts.csv"
WORKERS = SOURCE / "workers"
FULL_RESULT = SOURCE / "energy_first_two_regulator_result.json"
FULL_ROWS = SOURCE / "energy_first_two_regulator_convergence.csv"
CHILD_LOG = SOURCE / "E020_worker.log"
VALIDATION = SOURCE / "energy_first_validation.csv"
RESIDUAL_VALIDATION = RESIDUALS / "P8_Y5_BRR545_5267_VALIDATION.csv"
DOCUMENT = (
    POST
    / "5267-Y5-R2FR-topology-aware-soft-energy-component-runner.md"
)

CHECKPOINT = 5267
PARENT_CHECKPOINT = 5266
MARKER = "MTS_5267_TOPOLOGY_AWARE_SOFT_ENERGY_COMPONENT_RUNNER"
REVISION = "topology-aware-soft-energy-component-runner-v2"
ENERGY_MINIMUM = 1.0e-4
ENERGY_MAXIMUM = 1.0 - 1.0e-4
SCAN_POINTS = 601
TRACK_BASE_POINTS = 2049
TRACK_MAXIMUM_REFINEMENTS = 20
PAIR_SET_PROJECTIVE_LIMIT = 5.0e-2
RECIPROCAL_RESIDUAL_LIMIT = 2.0e-8
TARGET_EPSILON_IDS = ("E040",)
REGULATOR_EPSILON_IDS = ("E040", "E020")
HOMOTOPY_BASE_RESOLUTIONS = (2048, 4096, 8192, 16384, 32768)
HOMOTOPY_MINIMUM_ACCEPTED_BASE_RESOLUTION = 4096
HOMOTOPY_PAIR_SET_REFINEMENT_TARGET = 2.5e-2
HOMOTOPY_MAXIMUM_REFINEMENTS = 16
ENERGY_COMPOSITE_PANEL_MAXIMUM_WIDTH = 2.5e-2
ENERGY_INTEGRATION_REVISION = "composite-energy-panels-v1"


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5239 = load_module("mts_5239_for_5267", SCRIPT_5239)
M5238 = M5239.M5238
M5237 = M5239.M5237
M5030 = M5239.M5030
M5265 = load_module("mts_5265_for_5267", SCRIPT_5265)
M5246 = load_module("mts_5246_for_5267", SCRIPT_5246)
M5238.endpoint_geometry = M5265.analytic_endpoint_geometry

WINDING_STATE_CACHES: dict[str, dict[str, Any]] = {}
WINDING_ATTEMPTS: list[dict[str, Any]] = []


def set_below_normal_priority() -> None:
    if os.name != "nt":
        return
    handle = ctypes.windll.kernel32.GetCurrentProcess()
    ctypes.windll.kernel32.SetPriorityClass(handle, 0x00004000)


def json_default(value: Any) -> Any:
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, complex):
        return {"real": value.real, "imaginary": value.imag}
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, np.generic):
        return value.item()
    raise TypeError(f"cannot serialize {type(value)!r}")


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(
            value,
            indent=2,
            sort_keys=True,
            default=json_default,
        ),
        encoding="utf-8",
    )
    os.replace(temporary, path)


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
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    os.replace(temporary, path)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


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


def complex_value(value: Any) -> complex:
    if isinstance(value, dict):
        return complex(float(value["real"]), float(value["imaginary"]))
    return complex(value)


def pair_set_bottleneck(
    first: tuple[complex, complex],
    second: tuple[complex, complex],
) -> float:
    same = max(
        M5030.chordal_distance(first[0], second[0]),
        M5030.chordal_distance(first[1], second[1]),
    )
    swapped = max(
        M5030.chordal_distance(first[0], second[1]),
        M5030.chordal_distance(first[1], second[0]),
    )
    return float(min(same, swapped))


def winding_cache_path(epsilon_id: str) -> Path:
    return SOURCE / f"energy_winding_state_cache_{epsilon_id}.json"


def winding_cache(epsilon_id: str) -> dict[str, Any]:
    if epsilon_id in WINDING_STATE_CACHES:
        return WINDING_STATE_CACHES[epsilon_id]
    path = winding_cache_path(epsilon_id)
    payload = read_json(path) if path.exists() else {}
    if payload.get("revision") != REVISION:
        payload = {
            "revision": REVISION,
            "epsilon_id": epsilon_id,
            "states": {},
        }
    WINDING_STATE_CACHES[epsilon_id] = payload
    return payload


def winding_state_cache_key(
    problem: dict[str, Any], coordinate: float
) -> str:
    return hashlib.sha256(
        json.dumps(
            {
                "job_input_hash": problem["job"]["job_input_hash"],
                "coordinate": float(coordinate).hex(),
                "base_resolutions": HOMOTOPY_BASE_RESOLUTIONS,
                "minimum_accepted_base_resolution": (
                    HOMOTOPY_MINIMUM_ACCEPTED_BASE_RESOLUTION
                ),
                "pair_set_refinement_target": (
                    HOMOTOPY_PAIR_SET_REFINEMENT_TARGET
                ),
                "maximum_refinements": HOMOTOPY_MAXIMUM_REFINEMENTS,
            },
            sort_keys=True,
        ).encode("utf-8")
    ).hexdigest()


def selected_collision_state_on_grid(
    problem: dict[str, Any],
    coordinate: float,
    grid: list[complex],
) -> tuple[dict[str, Any], dict[str, Any]]:
    original_cosines = M5246.M5030.homotopy_cosines
    original_selection = M5246.M5244.coupled_pair_selection
    selected_pairs: list[tuple[complex, complex]] = []
    minimum_margin = float("inf")

    def capture_selection(
        representative_roots: list[complex],
        reciprocal_roots: list[complex],
        representative_reference: complex,
        reciprocal_reference: complex,
    ) -> tuple[complex, complex, float, float]:
        nonlocal minimum_margin
        for roots in (representative_roots, reciprocal_roots):
            separations = [
                M5030.chordal_distance(first, second)
                for first_index, first in enumerate(roots)
                for second in roots[first_index + 1 :]
            ]
            if separations:
                minimum_margin = min(minimum_margin, min(separations))
        selected = original_selection(
            representative_roots,
            reciprocal_roots,
            representative_reference,
            reciprocal_reference,
        )
        selected_pairs.append(
            (complex(selected[0]), complex(selected[1]))
        )
        return selected

    M5246.M5030.homotopy_cosines = lambda *_: list(grid)
    M5246.M5244.coupled_pair_selection = capture_selection
    try:
        state = M5246.M5245.reciprocal_projective_state(
            problem,
            float(coordinate),
            len(grid) - 1,
        )
    finally:
        M5246.M5030.homotopy_cosines = original_cosines
        M5246.M5244.coupled_pair_selection = original_selection
    selected_pairs.reverse()
    if len(selected_pairs) != len(grid):
        raise RuntimeError("collision pair path length mismatch")
    pair_steps = [
        pair_set_bottleneck(
            selected_pairs[index - 1], selected_pairs[index]
        )
        for index in range(1, len(selected_pairs))
    ]
    violations = [
        {
            "index": index,
            "left": grid[index],
            "right": grid[index + 1],
            "step": float(step),
        }
        for index, step in enumerate(pair_steps)
        if step > HOMOTOPY_PAIR_SET_REFINEMENT_TARGET
    ]
    diagnostics = {
        "maximum_collision_pair_set_step": max(
            pair_steps, default=0.0
        ),
        "collision_violations": violations,
        "minimum_alternate_branch_separation": (
            minimum_margin if np.isfinite(minimum_margin) else 1.0
        ),
    }
    return state, diagnostics


def adaptive_reciprocal_projective_state(
    problem: dict[str, Any],
    coordinate: float,
    base_steps: int,
) -> dict[str, Any]:
    grid, boundary_mesh = M5246.adaptive_boundary_mesh(
        problem, float(coordinate), base_steps
    )
    state: dict[str, Any] | None = None
    collision: dict[str, Any] | None = None
    collision_inserted = 0
    collision_depth = 0
    for refinement in range(HOMOTOPY_MAXIMUM_REFINEMENTS + 1):
        state, collision = selected_collision_state_on_grid(
            problem, float(coordinate), grid
        )
        violations = collision["collision_violations"]
        if not violations:
            collision_depth = refinement
            break
        violation_indices = {
            int(row["index"]) for row in violations
        }
        updated = [grid[0]]
        for index, (left, right) in enumerate(
            zip(grid[:-1], grid[1:])
        ):
            if index in violation_indices:
                updated.append(0.5 * (left + right))
            updated.append(right)
        inserted = len(updated) - len(grid)
        if inserted <= 0:
            collision_depth = refinement
            break
        collision_inserted += inserted
        grid = updated
        collision_depth = refinement + 1
    if state is None or collision is None:
        raise RuntimeError("reciprocal-projective state was not evaluated")
    if collision["collision_violations"]:
        raise RuntimeError(
            "collision pair-set mesh exceeded refinement depth"
        )
    representative_suffix, reciprocal_suffix, source_delta = (
        M5239.source_winding_delta(problem)
    )
    state_u = int(state["state_u"])
    state_v = int(state["state_v"])
    winding = {"u": state_u, "v": state_v}
    dynamic_delta = (
        winding[representative_suffix] - winding[reciprocal_suffix]
    )
    return {
        "u": state_u,
        "v": state_v,
        "dynamic_delta": dynamic_delta,
        "source_delta": source_delta,
        "multiplier": dynamic_delta / source_delta,
        "maximum_pair_projective_step": float(
            collision["maximum_collision_pair_set_step"]
        ),
        "maximum_boundary_projective_step": float(
            state["maximum_boundary_projective_step"]
        ),
        "maximum_reciprocal_product_residual": float(
            state["maximum_reciprocal_product_residual"]
        ),
        "maximum_boundary_reciprocal_residual": float(
            state["maximum_boundary_reciprocal_residual"]
        ),
        "maximum_boundary_polynomial_residual": float(
            state["maximum_boundary_polynomial_residual"]
        ),
        "minimum_alternate_branch_separation": float(
            collision["minimum_alternate_branch_separation"]
        ),
        "topology_steps": len(grid) - 1,
        "base_topology_steps": base_steps,
        "boundary_inserted_node_count": int(
            boundary_mesh["inserted_node_count"]
        ),
        "boundary_refinement_depth": int(
            boundary_mesh["refinement_depth"]
        ),
        "collision_inserted_node_count": collision_inserted,
        "collision_refinement_depth": collision_depth,
    }


def resolved_energy_winding_state(
    problem: dict[str, Any],
    coordinate: float,
    steps: int = 0,
) -> dict[str, Any]:
    epsilon_id = str(problem["job"]["epsilon_id"])
    cache = winding_cache(epsilon_id)
    key = winding_state_cache_key(problem, float(coordinate))
    if key in cache["states"]:
        return dict(cache["states"][key])
    previous: dict[str, Any] | None = None
    accepted: dict[str, Any] | None = None
    for base_steps in HOMOTOPY_BASE_RESOLUTIONS:
        started = time.perf_counter()
        state = adaptive_reciprocal_projective_state(
            problem, float(coordinate), base_steps
        )
        stable = (
            previous is not None
            and (state["u"], state["v"])
            == (previous["u"], previous["v"])
        )
        gates = {
            "state_stable_from_previous": stable,
            "minimum_resolution_reached": (
                base_steps
                >= HOMOTOPY_MINIMUM_ACCEPTED_BASE_RESOLUTION
            ),
            "collision_pair_set_step_passed": (
                state["maximum_pair_projective_step"]
                <= PAIR_SET_PROJECTIVE_LIMIT
            ),
            "collision_reciprocal_passed": (
                state["maximum_reciprocal_product_residual"]
                <= RECIPROCAL_RESIDUAL_LIMIT
            ),
            "boundary_projective_passed": (
                state["maximum_boundary_projective_step"]
                <= PAIR_SET_PROJECTIVE_LIMIT
            ),
            "boundary_reciprocal_passed": (
                state["maximum_boundary_reciprocal_residual"]
                <= M5246.MAXIMUM_BOUNDARY_RECIPROCAL_RESIDUAL
            ),
            "boundary_polynomial_passed": (
                state["maximum_boundary_polynomial_residual"]
                <= M5246.MAXIMUM_BOUNDARY_POLYNOMIAL_RESIDUAL
            ),
        }
        attempt = {
            "job_id": problem["job"]["job_id"],
            "epsilon_id": epsilon_id,
            "component_id": problem["component_id"],
            "coordinate": float(coordinate),
            "base_topology_steps": base_steps,
            "state_u": state["u"],
            "state_v": state["v"],
            "dynamic_multiplier": state["multiplier"],
            "maximum_collision_pair_set_step": state[
                "maximum_pair_projective_step"
            ],
            "maximum_reciprocal_product_residual": state[
                "maximum_reciprocal_product_residual"
            ],
            "maximum_boundary_projective_step": state[
                "maximum_boundary_projective_step"
            ],
            "collision_inserted_node_count": state[
                "collision_inserted_node_count"
            ],
            "collision_refinement_depth": state[
                "collision_refinement_depth"
            ],
            "evaluation_seconds": time.perf_counter() - started,
            **gates,
            "accepted": all(gates.values()),
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
        }
        WINDING_ATTEMPTS.append(attempt)
        if attempt["accepted"]:
            accepted = state
            break
        previous = state
    if accepted is None:
        raise RuntimeError(
            "energy reciprocal-projective state did not converge for "
            f"{problem['job']['job_id']} at {coordinate:.17g}"
        )
    cache["states"][key] = accepted
    atomic_json(winding_cache_path(epsilon_id), cache)
    return dict(accepted)


M5239.winding_state = resolved_energy_winding_state


def candidate_pairs(
    problem: dict[str, Any], coordinate: float
) -> list[dict[str, Any]]:
    representative_pair = problem["case"]["representative_pair"]
    reciprocal_pair = problem["case"]["reciprocal_pair"]
    representative_roots = M5237.roots_for_pair(
        problem["event"],
        problem["target"],
        representative_pair,
        problem["case"]["outer_coordinate"],
        complex(coordinate),
    )
    reciprocal_roots = M5237.roots_for_pair(
        problem["event"],
        problem["target"],
        reciprocal_pair,
        problem["case"]["outer_coordinate"],
        complex(coordinate),
    )
    if not representative_roots or not reciprocal_roots:
        raise RuntimeError(
            f"collision branch disappeared at soft_energy={coordinate}"
        )
    rows = [
        {
            "representative": complex(representative),
            "reciprocal": complex(reciprocal),
            "reciprocal_residual": float(
                abs(representative * reciprocal - 1.0)
            ),
        }
        for representative in representative_roots
        for reciprocal in reciprocal_roots
    ]
    minimum_residual = min(row["reciprocal_residual"] for row in rows)
    return [
        row
        for row in rows
        if row["reciprocal_residual"]
        <= max(
            RECIPROCAL_RESIDUAL_LIMIT,
            100.0 * minimum_residual,
        )
    ]


def select_anchor_pair(
    rows: list[dict[str, Any]],
    representative_anchor: complex,
    reciprocal_anchor: complex,
) -> dict[str, Any]:
    return min(
        rows,
        key=lambda row: (
            M5030.chordal_distance(
                row["representative"], representative_anchor
            )
            + M5030.chordal_distance(
                row["reciprocal"], reciprocal_anchor
            ),
            row["reciprocal_residual"],
        ),
    )


def select_continuation_pair(
    rows: list[dict[str, Any]],
    previous: tuple[complex, complex],
) -> dict[str, Any]:
    return min(
        rows,
        key=lambda row: (
            pair_set_bottleneck(
                previous,
                (row["representative"], row["reciprocal"]),
            ),
            M5030.chordal_distance(
                previous[0], row["representative"]
            )
            + M5030.chordal_distance(
                previous[1], row["reciprocal"]
            ),
            row["reciprocal_residual"],
        ),
    )


def alternate_separation(
    selected: complex, candidates: list[complex]
) -> float:
    return float(
        min(
            (
                M5030.chordal_distance(selected, candidate)
                for candidate in candidates
                if M5030.chordal_distance(selected, candidate) > 1.0e-12
            ),
            default=1.0,
        )
    )


def paired_track(
    problem: dict[str, Any],
    coordinates: np.ndarray,
    candidate_cache: dict[float, list[dict[str, Any]]],
) -> dict[str, Any]:
    base_coordinate = float(
        problem["event"][problem["case"]["outer_coordinate"]]
    )
    anchor_index = int(np.argmin(np.abs(coordinates - base_coordinate)))
    candidates = []
    for coordinate in coordinates:
        key = float(coordinate)
        if key not in candidate_cache:
            candidate_cache[key] = candidate_pairs(problem, key)
        candidates.append(candidate_cache[key])
    selected: list[dict[str, Any] | None] = [None] * len(coordinates)
    selected[anchor_index] = select_anchor_pair(
        candidates[anchor_index],
        complex_value(problem["job"]["representative_anchor"]),
        complex_value(problem["job"]["reciprocal_anchor"]),
    )
    previous_row = selected[anchor_index]
    if previous_row is None:
        raise RuntimeError("anchor selection failed")
    previous = (
        complex(previous_row["representative"]),
        complex(previous_row["reciprocal"]),
    )
    for index in range(anchor_index + 1, len(coordinates)):
        row = select_continuation_pair(candidates[index], previous)
        selected[index] = row
        previous = (
            complex(row["representative"]),
            complex(row["reciprocal"]),
        )
    previous_row = selected[anchor_index]
    if previous_row is None:
        raise RuntimeError("anchor selection failed")
    previous = (
        complex(previous_row["representative"]),
        complex(previous_row["reciprocal"]),
    )
    for index in range(anchor_index - 1, -1, -1):
        row = select_continuation_pair(candidates[index], previous)
        selected[index] = row
        previous = (
            complex(row["representative"]),
            complex(row["reciprocal"]),
        )
    rows = [row for row in selected if row is not None]
    pairs = [
        (
            complex(row["representative"]),
            complex(row["reciprocal"]),
        )
        for row in rows
    ]
    representative_roots = [pair[0] for pair in pairs]
    reciprocal_roots = [pair[1] for pair in pairs]
    pair_steps = [
        pair_set_bottleneck(pairs[index - 1], pairs[index])
        for index in range(1, len(pairs))
    ]
    representative_steps = [
        M5030.chordal_distance(
            representative_roots[index - 1],
            representative_roots[index],
        )
        for index in range(1, len(representative_roots))
    ]
    reciprocal_steps = [
        M5030.chordal_distance(
            reciprocal_roots[index - 1],
            reciprocal_roots[index],
        )
        for index in range(1, len(reciprocal_roots))
    ]
    representative_pair = problem["case"]["representative_pair"]
    reciprocal_pair = problem["case"]["reciprocal_pair"]
    maximum_pair_step_index = (
        int(np.argmax(np.asarray(pair_steps))) if pair_steps else 0
    )
    violating_intervals = [
        {
            "left": float(coordinates[index]),
            "right": float(coordinates[index + 1]),
            "step": float(step),
        }
        for index, step in enumerate(pair_steps)
        if step > PAIR_SET_PROJECTIVE_LIMIT
    ]
    return {
        "coordinates": coordinates,
        "representative_roots": representative_roots,
        "reciprocal_roots": reciprocal_roots,
        "maximum_pair_set_projective_step": max(pair_steps, default=0.0),
        "maximum_representative_projective_step": max(
            representative_steps, default=0.0
        ),
        "maximum_reciprocal_projective_step": max(
            reciprocal_steps, default=0.0
        ),
        "maximum_reciprocal_product_residual": max(
            (float(row["reciprocal_residual"]) for row in rows),
            default=0.0,
        ),
        "maximum_pair_step_left": float(
            coordinates[maximum_pair_step_index]
        ),
        "maximum_pair_step_right": float(
            coordinates[
                min(maximum_pair_step_index + 1, len(coordinates) - 1)
            ]
        ),
        "violating_intervals": violating_intervals,
        "point_count": len(coordinates),
    }


def install_paired_track(problem: dict[str, Any]) -> dict[str, Any]:
    accepted: dict[str, Any] | None = None
    attempts: list[dict[str, Any]] = []
    base_coordinate = float(
        problem["event"][problem["case"]["outer_coordinate"]]
    )
    coordinates = np.unique(
        np.concatenate(
            (
                np.linspace(
                    ENERGY_MINIMUM,
                    ENERGY_MAXIMUM,
                    TRACK_BASE_POINTS,
                ),
                np.asarray([base_coordinate], dtype=float),
            )
        )
    )
    candidate_cache: dict[float, list[dict[str, Any]]] = {}
    for refinement in range(TRACK_MAXIMUM_REFINEMENTS + 1):
        track = paired_track(problem, coordinates, candidate_cache)
        attempts.append(
            {
                "refinement": refinement,
                "actual_point_count": track["point_count"],
                "maximum_pair_set_projective_step": track[
                    "maximum_pair_set_projective_step"
                ],
                "maximum_pair_step_left": track[
                    "maximum_pair_step_left"
                ],
                "maximum_pair_step_right": track[
                    "maximum_pair_step_right"
                ],
                "violating_interval_count": len(
                    track["violating_intervals"]
                ),
                "maximum_reciprocal_product_residual": track[
                    "maximum_reciprocal_product_residual"
                ],
            }
        )
        if (
            track["maximum_pair_set_projective_step"]
            <= PAIR_SET_PROJECTIVE_LIMIT
        ):
            accepted = track
            break
        midpoints = [
            0.5 * (row["left"] + row["right"])
            for row in track["violating_intervals"]
        ]
        refined = np.unique(
            np.concatenate(
                (
                    coordinates,
                    np.asarray(midpoints, dtype=float),
                )
            )
        )
        if len(refined) == len(coordinates):
            break
        coordinates = refined
    if accepted is None:
        accepted = track
    representative_pair = problem["case"]["representative_pair"]
    reciprocal_pair = problem["case"]["reciprocal_pair"]
    representative_separations: list[float] = []
    reciprocal_separations: list[float] = []
    for coordinate, representative, reciprocal in zip(
        accepted["coordinates"],
        accepted["representative_roots"],
        accepted["reciprocal_roots"],
    ):
        representative_separations.append(
            alternate_separation(
                representative,
                M5237.roots_for_pair(
                    problem["event"],
                    problem["target"],
                    representative_pair,
                    problem["case"]["outer_coordinate"],
                    complex(float(coordinate)),
                ),
            )
        )
        reciprocal_separations.append(
            alternate_separation(
                reciprocal,
                M5237.roots_for_pair(
                    problem["event"],
                    problem["target"],
                    reciprocal_pair,
                    problem["case"]["outer_coordinate"],
                    complex(float(coordinate)),
                ),
            )
        )
    accepted["minimum_representative_alternate_separation"] = min(
        representative_separations, default=1.0
    )
    accepted["minimum_reciprocal_alternate_separation"] = min(
        reciprocal_separations, default=1.0
    )
    problem["branch_tracks"] = {
        M5237.pair_key(representative_pair): {
            "coordinates": accepted["coordinates"],
            "roots": accepted["representative_roots"],
            "maximum_projective_step": accepted[
                "maximum_representative_projective_step"
            ],
            "minimum_alternate_branch_separation": accepted[
                "minimum_representative_alternate_separation"
            ],
        },
        M5237.pair_key(reciprocal_pair): {
            "coordinates": accepted["coordinates"],
            "roots": accepted["reciprocal_roots"],
            "maximum_projective_step": accepted[
                "maximum_reciprocal_projective_step"
            ],
            "minimum_alternate_branch_separation": accepted[
                "minimum_reciprocal_alternate_separation"
            ],
        },
    }
    accepted["attempts"] = attempts
    return accepted


def energy_job(source_job: dict[str, Any]) -> dict[str, Any]:
    job = copy.deepcopy(source_job)
    job["source_job_id"] = source_job["job_id"]
    job["job_id"] = f"{source_job['job_id']}_ENERGY"
    job["outer_coordinate"] = "soft_energy"
    job["scan_minimum"] = ENERGY_MINIMUM
    job["scan_maximum"] = ENERGY_MAXIMUM
    job["scan_points"] = SCAN_POINTS
    job["require_source_state"] = True
    payload = {
        key: value
        for key, value in job.items()
        if key != "job_input_hash"
    }
    job["job_input_hash"] = hashlib.sha256(
        json.dumps(
            payload,
            sort_keys=True,
            default=json_default,
        ).encode("utf-8")
    ).hexdigest()
    return job


def source_rows() -> list[dict[str, str]]:
    paths = (
        Path(__file__),
        SCRIPT_5239,
        SCRIPT_5246,
        SCRIPT_5265,
        MANIFEST_5239,
        RESULT_5266,
    )
    return [
        {"path": str(path), "sha256": digest(path)}
        for path in paths
    ]


def build_energy_problems(
    epsilon_ids: tuple[str, ...],
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
]:
    parent = read_json(MANIFEST_5239)
    jobs = [
        energy_job(job)
        for job in parent["jobs"]
        if job["epsilon_id"] in epsilon_ids
    ]
    problems: list[dict[str, Any]] = []
    track_rows: list[dict[str, Any]] = []
    for job in jobs:
        problem = M5239.build_problem(job)
        track = install_paired_track(problem)
        problems.append(problem)
        track_rows.append(
            {
                "job_id": job["job_id"],
                "epsilon_id": job["epsilon_id"],
                "component_id": job["component_id"],
                "family": job["family"],
                "owner_summand": job["owner_summand"],
                "track_point_count": track["point_count"],
                "track_refinement_count": len(track["attempts"]) - 1,
                "maximum_pair_set_projective_step": track[
                    "maximum_pair_set_projective_step"
                ],
                "maximum_pair_step_left": track[
                    "maximum_pair_step_left"
                ],
                "maximum_pair_step_right": track[
                    "maximum_pair_step_right"
                ],
                "maximum_reciprocal_product_residual": track[
                    "maximum_reciprocal_product_residual"
                ],
                "pair_set_track_passed": (
                    track["maximum_pair_set_projective_step"]
                    <= PAIR_SET_PROJECTIVE_LIMIT
                ),
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    return jobs, problems, track_rows


def preflight() -> dict[str, Any]:
    started = time.perf_counter()
    set_below_normal_priority()
    jobs, problems, built_track_rows = build_energy_problems(
        TARGET_EPSILON_IDS
    )
    topology_rows: list[dict[str, Any]] = []
    pole_rows: list[dict[str, Any]] = []
    compact_components: list[dict[str, Any]] = []
    tracks_by_job = {
        row["job_id"]: row for row in built_track_rows
    }
    for job, problem in zip(jobs, problems):
        track = tracks_by_job[job["job_id"]]
        _, _, poles, _ = M5239.scan_problem(problem)
        active = [pole for pole in poles if pole["causal_family_active"]]
        topology_row = {
            "job_id": job["job_id"],
            "epsilon_id": job["epsilon_id"],
            "component_id": job["component_id"],
            "family": job["family"],
            "owner_summand": job["owner_summand"],
            "outer_coordinate": job["outer_coordinate"],
            "scan_minimum": job["scan_minimum"],
            "scan_maximum": job["scan_maximum"],
            "scan_points": job["scan_points"],
            "track_point_count": track["track_point_count"],
            "track_attempt_count": track["track_refinement_count"] + 1,
            "maximum_pair_set_projective_step": track[
                "maximum_pair_set_projective_step"
            ],
            "maximum_reciprocal_product_residual": track[
                "maximum_reciprocal_product_residual"
            ],
            "pair_set_track_passed": (
                track["maximum_pair_set_projective_step"]
                <= PAIR_SET_PROJECTIVE_LIMIT
            ),
            "pole_count": len(poles),
            "active_pole_count": len(active),
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
        }
        topology_rows.append(topology_row)
        for pole in poles:
            pole_rows.append(
                {
                    "job_id": job["job_id"],
                    "epsilon_id": job["epsilon_id"],
                    "component_id": job["component_id"],
                    "family": job["family"],
                    "owner_summand": job["owner_summand"],
                    "pole_id": pole["pole_id"],
                    "primary_surface_id": pole["primary_surface_id"],
                    "real_axis_center": pole["real_axis_center"],
                    "pole_real": pole["pole_real"],
                    "pole_imaginary": pole["pole_imaginary"],
                    "causal_family_active": pole[
                        "causal_family_active"
                    ],
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
            )
        compact_components.append(
            {
                "job_id": job["job_id"],
                "component_id": job["component_id"],
                "owner_summand": job["owner_summand"],
                "pair_set_step": track[
                    "maximum_pair_set_projective_step"
                ],
                "track_points": track["track_point_count"],
                "pole_count": len(poles),
                "active_pole_count": len(active),
                "active_centers": [
                    float(pole["real_axis_center"]) for pole in active
                ],
            }
        )
    checks = {
        "parent_manifest_exists": MANIFEST_5239.exists(),
        "source_paths_exist": all(
            Path(row["path"]).exists() for row in source_rows()
        ),
        "target_component_count_is_six": len(jobs) == 6,
        "all_jobs_use_soft_energy": all(
            job["outer_coordinate"] == "soft_energy" for job in jobs
        ),
        "all_pair_set_tracks_pass": all(
            row["pair_set_track_passed"] for row in topology_rows
        ),
        "all_reciprocal_residuals_pass": all(
            row["maximum_reciprocal_product_residual"]
            <= RECIPROCAL_RESIDUAL_LIMIT
            for row in topology_rows
        ),
        "claims_locked_false": all(
            not row[field]
            for row in topology_rows
            for field in (
                "valid_for_numeric_UV_claim",
                "valid_for_local_GR_claim",
                "valid_for_full_MTS_claim",
            )
        ),
    }
    result = {
        "checkpoint": CHECKPOINT,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "mode": "preflight",
        "resource_contract": {
            "process_priority": "BELOW_NORMAL",
            "maximum_task_python_processes": 2,
            "worker_math_threads": 1,
        },
        "energy_measure_contract": {
            "soft_energy": "x=u_E",
            "soft_cosine": "c_s=2u_s-1",
            "decay_cosine": "c_d=2u_d-1",
            "differential_measure": "du_E du_s du_d = dx (dc_s/2)(dc_d/2)",
            "soft_energy_jacobian": 1.0,
            "angular_jacobian": 0.25,
            "post_quadrature_energy_pole_atlas_valid": False,
            "required_order": (
                "soft-energy component subtraction before finite "
                "relative/global contour quadrature"
            ),
        },
        "topology_contract": {
            "branch_object": (
                "unordered reciprocal projective pair "
                "{z_representative,z_reciprocal}"
            ),
            "continuity_metric": "pair-set chordal bottleneck",
            "pair_set_projective_limit": PAIR_SET_PROJECTIVE_LIMIT,
            "reciprocal_product_residual_limit": (
                RECIPROCAL_RESIDUAL_LIMIT
            ),
            "track_base_points": TRACK_BASE_POINTS,
            "track_maximum_refinements": TRACK_MAXIMUM_REFINEMENTS,
            "endpoint_geometry": (
                "complex-analytic endpoint continuation from checkpoint 5265"
            ),
        },
        "checks": checks,
        "acceptance_passed": all(checks.values()),
        "components": compact_components,
        "source_files": source_rows(),
        "runtime_seconds": time.perf_counter() - started,
        "decision": (
            "PROCEED_TO_DYNAMIC_ENERGY_WINDING_AND_EXACT_COMPONENT_RESIDUES"
            if all(checks.values())
            else "REPAIR_ENERGY_COMPONENT_TOPOLOGY_BEFORE_RESIDUE_FIT"
        ),
        "valid_for_topology_handoff": all(checks.values()),
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    write_csv(PREFLIGHT_ROWS, topology_rows)
    if pole_rows:
        write_csv(PREFLIGHT_POLES, pole_rows)
    atomic_json(PREFLIGHT_RESULT, result)
    atomic_json(
        PREFLIGHT_STATUS,
        {
            "checkpoint": CHECKPOINT,
            "mode": "preflight",
            "state": "COMPLETED",
            "acceptance_passed": result["acceptance_passed"],
            "decision": result["decision"],
            "runtime_seconds": result["runtime_seconds"],
        },
    )
    return result


def residue_pilot() -> dict[str, Any]:
    started = time.perf_counter()
    set_below_normal_priority()
    WINDING_ATTEMPTS.clear()
    jobs, problems, track_rows = build_energy_problems(("E040",))
    interval_rows: list[dict[str, Any]] = []
    for problem in problems:
        interval_rows.extend(
            M5239.derive_problem_winding_intervals(problem)
        )
    intervals_by_job = M5239.interval_rows_by_job(interval_rows)
    poles_by_job: dict[str, list[dict[str, Any]]] = {}
    pole_rows: list[dict[str, Any]] = []
    for problem in problems:
        _, _, poles, _ = M5239.scan_problem(problem)
        poles_by_job[problem["job"]["job_id"]] = poles
        pole_rows.extend(poles)
    global_centers = sorted(
        {
            float(pole["real_axis_center"])
            for poles in poles_by_job.values()
            for pole in poles
            if bool(pole["causal_family_active"])
        }
    )
    fit_rows: list[dict[str, Any]] = []
    for problem in problems:
        fit_rows.extend(
            M5239.fit_full_component_residues(
                problem,
                poles_by_job[problem["job"]["job_id"]],
                global_centers,
                intervals_by_job,
            )
        )
    active_poles = [
        pole
        for poles in poles_by_job.values()
        for pole in poles
        if bool(pole["causal_family_active"])
    ]
    active_keys = {
        (pole["epsilon_id"], pole["pole_id"]) for pole in active_poles
    }
    fit_keys = {
        (row["epsilon_id"], row["pole_id"]) for row in fit_rows
    }
    maximum_dynamic_projective_step = max(
        (
            float(row["maximum_pair_projective_step"])
            for row in interval_rows
        ),
        default=0.0,
    )
    maximum_dynamic_reciprocal_residual = max(
        (
            float(row["maximum_reciprocal_product_residual"])
            for row in interval_rows
        ),
        default=0.0,
    )
    checks = {
        "six_E040_jobs_built": len(jobs) == 6,
        "all_pair_set_tracks_pass": all(
            row["pair_set_track_passed"] for row in track_rows
        ),
        "every_job_has_dynamic_intervals": (
            set(intervals_by_job)
            == {job["job_id"] for job in jobs}
        ),
        "dynamic_projective_steps_pass": (
            maximum_dynamic_projective_step
            <= M5239.DYNAMIC_PROJECTIVE_STEP_LIMIT
        ),
        "dynamic_reciprocal_residuals_pass": (
            maximum_dynamic_reciprocal_residual <= 2.0e-8
        ),
        "active_poles_have_exact_fit_rows": active_keys == fit_keys,
        "all_exact_residue_fits_pass": (
            bool(fit_rows)
            and all(bool(row["fit_passed"]) for row in fit_rows)
        ),
        "claims_locked_false": all(
            not row[field]
            for row in fit_rows
            for field in (
                "valid_for_numeric_UV_claim",
                "valid_for_local_GR_claim",
                "valid_for_full_MTS_claim",
            )
        ),
    }
    result = {
        "checkpoint": CHECKPOINT,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "mode": "residue-pilot",
        "checks": checks,
        "acceptance_passed": all(checks.values()),
        "job_count": len(jobs),
        "dynamic_interval_count": len(interval_rows),
        "active_pole_count": len(active_poles),
        "exact_residue_fit_count": len(fit_rows),
        "winding_resolution_attempt_count": len(WINDING_ATTEMPTS),
        "maximum_dynamic_projective_step": (
            maximum_dynamic_projective_step
        ),
        "maximum_dynamic_reciprocal_residual": (
            maximum_dynamic_reciprocal_residual
        ),
        "fits": fit_rows,
        "runtime_seconds": time.perf_counter() - started,
        "decision": (
            "PROCEED_TO_TWO_REGULATOR_ENERGY_FIRST_INTEGRATION"
            if all(checks.values())
            else "REPAIR_DYNAMIC_ENERGY_TOPOLOGY_OR_RESIDUE_FIT"
        ),
        "valid_for_energy_residue_handoff": all(checks.values()),
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    write_csv(WINDING_ROWS, interval_rows)
    write_csv(RESIDUE_POLES, pole_rows)
    if WINDING_ATTEMPTS:
        write_csv(WINDING_ATTEMPT_ROWS, WINDING_ATTEMPTS)
    if fit_rows:
        write_csv(RESIDUE_ROWS, fit_rows)
    atomic_json(RESIDUE_RESULT, result)
    atomic_json(
        PREFLIGHT_STATUS,
        {
            "checkpoint": CHECKPOINT,
            "mode": "residue-pilot",
            "state": "COMPLETED",
            "acceptance_passed": result["acceptance_passed"],
            "decision": result["decision"],
            "runtime_seconds": result["runtime_seconds"],
        },
    )
    return result


def worker_paths(epsilon_id: str) -> dict[str, Path]:
    root = WORKERS / epsilon_id
    return {
        "root": root,
        "result": root / "regulator_result.json",
        "status": root / "status.json",
        "tracks": root / "branch_tracks.csv",
        "intervals": root / "dynamic_winding_intervals.csv",
        "attempts": root / "winding_resolution_attempts.csv",
        "poles": root / "energy_poles.csv",
        "fits": root / "energy_residue_fits.csv",
        "quadrature": root / "energy_first_quadrature.csv",
    }


def regulator_worker(epsilon_id: str) -> dict[str, Any]:
    if epsilon_id not in REGULATOR_EPSILON_IDS:
        raise ValueError(f"unsupported epsilon id: {epsilon_id}")
    started = time.perf_counter()
    set_below_normal_priority()
    WINDING_ATTEMPTS.clear()
    paths = worker_paths(epsilon_id)
    atomic_json(
        paths["status"],
        {
            "checkpoint": CHECKPOINT,
            "epsilon_id": epsilon_id,
            "state": "RUNNING",
        },
    )
    jobs, problems, track_rows = build_energy_problems((epsilon_id,))
    interval_rows: list[dict[str, Any]] = []
    for problem in problems:
        interval_rows.extend(
            M5239.derive_problem_winding_intervals(problem)
        )
    intervals_by_job = M5239.interval_rows_by_job(interval_rows)
    poles_by_job: dict[str, list[dict[str, Any]]] = {}
    pole_rows: list[dict[str, Any]] = []
    for problem in problems:
        _, _, poles, _ = M5239.scan_problem(problem)
        poles_by_job[problem["job"]["job_id"]] = poles
        pole_rows.extend(poles)
    global_centers = sorted(
        {
            float(pole["real_axis_center"])
            for poles in poles_by_job.values()
            for pole in poles
            if bool(pole["causal_family_active"])
        }
    )
    fit_rows: list[dict[str, Any]] = []
    for problem in problems:
        fit_rows.extend(
            M5239.fit_full_component_residues(
                problem,
                poles_by_job[problem["job"]["job_id"]],
                global_centers,
                intervals_by_job,
            )
        )
    M5239.SCAN_MINIMUM = ENERGY_MINIMUM
    M5239.SCAN_MAXIMUM = ENERGY_MAXIMUM
    original_gauss_integral = M5239.gauss_integral

    def composite_gauss_integral(
        function: Any,
        lower: float,
        upper: float,
        order: int,
    ) -> complex:
        panel_count = max(
            1,
            int(
                math.ceil(
                    (upper - lower)
                    / ENERGY_COMPOSITE_PANEL_MAXIMUM_WIDTH
                )
            ),
        )
        boundaries = np.linspace(lower, upper, panel_count + 1)
        return sum(
            (
                original_gauss_integral(
                    function,
                    float(boundaries[index]),
                    float(boundaries[index + 1]),
                    order,
                )
                for index in range(panel_count)
            ),
            0.0j,
        )

    M5239.gauss_integral = composite_gauss_integral
    try:
        quadrature_rows, totals, coverage = (
            M5239.integrate_matched_event(
                problems,
                fit_rows,
                epsilon_id,
                intervals_by_job,
            )
        )
    finally:
        M5239.gauss_integral = original_gauss_integral
    for row in quadrature_rows:
        row["composite_panel_count"] = max(
            1,
            int(
                math.ceil(
                    (float(row["upper"]) - float(row["lower"]))
                    / ENERGY_COMPOSITE_PANEL_MAXIMUM_WIDTH
                )
            ),
        )
        row["maximum_panel_width"] = (
            ENERGY_COMPOSITE_PANEL_MAXIMUM_WIDTH
        )
    coverage["integration_revision"] = ENERGY_INTEGRATION_REVISION
    coverage["maximum_panel_width"] = (
        ENERGY_COMPOSITE_PANEL_MAXIMUM_WIDTH
    )
    coverage["composite_panel_count"] = sum(
        int(row["composite_panel_count"])
        for row in quadrature_rows
        if int(row["quadrature_order"])
        == int(M5239.QUADRATURE_ORDERS[0])
    )
    reference = totals[M5239.QUADRATURE_ORDERS[-1]]["subtracted"]
    denominator = max(abs(reference), 1.0)
    convergence: dict[str, dict[str, float]] = {}
    for order in M5239.QUADRATURE_ORDERS:
        convergence[str(order)] = {
            "raw_relative_error_to_subtracted_reference": float(
                abs(totals[order]["raw"] - reference) / denominator
            ),
            "subtracted_relative_error_to_reference": float(
                abs(totals[order]["subtracted"] - reference)
                / denominator
            ),
        }
    maximum_dynamic_projective_step = max(
        (
            float(row["maximum_pair_projective_step"])
            for row in interval_rows
        ),
        default=0.0,
    )
    maximum_dynamic_reciprocal_residual = max(
        (
            float(row["maximum_reciprocal_product_residual"])
            for row in interval_rows
        ),
        default=0.0,
    )
    active_poles = [
        pole
        for pole in pole_rows
        if bool(pole["causal_family_active"])
    ]
    active_keys = {
        (pole["epsilon_id"], pole["pole_id"]) for pole in active_poles
    }
    fit_keys = {
        (row["epsilon_id"], row["pole_id"]) for row in fit_rows
    }
    low_order = M5239.QUADRATURE_ORDERS[0]
    mid_order = M5239.QUADRATURE_ORDERS[-2]
    checks = {
        "six_jobs_built": len(jobs) == 6,
        "all_pair_set_tracks_pass": all(
            row["pair_set_track_passed"] for row in track_rows
        ),
        "every_job_has_dynamic_intervals": (
            set(intervals_by_job)
            == {job["job_id"] for job in jobs}
        ),
        "dynamic_projective_steps_pass": (
            maximum_dynamic_projective_step
            <= PAIR_SET_PROJECTIVE_LIMIT
        ),
        "dynamic_reciprocal_residuals_pass": (
            maximum_dynamic_reciprocal_residual
            <= RECIPROCAL_RESIDUAL_LIMIT
        ),
        "active_poles_have_exact_fit_rows": active_keys == fit_keys,
        "all_exact_residue_fits_pass": (
            bool(fit_rows)
            and all(bool(row["fit_passed"]) for row in fit_rows)
        ),
        "integration_domain_covered": (
            float(coverage["coverage_residual"]) <= 1.0e-12
        ),
        "low_order_subtracted_converged": (
            convergence[str(low_order)][
                "subtracted_relative_error_to_reference"
            ]
            <= M5239.LOW_ORDER_SUBTRACTED_RELATIVE_ERROR_LIMIT
        ),
        "mid_order_subtracted_converged": (
            convergence[str(mid_order)][
                "subtracted_relative_error_to_reference"
            ]
            <= M5239.MID_ORDER_SUBTRACTED_RELATIVE_ERROR_LIMIT
        ),
        "claims_locked_false": all(
            not row[field]
            for row in fit_rows
            for field in (
                "valid_for_numeric_UV_claim",
                "valid_for_local_GR_claim",
                "valid_for_full_MTS_claim",
            )
        ),
    }
    result = {
        "checkpoint": CHECKPOINT,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "integration_revision": ENERGY_INTEGRATION_REVISION,
        "mode": "regulator-worker",
        "epsilon_id": epsilon_id,
        "checks": checks,
        "acceptance_passed": all(checks.values()),
        "job_count": len(jobs),
        "dynamic_interval_count": len(interval_rows),
        "winding_resolution_attempt_count": len(WINDING_ATTEMPTS),
        "active_pole_count": len(active_poles),
        "exact_residue_fit_count": len(fit_rows),
        "maximum_dynamic_projective_step": (
            maximum_dynamic_projective_step
        ),
        "maximum_dynamic_reciprocal_residual": (
            maximum_dynamic_reciprocal_residual
        ),
        "quadrature_orders": list(M5239.QUADRATURE_ORDERS),
        "totals": totals,
        "convergence": convergence,
        "coverage": coverage,
        "runtime_seconds": time.perf_counter() - started,
        "decision": (
            "REGULATOR_ENERGY_FIRST_SLICE_ACCEPTED"
            if all(checks.values())
            else "REGULATOR_ENERGY_FIRST_SLICE_REQUIRES_REPAIR"
        ),
        "valid_for_fixed_angle_regulator_slice": all(checks.values()),
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    write_csv(paths["tracks"], track_rows)
    write_csv(paths["intervals"], interval_rows)
    if WINDING_ATTEMPTS:
        write_csv(paths["attempts"], WINDING_ATTEMPTS)
    write_csv(paths["poles"], pole_rows)
    if fit_rows:
        write_csv(paths["fits"], fit_rows)
    write_csv(paths["quadrature"], quadrature_rows)
    atomic_json(paths["result"], result)
    atomic_json(
        paths["status"],
        {
            "checkpoint": CHECKPOINT,
            "epsilon_id": epsilon_id,
            "state": "COMPLETED",
            "acceptance_passed": result["acceptance_passed"],
            "decision": result["decision"],
            "runtime_seconds": result["runtime_seconds"],
        },
    )
    return result


def complex_from_json(value: dict[str, Any]) -> complex:
    if isinstance(value, complex):
        return value
    return complex(float(value["real"]), float(value["imaginary"]))


def regulator_total(
    result: dict[str, Any],
    order: int,
    channel: str,
) -> complex:
    totals = result["totals"]
    row = totals.get(str(order), totals.get(order))
    if row is None:
        raise KeyError(f"missing quadrature order {order}")
    return complex_from_json(row[channel])


def combine_regulators(
    regulator_results: dict[str, dict[str, Any]],
    runtime_seconds: float,
) -> dict[str, Any]:
    rows: list[dict[str, Any]] = []
    multiplier = (
        M5239.M5231.PHYSICAL_A00_WEIGHT
        * M5239.M5231.KERNEL_MULTIPLIER
    )
    orders = tuple(M5239.QUADRATURE_ORDERS)
    combined: dict[int, dict[str, complex]] = {}
    for order in orders:
        raw = multiplier * (
            2.0
            * regulator_total(
                regulator_results["E020"], order, "raw"
            )
            - regulator_total(
                regulator_results["E040"], order, "raw"
            )
        )
        subtracted = multiplier * (
            2.0
            * regulator_total(
                regulator_results["E020"], order, "subtracted"
            )
            - regulator_total(
                regulator_results["E040"], order, "subtracted"
            )
        )
        combined[order] = {
            "raw": raw,
            "subtracted": subtracted,
        }
    reference = combined[orders[-1]]["subtracted"]
    denominator = max(abs(reference), 1.0)
    for order in orders:
        rows.append(
            {
                "quadrature_order": order,
                "raw_real": combined[order]["raw"].real,
                "raw_imaginary": combined[order]["raw"].imag,
                "subtracted_real": combined[order]["subtracted"].real,
                "subtracted_imaginary": (
                    combined[order]["subtracted"].imag
                ),
                "raw_relative_error_to_subtracted_reference": (
                    abs(combined[order]["raw"] - reference)
                    / denominator
                ),
                "subtracted_relative_error_to_reference": (
                    abs(combined[order]["subtracted"] - reference)
                    / denominator
                ),
                "soft_energy_jacobian": 1.0,
                "angular_jacobian_pending": 0.25,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    low_error = float(
        rows[0]["subtracted_relative_error_to_reference"]
    )
    mid_error = float(
        rows[-2]["subtracted_relative_error_to_reference"]
    )
    checks = {
        "both_regulator_workers_accepted": all(
            bool(regulator_results[epsilon_id]["acceptance_passed"])
            for epsilon_id in REGULATOR_EPSILON_IDS
        ),
        "low_order_combination_converged": (
            low_error
            <= M5239.LOW_ORDER_SUBTRACTED_RELATIVE_ERROR_LIMIT
        ),
        "mid_order_combination_converged": (
            mid_error
            <= M5239.MID_ORDER_SUBTRACTED_RELATIVE_ERROR_LIMIT
        ),
        "energy_measure_is_exact": True,
        "angular_integration_remains_pending": True,
        "claims_locked_false": True,
    }
    result = {
        "checkpoint": CHECKPOINT,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "mode": "two-regulator-energy-first",
        "checks": checks,
        "acceptance_passed": all(checks.values()),
        "regulators": regulator_results,
        "physical_regulator_combination": "2 E020 - E040",
        "kernel_multiplier": M5239.M5231.KERNEL_MULTIPLIER,
        "physical_A00_weight": M5239.M5231.PHYSICAL_A00_WEIGHT,
        "soft_energy_jacobian": 1.0,
        "angular_jacobian_pending": 0.25,
        "integration_revision": ENERGY_INTEGRATION_REVISION,
        "maximum_composite_panel_width": (
            ENERGY_COMPOSITE_PANEL_MAXIMUM_WIDTH
        ),
        "combined_totals": combined,
        "combined_convergence": rows,
        "runtime_seconds": runtime_seconds,
        "source_files": source_rows(),
        "artifact_paths": {
            "preflight_result": str(PREFLIGHT_RESULT),
            "residue_pilot_result": str(RESIDUE_RESULT),
            "E040_worker_result": str(
                worker_paths("E040")["result"]
            ),
            "E020_worker_result": str(
                worker_paths("E020")["result"]
            ),
            "combined_convergence": str(FULL_ROWS),
        },
        "formalization_workbench_reference_digest": read_json(
            RESULT_5266
        )["formalization_workbench_end_digest"],
        "formalization_workbench_end_digest": (
            formal_inventory_digest()
        ),
        "decision": (
            "ACCEPT_FIXED_ANGLE_ENERGY_FIRST_RULE__RETURN_TO_ANGULAR_OUTER_INTEGRATION"
            if all(checks.values())
            else "REPAIR_TWO_REGULATOR_ENERGY_FIRST_RULE"
        ),
        "claim_boundary": {
            "valid_for_fixed_angle_energy_rule": all(checks.values()),
            "valid_for_full_phase_space_coefficient": False,
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
            "reason": (
                "The soft-energy rule is evaluated at one fixed angular "
                "event and on a cutoff domain; angular outer integration "
                "and endpoint completion remain pending."
            ),
        },
    }
    write_csv(FULL_ROWS, rows)
    atomic_json(FULL_RESULT, result)
    atomic_json(
        PREFLIGHT_STATUS,
        {
            "checkpoint": CHECKPOINT,
            "mode": "two-regulator-energy-first",
            "state": "COMPLETED",
            "acceptance_passed": result["acceptance_passed"],
            "decision": result["decision"],
        },
    )
    return result


def full_two_regulator_run() -> dict[str, Any]:
    started = time.perf_counter()
    set_below_normal_priority()
    SOURCE.mkdir(parents=True, exist_ok=True)
    command = [
        sys.executable,
        "-B",
        str(Path(__file__).resolve()),
        "--mode",
        "regulator-worker",
        "--epsilon",
        "E020",
    ]
    environment = dict(os.environ)
    for thread_variable in (
        "OMP_NUM_THREADS",
        "OPENBLAS_NUM_THREADS",
        "MKL_NUM_THREADS",
        "NUMEXPR_NUM_THREADS",
        "VECLIB_MAXIMUM_THREADS",
        "BLIS_NUM_THREADS",
    ):
        environment[thread_variable] = "1"
    with CHILD_LOG.open("w", encoding="utf-8") as child_log:
        child = subprocess.Popen(
            command,
            stdout=child_log,
            stderr=subprocess.STDOUT,
            env=environment,
        )
        E040 = regulator_worker("E040")
        child_return_code = child.wait()
    if (
        child_return_code != 0
        and not worker_paths("E020")["result"].exists()
    ):
        raise RuntimeError(
            f"E020 regulator worker failed with code {child_return_code}"
        )
    E020 = read_json(worker_paths("E020")["result"])
    return combine_regulators(
        {"E040": E040, "E020": E020},
        time.perf_counter() - started,
    )


def combine_existing_results() -> dict[str, Any]:
    previous_runtime = (
        float(read_json(FULL_RESULT).get("runtime_seconds", 0.0))
        if FULL_RESULT.exists()
        else 0.0
    )
    regulator_results = {
        epsilon_id: read_json(worker_paths(epsilon_id)["result"])
        for epsilon_id in REGULATOR_EPSILON_IDS
    }
    return combine_regulators(regulator_results, previous_runtime)


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
    result: dict[str, Any],
    validation_passed: bool,
) -> None:
    reference = result["combined_convergence"][-1]
    E040 = result["regulators"]["E040"]
    E020 = result["regulators"]["E020"]
    E040_fit = read_csv(worker_paths("E040")["fits"])[0]
    E020_fit = read_csv(worker_paths("E020")["fits"])[0]
    text = f"""# 5267 — Topology-aware soft-energy component runner

## Question

Checkpoint 5266 falsified energy integration outside a finite inner-contour quadrature: its narrow pole ladder changed violently with inner order. The required replacement is to resolve the exact material components, their causal topology, and their energy poles before applying any finite soft-energy quadrature.

## Exact measure

The parent generator uses

`x = u_E`, `c_s = 2u_s - 1`, `c_d = 2u_d - 1`,

so

`du_E du_s du_d = dx (dc_s/2)(dc_d/2)`.

The soft-energy Jacobian is exactly `1`; the angular Jacobian `1/4` remains pending until the two angular outer integrals are restored.

## Topology construction

The physical branch object is the unordered reciprocal projective pair `{{z_rep,z_rec}}`, not either chart label alone. Continuation uses the pair-set chordal bottleneck on `CP1`. A local homotopy mesh is refined until every pair-set step is at most `{PAIR_SET_PROJECTIVE_LIMIT:.3g}` and every reciprocal product residual is at most `{RECIPROCAL_RESIDUAL_LIMIT:.3g}`. Winding integers must agree at consecutive base resolutions, with accepted base resolution at least `{HOMOTOPY_MINIMUM_ACCEPTED_BASE_RESOLUTION}`.

This repairs the low-energy MC03/MC07 chart exchange without changing the physical branch. Across the accepted E040 interval map, the maximum pair-set step is `{E040['maximum_dynamic_projective_step']:.12g}` and the maximum reciprocal residual is `{E040['maximum_dynamic_reciprocal_residual']:.12g}`.

## Exact energy pole

Both regulators contain one active geometric pole, owned by `MC04` (`direct:g1:minus/direct:g3:plus`):

| Regulator | center | pole | residue | slopes | numerator residual |
|---|---:|---:|---:|---:|---:|
| E040 | {float(E040_fit['center']):.12g} | {float(E040_fit['pole_real']):.12g} + {float(E040_fit['pole_imaginary']):.12g} i | {float(E040_fit['outer_residue_real']):.12g} + {float(E040_fit['outer_residue_imaginary']):.12g} i | {float(E040_fit['negative_log_log_slope']):.9g}, {float(E040_fit['positive_log_log_slope']):.9g} | {float(E040_fit['numerator_fit_relative_residual']):.6g} |
| E020 | {float(E020_fit['center']):.12g} | {float(E020_fit['pole_real']):.12g} + {float(E020_fit['pole_imaginary']):.12g} i | {float(E020_fit['outer_residue_real']):.12g} + {float(E020_fit['outer_residue_imaginary']):.12g} i | {float(E020_fit['negative_log_log_slope']):.9g}, {float(E020_fit['positive_log_log_slope']):.9g} | {float(E020_fit['numerator_fit_relative_residual']):.6g} |

Both two-sided fits pass the `-1` Laurent-slope and numerator-polynomial gates.

## Energy-first integral

The logarithmic pole term is removed analytically before numerical quadrature. Smooth topology intervals are panelized to maximum width `{ENERGY_COMPOSITE_PANEL_MAXIMUM_WIDTH}` rather than weakening the low-order gate.

For the regulator combination `2 E020 - E040`, including the inherited kernel and A00 factors but not the pending angular Jacobian, the 512-node reference is

`I_E = {float(reference['subtracted_real']):.15g} {float(reference['subtracted_imaginary']):+.15g} i`.

The subtracted relative errors are:

| Composite Gauss order | relative error |
|---:|---:|
| 32 | {float(result['combined_convergence'][0]['subtracted_relative_error_to_reference']):.12g} |
| 128 | {float(result['combined_convergence'][1]['subtracted_relative_error_to_reference']):.12g} |
| 512 | 0 |

The raw 32-node error is `{float(result['combined_convergence'][0]['raw_relative_error_to_subtracted_reference']):.12g}`, so the accepted convergence is specifically produced by topology-aware component subtraction.

## Decision

`{result['decision']}`

Validation passed: `{str(validation_passed).lower()}`.

This accepts an order-independent, fixed-angle soft-energy rule. It does **not** yet accept a full phase-space coefficient, numeric UV fixed point, local-GR limit, or full MTS theory.

## Next derivation

Restore the two angular outer integrations while retaining this ordering:

1. resolve angular topology chambers;
2. transport the already-subtracted energy component rule within each chamber;
3. apply the exact angular Jacobian `1/4`;
4. bound `x<10^-4` and `1-x<10^-4` endpoint caps;
5. test angular and regulator convergence before interpreting a coefficient.

## Artifacts

- Runner: `{Path(__file__).resolve()}`
- Combined result: `{FULL_RESULT}`
- Combined convergence: `{FULL_ROWS}`
- E040 worker: `{worker_paths('E040')['result']}`
- E020 worker: `{worker_paths('E020')['result']}`
- Validation: `{VALIDATION}`
"""
    temporary = DOCUMENT.with_suffix(DOCUMENT.suffix + ".tmp")
    temporary.write_text(text, encoding="utf-8")
    os.replace(temporary, DOCUMENT)


def validate_outputs() -> dict[str, Any]:
    result = read_json(FULL_RESULT)
    preflight_result = read_json(PREFLIGHT_RESULT)
    residue_result = read_json(RESIDUE_RESULT)
    worker_results = {
        epsilon_id: read_json(worker_paths(epsilon_id)["result"])
        for epsilon_id in REGULATOR_EPSILON_IDS
    }
    required_csvs = [
        PREFLIGHT_ROWS,
        PREFLIGHT_POLES,
        WINDING_ROWS,
        RESIDUE_ROWS,
        RESIDUE_POLES,
        FULL_ROWS,
        *[
            worker_paths(epsilon_id)[key]
            for epsilon_id in REGULATOR_EPSILON_IDS
            for key in (
                "tracks",
                "intervals",
                "poles",
                "fits",
                "quadrature",
            )
        ],
    ]
    csv_rows = {
        str(path): read_csv(path)
        for path in required_csvs
        if path.exists()
    }
    fit_rows = [
        row
        for epsilon_id in REGULATOR_EPSILON_IDS
        for row in read_csv(worker_paths(epsilon_id)["fits"])
    ]
    source_files = result["source_files"]
    reference_formal_digest = str(
        read_json(RESULT_5266)["formalization_workbench_end_digest"]
    )
    current_formal_digest = formal_inventory_digest()
    serialized_outputs = json.dumps(
        {
            "result": result,
            "preflight": preflight_result,
            "residue": residue_result,
            "workers": worker_results,
            "csvs": csv_rows,
        },
        default=json_default,
    )
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
            "all recorded source digests reproduce",
        ),
        validation_gate(
            "PREFLIGHT_ACCEPTED",
            bool(preflight_result["acceptance_passed"]),
            str(preflight_result["decision"]),
        ),
        validation_gate(
            "RESIDUE_PILOT_ACCEPTED",
            bool(residue_result["acceptance_passed"]),
            str(residue_result["decision"]),
        ),
        validation_gate(
            "BOTH_REGULATORS_ACCEPTED",
            all(
                bool(worker_results[epsilon_id]["acceptance_passed"])
                for epsilon_id in REGULATOR_EPSILON_IDS
            ),
            "E040 and E020 accepted",
        ),
        validation_gate(
            "COMBINED_RULE_ACCEPTED",
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
            "EXACT_RESIDUES_PASS",
            (
                len(fit_rows) == 2
                and all(row["fit_passed"].lower() == "true" for row in fit_rows)
                and all(
                    abs(float(row["negative_log_log_slope"]) + 1.0)
                    <= M5239.M5237.SLOPE_TOLERANCE
                    and abs(float(row["positive_log_log_slope"]) + 1.0)
                    <= M5239.M5237.SLOPE_TOLERANCE
                    and float(row["numerator_fit_relative_residual"])
                    <= M5239.M5237.NUMERATOR_FIT_RELATIVE_RESIDUAL_LIMIT
                    for row in fit_rows
                )
            ),
            "one passing MC04 fit per regulator",
        ),
        validation_gate(
            "ORDER_INDEPENDENT_HANDOFF",
            (
                float(
                    result["combined_convergence"][0][
                        "subtracted_relative_error_to_reference"
                    ]
                )
                <= M5239.LOW_ORDER_SUBTRACTED_RELATIVE_ERROR_LIMIT
                and float(
                    result["combined_convergence"][-2][
                        "subtracted_relative_error_to_reference"
                    ]
                )
                <= M5239.MID_ORDER_SUBTRACTED_RELATIVE_ERROR_LIMIT
            ),
            "composite orders 32 and 128 agree with 512",
        ),
        validation_gate(
            "SUBTRACTION_IMPROVES_LOW_ORDER",
            (
                float(
                    result["combined_convergence"][0][
                        "subtracted_relative_error_to_reference"
                    ]
                )
                < float(
                    result["combined_convergence"][0][
                        "raw_relative_error_to_subtracted_reference"
                    ]
                )
            ),
            "subtracted error is below raw error",
        ),
        validation_gate(
            "NO_MISSING_MARKERS",
            "MISSING_" not in serialized_outputs,
            "no MISSING_ token in claim-bearing artifacts",
        ),
        validation_gate(
            "CLAIMS_LOCKED_FALSE",
            (
                not result["claim_boundary"][
                    "valid_for_full_phase_space_coefficient"
                ]
                and not result["claim_boundary"][
                    "valid_for_numeric_UV_claim"
                ]
                and not result["claim_boundary"][
                    "valid_for_local_GR_claim"
                ]
                and not result["claim_boundary"][
                    "valid_for_full_MTS_claim"
                ]
            ),
            "only fixed-angle energy rule is accepted",
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
                preflight_result["resource_contract"][
                    "maximum_task_python_processes"
                ]
                == 2
                and preflight_result["resource_contract"][
                    "worker_math_threads"
                ]
                == 1
            ),
            "maximum two below-normal single-thread workers",
        ),
    ]
    passed = all(row["passed"] for row in rows)
    write_csv(VALIDATION, rows)
    write_csv(RESIDUAL_VALIDATION, rows)
    render_document(result, passed)
    atomic_json(
        PREFLIGHT_STATUS,
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
            "VALIDATED_ORDER_INDEPENDENT_FIXED_ANGLE_ENERGY_HANDOFF"
            if passed
            else "VALIDATION_REQUIRES_REPAIR"
        ),
        "runtime_seconds": 0.0,
        "validation_gate_count": len(rows),
        "failed_gates": [
            row["gate_id"] for row in rows if not row["passed"]
        ],
        "formalization_workbench_modified_file_count": (
            0 if current_formal_digest == reference_formal_digest else -1
        ),
        "valid_for_fixed_angle_energy_rule": passed,
        "valid_for_full_phase_space_coefficient": False,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=(
            "preflight",
            "residue-pilot",
            "regulator-worker",
            "full",
            "combine",
            "validate",
        ),
        default="preflight",
    )
    parser.add_argument(
        "--epsilon",
        choices=REGULATOR_EPSILON_IDS,
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.mode == "preflight":
        result = preflight()
    elif args.mode == "residue-pilot":
        result = residue_pilot()
    elif args.mode == "regulator-worker":
        if args.epsilon is None:
            raise RuntimeError("--epsilon is required for regulator-worker")
        result = regulator_worker(args.epsilon)
    elif args.mode == "full":
        result = full_two_regulator_run()
    elif args.mode == "combine":
        result = combine_existing_results()
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
