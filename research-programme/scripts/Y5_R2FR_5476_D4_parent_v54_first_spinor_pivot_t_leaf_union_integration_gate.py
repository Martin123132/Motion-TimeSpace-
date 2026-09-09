from __future__ import annotations

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
OUTPUT = FUNCTIONAL_RG / "5476"

SCRIPT_5467 = SCRIPTS / "Y5_R2FR_5467_D4_all_outer_leaf_epsilon_fiber_transplant_runner.py"
SCRIPT_5468 = SCRIPTS / "Y5_R2FR_5468_D4_exact_outer_cuboid_coalescence_runner.py"
SCRIPT_5469 = SCRIPTS / "Y5_R2FR_5469_D4_resumable_three_axis_cuboid_certificate_runner.py"
SCRIPT_5472 = SCRIPTS / "Y5_R2FR_5472_D4_parent_v52_collision_jacobian_leaf_union_integration_gate.py"
SCRIPT_5474 = SCRIPTS / "Y5_R2FR_5474_D4_parent_v53_stable_edge_t_leaf_union_integration_gate.py"
SCRIPT_5475 = SCRIPTS / "Y5_R2FR_5475_D4_parent_v53_hash_locked_frontier_runner.py"
RESULT_5474 = FUNCTIONAL_RG / "5474" / "D4_parent_v53_stable_edge_t_leaf_union_result.json"
VALIDATION_5474 = FUNCTIONAL_RG / "5474" / "P8_Y5_BRR5473_5474_VALIDATION.csv"
RESULT_5475 = FUNCTIONAL_RG / "5475" / "D4_parent_v53_hash_locked_frontier_result.json"
VALIDATION_5475 = FUNCTIONAL_RG / "5475" / "P8_Y5_BRR5474_5475_VALIDATION.csv"
MANIFEST_5468 = FUNCTIONAL_RG / "5468" / "D4_exact_outer_cuboid_manifest.csv"

TARGET_CUBOID_ID = "E07__U051__RIGHT_CONNECTOR__CUBOID__6df3d70a73e4618b"
STATE_5475 = FUNCTIONAL_RG / "5475" / "work-v1" / f"{TARGET_CUBOID_ID}.json"

AUDIT_ROWS = OUTPUT / "D4_parent_v54_first_spinor_pivot_t_leaf_union_audit.csv"
COMPARISON = OUTPUT / "D4_parent_v54_target_and_control_comparison.csv"
SOURCE_REGISTER = OUTPUT / "source_register.csv"
VALIDATION = OUTPUT / "P8_Y5_BRR5475_5476_VALIDATION.csv"
STATUS = OUTPUT / "status.json"
RESULT = OUTPUT / "D4_parent_v54_first_spinor_pivot_t_leaf_union_result.json"
DOCUMENT = POST / "5476-Y5-R2FR-D4-parent-v54-first-spinor-pivot-t-leaf-union-integration-gate.md"

