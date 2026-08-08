from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import math
import os
import shutil
import sys
import time
from pathlib import Path
from typing import Any


os.environ.setdefault("PYTHONDONTWRITEBYTECODE", "1")
os.environ.setdefault("OMP_NUM_THREADS", "1")
os.environ.setdefault("OPENBLAS_NUM_THREADS", "1")
os.environ.setdefault("MKL_NUM_THREADS", "1")
os.environ.setdefault("NUMEXPR_NUM_THREADS", "1")
os.environ.setdefault("VECLIB_MAXIMUM_THREADS", "1")
sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SCRIPTS = POST / "scripts"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
RESIDUALS = POST / "source-intake" / "mts_residuals"
SOURCE = FUNCTIONAL_RG / "5334"
BASE = SOURCE / "E0025"

SCRIPT_5327 = SCRIPTS / "Y5_R2FR_5327_D2_midpoint_regulator_ladder_controller.py"
SCRIPT_5324 = SCRIPTS / "Y5_R2FR_5324_decay_angle_measure_symmetry_topology_preflight.py"
RESULT_5324 = FUNCTIONAL_RG / "5324" / "decay_angle_measure_symmetry_topology_preflight_result.json"
VALIDATION_5324 = FUNCTIONAL_RG / "5324" / "decay_angle_measure_symmetry_topology_preflight_validation.csv"
TOPOLOGY_EVENTS_5324 = FUNCTIONAL_RG / "5324" / "decay_angle_topology_events.csv"
TOPOLOGY_PANELS_5324 = FUNCTIONAL_RG / "5324" / "decay_angle_topology_soft_panels.csv"
TOPOLOGY_SUMMARY_5324 = FUNCTIONAL_RG / "5324" / "decay_angle_topology_node_summary.csv"
MEASURE_5324 = FUNCTIONAL_RG / "5324" / "decay_angle_paired_quadrature_measure_contract.csv"

CHECKPOINT = 5334
PARENT_CHECKPOINT = 5324
DECAY_NODE_ID = "D4_OUTER"
ABSOLUTE_DECAY_COSINE = 0.8568306300360823
EXPECTED_CELL_COUNT = 55
EXPECTED_PANEL_COUNT = 13
EXPECTED_COARSE_NODE_COUNT = 78
FORMAL_DIGEST = "0ec1bc6012136ffc6b28a1512aca6ce712b6decd2ff793310a9bd61775f3db1f"
EVENT_PANEL_CONTAINMENT_TOLERANCE = 2.0e-12

LADDER = SOURCE / "D4_outer_finite_regulator_ladder.csv"
PAIRWISE = SOURCE / "D4_outer_finite_regulator_pairwise_convergence.csv"
TRENDS = SOURCE / "D4_outer_finite_regulator_three_point_trends.csv"
RESULT = SOURCE / "D4_outer_regulator_ladder_controller_result.json"
VALIDATION = SOURCE / "D4_outer_regulator_ladder_controller_validation.csv"
RESIDUAL_VALIDATION = RESIDUALS / "P8_Y5_BRR545_5334_VALIDATION.csv"
STATUS = SOURCE / "status.json"
DOCUMENT = POST / "5334-Y5-R2FR-D4-outer-regulator-ladder-controller.md"

CLAIM_FIELDS = (
    "valid_for_decay_angle_integral",
    "valid_for_full_angular_convergence",
    "valid_for_full_phase_space_coefficient",
    "valid_for_numeric_UV_claim",
    "valid_for_local_GR_claim",
    "valid_for_full_MTS_claim",
)

NUMBER_WORDS = {
    0: "ZERO",
    1: "ONE",
    2: "TWO",
    3: "THREE",
    4: "FOUR",
    5: "FIVE",
    6: "SIX",
    7: "SEVEN",
    8: "EIGHT",
    9: "NINE",
    10: "TEN",
}


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5327 = load_module("mts_5327_for_5334", SCRIPT_5327)
M5326 = M5327.M5326
M5325 = M5326.M5325
M5312 = M5326.M5312
M5283 = M5326.M5283
ORIGINAL_CONFIGURE_TARGET = M5327.configure_target
ORIGINAL_EVENT_CANDIDATE_ROWS = M5326.event_candidate_rows


def read_csv(path: Path) -> list[dict[str, str]]:
    return M5327.read_csv(path)


def write_csv(
    path: Path,
    rows: list[dict[str, Any]],
    leading_fields: list[str] | None = None,
) -> None:
    M5327.write_csv(path, rows, leading_fields)


def read_json(path: Path) -> dict[str, Any]:
    return M5327.read_json(path)


def atomic_json(path: Path, value: Any) -> None:
    M5327.atomic_json(path, value)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def parse_bool(value: Any) -> bool:
    return M5327.parse_bool(value)


def validation_gate(gate: str, passed: bool, detail: str) -> dict[str, Any]:
    return M5327.validation_gate(gate, passed, detail)


def smoke_paths() -> dict[str, Path]:
    return {
        "source": BASE,
        "shards": BASE / "smoke-shards",
        "dry_run": BASE / "D4_outer_E0025_pole_topology_smoke_dry_run.json",
        "contract": BASE / "D4_outer_reduced_MC04_cubature_contract.csv",
        "identity": BASE / "D4_outer_MC04_MC12_identity_audit.csv",
        "plan": BASE / "D4_outer_E0025_outer_node_plan.csv",
        "manifest": BASE / "D4_outer_E0025_outer_node_manifest.csv",
        "poles": BASE / "D4_outer_E0025_geometric_poles.csv",
        "fits": BASE / "D4_outer_E0025_pole_residue_fits.csv",
        "classifications": BASE / "D4_outer_E0025_pole_classification.csv",
        "cell_integrals": BASE / "D4_outer_E0025_cell_integrals.csv",
        "outer_totals": BASE / "D4_outer_E0025_outer_totals.csv",
        "panel_convergence": BASE / "D4_outer_E0025_panel_convergence.csv",
        "material_topology": BASE / "D4_outer_E0025_material_pole_topology.csv",
        "result": BASE / "D4_outer_E0025_pole_topology_smoke_result.json",
        "validation": BASE / "D4_outer_E0025_pole_topology_smoke_validation.csv",
        "residual_validation": RESIDUALS / "P8_Y5_BRR545_5334_SMOKE_VALIDATION.csv",
        "status": BASE / "smoke_status.json",
        "document": BASE / "D4_outer_E0025_pole_topology_smoke.md",
    }


def refinement_paths(epsilon_id: str) -> dict[str, Path]:
    source = BASE if epsilon_id == "E0025" else SOURCE / epsilon_id
    stem = f"D4_outer_event_aligned_{epsilon_id}"
    return {
        "source": source,
        "shards": source / "refinement-shards",
        "event_candidates": source / "D4_outer_support_event_candidates.csv",
        "event_cache": source / "D4_outer_support_event_state_cache.json",
        "event_states": source / "D4_outer_support_event_state_scan.csv",
        "events": source / "D4_outer_refined_support_events.csv",
        "initial_plan": source / "D4_outer_event_aligned_initial_plan.csv",
        "dry_run": source / f"{stem}_dry_run.json",
        "node_manifest": source / f"{stem}_node_manifest.csv",
        "adaptive_panels": source / f"{stem}_adaptive_panels.csv",
        "poles": source / f"{stem}_geometric_poles.csv",
        "fits": source / f"{stem}_pole_residue_fits.csv",
        "classifications": source / f"{stem}_pole_classification.csv",
        "cell_integrals": source / f"{stem}_cell_integrals.csv",
        "energy_repairs": source / "D4_outer_targeted_energy_partition_repairs.csv",
        "near_repairs": source / "D4_outer_active_support_pole_subtraction_repairs.csv",
        "near_fits": source / "D4_outer_active_support_pole_fits.csv",
        "near_identities": source / "D4_outer_active_support_masked_identity.csv",
        "selector_repairs": source / "D4_outer_algebraic_selector_repairs.csv",
        "inventory_audit": source / "synthetic_regulator_inventory_extension_audit.csv",
        "finite": source / f"{stem}_finite_value.csv",
        "result": source / f"{stem}_result.json",
        "validation": source / f"{stem}_validation.csv",
        "semantic_validation": source / f"{stem}_semantic_validation.csv",
        "residual_validation": RESIDUALS / f"P8_Y5_BRR545_5334_{epsilon_id}_VALIDATION.csv",
        "semantic_residual_validation": (
            RESIDUALS / f"P8_Y5_BRR545_5334_{epsilon_id}_SEMANTIC_VALIDATION.csv"
        ),
        "adaptive_event_audit": source / "D4_outer_adaptive_support_event_audit.csv",
        "adaptive_event_extension": source / "D4_outer_adaptive_support_event_extension.csv",
        "adaptive_event_root_evidence": (
            source / "D4_outer_adaptive_support_event_root_evidence.csv"
        ),
        "adaptive_event_validation": source / "D4_outer_adaptive_support_event_validation.csv",
        "adaptive_event_residual_validation": (
            RESIDUALS / f"P8_Y5_BRR545_5334_{epsilon_id}_ADAPTIVE_EVENT_VALIDATION.csv"
        ),
        "adaptive_event_result": source / "D4_outer_adaptive_support_event_result.json",
        "pre_adaptive_event_closure": source / "pre-adaptive-event-closure",
        "shard_migration": source / "D4_outer_adaptive_event_shard_migration.csv",
        "shard_migration_validation": (
            source / "D4_outer_adaptive_event_shard_migration_validation.csv"
        ),
        "status": source / "status.json",
        "document": source / f"{stem}.md",
    }


def adaptive_event_extension_is_valid(paths: dict[str, Path]) -> bool:
    if not paths["adaptive_event_extension"].exists() or not paths[
        "adaptive_event_validation"
    ].exists() or not paths["adaptive_event_root_evidence"].exists():
        return False
    validation = read_csv(paths["adaptive_event_validation"])
    extensions = read_csv(paths["adaptive_event_extension"])
    evidence_sha256 = digest(paths["adaptive_event_root_evidence"])
    return (
        bool(validation)
        and bool(extensions)
        and all(parse_bool(row["passed"]) for row in validation)
        and all(row.get("root_evidence_sha256") == evidence_sha256 for row in extensions)
    )


def d4_event_candidate_rows() -> list[dict[str, Any]]:
    base_rows = [dict(row) for row in ORIGINAL_EVENT_CANDIDATE_ROWS()]
    paths = refinement_paths(M5326.EPSILON_ID)
    if not adaptive_event_extension_is_valid(paths):
        return base_rows
    extension_rows = read_csv(paths["adaptive_event_extension"])
    merged = base_rows + [dict(row) for row in extension_rows]
    merged.sort(
        key=lambda row: (
            int(row["x_panel_index"]),
            float(row["left_coordinate"]),
            row["term_id"],
            row["primary_surface_id"],
        )
    )
    for index, row in enumerate(merged, start=1):
        row["candidate_id"] = f"C{index:02d}"
        row.setdefault("candidate_source", "COARSE_SMOKE_INVENTORY")
    write_csv(
        M5326.EVENT_CANDIDATES,
        merged,
        ["candidate_id", "x_panel_index", "term_id", "primary_surface_id"],
    )
    return merged


