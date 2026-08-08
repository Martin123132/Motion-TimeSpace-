from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import math
import os
import shutil
import subprocess
import sys
import time
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE = POST / "source-intake" / "functional_rg" / "5251"
NODES = SOURCE / "nodes"
RESIDUALS = POST / "source-intake" / "mts_residuals"

SCRIPT_5246 = (
    POST
    / "scripts"
    / "Y5_R2FR_5246_Q03_reciprocal_projective_interval_topology_rebuild.py"
)
SCRIPT_5247 = (
    POST
    / "scripts"
    / "Y5_R2FR_5247_Q03_reciprocal_projective_corrected_inner_slice.py"
)
RESULT_5245 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5245"
    / "reciprocal_projective_boundary_result.json"
)
VALIDATION_5245 = (
    RESIDUALS / "P8_Y5_BRR545_5245_VALIDATION.csv"
)
MANIFEST_5241 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5241"
    / "decay_angle_order9_manifest.json"
)
RESULT_5241 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5241"
    / "decay_angle_order9_result.json"
)
NODE_ROWS_5241 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5241"
    / "decay_angle_order9_node_summary.csv"
)
WINDING_5241 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5241"
    / "decay_angle_order9_winding_intervals.csv"
)
RESULT_5247 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5247"
    / "Q03_corrected_inner_slice_result.json"
)
EXTRAPOLATION_5247 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5247"
    / "Q03_corrected_regulator_extrapolation.csv"
)
RESULT_5249 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5249"
    / "Q05_corrected_inner_slice_result.json"
)
EXTRAPOLATION_5249 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5249"
    / "Q05_corrected_regulator_extrapolation.csv"
)
RESULT_5250 = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5250"
    / "partial_outer_impact_result.json"
)
VALIDATION_5250 = (
    RESIDUALS / "P8_Y5_BRR545_5250_VALIDATION.csv"
)

MANIFEST = SOURCE / "order5_backbone_manifest.json"
DRY_RUN = SOURCE / "order5_backbone_dry_run.json"
STATUS = SOURCE / "order5_backbone_status.json"
RESULT = SOURCE / "order5_backbone_result.json"
NODE_SUMMARY = SOURCE / "order5_backbone_node_summary.csv"
CUBATURE_ROWS = SOURCE / "corrected_order5_cubature.csv"
VALIDATION = RESIDUALS / "P8_Y5_BRR545_5251_VALIDATION.csv"
DOCUMENT = (
    POST
    / "5251-Y5-R2FR-order5-backbone-paired-transport-rebuild.md"
)
COMPLETE = SOURCE / "COMPLETE.marker"
FORMAL_INVENTORY = (
    SOURCE / "formalization_workbench_start_inventory.csv"
)
FORMAL_DIFF = SOURCE / "formalization_workbench_run_diff.csv"

MARKER = "MTS_5251_ORDER5_BACKBONE_PAIRED_TRANSPORT_REBUILD"
REVISION = "order5-backbone-paired-transport-rebuild-v2"
TRANSPORT_CACHE_REVISION = "order5-backbone-paired-transport-rebuild-v1"
CHECKPOINT = 5251
PARENT_CHECKPOINT = 5250
TARGET_NODE_IDS = ("Q00", "Q02", "Q04", "Q06", "Q08")
CORRECTED_ORDER9_ONLY_IDS = ("Q03", "Q05")
REMAINING_ORDER9_IDS = ("Q01", "Q07")
BACKBONE_BASE_RESOLUTION_LADDER = (
    2048,
    4096,
    8192,
    16384,
    32768,
    65536,
    131072,
    262144,
    524288,
)
DEFAULT_MAX_WORKERS = 2
MAXIMUM_RECONSTRUCTION_RESIDUAL = 2.0e-12
MAXIMUM_NODE_RUNTIME_SECONDS = 4.0 * 60.0 * 60.0
MAXIMUM_BATCH_RUNTIME_SECONDS = 12.0 * 60.0 * 60.0
HISTORIC_FORMAL_BASELINE = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)


