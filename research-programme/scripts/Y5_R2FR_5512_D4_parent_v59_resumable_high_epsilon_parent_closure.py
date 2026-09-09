from __future__ import annotations

import argparse
import importlib.util
import json
import math
import time
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


POST = Path(__file__).resolve().parents[1]
SCRIPTS = POST / "scripts"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
OUTPUT = FUNCTIONAL_RG / "5512"
WORK = OUTPUT / "work-v1"

SCRIPT_5511 = SCRIPTS / "Y5_R2FR_5511_D4_parent_v59_resumable_high_x_parent_closure.py"
SOURCE_STATE = FUNCTIONAL_RG / "5511" / "work-v1" / "E07__U051__RIGHT_CONNECTOR__CUBOID__6df3d70a73e4618b.json"
RESULT_5511 = FUNCTIONAL_RG / "5511" / "D4_parent_v59_resumable_high_x_parent_closure_result.json"
VALIDATION_5511 = FUNCTIONAL_RG / "5511" / "P8_Y5_BRR5510_5511_VALIDATION.csv"
SOURCE_REGISTER_5511 = FUNCTIONAL_RG / "5511" / "source_register.csv"
NODE_AUDIT_5511 = FUNCTIONAL_RG / "5511" / "D4_parent_v59_high_x_frontier_node_audit.csv"
UNION_AUDIT_5511 = FUNCTIONAL_RG / "5511" / "D4_parent_v59_low_epsilon_parent_union_audit.csv"
V59_AUDIT_5511 = FUNCTIONAL_RG / "5511" / "D4_parent_v59_high_x_frontier_adaptive_xt_audit.csv"

TARGET_CUBOID_ID = "E07__U051__RIGHT_CONNECTOR__CUBOID__6df3d70a73e4618b"
STATE = WORK / f"{TARGET_CUBOID_ID}.json"
NODE_AUDIT = OUTPUT / "D4_parent_v59_high_epsilon_frontier_node_audit.csv"
UNION_AUDIT = OUTPUT / "D4_parent_v59_epsilon_pair_parent_union_audit.csv"
V59_AUDIT = OUTPUT / "D4_parent_v59_high_epsilon_frontier_adaptive_xt_audit.csv"
V58_AUDIT = OUTPUT / "D4_parent_v59_high_epsilon_frontier_v58_certificate_application_audit.csv"
V57_AUDIT = OUTPUT / "D4_parent_v59_high_epsilon_frontier_v57_scoped_certificate_audit.csv"
JACOBIAN_XT_AUDIT = OUTPUT / "D4_parent_v59_high_epsilon_frontier_collision_jacobian_xt_audit.csv"
STABLE_XT_AUDIT = OUTPUT / "D4_parent_v59_high_epsilon_frontier_stable_edge_xt_audit.csv"
PIVOT_AUDIT = OUTPUT / "D4_parent_v59_high_epsilon_frontier_first_spinor_pivot_audit.csv"
STABLE_T_AUDIT = OUTPUT / "D4_parent_v59_high_epsilon_frontier_stable_edge_t_audit.csv"
JACOBIAN_T_AUDIT = OUTPUT / "D4_parent_v59_high_epsilon_frontier_collision_jacobian_t_audit.csv"
SOURCE_REGISTER = OUTPUT / "source_register.csv"
VALIDATION = OUTPUT / "P8_Y5_BRR5511_5512_VALIDATION.csv"
STATUS = OUTPUT / "status.json"
RESULT = OUTPUT / "D4_parent_v59_resumable_high_epsilon_parent_closure_result.json"
DOCUMENT = POST / "5512-Y5-R2FR-D4-parent-v59-resumable-high-epsilon-parent-closure.md"

CHECKPOINT = 5512
REVISION = "D4-parent-v59-resumable-high-epsilon-parent-closure-v1"
PARENT_V59_REVISION = "D4-deformed-contour-regular-away-W3-v59-proof-carrying-adaptive-xt-cover"
EXPECTED_PATH = "R_E0S_E1S_E1S"
EXPECTED_SOURCE_COUNTS = (190, 2, 0)
EXPECTED_SOURCE_WITNESSES = 69
EXPECTED_SOURCE_V59_AUDIT_ROWS = 34
EXPECTED_PENDING_PATHS = (
    "R_E1S",
    EXPECTED_PATH,
)

EPSILON_PAIR_PARENT_PATH = "R_E0S_E1S"
HIGH_EPSILON_PREFIX = EXPECTED_PATH
LOW_EPSILON_LEAF_PATHS = {
    "R_E0S_E1S_E0S_X0S_X0S_T0S_X0S",
    "R_E0S_E1S_E0S_X0S_X0S_T0S_X1S",
    "R_E0S_E1S_E0S_X0S_X0S_T1S",
    "R_E0S_E1S_E0S_X0S_X1S",
    "R_E0S_E1S_E0S_X1S",
}