def adaptive_support_transition_rows() -> list[dict[str, Any]]:
    manifest = read_csv(M5326.NODE_MANIFEST)
    poles = read_csv(M5326.OFF_AXIS_POLES)
    classifications = read_csv(M5326.OFF_AXIS_CLASSIFICATIONS)
    existing_events = read_csv(M5326.EVENTS)
    pole_by_identity = {
        (row["node_id"], row["term_id"], row["pole_id"]): row for row in poles
    }
    material_keys = {
        (
            int(pole_by_identity[(row["node_id"], row["term_id"], row["pole_id"])][
                "x_panel_index"
            ]),
            row["term_id"],
            pole_by_identity[(row["node_id"], row["term_id"], row["pole_id"])][
                "primary_surface_id"
            ],
        )
        for row in classifications
        if parse_bool(row["material_simple_pole"])
        and (row["node_id"], row["term_id"], row["pole_id"]) in pole_by_identity
    }
    poles_by_branch: dict[tuple[str, str, str], list[dict[str, str]]] = {}
    for pole in poles:
        poles_by_branch.setdefault(
            (pole["node_id"], pole["term_id"], pole["primary_surface_id"]), []
        ).append(pole)
    rows: list[dict[str, Any]] = []
    for panel_index, term_id, surface_id in sorted(material_keys):
        states_by_coordinate: dict[float, dict[str, Any]] = {}
        for node in manifest:
            if int(node["x_panel_index"]) != panel_index:
                continue
            coordinate = float(node["absolute_soft_cosine"])
            branch_poles = poles_by_branch.get(
                (node["node_id"], term_id, surface_id), []
            )
            inside = any(
                parse_bool(pole["inside_reduced_term_support"])
                for pole in branch_poles
            )
            state = states_by_coordinate.setdefault(
                coordinate,
                {
                    "coordinate": coordinate,
                    "inside": inside,
                    "branch_exists": bool(branch_poles),
                    "node_ids": [],
                },
            )
            state["inside"] = bool(state["inside"] or inside)
            state["branch_exists"] = bool(
                state["branch_exists"] or bool(branch_poles)
            )
            state["node_ids"].append(node["node_id"])
        ordered = [states_by_coordinate[key] for key in sorted(states_by_coordinate)]
        for left, right in zip(ordered[:-1], ordered[1:]):
            if bool(left["inside"]) == bool(right["inside"]):
                continue
            covered = any(
                int(event["x_panel_index"]) == panel_index
                and event["term_id"] == term_id
                and event["primary_surface_id"] == surface_id
                and float(left["coordinate"])
                <= float(event["event_coordinate"])
                <= float(right["coordinate"])
                for event in existing_events
            )
            rows.append(
                {
                    "transition_id": f"T{len(rows) + 1:02d}",
                    "x_panel_index": panel_index,
                    "term_id": term_id,
                    "primary_surface_id": surface_id,
                    "left_coordinate": left["coordinate"],
                    "right_coordinate": right["coordinate"],
                    "left_inside_support": left["inside"],
                    "right_inside_support": right["inside"],
                    "left_branch_exists": left["branch_exists"],
                    "right_branch_exists": right["branch_exists"],
                    "source_left_node_id": "|".join(left["node_ids"]),
                    "source_right_node_id": "|".join(right["node_ids"]),
                    "event_type": (
                        "SUPPORT_ENTRY" if not left["inside"] else "SUPPORT_EXIT"
                    ),
                    "already_covered_by_coarse_event": covered,
                    **{field: False for field in CLAIM_FIELDS},
                }
            )
    return rows


def adaptive_event_audit() -> dict[str, Any]:
    started = time.perf_counter()
    paths = refinement_paths(M5326.EPSILON_ID)
    result = read_json(M5326.RESULT)
    if not bool(result.get("completed_full_run", False)):
        raise RuntimeError("adaptive event audit requires a completed refinement tree")
    transitions = adaptive_support_transition_rows()
    write_csv(
        paths["adaptive_event_audit"],
        transitions,
        ["transition_id", "x_panel_index", "term_id", "primary_surface_id"],
    )
    uncovered = [
        dict(row)
        for row in transitions
        if not parse_bool(row["already_covered_by_coarse_event"])
    ]
    contract = read_csv(M5326.CONTRACT_5325)
    cache = M5326.load_event_cache()
    old_kernel = M5326.configure_kernel()
    try:
        extensions: list[dict[str, Any]] = []
        for index, row in enumerate(uncovered, start=1):
            candidate = {
                **row,
                "candidate_id": f"A{index:02d}",
                "candidate_source": "COMPLETED_ADAPTIVE_TREE",
            }
            refined = M5326.refine_event(candidate, contract, cache)
            extensions.append(
                {
                    **candidate,
                    "refined_event_coordinate": refined["event_coordinate"],
                    "refined_event_signed_support_margin": refined[
                        "event_signed_support_margin"
                    ],
                    "refined_event_coordinate_error_estimate": refined[
                        "event_coordinate_error_estimate"
                    ],
                    "refined_event_contract_passes": refined[
                        "event_contract_passes"
                    ],
                    "adaptive_manifest_sha256": digest(M5326.NODE_MANIFEST),
                    "adaptive_pole_sha256": digest(M5326.OFF_AXIS_POLES),
                    "adaptive_classification_sha256": digest(
                        M5326.OFF_AXIS_CLASSIFICATIONS
                    ),
                }
            )
    finally:
        M5326.restore_kernel(old_kernel)
    write_csv(
        paths["adaptive_event_extension"],
        extensions,
        ["candidate_id", "x_panel_index", "term_id", "primary_surface_id"],
    )
    source_hashes_current = all(
        row["adaptive_manifest_sha256"] == digest(M5326.NODE_MANIFEST)
        and row["adaptive_pole_sha256"] == digest(M5326.OFF_AXIS_POLES)
        and row["adaptive_classification_sha256"]
        == digest(M5326.OFF_AXIS_CLASSIFICATIONS)
        for row in extensions
    )
    gates = [
        validation_gate(
            "completed_adaptive_tree_is_source",
            bool(result["completed_full_run"])
            and int(result["failed_inner_node_count"]) == 0,
            f"nodes={result['completed_node_count']}",
        ),
        validation_gate(
            "adaptive_material_support_transitions_are_detected",
            bool(transitions),
            f"transitions={len(transitions)}",
        ),
        validation_gate(
            "uncovered_transitions_are_not_silently_discarded",
            bool(extensions)
            and len(extensions)
            == sum(
                not parse_bool(row["already_covered_by_coarse_event"])
                for row in transitions
            ),
            f"extensions={len(extensions)}",
        ),
        validation_gate(
            "adaptive_extension_brackets_change_support_state",
            all(
                parse_bool(row["left_inside_support"])
                != parse_bool(row["right_inside_support"])
                and float(row["left_coordinate"])
                < float(row["right_coordinate"])
                for row in extensions
            ),
            "all extension brackets are sign-changing",
        ),
        validation_gate(
            "adaptive_extension_roots_pass_source_contract",
            all(parse_bool(row["refined_event_contract_passes"]) for row in extensions),
            "all refined roots pass",
        ),
        validation_gate(
            "adaptive_extension_source_hashes_are_current",
            bool(extensions) and source_hashes_current,
            f"rows={len(extensions)}",
        ),
        validation_gate(
            "formal_workbench_unchanged",
            M5283.formal_inventory_digest() == FORMAL_DIGEST,
            M5283.formal_inventory_digest(),
        ),
        validation_gate(
            "broader_claims_locked_false",
            all(
                all(not parse_bool(row[field]) for field in CLAIM_FIELDS)
                for row in extensions
            ),
            "event discovery is not a physics claim",
        ),
        validation_gate(
            "scripts_cache_absent",
            not (SCRIPTS / "__pycache__").exists(),
            str(SCRIPTS / "__pycache__"),
        ),
    ]
    passed = all(parse_bool(row["passed"]) for row in gates)
    write_csv(paths["adaptive_event_validation"], gates, ["gate"])
    write_csv(paths["adaptive_event_residual_validation"], gates, ["gate"])
    audit_result = {
        "checkpoint": CHECKPOINT,
        "mode": "D4-outer-adaptive-support-event-audit",
        "epsilon_id": M5326.EPSILON_ID,
        "acceptance_passed": passed,
        "decision": (
            "D4_OUTER_ADAPTIVE_SUPPORT_EVENT_EXTENSION_DERIVED__PROMOTE_PLAN"
            if passed
            else "D4_OUTER_ADAPTIVE_SUPPORT_EVENT_AUDIT_FAILED"
        ),
        "adaptive_transition_count": len(transitions),
        "uncovered_extension_count": len(extensions),
        "formalization_workbench_end_digest": M5283.formal_inventory_digest(),
        "runtime_seconds": time.perf_counter() - started,
    }
    atomic_json(paths["adaptive_event_result"], audit_result)
    canonicalize_refinement_result(read_json(M5326.RESULT))
    return audit_result


