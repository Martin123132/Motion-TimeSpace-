from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


POST = Path(__file__).resolve().parents[1]
SCRIPTS = POST / "scripts"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
FORMALIZATION = POST.parent / "formalization-workbench"
OUTPUT = FUNCTIONAL_RG / "5475"
WORK = OUTPUT / "work-v1"

SCRIPT_5467 = SCRIPTS / "Y5_R2FR_5467_D4_all_outer_leaf_epsilon_fiber_transplant_runner.py"
SCRIPT_5468 = SCRIPTS / "Y5_R2FR_5468_D4_exact_outer_cuboid_coalescence_runner.py"
SCRIPT_5469 = SCRIPTS / "Y5_R2FR_5469_D4_resumable_three_axis_cuboid_certificate_runner.py"
SCRIPT_5472 = SCRIPTS / "Y5_R2FR_5472_D4_parent_v52_collision_jacobian_leaf_union_integration_gate.py"
SCRIPT_5473 = SCRIPTS / "Y5_R2FR_5473_D4_parent_v52_hash_locked_frontier_runner.py"
SCRIPT_5474 = SCRIPTS / "Y5_R2FR_5474_D4_parent_v53_stable_edge_t_leaf_union_integration_gate.py"
RESULT_5473 = FUNCTIONAL_RG / "5473" / "D4_parent_v52_hash_locked_frontier_result.json"
VALIDATION_5473 = FUNCTIONAL_RG / "5473" / "P8_Y5_BRR5472_5473_VALIDATION.csv"
RESULT_5474 = FUNCTIONAL_RG / "5474" / "D4_parent_v53_stable_edge_t_leaf_union_result.json"
VALIDATION_5474 = FUNCTIONAL_RG / "5474" / "P8_Y5_BRR5473_5474_VALIDATION.csv"
MANIFEST_5468 = FUNCTIONAL_RG / "5468" / "D4_exact_outer_cuboid_manifest.csv"

TARGET_CUBOID_ID = "E07__U051__RIGHT_CONNECTOR__CUBOID__6df3d70a73e4618b"
SOURCE_STATE_5473 = FUNCTIONAL_RG / "5473" / "work-v1" / f"{TARGET_CUBOID_ID}.json"
STATE = WORK / f"{TARGET_CUBOID_ID}.json"

STABLE_EDGE_AUDIT = OUTPUT / "D4_parent_v53_frontier_stable_edge_t_leaf_union_audit.csv"
JACOBIAN_AUDIT = OUTPUT / "D4_parent_v53_frontier_collision_jacobian_leaf_union_audit.csv"
CERTIFICATE = OUTPUT / "D4_parent_v53_active_cuboid_certificate.json"
SOURCE_REGISTER = OUTPUT / "source_register.csv"
VALIDATION = OUTPUT / "P8_Y5_BRR5474_5475_VALIDATION.csv"
STATUS = OUTPUT / "status.json"
RESULT = OUTPUT / "D4_parent_v53_hash_locked_frontier_result.json"
DOCUMENT = POST / "5475-Y5-R2FR-D4-parent-v53-hash-locked-frontier-runner.md"

CHECKPOINT = 5475
REVISION = "D4-parent-v53-hash-locked-frontier-runner-v1"
PARENT_V51_REVISION = "D4-deformed-contour-regular-away-W3-v51"
PARENT_V52_REVISION = "D4-deformed-contour-regular-away-W3-v52-leaf-union"
PARENT_V53_REVISION = "D4-deformed-contour-regular-away-W3-v53-stable-edge-t-leaf-union"
EXPECTED_SOURCE_LEAF_COUNT = 39_732


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


def source_paths() -> tuple[Path, ...]:
    return (
        Path(__file__).resolve(),
        SCRIPT_5467,
        SCRIPT_5468,
        SCRIPT_5469,
        SCRIPT_5472,
        SCRIPT_5473,
        SCRIPT_5474,
        RESULT_5473,
        VALIDATION_5473,
        RESULT_5474,
        VALIDATION_5474,
        MANIFEST_5468,
        SOURCE_STATE_5473,
    )


