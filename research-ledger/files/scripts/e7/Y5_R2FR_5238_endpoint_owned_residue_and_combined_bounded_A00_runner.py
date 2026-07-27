from __future__ import annotations

import argparse
import cmath
import csv
import hashlib
import importlib.util
import json
import math
import os
import sys
import time
from pathlib import Path
from typing import Any, Callable

import numpy as np


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE = POST / "source-intake" / "functional_rg" / "5238"
RESIDUALS = POST / "source-intake" / "mts_residuals"
CACHE = SOURCE / "job-cache"

SCRIPT_5237 = (
    POST
    / "scripts"
    / "Y5_R2FR_5237_bounded_multi_event_direct_A00_causal_runner.py"
)
RESULT_5237 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5237"
    / "bounded_multi_event_direct_A00_causal_run.json"
)
QUADRATURE_5237 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5237"
    / "bounded_multi_event_patch_quadrature.csv"
)
VALIDATION_5237 = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5237_VALIDATION.csv"
)

MANIFEST_JSON = SOURCE / "endpoint_bounded_job_manifest.json"
MANIFEST_CSV = SOURCE / "endpoint_bounded_job_manifest.csv"
DRY_RUN = SOURCE / "endpoint_bounded_dry_run_report.json"
RESULT = SOURCE / "endpoint_owned_and_combined_bounded_A00_run.json"
JOB_ROWS = SOURCE / "endpoint_bounded_job_summary.csv"
OWNER_ROWS = SOURCE / "endpoint_owner_identity_audit.csv"
SCAN_ROWS = SOURCE / "endpoint_surface_scan_audit.csv"
POLE_ROWS = SOURCE / "endpoint_pole_catalog.csv"
TOPOLOGY_ROWS = SOURCE / "endpoint_causal_topology_audit.csv"
RESIDUE_ROWS = SOURCE / "endpoint_residue_fit_summary.csv"
QUADRATURE_ROWS = SOURCE / "endpoint_patch_quadrature.csv"
ENDPOINT_POOL_ROWS = SOURCE / "endpoint_pool_convergence.csv"
COMBINED_POOL_ROWS = SOURCE / "direct_endpoint_combined_pool_convergence.csv"
DOCUMENT = (
    POST
    / "5238-Y5-R2FR-endpoint-owned-residue-and-combined-bounded-A00-runner.md"
)
VALIDATION = RESIDUALS / "P8_Y5_BRR545_5238_VALIDATION.csv"

MARKER = "MTS_5238_ENDPOINT_OWNED_RESIDUE_AND_COMBINED_BOUNDED_A00_RUNNER"
REVISION = "endpoint-owned-residue-combined-bounded-A00-v1"
FORMAL_BASELINE = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)
EXPECTED_FAMILY_COUNT = 4
EXPECTED_STRATUM_COUNT = 8
EXPECTED_COMPONENT_COUNT = 8
EXPECTED_JOB_COUNT = 24
MAXIMUM_JOB_COUNT = 24
MAXIMUM_TOTAL_ROOTS = 180
MAXIMUM_ROOTS_PER_JOB = 10
MAXIMUM_ACTIVE_ROOTS_PER_JOB = 8
MINIMUM_ENDPOINT_OWNER_FRACTION = 0.99
OWNER_CLOSURE_LIMIT = 2.0e-8
MAXIMUM_RUN_SECONDS = 4.0 * 60.0 * 60.0


def load_module(path: Path, name: str) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5237 = load_module(SCRIPT_5237, "mts_5237_for_5238")
M5235 = M5237.M5235
M5234 = M5237.M5234
M5232 = M5237.M5232
M5231 = M5237.M5231
M5024 = M5237.M5024
M5022 = M5234.M5022
M5017 = M5237.M5017
M5030 = M5237.M5030


def atomic_json(path: Path, value: Any) -> None:
    M5237.atomic_json(path, value)


def atomic_text(path: Path, value: str) -> None:
    M5237.atomic_text(path, value)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    M5237.write_csv(path, rows)


def read_csv(path: Path) -> list[dict[str, str]]:
    return M5237.read_csv(path)


def read_json(path: Path) -> Any:
    return M5237.read_json(path)


def digest(path: Path) -> str:
    return M5237.digest(path)


def tree_digest(path: Path) -> str:
    return M5237.tree_digest(path)


def complex_value(value: Any) -> complex:
    return M5237.complex_value(value)


def complex_row(value: complex) -> dict[str, float]:
    return M5237.complex_row(value)


def serialized_hash(value: Any) -> str:
    return M5237.serialized_hash(value)


def endpoint_family_strata() -> list[dict[str, str]]:
    selected: dict[tuple[str, str], dict[str, str]] = {}
    for row in read_csv(M5237.FAMILY_SOURCE):
        family = row["family"]
        magnitude = float(row["A00_family_magnitude"])
        if magnitude <= M5237.ACTIVE_FAMILY_FLOOR:
            continue
        if "subtraction:decay:" not in family:
            continue
        key = family, row["tranche"]
        if key not in selected or magnitude > float(
            selected[key]["A00_family_magnitude"]
        ):
            selected[key] = row
    rows = [selected[key] for key in sorted(selected)]
    if len({row["family"] for row in rows}) != EXPECTED_FAMILY_COUNT:
        raise RuntimeError("endpoint family count changed")
    if len(rows) != EXPECTED_STRATUM_COUNT:
        raise RuntimeError("endpoint family/tranche strata changed")
    return rows


def endpoint_candidate_rows(
    representative_pair: tuple[str, str],
) -> list[dict[str, str]]:
    rows = [
        row
        for row in read_csv(M5237.ATLAS_5234)
        if row["owner_summand"] == "endpoint_subtraction"
        and row["atlas_status"]
        != "KINEMATICALLY_FIXED_NONZERO"
    ]
    consumed = {
        M5234.endpoint_label_surface(label)[0]
        for label in representative_pair
    }
    by_surface: dict[str, dict[str, str]] = {}
    for row in rows:
        if row["surface_id"] in consumed:
            continue
        by_surface.setdefault(row["surface_id"], row)
    result = list(by_surface.values())
    result.sort(key=lambda row: row["surface_id"])
    if len(result) != 8:
        raise RuntimeError(
            f"expected 8 endpoint candidate surfaces, found {len(result)}"
        )
    return result


def endpoint_suffix_and_winding(
    entry: dict[str, Any],
) -> tuple[str, int]:
    labels = list(entry["representing_pairs"][0])
    return (
        labels[0].rsplit("_", 1)[-1],
        int(entry["winding_correction"]),
    )


