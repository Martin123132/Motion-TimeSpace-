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
OUTPUT = FUNCTIONAL_RG / "5500"
WORK = OUTPUT / "work-v1"

SCRIPT_5499 = SCRIPTS / "Y5_R2FR_5499_D4_parent_v58_resumable_two_node_frontier_runner.py"
SOURCE_STATE = (
    FUNCTIONAL_RG
    / "5499"
    / "work-v1"
    / "E07__U051__RIGHT_CONNECTOR__CUBOID__6df3d70a73e4618b.json"
)
RESULT_5499 = FUNCTIONAL_RG / "5499" / "D4_parent_v58_resumable_two_node_result.json"
VALIDATION_5499 = FUNCTIONAL_RG / "5499" / "P8_Y5_BRR5498_5499_VALIDATION.csv"
SOURCE_REGISTER_5499 = FUNCTIONAL_RG / "5499" / "source_register.csv"
NODE_AUDIT_5499 = FUNCTIONAL_RG / "5499" / "D4_parent_v58_resumable_two_node_audit.csv"
CERTIFICATE_5496 = FUNCTIONAL_RG / "5496" / "D4_parent_v58_adaptive_complete_amplitude_certificate.json"

TARGET_CUBOID_ID = "E07__U051__RIGHT_CONNECTOR__CUBOID__6df3d70a73e4618b"
STATE = WORK / f"{TARGET_CUBOID_ID}.json"
NODE_AUDIT = OUTPUT / "D4_parent_v58_low_t_two_node_audit.csv"
V58_AUDIT = OUTPUT / "D4_parent_v58_frontier_certificate_application_audit.csv"
V57_AUDIT = OUTPUT / "D4_parent_v58_frontier_scoped_certificate_audit.csv"
JACOBIAN_XT_AUDIT = OUTPUT / "D4_parent_v58_frontier_collision_jacobian_xt_audit.csv"
STABLE_XT_AUDIT = OUTPUT / "D4_parent_v58_frontier_stable_edge_xt_audit.csv"
PIVOT_AUDIT = OUTPUT / "D4_parent_v58_frontier_first_spinor_pivot_audit.csv"
STABLE_T_AUDIT = OUTPUT / "D4_parent_v58_frontier_stable_edge_t_audit.csv"
JACOBIAN_T_AUDIT = OUTPUT / "D4_parent_v58_frontier_collision_jacobian_t_audit.csv"
SOURCE_REGISTER = OUTPUT / "source_register.csv"
VALIDATION = OUTPUT / "P8_Y5_BRR5499_5500_VALIDATION.csv"
STATUS = OUTPUT / "status.json"
RESULT = OUTPUT / "D4_parent_v58_low_t_two_node_result.json"
DOCUMENT = POST / "5500-Y5-R2FR-D4-parent-v58-low-t-two-node-frontier-runner.md"

CHECKPOINT = 5500
REVISION = "D4-parent-v58-low-t-two-node-frontier-v1"
PARENT_V58_REVISION = "D4-deformed-contour-regular-away-W3-v58-adaptive-stable-edge-local-T2-union"
EXPECTED_FIRST_PATH = "R_E0S_E0S_E1S_X0S_X0S_T0S"
EXPECTED_SOURCE_PENDING_PATHS = (
    "R_E1S",
    "R_E0S_E1S",
    "R_E0S_E0S_E1S_X1S",
    "R_E0S_E0S_E1S_X0S_X1S",
    "R_E0S_E0S_E1S_X0S_X0S_T1S",
    EXPECTED_FIRST_PATH,
)
EXPECTED_SOURCE_COUNTS = (179, 6, 0)
EXPECTED_SOURCE_WITNESSES = 62
EXPECTED_SCRIPT_5499_SHA256 = "0b40e436faa92226b5b8e36c075e0ce74be8d91a1581220a794a490cd1fa9962"
EXPECTED_SOURCE_STATE_SHA256 = "c63cc94f32504abba2bf9adb5fa95e981505fd7d2a6260af8170ac60b47bd994"
EXPECTED_RESULT_5499_SHA256 = "d60c1832aa4496630f1c5ded08599841c71a657a54abe243b90c46b7ceb6d4b7"
EXPECTED_VALIDATION_5499_SHA256 = "bd3269d7f16010d38e99a7eb463e251e5ae01ddc3068ebc8db7331fc33b6298c"
EXPECTED_SOURCE_REGISTER_5499_SHA256 = "4d5ada1d49b7d0ed0e9f6929e9e3696ac762db0fc0c3613f7ad0d164553b403d"
EXPECTED_NODE_AUDIT_5499_SHA256 = "ca4f55e8547760d7787458e28088b0a4424108ae7d33a3b229e72ebb498ada83"
EXPECTED_CERTIFICATE_5496_SHA256 = "27dc7fce1f83b424e9d9341778a392b83ed7c8659d12e05afd561338782fc708"