def load_module(path: Path, name: str) -> Any:
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise RuntimeError(f"Unable to load {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


M5246 = load_module(SCRIPT_5246, "mts_5246_for_5251")
M5247 = load_module(SCRIPT_5247, "mts_5247_for_5251")
M5245 = M5246.M5245
M5243 = M5246.M5243
M5240 = M5246.M5240
M5239 = M5247.M5239
M5246.BASE_RESOLUTION_LADDER = BACKBONE_BASE_RESOLUTION_LADDER


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def tree_digest(path: Path) -> str:
    value = hashlib.sha256()
    for child in sorted(
        item for item in path.rglob("*") if item.is_file()
    ):
        relative = child.relative_to(path).as_posix()
        value.update(relative.encode("utf-8"))
        value.update(b"\0")
        value.update(bytes.fromhex(digest(child)))
    return value.hexdigest()


def formal_inventory_rows() -> list[dict[str, Any]]:
    return [
        {
            "relative_path": child.relative_to(FORMAL).as_posix(),
            "size_bytes": child.stat().st_size,
            "sha256": digest(child),
        }
        for child in sorted(
            item for item in FORMAL.rglob("*") if item.is_file()
        )
    ]


def inventory_digest(rows: list[dict[str, Any]]) -> str:
    value = hashlib.sha256()
    for row in sorted(
        rows, key=lambda item: Path(item["relative_path"])
    ):
        value.update(row["relative_path"].encode("utf-8"))
        value.update(b"\0")
        value.update(bytes.fromhex(row["sha256"]))
    return value.hexdigest()


def inventory_diff_rows(
    before_rows: list[dict[str, Any]],
    after_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    before = {row["relative_path"]: row for row in before_rows}
    after = {row["relative_path"]: row for row in after_rows}
    rows = []
    for relative_path in sorted(set(before) | set(after)):
        old = before.get(relative_path)
        new = after.get(relative_path)
        if old is not None and new is not None:
            if (
                old["sha256"] == new["sha256"]
                and int(old["size_bytes"]) == int(new["size_bytes"])
            ):
                continue
            change_kind = "MODIFIED"
        elif old is None:
            change_kind = "ADDED"
        else:
            change_kind = "REMOVED"
        rows.append(
            {
                "relative_path": relative_path,
                "change_kind": change_kind,
                "before_size_bytes": (
                    int(old["size_bytes"]) if old is not None else ""
                ),
                "after_size_bytes": (
                    int(new["size_bytes"]) if new is not None else ""
                ),
                "before_sha256": old["sha256"] if old is not None else "",
                "after_sha256": new["sha256"] if new is not None else "",
            }
        )
    return rows


def serialized_hash(value: Any) -> str:
    payload = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        default=str,
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def atomic_text(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(
        f"{path.name}.{os.getpid()}.tmp"
    )
    temporary.write_text(value, encoding="utf-8")
    try:
        for attempt in range(8):
            try:
                temporary.replace(path)
                return
            except PermissionError:
                if attempt == 7:
                    raise
                time.sleep(0.05 * (attempt + 1))
    finally:
        if temporary.exists():
            temporary.unlink()


def atomic_json(path: Path, value: Any) -> None:
    atomic_text(
        path,
        json.dumps(value, indent=2, sort_keys=True, default=str)
        + "\n",
    )


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        atomic_text(path, "")
        return
    fieldnames: list[str] = []
    seen: set[str] = set()
    for row in rows:
        for key in row:
            if key not in seen:
                seen.add(key)
                fieldnames.append(key)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(
            handle,
            fieldnames=fieldnames,
            extrasaction="ignore",
        )
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(path)


def source_rows() -> list[dict[str, str]]:
    paths = (
        Path(__file__),
        SCRIPT_5246,
        SCRIPT_5247,
        RESULT_5245,
        VALIDATION_5245,
        MANIFEST_5241,
        RESULT_5241,
        NODE_ROWS_5241,
        WINDING_5241,
        RESULT_5247,
        EXTRAPOLATION_5247,
        RESULT_5249,
        EXTRAPOLATION_5249,
        RESULT_5250,
        VALIDATION_5250,
    )
    return [
        {"path": str(path), "sha256": digest(path)}
        for path in paths
    ]


def prepare_batch() -> tuple[dict[str, Any], dict[str, Any]]:
    parent_5245 = read_json(RESULT_5245)
    parent_5250 = read_json(RESULT_5250)
    manifest_5241 = read_json(MANIFEST_5241)
    target_nodes = [
        row
        for row in manifest_5241["outer_nodes"]
        if row["order9_node_id"] in TARGET_NODE_IDS
    ]
    rules5 = [
        row
        for row in manifest_5241["outer_rule_rows"]
        if int(row["outer_rule_order"]) == 5
    ]
    formal_rows = formal_inventory_rows()
    formal_start_digest = inventory_digest(formal_rows)
    write_csv(FORMAL_INVENTORY, formal_rows)
    manifest = {
        "marker": MARKER,
        "revision": REVISION,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "parent_decision": parent_5250["decision"],
        "transport_checkpoint": 5245,
        "transport_decision": parent_5245["decision"],
        "target_node_ids": list(TARGET_NODE_IDS),
        "target_nodes": target_nodes,
        "order5_rule_rows": rules5,
        "base_resolution_ladder": list(
            BACKBONE_BASE_RESOLUTION_LADDER
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
        "maximum_node_runtime_seconds": (
            MAXIMUM_NODE_RUNTIME_SECONDS
        ),
        "maximum_batch_runtime_seconds": (
            MAXIMUM_BATCH_RUNTIME_SECONDS
        ),
        "resolution_escalation_contract": {
            "trigger": (
                "Q00 Y00_E040_MC07 at soft cosine -0.995 retained "
                "stable winding (-1,+1) from 8192 upward but its "
                "maximum paired-projective step was 0.232171479257 "
                "at 32768, above the locked 0.05 gate."
            ),
            "derivation": (
                "The observed asymptotic step ratios were approximately "
                "0.597 and 0.599 per doubling. Four further doublings "
                "predict a step near 0.030, so the ladder is extended "
                "without relaxing any acceptance threshold."
            ),
            "maximum_base_resolution": max(
                BACKBONE_BASE_RESOLUTION_LADDER
            ),
            "acceptance_threshold_relaxed": False,
        },
        "formalization_workbench_start_digest": formal_start_digest,
        "formalization_workbench_start_file_count": len(formal_rows),
        "historic_formalization_workbench_digest": (
            HISTORIC_FORMAL_BASELINE
        ),
        "historic_formalization_digest_matches_start": (
            formal_start_digest == HISTORIC_FORMAL_BASELINE
        ),
        "source_files": source_rows(),
        "claim_boundary": {
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
            "reason": (
                "This rebuild closes only the nested order-5 backbone. "
                "Q01 and Q07 remain before a fully corrected order-9 "
                "cubature or coefficient statement."
            ),
        },
    }
    manifest["manifest_hash"] = serialized_hash(manifest)
    validation_5245 = read_csv(VALIDATION_5245)
    validation_5250 = read_csv(VALIDATION_5250)
    checks = {
        "source_paths_exist_and_match": all(
            Path(row["path"]).exists()
            and digest(Path(row["path"])) == row["sha256"]
            for row in manifest["source_files"]
        ),
        "transport_parent_passed": (
            parent_5245["integrity_passed"]
            and parent_5245["acceptance_passed"]
            and all(row["passed"] == "True" for row in validation_5245)
        ),
        "checkpoint_5250_passed_and_authorizes_backbone": (
            parent_5250["integrity_passed"]
            and parent_5250["acceptance_passed"]
            and all(row["passed"] == "True" for row in validation_5250)
            and parent_5250["decision"]
            == (
                "HOLD_HYBRID_OUTER_VALUE__"
                "REBUILD_ORDER5_BACKBONE_WITH_PAIRED_TRANSPORT"
            )
        ),
        "target_nodes_exact": (
            {row["order9_node_id"] for row in target_nodes}
            == set(TARGET_NODE_IDS)
            and len(target_nodes) == len(TARGET_NODE_IDS)
        ),
        "order5_rule_exact": (
            {row["order9_node_id"] for row in rules5}
            == set(TARGET_NODE_IDS)
            and len(rules5) == len(TARGET_NODE_IDS)
        ),
        "formal_snapshot_captured": (
            len(formal_rows) > 0
            and len(formal_start_digest) == 64
            and FORMAL_INVENTORY.exists()
        ),
        "formal_tree_stable_during_prepare": (
            tree_digest(FORMAL) == formal_start_digest
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
        "target_node_ids": list(TARGET_NODE_IDS),
        "warnings": {
            "historic_formalization_digest_matches_start": (
                formal_start_digest == HISTORIC_FORMAL_BASELINE
            ),
            "historic_digest": HISTORIC_FORMAL_BASELINE,
            "captured_start_digest": formal_start_digest,
            "handling": (
                "The current workbench is frozen as the 5251 start "
                "snapshot. Historical digest drift is recorded as a "
                "provenance warning and is not silently called unchanged."
            ),
        },
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    return manifest, dry_run


def node_paths(node_id: str) -> dict[str, Path]:
    node_root = NODES / node_id
    return {
        "root": node_root,
        "manifest": node_root / "node_manifest.json",
        "dry_run": node_root / "node_dry_run.json",
        "status": node_root / "node_status.json",
        "result": node_root / "node_result.json",
        "state_cache": node_root / "state_cache.json",
        "job_cache": node_root / "job-cache",
        "attempts": node_root / "topology_resolution_attempts.csv",
        "intervals": node_root / "topology_intervals.csv",
        "transitions": node_root / "topology_transitions.csv",
        "jobs": node_root / "topology_job_summary.csv",
        "comparisons": node_root / "legacy_comparison.csv",
        "scan": node_root / "corrected_scan.csv",
        "poles": node_root / "corrected_pole_catalog.csv",
        "topology": node_root / "corrected_pole_topology.csv",
        "residues": node_root / "corrected_residue_fits.csv",
        "closure": node_root / "corrected_dynamic_closure.csv",
        "zeros": node_root / "corrected_structural_zero_audit.csv",
        "quadrature": node_root / "corrected_inner_quadrature.csv",
        "extrapolation": node_root / "corrected_regulator_extrapolation.csv",
        "validation": node_root / "node_validation.csv",
    }


def configure_transport(
    node_id: str,
    paths: dict[str, Path],
    batch_manifest: dict[str, Any],
) -> None:
    M5246.MARKER = f"{MARKER}_{node_id}"
    M5246.REVISION = (
        f"{TRANSPORT_CACHE_REVISION}-{node_id.lower()}"
    )
    M5246.TARGET_NODE_ID = node_id
    M5246.BASE_RESOLUTION_LADDER = (
        BACKBONE_BASE_RESOLUTION_LADDER
    )
    M5246.SOURCE = paths["root"]
    M5246.JOB_CACHE = paths["job_cache"]
    M5246.STATE_CACHE = paths["state_cache"]
    M5246.MAXIMUM_RUNTIME_SECONDS = (
        MAXIMUM_NODE_RUNTIME_SECONDS
    )
    M5246.FORMAL_BASELINE = batch_manifest[
        "formalization_workbench_start_digest"
    ]


def build_node_problem(
    batch_manifest: dict[str, Any],
    node_id: str,
) -> tuple[
    dict[str, Any],
    dict[str, Any],
    dict[str, Any],
    list[dict[str, Any]],
]:
    parent_manifest, matches, base_jobs, _ = M5240.build_manifest()
    outer_manifest = read_json(MANIFEST_5241)
    node = next(
        row
        for row in outer_manifest["outer_nodes"]
        if row["order9_node_id"] == node_id
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
    node_manifest = {
        "marker": f"{MARKER}_{node_id}",
        "revision": f"{REVISION}-{node_id.lower()}",
        "batch_manifest_hash": batch_manifest["manifest_hash"],
        "parent_checkpoint": PARENT_CHECKPOINT,
        "parent_decision": batch_manifest["parent_decision"],
        "target_node": node,
        "job_count": len(problems),
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
        "source_files": [
            {"path": str(MANIFEST), "sha256": digest(MANIFEST)},
            {"path": str(SCRIPT_5246), "sha256": digest(SCRIPT_5246)},
            {"path": str(SCRIPT_5247), "sha256": digest(SCRIPT_5247)},
            {"path": str(RESULT_5245), "sha256": digest(RESULT_5245)},
            {"path": str(RESULT_5250), "sha256": digest(RESULT_5250)},
        ],
        "jobs": [
            {
                "job_id": problem["job"]["job_id"],
                "job_input_hash": problem["job"]["job_input_hash"],
                "epsilon_id": problem["job"]["epsilon_id"],
                "component_id": problem["component_id"],
                "family": problem["case"]["family"],
            }
            for problem in problems
        ],
        "claim_boundary": dict(batch_manifest["claim_boundary"]),
    }
    node_manifest["manifest_hash"] = serialized_hash(node_manifest)
    context = {
        "node": node,
        "execution_node": execution_node,
        "event": event,
        "matches": matches,
        "tracks": tracks,
    }
    return node_manifest, context, node, problems


def inner_validation_rows(
    node_manifest: dict[str, Any],
    node_id: str,
    calculation: dict[str, Any],
    topology_passed: bool,
    elapsed: float,
) -> list[dict[str, Any]]:
    fits = calculation["residue_rows"]
    zero_rows = calculation["zero_rows"]
    closure_rows = calculation["closure_rows"]
    coverage_rows = calculation["coverage_rows"]
    convergence = calculation["convergence"]
    physical = calculation["physical_values"]
    definitions = [
        (
            "integrity",
            f"{node_id}_TOPOLOGY_GATE_PASSED",
            topology_passed,
            topology_passed,
            True,
        ),
        (
            "acceptance",
            f"{node_id}_ALL_STRUCTURAL_ZERO_ROWS_PASS",
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
            f"{node_id}_DYNAMIC_CLOSURE_PASSES",
            max(
                float(row["relative_closure_residual"])
                for row in closure_rows
            )
            <= M5247.MAXIMUM_DYNAMIC_CLOSURE_RESIDUAL,
            max(
                float(row["relative_closure_residual"])
                for row in closure_rows
            ),
            M5247.MAXIMUM_DYNAMIC_CLOSURE_RESIDUAL,
        ),
        (
            "acceptance",
            f"{node_id}_ACTIVE_POLES_HAVE_ONE_ACCEPTED_FIT",
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
            f"{node_id}_INNER_COVERAGE_CLOSES",
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
            f"{node_id}_LOW_ORDER_EXTRAPOLATION_CONVERGES",
            convergence["low_order_subtracted_relative_error"]
            <= M5239.LOW_ORDER_SUBTRACTED_RELATIVE_ERROR_LIMIT,
            convergence["low_order_subtracted_relative_error"],
            M5239.LOW_ORDER_SUBTRACTED_RELATIVE_ERROR_LIMIT,
        ),
        (
            "acceptance",
            f"{node_id}_MID_ORDER_EXTRAPOLATION_CONVERGES",
            convergence["mid_order_subtracted_relative_error"]
            <= M5239.MID_ORDER_SUBTRACTED_RELATIVE_ERROR_LIMIT,
            convergence["mid_order_subtracted_relative_error"],
            M5239.MID_ORDER_SUBTRACTED_RELATIVE_ERROR_LIMIT,
        ),
        (
            "acceptance",
            f"{node_id}_CORRECTED_VALUES_FINITE",
            all(
                math.isfinite(physical[order]["subtracted"].real)
                and math.isfinite(physical[order]["subtracted"].imag)
                for order in (128, 512)
            ),
            {
                str(order): str(physical[order]["subtracted"])
                for order in (128, 512)
            },
            "finite complex values",
        ),
        (
            "integrity",
            f"{node_id}_CLAIMS_REMAIN_FALSE",
            all(
                not bool(node_manifest["claim_boundary"][field])
                for field in (
                    "valid_for_numeric_UV_claim",
                    "valid_for_local_GR_claim",
                    "valid_for_full_MTS_claim",
                )
            ),
            "false,false,false",
            "false,false,false",
        ),
        (
            "integrity",
            f"{node_id}_RUNTIME_BOUNDED",
            elapsed <= MAXIMUM_NODE_RUNTIME_SECONDS,
            elapsed,
            MAXIMUM_NODE_RUNTIME_SECONDS,
        ),
    ]
    return [
        {
            "checkpoint": CHECKPOINT,
            "node_id": node_id,
            "gate_kind": gate_kind,
            "gate": gate,
            "passed": passed,
            "observed": observed,
            "required": required,
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
        }
        for gate_kind, gate, passed, observed, required in definitions
    ]


def fixed_node_values() -> dict[str, dict[int, complex]]:
    return {
        row["order9_node_id"]: {
            order: complex(
                float(row[f"order{order}_subtracted_real"]),
                float(row[f"order{order}_subtracted_imaginary"]),
            )
            for order in (128, 512)
        }
        for row in read_csv(NODE_ROWS_5241)
    }


def run_node(node_id: str) -> dict[str, Any]:
    if node_id not in TARGET_NODE_IDS:
        raise ValueError(f"Unsupported node {node_id}")
    started = time.perf_counter()
    batch_manifest = read_json(MANIFEST)
    paths = node_paths(node_id)
    paths["root"].mkdir(parents=True, exist_ok=True)
    configure_transport(node_id, paths, batch_manifest)
    node_manifest, context, node, problems = build_node_problem(
        batch_manifest, node_id
    )
    dry_checks = {
        "batch_manifest_hash_matches": (
            node_manifest["batch_manifest_hash"]
            == batch_manifest["manifest_hash"]
        ),
        "source_paths_exist_and_match": all(
            Path(row["path"]).exists()
            and digest(Path(row["path"])) == row["sha256"]
            for row in node_manifest["source_files"]
        ),
        "target_node_exact": (
            node["order9_node_id"] == node_id
        ),
        "job_count_exact": (
            len(problems) == M5246.EXPECTED_JOB_COUNT
        ),
        "formal_digest_unchanged": (
            tree_digest(FORMAL)
            == batch_manifest["formalization_workbench_start_digest"]
        ),
        "claims_locked_false": all(
            not bool(node_manifest["claim_boundary"][field])
            for field in (
                "valid_for_numeric_UV_claim",
                "valid_for_local_GR_claim",
                "valid_for_full_MTS_claim",
            )
        ),
    }
    node_dry_run = {
        "marker": f"{MARKER}_{node_id}",
        "revision": f"{REVISION}-{node_id.lower()}",
        "dry_run_passed": all(dry_checks.values()),
        "checks": dry_checks,
        "manifest_hash": node_manifest["manifest_hash"],
        "node_id": node_id,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(paths["manifest"], node_manifest)
    atomic_json(paths["dry_run"], node_dry_run)
    if not node_dry_run["dry_run_passed"]:
        failed = [
            key
            for key, passed in dry_checks.items()
            if not passed
        ]
        raise RuntimeError(f"{node_id} dry run failed: {failed}")

    state_cache = M5246.load_state_cache(node_manifest)
    paths["job_cache"].mkdir(parents=True, exist_ok=True)
    results: list[dict[str, Any]] = []
    cache_flags: list[bool] = []
    for index, problem in enumerate(problems, start=1):
        result, cache_hit = M5246.derive_job(
            node_manifest, problem, state_cache
        )
        results.append(result)
        cache_flags.append(cache_hit)
        attempts_so_far = [
            row
            for local in results
            for row in local["attempt_rows"]
        ]
        intervals_so_far = [
            row
            for local in results
            for row in local["interval_rows"]
        ]
        transitions_so_far = [
            row
            for local in results
            for row in local["transition_rows"]
        ]
        write_csv(paths["attempts"], attempts_so_far)
        write_csv(paths["intervals"], intervals_so_far)
        write_csv(paths["transitions"], transitions_so_far)
        atomic_json(
            paths["status"],
            {
                "node_id": node_id,
                "status": "RUNNING",
                "completed_jobs": index,
                "total_jobs": len(problems),
                "cache_hits": sum(cache_flags),
                "elapsed_seconds": time.perf_counter() - started,
            },
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
    comparisons = M5243.compare_intervals(
        node_id, intervals, read_csv(WINDING_5241)
    )
    topology_elapsed = time.perf_counter() - started
    topology_validations = M5246.validation_rows(
        node_manifest,
        attempts,
        intervals,
        transitions,
        summaries,
        comparisons,
        tree_digest(FORMAL),
        topology_elapsed,
    )
    for row in topology_validations:
        row["checkpoint"] = CHECKPOINT
        row["node_id"] = node_id
        inherited_gate = row["gate"]
        if inherited_gate.startswith("Q03_"):
            inherited_gate = (
                f"{node_id}_{inherited_gate.removeprefix('Q03_')}"
            )
        row["gate"] = f"{node_id}_TOPOLOGY_{inherited_gate}"
    topology_integrity = all(
        bool(row["passed"])
        for row in topology_validations
        if row["gate_kind"] == "integrity"
    )
    topology_acceptance = all(
        bool(row["passed"])
        for row in topology_validations
        if row["gate_kind"] == "acceptance"
    )
    if not topology_integrity or not topology_acceptance:
        write_csv(paths["attempts"], attempts)
        write_csv(paths["intervals"], intervals)
        write_csv(paths["transitions"], transitions)
        write_csv(paths["jobs"], summaries)
        write_csv(paths["comparisons"], comparisons)
        write_csv(paths["validation"], topology_validations)
        atomic_json(
            paths["status"],
            {
                "node_id": node_id,
                "status": "FAILED",
                "failure_stage": "TOPOLOGY",
                "integrity_passed": topology_integrity,
                "acceptance_passed": topology_acceptance,
                "completed_jobs": len(problems),
                "total_jobs": len(problems),
                "cache_hits": sum(cache_flags),
                "elapsed_seconds": topology_elapsed,
            },
        )
        raise RuntimeError(
            f"{node_id} topology gate failed: "
            f"integrity={topology_integrity}, "
            f"acceptance={topology_acceptance}"
        )

    calculation = M5247.corrected_inner_slice(
        context, problems, intervals
    )
    elapsed = time.perf_counter() - started
    inner_validations = inner_validation_rows(
        node_manifest,
        node_id,
        calculation,
        topology_integrity and topology_acceptance,
        elapsed,
    )
    validations = topology_validations + inner_validations
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

    write_csv(paths["attempts"], attempts)
    write_csv(paths["intervals"], intervals)
    write_csv(paths["transitions"], transitions)
    write_csv(paths["jobs"], summaries)
    write_csv(paths["comparisons"], comparisons)
    write_csv(paths["scan"], calculation["scan_rows"])
    write_csv(paths["poles"], calculation["pole_rows"])
    write_csv(paths["topology"], calculation["topology_rows"])
    write_csv(paths["residues"], calculation["residue_rows"])
    write_csv(paths["closure"], calculation["closure_rows"])
    write_csv(paths["zeros"], calculation["zero_rows"])
    write_csv(paths["quadrature"], calculation["quadrature_rows"])
    write_csv(
        paths["extrapolation"],
        calculation["extrapolation_rows"],
    )
    write_csv(paths["validation"], validations)

    fixed_values = fixed_node_values()[node_id]
    physical_values = {
        order: calculation["physical_values"][order]["subtracted"]
        for order in (128, 512)
    }
    summary = {
        "order9_node_id": node_id,
        "decay_cosine": float(node["decay_cosine"]),
        "job_count": len(problems),
        "job_cache_hit_count": sum(cache_flags),
        "interval_count": len(intervals),
        "transition_count": len(transitions),
        "changed_job_count": sum(
            not bool(row["maps_identical_up_to_measure"])
            for row in comparisons
        ),
        "geometric_pole_count": calculation[
            "geometric_pole_count"
        ],
        "active_pole_count": calculation["active_pole_count"],
        "fit_count": calculation["fit_count"],
        "fixed_128_real": fixed_values[128].real,
        "fixed_128_imaginary": fixed_values[128].imag,
        "corrected_128_real": physical_values[128].real,
        "corrected_128_imaginary": physical_values[128].imag,
        "fixed_512_real": fixed_values[512].real,
        "fixed_512_imaginary": fixed_values[512].imag,
        "corrected_512_real": physical_values[512].real,
        "corrected_512_imaginary": physical_values[512].imag,
        "relative_change_512": (
            abs(physical_values[512] - fixed_values[512])
            / max(abs(fixed_values[512]), 1.0e-300)
        ),
        "low_order_error": calculation["convergence"][
            "low_order_subtracted_relative_error"
        ],
        "mid_order_error": calculation["convergence"][
            "mid_order_subtracted_relative_error"
        ],
        "integrity_passed": integrity_passed,
        "acceptance_passed": acceptance_passed,
        "elapsed_seconds": elapsed,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    result = {
        "marker": f"{MARKER}_{node_id}",
        "revision": f"{REVISION}-{node_id.lower()}",
        "manifest_hash": node_manifest["manifest_hash"],
        "node_id": node_id,
        "integrity_passed": integrity_passed,
        "acceptance_passed": acceptance_passed,
        "summary": summary,
        "physical_values": {
            str(order): {
                "subtracted_real": physical_values[order].real,
                "subtracted_imaginary": physical_values[order].imag,
            }
            for order in (128, 512)
        },
        "formalization_workbench_digest": tree_digest(FORMAL),
        "elapsed_seconds": elapsed,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(paths["result"], result)
    atomic_json(
        paths["status"],
        {
            "node_id": node_id,
            "status": "COMPLETE" if integrity_passed else "FAILED",
            "integrity_passed": integrity_passed,
            "acceptance_passed": acceptance_passed,
            "completed_jobs": len(problems),
            "total_jobs": len(problems),
            "cache_hits": sum(cache_flags),
            "elapsed_seconds": elapsed,
        },
    )
    if not integrity_passed:
        raise RuntimeError(f"{node_id} node integrity failed")
    return result


def physical_values(path: Path) -> dict[int, complex]:
    rows = [
        row
        for row in read_csv(path)
        if row["row_type"] == "PHYSICAL_RICHARDSON_SLICE"
    ]
    return {
        int(row["quadrature_order"]): complex(
            float(row["subtracted_integral_real"]),
            float(row["subtracted_integral_imaginary"]),
        )
        for row in rows
    }


def node_result_values(result: dict[str, Any]) -> dict[int, complex]:
    return {
        int(order): complex(
            float(values["subtracted_real"]),
            float(values["subtracted_imaginary"]),
        )
        for order, values in result["physical_values"].items()
    }


def cubature_value(
    rule_rows: list[dict[str, Any]],
    values: dict[str, dict[int, complex]],
    inner_order: int,
) -> complex:
    return 0.25 * sum(
        (
            float(row["weight_d_decay_cosine"])
            * values[row["order9_node_id"]][inner_order]
            for row in rule_rows
        ),
        0.0j,
    )


def batch_validation_rows(
    manifest: dict[str, Any],
    node_results: list[dict[str, Any]],
    summary: dict[str, Any],
    elapsed: float,
) -> list[dict[str, Any]]:
    convergence_limit = float(
        read_json(MANIFEST_5241)["acceptance_thresholds"][
            "maximum_outer_relative_difference"
        ]
    )
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
            "ALL_FIVE_NODE_RESULTS_PRESENT",
            {row["node_id"] for row in node_results}
            == set(TARGET_NODE_IDS),
            sorted(row["node_id"] for row in node_results),
            list(TARGET_NODE_IDS),
        ),
        (
            "acceptance",
            "ALL_NODE_INTEGRITY_GATES_PASS",
            all(row["integrity_passed"] for row in node_results),
            sum(row["integrity_passed"] for row in node_results),
            len(TARGET_NODE_IDS),
        ),
        (
            "acceptance",
            "ALL_NODE_ACCEPTANCE_GATES_PASS",
            all(row["acceptance_passed"] for row in node_results),
            sum(row["acceptance_passed"] for row in node_results),
            len(TARGET_NODE_IDS),
        ),
        (
            "acceptance",
            "FIXED_RULES_RECONSTRUCT_REPORTED_VALUES",
            summary["maximum_fixed_reconstruction_residual"]
            <= MAXIMUM_RECONSTRUCTION_RESIDUAL,
            summary["maximum_fixed_reconstruction_residual"],
            MAXIMUM_RECONSTRUCTION_RESIDUAL,
        ),
        (
            "acceptance",
            "CORRECTED_ORDER3_ORDER5_VALUES_FINITE",
            all(
                math.isfinite(summary[key])
                for key in (
                    "corrected_order3_512_real",
                    "corrected_order3_512_imaginary",
                    "corrected_order5_512_real",
                    "corrected_order5_512_imaginary",
                )
            ),
            "finite",
            "finite",
        ),
        (
            "acceptance",
            "CORRECTED_ORDER5_INNER_RESOLUTION_FINITE",
            math.isfinite(
                summary[
                    "corrected_order5_inner128_to512_relative_difference"
                ]
            ),
            summary[
                "corrected_order5_inner128_to512_relative_difference"
            ],
            "finite",
        ),
        (
            "diagnostic",
            "CORRECTED_ORDER3_TO_ORDER5_CONVERGENCE",
            summary[
                "corrected_order3_to_order5_relative_difference"
            ]
            <= convergence_limit,
            summary[
                "corrected_order3_to_order5_relative_difference"
            ],
            convergence_limit,
        ),
        (
            "diagnostic",
            "PARTIAL_ORDER5_TO_ORDER9_DIAGNOSTIC",
            summary[
                "corrected_order5_to_partial_order9_relative_difference"
            ]
            <= convergence_limit,
            summary[
                "corrected_order5_to_partial_order9_relative_difference"
            ],
            (
                f"{convergence_limit}; non-promotion diagnostic until "
                "Q01/Q07 are corrected"
            ),
        ),
        (
            "integrity",
            "FORMALIZATION_WORKBENCH_UNCHANGED_DURING_5251",
            summary["formalization_workbench_modified_file_count"] == 0,
            summary["formalization_workbench_modified_file_count"],
            0,
        ),
        (
            "provenance",
            "HISTORIC_FORMAL_BASELINE_MATCHES_5251_START",
            manifest["historic_formalization_digest_matches_start"],
            manifest["formalization_workbench_start_digest"],
            manifest["historic_formalization_workbench_digest"],
        ),
        (
            "integrity",
            "RUNTIME_BOUNDED",
            elapsed <= MAXIMUM_BATCH_RUNTIME_SECONDS,
            elapsed,
            MAXIMUM_BATCH_RUNTIME_SECONDS,
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
            "checkpoint": 5251,
            "gate_kind": gate_kind,
            "gate": gate,
            "passed": passed,
            "observed": observed,
            "required": required,
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
        }
        for gate_kind, gate, passed, observed, required in definitions
    ]


def render_document(
    node_results: list[dict[str, Any]],
    summary: dict[str, Any],
    decision: str,
) -> str:
    node_lines = []
    for result in sorted(node_results, key=lambda row: row["node_id"]):
        row = result["summary"]
        node_lines.append(
            "- "
            f"{row['order9_node_id']}: changed maps "
            f"`{row['changed_job_count']}/{row['job_count']}`, corrected "
            f"`({row['corrected_512_real']}{row['corrected_512_imaginary']:+}j)`, "
            f"relative change `{row['relative_change_512']:.12g}`, "
            f"acceptance `{row['acceptance_passed']}`."
        )
    return "\n".join(
        [
            "# 5251 - Order-5 backbone paired-transport rebuild",
            "",
            "## Calculation",
            "",
            "The reciprocal-projective collision and chamber-boundary "
            "transport accepted at checkpoints 5245-5249 is applied to "
            "every nested order-5 node: Q00/Q02/Q04/Q06/Q08. Each node "
            "has an independent resumable state/job cache. Its corrected "
            "inner slice is then recomputed under the same residue, "
            "coverage, and regulator-extrapolation gates as Q03/Q05.",
            "",
            "## Endpoint-resolution derivation",
            "",
            "Q00 exposed a resolution failure rather than a failed "
            "physical gate. For Y00_E040_MC07 at soft cosine -0.995, "
            "the winding pair remained (-1,+1) while the maximum paired "
            "projective step fell through 0.387743, 0.232171, 0.121320, "
            "0.061304, and 0.030760. The locked 0.05 gate therefore "
            "closed at base resolution 262144. Q08 independently "
            "required the same maximum resolution at the reflected "
            "endpoint. No acceptance threshold was relaxed.",
            "",
            "## Per-node results",
            "",
            *node_lines,
            "",
            "## Corrected cubature",
            "",
            f"- Corrected order-3 value: "
            f"`({summary['corrected_order3_512_real']}"
            f"{summary['corrected_order3_512_imaginary']:+}j)`.",
            f"- Corrected order-5 value: "
            f"`({summary['corrected_order5_512_real']}"
            f"{summary['corrected_order5_512_imaginary']:+}j)`.",
            f"- Corrected order-3/order-5 relative difference: "
            f"`{summary['corrected_order3_to_order5_relative_difference']:.12g}`.",
            f"- Corrected order-5 inner 128/512 relative difference: "
            f"`{summary['corrected_order5_inner128_to512_relative_difference']:.12g}`.",
            f"- Backbone+Q03/Q05 partial order-9 diagnostic: "
            f"`({summary['partial_order9_512_real']}"
            f"{summary['partial_order9_512_imaginary']:+}j)`.",
            f"- Corrected order-5/partial-order-9 relative difference: "
            f"`{summary['corrected_order5_to_partial_order9_relative_difference']:.12g}`.",
            f"- Formal-workbench files changed during 5251: "
            f"`{summary['formalization_workbench_modified_file_count']}`.",
            f"- Historical protected digest matched at start: "
            f"`{summary['historic_formalization_digest_matches_start']}` "
            "(a false value is retained as a provenance warning, not "
            "silently relabelled).",
            "",
            "## Decision",
            "",
            f"`{decision}`",
            "",
            "## Interpretation",
            "",
            "The order-5 baseline is now like-for-like only if all five "
            "node gates pass. The partial order-9 value remains a "
            "diagnostic because Q01 and Q07 still retain inherited "
            "topology; it is not a coefficient.",
            "",
            "## Claim boundary",
            "",
            "No numeric UV coefficient, local-GR extension, or full-MTS "
            "claim follows from this checkpoint. The selected local "
            "two-derivative GR+SM+Maxwell theorem is unchanged.",
            "",
            "## Next exact target",
            "",
            "Apply the same paired reciprocal-projective transport to "
            "Q01 and Q07, then recompute the fully corrected order-9 "
            "cubature and only then test the locked outer-convergence "
            "and Chebyshev-tail gates.",
            "",
        ]
    )


def launch_workers(max_workers: int) -> dict[str, int]:
    pending = list(TARGET_NODE_IDS)
    running: dict[str, tuple[subprocess.Popen[Any], Any]] = {}
    return_codes: dict[str, int] = {}
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    while pending or running:
        while pending and len(running) < max_workers:
            node_id = pending.pop(0)
            log_path = node_paths(node_id)["root"] / "worker.log"
            log_path.parent.mkdir(parents=True, exist_ok=True)
            log_handle = log_path.open("a", encoding="utf-8")
            process = subprocess.Popen(
                [
                    sys.executable,
                    str(Path(__file__)),
                    "--worker-node",
                    node_id,
                ],
                cwd=ROOT,
                stdout=log_handle,
                stderr=subprocess.STDOUT,
                env=environment,
                text=True,
            )
            running[node_id] = (process, log_handle)
        completed: list[str] = []
        for node_id, (process, log_handle) in running.items():
            return_code = process.poll()
            if return_code is None:
                continue
            log_handle.close()
            return_codes[node_id] = return_code
            completed.append(node_id)
        for node_id in completed:
            del running[node_id]
        status_rows = {}
        for node_id in TARGET_NODE_IDS:
            path = node_paths(node_id)["status"]
            status_rows[node_id] = (
                read_json(path)
                if path.exists()
                else {
                    "node_id": node_id,
                    "status": (
                        "PENDING"
                        if node_id in pending
                        else (
                            "STARTING"
                            if node_id in running
                            else "UNKNOWN"
                        )
                    ),
                }
            )
        atomic_json(
            STATUS,
            {
                "marker": MARKER,
                "status": "RUNNING" if pending or running else "WORKERS_DONE",
                "pending": pending,
                "running": sorted(running),
                "return_codes": return_codes,
                "nodes": status_rows,
            },
        )
        if pending or running:
            time.sleep(5.0)
    return return_codes


def execute(max_workers: int) -> dict[str, Any]:
    started = time.perf_counter()
    SOURCE.mkdir(parents=True, exist_ok=True)
    manifest, dry_run = prepare_batch()
    atomic_json(MANIFEST, manifest)
    atomic_json(DRY_RUN, dry_run)
    if not dry_run["dry_run_passed"]:
        failed = [
            key
            for key, passed in dry_run["checks"].items()
            if not passed
        ]
        raise RuntimeError(f"5251 dry run failed: {failed}")

    return_codes = launch_workers(max_workers)
    node_results = [
        read_json(node_paths(node_id)["result"])
        for node_id in TARGET_NODE_IDS
        if node_paths(node_id)["result"].exists()
    ]
    worker_failures = [
        node_id
        for node_id in TARGET_NODE_IDS
        if return_codes.get(node_id) != 0
        or not node_paths(node_id)["result"].exists()
    ]

    fixed_values = fixed_node_values()
    corrected_values = {
        result["node_id"]: node_result_values(result)
        for result in node_results
    }
    corrected_values["Q03"] = physical_values(EXTRAPOLATION_5247)
    corrected_values["Q05"] = physical_values(EXTRAPOLATION_5249)
    values_backbone = {
        node_id: (
            corrected_values[node_id]
            if node_id in corrected_values
            else fixed_values[node_id]
        )
        for node_id in fixed_values
    }
    manifest_5241 = read_json(MANIFEST_5241)
    rules_by_order = {
        order: [
            row
            for row in manifest_5241["outer_rule_rows"]
            if int(row["outer_rule_order"]) == order
        ]
        for order in (3, 5, 9)
    }
    fixed_cubature = {
        order: {
            inner_order: cubature_value(
                rules_by_order[order],
                fixed_values,
                inner_order,
            )
            for inner_order in (128, 512)
        }
        for order in (3, 5, 9)
    }
    corrected_order3 = {
        inner_order: cubature_value(
            rules_by_order[3], values_backbone, inner_order
        )
        for inner_order in (128, 512)
    }
    corrected_order5 = {
        inner_order: cubature_value(
            rules_by_order[5], values_backbone, inner_order
        )
        for inner_order in (128, 512)
    }
    partial_order9 = {
        inner_order: cubature_value(
            rules_by_order[9], values_backbone, inner_order
        )
        for inner_order in (128, 512)
    }
    reported_5241 = read_json(RESULT_5241)["cubature_values"]
    reconstruction_residuals = {
        order: abs(
            fixed_cubature[order][512]
            - complex(
                float(reported_5241[str(order)]["real"]),
                float(reported_5241[str(order)]["imaginary"]),
            )
        )
        for order in (3, 5, 9)
    }
    summary = {
        "worker_failures": "|".join(worker_failures),
        "corrected_node_count": len(corrected_values),
        "remaining_order9_ids": "|".join(REMAINING_ORDER9_IDS),
        "corrected_order3_128_real": corrected_order3[128].real,
        "corrected_order3_128_imaginary": corrected_order3[128].imag,
        "corrected_order3_512_real": corrected_order3[512].real,
        "corrected_order3_512_imaginary": corrected_order3[512].imag,
        "corrected_order5_128_real": corrected_order5[128].real,
        "corrected_order5_128_imaginary": corrected_order5[128].imag,
        "corrected_order5_512_real": corrected_order5[512].real,
        "corrected_order5_512_imaginary": corrected_order5[512].imag,
        "partial_order9_128_real": partial_order9[128].real,
        "partial_order9_128_imaginary": partial_order9[128].imag,
        "partial_order9_512_real": partial_order9[512].real,
        "partial_order9_512_imaginary": partial_order9[512].imag,
        "corrected_order3_to_order5_relative_difference": (
            abs(corrected_order3[512] - corrected_order5[512])
            / max(abs(corrected_order5[512]), 1.0)
        ),
        "corrected_order5_inner128_to512_relative_difference": (
            abs(corrected_order5[128] - corrected_order5[512])
            / max(abs(corrected_order5[512]), 1.0)
        ),
        "corrected_order5_to_partial_order9_relative_difference": (
            abs(corrected_order5[512] - partial_order9[512])
            / max(abs(partial_order9[512]), 1.0)
        ),
        "maximum_fixed_reconstruction_residual": max(
            reconstruction_residuals.values()
        ),
        "historic_formalization_digest_matches_start": manifest[
            "historic_formalization_digest_matches_start"
        ],
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    formal_after_rows = formal_inventory_rows()
    formal_diff_rows = inventory_diff_rows(
        read_csv(FORMAL_INVENTORY), formal_after_rows
    )
    write_csv(FORMAL_DIFF, formal_diff_rows)
    summary["formalization_workbench_start_digest"] = manifest[
        "formalization_workbench_start_digest"
    ]
    summary["formalization_workbench_end_digest"] = inventory_digest(
        formal_after_rows
    )
    summary["formalization_workbench_modified_file_count"] = len(
        formal_diff_rows
    )
    elapsed = time.perf_counter() - started
    validations = batch_validation_rows(
        manifest, node_results, summary, elapsed
    )
    integrity_passed = (
        not worker_failures
        and all(
            bool(row["passed"])
            for row in validations
            if row["gate_kind"] == "integrity"
        )
    )
    acceptance_passed = all(
        bool(row["passed"])
        for row in validations
        if row["gate_kind"] == "acceptance"
    )
    decision = (
        "INVALID_ORDER5_BACKBONE_PAIRED_TRANSPORT_REBUILD"
        if not integrity_passed
        else (
            "ADOPT_CORRECTED_ORDER5_BACKBONE__"
            "REBUILD_Q01_Q07_FOR_FULL_ORDER9"
            if acceptance_passed
            else (
                "HOLD_ORDER5_BACKBONE__"
                "LOCALIZE_FAILED_NODE_OR_CUBATURE_GATE"
            )
        )
    )

    node_summary_rows = [
        result["summary"]
        for result in sorted(
            node_results, key=lambda row: row["node_id"]
        )
    ]
    cubature_rows = []
    for rule_order, values in (
        (3, corrected_order3),
        (5, corrected_order5),
        (9, partial_order9),
    ):
        for inner_order in (128, 512):
            cubature_rows.append(
                {
                    "outer_rule_order": rule_order,
                    "inner_quadrature_order": inner_order,
                    "value_real": values[inner_order].real,
                    "value_imaginary": values[inner_order].imag,
                    "fully_corrected": rule_order in (3, 5),
                    "remaining_node_ids": (
                        ""
                        if rule_order in (3, 5)
                        else "|".join(REMAINING_ORDER9_IDS)
                    ),
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
            )
    write_csv(NODE_SUMMARY, node_summary_rows)
    write_csv(CUBATURE_ROWS, cubature_rows)
    write_csv(VALIDATION, validations)
    atomic_text(
        DOCUMENT,
        render_document(node_results, summary, decision),
    )
    result = {
        "marker": MARKER,
        "revision": REVISION,
        "manifest_hash": manifest["manifest_hash"],
        "decision": decision,
        "integrity_passed": integrity_passed,
        "acceptance_passed": acceptance_passed,
        "diagnostic_gates_passed": all(
            bool(row["passed"])
            for row in validations
            if row["gate_kind"] == "diagnostic"
        ),
        "summary": summary,
        "worker_return_codes": return_codes,
        "formalization_workbench_digest": summary[
            "formalization_workbench_end_digest"
        ],
        "historic_formalization_digest_matches_start": manifest[
            "historic_formalization_digest_matches_start"
        ],
        "elapsed_seconds": elapsed,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(RESULT, result)
    atomic_json(
        STATUS,
        {
            "marker": MARKER,
            "status": "COMPLETE" if integrity_passed else "FAILED",
            "decision": decision,
            "worker_return_codes": return_codes,
            "elapsed_seconds": elapsed,
        },
    )
    atomic_text(
        COMPLETE,
        json.dumps(
            {
                "marker": MARKER,
                "decision": decision,
                "result_sha256": digest(RESULT),
            },
            sort_keys=True,
        )
        + "\n",
    )
    pycache = POST / "scripts" / "__pycache__"
    if pycache.exists():
        shutil.rmtree(pycache)
    if not integrity_passed:
        raise RuntimeError(
            f"5251 integrity failed; worker failures={worker_failures}"
        )
    return result


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument(
        "--worker-node",
        choices=TARGET_NODE_IDS,
    )
    parser.add_argument(
        "--max-workers",
        type=int,
        default=DEFAULT_MAX_WORKERS,
    )
    arguments = parser.parse_args()
    if arguments.worker_node:
        result = run_node(arguments.worker_node)
        print(json.dumps(result, indent=2, sort_keys=True))
        return
    manifest, dry_run = prepare_batch()
    SOURCE.mkdir(parents=True, exist_ok=True)
    atomic_json(MANIFEST, manifest)
    atomic_json(DRY_RUN, dry_run)
    if arguments.dry_run:
        print(json.dumps(dry_run, indent=2, sort_keys=True))
        if not dry_run["dry_run_passed"]:
            raise SystemExit(1)
        return
    if arguments.max_workers < 1:
        raise ValueError("--max-workers must be positive")
    result = execute(
        min(arguments.max_workers, len(TARGET_NODE_IDS))
    )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
