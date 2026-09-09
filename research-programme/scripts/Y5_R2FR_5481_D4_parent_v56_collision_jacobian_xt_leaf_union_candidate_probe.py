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
OUTPUT = FUNCTIONAL_RG / "5481"

SCRIPT_5467 = SCRIPTS / "Y5_R2FR_5467_D4_all_outer_leaf_epsilon_fiber_transplant_runner.py"
SCRIPT_5468 = SCRIPTS / "Y5_R2FR_5468_D4_exact_outer_cuboid_coalescence_runner.py"
SCRIPT_5469 = SCRIPTS / "Y5_R2FR_5469_D4_resumable_three_axis_cuboid_certificate_runner.py"
SCRIPT_5472 = SCRIPTS / "Y5_R2FR_5472_D4_parent_v52_collision_jacobian_leaf_union_integration_gate.py"
SCRIPT_5474 = SCRIPTS / "Y5_R2FR_5474_D4_parent_v53_stable_edge_t_leaf_union_integration_gate.py"
SCRIPT_5476 = SCRIPTS / "Y5_R2FR_5476_D4_parent_v54_first_spinor_pivot_t_leaf_union_integration_gate.py"
SCRIPT_5478 = SCRIPTS / "Y5_R2FR_5478_D4_parent_v55_stable_edge_xt_leaf_union_integration_gate.py"
SCRIPT_5480 = SCRIPTS / "Y5_R2FR_5480_D4_parent_v55_hash_locked_frontier_runner.py"
RESULT_5480 = FUNCTIONAL_RG / "5480" / "D4_parent_v55_hash_locked_frontier_result.json"
VALIDATION_5480 = FUNCTIONAL_RG / "5480" / "P8_Y5_BRR5479_5480_VALIDATION.csv"
MANIFEST_5468 = FUNCTIONAL_RG / "5468" / "D4_exact_outer_cuboid_manifest.csv"

TARGET_CUBOID_ID = "E07__U051__RIGHT_CONNECTOR__CUBOID__6df3d70a73e4618b"
STATE_5480 = FUNCTIONAL_RG / "5480" / "work-v1" / f"{TARGET_CUBOID_ID}.json"

AUDIT = OUTPUT / "D4_parent_v56_collision_jacobian_xt_leaf_union_candidate_audit.csv"
SOURCE_REGISTER = OUTPUT / "source_register.csv"
VALIDATION = OUTPUT / "P8_Y5_BRR5480_5481_VALIDATION.csv"
STATUS = OUTPUT / "status.json"
RESULT = OUTPUT / "D4_parent_v56_collision_jacobian_xt_leaf_union_candidate_result.json"
DOCUMENT = POST / "5481-Y5-R2FR-D4-parent-v56-collision-jacobian-xt-leaf-union-candidate-probe.md"

CHECKPOINT = 5481
REVISION = "D4-parent-v56-collision-jacobian-xt-leaf-union-candidate-probe-v1"
PARENT_V54_REVISION = "D4-deformed-contour-regular-away-W3-v54-first-spinor-pivot-t-leaf-union"
PARENT_V55_REVISION = "D4-deformed-contour-regular-away-W3-v55-stable-edge-xt-leaf-union"
PARENT_V56_REVISION = "D4-deformed-contour-regular-away-W3-v56-collision-jacobian-xt-leaf-union"
EXPECTED_FAILURE_MARKER = "global contour geometric denominator reaches zero"
SCHEDULE = ((4, 128), (8, 128), (16, 128), (8, 256))


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
        RESULT_5480,
        VALIDATION_5480,
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
) -> Any:
    return base_5478.install_parent_v55(
        base_5476.install_parent_v54(
            base_5474.install_parent_v53(
                base_5472.install_parent_v52(
                    base_5472.fresh_parent(base_5467, "mts_parent_v56_probe_5481")
                )
            ),
            base_5474,
        ),
        base_5474,
    )