AUDIT_BINDINGS = (
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


def source_paths(base_5499: Any, base_5498: Any, base_5496: Any, base_5495: Any) -> tuple[Path, ...]:
    return tuple(
        dict.fromkeys(
            (
                Path(__file__).resolve(),
                *base_5499.source_paths(base_5498, base_5496, base_5495),
                SCRIPT_5499,
                SOURCE_STATE,
                RESULT_5499,
                VALIDATION_5499,
                SOURCE_REGISTER_5499,
                NODE_AUDIT_5499,
                CERTIFICATE_5496,
            )
        )
    )


def carry_forward_state(base_5499: Any, source: dict[str, Any], target: int) -> dict[str, Any]:
    state = deepcopy(source)
    state["checkpoint"] = CHECKPOINT
    state["revision"] = REVISION
    state["parent_revision"] = PARENT_V58_REVISION
    state["checkpoint_5500"] = {
        "source_state_path": str(SOURCE_STATE),
        "source_state_sha256": EXPECTED_SOURCE_STATE_SHA256,
        "source_accepted_sha256": base_5499.canonical_digest(source["accepted"]),
        "source_pending_sha256": base_5499.canonical_digest(source["stack"]),
        "source_unresolved_sha256": base_5499.canonical_digest(source["unresolved"]),
        "source_refinement_witnesses_sha256": base_5499.canonical_digest(source["refinement_witnesses"]),
        "target_node_evaluations": target,
        "records": [],
        "created_utc": datetime.now(timezone.utc).isoformat(),
    }
    state["processed_this_run"] = 0
    state["decision"] = "PARENT_V58_FRONTIER_PARTIAL__RESUME"
    for field in (
        "valid_for_parent_v58_active_cuboid",
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
    parent_v58: Any,
    cells: dict[str, Any],
    support_segments: list[dict[str, Any]],
    branches: dict[str, Any],
    cuboid: dict[str, Any],
    state: dict[str, Any],
    maximum_refinement_depth: int,
    work_key: str,
    state_path: Path,
    certificate_source: str,
) -> dict[str, Any]:
    node = deepcopy(state["stack"][-1])
    before = {
        "accepted": len(state["accepted"]),
        "pending": len(state["stack"]),
        "unresolved": len(state["unresolved"]),
        "witnesses": len(state["refinement_witnesses"]),
    }
    audit_starts = {
        key: len(getattr(parent_v58, attribute, []))
        for key, attribute, _ in AUDIT_BINDINGS
    }
    started = time.perf_counter()
    result = base_5469.evaluate_node(
        base_5468,
        stable,
        parent_v58,
        cells,
        support_segments,
        branches,
        cuboid,
        node,
    )
    runtime = time.perf_counter() - started
    compact = base_5469.compact_node_result(node, result)
    compact["certificate_source"] = certificate_source
    compact["parent_revision"] = PARENT_V58_REVISION
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
                lower_child, upper_child = base_5469.split_node(node, axis, split, source_boundary)
                state["stack"].append(upper_child)
                state["stack"].append(lower_child)
                state["split_axis_counts"][axis] = int(state["split_axis_counts"][axis]) + 1
                children = [lower_child, upper_child]
                outcome = f"REFINED_{str(axis).upper()}2"
    new_audits: dict[str, int] = {}
    for key, attribute, _ in AUDIT_BINDINGS:
        parent_rows = list(getattr(parent_v58, attribute, []))
        rows = parent_rows[audit_starts[key] :]
        state.setdefault(key, []).extend(rows)
        new_audits[key] = len(rows)
    state["v58_node_evaluation_count"] = int(state.get("v58_node_evaluation_count", 0)) + 1
    state["v58_accepted_subcuboid_count"] = int(state.get("v58_accepted_subcuboid_count", 0)) + (1 if outcome == "ACCEPTED" else 0)
    state["v58_refinement_witness_count"] = int(state.get("v58_refinement_witness_count", 0)) + (0 if outcome == "ACCEPTED" else 1)
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
        raise RuntimeError("checkpoint-5500 atomic node broke the exact partition")
    after = {
        "accepted": len(state["accepted"]),
        "pending": len(state["stack"]),
        "unresolved": len(state["unresolved"]),
        "witnesses": len(state["refinement_witnesses"]),
    }
    record = {
        "ordinal": len(state[work_key]["records"]),
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
        "counts_before": before,
        "counts_after": after,
        "runtime_seconds": runtime,
        "new_audit_counts": new_audits,
        "created_utc": datetime.now(timezone.utc).isoformat(),
    }
    state[work_key]["records"].append(record)
    state["processed_this_run"] = len(state[work_key]["records"])
    state["coverage_error"] = 0.0
    state["decision"] = "PARENT_V58_FRONTIER_PARTIAL__RESUME"
    for field in (
        "valid_for_parent_v58_active_cuboid",
        "valid_for_full_outer_parent_leaf_enclosure",
        "valid_for_D4_event_local_W3_bound",
        "valid_for_all_operator_local_GR_claim",
        "valid_for_full_MTS_claim",
    ):
        state[field] = False
    state["last_update_utc"] = record["created_utc"]
    base_5467.atomic_json(state_path, state, compact=True)
    return state


def replay_records(
    source: dict[str, Any],
    state: dict[str, Any],
    work_key: str,
) -> bool:
    pending = [str(row["refinement_path"]) for row in source["stack"]]
    accepted: list[str] = []
    witnesses: list[str] = []
    unresolved: list[str] = []
    records = state[work_key]["records"]
    for ordinal, record in enumerate(records):
        if not pending or int(record["ordinal"]) != ordinal:
            return False
        path = pending.pop()
        if path != record["refinement_path"]:
            return False
        outcome = str(record["outcome"])
        children = list(record["child_paths"])
        if outcome == "ACCEPTED":
            accepted.append(path)
            if children:
                return False
        else:
            witnesses.append(path)
            if outcome.startswith("REFINED_") and len(children) == 2:
                pending.extend([children[1], children[0]])
            elif outcome.startswith("UNRESOLVED_") and not children:
                unresolved.append(path)
            else:
                return False
    return (
        pending == [str(row["refinement_path"]) for row in state["stack"]]
        and accepted == [str(row["refinement_path"]) for row in state["accepted"][len(source["accepted"]) :]]
        and witnesses == [str(row["refinement_path"]) for row in state["refinement_witnesses"][len(source["refinement_witnesses"]) :]]
        and unresolved == [str(row["refinement_path"]) for row in state["unresolved"][len(source["unresolved"]) :]]
    )


def render_document(payload: dict[str, Any], records: list[dict[str, Any]], base_5467: Any) -> None:
    rows = [
        f"- `{record['refinement_path']}` -> `{record['outcome']}` in `{record['runtime_seconds']}` seconds; `{record['failure_message']}`."
        for record in records
    ]
    lines = [
        "# 5500: D4 parent-v58 low-t two-node frontier runner",
        "",
        "Checkpoint 5499 is hash locked and its exact low-t child is evaluated first. At most one depth-first successor is then evaluated, with an atomic state commit after each node.",
        "",
        *rows,
        "",
        f"Frontier: `{payload['accepted_subcuboid_count']}/{payload['pending_subcuboid_count']}/{payload['unresolved_subcuboid_count']}`. Exact partition error: `{payload['partition_volume_error']}`. New v58 applications: `{payload['new_v58_application_count']}`.",
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
    parser.add_argument("--target-node-evaluations", type=int, default=2)
    parser.add_argument("--max-runtime-seconds", type=float, default=12600.0)
    parser.add_argument("--maximum-refinement-depth", type=int, default=33)
    arguments = parser.parse_args()
    if arguments.target_node_evaluations < 1 or arguments.target_node_evaluations > 2:
        raise ValueError("target node evaluations must be one or two")
    base_5499 = load_module("mts_5499_for_5500", SCRIPT_5499)
    base_5498 = load_module("mts_5498_for_5500", base_5499.SCRIPT_5498)
    base_5496 = load_module("mts_5496_for_5500", base_5498.SCRIPT_5496)
    base_5495 = load_module("mts_5495_for_5500", base_5496.SCRIPT_5495)
    base_5467 = load_module("mts_5467_for_5500", base_5495.SCRIPT_5467)
    base_5468 = load_module("mts_5468_for_5500", base_5495.SCRIPT_5468)
    base_5469 = load_module("mts_5469_for_5500", base_5495.SCRIPT_5469)
    base_5472 = load_module("mts_5472_for_5500", base_5495.SCRIPT_5472)
    base_5474 = load_module("mts_5474_for_5500", base_5495.SCRIPT_5474)
    base_5476 = load_module("mts_5476_for_5500", base_5495.SCRIPT_5476)
    base_5478 = load_module("mts_5478_for_5500", base_5495.SCRIPT_5478)
    base_5480 = load_module("mts_5480_for_5500", base_5495.SCRIPT_5480)
    base_5483 = load_module("mts_5483_for_5500", base_5495.SCRIPT_5483)
    base_5490 = load_module("mts_5490_for_5500", base_5495.SCRIPT_5490)
    base_5493 = load_module("mts_5493_for_5500", base_5495.SCRIPT_5493)
    base_5467.set_below_normal_priority()
    base_5480.set_single_core_affinity()
    before_formalization = base_5467.formalization_snapshot()
    paths = source_paths(base_5499, base_5498, base_5496, base_5495)
    missing = [str(path) for path in paths if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"missing sources: {missing}")
    inherited_hashes = {
        "script_5499": base_5499.digest(SCRIPT_5499),
        "source_state": base_5499.digest(SOURCE_STATE),
        "result_5499": base_5499.digest(RESULT_5499),
        "validation_5499": base_5499.digest(VALIDATION_5499),
        "source_register_5499": base_5499.digest(SOURCE_REGISTER_5499),
        "node_audit_5499": base_5499.digest(NODE_AUDIT_5499),
        "certificate_5496": base_5499.digest(CERTIFICATE_5496),
    }
    expected_hashes = {
        "script_5499": EXPECTED_SCRIPT_5499_SHA256,
        "source_state": EXPECTED_SOURCE_STATE_SHA256,
        "result_5499": EXPECTED_RESULT_5499_SHA256,
        "validation_5499": EXPECTED_VALIDATION_5499_SHA256,
        "source_register_5499": EXPECTED_SOURCE_REGISTER_5499_SHA256,
        "node_audit_5499": EXPECTED_NODE_AUDIT_5499_SHA256,
        "certificate_5496": EXPECTED_CERTIFICATE_5496_SHA256,
    }
    if inherited_hashes != expected_hashes:
        raise RuntimeError("checkpoint-5500 inherited source hash mismatch")
    source = base_5499.read_json(SOURCE_STATE)
    result_5499 = base_5499.read_json(RESULT_5499)
    validation_5499 = base_5499.read_csv(VALIDATION_5499)
    register_5499 = base_5499.read_csv(SOURCE_REGISTER_5499)
    certificate_5496 = base_5499.read_json(CERTIFICATE_5496)
    source_counts = (len(source["accepted"]), len(source["stack"]), len(source["unresolved"]))
    pending_paths = tuple(str(row["refinement_path"]) for row in source["stack"])
    source_certified = (
        result_5499.get("decision") == "PARENT_V58_TWO_NODE_FRONTIER_CERTIFIED__INTERPRET_NEXT_OBSTRUCTION"
        and int(result_5499.get("failed_validation_count", -1)) == 0
        and all(base_5499.truth(row.get("passed")) for row in validation_5499)
        and base_5499.source_register_is_current(register_5499)
        and source_counts == EXPECTED_SOURCE_COUNTS
        and len(source["refinement_witnesses"]) == EXPECTED_SOURCE_WITNESSES
        and pending_paths == EXPECTED_SOURCE_PENDING_PATHS
        and base_5498.exact_partition_volume(source) == base_5498.exact_node_volume(source["root"])
    )
    if not source_certified:
        raise RuntimeError("checkpoint-5499 source is not current and certified")
    stable, _, cells, support_segments, branches = base_5467.load_parent()
    cuboid = next(row for row in base_5499.read_csv(base_5495.MANIFEST_5468) if row["cuboid_job_id"] == TARGET_CUBOID_ID)
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
    if arguments.dry_run:
        print(json.dumps({
            "checkpoint": CHECKPOINT,
            "dry_run": True,
            "source_counts": list(source_counts),
            "first_path": source["stack"][-1]["refinement_path"],
            "target_node_evaluations": arguments.target_node_evaluations,
            "parent_revision": parent_v58.REVISION,
            "source_hashes_match": inherited_hashes == expected_hashes,
            "exact_source_partition": True,
        }, indent=2))
        return 0
    if STATE.is_file():
        state = base_5499.read_json(STATE)
        work = state.get("checkpoint_5500", {})
        if work.get("source_state_sha256") != EXPECTED_SOURCE_STATE_SHA256:
            raise RuntimeError("checkpoint-5500 resumable source mismatch")
        if int(work.get("target_node_evaluations", -1)) != arguments.target_node_evaluations:
            raise RuntimeError("checkpoint-5500 target changed after start")
    else:
        WORK.mkdir(parents=True, exist_ok=True)
        state = carry_forward_state(base_5499, source, arguments.target_node_evaluations)
        base_5467.atomic_json(STATE, state, compact=True)
    started = time.perf_counter()
    processed = 0
    while len(state["checkpoint_5500"]["records"]) < arguments.target_node_evaluations and state["stack"] and not state["unresolved"]:
        if processed and time.perf_counter() - started >= arguments.max_runtime_seconds:
            break
        state = process_atomic_node(
            base_5499,
            base_5498,
            base_5467,
            base_5468,
            base_5469,
            stable,
            parent_v58,
            cells,
            support_segments,
            branches,
            cuboid,
            state,
            arguments.maximum_refinement_depth,
            "checkpoint_5500",
            STATE,
            "checkpoint_5500_parent_v58",
        )
        processed += 1
    records = list(state["checkpoint_5500"]["records"])
    counts = (len(state["accepted"]), len(state["stack"]), len(state["unresolved"]))
    partition_error = abs(base_5498.exact_partition_volume(state) - base_5498.exact_node_volume(state["root"]))
    new_v58 = len(state.get("v58_certificate_application_audit_rows", [])) - len(source.get("v58_certificate_application_audit_rows", []))
    carry = state["checkpoint_5500"]
    after_formalization = base_5467.formalization_snapshot()
    validations = [
        check("all_sources_exist", not missing, len(paths)),
        check("checkpoint_5499_evidence_is_hash_locked", inherited_hashes == expected_hashes, inherited_hashes),
        check("checkpoint_5499_frontier_is_certified", source_certified, result_5499.get("decision")),
        check("source_frontier_is_exact_179_6_0", source_counts == EXPECTED_SOURCE_COUNTS, source_counts),
        check("source_pending_order_is_exact", pending_paths == EXPECTED_SOURCE_PENDING_PATHS, pending_paths),
        check("parent_v58_reconstructs_at_signed_revision", parent_v58.REVISION == PARENT_V58_REVISION and not parent_v58.V58_PARENT_ACTION_CHANGED and parent_v58.V58_ONLY_ENCLOSURE_COMPOSITION_CHANGED, parent_v58.REVISION),
        check("one_or_two_nodes_are_atomically_committed", 1 <= len(records) <= arguments.target_node_evaluations, len(records)),
        check("first_low_t_path_is_exact", records and records[0]["refinement_path"] == EXPECTED_FIRST_PATH, records[0]["refinement_path"] if records else "NONE"),
        check("node_counts_match_records", int(state["node_evaluation_count"]) == int(source["node_evaluation_count"]) + len(records) and int(state["v58_node_evaluation_count"]) == int(source["v58_node_evaluation_count"]) + len(records), state["node_evaluation_count"]),
        check(
            "atomic_records_replay_exactly",
            replay_records(source, state, "checkpoint_5500"),
            len(records),
        ),
        check("source_append_only_ledgers_are_preserved", state["accepted"][: len(source["accepted"])] == source["accepted"] and state["refinement_witnesses"][: len(source["refinement_witnesses"])] == source["refinement_witnesses"] and state["unresolved"][: len(source["unresolved"])] == source["unresolved"], "accepted/witness/unresolved prefixes"),
        check("source_hash_ledger_is_current", carry["source_accepted_sha256"] == base_5499.canonical_digest(source["accepted"]) and carry["source_pending_sha256"] == base_5499.canonical_digest(source["stack"]) and carry["source_refinement_witnesses_sha256"] == base_5499.canonical_digest(source["refinement_witnesses"]), carry["source_state_sha256"]),
        check("v58_certificate_does_not_leak_outside_binding", new_v58 == 0 and sum(int(row["new_audit_counts"]["v58_certificate_application_audit_rows"]) for row in records) == 0, new_v58),
        check("frontier_count_fields_are_coherent", int(state["accepted_subcuboid_count"]) == counts[0] and int(state["pending_subcuboid_count"]) == counts[1] and int(state["unresolved_subcuboid_count"]) == counts[2], counts),
        check("exact_partition_volume_is_preserved", partition_error == 0, float(partition_error)),
        check("formalization_workbench_untouched", before_formalization == after_formalization, f"before={len(before_formalization)};after={len(after_formalization)}"),
        check("broad_claims_remain_false", not state["valid_for_parent_v58_active_cuboid"] and not state["valid_for_full_outer_parent_leaf_enclosure"] and not state["valid_for_D4_event_local_W3_bound"] and not state["valid_for_all_operator_local_GR_claim"] and not state["valid_for_full_MTS_claim"], "partial frontier"),
    ]
    failed = [row for row in validations if not row["passed"]]
    decision = (
        "PARENT_V58_LOW_T_TWO_NODE_FRONTIER_CERTIFIED__CHOOSE_NEXT_ROUTE"
        if not failed and len(records) == arguments.target_node_evaluations and not state["unresolved"]
        else (
            "PARENT_V58_LOW_T_FRONTIER_CERTIFIED__DERIVE_LOCAL_REPAIR"
            if not failed and state["unresolved"]
            else (
                "PARENT_V58_LOW_T_FRONTIER_PARTIAL__RESUME"
                if not failed
                else "PARENT_V58_LOW_T_FRONTIER_NOT_CERTIFIED"
            )
        )
    )
    payload = {
        "checkpoint": CHECKPOINT,
        "revision": REVISION,
        "parent_revision": PARENT_V58_REVISION,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "decision": decision,
        "target_node_evaluations": arguments.target_node_evaluations,
        "completed_node_evaluations": len(records),
        "evaluated_paths": [row["refinement_path"] for row in records],
        "node_outcomes": [row["outcome"] for row in records],
        "accepted_subcuboid_count": counts[0],
        "pending_subcuboid_count": counts[1],
        "unresolved_subcuboid_count": counts[2],
        "new_v58_application_count": new_v58,
        "partition_volume_error": float(partition_error),
        "validation_row_count": len(validations),
        "failed_validation_count": len(failed),
        "valid_for_parent_v58_low_t_frontier": not failed,
        "valid_for_parent_v58_active_cuboid": False,
        "valid_for_full_outer_parent_leaf_enclosure": False,
        "valid_for_D4_event_local_W3_bound": False,
        "valid_for_all_operator_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
        "next_target": state["stack"][-1]["refinement_path"] if state["stack"] and not state["unresolved"] else "DERIVE_LOCAL_REPAIR",
    }
    node_rows = [{
        **{key: value for key, value in row.items() if key not in {"counts_before", "counts_after", "new_audit_counts", "child_paths"}},
        "child_paths": "|".join(row["child_paths"]),
        "counts_before": json.dumps(row["counts_before"], sort_keys=True, separators=(",", ":")),
        "counts_after": json.dumps(row["counts_after"], sort_keys=True, separators=(",", ":")),
        "new_audit_counts": json.dumps(row["new_audit_counts"], sort_keys=True, separators=(",", ":")),
    } for row in records]
    base_5467.atomic_csv(NODE_AUDIT, node_rows)
    for key, _, path in AUDIT_BINDINGS:
        if state.get(key):
            base_5467.atomic_csv(path, state[key])
    base_5467.atomic_csv(SOURCE_REGISTER, [{"source_path": str(path), "sha256": base_5499.digest(path), "exists": path.is_file()} for path in paths])
    base_5467.atomic_csv(VALIDATION, validations)
    base_5467.atomic_json(STATUS, payload)
    base_5467.atomic_json(RESULT, payload)
    render_document(payload, records, base_5467)
    print(json.dumps({key: payload[key] for key in (
        "decision",
        "completed_node_evaluations",
        "evaluated_paths",
        "node_outcomes",
        "accepted_subcuboid_count",
        "pending_subcuboid_count",
        "unresolved_subcuboid_count",
        "new_v58_application_count",
        "partition_volume_error",
        "failed_validation_count",
        "next_target",
    )}, indent=2))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
