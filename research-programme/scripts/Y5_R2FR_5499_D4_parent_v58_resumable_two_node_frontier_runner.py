from __future__ import annotations

import argparse
import csv
import hashlib
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
OUTPUT = FUNCTIONAL_RG / "5499"
WORK = OUTPUT / "work-v1"

SCRIPT_5498 = SCRIPTS / "Y5_R2FR_5498_D4_parent_v58_one_atomic_frontier_node.py"
SOURCE_STATE = (
    FUNCTIONAL_RG
    / "5498"
    / "work-v1"
    / "E07__U051__RIGHT_CONNECTOR__CUBOID__6df3d70a73e4618b.json"
)
RESULT_5498 = FUNCTIONAL_RG / "5498" / "D4_parent_v58_one_atomic_frontier_node_result.json"
VALIDATION_5498 = FUNCTIONAL_RG / "5498" / "P8_Y5_BRR5497_5498_VALIDATION.csv"
SOURCE_REGISTER_5498 = FUNCTIONAL_RG / "5498" / "source_register.csv"
NODE_AUDIT_5498 = FUNCTIONAL_RG / "5498" / "D4_parent_v58_one_atomic_frontier_node_audit.csv"
CERTIFICATE_5496 = FUNCTIONAL_RG / "5496" / "D4_parent_v58_adaptive_complete_amplitude_certificate.json"

TARGET_CUBOID_ID = "E07__U051__RIGHT_CONNECTOR__CUBOID__6df3d70a73e4618b"
STATE = WORK / f"{TARGET_CUBOID_ID}.json"
NODE_AUDIT = OUTPUT / "D4_parent_v58_resumable_two_node_audit.csv"
V58_AUDIT = OUTPUT / "D4_parent_v58_frontier_certificate_application_audit.csv"
V57_AUDIT = OUTPUT / "D4_parent_v58_frontier_scoped_certificate_audit.csv"
JACOBIAN_XT_AUDIT = OUTPUT / "D4_parent_v58_frontier_collision_jacobian_xt_audit.csv"
STABLE_XT_AUDIT = OUTPUT / "D4_parent_v58_frontier_stable_edge_xt_audit.csv"
PIVOT_AUDIT = OUTPUT / "D4_parent_v58_frontier_first_spinor_pivot_audit.csv"
STABLE_T_AUDIT = OUTPUT / "D4_parent_v58_frontier_stable_edge_t_audit.csv"
JACOBIAN_T_AUDIT = OUTPUT / "D4_parent_v58_frontier_collision_jacobian_t_audit.csv"
SOURCE_REGISTER = OUTPUT / "source_register.csv"
VALIDATION = OUTPUT / "P8_Y5_BRR5498_5499_VALIDATION.csv"
STATUS = OUTPUT / "status.json"
RESULT = OUTPUT / "D4_parent_v58_resumable_two_node_result.json"
DOCUMENT = POST / "5499-Y5-R2FR-D4-parent-v58-resumable-two-node-frontier-runner.md"

CHECKPOINT = 5499
REVISION = "D4-parent-v58-resumable-two-node-frontier-v1"
PARENT_V58_REVISION = "D4-deformed-contour-regular-away-W3-v58-adaptive-stable-edge-local-T2-union"
EXPECTED_FIRST_PATH = "R_E0S_E0S_E1S_X0S"
EXPECTED_SOURCE_PENDING_PATHS = (
    "R_E1S",
    "R_E0S_E1S",
    "R_E0S_E0S_E1S_X1S",
    EXPECTED_FIRST_PATH,
)
EXPECTED_SOURCE_COUNTS = (179, 4, 0)
EXPECTED_SOURCE_WITNESSES = 60
EXPECTED_SCRIPT_5498_SHA256 = "8ff72aa9a079e7bbca4144e00be186f99a3b2f34e1fb94f468881a2342e09c87"
EXPECTED_SOURCE_STATE_SHA256 = "3fb9224e90c8864568075ba5227a3eb0cfdea1bd0e17a938c9f28b1b9e4cbde7"
EXPECTED_RESULT_5498_SHA256 = "0c22ac6481eac41bb884bf866e1e6d8b60c742350bf87d4a6b3483b3a6e280b5"
EXPECTED_VALIDATION_5498_SHA256 = "faa01d8bb09d9566170ce8b985ffa8a7c310f189273c8b83d610eedfa8f2c142"
EXPECTED_SOURCE_REGISTER_5498_SHA256 = "ffea2c533775304833d616b75bbd31fba36313b87e8db944d695038e30424ac6"
EXPECTED_NODE_AUDIT_5498_SHA256 = "7ed4a1a9a66ba9ecc6c5806ac48fef124b2146aa97fb65933e4664162e5667e7"
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


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def truth(value: Any) -> bool:
    return value is True or str(value).strip().lower() == "true"


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def canonical_digest(value: Any) -> str:
    encoded = json.dumps(
        value,
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=True,
    ).encode("utf-8")
    return hashlib.sha256(encoded).hexdigest()


