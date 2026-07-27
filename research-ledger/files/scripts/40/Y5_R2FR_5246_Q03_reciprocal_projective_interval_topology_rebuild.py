from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import math
import shutil
import sys
import time
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE = POST / "source-intake" / "functional_rg" / "5246"
RESIDUALS = POST / "source-intake" / "mts_residuals"
JOB_CACHE = SOURCE / "job-cache"

SCRIPT_5245 = (
    POST
    / "scripts"
    / "Y5_R2FR_5245_reciprocal_projective_chamber_boundary_tracker.py"
)
RESULT_5245 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5245"
    / "reciprocal_projective_boundary_result.json"
)
VALIDATION_5245 = (
    RESIDUALS / "P8_Y5_BRR545_5245_VALIDATION.csv"
)
SUMMARY_5245 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5245"
    / "reciprocal_projective_case_summary.csv"
)

MANIFEST = SOURCE / "Q03_reciprocal_projective_interval_manifest.json"
DRY_RUN = SOURCE / "Q03_reciprocal_projective_interval_dry_run.json"
RESULT = SOURCE / "Q03_reciprocal_projective_interval_result.json"
STATE_CACHE = SOURCE / "Q03_reciprocal_projective_state_cache.json"
ATTEMPT_ROWS = SOURCE / "Q03_reciprocal_projective_resolution_attempts.csv"
INTERVAL_ROWS = SOURCE / "Q03_reciprocal_projective_intervals.csv"
TRANSITION_ROWS = SOURCE / "Q03_reciprocal_projective_transitions.csv"
JOB_ROWS = SOURCE / "Q03_reciprocal_projective_job_summary.csv"
COMPARISON_ROWS = SOURCE / "Q03_legacy_vs_reciprocal_projective_map.csv"
VALIDATION = RESIDUALS / "P8_Y5_BRR545_5246_VALIDATION.csv"
DOCUMENT = (
    POST
    / "5246-Y5-R2FR-Q03-reciprocal-projective-interval-topology-rebuild.md"
)

MARKER = "MTS_5246_Q03_RECIPROCAL_PROJECTIVE_INTERVAL_TOPOLOGY_REBUILD"
REVISION = "Q03-reciprocal-projective-interval-topology-rebuild-v1"
FORMAL_BASELINE = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)

TARGET_NODE_ID = "Q03"
BASE_RESOLUTION_LADDER = (2048, 4096, 8192, 16384, 32768)
MINIMUM_ACCEPTED_BASE_RESOLUTION = 4096
MAXIMUM_PROJECTIVE_STEP = 5.0e-2
MAXIMUM_RECIPROCAL_RESIDUAL = 2.0e-8
MAXIMUM_BOUNDARY_RECIPROCAL_RESIDUAL = 2.0e-10
MAXIMUM_BOUNDARY_POLYNOMIAL_RESIDUAL = 2.0e-10
MAXIMUM_STEP_RATIO = 0.65
BOUNDARY_REFINEMENT_TARGET = 2.5e-2
MAXIMUM_BOUNDARY_REFINEMENT_DEPTH = 12
EXPECTED_JOB_COUNT = 12
MAXIMUM_RUNTIME_SECONDS = 4.0 * 60.0 * 60.0


def load_module(path: Path, name: str) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5245 = load_module(SCRIPT_5245, "mts_5245_for_5246")
M5244 = M5245.M5244
M5243 = M5244.M5243
M5240 = M5244.M5240
M5239 = M5244.M5239
M5232 = M5244.M5232
M5030 = M5245.M5030
M5034 = M5245.M5034

digest = M5245.digest
tree_digest = M5245.tree_digest
serialized_hash = M5245.serialized_hash
atomic_text = M5245.atomic_text
atomic_json = M5245.atomic_json
write_csv = M5245.write_csv


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def source_rows() -> list[dict[str, str]]:
    paths = (
        SCRIPT_5245,
        RESULT_5245,
        VALIDATION_5245,
        SUMMARY_5245,
        M5244.SCRIPT_5243,
        M5243.MANIFEST_5241,
        M5243.WINDING_5241,
        M5243.NODE_ROWS_5241,
    )
    return [
        {"path": str(path), "sha256": digest(path)}
        for path in paths
    ]


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