def build_manifest() -> dict[str, Any]:
    contracts = {
        contract["tranche"]: contract
        for contract in M5231.source_contracts()
    }
    jobs: list[dict[str, Any]] = []
    for stratum_index, row in enumerate(
        endpoint_family_strata(), start=1
    ):
        family = row["family"]
        tranche = row["tranche"]
        seed = int(row["seed"])
        contract = contracts[tranche]
        topology_path = M5231.topology_path(
            contract, seed, M5237.EPSILON_ID
        )
        topology = read_json(topology_path)
        configuration = read_json(contract["config"])
        event = next(
            item
            for item in configuration["events"]
            if int(item["seed"]) == seed
        )
        pairs = [
            item
            for item in M5231.reciprocal_pairs(topology)
            if M5231.canonical_family(item[0], item[1]) == family
        ]
        normalized = [
            (*M5237.normalized_component(first, second), residual)
            for first, second, residual in pairs
        ]
        normalized.sort(
            key=lambda item: (
                int(item[0]["chamber_index"]),
                complex_value(item[0]["target_root"]).real,
                complex_value(item[0]["target_root"]).imag,
            )
        )
        for component_index, (
            representative,
            reciprocal,
            reciprocal_residual,
        ) in enumerate(normalized, start=1):
            representative_suffix, representative_winding = (
                endpoint_suffix_and_winding(representative)
            )
            reciprocal_suffix, reciprocal_winding = (
                endpoint_suffix_and_winding(reciprocal)
            )
            expected = {
                representative_suffix: representative_winding,
                reciprocal_suffix: reciprocal_winding,
            }
            if set(expected) != {"u", "v"}:
                raise RuntimeError(
                    f"incomplete endpoint winding map for {family}"
                )
            for coordinate in M5237.OUTER_COORDINATES:
                lower, upper = M5237.scan_domain(coordinate)
                job_number = len(jobs) + 1
                job = {
                    "job_id": f"EPM{job_number:02d}",
                    "component_id": (
                        f"ES{stratum_index:02d}_C"
                        f"{component_index:02d}"
                    ),
                    "stratum_id": f"ES{stratum_index:02d}",
                    "component_index": component_index,
                    "owner_summand": "endpoint_subtraction",
                    "family": family,
                    "tranche": tranche,
                    "seed": seed,
                    "epsilon_id": M5237.EPSILON_ID,
                    "source_A00_family_magnitude": float(
                        row["A00_family_magnitude"]
                    ),
                    "outer_coordinate": coordinate,
                    "scan_minimum": lower,
                    "scan_maximum": upper,
                    "scan_points": M5237.SCAN_POINTS,
                    "soft_energy": float(event["soft_energy"]),
                    "soft_cosine": float(event["soft_cosine"]),
                    "decay_cosine": float(event["decay_cosine"]),
                    "representative_pair": list(
                        representative["representing_pairs"][0]
                    ),
                    "reciprocal_pair": list(
                        reciprocal["representing_pairs"][0]
                    ),
                    "representative_anchor": complex_row(
                        complex_value(representative["target_root"])
                    ),
                    "reciprocal_anchor": complex_row(
                        complex_value(reciprocal["target_root"])
                    ),
                    "representative_chamber": int(
                        representative["chamber_index"]
                    ),
                    "reciprocal_chamber": int(
                        reciprocal["chamber_index"]
                    ),
                    "expected_u_winding": expected["u"],
                    "expected_v_winding": expected["v"],
                    "source_reciprocal_root_residual": float(
                        reciprocal_residual
                    ),
                    "source_topology": str(topology_path),
                    "source_config": str(contract["config"]),
                    "candidate_surface_count": 8,
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
                job["job_input_hash"] = serialized_hash(
                    {
                        "revision": REVISION,
                        "job": job,
                        "runner_script": digest(Path(__file__).resolve()),
                        "script_5237": digest(SCRIPT_5237),
                        "atlas": digest(M5237.ATLAS_5234),
                        "topology": digest(topology_path),
                    }
                )
                jobs.append(job)
    if len(jobs) != EXPECTED_JOB_COUNT:
        raise RuntimeError(
            f"expected {EXPECTED_JOB_COUNT} jobs, found {len(jobs)}"
        )
    return {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "scope": (
            "maximum-magnitude event in each endpoint-family/tranche "
            "stratum, every reciprocal component and all three "
            "conditional coordinates"
        ),
        "bounds": {
            "maximum_job_count": MAXIMUM_JOB_COUNT,
            "maximum_run_seconds": MAXIMUM_RUN_SECONDS,
            "scan_points_per_job": M5237.SCAN_POINTS,
            "maximum_roots_per_job": MAXIMUM_ROOTS_PER_JOB,
            "maximum_total_roots": MAXIMUM_TOTAL_ROOTS,
            "maximum_active_roots_per_job": (
                MAXIMUM_ACTIVE_ROOTS_PER_JOB
            ),
            "quadrature_orders": list(M5237.QUADRATURE_ORDERS),
        },
        "source_paths": [
            str(SCRIPT_5237),
            str(RESULT_5237),
            str(QUADRATURE_5237),
            str(VALIDATION_5237),
            str(M5237.ATLAS_5234),
            str(M5237.FAMILY_SOURCE),
        ],
        "jobs": jobs,
        "claim_boundary": {
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
        },
    }


def manifest_csv_rows(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    return M5237.manifest_csv_rows(manifest)


def write_manifest_and_dry_run() -> dict[str, Any]:
    manifest = build_manifest()
    atomic_json(MANIFEST_JSON, manifest)
    write_csv(MANIFEST_CSV, manifest_csv_rows(manifest))
    jobs = manifest["jobs"]
    required = [
        Path(path) for path in manifest["source_paths"]
    ] + [
        Path(job["source_topology"]) for job in jobs
    ] + [
        Path(job["source_config"]) for job in jobs
    ]
    component_ids = {job["component_id"] for job in jobs}
    checks = {
        "all_source_paths_exist": all(path.exists() for path in required),
        "job_count_within_bound": (
            len(jobs) == EXPECTED_JOB_COUNT
            and len(jobs) <= MAXIMUM_JOB_COUNT
        ),
        "job_ids_unique": len({job["job_id"] for job in jobs}) == len(jobs),
        "family_coverage_complete": (
            len({job["family"] for job in jobs})
            == EXPECTED_FAMILY_COUNT
        ),
        "stratum_coverage_complete": (
            len(
                {
                    (job["family"], job["tranche"])
                    for job in jobs
                }
            )
            == EXPECTED_STRATUM_COUNT
        ),
        "component_coordinate_cross_product_complete": (
            len(component_ids) == EXPECTED_COMPONENT_COUNT
            and all(
                {
                    job["outer_coordinate"]
                    for job in jobs
                    if job["component_id"] == component_id
                }
                == set(M5237.OUTER_COORDINATES)
                for component_id in component_ids
            )
        ),
        "candidate_surface_contract_complete": all(
            int(job["candidate_surface_count"]) == 8 for job in jobs
        ),
        "all_claim_flags_false": all(
            not bool(job[key])
            for job in jobs
            for key in (
                "valid_for_numeric_UV_claim",
                "valid_for_local_GR_claim",
                "valid_for_full_MTS_claim",
            )
        ),
    }
    report = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "mode": "dry_run",
        "manifest_sha256": digest(MANIFEST_JSON),
        "manifest_job_count": len(jobs),
        "family_count": len({job["family"] for job in jobs}),
        "family_tranche_stratum_count": len(
            {(job["family"], job["tranche"]) for job in jobs}
        ),
        "reciprocal_component_count": len(component_ids),
        "unique_event_count": len(
            {(job["tranche"], job["seed"]) for job in jobs}
        ),
        "estimated_surface_evaluations": (
            len(jobs) * 8 * M5237.SCAN_POINTS
        ),
        "checks": checks,
        "authorized_to_execute": all(checks.values()),
        "claim_boundary": manifest["claim_boundary"],
    }
    atomic_json(DRY_RUN, report)
    return report


def event_from_job(job: dict[str, Any]) -> dict[str, Any]:
    return M5237.event_from_job(job)


def build_problem(job: dict[str, Any]) -> dict[str, Any]:
    topology = read_json(Path(job["source_topology"]))
    target = complex_value(topology["target_cosine"])
    event = event_from_job(job)
    representative_pair = tuple(job["representative_pair"])
    reciprocal_pair = tuple(job["reciprocal_pair"])
    representative = M5237.find_source_crossing(
        topology,
        int(job["representative_chamber"]),
        representative_pair,
        complex_value(job["representative_anchor"]),
    )
    reciprocal = M5237.find_source_crossing(
        topology,
        int(job["reciprocal_chamber"]),
        reciprocal_pair,
        complex_value(job["reciprocal_anchor"]),
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
            job["outer_coordinate"],
            coordinates,
        ),
        M5237.pair_key(
            reciprocal_pair
        ): M5237.build_coordinate_branch_track(
            event,
            target,
            reciprocal_pair,
            complex_value(job["reciprocal_anchor"]),
            job["outer_coordinate"],
            coordinates,
        ),
    }
    case = {
        "case_id": job["job_id"],
        "family": job["family"],
        "tranche": job["tranche"],
        "seed": int(job["seed"]),
        "outer_coordinate": job["outer_coordinate"],
        "representative_pair": representative_pair,
        "reciprocal_pair": reciprocal_pair,
        "expected_u_winding": int(job["expected_u_winding"]),
        "expected_v_winding": int(job["expected_v_winding"]),
    }
    return {
        "job": job,
        "owner_summand": "endpoint_subtraction",
        "component_id": job["component_id"],
        "case": case,
        "event": event,
        "topology": topology,
        "target": target,
        "representative": representative,
        "reciprocal": reciprocal,
        "atlas_rows": endpoint_candidate_rows(representative_pair),
        "coordinates": coordinates,
        "branch_tracks": branch_tracks,
    }


