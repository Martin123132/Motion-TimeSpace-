from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import math
import os
import time
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SCRIPTS = POST / "scripts"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
RESIDUALS = POST / "source-intake" / "mts_residuals"
SOURCE = FUNCTIONAL_RG / "5306"
NODE_RUNS = SOURCE / "nodes"

SCRIPT_5305 = SCRIPTS / "Y5_R2FR_5305_topology_safe_regulator_ladder_preflight.py"
RESULT_5305 = FUNCTIONAL_RG / "5305" / "topology_safe_regulator_ladder_preflight_result.json"
VALIDATION_5305 = FUNCTIONAL_RG / "5305" / "topology_safe_regulator_ladder_preflight_validation.csv"

DRY_RUN = SOURCE / "selected_energy_regulator_ladders_dry_run.json"
SHARD_MANIFEST = SOURCE / "selected_energy_regulator_shard_manifest.csv"
INTEGRALS = SOURCE / "selected_energy_finite_regulator_integrals.csv"
LIMITS = SOURCE / "selected_energy_regulator_zero_limits.csv"
RESULT = SOURCE / "selected_energy_regulator_ladders_result.json"
VALIDATION = SOURCE / "selected_energy_regulator_ladders_validation.csv"
RESIDUAL_VALIDATION = RESIDUALS / "P8_Y5_BRR545_5306_VALIDATION.csv"
STATUS = SOURCE / "status.json"
DOCUMENT = POST / "5306-Y5-R2FR-selected-energy-five-regulator-ladders.md"

CHECKPOINT = 5306
PARENT_CHECKPOINT = 5305
MARKER = "MTS_5306_SELECTED_ENERGY_FIVE_REGULATOR_LADDERS"
REVISION = "selected-energy-five-regulator-ladders-v1"
SHARD_REVISION = "selected-energy-regulator-shard-v1"
QUADRATURE_ORDERS = (4, 8)
MAXIMUM_RUNTIME_SECONDS = 3.25 * 60.0 * 60.0
CLAIM_FIELDS = (
    "valid_for_full_angular_convergence",
    "valid_for_full_phase_space_coefficient",
    "valid_for_numeric_UV_claim",
    "valid_for_local_GR_claim",
    "valid_for_full_MTS_claim",
)


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5305 = load_module("mts_5305_for_5306", SCRIPT_5305)
M5304 = M5305.M5304
M5303 = M5305.M5303
M5301 = M5305.M5301
M5280 = M5305.M5280
M5283 = M5305.M5283
np = M5305.np
mp = M5305.mp


def set_below_normal_priority() -> None:
    if os.name != "nt":
        return
    import ctypes

    process = ctypes.windll.kernel32.GetCurrentProcess()
    ctypes.windll.kernel32.SetPriorityClass(process, 0x00004000)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        raise ValueError(f"no rows for {path}")
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    os.replace(temporary, path)


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary, path)


def digest(path: Path) -> str:
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            hasher.update(block)
    return hasher.hexdigest()


def parse_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() == "true"


def complex_fields(prefix: str, value: complex) -> dict[str, float]:
    return {
        f"{prefix}_real": float(value.real),
        f"{prefix}_imaginary": float(value.imag),
        f"{prefix}_magnitude": float(abs(value)),
    }


def relative_complex_change(first: complex, second: complex) -> float:
    return abs(second - first) / max(abs(second), abs(first), 1.0e-300)


def node_rows() -> list[dict[str, str]]:
    return read_csv(M5305.NODES)


def panel_lookup() -> dict[str, list[dict[str, str]]]:
    result: dict[str, list[dict[str, str]]] = {}
    for row in read_csv(M5305.PANELS):
        result.setdefault(row["energy_node_id"], []).append(row)
    for rows in result.values():
        rows.sort(key=lambda row: int(row["panel_index"]))
    return result


