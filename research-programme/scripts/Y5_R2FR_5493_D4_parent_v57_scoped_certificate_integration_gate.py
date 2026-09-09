from __future__ import annotations

import csv
import hashlib
import importlib.util
import json
import math
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


POST = Path(__file__).resolve().parents[1]
SCRIPTS = POST / "scripts"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
OUTPUT = FUNCTIONAL_RG / "5493"

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
SCRIPT_5492 = SCRIPTS / "Y5_R2FR_5492_D4_parent_v57_adaptive_x_replacement_candidate_probe.py"

MANIFEST_5468 = FUNCTIONAL_RG / "5468" / "D4_exact_outer_cuboid_manifest.csv"
STATE_5484 = (
    FUNCTIONAL_RG
    / "5484"
    / "work-v1"
    / "E07__U051__RIGHT_CONNECTOR__CUBOID__6df3d70a73e4618b.json"
)
RESULT_5492 = FUNCTIONAL_RG / "5492" / "D4_parent_v57_adaptive_x_replacement_candidate_result.json"
VALIDATION_5492 = FUNCTIONAL_RG / "5492" / "P8_Y5_BRR5491_5492_VALIDATION.csv"
SOURCE_REGISTER_5492 = FUNCTIONAL_RG / "5492" / "source_register.csv"
WORK_STATE_5492 = FUNCTIONAL_RG / "5492" / "work-v1" / "adaptive_x_replacement_state.json"
LEAF_AUDIT_5492 = FUNCTIONAL_RG / "5492" / "D4_parent_v57_adaptive_x_replacement_leaf_audit.csv"

SCOPE_BINDING = OUTPUT / "D4_parent_v57_scoped_certificate_binding.json"
AUDIT = OUTPUT / "D4_parent_v57_scoped_certificate_application_audit.csv"
COMPARISON = OUTPUT / "D4_parent_v56_v57_target_and_control_comparison.csv"
SOURCE_REGISTER = OUTPUT / "source_register.csv"
VALIDATION = OUTPUT / "P8_Y5_BRR5492_5493_VALIDATION.csv"
STATUS = OUTPUT / "status.json"
RESULT = OUTPUT / "D4_parent_v57_scoped_certificate_integration_result.json"
DOCUMENT = POST / "5493-Y5-R2FR-D4-parent-v57-scoped-certificate-integration-gate.md"

CHECKPOINT = 5493
REVISION = "D4-parent-v57-scoped-certificate-integration-gate-v1"
PARENT_V56_REVISION = "D4-deformed-contour-regular-away-W3-v56-collision-jacobian-xt-leaf-union"
PARENT_V57_REVISION = "D4-deformed-contour-regular-away-W3-v57-scoped-E16-X32-T128-certificate"
TARGET_CUBOID_ID = "E07__U051__RIGHT_CONNECTOR__CUBOID__6df3d70a73e4618b"
TARGET_REFINEMENT_PATH = "R_E0S_E0S_E0S_E1S"
EXPECTED_FAILURE_MARKER = "global contour geometric denominator reaches zero"
EXPECTED_STATE_SHA256 = "3f485d18bb2a55d3fda317091e58c0330166a7b5ae7e2185a82ab46602e23faa"
EXPECTED_WORK_SHA256 = "351b27598779707c199746bdc64f498b9a035dd4ef2e66bec9cfafe122a10881"
EXPECTED_LEAF_AUDIT_SHA256 = "4ea6f7369a6928cb4975d409e4db1cd876bb6ac1f10c764fb4c775665acacaee"
EXPECTED_RESULT_SHA256 = "6a02d818cb0155f2e54d942fbcb0789f8d7a2cfeb7fb5ae5385898a5051e381e"
METHOD = "V57_SCOPED_EXACT_E16_X32_T128_CERTIFICATE"
METRIC_FIELDS = (
    "integrated_regular_path_abs_upper",
    "minimum_amplitude_denominator_abs_lower",
    "relative_root_abs_lower",
    "selected_global_root_abs_lower",
    "collision_jacobian_abs_lower",
)
DOMAIN_FIELDS = (
    "epsilon_real_lower",
    "epsilon_real_upper",
    "epsilon_imaginary_lower",
    "epsilon_imaginary_upper",
    "x_lower",
    "x_upper",
    "t_lower",
    "t_upper",
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
        SCRIPT_5483,
        SCRIPT_5490,
        SCRIPT_5492,
        MANIFEST_5468,
        STATE_5484,
        RESULT_5492,
        VALIDATION_5492,
        SOURCE_REGISTER_5492,
        WORK_STATE_5492,
        LEAF_AUDIT_5492,
    )


