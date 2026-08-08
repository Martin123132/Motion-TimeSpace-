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
SOURCE = FUNCTIONAL_RG / "5309"
SHARDS = SOURCE / "shards"

SCRIPT_5308 = SCRIPTS / "Y5_R2FR_5308_full_fixed_decay_pair_orbit_topology.py"
RESULT_5308 = FUNCTIONAL_RG / "5308" / "full_fixed_decay_pair_topology_result.json"
VALIDATION_5308 = FUNCTIONAL_RG / "5308" / "full_fixed_decay_pair_topology_validation.csv"
CONTRACT_5308 = FUNCTIONAL_RG / "5308" / "fixed_decay_energy_soft_cubature_contract.csv"

DRY_RUN = SOURCE / "fixed_decay_pair_cubature_dry_run.json"
REDUCTION_AUDIT = SOURCE / "five_regulator_pair_reduction_transfer_audit.csv"
MANIFEST = SOURCE / "fixed_decay_pair_cubature_shard_manifest.csv"
CELL_INTEGRALS = SOURCE / "fixed_decay_pair_cubature_cell_integrals.csv"
FINITE_INTEGRALS = SOURCE / "fixed_decay_pair_finite_regulator_integrals.csv"
CONVERGENCE = SOURCE / "fixed_decay_pair_cubature_convergence.csv"
CELL_DISCREPANCY = SOURCE / "fixed_decay_pair_cell_discrepancy.csv"
LIMITS = SOURCE / "fixed_decay_pair_regulator_zero_limits.csv"
RESULT = SOURCE / "fixed_decay_pair_cubature_result.json"
VALIDATION = SOURCE / "fixed_decay_pair_cubature_validation.csv"
RESIDUAL_VALIDATION = RESIDUALS / "P8_Y5_BRR545_5309_VALIDATION.csv"
STATUS = SOURCE / "status.json"
DOCUMENT = POST / "5309-Y5-R2FR-fixed-decay-pair-energy-soft-cubature.md"

CHECKPOINT = 5309
PARENT_CHECKPOINT = 5308
MARKER = "MTS_5309_FIXED_DECAY_PAIR_ENERGY_SOFT_CUBATURE"
REVISION = "fixed-decay-pair-energy-soft-cubature-v1"
SHARD_REVISION = "fixed-decay-pair-energy-soft-cubature-shard-v1"
CUBATURE_ORDERS = (2, 4, 8)
GLOBAL_ORDER_CHANGE_LIMIT = 5.0e-3
CELL_ERROR_BUDGET_LIMIT = 1.0e-2
REDUCTION_TRANSFER_LIMIT = 1.0e-9
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


M5308 = load_module("mts_5308_for_5309", SCRIPT_5308)
M5307 = M5308.M5307
M5305 = M5308.M5305
M5303 = M5308.M5303
M5301 = M5308.M5301
M5280 = M5308.M5280
M5283 = M5308.M5283
np = M5308.np
mp = M5308.mp


def set_below_normal_priority() -> None:
    M5308.set_below_normal_priority()


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
    return M5308.parse_bool(value)


def complex_fields(prefix: str, value: complex) -> dict[str, float]:
    return M5308.complex_fields(prefix, value)


def relative_complex_change(first: complex, second: complex) -> float:
    return M5308.relative_complex_change(first, second)


def term_ids(value: Any) -> tuple[str, ...]:
    return tuple(item for item in str(value).split("|") if item)


def physical_multiplier() -> float:
    return M5301.M5300.M5292.physical_multiplier()


def shard_paths(epsilon_id: str, order: int) -> dict[str, Path]:
    root = SHARDS / epsilon_id / f"Q{order:02d}"
    return {
        "root": root,
        "cells": root / "cell_integrals.csv",
        "result": root / "result.json",
    }


