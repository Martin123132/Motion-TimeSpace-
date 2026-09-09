from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import math
import os
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


POST = Path(__file__).resolve().parents[1]
SCRIPTS = POST / "scripts"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
OUTPUT = FUNCTIONAL_RG / "5495"
WORK = OUTPUT / "work-v1"

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
SCRIPT_5493 = SCRIPTS / "Y5_R2FR_5493_D4_parent_v57_scoped_certificate_integration_gate.py"
SCRIPT_5494 = SCRIPTS / "Y5_R2FR_5494_D4_parent_v57_post_certificate_stable_edge_axis_probe.py"

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
RESULT_5493 = FUNCTIONAL_RG / "5493" / "D4_parent_v57_scoped_certificate_integration_result.json"
BINDING_5493 = FUNCTIONAL_RG / "5493" / "D4_parent_v57_scoped_certificate_binding.json"
VALIDATION_5493 = FUNCTIONAL_RG / "5493" / "P8_Y5_BRR5492_5493_VALIDATION.csv"
SOURCE_REGISTER_5493 = FUNCTIONAL_RG / "5493" / "source_register.csv"
RESULT_5494 = FUNCTIONAL_RG / "5494" / "D4_parent_v57_post_certificate_stable_edge_axis_result.json"
V55_AUDIT_5494 = FUNCTIONAL_RG / "5494" / "D4_parent_v57_post_certificate_v55_stable_edge_audit.csv"
AXIS_AUDIT_5494 = FUNCTIONAL_RG / "5494" / "D4_parent_v57_post_certificate_stable_edge_axis_ablation.csv"
VALIDATION_5494 = FUNCTIONAL_RG / "5494" / "P8_Y5_BRR5493_5494_VALIDATION.csv"
SOURCE_REGISTER_5494 = FUNCTIONAL_RG / "5494" / "source_register.csv"

WORK_STATE = WORK / "parent_v58_complete_amplitude_cover_state.json"
LEAF_AUDIT = OUTPUT / "D4_parent_v58_complete_amplitude_leaf_audit.csv"
BINDING = OUTPUT / "D4_parent_v58_target_call_binding.json"
CERTIFICATE = OUTPUT / "D4_parent_v58_complete_amplitude_leaf_union_certificate.json"
APPLICATION_AUDIT = OUTPUT / "D4_parent_v58_certificate_application_audit.csv"
COMPARISON = OUTPUT / "D4_parent_v57_v58_target_and_control_comparison.csv"
SOURCE_REGISTER = OUTPUT / "source_register.csv"
VALIDATION = OUTPUT / "P8_Y5_BRR5494_5495_VALIDATION.csv"
STATUS = OUTPUT / "status.json"
RESULT = OUTPUT / "D4_parent_v58_resumable_complete_amplitude_gate_result.json"
DOCUMENT = POST / "5495-Y5-R2FR-D4-parent-v58-resumable-complete-amplitude-t-replacement-gate.md"

CHECKPOINT = 5495
REVISION = "D4-parent-v58-resumable-complete-amplitude-t-replacement-gate-v1"
PARENT_V57_REVISION = "D4-deformed-contour-regular-away-W3-v57-scoped-E16-X32-T128-certificate"
PARENT_V58_REVISION = "D4-deformed-contour-regular-away-W3-v58-scoped-X4-T64-plus-local-T2-certificate"
TARGET_CUBOID_ID = "E07__U051__RIGHT_CONNECTOR__CUBOID__6df3d70a73e4618b"
TARGET_REFINEMENT_PATH = "R_E0S_E0S_E0S_E1S"
EXPECTED_FAILURE_MARKER = "edge_2_1_3:stable_edge"
EXPECTED_STATE_SHA256 = "3f485d18bb2a55d3fda317091e58c0330166a7b5ae7e2185a82ab46602e23faa"
EXPECTED_RESULT_5493_SHA256 = "439347c5b5bdfa92784ef032b6125503687148f4321b54dadeb8fbafc97619d1"
EXPECTED_BINDING_5493_SHA256 = "180597828dfd42a66e81f15671959791c35fd57b2b138fd72c37700bc0a254e6"
EXPECTED_VALIDATION_5493_SHA256 = "b3505a7a14ade71b8c23b46513b823f0a60fbde6091fe27f252182b525f97c01"
EXPECTED_RESULT_5494_SHA256 = "bb624b0ce3d54699212723526ff109305a7400b34f54d9f8588095bc2c9710bd"
EXPECTED_V55_AUDIT_5494_SHA256 = "bbadfa276cfc26ca4bac7243eb037968d62f55f6de1aa67da9bc8243d6a1e725"
EXPECTED_AXIS_AUDIT_5494_SHA256 = "8b7f0208048a6bc3ff334f678124a3fac36b3cd54050cb091bfb1caabc570145"
EXPECTED_VALIDATION_5494_SHA256 = "2d0f750871ecce8e66a5411ec30bb4684b7b0aba7a516982b04a6bacc32cfa61"
PRE_REPORT_FIX_SCRIPT_SHA256 = "d4a6953a18f7ab5dfa0d72a77054ee52b1e5c9fb6d72d564041d13d677eda431"
PRE_EXPECTED_FAILURE_VALIDATION_FIX_SCRIPT_SHA256 = "6446a6bfffced2fd9b4a2dbf66894af8e99cf90654305598707fe72021dee3aa"
X_COUNT = 4
T_COUNT = 64
REPAIR_X_INDEX = 1
REPAIR_T_INDEX = 0
REPAIR_T_CHILD_COUNT = 2
EXPECTED_FINAL_LEAF_COUNT = X_COUNT * T_COUNT + REPAIR_T_CHILD_COUNT - 1
METHOD = "V58_EXACT_X4_T64_PLUS_ONE_LOCAL_T2_COMPLETE_AMPLITUDE_UNION"
METRIC_FIELDS = (
    "integrated_regular_path_abs_upper",
    "minimum_amplitude_denominator_abs_lower",
    "relative_root_abs_lower",
    "selected_global_root_abs_lower",
    "collision_jacobian_abs_lower",
)
CONTROL_FIELDS = (
    *METRIC_FIELDS,
    "active_material_branch_count",
    "active_material_branch_ids",
    "path_integral_enclosure_method",
    "reconstructed_physical_path_area_abs_upper",
    "physical_path_area_excess",
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
    return str(value).strip().lower() in {"1", "true", "yes", "pass", "passed"}


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(chunk)
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
        SCRIPT_5493,
        SCRIPT_5494,
        MANIFEST_5468,
        STATE_5484,
        RESULT_5492,
        VALIDATION_5492,
        SOURCE_REGISTER_5492,
        WORK_STATE_5492,
        LEAF_AUDIT_5492,
        RESULT_5493,
        BINDING_5493,
        VALIDATION_5493,
        SOURCE_REGISTER_5493,
        RESULT_5494,
        V55_AUDIT_5494,
        AXIS_AUDIT_5494,
        VALIDATION_5494,
        SOURCE_REGISTER_5494,
    )


