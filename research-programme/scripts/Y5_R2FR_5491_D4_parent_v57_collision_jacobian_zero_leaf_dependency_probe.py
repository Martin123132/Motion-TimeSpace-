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
OUTPUT = FUNCTIONAL_RG / "5491"

SCRIPT_5467 = SCRIPTS / "Y5_R2FR_5467_D4_all_outer_leaf_epsilon_fiber_transplant_runner.py"
SCRIPT_5468 = SCRIPTS / "Y5_R2FR_5468_D4_exact_outer_cuboid_coalescence_runner.py"
SCRIPT_5469 = SCRIPTS / "Y5_R2FR_5469_D4_resumable_three_axis_cuboid_certificate_runner.py"
SCRIPT_5472 = SCRIPTS / "Y5_R2FR_5472_D4_parent_v52_collision_jacobian_leaf_union_integration_gate.py"
SCRIPT_5474 = SCRIPTS / "Y5_R2FR_5474_D4_parent_v53_stable_edge_t_leaf_union_integration_gate.py"
SCRIPT_5476 = SCRIPTS / "Y5_R2FR_5476_D4_parent_v54_first_spinor_pivot_t_leaf_union_integration_gate.py"
SCRIPT_5478 = SCRIPTS / "Y5_R2FR_5478_D4_parent_v55_stable_edge_xt_leaf_union_integration_gate.py"
SCRIPT_5480 = SCRIPTS / "Y5_R2FR_5480_D4_parent_v55_hash_locked_frontier_runner.py"
SCRIPT_5483 = SCRIPTS / "Y5_R2FR_5483_D4_parent_v56_collision_jacobian_xt_leaf_union_integration_gate.py"
SCRIPT_5490 = SCRIPTS / "Y5_R2FR_5490_D4_parent_v57_collision_jacobian_epsilon_xt_leaf_union_candidate_probe.py"

MANIFEST_5468 = FUNCTIONAL_RG / "5468" / "D4_exact_outer_cuboid_manifest.csv"
STATE_5484 = (
    FUNCTIONAL_RG
    / "5484"
    / "work-v1"
    / "E07__U051__RIGHT_CONNECTOR__CUBOID__6df3d70a73e4618b.json"
)
RESULT_5490 = FUNCTIONAL_RG / "5490" / "D4_parent_v57_collision_jacobian_epsilon_xt_leaf_union_candidate_result.json"
VALIDATION_5490 = FUNCTIONAL_RG / "5490" / "P8_Y5_BRR5489_5490_VALIDATION.csv"

LOCATOR = OUTPUT / "D4_parent_v57_first_zero_leaf.json"
AXIS_AUDIT = OUTPUT / "D4_parent_v57_zero_leaf_single_axis_ablation.csv"
PAIR_AUDIT = OUTPUT / "D4_parent_v57_zero_leaf_pair_axis_ablation.csv"
POINT_AUDIT = OUTPUT / "D4_parent_v57_zero_leaf_point_sample.csv"
SOURCE_REGISTER = OUTPUT / "source_register.csv"
VALIDATION = OUTPUT / "P8_Y5_BRR5490_5491_VALIDATION.csv"
STATUS = OUTPUT / "status.json"
RESULT = OUTPUT / "D4_parent_v57_collision_jacobian_zero_leaf_dependency_result.json"
DOCUMENT = POST / "5491-Y5-R2FR-D4-parent-v57-collision-jacobian-zero-leaf-dependency-probe.md"

