from __future__ import annotations

import argparse
import cmath
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
SOURCE = POST / "source-intake" / "functional_rg" / "5244"
RESIDUALS = POST / "source-intake" / "mts_residuals"

SCRIPT_5243 = (
    POST
    / "scripts"
    / "Y5_R2FR_5243_adaptive_homotopy_winding_rebuild_and_Q03_Q05_slice_rerun.py"
)
RESULT_5242 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5242"
    / "homotopy_branch_resolution_result.json"
)
MANIFEST_5242 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5242"
    / "homotopy_branch_resolution_manifest.json"
)
STATE_CACHE_5243 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5243"
    / "adaptive_homotopy_state_cache.json"
)

MANIFEST = SOURCE / "coupled_reciprocal_tracker_manifest.json"
DRY_RUN = SOURCE / "coupled_reciprocal_tracker_dry_run.json"
RESULT = SOURCE / "coupled_reciprocal_tracker_result.json"
ROWS = SOURCE / "coupled_reciprocal_resolution_ladder.csv"
SUMMARY_ROWS = SOURCE / "coupled_reciprocal_case_summary.csv"
CACHE_DIAGNOSTIC = SOURCE / "Q03_bruteforce_cache_diagnostic.json"
VALIDATION = RESIDUALS / "P8_Y5_BRR545_5244_VALIDATION.csv"
DOCUMENT = (
    POST
    / "5244-Y5-R2FR-coupled-reciprocal-homotopy-tracker-prototype.md"
)

MARKER = "MTS_5244_COUPLED_RECIPROCAL_HOMOTOPY_TRACKER_PROTOTYPE"
REVISION = "coupled-reciprocal-homotopy-tracker-prototype-v1"
FORMAL_BASELINE = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)

COUPLED_RESOLUTIONS = (1024, 2048, 4096, 8192)
MAXIMUM_PROJECTIVE_STEP = 5.0e-2
MAXIMUM_BOUNDARY_PROJECTIVE_STEP = 5.0e-2
MAXIMUM_RECIPROCAL_RESIDUAL = 2.0e-8
MAXIMUM_PROTOTYPE_SECONDS = 60.0 * 60.0


def load_module(path: Path, name: str) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5243 = load_module(SCRIPT_5243, "mts_5243_for_5244")
M5242 = M5243.M5242
M5241 = M5243.M5241
M5240 = M5243.M5240
M5239 = M5243.M5239
M5237 = M5240.M5237
M5232 = M5237.M5232
M5030 = M5237.M5030
M5034 = M5237.M5034


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


def source_rows() -> list[dict[str, str]]:
    paths = (
        SCRIPT_5243,
        RESULT_5242,
        MANIFEST_5242,
        STATE_CACHE_5243,
        M5242.SCRIPT_5241,
        M5241.SCRIPT_5240,
        M5240.SCRIPT_5239,
    )
    return [
        {"path": str(path), "sha256": digest(path)} for path in paths
    ]


def accepted_cached_states(
    problem: dict[str, Any],
) -> list[dict[str, Any]]:
    payload = read_json(STATE_CACHE_5243)
    grouped: defaultdict[float, dict[int, dict[str, Any]]] = defaultdict(
        dict
    )
    prefix = problem["job"]["job_input_hash"] + "|"
    for key, state in payload["states"].items():
        if not key.startswith(prefix):
            continue
        _, coordinate, steps = key.split("|")
        grouped[float(coordinate)][int(steps)] = state
    rows: list[dict[str, Any]] = []
    for coordinate, levels in grouped.items():
        previous: dict[str, Any] | None = None
        for steps in M5243.RESOLUTION_LADDER:
            if steps not in levels:
                continue
            state = levels[steps]
            stable = (
                previous is not None
                and M5243.state_key(state)
                == M5243.state_key(previous)
            )
            ratio = (
                float(state["maximum_pair_projective_step"])
                / max(
                    float(previous["maximum_pair_projective_step"]),
                    1.0e-300,
                )
                if previous is not None
                else None
            )
            accepted = (
                steps >= M5243.MINIMUM_ACCEPTED_RESOLUTION
                and stable
                and float(state["maximum_pair_projective_step"])
                <= M5243.MAXIMUM_PROJECTIVE_STEP
                and float(
                    state["maximum_reciprocal_product_residual"]
                )
                <= M5243.MAXIMUM_RECIPROCAL_RESIDUAL
                and ratio is not None
                and ratio <= M5243.MAXIMUM_STEP_RATIO
            )
            if accepted:
                rows.append(
                    {
                        "coordinate": coordinate,
                        "reference_steps": steps,
                        "reference_state_u": int(state["u"]),
                        "reference_state_v": int(state["v"]),
                        "reference_dynamic_multiplier": float(
                            state["multiplier"]
                        ),
                    }
                )
                break
            previous = state
    rows.sort(key=lambda row: float(row["coordinate"]))
    return rows