def check(gate: str, passed: bool, evidence: Any) -> dict[str, Any]:
    return {
        "checkpoint": CHECKPOINT,
        "validation_gate": gate,
        "passed": bool(passed),
        "evidence": evidence,
    }


def atomic_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temporary.write_text(
        json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=True),
        encoding="utf-8",
    )
    os.replace(temporary, path)


def normalized(value: Any) -> Any:
    if value is None or isinstance(value, (bool, int, str)):
        return value
    if isinstance(value, float):
        if math.isnan(value):
            return "NaN"
        if math.isinf(value):
            return "Infinity" if value > 0.0 else "-Infinity"
        return value
    if isinstance(value, dict):
        return {
            str(key): normalized(item)
            for key, item in sorted(value.items(), key=lambda pair: str(pair[0]))
        }
    if isinstance(value, (list, tuple)):
        return [normalized(item) for item in value]
    try:
        candidate = float(value)
    except (TypeError, ValueError, OverflowError):
        return str(value)
    return normalized(candidate)


def canonical_json(value: Any) -> str:
    return json.dumps(
        normalized(value),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=True,
    )


def object_fingerprint(value: Any) -> tuple[str, str]:
    encoded = canonical_json(value)
    return hashlib.sha256(encoded.encode("utf-8")).hexdigest(), encoded


def source_snapshot(paths: tuple[Path, ...]) -> dict[str, str]:
    return {str(path): digest(path) for path in paths}


def source_register_is_current(rows: list[dict[str, str]]) -> bool:
    return bool(rows) and all(
        truth(row.get("exists"))
        and Path(row["source_path"]).is_file()
        and digest(Path(row["source_path"])) == row["sha256"]
        for row in rows
    )


def reconcile_report_only_source_transition(
    state: dict[str, Any],
    sources: dict[str, str],
) -> bool:
    previous = dict(state.get("source_snapshot", {}))
    if previous == sources:
        return False
    script_path = str(Path(__file__).resolve())
    differing = sorted(
        path
        for path in set(previous) | set(sources)
        if previous.get(path) != sources.get(path)
    )
    allowed_transitions = {
        PRE_REPORT_FIX_SCRIPT_SHA256: "REPORT_ONLY_FORMALIZATION_SNAPSHOT_EVIDENCE_KEY_FIX",
        PRE_EXPECTED_FAILURE_VALIDATION_FIX_SCRIPT_SHA256: (
            "REPORT_ONLY_EXPECTED_5493_FAILURE_VALIDATION_FIX"
        ),
    }
    previous_script_sha256 = previous.get(script_path)
    if differing != [script_path] or previous_script_sha256 not in allowed_transitions:
        raise RuntimeError("checkpoint-5495 numerical source snapshot changed")
    state.setdefault("source_transitions", []).append(
        {
            "transition_utc": datetime.now(timezone.utc).isoformat(),
            "committed_leaf_count": len(state.get("rows", [])),
            "from_script_sha256": previous[script_path],
            "to_script_sha256": sources[script_path],
            "scope": allowed_transitions[previous_script_sha256],
            "numerical_algorithm_changed": False,
        }
    )
    state["source_snapshot"] = sources
    state["last_update_utc"] = datetime.now(timezone.utc).isoformat()
    atomic_json(WORK_STATE, state)
    return True


def fresh_v57_with_v54_handle(
    base_5467: Any,
    base_5472: Any,
    base_5474: Any,
    base_5476: Any,
    base_5478: Any,
    base_5483: Any,
    base_5493: Any,
    binding: dict[str, Any],
    collision_certificate: dict[str, Any],
    module_name: str,
) -> tuple[Any, Any]:
    parent = base_5472.install_parent_v52(
        base_5472.fresh_parent(base_5467, module_name)
    )
    parent = base_5474.install_parent_v53(parent)
    parent = base_5476.install_parent_v54(parent, base_5474)
    evaluate_v54 = parent.evaluate_path_box
    parent = base_5478.install_parent_v55(parent, base_5474)
    parent = base_5483.install_parent_v56(parent, base_5472)
    parent = base_5493.install_parent_v57(parent, binding, collision_certificate)
    return parent, evaluate_v54


def target_arguments(
    stable: Any,
    parent: Any,
    cells: dict[str, Any],
    support_segments: list[dict[str, Any]],
    branches: dict[str, Any],
    cuboid: dict[str, Any],
    target: dict[str, Any],
) -> dict[str, Any]:
    return {
        "cell": cells[cuboid["mapped_cell_id"]],
        "term_id": cuboid["term_id"],
        "configurations": parent.configuration_variants(cuboid["term_id"]),
        "epsilon_row": {
            "regulator_bin_index": int(cuboid["source_epsilon_bin_index_lower"]),
            "epsilon_subdivision_index": 0,
            "epsilon_subdivision_count": 1,
            "epsilon_real_lower": float(target["epsilon_real_lower"]),
            "epsilon_real_upper": float(target["epsilon_real_upper"]),
            "epsilon_imaginary_lower": float(cuboid["epsilon_imaginary_lower"]),
            "epsilon_imaginary_upper": float(cuboid["epsilon_imaginary_upper"]),
        },
        "path_segment": cuboid["path_segment"],
        "x_lower": float(target["x_lower"]),
        "x_upper": float(target["x_upper"]),
        "t_lower": float(target["t_lower"]),
        "t_upper": float(target["t_upper"]),
        "refinement_depth": int(target["refinement_depth"]),
        "refinement_path": f"5456:{target['refinement_path']}",
        "support_segments": support_segments,
        "branches": branches,
        "global_arc_count": int(stable.GLOBAL_ARC_COUNT),
        "reduce_selector_charts": True,
    }


def call_binding(arguments: dict[str, Any]) -> tuple[str, dict[str, Any]]:
    configuration_sha256, _ = object_fingerprint(arguments["configurations"])
    cell_sha256, _ = object_fingerprint(arguments["cell"])
    epsilon_sha256, _ = object_fingerprint(arguments["epsilon_row"])
    support_sha256, _ = object_fingerprint(arguments["support_segments"])
    branches_sha256, _ = object_fingerprint(arguments["branches"])
    payload = {
        "cell_sha256": cell_sha256,
        "term_id": str(arguments["term_id"]),
        "configurations_sha256": configuration_sha256,
        "epsilon_row_sha256": epsilon_sha256,
        "path_segment": str(arguments["path_segment"]),
        "x_lower": float(arguments["x_lower"]),
        "x_upper": float(arguments["x_upper"]),
        "t_lower": float(arguments["t_lower"]),
        "t_upper": float(arguments["t_upper"]),
        "refinement_depth": int(arguments["refinement_depth"]),
        "refinement_path": str(arguments["refinement_path"]),
        "support_segments_sha256": support_sha256,
        "branches_sha256": branches_sha256,
        "global_arc_count": int(arguments["global_arc_count"]),
        "reduce_selector_charts": bool(arguments["reduce_selector_charts"]),
    }
    binding_sha256, _ = object_fingerprint(payload)
    return binding_sha256, payload


