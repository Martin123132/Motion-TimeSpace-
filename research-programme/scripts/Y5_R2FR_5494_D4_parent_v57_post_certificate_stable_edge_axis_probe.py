from __future__ import annotations

import csv
import hashlib
import importlib.util
import inspect
import json
import math
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


POST = Path(__file__).resolve().parents[1]
SCRIPTS = POST / "scripts"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
OUTPUT = FUNCTIONAL_RG / "5494"

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
SCRIPT_5493 = SCRIPTS / "Y5_R2FR_5493_D4_parent_v57_scoped_certificate_integration_gate.py"

MANIFEST_5468 = FUNCTIONAL_RG / "5468" / "D4_exact_outer_cuboid_manifest.csv"
STATE_5484 = (
    FUNCTIONAL_RG
    / "5484"
    / "work-v1"
    / "E07__U051__RIGHT_CONNECTOR__CUBOID__6df3d70a73e4618b.json"
)
RESULT_5492 = FUNCTIONAL_RG / "5492" / "D4_parent_v57_adaptive_x_replacement_candidate_result.json"
WORK_STATE_5492 = FUNCTIONAL_RG / "5492" / "work-v1" / "adaptive_x_replacement_state.json"
LEAF_AUDIT_5492 = FUNCTIONAL_RG / "5492" / "D4_parent_v57_adaptive_x_replacement_leaf_audit.csv"
RESULT_5493 = FUNCTIONAL_RG / "5493" / "D4_parent_v57_scoped_certificate_integration_result.json"
VALIDATION_5493 = FUNCTIONAL_RG / "5493" / "P8_Y5_BRR5492_5493_VALIDATION.csv"
SOURCE_REGISTER_5493 = FUNCTIONAL_RG / "5493" / "source_register.csv"
SCOPE_BINDING_5493 = FUNCTIONAL_RG / "5493" / "D4_parent_v57_scoped_certificate_binding.json"

V55_AUDIT = OUTPUT / "D4_parent_v57_post_certificate_v55_stable_edge_audit.csv"
AXIS_AUDIT = OUTPUT / "D4_parent_v57_post_certificate_stable_edge_axis_ablation.csv"
V57_AUDIT = OUTPUT / "D4_parent_v57_certificate_application_audit.csv"
SOURCE_REGISTER = OUTPUT / "source_register.csv"
VALIDATION = OUTPUT / "P8_Y5_BRR5493_5494_VALIDATION.csv"
STATUS = OUTPUT / "status.json"
RESULT = OUTPUT / "D4_parent_v57_post_certificate_stable_edge_axis_result.json"
DOCUMENT = POST / "5494-Y5-R2FR-D4-parent-v57-post-certificate-stable-edge-axis-probe.md"

CHECKPOINT = 5494
REVISION = "D4-parent-v57-post-certificate-stable-edge-axis-probe-v1"
TARGET_CUBOID_ID = "E07__U051__RIGHT_CONNECTOR__CUBOID__6df3d70a73e4618b"
TARGET_REFINEMENT_PATH = "R_E0S_E0S_E0S_E1S"
EXPECTED_FAILURE_MARKER = "edge_2_1_3:stable_edge"
EXPECTED_STATE_SHA256 = "3f485d18bb2a55d3fda317091e58c0330166a7b5ae7e2185a82ab46602e23faa"
EXPECTED_RESULT_5493_SHA256 = "439347c5b5bdfa92784ef032b6125503687148f4321b54dadeb8fbafc97619d1"
EXPECTED_BINDING_5493_SHA256 = "180597828dfd42a66e81f15671959791c35fd57b2b138fd72c37700bc0a254e6"
EXPECTED_VALIDATION_5493_SHA256 = "b3505a7a14ade71b8c23b46513b823f0a60fbde6091fe27f252182b525f97c01"
AXIS_COUNTS = (2, 4, 8, 16, 32)
AXES = ("epsilon_real", "epsilon_imaginary", "x", "t")


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
        SCRIPT_5493,
        MANIFEST_5468,
        STATE_5484,
        RESULT_5492,
        WORK_STATE_5492,
        LEAF_AUDIT_5492,
        RESULT_5493,
        VALIDATION_5493,
        SOURCE_REGISTER_5493,
        SCOPE_BINDING_5493,
    )


