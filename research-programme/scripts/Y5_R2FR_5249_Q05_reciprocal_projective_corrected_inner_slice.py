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
SOURCE = POST / "source-intake" / "functional_rg" / "5249"
RESIDUALS = POST / "source-intake" / "mts_residuals"

SCRIPT_5247 = (
    POST
    / "scripts"
    / "Y5_R2FR_5247_Q03_reciprocal_projective_corrected_inner_slice.py"
)
SCRIPT_5248 = (
    POST
    / "scripts"
    / "Y5_R2FR_5248_Q05_reciprocal_projective_interval_topology_rebuild.py"
)
RESULT_5248 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5248"
    / "Q05_reciprocal_projective_interval_result.json"
)
INTERVALS_5248 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5248"
    / "Q05_reciprocal_projective_intervals.csv"
)
VALIDATION_5248 = (
    RESIDUALS / "P8_Y5_BRR545_5248_VALIDATION.csv"
)

MANIFEST = SOURCE / "Q05_corrected_inner_slice_manifest.json"
DRY_RUN = SOURCE / "Q05_corrected_inner_slice_dry_run.json"
RESULT = SOURCE / "Q05_corrected_inner_slice_result.json"
NODE_ROW = SOURCE / "Q05_corrected_inner_slice_summary.csv"
ZERO_ROWS = SOURCE / "Q05_corrected_structural_zero_audit.csv"
CLOSURE_ROWS = SOURCE / "Q05_corrected_dynamic_closure.csv"
SCAN_ROWS = SOURCE / "Q05_corrected_scan.csv"
POLE_ROWS = SOURCE / "Q05_corrected_pole_catalog.csv"
TOPOLOGY_ROWS = SOURCE / "Q05_corrected_pole_topology.csv"
RESIDUE_ROWS = SOURCE / "Q05_corrected_residue_fits.csv"
QUADRATURE_ROWS = SOURCE / "Q05_corrected_inner_quadrature.csv"
EXTRAPOLATION_ROWS = SOURCE / "Q05_corrected_regulator_extrapolation.csv"
VALIDATION = RESIDUALS / "P8_Y5_BRR545_5249_VALIDATION.csv"
DOCUMENT = (
    POST
    / "5249-Y5-R2FR-Q05-reciprocal-projective-corrected-inner-slice.md"
)

MARKER = "MTS_5249_Q05_RECIPROCAL_PROJECTIVE_CORRECTED_INNER_SLICE"
REVISION = "Q05-reciprocal-projective-corrected-inner-slice-v1"
FORMAL_BASELINE = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)
TARGET_NODE_ID = "Q05"
EXPECTED_JOB_COUNT = 12
MAXIMUM_RUNTIME_SECONDS = 2.0 * 60.0 * 60.0


def load_module(path: Path, name: str) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5247 = load_module(SCRIPT_5247, "mts_5247_for_5249")
M5248 = load_module(SCRIPT_5248, "mts_5248_for_5249")
M5246 = M5248.M5246
M5243 = M5248.M5243
M5240 = M5248.M5240
M5239 = M5246.M5239

digest = M5248.digest
tree_digest = M5248.tree_digest
serialized_hash = M5248.serialized_hash
atomic_text = M5248.atomic_text
atomic_json = M5248.atomic_json
write_csv = M5248.write_csv


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def source_rows() -> list[dict[str, str]]:
    paths = (
        SCRIPT_5247,
        SCRIPT_5248,
        RESULT_5248,
        INTERVALS_5248,
        VALIDATION_5248,
        M5243.NODE_ROWS_5241,
        M5243.MANIFEST_5241,
    )
    return [
        {"path": str(path), "sha256": digest(path)}
        for path in paths
    ]


