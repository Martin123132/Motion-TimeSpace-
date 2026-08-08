from __future__ import annotations

import argparse
import csv
import ctypes
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
SOURCE = FUNCTIONAL_RG / "5310"
SHARDS = SOURCE / "shards"

SCRIPT_5309 = SCRIPTS / "Y5_R2FR_5309_fixed_decay_pair_energy_soft_cubature.py"
RESULT_5309 = FUNCTIONAL_RG / "5309" / "fixed_decay_pair_cubature_result.json"
CONTRACT_5308 = FUNCTIONAL_RG / "5308" / "fixed_decay_energy_soft_cubature_contract.csv"
CELLS_5309 = FUNCTIONAL_RG / "5309" / "fixed_decay_pair_cubature_cell_integrals.csv"
DISCREPANCY_5309 = FUNCTIONAL_RG / "5309" / "fixed_decay_pair_cell_discrepancy.csv"
REDUCTION_5309 = FUNCTIONAL_RG / "5309" / "five_regulator_pair_reduction_transfer_audit.csv"

DRY_RUN = SOURCE / "anisotropic_refinement_dry_run.json"
TARGETS = SOURCE / "adaptive_target_cells.csv"
PLAN_TRACE = SOURCE / "E0025_adaptive_plan_trace.csv"
LEAF_PLAN = SOURCE / "E0025_adaptive_leaf_plan.csv"
PLAN_META = SOURCE / "E0025_adaptive_plan_meta.json"
MANIFEST = SOURCE / "adaptive_refinement_shard_manifest.csv"
LEAF_INTEGRALS = SOURCE / "five_regulator_adaptive_leaf_integrals.csv"
TARGET_INTEGRALS = SOURCE / "five_regulator_refined_target_cell_integrals.csv"
REFINED_CELLS = SOURCE / "five_regulator_refined_all_cell_integrals.csv"
REFINED_TOTALS = SOURCE / "five_regulator_refined_fixed_decay_integrals.csv"
CONVERGENCE = SOURCE / "refined_fixed_decay_cubature_convergence.csv"
LIMITS = SOURCE / "refined_fixed_decay_regulator_zero_limits.csv"
RESULT = SOURCE / "anisotropic_refinement_result.json"
VALIDATION = SOURCE / "anisotropic_refinement_validation.csv"
RESIDUAL_VALIDATION = RESIDUALS / "P8_Y5_BRR545_5310_VALIDATION.csv"
STATUS = SOURCE / "status.json"
DOCUMENT = POST / "5310-Y5-R2FR-anisotropic-topology-cell-refinement.md"

