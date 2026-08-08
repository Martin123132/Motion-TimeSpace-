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
SOURCE = FUNCTIONAL_RG / "5307"
NODE_RUNS = SOURCE / "nodes"

SCRIPT_5306 = SCRIPTS / "Y5_R2FR_5306_selected_energy_five_regulator_ladders.py"
RESULT_5306 = FUNCTIONAL_RG / "5306" / "selected_energy_regulator_ladders_result.json"
VALIDATION_5306 = FUNCTIONAL_RG / "5306" / "selected_energy_regulator_ladders_validation.csv"
STATUS_5306 = FUNCTIONAL_RG / "5306" / "status.json"
MANIFEST_5306 = FUNCTIONAL_RG / "5306" / "selected_energy_regulator_shard_manifest.csv"
INTEGRALS_5306 = FUNCTIONAL_RG / "5306" / "selected_energy_finite_regulator_integrals.csv"

DRY_RUN = SOURCE / "N04_secondary_peak_refinement_dry_run.json"
DISCREPANCY = SOURCE / "N04_parent_panel_discrepancy.csv"
PEAK_SCAN = SOURCE / "N04_secondary_peak_scan.csv"
PEAK_RESULT = SOURCE / "N04_secondary_peak_result.json"
REFINED_PANELS = SOURCE / "N04_secondary_peak_refined_panel_plan.csv"
SHARD_MANIFEST = SOURCE / "N04_refined_regulator_shard_manifest.csv"
N04_INTEGRALS = SOURCE / "N04_refined_finite_regulator_integrals.csv"
COMBINED_INTEGRALS = SOURCE / "four_node_refined_finite_regulator_integrals.csv"
LIMITS = SOURCE / "four_node_refined_regulator_zero_limits.csv"
RESULT = SOURCE / "N04_secondary_peak_refinement_result.json"
VALIDATION = SOURCE / "N04_secondary_peak_refinement_validation.csv"
RESIDUAL_VALIDATION = RESIDUALS / "P8_Y5_BRR545_5307_VALIDATION.csv"
STATUS = SOURCE / "status.json"
DOCUMENT = POST / "5307-Y5-R2FR-N04-secondary-peak-adaptive-refinement.md"

CHECKPOINT = 5307
PARENT_CHECKPOINT = 5306
MARKER = "MTS_5307_N04_SECONDARY_PEAK_ADAPTIVE_REFINEMENT"
REVISION = "N04-secondary-peak-adaptive-refinement-v1"
SHARD_REVISION = "N04-secondary-peak-refined-shard-v1"
TARGET_NODE_ID = "N04_INNER_HIGH_MID"
TARGET_EPSILON_ID = "E0025"
QUADRATURE_ORDERS = (4, 8)
MAXIMUM_RUNTIME_SECONDS = 2.5 * 60.0 * 60.0
PEAK_REFERENCE_CHANGE_LIMIT = 5.0e-5
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


M5306 = load_module("mts_5306_for_5307", SCRIPT_5306)
M5305 = M5306.M5305
M5303 = M5306.M5303
M5301 = M5306.M5301
M5280 = M5306.M5280
M5283 = M5306.M5283
np = M5306.np
mp = M5306.mp


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


def target_node() -> dict[str, str]:
    return next(
        row for row in read_csv(M5305.NODES)
        if row["energy_node_id"] == TARGET_NODE_ID
    )


def parent_panel_rows(order: int) -> list[dict[str, str]]:
    return read_csv(
        M5306.shard_paths(TARGET_NODE_ID, TARGET_EPSILON_ID, order)["panels"]
    )


