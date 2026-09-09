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
OUTPUT = FUNCTIONAL_RG / "5472"

SCRIPT_5467 = SCRIPTS / "Y5_R2FR_5467_D4_all_outer_leaf_epsilon_fiber_transplant_runner.py"
SCRIPT_5468 = SCRIPTS / "Y5_R2FR_5468_D4_exact_outer_cuboid_coalescence_runner.py"
SCRIPT_5469 = SCRIPTS / "Y5_R2FR_5469_D4_resumable_three_axis_cuboid_certificate_runner.py"
PARENT_V51 = SCRIPTS / "Y5_R2FR_5396_D4_deformed_contour_regular_away_W3.py"
MANIFEST_5468 = FUNCTIONAL_RG / "5468" / "D4_exact_outer_cuboid_manifest.csv"
TARGET_SNAPSHOT_5470 = FUNCTIONAL_RG / "5470" / "target_unresolved_node_snapshot.json"
RESULT_5470 = FUNCTIONAL_RG / "5470" / "D4_unresolved_collision_jacobian_leaf_union_result.json"
VALIDATION_5470 = FUNCTIONAL_RG / "5470" / "P8_Y5_BRR5469_5470_VALIDATION.csv"
CONTROL_LEAF_5471 = FUNCTIONAL_RG / "5471" / "work-v1" / "T000_OF_128.json"

AUDIT_ROWS = OUTPUT / "D4_parent_v52_collision_jacobian_leaf_union_audit.csv"
COMPARISON = OUTPUT / "D4_parent_v52_target_and_control_comparison.csv"
SOURCE_REGISTER = OUTPUT / "source_register.csv"
VALIDATION = OUTPUT / "P8_Y5_BRR5471_5472_VALIDATION.csv"
STATUS = OUTPUT / "status.json"
RESULT = OUTPUT / "D4_parent_v52_collision_jacobian_leaf_union_result.json"
DOCUMENT = POST / "5472-Y5-R2FR-D4-parent-v52-collision-jacobian-leaf-union-integration-gate.md"

CHECKPOINT = 5472
REVISION = "D4-parent-v52-collision-jacobian-leaf-union-integration-gate-v1"
PARENT_V51_REVISION = "D4-deformed-contour-regular-away-W3-v51"
PARENT_V52_REVISION = "D4-deformed-contour-regular-away-W3-v52-leaf-union"
TARGET_CUBOID_ID = "E07__U051__RIGHT_CONNECTOR__CUBOID__6df3d70a73e4618b"
LEAF_UNION_SCHEDULE = ((1, 128), (1, 256), (2, 128))


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
        PARENT_V51,
        MANIFEST_5468,
        TARGET_SNAPSHOT_5470,
        RESULT_5470,
        VALIDATION_5470,
        CONTROL_LEAF_5471,
    )