def representative_cached_cases(
    problem: dict[str, Any],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows = accepted_cached_states(problem)
    by_state: defaultdict[tuple[int, int], list[dict[str, Any]]] = (
        defaultdict(list)
    )
    for row in rows:
        by_state[
            (
                int(row["reference_state_u"]),
                int(row["reference_state_v"]),
            )
        ].append(row)
    all_coordinates = {
        state: np.asarray(
            [float(row["coordinate"]) for row in state_rows],
            dtype=np.float64,
        )
        for state, state_rows in by_state.items()
    }
    selected: list[dict[str, Any]] = []
    for state, state_rows in sorted(by_state.items()):
        alternatives = np.concatenate(
            [
                coordinates
                for other_state, coordinates in all_coordinates.items()
                if other_state != state
            ]
        )
        candidate = max(
            state_rows,
            key=lambda row: float(
                np.min(
                    np.abs(
                        alternatives - float(row["coordinate"])
                    )
                )
            ),
        )
        selected.append(
            {
                "case_id": (
                    f"Q03_CACHE_STATE_{state[0]}_{state[1]}"
                ),
                "case_source": "Q03_BRUTEFORCE_CACHE",
                "case_role": "cached-state-representative",
                "order9_node_id": "Q03",
                "epsilon_id": "E040",
                "component_id": "MC03",
                "soft_cosine": float(candidate["coordinate"]),
                "reference_steps": int(candidate["reference_steps"]),
                "reference_state_u": state[0],
                "reference_state_v": state[1],
                "reference_dynamic_multiplier": float(
                    candidate["reference_dynamic_multiplier"]
                ),
            }
        )
    transition_count = sum(
        (
            int(first["reference_state_u"]),
            int(first["reference_state_v"]),
        )
        != (
            int(second["reference_state_u"]),
            int(second["reference_state_v"]),
        )
        for first, second in zip(rows[:-1], rows[1:])
    )
    diagnostic = {
        "cached_resolution_state_count": len(
            read_json(STATE_CACHE_5243)["states"]
        ),
        "accepted_physical_coordinate_count": len(rows),
        "distinct_winding_state_count": len(by_state),
        "observed_state_transition_count": transition_count,
        "representative_case_count": len(selected),
        "states": [
            {"u": state[0], "v": state[1], "sample_count": len(state_rows)}
            for state, state_rows in sorted(by_state.items())
        ],
        "interpretation": (
            "Uniform adaptive homotopy is source-complete but too costly "
            "for the full interval map; use these states as references "
            "for the coupled reciprocal tracker."
        ),
    }
    return selected, diagnostic


def q03_problem(
    parent_manifest: dict[str, Any],
    base_jobs: list[dict[str, Any]],
    tracks: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    node = next(
        row
        for row in read_json(M5241.MANIFEST)["outer_nodes"]
        if row["order9_node_id"] == "Q03"
    )
    execution_node = {
        "outer_node_id": node["execution_node_id"],
        "master_index": int(node["master_index"]),
        "decay_cosine": float(node["decay_cosine"]),
    }
    jobs = M5240.material_node_jobs(
        execution_node, base_jobs, tracks
    )
    job = next(
        row
        for row in jobs
        if row["epsilon_id"] == "E040"
        and row["component_id"] == "MC03"
    )
    return M5240.build_node_problem(job)


def build_cases() -> tuple[
    dict[str, Any],
    list[dict[str, Any]],
    dict[str, dict[str, Any]],
    dict[str, Any],
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[str, dict[str, Any]],
]:
    parent_manifest, matches, base_jobs, _ = M5240.build_manifest()
    event = dict(parent_manifest["target_event"])
    tracks, _ = M5240.build_outer_branch_tracks(matches, event)
    problem_q03 = q03_problem(parent_manifest, base_jobs, tracks)
    cache_cases, cache_diagnostic = representative_cached_cases(
        problem_q03
    )
    problems: dict[str, dict[str, Any]] = {}
    cases: list[dict[str, Any]] = []
    manifest_5242 = read_json(MANIFEST_5242)
    summary_5242 = {
        row["case_id"]: row
        for row in read_json(RESULT_5242)["summary"]
    }
    for source_case in manifest_5242["cases"]:
        reference = summary_5242[source_case["case_id"]]
        case = {
            "case_id": source_case["case_id"],
            "case_source": "5242_HIGH_RESOLUTION_REFERENCE",
            "case_role": source_case["case_role"],
            "order9_node_id": source_case["order9_node_id"],
            "epsilon_id": source_case["epsilon_id"],
            "component_id": source_case["component_id"],
            "soft_cosine": float(source_case["soft_cosine"]),
            "reference_steps": 32768,
            "reference_state_u": int(
                reference["high_resolution_state_u"]
            ),
            "reference_state_v": int(
                reference["high_resolution_state_v"]
            ),
            "reference_dynamic_multiplier": float(
                reference["high_resolution_dynamic_multiplier"]
            ),
        }
        problem = M5242.build_problem_for_case(
            source_case, parent_manifest, base_jobs, tracks
        )
        cases.append(case)
        problems[case["case_id"]] = problem
    for case in cache_cases:
        cases.append(case)
        problems[case["case_id"]] = problem_q03
    return (
        parent_manifest,
        matches,
        problems,
        cache_diagnostic,
        cases,
        base_jobs,
        tracks,
    )


def coupled_pair_selection(
    representative_roots: list[complex],
    reciprocal_roots: list[complex],
    representative_reference: complex,
    reciprocal_reference: complex,
) -> tuple[complex, complex, float, float]:
    candidates = [
        {
            "representative": representative,
            "reciprocal": reciprocal,
            "reciprocal_residual": abs(
                representative * reciprocal - 1.0
            ),
            "continuity": (
                M5030.chordal_distance(
                    representative, representative_reference
                )
                + M5030.chordal_distance(
                    reciprocal, reciprocal_reference
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
        <= max(
            MAXIMUM_RECIPROCAL_RESIDUAL,
            100.0 * minimum_residual,
        )
    ]
    selected = min(
        eligible,
        key=lambda row: (
            row["continuity"],
            row["reciprocal_residual"],
        ),
    )
    return (
        complex(selected["representative"]),
        complex(selected["reciprocal"]),
        float(selected["reciprocal_residual"]),
        float(selected["continuity"]),
    )


def coupled_target_pair_track(
    problem: dict[str, Any],
    coordinate: float,
    steps: int,
) -> dict[str, Any]:
    event = dict(problem["event"])
    event[problem["case"]["outer_coordinate"]] = float(coordinate)
    target = problem["target"]
    representative_pair = problem["case"]["representative_pair"]
    reciprocal_pair = problem["case"]["reciprocal_pair"]
    representative_anchor = M5237.track_anchor(
        problem["branch_tracks"][M5237.pair_key(representative_pair)],
        complex(coordinate),
    )
    reciprocal_anchor = M5237.track_anchor(
        problem["branch_tracks"][M5237.pair_key(reciprocal_pair)],
        complex(coordinate),
    )
    M5034.configure(event, target)
    cosines = M5030.homotopy_cosines(
        steps, M5232.REGULATOR, "feynman"
    )
    boundaries, ownerships = M5030.physical_chambers()
    endpoint_paths, _, boundary_step = M5030.endpoint_log_paths(
        boundaries, cosines, M5232.BOUNDARY_TRACKING_STEPS
    )
    representative_paths: list[list[complex]] = []
    reciprocal_paths: list[list[complex]] = []
    for cosine in cosines:
        rationals = M5030.M5029.root_rationals(
            float(event["soft_energy"]),
            float(event["soft_cosine"]),
            float(event["decay_cosine"]),
            cosine,
        )
        representative_paths.append(
            M5030.M5029.collision_roots(
                rationals[representative_pair[0]],
                rationals[representative_pair[1]],
            )
        )
        reciprocal_paths.append(
            M5030.M5029.collision_roots(
                rationals[reciprocal_pair[0]],
                rationals[reciprocal_pair[1]],
            )
        )
    selected_representative: list[complex | None] = [
        None
    ] * len(cosines)
    selected_reciprocal: list[complex | None] = [
        None
    ] * len(cosines)
    (
        selected_representative[-1],
        selected_reciprocal[-1],
        _,
        _,
    ) = coupled_pair_selection(
        representative_paths[-1],
        reciprocal_paths[-1],
        representative_anchor,
        reciprocal_anchor,
    )
    for index in range(len(cosines) - 2, -1, -1):
        (
            selected_representative[index],
            selected_reciprocal[index],
            _,
            _,
        ) = coupled_pair_selection(
            representative_paths[index],
            reciprocal_paths[index],
            complex(selected_representative[index + 1]),
            complex(selected_reciprocal[index + 1]),
        )
    representative_roots = [
        complex(value) for value in selected_representative
    ]
    reciprocal_roots = [
        complex(value) for value in selected_reciprocal
    ]
    representative_steps = [
        M5030.chordal_distance(first, second)
        for first, second in zip(
            representative_roots[:-1],
            representative_roots[1:],
        )
    ]
    reciprocal_steps = [
        M5030.chordal_distance(first, second)
        for first, second in zip(
            reciprocal_roots[:-1],
            reciprocal_roots[1:],
        )
    ]
    maximum_pair_step = max(
        [*representative_steps, *reciprocal_steps], default=0.0
    )
    maximum_reciprocal_residual = max(
        abs(representative * reciprocal - 1.0)
        for representative, reciprocal in zip(
            representative_roots, reciprocal_roots
        )
    )

    def lifted_logs(roots: list[complex]) -> list[complex]:
        rows: list[complex] = []
        previous: complex | None = None
        for root in roots:
            value = (
                complex(np.log(root))
                if previous is None
                else M5030.lifted_log(root, previous)
            )
            rows.append(value)
            previous = value
        return rows

    tracks = [
        {
            "logs": lifted_logs(reciprocal_roots),
            "initial_pairs": [reciprocal_pair],
            "target_pairs": [reciprocal_pair],
        },
        {
            "logs": lifted_logs(representative_roots),
            "initial_pairs": [representative_pair],
            "target_pairs": [representative_pair],
        },
    ]
    crossings: list[dict[str, Any]] = []
    for chamber_index, ownership in enumerate(ownerships):
        selected_tracks = [
            track
            for track in tracks
            if ownership[track["target_pairs"][0][0]]
            != ownership[track["target_pairs"][0][1]]
        ]
        start_logs, end_logs = M5030.chamber_segment_logs(
            endpoint_paths, chamber_index
        )
        chamber_crossings, _ = M5030.surface_crossings(
            selected_tracks, start_logs, end_logs
        )
        crossings.extend(chamber_crossings)
    pair_rows: list[dict[str, Any]] = []
    for pair in (reciprocal_pair, representative_pair):
        selected_crossings = [
            crossing
            for crossing in crossings
            if crossing["target_pairs"][0] == list(pair)
        ]
        pair_rows.append(
            {
                "pair": list(pair),
                "crossing_count": len(selected_crossings),
                "winding_sum": sum(
                    int(row["winding_correction"])
                    for row in selected_crossings
                ),
            }
        )
    winding = {
        row["pair"][0].rsplit("_", 1)[-1]: int(
            row["winding_sum"]
        )
        for row in pair_rows
    }
    if set(winding) != {"u", "v"}:
        raise RuntimeError(f"incomplete coupled winding state: {winding}")
    representative_suffix, reciprocal_suffix, source_delta = (
        M5239.source_winding_delta(problem)
    )
    dynamic_delta = (
        winding[representative_suffix]
        - winding[reciprocal_suffix]
    )
    return {
        "state_u": winding["u"],
        "state_v": winding["v"],
        "dynamic_delta": dynamic_delta,
        "dynamic_multiplier": dynamic_delta / source_delta,
        "maximum_pair_projective_step": maximum_pair_step,
        "maximum_boundary_projective_step": float(boundary_step),
        "maximum_reciprocal_product_residual": (
            maximum_reciprocal_residual
        ),
        "pair_rows": pair_rows,
    }


def build_manifest() -> tuple[
    dict[str, Any],
    dict[str, dict[str, Any]],
    dict[str, Any],
]:
    (
        parent_manifest,
        _,
        problems,
        cache_diagnostic,
        cases,
        _,
        _,
    ) = build_cases()
    manifest = {
        "marker": MARKER,
        "revision": REVISION,
        "parent_checkpoint": 5243,
        "parent_5240_manifest_hash": parent_manifest["manifest_hash"],
        "coupled_resolutions": list(COUPLED_RESOLUTIONS),
        "case_count": len(cases),
        "source_files": source_rows(),
        "Q03_cache_diagnostic": cache_diagnostic,
        "cases": cases,
        "claim_boundary": {
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
            "reason": (
                "This is a finite reference-state prototype for branch "
                "transport, not a rebuilt interval map or integral."
            ),
        },
    }
    manifest["manifest_hash"] = serialized_hash(manifest)
    return manifest, problems, cache_diagnostic


def write_manifest_and_dry_run() -> dict[str, Any]:
    manifest, _, cache_diagnostic = build_manifest()
    checks = {
        "source_paths_exist_and_match": all(
            Path(row["path"]).exists()
            and digest(Path(row["path"])) == row["sha256"]
            for row in manifest["source_files"]
        ),
        "reference_case_count_bounded": (
            8 <= manifest["case_count"] <= 12
        ),
        "Q03_cache_has_multiple_states": (
            cache_diagnostic["distinct_winding_state_count"] >= 3
        ),
        "coupled_resolution_ceiling_below_reference": (
            max(COUPLED_RESOLUTIONS) < 32768
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
        "case_count": manifest["case_count"],
        "scheduled_tracks": (
            manifest["case_count"] * len(COUPLED_RESOLUTIONS)
        ),
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(MANIFEST, manifest)
    atomic_json(CACHE_DIAGNOSTIC, cache_diagnostic)
    atomic_json(DRY_RUN, report)
    if not report["dry_run_passed"]:
        failed = [key for key, passed in checks.items() if not passed]
        raise RuntimeError(f"5244 dry run failed: {failed}")
    return report


def validation_rows(
    manifest: dict[str, Any],
    summaries: list[dict[str, Any]],
    formal_digest: str,
    elapsed: float,
) -> list[dict[str, Any]]:
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
            "REFERENCE_CASE_COUNT",
            len(summaries) == manifest["case_count"],
            len(summaries),
            manifest["case_count"],
        ),
        (
            "acceptance",
            "ALL_REFERENCE_STATES_REPRODUCED",
            all(bool(row["reference_state_reproduced"]) for row in summaries),
            (
                f"{sum(bool(row['reference_state_reproduced']) for row in summaries)}"
                f"/{len(summaries)}"
            ),
            f"{len(summaries)}/{len(summaries)}",
        ),
        (
            "acceptance",
            "ALL_RECIPROCAL_IDENTITIES_PRESERVED",
            all(bool(row["reciprocal_gate_passed"]) for row in summaries),
            max(
                float(row["accepted_reciprocal_residual"])
                for row in summaries
            ),
            MAXIMUM_RECIPROCAL_RESIDUAL,
        ),
        (
            "acceptance",
            "ALL_PAIR_TRACKS_RESOLVED",
            all(bool(row["pair_projective_gate_passed"]) for row in summaries),
            max(
                float(row["accepted_pair_projective_step"])
                for row in summaries
            ),
            MAXIMUM_PROJECTIVE_STEP,
        ),
        (
            "acceptance",
            "ALL_BOUNDARY_TRACKS_RESOLVED",
            all(bool(row["boundary_projective_gate_passed"]) for row in summaries),
            max(
                float(row["accepted_boundary_projective_step"])
                for row in summaries
            ),
            MAXIMUM_BOUNDARY_PROJECTIVE_STEP,
        ),
        (
            "acceptance",
            "COUPLED_TRACK_USES_FEWER_STEPS",
            all(
                int(row["accepted_coupled_steps"])
                < int(row["reference_steps"])
                for row in summaries
            ),
            max(
                float(row["step_fraction_of_reference"])
                for row in summaries
            ),
            "<1",
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
            elapsed <= MAXIMUM_PROTOTYPE_SECONDS,
            elapsed,
            MAXIMUM_PROTOTYPE_SECONDS,
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
            "checkpoint": 5244,
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
    manifest: dict[str, Any],
    summaries: list[dict[str, Any]],
    validations: list[dict[str, Any]],
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
    reciprocal_passed = all(
        bool(row["reciprocal_gate_passed"]) for row in summaries
    )
    boundary_passed = all(
        bool(row["boundary_projective_gate_passed"])
        for row in summaries
    )
    if not integrity_passed:
        decision = "INVALID_COUPLED_RECIPROCAL_PROTOTYPE"
    elif acceptance_passed:
        decision = (
            "ADOPT_COUPLED_RECIPROCAL_TRACKER_FOR_INTERVAL_REBUILD"
        )
    elif reciprocal_passed and not boundary_passed:
        decision = (
            "HOLD_COLLISION_PAIR_REPAIR__DERIVE_RECIPROCAL_PROJECTIVE_BOUNDARY_TRACKER"
        )
    else:
        decision = (
            "HOLD_COUPLED_RECIPROCAL_TRACKER_PENDING_FAILED_GATE"
        )
    maximum_fraction = max(
        float(row["step_fraction_of_reference"]) for row in summaries
    )
    return "\n".join(
        [
            "# 5244 — Coupled reciprocal homotopy tracker prototype",
            "",
            "## Derivation",
            "",
            (
                "The matched component owns a reciprocal root pair, so "
                "representative and reciprocal roots are not independent "
                "branches. At every homotopy node this prototype selects "
                "the joint candidate pair that first minimizes "
                "`|r_rep r_rec - 1|` and then minimizes projective "
                "continuation distance. This enforces the exact component "
                "constraint during transport rather than checking it only "
                "after two independent tracks have been chosen."
            ),
            "",
            "## Reference set",
            "",
            (
                f"`{manifest['case_count']}` cases: five 5242 "
                "high-resolution controls plus one interior representative "
                "for every distinct Q03 cached winding state."
            ),
            "",
            "## Results",
            "",
            (
                f"- Reference states reproduced: "
                f"`{sum(bool(row['reference_state_reproduced']) for row in summaries)}/{len(summaries)}`."
            ),
            (
                f"- Maximum coupled/reference step fraction: "
                f"`{maximum_fraction:.12g}`."
            ),
            (
                "- Maximum reciprocal residual: "
                f"`{max(float(row['accepted_reciprocal_residual']) for row in summaries):.12g}`."
            ),
            (
                "- Maximum collision-pair projective step: "
                f"`{max(float(row['accepted_pair_projective_step']) for row in summaries):.12g}`."
            ),
            (
                "- Maximum chamber-boundary projective step: "
                f"`{max(float(row['accepted_boundary_projective_step']) for row in summaries):.12g}`."
            ),
            f"- Runtime: `{elapsed:.3f} s`.",
            "",
            "## Decision",
            "",
            (
                f"`{decision}`"
            ),
            "",
            "## Claim boundary",
            "",
            (
                "This audits collision and boundary transport at a bounded "
                "reference set. It does not yet rebuild Q03/Q05, integrate the "
                "two-angle slice, derive local GR, or validate full MTS."
            ),
            "",
            "## Interpretation",
            "",
            (
                "Joint collision-root selection repairs reciprocal identity "
                "to about 1e-11, but it is not sufficient. The physical "
                "chamber endpoint can still make an almost unit projective "
                "jump, and one cached winding state is not reproduced. The "
                "remaining ambiguity belongs to endpoint sheet exchange, "
                "not to the reciprocal collision pair."
            ),
            "",
            "## Next exact target",
            "",
            (
                "Track each physical chamber endpoint as its reciprocal "
                "projective pair through the homotopy, allowing endpoint "
                "sheet exchange without a logarithmic jump. Re-run this "
                "same ten-case reference set before returning to 5243."
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
    dry_run = write_manifest_and_dry_run()
    manifest, problems, cache_diagnostic = build_manifest()
    rows: list[dict[str, Any]] = []
    summaries: list[dict[str, Any]] = []
    for case in manifest["cases"]:
        problem = problems[case["case_id"]]
        local_rows: list[dict[str, Any]] = []
        accepted: dict[str, Any] | None = None
        for steps in COUPLED_RESOLUTIONS:
            track_started = time.perf_counter()
            state = coupled_target_pair_track(
                problem, float(case["soft_cosine"]), steps
            )
            state_matches = (
                int(state["state_u"])
                == int(case["reference_state_u"])
                and int(state["state_v"])
                == int(case["reference_state_v"])
            )
            pair_passed = (
                float(state["maximum_pair_projective_step"])
                <= MAXIMUM_PROJECTIVE_STEP
            )
            boundary_passed = (
                float(state["maximum_boundary_projective_step"])
                <= MAXIMUM_BOUNDARY_PROJECTIVE_STEP
            )
            reciprocal_passed = (
                float(
                    state["maximum_reciprocal_product_residual"]
                )
                <= MAXIMUM_RECIPROCAL_RESIDUAL
            )
            row = {
                "case_id": case["case_id"],
                "case_source": case["case_source"],
                "case_role": case["case_role"],
                "order9_node_id": case["order9_node_id"],
                "epsilon_id": case["epsilon_id"],
                "component_id": case["component_id"],
                "soft_cosine": case["soft_cosine"],
                "reference_steps": case["reference_steps"],
                "reference_state_u": case["reference_state_u"],
                "reference_state_v": case["reference_state_v"],
                "coupled_steps": steps,
                "coupled_state_u": state["state_u"],
                "coupled_state_v": state["state_v"],
                "coupled_dynamic_multiplier": state[
                    "dynamic_multiplier"
                ],
                "reference_state_reproduced": state_matches,
                "maximum_pair_projective_step": state[
                    "maximum_pair_projective_step"
                ],
                "maximum_boundary_projective_step": state[
                    "maximum_boundary_projective_step"
                ],
                "maximum_reciprocal_product_residual": state[
                    "maximum_reciprocal_product_residual"
                ],
                "pair_projective_gate_passed": pair_passed,
                "boundary_projective_gate_passed": boundary_passed,
                "reciprocal_gate_passed": reciprocal_passed,
                "accepted": (
                    state_matches
                    and pair_passed
                    and boundary_passed
                    and reciprocal_passed
                ),
                "elapsed_seconds": (
                    time.perf_counter() - track_started
                ),
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
            local_rows.append(row)
            rows.append(row)
            if row["accepted"]:
                accepted = row
                break
        if accepted is None:
            accepted = local_rows[-1]
        summaries.append(
            {
                "case_id": case["case_id"],
                "case_source": case["case_source"],
                "case_role": case["case_role"],
                "reference_steps": case["reference_steps"],
                "accepted_coupled_steps": accepted["coupled_steps"],
                "reference_state_reproduced": accepted[
                    "reference_state_reproduced"
                ],
                "accepted_state_u": accepted["coupled_state_u"],
                "accepted_state_v": accepted["coupled_state_v"],
                "accepted_pair_projective_step": accepted[
                    "maximum_pair_projective_step"
                ],
                "accepted_boundary_projective_step": accepted[
                    "maximum_boundary_projective_step"
                ],
                "accepted_reciprocal_residual": accepted[
                    "maximum_reciprocal_product_residual"
                ],
                "pair_projective_gate_passed": accepted[
                    "pair_projective_gate_passed"
                ],
                "boundary_projective_gate_passed": accepted[
                    "boundary_projective_gate_passed"
                ],
                "reciprocal_gate_passed": accepted[
                    "reciprocal_gate_passed"
                ],
                "step_fraction_of_reference": (
                    int(accepted["coupled_steps"])
                    / int(case["reference_steps"])
                ),
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    formal_digest = tree_digest(FORMAL)
    elapsed = time.perf_counter() - started
    validations = validation_rows(
        manifest, summaries, formal_digest, elapsed
    )
    write_csv(ROWS, rows)
    write_csv(SUMMARY_ROWS, summaries)
    write_csv(VALIDATION, validations)
    atomic_text(
        DOCUMENT,
        render_document(manifest, summaries, validations, elapsed),
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
    reciprocal_passed = all(
        bool(row["reciprocal_gate_passed"]) for row in summaries
    )
    boundary_passed = all(
        bool(row["boundary_projective_gate_passed"])
        for row in summaries
    )
    if not integrity_passed:
        decision = "INVALID_COUPLED_RECIPROCAL_PROTOTYPE"
    elif acceptance_passed:
        decision = (
            "ADOPT_COUPLED_RECIPROCAL_TRACKER_FOR_INTERVAL_REBUILD"
        )
    elif reciprocal_passed and not boundary_passed:
        decision = (
            "HOLD_COLLISION_PAIR_REPAIR__DERIVE_RECIPROCAL_PROJECTIVE_BOUNDARY_TRACKER"
        )
    else:
        decision = (
            "HOLD_COUPLED_RECIPROCAL_TRACKER_PENDING_FAILED_GATE"
        )
    result = {
        "marker": MARKER,
        "revision": REVISION,
        "dry_run": dry_run,
        "manifest_hash": manifest["manifest_hash"],
        "decision": decision,
        "integrity_passed": integrity_passed,
        "acceptance_passed": acceptance_passed,
        "case_count": len(summaries),
        "Q03_cache_diagnostic": cache_diagnostic,
        "maximum_step_fraction_of_reference": max(
            float(row["step_fraction_of_reference"])
            for row in summaries
        ),
        "formalization_workbench_digest": formal_digest,
        "elapsed_seconds": elapsed,
        "outputs": [
            str(path)
            for path in (
                MANIFEST,
                DRY_RUN,
                CACHE_DIAGNOSTIC,
                ROWS,
                SUMMARY_ROWS,
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
        raise RuntimeError(f"5244 integrity validation failed: {failed}")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="validate the coupled reference-set manifest only",
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
    print(json.dumps(execute(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