def shard_is_valid(
    epsilon_id: str,
    order: int,
    contract_sha256: str,
    contract_count: int,
) -> bool:
    paths = shard_paths(epsilon_id, order)
    if not paths["cells"].exists() or not paths["result"].exists():
        return False
    try:
        result = read_json(paths["result"])
        rows = read_csv(paths["cells"])
    except Exception:
        return False
    return (
        result.get("shard_revision") == SHARD_REVISION
        and result.get("epsilon_id") == epsilon_id
        and int(result.get("cubature_order", -1)) == order
        and result.get("contract_sha256") == contract_sha256
        and int(result.get("cell_count", -1)) == contract_count
        and len(rows) == contract_count
        and bool(result.get("all_selected_terms_mask_active"))
    )


def evaluate_selected_terms(
    evaluate: Any,
    epsilon_id: str,
    energy: float,
    coordinate: float,
    selected_ids: tuple[str, ...],
) -> tuple[complex, int]:
    total = 0.0j
    inactive_count = 0
    for term_id in selected_ids:
        spec = M5308.SURFACE_LOOKUP[term_id]
        value, active = evaluate(
            epsilon_id,
            energy,
            coordinate,
            spec["component_id"],
            int(spec["soft_sign"]),
            int(spec["decay_sign"]),
        )
        total += value
        inactive_count += int(not active)
    return total, inactive_count


def integrate_shard(
    epsilon_id: str,
    epsilon: float,
    order: int,
    contract: list[dict[str, str]],
    contract_sha256: str,
    evaluate: Any,
    multiplier: float,
) -> dict[str, Any]:
    paths = shard_paths(epsilon_id, order)
    paths["root"].mkdir(parents=True, exist_ok=True)
    started = time.perf_counter()
    nodes, weights = np.polynomial.legendre.leggauss(order)
    total = 0.0j
    inactive_count = 0
    evaluation_count = 0
    rows: list[dict[str, Any]] = []
    for cell_counter, cell in enumerate(contract, start=1):
        x_lower = float(cell["lower_absolute_soft_cosine"])
        x_upper = float(cell["upper_absolute_soft_cosine"])
        x_half = 0.5 * (x_upper - x_lower)
        x_midpoint = 0.5 * (x_upper + x_lower)
        selected_ids = term_ids(cell["evaluation_term_ids"])
        cell_value = 0.0j
        cell_inactive = 0
        for x_node, x_weight in zip(nodes, weights):
            coordinate = x_midpoint + x_half * float(x_node)
            energy_lower = M5308.boundary_energy(
                cell["lower_energy_boundary"], coordinate
            )
            energy_upper = M5308.boundary_energy(
                cell["upper_energy_boundary"], coordinate
            )
            energy_half = 0.5 * (energy_upper - energy_lower)
            energy_midpoint = 0.5 * (energy_upper + energy_lower)
            for energy_node, energy_weight in zip(nodes, weights):
                energy = energy_midpoint + energy_half * float(energy_node)
                value, local_inactive = evaluate_selected_terms(
                    evaluate,
                    epsilon_id,
                    energy,
                    coordinate,
                    selected_ids,
                )
                evaluation_count += len(selected_ids)
                inactive_count += local_inactive
                cell_inactive += local_inactive
                cell_value += (
                    x_half
                    * float(x_weight)
                    * energy_half
                    * float(energy_weight)
                    * multiplier
                    * value
                )
        total += cell_value
        rows.append(
            {
                "contract_index": cell["contract_index"],
                "x_panel_index": cell["x_panel_index"],
                "chamber_index": cell["chamber_index"],
                "epsilon_id": epsilon_id,
                "epsilon": epsilon,
                "cubature_order": order,
                "evaluation_term_ids": cell["evaluation_term_ids"],
                "evaluation_term_count": len(selected_ids),
                "cubature_point_count": order**2,
                "selected_term_evaluation_count": order**2 * len(selected_ids),
                "inactive_selected_term_count": cell_inactive,
                **complex_fields("cell_integral", cell_value),
                **{field: False for field in CLAIM_FIELDS},
            }
        )
        atomic_json(
            STATUS,
            {
                "checkpoint": CHECKPOINT,
                "state": "RUNNING",
                "stage": "FIXED_DECAY_PAIR_CUBATURE_SHARD",
                "epsilon_id": epsilon_id,
                "cubature_order": order,
                "completed_cell_count": cell_counter,
                "planned_cell_count": len(contract),
            },
        )
    write_csv(paths["cells"], rows)
    result = {
        "checkpoint": CHECKPOINT,
        "shard_revision": SHARD_REVISION,
        "epsilon_id": epsilon_id,
        "epsilon": epsilon,
        "cubature_order": order,
        "contract_sha256": contract_sha256,
        "cell_count": len(contract),
        "selected_term_evaluation_count": evaluation_count,
        "inactive_selected_term_count": inactive_count,
        "all_selected_terms_mask_active": inactive_count == 0,
        **complex_fields("fixed_decay_pair_integral", total),
        "runtime_seconds": time.perf_counter() - started,
        **{field: False for field in CLAIM_FIELDS},
    }
    atomic_json(paths["result"], result)
    return result


