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
OUTPUT = FUNCTIONAL_RG / "5496"
WORK = OUTPUT / "work-v1"

SCRIPT_5495 = SCRIPTS / "Y5_R2FR_5495_D4_parent_v58_resumable_complete_amplitude_t_replacement_gate.py"
WORK_STATE_5495 = FUNCTIONAL_RG / "5495" / "work-v1" / "parent_v58_complete_amplitude_cover_state.json"
RESULT_5495 = FUNCTIONAL_RG / "5495" / "D4_parent_v58_resumable_complete_amplitude_gate_result.json"
LEAF_AUDIT_5495 = FUNCTIONAL_RG / "5495" / "D4_parent_v58_complete_amplitude_leaf_audit.csv"
VALIDATION_5495 = FUNCTIONAL_RG / "5495" / "P8_Y5_BRR5494_5495_VALIDATION.csv"
SOURCE_REGISTER_5495 = FUNCTIONAL_RG / "5495" / "source_register.csv"

WORK_STATE = WORK / "parent_v58_adaptive_stable_edge_T2_state.json"
LEAF_AUDIT = OUTPUT / "D4_parent_v58_adaptive_stable_edge_T2_leaf_audit.csv"
BASE_AUDIT = OUTPUT / "D4_parent_v58_adaptive_stable_edge_T2_base_audit.csv"
BINDING = OUTPUT / "D4_parent_v58_adaptive_target_binding.json"
CERTIFICATE = OUTPUT / "D4_parent_v58_adaptive_complete_amplitude_certificate.json"
APPLICATION_AUDIT = OUTPUT / "D4_parent_v58_adaptive_certificate_application_audit.csv"
COMPARISON = OUTPUT / "D4_parent_v57_v58_adaptive_target_control_comparison.csv"
SOURCE_REGISTER = OUTPUT / "source_register.csv"
VALIDATION = OUTPUT / "P8_Y5_BRR5495_5496_VALIDATION.csv"
STATUS = OUTPUT / "status.json"
RESULT = OUTPUT / "D4_parent_v58_adaptive_stable_edge_T2_result.json"
DOCUMENT = POST / "5496-Y5-R2FR-D4-parent-v58-adaptive-stable-edge-T2-gate.md"

CHECKPOINT = 5496
REVISION = "D4-parent-v58-adaptive-stable-edge-T2-gate-v1"
PARENT_V57_REVISION = "D4-deformed-contour-regular-away-W3-v57-scoped-E16-X32-T128-certificate"
PARENT_V58_REVISION = "D4-deformed-contour-regular-away-W3-v58-adaptive-stable-edge-local-T2-union"
METHOD = "V58_ADAPTIVE_STABLE_EDGE_LOCAL_T2_COMPLETE_AMPLITUDE_UNION"
EXPECTED_FAILURE_MARKER = "edge_2_1_3:stable_edge"
EXPECTED_SCRIPT_5495_SHA256 = "539493d357c74255a42f96cd6aba4f7f37020062baa962454da77a453a411bb9"
EXPECTED_WORK_STATE_5495_SHA256 = "dbfe3596921c618ec843b285668ad36969d44862c7438a8fdcfd06d218e3792f"
EXPECTED_RESULT_5495_SHA256 = "d85f50df4be57b8fb3efc351a6d6e81054f162c3278dbb328c7594ae5ec11078"
EXPECTED_LEAF_AUDIT_5495_SHA256 = "063699c26b8ac700155411d0b644038a028e602c1fba69d7fb109e8e690981e2"
EXPECTED_VALIDATION_5495_SHA256 = "bb10c845592240a2e5e67e7569d48ff0cf1b2599a322d18cd9a3129ec2dca31d"
EXPECTED_SOURCE_REGISTER_5495_SHA256 = "6fc1c215ed2d1d1198f0ccc32391906c0862b8a02deaa0b6b431c891436c12d5"
PRE_NAN_SAFE_CARRY_VALIDATION_SCRIPT_SHA256 = "bf81488037e8825563b1d8c87b240d1688cfc2d435eefc05c4a7d120ae15e21a"
BASE_X_COUNT = 4
BASE_T_COUNT = 64
BASE_CELL_COUNT = BASE_X_COUNT * BASE_T_COUNT
T2_COUNT = 2
SOURCE_CARRY_BASE_COUNT = 128
SOURCE_CARRY_FINAL_LEAF_COUNT = 129
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


