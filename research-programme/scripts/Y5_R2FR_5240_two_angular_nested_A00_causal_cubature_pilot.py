from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import importlib.util
import json
import math
import os
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
SOURCE = POST / "source-intake" / "functional_rg" / "5240"
RESIDUALS = POST / "source-intake" / "mts_residuals"
NODE_CACHE = SOURCE / "node-cache"

SCRIPT_5239 = (
    POST
    / "scripts"
    / "Y5_R2FR_5239_matched_event_A00_regular_complement_and_regulator_extrapolation.py"
)
RESULT_5239 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5239"
    / "matched_event_A00_regular_complement_run.json"
)
VALIDATION_5239 = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5239_VALIDATION.csv"
)

MANIFEST_JSON = SOURCE / "two_angular_nested_A00_manifest.json"
MANIFEST_CSV = SOURCE / "two_angular_nested_A00_jobs.csv"
DRY_RUN = SOURCE / "two_angular_nested_A00_dry_run.json"
RESULT = SOURCE / "two_angular_nested_A00_result.json"
OUTER_TRACK_ROWS = SOURCE / "decay_cosine_outer_branch_track_audit.csv"
ZERO_ROWS = SOURCE / "outer_node_structural_zero_audit.csv"
WINDING_ROWS = SOURCE / "nested_inner_dynamic_winding_intervals.csv"
WINDING_CACHE = SOURCE / "nested_inner_dynamic_winding_cache.json"
NODE_ROWS = SOURCE / "two_angular_node_summary.csv"
CLOSURE_ROWS = SOURCE / "two_angular_dynamic_closure.csv"
SCAN_ROWS = SOURCE / "two_angular_surface_scan_audit.csv"
POLE_ROWS = SOURCE / "two_angular_pole_catalog.csv"
TOPOLOGY_ROWS = SOURCE / "two_angular_topology_audit.csv"
RESIDUE_ROWS = SOURCE / "two_angular_residue_fits.csv"
INNER_QUADRATURE_ROWS = SOURCE / "two_angular_inner_quadrature.csv"
INNER_EXTRAPOLATION_ROWS = SOURCE / "two_angular_inner_regulator_extrapolation.csv"
OUTER_RULE_ROWS = SOURCE / "two_angular_outer_rule_audit.csv"
OUTER_CUBATURE_ROWS = SOURCE / "two_angular_outer_cubature.csv"
DOCUMENT = POST / "5240-Y5-R2FR-two-angular-nested-A00-causal-cubature-pilot.md"
VALIDATION = RESIDUALS / "P8_Y5_BRR545_5240_VALIDATION.csv"

MARKER = "MTS_5240_TWO_ANGULAR_NESTED_A00_CAUSAL_CUBATURE_PILOT"
REVISION = "two-angular-nested-A00-causal-cubature-pilot-v1"
FORMAL_BASELINE = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)

INNER_COORDINATE = "soft_cosine"
OUTER_COORDINATE = "decay_cosine"
ANGULAR_CUTOFF = 5.0e-3
ANGULAR_LIMIT = 1.0 - ANGULAR_CUTOFF
OUTER_RULE_ORDERS = (3, 5)
MASTER_OUTER_ORDER = 5
OUTER_TRACK_POINTS = 601
EXPECTED_OUTER_NODE_COUNT = 5
EXPECTED_BASE_JOB_COUNT = 12
EXPECTED_NESTED_JOB_COUNT = 60
EXPECTED_SAFE_COMPONENT_COUNT = 15
EXPECTED_MATERIAL_COMPONENT_COUNT = 6
EXPECTED_STRUCTURAL_ZERO_COUNT = 9
MAXIMUM_JOB_COUNT = 60
MAXIMUM_OUTER_BRANCH_PROJECTIVE_STEP = 0.1
MAXIMUM_STRUCTURAL_ZERO_MAGNITUDE = 1.0e-10
MAXIMUM_DYNAMIC_CLOSURE_RESIDUAL = 2.0e-10
MAXIMUM_OUTER_RULE_MOMENT_RESIDUAL = 2.0e-12
MAXIMUM_OUTER_3_TO_5_RELATIVE_DIFFERENCE = 0.2
MAXIMUM_NESTED_INNER_RELATIVE_ERROR = 1.0e-3
MAXIMUM_RUN_SECONDS = 4.0 * 60.0 * 60.0


def load_module(path: Path, name: str) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5239 = load_module(SCRIPT_5239, "mts_5239_for_5240")
M5238 = M5239.M5238
M5237 = M5239.M5237
M5231 = M5239.M5231


def complex_value(value: Any) -> complex:
    return M5239.complex_value(value)


def complex_row(value: complex) -> dict[str, float]:
    return M5239.complex_row(value)


def digest(path: Path) -> str:
    return M5239.digest(path)


def tree_digest(path: Path) -> str:
    return M5239.tree_digest(path)


def serialized_hash(value: Any) -> str:
    return M5239.serialized_hash(value)


def read_json(path: Path) -> Any:
    return M5239.read_json(path)


def read_csv(path: Path) -> list[dict[str, str]]:
    return M5239.read_csv(path)


def atomic_json(path: Path, value: Any) -> None:
    M5239.atomic_json(path, value)


def atomic_text(path: Path, value: str) -> None:
    M5239.atomic_text(path, value)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    M5239.write_csv(path, rows)


def interpolatory_rule(
    order: int,
    lower: float,
    upper: float,
) -> tuple[np.ndarray, np.ndarray, float]:
    if order < 2:
        raise ValueError("interpolatory rule requires at least two nodes")
    normalized = np.cos(
        np.pi * np.arange(order, dtype=np.float64) / (order - 1)
    )
    normalized.sort()
    vandermonde = np.asarray(
        [
            [float(node) ** power for node in normalized]
            for power in range(order)
        ],
        dtype=np.float64,
    )
    moments = np.asarray(
        [
            2.0 / (power + 1) if power % 2 == 0 else 0.0
            for power in range(order)
        ],
        dtype=np.float64,
    )
    normalized_weights = np.linalg.solve(vandermonde, moments)
    half_width = 0.5 * (upper - lower)
    midpoint = 0.5 * (upper + lower)
    nodes = midpoint + half_width * normalized
    weights = half_width * normalized_weights
    maximum_residual = 0.0
    for power in range(order):
        predicted = float(np.sum(weights * nodes**power))
        exact = (
            (upper ** (power + 1) - lower ** (power + 1))
            / (power + 1)
        )
        maximum_residual = max(
            maximum_residual, abs(predicted - exact)
        )
    return nodes, weights, maximum_residual