EXPECTED_SCRIPT_5511_SHA256 = "fdf8c5adfbe0c86c2edb0ed770cf310928db10fa54dd32dd3376e726b59d1718"
EXPECTED_SOURCE_STATE_SHA256 = "3223adbc9dbeb2d5445fffca0d8a78f086ddb345a2226534187f2835acf9d213"
EXPECTED_RESULT_5511_SHA256 = "21a995327376d7fdcf47784616244590486033afc0852e2afce4c3e3fd681b7f"
EXPECTED_VALIDATION_5511_SHA256 = "b1bac53870a518254d50f65ebf40c0c84b3663c55739f2e91d56cf71c608fc93"
EXPECTED_SOURCE_REGISTER_5511_SHA256 = "3cab37261d9fa3ff735d98e0c14e99414298453f9e2d7e7b8c2a6a801209f441"
EXPECTED_NODE_AUDIT_5511_SHA256 = "22c29129dfe614f7fa26ec2ff324683dde626bfa633c5a608a0c8133fe560573"
EXPECTED_UNION_AUDIT_5511_SHA256 = "2cd70b906d0c57ebb636901cb98067d9a44bc76d37ea3924e46102a24d612595"
EXPECTED_V59_AUDIT_5511_SHA256 = "ddf1f910d6d4a6bb931a755e910e90bad832cf4fa4e663cb186c26e3ff16dd8c"

