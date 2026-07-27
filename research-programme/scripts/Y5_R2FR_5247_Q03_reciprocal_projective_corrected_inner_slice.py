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
SOURCE = POST / "source-intake" / "functional_rg" / "5247"
RESIDUALS = POST / "source-intake" / "mts_residuals"

SCRIPT_5246 = (
    POST
    / "scripts"
    / "Y5_R2FR_5246_Q03_reciprocal_projective_interval_topology_rebuild.py"
)
RESULT_5246 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5246"
    / "Q03_reciprocal_projective_interval_result.json"
)
INTERVALS_5246 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5246"
    / "Q03_reciprocal_projective_intervals.csv"
)
VALIDATION_5246 = (
    RESIDUALS / "P8_Y5_BRR545_5246_VALIDATION.csv"
)

MANIFEST = SOURCE / "Q03_corrected_inner_slice_manifest.json"
DRY_RUN = SOURCE / "Q03_corrected_inner_slice_dry_run.json"
RESULT = SOURCE / "Q03_corrected_inner_slice_result.json"
NODE_ROW = SOURCE / "Q03_corrected_inner_slice_summary.csv"
ZERO_ROWS = SOURCE / "Q03_corrected_structural_zero_audit.csv"
CLOSURE_ROWS = SOURCE / "Q03_corrected_dynamic_closure.csv"
SCAN_ROWS = SOURCE / "Q03_corrected_scan.csv"
POLE_ROWS = SOURCE / "Q03_corrected_pole_catalog.csv"
TOPOLOGY_ROWS = SOURCE / "Q03_corrected_pole_topology.csv"
RESIDUE_ROWS = SOURCE / "Q03_corrected_residue_fits.csv"
QUADRATURE_ROWS = SOURCE / "Q03_corrected_inner_quadrature.csv"
EXTRAPOLATION_ROWS = SOURCE / "Q03_corrected_regulator_extrapolation.csv"
VALIDATION = RESIDUALS / "P8_Y5_BRR545_5247_VALIDATION.csv"
DOCUMENT = (
    POST
    / "5247-Y5-R2FR-Q03-reciprocal-projective-corrected-inner-slice.md"
)

MARKER = "MTS_5247_Q03_RECIPROCAL_PROJECTIVE_CORRECTED_INNER_SLICE"
REVISION = "Q03-reciprocal-projective-corrected-inner-slice-v1"
FORMAL_BASELINE = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)

TARGET_NODE_ID = "Q03"
EXPECTED_JOB_COUNT = 12
MAXIMUM_DYNAMIC_CLOSURE_RESIDUAL = 2.0e-10
MAXIMUM_RUNTIME_SECONDS = 2.0 * 60.0 * 60.0


def load_module(path: Path, name: str) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5246 = load_module(SCRIPT_5246, "mts_5246_for_5247")
M5245 = M5246.M5245
M5244 = M5246.M5244
M5243 = M5246.M5243
M5240 = M5246.M5240
M5239 = M5246.M5239

digest = M5246.digest
tree_digest = M5246.tree_digest
serialized_hash = M5246.serialized_hash
atomic_text = M5246.atomic_text
atomic_json = M5246.atomic_json
write_csv = M5246.write_csv


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def complex_row(value: complex) -> dict[str, float]:
    return {
        "real": float(value.real),
        "imaginary": float(value.imag),
    }