def endpoint_geometry(
    problem: dict[str, Any], coordinate: complex
) -> dict[str, Any]:
    event = dict(problem["event"])
    event[problem["case"]["outer_coordinate"]] = float(coordinate.real)
    relative_root, _ = M5237.selected_component_roots(
        problem, coordinate
    )
    rationals = M5231.root_rationals(event, problem["target"])
    global_values = [
        M5231.rational_value_and_derivative(
            rationals[label], relative_root
        )[0]
        for label in problem["case"]["representative_pair"]
    ]
    global_root = complex(sum(global_values) / len(global_values))
    soft_direction, decay_direction, _ = M5232.M5028.event_geometry(
        float(event["soft_energy"]),
        complex(float(event["soft_cosine"])),
        complex(float(event["decay_cosine"])),
        relative_root,
    )
    soft_rotated = M5022.rotate_vector(soft_direction, global_root)
    decay_rotated = M5022.rotate_vector(decay_direction, global_root)
    endpoint_internal = np.zeros((3, 4), dtype=np.complex128)
    endpoint_internal[0] = np.concatenate(([1.0], decay_rotated))
    endpoint_internal[1] = np.concatenate(([1.0], -decay_rotated))
    left, right = M5017.cut_momenta(
        endpoint_internal, problem["target"], 1.0
    )
    soft_left = np.concatenate(([1.0], soft_rotated)).astype(
        np.complex128
    )
    return {
        "left": left,
        "right": right,
        "soft_left": soft_left,
        "soft_right": -soft_left,
    }


def endpoint_surface_values(
    problem: dict[str, Any], coordinate: complex
) -> dict[str, complex]:
    geometry = endpoint_geometry(problem, coordinate)
    left = geometry["left"]
    right = geometry["right"]
    soft_left = geometry["soft_left"]
    soft_right = geometry["soft_right"]
    values = {
        "endpoint:shared:soft:s13": M5234.vector_invariant(
            left[1], soft_left
        ),
        "endpoint:shared:soft:s23": M5234.vector_invariant(
            left[2], soft_left
        ),
        "endpoint:L:hard:s01=s24": M5234.pair_invariant(left, 0, 1),
        "endpoint:L:hard:s02=s14": M5234.pair_invariant(left, 0, 2),
        "endpoint:L:soft:s03": M5234.vector_invariant(
            left[0], soft_left
        ),
        "endpoint:L:soft:s34": M5234.vector_invariant(
            left[4], soft_left
        ),
        "endpoint:R:hard:s01=s24": M5234.pair_invariant(
            right, 0, 1
        ),
        "endpoint:R:hard:s02=s14": M5234.pair_invariant(
            right, 0, 2
        ),
        "endpoint:R:soft:s03": M5234.vector_invariant(
            right[0], soft_right
        ),
        "endpoint:R:soft:s34": M5234.vector_invariant(
            right[4], soft_right
        ),
    }
    return {
        row["surface_id"]: values[row["surface_id"]]
        for row in problem["atlas_rows"]
    }