CHECKPOINT = 5491
REVISION = "D4-parent-v57-collision-jacobian-zero-leaf-dependency-probe-v1"
PARENT_V56_REVISION = "D4-deformed-contour-regular-away-W3-v56-collision-jacobian-xt-leaf-union"
PARENT_V57_DIAGNOSTIC_REVISION = "D4-deformed-contour-regular-away-W3-v57-zero-leaf-dependency-diagnostic"
TARGET_CUBOID_ID = "E07__U051__RIGHT_CONNECTOR__CUBOID__6df3d70a73e4618b"
TARGET_REFINEMENT_PATH = "R_E0S_E0S_E0S_E1S"
EXPECTED_STATE_SHA256 = "3f485d18bb2a55d3fda317091e58c0330166a7b5ae7e2185a82ab46602e23faa"
EXPECTED_FAILURE_MARKER = "global contour geometric denominator reaches zero"
LOCATOR_COUNTS = {"epsilon_real": 16, "x": 16, "t": 128}
AXIS_COUNTS = (2, 4, 8, 16, 32)
PAIR_COUNTS = (2, 4, 8, 16)
AXES = ("epsilon_real", "epsilon_imaginary", "x", "t")
AXIS_FIELDS = {
    "epsilon_real": ("epsilon_real_lower", "epsilon_real_upper"),
    "epsilon_imaginary": (
        "epsilon_imaginary_lower",
        "epsilon_imaginary_upper",
    ),
    "x": ("x_lower", "x_upper"),
    "t": ("t_lower", "t_upper"),
}


class DiagnosticComplete(RuntimeError):
    pass


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
        SCRIPT_5476,
        SCRIPT_5478,
        SCRIPT_5480,
        SCRIPT_5483,
        SCRIPT_5490,
        MANIFEST_5468,
        STATE_5484,
        RESULT_5490,
        VALIDATION_5490,
    )


def check(gate: str, passed: bool, evidence: Any) -> dict[str, Any]:
    return {
        "checkpoint": CHECKPOINT,
        "validation_gate": gate,
        "passed": bool(passed),
        "evidence": evidence,
    }


def make_box(
    parent: Any,
    epsilon_real_lower: float,
    epsilon_real_upper: float,
    epsilon_imaginary_lower: float,
    epsilon_imaginary_upper: float,
    x_lower: float,
    x_upper: float,
    t_lower: float,
    t_upper: float,
) -> tuple[Any, Any, Any]:
    return (
        parent.cbox(
            epsilon_real_lower,
            epsilon_real_upper,
            epsilon_imaginary_lower,
            epsilon_imaginary_upper,
        ),
        parent.cbox(x_lower, x_upper),
        parent.cbox(t_lower, t_upper),
    )


def evaluate_box(
    parent: Any,
    configuration: dict[str, Any],
    cell: dict[str, Any],
    path_segment: str,
    box: dict[str, float],
) -> tuple[float, float, str, Any, list[dict[str, Any]]]:
    epsilon, coordinate, parameter = make_box(
        parent,
        box["epsilon_real_lower"],
        box["epsilon_real_upper"],
        box["epsilon_imaginary_lower"],
        box["epsilon_imaginary_upper"],
        box["x_lower"],
        box["x_upper"],
        box["t_lower"],
        box["t_upper"],
    )
    candidates = [
        candidate
        for candidate in parent.path_correlated_collision_jacobian_candidates(
            configuration,
            cell,
            path_segment,
            coordinate,
            parameter,
            epsilon,
        )
        if candidate[3] > 0.0
    ]
    if not candidates:
        raise parent.M5258.IntervalSingularity(
            "zero-leaf dependency probe has no chart-covered candidate"
        )
    selected = max(candidates, key=lambda candidate: (candidate[0], candidate[3]))
    details = [
        {
            "lower": float(candidate[0]),
            "method": str(candidate[1]),
            "denominator_lower": float(candidate[3]),
        }
        for candidate in candidates
    ]
    return (
        float(selected[0]),
        float(selected[3]),
        str(selected[1]),
        selected[2],
        details,
    )


