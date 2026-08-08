from __future__ import annotations

import argparse
import cmath
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
from typing import Any, Callable

import numpy as np


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE = POST / "source-intake" / "functional_rg" / "5239"
RESIDUALS = POST / "source-intake" / "mts_residuals"

SCRIPT_5238 = (
    POST
    / "scripts"
    / "Y5_R2FR_5238_endpoint_owned_residue_and_combined_bounded_A00_runner.py"
)
FAMILY_SOURCE = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5231"
    / "pooled_A00_tail_family_decomposition.csv"
)

MANIFEST_JSON = SOURCE / "matched_event_A00_job_manifest.json"
MANIFEST_CSV = SOURCE / "matched_event_A00_job_manifest.csv"
DRY_RUN = SOURCE / "matched_event_A00_dry_run_report.json"
RESULT = SOURCE / "matched_event_A00_regular_complement_run.json"
COMPONENT_ROWS = SOURCE / "matched_regulator_component_map.csv"
CLOSURE_ROWS = SOURCE / "matched_event_integrand_closure.csv"
SCAN_ROWS = SOURCE / "matched_event_surface_scan_audit.csv"
POLE_ROWS = SOURCE / "matched_event_pole_catalog.csv"
TOPOLOGY_ROWS = SOURCE / "matched_event_causal_topology_audit.csv"
WINDING_INTERVAL_ROWS = (
    SOURCE / "matched_event_dynamic_winding_intervals.csv"
)
WINDING_INTERVAL_CACHE = (
    SOURCE / "matched_event_dynamic_winding_interval_cache.json"
)
RESIDUE_ROWS = SOURCE / "matched_event_residue_fit_summary.csv"
QUADRATURE_ROWS = SOURCE / "matched_event_regular_complement_quadrature.csv"
EXTRAPOLATION_ROWS = SOURCE / "matched_event_regulator_extrapolation.csv"
DOCUMENT = (
    POST
    / "5239-Y5-R2FR-matched-event-A00-regular-complement-and-regulator-extrapolation.md"
)
VALIDATION = RESIDUALS / "P8_Y5_BRR545_5239_VALIDATION.csv"

MARKER = (
    "MTS_5239_MATCHED_EVENT_A00_REGULAR_COMPLEMENT_AND_REGULATOR_EXTRAPOLATION"
)
REVISION = "matched-event-A00-regular-complement-regulator-extrapolation-v3"
FORMAL_BASELINE = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)

TARGET_TRANCHE = "old_5224"
TARGET_SEED = 522124
OUTER_COORDINATE = "soft_cosine"
EPSILON_IDS = ("E040", "E020")
SCAN_MINIMUM = -0.995
SCAN_MAXIMUM = 0.995
SCAN_POINTS = 601
MATERIAL_COMPONENT_FLOOR = 1.0e-10
EXPECTED_SAFE_COMPONENT_COUNT = 15
EXPECTED_MATERIAL_COMPONENT_COUNT = 6
EXPECTED_DIRECT_MATERIAL_COUNT = 4
EXPECTED_ENDPOINT_MATERIAL_COUNT = 2
EXPECTED_JOB_COUNT = 12
MAXIMUM_JOB_COUNT = 12
QUADRATURE_ORDERS = (32, 128, 512)
WITNESS_COORDINATES = (-0.9, -0.6, -0.35, 0.0, 0.3, 0.6, 0.9)
DYNAMIC_TOPOLOGY_STEPS = 1024
DYNAMIC_CONFIRMATION_STEPS = 4096
DYNAMIC_COARSE_POINTS = 25
DYNAMIC_BISECTION_STEPS = 26
DYNAMIC_PROJECTIVE_STEP_LIMIT = 5.0e-2
MATCH_PROJECTIVE_LIMIT = 5.0e-3
SOURCE_CLOSURE_LIMIT = 5.0e-9
DYNAMIC_CLOSURE_LIMIT = 2.0e-10
STORED_FAMILY_CLOSURE_LIMIT = 2.0e-10
LOW_ORDER_SUBTRACTED_RELATIVE_ERROR_LIMIT = 5.0e-3
MID_ORDER_SUBTRACTED_RELATIVE_ERROR_LIMIT = 1.0e-3
MINIMUM_LOW_ORDER_IMPROVEMENT = 10.0
MAXIMUM_RUN_SECONDS = 4.0 * 60.0 * 60.0


def load_module(path: Path, name: str) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5238 = load_module(SCRIPT_5238, "mts_5238_for_5239")
M5237 = M5238.M5237
M5235 = M5237.M5235
M5234 = M5237.M5234
M5231 = M5237.M5231
M5030 = M5237.M5030


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
    if isinstance(value, dict):
        return complex(float(value["real"]), float(value["imaginary"]))
    return complex(value)


def complex_row(value: complex) -> dict[str, float]:
    return {"real": float(value.real), "imaginary": float(value.imag)}


def serialized_hash(value: Any) -> str:
    payload = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        default=json_default,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def source_contract() -> dict[str, Any]:
    matches = [
        contract
        for contract in M5231.source_contracts()
        if contract["tranche"] == TARGET_TRANCHE
    ]
    if len(matches) != 1:
        raise RuntimeError(
            f"expected one source contract for {TARGET_TRANCHE}"
        )
    return matches[0]


def source_event(contract: dict[str, Any]) -> dict[str, Any]:
    config = read_json(Path(contract["config"]))
    matches = [
        event
        for event in config["events"]
        if int(event["seed"]) == TARGET_SEED
    ]
    if len(matches) != 1:
        raise RuntimeError(f"expected one source event for seed {TARGET_SEED}")
    return matches[0]


def crossing_without_chamber(entry: dict[str, Any]) -> dict[str, Any]:
    return {
        key: copy.deepcopy(value)
        for key, value in entry.items()
        if key != "chamber_index"
    }


def isolated_component_topology(
    topology: dict[str, Any],
    representative: dict[str, Any],
    reciprocal: dict[str, Any],
) -> dict[str, Any]:
    isolated = copy.deepcopy(topology)
    for chamber in isolated["chambers"]:
        chamber["surface_crossings"] = []
    for entry in (representative, reciprocal):
        chamber_index = int(entry["chamber_index"])
        isolated["chambers"][chamber_index]["surface_crossings"].append(
            crossing_without_chamber(entry)
        )
    retained = sum(
        len(chamber["surface_crossings"])
        for chamber in isolated["chambers"]
    )
    if retained != 2:
        raise RuntimeError(f"isolated topology retained {retained} crossings")
    return isolated


def label_signature(
    representative: dict[str, Any],
    reciprocal: dict[str, Any],
) -> str:
    pairs = [
        "|".join(entry["representing_pairs"][0])
        for entry in (representative, reciprocal)
    ]
    return "||".join(sorted(pairs))