def source_paths(base_5498: Any, base_5496: Any, base_5495: Any) -> tuple[Path, ...]:
    return tuple(
        dict.fromkeys(
            (
                Path(__file__).resolve(),
                *base_5498.source_paths(base_5496, base_5495),
                SCRIPT_5498,
                SOURCE_STATE,
                RESULT_5498,
                VALIDATION_5498,
                SOURCE_REGISTER_5498,
                NODE_AUDIT_5498,
                CERTIFICATE_5496,
            )
        )
    )


def source_register_is_current(rows: list[dict[str, str]]) -> bool:
    return bool(rows) and all(
        truth(row.get("exists"))
        and Path(row["source_path"]).is_file()
        and digest(Path(row["source_path"])) == row["sha256"]
        for row in rows
    )


def check(gate: str, passed: bool, evidence: Any) -> dict[str, Any]:
    return {
        "checkpoint": CHECKPOINT,
        "validation_gate": gate,
        "passed": bool(passed),
        "evidence": evidence,
    }


def carry_forward_state(source: dict[str, Any], target_node_evaluations: int) -> dict[str, Any]:
    state = deepcopy(source)
    state["checkpoint"] = CHECKPOINT
    state["revision"] = REVISION
    state["parent_revision"] = PARENT_V58_REVISION
    state["checkpoint_5499"] = {
        "source_state_path": str(SOURCE_STATE),
        "source_state_sha256": EXPECTED_SOURCE_STATE_SHA256,
        "source_accepted_sha256": canonical_digest(source["accepted"]),
        "source_pending_sha256": canonical_digest(source["stack"]),
        "source_unresolved_sha256": canonical_digest(source["unresolved"]),
        "source_refinement_witnesses_sha256": canonical_digest(source["refinement_witnesses"]),
        "source_counts": list(EXPECTED_SOURCE_COUNTS),
        "target_node_evaluations": target_node_evaluations,
        "records": [],
        "created_utc": datetime.now(timezone.utc).isoformat(),
    }
    state["processed_this_run"] = 0
    state["decision"] = "PARENT_V58_FRONTIER_PARTIAL__RESUME"
    state["valid_for_parent_v58_active_cuboid"] = False
    state["valid_for_full_outer_parent_leaf_enclosure"] = False
    state["valid_for_D4_event_local_W3_bound"] = False
    state["valid_for_all_operator_local_GR_claim"] = False
    state["valid_for_full_MTS_claim"] = False
    return state