def split_edges(base_5474: Any, lower: float, upper: float, count: int) -> list[float]:
    return [float(value) for value in base_5474.exact_uniform_edges(lower, upper, count)]


def build_leaf_manifest(base_5474: Any, arguments: dict[str, Any]) -> list[dict[str, Any]]:
    x_edges = split_edges(
        base_5474,
        float(arguments["x_lower"]),
        float(arguments["x_upper"]),
        X_COUNT,
    )
    t_edges = split_edges(
        base_5474,
        float(arguments["t_lower"]),
        float(arguments["t_upper"]),
        T_COUNT,
    )
    leaves: list[dict[str, Any]] = []
    for x_index, (x_lower, x_upper) in enumerate(zip(x_edges, x_edges[1:])):
        for t_index, (t_lower, t_upper) in enumerate(zip(t_edges, t_edges[1:])):
            if x_index == REPAIR_X_INDEX and t_index == REPAIR_T_INDEX:
                repair_edges = split_edges(
                    base_5474,
                    t_lower,
                    t_upper,
                    REPAIR_T_CHILD_COUNT,
                )
                for repair_index, (child_lower, child_upper) in enumerate(
                    zip(repair_edges, repair_edges[1:])
                ):
                    leaves.append(
                        {
                            "ordinal": len(leaves),
                            "leaf_id": f"X{x_index}:T{t_index}:T2:{repair_index}",
                            "x_index": x_index,
                            "t_index": t_index,
                            "repair_child_index": repair_index,
                            "x_lower": x_lower,
                            "x_upper": x_upper,
                            "t_lower": child_lower,
                            "t_upper": child_upper,
                            "parameter_area": (x_upper - x_lower)
                            * (child_upper - child_lower),
                            "refinement_depth": int(arguments["refinement_depth"]) + 1,
                            "refinement_path": (
                                f"{arguments['refinement_path']}:V58X{X_COUNT}:{x_index}:"
                                f"T{T_COUNT}:{t_index}:T2:{repair_index}"
                            ),
                        }
                    )
            else:
                leaves.append(
                    {
                        "ordinal": len(leaves),
                        "leaf_id": f"X{x_index}:T{t_index}",
                        "x_index": x_index,
                        "t_index": t_index,
                        "repair_child_index": -1,
                        "x_lower": x_lower,
                        "x_upper": x_upper,
                        "t_lower": t_lower,
                        "t_upper": t_upper,
                        "parameter_area": (x_upper - x_lower) * (t_upper - t_lower),
                        "refinement_depth": int(arguments["refinement_depth"]) + 1,
                        "refinement_path": (
                            f"{arguments['refinement_path']}:V58X{X_COUNT}:{x_index}:"
                            f"T{T_COUNT}:{t_index}"
                        ),
                    }
                )
    return leaves


def compact_leaf_result(
    base_5474: Any,
    result: dict[str, Any],
    leaf: dict[str, Any],
) -> dict[str, Any]:
    fields = {
        "selected_role",
        "chart_roles",
        "chart_count",
        "path_speed_abs_upper",
        "active_material_branch_ids",
        "active_material_branch_count",
        "integrated_regular_path_abs_upper",
        "path_integral_enclosure_method",
        "collision_jacobian_enclosure_method",
        *base_5474.LOWER_FIELDS,
        *base_5474.UPPER_FIELDS,
    }
    compact = {
        field: normalized(result[field])
        for field in fields
        if field in result
    }
    compact.update(
        {
            "x_lower": float(leaf["x_lower"]),
            "x_upper": float(leaf["x_upper"]),
            "x_width": float(leaf["x_upper"]) - float(leaf["x_lower"]),
            "t_lower": float(leaf["t_lower"]),
            "t_upper": float(leaf["t_upper"]),
            "t_width": float(leaf["t_upper"]) - float(leaf["t_lower"]),
            "parameter_area": float(result["parameter_area"]),
            "refinement_depth": int(leaf["refinement_depth"]),
            "refinement_path": str(leaf["refinement_path"]),
        }
    )
    return compact


def evaluate_leaf(
    parent: Any,
    evaluate_v54: Any,
    base_5474: Any,
    arguments: dict[str, Any],
    leaf: dict[str, Any],
) -> dict[str, Any]:
    call = dict(arguments)
    call.update(
        {
            "x_lower": float(leaf["x_lower"]),
            "x_upper": float(leaf["x_upper"]),
            "t_lower": float(leaf["t_lower"]),
            "t_upper": float(leaf["t_upper"]),
            "refinement_depth": int(leaf["refinement_depth"]),
            "refinement_path": str(leaf["refinement_path"]),
        }
    )
    started = time.perf_counter()
    audit_start = len(parent.V57_SCOPED_CERTIFICATE_AUDIT_ROWS)
    try:
        result = evaluate_v54(**call)
        compact = compact_leaf_result(base_5474, result, leaf)
        metrics = [float(compact[field]) for field in METRIC_FIELDS]
        area_error = abs(float(compact["parameter_area"]) - float(leaf["parameter_area"]))
        passed = (
            all(math.isfinite(value) and value > 0.0 for value in metrics)
            and area_error <= 1.0e-14 * max(float(leaf["parameter_area"]), 1.0)
        )
        failure_type = "" if passed else "NonPositiveOrNonfiniteMetric"
        failure_message = "" if passed else canonical_json(dict(zip(METRIC_FIELDS, metrics)))
    except Exception as error:
        compact = {}
        area_error = math.nan
        passed = False
        failure_type = type(error).__name__
        failure_message = str(error).splitlines()[0][:600]
    new_audit = parent.V57_SCOPED_CERTIFICATE_AUDIT_ROWS[audit_start:]
    return {
        **leaf,
        "status": "PASS" if passed else "FAIL",
        "runtime_seconds": time.perf_counter() - started,
        "parameter_area_error": area_error,
        "v57_certificate_application_count": sum(
            1 for row in new_audit if row.get("status") == "APPLIED"
        ),
        "v57_scope_miss_count": sum(
            1 for row in new_audit if row.get("status") == "SCOPE_MISS"
        ),
        "failure_type": failure_type,
        "failure_message": failure_message,
        "result": compact,
    }