def carry_forward_state(base_5467: Any) -> dict[str, Any]:
    source = read_json(SOURCE_STATE_5473)
    if source["cuboid_job_id"] != TARGET_CUBOID_ID:
        raise RuntimeError("checkpoint 5473 source state has the wrong cuboid id")
    if source["unresolved"]:
        raise RuntimeError("checkpoint 5473 source state is not cleanly resumable")
    source_revision = source.get("revision", "")
    source["checkpoint"] = CHECKPOINT
    source["revision"] = REVISION
    source["parent_revision"] = PARENT_V53_REVISION
    source["parent_revision_history"] = [
        PARENT_V51_REVISION,
        PARENT_V52_REVISION,
        PARENT_V53_REVISION,
    ]
    source["v53_carry_forward"] = {
        "source_checkpoint": 5473,
        "source_state_path": str(SOURCE_STATE_5473),
        "source_state_sha256": digest(SOURCE_STATE_5473),
        "source_revision": source_revision,
        "carried_accepted_subcuboid_count": len(source["accepted"]),
        "carried_pending_subcuboid_count": len(source["stack"]),
        "carried_unresolved_subcuboid_count": len(source["unresolved"]),
        "carried_utc": datetime.now(timezone.utc).isoformat(),
        "carry_rule": (
            "v53 returns the unchanged v52 evaluation unless the precise "
            "connector edge_2_1_3 stable-edge singularity triggers"
        ),
    }
    source["v53_node_evaluation_count"] = 0
    source["v53_accepted_subcuboid_count"] = 0
    source["v53_refinement_witness_count"] = 0
    source["v53_stable_edge_t_leaf_union_audit_rows"] = []
    source["v53_collision_jacobian_leaf_union_audit_rows"] = []
    source["decision"] = "PARENT_V53_FRONTIER_PARTIAL__RESUME"
    base_5467.atomic_json(STATE, source, compact=True)
    return source


def partition_volume(base_5469: Any, state: dict[str, Any]) -> float:
    return sum(
        base_5469.node_volume(row)
        for row in state["accepted"] + state["stack"] + state["unresolved"]
    )


def check(gate: str, passed: bool, evidence: Any) -> dict[str, Any]:
    return {
        "checkpoint": CHECKPOINT,
        "validation_gate": gate,
        "passed": bool(passed),
        "evidence": evidence,
    }


def render_document(payload: dict[str, Any], base_5467: Any) -> None:
    lines = [
        "# 5475: D4 parent-v53 hash-locked frontier runner",
        "",
        "## Carry-forward contract",
        "",
        "The checkpoint-5473 v52 state is preserved byte-for-byte. This checkpoint owns a separate hash-locked copy. Every earlier accepted subcuboid remains valid because v53 invokes its exact t-leaf union only after the precise stable-edge singularity; otherwise it returns the unchanged v52 result.",
        "",
        "## Current result",
        "",
        f"Accepted: `{payload['accepted_subcuboid_count']}`. Pending: `{payload['pending_subcuboid_count']}`. Unresolved: `{payload['unresolved_subcuboid_count']}`.",
        "",
        f"V53 node evaluations: `{payload['v53_node_evaluation_count']}`. V53 accepted: `{payload['v53_accepted_subcuboid_count']}`. Stable-edge audit rows: `{payload['v53_stable_edge_audit_row_count']}`.",
        "",
        "## Decision",
        "",
        f"**{payload['decision']}**",
        "",
        "## Claim boundary",
        "",
        "Only this active coalesced cuboid is under reconstruction. Full outer-cover, W3, regulator-limit, local-GR, and full-MTS claims remain false.",
        "",
    ]
    base_5467.atomic_text(DOCUMENT, "\n".join(lines))