def adaptive_boundary_mesh(
    problem: dict[str, Any],
    coordinate: float,
    base_steps: int,
) -> tuple[list[complex], dict[str, Any]]:
    event = dict(problem["event"])
    event[problem["case"]["outer_coordinate"]] = float(coordinate)
    M5034.configure(event, problem["target"])
    grid = M5030.homotopy_cosines(
        base_steps, M5232.REGULATOR, "feynman"
    )
    boundaries, _ = M5030.physical_chambers()
    representatives: list[dict[str, Any]] = []
    keys: set[tuple[int, int]] = set()
    for boundary in boundaries:
        if boundary.get("synthetic"):
            continue
        key = M5245.equation_key(boundary)
        if key not in keys:
            keys.add(key)
            representatives.append(boundary)
    root_cache: dict[
        tuple[tuple[int, int], complex],
        tuple[complex, complex],
    ] = {}

    def roots(
        boundary: dict[str, Any], cosine: complex
    ) -> tuple[complex, complex]:
        key = (M5245.equation_key(boundary), cosine)
        if key not in root_cache:
            root_cache[key] = (
                M5245.reciprocal_polynomial_roots(
                    boundary, cosine
                )[0]
            )
        return root_cache[key]

    refinement_depth = 0
    total_inserted_nodes = 0
    maximum_half_step = 0.0
    while representatives:
        updated = [grid[0]]
        inserted = 0
        maximum_half_step = 0.0
        for first, second in zip(grid[:-1], grid[1:]):
            midpoint = 0.5 * (first + second)
            local_step = 0.0
            for boundary in representatives:
                local_step = max(
                    local_step,
                    pair_set_bottleneck(
                        roots(boundary, first),
                        roots(boundary, midpoint),
                    ),
                    pair_set_bottleneck(
                        roots(boundary, midpoint),
                        roots(boundary, second),
                    ),
                )
            maximum_half_step = max(
                maximum_half_step, local_step
            )
            if local_step > BOUNDARY_REFINEMENT_TARGET:
                updated.append(midpoint)
                inserted += 1
            updated.append(second)
        grid = updated
        total_inserted_nodes += inserted
        if inserted == 0:
            break
        refinement_depth += 1
        if refinement_depth >= MAXIMUM_BOUNDARY_REFINEMENT_DEPTH:
            raise RuntimeError(
                "adaptive boundary mesh exceeded refinement depth"
            )
    return grid, {
        "base_steps": base_steps,
        "adaptive_node_count": len(grid),
        "inserted_node_count": total_inserted_nodes,
        "refinement_depth": refinement_depth,
        "reciprocal_boundary_group_count": len(representatives),
        "maximum_refinement_half_step": maximum_half_step,
    }


def state_on_mesh(
    problem: dict[str, Any],
    coordinate: float,
    grid: list[complex],
) -> dict[str, Any]:
    original_cosines = M5030.homotopy_cosines
    original_selection = M5244.coupled_pair_selection
    minimum_margin = math.inf

    def capture_selection(
        representative_roots: list[complex],
        reciprocal_roots: list[complex],
        representative_reference: complex,
        reciprocal_reference: complex,
    ) -> tuple[complex, complex, float, float]:
        nonlocal minimum_margin
        for candidates in (
            representative_roots,
            reciprocal_roots,
        ):
            separations = [
                M5030.chordal_distance(first, second)
                for first_index, first in enumerate(candidates)
                for second in candidates[first_index + 1 :]
            ]
            if separations:
                minimum_margin = min(
                    minimum_margin, min(separations)
                )
        return original_selection(
            representative_roots,
            reciprocal_roots,
            representative_reference,
            reciprocal_reference,
        )

    M5030.homotopy_cosines = lambda *_: list(grid)
    M5244.coupled_pair_selection = capture_selection
    try:
        state = M5245.reciprocal_projective_state(
            problem,
            float(coordinate),
            len(grid) - 1,
        )
    finally:
        M5030.homotopy_cosines = original_cosines
        M5244.coupled_pair_selection = original_selection
    representative_suffix, reciprocal_suffix, source_delta = (
        M5239.source_winding_delta(problem)
    )
    dynamic_delta = (
        int(state["state_u"])
        if representative_suffix == "u"
        else int(state["state_v"])
    ) - (
        int(state["state_u"])
        if reciprocal_suffix == "u"
        else int(state["state_v"])
    )
    return {
        "u": int(state["state_u"]),
        "v": int(state["state_v"]),
        "dynamic_delta": dynamic_delta,
        "source_delta": source_delta,
        "multiplier": dynamic_delta / source_delta,
        "maximum_pair_projective_step": float(
            state["maximum_pair_projective_step"]
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
            minimum_margin if math.isfinite(minimum_margin) else 1.0
        ),
        "topology_steps": len(grid) - 1,
    }