def initial_work_state(
    sources: dict[str, str],
    target_binding_sha256: str,
    manifest_sha256: str,
) -> dict[str, Any]:
    return {
        "checkpoint": CHECKPOINT,
        "revision": REVISION,
        "source_snapshot": sources,
        "source_state_sha256": EXPECTED_STATE_SHA256,
        "target_refinement_path": TARGET_REFINEMENT_PATH,
        "target_binding_sha256": target_binding_sha256,
        "leaf_manifest_sha256": manifest_sha256,
        "x_count": X_COUNT,
        "t_count": T_COUNT,
        "repair_x_index": REPAIR_X_INDEX,
        "repair_t_index": REPAIR_T_INDEX,
        "repair_t_child_count": REPAIR_T_CHILD_COUNT,
        "expected_final_leaf_count": EXPECTED_FINAL_LEAF_COUNT,
        "next_leaf_ordinal": 0,
        "rows": [],
        "complete": False,
        "terminal_failure": False,
        "last_update_utc": datetime.now(timezone.utc).isoformat(),
    }


def verify_work_state(
    state: dict[str, Any],
    sources: dict[str, str],
    target_binding_sha256: str,
    manifest_sha256: str,
    manifest: list[dict[str, Any]],
) -> None:
    expected = {
        "checkpoint": CHECKPOINT,
        "revision": REVISION,
        "source_snapshot": sources,
        "source_state_sha256": EXPECTED_STATE_SHA256,
        "target_refinement_path": TARGET_REFINEMENT_PATH,
        "target_binding_sha256": target_binding_sha256,
        "leaf_manifest_sha256": manifest_sha256,
        "x_count": X_COUNT,
        "t_count": T_COUNT,
        "repair_x_index": REPAIR_X_INDEX,
        "repair_t_index": REPAIR_T_INDEX,
        "repair_t_child_count": REPAIR_T_CHILD_COUNT,
        "expected_final_leaf_count": EXPECTED_FINAL_LEAF_COUNT,
    }
    for key, value in expected.items():
        if state.get(key) != value:
            raise RuntimeError(f"checkpoint-5495 work state mismatch at {key}")
    next_ordinal = int(state.get("next_leaf_ordinal", -1))
    rows = list(state.get("rows", []))
    if next_ordinal != len(rows) or next_ordinal > len(manifest):
        raise RuntimeError("checkpoint-5495 committed prefix length mismatch")
    for ordinal, row in enumerate(rows):
        if int(row.get("ordinal", -1)) != ordinal:
            raise RuntimeError("checkpoint-5495 row ordinal mismatch")
        if row.get("leaf_id") != manifest[ordinal]["leaf_id"]:
            raise RuntimeError("checkpoint-5495 row identity mismatch")
    failures = [row for row in rows if row.get("status") != "PASS"]
    if bool(state.get("terminal_failure")) != bool(failures):
        raise RuntimeError("checkpoint-5495 terminal failure flag mismatch")


def aggregate_cover(
    base_5474: Any,
    rows: list[dict[str, Any]],
    arguments: dict[str, Any],
) -> tuple[dict[str, Any], float]:
    results = [dict(row["result"]) for row in rows]
    original_area = (
        float(arguments["x_upper"]) - float(arguments["x_lower"])
    ) * (float(arguments["t_upper"]) - float(arguments["t_lower"]))
    covered_area = math.fsum(float(result["parameter_area"]) for result in results)
    coverage_error = abs(covered_area - original_area)
    if coverage_error > 1.0e-12 * max(original_area, 1.0):
        raise RuntimeError("parent-v58 exact cover does not preserve target area")
    denominator_lower = min(
        float(result["minimum_amplitude_denominator_abs_lower"])
        for result in results
    )
    aggregate = base_5474.aggregate_leaf_results(
        results,
        float(arguments["x_lower"]),
        float(arguments["x_upper"]),
        float(arguments["t_lower"]),
        float(arguments["t_upper"]),
        int(arguments["refinement_depth"]),
        str(arguments["refinement_path"]),
        denominator_lower,
        coverage_error,
    )
    aggregate.pop("v53_stable_edge_t_leaf_count", None)
    aggregate.pop("v53_left_first_soft_invariant_abs_lower", None)
    aggregate.pop("v53_parameter_area_coverage_error", None)
    aggregate.update(
        {
            "selected_role": "EXACT_XT_PLUS_LOCAL_T_LEAF_UNION",
            "path_integral_enclosure_method": METHOD,
            "v58_base_x_count": X_COUNT,
            "v58_base_t_count": T_COUNT,
            "v58_repair_x_index": REPAIR_X_INDEX,
            "v58_repair_t_index": REPAIR_T_INDEX,
            "v58_repair_t_child_count": REPAIR_T_CHILD_COUNT,
            "v58_complete_amplitude_leaf_count": len(results),
            "v58_parent_amplitude_denominator_abs_lower": denominator_lower,
            "v58_parameter_area_coverage_error": coverage_error,
        }
    )
    return normalized(aggregate), coverage_error


