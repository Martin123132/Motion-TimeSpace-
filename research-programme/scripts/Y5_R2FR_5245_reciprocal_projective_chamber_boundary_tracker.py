from __future__ import annotations

import argparse
import cmath
import csv
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
SOURCE = POST / "source-intake" / "functional_rg" / "5245"
RESIDUALS = POST / "source-intake" / "mts_residuals"

SCRIPT_5244 = (
    POST
    / "scripts"
    / "Y5_R2FR_5244_coupled_reciprocal_homotopy_tracker_prototype.py"
)
RESULT_5244 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5244"
    / "coupled_reciprocal_tracker_result.json"
)
SUMMARY_5244 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5244"
    / "coupled_reciprocal_case_summary.csv"
)

MANIFEST = SOURCE / "reciprocal_projective_boundary_manifest.json"
DRY_RUN = SOURCE / "reciprocal_projective_boundary_dry_run.json"
RESULT = SOURCE / "reciprocal_projective_boundary_result.json"
ROWS = SOURCE / "reciprocal_projective_resolution_ladder.csv"
SUMMARY_ROWS = SOURCE / "reciprocal_projective_case_summary.csv"
BOUNDARY_ROWS = SOURCE / "reciprocal_projective_boundary_audit.csv"
VALIDATION = RESIDUALS / "P8_Y5_BRR545_5245_VALIDATION.csv"
DOCUMENT = (
    POST
    / "5245-Y5-R2FR-reciprocal-projective-chamber-boundary-tracker.md"
)

MARKER = "MTS_5245_RECIPROCAL_PROJECTIVE_CHAMBER_BOUNDARY_TRACKER"
REVISION = "reciprocal-projective-chamber-boundary-tracker-v1"
FORMAL_BASELINE = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)

RESOLUTION_LADDER = (8192, 16384, 32768, 65536)
MAXIMUM_PROJECTIVE_STEP = 5.0e-2
MAXIMUM_COLLISION_RECIPROCAL_RESIDUAL = 2.0e-8
MAXIMUM_BOUNDARY_RECIPROCAL_RESIDUAL = 2.0e-10
MAXIMUM_BOUNDARY_POLYNOMIAL_RESIDUAL = 2.0e-10
MAXIMUM_RUNTIME_SECONDS = 60.0 * 60.0


def load_module(path: Path, name: str) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5244 = load_module(SCRIPT_5244, "mts_5244_for_5245")
M5243 = M5244.M5243
M5242 = M5244.M5242
M5240 = M5244.M5240
M5239 = M5244.M5239
M5237 = M5244.M5237
M5232 = M5244.M5232
M5030 = M5244.M5030
M5034 = M5244.M5034
M5027 = M5030.M5028.M5027

digest = M5244.digest
tree_digest = M5244.tree_digest
serialized_hash = M5244.serialized_hash
atomic_text = M5244.atomic_text
atomic_json = M5244.atomic_json
write_csv = M5244.write_csv


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def source_rows() -> list[dict[str, str]]:
    paths = (
        SCRIPT_5244,
        RESULT_5244,
        SUMMARY_5244,
        M5244.SCRIPT_5243,
        M5244.RESULT_5242,
        Path(M5030.__file__),
        Path(M5027.__file__),
        M5244.STATE_CACHE_5243,
    )
    return [
        {"path": str(path), "sha256": digest(path)}
        for path in paths
    ]


def equation_key(boundary: dict[str, Any]) -> tuple[int, int]:
    equation = boundary["equations"][0]
    return (
        int(equation["hard_sign"]),
        int(equation["external_sign"]),
    )


def boundary_eta(
    boundary: dict[str, Any], scattering_cosine: complex
) -> complex:
    equation = boundary["equations"][0]
    soft_cosine = complex(M5030.SOFT_COSINE, 0.0)
    decay_cosine = complex(M5030.DECAY_COSINE, 0.0)
    relative_cosine = M5027.required_relative_cosine(
        float(M5030.SOFT_ENERGY),
        soft_cosine,
        decay_cosine,
        int(equation["external_sign"]) * scattering_cosine,
        int(equation["hard_sign"]),
    )
    soft_transverse = np.sqrt(1.0 - soft_cosine**2 + 0.0j)
    decay_transverse = np.sqrt(1.0 - decay_cosine**2 + 0.0j)
    return complex(
        (
            relative_cosine
            - soft_cosine * decay_cosine
        )
        / (soft_transverse * decay_transverse)
    )