def parent_discrepancy_rows() -> list[dict[str, Any]]:
    lower = parent_panel_rows(min(QUADRATURE_ORDERS))
    upper = parent_panel_rows(max(QUADRATURE_ORDERS))
    if len(lower) != len(upper):
        raise RuntimeError("parent N04 panel rows do not align")
    rows: list[dict[str, Any]] = []
    for lower_row, upper_row in zip(lower, upper):
        lower_value = complex(
            float(lower_row["panel_integral_real"]),
            float(lower_row["panel_integral_imaginary"]),
        )
        upper_value = complex(
            float(upper_row["panel_integral_real"]),
            float(upper_row["panel_integral_imaginary"]),
        )
        difference = upper_value - lower_value
        rows.append(
            {
                "energy_node_id": TARGET_NODE_ID,
                "epsilon_id": TARGET_EPSILON_ID,
                "panel_index": int(lower_row["panel_index"]),
                "left_absolute_soft_cosine": float(
                    lower_row["left_absolute_soft_cosine"]
                ),
                "right_absolute_soft_cosine": float(
                    lower_row["right_absolute_soft_cosine"]
                ),
                "panel_width": float(lower_row["panel_width"]),
                **complex_fields("order4_panel_integral", lower_value),
                **complex_fields("order8_panel_integral", upper_value),
                **complex_fields("order8_minus_order4", difference),
                "valid_for_parent_panel_discrepancy_localization": True,
                **{field: False for field in CLAIM_FIELDS},
            }
        )
    return rows


def unique_coordinates(values: list[float], lower: float, upper: float) -> list[float]:
    clipped = sorted(max(lower, min(upper, value)) for value in values)
    result: list[float] = []
    for value in clipped:
        if not result or abs(value - result[-1]) > 2.0e-14:
            result.append(value)
    return result


def localize_secondary_peak(evaluate: Any) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    discrepancies = parent_discrepancy_rows()
    worst = max(
        discrepancies,
        key=lambda row: float(row["order8_minus_order4_magnitude"]),
    )
    lower = float(worst["left_absolute_soft_cosine"])
    upper = float(worst["right_absolute_soft_cosine"])
    energy = float(target_node()["soft_energy"])
    reference = float(read_json(STATUS_5306)["refinement_peak_absolute_soft_cosine"])
    evaluated: dict[float, tuple[complex, bool, str]] = {}
    coordinates = [float(value) for value in np.linspace(lower, upper, 501)]
    for stage in ("PANEL_SCAN", "REFINE_1", "REFINE_2"):
        for coordinate in coordinates:
            if coordinate in evaluated:
                continue
            value, active = M5305.edge_component(
                evaluate,
                TARGET_EPSILON_ID,
                energy,
                coordinate,
            )
            evaluated[coordinate] = (value, active, stage)
        active_values = [
            (coordinate, value)
            for coordinate, (value, active, _) in evaluated.items()
            if active
        ]
        peak_coordinate, _ = max(active_values, key=lambda item: abs(item[1]))
        if stage == "PANEL_SCAN":
            span = (upper - lower) / 500.0
        elif stage == "REFINE_1":
            span = (upper - lower) / 5000.0
        else:
            break
        coordinates = unique_coordinates(
            [
                peak_coordinate + float(offset)
                for offset in np.linspace(-span, span, 201)
            ],
            lower,
            upper,
        )
    rows: list[dict[str, Any]] = []
    for coordinate, (value, active, stage) in sorted(evaluated.items()):
        rows.append(
            {
                "scan_stage": stage,
                "soft_energy": energy,
                "epsilon_id": TARGET_EPSILON_ID,
                "absolute_soft_cosine": coordinate,
                "edge_mask_active": active,
                **complex_fields("edge_component", value),
                **{field: False for field in CLAIM_FIELDS},
            }
        )
    peak = max(
        (row for row in rows if row["edge_mask_active"]),
        key=lambda row: float(row["edge_component_magnitude"]),
    )
    peak_coordinate = float(peak["absolute_soft_cosine"])
    result = {
        "parent_failed_panel_index": int(worst["panel_index"]),
        "parent_failed_panel_left": lower,
        "parent_failed_panel_right": upper,
        "parent_failed_panel_order_difference_magnitude": float(
            worst["order8_minus_order4_magnitude"]
        ),
        "secondary_peak_absolute_soft_cosine": peak_coordinate,
        "secondary_peak_magnitude": float(peak["edge_component_magnitude"]),
        "reference_peak_absolute_soft_cosine": reference,
        "reference_peak_absolute_change": abs(peak_coordinate - reference),
        "peak_scan_row_count": len(rows),
        "valid_for_secondary_peak_refinement": (
            lower < peak_coordinate < upper
            and abs(peak_coordinate - reference) <= PEAK_REFERENCE_CHANGE_LIMIT
        ),
    }
    return rows, result