def refresh_adaptive_event_root_evidence() -> dict[str, Any]:
    started = time.perf_counter()
    paths = refinement_paths(M5326.EPSILON_ID)
    extensions = read_csv(paths["adaptive_event_extension"])
    if not extensions:
        raise RuntimeError("adaptive event extensions are missing")
    snapshot_manifest_path = (
        paths["pre_adaptive_event_closure"] / M5326.NODE_MANIFEST.name
    )
    if not snapshot_manifest_path.exists():
        raise FileNotFoundError(snapshot_manifest_path)
    snapshot_manifest = read_csv(snapshot_manifest_path)
    manifest_lookup = {
        row["node_id"]: row for row in snapshot_manifest
    }
    contract = read_csv(M5326.CONTRACT_5325)
    cache = M5326.load_event_cache()
    evidence: list[dict[str, Any]] = []
    old_kernel = M5326.configure_kernel()
    try:
        for extension in extensions:
            panel_index = int(extension["x_panel_index"])
            term_id = extension["term_id"]
            surface_id = extension["primary_surface_id"]
            coordinates = (
                ("LEFT", float(extension["left_coordinate"])),
                ("ROOT", float(extension["refined_event_coordinate"])),
                ("RIGHT", float(extension["right_coordinate"])),
            )
            states = {
                label: M5326.branch_state(
                    panel_index,
                    term_id,
                    surface_id,
                    coordinate,
                    contract,
                    cache,
                )
                for label, coordinate in coordinates
            }
            root_margin = float(states["ROOT"]["signed_support_margin"])
            event_contract = (
                parse_bool(states["LEFT"]["inside_reduced_term_support"])
                != parse_bool(states["RIGHT"]["inside_reduced_term_support"])
                and parse_bool(states["ROOT"]["branch_exists"])
                and abs(root_margin) <= M5326.EVENT_MARGIN_TOLERANCE
                and parse_bool(extension["refined_event_contract_passes"])
            )
            for label, coordinate in coordinates:
                state = states[label]
                evidence.append(
                    {
                        "candidate_id": extension["candidate_id"],
                        "x_panel_index": panel_index,
                        "term_id": term_id,
                        "primary_surface_id": surface_id,
                        "evidence_state": label,
                        "absolute_soft_cosine": coordinate,
                        "branch_exists": state["branch_exists"],
                        "pole_real": state["pole_real"],
                        "pole_imaginary": state["pole_imaginary"],
                        "support_id": state["support_id"],
                        "support_energy_lower": state["support_energy_lower"],
                        "support_energy_upper": state["support_energy_upper"],
                        "signed_support_margin": state["signed_support_margin"],
                        "inside_reduced_term_support": state[
                            "inside_reduced_term_support"
                        ],
                        "root_evidence_valid_for_event_extension": event_contract,
                        "contract_path": str(M5326.CONTRACT_5325),
                        "contract_sha256": digest(M5326.CONTRACT_5325),
                        **{field: False for field in CLAIM_FIELDS},
                    }
                )
    finally:
        M5326.restore_kernel(old_kernel)
    write_csv(
        paths["adaptive_event_root_evidence"],
        evidence,
        [
            "candidate_id",
            "x_panel_index",
            "term_id",
            "primary_surface_id",
            "evidence_state",
        ],
    )
    evidence_sha256 = digest(paths["adaptive_event_root_evidence"])
    for extension in extensions:
        extension["root_evidence_path"] = str(paths["adaptive_event_root_evidence"])
        extension["root_evidence_sha256"] = evidence_sha256
    write_csv(
        paths["adaptive_event_extension"],
        extensions,
        ["candidate_id", "x_panel_index", "term_id", "primary_surface_id"],
    )
    source_nodes_match = True
    for extension in extensions:
        for side in ("left", "right"):
            coordinate = float(extension[f"{side}_coordinate"])
            node_ids = extension[f"source_{side}_node_id"].split("|")
            source_nodes_match = source_nodes_match and any(
                node_id in manifest_lookup
                and math.isclose(
                    float(manifest_lookup[node_id]["absolute_soft_cosine"]),
                    coordinate,
                    rel_tol=0.0,
                    abs_tol=2.0e-15,
                )
                for node_id in node_ids
            )
    snapshot_manifest_matches = all(
        row["adaptive_manifest_sha256"] == digest(snapshot_manifest_path)
        for row in extensions
    )
    roots = [row for row in evidence if row["evidence_state"] == "ROOT"]
    gates = [
        validation_gate(
            "completed_tree_manifest_is_immutable_snapshot",
            snapshot_manifest_matches,
            digest(snapshot_manifest_path),
        ),
        validation_gate(
            "extension_bracket_nodes_match_snapshot_coordinates",
            source_nodes_match,
            f"extensions={len(extensions)}",
        ),
        validation_gate(
            "left_and_right_evidence_change_support_state",
            all(
                parse_bool(next(
                    row for row in evidence
                    if row["candidate_id"] == extension["candidate_id"]
                    and row["evidence_state"] == "LEFT"
                )["inside_reduced_term_support"])
                != parse_bool(next(
                    row for row in evidence
                    if row["candidate_id"] == extension["candidate_id"]
                    and row["evidence_state"] == "RIGHT"
                )["inside_reduced_term_support"])
                for extension in extensions
            ),
            "all brackets change support state",
        ),
        validation_gate(
            "root_support_margins_meet_contract",
            len(roots) == len(extensions)
            and all(
                abs(float(row["signed_support_margin"]))
                <= M5326.EVENT_MARGIN_TOLERANCE
                for row in roots
            ),
            f"roots={len(roots)}",
        ),
        validation_gate(
            "root_evidence_rows_are_contract_valid",
            bool(evidence)
            and all(
                parse_bool(row["root_evidence_valid_for_event_extension"])
                for row in evidence
            ),
            f"rows={len(evidence)}",
        ),
        validation_gate(
            "root_evidence_hash_is_locked_into_extensions",
            all(row["root_evidence_sha256"] == evidence_sha256 for row in extensions),
            evidence_sha256,
        ),
        validation_gate(
            "formal_workbench_unchanged",
            M5283.formal_inventory_digest() == FORMAL_DIGEST,
            M5283.formal_inventory_digest(),
        ),
        validation_gate(
            "broader_claims_locked_false",
            all(
                all(not parse_bool(row[field]) for field in CLAIM_FIELDS)
                for row in evidence
            ),
            "root evidence is not a physics claim",
        ),
        validation_gate(
            "scripts_cache_absent",
            not (SCRIPTS / "__pycache__").exists(),
            str(SCRIPTS / "__pycache__"),
        ),
    ]
    passed = all(parse_bool(row["passed"]) for row in gates)
    write_csv(paths["adaptive_event_validation"], gates, ["gate"])
    write_csv(paths["adaptive_event_residual_validation"], gates, ["gate"])
    audit_result = read_json(paths["adaptive_event_result"])
    audit_result["acceptance_passed"] = passed
    audit_result["decision"] = (
        "D4_OUTER_ADAPTIVE_SUPPORT_EVENT_ROOT_EVIDENCE_LOCKED"
        if passed
        else "D4_OUTER_ADAPTIVE_SUPPORT_EVENT_ROOT_EVIDENCE_FAILED"
    )
    audit_result["root_evidence_path"] = str(paths["adaptive_event_root_evidence"])
    audit_result["root_evidence_sha256"] = evidence_sha256
    audit_result["runtime_seconds"] = time.perf_counter() - started
    atomic_json(paths["adaptive_event_result"], audit_result)
    canonicalize_refinement_result(read_json(M5326.RESULT))
    return {
        "checkpoint": CHECKPOINT,
        "mode": "D4-outer-adaptive-event-root-evidence",
        "epsilon_id": M5326.EPSILON_ID,
        "acceptance_passed": passed,
        "decision": audit_result["decision"],
        "runtime_seconds": time.perf_counter() - started,
    }


def plan_rows_by_panel(rows: list[dict[str, str]]) -> dict[int, list[dict[str, str]]]:
    grouped: dict[int, list[dict[str, str]]] = {}
    for row in rows:
        grouped.setdefault(int(row["x_panel_index"]), []).append(dict(row))
    for panel_rows in grouped.values():
        panel_rows.sort(key=lambda row: row["initial_segment_id"])
    return grouped


def snapshot_pre_adaptive_event_state(paths: dict[str, Path]) -> None:
    snapshot = paths["pre_adaptive_event_closure"]
    snapshot.mkdir(parents=True, exist_ok=True)
    source_paths = (
        M5326.EVENT_CANDIDATES,
        M5326.EVENTS,
        M5326.INITIAL_PLAN,
        M5326.DRY_RUN,
        M5326.NODE_MANIFEST,
        M5326.ADAPTIVE_PANELS,
        M5326.FINITE_VALUE,
        M5326.RESULT,
        M5326.VALIDATION,
        M5326.STATUS,
        M5326.DOCUMENT,
    )
    for source in source_paths:
        if source.exists():
            target = snapshot / source.name
            if not target.exists():
                shutil.copy2(source, target)