def check(gate: str, passed: bool, evidence: Any) -> dict[str, Any]:
    return {
        "checkpoint": CHECKPOINT,
        "validation_gate": gate,
        "passed": bool(passed),
        "evidence": evidence,
    }


def source_register_is_current(rows: list[dict[str, str]]) -> bool:
    return bool(rows) and all(
        truth(row.get("exists"))
        and Path(row["source_path"]).is_file()
        and digest(Path(row["source_path"])) == row["sha256"]
        for row in rows
    )


def fresh_v57_with_v54_handle(
    base_5467: Any,
    base_5472: Any,
    base_5474: Any,
    base_5476: Any,
    base_5478: Any,
    base_5483: Any,
    base_5493: Any,
    binding: dict[str, Any],
    certificate: dict[str, Any],
) -> tuple[Any, Any]:
    parent = base_5472.install_parent_v52(
        base_5472.fresh_parent(base_5467, "mts_parent_v57_axis_probe_5494")
    )
    parent = base_5474.install_parent_v53(parent)
    parent = base_5476.install_parent_v54(parent, base_5474)
    evaluate_v54 = parent.evaluate_path_box
    parent = base_5478.install_parent_v55(parent, base_5474)
    parent = base_5483.install_parent_v56(parent, base_5472)
    parent = base_5493.install_parent_v57(parent, binding, certificate)
    return parent, evaluate_v54


def install_path_failure_capture(parent: Any) -> Any:
    original = parent.evaluate_path_box
    signature = inspect.signature(original)
    parent.V57_STABLE_EDGE_CAPTURE = None

    def evaluate_capture(*args: Any, **kwargs: Any) -> dict[str, Any]:
        try:
            return original(*args, **kwargs)
        except parent.M5258.IntervalSingularity as error:
            if (
                EXPECTED_FAILURE_MARKER in str(error)
                and parent.V57_STABLE_EDGE_CAPTURE is None
            ):
                bound = signature.bind_partial(*args, **kwargs)
                bound.apply_defaults()
                parent.V57_STABLE_EDGE_CAPTURE = {
                    "arguments": dict(bound.arguments),
                    "failure_type": type(error).__name__,
                    "failure_message": str(error).splitlines()[0][:600],
                }
            raise

    parent.evaluate_path_box = evaluate_capture
    return parent


def finest_failed_leaf(rows: list[dict[str, Any]]) -> dict[str, Any]:
    failed = [
        row
        for row in rows
        if row.get("row_type") == "leaf" and row.get("status") == "FAIL"
    ]
    if not failed:
        raise RuntimeError("parent-v55 audit contains no failed leaf")
    return max(
        failed,
        key=lambda row: (
            int(row["x_count"]) * int(row["t_count"]),
            -int(row["x_index"]),
            -int(row["t_index"]),
        ),
    )


def split_interval(lower: float, upper: float, index: int, count: int) -> tuple[float, float]:
    return (
        lower + (upper - lower) * index / count,
        lower + (upper - lower) * (index + 1) / count,
    )


def axis_child_arguments(
    captured: dict[str, Any],
    failed_leaf: dict[str, Any],
    axis: str,
    index: int,
    count: int,
) -> dict[str, Any]:
    arguments = dict(captured)
    arguments["epsilon_row"] = dict(captured["epsilon_row"])
    arguments["x_lower"] = float(failed_leaf["x_lower"])
    arguments["x_upper"] = float(failed_leaf["x_upper"])
    arguments["t_lower"] = float(failed_leaf["t_lower"])
    arguments["t_upper"] = float(failed_leaf["t_upper"])
    arguments["refinement_depth"] = int(captured["refinement_depth"]) + 1
    arguments["refinement_path"] = (
        f"{captured['refinement_path']}:V57_AXIS:{axis}:{count}:{index}"
    )
    if axis == "x":
        arguments["x_lower"], arguments["x_upper"] = split_interval(
            float(failed_leaf["x_lower"]),
            float(failed_leaf["x_upper"]),
            index,
            count,
        )
    elif axis == "t":
        arguments["t_lower"], arguments["t_upper"] = split_interval(
            float(failed_leaf["t_lower"]),
            float(failed_leaf["t_upper"]),
            index,
            count,
        )
    elif axis == "epsilon_real":
        lower, upper = split_interval(
            float(captured["epsilon_row"]["epsilon_real_lower"]),
            float(captured["epsilon_row"]["epsilon_real_upper"]),
            index,
            count,
        )
        arguments["epsilon_row"]["epsilon_real_lower"] = lower
        arguments["epsilon_row"]["epsilon_real_upper"] = upper
    elif axis == "epsilon_imaginary":
        lower, upper = split_interval(
            float(captured["epsilon_row"]["epsilon_imaginary_lower"]),
            float(captured["epsilon_row"]["epsilon_imaginary_upper"]),
            index,
            count,
        )
        arguments["epsilon_row"]["epsilon_imaginary_lower"] = lower
        arguments["epsilon_row"]["epsilon_imaginary_upper"] = upper
    else:
        raise ValueError(f"unknown axis {axis}")
    return arguments


