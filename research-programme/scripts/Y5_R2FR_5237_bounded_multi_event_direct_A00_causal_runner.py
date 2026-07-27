from __future__ import annotations

import argparse
import copy
import csv
import hashlib
import importlib.util
import json
import math
import os
import re
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE = POST / "source-intake" / "functional_rg" / "5237"
RESIDUALS = POST / "source-intake" / "mts_residuals"
CACHE = SOURCE / "job-cache"

SCRIPT_5234 = (
    POST
    / "scripts"
    / "Y5_R2FR_5234_complete_active_family_physical_channel_and_pole_order_atlas.py"
)
SCRIPT_5235 = (
    POST
    / "scripts"
    / "Y5_R2FR_5235_dynamic_all_channel_conditional_A00_slice_pilot.py"
)
RESULT_5234 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5234"
    / "complete_active_family_physical_channel_and_pole_order_atlas.json"
)
ATLAS_5234 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5234"
    / "complete_active_family_pole_atlas.csv"
)
FAMILY_SOURCE = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5231"
    / "pooled_A00_tail_family_decomposition.csv"
)

MANIFEST_JSON = SOURCE / "bounded_multi_event_job_manifest.json"
MANIFEST_CSV = SOURCE / "bounded_multi_event_job_manifest.csv"
DRY_RUN = SOURCE / "bounded_multi_event_dry_run_report.json"
RESULT = SOURCE / "bounded_multi_event_direct_A00_causal_run.json"
JOB_ROWS = SOURCE / "bounded_multi_event_job_summary.csv"
SCAN_ROWS = SOURCE / "bounded_multi_event_surface_scan_audit.csv"
POLE_ROWS = SOURCE / "bounded_multi_event_pole_catalog.csv"
TOPOLOGY_ROWS = SOURCE / "bounded_multi_event_causal_topology_audit.csv"
RESIDUE_ROWS = SOURCE / "bounded_multi_event_residue_fit_summary.csv"
QUADRATURE_ROWS = SOURCE / "bounded_multi_event_patch_quadrature.csv"
POOL_ROWS = SOURCE / "bounded_multi_event_pool_convergence.csv"
DOCUMENT = (
    POST
    / "5237-Y5-R2FR-bounded-multi-event-direct-A00-causal-runner.md"
)
VALIDATION = RESIDUALS / "P8_Y5_BRR545_5237_VALIDATION.csv"

MARKER = "MTS_5237_BOUNDED_MULTI_EVENT_DIRECT_A00_CAUSAL_RUNNER"
REVISION = "bounded-multi-event-direct-A00-causal-runner-v1"
FORMAL_BASELINE = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)
EPSILON_ID = "E020"
ACTIVE_FAMILY_FLOOR = 1.0e-10
EXPECTED_FAMILY_COUNT = 6
EXPECTED_STRATUM_COUNT = 12
EXPECTED_COMPONENT_COUNT = 16
EXPECTED_JOB_COUNT = 48
MAXIMUM_JOB_COUNT = 48
SCAN_POINTS = 601
TOPOLOGY_STEPS = 12288
MAXIMUM_TOPOLOGY_STEPS = 24576
PROJECTIVE_LIMIT = 0.1
RECIPROCAL_LIMIT = 2.0e-3
POLE_IMAGINARY_LIMIT = 0.02
ROOT_GROUP_TOLERANCE = 7.5e-5
MAXIMUM_ROOTS_PER_JOB = 10
MAXIMUM_TOTAL_ROOTS = 360
MAXIMUM_ACTIVE_ROOTS_PER_JOB = 8
PATCH_HALF_WIDTH = 1.0e-2
QUADRATURE_ORDERS = (32, 128, 512)
SLOPE_TOLERANCE = 0.12
NUMERATOR_FIT_RELATIVE_RESIDUAL_LIMIT = 5.0e-4
LOW_ORDER_SUBTRACTED_RELATIVE_ERROR_LIMIT = 5.0e-3
MID_ORDER_SUBTRACTED_RELATIVE_ERROR_LIMIT = 1.0e-3
MAXIMUM_RUN_SECONDS = 4.0 * 60.0 * 60.0

OUTER_COORDINATES = (
    "soft_energy",
    "soft_cosine",
    "decay_cosine",
)


def load_module(path: Path, name: str) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5235 = load_module(SCRIPT_5235, "mts_5235_for_5237")
M5234 = M5235.M5234
M5232 = M5235.M5232
M5231 = M5235.M5231
M5024 = M5235.M5024
M5017 = M5235.M5017
M5030 = M5232.M5030
M5034 = M5232.M5034


def json_default(value: Any) -> Any:
    if isinstance(value, np.generic):
        return value.item()
    raise TypeError(
        f"Object of type {type(value).__name__} is not JSON serializable"
    )


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


def atomic_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(value, encoding="utf-8")
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
    with temporary.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    os.replace(temporary, path)


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def tree_digest(path: Path) -> str:
    value = hashlib.sha256()
    for candidate in sorted(item for item in path.rglob("*") if item.is_file()):
        value.update(candidate.relative_to(path).as_posix().encode("utf-8"))
        value.update(digest(candidate).encode("ascii"))
    return value.hexdigest()


def complex_value(value: Any) -> complex:
    return M5231.complex_value(value)


def complex_row(value: complex) -> dict[str, float]:
    return {"real": float(value.real), "imaginary": float(value.imag)}


def serialized_hash(value: Any) -> str:
    payload = json.dumps(
        value, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def scan_domain(coordinate: str) -> tuple[float, float]:
    if coordinate == "soft_energy":
        return 0.005, 0.995
    if coordinate in {"soft_cosine", "decay_cosine"}:
        return -0.995, 0.995
    raise RuntimeError(f"unsupported outer coordinate: {coordinate}")


def direct_candidate_rows(
    representative_pair: tuple[str, str],
) -> list[dict[str, str]]:
    rows = [
        row
        for row in read_csv(ATLAS_5234)
        if row["owner_summand"] == "direct_five_point"
        and row["atlas_status"]
        != "KINEMATICALLY_FIXED_NONZERO"
    ]
    consumed = {
        M5234.direct_label_surface(label)[0]
        for label in representative_pair
    }
    by_surface: dict[str, dict[str, str]] = {}
    for row in rows:
        if row["surface_id"] in consumed:
            continue
        by_surface.setdefault(row["surface_id"], row)
    result = list(by_surface.values())
    result.sort(key=lambda row: row["surface_id"])
    if len(result) != 13:
        raise RuntimeError(
            f"expected 13 direct candidate surfaces, found {len(result)}"
        )
    return result


def selected_family_strata() -> list[dict[str, str]]:
    selected: dict[tuple[str, str], dict[str, str]] = {}
    for row in read_csv(FAMILY_SOURCE):
        family = row["family"]
        magnitude = float(row["A00_family_magnitude"])
        if magnitude <= ACTIVE_FAMILY_FLOOR:
            continue
        if any(
            not label.startswith("direct:")
            for label in family.split("/")
        ):
            continue
        key = family, row["tranche"]
        if key not in selected or magnitude > float(
            selected[key]["A00_family_magnitude"]
        ):
            selected[key] = row
    rows = [selected[key] for key in sorted(selected)]
    if len({row["family"] for row in rows}) != EXPECTED_FAMILY_COUNT:
        raise RuntimeError("direct family count changed")
    if len(rows) != EXPECTED_STRATUM_COUNT:
        raise RuntimeError("family/tranche stratum count changed")
    return rows


def normalized_component(
    first: dict[str, Any],
    second: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any]]:
    first_root = complex_value(first["target_root"])
    second_root = complex_value(second["target_root"])
    if abs(first_root) > abs(second_root):
        return first, second
    if abs(second_root) > abs(first_root):
        return second, first
    first_key = (
        int(first["chamber_index"]),
        first_root.real,
        first_root.imag,
    )
    second_key = (
        int(second["chamber_index"]),
        second_root.real,
        second_root.imag,
    )
    return (first, second) if first_key <= second_key else (second, first)