CHECKPOINT = 5310
PARENT_CHECKPOINT = 5309
MARKER = "MTS_5310_ANISOTROPIC_TOPOLOGY_CELL_REFINEMENT"
REVISION = "anisotropic-topology-cell-refinement-v1"
PLAN_REVISION = "E0025-anisotropic-recursive-plan-v1"
SHARD_REVISION = "five-regulator-adaptive-leaf-shard-v1"
TARGET_ERROR_FRACTION_MINIMUM = 5.0e-5
LOCAL_RELATIVE_LIMIT = 5.0e-4
GLOBAL_ORDER_CHANGE_LIMIT = 5.0e-3
CELL_ERROR_BUDGET_LIMIT = 1.0e-2
MAXIMUM_DEPTH = 6
MAXIMUM_LEAVES_PER_CELL = 256
PLAN_EPSILON_ID = "E0025"
LEAF_ORDERS = (4, 8)
MAXIMUM_RUNTIME_SECONDS = 2.75 * 60.0 * 60.0
CLAIM_FIELDS = (
    "valid_for_decay_angle_integration",
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


M5309 = load_module("mts_5309_for_5310", SCRIPT_5309)
M5308 = M5309.M5308
M5305 = M5309.M5305
M5303 = M5309.M5303
M5301 = M5309.M5301
M5280 = M5309.M5280
M5283 = M5309.M5283
np = M5309.np
mp = M5309.mp


def set_below_normal_priority() -> None:
    if os.name != "nt":
        return
    kernel32 = ctypes.WinDLL("kernel32", use_last_error=True)
    kernel32.GetCurrentProcess.restype = ctypes.c_void_p
    kernel32.SetPriorityClass.argtypes = (ctypes.c_void_p, ctypes.c_uint32)
    kernel32.SetPriorityClass.restype = ctypes.c_int
    process = kernel32.GetCurrentProcess()
    if not kernel32.SetPriorityClass(process, 0x00004000):
        raise ctypes.WinError()


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
    return M5309.parse_bool(value)


def complex_fields(prefix: str, value: complex) -> dict[str, float]:
    return M5309.complex_fields(prefix, value)


def relative_complex_change(first: complex, second: complex) -> float:
    return M5309.relative_complex_change(first, second)


def contract_lookup() -> dict[int, dict[str, str]]:
    return {
        int(row["contract_index"]): row for row in read_csv(CONTRACT_5308)
    }


def target_rows() -> list[dict[str, Any]]:
    contract = contract_lookup()
    rows = [
        row for row in read_csv(DISCREPANCY_5309)
        if row["epsilon_id"] == PLAN_EPSILON_ID
        and float(row["absolute_error_fraction_of_order8_total"])
        >= TARGET_ERROR_FRACTION_MINIMUM
    ]
    result: list[dict[str, Any]] = []
    for rank, row in enumerate(
        sorted(
            rows,
            key=lambda item: float(
                item["absolute_error_fraction_of_order8_total"]
            ),
            reverse=True,
        ),
        start=1,
    ):
        cell = contract[int(row["contract_index"])]
        result.append(
            {
                "target_rank": rank,
                "contract_index": row["contract_index"],
                "parent_error_fraction": row[
                    "absolute_error_fraction_of_order8_total"
                ],
                "parent_cell_relative_change": row["cell_relative_change"],
                "x_panel_index": cell["x_panel_index"],
                "lower_absolute_soft_cosine": cell[
                    "lower_absolute_soft_cosine"
                ],
                "upper_absolute_soft_cosine": cell[
                    "upper_absolute_soft_cosine"
                ],
                "lower_energy_boundary": cell["lower_energy_boundary"],
                "upper_energy_boundary": cell["upper_energy_boundary"],
                "evaluation_term_ids": cell["evaluation_term_ids"],
                "valid_for_adaptive_target_selection": True,
                **{field: False for field in CLAIM_FIELDS},
            }
        )
    return result


def integrate_region(
    cell: dict[str, str],
    epsilon_id: str,
    evaluate: Any,
    multiplier: float,
    u_lower: float,
    u_upper: float,
    v_lower: float,
    v_upper: float,
    x_order: int,
    energy_order: int,
) -> complex:
    x_nodes, x_weights = np.polynomial.legendre.leggauss(x_order)
    energy_nodes, energy_weights = np.polynomial.legendre.leggauss(
        energy_order
    )
    u_half = 0.5 * (u_upper - u_lower)
    u_midpoint = 0.5 * (u_upper + u_lower)
    v_half = 0.5 * (v_upper - v_lower)
    v_midpoint = 0.5 * (v_upper + v_lower)
    x_lower = float(cell["lower_absolute_soft_cosine"])
    x_width = (
        float(cell["upper_absolute_soft_cosine"]) - x_lower
    )
    selected_ids = M5309.term_ids(cell["evaluation_term_ids"])
    total = 0.0j
    for local_u, u_weight in zip(x_nodes, x_weights):
        u_value = u_midpoint + u_half * float(local_u)
        coordinate = x_lower + x_width * u_value
        energy_lower = M5308.boundary_energy(
            cell["lower_energy_boundary"], coordinate
        )
        energy_upper = M5308.boundary_energy(
            cell["upper_energy_boundary"], coordinate
        )
        energy_width = energy_upper - energy_lower
        for local_v, v_weight in zip(energy_nodes, energy_weights):
            v_value = v_midpoint + v_half * float(local_v)
            energy = energy_lower + energy_width * v_value
            value, inactive_count = M5309.evaluate_selected_terms(
                evaluate,
                epsilon_id,
                energy,
                coordinate,
                selected_ids,
            )
            if inactive_count:
                raise RuntimeError(
                    f"selected term inactive in contract {cell['contract_index']}"
                )
            total += (
                u_half
                * float(u_weight)
                * v_half
                * float(v_weight)
                * x_width
                * energy_width
                * multiplier
                * value
            )
    return total


def plan_is_valid() -> bool:
    if not LEAF_PLAN.exists() or not PLAN_TRACE.exists() or not PLAN_META.exists():
        return False
    try:
        meta = read_json(PLAN_META)
        leaves = read_csv(LEAF_PLAN)
    except Exception:
        return False
    return (
        meta.get("plan_revision") == PLAN_REVISION
        and meta.get("contract_sha256") == digest(CONTRACT_5308)
        and meta.get("parent_discrepancy_sha256") == digest(DISCREPANCY_5309)
        and int(meta.get("leaf_count", -1)) == len(leaves)
        and all(parse_bool(row["leaf_local_gate_passes"]) for row in leaves)
    )


def split_regions(
    u_lower: float,
    u_upper: float,
    v_lower: float,
    v_upper: float,
    split_mode: str,
) -> list[tuple[float, float, float, float, str]]:
    u_midpoint = 0.5 * (u_lower + u_upper)
    v_midpoint = 0.5 * (v_lower + v_upper)
    if split_mode == "SOFT":
        return [
            (u_lower, u_midpoint, v_lower, v_upper, "S0"),
            (u_midpoint, u_upper, v_lower, v_upper, "S1"),
        ]
    if split_mode == "ENERGY":
        return [
            (u_lower, u_upper, v_lower, v_midpoint, "E0"),
            (u_lower, u_upper, v_midpoint, v_upper, "E1"),
        ]
    return [
        (u_lower, u_midpoint, v_lower, v_midpoint, "B00"),
        (u_lower, u_midpoint, v_midpoint, v_upper, "B01"),
        (u_midpoint, u_upper, v_lower, v_midpoint, "B10"),
        (u_midpoint, u_upper, v_midpoint, v_upper, "B11"),
    ]


def build_plan(
    targets: list[dict[str, Any]],
    evaluate: Any,
    multiplier: float,
    global_scale: float,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    contract = contract_lookup()
    trace: list[dict[str, Any]] = []
    leaves: list[dict[str, Any]] = []
    for target_counter, target in enumerate(targets, start=1):
        contract_index = int(target["contract_index"])
        cell = contract[contract_index]
        stack = [(0.0, 1.0, 0.0, 1.0, 0, "R")]
        local_leaf_count = 0
        while stack:
            u_lower, u_upper, v_lower, v_upper, depth, region_id = stack.pop()
            order4 = integrate_region(
                cell,
                PLAN_EPSILON_ID,
                evaluate,
                multiplier,
                u_lower,
                u_upper,
                v_lower,
                v_upper,
                4,
                4,
            )
            order8 = integrate_region(
                cell,
                PLAN_EPSILON_ID,
                evaluate,
                multiplier,
                u_lower,
                u_upper,
                v_lower,
                v_upper,
                8,
                8,
            )
            area = (u_upper - u_lower) * (v_upper - v_lower)
            error = abs(order8 - order4)
            scale = max(abs(order8), global_scale * area, 1.0e-12)
            local_change = error / scale
            local_passes = local_change <= LOCAL_RELATIVE_LIMIT
            split_mode = "LEAF"
            soft_effect = 0.0
            energy_effect = 0.0
            if not local_passes and depth < MAXIMUM_DEPTH:
                soft_high = integrate_region(
                    cell,
                    PLAN_EPSILON_ID,
                    evaluate,
                    multiplier,
                    u_lower,
                    u_upper,
                    v_lower,
                    v_upper,
                    8,
                    4,
                )
                energy_high = integrate_region(
                    cell,
                    PLAN_EPSILON_ID,
                    evaluate,
                    multiplier,
                    u_lower,
                    u_upper,
                    v_lower,
                    v_upper,
                    4,
                    8,
                )
                soft_effect = abs(order8 - energy_high)
                energy_effect = abs(order8 - soft_high)
                largest = max(soft_effect, energy_effect, 1.0e-300)
                if (
                    soft_effect >= 0.3 * largest
                    and energy_effect >= 0.3 * largest
                ):
                    split_mode = "BOTH"
                elif soft_effect >= energy_effect:
                    split_mode = "SOFT"
                else:
                    split_mode = "ENERGY"
            terminal = local_passes or depth >= MAXIMUM_DEPTH
            trace.append(
                {
                    "contract_index": contract_index,
                    "region_id": region_id,
                    "depth": depth,
                    "u_lower": u_lower,
                    "u_upper": u_upper,
                    "v_lower": v_lower,
                    "v_upper": v_upper,
                    "unit_square_area": area,
                    **complex_fields("order4_integral", order4),
                    **complex_fields("order8_integral", order8),
                    "order4_order8_absolute_change": error,
                    "local_normalization_scale": scale,
                    "local_relative_change": local_change,
                    "soft_resolution_effect": soft_effect,
                    "energy_resolution_effect": energy_effect,
                    "split_mode": split_mode,
                    "terminal_leaf": terminal,
                    "local_gate_passes": local_passes,
                    **{field: False for field in CLAIM_FIELDS},
                }
            )
            if terminal:
                local_leaf_count += 1
                if local_leaf_count + len(stack) > MAXIMUM_LEAVES_PER_CELL:
                    raise RuntimeError(
                        f"adaptive leaf bound reached for cell {contract_index}"
                    )
                leaves.append(
                    {
                        "contract_index": contract_index,
                        "region_id": region_id,
                        "depth": depth,
                        "u_lower": u_lower,
                        "u_upper": u_upper,
                        "v_lower": v_lower,
                        "v_upper": v_upper,
                        "unit_square_area": area,
                        **complex_fields("E0025_order4_integral", order4),
                        **complex_fields("E0025_order8_integral", order8),
                        "E0025_local_relative_change": local_change,
                        "leaf_local_gate_passes": local_passes,
                        **{field: False for field in CLAIM_FIELDS},
                    }
                )
            else:
                children = split_regions(
                    u_lower,
                    u_upper,
                    v_lower,
                    v_upper,
                    split_mode,
                )
                if local_leaf_count + len(stack) + len(children) > MAXIMUM_LEAVES_PER_CELL:
                    raise RuntimeError(
                        f"adaptive leaf bound reached for cell {contract_index}"
                    )
                for child in reversed(children):
                    stack.append(
                        (*child[:4], depth + 1, f"{region_id}.{child[4]}")
                    )
        atomic_json(
            STATUS,
            {
                "checkpoint": CHECKPOINT,
                "state": "RUNNING",
                "stage": "E0025_ADAPTIVE_PLAN",
                "completed_target_count": target_counter,
                "planned_target_count": len(targets),
                "latest_contract_index": contract_index,
                "latest_leaf_count": local_leaf_count,
            },
        )
    return trace, leaves


def shard_paths(epsilon_id: str) -> dict[str, Path]:
    root = SHARDS / epsilon_id
    return {
        "root": root,
        "leaves": root / "leaf_integrals.csv",
        "result": root / "result.json",
    }


def shard_is_valid(
    epsilon_id: str, plan_sha256: str, leaf_count: int
) -> bool:
    paths = shard_paths(epsilon_id)
    if not paths["leaves"].exists() or not paths["result"].exists():
        return False
    try:
        result = read_json(paths["result"])
        rows = read_csv(paths["leaves"])
    except Exception:
        return False
    return (
        result.get("shard_revision") == SHARD_REVISION
        and result.get("epsilon_id") == epsilon_id
        and result.get("leaf_plan_sha256") == plan_sha256
        and int(result.get("leaf_count", -1)) == leaf_count
        and len(rows) == leaf_count
    )


def integrate_refined_shard(
    epsilon_id: str,
    epsilon: float,
    leaves: list[dict[str, str]],
    plan_sha256: str,
    evaluate: Any,
    multiplier: float,
) -> dict[str, Any]:
    paths = shard_paths(epsilon_id)
    paths["root"].mkdir(parents=True, exist_ok=True)
    started = time.perf_counter()
    contract = contract_lookup()
    rows: list[dict[str, Any]] = []
    for leaf_counter, leaf in enumerate(leaves, start=1):
        contract_index = int(leaf["contract_index"])
        cell = contract[contract_index]
        values: dict[int, complex] = {}
        for order in LEAF_ORDERS:
            values[order] = integrate_region(
                cell,
                epsilon_id,
                evaluate,
                multiplier,
                float(leaf["u_lower"]),
                float(leaf["u_upper"]),
                float(leaf["v_lower"]),
                float(leaf["v_upper"]),
                order,
                order,
            )
        change = relative_complex_change(values[4], values[8])
        rows.append(
            {
                "contract_index": contract_index,
                "region_id": leaf["region_id"],
                "depth": leaf["depth"],
                "u_lower": leaf["u_lower"],
                "u_upper": leaf["u_upper"],
                "v_lower": leaf["v_lower"],
                "v_upper": leaf["v_upper"],
                "epsilon_id": epsilon_id,
                "epsilon": epsilon,
                **complex_fields("order4_leaf_integral", values[4]),
                **complex_fields("order8_leaf_integral", values[8]),
                "order4_order8_relative_change": change,
                **{field: False for field in CLAIM_FIELDS},
            }
        )
        if leaf_counter % 10 == 0 or leaf_counter == len(leaves):
            atomic_json(
                STATUS,
                {
                    "checkpoint": CHECKPOINT,
                    "state": "RUNNING",
                    "stage": "FIVE_REGULATOR_ADAPTIVE_LEAVES",
                    "epsilon_id": epsilon_id,
                    "completed_leaf_count": leaf_counter,
                    "planned_leaf_count": len(leaves),
                },
            )
    write_csv(paths["leaves"], rows)
    result = {
        "checkpoint": CHECKPOINT,
        "shard_revision": SHARD_REVISION,
        "epsilon_id": epsilon_id,
        "epsilon": epsilon,
        "leaf_plan_sha256": plan_sha256,
        "leaf_count": len(leaves),
        "runtime_seconds": time.perf_counter() - started,
        **{field: False for field in CLAIM_FIELDS},
    }
    atomic_json(paths["result"], result)
    return result


def manifest_rows(plan_sha256: str, leaf_count: int) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for epsilon_id, epsilon in M5303.REGULATORS:
        paths = shard_paths(epsilon_id)
        complete = shard_is_valid(epsilon_id, plan_sha256, leaf_count)
        result = read_json(paths["result"]) if complete else {}
        rows.append(
            {
                "epsilon_id": epsilon_id,
                "epsilon": epsilon,
                "leaf_count": leaf_count,
                "shard_complete": complete,
                "shard_result_path": str(paths["result"]),
                "shard_leaf_rows_path": str(paths["leaves"]),
                "runtime_seconds": result.get("runtime_seconds", ""),
                **{field: False for field in CLAIM_FIELDS},
            }
        )
    return rows


def refined_products(
    manifest: list[dict[str, Any]],
    target_indices: set[int],
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
]:
    parent = read_csv(CELLS_5309)
    leaf_rows = [
        row
        for item in manifest
        if parse_bool(item["shard_complete"])
        for row in read_csv(Path(item["shard_leaf_rows_path"]))
    ]
    target_totals: list[dict[str, Any]] = []
    target_lookup: dict[tuple[str, int, int], complex] = {}
    for epsilon_id, epsilon in M5303.REGULATORS:
        for contract_index in sorted(target_indices):
            local = [
                row for row in leaf_rows
                if row["epsilon_id"] == epsilon_id
                and int(row["contract_index"]) == contract_index
            ]
            for order in LEAF_ORDERS:
                value = sum(
                    (
                        complex(
                            float(row[f"order{order}_leaf_integral_real"]),
                            float(row[f"order{order}_leaf_integral_imaginary"]),
                        )
                        for row in local
                    ),
                    0.0j,
                )
                target_lookup[(epsilon_id, contract_index, order)] = value
                target_totals.append(
                    {
                        "epsilon_id": epsilon_id,
                        "epsilon": epsilon,
                        "contract_index": contract_index,
                        "cubature_order": order,
                        "leaf_count": len(local),
                        **complex_fields("refined_cell_integral", value),
                        **{field: False for field in CLAIM_FIELDS},
                    }
                )
    refined_cells: list[dict[str, Any]] = []
    for row in parent:
        order = int(row["cubature_order"])
        if order not in LEAF_ORDERS:
            continue
        contract_index = int(row["contract_index"])
        if contract_index in target_indices:
            value = target_lookup[(row["epsilon_id"], contract_index, order)]
            source = "ADAPTIVE_LEAF_REPLACEMENT"
        else:
            value = complex(
                float(row["cell_integral_real"]),
                float(row["cell_integral_imaginary"]),
            )
            source = "REUSED_5309_PARENT_CELL"
        refined_cells.append(
            {
                "epsilon_id": row["epsilon_id"],
                "epsilon": row["epsilon"],
                "contract_index": contract_index,
                "cubature_order": order,
                "cell_source": source,
                **complex_fields("cell_integral", value),
                **{field: False for field in CLAIM_FIELDS},
            }
        )
    totals: list[dict[str, Any]] = []
    convergence: list[dict[str, Any]] = []
    for epsilon_id, epsilon in M5303.REGULATORS:
        values: dict[int, complex] = {}
        for order in LEAF_ORDERS:
            values[order] = sum(
                (
                    complex(
                        float(row["cell_integral_real"]),
                        float(row["cell_integral_imaginary"]),
                    )
                    for row in refined_cells
                    if row["epsilon_id"] == epsilon_id
                    and int(row["cubature_order"]) == order
                ),
                0.0j,
            )
            totals.append(
                {
                    "epsilon_id": epsilon_id,
                    "epsilon": epsilon,
                    "cubature_order": order,
                    "quadrature_order": order,
                    **complex_fields("fixed_decay_pair_integral", values[order]),
                    **complex_fields("edge_integral", values[order]),
                    **{field: False for field in CLAIM_FIELDS},
                }
            )
        local_cells = [
            row for row in refined_cells
            if row["epsilon_id"] == epsilon_id
        ]
        local_lookup = {
            (int(row["contract_index"]), int(row["cubature_order"])): complex(
                float(row["cell_integral_real"]),
                float(row["cell_integral_imaginary"]),
            )
            for row in local_cells
        }
        error_budget = sum(
            abs(
                local_lookup[(contract_index, 8)]
                - local_lookup[(contract_index, 4)]
            )
            for contract_index in sorted(
                {int(row["contract_index"]) for row in local_cells}
            )
        ) / max(abs(values[8]), 1.0e-300)
        change = relative_complex_change(values[4], values[8])
        convergence.append(
            {
                "epsilon_id": epsilon_id,
                "epsilon": epsilon,
                **complex_fields("order4_integral", values[4]),
                **complex_fields("order8_integral", values[8]),
                "order4_order8_relative_change": change,
                "summed_cell_error_budget_relative_to_order8": error_budget,
                "passes_refined_fixed_decay_cubature_gate": (
                    change <= GLOBAL_ORDER_CHANGE_LIMIT
                    and error_budget <= CELL_ERROR_BUDGET_LIMIT
                ),
                **{field: False for field in CLAIM_FIELDS},
            }
        )
    return leaf_rows, target_totals, refined_cells, totals, convergence


def source_rows() -> list[dict[str, str]]:
    paths = (
        Path(__file__).resolve(),
        SCRIPT_5309,
        RESULT_5309,
        CONTRACT_5308,
        CELLS_5309,
        DISCREPANCY_5309,
        REDUCTION_5309,
    )
    return [{"path": str(path), "sha256": digest(path)} for path in paths]


def dry_run() -> dict[str, Any]:
    SOURCE.mkdir(parents=True, exist_ok=True)
    parent = read_json(RESULT_5309)
    targets = target_rows()
    reduction = read_csv(REDUCTION_5309)
    checks = {
        "parent_5309_completed_all_shards": (
            int(parent["completed_shard_count"]) == 15
        ),
        "parent_5309_localized_not_claimed": (
            not bool(parent["acceptance_passed"])
            and parent["decision"]
            == "FIXED_DECAY_PAIR_CUBATURE_LOCALIZES_ADAPTIVE_REFINEMENT"
        ),
        "adaptive_targets_are_nonempty_strict_subset": (
            0 < len(targets) < int(parent["contract_cell_count"])
        ),
        "target_error_is_localized": (
            sum(float(row["parent_error_fraction"]) for row in targets)
            >= 0.99 * float(parent["maximum_summed_cell_error_budget"])
        ),
        "pair_reduction_transfer_passes": all(
            parse_bool(row["valid_for_five_regulator_reduction_transfer"])
            for row in reduction
        ),
        "runtime_bound_below_four_hours": (
            MAXIMUM_RUNTIME_SECONDS < 4.0 * 3600.0
        ),
        "formalization_workbench_unchanged": (
            M5283.formal_inventory_digest()
            == parent["formalization_workbench_end_digest"]
        ),
    }
    accepted = all(checks.values())
    result = {
        "checkpoint": CHECKPOINT,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "mode": "dry-run",
        "checks": checks,
        "acceptance_passed": accepted,
        "adaptive_target_count": len(targets),
        "decision": (
            "DRY_RUN_ACCEPTED__BUILD_ANISOTROPIC_LEAF_PLAN"
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
        raise RuntimeError("5310 dry run did not pass")
    targets = target_rows()
    write_csv(TARGETS, targets)
    target_indices = {int(row["contract_index"]) for row in targets}
    parent_cells = read_csv(CELLS_5309)
    global_scale = abs(
        sum(
            (
                complex(
                    float(row["cell_integral_real"]),
                    float(row["cell_integral_imaginary"]),
                )
                for row in parent_cells
                if row["epsilon_id"] == PLAN_EPSILON_ID
                and int(row["cubature_order"]) == 8
            ),
            0.0j,
        )
    )
    context = M5303.synthetic_context()
    evaluate = M5305.component_evaluator(context)
    multiplier = M5309.physical_multiplier()
    if plan_is_valid():
        trace = read_csv(PLAN_TRACE)
        leaves = read_csv(LEAF_PLAN)
    else:
        trace, leaves = build_plan(
            targets, evaluate, multiplier, global_scale
        )
        write_csv(PLAN_TRACE, trace)
        write_csv(LEAF_PLAN, leaves)
        atomic_json(
            PLAN_META,
            {
                "checkpoint": CHECKPOINT,
                "plan_revision": PLAN_REVISION,
                "contract_sha256": digest(CONTRACT_5308),
                "parent_discrepancy_sha256": digest(DISCREPANCY_5309),
                "target_count": len(targets),
                "leaf_count": len(leaves),
                "all_leaf_local_gates_pass": all(
                    parse_bool(row["leaf_local_gate_passes"])
                    for row in leaves
                ),
            },
        )
    if not all(
        parse_bool(row["leaf_local_gate_passes"]) for row in leaves
    ):
        result = {
            "checkpoint": CHECKPOINT,
            "parent_checkpoint": PARENT_CHECKPOINT,
            "mode": "adaptive-plan-requires-deeper-refinement",
            "acceptance_passed": False,
            "decision": "ADAPTIVE_PLAN_REACHES_DEPTH_BOUND__REFINE_POLE_COORDINATES",
            "adaptive_target_count": len(targets),
            "adaptive_leaf_count": len(leaves),
            "formalization_workbench_end_digest": M5283.formal_inventory_digest(),
            "claim_boundary": {field: False for field in CLAIM_FIELDS},
            "runtime_seconds": time.perf_counter() - started,
        }
        atomic_json(RESULT, result)
        return result
    plan_sha256 = digest(LEAF_PLAN)
    runtime_limit_reached = False
    for epsilon_id, epsilon in M5303.REGULATORS:
        if not shard_is_valid(epsilon_id, plan_sha256, len(leaves)):
            integrate_refined_shard(
                epsilon_id,
                epsilon,
                leaves,
                plan_sha256,
                evaluate,
                multiplier,
            )
        if time.perf_counter() - started >= MAXIMUM_RUNTIME_SECONDS:
            runtime_limit_reached = True
            break
    manifest = manifest_rows(plan_sha256, len(leaves))
    write_csv(MANIFEST, manifest)
    complete_count = sum(parse_bool(row["shard_complete"]) for row in manifest)
    formal_end = M5283.formal_inventory_digest()
    if complete_count != len(manifest):
        result = {
            "checkpoint": CHECKPOINT,
            "parent_checkpoint": PARENT_CHECKPOINT,
            "mode": "anisotropic-refinement-partial",
            "acceptance_passed": False,
            "decision": "RUNTIME_BOUND_REACHED__RESUME_ADAPTIVE_SHARDS",
            "completed_shard_count": complete_count,
            "remaining_shard_count": len(manifest) - complete_count,
            "formalization_workbench_end_digest": formal_end,
            "claim_boundary": {field: False for field in CLAIM_FIELDS},
            "runtime_seconds": time.perf_counter() - started,
        }
        atomic_json(RESULT, result)
        return result
    (
        leaf_integrals,
        target_integrals,
        refined_cells,
        totals,
        convergence,
    ) = refined_products(manifest, target_indices)
    limit_rows, estimates = M5303.limit_rows(totals)
    richardson_change = float(
        limit_rows[0]["last_two_richardson_relative_change"]
    )
    model_change = float(
        limit_rows[0]["small_regulator_model_intercept_relative_change"]
    )
    regulator_stable = (
        richardson_change <= M5303.RICHARDSON_LIMIT_CHANGE_LIMIT
        and model_change <= M5303.MODEL_INTERCEPT_CHANGE_LIMIT
    )
    final_estimate = estimates["RICHARDSON_E005_E0025"]
    write_csv(LEAF_INTEGRALS, leaf_integrals)
    write_csv(TARGET_INTEGRALS, target_integrals)
    write_csv(REFINED_CELLS, refined_cells)
    write_csv(REFINED_TOTALS, totals)
    write_csv(CONVERGENCE, convergence)
    write_csv(LIMITS, limit_rows)
    checks = {
        "all_adaptive_leaf_local_gates_pass": all(
            parse_bool(row["leaf_local_gate_passes"]) for row in leaves
        ),
        "all_five_refined_shards_complete": complete_count == 5,
        "all_five_regulators_pass_refined_cubature_gate": all(
            parse_bool(row["passes_refined_fixed_decay_cubature_gate"])
            for row in convergence
        ),
        "refined_regulator_zero_limit_stable": regulator_stable,
        "non_target_parent_cells_reused": sum(
            row["cell_source"] == "REUSED_5309_PARENT_CELL"
            for row in refined_cells
        )
        == 5 * 2 * (32 - len(target_indices)),
        "integration_precision_initialized": (
            mp.mp.dps >= M5280.MP_DECIMAL_DIGITS
        ),
        "formalization_workbench_unchanged": (
            formal_end
            == read_json(RESULT_5309)["formalization_workbench_end_digest"]
        ),
        "claims_locked_false": True,
    }
    accepted = all(checks.values())
    decision = (
        "FIXED_DECAY_PAIR_CUBATURE_ADAPTIVELY_RESOLVED__"
        "DERIVE_DECAY_ANGLE_TOPOLOGY"
        if accepted
        else "ADAPTIVE_REFINEMENT_REQUIRES_POLE_ALIGNED_COORDINATES"
    )
    result = {
        "checkpoint": CHECKPOINT,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "mode": "anisotropic-topology-cell-refinement",
        "checks": checks,
        "acceptance_passed": accepted,
        "decision": decision,
        "adaptive_target_count": len(targets),
        "adaptive_leaf_count": len(leaves),
        "maximum_adaptive_depth": max(int(row["depth"]) for row in leaves),
        "completed_refined_shard_count": complete_count,
        "reused_parent_cell_row_count": sum(
            row["cell_source"] == "REUSED_5309_PARENT_CELL"
            for row in refined_cells
        ),
        "maximum_refined_order4_order8_relative_change": max(
            float(row["order4_order8_relative_change"])
            for row in convergence
        ),
        "maximum_refined_cell_error_budget": max(
            float(row["summed_cell_error_budget_relative_to_order8"])
            for row in convergence
        ),
        "last_two_richardson_relative_change": richardson_change,
        "small_regulator_model_intercept_relative_change": model_change,
        **complex_fields("regulator_zero_estimate", final_estimate),
        "formalization_workbench_reference_digest": read_json(RESULT_5309)[
            "formalization_workbench_end_digest"
        ],
        "formalization_workbench_end_digest": formal_end,
        "formalization_workbench_modified_file_count": (
            0
            if formal_end
            == read_json(RESULT_5309)["formalization_workbench_end_digest"]
            else -1
        ),
        "claim_boundary": {
            "valid_for_fixed_decay_pair_energy_soft_integral": accepted,
            "valid_for_fixed_decay_pair_regulator_zero_limit": accepted,
            **{field: False for field in CLAIM_FIELDS},
            "reason": (
                "The fixed-decay pair sector is controlled, but the "
                "decay-angle topology and outer integral remain."
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
            "state": "COMPLETE" if accepted else "REFINEMENT_REQUIRED",
            "decision": decision,
            "adaptive_leaf_count": len(leaves),
        },
    )
    return result


def validation_gate(gate: str, passed: bool, detail: str) -> dict[str, Any]:
    return {"gate": gate, "passed": bool(passed), "detail": detail}


def claims_are_false(rows: list[dict[str, Any]]) -> bool:
    return all(
        not parse_bool(row[field])
        for row in rows
        for field in CLAIM_FIELDS
        if field in row
    )


def render_document(result: dict[str, Any], passed: bool) -> None:
    parent = read_json(RESULT_5309)
    text = f"""# 5310 — Anisotropic topology-cell refinement

## Question

Checkpoint 5309 found a stable five-regulator limit but failed its spatial
cubature gate.  More than 99% of its order-four/order-eight discrepancy was
localized rather than distributed over the 32 topology cells.  This checkpoint
tests the discrepancy instead of replacing the failed integral by a closure.

## Method

The E0025 regulator selects the cells carrying at least
`{TARGET_ERROR_FRACTION_MINIMUM:.3g}` of the parent order-eight total.  Each
selected unit-square topology cell is recursively bisected in the soft,
energy, or both directions according to mixed `Q8xQ4` and `Q4xQ8` probes.
Every terminal leaf must satisfy a local `Q4xQ4`/`Q8xQ8` relative gate of
`{LOCAL_RELATIVE_LIMIT:.3g}`.  The resulting geometry-only leaf plan is then
reused independently at all five finite regulators.  Non-target cells are
reused exactly from 5309.

- adaptive target cells: `{result['adaptive_target_count']}`;
- terminal adaptive leaves: `{result['adaptive_leaf_count']}`;
- maximum adaptive depth: `{result['maximum_adaptive_depth']}`;
- completed regulator shards: `{result['completed_refined_shard_count']}/5`;
- reused parent cell rows: `{result['reused_parent_cell_row_count']}`;
- parent maximum global Q4/Q8 change:
  `{parent['maximum_order4_order8_relative_change']:.12g}`;
- refined maximum global Q4/Q8 change:
  `{result['maximum_refined_order4_order8_relative_change']:.12g}`;
- parent maximum summed cell-error budget:
  `{parent['maximum_summed_cell_error_budget']:.12g}`;
- refined maximum summed cell-error budget:
  `{result['maximum_refined_cell_error_budget']:.12g}`;
- last-two Richardson change:
  `{result['last_two_richardson_relative_change']:.12g}`;
- small-regulator model-intercept change:
  `{result['small_regulator_model_intercept_relative_change']:.12g}`;
- regulator-zero estimate:
  `{result['regulator_zero_estimate_real']:.12g} `
  `{result['regulator_zero_estimate_imaginary']:+.12g} i`.

Decision: **{result['decision']}**.

Validation: **{'PASS' if passed else 'FAIL'}**.

## Claim boundary

Passing 5310 controls only the energy/soft-angle integral at one fixed absolute
decay cosine.  It does not integrate the decay angle and therefore does not
establish the full angular coefficient, a UV fixed point, local GR, or the full
MTS theory.  Those claims remain explicitly false.
"""
    DOCUMENT.write_text(text, encoding="utf-8")


def validate_outputs() -> dict[str, Any]:
    started = time.perf_counter()
    result = read_json(RESULT)
    targets = read_csv(TARGETS)
    trace = read_csv(PLAN_TRACE)
    leaves = read_csv(LEAF_PLAN)
    plan_meta = read_json(PLAN_META)
    manifest = read_csv(MANIFEST)
    leaf_integrals = read_csv(LEAF_INTEGRALS)
    target_integrals = read_csv(TARGET_INTEGRALS)
    refined_cells = read_csv(REFINED_CELLS)
    totals = read_csv(REFINED_TOTALS)
    convergence = read_csv(CONVERGENCE)
    limits = read_csv(LIMITS)
    target_count = int(result["adaptive_target_count"])
    leaf_count = int(result["adaptive_leaf_count"])
    contract_count = int(read_json(RESULT_5309)["contract_cell_count"])
    plan_sha256 = digest(LEAF_PLAN)
    source_files_current = all(
        Path(row["path"]).exists()
        and digest(Path(row["path"])) == row["sha256"]
        for row in result["source_files"]
    )
    gates = [
        validation_gate(
            "result_pipeline_accepted",
            bool(result["acceptance_passed"]),
            result["decision"],
        ),
        validation_gate(
            "adaptive_targets_are_complete_and_nonclaim",
            len(targets) == target_count
            and 0 < target_count < contract_count
            and all(
                parse_bool(row["valid_for_adaptive_target_selection"])
                for row in targets
            )
            and claims_are_false(targets),
            f"targets={len(targets)}; contracts={contract_count}",
        ),
        validation_gate(
            "adaptive_plan_is_source_current_and_locally_converged",
            int(plan_meta["leaf_count"]) == leaf_count
            and plan_meta["plan_revision"] == PLAN_REVISION
            and plan_meta["contract_sha256"] == digest(CONTRACT_5308)
            and plan_meta["parent_discrepancy_sha256"]
            == digest(DISCREPANCY_5309)
            and len(leaves) == leaf_count
            and len(trace) >= leaf_count
            and all(parse_bool(row["leaf_local_gate_passes"]) for row in leaves)
            and claims_are_false(leaves),
            f"trace={len(trace)}; leaves={len(leaves)}",
        ),
        validation_gate(
            "all_five_refined_shards_complete",
            len(manifest) == 5
            and all(parse_bool(row["shard_complete"]) for row in manifest)
            and all(
                shard_is_valid(row["epsilon_id"], plan_sha256, leaf_count)
                for row in manifest
            ),
            f"rows={len(manifest)}",
        ),
        validation_gate(
            "adaptive_integral_tables_are_complete",
            len(leaf_integrals) == 5 * leaf_count
            and len(target_integrals) == 5 * target_count * len(LEAF_ORDERS)
            and len(refined_cells) == 5 * contract_count * len(LEAF_ORDERS)
            and len(totals) == 5 * len(LEAF_ORDERS)
            and claims_are_false(leaf_integrals)
            and claims_are_false(target_integrals)
            and claims_are_false(refined_cells)
            and claims_are_false(totals),
            (
                f"leaf={len(leaf_integrals)}; target={len(target_integrals)}; "
                f"cells={len(refined_cells)}; totals={len(totals)}"
            ),
        ),
        validation_gate(
            "non_target_parent_cells_reused_exactly",
            sum(
                row["cell_source"] == "REUSED_5309_PARENT_CELL"
                for row in refined_cells
            )
            == 5 * len(LEAF_ORDERS) * (contract_count - target_count),
            f"recorded={result['reused_parent_cell_row_count']}",
        ),
        validation_gate(
            "refined_nested_cubature_converges",
            len(convergence) == 5
            and all(
                parse_bool(row["passes_refined_fixed_decay_cubature_gate"])
                for row in convergence
            )
            and claims_are_false(convergence),
            f"rows={len(convergence)}",
        ),
        validation_gate(
            "refined_regulator_zero_limit_stable",
            len(limits) == 9
            and all(
                parse_bool(row["valid_for_regulator_zero_edge_slice"])
                for row in limits
            ),
            f"rows={len(limits)}",
        ),
        validation_gate(
            "formal_workbench_unchanged",
            M5283.formal_inventory_digest()
            == result["formalization_workbench_end_digest"]
            == result["formalization_workbench_reference_digest"]
            and int(result["formalization_workbench_modified_file_count"]) == 0,
            result["formalization_workbench_end_digest"],
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
            "broader_claims_locked_false",
            all(
                not bool(result["claim_boundary"][field])
                for field in CLAIM_FIELDS
            ),
            "no decay-angle, phase-space, UV, local-GR, or full-MTS claim",
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
            "VALIDATED_ANISOTROPIC_TOPOLOGY_CELL_REFINEMENT"
            if passed
            else "ANISOTROPIC_TOPOLOGY_CELL_REFINEMENT_VALIDATION_FAILED"
        ),
        "runtime_seconds": time.perf_counter() - started,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode", choices=("dry-run", "run", "validate"), required=True
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