def shard_paths(
    energy_node_id: str,
    epsilon_id: str,
    order: int,
) -> dict[str, Path]:
    root = NODE_RUNS / energy_node_id / epsilon_id / f"Q{order:02d}"
    return {
        "root": root,
        "panels": root / "panel_integrals.csv",
        "result": root / "result.json",
    }


def shard_is_valid(
    energy_node_id: str,
    epsilon_id: str,
    order: int,
    expected_panel_count: int,
    panel_plan_sha256: str,
) -> bool:
    paths = shard_paths(energy_node_id, epsilon_id, order)
    if not paths["result"].exists() or not paths["panels"].exists():
        return False
    try:
        result = read_json(paths["result"])
        rows = read_csv(paths["panels"])
    except Exception:
        return False
    return (
        result.get("shard_revision") == SHARD_REVISION
        and result.get("energy_node_id") == energy_node_id
        and result.get("epsilon_id") == epsilon_id
        and int(result.get("quadrature_order", -1)) == order
        and int(result.get("panel_count", -1)) == expected_panel_count
        and result.get("panel_plan_sha256") == panel_plan_sha256
        and bool(result.get("all_quadrature_nodes_mask_active"))
        and len(rows) == expected_panel_count
    )


def integrate_shard(
    node: dict[str, str],
    panels: list[dict[str, str]],
    epsilon_id: str,
    epsilon: float,
    order: int,
    evaluate: Any,
    multiplier: float,
    panel_plan_sha256: str,
) -> dict[str, Any]:
    energy_node_id = node["energy_node_id"]
    paths = shard_paths(energy_node_id, epsilon_id, order)
    paths["root"].mkdir(parents=True, exist_ok=True)
    started = time.perf_counter()
    quadrature_nodes, quadrature_weights = np.polynomial.legendre.leggauss(order)
    energy = float(node["soft_energy"])
    total = 0.0j
    rows: list[dict[str, Any]] = []
    inactive_count = 0
    for panel_counter, panel in enumerate(panels, start=1):
        left = float(panel["left_absolute_soft_cosine"])
        right = float(panel["right_absolute_soft_cosine"])
        half_width = 0.5 * (right - left)
        midpoint = 0.5 * (right + left)
        panel_value = 0.0j
        for quadrature_node, quadrature_weight in zip(
            quadrature_nodes, quadrature_weights
        ):
            coordinate = midpoint + half_width * float(quadrature_node)
            value, active = M5305.edge_component(
                evaluate, epsilon_id, energy, coordinate
            )
            inactive_count += int(not active)
            panel_value += (
                half_width
                * float(quadrature_weight)
                * multiplier
                * value
            )
        total += panel_value
        rows.append(
            {
                "energy_node_id": energy_node_id,
                "soft_energy": energy,
                "epsilon_id": epsilon_id,
                "epsilon": epsilon,
                "quadrature_order": order,
                "panel_index": int(panel["panel_index"]),
                "left_absolute_soft_cosine": left,
                "right_absolute_soft_cosine": right,
                "panel_width": right - left,
                "intersects_peak_core": panel["intersects_peak_core"],
                **complex_fields("panel_integral", panel_value),
                **{field: False for field in CLAIM_FIELDS},
            }
        )
        if panel_counter % 25 == 0 or panel_counter == len(panels):
            atomic_json(
                STATUS,
                {
                    "checkpoint": CHECKPOINT,
                    "state": "RUNNING",
                    "stage": "SELECTED_ENERGY_REGULATOR_SHARD",
                    "energy_node_id": energy_node_id,
                    "epsilon_id": epsilon_id,
                    "quadrature_order": order,
                    "completed_panel_count": panel_counter,
                    "planned_panel_count": len(panels),
                },
            )
    write_csv(paths["panels"], rows)
    result = {
        "checkpoint": CHECKPOINT,
        "shard_revision": SHARD_REVISION,
        "energy_node_id": energy_node_id,
        "soft_energy": energy,
        "epsilon_id": epsilon_id,
        "epsilon": epsilon,
        "quadrature_order": order,
        "panel_count": len(panels),
        "quadrature_node_evaluation_count": len(panels) * order,
        "inactive_quadrature_node_count": inactive_count,
        "all_quadrature_nodes_mask_active": inactive_count == 0,
        **complex_fields("edge_integral", total),
        "panel_plan_sha256": panel_plan_sha256,
        "runtime_seconds": time.perf_counter() - started,
        **{field: False for field in CLAIM_FIELDS},
    }
    atomic_json(paths["result"], result)
    return result


