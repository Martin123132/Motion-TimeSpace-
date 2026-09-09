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
OUTPUT = FUNCTIONAL_RG / "5513"
WORK = OUTPUT / "work-v1"

SCRIPT_5512 = SCRIPTS / "Y5_R2FR_5512_D4_parent_v59_resumable_high_epsilon_parent_closure.py"
SOURCE_STATE = FUNCTIONAL_RG / "5512" / "work-v1" / "E07__U051__RIGHT_CONNECTOR__CUBOID__6df3d70a73e4618b.json"
RESULT_5512 = FUNCTIONAL_RG / "5512" / "D4_parent_v59_resumable_high_epsilon_parent_closure_result.json"
VALIDATION_5512 = FUNCTIONAL_RG / "5512" / "P8_Y5_BRR5511_5512_VALIDATION.csv"
SOURCE_REGISTER_5512 = FUNCTIONAL_RG / "5512" / "source_register.csv"
NODE_AUDIT_5512 = FUNCTIONAL_RG / "5512" / "D4_parent_v59_high_epsilon_frontier_node_audit.csv"
UNION_AUDIT_5512 = FUNCTIONAL_RG / "5512" / "D4_parent_v59_epsilon_pair_parent_union_audit.csv"
V59_AUDIT_5512 = FUNCTIONAL_RG / "5512" / "D4_parent_v59_high_epsilon_frontier_adaptive_xt_audit.csv"

TARGET_CUBOID_ID = "E07__U051__RIGHT_CONNECTOR__CUBOID__6df3d70a73e4618b"
STATE = WORK / f"{TARGET_CUBOID_ID}.json"
NODE_AUDIT = OUTPUT / "D4_parent_v59_final_branch_node_audit.csv"
UNION_AUDIT = OUTPUT / "D4_parent_v59_active_cuboid_union_audit.csv"
NESTED_UNION_AUDIT = OUTPUT / "D4_parent_v59_final_branch_nested_union_audit.csv"
V59_AUDIT = OUTPUT / "D4_parent_v59_final_branch_adaptive_xt_audit.csv"
V58_AUDIT = OUTPUT / "D4_parent_v59_final_branch_v58_certificate_application_audit.csv"
V57_AUDIT = OUTPUT / "D4_parent_v59_final_branch_v57_scoped_certificate_audit.csv"
JACOBIAN_XT_AUDIT = OUTPUT / "D4_parent_v59_final_branch_collision_jacobian_xt_audit.csv"
STABLE_XT_AUDIT = OUTPUT / "D4_parent_v59_final_branch_stable_edge_xt_audit.csv"
PIVOT_AUDIT = OUTPUT / "D4_parent_v59_final_branch_first_spinor_pivot_audit.csv"
STABLE_T_AUDIT = OUTPUT / "D4_parent_v59_final_branch_stable_edge_t_audit.csv"
JACOBIAN_T_AUDIT = OUTPUT / "D4_parent_v59_final_branch_collision_jacobian_t_audit.csv"
SOURCE_REGISTER = OUTPUT / "source_register.csv"
VALIDATION = OUTPUT / "P8_Y5_BRR5512_5513_VALIDATION.csv"
STATUS = OUTPUT / "status.json"
RESULT = OUTPUT / "D4_parent_v59_resumable_final_branch_active_cuboid_closure_result.json"
DOCUMENT = POST / "5513-Y5-R2FR-D4-parent-v59-resumable-final-branch-active-cuboid-closure.md"

