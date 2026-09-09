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
from fractions import Fraction
from pathlib import Path
from typing import Any


POST = Path(__file__).resolve().parents[1]
SCRIPTS = POST / "scripts"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
OUTPUT = FUNCTIONAL_RG / "5498"
WORK = OUTPUT / "work-v1"

SCRIPT_5496 = SCRIPTS / "Y5_R2FR_5496_D4_parent_v58_adaptive_stable_edge_T2_gate.py"
SCRIPT_5497 = SCRIPTS / "Y5_R2FR_5497_D4_parent_v58_hash_locked_frontier_migration.py"
SOURCE_STATE = (
    FUNCTIONAL_RG
    / "5497"
    / "work-v1"
    / "E07__U051__RIGHT_CONNECTOR__CUBOID__6df3d70a73e4618b.json"
)
RESULT_5497 = FUNCTIONAL_RG / "5497" / "D4_parent_v58_hash_locked_frontier_migration_result.json"
VALIDATION_5497 = FUNCTIONAL_RG / "5497" / "P8_Y5_BRR5496_5497_VALIDATION.csv"
SOURCE_REGISTER_5497 = FUNCTIONAL_RG / "5497" / "source_register.csv"
COLLAPSE_AUDIT_5497 = FUNCTIONAL_RG / "5497" / "D4_parent_v58_frontier_collapse_audit.csv"
SUPERSESSION_AUDIT_5497 = FUNCTIONAL_RG / "5497" / "D4_parent_v58_witness_supersession_audit.csv"
CERTIFICATE_5496 = FUNCTIONAL_RG / "5496" / "D4_parent_v58_adaptive_complete_amplitude_certificate.json"

TARGET_CUBOID_ID = "E07__U051__RIGHT_CONNECTOR__CUBOID__6df3d70a73e4618b"
STATE = WORK / f"{TARGET_CUBOID_ID}.json"
NODE_AUDIT = OUTPUT / "D4_parent_v58_one_atomic_frontier_node_audit.csv"
V58_AUDIT = OUTPUT / "D4_parent_v58_frontier_certificate_application_audit.csv"
V57_AUDIT = OUTPUT / "D4_parent_v58_frontier_scoped_certificate_audit.csv"
JACOBIAN_XT_AUDIT = OUTPUT / "D4_parent_v58_frontier_collision_jacobian_xt_audit.csv"
STABLE_XT_AUDIT = OUTPUT / "D4_parent_v58_frontier_stable_edge_xt_audit.csv"
PIVOT_AUDIT = OUTPUT / "D4_parent_v58_frontier_first_spinor_pivot_audit.csv"
STABLE_T_AUDIT = OUTPUT / "D4_parent_v58_frontier_stable_edge_t_audit.csv"
JACOBIAN_T_AUDIT = OUTPUT / "D4_parent_v58_frontier_collision_jacobian_t_audit.csv"
SOURCE_REGISTER = OUTPUT / "source_register.csv"
VALIDATION = OUTPUT / "P8_Y5_BRR5497_5498_VALIDATION.csv"
STATUS = OUTPUT / "status.json"
RESULT = OUTPUT / "D4_parent_v58_one_atomic_frontier_node_result.json"
DOCUMENT = POST / "5498-Y5-R2FR-D4-parent-v58-one-atomic-frontier-node.md"