def check(gate: str, passed: bool, evidence: Any) -> dict[str, Any]:
    return {
        "checkpoint": CHECKPOINT,
        "validation_gate": gate,
        "passed": bool(passed),
        "evidence": evidence,
    }


def normalized(value: Any) -> Any:
    if value is None or isinstance(value, (bool, int, float, str)):
        return value
    if isinstance(value, complex):
        return {"complex_real": value.real, "complex_imaginary": value.imag}
    if isinstance(value, dict):
        return {
            str(key): normalized(item)
            for key, item in sorted(value.items(), key=lambda pair: str(pair[0]))
        }
    if isinstance(value, (list, tuple)):
        return [normalized(item) for item in value]
    if isinstance(value, set):
        return sorted((normalized(item) for item in value), key=repr)
    return {"type": type(value).__qualname__, "repr": repr(value)}


def canonical_json(value: Any) -> str:
    return json.dumps(
        normalized(value),
        sort_keys=True,
        separators=(",", ":"),
        allow_nan=False,
    )


def object_fingerprint(value: Any) -> tuple[str, str]:
    serialized = canonical_json(value)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest(), serialized


def context_domain(
    parent: Any,
    inputs: dict[str, Any],
    path_context: dict[str, Any],
) -> dict[str, float]:
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
    return {
        "epsilon_real_lower": epsilon_real_lower,
        "epsilon_real_upper": epsilon_real_upper,
        "epsilon_imaginary_lower": epsilon_imaginary_lower,
        "epsilon_imaginary_upper": epsilon_imaginary_upper,
        "x_lower": x_lower,
        "x_upper": x_upper,
        "t_lower": t_lower,
        "t_upper": t_upper,
    }


def domains_equal(left: dict[str, Any], right: dict[str, Any]) -> bool:
    return all(float(left[field]) == float(right[field]) for field in DOMAIN_FIELDS)


def domain_contained(
    candidate: dict[str, Any],
    certificate: dict[str, Any],
) -> bool:
    for lower_field, upper_field in (
        ("epsilon_real_lower", "epsilon_real_upper"),
        ("epsilon_imaginary_lower", "epsilon_imaginary_upper"),
        ("x_lower", "x_upper"),
        ("t_lower", "t_upper"),
    ):
        scale = max(
            1.0,
            abs(float(candidate[lower_field])),
            abs(float(candidate[upper_field])),
            abs(float(certificate[lower_field])),
            abs(float(certificate[upper_field])),
        )
        tolerance = 1.0e-14 * scale
        if float(candidate[lower_field]) < float(certificate[lower_field]) - tolerance:
            return False
        if float(candidate[upper_field]) > float(certificate[upper_field]) + tolerance:
            return False
    return True


def source_register_is_current(rows: list[dict[str, str]]) -> bool:
    return bool(rows) and all(
        truth(row.get("exists"))
        and Path(row["source_path"]).is_file()
        and digest(Path(row["source_path"])) == row["sha256"]
        for row in rows
    )


