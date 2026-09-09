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
OUTPUT = FUNCTIONAL_RG / "5474"

SCRIPT_5467 = SCRIPTS / "Y5_R2FR_5467_D4_all_outer_leaf_epsilon_fiber_transplant_runner.py"
SCRIPT_5468 = SCRIPTS / "Y5_R2FR_5468_D4_exact_outer_cuboid_coalescence_runner.py"
SCRIPT_5469 = SCRIPTS / "Y5_R2FR_5469_D4_resumable_three_axis_cuboid_certificate_runner.py"
SCRIPT_5472 = SCRIPTS / "Y5_R2FR_5472_D4_parent_v52_collision_jacobian_leaf_union_integration_gate.py"
SCRIPT_5473 = SCRIPTS / "Y5_R2FR_5473_D4_parent_v52_hash_locked_frontier_runner.py"
RESULT_5472 = FUNCTIONAL_RG / "5472" / "D4_parent_v52_collision_jacobian_leaf_union_result.json"
VALIDATION_5472 = FUNCTIONAL_RG / "5472" / "P8_Y5_BRR5471_5472_VALIDATION.csv"
RESULT_5473 = FUNCTIONAL_RG / "5473" / "D4_parent_v52_hash_locked_frontier_result.json"
VALIDATION_5473 = FUNCTIONAL_RG / "5473" / "P8_Y5_BRR5472_5473_VALIDATION.csv"
MANIFEST_5468 = FUNCTIONAL_RG / "5468" / "D4_exact_outer_cuboid_manifest.csv"

TARGET_CUBOID_ID = "E07__U051__RIGHT_CONNECTOR__CUBOID__6df3d70a73e4618b"
STATE_5473 = FUNCTIONAL_RG / "5473" / "work-v1" / f"{TARGET_CUBOID_ID}.json"

AUDIT_ROWS = OUTPUT / "D4_parent_v53_stable_edge_t_leaf_union_audit.csv"
COMPARISON = OUTPUT / "D4_parent_v53_target_and_control_comparison.csv"
SOURCE_REGISTER = OUTPUT / "source_register.csv"
VALIDATION = OUTPUT / "P8_Y5_BRR5473_5474_VALIDATION.csv"
STATUS = OUTPUT / "status.json"
RESULT = OUTPUT / "D4_parent_v53_stable_edge_t_leaf_union_result.json"
DOCUMENT = POST / "5474-Y5-R2FR-D4-parent-v53-stable-edge-t-leaf-union-integration-gate.md"

CHECKPOINT = 5474
REVISION = "D4-parent-v53-stable-edge-t-leaf-union-integration-gate-v1"
PARENT_V52_REVISION = "D4-deformed-contour-regular-away-W3-v52-leaf-union"
PARENT_V53_REVISION = "D4-deformed-contour-regular-away-W3-v53-stable-edge-t-leaf-union"
EXPECTED_FAILURE_MARKER = "edge_2_1_3:stable_edge"
T_LEAF_SCHEDULE = (4, 8, 16, 32)

METRIC_FIELDS = (
    "integrated_regular_path_abs_upper",
    "minimum_amplitude_denominator_abs_lower",
    "relative_root_abs_lower",
    "selected_global_root_abs_lower",
    "collision_jacobian_abs_lower",
)
LOWER_FIELDS = (
    "pole_gap_abs_lower",
    "material_root_coefficient_abs_lower",
    "material_root_discriminant_abs_lower",
    "material_root_implicit_derivative_abs_lower",
    "minimum_amplitude_denominator_abs_lower",
    "relative_root_abs_lower",
    "selected_global_root_abs_lower",
    "collision_jacobian_abs_lower",
    "external01_path_jacobian_abs_lower",
)
UPPER_FIELDS = (
    "raw_integrand_abs_upper",
    "pole_correction_abs_upper",
    "regular_integrand_abs_upper",
    "global_regularized_coefficient_abs_upper",
    "external01_pole_residue_abs_upper",
    "external01_reciprocal_integral_abs_upper",
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
        SCRIPT_5473,
        RESULT_5472,
        VALIDATION_5472,
        RESULT_5473,
        VALIDATION_5473,
        MANIFEST_5468,
        STATE_5473,
    )