def install_candidate_probe(parent: Any, base_5472: Any) -> Any:
    if parent.REVISION != PARENT_V55_REVISION:
        raise RuntimeError(
            f"expected parent revision {PARENT_V55_REVISION}, found {parent.REVISION}"
        )
    original = parent.tight_energy_contour_geometric_factors
    audit_rows: list[dict[str, Any]] = []

    def tight_v56_probe(
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
        if lower > 0.0 or path_context is None:
            return factors
        for x_count, t_count in SCHEDULE:
            started = time.perf_counter()
            try:
                candidate = base_5472.collision_jacobian_leaf_union_candidate(
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
                candidate_lower, method, _, denominator, diagnostics = candidate
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
                    "x_count": x_count,
                    "t_count": t_count,
                    "status": "PASS" if candidate_lower > 0.0 else "ZERO",
                    "leaf_union_abs_lower": candidate_lower,
                    "rectangular_hull_abs_lower": diagnostics[
                        "rectangular_hull_abs_lower"
                    ],
                    "minimum_chart_denominator_abs_lower": denominator,
                    "runtime_seconds": time.perf_counter() - started,
                    "error_type": "",
                    "error": "",
                    "method": method,
                    "leaf_union_theorem": diagnostics["leaf_union_theorem"],
                }
            )
            if candidate_lower > 0.0 and denominator > 0.0:
                raise PositiveCandidateFound(
                    f"v56 candidate {x_count}x{t_count}: {candidate_lower}"
                )
        return factors

    parent.tight_energy_contour_geometric_factors = tight_v56_probe
    parent.V56_CANDIDATE_AUDIT_ROWS = audit_rows
    parent.REVISION = PARENT_V56_REVISION
    return parent


def render_document(payload: dict[str, Any], base_5467: Any) -> None:
    lines = [
        "# 5481: D4 parent-v56 collision-Jacobian x/t-leaf-union candidate probe",
        "",
        "Checkpoint 5480 exposed a new global-contour collision-Jacobian hull obstruction after parent v55 had closed the stable-edge class. This probe does not alter the parent action or acceptance threshold. It asks whether a finer exact x/t partition makes every collision-Jacobian image leaf exclude zero.",
        "",
        f"Selected schedule: `{payload['selected_x_count']} x {payload['selected_t_count']}`. Leaf-union lower: `{payload['selected_leaf_union_abs_lower']}`. Rectangular-hull diagnostic lower: `{payload['selected_rectangular_hull_abs_lower']}`. Chart denominator lower: `{payload['selected_chart_denominator_abs_lower']}`.",
        "",
        f"**{payload['decision']}**",
        "",
        "This is a local candidate only. A complete parent-amplitude target/control integration gate is still required before frontier migration, and every broader claim remains false.",
        "",
    ]
    base_5467.atomic_text(DOCUMENT, "\n".join(lines))