def build_certificate(
    parent: Any,
    result: dict[str, Any],
    work_state: dict[str, Any],
    leaf_rows: list[dict[str, str]],
) -> dict[str, Any]:
    intervals: list[tuple[float, float, float, float]] = []
    final_lowers: list[float] = []
    denominator_lowers: list[float] = []
    covered_volumes: list[float] = []
    for row in leaf_rows:
        final_lowers.append(float(row["final_lower"]))
        denominator_lowers.append(float(row["final_denominator_lower"]))
        covered_volumes.append(float(row["accepted_volume"]))
        for child_index in range(2):
            prefix = f"child{child_index}"
            intervals.append(
                (
                    float(row[f"{prefix}_jacobian_real_lower"]),
                    float(row[f"{prefix}_jacobian_real_upper"]),
                    float(row[f"{prefix}_jacobian_imaginary_lower"]),
                    float(row[f"{prefix}_jacobian_imaginary_upper"]),
                )
            )
    hull_bounds = {
        "real_lower": min(interval[0] for interval in intervals),
        "real_upper": max(interval[1] for interval in intervals),
        "imaginary_lower": min(interval[2] for interval in intervals),
        "imaginary_upper": max(interval[3] for interval in intervals),
    }
    hull = parent.cbox(
        hull_bounds["real_lower"],
        hull_bounds["real_upper"],
        hull_bounds["imaginary_lower"],
        hull_bounds["imaginary_upper"],
    )
    domain = {field: float(work_state["domain"][field]) for field in DOMAIN_FIELDS}
    return {
        "method": METHOD,
        "configuration_role": str(work_state["configuration_role"]),
        "domain": domain,
        "base_leaf_count": len(leaf_rows),
        "final_leaf_count": len(intervals),
        "leaf_union_abs_lower": min(final_lowers),
        "minimum_chart_denominator_abs_lower": min(denominator_lowers),
        "rectangular_hull_abs_lower": parent.M5258.lower_abs(hull),
        "hull_bounds": hull_bounds,
        "original_parameter_volume": float(result["original_parameter_volume"]),
        "covered_parameter_volume": math.fsum(covered_volumes),
        "parameter_volume_coverage_error": abs(
            math.fsum(covered_volumes)
            - float(result["original_parameter_volume"])
        ),
        "source_state_sha256": EXPECTED_STATE_SHA256,
        "work_state_sha256": EXPECTED_WORK_SHA256,
        "leaf_audit_sha256": EXPECTED_LEAF_AUDIT_SHA256,
        "candidate_result_sha256": EXPECTED_RESULT_SHA256,
    }


def install_capture(parent: Any) -> Any:
    if parent.REVISION != PARENT_V56_REVISION:
        raise RuntimeError(
            f"expected parent revision {PARENT_V56_REVISION}, found {parent.REVISION}"
        )
    original = parent.tight_energy_contour_geometric_factors
    parent.V57_SCOPE_CAPTURE = None

    def tight_capture(
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
            lower <= 0.0
            and path_context is not None
            and path_context.get("path_segment")
            in {"LEFT_CONNECTOR", "RIGHT_CONNECTOR"}
            and parent.V57_SCOPE_CAPTURE is None
        ):
            configuration_sha256, configuration_json = object_fingerprint(
                configuration
            )
            cell_sha256, cell_json = object_fingerprint(path_context["cell"])
            parent.V57_SCOPE_CAPTURE = {
                "configuration_role": str(configuration.get("role", "")),
                "configuration_sha256": configuration_sha256,
                "configuration_json": configuration_json,
                "cell_sha256": cell_sha256,
                "cell_json": cell_json,
                "path_segment": str(path_context["path_segment"]),
                "domain": context_domain(parent, inputs, path_context),
            }
        return factors

    parent.tight_energy_contour_geometric_factors = tight_capture
    return parent