def migrate_unchanged_panel_shards(
    old_manifest: list[dict[str, str]],
    old_plan_sha256: str,
    new_plan_sha256: str,
    changed_panels: set[int],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for node in old_manifest:
        panel_index = int(node["x_panel_index"])
        result_path = M5326.SHARDS / node["node_id"] / "result.json"
        action = "RECOMPUTE_CHANGED_EVENT_PANEL"
        source_hash = ""
        migrated_hash = ""
        coordinate_matches = False
        weight_matches = False
        if result_path.exists():
            result = read_json(result_path)
            source_hash = str(result.get("node_plan_sha256", ""))
            coordinate_matches = math.isclose(
                float(result["absolute_soft_cosine"]),
                float(node["absolute_soft_cosine"]),
                rel_tol=0.0,
                abs_tol=2.0e-15,
            )
            weight_matches = math.isclose(
                float(result["mapped_outer_weight"]),
                float(node["mapped_outer_weight"]),
                rel_tol=0.0,
                abs_tol=2.0e-15,
            )
            if panel_index not in changed_panels:
                reusable = (
                    result.get("node_revision") == M5326.NODE_REVISION
                    and result.get("node_id") == node["node_id"]
                    and source_hash == old_plan_sha256
                    and bool(result.get("node_complete"))
                    and coordinate_matches
                    and weight_matches
                )
                if reusable:
                    result["node_plan_sha256"] = new_plan_sha256
                    atomic_json(result_path, result)
                    migrated_hash = new_plan_sha256
                    action = "MIGRATED_IDENTICAL_NODE_TO_EXTENDED_PLAN"
                else:
                    action = "RECOMPUTE_FAILED_MIGRATION_GATES"
        else:
            action = "RECOMPUTE_MISSING_SHARD"
        rows.append(
            {
                "node_id": node["node_id"],
                "x_panel_index": panel_index,
                "absolute_soft_cosine": node["absolute_soft_cosine"],
                "mapped_outer_weight": node["mapped_outer_weight"],
                "old_node_plan_sha256": source_hash,
                "new_node_plan_sha256": migrated_hash,
                "coordinate_matches": coordinate_matches,
                "mapped_weight_matches": weight_matches,
                "migration_action": action,
                "valid_for_reuse_in_adaptive_event_extended_plan": (
                    action == "MIGRATED_IDENTICAL_NODE_TO_EXTENDED_PLAN"
                ),
                **{field: False for field in CLAIM_FIELDS},
            }
        )
    return rows


def promote_adaptive_event_extension() -> dict[str, Any]:
    started = time.perf_counter()
    paths = refinement_paths(M5326.EPSILON_ID)
    if not adaptive_event_extension_is_valid(paths):
        raise RuntimeError("validated adaptive event extension is required")
    snapshot_pre_adaptive_event_state(paths)
    snapshot = paths["pre_adaptive_event_closure"]
    old_result = read_json(snapshot / M5326.RESULT.name)
    if not bool(old_result.get("completed_full_run", False)):
        raise RuntimeError("pre-extension adaptive tree is not complete")
    old_plan = read_csv(snapshot / M5326.INITIAL_PLAN.name)
    old_manifest = read_csv(snapshot / M5326.NODE_MANIFEST.name)
    old_dry = read_json(snapshot / M5326.DRY_RUN.name)
    old_plan_sha256 = str(old_dry["node_plan_sha256"])
    dry = d4_refinement_dry_run()
    if not bool(dry["acceptance_passed"]):
        raise RuntimeError("adaptive-event-extended dry run failed")
    new_plan = read_csv(M5326.INITIAL_PLAN)
    new_plan_sha256 = str(dry["node_plan_sha256"])
    old_by_panel = plan_rows_by_panel(old_plan)
    new_by_panel = plan_rows_by_panel(new_plan)
    all_panels = set(old_by_panel) | set(new_by_panel)
    changed_panels = {
        panel
        for panel in all_panels
        if old_by_panel.get(panel, []) != new_by_panel.get(panel, [])
    }
    extension_panels = {
        int(row["x_panel_index"])
        for row in read_csv(paths["adaptive_event_extension"])
    }
    migration = migrate_unchanged_panel_shards(
        old_manifest, old_plan_sha256, new_plan_sha256, changed_panels
    )
    write_csv(paths["shard_migration"], migration, ["x_panel_index", "node_id"])
    migrated = [
        row
        for row in migration
        if row["migration_action"] == "MIGRATED_IDENTICAL_NODE_TO_EXTENDED_PLAN"
    ]
    recompute = [row for row in migration if row not in migrated]
    events = read_csv(M5326.EVENTS)
    unchanged_panels_identical = all(
        old_by_panel.get(panel, []) == new_by_panel.get(panel, [])
        for panel in all_panels - changed_panels
    )
    gates = [
        validation_gate(
            "adaptive_event_extended_dry_run_passes",
            bool(dry["acceptance_passed"]),
            dry["decision"],
        ),
        validation_gate(
            "all_validated_adaptive_events_are_promoted",
            len(events) == int(dry["event_candidate_count"])
            and len(events)
            == int(old_dry["event_candidate_count"])
            + len(read_csv(paths["adaptive_event_extension"]))
            and all(parse_bool(row["event_contract_passes"]) for row in events),
            f"events={len(events)}",
        ),
        validation_gate(
            "only_extension_panels_change_initial_geometry",
            changed_panels == extension_panels and unchanged_panels_identical,
            "changed=" + "|".join(map(str, sorted(changed_panels))),
        ),
        validation_gate(
            "unchanged_node_reuse_requires_exact_coordinate_and_weight_identity",
            bool(migrated)
            and all(
                parse_bool(row["coordinate_matches"])
                and parse_bool(row["mapped_weight_matches"])
                and row["new_node_plan_sha256"] == new_plan_sha256
                for row in migrated
            ),
            f"migrated={len(migrated)}",
        ),
        validation_gate(
            "changed_event_panel_nodes_are_forced_to_recompute",
            bool(recompute)
            and all(
                int(row["x_panel_index"]) in changed_panels
                and row["migration_action"] == "RECOMPUTE_CHANGED_EVENT_PANEL"
                for row in recompute
            )
            and all(
                not parse_bool(row["valid_for_reuse_in_adaptive_event_extended_plan"])
                for row in recompute
            ),
            f"recompute={len(recompute)}",
        ),
        validation_gate(
            "old_and_new_plan_hashes_are_distinct",
            old_plan_sha256 != new_plan_sha256,
            f"old={old_plan_sha256};new={new_plan_sha256}",
        ),
        validation_gate(
            "pre_extension_state_is_snapshotted",
            (paths["pre_adaptive_event_closure"] / M5326.RESULT.name).exists()
            and (paths["pre_adaptive_event_closure"] / M5326.INITIAL_PLAN.name).exists(),
            str(paths["pre_adaptive_event_closure"]),
        ),
        validation_gate(
            "formal_workbench_unchanged",
            M5283.formal_inventory_digest() == FORMAL_DIGEST,
            M5283.formal_inventory_digest(),
        ),
        validation_gate(
            "broader_claims_locked_false",
            all(
                all(not parse_bool(row[field]) for field in CLAIM_FIELDS)
                for row in migration
            ),
            "cache migration is not a physics claim",
        ),
        validation_gate(
            "scripts_cache_absent",
            not (SCRIPTS / "__pycache__").exists(),
            str(SCRIPTS / "__pycache__"),
        ),
    ]
    passed = all(parse_bool(row["passed"]) for row in gates)
    write_csv(paths["shard_migration_validation"], gates, ["gate"])
    atomic_json(
        M5326.STATUS,
        {
            "checkpoint": CHECKPOINT,
            "state": "READY_ADAPTIVE_EVENT_EXTENDED_REFINEMENT" if passed else "BLOCKED",
            "decision": (
                "D4_OUTER_ADAPTIVE_EVENTS_PROMOTED__RUN_REFINEMENT"
                if passed
                else "D4_OUTER_ADAPTIVE_EVENT_PROMOTION_FAILED"
            ),
            "decay_node_id": DECAY_NODE_ID,
            "epsilon_id": M5326.EPSILON_ID,
            "promoted_event_count": len(events),
            "changed_panel_indices": sorted(changed_panels),
            "migrated_shard_count": len(migrated),
            "recompute_shard_count": len(recompute),
        },
    )
    return {
        "checkpoint": CHECKPOINT,
        "mode": "D4-outer-adaptive-event-plan-promotion",
        "epsilon_id": M5326.EPSILON_ID,
        "acceptance_passed": passed,
        "decision": (
            "D4_OUTER_ADAPTIVE_EVENTS_PROMOTED__RUN_REFINEMENT"
            if passed
            else "D4_OUTER_ADAPTIVE_EVENT_PROMOTION_FAILED"
        ),
        "promoted_event_count": len(events),
        "changed_panel_indices": sorted(changed_panels),
        "migrated_shard_count": len(migrated),
        "recompute_shard_count": len(recompute),
        "runtime_seconds": time.perf_counter() - started,
    }


def configure_smoke() -> dict[str, Path]:
    paths = smoke_paths()
    assignments = {
        "SOURCE": paths["source"],
        "SHARDS": paths["shards"],
        "DRY_RUN": paths["dry_run"],
        "REDUCED_CONTRACT": paths["contract"],
        "IDENTITY_AUDIT": paths["identity"],
        "NODE_PLAN": paths["plan"],
        "NODE_MANIFEST": paths["manifest"],
        "ALL_POLES": paths["poles"],
        "ALL_FITS": paths["fits"],
        "ALL_CLASSIFICATIONS": paths["classifications"],
        "ALL_CELL_INTEGRALS": paths["cell_integrals"],
        "OUTER_TOTALS": paths["outer_totals"],
        "PANEL_CONVERGENCE": paths["panel_convergence"],
        "MATERIAL_TOPOLOGY": paths["material_topology"],
        "RESULT": paths["result"],
        "VALIDATION": paths["validation"],
        "RESIDUAL_VALIDATION": paths["residual_validation"],
        "STATUS": paths["status"],
        "DOCUMENT": paths["document"],
        "CHECKPOINT": CHECKPOINT,
        "PARENT_CHECKPOINT": PARENT_CHECKPOINT,
        "MARKER": "MTS_5334_D4_OUTER_E0025_POLE_TOPOLOGY_SMOKE",
        "REVISION": "D4-outer-E0025-pole-topology-smoke-v1",
        "NODE_REVISION": "D4-outer-E0025-pole-topology-node-v1",
        "DECAY_NODE_ID": DECAY_NODE_ID,
        "EPSILON_ID": "E0025",
        "EPSILON": M5327.EPSILON_VALUES["E0025"],
        "EXPECTED_CELL_COUNT": EXPECTED_CELL_COUNT,
        "EXPECTED_PANEL_COUNT": EXPECTED_PANEL_COUNT,
        "EXPECTED_NODE_COUNT": EXPECTED_COARSE_NODE_COUNT,
    }
    for name, value in assignments.items():
        setattr(M5325, name, value)
    M5325.dry_run = d4_smoke_dry_run
    M5325.load_validated_dry_run = d4_load_validated_smoke_dry_run
    return paths


def d4_smoke_dry_run() -> dict[str, Any]:
    started = time.perf_counter()
    M5325.SOURCE.mkdir(parents=True, exist_ok=True)
    old = M5325.configure_kernel()
    try:
        parent = read_json(RESULT_5324)
        parent_validation = read_csv(VALIDATION_5324)
        node_summary = next(
            row
            for row in read_csv(TOPOLOGY_SUMMARY_5324)
            if row["decay_node_id"] == DECAY_NODE_ID
        )
        contract = M5325.build_reduced_contract()
        plan = M5312.build_node_plan(contract)
        write_csv(M5325.NODE_PLAN, plan, ["x_panel_index", "outer_order", "node_id"])
        evaluate = M5312.M5305.component_evaluator(M5312.M5303.synthetic_context())
        identity = M5312.identity_audit_rows(contract, evaluate)
        write_csv(
            M5325.IDENTITY_AUDIT,
            identity,
            ["contract_index", "epsilon_id", "MC12_term_id"],
        )
        panel_ids = sorted({int(row["x_panel_index"]) for row in contract})
        checks = {
            "parent_5324_decay_angle_preflight_accepted": bool(parent["acceptance_passed"]),
            "parent_5324_validation_passes": bool(parent_validation)
            and all(parse_bool(row["passed"]) for row in parent_validation),
            "D4_outer_topology_preflight_passes": parse_bool(
                node_summary["topology_node_preflight_passes"]
            ),
            "D4_outer_contract_has_55_cells_and_13_panels": len(contract)
            == EXPECTED_CELL_COUNT
            and panel_ids == list(range(1, EXPECTED_PANEL_COUNT + 1)),
            "all_reduced_cells_are_derived_and_parent_topology_safe": all(
                parse_bool(row["zero_cell_derived_from_active_orbit"])
                and parse_bool(row["valid_for_MC04_MC12_identity_reduction"])
                for row in contract
            ),
            "MC04_MC12_identity_transfers_at_D4_outer": bool(identity)
            and all(
                parse_bool(row["valid_for_MC04_MC12_identity_transfer"])
                for row in identity
            ),
            "Q2_Q4_plan_covers_all_13_panels": len(plan)
            == EXPECTED_COARSE_NODE_COUNT
            and {int(row["x_panel_index"]) for row in plan}
            == set(range(1, EXPECTED_PANEL_COUNT + 1))
            and all(
                parse_bool(row["valid_for_resumable_outer_soft_node"])
                for row in plan
            ),
            "formalization_workbench_unchanged": M5283.formal_inventory_digest()
            == parent["formalization_workbench_end_digest"]
            == FORMAL_DIGEST,
        }
        accepted = all(checks.values())
        result = {
            "checkpoint": CHECKPOINT,
            "parent_checkpoint": PARENT_CHECKPOINT,
            "mode": "D4-outer-E0025-pole-topology-smoke-dry-run",
            "checks": checks,
            "acceptance_passed": accepted,
            "decision": (
                "DRY_RUN_ACCEPTED__RUN_D4_OUTER_E0025_POLE_TOPOLOGY_SMOKE"
                if accepted
                else "D4_OUTER_E0025_POLE_TOPOLOGY_SMOKE_DRY_RUN_BLOCKED"
            ),
            "decay_node_id": DECAY_NODE_ID,
            "absolute_decay_cosine": M5325.decay_coordinate(),
            "reduced_contract_cell_count": len(contract),
            "soft_panel_count": len(panel_ids),
            "planned_node_count": len(plan),
            "identity_audit_row_count": len(identity),
            "contract_sha256": digest(M5325.REDUCED_CONTRACT),
            "node_plan_sha256": M5325.node_plan_sha256(plan),
            "runtime_seconds": time.perf_counter() - started,
            **{field: False for field in M5325.CLAIM_FIELDS},
        }
        atomic_json(M5325.DRY_RUN, result)
        return result
    finally:
        M5325.restore_kernel(old)


def d4_load_validated_smoke_dry_run() -> dict[str, Any]:
    required = (
        M5325.DRY_RUN,
        M5325.REDUCED_CONTRACT,
        M5325.IDENTITY_AUDIT,
        M5325.NODE_PLAN,
    )
    if not all(path.exists() for path in required):
        return d4_smoke_dry_run()
    cached = read_json(M5325.DRY_RUN)
    plan = read_csv(M5325.NODE_PLAN)
    identity = read_csv(M5325.IDENTITY_AUDIT)
    current = (
        bool(cached.get("acceptance_passed"))
        and cached.get("decision")
        == "DRY_RUN_ACCEPTED__RUN_D4_OUTER_E0025_POLE_TOPOLOGY_SMOKE"
        and cached.get("contract_sha256") == digest(M5325.REDUCED_CONTRACT)
        and cached.get("node_plan_sha256") == M5325.node_plan_sha256(plan)
        and len(plan) == EXPECTED_COARSE_NODE_COUNT
        and bool(identity)
        and all(
            parse_bool(row["valid_for_MC04_MC12_identity_transfer"])
            for row in identity
        )
        and all(parse_bool(row["passed"]) for row in read_csv(VALIDATION_5324))
    )
    return cached if current else d4_smoke_dry_run()


def topology_panel_bounds() -> dict[int, tuple[float, float]]:
    return {
        int(row["x_panel_index"]): (
            float(row["lower_absolute_soft_cosine"]),
            float(row["upper_absolute_soft_cosine"]),
        )
        for row in read_csv(TOPOLOGY_PANELS_5324)
        if row["decay_node_id"] == DECAY_NODE_ID
    }


def d4_refinement_dry_run() -> dict[str, Any]:
    started = time.perf_counter()
    M5326.SOURCE.mkdir(parents=True, exist_ok=True)
    old = M5326.configure_kernel()
    try:
        parent = read_json(M5326.RESULT_5325)
        parent_validation = read_csv(M5326.VALIDATION_5325)
        candidates = M5326.event_candidate_rows()
        M5326.EXPECTED_EVENT_COUNT = len(candidates)
        events = M5326.derive_events()
        candidate_lookup = {row["candidate_id"]: row for row in candidates}
        for event in events:
            candidate = candidate_lookup.get(event["candidate_id"], {})
            event["candidate_source"] = candidate.get(
                "candidate_source", "COARSE_SMOKE_INVENTORY"
            )
            for field in (
                "adaptive_manifest_sha256",
                "adaptive_pole_sha256",
                "adaptive_classification_sha256",
                "source_left_node_id",
                "source_right_node_id",
            ):
                event[field] = candidate.get(field, "")
        write_csv(M5326.EVENTS, events, ["event_id", "x_panel_index", "term_id"])
        initial = M5326.build_initial_plan(events)
        limits = M5326.panel_limits(read_csv(M5326.CONTRACT_5325))
        total_width = sum(float(row["segment_width"]) for row in initial)
        candidate_panels = {int(row["x_panel_index"]) for row in candidates}
        event_panels = {int(row["x_panel_index"]) for row in events}
        panel_bounds = topology_panel_bounds()
        panel_violations = []
        bracket_violations = []
        support_margin_violations = []
        branch_death_error_violations = []
        for event in events:
            coordinate = float(event["event_coordinate"])
            lower, upper = panel_bounds[int(event["x_panel_index"])]
            panel_violations.append(max(lower - coordinate, coordinate - upper, 0.0))
            bracket_left = float(event["source_bracket_left"])
            bracket_right = float(event["source_bracket_right"])
            bracket_violations.append(
                max(bracket_left - coordinate, coordinate - bracket_right, 0.0)
            )
            if event["event_type"] in {"SUPPORT_ENTRY", "SUPPORT_EXIT"}:
                support_margin_violations.append(
                    max(
                        abs(float(event["event_signed_support_margin"]))
                        - M5326.EVENT_MARGIN_TOLERANCE,
                        0.0,
                    )
                )
            if event["event_type"] == "BRANCH_DEATH":
                branch_death_error_violations.append(
                    max(
                        float(event["event_coordinate_error_estimate"])
                        - M5326.EVENT_COORDINATE_ERROR_TOLERANCE,
                        0.0,
                    )
                )
        maximum_panel_violation = max(panel_violations, default=math.inf)
        maximum_bracket_violation = max(bracket_violations, default=math.inf)
        maximum_support_margin_violation = max(
            support_margin_violations, default=0.0
        )
        maximum_branch_death_error_violation = max(
            branch_death_error_violations, default=0.0
        )
        checks = {
            "D4_outer_E0025_smoke_is_source_complete": bool(parent["acceptance_passed"]),
            "D4_outer_E0025_smoke_validation_passes": bool(parent_validation)
            and all(parse_bool(row["passed"]) for row in parent_validation),
            "material_support_crossings_are_derived_not_enumerated": bool(candidates)
            and len(candidates) == len(events)
            and candidate_panels == event_panels
            and all(parse_bool(row["event_contract_passes"]) for row in events),
            "support_crossings_refine_inside_independent_5324_topology_panels": len(
                panel_bounds
            )
            == EXPECTED_PANEL_COUNT
            and maximum_panel_violation <= EVENT_PANEL_CONTAINMENT_TOLERANCE
            and maximum_bracket_violation <= EVENT_PANEL_CONTAINMENT_TOLERANCE
            and maximum_support_margin_violation == 0.0
            and maximum_branch_death_error_violation == 0.0,
            "event_aligned_plan_covers_D4_outer_soft_domain": len(limits)
            == EXPECTED_PANEL_COUNT
            and len(initial) == M5326.expected_initial_segment_count(events)
            and abs(total_width - M5312.M5308.angular_limit()) <= 2.0e-12
            and all(float(row["segment_width"]) > 0.0 for row in initial),
            "Q4_Q8_adaptive_contract_is_active": M5326.OUTER_ORDERS == (4, 8)
            and M5326.LOCAL_OUTER_CHANGE_LIMIT == M5312.OUTER_RELATIVE_CHANGE_LIMIT,
            "formalization_workbench_unchanged": M5283.formal_inventory_digest()
            == parent["formalization_workbench_end_digest"]
            == FORMAL_DIGEST,
        }
        accepted = all(checks.values())
        result = {
            "checkpoint": CHECKPOINT,
            "parent_checkpoint": PARENT_CHECKPOINT,
            "mode": "D4-outer-event-aligned-refinement-dry-run",
            "checks": checks,
            "acceptance_passed": accepted,
            "decision": (
                "DRY_RUN_ACCEPTED__RUN_D4_OUTER_EVENT_ALIGNED_REFINEMENT"
                if accepted
                else "D4_OUTER_EVENT_ALIGNED_REFINEMENT_DRY_RUN_BLOCKED"
            ),
            "decay_node_id": DECAY_NODE_ID,
            "absolute_decay_cosine": ABSOLUTE_DECAY_COSINE,
            "epsilon_id": M5326.EPSILON_ID,
            "epsilon": M5326.EPSILON,
            "event_candidate_count": len(candidates),
            "refined_event_count": len(events),
            "event_panel_indices": sorted(event_panels),
            "maximum_5324_panel_containment_violation": maximum_panel_violation,
            "maximum_source_bracket_containment_violation": maximum_bracket_violation,
            "maximum_support_margin_tolerance_violation": maximum_support_margin_violation,
            "maximum_branch_death_error_tolerance_violation": maximum_branch_death_error_violation,
            "initial_segment_count": len(initial),
            "node_plan_sha256": M5326.plan_sha256(initial),
            "runtime_seconds": time.perf_counter() - started,
            **{field: False for field in M5326.CLAIM_FIELDS},
        }
        atomic_json(M5326.DRY_RUN, result)
        return result
    finally:
        M5326.restore_kernel(old)


def d4_load_validated_refinement_dry_run() -> dict[str, Any]:
    required = (
        M5326.DRY_RUN,
        M5326.EVENT_CANDIDATES,
        M5326.EVENT_STATES,
        M5326.EVENTS,
        M5326.INITIAL_PLAN,
    )
    if not all(path.exists() for path in required):
        return d4_refinement_dry_run()
    cached = read_json(M5326.DRY_RUN)
    events = read_csv(M5326.EVENTS)
    initial = read_csv(M5326.INITIAL_PLAN)
    M5326.EXPECTED_EVENT_COUNT = len(events)
    current = (
        bool(cached.get("acceptance_passed"))
        and cached.get("decision")
        == "DRY_RUN_ACCEPTED__RUN_D4_OUTER_EVENT_ALIGNED_REFINEMENT"
        and len(events) > 0
        and all(parse_bool(row["event_contract_passes"]) for row in events)
        and all(row["contract_sha256"] == digest(M5326.CONTRACT_5325) for row in events)
        and all(row["parent_pole_sha256"] == digest(M5326.POLES_5325) for row in events)
        and len(initial) == M5326.expected_initial_segment_count(events)
        and cached.get("node_plan_sha256") == M5326.plan_sha256(initial)
        and all(parse_bool(row["passed"]) for row in read_csv(M5326.VALIDATION_5325))
    )
    return cached if current else d4_refinement_dry_run()


def configure_refinement(epsilon_id: str = "E0025") -> dict[str, Path]:
    smoke = configure_smoke()
    paths = refinement_paths(epsilon_id)
    assignments = {
        "SOURCE": paths["source"],
        "SHARDS": paths["shards"],
        "RESULT_5325": smoke["result"],
        "VALIDATION_5325": smoke["validation"],
        "CONTRACT_5325": smoke["contract"],
        "PLAN_5325": smoke["plan"],
        "POLES_5325": smoke["poles"],
        "CLASSIFICATIONS_5325": smoke["classifications"],
        "PANELS_5325": smoke["panel_convergence"],
        "EVENT_CANDIDATES": paths["event_candidates"],
        "EVENT_CACHE": paths["event_cache"],
        "EVENT_STATES": paths["event_states"],
        "EVENTS": paths["events"],
        "INITIAL_PLAN": paths["initial_plan"],
        "DRY_RUN": paths["dry_run"],
        "NODE_MANIFEST": paths["node_manifest"],
        "ADAPTIVE_PANELS": paths["adaptive_panels"],
        "OFF_AXIS_POLES": paths["poles"],
        "OFF_AXIS_FITS": paths["fits"],
        "OFF_AXIS_CLASSIFICATIONS": paths["classifications"],
        "CELL_INTEGRALS": paths["cell_integrals"],
        "ENERGY_REPAIRS": paths["energy_repairs"],
        "NEAR_SUPPORT_REPAIRS": paths["near_repairs"],
        "NEAR_SUPPORT_FITS": paths["near_fits"],
        "NEAR_SUPPORT_IDENTITIES": paths["near_identities"],
        "FINITE_VALUE": paths["finite"],
        "RESULT": paths["result"],
        "VALIDATION": paths["validation"],
        "RESIDUAL_VALIDATION": paths["residual_validation"],
        "STATUS": paths["status"],
        "DOCUMENT": paths["document"],
        "CHECKPOINT": CHECKPOINT,
        "PARENT_CHECKPOINT": PARENT_CHECKPOINT,
        "MARKER": f"MTS_5334_D4_OUTER_{epsilon_id}_EVENT_ALIGNED_REFINEMENT",
        "REVISION": f"D4-outer-event-aligned-refinement-v1-{epsilon_id}",
        "NODE_REVISION": f"D4-outer-{epsilon_id}-node-v1",
        "DECAY_NODE_ID": DECAY_NODE_ID,
        "EPSILON_ID": epsilon_id,
        "EPSILON": M5327.EPSILON_VALUES[epsilon_id],
        "EXPECTED_TOPOLOGY_PANEL_COUNT": EXPECTED_PANEL_COUNT,
    }
    for name, value in assignments.items():
        setattr(M5326, name, value)
    M5325.EPSILON_ID = epsilon_id
    M5325.EPSILON = M5327.EPSILON_VALUES[epsilon_id]
    M5326.dry_run = d4_refinement_dry_run
    M5326.load_validated_dry_run = d4_load_validated_refinement_dry_run
    M5326.event_candidate_rows = d4_event_candidate_rows
    if paths["events"].exists():
        M5326.EXPECTED_EVENT_COUNT = len(read_csv(paths["events"]))
    return paths


def disable_D2_owner_channel_transfer(epsilon_id: str) -> None:
    del epsilon_id
    M5327.OWNER_CHANNEL_CERTIFICATE_BYPASS = True
    M5327.OWNER_CHANNEL_CERTIFICATE_ROWS.clear()
    M5327.OWNER_CHANNEL_CERTIFICATE_FIT_ROWS.clear()
    M5327.ADAPTIVE_DIVISOR_RUNTIME_CERTIFICATES.clear()
    M5326.M5312.fit_node_poles = M5327.ORIGINAL_FIT_NODE_POLES


def d4_target_source(epsilon_id: str) -> Path:
    return SOURCE / epsilon_id


def d4_target_paths(epsilon_id: str) -> dict[str, Path]:
    return refinement_paths(epsilon_id)


def configure_D4_target(epsilon_id: str) -> dict[str, Path]:
    configure_refinement(epsilon_id)
    paths = ORIGINAL_CONFIGURE_TARGET(epsilon_id)
    M5326.MARKER = f"MTS_5334_D4_OUTER_{epsilon_id}_EVENT_ALIGNED_REFINEMENT"
    M5326.REVISION = f"D4-outer-event-aligned-refinement-v1-{epsilon_id}"
    M5326.NODE_REVISION = f"D4-outer-{epsilon_id}-node-v1"
    M5326.DECAY_NODE_ID = DECAY_NODE_ID
    M5326.EXPECTED_TOPOLOGY_PANEL_COUNT = EXPECTED_PANEL_COUNT
    M5326.dry_run = d4_refinement_dry_run
    M5326.load_validated_dry_run = d4_load_validated_refinement_dry_run
    if paths["events"].exists():
        M5326.EXPECTED_EVENT_COUNT = len(read_csv(paths["events"]))
    return paths


def configure_ladder() -> None:
    base = configure_refinement("E0025")
    M5327.SOURCE = SOURCE
    M5327.LADDER = LADDER
    M5327.PAIRWISE = PAIRWISE
    M5327.TRENDS = TRENDS
    M5327.RESULT = RESULT
    M5327.VALIDATION = VALIDATION
    M5327.RESIDUAL_VALIDATION = RESIDUAL_VALIDATION
    M5327.STATUS = STATUS
    M5327.DOCUMENT = DOCUMENT
    M5327.RESULT_5326 = base["result"]
    M5327.VALIDATION_5326 = base["validation"]
    M5327.FINITE_5326 = base["finite"]
    M5327.CHECKPOINT = CHECKPOINT
    M5327.PARENT_CHECKPOINT = PARENT_CHECKPOINT
    M5327.MARKER = "MTS_5334_D4_OUTER_REGULATOR_LADDER_CONTROLLER"
    M5327.REVISION = "D4-outer-regulator-ladder-controller-v1"
    M5327.FORMAL_DIGEST = FORMAL_DIGEST
    M5327.target_source = d4_target_source
    M5327.target_paths = d4_target_paths
    M5327.configure_owner_channel_certificate = disable_D2_owner_channel_transfer
    M5327.REQUIRED_LOCAL_REPAIR_MODES_BY_EPSILON = {}
    M5327.REQUIRED_LOCAL_REPAIR_REVISION_BY_EPSILON = {}
    M5327.E020_EXTENDED_ENERGY_NODE_IDS = ()
    M5327.E020_DIRECT_CONTOUR_FALLBACK_NODE_IDS = ()
    M5327.E020_TOPOLOGY_REPAIR_NODE_IDS = ()
    M5327.TOPOLOGY_SAFE_REPAIR_REVISION = "D4-outer-topology-safe-symmetric-interior-laurent-v1"
    M5327.OFF_SUPPORT_ENERGY_REPAIR_REVISION = "D4-outer-off-support-real-axis-quadrature-v1"
    M5327.configure_target = configure_D4_target


def canonicalize_smoke_result(result: dict[str, Any]) -> dict[str, Any]:
    value = dict(result)
    value["marker"] = "MTS_5334_D4_OUTER_E0025_POLE_TOPOLOGY_SMOKE"
    value["revision"] = "D4-outer-E0025-pole-topology-smoke-v1"
    value["mode"] = "D4-outer-E0025-pole-topology-smoke"
    value["decay_node_id"] = DECAY_NODE_ID
    if "PAUSED" in str(value.get("decision", "")):
        value["decision"] = "D4_OUTER_E0025_SMOKE_PAUSED__RESUME_SAVED_SHARDS"
    elif bool(value.get("finite_regulator_fixed_decay_integral_accepted", False)):
        value["decision"] = (
            "D4_OUTER_E0025_COARSE_FIXED_DECAY_ACCEPTED__VERIFY_EVENT_ALIGNED_VALUE"
        )
    elif bool(value.get("acceptance_passed", False)):
        value["decision"] = (
            "D4_OUTER_E0025_POLE_TOPOLOGY_LOCALIZED__BUILD_EVENT_ALIGNED_REFINEMENT"
        )
    else:
        value["decision"] = "D4_OUTER_E0025_INNER_KERNEL_FAILURES_REQUIRE_REPAIR"
    atomic_json(M5325.RESULT, value)
    return value


def canonicalize_smoke_validation(result: dict[str, Any]) -> dict[str, Any]:
    replacements = {
        "D2_preflight_and_identity_pass": "D4_outer_preflight_and_identity_pass",
        "all_planned_E0025_nodes_complete_and_pass": (
            "all_planned_D4_outer_E0025_nodes_complete_and_pass"
        ),
        "all_eleven_panel_diagnostics_present": "all_thirteen_panel_diagnostics_present",
    }
    rows = read_csv(M5325.VALIDATION)
    for row in rows:
        row["gate"] = replacements.get(row["gate"], row["gate"])
    write_csv(M5325.VALIDATION, rows, ["gate"])
    write_csv(M5325.RESIDUAL_VALIDATION, rows, ["gate"])
    value = dict(result)
    value["decision"] = (
        "VALIDATED_D4_OUTER_E0025_POLE_TOPOLOGY_SMOKE"
        if bool(value.get("acceptance_passed", False))
        else "D4_OUTER_E0025_POLE_TOPOLOGY_SMOKE_VALIDATION_FAILED"
    )
    render_smoke_document(
        read_json(M5325.RESULT), bool(value.get("acceptance_passed", False))
    )
    return value


def render_smoke_document(result: dict[str, Any], passed: bool) -> None:
    lines = [
        "# 5334 - D4 outer E0025 pole-topology smoke",
        "",
        "## Purpose",
        "",
        "This is the missing paired-GL4 outer decay node. It rebuilds the",
        f"{EXPECTED_CELL_COUNT}-cell, {EXPECTED_PANEL_COUNT}-panel contract at",
        f"`|d|={ABSOLUTE_DECAY_COSINE}` without transferring the D2 pole topology.",
        "",
        "## Result",
        "",
        f"- completed nodes: `{result['completed_node_count']}/{result['planned_node_count']}`;",
        f"- all inner nodes pass: `{result['all_inner_nodes_pass']}`;",
        f"- geometric poles: `{result['geometric_pole_count']}`;",
        f"- material simple poles: `{result['material_simple_pole_count']}`;",
        f"- unresolved poles: `{result['unresolved_pole_count']}`;",
        f"- failed coarse outer panels: `{result['failed_outer_panel_indices']}`;",
        f"- coarse outer relative change: `{result['outer_relative_change']}`;",
        f"- coarse fixed-decay acceptance: `{result['finite_regulator_fixed_decay_integral_accepted']}`;",
        f"- decision: `{result['decision']}`;",
        f"- validation: `{'PASS' if passed else 'FAIL'}`.",
        "",
        "## Claim boundary",
        "",
        "The scan source-completes the D4_OUTER E0025 pole inventory only. Its",
        "coarse outer convergence fails, so no fixed-decay value is accepted.",
        "The event-aligned refinement, regulator-zero limit, GL2/GL4 comparison,",
        "endpoint cap, phase space, UV coefficient, local GR and full MTS remain",
        "separate gates.",
    ]
    M5325.DOCUMENT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def d4_fixed_decay_claim_field() -> str:
    return f"valid_for_D4_outer_{M5326.EPSILON_ID}_fixed_decay_integral"


def d4_refinement_method(event_count: int) -> str:
    count_label = NUMBER_WORDS.get(event_count, str(event_count))
    return f"{count_label}_SUPPORT_EVENTS_SQUARED_Q4_Q8_ADAPTIVE"


def d4_refinement_decision(result: dict[str, Any]) -> str:
    if "PAUSED" in str(result.get("decision", "")):
        return f"D4_OUTER_EVENT_ALIGNED_{M5326.EPSILON_ID}_PAUSED__RESUME_SHARDS"
    if bool(result.get("acceptance_passed", False)):
        return f"D4_OUTER_EVENT_ALIGNED_{M5326.EPSILON_ID}_ACCEPTED__CONTINUE_LADDER"
    if bool(result.get("completed_full_run", False)):
        return f"D4_OUTER_EVENT_ALIGNED_{M5326.EPSILON_ID}_REQUIRES_REFINEMENT"
    return f"D4_OUTER_EVENT_ALIGNED_{M5326.EPSILON_ID}_INNER_FAILURES_LOCALIZED"


def canonicalize_refinement_finite_value(event_count: int) -> None:
    if not M5326.FINITE_VALUE.exists():
        return
    rows = read_csv(M5326.FINITE_VALUE)
    fixed_claim = d4_fixed_decay_claim_field()
    for row in rows:
        accepted = parse_bool(row["finite_regulator_fixed_decay_integral_accepted"])
        for field in tuple(row):
            if field.startswith("valid_for_D2_"):
                row.pop(field)
        row["decay_node_id"] = DECAY_NODE_ID
        row["epsilon_id"] = M5326.EPSILON_ID
        row["epsilon"] = M5326.EPSILON
        row["method"] = d4_refinement_method(event_count)
        row[fixed_claim] = accepted
        row["valid_for_D4_outer_regulator_zero_limit"] = False
    write_csv(M5326.FINITE_VALUE, rows, ["decay_node_id", "epsilon_id"])


def canonicalize_refinement_status(result: dict[str, Any]) -> None:
    status = read_json(M5326.STATUS) if M5326.STATUS.exists() else {}
    status["checkpoint"] = CHECKPOINT
    status["decision"] = result["decision"]
    status["decay_node_id"] = DECAY_NODE_ID
    status["epsilon_id"] = M5326.EPSILON_ID
    if "stage" in status:
        status["stage"] = str(status["stage"]).replace("D2_", "D4_OUTER_")
    atomic_json(M5326.STATUS, status)


def canonicalize_refinement_result(result: dict[str, Any]) -> dict[str, Any]:
    value = dict(result)
    event_count = len(read_csv(M5326.EVENTS)) if M5326.EVENTS.exists() else 0
    canonicalize_refinement_finite_value(event_count)
    source_paths = {
        Path(row["path"])
        for row in value.get("source_files", [])
        if Path(row["path"]).exists()
    }
    source_paths.add(Path(__file__).resolve())
    value["source_files"] = [
        {"path": str(path), "sha256": digest(path)}
        for path in sorted(source_paths, key=str)
    ]
    value["marker"] = f"MTS_5334_D4_OUTER_{M5326.EPSILON_ID}_EVENT_ALIGNED_REFINEMENT"
    value["revision"] = f"D4-outer-event-aligned-refinement-v1-{M5326.EPSILON_ID}"
    value["mode"] = f"D4-outer-event-aligned-{M5326.EPSILON_ID}-refinement"
    value["decay_node_id"] = DECAY_NODE_ID
    value["epsilon_id"] = M5326.EPSILON_ID
    value["epsilon"] = M5326.EPSILON
    value["support_event_count"] = event_count
    value["finite_regulator_method"] = d4_refinement_method(event_count)
    value["decision"] = d4_refinement_decision(value)
    fixed_claim = d4_fixed_decay_claim_field()
    prior_boundary = dict(value.get("claim_boundary", {}))
    value["claim_boundary"] = {
        fixed_claim: bool(value.get("acceptance_passed", False)),
        "valid_for_D4_outer_regulator_zero_limit": False,
        **{field: bool(prior_boundary.get(field, False)) for field in CLAIM_FIELDS},
        "reason": (
            f"This is one event-aligned finite-regulator value at {DECAY_NODE_ID}. "
            "The D4_OUTER regulator-zero and decay-angle limits remain separate."
        ),
    }
    atomic_json(M5326.RESULT, value)
    canonicalize_refinement_status(value)
    return value


def validate_refinement_semantics(result: dict[str, Any]) -> dict[str, Any]:
    started = time.perf_counter()
    paths = refinement_paths(M5326.EPSILON_ID)
    events = read_csv(M5326.EVENTS)
    finite = read_csv(M5326.FINITE_VALUE)
    manifest = read_csv(M5326.NODE_MANIFEST)
    status = read_json(M5326.STATUS)
    fixed_claim = d4_fixed_decay_claim_field()
    method = d4_refinement_method(len(events))
    completed_manifest = [row for row in manifest if row["shard_state"] != "PENDING"]
    shard_results = []
    for row in completed_manifest:
        path = M5326.SHARDS / row["node_id"] / "result.json"
        try:
            shard_results.append(read_json(path))
        except (json.JSONDecodeError, OSError):
            shard_results.append({"decision": "UNREADABLE"})
    semantic_payload = json.dumps(
        {
            "decision": result.get("decision"),
            "mode": result.get("mode"),
            "decay_node_id": result.get("decay_node_id"),
            "claim_boundary": result.get("claim_boundary"),
            "status": status,
            "finite": finite,
        },
        sort_keys=True,
    )
    sources_current = all(
        Path(row["path"]).exists()
        and digest(Path(row["path"])) == row["sha256"]
        for row in result["source_files"]
    )
    incomplete = not bool(result.get("completed_full_run", False))
    gates = [
        validation_gate(
            "D4_outer_identity_is_canonical",
            result.get("decay_node_id") == DECAY_NODE_ID
            and result.get("epsilon_id") == M5326.EPSILON_ID
            and str(result.get("decision", "")).startswith("D4_OUTER_")
            and "D2_" not in semantic_payload,
            result.get("decision", ""),
        ),
        validation_gate(
            "support_event_method_matches_derived_event_inventory",
            len(events) == int(result["support_event_count"])
            and len(finite) == 1
            and finite[0]["method"] == method,
            f"events={len(events)};method={method}",
        ),
        validation_gate(
            "D4_outer_claim_fields_replace_inherited_D2_fields",
            fixed_claim in result["claim_boundary"]
            and "valid_for_D4_outer_regulator_zero_limit" in result["claim_boundary"]
            and all(not key.startswith("valid_for_D2_") for key in result["claim_boundary"])
            and all(not key.startswith("valid_for_D2_") for key in finite[0]),
            fixed_claim,
        ),
        validation_gate(
            "saved_node_counts_and_shards_are_consistent",
            len(manifest) == int(result["encountered_node_count"])
            and len(completed_manifest) == int(result["completed_node_count"])
            and len(shard_results) == int(result["completed_node_count"])
            and all(
                row.get("decision") == "NODE_POLE_SUBTRACTED_ENERGY_INTEGRAL_ACCEPTED"
                for row in shard_results
            )
            and int(result["failed_inner_node_count"]) == 0,
            (
                f"encountered={len(manifest)};completed={len(completed_manifest)};"
                f"shards={len(shard_results)}"
            ),
        ),
        validation_gate(
            "status_matches_canonical_saved_result",
            status.get("decision") == result.get("decision")
            and status.get("decay_node_id") == DECAY_NODE_ID
            and status.get("epsilon_id") == M5326.EPSILON_ID
            and int(status.get("completed_node_count", -1))
            == int(result["completed_node_count"])
            and int(status.get("encountered_node_count", -1))
            == int(result["encountered_node_count"]),
            status.get("state", ""),
        ),
        validation_gate(
            "incomplete_rung_keeps_all_physics_claims_false",
            not incomplete
            or (
                not bool(result["claim_boundary"][fixed_claim])
                and not bool(result["claim_boundary"]["valid_for_D4_outer_regulator_zero_limit"])
                and all(not bool(result["claim_boundary"][field]) for field in CLAIM_FIELDS)
            ),
            f"completed_full_run={not incomplete}",
        ),
        validation_gate(
            "source_paths_and_hashes_current",
            sources_current
            and any(Path(row["path"]).resolve() == Path(__file__).resolve() for row in result["source_files"]),
            f"rows={len(result['source_files'])}",
        ),
        validation_gate(
            "formal_workbench_unchanged",
            M5283.formal_inventory_digest()
            == result["formalization_workbench_end_digest"]
            == result["formalization_workbench_reference_digest"]
            == FORMAL_DIGEST
            and int(result["formalization_workbench_modified_file_count"]) == 0,
            result["formalization_workbench_end_digest"],
        ),
        validation_gate(
            "scripts_cache_absent",
            not (SCRIPTS / "__pycache__").exists(),
            str(SCRIPTS / "__pycache__"),
        ),
    ]
    passed = all(parse_bool(row["passed"]) for row in gates)
    write_csv(paths["semantic_validation"], gates, ["gate"])
    write_csv(paths["semantic_residual_validation"], gates, ["gate"])
    return {
        "checkpoint": CHECKPOINT,
        "mode": f"D4-outer-{M5326.EPSILON_ID}-semantic-canonicalization",
        "epsilon_id": M5326.EPSILON_ID,
        "acceptance_passed": passed,
        "decision": (
            f"D4_OUTER_{M5326.EPSILON_ID}_SEMANTIC_ARTIFACTS_CANONICALIZED"
            if passed
            else f"D4_OUTER_{M5326.EPSILON_ID}_SEMANTIC_CANONICALIZATION_FAILED"
        ),
        "runtime_seconds": time.perf_counter() - started,
    }


def canonicalize_saved_refinement() -> dict[str, Any]:
    if not M5326.RESULT.exists():
        raise FileNotFoundError(M5326.RESULT)
    result = canonicalize_refinement_result(read_json(M5326.RESULT))
    return validate_refinement_semantics(result)


def render_d4_refinement_document(result: dict[str, Any], passed: bool) -> None:
    lines = [
        f"# 5334 - D4 outer {M5326.EPSILON_ID} event-aligned refinement",
        "",
        "## Purpose",
        "",
        "Evaluate the independently derived D4_OUTER finite-regulator rung using",
        "the source-derived support-event partition and paired Q4/Q8 adaptivity.",
        "No D2 owner-channel certificate or D2 result is transferred.",
        "",
        "## Saved result",
        "",
        f"- support events: `{result['support_event_count']}`;",
        f"- encountered nodes: `{result['encountered_node_count']}`;",
        f"- completed nodes: `{result['completed_node_count']}`;",
        f"- failed inner nodes: `{result['failed_inner_node_count']}`;",
        f"- adaptive panels/leaves: `{result['adaptive_panel_count']}/{result['adaptive_leaf_count']}`;",
        f"- completed full run: `{result['completed_full_run']}`;",
        f"- finite-rung acceptance: `{result['acceptance_passed']}`;",
        f"- decision: `{result['decision']}`;",
        f"- full-rung validation: `{'PASS' if passed else 'INCOMPLETE'}`.",
        "",
        "## Claim boundary",
        "",
        "All decay-angle, regulator-zero, phase-space, UV, local-GR and full-MTS",
        "claims remain false until this saved rung completes and passes its numerical",
        "error budget. The resumable calculation does not restart completed shards.",
        "",
        "## Resume command",
        "",
        "```powershell",
        ".\\.venv-score\\Scripts\\python.exe "
        ".\\scripts\\Y5_R2FR_5334_D4_outer_regulator_ladder_controller.py "
        "--mode refinement-run --max-runtime-hours 2",
        "```",
    ]
    M5326.DOCUMENT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def validate_refinement_outputs() -> dict[str, Any]:
    started = time.perf_counter()
    result = canonicalize_refinement_result(read_json(M5326.RESULT))
    semantic = validate_refinement_semantics(result)
    dry = read_json(M5326.DRY_RUN)
    events = read_csv(M5326.EVENTS)
    manifest = read_csv(M5326.NODE_MANIFEST)
    panels = read_csv(M5326.ADAPTIVE_PANELS)
    finite = read_csv(M5326.FINITE_VALUE)
    leaves = [row for row in panels if parse_bool(row["adaptive_leaf"])]
    fixed_claim = d4_fixed_decay_claim_field()
    source_current = all(
        Path(row["path"]).exists()
        and digest(Path(row["path"])) == row["sha256"]
        for row in result["source_files"]
    )
    gates = [
        validation_gate(
            "D4_outer_semantic_canonicalization_passes",
            bool(semantic["acceptance_passed"]),
            semantic["decision"],
        ),
        validation_gate(
            "source_derived_support_events_resolved",
            bool(dry["acceptance_passed"])
            and len(events) == int(result["support_event_count"])
            and all(parse_bool(row["event_contract_passes"]) for row in events),
            f"events={len(events)}",
        ),
        validation_gate(
            "all_encountered_D4_outer_nodes_complete_and_pass",
            bool(manifest)
            and all(row["shard_state"] == "COMPLETE_PASS" for row in manifest)
            and int(result["failed_inner_node_count"]) == 0,
            f"nodes={len(manifest)};complete={result['completed_node_count']}",
        ),
        validation_gate(
            "all_D4_outer_adaptive_leaves_pass",
            bool(leaves)
            and all(parse_bool(row["adaptive_gate_passes"]) for row in leaves)
            and bool(result["all_adaptive_leaf_gates_pass"]),
            f"leaves={len(leaves)}",
        ),
        validation_gate(
            f"D4_outer_{M5326.EPSILON_ID}_conservative_budget_passes",
            len(finite) == 1
            and parse_bool(finite[0]["finite_regulator_fixed_decay_integral_accepted"])
            and float(finite[0]["total_error_relative_conservative"])
            <= M5326.GLOBAL_ERROR_BUDGET_LIMIT
            and bool(result["acceptance_passed"])
            and bool(result["claim_boundary"][fixed_claim]),
            str(result["total_error_relative_conservative"]),
        ),
        validation_gate(
            "formal_workbench_unchanged",
            M5283.formal_inventory_digest()
            == result["formalization_workbench_end_digest"]
            == result["formalization_workbench_reference_digest"]
            == FORMAL_DIGEST
            and int(result["formalization_workbench_modified_file_count"]) == 0,
            result["formalization_workbench_end_digest"],
        ),
        validation_gate(
            "source_paths_and_hashes_current",
            source_current,
            f"rows={len(result['source_files'])}",
        ),
        validation_gate(
            "scripts_cache_absent",
            not (SCRIPTS / "__pycache__").exists(),
            str(SCRIPTS / "__pycache__"),
        ),
        validation_gate(
            "broader_claims_locked_false",
            not bool(result["claim_boundary"]["valid_for_D4_outer_regulator_zero_limit"])
            and all(not bool(result["claim_boundary"][field]) for field in CLAIM_FIELDS),
            "regulator-zero, angular and broader claims remain separate",
        ),
    ]
    passed = all(parse_bool(row["passed"]) for row in gates)
    write_csv(M5326.VALIDATION, gates, ["gate"])
    write_csv(M5326.RESIDUAL_VALIDATION, gates, ["gate"])
    render_d4_refinement_document(result, passed)
    return {
        "checkpoint": CHECKPOINT,
        "mode": f"D4-outer-{M5326.EPSILON_ID}-refinement-validation",
        "epsilon_id": M5326.EPSILON_ID,
        "acceptance_passed": passed,
        "decision": (
            f"VALIDATED_D4_OUTER_EVENT_ALIGNED_{M5326.EPSILON_ID}_REFINEMENT"
            if passed
            else f"D4_OUTER_EVENT_ALIGNED_{M5326.EPSILON_ID}_REFINEMENT_INCOMPLETE"
        ),
        "runtime_seconds": time.perf_counter() - started,
    }


def canonical_finite_row(
    epsilon_id: str,
    finite_path: Path,
    result_path: Path,
    validation_path: Path,
) -> dict[str, Any] | None:
    row = M5327.finite_row(epsilon_id, finite_path, result_path, validation_path)
    if row is None:
        return None
    row["decay_node_id"] = DECAY_NODE_ID
    row.pop("valid_for_D2_regulator_zero_fit_input", None)
    row["valid_for_D4_outer_regulator_zero_fit_input"] = True
    return row


def collect_ladder() -> dict[str, Any]:
    started = time.perf_counter()
    configure_ladder()
    SOURCE.mkdir(parents=True, exist_ok=True)
    rows: list[dict[str, Any]] = []
    base = refinement_paths("E0025")
    inherited = canonical_finite_row(
        "E0025", base["finite"], base["result"], base["validation"]
    )
    if inherited is not None:
        rows.append(inherited)
    for epsilon_id in M5327.RUN_IDS:
        paths = refinement_paths(epsilon_id)
        row = canonical_finite_row(
            epsilon_id, paths["finite"], paths["result"], paths["validation"]
        )
        if row is not None:
            rows.append(row)
    rows.sort(key=lambda row: float(row["epsilon"]))
    write_csv(LADDER, rows, ["decay_node_id", "epsilon_id"])
    pairwise = M5327.pairwise_convergence_rows(rows)
    for row in pairwise:
        row.pop("valid_for_D2_regulator_zero_fit_input_pair", None)
        row["valid_for_D4_outer_regulator_zero_fit_input_pair"] = True
    if pairwise:
        write_csv(PAIRWISE, pairwise, ["lower_epsilon_id", "upper_epsilon_id"])
    trends = M5327.three_point_trend_rows(rows)
    if trends:
        write_csv(
            TRENDS,
            trends,
            ["lower_epsilon_id", "middle_epsilon_id", "upper_epsilon_id"],
        )
    completed_ids = tuple(row["epsilon_id"] for row in rows)
    missing_ids = tuple(
        epsilon_id
        for epsilon_id in M5327.EXPECTED_IDS
        if epsilon_id not in completed_ids
    )
    complete = not missing_ids
    source_paths = {
        Path(__file__).resolve(),
        SCRIPT_5327,
        SCRIPT_5324,
        RESULT_5324,
        VALIDATION_5324,
        TOPOLOGY_EVENTS_5324,
        TOPOLOGY_PANELS_5324,
        TOPOLOGY_SUMMARY_5324,
        MEASURE_5324,
        LADDER,
    }
    if pairwise:
        source_paths.add(PAIRWISE)
    if trends:
        source_paths.add(TRENDS)
    for row in rows:
        source_paths.update(
            {
                Path(row["finite_source_path"]),
                Path(row["result_source_path"]),
                Path(row["validation_source_path"]),
            }
        )
    formal_end = M5283.formal_inventory_digest()
    result = {
        "checkpoint": CHECKPOINT,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "marker": "MTS_5334_D4_OUTER_REGULATOR_LADDER_CONTROLLER",
        "revision": "D4-outer-regulator-ladder-controller-v1",
        "mode": "D4-outer-regulator-ladder-controller",
        "acceptance_passed": complete,
        "checkpoint_execution_passed": True,
        "decision": (
            "D4_OUTER_SEVEN_POINT_FINITE_REGULATOR_LADDER_COMPLETE__FIT_ZERO_LIMIT"
            if complete
            else "D4_OUTER_REGULATOR_LADDER_PARTIAL__RUN_MISSING_EPSILONS"
        ),
        "decay_node_id": DECAY_NODE_ID,
        "absolute_decay_cosine": ABSOLUTE_DECAY_COSINE,
        "completed_regulator_count": len(rows),
        "expected_regulator_count": len(M5327.EXPECTED_IDS),
        "completed_regulator_ids": list(completed_ids),
        "missing_regulator_ids": list(missing_ids),
        "adjacent_regulator_pair_count": len(pairwise),
        "three_point_trend_count": len(trends),
        "formalization_workbench_reference_digest": FORMAL_DIGEST,
        "formalization_workbench_end_digest": formal_end,
        "formalization_workbench_modified_file_count": 0
        if formal_end == FORMAL_DIGEST
        else -1,
        "D2_owner_channel_certificate_transferred": False,
        "claim_boundary": {
            **{field: False for field in CLAIM_FIELDS},
            "reason": (
                "Finite D4_OUTER regulator rows are inputs only. No angular result "
                "is allowed until a separately validated regulator-zero fit exists."
            ),
        },
        "source_files": [
            {"path": str(path), "sha256": digest(path)}
            for path in sorted(source_paths, key=str)
        ],
        "runtime_seconds": time.perf_counter() - started,
    }
    atomic_json(RESULT, result)
    atomic_json(
        STATUS,
        {
            "checkpoint": CHECKPOINT,
            "state": "COMPLETE_INPUT_LADDER" if complete else "PARTIAL_RESUMABLE",
            "completed_regulator_count": len(rows),
            "missing_regulator_ids": list(missing_ids),
            "decision": result["decision"],
        },
    )
    render_document(result)
    return result


def validate_ladder() -> dict[str, Any]:
    started = time.perf_counter()
    configure_ladder()
    result = read_json(RESULT)
    rows = read_csv(LADDER)
    pairwise = read_csv(PAIRWISE) if PAIRWISE.exists() else []
    trends = read_csv(TRENDS) if TRENDS.exists() else []
    ids = tuple(row["epsilon_id"] for row in rows)
    expected_subset = tuple(
        epsilon_id for epsilon_id in M5327.EXPECTED_IDS if epsilon_id in set(ids)
    )
    sources_current = all(
        Path(row["path"]).exists()
        and digest(Path(row["path"])) == row["sha256"]
        for row in result["source_files"]
    )
    gates = [
        validation_gate(
            "all_collected_D4_outer_rows_numeric_and_accepted",
            all(
                float(row["epsilon"]) > 0.0
                and math.isfinite(float(row["fixed_decay_integral_real"]))
                and math.isfinite(float(row["fixed_decay_integral_imaginary"]))
                and 0.0 < float(row["fixed_decay_error_relative_conservative"])
                <= M5327.GLOBAL_ERROR_BUDGET_LIMIT
                and parse_bool(row["finite_regulator_fixed_decay_integral_accepted"])
                and parse_bool(row["valid_for_D4_outer_regulator_zero_fit_input"])
                for row in rows
            ),
            f"rows={len(rows)}",
        ),
        validation_gate(
            "collected_ids_are_ordered_expected_subset",
            ids == expected_subset,
            "|".join(ids),
        ),
        validation_gate(
            "adjacent_pair_rows_are_complete_and_nonclaim",
            len(pairwise) == max(len(rows) - 1, 0)
            and all(
                parse_bool(row["valid_for_D4_outer_regulator_zero_fit_input_pair"])
                and all(not parse_bool(row[field]) for field in M5327.CLAIM_FIELDS)
                for row in pairwise
            ),
            f"pairs={len(pairwise)}",
        ),
        validation_gate(
            "three_point_rows_are_complete_and_preliminary",
            len(trends) == max(len(rows) - 2, 0)
            and all(
                parse_bool(row["valid_for_preliminary_regulator_trend_diagnostic"])
                and all(not parse_bool(row[field]) for field in M5327.CLAIM_FIELDS)
                for row in trends
            ),
            f"trends={len(trends)}",
        ),
        validation_gate(
            "D2_owner_channel_certificate_not_transferred",
            not bool(result["D2_owner_channel_certificate_transferred"]),
            "different decay node requires independently derived pole certificates",
        ),
        validation_gate(
            "source_paths_and_hashes_current",
            sources_current,
            f"rows={len(result['source_files'])}",
        ),
        validation_gate(
            "formal_workbench_unchanged",
            M5283.formal_inventory_digest()
            == result["formalization_workbench_end_digest"]
            == result["formalization_workbench_reference_digest"]
            == FORMAL_DIGEST
            and int(result["formalization_workbench_modified_file_count"]) == 0,
            result["formalization_workbench_end_digest"],
        ),
        validation_gate(
            "broader_claims_locked_false",
            all(not bool(result["claim_boundary"][field]) for field in CLAIM_FIELDS),
            "regulator-zero and angular gates remain separate",
        ),
        validation_gate(
            "scripts_cache_absent",
            not (SCRIPTS / "__pycache__").exists(),
            str(SCRIPTS / "__pycache__"),
        ),
    ]
    passed = all(parse_bool(row["passed"]) for row in gates)
    write_csv(VALIDATION, gates, ["gate"])
    write_csv(RESIDUAL_VALIDATION, gates, ["gate"])
    return {
        "checkpoint": CHECKPOINT,
        "mode": "validation",
        "acceptance_passed": passed,
        "decision": (
            "VALIDATED_D4_OUTER_REGULATOR_LADDER_CONTROLLER"
            if passed
            else "D4_OUTER_REGULATOR_LADDER_CONTROLLER_VALIDATION_FAILED"
        ),
        "runtime_seconds": time.perf_counter() - started,
    }


def render_document(result: dict[str, Any]) -> None:
    lines = [
        "# 5334 — D4 outer regulator ladder controller",
        "",
        "## Purpose",
        "",
        "Evaluate the missing `D4_OUTER` paired Gauss-Legendre decay node at",
        "seven finite regulators using the source-complete 5324 topology contract",
        "and the already validated adaptive fixed-decay engine.",
        "",
        "## Current state",
        "",
        f"- Decision: `{result['decision']}`",
        f"- Completed regulators: `{result['completed_regulator_count']}/{result['expected_regulator_count']}`",
        f"- Missing: `{'|'.join(result['missing_regulator_ids']) or 'none'}`",
        "- The `D2` E040 owner-channel certificate is deliberately not transferred.",
        "- All decay-angle, phase-space, UV, and local-GR claims remain false.",
        "",
        "## Next gate",
        "",
        "Complete any missing finite rungs, fit the independent D4_OUTER regulator-zero",
        "limit, and only then compare paired GL2 against paired GL4 plus the separately",
        "bounded 0.5% endpoint cap.",
    ]
    DOCUMENT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=(
            "smoke-dry-run",
            "smoke-run",
            "smoke-validate",
            "adaptive-event-audit",
            "adaptive-event-evidence",
            "adaptive-event-promote",
            "refinement-dry-run",
            "refinement-run",
            "refinement-repair",
            "refinement-canonicalize",
            "refinement-validate",
            "target-dry-run",
            "target-run",
            "target-repair",
            "target-validate",
            "collect",
            "validate",
        ),
        required=True,
    )
    parser.add_argument("--epsilon-id", choices=M5327.RUN_IDS)
    parser.add_argument("--max-runtime-hours", type=float, default=2.0)
    return parser.parse_args()


