from __future__ import annotations

import argparse
import csv
import importlib.util
import json
import shutil
import sys
import time
from pathlib import Path
from typing import Any


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE = POST / "source-intake" / "functional_rg" / "5248"
RESIDUALS = POST / "source-intake" / "mts_residuals"
JOB_CACHE = SOURCE / "job-cache"

SCRIPT_5246 = (
    POST
    / "scripts"
    / "Y5_R2FR_5246_Q03_reciprocal_projective_interval_topology_rebuild.py"
)
RESULT_5245 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5245"
    / "reciprocal_projective_boundary_result.json"
)
RESULT_5246 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5246"
    / "Q03_reciprocal_projective_interval_result.json"
)
RESULT_5247 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5247"
    / "Q03_corrected_inner_slice_result.json"
)
VALIDATION_5247 = (
    RESIDUALS / "P8_Y5_BRR545_5247_VALIDATION.csv"
)

MANIFEST = SOURCE / "Q05_reciprocal_projective_interval_manifest.json"
DRY_RUN = SOURCE / "Q05_reciprocal_projective_interval_dry_run.json"
RESULT = SOURCE / "Q05_reciprocal_projective_interval_result.json"
STATE_CACHE = SOURCE / "Q05_reciprocal_projective_state_cache.json"
ATTEMPT_ROWS = SOURCE / "Q05_reciprocal_projective_resolution_attempts.csv"
INTERVAL_ROWS = SOURCE / "Q05_reciprocal_projective_intervals.csv"
TRANSITION_ROWS = SOURCE / "Q05_reciprocal_projective_transitions.csv"
JOB_ROWS = SOURCE / "Q05_reciprocal_projective_job_summary.csv"
COMPARISON_ROWS = SOURCE / "Q05_legacy_vs_reciprocal_projective_map.csv"
VALIDATION = RESIDUALS / "P8_Y5_BRR545_5248_VALIDATION.csv"
DOCUMENT = (
    POST
    / "5248-Y5-R2FR-Q05-reciprocal-projective-interval-topology-rebuild.md"
)

MARKER = "MTS_5248_Q05_RECIPROCAL_PROJECTIVE_INTERVAL_TOPOLOGY_REBUILD"
REVISION = "Q05-reciprocal-projective-interval-topology-rebuild-v1"
FORMAL_BASELINE = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)
TARGET_NODE_ID = "Q05"
EXPECTED_JOB_COUNT = 12
MAXIMUM_RUNTIME_SECONDS = 4.0 * 60.0 * 60.0


def load_module(path: Path, name: str) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5246 = load_module(SCRIPT_5246, "mts_5246_for_5248")
M5245 = M5246.M5245
M5244 = M5246.M5244
M5243 = M5246.M5243
M5240 = M5246.M5240

digest = M5246.digest
tree_digest = M5246.tree_digest
serialized_hash = M5246.serialized_hash
atomic_text = M5246.atomic_text
atomic_json = M5246.atomic_json
write_csv = M5246.write_csv

M5246.MARKER = MARKER
M5246.REVISION = REVISION
M5246.TARGET_NODE_ID = TARGET_NODE_ID
M5246.SOURCE = SOURCE
M5246.JOB_CACHE = JOB_CACHE
M5246.STATE_CACHE = STATE_CACHE


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def source_rows() -> list[dict[str, str]]:
    paths = (
        SCRIPT_5246,
        RESULT_5245,
        RESULT_5246,
        RESULT_5247,
        VALIDATION_5247,
        M5243.MANIFEST_5241,
        M5243.WINDING_5241,
        M5243.NODE_ROWS_5241,
    )
    return [
        {"path": str(path), "sha256": digest(path)}
        for path in paths
    ]


