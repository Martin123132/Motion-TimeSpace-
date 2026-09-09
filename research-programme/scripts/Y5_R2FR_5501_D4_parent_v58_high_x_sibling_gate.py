from __future__ import annotations

import argparse
import importlib.util
import json
from copy import deepcopy
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path
from typing import Any


POST = Path(__file__).resolve().parents[1]
SCRIPTS = POST / "scripts"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
OUTPUT = FUNCTIONAL_RG / "5501"
WORK = OUTPUT / "work-v1"

SCRIPT_5500 = SCRIPTS / "Y5_R2FR_5500_D4_parent_v58_low_t_two_node_frontier_runner.py"
SOURCE_STATE = (
    FUNCTIONAL_RG
    / "5500"
    / "work-v1"
    / "E07__U051__RIGHT_CONNECTOR__CUBOID__6df3d70a73e4618b.json"
)
RESULT_5500 = FUNCTIONAL_RG / "5500" / "D4_parent_v58_low_t_two_node_result.json"
VALIDATION_5500 = FUNCTIONAL_RG / "5500" / "P8_Y5_BRR5499_5500_VALIDATION.csv"
SOURCE_REGISTER_5500 = FUNCTIONAL_RG / "5500" / "source_register.csv"
NODE_AUDIT_5500 = FUNCTIONAL_RG / "5500" / "D4_parent_v58_low_t_two_node_audit.csv"
CERTIFICATE_5496 = FUNCTIONAL_RG / "5496" / "D4_parent_v58_adaptive_complete_amplitude_certificate.json"

TARGET_CUBOID_ID = "E07__U051__RIGHT_CONNECTOR__CUBOID__6df3d70a73e4618b"
STATE = WORK / f"{TARGET_CUBOID_ID}.json"
NODE_AUDIT = OUTPUT / "D4_parent_v58_high_x_sibling_audit.csv"
V58_AUDIT = OUTPUT / "D4_parent_v58_frontier_certificate_application_audit.csv"
V57_AUDIT = OUTPUT / "D4_parent_v58_frontier_scoped_certificate_audit.csv"
JACOBIAN_XT_AUDIT = OUTPUT / "D4_parent_v58_frontier_collision_jacobian_xt_audit.csv"
STABLE_XT_AUDIT = OUTPUT / "D4_parent_v58_frontier_stable_edge_xt_audit.csv"
PIVOT_AUDIT = OUTPUT / "D4_parent_v58_frontier_first_spinor_pivot_audit.csv"
STABLE_T_AUDIT = OUTPUT / "D4_parent_v58_frontier_stable_edge_t_audit.csv"
JACOBIAN_T_AUDIT = OUTPUT / "D4_parent_v58_frontier_collision_jacobian_t_audit.csv"
SOURCE_REGISTER = OUTPUT / "source_register.csv"
VALIDATION = OUTPUT / "P8_Y5_BRR5500_5501_VALIDATION.csv"
STATUS = OUTPUT / "status.json"
RESULT = OUTPUT / "D4_parent_v58_high_x_sibling_result.json"
DOCUMENT = POST / "5501-Y5-R2FR-D4-parent-v58-high-x-sibling-gate.md"

