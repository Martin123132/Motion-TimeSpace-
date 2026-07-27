from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import math
import shutil
import sys
import time
from collections import defaultdict
from pathlib import Path
from typing import Any

import numpy as np


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE = POST / "source-intake" / "functional_rg" / "5243"
SOURCE_5241 = POST / "source-intake" / "functional_rg" / "5241"
RESIDUALS = POST / "source-intake" / "mts_residuals"
NODE_CACHE = SOURCE / "node-cache"

SCRIPT_5242 = (
    POST
    / "scripts"
    / "Y5_R2FR_5242_homotopy_branch_resolution_or_collision_classifier.py"
)
RESULT_5242 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5242"
    / "homotopy_branch_resolution_result.json"
)
MANIFEST_5241 = SOURCE_5241 / "decay_angle_order9_manifest.json"
WINDING_5241 = SOURCE_5241 / "decay_angle_order9_winding_intervals.csv"
NODE_ROWS_5241 = SOURCE_5241 / "decay_angle_order9_node_summary.csv"
VALIDATION_5242 = (
    RESIDUALS / "P8_Y5_BRR545_5242_VALIDATION.csv"
)

MANIFEST = SOURCE / "adaptive_winding_rebuild_manifest.json"
DRY_RUN = SOURCE / "adaptive_winding_rebuild_dry_run.json"
RESULT = SOURCE / "adaptive_winding_rebuild_result.json"
STATE_CACHE = SOURCE / "adaptive_homotopy_state_cache.json"
ATTEMPT_ROWS = SOURCE / "adaptive_homotopy_resolution_attempts.csv"
INTERVAL_ROWS = SOURCE / "adaptive_winding_intervals.csv"
TRANSITION_ROWS = SOURCE / "adaptive_winding_transition_brackets.csv"
COMPARISON_ROWS = SOURCE / "fixed_vs_adaptive_interval_comparison.csv"
NODE_ROWS = SOURCE / "corrected_Q03_Q05_node_summary.csv"
ZERO_ROWS = SOURCE / "corrected_Q03_Q05_structural_zero_audit.csv"
CLOSURE_ROWS = SOURCE / "corrected_Q03_Q05_dynamic_closure.csv"
POLE_ROWS = SOURCE / "corrected_Q03_Q05_pole_catalog.csv"
RESIDUE_ROWS = SOURCE / "corrected_Q03_Q05_residue_fits.csv"
QUADRATURE_ROWS = SOURCE / "corrected_Q03_Q05_inner_quadrature.csv"
EXTRAPOLATION_ROWS = (
    SOURCE / "corrected_Q03_Q05_regulator_extrapolation.csv"
)
VALIDATION = RESIDUALS / "P8_Y5_BRR545_5243_VALIDATION.csv"
DOCUMENT = (
    POST
    / "5243-Y5-R2FR-adaptive-homotopy-winding-rebuild-and-Q03-Q05-slice-rerun.md"
)

MARKER = "MTS_5243_ADAPTIVE_HOMOTOPY_WINDING_REBUILD_Q03_Q05"
REVISION = "adaptive-homotopy-winding-rebuild-Q03-Q05-v1"
FORMAL_BASELINE = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)

TARGET_NODE_IDS = ("Q03", "Q05")
RESOLUTION_LADDER = (1024, 2048, 4096, 8192, 16384, 32768)
MINIMUM_ACCEPTED_RESOLUTION = 4096
MAXIMUM_PROJECTIVE_STEP = 5.0e-2
MAXIMUM_RECIPROCAL_RESIDUAL = 2.0e-8
MAXIMUM_STEP_RATIO = 0.65
COARSE_POINTS = 25
BISECTION_STEPS = 26
MAXIMUM_DYNAMIC_CLOSURE_RESIDUAL = 2.0e-10
MAXIMUM_RUNTIME_SECONDS = 4.0 * 60.0 * 60.0
EXPECTED_BASE_JOBS = 12
EXPECTED_NODE_COUNT = 2
EXPECTED_TOTAL_JOBS = EXPECTED_BASE_JOBS * EXPECTED_NODE_COUNT


def load_module(path: Path, name: str) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5242 = load_module(SCRIPT_5242, "mts_5242_for_5243")
M5241 = M5242.M5241
M5240 = M5242.M5240
M5239 = M5242.M5239


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(chunk)
    return value.hexdigest()


def tree_digest(path: Path) -> str:
    value = hashlib.sha256()
    for item in sorted(candidate for candidate in path.rglob("*") if candidate.is_file()):
        value.update(str(item.relative_to(path)).replace("\\", "/").encode())
        value.update(digest(item).encode())
    return value.hexdigest()


def serialized_hash(value: Any) -> str:
    encoded = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    ).encode()
    return hashlib.sha256(encoded).hexdigest()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def atomic_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(value, encoding="utf-8")
    temporary.replace(path)


def atomic_json(path: Path, value: Any) -> None:
    atomic_text(path, json.dumps(value, indent=2, sort_keys=True) + "\n")


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        atomic_text(path, "")
        return
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
    temporary.replace(path)


def complex_value(value: Any) -> complex:
    return M5240.complex_value(value)


def complex_row(value: complex) -> dict[str, float]:
    return {"real": float(value.real), "imaginary": float(value.imag)}


def source_rows() -> list[dict[str, str]]:
    paths = (
        SCRIPT_5242,
        RESULT_5242,
        MANIFEST_5241,
        WINDING_5241,
        NODE_ROWS_5241,
        VALIDATION_5242,
        M5240.SCRIPT_5239,
        M5241.SCRIPT_5240,
    )
    return [
        {"path": str(path), "sha256": digest(path)} for path in paths
    ]


