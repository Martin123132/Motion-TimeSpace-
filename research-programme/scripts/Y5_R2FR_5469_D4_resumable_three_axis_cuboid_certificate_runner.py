from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import math
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


POST = Path(__file__).resolve().parents[1]
SCRIPTS = POST / "scripts"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
FORMALIZATION = POST.parent / "formalization-workbench"
OUTPUT = FUNCTIONAL_RG / "5469"
WORK = OUTPUT / "work-v1"
REPAIR_5471 = FUNCTIONAL_RG / "5471" / "D4_unresolved_subcuboid_repair_certificate.json"
RESULT_5471 = FUNCTIONAL_RG / "5471" / "D4_collision_leaf_union_full_amplitude_result.json"
VALIDATION_5471 = FUNCTIONAL_RG / "5471" / "P8_Y5_BRR5470_5471_VALIDATION.csv"
WORK_5471 = FUNCTIONAL_RG / "5471" / "work-v1"

SCRIPT_5468 = SCRIPTS / "Y5_R2FR_5468_D4_exact_outer_cuboid_coalescence_runner.py"
MANIFEST_5468 = FUNCTIONAL_RG / "5468" / "D4_exact_outer_cuboid_manifest.csv"
MEMBERSHIP_5468 = FUNCTIONAL_RG / "5468" / "D4_exact_outer_cuboid_membership.csv"
RESULT_5468 = FUNCTIONAL_RG / "5468" / "D4_exact_outer_cuboid_coalescence_result.json"
VALIDATION_5468 = FUNCTIONAL_RG / "5468" / "P8_Y5_BRR5467_5468_VALIDATION.csv"
CERTIFICATES_5468 = FUNCTIONAL_RG / "5468" / "D4_exact_outer_cuboid_certificates.csv"
MANIFEST_5467 = FUNCTIONAL_RG / "5467" / "D4_outer_leaf_epsilon_fiber_manifest.csv"

CERTIFICATES = OUTPUT / "D4_resumable_three_axis_cuboid_certificates.csv"
PROGRESS = OUTPUT / "D4_resumable_three_axis_cuboid_progress.csv"
SOURCE_REGISTER = OUTPUT / "source_register.csv"
VALIDATION = OUTPUT / "P8_Y5_BRR5468_5469_VALIDATION.csv"
STATUS = OUTPUT / "status.json"
RESULT = OUTPUT / "D4_resumable_three_axis_cuboid_result.json"
DOCUMENT = POST / "5469-Y5-R2FR-D4-resumable-three-axis-cuboid-certificate-runner.md"

CHECKPOINT = 5469
REVISION = "D4-resumable-three-axis-cuboid-certificate-runner-v4"
PARENT_REVISION = "D4-deformed-contour-regular-away-W3-v51"
EXPECTED_CUBOID_COUNT = 21_065
EXPECTED_FIBER_COUNT = 99_522
EXPECTED_SOURCE_LEAF_COUNT = 606_990
MAXIMUM_REFINEMENT_DEPTH = 24
MINIMUM_WIDTHS = {"epsilon": 1.0e-12, "x": 1.0e-12, "t": 1.0e-10}
AXIS_FIELDS = {
    "epsilon": ("epsilon_real_lower", "epsilon_real_upper"),
    "x": ("x_lower", "x_upper"),
    "t": ("t_lower", "t_upper"),
}


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
        SCRIPT_5468,
        MANIFEST_5468,
        MEMBERSHIP_5468,
        RESULT_5468,
        VALIDATION_5468,
        CERTIFICATES_5468,
        MANIFEST_5467,
        REPAIR_5471,
        RESULT_5471,
        VALIDATION_5471,
    )


def node_volume(node: dict[str, Any]) -> float:
    return math.prod(
        float(node[upper]) - float(node[lower])
        for lower, upper in AXIS_FIELDS.values()
    )


def root_node(row: dict[str, Any]) -> dict[str, Any]:
    return {
        "epsilon_real_lower": float(row["epsilon_real_lower"]),
        "epsilon_real_upper": float(row["epsilon_real_upper"]),
        "x_lower": float(row["x_lower"]),
        "x_upper": float(row["x_upper"]),
        "t_lower": float(row["t_lower"]),
        "t_upper": float(row["t_upper"]),
        "refinement_depth": 0,
        "refinement_path": "R",
    }


def member_profile(
    cuboid_id: str,
    memberships_by_cuboid: dict[str, list[str]],
    fibers_by_id: dict[str, dict[str, str]],
) -> dict[str, Any]:
    member_ids = memberships_by_cuboid[cuboid_id]
    members = [fibers_by_id[member_id] for member_id in member_ids]
    boundaries: dict[str, list[float]] = {}
    maximum_source_widths: dict[str, float] = {}
    for axis, (lower_field, upper_field) in AXIS_FIELDS.items():
        boundaries[axis] = sorted(
            {
                float(row[field])
                for row in members
                for field in (lower_field, upper_field)
            }
        )
        maximum_source_widths[axis] = max(
            float(row[upper_field]) - float(row[lower_field]) for row in members
        )
    return {
        "source_fiber_ids": member_ids,
        "source_boundaries": boundaries,
        "maximum_source_widths": maximum_source_widths,
    }


