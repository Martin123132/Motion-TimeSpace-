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
OUTPUT = FUNCTIONAL_RG / "5477"
WORK = OUTPUT / "work-v1"

SCRIPT_5467 = SCRIPTS / "Y5_R2FR_5467_D4_all_outer_leaf_epsilon_fiber_transplant_runner.py"
SCRIPT_5468 = SCRIPTS / "Y5_R2FR_5468_D4_exact_outer_cuboid_coalescence_runner.py"
SCRIPT_5469 = SCRIPTS / "Y5_R2FR_5469_D4_resumable_three_axis_cuboid_certificate_runner.py"
SCRIPT_5472 = SCRIPTS / "Y5_R2FR_5472_D4_parent_v52_collision_jacobian_leaf_union_integration_gate.py"
SCRIPT_5474 = SCRIPTS / "Y5_R2FR_5474_D4_parent_v53_stable_edge_t_leaf_union_integration_gate.py"
SCRIPT_5475 = SCRIPTS / "Y5_R2FR_5475_D4_parent_v53_hash_locked_frontier_runner.py"
SCRIPT_5476 = SCRIPTS / "Y5_R2FR_5476_D4_parent_v54_first_spinor_pivot_t_leaf_union_integration_gate.py"
RESULT_5475 = FUNCTIONAL_RG / "5475" / "D4_parent_v53_hash_locked_frontier_result.json"
VALIDATION_5475 = FUNCTIONAL_RG / "5475" / "P8_Y5_BRR5474_5475_VALIDATION.csv"
RESULT_5476 = FUNCTIONAL_RG / "5476" / "D4_parent_v54_first_spinor_pivot_t_leaf_union_result.json"
VALIDATION_5476 = FUNCTIONAL_RG / "5476" / "P8_Y5_BRR5475_5476_VALIDATION.csv"
MANIFEST_5468 = FUNCTIONAL_RG / "5468" / "D4_exact_outer_cuboid_manifest.csv"

TARGET_CUBOID_ID = "E07__U051__RIGHT_CONNECTOR__CUBOID__6df3d70a73e4618b"
SOURCE_STATE_5475 = FUNCTIONAL_RG / "5475" / "work-v1" / f"{TARGET_CUBOID_ID}.json"
STATE = WORK / f"{TARGET_CUBOID_ID}.json"

PIVOT_AUDIT = OUTPUT / "D4_parent_v54_frontier_first_spinor_pivot_audit.csv"
STABLE_EDGE_AUDIT = OUTPUT / "D4_parent_v54_frontier_stable_edge_audit.csv"
JACOBIAN_AUDIT = OUTPUT / "D4_parent_v54_frontier_collision_jacobian_audit.csv"
CERTIFICATE = OUTPUT / "D4_parent_v54_active_cuboid_certificate.json"
SOURCE_REGISTER = OUTPUT / "source_register.csv"
VALIDATION = OUTPUT / "P8_Y5_BRR5476_5477_VALIDATION.csv"
STATUS = OUTPUT / "status.json"
RESULT = OUTPUT / "D4_parent_v54_hash_locked_frontier_result.json"
DOCUMENT = POST / "5477-Y5-R2FR-D4-parent-v54-hash-locked-frontier-runner.md"

CHECKPOINT = 5477
REVISION = "D4-parent-v54-hash-locked-frontier-runner-v1"
PARENT_V51_REVISION = "D4-deformed-contour-regular-away-W3-v51"
PARENT_V52_REVISION = "D4-deformed-contour-regular-away-W3-v52-leaf-union"
PARENT_V53_REVISION = "D4-deformed-contour-regular-away-W3-v53-stable-edge-t-leaf-union"
PARENT_V54_REVISION = "D4-deformed-contour-regular-away-W3-v54-first-spinor-pivot-t-leaf-union"
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
        SCRIPT_5474,
        SCRIPT_5475,
        SCRIPT_5476,
        RESULT_5475,
        VALIDATION_5475,
        RESULT_5476,
        VALIDATION_5476,
        MANIFEST_5468,
        SOURCE_STATE_5475,
    )


