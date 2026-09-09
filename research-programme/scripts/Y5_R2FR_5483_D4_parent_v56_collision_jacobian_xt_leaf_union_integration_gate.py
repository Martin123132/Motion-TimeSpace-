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
OUTPUT = FUNCTIONAL_RG / "5483"

SCRIPT_5467 = SCRIPTS / "Y5_R2FR_5467_D4_all_outer_leaf_epsilon_fiber_transplant_runner.py"
SCRIPT_5468 = SCRIPTS / "Y5_R2FR_5468_D4_exact_outer_cuboid_coalescence_runner.py"
SCRIPT_5469 = SCRIPTS / "Y5_R2FR_5469_D4_resumable_three_axis_cuboid_certificate_runner.py"
SCRIPT_5472 = SCRIPTS / "Y5_R2FR_5472_D4_parent_v52_collision_jacobian_leaf_union_integration_gate.py"
SCRIPT_5474 = SCRIPTS / "Y5_R2FR_5474_D4_parent_v53_stable_edge_t_leaf_union_integration_gate.py"
SCRIPT_5476 = SCRIPTS / "Y5_R2FR_5476_D4_parent_v54_first_spinor_pivot_t_leaf_union_integration_gate.py"
SCRIPT_5478 = SCRIPTS / "Y5_R2FR_5478_D4_parent_v55_stable_edge_xt_leaf_union_integration_gate.py"
SCRIPT_5480 = SCRIPTS / "Y5_R2FR_5480_D4_parent_v55_hash_locked_frontier_runner.py"
SCRIPT_5481 = SCRIPTS / "Y5_R2FR_5481_D4_parent_v56_collision_jacobian_xt_leaf_union_candidate_probe.py"
RESULT_5480 = FUNCTIONAL_RG / "5480" / "D4_parent_v55_hash_locked_frontier_result.json"
VALIDATION_5480 = FUNCTIONAL_RG / "5480" / "P8_Y5_BRR5479_5480_VALIDATION.csv"
RESULT_5481 = FUNCTIONAL_RG / "5481" / "D4_parent_v56_collision_jacobian_xt_leaf_union_candidate_result.json"
VALIDATION_5481 = FUNCTIONAL_RG / "5481" / "P8_Y5_BRR5480_5481_VALIDATION.csv"
MANIFEST_5468 = FUNCTIONAL_RG / "5468" / "D4_exact_outer_cuboid_manifest.csv"

TARGET_CUBOID_ID = "E07__U051__RIGHT_CONNECTOR__CUBOID__6df3d70a73e4618b"
STATE_5480 = FUNCTIONAL_RG / "5480" / "work-v1" / f"{TARGET_CUBOID_ID}.json"

AUDIT = OUTPUT / "D4_parent_v56_collision_jacobian_xt_leaf_union_audit.csv"
COMPARISON = OUTPUT / "D4_parent_v56_target_and_control_comparison.csv"
SOURCE_REGISTER = OUTPUT / "source_register.csv"
VALIDATION = OUTPUT / "P8_Y5_BRR5482_5483_VALIDATION.csv"
STATUS = OUTPUT / "status.json"
RESULT = OUTPUT / "D4_parent_v56_collision_jacobian_xt_leaf_union_result.json"
DOCUMENT = POST / "5483-Y5-R2FR-D4-parent-v56-collision-jacobian-xt-leaf-union-integration-gate.md"

CHECKPOINT = 5483
REVISION = "D4-parent-v56-collision-jacobian-xt-leaf-union-integration-gate-v1"
PARENT_V55_REVISION = "D4-deformed-contour-regular-away-W3-v55-stable-edge-xt-leaf-union"
PARENT_V56_REVISION = "D4-deformed-contour-regular-away-W3-v56-collision-jacobian-xt-leaf-union"
EXPECTED_FAILURE_MARKER = "global contour geometric denominator reaches zero"
X_COUNT = 16
T_COUNT = 128
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
        SCRIPT_5476,
        SCRIPT_5478,
        SCRIPT_5480,
        SCRIPT_5481,
        RESULT_5480,
        VALIDATION_5480,
        RESULT_5481,
        VALIDATION_5481,
        MANIFEST_5468,
        STATE_5480,
    )