def planned_shards(
    nodes: list[dict[str, str]],
) -> list[tuple[dict[str, str], str, float, int]]:
    return [
        (node, epsilon_id, epsilon, order)
        for node in nodes
        for epsilon_id, epsilon in M5303.REGULATORS
        for order in QUADRATURE_ORDERS
    ]


def completed_manifest(
    nodes: list[dict[str, str]],
    panels: dict[str, list[dict[str, str]]],
    panel_plan_sha256: str,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for node, epsilon_id, epsilon, order in planned_shards(nodes):
        energy_node_id = node["energy_node_id"]
        paths = shard_paths(energy_node_id, epsilon_id, order)
        complete = shard_is_valid(
            energy_node_id,
            epsilon_id,
            order,
            len(panels[energy_node_id]),
            panel_plan_sha256,
        )
        result = read_json(paths["result"]) if complete else {}
        rows.append(
            {
                "energy_node_id": energy_node_id,
                "soft_energy": node["soft_energy"],
                "epsilon_id": epsilon_id,
                "epsilon": epsilon,
                "quadrature_order": order,
                "panel_count": len(panels[energy_node_id]),
                "shard_complete": complete,
                "shard_result_path": str(paths["result"]),
                "shard_panel_rows_path": str(paths["panels"]),
                "runtime_seconds": result.get("runtime_seconds", ""),
                "all_quadrature_nodes_mask_active": result.get(
                    "all_quadrature_nodes_mask_active", False
                ),
                **{field: False for field in CLAIM_FIELDS},
            }
        )
    return rows


def integral_rows(manifest: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    results: dict[tuple[str, str, int], dict[str, Any]] = {}
    for row in manifest:
        if not parse_bool(row["shard_complete"]):
            continue
        result = read_json(Path(row["shard_result_path"]))
        results[(row["energy_node_id"], row["epsilon_id"], int(row["quadrature_order"]))] = result
    node_ids = sorted({key[0] for key in results})
    for energy_node_id in node_ids:
        for epsilon_id, epsilon in M5303.REGULATORS:
            lower = results[(energy_node_id, epsilon_id, min(QUADRATURE_ORDERS))]
            upper = results[(energy_node_id, epsilon_id, max(QUADRATURE_ORDERS))]
            lower_value = complex(
                float(lower["edge_integral_real"]),
                float(lower["edge_integral_imaginary"]),
            )
            upper_value = complex(
                float(upper["edge_integral_real"]),
                float(upper["edge_integral_imaginary"]),
            )
            change = relative_complex_change(lower_value, upper_value)
            for order, result in (
                (min(QUADRATURE_ORDERS), lower),
                (max(QUADRATURE_ORDERS), upper),
            ):
                value = lower_value if order == min(QUADRATURE_ORDERS) else upper_value
                rows.append(
                    {
                        "energy_node_id": energy_node_id,
                        "soft_energy": result["soft_energy"],
                        "epsilon_id": epsilon_id,
                        "epsilon": epsilon,
                        "quadrature_order": order,
                        **complex_fields("edge_integral", value),
                        "order4_order8_relative_change": change,
                        "passes_edge_quadrature_gate": (
                            change <= M5303.QUADRATURE_CHANGE_LIMIT
                        ),
                        **{field: False for field in CLAIM_FIELDS},
                    }
                )
    return rows


def limit_products(
    integrals: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    rows: list[dict[str, Any]] = []
    summaries: list[dict[str, Any]] = []
    for energy_node_id in sorted({row["energy_node_id"] for row in integrals}):
        local = [row for row in integrals if row["energy_node_id"] == energy_node_id]
        limit_rows, estimates = M5303.limit_rows(local)
        for row in limit_rows:
            rows.append({"energy_node_id": energy_node_id, **row})
        richardson_change = float(
            limit_rows[0]["last_two_richardson_relative_change"]
        )
        model_change = float(
            limit_rows[0]["small_regulator_model_intercept_relative_change"]
        )
        final = estimates["RICHARDSON_E005_E0025"]
        summaries.append(
            {
                "energy_node_id": energy_node_id,
                "soft_energy": local[0]["soft_energy"],
                **complex_fields("regulator_zero_estimate", final),
                "last_two_richardson_relative_change": richardson_change,
                "small_regulator_model_intercept_relative_change": model_change,
                "regulator_zero_limit_stable": (
                    richardson_change <= M5303.RICHARDSON_LIMIT_CHANGE_LIMIT
                    and model_change <= M5303.MODEL_INTERCEPT_CHANGE_LIMIT
                ),
                **{field: False for field in CLAIM_FIELDS},
            }
        )
    return rows, summaries


def source_rows() -> list[dict[str, str]]:
    paths = (
        Path(__file__).resolve(),
        SCRIPT_5305,
        RESULT_5305,
        VALIDATION_5305,
        M5305.NODES,
        M5305.PANELS,
    )
    return [{"path": str(path), "sha256": digest(path)} for path in paths]


def dry_run() -> dict[str, Any]:
    SOURCE.mkdir(parents=True, exist_ok=True)
    parent = read_json(RESULT_5305)
    nodes = node_rows()
    panels = panel_lookup()
    estimated_evaluations = sum(
        len(panels[node["energy_node_id"]])
        * sum(QUADRATURE_ORDERS)
        * len(M5303.REGULATORS)
        for node in nodes
    )
    checks = {
        "parent_5305_accepted": bool(parent["acceptance_passed"]),
        "parent_5305_validated": all(
            parse_bool(row["passed"]) for row in read_csv(VALIDATION_5305)
        ),
        "parent_requests_five_regulator_ladders": (
            parent["decision"]
            == (
                "TOPOLOGY_SAFE_NODES_SYMMETRY_AND_PEAK_PANELS_RESOLVED__"
                "RUN_FIVE_REGULATOR_LADDERS"
            )
        ),
        "four_nodes_and_all_panel_plans_loaded": (
            len(nodes) == 4
            and set(panels) == {node["energy_node_id"] for node in nodes}
            and all(panels.values())
        ),
        "forty_resumable_shards_planned": (
            len(planned_shards(nodes))
            == len(nodes) * len(M5303.REGULATORS) * len(QUADRATURE_ORDERS)
            == 40
        ),
        "single_process_budget_explicit": MAXIMUM_RUNTIME_SECONDS < 4.0 * 3600.0,
        "formalization_workbench_unchanged": (
            M5283.formal_inventory_digest()
            == str(parent["formalization_workbench_end_digest"])
        ),
    }
    accepted = all(checks.values())
    result = {
        "checkpoint": CHECKPOINT,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "mode": "dry-run",
        "checks": checks,
        "acceptance_passed": accepted,
        "planned_shard_count": len(planned_shards(nodes)),
        "estimated_component_evaluation_count": estimated_evaluations,
        "maximum_runtime_seconds": MAXIMUM_RUNTIME_SECONDS,
        "decision": (
            "DRY_RUN_ACCEPTED__RUN_RESUMABLE_SELECTED_ENERGY_LADDERS"
            if accepted
            else "DRY_RUN_REQUIRES_REPAIR"
        ),
        "runtime_seconds": 0.0,
        **{field: False for field in CLAIM_FIELDS},
    }
    atomic_json(DRY_RUN, result)
    return result


def execute() -> dict[str, Any]:
    set_below_normal_priority()
    mp.mp.dps = M5280.MP_DECIMAL_DIGITS
    M5301.configure_reused_pipeline()
    started = time.perf_counter()
    dry = dry_run()
    if not dry["acceptance_passed"]:
        raise RuntimeError("5306 dry run did not pass")
    parent = read_json(RESULT_5305)
    nodes = node_rows()
    panels = panel_lookup()
    panel_plan_sha256 = digest(M5305.PANELS)
    context = M5303.synthetic_context()
    evaluate = M5305.component_evaluator(context)
    multiplier = M5301.M5300.M5292.physical_multiplier()
    runtime_limit_reached = False
    for node, epsilon_id, epsilon, order in planned_shards(nodes):
        energy_node_id = node["energy_node_id"]
        if shard_is_valid(
            energy_node_id,
            epsilon_id,
            order,
            len(panels[energy_node_id]),
            panel_plan_sha256,
        ):
            continue
        integrate_shard(
            node,
            panels[energy_node_id],
            epsilon_id,
            epsilon,
            order,
            evaluate,
            multiplier,
            panel_plan_sha256,
        )
        if time.perf_counter() - started >= MAXIMUM_RUNTIME_SECONDS:
            runtime_limit_reached = True
            break
    manifest = completed_manifest(nodes, panels, panel_plan_sha256)
    write_csv(SHARD_MANIFEST, manifest)
    completed_count = sum(parse_bool(row["shard_complete"]) for row in manifest)
    all_complete = completed_count == len(manifest)
    formal_end = M5283.formal_inventory_digest()
    if not all_complete:
        decision = (
            "RUNTIME_BOUND_REACHED__RESUME_REMAINING_REGULATOR_SHARDS"
            if runtime_limit_reached
            else "REGULATOR_SHARDS_INCOMPLETE__RESUME"
        )
        result = {
            "checkpoint": CHECKPOINT,
            "parent_checkpoint": PARENT_CHECKPOINT,
            "marker": MARKER,
            "revision": REVISION,
            "mode": "selected-energy-five-regulator-ladders-partial",
            "acceptance_passed": False,
            "decision": decision,
            "planned_shard_count": len(manifest),
            "completed_shard_count": completed_count,
            "remaining_shard_count": len(manifest) - completed_count,
            "runtime_limit_reached": runtime_limit_reached,
            "formalization_workbench_end_digest": formal_end,
            "formalization_workbench_modified_file_count": (
                0
                if formal_end == str(parent["formalization_workbench_end_digest"])
                else -1
            ),
            "claim_boundary": {field: False for field in CLAIM_FIELDS},
            "runtime_seconds": time.perf_counter() - started,
        }
        atomic_json(RESULT, result)
        atomic_json(
            STATUS,
            {
                "checkpoint": CHECKPOINT,
                "state": "PARTIAL",
                "decision": decision,
                "completed_shard_count": completed_count,
                "remaining_shard_count": len(manifest) - completed_count,
            },
        )
        return result
    integrals = integral_rows(manifest)
    limit_rows, summaries = limit_products(integrals)
    write_csv(INTEGRALS, integrals)
    write_csv(LIMITS, limit_rows)
    maximum_quadrature_change = max(
        float(row["order4_order8_relative_change"]) for row in integrals
    )
    maximum_richardson_change = max(
        float(row["last_two_richardson_relative_change"])
        for row in summaries
    )
    maximum_model_change = max(
        float(row["small_regulator_model_intercept_relative_change"])
        for row in summaries
    )
    checks = {
        "all_forty_shards_complete": all_complete,
        "all_quadrature_nodes_inside_exact_net_support": all(
            parse_bool(row["all_quadrature_nodes_mask_active"])
            for row in manifest
        ),
        "all_finite_regulator_integrals_finite": all(
            math.isfinite(float(row[field]))
            for row in integrals
            for field in (
                "edge_integral_real",
                "edge_integral_imaginary",
                "edge_integral_magnitude",
            )
        ),
        "all_finite_regulator_integrals_quadrature_converged": all(
            parse_bool(row["passes_edge_quadrature_gate"])
            for row in integrals
        ),
        "all_selected_node_regulator_zero_limits_stable": all(
            bool(row["regulator_zero_limit_stable"])
            for row in summaries
        ),
        "integration_precision_initialized": (
            mp.mp.dps >= M5280.MP_DECIMAL_DIGITS
        ),
        "formalization_workbench_unchanged": (
            formal_end == str(parent["formalization_workbench_end_digest"])
        ),
        "claims_locked_false": True,
    }
    accepted = all(checks.values())
    decision = (
        "FOUR_SELECTED_ENERGY_REGULATOR_ZERO_LIMITS_RESOLVED__"
        "TEST_ENERGY_INTERPOLATION_AND_CUBATURE"
        if accepted
        else "SELECTED_ENERGY_REGULATOR_LADDERS_REQUIRE_REFINEMENT"
    )
    result = {
        "checkpoint": CHECKPOINT,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "mode": "selected-energy-five-regulator-ladders",
        "checks": checks,
        "acceptance_passed": accepted,
        "decision": decision,
        "planned_shard_count": len(manifest),
        "completed_shard_count": completed_count,
        "selected_energy_node_count": len(nodes),
        "finite_regulator_integral_row_count": len(integrals),
        "regulator_zero_summary_rows": summaries,
        "maximum_order4_order8_relative_change": maximum_quadrature_change,
        "maximum_last_two_richardson_relative_change": maximum_richardson_change,
        "maximum_small_regulator_model_intercept_relative_change": maximum_model_change,
        "integration_mp_decimal_digits": mp.mp.dps,
        "formalization_workbench_reference_digest": str(
            parent["formalization_workbench_end_digest"]
        ),
        "formalization_workbench_end_digest": formal_end,
        "formalization_workbench_modified_file_count": (
            0
            if formal_end == str(parent["formalization_workbench_end_digest"])
            else -1
        ),
        "claim_boundary": {
            "valid_for_selected_energy_five_regulator_integrals": accepted,
            "valid_for_selected_energy_regulator_zero_limits": accepted,
            "valid_for_energy_interpolation": False,
            "valid_for_boundary_aligned_energy_angle_cubature": False,
            **{field: False for field in CLAIM_FIELDS},
            "reason": (
                "Four selected fixed-decay energy slices do not establish "
                "a converged energy integral or the decay-angle integral."
            ),
        },
        "resource_contract": {
            "maximum_task_python_processes": 1,
            "worker_math_threads": 1,
            "windows_priority": "BelowNormal",
            "maximum_silent_work_hours": 4,
            "runtime_stop_seconds": MAXIMUM_RUNTIME_SECONDS,
        },
        "source_files": source_rows(),
        "runtime_seconds": time.perf_counter() - started,
    }
    atomic_json(RESULT, result)
    atomic_json(
        STATUS,
        {
            "checkpoint": CHECKPOINT,
            "state": "COMPLETE" if accepted else "FAILED",
            "decision": decision,
            "completed_shard_count": completed_count,
            "maximum_order4_order8_relative_change": maximum_quadrature_change,
        },
    )
    return result


def validation_gate(gate: str, passed: bool, detail: str) -> dict[str, Any]:
    return {"gate": gate, "passed": bool(passed), "detail": detail}


def render_document(result: dict[str, Any], passed: bool) -> None:
    lines = [
        "# 5306 — Selected-energy five-regulator ladders",
        "",
        "## Result",
        "",
        "The exact activation/cancellation support from 5305 was integrated at",
        "four representative fixed-decay energy nodes. Each node uses all five",
        "regulators, order-4/order-8 angular quadrature, and a resumable shard",
        "per regulator/order pair.",
        "",
        f"- completed shards: `{result['completed_shard_count']}/{result['planned_shard_count']}`;",
        f"- maximum order change: `{result['maximum_order4_order8_relative_change']:.12g}`;",
        f"- maximum final Richardson change: `{result['maximum_last_two_richardson_relative_change']:.12g}`;",
        f"- maximum model-intercept change: `{result['maximum_small_regulator_model_intercept_relative_change']:.12g}`;",
        "",
        "| node | energy | zero-regulator estimate | stable |",
        "|---|---:|---:|:---:|",
    ]
    for row in result["regulator_zero_summary_rows"]:
        lines.append(
            "| {energy_node_id} | {soft_energy:.12g} | "
            "{regulator_zero_estimate_real:.9g} "
            "{regulator_zero_estimate_imaginary:+.9g} i | {stable} |".format(
                stable="yes" if row["regulator_zero_limit_stable"] else "no",
                **row,
            )
        )
    lines.extend(
        (
            "",
            f"Decision: **{result['decision']}**.",
            "",
            f"Validation: **{'PASS' if passed else 'FAIL'}**.",
            "",
            "## Claim boundary",
            "",
            "These are four selected fixed-decay slices. They do not yet prove",
            "energy interpolation, the energy integral, the decay-angle integral,",
            "the phase-space coefficient, local GR, or the full MTS theory.",
            "",
        )
    )
    DOCUMENT.write_text("\n".join(lines), encoding="utf-8")


def validate_outputs() -> dict[str, Any]:
    started = time.perf_counter()
    result = read_json(RESULT)
    manifest = read_csv(SHARD_MANIFEST)
    integrals = read_csv(INTEGRALS)
    limits = read_csv(LIMITS)
    gates = [
        validation_gate(
            "result_pipeline_accepted",
            bool(result["acceptance_passed"]),
            str(result["decision"]),
        ),
        validation_gate(
            "forty_resumable_shards_complete",
            len(manifest) == 40
            and all(parse_bool(row["shard_complete"]) for row in manifest),
            f"rows={len(manifest)}",
        ),
        validation_gate(
            "all_finite_regulator_integrals_converged",
            len(integrals) == 4 * len(M5303.REGULATORS) * len(QUADRATURE_ORDERS)
            and all(
                parse_bool(row["passes_edge_quadrature_gate"])
                for row in integrals
            ),
            f"rows={len(integrals)}",
        ),
        validation_gate(
            "all_limit_estimates_complete",
            len(limits) == 4 * 9,
            f"rows={len(limits)}",
        ),
        validation_gate(
            "formal_workbench_unchanged",
            M5283.formal_inventory_digest()
            == str(result["formalization_workbench_end_digest"]),
            str(result["formalization_workbench_end_digest"]),
        ),
        validation_gate(
            "full_claims_locked_false",
            all(
                not bool(result["claim_boundary"][field])
                for field in CLAIM_FIELDS
            ),
            "no phase-space, UV, local-GR, or full-MTS claim",
        ),
    ]
    passed = all(bool(row["passed"]) for row in gates)
    write_csv(VALIDATION, gates)
    write_csv(RESIDUAL_VALIDATION, gates)
    render_document(result, passed)
    return {
        "checkpoint": CHECKPOINT,
        "mode": "validation",
        "acceptance_passed": passed,
        "decision": (
            "VALIDATED_SELECTED_ENERGY_FIVE_REGULATOR_LADDERS"
            if passed
            else "SELECTED_ENERGY_REGULATOR_LADDER_VALIDATION_FAILED"
        ),
        "runtime_seconds": time.perf_counter() - started,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=("dry-run", "run", "validate"),
        required=True,
    )
    return parser.parse_args()


def main() -> int:
    arguments = parse_args()
    if arguments.mode == "dry-run":
        result = dry_run()
    elif arguments.mode == "run":
        result = execute()
    else:
        result = validate_outputs()
    print(
        json.dumps(
            {
                "checkpoint": result["checkpoint"],
                "mode": result["mode"],
                "acceptance_passed": result["acceptance_passed"],
                "decision": result["decision"],
                "runtime_seconds": result["runtime_seconds"],
            },
            sort_keys=True,
        )
    )
    return 0 if result["acceptance_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