def refined_panel_rows(peak: float) -> list[dict[str, Any]]:
    base = [
        row for row in read_csv(M5305.PANELS)
        if row["energy_node_id"] == TARGET_NODE_ID
    ]
    values = [float(base[0]["left_absolute_soft_cosine"])]
    values.extend(float(row["right_absolute_soft_cosine"]) for row in base)
    values.extend(
        peak + float(offset)
        for offset in np.arange(-1.0e-3, 1.0e-3 + 0.5e-5, 1.0e-5)
    )
    values.extend(
        peak + float(offset)
        for offset in np.arange(-1.0e-4, 1.0e-4 + 1.0e-6, 2.0e-6)
    )
    values.extend(
        peak + float(offset)
        for offset in np.arange(-2.0e-5, 2.0e-5 + 2.0e-7, 4.0e-7)
    )
    lower = float(base[0]["left_absolute_soft_cosine"])
    upper = float(base[-1]["right_absolute_soft_cosine"])
    coordinates = unique_coordinates(values, lower, upper)
    rows: list[dict[str, Any]] = []
    for panel_index, (left, right) in enumerate(
        zip(coordinates[:-1], coordinates[1:]), start=1
    ):
        rows.append(
            {
                "energy_node_id": TARGET_NODE_ID,
                "panel_index": panel_index,
                "left_absolute_soft_cosine": left,
                "right_absolute_soft_cosine": right,
                "panel_width": right - left,
                "intersects_secondary_peak_core": (
                    left >= peak - 2.0001e-5
                    and right <= peak + 2.0001e-5
                ),
                "valid_for_secondary_peak_refined_panel_plan": (
                    lower <= left < right <= upper
                ),
                **{field: False for field in CLAIM_FIELDS},
            }
        )
    return rows


def prepare_refinement(evaluate: Any) -> tuple[list[dict[str, str]], dict[str, Any]]:
    if REFINED_PANELS.exists() and PEAK_RESULT.exists():
        return read_csv(REFINED_PANELS), read_json(PEAK_RESULT)
    discrepancies = parent_discrepancy_rows()
    scans, peak_result = localize_secondary_peak(evaluate)
    panels = refined_panel_rows(
        float(peak_result["secondary_peak_absolute_soft_cosine"])
    )
    write_csv(DISCREPANCY, discrepancies)
    write_csv(PEAK_SCAN, scans)
    write_csv(REFINED_PANELS, panels)
    atomic_json(PEAK_RESULT, peak_result)
    return read_csv(REFINED_PANELS), peak_result


def shard_paths(epsilon_id: str, order: int) -> dict[str, Path]:
    root = NODE_RUNS / TARGET_NODE_ID / epsilon_id / f"Q{order:02d}"
    return {
        "root": root,
        "panels": root / "panel_integrals.csv",
        "result": root / "result.json",
    }


def shard_is_valid(
    epsilon_id: str,
    order: int,
    panel_count: int,
    panel_sha256: str,
) -> bool:
    paths = shard_paths(epsilon_id, order)
    if not paths["result"].exists() or not paths["panels"].exists():
        return False
    try:
        result = read_json(paths["result"])
        rows = read_csv(paths["panels"])
    except Exception:
        return False
    return (
        result.get("shard_revision") == SHARD_REVISION
        and result.get("epsilon_id") == epsilon_id
        and int(result.get("quadrature_order", -1)) == order
        and int(result.get("panel_count", -1)) == panel_count
        and result.get("panel_plan_sha256") == panel_sha256
        and bool(result.get("all_quadrature_nodes_mask_active"))
        and len(rows) == panel_count
    )