def process_atomic_node(
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
) -> dict[str, Any]:
    node = deepcopy(state["stack"][-1])
    counts_before = {
        "accepted": len(state["accepted"]),
        "pending": len(state["stack"]),
        "unresolved": len(state["unresolved"]),
        "witnesses": len(state["refinement_witnesses"]),
    }
    audit_starts = {
        state_key: len(getattr(parent_v58, parent_attribute, []))
        for state_key, parent_attribute, _ in AUDIT_BINDINGS
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
    runtime_seconds = time.perf_counter() - started
    compact = base_5469.compact_node_result(node, result)
    compact["certificate_source"] = "checkpoint_5499_parent_v58"
    compact["parent_revision"] = PARENT_V58_REVISION
    state["stack"].pop()
    state["node_evaluation_count"] = int(state["node_evaluation_count"]) + 1
    children: list[dict[str, Any]] = []
    if truth(result.get("probe_passed")):
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
    new_audit_counts: dict[str, int] = {}
    for state_key, parent_attribute, _ in AUDIT_BINDINGS:
        parent_rows = list(getattr(parent_v58, parent_attribute, []))
        new_rows = parent_rows[audit_starts[state_key] :]
        state.setdefault(state_key, []).extend(new_rows)
        new_audit_counts[state_key] = len(new_rows)
    state["v58_node_evaluation_count"] = int(state.get("v58_node_evaluation_count", 0)) + 1
    state["v58_accepted_subcuboid_count"] = int(state.get("v58_accepted_subcuboid_count", 0)) + (1 if outcome == "ACCEPTED" else 0)
    state["v58_refinement_witness_count"] = int(state.get("v58_refinement_witness_count", 0)) + (0 if outcome == "ACCEPTED" else 1)
    state["runtime_seconds"] = float(state.get("runtime_seconds", 0.0)) + runtime_seconds
    state["accepted_subcuboid_count"] = len(state["accepted"])
    state["pending_subcuboid_count"] = len(state["stack"])
    state["unresolved_subcuboid_count"] = len(state["unresolved"])
    state["accepted_volume"] = math.fsum(base_5469.node_volume(row) for row in state["accepted"])
    exact_error = abs(
        base_5498.exact_partition_volume(state)
        - base_5498.exact_node_volume(state["root"])
    )
    if exact_error != 0:
        raise RuntimeError("checkpoint-5499 atomic node broke the exact partition")
    counts_after = {
        "accepted": len(state["accepted"]),
        "pending": len(state["stack"]),
        "unresolved": len(state["unresolved"]),
        "witnesses": len(state["refinement_witnesses"]),
    }
    record = {
        "ordinal": len(state["checkpoint_5499"]["records"]),
        "refinement_path": node["refinement_path"],
        "epsilon_real_lower": node["epsilon_real_lower"],
        "epsilon_real_upper": node["epsilon_real_upper"],
        "x_lower": node["x_lower"],
        "x_upper": node["x_upper"],
        "t_lower": node["t_lower"],
        "t_upper": node["t_upper"],
        "outcome": outcome,
        "probe_passed": truth(result.get("probe_passed")),
        "failure_type": result.get("failure_type", ""),
        "failure_message": result.get("failure_message", ""),
        "child_paths": [str(row["refinement_path"]) for row in children],
        "counts_before": counts_before,
        "counts_after": counts_after,
        "runtime_seconds": runtime_seconds,
        "new_audit_counts": new_audit_counts,
        "created_utc": datetime.now(timezone.utc).isoformat(),
    }
    state["checkpoint_5499"]["records"].append(record)
    state["processed_this_run"] = len(state["checkpoint_5499"]["records"])
    state["coverage_error"] = 0.0
    state["decision"] = "PARENT_V58_FRONTIER_PARTIAL__RESUME"
    state["valid_for_parent_v58_active_cuboid"] = False
    state["valid_for_full_outer_parent_leaf_enclosure"] = False
    state["valid_for_D4_event_local_W3_bound"] = False
    state["valid_for_all_operator_local_GR_claim"] = False
    state["valid_for_full_MTS_claim"] = False
    state["last_update_utc"] = record["created_utc"]
    base_5467.atomic_json(STATE, state, compact=True)
    return state


def replay_records(source: dict[str, Any], state: dict[str, Any]) -> bool:
    records = state["checkpoint_5499"]["records"]
    pending = [str(row["refinement_path"]) for row in source["stack"]]
    accepted_paths: list[str] = []
    witness_paths: list[str] = []
    unresolved_paths: list[str] = []
    for ordinal, record in enumerate(records):
        if int(record["ordinal"]) != ordinal or not pending:
            return False
        path = pending.pop()
        if path != record["refinement_path"]:
            return False
        outcome = str(record["outcome"])
        children = list(record["child_paths"])
        if outcome == "ACCEPTED":
            accepted_paths.append(path)
            if children:
                return False
        else:
            witness_paths.append(path)
            if outcome.startswith("REFINED_"):
                if len(children) != 2:
                    return False
                pending.extend([children[1], children[0]])
            elif outcome.startswith("UNRESOLVED_"):
                unresolved_paths.append(path)
                if children:
                    return False
            else:
                return False
        after = record["counts_after"]
        if (
            int(after["accepted"]) != len(source["accepted"]) + len(accepted_paths)
            or int(after["pending"]) != len(pending)
            or int(after["unresolved"]) != len(source["unresolved"]) + len(unresolved_paths)
            or int(after["witnesses"]) != len(source["refinement_witnesses"]) + len(witness_paths)
        ):
            return False
    return (
        pending == [str(row["refinement_path"]) for row in state["stack"]]
        and accepted_paths
        == [str(row["refinement_path"]) for row in state["accepted"][len(source["accepted"]) :]]
        and witness_paths
        == [str(row["refinement_path"]) for row in state["refinement_witnesses"][len(source["refinement_witnesses"]) :]]
        and unresolved_paths
        == [str(row["refinement_path"]) for row in state["unresolved"][len(source["unresolved"]) :]]
    )


def render_document(payload: dict[str, Any], records: list[dict[str, Any]], base_5467: Any) -> None:
    result_lines = [
        f"- `{row['refinement_path']}` -> `{row['outcome']}` in `{row['runtime_seconds']}` seconds; failure `{row['failure_message']}`."
        for row in records
    ]
    lines = [
        "# 5499: D4 parent-v58 resumable two-node frontier runner",
        "",
        "The checkpoint-5498 frontier is hash locked. The unchanged parent-v58 chain advances depth first, committing each completed node atomically and stopping after two nodes or an unresolved result.",
        "",
        *result_lines,
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
    if arguments.max_runtime_seconds <= 0.0:
        raise ValueError("max runtime seconds must be positive")
    base_5498 = load_module("mts_5498_for_5499", SCRIPT_5498)
    base_5496 = load_module("mts_5496_for_5499", base_5498.SCRIPT_5496)
    base_5495 = load_module("mts_5495_for_5499", base_5496.SCRIPT_5495)
    base_5467 = load_module("mts_5467_for_5499", base_5495.SCRIPT_5467)
    base_5468 = load_module("mts_5468_for_5499", base_5495.SCRIPT_5468)
    base_5469 = load_module("mts_5469_for_5499", base_5495.SCRIPT_5469)
    base_5472 = load_module("mts_5472_for_5499", base_5495.SCRIPT_5472)
    base_5474 = load_module("mts_5474_for_5499", base_5495.SCRIPT_5474)
    base_5476 = load_module("mts_5476_for_5499", base_5495.SCRIPT_5476)
    base_5478 = load_module("mts_5478_for_5499", base_5495.SCRIPT_5478)
    base_5480 = load_module("mts_5480_for_5499", base_5495.SCRIPT_5480)
    base_5483 = load_module("mts_5483_for_5499", base_5495.SCRIPT_5483)
    base_5490 = load_module("mts_5490_for_5499", base_5495.SCRIPT_5490)
    base_5493 = load_module("mts_5493_for_5499", base_5495.SCRIPT_5493)
    base_5467.set_below_normal_priority()
    base_5480.set_single_core_affinity()
    before_formalization = base_5467.formalization_snapshot()
    paths = source_paths(base_5498, base_5496, base_5495)
    missing = [str(path) for path in paths if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"missing sources: {missing}")
    inherited_hashes = {
        "script_5498": digest(SCRIPT_5498),
        "source_state": digest(SOURCE_STATE),
        "result_5498": digest(RESULT_5498),
        "validation_5498": digest(VALIDATION_5498),
        "source_register_5498": digest(SOURCE_REGISTER_5498),
        "node_audit_5498": digest(NODE_AUDIT_5498),
        "certificate_5496": digest(CERTIFICATE_5496),
    }
    expected_hashes = {
        "script_5498": EXPECTED_SCRIPT_5498_SHA256,
        "source_state": EXPECTED_SOURCE_STATE_SHA256,
        "result_5498": EXPECTED_RESULT_5498_SHA256,
        "validation_5498": EXPECTED_VALIDATION_5498_SHA256,
        "source_register_5498": EXPECTED_SOURCE_REGISTER_5498_SHA256,
        "node_audit_5498": EXPECTED_NODE_AUDIT_5498_SHA256,
        "certificate_5496": EXPECTED_CERTIFICATE_5496_SHA256,
    }
    if inherited_hashes != expected_hashes:
        raise RuntimeError("checkpoint-5499 inherited source hash mismatch")
    source = read_json(SOURCE_STATE)
    result_5498 = read_json(RESULT_5498)
    validation_5498 = read_csv(VALIDATION_5498)
    register_5498 = read_csv(SOURCE_REGISTER_5498)
    certificate_5496 = read_json(CERTIFICATE_5496)
    source_counts = (len(source["accepted"]), len(source["stack"]), len(source["unresolved"]))
    source_paths_pending = tuple(str(row["refinement_path"]) for row in source["stack"])
    source_certified = (
        result_5498.get("decision")
        == "PARENT_V58_ONE_ATOMIC_FRONTIER_NODE_CERTIFIED__CONTINUE_FRONTIER"
        and int(result_5498.get("failed_validation_count", -1)) == 0
        and all(truth(row.get("passed")) for row in validation_5498)
        and source_register_is_current(register_5498)
        and source_counts == EXPECTED_SOURCE_COUNTS
        and len(source["refinement_witnesses"]) == EXPECTED_SOURCE_WITNESSES
        and source_paths_pending == EXPECTED_SOURCE_PENDING_PATHS
        and base_5498.exact_partition_volume(source) == base_5498.exact_node_volume(source["root"])
    )
    if not source_certified:
        raise RuntimeError("checkpoint-5498 source frontier is not current and certified")
    stable, _, cells, support_segments, branches = base_5467.load_parent()
    cuboid = next(
        row
        for row in read_csv(base_5495.MANIFEST_5468)
        if row["cuboid_job_id"] == TARGET_CUBOID_ID
    )
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
        print(
            json.dumps(
                {
                    "checkpoint": CHECKPOINT,
                    "dry_run": True,
                    "source_counts": list(source_counts),
                    "first_path": source["stack"][-1]["refinement_path"],
                    "target_node_evaluations": arguments.target_node_evaluations,
                    "parent_revision": parent_v58.REVISION,
                    "source_hashes_match": inherited_hashes == expected_hashes,
                    "exact_source_partition": True,
                },
                indent=2,
            )
        )
        return 0
    if STATE.is_file():
        state = read_json(STATE)
        work = state.get("checkpoint_5499", {})
        if work.get("source_state_sha256") != EXPECTED_SOURCE_STATE_SHA256:
            raise RuntimeError("checkpoint-5499 resumable state source mismatch")
        if int(work.get("target_node_evaluations", -1)) != arguments.target_node_evaluations:
            raise RuntimeError("checkpoint-5499 target count changed after start")
    else:
        WORK.mkdir(parents=True, exist_ok=True)
        state = carry_forward_state(source, arguments.target_node_evaluations)
        base_5467.atomic_json(STATE, state, compact=True)
    started = time.perf_counter()
    processed_this_invocation = 0
    while (
        len(state["checkpoint_5499"]["records"]) < arguments.target_node_evaluations
        and state["stack"]
        and not state["unresolved"]
    ):
        if processed_this_invocation and time.perf_counter() - started >= arguments.max_runtime_seconds:
            break
        state = process_atomic_node(
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
        )
        processed_this_invocation += 1
    records = list(state["checkpoint_5499"]["records"])
    counts = (len(state["accepted"]), len(state["stack"]), len(state["unresolved"]))
    partition_error = abs(
        base_5498.exact_partition_volume(state)
        - base_5498.exact_node_volume(state["root"])
    )
    source_v58_applications = len(source.get("v58_certificate_application_audit_rows", []))
    current_v58_applications = len(state.get("v58_certificate_application_audit_rows", []))
    new_v58_applications = current_v58_applications - source_v58_applications
    carry = state["checkpoint_5499"]
    formalization_after = base_5467.formalization_snapshot()
    validations = [
        check("all_sources_exist", not missing, len(paths)),
        check("checkpoint_5498_evidence_is_hash_locked", inherited_hashes == expected_hashes, inherited_hashes),
        check("checkpoint_5498_frontier_is_certified", source_certified, result_5498.get("decision")),
        check("source_frontier_is_exact_179_4_0", source_counts == EXPECTED_SOURCE_COUNTS, source_counts),
        check("source_pending_order_is_exact", source_paths_pending == EXPECTED_SOURCE_PENDING_PATHS, source_paths_pending),
        check("parent_v58_reconstructs_at_signed_revision", parent_v58.REVISION == PARENT_V58_REVISION and not parent_v58.V58_PARENT_ACTION_CHANGED and parent_v58.V58_ONLY_ENCLOSURE_COMPOSITION_CHANGED, parent_v58.REVISION),
        check("at_least_one_and_at_most_two_nodes_are_committed", 1 <= len(records) <= arguments.target_node_evaluations, len(records)),
        check("first_consumed_path_is_exact", records and records[0]["refinement_path"] == EXPECTED_FIRST_PATH, records[0]["refinement_path"] if records else "NONE"),
        check("node_count_increments_match_records", int(state["node_evaluation_count"]) == int(source["node_evaluation_count"]) + len(records) and int(state["v58_node_evaluation_count"]) == int(source["v58_node_evaluation_count"]) + len(records), state["node_evaluation_count"]),
        check("atomic_records_replay_exactly", replay_records(source, state), len(records)),
        check("source_append_only_ledgers_are_preserved", state["accepted"][: len(source["accepted"])] == source["accepted"] and state["refinement_witnesses"][: len(source["refinement_witnesses"])] == source["refinement_witnesses"] and state["unresolved"][: len(source["unresolved"])] == source["unresolved"], "accepted/witness/unresolved prefixes"),
        check("source_hash_ledger_is_current", carry["source_accepted_sha256"] == canonical_digest(source["accepted"]) and carry["source_pending_sha256"] == canonical_digest(source["stack"]) and carry["source_refinement_witnesses_sha256"] == canonical_digest(source["refinement_witnesses"]), carry["source_state_sha256"]),
        check("v58_certificate_does_not_leak_outside_binding", new_v58_applications == 0 and sum(int(row["new_audit_counts"]["v58_certificate_application_audit_rows"]) for row in records) == 0, new_v58_applications),
        check("frontier_count_fields_are_coherent", int(state["accepted_subcuboid_count"]) == counts[0] and int(state["pending_subcuboid_count"]) == counts[1] and int(state["unresolved_subcuboid_count"]) == counts[2], counts),
        check("exact_partition_volume_is_preserved", partition_error == 0, float(partition_error)),
        check("formalization_workbench_untouched", before_formalization == formalization_after, f"before={len(before_formalization)};after={len(formalization_after)}"),
        check("broad_claims_remain_false", not state["valid_for_parent_v58_active_cuboid"] and not state["valid_for_full_outer_parent_leaf_enclosure"] and not state["valid_for_D4_event_local_W3_bound"] and not state["valid_for_all_operator_local_GR_claim"] and not state["valid_for_full_MTS_claim"], "partial frontier"),
    ]
    failed = [row for row in validations if not row["passed"]]
    target_reached = len(records) == arguments.target_node_evaluations
    decision = (
        "PARENT_V58_TWO_NODE_FRONTIER_CERTIFIED__INTERPRET_NEXT_OBSTRUCTION"
        if not failed and target_reached and not state["unresolved"]
        else (
            "PARENT_V58_RESUMABLE_FRONTIER_CERTIFIED__DERIVE_LOCAL_REPAIR"
            if not failed and state["unresolved"]
            else (
                "PARENT_V58_RESUMABLE_FRONTIER_PARTIAL__RESUME"
                if not failed
                else "PARENT_V58_RESUMABLE_FRONTIER_NOT_CERTIFIED"
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
        "processed_this_invocation": processed_this_invocation,
        "evaluated_paths": [row["refinement_path"] for row in records],
        "node_outcomes": [row["outcome"] for row in records],
        "accepted_subcuboid_count": counts[0],
        "pending_subcuboid_count": counts[1],
        "unresolved_subcuboid_count": counts[2],
        "node_evaluation_count": state["node_evaluation_count"],
        "v58_node_evaluation_count": state["v58_node_evaluation_count"],
        "new_v58_application_count": new_v58_applications,
        "partition_volume_error": float(partition_error),
        "validation_row_count": len(validations),
        "failed_validation_count": len(failed),
        "valid_for_parent_v58_resumable_frontier": not failed,
        "valid_for_parent_v58_active_cuboid": False,
        "valid_for_full_outer_parent_leaf_enclosure": False,
        "valid_for_D4_event_local_W3_bound": False,
        "valid_for_all_operator_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
        "next_target": state["stack"][-1]["refinement_path"] if state["stack"] and not state["unresolved"] else "DERIVE_LOCAL_REPAIR",
    }
    node_rows = [
        {
            **{key: value for key, value in row.items() if key not in {"counts_before", "counts_after", "new_audit_counts", "child_paths"}},
            "child_paths": "|".join(row["child_paths"]),
            "counts_before": json.dumps(row["counts_before"], sort_keys=True, separators=(",", ":")),
            "counts_after": json.dumps(row["counts_after"], sort_keys=True, separators=(",", ":")),
            "new_audit_counts": json.dumps(row["new_audit_counts"], sort_keys=True, separators=(",", ":")),
        }
        for row in records
    ]
    base_5467.atomic_csv(NODE_AUDIT, node_rows)
    for state_key, _, output_path in AUDIT_BINDINGS:
        if state.get(state_key):
            base_5467.atomic_csv(output_path, state[state_key])
    base_5467.atomic_csv(
        SOURCE_REGISTER,
        [{"source_path": str(path), "sha256": digest(path), "exists": path.is_file()} for path in paths],
    )
    base_5467.atomic_csv(VALIDATION, validations)
    base_5467.atomic_json(STATUS, payload)
    base_5467.atomic_json(RESULT, payload)
    render_document(payload, records, base_5467)
    print(
        json.dumps(
            {
                key: payload[key]
                for key in (
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
                )
            },
            indent=2,
        )
    )
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