def install_parent_v58(
    parent: Any,
    target_binding_sha256: str,
    aggregate: dict[str, Any],
) -> Any:
    if parent.REVISION != PARENT_V57_REVISION:
        raise RuntimeError(
            f"expected parent revision {PARENT_V57_REVISION}, found {parent.REVISION}"
        )
    original = parent.evaluate_path_box
    audit_rows: list[dict[str, Any]] = []

    def evaluate_v58(
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
        current_sha256, _ = call_binding(arguments)
        if current_sha256 != target_binding_sha256:
            return original(**arguments)
        audit_rows.append(
            {
                "status": "APPLIED",
                "method": METHOD,
                "target_binding_sha256": target_binding_sha256,
                "current_binding_sha256": current_sha256,
                "x_lower": x_lower,
                "x_upper": x_upper,
                "t_lower": t_lower,
                "t_upper": t_upper,
                "complete_amplitude_leaf_count": EXPECTED_FINAL_LEAF_COUNT,
                "minimum_amplitude_denominator_abs_lower": aggregate[
                    "minimum_amplitude_denominator_abs_lower"
                ],
                "collision_jacobian_abs_lower": aggregate[
                    "collision_jacobian_abs_lower"
                ],
                "parameter_area_coverage_error": aggregate[
                    "v58_parameter_area_coverage_error"
                ],
            }
        )
        result = dict(aggregate)
        result.update(
            {
                "x_lower": x_lower,
                "x_upper": x_upper,
                "x_width": x_upper - x_lower,
                "t_lower": t_lower,
                "t_upper": t_upper,
                "t_width": t_upper - t_lower,
                "parameter_area": (x_upper - x_lower) * (t_upper - t_lower),
                "refinement_depth": refinement_depth,
                "refinement_path": refinement_path,
            }
        )
        return result

    parent.evaluate_path_box = evaluate_v58
    parent.V58_COMPLETE_AMPLITUDE_CERTIFICATE_AUDIT_ROWS = audit_rows
    parent.V58_PARENT_ACTION_CHANGED = False
    parent.V58_ONLY_ENCLOSURE_COMPOSITION_CHANGED = True
    parent.REVISION = PARENT_V58_REVISION
    return parent


def result_row(role: str, result: dict[str, Any], revision: str) -> dict[str, Any]:
    return {
        "role": role,
        "parent_revision": revision,
        "probe_passed": result.get("probe_passed"),
        "failure_type": result.get("failure_type", ""),
        "failure_message": result.get("failure_message", ""),
        **{field: result.get(field) for field in CONTROL_FIELDS},
    }


def leaf_audit_rows(state: dict[str, Any]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in state.get("rows", []):
        result = source.get("result", {})
        rows.append(
            {
                **{key: value for key, value in source.items() if key != "result"},
                **{field: result.get(field, math.nan) for field in METRIC_FIELDS},
                "path_speed_abs_upper": result.get("path_speed_abs_upper", math.nan),
                "active_material_branch_count": result.get(
                    "active_material_branch_count", -1
                ),
                "active_material_branch_ids": result.get(
                    "active_material_branch_ids", ""
                ),
                "path_integral_enclosure_method": result.get(
                    "path_integral_enclosure_method", ""
                ),
            }
        )
    return rows


def render_document(payload: dict[str, Any], base_5467: Any) -> None:
    lines = [
        "# 5495: D4 parent-v58 resumable complete-amplitude t-replacement gate",
        "",
        "## Exact construction",
        "",
        "The unchanged parent-v54 complete amplitude is evaluated on the parent-v55 `X4 x T64` target cover. Only the source-identified failed leaf `X1:T0` is replaced by its checkpoint-5494-proved exact `T2` children. The final union has 257 leaves and exactly equals the target x/t rectangle.",
        "",
        f"Committed leaves: `{payload['committed_leaf_count']}/{payload['expected_final_leaf_count']}`. Terminal failure: `{payload['terminal_failure']}`. Exact cover complete: `{payload['candidate_cover_complete']}`.",
        "",
        f"Minimum complete-amplitude denominator lower: `{payload['candidate_amplitude_denominator_abs_lower']}`. Minimum relative-root lower: `{payload['candidate_relative_root_abs_lower']}`. Minimum selected-global-root lower: `{payload['candidate_selected_global_root_abs_lower']}`. Minimum collision-Jacobian lower: `{payload['candidate_collision_jacobian_abs_lower']}`.",
        "",
        f"Parent-v58 target passed: `{payload['target_v58_passed']}`. Certificate applications: `{payload['v58_target_application_count']}`. Untriggered parent-v57/parent-v58 control exactly unchanged: `{payload['control_v57_v58_identical']}`.",
        "",
        "## Decision",
        "",
        f"**{payload['decision']}**",
        "",
        "## Claim boundary",
        "",
        "This checkpoint changes only exact enclosure composition. It does not alter the action, contour, chart candidates, selector, residues or thresholds. Until the 257-leaf union and target/control gate close, parent v58 is not certified. Full outer enclosure, event-local or combined W3, the regulator limit, all-operator local GR and full MTS remain open.",
        "",
    ]
    base_5467.atomic_text(DOCUMENT, "\n".join(lines))


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-leaves", type=int, default=EXPECTED_FINAL_LEAF_COUNT)
    parser.add_argument("--max-runtime-seconds", type=float, default=12600.0)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> int:
    arguments_cli = parse_arguments()
    if arguments_cli.max_leaves < 1:
        raise ValueError("max-leaves must be positive")
    if arguments_cli.max_runtime_seconds <= 0.0:
        raise ValueError("max-runtime-seconds must be positive")
    base_5467 = load_module("mts_5467_for_5495", SCRIPT_5467)
    base_5468 = load_module("mts_5468_for_5495", SCRIPT_5468)
    base_5469 = load_module("mts_5469_for_5495", SCRIPT_5469)
    base_5472 = load_module("mts_5472_for_5495", SCRIPT_5472)
    base_5474 = load_module("mts_5474_for_5495", SCRIPT_5474)
    base_5476 = load_module("mts_5476_for_5495", SCRIPT_5476)
    base_5478 = load_module("mts_5478_for_5495", SCRIPT_5478)
    base_5480 = load_module("mts_5480_for_5495", SCRIPT_5480)
    base_5483 = load_module("mts_5483_for_5495", SCRIPT_5483)
    base_5490 = load_module("mts_5490_for_5495", SCRIPT_5490)
    base_5493 = load_module("mts_5493_for_5495", SCRIPT_5493)
    base_5467.set_below_normal_priority()
    base_5480.set_single_core_affinity()
    before_formalization = base_5467.formalization_snapshot()
    paths = source_paths()
    missing = [str(path) for path in paths if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"missing sources: {missing}")
    inherited_hashes = {
        "state_5484": digest(STATE_5484),
        "result_5493": digest(RESULT_5493),
        "binding_5493": digest(BINDING_5493),
        "validation_5493": digest(VALIDATION_5493),
        "result_5494": digest(RESULT_5494),
        "v55_audit_5494": digest(V55_AUDIT_5494),
        "axis_audit_5494": digest(AXIS_AUDIT_5494),
        "validation_5494": digest(VALIDATION_5494),
    }
    expected_hashes = {
        "state_5484": EXPECTED_STATE_SHA256,
        "result_5493": EXPECTED_RESULT_5493_SHA256,
        "binding_5493": EXPECTED_BINDING_5493_SHA256,
        "validation_5493": EXPECTED_VALIDATION_5493_SHA256,
        "result_5494": EXPECTED_RESULT_5494_SHA256,
        "v55_audit_5494": EXPECTED_V55_AUDIT_5494_SHA256,
        "axis_audit_5494": EXPECTED_AXIS_AUDIT_5494_SHA256,
        "validation_5494": EXPECTED_VALIDATION_5494_SHA256,
    }
    if inherited_hashes != expected_hashes:
        raise RuntimeError("checkpoint-5495 inherited source hash mismatch")
    result_5492 = read_json(RESULT_5492)
    work_state_5492 = read_json(WORK_STATE_5492)
    leaf_rows_5492 = read_csv(LEAF_AUDIT_5492)
    result_5494 = read_json(RESULT_5494)
    v55_rows_5494 = read_csv(V55_AUDIT_5494)
    axis_rows_5494 = read_csv(AXIS_AUDIT_5494)
    validation_5493 = read_csv(VALIDATION_5493)
    validation_5494 = read_csv(VALIDATION_5494)
    source_register_5492 = read_csv(SOURCE_REGISTER_5492)
    source_register_5493 = read_csv(SOURCE_REGISTER_5493)
    source_register_5494 = read_csv(SOURCE_REGISTER_5494)
    failed_validation_5493 = [
        row for row in validation_5493 if not truth(row.get("passed"))
    ]
    validation_5493_has_expected_target_failure_only = (
        len(failed_validation_5493) == 1
        and failed_validation_5493[0].get("validation_gate")
        == "v57_complete_parent_target_is_finite"
    )
    binding_5493 = read_json(BINDING_5493)
    state_5484 = read_json(STATE_5484)
    cuboid = next(
        row
        for row in read_csv(MANIFEST_5468)
        if row["cuboid_job_id"] == TARGET_CUBOID_ID
    )
    target_candidates = [
        row
        for row in state_5484["refinement_witnesses"]
        if row.get("refinement_path") == TARGET_REFINEMENT_PATH
    ]
    if len(target_candidates) != 1:
        raise RuntimeError(f"expected one target witness, found {len(target_candidates)}")
    target = target_candidates[0]
    control_candidates = [
        row
        for row in state_5484["accepted"]
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
    collision_certificate = base_5493.build_certificate(
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
        binding_5493,
        collision_certificate,
        "mts_parent_v57_work_5495",
    )
    target_call = target_arguments(
        stable,
        parent,
        cells,
        support_segments,
        branches,
        cuboid,
        target,
    )
    target_binding_sha256, target_binding = call_binding(target_call)
    manifest = build_leaf_manifest(base_5474, target_call)
    manifest_sha256, _ = object_fingerprint(manifest)
    repair_leaves = [row for row in manifest if int(row["repair_child_index"]) >= 0]
    expected_failed_leaf = next(
        row
        for row in v55_rows_5494
        if row.get("row_type") == "leaf"
        and row.get("status") == "FAIL"
        and int(row["x_count"]) == X_COUNT
        and int(row["t_count"]) == T_COUNT
    )
    selected_axis = next(
        row
        for row in axis_rows_5494
        if row.get("axis") == "t"
        and int(row["count"]) == REPAIR_T_CHILD_COUNT
        and row.get("status") == "PASS"
    )
    derivation_source_signed = (
        truth(result_5494.get("target_stable_edge_failure_reproduced"))
        and result_5494.get("selected_axis") == "t"
        and int(result_5494.get("selected_axis_count", 0)) == REPAIR_T_CHILD_COUNT
        and int(expected_failed_leaf["x_index"]) == REPAIR_X_INDEX
        and int(expected_failed_leaf["t_index"]) == REPAIR_T_INDEX
        and float(repair_leaves[0]["x_lower"]) == float(expected_failed_leaf["x_lower"])
        and float(repair_leaves[-1]["x_upper"]) == float(expected_failed_leaf["x_upper"])
        and float(repair_leaves[0]["t_lower"]) == float(expected_failed_leaf["t_lower"])
        and float(repair_leaves[-1]["t_upper"]) == float(expected_failed_leaf["t_upper"])
        and float(selected_axis["coverage_error"]) == 0.0
        and all(truth(row.get("passed")) for row in validation_5494)
    )
    if not derivation_source_signed:
        raise RuntimeError("checkpoint-5494 t-replacement derivation is not source-signed")
    if len(manifest) != EXPECTED_FINAL_LEAF_COUNT:
        raise RuntimeError("checkpoint-5495 leaf manifest has the wrong size")
    if arguments_cli.dry_run:
        print(
            json.dumps(
                {
                    "checkpoint": CHECKPOINT,
                    "dry_run": True,
                    "target_binding_sha256": target_binding_sha256,
                    "leaf_manifest_sha256": manifest_sha256,
                    "final_leaf_count": len(manifest),
                    "repair_leaf_ids": [row["leaf_id"] for row in repair_leaves],
                    "derivation_source_signed": derivation_source_signed,
                },
                indent=2,
            )
        )
        return 0
    sources = source_snapshot(paths)
    WORK.mkdir(parents=True, exist_ok=True)
    state = (
        read_json(WORK_STATE)
        if WORK_STATE.is_file()
        else initial_work_state(
            sources,
            target_binding_sha256,
            manifest_sha256,
        )
    )
    report_only_source_transition = reconcile_report_only_source_transition(
        state,
        sources,
    )
    verify_work_state(
        state,
        sources,
        target_binding_sha256,
        manifest_sha256,
        manifest,
    )
    if not WORK_STATE.is_file():
        atomic_json(WORK_STATE, state)
    run_started = time.perf_counter()
    evaluated_this_run = 0
    while (
        int(state["next_leaf_ordinal"]) < len(manifest)
        and not bool(state["terminal_failure"])
        and evaluated_this_run < arguments_cli.max_leaves
    ):
        if (
            evaluated_this_run > 0
            and time.perf_counter() - run_started >= arguments_cli.max_runtime_seconds
        ):
            break
        ordinal = int(state["next_leaf_ordinal"])
        row = evaluate_leaf(
            parent,
            evaluate_v54,
            base_5474,
            target_call,
            manifest[ordinal],
        )
        state["rows"].append(row)
        state["next_leaf_ordinal"] = ordinal + 1
        state["terminal_failure"] = row["status"] != "PASS"
        state["complete"] = (
            state["next_leaf_ordinal"] == len(manifest)
            and not state["terminal_failure"]
        )
        state["last_update_utc"] = datetime.now(timezone.utc).isoformat()
        state["last_run_seconds"] = time.perf_counter() - run_started
        state["last_run_evaluated_leaf_count"] = evaluated_this_run + 1
        atomic_json(WORK_STATE, state)
        evaluated_this_run += 1
    rows = list(state["rows"])
    complete = bool(state["complete"])
    terminal_failure = bool(state["terminal_failure"])
    aggregate: dict[str, Any] | None = None
    coverage_error = math.nan
    if complete:
        aggregate, coverage_error = aggregate_cover(base_5474, rows, target_call)
    target_v58: dict[str, Any] = {}
    control_v57: dict[str, Any] = {}
    control_v58: dict[str, Any] = {}
    target_application_rows: list[dict[str, Any]] = []
    control_application_rows: list[dict[str, Any]] = []
    control_identical = False
    target_binding_preflight = False
    if aggregate is not None:
        parent_v58_target, _ = fresh_v57_with_v54_handle(
            base_5467,
            base_5472,
            base_5474,
            base_5476,
            base_5478,
            base_5483,
            base_5493,
            binding_5493,
            collision_certificate,
            "mts_parent_v58_target_5495",
        )
        preflight_call = target_arguments(
            stable,
            parent_v58_target,
            cells,
            support_segments,
            branches,
            cuboid,
            target,
        )
        preflight_sha256, _ = call_binding(preflight_call)
        target_binding_preflight = preflight_sha256 == target_binding_sha256
        if not target_binding_preflight:
            raise RuntimeError("parent-v58 target binding preflight mismatch")
        parent_v58_target = install_parent_v58(
            parent_v58_target,
            target_binding_sha256,
            aggregate,
        )
        target_v58 = base_5469.evaluate_node(
            base_5468,
            stable,
            parent_v58_target,
            cells,
            support_segments,
            branches,
            cuboid,
            target,
        )
        target_application_rows = list(
            parent_v58_target.V58_COMPLETE_AMPLITUDE_CERTIFICATE_AUDIT_ROWS
        )
        parent_v57_control, _ = fresh_v57_with_v54_handle(
            base_5467,
            base_5472,
            base_5474,
            base_5476,
            base_5478,
            base_5483,
            base_5493,
            binding_5493,
            collision_certificate,
            "mts_parent_v57_control_5495",
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
        parent_v58_control, _ = fresh_v57_with_v54_handle(
            base_5467,
            base_5472,
            base_5474,
            base_5476,
            base_5478,
            base_5483,
            base_5493,
            binding_5493,
            collision_certificate,
            "mts_parent_v58_control_5495",
        )
        parent_v58_control = install_parent_v58(
            parent_v58_control,
            target_binding_sha256,
            aggregate,
        )
        control_v58 = base_5469.evaluate_node(
            base_5468,
            stable,
            parent_v58_control,
            cells,
            support_segments,
            branches,
            cuboid,
            control,
        )
        control_application_rows = list(
            parent_v58_control.V58_COMPLETE_AMPLITUDE_CERTIFICATE_AUDIT_ROWS
        )
        control_identical = (
            truth(control_v57.get("probe_passed"))
            and truth(control_v58.get("probe_passed"))
            and all(control_v57.get(field) == control_v58.get(field) for field in CONTROL_FIELDS)
            and not control_application_rows
        )
    candidate_metrics = {
        field: (
            float(aggregate[field])
            if aggregate is not None and field in aggregate
            else math.nan
        )
        for field in METRIC_FIELDS
    }
    target_v58_passed = truth(target_v58.get("probe_passed"))
    source_v57_failure_locked = (
        derivation_source_signed
        and truth(result_5494.get("target_stable_edge_failure_reproduced"))
    )
    preliminary_certified = (
        complete
        and not terminal_failure
        and aggregate is not None
        and all(
            math.isfinite(value) and value > 0.0
            for value in candidate_metrics.values()
        )
        and coverage_error == 0.0
        and target_binding_preflight
        and target_v58_passed
        and len(target_application_rows) == 1
        and control_identical
        and source_v57_failure_locked
    )
    committed_prefix_exact = len(rows) == int(state["next_leaf_ordinal"]) and all(
        int(row["ordinal"]) == ordinal
        and row["leaf_id"] == manifest[ordinal]["leaf_id"]
        for ordinal, row in enumerate(rows)
    )
    committed_rows_numeric = all(
        row["status"] == "FAIL"
        or (
            all(
                math.isfinite(float(row["result"][field]))
                and float(row["result"][field]) > 0.0
                for field in METRIC_FIELDS
            )
            and int(row["v57_scope_miss_count"]) == 0
        )
        for row in rows
    )
    exact_manifest_area = math.fsum(float(row["parameter_area"]) for row in manifest)
    target_area = (
        float(target_call["x_upper"]) - float(target_call["x_lower"])
    ) * (float(target_call["t_upper"]) - float(target_call["t_lower"]))
    manifest_coverage_error = abs(exact_manifest_area - target_area)
    after_formalization = base_5467.formalization_snapshot()
    source_rows = [
        {
            "source_path": str(path),
            "sha256": digest(path),
            "exists": path.is_file(),
        }
        for path in paths
    ]
    validations = [
        check("all_sources_exist", not missing, len(paths)),
        check(
            "inherited_sources_are_hash_locked",
            inherited_hashes == expected_hashes,
            inherited_hashes,
        ),
        check(
            "previous_source_registers_are_current",
            source_register_is_current(source_register_5492)
            and source_register_is_current(source_register_5493)
            and source_register_is_current(source_register_5494),
            "5492/5493/5494",
        ),
        check(
            "previous_validation_rows_pass",
            validation_5493_has_expected_target_failure_only
            and all(truth(row.get("passed")) for row in validation_5494),
            (
                f"5493_expected_failure_count={len(failed_validation_5493)};"
                f"5494={len(validation_5494)}"
            ),
        ),
        check(
            "checkpoint_5494_derives_exact_local_t2_replacement",
            derivation_source_signed,
            [row["leaf_id"] for row in repair_leaves],
        ),
        check(
            "final_leaf_manifest_is_exact",
            len(manifest) == EXPECTED_FINAL_LEAF_COUNT
            and len(repair_leaves) == REPAIR_T_CHILD_COUNT
            and manifest_coverage_error == 0.0,
            f"leaves={len(manifest)};coverage_error={manifest_coverage_error}",
        ),
        check(
            "work_state_is_source_locked_and_prefix_exact",
            state["source_snapshot"] == sources and committed_prefix_exact,
            f"committed={len(rows)};report_only_transition={report_only_source_transition}",
        ),
        check(
            "committed_complete_amplitude_rows_are_numeric",
            committed_rows_numeric,
            len(rows),
        ),
        check(
            "work_outcome_is_internally_consistent",
            (
                complete
                and len(rows) == EXPECTED_FINAL_LEAF_COUNT
                and not terminal_failure
            )
            or (
                terminal_failure
                and bool(rows)
                and rows[-1]["status"] == "FAIL"
                and not complete
            )
            or (
                not complete
                and not terminal_failure
                and len(rows) < EXPECTED_FINAL_LEAF_COUNT
            ),
            f"complete={complete};terminal={terminal_failure};rows={len(rows)}",
        ),
        check(
            "complete_cover_has_positive_finite_metrics",
            not complete
            or (
                all(
                    math.isfinite(value) and value > 0.0
                    for value in candidate_metrics.values()
                )
                and coverage_error == 0.0
            ),
            candidate_metrics,
        ),
        check(
            "parent_v58_target_control_gate_matches_cover_state",
            not complete
            or (
                target_binding_preflight
                and target_v58_passed
                and len(target_application_rows) == 1
                and control_identical
            ),
            f"target={target_v58_passed};applications={len(target_application_rows)};control={control_identical}",
        ),
        check(
            "only_enclosure_composition_changes",
            not complete
            or (
                not parent_v58_target.V58_PARENT_ACTION_CHANGED
                and parent_v58_target.V58_ONLY_ENCLOSURE_COMPOSITION_CHANGED
            ),
            PARENT_V58_REVISION,
        ),
        check(
            "formalization_workbench_untouched",
            before_formalization == after_formalization,
            f"before={len(before_formalization)};after={len(after_formalization)}",
        ),
        check(
            "broad_claims_remain_false",
            True,
            "one active-cuboid target gate only",
        ),
    ]
    failed_validations = [row for row in validations if not row["passed"]]
    certified = preliminary_certified and not failed_validations
    if certified:
        decision = "PARENT_V58_COMPLETE_AMPLITUDE_T_REPLACEMENT_CERTIFIED__MIGRATE_FRONTIER"
        next_target = "CREATE_HASH_LOCKED_PARENT_V58_CARRY_FORWARD_OF_CHECKPOINT_5484_STATE"
    elif terminal_failure:
        decision = "PARENT_V58_COMPLETE_AMPLITUDE_T_REPLACEMENT_REJECTED__DERIVE_NEXT_FAILED_LEAF"
        next_target = "DERIVE_EXACT_REPAIR_FOR_CHECKPOINT_5495_TERMINAL_LEAF"
    elif not complete:
        decision = "PARENT_V58_COMPLETE_AMPLITUDE_T_REPLACEMENT_PARTIAL__RESUME"
        next_target = "RESUME_CHECKPOINT_5495_COMPLETE_AMPLITUDE_LEAF_COVER"
    else:
        decision = "PARENT_V58_COMPLETE_AMPLITUDE_T_REPLACEMENT_NOT_CERTIFIED"
        next_target = "AUDIT_CHECKPOINT_5495_FAILED_ACCEPTANCE_GATE"
    work_state_sha256 = digest(WORK_STATE)
    certificate_payload: dict[str, Any] = {}
    if aggregate is not None:
        certificate_payload = {
            "checkpoint": CHECKPOINT,
            "revision": REVISION,
            "method": METHOD,
            "target_binding_sha256": target_binding_sha256,
            "leaf_manifest_sha256": manifest_sha256,
            "work_state_sha256": work_state_sha256,
            "final_leaf_count": len(rows),
            "x_count": X_COUNT,
            "t_count": T_COUNT,
            "repair_x_index": REPAIR_X_INDEX,
            "repair_t_index": REPAIR_T_INDEX,
            "repair_t_child_count": REPAIR_T_CHILD_COUNT,
            "parameter_area_coverage_error": coverage_error,
            "aggregate_result": aggregate,
        }
        atomic_json(CERTIFICATE, certificate_payload)
    payload = {
        "checkpoint": CHECKPOINT,
        "revision": REVISION,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "decision": decision,
        "next_target": next_target,
        "target_cuboid_id": TARGET_CUBOID_ID,
        "target_refinement_path": TARGET_REFINEMENT_PATH,
        "target_binding_sha256": target_binding_sha256,
        "leaf_manifest_sha256": manifest_sha256,
        "work_state_sha256": work_state_sha256,
        "committed_leaf_count": len(rows),
        "expected_final_leaf_count": EXPECTED_FINAL_LEAF_COUNT,
        "remaining_leaf_count": EXPECTED_FINAL_LEAF_COUNT - len(rows),
        "last_run_evaluated_leaf_count": evaluated_this_run,
        "last_run_seconds": time.perf_counter() - run_started,
        "report_only_source_transition_applied": report_only_source_transition,
        "candidate_cover_complete": complete,
        "terminal_failure": terminal_failure,
        "terminal_failure_leaf_id": (
            rows[-1]["leaf_id"] if terminal_failure and rows else ""
        ),
        "terminal_failure_type": (
            rows[-1]["failure_type"] if terminal_failure and rows else ""
        ),
        "terminal_failure_message": (
            rows[-1]["failure_message"] if terminal_failure and rows else ""
        ),
        "manifest_parameter_area_coverage_error": manifest_coverage_error,
        "candidate_parameter_area_coverage_error": coverage_error,
        "candidate_integrated_regular_path_abs_upper": candidate_metrics[
            "integrated_regular_path_abs_upper"
        ],
        "candidate_amplitude_denominator_abs_lower": candidate_metrics[
            "minimum_amplitude_denominator_abs_lower"
        ],
        "candidate_relative_root_abs_lower": candidate_metrics[
            "relative_root_abs_lower"
        ],
        "candidate_selected_global_root_abs_lower": candidate_metrics[
            "selected_global_root_abs_lower"
        ],
        "candidate_collision_jacobian_abs_lower": candidate_metrics[
            "collision_jacobian_abs_lower"
        ],
        "source_v57_stable_edge_failure_locked": source_v57_failure_locked,
        "target_binding_preflight": target_binding_preflight,
        "target_v58_passed": target_v58_passed,
        "v58_target_application_count": len(target_application_rows),
        "v58_control_application_count": len(control_application_rows),
        "control_refinement_path": control["refinement_path"],
        "control_v57_v58_identical": control_identical,
        "parent_action_changed": False,
        "validation_row_count": len(validations),
        "failed_validation_count": len(failed_validations),
        "valid_for_parent_v58_complete_amplitude_t_replacement": certified,
        "valid_for_parent_v58_active_cuboid": False,
        "valid_for_full_outer_parent_leaf_enclosure": False,
        "valid_for_D4_event_local_W3_bound": False,
        "valid_for_all_operator_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    OUTPUT.mkdir(parents=True, exist_ok=True)
    base_5467.atomic_csv(LEAF_AUDIT, leaf_audit_rows(state))
    atomic_json(
        BINDING,
        {
            "checkpoint": CHECKPOINT,
            "target_binding_sha256": target_binding_sha256,
            "target_binding": target_binding,
            "leaf_manifest_sha256": manifest_sha256,
            "final_leaf_count": len(manifest),
            "repair_leaf_ids": [row["leaf_id"] for row in repair_leaves],
        },
    )
    base_5467.atomic_csv(APPLICATION_AUDIT, target_application_rows)
    comparison_rows: list[dict[str, Any]] = []
    if aggregate is not None:
        comparison_rows = [
            {
                "role": "source_target_v57",
                "parent_revision": PARENT_V57_REVISION,
                "probe_passed": False,
                "failure_type": "IntervalSingularity",
                "failure_message": EXPECTED_FAILURE_MARKER,
            },
            result_row("target_v58", target_v58, PARENT_V58_REVISION),
            result_row("untriggered_control_v57", control_v57, PARENT_V57_REVISION),
            result_row("untriggered_control_v58", control_v58, PARENT_V58_REVISION),
        ]
    base_5467.atomic_csv(COMPARISON, comparison_rows)
    base_5467.atomic_csv(SOURCE_REGISTER, source_rows)
    base_5467.atomic_csv(VALIDATION, validations)
    atomic_json(STATUS, payload)
    atomic_json(RESULT, payload)
    render_document(payload, base_5467)
    print(
        json.dumps(
            {
                key: payload[key]
                for key in (
                    "decision",
                    "committed_leaf_count",
                    "expected_final_leaf_count",
                    "remaining_leaf_count",
                    "last_run_evaluated_leaf_count",
                    "last_run_seconds",
                    "candidate_cover_complete",
                    "terminal_failure",
                    "terminal_failure_leaf_id",
                    "candidate_amplitude_denominator_abs_lower",
                    "candidate_collision_jacobian_abs_lower",
                    "target_v58_passed",
                    "control_v57_v58_identical",
                    "failed_validation_count",
                    "next_target",
                )
            },
            indent=2,
        )
    )
    return 0 if not failed_validations else 1


if __name__ == "__main__":
    raise SystemExit(main())