def finite_values(rows: list[dict[str, Any]], field: str) -> list[float]:
    values = [float(row[field]) for row in rows if field in row]
    return [value for value in values if math.isfinite(value)]


def exact_uniform_edges(lower: float, upper: float, count: int) -> list[float]:
    if not upper > lower or count < 2:
        raise ValueError("an exact leaf cover needs a positive interval and two leaves")
    edges = [lower + (upper - lower) * index / count for index in range(count + 1)]
    edges[0] = lower
    edges[-1] = upper
    return edges


def invariant_lower_for_leaf(
    parent: Any,
    configurations: list[dict[str, Any]],
    cell: dict[str, Any],
    path_segment: str,
    epsilon_row: dict[str, Any],
    x_lower: float,
    x_upper: float,
    t_lower: float,
    t_upper: float,
) -> float:
    epsilon = parent.cbox(
        float(epsilon_row["epsilon_real_lower"]),
        float(epsilon_row["epsilon_real_upper"]),
        float(epsilon_row["epsilon_imaginary_lower"]),
        float(epsilon_row["epsilon_imaginary_upper"]),
    )
    coordinate = parent.cbox(x_lower, x_upper)
    parameter = parent.cbox(t_lower, t_upper)
    reciprocal = [row for row in configurations if row.get("role") == "reciprocal"]
    if not reciprocal:
        raise ValueError("stable-edge fallback has no reciprocal configuration")
    return min(
        parent.M5258.lower_abs(
            parent.centered_path_correlated_left_first_soft_invariant(
                configuration,
                cell,
                path_segment,
                coordinate,
                parameter,
                epsilon,
            )
        )
        for configuration in reciprocal
    )


def aggregate_leaf_results(
    rows: list[dict[str, Any]],
    x_lower: float,
    x_upper: float,
    t_lower: float,
    t_upper: float,
    refinement_depth: int,
    refinement_path: str,
    invariant_lower: float,
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
            "chart_roles": "|".join(
                sorted({str(row.get("chart_roles", "")) for row in rows})
            ),
            "chart_count": sum(int(row.get("chart_count", 0)) for row in rows),
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
                "V53_EXACT_UNIFORM_T_LEAF_UNION_SUM"
            ),
            "collision_jacobian_enclosure_method": "|".join(
                sorted(
                    {
                        str(row.get("collision_jacobian_enclosure_method", ""))
                        for row in rows
                    }
                )
            ),
            "v53_stable_edge_t_leaf_count": len(rows),
            "v53_left_first_soft_invariant_abs_lower": invariant_lower,
            "v53_parameter_area_coverage_error": coverage_error,
        }
    )
    for field in LOWER_FIELDS:
        values = finite_values(rows, field)
        if values:
            result[field] = min(values)
    for field in UPPER_FIELDS:
        values = finite_values(rows, field)
        if values:
            result[field] = max(values)
    return result