def main() -> int:
    arguments = parse_args()
    M5312.set_below_normal_priority()
    runtime_seconds = max(arguments.max_runtime_hours, 0.0) * 3600.0
    if arguments.mode == "adaptive-event-audit":
        configure_refinement("E0025")
        result = adaptive_event_audit()
    elif arguments.mode == "adaptive-event-evidence":
        configure_refinement("E0025")
        result = refresh_adaptive_event_root_evidence()
    elif arguments.mode == "adaptive-event-promote":
        configure_refinement("E0025")
        result = promote_adaptive_event_extension()
    elif arguments.mode.startswith("smoke-"):
        configure_smoke()
        if arguments.mode == "smoke-dry-run":
            result = M5325.dry_run()
        elif arguments.mode == "smoke-run":
            result = canonicalize_smoke_result(M5325.execute(runtime_seconds))
        else:
            result = canonicalize_smoke_validation(M5325.validate_outputs())
    elif arguments.mode.startswith("refinement-"):
        configure_refinement("E0025")
        if arguments.mode == "refinement-dry-run":
            result = d4_refinement_dry_run()
        elif arguments.mode == "refinement-run":
            result = canonicalize_refinement_result(M5326.execute(runtime_seconds))
        elif arguments.mode == "refinement-repair":
            result = M5326.repair_failed_nodes()
        elif arguments.mode == "refinement-canonicalize":
            result = canonicalize_saved_refinement()
        else:
            result = validate_refinement_outputs()
    elif arguments.mode.startswith("target-"):
        if arguments.epsilon_id is None:
            raise RuntimeError("--epsilon-id is required for target modes")
        configure_ladder()
        configure_D4_target(arguments.epsilon_id)
        if arguments.mode == "target-dry-run":
            result = d4_refinement_dry_run()
        elif arguments.mode == "target-run":
            result = canonicalize_refinement_result(M5326.execute(runtime_seconds))
        elif arguments.mode == "target-repair":
            result = M5326.repair_failed_nodes()
        else:
            result = M5326.validate_outputs()
    elif arguments.mode == "collect":
        result = collect_ladder()
    else:
        result = validate_ladder()
    summary = {
        "checkpoint": CHECKPOINT,
        "mode": result["mode"],
        "epsilon_id": result.get("epsilon_id"),
        "acceptance_passed": bool(result["acceptance_passed"]),
        "decision": result["decision"],
        "runtime_seconds": result.get("runtime_seconds"),
    }
    print(json.dumps(summary, sort_keys=True))
    return 0 if bool(result["acceptance_passed"]) else 1


if __name__ == "__main__":
    raise SystemExit(main())
