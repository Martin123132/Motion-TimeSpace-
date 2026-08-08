from __future__ import annotations

import argparse
import cmath
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
SOURCE = FUNCTIONAL_RG / "5312"
SHARDS = SOURCE / "shards"

SCRIPT_5311 = SCRIPTS / "Y5_R2FR_5311_material_pole_aligned_energy_preflight.py"
RESULT_5311 = FUNCTIONAL_RG / "5311" / "material_pole_aligned_energy_preflight_result.json"
CONTRACT_5308 = FUNCTIONAL_RG / "5308" / "fixed_decay_energy_soft_cubature_contract.csv"
RESULT_5289 = FUNCTIONAL_RG / "5289" / "MC04_MC12_angular_pole_result.json"
VALIDATION_5289 = FUNCTIONAL_RG / "5289" / "MC04_MC12_angular_pole_validation.csv"
FINITE_5309 = FUNCTIONAL_RG / "5309" / "fixed_decay_pair_finite_regulator_integrals.csv"

DRY_RUN = SOURCE / "pole_subtracted_outer_soft_integral_dry_run.json"
IDENTITY_AUDIT = SOURCE / "MC04_MC12_pair_identity_audit.csv"
REDUCED_CONTRACT = SOURCE / "reduced_fixed_decay_cubature_contract.csv"
NODE_PLAN = SOURCE / "E0025_outer_soft_node_plan.csv"
NODE_MANIFEST = SOURCE / "E0025_outer_soft_node_manifest.csv"
ALL_POLES = SOURCE / "E0025_outer_soft_geometric_poles.csv"
ALL_FITS = SOURCE / "E0025_outer_soft_pole_residue_fits.csv"
ALL_CLASSIFICATIONS = SOURCE / "E0025_outer_soft_pole_classification.csv"
ALL_CELL_INTEGRALS = SOURCE / "E0025_outer_soft_cell_integrals.csv"
OUTER_TOTALS = SOURCE / "E0025_outer_soft_integrals.csv"
OUTER_PANEL_CONVERGENCE = SOURCE / "E0025_outer_panel_convergence.csv"
RESULT = SOURCE / "pole_subtracted_outer_soft_integral_result.json"
VALIDATION = SOURCE / "pole_subtracted_outer_soft_integral_validation.csv"
RESIDUAL_VALIDATION = RESIDUALS / "P8_Y5_BRR545_5312_VALIDATION.csv"
STATUS = SOURCE / "status.json"
DOCUMENT = POST / "5312-Y5-R2FR-resumable-pole-subtracted-outer-soft-integral.md"

CHECKPOINT = 5312
PARENT_CHECKPOINT = 5311
MARKER = "MTS_5312_RESUMABLE_POLE_SUBTRACTED_OUTER_SOFT_INTEGRAL"
REVISION = "resumable-pole-subtracted-outer-soft-integral-v2"
NODE_REVISION = "E0025-pole-subtracted-outer-soft-node-v1"
EPSILON_ID = "E0025"
EPSILON = 0.0025
IDENTITY_REGULATORS = ("E040", "E0025")
OUTER_ORDERS = (2, 4)
ENERGY_ORDERS = (4, 8)
FIT_BACKGROUND_DEGREE = 4
FIT_RELATIVE_RESIDUAL_LIMIT = 1.0e-4
FIT_RESIDUE_CHANGE_LIMIT = 5.0e-4
MATERIAL_RESIDUE_FLOOR = 1.0e-6
REMOVABLE_RESIDUE_CEILING = 1.0e-8
IDENTITY_RELATIVE_RESIDUAL_LIMIT = 1.0e-9
INNER_RELATIVE_CHANGE_LIMIT = 5.0e-3
INNER_ERROR_BUDGET_LIMIT = 1.0e-2
OUTER_RELATIVE_CHANGE_LIMIT = 5.0e-3
DEFAULT_RUNTIME_LIMIT_SECONDS = 2.75 * 3600.0
EXPECTED_ZERO_CONTRACTS = {1, 5, 6, 10, 13, 15, 17, 20, 24, 26, 28, 30, 32}
CLAIM_FIELDS = (
    "valid_for_full_regulator_zero_limit",
    "valid_for_decay_angle_integration",
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


M5311 = load_module("mts_5311_for_5312", SCRIPT_5311)
M5310 = M5311.M5310
M5309 = M5311.M5309
M5308 = M5311.M5308
M5305 = M5311.M5305
M5303 = M5311.M5303
M5301 = M5311.M5301
M5283 = M5311.M5283
M5280 = M5311.M5280
M5291 = M5311.M5291
np = M5311.np
mp = M5311.mp


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


def write_csv(
    path: Path,
    rows: list[dict[str, Any]],
    fieldnames: list[str] | None = None,
) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    columns = list(fieldnames or [])
    for row in rows:
        for key in row:
            if key not in columns:
                columns.append(key)
    if not columns:
        raise ValueError(f"no columns for {path}")
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=columns)
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
    return M5311.parse_bool(value)


def complex_fields(prefix: str, value: complex) -> dict[str, float]:
    return M5311.complex_fields(prefix, value)


def relative_complex_change(first: complex, second: complex) -> float:
    return M5311.relative_complex_change(first, second)


def term_ids(value: Any) -> tuple[str, ...]:
    return M5309.term_ids(value)


def surface_id(component_id: str, soft_sign: int, decay_sign: int) -> str:
    return (
        f"{component_id}_S{'P' if soft_sign > 0 else 'M'}_"
        f"D{'P' if decay_sign > 0 else 'M'}"
    )


def canonical_mc04_term(term_id: str) -> tuple[str, int]:
    specification = M5308.SURFACE_LOOKUP[term_id]
    soft_sign = int(specification["soft_sign"])
    decay_sign = int(specification["decay_sign"])
    if specification["component_id"] == "MC04":
        return term_id, 1
    return surface_id("MC04", soft_sign, -decay_sign), -1


def reduced_coefficients(active_term_ids: Any) -> dict[str, int]:
    coefficients: dict[str, int] = {}
    for term_id in term_ids(active_term_ids):
        canonical, coefficient = canonical_mc04_term(term_id)
        coefficients[canonical] = coefficients.get(canonical, 0) + coefficient
    return {
        term_id: coefficient
        for term_id, coefficient in sorted(coefficients.items())
        if coefficient
    }


def encode_coefficients(coefficients: dict[str, int]) -> str:
    return "|".join(
        f"{term_id}:{coefficient:+d}"
        for term_id, coefficient in sorted(coefficients.items())
    )


def parse_coefficients(value: Any) -> dict[str, int]:
    coefficients: dict[str, int] = {}
    for item in str(value).split("|"):
        if not item:
            continue
        term_id, coefficient = item.rsplit(":", 1)
        coefficients[term_id] = int(coefficient)
    return coefficients


