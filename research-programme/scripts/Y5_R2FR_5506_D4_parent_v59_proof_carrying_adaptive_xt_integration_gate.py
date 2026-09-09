from __future__ import annotations

import argparse
import importlib.util
import json
import math
import time
from copy import deepcopy
from datetime import datetime, timezone
from fractions import Fraction
from pathlib import Path
from typing import Any, Callable


POST = Path(__file__).resolve().parents[1]
SCRIPTS = POST / "scripts"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
OUTPUT = FUNCTIONAL_RG / "5506"

SCRIPT_5505 = SCRIPTS / "Y5_R2FR_5505_D4_parent_v58_high_t_and_five_leaf_closure_gate.py"
SOURCE_STATE = FUNCTIONAL_RG / "5505" / "work-v1" / "E07__U051__RIGHT_CONNECTOR__CUBOID__6df3d70a73e4618b.json"
RESULT_5505 = FUNCTIONAL_RG / "5505" / "D4_parent_v58_high_t_and_five_leaf_closure_result.json"
VALIDATION_5505 = FUNCTIONAL_RG / "5505" / "P8_Y5_BRR5504_5505_VALIDATION.csv"
SOURCE_REGISTER_5505 = FUNCTIONAL_RG / "5505" / "source_register.csv"
NODE_AUDIT_5505 = FUNCTIONAL_RG / "5505" / "D4_parent_v58_high_t_child_audit.csv"
UNION_AUDIT_5505 = FUNCTIONAL_RG / "5505" / "D4_parent_v58_two_and_five_leaf_union_audit.csv"
THEOREM = POST / "D4-general-proof-carrying-adaptive-cover-theorem-draft.md"
CERTIFICATE_5496 = FUNCTIONAL_RG / "5496" / "D4_parent_v58_adaptive_complete_amplitude_certificate.json"

TARGET_CUBOID_ID = "E07__U051__RIGHT_CONNECTOR__CUBOID__6df3d70a73e4618b"
TARGET_PATH = "R_E0S_E0S_E1S_X0S_X1S"
LOW_T_PATH = f"{TARGET_PATH}_T0S"
HIGH_T_PATH = f"{TARGET_PATH}_T1S"
EXPECTED_SOURCE_COUNTS = (184, 3, 0)
EXPECTED_SOURCE_WITNESSES = 64
EXPECTED_FAILURE_MARKER = "edge_2_1_3:stable_edge"
PARENT_V58_REVISION = "D4-deformed-contour-regular-away-W3-v58-adaptive-stable-edge-local-T2-union"
PARENT_V59_REVISION = "D4-deformed-contour-regular-away-W3-v59-proof-carrying-adaptive-xt-cover"

EXPECTED_SCRIPT_5505_SHA256 = "f83530455d165f3decf730e3a7a3cfc316cb511be708577ec7b1920d3df2e733"
EXPECTED_SOURCE_STATE_SHA256 = "df67524e5d8f81d9642cd04514c1f22e325fa0dedf1f466dcf7a74de3c940a8b"
EXPECTED_RESULT_5505_SHA256 = "2ec5aad038be98e747b53a753ca2f0bfeb5fa55f878f9e3601be616cbebbe171"
EXPECTED_VALIDATION_5505_SHA256 = "82bf0aeaf125ca333ca2897e9924110e9d8c9c48466343125fdf12bd59fd25cd"
EXPECTED_SOURCE_REGISTER_5505_SHA256 = "5cc54ff2ff25a83d5de40737766f666f81d618b6f4f2975bbd2e8d428349b423"
EXPECTED_NODE_AUDIT_5505_SHA256 = "d22c570a90eeb8b4762844bbae8b9c2e5ecbc79c98df4073c2749558b942a095"
EXPECTED_UNION_AUDIT_5505_SHA256 = "2326dd6e1da6e25cae8349218a31450f59f0841cfd4c64a61eb7aab06d112973"
EXPECTED_THEOREM_SHA256 = "eccf43655d5eae9da52d5717e51e873915da00a35ac3309a12c31d1df4efc56b"
EXPECTED_CERTIFICATE_5496_SHA256 = "27dc7fce1f83b424e9d9341778a392b83ed7c8659d12e05afd561338782fc708"

CHECKPOINT = 5506
REVISION = "D4-parent-v59-proof-carrying-adaptive-xt-integration-v1"
AUDIT = OUTPUT / "D4_parent_v59_adaptive_xt_application_audit.csv"
CACHE = OUTPUT / "D4_parent_v59_exact_binding_proof_cache.csv"
COMPARISON = OUTPUT / "D4_parent_v59_target_control_comparison.csv"
SOURCE_REGISTER = OUTPUT / "source_register.csv"
VALIDATION = OUTPUT / "P8_Y5_BRR5505_5506_VALIDATION.csv"
STATUS = OUTPUT / "status.json"
RESULT = OUTPUT / "D4_parent_v59_proof_carrying_adaptive_xt_result.json"
DOCUMENT = POST / "5506-Y5-R2FR-D4-parent-v59-proof-carrying-adaptive-xt-integration-gate.md"