def run(
    maximum_node_evaluations: int,
    maximum_runtime_seconds: float,
    maximum_refinement_depth: int,
    status_only: bool,
) -> dict[str, Any]:
    base_5467 = load_module("mts_5467_for_5475", SCRIPT_5467)
    base_5468 = load_module("mts_5468_for_5475", SCRIPT_5468)
    base_5469 = load_module("mts_5469_for_5475", SCRIPT_5469)
    base_5472 = load_module("mts_5472_for_5475", SCRIPT_5472)
    base_5474 = load_module("mts_5474_for_5475", SCRIPT_5474)
    base_5467.set_below_normal_priority()
    before_formalization = base_5467.formalization_snapshot()
    missing = [str(path) for path in source_paths() if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"missing sources: {missing}")

    result_5473 = read_json(RESULT_5473)
    validation_5473 = read_csv(VALIDATION_5473)
    result_5474 = read_json(RESULT_5474)
    validation_5474 = read_csv(VALIDATION_5474)
    cuboid = next(
        row
        for row in read_csv(MANIFEST_5468)
        if row["cuboid_job_id"] == TARGET_CUBOID_ID
    )
    WORK.mkdir(parents=True, exist_ok=True)
    state = read_json(STATE) if STATE.is_file() else carry_forward_state(base_5467)
    source_hash = digest(SOURCE_STATE_5473)
    if state["v53_carry_forward"]["source_state_sha256"] != source_hash:
        raise RuntimeError("checkpoint 5473 source state changed after v53 carry-forward")

    accepted_before = len(state["accepted"])
    witnesses_before = len(state["refinement_witnesses"])
    nodes_before = int(state["node_evaluation_count"])
    stable_edge_audit: list[dict[str, Any]] = []
    jacobian_audit: list[dict[str, Any]] = []
    if state["stack"] and not state["unresolved"] and not status_only:
        stable, _, cells, support_segments, branches = base_5467.load_parent()
        parent_v53 = base_5474.install_parent_v53(
            base_5472.install_parent_v52(
                base_5472.fresh_parent(base_5467, "mts_parent_v53_for_5475")
            )
        )
        state = base_5469.process_state(
            base_5467,
            base_5468,
            stable,
            parent_v53,
            cells,
            support_segments,
            branches,
            cuboid,
            state,
            STATE,
            maximum_node_evaluations,
            maximum_runtime_seconds,
            maximum_refinement_depth,
        )
        stable_edge_audit = list(
            parent_v53.V53_STABLE_EDGE_T_LEAF_UNION_AUDIT_ROWS
        )
        jacobian_audit = list(
            parent_v53.V52_COLLISION_JACOBIAN_LEAF_UNION_AUDIT_ROWS
        )
        for row in state["accepted"][accepted_before:]:
            row["certificate_source"] = "checkpoint_5475_parent_v53"
            row["parent_revision"] = PARENT_V53_REVISION
        for row in state["refinement_witnesses"][witnesses_before:]:
            row["certificate_source"] = "checkpoint_5475_parent_v53_witness"
            row["parent_revision"] = PARENT_V53_REVISION
        state["v53_node_evaluation_count"] = int(
            state.get("v53_node_evaluation_count", 0)
        ) + int(state["node_evaluation_count"]) - nodes_before
        state["v53_accepted_subcuboid_count"] = int(
            state.get("v53_accepted_subcuboid_count", 0)
        ) + len(state["accepted"]) - accepted_before
        state["v53_refinement_witness_count"] = int(
            state.get("v53_refinement_witness_count", 0)
        ) + len(state["refinement_witnesses"]) - witnesses_before
        state.setdefault("v53_stable_edge_t_leaf_union_audit_rows", []).extend(
            stable_edge_audit
        )
        state.setdefault("v53_collision_jacobian_leaf_union_audit_rows", []).extend(
            jacobian_audit
        )
        base_5467.atomic_json(STATE, state, compact=True)

    if state.get("v53_stable_edge_t_leaf_union_audit_rows"):
        base_5467.atomic_csv(
            STABLE_EDGE_AUDIT,
            state["v53_stable_edge_t_leaf_union_audit_rows"],
        )
    if state.get("v53_collision_jacobian_leaf_union_audit_rows"):
        base_5467.atomic_csv(
            JACOBIAN_AUDIT,
            state["v53_collision_jacobian_leaf_union_audit_rows"],
        )

    partition_total = partition_volume(base_5469, state)
    partition_error = abs(partition_total - float(state["root_volume"]))
    partition_tolerance = 1.0e-12 * max(float(state["root_volume"]), 1.0)
    complete = (
        bool(state["accepted"])
        and not state["stack"]
        and not state["unresolved"]
        and partition_error <= partition_tolerance
    )
    state["decision"] = (
        "PARENT_V53_ACTIVE_CUBOID_CERTIFIED"
        if complete
        else (
            "PARENT_V53_FRONTIER_REACHES_UNRESOLVED__DERIVE_LOCAL_REPAIR"
            if state["unresolved"]
            else "PARENT_V53_FRONTIER_PARTIAL__RESUME"
        )
    )
    state["valid_for_parent_v53_active_cuboid"] = complete
    state["valid_for_full_outer_parent_leaf_enclosure"] = False
    state["valid_for_D4_event_local_W3_bound"] = False
    state["valid_for_all_operator_local_GR_claim"] = False
    state["valid_for_full_MTS_claim"] = False
    base_5467.atomic_json(STATE, state, compact=True)

    if complete:
        certificate = {
            "checkpoint": CHECKPOINT,
            "revision": REVISION,
            "parent_revision": PARENT_V53_REVISION,
            "cuboid_job_id": TARGET_CUBOID_ID,
            "source_fiber_count": int(cuboid["source_fiber_count"]),
            "source_leaf_count": int(cuboid["source_leaf_count"]),
            "source_fiber_membership_sha256": cuboid[
                "source_fiber_membership_sha256"
            ],
            "accepted_subcuboid_count": len(state["accepted"]),
            "integrated_regular_path_abs_upper": sum(
                float(row["integrated_regular_path_abs_upper"])
                for row in state["accepted"]
            ),
            "minimum_amplitude_denominator_abs_lower": min(
                float(row["minimum_amplitude_denominator_abs_lower"])
                for row in state["accepted"]
            ),
            "minimum_relative_root_abs_lower": min(
                float(row["relative_root_abs_lower"]) for row in state["accepted"]
            ),
            "minimum_selected_global_root_abs_lower": min(
                float(row["selected_global_root_abs_lower"])
                for row in state["accepted"]
            ),
            "minimum_collision_jacobian_abs_lower": min(
                float(row["collision_jacobian_abs_lower"])
                for row in state["accepted"]
            ),
            "partition_volume_error": partition_error,
            "certificate_source": "checkpoint_5475_v51_v52_carry_plus_v53_frontier",
            "valid_for_parent_v53_active_cuboid": True,
            "valid_for_full_outer_parent_leaf_enclosure": False,
            "valid_for_D4_event_local_W3_bound": False,
            "valid_for_all_operator_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
        }
        base_5467.atomic_json(CERTIFICATE, certificate)

    after_formalization = base_5467.formalization_snapshot()
    payload: dict[str, Any] = {
        "checkpoint": CHECKPOINT,
        "revision": REVISION,
        "parent_revision": PARENT_V53_REVISION,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "decision": state["decision"],
        "target_cuboid_id": TARGET_CUBOID_ID,
        "source_fiber_count": int(cuboid["source_fiber_count"]),
        "source_leaf_count": int(cuboid["source_leaf_count"]),
        "accepted_subcuboid_count": len(state["accepted"]),
        "pending_subcuboid_count": len(state["stack"]),
        "unresolved_subcuboid_count": len(state["unresolved"]),
        "node_evaluation_count": int(state["node_evaluation_count"]),
        "v53_node_evaluation_count": int(state["v53_node_evaluation_count"]),
        "v53_accepted_subcuboid_count": int(
            state["v53_accepted_subcuboid_count"]
        ),
        "v53_refinement_witness_count": int(
            state["v53_refinement_witness_count"]
        ),
        "v53_stable_edge_audit_row_count": len(
            state.get("v53_stable_edge_t_leaf_union_audit_rows", [])
        ),
        "v53_collision_jacobian_audit_row_count": len(
            state.get("v53_collision_jacobian_leaf_union_audit_rows", [])
        ),
        "processed_this_run": (
            0 if status_only else int(state.get("processed_this_run", 0))
        ),
        "partition_volume_error": partition_error,
        "source_state_5473_sha256": source_hash,
        "valid_for_parent_v53_active_cuboid": complete,
        "valid_for_full_outer_parent_leaf_enclosure": False,
        "valid_for_D4_event_local_W3_bound": False,
        "valid_for_all_operator_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
        "next_target": (
            "RECONCILE_ACTIVE_CUBOID_IN_ALL_OUTER_COVER"
            if complete
            else (
                "DERIVE_NEW_LOCAL_FRONTIER_REPAIR"
                if state["unresolved"]
                else TARGET_CUBOID_ID
            )
        ),
    }

    validations = [
        check("all_sources_exist", not missing, len(source_paths())),
        check(
            "checkpoint_5473_v52_frontier_is_valid",
            int(result_5473.get("failed_validation_count", -1)) == 0
            and all(truth(row["passed"]) for row in validation_5473),
            result_5473.get("decision"),
        ),
        check(
            "checkpoint_5474_parent_v53_is_certified",
            truth(result_5474.get("valid_for_parent_v53_stable_edge_t_leaf_union"))
            and int(result_5474.get("failed_validation_count", -1)) == 0
            and all(truth(row["passed"]) for row in validation_5474),
            result_5474.get("decision"),
        ),
        check(
            "v52_source_state_is_hash_locked",
            state["v53_carry_forward"]["source_state_sha256"] == source_hash,
            source_hash,
        ),
        check(
            "active_cuboid_source_count_is_preserved",
            int(cuboid["source_leaf_count"]) == EXPECTED_SOURCE_LEAF_COUNT
            and int(state["source_leaf_count"]) == EXPECTED_SOURCE_LEAF_COUNT,
            state["source_leaf_count"],
        ),
        check(
            "accepted_pending_unresolved_partition_is_exact",
            partition_error <= partition_tolerance,
            partition_error,
        ),
        check(
            "every_accepted_subcuboid_has_positive_parent_factors",
            bool(state["accepted"])
            and all(
                all(
                    math.isfinite(float(row[field])) and float(row[field]) > 0.0
                    for field in (
                        "minimum_amplitude_denominator_abs_lower",
                        "relative_root_abs_lower",
                        "selected_global_root_abs_lower",
                        "collision_jacobian_abs_lower",
                    )
                )
                for row in state["accepted"]
            ),
            len(state["accepted"]),
        ),
        check(
            "v53_changes_only_enclosure_composition",
            not result_5474.get("parent_action_changed", True)
            and truth(result_5474.get("only_enclosure_composition_changed")),
            PARENT_V53_REVISION,
        ),
        check(
            "formalization_workbench_untouched",
            before_formalization == after_formalization,
            f"before={len(before_formalization)};after={len(after_formalization)}",
        ),
        check(
            "broad_claims_remain_false",
            not payload["valid_for_full_outer_parent_leaf_enclosure"]
            and not payload["valid_for_D4_event_local_W3_bound"]
            and not payload["valid_for_all_operator_local_GR_claim"]
            and not payload["valid_for_full_MTS_claim"],
            "one active outer cuboid only",
        ),
    ]
    payload["validation_row_count"] = len(validations)
    payload["failed_validation_count"] = sum(
        not row["passed"] for row in validations
    )
    source_rows = [
        {
            "source_path": str(path),
            "sha256": digest(path),
            "exists": path.is_file(),
        }
        for path in source_paths()
    ]
    base_5467.atomic_csv(SOURCE_REGISTER, source_rows)
    base_5467.atomic_csv(VALIDATION, validations)
    base_5467.atomic_json(STATUS, payload)
    base_5467.atomic_json(RESULT, payload)
    render_document(payload, base_5467)
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-node-evaluations", type=int, default=8)
    parser.add_argument("--max-runtime-seconds", type=float, default=600.0)
    parser.add_argument("--maximum-refinement-depth", type=int, default=33)
    parser.add_argument("--status-only", action="store_true")
    arguments = parser.parse_args()
    if arguments.max_node_evaluations <= 0:
        raise ValueError("--max-node-evaluations must be positive")
    payload = run(
        arguments.max_node_evaluations,
        arguments.max_runtime_seconds,
        arguments.maximum_refinement_depth,
        arguments.status_only,
    )
    print(
        json.dumps(
            {
                key: payload[key]
                for key in (
                    "decision",
                    "accepted_subcuboid_count",
                    "pending_subcuboid_count",
                    "unresolved_subcuboid_count",
                    "v53_node_evaluation_count",
                    "v53_accepted_subcuboid_count",
                    "v53_stable_edge_audit_row_count",
                    "processed_this_run",
                    "valid_for_parent_v53_active_cuboid",
                    "next_target",
                    "failed_validation_count",
                )
            },
            indent=2,
        )
    )
    return 0 if payload["failed_validation_count"] == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