def initial_state(row: dict[str, Any], profile: dict[str, Any]) -> dict[str, Any]:
    root = root_node(row)
    return {
        "checkpoint": CHECKPOINT,
        "revision": REVISION,
        "parent_revision": PARENT_REVISION,
        "cuboid_job_id": row["cuboid_job_id"],
        "source_fiber_membership_sha256": row[
            "source_fiber_membership_sha256"
        ],
        "source_fiber_count": int(row["source_fiber_count"]),
        "source_leaf_count": int(row["source_leaf_count"]),
        "root": root,
        "root_volume": node_volume(root),
        "maximum_source_widths": profile["maximum_source_widths"],
        "source_boundaries": profile["source_boundaries"],
        "stack": [root],
        "accepted": [],
        "refinement_witnesses": [],
        "unresolved": [],
        "node_evaluation_count": 0,
        "split_axis_counts": {"epsilon": 0, "x": 0, "t": 0},
        "runtime_seconds": 0.0,
        "maximum_refinement_depth_allowed": MAXIMUM_REFINEMENT_DEPTH,
        "depth_extension_history": [],
        "last_update_utc": datetime.now(timezone.utc).isoformat(),
        "decision": "THREE_AXIS_CUBOID_PARTIAL__RESUME",
        "valid_for_resumable_three_axis_cuboid_certificate": False,
        "valid_for_full_outer_parent_leaf_enclosure": False,
        "valid_for_D4_event_local_W3_bound": False,
        "valid_for_all_operator_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }


def compact_node_result(
    node: dict[str, Any], result: dict[str, Any]
) -> dict[str, Any]:
    fields = (
        "probe_passed",
        "failure_type",
        "failure_message",
        "integrated_regular_path_abs_upper",
        "minimum_amplitude_denominator_abs_lower",
        "relative_root_abs_lower",
        "selected_global_root_abs_lower",
        "collision_jacobian_abs_lower",
        "active_material_branch_count",
        "active_material_branch_ids",
        "path_integral_enclosure_method",
        "runtime_seconds",
    )
    return {
        **node,
        **{field: result.get(field) for field in fields},
    }


def evaluate_node(
    base_5468: Any,
    stable: Any,
    parent: Any,
    cells: dict[str, Any],
    support_segments: list[dict[str, Any]],
    branches: dict[str, Any],
    row: dict[str, Any],
    node: dict[str, Any],
) -> dict[str, Any]:
    path_speed_bound = base_5468.full_cell_path_speed_bound(
        parent,
        cells[row["mapped_cell_id"]],
        row["path_segment"],
    )
    parameter_area = (
        float(node["x_upper"]) - float(node["x_lower"])
    ) * (float(node["t_upper"]) - float(node["t_lower"]))
    probe = {
        "smoke_job_id": row["cuboid_job_id"],
        "selection_role": "RESUMABLE_EXACT_THREE_AXIS_SUBCUBOID",
        "event_id": row["event_id"],
        "mapped_cell_id": row["mapped_cell_id"],
        "term_id": row["term_id"],
        "branch_owner_id": row["branch_owner_id"],
        "epsilon_bin_index": int(row["source_epsilon_bin_index_lower"]),
        "epsilon_subdivision_index": 0,
        "epsilon_subdivision_count": 1,
        "epsilon_real_lower": float(node["epsilon_real_lower"]),
        "epsilon_real_upper": float(node["epsilon_real_upper"]),
        "epsilon_imaginary_lower": float(row["epsilon_imaginary_lower"]),
        "epsilon_imaginary_upper": float(row["epsilon_imaginary_upper"]),
        "path_segment": row["path_segment"],
        "x_lower": float(node["x_lower"]),
        "x_upper": float(node["x_upper"]),
        "t_lower": float(node["t_lower"]),
        "t_upper": float(node["t_upper"]),
        "refinement_depth": int(node["refinement_depth"]),
        "refinement_path": node["refinement_path"],
        "gap_abs_lower": float(row["source_partition_minimum_gap_abs_lower"]),
        "physical_path_area_abs_upper": parameter_area * path_speed_bound,
    }
    return stable.evaluate_representative(
        parent,
        cells,
        support_segments,
        branches,
        probe,
    )


def split_choice(
    node: dict[str, Any], state: dict[str, Any]
) -> tuple[str, float, bool] | None:
    widths = {
        axis: float(node[upper]) - float(node[lower])
        for axis, (lower, upper) in AXIS_FIELDS.items()
    }
    candidates = [
        axis for axis in AXIS_FIELDS if widths[axis] > MINIMUM_WIDTHS[axis]
    ]
    if not candidates:
        return None
    ratios = {
        axis: widths[axis]
        / max(float(state["maximum_source_widths"][axis]), MINIMUM_WIDTHS[axis])
        for axis in candidates
    }
    if "epsilon" in candidates and ratios["epsilon"] > 1.0 + 1.0e-12:
        axis = "epsilon"
    else:
        axis = max(
            candidates,
            key=lambda candidate: (
                ratios[candidate],
                {"epsilon": 2, "x": 1, "t": 0}[candidate],
            ),
        )
    lower_field, upper_field = AXIS_FIELDS[axis]
    lower = float(node[lower_field])
    upper = float(node[upper_field])
    midpoint = 0.5 * (lower + upper)
    interior = [
        float(boundary)
        for boundary in state["source_boundaries"][axis]
        if lower < float(boundary) < upper
    ]
    if interior:
        split = min(interior, key=lambda boundary: abs(boundary - midpoint))
        return axis, split, True
    return axis, midpoint, False


def split_node(
    node: dict[str, Any], axis: str, split: float, source_boundary: bool
) -> tuple[dict[str, Any], dict[str, Any]]:
    lower_field, upper_field = AXIS_FIELDS[axis]
    lower_child = dict(node)
    upper_child = dict(node)
    lower_child[upper_field] = split
    upper_child[lower_field] = split
    depth = int(node["refinement_depth"]) + 1
    marker = {"epsilon": "E", "x": "X", "t": "T"}[axis]
    suffix = "S" if source_boundary else "M"
    lower_child["refinement_depth"] = depth
    upper_child["refinement_depth"] = depth
    lower_child["refinement_path"] = (
        f"{node['refinement_path']}_{marker}0{suffix}"
    )
    upper_child["refinement_path"] = (
        f"{node['refinement_path']}_{marker}1{suffix}"
    )
    return lower_child, upper_child


def update_state_decision(state: dict[str, Any]) -> None:
    accepted_volume = sum(node_volume(row) for row in state["accepted"])
    coverage_error = abs(accepted_volume - float(state["root_volume"]))
    coverage_tolerance = 1.0e-12 * max(float(state["root_volume"]), 1.0)
    complete = (
        bool(state["accepted"])
        and not state["stack"]
        and not state["unresolved"]
        and coverage_error <= coverage_tolerance
    )
    state["accepted_volume"] = accepted_volume
    state["coverage_error"] = coverage_error
    state["accepted_subcuboid_count"] = len(state["accepted"])
    state["pending_subcuboid_count"] = len(state["stack"])
    state["unresolved_subcuboid_count"] = len(state["unresolved"])
    state["decision"] = (
        "THREE_AXIS_CUBOID_CERTIFIED"
        if complete
        else (
            "THREE_AXIS_CUBOID_REACHES_DEPTH_LIMIT__SPLIT_SOURCE_MEMBERSHIP"
            if state["unresolved"]
            else "THREE_AXIS_CUBOID_PARTIAL__RESUME"
        )
    )
    state["valid_for_resumable_three_axis_cuboid_certificate"] = complete
    state["valid_for_full_outer_parent_leaf_enclosure"] = False
    state["valid_for_D4_event_local_W3_bound"] = False
    state["valid_for_all_operator_local_GR_claim"] = False
    state["valid_for_full_MTS_claim"] = False
    state["last_update_utc"] = datetime.now(timezone.utc).isoformat()


def process_state(
    base_5467: Any,
    base_5468: Any,
    stable: Any,
    parent: Any,
    cells: dict[str, Any],
    support_segments: list[dict[str, Any]],
    branches: dict[str, Any],
    row: dict[str, Any],
    state: dict[str, Any],
    state_path: Path,
    maximum_node_evaluations: int,
    maximum_runtime_seconds: float,
    maximum_refinement_depth: int,
) -> dict[str, Any]:
    started = time.perf_counter()
    processed = 0
    base_5467.atomic_json(state_path, state, compact=True)
    while state["stack"] and not state["unresolved"]:
        if processed >= maximum_node_evaluations:
            break
        if time.perf_counter() - started >= maximum_runtime_seconds:
            break
        node = state["stack"][-1]
        result = evaluate_node(
            base_5468,
            stable,
            parent,
            cells,
            support_segments,
            branches,
            row,
            node,
        )
        state["stack"].pop()
        compact = compact_node_result(node, result)
        state["node_evaluation_count"] = int(state["node_evaluation_count"]) + 1
        processed += 1
        if truth(result.get("probe_passed")):
            state["accepted"].append(compact)
        else:
            state["refinement_witnesses"].append(compact)
            if int(node["refinement_depth"]) >= maximum_refinement_depth:
                state["unresolved"].append(compact)
            else:
                choice = split_choice(node, state)
                if choice is None:
                    state["unresolved"].append(compact)
                else:
                    axis, split, source_boundary = choice
                    lower_child, upper_child = split_node(
                        node, axis, split, source_boundary
                    )
                    state["stack"].append(upper_child)
                    state["stack"].append(lower_child)
                    state["split_axis_counts"][axis] = int(
                        state["split_axis_counts"][axis]
                    ) + 1
        state["runtime_seconds"] = float(state["runtime_seconds"]) + (
            time.perf_counter() - started
            - float(state.get("runtime_accounted_this_run", 0.0))
        )
        state["runtime_accounted_this_run"] = time.perf_counter() - started
        update_state_decision(state)
        base_5467.atomic_json(state_path, state, compact=True)
    state.pop("runtime_accounted_this_run", None)
    state["processed_this_run"] = processed
    update_state_decision(state)
    base_5467.atomic_json(state_path, state, compact=True)
    return state


def reopen_depth_limit(
    state: dict[str, Any],
    maximum_refinement_depth: int,
    extension_axis: str | None,
) -> None:
    previous_limit = int(
        state.get("maximum_refinement_depth_allowed", MAXIMUM_REFINEMENT_DEPTH)
    )
    if not state["unresolved"] or maximum_refinement_depth <= previous_limit:
        return
    retained: list[dict[str, Any]] = []
    reopened_count = 0
    for witness in state["unresolved"]:
        node = {
            field: witness[field]
            for field in (
                "epsilon_real_lower",
                "epsilon_real_upper",
                "x_lower",
                "x_upper",
                "t_lower",
                "t_upper",
                "refinement_depth",
                "refinement_path",
            )
        }
        if extension_axis is None:
            choice = split_choice(node, state)
            split_rule = "SOURCE_WIDTH_RATIO"
        else:
            lower_field, upper_field = AXIS_FIELDS[extension_axis]
            lower = float(node[lower_field])
            upper = float(node[upper_field])
            if upper - lower <= MINIMUM_WIDTHS[extension_axis]:
                choice = None
            else:
                midpoint = 0.5 * (lower + upper)
                interior = [
                    float(boundary)
                    for boundary in state["source_boundaries"][extension_axis]
                    if lower < float(boundary) < upper
                ]
                if interior:
                    split = min(
                        interior, key=lambda boundary: abs(boundary - midpoint)
                    )
                    choice = (extension_axis, split, True)
                else:
                    choice = (extension_axis, midpoint, False)
            split_rule = f"EXPLICIT_{extension_axis.upper()}_ABLATION"
        if choice is None or int(node["refinement_depth"]) >= maximum_refinement_depth:
            retained.append(witness)
            continue
        axis, split, source_boundary = choice
        lower_child, upper_child = split_node(node, axis, split, source_boundary)
        state["stack"].append(upper_child)
        state["stack"].append(lower_child)
        state["split_axis_counts"][axis] = int(
            state["split_axis_counts"][axis]
        ) + 1
        state["depth_extension_history"].append(
            {
                "previous_limit": previous_limit,
                "new_limit": maximum_refinement_depth,
                "reopened_refinement_path": node["refinement_path"],
                "derived_split_axis": axis,
                "split_value": split,
                "source_boundary": source_boundary,
                "split_rule": split_rule,
                "recorded_utc": datetime.now(timezone.utc).isoformat(),
            }
        )
        reopened_count += 1
    state["unresolved"] = retained
    state["maximum_refinement_depth_allowed"] = maximum_refinement_depth
    state["last_depth_extension_reopened_count"] = reopened_count
    update_state_decision(state)


def integrate_5471_repair(state: dict[str, Any]) -> None:
    history = state.setdefault("external_repair_history", [])
    if any(int(row.get("checkpoint", -1)) == 5471 for row in history):
        return
    repair = read_json(REPAIR_5471)
    result = read_json(RESULT_5471)
    validation = read_csv(VALIDATION_5471)
    if not (
        truth(repair.get("valid_for_unresolved_subcuboid_repair"))
        and truth(result.get("valid_for_unresolved_subcuboid_repair"))
        and int(result.get("passed_leaf_count", -1)) == 128
        and int(result.get("failed_leaf_count", -1)) == 0
        and int(result.get("failed_validation_count", -1)) == 0
        and all(truth(row["passed"]) for row in validation)
    ):
        raise RuntimeError("checkpoint 5471 repair is not fully certified")
    target_path = repair["repaired_refinement_path"]
    matching = [
        row for row in state["unresolved"] if row["refinement_path"] == target_path
    ]
    if len(matching) != 1:
        raise RuntimeError("checkpoint 5471 repair target is not uniquely unresolved")
    leaf_ids = repair["replacement_leaf_ids"]
    leaves = [read_json(WORK_5471 / f"{leaf_id}.json") for leaf_id in leaf_ids]
    if len(leaves) != 128 or not all(
        truth(row.get("valid_for_full_amplitude_leaf")) for row in leaves
    ):
        raise RuntimeError("checkpoint 5471 amplitude leaf set is incomplete")
    state["unresolved"] = [
        row for row in state["unresolved"] if row["refinement_path"] != target_path
    ]
    state["accepted"].extend(leaves)
    state["node_evaluation_count"] = int(state["node_evaluation_count"]) + len(
        leaves
    )
    state["split_axis_counts"]["t"] = int(
        state["split_axis_counts"]["t"]
    ) + len(leaves) - 1
    state["runtime_seconds"] = float(state["runtime_seconds"]) + sum(
        float(row["runtime_seconds"]) for row in leaves
    )
    state["maximum_refinement_depth_allowed"] = max(
        int(state.get("maximum_refinement_depth_allowed", 0)),
        max(int(row["refinement_depth"]) for row in leaves),
    )
    history.append(
        {
            "checkpoint": 5471,
            "repaired_refinement_path": target_path,
            "replacement_leaf_count": len(leaves),
            "minimum_amplitude_denominator_abs_lower": repair[
                "minimum_amplitude_denominator_abs_lower"
            ],
            "minimum_collision_jacobian_abs_lower": repair[
                "minimum_collision_jacobian_abs_lower"
            ],
            "coverage_error": repair["coverage_error"],
            "integrated_utc": datetime.now(timezone.utc).isoformat(),
        }
    )
    update_state_decision(state)


def state_certificate(
    row: dict[str, Any], state: dict[str, Any]
) -> dict[str, Any]:
    accepted = state["accepted"]
    return {
        "cuboid_job_id": row["cuboid_job_id"],
        "event_id": row["event_id"],
        "mapped_cell_id": row["mapped_cell_id"],
        "term_id": row["term_id"],
        "path_segment": row["path_segment"],
        "source_fiber_count": int(row["source_fiber_count"]),
        "source_leaf_count": int(row["source_leaf_count"]),
        "source_fiber_membership_sha256": row[
            "source_fiber_membership_sha256"
        ],
        "accepted_subcuboid_count": len(accepted),
        "refinement_witness_count": len(state["refinement_witnesses"]),
        "maximum_refinement_depth": max(
            int(item["refinement_depth"]) for item in accepted
        ),
        "node_evaluation_count": int(state["node_evaluation_count"]),
        "split_axis_counts": json.dumps(
            state["split_axis_counts"], sort_keys=True, separators=(",", ":")
        ),
        "integrated_regular_path_abs_upper": sum(
            float(item["integrated_regular_path_abs_upper"]) for item in accepted
        ),
        "integrated_bound_aggregation": "CONSERVATIVE_SUM_OVER_EXACT_3D_SUBCOVER",
        "minimum_amplitude_denominator_abs_lower": min(
            float(item["minimum_amplitude_denominator_abs_lower"])
            for item in accepted
        ),
        "relative_root_abs_lower": min(
            float(item["relative_root_abs_lower"]) for item in accepted
        ),
        "selected_global_root_abs_lower": min(
            float(item["selected_global_root_abs_lower"]) for item in accepted
        ),
        "collision_jacobian_abs_lower": min(
            float(item["collision_jacobian_abs_lower"]) for item in accepted
        ),
        "coverage_error": float(state["coverage_error"]),
        "runtime_seconds": float(state["runtime_seconds"]),
        "certificate_source": "checkpoint_5469_resumable_exact_three_axis_subcover",
        "parent_revision": PARENT_REVISION,
        "valid_for_exact_outer_cuboid_transplant": True,
        "valid_for_resumable_three_axis_cuboid_certificate": True,
        "valid_for_full_outer_parent_leaf_enclosure": False,
        "valid_for_D4_event_local_W3_bound": False,
        "valid_for_all_operator_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }


def check(gate: str, passed: bool, evidence: Any) -> dict[str, Any]:
    return {
        "checkpoint": CHECKPOINT,
        "validation_gate": gate,
        "passed": bool(passed),
        "evidence": evidence,
    }


def render_document(payload: dict[str, Any], base_5467: Any) -> None:
    lines = [
        "# 5469: D4 resumable three-axis cuboid certificate runner",
        "",
        "## Derived repair",
        "",
        "Checkpoint 5468 proved a lossless 21,065-cuboid cover, but its largest all-at-once hull spent thirty minutes in x/t-only adaptive refinement without committing a witness. That interruption is non-evidential. This runner evaluates one exact subcuboid at a time, splits epsilon first whenever coalescence made it broader than its source-fiber scale, then selects x or t from source-width ratios. Every completed node is written atomically before the next node starts. A depth limit can be extended only explicitly; the recorded terminal witness is retained and split once by the same source-ratio rule without being reevaluated or erased.",
        "",
        "Every split is an exact interval identity. Source boundaries nearest the midpoint are preferred; a numerical midpoint is used only when no interior source boundary exists. An interrupted run retains its unchanged pending node and all prior accepted certificates.",
        "",
        "## Current state",
        "",
        f"Certified cuboids: `{payload['certified_cuboid_count']}/{payload['cuboid_manifest_count']}`, covering `{payload['certified_source_leaf_count']}/{payload['source_leaf_count']}` source leaves. Partial resumable cuboids: `{payload['partial_cuboid_count']}`. Depth-limit cuboids: `{payload['failed_cuboid_count']}`.",
        "",
        f"Accepted three-axis subcuboids: `{payload['accepted_subcuboid_count']}`. Pending subcuboids: `{payload['pending_subcuboid_count']}`. Total node evaluations: `{payload['node_evaluation_count']}`.",
        "",
        "## Decision",
        "",
        f"**{payload['decision']}**",
        "",
        "## Claim boundary",
        "",
        "Partial states and interrupted hulls are not failures. Full outer enclosure requires every cuboid to be certified or losslessly split to certified descendants. Event-local W3, the regulator limit, local GR and full MTS remain unclaimed.",
        "",
    ]
    base_5467.atomic_text(DOCUMENT, "\n".join(lines))


def run(
    requested_job_id: str | None,
    choose_next: bool,
    maximum_node_evaluations: int,
    maximum_runtime_seconds: float,
    maximum_refinement_depth: int,
    reopen_terminal_depth: bool,
    depth_extension_axis: str | None,
    integrate_repair_5471: bool,
    status_only: bool,
    list_next: int,
) -> dict[str, Any]:
    base_5468 = load_module("mts_5468_for_5469", SCRIPT_5468)
    base_5467 = base_5468.load_module("mts_5467_for_5469", base_5468.SCRIPT_5467)
    base_5467.set_below_normal_priority()
    before_formalization = base_5467.formalization_snapshot()
    missing = [str(path) for path in source_paths() if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"missing sources: {missing}")
    result_5468 = read_json(RESULT_5468)
    validation_5468 = read_csv(VALIDATION_5468)
    manifest = read_csv(MANIFEST_5468)
    manifest_by_id = {row["cuboid_job_id"]: row for row in manifest}
    membership = read_csv(MEMBERSHIP_5468)
    memberships_by_cuboid: dict[str, list[str]] = {}
    for item in membership:
        memberships_by_cuboid.setdefault(item["cuboid_job_id"], []).append(
            item["source_fiber_job_id"]
        )
    fibers_by_id = {
        row["fiber_job_id"]: row for row in read_csv(MANIFEST_5467)
    }
    WORK.mkdir(parents=True, exist_ok=True)
    states: dict[str, dict[str, Any]] = {
        path.stem: read_json(path) for path in WORK.glob("*.json") if path.is_file()
    }
    carried = {
        row["cuboid_job_id"]: row for row in read_csv(CERTIFICATES_5468)
    }
    partial_ids = [
        cuboid_id
        for cuboid_id, state in states.items()
        if state["stack"] and not state["unresolved"]
    ]
    pending_rows = [
        row
        for row in manifest
        if row["cuboid_job_id"] not in carried
        and row["cuboid_job_id"] not in states
    ]
    next_rows = [manifest_by_id[cuboid_id] for cuboid_id in partial_ids] + pending_rows
    next_rows.sort(
        key=lambda row: (
            0 if row["cuboid_job_id"] in partial_ids else 1,
            int(row["evaluation_priority"]),
        )
    )
    if list_next > 0:
        print(
            json.dumps(
                [
                    {
                        "cuboid_job_id": row["cuboid_job_id"],
                        "source_leaf_count": int(row["source_leaf_count"]),
                        "state": (
                            "PARTIAL_RESUME"
                            if row["cuboid_job_id"] in partial_ids
                            else "NEW"
                        ),
                    }
                    for row in next_rows[:list_next]
                ],
                indent=2,
            )
        )
    selected: dict[str, Any] | None = None
    if requested_job_id:
        if requested_job_id not in manifest_by_id:
            raise ValueError(f"unknown cuboid job id: {requested_job_id}")
        selected = manifest_by_id[requested_job_id]
    elif choose_next and next_rows:
        selected = next_rows[0]
    processed_this_run = 0
    if selected is not None and not status_only:
        cuboid_id = selected["cuboid_job_id"]
        if cuboid_id in carried and cuboid_id not in states:
            selected = None
        else:
            profile = member_profile(
                cuboid_id, memberships_by_cuboid, fibers_by_id
            )
            state = states.get(cuboid_id)
            if state is None:
                state = initial_state(selected, profile)
            state.setdefault("created_revision", state.get("revision", REVISION))
            state.setdefault("depth_extension_history", [])
            state.setdefault(
                "maximum_refinement_depth_allowed", MAXIMUM_REFINEMENT_DEPTH
            )
            state["revision"] = REVISION
            if (
                state["source_fiber_membership_sha256"]
                != selected["source_fiber_membership_sha256"]
            ):
                raise RuntimeError("stale cuboid membership hash in resume state")
            if reopen_terminal_depth:
                reopen_depth_limit(
                    state,
                    maximum_refinement_depth,
                    depth_extension_axis,
                )
            if integrate_repair_5471:
                integrate_5471_repair(state)
            stable, parent, cells, support_segments, branches = base_5467.load_parent()
            if parent.REVISION != PARENT_REVISION:
                raise RuntimeError(
                    f"expected parent revision {PARENT_REVISION}, found {parent.REVISION}"
                )
            state = process_state(
                base_5467,
                base_5468,
                stable,
                parent,
                cells,
                support_segments,
                branches,
                selected,
                state,
                WORK / f"{cuboid_id}.json",
                maximum_node_evaluations,
                maximum_runtime_seconds,
                maximum_refinement_depth,
            )
            processed_this_run = int(state["processed_this_run"])
            states[cuboid_id] = state
    certificates = dict(carried)
    for cuboid_id, state in states.items():
        update_state_decision(state)
        if truth(state["valid_for_resumable_three_axis_cuboid_certificate"]):
            certificates[cuboid_id] = state_certificate(
                manifest_by_id[cuboid_id], state
            )
    certificate_rows = sorted(
        certificates.values(), key=lambda row: row["cuboid_job_id"]
    )
    if certificate_rows:
        base_5467.atomic_csv(CERTIFICATES, certificate_rows)
    progress_rows: list[dict[str, Any]] = []
    for cuboid_id, state in sorted(states.items()):
        progress_rows.append(
            {
                "cuboid_job_id": cuboid_id,
                "source_leaf_count": int(state["source_leaf_count"]),
                "decision": state["decision"],
                "node_evaluation_count": int(state["node_evaluation_count"]),
                "accepted_subcuboid_count": len(state["accepted"]),
                "pending_subcuboid_count": len(state["stack"]),
                "unresolved_subcuboid_count": len(state["unresolved"]),
                "runtime_seconds": float(state["runtime_seconds"]),
                "valid_for_resumable_three_axis_cuboid_certificate": truth(
                    state["valid_for_resumable_three_axis_cuboid_certificate"]
                ),
            }
        )
    if progress_rows:
        base_5467.atomic_csv(PROGRESS, progress_rows)
    partial_states = [
        state
        for state in states.values()
        if state["stack"] and not state["unresolved"]
    ]
    failed_states = [state for state in states.values() if state["unresolved"]]
    certified_source_leaf_count = sum(
        int(manifest_by_id[cuboid_id]["source_leaf_count"])
        for cuboid_id in certificates
    )
    complete = len(certificates) == len(manifest) and not failed_states
    next_target = ""
    if partial_states:
        next_target = sorted(
            partial_states,
            key=lambda state: int(
                manifest_by_id[state["cuboid_job_id"]]["evaluation_priority"]
            ),
        )[0]["cuboid_job_id"]
    elif failed_states:
        next_target = failed_states[0]["cuboid_job_id"]
    else:
        remaining_rows = [
            row for row in manifest if row["cuboid_job_id"] not in certificates
        ]
        if remaining_rows:
            remaining_rows.sort(key=lambda row: int(row["evaluation_priority"]))
            next_target = remaining_rows[0]["cuboid_job_id"]
    after_formalization = base_5467.formalization_snapshot()
    payload: dict[str, Any] = {
        "checkpoint": CHECKPOINT,
        "revision": REVISION,
        "parent_revision": PARENT_REVISION,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "decision": (
            "ALL_OUTER_CUBOIDS_CERTIFIED__AGGREGATE_INNER_AND_PRINCIPAL"
            if complete
            else (
                "THREE_AXIS_DEPTH_LIMIT__SPLIT_RECORDED_SOURCE_MEMBERSHIP"
                if failed_states
                else "THREE_AXIS_CUBOID_CERTIFICATION_PARTIAL__RESUME"
            )
        ),
        "cuboid_manifest_count": len(manifest),
        "source_fiber_count": len(fibers_by_id),
        "source_leaf_count": sum(int(row["source_leaf_count"]) for row in manifest),
        "carried_checkpoint_5468_certificate_count": len(carried),
        "three_axis_certificate_count": sum(
            truth(state["valid_for_resumable_three_axis_cuboid_certificate"])
            for state in states.values()
        ),
        "certified_cuboid_count": len(certificates),
        "certified_source_leaf_count": certified_source_leaf_count,
        "remaining_cuboid_count": len(manifest) - len(certificates),
        "remaining_source_leaf_count": EXPECTED_SOURCE_LEAF_COUNT
        - certified_source_leaf_count,
        "partial_cuboid_count": len(partial_states),
        "failed_cuboid_count": len(failed_states),
        "accepted_subcuboid_count": sum(
            len(state["accepted"]) for state in states.values()
        ),
        "pending_subcuboid_count": sum(
            len(state["stack"]) for state in states.values()
        ),
        "unresolved_subcuboid_count": sum(
            len(state["unresolved"]) for state in states.values()
        ),
        "node_evaluation_count": sum(
            int(state["node_evaluation_count"]) for state in states.values()
        ),
        "processed_this_run": processed_this_run,
        "next_target": (
            "COMBINE_CERTIFIED_OUTER_WITH_INNER_Q_AND_PRINCIPAL_PART"
            if complete
            else next_target
        ),
        "valid_for_full_outer_parent_leaf_enclosure": complete,
        "valid_for_full_event_cell_finite_cover": False,
        "valid_for_D4_event_local_W3_bound": False,
        "valid_for_all_operator_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    state_hashes_match = all(
        state["source_fiber_membership_sha256"]
        == manifest_by_id[cuboid_id]["source_fiber_membership_sha256"]
        for cuboid_id, state in states.items()
    )
    completed_states_are_exact = all(
        not truth(state["valid_for_resumable_three_axis_cuboid_certificate"])
        or (
            not state["stack"]
            and not state["unresolved"]
            and float(state["coverage_error"])
            <= 1.0e-12 * max(float(state["root_volume"]), 1.0)
        )
        for state in states.values()
    )
    validations = [
        check("all_sources_exist", not missing, len(source_paths())),
        check(
            "checkpoint_5468_exact_cuboid_cover_is_valid",
            int(result_5468.get("cuboid_manifest_count", -1))
            == EXPECTED_CUBOID_COUNT
            and int(result_5468.get("failed_validation_count", -1)) == 0
            and all(truth(row["passed"]) for row in validation_5468),
            result_5468.get("decision"),
        ),
        check(
            "source_counts_are_preserved",
            len(manifest) == EXPECTED_CUBOID_COUNT
            and len(fibers_by_id) == EXPECTED_FIBER_COUNT
            and payload["source_leaf_count"] == EXPECTED_SOURCE_LEAF_COUNT,
            f"cuboids={len(manifest)};fibers={len(fibers_by_id)};leaves={payload['source_leaf_count']}",
        ),
        check(
            "membership_rows_are_complete",
            len(membership) == EXPECTED_FIBER_COUNT
            and len({row["source_fiber_job_id"] for row in membership})
            == EXPECTED_FIBER_COUNT,
            len(membership),
        ),
        check(
            "all_resume_states_match_current_membership",
            state_hashes_match,
            len(states),
        ),
        check(
            "completed_three_axis_states_have_exact_coverage",
            completed_states_are_exact,
            sum(
                truth(state["valid_for_resumable_three_axis_cuboid_certificate"])
                for state in states.values()
            ),
        ),
        check(
            "every_certified_cuboid_has_positive_parent_factors",
            all(
                all(
                    math.isfinite(float(row[field])) and float(row[field]) > 0.0
                    for field in (
                        "minimum_amplitude_denominator_abs_lower",
                        "relative_root_abs_lower",
                        "selected_global_root_abs_lower",
                        "collision_jacobian_abs_lower",
                    )
                )
                for row in certificate_rows
            ),
            len(certificate_rows),
        ),
        check(
            "partial_and_depth_limit_states_remain_nonclaim",
            all(
                not truth(state["valid_for_full_outer_parent_leaf_enclosure"])
                and not truth(state["valid_for_D4_event_local_W3_bound"])
                and not truth(state["valid_for_all_operator_local_GR_claim"])
                and not truth(state["valid_for_full_MTS_claim"])
                for state in states.values()
            ),
            len(states),
        ),
        check(
            "formalization_workbench_untouched",
            before_formalization == after_formalization,
            f"before={len(before_formalization)};after={len(after_formalization)}",
        ),
        check(
            "broad_claims_remain_false",
            not payload["valid_for_full_event_cell_finite_cover"]
            and not payload["valid_for_D4_event_local_W3_bound"]
            and not payload["valid_for_all_operator_local_GR_claim"]
            and not payload["valid_for_full_MTS_claim"],
            "resumable outer cuboid layer only",
        ),
    ]
    payload["validation_row_count"] = len(validations)
    payload["failed_validation_count"] = sum(
        not row["passed"] for row in validations
    )
    register = [
        {
            "checkpoint": CHECKPOINT,
            "source_path": str(path),
            "sha256": digest(path),
            "exists": path.is_file(),
            "source_role": "resumable-three-axis-parent-input",
        }
        for path in source_paths()
    ]
    base_5467.atomic_csv(SOURCE_REGISTER, register)
    base_5467.atomic_csv(VALIDATION, validations)
    base_5467.atomic_json(STATUS, payload)
    base_5467.atomic_json(RESULT, payload)
    render_document(payload, base_5467)
    return payload


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--job-id")
    parser.add_argument("--next", action="store_true")
    parser.add_argument("--max-node-evaluations", type=int, default=8)
    parser.add_argument("--max-runtime-seconds", type=float, default=600.0)
    parser.add_argument(
        "--maximum-refinement-depth",
        type=int,
        default=MAXIMUM_REFINEMENT_DEPTH,
    )
    parser.add_argument("--reopen-terminal-depth", action="store_true")
    parser.add_argument(
        "--depth-extension-axis",
        choices=tuple(AXIS_FIELDS),
    )
    parser.add_argument("--integrate-repair-5471", action="store_true")
    parser.add_argument("--status-only", action="store_true")
    parser.add_argument("--list-next", type=int, default=0)
    arguments = parser.parse_args()
    if arguments.max_node_evaluations <= 0:
        raise ValueError("--max-node-evaluations must be positive")
    if arguments.max_runtime_seconds <= 0.0:
        raise ValueError("--max-runtime-seconds must be positive")
    if arguments.maximum_refinement_depth < MAXIMUM_REFINEMENT_DEPTH:
        raise ValueError(
            f"--maximum-refinement-depth must be at least {MAXIMUM_REFINEMENT_DEPTH}"
        )
    payload = run(
        arguments.job_id,
        arguments.next,
        arguments.max_node_evaluations,
        arguments.max_runtime_seconds,
        arguments.maximum_refinement_depth,
        arguments.reopen_terminal_depth,
        arguments.depth_extension_axis,
        arguments.integrate_repair_5471,
        arguments.status_only,
        arguments.list_next,
    )
    print(
        json.dumps(
            {
                key: payload[key]
                for key in (
                    "decision",
                    "certified_cuboid_count",
                    "certified_source_leaf_count",
                    "partial_cuboid_count",
                    "failed_cuboid_count",
                    "accepted_subcuboid_count",
                    "pending_subcuboid_count",
                    "node_evaluation_count",
                    "processed_this_run",
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