def prepare() -> tuple[
    dict[str, Any],
    dict[str, Any],
    list[dict[str, Any]],
]:
    parent_5245 = read_json(RESULT_5245)
    parent_5247 = read_json(RESULT_5247)
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
        "parent_checkpoint": 5247,
        "parent_decision": parent_5247["decision"],
        "transport_checkpoint": 5245,
        "transport_decision": parent_5245["decision"],
        "parent_5240_manifest_hash": (
            parent_manifest["manifest_hash"]
        ),
        "target_node": node,
        "job_count": len(jobs),
        "base_resolution_ladder": list(
            M5246.BASE_RESOLUTION_LADDER
        ),
        "minimum_accepted_base_resolution": (
            M5246.MINIMUM_ACCEPTED_BASE_RESOLUTION
        ),
        "boundary_refinement_target": (
            M5246.BOUNDARY_REFINEMENT_TARGET
        ),
        "maximum_boundary_refinement_depth": (
            M5246.MAXIMUM_BOUNDARY_REFINEMENT_DEPTH
        ),
        "maximum_projective_step": (
            M5246.MAXIMUM_PROJECTIVE_STEP
        ),
        "maximum_reciprocal_residual": (
            M5246.MAXIMUM_RECIPROCAL_RESIDUAL
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
                "This rebuilds only the Q05 winding interval map. "
                "Its inner slice and the full outer cubature remain open."
            ),
        },
    }
    manifest["manifest_hash"] = serialized_hash(manifest)
    validation_5247 = read_csv(VALIDATION_5247)
    checks = {
        "source_paths_exist_and_match": all(
            Path(row["path"]).exists()
            and digest(Path(row["path"])) == row["sha256"]
            for row in manifest["source_files"]
        ),
        "transport_checkpoint_passed": (
            parent_5245["integrity_passed"]
            and parent_5245["acceptance_passed"]
        ),
        "Q03_corrected_pipeline_passed": (
            parent_5247["integrity_passed"]
            and parent_5247["acceptance_passed"]
            and all(row["passed"] == "True" for row in validation_5247)
        ),
        "parent_decision_authorizes_Q05": (
            parent_5247["decision"]
            == (
                "ADOPT_CORRECTED_Q03_INNER_SLICE__"
                "REBUILD_Q05_RECIPROCAL_PROJECTIVE_MAP"
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
        "dry_run_passed": all(checks.values()),
        "checks": checks,
        "manifest_hash": manifest["manifest_hash"],
        "target_node": TARGET_NODE_ID,
        "job_count": len(problems),
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    return manifest, dry_run, problems


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
    rows = M5246.validation_rows(
        manifest,
        attempts,
        intervals,
        transitions,
        summaries,
        comparisons,
        formal_digest,
        elapsed,
    )
    for row in rows:
        row["checkpoint"] = 5248
        if row["gate"] == "Q03_JOB_COUNT_EXACT":
            row["gate"] = "Q05_JOB_COUNT_EXACT"
    return rows


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
        decision = "INVALID_Q05_RECIPROCAL_PROJECTIVE_INTERVAL_REBUILD"
    elif acceptance_passed:
        decision = (
            "ADOPT_Q05_RECIPROCAL_PROJECTIVE_INTERVAL_MAP__"
            "RUN_CORRECTED_INNER_SLICE"
        )
    else:
        decision = (
            "HOLD_Q05_RECIPROCAL_PROJECTIVE_INTERVAL_MAP__"
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
            "# 5248 — Q05 reciprocal-projective interval topology rebuild",
            "",
            "## Method",
            "",
            (
                "The accepted 5245/5246 reciprocal-projective transport "
                "law is applied unchanged to Q05. Collision roots and "
                "reciprocal chamber endpoints share the locally refined "
                "homotopy mesh, with two-resolution state convergence and "
                "all projective, reciprocal, polynomial, and coverage "
                "gates enforced independently for twelve material jobs."
            ),
            "",
            "## Results",
            "",
            f"- Q05 material jobs rebuilt: `{len(summaries)}`.",
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
                "This establishes only Q05 interval topology. It does not "
                "yet change the full outer cubature or support numeric UV, "
                "local-GR, or full-MTS claims."
            ),
            "",
            "## Next exact target",
            "",
            (
                "Use these Q05 rows to reclassify poles, refit retained "
                "residues, and rerun its regulated inner slice under the "
                "same convergence gates."
                if acceptance_passed
                else
                "Resolve the first failed Q05 gate before integration."
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
    manifest, dry_run, problems = prepare()
    atomic_json(MANIFEST, manifest)
    atomic_json(DRY_RUN, dry_run)
    if not dry_run["dry_run_passed"]:
        failed = [
            key
            for key, passed in dry_run["checks"].items()
            if not passed
        ]
        raise RuntimeError(f"5248 dry run failed: {failed}")
    state_cache = M5246.load_state_cache(manifest)
    JOB_CACHE.mkdir(parents=True, exist_ok=True)
    results: list[dict[str, Any]] = []
    cache_flags: list[bool] = []
    for problem in problems:
        result, cache_hit = M5246.derive_job(
            manifest, problem, state_cache
        )
        results.append(result)
        cache_flags.append(cache_hit)
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
            "job_cache_hit": cache_hit,
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
        }
        for result, cache_hit in zip(results, cache_flags)
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
            sum(cache_flags),
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
        "INVALID_Q05_RECIPROCAL_PROJECTIVE_INTERVAL_REBUILD"
        if not integrity_passed
        else (
            "ADOPT_Q05_RECIPROCAL_PROJECTIVE_INTERVAL_MAP__"
            "RUN_CORRECTED_INNER_SLICE"
            if acceptance_passed
            else (
                "HOLD_Q05_RECIPROCAL_PROJECTIVE_INTERVAL_MAP__"
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
        "job_cache_hit_count": sum(cache_flags),
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
        raise RuntimeError(f"5248 integrity validation failed: {failed}")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="validate the Q05 interval-rebuild manifest only",
    )
    arguments = parser.parse_args()
    if arguments.dry_run:
        manifest, dry_run, _ = prepare()
        atomic_json(MANIFEST, manifest)
        atomic_json(DRY_RUN, dry_run)
        print(json.dumps(dry_run, indent=2, sort_keys=True))
        return
    print(json.dumps(execute(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