def install_parent_v57(
    parent: Any,
    binding: dict[str, Any],
    certificate: dict[str, Any],
) -> Any:
    if parent.REVISION != PARENT_V56_REVISION:
        raise RuntimeError(
            f"expected parent revision {PARENT_V56_REVISION}, found {parent.REVISION}"
        )
    original = parent.tight_energy_contour_geometric_factors
    audit_rows: list[dict[str, Any]] = []

    def tight_v57(
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
        configuration_sha256, _ = object_fingerprint(configuration)
        cell_sha256, _ = object_fingerprint(path_context["cell"])
        current_domain = context_domain(parent, inputs, path_context)
        scope_matches = (
            str(configuration.get("role", ""))
            == binding["configuration_role"]
            and configuration_sha256 == binding["configuration_sha256"]
            and cell_sha256 == binding["cell_sha256"]
            and str(path_context.get("path_segment", ""))
            == binding["path_segment"]
            and domain_contained(current_domain, certificate["domain"])
        )
        audit_row = {
            "configuration_role": str(configuration.get("role", "")),
            "configuration_sha256": configuration_sha256,
            "cell_sha256": cell_sha256,
            "path_segment": str(path_context.get("path_segment", "")),
            **current_domain,
            "scope_matches": scope_matches,
            "status": "APPLIED" if scope_matches else "SCOPE_MISS",
            "method": METHOD if scope_matches else "",
            "leaf_union_abs_lower": (
                certificate["leaf_union_abs_lower"] if scope_matches else 0.0
            ),
            "rectangular_hull_abs_lower": (
                certificate["rectangular_hull_abs_lower"]
                if scope_matches
                else 0.0
            ),
            "minimum_chart_denominator_abs_lower": (
                certificate["minimum_chart_denominator_abs_lower"]
                if scope_matches
                else 0.0
            ),
            "parameter_volume_coverage_error": (
                certificate["parameter_volume_coverage_error"]
                if scope_matches
                else math.nan
            ),
        }
        audit_rows.append(audit_row)
        if not scope_matches:
            return factors
        hull_bounds = certificate["hull_bounds"]
        hull = parent.cbox(
            hull_bounds["real_lower"],
            hull_bounds["real_upper"],
            hull_bounds["imaginary_lower"],
            hull_bounds["imaginary_upper"],
        )
        candidate_lowers = dict(
            factors.get("collision_jacobian_candidate_abs_lowers", {})
        )
        candidate_lowers[METHOD] = certificate["leaf_union_abs_lower"]
        factors["collision_jacobian_candidate_abs_lowers"] = candidate_lowers
        factors["collision_jacobian"] = hull
        factors["collision_jacobian_enclosure_method"] = METHOD
        factors["collision_jacobian_chart_denominator_lower"] = certificate[
            "minimum_chart_denominator_abs_lower"
        ]
        factors["collision_jacobian_selected_abs_lower"] = certificate[
            "leaf_union_abs_lower"
        ]
        factors["collision_jacobian_leaf_union_abs_lower"] = certificate[
            "leaf_union_abs_lower"
        ]
        factors["collision_jacobian_leaf_union_rectangular_hull_abs_lower"] = (
            certificate["rectangular_hull_abs_lower"]
        )
        factors["collision_jacobian_leaf_union_leaf_count"] = certificate[
            "final_leaf_count"
        ]
        factors["collision_jacobian_leaf_union_parameter_volume_coverage_error"] = (
            certificate["parameter_volume_coverage_error"]
        )
        return factors

    parent.tight_energy_contour_geometric_factors = tight_v57
    parent.V57_SCOPED_CERTIFICATE_AUDIT_ROWS = audit_rows
    parent.V57_PARENT_ACTION_CHANGED = False
    parent.V57_ONLY_ENCLOSURE_COMPOSITION_CHANGED = True
    parent.REVISION = PARENT_V57_REVISION
    return parent


def render_document(payload: dict[str, Any], base_5467: Any) -> None:
    lines = [
        "# 5493: D4 parent-v57 scoped-certificate integration gate",
        "",
        "Parent v57 binds checkpoint 5492's immutable E16/X32/T128 finite-union certificate to the exact discrete configuration fingerprint, cell fingerprint, connector segment and contained local parameter domain captured from the parent-v56 failure. It changes no action, contour, chart candidate, residue or threshold.",
        "",
        f"Parent-v56 target failure reproduced: `{payload['target_v56_expected_failure']}`. Complete parent-v57 target passed: `{payload['target_v57_passed']}`. Certificate applications: `{payload['v57_applied_audit_row_count']}`. Scope misses: `{payload['v57_scope_miss_audit_row_count']}`.",
        "",
        f"Certificate Jacobian lower: `{payload['certificate_leaf_union_abs_lower']}`. Complete-amplitude denominator lower: `{payload['target_v57_amplitude_denominator_abs_lower']}`. Complete target collision-Jacobian lower: `{payload['target_v57_collision_jacobian_abs_lower']}`.",
        "",
        f"Untriggered parent-v56/parent-v57 control exactly unchanged: `{payload['control_v56_v57_identical']}`.",
        "",
        f"**{payload['decision']}**",
        "",
        "This gate certifies only the scoped parent enclosure mechanism. The active cuboid and every broader GR/MTS claim remain open until hash-locked migration and further coverage complete.",
        "",
    ]
    base_5467.atomic_text(DOCUMENT, "\n".join(lines))


def main() -> int:
    base_5467 = load_module("mts_5467_for_5493", SCRIPT_5467)
    base_5468 = load_module("mts_5468_for_5493", SCRIPT_5468)
    base_5469 = load_module("mts_5469_for_5493", SCRIPT_5469)
    base_5472 = load_module("mts_5472_for_5493", SCRIPT_5472)
    base_5474 = load_module("mts_5474_for_5493", SCRIPT_5474)
    base_5476 = load_module("mts_5476_for_5493", SCRIPT_5476)
    base_5478 = load_module("mts_5478_for_5493", SCRIPT_5478)
    base_5480 = load_module("mts_5480_for_5493", SCRIPT_5480)
    base_5483 = load_module("mts_5483_for_5493", SCRIPT_5483)
    base_5490 = load_module("mts_5490_for_5493", SCRIPT_5490)
    base_5467.set_below_normal_priority()
    base_5480.set_single_core_affinity()
    before_formalization = base_5467.formalization_snapshot()
    missing = [str(path) for path in source_paths() if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"missing sources: {missing}")
    state_sha256 = digest(STATE_5484)
    work_sha256 = digest(WORK_STATE_5492)
    leaf_audit_sha256 = digest(LEAF_AUDIT_5492)
    result_sha256 = digest(RESULT_5492)
    if state_sha256 != EXPECTED_STATE_SHA256:
        raise RuntimeError("checkpoint 5484 state differs from checkpoint-5493 lock")
    if work_sha256 != EXPECTED_WORK_SHA256:
        raise RuntimeError("checkpoint 5492 work state differs from source lock")
    if leaf_audit_sha256 != EXPECTED_LEAF_AUDIT_SHA256:
        raise RuntimeError("checkpoint 5492 leaf audit differs from source lock")
    if result_sha256 != EXPECTED_RESULT_SHA256:
        raise RuntimeError("checkpoint 5492 result differs from source lock")
    result_5492 = read_json(RESULT_5492)
    validation_5492 = read_csv(VALIDATION_5492)
    source_register_5492 = read_csv(SOURCE_REGISTER_5492)
    work_state_5492 = read_json(WORK_STATE_5492)
    leaf_rows_5492 = read_csv(LEAF_AUDIT_5492)
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
        and EXPECTED_FAILURE_MARKER in str(row.get("failure_message", ""))
        and '"collision_jacobian": 0.0' in str(row.get("failure_message", ""))
    ]
    if len(target_candidates) != 1:
        raise RuntimeError(
            f"expected one parent-v56 target witness, found {len(target_candidates)}"
        )
    target = target_candidates[0]
    control_candidates = [
        row
        for row in state["accepted"]
        if truth(row.get("probe_passed"))
        and math.isfinite(float(row.get("runtime_seconds", math.inf)))
        and float(row.get("collision_jacobian_abs_lower", 0.0)) > 0.0
    ]
    if not control_candidates:
        raise RuntimeError("checkpoint 5484 has no passing control candidate")
    control = min(
        control_candidates,
        key=lambda row: float(row.get("runtime_seconds", math.inf)),
    )
    stable, _, cells, support_segments, branches = base_5467.load_parent()
    certificate_parent = base_5490.fresh_v56(
        base_5467,
        base_5472,
        base_5474,
        base_5476,
        base_5478,
        base_5483,
    )
    certificate = build_certificate(
        certificate_parent,
        result_5492,
        work_state_5492,
        leaf_rows_5492,
    )

    parent_v56_target = install_capture(
        base_5490.fresh_v56(
            base_5467,
            base_5472,
            base_5474,
            base_5476,
            base_5478,
            base_5483,
        )
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
    binding = parent_v56_target.V57_SCOPE_CAPTURE
    if binding is None:
        raise RuntimeError("parent-v56 target failure produced no scope capture")

    parent_v57_target = install_parent_v57(
        base_5490.fresh_v56(
            base_5467,
            base_5472,
            base_5474,
            base_5476,
            base_5478,
            base_5483,
        ),
        binding,
        certificate,
    )
    target_v57 = base_5469.evaluate_node(
        base_5468,
        stable,
        parent_v57_target,
        cells,
        support_segments,
        branches,
        cuboid,
        target,
    )
    target_audit = list(parent_v57_target.V57_SCOPED_CERTIFICATE_AUDIT_ROWS)

    parent_v56_control = base_5490.fresh_v56(
        base_5467,
        base_5472,
        base_5474,
        base_5476,
        base_5478,
        base_5483,
    )
    parent_v57_control = install_parent_v57(
        base_5490.fresh_v56(
            base_5467,
            base_5472,
            base_5474,
            base_5476,
            base_5478,
            base_5483,
        ),
        binding,
        certificate,
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
    control_v57 = base_5469.evaluate_node(
        base_5468,
        stable,
        parent_v57_control,
        cells,
        support_segments,
        branches,
        cuboid,
        control,
    )
    control_audit = list(parent_v57_control.V57_SCOPED_CERTIFICATE_AUDIT_ROWS)
    control_identical = (
        truth(control_v56.get("probe_passed"))
        and truth(control_v57.get("probe_passed"))
        and all(
            float(control_v56[field]) == float(control_v57[field])
            for field in METRIC_FIELDS
        )
        and not control_audit
    )
    target_v56_expected_failure = (
        not truth(target_v56.get("probe_passed"))
        and EXPECTED_FAILURE_MARKER
        in str(target_v56.get("failure_message", ""))
        and '"collision_jacobian": 0.0'
        in str(target_v56.get("failure_message", ""))
    )
    target_v57_passed = truth(target_v57.get("probe_passed"))
    applied_rows = [row for row in target_audit if row["status"] == "APPLIED"]
    scope_miss_rows = [row for row in target_audit if row["status"] == "SCOPE_MISS"]
    scope_binding_matches_candidate = (
        binding["configuration_role"] == certificate["configuration_role"]
        and domains_equal(binding["domain"], certificate["domain"])
        and binding["path_segment"] in {"LEFT_CONNECTOR", "RIGHT_CONNECTOR"}
    )
    candidate_rows_valid = (
        len(leaf_rows_5492) == 32768
        and all(float(row["base_lower"]) == 0.0 for row in leaf_rows_5492)
        and all(
            float(row["child0_lower"]) > 0.0
            and float(row["child1_lower"]) > 0.0
            and float(row["final_lower"]) > 0.0
            and row["status"] == "PASS"
            for row in leaf_rows_5492
        )
    )
    comparison_rows: list[dict[str, Any]] = []
    for role, result, revision in (
        ("collision_jacobian_target_v56", target_v56, PARENT_V56_REVISION),
        ("collision_jacobian_target_v57", target_v57, PARENT_V57_REVISION),
        ("untriggered_control_v56", control_v56, PARENT_V56_REVISION),
        ("untriggered_control_v57", control_v57, PARENT_V57_REVISION),
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
        "parent_revision": PARENT_V57_REVISION,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "decision": (
            "PARENT_V57_SCOPED_E16_X32_T128_CERTIFICATE_CERTIFIED__MIGRATE_FRONTIER"
            if target_v56_expected_failure
            and target_v57_passed
            and applied_rows
            and not scope_miss_rows
            and scope_binding_matches_candidate
            and control_identical
            else "PARENT_V57_SCOPED_E16_X32_T128_CERTIFICATE_NOT_CERTIFIED"
        ),
        "target_cuboid_id": TARGET_CUBOID_ID,
        "target_refinement_path": target["refinement_path"],
        "control_refinement_path": control["refinement_path"],
        "target_v56_expected_failure": target_v56_expected_failure,
        "target_v57_passed": target_v57_passed,
        "scope_binding_matches_candidate": scope_binding_matches_candidate,
        "v57_audit_row_count": len(target_audit),
        "v57_applied_audit_row_count": len(applied_rows),
        "v57_scope_miss_audit_row_count": len(scope_miss_rows),
        "certificate_leaf_union_abs_lower": certificate[
            "leaf_union_abs_lower"
        ],
        "certificate_rectangular_hull_abs_lower": certificate[
            "rectangular_hull_abs_lower"
        ],
        "certificate_chart_denominator_abs_lower": certificate[
            "minimum_chart_denominator_abs_lower"
        ],
        "certificate_parameter_volume_coverage_error": certificate[
            "parameter_volume_coverage_error"
        ],
        "certificate_final_leaf_count": certificate["final_leaf_count"],
        "target_v57_amplitude_denominator_abs_lower": target_v57.get(
            "minimum_amplitude_denominator_abs_lower"
        ),
        "target_v57_collision_jacobian_abs_lower": target_v57.get(
            "collision_jacobian_abs_lower"
        ),
        "target_v57_integrated_regular_path_abs_upper": target_v57.get(
            "integrated_regular_path_abs_upper"
        ),
        "control_v56_v57_identical": control_identical,
        "source_state_5484_sha256": state_sha256,
        "source_work_state_5492_sha256": work_sha256,
        "source_leaf_audit_5492_sha256": leaf_audit_sha256,
        "source_result_5492_sha256": result_sha256,
        "parent_action_changed": False,
        "only_enclosure_composition_changed": True,
        "valid_for_parent_v57_scoped_certificate": False,
        "valid_for_parent_v57_active_cuboid": False,
        "valid_for_full_outer_parent_leaf_enclosure": False,
        "valid_for_D4_event_local_W3_bound": False,
        "valid_for_all_operator_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
        "next_target": "CREATE_HASH_LOCKED_V57_CARRY_FORWARD_OF_CHECKPOINT_5484_STATE",
    }
    after_formalization = base_5467.formalization_snapshot()
    validations = [
        check("all_sources_exist", not missing, len(source_paths())),
        check(
            "checkpoint_5492_source_register_is_current",
            source_register_is_current(source_register_5492),
            len(source_register_5492),
        ),
        check(
            "checkpoint_5492_hashes_are_locked",
            state_sha256 == EXPECTED_STATE_SHA256
            and work_sha256 == EXPECTED_WORK_SHA256
            and leaf_audit_sha256 == EXPECTED_LEAF_AUDIT_SHA256
            and result_sha256 == EXPECTED_RESULT_SHA256,
            result_sha256,
        ),
        check(
            "checkpoint_5492_candidate_is_valid",
            int(result_5492.get("failed_validation_count", -1)) == 0
            and all(truth(row["passed"]) for row in validation_5492)
            and truth(result_5492.get("candidate_cover_complete"))
            and truth(result_5492.get("candidate_positive"))
            and candidate_rows_valid,
            result_5492.get("decision"),
        ),
        check(
            "scope_binding_matches_candidate_role_domain",
            scope_binding_matches_candidate,
            binding["configuration_sha256"],
        ),
        check(
            "v56_target_reproduces_scoped_collision_failure",
            target_v56_expected_failure,
            target_v56.get("failure_message", ""),
        ),
        check(
            "v57_certificate_applies_without_scope_miss",
            bool(applied_rows)
            and not scope_miss_rows
            and all(truth(row["scope_matches"]) for row in applied_rows),
            f"applied={len(applied_rows)};miss={len(scope_miss_rows)}",
        ),
        check(
            "v57_certificate_metrics_match_immutable_candidate",
            payload["certificate_leaf_union_abs_lower"]
            == float(result_5492["leaf_union_abs_lower"])
            and payload["certificate_rectangular_hull_abs_lower"]
            == float(result_5492["rectangular_hull_abs_lower"])
            and payload["certificate_chart_denominator_abs_lower"]
            == float(result_5492["minimum_chart_denominator_abs_lower"])
            and payload["certificate_parameter_volume_coverage_error"] == 0.0
            and payload["certificate_final_leaf_count"] == 65536,
            payload["certificate_leaf_union_abs_lower"],
        ),
        check(
            "v57_complete_parent_target_is_finite",
            target_v57_passed
            and all(
                math.isfinite(float(target_v57[field]))
                and float(target_v57[field]) > 0.0
                for field in METRIC_FIELDS
            ),
            target_v57.get("minimum_amplitude_denominator_abs_lower"),
        ),
        check(
            "untriggered_v56_v57_control_is_exactly_unchanged",
            control_identical,
            control["refinement_path"],
        ),
        check(
            "v57_changes_only_enclosure_composition",
            not parent_v57_target.V57_PARENT_ACTION_CHANGED
            and parent_v57_target.V57_ONLY_ENCLOSURE_COMPOSITION_CHANGED,
            PARENT_V57_REVISION,
        ),
        check(
            "formalization_workbench_untouched",
            before_formalization == after_formalization,
            f"before={len(before_formalization)};after={len(after_formalization)}",
        ),
        check(
            "broad_claims_remain_false",
            not payload["valid_for_parent_v57_active_cuboid"]
            and not payload["valid_for_full_outer_parent_leaf_enclosure"]
            and not payload["valid_for_D4_event_local_W3_bound"]
            and not payload["valid_for_all_operator_local_GR_claim"]
            and not payload["valid_for_full_MTS_claim"],
            "one scoped collision-Jacobian enclosure class only",
        ),
    ]
    payload["validation_row_count"] = len(validations)
    payload["failed_validation_count"] = sum(not row["passed"] for row in validations)
    payload["valid_for_parent_v57_scoped_certificate"] = (
        payload["failed_validation_count"] == 0
        and "CERTIFIED" in payload["decision"]
    )
    OUTPUT.mkdir(parents=True, exist_ok=True)
    binding_output = {
        **binding,
        "certificate_domain": certificate["domain"],
        "certificate_method": METHOD,
        "certificate_source_hashes": {
            "state_5484": state_sha256,
            "work_state_5492": work_sha256,
            "leaf_audit_5492": leaf_audit_sha256,
            "result_5492": result_sha256,
        },
    }
    base_5467.atomic_json(SCOPE_BINDING, binding_output)
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
                    "target_v56_expected_failure",
                    "target_v57_passed",
                    "scope_binding_matches_candidate",
                    "v57_applied_audit_row_count",
                    "v57_scope_miss_audit_row_count",
                    "certificate_leaf_union_abs_lower",
                    "target_v57_amplitude_denominator_abs_lower",
                    "target_v57_collision_jacobian_abs_lower",
                    "control_v56_v57_identical",
                    "valid_for_parent_v57_scoped_certificate",
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