def build_reduced_contract() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in read_csv(CONTRACT_5308):
        coefficients = reduced_coefficients(source["active_term_ids"])
        contract_index = int(source["contract_index"])
        rows.append(
            {
                "contract_index": contract_index,
                "x_panel_index": int(source["x_panel_index"]),
                "chamber_index": int(source["chamber_index"]),
                "lower_absolute_soft_cosine": source[
                    "lower_absolute_soft_cosine"
                ],
                "upper_absolute_soft_cosine": source[
                    "upper_absolute_soft_cosine"
                ],
                "lower_energy_boundary": source["lower_energy_boundary"],
                "upper_energy_boundary": source["upper_energy_boundary"],
                "original_active_term_ids": source["active_term_ids"],
                "parent_evaluation_term_ids": source["evaluation_term_ids"],
                "reduced_MC04_coefficients": encode_coefficients(coefficients),
                "reduced_MC04_term_ids": "|".join(coefficients),
                "reduced_MC04_term_count": len(coefficients),
                "algebraically_zero_cell": not coefficients,
                "zero_cell_matches_expected_inventory": (
                    (contract_index in EXPECTED_ZERO_CONTRACTS)
                    == (not coefficients)
                ),
                "valid_for_MC04_MC12_identity_reduction": True,
                **{field: False for field in CLAIM_FIELDS},
            }
        )
    return rows


def build_node_plan(contract: list[dict[str, Any]]) -> list[dict[str, Any]]:
    panels: dict[int, dict[str, Any]] = {}
    for row in contract:
        panel_index = int(row["x_panel_index"])
        panels.setdefault(
            panel_index,
            {
                "lower": float(row["lower_absolute_soft_cosine"]),
                "upper": float(row["upper_absolute_soft_cosine"]),
                "contracts": [],
            },
        )
        if int(row["reduced_MC04_term_count"]) > 0:
            panels[panel_index]["contracts"].append(int(row["contract_index"]))
    rows: list[dict[str, Any]] = []
    for outer_order in OUTER_ORDERS:
        nodes, weights = np.polynomial.legendre.leggauss(outer_order)
        for panel_index, panel in sorted(panels.items()):
            lower = float(panel["lower"])
            upper = float(panel["upper"])
            half = 0.5 * (upper - lower)
            midpoint = 0.5 * (upper + lower)
            for local_index, (node, weight) in enumerate(
                zip(nodes, weights), start=1
            ):
                coordinate = midpoint + half * float(node)
                rows.append(
                    {
                        "node_id": (
                            f"P{panel_index:02d}_Q{outer_order:02d}_"
                            f"N{local_index:02d}"
                        ),
                        "x_panel_index": panel_index,
                        "outer_order": outer_order,
                        "local_node_index": local_index,
                        "lower_absolute_soft_cosine": lower,
                        "upper_absolute_soft_cosine": upper,
                        "absolute_soft_cosine": coordinate,
                        "mapped_outer_weight": half * float(weight),
                        "active_nonzero_contract_indices": "|".join(
                            str(value) for value in panel["contracts"]
                        ),
                        "valid_for_resumable_outer_soft_node": bool(
                            panel["contracts"]
                        ),
                        **{field: False for field in CLAIM_FIELDS},
                    }
                )
    return rows


def source_rows() -> list[dict[str, str]]:
    paths = (
        Path(__file__).resolve(),
        SCRIPT_5311,
        RESULT_5311,
        CONTRACT_5308,
        RESULT_5289,
        VALIDATION_5289,
        FINITE_5309,
    )
    return [{"path": str(path), "sha256": digest(path)} for path in paths]