def state_cache_contract(manifest: dict[str, Any]) -> dict[str, Any]:
    return {
        "marker": MARKER,
        "revision": REVISION,
        "manifest_hash": manifest["manifest_hash"],
        "base_resolution_ladder": list(BASE_RESOLUTION_LADDER),
        "minimum_accepted_base_resolution": (
            MINIMUM_ACCEPTED_BASE_RESOLUTION
        ),
        "maximum_projective_step": MAXIMUM_PROJECTIVE_STEP,
        "maximum_reciprocal_residual": (
            MAXIMUM_RECIPROCAL_RESIDUAL
        ),
        "maximum_boundary_reciprocal_residual": (
            MAXIMUM_BOUNDARY_RECIPROCAL_RESIDUAL
        ),
        "maximum_boundary_polynomial_residual": (
            MAXIMUM_BOUNDARY_POLYNOMIAL_RESIDUAL
        ),
        "maximum_step_ratio": MAXIMUM_STEP_RATIO,
        "boundary_refinement_target": BOUNDARY_REFINEMENT_TARGET,
        "maximum_boundary_refinement_depth": (
            MAXIMUM_BOUNDARY_REFINEMENT_DEPTH
        ),
    }


def load_state_cache(manifest: dict[str, Any]) -> dict[str, Any]:
    contract = state_cache_contract(manifest)
    if STATE_CACHE.exists():
        payload = read_json(STATE_CACHE)
        if payload.get("contract") == contract:
            return payload
        previous = payload.get("contract", {})
        comparable_keys = (
            "marker",
            "revision",
            "minimum_accepted_base_resolution",
            "maximum_projective_step",
            "maximum_reciprocal_residual",
            "maximum_boundary_reciprocal_residual",
            "maximum_boundary_polynomial_residual",
            "maximum_step_ratio",
            "boundary_refinement_target",
            "maximum_boundary_refinement_depth",
        )
        previous_ladder = tuple(
            previous.get("base_resolution_ladder", ())
        )
        current_ladder = tuple(
            contract["base_resolution_ladder"]
        )
        prefix_extension = (
            previous_ladder
            and current_ladder[: len(previous_ladder)]
            == previous_ladder
        )
        compatible = prefix_extension and all(
            previous.get(key) == contract.get(key)
            for key in comparable_keys
        )
        if compatible and isinstance(payload.get("states"), dict):
            payload["contract"] = contract
            atomic_json(STATE_CACHE, payload)
            return payload
    payload = {"contract": contract, "states": {}}
    atomic_json(STATE_CACHE, payload)
    return payload


def cached_mesh_state(
    problem: dict[str, Any],
    coordinate: float,
    base_steps: int,
    cache: dict[str, Any],
) -> tuple[dict[str, Any], bool, float]:
    key = "|".join(
        (
            problem["job"]["job_input_hash"],
            format(float(coordinate), ".17g"),
            str(base_steps),
        )
    )
    cached = cache["states"].get(key)
    if cached is not None:
        return dict(cached), True, 0.0
    started = time.perf_counter()
    grid, mesh = adaptive_boundary_mesh(
        problem, coordinate, base_steps
    )
    state = {
        **state_on_mesh(problem, coordinate, grid),
        **mesh,
    }
    elapsed = time.perf_counter() - started
    cache["states"][key] = state
    atomic_json(STATE_CACHE, cache)
    return state, False, elapsed