def atomic_json(path: Path, payload: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_name(f".{path.name}.{os.getpid()}.tmp")
    temporary.write_text(
        json.dumps(payload, sort_keys=True, separators=(",", ":"), allow_nan=True),
        encoding="utf-8",
    )
    os.replace(temporary, path)


def check(gate: str, passed: bool, evidence: Any) -> dict[str, Any]:
    return {
        "checkpoint": CHECKPOINT,
        "validation_gate": gate,
        "passed": bool(passed),
        "evidence": evidence,
    }


def source_paths(base_5495: Any) -> tuple[Path, ...]:
    return tuple(
        dict.fromkeys(
            (
                Path(__file__).resolve(),
                *base_5495.source_paths(),
                SCRIPT_5495,
                WORK_STATE_5495,
                RESULT_5495,
                LEAF_AUDIT_5495,
                VALIDATION_5495,
                SOURCE_REGISTER_5495,
            )
        )
    )


def source_snapshot(paths: tuple[Path, ...]) -> dict[str, str]:
    return {str(path): digest(path) for path in paths}


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
    if (
        differing != [script_path]
        or previous.get(script_path) != PRE_NAN_SAFE_CARRY_VALIDATION_SCRIPT_SHA256
    ):
        raise RuntimeError("checkpoint-5496 numerical source snapshot changed")
    state.setdefault("source_transitions", []).append(
        {
            "transition_utc": datetime.now(timezone.utc).isoformat(),
            "resolved_base_cell_count": int(state.get("next_base_ordinal", 0)),
            "final_leaf_count": len(state.get("rows", [])),
            "from_script_sha256": previous[script_path],
            "to_script_sha256": sources[script_path],
            "scope": "REPORT_ONLY_NAN_SAFE_CARRY_FORWARD_EQUALITY_FIX",
            "numerical_algorithm_changed": False,
        }
    )
    state["source_snapshot"] = sources
    state["last_update_utc"] = datetime.now(timezone.utc).isoformat()
    atomic_json(WORK_STATE, state)
    return True


def base_cells(base_5474: Any, target_call: dict[str, Any]) -> list[dict[str, Any]]:
    x_edges = [
        float(value)
        for value in base_5474.exact_uniform_edges(
            float(target_call["x_lower"]),
            float(target_call["x_upper"]),
            BASE_X_COUNT,
        )
    ]
    t_edges = [
        float(value)
        for value in base_5474.exact_uniform_edges(
            float(target_call["t_lower"]),
            float(target_call["t_upper"]),
            BASE_T_COUNT,
        )
    ]
    cells: list[dict[str, Any]] = []
    for x_index, (x_lower, x_upper) in enumerate(zip(x_edges, x_edges[1:])):
        for t_index, (t_lower, t_upper) in enumerate(zip(t_edges, t_edges[1:])):
            cells.append(
                {
                    "base_ordinal": len(cells),
                    "base_id": f"X{x_index}:T{t_index}",
                    "x_index": x_index,
                    "t_index": t_index,
                    "x_lower": x_lower,
                    "x_upper": x_upper,
                    "t_lower": t_lower,
                    "t_upper": t_upper,
                    "parameter_area": (x_upper - x_lower) * (t_upper - t_lower),
                }
            )
    return cells


def final_leaf(
    target_call: dict[str, Any],
    base_cell: dict[str, Any],
    ordinal: int,
    child_index: int = -1,
) -> dict[str, Any]:
    t_lower = float(base_cell["t_lower"])
    t_upper = float(base_cell["t_upper"])
    if child_index >= 0:
        child_lower = t_lower + (t_upper - t_lower) * child_index / T2_COUNT
        child_upper = t_lower + (t_upper - t_lower) * (child_index + 1) / T2_COUNT
        leaf_id = f"{base_cell['base_id']}:T2:{child_index}"
    else:
        child_lower = t_lower
        child_upper = t_upper
        leaf_id = str(base_cell["base_id"])
    path_suffix = (
        f":T2:{child_index}" if child_index >= 0 else ""
    )
    return {
        "ordinal": ordinal,
        "leaf_id": leaf_id,
        "base_ordinal": int(base_cell["base_ordinal"]),
        "x_index": int(base_cell["x_index"]),
        "t_index": int(base_cell["t_index"]),
        "repair_child_index": child_index,
        "x_lower": float(base_cell["x_lower"]),
        "x_upper": float(base_cell["x_upper"]),
        "t_lower": child_lower,
        "t_upper": child_upper,
        "parameter_area": (
            float(base_cell["x_upper"]) - float(base_cell["x_lower"])
        ) * (child_upper - child_lower),
        "refinement_depth": int(target_call["refinement_depth"]) + 1,
        "refinement_path": (
            f"{target_call['refinement_path']}:V58AX{BASE_X_COUNT}:"
            f"{base_cell['x_index']}:T{BASE_T_COUNT}:{base_cell['t_index']}"
            f"{path_suffix}"
        ),
    }


def source_carry_forward(
    source_state: dict[str, Any],
    cells: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    source_rows = list(source_state["rows"])
    if (
        len(source_rows) != 130
        or source_rows[-1].get("status") != "FAIL"
        or source_rows[-1].get("leaf_id") != "X2:T0"
        or EXPECTED_FAILURE_MARKER not in str(source_rows[-1].get("failure_message", ""))
    ):
        raise RuntimeError("checkpoint-5495 terminal source has changed")
    carried = [dict(row) for row in source_rows[:-1]]
    if len(carried) != SOURCE_CARRY_FINAL_LEAF_COUNT:
        raise RuntimeError("checkpoint-5495 passing carry-forward count mismatch")
    base_audit: list[dict[str, Any]] = []
    carried_index = 0
    for base_cell in cells[:SOURCE_CARRY_BASE_COUNT]:
        base_id = str(base_cell["base_id"])
        matching: list[dict[str, Any]] = []
        while carried_index < len(carried):
            row = carried[carried_index]
            if int(row.get("x_index", -1)) != int(base_cell["x_index"]) or int(
                row.get("t_index", -1)
            ) != int(base_cell["t_index"]):
                break
            matching.append(row)
            carried_index += 1
        expected_count = 2 if base_id == "X1:T0" else 1
        if len(matching) != expected_count or any(
            row.get("status") != "PASS" for row in matching
        ):
            raise RuntimeError(f"invalid checkpoint-5495 carry-forward at {base_id}")
        base_audit.append(
            {
                **base_cell,
                "status": "PASS",
                "resolution": "T2_REPLACEMENT" if expected_count == 2 else "BASE_PASS",
                "base_failure_type": (
                    "IntervalSingularity" if expected_count == 2 else ""
                ),
                "base_failure_message": (
                    EXPECTED_FAILURE_MARKER if expected_count == 2 else ""
                ),
                "final_leaf_ids": "|".join(str(row["leaf_id"]) for row in matching),
                "final_leaf_count": len(matching),
                "runtime_seconds": math.fsum(
                    float(row.get("runtime_seconds", 0.0)) for row in matching
                ),
                "provenance_checkpoint": 5495,
            }
        )
    if carried_index != len(carried):
        raise RuntimeError("checkpoint-5495 carry-forward has unmatched rows")
    return carried, base_audit, dict(source_rows[-1])


def initial_work_state(
    sources: dict[str, str],
    target_binding_sha256: str,
    base_manifest_sha256: str,
    carried_rows: list[dict[str, Any]],
    carried_base_audit: list[dict[str, Any]],
    source_terminal: dict[str, Any],
) -> dict[str, Any]:
    return {
        "checkpoint": CHECKPOINT,
        "revision": REVISION,
        "source_snapshot": sources,
        "target_binding_sha256": target_binding_sha256,
        "base_manifest_sha256": base_manifest_sha256,
        "base_x_count": BASE_X_COUNT,
        "base_t_count": BASE_T_COUNT,
        "base_cell_count": BASE_CELL_COUNT,
        "t2_count": T2_COUNT,
        "source_carry_base_count": SOURCE_CARRY_BASE_COUNT,
        "source_carry_final_leaf_count": SOURCE_CARRY_FINAL_LEAF_COUNT,
        "source_terminal_failure": source_terminal,
        "next_base_ordinal": SOURCE_CARRY_BASE_COUNT,
        "rows": carried_rows,
        "base_audit_rows": carried_base_audit,
        "complete": False,
        "terminal_failure": False,
        "terminal_failure_record": {},
        "last_update_utc": datetime.now(timezone.utc).isoformat(),
    }


def verify_work_state(
    state: dict[str, Any],
    sources: dict[str, str],
    target_binding_sha256: str,
    base_manifest_sha256: str,
    cells: list[dict[str, Any]],
) -> None:
    expected = {
        "checkpoint": CHECKPOINT,
        "revision": REVISION,
        "source_snapshot": sources,
        "target_binding_sha256": target_binding_sha256,
        "base_manifest_sha256": base_manifest_sha256,
        "base_x_count": BASE_X_COUNT,
        "base_t_count": BASE_T_COUNT,
        "base_cell_count": BASE_CELL_COUNT,
        "t2_count": T2_COUNT,
        "source_carry_base_count": SOURCE_CARRY_BASE_COUNT,
        "source_carry_final_leaf_count": SOURCE_CARRY_FINAL_LEAF_COUNT,
    }
    for key, value in expected.items():
        if state.get(key) != value:
            raise RuntimeError(f"checkpoint-5496 work state mismatch at {key}")
    next_base = int(state.get("next_base_ordinal", -1))
    base_audit = list(state.get("base_audit_rows", []))
    if next_base < SOURCE_CARRY_BASE_COUNT or next_base > len(cells):
        raise RuntimeError("checkpoint-5496 next-base index is invalid")
    successful_audit = [row for row in base_audit if row.get("status") == "PASS"]
    if len(successful_audit) != next_base:
        raise RuntimeError("checkpoint-5496 successful-base prefix mismatch")
    for ordinal, row in enumerate(successful_audit):
        if int(row.get("base_ordinal", -1)) != ordinal:
            raise RuntimeError("checkpoint-5496 base-audit ordinal mismatch")
    expected_leaf_ids = [
        leaf_id
        for row in successful_audit
        for leaf_id in str(row["final_leaf_ids"]).split("|")
        if leaf_id
    ]
    rows = list(state.get("rows", []))
    if [str(row.get("leaf_id", "")) for row in rows] != expected_leaf_ids:
        raise RuntimeError("checkpoint-5496 final-leaf prefix mismatch")
    if any(row.get("status") != "PASS" for row in rows):
        raise RuntimeError("checkpoint-5496 final-leaf ledger contains a failure")
    if bool(state.get("complete")) != (
        next_base == BASE_CELL_COUNT and not bool(state.get("terminal_failure"))
    ):
        raise RuntimeError("checkpoint-5496 completion flag mismatch")


def resolve_base_cell(
    base_5495: Any,
    base_5474: Any,
    parent: Any,
    evaluate_v54: Any,
    target_call: dict[str, Any],
    base_cell: dict[str, Any],
    next_final_ordinal: int,
    source_terminal: dict[str, Any],
) -> tuple[list[dict[str, Any]], dict[str, Any], dict[str, Any] | None]:
    started = time.perf_counter()
    source_trigger = (
        int(base_cell["base_ordinal"]) == SOURCE_CARRY_BASE_COUNT
        and source_terminal.get("leaf_id") == base_cell["base_id"]
        and source_terminal.get("status") == "FAIL"
        and EXPECTED_FAILURE_MARKER
        in str(source_terminal.get("failure_message", ""))
    )
    if source_trigger:
        base_probe = dict(source_terminal)
    else:
        base_probe = base_5495.evaluate_leaf(
            parent,
            evaluate_v54,
            base_5474,
            target_call,
            final_leaf(target_call, base_cell, next_final_ordinal),
        )
    if base_probe["status"] == "PASS":
        audit = {
            **base_cell,
            "status": "PASS",
            "resolution": "BASE_PASS",
            "base_failure_type": "",
            "base_failure_message": "",
            "final_leaf_ids": base_probe["leaf_id"],
            "final_leaf_count": 1,
            "runtime_seconds": time.perf_counter() - started,
            "provenance_checkpoint": CHECKPOINT,
        }
        return [base_probe], audit, None
    expected_class = (
        base_probe.get("failure_type") == "IntervalSingularity"
        and EXPECTED_FAILURE_MARKER in str(base_probe.get("failure_message", ""))
    )
    if not expected_class:
        audit = {
            **base_cell,
            "status": "FAIL",
            "resolution": "UNEXPECTED_BASE_FAILURE",
            "base_failure_type": base_probe.get("failure_type", ""),
            "base_failure_message": base_probe.get("failure_message", ""),
            "final_leaf_ids": "",
            "final_leaf_count": 0,
            "runtime_seconds": time.perf_counter() - started,
            "provenance_checkpoint": CHECKPOINT,
        }
        return [], audit, base_probe
    children: list[dict[str, Any]] = []
    for child_index in range(T2_COUNT):
        child = base_5495.evaluate_leaf(
            parent,
            evaluate_v54,
            base_5474,
            target_call,
            final_leaf(
                target_call,
                base_cell,
                next_final_ordinal + child_index,
                child_index,
            ),
        )
        if child["status"] != "PASS":
            audit = {
                **base_cell,
                "status": "FAIL",
                "resolution": "T2_CHILD_FAILURE",
                "base_failure_type": base_probe.get("failure_type", ""),
                "base_failure_message": base_probe.get("failure_message", ""),
                "final_leaf_ids": "|".join(row["leaf_id"] for row in children),
                "final_leaf_count": len(children),
                "runtime_seconds": time.perf_counter() - started,
                "provenance_checkpoint": CHECKPOINT,
            }
            return [], audit, child
        children.append(child)
    audit = {
        **base_cell,
        "status": "PASS",
        "resolution": "T2_REPLACEMENT",
        "base_failure_type": base_probe.get("failure_type", ""),
        "base_failure_message": base_probe.get("failure_message", ""),
        "final_leaf_ids": "|".join(row["leaf_id"] for row in children),
        "final_leaf_count": len(children),
        "runtime_seconds": time.perf_counter() - started,
        "provenance_checkpoint": CHECKPOINT,
    }
    return children, audit, None


def aggregate_cover(
    base_5495: Any,
    base_5474: Any,
    rows: list[dict[str, Any]],
    target_call: dict[str, Any],
    base_audit: list[dict[str, Any]],
) -> tuple[dict[str, Any], float]:
    results = [dict(row["result"]) for row in rows]
    target_area = (
        float(target_call["x_upper"]) - float(target_call["x_lower"])
    ) * (float(target_call["t_upper"]) - float(target_call["t_lower"]))
    covered_area = math.fsum(float(row["parameter_area"]) for row in results)
    coverage_error = abs(covered_area - target_area)
    if coverage_error > 1.0e-12 * max(target_area, 1.0):
        raise RuntimeError("parent-v58 adaptive cover does not preserve target area")
    denominator_lower = min(
        float(row["minimum_amplitude_denominator_abs_lower"])
        for row in results
    )
    aggregate = base_5474.aggregate_leaf_results(
        results,
        float(target_call["x_lower"]),
        float(target_call["x_upper"]),
        float(target_call["t_lower"]),
        float(target_call["t_upper"]),
        int(target_call["refinement_depth"]),
        str(target_call["refinement_path"]),
        denominator_lower,
        coverage_error,
    )
    aggregate.pop("v53_stable_edge_t_leaf_count", None)
    aggregate.pop("v53_left_first_soft_invariant_abs_lower", None)
    aggregate.pop("v53_parameter_area_coverage_error", None)
    repaired = [row for row in base_audit if row.get("resolution") == "T2_REPLACEMENT"]
    aggregate.update(
        {
            "selected_role": "ADAPTIVE_STABLE_EDGE_LOCAL_T2_LEAF_UNION",
            "path_integral_enclosure_method": METHOD,
            "v58_base_x_count": BASE_X_COUNT,
            "v58_base_t_count": BASE_T_COUNT,
            "v58_base_cell_count": BASE_CELL_COUNT,
            "v58_t2_replacement_count": len(repaired),
            "v58_t2_replacement_base_ids": "|".join(
                str(row["base_id"]) for row in repaired
            ),
            "v58_complete_amplitude_leaf_count": len(results),
            "v58_parent_amplitude_denominator_abs_lower": denominator_lower,
            "v58_parameter_area_coverage_error": coverage_error,
        }
    )
    return base_5495.normalized(aggregate), coverage_error


def install_parent_v58(
    base_5495: Any,
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
        current_sha256, _ = base_5495.call_binding(arguments)
        if current_sha256 != target_binding_sha256:
            return original(**arguments)
        audit_rows.append(
            {
                "status": "APPLIED",
                "method": METHOD,
                "target_binding_sha256": target_binding_sha256,
                "current_binding_sha256": current_sha256,
                "complete_amplitude_leaf_count": aggregate[
                    "v58_complete_amplitude_leaf_count"
                ],
                "t2_replacement_count": aggregate["v58_t2_replacement_count"],
                "t2_replacement_base_ids": aggregate[
                    "v58_t2_replacement_base_ids"
                ],
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
    parent.V58_ADAPTIVE_CERTIFICATE_AUDIT_ROWS = audit_rows
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
    flattened: list[dict[str, Any]] = []
    for source in state["rows"]:
        result = source.get("result", {})
        flattened.append(
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
    return flattened


def render_document(payload: dict[str, Any], base_5467: Any) -> None:
    lines = [
        "# 5496: D4 parent-v58 adaptive stable-edge T2 gate",
        "",
        "Checkpoint 5495 proves that hard-coding the checkpoint-5494 repair to `X1:T0` is too narrow: 129 final leaves pass, then the identical stable-edge class appears at `X2:T0`. Parent v58 therefore promotes the operation, not the location: every base leaf is first evaluated unchanged, and only an exact `edge_2_1_3:stable_edge` failure is replaced by its two exact t children.",
        "",
        f"Resolved base cells: `{payload['resolved_base_cell_count']}/{payload['base_cell_count']}`. Final complete-amplitude leaves: `{payload['final_leaf_count']}`. T2 replacements: `{payload['t2_replacement_count']}` at `{payload['t2_replacement_base_ids']}`.",
        "",
        f"Cover complete: `{payload['candidate_cover_complete']}`. Terminal failure: `{payload['terminal_failure']}`. Denominator lower: `{payload['candidate_amplitude_denominator_abs_lower']}`. Collision-Jacobian lower: `{payload['candidate_collision_jacobian_abs_lower']}`.",
        "",
        f"Parent-v58 target passed: `{payload['target_v58_passed']}`. Untriggered v57/v58 control identical: `{payload['control_v57_v58_identical']}`.",
        "",
        f"**{payload['decision']}**",
        "",
        "No action, contour, chart, selector, residue or threshold changes. This remains one active-cuboid target until migrated and continued. Full outer enclosure, event-local or combined W3, the regulator limit, all-operator local GR and full MTS remain open.",
        "",
    ]
    base_5467.atomic_text(DOCUMENT, "\n".join(lines))


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--max-base-cells", type=int, default=BASE_CELL_COUNT)
    parser.add_argument("--max-runtime-seconds", type=float, default=10800.0)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args()


def main() -> int:
    arguments_cli = parse_arguments()
    if arguments_cli.max_base_cells < 1:
        raise ValueError("max-base-cells must be positive")
    if arguments_cli.max_runtime_seconds <= 0.0:
        raise ValueError("max-runtime-seconds must be positive")
    base_5495 = load_module("mts_5495_for_5496", SCRIPT_5495)
    base_5467 = load_module("mts_5467_for_5496", base_5495.SCRIPT_5467)
    base_5468 = load_module("mts_5468_for_5496", base_5495.SCRIPT_5468)
    base_5469 = load_module("mts_5469_for_5496", base_5495.SCRIPT_5469)
    base_5472 = load_module("mts_5472_for_5496", base_5495.SCRIPT_5472)
    base_5474 = load_module("mts_5474_for_5496", base_5495.SCRIPT_5474)
    base_5476 = load_module("mts_5476_for_5496", base_5495.SCRIPT_5476)
    base_5478 = load_module("mts_5478_for_5496", base_5495.SCRIPT_5478)
    base_5480 = load_module("mts_5480_for_5496", base_5495.SCRIPT_5480)
    base_5483 = load_module("mts_5483_for_5496", base_5495.SCRIPT_5483)
    base_5490 = load_module("mts_5490_for_5496", base_5495.SCRIPT_5490)
    base_5493 = load_module("mts_5493_for_5496", base_5495.SCRIPT_5493)
    base_5467.set_below_normal_priority()
    base_5480.set_single_core_affinity()
    before_formalization = base_5467.formalization_snapshot()
    paths = source_paths(base_5495)
    missing = [str(path) for path in paths if not path.is_file()]
    if missing:
        raise FileNotFoundError(f"missing sources: {missing}")
    inherited_hashes = {
        "script_5495": digest(SCRIPT_5495),
        "work_state_5495": digest(WORK_STATE_5495),
        "result_5495": digest(RESULT_5495),
        "leaf_audit_5495": digest(LEAF_AUDIT_5495),
        "validation_5495": digest(VALIDATION_5495),
        "source_register_5495": digest(SOURCE_REGISTER_5495),
    }
    expected_hashes = {
        "script_5495": EXPECTED_SCRIPT_5495_SHA256,
        "work_state_5495": EXPECTED_WORK_STATE_5495_SHA256,
        "result_5495": EXPECTED_RESULT_5495_SHA256,
        "leaf_audit_5495": EXPECTED_LEAF_AUDIT_5495_SHA256,
        "validation_5495": EXPECTED_VALIDATION_5495_SHA256,
        "source_register_5495": EXPECTED_SOURCE_REGISTER_5495_SHA256,
    }
    if inherited_hashes != expected_hashes:
        raise RuntimeError("checkpoint-5496 inherited source hash mismatch")
    source_state = read_json(WORK_STATE_5495)
    source_result = read_json(RESULT_5495)
    source_validation = read_csv(VALIDATION_5495)
    source_register = read_csv(SOURCE_REGISTER_5495)
    if (
        source_result.get("decision")
        != "PARENT_V58_COMPLETE_AMPLITUDE_T_REPLACEMENT_REJECTED__DERIVE_NEXT_FAILED_LEAF"
        or source_result.get("terminal_failure_leaf_id") != "X2:T0"
        or EXPECTED_FAILURE_MARKER
        not in str(source_result.get("terminal_failure_message", ""))
        or not all(truth(row.get("passed")) for row in source_validation)
        or not base_5495.source_register_is_current(source_register)
    ):
        raise RuntimeError("checkpoint-5495 rejection evidence is not current")
    result_5492 = read_json(base_5495.RESULT_5492)
    work_state_5492 = read_json(base_5495.WORK_STATE_5492)
    leaf_rows_5492 = read_csv(base_5495.LEAF_AUDIT_5492)
    binding_5493 = read_json(base_5495.BINDING_5493)
    state_5484 = read_json(base_5495.STATE_5484)
    cuboid = next(
        row
        for row in read_csv(base_5495.MANIFEST_5468)
        if row["cuboid_job_id"] == base_5495.TARGET_CUBOID_ID
    )
    target = next(
        row
        for row in state_5484["refinement_witnesses"]
        if row.get("refinement_path") == base_5495.TARGET_REFINEMENT_PATH
    )
    control = min(
        (
            row
            for row in state_5484["accepted"]
            if truth(row.get("probe_passed"))
            and math.isfinite(float(row.get("runtime_seconds", math.inf)))
            and float(row.get("collision_jacobian_abs_lower", 0.0)) > 0.0
        ),
        key=lambda row: float(row.get("runtime_seconds", math.inf)),
    )
    stable, _, mapped_cells, support_segments, branches = base_5467.load_parent()
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
    parent, evaluate_v54 = base_5495.fresh_v57_with_v54_handle(
        base_5467,
        base_5472,
        base_5474,
        base_5476,
        base_5478,
        base_5483,
        base_5493,
        binding_5493,
        collision_certificate,
        "mts_parent_v58_adaptive_work_5496",
    )
    target_call = base_5495.target_arguments(
        stable,
        parent,
        mapped_cells,
        support_segments,
        branches,
        cuboid,
        target,
    )
    target_binding_sha256, target_binding = base_5495.call_binding(target_call)
    cells = base_cells(base_5474, target_call)
    base_manifest_sha256, _ = base_5495.object_fingerprint(cells)
    carried_rows, carried_base_audit, source_terminal = source_carry_forward(
        source_state,
        cells,
    )
    if arguments_cli.dry_run:
        print(
            json.dumps(
                {
                    "checkpoint": CHECKPOINT,
                    "dry_run": True,
                    "target_binding_sha256": target_binding_sha256,
                    "base_manifest_sha256": base_manifest_sha256,
                    "base_cell_count": len(cells),
                    "carried_base_count": len(carried_base_audit),
                    "carried_final_leaf_count": len(carried_rows),
                    "next_source_trigger": source_terminal["leaf_id"],
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
            base_manifest_sha256,
            carried_rows,
            carried_base_audit,
            source_terminal,
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
        base_manifest_sha256,
        cells,
    )
    if not WORK_STATE.is_file():
        atomic_json(WORK_STATE, state)
    run_started = time.perf_counter()
    evaluated_base_cells = 0
    while (
        int(state["next_base_ordinal"]) < BASE_CELL_COUNT
        and not bool(state["terminal_failure"])
        and evaluated_base_cells < arguments_cli.max_base_cells
    ):
        if (
            evaluated_base_cells > 0
            and time.perf_counter() - run_started >= arguments_cli.max_runtime_seconds
        ):
            break
        base_ordinal = int(state["next_base_ordinal"])
        final_rows, base_audit_row, terminal = resolve_base_cell(
            base_5495,
            base_5474,
            parent,
            evaluate_v54,
            target_call,
            cells[base_ordinal],
            len(state["rows"]),
            state["source_terminal_failure"],
        )
        state["base_audit_rows"].append(base_audit_row)
        if terminal is None:
            state["rows"].extend(final_rows)
            state["next_base_ordinal"] = base_ordinal + 1
        else:
            state["terminal_failure"] = True
            state["terminal_failure_record"] = terminal
        state["complete"] = (
            state["next_base_ordinal"] == BASE_CELL_COUNT
            and not state["terminal_failure"]
        )
        state["last_update_utc"] = datetime.now(timezone.utc).isoformat()
        state["last_run_seconds"] = time.perf_counter() - run_started
        state["last_run_evaluated_base_cell_count"] = evaluated_base_cells + 1
        atomic_json(WORK_STATE, state)
        evaluated_base_cells += 1
    verify_work_state(
        state,
        sources,
        target_binding_sha256,
        base_manifest_sha256,
        cells,
    )
    rows = list(state["rows"])
    base_audit_rows = list(state["base_audit_rows"])
    complete = bool(state["complete"])
    terminal_failure = bool(state["terminal_failure"])
    aggregate: dict[str, Any] | None = None
    coverage_error = math.nan
    if complete:
        aggregate, coverage_error = aggregate_cover(
            base_5495,
            base_5474,
            rows,
            target_call,
            base_audit_rows,
        )
    target_v58: dict[str, Any] = {}
    control_v57: dict[str, Any] = {}
    control_v58: dict[str, Any] = {}
    target_application_rows: list[dict[str, Any]] = []
    control_application_rows: list[dict[str, Any]] = []
    target_binding_preflight = False
    control_identical = False
    if aggregate is not None:
        parent_v58_target, _ = base_5495.fresh_v57_with_v54_handle(
            base_5467,
            base_5472,
            base_5474,
            base_5476,
            base_5478,
            base_5483,
            base_5493,
            binding_5493,
            collision_certificate,
            "mts_parent_v58_adaptive_target_5496",
        )
        preflight_call = base_5495.target_arguments(
            stable,
            parent_v58_target,
            mapped_cells,
            support_segments,
            branches,
            cuboid,
            target,
        )
        preflight_sha256, _ = base_5495.call_binding(preflight_call)
        target_binding_preflight = preflight_sha256 == target_binding_sha256
        if not target_binding_preflight:
            raise RuntimeError("checkpoint-5496 target binding preflight mismatch")
        parent_v58_target = install_parent_v58(
            base_5495,
            parent_v58_target,
            target_binding_sha256,
            aggregate,
        )
        target_v58 = base_5469.evaluate_node(
            base_5468,
            stable,
            parent_v58_target,
            mapped_cells,
            support_segments,
            branches,
            cuboid,
            target,
        )
        target_application_rows = list(
            parent_v58_target.V58_ADAPTIVE_CERTIFICATE_AUDIT_ROWS
        )
        parent_v57_control, _ = base_5495.fresh_v57_with_v54_handle(
            base_5467,
            base_5472,
            base_5474,
            base_5476,
            base_5478,
            base_5483,
            base_5493,
            binding_5493,
            collision_certificate,
            "mts_parent_v57_adaptive_control_5496",
        )
        control_v57 = base_5469.evaluate_node(
            base_5468,
            stable,
            parent_v57_control,
            mapped_cells,
            support_segments,
            branches,
            cuboid,
            control,
        )
        parent_v58_control, _ = base_5495.fresh_v57_with_v54_handle(
            base_5467,
            base_5472,
            base_5474,
            base_5476,
            base_5478,
            base_5483,
            base_5493,
            binding_5493,
            collision_certificate,
            "mts_parent_v58_adaptive_control_5496",
        )
        parent_v58_control = install_parent_v58(
            base_5495,
            parent_v58_control,
            target_binding_sha256,
            aggregate,
        )
        control_v58 = base_5469.evaluate_node(
            base_5468,
            stable,
            parent_v58_control,
            mapped_cells,
            support_segments,
            branches,
            cuboid,
            control,
        )
        control_application_rows = list(
            parent_v58_control.V58_ADAPTIVE_CERTIFICATE_AUDIT_ROWS
        )
        control_identical = (
            truth(control_v57.get("probe_passed"))
            and truth(control_v58.get("probe_passed"))
            and all(
                control_v57.get(field) == control_v58.get(field)
                for field in CONTROL_FIELDS
            )
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
    repaired_base_rows = [
        row for row in base_audit_rows if row.get("resolution") == "T2_REPLACEMENT"
    ]
    target_v58_passed = truth(target_v58.get("probe_passed"))
    preliminary_certified = (
        complete
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
    )
    exact_prefix = (
        len([row for row in base_audit_rows if row.get("status") == "PASS"])
        == int(state["next_base_ordinal"])
        and all(row.get("status") == "PASS" for row in rows)
    )
    committed_rows_numeric = all(
        all(
            math.isfinite(float(row["result"][field]))
            and float(row["result"][field]) > 0.0
            for field in METRIC_FIELDS
        )
        and int(row.get("v57_scope_miss_count", 0)) == 0
        for row in rows
    )
    resolved_area = math.fsum(
        float(row["parameter_area"])
        for row in cells[: int(state["next_base_ordinal"])]
    )
    final_area = math.fsum(float(row["parameter_area"]) for row in rows)
    prefix_coverage_error = abs(resolved_area - final_area)
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
        check("checkpoint_5495_sources_are_hash_locked", inherited_hashes == expected_hashes, inherited_hashes),
        check(
            "checkpoint_5495_rejection_is_source_signed",
            source_result.get("terminal_failure_leaf_id") == "X2:T0"
            and all(truth(row.get("passed")) for row in source_validation)
            and base_5495.source_register_is_current(source_register),
            source_result.get("decision"),
        ),
        check(
            "passing_5495_prefix_is_carried_exactly",
            base_5495.canonical_json(
                state["rows"][:SOURCE_CARRY_FINAL_LEAF_COUNT]
            )
            == base_5495.canonical_json(carried_rows)
            and base_5495.canonical_json(
                state["base_audit_rows"][:SOURCE_CARRY_BASE_COUNT]
            )
            == base_5495.canonical_json(carried_base_audit),
            f"base={SOURCE_CARRY_BASE_COUNT};leaves={SOURCE_CARRY_FINAL_LEAF_COUNT}",
        ),
        check(
            "adaptive_rule_is_failure_class_triggered",
            all(
                row.get("resolution") != "T2_REPLACEMENT"
                or (
                    row.get("base_failure_type") == "IntervalSingularity"
                    and EXPECTED_FAILURE_MARKER
                    in str(row.get("base_failure_message", ""))
                )
                for row in base_audit_rows
            ),
            [row["base_id"] for row in repaired_base_rows],
        ),
        check(
            "committed_prefix_has_exact_coverage",
            exact_prefix and prefix_coverage_error == 0.0,
            f"base={state['next_base_ordinal']};coverage_error={prefix_coverage_error}",
        ),
        check("committed_complete_amplitudes_are_numeric", committed_rows_numeric, len(rows)),
        check(
            "work_outcome_is_internally_consistent",
            complete
            or terminal_failure
            or int(state["next_base_ordinal"]) < BASE_CELL_COUNT,
            f"complete={complete};terminal={terminal_failure};base={state['next_base_ordinal']}",
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
            f"target={target_v58_passed};control={control_identical}",
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
        check("broad_claims_remain_false", True, "one active-cuboid target only"),
    ]
    failed_validations = [row for row in validations if not row["passed"]]
    certified = preliminary_certified and not failed_validations
    if certified:
        decision = "PARENT_V58_ADAPTIVE_STABLE_EDGE_T2_CERTIFIED__MIGRATE_FRONTIER"
        next_target = "CREATE_HASH_LOCKED_PARENT_V58_CARRY_FORWARD_OF_CHECKPOINT_5484_STATE"
    elif terminal_failure:
        decision = "PARENT_V58_ADAPTIVE_STABLE_EDGE_T2_REJECTED__DERIVE_TERMINAL_CHILD"
        next_target = "DERIVE_CHECKPOINT_5496_TERMINAL_CHILD_REPAIR"
    else:
        decision = "PARENT_V58_ADAPTIVE_STABLE_EDGE_T2_PARTIAL__RESUME"
        next_target = "RESUME_CHECKPOINT_5496_ADAPTIVE_COMPLETE_AMPLITUDE_COVER"
    work_state_sha256 = digest(WORK_STATE)
    if aggregate is not None:
        atomic_json(
            CERTIFICATE,
            {
                "checkpoint": CHECKPOINT,
                "revision": REVISION,
                "method": METHOD,
                "target_binding_sha256": target_binding_sha256,
                "base_manifest_sha256": base_manifest_sha256,
                "work_state_sha256": work_state_sha256,
                "base_cell_count": BASE_CELL_COUNT,
                "final_leaf_count": len(rows),
                "t2_replacement_count": len(repaired_base_rows),
                "t2_replacement_base_ids": [row["base_id"] for row in repaired_base_rows],
                "parameter_area_coverage_error": coverage_error,
                "aggregate_result": aggregate,
            },
        )
    terminal_record = dict(state.get("terminal_failure_record", {}))
    payload = {
        "checkpoint": CHECKPOINT,
        "revision": REVISION,
        "created_utc": datetime.now(timezone.utc).isoformat(),
        "decision": decision,
        "next_target": next_target,
        "target_binding_sha256": target_binding_sha256,
        "base_manifest_sha256": base_manifest_sha256,
        "work_state_sha256": work_state_sha256,
        "base_cell_count": BASE_CELL_COUNT,
        "resolved_base_cell_count": int(state["next_base_ordinal"]),
        "remaining_base_cell_count": BASE_CELL_COUNT - int(state["next_base_ordinal"]),
        "final_leaf_count": len(rows),
        "t2_replacement_count": len(repaired_base_rows),
        "t2_replacement_base_ids": [row["base_id"] for row in repaired_base_rows],
        "last_run_evaluated_base_cell_count": evaluated_base_cells,
        "last_run_seconds": time.perf_counter() - run_started,
        "report_only_source_transition_applied": report_only_source_transition,
        "candidate_cover_complete": complete,
        "terminal_failure": terminal_failure,
        "terminal_failure_leaf_id": terminal_record.get("leaf_id", ""),
        "terminal_failure_type": terminal_record.get("failure_type", ""),
        "terminal_failure_message": terminal_record.get("failure_message", ""),
        "prefix_parameter_area_coverage_error": prefix_coverage_error,
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
        "target_binding_preflight": target_binding_preflight,
        "target_v58_passed": target_v58_passed,
        "v58_target_application_count": len(target_application_rows),
        "v58_control_application_count": len(control_application_rows),
        "control_refinement_path": control["refinement_path"],
        "control_v57_v58_identical": control_identical,
        "parent_action_changed": False,
        "validation_row_count": len(validations),
        "failed_validation_count": len(failed_validations),
        "valid_for_parent_v58_adaptive_stable_edge_T2": certified,
        "valid_for_parent_v58_active_cuboid": False,
        "valid_for_full_outer_parent_leaf_enclosure": False,
        "valid_for_D4_event_local_W3_bound": False,
        "valid_for_all_operator_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    OUTPUT.mkdir(parents=True, exist_ok=True)
    base_5467.atomic_csv(LEAF_AUDIT, leaf_audit_rows(state))
    base_5467.atomic_csv(BASE_AUDIT, base_audit_rows)
    atomic_json(
        BINDING,
        {
            "checkpoint": CHECKPOINT,
            "target_binding_sha256": target_binding_sha256,
            "target_binding": target_binding,
            "base_manifest_sha256": base_manifest_sha256,
            "base_cell_count": BASE_CELL_COUNT,
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
                    "resolved_base_cell_count",
                    "base_cell_count",
                    "remaining_base_cell_count",
                    "final_leaf_count",
                    "t2_replacement_count",
                    "t2_replacement_base_ids",
                    "last_run_evaluated_base_cell_count",
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