CHECKPOINT = 5513
REVISION = "D4-parent-v59-resumable-final-branch-active-cuboid-closure-v1"
PARENT_V59_REVISION = "D4-deformed-contour-regular-away-W3-v59-proof-carrying-adaptive-xt-cover"
EXPECTED_PATH = "R_E1S"
ROOT_PARENT_PATH = "R"
FINAL_BRANCH_PREFIX = EXPECTED_PATH
NESTED_PARENT_PATHS = (
    "R_E1S_E0S_E0S",
    "R_E1S_E0S",
    "R_E1S",
)
EXPECTED_SOURCE_COUNTS = (195, 1, 0)
EXPECTED_SOURCE_WITNESSES = 73
EXPECTED_SOURCE_V59_AUDIT_ROWS = 55
EXPECTED_PENDING_PATHS = (EXPECTED_PATH,)

EXPECTED_SCRIPT_5512_SHA256 = "6d78c6f752a48e94e6a3ad0d643243ed31d4abb54534457779c41bbc2b62a7f9"
EXPECTED_SOURCE_STATE_SHA256 = "c3c637a87677d0b3c6e97899ac3e357f8f4e170b5b7b3f45eb26338291dc8ead"
EXPECTED_RESULT_5512_SHA256 = "696b07b6e843025c69c00c4a465d79bf3b86a0f340b1486eefb229e6c5a585b2"
EXPECTED_VALIDATION_5512_SHA256 = "b9927138a21a53ebd6df175b773fd5f79d5f030f9a46c410ae0e3e18da0e1e09"
EXPECTED_SOURCE_REGISTER_5512_SHA256 = "5d6c85e41920f478bb68dcc72987ae4868881201f2216ad2c15b3cc4a813ea53"
EXPECTED_NODE_AUDIT_5512_SHA256 = "1419ca1b8d101c8a425edb7dd7236dc6a9f9477e42dcb852dc35fffab05d4af9"
EXPECTED_UNION_AUDIT_5512_SHA256 = "f573439f5172244f311c06838c4d6704c90bfc76ba2a972c56c1989d4d358434"
EXPECTED_V59_AUDIT_5512_SHA256 = "0c2c6fd0ad20895c769cc3721833360c4f06148eeeed4e7862a53b4f40801845"

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
    state["checkpoint_5513"] = {
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
    state["decision"] = "PARENT_V59_FINAL_BRANCH_PARTIAL__RESUME"
    for field in (
        "valid_for_parent_v59_active_cuboid",
        "valid_for_full_outer_parent_leaf_enclosure",
        "valid_for_D4_event_local_W3_bound",
        "valid_for_all_operator_local_GR_claim",
        "valid_for_full_MTS_claim",
    ):
        state[field] = False
    return state


def normalize_adapter_state(base_5467: Any, state: dict[str, Any]) -> dict[str, Any]:
    if "checkpoint_5512_source_copy" not in state:
        return state
    state["checkpoint_5513"] = state["checkpoint_5512"]
    state["checkpoint_5512"] = state.pop("checkpoint_5512_source_copy")
    base_5467.atomic_json(STATE, state, compact=True)
    return state


def process_atomic_node(
    base_5512: Any,
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
    state["checkpoint_5512_source_copy"] = deepcopy(state["checkpoint_5512"])
    state["checkpoint_5512"] = state["checkpoint_5513"]
    base_5512.CHECKPOINT = CHECKPOINT
    base_5512.REVISION = REVISION
    base_5512.EXPECTED_PATH = EXPECTED_PATH
    base_5512.STATE = STATE
    base_5512.AUDIT_BINDINGS = AUDIT_BINDINGS
    state = base_5512.process_atomic_node(
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
        maximum_refinement_depth,
    )
    state["checkpoint_5513"] = state["checkpoint_5512"]
    state["checkpoint_5512"] = state.pop("checkpoint_5512_source_copy")
    newest_record = state["checkpoint_5513"]["records"][-1]
    newest_path = newest_record["refinement_path"]
    for collection_name in ("accepted", "refinement_witnesses", "unresolved"):
        for row in state[collection_name]:
            if (
                row.get("refinement_path") == newest_path
                and row.get("certificate_source") == "checkpoint_5512_parent_v59"
            ):
                row["certificate_source"] = "checkpoint_5513_parent_v59"
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
        "# 5513: D4 parent-v59 resumable final-branch active-cuboid closure",
        "",
        "Checkpoint 5512 is hash locked and the sole remaining root branch is evaluated under the unchanged proof-carrying parent-v59 chain.",
        "",
        *evaluations,
        "",
        f"Last outcome: `{payload['node_outcome']}`. Checkpoint runtime: `{payload['checkpoint_runtime_seconds']}` seconds. Frontier: `{payload['accepted_subcuboid_count']}/{payload['pending_subcuboid_count']}/{payload['unresolved_subcuboid_count']}`.",
        "",
        f"New v59 triggers/splits/cache hits/live passes/aggregates: `{payload['v59_trigger_count']}/{payload['v59_split_count']}/{payload['v59_cache_hit_count']}/{payload['v59_live_parent_pass_count']}/{payload['v59_aggregate_count']}`.",
        "",
        f"Exact active-cuboid closure: `{payload['exact_active_cuboid_closure']}` using `{payload['active_cuboid_leaf_count']}` leaves.",
        "",
        f"**{payload['decision']}**",
        "",
        "Full outer, event-local/combined W3, regulator-limit, all-operator local GR and full MTS claims remain open.",
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
    if arguments.target_node_evaluations < 1 or arguments.target_node_evaluations > 64:
        raise ValueError("target node evaluations must be between one and sixty-four")
    if arguments.max_runtime_seconds <= 0:
        raise ValueError("maximum runtime must be positive")

    base_5512 = load_module("mts_5512_for_5513", SCRIPT_5512)
    base_5511 = load_module("mts_5511_for_5513", base_5512.SCRIPT_5511)
    base_5510 = load_module("mts_5510_for_5513", base_5511.SCRIPT_5510)
    base_5509 = load_module("mts_5509_for_5513", base_5510.SCRIPT_5509)
    base_5508 = load_module("mts_5508_for_5513", base_5509.SCRIPT_5508)
    base_5507 = load_module("mts_5507_for_5513", base_5508.SCRIPT_5507)
    base_5506 = load_module("mts_5506_for_5513", base_5508.SCRIPT_5506)
    base_5505 = load_module("mts_5505_for_5513", base_5506.SCRIPT_5505)
    base_5504 = load_module("mts_5504_for_5513", base_5505.SCRIPT_5504)
    base_5503 = load_module("mts_5503_for_5513", base_5504.SCRIPT_5503)
    base_5502 = load_module("mts_5502_for_5513", base_5503.SCRIPT_5502)
    base_5501 = load_module("mts_5501_for_5513", base_5502.SCRIPT_5501)
    base_5500 = load_module("mts_5500_for_5513", base_5501.SCRIPT_5500)
    base_5499 = load_module("mts_5499_for_5513", base_5500.SCRIPT_5499)
    base_5498 = load_module("mts_5498_for_5513", base_5499.SCRIPT_5498)
    base_5496 = load_module("mts_5496_for_5513", base_5498.SCRIPT_5496)
    base_5495 = load_module("mts_5495_for_5513", base_5496.SCRIPT_5495)
    base_5467 = load_module("mts_5467_for_5513", base_5495.SCRIPT_5467)
    base_5468 = load_module("mts_5468_for_5513", base_5495.SCRIPT_5468)
    base_5469 = load_module("mts_5469_for_5513", base_5495.SCRIPT_5469)
    base_5472 = load_module("mts_5472_for_5513", base_5495.SCRIPT_5472)
    base_5474 = load_module("mts_5474_for_5513", base_5495.SCRIPT_5474)
    base_5476 = load_module("mts_5476_for_5513", base_5495.SCRIPT_5476)
    base_5478 = load_module("mts_5478_for_5513", base_5495.SCRIPT_5478)
    base_5480 = load_module("mts_5480_for_5513", base_5495.SCRIPT_5480)
    base_5483 = load_module("mts_5483_for_5513", base_5495.SCRIPT_5483)
    base_5490 = load_module("mts_5490_for_5513", base_5495.SCRIPT_5490)
    base_5493 = load_module("mts_5493_for_5513", base_5495.SCRIPT_5493)

    base_5467.set_below_normal_priority()
    base_5480.set_single_core_affinity()
    before_formalization = base_5467.formalization_snapshot()
    inherited_hashes = {
        "script_5512": base_5499.digest(SCRIPT_5512),
        "source_state": base_5499.digest(SOURCE_STATE),
        "result_5512": base_5499.digest(RESULT_5512),
        "validation_5512": base_5499.digest(VALIDATION_5512),
        "source_register_5512": base_5499.digest(SOURCE_REGISTER_5512),
        "node_audit_5512": base_5499.digest(NODE_AUDIT_5512),
        "union_audit_5512": base_5499.digest(UNION_AUDIT_5512),
        "v59_audit_5512": base_5499.digest(V59_AUDIT_5512),
    }
    expected_hashes = {
        "script_5512": EXPECTED_SCRIPT_5512_SHA256,
        "source_state": EXPECTED_SOURCE_STATE_SHA256,
        "result_5512": EXPECTED_RESULT_5512_SHA256,
        "validation_5512": EXPECTED_VALIDATION_5512_SHA256,
        "source_register_5512": EXPECTED_SOURCE_REGISTER_5512_SHA256,
        "node_audit_5512": EXPECTED_NODE_AUDIT_5512_SHA256,
        "union_audit_5512": EXPECTED_UNION_AUDIT_5512_SHA256,
        "v59_audit_5512": EXPECTED_V59_AUDIT_5512_SHA256,
    }
    if inherited_hashes != expected_hashes:
        raise RuntimeError("checkpoint-5513 inherited source hash mismatch")

    register_5512 = base_5499.read_csv(SOURCE_REGISTER_5512)
    paths = tuple(dict.fromkeys((
        Path(__file__).resolve(),
        SCRIPT_5512,
        SOURCE_STATE,
        RESULT_5512,
        VALIDATION_5512,
        SOURCE_REGISTER_5512,
        NODE_AUDIT_5512,
        UNION_AUDIT_5512,
        V59_AUDIT_5512,
        *(Path(row["source_path"]) for row in register_5512),
    )))
    missing = [str(path) for path in paths if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"missing sources: {missing}")

    source = base_5499.read_json(SOURCE_STATE)
    result_5512 = base_5499.read_json(RESULT_5512)
    validation_5512 = base_5499.read_csv(VALIDATION_5512)
    source_counts = (
        len(source["accepted"]),
        len(source["stack"]),
        len(source["unresolved"]),
    )
    pending_paths = tuple(str(row["refinement_path"]) for row in source["stack"])
    source_accepted_paths = {str(row["refinement_path"]) for row in source["accepted"]}
    source_bounds_positive = all(
        float(row["minimum_amplitude_denominator_abs_lower"]) > 0.0
        and float(row["relative_root_abs_lower"]) > 0.0
        and float(row["selected_global_root_abs_lower"]) > 0.0
        and float(row["collision_jacobian_abs_lower"]) > 0.0
        for row in source["accepted"]
    )
    root_witness_count = sum(
        row.get("refinement_path") == ROOT_PARENT_PATH
        for row in source["refinement_witnesses"]
    )
    source_certified = (
        result_5512.get("decision") == "PARENT_V59_COMPLETE_EPSILON_PAIR_PARENT_CERTIFIED__RESUME_FRONTIER"
        and result_5512.get("valid_for_parent_v59_high_epsilon_frontier") is True
        and result_5512.get("valid_for_parent_v59_complete_epsilon_pair_parent") is True
        and result_5512.get("valid_for_parent_v59_active_cuboid") is False
        and int(result_5512.get("failed_validation_count", -1)) == 0
        and int(result_5512.get("processed_node_evaluations", -1)) == 9
        and all(base_5499.truth(row.get("passed")) for row in validation_5512)
        and base_5499.source_register_is_current(register_5512)
        and source_counts == EXPECTED_SOURCE_COUNTS
        and len(source["refinement_witnesses"]) == EXPECTED_SOURCE_WITNESSES
        and len(source.get("v59_adaptive_xt_audit_rows", [])) == EXPECTED_SOURCE_V59_AUDIT_ROWS
        and pending_paths == EXPECTED_PENDING_PATHS
        and source.get("parent_revision") == PARENT_V59_REVISION
        and len(source.get("checkpoint_5512", {}).get("records", [])) == 9
        and source["checkpoint_5512"]["records"][-1]["outcome"] == "ACCEPTED"
        and len(source_accepted_paths) == len(source["accepted"])
        and source_bounds_positive
        and root_witness_count == 1
        and base_5498.exact_partition_volume(source) == base_5498.exact_node_volume(source["root"])
    )
    if not source_certified:
        raise RuntimeError("checkpoint-5512 source is not current and certified")

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
            "source_accepted_leaf_count": len(source_accepted_paths),
            "source_bounds_positive": source_bounds_positive,
            "root_parent_witness_count": root_witness_count,
        }, indent=2))
        return 0

    if STATE.is_file():
        state = base_5499.read_json(STATE)
        state = normalize_adapter_state(base_5467, state)
        if state.get("checkpoint_5513", {}).get("source_state_sha256") != EXPECTED_SOURCE_STATE_SHA256:
            raise RuntimeError("checkpoint-5513 output source mismatch")
    else:
        WORK.mkdir(parents=True, exist_ok=True)
        state = carry_forward(base_5499, source)
        base_5467.atomic_json(STATE, state, compact=True)
    run_started = time.perf_counter()
    while (
        len(state["checkpoint_5513"]["records"]) < arguments.target_node_evaluations
        and state["stack"]
        and not state["unresolved"]
    ):
        if state["checkpoint_5513"]["records"] and time.perf_counter() - run_started >= arguments.max_runtime_seconds:
            break
        state = process_atomic_node(
            base_5512,
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

    records = state["checkpoint_5513"]["records"]
    if not records:
        raise RuntimeError("checkpoint-5513 committed no atomic node")
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
    carry = state["checkpoint_5513"]
    source_audits_preserved = all(
        state.get(key, [])[: len(source.get(key, []))] == source.get(key, [])
        for key, _, _ in AUDIT_BINDINGS
    )
    final_branch_pending = any(
        row["refinement_path"] == FINAL_BRANCH_PREFIX
        or row["refinement_path"].startswith(f"{FINAL_BRANCH_PREFIX}_")
        for row in state["stack"]
    )
    final_branch_unresolved = any(
        row["refinement_path"] == FINAL_BRANCH_PREFIX
        or row["refinement_path"].startswith(f"{FINAL_BRANCH_PREFIX}_")
        for row in state["unresolved"]
    )
    final_branch_accepted_paths = {
        row["refinement_path"]
        for row in state["accepted"]
        if row["refinement_path"] == FINAL_BRANCH_PREFIX
        or row["refinement_path"].startswith(f"{FINAL_BRANCH_PREFIX}_")
    }
    final_branch_started = any(
        row["refinement_path"] == FINAL_BRANCH_PREFIX
        or row["refinement_path"].startswith(f"{FINAL_BRANCH_PREFIX}_")
        for row in records
    )
    nested_union_rows = []
    for parent_path in NESTED_PARENT_PATHS:
        branch_leaf_paths = {
            row["refinement_path"]
            for row in state["accepted"]
            if row["refinement_path"] == parent_path
            or row["refinement_path"].startswith(f"{parent_path}_")
        }
        branch_pending = any(
            row["refinement_path"] == parent_path
            or row["refinement_path"].startswith(f"{parent_path}_")
            for row in state["stack"]
        )
        branch_unresolved = any(
            row["refinement_path"] == parent_path
            or row["refinement_path"].startswith(f"{parent_path}_")
            for row in state["unresolved"]
        )
        branch_started = any(
            row["refinement_path"] == parent_path
            or row["refinement_path"].startswith(f"{parent_path}_")
            for row in records
        )
        branch_complete = branch_started and not branch_pending and not branch_unresolved
        if branch_leaf_paths:
            branch_union = base_5511.exact_union(
                base_5498,
                base_5503,
                state,
                parent_path,
                branch_leaf_paths,
            )
        else:
            branch_union = {
                "parent_path": parent_path,
                "expected_leaf_count": 0,
                "actual_leaf_count": 0,
                "closure": False,
                "volume_error": math.nan,
                "pairwise_interior_disjoint": False,
                "integrated_regular_path_abs_upper": math.nan,
                "minimum_amplitude_denominator_abs_lower": math.nan,
                "minimum_relative_root_abs_lower": math.nan,
                "minimum_selected_global_root_abs_lower": math.nan,
                "collision_jacobian_abs_lower": math.nan,
            }
        branch_certified = (
            branch_complete
            and bool(branch_leaf_paths)
            and branch_union["closure"]
            and branch_union["volume_error"] == 0.0
            and branch_union["minimum_amplitude_denominator_abs_lower"] > 0.0
            and branch_union["minimum_relative_root_abs_lower"] > 0.0
            and branch_union["minimum_selected_global_root_abs_lower"] > 0.0
            and branch_union["collision_jacobian_abs_lower"] > 0.0
        )
        nested_union_rows.append({
            "union_id": f"nested_{parent_path}",
            "branch_started": branch_started,
            "branch_complete": branch_complete,
            "branch_certified": branch_certified,
            "branch_pending": branch_pending,
            "branch_unresolved": branch_unresolved,
            **branch_union,
        })
    completed_nested_unions = [row for row in nested_union_rows if row["branch_complete"]]
    completed_nested_unions_certified = all(
        row["branch_certified"] for row in completed_nested_unions
    )
    full_nested_chain_certified = all(
        row["branch_complete"] and row["branch_certified"]
        for row in nested_union_rows
    )
    active_leaf_paths = source_accepted_paths | final_branch_accepted_paths
    active_union = base_5511.exact_union(
        base_5498,
        base_5503,
        state,
        ROOT_PARENT_PATH,
        active_leaf_paths,
    )
    all_accepted_paths_unique = len(active_leaf_paths) == len(state["accepted"])
    all_accepted_bounds_positive = all(
        float(row["minimum_amplitude_denominator_abs_lower"]) > 0.0
        and float(row["relative_root_abs_lower"]) > 0.0
        and float(row["selected_global_root_abs_lower"]) > 0.0
        and float(row["collision_jacobian_abs_lower"]) > 0.0
        for row in state["accepted"]
    )
    active_closure_required = (
        final_branch_started
        and not final_branch_pending
        and not final_branch_unresolved
        and not state["stack"]
        and not state["unresolved"]
    )
    active_closure_certified = (
        active_closure_required
        and bool(final_branch_accepted_paths)
        and full_nested_chain_certified
        and all_accepted_paths_unique
        and all_accepted_bounds_positive
        and active_union["closure"]
        and active_union["volume_error"] == 0.0
        and active_union["minimum_amplitude_denominator_abs_lower"] > 0.0
        and active_union["minimum_relative_root_abs_lower"] > 0.0
        and active_union["minimum_selected_global_root_abs_lower"] > 0.0
        and active_union["collision_jacobian_abs_lower"] > 0.0
    )
    state["valid_for_parent_v59_active_cuboid"] = active_closure_certified
    after_formalization = base_5467.formalization_snapshot()
    validations = [
        check("all_sources_exist", not missing, len(paths)),
        check("checkpoint_5512_evidence_is_hash_locked", inherited_hashes == expected_hashes, inherited_hashes),
        check("checkpoint_5512_epsilon_pair_parent_is_certified", source_certified, result_5512.get("decision")),
        check("source_frontier_is_exact_195_1_0", source_counts == EXPECTED_SOURCE_COUNTS, source_counts),
        check("source_pending_order_is_exact", pending_paths == EXPECTED_PENDING_PATHS, pending_paths),
        check("source_accepted_paths_are_unique_and_positive", len(source_accepted_paths) == len(source["accepted"]) and source_bounds_positive, len(source_accepted_paths)),
        check("root_parent_witness_is_unique", root_witness_count == 1, root_witness_count),
        check("source_v59_event_ledger_is_complete", len(source.get("v59_adaptive_xt_audit_rows", [])) == EXPECTED_SOURCE_V59_AUDIT_ROWS, source_v59_count),
        check("parent_v59_reconstructs_at_signed_revision", parent_reconstructed, parent_v59.REVISION),
        check("bounded_frontier_records_are_committed", 1 <= len(records) <= arguments.target_node_evaluations and records[0]["refinement_path"] == EXPECTED_PATH, [row["refinement_path"] for row in records]),
        check("total_and_v59_node_counts_increment_by_records", int(state["node_evaluation_count"]) == int(source["node_evaluation_count"]) + len(records) and int(state["v59_node_evaluation_count"]) == int(source.get("v59_node_evaluation_count", 0)) + len(records), (state["node_evaluation_count"], state["v59_node_evaluation_count"])),
        check("v58_frontier_node_count_does_not_increment", int(state["v58_node_evaluation_count"]) == int(source["v58_node_evaluation_count"]), state["v58_node_evaluation_count"]),
        check("atomic_records_replay_exactly", base_5500.replay_records(source, state, "checkpoint_5513"), record["outcome"]),
        check("source_append_only_ledgers_are_preserved", state["accepted"][: len(source["accepted"])] == source["accepted"] and state["refinement_witnesses"][: len(source["refinement_witnesses"])] == source["refinement_witnesses"] and state["unresolved"][: len(source["unresolved"])] == source["unresolved"], "accepted/witness/unresolved prefixes"),
        check("source_audit_ledgers_are_preserved", source_audits_preserved, len(AUDIT_BINDINGS)),
        check("source_hash_ledger_is_current", carry["source_accepted_sha256"] == base_5499.canonical_digest(source["accepted"]) and carry["source_pending_sha256"] == base_5499.canonical_digest(source["stack"]) and carry["source_refinement_witnesses_sha256"] == base_5499.canonical_digest(source["refinement_witnesses"]) and carry["source_v59_audit_sha256"] == base_5499.canonical_digest(source.get("v59_adaptive_xt_audit_rows", [])), carry["source_state_sha256"]),
        check("proof_cache_cannot_leak_to_other_bindings", cache_rows_scoped, event_count("TERMINAL")),
        check("exact_partition_volume_is_preserved", partition_error == 0, float(partition_error)),
        check("every_completed_nested_final_branch_union_is_exact", completed_nested_unions_certified, nested_union_rows),
        check("completed_final_branch_closes_active_cuboid_exactly", not active_closure_required or active_closure_certified, {"required": active_closure_required, "final_branch_pending": final_branch_pending, "final_branch_unresolved": final_branch_unresolved, "final_branch_accepted_paths": sorted(final_branch_accepted_paths), "union": active_union}),
        check("active_cuboid_flag_matches_exact_gate", state["valid_for_parent_v59_active_cuboid"] == active_closure_certified, active_closure_certified),
        check("formalization_workbench_untouched", before_formalization == after_formalization, f"before={len(before_formalization)};after={len(after_formalization)}"),
        check("broader_claims_remain_false", not state["valid_for_full_outer_parent_leaf_enclosure"] and not state["valid_for_D4_event_local_W3_bound"] and not state["valid_for_all_operator_local_GR_claim"] and not state["valid_for_full_MTS_claim"], "active cuboid is not broader local-GR closure"),
    ]
    failed = [row for row in validations if not row["passed"]]
    if failed:
        state["valid_for_parent_v59_active_cuboid"] = False
        decision = "PARENT_V59_ACTIVE_CUBOID_CLOSURE_NOT_CERTIFIED"
    elif state["unresolved"]:
        decision = "PARENT_V59_FINAL_BRANCH_UNRESOLVED__DERIVE_REPAIR"
    elif active_closure_certified:
        decision = "PARENT_V59_ACTIVE_CUBOID_CERTIFIED__OUTER_TRANSPLANT_NEXT"
    elif str(record["outcome"]).startswith("REFINED_"):
        decision = "PARENT_V59_FINAL_BRANCH_REFINED__CONTINUE"
    elif state["stack"]:
        decision = "PARENT_V59_FINAL_BRANCH_PARTIAL__RESUME"
    else:
        decision = "PARENT_V59_EMPTY_FRONTIER_WITHOUT_ROOT_CERTIFICATE"
    state["decision"] = decision
    base_5467.atomic_json(STATE, state, compact=True)
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
        "final_branch_complete": active_closure_required,
        "final_branch_accepted_leaf_count": len(final_branch_accepted_paths),
        "completed_nested_union_count": len(completed_nested_unions),
        "certified_completed_nested_union_count": sum(
            row["branch_certified"] for row in completed_nested_unions
        ),
        "full_nested_chain_certified": full_nested_chain_certified,
        "exact_active_cuboid_closure": active_closure_certified,
        "active_cuboid_leaf_count": len(active_leaf_paths),
        "active_cuboid_integrated_regular_path_abs_upper": active_union["integrated_regular_path_abs_upper"],
        "active_cuboid_amplitude_denominator_abs_lower": active_union["minimum_amplitude_denominator_abs_lower"],
        "active_cuboid_relative_root_abs_lower": active_union["minimum_relative_root_abs_lower"],
        "active_cuboid_selected_global_root_abs_lower": active_union["minimum_selected_global_root_abs_lower"],
        "active_cuboid_collision_jacobian_abs_lower": active_union["collision_jacobian_abs_lower"],
        "all_accepted_paths_unique": all_accepted_paths_unique,
        "all_accepted_bounds_positive": all_accepted_bounds_positive,
        "partition_volume_error": float(partition_error),
        "validation_row_count": len(validations),
        "failed_validation_count": len(failed),
        "valid_for_parent_v59_active_cuboid": state["valid_for_parent_v59_active_cuboid"],
        "valid_for_full_outer_parent_leaf_enclosure": False,
        "valid_for_D4_event_local_W3_bound": False,
        "valid_for_all_operator_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
        "next_target": state["stack"][-1]["refinement_path"] if state["stack"] and not state["unresolved"] else ("OUTER_TRANSPLANT" if active_closure_certified else "DERIVE_LOCAL_REPAIR"),
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
    base_5467.atomic_csv(NESTED_UNION_AUDIT, nested_union_rows)
    base_5467.atomic_csv(UNION_AUDIT, [{
        "union_id": "complete_active_cuboid",
        "final_branch_complete": active_closure_required,
        "final_branch_accepted_leaf_count": len(final_branch_accepted_paths),
        "all_accepted_paths_unique": all_accepted_paths_unique,
        "all_accepted_bounds_positive": all_accepted_bounds_positive,
        **active_union,
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
        "final_branch_complete",
        "final_branch_accepted_leaf_count",
        "exact_active_cuboid_closure",
        "partition_volume_error",
        "failed_validation_count",
        "next_target",
    )}, indent=2))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