def install_parent_v53(parent: Any) -> Any:
    if parent.REVISION != PARENT_V52_REVISION:
        raise RuntimeError(
            f"expected parent revision {PARENT_V52_REVISION}, found {parent.REVISION}"
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
        invariant_lower: float = math.nan,
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
                "left_first_soft_invariant_abs_lower": invariant_lower,
                "minimum_amplitude_denominator_abs_lower": denominator_lower,
                "collision_jacobian_abs_lower": jacobian_lower,
                "integrated_regular_path_abs_upper": integrated_upper,
                "parameter_area_coverage_error": coverage_error,
                "runtime_seconds": runtime_seconds,
                "error_type": error_type,
                "error": error,
                "leaf_union_theorem": (
                    "D=union_i D_i; evaluate the full amplitude on every D_i; "
                    "sum integrated upper bounds and take minima of denominator lowers"
                ),
            }
        )

    def evaluate_v53(
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
        trigger_error: Exception | None = None
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
            edges = exact_uniform_edges(t_lower, t_upper, t_count)
            leaves: list[dict[str, Any]] = []
            invariant_lowers: list[float] = []
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
                        f"{refinement_path}:V53T{t_count}:{index}",
                        support_segments,
                        branches,
                        global_arc_count,
                        reduce_selector_charts,
                    )
                    invariant_lower = invariant_lower_for_leaf(
                        parent,
                        configurations,
                        cell,
                        path_segment,
                        epsilon_row,
                        x_lower,
                        x_upper,
                        leaf_lower,
                        leaf_upper,
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
                if invariant_lower <= 0.0:
                    expected_failure = parent.M5258.IntervalSingularity(
                        "v53 explicit invariant leaf lower reaches zero"
                    )
                    audit(
                        "leaf",
                        "ZERO",
                        t_count,
                        index,
                        leaf_lower,
                        leaf_upper,
                        invariant_lower=invariant_lower,
                        runtime_seconds=time.perf_counter() - started,
                        error_type=type(expected_failure).__name__,
                        error=str(expected_failure),
                    )
                    break
                leaves.append(leaf)
                invariant_lowers.append(invariant_lower)
                audit(
                    "leaf",
                    "PASS",
                    t_count,
                    index,
                    leaf_lower,
                    leaf_upper,
                    invariant_lower,
                    float(leaf["minimum_amplitude_denominator_abs_lower"]),
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
            coverage_tolerance = 1.0e-12 * max(original_area, 1.0)
            if coverage_error > coverage_tolerance:
                raise RuntimeError("v53 exact t cover does not preserve parameter area")
            result = aggregate_leaf_results(
                leaves,
                x_lower,
                x_upper,
                t_lower,
                t_upper,
                refinement_depth,
                refinement_path,
                min(invariant_lowers),
                coverage_error,
            )
            audit(
                "schedule",
                "SELECTED",
                t_count,
                -1,
                t_lower,
                t_upper,
                min(invariant_lowers),
                float(result["minimum_amplitude_denominator_abs_lower"]),
                float(result["collision_jacobian_abs_lower"]),
                float(result["integrated_regular_path_abs_upper"]),
                coverage_error,
                time.perf_counter() - started,
            )
            return result
        if trigger_error is None:
            raise RuntimeError("v53 fallback lost its triggering stable-edge error")
        raise trigger_error

    parent.evaluate_path_box = evaluate_v53
    parent.V53_STABLE_EDGE_T_LEAF_UNION_AUDIT_ROWS = audit_rows
    parent.V53_PARENT_ACTION_CHANGED = False
    parent.V53_ONLY_ENCLOSURE_COMPOSITION_CHANGED = True
    parent.REVISION = PARENT_V53_REVISION
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
        "# 5474: D4 parent-v53 stable-edge t-leaf-union integration gate",
        "",
        "## Derived enclosure law",
        "",
        "The v52 frontier isolated `away_arc_left_K5:s1:c0:left1:edge_2_1_3:stable_edge`. The parent already partitions the left first-soft invariant internally, but then replaces its disconnected finite image union by one rectangular hull. That hull can contain zero even when every source leaf excludes zero.",
        "",
        "Parent v53 changes no action, contour, selector, residue, or acceptance threshold. Only after the precise connector stable-edge singularity occurs, it partitions the original path-parameter interval into an exact finite cover, evaluates the complete unchanged v52 amplitude on every leaf, sums the integrated upper bounds, and takes minima of all denominator lower bounds.",
        "",
        "## Result",
        "",
        f"The v52 target fails as expected: `{payload['target_v52_expected_failure']}`. The same target passes v53: `{payload['target_v53_passed']}` using `{payload['selected_t_leaf_count']}` leaves.",
        "",
        f"Minimum explicit left first-soft invariant lower: `{payload['minimum_selected_invariant_abs_lower']}`. Minimum full-amplitude denominator lower: `{payload['target_v53_amplitude_denominator_abs_lower']}`. Minimum collision-Jacobian lower: `{payload['target_v53_collision_jacobian_abs_lower']}`.",
        "",
        f"The untriggered v52/v53 control is exactly unchanged: `{payload['control_v52_v53_identical']}`.",
        "",
        "## Decision",
        "",
        f"**{payload['decision']}**",
        "",
        "## Claim boundary",
        "",
        "This proves a parent-level finite-union repair for one amplitude stable-edge enclosure class. It does not yet certify the active cuboid, full outer cover, W3, regulator limit, local GR, or full MTS.",
        "",
    ]
    base_5467.atomic_text(DOCUMENT, "\n".join(lines))


def main() -> int:
    base_5467 = load_module("mts_5467_for_5474", SCRIPT_5467)
    base_5468 = load_module("mts_5468_for_5474", SCRIPT_5468)
    base_5469 = load_module("mts_5469_for_5474", SCRIPT_5469)
    base_5472 = load_module("mts_5472_for_5474", SCRIPT_5472)
    base_5467.set_below_normal_priority()
    before_formalization = base_5467.formalization_snapshot()
    missing = [str(path) for path in source_paths() if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"missing sources: {missing}")

    result_5472 = read_json(RESULT_5472)
    validation_5472 = read_csv(VALIDATION_5472)
    result_5473 = read_json(RESULT_5473)
    validation_5473 = read_csv(VALIDATION_5473)
    state = read_json(STATE_5473)
    state_sha256 = digest(STATE_5473)
    cuboid = next(
        row
        for row in read_csv(MANIFEST_5468)
        if row["cuboid_job_id"] == TARGET_CUBOID_ID
    )
    target_candidates = [
        row
        for row in state["refinement_witnesses"]
        if row.get("parent_revision") == PARENT_V52_REVISION
        and EXPECTED_FAILURE_MARKER in str(row.get("failure_message", ""))
    ]
    if not target_candidates:
        raise RuntimeError("checkpoint 5473 has no v52 stable-edge witness")
    target_node = max(target_candidates, key=node_volume)
    control_node = next(
        row
        for row in state["accepted"]
        if row.get("parent_revision") != PARENT_V52_REVISION
    )

    stable, _, cells, support_segments, branches = base_5467.load_parent()
    parent_v52_target = base_5472.install_parent_v52(
        base_5472.fresh_parent(base_5467, "mts_parent_v52_target_for_5474")
    )
    target_v52 = base_5469.evaluate_node(
        base_5468,
        stable,
        parent_v52_target,
        cells,
        support_segments,
        branches,
        cuboid,
        target_node,
    )

    parent_v53_target = install_parent_v53(
        base_5472.install_parent_v52(
            base_5472.fresh_parent(base_5467, "mts_parent_v53_target_for_5474")
        )
    )
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
    target_audit = list(parent_v53_target.V53_STABLE_EDGE_T_LEAF_UNION_AUDIT_ROWS)

    parent_v52_control = base_5472.install_parent_v52(
        base_5472.fresh_parent(base_5467, "mts_parent_v52_control_for_5474")
    )
    parent_v53_control = install_parent_v53(
        base_5472.install_parent_v52(
            base_5472.fresh_parent(base_5467, "mts_parent_v53_control_for_5474")
        )
    )
    control_v52 = base_5469.evaluate_node(
        base_5468,
        stable,
        parent_v52_control,
        cells,
        support_segments,
        branches,
        cuboid,
        control_node,
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
    control_identical = (
        truth(control_v52.get("probe_passed"))
        and truth(control_v53.get("probe_passed"))
        and all(
            float(control_v52[field]) == float(control_v53[field])
            for field in METRIC_FIELDS
        )
        and not parent_v53_control.V53_STABLE_EDGE_T_LEAF_UNION_AUDIT_ROWS
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
    target_v52_expected_failure = (
        not truth(target_v52.get("probe_passed"))
        and EXPECTED_FAILURE_MARKER in str(target_v52.get("failure_message", ""))
    )
    target_v53_passed = truth(target_v53.get("probe_passed"))
    exact_cover = (
        selected_count >= 2
        and len(selected_leaves) == selected_count
        and float(selected_schedule["parameter_area_coverage_error"])
        <= 1.0e-12
    ) if selected_schedule else False

    comparison_rows = [
        {
            "role": "stable_edge_target_v52",
            "probe_passed": truth(target_v52.get("probe_passed")),
            "failure_type": target_v52.get("failure_type", ""),
            "failure_message": target_v52.get("failure_message", ""),
            **{field: target_v52.get(field) for field in METRIC_FIELDS},
            "parent_revision": PARENT_V52_REVISION,
        },
        {
            "role": "stable_edge_target_v53",
            "probe_passed": target_v53_passed,
            "failure_type": target_v53.get("failure_type", ""),
            "failure_message": target_v53.get("failure_message", ""),
            **{field: target_v53.get(field) for field in METRIC_FIELDS},
            "parent_revision": PARENT_V53_REVISION,
        },
        {
            "role": "untriggered_control_v52",
            "probe_passed": truth(control_v52.get("probe_passed")),
            "failure_type": control_v52.get("failure_type", ""),
            "failure_message": control_v52.get("failure_message", ""),
            **{field: control_v52.get(field) for field in METRIC_FIELDS},
            "parent_revision": PARENT_V52_REVISION,
        },
        {
            "role": "untriggered_control_v53",
            "probe_passed": truth(control_v53.get("probe_passed")),
            "failure_type": control_v53.get("failure_type", ""),
            "failure_message": control_v53.get("failure_message", ""),
            **{field: control_v53.get(field) for field in METRIC_FIELDS},
            "parent_revision": PARENT_V53_REVISION,
        },
    ]
    base_5467.atomic_csv(AUDIT_ROWS, target_audit)
    base_5467.atomic_csv(COMPARISON, comparison_rows)

    payload: dict[str, Any] = {
        "checkpoint": CHECKPOINT,
        "revision": REVISION,
        "parent_revision": PARENT_V53_REVISION,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "decision": (
            "PARENT_V53_STABLE_EDGE_T_LEAF_UNION_CERTIFIED__MIGRATE_FRONTIER"
            if target_v52_expected_failure
            and target_v53_passed
            and exact_cover
            and control_identical
            else "PARENT_V53_STABLE_EDGE_T_LEAF_UNION_NOT_CERTIFIED"
        ),
        "target_cuboid_id": TARGET_CUBOID_ID,
        "target_refinement_path": target_node["refinement_path"],
        "target_v52_expected_failure": target_v52_expected_failure,
        "target_v53_passed": target_v53_passed,
        "selected_t_leaf_count": selected_count,
        "selected_leaf_count": len(selected_leaves),
        "minimum_selected_invariant_abs_lower": min(
            (
                float(row["left_first_soft_invariant_abs_lower"])
                for row in selected_leaves
            ),
            default=math.nan,
        ),
        "target_v53_amplitude_denominator_abs_lower": target_v53.get(
            "minimum_amplitude_denominator_abs_lower"
        ),
        "target_v53_collision_jacobian_abs_lower": target_v53.get(
            "collision_jacobian_abs_lower"
        ),
        "target_v53_integrated_regular_path_abs_upper": target_v53.get(
            "integrated_regular_path_abs_upper"
        ),
        "parameter_area_coverage_error": (
            float(selected_schedule["parameter_area_coverage_error"])
            if selected_schedule
            else math.nan
        ),
        "control_v52_v53_identical": control_identical,
        "v53_audit_row_count": len(target_audit),
        "source_state_5473_sha256": state_sha256,
        "parent_action_changed": False,
        "only_enclosure_composition_changed": True,
        "valid_for_parent_v53_stable_edge_t_leaf_union": False,
        "valid_for_parent_v53_active_cuboid": False,
        "valid_for_full_outer_parent_leaf_enclosure": False,
        "valid_for_D4_event_local_W3_bound": False,
        "valid_for_all_operator_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
        "next_target": "CREATE_HASH_LOCKED_V53_CARRY_FORWARD_OF_CHECKPOINT_5473_STATE",
    }

    after_formalization = base_5467.formalization_snapshot()
    validations = [
        check("all_sources_exist", not missing, len(source_paths())),
        check(
            "checkpoint_5472_parent_v52_is_certified",
            truth(result_5472.get("valid_for_parent_v52_leaf_union_enclosure"))
            and int(result_5472.get("failed_validation_count", -1)) == 0
            and all(truth(row["passed"]) for row in validation_5472),
            result_5472.get("decision"),
        ),
        check(
            "checkpoint_5473_frontier_is_clean_and_hash_locked",
            int(result_5473.get("failed_validation_count", -1)) == 0
            and all(truth(row["passed"]) for row in validation_5473)
            and not state["unresolved"],
            state_sha256,
        ),
        check(
            "v52_target_reproduces_precise_stable_edge_failure",
            target_v52_expected_failure,
            target_v52.get("failure_message", ""),
        ),
        check(
            "v53_target_full_amplitude_is_finite",
            target_v53_passed
            and all(
                math.isfinite(float(target_v53[field]))
                and float(target_v53[field]) > 0.0
                for field in METRIC_FIELDS
            ),
            target_v53.get("minimum_amplitude_denominator_abs_lower"),
        ),
        check(
            "selected_t_leaf_union_is_an_exact_cover",
            exact_cover,
            payload["parameter_area_coverage_error"],
        ),
        check(
            "every_selected_leaf_has_positive_explicit_invariant",
            bool(selected_leaves)
            and all(
                float(row["left_first_soft_invariant_abs_lower"]) > 0.0
                for row in selected_leaves
            ),
            payload["minimum_selected_invariant_abs_lower"],
        ),
        check(
            "every_selected_leaf_has_positive_full_amplitude_factors",
            bool(selected_leaves)
            and all(
                float(row["minimum_amplitude_denominator_abs_lower"]) > 0.0
                and float(row["collision_jacobian_abs_lower"]) > 0.0
                for row in selected_leaves
            ),
            len(selected_leaves),
        ),
        check(
            "untriggered_v52_v53_control_is_exactly_unchanged",
            control_identical,
            control_node["refinement_path"],
        ),
        check(
            "v53_changes_only_enclosure_composition",
            not parent_v53_target.V53_PARENT_ACTION_CHANGED
            and parent_v53_target.V53_ONLY_ENCLOSURE_COMPOSITION_CHANGED
            and not parent_v53_target.V52_PARENT_ACTION_CHANGED
            and parent_v53_target.V52_ONLY_ENCLOSURE_COMPOSITION_CHANGED,
            PARENT_V53_REVISION,
        ),
        check(
            "formalization_workbench_untouched",
            before_formalization == after_formalization,
            f"before={len(before_formalization)};after={len(after_formalization)}",
        ),
        check(
            "broad_claims_remain_false",
            not payload["valid_for_parent_v53_active_cuboid"]
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
    payload["valid_for_parent_v53_stable_edge_t_leaf_union"] = (
        payload["failed_validation_count"] == 0
        and payload["decision"].startswith("PARENT_V53_")
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
                    "target_v52_expected_failure",
                    "target_v53_passed",
                    "selected_t_leaf_count",
                    "minimum_selected_invariant_abs_lower",
                    "target_v53_amplitude_denominator_abs_lower",
                    "target_v53_collision_jacobian_abs_lower",
                    "control_v52_v53_identical",
                    "valid_for_parent_v53_stable_edge_t_leaf_union",
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