def suffix_and_winding(entry: dict[str, Any]) -> tuple[str, int]:
    labels = list(entry["representing_pairs"][0])
    suffixes = {label.rsplit("_", 1)[-1] for label in labels}
    if len(suffixes) != 1:
        raise RuntimeError(f"mixed reciprocal suffixes: {labels}")
    return suffixes.pop(), int(entry["winding_correction"])


def build_manifest() -> dict[str, Any]:
    contracts = {
        contract["tranche"]: contract
        for contract in M5231.source_contracts()
    }
    jobs: list[dict[str, Any]] = []
    for stratum_index, row in enumerate(selected_family_strata(), start=1):
        family = row["family"]
        tranche = row["tranche"]
        seed = int(row["seed"])
        contract = contracts[tranche]
        topology_path = M5231.topology_path(
            contract, seed, EPSILON_ID
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
            (*normalized_component(first, second), residual)
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
                suffix_and_winding(representative)
            )
            reciprocal_suffix, reciprocal_winding = suffix_and_winding(
                reciprocal
            )
            expected = {
                representative_suffix: representative_winding,
                reciprocal_suffix: reciprocal_winding,
            }
            if set(expected) != {"u", "v"}:
                raise RuntimeError(
                    f"incomplete reciprocal winding map for {family}"
                )
            for coordinate in OUTER_COORDINATES:
                lower, upper = scan_domain(coordinate)
                job_number = len(jobs) + 1
                job = {
                    "job_id": f"BME{job_number:02d}",
                    "component_id": (
                        f"S{stratum_index:02d}_C{component_index:02d}"
                    ),
                    "stratum_id": f"S{stratum_index:02d}",
                    "component_index": component_index,
                    "family": family,
                    "tranche": tranche,
                    "seed": seed,
                    "epsilon_id": EPSILON_ID,
                    "source_A00_family_magnitude": float(
                        row["A00_family_magnitude"]
                    ),
                    "outer_coordinate": coordinate,
                    "scan_minimum": lower,
                    "scan_maximum": upper,
                    "scan_points": SCAN_POINTS,
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
                    "candidate_surface_count": 13,
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
                job["job_input_hash"] = serialized_hash(
                    {
                        "revision": REVISION,
                        "job": job,
                        "runner_script": digest(Path(__file__).resolve()),
                        "script_5234": digest(SCRIPT_5234),
                        "script_5235": digest(SCRIPT_5235),
                        "atlas": digest(ATLAS_5234),
                        "topology": digest(topology_path),
                    }
                )
                jobs.append(job)
    if len(jobs) != EXPECTED_JOB_COUNT:
        raise RuntimeError(
            f"expected {EXPECTED_JOB_COUNT} jobs, found {len(jobs)}"
        )
    manifest = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "scope": (
            "maximum-magnitude event in each direct-family/tranche "
            "stratum, every reciprocal component and all three "
            "conditional outer coordinates"
        ),
        "bounds": {
            "maximum_job_count": MAXIMUM_JOB_COUNT,
            "maximum_run_seconds": MAXIMUM_RUN_SECONDS,
            "scan_points_per_job": SCAN_POINTS,
            "maximum_roots_per_job": MAXIMUM_ROOTS_PER_JOB,
            "maximum_total_roots": MAXIMUM_TOTAL_ROOTS,
            "maximum_active_roots_per_job": (
                MAXIMUM_ACTIVE_ROOTS_PER_JOB
            ),
            "quadrature_orders": list(QUADRATURE_ORDERS),
        },
        "source_paths": [
            str(SCRIPT_5234),
            str(SCRIPT_5235),
            str(RESULT_5234),
            str(ATLAS_5234),
            str(FAMILY_SOURCE),
        ],
        "jobs": jobs,
        "claim_boundary": {
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
        },
    }
    return manifest