CHECKPOINT = 5501
REVISION = "D4-parent-v58-high-x-sibling-gate-v1"
PARENT_V58_REVISION = "D4-deformed-contour-regular-away-W3-v58-adaptive-stable-edge-local-T2-union"
EXPECTED_PATH = "R_E0S_E0S_E1S_X0S_X0S_T0S_X1S"
LOW_X_PATH = "R_E0S_E0S_E1S_X0S_X0S_T0S_X0S"
LOW_T_PARENT_PATH = "R_E0S_E0S_E1S_X0S_X0S_T0S"
EXPECTED_PENDING_PATHS = (
    "R_E1S",
    "R_E0S_E1S",
    "R_E0S_E0S_E1S_X1S",
    "R_E0S_E0S_E1S_X0S_X1S",
    "R_E0S_E0S_E1S_X0S_X0S_T1S",
    EXPECTED_PATH,
)
EXPECTED_SOURCE_COUNTS = (180, 6, 0)
EXPECTED_SOURCE_WITNESSES = 63
EXPECTED_SCRIPT_5500_SHA256 = "730d3e3f13b8302d323ea488eca6513c0e7c29a37e3f29f6ab1458ef88f98f94"
EXPECTED_SOURCE_STATE_SHA256 = "b916d268ac3c6466c46b53d9fa597feab86ae37d8d8584731c6c3fd248d05e8e"
EXPECTED_RESULT_5500_SHA256 = "823765b7974953217d80244db8a39ee9bc4b1a04d525496457a9f828f7df82ac"
EXPECTED_VALIDATION_5500_SHA256 = "c0a11f710f2d2437de7206ecee43b334b76451e44fbfc9ddc72fd96ab10c3ac7"
EXPECTED_SOURCE_REGISTER_5500_SHA256 = "daf9497593c5b2b789db2d60902c9b226654f714d145f6b61be5f406d098cbca"
EXPECTED_NODE_AUDIT_5500_SHA256 = "4e8f59a1308b873e61475a7d2e94e588470f1aea606db2771efd2801f28a1701"
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


def source_paths(
    base_5500: Any,
    base_5499: Any,
    base_5498: Any,
    base_5496: Any,
    base_5495: Any,
) -> tuple[Path, ...]:
    return tuple(
        dict.fromkeys(
            (
                Path(__file__).resolve(),
                *base_5500.source_paths(base_5499, base_5498, base_5496, base_5495),
                SCRIPT_5500,
                SOURCE_STATE,
                RESULT_5500,
                VALIDATION_5500,
                SOURCE_REGISTER_5500,
                NODE_AUDIT_5500,
                CERTIFICATE_5496,
            )
        )
    )


