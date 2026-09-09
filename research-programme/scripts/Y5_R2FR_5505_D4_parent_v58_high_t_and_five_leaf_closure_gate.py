from __future__ import annotations

import argparse
import importlib.util
import json
import math
from copy import deepcopy
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path
from typing import Any


POST = Path(__file__).resolve().parents[1]
SCRIPTS = POST / "scripts"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
OUTPUT = FUNCTIONAL_RG / "5505"
WORK = OUTPUT / "work-v1"

SCRIPT_5504 = SCRIPTS / "Y5_R2FR_5504_D4_parent_v58_low_t_child_gate.py"
SOURCE_STATE = FUNCTIONAL_RG / "5504" / "work-v1" / "E07__U051__RIGHT_CONNECTOR__CUBOID__6df3d70a73e4618b.json"
RESULT_5504 = FUNCTIONAL_RG / "5504" / "D4_parent_v58_low_t_child_result.json"
VALIDATION_5504 = FUNCTIONAL_RG / "5504" / "P8_Y5_BRR5503_5504_VALIDATION.csv"
SOURCE_REGISTER_5504 = FUNCTIONAL_RG / "5504" / "source_register.csv"
NODE_AUDIT_5504 = FUNCTIONAL_RG / "5504" / "D4_parent_v58_low_t_child_audit.csv"
CERTIFICATE_5496 = FUNCTIONAL_RG / "5496" / "D4_parent_v58_adaptive_complete_amplitude_certificate.json"

TARGET_CUBOID_ID = "E07__U051__RIGHT_CONNECTOR__CUBOID__6df3d70a73e4618b"
STATE = WORK / f"{TARGET_CUBOID_ID}.json"
NODE_AUDIT = OUTPUT / "D4_parent_v58_high_t_child_audit.csv"
UNION_AUDIT = OUTPUT / "D4_parent_v58_two_and_five_leaf_union_audit.csv"
V58_AUDIT = OUTPUT / "D4_parent_v58_frontier_certificate_application_audit.csv"
V57_AUDIT = OUTPUT / "D4_parent_v58_frontier_scoped_certificate_audit.csv"
JACOBIAN_XT_AUDIT = OUTPUT / "D4_parent_v58_frontier_collision_jacobian_xt_audit.csv"
STABLE_XT_AUDIT = OUTPUT / "D4_parent_v58_frontier_stable_edge_xt_audit.csv"
PIVOT_AUDIT = OUTPUT / "D4_parent_v58_frontier_first_spinor_pivot_audit.csv"
STABLE_T_AUDIT = OUTPUT / "D4_parent_v58_frontier_stable_edge_t_audit.csv"
JACOBIAN_T_AUDIT = OUTPUT / "D4_parent_v58_frontier_collision_jacobian_t_audit.csv"
SOURCE_REGISTER = OUTPUT / "source_register.csv"
VALIDATION = OUTPUT / "P8_Y5_BRR5504_5505_VALIDATION.csv"
STATUS = OUTPUT / "status.json"
RESULT = OUTPUT / "D4_parent_v58_high_t_and_five_leaf_closure_result.json"
DOCUMENT = POST / "5505-Y5-R2FR-D4-parent-v58-high-t-and-five-leaf-closure-gate.md"