AUDIT_BINDINGS = (
    ("v59_adaptive_xt_audit_rows", "V59_ADAPTIVE_XT_AUDIT_ROWS", V59_AUDIT),
    ("v58_certificate_application_audit_rows", "V58_ADAPTIVE_CERTIFICATE_AUDIT_ROWS", V58_AUDIT),
    ("v57_scoped_certificate_audit_rows", "V57_SCOPED_CERTIFICATE_AUDIT_ROWS", V57_AUDIT),
    ("v56_collision_jacobian_xt_audit_rows", "V56_COLLISION_JACOBIAN_XT_LEAF_UNION_AUDIT_ROWS", JACOBIAN_XT_AUDIT),
    ("v56_stable_edge_xt_audit_rows", "V55_STABLE_EDGE_XT_LEAF_UNION_AUDIT_ROWS", STABLE_XT_AUDIT),
    ("v56_first_spinor_pivot_audit_rows", "V54_FIRST_SPINOR_PIVOT_T_LEAF_UNION_AUDIT_ROWS", PIVOT_AUDIT),
    ("v56_stable_edge_t_audit_rows", "V53_STABLE_EDGE_T_LEAF_UNION_AUDIT_ROWS", STABLE_T_AUDIT),
    ("v56_collision_jacobian_t_audit_rows", "V52_COLLISION_JACOBIAN_LEAF_UNION_AUDIT_ROWS", JACOBIAN_T_AUDIT),
)


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise ImportError(f"cannot load {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def check(gate: str, passed: bool, evidence: Any) -> dict[str, Any]:
    return {
        "checkpoint": CHECKPOINT,
        "validation_gate": gate,
        "passed": bool(passed),
        "evidence": evidence,
    }


def carry_forward(base_5499: Any, source: dict[str, Any]) -> dict[str, Any]:
    state = deepcopy(source)
    state["checkpoint"] = CHECKPOINT
    state["revision"] = REVISION
    state["parent_revision"] = PARENT_V59_REVISION
    state["checkpoint_5512"] = {
        "source_state_path": str(SOURCE_STATE),
        "source_state_sha256": EXPECTED_SOURCE_STATE_SHA256,
        "source_accepted_sha256": base_5499.canonical_digest(source["accepted"]),
        "source_pending_sha256": base_5499.canonical_digest(source["stack"]),
        "source_unresolved_sha256": base_5499.canonical_digest(source["unresolved"]),
        "source_refinement_witnesses_sha256": base_5499.canonical_digest(source["refinement_witnesses"]),
        "source_v59_audit_sha256": base_5499.canonical_digest(source.get("v59_adaptive_xt_audit_rows", [])),
        "records": [],
        "created_utc": datetime.now(timezone.utc).isoformat(),
    }
    for key, _, _ in AUDIT_BINDINGS:
        state.setdefault(key, [])
    state["processed_this_run"] = 0
    state["decision"] = "PARENT_V59_FRONTIER_PARTIAL__RESUME"
    for field in (
        "valid_for_parent_v59_active_cuboid",
        "valid_for_full_outer_parent_leaf_enclosure",
        "valid_for_D4_event_local_W3_bound",
        "valid_for_all_operator_local_GR_claim",
        "valid_for_full_MTS_claim",
    ):
        state[field] = False
    return state


def process_atomic_node(
    base_5499: Any,
    base_5498: Any,
    base_5467: Any,
    base_5468: Any,
    base_5469: Any,
    stable: Any,
    parent_v59: Any,
    cells: dict[str, Any],
    support_segments: list[dict[str, Any]],
    branches: dict[str, Any],
    cuboid: dict[str, Any],
    state: dict[str, Any],
    maximum_refinement_depth: int,
) -> dict[str, Any]:
    node = deepcopy(state["stack"][-1])
    records = state["checkpoint_5512"]["records"]
    if not records and node["refinement_path"] != EXPECTED_PATH:
        raise RuntimeError(f"unexpected checkpoint-5512 first node {node['refinement_path']}")
    counts_before = {
        "accepted": len(state["accepted"]),
        "pending": len(state["stack"]),
        "unresolved": len(state["unresolved"]),
        "witnesses": len(state["refinement_witnesses"]),
    }
    audit_starts = {
        key: len(getattr(parent_v59, attribute, []))
        for key, attribute, _ in AUDIT_BINDINGS
    }
    started = time.perf_counter()
    result = base_5469.evaluate_node(
        base_5468,
        stable,
        parent_v59,
        cells,
        support_segments,
        branches,
        cuboid,
        node,
    )
    runtime = time.perf_counter() - started
    compact = base_5469.compact_node_result(node, result)
    compact["certificate_source"] = "checkpoint_5512_parent_v59"
    compact["parent_revision"] = PARENT_V59_REVISION
    state["stack"].pop()
    state["node_evaluation_count"] = int(state["node_evaluation_count"]) + 1
    children: list[dict[str, Any]] = []
    if base_5499.truth(result.get("probe_passed")):
        outcome = "ACCEPTED"
        state["accepted"].append(compact)
    else:
        state["refinement_witnesses"].append(compact)
        if int(node["refinement_depth"]) >= maximum_refinement_depth:
            outcome = "UNRESOLVED_DEPTH_LIMIT"
            state["unresolved"].append(compact)
        else:
            choice = base_5469.split_choice(node, state)
            if choice is None:
                outcome = "UNRESOLVED_NO_SPLIT"
                state["unresolved"].append(compact)
            else:
                axis, split, source_boundary = choice
                lower_child, upper_child = base_5469.split_node(
                    node,
                    axis,
                    split,
                    source_boundary,
                )
                state["stack"].append(upper_child)
                state["stack"].append(lower_child)
                state["split_axis_counts"][axis] = int(state["split_axis_counts"][axis]) + 1
                children = [lower_child, upper_child]
                outcome = f"REFINED_{str(axis).upper()}2"
    new_audits: dict[str, int] = {}
    for key, attribute, _ in AUDIT_BINDINGS:
        rows = list(getattr(parent_v59, attribute, []))[audit_starts[key] :]
        state.setdefault(key, []).extend(rows)
        new_audits[key] = len(rows)
    new_v59_count = new_audits["v59_adaptive_xt_audit_rows"]
    new_v59_rows = (
        state["v59_adaptive_xt_audit_rows"][-new_v59_count:]
        if new_v59_count
        else []
    )
    state["v59_node_evaluation_count"] = int(state.get("v59_node_evaluation_count", 0)) + 1
    state["v59_accepted_subcuboid_count"] = int(state.get("v59_accepted_subcuboid_count", 0)) + (
        1 if outcome == "ACCEPTED" else 0
    )
    state["v59_refinement_witness_count"] = int(state.get("v59_refinement_witness_count", 0)) + (
        0 if outcome == "ACCEPTED" else 1
    )
    state["v59_adaptive_application_count"] = int(state.get("v59_adaptive_application_count", 0)) + sum(
        row.get("event") == "TRIGGER" for row in new_v59_rows
    )
    state["runtime_seconds"] = float(state.get("runtime_seconds", 0.0)) + runtime
    state["accepted_subcuboid_count"] = len(state["accepted"])
    state["pending_subcuboid_count"] = len(state["stack"])
    state["unresolved_subcuboid_count"] = len(state["unresolved"])
    state["accepted_volume"] = math.fsum(base_5469.node_volume(row) for row in state["accepted"])
    partition_error = abs(
        base_5498.exact_partition_volume(state)
        - base_5498.exact_node_volume(state["root"])
    )
    if partition_error != 0:
        raise RuntimeError("checkpoint-5512 atomic node broke the exact partition")
    counts_after = {
        "accepted": len(state["accepted"]),
        "pending": len(state["stack"]),
        "unresolved": len(state["unresolved"]),
        "witnesses": len(state["refinement_witnesses"]),
    }
    record = {
        "ordinal": len(records),
        "refinement_path": node["refinement_path"],
        "epsilon_real_lower": node["epsilon_real_lower"],
        "epsilon_real_upper": node["epsilon_real_upper"],
        "x_lower": node["x_lower"],
        "x_upper": node["x_upper"],
        "t_lower": node["t_lower"],
        "t_upper": node["t_upper"],
        "outcome": outcome,
        "probe_passed": base_5499.truth(result.get("probe_passed")),
        "failure_type": result.get("failure_type", ""),
        "failure_message": result.get("failure_message", ""),
        "child_paths": [str(row["refinement_path"]) for row in children],
        "counts_before": counts_before,
        "counts_after": counts_after,
        "runtime_seconds": runtime,
        "new_audit_counts": new_audits,
        "created_utc": datetime.now(timezone.utc).isoformat(),
    }
    records.append(record)
    state["processed_this_run"] = len(records)
    state["coverage_error"] = 0.0
    state["decision"] = "PARENT_V59_FRONTIER_PARTIAL__RESUME"
    state["last_update_utc"] = record["created_utc"]
    base_5467.atomic_json(STATE, state, compact=True)
    return state


def empty_v59_audit() -> list[dict[str, Any]]:
    return [{
        "checkpoint": CHECKPOINT,
        "call_id": 0,
        "event": "NO_EVENT",
        "adaptive_depth": 0,
        "outcome": "NO_V59_TRIGGER_OR_TERMINAL_AUDIT",
        "binding_sha256": "",
        "refinement_path": EXPECTED_PATH,
        "x_lower": "",
        "x_upper": "",
        "t_lower": "",
        "t_upper": "",
        "axis": "",
        "split": "",
        "source_boundary": "",
        "failure_type": "",
        "failure_message": "",
        "integrated_regular_path_abs_upper": math.nan,
        "minimum_amplitude_denominator_abs_lower": math.nan,
        "collision_jacobian_abs_lower": math.nan,
        "path_integral_enclosure_method": "",
        "source_state_sha256": "",
    }]


def render_document(payload: dict[str, Any], base_5467: Any) -> None:
    evaluations = [
        f"- `{path}` -> `{outcome}`."
        for path, outcome in zip(payload["evaluated_paths"], payload["node_outcomes"])
    ]
    lines = [
        "# 5512: D4 parent-v59 resumable high-epsilon parent closure",
        "",
        "Checkpoint 5511 is hash locked and a bounded depth-first sequence beginning at the remaining high-epsilon sibling is evaluated under the unchanged proof-carrying parent-v59 chain.",
        "",
        *evaluations,
        "",
        f"Last outcome: `{payload['node_outcome']}`. Checkpoint runtime: `{payload['checkpoint_runtime_seconds']}` seconds. Frontier: `{payload['accepted_subcuboid_count']}/{payload['pending_subcuboid_count']}/{payload['unresolved_subcuboid_count']}`.",
        "",
        f"New v59 triggers/splits/cache hits/live passes/aggregates: `{payload['v59_trigger_count']}/{payload['v59_split_count']}/{payload['v59_cache_hit_count']}/{payload['v59_live_parent_pass_count']}/{payload['v59_aggregate_count']}`.",
        "",
        f"Complete epsilon-pair parent closure: `{payload['exact_epsilon_pair_parent_closure']}` using `{payload['epsilon_pair_parent_leaf_count']}` leaves.",
        "",
        f"**{payload['decision']}**",
        "",
        "Complete active-cuboid, full outer, event-local/combined W3, regulator-limit, all-operator local GR and full MTS claims remain open.",
        "",
    ]
    base_5467.atomic_text(DOCUMENT, "\n".join(lines))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--target-node-evaluations", type=int, default=1)
    parser.add_argument("--max-runtime-seconds", type=float, default=12600.0)
    parser.add_argument("--maximum-refinement-depth", type=int, default=33)
    parser.add_argument("--maximum-adaptive-depth", type=int, default=3)
    arguments = parser.parse_args()
    if arguments.target_node_evaluations < 1 or arguments.target_node_evaluations > 16:
        raise ValueError("target node evaluations must be between one and sixteen")
    if arguments.max_runtime_seconds <= 0:
        raise ValueError("maximum runtime must be positive")

    base_5511 = load_module("mts_5511_for_5512", SCRIPT_5511)
    base_5510 = load_module("mts_5510_for_5512", base_5511.SCRIPT_5510)
    base_5509 = load_module("mts_5509_for_5512", base_5510.SCRIPT_5509)
    base_5508 = load_module("mts_5508_for_5512", base_5509.SCRIPT_5508)
    base_5507 = load_module("mts_5507_for_5512", base_5508.SCRIPT_5507)
    base_5506 = load_module("mts_5506_for_5512", base_5508.SCRIPT_5506)
    base_5505 = load_module("mts_5505_for_5512", base_5506.SCRIPT_5505)
    base_5504 = load_module("mts_5504_for_5512", base_5505.SCRIPT_5504)
    base_5503 = load_module("mts_5503_for_5512", base_5504.SCRIPT_5503)
    base_5502 = load_module("mts_5502_for_5512", base_5503.SCRIPT_5502)
    base_5501 = load_module("mts_5501_for_5512", base_5502.SCRIPT_5501)
    base_5500 = load_module("mts_5500_for_5512", base_5501.SCRIPT_5500)
    base_5499 = load_module("mts_5499_for_5512", base_5500.SCRIPT_5499)
    base_5498 = load_module("mts_5498_for_5512", base_5499.SCRIPT_5498)
    base_5496 = load_module("mts_5496_for_5512", base_5498.SCRIPT_5496)
    base_5495 = load_module("mts_5495_for_5512", base_5496.SCRIPT_5495)
    base_5467 = load_module("mts_5467_for_5512", base_5495.SCRIPT_5467)
    base_5468 = load_module("mts_5468_for_5512", base_5495.SCRIPT_5468)
    base_5469 = load_module("mts_5469_for_5512", base_5495.SCRIPT_5469)
    base_5472 = load_module("mts_5472_for_5512", base_5495.SCRIPT_5472)
    base_5474 = load_module("mts_5474_for_5512", base_5495.SCRIPT_5474)
    base_5476 = load_module("mts_5476_for_5512", base_5495.SCRIPT_5476)
    base_5478 = load_module("mts_5478_for_5512", base_5495.SCRIPT_5478)
    base_5480 = load_module("mts_5480_for_5512", base_5495.SCRIPT_5480)
    base_5483 = load_module("mts_5483_for_5512", base_5495.SCRIPT_5483)
    base_5490 = load_module("mts_5490_for_5512", base_5495.SCRIPT_5490)
    base_5493 = load_module("mts_5493_for_5512", base_5495.SCRIPT_5493)

    base_5467.set_below_normal_priority()
    base_5480.set_single_core_affinity()
    before_formalization = base_5467.formalization_snapshot()
    inherited_hashes = {
        "script_5511": base_5499.digest(SCRIPT_5511),
        "source_state": base_5499.digest(SOURCE_STATE),
        "result_5511": base_5499.digest(RESULT_5511),
        "validation_5511": base_5499.digest(VALIDATION_5511),
        "source_register_5511": base_5499.digest(SOURCE_REGISTER_5511),
        "node_audit_5511": base_5499.digest(NODE_AUDIT_5511),
        "union_audit_5511": base_5499.digest(UNION_AUDIT_5511),
        "v59_audit_5511": base_5499.digest(V59_AUDIT_5511),
    }
    expected_hashes = {
        "script_5511": EXPECTED_SCRIPT_5511_SHA256,
        "source_state": EXPECTED_SOURCE_STATE_SHA256,
        "result_5511": EXPECTED_RESULT_5511_SHA256,
        "validation_5511": EXPECTED_VALIDATION_5511_SHA256,
        "source_register_5511": EXPECTED_SOURCE_REGISTER_5511_SHA256,
        "node_audit_5511": EXPECTED_NODE_AUDIT_5511_SHA256,
        "union_audit_5511": EXPECTED_UNION_AUDIT_5511_SHA256,
        "v59_audit_5511": EXPECTED_V59_AUDIT_5511_SHA256,
    }
    if inherited_hashes != expected_hashes:
        raise RuntimeError("checkpoint-5512 inherited source hash mismatch")

    register_5511 = base_5499.read_csv(SOURCE_REGISTER_5511)
    paths = tuple(dict.fromkeys((
        Path(__file__).resolve(),
        SCRIPT_5511,
        SOURCE_STATE,
        RESULT_5511,
        VALIDATION_5511,
        SOURCE_REGISTER_5511,
        NODE_AUDIT_5511,
        UNION_AUDIT_5511,
        V59_AUDIT_5511,
        *(Path(row["source_path"]) for row in register_5511),
    )))
    missing = [str(path) for path in paths if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"missing sources: {missing}")

    source = base_5499.read_json(SOURCE_STATE)
    result_5511 = base_5499.read_json(RESULT_5511)
    validation_5511 = base_5499.read_csv(VALIDATION_5511)
    source_counts = (
        len(source["accepted"]),
        len(source["stack"]),
        len(source["unresolved"]),
    )
    pending_paths = tuple(str(row["refinement_path"]) for row in source["stack"])
    source_certified = (
        result_5511.get("decision") == "PARENT_V59_COMPLETE_LOW_EPSILON_PARENT_CERTIFIED__RESUME_FRONTIER"
        and result_5511.get("valid_for_parent_v59_high_x_frontier") is True
        and result_5511.get("valid_for_parent_v59_complete_low_epsilon_parent") is True
        and int(result_5511.get("failed_validation_count", -1)) == 0
        and int(result_5511.get("processed_node_evaluations", -1)) == 1
        and all(base_5499.truth(row.get("passed")) for row in validation_5511)
        and base_5499.source_register_is_current(register_5511)
        and source_counts == EXPECTED_SOURCE_COUNTS
        and len(source["refinement_witnesses"]) == EXPECTED_SOURCE_WITNESSES
        and len(source.get("v59_adaptive_xt_audit_rows", [])) == EXPECTED_SOURCE_V59_AUDIT_ROWS
        and pending_paths == EXPECTED_PENDING_PATHS
        and source.get("parent_revision") == PARENT_V59_REVISION
        and len(source.get("checkpoint_5511", {}).get("records", [])) == 1
        and source["checkpoint_5511"]["records"][-1]["outcome"] == "ACCEPTED"
        and base_5498.exact_partition_volume(source) == base_5498.exact_node_volume(source["root"])
    )
    if not source_certified:
        raise RuntimeError("checkpoint-5511 source is not current and certified")

    stable, _, cells, support_segments, branches = base_5467.load_parent()
    cuboid = next(
        row
        for row in base_5499.read_csv(base_5495.MANIFEST_5468)
        if row["cuboid_job_id"] == TARGET_CUBOID_ID
    )
    certificate_5496 = base_5499.read_json(base_5508.CERTIFICATE_5496)
    parent_v58 = base_5498.reconstruct_parent(
        base_5467,
        base_5472,
        base_5474,
        base_5476,
        base_5478,
        base_5483,
        base_5490,
        base_5493,
        base_5495,
        base_5496,
        certificate_5496,
    )
    target_witness = next(
        row
        for row in source["refinement_witnesses"]
        if row.get("refinement_path") == base_5506.TARGET_PATH
    )
    target_arguments = base_5495.target_arguments(
        stable,
        parent_v58,
        cells,
        support_segments,
        branches,
        cuboid,
        target_witness,
    )
    lower_arguments, upper_arguments, split = base_5506.split_arguments(target_arguments, source)
    path_speed = base_5468.full_cell_path_speed_bound(
        parent_v58,
        cells[cuboid["mapped_cell_id"]],
        cuboid["path_segment"],
    )
    proof_cache, cache_rows = base_5506.build_proof_cache(
        base_5495,
        source,
        (lower_arguments, upper_arguments),
        path_speed,
    )
    parent_v59 = base_5506.install_parent_v59(
        parent_v58,
        base_5495,
        source,
        proof_cache,
        arguments.maximum_adaptive_depth,
    )
    parent_reconstructed = (
        parent_v59.REVISION == PARENT_V59_REVISION
        and not parent_v59.V59_PARENT_ACTION_CHANGED
        and parent_v59.V59_ONLY_ENCLOSURE_COMPOSITION_CHANGED
        and len(proof_cache) == 2
        and len(cache_rows) == 2
        and split["coverage_error"] == 0.0
    )

    if arguments.dry_run:
        print(json.dumps({
            "checkpoint": CHECKPOINT,
            "dry_run": True,
            "source_counts": list(source_counts),
            "source_witnesses": len(source["refinement_witnesses"]),
            "source_v59_audit_rows": len(source.get("v59_adaptive_xt_audit_rows", [])),
            "next_path": source["stack"][-1]["refinement_path"],
            "parent_revision": parent_v59.REVISION,
            "proof_cache_binding_count": len(proof_cache),
            "target_node_evaluations": arguments.target_node_evaluations,
            "max_runtime_seconds": arguments.max_runtime_seconds,
            "source_hashes_match": inherited_hashes == expected_hashes,
            "exact_source_partition": True,
            "low_epsilon_leaf_count": len(LOW_EPSILON_LEAF_PATHS),
            "epsilon_pair_parent_witness_count": sum(
                row.get("refinement_path") == EPSILON_PAIR_PARENT_PATH
                for row in source["refinement_witnesses"]
            ),
        }, indent=2))
        return 0

    if STATE.is_file():
        state = base_5499.read_json(STATE)
        if state.get("checkpoint_5512", {}).get("source_state_sha256") != EXPECTED_SOURCE_STATE_SHA256:
            raise RuntimeError("checkpoint-5512 output source mismatch")
    else:
        WORK.mkdir(parents=True, exist_ok=True)
        state = carry_forward(base_5499, source)
        base_5467.atomic_json(STATE, state, compact=True)
    run_started = time.perf_counter()
    while (
        len(state["checkpoint_5512"]["records"]) < arguments.target_node_evaluations
        and state["stack"]
        and not state["unresolved"]
    ):
        if state["checkpoint_5512"]["records"] and time.perf_counter() - run_started >= arguments.max_runtime_seconds:
            break
        state = process_atomic_node(
            base_5499,
            base_5498,
            base_5467,
            base_5468,
            base_5469,
            stable,
            parent_v59,
            cells,
            support_segments,
            branches,
            cuboid,
            state,
            arguments.maximum_refinement_depth,
        )

    records = state["checkpoint_5512"]["records"]
    if not records:
        raise RuntimeError("checkpoint-5512 committed no atomic node")
    record = records[-1]
    counts = (
        len(state["accepted"]),
        len(state["stack"]),
        len(state["unresolved"]),
    )
    partition_error = abs(
        base_5498.exact_partition_volume(state)
        - base_5498.exact_node_volume(state["root"])
    )
    source_v59_count = len(source.get("v59_adaptive_xt_audit_rows", []))
    new_v59_rows = state.get("v59_adaptive_xt_audit_rows", [])[source_v59_count:]

    def event_count(event: str) -> int:
        return sum(row.get("event") == event for row in new_v59_rows)

    cache_bindings = set(proof_cache)
    cache_rows_scoped = all(
        row.get("binding_sha256") in cache_bindings
        for row in new_v59_rows
        if row.get("outcome") == "CACHE_PASS"
    )
    carry = state["checkpoint_5512"]
    source_audits_preserved = all(
        state.get(key, [])[: len(source.get(key, []))] == source.get(key, [])
        for key, _, _ in AUDIT_BINDINGS
    )
    high_epsilon_pending = any(
        row["refinement_path"] == HIGH_EPSILON_PREFIX
        or row["refinement_path"].startswith(f"{HIGH_EPSILON_PREFIX}_")
        for row in state["stack"]
    )
    high_epsilon_unresolved = any(
        row["refinement_path"] == HIGH_EPSILON_PREFIX
        or row["refinement_path"].startswith(f"{HIGH_EPSILON_PREFIX}_")
        for row in state["unresolved"]
    )
    high_epsilon_accepted_paths = {
        row["refinement_path"]
        for row in state["accepted"]
        if row["refinement_path"] == HIGH_EPSILON_PREFIX
        or row["refinement_path"].startswith(f"{HIGH_EPSILON_PREFIX}_")
    }
    high_epsilon_branch_started = any(
        row["refinement_path"] == HIGH_EPSILON_PREFIX
        or row["refinement_path"].startswith(f"{HIGH_EPSILON_PREFIX}_")
        for row in records
    )
    complete_parent_leaf_paths = LOW_EPSILON_LEAF_PATHS | high_epsilon_accepted_paths
    epsilon_pair_union = base_5511.exact_union(
        base_5498,
        base_5503,
        state,
        EPSILON_PAIR_PARENT_PATH,
        complete_parent_leaf_paths,
    )
    parent_closure_required = (
        high_epsilon_branch_started
        and not high_epsilon_pending
        and not high_epsilon_unresolved
    )
    parent_closure_certified = (
        parent_closure_required
        and bool(high_epsilon_accepted_paths)
        and epsilon_pair_union["closure"]
        and epsilon_pair_union["volume_error"] == 0.0
        and epsilon_pair_union["minimum_amplitude_denominator_abs_lower"] > 0.0
        and epsilon_pair_union["minimum_relative_root_abs_lower"] > 0.0
        and epsilon_pair_union["minimum_selected_global_root_abs_lower"] > 0.0
        and epsilon_pair_union["collision_jacobian_abs_lower"] > 0.0
    )
    after_formalization = base_5467.formalization_snapshot()
    validations = [
        check("all_sources_exist", not missing, len(paths)),
        check("checkpoint_5511_evidence_is_hash_locked", inherited_hashes == expected_hashes, inherited_hashes),
        check("checkpoint_5511_low_epsilon_parent_is_certified", source_certified, result_5511.get("decision")),
        check("source_frontier_is_exact_190_2_0", source_counts == EXPECTED_SOURCE_COUNTS, source_counts),
        check("source_pending_order_is_exact", pending_paths == EXPECTED_PENDING_PATHS, pending_paths),
        check("source_v59_event_ledger_is_complete", len(source.get("v59_adaptive_xt_audit_rows", [])) == EXPECTED_SOURCE_V59_AUDIT_ROWS, source_v59_count),
        check("parent_v59_reconstructs_at_signed_revision", parent_reconstructed, parent_v59.REVISION),
        check("bounded_frontier_records_are_committed", 1 <= len(records) <= arguments.target_node_evaluations and records[0]["refinement_path"] == EXPECTED_PATH, [row["refinement_path"] for row in records]),
        check("total_and_v59_node_counts_increment_by_records", int(state["node_evaluation_count"]) == int(source["node_evaluation_count"]) + len(records) and int(state["v59_node_evaluation_count"]) == int(source.get("v59_node_evaluation_count", 0)) + len(records), (state["node_evaluation_count"], state["v59_node_evaluation_count"])),
        check("v58_frontier_node_count_does_not_increment", int(state["v58_node_evaluation_count"]) == int(source["v58_node_evaluation_count"]), state["v58_node_evaluation_count"]),
        check("atomic_record_replays_exactly", base_5500.replay_records(source, state, "checkpoint_5512"), record["outcome"]),
        check("source_append_only_ledgers_are_preserved", state["accepted"][: len(source["accepted"])] == source["accepted"] and state["refinement_witnesses"][: len(source["refinement_witnesses"])] == source["refinement_witnesses"] and state["unresolved"][: len(source["unresolved"])] == source["unresolved"], "accepted/witness/unresolved prefixes"),
        check("source_audit_ledgers_are_preserved", source_audits_preserved, len(AUDIT_BINDINGS)),
        check("source_hash_ledger_is_current", carry["source_accepted_sha256"] == base_5499.canonical_digest(source["accepted"]) and carry["source_pending_sha256"] == base_5499.canonical_digest(source["stack"]) and carry["source_refinement_witnesses_sha256"] == base_5499.canonical_digest(source["refinement_witnesses"]) and carry["source_v59_audit_sha256"] == base_5499.canonical_digest(source.get("v59_adaptive_xt_audit_rows", [])), carry["source_state_sha256"]),
        check("proof_cache_cannot_leak_to_other_bindings", cache_rows_scoped, event_count("TERMINAL")),
        check("exact_partition_volume_is_preserved", partition_error == 0, float(partition_error)),
        check("completed_high_epsilon_branch_closes_epsilon_pair_parent_exactly", not parent_closure_required or parent_closure_certified, {"required": parent_closure_required, "high_epsilon_pending": high_epsilon_pending, "high_epsilon_unresolved": high_epsilon_unresolved, "high_epsilon_accepted_paths": sorted(high_epsilon_accepted_paths), "union": epsilon_pair_union}),
        check("formalization_workbench_untouched", before_formalization == after_formalization, f"before={len(before_formalization)};after={len(after_formalization)}"),
        check("broad_claims_remain_false", not state["valid_for_parent_v59_active_cuboid"] and not state["valid_for_full_outer_parent_leaf_enclosure"] and not state["valid_for_D4_event_local_W3_bound"] and not state["valid_for_all_operator_local_GR_claim"] and not state["valid_for_full_MTS_claim"], "bounded parent-v59 frontier pass"),
    ]
    failed = [row for row in validations if not row["passed"]]
    if failed:
        decision = "PARENT_V59_HIGH_EPSILON_PARENT_CLOSURE_NOT_CERTIFIED"
    elif state["unresolved"]:
        decision = "PARENT_V59_HIGH_EPSILON_BRANCH_UNRESOLVED__DERIVE_REPAIR"
    elif parent_closure_certified:
        decision = "PARENT_V59_COMPLETE_EPSILON_PAIR_PARENT_CERTIFIED__RESUME_FRONTIER"
    elif str(record["outcome"]).startswith("REFINED_"):
        decision = "PARENT_V59_HIGH_EPSILON_BRANCH_REFINED__CONTINUE"
    elif state["stack"]:
        decision = "PARENT_V59_HIGH_EPSILON_BRANCH_PARTIAL__RESUME"
    else:
        decision = "PARENT_V59_ACTIVE_CUBOID_FRONTIER_EXHAUSTED__AGGREGATE"
    payload = {
        "checkpoint": CHECKPOINT,
        "revision": REVISION,
        "parent_revision": PARENT_V59_REVISION,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "decision": decision,
        "target_node_evaluations": arguments.target_node_evaluations,
        "processed_node_evaluations": len(records),
        "evaluated_paths": [row["refinement_path"] for row in records],
        "node_outcomes": [row["outcome"] for row in records],
        "checkpoint_runtime_seconds": math.fsum(float(row["runtime_seconds"]) for row in records),
        "evaluated_path": record["refinement_path"],
        "node_outcome": record["outcome"],
        "node_probe_passed": record["probe_passed"],
        "node_failure_type": record["failure_type"],
        "node_failure_message": record["failure_message"],
        "node_child_paths": record["child_paths"],
        "node_runtime_seconds": record["runtime_seconds"],
        "accepted_subcuboid_count": counts[0],
        "pending_subcuboid_count": counts[1],
        "unresolved_subcuboid_count": counts[2],
        "refinement_witness_count": len(state["refinement_witnesses"]),
        "v59_trigger_count": event_count("TRIGGER"),
        "v59_split_count": event_count("SPLIT"),
        "v59_cache_hit_count": sum(row.get("outcome") == "CACHE_PASS" for row in new_v59_rows),
        "v59_live_parent_pass_count": sum(row.get("outcome") == "LIVE_PARENT_PASS" for row in new_v59_rows),
        "v59_aggregate_count": event_count("AGGREGATE"),
        "high_epsilon_branch_complete": parent_closure_required,
        "high_epsilon_accepted_leaf_count": len(high_epsilon_accepted_paths),
        "exact_epsilon_pair_parent_closure": parent_closure_certified,
        "epsilon_pair_parent_leaf_count": len(complete_parent_leaf_paths),
        "epsilon_pair_parent_integrated_regular_path_abs_upper": epsilon_pair_union["integrated_regular_path_abs_upper"],
        "epsilon_pair_parent_amplitude_denominator_abs_lower": epsilon_pair_union["minimum_amplitude_denominator_abs_lower"],
        "epsilon_pair_parent_relative_root_abs_lower": epsilon_pair_union["minimum_relative_root_abs_lower"],
        "epsilon_pair_parent_selected_global_root_abs_lower": epsilon_pair_union["minimum_selected_global_root_abs_lower"],
        "epsilon_pair_parent_collision_jacobian_abs_lower": epsilon_pair_union["collision_jacobian_abs_lower"],
        "partition_volume_error": float(partition_error),
        "validation_row_count": len(validations),
        "failed_validation_count": len(failed),
        "valid_for_parent_v59_high_epsilon_frontier": not failed,
        "valid_for_parent_v59_complete_epsilon_pair_parent": not failed and parent_closure_certified,
        "valid_for_parent_v59_active_cuboid": False,
        "valid_for_full_outer_parent_leaf_enclosure": False,
        "valid_for_D4_event_local_W3_bound": False,
        "valid_for_all_operator_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
        "next_target": state["stack"][-1]["refinement_path"] if state["stack"] and not state["unresolved"] else "DERIVE_LOCAL_REPAIR",
    }
    node_rows = [{
        **{
            key: value
            for key, value in item.items()
            if key not in {"counts_before", "counts_after", "new_audit_counts", "child_paths"}
        },
        "child_paths": "|".join(item["child_paths"]),
        "counts_before": json.dumps(item["counts_before"], sort_keys=True, separators=(",", ":")),
        "counts_after": json.dumps(item["counts_after"], sort_keys=True, separators=(",", ":")),
        "new_audit_counts": json.dumps(item["new_audit_counts"], sort_keys=True, separators=(",", ":")),
    } for item in records]
    base_5467.atomic_csv(NODE_AUDIT, node_rows)
    base_5467.atomic_csv(UNION_AUDIT, [{
        "union_id": "complete_epsilon_pair_parent",
        "high_epsilon_branch_complete": parent_closure_required,
        "high_epsilon_accepted_leaf_count": len(high_epsilon_accepted_paths),
        **epsilon_pair_union,
    }])
    for key, _, path in AUDIT_BINDINGS:
        rows = state.get(key, [])
        if key == "v59_adaptive_xt_audit_rows":
            base_5467.atomic_csv(path, rows or empty_v59_audit())
        elif rows:
            base_5467.atomic_csv(path, rows)
    base_5467.atomic_csv(SOURCE_REGISTER, [{
        "source_path": str(path),
        "sha256": base_5499.digest(path),
        "exists": path.is_file(),
    } for path in paths])
    base_5467.atomic_csv(VALIDATION, validations)
    base_5467.atomic_json(STATUS, payload)
    base_5467.atomic_json(RESULT, payload)
    render_document(payload, base_5467)
    print(json.dumps({key: payload[key] for key in (
        "decision",
        "processed_node_evaluations",
        "evaluated_path",
        "node_outcome",
        "accepted_subcuboid_count",
        "pending_subcuboid_count",
        "unresolved_subcuboid_count",
        "v59_trigger_count",
        "v59_split_count",
        "v59_cache_hit_count",
        "v59_aggregate_count",
        "high_epsilon_branch_complete",
        "high_epsilon_accepted_leaf_count",
        "exact_epsilon_pair_parent_closure",
        "partition_volume_error",
        "failed_validation_count",
        "next_target",
    )}, indent=2))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
