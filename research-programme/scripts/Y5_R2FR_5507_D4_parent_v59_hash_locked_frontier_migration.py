from __future__ import annotations

import argparse
import importlib.util
import json
from copy import deepcopy
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


POST = Path(__file__).resolve().parents[1]
SCRIPTS = POST / "scripts"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
OUTPUT = FUNCTIONAL_RG / "5507"
WORK = OUTPUT / "work-v1"

SCRIPT_5506 = SCRIPTS / "Y5_R2FR_5506_D4_parent_v59_proof_carrying_adaptive_xt_integration_gate.py"
SOURCE_STATE = FUNCTIONAL_RG / "5505" / "work-v1" / "E07__U051__RIGHT_CONNECTOR__CUBOID__6df3d70a73e4618b.json"
RESULT_5506 = FUNCTIONAL_RG / "5506" / "D4_parent_v59_proof_carrying_adaptive_xt_result.json"
VALIDATION_5506 = FUNCTIONAL_RG / "5506" / "P8_Y5_BRR5505_5506_VALIDATION.csv"
SOURCE_REGISTER_5506 = FUNCTIONAL_RG / "5506" / "source_register.csv"
APPLICATION_AUDIT_5506 = FUNCTIONAL_RG / "5506" / "D4_parent_v59_adaptive_xt_application_audit.csv"
PROOF_CACHE_5506 = FUNCTIONAL_RG / "5506" / "D4_parent_v59_exact_binding_proof_cache.csv"
COMPARISON_5506 = FUNCTIONAL_RG / "5506" / "D4_parent_v59_target_control_comparison.csv"
CERTIFICATE_5496 = FUNCTIONAL_RG / "5496" / "D4_parent_v58_adaptive_complete_amplitude_certificate.json"

TARGET_CUBOID_ID = "E07__U051__RIGHT_CONNECTOR__CUBOID__6df3d70a73e4618b"
STATE = WORK / f"{TARGET_CUBOID_ID}.json"
MIGRATION_AUDIT = OUTPUT / "D4_parent_v59_frontier_migration_audit.csv"
SOURCE_REGISTER = OUTPUT / "source_register.csv"
VALIDATION = OUTPUT / "P8_Y5_BRR5506_5507_VALIDATION.csv"
STATUS = OUTPUT / "status.json"
RESULT = OUTPUT / "D4_parent_v59_frontier_migration_result.json"
DOCUMENT = POST / "5507-Y5-R2FR-D4-parent-v59-hash-locked-frontier-migration.md"

CHECKPOINT = 5507
REVISION = "D4-parent-v59-hash-locked-frontier-migration-v1"
PARENT_V58_REVISION = "D4-deformed-contour-regular-away-W3-v58-adaptive-stable-edge-local-T2-union"
PARENT_V59_REVISION = "D4-deformed-contour-regular-away-W3-v59-proof-carrying-adaptive-xt-cover"
EXPECTED_COUNTS = (184, 3, 0)
EXPECTED_WITNESSES = 64
EXPECTED_PENDING_PATHS = (
    "R_E1S",
    "R_E0S_E1S",
    "R_E0S_E0S_E1S_X1S",
)