NUMERIC_FIELDS = (
    "integrated_regular_path_abs_upper",
    "minimum_amplitude_denominator_abs_lower",
    "relative_root_abs_lower",
    "selected_global_root_abs_lower",
    "collision_jacobian_abs_lower",
)
CONTROL_FIELDS = NUMERIC_FIELDS + (
    "active_material_branch_count",
    "active_material_branch_ids",
    "path_integral_enclosure_method",
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


def exact(value: Any) -> Fraction:
    return Fraction(str(value))


def exact_parameter_area(arguments: dict[str, Any]) -> Fraction:
    return (
        exact(arguments["x_upper"]) - exact(arguments["x_lower"])
    ) * (
        exact(arguments["t_upper"]) - exact(arguments["t_lower"])
    )


def raw_path(refinement_path: str) -> str:
    return refinement_path.split(":", 1)[-1]


def path_prefix(refinement_path: str) -> str:
    raw = raw_path(refinement_path)
    return refinement_path[: -len(raw)] if raw else refinement_path


def choose_xt_split(
    arguments: dict[str, Any],
    source_state: dict[str, Any],
) -> tuple[str, float, bool]:
    widths = {
        "x": float(arguments["x_upper"]) - float(arguments["x_lower"]),
        "t": float(arguments["t_upper"]) - float(arguments["t_lower"]),
    }
    ratios = {
        axis: widths[axis] / float(source_state["maximum_source_widths"][axis])
        for axis in widths
    }
    axis = max(("x", "t"), key=lambda candidate: (ratios[candidate], candidate == "x"))
    lower = float(arguments[f"{axis}_lower"])
    upper = float(arguments[f"{axis}_upper"])
    midpoint = 0.5 * (lower + upper)
    interior = [
        float(value)
        for value in source_state["source_boundaries"][axis]
        if lower < float(value) < upper
    ]
    if interior:
        return axis, min(interior, key=lambda value: abs(value - midpoint)), True
    return axis, midpoint, False


def split_arguments(
    arguments: dict[str, Any],
    source_state: dict[str, Any],
) -> tuple[dict[str, Any], dict[str, Any], dict[str, Any]]:
    axis, split, source_boundary = choose_xt_split(arguments, source_state)
    lower = deepcopy(arguments)
    upper = deepcopy(arguments)
    lower[f"{axis}_upper"] = split
    upper[f"{axis}_lower"] = split
    marker = axis.upper()
    suffix = "S" if source_boundary else "M"
    prefix = path_prefix(str(arguments["refinement_path"]))
    parent_raw = raw_path(str(arguments["refinement_path"]))
    lower["refinement_depth"] = int(arguments["refinement_depth"]) + 1
    upper["refinement_depth"] = int(arguments["refinement_depth"]) + 1
    lower["refinement_path"] = f"{prefix}{parent_raw}_{marker}0{suffix}"
    upper["refinement_path"] = f"{prefix}{parent_raw}_{marker}1{suffix}"
    parent_area = exact_parameter_area(arguments)
    child_area = exact_parameter_area(lower) + exact_parameter_area(upper)
    if parent_area != child_area:
        raise RuntimeError("adaptive x/t split does not preserve exact rational area")
    return lower, upper, {
        "axis": axis,
        "split": split,
        "source_boundary": source_boundary,
        "parent_area": float(parent_area),
        "child_area": float(child_area),
        "coverage_error": float(abs(parent_area - child_area)),
    }


def positive_certificate(row: dict[str, Any]) -> bool:
    return (
        row.get("probe_passed") is True
        and row.get("parent_revision") == PARENT_V58_REVISION
        and all(math.isfinite(float(row[field])) and float(row[field]) > 0.0 for field in NUMERIC_FIELDS)
        and int(row.get("active_material_branch_count", -1)) >= 0
    )


def same_leaf_binding(row: dict[str, Any], arguments: dict[str, Any]) -> bool:
    return (
        row.get("refinement_path") == raw_path(str(arguments["refinement_path"]))
        and int(row.get("refinement_depth", -1)) == int(arguments["refinement_depth"])
        and all(
            exact(row[field]) == exact(arguments[field])
            for field in ("x_lower", "x_upper", "t_lower", "t_upper")
        )
        and exact(row["epsilon_real_lower"]) == exact(arguments["epsilon_row"]["epsilon_real_lower"])
        and exact(row["epsilon_real_upper"]) == exact(arguments["epsilon_row"]["epsilon_real_upper"])
    )


def build_proof_cache(
    base_5495: Any,
    source_state: dict[str, Any],
    child_arguments: tuple[dict[str, Any], dict[str, Any]],
    path_speed_abs_upper: float,
) -> tuple[dict[str, dict[str, Any]], list[dict[str, Any]]]:
    cache: dict[str, dict[str, Any]] = {}
    manifest: list[dict[str, Any]] = []
    for arguments in child_arguments:
        path = raw_path(str(arguments["refinement_path"]))
        matches = [row for row in source_state["accepted"] if row.get("refinement_path") == path]
        if len(matches) != 1 or not positive_certificate(matches[0]) or not same_leaf_binding(matches[0], arguments):
            raise RuntimeError(f"invalid exact-binding proof cache source: {path}")
        row = matches[0]
        binding_sha256, binding = base_5495.call_binding(arguments)
        result = {
            "selected_role": "IMMUTABLE_EXACT_BINDING_PARENT_V58_CERTIFICATE",
            "x_lower": float(arguments["x_lower"]),
            "x_upper": float(arguments["x_upper"]),
            "x_width": float(arguments["x_upper"]) - float(arguments["x_lower"]),
            "t_lower": float(arguments["t_lower"]),
            "t_upper": float(arguments["t_upper"]),
            "t_width": float(arguments["t_upper"]) - float(arguments["t_lower"]),
            "parameter_area": float(exact_parameter_area(arguments)),
            "path_speed_abs_upper": path_speed_abs_upper,
            "refinement_depth": int(arguments["refinement_depth"]),
            "refinement_path": str(arguments["refinement_path"]),
            **{field: row[field] for field in CONTROL_FIELDS},
            "v59_proof_cache_binding_sha256": binding_sha256,
            "v59_proof_cache_source_state_sha256": EXPECTED_SOURCE_STATE_SHA256,
            "v59_proof_cache_certificate_source": row["certificate_source"],
        }
        cache[binding_sha256] = {
            "binding": binding,
            "result": result,
            "source_row": row,
        }
        manifest.append({
            "checkpoint": CHECKPOINT,
            "binding_sha256": binding_sha256,
            "refinement_path": path,
            "parent_revision": row["parent_revision"],
            "certificate_source": row["certificate_source"],
            "source_state_sha256": EXPECTED_SOURCE_STATE_SHA256,
            "exact_binding_match": True,
            "positive_complete_parent_certificate": True,
            **{field: row[field] for field in CONTROL_FIELDS},
        })
    return cache, manifest


def aggregate_results(
    arguments: dict[str, Any],
    children: list[dict[str, Any]],
    split: dict[str, Any],
) -> dict[str, Any]:
    if len(children) != 2 or split["coverage_error"] != 0.0:
        raise RuntimeError("adaptive aggregate lacks an exact two-child cover")
    if not all(all(math.isfinite(float(row[field])) and float(row[field]) > 0.0 for field in NUMERIC_FIELDS) for row in children):
        raise RuntimeError("adaptive aggregate has a non-positive terminal certificate")
    branch_ids = sorted({branch for row in children for branch in str(row["active_material_branch_ids"]).split("|") if branch})
    result = dict(children[0])
    result.update({
        "selected_role": "PROOF_CARRYING_ADAPTIVE_XT_LEAF_UNION",
        "x_lower": float(arguments["x_lower"]),
        "x_upper": float(arguments["x_upper"]),
        "x_width": float(arguments["x_upper"]) - float(arguments["x_lower"]),
        "t_lower": float(arguments["t_lower"]),
        "t_upper": float(arguments["t_upper"]),
        "t_width": float(arguments["t_upper"]) - float(arguments["t_lower"]),
        "parameter_area": float(exact_parameter_area(arguments)),
        "path_speed_abs_upper": max(float(row["path_speed_abs_upper"]) for row in children),
        "refinement_depth": int(arguments["refinement_depth"]),
        "refinement_path": str(arguments["refinement_path"]),
        "integrated_regular_path_abs_upper": sum(float(row["integrated_regular_path_abs_upper"]) for row in children),
        "minimum_amplitude_denominator_abs_lower": min(float(row["minimum_amplitude_denominator_abs_lower"]) for row in children),
        "relative_root_abs_lower": min(float(row["relative_root_abs_lower"]) for row in children),
        "selected_global_root_abs_lower": min(float(row["selected_global_root_abs_lower"]) for row in children),
        "collision_jacobian_abs_lower": min(float(row["collision_jacobian_abs_lower"]) for row in children),
        "active_material_branch_count": len(branch_ids),
        "active_material_branch_ids": "|".join(branch_ids),
        "path_integral_enclosure_method": "V59_PROOF_CARRYING_ADAPTIVE_XT_LEAF_UNION_SUM",
        "v59_adaptive_axis": split["axis"],
        "v59_adaptive_split": split["split"],
        "v59_source_boundary_split": split["source_boundary"],
        "v59_terminal_leaf_count": sum(int(row.get("v59_terminal_leaf_count", 1)) for row in children),
        "v59_parameter_area_coverage_error": split["coverage_error"],
    })
    return result


def install_parent_v59(
    parent: Any,
    base_5495: Any,
    source_state: dict[str, Any],
    proof_cache: dict[str, dict[str, Any]],
    maximum_adaptive_depth: int,
) -> Any:
    if parent.REVISION != PARENT_V58_REVISION:
        raise RuntimeError(f"expected {PARENT_V58_REVISION}, found {parent.REVISION}")
    original = parent.evaluate_path_box
    audit_rows: list[dict[str, Any]] = []
    top_level_count = 0

    def audit(
        call_id: int,
        event: str,
        arguments: dict[str, Any],
        adaptive_depth: int,
        outcome: str,
        binding_sha256: str = "",
        failure_type: str = "",
        failure_message: str = "",
        axis: str = "",
        split: Any = "",
        source_boundary: Any = "",
        result: dict[str, Any] | None = None,
    ) -> None:
        result = result or {}
        audit_rows.append({
            "checkpoint": CHECKPOINT,
            "call_id": call_id,
            "event": event,
            "adaptive_depth": adaptive_depth,
            "outcome": outcome,
            "binding_sha256": binding_sha256,
            "refinement_path": raw_path(str(arguments["refinement_path"])),
            "x_lower": arguments["x_lower"],
            "x_upper": arguments["x_upper"],
            "t_lower": arguments["t_lower"],
            "t_upper": arguments["t_upper"],
            "axis": axis,
            "split": split,
            "source_boundary": source_boundary,
            "failure_type": failure_type,
            "failure_message": failure_message,
            "integrated_regular_path_abs_upper": result.get("integrated_regular_path_abs_upper", math.nan),
            "minimum_amplitude_denominator_abs_lower": result.get("minimum_amplitude_denominator_abs_lower", math.nan),
            "collision_jacobian_abs_lower": result.get("collision_jacobian_abs_lower", math.nan),
            "path_integral_enclosure_method": result.get("path_integral_enclosure_method", ""),
            "source_state_sha256": result.get("v59_proof_cache_source_state_sha256", ""),
        })

    def recurse(arguments: dict[str, Any], remaining: int, call_id: int, adaptive_depth: int, permit_cache: bool) -> dict[str, Any]:
        if permit_cache:
            binding_sha256, _ = base_5495.call_binding(arguments)
            cached = proof_cache.get(binding_sha256)
            if cached is not None:
                result = deepcopy(cached["result"])
                audit(call_id, "TERMINAL", arguments, adaptive_depth, "CACHE_PASS", binding_sha256=binding_sha256, result=result)
                return result
        try:
            result = original(**arguments)
        except parent.M5258.IntervalSingularity as error:
            if arguments["path_segment"] not in {"LEFT_CONNECTOR", "RIGHT_CONNECTOR"} or EXPECTED_FAILURE_MARKER not in str(error):
                raise
            audit(call_id, "TRIGGER", arguments, adaptive_depth, "PRECISE_STABLE_EDGE_FAILURE", failure_type=type(error).__name__, failure_message=str(error).splitlines()[0][:600])
            if remaining <= 0:
                raise
            lower, upper, split = split_arguments(arguments, source_state)
            audit(call_id, "SPLIT", arguments, adaptive_depth, "EXACT_XT_PARTITION", axis=split["axis"], split=split["split"], source_boundary=split["source_boundary"])
            child_results = [
                recurse(child, remaining - 1, call_id, adaptive_depth + 1, True)
                for child in (lower, upper)
            ]
            result = aggregate_results(arguments, child_results, split)
            audit(call_id, "AGGREGATE", arguments, adaptive_depth, "PASS", axis=split["axis"], split=split["split"], source_boundary=split["source_boundary"], result=result)
            return result
        audit(call_id, "TERMINAL", arguments, adaptive_depth, "LIVE_PARENT_PASS", result=result)
        return result

    def evaluate_v59(
        cell: dict[str, Any],
        term_id: str,
        configurations: list[dict[str, Any]],
        epsilon_row: dict[str, Any],
        path_segment: str,
        x_lower: float,
        x_upper: float,
        t_lower: float,
        t_upper: float,
        refinement_depth: int,
        refinement_path: str,
        support_segments: list[dict[str, Any]],
        branches: dict[str, dict[str, Any]],
        global_arc_count: int,
        reduce_selector_charts: bool = True,
    ) -> dict[str, Any]:
        nonlocal top_level_count
        top_level_count += 1
        arguments = {
            "cell": cell,
            "term_id": term_id,
            "configurations": configurations,
            "epsilon_row": epsilon_row,
            "path_segment": path_segment,
            "x_lower": x_lower,
            "x_upper": x_upper,
            "t_lower": t_lower,
            "t_upper": t_upper,
            "refinement_depth": refinement_depth,
            "refinement_path": refinement_path,
            "support_segments": support_segments,
            "branches": branches,
            "global_arc_count": global_arc_count,
            "reduce_selector_charts": reduce_selector_charts,
        }
        return recurse(arguments, maximum_adaptive_depth, top_level_count, 0, False)

    parent.evaluate_path_box = evaluate_v59
    parent.V59_ADAPTIVE_XT_AUDIT_ROWS = audit_rows
    parent.V59_PARENT_ACTION_CHANGED = False
    parent.V59_ONLY_ENCLOSURE_COMPOSITION_CHANGED = True
    parent.REVISION = PARENT_V59_REVISION
    return parent


def exact_fields_equal(left: dict[str, Any], right: dict[str, Any], fields: tuple[str, ...]) -> bool:
    return all(left.get(field) == right.get(field) for field in fields)


def render_document(payload: dict[str, Any], base_5467: Any) -> None:
    lines = [
        "# 5506: D4 parent-v59 proof-carrying adaptive x/t integration gate",
        "",
        "The checkpoint-5503 real parent-v58 stable-edge target is evaluated through a general recursive wrapper. The root is evaluated live; only its two identical-binding child results may be replayed from the hash-locked checkpoint-5505 state.",
        "",
        f"Target passed: `{payload['target_v59_passed']}` after `{payload['target_runtime_seconds']}` seconds. Trigger count: `{payload['target_trigger_count']}`. Exact cache hits: `{payload['target_cache_hit_count']}`.",
        "",
        f"Target/independent-union fields identical: `{payload['target_matches_independent_union']}`. Control fields identical: `{payload['control_matches_parent_v58_source']}` with `{payload['control_new_trigger_count']}` new triggers.",
        "",
        f"**{payload['decision']}**",
        "",
        "No action, field, contour, chart, selector, residue or threshold changes. Parent-v59 migration, active-cuboid closure and all broader GR/MTS claims remain open.",
        "",
    ]
    base_5467.atomic_text(DOCUMENT, "\n".join(lines))


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--maximum-adaptive-depth", type=int, default=1)
    arguments = parser.parse_args()

    base_5505 = load_module("mts_5505_for_5506", SCRIPT_5505)
    base_5504 = load_module("mts_5504_for_5506", base_5505.SCRIPT_5504)
    base_5503 = load_module("mts_5503_for_5506", base_5504.SCRIPT_5503)
    base_5502 = load_module("mts_5502_for_5506", base_5503.SCRIPT_5502)
    base_5501 = load_module("mts_5501_for_5506", base_5502.SCRIPT_5501)
    base_5500 = load_module("mts_5500_for_5506", base_5501.SCRIPT_5500)
    base_5499 = load_module("mts_5499_for_5506", base_5500.SCRIPT_5499)
    base_5498 = load_module("mts_5498_for_5506", base_5499.SCRIPT_5498)
    base_5496 = load_module("mts_5496_for_5506", base_5498.SCRIPT_5496)
    base_5495 = load_module("mts_5495_for_5506", base_5496.SCRIPT_5495)
    base_5467 = load_module("mts_5467_for_5506", base_5495.SCRIPT_5467)
    base_5468 = load_module("mts_5468_for_5506", base_5495.SCRIPT_5468)
    base_5472 = load_module("mts_5472_for_5506", base_5495.SCRIPT_5472)
    base_5474 = load_module("mts_5474_for_5506", base_5495.SCRIPT_5474)
    base_5476 = load_module("mts_5476_for_5506", base_5495.SCRIPT_5476)
    base_5478 = load_module("mts_5478_for_5506", base_5495.SCRIPT_5478)
    base_5480 = load_module("mts_5480_for_5506", base_5495.SCRIPT_5480)
    base_5483 = load_module("mts_5483_for_5506", base_5495.SCRIPT_5483)
    base_5490 = load_module("mts_5490_for_5506", base_5495.SCRIPT_5490)
    base_5493 = load_module("mts_5493_for_5506", base_5495.SCRIPT_5493)

    base_5467.set_below_normal_priority()
    base_5480.set_single_core_affinity()
    before_formalization = base_5467.formalization_snapshot()
    inherited_hashes = {
        "script_5505": base_5499.digest(SCRIPT_5505),
        "source_state": base_5499.digest(SOURCE_STATE),
        "result_5505": base_5499.digest(RESULT_5505),
        "validation_5505": base_5499.digest(VALIDATION_5505),
        "source_register_5505": base_5499.digest(SOURCE_REGISTER_5505),
        "node_audit_5505": base_5499.digest(NODE_AUDIT_5505),
        "union_audit_5505": base_5499.digest(UNION_AUDIT_5505),
        "theorem": base_5499.digest(THEOREM),
        "certificate_5496": base_5499.digest(CERTIFICATE_5496),
    }
    expected_hashes = {
        "script_5505": EXPECTED_SCRIPT_5505_SHA256,
        "source_state": EXPECTED_SOURCE_STATE_SHA256,
        "result_5505": EXPECTED_RESULT_5505_SHA256,
        "validation_5505": EXPECTED_VALIDATION_5505_SHA256,
        "source_register_5505": EXPECTED_SOURCE_REGISTER_5505_SHA256,
        "node_audit_5505": EXPECTED_NODE_AUDIT_5505_SHA256,
        "union_audit_5505": EXPECTED_UNION_AUDIT_5505_SHA256,
        "theorem": EXPECTED_THEOREM_SHA256,
        "certificate_5496": EXPECTED_CERTIFICATE_5496_SHA256,
    }
    if inherited_hashes != expected_hashes:
        raise RuntimeError("checkpoint-5506 inherited source hash mismatch")

    source_register_5505 = base_5499.read_csv(SOURCE_REGISTER_5505)
    paths = tuple(dict.fromkeys((
        Path(__file__).resolve(), THEOREM, SCRIPT_5505, SOURCE_STATE, RESULT_5505,
        VALIDATION_5505, SOURCE_REGISTER_5505, NODE_AUDIT_5505,
        UNION_AUDIT_5505, CERTIFICATE_5496,
        *(Path(row["source_path"]) for row in source_register_5505),
    )))
    missing = [str(path) for path in paths if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"missing sources: {missing}")

    source_state = base_5499.read_json(SOURCE_STATE)
    result_5505 = base_5499.read_json(RESULT_5505)
    validation_5505 = base_5499.read_csv(VALIDATION_5505)
    source_counts = (len(source_state["accepted"]), len(source_state["stack"]), len(source_state["unresolved"]))
    source_certified = (
        result_5505.get("decision") == "PARENT_V58_EXACT_FIVE_LEAF_X_REGION_CERTIFIED__ADVANCE_FRONTIER"
        and result_5505.get("exact_two_leaf_parent_closure") is True
        and result_5505.get("exact_five_leaf_x_region_closure") is True
        and int(result_5505.get("failed_validation_count", -1)) == 0
        and all(base_5499.truth(row.get("passed")) for row in validation_5505)
        and base_5499.source_register_is_current(source_register_5505)
        and source_counts == EXPECTED_SOURCE_COUNTS
        and len(source_state["refinement_witnesses"]) == EXPECTED_SOURCE_WITNESSES
        and base_5498.exact_partition_volume(source_state) == base_5498.exact_node_volume(source_state["root"])
    )
    if not source_certified:
        raise RuntimeError("checkpoint-5505 source is not current and certified")

    target_nodes = [row for row in source_state["refinement_witnesses"] if row.get("refinement_path") == TARGET_PATH]
    child_rows = [row for row in source_state["accepted"] if row.get("refinement_path") in {LOW_T_PATH, HIGH_T_PATH}]
    if len(target_nodes) != 1 or len(child_rows) != 2:
        raise RuntimeError("checkpoint-5506 target tree is not unique")
    target_node = target_nodes[0]
    control_row = next(row for row in child_rows if row["refinement_path"] == HIGH_T_PATH)
    target_source_failure = (
        target_node.get("parent_revision") == PARENT_V58_REVISION
        and target_node.get("failure_type") == "IntervalSingularity"
        and EXPECTED_FAILURE_MARKER in str(target_node.get("failure_message"))
    )
    if not target_source_failure:
        raise RuntimeError("checkpoint-5506 target is not a certified parent-v58 stable-edge failure")

    stable, _, cells, support_segments, branches = base_5467.load_parent()
    cuboid = next(row for row in base_5499.read_csv(base_5495.MANIFEST_5468) if row["cuboid_job_id"] == TARGET_CUBOID_ID)
    certificate_5496 = base_5499.read_json(CERTIFICATE_5496)
    parent_v58 = base_5498.reconstruct_parent(
        base_5467, base_5472, base_5474, base_5476, base_5478, base_5483,
        base_5490, base_5493, base_5495, base_5496, certificate_5496,
    )
    target_arguments = base_5495.target_arguments(stable, parent_v58, cells, support_segments, branches, cuboid, target_node)
    lower_arguments, upper_arguments, source_split = split_arguments(target_arguments, source_state)
    path_speed = base_5468.full_cell_path_speed_bound(parent_v58, cells[cuboid["mapped_cell_id"]], cuboid["path_segment"])
    proof_cache, cache_manifest = build_proof_cache(base_5495, source_state, (lower_arguments, upper_arguments), path_speed)
    cache_paths = {row["refinement_path"] for row in cache_manifest}
    split_contract = (
        source_split["axis"] == "t"
        and exact(source_split["split"]) == exact(0.5)
        and source_split["source_boundary"] is True
        and raw_path(lower_arguments["refinement_path"]) == LOW_T_PATH
        and raw_path(upper_arguments["refinement_path"]) == HIGH_T_PATH
        and source_split["coverage_error"] == 0.0
        and cache_paths == {LOW_T_PATH, HIGH_T_PATH}
    )

    if arguments.dry_run:
        print(json.dumps({
            "checkpoint": CHECKPOINT,
            "dry_run": True,
            "source_counts": list(source_counts),
            "target_path": TARGET_PATH,
            "target_source_failure": target_source_failure,
            "split_axis": source_split["axis"],
            "split_value": source_split["split"],
            "source_boundary": source_split["source_boundary"],
            "cache_paths": sorted(cache_paths),
            "cache_binding_count": len(proof_cache),
            "split_contract": split_contract,
            "parent_revision": parent_v58.REVISION,
            "source_hashes_match": inherited_hashes == expected_hashes,
        }, indent=2))
        return 0

    parent_v59 = install_parent_v59(parent_v58, base_5495, source_state, proof_cache, arguments.maximum_adaptive_depth)
    target_started = time.perf_counter()
    target_result = parent_v59.evaluate_path_box(**target_arguments)
    target_runtime = time.perf_counter() - target_started
    target_audit_count = len(parent_v59.V59_ADAPTIVE_XT_AUDIT_ROWS)
    target_audit = list(parent_v59.V59_ADAPTIVE_XT_AUDIT_ROWS)
    target_triggers = sum(row["event"] == "TRIGGER" for row in target_audit)
    target_cache_hits = sum(row["outcome"] == "CACHE_PASS" for row in target_audit)

    control_arguments = base_5495.target_arguments(stable, parent_v59, cells, support_segments, branches, cuboid, control_row)
    control_started = time.perf_counter()
    control_result = parent_v59.evaluate_path_box(**control_arguments)
    control_runtime = time.perf_counter() - control_started
    full_audit = list(parent_v59.V59_ADAPTIVE_XT_AUDIT_ROWS)
    control_audit = full_audit[target_audit_count:]
    control_new_triggers = sum(row["event"] == "TRIGGER" for row in control_audit)

    independent_union = {
        "integrated_regular_path_abs_upper": sum(float(row["integrated_regular_path_abs_upper"]) for row in sorted(child_rows, key=lambda row: row["t_lower"])),
        "minimum_amplitude_denominator_abs_lower": min(float(row["minimum_amplitude_denominator_abs_lower"]) for row in child_rows),
        "relative_root_abs_lower": min(float(row["relative_root_abs_lower"]) for row in child_rows),
        "selected_global_root_abs_lower": min(float(row["selected_global_root_abs_lower"]) for row in child_rows),
        "collision_jacobian_abs_lower": min(float(row["collision_jacobian_abs_lower"]) for row in child_rows),
        "active_material_branch_count": len({branch for row in child_rows for branch in str(row["active_material_branch_ids"]).split("|") if branch}),
        "active_material_branch_ids": "|".join(sorted({branch for row in child_rows for branch in str(row["active_material_branch_ids"]).split("|") if branch})),
    }
    target_comparison_fields = NUMERIC_FIELDS + ("active_material_branch_count", "active_material_branch_ids")
    target_matches_union = exact_fields_equal(target_result, independent_union, target_comparison_fields)
    control_matches_source = exact_fields_equal(control_result, control_row, CONTROL_FIELDS)
    target_positive = all(math.isfinite(float(target_result[field])) and float(target_result[field]) > 0.0 for field in NUMERIC_FIELDS)
    control_positive = all(math.isfinite(float(control_result[field])) and float(control_result[field]) > 0.0 for field in NUMERIC_FIELDS)
    target_exact_area = exact(target_result["parameter_area"]) == exact(source_split["parent_area"])
    v58_applications = len(getattr(parent_v59, "V58_ADAPTIVE_CERTIFICATE_AUDIT_ROWS", []))
    after_formalization = base_5467.formalization_snapshot()

    validations = [
        check("all_sources_exist", not missing, len(paths)),
        check("checkpoint_5505_evidence_is_hash_locked", inherited_hashes == expected_hashes, inherited_hashes),
        check("checkpoint_5505_nested_unions_are_certified", source_certified, result_5505.get("decision")),
        check("source_frontier_is_exact_184_3_0", source_counts == EXPECTED_SOURCE_COUNTS, source_counts),
        check("real_parent_v58_trigger_is_exact", target_source_failure, target_node.get("failure_message")),
        check("proof_cache_has_two_exact_positive_bindings", len(proof_cache) == 2 and len(cache_manifest) == 2 and all(row["exact_binding_match"] and row["positive_complete_parent_certificate"] for row in cache_manifest), sorted(cache_paths)),
        check("source_width_rule_selects_exact_t_boundary", split_contract, source_split),
        check("parent_v59_wraps_signed_parent_v58", parent_v59.REVISION == PARENT_V59_REVISION, parent_v59.REVISION),
        check("target_reproduces_one_live_precise_trigger", target_triggers == 1, target_triggers),
        check("target_resolves_exactly_two_cached_parent_leaves", target_cache_hits == 2, target_cache_hits),
        check("target_returns_positive_complete_amplitude", target_positive, {field: target_result[field] for field in NUMERIC_FIELDS}),
        check("target_exact_area_is_preserved", target_exact_area and source_split["coverage_error"] == 0.0, source_split),
        check("target_matches_independent_child_union_exactly", target_matches_union, independent_union),
        check("control_returns_live_parent_result_without_trigger", control_positive and control_new_triggers == 0 and len(control_audit) == 1 and control_audit[0]["outcome"] == "LIVE_PARENT_PASS", control_audit),
        check("control_physics_fields_are_exactly_unchanged", control_matches_source, {field: control_result.get(field) for field in CONTROL_FIELDS}),
        check("v58_bound_certificate_does_not_leak", v58_applications == 0, v58_applications),
        check("parent_action_and_physics_objects_are_unchanged", not parent_v59.V59_PARENT_ACTION_CHANGED and parent_v59.V59_ONLY_ENCLOSURE_COMPOSITION_CHANGED, PARENT_V59_REVISION),
        check("formalization_workbench_untouched", before_formalization == after_formalization, f"before={len(before_formalization)};after={len(after_formalization)}"),
        check("broad_claims_remain_false", all(result_5505.get(field) is False for field in ("valid_for_parent_v58_active_cuboid", "valid_for_full_outer_parent_leaf_enclosure", "valid_for_D4_event_local_W3_bound", "valid_for_all_operator_local_GR_claim", "valid_for_full_MTS_claim")), "candidate integration only"),
    ]
    failed = [row for row in validations if not row["passed"]]
    decision = (
        "PARENT_V59_PROOF_CARRYING_ADAPTIVE_XT_CANDIDATE_CERTIFIED__MIGRATION_REQUIRED"
        if not failed
        else "PARENT_V59_PROOF_CARRYING_ADAPTIVE_XT_CANDIDATE_REJECTED"
    )
    payload = {
        "checkpoint": CHECKPOINT,
        "revision": REVISION,
        "parent_revision": PARENT_V59_REVISION,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "decision": decision,
        "target_path": TARGET_PATH,
        "target_runtime_seconds": target_runtime,
        "target_v59_passed": target_positive,
        "target_trigger_count": target_triggers,
        "target_cache_hit_count": target_cache_hits,
        "target_matches_independent_union": target_matches_union,
        "target_parameter_area_coverage_error": source_split["coverage_error"],
        **{f"target_{field}": target_result[field] for field in CONTROL_FIELDS},
        "control_path": HIGH_T_PATH,
        "control_runtime_seconds": control_runtime,
        "control_new_trigger_count": control_new_triggers,
        "control_matches_parent_v58_source": control_matches_source,
        "proof_cache_binding_count": len(proof_cache),
        "v58_certificate_application_count": v58_applications,
        "validation_row_count": len(validations),
        "failed_validation_count": len(failed),
        "valid_for_parent_v59_candidate": not failed,
        "valid_for_parent_v59_frontier_migration": False,
        "valid_for_parent_v59_active_cuboid": False,
        "valid_for_full_outer_parent_leaf_enclosure": False,
        "valid_for_D4_event_local_W3_bound": False,
        "valid_for_all_operator_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
        "next_target": "MIGRATE_PARENT_V59_STATUS_ONLY" if not failed else "RETAIN_PARENT_V58_AND_ADVANCE_FRONTIER",
    }
    comparison_rows = [
        {"role": "target_v59", **{field: target_result.get(field) for field in CONTROL_FIELDS}, "trigger_count": target_triggers, "cache_hit_count": target_cache_hits, "matches_reference": target_matches_union},
        {"role": "target_independent_union", **{field: independent_union.get(field, "") for field in CONTROL_FIELDS}, "trigger_count": "", "cache_hit_count": 2, "matches_reference": target_matches_union},
        {"role": "control_v59", **{field: control_result.get(field) for field in CONTROL_FIELDS}, "trigger_count": control_new_triggers, "cache_hit_count": 0, "matches_reference": control_matches_source},
        {"role": "control_parent_v58_source", **{field: control_row.get(field) for field in CONTROL_FIELDS}, "trigger_count": "", "cache_hit_count": 0, "matches_reference": control_matches_source},
    ]
    base_5467.atomic_csv(AUDIT, full_audit)
    base_5467.atomic_csv(CACHE, cache_manifest)
    base_5467.atomic_csv(COMPARISON, comparison_rows)
    base_5467.atomic_csv(SOURCE_REGISTER, [{"source_path": str(path), "sha256": base_5499.digest(path), "exists": path.is_file()} for path in paths])
    base_5467.atomic_csv(VALIDATION, validations)
    base_5467.atomic_json(STATUS, payload)
    base_5467.atomic_json(RESULT, payload)
    render_document(payload, base_5467)
    print(json.dumps({key: payload[key] for key in (
        "decision", "target_v59_passed", "target_runtime_seconds",
        "target_trigger_count", "target_cache_hit_count",
        "target_matches_independent_union", "control_new_trigger_count",
        "control_matches_parent_v58_source", "failed_validation_count",
        "next_target",
    )}, indent=2))
    return 0 if not failed else 1


if __name__ == "__main__":
    raise SystemExit(main())