def carry_forward(base_5499: Any, source: dict[str, Any]) -> dict[str, Any]:
    state = deepcopy(source)
    state["checkpoint"] = CHECKPOINT
    state["revision"] = REVISION
    state["parent_revision"] = PARENT_V58_REVISION
    state["checkpoint_5501"] = {
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


def exact_two_child_closure(
    base_5498: Any,
    state: dict[str, Any],
) -> tuple[bool, float, float, float]:
    rows = [
        row
        for row in state["accepted"]
        if row.get("refinement_path") in {LOW_X_PATH, EXPECTED_PATH}
    ]
    parent = next(
        row
        for row in state["refinement_witnesses"]
        if row.get("refinement_path") == LOW_T_PARENT_PATH
    )
    if len(rows) != 2:
        return False, float("nan"), float("nan"), float("nan")
    volume_error = abs(
        sum((base_5498.exact_node_volume(row) for row in rows), start=Fraction(0))
        - base_5498.exact_node_volume(parent)
    )
    interiors_disjoint = not all(
        min(
            base_5498.exact_coordinate(rows[0][upper]),
            base_5498.exact_coordinate(rows[1][upper]),
        )
        > max(
            base_5498.exact_coordinate(rows[0][lower]),
            base_5498.exact_coordinate(rows[1][lower]),
        )
        for lower, upper in (
            ("epsilon_real_lower", "epsilon_real_upper"),
            ("x_lower", "x_upper"),
            ("t_lower", "t_upper"),
        )
    )
    closure = volume_error == 0 and interiors_disjoint
    return (
        closure,
        float(volume_error),
        min(float(row["minimum_amplitude_denominator_abs_lower"]) for row in rows),
        min(float(row["collision_jacobian_abs_lower"]) for row in rows),
    )


def render_document(payload: dict[str, Any], base_5467: Any) -> None:
    lines = [
        "# 5501: D4 parent-v58 high-x sibling gate",
        "",
        "The checkpoint-5500 frontier is hash locked and the exact high-x sibling of its accepted low-x leaf is evaluated once under unchanged parent v58.",
        "",
        f"Sibling outcome: `{payload['node_outcome']}` in `{payload['node_runtime_seconds']}` seconds. Frontier: `{payload['accepted_subcuboid_count']}/{payload['pending_subcuboid_count']}/{payload['unresolved_subcuboid_count']}`.",
        "",
        f"Exact two-child low-t closure: `{payload['exact_low_t_parent_closure']}`. Union amplitude-denominator lower: `{payload['low_t_union_amplitude_denominator_abs_lower']}`. Union collision-Jacobian lower: `{payload['low_t_union_collision_jacobian_abs_lower']}`.",
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
    base_5500 = load_module("mts_5500_for_5501", SCRIPT_5500)
    base_5499 = load_module("mts_5499_for_5501", base_5500.SCRIPT_5499)
    base_5498 = load_module("mts_5498_for_5501", base_5499.SCRIPT_5498)
    base_5496 = load_module("mts_5496_for_5501", base_5498.SCRIPT_5496)
    base_5495 = load_module("mts_5495_for_5501", base_5496.SCRIPT_5495)
    base_5467 = load_module("mts_5467_for_5501", base_5495.SCRIPT_5467)
    base_5468 = load_module("mts_5468_for_5501", base_5495.SCRIPT_5468)
    base_5469 = load_module("mts_5469_for_5501", base_5495.SCRIPT_5469)
    base_5472 = load_module("mts_5472_for_5501", base_5495.SCRIPT_5472)
    base_5474 = load_module("mts_5474_for_5501", base_5495.SCRIPT_5474)
    base_5476 = load_module("mts_5476_for_5501", base_5495.SCRIPT_5476)
    base_5478 = load_module("mts_5478_for_5501", base_5495.SCRIPT_5478)
    base_5480 = load_module("mts_5480_for_5501", base_5495.SCRIPT_5480)
    base_5483 = load_module("mts_5483_for_5501", base_5495.SCRIPT_5483)
    base_5490 = load_module("mts_5490_for_5501", base_5495.SCRIPT_5490)
    base_5493 = load_module("mts_5493_for_5501", base_5495.SCRIPT_5493)
    base_5467.set_below_normal_priority()
    base_5480.set_single_core_affinity()
    before_formalization = base_5467.formalization_snapshot()
    paths = source_paths(base_5500, base_5499, base_5498, base_5496, base_5495)
    missing = [str(path) for path in paths if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"missing sources: {missing}")
    inherited_hashes = {
        "script_5500": base_5499.digest(SCRIPT_5500),
        "source_state": base_5499.digest(SOURCE_STATE),
        "result_5500": base_5499.digest(RESULT_5500),
        "validation_5500": base_5499.digest(VALIDATION_5500),
        "source_register_5500": base_5499.digest(SOURCE_REGISTER_5500),
        "node_audit_5500": base_5499.digest(NODE_AUDIT_5500),
        "certificate_5496": base_5499.digest(CERTIFICATE_5496),
    }
    expected_hashes = {
        "script_5500": EXPECTED_SCRIPT_5500_SHA256,
        "source_state": EXPECTED_SOURCE_STATE_SHA256,
        "result_5500": EXPECTED_RESULT_5500_SHA256,
        "validation_5500": EXPECTED_VALIDATION_5500_SHA256,
        "source_register_5500": EXPECTED_SOURCE_REGISTER_5500_SHA256,
        "node_audit_5500": EXPECTED_NODE_AUDIT_5500_SHA256,
        "certificate_5496": EXPECTED_CERTIFICATE_5496_SHA256,
    }
    if inherited_hashes != expected_hashes:
        raise RuntimeError("checkpoint-5501 inherited source hash mismatch")
    source = base_5499.read_json(SOURCE_STATE)
    result_5500 = base_5499.read_json(RESULT_5500)
    validation_5500 = base_5499.read_csv(VALIDATION_5500)
    register_5500 = base_5499.read_csv(SOURCE_REGISTER_5500)
    certificate_5496 = base_5499.read_json(CERTIFICATE_5496)
    source_counts = (len(source["accepted"]), len(source["stack"]), len(source["unresolved"]))
    pending_paths = tuple(str(row["refinement_path"]) for row in source["stack"])
    source_certified = (
        result_5500.get("decision") == "PARENT_V58_LOW_T_TWO_NODE_FRONTIER_CERTIFIED__CHOOSE_NEXT_ROUTE"
        and int(result_5500.get("failed_validation_count", -1)) == 0
        and all(base_5499.truth(row.get("passed")) for row in validation_5500)
        and base_5499.source_register_is_current(register_5500)
        and source_counts == EXPECTED_SOURCE_COUNTS
        and len(source["refinement_witnesses"]) == EXPECTED_SOURCE_WITNESSES
        and pending_paths == EXPECTED_PENDING_PATHS
        and base_5498.exact_partition_volume(source) == base_5498.exact_node_volume(source["root"])
    )
    if not source_certified:
        raise RuntimeError("checkpoint-5500 source is not current and certified")
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
            "next_path": source["stack"][-1]["refinement_path"],
            "parent_revision": parent_v58.REVISION,
            "source_hashes_match": inherited_hashes == expected_hashes,
            "exact_source_partition": True,
        }, indent=2))
        return 0
    if STATE.is_file():
        state = base_5499.read_json(STATE)
        if state.get("checkpoint_5501", {}).get("source_state_sha256") != EXPECTED_SOURCE_STATE_SHA256:
            raise RuntimeError("checkpoint-5501 output source mismatch")
    else:
        WORK.mkdir(parents=True, exist_ok=True)
        state = carry_forward(base_5499, source)
        base_5467.atomic_json(STATE, state, compact=True)
    if not state["checkpoint_5501"]["records"]:
        state = base_5500.process_atomic_node(
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
            "checkpoint_5501",
            STATE,
            "checkpoint_5501_parent_v58",
        )
    records = list(state["checkpoint_5501"]["records"])
    record = records[0]
    counts = (len(state["accepted"]), len(state["stack"]), len(state["unresolved"]))
    partition_error = abs(base_5498.exact_partition_volume(state) - base_5498.exact_node_volume(state["root"]))
    new_v58 = len(state.get("v58_certificate_application_audit_rows", [])) - len(source.get("v58_certificate_application_audit_rows", []))
    closure, closure_error, denominator_lower, jacobian_lower = exact_two_child_closure(base_5498, state)
    carry = state["checkpoint_5501"]
    after_formalization = base_5467.formalization_snapshot()
    validations = [
        check("all_sources_exist", not missing, len(paths)),
        check("checkpoint_5500_evidence_is_hash_locked", inherited_hashes == expected_hashes, inherited_hashes),
        check("checkpoint_5500_frontier_is_certified", source_certified, result_5500.get("decision")),
        check("source_frontier_is_exact_180_6_0", source_counts == EXPECTED_SOURCE_COUNTS, source_counts),
        check("source_pending_order_is_exact", pending_paths == EXPECTED_PENDING_PATHS, pending_paths),
        check("parent_v58_reconstructs_at_signed_revision", parent_v58.REVISION == PARENT_V58_REVISION and not parent_v58.V58_PARENT_ACTION_CHANGED and parent_v58.V58_ONLY_ENCLOSURE_COMPOSITION_CHANGED, parent_v58.REVISION),
        check("exactly_one_high_x_sibling_is_committed", len(records) == 1 and record["refinement_path"] == EXPECTED_PATH, record["refinement_path"]),
        check("node_count_increments_once", int(state["node_evaluation_count"]) == int(source["node_evaluation_count"]) + 1 and int(state["v58_node_evaluation_count"]) == int(source["v58_node_evaluation_count"]) + 1, state["node_evaluation_count"]),
        check("atomic_record_replays_exactly", base_5500.replay_records(source, state, "checkpoint_5501"), record["outcome"]),
        check("source_append_only_ledgers_are_preserved", state["accepted"][: len(source["accepted"])] == source["accepted"] and state["refinement_witnesses"][: len(source["refinement_witnesses"])] == source["refinement_witnesses"] and state["unresolved"][: len(source["unresolved"])] == source["unresolved"], "accepted/witness/unresolved prefixes"),
        check("source_hash_ledger_is_current", carry["source_accepted_sha256"] == base_5499.canonical_digest(source["accepted"]) and carry["source_pending_sha256"] == base_5499.canonical_digest(source["stack"]) and carry["source_refinement_witnesses_sha256"] == base_5499.canonical_digest(source["refinement_witnesses"]), carry["source_state_sha256"]),
        check("v58_certificate_does_not_leak_outside_binding", new_v58 == 0 and int(record["new_audit_counts"]["v58_certificate_application_audit_rows"]) == 0, new_v58),
        check("exact_partition_volume_is_preserved", partition_error == 0, float(partition_error)),
        check("low_t_closure_is_only_claimed_if_both_siblings_pass", not closure or (record["outcome"] == "ACCEPTED" and closure_error == 0.0 and denominator_lower > 0.0 and jacobian_lower > 0.0), closure),
        check("formalization_workbench_untouched", before_formalization == after_formalization, f"before={len(before_formalization)};after={len(after_formalization)}"),
        check("broad_claims_remain_false", not state["valid_for_parent_v58_active_cuboid"] and not state["valid_for_full_outer_parent_leaf_enclosure"] and not state["valid_for_D4_event_local_W3_bound"] and not state["valid_for_all_operator_local_GR_claim"] and not state["valid_for_full_MTS_claim"], "one sibling only"),
    ]
    failed = [row for row in validations if not row["passed"]]
    decision = (
        "PARENT_V58_LOW_T_EXACT_X2_UNION_CERTIFIED__ADVANCE_HIGH_T"
        if not failed and closure
        else (
            "PARENT_V58_HIGH_X_SIBLING_CERTIFIED__CONTINUE_REFINEMENT"
            if not failed
            else "PARENT_V58_HIGH_X_SIBLING_NOT_CERTIFIED"
        )
    )
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
        "accepted_subcuboid_count": counts[0],
        "pending_subcuboid_count": counts[1],
        "unresolved_subcuboid_count": counts[2],
        "new_v58_application_count": new_v58,
        "partition_volume_error": float(partition_error),
        "exact_low_t_parent_closure": closure,
        "low_t_parent_volume_error": closure_error,
        "low_t_union_amplitude_denominator_abs_lower": denominator_lower,
        "low_t_union_collision_jacobian_abs_lower": jacobian_lower,
        "validation_row_count": len(validations),
        "failed_validation_count": len(failed),
        "valid_for_parent_v58_high_x_sibling": not failed,
        "valid_for_parent_v58_low_t_parent": not failed and closure,
        "valid_for_parent_v58_active_cuboid": False,
        "valid_for_full_outer_parent_leaf_enclosure": False,
        "valid_for_D4_event_local_W3_bound": False,
        "valid_for_all_operator_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
        "next_target": state["stack"][-1]["refinement_path"] if state["stack"] and not state["unresolved"] else "DERIVE_LOCAL_REPAIR",
    }
    node_row = {
        **{key: value for key, value in record.items() if key not in {"counts_before", "counts_after", "new_audit_counts", "child_paths"}},
        "child_paths": "|".join(record["child_paths"]),
        "counts_before": json.dumps(record["counts_before"], sort_keys=True, separators=(",", ":")),
        "counts_after": json.dumps(record["counts_after"], sort_keys=True, separators=(",", ":")),
        "new_audit_counts": json.dumps(record["new_audit_counts"], sort_keys=True, separators=(",", ":")),
    }
    base_5467.atomic_csv(NODE_AUDIT, [node_row])
    for key, _, path in AUDIT_BINDINGS:
        if state.get(key):
            base_5467.atomic_csv(path, state[key])
    base_5467.atomic_csv(SOURCE_REGISTER, [{"source_path": str(path), "sha256": base_5499.digest(path), "exists": path.is_file()} for path in paths])
    base_5467.atomic_csv(VALIDATION, validations)
    base_5467.atomic_json(STATUS, payload)
    base_5467.atomic_json(RESULT, payload)
    render_document(payload, base_5467)
    print(json.dumps({key: payload[key] for key in (
        "decision",
        "evaluated_path",
        "node_outcome",
        "accepted_subcuboid_count",
        "pending_subcuboid_count",
        "unresolved_subcuboid_count",
        "exact_low_t_parent_closure",
        "low_t_union_amplitude_denominator_abs_lower",
        "low_t_union_collision_jacobian_abs_lower",
        "new_v58_application_count",
        "partition_volume_error",
        "failed_validation_count",
        "next_target",
    )}, indent=2))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