CHECKPOINT = 5498
REVISION = "D4-parent-v58-one-atomic-frontier-node-v1"
PARENT_V58_REVISION = "D4-deformed-contour-regular-away-W3-v58-adaptive-stable-edge-local-T2-union"
EXPECTED_NEXT_PATH = "R_E0S_E0S_E1S"
EXPECTED_PENDING_PATHS = (
    "R_E1S",
    "R_E0S_E1S",
    EXPECTED_NEXT_PATH,
)
EXPECTED_SOURCE_COUNTS = (179, 3, 0)
EXPECTED_SCRIPT_5497_SHA256 = "288bea08b37f0a55512655549f214e0aae3364052ad8848ab06c960177bb9dda"
EXPECTED_SOURCE_STATE_SHA256 = "0bb34051ffe2e603d6429fd2a6aab76b285633f2a81db0e63787f2c73024a69f"
EXPECTED_RESULT_5497_SHA256 = "dec831e177792de709bc7682fff29b5493a5b2455ffdc1e2cd265150c77efa50"
EXPECTED_VALIDATION_5497_SHA256 = "86a473b6543f518170ca9a3e537f5edbce71e6fbca16f36b555f5e2bcef429bf"
EXPECTED_SOURCE_REGISTER_5497_SHA256 = "a42d5fa53c71e17d58bc53a01c9aaaeb7880fce9582d89365c3c956160887189"
EXPECTED_COLLAPSE_AUDIT_5497_SHA256 = "9163b5d04a42dffefbde65514b305d28f27f88468428af256cdb911adf6579a4"
EXPECTED_SUPERSESSION_AUDIT_5497_SHA256 = "46437fda565489290015561880c3dd8695f85dc06653884bcc7460182b3cdfa0"
EXPECTED_CERTIFICATE_5496_SHA256 = "27dc7fce1f83b424e9d9341778a392b83ed7c8659d12e05afd561338782fc708"