def locate_first_zero_leaf(
    parent: Any,
    configuration: dict[str, Any],
    cell: dict[str, Any],
    path_segment: str,
    inputs: dict[str, Any],
    path_context: dict[str, Any],
) -> dict[str, Any]:
    epsilon_real_lower, epsilon_real_upper = parent.M5394.real_bounds(
        inputs["epsilon"]
    )
    epsilon_imaginary_lower, epsilon_imaginary_upper = (
        parent.M5394.imaginary_bounds(inputs["epsilon"])
    )
    x_lower, x_upper = parent.M5394.real_bounds(
        path_context["absolute_coordinate"]
    )
    t_lower, t_upper = parent.M5394.real_bounds(path_context["path_parameter"])
    epsilon_count = LOCATOR_COUNTS["epsilon_real"]
    x_count = LOCATOR_COUNTS["x"]
    t_count = LOCATOR_COUNTS["t"]
    tested = 0
    started = time.perf_counter()
    for epsilon_index in range(epsilon_count):
        for x_index in range(x_count):
            for t_index in range(t_count):
                box = {
                    "epsilon_real_lower": epsilon_real_lower
                    + (epsilon_real_upper - epsilon_real_lower)
                    * epsilon_index
                    / epsilon_count,
                    "epsilon_real_upper": epsilon_real_lower
                    + (epsilon_real_upper - epsilon_real_lower)
                    * (epsilon_index + 1)
                    / epsilon_count,
                    "epsilon_imaginary_lower": epsilon_imaginary_lower,
                    "epsilon_imaginary_upper": epsilon_imaginary_upper,
                    "x_lower": x_lower
                    + (x_upper - x_lower) * x_index / x_count,
                    "x_upper": x_lower
                    + (x_upper - x_lower) * (x_index + 1) / x_count,
                    "t_lower": t_lower
                    + (t_upper - t_lower) * t_index / t_count,
                    "t_upper": t_lower
                    + (t_upper - t_lower) * (t_index + 1) / t_count,
                }
                selected_lower, denominator, method, jacobian, details = evaluate_box(
                    parent,
                    configuration,
                    cell,
                    path_segment,
                    box,
                )
                tested += 1
                if selected_lower <= 0.0:
                    jacobian_real_lower, jacobian_real_upper = (
                        parent.M5394.real_bounds(jacobian)
                    )
                    jacobian_imaginary_lower, jacobian_imaginary_upper = (
                        parent.M5394.imaginary_bounds(jacobian)
                    )
                    return {
                        **box,
                        "epsilon_index": epsilon_index,
                        "x_index": x_index,
                        "t_index": t_index,
                        "tested_leaf_count": tested,
                        "selected_lower": selected_lower,
                        "selected_method": method,
                        "minimum_chart_denominator_abs_lower": denominator,
                        "jacobian_real_lower": jacobian_real_lower,
                        "jacobian_real_upper": jacobian_real_upper,
                        "jacobian_imaginary_lower": jacobian_imaginary_lower,
                        "jacobian_imaginary_upper": jacobian_imaginary_upper,
                        "candidate_details": json.dumps(
                            details,
                            sort_keys=True,
                            separators=(",", ":"),
                        ),
                        "runtime_seconds": time.perf_counter() - started,
                    }
    raise RuntimeError("E16/X16/T128 scan found no zero leaf")


def partition_box(
    box: dict[str, float],
    axis: str,
    index: int,
    count: int,
) -> dict[str, float]:
    lower_field, upper_field = AXIS_FIELDS[axis]
    lower = float(box[lower_field])
    upper = float(box[upper_field])
    child = dict(box)
    child[lower_field] = lower + (upper - lower) * index / count
    child[upper_field] = lower + (upper - lower) * (index + 1) / count
    return child