def enumerate_components(
    event: dict[str, Any],
    topology: dict[str, Any],
    epsilon_id: str,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for pair_index, (first, second, pair_residual) in enumerate(
        M5231.reciprocal_pairs(topology)
    ):
        if M5231.reciprocal_pair_is_unsafe(
            first
        ) or M5231.reciprocal_pair_is_unsafe(second):
            continue
        representative, reciprocal = M5237.normalized_component(
            first, second
        )
        family = M5231.canonical_family(first, second)
        isolated = isolated_component_topology(
            topology, representative, reciprocal
        )
        contributions, diagnostics = M5231.safe_family_contributions(
            event, isolated
        )
        contribution = complex(contributions.get(family, 0.0j))
        owner = (
            "endpoint_subtraction"
            if "subtraction:decay:" in family
            else "direct_five_point"
        )
        rows.append(
            {
                "epsilon_id": epsilon_id,
                "source_pair_index": pair_index,
                "family": family,
                "owner_summand": owner,
                "label_signature": label_signature(
                    representative, reciprocal
                ),
                "representative": representative,
                "reciprocal": reciprocal,
                "representative_root": complex_value(
                    representative["target_root"]
                ),
                "reciprocal_root": complex_value(
                    reciprocal["target_root"]
                ),
                "raw_contribution": contribution,
                "reciprocal_pair_residual": float(pair_residual),
                "local_classifications": "|".join(
                    sorted(
                        {
                            str(row["classification"])
                            for row in diagnostics
                        }
                    )
                ),
            }
        )
    return rows


def match_regulator_components(
    event: dict[str, Any],
    topologies: dict[str, dict[str, Any]],
) -> list[dict[str, Any]]:
    by_epsilon = {
        epsilon_id: enumerate_components(
            event, topologies[epsilon_id], epsilon_id
        )
        for epsilon_id in EPSILON_IDS
    }
    first_id, second_id = EPSILON_IDS
    first_groups: defaultdict[tuple[str, str], list[dict[str, Any]]] = (
        defaultdict(list)
    )
    second_groups: defaultdict[tuple[str, str], list[dict[str, Any]]] = (
        defaultdict(list)
    )
    for row in by_epsilon[first_id]:
        first_groups[(row["family"], row["label_signature"])].append(row)
    for row in by_epsilon[second_id]:
        second_groups[(row["family"], row["label_signature"])].append(row)
    if set(first_groups) != set(second_groups):
        raise RuntimeError("regulator component signature sets differ")
    matches: list[dict[str, Any]] = []
    for group_key in sorted(first_groups):
        first_rows = first_groups[group_key]
        second_rows = second_groups[group_key]
        if len(first_rows) != len(second_rows):
            raise RuntimeError(
                f"regulator component multiplicity differs for {group_key}"
            )
        candidates = sorted(
            (
                M5030.chordal_distance(
                    first["representative_root"],
                    second["representative_root"],
                )
                + M5030.chordal_distance(
                    first["reciprocal_root"],
                    second["reciprocal_root"],
                ),
                first_index,
                second_index,
            )
            for first_index, first in enumerate(first_rows)
            for second_index, second in enumerate(second_rows)
        )
        consumed_first: set[int] = set()
        consumed_second: set[int] = set()
        for residual, first_index, second_index in candidates:
            if (
                first_index in consumed_first
                or second_index in consumed_second
            ):
                continue
            consumed_first.add(first_index)
            consumed_second.add(second_index)
            first = first_rows[first_index]
            second = second_rows[second_index]
            matches.append(
                {
                    "family": first["family"],
                    "owner_summand": first["owner_summand"],
                    "label_signature": first["label_signature"],
                    "match_projective_residual": float(residual),
                    first_id: first,
                    second_id: second,
                }
            )
        if len(consumed_first) != len(first_rows):
            raise RuntimeError(f"regulator matching failed for {group_key}")
    matches.sort(
        key=lambda row: (
            row["family"],
            row[second_id]["representative_root"].real,
            row[second_id]["representative_root"].imag,
        )
    )
    for index, row in enumerate(matches, start=1):
        row["component_id"] = f"MC{index:02d}"
        row["material"] = max(
            abs(row[epsilon_id]["raw_contribution"])
            for epsilon_id in EPSILON_IDS
        ) > MATERIAL_COMPONENT_FLOOR
    return matches


def suffix_windings(
    representative: dict[str, Any],
    reciprocal: dict[str, Any],
) -> dict[str, int]:
    windings: dict[str, int] = {}
    for entry in (representative, reciprocal):
        suffix = entry["representing_pairs"][0][0].rsplit("_", 1)[-1]
        winding = int(entry["winding_correction"])
        if suffix in windings and windings[suffix] != winding:
            raise RuntimeError(f"inconsistent {suffix} winding")
        windings[suffix] = winding
    if set(windings) != {"u", "v"}:
        raise RuntimeError(f"incomplete component windings: {windings}")
    return windings


def build_job(
    match: dict[str, Any],
    epsilon_id: str,
    contract: dict[str, Any],
    event: dict[str, Any],
) -> dict[str, Any]:
    component = match[epsilon_id]
    representative = component["representative"]
    reciprocal = component["reciprocal"]
    windings = suffix_windings(representative, reciprocal)
    topology_path = M5231.topology_path(
        contract, TARGET_SEED, epsilon_id
    )
    owner = match["owner_summand"]
    candidate_count = 8 if owner == "endpoint_subtraction" else 13
    job = {
        "job_id": f"{epsilon_id}_{match['component_id']}",
        "component_id": match["component_id"],
        "family": match["family"],
        "owner_summand": owner,
        "tranche": TARGET_TRANCHE,
        "seed": TARGET_SEED,
        "epsilon_id": epsilon_id,
        "outer_coordinate": OUTER_COORDINATE,
        "representative_pair": list(
            representative["representing_pairs"][0]
        ),
        "reciprocal_pair": list(reciprocal["representing_pairs"][0]),
        "expected_u_winding": windings["u"],
        "expected_v_winding": windings["v"],
        "representative_anchor": complex_row(
            component["representative_root"]
        ),
        "reciprocal_anchor": complex_row(component["reciprocal_root"]),
        "representative_chamber": int(
            representative["chamber_index"]
        ),
        "reciprocal_chamber": int(reciprocal["chamber_index"]),
        "scan_minimum": SCAN_MINIMUM,
        "scan_maximum": SCAN_MAXIMUM,
        "scan_points": SCAN_POINTS,
        "candidate_surface_count": candidate_count,
        "soft_energy": float(event["soft_energy"]),
        "soft_cosine": float(event["soft_cosine"]),
        "decay_cosine": float(event["decay_cosine"]),
        "base_raw_contribution": complex_row(
            component["raw_contribution"]
        ),
        "source_topology": str(topology_path),
        "source_topology_sha256": digest(topology_path),
        "source_config": str(contract["config"]),
        "match_projective_residual": match[
            "match_projective_residual"
        ],
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    job["job_input_hash"] = serialized_hash(job)
    return job


def component_csv_rows(matches: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for match in matches:
        row: dict[str, Any] = {
            "component_id": match["component_id"],
            "family": match["family"],
            "owner_summand": match["owner_summand"],
            "label_signature": match["label_signature"],
            "material": match["material"],
            "material_floor": MATERIAL_COMPONENT_FLOOR,
            "match_projective_residual": match[
                "match_projective_residual"
            ],
        }
        for epsilon_id in EPSILON_IDS:
            component = match[epsilon_id]
            row.update(
                {
                    f"{epsilon_id}_source_pair_index": component[
                        "source_pair_index"
                    ],
                    f"{epsilon_id}_representative_root_real": component[
                        "representative_root"
                    ].real,
                    f"{epsilon_id}_representative_root_imaginary": component[
                        "representative_root"
                    ].imag,
                    f"{epsilon_id}_reciprocal_root_real": component[
                        "reciprocal_root"
                    ].real,
                    f"{epsilon_id}_reciprocal_root_imaginary": component[
                        "reciprocal_root"
                    ].imag,
                    f"{epsilon_id}_raw_contribution_real": component[
                        "raw_contribution"
                    ].real,
                    f"{epsilon_id}_raw_contribution_imaginary": component[
                        "raw_contribution"
                    ].imag,
                    f"{epsilon_id}_raw_contribution_magnitude": abs(
                        component["raw_contribution"]
                    ),
                    f"{epsilon_id}_local_classifications": component[
                        "local_classifications"
                    ],
                }
            )
        row.update(
            {
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
        rows.append(row)
    return rows


def build_manifest() -> tuple[dict[str, Any], list[dict[str, Any]]]:
    contract = source_contract()
    event = source_event(contract)
    topologies = {
        epsilon_id: read_json(
            M5231.topology_path(contract, TARGET_SEED, epsilon_id)
        )
        for epsilon_id in EPSILON_IDS
    }
    matches = match_regulator_components(event, topologies)
    jobs = [
        build_job(match, epsilon_id, contract, event)
        for match in matches
        if match["material"]
        for epsilon_id in EPSILON_IDS
    ]
    manifest = {
        "marker": MARKER,
        "revision": REVISION,
        "target_event": event,
        "target_tranche": TARGET_TRANCHE,
        "outer_coordinate": OUTER_COORDINATE,
        "regulators": list(EPSILON_IDS),
        "source_contract": {
            key: str(value) if isinstance(value, Path) else value
            for key, value in contract.items()
        },
        "source_files": [
            {
                "path": str(Path(contract["config"])),
                "sha256": digest(Path(contract["config"])),
            },
            {
                "path": str(FAMILY_SOURCE),
                "sha256": digest(FAMILY_SOURCE),
            },
            *[
                {
                    "path": str(
                        M5231.topology_path(
                            contract, TARGET_SEED, epsilon_id
                        )
                    ),
                    "sha256": digest(
                        M5231.topology_path(
                            contract, TARGET_SEED, epsilon_id
                        )
                    ),
                }
                for epsilon_id in EPSILON_IDS
            ],
        ],
        "safe_component_count": len(matches),
        "material_component_count": sum(
            bool(row["material"]) for row in matches
        ),
        "direct_material_component_count": sum(
            bool(row["material"])
            and row["owner_summand"] == "direct_five_point"
            for row in matches
        ),
        "endpoint_material_component_count": sum(
            bool(row["material"])
            and row["owner_summand"] == "endpoint_subtraction"
            for row in matches
        ),
        "job_count": len(jobs),
        "maximum_job_count": MAXIMUM_JOB_COUNT,
        "scheduled_surface_evaluations": sum(
            int(job["scan_points"])
            * int(job["candidate_surface_count"])
            for job in jobs
        ),
        "quadrature_orders": list(QUADRATURE_ORDERS),
        "witness_coordinates": list(WITNESS_COORDINATES),
        "material_component_floor": MATERIAL_COMPONENT_FLOOR,
        "regulator_extrapolation": (
            "I_phys = w_A00 K_kernel (2 I_E020 - I_E040)"
        ),
        "physical_A00_weight": M5231.PHYSICAL_A00_WEIGHT,
        "kernel_multiplier": M5231.KERNEL_MULTIPLIER,
        "jobs": jobs,
        "claim_boundary": {
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
            "reason": (
                "This is one matched conditional event slice, not the "
                "complete multidimensional A00 coefficient."
            ),
        },
    }
    manifest["manifest_hash"] = serialized_hash(manifest)
    return manifest, matches


def manifest_csv_rows(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    return list(manifest["jobs"])


def write_manifest_and_dry_run() -> dict[str, Any]:
    manifest, matches = build_manifest()
    source_paths = [
        Path(row["path"]) for row in manifest["source_files"]
    ]
    checks = {
        "source_paths_exist": all(path.exists() for path in source_paths),
        "formal_digest_unchanged": tree_digest(FORMAL) == FORMAL_BASELINE,
        "safe_component_count_expected": (
            manifest["safe_component_count"]
            == EXPECTED_SAFE_COMPONENT_COUNT
        ),
        "material_component_count_expected": (
            manifest["material_component_count"]
            == EXPECTED_MATERIAL_COMPONENT_COUNT
        ),
        "direct_material_count_expected": (
            manifest["direct_material_component_count"]
            == EXPECTED_DIRECT_MATERIAL_COUNT
        ),
        "endpoint_material_count_expected": (
            manifest["endpoint_material_component_count"]
            == EXPECTED_ENDPOINT_MATERIAL_COUNT
        ),
        "job_count_bounded": (
            manifest["job_count"] == EXPECTED_JOB_COUNT
            and manifest["job_count"] <= MAXIMUM_JOB_COUNT
        ),
        "regulator_matches_bijective": (
            len(matches) == EXPECTED_SAFE_COMPONENT_COUNT
            and max(
                row["match_projective_residual"] for row in matches
            )
            <= MATCH_PROJECTIVE_LIMIT
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
        "job_count": manifest["job_count"],
        "scheduled_surface_evaluations": manifest[
            "scheduled_surface_evaluations"
        ],
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(MANIFEST_JSON, manifest)
    write_csv(MANIFEST_CSV, manifest_csv_rows(manifest))
    write_csv(COMPONENT_ROWS, component_csv_rows(matches))
    atomic_json(DRY_RUN, report)
    if not report["dry_run_passed"]:
        failed = [key for key, passed in checks.items() if not passed]
        raise RuntimeError(f"5239 dry run failed: {failed}")
    return report


def build_problem(job: dict[str, Any]) -> dict[str, Any]:
    if job["owner_summand"] == "endpoint_subtraction":
        return M5238.build_problem(job)
    if job["owner_summand"] == "direct_five_point":
        return M5237.build_problem(job)
    raise RuntimeError(f"unknown owner summand: {job['owner_summand']}")


def source_winding_delta(problem: dict[str, Any]) -> tuple[str, str, int]:
    representative_suffix = problem["case"]["representative_pair"][
        0
    ].rsplit("_", 1)[-1]
    reciprocal_suffix = problem["case"]["reciprocal_pair"][0].rsplit(
        "_", 1
    )[-1]
    expected = {
        "u": int(problem["case"]["expected_u_winding"]),
        "v": int(problem["case"]["expected_v_winding"]),
    }
    delta = (
        expected[representative_suffix]
        - expected[reciprocal_suffix]
    )
    if delta == 0:
        raise RuntimeError("source winding difference vanishes")
    return representative_suffix, reciprocal_suffix, delta


def winding_state(
    problem: dict[str, Any],
    coordinate: float,
    steps: int = DYNAMIC_TOPOLOGY_STEPS,
) -> dict[str, Any]:
    event = dict(problem["event"])
    event[problem["case"]["outer_coordinate"]] = float(coordinate)
    pairs = [
        problem["case"]["reciprocal_pair"],
        problem["case"]["representative_pair"],
    ]
    pairs_and_anchors = [
        (
            pair,
            M5237.track_anchor(
                problem["branch_tracks"][M5237.pair_key(pair)],
                complex(coordinate),
            ),
        )
        for pair in pairs
    ]
    audit = M5237.branch_aware_target_pair_track(
        event,
        problem["target"],
        pairs_and_anchors,
        steps,
    )
    winding = {
        row["pair"][0].rsplit("_", 1)[-1]: int(row["winding_sum"])
        for row in audit["pair_rows"]
    }
    if set(winding) != {"u", "v"}:
        raise RuntimeError(f"incomplete dynamic winding state: {winding}")
    representative_suffix, reciprocal_suffix, source_delta = (
        source_winding_delta(problem)
    )
    dynamic_delta = (
        winding[representative_suffix]
        - winding[reciprocal_suffix]
    )
    return {
        "u": winding["u"],
        "v": winding["v"],
        "dynamic_delta": dynamic_delta,
        "source_delta": source_delta,
        "multiplier": dynamic_delta / source_delta,
        "maximum_pair_projective_step": float(
            audit["maximum_pair_projective_step"]
        ),
        "maximum_reciprocal_product_residual": float(
            audit["maximum_reciprocal_product_residual"]
        ),
        "minimum_alternate_branch_separation": float(
            audit["minimum_alternate_branch_separation"]
        ),
        "topology_steps": steps,
    }


def state_key(state: dict[str, Any]) -> tuple[int, int]:
    return int(state["u"]), int(state["v"])


def derive_problem_winding_intervals(
    problem: dict[str, Any],
) -> list[dict[str, Any]]:
    lower = float(problem["job"]["scan_minimum"])
    upper = float(problem["job"]["scan_maximum"])
    base = float(
        problem["event"][problem["case"]["outer_coordinate"]]
    )
    coordinates = sorted(
        {
            *np.linspace(
                lower, upper, DYNAMIC_COARSE_POINTS
            ).tolist(),
            base,
        }
    )
    state_cache: dict[float, dict[str, Any]] = {}

    def evaluate(coordinate: float, steps: int) -> dict[str, Any]:
        key = float(coordinate)
        cached = state_cache.get(key)
        if cached is not None and int(cached["topology_steps"]) >= steps:
            return cached
        state = winding_state(problem, key, steps)
        state_cache[key] = state
        return state

    coarse_states = [
        evaluate(coordinate, DYNAMIC_TOPOLOGY_STEPS)
        for coordinate in coordinates
    ]
    transition_brackets: list[dict[str, Any]] = []
    for left_index in range(len(coordinates) - 1):
        left = float(coordinates[left_index])
        right = float(coordinates[left_index + 1])
        left_state = coarse_states[left_index]
        right_state = coarse_states[left_index + 1]
        if state_key(left_state) == state_key(right_state):
            continue
        original_left = left
        original_right = right
        for _ in range(DYNAMIC_BISECTION_STEPS):
            midpoint = 0.5 * (left + right)
            midpoint_state = evaluate(
                midpoint, DYNAMIC_TOPOLOGY_STEPS
            )
            if state_key(midpoint_state) == state_key(left_state):
                left = midpoint
                left_state = midpoint_state
            else:
                right = midpoint
                right_state = midpoint_state
        transition_brackets.append(
            {
                "left": left,
                "right": right,
                "center": 0.5 * (left + right),
                "width": right - left,
                "left_state": state_key(left_state),
                "right_state": state_key(right_state),
                "coarse_left": original_left,
                "coarse_right": original_right,
            }
        )
    boundaries = [
        lower,
        *[
            float(row["center"]) for row in transition_brackets
        ],
        upper,
    ]
    boundaries = sorted(set(boundaries))
    rows: list[dict[str, Any]] = []
    representative_suffix, reciprocal_suffix, source_delta = (
        source_winding_delta(problem)
    )
    for interval_index in range(len(boundaries) - 1):
        interval_lower = float(boundaries[interval_index])
        interval_upper = float(boundaries[interval_index + 1])
        midpoint = 0.5 * (interval_lower + interval_upper)
        state = evaluate(midpoint, DYNAMIC_CONFIRMATION_STEPS)
        dynamic_delta = int(state["dynamic_delta"])
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
                "state_u": int(state["u"]),
                "state_v": int(state["v"]),
                "representative_suffix": representative_suffix,
                "reciprocal_suffix": reciprocal_suffix,
                "source_winding_delta": source_delta,
                "dynamic_winding_delta": dynamic_delta,
                "dynamic_multiplier": dynamic_delta / source_delta,
                "maximum_pair_projective_step": state[
                    "maximum_pair_projective_step"
                ],
                "maximum_reciprocal_product_residual": state[
                    "maximum_reciprocal_product_residual"
                ],
                "minimum_alternate_branch_separation": state[
                    "minimum_alternate_branch_separation"
                ],
                "topology_steps": state["topology_steps"],
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
    base_row = next(
        row
        for row in rows
        if float(row["interval_lower"])
        <= base
        <= float(row["interval_upper"])
    )
    expected = {
        "u": int(problem["case"]["expected_u_winding"]),
        "v": int(problem["case"]["expected_v_winding"]),
    }
    if bool(problem["job"].get("require_source_state", True)) and (
        int(base_row["state_u"]),
        int(base_row["state_v"]),
    ) != (expected["u"], expected["v"]):
        raise RuntimeError(
            f"dynamic interval misses source state for "
            f"{problem['job']['job_id']}"
        )
    return rows


def winding_cache_contract(
    manifest: dict[str, Any],
) -> dict[str, Any]:
    return {
        "marker": MARKER,
        "revision": REVISION,
        "manifest_hash": manifest["manifest_hash"],
        "dynamic_topology_steps": DYNAMIC_TOPOLOGY_STEPS,
        "dynamic_confirmation_steps": DYNAMIC_CONFIRMATION_STEPS,
        "dynamic_coarse_points": DYNAMIC_COARSE_POINTS,
        "dynamic_bisection_steps": DYNAMIC_BISECTION_STEPS,
        "job_hashes": sorted(
            job["job_input_hash"] for job in manifest["jobs"]
        ),
    }


def build_dynamic_winding_intervals(
    problems_by_epsilon: dict[str, list[dict[str, Any]]],
    manifest: dict[str, Any],
) -> tuple[list[dict[str, Any]], bool]:
    contract = winding_cache_contract(manifest)
    if WINDING_INTERVAL_CACHE.exists():
        cached = read_json(WINDING_INTERVAL_CACHE)
        if cached.get("contract") == contract:
            rows = list(cached["rows"])
            write_csv(WINDING_INTERVAL_ROWS, rows)
            return rows, True
    rows: list[dict[str, Any]] = []
    for epsilon_id in EPSILON_IDS:
        for problem in problems_by_epsilon[epsilon_id]:
            rows.extend(derive_problem_winding_intervals(problem))
    payload = {"contract": contract, "rows": rows}
    atomic_json(WINDING_INTERVAL_CACHE, payload)
    write_csv(WINDING_INTERVAL_ROWS, rows)
    return rows, False


def interval_rows_by_job(
    rows: list[dict[str, Any]],
) -> dict[str, list[dict[str, Any]]]:
    grouped: defaultdict[str, list[dict[str, Any]]] = defaultdict(
        list
    )
    for row in rows:
        grouped[str(row["job_id"])].append(row)
    for job_rows in grouped.values():
        job_rows.sort(key=lambda row: float(row["interval_lower"]))
    return dict(grouped)


def interval_for_coordinate(
    problem: dict[str, Any],
    coordinate: float,
    intervals_by_job: dict[str, list[dict[str, Any]]],
) -> dict[str, Any]:
    rows = intervals_by_job[problem["job"]["job_id"]]
    for index, row in enumerate(rows):
        lower = float(row["interval_lower"])
        upper = float(row["interval_upper"])
        if lower <= coordinate < upper or (
            index == len(rows) - 1 and coordinate <= upper
        ):
            return row
    raise RuntimeError(
        f"coordinate {coordinate} is outside dynamic intervals for "
        f"{problem['job']['job_id']}"
    )


def dynamic_component_contribution(
    problem: dict[str, Any],
    coordinate: float,
    intervals_by_job: dict[str, list[dict[str, Any]]],
) -> complex:
    interval = interval_for_coordinate(
        problem, coordinate, intervals_by_job
    )
    multiplier = float(interval["dynamic_multiplier"])
    if multiplier == 0.0:
        return 0.0j
    return multiplier * M5237.component_contribution(
        problem, coordinate
    )


def owner_surface_values(
    problem: dict[str, Any], coordinate: complex
) -> dict[str, complex]:
    if problem["job"]["owner_summand"] == "endpoint_subtraction":
        return M5238.endpoint_surface_values(problem, coordinate)
    return M5237.surface_values(problem, coordinate)


def scan_problem(
    problem: dict[str, Any],
) -> tuple[
    dict[str, list[complex]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
]:
    endpoint = (
        problem["job"]["owner_summand"] == "endpoint_subtraction"
    )
    values, scan_rows = (
        M5238.scan_surfaces(problem)
        if endpoint
        else M5237.scan_surfaces(problem)
    )
    poles = (
        M5238.locate_geometric_roots(problem, values)
        if endpoint
        else M5237.locate_geometric_roots(problem, values)
    )
    for pole in poles:
        pole["pole_id"] = (
            f"{problem['component_id']}_{pole['pole_id']}"
        )
    topology_rows = M5237.topology_audit(problem, poles)
    for row in (*scan_rows, *poles, *topology_rows):
        row["epsilon_id"] = problem["job"]["epsilon_id"]
        row["owner_summand"] = problem["job"]["owner_summand"]
    return values, scan_rows, poles, topology_rows


def fit_full_component_residues(
    problem: dict[str, Any],
    poles: list[dict[str, Any]],
    global_centers: list[float],
    intervals_by_job: dict[str, list[dict[str, Any]]],
) -> list[dict[str, Any]]:
    active = [row for row in poles if row["causal_family_active"]]
    rows: list[dict[str, Any]] = []
    lower = float(problem["job"]["scan_minimum"])
    upper = float(problem["job"]["scan_maximum"])
    for pole in active:
        center = float(pole["real_axis_center"])
        nearest = min(
            (
                abs(center - other)
                for other in global_centers
                if abs(center - other) > 1.0e-10
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
                f"insufficient matched-event fit radius at {center}"
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
                (-1.0, -0.5, -0.2, -0.1, 0.1, 0.2, 0.5, 1.0)
            )
            contributions: list[complex] = []
            numerators: list[complex] = []
            for offset in offsets:
                coordinate = center + float(offset)
                contribution = dynamic_component_contribution(
                    problem, coordinate, intervals_by_job
                )
                channel = owner_surface_values(
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
                "epsilon_id": problem["job"]["epsilon_id"],
                "pole_id": pole["pole_id"],
                "component_id": problem["component_id"],
                "family": problem["case"]["family"],
                "owner_summand": problem["job"]["owner_summand"],
                "surface_id": surface_id,
                "center": center,
                "pole_real": complex_pole.real,
                "pole_imaginary": complex_pole.imag,
                "fit_radius": radius,
                "nearest_event_pole_distance": nearest,
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


def merged_active_topology(
    problems: list[dict[str, Any]],
    coordinate: float,
    intervals_by_job: dict[str, list[dict[str, Any]]],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    merged = copy.deepcopy(problems[0]["topology"])
    for chamber in merged["chambers"]:
        chamber["surface_crossings"] = []
    active: list[dict[str, Any]] = []
    for problem in problems:
        interval = interval_for_coordinate(
            problem, coordinate, intervals_by_job
        )
        component_topology = M5237.updated_component_topology(
            problem, coordinate
        )
        cycle_active, _ = M5237.component_cycle_state(
            problem, coordinate, component_topology
        )
        if not cycle_active:
            continue
        active.append(problem)
        for chamber_index, chamber in enumerate(
            component_topology["chambers"]
        ):
            for crossing in chamber["surface_crossings"]:
                suffix = crossing["representing_pairs"][0][0].rsplit(
                    "_", 1
                )[-1]
                crossing["winding_correction"] = int(
                    interval[f"state_{suffix}"]
                )
            merged["chambers"][chamber_index][
                "surface_crossings"
            ].extend(copy.deepcopy(chamber["surface_crossings"]))
    return merged, active


def closure_audit(
    problems_by_epsilon: dict[str, list[dict[str, Any]]],
    matches: list[dict[str, Any]],
    intervals_by_job: dict[str, list[dict[str, Any]]],
) -> list[dict[str, Any]]:
    contract = source_contract()
    event = source_event(contract)
    rows: list[dict[str, Any]] = []
    for epsilon_id in EPSILON_IDS:
        problems = problems_by_epsilon[epsilon_id]
        topology = read_json(
            M5231.topology_path(contract, TARGET_SEED, epsilon_id)
        )
        parent_families, _ = M5231.safe_family_contributions(
            event, topology
        )
        component_families: defaultdict[str, complex] = defaultdict(
            complex
        )
        base_coordinate = float(event[OUTER_COORDINATE])
        for problem in problems:
            component_families[problem["case"]["family"]] += (
                dynamic_component_contribution(
                    problem, base_coordinate, intervals_by_job
                )
            )
        all_families = set(parent_families) | set(component_families)
        for family in sorted(all_families):
            parent = complex(parent_families.get(family, 0.0j))
            reconstructed = complex(
                component_families.get(family, 0.0j)
            )
            residual = reconstructed - parent
            relative = abs(residual) / max(
                abs(parent), abs(reconstructed), 1.0
            )
            rows.append(
                {
                    "audit_type": "BASE_SOURCE_FAMILY",
                    "epsilon_id": epsilon_id,
                    "coordinate": base_coordinate,
                    "family": family,
                    "active_component_count": sum(
                        problem["case"]["family"] == family
                        for problem in problems
                    ),
                    "parent_real": parent.real,
                    "parent_imaginary": parent.imag,
                    "reconstructed_real": reconstructed.real,
                    "reconstructed_imaginary": reconstructed.imag,
                    "residual_magnitude": abs(residual),
                    "relative_closure_residual": relative,
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
            )
        parent_total = sum(parent_families.values(), 0.0j)
        reconstructed_total = sum(
            component_families.values(), 0.0j
        )
        total_residual = reconstructed_total - parent_total
        rows.append(
            {
                "audit_type": "BASE_SOURCE_TOTAL",
                "epsilon_id": epsilon_id,
                "coordinate": base_coordinate,
                "family": "ALL_SAFE_FAMILIES",
                "active_component_count": len(problems),
                "parent_real": parent_total.real,
                "parent_imaginary": parent_total.imag,
                "reconstructed_real": reconstructed_total.real,
                "reconstructed_imaginary": reconstructed_total.imag,
                "residual_magnitude": abs(total_residual),
                "relative_closure_residual": (
                    abs(total_residual)
                    / max(
                        abs(parent_total),
                        abs(reconstructed_total),
                        1.0,
                    )
                ),
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
        for coordinate in WITNESS_COORDINATES:
            varied_event = dict(event)
            varied_event[OUTER_COORDINATE] = float(coordinate)
            merged, active = merged_active_topology(
                problems, float(coordinate), intervals_by_job
            )
            parent_dynamic = (
                sum(
                    M5231.safe_family_contributions(
                        varied_event, merged
                    )[0].values(),
                    0.0j,
                )
                if active
                else 0.0j
            )
            reconstructed_dynamic = sum(
                (
                    dynamic_component_contribution(
                        problem,
                        float(coordinate),
                        intervals_by_job,
                    )
                    for problem in problems
                ),
                0.0j,
            )
            residual = reconstructed_dynamic - parent_dynamic
            rows.append(
                {
                    "audit_type": "DYNAMIC_WITNESS_TOTAL",
                    "epsilon_id": epsilon_id,
                    "coordinate": coordinate,
                    "family": "ALL_ACTIVE_MATERIAL_COMPONENTS",
                    "active_component_count": len(active),
                    "parent_real": parent_dynamic.real,
                    "parent_imaginary": parent_dynamic.imag,
                    "reconstructed_real": reconstructed_dynamic.real,
                    "reconstructed_imaginary": reconstructed_dynamic.imag,
                    "residual_magnitude": abs(residual),
                    "relative_closure_residual": (
                        abs(residual)
                        / max(
                            abs(parent_dynamic),
                            abs(reconstructed_dynamic),
                            1.0,
                        )
                    ),
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
            )
    stored_rows = [
        row
        for row in read_csv(FAMILY_SOURCE)
        if row["tranche"] == TARGET_TRANCHE
        and int(row["seed"]) == TARGET_SEED
    ]
    stored = {
        row["family"]: complex(
            float(row["A00_family_real"]),
            float(row["A00_family_imaginary"]),
        )
        for row in stored_rows
    }
    grouped: defaultdict[str, dict[str, complex]] = defaultdict(
        lambda: {epsilon_id: 0.0j for epsilon_id in EPSILON_IDS}
    )
    for match in matches:
        for epsilon_id in EPSILON_IDS:
            grouped[match["family"]][epsilon_id] += match[epsilon_id][
                "raw_contribution"
            ]
    for family in sorted(set(stored) | set(grouped)):
        predicted = (
            M5231.PHYSICAL_A00_WEIGHT
            * M5231.KERNEL_MULTIPLIER
            * (
                2.0 * grouped[family]["E020"]
                - grouped[family]["E040"]
            )
        )
        observed = stored.get(family, 0.0j)
        residual = predicted - observed
        rows.append(
            {
                "audit_type": "REGULATOR_TO_STORED_FAMILY",
                "epsilon_id": "E040_E020",
                "coordinate": float(event[OUTER_COORDINATE]),
                "family": family,
                "active_component_count": sum(
                    match["family"] == family for match in matches
                ),
                "parent_real": observed.real,
                "parent_imaginary": observed.imag,
                "reconstructed_real": predicted.real,
                "reconstructed_imaginary": predicted.imag,
                "residual_magnitude": abs(residual),
                "relative_closure_residual": (
                    abs(residual)
                    / max(abs(observed), abs(predicted), 1.0)
                ),
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    return rows


def gauss_integral(
    function: Callable[[float], complex],
    lower: float,
    upper: float,
    order: int,
) -> complex:
    if upper <= lower:
        return 0.0j
    nodes, weights = np.polynomial.legendre.leggauss(order)
    half_width = 0.5 * (upper - lower)
    midpoint = 0.5 * (upper + lower)
    coordinates = half_width * nodes + midpoint
    values = np.asarray(
        [function(float(coordinate)) for coordinate in coordinates],
        dtype=np.complex128,
    )
    return complex(np.sum(half_width * weights * values))


def complement_segments(
    groups: list[dict[str, Any]],
    lower: float,
    upper: float,
) -> list[tuple[float, float]]:
    segments: list[tuple[float, float]] = []
    cursor = lower
    for group in groups:
        group_lower = float(group["lower"])
        group_upper = float(group["upper"])
        if group_lower > cursor:
            segments.append((cursor, group_lower))
        cursor = max(cursor, group_upper)
    if cursor < upper:
        segments.append((cursor, upper))
    return segments


def integrate_matched_event(
    problems: list[dict[str, Any]],
    fits: list[dict[str, Any]],
    epsilon_id: str,
    intervals_by_job: dict[str, list[dict[str, Any]]],
) -> tuple[list[dict[str, Any]], dict[int, dict[str, complex]], dict[str, Any]]:
    accepted = [row for row in fits if bool(row["fit_passed"])]
    groups = M5237.patch_groups(
        accepted, SCAN_MINIMUM, SCAN_MAXIMUM
    )
    transition_boundaries = sorted(
        {
            float(row["interval_upper"])
            for problem in problems
            for row in intervals_by_job[problem["job"]["job_id"]][:-1]
        }
    )
    partition_boundaries = sorted(
        {
            SCAN_MINIMUM,
            SCAN_MAXIMUM,
            *transition_boundaries,
            *[
                float(group[side])
                for group in groups
                for side in ("lower", "upper")
            ],
        }
    )
    segments = [
        (
            float(partition_boundaries[index]),
            float(partition_boundaries[index + 1]),
        )
        for index in range(len(partition_boundaries) - 1)
    ]
    cache: dict[float, complex] = {}
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
        for fit in accepted
    ]

    def total_integrand(coordinate: float) -> complex:
        key = float(coordinate)
        if key not in cache:
            cache[key] = sum(
                (
                    dynamic_component_contribution(
                        problem, key, intervals_by_job
                    )
                    for problem in problems
                ),
                0.0j,
            )
        return cache[key]

    def regular_integrand(coordinate: float) -> complex:
        singular = sum(
            (
                residue / (coordinate - pole)
                for pole, residue in singular_terms
            ),
            0.0j,
        )
        return total_integrand(coordinate) - singular

    def analytic_singular(lower: float, upper: float) -> complex:
        return sum(
            (
                residue
                * (
                    cmath.log(upper - pole)
                    - cmath.log(lower - pole)
                )
                for pole, residue in singular_terms
            ),
            0.0j,
        )

    rows: list[dict[str, Any]] = []
    totals: dict[int, dict[str, complex]] = {}
    for order in QUADRATURE_ORDERS:
        raw_total = 0.0j
        subtracted_total = 0.0j
        for segment_index, (lower, upper) in enumerate(
            segments, start=1
        ):
            midpoint = 0.5 * (lower + upper)
            containing_group = next(
                (
                    group
                    for group in groups
                    if float(group["lower"]) <= midpoint
                    <= float(group["upper"])
                ),
                None,
            )
            segment_type = (
                "SINGULAR_PATCH"
                if containing_group is not None
                else "REGULAR_COMPLEMENT"
            )
            raw = gauss_integral(
                total_integrand, lower, upper, order
            )
            remainder = gauss_integral(
                regular_integrand, lower, upper, order
            )
            analytic = analytic_singular(lower, upper)
            subtracted = remainder + analytic
            raw_total += raw
            subtracted_total += subtracted
            rows.append(
                {
                    "epsilon_id": epsilon_id,
                    "quadrature_order": order,
                    "segment_type": segment_type,
                    "segment_id": f"S{segment_index:02d}",
                    "lower": lower,
                    "upper": upper,
                    "segment_length": upper - lower,
                    "pole_ids": "|".join(
                        fit["pole_id"] for fit in accepted
                    ),
                    "pole_count": len(accepted),
                    "raw_integral_real": raw.real,
                    "raw_integral_imaginary": raw.imag,
                    "regular_remainder_real": remainder.real,
                    "regular_remainder_imaginary": remainder.imag,
                    "analytic_singular_real": analytic.real,
                    "analytic_singular_imaginary": analytic.imag,
                    "subtracted_integral_real": subtracted.real,
                    "subtracted_integral_imaginary": subtracted.imag,
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
            )
        totals[order] = {
            "raw": complex(raw_total),
            "subtracted": complex(subtracted_total),
        }
    covered_length = sum(upper - lower for lower, upper in segments)
    coverage = {
        "epsilon_id": epsilon_id,
        "patch_group_count": len(groups),
        "segment_count": len(segments),
        "topology_transition_count": len(transition_boundaries),
        "accepted_fit_count": len(accepted),
        "domain_length": SCAN_MAXIMUM - SCAN_MINIMUM,
        "covered_length": covered_length,
        "coverage_residual": abs(
            covered_length - (SCAN_MAXIMUM - SCAN_MINIMUM)
        ),
        "integrand_evaluation_count": len(cache),
    }
    return rows, totals, coverage


def extrapolation_rows(
    regulator_totals: dict[str, dict[int, dict[str, complex]]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for epsilon_id in EPSILON_IDS:
        for order in QUADRATURE_ORDERS:
            values = regulator_totals[epsilon_id][order]
            rows.append(
                {
                    "row_type": "REGULATOR_INTEGRAL",
                    "epsilon_id": epsilon_id,
                    "quadrature_order": order,
                    "raw_integral_real": values["raw"].real,
                    "raw_integral_imaginary": values["raw"].imag,
                    "subtracted_integral_real": values[
                        "subtracted"
                    ].real,
                    "subtracted_integral_imaginary": values[
                        "subtracted"
                    ].imag,
                    "kernel_multiplier": M5231.KERNEL_MULTIPLIER,
                    "physical_A00_weight": M5231.PHYSICAL_A00_WEIGHT,
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
            )
    physical: dict[int, dict[str, complex]] = {}
    multiplier = (
        M5231.PHYSICAL_A00_WEIGHT * M5231.KERNEL_MULTIPLIER
    )
    for order in QUADRATURE_ORDERS:
        raw = multiplier * (
            2.0 * regulator_totals["E020"][order]["raw"]
            - regulator_totals["E040"][order]["raw"]
        )
        subtracted = multiplier * (
            2.0 * regulator_totals["E020"][order]["subtracted"]
            - regulator_totals["E040"][order]["subtracted"]
        )
        physical[order] = {
            "raw": complex(raw),
            "subtracted": complex(subtracted),
        }
    reference = physical[QUADRATURE_ORDERS[-1]]["subtracted"]
    denominator = max(abs(reference), 1.0)
    errors: dict[int, dict[str, float]] = {}
    for order in QUADRATURE_ORDERS:
        raw_error = abs(physical[order]["raw"] - reference) / denominator
        subtracted_error = (
            abs(physical[order]["subtracted"] - reference)
            / denominator
        )
        errors[order] = {
            "raw": raw_error,
            "subtracted": subtracted_error,
        }
        rows.append(
            {
                "row_type": "PHYSICAL_RICHARDSON_SLICE",
                "epsilon_id": "2E020_MINUS_E040",
                "quadrature_order": order,
                "raw_integral_real": physical[order]["raw"].real,
                "raw_integral_imaginary": physical[order]["raw"].imag,
                "subtracted_integral_real": physical[order][
                    "subtracted"
                ].real,
                "subtracted_integral_imaginary": physical[order][
                    "subtracted"
                ].imag,
                "raw_relative_error_to_order512_subtracted": raw_error,
                "subtracted_relative_error_to_order512_subtracted": (
                    subtracted_error
                ),
                "kernel_multiplier": M5231.KERNEL_MULTIPLIER,
                "physical_A00_weight": M5231.PHYSICAL_A00_WEIGHT,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    summary = {
        "reference_order": QUADRATURE_ORDERS[-1],
        "physical_subtracted_reference": complex_row(reference),
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
    return rows, summary


def validation_rows(
    manifest: dict[str, Any],
    matches: list[dict[str, Any]],
    closure_rows: list[dict[str, Any]],
    poles: list[dict[str, Any]],
    fits: list[dict[str, Any]],
    winding_intervals: list[dict[str, Any]],
    intervals_by_job: dict[str, list[dict[str, Any]]],
    problem_by_job: dict[str, dict[str, Any]],
    coverage_rows: list[dict[str, Any]],
    summary: dict[str, Any],
    formal_after: str,
    elapsed: float,
) -> list[dict[str, Any]]:
    base_source = [
        row
        for row in closure_rows
        if row["audit_type"].startswith("BASE_SOURCE")
    ]
    dynamic = [
        row
        for row in closure_rows
        if row["audit_type"] == "DYNAMIC_WITNESS_TOTAL"
    ]
    stored = [
        row
        for row in closure_rows
        if row["audit_type"] == "REGULATOR_TO_STORED_FAMILY"
    ]
    active_poles = [
        row for row in poles if bool(row["causal_family_active"])
    ]
    pole_gate_rows = []
    for pole in poles:
        problem = problem_by_job[pole["job_id"]]
        interval = interval_for_coordinate(
            problem,
            float(pole["real_axis_center"]),
            intervals_by_job,
        )
        pole_gate_rows.append(
            {
                "causal_active": bool(pole["causal_family_active"]),
                "dynamic_multiplier": float(
                    interval["dynamic_multiplier"]
                ),
            }
        )
    checks = [
        (
            "SOURCE_PATHS_EXIST",
            all(
                Path(row["path"]).exists()
                for row in manifest["source_files"]
            ),
            len(manifest["source_files"]),
            "all manifest source paths exist",
        ),
        (
            "SAFE_COMPONENT_COUNT",
            len(matches) == EXPECTED_SAFE_COMPONENT_COUNT,
            len(matches),
            EXPECTED_SAFE_COMPONENT_COUNT,
        ),
        (
            "MATERIAL_COMPONENT_COUNT",
            sum(bool(row["material"]) for row in matches)
            == EXPECTED_MATERIAL_COMPONENT_COUNT,
            sum(bool(row["material"]) for row in matches),
            EXPECTED_MATERIAL_COMPONENT_COUNT,
        ),
        (
            "REGULATOR_MATCH_RESIDUAL",
            max(
                row["match_projective_residual"] for row in matches
            )
            <= MATCH_PROJECTIVE_LIMIT,
            max(
                row["match_projective_residual"] for row in matches
            ),
            MATCH_PROJECTIVE_LIMIT,
        ),
        (
            "BASE_SOURCE_CLOSURE",
            max(
                float(row["relative_closure_residual"])
                for row in base_source
            )
            <= SOURCE_CLOSURE_LIMIT,
            max(
                float(row["relative_closure_residual"])
                for row in base_source
            ),
            SOURCE_CLOSURE_LIMIT,
        ),
        (
            "DYNAMIC_WITNESS_CLOSURE",
            max(
                float(row["relative_closure_residual"])
                for row in dynamic
            )
            <= DYNAMIC_CLOSURE_LIMIT,
            max(
                float(row["relative_closure_residual"])
                for row in dynamic
            ),
            DYNAMIC_CLOSURE_LIMIT,
        ),
        (
            "DYNAMIC_WINDING_INTERVAL_COVERAGE",
            all(
                abs(
                    sum(
                        float(row["interval_upper"])
                        - float(row["interval_lower"])
                        for row in job_rows
                    )
                    - (SCAN_MAXIMUM - SCAN_MINIMUM)
                )
                <= 2.0e-12
                for job_rows in intervals_by_job.values()
            ),
            len(winding_intervals),
            "complete non-overlapping interval cover per job",
        ),
        (
            "DYNAMIC_WINDING_TRACK_RESOLUTION",
            max(
                float(row["maximum_pair_projective_step"])
                for row in winding_intervals
            )
            <= DYNAMIC_PROJECTIVE_STEP_LIMIT,
            max(
                float(row["maximum_pair_projective_step"])
                for row in winding_intervals
            ),
            DYNAMIC_PROJECTIVE_STEP_LIMIT,
        ),
        (
            "POLE_CAUSAL_GATE_CONSISTENT",
            all(
                (
                    row["causal_active"]
                    and abs(row["dynamic_multiplier"] - 1.0)
                    <= 1.0e-12
                )
                or (
                    not row["causal_active"]
                    and abs(row["dynamic_multiplier"]) <= 1.0e-12
                )
                for row in pole_gate_rows
            ),
            "|".join(
                f"{int(row['causal_active'])}:{row['dynamic_multiplier']:.3g}"
                for row in pole_gate_rows
            ),
            "active:1 and inactive:0",
        ),
        (
            "STORED_FAMILY_REGULATOR_CLOSURE",
            max(
                float(row["relative_closure_residual"])
                for row in stored
            )
            <= STORED_FAMILY_CLOSURE_LIMIT,
            max(
                float(row["relative_closure_residual"])
                for row in stored
            ),
            STORED_FAMILY_CLOSURE_LIMIT,
        ),
        (
            "ACTIVE_POLES_FITTED",
            len(fits) == len(active_poles)
            and all(bool(row["fit_passed"]) for row in fits),
            f"{len(fits)}/{len(active_poles)}",
            "all active geometric poles",
        ),
        (
            "REGULAR_DOMAIN_COVERED",
            max(
                float(row["coverage_residual"])
                for row in coverage_rows
            )
            <= 2.0e-12,
            max(
                float(row["coverage_residual"])
                for row in coverage_rows
            ),
            2.0e-12,
        ),
        (
            "LOW_ORDER_SUBTRACTED_CONVERGENCE",
            summary["low_order_subtracted_relative_error"]
            <= LOW_ORDER_SUBTRACTED_RELATIVE_ERROR_LIMIT,
            summary["low_order_subtracted_relative_error"],
            LOW_ORDER_SUBTRACTED_RELATIVE_ERROR_LIMIT,
        ),
        (
            "MID_ORDER_SUBTRACTED_CONVERGENCE",
            summary["mid_order_subtracted_relative_error"]
            <= MID_ORDER_SUBTRACTED_RELATIVE_ERROR_LIMIT,
            summary["mid_order_subtracted_relative_error"],
            MID_ORDER_SUBTRACTED_RELATIVE_ERROR_LIMIT,
        ),
        (
            "SUBTRACTION_IMPROVES_LOW_ORDER",
            summary["low_order_improvement_factor"]
            >= MINIMUM_LOW_ORDER_IMPROVEMENT,
            summary["low_order_improvement_factor"],
            MINIMUM_LOW_ORDER_IMPROVEMENT,
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
            "checkpoint": 5239,
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
    matches: list[dict[str, Any]],
    closure_rows: list[dict[str, Any]],
    poles: list[dict[str, Any]],
    fits: list[dict[str, Any]],
    winding_intervals: list[dict[str, Any]],
    winding_cache_hit: bool,
    coverage_rows: list[dict[str, Any]],
    summary: dict[str, Any],
    validations: list[dict[str, Any]],
    elapsed: float,
) -> str:
    material = [row for row in matches if row["material"]]
    direct_count = sum(
        row["owner_summand"] == "direct_five_point"
        for row in material
    )
    endpoint_count = sum(
        row["owner_summand"] == "endpoint_subtraction"
        for row in material
    )
    active_poles = [
        row for row in poles if bool(row["causal_family_active"])
    ]
    source_max = max(
        float(row["relative_closure_residual"])
        for row in closure_rows
        if row["audit_type"].startswith("BASE_SOURCE")
    )
    dynamic_max = max(
        float(row["relative_closure_residual"])
        for row in closure_rows
        if row["audit_type"] == "DYNAMIC_WITNESS_TOTAL"
    )
    stored_max = max(
        float(row["relative_closure_residual"])
        for row in closure_rows
        if row["audit_type"] == "REGULATOR_TO_STORED_FAMILY"
    )
    reference = complex_value(summary["physical_subtracted_reference"])
    validation_passed = all(bool(row["passed"]) for row in validations)
    lines = [
        "# 5239 — Matched-event A00 regular complement and regulator extrapolation",
        "",
        "## Scope",
        "",
        (
            f"This checkpoint selects source event `S{TARGET_SEED}_N0000` "
            f"and integrates its conditional `{OUTER_COORDINATE}` slice. "
            "Unlike the separate 5237/5238 method pools, the direct and "
            "endpoint-owned summands now coexist inside one event integrand."
        ),
        "",
        "## Why this event",
        "",
        (
            f"The source topology contains {len(matches)} safe reciprocal "
            f"components. {len(material)} are nonzero at the parent event: "
            f"{direct_count} direct and {endpoint_count} endpoint-owned. "
            "Along `soft_cosine`, both owner sectors contain a causally "
            "active pole, so the test exercises a genuine mixed singular "
            "slice rather than combining disconnected convergence scores."
        ),
        "",
        "## Derived event contract",
        "",
        "For regulator $\\epsilon$, the matched conditional integrand is",
        "",
        "$$",
        "\\mathcal I_\\epsilon(x)=\\sum_{c\\in\\mathcal C_{\\rm mat}}"
        "\\Delta w_c\\,\\sigma_c\\,"
        "\\frac{C_c(x)}{r_c(x)z_c(x)J_c(x)}.",
        "$$",
        "",
        (
            "Every term is inherited from the parent reciprocal topology. "
            "No event-level closure coefficient is introduced. The six "
            "material components reproduce the full parent safe-family "
            f"integrand at the source point with maximum relative residual "
            f"`{source_max:.6e}`. Dynamic merged-topology witnesses close "
            f"to `{dynamic_max:.6e}`."
        ),
        "",
        (
            "The source winding cannot be frozen over the full outer "
            "domain. The branch-aware target homotopy is therefore "
            "evaluated on a bounded coarse grid, each integer transition "
            "is bisected, and the resulting piecewise winding difference "
            "multiplies the local residue. This removes two geometrically "
            "real but causally inactive poles per regulator rather than "
            "silently integrating their fixed-source continuation."
        ),
        "",
        "For each causally active outer pole $p_j$,",
        "",
        "$$",
        "\\mathcal I_\\epsilon(x)="
        "\\sum_j\\frac{R_j}{x-p_j}+\\mathcal I_{\\epsilon,\\rm reg}(x),"
        "$$",
        "",
        (
            "Every topology-resolved segment is evaluated as the globally "
            "regularized remainder plus "
            "$R_j[\\log(b-p_j)-\\log(a-p_j)]$. Pole-patch edges and all "
            "integer-winding transitions are explicit segment boundaries. "
            "Those segments cover the complete source domain without "
            "overlap."
        ),
        "",
        "The inherited two-level physical slice is",
        "",
        "$$",
        "I_{A00}^{(2)}=w_{A00}K\\left(2I_{E020}-I_{E040}\\right),"
        "$$",
        "",
        (
            f"with `w_A00={M5231.PHYSICAL_A00_WEIGHT}` and "
            f"`K={M5231.KERNEL_MULTIPLIER:.16g}`. Component matching "
            "reconstructs the stored parent family decomposition with "
            f"maximum relative residual `{stored_max:.6e}`."
        ),
        "",
        "## Numerical result",
        "",
        f"- Material regulator jobs: `{manifest['job_count']}`.",
        f"- Geometric poles: `{len(poles)}`.",
        f"- Causally active poles: `{len(active_poles)}`.",
        (
            f"- Dynamic winding intervals: `{len(winding_intervals)}` "
            f"(`cache_hit={str(winding_cache_hit).lower()}`)."
        ),
        f"- Accepted full-component residue fits: `{sum(bool(row['fit_passed']) for row in fits)}/{len(fits)}`.",
        (
            "- Domain coverage residuals: `"
            + "`, `".join(
                f"{row['epsilon_id']}={float(row['coverage_residual']):.3e}"
                for row in coverage_rows
            )
            + "`."
        ),
        (
            "- Order-32 raw relative error: "
            f"`{summary['low_order_raw_relative_error']:.12g}`."
        ),
        (
            "- Order-32 subtracted relative error: "
            f"`{summary['low_order_subtracted_relative_error']:.12g}`."
        ),
        (
            "- Order-128 subtracted relative error: "
            f"`{summary['mid_order_subtracted_relative_error']:.12g}`."
        ),
        (
            "- Low-order improvement factor: "
            f"`{summary['low_order_improvement_factor']:.12g}`."
        ),
        (
            "- Order-512 subtracted two-level slice: "
            f"`{reference.real:.16g} {reference.imag:+.16g} i`."
        ),
        f"- Runtime: `{elapsed:.3f} s`.",
        "",
        "## Decision",
        "",
        (
            "`ADOPT_MATCHED_EVENT_REGULAR_COMPLEMENT_AND_TWO_LEVEL_"
            "REGULATOR_EXTRAPOLATION`"
            if validation_passed
            else "`HOLD_MATCHED_EVENT_METHOD_PENDING_FAILED_GATE`"
        ),
        "",
        (
            "This closes the first event-level direct-plus-endpoint "
            "conditional A00 integration contract. It replaces the prior "
            "sum of independent method pools with one source-matched "
            "integrand, explicit regular complement, and inherited "
            "E040/E020 extrapolation."
        ),
        "",
        "## Claim boundary",
        "",
        (
            "The result is **not** a numeric UV coefficient, local-GR "
            "derivation, or full-MTS result. It is one-dimensional "
            "conditional slice. A physical coefficient still requires "
            "the remaining outer integrations and a source-pool "
            "replication; a third regulator level would independently "
            "test, rather than merely apply, the inherited linear "
            "extrapolation law."
        ),
        "",
        "## Next target",
        "",
        (
            "Promote the matched event contract to nested integration over "
            "the remaining outer coordinates, while carrying the same "
            "component matching, causal-pole subtraction, regular "
            "complement, and regulator checks."
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
    return "\n".join(lines)


def remove_pycache() -> None:
    for path in POST.rglob("__pycache__"):
        shutil.rmtree(path)


def execute() -> dict[str, Any]:
    started = time.perf_counter()
    dry_run = write_manifest_and_dry_run()
    manifest = read_json(MANIFEST_JSON)
    _, matches = build_manifest()
    problems_by_epsilon: dict[str, list[dict[str, Any]]] = {
        epsilon_id: [] for epsilon_id in EPSILON_IDS
    }
    for job in manifest["jobs"]:
        problems_by_epsilon[job["epsilon_id"]].append(
            build_problem(job)
        )
    winding_intervals, winding_cache_hit = (
        build_dynamic_winding_intervals(
            problems_by_epsilon, manifest
        )
    )
    intervals_by_job = interval_rows_by_job(winding_intervals)
    all_scan_rows: list[dict[str, Any]] = []
    all_poles: list[dict[str, Any]] = []
    all_topology_rows: list[dict[str, Any]] = []
    poles_by_job: dict[str, list[dict[str, Any]]] = {}
    problem_by_job: dict[str, dict[str, Any]] = {}
    for epsilon_id in EPSILON_IDS:
        for problem in problems_by_epsilon[epsilon_id]:
            _, scan_rows, poles, topology_rows = scan_problem(problem)
            problem_by_job[problem["job"]["job_id"]] = problem
            poles_by_job[problem["job"]["job_id"]] = poles
            all_scan_rows.extend(scan_rows)
            all_poles.extend(poles)
            all_topology_rows.extend(topology_rows)
    all_fits: list[dict[str, Any]] = []
    for epsilon_id in EPSILON_IDS:
        regulator_poles = [
            row
            for row in all_poles
            if row["epsilon_id"] == epsilon_id
        ]
        global_centers = [
            float(row["real_axis_center"]) for row in regulator_poles
        ]
        for problem in problems_by_epsilon[epsilon_id]:
            all_fits.extend(
                fit_full_component_residues(
                    problem,
                    poles_by_job[problem["job"]["job_id"]],
                    global_centers,
                    intervals_by_job,
                )
            )
    if not all(bool(row["fit_passed"]) for row in all_fits):
        raise RuntimeError("one or more matched-event residue fits failed")
    closure_rows = closure_audit(
        problems_by_epsilon, matches, intervals_by_job
    )
    all_quadrature_rows: list[dict[str, Any]] = []
    regulator_totals: dict[
        str, dict[int, dict[str, complex]]
    ] = {}
    coverage_rows: list[dict[str, Any]] = []
    for epsilon_id in EPSILON_IDS:
        fits = [
            row
            for row in all_fits
            if row["epsilon_id"] == epsilon_id
        ]
        quadrature_rows, totals, coverage = integrate_matched_event(
            problems_by_epsilon[epsilon_id],
            fits,
            epsilon_id,
            intervals_by_job,
        )
        all_quadrature_rows.extend(quadrature_rows)
        regulator_totals[epsilon_id] = totals
        coverage_rows.append(coverage)
    extrapolated_rows, summary = extrapolation_rows(regulator_totals)
    formal_after = tree_digest(FORMAL)
    elapsed = time.perf_counter() - started
    validations = validation_rows(
        manifest,
        matches,
        closure_rows,
        all_poles,
        all_fits,
        winding_intervals,
        intervals_by_job,
        problem_by_job,
        coverage_rows,
        summary,
        formal_after,
        elapsed,
    )
    write_csv(CLOSURE_ROWS, closure_rows)
    write_csv(SCAN_ROWS, all_scan_rows)
    write_csv(POLE_ROWS, all_poles)
    write_csv(TOPOLOGY_ROWS, all_topology_rows)
    write_csv(RESIDUE_ROWS, all_fits)
    write_csv(QUADRATURE_ROWS, all_quadrature_rows)
    write_csv(EXTRAPOLATION_ROWS, extrapolated_rows)
    write_csv(VALIDATION, validations)
    document = render_document(
        manifest,
        matches,
        closure_rows,
        all_poles,
        all_fits,
        winding_intervals,
        winding_cache_hit,
        coverage_rows,
        summary,
        validations,
        elapsed,
    )
    atomic_text(DOCUMENT, document)
    result = {
        "marker": MARKER,
        "revision": REVISION,
        "dry_run": dry_run,
        "manifest_hash": manifest["manifest_hash"],
        "target_event": manifest["target_event"],
        "outer_coordinate": OUTER_COORDINATE,
        "safe_component_count": len(matches),
        "material_component_count": sum(
            bool(row["material"]) for row in matches
        ),
        "job_count": manifest["job_count"],
        "geometric_pole_count": len(all_poles),
        "active_pole_count": sum(
            bool(row["causal_family_active"]) for row in all_poles
        ),
        "accepted_residue_fit_count": sum(
            bool(row["fit_passed"]) for row in all_fits
        ),
        "dynamic_winding_interval_count": len(winding_intervals),
        "dynamic_winding_cache_hit": winding_cache_hit,
        "coverage": coverage_rows,
        "convergence": summary,
        "decision": (
            "ADOPT_MATCHED_EVENT_REGULAR_COMPLEMENT_AND_TWO_LEVEL_"
            "REGULATOR_EXTRAPOLATION"
            if all(bool(row["passed"]) for row in validations)
            else "HOLD_MATCHED_EVENT_METHOD_PENDING_FAILED_GATE"
        ),
        "formalization_workbench_digest": formal_after,
        "elapsed_seconds": elapsed,
        "outputs": [
            str(path)
            for path in (
                MANIFEST_JSON,
                MANIFEST_CSV,
                DRY_RUN,
                COMPONENT_ROWS,
                CLOSURE_ROWS,
                SCAN_ROWS,
                POLE_ROWS,
                TOPOLOGY_ROWS,
                WINDING_INTERVAL_ROWS,
                WINDING_INTERVAL_CACHE,
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
    remove_pycache()
    if not all(bool(row["passed"]) for row in validations):
        failed = [
            row["gate"] for row in validations if not row["passed"]
        ]
        raise RuntimeError(f"5239 validation failed: {failed}")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="write and validate the bounded source manifest only",
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