def prepare() -> tuple[
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    list[dict[str, Any]],
    list[dict[str, str]],
]:
    parent_5248 = read_json(RESULT_5248)
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
    intervals = read_csv(INTERVALS_5248)
    manifest = {
        "marker": MARKER,
        "revision": REVISION,
        "parent_checkpoint": 5248,
        "parent_decision": parent_5248["decision"],
        "parent_5240_manifest_hash": (
            parent_manifest["manifest_hash"]
        ),
        "target_node": node,
        "job_count": len(jobs),
        "interval_count": len(intervals),
        "source_files": source_rows(),
        "claim_boundary": {
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
            "reason": (
                "Only Q05 is recalculated here. The full corrected "
                "outer cubature is not yet assembled."
            ),
        },
    }
    manifest["manifest_hash"] = serialized_hash(manifest)
    validation_5248 = read_csv(VALIDATION_5248)
    interval_jobs = {row["job_id"] for row in intervals}
    problem_jobs = {problem["job"]["job_id"] for problem in problems}
    checks = {
        "source_paths_exist_and_match": all(
            Path(row["path"]).exists()
            and digest(Path(row["path"])) == row["sha256"]
            for row in manifest["source_files"]
        ),
        "parent_5248_integrity_and_acceptance_pass": (
            parent_5248["integrity_passed"]
            and parent_5248["acceptance_passed"]
            and all(row["passed"] == "True" for row in validation_5248)
        ),
        "parent_decision_authorizes_inner_slice": (
            parent_5248["decision"]
            == (
                "ADOPT_Q05_RECIPROCAL_PROJECTIVE_INTERVAL_MAP__"
                "RUN_CORRECTED_INNER_SLICE"
            )
        ),
        "target_node_exact": (
            node["order9_node_id"] == TARGET_NODE_ID
        ),
        "job_count_exact": len(problems) == EXPECTED_JOB_COUNT,
        "interval_job_coverage_exact": (
            interval_jobs == problem_jobs
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
        "dry_run_passed": all(checks.values()),
        "checks": checks,
        "manifest_hash": manifest["manifest_hash"],
        "target_node": TARGET_NODE_ID,
        "job_count": len(problems),
        "interval_count": len(intervals),
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    context = {
        "node": node,
        "execution_node": execution_node,
        "event": event,
        "matches": matches,
        "tracks": tracks,
    }
    return manifest, dry_run, context, problems, intervals


def validation_rows(
    manifest: dict[str, Any],
    calculation: dict[str, Any],
    corrected: complex,
    formal_digest: str,
    elapsed: float,
) -> list[dict[str, Any]]:
    original_parent = M5247.RESULT_5246
    M5247.RESULT_5246 = RESULT_5248
    try:
        rows = M5247.validation_rows(
            manifest,
            calculation,
            corrected,
            formal_digest,
            elapsed,
        )
    finally:
        M5247.RESULT_5246 = original_parent
    for row in rows:
        row["checkpoint"] = 5249
        if row["gate"] == "PARENT_INTERVAL_GATE_PASSED":
            row["required"] = (
                "ADOPT_Q05_RECIPROCAL_PROJECTIVE_INTERVAL_MAP__"
                "RUN_CORRECTED_INNER_SLICE"
            )
    return rows


def render_document(
    summary: dict[str, Any],
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
    if not integrity_passed:
        decision = "INVALID_Q05_CORRECTED_INNER_SLICE"
    elif acceptance_passed:
        decision = (
            "ADOPT_CORRECTED_Q05_INNER_SLICE__"
            "ASSESS_TWO_NODE_OUTER_IMPACT"
        )
    else:
        decision = (
            "HOLD_Q05_CORRECTED_INNER_SLICE__"
            "LOCALIZE_FAILED_INTEGRATION_GATE"
        )
    return "\n".join(
        [
            "# 5249 — Q05 reciprocal-projective corrected inner slice",
            "",
            "## Calculation",
            "",
            (
                "The accepted 5248 interval map directly classifies Q05 "
                "geometric poles. Retained residues are refitted, then "
                "the regulated inner quadrature and E020/E040 "
                "extrapolation are rerun under the same gates as Q03."
            ),
            "",
            "## Results",
            "",
            (
                f"- Geometric poles: "
                f"`{summary['geometric_pole_count']}`."
            ),
            (
                f"- Corrected active poles/fits: "
                f"`{summary['active_pole_count']}/{summary['fit_count']}`."
            ),
            (
                "- Fixed Q05 order-512 subtracted value: "
                f"`{summary['fixed_value']}`."
            ),
            (
                "- Corrected Q05 order-512 subtracted value: "
                f"`{summary['corrected_value']}`."
            ),
            (
                "- Corrected-minus-fixed value: "
                f"`{summary['difference']}`."
            ),
            (
                "- Relative change: "
                f"`{summary['relative_change']:.12g}`."
            ),
            (
                "- Low/mid extrapolation errors: "
                f"`{summary['low_order_error']:.12g}`, "
                f"`{summary['mid_order_error']:.12g}`."
            ),
            f"- Runtime: `{elapsed:.3f} s`.",
            "",
            "## Decision",
            "",
            f"`{decision}`",
            "",
            "## Claim boundary",
            "",
            (
                "Q03 and Q05 are corrected nodes, but the order-9 outer "
                "sum still contains inherited values at the other seven "
                "nodes. No numeric UV or broader MTS claim follows yet."
            ),
            "",
            "## Next exact target",
            "",
            (
                "Insert the corrected Q03 and Q05 values into the locked "
                "order-9 outer rule, quantify their weighted change, and "
                "determine which remaining nodes require the paired "
                "topology rebuild before a corrected cubature can close."
                if acceptance_passed
                else
                "Resolve the failed Q05 integration gate without altering "
                "the accepted 5248 topology map."
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
    manifest, dry_run, context, problems, intervals = prepare()
    atomic_json(MANIFEST, manifest)
    atomic_json(DRY_RUN, dry_run)
    if not dry_run["dry_run_passed"]:
        failed = [
            key
            for key, passed in dry_run["checks"].items()
            if not passed
        ]
        raise RuntimeError(f"5249 dry run failed: {failed}")
    calculation = M5247.corrected_inner_slice(
        context, problems, intervals
    )
    corrected = calculation["physical_values"][512]["subtracted"]
    fixed = M5243.fixed_node_value(TARGET_NODE_ID)
    difference = corrected - fixed
    relative_change = abs(difference) / max(abs(fixed), 1.0e-300)
    formal_digest = tree_digest(FORMAL)
    elapsed = time.perf_counter() - started
    validations = validation_rows(
        manifest,
        calculation,
        corrected,
        formal_digest,
        elapsed,
    )
    summary = {
        "order9_node_id": TARGET_NODE_ID,
        "decay_cosine": context["node"]["decay_cosine"],
        "job_count": len(problems),
        "geometric_pole_count": calculation[
            "geometric_pole_count"
        ],
        "active_pole_count": calculation["active_pole_count"],
        "fit_count": calculation["fit_count"],
        "fixed_value": str(fixed),
        "corrected_value": str(corrected),
        "difference": str(difference),
        "relative_change": relative_change,
        "fixed_real": fixed.real,
        "fixed_imaginary": fixed.imag,
        "corrected_real": corrected.real,
        "corrected_imaginary": corrected.imag,
        "difference_real": difference.real,
        "difference_imaginary": difference.imag,
        "low_order_error": calculation["convergence"][
            "low_order_subtracted_relative_error"
        ],
        "mid_order_error": calculation["convergence"][
            "mid_order_subtracted_relative_error"
        ],
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    write_csv(NODE_ROW, [summary])
    write_csv(ZERO_ROWS, calculation["zero_rows"])
    write_csv(CLOSURE_ROWS, calculation["closure_rows"])
    write_csv(SCAN_ROWS, calculation["scan_rows"])
    write_csv(POLE_ROWS, calculation["pole_rows"])
    write_csv(TOPOLOGY_ROWS, calculation["topology_rows"])
    write_csv(RESIDUE_ROWS, calculation["residue_rows"])
    write_csv(QUADRATURE_ROWS, calculation["quadrature_rows"])
    write_csv(
        EXTRAPOLATION_ROWS, calculation["extrapolation_rows"]
    )
    write_csv(VALIDATION, validations)
    atomic_text(
        DOCUMENT,
        render_document(summary, validations, elapsed),
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
        "INVALID_Q05_CORRECTED_INNER_SLICE"
        if not integrity_passed
        else (
            "ADOPT_CORRECTED_Q05_INNER_SLICE__"
            "ASSESS_TWO_NODE_OUTER_IMPACT"
            if acceptance_passed
            else (
                "HOLD_Q05_CORRECTED_INNER_SLICE__"
                "LOCALIZE_FAILED_INTEGRATION_GATE"
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
        "summary": summary,
        "formalization_workbench_digest": formal_digest,
        "elapsed_seconds": elapsed,
        "outputs": [
            str(path)
            for path in (
                MANIFEST,
                DRY_RUN,
                NODE_ROW,
                ZERO_ROWS,
                CLOSURE_ROWS,
                SCAN_ROWS,
                POLE_ROWS,
                TOPOLOGY_ROWS,
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
    if not integrity_passed:
        failed = [
            row["gate"]
            for row in validations
            if row["gate_kind"] == "integrity"
            and not row["passed"]
        ]
        raise RuntimeError(f"5249 integrity validation failed: {failed}")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="validate the corrected Q05 inner-slice manifest only",
    )
    arguments = parser.parse_args()
    if arguments.dry_run:
        manifest, dry_run, _, _, _ = prepare()
        atomic_json(MANIFEST, manifest)
        atomic_json(DRY_RUN, dry_run)
        print(json.dumps(dry_run, indent=2, sort_keys=True))
        return
    print(json.dumps(execute(), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
