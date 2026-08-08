from __future__ import annotations

import argparse
import csv
import hashlib
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
SOURCE = POST / "source-intake" / "functional_rg" / "5242"
RESIDUALS = POST / "source-intake" / "mts_residuals"

SCRIPT_5241 = (
    POST
    / "scripts"
    / "Y5_R2FR_5241_decay_angle_order9_causal_topology_resolution.py"
)
RESULT_5241 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5241"
    / "decay_angle_order9_result.json"
)
MANIFEST_5241 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5241"
    / "decay_angle_order9_manifest.json"
)
WINDING_5241 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5241"
    / "decay_angle_order9_winding_intervals.csv"
)
VALIDATION_5241 = (
    RESIDUALS / "P8_Y5_BRR545_5241_VALIDATION.csv"
)

MANIFEST = SOURCE / "homotopy_branch_resolution_manifest.json"
DRY_RUN = SOURCE / "homotopy_branch_resolution_dry_run.json"
RESULT = SOURCE / "homotopy_branch_resolution_result.json"
ROWS = SOURCE / "homotopy_branch_resolution_ladder.csv"
SUMMARY_ROWS = SOURCE / "homotopy_branch_resolution_summary.csv"
VALIDATION = RESIDUALS / "P8_Y5_BRR545_5242_VALIDATION.csv"
DOCUMENT = (
    POST
    / "5242-Y5-R2FR-homotopy-branch-resolution-or-collision-classifier.md"
)

MARKER = "MTS_5242_HOMOTOPY_BRANCH_RESOLUTION_OR_COLLISION_CLASSIFIER"
REVISION = "homotopy-branch-resolution-or-collision-classifier-v1"
FORMAL_BASELINE = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)

RESOLUTIONS = (1024, 2048, 4096, 8192, 16384, 32768)
TARGET_CASES = (
    ("Q01", "E040", "MC07", "endpoint-positive"),
    ("Q07", "E040", "MC03", "endpoint-positive"),
    ("Q00", "E040", "MC07", "endpoint-negative"),
    ("Q08", "E040", "MC03", "endpoint-negative"),
)
CONTROL_CASE = ("Q06", "E040", "MC04", "resolved-control")
PROJECTIVE_STEP_LIMIT = 0.05
PERSISTENT_RATIO_FLOOR = 0.8
CONVERGENT_RATIO_CEILING = 0.65
NEAR_COLLISION_MARGIN = 1.0e-4
HIGH_RESOLUTION_STABILITY_START = 2048
RECIPROCAL_RESIDUAL_LIMIT = 2.0e-8
MAXIMUM_RUNTIME_SECONDS = 4.0 * 60.0 * 60.0


def load_module(path: Path, name: str) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5241 = load_module(SCRIPT_5241, "mts_5241_for_5242")
M5240 = M5241.M5240
M5239 = M5240.M5239


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
    return [
        {"path": str(path), "sha256": digest(path)}
        for path in (
            SCRIPT_5241,
            RESULT_5241,
            MANIFEST_5241,
            WINDING_5241,
            VALIDATION_5241,
            M5240.SCRIPT_5239,
        )
    ]


def select_case_row(
    winding_rows: list[dict[str, str]],
    order9_node_id: str,
    epsilon_id: str,
    component_id: str,
) -> dict[str, str]:
    candidates = [
        row
        for row in winding_rows
        if row["order9_node_id"] == order9_node_id
        and row["epsilon_id"] == epsilon_id
        and row["component_id"] == component_id
    ]
    if not candidates:
        raise RuntimeError(
            f"missing 5241 case {order9_node_id}/{epsilon_id}/{component_id}"
        )
    return max(
        candidates,
        key=lambda row: float(row["maximum_pair_projective_step"]),
    )