def outer_rules() -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    master_nodes, _, master_residual = interpolatory_rule(
        MASTER_OUTER_ORDER, -ANGULAR_LIMIT, ANGULAR_LIMIT
    )
    nodes = [
        {
            "outer_node_id": f"Y{index:02d}",
            "decay_cosine": float(value),
            "master_index": index,
        }
        for index, value in enumerate(master_nodes)
    ]
    rows: list[dict[str, Any]] = []
    for order in OUTER_RULE_ORDERS:
        rule_nodes, weights, residual = interpolatory_rule(
            order, -ANGULAR_LIMIT, ANGULAR_LIMIT
        )
        selected: list[dict[str, Any]] = []
        for value, weight in zip(rule_nodes, weights):
            node = min(
                nodes,
                key=lambda row: abs(
                    float(row["decay_cosine"]) - float(value)
                ),
            )
            mismatch = abs(
                float(node["decay_cosine"]) - float(value)
            )
            if mismatch > 2.0e-12:
                raise RuntimeError(
                    f"outer rule {order} is not nested in master nodes"
                )
            selected.append(node)
            rows.append(
                {
                    "outer_rule_order": order,
                    "outer_node_id": node["outer_node_id"],
                    "decay_cosine": float(value),
                    "weight_d_decay_cosine": float(weight),
                    "master_node_mismatch": mismatch,
                    "maximum_monomial_moment_residual": residual,
                    "angular_unit_cube_jacobian": 0.25,
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
            )
        if len({row["outer_node_id"] for row in selected}) != order:
            raise RuntimeError("outer rule node matching is not injective")
    if master_residual > MAXIMUM_OUTER_RULE_MOMENT_RESIDUAL:
        raise RuntimeError("master outer rule fails its moment audit")
    return nodes, rows


def parent_state() -> tuple[
    dict[str, Any],
    list[dict[str, Any]],
    list[dict[str, Any]],
]:
    manifest, matches = M5239.build_manifest()
    jobs = list(manifest["jobs"])
    if len(jobs) != EXPECTED_BASE_JOB_COUNT:
        raise RuntimeError("5239 base job count changed")
    return manifest, matches, jobs


def source_paths(
    parent_manifest: dict[str, Any],
) -> list[dict[str, str]]:
    paths = [
        SCRIPT_5239,
        RESULT_5239,
        VALIDATION_5239,
        Path(parent_manifest["source_contract"]["config"]),
        *[
            Path(row["path"])
            for row in parent_manifest["source_files"]
        ],
    ]
    unique: list[Path] = []
    for path in paths:
        if path not in unique:
            unique.append(path)
    return [
        {"path": str(path), "sha256": digest(path)}
        for path in unique
    ]


def node_job(
    base_job: dict[str, Any],
    node: dict[str, Any],
    representative_anchor: complex,
    reciprocal_anchor: complex,
) -> dict[str, Any]:
    job = copy.deepcopy(base_job)
    job.pop("job_input_hash", None)
    job.update(
        {
            "job_id": (
                f"{node['outer_node_id']}_{base_job['epsilon_id']}_"
                f"{base_job['component_id']}"
            ),
            "outer_node_id": node["outer_node_id"],
            "outer_node_index": int(node["master_index"]),
            "outer_coordinate": INNER_COORDINATE,
            "decay_cosine": float(node["decay_cosine"]),
            "representative_anchor": complex_row(
                representative_anchor
            ),
            "reciprocal_anchor": complex_row(reciprocal_anchor),
            "source_representative_anchor": base_job[
                "representative_anchor"
            ],
            "source_reciprocal_anchor": base_job[
                "reciprocal_anchor"
            ],
            "require_source_state": False,
            "nested_parent_job_hash": base_job["job_input_hash"],
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
        }
    )
    job["job_input_hash"] = serialized_hash(job)
    return job


def build_manifest() -> tuple[
    dict[str, Any],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
]:
    parent_manifest, matches, base_jobs = parent_state()
    nodes, rule_rows = outer_rules()
    jobs = [
        {
            "outer_node_id": node["outer_node_id"],
            "outer_node_index": node["master_index"],
            "decay_cosine": node["decay_cosine"],
            "epsilon_id": base_job["epsilon_id"],
            "component_id": base_job["component_id"],
            "family": base_job["family"],
            "owner_summand": base_job["owner_summand"],
            "base_job_id": base_job["job_id"],
            "base_job_hash": base_job["job_input_hash"],
            "source_topology": base_job["source_topology"],
            "scan_points": base_job["scan_points"],
            "candidate_surface_count": base_job[
                "candidate_surface_count"
            ],
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
        }
        for node in nodes
        for base_job in base_jobs
    ]
    manifest = {
        "marker": MARKER,
        "revision": REVISION,
        "parent_checkpoint": 5239,
        "parent_manifest_hash": parent_manifest["manifest_hash"],
        "target_event": parent_manifest["target_event"],
        "fixed_soft_energy": parent_manifest["target_event"][
            "soft_energy"
        ],
        "inner_coordinate": INNER_COORDINATE,
        "outer_coordinate": OUTER_COORDINATE,
        "angular_cutoff": ANGULAR_CUTOFF,
        "angular_domain": [-ANGULAR_LIMIT, ANGULAR_LIMIT],
        "outer_rule_orders": list(OUTER_RULE_ORDERS),
        "master_outer_order": MASTER_OUTER_ORDER,
        "outer_node_count": len(nodes),
        "base_job_count": len(base_jobs),
        "nested_job_count": len(jobs),
        "maximum_job_count": MAXIMUM_JOB_COUNT,
        "safe_component_count": len(matches),
        "material_component_count": sum(
            bool(row["material"]) for row in matches
        ),
        "structural_zero_component_count": sum(
            not bool(row["material"]) for row in matches
        ),
        "scheduled_inner_surface_evaluations": sum(
            int(row["scan_points"])
            * int(row["candidate_surface_count"])
            for row in jobs
        ),
        "normalized_angular_measure": (
            "du_soft du_decay = "
            "(d soft_cosine / 2)(d decay_cosine / 2)"
        ),
        "angular_jacobian": 0.25,
        "covered_normalized_angular_measure": ANGULAR_LIMIT**2,
        "source_files": source_paths(parent_manifest),
        "outer_nodes": nodes,
        "outer_rule_rows": rule_rows,
        "jobs": jobs,
        "claim_boundary": {
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
            "reason": (
                "This integrates two angular coordinates at one fixed "
                "soft energy and one explicit endpoint cutoff."
            ),
        },
    }
    manifest["manifest_hash"] = serialized_hash(manifest)
    return manifest, matches, base_jobs, rule_rows


def write_manifest_and_dry_run() -> dict[str, Any]:
    manifest, matches, base_jobs, rule_rows = build_manifest()
    parent_validation = read_csv(VALIDATION_5239)
    checks = {
        "source_paths_exist_and_match": all(
            Path(row["path"]).exists()
            and digest(Path(row["path"])) == row["sha256"]
            for row in manifest["source_files"]
        ),
        "parent_5239_validation_passed": all(
            row["passed"] == "True" for row in parent_validation
        ),
        "formal_digest_unchanged": tree_digest(FORMAL)
        == FORMAL_BASELINE,
        "outer_node_count_expected": manifest["outer_node_count"]
        == EXPECTED_OUTER_NODE_COUNT,
        "base_job_count_expected": len(base_jobs)
        == EXPECTED_BASE_JOB_COUNT,
        "nested_job_count_bounded": manifest["nested_job_count"]
        == EXPECTED_NESTED_JOB_COUNT
        and manifest["nested_job_count"] <= MAXIMUM_JOB_COUNT,
        "component_counts_expected": (
            len(matches) == EXPECTED_SAFE_COMPONENT_COUNT
            and manifest["material_component_count"]
            == EXPECTED_MATERIAL_COMPONENT_COUNT
            and manifest["structural_zero_component_count"]
            == EXPECTED_STRUCTURAL_ZERO_COUNT
        ),
        "outer_rules_nested_and_exact": (
            len(rule_rows) == sum(OUTER_RULE_ORDERS)
            and max(
                float(row["maximum_monomial_moment_residual"])
                for row in rule_rows
            )
            <= MAXIMUM_OUTER_RULE_MOMENT_RESIDUAL
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
        "nested_job_count": manifest["nested_job_count"],
        "scheduled_inner_surface_evaluations": manifest[
            "scheduled_inner_surface_evaluations"
        ],
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(MANIFEST_JSON, manifest)
    write_csv(MANIFEST_CSV, manifest["jobs"])
    write_csv(OUTER_RULE_ROWS, rule_rows)
    atomic_json(DRY_RUN, report)
    if not report["dry_run_passed"]:
        failed = [key for key, passed in checks.items() if not passed]
        raise RuntimeError(f"5240 dry run failed: {failed}")
    return report


def outer_track_key(
    epsilon_id: str, component_id: str, role: str
) -> str:
    return f"{epsilon_id}|{component_id}|{role}"


def build_outer_branch_tracks(
    matches: list[dict[str, Any]],
    event: dict[str, Any],
) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]]]:
    contract = M5239.source_contract()
    coordinates = np.linspace(
        -ANGULAR_LIMIT, ANGULAR_LIMIT, OUTER_TRACK_POINTS
    )
    tracks: dict[str, dict[str, Any]] = {}
    rows: list[dict[str, Any]] = []
    for epsilon_id in M5239.EPSILON_IDS:
        topology = read_json(
            M5231.topology_path(
                contract, M5239.TARGET_SEED, epsilon_id
            )
        )
        target = complex_value(topology["target_cosine"])
        for match in matches:
            component = match[epsilon_id]
            for role in ("representative", "reciprocal"):
                entry = component[role]
                pair = tuple(entry["representing_pairs"][0])
                anchor = component[f"{role}_root"]
                track = M5237.build_coordinate_branch_track(
                    event,
                    target,
                    pair,
                    anchor,
                    OUTER_COORDINATE,
                    coordinates,
                )
                key = outer_track_key(
                    epsilon_id, match["component_id"], role
                )
                tracks[key] = track
                rows.append(
                    {
                        "epsilon_id": epsilon_id,
                        "component_id": match["component_id"],
                        "family": match["family"],
                        "owner_summand": match["owner_summand"],
                        "role": role,
                        "pair": "|".join(pair),
                        "coordinate_minimum": -ANGULAR_LIMIT,
                        "coordinate_maximum": ANGULAR_LIMIT,
                        "coordinate_count": OUTER_TRACK_POINTS,
                        "maximum_projective_step": track[
                            "maximum_projective_step"
                        ],
                        "minimum_alternate_branch_separation": track[
                            "minimum_alternate_branch_separation"
                        ],
                        "valid_for_numeric_UV_claim": False,
                        "valid_for_local_GR_claim": False,
                        "valid_for_full_MTS_claim": False,
                    }
                )
    return tracks, rows