def carry_forward_state(base_5467: Any) -> dict[str, Any]:
    source = read_json(SOURCE_STATE_5475)
    if source["cuboid_job_id"] != TARGET_CUBOID_ID:
        raise RuntimeError("checkpoint 5475 source state has the wrong cuboid id")
    if source["unresolved"]:
        raise RuntimeError("checkpoint 5475 source state is not cleanly resumable")
    source_revision = source.get("revision", "")
    source["checkpoint"] = CHECKPOINT
    source["revision"] = REVISION
    source["parent_revision"] = PARENT_V54_REVISION
    source["parent_revision_history"] = [
        PARENT_V51_REVISION,
        PARENT_V52_REVISION,
        PARENT_V53_REVISION,
        PARENT_V54_REVISION,
    ]
    source["v54_carry_forward"] = {
        "source_checkpoint": 5475,
        "source_state_path": str(SOURCE_STATE_5475),
        "source_state_sha256": digest(SOURCE_STATE_5475),
        "source_revision": source_revision,
        "carried_accepted_subcuboid_count": len(source["accepted"]),
        "carried_pending_subcuboid_count": len(source["stack"]),
        "carried_unresolved_subcuboid_count": len(source["unresolved"]),
        "carried_utc": datetime.now(timezone.utc).isoformat(),
        "carry_rule": (
            "v54 returns the unchanged v53 evaluation unless the precise "
            "left-first projective-pivot singularity triggers"
        ),
    }
    source["v54_node_evaluation_count"] = 0
    source["v54_accepted_subcuboid_count"] = 0
    source["v54_refinement_witness_count"] = 0
    source["v54_first_spinor_pivot_audit_rows"] = []
    source["v54_stable_edge_audit_rows"] = []
    source["v54_collision_jacobian_audit_rows"] = []
    source["decision"] = "PARENT_V54_FRONTIER_PARTIAL__RESUME"
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
        "# 5477: D4 parent-v54 hash-locked frontier runner",
        "",
        "The checkpoint-5475 state is preserved byte-for-byte. This checkpoint carries its exact accepted/pending partition into parent v54; prior passing boxes remain unchanged, while only the certified first-spinor pivot exception may invoke the new exact t-leaf union.",
        "",
        f"Accepted: `{payload['accepted_subcuboid_count']}`. Pending: `{payload['pending_subcuboid_count']}`. Unresolved: `{payload['unresolved_subcuboid_count']}`.",
        "",
        f"V54 evaluations: `{payload['v54_node_evaluation_count']}`. V54 accepted: `{payload['v54_accepted_subcuboid_count']}`. Pivot audit rows: `{payload['v54_pivot_audit_row_count']}`.",
        "",
        f"**{payload['decision']}**",
        "",
        "Only this active cuboid can be certified here; every broader claim remains false.",
        "",
    ]
    base_5467.atomic_text(DOCUMENT, "\n".join(lines))