def manifest_csv_rows(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for job in manifest["jobs"]:
        rows.append(
            {
                **{
                    key: value
                    for key, value in job.items()
                    if key
                    not in {
                        "representative_pair",
                        "reciprocal_pair",
                        "representative_anchor",
                        "reciprocal_anchor",
                    }
                },
                "representative_pair": "|".join(
                    job["representative_pair"]
                ),
                "reciprocal_pair": "|".join(job["reciprocal_pair"]),
                "representative_anchor_real": job[
                    "representative_anchor"
                ]["real"],
                "representative_anchor_imaginary": job[
                    "representative_anchor"
                ]["imaginary"],
                "reciprocal_anchor_real": job["reciprocal_anchor"][
                    "real"
                ],
                "reciprocal_anchor_imaginary": job[
                    "reciprocal_anchor"
                ]["imaginary"],
            }
        )
    return rows


def write_manifest_and_dry_run() -> dict[str, Any]:
    manifest = build_manifest()
    atomic_json(MANIFEST_JSON, manifest)
    write_csv(MANIFEST_CSV, manifest_csv_rows(manifest))
    jobs = manifest["jobs"]
    source_paths = [
        Path(path)
        for path in manifest["source_paths"]
    ] + [
        Path(job["source_topology"]) for job in jobs
    ] + [
        Path(job["source_config"]) for job in jobs
    ]
    checks = {
        "all_source_paths_exist": all(path.exists() for path in source_paths),
        "job_count_within_bound": (
            len(jobs) == EXPECTED_JOB_COUNT
            and len(jobs) <= MAXIMUM_JOB_COUNT
        ),
        "job_ids_unique": len({job["job_id"] for job in jobs}) == len(jobs),
        "component_coordinate_cross_product_complete": (
            len({job["component_id"] for job in jobs})
            == EXPECTED_COMPONENT_COUNT
            and all(
                {
                    job["outer_coordinate"]
                    for job in jobs
                    if job["component_id"] == component_id
                }
                == set(OUTER_COORDINATES)
                for component_id in {
                    job["component_id"] for job in jobs
                }
            )
        ),
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
        "coordinate_coverage_complete": (
            {job["outer_coordinate"] for job in jobs}
            == {"soft_energy", "soft_cosine", "decay_cosine"}
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
        "candidate_surface_contract_complete": all(
            int(job["candidate_surface_count"]) == 13
            for job in jobs
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
        "reciprocal_component_count": len(
            {job["component_id"] for job in jobs}
        ),
        "unique_event_count": len(
            {(job["tranche"], job["seed"]) for job in jobs}
        ),
        "estimated_surface_evaluations": (
            len(jobs) * 13 * SCAN_POINTS
        ),
        "checks": checks,
        "authorized_to_execute": all(checks.values()),
        "claim_boundary": manifest["claim_boundary"],
    }
    atomic_json(DRY_RUN, report)
    return report


def pair_key(pair: list[str] | tuple[str, str]) -> str:
    return "|".join(pair)


def event_from_job(job: dict[str, Any]) -> dict[str, Any]:
    return {
        "seed": int(job["seed"]),
        "soft_energy": float(job["soft_energy"]),
        "soft_cosine": float(job["soft_cosine"]),
        "decay_cosine": float(job["decay_cosine"]),
    }


def find_source_crossing(
    topology: dict[str, Any],
    chamber_index: int,
    pair: tuple[str, str],
    anchor: complex,
) -> dict[str, Any]:
    candidates = [
        crossing
        for crossing in topology["chambers"][chamber_index][
            "surface_crossings"
        ]
        if tuple(crossing["representing_pairs"][0]) == pair
    ]
    if not candidates:
        raise RuntimeError(
            f"source crossing absent in chamber {chamber_index}: {pair}"
        )
    return min(
        candidates,
        key=lambda crossing: M5030.chordal_distance(
            complex_value(crossing["target_root"]), anchor
        ),
    )


def roots_for_pair(
    event: dict[str, Any],
    target: complex,
    pair: tuple[str, str],
    coordinate_name: str,
    coordinate: complex,
) -> list[complex]:
    varied = dict(event)
    varied[coordinate_name] = coordinate
    rationals = M5232.M5029.root_rationals(
        varied["soft_energy"],
        varied["soft_cosine"],
        varied["decay_cosine"],
        target,
    )
    return M5232.M5029.collision_roots(
        rationals[pair[0]], rationals[pair[1]]
    )


def build_coordinate_branch_track(
    event: dict[str, Any],
    target: complex,
    pair: tuple[str, str],
    anchor: complex,
    coordinate_name: str,
    coordinates: np.ndarray,
) -> dict[str, Any]:
    base_coordinate = float(event[coordinate_name])
    anchor_index = int(np.argmin(np.abs(coordinates - base_coordinate)))
    paths = [
        roots_for_pair(
            event,
            target,
            pair,
            coordinate_name,
            complex(float(coordinate)),
        )
        for coordinate in coordinates
    ]
    if any(not roots for roots in paths):
        raise RuntimeError(f"collision branch disappeared for {pair}")
    selected: list[complex | None] = [None] * len(paths)
    selected[anchor_index] = min(
        paths[anchor_index],
        key=lambda root: M5030.chordal_distance(root, anchor),
    )
    previous = complex(selected[anchor_index])
    for index in range(anchor_index + 1, len(paths)):
        root = min(
            paths[index],
            key=lambda candidate: M5030.chordal_distance(
                candidate, previous
            ),
        )
        selected[index] = root
        previous = root
    previous = complex(selected[anchor_index])
    for index in range(anchor_index - 1, -1, -1):
        root = min(
            paths[index],
            key=lambda candidate: M5030.chordal_distance(
                candidate, previous
            ),
        )
        selected[index] = root
        previous = root
    roots = [complex(root) for root in selected if root is not None]
    maximum_step = max(
        (
            M5030.chordal_distance(roots[index - 1], roots[index])
            for index in range(1, len(roots))
        ),
        default=0.0,
    )
    branch_margins = [
        min(
            (
                M5030.chordal_distance(selected_root, candidate)
                for candidate in candidates
                if M5030.chordal_distance(
                    selected_root, candidate
                )
                > 1.0e-12
            ),
            default=1.0,
        )
        for selected_root, candidates in zip(roots, paths)
    ]
    return {
        "coordinates": coordinates,
        "roots": roots,
        "maximum_projective_step": maximum_step,
        "minimum_alternate_branch_separation": min(branch_margins),
    }


def track_anchor(track: dict[str, Any], coordinate: complex) -> complex:
    coordinates = track["coordinates"]
    index = int(np.argmin(np.abs(coordinates - coordinate.real)))
    return complex(track["roots"][index])


def selected_component_roots(
    problem: dict[str, Any], coordinate: complex
) -> tuple[complex, complex]:
    representative_pair = problem["case"]["representative_pair"]
    reciprocal_pair = problem["case"]["reciprocal_pair"]
    representative_roots = roots_for_pair(
        problem["event"],
        problem["target"],
        representative_pair,
        problem["case"]["outer_coordinate"],
        coordinate,
    )
    reciprocal_roots = roots_for_pair(
        problem["event"],
        problem["target"],
        reciprocal_pair,
        problem["case"]["outer_coordinate"],
        coordinate,
    )
    if not representative_roots or not reciprocal_roots:
        raise RuntimeError("component collision root disappeared")
    representative_anchor = track_anchor(
        problem["branch_tracks"][pair_key(representative_pair)],
        coordinate,
    )
    reciprocal_anchor = track_anchor(
        problem["branch_tracks"][pair_key(reciprocal_pair)],
        coordinate,
    )
    candidates = [
        {
            "representative": representative,
            "reciprocal": reciprocal,
            "reciprocal_residual": abs(
                representative * reciprocal - 1.0
            ),
            "continuity_distance": (
                M5030.chordal_distance(
                    representative, representative_anchor
                )
                + M5030.chordal_distance(
                    reciprocal, reciprocal_anchor
                )
            ),
        }
        for representative in representative_roots
        for reciprocal in reciprocal_roots
    ]
    minimum_residual = min(
        row["reciprocal_residual"] for row in candidates
    )
    eligible = [
        row
        for row in candidates
        if row["reciprocal_residual"]
        <= max(2.0e-8, 100.0 * minimum_residual)
    ]
    selected = min(
        eligible,
        key=lambda row: (
            row["continuity_distance"],
            row["reciprocal_residual"],
        ),
    )
    return (
        complex(selected["representative"]),
        complex(selected["reciprocal"]),
    )


def selected_root(
    problem: dict[str, Any],
    pair: tuple[str, str],
    coordinate: complex,
) -> complex:
    representative, reciprocal = selected_component_roots(
        problem, coordinate
    )
    if pair == problem["case"]["representative_pair"]:
        return representative
    if pair == problem["case"]["reciprocal_pair"]:
        return reciprocal
    raise RuntimeError(f"pair does not belong to component: {pair}")


def build_problem(job: dict[str, Any]) -> dict[str, Any]:
    topology = read_json(Path(job["source_topology"]))
    target = complex_value(topology["target_cosine"])
    event = event_from_job(job)
    representative_pair = tuple(job["representative_pair"])
    reciprocal_pair = tuple(job["reciprocal_pair"])
    representative_anchor = complex_value(job["representative_anchor"])
    reciprocal_anchor = complex_value(job["reciprocal_anchor"])
    representative = find_source_crossing(
        topology,
        int(job["representative_chamber"]),
        representative_pair,
        representative_anchor,
    )
    reciprocal = find_source_crossing(
        topology,
        int(job["reciprocal_chamber"]),
        reciprocal_pair,
        reciprocal_anchor,
    )
    coordinates = np.linspace(
        float(job["scan_minimum"]),
        float(job["scan_maximum"]),
        int(job["scan_points"]),
    )
    branch_tracks = {
        pair_key(representative_pair): build_coordinate_branch_track(
            event,
            target,
            representative_pair,
            representative_anchor,
            job["outer_coordinate"],
            coordinates,
        ),
        pair_key(reciprocal_pair): build_coordinate_branch_track(
            event,
            target,
            reciprocal_pair,
            reciprocal_anchor,
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
        "component_id": job["component_id"],
        "case": case,
        "event": event,
        "topology": topology,
        "target": target,
        "representative": representative,
        "reciprocal": reciprocal,
        "atlas_rows": direct_candidate_rows(representative_pair),
        "coordinates": coordinates,
        "branch_tracks": branch_tracks,
    }


def collision_geometry(
    problem: dict[str, Any], coordinate: complex
) -> dict[str, Any]:
    case = problem["case"]
    event = problem["event"]
    varied = dict(event)
    varied[case["outer_coordinate"]] = coordinate
    relative_root = selected_root(
        problem, case["representative_pair"], coordinate
    )
    rationals = M5232.M5029.root_rationals(
        varied["soft_energy"],
        varied["soft_cosine"],
        varied["decay_cosine"],
        problem["target"],
    )
    values = [
        M5231.rational_value_and_derivative(
            rationals[label], relative_root
        )[0]
        for label in case["representative_pair"]
    ]
    global_root = complex(sum(values) / len(values))
    _, _, internal = M5232.M5028.event_geometry(
        varied["soft_energy"],
        varied["soft_cosine"],
        varied["decay_cosine"],
        relative_root,
    )
    rotated = M5024.rotate_internal(internal, global_root)
    left, right = M5017.cut_momenta(
        rotated, problem["target"], 1.0
    )
    return {
        "relative_root": relative_root,
        "global_root": global_root,
        "left": left,
        "right": right,
    }


def surface_value(
    geometry: dict[str, Any], surface_id: str
) -> complex:
    return M5235.surface_value(geometry, surface_id)


def surface_values(
    problem: dict[str, Any], coordinate: complex
) -> dict[str, complex]:
    geometry = collision_geometry(problem, coordinate)
    return {
        row["surface_id"]: surface_value(geometry, row["surface_id"])
        for row in problem["atlas_rows"]
    }


def scan_surfaces(
    problem: dict[str, Any],
) -> tuple[dict[str, list[complex]], list[dict[str, Any]]]:
    values_by_surface = {
        row["surface_id"]: [] for row in problem["atlas_rows"]
    }
    for coordinate in problem["coordinates"]:
        values = surface_values(problem, complex(float(coordinate)))
        for surface_id, value in values.items():
            values_by_surface[surface_id].append(value)
    rows: list[dict[str, Any]] = []
    for surface_id, values in values_by_surface.items():
        magnitudes = np.abs(np.asarray(values, dtype=np.complex128))
        real_values = np.real(np.asarray(values, dtype=np.complex128))
        minimum_index = int(np.argmin(magnitudes))
        sign_changes = sum(
            real_values[index] * real_values[index + 1] < 0.0
            for index in range(len(real_values) - 1)
        )
        rows.append(
            {
                "job_id": problem["job"]["job_id"],
                "component_id": problem["component_id"],
                "family": problem["case"]["family"],
                "outer_coordinate": problem["case"]["outer_coordinate"],
                "surface_id": surface_id,
                "sign_change_count": sign_changes,
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
    lower_value = surface_values(problem, lower)[surface_id].real
    upper_value = surface_values(problem, upper)[surface_id].real
    if lower_value == 0.0:
        return lower
    if upper_value == 0.0:
        return upper
    if lower_value * upper_value > 0.0:
        raise RuntimeError("root bracket does not change sign")
    for _ in range(70):
        midpoint = 0.5 * (lower + upper)
        midpoint_value = surface_values(
            problem, midpoint
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
            step = min(
                1.0e-6,
                0.05
                * (
                    float(problem["job"]["scan_maximum"])
                    - float(problem["job"]["scan_minimum"])
                )
                / (int(problem["job"]["scan_points"]) - 1),
            )
            center_value = surface_values(problem, center)[surface_id]
            derivative = (
                surface_values(problem, center + step)[surface_id]
                - surface_values(problem, center - step)[surface_id]
            ) / (2.0 * step)
            if abs(derivative) < 1.0e-10:
                continue
            pole = complex(center) - center_value / derivative
            if not (
                float(problem["job"]["scan_minimum"]) < pole.real
                < float(problem["job"]["scan_maximum"])
                and abs(pole.imag) < POLE_IMAGINARY_LIMIT
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
                < ROOT_GROUP_TOLERANCE
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
                "pole_id": f"P{index:02d}",
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


def homotopy_branch_path(
    roots_path: list[list[complex]], anchor: complex
) -> tuple[list[complex], float, float]:
    if any(not roots for roots in roots_path):
        raise RuntimeError("homotopy collision branch disappeared")
    anchor_index, anchor_root = min(
        (
            (
                index,
                min(
                    roots,
                    key=lambda root: M5030.chordal_distance(
                        root, anchor
                    ),
                ),
            )
            for index, roots in enumerate(roots_path)
        ),
        key=lambda item: M5030.chordal_distance(item[1], anchor),
    )
    selected: list[complex | None] = [None] * len(roots_path)
    selected[anchor_index] = anchor_root
    previous = anchor_root
    for index in range(anchor_index + 1, len(roots_path)):
        root = min(
            roots_path[index],
            key=lambda candidate: M5030.chordal_distance(
                candidate, previous
            ),
        )
        selected[index] = root
        previous = root
    previous = anchor_root
    for index in range(anchor_index - 1, -1, -1):
        root = min(
            roots_path[index],
            key=lambda candidate: M5030.chordal_distance(
                candidate, previous
            ),
        )
        selected[index] = root
        previous = root
    roots = [complex(root) for root in selected if root is not None]
    maximum_step = max(
        (
            M5030.chordal_distance(roots[index - 1], roots[index])
            for index in range(1, len(roots))
        ),
        default=0.0,
    )
    margins = [
        min(
            (
                M5030.chordal_distance(selected_root, candidate)
                for candidate in candidates
                if M5030.chordal_distance(
                    selected_root, candidate
                )
                > 1.0e-12
            ),
            default=1.0,
        )
        for selected_root, candidates in zip(roots, roots_path)
    ]
    return roots, maximum_step, min(margins)


def branch_aware_target_pair_track(
    event: dict[str, Any],
    target: complex,
    pairs_and_anchors: list[tuple[tuple[str, str], complex]],
    steps: int,
) -> dict[str, Any]:
    M5034.configure(event, target)
    cosines = M5030.homotopy_cosines(
        steps, M5232.REGULATOR, "feynman"
    )
    boundaries, ownerships = M5030.physical_chambers()
    endpoint_paths, _, boundary_step = M5030.endpoint_log_paths(
        boundaries, cosines, M5232.BOUNDARY_TRACKING_STEPS
    )
    tracks: list[dict[str, Any]] = []
    roots_by_pair: list[list[complex]] = []
    maximum_step = 0.0
    minimum_margin = math.inf
    for pair, anchor in pairs_and_anchors:
        roots_path = [
            M5030.M5029.collision_roots(
                M5030.M5029.root_rationals(
                    float(event["soft_energy"]),
                    float(event["soft_cosine"]),
                    float(event["decay_cosine"]),
                    cosine,
                )[pair[0]],
                M5030.M5029.root_rationals(
                    float(event["soft_energy"]),
                    float(event["soft_cosine"]),
                    float(event["decay_cosine"]),
                    cosine,
                )[pair[1]],
            )
            for cosine in cosines
        ]
        roots, pair_step, branch_margin = homotopy_branch_path(
            roots_path, anchor
        )
        maximum_step = max(maximum_step, pair_step)
        minimum_margin = min(minimum_margin, branch_margin)
        logs: list[complex] = []
        previous: complex | None = None
        for root in roots:
            value = (
                complex(np.log(root))
                if previous is None
                else M5030.lifted_log(root, previous)
            )
            logs.append(value)
            previous = value
        roots_by_pair.append(roots)
        tracks.append(
            {
                "logs": logs,
                "initial_pairs": [pair],
                "target_pairs": [pair],
            }
        )
    reciprocal_residual = max(
        abs(roots_by_pair[0][index] * roots_by_pair[1][index] - 1.0)
        for index in range(len(cosines))
    )
    crossings: list[dict[str, Any]] = []
    for chamber_index, ownership in enumerate(ownerships):
        selected = [
            track
            for track in tracks
            if ownership[track["target_pairs"][0][0]]
            != ownership[track["target_pairs"][0][1]]
        ]
        start_logs, end_logs = M5030.chamber_segment_logs(
            endpoint_paths, chamber_index
        )
        chamber_crossings, _ = M5030.surface_crossings(
            selected, start_logs, end_logs
        )
        crossings.extend(chamber_crossings)
    pair_rows: list[dict[str, Any]] = []
    for pair, _ in pairs_and_anchors:
        selected = [
            crossing
            for crossing in crossings
            if crossing["target_pairs"][0] == list(pair)
        ]
        pair_rows.append(
            {
                "pair": list(pair),
                "crossing_count": len(selected),
                "winding_sum": sum(
                    int(row["winding_correction"])
                    for row in selected
                ),
            }
        )
    return {
        "steps": steps,
        "pair_rows": pair_rows,
        "maximum_pair_projective_step": maximum_step,
        "maximum_boundary_projective_step": boundary_step,
        "maximum_reciprocal_product_residual": reciprocal_residual,
        "minimum_alternate_branch_separation": minimum_margin,
    }


def topology_audit(
    problem: dict[str, Any], poles: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    case = problem["case"]
    expected = {
        "u": int(case["expected_u_winding"]),
        "v": int(case["expected_v_winding"]),
    }
    pairs = [
        case["reciprocal_pair"],
        case["representative_pair"],
    ]
    for pole in poles:
        event = dict(problem["event"])
        coordinate = float(pole["real_axis_center"])
        event[case["outer_coordinate"]] = coordinate
        pairs_and_anchors = [
            (
                pair,
                track_anchor(
                    problem["branch_tracks"][pair_key(pair)],
                    complex(coordinate),
                ),
            )
            for pair in pairs
        ]
        steps = TOPOLOGY_STEPS
        audit = branch_aware_target_pair_track(
            event, problem["target"], pairs_and_anchors, steps
        )
        winding = {
            row["pair"][0].rsplit("_", 1)[-1]: int(
                row["winding_sum"]
            )
            for row in audit["pair_rows"]
        }
        active = winding == expected
        if (
            audit["maximum_pair_projective_step"]
            >= 0.5 * PROJECTIVE_LIMIT
            and steps < MAXIMUM_TOPOLOGY_STEPS
        ):
            steps = MAXIMUM_TOPOLOGY_STEPS
            audit = branch_aware_target_pair_track(
                event, problem["target"], pairs_and_anchors, steps
            )
            winding = {
                row["pair"][0].rsplit("_", 1)[-1]: int(
                    row["winding_sum"]
                )
                for row in audit["pair_rows"]
            }
            active = winding == expected
        pole["causal_family_active"] = active
        pole["u_winding"] = winding.get("u")
        pole["v_winding"] = winding.get("v")
        pole["topology_steps"] = steps
        pole["maximum_pair_projective_step"] = audit[
            "maximum_pair_projective_step"
        ]
        pole["maximum_reciprocal_product_residual"] = audit[
            "maximum_reciprocal_product_residual"
        ]
        pole["minimum_alternate_branch_separation"] = audit[
            "minimum_alternate_branch_separation"
        ]
        for pair_row in audit["pair_rows"]:
            suffix = pair_row["pair"][0].rsplit("_", 1)[-1]
            rows.append(
                {
                    "job_id": problem["job"]["job_id"],
                    "pole_id": pole["pole_id"],
                    "component_id": problem["component_id"],
                    "family": case["family"],
                    "pair": "|".join(pair_row["pair"]),
                    "suffix": suffix,
                    "winding_sum": int(pair_row["winding_sum"]),
                    "expected_winding_sum": expected[suffix],
                    "winding_matches": (
                        int(pair_row["winding_sum"])
                        == expected[suffix]
                    ),
                    "causal_family_active": active,
                    "topology_steps": steps,
                    "maximum_pair_projective_step": audit[
                        "maximum_pair_projective_step"
                    ],
                    "maximum_boundary_projective_step": audit[
                        "maximum_boundary_projective_step"
                    ],
                    "maximum_reciprocal_product_residual": audit[
                        "maximum_reciprocal_product_residual"
                    ],
                    "minimum_alternate_branch_separation": audit[
                        "minimum_alternate_branch_separation"
                    ],
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
            )
    return rows


def updated_component_topology(
    problem: dict[str, Any], coordinate: float
) -> dict[str, Any]:
    topology = copy.deepcopy(problem["topology"])
    representative_pair = problem["case"]["representative_pair"]
    reciprocal_pair = problem["case"]["reciprocal_pair"]
    representative_root, reciprocal_root = selected_component_roots(
        problem,
        complex(coordinate),
    )
    reciprocal_residual = abs(
        representative_root * reciprocal_root - 1.0
    )
    targets = (
        (
            int(problem["job"]["representative_chamber"]),
            problem["representative"],
            representative_root,
        ),
        (
            int(problem["job"]["reciprocal_chamber"]),
            problem["reciprocal"],
            reciprocal_root,
        ),
    )
    retained = 0
    for chamber_index, chamber in enumerate(topology["chambers"]):
        selected_crossings: list[dict[str, Any]] = []
        for target_chamber, source_crossing, root in targets:
            if chamber_index != target_chamber:
                continue
            crossing = copy.deepcopy(source_crossing)
            crossing["target_root"] = str(root)
            selected_crossings.append(crossing)
            retained += 1
        chamber["surface_crossings"] = selected_crossings
    if retained != 2:
        raise RuntimeError(
            f"component topology retained {retained} crossings"
        )
    topology["component_reciprocal_residual"] = reciprocal_residual
    return topology


def component_cycle_state(
    problem: dict[str, Any],
    coordinate: float,
    topology: dict[str, Any] | None = None,
) -> tuple[bool, float]:
    if topology is None:
        topology = updated_component_topology(problem, coordinate)
    reciprocal_residual = float(
        topology["component_reciprocal_residual"]
    )
    if reciprocal_residual > 2.0e-8:
        return False, reciprocal_residual
    event = dict(problem["event"])
    event[problem["case"]["outer_coordinate"]] = float(coordinate)
    ownership_states: list[bool] = []
    for chamber in topology["chambers"]:
        ownership = M5231.chamber_ownership(event, chamber)
        for crossing in chamber["surface_crossings"]:
            labels = crossing["representing_pairs"][0]
            ownership_states.append(
                sum(bool(ownership[label]) for label in labels) == 1
            )
    return (
        len(ownership_states) == 2 and all(ownership_states),
        reciprocal_residual,
    )


def component_contribution(
    problem: dict[str, Any], coordinate: float
) -> complex:
    event = dict(problem["event"])
    event[problem["case"]["outer_coordinate"]] = float(coordinate)
    topology = updated_component_topology(problem, coordinate)
    cycle_active, _ = component_cycle_state(
        problem, coordinate, topology
    )
    if not cycle_active:
        return 0.0j
    contributions, _ = M5231.safe_family_contributions(event, topology)
    return complex(contributions.get(problem["case"]["family"], 0.0j))


def local_cycle_half_width(
    problem: dict[str, Any], center: float
) -> float:
    center_active, _ = component_cycle_state(problem, center)
    if not center_active:
        raise RuntimeError(
            f"active winding pole is outside the local cycle at {center}"
        )
    lower_limit = float(problem["job"]["scan_minimum"])
    upper_limit = float(problem["job"]["scan_maximum"])
    margins: list[float] = []
    for direction, boundary in (
        (-1.0, lower_limit),
        (1.0, upper_limit),
    ):
        available = abs(boundary - center)
        probe_width = min(2.0 * PATCH_HALF_WIDTH, available)
        previous = center
        transition: tuple[float, float] | None = None
        for fraction in np.linspace(1.0 / 32.0, 1.0, 32):
            coordinate = center + direction * probe_width * float(
                fraction
            )
            active, _ = component_cycle_state(problem, coordinate)
            if not active:
                transition = previous, coordinate
                break
            previous = coordinate
        if transition is None:
            margins.append(probe_width)
            continue
        active_coordinate, inactive_coordinate = transition
        for _ in range(45):
            midpoint = 0.5 * (
                active_coordinate + inactive_coordinate
            )
            active, _ = component_cycle_state(problem, midpoint)
            if active:
                active_coordinate = midpoint
            else:
                inactive_coordinate = midpoint
        margins.append(abs(active_coordinate - center))
    return min(margins)


def fit_active_residues(
    problem: dict[str, Any],
    poles: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    active = [row for row in poles if row["causal_family_active"]]
    rows: list[dict[str, Any]] = []
    all_centers = [
        float(row["real_axis_center"]) for row in poles
    ]
    lower = float(problem["job"]["scan_minimum"])
    upper = float(problem["job"]["scan_maximum"])
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
        cycle_half_width = local_cycle_half_width(problem, center)
        maximum_fit_radius = min(
            5.0e-3,
            0.2 * nearest,
            0.2 * cycle_half_width,
            0.2 * (center - lower),
            0.2 * (upper - center),
        )
        if maximum_fit_radius < 2.0e-5:
            raise RuntimeError(
                f"insufficient isolated fit radius at {center}"
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
            fit_radius = maximum_fit_radius * 0.5**refinement
            if fit_radius < 2.0e-5:
                break
            offsets = fit_radius * np.asarray(
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
                contribution = component_contribution(
                    problem, coordinate
                )
                channel = surface_values(problem, coordinate)[
                    surface_id
                ]
                contributions.append(contribution)
                numerators.append(channel * contribution)
            coefficients = np.polyfit(
                offsets,
                np.asarray(numerators, dtype=np.complex128),
                3,
            )
            fitted = np.polyval(coefficients, offsets)
            fit_residual = float(
                np.max(
                    np.abs(
                        fitted
                        - np.asarray(
                            numerators, dtype=np.complex128
                        )
                    )
                )
                / max(
                    float(
                        np.max(
                            np.abs(
                                np.asarray(
                                    numerators,
                                    dtype=np.complex128,
                                )
                            )
                        )
                    ),
                    1.0e-30,
                )
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
            fit_passed = (
                fit_residual
                <= NUMERATOR_FIT_RELATIVE_RESIDUAL_LIMIT
                and all(
                    abs(slopes[side] + 1.0) <= SLOPE_TOLERANCE
                    for side in ("negative", "positive")
                )
            )
            candidates.append(
                {
                    "fit_radius": fit_radius,
                    "fit_residual": fit_residual,
                    "numerator_at_pole": numerator_at_pole,
                    "slopes": slopes,
                    "fit_passed": fit_passed,
                    "score": max(
                        fit_residual
                        / NUMERATOR_FIT_RELATIVE_RESIDUAL_LIMIT,
                        *[
                            abs(slopes[side] + 1.0)
                            / SLOPE_TOLERANCE
                            for side in ("negative", "positive")
                        ],
                    ),
                }
            )
            if fit_passed:
                break
        selected_fit = next(
            (
                candidate
                for candidate in candidates
                if candidate["fit_passed"]
            ),
            min(candidates, key=lambda candidate: candidate["score"]),
        )
        fit_radius = float(selected_fit["fit_radius"])
        fit_residual = float(selected_fit["fit_residual"])
        numerator_at_pole = complex(
            selected_fit["numerator_at_pole"]
        )
        slopes = selected_fit["slopes"]
        fit_passed = bool(selected_fit["fit_passed"])
        residue = numerator_at_pole / derivative
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
                "fit_radius": fit_radius,
                "local_cycle_half_width": cycle_half_width,
                "patch_half_width": min(
                    PATCH_HALF_WIDTH,
                    0.8 * cycle_half_width,
                    fit_radius,
                ),
                "fit_refinement_count": candidates.index(selected_fit),
                "channel_derivative_real": derivative.real,
                "channel_derivative_imaginary": derivative.imag,
                "numerator_at_pole_real": numerator_at_pole.real,
                "numerator_at_pole_imaginary": numerator_at_pole.imag,
                "outer_residue_real": residue.real,
                "outer_residue_imaginary": residue.imag,
                "numerator_fit_relative_residual": fit_residual,
                "negative_log_log_slope": slopes["negative"],
                "positive_log_log_slope": slopes["positive"],
                "fit_passed": fit_passed,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    return rows


def patch_groups(
    fits: list[dict[str, Any]],
    lower_limit: float,
    upper_limit: float,
) -> list[dict[str, Any]]:
    ordered = sorted(fits, key=lambda row: float(row["pole_real"]))
    groups: list[dict[str, Any]] = []
    for fit in ordered:
        half_width = float(fit["patch_half_width"])
        lower = max(
            lower_limit, float(fit["pole_real"]) - half_width
        )
        upper = min(
            upper_limit, float(fit["pole_real"]) + half_width
        )
        if groups and lower <= groups[-1]["upper"]:
            groups[-1]["upper"] = max(groups[-1]["upper"], upper)
            groups[-1]["fits"].append(fit)
        else:
            groups.append(
                {"lower": lower, "upper": upper, "fits": [fit]}
            )
    return groups


def integrate_patch_unions(
    problem: dict[str, Any],
    fits: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    accepted = [row for row in fits if bool(row["fit_passed"])]
    groups = patch_groups(
        accepted,
        float(problem["job"]["scan_minimum"]),
        float(problem["job"]["scan_maximum"]),
    )
    rows: list[dict[str, Any]] = []
    combined_by_order: dict[int, tuple[complex, complex]] = {}
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
        for order in QUADRATURE_ORDERS:
            nodes, weights = np.polynomial.legendre.leggauss(order)
            half_width = 0.5 * (upper - lower)
            midpoint = 0.5 * (upper + lower)
            coordinates = half_width * nodes + midpoint
            physical_weights = half_width * weights
            values = np.asarray(
                [
                    component_contribution(
                        problem, float(coordinate)
                    )
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
                    "patch_group_id": f"G{group_index:02d}",
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
    for order in QUADRATURE_ORDERS:
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
        combined_by_order[order] = raw, subtracted
    if not groups:
        return rows, {
            "active_patch_group_count": 0,
            "accepted_fit_count": 0,
            "quadrature_available": False,
        }
    reference = combined_by_order[QUADRATURE_ORDERS[-1]][1]
    denominator = max(abs(reference), 1.0)
    errors = {
        order: {
            "raw": abs(combined_by_order[order][0] - reference)
            / denominator,
            "subtracted": abs(
                combined_by_order[order][1] - reference
            )
            / denominator,
        }
        for order in QUADRATURE_ORDERS
    }
    return rows, {
        "active_patch_group_count": len(groups),
        "accepted_fit_count": len(accepted),
        "quadrature_available": True,
        "reference_order": QUADRATURE_ORDERS[-1],
        "subtracted_reference": complex_row(reference),
        "low_order_raw_relative_error": errors[
            QUADRATURE_ORDERS[0]
        ]["raw"],
        "low_order_subtracted_relative_error": errors[
            QUADRATURE_ORDERS[0]
        ]["subtracted"],
        "mid_order_subtracted_relative_error": errors[
            QUADRATURE_ORDERS[1]
        ]["subtracted"],
        "low_order_improvement_factor": (
            errors[QUADRATURE_ORDERS[0]]["raw"]
            / max(
                errors[QUADRATURE_ORDERS[0]]["subtracted"],
                1.0e-30,
            )
        ),
    }


def run_job(job: dict[str, Any]) -> dict[str, Any]:
    started = time.monotonic()
    problem = build_problem(job)
    values, scan_rows = scan_surfaces(problem)
    poles = locate_geometric_roots(problem, values)
    if len(poles) > MAXIMUM_ROOTS_PER_JOB:
        raise RuntimeError(
            f"root cap exceeded: {len(poles)} > {MAXIMUM_ROOTS_PER_JOB}"
        )
    topology_rows = topology_audit(problem, poles)
    active = [row for row in poles if row["causal_family_active"]]
    if len(active) > MAXIMUM_ACTIVE_ROOTS_PER_JOB:
        raise RuntimeError(
            f"active root cap exceeded: {len(active)}"
        )
    fits = fit_active_residues(problem, poles)
    quadrature_rows, quadrature = integrate_patch_unions(
        problem, fits
    )
    branch_steps = [
        float(track["maximum_projective_step"])
        for track in problem["branch_tracks"].values()
    ]
    branch_margins = [
        float(track["minimum_alternate_branch_separation"])
        for track in problem["branch_tracks"].values()
    ]
    topology_stable = all(
        float(row["maximum_pair_projective_step"])
        < PROJECTIVE_LIMIT
        and float(row["maximum_reciprocal_product_residual"])
        < RECIPROCAL_LIMIT
        for row in poles
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
            <= LOW_ORDER_SUBTRACTED_RELATIVE_ERROR_LIMIT
            and float(
                quadrature["mid_order_subtracted_relative_error"]
            )
            <= MID_ORDER_SUBTRACTED_RELATIVE_ERROR_LIMIT
        )
    )
    job_passed = (
        topology_stable
        and fit_complete
        and quadrature_passed
        and max(branch_steps, default=0.0) < PROJECTIVE_LIMIT
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
        "minimum_coordinate_alternate_branch_separation": min(
            branch_margins, default=math.inf
        ),
        "topology_stable": topology_stable,
        "fit_complete": fit_complete,
        "quadrature_passed": quadrature_passed,
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
            raise RuntimeError("bounded run time cap exceeded")
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


def flattened_rows(
    jobs: list[dict[str, Any]],
    results: list[dict[str, Any]],
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
]:
    job_lookup = {job["job_id"]: job for job in jobs}
    job_rows: list[dict[str, Any]] = []
    scan_rows: list[dict[str, Any]] = []
    poles: list[dict[str, Any]] = []
    topology: list[dict[str, Any]] = []
    fits: list[dict[str, Any]] = []
    quadrature: list[dict[str, Any]] = []
    for result in results:
        job = job_lookup[result["job_id"]]
        summary = {
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
            "geometric_root_count": result["geometric_root_count"],
            "active_root_count": result["active_root_count"],
            "inactive_root_count": result["inactive_root_count"],
            "maximum_coordinate_branch_projective_step": result.get(
                "maximum_coordinate_branch_projective_step", ""
            ),
            "minimum_coordinate_alternate_branch_separation": result.get(
                "minimum_coordinate_alternate_branch_separation", ""
            ),
            "topology_stable": result.get("topology_stable", False),
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
        job_rows.append(summary)
        scan_rows.extend(result["scan_rows"])
        poles.extend(result["poles"])
        topology.extend(result["topology_rows"])
        fits.extend(result["fits"])
        quadrature.extend(result["quadrature_rows"])
    return job_rows, scan_rows, poles, topology, fits, quadrature


def pooled_convergence(
    quadrature_rows: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    combined: dict[int, tuple[complex, complex]] = {}
    for order in QUADRATURE_ORDERS:
        selected = [
            row
            for row in quadrature_rows
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
    reference = combined[QUADRATURE_ORDERS[-1]][1]
    denominator = max(abs(reference), 1.0)
    for order in QUADRATURE_ORDERS:
        raw, subtracted = combined[order]
        rows.append(
            {
                "quadrature_order": order,
                "raw_integral_real": raw.real,
                "raw_integral_imaginary": raw.imag,
                "subtracted_integral_real": subtracted.real,
                "subtracted_integral_imaginary": subtracted.imag,
                "raw_relative_error_to_subtracted_512": (
                    abs(raw - reference) / denominator
                ),
                "subtracted_relative_error_to_subtracted_512": (
                    abs(subtracted - reference) / denominator
                ),
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    low = rows[0]
    mid = rows[1]
    return rows, {
        "reference_order": QUADRATURE_ORDERS[-1],
        "subtracted_reference": complex_row(reference),
        "low_order_raw_relative_error": low[
            "raw_relative_error_to_subtracted_512"
        ],
        "low_order_subtracted_relative_error": low[
            "subtracted_relative_error_to_subtracted_512"
        ],
        "mid_order_subtracted_relative_error": mid[
            "subtracted_relative_error_to_subtracted_512"
        ],
        "low_order_improvement_factor": (
            float(low["raw_relative_error_to_subtracted_512"])
            / max(
                float(
                    low[
                        "subtracted_relative_error_to_subtracted_512"
                    ]
                ),
                1.0e-30,
            )
        ),
    }


def validation_rows(
    manifest: dict[str, Any],
    dry_run: dict[str, Any],
    results: list[dict[str, Any]],
    job_rows: list[dict[str, Any]],
    scan_rows: list[dict[str, Any]],
    poles: list[dict[str, Any]],
    topology_rows: list[dict[str, Any]],
    fits: list[dict[str, Any]],
    quadrature_rows: list[dict[str, Any]],
    pool: dict[str, Any],
) -> list[dict[str, Any]]:
    required = [
        SCRIPT_5234,
        SCRIPT_5235,
        RESULT_5234,
        ATLAS_5234,
        FAMILY_SOURCE,
        MANIFEST_JSON,
        MANIFEST_CSV,
        DRY_RUN,
    ]
    claims_false = all(
        not bool(row[key])
        for collection in (
            manifest["jobs"],
            results,
            job_rows,
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
    inactive_ids = {
        (row["job_id"], row["pole_id"])
        for row in poles
        if not bool(row["causal_family_active"])
    }
    fitted_ids = {
        (row["job_id"], row["pole_id"]) for row in fits
    }
    active_ids = {
        (row["job_id"], row["pole_id"])
        for row in poles
        if bool(row["causal_family_active"])
    }
    jobs_by_id = {
        job["job_id"]: job for job in manifest["jobs"]
    }
    unbracketed_interior_candidates = []
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
            unbracketed_interior_candidates.append(row)
    sign_change_count = sum(
        int(row["sign_change_count"]) for row in scan_rows
    )
    represented_root_surface_count = sum(
        int(row["surface_count"]) for row in poles
    )
    checks = [
        (
            "required_sources_exist",
            all(path.exists() for path in required),
            f"{len(required)} required paths",
        ),
        (
            "dry_run_authorized_exact_manifest",
            bool(dry_run["authorized_to_execute"])
            and dry_run["manifest_sha256"] == digest(MANIFEST_JSON),
            dry_run["manifest_sha256"],
        ),
        (
            "bounded_manifest_complete",
            len(manifest["jobs"]) == EXPECTED_JOB_COUNT
            and len(manifest["jobs"]) <= MAXIMUM_JOB_COUNT,
            f"{len(manifest['jobs'])} jobs",
        ),
        (
            "component_coordinate_cross_product_complete",
            len(
                {
                    (
                        job["component_id"],
                        job["outer_coordinate"],
                    )
                    for job in manifest["jobs"]
                }
            )
            == EXPECTED_COMPONENT_COUNT * len(OUTER_COORDINATES),
            (
                f"{EXPECTED_COMPONENT_COUNT} components x "
                f"{len(OUTER_COORDINATES)} coordinates"
            ),
        ),
        (
            "all_jobs_completed_and_passed",
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
            "root_caps_respected",
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
            "root_scan_exhaustive_on_bounded_grid",
            sign_change_count == represented_root_surface_count
            and not unbracketed_interior_candidates,
            (
                f"{sign_change_count} sign changes; "
                f"{represented_root_surface_count} represented surfaces; "
                f"{len(unbracketed_interior_candidates)} "
                "unbracketed interior near-zeros"
            ),
        ),
        (
            "causal_gate_complete",
            active_ids == fitted_ids
            and inactive_ids.isdisjoint(fitted_ids)
            and all(
                float(row["maximum_pair_projective_step"])
                < PROJECTIVE_LIMIT
                and float(
                    row["maximum_reciprocal_product_residual"]
                )
                < RECIPROCAL_LIMIT
                for row in poles
            ),
            (
                f"{len(active_ids)} active; "
                f"{len(inactive_ids)} inactive"
            ),
        ),
        (
            "residue_fits_pass",
            bool(fits) and all(bool(row["fit_passed"]) for row in fits),
            f"{sum(bool(row['fit_passed']) for row in fits)}/{len(fits)}",
        ),
        (
            "union_quadrature_passes",
            bool(quadrature_rows)
            and all(bool(row["quadrature_passed"]) for row in job_rows),
            f"{len(quadrature_rows)} patch-order rows",
        ),
        (
            "pooled_subtraction_converges",
            float(pool["low_order_subtracted_relative_error"])
            <= LOW_ORDER_SUBTRACTED_RELATIVE_ERROR_LIMIT
            and float(pool["mid_order_subtracted_relative_error"])
            <= MID_ORDER_SUBTRACTED_RELATIVE_ERROR_LIMIT,
            (
                f"low={pool['low_order_subtracted_relative_error']}; "
                f"mid={pool['mid_order_subtracted_relative_error']}"
            ),
        ),
        (
            "claim_boundary_preserved",
            claims_false,
            "all claim flags false",
        ),
        (
            "formalization_workbench_unchanged",
            tree_digest(FORMAL) == FORMAL_BASELINE,
            tree_digest(FORMAL),
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
    job_rows: list[dict[str, Any]],
) -> str:
    passed_jobs = sum(bool(row["job_passed"]) for row in job_rows)
    root_jobs = sum(int(row["active_root_count"]) > 0 for row in job_rows)
    pool = result["pooled_quadrature"]
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
    return f"""# 5237 - Bounded multi-event direct A00 causal runner

## Decision

`{result['decision']}`.

This checkpoint converts the 5235/5236 hand-selected slices into a
deterministic, cached and time-bounded runner.  It selects the strongest real
event in every direct-family/tranche stratum and expands every reciprocal
component before looking at the new roots.

## Coverage

- Direct residue families: `{result['family_count']}`.
- Family/tranche strata: `{result['stratum_count']}`.
- Reciprocal components: `{result['component_count']}`.
- Component-coordinate jobs: `{result['job_count']}`.
- Distinct source events: `{result['unique_event_count']}`.
- Outer coordinates: `soft_energy`, `soft_cosine`, and `decay_cosine`.
- Passed jobs: `{passed_jobs}/{len(job_rows)}`.

The dry run fixed the manifest before execution and bounded the job count,
surface scans, roots, topology steps, quadrature orders and wall-clock time.
Each job is independently cached by an input hash.

## Causal result

The all-channel scans found `{result['total_geometric_root_count']}`
geometric roots.  The branch-aware winding audit retained
`{result['total_active_root_count']}` as active and rejected
`{result['total_inactive_root_count']}` as inactive.  Residues were fitted
only for active roots; inactive denominator zeros were never subtracted.

Active roots occurred in `{root_jobs}` of the `{len(job_rows)}` component
slices.  Multi-root overlaps were integrated as patch unions, so overlapping
windows are not double counted.

## Pooled convergence

Relative to the pooled order-{pool['reference_order']} subtracted result:

- raw order-32 error:
  `{pool['low_order_raw_relative_error']:.12g}`;
- subtracted order-32 error:
  `{pool['low_order_subtracted_relative_error']:.12g}`;
- subtracted order-128 error:
  `{pool['mid_order_subtracted_relative_error']:.12g}`;
- order-32 improvement:
  `{pool['low_order_improvement_factor']:.12g}x`.

## Failed jobs

{failure_text}

## Scope

This validates a bounded direct-summand computation, not the full
multidimensional A00 coefficient.  Endpoint-owned families still require
their own positive-residue implementation.  No numeric UV, local-GR, or
full-MTS claim is made.

## Next target

Build the endpoint-owned analogue using the same branch tracker and causal
gate, then combine direct and endpoint patch unions in a bounded
multi-event A00 coefficient run.
"""


def execute() -> dict[str, Any]:
    dry_run = read_json(DRY_RUN)
    if not bool(dry_run.get("authorized_to_execute")):
        raise RuntimeError("dry run did not authorize execution")
    manifest = read_json(MANIFEST_JSON)
    if dry_run["manifest_sha256"] != digest(MANIFEST_JSON):
        raise RuntimeError("manifest changed after dry run")
    started = time.monotonic()
    results, cache_hits = execute_jobs(manifest)
    (
        job_rows,
        scan_rows,
        poles,
        topology_rows,
        fits,
        quadrature_rows,
    ) = flattened_rows(manifest["jobs"], results)
    if len(poles) > MAXIMUM_TOTAL_ROOTS:
        raise RuntimeError("aggregate root cap exceeded")
    pool_rows, pool = pooled_convergence(quadrature_rows)
    validation = validation_rows(
        manifest,
        dry_run,
        results,
        job_rows,
        scan_rows,
        poles,
        topology_rows,
        fits,
        quadrature_rows,
        pool,
    )
    all_passed = all(bool(row["passed"]) for row in validation)
    decision = (
        "ADOPT_BOUNDED_MULTI_EVENT_DIRECT_A00_RUNNER_AND_EXTEND_TO_ENDPOINT_SUMMAND"
        if all_passed
        else "RETAIN_RUNNER_AND_REPAIR_FAILED_MULTI_EVENT_GATES_BEFORE_SCALE"
    )
    result = {
        "checkpoint_marker": MARKER,
        "revision": REVISION,
        "decision": decision,
        "scope": (
            "bounded direct-summand conditional A00 multi-event run; "
            "not the full multidimensional coefficient"
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
        "total_geometric_root_count": len(poles),
        "total_active_root_count": sum(
            bool(row["causal_family_active"]) for row in poles
        ),
        "total_inactive_root_count": sum(
            not bool(row["causal_family_active"]) for row in poles
        ),
        "passed_job_count": sum(
            bool(row["job_passed"]) for row in job_rows
        ),
        "pooled_quadrature": pool,
        "validation_all_passed": all_passed,
        "next_target": (
            "implement endpoint-owned positive-residue fitting with the "
            "same branch-aware causal gate, then combine both summands"
        ),
        "source_paths": manifest["source_paths"],
        "claim_boundary": {
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
        },
    }
    write_csv(JOB_ROWS, job_rows)
    write_csv(SCAN_ROWS, scan_rows)
    write_csv(POLE_ROWS, poles)
    write_csv(TOPOLOGY_ROWS, topology_rows)
    write_csv(RESIDUE_ROWS, fits)
    write_csv(QUADRATURE_ROWS, quadrature_rows)
    write_csv(POOL_ROWS, pool_rows)
    write_csv(VALIDATION, validation)
    atomic_json(RESULT, result)
    atomic_text(DOCUMENT, render_document(result, job_rows))
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