EXPECTED_SCRIPT_5506_SHA256 = "e29f4bc38eab7c9834512dd7c3020bc10a3207dc63486ca27d1e282dfe894fa0"
EXPECTED_SOURCE_STATE_SHA256 = "df67524e5d8f81d9642cd04514c1f22e325fa0dedf1f466dcf7a74de3c940a8b"
EXPECTED_RESULT_5506_SHA256 = "f519605a65d2947c8a2866f5e4e929816e47c5f684ffe380f1bd0891d025f2f9"
EXPECTED_VALIDATION_5506_SHA256 = "423ece3372279b98df7a763b1f7442af64bff159bdf014a7b7b47f2ca02c7184"
EXPECTED_SOURCE_REGISTER_5506_SHA256 = "a40668f99d394e400394d31bb257c2d04a91124e148c4711368a1e6971ca3efa"
EXPECTED_APPLICATION_AUDIT_5506_SHA256 = "0d47a2798846f0e3c7d4ddc2d0051e3baa4365fdf7f2512bc415f423c00dfc27"
EXPECTED_PROOF_CACHE_5506_SHA256 = "981da19698a0db9195038b15aba849647deec80e2ea277b725419f8047a5aaba"
EXPECTED_COMPARISON_5506_SHA256 = "54e65b04ed5dc25271eec5324bb184c1cda722c424b175b28a923f3b8b7717cf"
EXPECTED_CERTIFICATE_5496_SHA256 = "27dc7fce1f83b424e9d9341778a392b83ed7c8659d12e05afd561338782fc708"


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise ImportError(f"cannot load {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def check(gate: str, passed: bool, evidence: Any) -> dict[str, Any]:
    return {"checkpoint": CHECKPOINT, "validation_gate": gate, "passed": bool(passed), "evidence": evidence}


def migrated_state(base_5499: Any, source: dict[str, Any], inherited_hashes: dict[str, str], cache_bindings: list[str]) -> dict[str, Any]:
    state = deepcopy(source)
    state["checkpoint"] = CHECKPOINT
    state["revision"] = REVISION
    state["parent_revision"] = PARENT_V59_REVISION
    history = list(state.get("parent_revision_history", []))
    if not history or history[-1] != PARENT_V59_REVISION:
        history.append(PARENT_V59_REVISION)
    state["parent_revision_history"] = history
    state["v59_frontier_carry_forward"] = {
        "source_checkpoint": 5505,
        "candidate_checkpoint": 5506,
        "source_state_path": str(SOURCE_STATE),
        "source_state_sha256": EXPECTED_SOURCE_STATE_SHA256,
        "source_accepted_sha256": base_5499.canonical_digest(source["accepted"]),
        "source_pending_sha256": base_5499.canonical_digest(source["stack"]),
        "source_unresolved_sha256": base_5499.canonical_digest(source["unresolved"]),
        "source_refinement_witnesses_sha256": base_5499.canonical_digest(source["refinement_witnesses"]),
        "candidate_evidence_sha256": inherited_hashes,
        "proof_cache_binding_sha256": cache_bindings,
        "migration_rule": "status-only parent revision migration; numerical ledgers unchanged",
        "carried_counts": list(EXPECTED_COUNTS),
        "carried_utc": datetime.now(timezone.utc).isoformat(),
    }
    state["v59_node_evaluation_count"] = 0
    state["v59_adaptive_application_count"] = 0
    state["v59_proof_cache_binding_count"] = len(cache_bindings)
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
    state["last_update_utc"] = datetime.now(timezone.utc).isoformat()
    return state


def render_document(payload: dict[str, Any], base_5467: Any) -> None:
    lines = [
        "# 5507: D4 parent-v59 hash-locked frontier migration",
        "",
        "Checkpoint 5506's executable target/control candidate is hash locked. Checkpoint 5505's active numerical frontier is migrated by revision status only.",
        "",
        f"Frontier before/after: `{payload['source_counts']}` -> `{payload['migrated_counts']}`. Pending order unchanged: `{payload['pending_order_unchanged']}`. Numerical ledgers unchanged: `{payload['numerical_ledgers_unchanged']}`.",
        "",
        f"Parent revision: `{payload['parent_revision']}`. Proof-cache bindings: `{payload['proof_cache_binding_count']}`.",
        "",
        f"**{payload['decision']}**",
        "",
        "No numerical node is evaluated. Active-cuboid, full outer, event-local/combined W3, regulator-limit, all-operator local GR and full MTS claims remain open.",
        "",
    ]
    base_5467.atomic_text(DOCUMENT, "\n".join(lines))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    arguments = parser.parse_args()

    base_5506 = load_module("mts_5506_for_5507", SCRIPT_5506)
    base_5505 = load_module("mts_5505_for_5507", base_5506.SCRIPT_5505)
    base_5504 = load_module("mts_5504_for_5507", base_5505.SCRIPT_5504)
    base_5503 = load_module("mts_5503_for_5507", base_5504.SCRIPT_5503)
    base_5502 = load_module("mts_5502_for_5507", base_5503.SCRIPT_5502)
    base_5501 = load_module("mts_5501_for_5507", base_5502.SCRIPT_5501)
    base_5500 = load_module("mts_5500_for_5507", base_5501.SCRIPT_5500)
    base_5499 = load_module("mts_5499_for_5507", base_5500.SCRIPT_5499)
    base_5498 = load_module("mts_5498_for_5507", base_5499.SCRIPT_5498)
    base_5496 = load_module("mts_5496_for_5507", base_5498.SCRIPT_5496)
    base_5495 = load_module("mts_5495_for_5507", base_5496.SCRIPT_5495)
    base_5467 = load_module("mts_5467_for_5507", base_5495.SCRIPT_5467)
    base_5468 = load_module("mts_5468_for_5507", base_5495.SCRIPT_5468)
    base_5472 = load_module("mts_5472_for_5507", base_5495.SCRIPT_5472)
    base_5474 = load_module("mts_5474_for_5507", base_5495.SCRIPT_5474)
    base_5476 = load_module("mts_5476_for_5507", base_5495.SCRIPT_5476)
    base_5478 = load_module("mts_5478_for_5507", base_5495.SCRIPT_5478)
    base_5480 = load_module("mts_5480_for_5507", base_5495.SCRIPT_5480)
    base_5483 = load_module("mts_5483_for_5507", base_5495.SCRIPT_5483)
    base_5490 = load_module("mts_5490_for_5507", base_5495.SCRIPT_5490)
    base_5493 = load_module("mts_5493_for_5507", base_5495.SCRIPT_5493)

    base_5467.set_below_normal_priority()
    base_5480.set_single_core_affinity()
    before_formalization = base_5467.formalization_snapshot()
    inherited_hashes = {
        "script_5506": base_5499.digest(SCRIPT_5506),
        "source_state": base_5499.digest(SOURCE_STATE),
        "result_5506": base_5499.digest(RESULT_5506),
        "validation_5506": base_5499.digest(VALIDATION_5506),
        "source_register_5506": base_5499.digest(SOURCE_REGISTER_5506),
        "application_audit_5506": base_5499.digest(APPLICATION_AUDIT_5506),
        "proof_cache_5506": base_5499.digest(PROOF_CACHE_5506),
        "comparison_5506": base_5499.digest(COMPARISON_5506),
        "certificate_5496": base_5499.digest(CERTIFICATE_5496),
    }
    expected_hashes = {
        "script_5506": EXPECTED_SCRIPT_5506_SHA256,
        "source_state": EXPECTED_SOURCE_STATE_SHA256,
        "result_5506": EXPECTED_RESULT_5506_SHA256,
        "validation_5506": EXPECTED_VALIDATION_5506_SHA256,
        "source_register_5506": EXPECTED_SOURCE_REGISTER_5506_SHA256,
        "application_audit_5506": EXPECTED_APPLICATION_AUDIT_5506_SHA256,
        "proof_cache_5506": EXPECTED_PROOF_CACHE_5506_SHA256,
        "comparison_5506": EXPECTED_COMPARISON_5506_SHA256,
        "certificate_5496": EXPECTED_CERTIFICATE_5496_SHA256,
    }
    if inherited_hashes != expected_hashes:
        raise RuntimeError("checkpoint-5507 inherited source hash mismatch")

    register_5506 = base_5499.read_csv(SOURCE_REGISTER_5506)
    paths = tuple(dict.fromkeys((
        Path(__file__).resolve(), SCRIPT_5506, SOURCE_STATE, RESULT_5506,
        VALIDATION_5506, SOURCE_REGISTER_5506, APPLICATION_AUDIT_5506,
        PROOF_CACHE_5506, COMPARISON_5506, CERTIFICATE_5496,
        *(Path(row["source_path"]) for row in register_5506),
    )))
    missing = [str(path) for path in paths if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"missing sources: {missing}")

    source = base_5499.read_json(SOURCE_STATE)
    result_5506 = base_5499.read_json(RESULT_5506)
    validation_5506 = base_5499.read_csv(VALIDATION_5506)
    proof_cache_rows = base_5499.read_csv(PROOF_CACHE_5506)
    source_counts = (len(source["accepted"]), len(source["stack"]), len(source["unresolved"]))
    pending_paths = tuple(str(row["refinement_path"]) for row in source["stack"])
    candidate_certified = (
        result_5506.get("decision") == "PARENT_V59_PROOF_CARRYING_ADAPTIVE_XT_CANDIDATE_CERTIFIED__MIGRATION_REQUIRED"
        and result_5506.get("valid_for_parent_v59_candidate") is True
        and int(result_5506.get("failed_validation_count", -1)) == 0
        and all(base_5499.truth(row.get("passed")) for row in validation_5506)
        and base_5499.source_register_is_current(register_5506)
        and len(proof_cache_rows) == 2
        and all(base_5499.truth(row.get("exact_binding_match")) and base_5499.truth(row.get("positive_complete_parent_certificate")) for row in proof_cache_rows)
        and source_counts == EXPECTED_COUNTS
        and len(source["refinement_witnesses"]) == EXPECTED_WITNESSES
        and pending_paths == EXPECTED_PENDING_PATHS
        and source.get("parent_revision") == PARENT_V58_REVISION
        and base_5498.exact_partition_volume(source) == base_5498.exact_node_volume(source["root"])
    )
    if not candidate_certified:
        raise RuntimeError("checkpoint-5506 candidate or checkpoint-5505 frontier is not certified")

    stable, _, cells, support_segments, branches = base_5467.load_parent()
    cuboid = next(row for row in base_5499.read_csv(base_5495.MANIFEST_5468) if row["cuboid_job_id"] == TARGET_CUBOID_ID)
    certificate_5496 = base_5499.read_json(CERTIFICATE_5496)
    parent_v58 = base_5498.reconstruct_parent(
        base_5467, base_5472, base_5474, base_5476, base_5478, base_5483,
        base_5490, base_5493, base_5495, base_5496, certificate_5496,
    )
    target_node = next(row for row in source["refinement_witnesses"] if row.get("refinement_path") == base_5506.TARGET_PATH)
    target_arguments = base_5495.target_arguments(stable, parent_v58, cells, support_segments, branches, cuboid, target_node)
    lower_arguments, upper_arguments, split = base_5506.split_arguments(target_arguments, source)
    path_speed = base_5468.full_cell_path_speed_bound(parent_v58, cells[cuboid["mapped_cell_id"]], cuboid["path_segment"])
    proof_cache, rebuilt_cache_rows = base_5506.build_proof_cache(base_5495, source, (lower_arguments, upper_arguments), path_speed)
    parent_v59 = base_5506.install_parent_v59(parent_v58, base_5495, source, proof_cache, 1)
    cache_bindings = sorted(proof_cache)
    reconstructed_parent = (
        parent_v59.REVISION == PARENT_V59_REVISION
        and not parent_v59.V59_PARENT_ACTION_CHANGED
        and parent_v59.V59_ONLY_ENCLOSURE_COMPOSITION_CHANGED
        and split["coverage_error"] == 0.0
        and len(rebuilt_cache_rows) == 2
    )

    if arguments.dry_run:
        print(json.dumps({
            "checkpoint": CHECKPOINT,
            "dry_run": True,
            "source_counts": list(source_counts),
            "pending_paths": list(pending_paths),
            "candidate_certified": candidate_certified,
            "reconstructed_parent_revision": parent_v59.REVISION,
            "proof_cache_binding_count": len(cache_bindings),
            "source_hashes_match": inherited_hashes == expected_hashes,
            "exact_source_partition": True,
        }, indent=2))
        return 0

    state = migrated_state(base_5499, source, inherited_hashes, cache_bindings)
    numerical_fields = ("accepted", "stack", "unresolved", "refinement_witnesses")
    before_digests = {field: base_5499.canonical_digest(source[field]) for field in numerical_fields}
    after_digests = {field: base_5499.canonical_digest(state[field]) for field in numerical_fields}
    numerical_ledgers_unchanged = before_digests == after_digests
    migrated_counts = (len(state["accepted"]), len(state["stack"]), len(state["unresolved"]))
    migrated_pending = tuple(str(row["refinement_path"]) for row in state["stack"])
    exact_partition = base_5498.exact_partition_volume(state) == base_5498.exact_node_volume(state["root"])
    history = state["parent_revision_history"]
    history_append_exact = history[:-1] == source.get("parent_revision_history", []) and history[-1] == PARENT_V59_REVISION
    counters_unchanged = int(state["node_evaluation_count"]) == int(source["node_evaluation_count"]) and int(state["v58_node_evaluation_count"]) == int(source["v58_node_evaluation_count"])
    after_formalization = base_5467.formalization_snapshot()

    validations = [
        check("all_sources_exist", not missing, len(paths)),
        check("checkpoint_5506_candidate_is_hash_locked", inherited_hashes == expected_hashes, inherited_hashes),
        check("checkpoint_5506_candidate_is_certified", candidate_certified, result_5506.get("decision")),
        check("source_frontier_is_exact_184_3_0", source_counts == EXPECTED_COUNTS, source_counts),
        check("source_pending_order_is_exact", pending_paths == EXPECTED_PENDING_PATHS, pending_paths),
        check("parent_v59_reconstructs_from_signed_sources", reconstructed_parent, parent_v59.REVISION),
        check("proof_cache_bindings_reconstruct_exactly", cache_bindings == sorted(row["binding_sha256"] for row in proof_cache_rows), cache_bindings),
        check("migration_changes_no_numerical_ledger", numerical_ledgers_unchanged, {"before": before_digests, "after": after_digests}),
        check("migration_preserves_frontier_counts", migrated_counts == source_counts == EXPECTED_COUNTS, migrated_counts),
        check("migration_preserves_pending_order", migrated_pending == pending_paths, migrated_pending),
        check("migration_appends_exactly_parent_v59_revision", history_append_exact, history[-2:]),
        check("migration_evaluates_no_numerical_node", counters_unchanged and state["v59_node_evaluation_count"] == 0 and state["processed_this_run"] == 0, state["node_evaluation_count"]),
        check("exact_partition_is_preserved", exact_partition, exact_partition),
        check("formalization_workbench_untouched", before_formalization == after_formalization, f"before={len(before_formalization)};after={len(after_formalization)}"),
        check("broad_claims_remain_false", not state["valid_for_parent_v59_active_cuboid"] and not state["valid_for_full_outer_parent_leaf_enclosure"] and not state["valid_for_D4_event_local_W3_bound"] and not state["valid_for_all_operator_local_GR_claim"] and not state["valid_for_full_MTS_claim"], "status-only migration"),
    ]
    failed = [row for row in validations if not row["passed"]]
    decision = "PARENT_V59_FRONTIER_MIGRATION_CERTIFIED__RUN_NEXT_NODE" if not failed else "PARENT_V59_FRONTIER_MIGRATION_REJECTED"
    payload = {
        "checkpoint": CHECKPOINT,
        "revision": REVISION,
        "parent_revision": PARENT_V59_REVISION,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "decision": decision,
        "source_counts": list(source_counts),
        "migrated_counts": list(migrated_counts),
        "source_pending_paths": list(pending_paths),
        "migrated_pending_paths": list(migrated_pending),
        "pending_order_unchanged": migrated_pending == pending_paths,
        "numerical_ledgers_unchanged": numerical_ledgers_unchanged,
        "node_counters_unchanged": counters_unchanged,
        "proof_cache_binding_count": len(cache_bindings),
        "exact_partition_preserved": exact_partition,
        "validation_row_count": len(validations),
        "failed_validation_count": len(failed),
        "valid_for_parent_v59_frontier_migration": not failed,
        "valid_for_parent_v59_active_cuboid": False,
        "valid_for_full_outer_parent_leaf_enclosure": False,
        "valid_for_D4_event_local_W3_bound": False,
        "valid_for_all_operator_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
        "next_target": state["stack"][-1]["refinement_path"],
    }
    audit_row = {
        "checkpoint": CHECKPOINT,
        "source_state_sha256": EXPECTED_SOURCE_STATE_SHA256,
        "source_parent_revision": source["parent_revision"],
        "migrated_parent_revision": state["parent_revision"],
        "source_counts": json.dumps(source_counts),
        "migrated_counts": json.dumps(migrated_counts),
        "source_accepted_sha256": before_digests["accepted"],
        "migrated_accepted_sha256": after_digests["accepted"],
        "source_pending_sha256": before_digests["stack"],
        "migrated_pending_sha256": after_digests["stack"],
        "source_unresolved_sha256": before_digests["unresolved"],
        "migrated_unresolved_sha256": after_digests["unresolved"],
        "source_witness_sha256": before_digests["refinement_witnesses"],
        "migrated_witness_sha256": after_digests["refinement_witnesses"],
        "proof_cache_binding_count": len(cache_bindings),
        "exact_partition_preserved": exact_partition,
        "numerical_node_evaluations": 0,
    }
    WORK.mkdir(parents=True, exist_ok=True)
    base_5467.atomic_json(STATE, state, compact=True)
    base_5467.atomic_csv(MIGRATION_AUDIT, [audit_row])
    base_5467.atomic_csv(SOURCE_REGISTER, [{"source_path": str(path), "sha256": base_5499.digest(path), "exists": path.is_file()} for path in paths])
    base_5467.atomic_csv(VALIDATION, validations)
    base_5467.atomic_json(STATUS, payload)
    base_5467.atomic_json(RESULT, payload)
    render_document(payload, base_5467)
    print(json.dumps({key: payload[key] for key in (
        "decision", "source_counts", "migrated_counts",
        "pending_order_unchanged", "numerical_ledgers_unchanged",
        "node_counters_unchanged", "proof_cache_binding_count",
        "exact_partition_preserved", "failed_validation_count", "next_target",
    )}, indent=2))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