def reduction_transfer_rows(
    contract: list[dict[str, str]], evaluate: Any
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for cell in contract:
        coordinate = 0.5 * (
            float(cell["lower_absolute_soft_cosine"])
            + float(cell["upper_absolute_soft_cosine"])
        )
        energy_lower = M5308.boundary_energy(
            cell["lower_energy_boundary"], coordinate
        )
        energy_upper = M5308.boundary_energy(
            cell["upper_energy_boundary"], coordinate
        )
        energy = 0.5 * (energy_lower + energy_upper)
        selected_ids = term_ids(cell["evaluation_term_ids"])
        analytic = set(M5308.analytic_active_terms(energy, coordinate))
        for epsilon_id, epsilon in M5303.REGULATORS:
            values, masks = M5308.term_values(
                evaluate, epsilon_id, energy, coordinate
            )
            observed = {
                term_id for term_id, active in masks.items() if active
            }
            full_orbit = sum(values.values(), 0.0j)
            reduced_orbit = sum(
                (values[term_id] for term_id in selected_ids), 0.0j
            )
            cancellation_scale = max(
                sum(abs(value) for value in values.values()), 1.0
            )
            change = abs(full_orbit - reduced_orbit) / cancellation_scale
            rows.append(
                {
                    "contract_index": cell["contract_index"],
                    "x_panel_index": cell["x_panel_index"],
                    "chamber_index": cell["chamber_index"],
                    "epsilon_id": epsilon_id,
                    "epsilon": epsilon,
                    "absolute_soft_cosine": coordinate,
                    "soft_energy": energy,
                    "analytic_active_term_ids": "|".join(sorted(analytic)),
                    "observed_active_term_ids": "|".join(sorted(observed)),
                    "evaluation_term_ids": "|".join(selected_ids),
                    "mask_signature_agrees": analytic == observed,
                    **complex_fields("full_pair_orbit", full_orbit),
                    **complex_fields("reduced_pair_orbit", reduced_orbit),
                    "cancellation_normalization_scale": cancellation_scale,
                    "reduction_relative_change": change,
                    "valid_for_five_regulator_reduction_transfer": (
                        analytic == observed
                        and change <= REDUCTION_TRANSFER_LIMIT
                    ),
                    **{field: False for field in CLAIM_FIELDS},
                }
            )
    return rows


def manifest_rows(
    contract_sha256: str, contract_count: int
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for epsilon_id, epsilon in M5303.REGULATORS:
        for order in CUBATURE_ORDERS:
            paths = shard_paths(epsilon_id, order)
            complete = shard_is_valid(
                epsilon_id, order, contract_sha256, contract_count
            )
            result = read_json(paths["result"]) if complete else {}
            rows.append(
                {
                    "epsilon_id": epsilon_id,
                    "epsilon": epsilon,
                    "cubature_order": order,
                    "cell_count": contract_count,
                    "shard_complete": complete,
                    "shard_result_path": str(paths["result"]),
                    "shard_cell_rows_path": str(paths["cells"]),
                    "selected_term_evaluation_count": result.get(
                        "selected_term_evaluation_count", ""
                    ),
                    "all_selected_terms_mask_active": result.get(
                        "all_selected_terms_mask_active", False
                    ),
                    "runtime_seconds": result.get("runtime_seconds", ""),
                    **{field: False for field in CLAIM_FIELDS},
                }
            )
    return rows


def finite_integral_rows(
    manifest: list[dict[str, Any]]
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for item in manifest:
        if not parse_bool(item["shard_complete"]):
            continue
        result = read_json(Path(item["shard_result_path"]))
        value = complex(
            float(result["fixed_decay_pair_integral_real"]),
            float(result["fixed_decay_pair_integral_imaginary"]),
        )
        rows.append(
            {
                "epsilon_id": item["epsilon_id"],
                "epsilon": item["epsilon"],
                "cubature_order": item["cubature_order"],
                "quadrature_order": item["cubature_order"],
                **complex_fields("fixed_decay_pair_integral", value),
                **complex_fields("edge_integral", value),
                "all_selected_terms_mask_active": result[
                    "all_selected_terms_mask_active"
                ],
                **{field: False for field in CLAIM_FIELDS},
            }
        )
    return rows


def combined_cell_rows(
    manifest: list[dict[str, Any]]
) -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for item in manifest:
        if parse_bool(item["shard_complete"]):
            rows.extend(read_csv(Path(item["shard_cell_rows_path"])))
    return rows


def convergence_products(
    finite: list[dict[str, Any]],
    cells: list[dict[str, str]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    totals = {
        (row["epsilon_id"], int(row["cubature_order"])): complex(
            float(row["fixed_decay_pair_integral_real"]),
            float(row["fixed_decay_pair_integral_imaginary"]),
        )
        for row in finite
    }
    cell_values = {
        (
            row["epsilon_id"],
            int(row["cubature_order"]),
            int(row["contract_index"]),
        ): complex(
            float(row["cell_integral_real"]),
            float(row["cell_integral_imaginary"]),
        )
        for row in cells
    }
    convergence: list[dict[str, Any]] = []
    discrepancy: list[dict[str, Any]] = []
    for epsilon_id, epsilon in M5303.REGULATORS:
        order2 = totals[(epsilon_id, 2)]
        order4 = totals[(epsilon_id, 4)]
        order8 = totals[(epsilon_id, 8)]
        change24 = relative_complex_change(order2, order4)
        change48 = relative_complex_change(order4, order8)
        local_rows: list[dict[str, Any]] = []
        contract_indices = sorted(
            key[2] for key in cell_values
            if key[0] == epsilon_id and key[1] == 8
        )
        for contract_index in contract_indices:
            lower = cell_values[(epsilon_id, 4, contract_index)]
            upper = cell_values[(epsilon_id, 8, contract_index)]
            difference = upper - lower
            local_rows.append(
                {
                    "epsilon_id": epsilon_id,
                    "epsilon": epsilon,
                    "contract_index": contract_index,
                    **complex_fields("order4_cell_integral", lower),
                    **complex_fields("order8_cell_integral", upper),
                    **complex_fields("order8_minus_order4", difference),
                    "cell_relative_change": relative_complex_change(
                        lower, upper
                    ),
                    **{field: False for field in CLAIM_FIELDS},
                }
            )
        error_budget = sum(
            float(row["order8_minus_order4_magnitude"])
            for row in local_rows
        ) / max(abs(order8), 1.0e-300)
        passes = (
            change48 <= GLOBAL_ORDER_CHANGE_LIMIT
            and error_budget <= CELL_ERROR_BUDGET_LIMIT
        )
        for row in local_rows:
            row["absolute_error_fraction_of_order8_total"] = (
                float(row["order8_minus_order4_magnitude"])
                / max(abs(order8), 1.0e-300)
            )
            row["valid_for_cell_discrepancy_localization"] = True
            discrepancy.append(row)
        convergence.append(
            {
                "epsilon_id": epsilon_id,
                "epsilon": epsilon,
                **complex_fields("order2_integral", order2),
                **complex_fields("order4_integral", order4),
                **complex_fields("order8_integral", order8),
                "order2_order4_relative_change": change24,
                "order4_order8_relative_change": change48,
                "summed_cell_error_budget_relative_to_order8": error_budget,
                "passes_fixed_decay_cubature_gate": passes,
                **{field: False for field in CLAIM_FIELDS},
            }
        )
    return convergence, discrepancy


def source_rows() -> list[dict[str, str]]:
    paths = (
        Path(__file__).resolve(),
        SCRIPT_5308,
        RESULT_5308,
        VALIDATION_5308,
        CONTRACT_5308,
    )
    return [{"path": str(path), "sha256": digest(path)} for path in paths]


def dry_run() -> dict[str, Any]:
    SOURCE.mkdir(parents=True, exist_ok=True)
    parent = read_json(RESULT_5308)
    validation = read_csv(VALIDATION_5308)
    contract = read_csv(CONTRACT_5308)
    checks = {
        "parent_5308_accepted": bool(parent["acceptance_passed"]),
        "parent_5308_validation_passes": all(
            parse_bool(row["passed"]) for row in validation
        ),
        "all_contract_cells_topology_safe": (
            len(contract) == int(parent["cubature_contract_row_count"])
            and all(
                parse_bool(
                    row["valid_for_chamber_aligned_cubature_contract"]
                )
                for row in contract
            )
        ),
        "five_regulators_and_three_orders_planned": (
            len(M5303.REGULATORS) == 5 and CUBATURE_ORDERS == (2, 4, 8)
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
        "planned_shard_count": len(M5303.REGULATORS) * len(CUBATURE_ORDERS),
        "decision": (
            "DRY_RUN_ACCEPTED__RUN_FIXED_DECAY_PAIR_CUBATURE"
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
        raise RuntimeError("5309 dry run did not pass")
    contract = read_csv(CONTRACT_5308)
    contract_sha256 = digest(CONTRACT_5308)
    context = M5303.synthetic_context()
    evaluate = M5305.component_evaluator(context)
    reduction = reduction_transfer_rows(contract, evaluate)
    write_csv(REDUCTION_AUDIT, reduction)
    if not all(
        parse_bool(row["valid_for_five_regulator_reduction_transfer"])
        for row in reduction
    ):
        raise RuntimeError("5308 pair reduction did not transfer to all regulators")
    multiplier = physical_multiplier()
    runtime_limit_reached = False
    for epsilon_id, epsilon in M5303.REGULATORS:
        for order in CUBATURE_ORDERS:
            if shard_is_valid(
                epsilon_id, order, contract_sha256, len(contract)
            ):
                continue
            integrate_shard(
                epsilon_id,
                epsilon,
                order,
                contract,
                contract_sha256,
                evaluate,
                multiplier,
            )
            if time.perf_counter() - started >= MAXIMUM_RUNTIME_SECONDS:
                runtime_limit_reached = True
                break
        if runtime_limit_reached:
            break
    manifest = manifest_rows(contract_sha256, len(contract))
    write_csv(MANIFEST, manifest)
    complete_count = sum(parse_bool(row["shard_complete"]) for row in manifest)
    formal_end = M5283.formal_inventory_digest()
    if complete_count != len(manifest):
        result = {
            "checkpoint": CHECKPOINT,
            "parent_checkpoint": PARENT_CHECKPOINT,
            "marker": MARKER,
            "revision": REVISION,
            "mode": "fixed-decay-pair-cubature-partial",
            "acceptance_passed": False,
            "decision": "RUNTIME_BOUND_REACHED__RESUME_FIXED_DECAY_CUBATURE",
            "completed_shard_count": complete_count,
            "remaining_shard_count": len(manifest) - complete_count,
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
                "completed_shard_count": complete_count,
            },
        )
        return result
    finite = finite_integral_rows(manifest)
    cells = combined_cell_rows(manifest)
    convergence, discrepancy = convergence_products(finite, cells)
    limit_rows, estimates = M5303.limit_rows(finite)
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
    write_csv(CELL_INTEGRALS, cells)
    write_csv(FINITE_INTEGRALS, finite)
    write_csv(CONVERGENCE, convergence)
    write_csv(CELL_DISCREPANCY, discrepancy)
    write_csv(LIMITS, limit_rows)
    worst = max(
        discrepancy,
        key=lambda row: float(row["absolute_error_fraction_of_order8_total"]),
    )
    checks = {
        "all_fifteen_shards_complete": complete_count == 15,
        "all_selected_terms_remain_mask_active": all(
            parse_bool(row["all_selected_terms_mask_active"])
            for row in manifest
        ),
        "pair_reduction_transfers_to_all_five_regulators": all(
            parse_bool(row["valid_for_five_regulator_reduction_transfer"])
            for row in reduction
        ),
        "all_five_regulators_pass_nested_cubature_gate": all(
            parse_bool(row["passes_fixed_decay_cubature_gate"])
            for row in convergence
        ),
        "fixed_decay_regulator_zero_limit_stable": regulator_stable,
        "integration_precision_initialized": (
            mp.mp.dps >= M5280.MP_DECIMAL_DIGITS
        ),
        "formalization_workbench_unchanged": (
            formal_end
            == read_json(RESULT_5308)["formalization_workbench_end_digest"]
        ),
        "claims_locked_false": True,
    }
    accepted = all(checks.values())
    decision = (
        "FIXED_DECAY_PAIR_ENERGY_SOFT_CUBATURE_RESOLVED__"
        "MAP_DECAY_ANGLE_TOPOLOGY"
        if accepted
        else "FIXED_DECAY_PAIR_CUBATURE_LOCALIZES_ADAPTIVE_REFINEMENT"
    )
    result = {
        "checkpoint": CHECKPOINT,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "mode": "fixed-decay-pair-energy-soft-cubature",
        "checks": checks,
        "acceptance_passed": accepted,
        "decision": decision,
        "absolute_decay_cosine": M5308.M5302.EDGE_DECAY_ABSOLUTE,
        "completed_shard_count": complete_count,
        "contract_cell_count": len(contract),
        "reduction_transfer_probe_count": len(reduction),
        "finite_integral_row_count": len(finite),
        "cell_integral_row_count": len(cells),
        "maximum_order4_order8_relative_change": max(
            float(row["order4_order8_relative_change"])
            for row in convergence
        ),
        "maximum_summed_cell_error_budget": max(
            float(row["summed_cell_error_budget_relative_to_order8"])
            for row in convergence
        ),
        "last_two_richardson_relative_change": richardson_change,
        "small_regulator_model_intercept_relative_change": model_change,
        **complex_fields("regulator_zero_estimate", final_estimate),
        "worst_cell": worst,
        "formalization_workbench_reference_digest": read_json(RESULT_5308)[
            "formalization_workbench_end_digest"
        ],
        "formalization_workbench_end_digest": formal_end,
        "formalization_workbench_modified_file_count": (
            0
            if formal_end
            == read_json(RESULT_5308)["formalization_workbench_end_digest"]
            else -1
        ),
        "claim_boundary": {
            "valid_for_fixed_decay_pair_energy_soft_integral": accepted,
            "valid_for_fixed_decay_pair_regulator_zero_limit": accepted,
            **{field: False for field in CLAIM_FIELDS},
            "reason": (
                "Only one absolute decay-angle slice is integrated. "
                "The decay-angle topology and outer integral remain."
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
            "completed_shard_count": complete_count,
            "worst_contract_index": worst["contract_index"],
        },
    )
    return result


def validation_gate(gate: str, passed: bool, detail: str) -> dict[str, Any]:
    return {"gate": gate, "passed": bool(passed), "detail": detail}


def render_document(result: dict[str, Any], passed: bool) -> None:
    text = f"""# 5309 — Fixed-decay pair energy–soft cubature

## Calculation

All `32` topology cells from 5308 are integrated directly with tensor
Gauss rules of orders two, four, and eight for each of the five regulators.
The regulator limit is taken only after the finite-regulator energy/soft-angle
volume integrals are assembled.  No interpolation through a mask edge is used.

- completed shards: `{result['completed_shard_count']}/15`;
- finite-integral rows: `{result['finite_integral_row_count']}`;
- cell-integral rows: `{result['cell_integral_row_count']}`;
- maximum order-four/order-eight change:
  `{result['maximum_order4_order8_relative_change']:.12g}`;
- maximum summed cell-error budget:
  `{result['maximum_summed_cell_error_budget']:.12g}`;
- last-two Richardson change:
  `{result['last_two_richardson_relative_change']:.12g}`;
- regulator-model intercept change:
  `{result['small_regulator_model_intercept_relative_change']:.12g}`;
- regulator-zero estimate:
  `{result['regulator_zero_estimate_real']:.12g} `
  `{result['regulator_zero_estimate_imaginary']:+.12g} i`;
- worst cell: contract `{result['worst_cell']['contract_index']}` at
  regulator `{result['worst_cell']['epsilon_id']}`.

Decision: **{result['decision']}**.

Validation: **{'PASS' if passed else 'FAIL'}**.

## Claim boundary

This is a fixed-absolute-decay calculation.  It does not integrate the decay
angle and therefore does not yet establish full angular convergence, a full
phase-space coefficient, local GR, or the full MTS theory.
"""
    DOCUMENT.write_text(text, encoding="utf-8")


def validate_outputs() -> dict[str, Any]:
    started = time.perf_counter()
    result = read_json(RESULT)
    manifest = read_csv(MANIFEST)
    reduction = read_csv(REDUCTION_AUDIT)
    finite = read_csv(FINITE_INTEGRALS)
    cells = read_csv(CELL_INTEGRALS)
    convergence = read_csv(CONVERGENCE)
    discrepancy = read_csv(CELL_DISCREPANCY)
    limits = read_csv(LIMITS)
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
            "all_fifteen_shards_complete",
            len(manifest) == 15
            and all(parse_bool(row["shard_complete"]) for row in manifest),
            f"rows={len(manifest)}",
        ),
        validation_gate(
            "five_regulator_reduction_transfer_passes",
            len(reduction) == int(result["reduction_transfer_probe_count"])
            and all(
                parse_bool(
                    row["valid_for_five_regulator_reduction_transfer"]
                )
                for row in reduction
            ),
            f"rows={len(reduction)}",
        ),
        validation_gate(
            "finite_and_cell_integrals_complete",
            len(finite) == int(result["finite_integral_row_count"])
            and len(cells) == int(result["cell_integral_row_count"])
            and all(
                parse_bool(row["all_selected_terms_mask_active"])
                for row in finite
            ),
            f"finite={len(finite)}; cells={len(cells)}",
        ),
        validation_gate(
            "nested_cubature_converges",
            len(convergence) == 5
            and all(
                parse_bool(row["passes_fixed_decay_cubature_gate"])
                for row in convergence
            ),
            f"rows={len(convergence)}",
        ),
        validation_gate(
            "cell_discrepancy_ledger_complete",
            len(discrepancy) == 5 * int(result["contract_cell_count"])
            and all(
                parse_bool(
                    row["valid_for_cell_discrepancy_localization"]
                )
                for row in discrepancy
            ),
            f"rows={len(discrepancy)}",
        ),
        validation_gate(
            "regulator_zero_limit_stable",
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
            == result["formalization_workbench_end_digest"],
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
            "full_claims_locked_false",
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
            "VALIDATED_FIXED_DECAY_PAIR_ENERGY_SOFT_CUBATURE"
            if passed
            else "FIXED_DECAY_PAIR_CUBATURE_VALIDATION_FAILED"
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
