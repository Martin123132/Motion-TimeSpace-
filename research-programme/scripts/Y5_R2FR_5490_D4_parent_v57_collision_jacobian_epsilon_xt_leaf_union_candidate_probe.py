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
OUTPUT = FUNCTIONAL_RG / "5490"
FORMALIZATION = POST.parent / "formalization-workbench"

SCRIPT_5467 = SCRIPTS / "Y5_R2FR_5467_D4_all_outer_leaf_epsilon_fiber_transplant_runner.py"
SCRIPT_5468 = SCRIPTS / "Y5_R2FR_5468_D4_exact_outer_cuboid_coalescence_runner.py"
SCRIPT_5469 = SCRIPTS / "Y5_R2FR_5469_D4_resumable_three_axis_cuboid_certificate_runner.py"
SCRIPT_5472 = SCRIPTS / "Y5_R2FR_5472_D4_parent_v52_collision_jacobian_leaf_union_integration_gate.py"
SCRIPT_5474 = SCRIPTS / "Y5_R2FR_5474_D4_parent_v53_stable_edge_t_leaf_union_integration_gate.py"
SCRIPT_5476 = SCRIPTS / "Y5_R2FR_5476_D4_parent_v54_first_spinor_pivot_t_leaf_union_integration_gate.py"
SCRIPT_5478 = SCRIPTS / "Y5_R2FR_5478_D4_parent_v55_stable_edge_xt_leaf_union_integration_gate.py"
SCRIPT_5480 = SCRIPTS / "Y5_R2FR_5480_D4_parent_v55_hash_locked_frontier_runner.py"
SCRIPT_5483 = SCRIPTS / "Y5_R2FR_5483_D4_parent_v56_collision_jacobian_xt_leaf_union_integration_gate.py"
SCRIPT_5484 = SCRIPTS / "Y5_R2FR_5484_D4_parent_v56_hash_locked_frontier_runner.py"

MANIFEST_5468 = FUNCTIONAL_RG / "5468" / "D4_exact_outer_cuboid_manifest.csv"
RESULT_5483 = FUNCTIONAL_RG / "5483" / "D4_parent_v56_collision_jacobian_xt_leaf_union_result.json"
VALIDATION_5483 = FUNCTIONAL_RG / "5483" / "P8_Y5_BRR5482_5483_VALIDATION.csv"
RESULT_5484 = FUNCTIONAL_RG / "5484" / "D4_parent_v56_hash_locked_frontier_result.json"
VALIDATION_5484 = FUNCTIONAL_RG / "5484" / "P8_Y5_BRR5483_5484_VALIDATION.csv"
STATE_5484 = (
    FUNCTIONAL_RG
    / "5484"
    / "work-v1"
    / "E07__U051__RIGHT_CONNECTOR__CUBOID__6df3d70a73e4618b.json"
)

AUDIT = OUTPUT / "D4_parent_v57_collision_jacobian_epsilon_xt_leaf_union_candidate_audit.csv"
SOURCE_REGISTER = OUTPUT / "source_register.csv"
VALIDATION = OUTPUT / "P8_Y5_BRR5489_5490_VALIDATION.csv"
STATUS = OUTPUT / "status.json"
RESULT = OUTPUT / "D4_parent_v57_collision_jacobian_epsilon_xt_leaf_union_candidate_result.json"
DOCUMENT = POST / "5490-Y5-R2FR-D4-parent-v57-collision-jacobian-epsilon-xt-leaf-union-candidate-probe.md"

CHECKPOINT = 5490
REVISION = "D4-parent-v57-collision-jacobian-epsilon-xt-leaf-union-candidate-v1"
PARENT_V56_REVISION = "D4-deformed-contour-regular-away-W3-v56-collision-jacobian-xt-leaf-union"
PARENT_V57_REVISION = "D4-deformed-contour-regular-away-W3-v57-collision-jacobian-epsilon-xt-leaf-union-candidate"
TARGET_CUBOID_ID = "E07__U051__RIGHT_CONNECTOR__CUBOID__6df3d70a73e4618b"
TARGET_REFINEMENT_PATH = "R_E0S_E0S_E0S_E1S"
EXPECTED_STATE_SHA256 = "3f485d18bb2a55d3fda317091e58c0330166a7b5ae7e2185a82ab46602e23faa"
EXPECTED_FAILURE_MARKER = "global contour geometric denominator reaches zero"
X_COUNT = 16
T_COUNT = 128
EPSILON_COUNTS = (2, 4, 8, 16)