def integrate_shard(
    node: dict[str, str],
    panels: list[dict[str, str]],
    epsilon_id: str,
    epsilon: float,
    order: int,
    evaluate: Any,
    multiplier: float,
    panel_sha256: str,
) -> dict[str, Any]:
    paths = shard_paths(epsilon_id, order)
    paths["root"].mkdir(parents=True, exist_ok=True)
    started = time.perf_counter()
    quadrature_nodes, quadrature_weights = np.polynomial.legendre.leggauss(order)
    energy = float(node["soft_energy"])
    total = 0.0j
    inactive_count = 0
    rows: list[dict[str, Any]] = []
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
                "energy_node_id": TARGET_NODE_ID,
                "soft_energy": energy,
                "epsilon_id": epsilon_id,
                "epsilon": epsilon,
                "quadrature_order": order,
                "panel_index": int(panel["panel_index"]),
                "left_absolute_soft_cosine": left,
                "right_absolute_soft_cosine": right,
                "panel_width": right - left,
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
                    "stage": "N04_REFINED_REGULATOR_SHARD",
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
        "energy_node_id": TARGET_NODE_ID,
        "soft_energy": energy,
        "epsilon_id": epsilon_id,
        "epsilon": epsilon,
        "quadrature_order": order,
        "panel_count": len(panels),
        "quadrature_node_evaluation_count": len(panels) * order,
        "inactive_quadrature_node_count": inactive_count,
        "all_quadrature_nodes_mask_active": inactive_count == 0,
        **complex_fields("edge_integral", total),
        "panel_plan_sha256": panel_sha256,
        "runtime_seconds": time.perf_counter() - started,
        **{field: False for field in CLAIM_FIELDS},
    }
    atomic_json(paths["result"], result)
    return result