def reciprocal_polynomial_roots(
    boundary: dict[str, Any], scattering_cosine: complex
) -> tuple[tuple[complex, complex], complex, float, float]:
    eta = boundary_eta(boundary, scattering_cosine)
    discriminant = complex(np.sqrt(eta * eta - 1.0 + 0.0j))
    candidates = (
        complex(eta + discriminant),
        complex(eta - discriminant),
    )
    primary = max(candidates, key=abs)
    if abs(primary) <= 1.0e-300:
        raise RuntimeError("reciprocal boundary root collapsed to zero")
    secondary = complex(1.0 / primary)
    roots = (primary, secondary)
    product_residual = abs(roots[0] * roots[1] - 1.0)
    polynomial_residual = max(
        abs(root * root - 2.0 * eta * root + 1.0)
        / max(
            1.0,
            abs(root) ** 2
            + 2.0 * abs(eta) * abs(root)
            + 1.0,
        )
        for root in roots
    )
    return roots, eta, product_residual, polynomial_residual


def assign_reciprocal_pair(
    previous: tuple[complex, complex],
    candidates: tuple[complex, complex],
) -> tuple[tuple[complex, complex], float, int]:
    same_steps = (
        M5030.chordal_distance(previous[0], candidates[0]),
        M5030.chordal_distance(previous[1], candidates[1]),
    )
    swapped_steps = (
        M5030.chordal_distance(previous[0], candidates[1]),
        M5030.chordal_distance(previous[1], candidates[0]),
    )
    same_cost = (max(same_steps), sum(same_steps))
    swapped_cost = (max(swapped_steps), sum(swapped_steps))
    if swapped_cost < same_cost:
        return (
            (candidates[1], candidates[0]),
            float(swapped_cost[0]),
            1,
        )
    return (
        candidates,
        float(same_cost[0]),
        0,
    )