def build_manifest() -> tuple[
    dict[str, Any],
    dict[str, Any],
    list[dict[str, Any]],
    list[dict[str, Any]],
]:
    parent_manifest, matches, base_jobs, _ = M5240.build_manifest()
    parent_5241 = read_json(MANIFEST_5241)
    nodes = [
        row
        for row in parent_5241["outer_nodes"]
        if row["order9_node_id"] in TARGET_NODE_IDS
    ]
    nodes.sort(key=lambda row: TARGET_NODE_IDS.index(row["order9_node_id"]))
    jobs = [
        {
            "order9_node_id": node["order9_node_id"],
            "execution_node_id": node["execution_node_id"],
            "decay_cosine": node["decay_cosine"],
            "epsilon_id": job["epsilon_id"],
            "component_id": job["component_id"],
            "family": job["family"],
            "owner_summand": job["owner_summand"],
            "base_job_id": job["job_id"],
            "base_job_hash": job["job_input_hash"],
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
        }
        for node in nodes
        for job in base_jobs
    ]
    manifest = {
        "marker": MARKER,
        "revision": REVISION,
        "parent_checkpoint": 5242,
        "parent_decision": read_json(RESULT_5242)["decision"],
        "parent_5240_manifest_hash": parent_manifest["manifest_hash"],
        "target_nodes": nodes,
        "target_node_count": len(nodes),
        "base_job_count": len(base_jobs),
        "total_job_count": len(jobs),
        "resolution_ladder": list(RESOLUTION_LADDER),
        "minimum_accepted_resolution": MINIMUM_ACCEPTED_RESOLUTION,
        "maximum_projective_step": MAXIMUM_PROJECTIVE_STEP,
        "maximum_reciprocal_residual": MAXIMUM_RECIPROCAL_RESIDUAL,
        "maximum_step_ratio": MAXIMUM_STEP_RATIO,
        "coarse_points": COARSE_POINTS,
        "bisection_steps": BISECTION_STEPS,
        "source_files": source_rows(),
        "jobs": jobs,
        "claim_boundary": {
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
            "reason": (
                "Only the Q03/Q05 fixed-soft-energy angular nodes are "
                "rebuilt; the full order-9 cubature is not rerun here."
            ),
        },
    }
    manifest["manifest_hash"] = serialized_hash(manifest)
    return manifest, parent_manifest, matches, base_jobs