def scan_surfaces(
    problem: dict[str, Any],
) -> tuple[dict[str, list[complex]], list[dict[str, Any]]]:
    values_by_surface = {
        row["surface_id"]: [] for row in problem["atlas_rows"]
    }
    for coordinate in problem["coordinates"]:
        values = endpoint_surface_values(
            problem, complex(float(coordinate))
        )
        for surface_id, value in values.items():
            values_by_surface[surface_id].append(value)
    rows: list[dict[str, Any]] = []
    for surface_id, values in values_by_surface.items():
        array = np.asarray(values, dtype=np.complex128)
        magnitudes = np.abs(array)
        real_values = np.real(array)
        minimum_index = int(np.argmin(magnitudes))
        rows.append(
            {
                "job_id": problem["job"]["job_id"],
                "component_id": problem["component_id"],
                "family": problem["case"]["family"],
                "outer_coordinate": problem["case"]["outer_coordinate"],
                "surface_id": surface_id,
                "sign_change_count": int(
                    sum(
                        real_values[index]
                        * real_values[index + 1]
                        < 0.0
                        for index in range(len(real_values) - 1)
                    )
                ),
                "minimum_channel_magnitude": float(
                    magnitudes[minimum_index]
                ),
                "minimum_channel_coordinate": float(
                    problem["coordinates"][minimum_index]
                ),
                "median_channel_magnitude": float(
                    np.median(magnitudes)
                ),
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    return values_by_surface, rows


def bisect_real_zero(
    problem: dict[str, Any],
    surface_id: str,
    lower: float,
    upper: float,
) -> float:
    lower_value = endpoint_surface_values(
        problem, complex(lower)
    )[surface_id].real
    upper_value = endpoint_surface_values(
        problem, complex(upper)
    )[surface_id].real
    if lower_value == 0.0:
        return lower
    if upper_value == 0.0:
        return upper
    if lower_value * upper_value > 0.0:
        raise RuntimeError("endpoint root bracket does not change sign")
    for _ in range(70):
        midpoint = 0.5 * (lower + upper)
        midpoint_value = endpoint_surface_values(
            problem, complex(midpoint)
        )[surface_id].real
        if lower_value * midpoint_value <= 0.0:
            upper = midpoint
            upper_value = midpoint_value
        else:
            lower = midpoint
            lower_value = midpoint_value
        if upper - lower < 2.0e-14:
            break
    return 0.5 * (lower + upper)


def locate_geometric_roots(
    problem: dict[str, Any],
    values_by_surface: dict[str, list[complex]],
) -> list[dict[str, Any]]:
    coordinates = problem["coordinates"]
    raw_roots: list[dict[str, Any]] = []
    for surface_id, values in values_by_surface.items():
        centers: list[float] = []
        for index in range(len(coordinates) - 1):
            left = values[index].real
            right = values[index + 1].real
            if left == 0.0:
                centers.append(float(coordinates[index]))
            elif left * right < 0.0:
                centers.append(
                    bisect_real_zero(
                        problem,
                        surface_id,
                        float(coordinates[index]),
                        float(coordinates[index + 1]),
                    )
                )
        if values[-1].real == 0.0:
            centers.append(float(coordinates[-1]))
        for center in centers:
            if any(
                row["surface_id"] == surface_id
                and abs(center - row["real_axis_center"]) < 1.0e-8
                for row in raw_roots
            ):
                continue
            step = 1.0e-6
            center_value = endpoint_surface_values(
                problem, complex(center)
            )[surface_id]
            derivative = (
                endpoint_surface_values(
                    problem, complex(center + step)
                )[surface_id]
                - endpoint_surface_values(
                    problem, complex(center - step)
                )[surface_id]
            ) / (2.0 * step)
            if abs(derivative) < 1.0e-10:
                continue
            pole = complex(center) - center_value / derivative
            if not (
                float(problem["job"]["scan_minimum"]) < pole.real
                < float(problem["job"]["scan_maximum"])
                and abs(pole.imag) < M5237.POLE_IMAGINARY_LIMIT
            ):
                continue
            raw_roots.append(
                {
                    "surface_id": surface_id,
                    "real_axis_center": center,
                    "channel_at_center": center_value,
                    "channel_derivative": derivative,
                    "complex_pole": pole,
                }
            )
    raw_roots.sort(key=lambda row: row["complex_pole"].real)
    groups: list[list[dict[str, Any]]] = []
    for root in raw_roots:
        group = next(
            (
                candidate
                for candidate in groups
                if abs(
                    candidate[0]["complex_pole"]
                    - root["complex_pole"]
                )
                < M5237.ROOT_GROUP_TOLERANCE
            ),
            None,
        )
        if group is None:
            groups.append([root])
        else:
            group.append(root)
    rows: list[dict[str, Any]] = []
    for index, group in enumerate(groups, start=1):
        representative = min(
            group, key=lambda row: abs(row["channel_at_center"])
        )
        rows.append(
            {
                "job_id": problem["job"]["job_id"],
                "pole_id": f"EP{index:02d}",
                "component_id": problem["component_id"],
                "family": problem["case"]["family"],
                "tranche": problem["case"]["tranche"],
                "seed": problem["case"]["seed"],
                "outer_coordinate": problem["case"]["outer_coordinate"],
                "surface_ids": "|".join(
                    sorted(row["surface_id"] for row in group)
                ),
                "surface_count": len(group),
                "primary_surface_id": representative["surface_id"],
                "real_axis_center": representative["real_axis_center"],
                "pole_real": representative["complex_pole"].real,
                "pole_imaginary": representative["complex_pole"].imag,
                "channel_at_center_real": representative[
                    "channel_at_center"
                ].real,
                "channel_at_center_imaginary": representative[
                    "channel_at_center"
                ].imag,
                "channel_derivative_real": representative[
                    "channel_derivative"
                ].real,
                "channel_derivative_imaginary": representative[
                    "channel_derivative"
                ].imag,
                "geometric_root": True,
                "causal_family_active": False,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    return rows


def local_endpoint_residue_data(
    problem: dict[str, Any],
    coordinate: float,
    include_direct: bool,
) -> dict[str, Any]:
    event = dict(problem["event"])
    event[problem["case"]["outer_coordinate"]] = float(coordinate)
    topology = M5237.updated_component_topology(problem, coordinate)
    cycle_active, reciprocal_residual = M5237.component_cycle_state(
        problem, coordinate, topology
    )
    if not cycle_active:
        return {
            "cycle_active": False,
            "reciprocal_residual": reciprocal_residual,
            "endpoint_contribution": 0.0j,
            "direct_contribution": 0.0j,
            "full_split_contribution": 0.0j,
            "endpoint_owner_fraction": None,
        }
    pairs = M5231.reciprocal_pairs(topology)
    if len(pairs) != 1:
        raise RuntimeError(
            f"endpoint component has {len(pairs)} reciprocal pairs"
        )
    first, second, _ = pairs[0]
    representative, partner = (
        (first, second)
        if abs(complex_value(first["target_root"])) >= 1.0
        else (second, first)
    )
    labels = representative["representing_pairs"][0]
    relative_root = complex_value(representative["target_root"])
    rationals = M5231.root_rationals(event, problem["target"])
    first_root, first_derivative = (
        M5231.rational_value_and_derivative(
            rationals[labels[0]], relative_root
        )
    )
    second_root, second_derivative = (
        M5231.rational_value_and_derivative(
            rationals[labels[1]], relative_root
        )
    )
    global_root = 0.5 * (first_root + second_root)
    soft_direction, decay_direction, internal = (
        M5232.M5028.event_geometry(
            float(event["soft_energy"]),
            complex(float(event["soft_cosine"])),
            complex(float(event["decay_cosine"])),
            relative_root,
        )
    )
    phase = cmath.exp(0.37j)
    scale = max(1.0, abs(global_root))
    endpoint_samples: list[complex] = []
    direct_samples: list[complex] = []
    for fraction in (2.0e-5, 1.0e-5, 5.0e-6):
        displacement = fraction * scale * phase
        point = global_root + displacement
        endpoint_integrand = (
            -M5022.endpoint_value(
                soft_direction,
                decay_direction,
                problem["target"],
                point,
            )
            / float(event["soft_energy"])
        )
        endpoint_samples.append(
            complex(endpoint_integrand * displacement**2)
        )
        if include_direct:
            rotated = M5024.rotate_internal(internal, point)
            inverse_energy_square_sum = sum(
                1.0 / (momentum[0] * momentum[0])
                for momentum in rotated
            )
            multiplier = (
                3.0
                / (rotated[2, 0] * rotated[2, 0])
                / inverse_energy_square_sum
            )
            direct_integrand = (
                float(event["soft_energy"])
                * multiplier
                * M5017.hhh_reduced_product(
                    rotated, problem["target"], 1.0
                )
                / (M5017.S_VALUE * M5017.S_VALUE)
            )
            direct_samples.append(
                complex(direct_integrand * displacement**2)
            )
    endpoint_coefficient = (
        2.0 * endpoint_samples[-1] - endpoint_samples[-2]
    )
    direct_coefficient = (
        2.0 * direct_samples[-1] - direct_samples[-2]
        if include_direct
        else 0.0j
    )
    middle = max(abs(endpoint_samples[-2]), 1.0e-300)
    scaling_power = -math.log(
        max(abs(endpoint_samples[-1]) / middle, 1.0e-300),
        2.0,
    )
    if scaling_power > M5231.DOUBLE_POLE_POWER_MAXIMUM:
        endpoint_coefficient = 0.0j
    chamber = topology["chambers"][
        int(representative["chamber_index"])
    ]
    ownership = M5231.chamber_ownership(event, chamber)
    owned = [bool(ownership[label]) for label in labels]
    if sum(owned) != 1:
        raise RuntimeError(
            f"endpoint collision ownership is not unique: {owned}"
        )
    orientation = 1.0 if owned[0] else -1.0
    collision_jacobian = first_derivative - second_derivative
    denominator = relative_root * global_root * collision_jacobian
    winding_difference = int(
        representative["winding_correction"]
    ) - int(partner["winding_correction"])
    endpoint_contribution = (
        winding_difference
        * orientation
        * endpoint_coefficient
        / denominator
    )
    direct_contribution = (
        winding_difference
        * orientation
        * direct_coefficient
        / denominator
    )
    coefficient_denominator = max(
        abs(endpoint_coefficient) + abs(direct_coefficient),
        1.0e-300,
    )
    return {
        "cycle_active": True,
        "reciprocal_residual": reciprocal_residual,
        "endpoint_contribution": complex(endpoint_contribution),
        "direct_contribution": complex(direct_contribution),
        "full_split_contribution": complex(
            endpoint_contribution + direct_contribution
        ),
        "endpoint_coefficient": endpoint_coefficient,
        "direct_coefficient": direct_coefficient,
        "endpoint_owner_fraction": (
            abs(endpoint_coefficient) / coefficient_denominator
            if include_direct
            else None
        ),
        "coefficient_scaling_power": scaling_power,
        "relative_root": relative_root,
        "global_root": global_root,
        "collision_jacobian": collision_jacobian,
        "winding_difference": winding_difference,
    }


def endpoint_contribution(
    problem: dict[str, Any], coordinate: float
) -> complex:
    return complex(
        local_endpoint_residue_data(
            problem, coordinate, include_direct=False
        )["endpoint_contribution"]
    )


def owner_identity_audit(problem: dict[str, Any]) -> dict[str, Any]:
    coordinate = float(
        problem["event"][problem["case"]["outer_coordinate"]]
    )
    data = local_endpoint_residue_data(
        problem, coordinate, include_direct=True
    )
    full = M5237.component_contribution(problem, coordinate)
    split = complex(data["full_split_contribution"])
    endpoint = complex(data["endpoint_contribution"])
    closure = abs(split - full) / max(abs(full), 1.0e-30)
    endpoint_difference = abs(endpoint - full) / max(
        abs(full), 1.0e-30
    )
    return {
        "job_id": problem["job"]["job_id"],
        "component_id": problem["component_id"],
        "family": problem["case"]["family"],
        "tranche": problem["case"]["tranche"],
        "seed": problem["case"]["seed"],
        "outer_coordinate": problem["case"]["outer_coordinate"],
        "base_coordinate": coordinate,
        "cycle_active": data["cycle_active"],
        "endpoint_owner_fraction": data["endpoint_owner_fraction"],
        "split_to_full_relative_closure_residual": closure,
        "endpoint_to_full_relative_difference": endpoint_difference,
        "endpoint_contribution_real": endpoint.real,
        "endpoint_contribution_imaginary": endpoint.imag,
        "direct_contamination_real": complex(
            data["direct_contribution"]
        ).real,
        "direct_contamination_imaginary": complex(
            data["direct_contribution"]
        ).imag,
        "full_contribution_real": full.real,
        "full_contribution_imaginary": full.imag,
        "coefficient_scaling_power": data.get(
            "coefficient_scaling_power"
        ),
        "reciprocal_residual": data["reciprocal_residual"],
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }


def fit_active_residues(
    problem: dict[str, Any],
    poles: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    active = [row for row in poles if row["causal_family_active"]]
    all_centers = [
        float(row["real_axis_center"]) for row in poles
    ]
    lower = float(problem["job"]["scan_minimum"])
    upper = float(problem["job"]["scan_maximum"])
    rows: list[dict[str, Any]] = []
    for pole in active:
        center = float(pole["real_axis_center"])
        nearest = min(
            (
                abs(center - other)
                for other in all_centers
                if other != center
            ),
            default=math.inf,
        )
        cycle_half_width = M5237.local_cycle_half_width(
            problem, center
        )
        maximum_fit_radius = min(
            5.0e-3,
            0.2 * nearest,
            0.2 * cycle_half_width,
            0.2 * (center - lower),
            0.2 * (upper - center),
        )
        if maximum_fit_radius < 2.0e-5:
            raise RuntimeError(
                f"insufficient endpoint fit radius at {center}"
            )
        surface_id = pole["primary_surface_id"]
        complex_pole = complex(
            float(pole["pole_real"]),
            float(pole["pole_imaginary"]),
        )
        derivative = complex(
            float(pole["channel_derivative_real"]),
            float(pole["channel_derivative_imaginary"]),
        )
        candidates: list[dict[str, Any]] = []
        for refinement in range(6):
            radius = maximum_fit_radius * 0.5**refinement
            if radius < 2.0e-5:
                break
            offsets = radius * np.asarray(
                (
                    -1.0,
                    -0.5,
                    -0.2,
                    -0.1,
                    0.1,
                    0.2,
                    0.5,
                    1.0,
                )
            )
            contributions: list[complex] = []
            numerators: list[complex] = []
            for offset in offsets:
                coordinate = center + float(offset)
                contribution = endpoint_contribution(
                    problem, coordinate
                )
                channel = endpoint_surface_values(
                    problem, complex(coordinate)
                )[surface_id]
                contributions.append(contribution)
                numerators.append(channel * contribution)
            coefficients = np.polyfit(
                offsets,
                np.asarray(numerators, dtype=np.complex128),
                3,
            )
            fitted = np.polyval(coefficients, offsets)
            numerator_array = np.asarray(
                numerators, dtype=np.complex128
            )
            fit_residual = float(
                np.max(np.abs(fitted - numerator_array))
                / max(float(np.max(np.abs(numerator_array))), 1.0e-30)
            )
            numerator_at_pole = complex(
                np.polyval(coefficients, complex_pole - center)
            )
            slopes: dict[str, float] = {}
            for side, sign in (
                ("negative", -1.0),
                ("positive", 1.0),
            ):
                selected = [
                    index
                    for index, offset in enumerate(offsets)
                    if float(offset) * sign > 0.0
                ]
                slope, _ = np.polyfit(
                    np.log(
                        [
                            abs(
                                center
                                + float(offsets[index])
                                - complex_pole
                            )
                            for index in selected
                        ]
                    ),
                    np.log(
                        [
                            max(
                                abs(contributions[index]),
                                1.0e-300,
                            )
                            for index in selected
                        ]
                    ),
                    1,
                )
                slopes[side] = float(slope)
            passed = (
                fit_residual
                <= M5237.NUMERATOR_FIT_RELATIVE_RESIDUAL_LIMIT
                and all(
                    abs(slopes[side] + 1.0)
                    <= M5237.SLOPE_TOLERANCE
                    for side in ("negative", "positive")
                )
            )
            candidates.append(
                {
                    "fit_radius": radius,
                    "fit_residual": fit_residual,
                    "numerator_at_pole": numerator_at_pole,
                    "slopes": slopes,
                    "fit_passed": passed,
                    "score": max(
                        fit_residual
                        / M5237.NUMERATOR_FIT_RELATIVE_RESIDUAL_LIMIT,
                        *[
                            abs(slopes[side] + 1.0)
                            / M5237.SLOPE_TOLERANCE
                            for side in ("negative", "positive")
                        ],
                    ),
                }
            )
            if passed:
                break
        selected_fit = next(
            (
                candidate
                for candidate in candidates
                if candidate["fit_passed"]
            ),
            min(candidates, key=lambda candidate: candidate["score"]),
        )
        numerator_at_pole = complex(
            selected_fit["numerator_at_pole"]
        )
        residue = numerator_at_pole / derivative
        radius = float(selected_fit["fit_radius"])
        rows.append(
            {
                "job_id": problem["job"]["job_id"],
                "pole_id": pole["pole_id"],
                "component_id": problem["component_id"],
                "family": problem["case"]["family"],
                "surface_id": surface_id,
                "center": center,
                "pole_real": complex_pole.real,
                "pole_imaginary": complex_pole.imag,
                "fit_radius": radius,
                "local_cycle_half_width": cycle_half_width,
                "patch_half_width": min(
                    M5237.PATCH_HALF_WIDTH,
                    0.8 * cycle_half_width,
                    radius,
                ),
                "fit_refinement_count": candidates.index(selected_fit),
                "channel_derivative_real": derivative.real,
                "channel_derivative_imaginary": derivative.imag,
                "numerator_at_pole_real": numerator_at_pole.real,
                "numerator_at_pole_imaginary": numerator_at_pole.imag,
                "outer_residue_real": residue.real,
                "outer_residue_imaginary": residue.imag,
                "numerator_fit_relative_residual": selected_fit[
                    "fit_residual"
                ],
                "negative_log_log_slope": selected_fit["slopes"][
                    "negative"
                ],
                "positive_log_log_slope": selected_fit["slopes"][
                    "positive"
                ],
                "fit_passed": selected_fit["fit_passed"],
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    return rows


def integrate_patch_unions(
    problem: dict[str, Any],
    fits: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    accepted = [row for row in fits if bool(row["fit_passed"])]
    groups = M5237.patch_groups(
        accepted,
        float(problem["job"]["scan_minimum"]),
        float(problem["job"]["scan_maximum"]),
    )
    rows: list[dict[str, Any]] = []
    combined: dict[int, tuple[complex, complex]] = {}
    for group_index, group in enumerate(groups, start=1):
        lower = float(group["lower"])
        upper = float(group["upper"])
        singular_terms = [
            (
                complex(
                    float(fit["pole_real"]),
                    float(fit["pole_imaginary"]),
                ),
                complex(
                    float(fit["outer_residue_real"]),
                    float(fit["outer_residue_imaginary"]),
                ),
            )
            for fit in group["fits"]
        ]
        analytic = sum(
            (
                residue
                * (
                    np.log(upper - pole)
                    - np.log(lower - pole)
                )
                for pole, residue in singular_terms
            ),
            0.0j,
        )
        for order in M5237.QUADRATURE_ORDERS:
            nodes, weights = np.polynomial.legendre.leggauss(order)
            half_width = 0.5 * (upper - lower)
            midpoint = 0.5 * (upper + lower)
            coordinates = half_width * nodes + midpoint
            physical_weights = half_width * weights
            values = np.asarray(
                [
                    endpoint_contribution(problem, float(coordinate))
                    for coordinate in coordinates
                ],
                dtype=np.complex128,
            )
            singular = np.asarray(
                [
                    sum(
                        (
                            residue / (coordinate - pole)
                            for pole, residue in singular_terms
                        ),
                        0.0j,
                    )
                    for coordinate in coordinates
                ],
                dtype=np.complex128,
            )
            raw = complex(np.sum(physical_weights * values))
            regular = complex(
                np.sum(physical_weights * (values - singular))
            )
            subtracted = regular + analytic
            rows.append(
                {
                    "job_id": problem["job"]["job_id"],
                    "component_id": problem["component_id"],
                    "family": problem["case"]["family"],
                    "patch_group_id": f"EG{group_index:02d}",
                    "pole_ids": "|".join(
                        fit["pole_id"] for fit in group["fits"]
                    ),
                    "pole_count": len(group["fits"]),
                    "quadrature_order": order,
                    "patch_lower": lower,
                    "patch_upper": upper,
                    "raw_integral_real": raw.real,
                    "raw_integral_imaginary": raw.imag,
                    "regular_remainder_real": regular.real,
                    "regular_remainder_imaginary": regular.imag,
                    "analytic_singular_real": analytic.real,
                    "analytic_singular_imaginary": analytic.imag,
                    "subtracted_integral_real": subtracted.real,
                    "subtracted_integral_imaginary": subtracted.imag,
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
            )
    if not groups:
        return rows, {
            "active_patch_group_count": 0,
            "accepted_fit_count": 0,
            "quadrature_available": False,
        }
    for order in M5237.QUADRATURE_ORDERS:
        selected = [
            row
            for row in rows
            if int(row["quadrature_order"]) == order
        ]
        raw = sum(
            (
                complex(
                    float(row["raw_integral_real"]),
                    float(row["raw_integral_imaginary"]),
                )
                for row in selected
            ),
            0.0j,
        )
        subtracted = sum(
            (
                complex(
                    float(row["subtracted_integral_real"]),
                    float(row["subtracted_integral_imaginary"]),
                )
                for row in selected
            ),
            0.0j,
        )
        combined[order] = raw, subtracted
    reference = combined[M5237.QUADRATURE_ORDERS[-1]][1]
    denominator = max(abs(reference), 1.0)
    errors = {
        order: {
            "raw": abs(combined[order][0] - reference) / denominator,
            "subtracted": abs(
                combined[order][1] - reference
            )
            / denominator,
        }
        for order in M5237.QUADRATURE_ORDERS
    }
    low = M5237.QUADRATURE_ORDERS[0]
    mid = M5237.QUADRATURE_ORDERS[1]
    return rows, {
        "active_patch_group_count": len(groups),
        "accepted_fit_count": len(accepted),
        "quadrature_available": True,
        "reference_order": M5237.QUADRATURE_ORDERS[-1],
        "subtracted_reference": complex_row(reference),
        "low_order_raw_relative_error": errors[low]["raw"],
        "low_order_subtracted_relative_error": errors[low][
            "subtracted"
        ],
        "mid_order_subtracted_relative_error": errors[mid][
            "subtracted"
        ],
        "low_order_improvement_factor": (
            errors[low]["raw"]
            / max(errors[low]["subtracted"], 1.0e-30)
        ),
    }


def run_job(job: dict[str, Any]) -> dict[str, Any]:
    started = time.monotonic()
    problem = build_problem(job)
    values, scan_rows = scan_surfaces(problem)
    poles = locate_geometric_roots(problem, values)
    if len(poles) > MAXIMUM_ROOTS_PER_JOB:
        raise RuntimeError("endpoint root cap exceeded")
    topology_rows = M5237.topology_audit(problem, poles)
    active = [row for row in poles if row["causal_family_active"]]
    if len(active) > MAXIMUM_ACTIVE_ROOTS_PER_JOB:
        raise RuntimeError("endpoint active-root cap exceeded")
    owner = owner_identity_audit(problem)
    fits = fit_active_residues(problem, poles)
    quadrature_rows, quadrature = integrate_patch_unions(
        problem, fits
    )
    branch_steps = [
        float(track["maximum_projective_step"])
        for track in problem["branch_tracks"].values()
    ]
    topology_stable = all(
        float(row["maximum_pair_projective_step"])
        < M5237.PROJECTIVE_LIMIT
        and float(row["maximum_reciprocal_product_residual"])
        < M5237.RECIPROCAL_LIMIT
        for row in poles
    )
    owner_passed = (
        bool(owner["cycle_active"])
        and float(owner["endpoint_owner_fraction"])
        >= MINIMUM_ENDPOINT_OWNER_FRACTION
        and float(owner["split_to_full_relative_closure_residual"])
        <= OWNER_CLOSURE_LIMIT
    )
    fit_complete = len(fits) == len(active) and all(
        bool(row["fit_passed"]) for row in fits
    )
    quadrature_passed = (
        not active
        or (
            quadrature["quadrature_available"]
            and float(
                quadrature["low_order_subtracted_relative_error"]
            )
            <= M5237.LOW_ORDER_SUBTRACTED_RELATIVE_ERROR_LIMIT
            and float(
                quadrature["mid_order_subtracted_relative_error"]
            )
            <= M5237.MID_ORDER_SUBTRACTED_RELATIVE_ERROR_LIMIT
        )
    )
    job_passed = (
        topology_stable
        and owner_passed
        and fit_complete
        and quadrature_passed
        and max(branch_steps, default=0.0)
        < M5237.PROJECTIVE_LIMIT
    )
    return {
        "job_id": job["job_id"],
        "job_input_hash": job["job_input_hash"],
        "status": "COMPLETED" if job_passed else "COMPLETED_WITH_FAILURE",
        "job_passed": job_passed,
        "elapsed_seconds": time.monotonic() - started,
        "geometric_root_count": len(poles),
        "active_root_count": len(active),
        "inactive_root_count": len(poles) - len(active),
        "maximum_coordinate_branch_projective_step": max(
            branch_steps, default=0.0
        ),
        "topology_stable": topology_stable,
        "owner_passed": owner_passed,
        "fit_complete": fit_complete,
        "quadrature_passed": quadrature_passed,
        "owner": owner,
        "scan_rows": scan_rows,
        "poles": poles,
        "topology_rows": topology_rows,
        "fits": fits,
        "quadrature_rows": quadrature_rows,
        "quadrature": quadrature,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }


def execute_jobs(
    manifest: dict[str, Any],
) -> tuple[list[dict[str, Any]], int]:
    started = time.monotonic()
    results: list[dict[str, Any]] = []
    cache_hits = 0
    for job in manifest["jobs"]:
        if time.monotonic() - started > MAXIMUM_RUN_SECONDS:
            raise RuntimeError("endpoint bounded time cap exceeded")
        cache_path = CACHE / f"{job['job_id']}.json"
        if cache_path.exists():
            cached = read_json(cache_path)
            if (
                cached.get("job_input_hash")
                == job["job_input_hash"]
                and cached.get("status")
                in {"COMPLETED", "COMPLETED_WITH_FAILURE"}
            ):
                results.append(cached)
                cache_hits += 1
                continue
        try:
            result = run_job(job)
        except Exception as error:
            result = {
                "job_id": job["job_id"],
                "job_input_hash": job["job_input_hash"],
                "status": "FAILED",
                "job_passed": False,
                "error": f"{type(error).__name__}: {error}",
                "elapsed_seconds": 0.0,
                "geometric_root_count": 0,
                "active_root_count": 0,
                "inactive_root_count": 0,
                "owner": {},
                "scan_rows": [],
                "poles": [],
                "topology_rows": [],
                "fits": [],
                "quadrature_rows": [],
                "quadrature": {
                    "quadrature_available": False,
                },
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        atomic_json(cache_path, result)
        results.append(result)
    return results, cache_hits


def flatten_results(
    jobs: list[dict[str, Any]],
    results: list[dict[str, Any]],
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
]:
    lookup = {job["job_id"]: job for job in jobs}
    job_rows: list[dict[str, Any]] = []
    owner_rows: list[dict[str, Any]] = []
    scan_rows: list[dict[str, Any]] = []
    poles: list[dict[str, Any]] = []
    topology: list[dict[str, Any]] = []
    fits: list[dict[str, Any]] = []
    quadrature: list[dict[str, Any]] = []
    for result in results:
        job = lookup[result["job_id"]]
        job_rows.append(
            {
                "job_id": result["job_id"],
                "component_id": job["component_id"],
                "family": job["family"],
                "tranche": job["tranche"],
                "seed": job["seed"],
                "outer_coordinate": job["outer_coordinate"],
                "status": result["status"],
                "job_passed": result["job_passed"],
                "error": result.get("error", ""),
                "elapsed_seconds": result["elapsed_seconds"],
                "geometric_root_count": result[
                    "geometric_root_count"
                ],
                "active_root_count": result["active_root_count"],
                "inactive_root_count": result["inactive_root_count"],
                "maximum_coordinate_branch_projective_step": result.get(
                    "maximum_coordinate_branch_projective_step", ""
                ),
                "topology_stable": result.get(
                    "topology_stable", False
                ),
                "owner_passed": result.get("owner_passed", False),
                "fit_complete": result.get("fit_complete", False),
                "quadrature_passed": result.get(
                    "quadrature_passed", False
                ),
                "low_order_raw_relative_error": result[
                    "quadrature"
                ].get("low_order_raw_relative_error", ""),
                "low_order_subtracted_relative_error": result[
                    "quadrature"
                ].get("low_order_subtracted_relative_error", ""),
                "mid_order_subtracted_relative_error": result[
                    "quadrature"
                ].get("mid_order_subtracted_relative_error", ""),
                "low_order_improvement_factor": result[
                    "quadrature"
                ].get("low_order_improvement_factor", ""),
                "job_input_hash": result["job_input_hash"],
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
        if result["owner"]:
            owner_rows.append(result["owner"])
        scan_rows.extend(result["scan_rows"])
        poles.extend(result["poles"])
        topology.extend(result["topology_rows"])
        fits.extend(result["fits"])
        quadrature.extend(result["quadrature_rows"])
    return (
        job_rows,
        owner_rows,
        scan_rows,
        poles,
        topology,
        fits,
        quadrature,
    )


def pool_rows(
    quadrature_rows: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    return M5237.pooled_convergence(quadrature_rows)


def validation_rows(
    manifest: dict[str, Any],
    dry_run: dict[str, Any],
    results: list[dict[str, Any]],
    job_rows: list[dict[str, Any]],
    owner_rows: list[dict[str, Any]],
    scan_rows: list[dict[str, Any]],
    poles: list[dict[str, Any]],
    topology_rows: list[dict[str, Any]],
    fits: list[dict[str, Any]],
    quadrature_rows: list[dict[str, Any]],
    endpoint_pool: dict[str, Any],
    combined_pool: dict[str, Any],
) -> list[dict[str, Any]]:
    direct_validation = read_csv(VALIDATION_5237)
    jobs_by_id = {
        job["job_id"]: job for job in manifest["jobs"]
    }
    unbracketed: list[dict[str, Any]] = []
    for row in scan_rows:
        job = jobs_by_id[row["job_id"]]
        step = (
            float(job["scan_maximum"]) - float(job["scan_minimum"])
        ) / (int(job["scan_points"]) - 1)
        ratio = float(row["minimum_channel_magnitude"]) / max(
            float(row["median_channel_magnitude"]), 1.0e-300
        )
        coordinate = float(row["minimum_channel_coordinate"])
        interior = (
            coordinate > float(job["scan_minimum"]) + 1.5 * step
            and coordinate < float(job["scan_maximum"]) - 1.5 * step
        )
        if (
            int(row["sign_change_count"]) == 0
            and interior
            and ratio < 4.0e-3
        ):
            unbracketed.append(row)
    sign_changes = sum(
        int(row["sign_change_count"]) for row in scan_rows
    )
    represented_surfaces = sum(
        int(row["surface_count"]) for row in poles
    )
    active_ids = {
        (row["job_id"], row["pole_id"])
        for row in poles
        if bool(row["causal_family_active"])
    }
    inactive_ids = {
        (row["job_id"], row["pole_id"])
        for row in poles
        if not bool(row["causal_family_active"])
    }
    fitted_ids = {
        (row["job_id"], row["pole_id"]) for row in fits
    }
    claims_false = all(
        not bool(row[key])
        for collection in (
            manifest["jobs"],
            results,
            job_rows,
            owner_rows,
            scan_rows,
            poles,
            topology_rows,
            fits,
            quadrature_rows,
        )
        for row in collection
        for key in (
            "valid_for_numeric_UV_claim",
            "valid_for_local_GR_claim",
            "valid_for_full_MTS_claim",
        )
    )
    formal_digest = tree_digest(FORMAL)
    checks = [
        (
            "direct_parent_validation_passes",
            bool(direct_validation)
            and all(row["passed"] == "True" for row in direct_validation),
            f"{len(direct_validation)} direct checks",
        ),
        (
            "dry_run_authorized_exact_manifest",
            bool(dry_run["authorized_to_execute"])
            and dry_run["manifest_sha256"] == digest(MANIFEST_JSON),
            dry_run["manifest_sha256"],
        ),
        (
            "bounded_endpoint_manifest_complete",
            len(manifest["jobs"]) == EXPECTED_JOB_COUNT
            and len(manifest["jobs"]) <= MAXIMUM_JOB_COUNT,
            f"{len(manifest['jobs'])} jobs",
        ),
        (
            "all_endpoint_jobs_completed_and_passed",
            len(results) == EXPECTED_JOB_COUNT
            and all(
                row["status"] == "COMPLETED"
                and bool(row["job_passed"])
                for row in results
            ),
            (
                f"{sum(row['status'] == 'COMPLETED' for row in results)}"
                f"/{len(results)} completed"
            ),
        ),
        (
            "endpoint_owner_identity_closes",
            len(owner_rows) == EXPECTED_JOB_COUNT
            and all(
                float(row["endpoint_owner_fraction"])
                >= MINIMUM_ENDPOINT_OWNER_FRACTION
                and float(
                    row["split_to_full_relative_closure_residual"]
                )
                <= OWNER_CLOSURE_LIMIT
                for row in owner_rows
            ),
            (
                f"min owner fraction="
                f"{min(float(row['endpoint_owner_fraction']) for row in owner_rows)}; "
                f"max closure="
                f"{max(float(row['split_to_full_relative_closure_residual']) for row in owner_rows)}"
            ),
        ),
        (
            "endpoint_root_scan_exhaustive",
            sign_changes == represented_surfaces and not unbracketed,
            (
                f"{sign_changes} sign changes; "
                f"{represented_surfaces} represented; "
                f"{len(unbracketed)} unbracketed"
            ),
        ),
        (
            "endpoint_root_caps_respected",
            len(poles) <= MAXIMUM_TOTAL_ROOTS
            and all(
                int(row["geometric_root_count"])
                <= MAXIMUM_ROOTS_PER_JOB
                and int(row["active_root_count"])
                <= MAXIMUM_ACTIVE_ROOTS_PER_JOB
                for row in results
            ),
            f"{len(poles)} geometric roots",
        ),
        (
            "endpoint_causal_gate_complete",
            active_ids == fitted_ids
            and inactive_ids.isdisjoint(fitted_ids)
            and all(
                float(row["maximum_pair_projective_step"])
                < M5237.PROJECTIVE_LIMIT
                and float(
                    row["maximum_reciprocal_product_residual"]
                )
                < M5237.RECIPROCAL_LIMIT
                for row in poles
            ),
            f"{len(active_ids)} active; {len(inactive_ids)} inactive",
        ),
        (
            "endpoint_residue_fits_pass",
            bool(fits) and all(bool(row["fit_passed"]) for row in fits),
            f"{sum(bool(row['fit_passed']) for row in fits)}/{len(fits)}",
        ),
        (
            "endpoint_union_quadrature_passes",
            bool(quadrature_rows)
            and all(bool(row["quadrature_passed"]) for row in job_rows),
            f"{len(quadrature_rows)} patch-order rows",
        ),
        (
            "endpoint_pool_converges",
            float(endpoint_pool["low_order_subtracted_relative_error"])
            <= M5237.LOW_ORDER_SUBTRACTED_RELATIVE_ERROR_LIMIT
            and float(
                endpoint_pool["mid_order_subtracted_relative_error"]
            )
            <= M5237.MID_ORDER_SUBTRACTED_RELATIVE_ERROR_LIMIT,
            (
                f"low="
                f"{endpoint_pool['low_order_subtracted_relative_error']}; "
                f"mid="
                f"{endpoint_pool['mid_order_subtracted_relative_error']}"
            ),
        ),
        (
            "combined_direct_endpoint_pool_converges",
            float(combined_pool["low_order_subtracted_relative_error"])
            <= M5237.LOW_ORDER_SUBTRACTED_RELATIVE_ERROR_LIMIT
            and float(
                combined_pool["mid_order_subtracted_relative_error"]
            )
            <= M5237.MID_ORDER_SUBTRACTED_RELATIVE_ERROR_LIMIT,
            (
                f"low="
                f"{combined_pool['low_order_subtracted_relative_error']}; "
                f"mid="
                f"{combined_pool['mid_order_subtracted_relative_error']}"
            ),
        ),
        (
            "claim_boundary_preserved",
            claims_false,
            "all claim flags false",
        ),
        (
            "formalization_workbench_unchanged",
            formal_digest == FORMAL_BASELINE,
            formal_digest,
        ),
    ]
    return [
        {
            "check": name,
            "passed": passed,
            "detail": detail,
            "checkpoint_marker": MARKER,
        }
        for name, passed, detail in checks
    ]


def render_document(
    result: dict[str, Any],
    owner_rows: list[dict[str, Any]],
    job_rows: list[dict[str, Any]],
) -> str:
    failures = [
        row for row in job_rows if not bool(row["job_passed"])
    ]
    failure_text = (
        "\n".join(
            f"- `{row['job_id']}` `{row['family']}`: "
            f"`{row['error'] or 'numerical gate failed'}`."
            for row in failures
        )
        if failures
        else "- None."
    )
    endpoint = result["endpoint_pool"]
    combined = result["combined_pool"]
    return f"""# 5238 - Endpoint-owned residue and combined bounded A00 runner

## Decision

`{result['decision']}`.

The endpoint contribution is now isolated from the parent finite-plus
integrand rather than inferred from an ownership label.  At a local
collision its coefficient is

```text
C_endpoint = lim_(delta->0)
             [-endpoint_value / soft_energy] delta^2,

R_endpoint = (Delta w) sigma C_endpoint
             / (r_* z_* J_collision).
```

The symbols are the same reciprocal winding difference, chamber orientation,
relative root, global root and collision Jacobian already fixed by the direct
residue theorem.  No new closure coefficient is introduced.

## Ownership identity

- Audited endpoint component-coordinate jobs:
  `{len(owner_rows)}`.
- Minimum endpoint coefficient fraction:
  `{min(float(row['endpoint_owner_fraction']) for row in owner_rows):.12g}`.
- Maximum split-to-full closure residual:
  `{max(float(row['split_to_full_relative_closure_residual']) for row in owner_rows):.12g}`.

Thus the isolated direct and endpoint coefficients reconstruct the original
finite-plus family residue before any outer-pole fit.

## Bounded endpoint run

- Families: `{result['family_count']}`.
- Family/tranche strata: `{result['stratum_count']}`.
- Reciprocal components: `{result['component_count']}`.
- Component-coordinate jobs: `{result['job_count']}`.
- Passed jobs: `{result['passed_job_count']}/{result['job_count']}`.
- Geometric/active/inactive roots:
  `{result['total_geometric_root_count']}/`
  `{result['total_active_root_count']}/`
  `{result['total_inactive_root_count']}`.

Relative to the endpoint order-{endpoint['reference_order']} subtracted
reference, order-32 subtraction changes the error from
`{endpoint['low_order_raw_relative_error']:.12g}` to
`{endpoint['low_order_subtracted_relative_error']:.12g}`.

## Combined method pool

The cached direct and endpoint patch unions were combined order by order.
This is a method-convergence pool, not yet the physical multidimensional
A00 coefficient.

- Raw order-32 error:
  `{combined['low_order_raw_relative_error']:.12g}`.
- Subtracted order-32 error:
  `{combined['low_order_subtracted_relative_error']:.12g}`.
- Subtracted order-128 error:
  `{combined['mid_order_subtracted_relative_error']:.12g}`.
- Order-32 improvement:
  `{combined['low_order_improvement_factor']:.12g}x`.

## Failed jobs

{failure_text}

## Scope

The complete active direct and endpoint residue families now have a common
branch-aware causal subtraction method.  This does not yet supply the
remaining regular-domain integration or regulator extrapolation needed for a
physical A00 coefficient, and it makes no UV, local-GR or full-MTS claim.

## Next target

Construct one matched event-level A00 integral that combines all active
component patches with the regular complement, then perform the E040/E020
regulator extrapolation before scaling to the 48-event source pool.
"""


def execute() -> dict[str, Any]:
    dry_run = read_json(DRY_RUN)
    if not bool(dry_run.get("authorized_to_execute")):
        raise RuntimeError("endpoint dry run did not authorize execution")
    manifest = read_json(MANIFEST_JSON)
    if dry_run["manifest_sha256"] != digest(MANIFEST_JSON):
        raise RuntimeError("endpoint manifest changed after dry run")
    started = time.monotonic()
    results, cache_hits = execute_jobs(manifest)
    (
        job_rows,
        owner_rows,
        scan_rows,
        poles,
        topology_rows,
        fits,
        quadrature_rows,
    ) = flatten_results(manifest["jobs"], results)
    if len(poles) > MAXIMUM_TOTAL_ROOTS:
        raise RuntimeError("endpoint aggregate root cap exceeded")
    endpoint_pool_rows, endpoint_pool = pool_rows(quadrature_rows)
    direct_quadrature = read_csv(QUADRATURE_5237)
    combined_input = [
        {
            **row,
            "quadrature_order": int(row["quadrature_order"]),
        }
        for row in direct_quadrature
    ] + quadrature_rows
    combined_pool_rows, combined_pool = pool_rows(combined_input)
    validation = validation_rows(
        manifest,
        dry_run,
        results,
        job_rows,
        owner_rows,
        scan_rows,
        poles,
        topology_rows,
        fits,
        quadrature_rows,
        endpoint_pool,
        combined_pool,
    )
    all_passed = all(bool(row["passed"]) for row in validation)
    decision = (
        "ADOPT_ENDPOINT_OWNED_RESIDUE_AND_COMBINED_BOUNDED_A00_METHOD"
        if all_passed
        else "RETAIN_ENDPOINT_DERIVATION_AND_REPAIR_FAILED_GATES"
    )
    result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "decision": decision,
        "scope": (
            "isolated endpoint-owned residues plus combined direct/endpoint "
            "conditional method pool; not the full A00 coefficient"
        ),
        "job_count": len(manifest["jobs"]),
        "component_count": len(
            {job["component_id"] for job in manifest["jobs"]}
        ),
        "family_count": len(
            {job["family"] for job in manifest["jobs"]}
        ),
        "stratum_count": len(
            {
                (job["family"], job["tranche"])
                for job in manifest["jobs"]
            }
        ),
        "unique_event_count": len(
            {
                (job["tranche"], job["seed"])
                for job in manifest["jobs"]
            }
        ),
        "cache_hit_count": cache_hits,
        "elapsed_seconds": time.monotonic() - started,
        "passed_job_count": sum(
            bool(row["job_passed"]) for row in job_rows
        ),
        "total_geometric_root_count": len(poles),
        "total_active_root_count": sum(
            bool(row["causal_family_active"]) for row in poles
        ),
        "total_inactive_root_count": sum(
            not bool(row["causal_family_active"]) for row in poles
        ),
        "minimum_endpoint_owner_fraction": min(
            float(row["endpoint_owner_fraction"]) for row in owner_rows
        ),
        "maximum_owner_closure_residual": max(
            float(row["split_to_full_relative_closure_residual"])
            for row in owner_rows
        ),
        "endpoint_pool": endpoint_pool,
        "combined_pool": combined_pool,
        "validation_all_passed": all_passed,
        "next_target": (
            "construct one matched event-level A00 integral with regular "
            "complement and E040/E020 regulator extrapolation"
        ),
        "source_paths": manifest["source_paths"],
        "claim_boundary": {
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
        },
    }
    write_csv(JOB_ROWS, job_rows)
    write_csv(OWNER_ROWS, owner_rows)
    write_csv(SCAN_ROWS, scan_rows)
    write_csv(POLE_ROWS, poles)
    write_csv(TOPOLOGY_ROWS, topology_rows)
    write_csv(RESIDUE_ROWS, fits)
    write_csv(QUADRATURE_ROWS, quadrature_rows)
    write_csv(ENDPOINT_POOL_ROWS, endpoint_pool_rows)
    write_csv(COMBINED_POOL_ROWS, combined_pool_rows)
    write_csv(VALIDATION, validation)
    atomic_json(RESULT, result)
    atomic_text(
        DOCUMENT, render_document(result, owner_rows, job_rows)
    )
    print(json.dumps(result, indent=2, sort_keys=True))
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode", choices=("dry-run", "execute"), required=True
    )
    arguments = parser.parse_args()
    if arguments.mode == "dry-run":
        report = write_manifest_and_dry_run()
        print(json.dumps(report, indent=2, sort_keys=True))
        if not bool(report["authorized_to_execute"]):
            raise SystemExit(1)
        return
    execute()


if __name__ == "__main__":
    main()