def adaptive_winding_state(
    problem: dict[str, Any],
    coordinate: float,
    cache: dict[str, Any],
    attempt_rows: list[dict[str, Any]],
) -> dict[str, Any]:
    previous: dict[str, Any] | None = None
    for base_steps in BASE_RESOLUTION_LADDER:
        state, cache_hit, elapsed = cached_mesh_state(
            problem,
            coordinate,
            base_steps,
            cache,
        )
        stable = (
            previous is not None
            and (int(state["u"]), int(state["v"]))
            == (int(previous["u"]), int(previous["v"]))
        )
        previous_step = (
            float(previous["maximum_pair_projective_step"])
            if previous is not None
            else None
        )
        ratio = (
            float(state["maximum_pair_projective_step"])
            / max(previous_step, 1.0e-300)
            if previous_step is not None
            else None
        )
        collision_projective_passed = (
            float(state["maximum_pair_projective_step"])
            <= MAXIMUM_PROJECTIVE_STEP
        )
        boundary_projective_passed = (
            float(state["maximum_boundary_projective_step"])
            <= MAXIMUM_PROJECTIVE_STEP
        )
        collision_reciprocal_passed = (
            float(state["maximum_reciprocal_product_residual"])
            <= MAXIMUM_RECIPROCAL_RESIDUAL
        )
        boundary_reciprocal_passed = (
            float(state["maximum_boundary_reciprocal_residual"])
            <= MAXIMUM_BOUNDARY_RECIPROCAL_RESIDUAL
        )
        boundary_polynomial_passed = (
            float(state["maximum_boundary_polynomial_residual"])
            <= MAXIMUM_BOUNDARY_POLYNOMIAL_RESIDUAL
        )
        ratio_passed = (
            ratio is not None and ratio <= MAXIMUM_STEP_RATIO
        )
        accepted = (
            base_steps >= MINIMUM_ACCEPTED_BASE_RESOLUTION
            and stable
            and collision_projective_passed
            and boundary_projective_passed
            and collision_reciprocal_passed
            and boundary_reciprocal_passed
            and boundary_polynomial_passed
            and ratio_passed
        )
        attempt_rows.append(
            {
                "job_id": problem["job"]["job_id"],
                "epsilon_id": problem["job"]["epsilon_id"],
                "component_id": problem["component_id"],
                "family": problem["case"]["family"],
                "decay_cosine": problem["event"]["decay_cosine"],
                "soft_cosine": float(coordinate),
                "base_topology_steps": base_steps,
                "adaptive_topology_steps": state[
                    "topology_steps"
                ],
                "adaptive_node_count": state[
                    "adaptive_node_count"
                ],
                "inserted_node_count": state[
                    "inserted_node_count"
                ],
                "refinement_depth": state["refinement_depth"],
                "state_u": state["u"],
                "state_v": state["v"],
                "dynamic_delta": state["dynamic_delta"],
                "dynamic_multiplier": state["multiplier"],
                "maximum_pair_projective_step": state[
                    "maximum_pair_projective_step"
                ],
                "maximum_boundary_projective_step": state[
                    "maximum_boundary_projective_step"
                ],
                "maximum_reciprocal_product_residual": state[
                    "maximum_reciprocal_product_residual"
                ],
                "maximum_boundary_reciprocal_residual": state[
                    "maximum_boundary_reciprocal_residual"
                ],
                "maximum_boundary_polynomial_residual": state[
                    "maximum_boundary_polynomial_residual"
                ],
                "minimum_alternate_branch_separation": state[
                    "minimum_alternate_branch_separation"
                ],
                "state_stable_from_previous": stable,
                "projective_step_ratio_from_previous": ratio,
                "collision_projective_passed": (
                    collision_projective_passed
                ),
                "boundary_projective_passed": (
                    boundary_projective_passed
                ),
                "collision_reciprocal_passed": (
                    collision_reciprocal_passed
                ),
                "boundary_reciprocal_passed": (
                    boundary_reciprocal_passed
                ),
                "boundary_polynomial_passed": (
                    boundary_polynomial_passed
                ),
                "step_ratio_passed": ratio_passed,
                "accepted": accepted,
                "state_cache_hit": cache_hit,
                "evaluation_elapsed_seconds": elapsed,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
        if accepted:
            return {
                **state,
                "accepted_topology_steps": state[
                    "topology_steps"
                ],
                "accepted_base_resolution": base_steps,
                "accepted_step_ratio": ratio,
            }
        previous = state
    raise RuntimeError(
        "reciprocal-projective state did not converge for "
        f"{problem['job']['job_id']} at {coordinate:.17g}"
    )


def prepare() -> tuple[
    dict[str, Any],
    dict[str, Any],
    list[dict[str, Any]],
    list[dict[str, Any]],
]:
    parent_5245 = read_json(RESULT_5245)
    parent_manifest, matches, base_jobs, _ = M5240.build_manifest()
    parent_5241 = read_json(M5243.MANIFEST_5241)
    node = next(
        row
        for row in parent_5241["outer_nodes"]
        if row["order9_node_id"] == TARGET_NODE_ID
    )
    event = dict(parent_manifest["target_event"])
    tracks, _ = M5240.build_outer_branch_tracks(matches, event)
    execution_node = {
        "outer_node_id": node["execution_node_id"],
        "master_index": int(node["master_index"]),
        "decay_cosine": float(node["decay_cosine"]),
    }
    jobs = M5240.material_node_jobs(
        execution_node, base_jobs, tracks
    )
    problems = [M5240.build_node_problem(job) for job in jobs]
    manifest = {
        "marker": MARKER,
        "revision": REVISION,
        "parent_checkpoint": 5245,
        "parent_decision": parent_5245["decision"],
        "parent_5240_manifest_hash": (
            parent_manifest["manifest_hash"]
        ),
        "target_node": node,
        "job_count": len(jobs),
        "base_resolution_ladder": list(
            BASE_RESOLUTION_LADDER
        ),
        "minimum_accepted_base_resolution": (
            MINIMUM_ACCEPTED_BASE_RESOLUTION
        ),
        "boundary_refinement_target": (
            BOUNDARY_REFINEMENT_TARGET
        ),
        "maximum_boundary_refinement_depth": (
            MAXIMUM_BOUNDARY_REFINEMENT_DEPTH
        ),
        "maximum_projective_step": MAXIMUM_PROJECTIVE_STEP,
        "maximum_reciprocal_residual": (
            MAXIMUM_RECIPROCAL_RESIDUAL
        ),
        "coarse_points": M5243.COARSE_POINTS,
        "bisection_steps": M5243.BISECTION_STEPS,
        "source_files": source_rows(),
        "jobs": [
            {
                "job_id": problem["job"]["job_id"],
                "job_input_hash": problem["job"][
                    "job_input_hash"
                ],
                "epsilon_id": problem["job"]["epsilon_id"],
                "component_id": problem["component_id"],
                "family": problem["case"]["family"],
            }
            for problem in problems
        ],
        "claim_boundary": {
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
            "reason": (
                "This rebuilds only the Q03 winding interval map. "
                "It does not yet rerun the Q03 inner integral."
            ),
        },
    }
    manifest["manifest_hash"] = serialized_hash(manifest)
    validation_5245 = read_csv(VALIDATION_5245)
    dry_checks = {
        "source_paths_exist_and_match": all(
            Path(row["path"]).exists()
            and digest(Path(row["path"])) == row["sha256"]
            for row in manifest["source_files"]
        ),
        "parent_5245_integrity_and_acceptance_pass": (
            parent_5245["integrity_passed"]
            and parent_5245["acceptance_passed"]
            and all(row["passed"] == "True" for row in validation_5245)
        ),
        "parent_decision_supersedes_legacy_Q03": (
            parent_5245["decision"]
            == (
                "SUPERSEDE_Q03_LEGACY_WINDING_CACHE__"
                "REBUILD_WITH_RECIPROCAL_PROJECTIVE_BOUNDARIES"
            )
        ),
        "target_node_exact": (
            node["order9_node_id"] == TARGET_NODE_ID
        ),
        "job_count_exact": len(problems) == EXPECTED_JOB_COUNT,
        "formal_digest_unchanged": (
            tree_digest(FORMAL) == FORMAL_BASELINE
        ),
        "claims_locked_false": all(
            not bool(manifest["claim_boundary"][field])
            for field in (
                "valid_for_numeric_UV_claim",
                "valid_for_local_GR_claim",
                "valid_for_full_MTS_claim",
            )
        ),
    }
    dry_run = {
        "marker": MARKER,
        "revision": REVISION,
        "dry_run_passed": all(dry_checks.values()),
        "checks": dry_checks,
        "manifest_hash": manifest["manifest_hash"],
        "target_node": TARGET_NODE_ID,
        "job_count": len(problems),
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    return manifest, dry_run, problems, jobs


def job_cache_path(problem: dict[str, Any]) -> Path:
    return JOB_CACHE / (
        serialized_hash(
            {
                "job_id": problem["job"]["job_id"],
                "job_input_hash": problem["job"][
                    "job_input_hash"
                ],
            }
        )
        + ".json"
    )


def derive_job(
    manifest: dict[str, Any],
    problem: dict[str, Any],
    state_cache: dict[str, Any],
) -> tuple[dict[str, Any], bool]:
    path = job_cache_path(problem)
    contract = {
        "marker": MARKER,
        "revision": REVISION,
        "manifest_hash": manifest["manifest_hash"],
        "job_input_hash": problem["job"]["job_input_hash"],
        "state_cache_contract": state_cache_contract(manifest),
    }
    if path.exists():
        payload = read_json(path)
        if (
            payload.get("contract") == contract
            and payload.get("status") == "COMPLETED"
        ):
            return payload["result"], True
        previous = payload.get("contract", {})
        previous_state = previous.get("state_cache_contract", {})
        current_state = contract["state_cache_contract"]
        previous_ladder = tuple(
            previous_state.get("base_resolution_ladder", ())
        )
        current_ladder = tuple(
            current_state["base_resolution_ladder"]
        )
        comparable_keys = (
            "marker",
            "revision",
            "minimum_accepted_base_resolution",
            "maximum_projective_step",
            "maximum_reciprocal_residual",
            "maximum_boundary_reciprocal_residual",
            "maximum_boundary_polynomial_residual",
            "maximum_step_ratio",
            "boundary_refinement_target",
            "maximum_boundary_refinement_depth",
        )
        compatible_extension = (
            payload.get("status") == "COMPLETED"
            and previous.get("marker") == contract["marker"]
            and previous.get("revision") == contract["revision"]
            and previous.get("job_input_hash")
            == contract["job_input_hash"]
            and previous_ladder
            and current_ladder[: len(previous_ladder)]
            == previous_ladder
            and all(
                previous_state.get(key)
                == current_state.get(key)
                for key in comparable_keys
            )
        )
        if compatible_extension:
            atomic_json(
                path,
                {
                    "contract": contract,
                    "status": "COMPLETED",
                    "result": payload["result"],
                },
            )
            return payload["result"], True
    attempts: list[dict[str, Any]] = []
    original = M5243.adaptive_winding_state
    M5243.adaptive_winding_state = adaptive_winding_state
    try:
        intervals, transitions, summary = (
            M5243.derive_adaptive_intervals(
                problem, state_cache, attempts
            )
        )
    finally:
        M5243.adaptive_winding_state = original
    result = {
        "job_id": problem["job"]["job_id"],
        "job_input_hash": problem["job"]["job_input_hash"],
        "epsilon_id": problem["job"]["epsilon_id"],
        "component_id": problem["component_id"],
        "family": problem["case"]["family"],
        "attempt_rows": attempts,
        "interval_rows": intervals,
        "transition_rows": transitions,
        "summary": summary,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(
        path,
        {
            "contract": contract,
            "status": "COMPLETED",
            "result": result,
        },
    )
    return result, False


def validation_rows(
    manifest: dict[str, Any],
    attempts: list[dict[str, Any]],
    intervals: list[dict[str, Any]],
    transitions: list[dict[str, Any]],
    summaries: list[dict[str, Any]],
    comparisons: list[dict[str, Any]],
    formal_digest: str,
    elapsed: float,
) -> list[dict[str, Any]]:
    accepted = [row for row in attempts if bool(row["accepted"])]
    evaluated_states = {
        (row["job_id"], float(row["soft_cosine"]))
        for row in attempts
    }
    accepted_states = {
        (row["job_id"], float(row["soft_cosine"]))
        for row in accepted
    }
    definitions = [
        (
            "integrity",
            "SOURCE_PATHS_EXIST_AND_MATCH",
            all(
                Path(row["path"]).exists()
                and digest(Path(row["path"])) == row["sha256"]
                for row in manifest["source_files"]
            ),
            len(manifest["source_files"]),
            "all source paths and hashes",
        ),
        (
            "integrity",
            "Q03_JOB_COUNT_EXACT",
            len(summaries) == EXPECTED_JOB_COUNT,
            len(summaries),
            EXPECTED_JOB_COUNT,
        ),
        (
            "acceptance",
            "EVERY_EVALUATED_STATE_ACCEPTED",
            evaluated_states == accepted_states,
            f"{len(accepted_states)}/{len(evaluated_states)}",
            f"{len(evaluated_states)}/{len(evaluated_states)}",
        ),
        (
            "acceptance",
            "ALL_COLLISION_PROJECTIVE_GATES_PASS",
            all(
                bool(row["collision_projective_passed"])
                for row in accepted
            ),
            max(
                float(row["maximum_pair_projective_step"])
                for row in accepted
            ),
            MAXIMUM_PROJECTIVE_STEP,
        ),
        (
            "acceptance",
            "ALL_BOUNDARY_PROJECTIVE_GATES_PASS",
            all(
                bool(row["boundary_projective_passed"])
                for row in accepted
            ),
            max(
                float(row["maximum_boundary_projective_step"])
                for row in accepted
            ),
            MAXIMUM_PROJECTIVE_STEP,
        ),
        (
            "acceptance",
            "ALL_RECIPROCAL_GATES_PASS",
            all(
                bool(row["collision_reciprocal_passed"])
                and bool(row["boundary_reciprocal_passed"])
                for row in accepted
            ),
            max(
                max(
                    float(
                        row[
                            "maximum_reciprocal_product_residual"
                        ]
                    ),
                    float(
                        row[
                            "maximum_boundary_reciprocal_residual"
                        ]
                    ),
                )
                for row in accepted
            ),
            MAXIMUM_RECIPROCAL_RESIDUAL,
        ),
        (
            "acceptance",
            "ALL_BOUNDARY_POLYNOMIAL_GATES_PASS",
            all(
                bool(row["boundary_polynomial_passed"])
                for row in accepted
            ),
            max(
                float(
                    row[
                        "maximum_boundary_polynomial_residual"
                    ]
                )
                for row in accepted
            ),
            MAXIMUM_BOUNDARY_POLYNOMIAL_RESIDUAL,
        ),
        (
            "acceptance",
            "ALL_INTERVAL_COVERAGES_CLOSE",
            all(
                float(row["coverage_residual"]) <= 2.0e-12
                for row in summaries
            ),
            max(
                float(row["coverage_residual"])
                for row in summaries
            ),
            2.0e-12,
        ),
        (
            "acceptance",
            "ALL_JOBS_HAVE_INTERVAL_MAPS",
            {
                row["job_id"] for row in intervals
            }
            == {row["job_id"] for row in summaries},
            len({row["job_id"] for row in intervals}),
            EXPECTED_JOB_COUNT,
        ),
        (
            "acceptance",
            "LEGACY_COMPARISON_COMPLETE",
            len(comparisons) == EXPECTED_JOB_COUNT,
            len(comparisons),
            EXPECTED_JOB_COUNT,
        ),
        (
            "integrity",
            "FORMALIZATION_WORKBENCH_UNCHANGED",
            formal_digest == FORMAL_BASELINE,
            formal_digest,
            FORMAL_BASELINE,
        ),
        (
            "integrity",
            "RUNTIME_BOUNDED",
            elapsed <= MAXIMUM_RUNTIME_SECONDS,
            elapsed,
            MAXIMUM_RUNTIME_SECONDS,
        ),
        (
            "integrity",
            "CLAIMS_REMAIN_FALSE",
            all(
                not bool(manifest["claim_boundary"][field])
                for field in (
                    "valid_for_numeric_UV_claim",
                    "valid_for_local_GR_claim",
                    "valid_for_full_MTS_claim",
                )
            ),
            "false,false,false",
            "false,false,false",
        ),
    ]
    return [
        {
            "checkpoint": 5246,
            "gate_kind": kind,
            "gate": gate,
            "passed": passed,
            "observed": observed,
            "required": required,
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
        }
        for kind, gate, passed, observed, required in definitions
    ]


def render_document(
    intervals: list[dict[str, Any]],
    transitions: list[dict[str, Any]],
    summaries: list[dict[str, Any]],
    comparisons: list[dict[str, Any]],
    validations: list[dict[str, Any]],
    cache_hits: int,
    elapsed: float,
) -> str:
    integrity_passed = all(
        bool(row["passed"])
        for row in validations
        if row["gate_kind"] == "integrity"
    )
    acceptance_passed = all(
        bool(row["passed"])
        for row in validations
        if row["gate_kind"] == "acceptance"
    )
    if not integrity_passed:
        decision = "INVALID_Q03_RECIPROCAL_PROJECTIVE_INTERVAL_REBUILD"
    elif acceptance_passed:
        decision = (
            "ADOPT_Q03_RECIPROCAL_PROJECTIVE_INTERVAL_MAP__"
            "RUN_CORRECTED_INNER_SLICE"
        )
    else:
        decision = (
            "HOLD_Q03_RECIPROCAL_PROJECTIVE_INTERVAL_MAP__"
            "LOCALIZE_FAILED_GATE"
        )
    state_measure: dict[str, float] = {}
    for row in intervals:
        state = format(float(row["dynamic_multiplier"]), ".12g")
        state_measure[state] = state_measure.get(state, 0.0) + (
            float(row["interval_upper"])
            - float(row["interval_lower"])
        )
    changed_jobs = sum(
        not bool(row["maps_identical_up_to_measure"])
        for row in comparisons
    )
    return "\n".join(
        [
            "# 5246 — Q03 reciprocal-projective interval topology rebuild",
            "",
            "## Method",
            "",
            (
                "Each Q03 state uses a shared homotopy mesh for the "
                "coupled collision roots and reciprocal chamber endpoints. "
                "The base 2048/4096 ladder is locally refined only where "
                "a boundary-pair half-step exceeds 0.025. Acceptance "
                "requires identical winding integers at consecutive base "
                "resolutions and every collision, boundary, reciprocal, "
                "polynomial, and step-ratio gate."
            ),
            "",
            "## Results",
            "",
            f"- Q03 material jobs rebuilt: `{len(summaries)}`.",
            f"- Corrected interval rows: `{len(intervals)}`.",
            f"- Corrected transition brackets: `{len(transitions)}`.",
            f"- Legacy maps changed: `{changed_jobs}/{len(comparisons)}`.",
            f"- Corrected multiplier measure: `{json.dumps(state_measure, sort_keys=True)}`.",
            f"- Job-cache hits: `{cache_hits}/{len(summaries)}`.",
            f"- Runtime: `{elapsed:.3f} s`.",
            "",
            "## Decision",
            "",
            f"`{decision}`",
            "",
            "## Claim boundary",
            "",
            (
                "This establishes only the corrected Q03 interval "
                "topology. It does not yet alter a published coefficient, "
                "rerun Q05, derive local GR, or validate full MTS."
            ),
            "",
            "## Next exact target",
            "",
            (
                "Use these exact Q03 interval rows to reclassify active "
                "poles, refit only the retained residues, rerun the "
                "regulated inner quadrature, and compare the corrected "
                "Q03 value with the 5241 fixed-resolution value."
                if acceptance_passed
                else
                "Resolve the first failed Q03 topology gate before any "
                "inner-slice calculation."
            ),
            "",
        ]
    )


def remove_project_pycache() -> None:
    target = POST / "scripts" / "__pycache__"
    if target.exists():
        shutil.rmtree(target)


def execute() -> dict[str, Any]:
    started = time.perf_counter()
    manifest, dry_run, problems, _ = prepare()
    atomic_json(MANIFEST, manifest)
    atomic_json(DRY_RUN, dry_run)
    if not dry_run["dry_run_passed"]:
        failed = [
            key
            for key, passed in dry_run["checks"].items()
            if not passed
        ]
        raise RuntimeError(f"5246 dry run failed: {failed}")
    state_cache = load_state_cache(manifest)
    JOB_CACHE.mkdir(parents=True, exist_ok=True)
    results: list[dict[str, Any]] = []
    cache_hits = 0
    for problem in problems:
        result, cache_hit = derive_job(
            manifest, problem, state_cache
        )
        results.append(result)
        cache_hits += int(cache_hit)
        write_csv(
            ATTEMPT_ROWS,
            [
                row
                for local in results
                for row in local["attempt_rows"]
            ],
        )
        write_csv(
            INTERVAL_ROWS,
            [
                row
                for local in results
                for row in local["interval_rows"]
            ],
        )
        write_csv(
            TRANSITION_ROWS,
            [
                row
                for local in results
                for row in local["transition_rows"]
            ],
        )
    attempts = [
        row for result in results for row in result["attempt_rows"]
    ]
    intervals = [
        row for result in results for row in result["interval_rows"]
    ]
    transitions = [
        row
        for result in results
        for row in result["transition_rows"]
    ]
    summaries = [
        {
            **result["summary"],
            "job_cache_hit": False,
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
        }
        for result in results
    ]
    fixed_rows = read_csv(M5243.WINDING_5241)
    comparisons = M5243.compare_intervals(
        TARGET_NODE_ID, intervals, fixed_rows
    )
    formal_digest = tree_digest(FORMAL)
    elapsed = time.perf_counter() - started
    validations = validation_rows(
        manifest,
        attempts,
        intervals,
        transitions,
        summaries,
        comparisons,
        formal_digest,
        elapsed,
    )
    write_csv(ATTEMPT_ROWS, attempts)
    write_csv(INTERVAL_ROWS, intervals)
    write_csv(TRANSITION_ROWS, transitions)
    write_csv(JOB_ROWS, summaries)
    write_csv(COMPARISON_ROWS, comparisons)
    write_csv(VALIDATION, validations)
    atomic_text(
        DOCUMENT,
        render_document(
            intervals,
            transitions,
            summaries,
            comparisons,
            validations,
            cache_hits,
            elapsed,
        ),
    )
    integrity_passed = all(
        bool(row["passed"])
        for row in validations
        if row["gate_kind"] == "integrity"
    )
    acceptance_passed = all(
        bool(row["passed"])
        for row in validations
        if row["gate_kind"] == "acceptance"
    )
    decision = (
        "INVALID_Q03_RECIPROCAL_PROJECTIVE_INTERVAL_REBUILD"
        if not integrity_passed
        else (
            "ADOPT_Q03_RECIPROCAL_PROJECTIVE_INTERVAL_MAP__"
            "RUN_CORRECTED_INNER_SLICE"
            if acceptance_passed
            else (
                "HOLD_Q03_RECIPROCAL_PROJECTIVE_INTERVAL_MAP__"
                "LOCALIZE_FAILED_GATE"
            )
        )
    )
    result = {
        "marker": MARKER,
        "revision": REVISION,
        "dry_run": dry_run,
        "manifest_hash": manifest["manifest_hash"],
        "decision": decision,
        "integrity_passed": integrity_passed,
        "acceptance_passed": acceptance_passed,
        "job_count": len(summaries),
        "state_evaluation_count": len(
            {
                (row["job_id"], float(row["soft_cosine"]))
                for row in attempts
            }
        ),
        "interval_count": len(intervals),
        "transition_count": len(transitions),
        "changed_job_count": sum(
            not bool(row["maps_identical_up_to_measure"])
            for row in comparisons
        ),
        "job_cache_hit_count": cache_hits,
        "formalization_workbench_digest": formal_digest,
        "elapsed_seconds": elapsed,
        "outputs": [
            str(path)
            for path in (
                MANIFEST,
                DRY_RUN,
                STATE_CACHE,
                ATTEMPT_ROWS,
                INTERVAL_ROWS,
                TRANSITION_ROWS,
                JOB_ROWS,
                COMPARISON_ROWS,
                VALIDATION,
                DOCUMENT,
            )
        ],
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(RESULT, result)
    remove_project_pycache()
    if not integrity_passed:
        failed = [
            row["gate"]
            for row in validations
            if row["gate_kind"] == "integrity"
            and not row["passed"]
        ]
        raise RuntimeError(f"5246 integrity validation failed: {failed}")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="validate the Q03 interval-rebuild manifest only",
    )
    arguments = parser.parse_args()
    if arguments.dry_run:
        manifest, dry_run, _, _ = prepare()
        atomic_json(MANIFEST, manifest)
        atomic_json(DRY_RUN, dry_run)
        print(json.dumps(dry_run, indent=2, sort_keys=True))
        return
    print(json.dumps(execute(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