CHECKPOINT = 5505
REVISION = "D4-parent-v58-high-t-and-five-leaf-closure-v1"
PARENT_V58_REVISION = "D4-deformed-contour-regular-away-W3-v58-adaptive-stable-edge-local-T2-union"
LOW_T_PATH = "R_E0S_E0S_E1S_X0S_X1S_T0S"
EXPECTED_PATH = "R_E0S_E0S_E1S_X0S_X1S_T1S"
T2_PARENT_PATH = "R_E0S_E0S_E1S_X0S_X1S"
X_REGION_PARENT_PATH = "R_E0S_E0S_E1S_X0S"
THREE_LEAF_PATHS = {
    "R_E0S_E0S_E1S_X0S_X0S_T0S_X0S",
    "R_E0S_E0S_E1S_X0S_X0S_T0S_X1S",
    "R_E0S_E0S_E1S_X0S_X0S_T1S",
}
FIVE_LEAF_PATHS = THREE_LEAF_PATHS | {LOW_T_PATH, EXPECTED_PATH}
EXPECTED_PENDING_PATHS = (
    "R_E1S",
    "R_E0S_E1S",
    "R_E0S_E0S_E1S_X1S",
    EXPECTED_PATH,
)
EXPECTED_SOURCE_COUNTS = (183, 4, 0)
EXPECTED_SOURCE_WITNESSES = 64
EXPECTED_SCRIPT_5504_SHA256 = "e98781b737fcbf3cfe64f009d8f65040840d6cab3fc834e84fd77b888abc39b9"
EXPECTED_SOURCE_STATE_SHA256 = "74ed505b52d668d1719e99f8c992e255b6c94dd6edf266afe265f90bbb63f02d"
EXPECTED_RESULT_5504_SHA256 = "e561f8368eebf30653a6a39e6920868054f01129cb52d8baf4885683a839ce2d"
EXPECTED_VALIDATION_5504_SHA256 = "5d16b27dde44ee02a95a06336256fd4d2ad3c68aab7581ace2c47a28e08a9bc1"
EXPECTED_SOURCE_REGISTER_5504_SHA256 = "9e496ff443353ccedec32bc4feb82b44a9f85abcafc6e9b67eca413868bf1e24"
EXPECTED_NODE_AUDIT_5504_SHA256 = "2708abd28221505d797b6b46269d2ef3acde82ec83a97ba8cbd92b47745cc27a"
EXPECTED_CERTIFICATE_5496_SHA256 = "27dc7fce1f83b424e9d9341778a392b83ed7c8659d12e05afd561338782fc708"

METRIC_FIELDS = (
    "integrated_regular_path_abs_upper",
    "minimum_amplitude_denominator_abs_lower",
    "relative_root_abs_lower",
    "selected_global_root_abs_lower",
    "collision_jacobian_abs_lower",
    "path_integral_enclosure_method",
)