def axis_ablation(
    parent: Any,
    evaluate_v54: Any,
    captured: dict[str, Any],
    failed_leaf: dict[str, Any],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for axis in AXES:
        for count in AXIS_COUNTS:
            started = time.perf_counter()
            results: list[dict[str, Any]] = []
            failure: Exception | None = None
            failed_index = -1
            for index in range(count):
                arguments = axis_child_arguments(
                    captured,
                    failed_leaf,
                    axis,
                    index,
                    count,
                )
                try:
                    results.append(evaluate_v54(**arguments))
                except (
                    parent.EnclosureFailure,
                    parent.M5258.IntervalSingularity,
                    ValueError,
                ) as error:
                    failure = error
                    failed_index = index
                    break
            status = "PASS" if failure is None and len(results) == count else "FAIL"
            if axis == "x":
                original_width = float(failed_leaf["x_upper"]) - float(
                    failed_leaf["x_lower"]
                )
            elif axis == "t":
                original_width = float(failed_leaf["t_upper"]) - float(
                    failed_leaf["t_lower"]
                )
            elif axis == "epsilon_real":
                original_width = float(
                    captured["epsilon_row"]["epsilon_real_upper"]
                ) - float(captured["epsilon_row"]["epsilon_real_lower"])
            else:
                original_width = float(
                    captured["epsilon_row"]["epsilon_imaginary_upper"]
                ) - float(captured["epsilon_row"]["epsilon_imaginary_lower"])
            covered_width = original_width if status == "PASS" else math.nan
            rows.append(
                {
                    "axis": axis,
                    "count": count,
                    "status": status,
                    "completed_child_count": len(results),
                    "failed_child_index": failed_index,
                    "minimum_amplitude_denominator_abs_lower": (
                        min(
                            float(result["minimum_amplitude_denominator_abs_lower"])
                            for result in results
                        )
                        if results
                        else math.nan
                    ),
                    "minimum_collision_jacobian_abs_lower": (
                        min(
                            float(result["collision_jacobian_abs_lower"])
                            for result in results
                        )
                        if results
                        else math.nan
                    ),
                    "maximum_integrated_regular_path_abs_upper": (
                        max(
                            float(result["integrated_regular_path_abs_upper"])
                            for result in results
                        )
                        if results
                        else math.nan
                    ),
                    "coverage_error": (
                        abs(covered_width - original_width)
                        if status == "PASS"
                        else math.nan
                    ),
                    "runtime_seconds": time.perf_counter() - started,
                    "error_type": type(failure).__name__ if failure else "",
                    "error": (
                        str(failure).splitlines()[0][:600] if failure else ""
                    ),
                }
            )
            if status == "PASS":
                break
    return rows


def render_document(payload: dict[str, Any], base_5467: Any) -> None:
    lines = [
        "# 5494: D4 parent-v57 post-certificate stable-edge axis probe",
        "",
        "Checkpoint 5493 applies the scoped collision-Jacobian certificate correctly, then exposes the established stable-edge denominator class. This probe reproduces that post-certificate target, preserves the inherited parent-v55 schedule audit, captures the exact failing complete-amplitude call and ablates epsilon-real, epsilon-imaginary, x and t on its finest failed leaf through count 32.",
        "",
        f"Parent-v57 target failure reproduced: `{payload['target_stable_edge_failure_reproduced']}`. V55 schedule rows: `{payload['v55_schedule_row_count']}`. Finest failed schedule: `X{payload['failed_leaf_x_count']} x T{payload['failed_leaf_t_count']}` at leaf `{payload['failed_leaf_x_index']}:{payload['failed_leaf_t_index']}`.",
        "",
        f"Selected resolving axis: `{payload['selected_axis']}` at count `{payload['selected_axis_count']}`. Complete-child amplitude-denominator lower: `{payload['selected_axis_amplitude_denominator_abs_lower']}`. Collision-Jacobian lower: `{payload['selected_axis_collision_jacobian_abs_lower']}`.",
        "",
        f"**{payload['decision']}**",
        "",
        "This is a local complete-amplitude axis diagnostic only. No parent-v58 mechanism, active-cuboid certificate or broader GR/MTS claim is made.",
        "",
    ]
    base_5467.atomic_text(DOCUMENT, "\n".join(lines))


def main() -> int:
    base_5467 = load_module("mts_5467_for_5494", SCRIPT_5467)
    base_5468 = load_module("mts_5468_for_5494", SCRIPT_5468)
    base_5469 = load_module("mts_5469_for_5494", SCRIPT_5469)
    base_5472 = load_module("mts_5472_for_5494", SCRIPT_5472)
    base_5474 = load_module("mts_5474_for_5494", SCRIPT_5474)
    base_5476 = load_module("mts_5476_for_5494", SCRIPT_5476)
    base_5478 = load_module("mts_5478_for_5494", SCRIPT_5478)
    base_5480 = load_module("mts_5480_for_5494", SCRIPT_5480)
    base_5483 = load_module("mts_5483_for_5494", SCRIPT_5483)
    base_5490 = load_module("mts_5490_for_5494", SCRIPT_5490)
    base_5493 = load_module("mts_5493_for_5494", SCRIPT_5493)
    base_5467.set_below_normal_priority()
    base_5480.set_single_core_affinity()
    before_formalization = base_5467.formalization_snapshot()
    missing = [str(path) for path in source_paths() if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"missing sources: {missing}")
    state_sha256 = digest(STATE_5484)
    result_5493_sha256 = digest(RESULT_5493)
    binding_5493_sha256 = digest(SCOPE_BINDING_5493)
    validation_5493_sha256 = digest(VALIDATION_5493)
    if state_sha256 != EXPECTED_STATE_SHA256:
        raise RuntimeError("checkpoint 5484 state differs from checkpoint-5494 lock")
    if result_5493_sha256 != EXPECTED_RESULT_5493_SHA256:
        raise RuntimeError("checkpoint 5493 result differs from source lock")
    if binding_5493_sha256 != EXPECTED_BINDING_5493_SHA256:
        raise RuntimeError("checkpoint 5493 binding differs from source lock")
    if validation_5493_sha256 != EXPECTED_VALIDATION_5493_SHA256:
        raise RuntimeError("checkpoint 5493 validation differs from source lock")
    result_5492 = read_json(RESULT_5492)
    work_state_5492 = read_json(WORK_STATE_5492)
    leaf_rows_5492 = read_csv(LEAF_AUDIT_5492)
    result_5493 = read_json(RESULT_5493)
    validation_5493 = read_csv(VALIDATION_5493)
    source_register_5493 = read_csv(SOURCE_REGISTER_5493)
    binding = read_json(SCOPE_BINDING_5493)
    state = read_json(STATE_5484)
    cuboid = next(
        row
        for row in read_csv(MANIFEST_5468)
        if row["cuboid_job_id"] == TARGET_CUBOID_ID
    )
    target_candidates = [
        row
        for row in state["refinement_witnesses"]
        if row.get("refinement_path") == TARGET_REFINEMENT_PATH
    ]
    if len(target_candidates) != 1:
        raise RuntimeError(f"expected one target witness, found {len(target_candidates)}")
    target = target_candidates[0]
    stable, _, cells, support_segments, branches = base_5467.load_parent()
    certificate_parent = base_5490.fresh_v56(
        base_5467,
        base_5472,
        base_5474,
        base_5476,
        base_5478,
        base_5483,
    )
    certificate = base_5493.build_certificate(
        certificate_parent,
        result_5492,
        work_state_5492,
        leaf_rows_5492,
    )
    parent, evaluate_v54 = fresh_v57_with_v54_handle(
        base_5467,
        base_5472,
        base_5474,
        base_5476,
        base_5478,
        base_5483,
        base_5493,
        binding,
        certificate,
    )
    parent = install_path_failure_capture(parent)
    target_result = base_5469.evaluate_node(
        base_5468,
        stable,
        parent,
        cells,
        support_segments,
        branches,
        cuboid,
        target,
    )
    target_v57_audit = list(parent.V57_SCOPED_CERTIFICATE_AUDIT_ROWS)
    captured = parent.V57_STABLE_EDGE_CAPTURE
    if captured is None:
        raise RuntimeError("post-certificate target produced no stable-edge capture")
    v55_rows = list(parent.V55_STABLE_EDGE_XT_LEAF_UNION_AUDIT_ROWS)
    failed_leaf = finest_failed_leaf(v55_rows)
    axis_rows = axis_ablation(
        parent,
        evaluate_v54,
        captured["arguments"],
        failed_leaf,
    )
    passing_axes = [row for row in axis_rows if row["status"] == "PASS"]
    selected = min(
        passing_axes,
        key=lambda row: (int(row["count"]), AXES.index(row["axis"])),
    ) if passing_axes else None
    target_failure_reproduced = (
        not truth(target_result.get("probe_passed"))
        and target_result.get("failure_type") == "IntervalSingularity"
        and EXPECTED_FAILURE_MARKER
        in str(target_result.get("failure_message", ""))
    )
    schedule_rows = [row for row in v55_rows if row["row_type"] == "schedule"]
    if selected:
        decision = "POST_CERTIFICATE_STABLE_EDGE_SINGLE_AXIS_FOUND__BUILD_PARENT_V58_GATE"
        next_target = "BUILD_PARENT_V58_COMPLETE_AMPLITUDE_AXIS_COVER_GATE"
    else:
        decision = "POST_CERTIFICATE_STABLE_EDGE_SINGLE_AXIS_NOT_FOUND__TEST_PAIRED_COVER"
        next_target = "DERIVE_PAIRED_AXIS_COMPLETE_AMPLITUDE_COVER"
    payload: dict[str, Any] = {
        "checkpoint": CHECKPOINT,
        "revision": REVISION,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "decision": decision,
        "target_refinement_path": TARGET_REFINEMENT_PATH,
        "target_stable_edge_failure_reproduced": target_failure_reproduced,
        "v57_certificate_application_count": len(target_v57_audit),
        "axis_probe_certificate_application_count": len(
            parent.V57_SCOPED_CERTIFICATE_AUDIT_ROWS
        )
        - len(target_v57_audit),
        "v55_audit_row_count": len(v55_rows),
        "v55_schedule_row_count": len(schedule_rows),
        "failed_leaf_x_count": int(failed_leaf["x_count"]),
        "failed_leaf_t_count": int(failed_leaf["t_count"]),
        "failed_leaf_x_index": int(failed_leaf["x_index"]),
        "failed_leaf_t_index": int(failed_leaf["t_index"]),
        "failed_leaf_x_lower": float(failed_leaf["x_lower"]),
        "failed_leaf_x_upper": float(failed_leaf["x_upper"]),
        "failed_leaf_t_lower": float(failed_leaf["t_lower"]),
        "failed_leaf_t_upper": float(failed_leaf["t_upper"]),
        "axis_audit_row_count": len(axis_rows),
        "selected_axis": selected["axis"] if selected else "",
        "selected_axis_count": int(selected["count"]) if selected else 0,
        "selected_axis_amplitude_denominator_abs_lower": (
            float(selected["minimum_amplitude_denominator_abs_lower"])
            if selected
            else 0.0
        ),
        "selected_axis_collision_jacobian_abs_lower": (
            float(selected["minimum_collision_jacobian_abs_lower"])
            if selected
            else 0.0
        ),
        "source_state_5484_sha256": state_sha256,
        "source_result_5493_sha256": result_5493_sha256,
        "source_binding_5493_sha256": binding_5493_sha256,
        "parent_action_changed": False,
        "valid_for_parent_v58_stable_edge_axis_cover": False,
        "valid_for_parent_v57_active_cuboid": False,
        "valid_for_full_outer_parent_leaf_enclosure": False,
        "valid_for_D4_event_local_W3_bound": False,
        "valid_for_all_operator_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
        "next_target": next_target,
    }
    axis_numeric = bool(axis_rows) and all(
        row["status"] in {"PASS", "FAIL"}
        and math.isfinite(float(row["runtime_seconds"]))
        and float(row["runtime_seconds"]) >= 0.0
        for row in axis_rows
    )
    outcome_consistent = bool(selected) == bool(passing_axes)
    after_formalization = base_5467.formalization_snapshot()
    validations = [
        check("all_sources_exist", not missing, len(source_paths())),
        check(
            "checkpoint_5493_sources_are_hash_locked",
            state_sha256 == EXPECTED_STATE_SHA256
            and result_5493_sha256 == EXPECTED_RESULT_5493_SHA256
            and binding_5493_sha256 == EXPECTED_BINDING_5493_SHA256
            and validation_5493_sha256 == EXPECTED_VALIDATION_5493_SHA256
            and source_register_is_current(source_register_5493),
            result_5493_sha256,
        ),
        check(
            "checkpoint_5493_has_only_the_expected_target_gate_failure",
            int(result_5493.get("failed_validation_count", -1)) == 1
            and sum(not truth(row["passed"]) for row in validation_5493) == 1
            and not truth(result_5493.get("target_v57_passed"))
            and truth(result_5493.get("control_v56_v57_identical")),
            result_5493.get("decision"),
        ),
        check(
            "post_certificate_stable_edge_failure_is_reproduced",
            target_failure_reproduced,
            target_result.get("failure_message", ""),
        ),
        check(
            "scoped_collision_certificate_applies_before_stable_failure",
            len(target_v57_audit) == 1
            and target_v57_audit[0]["status"] == "APPLIED",
            len(target_v57_audit),
        ),
        check(
            "inherited_v55_schedule_failure_is_fully_audited",
            bool(schedule_rows)
            and all(row["status"] == "FAIL" for row in schedule_rows)
            and bool(v55_rows),
            len(v55_rows),
        ),
        check(
            "finest_failed_leaf_is_source_bounded",
            float(failed_leaf["x_upper"]) > float(failed_leaf["x_lower"])
            and float(failed_leaf["t_upper"]) > float(failed_leaf["t_lower"]),
            f"X{failed_leaf['x_count']}T{failed_leaf['t_count']}",
        ),
        check("single_axis_ablation_is_numeric", axis_numeric, len(axis_rows)),
        check("axis_outcome_is_internally_consistent", outcome_consistent, decision),
        check(
            "diagnostic_is_not_misreported_as_parent_v58_pass",
            not payload["valid_for_parent_v58_stable_edge_axis_cover"]
            and not payload["valid_for_parent_v57_active_cuboid"],
            "candidate axis only",
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
            "post-certificate stable-edge diagnostic only",
        ),
    ]
    payload["validation_row_count"] = len(validations)
    payload["failed_validation_count"] = sum(not row["passed"] for row in validations)
    OUTPUT.mkdir(parents=True, exist_ok=True)
    base_5467.atomic_csv(V55_AUDIT, v55_rows)
    base_5467.atomic_csv(AXIS_AUDIT, axis_rows)
    base_5467.atomic_csv(
        V57_AUDIT,
        target_v57_audit,
    )
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
                    "target_stable_edge_failure_reproduced",
                    "v55_schedule_row_count",
                    "failed_leaf_x_count",
                    "failed_leaf_t_count",
                    "failed_leaf_x_index",
                    "failed_leaf_t_index",
                    "axis_audit_row_count",
                    "selected_axis",
                    "selected_axis_count",
                    "selected_axis_amplitude_denominator_abs_lower",
                    "selected_axis_collision_jacobian_abs_lower",
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