def reciprocal_projective_endpoint_log_paths(
    boundaries: list[dict[str, Any]],
    cosines: list[complex],
    tracking_steps: int,
) -> tuple[
    list[list[complex]],
    float,
    float,
    dict[str, Any],
]:
    if not cosines:
        raise ValueError("endpoint transport requires a non-empty path")
    paths: list[list[complex] | None] = [None] * len(boundaries)
    groups: dict[tuple[int, int], list[int]] = defaultdict(list)
    synthetic_indices: list[int] = []
    multiple_equation_boundary_count = 0
    for index, boundary in enumerate(boundaries):
        if boundary.get("synthetic"):
            synthetic_indices.append(index)
            continue
        if len(boundary["equations"]) != 1:
            multiple_equation_boundary_count += 1
        groups[equation_key(boundary)].append(index)
    for index in synthetic_indices:
        reference = complex(0.0, float(boundaries[index]["angle"]))
        paths[index] = [reference for _ in cosines]

    maximum_log_step = 0.0
    maximum_projective_step = 0.0
    maximum_reciprocal_residual = 0.0
    maximum_polynomial_residual = 0.0
    maximum_eta_magnitude = 0.0
    chart_assignment_flip_count = 0
    invalid_group_count = 0
    group_rows: list[dict[str, Any]] = []
    bridge_steps = max(1, int(tracking_steps))
    bridge = [
        M5030.REFERENCE_COSINE
        + index
        / bridge_steps
        * (cosines[0] - M5030.REFERENCE_COSINE)
        for index in range(1, bridge_steps + 1)
    ]
    transport_cosines = [*bridge, *cosines[1:]]

    for key, indices in sorted(groups.items()):
        if len(indices) != 2:
            invalid_group_count += 1
            continue
        first_boundary = boundaries[indices[0]]
        previous = (
            complex(boundaries[indices[0]]["root"]),
            complex(boundaries[indices[1]]["root"]),
        )
        initial_product_residual = abs(
            previous[0] * previous[1] - 1.0
        )
        maximum_reciprocal_residual = max(
            maximum_reciprocal_residual,
            initial_product_residual,
        )
        references = [
            complex(0.0, float(boundaries[index]["angle"]))
            for index in indices
        ]
        values: list[list[complex]] = [[], []]
        previous_assignment: int | None = None
        local_maximum_step = 0.0
        local_maximum_eta = 0.0
        local_assignment_flips = 0
        for transport_index, cosine in enumerate(transport_cosines):
            (
                candidates,
                eta,
                reciprocal_residual,
                polynomial_residual,
            ) = reciprocal_polynomial_roots(first_boundary, cosine)
            assigned, projective_step, assignment = (
                assign_reciprocal_pair(previous, candidates)
            )
            if (
                previous_assignment is not None
                and assignment != previous_assignment
            ):
                local_assignment_flips += 1
            previous_assignment = assignment
            maximum_projective_step = max(
                maximum_projective_step,
                projective_step,
            )
            local_maximum_step = max(
                local_maximum_step,
                projective_step,
            )
            maximum_reciprocal_residual = max(
                maximum_reciprocal_residual,
                reciprocal_residual,
                abs(assigned[0] * assigned[1] - 1.0),
            )
            maximum_polynomial_residual = max(
                maximum_polynomial_residual,
                polynomial_residual,
            )
            maximum_eta_magnitude = max(
                maximum_eta_magnitude,
                abs(eta),
            )
            local_maximum_eta = max(local_maximum_eta, abs(eta))
            for track_index, root in enumerate(assigned):
                lifted = M5030.lifted_log(
                    root, references[track_index]
                )
                maximum_log_step = max(
                    maximum_log_step,
                    abs(lifted - references[track_index]),
                )
                references[track_index] = lifted
            if transport_index >= bridge_steps - 1:
                for track_index in range(2):
                    values[track_index].append(
                        references[track_index]
                    )
            previous = assigned
        chart_assignment_flip_count += local_assignment_flips
        for track_index, boundary_index in enumerate(indices):
            if len(values[track_index]) != len(cosines):
                raise RuntimeError(
                    "reciprocal boundary path length mismatch"
                )
            paths[boundary_index] = values[track_index]
        group_rows.append(
            {
                "hard_sign": key[0],
                "external_sign": key[1],
                "boundary_indices": list(indices),
                "initial_product_residual": initial_product_residual,
                "maximum_projective_step": local_maximum_step,
                "maximum_eta_magnitude": local_maximum_eta,
                "chart_assignment_flip_count": (
                    local_assignment_flips
                ),
            }
        )

    if invalid_group_count:
        raise RuntimeError(
            f"{invalid_group_count} reciprocal boundary groups "
            "did not contain exactly two physical endpoints"
        )
    if any(path is None for path in paths):
        raise RuntimeError("incomplete reciprocal endpoint path set")
    diagnostics = {
        "physical_boundary_count": len(boundaries)
        - len(synthetic_indices),
        "synthetic_boundary_count": len(synthetic_indices),
        "reciprocal_boundary_group_count": len(groups),
        "invalid_boundary_group_count": invalid_group_count,
        "multiple_equation_boundary_count": (
            multiple_equation_boundary_count
        ),
        "maximum_boundary_reciprocal_residual": (
            maximum_reciprocal_residual
        ),
        "maximum_boundary_polynomial_residual": (
            maximum_polynomial_residual
        ),
        "maximum_boundary_eta_magnitude": maximum_eta_magnitude,
        "chart_assignment_flip_count": (
            chart_assignment_flip_count
        ),
        "groups": group_rows,
    }
    return (
        [list(path) for path in paths if path is not None],
        maximum_log_step,
        maximum_projective_step,
        diagnostics,
    )