def manifest_rows(
    panels: list[dict[str, str]],
    panel_sha256: str,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for epsilon_id, epsilon in M5303.REGULATORS:
        for order in QUADRATURE_ORDERS:
            paths = shard_paths(epsilon_id, order)
            complete = shard_is_valid(
                epsilon_id, order, len(panels), panel_sha256
            )
            result = read_json(paths["result"]) if complete else {}
            rows.append(
                {
                    "energy_node_id": TARGET_NODE_ID,
                    "epsilon_id": epsilon_id,
                    "epsilon": epsilon,
                    "quadrature_order": order,
                    "panel_count": len(panels),
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


def refined_integral_rows(manifest: list[dict[str, Any]]) -> list[dict[str, Any]]:
    results = {
        (row["epsilon_id"], int(row["quadrature_order"])): read_json(
            Path(row["shard_result_path"])
        )
        for row in manifest
        if parse_bool(row["shard_complete"])
    }
    rows: list[dict[str, Any]] = []
    for epsilon_id, epsilon in M5303.REGULATORS:
        lower = results[(epsilon_id, min(QUADRATURE_ORDERS))]
        upper = results[(epsilon_id, max(QUADRATURE_ORDERS))]
        lower_value = complex(
            float(lower["edge_integral_real"]),
            float(lower["edge_integral_imaginary"]),
        )
        upper_value = complex(
            float(upper["edge_integral_real"]),
            float(upper["edge_integral_imaginary"]),
        )
        change = relative_complex_change(lower_value, upper_value)
        for order, value in (
            (min(QUADRATURE_ORDERS), lower_value),
            (max(QUADRATURE_ORDERS), upper_value),
        ):
            rows.append(
                {
                    "energy_node_id": TARGET_NODE_ID,
                    "soft_energy": lower["soft_energy"],
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


def source_rows() -> list[dict[str, str]]:
    paths = (
        Path(__file__).resolve(),
        SCRIPT_5306,
        RESULT_5306,
        VALIDATION_5306,
        STATUS_5306,
        MANIFEST_5306,
        INTEGRALS_5306,
    )
    return [{"path": str(path), "sha256": digest(path)} for path in paths]


def dry_run() -> dict[str, Any]:
    SOURCE.mkdir(parents=True, exist_ok=True)
    parent = read_json(RESULT_5306)
    status = read_json(STATUS_5306)
    manifest = read_csv(MANIFEST_5306)
    integrals = read_csv(INTEGRALS_5306)
    failed_rows = [
        row for row in integrals
        if not parse_bool(row["passes_edge_quadrature_gate"])
    ]
    checks = {
        "parent_5306_completed_all_shards": (
            int(parent["completed_shard_count"]) == 40
            and len(manifest) == 40
            and all(parse_bool(row["shard_complete"]) for row in manifest)
        ),
        "parent_failure_is_only_N04": (
            bool(failed_rows)
            and {row["energy_node_id"] for row in failed_rows}
            == {TARGET_NODE_ID}
        ),
        "parent_status_records_resumable_panel_489": (
            status["state"] == "REFINEMENT_REQUIRED"
            and int(status["failed_panel_index"]) == 489
            and bool(status["resumable_without_repeating_other_nodes"])
        ),
        "thirty_parent_rows_are_converged_and_reusable": (
            len(
                [
                    row for row in integrals
                    if row["energy_node_id"] != TARGET_NODE_ID
                    and parse_bool(row["passes_edge_quadrature_gate"])
                ]
            )
            == 30
        ),
        "ten_selective_refinement_shards_planned": (
            len(M5303.REGULATORS) * len(QUADRATURE_ORDERS) == 10
        ),
        "runtime_bound_below_four_hours": (
            MAXIMUM_RUNTIME_SECONDS < 4.0 * 3600.0
        ),
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
        "reused_parent_integral_row_count": 30,
        "planned_refined_shard_count": 10,
        "maximum_runtime_seconds": MAXIMUM_RUNTIME_SECONDS,
        "decision": (
            "DRY_RUN_ACCEPTED__REFINE_ONLY_N04_SECONDARY_PEAK"
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
        raise RuntimeError("5307 dry run did not pass")
    parent = read_json(RESULT_5306)
    node = target_node()
    context = M5303.synthetic_context()
    evaluate = M5305.component_evaluator(context)
    panels, peak_result = prepare_refinement(evaluate)
    panel_sha256 = digest(REFINED_PANELS)
    multiplier = M5301.M5300.M5292.physical_multiplier()
    runtime_limit_reached = False
    for epsilon_id, epsilon in M5303.REGULATORS:
        for order in QUADRATURE_ORDERS:
            if shard_is_valid(
                epsilon_id, order, len(panels), panel_sha256
            ):
                continue
            integrate_shard(
                node,
                panels,
                epsilon_id,
                epsilon,
                order,
                evaluate,
                multiplier,
                panel_sha256,
            )
            if time.perf_counter() - started >= MAXIMUM_RUNTIME_SECONDS:
                runtime_limit_reached = True
                break
        if runtime_limit_reached:
            break
    manifest = manifest_rows(panels, panel_sha256)
    write_csv(SHARD_MANIFEST, manifest)
    completed_count = sum(parse_bool(row["shard_complete"]) for row in manifest)
    formal_end = M5283.formal_inventory_digest()
    if completed_count != len(manifest):
        decision = "RUNTIME_BOUND_REACHED__RESUME_N04_REFINED_SHARDS"
        result = {
            "checkpoint": CHECKPOINT,
            "parent_checkpoint": PARENT_CHECKPOINT,
            "marker": MARKER,
            "revision": REVISION,
            "mode": "N04-secondary-peak-refinement-partial",
            "acceptance_passed": False,
            "decision": decision,
            "completed_refined_shard_count": completed_count,
            "remaining_refined_shard_count": len(manifest) - completed_count,
            "formalization_workbench_end_digest": formal_end,
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
                "completed_refined_shard_count": completed_count,
            },
        )
        return result
    n04_integrals = refined_integral_rows(manifest)
    parent_reused = [
        row for row in read_csv(INTEGRALS_5306)
        if row["energy_node_id"] != TARGET_NODE_ID
    ]
    combined: list[dict[str, Any]] = [*parent_reused, *n04_integrals]
    combined.sort(
        key=lambda row: (
            row["energy_node_id"],
            float(row["epsilon"]),
            int(row["quadrature_order"]),
        )
    )
    limit_rows, summaries = M5306.limit_products(combined)
    write_csv(N04_INTEGRALS, n04_integrals)
    write_csv(COMBINED_INTEGRALS, combined)
    write_csv(LIMITS, limit_rows)
    maximum_order_change = max(
        float(row["order4_order8_relative_change"]) for row in combined
    )
    n04_order_change = max(
        float(row["order4_order8_relative_change"])
        for row in n04_integrals
    )
    maximum_richardson_change = max(
        float(row["last_two_richardson_relative_change"])
        for row in summaries
    )
    maximum_model_change = max(
        float(row["small_regulator_model_intercept_relative_change"])
        for row in summaries
    )
    n04_summary = next(
        row for row in summaries if row["energy_node_id"] == TARGET_NODE_ID
    )
    old_n04_summary = next(
        row for row in parent["regulator_zero_summary_rows"]
        if row["energy_node_id"] == TARGET_NODE_ID
    )
    old_n04_estimate = complex(
        float(old_n04_summary["regulator_zero_estimate_real"]),
        float(old_n04_summary["regulator_zero_estimate_imaginary"]),
    )
    new_n04_estimate = complex(
        float(n04_summary["regulator_zero_estimate_real"]),
        float(n04_summary["regulator_zero_estimate_imaginary"]),
    )
    checks = {
        "secondary_peak_reproduced_and_refined": bool(
            peak_result["valid_for_secondary_peak_refinement"]
        ),
        "all_ten_refined_shards_complete": completed_count == 10,
        "all_refined_quadrature_nodes_inside_support": all(
            parse_bool(row["all_quadrature_nodes_mask_active"])
            for row in manifest
        ),
        "N04_all_five_regulators_quadrature_converged": all(
            parse_bool(row["passes_edge_quadrature_gate"])
            for row in n04_integrals
        ),
        "all_four_regulator_zero_limits_stable": all(
            bool(row["regulator_zero_limit_stable"])
            for row in summaries
        ),
        "thirty_parent_integral_rows_reused_without_recompute": (
            len(parent_reused) == 30
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
        else "N04_SECONDARY_PEAK_REFINEMENT_REQUIRES_FURTHER_WORK"
    )
    result = {
        "checkpoint": CHECKPOINT,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "mode": "N04-secondary-peak-adaptive-refinement",
        "checks": checks,
        "acceptance_passed": accepted,
        "decision": decision,
        "reused_parent_integral_row_count": len(parent_reused),
        "completed_refined_shard_count": completed_count,
        "refined_panel_count": len(panels),
        "peak_result": peak_result,
        "maximum_order4_order8_relative_change": maximum_order_change,
        "N04_maximum_order4_order8_relative_change": n04_order_change,
        "maximum_last_two_richardson_relative_change": maximum_richardson_change,
        "maximum_small_regulator_model_intercept_relative_change": maximum_model_change,
        "N04_old_new_zero_estimate_relative_change": relative_complex_change(
            old_n04_estimate, new_n04_estimate
        ),
        "regulator_zero_summary_rows": summaries,
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
            "valid_for_four_selected_energy_regulator_zero_limits": accepted,
            "valid_for_energy_interpolation": False,
            "valid_for_boundary_aligned_energy_angle_cubature": False,
            **{field: False for field in CLAIM_FIELDS},
            "reason": (
                "The four selected fixed-decay slices are controlled, but "
                "the continuous energy and decay-angle integrations remain."
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
            "completed_refined_shard_count": completed_count,
            "N04_maximum_order4_order8_relative_change": n04_order_change,
        },
    )
    return result


def validation_gate(gate: str, passed: bool, detail: str) -> dict[str, Any]:
    return {"gate": gate, "passed": bool(passed), "detail": detail}


def render_document(result: dict[str, Any], passed: bool) -> None:
    lines = [
        "# 5307 — N04 secondary-peak adaptive refinement",
        "",
        "## Repair",
        "",
        "The 5306 order discrepancy was isolated to one N04 panel. A local",
        "E0025 scan resolves a second narrow peak and the panel is replaced by",
        "nested 1e-5, 2e-6, and 4e-7 angular spacing around that peak.",
        "The thirty converged parent integral rows are reused unchanged; only",
        "the ten N04 regulator/order shards are recomputed.",
        "",
        f"- secondary peak: `{result['peak_result']['secondary_peak_absolute_soft_cosine']:.15g}`;",
        f"- refined panels: `{result['refined_panel_count']}`;",
        f"- completed refined shards: `{result['completed_refined_shard_count']}/10`;",
        f"- N04 maximum order change: `{result['N04_maximum_order4_order8_relative_change']:.12g}`;",
        f"- maximum final Richardson change: `{result['maximum_last_two_richardson_relative_change']:.12g}`;",
        f"- maximum model-intercept change: `{result['maximum_small_regulator_model_intercept_relative_change']:.12g}`;",
        "",
        "| node | energy | zero-regulator estimate | stable |",
        "|---|---:|---:|:---:|",
    ]
    for row in result["regulator_zero_summary_rows"]:
        soft_energy = float(row["soft_energy"])
        estimate_real = float(row["regulator_zero_estimate_real"])
        estimate_imaginary = float(
            row["regulator_zero_estimate_imaginary"]
        )
        stable = (
            "yes"
            if parse_bool(row["regulator_zero_limit_stable"])
            else "no"
        )
        lines.append(
            f"| {row['energy_node_id']} | {soft_energy:.12g} | "
            f"{estimate_real:.9g} {estimate_imaginary:+.9g} i | "
            f"{stable} |"
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
            "This controls four selected fixed-decay energy slices. It does not",
            "yet establish continuous energy interpolation, the energy integral,",
            "the decay-angle integral, the full phase-space coefficient, local",
            "GR, or the full MTS theory.",
            "",
        )
    )
    DOCUMENT.write_text("\n".join(lines), encoding="utf-8")


def validate_outputs() -> dict[str, Any]:
    started = time.perf_counter()
    result = read_json(RESULT)
    manifest = read_csv(SHARD_MANIFEST)
    n04 = read_csv(N04_INTEGRALS)
    combined = read_csv(COMBINED_INTEGRALS)
    limits = read_csv(LIMITS)
    panels = read_csv(REFINED_PANELS)
    parent_rows = [
        row for row in read_csv(INTEGRALS_5306)
        if row["energy_node_id"] != TARGET_NODE_ID
    ]
    combined_parent_rows = [
        row for row in combined
        if row["energy_node_id"] != TARGET_NODE_ID
    ]
    parent_fields = tuple(parent_rows[0])
    row_key = lambda row: (
        row["energy_node_id"],
        row["epsilon_id"],
        int(row["quadrature_order"]),
    )
    parent_rows_unchanged = all(
        tuple(parent.get(field, "") for field in parent_fields)
        == tuple(combined_parent.get(field, "") for field in parent_fields)
        for parent, combined_parent in zip(
            sorted(parent_rows, key=row_key),
            sorted(combined_parent_rows, key=row_key),
        )
    )
    source_files_current = all(
        Path(row["path"]).exists()
        and digest(Path(row["path"])) == row["sha256"]
        for row in result["source_files"]
    )
    gates = [
        validation_gate(
            "result_pipeline_accepted",
            bool(result["acceptance_passed"]),
            str(result["decision"]),
        ),
        validation_gate(
            "ten_selective_shards_complete",
            len(manifest) == 10
            and all(parse_bool(row["shard_complete"]) for row in manifest),
            f"rows={len(manifest)}",
        ),
        validation_gate(
            "refined_panel_plan_complete",
            len(panels) == int(result["refined_panel_count"])
            and all(
                parse_bool(
                    row["valid_for_secondary_peak_refined_panel_plan"]
                )
                for row in panels
            ),
            f"rows={len(panels)}",
        ),
        validation_gate(
            "N04_and_combined_integrals_converged",
            len(n04) == 10
            and len(combined) == 40
            and all(
                parse_bool(row["passes_edge_quadrature_gate"])
                for row in combined
            ),
            f"N04={len(n04)}; combined={len(combined)}",
        ),
        validation_gate(
            "thirty_parent_rows_reused_byte_for_field",
            len(parent_rows) == 30
            and len(combined_parent_rows) == 30
            and parent_rows_unchanged,
            f"parent={len(parent_rows)}; combined={len(combined_parent_rows)}",
        ),
        validation_gate(
            "four_regulator_zero_summaries_stable",
            len(result["regulator_zero_summary_rows"]) == 4
            and all(
                parse_bool(row["regulator_zero_limit_stable"])
                for row in result["regulator_zero_summary_rows"]
            ),
            f"rows={len(result['regulator_zero_summary_rows'])}",
        ),
        validation_gate(
            "all_four_limit_estimates_complete",
            len(limits) == 36
            and all(
                not parse_bool(row["valid_for_full_phase_space_coefficient"])
                for row in limits
            ),
            f"rows={len(limits)}",
        ),
        validation_gate(
            "formal_workbench_unchanged",
            M5283.formal_inventory_digest()
            == str(result["formalization_workbench_end_digest"]),
            str(result["formalization_workbench_end_digest"]),
        ),
        validation_gate(
            "recorded_source_paths_and_hashes_current",
            source_files_current,
            f"rows={len(result['source_files'])}",
        ),
        validation_gate(
            "scripts_cache_absent",
            not (SCRIPTS / "__pycache__").exists(),
            str(SCRIPTS / "__pycache__"),
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
            "VALIDATED_N04_SECONDARY_PEAK_REFINEMENT"
            if passed
            else "N04_SECONDARY_PEAK_REFINEMENT_VALIDATION_FAILED"
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
    set_below_normal_priority()
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