def main() -> int:
    base_5467 = load_module("mts_5467_for_5481", SCRIPT_5467)
    base_5468 = load_module("mts_5468_for_5481", SCRIPT_5468)
    base_5469 = load_module("mts_5469_for_5481", SCRIPT_5469)
    base_5472 = load_module("mts_5472_for_5481", SCRIPT_5472)
    base_5474 = load_module("mts_5474_for_5481", SCRIPT_5474)
    base_5476 = load_module("mts_5476_for_5481", SCRIPT_5476)
    base_5478 = load_module("mts_5478_for_5481", SCRIPT_5478)
    base_5480 = load_module("mts_5480_for_5481", SCRIPT_5480)
    base_5467.set_below_normal_priority()
    base_5480.set_single_core_affinity()
    before_formalization = base_5467.formalization_snapshot()
    missing = [str(path) for path in source_paths() if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"missing sources: {missing}")
    result_5480 = read_json(RESULT_5480)
    validation_5480 = read_csv(VALIDATION_5480)
    state = read_json(STATE_5480)
    state_sha256 = digest(STATE_5480)
    cuboid = next(
        row
        for row in read_csv(MANIFEST_5468)
        if row["cuboid_job_id"] == TARGET_CUBOID_ID
    )
    candidates = [
        row
        for row in state["refinement_witnesses"]
        if row.get("certificate_source") == "checkpoint_5480_parent_v55_witness"
        and EXPECTED_FAILURE_MARKER in str(row.get("failure_message", ""))
        and '"collision_jacobian": 0.0' in str(row.get("failure_message", ""))
    ]
    if not candidates:
        raise RuntimeError("checkpoint 5480 has no new collision-Jacobian witness")
    target = max(
        candidates,
        key=lambda row: (
            (float(row["x_upper"]) - float(row["x_lower"]))
            * (float(row["t_upper"]) - float(row["t_lower"]))
        ),
    )
    stable, _, cells, support_segments, branches = base_5467.load_parent()
    parent = install_candidate_probe(
        fresh_v55(base_5467, base_5472, base_5474, base_5476, base_5478),
        base_5472,
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
    audit_rows = list(parent.V56_CANDIDATE_AUDIT_ROWS)
    positive = [
        row
        for row in audit_rows
        if row["status"] == "PASS"
        and float(row["leaf_union_abs_lower"]) > 0.0
        and float(row["minimum_chart_denominator_abs_lower"]) > 0.0
    ]
    selected = positive[0] if positive else None
    payload: dict[str, Any] = {
        "checkpoint": CHECKPOINT,
        "revision": REVISION,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "decision": (
            "PARENT_V56_COLLISION_JACOBIAN_XT_LEAF_UNION_CANDIDATE_FOUND__BUILD_FULL_INTEGRATION_GATE"
            if selected
            else "PARENT_V56_COLLISION_JACOBIAN_XT_LEAF_UNION_CANDIDATE_NOT_FOUND"
        ),
        "target_cuboid_id": TARGET_CUBOID_ID,
        "target_refinement_path": target["refinement_path"],
        "target_failure_message": target["failure_message"],
        "probe_terminated_on_positive_candidate": (
            probe_result.get("failure_type") == "PositiveCandidateFound"
        ),
        "audit_row_count": len(audit_rows),
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
        "source_state_5480_sha256": state_sha256,
        "parent_action_changed": False,
        "only_enclosure_composition_candidate": True,
        "valid_for_parent_v56_collision_jacobian_xt_candidate": False,
        "valid_for_parent_v56_active_cuboid": False,
        "valid_for_full_outer_parent_leaf_enclosure": False,
        "valid_for_D4_event_local_W3_bound": False,
        "valid_for_all_operator_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
        "next_target": (
            "BUILD_PARENT_V56_COMPLETE_AMPLITUDE_TARGET_CONTROL_INTEGRATION_GATE"
            if selected
            else "DERIVE_COLLISION_JACOBIAN_ZERO_SET_OR_REFINE_EXACT_COVER"
        ),
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
            "target_is_new_v55_collision_jacobian_witness",
            bool(candidates),
            target["refinement_path"],
        ),
        check(
            "candidate_probe_stops_before_parent_acceptance",
            payload["probe_terminated_on_positive_candidate"] if selected else True,
            probe_result.get("failure_type", ""),
        ),
        check(
            "positive_candidate_has_exact_finite_leaf_union_bound",
            bool(selected)
            and math.isfinite(payload["selected_leaf_union_abs_lower"])
            and payload["selected_leaf_union_abs_lower"] > 0.0
            and payload["selected_chart_denominator_abs_lower"] > 0.0,
            payload["selected_leaf_union_abs_lower"],
        ),
        check(
            "candidate_is_not_misreported_as_parent_pass",
            not payload["valid_for_parent_v56_collision_jacobian_xt_candidate"]
            and not payload["valid_for_parent_v56_active_cuboid"],
            "full-amplitude integration gate not run",
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
                    "selected_x_count",
                    "selected_t_count",
                    "selected_leaf_union_abs_lower",
                    "selected_rectangular_hull_abs_lower",
                    "selected_chart_denominator_abs_lower",
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