def reciprocal_projective_state(
    problem: dict[str, Any],
    coordinate: float,
    steps: int,
) -> dict[str, Any]:
    diagnostics: dict[str, Any] = {}
    original = M5030.endpoint_log_paths

    def replacement(
        boundaries: list[dict[str, Any]],
        cosines: list[complex],
        tracking_steps: int,
    ) -> tuple[list[list[complex]], float, float]:
        paths, log_step, projective_step, report = (
            reciprocal_projective_endpoint_log_paths(
                boundaries,
                cosines,
                tracking_steps,
            )
        )
        diagnostics.update(report)
        return paths, log_step, projective_step

    M5030.endpoint_log_paths = replacement
    try:
        state = M5244.coupled_target_pair_track(
            problem, coordinate, steps
        )
    finally:
        M5030.endpoint_log_paths = original
    if not diagnostics:
        raise RuntimeError("boundary diagnostics were not produced")
    return {**state, **diagnostics}


def prepare() -> tuple[
    dict[str, Any],
    dict[str, Any],
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
    ) = M5244.build_cases()
    manifest = {
        "marker": MARKER,
        "revision": REVISION,
        "parent_checkpoint": 5244,
        "parent_5240_manifest_hash": (
            parent_manifest["manifest_hash"]
        ),
        "resolution_ladder": list(RESOLUTION_LADDER),
        "case_count": len(cases),
        "source_files": source_rows(),
        "Q03_cache_diagnostic": cache_diagnostic,
        "cases": cases,
        "transport_contract": {
            "boundary_polynomial": "z^2 - 2 eta z + 1 = 0",
            "reciprocal_involution": "z -> 1/z",
            "pair_product": "z_plus z_minus = 1",
            "continuation_metric": "chordal metric on CP1",
            "assignment": (
                "minimum bottleneck then minimum total pair distance"
            ),
            "convergence": (
                "two consecutive fully resolved resolutions "
                "with identical winding state"
            ),
        },
        "claim_boundary": {
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
            "reason": (
                "This resolves a bounded homotopy-topology reference "
                "set and does not itself rebuild or integrate Q03/Q05."
            ),
        },
    }
    manifest["manifest_hash"] = serialized_hash(manifest)
    dry_checks = {
        "source_paths_exist_and_match": all(
            Path(row["path"]).exists()
            and digest(Path(row["path"])) == row["sha256"]
            for row in manifest["source_files"]
        ),
        "reference_case_count_is_ten": len(cases) == 10,
        "resolution_ladder_strictly_increases": all(
            first < second
            for first, second in zip(
                RESOLUTION_LADDER[:-1],
                RESOLUTION_LADDER[1:],
            )
        ),
        "Q03_cache_has_multiple_states": (
            cache_diagnostic["distinct_winding_state_count"] >= 3
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
    dry_run = {
        "marker": MARKER,
        "revision": REVISION,
        "dry_run_passed": all(dry_checks.values()),
        "checks": dry_checks,
        "manifest_hash": manifest["manifest_hash"],
        "case_count": len(cases),
        "maximum_scheduled_tracks": (
            len(cases) * len(RESOLUTION_LADDER)
        ),
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    return manifest, problems, dry_run


def validation_rows(
    manifest: dict[str, Any],
    summaries: list[dict[str, Any]],
    formal_digest: str,
    elapsed: float,
) -> list[dict[str, Any]]:
    controls = [
        row
        for row in summaries
        if row["case_source"] == "5242_HIGH_RESOLUTION_REFERENCE"
    ]
    q03_rows = [
        row
        for row in summaries
        if row["case_source"] == "Q03_BRUTEFORCE_CACHE"
    ]
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
            len(summaries) == manifest["case_count"] == 10,
            len(summaries),
            10,
        ),
        (
            "acceptance",
            "ALL_CASES_TWO_RESOLUTION_CONVERGED",
            all(bool(row["two_resolution_converged"]) for row in summaries),
            (
                f"{sum(bool(row['two_resolution_converged']) for row in summaries)}"
                f"/{len(summaries)}"
            ),
            f"{len(summaries)}/{len(summaries)}",
        ),
        (
            "acceptance",
            "ALL_5242_CONTROL_STATES_REPRODUCED",
            len(controls) == 5
            and all(
                bool(row["legacy_reference_state_reproduced"])
                for row in controls
            ),
            (
                f"{sum(bool(row['legacy_reference_state_reproduced']) for row in controls)}"
                f"/{len(controls)}"
            ),
            "5/5",
        ),
        (
            "acceptance",
            "ALL_COLLISION_PAIR_TRACKS_RESOLVED",
            all(
                bool(row["collision_projective_gate_passed"])
                for row in summaries
            ),
            max(
                float(row["accepted_collision_projective_step"])
                for row in summaries
            ),
            MAXIMUM_PROJECTIVE_STEP,
        ),
        (
            "acceptance",
            "ALL_BOUNDARY_PAIR_TRACKS_RESOLVED",
            all(
                bool(row["boundary_projective_gate_passed"])
                for row in summaries
            ),
            max(
                float(row["accepted_boundary_projective_step"])
                for row in summaries
            ),
            MAXIMUM_PROJECTIVE_STEP,
        ),
        (
            "acceptance",
            "ALL_COLLISION_RECIPROCITIES_PRESERVED",
            all(
                bool(row["collision_reciprocal_gate_passed"])
                for row in summaries
            ),
            max(
                float(row["accepted_collision_reciprocal_residual"])
                for row in summaries
            ),
            MAXIMUM_COLLISION_RECIPROCAL_RESIDUAL,
        ),
        (
            "acceptance",
            "ALL_BOUNDARY_RECIPROCITIES_PRESERVED",
            all(
                bool(row["boundary_reciprocal_gate_passed"])
                for row in summaries
            ),
            max(
                float(row["accepted_boundary_reciprocal_residual"])
                for row in summaries
            ),
            MAXIMUM_BOUNDARY_RECIPROCAL_RESIDUAL,
        ),
        (
            "acceptance",
            "ALL_BOUNDARY_POLYNOMIALS_SATISFIED",
            all(
                bool(row["boundary_polynomial_gate_passed"])
                for row in summaries
            ),
            max(
                float(row["accepted_boundary_polynomial_residual"])
                for row in summaries
            ),
            MAXIMUM_BOUNDARY_POLYNOMIAL_RESIDUAL,
        ),
        (
            "acceptance",
            "Q03_LEGACY_DIFFERENCES_CLASSIFIED",
            len(q03_rows) == 5
            and all(
                bool(row["two_resolution_converged"])
                for row in q03_rows
            ),
            (
                f"{sum(not bool(row['legacy_reference_state_reproduced']) for row in q03_rows)}"
                f" superseded of {len(q03_rows)}"
            ),
            "all Q03 rows converged before classification",
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
            "checkpoint": 5245,
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


def decision_from(
    validations: list[dict[str, Any]],
    summaries: list[dict[str, Any]],
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
        return "INVALID_RECIPROCAL_PROJECTIVE_BOUNDARY_TRACKER"
    if not acceptance_passed:
        return "HOLD_RECIPROCAL_PROJECTIVE_BOUNDARY_TRACKER_PENDING_FAILED_GATE"
    q03_changed = any(
        not bool(row["legacy_reference_state_reproduced"])
        for row in summaries
        if row["case_source"] == "Q03_BRUTEFORCE_CACHE"
    )
    if q03_changed:
        return (
            "SUPERSEDE_Q03_LEGACY_WINDING_CACHE__"
            "REBUILD_WITH_RECIPROCAL_PROJECTIVE_BOUNDARIES"
        )
    return (
        "ADOPT_RECIPROCAL_PROJECTIVE_BOUNDARY_TRACKER__"
        "REBUILD_Q03_INTERVALS"
    )


def render_document(
    manifest: dict[str, Any],
    summaries: list[dict[str, Any]],
    validations: list[dict[str, Any]],
    elapsed: float,
) -> str:
    decision = decision_from(validations, summaries)
    q03_rows = [
        row
        for row in summaries
        if row["case_source"] == "Q03_BRUTEFORCE_CACHE"
    ]
    q03_legacy_matches = sum(
        bool(row["legacy_reference_state_reproduced"])
        for row in q03_rows
    )
    q03_states = sorted(
        {
            (
                int(row["accepted_state_u"]),
                int(row["accepted_state_v"]),
            )
            for row in q03_rows
        }
    )
    acceptance_passed = all(
        bool(row["passed"])
        for row in validations
        if row["gate_kind"] == "acceptance"
    )
    return "\n".join(
        [
            "# 5245 — Reciprocal-projective chamber-boundary tracker",
            "",
            "## Exact transport law",
            "",
            (
                "Every non-synthetic chamber endpoint is a root of "
                "`z^2 - 2 eta z + 1 = 0`. Hence its two sheets obey "
                "`z_+ z_- = 1`; they are one reciprocal pair on "
                "`CP1`, not two independently selectable square roots."
            ),
            "",
            (
                "The tracker evaluates the non-cancelling root, obtains "
                "its partner by exact reciprocal division, and labels the "
                "pair at each homotopy node by minimum bottleneck chordal "
                "distance followed by minimum total chordal distance. "
                "This remains regular through the zero/infinity chart "
                "exchange that defeated the Euclidean square-root rule."
            ),
            "",
            "## Resolution contract",
            "",
            (
                "A state is accepted only after two consecutive ladder "
                "resolutions satisfy both projective gates, both "
                "reciprocity gates, the boundary-polynomial gate, and "
                "return identical winding integers."
            ),
            "",
            "## Results",
            "",
            (
                f"- Ten-case two-resolution convergence: "
                f"`{sum(bool(row['two_resolution_converged']) for row in summaries)}/{len(summaries)}`."
            ),
            (
                "- 5242 high-resolution control states reproduced: "
                f"`{sum(bool(row['legacy_reference_state_reproduced']) for row in summaries if row['case_source'] == '5242_HIGH_RESOLUTION_REFERENCE')}/5`."
            ),
            (
                "- Maximum accepted collision-pair projective step: "
                f"`{max(float(row['accepted_collision_projective_step']) for row in summaries):.12g}`."
            ),
            (
                "- Maximum accepted boundary-pair projective step: "
                f"`{max(float(row['accepted_boundary_projective_step']) for row in summaries):.12g}`."
            ),
            (
                "- Maximum accepted boundary reciprocal residual: "
                f"`{max(float(row['accepted_boundary_reciprocal_residual']) for row in summaries):.12g}`."
            ),
            (
                "- Maximum accepted normalized boundary-polynomial "
                "residual: "
                f"`{max(float(row['accepted_boundary_polynomial_residual']) for row in summaries):.12g}`."
            ),
            (
                f"- Legacy Q03 cache states retained: "
                f"`{q03_legacy_matches}/{len(q03_rows)}`."
            ),
            f"- Converged Q03 paired states: `{q03_states}`.",
            f"- Runtime: `{elapsed:.3f} s`.",
            "",
            "## Decision",
            "",
            f"`{decision}`",
            "",
            "## Interpretation",
            "",
            (
                "The old near-unit boundary jump was not a physical "
                "topology signal. It came from independently transporting "
                "one principal-square-root representative through a "
                "reciprocal zero/infinity chart exchange. The paired "
                "polynomial transport removes that discontinuity while "
                "preserving the independently established 5242 controls."
                if acceptance_passed
                else
                "At least one reciprocal-projective acceptance gate "
                "remains open; no legacy winding row is superseded."
            ),
            "",
            "## Claim boundary",
            "",
            (
                "This is a topology/transport correction on ten bounded "
                "reference cases. It does not supply a corrected Q03/Q05 "
                "integral, a numeric UV coefficient, local GR, or full MTS."
            ),
            "",
            "## Next exact target",
            "",
            (
                "Invalidate only the legacy Q03 winding cache rows whose "
                "states fail this paired convergence contract, rebuild the "
                "Q03 interval topology with the reciprocal-projective "
                "endpoint tracker, and then rerun the Q03 inner slice. "
                "Do not return to uniform 5243 state doubling."
                if acceptance_passed
                else
                "Localize the first failed resolution case before any "
                "Q03 interval rebuild."
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
    manifest, problems, dry_run = prepare()
    atomic_json(MANIFEST, manifest)
    atomic_json(DRY_RUN, dry_run)
    if not dry_run["dry_run_passed"]:
        failed = [
            key
            for key, passed in dry_run["checks"].items()
            if not passed
        ]
        raise RuntimeError(f"5245 dry run failed: {failed}")

    rows: list[dict[str, Any]] = []
    summaries: list[dict[str, Any]] = []
    boundary_rows: list[dict[str, Any]] = []
    for case in manifest["cases"]:
        problem = problems[case["case_id"]]
        local_rows: list[dict[str, Any]] = []
        previous: dict[str, Any] | None = None
        accepted: dict[str, Any] | None = None
        for steps in RESOLUTION_LADDER:
            track_started = time.perf_counter()
            state = reciprocal_projective_state(
                problem,
                float(case["soft_cosine"]),
                steps,
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
                float(
                    state[
                        "maximum_reciprocal_product_residual"
                    ]
                )
                <= MAXIMUM_COLLISION_RECIPROCAL_RESIDUAL
            )
            boundary_reciprocal_passed = (
                float(
                    state[
                        "maximum_boundary_reciprocal_residual"
                    ]
                )
                <= MAXIMUM_BOUNDARY_RECIPROCAL_RESIDUAL
            )
            boundary_polynomial_passed = (
                float(
                    state[
                        "maximum_boundary_polynomial_residual"
                    ]
                )
                <= MAXIMUM_BOUNDARY_POLYNOMIAL_RESIDUAL
            )
            boundary_structure_passed = (
                int(state["invalid_boundary_group_count"]) == 0
                and int(
                    state["multiple_equation_boundary_count"]
                )
                == 0
            )
            fully_resolved = all(
                (
                    collision_projective_passed,
                    boundary_projective_passed,
                    collision_reciprocal_passed,
                    boundary_reciprocal_passed,
                    boundary_polynomial_passed,
                    boundary_structure_passed,
                )
            )
            state_stable = (
                previous is not None
                and int(previous["paired_state_u"])
                == int(state["state_u"])
                and int(previous["paired_state_v"])
                == int(state["state_v"])
            )
            two_resolution_converged = (
                fully_resolved
                and previous is not None
                and bool(previous["fully_resolved"])
                and state_stable
            )
            row = {
                "case_id": case["case_id"],
                "case_source": case["case_source"],
                "case_role": case["case_role"],
                "order9_node_id": case["order9_node_id"],
                "epsilon_id": case["epsilon_id"],
                "component_id": case["component_id"],
                "soft_cosine": case["soft_cosine"],
                "legacy_reference_steps": case["reference_steps"],
                "legacy_state_u": case["reference_state_u"],
                "legacy_state_v": case["reference_state_v"],
                "paired_steps": steps,
                "paired_state_u": state["state_u"],
                "paired_state_v": state["state_v"],
                "paired_dynamic_multiplier": state[
                    "dynamic_multiplier"
                ],
                "legacy_reference_state_reproduced": (
                    int(state["state_u"])
                    == int(case["reference_state_u"])
                    and int(state["state_v"])
                    == int(case["reference_state_v"])
                ),
                "state_stable_from_previous": state_stable,
                "two_resolution_converged": (
                    two_resolution_converged
                ),
                "maximum_collision_projective_step": state[
                    "maximum_pair_projective_step"
                ],
                "maximum_boundary_projective_step": state[
                    "maximum_boundary_projective_step"
                ],
                "maximum_collision_reciprocal_residual": state[
                    "maximum_reciprocal_product_residual"
                ],
                "maximum_boundary_reciprocal_residual": state[
                    "maximum_boundary_reciprocal_residual"
                ],
                "maximum_boundary_polynomial_residual": state[
                    "maximum_boundary_polynomial_residual"
                ],
                "maximum_boundary_eta_magnitude": state[
                    "maximum_boundary_eta_magnitude"
                ],
                "physical_boundary_count": state[
                    "physical_boundary_count"
                ],
                "reciprocal_boundary_group_count": state[
                    "reciprocal_boundary_group_count"
                ],
                "chart_assignment_flip_count": state[
                    "chart_assignment_flip_count"
                ],
                "collision_projective_gate_passed": (
                    collision_projective_passed
                ),
                "boundary_projective_gate_passed": (
                    boundary_projective_passed
                ),
                "collision_reciprocal_gate_passed": (
                    collision_reciprocal_passed
                ),
                "boundary_reciprocal_gate_passed": (
                    boundary_reciprocal_passed
                ),
                "boundary_polynomial_gate_passed": (
                    boundary_polynomial_passed
                ),
                "boundary_structure_gate_passed": (
                    boundary_structure_passed
                ),
                "fully_resolved": fully_resolved,
                "elapsed_seconds": (
                    time.perf_counter() - track_started
                ),
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
            rows.append(row)
            local_rows.append(row)
            for group in state["groups"]:
                boundary_rows.append(
                    {
                        "case_id": case["case_id"],
                        "paired_steps": steps,
                        **group,
                        "valid_for_numeric_UV_claim": False,
                        "valid_for_local_GR_claim": False,
                        "valid_for_full_MTS_claim": False,
                    }
                )
            if two_resolution_converged:
                accepted = row
                break
            previous = row
        if accepted is None:
            accepted = local_rows[-1]
        summaries.append(
            {
                "case_id": case["case_id"],
                "case_source": case["case_source"],
                "case_role": case["case_role"],
                "legacy_reference_steps": case["reference_steps"],
                "accepted_paired_steps": accepted["paired_steps"],
                "legacy_state_u": case["reference_state_u"],
                "legacy_state_v": case["reference_state_v"],
                "accepted_state_u": accepted["paired_state_u"],
                "accepted_state_v": accepted["paired_state_v"],
                "legacy_reference_state_reproduced": accepted[
                    "legacy_reference_state_reproduced"
                ],
                "two_resolution_converged": accepted[
                    "two_resolution_converged"
                ],
                "accepted_collision_projective_step": accepted[
                    "maximum_collision_projective_step"
                ],
                "accepted_boundary_projective_step": accepted[
                    "maximum_boundary_projective_step"
                ],
                "accepted_collision_reciprocal_residual": accepted[
                    "maximum_collision_reciprocal_residual"
                ],
                "accepted_boundary_reciprocal_residual": accepted[
                    "maximum_boundary_reciprocal_residual"
                ],
                "accepted_boundary_polynomial_residual": accepted[
                    "maximum_boundary_polynomial_residual"
                ],
                "collision_projective_gate_passed": accepted[
                    "collision_projective_gate_passed"
                ],
                "boundary_projective_gate_passed": accepted[
                    "boundary_projective_gate_passed"
                ],
                "collision_reciprocal_gate_passed": accepted[
                    "collision_reciprocal_gate_passed"
                ],
                "boundary_reciprocal_gate_passed": accepted[
                    "boundary_reciprocal_gate_passed"
                ],
                "boundary_polynomial_gate_passed": accepted[
                    "boundary_polynomial_gate_passed"
                ],
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
    decision = decision_from(validations, summaries)
    write_csv(ROWS, rows)
    write_csv(SUMMARY_ROWS, summaries)
    write_csv(BOUNDARY_ROWS, boundary_rows)
    write_csv(VALIDATION, validations)
    atomic_text(
        DOCUMENT,
        render_document(
            manifest,
            summaries,
            validations,
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
    result = {
        "marker": MARKER,
        "revision": REVISION,
        "dry_run": dry_run,
        "manifest_hash": manifest["manifest_hash"],
        "decision": decision,
        "integrity_passed": integrity_passed,
        "acceptance_passed": acceptance_passed,
        "case_count": len(summaries),
        "Q03_legacy_state_match_count": sum(
            bool(row["legacy_reference_state_reproduced"])
            for row in summaries
            if row["case_source"] == "Q03_BRUTEFORCE_CACHE"
        ),
        "formalization_workbench_digest": formal_digest,
        "elapsed_seconds": elapsed,
        "outputs": [
            str(path)
            for path in (
                MANIFEST,
                DRY_RUN,
                ROWS,
                SUMMARY_ROWS,
                BOUNDARY_ROWS,
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
        raise RuntimeError(f"5245 integrity validation failed: {failed}")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="validate the reciprocal-projective manifest only",
    )
    arguments = parser.parse_args()
    if arguments.dry_run:
        manifest, _, dry_run = prepare()
        atomic_json(MANIFEST, manifest)
        atomic_json(DRY_RUN, dry_run)
        print(json.dumps(dry_run, indent=2, sort_keys=True))
        return
    print(json.dumps(execute(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