def dry_run() -> dict[str, Any]:
    SOURCE.mkdir(parents=True, exist_ok=True)
    parent = read_json(RESULT_5311)
    antisymmetry = read_json(RESULT_5289)
    contract = build_reduced_contract()
    plan = build_node_plan(contract)
    write_csv(REDUCED_CONTRACT, contract)
    write_csv(NODE_PLAN, plan)
    zero_contracts = {
        int(row["contract_index"])
        for row in contract
        if bool(row["algebraically_zero_cell"])
    }
    checks = {
        "parent_5311_accepts_material_pole_subtraction_route": (
            bool(parent["acceptance_passed"])
            and parent["decision"]
            == (
                "MATERIAL_POLE_CAUSE_PROVED_AND_SUBTRACTION_PREFLIGHT_"
                "PASSES__BUILD_RESUMABLE_OUTER_SOFT_INTEGRAL"
            )
        ),
        "parent_5289_certifies_MC04_MC12_antisymmetry": (
            bool(antisymmetry["acceptance_passed"])
            and bool(antisymmetry["checks"]["MC04_MC12_antisymmetry_certified"])
            and float(antisymmetry["maximum_antisymmetry_relative_residual"])
            <= IDENTITY_RELATIVE_RESIDUAL_LIMIT
        ),
        "all_32_topology_contracts_reduce_algebraically": (
            len(contract) == 32
            and all(
                bool(row["zero_cell_matches_expected_inventory"])
                for row in contract
            )
        ),
        "thirteen_zero_and_nineteen_nonzero_cells": (
            zero_contracts == EXPECTED_ZERO_CONTRACTS
            and sum(
                int(row["reduced_MC04_term_count"]) > 0 for row in contract
            )
            == 19
        ),
        "nine_panels_have_Q2_Q4_resumable_nodes": (
            len(plan) == 54
            and {int(row["x_panel_index"]) for row in plan} == set(range(1, 10))
            and {int(row["outer_order"]) for row in plan} == set(OUTER_ORDERS)
            and all(bool(row["valid_for_resumable_outer_soft_node"]) for row in plan)
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
        "reduced_contract_sha256": digest(REDUCED_CONTRACT),
        "node_plan_sha256": digest(NODE_PLAN),
        "node_count": len(plan),
        "zero_contract_count": len(zero_contracts),
        "nonzero_contract_count": len(contract) - len(zero_contracts),
        "decision": (
            "DRY_RUN_ACCEPTED__RUN_RESUMABLE_POLE_SUBTRACTED_OUTER_SOFT_INTEGRAL"
            if accepted
            else "DRY_RUN_REQUIRES_REPAIR"
        ),
        "runtime_seconds": 0.0,
        **{field: False for field in CLAIM_FIELDS},
    }
    atomic_json(DRY_RUN, result)
    return result


def identity_audit_rows(
    contract: list[dict[str, Any]], evaluate: Any
) -> list[dict[str, Any]]:
    available_regulators = dict(M5303.REGULATORS)
    rows: list[dict[str, Any]] = []
    for cell in contract:
        coordinate = 0.5 * (
            float(cell["lower_absolute_soft_cosine"])
            + float(cell["upper_absolute_soft_cosine"])
        )
        energy_lower = M5308.boundary_energy(
            str(cell["lower_energy_boundary"]), coordinate
        )
        energy_upper = M5308.boundary_energy(
            str(cell["upper_energy_boundary"]), coordinate
        )
        energy = 0.5 * (energy_lower + energy_upper)
        coefficients = parse_coefficients(cell["reduced_MC04_coefficients"])
        active_terms = set(term_ids(cell["original_active_term_ids"]))
        for epsilon_id in IDENTITY_REGULATORS:
            if epsilon_id not in available_regulators:
                raise RuntimeError(f"missing regulator {epsilon_id}")
            values, masks = M5308.term_values(
                evaluate, epsilon_id, energy, coordinate
            )
            full_orbit = sum(values.values(), 0.0j)
            reduced_orbit = sum(
                (
                    coefficient * values[term_id]
                    for term_id, coefficient in coefficients.items()
                ),
                0.0j,
            )
            orbit_scale = max(sum(abs(value) for value in values.values()), 1.0)
            orbit_residual = abs(full_orbit - reduced_orbit) / orbit_scale
            for soft_sign in (-1, 1):
                for decay_sign in (-1, 1):
                    mc12_id = surface_id("MC12", soft_sign, decay_sign)
                    mc04_id = surface_id("MC04", soft_sign, -decay_sign)
                    identity_scale = max(
                        abs(values[mc12_id]) + abs(values[mc04_id]), 1.0
                    )
                    identity_residual = abs(
                        values[mc12_id] + values[mc04_id]
                    ) / identity_scale
                    identity_applied = mc12_id in active_terms
                    mapped_term_active = mc04_id in active_terms
                    applied_identity_passes = (
                        mapped_term_active
                        and masks[mc12_id]
                        and masks[mc04_id]
                        and identity_residual
                        <= IDENTITY_RELATIVE_RESIDUAL_LIMIT
                    )
                    rows.append(
                        {
                            "contract_index": cell["contract_index"],
                            "x_panel_index": cell["x_panel_index"],
                            "epsilon_id": epsilon_id,
                            "epsilon": available_regulators[epsilon_id],
                            "absolute_soft_cosine": coordinate,
                            "soft_energy": energy,
                            "MC12_term_id": mc12_id,
                            "mapped_MC04_term_id": mc04_id,
                            **complex_fields("MC12_value", values[mc12_id]),
                            **complex_fields("mapped_MC04_value", values[mc04_id]),
                            "identity_reduction_applied": identity_applied,
                            "mapped_MC04_active_in_contract": mapped_term_active,
                            "mask_identity_agrees": masks[mc12_id] == masks[mc04_id],
                            "pair_antisymmetry_relative_residual": identity_residual,
                            **complex_fields("full_pair_orbit", full_orbit),
                            **complex_fields("reduced_MC04_orbit", reduced_orbit),
                            "orbit_reduction_relative_residual": orbit_residual,
                            "valid_for_MC04_MC12_identity_transfer": (
                                orbit_residual
                                <= IDENTITY_RELATIVE_RESIDUAL_LIMIT
                                and (
                                    not identity_applied
                                    or applied_identity_passes
                                )
                            ),
                            **{field: False for field in CLAIM_FIELDS},
                        }
                    )
    return rows


def cell_geometry(
    cell: dict[str, Any], coordinate: float
) -> dict[str, Any]:
    lower = M5308.boundary_energy(
        str(cell["lower_energy_boundary"]), coordinate
    )
    upper = M5308.boundary_energy(
        str(cell["upper_energy_boundary"]), coordinate
    )
    if upper <= lower:
        raise RuntimeError(
            f"contract {cell['contract_index']} reversed at |s|={coordinate}"
        )
    return {
        **cell,
        "energy_lower": lower,
        "energy_upper": upper,
        "coefficients": parse_coefficients(cell["reduced_MC04_coefficients"]),
    }


def merged_term_supports(
    cells: list[dict[str, Any]],
) -> dict[str, list[dict[str, Any]]]:
    segments: dict[str, list[dict[str, Any]]] = {}
    for cell in cells:
        for term_id in cell["coefficients"]:
            segments.setdefault(term_id, []).append(
                {
                    "lower": float(cell["energy_lower"]),
                    "upper": float(cell["energy_upper"]),
                    "contracts": [int(cell["contract_index"])],
                }
            )
    merged: dict[str, list[dict[str, Any]]] = {}
    for term_id, local_segments in segments.items():
        result: list[dict[str, Any]] = []
        for segment in sorted(local_segments, key=lambda row: row["lower"]):
            if result and segment["lower"] <= result[-1]["upper"] + 2.0e-10:
                result[-1]["upper"] = max(result[-1]["upper"], segment["upper"])
                result[-1]["contracts"].extend(segment["contracts"])
            else:
                result.append(dict(segment))
        for support_index, support in enumerate(result, start=1):
            support["support_id"] = f"{term_id}_S{support_index:02d}"
            support["contracts"] = sorted(set(support["contracts"]))
        merged[term_id] = result
    return merged


def locate_support(
    supports: list[dict[str, Any]], pole_real: float
) -> dict[str, Any] | None:
    for support in supports:
        if support["lower"] - 1.0e-12 <= pole_real <= support["upper"] + 1.0e-12:
            return support
    return None


def scan_term_poles(
    node: dict[str, Any],
    term_id: str,
    supports: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    specification = M5308.SURFACE_LOOKUP[term_id]
    coordinate = float(node["absolute_soft_cosine"])
    problem = M5311.synthetic_energy_problem(
        "MC04",
        int(specification["soft_sign"]) * coordinate,
        int(specification["decay_sign"]) * M5308.M5302.EDGE_DECAY_ABSOLUTE,
    )
    _, _, poles, _ = M5291.M5267.M5239.scan_problem(problem)
    rows: list[dict[str, Any]] = []
    for pole in poles:
        pole_real = float(pole["pole_real"])
        support = locate_support(supports, pole_real)
        rows.append(
            {
                "node_id": node["node_id"],
                "x_panel_index": node["x_panel_index"],
                "outer_order": node["outer_order"],
                "absolute_soft_cosine": coordinate,
                "term_id": term_id,
                "component_id": "MC04",
                "soft_sign": specification["soft_sign"],
                "decay_sign": specification["decay_sign"],
                "epsilon_id": EPSILON_ID,
                "epsilon": EPSILON,
                "pole_id": pole["pole_id"],
                "primary_surface_id": pole["primary_surface_id"],
                "real_axis_center": float(pole["real_axis_center"]),
                "pole_real": pole_real,
                "pole_imaginary": float(pole["pole_imaginary"]),
                "inside_reduced_term_support": support is not None,
                "support_id": support["support_id"] if support else "",
                "support_energy_lower": support["lower"] if support else "",
                "support_energy_upper": support["upper"] if support else "",
                "support_contract_indices": (
                    "|".join(str(value) for value in support["contracts"])
                    if support
                    else ""
                ),
                "valid_for_E0025_outer_soft_geometric_pole": support is not None,
                **{field: False for field in CLAIM_FIELDS},
            }
        )
    return rows


def fit_node_poles(
    node: dict[str, Any],
    poles: list[dict[str, Any]],
    evaluate: Any,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    fit_rows: list[dict[str, Any]] = []
    classifications: list[dict[str, Any]] = []
    active_poles = [row for row in poles if bool(row["inside_reduced_term_support"])]
    for row in active_poles:
        center = float(row["real_axis_center"])
        pole = complex(float(row["pole_real"]), float(row["pole_imaginary"]))
        lower = float(row["support_energy_lower"])
        upper = float(row["support_energy_upper"])
        separations = [
            abs(center - float(other["real_axis_center"]))
            for other in active_poles
            if other is not row
            and other["term_id"] == row["term_id"]
            and other["support_id"] == row["support_id"]
        ]
        margin = min(center - lower, upper - center, *(separations or [1.0]))
        residues: list[complex] = []
        residuals: list[float] = []
        all_samples_active = True
        failure_reason = ""
        if margin <= 0.0:
            failure_reason = "NONPOSITIVE_SUPPORT_MARGIN"
        else:
            base_radius = min(
                max(8.0 * abs(pole.imag), 2.0e-6),
                margin / 10.0,
            )
            specification = M5308.SURFACE_LOOKUP[str(row["term_id"])]
            for fit_scale in (1.0, 2.0):
                radius = fit_scale * base_radius
                offsets = (
                    -4.0 * radius,
                    -2.0 * radius,
                    -radius,
                    -0.5 * radius,
                    0.5 * radius,
                    radius,
                    2.0 * radius,
                    4.0 * radius,
                )
                matrix_rows: list[list[complex]] = []
                values: list[complex] = []
                local_active = True
                for offset in offsets:
                    energy = center + offset
                    value, active = evaluate(
                        EPSILON_ID,
                        energy,
                        float(node["absolute_soft_cosine"]),
                        "MC04",
                        int(specification["soft_sign"]),
                        int(specification["decay_sign"]),
                    )
                    local_active = local_active and active
                    delta = energy - center
                    matrix_rows.append(
                        [
                            1.0 / (energy - pole),
                            *[
                                complex(delta**power)
                                for power in range(FIT_BACKGROUND_DEGREE + 1)
                            ],
                        ]
                    )
                    values.append(value)
                matrix = np.asarray(matrix_rows, dtype=np.complex128)
                vector = np.asarray(values, dtype=np.complex128)
                coefficients, _, _, _ = np.linalg.lstsq(matrix, vector, rcond=None)
                predicted = matrix @ coefficients
                residual = float(
                    np.linalg.norm(predicted - vector)
                    / max(np.linalg.norm(vector), 1.0)
                )
                residue = complex(coefficients[0])
                residues.append(residue)
                residuals.append(residual)
                all_samples_active = all_samples_active and local_active
                fit_rows.append(
                    {
                        "node_id": node["node_id"],
                        "term_id": row["term_id"],
                        "support_id": row["support_id"],
                        "pole_id": row["pole_id"],
                        "fit_scale": fit_scale,
                        "fit_radius": radius,
                        "fit_sample_count": len(offsets),
                        "background_polynomial_degree": FIT_BACKGROUND_DEGREE,
                        **complex_fields("fitted_residue", residue),
                        "fit_relative_residual": residual,
                        "all_fit_samples_mask_active": local_active,
                        **{field: False for field in CLAIM_FIELDS},
                    }
                )
        if residues:
            residue_change = relative_complex_change(residues[0], residues[1])
            material = (
                all_samples_active
                and min(abs(value) for value in residues) >= MATERIAL_RESIDUE_FLOOR
                and max(residuals) <= FIT_RELATIVE_RESIDUAL_LIMIT
                and residue_change <= FIT_RESIDUE_CHANGE_LIMIT
            )
            removable = (
                all_samples_active
                and max(abs(value) for value in residues)
                <= REMOVABLE_RESIDUE_CEILING
            )
            selected_residue = residues[-1]
            maximum_residual = max(residuals)
        else:
            residue_change = math.inf
            material = False
            removable = False
            selected_residue = 0.0j
            maximum_residual = math.inf
        resolved = material or removable
        if not failure_reason and not resolved:
            failure_reason = "RESIDUE_CLASSIFICATION_GATE_FAILED"
        classifications.append(
            {
                "node_id": node["node_id"],
                "x_panel_index": node["x_panel_index"],
                "outer_order": node["outer_order"],
                "absolute_soft_cosine": node["absolute_soft_cosine"],
                "term_id": row["term_id"],
                "support_id": row["support_id"],
                "pole_id": row["pole_id"],
                "pole_real": row["pole_real"],
                "pole_imaginary": row["pole_imaginary"],
                **complex_fields("selected_residue", selected_residue),
                "maximum_fit_relative_residual": maximum_residual,
                "fit_residue_relative_change": residue_change,
                "all_fit_samples_mask_active": all_samples_active,
                "material_simple_pole": material,
                "removable_zero_residue_pole": removable,
                "pole_classification_resolved": resolved,
                "failure_reason": failure_reason,
                "valid_for_pole_subtracted_outer_soft_node": resolved,
                **{field: False for field in CLAIM_FIELDS},
            }
        )
    return fit_rows, classifications


def support_for_cell_term(
    supports: dict[str, list[dict[str, Any]]],
    term_id: str,
    cell: dict[str, Any],
) -> dict[str, Any]:
    midpoint = 0.5 * (
        float(cell["energy_lower"]) + float(cell["energy_upper"])
    )
    support = locate_support(supports[term_id], midpoint)
    if support is None:
        raise RuntimeError(
            f"no support for {term_id} in contract {cell['contract_index']}"
        )
    return support


def energy_panel_rows(
    node: dict[str, Any],
    cell: dict[str, Any],
    supports: dict[str, list[dict[str, Any]]],
    classifications: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    lower = float(cell["energy_lower"])
    upper = float(cell["energy_upper"])
    points = {lower, upper}
    points.update(lower + index * (upper - lower) / 16.0 for index in range(17))
    for term_id in cell["coefficients"]:
        support = support_for_cell_term(supports, term_id, cell)
        for row in classifications:
            if row["term_id"] != term_id or row["support_id"] != support["support_id"]:
                continue
            center = float(row["pole_real"])
            if not lower - 1.0e-12 <= center <= upper + 1.0e-12:
                continue
            core = max(abs(float(row["pole_imaginary"])), 1.0e-7)
            for scale in (0.0, 1.0, 2.0, 4.0, 8.0, 16.0, 32.0, 64.0):
                points.add(max(lower, min(upper, center - scale * core)))
                points.add(max(lower, min(upper, center + scale * core)))
    coordinates = sorted(points)
    rows: list[dict[str, Any]] = []
    for panel_index, (left, right) in enumerate(
        zip(coordinates[:-1], coordinates[1:]), start=1
    ):
        if right - left <= 1.0e-15:
            continue
        rows.append(
            {
                "node_id": node["node_id"],
                "contract_index": cell["contract_index"],
                "energy_panel_index": panel_index,
                "energy_lower": left,
                "energy_upper": right,
                "panel_width": right - left,
            }
        )
    return rows


def integrate_node_cells(
    node: dict[str, Any],
    cells: list[dict[str, Any]],
    supports: dict[str, list[dict[str, Any]]],
    classifications: list[dict[str, Any]],
    evaluate: Any,
    multiplier: float,
) -> tuple[list[dict[str, Any]], dict[int, complex], int]:
    coordinate = float(node["absolute_soft_cosine"])
    material_lookup: dict[tuple[str, str], list[dict[str, Any]]] = {}
    for row in classifications:
        if bool(row["material_simple_pole"]):
            material_lookup.setdefault(
                (str(row["term_id"]), str(row["support_id"])), []
            ).append(row)
    integral_rows: list[dict[str, Any]] = []
    node_totals = {order: 0.0j for order in ENERGY_ORDERS}
    inactive_count = 0
    for cell in cells:
        panels = energy_panel_rows(node, cell, supports, classifications)
        local_material: list[tuple[int, dict[str, Any]]] = []
        for term_id, coefficient in cell["coefficients"].items():
            support = support_for_cell_term(supports, term_id, cell)
            for row in material_lookup.get((term_id, support["support_id"]), []):
                local_material.append((coefficient, row))
        analytic = sum(
            (
                coefficient
                * complex(
                    float(row["selected_residue_real"]),
                    float(row["selected_residue_imaginary"]),
                )
                * (
                    cmath.log(
                        float(cell["energy_upper"])
                        - complex(float(row["pole_real"]), float(row["pole_imaginary"]))
                    )
                    - cmath.log(
                        float(cell["energy_lower"])
                        - complex(float(row["pole_real"]), float(row["pole_imaginary"]))
                    )
                )
                for coefficient, row in local_material
            ),
            0.0j,
        )

        def raw_value(energy: float) -> complex:
            nonlocal inactive_count
            total = 0.0j
            for term_id, coefficient in cell["coefficients"].items():
                specification = M5308.SURFACE_LOOKUP[term_id]
                value, active = evaluate(
                    EPSILON_ID,
                    energy,
                    coordinate,
                    "MC04",
                    int(specification["soft_sign"]),
                    int(specification["decay_sign"]),
                )
                inactive_count += int(not active)
                total += coefficient * value
            return total

        def singular_value(energy: float) -> complex:
            return sum(
                (
                    coefficient
                    * complex(
                        float(row["selected_residue_real"]),
                        float(row["selected_residue_imaginary"]),
                    )
                    / (
                        energy
                        - complex(
                            float(row["pole_real"]),
                            float(row["pole_imaginary"]),
                        )
                    )
                    for coefficient, row in local_material
                ),
                0.0j,
            )

        for order in ENERGY_ORDERS:
            nodes, weights = np.polynomial.legendre.leggauss(order)
            lower = float(cell["energy_lower"])
            upper = float(cell["energy_upper"])
            half = 0.5 * (upper - lower)
            midpoint = 0.5 * (upper + lower)
            direct = sum(
                (
                    half
                    * float(weight)
                    * raw_value(midpoint + half * float(local_node))
                    for local_node, weight in zip(nodes, weights)
                ),
                0.0j,
            )
            regular = 0.0j
            for panel in panels:
                panel_lower = float(panel["energy_lower"])
                panel_upper = float(panel["energy_upper"])
                panel_half = 0.5 * (panel_upper - panel_lower)
                panel_midpoint = 0.5 * (panel_upper + panel_lower)
                for local_node, weight in zip(nodes, weights):
                    energy = panel_midpoint + panel_half * float(local_node)
                    regular += (
                        panel_half
                        * float(weight)
                        * (raw_value(energy) - singular_value(energy))
                    )
            corrected = multiplier * (regular + analytic)
            node_totals[order] += corrected
            integral_rows.append(
                {
                    "node_id": node["node_id"],
                    "x_panel_index": node["x_panel_index"],
                    "outer_order": node["outer_order"],
                    "absolute_soft_cosine": coordinate,
                    "contract_index": cell["contract_index"],
                    "energy_order": order,
                    "energy_panel_count": len(panels),
                    "reduced_MC04_coefficients": cell[
                        "reduced_MC04_coefficients"
                    ],
                    "material_pole_count": len(local_material),
                    **complex_fields("unpanelled_direct_integral", multiplier * direct),
                    **complex_fields("regularized_numeric_integral", multiplier * regular),
                    **complex_fields("analytic_pole_integral", multiplier * analytic),
                    **complex_fields("pole_corrected_integral", corrected),
                    **{field: False for field in CLAIM_FIELDS},
                }
            )
    by_cell: dict[int, dict[int, complex]] = {}
    for row in integral_rows:
        by_cell.setdefault(int(row["contract_index"]), {})[
            int(row["energy_order"])
        ] = complex(
            float(row["pole_corrected_integral_real"]),
            float(row["pole_corrected_integral_imaginary"]),
        )
    node_change = relative_complex_change(
        node_totals[ENERGY_ORDERS[0]], node_totals[ENERGY_ORDERS[1]]
    )
    node_error = sum(
        abs(values[ENERGY_ORDERS[1]] - values[ENERGY_ORDERS[0]])
        for values in by_cell.values()
    )
    node_error_relative = node_error / max(abs(node_totals[ENERGY_ORDERS[1]]), 1.0e-12)
    for row in integral_rows:
        values = by_cell[int(row["contract_index"])]
        row["cell_Q4_Q8_relative_change"] = relative_complex_change(
            values[ENERGY_ORDERS[0]], values[ENERGY_ORDERS[1]]
        )
        row["node_Q4_Q8_relative_change"] = node_change
        row["node_energy_error_budget_relative"] = node_error_relative
    return integral_rows, node_totals, inactive_count


def shard_paths(node_id: str) -> dict[str, Path]:
    root = SHARDS / node_id
    return {
        "root": root,
        "poles": root / "geometric_poles.csv",
        "fits": root / "pole_residue_fits.csv",
        "classifications": root / "pole_classification.csv",
        "integrals": root / "cell_integrals.csv",
        "result": root / "result.json",
    }


def shard_is_complete(node: dict[str, Any], plan_sha256: str) -> bool:
    paths = shard_paths(str(node["node_id"]))
    if not all(path.exists() for key, path in paths.items() if key != "root"):
        return False
    try:
        result = read_json(paths["result"])
        read_csv(paths["poles"])
        read_csv(paths["fits"])
        read_csv(paths["classifications"])
        read_csv(paths["integrals"])
    except Exception:
        return False
    return (
        result.get("node_revision") == NODE_REVISION
        and result.get("node_id") == node["node_id"]
        and result.get("node_plan_sha256") == plan_sha256
        and bool(result.get("node_complete"))
    )


def run_node(
    node: dict[str, Any],
    contract: list[dict[str, Any]],
    plan_sha256: str,
    base_context: dict[str, Any],
    multiplier: float,
) -> dict[str, Any]:
    started = time.perf_counter()
    paths = shard_paths(str(node["node_id"]))
    paths["root"].mkdir(parents=True, exist_ok=True)
    coordinate = float(node["absolute_soft_cosine"])
    panel_index = int(node["x_panel_index"])
    cells = [
        cell_geometry(row, coordinate)
        for row in contract
        if int(row["x_panel_index"]) == panel_index
        and int(row["reduced_MC04_term_count"]) > 0
    ]
    supports = merged_term_supports(cells)
    poles: list[dict[str, Any]] = []
    for term_id, local_supports in sorted(supports.items()):
        poles.extend(scan_term_poles(node, term_id, local_supports))
    evaluate = M5305.component_evaluator(base_context)
    fits, classifications = fit_node_poles(node, poles, evaluate)
    unresolved = [
        row for row in classifications
        if not bool(row["pole_classification_resolved"])
    ]
    if unresolved:
        integrals: list[dict[str, Any]] = []
        node_totals = {order: 0.0j for order in ENERGY_ORDERS}
        inactive_count = 0
    else:
        integrals, node_totals, inactive_count = integrate_node_cells(
            node,
            cells,
            supports,
            classifications,
            evaluate,
            multiplier,
        )
    node_change = relative_complex_change(
        node_totals[ENERGY_ORDERS[0]], node_totals[ENERGY_ORDERS[1]]
    )
    q4_rows = [row for row in integrals if int(row["energy_order"]) == 4]
    q8_rows = [row for row in integrals if int(row["energy_order"]) == 8]
    error_budget = sum(
        abs(
            complex(
                float(q8["pole_corrected_integral_real"]),
                float(q8["pole_corrected_integral_imaginary"]),
            )
            - complex(
                float(q4["pole_corrected_integral_real"]),
                float(q4["pole_corrected_integral_imaginary"]),
            )
        )
        for q4, q8 in zip(q4_rows, q8_rows)
    )
    error_budget_relative = error_budget / max(
        abs(node_totals[ENERGY_ORDERS[1]]), 1.0e-12
    )
    accepted = (
        not unresolved
        and inactive_count == 0
        and len(integrals) == len(cells) * len(ENERGY_ORDERS)
        and node_change <= INNER_RELATIVE_CHANGE_LIMIT
        and error_budget_relative <= INNER_ERROR_BUDGET_LIMIT
    )
    write_csv(paths["poles"], poles, ["node_id", "term_id", "pole_id"])
    write_csv(paths["fits"], fits, ["node_id", "term_id", "pole_id", "fit_scale"])
    write_csv(
        paths["classifications"],
        classifications,
        ["node_id", "term_id", "pole_id", "pole_classification_resolved"],
    )
    write_csv(
        paths["integrals"],
        integrals,
        ["node_id", "contract_index", "energy_order"],
    )
    result = {
        "checkpoint": CHECKPOINT,
        "node_revision": NODE_REVISION,
        "node_plan_sha256": plan_sha256,
        "node_id": node["node_id"],
        "x_panel_index": panel_index,
        "outer_order": int(node["outer_order"]),
        "absolute_soft_cosine": coordinate,
        "mapped_outer_weight": float(node["mapped_outer_weight"]),
        "node_complete": True,
        "acceptance_passed": accepted,
        "nonzero_cell_count": len(cells),
        "distinct_reduced_term_count": len(supports),
        "geometric_pole_count": len(poles),
        "in_support_pole_count": sum(
            bool(row["inside_reduced_term_support"]) for row in poles
        ),
        "material_simple_pole_count": sum(
            bool(row["material_simple_pole"]) for row in classifications
        ),
        "removable_zero_residue_pole_count": sum(
            bool(row["removable_zero_residue_pole"]) for row in classifications
        ),
        "unresolved_pole_count": len(unresolved),
        "inactive_selected_term_count": inactive_count,
        **complex_fields("inner_energy_Q4", node_totals[4]),
        **complex_fields("inner_energy_Q8", node_totals[8]),
        "inner_Q4_Q8_relative_change": node_change,
        "inner_energy_error_budget_absolute": error_budget,
        "inner_energy_error_budget_relative": error_budget_relative,
        "decision": (
            "NODE_POLE_SUBTRACTED_ENERGY_INTEGRAL_ACCEPTED"
            if accepted
            else "NODE_REQUIRES_LOCAL_REFINEMENT"
        ),
        "runtime_seconds": time.perf_counter() - started,
        **{field: False for field in CLAIM_FIELDS},
    }
    atomic_json(paths["result"], result)
    return result


def node_manifest_rows(
    plan: list[dict[str, str]], plan_sha256: str
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for node in plan:
        complete = shard_is_complete(node, plan_sha256)
        result = read_json(shard_paths(node["node_id"])["result"]) if complete else {}
        rows.append(
            {
                **node,
                "shard_state": (
                    "COMPLETE_PASS"
                    if complete and bool(result["acceptance_passed"])
                    else ("COMPLETE_FAIL" if complete else "PENDING")
                ),
                "node_acceptance_passed": (
                    bool(result["acceptance_passed"]) if complete else False
                ),
                "runtime_seconds": result.get("runtime_seconds", ""),
                "node_result_path": str(shard_paths(node["node_id"])["result"]),
            }
        )
    return rows


def collect_shard_rows(
    plan: list[dict[str, str]], plan_sha256: str
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, str]],
    list[dict[str, str]],
    list[dict[str, str]],
    list[dict[str, str]],
]:
    results: list[dict[str, Any]] = []
    poles: list[dict[str, str]] = []
    fits: list[dict[str, str]] = []
    classifications: list[dict[str, str]] = []
    integrals: list[dict[str, str]] = []
    for node in plan:
        if not shard_is_complete(node, plan_sha256):
            continue
        paths = shard_paths(node["node_id"])
        results.append(read_json(paths["result"]))
        poles.extend(read_csv(paths["poles"]))
        fits.extend(read_csv(paths["fits"]))
        classifications.extend(read_csv(paths["classifications"]))
        integrals.extend(read_csv(paths["integrals"]))
    return results, poles, fits, classifications, integrals


def aggregate_outer_integrals(
    plan: list[dict[str, str]],
    node_results: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    result_lookup = {row["node_id"]: row for row in node_results}
    outer_rows: list[dict[str, Any]] = []
    panel_values: dict[tuple[int, int, int], complex] = {}
    for outer_order in OUTER_ORDERS:
        selected = [row for row in plan if int(row["outer_order"]) == outer_order]
        for energy_order in ENERGY_ORDERS:
            total = 0.0j
            for node in selected:
                result = result_lookup[node["node_id"]]
                value = complex(
                    float(result[f"inner_energy_Q{energy_order}_real"]),
                    float(result[f"inner_energy_Q{energy_order}_imaginary"]),
                )
                contribution = float(node["mapped_outer_weight"]) * value
                total += contribution
                key = (
                    int(node["x_panel_index"]),
                    outer_order,
                    energy_order,
                )
                panel_values[key] = panel_values.get(key, 0.0j) + contribution
            outer_rows.append(
                {
                    "epsilon_id": EPSILON_ID,
                    "epsilon": EPSILON,
                    "outer_order": outer_order,
                    "energy_order": energy_order,
                    "node_count": len(selected),
                    **complex_fields("fixed_decay_outer_soft_integral", total),
                    **{field: False for field in CLAIM_FIELDS},
                }
            )
    outer_lookup = {
        (int(row["outer_order"]), int(row["energy_order"])): complex(
            float(row["fixed_decay_outer_soft_integral_real"]),
            float(row["fixed_decay_outer_soft_integral_imaginary"]),
        )
        for row in outer_rows
    }
    outer_change = relative_complex_change(
        outer_lookup[(2, 8)], outer_lookup[(4, 8)]
    )
    inner_budget = sum(
        abs(float(node["mapped_outer_weight"]))
        * float(result_lookup[node["node_id"]]["inner_energy_error_budget_absolute"])
        for node in plan
        if int(node["outer_order"]) == 4
    )
    inner_budget_relative = inner_budget / max(abs(outer_lookup[(4, 8)]), 1.0e-12)
    panel_rows: list[dict[str, Any]] = []
    for panel_index in range(1, 10):
        q2 = panel_values[(panel_index, 2, 8)]
        q4 = panel_values[(panel_index, 4, 8)]
        panel_rows.append(
            {
                "x_panel_index": panel_index,
                **complex_fields("outer_Q2_energy_Q8", q2),
                **complex_fields("outer_Q4_energy_Q8", q4),
                "outer_Q2_Q4_relative_change": relative_complex_change(q2, q4),
                **{field: False for field in CLAIM_FIELDS},
            }
        )
    metrics = {
        "outer_Q2_Q4_relative_change": outer_change,
        "outer_Q4_inner_energy_error_budget_absolute": inner_budget,
        "outer_Q4_inner_energy_error_budget_relative": inner_budget_relative,
        **complex_fields("selected_E0025_fixed_decay_outer_soft_integral", outer_lookup[(4, 8)]),
    }
    return outer_rows, panel_rows, metrics


def direct_5309_control() -> complex:
    row = next(
        row for row in read_csv(FINITE_5309)
        if row["epsilon_id"] == EPSILON_ID and int(row["cubature_order"]) == 8
    )
    return complex(
        float(row["fixed_decay_pair_integral_real"]),
        float(row["fixed_decay_pair_integral_imaginary"]),
    )


def execute(runtime_limit_seconds: float) -> dict[str, Any]:
    set_below_normal_priority()
    mp.mp.dps = M5280.MP_DECIMAL_DIGITS
    M5301.configure_reused_pipeline()
    started = time.perf_counter()
    dry = dry_run()
    if not dry["acceptance_passed"]:
        raise RuntimeError("5312 dry run did not pass")
    contract = read_csv(REDUCED_CONTRACT)
    plan = read_csv(NODE_PLAN)
    plan_sha256 = digest(NODE_PLAN)
    audit_context = M5303.synthetic_context()
    audit_evaluate = M5305.component_evaluator(audit_context)
    identity = identity_audit_rows(contract, audit_evaluate)
    write_csv(IDENTITY_AUDIT, identity)
    identity_passed = bool(identity) and all(
        parse_bool(row["valid_for_MC04_MC12_identity_transfer"])
        for row in identity
    )
    base_context = M5303.synthetic_context()
    multiplier = M5309.physical_multiplier()
    completed_this_run = 0
    for node in plan:
        if shard_is_complete(node, plan_sha256):
            continue
        if time.perf_counter() - started >= runtime_limit_seconds:
            break
        result = run_node(
            node,
            contract,
            plan_sha256,
            base_context,
            multiplier,
        )
        completed_this_run += 1
        atomic_json(
            STATUS,
            {
                "checkpoint": CHECKPOINT,
                "state": "RUNNING",
                "stage": "RESUMABLE_E0025_OUTER_SOFT_NODES",
                "last_completed_node_id": node["node_id"],
                "last_node_acceptance_passed": result["acceptance_passed"],
                "completed_this_run": completed_this_run,
            },
        )
    manifest = node_manifest_rows(plan, plan_sha256)
    write_csv(NODE_MANIFEST, manifest)
    node_results, poles, fits, classifications, integrals = collect_shard_rows(
        plan, plan_sha256
    )
    write_csv(ALL_POLES, poles, ["node_id", "term_id", "pole_id"])
    write_csv(ALL_FITS, fits, ["node_id", "term_id", "pole_id", "fit_scale"])
    write_csv(
        ALL_CLASSIFICATIONS,
        classifications,
        ["node_id", "term_id", "pole_id", "pole_classification_resolved"],
    )
    write_csv(
        ALL_CELL_INTEGRALS,
        integrals,
        ["node_id", "contract_index", "energy_order"],
    )
    all_complete = len(node_results) == len(plan)
    all_nodes_pass = all_complete and all(
        bool(row["acceptance_passed"]) for row in node_results
    )
    if all_complete:
        outer_rows, panel_rows, metrics = aggregate_outer_integrals(
            plan, node_results
        )
    else:
        outer_rows, panel_rows, metrics = [], [], {}
    write_csv(
        OUTER_TOTALS,
        outer_rows,
        ["epsilon_id", "outer_order", "energy_order"],
    )
    write_csv(
        OUTER_PANEL_CONVERGENCE,
        panel_rows,
        ["x_panel_index", "outer_Q2_Q4_relative_change"],
    )
    convergence_passed = (
        all_nodes_pass
        and float(metrics["outer_Q2_Q4_relative_change"])
        <= OUTER_RELATIVE_CHANGE_LIMIT
        and float(metrics["outer_Q4_inner_energy_error_budget_relative"])
        <= INNER_ERROR_BUDGET_LIMIT
    )
    accepted = identity_passed and convergence_passed
    if not all_complete:
        decision = "RESUMABLE_OUTER_SOFT_INTEGRAL_PAUSED__RESUME_REMAINING_NODES"
    elif not all_nodes_pass:
        decision = "POLE_SUBTRACTED_NODE_FAILURES_LOCALIZED__REFINE_LOCAL_POLE_MODEL"
    elif not convergence_passed:
        decision = "POLE_SUBTRACTED_OUTER_SOFT_NOT_CONVERGED__REFINE_OUTER_X_PANELS"
    else:
        decision = (
            "E0025_FIXED_DECAY_OUTER_SOFT_INTEGRAL_CONVERGED__"
            "EXTEND_FIVE_REGULATOR_LADDER"
        )
    formal_end = M5283.formal_inventory_digest()
    direct_control = direct_5309_control()
    selected = (
        complex(
            float(metrics["selected_E0025_fixed_decay_outer_soft_integral_real"]),
            float(metrics["selected_E0025_fixed_decay_outer_soft_integral_imaginary"]),
        )
        if all_complete
        else 0.0j
    )
    result = {
        "checkpoint": CHECKPOINT,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "mode": "resumable-pole-subtracted-outer-soft-integral",
        "acceptance_passed": accepted,
        "decision": decision,
        "identity_audit_passed": identity_passed,
        "identity_audit_row_count": len(identity),
        "maximum_pair_antisymmetry_relative_residual": max(
            float(row["pair_antisymmetry_relative_residual"])
            for row in identity
            if bool(row["identity_reduction_applied"])
        ),
        "maximum_unapplied_pair_diagnostic_residual": max(
            float(row["pair_antisymmetry_relative_residual"])
            for row in identity
            if not bool(row["identity_reduction_applied"])
        ),
        "maximum_orbit_reduction_relative_residual": max(
            float(row["orbit_reduction_relative_residual"]) for row in identity
        ),
        "planned_node_count": len(plan),
        "completed_node_count": len(node_results),
        "completed_node_count_this_run": completed_this_run,
        "accepted_node_count": sum(
            bool(row["acceptance_passed"]) for row in node_results
        ),
        "failed_node_count": sum(
            not bool(row["acceptance_passed"]) for row in node_results
        ),
        "geometric_pole_count": len(poles),
        "classified_in_support_pole_count": len(classifications),
        "material_simple_pole_count": sum(
            parse_bool(row["material_simple_pole"]) for row in classifications
        ),
        "removable_zero_residue_pole_count": sum(
            parse_bool(row["removable_zero_residue_pole"]) for row in classifications
        ),
        "unresolved_pole_count": sum(
            not parse_bool(row["pole_classification_resolved"])
            for row in classifications
        ),
        "all_nodes_complete": all_complete,
        "all_nodes_pass": all_nodes_pass,
        "convergence_passed": convergence_passed,
        **metrics,
        **complex_fields("unaligned_5309_Q8_control", direct_control),
        "aligned_vs_unaligned_control_relative_change": (
            relative_complex_change(direct_control, selected)
            if all_complete
            else ""
        ),
        "formalization_workbench_reference_digest": read_json(RESULT_5311)[
            "formalization_workbench_end_digest"
        ],
        "formalization_workbench_end_digest": formal_end,
        "formalization_workbench_modified_file_count": (
            0
            if formal_end
            == read_json(RESULT_5311)["formalization_workbench_end_digest"]
            else -1
        ),
        "claim_boundary": {
            "valid_for_MC04_MC12_pair_identity_reduction": identity_passed,
            "valid_for_E0025_fixed_decay_outer_soft_integral": accepted,
            **{field: False for field in CLAIM_FIELDS},
            "reason": (
                "Only the E0025 regulator at one fixed absolute decay angle is "
                "integrated. The five-regulator zero limit, decay-angle "
                "integral, phase-space coefficient, local GR, and full MTS "
                "claims remain open."
            ),
        },
        "resource_contract": {
            "maximum_task_python_processes": 1,
            "worker_math_threads": 1,
            "windows_priority": "BelowNormal",
            "maximum_silent_work_hours": 4,
            "runtime_limit_seconds_per_invocation": runtime_limit_seconds,
        },
        "source_files": source_rows(),
        "runtime_seconds": time.perf_counter() - started,
    }
    atomic_json(RESULT, result)
    atomic_json(
        STATUS,
        {
            "checkpoint": CHECKPOINT,
            "state": (
                "COMPLETE"
                if accepted
                else ("PAUSED_RESUMABLE" if not all_complete else "REFINEMENT_REQUIRED")
            ),
            "completed_node_count": len(node_results),
            "planned_node_count": len(plan),
            "decision": decision,
        },
    )
    return result


def validation_gate(gate: str, passed: bool, detail: str) -> dict[str, Any]:
    return {"gate": gate, "passed": bool(passed), "detail": detail}


def render_document(result: dict[str, Any], passed: bool) -> None:
    selected = (
        f"{result['selected_E0025_fixed_decay_outer_soft_integral_real']:.12g} "
        f"{result['selected_E0025_fixed_decay_outer_soft_integral_imaginary']:+.12g} i"
        if result["all_nodes_complete"]
        else "not assembled"
    )
    text = f"""# 5312 — Resumable pole-subtracted outer-soft integral

## Result

The exact 5289 identity
`MC12(s,d) = -MC04(s,-d)` is applied before quadrature.  It removes thirteen
identically zero topology cells and leaves nineteen nonzero MC04-only cells.
The identity and the reduced full orbit are rechecked at both `E040` and
`E0025`; this is an algebraic reduction, not a numerical cancellation guess.

At every Gauss node of all nine topology-aligned soft-angle panels, the inner
energy integral derives its geometric poles, fits each in-support Laurent
residue twice, subtracts material simple poles, and restores their exact
complex logarithms.  Every node is an independent resumable shard.

- completed nodes: `{result['completed_node_count']}/{result['planned_node_count']}`;
- accepted nodes: `{result['accepted_node_count']}`;
- material simple poles: `{result['material_simple_pole_count']}`;
- removable zero-residue poles: `{result['removable_zero_residue_pole_count']}`;
- unresolved poles: `{result['unresolved_pole_count']}`;
- selected `E0025` fixed-decay outer-soft integral: `{selected}`;
- outer Q2/Q4 relative change:
  `{result.get('outer_Q2_Q4_relative_change', 'not assembled')}`;
- propagated inner Q4/Q8 error budget:
  `{result.get('outer_Q4_inner_energy_error_budget_relative', 'not assembled')}`.

Decision: **{result['decision']}**.

Validation: **{'PASS' if passed else 'FAIL'}**.

## Claim boundary

This checkpoint can establish one regulator at one fixed absolute decay
angle.  It does not establish the five-regulator zero limit, decay-angle
integration, a full phase-space coefficient, a UV prediction, local GR, or
the full MTS theory.
"""
    DOCUMENT.write_text(text, encoding="utf-8")


def validate_outputs() -> dict[str, Any]:
    started = time.perf_counter()
    result = read_json(RESULT)
    dry = read_json(DRY_RUN)
    identity = read_csv(IDENTITY_AUDIT)
    contract = read_csv(REDUCED_CONTRACT)
    plan = read_csv(NODE_PLAN)
    manifest = read_csv(NODE_MANIFEST)
    poles = read_csv(ALL_POLES)
    fits = read_csv(ALL_FITS)
    classifications = read_csv(ALL_CLASSIFICATIONS)
    integrals = read_csv(ALL_CELL_INTEGRALS)
    outer = read_csv(OUTER_TOTALS)
    panels = read_csv(OUTER_PANEL_CONVERGENCE)
    plan_sha256 = digest(NODE_PLAN)
    source_files_current = all(
        Path(row["path"]).exists()
        and digest(Path(row["path"])) == row["sha256"]
        for row in result["source_files"]
    )
    shards_current = all(shard_is_complete(node, plan_sha256) for node in plan)
    gates = [
        validation_gate(
            "dry_run_and_result_accepted",
            bool(dry["acceptance_passed"]) and bool(result["acceptance_passed"]),
            result["decision"],
        ),
        validation_gate(
            "MC04_MC12_identity_and_reduced_orbit_rechecked",
            len(identity) == 32 * len(IDENTITY_REGULATORS) * 4
            and all(
                parse_bool(row["valid_for_MC04_MC12_identity_transfer"])
                for row in identity
            ),
            f"rows={len(identity)}; max_pair={result['maximum_pair_antisymmetry_relative_residual']}",
        ),
        validation_gate(
            "thirteen_zero_nineteen_nonzero_contracts",
            len(contract) == 32
            and sum(parse_bool(row["algebraically_zero_cell"]) for row in contract)
            == 13
            and sum(int(row["reduced_MC04_term_count"]) > 0 for row in contract)
            == 19,
            f"contracts={len(contract)}",
        ),
        validation_gate(
            "all_54_resumable_nodes_complete_and_current",
            len(plan) == len(manifest) == 54
            and shards_current
            and all(row["shard_state"] == "COMPLETE_PASS" for row in manifest),
            f"complete={result['completed_node_count']}; planned={len(plan)}",
        ),
        validation_gate(
            "all_in_support_poles_classified",
            len(classifications)
            == int(result["classified_in_support_pole_count"])
            and all(
                parse_bool(row["pole_classification_resolved"])
                for row in classifications
            )
            and int(result["unresolved_pole_count"]) == 0,
            f"geometric={len(poles)}; classified={len(classifications)}; fits={len(fits)}",
        ),
        validation_gate(
            "inner_and_outer_quadrature_converge",
            len(integrals) > 0
            and len(outer) == len(OUTER_ORDERS) * len(ENERGY_ORDERS)
            and len(panels) == 9
            and bool(result["convergence_passed"])
            and float(result["outer_Q2_Q4_relative_change"])
            <= OUTER_RELATIVE_CHANGE_LIMIT
            and float(result["outer_Q4_inner_energy_error_budget_relative"])
            <= INNER_ERROR_BUDGET_LIMIT,
            (
                f"outer={result.get('outer_Q2_Q4_relative_change')}; "
                f"inner_budget={result.get('outer_Q4_inner_energy_error_budget_relative')}"
            ),
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
            "no regulator-zero, decay-angle, phase-space, UV, local-GR, or full-MTS claim",
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
            "VALIDATED_E0025_FIXED_DECAY_POLE_SUBTRACTED_OUTER_SOFT_INTEGRAL"
            if passed
            else "E0025_OUTER_SOFT_INTEGRAL_VALIDATION_FAILED"
        ),
        "runtime_seconds": time.perf_counter() - started,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode", choices=("dry-run", "run", "validate"), required=True
    )
    parser.add_argument(
        "--max-runtime-hours", type=float, default=2.75
    )
    return parser.parse_args()


def main() -> int:
    set_below_normal_priority()
    arguments = parse_args()
    if arguments.mode == "dry-run":
        result = dry_run()
    elif arguments.mode == "run":
        result = execute(arguments.max_runtime_hours * 3600.0)
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