def single_axis_ablation(
    parent: Any,
    configuration: dict[str, Any],
    cell: dict[str, Any],
    path_segment: str,
    zero_leaf: dict[str, Any],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    base_box = {field: float(zero_leaf[field]) for fields in AXIS_FIELDS.values() for field in fields}
    for axis in AXES:
        for count in AXIS_COUNTS:
            started = time.perf_counter()
            lowers: list[float] = []
            denominators: list[float] = []
            methods: dict[str, int] = {}
            first_zero_index = -1
            for index in range(count):
                child = partition_box(base_box, axis, index, count)
                lower, denominator, method, _, _ = evaluate_box(
                    parent,
                    configuration,
                    cell,
                    path_segment,
                    child,
                )
                lowers.append(lower)
                denominators.append(denominator)
                methods[method] = methods.get(method, 0) + 1
                if lower <= 0.0 and first_zero_index < 0:
                    first_zero_index = index
            original_width = (
                base_box[AXIS_FIELDS[axis][1]] - base_box[AXIS_FIELDS[axis][0]]
            )
            covered_width = sum(
                partition_box(base_box, axis, index, count)[AXIS_FIELDS[axis][1]]
                - partition_box(base_box, axis, index, count)[AXIS_FIELDS[axis][0]]
                for index in range(count)
            )
            row = {
                "axis": axis,
                "count": count,
                "status": "PASS" if min(lowers) > 0.0 else "ZERO",
                "leaf_union_abs_lower": min(lowers),
                "minimum_chart_denominator_abs_lower": min(denominators),
                "coverage_error": abs(covered_width - original_width),
                "first_zero_index": first_zero_index,
                "method_counts": json.dumps(
                    methods,
                    sort_keys=True,
                    separators=(",", ":"),
                ),
                "runtime_seconds": time.perf_counter() - started,
            }
            rows.append(row)
            if row["status"] == "PASS":
                break
    return rows


def pair_axis_ablation(
    parent: Any,
    configuration: dict[str, Any],
    cell: dict[str, Any],
    path_segment: str,
    zero_leaf: dict[str, Any],
    run_pairs: bool,
) -> list[dict[str, Any]]:
    if not run_pairs:
        return []
    rows: list[dict[str, Any]] = []
    base_box = {field: float(zero_leaf[field]) for fields in AXIS_FIELDS.values() for field in fields}
    for left_index, left_axis in enumerate(AXES):
        for right_axis in AXES[left_index + 1 :]:
            for count in PAIR_COUNTS:
                started = time.perf_counter()
                lowers: list[float] = []
                denominators: list[float] = []
                first_zero_index = ""
                for left_leaf_index in range(count):
                    left_child = partition_box(
                        base_box,
                        left_axis,
                        left_leaf_index,
                        count,
                    )
                    for right_leaf_index in range(count):
                        child = partition_box(
                            left_child,
                            right_axis,
                            right_leaf_index,
                            count,
                        )
                        lower, denominator, _, _, _ = evaluate_box(
                            parent,
                            configuration,
                            cell,
                            path_segment,
                            child,
                        )
                        lowers.append(lower)
                        denominators.append(denominator)
                        if lower <= 0.0 and not first_zero_index:
                            first_zero_index = (
                                f"{left_leaf_index}:{right_leaf_index}"
                            )
                row = {
                    "left_axis": left_axis,
                    "right_axis": right_axis,
                    "count_per_axis": count,
                    "leaf_count": count * count,
                    "status": "PASS" if min(lowers) > 0.0 else "ZERO",
                    "leaf_union_abs_lower": min(lowers),
                    "minimum_chart_denominator_abs_lower": min(denominators),
                    "coverage_error": 0.0,
                    "first_zero_index": first_zero_index,
                    "runtime_seconds": time.perf_counter() - started,
                }
                rows.append(row)
                if row["status"] == "PASS":
                    break
    return rows


def point_sample(
    parent: Any,
    configuration: dict[str, Any],
    cell: dict[str, Any],
    path_segment: str,
    zero_leaf: dict[str, Any],
) -> list[dict[str, Any]]:
    values: dict[str, tuple[float, float, float]] = {}
    for axis, (lower_field, upper_field) in AXIS_FIELDS.items():
        lower = float(zero_leaf[lower_field])
        upper = float(zero_leaf[upper_field])
        values[axis] = (lower, 0.5 * (lower + upper), upper)
    rows: list[dict[str, Any]] = []
    for epsilon_real_index, epsilon_real in enumerate(values["epsilon_real"]):
        for epsilon_imaginary_index, epsilon_imaginary in enumerate(
            values["epsilon_imaginary"]
        ):
            for x_index, x_value in enumerate(values["x"]):
                for t_index, t_value in enumerate(values["t"]):
                    box = {
                        "epsilon_real_lower": epsilon_real,
                        "epsilon_real_upper": epsilon_real,
                        "epsilon_imaginary_lower": epsilon_imaginary,
                        "epsilon_imaginary_upper": epsilon_imaginary,
                        "x_lower": x_value,
                        "x_upper": x_value,
                        "t_lower": t_value,
                        "t_upper": t_value,
                    }
                    lower, denominator, method, jacobian, _ = evaluate_box(
                        parent,
                        configuration,
                        cell,
                        path_segment,
                        box,
                    )
                    jacobian_real_lower, jacobian_real_upper = (
                        parent.M5394.real_bounds(jacobian)
                    )
                    jacobian_imaginary_lower, jacobian_imaginary_upper = (
                        parent.M5394.imaginary_bounds(jacobian)
                    )
                    rows.append(
                        {
                            "epsilon_real_index": epsilon_real_index,
                            "epsilon_imaginary_index": epsilon_imaginary_index,
                            "x_index": x_index,
                            "t_index": t_index,
                            "epsilon_real": epsilon_real,
                            "epsilon_imaginary": epsilon_imaginary,
                            "x": x_value,
                            "t": t_value,
                            "selected_abs_lower": lower,
                            "minimum_chart_denominator_abs_lower": denominator,
                            "selected_method": method,
                            "jacobian_real_lower": jacobian_real_lower,
                            "jacobian_real_upper": jacobian_real_upper,
                            "jacobian_imaginary_lower": jacobian_imaginary_lower,
                            "jacobian_imaginary_upper": jacobian_imaginary_upper,
                        }
                    )
    return rows


def install_diagnostic(parent: Any) -> Any:
    if parent.REVISION != PARENT_V56_REVISION:
        raise RuntimeError(
            f"expected parent revision {PARENT_V56_REVISION}, found {parent.REVISION}"
        )
    original = parent.tight_energy_contour_geometric_factors
    parent.V57_ZERO_LEAF = None
    parent.V57_AXIS_ROWS = []
    parent.V57_PAIR_ROWS = []
    parent.V57_POINT_ROWS = []

    def tight_diagnostic(
        configuration: dict[str, Any],
        inputs: dict[str, Any],
        geometry: dict[str, Any],
        path_context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        factors = original(configuration, inputs, geometry, path_context)
        lower = float(
            factors.get(
                "collision_jacobian_selected_abs_lower",
                parent.M5258.lower_abs(factors["collision_jacobian"]),
            )
        )
        if (
            lower > 0.0
            or path_context is None
            or path_context.get("path_segment")
            not in {"LEFT_CONNECTOR", "RIGHT_CONNECTOR"}
        ):
            return factors
        zero_leaf = locate_first_zero_leaf(
            parent,
            configuration,
            path_context["cell"],
            path_context["path_segment"],
            inputs,
            path_context,
        )
        axis_rows = single_axis_ablation(
            parent,
            configuration,
            path_context["cell"],
            path_context["path_segment"],
            zero_leaf,
        )
        single_axis_pass = any(row["status"] == "PASS" for row in axis_rows)
        pair_rows = pair_axis_ablation(
            parent,
            configuration,
            path_context["cell"],
            path_context["path_segment"],
            zero_leaf,
            not single_axis_pass,
        )
        point_rows = point_sample(
            parent,
            configuration,
            path_context["cell"],
            path_context["path_segment"],
            zero_leaf,
        )
        parent.V57_ZERO_LEAF = {
            **zero_leaf,
            "configuration_role": configuration.get("role", ""),
            "path_segment": path_context["path_segment"],
        }
        parent.V57_AXIS_ROWS = axis_rows
        parent.V57_PAIR_ROWS = pair_rows
        parent.V57_POINT_ROWS = point_rows
        raise DiagnosticComplete("v57 collision-Jacobian zero-leaf diagnostic complete")

    parent.tight_energy_contour_geometric_factors = tight_diagnostic
    parent.REVISION = PARENT_V57_DIAGNOSTIC_REVISION
    return parent


def render_document(payload: dict[str, Any], base_5467: Any) -> None:
    lines = [
        "# 5491: D4 parent-v57 collision-Jacobian zero-leaf dependency probe",
        "",
        "Checkpoint 5490 proves that epsilon-real counts through 16 do not close the first positive-epsilon parent-v56 box. This probe locates the first exact E16/X16/T128 zero leaf, ablates each interval axis on that leaf, then checks paired axes only if no single axis resolves it. An 81-point corners/midpoints scan is diagnostic and is never promoted to an interval proof.",
        "",
        f"First zero leaf index: `E{payload['zero_leaf_epsilon_index']}:X{payload['zero_leaf_x_index']}:T{payload['zero_leaf_t_index']}` after `{payload['zero_leaf_tested_count']}` leaves. Selected chart denominator lower: `{payload['zero_leaf_chart_denominator_abs_lower']}`.",
        "",
        f"Single-axis pass: `{payload['selected_single_axis']}` at count `{payload['selected_single_axis_count']}` with lower `{payload['selected_single_axis_lower']}`. Paired-axis pass: `{payload['selected_axis_pair']}` at count `{payload['selected_pair_count']}` with lower `{payload['selected_pair_lower']}`.",
        "",
        f"Point-sample minimum: `{payload['point_sample_minimum_abs_lower']}` across `{payload['point_sample_count']}` samples. This is diagnostic only.",
        "",
        f"**{payload['decision']}**",
        "",
        "No parent action, contour, chart candidate, residue or threshold changes. This does not certify parent v57, the active cuboid, the outer enclosure, local GR or MTS.",
        "",
    ]
    base_5467.atomic_text(DOCUMENT, "\n".join(lines))


def main() -> int:
    base_5467 = load_module("mts_5467_for_5491", SCRIPT_5467)
    base_5468 = load_module("mts_5468_for_5491", SCRIPT_5468)
    base_5469 = load_module("mts_5469_for_5491", SCRIPT_5469)
    base_5472 = load_module("mts_5472_for_5491", SCRIPT_5472)
    base_5474 = load_module("mts_5474_for_5491", SCRIPT_5474)
    base_5476 = load_module("mts_5476_for_5491", SCRIPT_5476)
    base_5478 = load_module("mts_5478_for_5491", SCRIPT_5478)
    base_5480 = load_module("mts_5480_for_5491", SCRIPT_5480)
    base_5483 = load_module("mts_5483_for_5491", SCRIPT_5483)
    base_5490 = load_module("mts_5490_for_5491", SCRIPT_5490)
    base_5467.set_below_normal_priority()
    base_5480.set_single_core_affinity()
    before_formalization = base_5467.formalization_snapshot()
    missing = [str(path) for path in source_paths() if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"missing sources: {missing}")
    state_sha256 = digest(STATE_5484)
    if state_sha256 != EXPECTED_STATE_SHA256:
        raise RuntimeError("checkpoint 5484 state differs from checkpoint-5491 lock")
    result_5490 = read_json(RESULT_5490)
    validation_5490 = read_csv(VALIDATION_5490)
    state = read_json(STATE_5484)
    cuboid = next(
        row
        for row in read_csv(MANIFEST_5468)
        if row["cuboid_job_id"] == TARGET_CUBOID_ID
    )
    candidates = [
        row
        for row in state["refinement_witnesses"]
        if row.get("refinement_path") == TARGET_REFINEMENT_PATH
        and EXPECTED_FAILURE_MARKER in str(row.get("failure_message", ""))
    ]
    if len(candidates) != 1:
        raise RuntimeError(f"expected one target witness, found {len(candidates)}")
    target = candidates[0]
    stable, _, cells, support_segments, branches = base_5467.load_parent()
    parent = install_diagnostic(
        base_5490.fresh_v56(
            base_5467,
            base_5472,
            base_5474,
            base_5476,
            base_5478,
            base_5483,
        )
    )
    probe_result = base_5469.evaluate_node(
        base_5468,
        stable,
        parent,
        cells,
        support_segments,
        branches,
        cuboid,
        target,
    )
    zero_leaf = parent.V57_ZERO_LEAF
    axis_rows = list(parent.V57_AXIS_ROWS)
    pair_rows = list(parent.V57_PAIR_ROWS)
    point_rows = list(parent.V57_POINT_ROWS)
    if zero_leaf is None:
        raise RuntimeError("diagnostic did not produce a zero leaf")
    single_passes = [row for row in axis_rows if row["status"] == "PASS"]
    pair_passes = [row for row in pair_rows if row["status"] == "PASS"]
    selected_single = single_passes[0] if single_passes else None
    selected_pair = pair_passes[0] if pair_passes else None
    point_minimum = min(float(row["selected_abs_lower"]) for row in point_rows)
    if selected_single:
        decision = "ZERO_LEAF_SINGLE_AXIS_DEPENDENCY_IDENTIFIED__BUILD_TARGETED_EXACT_COVER"
        next_target = "BUILD_SINGLE_AXIS_ZERO_LEAF_TARGET_CONTROL_GATE"
    elif selected_pair:
        decision = "ZERO_LEAF_PAIRED_AXIS_DEPENDENCY_IDENTIFIED__BUILD_TARGETED_EXACT_COVER"
        next_target = "BUILD_PAIRED_AXIS_ZERO_LEAF_TARGET_CONTROL_GATE"
    elif point_minimum <= 0.0:
        decision = "POINTWISE_ZERO_CANDIDATE_FOUND__DERIVE_ANALYTIC_JACOBIAN_ZERO_SET"
        next_target = "DERIVE_ANALYTIC_COLLISION_JACOBIAN_ZERO_SET"
    else:
        decision = "MULTI_AXIS_INTERVAL_DEPENDENCY_REMAINS__BUILD_ADAPTIVE_LOCAL_COVER"
        next_target = "BUILD_ADAPTIVE_MULTI_AXIS_ZERO_LEAF_COVER"
    payload: dict[str, Any] = {
        "checkpoint": CHECKPOINT,
        "revision": REVISION,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "decision": decision,
        "target_cuboid_id": TARGET_CUBOID_ID,
        "target_refinement_path": TARGET_REFINEMENT_PATH,
        "source_state_5484_sha256": state_sha256,
        "diagnostic_terminated_intentionally": (
            probe_result.get("failure_type") == "DiagnosticComplete"
        ),
        "zero_leaf_epsilon_index": int(zero_leaf["epsilon_index"]),
        "zero_leaf_x_index": int(zero_leaf["x_index"]),
        "zero_leaf_t_index": int(zero_leaf["t_index"]),
        "zero_leaf_tested_count": int(zero_leaf["tested_leaf_count"]),
        "zero_leaf_chart_denominator_abs_lower": float(
            zero_leaf["minimum_chart_denominator_abs_lower"]
        ),
        "zero_leaf_selected_method": zero_leaf["selected_method"],
        "axis_audit_row_count": len(axis_rows),
        "pair_audit_row_count": len(pair_rows),
        "point_sample_count": len(point_rows),
        "point_sample_minimum_abs_lower": point_minimum,
        "selected_single_axis": selected_single["axis"] if selected_single else "",
        "selected_single_axis_count": (
            int(selected_single["count"]) if selected_single else 0
        ),
        "selected_single_axis_lower": (
            float(selected_single["leaf_union_abs_lower"])
            if selected_single
            else 0.0
        ),
        "selected_axis_pair": (
            f"{selected_pair['left_axis']}+{selected_pair['right_axis']}"
            if selected_pair
            else ""
        ),
        "selected_pair_count": (
            int(selected_pair["count_per_axis"]) if selected_pair else 0
        ),
        "selected_pair_lower": (
            float(selected_pair["leaf_union_abs_lower"])
            if selected_pair
            else 0.0
        ),
        "parent_action_changed": False,
        "valid_for_parent_v57_active_cuboid": False,
        "valid_for_full_outer_parent_leaf_enclosure": False,
        "valid_for_D4_event_local_W3_bound": False,
        "valid_for_all_operator_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
        "next_target": next_target,
    }
    after_formalization = base_5467.formalization_snapshot()
    axis_numeric = bool(axis_rows) and all(
        math.isfinite(float(row["leaf_union_abs_lower"]))
        and float(row["minimum_chart_denominator_abs_lower"]) > 0.0
        and float(row["coverage_error"]) <= 1.0e-18
        for row in axis_rows
    )
    pair_numeric = not pair_rows or all(
        math.isfinite(float(row["leaf_union_abs_lower"]))
        and float(row["minimum_chart_denominator_abs_lower"]) > 0.0
        and float(row["coverage_error"]) <= 1.0e-18
        for row in pair_rows
    )
    point_numeric = len(point_rows) == 81 and all(
        math.isfinite(float(row["selected_abs_lower"]))
        and float(row["minimum_chart_denominator_abs_lower"]) > 0.0
        for row in point_rows
    )
    validations = [
        check("all_sources_exist", not missing, len(source_paths())),
        check("source_state_is_hash_locked", state_sha256 == EXPECTED_STATE_SHA256, state_sha256),
        check(
            "checkpoint_5490_negative_candidate_result_is_valid",
            int(result_5490.get("failed_validation_count", -1)) == 0
            and all(truth(row["passed"]) for row in validation_5490)
            and result_5490.get("selected_epsilon_count") == 0,
            result_5490.get("decision"),
        ),
        check("target_witness_is_unique", len(candidates) == 1, TARGET_REFINEMENT_PATH),
        check(
            "diagnostic_stops_before_parent_acceptance",
            payload["diagnostic_terminated_intentionally"]
            and not payload["valid_for_parent_v57_active_cuboid"],
            probe_result.get("failure_type", ""),
        ),
        check(
            "first_zero_leaf_is_located_with_positive_chart_denominator",
            float(zero_leaf["selected_lower"]) == 0.0
            and payload["zero_leaf_chart_denominator_abs_lower"] > 0.0,
            f"tested={payload['zero_leaf_tested_count']}",
        ),
        check("single_axis_ablation_is_numeric_and_exact", axis_numeric, len(axis_rows)),
        check("pair_axis_ablation_is_numeric_and_exact", pair_numeric, len(pair_rows)),
        check("point_sample_is_complete_numeric_diagnostic", point_numeric, len(point_rows)),
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
            "zero-leaf dependency diagnostic only",
        ),
    ]
    payload["validation_row_count"] = len(validations)
    payload["failed_validation_count"] = sum(not row["passed"] for row in validations)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    base_5467.atomic_json(LOCATOR, zero_leaf)
    base_5467.atomic_csv(AXIS_AUDIT, axis_rows)
    if pair_rows:
        base_5467.atomic_csv(PAIR_AUDIT, pair_rows)
    base_5467.atomic_csv(POINT_AUDIT, point_rows)
    base_5467.atomic_csv(
        SOURCE_REGISTER,
        [
            {
                "source_path": str(path),
                "sha256": digest(path),
                "exists": path.is_file(),
            }
            for path in source_paths()
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
                    "zero_leaf_epsilon_index",
                    "zero_leaf_x_index",
                    "zero_leaf_t_index",
                    "zero_leaf_tested_count",
                    "selected_single_axis",
                    "selected_single_axis_count",
                    "selected_single_axis_lower",
                    "selected_axis_pair",
                    "selected_pair_count",
                    "selected_pair_lower",
                    "point_sample_minimum_abs_lower",
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