class PositiveCandidateFound(RuntimeError):
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
        SCRIPT_5484,
        MANIFEST_5468,
        RESULT_5483,
        VALIDATION_5483,
        RESULT_5484,
        VALIDATION_5484,
        STATE_5484,
    )


def check(gate: str, passed: bool, evidence: Any) -> dict[str, Any]:
    return {
        "checkpoint": CHECKPOINT,
        "validation_gate": gate,
        "passed": bool(passed),
        "evidence": evidence,
    }


def fresh_v56(
    base_5467: Any,
    base_5472: Any,
    base_5474: Any,
    base_5476: Any,
    base_5478: Any,
    base_5483: Any,
) -> Any:
    return base_5483.install_parent_v56(
        base_5478.install_parent_v55(
            base_5476.install_parent_v54(
                base_5474.install_parent_v53(
                    base_5472.install_parent_v52(
                        base_5472.fresh_parent(
                            base_5467,
                            "mts_parent_v57_candidate_5490",
                        )
                    )
                ),
                base_5474,
            ),
            base_5474,
        ),
        base_5472,
    )


def collision_jacobian_epsilon_xt_leaf_union_candidate(
    parent: Any,
    configuration: dict[str, Any],
    cell: dict[str, Any],
    path_segment: str,
    absolute_coordinate: Any,
    path_parameter: Any,
    epsilon: Any,
    epsilon_count: int,
    x_count: int,
    t_count: int,
) -> tuple[float, str, Any, float, dict[str, Any]]:
    if epsilon_count < 1 or x_count < 1 or t_count < 1:
        raise ValueError("epsilon/x/t subdivision counts must be positive")
    if epsilon_count * x_count * t_count <= 1:
        raise ValueError("leaf-union cover requires at least two leaves")
    epsilon_lower, epsilon_upper = parent.M5394.real_bounds(epsilon)
    epsilon_imaginary_lower, epsilon_imaginary_upper = (
        parent.M5394.imaginary_bounds(epsilon)
    )
    x_lower, x_upper = parent.M5394.real_bounds(absolute_coordinate)
    t_lower, t_upper = parent.M5394.real_bounds(path_parameter)
    jacobians: list[Any] = []
    leaf_lowers: list[float] = []
    denominator_lowers: list[float] = []
    method_counts: dict[str, int] = {}
    for epsilon_index in range(epsilon_count):
        epsilon_subbox = parent.cbox(
            epsilon_lower
            + (epsilon_upper - epsilon_lower) * epsilon_index / epsilon_count,
            epsilon_lower
            + (epsilon_upper - epsilon_lower)
            * (epsilon_index + 1)
            / epsilon_count,
            epsilon_imaginary_lower,
            epsilon_imaginary_upper,
        )
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
                        epsilon_subbox,
                    )
                    if candidate[3] > 0.0
                ]
                if not local_candidates:
                    raise parent.M5258.IntervalSingularity(
                        "epsilon/x/t leaf union has an uncovered collision-Jacobian chart box"
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
    method = (
        f"V57_EXACT_EPSILON_XT_PROJECTIVE_LEAF_UNION_"
        f"E{epsilon_count}X{x_count}T{t_count}"
    )
    original_volume = (
        (epsilon_upper - epsilon_lower)
        * (x_upper - x_lower)
        * (t_upper - t_lower)
    )
    covered_volume = (
        epsilon_count
        * x_count
        * t_count
        * ((epsilon_upper - epsilon_lower) / epsilon_count)
        * ((x_upper - x_lower) / x_count)
        * ((t_upper - t_lower) / t_count)
    )
    diagnostics = {
        "method": method,
        "epsilon_count": epsilon_count,
        "x_count": x_count,
        "t_count": t_count,
        "leaf_count": epsilon_count * x_count * t_count,
        "leaf_union_abs_lower": leaf_union_lower,
        "rectangular_hull_abs_lower": hull_lower,
        "minimum_chart_denominator_abs_lower": min(denominator_lowers),
        "parameter_volume_coverage_error": abs(covered_volume - original_volume),
        "method_counts": json.dumps(
            method_counts,
            sort_keys=True,
            separators=(",", ":"),
        ),
        "leaf_union_theorem": (
            "D=union_ijk D_ijk and 0 notin J(D_ijk) for every exact "
            "epsilon/x/t leaf implies inf_D|J|>=min_ijk dist(0,J(D_ijk))"
        ),
    }
    return (
        leaf_union_lower,
        method,
        hull,
        min(denominator_lowers),
        diagnostics,
    )


def install_candidate_probe(parent: Any) -> Any:
    if parent.REVISION != PARENT_V56_REVISION:
        raise RuntimeError(
            f"expected parent revision {PARENT_V56_REVISION}, found {parent.REVISION}"
        )
    original = parent.tight_energy_contour_geometric_factors
    audit_rows: list[dict[str, Any]] = []

    def tight_v57_probe(
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
        for epsilon_count in EPSILON_COUNTS:
            started = time.perf_counter()
            try:
                candidate = collision_jacobian_epsilon_xt_leaf_union_candidate(
                    parent,
                    configuration,
                    path_context["cell"],
                    path_context["path_segment"],
                    path_context["absolute_coordinate"],
                    path_context["path_parameter"],
                    inputs["epsilon"],
                    epsilon_count,
                    X_COUNT,
                    T_COUNT,
                )
                candidate_lower, method, _, denominator, diagnostics = candidate
            except (
                parent.EnclosureFailure,
                parent.M5258.IntervalSingularity,
                ValueError,
            ) as error:
                audit_rows.append(
                    {
                        "configuration_role": configuration.get("role", ""),
                        "epsilon_count": epsilon_count,
                        "x_count": X_COUNT,
                        "t_count": T_COUNT,
                        "leaf_count": epsilon_count * X_COUNT * T_COUNT,
                        "status": "FAIL",
                        "leaf_union_abs_lower": 0.0,
                        "rectangular_hull_abs_lower": 0.0,
                        "minimum_chart_denominator_abs_lower": 0.0,
                        "parameter_volume_coverage_error": math.nan,
                        "runtime_seconds": time.perf_counter() - started,
                        "error_type": type(error).__name__,
                        "error": str(error).splitlines()[0][:600],
                        "method": "",
                        "leaf_union_theorem": "",
                    }
                )
                continue
            audit_rows.append(
                {
                    "configuration_role": configuration.get("role", ""),
                    "epsilon_count": epsilon_count,
                    "x_count": X_COUNT,
                    "t_count": T_COUNT,
                    "status": "PASS" if candidate_lower > 0.0 else "ZERO",
                    "runtime_seconds": time.perf_counter() - started,
                    "error_type": "",
                    "error": "",
                    **diagnostics,
                }
            )
            if candidate_lower > 0.0 and denominator > 0.0:
                raise PositiveCandidateFound(
                    f"v57 candidate E{epsilon_count}X{X_COUNT}T{T_COUNT}: "
                    f"{candidate_lower}"
                )
        return factors

    parent.tight_energy_contour_geometric_factors = tight_v57_probe
    parent.V57_CANDIDATE_AUDIT_ROWS = audit_rows
    parent.V57_PARENT_ACTION_CHANGED = False
    parent.V57_ONLY_ENCLOSURE_COMPOSITION_CANDIDATE = True
    parent.REVISION = PARENT_V57_REVISION
    return parent


def render_document(payload: dict[str, Any], base_5467: Any) -> None:
    lines = [
        "# 5490: D4 parent-v57 collision-Jacobian epsilon/x/t leaf-union candidate probe",
        "",
        "The first positive-epsilon parent-v56 box retains positive relative-root and selected-global-root bounds, but its exact 16 x 128 x/t collision-Jacobian union still contains zero. This probe tests the missing dependency directly: an exact finite cover in epsilon-real, x and t with the unchanged imaginary-epsilon interval on every leaf.",
        "",
        f"Target: `{payload['target_refinement_path']}`. Schedules run: `{payload['audit_row_count']}`. Selected exact cover: `E{payload['selected_epsilon_count']} x X{payload['selected_x_count']} x T{payload['selected_t_count']}`.",
        "",
        f"Leaf-union lower: `{payload['selected_leaf_union_abs_lower']}`. Rectangular-hull diagnostic lower: `{payload['selected_rectangular_hull_abs_lower']}`. Chart-denominator lower: `{payload['selected_chart_denominator_abs_lower']}`. Exact parameter-volume error: `{payload['selected_parameter_volume_coverage_error']}`.",
        "",
        f"**{payload['decision']}**",
        "",
        "This is a candidate probe only. It changes no action, contour, chart candidate, residue or acceptance threshold and deliberately stops before parent acceptance. A complete-amplitude target/control gate is required before any parent-v57 migration. Every broader GR/MTS claim remains false.",
        "",
    ]
    base_5467.atomic_text(DOCUMENT, "\n".join(lines))


def main() -> int:
    base_5467 = load_module("mts_5467_for_5490", SCRIPT_5467)
    base_5468 = load_module("mts_5468_for_5490", SCRIPT_5468)
    base_5469 = load_module("mts_5469_for_5490", SCRIPT_5469)
    base_5472 = load_module("mts_5472_for_5490", SCRIPT_5472)
    base_5474 = load_module("mts_5474_for_5490", SCRIPT_5474)
    base_5476 = load_module("mts_5476_for_5490", SCRIPT_5476)
    base_5478 = load_module("mts_5478_for_5490", SCRIPT_5478)
    base_5480 = load_module("mts_5480_for_5490", SCRIPT_5480)
    base_5483 = load_module("mts_5483_for_5490", SCRIPT_5483)
    base_5484 = load_module("mts_5484_for_5490", SCRIPT_5484)
    base_5467.set_below_normal_priority()
    base_5480.set_single_core_affinity()
    before_formalization = base_5467.formalization_snapshot()
    missing = [str(path) for path in source_paths() if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"missing sources: {missing}")
    state_sha256 = digest(STATE_5484)
    if state_sha256 != EXPECTED_STATE_SHA256:
        raise RuntimeError(
            "checkpoint 5484 state differs from the checkpoint-5490 source lock"
        )
    result_5483 = read_json(RESULT_5483)
    validation_5483 = read_csv(VALIDATION_5483)
    result_5484 = read_json(RESULT_5484)
    validation_5484 = read_csv(VALIDATION_5484)
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
        and '"collision_jacobian": 0.0' in str(row.get("failure_message", ""))
    ]
    if len(candidates) != 1:
        raise RuntimeError(
            f"expected one positive-epsilon collision witness, found {len(candidates)}"
        )
    target = candidates[0]
    stable, _, cells, support_segments, branches = base_5467.load_parent()
    parent = install_candidate_probe(
        fresh_v56(
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
    audit_rows = list(parent.V57_CANDIDATE_AUDIT_ROWS)
    positive = [
        row
        for row in audit_rows
        if row["status"] == "PASS"
        and float(row["leaf_union_abs_lower"]) > 0.0
        and float(row["minimum_chart_denominator_abs_lower"]) > 0.0
        and float(row["parameter_volume_coverage_error"]) <= 1.0e-18
    ]
    selected = positive[0] if positive else None
    payload: dict[str, Any] = {
        "checkpoint": CHECKPOINT,
        "revision": REVISION,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "decision": (
            "PARENT_V57_COLLISION_JACOBIAN_EPSILON_XT_LEAF_UNION_CANDIDATE_FOUND__BUILD_FULL_INTEGRATION_GATE"
            if selected
            else "PARENT_V57_COLLISION_JACOBIAN_EPSILON_XT_LEAF_UNION_CANDIDATE_NOT_FOUND"
        ),
        "target_cuboid_id": TARGET_CUBOID_ID,
        "target_refinement_path": target["refinement_path"],
        "target_epsilon_real_lower": float(target["epsilon_real_lower"]),
        "target_epsilon_real_upper": float(target["epsilon_real_upper"]),
        "target_x_lower": float(target["x_lower"]),
        "target_x_upper": float(target["x_upper"]),
        "target_t_lower": float(target["t_lower"]),
        "target_t_upper": float(target["t_upper"]),
        "target_failure_message": target["failure_message"],
        "probe_terminated_on_positive_candidate": (
            probe_result.get("failure_type") == "PositiveCandidateFound"
        ),
        "audit_row_count": len(audit_rows),
        "selected_epsilon_count": int(selected["epsilon_count"]) if selected else 0,
        "selected_x_count": int(selected["x_count"]) if selected else 0,
        "selected_t_count": int(selected["t_count"]) if selected else 0,
        "selected_leaf_union_abs_lower": (
            float(selected["leaf_union_abs_lower"]) if selected else 0.0
        ),
        "selected_rectangular_hull_abs_lower": (
            float(selected["rectangular_hull_abs_lower"]) if selected else 0.0
        ),
        "selected_chart_denominator_abs_lower": (
            float(selected["minimum_chart_denominator_abs_lower"])
            if selected
            else 0.0
        ),
        "selected_parameter_volume_coverage_error": (
            float(selected["parameter_volume_coverage_error"])
            if selected
            else math.nan
        ),
        "source_state_5484_sha256": state_sha256,
        "parent_action_changed": False,
        "only_enclosure_composition_candidate": True,
        "valid_for_parent_v57_collision_jacobian_epsilon_xt_candidate": False,
        "valid_for_parent_v57_active_cuboid": False,
        "valid_for_full_outer_parent_leaf_enclosure": False,
        "valid_for_D4_event_local_W3_bound": False,
        "valid_for_all_operator_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
        "next_target": (
            "BUILD_PARENT_V57_COMPLETE_AMPLITUDE_TARGET_CONTROL_INTEGRATION_GATE"
            if selected
            else "DERIVE_COLLISION_JACOBIAN_EPSILON_ZERO_SET_OR_REFINE_EPSILON_COVER"
        ),
    }
    finite_rows = [
        row
        for row in audit_rows
        if row["status"] in {"PASS", "ZERO"}
        and math.isfinite(float(row["leaf_union_abs_lower"]))
        and float(row["minimum_chart_denominator_abs_lower"]) > 0.0
        and float(row["parameter_volume_coverage_error"]) <= 1.0e-18
    ]
    outcome_consistent = bool(selected) or (
        bool(audit_rows)
        and not positive
        and all(row["status"] in {"ZERO", "FAIL"} for row in audit_rows)
    )
    after_formalization = base_5467.formalization_snapshot()
    validations = [
        check("all_sources_exist", not missing, len(source_paths())),
        check(
            "checkpoint_5484_state_is_hash_locked",
            state_sha256 == EXPECTED_STATE_SHA256,
            state_sha256,
        ),
        check(
            "parent_v56_gate_and_frontier_are_valid",
            int(result_5483.get("failed_validation_count", -1)) == 0
            and all(truth(row["passed"]) for row in validation_5483)
            and int(result_5484.get("failed_validation_count", -1)) == 0
            and all(truth(row["passed"]) for row in validation_5484)
            and not state["unresolved"],
            f"5483={result_5483.get('decision')};5484={result_5484.get('decision')}",
        ),
        check(
            "target_is_the_first_positive_epsilon_v56_collision_witness",
            len(candidates) == 1,
            target["refinement_path"],
        ),
        check(
            "epsilon_xt_cover_rows_are_numeric_and_exact",
            bool(finite_rows) and len(finite_rows) == len(audit_rows),
            f"finite={len(finite_rows)};total={len(audit_rows)}",
        ),
        check(
            "candidate_outcome_is_internally_consistent",
            outcome_consistent,
            payload["decision"],
        ),
        check(
            "candidate_probe_stops_before_parent_acceptance",
            (
                payload["probe_terminated_on_positive_candidate"]
                if selected
                else not payload["valid_for_parent_v57_active_cuboid"]
            ),
            probe_result.get("failure_type", ""),
        ),
        check(
            "parent_action_and_thresholds_are_unchanged",
            not payload["parent_action_changed"]
            and payload["only_enclosure_composition_candidate"],
            "exact finite-cover composition only",
        ),
        check(
            "candidate_is_not_misreported_as_parent_pass",
            not payload[
                "valid_for_parent_v57_collision_jacobian_epsilon_xt_candidate"
            ]
            and not payload["valid_for_parent_v57_active_cuboid"],
            "complete-amplitude target/control gate not run",
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
            "local geometric-factor candidate only",
        ),
    ]
    payload["validation_row_count"] = len(validations)
    payload["failed_validation_count"] = sum(
        not row["passed"] for row in validations
    )
    OUTPUT.mkdir(parents=True, exist_ok=True)
    base_5467.atomic_csv(AUDIT, audit_rows)
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
                    "target_refinement_path",
                    "audit_row_count",
                    "selected_epsilon_count",
                    "selected_x_count",
                    "selected_t_count",
                    "selected_leaf_union_abs_lower",
                    "selected_rectangular_hull_abs_lower",
                    "selected_chart_denominator_abs_lower",
                    "selected_parameter_volume_coverage_error",
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