def collision_jacobian_leaf_union_candidate(
    parent: Any,
    configuration: dict[str, Any],
    cell: dict[str, Any],
    path_segment: str,
    absolute_coordinate: Any,
    path_parameter: Any,
    epsilon: Any,
    x_count: int,
    t_count: int,
) -> tuple[float, str, Any, float, dict[str, Any]]:
    if x_count < 1 or t_count < 1 or x_count * t_count <= 1:
        raise ValueError("leaf-union cover requires at least two leaves")
    x_lower, x_upper = parent.M5394.real_bounds(absolute_coordinate)
    t_lower, t_upper = parent.M5394.real_bounds(path_parameter)
    jacobians: list[Any] = []
    leaf_lowers: list[float] = []
    denominator_lowers: list[float] = []
    method_counts: dict[str, int] = {}
    for x_index in range(x_count):
        coordinate = parent.cbox(
            x_lower + (x_upper - x_lower) * x_index / x_count,
            x_lower + (x_upper - x_lower) * (x_index + 1) / x_count,
        )
        for t_index in range(t_count):
            parameter = parent.cbox(
                t_lower + (t_upper - t_lower) * t_index / t_count,
                t_lower + (t_upper - t_lower) * (t_index + 1) / t_count,
            )
            local_candidates = [
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
            if not local_candidates:
                raise parent.M5258.IntervalSingularity(
                    "leaf-union collision Jacobian has an uncovered chart box"
                )
            selected = max(
                local_candidates,
                key=lambda candidate: (candidate[0], candidate[3]),
            )
            jacobians.append(selected[2])
            leaf_lowers.append(float(selected[0]))
            denominator_lowers.append(float(selected[3]))
            method_counts[selected[1]] = method_counts.get(selected[1], 0) + 1
    hull = parent.rectangular_interval_hull(jacobians)
    leaf_union_lower = min(leaf_lowers)
    hull_lower = parent.M5258.lower_abs(hull)
    method = f"V52_PATH_ONLY_PROJECTIVE_LEAF_UNION_{x_count}X{t_count}"
    diagnostics = {
        "method": method,
        "x_count": x_count,
        "t_count": t_count,
        "leaf_count": x_count * t_count,
        "leaf_union_abs_lower": leaf_union_lower,
        "rectangular_hull_abs_lower": hull_lower,
        "minimum_chart_denominator_abs_lower": min(denominator_lowers),
        "method_counts": json.dumps(
            method_counts, sort_keys=True, separators=(",", ":")
        ),
        "leaf_union_theorem": (
            "D=union_i D_i and 0 notin J(D_i) for all i implies "
            "inf_D|J|>=min_i dist(0,J(D_i))"
        ),
    }
    return (
        leaf_union_lower,
        method,
        hull,
        min(denominator_lowers),
        diagnostics,
    )


def install_parent_v52(parent: Any) -> Any:
    if parent.REVISION != PARENT_V51_REVISION:
        raise RuntimeError(
            f"expected parent revision {PARENT_V51_REVISION}, found {parent.REVISION}"
        )
    original_tight = parent.tight_energy_contour_geometric_factors
    audit_rows: list[dict[str, Any]] = []

    def tight_v52(
        configuration: dict[str, Any],
        inputs: dict[str, Any],
        geometry: dict[str, Any],
        path_context: dict[str, Any] | None = None,
    ) -> dict[str, Any]:
        factors = original_tight(configuration, inputs, geometry, path_context)
        original_lower = float(
            factors.get(
                "collision_jacobian_selected_abs_lower",
                parent.M5258.lower_abs(factors["collision_jacobian"]),
            )
        )
        if original_lower > 0.0 or path_context is None:
            return factors
        for x_count, t_count in LEAF_UNION_SCHEDULE:
            started = time.perf_counter()
            try:
                lower, method, hull, denominator, diagnostics = (
                    collision_jacobian_leaf_union_candidate(
                        parent,
                        configuration,
                        path_context["cell"],
                        path_context["path_segment"],
                        path_context["absolute_coordinate"],
                        path_context["path_parameter"],
                        inputs["epsilon"],
                        x_count,
                        t_count,
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
                        "x_count": x_count,
                        "t_count": t_count,
                        "status": "FAIL",
                        "leaf_union_abs_lower": 0.0,
                        "rectangular_hull_abs_lower": 0.0,
                        "minimum_chart_denominator_abs_lower": 0.0,
                        "runtime_seconds": time.perf_counter() - started,
                        "error_type": type(error).__name__,
                        "error": str(error).splitlines()[0][:600],
                    }
                )
                continue
            audit_rows.append(
                {
                    "configuration_role": configuration.get("role", ""),
                    "status": "PASS" if lower > 0.0 else "ZERO",
                    "runtime_seconds": time.perf_counter() - started,
                    "error_type": "",
                    "error": "",
                    **diagnostics,
                }
            )
            candidate_lowers = dict(
                factors.get("collision_jacobian_candidate_abs_lowers", {})
            )
            candidate_lowers[method] = lower
            factors["collision_jacobian_candidate_abs_lowers"] = candidate_lowers
            if lower <= 0.0:
                continue
            factors["collision_jacobian"] = hull
            factors["collision_jacobian_enclosure_method"] = method
            factors["collision_jacobian_chart_denominator_lower"] = denominator
            factors["collision_jacobian_selected_abs_lower"] = lower
            factors["collision_jacobian_leaf_union_abs_lower"] = lower
            factors["collision_jacobian_leaf_union_rectangular_hull_abs_lower"] = diagnostics[
                "rectangular_hull_abs_lower"
            ]
            factors["collision_jacobian_leaf_union_leaf_count"] = diagnostics[
                "leaf_count"
            ]
            break
        return factors

    parent.tight_energy_contour_geometric_factors = tight_v52
    parent.V52_COLLISION_JACOBIAN_LEAF_UNION_AUDIT_ROWS = audit_rows
    parent.V52_PARENT_ACTION_CHANGED = False
    parent.V52_ONLY_ENCLOSURE_COMPOSITION_CHANGED = True
    parent.REVISION = PARENT_V52_REVISION
    return parent


def fresh_parent(base_5467: Any, name: str) -> Any:
    parent = base_5467.load_module(name, PARENT_V51)
    parent.set_below_normal_priority()
    parent.iv.dps = parent.INTERVAL_DIGITS
    return parent


def check(gate: str, passed: bool, evidence: Any) -> dict[str, Any]:
    return {
        "checkpoint": CHECKPOINT,
        "validation_gate": gate,
        "passed": bool(passed),
        "evidence": evidence,
    }


def render_document(payload: dict[str, Any], base_5467: Any) -> None:
    lines = [
        "# 5472: D4 parent-v52 collision-Jacobian leaf-union integration gate",
        "",
        "## Derived enclosure law",
        "",
        "For a compact finite cover `D = union_i D_i`, interval certificates `J(D_i) subset B_i` with `0 notin B_i` imply `inf_D |J| >= min_i dist(0,B_i) > 0`. Replacing the finite image union by one rectangular hull is sufficient but not necessary and can reintroduce zero between disconnected image boxes.",
        "",
        "Parent v52 leaves the action, contour, configurations, residues and acceptance thresholds unchanged. It invokes a path-only leaf-union candidate only when every v51 collision-Jacobian candidate has zero lower bound. The interval hull is retained for diagnostics; the denominator uses the source-proved minimum over leaf images.",
        "",
        "## Result",
        "",
        f"Previously unresolved target passes v52: `{payload['target_v52_passed']}`. Collision-Jacobian lower bound: `{payload['target_v52_collision_jacobian_abs_lower']}`. Amplitude-denominator lower bound: `{payload['target_v52_amplitude_denominator_abs_lower']}`.",
        "",
        f"Untriggered passing control is unchanged: `{payload['control_v51_v52_identical']}`. V52 fallback rows: `{payload['v52_leaf_union_audit_row_count']}`.",
        "",
        "## Decision",
        "",
        f"**{payload['decision']}**",
        "",
        "## Claim boundary",
        "",
        "This validates a stricter implementation of the existing finite-union theorem for collision-Jacobian enclosure. It does not yet migrate the complete checkpoint-5469 frontier or certify the active cuboid, full outer cover, W3, regulator limit, local GR or full MTS.",
        "",
    ]
    base_5467.atomic_text(DOCUMENT, "\n".join(lines))


def main() -> int:
    base_5468 = load_module("mts_5468_for_5472", SCRIPT_5468)
    base_5469 = load_module("mts_5469_for_5472", SCRIPT_5469)
    base_5467 = load_module("mts_5467_for_5472", SCRIPT_5467)
    base_5467.set_below_normal_priority()
    before_formalization = base_5467.formalization_snapshot()
    missing = [str(path) for path in source_paths() if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"missing sources: {missing}")
    result_5470 = read_json(RESULT_5470)
    validation_5470 = read_csv(VALIDATION_5470)
    snapshot = read_json(TARGET_SNAPSHOT_5470)
    target_node = snapshot["unresolved_node"]
    control_node = read_json(CONTROL_LEAF_5471)
    cuboid = next(
        row
        for row in read_csv(MANIFEST_5468)
        if row["cuboid_job_id"] == TARGET_CUBOID_ID
    )
    stable, _, cells, support_segments, branches = base_5467.load_parent()
    parent_v51 = fresh_parent(base_5467, "mts_parent_v51_control_for_5472")
    parent_v52 = install_parent_v52(
        fresh_parent(base_5467, "mts_parent_v52_target_for_5472")
    )
    target_started = time.perf_counter()
    target_result = base_5469.evaluate_node(
        base_5468,
        stable,
        parent_v52,
        cells,
        support_segments,
        branches,
        cuboid,
        target_node,
    )
    target_runtime = time.perf_counter() - target_started
    target_audit = list(parent_v52.V52_COLLISION_JACOBIAN_LEAF_UNION_AUDIT_ROWS)
    parent_v52_control = install_parent_v52(
        fresh_parent(base_5467, "mts_parent_v52_control_for_5472")
    )
    control_v51 = base_5469.evaluate_node(
        base_5468,
        stable,
        parent_v51,
        cells,
        support_segments,
        branches,
        cuboid,
        control_node,
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
    metric_fields = (
        "integrated_regular_path_abs_upper",
        "minimum_amplitude_denominator_abs_lower",
        "relative_root_abs_lower",
        "selected_global_root_abs_lower",
        "collision_jacobian_abs_lower",
    )
    control_identical = (
        truth(control_v51.get("probe_passed"))
        and truth(control_v52.get("probe_passed"))
        and all(
            float(control_v51[field]) == float(control_v52[field])
            for field in metric_fields
        )
        and not parent_v52_control.V52_COLLISION_JACOBIAN_LEAF_UNION_AUDIT_ROWS
    )
    comparison_rows = [
        {
            "role": "previously_unresolved_target_v52",
            "probe_passed": truth(target_result.get("probe_passed")),
            "failure_type": target_result.get("failure_type", ""),
            "failure_message": target_result.get("failure_message", ""),
            **{field: target_result.get(field) for field in metric_fields},
            "runtime_seconds": target_runtime,
            "parent_revision": PARENT_V52_REVISION,
        },
        {
            "role": "passing_control_v51",
            "probe_passed": truth(control_v51.get("probe_passed")),
            "failure_type": control_v51.get("failure_type", ""),
            "failure_message": control_v51.get("failure_message", ""),
            **{field: control_v51.get(field) for field in metric_fields},
            "runtime_seconds": control_v51.get("runtime_seconds"),
            "parent_revision": PARENT_V51_REVISION,
        },
        {
            "role": "passing_control_v52",
            "probe_passed": truth(control_v52.get("probe_passed")),
            "failure_type": control_v52.get("failure_type", ""),
            "failure_message": control_v52.get("failure_message", ""),
            **{field: control_v52.get(field) for field in metric_fields},
            "runtime_seconds": control_v52.get("runtime_seconds"),
            "parent_revision": PARENT_V52_REVISION,
        },
    ]
    base_5467.atomic_csv(COMPARISON, comparison_rows)
    if target_audit:
        base_5467.atomic_csv(AUDIT_ROWS, target_audit)
    target_passed = truth(target_result.get("probe_passed"))
    leaf_union_rows = [
        row for row in target_audit if float(row.get("leaf_union_abs_lower", 0.0)) > 0.0
    ]
    after_formalization = base_5467.formalization_snapshot()
    payload: dict[str, Any] = {
        "checkpoint": CHECKPOINT,
        "revision": REVISION,
        "parent_v51_revision": PARENT_V51_REVISION,
        "parent_v52_revision": PARENT_V52_REVISION,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "decision": (
            "PARENT_V52_LEAF_UNION_ENCLOSURE_CERTIFIED__MIGRATE_RESUMABLE_FRONTIER"
            if target_passed and control_identical and leaf_union_rows
            else "PARENT_V52_LEAF_UNION_ENCLOSURE_OPEN__DO_NOT_MIGRATE"
        ),
        "target_cuboid_id": TARGET_CUBOID_ID,
        "target_refinement_path": target_node["refinement_path"],
        "target_v51_failure_source": target_node["failure_message"],
        "target_v52_passed": target_passed,
        "target_v52_failure_type": target_result.get("failure_type", ""),
        "target_v52_failure_message": target_result.get("failure_message", ""),
        "target_v52_runtime_seconds": target_runtime,
        "target_v52_amplitude_denominator_abs_lower": target_result.get(
            "minimum_amplitude_denominator_abs_lower"
        ),
        "target_v52_relative_root_abs_lower": target_result.get(
            "relative_root_abs_lower"
        ),
        "target_v52_selected_global_root_abs_lower": target_result.get(
            "selected_global_root_abs_lower"
        ),
        "target_v52_collision_jacobian_abs_lower": target_result.get(
            "collision_jacobian_abs_lower"
        ),
        "v52_leaf_union_audit_row_count": len(target_audit),
        "v52_positive_leaf_union_row_count": len(leaf_union_rows),
        "minimum_v52_leaf_union_abs_lower": min(
            (float(row["leaf_union_abs_lower"]) for row in leaf_union_rows),
            default=math.nan,
        ),
        "minimum_v52_leaf_union_chart_denominator_abs_lower": min(
            (
                float(row["minimum_chart_denominator_abs_lower"])
                for row in leaf_union_rows
            ),
            default=math.nan,
        ),
        "control_v51_v52_identical": control_identical,
        "parent_action_changed": False,
        "only_enclosure_composition_changed": True,
        "valid_for_parent_v52_leaf_union_enclosure": (
            target_passed and control_identical and bool(leaf_union_rows)
        ),
        "valid_for_full_outer_parent_leaf_enclosure": False,
        "valid_for_D4_event_local_W3_bound": False,
        "valid_for_all_operator_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
        "next_target": (
            "CREATE_HASH_LOCKED_V52_CARRY_FORWARD_OF_CHECKPOINT_5469_STATE"
            if target_passed and control_identical and leaf_union_rows
            else "DIAGNOSE_V52_TARGET_OR_CONTROL_FAILURE"
        ),
    }
    validations = [
        check("all_sources_exist", not missing, len(source_paths())),
        check(
            "checkpoint_5470_leaf_union_theorem_is_source_certified",
            truth(result_5470.get("valid_for_collision_jacobian_leaf_union"))
            and int(result_5470.get("failed_validation_count", -1)) == 0
            and all(truth(row["passed"]) for row in validation_5470),
            result_5470.get("decision"),
        ),
        check(
            "v52_changes_only_enclosure_composition",
            not parent_v52.V52_PARENT_ACTION_CHANGED
            and parent_v52.V52_ONLY_ENCLOSURE_COMPOSITION_CHANGED,
            PARENT_V52_REVISION,
        ),
        check(
            "previously_unresolved_target_passes_v52",
            target_passed,
            target_result.get("failure_message", ""),
        ),
        check(
            "target_uses_positive_leaf_union_candidate",
            bool(leaf_union_rows)
            and all(
                float(row["leaf_union_abs_lower"]) > 0.0
                and float(row["minimum_chart_denominator_abs_lower"]) > 0.0
                for row in leaf_union_rows
            ),
            len(leaf_union_rows),
        ),
        check(
            "untriggered_v51_v52_control_is_identical",
            control_identical,
            control_node["leaf_id"],
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
            "parent enclosure revision only",
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
            "source_role": "parent-v52-leaf-union-input",
        }
        for path in source_paths()
    ]
    base_5467.atomic_csv(SOURCE_REGISTER, register)
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
                    "target_v52_passed",
                    "target_v52_amplitude_denominator_abs_lower",
                    "target_v52_collision_jacobian_abs_lower",
                    "v52_leaf_union_audit_row_count",
                    "minimum_v52_leaf_union_abs_lower",
                    "control_v51_v52_identical",
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