CHECKPOINT = 5476
REVISION = "D4-parent-v54-first-spinor-pivot-t-leaf-union-integration-gate-v1"
PARENT_V53_REVISION = "D4-deformed-contour-regular-away-W3-v53-stable-edge-t-leaf-union"
PARENT_V54_REVISION = "D4-deformed-contour-regular-away-W3-v54-first-spinor-pivot-t-leaf-union"
EXPECTED_FAILURE_MARKER = (
    "no displaced first-spinor rational pivot survives: away_arc_left_first"
)
T_LEAF_SCHEDULE = (4, 8, 16, 32)
METRIC_FIELDS = (
    "integrated_regular_path_abs_upper",
    "minimum_amplitude_denominator_abs_lower",
    "relative_root_abs_lower",
    "selected_global_root_abs_lower",
    "collision_jacobian_abs_lower",
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


def source_paths() -> tuple[Path, ...]:
    return (
        Path(__file__).resolve(),
        SCRIPT_5467,
        SCRIPT_5468,
        SCRIPT_5469,
        SCRIPT_5472,
        SCRIPT_5474,
        SCRIPT_5475,
        RESULT_5474,
        VALIDATION_5474,
        RESULT_5475,
        VALIDATION_5475,
        MANIFEST_5468,
        STATE_5475,
    )


def aggregate_leaf_results(
    base_5474: Any,
    rows: list[dict[str, Any]],
    x_lower: float,
    x_upper: float,
    t_lower: float,
    t_upper: float,
    refinement_depth: int,
    refinement_path: str,
    pivot_lower: float,
    coverage_error: float,
) -> dict[str, Any]:
    result = dict(rows[0])
    branch_ids = sorted(
        {
            branch
            for row in rows
            for branch in str(row.get("active_material_branch_ids", "")).split("|")
            if branch
        }
    )
    result.update(
        {
            "selected_role": "EXACT_T_LEAF_UNION",
            "x_lower": x_lower,
            "x_upper": x_upper,
            "x_width": x_upper - x_lower,
            "t_lower": t_lower,
            "t_upper": t_upper,
            "t_width": t_upper - t_lower,
            "parameter_area": (x_upper - x_lower) * (t_upper - t_lower),
            "refinement_depth": refinement_depth,
            "refinement_path": refinement_path,
            "path_speed_abs_upper": max(
                float(row["path_speed_abs_upper"]) for row in rows
            ),
            "active_material_branch_ids": "|".join(branch_ids),
            "active_material_branch_count": len(branch_ids),
            "integrated_regular_path_abs_upper": sum(
                float(row["integrated_regular_path_abs_upper"]) for row in rows
            ),
            "path_integral_enclosure_method": (
                "V54_EXACT_UNIFORM_T_LEAF_UNION_SUM"
            ),
            "collision_jacobian_enclosure_method": "|".join(
                sorted(
                    {
                        str(row.get("collision_jacobian_enclosure_method", ""))
                        for row in rows
                    }
                )
            ),
            "v54_first_spinor_pivot_t_leaf_count": len(rows),
            "v54_projective_denominator_abs_lower": pivot_lower,
            "v54_parameter_area_coverage_error": coverage_error,
        }
    )
    for field in base_5474.LOWER_FIELDS:
        values = base_5474.finite_values(rows, field)
        if values:
            result[field] = min(values)
    for field in base_5474.UPPER_FIELDS:
        values = base_5474.finite_values(rows, field)
        if values:
            result[field] = max(values)
    return result


def install_parent_v54(parent: Any, base_5474: Any) -> Any:
    if parent.REVISION != PARENT_V53_REVISION:
        raise RuntimeError(
            f"expected parent revision {PARENT_V53_REVISION}, found {parent.REVISION}"
        )
    original = parent.evaluate_path_box
    audit_rows: list[dict[str, Any]] = []

    def audit(
        row_type: str,
        status: str,
        t_count: int,
        t_index: int,
        t_lower: float,
        t_upper: float,
        denominator_lower: float = math.nan,
        jacobian_lower: float = math.nan,
        integrated_upper: float = math.nan,
        coverage_error: float = math.nan,
        runtime_seconds: float = 0.0,
        error_type: str = "",
        error: str = "",
    ) -> None:
        audit_rows.append(
            {
                "row_type": row_type,
                "status": status,
                "t_count": t_count,
                "t_index": t_index,
                "t_lower": t_lower,
                "t_upper": t_upper,
                "projective_denominator_abs_lower": denominator_lower,
                "collision_jacobian_abs_lower": jacobian_lower,
                "integrated_regular_path_abs_upper": integrated_upper,
                "parameter_area_coverage_error": coverage_error,
                "runtime_seconds": runtime_seconds,
                "error_type": error_type,
                "error": error,
                "leaf_union_theorem": (
                    "D=union_i D_i; every complete parent-v53 amplitude leaf is "
                    "finite; sum integrated uppers and minimize denominator lowers"
                ),
            }
        )

    def evaluate_v54(
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
        trigger_error: Exception | None = None
        arguments = (
            cell,
            term_id,
            configurations,
            epsilon_row,
            path_segment,
            x_lower,
            x_upper,
            t_lower,
            t_upper,
            refinement_depth,
            refinement_path,
            support_segments,
            branches,
            global_arc_count,
            reduce_selector_charts,
        )
        try:
            return original(*arguments)
        except parent.M5258.IntervalSingularity as error:
            if (
                path_segment not in {"LEFT_CONNECTOR", "RIGHT_CONNECTOR"}
                or EXPECTED_FAILURE_MARKER not in str(error)
            ):
                raise
            trigger_error = error
        for t_count in T_LEAF_SCHEDULE:
            started = time.perf_counter()
            edges = base_5474.exact_uniform_edges(t_lower, t_upper, t_count)
            leaves: list[dict[str, Any]] = []
            expected_failure: Exception | None = None
            for index, (leaf_lower, leaf_upper) in enumerate(
                zip(edges, edges[1:])
            ):
                try:
                    leaf = original(
                        cell,
                        term_id,
                        configurations,
                        epsilon_row,
                        path_segment,
                        x_lower,
                        x_upper,
                        leaf_lower,
                        leaf_upper,
                        refinement_depth + 1,
                        f"{refinement_path}:V54T{t_count}:{index}",
                        support_segments,
                        branches,
                        global_arc_count,
                        reduce_selector_charts,
                    )
                except parent.M5258.IntervalSingularity as error:
                    if EXPECTED_FAILURE_MARKER not in str(error):
                        raise
                    expected_failure = error
                    audit(
                        "leaf",
                        "FAIL",
                        t_count,
                        index,
                        leaf_lower,
                        leaf_upper,
                        runtime_seconds=time.perf_counter() - started,
                        error_type=type(error).__name__,
                        error=str(error).splitlines()[0][:600],
                    )
                    break
                denominator_lower = float(
                    leaf["minimum_amplitude_denominator_abs_lower"]
                )
                if denominator_lower <= 0.0:
                    raise RuntimeError("v54 full-amplitude leaf has no denominator gap")
                leaves.append(leaf)
                audit(
                    "leaf",
                    "PASS",
                    t_count,
                    index,
                    leaf_lower,
                    leaf_upper,
                    denominator_lower,
                    float(leaf["collision_jacobian_abs_lower"]),
                    float(leaf["integrated_regular_path_abs_upper"]),
                    runtime_seconds=time.perf_counter() - started,
                )
            if expected_failure is not None:
                audit(
                    "schedule",
                    "FAIL",
                    t_count,
                    -1,
                    t_lower,
                    t_upper,
                    runtime_seconds=time.perf_counter() - started,
                    error_type=type(expected_failure).__name__,
                    error=str(expected_failure).splitlines()[0][:600],
                )
                continue
            covered_area = sum(float(row["parameter_area"]) for row in leaves)
            original_area = (x_upper - x_lower) * (t_upper - t_lower)
            coverage_error = abs(covered_area - original_area)
            if coverage_error > 1.0e-12 * max(original_area, 1.0):
                raise RuntimeError("v54 exact t cover does not preserve parameter area")
            pivot_lower = min(
                float(row["minimum_amplitude_denominator_abs_lower"])
                for row in leaves
            )
            result = aggregate_leaf_results(
                base_5474,
                leaves,
                x_lower,
                x_upper,
                t_lower,
                t_upper,
                refinement_depth,
                refinement_path,
                pivot_lower,
                coverage_error,
            )
            audit(
                "schedule",
                "SELECTED",
                t_count,
                -1,
                t_lower,
                t_upper,
                pivot_lower,
                float(result["collision_jacobian_abs_lower"]),
                float(result["integrated_regular_path_abs_upper"]),
                coverage_error,
                time.perf_counter() - started,
            )
            return result
        if trigger_error is None:
            raise RuntimeError("v54 fallback lost its triggering pivot error")
        raise trigger_error

    parent.evaluate_path_box = evaluate_v54
    parent.V54_FIRST_SPINOR_PIVOT_T_LEAF_UNION_AUDIT_ROWS = audit_rows
    parent.V54_PARENT_ACTION_CHANGED = False
    parent.V54_ONLY_ENCLOSURE_COMPOSITION_CHANGED = True
    parent.REVISION = PARENT_V54_REVISION
    return parent


def check(gate: str, passed: bool, evidence: Any) -> dict[str, Any]:
    return {
        "checkpoint": CHECKPOINT,
        "validation_gate": gate,
        "passed": bool(passed),
        "evidence": evidence,
    }


def node_volume(row: dict[str, Any]) -> float:
    return (
        (float(row["epsilon_real_upper"]) - float(row["epsilon_real_lower"]))
        * (float(row["x_upper"]) - float(row["x_lower"]))
        * (float(row["t_upper"]) - float(row["t_lower"]))
    )


def render_document(payload: dict[str, Any], base_5467: Any) -> None:
    lines = [
        "# 5476: D4 parent-v54 first-spinor-pivot t-leaf-union integration gate",
        "",
        "## Derived enclosure law",
        "",
        "The v53 frontier exposed a distinct upstream projective-chart obstruction: no displaced left-first rational pivot survived on one coarse connector box. Parent v54 changes no action or amplitude formula. It invokes an exact path-parameter cover only after that precise error, evaluates the complete parent-v53 amplitude on every leaf, sums integrated upper bounds, and minimizes denominator lower bounds.",
        "",
        "## Result",
        "",
        f"The target reproduces the v53 pivot failure: `{payload['target_v53_expected_failure']}`. It passes v54: `{payload['target_v54_passed']}` using `{payload['selected_t_leaf_count']}` leaves.",
        "",
        f"Minimum projective/amplitude denominator lower: `{payload['target_v54_amplitude_denominator_abs_lower']}`. Collision-Jacobian lower: `{payload['target_v54_collision_jacobian_abs_lower']}`. Untriggered control unchanged: `{payload['control_v53_v54_identical']}`.",
        "",
        "## Decision",
        "",
        f"**{payload['decision']}**",
        "",
        "## Claim boundary",
        "",
        "This certifies one projective-chart enclosure class only; the active cuboid and all broader physics claims remain open.",
        "",
    ]
    base_5467.atomic_text(DOCUMENT, "\n".join(lines))


def main() -> int:
    base_5467 = load_module("mts_5467_for_5476", SCRIPT_5467)
    base_5468 = load_module("mts_5468_for_5476", SCRIPT_5468)
    base_5469 = load_module("mts_5469_for_5476", SCRIPT_5469)
    base_5472 = load_module("mts_5472_for_5476", SCRIPT_5472)
    base_5474 = load_module("mts_5474_for_5476", SCRIPT_5474)
    base_5467.set_below_normal_priority()
    before_formalization = base_5467.formalization_snapshot()
    missing = [str(path) for path in source_paths() if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"missing sources: {missing}")
    result_5474 = read_json(RESULT_5474)
    validation_5474 = read_csv(VALIDATION_5474)
    result_5475 = read_json(RESULT_5475)
    validation_5475 = read_csv(VALIDATION_5475)
    state = read_json(STATE_5475)
    state_sha256 = digest(STATE_5475)
    cuboid = next(
        row
        for row in read_csv(MANIFEST_5468)
        if row["cuboid_job_id"] == TARGET_CUBOID_ID
    )
    target_candidates = [
        row
        for row in state["refinement_witnesses"]
        if row.get("parent_revision") == PARENT_V53_REVISION
        and EXPECTED_FAILURE_MARKER in str(row.get("failure_message", ""))
    ]
    if not target_candidates:
        raise RuntimeError("checkpoint 5475 has no v53 first-spinor pivot witness")
    target_node = max(target_candidates, key=node_volume)
    control_node = next(
        row
        for row in state["accepted"]
        if row.get("parent_revision") != PARENT_V53_REVISION
    )

    stable, _, cells, support_segments, branches = base_5467.load_parent()

    def fresh_v53(name: str) -> Any:
        return base_5474.install_parent_v53(
            base_5472.install_parent_v52(
                base_5472.fresh_parent(base_5467, name)
            )
        )

    parent_v53_target = fresh_v53("mts_parent_v53_target_for_5476")
    target_v53 = base_5469.evaluate_node(
        base_5468,
        stable,
        parent_v53_target,
        cells,
        support_segments,
        branches,
        cuboid,
        target_node,
    )
    parent_v54_target = install_parent_v54(
        fresh_v53("mts_parent_v54_target_for_5476"), base_5474
    )
    target_v54 = base_5469.evaluate_node(
        base_5468,
        stable,
        parent_v54_target,
        cells,
        support_segments,
        branches,
        cuboid,
        target_node,
    )
    target_audit = list(
        parent_v54_target.V54_FIRST_SPINOR_PIVOT_T_LEAF_UNION_AUDIT_ROWS
    )
    parent_v53_control = fresh_v53("mts_parent_v53_control_for_5476")
    parent_v54_control = install_parent_v54(
        fresh_v53("mts_parent_v54_control_for_5476"), base_5474
    )
    control_v53 = base_5469.evaluate_node(
        base_5468,
        stable,
        parent_v53_control,
        cells,
        support_segments,
        branches,
        cuboid,
        control_node,
    )
    control_v54 = base_5469.evaluate_node(
        base_5468,
        stable,
        parent_v54_control,
        cells,
        support_segments,
        branches,
        cuboid,
        control_node,
    )
    control_identical = (
        truth(control_v53.get("probe_passed"))
        and truth(control_v54.get("probe_passed"))
        and all(
            float(control_v53[field]) == float(control_v54[field])
            for field in METRIC_FIELDS
        )
        and not parent_v54_control.V54_FIRST_SPINOR_PIVOT_T_LEAF_UNION_AUDIT_ROWS
    )

    selected_schedule = next(
        (row for row in target_audit if row["status"] == "SELECTED"), None
    )
    selected_count = int(selected_schedule["t_count"]) if selected_schedule else 0
    selected_leaves = [
        row
        for row in target_audit
        if row["row_type"] == "leaf"
        and row["status"] == "PASS"
        and int(row["t_count"]) == selected_count
    ]
    target_v53_expected_failure = (
        not truth(target_v53.get("probe_passed"))
        and EXPECTED_FAILURE_MARKER in str(target_v53.get("failure_message", ""))
    )
    target_v54_passed = truth(target_v54.get("probe_passed"))
    exact_cover = (
        selected_schedule is not None
        and selected_count >= 2
        and len(selected_leaves) == selected_count
        and float(selected_schedule["parameter_area_coverage_error"]) <= 1.0e-12
    )

    comparison_rows = []
    for role, result, revision in (
        ("first_spinor_pivot_target_v53", target_v53, PARENT_V53_REVISION),
        ("first_spinor_pivot_target_v54", target_v54, PARENT_V54_REVISION),
        ("untriggered_control_v53", control_v53, PARENT_V53_REVISION),
        ("untriggered_control_v54", control_v54, PARENT_V54_REVISION),
    ):
        comparison_rows.append(
            {
                "role": role,
                "probe_passed": truth(result.get("probe_passed")),
                "failure_type": result.get("failure_type", ""),
                "failure_message": result.get("failure_message", ""),
                **{field: result.get(field) for field in METRIC_FIELDS},
                "parent_revision": revision,
            }
        )
    base_5467.atomic_csv(AUDIT_ROWS, target_audit)
    base_5467.atomic_csv(COMPARISON, comparison_rows)

    payload: dict[str, Any] = {
        "checkpoint": CHECKPOINT,
        "revision": REVISION,
        "parent_revision": PARENT_V54_REVISION,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "decision": (
            "PARENT_V54_FIRST_SPINOR_PIVOT_T_LEAF_UNION_CERTIFIED__MIGRATE_FRONTIER"
            if target_v53_expected_failure
            and target_v54_passed
            and exact_cover
            and control_identical
            else "PARENT_V54_FIRST_SPINOR_PIVOT_T_LEAF_UNION_NOT_CERTIFIED"
        ),
        "target_cuboid_id": TARGET_CUBOID_ID,
        "target_refinement_path": target_node["refinement_path"],
        "target_v53_expected_failure": target_v53_expected_failure,
        "target_v54_passed": target_v54_passed,
        "selected_t_leaf_count": selected_count,
        "selected_leaf_count": len(selected_leaves),
        "target_v54_amplitude_denominator_abs_lower": target_v54.get(
            "minimum_amplitude_denominator_abs_lower"
        ),
        "target_v54_collision_jacobian_abs_lower": target_v54.get(
            "collision_jacobian_abs_lower"
        ),
        "target_v54_integrated_regular_path_abs_upper": target_v54.get(
            "integrated_regular_path_abs_upper"
        ),
        "parameter_area_coverage_error": (
            float(selected_schedule["parameter_area_coverage_error"])
            if selected_schedule
            else math.nan
        ),
        "control_v53_v54_identical": control_identical,
        "v54_audit_row_count": len(target_audit),
        "source_state_5475_sha256": state_sha256,
        "parent_action_changed": False,
        "only_enclosure_composition_changed": True,
        "valid_for_parent_v54_first_spinor_pivot_t_leaf_union": False,
        "valid_for_parent_v54_active_cuboid": False,
        "valid_for_full_outer_parent_leaf_enclosure": False,
        "valid_for_D4_event_local_W3_bound": False,
        "valid_for_all_operator_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
        "next_target": "CREATE_HASH_LOCKED_V54_CARRY_FORWARD_OF_CHECKPOINT_5475_STATE",
    }
    after_formalization = base_5467.formalization_snapshot()
    validations = [
        check("all_sources_exist", not missing, len(source_paths())),
        check(
            "checkpoint_5474_parent_v53_is_certified",
            truth(result_5474.get("valid_for_parent_v53_stable_edge_t_leaf_union"))
            and int(result_5474.get("failed_validation_count", -1)) == 0
            and all(truth(row["passed"]) for row in validation_5474),
            result_5474.get("decision"),
        ),
        check(
            "checkpoint_5475_frontier_is_clean",
            int(result_5475.get("failed_validation_count", -1)) == 0
            and all(truth(row["passed"]) for row in validation_5475)
            and not state["unresolved"],
            state_sha256,
        ),
        check(
            "v53_target_reproduces_precise_first_spinor_pivot_failure",
            target_v53_expected_failure,
            target_v53.get("failure_message", ""),
        ),
        check(
            "v54_target_full_amplitude_is_finite",
            target_v54_passed
            and all(
                math.isfinite(float(target_v54[field]))
                and float(target_v54[field]) > 0.0
                for field in METRIC_FIELDS
            ),
            target_v54.get("minimum_amplitude_denominator_abs_lower"),
        ),
        check(
            "selected_t_leaf_union_is_an_exact_cover",
            exact_cover,
            payload["parameter_area_coverage_error"],
        ),
        check(
            "every_selected_leaf_has_positive_full_amplitude_factors",
            bool(selected_leaves)
            and all(
                float(row["projective_denominator_abs_lower"]) > 0.0
                and float(row["collision_jacobian_abs_lower"]) > 0.0
                for row in selected_leaves
            ),
            len(selected_leaves),
        ),
        check(
            "untriggered_v53_v54_control_is_exactly_unchanged",
            control_identical,
            control_node["refinement_path"],
        ),
        check(
            "v54_changes_only_enclosure_composition",
            not parent_v54_target.V54_PARENT_ACTION_CHANGED
            and parent_v54_target.V54_ONLY_ENCLOSURE_COMPOSITION_CHANGED
            and not parent_v54_target.V53_PARENT_ACTION_CHANGED
            and parent_v54_target.V53_ONLY_ENCLOSURE_COMPOSITION_CHANGED,
            PARENT_V54_REVISION,
        ),
        check(
            "formalization_workbench_untouched",
            before_formalization == after_formalization,
            f"before={len(before_formalization)};after={len(after_formalization)}",
        ),
        check(
            "broad_claims_remain_false",
            not payload["valid_for_parent_v54_active_cuboid"]
            and not payload["valid_for_full_outer_parent_leaf_enclosure"]
            and not payload["valid_for_D4_event_local_W3_bound"]
            and not payload["valid_for_all_operator_local_GR_claim"]
            and not payload["valid_for_full_MTS_claim"],
            "one parent enclosure class only",
        ),
    ]
    payload["validation_row_count"] = len(validations)
    payload["failed_validation_count"] = sum(
        not row["passed"] for row in validations
    )
    payload["valid_for_parent_v54_first_spinor_pivot_t_leaf_union"] = (
        payload["failed_validation_count"] == 0
        and "CERTIFIED" in payload["decision"]
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
    print(
        json.dumps(
            {
                key: payload[key]
                for key in (
                    "decision",
                    "target_v53_expected_failure",
                    "target_v54_passed",
                    "selected_t_leaf_count",
                    "target_v54_amplitude_denominator_abs_lower",
                    "target_v54_collision_jacobian_abs_lower",
                    "control_v53_v54_identical",
                    "valid_for_parent_v54_first_spinor_pivot_t_leaf_union",
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