AUDIT_BINDINGS = (
    ("v58_certificate_application_audit_rows", V58_AUDIT),
    ("v57_scoped_certificate_audit_rows", V57_AUDIT),
    ("v56_collision_jacobian_xt_audit_rows", JACOBIAN_XT_AUDIT),
    ("v56_stable_edge_xt_audit_rows", STABLE_XT_AUDIT),
    ("v56_first_spinor_pivot_audit_rows", PIVOT_AUDIT),
    ("v56_stable_edge_t_audit_rows", STABLE_T_AUDIT),
    ("v56_collision_jacobian_t_audit_rows", JACOBIAN_T_AUDIT),
)


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise ImportError(f"cannot load {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def check(gate: str, passed: bool, evidence: Any) -> dict[str, Any]:
    return {"checkpoint": CHECKPOINT, "validation_gate": gate, "passed": bool(passed), "evidence": evidence}


def source_paths(
    base_5504: Any,
    base_5503: Any,
    base_5502: Any,
    base_5501: Any,
    base_5500: Any,
    base_5499: Any,
    base_5498: Any,
    base_5496: Any,
    base_5495: Any,
) -> tuple[Path, ...]:
    return tuple(dict.fromkeys((
        Path(__file__).resolve(),
        *base_5504.source_paths(base_5503, base_5502, base_5501, base_5500, base_5499, base_5498, base_5496, base_5495),
        SCRIPT_5504,
        SOURCE_STATE,
        RESULT_5504,
        VALIDATION_5504,
        SOURCE_REGISTER_5504,
        NODE_AUDIT_5504,
        CERTIFICATE_5496,
    )))


def carry_forward(base_5499: Any, source: dict[str, Any]) -> dict[str, Any]:
    state = deepcopy(source)
    state["checkpoint"] = CHECKPOINT
    state["revision"] = REVISION
    state["parent_revision"] = PARENT_V58_REVISION
    state["checkpoint_5505"] = {
        "source_state_path": str(SOURCE_STATE),
        "source_state_sha256": EXPECTED_SOURCE_STATE_SHA256,
        "source_accepted_sha256": base_5499.canonical_digest(source["accepted"]),
        "source_pending_sha256": base_5499.canonical_digest(source["stack"]),
        "source_unresolved_sha256": base_5499.canonical_digest(source["unresolved"]),
        "source_refinement_witnesses_sha256": base_5499.canonical_digest(source["refinement_witnesses"]),
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


def exact_union(
    base_5498: Any,
    base_5503: Any,
    state: dict[str, Any],
    parent_path: str,
    leaf_paths: set[str],
) -> dict[str, Any]:
    leaves = [row for row in state["accepted"] if row.get("refinement_path") in leaf_paths]
    parents = [row for row in state["refinement_witnesses"] if row.get("refinement_path") == parent_path]
    if len(leaves) != len(leaf_paths) or len(parents) != 1:
        return {
            "parent_path": parent_path,
            "expected_leaf_count": len(leaf_paths),
            "actual_leaf_count": len(leaves),
            "closure": False,
            "volume_error": math.nan,
            "integrated_regular_path_abs_upper": math.nan,
            "minimum_amplitude_denominator_abs_lower": math.nan,
            "collision_jacobian_abs_lower": math.nan,
        }
    volume_error = abs(
        sum((base_5498.exact_node_volume(row) for row in leaves), start=Fraction(0))
        - base_5498.exact_node_volume(parents[0])
    )
    disjoint = all(
        not base_5503.boxes_overlap(base_5498, left, right)
        for index, left in enumerate(leaves)
        for right in leaves[index + 1 :]
    )
    return {
        "parent_path": parent_path,
        "expected_leaf_count": len(leaf_paths),
        "actual_leaf_count": len(leaves),
        "closure": volume_error == 0 and disjoint,
        "volume_error": float(volume_error),
        "pairwise_interior_disjoint": disjoint,
        "integrated_regular_path_abs_upper": sum(float(row["integrated_regular_path_abs_upper"]) for row in leaves),
        "minimum_amplitude_denominator_abs_lower": min(float(row["minimum_amplitude_denominator_abs_lower"]) for row in leaves),
        "collision_jacobian_abs_lower": min(float(row["collision_jacobian_abs_lower"]) for row in leaves),
    }


def render_document(payload: dict[str, Any], base_5467: Any) -> None:
    lines = [
        "# 5505: D4 parent-v58 high-t and five-leaf closure gate",
        "",
        "Checkpoint 5504 is hash locked. Exactly the matching high-t sibling is evaluated under unchanged parent v58.",
        "",
        f"Outcome: `{payload['node_outcome']}` in `{payload['node_runtime_seconds']}` seconds. Frontier: `{payload['accepted_subcuboid_count']}/{payload['pending_subcuboid_count']}/{payload['unresolved_subcuboid_count']}`.",
        "",
        f"Two-leaf parent closure: `{payload['exact_two_leaf_parent_closure']}`. Five-leaf x-region closure: `{payload['exact_five_leaf_x_region_closure']}`.",
        "",
        f"Five-leaf denominator lower: `{payload['five_leaf_union_amplitude_denominator_abs_lower']}`. Five-leaf Jacobian lower: `{payload['five_leaf_union_collision_jacobian_abs_lower']}`.",
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
    parser.add_argument("--maximum-refinement-depth", type=int, default=33)
    arguments = parser.parse_args()

    base_5504 = load_module("mts_5504_for_5505", SCRIPT_5504)
    base_5503 = load_module("mts_5503_for_5505", base_5504.SCRIPT_5503)
    base_5502 = load_module("mts_5502_for_5505", base_5503.SCRIPT_5502)
    base_5501 = load_module("mts_5501_for_5505", base_5502.SCRIPT_5501)
    base_5500 = load_module("mts_5500_for_5505", base_5501.SCRIPT_5500)
    base_5499 = load_module("mts_5499_for_5505", base_5500.SCRIPT_5499)
    base_5498 = load_module("mts_5498_for_5505", base_5499.SCRIPT_5498)
    base_5496 = load_module("mts_5496_for_5505", base_5498.SCRIPT_5496)
    base_5495 = load_module("mts_5495_for_5505", base_5496.SCRIPT_5495)
    base_5467 = load_module("mts_5467_for_5505", base_5495.SCRIPT_5467)
    base_5468 = load_module("mts_5468_for_5505", base_5495.SCRIPT_5468)
    base_5469 = load_module("mts_5469_for_5505", base_5495.SCRIPT_5469)
    base_5472 = load_module("mts_5472_for_5505", base_5495.SCRIPT_5472)
    base_5474 = load_module("mts_5474_for_5505", base_5495.SCRIPT_5474)
    base_5476 = load_module("mts_5476_for_5505", base_5495.SCRIPT_5476)
    base_5478 = load_module("mts_5478_for_5505", base_5495.SCRIPT_5478)
    base_5480 = load_module("mts_5480_for_5505", base_5495.SCRIPT_5480)
    base_5483 = load_module("mts_5483_for_5505", base_5495.SCRIPT_5483)
    base_5490 = load_module("mts_5490_for_5505", base_5495.SCRIPT_5490)
    base_5493 = load_module("mts_5493_for_5505", base_5495.SCRIPT_5493)

    base_5467.set_below_normal_priority()
    base_5480.set_single_core_affinity()
    before_formalization = base_5467.formalization_snapshot()
    paths = source_paths(base_5504, base_5503, base_5502, base_5501, base_5500, base_5499, base_5498, base_5496, base_5495)
    missing = [str(path) for path in paths if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"missing sources: {missing}")

    inherited_hashes = {
        "script_5504": base_5499.digest(SCRIPT_5504),
        "source_state": base_5499.digest(SOURCE_STATE),
        "result_5504": base_5499.digest(RESULT_5504),
        "validation_5504": base_5499.digest(VALIDATION_5504),
        "source_register_5504": base_5499.digest(SOURCE_REGISTER_5504),
        "node_audit_5504": base_5499.digest(NODE_AUDIT_5504),
        "certificate_5496": base_5499.digest(CERTIFICATE_5496),
    }
    expected_hashes = {
        "script_5504": EXPECTED_SCRIPT_5504_SHA256,
        "source_state": EXPECTED_SOURCE_STATE_SHA256,
        "result_5504": EXPECTED_RESULT_5504_SHA256,
        "validation_5504": EXPECTED_VALIDATION_5504_SHA256,
        "source_register_5504": EXPECTED_SOURCE_REGISTER_5504_SHA256,
        "node_audit_5504": EXPECTED_NODE_AUDIT_5504_SHA256,
        "certificate_5496": EXPECTED_CERTIFICATE_5496_SHA256,
    }
    if inherited_hashes != expected_hashes:
        raise RuntimeError("checkpoint-5505 inherited source hash mismatch")

    source = base_5499.read_json(SOURCE_STATE)
    result_5504 = base_5499.read_json(RESULT_5504)
    validation_5504 = base_5499.read_csv(VALIDATION_5504)
    register_5504 = base_5499.read_csv(SOURCE_REGISTER_5504)
    certificate_5496 = base_5499.read_json(CERTIFICATE_5496)
    source_counts = (len(source["accepted"]), len(source["stack"]), len(source["unresolved"]))
    pending_paths = tuple(str(row["refinement_path"]) for row in source["stack"])
    source_certified = (
        result_5504.get("decision") == "PARENT_V58_LOW_T_LEAF_CERTIFIED__ADVANCE_HIGH_T"
        and result_5504.get("node_outcome") == "ACCEPTED"
        and result_5504.get("valid_for_parent_v58_low_t_child") is True
        and int(result_5504.get("failed_validation_count", -1)) == 0
        and all(base_5499.truth(row.get("passed")) for row in validation_5504)
        and base_5499.source_register_is_current(register_5504)
        and source_counts == EXPECTED_SOURCE_COUNTS
        and len(source["refinement_witnesses"]) == EXPECTED_SOURCE_WITNESSES
        and pending_paths == EXPECTED_PENDING_PATHS
        and base_5498.exact_partition_volume(source) == base_5498.exact_node_volume(source["root"])
    )
    if not source_certified:
        raise RuntimeError("checkpoint-5504 source is not current and certified")

    stable, _, cells, support_segments, branches = base_5467.load_parent()
    cuboid = next(row for row in base_5499.read_csv(base_5495.MANIFEST_5468) if row["cuboid_job_id"] == TARGET_CUBOID_ID)
    parent_v58 = base_5498.reconstruct_parent(
        base_5467, base_5472, base_5474, base_5476, base_5478, base_5483,
        base_5490, base_5493, base_5495, base_5496, certificate_5496,
    )

    if arguments.dry_run:
        print(json.dumps({
            "checkpoint": CHECKPOINT,
            "dry_run": True,
            "source_counts": list(source_counts),
            "source_witnesses": len(source["refinement_witnesses"]),
            "next_path": source["stack"][-1]["refinement_path"],
            "parent_revision": parent_v58.REVISION,
            "source_hashes_match": inherited_hashes == expected_hashes,
            "exact_source_partition": True,
        }, indent=2))
        return 0

    if STATE.is_file():
        state = base_5499.read_json(STATE)
        if state.get("checkpoint_5505", {}).get("source_state_sha256") != EXPECTED_SOURCE_STATE_SHA256:
            raise RuntimeError("checkpoint-5505 output source mismatch")
    else:
        WORK.mkdir(parents=True, exist_ok=True)
        state = carry_forward(base_5499, source)
        base_5467.atomic_json(STATE, state, compact=True)

    if not state["checkpoint_5505"]["records"]:
        state = base_5500.process_atomic_node(
            base_5499, base_5498, base_5467, base_5468, base_5469, stable,
            parent_v58, cells, support_segments, branches, cuboid, state,
            arguments.maximum_refinement_depth, "checkpoint_5505", STATE,
            "checkpoint_5505_parent_v58",
        )

    records = list(state["checkpoint_5505"]["records"])
    record = records[0]
    counts = (len(state["accepted"]), len(state["stack"]), len(state["unresolved"]))
    partition_error = abs(base_5498.exact_partition_volume(state) - base_5498.exact_node_volume(state["root"]))
    new_v58 = len(state.get("v58_certificate_application_audit_rows", [])) - len(source.get("v58_certificate_application_audit_rows", []))
    two_leaf = exact_union(base_5498, base_5503, state, T2_PARENT_PATH, {LOW_T_PATH, EXPECTED_PATH})
    five_leaf = exact_union(base_5498, base_5503, state, X_REGION_PARENT_PATH, FIVE_LEAF_PATHS)
    accepted_target = next((row for row in state["accepted"] if row.get("refinement_path") == EXPECTED_PATH), None)
    carry = state["checkpoint_5505"]
    after_formalization = base_5467.formalization_snapshot()
    accepted_metrics_positive = accepted_target is None or (
        math.isfinite(float(accepted_target["integrated_regular_path_abs_upper"]))
        and float(accepted_target["integrated_regular_path_abs_upper"]) > 0.0
        and all(math.isfinite(float(accepted_target[field])) and float(accepted_target[field]) > 0.0 for field in (
            "minimum_amplitude_denominator_abs_lower",
            "relative_root_abs_lower",
            "selected_global_root_abs_lower",
            "collision_jacobian_abs_lower",
        ))
    )

    validations = [
        check("all_sources_exist", not missing, len(paths)),
        check("checkpoint_5504_evidence_is_hash_locked", inherited_hashes == expected_hashes, inherited_hashes),
        check("checkpoint_5504_low_t_leaf_is_certified", source_certified, result_5504.get("decision")),
        check("source_frontier_is_exact_183_4_0", source_counts == EXPECTED_SOURCE_COUNTS, source_counts),
        check("source_pending_order_is_exact", pending_paths == EXPECTED_PENDING_PATHS, pending_paths),
        check("parent_v58_reconstructs_at_signed_revision", parent_v58.REVISION == PARENT_V58_REVISION and not parent_v58.V58_PARENT_ACTION_CHANGED and parent_v58.V58_ONLY_ENCLOSURE_COMPOSITION_CHANGED, parent_v58.REVISION),
        check("exactly_one_high_t_child_is_committed", len(records) == 1 and record["refinement_path"] == EXPECTED_PATH, record["refinement_path"]),
        check("node_count_increments_once", int(state["node_evaluation_count"]) == int(source["node_evaluation_count"]) + 1 and int(state["v58_node_evaluation_count"]) == int(source["v58_node_evaluation_count"]) + 1, state["node_evaluation_count"]),
        check("atomic_record_replays_exactly", base_5500.replay_records(source, state, "checkpoint_5505"), record["outcome"]),
        check("source_append_only_ledgers_are_preserved", state["accepted"][:len(source["accepted"])] == source["accepted"] and state["refinement_witnesses"][:len(source["refinement_witnesses"])] == source["refinement_witnesses"] and state["unresolved"][:len(source["unresolved"])] == source["unresolved"], "accepted/witness/unresolved prefixes"),
        check("source_hash_ledger_is_current", carry["source_accepted_sha256"] == base_5499.canonical_digest(source["accepted"]) and carry["source_pending_sha256"] == base_5499.canonical_digest(source["stack"]) and carry["source_refinement_witnesses_sha256"] == base_5499.canonical_digest(source["refinement_witnesses"]), carry["source_state_sha256"]),
        check("v58_certificate_does_not_leak_outside_binding", new_v58 == 0 and int(record["new_audit_counts"]["v58_certificate_application_audit_rows"]) == 0, new_v58),
        check("exact_partition_volume_is_preserved", partition_error == 0, float(partition_error)),
        check("accepted_target_metrics_are_finite_positive", accepted_metrics_positive, record["outcome"]),
        check("accepted_high_t_closes_exact_two_leaf_parent", record["outcome"] != "ACCEPTED" or (two_leaf["closure"] and two_leaf["volume_error"] == 0.0 and two_leaf["minimum_amplitude_denominator_abs_lower"] > 0.0 and two_leaf["collision_jacobian_abs_lower"] > 0.0), two_leaf),
        check("accepted_high_t_closes_exact_five_leaf_x_region", record["outcome"] != "ACCEPTED" or (five_leaf["closure"] and five_leaf["volume_error"] == 0.0 and five_leaf["minimum_amplitude_denominator_abs_lower"] > 0.0 and five_leaf["collision_jacobian_abs_lower"] > 0.0), five_leaf),
        check("formalization_workbench_untouched", before_formalization == after_formalization, f"before={len(before_formalization)};after={len(after_formalization)}"),
        check("broad_claims_remain_false", not state["valid_for_parent_v58_active_cuboid"] and not state["valid_for_full_outer_parent_leaf_enclosure"] and not state["valid_for_D4_event_local_W3_bound"] and not state["valid_for_all_operator_local_GR_claim"] and not state["valid_for_full_MTS_claim"], "one high-t child and finite unions"),
    ]
    failed = [row for row in validations if not row["passed"]]
    if failed:
        decision = "PARENT_V58_HIGH_T_OR_UNION_NOT_CERTIFIED"
    elif record["outcome"] == "ACCEPTED" and two_leaf["closure"] and five_leaf["closure"]:
        decision = "PARENT_V58_EXACT_FIVE_LEAF_X_REGION_CERTIFIED__ADVANCE_FRONTIER"
    elif str(record["outcome"]).startswith("REFINED_"):
        decision = "PARENT_V58_HIGH_T_CHILD_CERTIFIED__CONTINUE_REFINEMENT"
    else:
        decision = "PARENT_V58_HIGH_T_CHILD_UNRESOLVED__DERIVE_REPAIR"

    payload = {
        "checkpoint": CHECKPOINT,
        "revision": REVISION,
        "parent_revision": PARENT_V58_REVISION,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "decision": decision,
        "evaluated_path": record["refinement_path"],
        "node_outcome": record["outcome"],
        "node_probe_passed": record["probe_passed"],
        "node_failure_type": record["failure_type"],
        "node_failure_message": record["failure_message"],
        "node_child_paths": record["child_paths"],
        "node_runtime_seconds": record["runtime_seconds"],
        **{f"node_{field}": (accepted_target.get(field) if accepted_target is not None else math.nan) for field in METRIC_FIELDS},
        "accepted_subcuboid_count": counts[0],
        "pending_subcuboid_count": counts[1],
        "unresolved_subcuboid_count": counts[2],
        "refinement_witness_count": len(state["refinement_witnesses"]),
        "new_v58_application_count": new_v58,
        "partition_volume_error": float(partition_error),
        "exact_two_leaf_parent_closure": two_leaf["closure"],
        "two_leaf_parent_volume_error": two_leaf["volume_error"],
        "two_leaf_union_integrated_regular_path_abs_upper": two_leaf["integrated_regular_path_abs_upper"],
        "two_leaf_union_amplitude_denominator_abs_lower": two_leaf["minimum_amplitude_denominator_abs_lower"],
        "two_leaf_union_collision_jacobian_abs_lower": two_leaf["collision_jacobian_abs_lower"],
        "exact_five_leaf_x_region_closure": five_leaf["closure"],
        "five_leaf_x_region_volume_error": five_leaf["volume_error"],
        "five_leaf_union_integrated_regular_path_abs_upper": five_leaf["integrated_regular_path_abs_upper"],
        "five_leaf_union_amplitude_denominator_abs_lower": five_leaf["minimum_amplitude_denominator_abs_lower"],
        "five_leaf_union_collision_jacobian_abs_lower": five_leaf["collision_jacobian_abs_lower"],
        "validation_row_count": len(validations),
        "failed_validation_count": len(failed),
        "valid_for_parent_v58_high_t_child": not failed and record["outcome"] == "ACCEPTED",
        "valid_for_parent_v58_t2_parent": not failed and two_leaf["closure"],
        "valid_for_parent_v58_five_leaf_x_region": not failed and five_leaf["closure"],
        "valid_for_parent_v58_active_cuboid": False,
        "valid_for_full_outer_parent_leaf_enclosure": False,
        "valid_for_D4_event_local_W3_bound": False,
        "valid_for_all_operator_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
        "next_target": state["stack"][-1]["refinement_path"] if state["stack"] and not state["unresolved"] else "DERIVE_LOCAL_REPAIR",
    }
    accepted_fields = ({field: accepted_target.get(field) for field in METRIC_FIELDS} if accepted_target is not None else {})
    node_row = {
        **{key: value for key, value in record.items() if key not in {"counts_before", "counts_after", "new_audit_counts", "child_paths"}},
        **accepted_fields,
        "child_paths": "|".join(record["child_paths"]),
        "counts_before": json.dumps(record["counts_before"], sort_keys=True, separators=(",", ":")),
        "counts_after": json.dumps(record["counts_after"], sort_keys=True, separators=(",", ":")),
        "new_audit_counts": json.dumps(record["new_audit_counts"], sort_keys=True, separators=(",", ":")),
    }
    union_rows = [
        {"union_id": "two_leaf_t_parent", **two_leaf},
        {"union_id": "five_leaf_x_region", **five_leaf},
    ]
    base_5467.atomic_csv(NODE_AUDIT, [node_row])
    base_5467.atomic_csv(UNION_AUDIT, union_rows)
    for key, path in AUDIT_BINDINGS:
        if state.get(key):
            base_5467.atomic_csv(path, state[key])
    base_5467.atomic_csv(SOURCE_REGISTER, [{"source_path": str(path), "sha256": base_5499.digest(path), "exists": path.is_file()} for path in paths])
    base_5467.atomic_csv(VALIDATION, validations)
    base_5467.atomic_json(STATUS, payload)
    base_5467.atomic_json(RESULT, payload)
    render_document(payload, base_5467)
    print(json.dumps({key: payload[key] for key in (
        "decision", "evaluated_path", "node_outcome", "accepted_subcuboid_count",
        "pending_subcuboid_count", "unresolved_subcuboid_count",
        "exact_two_leaf_parent_closure", "exact_five_leaf_x_region_closure",
        "five_leaf_union_amplitude_denominator_abs_lower",
        "five_leaf_union_collision_jacobian_abs_lower", "new_v58_application_count",
        "partition_volume_error", "failed_validation_count", "next_target",
    )}, indent=2))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