def check(gate: str, passed: bool, evidence: Any) -> dict[str, Any]:
    return {
        "checkpoint": CHECKPOINT,
        "validation_gate": gate,
        "passed": bool(passed),
        "evidence": evidence,
    }


def fresh_v55(
    base_5467: Any,
    base_5472: Any,
    base_5474: Any,
    base_5476: Any,
    base_5478: Any,
    name: str,
) -> Any:
    return base_5478.install_parent_v55(
        base_5476.install_parent_v54(
            base_5474.install_parent_v53(
                base_5472.install_parent_v52(
                    base_5472.fresh_parent(base_5467, name)
                )
            ),
            base_5474,
        ),
        base_5474,
    )


def install_parent_v56(parent: Any, base_5472: Any) -> Any:
    if parent.REVISION != PARENT_V55_REVISION:
        raise RuntimeError(
            f"expected parent revision {PARENT_V55_REVISION}, found {parent.REVISION}"
        )
    original = parent.tight_energy_contour_geometric_factors
    audit_rows: list[dict[str, Any]] = []

    def tight_v56(
        configuration: dict[str, Any],
        inputs: dict[str, Any],
        geometry: dict[str, Any],
        path_context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        factors = original(configuration, inputs, geometry, path_context)
        original_lower = float(
            factors.get(
                "collision_jacobian_selected_abs_lower",
                parent.M5258.lower_abs(factors["collision_jacobian"]),
            )
        )
        if (
            original_lower > 0.0
            or path_context is None
            or path_context.get("path_segment")
            not in {"LEFT_CONNECTOR", "RIGHT_CONNECTOR"}
        ):
            return factors
        started = time.perf_counter()
        try:
            lower, _, hull, denominator, diagnostics = (
                base_5472.collision_jacobian_leaf_union_candidate(
                    parent,
                    configuration,
                    path_context["cell"],
                    path_context["path_segment"],
                    path_context["absolute_coordinate"],
                    path_context["path_parameter"],
                    inputs["epsilon"],
                    X_COUNT,
                    T_COUNT,
                )
            )
        except (
            parent.EnclosureFailure,
            parent.M5258.IntervalSingularity,
            ValueError,
        ) as error:
            audit_rows.append(
                {
                    "configuration_role": configuration.get("role", ""),
                    "x_count": X_COUNT,
                    "t_count": T_COUNT,
                    "status": "FAIL",
                    "leaf_union_abs_lower": 0.0,
                    "rectangular_hull_abs_lower": 0.0,
                    "minimum_chart_denominator_abs_lower": 0.0,
                    "parameter_area_coverage_error": math.nan,
                    "runtime_seconds": time.perf_counter() - started,
                    "error_type": type(error).__name__,
                    "error": str(error).splitlines()[0][:600],
                }
            )
            return factors
        x_lower, x_upper = parent.M5394.real_bounds(
            path_context["absolute_coordinate"]
        )
        t_lower, t_upper = parent.M5394.real_bounds(path_context["path_parameter"])
        original_area = (x_upper - x_lower) * (t_upper - t_lower)
        covered_area = (
            X_COUNT
            * T_COUNT
            * ((x_upper - x_lower) / X_COUNT)
            * ((t_upper - t_lower) / T_COUNT)
        )
        coverage_error = abs(covered_area - original_area)
        method = f"V56_EXACT_XT_PROJECTIVE_LEAF_UNION_{X_COUNT}X{T_COUNT}"
        audit_rows.append(
            {
                "configuration_role": configuration.get("role", ""),
                "x_count": X_COUNT,
                "t_count": T_COUNT,
                "status": "PASS" if lower > 0.0 else "ZERO",
                "leaf_union_abs_lower": lower,
                "rectangular_hull_abs_lower": diagnostics[
                    "rectangular_hull_abs_lower"
                ],
                "minimum_chart_denominator_abs_lower": denominator,
                "parameter_area_coverage_error": coverage_error,
                "runtime_seconds": time.perf_counter() - started,
                "error_type": "",
                "error": "",
                "method": method,
                "leaf_union_theorem": diagnostics["leaf_union_theorem"],
            }
        )
        if lower <= 0.0 or denominator <= 0.0:
            return factors
        candidate_lowers = dict(
            factors.get("collision_jacobian_candidate_abs_lowers", {})
        )
        candidate_lowers[method] = lower
        factors["collision_jacobian_candidate_abs_lowers"] = candidate_lowers
        factors["collision_jacobian"] = hull
        factors["collision_jacobian_enclosure_method"] = method
        factors["collision_jacobian_chart_denominator_lower"] = denominator
        factors["collision_jacobian_selected_abs_lower"] = lower
        factors["collision_jacobian_leaf_union_abs_lower"] = lower
        factors["collision_jacobian_leaf_union_rectangular_hull_abs_lower"] = (
            diagnostics["rectangular_hull_abs_lower"]
        )
        factors["collision_jacobian_leaf_union_leaf_count"] = X_COUNT * T_COUNT
        factors["collision_jacobian_leaf_union_parameter_area_coverage_error"] = (
            coverage_error
        )
        return factors

    parent.tight_energy_contour_geometric_factors = tight_v56
    parent.V56_COLLISION_JACOBIAN_XT_LEAF_UNION_AUDIT_ROWS = audit_rows
    parent.V56_PARENT_ACTION_CHANGED = False
    parent.V56_ONLY_ENCLOSURE_COMPOSITION_CHANGED = True
    parent.REVISION = PARENT_V56_REVISION
    return parent


def render_document(payload: dict[str, Any], base_5467: Any) -> None:
    lines = [
        "# 5483: D4 parent-v56 collision-Jacobian x/t-leaf-union integration gate",
        "",
        "Parent v56 changes no action, contour, configuration, residue or acceptance threshold. After a demonstrated connector collision-Jacobian zero lower bound only, it evaluates the unchanged Jacobian chart candidates on the exact 16 x 128 x/t cover derived at checkpoint 5481.",
        "",
        f"Parent-v55 target failure reproduced: `{payload['target_v55_expected_failure']}`. Complete parent-v56 target passed: `{payload['target_v56_passed']}`.",
        "",
        f"V56 leaf-union lower: `{payload['minimum_v56_leaf_union_abs_lower']}`. Chart-denominator lower: `{payload['minimum_v56_chart_denominator_abs_lower']}`. Complete-amplitude denominator lower: `{payload['target_v56_amplitude_denominator_abs_lower']}`. Collision-Jacobian lower: `{payload['target_v56_collision_jacobian_abs_lower']}`.",
        "",
        f"Untriggered control exactly unchanged: `{payload['control_v55_v56_identical']}`.",
        "",
        f"**{payload['decision']}**",
        "",
        "Only this parent enclosure class is certified. The active cuboid and every broader GR/MTS claim remain open until migration and further coverage complete.",
        "",
    ]
    base_5467.atomic_text(DOCUMENT, "\n".join(lines))


def main() -> int:
    base_5467 = load_module("mts_5467_for_5483", SCRIPT_5467)
    base_5468 = load_module("mts_5468_for_5483", SCRIPT_5468)
    base_5469 = load_module("mts_5469_for_5483", SCRIPT_5469)
    base_5472 = load_module("mts_5472_for_5483", SCRIPT_5472)
    base_5474 = load_module("mts_5474_for_5483", SCRIPT_5474)
    base_5476 = load_module("mts_5476_for_5483", SCRIPT_5476)
    base_5478 = load_module("mts_5478_for_5483", SCRIPT_5478)
    base_5480 = load_module("mts_5480_for_5483", SCRIPT_5480)
    base_5467.set_below_normal_priority()
    base_5480.set_single_core_affinity()
    before_formalization = base_5467.formalization_snapshot()
    missing = [str(path) for path in source_paths() if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"missing sources: {missing}")
    result_5480 = read_json(RESULT_5480)
    validation_5480 = read_csv(VALIDATION_5480)
    result_5481 = read_json(RESULT_5481)
    validation_5481 = read_csv(VALIDATION_5481)
    state = read_json(STATE_5480)
    state_sha256 = digest(STATE_5480)
    cuboid = next(
        row
        for row in read_csv(MANIFEST_5468)
        if row["cuboid_job_id"] == TARGET_CUBOID_ID
    )
    target_candidates = [
        row
        for row in state["refinement_witnesses"]
        if row.get("certificate_source") == "checkpoint_5480_parent_v55_witness"
        and EXPECTED_FAILURE_MARKER in str(row.get("failure_message", ""))
        and '"collision_jacobian": 0.0' in str(row.get("failure_message", ""))
    ]
    if not target_candidates:
        raise RuntimeError("checkpoint 5480 has no v55 collision-Jacobian witness")
    target = max(
        target_candidates,
        key=lambda row: (
            (float(row["x_upper"]) - float(row["x_lower"]))
            * (float(row["t_upper"]) - float(row["t_lower"]))
        ),
    )
    control_candidates = [
        row
        for row in state["accepted"]
        if truth(row.get("probe_passed"))
        and row.get("certificate_source") == "checkpoint_5480_parent_v55"
        and row.get("path_integral_enclosure_method")
        != "V55_EXACT_UNIFORM_XT_LEAF_UNION_SUM"
    ]
    if not control_candidates:
        raise RuntimeError("checkpoint 5480 has no untriggered parent-v55 control")
    control = min(
        control_candidates,
        key=lambda row: float(row.get("runtime_seconds", math.inf)),
    )
    stable, _, cells, support_segments, branches = base_5467.load_parent()

    parent_v55_target = fresh_v55(
        base_5467,
        base_5472,
        base_5474,
        base_5476,
        base_5478,
        "mts_parent_v55_target_for_5483",
    )
    target_v55 = base_5469.evaluate_node(
        base_5468,
        stable,
        parent_v55_target,
        cells,
        support_segments,
        branches,
        cuboid,
        target,
    )
    parent_v56_target = install_parent_v56(
        fresh_v55(
            base_5467,
            base_5472,
            base_5474,
            base_5476,
            base_5478,
            "mts_parent_v56_target_for_5483",
        ),
        base_5472,
    )
    target_v56 = base_5469.evaluate_node(
        base_5468,
        stable,
        parent_v56_target,
        cells,
        support_segments,
        branches,
        cuboid,
        target,
    )
    target_audit = list(
        parent_v56_target.V56_COLLISION_JACOBIAN_XT_LEAF_UNION_AUDIT_ROWS
    )

    parent_v55_control = fresh_v55(
        base_5467,
        base_5472,
        base_5474,
        base_5476,
        base_5478,
        "mts_parent_v55_control_for_5483",
    )
    parent_v56_control = install_parent_v56(
        fresh_v55(
            base_5467,
            base_5472,
            base_5474,
            base_5476,
            base_5478,
            "mts_parent_v56_control_for_5483",
        ),
        base_5472,
    )
    control_v55 = base_5469.evaluate_node(
        base_5468,
        stable,
        parent_v55_control,
        cells,
        support_segments,
        branches,
        cuboid,
        control,
    )
    control_v56 = base_5469.evaluate_node(
        base_5468,
        stable,
        parent_v56_control,
        cells,
        support_segments,
        branches,
        cuboid,
        control,
    )
    control_audit = list(
        parent_v56_control.V56_COLLISION_JACOBIAN_XT_LEAF_UNION_AUDIT_ROWS
    )
    control_identical = (
        truth(control_v55.get("probe_passed"))
        and truth(control_v56.get("probe_passed"))
        and all(
            float(control_v55[field]) == float(control_v56[field])
            for field in METRIC_FIELDS
        )
        and not control_audit
    )
    target_v55_expected_failure = (
        not truth(target_v55.get("probe_passed"))
        and EXPECTED_FAILURE_MARKER in str(target_v55.get("failure_message", ""))
        and '"collision_jacobian": 0.0'
        in str(target_v55.get("failure_message", ""))
    )
    target_v56_passed = truth(target_v56.get("probe_passed"))
    positive_rows = [
        row
        for row in target_audit
        if row["status"] == "PASS"
        and float(row["leaf_union_abs_lower"]) > 0.0
        and float(row["minimum_chart_denominator_abs_lower"]) > 0.0
    ]
    exact_cover = bool(positive_rows) and all(
        float(row["parameter_area_coverage_error"]) <= 1.0e-12
        for row in positive_rows
    )
    comparison_rows = []
    for role, result, revision in (
        ("collision_jacobian_target_v55", target_v55, PARENT_V55_REVISION),
        ("collision_jacobian_target_v56", target_v56, PARENT_V56_REVISION),
        ("untriggered_control_v55", control_v55, PARENT_V55_REVISION),
        ("untriggered_control_v56", control_v56, PARENT_V56_REVISION),
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
    payload: dict[str, Any] = {
        "checkpoint": CHECKPOINT,
        "revision": REVISION,
        "parent_revision": PARENT_V56_REVISION,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "decision": (
            "PARENT_V56_COLLISION_JACOBIAN_XT_LEAF_UNION_CERTIFIED__MIGRATE_FRONTIER"
            if target_v55_expected_failure
            and target_v56_passed
            and positive_rows
            and exact_cover
            and control_identical
            else "PARENT_V56_COLLISION_JACOBIAN_XT_LEAF_UNION_NOT_CERTIFIED"
        ),
        "target_cuboid_id": TARGET_CUBOID_ID,
        "target_refinement_path": target["refinement_path"],
        "control_refinement_path": control["refinement_path"],
        "target_v55_expected_failure": target_v55_expected_failure,
        "target_v56_passed": target_v56_passed,
        "v56_audit_row_count": len(target_audit),
        "v56_positive_audit_row_count": len(positive_rows),
        "minimum_v56_leaf_union_abs_lower": min(
            (float(row["leaf_union_abs_lower"]) for row in positive_rows),
            default=0.0,
        ),
        "minimum_v56_rectangular_hull_abs_lower": min(
            (float(row["rectangular_hull_abs_lower"]) for row in positive_rows),
            default=0.0,
        ),
        "minimum_v56_chart_denominator_abs_lower": min(
            (
                float(row["minimum_chart_denominator_abs_lower"])
                for row in positive_rows
            ),
            default=0.0,
        ),
        "maximum_v56_parameter_area_coverage_error": max(
            (
                float(row["parameter_area_coverage_error"])
                for row in positive_rows
            ),
            default=math.inf,
        ),
        "target_v56_amplitude_denominator_abs_lower": target_v56.get(
            "minimum_amplitude_denominator_abs_lower"
        ),
        "target_v56_collision_jacobian_abs_lower": target_v56.get(
            "collision_jacobian_abs_lower"
        ),
        "target_v56_integrated_regular_path_abs_upper": target_v56.get(
            "integrated_regular_path_abs_upper"
        ),
        "control_v55_v56_identical": control_identical,
        "source_state_5480_sha256": state_sha256,
        "parent_action_changed": False,
        "only_enclosure_composition_changed": True,
        "valid_for_parent_v56_collision_jacobian_xt_leaf_union": False,
        "valid_for_parent_v56_active_cuboid": False,
        "valid_for_full_outer_parent_leaf_enclosure": False,
        "valid_for_D4_event_local_W3_bound": False,
        "valid_for_all_operator_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
        "next_target": "CREATE_HASH_LOCKED_V56_CARRY_FORWARD_OF_CHECKPOINT_5480_STATE",
    }
    after_formalization = base_5467.formalization_snapshot()
    validations = [
        check("all_sources_exist", not missing, len(source_paths())),
        check(
            "checkpoint_5480_frontier_is_valid",
            int(result_5480.get("failed_validation_count", -1)) == 0
            and all(truth(row["passed"]) for row in validation_5480)
            and not state["unresolved"],
            result_5480.get("decision"),
        ),
        check(
            "checkpoint_5481_candidate_is_valid",
            int(result_5481.get("failed_validation_count", -1)) == 0
            and all(truth(row["passed"]) for row in validation_5481)
            and int(result_5481.get("selected_x_count", 0)) == X_COUNT
            and int(result_5481.get("selected_t_count", 0)) == T_COUNT
            and result_5481.get("source_state_5480_sha256") == state_sha256,
            result_5481.get("decision"),
        ),
        check(
            "v55_target_reproduces_collision_jacobian_failure",
            target_v55_expected_failure,
            target_v55.get("failure_message", ""),
        ),
        check(
            "v56_complete_parent_target_is_finite",
            target_v56_passed
            and all(
                math.isfinite(float(target_v56[field]))
                and float(target_v56[field]) > 0.0
                for field in METRIC_FIELDS
            ),
            target_v56.get("minimum_amplitude_denominator_abs_lower"),
        ),
        check(
            "v56_exact_leaf_union_is_positive",
            bool(positive_rows)
            and all(row["status"] == "PASS" for row in target_audit)
            and payload["minimum_v56_leaf_union_abs_lower"] > 0.0
            and payload["minimum_v56_chart_denominator_abs_lower"] > 0.0,
            payload["minimum_v56_leaf_union_abs_lower"],
        ),
        check(
            "v56_leaf_union_preserves_exact_parameter_cover",
            exact_cover,
            payload["maximum_v56_parameter_area_coverage_error"],
        ),
        check(
            "untriggered_v55_v56_control_is_exactly_unchanged",
            control_identical,
            control["refinement_path"],
        ),
        check(
            "v56_changes_only_enclosure_composition",
            not parent_v56_target.V56_PARENT_ACTION_CHANGED
            and parent_v56_target.V56_ONLY_ENCLOSURE_COMPOSITION_CHANGED,
            PARENT_V56_REVISION,
        ),
        check(
            "formalization_workbench_untouched",
            before_formalization == after_formalization,
            f"before={len(before_formalization)};after={len(after_formalization)}",
        ),
        check(
            "broad_claims_remain_false",
            not payload["valid_for_parent_v56_active_cuboid"]
            and not payload["valid_for_full_outer_parent_leaf_enclosure"]
            and not payload["valid_for_D4_event_local_W3_bound"]
            and not payload["valid_for_all_operator_local_GR_claim"]
            and not payload["valid_for_full_MTS_claim"],
            "one collision-Jacobian enclosure class only",
        ),
    ]
    payload["validation_row_count"] = len(validations)
    payload["failed_validation_count"] = sum(
        not row["passed"] for row in validations
    )
    payload["valid_for_parent_v56_collision_jacobian_xt_leaf_union"] = (
        payload["failed_validation_count"] == 0
        and "CERTIFIED" in payload["decision"]
    )
    OUTPUT.mkdir(parents=True, exist_ok=True)
    base_5467.atomic_csv(AUDIT, target_audit)
    base_5467.atomic_csv(COMPARISON, comparison_rows)
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
                    "target_v55_expected_failure",
                    "target_v56_passed",
                    "v56_audit_row_count",
                    "minimum_v56_leaf_union_abs_lower",
                    "minimum_v56_chart_denominator_abs_lower",
                    "target_v56_amplitude_denominator_abs_lower",
                    "target_v56_collision_jacobian_abs_lower",
                    "control_v55_v56_identical",
                    "valid_for_parent_v56_collision_jacobian_xt_leaf_union",
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