def build_manifest() -> dict[str, Any]:
    winding_rows = read_csv(WINDING_5241)
    case_rows = []
    for node_id, epsilon_id, component_id, role in (
        *TARGET_CASES,
        CONTROL_CASE,
    ):
        source = select_case_row(
            winding_rows, node_id, epsilon_id, component_id
        )
        case_rows.append(
            {
                "case_id": (
                    f"{node_id}_{epsilon_id}_{component_id}_{role}"
                ),
                "case_role": role,
                "order9_node_id": node_id,
                "execution_node_id": source["execution_node_id"],
                "decay_cosine": float(source["decay_cosine"]),
                "epsilon_id": epsilon_id,
                "component_id": component_id,
                "family": source["family"],
                "soft_cosine": float(source["interval_midpoint"]),
                "source_state_u": int(source["state_u"]),
                "source_state_v": int(source["state_v"]),
                "source_projective_step": float(
                    source["maximum_pair_projective_step"]
                ),
                "source_branch_margin": float(
                    source["minimum_alternate_branch_separation"]
                ),
                "source_topology_steps": int(source["topology_steps"]),
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    manifest = {
        "marker": MARKER,
        "revision": REVISION,
        "parent_checkpoint": 5241,
        "parent_decision": read_json(RESULT_5241)["decision"],
        "resolutions": list(RESOLUTIONS),
        "target_case_count": len(TARGET_CASES),
        "control_case_count": 1,
        "scheduled_homotopy_tracks": (
            (len(TARGET_CASES) + 1) * len(RESOLUTIONS)
        ),
        "classification_thresholds": {
            "projective_step_limit": PROJECTIVE_STEP_LIMIT,
            "persistent_ratio_floor": PERSISTENT_RATIO_FLOOR,
            "convergent_ratio_ceiling": CONVERGENT_RATIO_CEILING,
            "near_collision_margin": NEAR_COLLISION_MARGIN,
            "high_resolution_stability_start": (
                HIGH_RESOLUTION_STABILITY_START
            ),
            "reciprocal_residual_limit": RECIPROCAL_RESIDUAL_LIMIT,
        },
        "source_files": source_rows(),
        "cases": case_rows,
        "claim_boundary": {
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
            "reason": (
                "This classifies five local homotopy tracks; it does not "
                "repair or integrate the outer decay-angle topology."
            ),
        },
    }
    manifest["manifest_hash"] = serialized_hash(manifest)
    return manifest


def write_manifest_and_dry_run() -> dict[str, Any]:
    manifest = build_manifest()
    checks = {
        "source_paths_exist_and_match": all(
            Path(row["path"]).exists()
            and digest(Path(row["path"])) == row["sha256"]
            for row in manifest["source_files"]
        ),
        "parent_decision_is_outer_topology_hold": (
            manifest["parent_decision"]
            == "HOLD_OUTER_CUBATURE__DERIVE_PIECEWISE_DECAY_TOPOLOGY"
        ),
        "case_count_exact": (
            len(manifest["cases"]) == len(TARGET_CASES) + 1
        ),
        "resolution_ladder_exact": (
            manifest["resolutions"] == list(RESOLUTIONS)
        ),
        "source_rows_are_4096_confirmation_states": all(
            int(row["source_topology_steps"]) == 4096
            for row in manifest["cases"]
        ),
        "claims_locked_false": all(
            not bool(manifest["claim_boundary"][field])
            for field in (
                "valid_for_numeric_UV_claim",
                "valid_for_local_GR_claim",
                "valid_for_full_MTS_claim",
            )
        ),
        "formal_digest_unchanged": (
            tree_digest(FORMAL) == FORMAL_BASELINE
        ),
    }
    report = {
        "marker": MARKER,
        "revision": REVISION,
        "dry_run_passed": all(checks.values()),
        "checks": checks,
        "manifest_hash": manifest["manifest_hash"],
        "scheduled_homotopy_tracks": manifest[
            "scheduled_homotopy_tracks"
        ],
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(MANIFEST, manifest)
    atomic_json(DRY_RUN, report)
    if not report["dry_run_passed"]:
        failed = [key for key, passed in checks.items() if not passed]
        raise RuntimeError(f"5242 dry run failed: {failed}")
    return report


def build_problem_for_case(
    case: dict[str, Any],
    parent_manifest: dict[str, Any],
    base_jobs: list[dict[str, Any]],
    tracks: dict[str, dict[str, Any]],
) -> dict[str, Any]:
    source_node = next(
        row
        for row in read_json(MANIFEST_5241)["outer_nodes"]
        if row["order9_node_id"] == case["order9_node_id"]
    )
    node = {
        "outer_node_id": case["execution_node_id"],
        "master_index": int(source_node["master_index"]),
        "decay_cosine": float(case["decay_cosine"]),
    }
    jobs = M5240.material_node_jobs(node, base_jobs, tracks)
    job = next(
        row
        for row in jobs
        if row["epsilon_id"] == case["epsilon_id"]
        and row["component_id"] == case["component_id"]
    )
    return M5240.build_node_problem(job)


def classify_case(rows: list[dict[str, Any]]) -> dict[str, Any]:
    ordered = sorted(rows, key=lambda row: int(row["topology_steps"]))
    asymptotic_rows = [
        row
        for row in ordered
        if int(row["topology_steps"])
        >= HIGH_RESOLUTION_STABILITY_START
    ]
    states = {
        (int(row["state_u"]), int(row["state_v"]))
        for row in asymptotic_rows
    }
    high = ordered[-1]
    previous = ordered[-2]
    step_ratio = float(high["maximum_pair_projective_step"]) / max(
        float(previous["maximum_pair_projective_step"]), 1.0e-300
    )
    state_stable = len(states) == 1
    high_step = float(high["maximum_pair_projective_step"])
    high_margin = float(high["minimum_alternate_branch_separation"])
    high_reciprocal_residual = float(
        high["maximum_reciprocal_product_residual"]
    )
    if (
        state_stable
        and high_step <= PROJECTIVE_STEP_LIMIT
        and step_ratio <= CONVERGENT_RATIO_CEILING
        and high_reciprocal_residual <= RECIPROCAL_RESIDUAL_LIMIT
    ):
        classification = "RESOLUTION_CONVERGED"
    elif (
        state_stable
        and step_ratio <= CONVERGENT_RATIO_CEILING
        and high_reciprocal_residual > RECIPROCAL_RESIDUAL_LIMIT
    ):
        classification = (
            "PROJECTIVE_CONVERGENCE_BREAKS_RECIPROCAL_IDENTITY"
        )
    elif (
        state_stable
        and high_step > PROJECTIVE_STEP_LIMIT
        and step_ratio >= PERSISTENT_RATIO_FLOOR
        and high_margin <= NEAR_COLLISION_MARGIN
    ):
        classification = "PERSISTENT_NEAR_COLLISION_BRANCH_JUMP"
    elif not state_stable:
        classification = "WINDING_STATE_NOT_RESOLUTION_STABLE"
    else:
        classification = "UNRESOLVED_REFINEMENT"
    return {
        "case_id": high["case_id"],
        "case_role": high["case_role"],
        "order9_node_id": high["order9_node_id"],
        "epsilon_id": high["epsilon_id"],
        "component_id": high["component_id"],
        "family": high["family"],
        "decay_cosine": high["decay_cosine"],
        "soft_cosine": high["soft_cosine"],
        "state_stable_on_asymptotic_ladder": state_stable,
        "distinct_state_count": len(states),
        "high_resolution_state_u": high["state_u"],
        "high_resolution_state_v": high["state_v"],
        "high_resolution_dynamic_multiplier": high[
            "dynamic_multiplier"
        ],
        "high_resolution_projective_step": high_step,
        "high_resolution_branch_margin": high_margin,
        "high_resolution_reciprocal_product_residual": (
            high_reciprocal_residual
        ),
        "step_ratio_32768_to_16384": step_ratio,
        "classification": classification,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }


def validation_rows(
    manifest: dict[str, Any],
    summaries: list[dict[str, Any]],
    formal_digest: str,
    elapsed: float,
) -> list[dict[str, Any]]:
    targets = [
        row for row in summaries if row["case_role"] != "resolved-control"
    ]
    controls = [
        row for row in summaries if row["case_role"] == "resolved-control"
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
            "HOMOTOPY_TRACK_COUNT",
            len(summaries) == len(TARGET_CASES) + 1,
            len(summaries),
            len(TARGET_CASES) + 1,
        ),
        (
            "integrity",
            "CONTROL_TRACK_RESOLVES",
            (
                len(controls) == 1
                and controls[0]["classification"]
                == "RESOLUTION_CONVERGED"
            ),
            (
                controls[0]["classification"]
                if controls
                else "MISSING_CONTROL"
            ),
            "RESOLUTION_CONVERGED",
        ),
        (
            "acceptance",
            "TARGET_BRANCH_TRACKS_RESOLVE",
            all(
                row["classification"] == "RESOLUTION_CONVERGED"
                for row in targets
            ),
            "|".join(
                str(row["classification"]) for row in targets
            ),
            "all RESOLUTION_CONVERGED",
        ),
        (
            "acceptance",
            "TARGET_ASYMPTOTIC_WINDING_STATES_STABLE",
            all(
                bool(row["state_stable_on_asymptotic_ladder"])
                for row in targets
            ),
            (
                f"{sum(bool(row['state_stable_on_asymptotic_ladder']) for row in targets)}"
                f"/{len(targets)}"
            ),
            f"{len(targets)}/{len(targets)}",
        ),
        (
            "acceptance",
            "TARGET_RECIPROCAL_IDENTITY_PRESERVED",
            all(
                float(
                    row[
                        "high_resolution_reciprocal_product_residual"
                    ]
                )
                <= RECIPROCAL_RESIDUAL_LIMIT
                for row in targets
            ),
            max(
                float(
                    row[
                        "high_resolution_reciprocal_product_residual"
                    ]
                )
                for row in targets
            ),
            RECIPROCAL_RESIDUAL_LIMIT,
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
            "checkpoint": 5242,
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
    summaries: list[dict[str, Any]],
    validations: list[dict[str, Any]],
    elapsed: float,
) -> str:
    target_rows = [
        row for row in summaries if row["case_role"] != "resolved-control"
    ]
    persistent = [
        row
        for row in target_rows
        if row["classification"]
        == "PROJECTIVE_CONVERGENCE_BREAKS_RECIPROCAL_IDENTITY"
    ]
    integrity_passed = all(
        bool(row["passed"])
        for row in validations
        if row["gate_kind"] == "integrity"
    )
    target_resolved = all(
        row["classification"] == "RESOLUTION_CONVERGED"
        for row in target_rows
    )
    if not integrity_passed:
        decision = "INVALID_HOMOTOPY_CLASSIFIER"
    elif target_resolved:
        decision = "ADOPT_HIGHER_HOMOTOPY_RESOLUTION"
    elif len(persistent) == len(target_rows):
        decision = (
            "REJECT_RESOLUTION_ONLY_REPAIR__DERIVE_COUPLED_RECIPROCAL_BRANCH_TRACK"
        )
    else:
        decision = "HOLD_MIXED_HOMOTOPY_FAILURE"
    if target_resolved:
        consequence = (
            "The fixed 1024/4096 winding ladder used by 5239-5241 is "
            "insufficient for these near-collision states. At 32768 steps "
            "the projective step falls below 0.05, the asymptotic winding "
            "state is stable, and reciprocal identity returns below "
            "2e-8. The next repair is an adaptive doubling evaluator that "
            "requires both projective-step and reciprocal-residual gates "
            "before accepting a winding state."
        )
        next_target = (
            "Rebuild the Q03/Q05 high-chatter winding intervals with "
            "adaptive 1024-to-32768 confirmation, compare transition "
            "counts with the fixed-resolution intervals, and only then "
            "rerun their inner integrals."
        )
    else:
        consequence = (
            "If the projective step converges while reciprocal identity "
            "fails, blindly increasing homotopy resolution is not the "
            "repair. The representative and reciprocal roots must be "
            "continued as one constrained pair satisfying "
            "`r_rep r_rec = 1`."
        )
        next_target = (
            "Derive the paired reciprocal continuation before rerunning "
            "the decay-angle cubature."
        )
    lines = [
        "# 5242 — Homotopy branch resolution or collision classifier",
        "",
        "## Purpose",
        "",
        (
            "Test whether the failed 5240/5241 winding-resolution gate is "
            "fixed by adding homotopy samples, or whether MC03/MC07 retain "
            "a finite branch jump near a collision."
        ),
        "",
        "## Resolution ladder",
        "",
        "`1024 → 2048 → 4096 → 8192 → 16384 → 32768` homotopy steps.",
        "",
        "## Results",
        "",
    ]
    for row in summaries:
        lines.append(
            f"- `{row['case_id']}`: `{row['classification']}`; "
            f"state `({row['high_resolution_state_u']},"
            f"{row['high_resolution_state_v']})`; "
            f"step `{float(row['high_resolution_projective_step']):.12g}`; "
            f"ratio `{float(row['step_ratio_32768_to_16384']):.12g}`; "
            f"reciprocal residual "
            f"`{float(row['high_resolution_reciprocal_product_residual']):.12g}`; "
            f"margin `{float(row['high_resolution_branch_margin']):.12g}`."
        )
    lines.extend(
        [
            f"- Runtime: `{elapsed:.3f} s`.",
            "",
            "## Decision",
            "",
            f"`{decision}`",
            "",
            "## Consequence",
            "",
            consequence,
            "",
            "## Next exact target",
            "",
            next_target,
            "",
            "## Claim boundary",
            "",
            (
                "This is a numerical branch-classification result, not a "
                "UV coefficient, local-GR derivation, or full-MTS claim."
            ),
            "",
        ]
    )
    return "\n".join(lines)


def remove_project_pycache() -> None:
    target = POST / "scripts" / "__pycache__"
    if target.exists():
        shutil.rmtree(target)


def execute() -> dict[str, Any]:
    started = time.perf_counter()
    dry_run = write_manifest_and_dry_run()
    manifest = read_json(MANIFEST)
    parent_manifest, matches, base_jobs, _ = M5240.build_manifest()
    event = dict(parent_manifest["target_event"])
    tracks, _ = M5240.build_outer_branch_tracks(matches, event)

    ladder_rows: list[dict[str, Any]] = []
    summary_rows: list[dict[str, Any]] = []
    for case in manifest["cases"]:
        problem = build_problem_for_case(
            case, parent_manifest, base_jobs, tracks
        )
        local_rows: list[dict[str, Any]] = []
        for steps in RESOLUTIONS:
            track_started = time.perf_counter()
            state = M5239.winding_state(
                problem, float(case["soft_cosine"]), steps
            )
            row = {
                "case_id": case["case_id"],
                "case_role": case["case_role"],
                "order9_node_id": case["order9_node_id"],
                "execution_node_id": case["execution_node_id"],
                "epsilon_id": case["epsilon_id"],
                "component_id": case["component_id"],
                "family": case["family"],
                "decay_cosine": case["decay_cosine"],
                "soft_cosine": case["soft_cosine"],
                "topology_steps": steps,
                "state_u": state["u"],
                "state_v": state["v"],
                "dynamic_delta": state["dynamic_delta"],
                "source_delta": state["source_delta"],
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
                "track_elapsed_seconds": (
                    time.perf_counter() - track_started
                ),
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
            local_rows.append(row)
            ladder_rows.append(row)
        summary_rows.append(classify_case(local_rows))

    formal_digest = tree_digest(FORMAL)
    elapsed = time.perf_counter() - started
    validations = validation_rows(
        manifest, summary_rows, formal_digest, elapsed
    )
    write_csv(ROWS, ladder_rows)
    write_csv(SUMMARY_ROWS, summary_rows)
    write_csv(VALIDATION, validations)
    atomic_text(
        DOCUMENT,
        render_document(summary_rows, validations, elapsed),
    )

    integrity_passed = all(
        bool(row["passed"])
        for row in validations
        if row["gate_kind"] == "integrity"
    )
    target_resolved = all(
        row["classification"] == "RESOLUTION_CONVERGED"
        for row in summary_rows
        if row["case_role"] != "resolved-control"
    )
    persistent = all(
        row["classification"]
        == "PROJECTIVE_CONVERGENCE_BREAKS_RECIPROCAL_IDENTITY"
        for row in summary_rows
        if row["case_role"] != "resolved-control"
    )
    if not integrity_passed:
        decision = "INVALID_HOMOTOPY_CLASSIFIER"
    elif target_resolved:
        decision = "ADOPT_HIGHER_HOMOTOPY_RESOLUTION"
    elif persistent:
        decision = (
            "REJECT_RESOLUTION_ONLY_REPAIR__DERIVE_COUPLED_RECIPROCAL_BRANCH_TRACK"
        )
    else:
        decision = "HOLD_MIXED_HOMOTOPY_FAILURE"
    result = {
        "marker": MARKER,
        "revision": REVISION,
        "dry_run": dry_run,
        "manifest_hash": manifest["manifest_hash"],
        "decision": decision,
        "integrity_passed": integrity_passed,
        "target_tracks_resolved": target_resolved,
        "target_tracks_break_reciprocal_identity": persistent,
        "summary": summary_rows,
        "formalization_workbench_digest": formal_digest,
        "elapsed_seconds": elapsed,
        "outputs": [
            str(path)
            for path in (
                MANIFEST,
                DRY_RUN,
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
            and not bool(row["passed"])
        ]
        raise RuntimeError(f"5242 integrity validation failed: {failed}")
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="validate the bounded homotopy-resolution ladder only",
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