def write_manifest_and_dry_run() -> dict[str, Any]:
    manifest, parent_manifest, matches, base_jobs = build_manifest()
    validation_5242 = read_csv(VALIDATION_5242)
    checks = {
        "source_paths_exist_and_match": all(
            Path(row["path"]).exists()
            and digest(Path(row["path"])) == row["sha256"]
            for row in manifest["source_files"]
        ),
        "parent_5242_all_gates_pass": all(
            row["passed"] == "True" for row in validation_5242
        ),
        "parent_resolution_decision_adopted": (
            manifest["parent_decision"]
            == "ADOPT_HIGHER_HOMOTOPY_RESOLUTION"
        ),
        "target_nodes_exact": (
            [row["order9_node_id"] for row in manifest["target_nodes"]]
            == list(TARGET_NODE_IDS)
        ),
        "job_count_exact": (
            len(base_jobs) == EXPECTED_BASE_JOBS
            and manifest["total_job_count"] == EXPECTED_TOTAL_JOBS
        ),
        "component_contract_preserved": (
            len(matches) == M5240.EXPECTED_SAFE_COMPONENT_COUNT
            and parent_manifest["material_component_count"]
            == M5240.EXPECTED_MATERIAL_COMPONENT_COUNT
        ),
        "resolution_contract_stricter_than_parent": (
            max(RESOLUTION_LADDER) == 32768
            and MAXIMUM_PROJECTIVE_STEP
            == M5239.DYNAMIC_PROJECTIVE_STEP_LIMIT
            and MAXIMUM_RECIPROCAL_RESIDUAL <= 2.0e-8
        ),
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
    report = {
        "marker": MARKER,
        "revision": REVISION,
        "dry_run_passed": all(checks.values()),
        "checks": checks,
        "manifest_hash": manifest["manifest_hash"],
        "target_node_count": manifest["target_node_count"],
        "total_job_count": manifest["total_job_count"],
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(MANIFEST, manifest)
    atomic_json(DRY_RUN, report)
    if not report["dry_run_passed"]:
        failed = [key for key, passed in checks.items() if not passed]
        raise RuntimeError(f"5243 dry run failed: {failed}")
    return report


def state_cache_contract(manifest: dict[str, Any]) -> dict[str, Any]:
    return {
        "marker": MARKER,
        "revision": REVISION,
        "manifest_hash": manifest["manifest_hash"],
        "resolution_ladder": list(RESOLUTION_LADDER),
        "minimum_accepted_resolution": MINIMUM_ACCEPTED_RESOLUTION,
        "maximum_projective_step": MAXIMUM_PROJECTIVE_STEP,
        "maximum_reciprocal_residual": MAXIMUM_RECIPROCAL_RESIDUAL,
        "maximum_step_ratio": MAXIMUM_STEP_RATIO,
    }


def load_state_cache(manifest: dict[str, Any]) -> dict[str, Any]:
    contract = state_cache_contract(manifest)
    if STATE_CACHE.exists():
        payload = read_json(STATE_CACHE)
        if payload.get("contract") == contract:
            return payload
    payload = {"contract": contract, "states": {}}
    atomic_json(STATE_CACHE, payload)
    return payload


def state_key(state: dict[str, Any]) -> tuple[int, int]:
    return int(state["u"]), int(state["v"])


def cached_resolution_state(
    problem: dict[str, Any],
    coordinate: float,
    steps: int,
    cache: dict[str, Any],
) -> tuple[dict[str, Any], bool, float]:
    key = "|".join(
        (
            problem["job"]["job_input_hash"],
            format(float(coordinate), ".17g"),
            str(steps),
        )
    )
    cached = cache["states"].get(key)
    if cached is not None:
        return dict(cached), True, 0.0
    started = time.perf_counter()
    state = M5239.winding_state(problem, float(coordinate), steps)
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
    for steps in RESOLUTION_LADDER:
        state, cache_hit, elapsed = cached_resolution_state(
            problem, coordinate, steps, cache
        )
        stable = (
            previous is not None
            and state_key(state) == state_key(previous)
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
        projective_passed = (
            float(state["maximum_pair_projective_step"])
            <= MAXIMUM_PROJECTIVE_STEP
        )
        reciprocal_passed = (
            float(state["maximum_reciprocal_product_residual"])
            <= MAXIMUM_RECIPROCAL_RESIDUAL
        )
        ratio_passed = (
            ratio is not None and ratio <= MAXIMUM_STEP_RATIO
        )
        accepted = (
            steps >= MINIMUM_ACCEPTED_RESOLUTION
            and stable
            and projective_passed
            and reciprocal_passed
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
                "topology_steps": steps,
                "state_u": state["u"],
                "state_v": state["v"],
                "dynamic_delta": state["dynamic_delta"],
                "dynamic_multiplier": state["multiplier"],
                "maximum_pair_projective_step": state[
                    "maximum_pair_projective_step"
                ],
                "maximum_reciprocal_product_residual": state[
                    "maximum_reciprocal_product_residual"
                ],
                "minimum_alternate_branch_separation": state[
                    "minimum_alternate_branch_separation"
                ],
                "state_stable_from_previous": stable,
                "projective_step_ratio_from_previous": ratio,
                "projective_passed": projective_passed,
                "reciprocal_passed": reciprocal_passed,
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
                "accepted_topology_steps": steps,
                "accepted_step_ratio": ratio,
            }
        previous = state
    raise RuntimeError(
        f"adaptive winding state did not converge for "
        f"{problem['job']['job_id']} at {coordinate:.17g}"
    )


def derive_adaptive_intervals(
    problem: dict[str, Any],
    cache: dict[str, Any],
    attempt_rows: list[dict[str, Any]],
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[str, Any],
]:
    lower = float(problem["job"]["scan_minimum"])
    upper = float(problem["job"]["scan_maximum"])
    base = float(
        problem["event"][problem["case"]["outer_coordinate"]]
    )
    coordinates = sorted(
        {
            *np.linspace(lower, upper, COARSE_POINTS).tolist(),
            base,
        }
    )
    local_cache: dict[float, dict[str, Any]] = {}

    def evaluate(coordinate: float) -> dict[str, Any]:
        key = float(coordinate)
        if key not in local_cache:
            local_cache[key] = adaptive_winding_state(
                problem, key, cache, attempt_rows
            )
        return local_cache[key]

    coarse_states = [evaluate(coordinate) for coordinate in coordinates]
    transition_brackets: list[dict[str, Any]] = []

    def refine_transitions(
        left: float,
        left_state: dict[str, Any],
        right: float,
        right_state: dict[str, Any],
        depth: int,
        coarse_left: float,
        coarse_right: float,
    ) -> None:
        if depth >= BISECTION_STEPS:
            if state_key(left_state) == state_key(right_state):
                return
            transition_brackets.append(
                {
                    "job_id": problem["job"]["job_id"],
                    "epsilon_id": problem["job"]["epsilon_id"],
                    "component_id": problem["component_id"],
                    "family": problem["case"]["family"],
                    "coarse_left": coarse_left,
                    "coarse_right": coarse_right,
                    "left": left,
                    "right": right,
                    "center": 0.5 * (left + right),
                    "width": right - left,
                    "left_state_u": state_key(left_state)[0],
                    "left_state_v": state_key(left_state)[1],
                    "right_state_u": state_key(right_state)[0],
                    "right_state_v": state_key(right_state)[1],
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
            )
            return
        midpoint = 0.5 * (left + right)
        midpoint_state = evaluate(midpoint)
        if state_key(left_state) != state_key(midpoint_state):
            refine_transitions(
                left,
                left_state,
                midpoint,
                midpoint_state,
                depth + 1,
                coarse_left,
                coarse_right,
            )
        if state_key(midpoint_state) != state_key(right_state):
            refine_transitions(
                midpoint,
                midpoint_state,
                right,
                right_state,
                depth + 1,
                coarse_left,
                coarse_right,
            )

    for index in range(len(coordinates) - 1):
        left = float(coordinates[index])
        right = float(coordinates[index + 1])
        refine_transitions(
            left,
            coarse_states[index],
            right,
            coarse_states[index + 1],
            0,
            left,
            right,
        )
    transition_brackets.sort(key=lambda row: float(row["center"]))
    boundaries = sorted(
        {
            lower,
            *[
                float(row["center"]) for row in transition_brackets
            ],
            upper,
        }
    )
    representative_suffix, reciprocal_suffix, source_delta = (
        M5239.source_winding_delta(problem)
    )
    rows: list[dict[str, Any]] = []
    for interval_index in range(len(boundaries) - 1):
        interval_lower = float(boundaries[interval_index])
        interval_upper = float(boundaries[interval_index + 1])
        midpoint = 0.5 * (interval_lower + interval_upper)
        state = evaluate(midpoint)
        rows.append(
            {
                "job_id": problem["job"]["job_id"],
                "epsilon_id": problem["job"]["epsilon_id"],
                "component_id": problem["component_id"],
                "family": problem["case"]["family"],
                "owner_summand": problem["job"]["owner_summand"],
                "interval_index": interval_index + 1,
                "interval_lower": interval_lower,
                "interval_upper": interval_upper,
                "interval_midpoint": midpoint,
                "state_u": state["u"],
                "state_v": state["v"],
                "representative_suffix": representative_suffix,
                "reciprocal_suffix": reciprocal_suffix,
                "source_winding_delta": source_delta,
                "dynamic_winding_delta": state["dynamic_delta"],
                "dynamic_multiplier": state["multiplier"],
                "maximum_pair_projective_step": state[
                    "maximum_pair_projective_step"
                ],
                "maximum_reciprocal_product_residual": state[
                    "maximum_reciprocal_product_residual"
                ],
                "minimum_alternate_branch_separation": state[
                    "minimum_alternate_branch_separation"
                ],
                "accepted_topology_steps": state[
                    "accepted_topology_steps"
                ],
                "accepted_step_ratio": state["accepted_step_ratio"],
                "left_transition_uncertainty": (
                    transition_brackets[interval_index - 1]["width"]
                    if interval_index > 0
                    else 0.0
                ),
                "right_transition_uncertainty": (
                    transition_brackets[interval_index]["width"]
                    if interval_index < len(transition_brackets)
                    else 0.0
                ),
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    coverage = sum(
        float(row["interval_upper"]) - float(row["interval_lower"])
        for row in rows
    )
    if abs(coverage - (upper - lower)) > 2.0e-12:
        raise RuntimeError(
            f"adaptive interval coverage failed for "
            f"{problem['job']['job_id']}"
        )
    summary = {
        "job_id": problem["job"]["job_id"],
        "epsilon_id": problem["job"]["epsilon_id"],
        "component_id": problem["component_id"],
        "family": problem["case"]["family"],
        "adaptive_interval_count": len(rows),
        "adaptive_transition_count": len(transition_brackets),
        "maximum_accepted_topology_steps": max(
            int(row["accepted_topology_steps"]) for row in rows
        ),
        "maximum_accepted_projective_step": max(
            float(row["maximum_pair_projective_step"]) for row in rows
        ),
        "maximum_accepted_reciprocal_residual": max(
            float(row["maximum_reciprocal_product_residual"])
            for row in rows
        ),
        "coverage_residual": abs(coverage - (upper - lower)),
    }
    return rows, transition_brackets, summary


def interval_state(
    rows: list[dict[str, Any]], coordinate: float
) -> float:
    for index, row in enumerate(rows):
        lower = float(row["interval_lower"])
        upper = float(row["interval_upper"])
        if lower <= coordinate < upper or (
            index == len(rows) - 1 and coordinate <= upper
        ):
            return float(row["dynamic_multiplier"])
    raise RuntimeError(f"coordinate {coordinate} outside intervals")


def state_measure(rows: list[dict[str, Any]]) -> dict[str, float]:
    result: defaultdict[str, float] = defaultdict(float)
    for row in rows:
        key = format(float(row["dynamic_multiplier"]), ".12g")
        result[key] += (
            float(row["interval_upper"])
            - float(row["interval_lower"])
        )
    return dict(sorted(result.items()))


def interval_mismatch_measure(
    fixed_rows: list[dict[str, Any]],
    adaptive_rows: list[dict[str, Any]],
) -> float:
    boundaries = sorted(
        {
            *[
                float(row["interval_lower"]) for row in fixed_rows
            ],
            *[
                float(row["interval_upper"]) for row in fixed_rows
            ],
            *[
                float(row["interval_lower"]) for row in adaptive_rows
            ],
            *[
                float(row["interval_upper"]) for row in adaptive_rows
            ],
        }
    )
    mismatch = 0.0
    for lower, upper in zip(boundaries[:-1], boundaries[1:]):
        midpoint = 0.5 * (lower + upper)
        if not math.isclose(
            interval_state(fixed_rows, midpoint),
            interval_state(adaptive_rows, midpoint),
            abs_tol=1.0e-12,
        ):
            mismatch += upper - lower
    return mismatch


def compare_intervals(
    node_id: str,
    adaptive_rows: list[dict[str, Any]],
    fixed_rows_all: list[dict[str, str]],
) -> list[dict[str, Any]]:
    grouped_adaptive = M5239.interval_rows_by_job(adaptive_rows)
    rows: list[dict[str, Any]] = []
    for job_id, new_rows in sorted(grouped_adaptive.items()):
        sample = new_rows[0]
        fixed_rows = [
            row
            for row in fixed_rows_all
            if row["order9_node_id"] == node_id
            and row["epsilon_id"] == sample["epsilon_id"]
            and row["component_id"] == sample["component_id"]
        ]
        fixed_rows.sort(key=lambda row: float(row["interval_lower"]))
        mismatch = interval_mismatch_measure(fixed_rows, new_rows)
        rows.append(
            {
                "order9_node_id": node_id,
                "job_id": job_id,
                "epsilon_id": sample["epsilon_id"],
                "component_id": sample["component_id"],
                "family": sample["family"],
                "fixed_interval_count": len(fixed_rows),
                "adaptive_interval_count": len(new_rows),
                "interval_count_change": len(new_rows) - len(fixed_rows),
                "fixed_state_measure": json.dumps(
                    state_measure(fixed_rows), sort_keys=True
                ),
                "adaptive_state_measure": json.dumps(
                    state_measure(new_rows), sort_keys=True
                ),
                "multiplier_mismatch_measure": mismatch,
                "maps_identical_up_to_measure": mismatch <= 2.0e-10,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    return rows


def node_cache_contract(
    manifest: dict[str, Any],
    node: dict[str, Any],
    jobs: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "marker": MARKER,
        "revision": REVISION,
        "manifest_hash": manifest["manifest_hash"],
        "order9_node_id": node["order9_node_id"],
        "decay_cosine": node["decay_cosine"],
        "job_hashes": sorted(job["job_input_hash"] for job in jobs),
        "state_cache_contract": state_cache_contract(manifest),
    }


def run_corrected_node(
    manifest: dict[str, Any],
    node: dict[str, Any],
    base_jobs: list[dict[str, Any]],
    matches: list[dict[str, Any]],
    tracks: dict[str, dict[str, Any]],
    event: dict[str, Any],
    state_cache: dict[str, Any],
    fixed_rows_all: list[dict[str, str]],
) -> tuple[dict[str, Any], bool]:
    execution_node = {
        "outer_node_id": node["execution_node_id"],
        "master_index": int(node["master_index"]),
        "decay_cosine": float(node["decay_cosine"]),
    }
    jobs = M5240.material_node_jobs(
        execution_node, base_jobs, tracks
    )
    contract = node_cache_contract(manifest, node, jobs)
    cache_path = NODE_CACHE / f"{node['order9_node_id']}.json"
    if cache_path.exists():
        payload = read_json(cache_path)
        if (
            payload.get("contract") == contract
            and payload.get("status") == "COMPLETED"
        ):
            return payload["result"], True
    started = time.perf_counter()
    problems_by_epsilon: dict[str, list[dict[str, Any]]] = {
        epsilon_id: [] for epsilon_id in M5239.EPSILON_IDS
    }
    for job in jobs:
        problems_by_epsilon[job["epsilon_id"]].append(
            M5240.build_node_problem(job)
        )
    all_problems = [
        problem
        for epsilon_id in M5239.EPSILON_IDS
        for problem in problems_by_epsilon[epsilon_id]
    ]
    attempt_rows: list[dict[str, Any]] = []
    interval_rows: list[dict[str, Any]] = []
    transition_rows: list[dict[str, Any]] = []
    interval_summaries: list[dict[str, Any]] = []
    for problem in all_problems:
        local_rows, local_transitions, local_summary = (
            derive_adaptive_intervals(
                problem, state_cache, attempt_rows
            )
        )
        interval_rows.extend(local_rows)
        transition_rows.extend(local_transitions)
        interval_summaries.append(local_summary)
    intervals_by_job = M5239.interval_rows_by_job(interval_rows)
    comparison_rows = compare_intervals(
        node["order9_node_id"], interval_rows, fixed_rows_all
    )

    scan_rows: list[dict[str, Any]] = []
    poles: list[dict[str, Any]] = []
    topology_rows: list[dict[str, Any]] = []
    poles_by_job: dict[str, list[dict[str, Any]]] = {}
    for problem in all_problems:
        _, local_scan, local_poles, local_topology = (
            M5239.scan_problem(problem)
        )
        for pole in local_poles:
            pole["source_causal_family_active"] = bool(
                pole["causal_family_active"]
            )
            interval = M5239.interval_for_coordinate(
                problem,
                float(pole["real_axis_center"]),
                intervals_by_job,
            )
            multiplier = float(interval["dynamic_multiplier"])
            pole["dynamic_winding_multiplier"] = multiplier
            pole["causal_family_active"] = abs(multiplier) > 1.0e-12
        pole_lookup = {row["pole_id"]: row for row in local_poles}
        for row in local_topology:
            pole = pole_lookup[row["pole_id"]]
            row["source_causal_family_active"] = bool(
                row["causal_family_active"]
            )
            row["dynamic_winding_multiplier"] = pole[
                "dynamic_winding_multiplier"
            ]
            row["causal_family_active"] = pole[
                "causal_family_active"
            ]
        poles_by_job[problem["job"]["job_id"]] = local_poles
        scan_rows.extend(local_scan)
        poles.extend(local_poles)
        topology_rows.extend(local_topology)
    fits: list[dict[str, Any]] = []
    for epsilon_id in M5239.EPSILON_IDS:
        regulator_poles = [
            row for row in poles if row["epsilon_id"] == epsilon_id
        ]
        global_centers = [
            float(row["real_axis_center"]) for row in regulator_poles
        ]
        for problem in problems_by_epsilon[epsilon_id]:
            fits.extend(
                M5239.fit_full_component_residues(
                    problem,
                    poles_by_job[problem["job"]["job_id"]],
                    global_centers,
                    intervals_by_job,
                )
            )
    if not all(bool(row["fit_passed"]) for row in fits):
        raise RuntimeError(
            f"corrected residue fit failed at "
            f"{node['order9_node_id']}"
        )
    closure_rows = M5240.dynamic_closure_audit(
        execution_node, problems_by_epsilon, intervals_by_job
    )
    zero_rows = M5240.structural_zero_audit(
        execution_node, matches, tracks, event
    )
    quadrature_rows: list[dict[str, Any]] = []
    regulator_totals: dict[
        str, dict[int, dict[str, complex]]
    ] = {}
    coverage_rows: list[dict[str, Any]] = []
    for epsilon_id in M5239.EPSILON_IDS:
        regulator_fits = [
            row for row in fits if row["epsilon_id"] == epsilon_id
        ]
        local_rows, totals, coverage = M5239.integrate_matched_event(
            problems_by_epsilon[epsilon_id],
            regulator_fits,
            epsilon_id,
            intervals_by_job,
        )
        quadrature_rows.extend(local_rows)
        regulator_totals[epsilon_id] = totals
        coverage_rows.append(coverage)
    extrapolation_rows, convergence = M5239.extrapolation_rows(
        regulator_totals
    )
    physical_values = M5240.physical_slice_values(extrapolation_rows)
    active_poles = [
        row for row in poles if bool(row["causal_family_active"])
    ]
    node_passed = (
        max(
            float(row["maximum_accepted_projective_step"])
            for row in interval_summaries
        )
        <= MAXIMUM_PROJECTIVE_STEP
        and max(
            float(row["maximum_accepted_reciprocal_residual"])
            for row in interval_summaries
        )
        <= MAXIMUM_RECIPROCAL_RESIDUAL
        and max(
            float(row["coverage_residual"])
            for row in interval_summaries
        )
        <= 2.0e-12
        and all(
            bool(row["structural_zero_passed"]) for row in zero_rows
        )
        and max(
            float(row["relative_closure_residual"])
            for row in closure_rows
        )
        <= MAXIMUM_DYNAMIC_CLOSURE_RESIDUAL
        and len(fits) == len(active_poles)
        and all(bool(row["fit_passed"]) for row in fits)
        and convergence["low_order_subtracted_relative_error"]
        <= M5239.LOW_ORDER_SUBTRACTED_RELATIVE_ERROR_LIMIT
        and convergence["mid_order_subtracted_relative_error"]
        <= M5239.MID_ORDER_SUBTRACTED_RELATIVE_ERROR_LIMIT
        and max(
            float(row["coverage_residual"])
            for row in coverage_rows
        )
        <= 2.0e-12
    )
    result = {
        "order9_node_id": node["order9_node_id"],
        "execution_node_id": node["execution_node_id"],
        "decay_cosine": node["decay_cosine"],
        "node_passed": node_passed,
        "job_count": len(jobs),
        "adaptive_state_evaluation_count": len(
            {
                (
                    row["job_id"],
                    row["soft_cosine"],
                )
                for row in attempt_rows
            }
        ),
        "resolution_attempt_count": len(attempt_rows),
        "maximum_accepted_resolution": max(
            int(row["maximum_accepted_topology_steps"])
            for row in interval_summaries
        ),
        "maximum_accepted_projective_step": max(
            float(row["maximum_accepted_projective_step"])
            for row in interval_summaries
        ),
        "maximum_accepted_reciprocal_residual": max(
            float(row["maximum_accepted_reciprocal_residual"])
            for row in interval_summaries
        ),
        "fixed_interval_count": sum(
            int(row["fixed_interval_count"])
            for row in comparison_rows
        ),
        "adaptive_interval_count": len(interval_rows),
        "total_multiplier_mismatch_measure": sum(
            float(row["multiplier_mismatch_measure"])
            for row in comparison_rows
        ),
        "changed_job_count": sum(
            not bool(row["maps_identical_up_to_measure"])
            for row in comparison_rows
        ),
        "geometric_pole_count": len(poles),
        "active_pole_count": len(active_poles),
        "accepted_fit_count": sum(
            bool(row["fit_passed"]) for row in fits
        ),
        "convergence": convergence,
        "physical_values": {
            str(order): {
                kind: complex_row(value)
                for kind, value in values.items()
            }
            for order, values in physical_values.items()
        },
        "attempt_rows": attempt_rows,
        "interval_rows": interval_rows,
        "transition_rows": transition_rows,
        "interval_summaries": interval_summaries,
        "comparison_rows": comparison_rows,
        "zero_rows": M5240.qualify_rows(zero_rows, execution_node),
        "closure_rows": closure_rows,
        "scan_rows": M5240.qualify_rows(scan_rows, execution_node),
        "pole_rows": M5240.qualify_rows(poles, execution_node),
        "topology_rows": M5240.qualify_rows(
            topology_rows, execution_node
        ),
        "residue_rows": M5240.qualify_rows(fits, execution_node),
        "quadrature_rows": M5240.qualify_rows(
            quadrature_rows, execution_node
        ),
        "extrapolation_rows": M5240.qualify_rows(
            extrapolation_rows, execution_node
        ),
        "elapsed_seconds": time.perf_counter() - started,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(
        cache_path,
        {
            "contract": contract,
            "status": "COMPLETED" if node_passed else "FAILED_GATES",
            "result": result,
        },
    )
    if not node_passed:
        raise RuntimeError(
            f"corrected node {node['order9_node_id']} failed gates"
        )
    return result, False


def physical_value(
    result: dict[str, Any],
    order: int = 512,
    kind: str = "subtracted",
) -> complex:
    return complex_value(
        result["physical_values"][str(order)][kind]
    )


def fixed_node_value(node_id: str) -> complex:
    row = next(
        row
        for row in read_csv(NODE_ROWS_5241)
        if row["order9_node_id"] == node_id
    )
    return complex(
        float(row["order512_subtracted_real"]),
        float(row["order512_subtracted_imaginary"]),
    )


def node_summary_row(
    result: dict[str, Any], cache_hit: bool
) -> dict[str, Any]:
    corrected = physical_value(result)
    fixed = fixed_node_value(result["order9_node_id"])
    difference = corrected - fixed
    return {
        "order9_node_id": result["order9_node_id"],
        "decay_cosine": result["decay_cosine"],
        "node_passed": result["node_passed"],
        "node_cache_hit": cache_hit,
        "job_count": result["job_count"],
        "adaptive_state_evaluation_count": result[
            "adaptive_state_evaluation_count"
        ],
        "resolution_attempt_count": result[
            "resolution_attempt_count"
        ],
        "maximum_accepted_resolution": result[
            "maximum_accepted_resolution"
        ],
        "maximum_accepted_projective_step": result[
            "maximum_accepted_projective_step"
        ],
        "maximum_accepted_reciprocal_residual": result[
            "maximum_accepted_reciprocal_residual"
        ],
        "fixed_interval_count": result["fixed_interval_count"],
        "adaptive_interval_count": result[
            "adaptive_interval_count"
        ],
        "changed_job_count": result["changed_job_count"],
        "total_multiplier_mismatch_measure": result[
            "total_multiplier_mismatch_measure"
        ],
        "fixed_real": fixed.real,
        "fixed_imaginary": fixed.imag,
        "corrected_real": corrected.real,
        "corrected_imaginary": corrected.imag,
        "correction_real": difference.real,
        "correction_imaginary": difference.imag,
        "relative_correction": (
            abs(difference) / max(abs(corrected), 1.0)
        ),
        "low_order_subtracted_relative_error": result[
            "convergence"
        ]["low_order_subtracted_relative_error"],
        "elapsed_seconds": result["elapsed_seconds"],
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }


def validation_rows(
    manifest: dict[str, Any],
    node_rows: list[dict[str, Any]],
    attempt_rows: list[dict[str, Any]],
    interval_rows: list[dict[str, Any]],
    zero_rows: list[dict[str, Any]],
    closure_rows: list[dict[str, Any]],
    pole_rows: list[dict[str, Any]],
    residue_rows: list[dict[str, Any]],
    formal_digest: str,
    elapsed: float,
) -> list[dict[str, Any]]:
    accepted_attempts = [
        row for row in attempt_rows if bool(row["accepted"])
    ]
    active_poles = [
        row for row in pole_rows if bool(row["causal_family_active"])
    ]
    definitions = [
        (
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
            "CORRECTED_NODE_COUNT",
            len(node_rows) == EXPECTED_NODE_COUNT,
            len(node_rows),
            EXPECTED_NODE_COUNT,
        ),
        (
            "ALL_ADAPTIVE_STATES_ACCEPTED",
            (
                len(accepted_attempts)
                == sum(
                    int(row["adaptive_state_evaluation_count"])
                    for row in node_rows
                )
            ),
            (
                f"{len(accepted_attempts)}/"
                f"{sum(int(row['adaptive_state_evaluation_count']) for row in node_rows)}"
            ),
            "one accepted resolution per evaluated coordinate",
        ),
        (
            "ADAPTIVE_PROJECTIVE_GATE",
            max(
                float(row["maximum_pair_projective_step"])
                for row in accepted_attempts
            )
            <= MAXIMUM_PROJECTIVE_STEP,
            max(
                float(row["maximum_pair_projective_step"])
                for row in accepted_attempts
            ),
            MAXIMUM_PROJECTIVE_STEP,
        ),
        (
            "ADAPTIVE_RECIPROCAL_GATE",
            max(
                float(row["maximum_reciprocal_product_residual"])
                for row in accepted_attempts
            )
            <= MAXIMUM_RECIPROCAL_RESIDUAL,
            max(
                float(row["maximum_reciprocal_product_residual"])
                for row in accepted_attempts
            ),
            MAXIMUM_RECIPROCAL_RESIDUAL,
        ),
        (
            "ADAPTIVE_STEP_RATIO_GATE",
            max(
                float(row["projective_step_ratio_from_previous"])
                for row in accepted_attempts
            )
            <= MAXIMUM_STEP_RATIO,
            max(
                float(row["projective_step_ratio_from_previous"])
                for row in accepted_attempts
            ),
            MAXIMUM_STEP_RATIO,
        ),
        (
            "INTERVAL_COVERAGE",
            all(
                float(row["interval_upper"])
                > float(row["interval_lower"])
                for row in interval_rows
            ),
            len(interval_rows),
            "all positive intervals with per-job exact coverage",
        ),
        (
            "ALL_CORRECTED_NODES_PASS",
            all(bool(row["node_passed"]) for row in node_rows),
            (
                f"{sum(bool(row['node_passed']) for row in node_rows)}"
                f"/{len(node_rows)}"
            ),
            f"{EXPECTED_NODE_COUNT}/{EXPECTED_NODE_COUNT}",
        ),
        (
            "STRUCTURAL_ZEROS_PERSIST",
            all(bool(row["structural_zero_passed"]) for row in zero_rows),
            (
                f"{sum(bool(row['structural_zero_passed']) for row in zero_rows)}"
                f"/{len(zero_rows)}"
            ),
            "all structural-zero rows",
        ),
        (
            "DYNAMIC_CLOSURE",
            max(
                float(row["relative_closure_residual"])
                for row in closure_rows
            )
            <= MAXIMUM_DYNAMIC_CLOSURE_RESIDUAL,
            max(
                float(row["relative_closure_residual"])
                for row in closure_rows
            ),
            MAXIMUM_DYNAMIC_CLOSURE_RESIDUAL,
        ),
        (
            "ACTIVE_POLES_FITTED",
            (
                len(residue_rows) == len(active_poles)
                and all(bool(row["fit_passed"]) for row in residue_rows)
            ),
            f"{len(residue_rows)}/{len(active_poles)}",
            "all dynamically active poles",
        ),
        (
            "CORRECTED_VALUES_FINITE",
            all(
                math.isfinite(float(row["corrected_real"]))
                and math.isfinite(float(row["corrected_imaginary"]))
                for row in node_rows
            ),
            len(node_rows),
            EXPECTED_NODE_COUNT,
        ),
        (
            "FORMALIZATION_WORKBENCH_UNCHANGED",
            formal_digest == FORMAL_BASELINE,
            formal_digest,
            FORMAL_BASELINE,
        ),
        (
            "RUNTIME_BOUNDED",
            elapsed <= MAXIMUM_RUNTIME_SECONDS,
            elapsed,
            MAXIMUM_RUNTIME_SECONDS,
        ),
        (
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
            "checkpoint": 5243,
            "gate": gate,
            "passed": passed,
            "observed": observed,
            "required": required,
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
        }
        for gate, passed, observed, required in definitions
    ]


def render_document(
    node_rows: list[dict[str, Any]],
    comparison_rows: list[dict[str, Any]],
    validations: list[dict[str, Any]],
    elapsed: float,
) -> str:
    passed = all(bool(row["passed"]) for row in validations)
    changed_jobs = sum(
        not bool(row["maps_identical_up_to_measure"])
        for row in comparison_rows
    )
    lines = [
        "# 5243 — Adaptive homotopy winding rebuild and Q03/Q05 slice rerun",
        "",
        "## Purpose",
        "",
        (
            "Replace the fixed 1024/4096 winding evaluator with adaptive "
            "doubling through 32768. A state is accepted only when its "
            "winding integers stabilize and projective continuity, "
            "reciprocal identity, and step-ratio gates all pass."
        ),
        "",
        "## Results",
        "",
    ]
    for row in node_rows:
        lines.extend(
            [
                (
                    f"- `{row['order9_node_id']}`: intervals "
                    f"`{row['fixed_interval_count']} → "
                    f"{row['adaptive_interval_count']}`; changed jobs "
                    f"`{row['changed_job_count']}/12`; maximum resolution "
                    f"`{row['maximum_accepted_resolution']}`."
                ),
                (
                    f"- `{row['order9_node_id']}` value "
                    f"`{float(row['fixed_real']):.12g} "
                    f"{float(row['fixed_imaginary']):+.12g} i → "
                    f"{float(row['corrected_real']):.12g} "
                    f"{float(row['corrected_imaginary']):+.12g} i`; "
                    f"relative correction "
                    f"`{float(row['relative_correction']):.12g}`."
                ),
            ]
        )
    lines.extend(
        [
            f"- Changed component/regulator maps: `{changed_jobs}/24`.",
            f"- Runtime: `{elapsed:.3f} s`.",
            "",
            "## Decision",
            "",
            (
                "`ADOPT_ADAPTIVE_WINDING_REPAIR_FOR_Q03_Q05`"
                if passed
                else "`HOLD_ADAPTIVE_WINDING_REPAIR_PENDING_FAILED_GATE`"
            ),
            "",
            "## Interpretation",
            "",
            (
                "A material correction proves that the previous outer "
                "order-9 profile mixed physical angular variation with "
                "under-resolved homotopy topology. It must not be used as "
                "a rejection or coefficient estimate until every outer "
                "node is rebuilt under the same adaptive contract."
            ),
            "",
            "## Claim boundary",
            "",
            (
                "This repairs two angular nodes at one fixed soft energy. "
                "It is not a full two-angle coefficient, UV coefficient, "
                "local-GR derivation, or full-MTS claim."
            ),
            "",
            "## Next exact target",
            "",
            (
                "Propagate the adaptive winding evaluator to Q00-Q02 and "
                "Q04-Q08, then recompute the order-3/5/9 cubature and its "
                "Chebyshev tail using only corrected node values."
            ),
            "",
        ]
    )
    return "\n".join(lines)


def remove_project_pycache() -> None:
    target = POST / "scripts" / "__pycache__"
    if target.exists():
        shutil.rmtree(target)


def execute(selected_node: str | None = None) -> dict[str, Any]:
    started = time.perf_counter()
    dry_run = write_manifest_and_dry_run()
    manifest = read_json(MANIFEST)
    parent_manifest, matches, base_jobs, _ = M5240.build_manifest()
    event = dict(parent_manifest["target_event"])
    tracks, _ = M5240.build_outer_branch_tracks(matches, event)
    fixed_rows_all = read_csv(WINDING_5241)
    state_cache = load_state_cache(manifest)
    NODE_CACHE.mkdir(parents=True, exist_ok=True)
    target_nodes = [
        row
        for row in manifest["target_nodes"]
        if selected_node is None
        or row["order9_node_id"] == selected_node
    ]
    if selected_node is not None and not target_nodes:
        raise RuntimeError(f"unknown selected node: {selected_node}")
    node_results: list[dict[str, Any]] = []
    cache_flags: dict[str, bool] = {}
    for node in target_nodes:
        result, cache_hit = run_corrected_node(
            manifest,
            node,
            base_jobs,
            matches,
            tracks,
            event,
            state_cache,
            fixed_rows_all,
        )
        node_results.append(result)
        cache_flags[node["order9_node_id"]] = cache_hit
    if selected_node is not None:
        partial = {
            "marker": MARKER,
            "revision": REVISION,
            "status": "PARTIAL_NODE_COMPLETED",
            "order9_node_id": selected_node,
            "node_cache_hit": cache_flags[selected_node],
            "node_passed": node_results[0]["node_passed"],
            "adaptive_state_evaluation_count": node_results[0][
                "adaptive_state_evaluation_count"
            ],
            "resolution_attempt_count": node_results[0][
                "resolution_attempt_count"
            ],
            "maximum_accepted_resolution": node_results[0][
                "maximum_accepted_resolution"
            ],
            "fixed_interval_count": node_results[0][
                "fixed_interval_count"
            ],
            "adaptive_interval_count": node_results[0][
                "adaptive_interval_count"
            ],
            "changed_job_count": node_results[0][
                "changed_job_count"
            ],
            "corrected_value": complex_row(
                physical_value(node_results[0])
            ),
            "elapsed_seconds": time.perf_counter() - started,
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
        }
        remove_project_pycache()
        return partial

    node_rows = [
        node_summary_row(
            result, cache_flags[result["order9_node_id"]]
        )
        for result in node_results
    ]
    attempt_rows = [
        row for result in node_results for row in result["attempt_rows"]
    ]
    interval_rows = [
        row for result in node_results for row in result["interval_rows"]
    ]
    transition_rows = [
        row
        for result in node_results
        for row in result["transition_rows"]
    ]
    comparison_rows = [
        row
        for result in node_results
        for row in result["comparison_rows"]
    ]
    zero_rows = [
        row for result in node_results for row in result["zero_rows"]
    ]
    closure_rows = [
        row
        for result in node_results
        for row in result["closure_rows"]
    ]
    pole_rows = [
        row for result in node_results for row in result["pole_rows"]
    ]
    residue_rows = [
        row
        for result in node_results
        for row in result["residue_rows"]
    ]
    quadrature_rows = [
        row
        for result in node_results
        for row in result["quadrature_rows"]
    ]
    extrapolation_rows = [
        row
        for result in node_results
        for row in result["extrapolation_rows"]
    ]
    formal_digest = tree_digest(FORMAL)
    elapsed = time.perf_counter() - started
    validations = validation_rows(
        manifest,
        node_rows,
        attempt_rows,
        interval_rows,
        zero_rows,
        closure_rows,
        pole_rows,
        residue_rows,
        formal_digest,
        elapsed,
    )
    write_csv(ATTEMPT_ROWS, attempt_rows)
    write_csv(INTERVAL_ROWS, interval_rows)
    write_csv(TRANSITION_ROWS, transition_rows)
    write_csv(COMPARISON_ROWS, comparison_rows)
    write_csv(NODE_ROWS, node_rows)
    write_csv(ZERO_ROWS, zero_rows)
    write_csv(CLOSURE_ROWS, closure_rows)
    write_csv(POLE_ROWS, pole_rows)
    write_csv(RESIDUE_ROWS, residue_rows)
    write_csv(QUADRATURE_ROWS, quadrature_rows)
    write_csv(EXTRAPOLATION_ROWS, extrapolation_rows)
    write_csv(VALIDATION, validations)
    atomic_text(
        DOCUMENT,
        render_document(
            node_rows, comparison_rows, validations, elapsed
        ),
    )
    passed = all(bool(row["passed"]) for row in validations)
    result = {
        "marker": MARKER,
        "revision": REVISION,
        "dry_run": dry_run,
        "manifest_hash": manifest["manifest_hash"],
        "decision": (
            "ADOPT_ADAPTIVE_WINDING_REPAIR_FOR_Q03_Q05"
            if passed
            else "HOLD_ADAPTIVE_WINDING_REPAIR_PENDING_FAILED_GATE"
        ),
        "node_count": len(node_rows),
        "node_cache_hit_count": sum(cache_flags.values()),
        "node_rows": node_rows,
        "changed_job_count": sum(
            not bool(row["maps_identical_up_to_measure"])
            for row in comparison_rows
        ),
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
                COMPARISON_ROWS,
                NODE_ROWS,
                ZERO_ROWS,
                CLOSURE_ROWS,
                POLE_ROWS,
                RESIDUE_ROWS,
                QUADRATURE_ROWS,
                EXTRAPOLATION_ROWS,
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
    if not passed:
        failed = [
            row["gate"] for row in validations if not row["passed"]
        ]
        raise RuntimeError(f"5243 validation failed: {failed}")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="validate the adaptive rebuild manifest only",
    )
    parser.add_argument(
        "--node",
        choices=TARGET_NODE_IDS,
        help="compute and cache only one corrected node",
    )
    arguments = parser.parse_args()
    if arguments.dry_run:
        print(
            json.dumps(
                write_manifest_and_dry_run(),
                indent=2,
                sort_keys=True,
            )
        )
        return
    print(
        json.dumps(
            execute(arguments.node),
            indent=2,
            sort_keys=True,
        )
    )


if __name__ == "__main__":
    main()