def run(
    maximum_node_evaluations: int,
    maximum_runtime_seconds: float,
    maximum_refinement_depth: int,
    status_only: bool,
) -> dict[str, Any]:
    base_5467 = load_module("mts_5467_for_5477", SCRIPT_5467)
    base_5468 = load_module("mts_5468_for_5477", SCRIPT_5468)
    base_5469 = load_module("mts_5469_for_5477", SCRIPT_5469)
    base_5472 = load_module("mts_5472_for_5477", SCRIPT_5472)
    base_5474 = load_module("mts_5474_for_5477", SCRIPT_5474)
    base_5476 = load_module("mts_5476_for_5477", SCRIPT_5476)
    base_5467.set_below_normal_priority()
    before_formalization = base_5467.formalization_snapshot()
    missing = [str(path) for path in source_paths() if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"missing sources: {missing}")

    result_5475 = read_json(RESULT_5475)
    validation_5475 = read_csv(VALIDATION_5475)
    result_5476 = read_json(RESULT_5476)
    validation_5476 = read_csv(VALIDATION_5476)
    cuboid = next(
        row
        for row in read_csv(MANIFEST_5468)
        if row["cuboid_job_id"] == TARGET_CUBOID_ID
    )
    WORK.mkdir(parents=True, exist_ok=True)
    state = read_json(STATE) if STATE.is_file() else carry_forward_state(base_5467)
    source_hash = digest(SOURCE_STATE_5475)
    if state["v54_carry_forward"]["source_state_sha256"] != source_hash:
        raise RuntimeError("checkpoint 5475 source state changed after v54 carry-forward")

    accepted_before = len(state["accepted"])
    witnesses_before = len(state["refinement_witnesses"])
    nodes_before = int(state["node_evaluation_count"])
    if state["stack"] and not state["unresolved"] and not status_only:
        stable, _, cells, support_segments, branches = base_5467.load_parent()
        parent_v54 = base_5476.install_parent_v54(
            base_5474.install_parent_v53(
                base_5472.install_parent_v52(
                    base_5472.fresh_parent(base_5467, "mts_parent_v54_for_5477")
                )
            ),
            base_5474,
        )
        state = base_5469.process_state(
            base_5467,
            base_5468,
            stable,
            parent_v54,
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
        for row in state["accepted"][accepted_before:]:
            row["certificate_source"] = "checkpoint_5477_parent_v54"
            row["parent_revision"] = PARENT_V54_REVISION
        for row in state["refinement_witnesses"][witnesses_before:]:
            row["certificate_source"] = "checkpoint_5477_parent_v54_witness"
            row["parent_revision"] = PARENT_V54_REVISION
        state["v54_node_evaluation_count"] = int(
            state.get("v54_node_evaluation_count", 0)
        ) + int(state["node_evaluation_count"]) - nodes_before
        state["v54_accepted_subcuboid_count"] = int(
            state.get("v54_accepted_subcuboid_count", 0)
        ) + len(state["accepted"]) - accepted_before
        state["v54_refinement_witness_count"] = int(
            state.get("v54_refinement_witness_count", 0)
        ) + len(state["refinement_witnesses"]) - witnesses_before
        state.setdefault("v54_first_spinor_pivot_audit_rows", []).extend(
            parent_v54.V54_FIRST_SPINOR_PIVOT_T_LEAF_UNION_AUDIT_ROWS
        )
        state.setdefault("v54_stable_edge_audit_rows", []).extend(
            parent_v54.V53_STABLE_EDGE_T_LEAF_UNION_AUDIT_ROWS
        )
        state.setdefault("v54_collision_jacobian_audit_rows", []).extend(
            parent_v54.V52_COLLISION_JACOBIAN_LEAF_UNION_AUDIT_ROWS
        )
        base_5467.atomic_json(STATE, state, compact=True)

    for path, key in (
        (PIVOT_AUDIT, "v54_first_spinor_pivot_audit_rows"),
        (STABLE_EDGE_AUDIT, "v54_stable_edge_audit_rows"),
        (JACOBIAN_AUDIT, "v54_collision_jacobian_audit_rows"),
    ):
        if state.get(key):
            base_5467.atomic_csv(path, state[key])

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
        "PARENT_V54_ACTIVE_CUBOID_CERTIFIED"
        if complete
        else (
            "PARENT_V54_FRONTIER_REACHES_UNRESOLVED__DERIVE_LOCAL_REPAIR"
            if state["unresolved"]
            else "PARENT_V54_FRONTIER_PARTIAL__RESUME"
        )
    )
    state["valid_for_parent_v54_active_cuboid"] = complete
    state["valid_for_full_outer_parent_leaf_enclosure"] = False
    state["valid_for_D4_event_local_W3_bound"] = False
    state["valid_for_all_operator_local_GR_claim"] = False
    state["valid_for_full_MTS_claim"] = False
    base_5467.atomic_json(STATE, state, compact=True)

    if complete:
        certificate = {
            "checkpoint": CHECKPOINT,
            "revision": REVISION,
            "parent_revision": PARENT_V54_REVISION,
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
            "certificate_source": "checkpoint_5477_v51_v52_v53_carry_plus_v54_frontier",
            "valid_for_parent_v54_active_cuboid": True,
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
        "parent_revision": PARENT_V54_REVISION,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "decision": state["decision"],
        "target_cuboid_id": TARGET_CUBOID_ID,
        "source_fiber_count": int(cuboid["source_fiber_count"]),
        "source_leaf_count": int(cuboid["source_leaf_count"]),
        "accepted_subcuboid_count": len(state["accepted"]),
        "pending_subcuboid_count": len(state["stack"]),
        "unresolved_subcuboid_count": len(state["unresolved"]),
        "node_evaluation_count": int(state["node_evaluation_count"]),
        "v54_node_evaluation_count": int(state["v54_node_evaluation_count"]),
        "v54_accepted_subcuboid_count": int(
            state["v54_accepted_subcuboid_count"]
        ),
        "v54_refinement_witness_count": int(
            state["v54_refinement_witness_count"]
        ),
        "v54_pivot_audit_row_count": len(
            state.get("v54_first_spinor_pivot_audit_rows", [])
        ),
        "v54_stable_edge_audit_row_count": len(
            state.get("v54_stable_edge_audit_rows", [])
        ),
        "v54_collision_jacobian_audit_row_count": len(
            state.get("v54_collision_jacobian_audit_rows", [])
        ),
        "processed_this_run": (
            0 if status_only else int(state.get("processed_this_run", 0))
        ),
        "partition_volume_error": partition_error,
        "source_state_5475_sha256": source_hash,
        "valid_for_parent_v54_active_cuboid": complete,
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
            "checkpoint_5475_v53_frontier_is_valid",
            int(result_5475.get("failed_validation_count", -1)) == 0
            and all(truth(row["passed"]) for row in validation_5475),
            result_5475.get("decision"),
        ),
        check(
            "checkpoint_5476_parent_v54_is_certified",
            truth(
                result_5476.get(
                    "valid_for_parent_v54_first_spinor_pivot_t_leaf_union"
                )
            )
            and int(result_5476.get("failed_validation_count", -1)) == 0
            and all(truth(row["passed"]) for row in validation_5476),
            result_5476.get("decision"),
        ),
        check(
            "v53_source_state_is_hash_locked",
            state["v54_carry_forward"]["source_state_sha256"] == source_hash,
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
            "v54_changes_only_enclosure_composition",
            not result_5476.get("parent_action_changed", True)
            and truth(result_5476.get("only_enclosure_composition_changed")),
            PARENT_V54_REVISION,
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
                    "v54_node_evaluation_count",
                    "v54_accepted_subcuboid_count",
                    "v54_pivot_audit_row_count",
                    "processed_this_run",
                    "valid_for_parent_v54_active_cuboid",
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