def material_node_jobs(
    node: dict[str, Any],
    base_jobs: list[dict[str, Any]],
    tracks: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    jobs: list[dict[str, Any]] = []
    coordinate = complex(float(node["decay_cosine"]))
    for base_job in base_jobs:
        representative = M5237.track_anchor(
            tracks[
                outer_track_key(
                    base_job["epsilon_id"],
                    base_job["component_id"],
                    "representative",
                )
            ],
            coordinate,
        )
        reciprocal = M5237.track_anchor(
            tracks[
                outer_track_key(
                    base_job["epsilon_id"],
                    base_job["component_id"],
                    "reciprocal",
                )
            ],
            coordinate,
        )
        jobs.append(
            node_job(base_job, node, representative, reciprocal)
        )
    return jobs


def build_node_problem(job: dict[str, Any]) -> dict[str, Any]:
    topology = read_json(Path(job["source_topology"]))
    target = complex_value(topology["target_cosine"])
    event = M5237.event_from_job(job)
    representative_pair = tuple(job["representative_pair"])
    reciprocal_pair = tuple(job["reciprocal_pair"])
    representative = M5237.find_source_crossing(
        topology,
        int(job["representative_chamber"]),
        representative_pair,
        complex_value(job["source_representative_anchor"]),
    )
    reciprocal = M5237.find_source_crossing(
        topology,
        int(job["reciprocal_chamber"]),
        reciprocal_pair,
        complex_value(job["source_reciprocal_anchor"]),
    )
    coordinates = np.linspace(
        float(job["scan_minimum"]),
        float(job["scan_maximum"]),
        int(job["scan_points"]),
    )
    branch_tracks = {
        M5237.pair_key(
            representative_pair
        ): M5237.build_coordinate_branch_track(
            event,
            target,
            representative_pair,
            complex_value(job["representative_anchor"]),
            INNER_COORDINATE,
            coordinates,
        ),
        M5237.pair_key(
            reciprocal_pair
        ): M5237.build_coordinate_branch_track(
            event,
            target,
            reciprocal_pair,
            complex_value(job["reciprocal_anchor"]),
            INNER_COORDINATE,
            coordinates,
        ),
    }
    case = {
        "case_id": job["job_id"],
        "family": job["family"],
        "tranche": job["tranche"],
        "seed": int(job["seed"]),
        "outer_coordinate": INNER_COORDINATE,
        "representative_pair": representative_pair,
        "reciprocal_pair": reciprocal_pair,
        "expected_u_winding": int(job["expected_u_winding"]),
        "expected_v_winding": int(job["expected_v_winding"]),
    }
    endpoint = job["owner_summand"] == "endpoint_subtraction"
    return {
        "job": job,
        "owner_summand": job["owner_summand"],
        "component_id": job["component_id"],
        "case": case,
        "event": event,
        "topology": topology,
        "target": target,
        "representative": representative,
        "reciprocal": reciprocal,
        "atlas_rows": (
            M5238.endpoint_candidate_rows(representative_pair)
            if endpoint
            else M5237.direct_candidate_rows(representative_pair)
        ),
        "coordinates": coordinates,
        "branch_tracks": branch_tracks,
    }


def winding_cache_contract(manifest: dict[str, Any]) -> dict[str, Any]:
    return {
        "marker": MARKER,
        "revision": REVISION,
        "manifest_hash": manifest["manifest_hash"],
        "parent_5239_script_sha256": digest(SCRIPT_5239),
        "dynamic_topology_steps": M5239.DYNAMIC_TOPOLOGY_STEPS,
        "dynamic_confirmation_steps": M5239.DYNAMIC_CONFIRMATION_STEPS,
        "dynamic_coarse_points": M5239.DYNAMIC_COARSE_POINTS,
        "dynamic_bisection_steps": M5239.DYNAMIC_BISECTION_STEPS,
    }


def load_winding_cache(manifest: dict[str, Any]) -> dict[str, Any]:
    contract = winding_cache_contract(manifest)
    if WINDING_CACHE.exists():
        payload = read_json(WINDING_CACHE)
        if payload.get("contract") == contract:
            return payload
    payload = {"contract": contract, "jobs": {}}
    atomic_json(WINDING_CACHE, payload)
    return payload


def intervals_for_problems(
    problems: list[dict[str, Any]],
    cache: dict[str, Any],
) -> tuple[list[dict[str, Any]], int, int]:
    rows: list[dict[str, Any]] = []
    hits = 0
    misses = 0
    for problem in problems:
        job_id = problem["job"]["job_id"]
        job_hash = problem["job"]["job_input_hash"]
        cached = cache["jobs"].get(job_id)
        if cached and cached.get("job_hash") == job_hash:
            job_rows = list(cached["rows"])
            hits += 1
        else:
            job_rows = M5239.derive_problem_winding_intervals(
                problem
            )
            cache["jobs"][job_id] = {
                "job_hash": job_hash,
                "rows": job_rows,
            }
            atomic_json(WINDING_CACHE, cache)
            misses += 1
        rows.extend(job_rows)
    return rows, hits, misses


def qualify_rows(
    rows: list[dict[str, Any]],
    node: dict[str, Any],
) -> list[dict[str, Any]]:
    return [
        {
            "outer_node_id": node["outer_node_id"],
            "decay_cosine": node["decay_cosine"],
            **row,
        }
        for row in rows
    ]


def structural_zero_audit(
    node: dict[str, Any],
    matches: list[dict[str, Any]],
    tracks: dict[str, dict[str, Any]],
    event: dict[str, Any],
) -> list[dict[str, Any]]:
    contract = M5239.source_contract()
    varied_event = dict(event)
    varied_event[OUTER_COORDINATE] = float(node["decay_cosine"])
    rows: list[dict[str, Any]] = []
    coordinate = complex(float(node["decay_cosine"]))
    for epsilon_id in M5239.EPSILON_IDS:
        topology = read_json(
            M5231.topology_path(
                contract, M5239.TARGET_SEED, epsilon_id
            )
        )
        for match in matches:
            if match["material"]:
                continue
            component = match[epsilon_id]
            representative = copy.deepcopy(
                component["representative"]
            )
            reciprocal = copy.deepcopy(component["reciprocal"])
            representative["target_root"] = str(
                M5237.track_anchor(
                    tracks[
                        outer_track_key(
                            epsilon_id,
                            match["component_id"],
                            "representative",
                        )
                    ],
                    coordinate,
                )
            )
            reciprocal["target_root"] = str(
                M5237.track_anchor(
                    tracks[
                        outer_track_key(
                            epsilon_id,
                            match["component_id"],
                            "reciprocal",
                        )
                    ],
                    coordinate,
                )
            )
            isolated = M5239.isolated_component_topology(
                topology, representative, reciprocal
            )
            contributions, diagnostics = (
                M5231.safe_family_contributions(
                    varied_event, isolated
                )
            )
            contribution = complex(
                contributions.get(match["family"], 0.0j)
            )
            classifications = "|".join(
                sorted(
                    {
                        str(row["classification"])
                        for row in diagnostics
                    }
                )
            )
            rows.append(
                {
                    "outer_node_id": node["outer_node_id"],
                    "decay_cosine": node["decay_cosine"],
                    "epsilon_id": epsilon_id,
                    "component_id": match["component_id"],
                    "family": match["family"],
                    "classification": classifications,
                    "contribution_real": contribution.real,
                    "contribution_imaginary": contribution.imag,
                    "contribution_magnitude": abs(contribution),
                    "structural_zero_passed": (
                        "LOWER_THAN_DOUBLE_POLE__ZERO_DOUBLE_RESIDUE"
                        in classifications
                        and abs(contribution)
                        <= MAXIMUM_STRUCTURAL_ZERO_MAGNITUDE
                    ),
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
            )
    return rows


def dynamic_closure_audit(
    node: dict[str, Any],
    problems_by_epsilon: dict[str, list[dict[str, Any]]],
    intervals_by_job: dict[str, list[dict[str, Any]]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for epsilon_id in M5239.EPSILON_IDS:
        problems = problems_by_epsilon[epsilon_id]
        for coordinate in M5239.WITNESS_COORDINATES:
            varied_event = dict(problems[0]["event"])
            varied_event[INNER_COORDINATE] = float(coordinate)
            merged, active = M5239.merged_active_topology(
                problems, float(coordinate), intervals_by_job
            )
            parent = (
                sum(
                    M5231.safe_family_contributions(
                        varied_event, merged
                    )[0].values(),
                    0.0j,
                )
                if active
                else 0.0j
            )
            reconstructed = sum(
                (
                    M5239.dynamic_component_contribution(
                        problem,
                        float(coordinate),
                        intervals_by_job,
                    )
                    for problem in problems
                ),
                0.0j,
            )
            residual = reconstructed - parent
            rows.append(
                {
                    "outer_node_id": node["outer_node_id"],
                    "decay_cosine": node["decay_cosine"],
                    "epsilon_id": epsilon_id,
                    "soft_cosine": coordinate,
                    "active_component_count": len(active),
                    "parent_real": parent.real,
                    "parent_imaginary": parent.imag,
                    "reconstructed_real": reconstructed.real,
                    "reconstructed_imaginary": reconstructed.imag,
                    "residual_magnitude": abs(residual),
                    "relative_closure_residual": (
                        abs(residual)
                        / max(abs(parent), abs(reconstructed), 1.0)
                    ),
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
            )
    return rows


def physical_slice_values(
    extrapolation_rows: list[dict[str, Any]],
) -> dict[int, dict[str, complex]]:
    values: dict[int, dict[str, complex]] = {}
    for row in extrapolation_rows:
        if row["row_type"] != "PHYSICAL_RICHARDSON_SLICE":
            continue
        order = int(row["quadrature_order"])
        values[order] = {
            "raw": complex(
                float(row["raw_integral_real"]),
                float(row["raw_integral_imaginary"]),
            ),
            "subtracted": complex(
                float(row["subtracted_integral_real"]),
                float(row["subtracted_integral_imaginary"]),
            ),
        }
    if set(values) != set(M5239.QUADRATURE_ORDERS):
        raise RuntimeError("physical inner slice orders are incomplete")
    return values


def node_cache_contract(
    manifest: dict[str, Any],
    node: dict[str, Any],
    jobs: list[dict[str, Any]],
) -> dict[str, Any]:
    return {
        "marker": MARKER,
        "revision": REVISION,
        "manifest_hash": manifest["manifest_hash"],
        "outer_node_id": node["outer_node_id"],
        "decay_cosine": node["decay_cosine"],
        "job_hashes": sorted(job["job_input_hash"] for job in jobs),
        "parent_5239_script_sha256": digest(SCRIPT_5239),
    }


def run_node(
    manifest: dict[str, Any],
    node: dict[str, Any],
    base_jobs: list[dict[str, Any]],
    matches: list[dict[str, Any]],
    tracks: dict[str, dict[str, Any]],
    event: dict[str, Any],
    winding_cache: dict[str, Any],
) -> tuple[dict[str, Any], bool, int, int]:
    jobs = material_node_jobs(node, base_jobs, tracks)
    contract = node_cache_contract(manifest, node, jobs)
    cache_path = NODE_CACHE / f"{node['outer_node_id']}.json"
    if cache_path.exists():
        cached = read_json(cache_path)
        if (
            cached.get("contract") == contract
            and cached.get("status") == "COMPLETED"
        ):
            return cached["result"], True, 0, 0
    started = time.perf_counter()
    problems_by_epsilon: dict[str, list[dict[str, Any]]] = {
        epsilon_id: [] for epsilon_id in M5239.EPSILON_IDS
    }
    for job in jobs:
        problems_by_epsilon[job["epsilon_id"]].append(
            build_node_problem(job)
        )
    all_problems = [
        problem
        for epsilon_id in M5239.EPSILON_IDS
        for problem in problems_by_epsilon[epsilon_id]
    ]
    winding_rows, interval_hits, interval_misses = (
        intervals_for_problems(all_problems, winding_cache)
    )
    intervals_by_job = M5239.interval_rows_by_job(winding_rows)
    scan_rows: list[dict[str, Any]] = []
    poles: list[dict[str, Any]] = []
    topology_rows: list[dict[str, Any]] = []
    poles_by_job: dict[str, list[dict[str, Any]]] = {}
    problem_by_job = {
        problem["job"]["job_id"]: problem
        for problem in all_problems
    }
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
        pole_lookup = {
            row["pole_id"]: row for row in local_poles
        }
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
            f"inner residue fit failed at {node['outer_node_id']}"
        )
    closure_rows = dynamic_closure_audit(
        node, problems_by_epsilon, intervals_by_job
    )
    zero_rows = structural_zero_audit(
        node, matches, tracks, event
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
        local_rows, totals, coverage = (
            M5239.integrate_matched_event(
                problems_by_epsilon[epsilon_id],
                regulator_fits,
                epsilon_id,
                intervals_by_job,
            )
        )
        quadrature_rows.extend(local_rows)
        regulator_totals[epsilon_id] = totals
        coverage_rows.append(coverage)
    extrapolation_rows, convergence = M5239.extrapolation_rows(
        regulator_totals
    )
    physical_values = physical_slice_values(extrapolation_rows)
    active_poles = [
        row for row in poles if bool(row["causal_family_active"])
    ]
    node_passed = (
        all(bool(row["structural_zero_passed"]) for row in zero_rows)
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
    elapsed = time.perf_counter() - started
    result = {
        "outer_node_id": node["outer_node_id"],
        "decay_cosine": node["decay_cosine"],
        "status": "COMPLETED" if node_passed else "FAILED_GATES",
        "node_passed": node_passed,
        "job_count": len(jobs),
        "geometric_pole_count": len(poles),
        "active_pole_count": len(active_poles),
        "accepted_fit_count": sum(
            bool(row["fit_passed"]) for row in fits
        ),
        "winding_interval_count": len(winding_rows),
        "coverage": coverage_rows,
        "convergence": convergence,
        "physical_values": {
            str(order): {
                kind: complex_row(value)
                for kind, value in values.items()
            }
            for order, values in physical_values.items()
        },
        "zero_rows": qualify_rows(zero_rows, node),
        "winding_rows": qualify_rows(winding_rows, node),
        "closure_rows": closure_rows,
        "scan_rows": qualify_rows(scan_rows, node),
        "pole_rows": qualify_rows(poles, node),
        "topology_rows": qualify_rows(topology_rows, node),
        "residue_rows": qualify_rows(fits, node),
        "quadrature_rows": qualify_rows(quadrature_rows, node),
        "extrapolation_rows": qualify_rows(
            extrapolation_rows, node
        ),
        "elapsed_seconds": elapsed,
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
            f"outer node {node['outer_node_id']} failed inner gates"
        )
    return result, False, interval_hits, interval_misses


def row_complex(
    row: dict[str, Any], prefix: str
) -> complex:
    return complex(
        float(row[f"{prefix}_real"]),
        float(row[f"{prefix}_imaginary"]),
    )


def node_summary_row(
    result: dict[str, Any], cache_hit: bool
) -> dict[str, Any]:
    values = result["physical_values"]
    row: dict[str, Any] = {
        "outer_node_id": result["outer_node_id"],
        "decay_cosine": result["decay_cosine"],
        "node_passed": result["node_passed"],
        "node_cache_hit": cache_hit,
        "job_count": result["job_count"],
        "geometric_pole_count": result["geometric_pole_count"],
        "active_pole_count": result["active_pole_count"],
        "accepted_fit_count": result["accepted_fit_count"],
        "winding_interval_count": result["winding_interval_count"],
        "low_order_subtracted_relative_error": result[
            "convergence"
        ]["low_order_subtracted_relative_error"],
        "mid_order_subtracted_relative_error": result[
            "convergence"
        ]["mid_order_subtracted_relative_error"],
        "low_order_improvement_factor": result["convergence"][
            "low_order_improvement_factor"
        ],
        "elapsed_seconds": result["elapsed_seconds"],
    }
    for order in M5239.QUADRATURE_ORDERS:
        for kind in ("raw", "subtracted"):
            value = complex_value(values[str(order)][kind])
            row[f"order{order}_{kind}_real"] = value.real
            row[f"order{order}_{kind}_imaginary"] = value.imag
    row.update(
        {
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
        }
    )
    return row


def outer_cubature(
    node_rows: list[dict[str, Any]],
    rule_rows: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    by_node = {row["outer_node_id"]: row for row in node_rows}
    rows: list[dict[str, Any]] = []
    values_by_order: dict[int, dict[str, complex]] = {}
    for outer_order in OUTER_RULE_ORDERS:
        selected = [
            row
            for row in rule_rows
            if int(row["outer_rule_order"]) == outer_order
        ]
        outputs: dict[str, complex] = {}
        for inner_order in (128, 512):
            for kind in ("raw", "subtracted"):
                value = 0.25 * sum(
                    (
                        float(rule["weight_d_decay_cosine"])
                        * complex(
                            float(
                                by_node[rule["outer_node_id"]][
                                    f"order{inner_order}_{kind}_real"
                                ]
                            ),
                            float(
                                by_node[rule["outer_node_id"]][
                                    f"order{inner_order}_{kind}_imaginary"
                                ]
                            ),
                        )
                        for rule in selected
                    ),
                    0.0j,
                )
                outputs[f"inner{inner_order}_{kind}"] = value
        values_by_order[outer_order] = outputs
        rows.append(
            {
                "outer_rule_order": outer_order,
                "outer_node_ids": "|".join(
                    row["outer_node_id"] for row in selected
                ),
                "outer_node_count": len(selected),
                "angular_unit_cube_jacobian": 0.25,
                "covered_normalized_angular_measure": (
                    ANGULAR_LIMIT**2
                ),
                **{
                    f"{key}_real": value.real
                    for key, value in outputs.items()
                },
                **{
                    f"{key}_imaginary": value.imag
                    for key, value in outputs.items()
                },
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    reference = values_by_order[MASTER_OUTER_ORDER][
        "inner512_subtracted"
    ]
    denominator = max(abs(reference), 1.0)
    coarse = values_by_order[OUTER_RULE_ORDERS[0]][
        "inner512_subtracted"
    ]
    inner128 = values_by_order[MASTER_OUTER_ORDER][
        "inner128_subtracted"
    ]
    summary = {
        "reference_outer_order": MASTER_OUTER_ORDER,
        "reference_inner_order": 512,
        "two_angular_reference": complex_row(reference),
        "outer_order3_to_order5_relative_difference": (
            abs(coarse - reference) / denominator
        ),
        "nested_inner128_to512_relative_difference": (
            abs(inner128 - reference) / denominator
        ),
        "covered_normalized_angular_measure": ANGULAR_LIMIT**2,
        "omitted_normalized_angular_measure": (
            1.0 - ANGULAR_LIMIT**2
        ),
    }
    return rows, summary


def validation_rows(
    manifest: dict[str, Any],
    outer_track_rows: list[dict[str, Any]],
    zero_rows: list[dict[str, Any]],
    winding_rows: list[dict[str, Any]],
    closure_rows: list[dict[str, Any]],
    pole_rows: list[dict[str, Any]],
    residue_rows: list[dict[str, Any]],
    node_rows: list[dict[str, Any]],
    rule_rows: list[dict[str, Any]],
    cubature_summary: dict[str, Any],
    formal_after: str,
    elapsed: float,
) -> list[dict[str, Any]]:
    active_poles = [
        row for row in pole_rows if bool(row["causal_family_active"])
    ]
    checks = [
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
            "NESTED_JOB_COUNT",
            manifest["nested_job_count"] == EXPECTED_NESTED_JOB_COUNT,
            manifest["nested_job_count"],
            EXPECTED_NESTED_JOB_COUNT,
        ),
        (
            "OUTER_BRANCH_TRACK_STABLE",
            max(
                float(row["maximum_projective_step"])
                for row in outer_track_rows
            )
            <= MAXIMUM_OUTER_BRANCH_PROJECTIVE_STEP,
            max(
                float(row["maximum_projective_step"])
                for row in outer_track_rows
            ),
            MAXIMUM_OUTER_BRANCH_PROJECTIVE_STEP,
        ),
        (
            "STRUCTURAL_ZEROS_PERSIST",
            len(zero_rows)
            == (
                EXPECTED_OUTER_NODE_COUNT
                * len(M5239.EPSILON_IDS)
                * EXPECTED_STRUCTURAL_ZERO_COUNT
            )
            and all(
                bool(row["structural_zero_passed"])
                for row in zero_rows
            ),
            f"{sum(bool(row['structural_zero_passed']) for row in zero_rows)}/{len(zero_rows)}",
            "all omitted components remain structural zeros",
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
            "WINDING_INTERVAL_TRACK_RESOLUTION",
            max(
                float(row["maximum_pair_projective_step"])
                for row in winding_rows
            )
            <= M5239.DYNAMIC_PROJECTIVE_STEP_LIMIT,
            max(
                float(row["maximum_pair_projective_step"])
                for row in winding_rows
            ),
            M5239.DYNAMIC_PROJECTIVE_STEP_LIMIT,
        ),
        (
            "ACTIVE_POLES_FITTED",
            len(residue_rows) == len(active_poles)
            and all(bool(row["fit_passed"]) for row in residue_rows),
            f"{len(residue_rows)}/{len(active_poles)}",
            "all dynamically active poles",
        ),
        (
            "ALL_OUTER_NODES_PASS_INNER_GATES",
            len(node_rows) == EXPECTED_OUTER_NODE_COUNT
            and all(bool(row["node_passed"]) for row in node_rows),
            f"{sum(bool(row['node_passed']) for row in node_rows)}/{len(node_rows)}",
            EXPECTED_OUTER_NODE_COUNT,
        ),
        (
            "OUTER_RULE_MOMENTS",
            max(
                float(row["maximum_monomial_moment_residual"])
                for row in rule_rows
            )
            <= MAXIMUM_OUTER_RULE_MOMENT_RESIDUAL,
            max(
                float(row["maximum_monomial_moment_residual"])
                for row in rule_rows
            ),
            MAXIMUM_OUTER_RULE_MOMENT_RESIDUAL,
        ),
        (
            "OUTER_ORDER_3_TO_5_CONVERGENCE",
            cubature_summary[
                "outer_order3_to_order5_relative_difference"
            ]
            <= MAXIMUM_OUTER_3_TO_5_RELATIVE_DIFFERENCE,
            cubature_summary[
                "outer_order3_to_order5_relative_difference"
            ],
            MAXIMUM_OUTER_3_TO_5_RELATIVE_DIFFERENCE,
        ),
        (
            "NESTED_INNER_CONVERGENCE",
            cubature_summary[
                "nested_inner128_to512_relative_difference"
            ]
            <= MAXIMUM_NESTED_INNER_RELATIVE_ERROR,
            cubature_summary[
                "nested_inner128_to512_relative_difference"
            ],
            MAXIMUM_NESTED_INNER_RELATIVE_ERROR,
        ),
        (
            "FORMALIZATION_WORKBENCH_UNCHANGED",
            formal_after == FORMAL_BASELINE,
            formal_after,
            FORMAL_BASELINE,
        ),
        (
            "RUNTIME_BOUNDED",
            elapsed <= MAXIMUM_RUN_SECONDS,
            elapsed,
            MAXIMUM_RUN_SECONDS,
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
            "checkpoint": 5240,
            "gate": gate,
            "passed": bool(passed),
            "observed": observed,
            "required": required,
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
        }
        for gate, passed, observed, required in checks
    ]


def render_document(
    manifest: dict[str, Any],
    node_rows: list[dict[str, Any]],
    outer_track_rows: list[dict[str, Any]],
    zero_rows: list[dict[str, Any]],
    pole_rows: list[dict[str, Any]],
    residue_rows: list[dict[str, Any]],
    cubature_summary: dict[str, Any],
    validations: list[dict[str, Any]],
    node_cache_hits: int,
    interval_hits: int,
    interval_misses: int,
    elapsed: float,
) -> str:
    reference = complex_value(
        cubature_summary["two_angular_reference"]
    )
    validation_passed = all(bool(row["passed"]) for row in validations)
    active_poles = [
        row for row in pole_rows if bool(row["causal_family_active"])
    ]
    return "\n".join(
        [
            "# 5240 — Two-angular nested A00 causal cubature pilot",
            "",
            "## Scope",
            "",
            (
                "This checkpoint promotes the 5239 one-dimensional "
                "`soft_cosine` slice to a nested integration over "
                "`soft_cosine` and `decay_cosine` at the inherited fixed "
                f"`soft_energy={manifest['fixed_soft_energy']:.16g}`."
            ),
            "",
            "## Measure derivation",
            "",
            (
                "The parent Sobol events use `u_soft,u_decay in [0,1]` "
                "with `cosine=2u-1`. Therefore"
            ),
            "",
            "$$",
            "du_{\\rm soft}\\,du_{\\rm decay}"
            "=\\frac14\\,d c_{\\rm soft}\\,d c_{\\rm decay}.",
            "$$",
            "",
            (
                "The factor `1/4` is inherited from the parent sampling "
                "map; it is not fitted. Both cosine integrals use the "
                f"explicit cutoff domain `[-{ANGULAR_LIMIT},"
                f"{ANGULAR_LIMIT}]`, covering normalized angular measure "
                f"`{manifest['covered_normalized_angular_measure']:.9f}`."
            ),
            "",
            "## Construction",
            "",
            (
                f"All {EXPECTED_SAFE_COMPONENT_COUNT} reciprocal "
                "components are continued along `decay_cosine`. The six "
                "material components generate 60 inner regulator jobs. "
                "The nine omitted components are re-evaluated at every "
                "outer node and regulator rather than assumed to stay zero."
            ),
            "",
            (
                "At each outer node the complete 5239 machinery is rerun: "
                "inner branch continuation, piecewise integer-winding "
                "maps, causal pole classification, full-component residue "
                "fits, global pole subtraction, E040/E020 extrapolation, "
                "and dynamic merged-topology closure."
            ),
            "",
            "## Results",
            "",
            f"- Outer nodes: `{len(node_rows)}`.",
            f"- Nested regulator jobs: `{manifest['nested_job_count']}`.",
            f"- Outer branch tracks: `{len(outer_track_rows)}`.",
            (
                f"- Persistent structural-zero rows: "
                f"`{sum(bool(row['structural_zero_passed']) for row in zero_rows)}/{len(zero_rows)}`."
            ),
            f"- Geometric poles: `{len(pole_rows)}`.",
            f"- Dynamically active poles: `{len(active_poles)}`.",
            (
                f"- Accepted residue fits: "
                f"`{sum(bool(row['fit_passed']) for row in residue_rows)}/{len(residue_rows)}`."
            ),
            (
                "- Outer order-3 to order-5 relative difference: "
                f"`{cubature_summary['outer_order3_to_order5_relative_difference']:.12g}`."
            ),
            (
                "- Nested inner order-128 to order-512 relative "
                f"difference: `{cubature_summary['nested_inner128_to512_relative_difference']:.12g}`."
            ),
            (
                "- Order-5/order-512 normalized two-angular value: "
                f"`{reference.real:.16g} {reference.imag:+.16g} i`."
            ),
            (
                f"- Cache: node hits `{node_cache_hits}`, winding hits "
                f"`{interval_hits}`, winding misses `{interval_misses}`."
            ),
            f"- Runtime: `{elapsed:.3f} s`.",
            "",
            "## Decision",
            "",
            (
                "`ADOPT_TWO_ANGULAR_NESTED_CAUSAL_CUBATURE_PILOT`"
                if validation_passed
                else "`HOLD_TWO_ANGULAR_CUBATURE_PENDING_FAILED_GATE`"
            ),
            "",
            "## Claim boundary",
            "",
            (
                "This is not yet the physical multidimensional A00 "
                "coefficient. Soft energy remains fixed, the angular "
                f"endpoint strips carry unbounded omitted measure "
                f"`{cubature_summary['omitted_normalized_angular_measure']:.9f}`, "
                "and only the nested outer orders 3 and 5 have been run. "
                "No numeric-UV, local-GR, or full-MTS claim follows."
            ),
            "",
            "## Next target",
            "",
            (
                "Add the nested order-9 outer rule and an angular-cutoff "
                "ladder, then carry the resulting two-angular density into "
                "the final soft-energy integration with its endpoint "
                "subtraction."
            ),
            "",
            "## Validation",
            "",
            *[
                f"- `{row['gate']}`: `{'PASS' if row['passed'] else 'FAIL'}`."
                for row in validations
            ],
            "",
        ]
    )


def remove_project_pycache() -> None:
    target = POST / "scripts" / "__pycache__"
    if target.exists():
        shutil.rmtree(target)


def execute() -> dict[str, Any]:
    started = time.perf_counter()
    dry_run = write_manifest_and_dry_run()
    manifest = read_json(MANIFEST_JSON)
    _, matches, base_jobs, rule_rows = build_manifest()
    event = dict(manifest["target_event"])
    tracks, outer_track_rows = build_outer_branch_tracks(
        matches, event
    )
    write_csv(OUTER_TRACK_ROWS, outer_track_rows)
    winding_cache = load_winding_cache(manifest)
    node_results: list[dict[str, Any]] = []
    node_cache_flags: dict[str, bool] = {}
    interval_hits = 0
    interval_misses = 0
    for node in manifest["outer_nodes"]:
        result, cache_hit, hits, misses = run_node(
            manifest,
            node,
            base_jobs,
            matches,
            tracks,
            event,
            winding_cache,
        )
        node_results.append(result)
        node_cache_flags[node["outer_node_id"]] = cache_hit
        interval_hits += hits
        interval_misses += misses
    node_rows = [
        node_summary_row(
            result, node_cache_flags[result["outer_node_id"]]
        )
        for result in node_results
    ]
    zero_rows = [
        row for result in node_results for row in result["zero_rows"]
    ]
    winding_rows = [
        row
        for result in node_results
        for row in result["winding_rows"]
    ]
    closure_rows = [
        row
        for result in node_results
        for row in result["closure_rows"]
    ]
    scan_rows = [
        row for result in node_results for row in result["scan_rows"]
    ]
    pole_rows = [
        row for result in node_results for row in result["pole_rows"]
    ]
    topology_rows = [
        row
        for result in node_results
        for row in result["topology_rows"]
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
    cubature_rows, cubature_summary = outer_cubature(
        node_rows, rule_rows
    )
    formal_after = tree_digest(FORMAL)
    elapsed = time.perf_counter() - started
    validations = validation_rows(
        manifest,
        outer_track_rows,
        zero_rows,
        winding_rows,
        closure_rows,
        pole_rows,
        residue_rows,
        node_rows,
        rule_rows,
        cubature_summary,
        formal_after,
        elapsed,
    )
    write_csv(ZERO_ROWS, zero_rows)
    write_csv(WINDING_ROWS, winding_rows)
    write_csv(NODE_ROWS, node_rows)
    write_csv(CLOSURE_ROWS, closure_rows)
    write_csv(SCAN_ROWS, scan_rows)
    write_csv(POLE_ROWS, pole_rows)
    write_csv(TOPOLOGY_ROWS, topology_rows)
    write_csv(RESIDUE_ROWS, residue_rows)
    write_csv(INNER_QUADRATURE_ROWS, quadrature_rows)
    write_csv(INNER_EXTRAPOLATION_ROWS, extrapolation_rows)
    write_csv(OUTER_CUBATURE_ROWS, cubature_rows)
    write_csv(VALIDATION, validations)
    document = render_document(
        manifest,
        node_rows,
        outer_track_rows,
        zero_rows,
        pole_rows,
        residue_rows,
        cubature_summary,
        validations,
        sum(node_cache_flags.values()),
        interval_hits,
        interval_misses,
        elapsed,
    )
    atomic_text(DOCUMENT, document)
    passed = all(bool(row["passed"]) for row in validations)
    result = {
        "marker": MARKER,
        "revision": REVISION,
        "dry_run": dry_run,
        "manifest_hash": manifest["manifest_hash"],
        "outer_node_count": len(node_rows),
        "nested_job_count": manifest["nested_job_count"],
        "node_cache_hit_count": sum(node_cache_flags.values()),
        "winding_cache_hit_count": interval_hits,
        "winding_cache_miss_count": interval_misses,
        "geometric_pole_count": len(pole_rows),
        "active_pole_count": sum(
            bool(row["causal_family_active"]) for row in pole_rows
        ),
        "accepted_residue_fit_count": sum(
            bool(row["fit_passed"]) for row in residue_rows
        ),
        "cubature": cubature_summary,
        "decision": (
            "ADOPT_TWO_ANGULAR_NESTED_CAUSAL_CUBATURE_PILOT"
            if passed
            else "HOLD_TWO_ANGULAR_CUBATURE_PENDING_FAILED_GATE"
        ),
        "formalization_workbench_digest": formal_after,
        "elapsed_seconds": elapsed,
        "outputs": [
            str(path)
            for path in (
                MANIFEST_JSON,
                MANIFEST_CSV,
                DRY_RUN,
                OUTER_TRACK_ROWS,
                ZERO_ROWS,
                WINDING_ROWS,
                WINDING_CACHE,
                NODE_ROWS,
                CLOSURE_ROWS,
                SCAN_ROWS,
                POLE_ROWS,
                TOPOLOGY_ROWS,
                RESIDUE_ROWS,
                INNER_QUADRATURE_ROWS,
                INNER_EXTRAPOLATION_ROWS,
                OUTER_RULE_ROWS,
                OUTER_CUBATURE_ROWS,
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
        raise RuntimeError(f"5240 validation failed: {failed}")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="write and validate the bounded nested manifest only",
    )
    arguments = parser.parse_args()
    if arguments.dry_run:
        report = write_manifest_and_dry_run()
        print(json.dumps(report, indent=2, sort_keys=True))
        return
    result = execute()
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