def source_rows() -> list[dict[str, str]]:
    paths = (
        SCRIPT_5246,
        RESULT_5246,
        INTERVALS_5246,
        VALIDATION_5246,
        M5246.SCRIPT_5245,
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
    parent_5246 = read_json(RESULT_5246)
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
    intervals = read_csv(INTERVALS_5246)
    manifest = {
        "marker": MARKER,
        "revision": REVISION,
        "parent_checkpoint": 5246,
        "parent_decision": parent_5246["decision"],
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
                "Only one decay-angle node is recalculated. The full "
                "outer cubature and Q05 correction remain outstanding."
            ),
        },
    }
    manifest["manifest_hash"] = serialized_hash(manifest)
    validation_5246 = read_csv(VALIDATION_5246)
    interval_jobs = {row["job_id"] for row in intervals}
    problem_jobs = {problem["job"]["job_id"] for problem in problems}
    dry_checks = {
        "source_paths_exist_and_match": all(
            Path(row["path"]).exists()
            and digest(Path(row["path"])) == row["sha256"]
            for row in manifest["source_files"]
        ),
        "parent_5246_integrity_and_acceptance_pass": (
            parent_5246["integrity_passed"]
            and parent_5246["acceptance_passed"]
            and all(row["passed"] == "True" for row in validation_5246)
        ),
        "parent_decision_authorizes_inner_slice": (
            parent_5246["decision"]
            == (
                "ADOPT_Q03_RECIPROCAL_PROJECTIVE_INTERVAL_MAP__"
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
        "dry_run_passed": all(dry_checks.values()),
        "checks": dry_checks,
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


def corrected_inner_slice(
    context: dict[str, Any],
    problems: list[dict[str, Any]],
    intervals: list[dict[str, str]],
) -> dict[str, Any]:
    execution_node = context["execution_node"]
    intervals_by_job = M5239.interval_rows_by_job(intervals)
    problems_by_epsilon: dict[str, list[dict[str, Any]]] = {
        epsilon_id: [] for epsilon_id in M5239.EPSILON_IDS
    }
    for problem in problems:
        problems_by_epsilon[
            problem["job"]["epsilon_id"]
        ].append(problem)

    scan_rows: list[dict[str, Any]] = []
    poles: list[dict[str, Any]] = []
    topology_rows: list[dict[str, Any]] = []
    poles_by_job: dict[str, list[dict[str, Any]]] = {}
    for problem in problems:
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
            pole["causal_family_active"] = (
                abs(multiplier) > 1.0e-12
            )
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
            float(row["real_axis_center"])
            for row in regulator_poles
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

    closure_rows = M5240.dynamic_closure_audit(
        execution_node, problems_by_epsilon, intervals_by_job
    )
    zero_rows = M5240.structural_zero_audit(
        execution_node,
        context["matches"],
        context["tracks"],
        context["event"],
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
    physical_values = M5240.physical_slice_values(
        extrapolation_rows
    )
    active_poles = [
        row for row in poles if bool(row["causal_family_active"])
    ]
    return {
        "scan_rows": M5240.qualify_rows(
            scan_rows, execution_node
        ),
        "pole_rows": M5240.qualify_rows(poles, execution_node),
        "topology_rows": M5240.qualify_rows(
            topology_rows, execution_node
        ),
        "residue_rows": M5240.qualify_rows(fits, execution_node),
        "closure_rows": closure_rows,
        "zero_rows": M5240.qualify_rows(
            zero_rows, execution_node
        ),
        "quadrature_rows": M5240.qualify_rows(
            quadrature_rows, execution_node
        ),
        "extrapolation_rows": M5240.qualify_rows(
            extrapolation_rows, execution_node
        ),
        "coverage_rows": coverage_rows,
        "convergence": convergence,
        "physical_values": physical_values,
        "geometric_pole_count": len(poles),
        "active_pole_count": len(active_poles),
        "fit_count": len(fits),
    }


def validation_rows(
    manifest: dict[str, Any],
    calculation: dict[str, Any],
    corrected: complex,
    formal_digest: str,
    elapsed: float,
) -> list[dict[str, Any]]:
    fits = calculation["residue_rows"]
    zero_rows = calculation["zero_rows"]
    closure_rows = calculation["closure_rows"]
    coverage_rows = calculation["coverage_rows"]
    convergence = calculation["convergence"]
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
            "PARENT_INTERVAL_GATE_PASSED",
            read_json(RESULT_5246)["acceptance_passed"],
            read_json(RESULT_5246)["decision"],
            (
                "ADOPT_Q03_RECIPROCAL_PROJECTIVE_INTERVAL_MAP__"
                "RUN_CORRECTED_INNER_SLICE"
            ),
        ),
        (
            "acceptance",
            "ALL_STRUCTURAL_ZERO_ROWS_PASS",
            all(
                bool(row["structural_zero_passed"])
                for row in zero_rows
            ),
            (
                f"{sum(bool(row['structural_zero_passed']) for row in zero_rows)}"
                f"/{len(zero_rows)}"
            ),
            f"{len(zero_rows)}/{len(zero_rows)}",
        ),
        (
            "acceptance",
            "DYNAMIC_CLOSURE_PASSES",
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
            "acceptance",
            "ACTIVE_POLES_HAVE_ONE_ACCEPTED_FIT",
            calculation["fit_count"]
            == calculation["active_pole_count"]
            and all(bool(row["fit_passed"]) for row in fits),
            (
                f"{sum(bool(row['fit_passed']) for row in fits)} "
                f"fits/{calculation['active_pole_count']} active poles"
            ),
            "one passing fit per active pole",
        ),
        (
            "acceptance",
            "INNER_COVERAGE_CLOSES",
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
            "acceptance",
            "LOW_ORDER_EXTRAPOLATION_CONVERGES",
            convergence["low_order_subtracted_relative_error"]
            <= M5239.LOW_ORDER_SUBTRACTED_RELATIVE_ERROR_LIMIT,
            convergence["low_order_subtracted_relative_error"],
            M5239.LOW_ORDER_SUBTRACTED_RELATIVE_ERROR_LIMIT,
        ),
        (
            "acceptance",
            "MID_ORDER_EXTRAPOLATION_CONVERGES",
            convergence["mid_order_subtracted_relative_error"]
            <= M5239.MID_ORDER_SUBTRACTED_RELATIVE_ERROR_LIMIT,
            convergence["mid_order_subtracted_relative_error"],
            M5239.MID_ORDER_SUBTRACTED_RELATIVE_ERROR_LIMIT,
        ),
        (
            "acceptance",
            "CORRECTED_Q03_VALUE_FINITE",
            math.isfinite(corrected.real)
            and math.isfinite(corrected.imag),
            str(corrected),
            "finite complex value",
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
            "checkpoint": 5247,
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
        decision = "INVALID_Q03_CORRECTED_INNER_SLICE"
    elif acceptance_passed:
        decision = (
            "ADOPT_CORRECTED_Q03_INNER_SLICE__"
            "REBUILD_Q05_RECIPROCAL_PROJECTIVE_MAP"
        )
    else:
        decision = (
            "HOLD_Q03_CORRECTED_INNER_SLICE__"
            "LOCALIZE_FAILED_INTEGRATION_GATE"
        )
    return "\n".join(
        [
            "# 5247 — Q03 reciprocal-projective corrected inner slice",
            "",
            "## Calculation",
            "",
            (
                "The 5246 interval map is used without reinterpretation "
                "to classify every geometric pole. Only poles in a "
                "nonzero corrected winding interval remain active; those "
                "residues are refitted before the regulated inner "
                "quadrature and E020/E040 extrapolation are rerun."
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
                "- Fixed Q03 order-512 subtracted value: "
                f"`{summary['fixed_value']}`."
            ),
            (
                "- Corrected Q03 order-512 subtracted value: "
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
                "This is one corrected outer node, not the full order-9 "
                "angular result. It cannot support a numeric UV, local-GR, "
                "or full-MTS claim until Q05 and the remaining affected "
                "outer nodes are treated under the same transport law."
            ),
            "",
            "## Next exact target",
            "",
            (
                "Apply the 5245 reciprocal-projective transport and 5246 "
                "adaptive mesh contract to all twelve Q05 jobs, rebuild "
                "its interval map, and rerun its corrected inner slice."
                if acceptance_passed
                else
                "Resolve the failed Q03 integration gate without changing "
                "the accepted 5246 topology map."
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
        raise RuntimeError(f"5247 dry run failed: {failed}")

    calculation = corrected_inner_slice(
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
        "INVALID_Q03_CORRECTED_INNER_SLICE"
        if not integrity_passed
        else (
            "ADOPT_CORRECTED_Q03_INNER_SLICE__"
            "REBUILD_Q05_RECIPROCAL_PROJECTIVE_MAP"
            if acceptance_passed
            else (
                "HOLD_Q03_CORRECTED_INNER_SLICE__"
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
        raise RuntimeError(f"5247 integrity validation failed: {failed}")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="validate the corrected Q03 inner-slice manifest only",
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