AUDIT_BINDINGS = (
    (
        "v58_certificate_application_audit_rows",
        "V58_ADAPTIVE_CERTIFICATE_AUDIT_ROWS",
        V58_AUDIT,
    ),
    (
        "v57_scoped_certificate_audit_rows",
        "V57_SCOPED_CERTIFICATE_AUDIT_ROWS",
        V57_AUDIT,
    ),
    (
        "v56_collision_jacobian_xt_audit_rows",
        "V56_COLLISION_JACOBIAN_XT_LEAF_UNION_AUDIT_ROWS",
        JACOBIAN_XT_AUDIT,
    ),
    (
        "v56_stable_edge_xt_audit_rows",
        "V55_STABLE_EDGE_XT_LEAF_UNION_AUDIT_ROWS",
        STABLE_XT_AUDIT,
    ),
    (
        "v56_first_spinor_pivot_audit_rows",
        "V54_FIRST_SPINOR_PIVOT_T_LEAF_UNION_AUDIT_ROWS",
        PIVOT_AUDIT,
    ),
    (
        "v56_stable_edge_t_audit_rows",
        "V53_STABLE_EDGE_T_LEAF_UNION_AUDIT_ROWS",
        STABLE_T_AUDIT,
    ),
    (
        "v56_collision_jacobian_t_audit_rows",
        "V52_COLLISION_JACOBIAN_LEAF_UNION_AUDIT_ROWS",
        JACOBIAN_T_AUDIT,
    ),
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


def exact_coordinate(value: Any) -> Fraction:
    return Fraction(str(value))


def exact_node_volume(row: dict[str, Any]) -> Fraction:
    volume = Fraction(1)
    for lower, upper in (
        ("epsilon_real_lower", "epsilon_real_upper"),
        ("x_lower", "x_upper"),
        ("t_lower", "t_upper"),
    ):
        volume *= exact_coordinate(row[upper]) - exact_coordinate(row[lower])
    return volume


def exact_partition_volume(state: dict[str, Any]) -> Fraction:
    return sum(
        (
            exact_node_volume(row)
            for row in state["accepted"] + state["stack"] + state["unresolved"]
        ),
        start=Fraction(0),
    )


def source_paths(base_5496: Any, base_5495: Any) -> tuple[Path, ...]:
    return tuple(
        dict.fromkeys(
            (
                Path(__file__).resolve(),
                *base_5496.source_paths(base_5495),
                SCRIPT_5497,
                SOURCE_STATE,
                RESULT_5497,
                VALIDATION_5497,
                SOURCE_REGISTER_5497,
                COLLAPSE_AUDIT_5497,
                SUPERSESSION_AUDIT_5497,
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


def carry_forward_state(source: dict[str, Any]) -> dict[str, Any]:
    state = deepcopy(source)
    state["checkpoint"] = CHECKPOINT
    state["revision"] = REVISION
    state["parent_revision"] = PARENT_V58_REVISION
    history = list(state.get("parent_revision_history", []))
    if PARENT_V58_REVISION not in history:
        history.append(PARENT_V58_REVISION)
    state["parent_revision_history"] = history
    state["v58_frontier_carry_forward"] = {
        "source_checkpoint": 5497,
        "source_state_path": str(SOURCE_STATE),
        "source_state_sha256": EXPECTED_SOURCE_STATE_SHA256,
        "source_accepted_sha256": canonical_digest(source["accepted"]),
        "source_pending_sha256": canonical_digest(source["stack"]),
        "source_unresolved_sha256": canonical_digest(source["unresolved"]),
        "source_refinement_witnesses_sha256": canonical_digest(
            source["refinement_witnesses"]
        ),
        "carried_counts": list(EXPECTED_SOURCE_COUNTS),
        "carried_utc": datetime.now(timezone.utc).isoformat(),
    }
    state["processed_this_run"] = 0
    state["decision"] = "PARENT_V58_FRONTIER_PARTIAL__RESUME"
    state["valid_for_parent_v58_active_cuboid"] = False
    state["valid_for_full_outer_parent_leaf_enclosure"] = False
    state["valid_for_D4_event_local_W3_bound"] = False
    state["valid_for_all_operator_local_GR_claim"] = False
    state["valid_for_full_MTS_claim"] = False
    return state


def reconstruct_parent(
    base_5467: Any,
    base_5472: Any,
    base_5474: Any,
    base_5476: Any,
    base_5478: Any,
    base_5483: Any,
    base_5490: Any,
    base_5493: Any,
    base_5495: Any,
    base_5496: Any,
    certificate_5496: dict[str, Any],
) -> Any:
    result_5492 = read_json(base_5495.RESULT_5492)
    work_state_5492 = read_json(base_5495.WORK_STATE_5492)
    leaf_rows_5492 = read_csv(base_5495.LEAF_AUDIT_5492)
    binding_5493 = read_json(base_5495.BINDING_5493)
    certificate_parent = base_5490.fresh_v56(
        base_5467,
        base_5472,
        base_5474,
        base_5476,
        base_5478,
        base_5483,
    )
    collision_certificate = base_5493.build_certificate(
        certificate_parent,
        result_5492,
        work_state_5492,
        leaf_rows_5492,
    )
    parent_v57, _ = base_5495.fresh_v57_with_v54_handle(
        base_5467,
        base_5472,
        base_5474,
        base_5476,
        base_5478,
        base_5483,
        base_5493,
        binding_5493,
        collision_certificate,
        "mts_parent_v58_frontier_5498",
    )
    return base_5496.install_parent_v58(
        base_5495,
        parent_v57,
        certificate_5496["target_binding_sha256"],
        certificate_5496["aggregate_result"],
    )


def process_one_node(
    base_5467: Any,
    base_5468: Any,
    base_5469: Any,
    stable: Any,
    parent_v58: Any,
    cells: dict[str, Any],
    support_segments: list[dict[str, Any]],
    branches: dict[str, Any],
    cuboid: dict[str, Any],
    source: dict[str, Any],
    maximum_refinement_depth: int,
) -> tuple[dict[str, Any], dict[str, Any]]:
    state = carry_forward_state(source)
    node = deepcopy(state["stack"][-1])
    if node.get("refinement_path") != EXPECTED_NEXT_PATH:
        raise RuntimeError("checkpoint-5498 LIFO frontier path changed")
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
    compact["certificate_source"] = "checkpoint_5498_parent_v58"
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
                state["split_axis_counts"][axis] = int(
                    state["split_axis_counts"][axis]
                ) + 1
                children = [lower_child, upper_child]
                outcome = f"REFINED_{str(axis).upper()}2"
    new_audit_counts: dict[str, int] = {}
    for state_key, parent_attribute, _ in AUDIT_BINDINGS:
        new_rows = list(getattr(parent_v58, parent_attribute, []))
        state.setdefault(state_key, []).extend(new_rows)
        new_audit_counts[state_key] = len(new_rows)
    state["v58_node_evaluation_count"] = int(
        state.get("v58_node_evaluation_count", 0)
    ) + 1
    state["v58_accepted_subcuboid_count"] = int(
        state.get("v58_accepted_subcuboid_count", 0)
    ) + (1 if outcome == "ACCEPTED" else 0)
    state["v58_refinement_witness_count"] = int(
        state.get("v58_refinement_witness_count", 0)
    ) + (0 if outcome == "ACCEPTED" else 1)
    state["runtime_seconds"] = float(state.get("runtime_seconds", 0.0)) + runtime_seconds
    state["processed_this_run"] = 1
    state["accepted_subcuboid_count"] = len(state["accepted"])
    state["pending_subcuboid_count"] = len(state["stack"])
    state["unresolved_subcuboid_count"] = len(state["unresolved"])
    state["accepted_volume"] = math.fsum(
        base_5469.node_volume(row) for row in state["accepted"]
    )
    state["coverage_error"] = float(
        abs(exact_partition_volume(state) - exact_node_volume(state["root"]))
    )
    state["decision"] = "PARENT_V58_FRONTIER_PARTIAL__RESUME"
    state["valid_for_parent_v58_active_cuboid"] = False
    state["valid_for_full_outer_parent_leaf_enclosure"] = False
    state["valid_for_D4_event_local_W3_bound"] = False
    state["valid_for_all_operator_local_GR_claim"] = False
    state["valid_for_full_MTS_claim"] = False
    record = {
        "checkpoint": CHECKPOINT,
        "source_state_sha256": EXPECTED_SOURCE_STATE_SHA256,
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
        "child_paths": "|".join(str(row["refinement_path"]) for row in children),
        "runtime_seconds": runtime_seconds,
        "v58_application_count": new_audit_counts[
            "v58_certificate_application_audit_rows"
        ],
        "new_audit_counts": new_audit_counts,
        "created_utc": datetime.now(timezone.utc).isoformat(),
    }
    state["atomic_node_5498"] = record
    state["last_update_utc"] = record["created_utc"]
    base_5467.atomic_json(STATE, state, compact=True)
    return state, record


def node_consequences_are_exact(
    source: dict[str, Any],
    state: dict[str, Any],
    record: dict[str, Any],
) -> bool:
    outcome = str(record["outcome"])
    expected = {
        "ACCEPTED": (180, 2, 0, 59),
        "REFINED_EPSILON2": (179, 4, 0, 60),
        "REFINED_X2": (179, 4, 0, 60),
        "REFINED_T2": (179, 4, 0, 60),
        "UNRESOLVED_DEPTH_LIMIT": (179, 2, 1, 60),
        "UNRESOLVED_NO_SPLIT": (179, 2, 1, 60),
    }
    actual = (
        len(state["accepted"]),
        len(state["stack"]),
        len(state["unresolved"]),
        len(state["refinement_witnesses"]),
    )
    if expected.get(outcome) != actual:
        return False
    return (
        state["accepted"][: len(source["accepted"])] == source["accepted"]
        and state["stack"][: len(source["stack"]) - 1] == source["stack"][:-1]
        and state["unresolved"][: len(source["unresolved"])] == source["unresolved"]
        and state["refinement_witnesses"][: len(source["refinement_witnesses"])]
        == source["refinement_witnesses"]
    )


def render_document(payload: dict[str, Any], base_5467: Any) -> None:
    lines = [
        "# 5498: D4 parent-v58 one atomic frontier node",
        "",
        "The checkpoint-5497 `179/3/0` frontier is hash locked and carried without reinterpretation. The full source-derived parent chain through v58 evaluates exactly one LIFO node, `R_E0S_E0S_E1S`, at epsilon `[0.0025,0.005]`.",
        "",
        f"Outcome: `{payload['node_outcome']}`. Frontier: `{payload['accepted_subcuboid_count']}/{payload['pending_subcuboid_count']}/{payload['unresolved_subcuboid_count']}`. Runtime: `{payload['node_runtime_seconds']}` seconds.",
        "",
        f"V58 certificate applications on this node: `{payload['new_v58_application_count']}`. Exact partition-volume error: `{payload['partition_volume_error']}`.",
        "",
        f"**{payload['decision']}**",
        "",
        "This one-node result does not certify the complete active cuboid, full outer enclosure, event-local or combined W3, the regulator limit, all-operator local GR or full MTS.",
        "",
    ]
    base_5467.atomic_text(DOCUMENT, "\n".join(lines))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--maximum-refinement-depth", type=int, default=33)
    arguments = parser.parse_args()
    if arguments.maximum_refinement_depth < 3:
        raise ValueError("maximum refinement depth cannot exclude the source node")
    base_5496 = load_module("mts_5496_for_5498", SCRIPT_5496)
    base_5495 = load_module("mts_5495_for_5498", base_5496.SCRIPT_5495)
    base_5467 = load_module("mts_5467_for_5498", base_5495.SCRIPT_5467)
    base_5468 = load_module("mts_5468_for_5498", base_5495.SCRIPT_5468)
    base_5469 = load_module("mts_5469_for_5498", base_5495.SCRIPT_5469)
    base_5472 = load_module("mts_5472_for_5498", base_5495.SCRIPT_5472)
    base_5474 = load_module("mts_5474_for_5498", base_5495.SCRIPT_5474)
    base_5476 = load_module("mts_5476_for_5498", base_5495.SCRIPT_5476)
    base_5478 = load_module("mts_5478_for_5498", base_5495.SCRIPT_5478)
    base_5480 = load_module("mts_5480_for_5498", base_5495.SCRIPT_5480)
    base_5483 = load_module("mts_5483_for_5498", base_5495.SCRIPT_5483)
    base_5490 = load_module("mts_5490_for_5498", base_5495.SCRIPT_5490)
    base_5493 = load_module("mts_5493_for_5498", base_5495.SCRIPT_5493)
    base_5467.set_below_normal_priority()
    base_5480.set_single_core_affinity()
    before_formalization = base_5467.formalization_snapshot()
    paths = source_paths(base_5496, base_5495)
    missing = [str(path) for path in paths if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"missing sources: {missing}")
    inherited_hashes = {
        "script_5497": digest(SCRIPT_5497),
        "source_state": digest(SOURCE_STATE),
        "result_5497": digest(RESULT_5497),
        "validation_5497": digest(VALIDATION_5497),
        "source_register_5497": digest(SOURCE_REGISTER_5497),
        "collapse_audit_5497": digest(COLLAPSE_AUDIT_5497),
        "supersession_audit_5497": digest(SUPERSESSION_AUDIT_5497),
        "certificate_5496": digest(CERTIFICATE_5496),
    }
    expected_hashes = {
        "script_5497": EXPECTED_SCRIPT_5497_SHA256,
        "source_state": EXPECTED_SOURCE_STATE_SHA256,
        "result_5497": EXPECTED_RESULT_5497_SHA256,
        "validation_5497": EXPECTED_VALIDATION_5497_SHA256,
        "source_register_5497": EXPECTED_SOURCE_REGISTER_5497_SHA256,
        "collapse_audit_5497": EXPECTED_COLLAPSE_AUDIT_5497_SHA256,
        "supersession_audit_5497": EXPECTED_SUPERSESSION_AUDIT_5497_SHA256,
        "certificate_5496": EXPECTED_CERTIFICATE_5496_SHA256,
    }
    if inherited_hashes != expected_hashes:
        raise RuntimeError("checkpoint-5498 inherited source hash mismatch")
    source = read_json(SOURCE_STATE)
    result_5497 = read_json(RESULT_5497)
    validation_5497 = read_csv(VALIDATION_5497)
    register_5497 = read_csv(SOURCE_REGISTER_5497)
    certificate_5496 = read_json(CERTIFICATE_5496)
    source_counts = (
        len(source["accepted"]),
        len(source["stack"]),
        len(source["unresolved"]),
    )
    source_pending_paths = tuple(row["refinement_path"] for row in source["stack"])
    source_certified = (
        result_5497.get("decision")
        == "PARENT_V58_STATUS_ONLY_MIGRATION_CERTIFIED__RUN_ONE_FRONTIER_NODE"
        and int(result_5497.get("failed_validation_count", -1)) == 0
        and all(truth(row.get("passed")) for row in validation_5497)
        and source_register_is_current(register_5497)
        and source_counts == EXPECTED_SOURCE_COUNTS
        and source_pending_paths == EXPECTED_PENDING_PATHS
        and exact_partition_volume(source) == exact_node_volume(source["root"])
    )
    if not source_certified:
        raise RuntimeError("checkpoint-5497 frontier is not current and certified")
    stable, _, cells, support_segments, branches = base_5467.load_parent()
    cuboid = next(
        row
        for row in read_csv(base_5495.MANIFEST_5468)
        if row["cuboid_job_id"] == TARGET_CUBOID_ID
    )
    parent_v58 = reconstruct_parent(
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
                    "pending_paths": list(source_pending_paths),
                    "next_path": source["stack"][-1]["refinement_path"],
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
        record = state.get("atomic_node_5498")
        if not isinstance(record, dict):
            raise RuntimeError("checkpoint-5498 output state is incomplete")
    else:
        WORK.mkdir(parents=True, exist_ok=True)
        state, record = process_one_node(
            base_5467,
            base_5468,
            base_5469,
            stable,
            parent_v58,
            cells,
            support_segments,
            branches,
            cuboid,
            source,
            arguments.maximum_refinement_depth,
        )
    counts = (
        len(state["accepted"]),
        len(state["stack"]),
        len(state["unresolved"]),
    )
    partition_error_exact = abs(
        exact_partition_volume(state) - exact_node_volume(state["root"])
    )
    carry = state.get("v58_frontier_carry_forward", {})
    existing_v58_applications = len(
        source.get("v58_certificate_application_audit_rows", [])
    )
    current_v58_applications = len(
        state.get("v58_certificate_application_audit_rows", [])
    )
    new_v58_applications = current_v58_applications - existing_v58_applications
    formalization_after = base_5467.formalization_snapshot()
    validations = [
        check("all_sources_exist", not missing, len(paths)),
        check("checkpoint_5497_evidence_is_hash_locked", inherited_hashes == expected_hashes, inherited_hashes),
        check("checkpoint_5497_frontier_is_certified", source_certified, result_5497.get("decision")),
        check("source_frontier_is_exact_179_3_0", source_counts == EXPECTED_SOURCE_COUNTS, source_counts),
        check("source_pending_order_is_exact", source_pending_paths == EXPECTED_PENDING_PATHS, source_pending_paths),
        check("parent_v58_reconstructs_at_signed_revision", parent_v58.REVISION == PARENT_V58_REVISION and not parent_v58.V58_PARENT_ACTION_CHANGED and parent_v58.V58_ONLY_ENCLOSURE_COMPOSITION_CHANGED, parent_v58.REVISION),
        check("exactly_expected_lifo_node_is_consumed", record.get("refinement_path") == EXPECTED_NEXT_PATH, record.get("refinement_path")),
        check("exactly_one_node_is_evaluated", int(state["node_evaluation_count"]) == int(source["node_evaluation_count"]) + 1 and int(state["v58_node_evaluation_count"]) == int(source.get("v58_node_evaluation_count", 0)) + 1, state["node_evaluation_count"]),
        check("node_consequences_are_exact", node_consequences_are_exact(source, state, record), record.get("outcome")),
        check("source_ledgers_are_prefix_preserved", carry.get("source_accepted_sha256") == canonical_digest(source["accepted"]) and carry.get("source_pending_sha256") == canonical_digest(source["stack"]) and carry.get("source_unresolved_sha256") == canonical_digest(source["unresolved"]) and carry.get("source_refinement_witnesses_sha256") == canonical_digest(source["refinement_witnesses"]), carry.get("source_state_sha256")),
        check("v58_certificate_does_not_leak_outside_binding", int(record.get("v58_application_count", -1)) == 0 and new_v58_applications == 0, new_v58_applications),
        check("migrated_frontier_counts_are_coherent", int(state["accepted_subcuboid_count"]) == counts[0] and int(state["pending_subcuboid_count"]) == counts[1] and int(state["unresolved_subcuboid_count"]) == counts[2], counts),
        check("exact_partition_volume_is_preserved", partition_error_exact == 0, float(partition_error_exact)),
        check("one_node_record_is_source_bound", record.get("source_state_sha256") == EXPECTED_SOURCE_STATE_SHA256, record.get("source_state_sha256")),
        check("formalization_workbench_untouched", before_formalization == formalization_after, f"before={len(before_formalization)};after={len(formalization_after)}"),
        check("broad_claims_remain_false", not state["valid_for_parent_v58_active_cuboid"] and not state["valid_for_full_outer_parent_leaf_enclosure"] and not state["valid_for_D4_event_local_W3_bound"] and not state["valid_for_all_operator_local_GR_claim"] and not state["valid_for_full_MTS_claim"], "one frontier node only"),
    ]
    failed = [row for row in validations if not row["passed"]]
    decision = (
        "PARENT_V58_ONE_ATOMIC_FRONTIER_NODE_CERTIFIED__CONTINUE_FRONTIER"
        if not failed and not state["unresolved"]
        else (
            "PARENT_V58_ONE_ATOMIC_FRONTIER_NODE_CERTIFIED__DERIVE_LOCAL_REPAIR"
            if not failed
            else "PARENT_V58_ONE_ATOMIC_FRONTIER_NODE_NOT_CERTIFIED"
        )
    )
    payload = {
        "checkpoint": CHECKPOINT,
        "revision": REVISION,
        "parent_revision": PARENT_V58_REVISION,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "decision": decision,
        "target_cuboid_id": TARGET_CUBOID_ID,
        "evaluated_refinement_path": record["refinement_path"],
        "node_outcome": record["outcome"],
        "node_probe_passed": record["probe_passed"],
        "node_failure_type": record["failure_type"],
        "node_failure_message": record["failure_message"],
        "node_child_paths": record["child_paths"],
        "node_runtime_seconds": record["runtime_seconds"],
        "accepted_subcuboid_count": counts[0],
        "pending_subcuboid_count": counts[1],
        "unresolved_subcuboid_count": counts[2],
        "node_evaluation_count": state["node_evaluation_count"],
        "v58_node_evaluation_count": state["v58_node_evaluation_count"],
        "new_v58_application_count": new_v58_applications,
        "partition_volume_error": float(partition_error_exact),
        "source_state_sha256": EXPECTED_SOURCE_STATE_SHA256,
        "validation_row_count": len(validations),
        "failed_validation_count": len(failed),
        "valid_for_parent_v58_one_atomic_frontier_node": not failed,
        "valid_for_parent_v58_active_cuboid": False,
        "valid_for_full_outer_parent_leaf_enclosure": False,
        "valid_for_D4_event_local_W3_bound": False,
        "valid_for_all_operator_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
        "next_target": (
            state["stack"][-1]["refinement_path"]
            if state["stack"] and not state["unresolved"]
            else "DERIVE_LOCAL_REPAIR"
        ),
    }
    base_5467.atomic_csv(NODE_AUDIT, [record])
    for state_key, _, output_path in AUDIT_BINDINGS:
        if state.get(state_key):
            base_5467.atomic_csv(output_path, state[state_key])
    base_5467.atomic_csv(
        SOURCE_REGISTER,
        [
            {
                "source_path": str(path),
                "sha256": digest(path),
                "exists": path.is_file(),
            }
            for path in paths
        ],
    )
    base_5467.atomic_csv(VALIDATION, validations)
    base_5467.atomic_json(STATUS, payload)
    base_5467.atomic_json(RESULT, payload)
    render_document(payload, base_5467)
    print(
        json.dumps(
            {
                key: payload[key]
                for key in (
                    "decision",
                    "evaluated_refinement_path",
                    "node_outcome",
                    "node_probe_passed",
                    "accepted_subcuboid_count",
                    "pending_subcuboid_count",
                    "unresolved_subcuboid_count",
                    "new_v58_application_count",
                    "partition_volume_error",
                    "node_runtime_seconds",
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
