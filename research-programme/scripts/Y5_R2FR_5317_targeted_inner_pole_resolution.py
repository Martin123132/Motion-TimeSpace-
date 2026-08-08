from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import math
import time
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SCRIPTS = POST / "scripts"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
RESIDUALS = POST / "source-intake" / "mts_residuals"
SOURCE = FUNCTIONAL_RG / "5317"
SHARDS = SOURCE / "repaired_shards"

SCRIPT_5316 = SCRIPTS / "Y5_R2FR_5316_four_regulator_pole_subtracted_coarse_scan.py"
RESULT_5316 = FUNCTIONAL_RG / "5316" / "four_regulator_coarse_scan_result.json"
MANIFEST_5316 = FUNCTIONAL_RG / "5316" / "four_regulator_coarse_node_manifest.csv"
CONTRACT_5312 = FUNCTIONAL_RG / "5312" / "reduced_fixed_decay_cubature_contract.csv"
NODE_PLAN_5312 = FUNCTIONAL_RG / "5312" / "E0025_outer_soft_node_plan.csv"

DRY_RUN = SOURCE / "targeted_inner_pole_resolution_dry_run.json"
FAILED_INVENTORY = SOURCE / "failed_inner_node_inventory.csv"
PARENT_HASHES = SOURCE / "parent_5316_shard_hashes.csv"
REPAIR_MANIFEST = SOURCE / "targeted_repair_node_manifest.csv"
COMBINED_MANIFEST = SOURCE / "combined_four_regulator_node_manifest.csv"
MATERIAL_FITS = SOURCE / "normalized_double_laurent_material_fits.csv"
OFF_AXIS_AUDIT = SOURCE / "off_axis_raw_direct_convergence_audit.csv"
CLASSIFICATIONS = SOURCE / "repaired_pole_classifications.csv"
CELL_INTEGRALS = SOURCE / "repaired_cell_integrals.csv"
OUTER_TOTALS = SOURCE / "repaired_four_regulator_outer_totals.csv"
PANEL_CONVERGENCE = SOURCE / "repaired_four_regulator_panel_convergence.csv"
REGULATOR_SUMMARY = SOURCE / "five_regulator_repaired_status.csv"
RESULT = SOURCE / "targeted_inner_pole_resolution_result.json"
VALIDATION = SOURCE / "targeted_inner_pole_resolution_validation.csv"
RESIDUAL_VALIDATION = RESIDUALS / "P8_Y5_BRR545_5317_VALIDATION.csv"
STATUS = SOURCE / "status.json"
DOCUMENT = POST / "5317-Y5-R2FR-targeted-inner-pole-resolution.md"

CHECKPOINT = 5317
PARENT_CHECKPOINT = 5316
MARKER = "MTS_5317_TARGETED_INNER_POLE_RESOLUTION"
REVISION = "targeted-inner-pole-resolution-v1"
REPAIR_NODE_REVISION = "targeted-inner-pole-repair-node-v1"
FIT_BACKGROUND_DEGREE = 6
FIT_SCALES = (1.0, 1.5)
FIT_UNITS = (
    -5.0,
    -4.0,
    -3.0,
    -2.5,
    -2.0,
    -1.5,
    -1.0,
    -0.5,
    0.5,
    1.0,
    1.5,
    2.0,
    2.5,
    3.0,
    4.0,
    5.0,
)
HOLDOUT_UNITS = (
    -4.5,
    -3.5,
    -2.75,
    -2.25,
    -1.75,
    -1.25,
    -0.75,
    -0.25,
    0.25,
    0.75,
    1.25,
    1.75,
    2.25,
    2.75,
    3.5,
    4.5,
)
MAXIMUM_POLE_REFINEMENTS = 4
POLE_REFINEMENT_TOLERANCE = 1.0e-12
FIT_RELATIVE_RESIDUAL_LIMIT = 1.0e-4
HOLDOUT_RELATIVE_RESIDUAL_LIMIT = 1.0e-4
RESIDUE_SCALE_CHANGE_LIMIT = 5.0e-4
SECOND_ORDER_SUPPRESSION_LIMIT = 1.0e-4
OFF_AXIS_FLOAT_SEPARATION_MULTIPLIER = 100.0
DEFAULT_RUNTIME_LIMIT_SECONDS = 1.5 * 3600.0
CLAIM_FIELDS = (
    "valid_for_full_regulator_zero_limit",
    "valid_for_decay_angle_integration",
    "valid_for_full_phase_space_coefficient",
    "valid_for_numeric_UV_claim",
    "valid_for_local_GR_claim",
    "valid_for_full_MTS_claim",
)
CLASSIFICATION_BOOLEAN_FIELDS = (
    "all_fit_samples_mask_active",
    "material_simple_pole",
    "removable_zero_residue_pole",
    "pole_classification_resolved",
    "valid_for_pole_subtracted_outer_soft_node",
    *CLAIM_FIELDS,
)


def load_module(name: str, path: Path) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot import {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5316 = load_module("mts_5316_for_5317", SCRIPT_5316)
M5312 = M5316.M5312
M5283 = M5316.M5283
np = M5312.np
mp = M5312.mp


def read_json(path: Path) -> Any:
    return M5312.read_json(path)


def read_csv(path: Path) -> list[dict[str, str]]:
    return M5312.read_csv(path)


def write_csv(
    path: Path,
    rows: list[dict[str, Any]],
    fieldnames: list[str] | None = None,
) -> None:
    M5312.write_csv(path, rows, fieldnames)


def atomic_json(path: Path, value: Any) -> None:
    M5312.atomic_json(path, value)


def digest(path: Path) -> str:
    return M5312.digest(path)


def parse_bool(value: Any) -> bool:
    return M5312.parse_bool(value)


def complex_fields(prefix: str, value: complex) -> dict[str, float]:
    return M5312.complex_fields(prefix, value)


def relative_complex_change(first: complex, second: complex) -> float:
    return M5312.relative_complex_change(first, second)


def validation_gate(gate: str, passed: bool, detail: str) -> dict[str, Any]:
    return M5312.validation_gate(gate, passed, detail)


def target_regulators() -> dict[str, float]:
    return dict(M5316.TARGET_REGULATORS)


def parent_manifest() -> list[dict[str, str]]:
    return read_csv(MANIFEST_5316)


def parent_shard_files(epsilon_id: str, node_id: str) -> list[Path]:
    paths = M5316.shard_paths(epsilon_id, node_id)
    return [
        paths["poles"],
        paths["fits"],
        paths["classifications"],
        paths["integrals"],
        paths["result"],
    ]


def bundle_sha256(paths: list[Path]) -> str:
    hasher = hashlib.sha256()
    for path in paths:
        hasher.update(path.name.encode("utf-8"))
        hasher.update(digest(path).encode("ascii"))
    return hasher.hexdigest()


def parent_hash_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for manifest_row in parent_manifest():
        epsilon_id = manifest_row["epsilon_id"]
        node_id = manifest_row["node_id"]
        paths = parent_shard_files(epsilon_id, node_id)
        rows.append(
            {
                "epsilon_id": epsilon_id,
                "node_id": node_id,
                "parent_shard_state": manifest_row["shard_state"],
                "parent_shard_bundle_sha256": bundle_sha256(paths),
                "parent_result_path": str(paths[-1]),
                **{field: False for field in CLAIM_FIELDS},
            }
        )
    return rows


def parent_bundle_sha256(rows: list[dict[str, Any]]) -> str:
    payload = [
        {
            "epsilon_id": row["epsilon_id"],
            "node_id": row["node_id"],
            "state": row["parent_shard_state"],
            "sha256": row["parent_shard_bundle_sha256"],
        }
        for row in rows
    ]
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True).encode("utf-8")
    ).hexdigest()


def typed_classification(row: dict[str, Any]) -> dict[str, Any]:
    typed = dict(row)
    for field in CLASSIFICATION_BOOLEAN_FIELDS:
        if field in typed:
            typed[field] = parse_bool(typed[field])
    return typed


def unresolved_inventory_rows() -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for manifest_row in parent_manifest():
        if manifest_row["shard_state"] != "COMPLETE_FAIL":
            continue
        epsilon_id = manifest_row["epsilon_id"]
        node_id = manifest_row["node_id"]
        paths = M5316.shard_paths(epsilon_id, node_id)
        classifications = [
            typed_classification(row) for row in read_csv(paths["classifications"])
        ]
        unresolved = [
            row for row in classifications if not row["pole_classification_resolved"]
        ]
        for row in unresolved:
            residue = float(row["selected_residue_magnitude"])
            if residue >= M5312.MATERIAL_RESIDUE_FLOOR:
                route = "NORMALIZED_DOUBLE_LAURENT_POLE_REFINEMENT"
            elif residue > M5312.REMOVABLE_RESIDUE_CEILING:
                route = "OFF_AXIS_RAW_DIRECT_CONVERGENCE"
            else:
                route = "UNEXPECTED_UNRESOLVED_CLASS"
            rows.append(
                {
                    "epsilon_id": epsilon_id,
                    "epsilon": float(manifest_row["epsilon"]),
                    "node_id": node_id,
                    "x_panel_index": int(manifest_row["x_panel_index"]),
                    "outer_order": int(manifest_row["outer_order"]),
                    "absolute_soft_cosine": float(
                        manifest_row["absolute_soft_cosine"]
                    ),
                    "term_id": row["term_id"],
                    "pole_id": row["pole_id"],
                    "pole_real": float(row["pole_real"]),
                    "pole_imaginary": float(row["pole_imaginary"]),
                    "parent_selected_residue_magnitude": residue,
                    "resolution_route": route,
                    "parent_result_path": str(paths["result"]),
                    **{field: False for field in CLAIM_FIELDS},
                }
            )
    return rows


def dry_run() -> dict[str, Any]:
    started = time.perf_counter()
    SOURCE.mkdir(parents=True, exist_ok=True)
    required = [
        SCRIPT_5316,
        RESULT_5316,
        MANIFEST_5316,
        CONTRACT_5312,
        NODE_PLAN_5312,
    ]
    missing = [str(path) for path in required if not path.exists()]
    parent = read_json(RESULT_5316) if not missing else {}
    manifest = parent_manifest() if not missing else []
    inventory = unresolved_inventory_rows() if manifest else []
    hashes = parent_hash_rows() if manifest else []
    route_counts = {
        route: sum(row["resolution_route"] == route for row in inventory)
        for route in {
            "NORMALIZED_DOUBLE_LAURENT_POLE_REFINEMENT",
            "OFF_AXIS_RAW_DIRECT_CONVERGENCE",
            "UNEXPECTED_UNRESOLVED_CLASS",
        }
    }
    checks = {
        "required_paths_exist": not missing,
        "parent_diagnostic_is_complete": (
            bool(parent)
            and int(parent["completed_node_count"]) == 216
            and int(parent["failed_inner_node_count"]) == 18
        ),
        "parent_manifest_has_198_pass_and_18_fail": (
            len(manifest) == 216
            and sum(row["shard_state"] == "COMPLETE_PASS" for row in manifest)
            == 198
            and sum(row["shard_state"] == "COMPLETE_FAIL" for row in manifest)
            == 18
        ),
        "two_material_and_sixteen_off_axis_targets": (
            len(inventory) == 18
            and route_counts["NORMALIZED_DOUBLE_LAURENT_POLE_REFINEMENT"] == 2
            and route_counts["OFF_AXIS_RAW_DIRECT_CONVERGENCE"] == 16
            and route_counts["UNEXPECTED_UNRESOLVED_CLASS"] == 0
        ),
        "all_parent_shards_are_hashable": len(hashes) == 216,
        "formalization_workbench_unchanged": (
            bool(parent)
            and M5283.formal_inventory_digest()
            == parent["formalization_workbench_end_digest"]
        ),
    }
    accepted = all(checks.values())
    if inventory:
        write_csv(FAILED_INVENTORY, inventory, ["epsilon_id", "node_id"])
    if hashes:
        write_csv(PARENT_HASHES, hashes, ["epsilon_id", "node_id"])
    result = {
        "checkpoint": CHECKPOINT,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "mode": "dry-run",
        "acceptance_passed": accepted,
        "decision": (
            "DRY_RUN_ACCEPTED__REPAIR_ONLY_EIGHTEEN_FAILED_INNER_NODES"
            if accepted
            else "TARGETED_INNER_POLE_RESOLUTION_DRY_RUN_BLOCKED"
        ),
        "checks": checks,
        "missing_paths": missing,
        "parent_pass_node_count": 198 if accepted else 0,
        "target_node_count": len(inventory),
        "resolution_route_counts": route_counts,
        "parent_shard_bundle_sha256": (
            parent_bundle_sha256(hashes) if hashes else ""
        ),
        "runtime_seconds": time.perf_counter() - started,
        **{field: False for field in CLAIM_FIELDS},
    }
    atomic_json(DRY_RUN, result)
    return result


def repair_paths(epsilon_id: str, node_id: str) -> dict[str, Path]:
    root = SHARDS / epsilon_id / node_id
    return {
        "root": root,
        "fits": root / "material_refinement_fits.csv",
        "off_axis": root / "off_axis_raw_audit.csv",
        "classifications": root / "pole_classification.csv",
        "integrals": root / "cell_integrals.csv",
        "result": root / "result.json",
    }


def repair_plan_sha256(parent_bundle: str) -> str:
    payload = {
        "revision": REVISION,
        "node_revision": REPAIR_NODE_REVISION,
        "script_sha256": digest(Path(__file__).resolve()),
        "parent_shard_bundle_sha256": parent_bundle,
        "contract_sha256": digest(CONTRACT_5312),
        "node_plan_sha256": digest(NODE_PLAN_5312),
    }
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True).encode("utf-8")
    ).hexdigest()


def repair_complete(
    epsilon_id: str,
    node_id: str,
    plan_sha256: str,
) -> bool:
    paths = repair_paths(epsilon_id, node_id)
    required = [paths["fits"], paths["off_axis"], paths["classifications"], paths["integrals"], paths["result"]]
    if not all(path.exists() for path in required):
        return False
    try:
        result = read_json(paths["result"])
        for key in ("fits", "off_axis", "classifications", "integrals"):
            read_csv(paths[key])
    except Exception:
        return False
    return (
        result.get("node_revision") == REPAIR_NODE_REVISION
        and result.get("repair_plan_sha256") == plan_sha256
        and result.get("epsilon_id") == epsilon_id
        and result.get("node_id") == node_id
        and bool(result.get("node_complete"))
    )


def node_from_id(node_id: str) -> dict[str, str]:
    return next(row for row in M5316.base_plan() if row["node_id"] == node_id)


def fit_radius(
    center: float,
    pole: complex,
    lower: float,
    upper: float,
) -> float:
    maximum_unit = max(abs(value) for value in FIT_UNITS)
    boundary_safe = 0.8 * min(center - lower, upper - center) / (
        maximum_unit * max(FIT_SCALES)
    )
    return min(max(8.0 * abs(pole.imag), 2.0e-6), boundary_safe)


def normalized_double_laurent_fit(
    center: float,
    pole: complex,
    lower: float,
    upper: float,
    fit_scale: float,
    units: tuple[float, ...],
    evaluate_term: Any,
) -> dict[str, Any]:
    radius = fit_scale * fit_radius(center, pole, lower, upper)
    if radius <= 0.0:
        raise RuntimeError("nonpositive normalized Laurent fit radius")
    matrix_rows: list[list[complex]] = []
    values: list[complex] = []
    all_active = True
    for unit in units:
        energy = center + unit * radius
        value, active = evaluate_term(energy)
        all_active = all_active and active
        matrix_rows.append(
            [
                radius**2 / (energy - pole) ** 2,
                radius / (energy - pole),
                *[
                    complex(unit**power)
                    for power in range(FIT_BACKGROUND_DEGREE + 1)
                ],
            ]
        )
        values.append(value)
    matrix = np.asarray(matrix_rows, dtype=np.complex128)
    vector = np.asarray(values, dtype=np.complex128)
    coefficients, _, rank, singular_values = np.linalg.lstsq(
        matrix, vector, rcond=None
    )
    predicted = matrix @ coefficients
    residual = float(
        np.linalg.norm(predicted - vector) / max(np.linalg.norm(vector), 1.0)
    )
    return {
        "fit_scale": fit_scale,
        "fit_radius": radius,
        "sample_count": len(units),
        "all_samples_active": all_active,
        "matrix_rank": int(rank),
        "matrix_column_count": int(matrix.shape[1]),
        "condition_number": float(singular_values[0] / singular_values[-1]),
        "relative_residual": residual,
        "second_order_coefficient": complex(coefficients[0]) * radius**2,
        "simple_residue": complex(coefficients[1]) * radius,
        "coefficients": coefficients,
    }


def holdout_residual(
    center: float,
    pole: complex,
    fit: dict[str, Any],
    evaluate_term: Any,
) -> tuple[float, bool]:
    radius = float(fit["fit_radius"])
    matrix_rows: list[list[complex]] = []
    values: list[complex] = []
    all_active = True
    for unit in HOLDOUT_UNITS:
        energy = center + unit * radius
        value, active = evaluate_term(energy)
        all_active = all_active and active
        matrix_rows.append(
            [
                radius**2 / (energy - pole) ** 2,
                radius / (energy - pole),
                *[
                    complex(unit**power)
                    for power in range(FIT_BACKGROUND_DEGREE + 1)
                ],
            ]
        )
        values.append(value)
    matrix = np.asarray(matrix_rows, dtype=np.complex128)
    vector = np.asarray(values, dtype=np.complex128)
    predicted = matrix @ fit["coefficients"]
    residual = float(
        np.linalg.norm(predicted - vector) / max(np.linalg.norm(vector), 1.0)
    )
    return residual, all_active


def refine_material_pole(
    epsilon_id: str,
    node: dict[str, Any],
    pole_row: dict[str, Any],
    evaluate: Any,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    coordinate = float(node["absolute_soft_cosine"])
    term_id = str(pole_row["term_id"])
    specification = M5312.M5308.SURFACE_LOOKUP[term_id]
    center = float(pole_row["real_axis_center"])
    lower = float(pole_row["support_energy_lower"])
    upper = float(pole_row["support_energy_upper"])
    geometric = complex(
        float(pole_row["pole_real"]), float(pole_row["pole_imaginary"])
    )
    refined = geometric
    cache: dict[float, tuple[complex, bool]] = {}

    def evaluate_term(energy: float) -> tuple[complex, bool]:
        if energy not in cache:
            cache[energy] = evaluate(
                epsilon_id,
                energy,
                coordinate,
                "MC04",
                int(specification["soft_sign"]),
                int(specification["decay_sign"]),
            )
        return cache[energy]

    rows: list[dict[str, Any]] = []
    converged = False
    for iteration in range(1, MAXIMUM_POLE_REFINEMENTS + 1):
        fit = normalized_double_laurent_fit(
            center,
            refined,
            lower,
            upper,
            1.0,
            FIT_UNITS,
            evaluate_term,
        )
        residue = fit["simple_residue"]
        correction = (
            fit["second_order_coefficient"] / residue
            if abs(residue) > 0.0
            else complex(math.inf, math.inf)
        )
        rows.append(
            {
                "epsilon_id": epsilon_id,
                "node_id": node["node_id"],
                "term_id": term_id,
                "pole_id": pole_row["pole_id"],
                "fit_row_type": "POLE_REFINEMENT_ITERATION",
                "pole_refinement_iteration": iteration,
                "fit_scale": 1.0,
                "fit_radius": fit["fit_radius"],
                "fit_sample_count": fit["sample_count"],
                "holdout_sample_count": 0,
                "background_polynomial_degree": FIT_BACKGROUND_DEGREE,
                **complex_fields("input_pole", refined),
                **complex_fields(
                    "second_order_coefficient_R2",
                    fit["second_order_coefficient"],
                ),
                **complex_fields("simple_residue_R1", residue),
                **complex_fields("pole_correction_R2_over_R1", correction),
                "fit_relative_residual": fit["relative_residual"],
                "holdout_relative_residual": "",
                "matrix_rank": fit["matrix_rank"],
                "matrix_column_count": fit["matrix_column_count"],
                "condition_number": fit["condition_number"],
                "all_fit_samples_mask_active": fit["all_samples_active"],
                "all_holdout_samples_mask_active": "",
                "refined_simple_pole_contract_passes": False,
                **{field: False for field in CLAIM_FIELDS},
            }
        )
        if not math.isfinite(abs(correction)):
            break
        refined += correction
        if abs(correction) <= POLE_REFINEMENT_TOLERANCE:
            converged = True
            break
    final_fits: list[dict[str, Any]] = []
    for scale in FIT_SCALES:
        fit = normalized_double_laurent_fit(
            center,
            refined,
            lower,
            upper,
            scale,
            FIT_UNITS,
            evaluate_term,
        )
        holdout, holdout_active = holdout_residual(
            center, refined, fit, evaluate_term
        )
        fit["holdout_relative_residual"] = holdout
        fit["all_holdout_samples_active"] = holdout_active
        fit["second_order_suppression_ratio"] = abs(
            fit["second_order_coefficient"]
        ) / max(
            abs(fit["simple_residue"])
            * max(abs(refined.imag), float(fit["fit_radius"]), 1.0e-9),
            1.0e-300,
        )
        final_fits.append(fit)
    residues = [fit["simple_residue"] for fit in final_fits]
    residue_change = relative_complex_change(residues[0], residues[1])
    conditioning_passes = all(
        fit["condition_number"] * np.finfo(float).eps
        <= FIT_RELATIVE_RESIDUAL_LIMIT / 100.0
        for fit in final_fits
    )
    contract_passes = (
        converged
        and lower < refined.real < upper
        and all(fit["all_samples_active"] for fit in final_fits)
        and all(fit["all_holdout_samples_active"] for fit in final_fits)
        and all(
            fit["matrix_rank"] == fit["matrix_column_count"]
            for fit in final_fits
        )
        and conditioning_passes
        and max(fit["relative_residual"] for fit in final_fits)
        <= FIT_RELATIVE_RESIDUAL_LIMIT
        and max(fit["holdout_relative_residual"] for fit in final_fits)
        <= HOLDOUT_RELATIVE_RESIDUAL_LIMIT
        and residue_change <= RESIDUE_SCALE_CHANGE_LIMIT
        and max(fit["second_order_suppression_ratio"] for fit in final_fits)
        <= SECOND_ORDER_SUPPRESSION_LIMIT
        and min(abs(value) for value in residues)
        >= M5312.MATERIAL_RESIDUE_FLOOR
    )
    for fit in final_fits:
        rows.append(
            {
                "epsilon_id": epsilon_id,
                "node_id": node["node_id"],
                "term_id": term_id,
                "pole_id": pole_row["pole_id"],
                "fit_row_type": "FINAL_REFINED_SIMPLE_POLE_FIT",
                "pole_refinement_iteration": sum(
                    row["fit_row_type"] == "POLE_REFINEMENT_ITERATION"
                    for row in rows
                ),
                "fit_scale": fit["fit_scale"],
                "fit_radius": fit["fit_radius"],
                "fit_sample_count": fit["sample_count"],
                "holdout_sample_count": len(HOLDOUT_UNITS),
                "background_polynomial_degree": FIT_BACKGROUND_DEGREE,
                **complex_fields("input_pole", refined),
                **complex_fields(
                    "second_order_coefficient_R2",
                    fit["second_order_coefficient"],
                ),
                **complex_fields("simple_residue_R1", fit["simple_residue"]),
                **complex_fields("pole_correction_R2_over_R1", 0.0j),
                "fit_relative_residual": fit["relative_residual"],
                "holdout_relative_residual": fit["holdout_relative_residual"],
                "matrix_rank": fit["matrix_rank"],
                "matrix_column_count": fit["matrix_column_count"],
                "condition_number": fit["condition_number"],
                "all_fit_samples_mask_active": fit["all_samples_active"],
                "all_holdout_samples_mask_active": fit[
                    "all_holdout_samples_active"
                ],
                "residue_fit_scale_relative_change": residue_change,
                "second_order_suppression_ratio": fit[
                    "second_order_suppression_ratio"
                ],
                "refined_simple_pole_contract_passes": contract_passes,
                **{field: False for field in CLAIM_FIELDS},
            }
        )
    return (
        {
            "contract_passes": contract_passes,
            "geometric_pole": geometric,
            "refined_pole": refined,
            "selected_residue": residues[-1],
            "maximum_fit_relative_residual": max(
                fit["relative_residual"] for fit in final_fits
            ),
            "maximum_holdout_relative_residual": max(
                fit["holdout_relative_residual"] for fit in final_fits
            ),
            "residue_fit_scale_relative_change": residue_change,
            "maximum_second_order_suppression_ratio": max(
                fit["second_order_suppression_ratio"] for fit in final_fits
            ),
            "evaluation_count": len(cache),
        },
        rows,
    )


def weighted_support_width(
    term_id: str,
    support_id: str,
    cells: list[dict[str, Any]],
    supports: dict[str, list[dict[str, Any]]],
) -> float:
    total = 0.0
    for cell in cells:
        if term_id not in cell["coefficients"]:
            continue
        support = M5312.support_for_cell_term(supports, term_id, cell)
        if support["support_id"] != support_id:
            continue
        total += abs(int(cell["coefficients"][term_id])) * (
            float(cell["energy_upper"]) - float(cell["energy_lower"])
        )
    return total


def off_axis_audit_row(
    epsilon_id: str,
    node: dict[str, Any],
    classification: dict[str, Any],
    parent_fits: list[dict[str, str]],
    cells: list[dict[str, Any]],
    supports: dict[str, list[dict[str, Any]]],
    multiplier: float,
) -> dict[str, Any]:
    pole = complex(
        float(classification["pole_real"]),
        float(classification["pole_imaginary"]),
    )
    separation = abs(pole.imag)
    floating_floor = (
        OFF_AXIS_FLOAT_SEPARATION_MULTIPLIER
        * np.finfo(float).eps
        * max(1.0, abs(pole.real))
    )
    local_fits = [
        row
        for row in parent_fits
        if row["term_id"] == classification["term_id"]
        and row["pole_id"] == classification["pole_id"]
    ]
    residue_proxy = max(
        (float(row["fitted_residue_magnitude"]) for row in local_fits),
        default=float(classification["selected_residue_magnitude"]),
    )
    width = weighted_support_width(
        str(classification["term_id"]),
        str(classification["support_id"]),
        cells,
        supports,
    )
    proxy = (
        multiplier * residue_proxy * width / separation
        if separation > 0.0
        else math.inf
    )
    reliable = math.isfinite(separation) and separation > floating_floor
    return {
        "epsilon_id": epsilon_id,
        "node_id": node["node_id"],
        "term_id": classification["term_id"],
        "pole_id": classification["pole_id"],
        "pole_real": pole.real,
        "pole_imaginary": pole.imag,
        "minimum_real_contour_separation": separation,
        "floating_separation_floor": floating_floor,
        "contour_separation_to_float_floor_ratio": (
            separation / floating_floor if floating_floor > 0.0 else math.inf
        ),
        "weighted_support_width": width,
        "parent_fit_residue_envelope_proxy": residue_proxy,
        "fit_residue_contour_proxy_estimate": proxy,
        "contour_separation_reliable": reliable,
        "raw_integrand_retained_without_subtraction": True,
        "valid_for_rigorous_residue_bound": False,
        "valid_for_off_axis_raw_direct_quadrature": reliable,
        "raw_node_acceptance_passed": False,
        "reason": (
            "Nonzero imaginary separation proves the pole is off the real energy "
            "contour. The unstable small-residue fit is retained only as a proxy; "
            "acceptance instead requires direct raw Q4/Q8 convergence."
        ),
        **{field: False for field in CLAIM_FIELDS},
    }


def node_error_metrics(
    integrals: list[dict[str, Any]],
    node_totals: dict[int, complex],
) -> tuple[float, float, float]:
    node_change = relative_complex_change(node_totals[4], node_totals[8])
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
    error_relative = error_budget / max(abs(node_totals[8]), 1.0e-12)
    return node_change, error_budget, error_relative


def repair_node(
    inventory: dict[str, Any],
    contract: list[dict[str, Any]],
    plan_sha256: str,
    base_context: dict[str, Any],
    multiplier: float,
) -> dict[str, Any]:
    started = time.perf_counter()
    epsilon_id = str(inventory["epsilon_id"])
    node_id = str(inventory["node_id"])
    node = node_from_id(node_id)
    parent_paths = M5316.shard_paths(epsilon_id, node_id)
    paths = repair_paths(epsilon_id, node_id)
    paths["root"].mkdir(parents=True, exist_ok=True)
    poles = read_csv(parent_paths["poles"])
    parent_fits = read_csv(parent_paths["fits"])
    classifications = [
        typed_classification(row)
        for row in read_csv(parent_paths["classifications"])
    ]
    coordinate = float(node["absolute_soft_cosine"])
    panel_index = int(node["x_panel_index"])
    cells = [
        M5312.cell_geometry(row, coordinate)
        for row in contract
        if int(row["x_panel_index"]) == panel_index
        and int(row["reduced_MC04_term_count"]) > 0
    ]
    supports = M5312.merged_term_supports(cells)
    evaluate = M5312.M5305.component_evaluator(base_context)
    fit_rows: list[dict[str, Any]] = []
    off_axis_rows: list[dict[str, Any]] = []
    for classification in classifications:
        if classification["pole_classification_resolved"]:
            classification["resolution_method"] = "PARENT_5316_CLASSIFICATION"
            continue
        pole_row = next(
            row
            for row in poles
            if row["term_id"] == classification["term_id"]
            and row["pole_id"] == classification["pole_id"]
        )
        if inventory["resolution_route"] == (
            "NORMALIZED_DOUBLE_LAURENT_POLE_REFINEMENT"
        ):
            refined, local_fits = refine_material_pole(
                epsilon_id, node, pole_row, evaluate
            )
            fit_rows.extend(local_fits)
            if refined["contract_passes"]:
                classification.update(
                    {
                        "geometric_pole_real": refined["geometric_pole"].real,
                        "geometric_pole_imaginary": refined[
                            "geometric_pole"
                        ].imag,
                        "pole_real": refined["refined_pole"].real,
                        "pole_imaginary": refined["refined_pole"].imag,
                        **complex_fields(
                            "selected_residue", refined["selected_residue"]
                        ),
                        "maximum_fit_relative_residual": refined[
                            "maximum_fit_relative_residual"
                        ],
                        "maximum_holdout_relative_residual": refined[
                            "maximum_holdout_relative_residual"
                        ],
                        "fit_residue_relative_change": refined[
                            "residue_fit_scale_relative_change"
                        ],
                        "maximum_second_order_suppression_ratio": refined[
                            "maximum_second_order_suppression_ratio"
                        ],
                        "all_fit_samples_mask_active": True,
                        "material_simple_pole": True,
                        "removable_zero_residue_pole": False,
                        "pole_classification_resolved": True,
                        "failure_reason": "",
                        "valid_for_pole_subtracted_outer_soft_node": True,
                        "resolution_method": (
                            "NORMALIZED_DOUBLE_LAURENT_POLE_REFINEMENT"
                        ),
                    }
                )
        elif inventory["resolution_route"] == "OFF_AXIS_RAW_DIRECT_CONVERGENCE":
            audit = off_axis_audit_row(
                epsilon_id,
                node,
                classification,
                parent_fits,
                cells,
                supports,
                multiplier,
            )
            off_axis_rows.append(audit)
            if audit["contour_separation_reliable"]:
                classification.update(
                    {
                        "material_simple_pole": False,
                        "removable_zero_residue_pole": False,
                        "pole_classification_resolved": True,
                        "failure_reason": "",
                        "valid_for_pole_subtracted_outer_soft_node": True,
                        "resolution_method": "OFF_AXIS_RAW_DIRECT_CONVERGENCE",
                        "off_axis_raw_no_subtraction": True,
                    }
                )
    unresolved = [
        row for row in classifications if not row["pole_classification_resolved"]
    ]
    if unresolved:
        integrals: list[dict[str, Any]] = []
        node_totals = {4: 0.0j, 8: 0.0j}
        inactive_count = 0
    else:
        integrals, node_totals, inactive_count = M5312.integrate_node_cells(
            node,
            cells,
            supports,
            classifications,
            evaluate,
            multiplier,
        )
    node_change, error_budget, error_relative = node_error_metrics(
        integrals, node_totals
    )
    accepted = (
        not unresolved
        and inactive_count == 0
        and len(integrals) == len(cells) * len(M5312.ENERGY_ORDERS)
        and node_change <= M5312.INNER_RELATIVE_CHANGE_LIMIT
        and error_relative <= M5312.INNER_ERROR_BUDGET_LIMIT
    )
    for row in off_axis_rows:
        row["raw_node_acceptance_passed"] = accepted
    write_csv(
        paths["fits"],
        fit_rows,
        ["epsilon_id", "node_id", "term_id", "pole_id", "fit_row_type"],
    )
    write_csv(
        paths["off_axis"],
        off_axis_rows,
        ["epsilon_id", "node_id", "term_id", "pole_id"],
    )
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
        "parent_checkpoint": PARENT_CHECKPOINT,
        "node_revision": REPAIR_NODE_REVISION,
        "repair_plan_sha256": plan_sha256,
        "epsilon_id": epsilon_id,
        "epsilon": float(inventory["epsilon"]),
        "node_id": node_id,
        "x_panel_index": panel_index,
        "outer_order": int(node["outer_order"]),
        "absolute_soft_cosine": coordinate,
        "mapped_outer_weight": float(node["mapped_outer_weight"]),
        "node_complete": True,
        "acceptance_passed": accepted,
        "resolution_route": inventory["resolution_route"],
        "parent_node_result_path": str(parent_paths["result"]),
        "parent_node_result_sha256": digest(parent_paths["result"]),
        "nonzero_cell_count": len(cells),
        "distinct_reduced_term_count": len(supports),
        "geometric_pole_count": len(poles),
        "in_support_pole_count": sum(
            parse_bool(row["inside_reduced_term_support"]) for row in poles
        ),
        "material_simple_pole_count": sum(
            row["material_simple_pole"] for row in classifications
        ),
        "removable_zero_residue_pole_count": sum(
            row["removable_zero_residue_pole"] for row in classifications
        ),
        "off_axis_raw_direct_count": sum(
            row.get("resolution_method") == "OFF_AXIS_RAW_DIRECT_CONVERGENCE"
            for row in classifications
        ),
        "unresolved_pole_count": len(unresolved),
        "inactive_selected_term_count": inactive_count,
        **complex_fields("inner_energy_Q4", node_totals[4]),
        **complex_fields("inner_energy_Q8", node_totals[8]),
        "inner_Q4_Q8_relative_change": node_change,
        "inner_energy_error_budget_absolute": error_budget,
        "inner_energy_error_budget_relative": error_relative,
        "decision": (
            "TARGETED_INNER_POLE_NODE_ACCEPTED"
            if accepted
            else "TARGETED_INNER_POLE_NODE_REMAINS_UNRESOLVED"
        ),
        "runtime_seconds": time.perf_counter() - started,
        **{field: False for field in CLAIM_FIELDS},
    }
    atomic_json(paths["result"], result)
    return result


def repair_manifest_rows(
    inventory: list[dict[str, Any]],
    plan_sha256: str,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for target in inventory:
        epsilon_id = str(target["epsilon_id"])
        node_id = str(target["node_id"])
        complete = repair_complete(epsilon_id, node_id, plan_sha256)
        result = (
            read_json(repair_paths(epsilon_id, node_id)["result"])
            if complete
            else {}
        )
        rows.append(
            {
                **target,
                "repair_state": (
                    "COMPLETE_PASS"
                    if complete and bool(result["acceptance_passed"])
                    else ("COMPLETE_FAIL" if complete else "PENDING")
                ),
                "repair_result_path": str(
                    repair_paths(epsilon_id, node_id)["result"]
                ),
                "runtime_seconds": result.get("runtime_seconds", ""),
                **{field: False for field in CLAIM_FIELDS},
            }
        )
    return rows


def combined_result(
    epsilon_id: str,
    node_id: str,
    plan_sha256: str,
) -> tuple[dict[str, Any], str, Path]:
    parent_path = M5316.shard_paths(epsilon_id, node_id)["result"]
    parent = read_json(parent_path)
    if bool(parent["acceptance_passed"]):
        return parent, "PARENT_5316_PASS", parent_path
    repair_path = repair_paths(epsilon_id, node_id)["result"]
    if repair_complete(epsilon_id, node_id, plan_sha256):
        return read_json(repair_path), "REPAIRED_5317", repair_path
    return {}, "PENDING_REPAIR", repair_path


def combined_manifest_rows(plan_sha256: str) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for epsilon_id, epsilon in M5316.TARGET_REGULATORS:
        for node in M5316.base_plan():
            result, source_type, result_path = combined_result(
                epsilon_id, node["node_id"], plan_sha256
            )
            complete = bool(result)
            rows.append(
                {
                    "epsilon_id": epsilon_id,
                    "epsilon": epsilon,
                    **node,
                    "result_source": source_type,
                    "combined_state": (
                        "COMPLETE_PASS"
                        if complete and bool(result["acceptance_passed"])
                        else ("COMPLETE_FAIL" if complete else "PENDING")
                    ),
                    "node_result_path": str(result_path),
                    **{field: False for field in CLAIM_FIELDS},
                }
            )
    return rows


def aggregate_regulator(
    epsilon_id: str,
    epsilon: float,
    plan_sha256: str,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]] | None:
    plan = M5316.base_plan()
    selected = [
        combined_result(epsilon_id, node["node_id"], plan_sha256)[0]
        for node in plan
    ]
    if not all(result and bool(result["acceptance_passed"]) for result in selected):
        return None
    old = M5316.set_kernel_globals(epsilon_id, epsilon)
    try:
        outer, panels, metrics = M5312.aggregate_outer_integrals(plan, selected)
    finally:
        M5316.restore_kernel_globals(old)
    for row in outer:
        row["epsilon_id"] = epsilon_id
        row["epsilon"] = epsilon
        row["scan_checkpoint"] = CHECKPOINT
    for row in panels:
        row["epsilon_id"] = epsilon_id
        row["epsilon"] = epsilon
    return outer, panels, metrics


def source_rows() -> list[dict[str, str]]:
    paths = [
        Path(__file__).resolve(),
        SCRIPT_5316,
        RESULT_5316,
        MANIFEST_5316,
        CONTRACT_5312,
        NODE_PLAN_5312,
        DRY_RUN,
        FAILED_INVENTORY,
        PARENT_HASHES,
    ]
    return [{"path": str(path), "sha256": digest(path)} for path in paths]


def execute(runtime_limit_seconds: float) -> dict[str, Any]:
    M5312.set_below_normal_priority()
    mp.mp.dps = M5312.M5280.MP_DECIMAL_DIGITS
    M5312.M5301.configure_reused_pipeline()
    started = time.perf_counter()
    dry = dry_run()
    if not dry["acceptance_passed"]:
        raise RuntimeError("5317 dry run did not pass")
    inventory = read_csv(FAILED_INVENTORY)
    parent_bundle = dry["parent_shard_bundle_sha256"]
    plan_sha256 = repair_plan_sha256(parent_bundle)
    contract = read_csv(CONTRACT_5312)
    base_context = M5312.M5303.synthetic_context()
    multiplier = M5312.M5309.physical_multiplier()
    paused = False
    for target in inventory:
        epsilon_id = target["epsilon_id"]
        node_id = target["node_id"]
        if repair_complete(epsilon_id, node_id, plan_sha256):
            continue
        if time.perf_counter() - started >= runtime_limit_seconds:
            paused = True
            break
        epsilon = target_regulators()[epsilon_id]
        old = M5316.set_kernel_globals(epsilon_id, epsilon)
        try:
            result = repair_node(
                target,
                contract,
                plan_sha256,
                base_context,
                multiplier,
            )
        finally:
            M5316.restore_kernel_globals(old)
        atomic_json(
            STATUS,
            {
                "checkpoint": CHECKPOINT,
                "state": "RUNNING",
                "last_completed_epsilon_id": epsilon_id,
                "last_completed_node_id": node_id,
                "last_node_acceptance_passed": result["acceptance_passed"],
            },
        )
    repair_manifest = repair_manifest_rows(inventory, plan_sha256)
    combined_manifest = combined_manifest_rows(plan_sha256)
    write_csv(REPAIR_MANIFEST, repair_manifest, ["epsilon_id", "node_id"])
    write_csv(COMBINED_MANIFEST, combined_manifest, ["epsilon_id", "node_id"])
    fit_rows: list[dict[str, Any]] = []
    off_axis_rows: list[dict[str, Any]] = []
    classification_rows: list[dict[str, Any]] = []
    integral_rows: list[dict[str, Any]] = []
    for target in inventory:
        paths = repair_paths(target["epsilon_id"], target["node_id"])
        if not repair_complete(target["epsilon_id"], target["node_id"], plan_sha256):
            continue
        fit_rows.extend(read_csv(paths["fits"]))
        off_axis_rows.extend(read_csv(paths["off_axis"]))
        classification_rows.extend(read_csv(paths["classifications"]))
        integral_rows.extend(read_csv(paths["integrals"]))
    write_csv(
        MATERIAL_FITS,
        fit_rows,
        ["epsilon_id", "node_id", "term_id", "pole_id", "fit_row_type"],
    )
    write_csv(
        OFF_AXIS_AUDIT,
        off_axis_rows,
        ["epsilon_id", "node_id", "term_id", "pole_id"],
    )
    write_csv(
        CLASSIFICATIONS,
        classification_rows,
        ["node_id", "term_id", "pole_id", "pole_classification_resolved"],
    )
    write_csv(
        CELL_INTEGRALS,
        integral_rows,
        ["node_id", "contract_index", "energy_order"],
    )
    outer_rows: list[dict[str, Any]] = []
    panel_rows: list[dict[str, Any]] = []
    summaries = [M5316.E0025_summary()]
    for epsilon_id, epsilon in M5316.TARGET_REGULATORS:
        aggregate = aggregate_regulator(epsilon_id, epsilon, plan_sha256)
        if aggregate is None:
            summaries.append(
                {
                    "epsilon_id": epsilon_id,
                    "epsilon": epsilon,
                    "method": "TARGETED_INNER_REPAIR_PENDING",
                    "all_nodes_complete": False,
                    "all_nodes_pass": False,
                    "coarse_outer_gate_passes": False,
                    "finite_regulator_integral_accepted": False,
                    "failing_panel_ids": "PENDING",
                    "outer_error_relative": math.inf,
                    "inner_error_budget_relative": math.inf,
                    "fixed_decay_integral_real": 0.0,
                    "fixed_decay_integral_imaginary": 0.0,
                    "source_result_path": "",
                    **{field: False for field in CLAIM_FIELDS},
                }
            )
            continue
        local_outer, local_panels, metrics = aggregate
        outer_rows.extend(local_outer)
        panel_rows.extend(local_panels)
        failing_panels = [
            str(row["x_panel_index"])
            for row in local_panels
            if float(row["outer_Q2_Q4_relative_change"])
            > M5316.OUTER_CHANGE_LIMIT
        ]
        outer_gate = (
            float(metrics["outer_Q2_Q4_relative_change"])
            <= M5316.OUTER_CHANGE_LIMIT
            and float(metrics["outer_Q4_inner_energy_error_budget_relative"])
            <= M5316.INNER_ERROR_BUDGET_LIMIT
        )
        selected = complex(
            float(metrics["selected_E0025_fixed_decay_outer_soft_integral_real"]),
            float(
                metrics[
                    "selected_E0025_fixed_decay_outer_soft_integral_imaginary"
                ]
            ),
        )
        summaries.append(
            {
                "epsilon_id": epsilon_id,
                "epsilon": epsilon,
                "method": "POLE_SUBTRACTED_COARSE_PLUS_TARGETED_INNER_REPAIR",
                "all_nodes_complete": True,
                "all_nodes_pass": True,
                "coarse_outer_gate_passes": outer_gate,
                "finite_regulator_integral_accepted": outer_gate,
                "failing_panel_ids": "|".join(failing_panels),
                "outer_error_relative": metrics["outer_Q2_Q4_relative_change"],
                "inner_error_budget_relative": metrics[
                    "outer_Q4_inner_energy_error_budget_relative"
                ],
                **complex_fields("fixed_decay_integral", selected),
                "source_result_path": str(RESULT),
                **{field: False for field in CLAIM_FIELDS},
            }
        )
    write_csv(OUTER_TOTALS, outer_rows, ["epsilon_id", "outer_order", "energy_order"])
    write_csv(PANEL_CONVERGENCE, panel_rows, ["epsilon_id", "x_panel_index"])
    write_csv(REGULATOR_SUMMARY, summaries, ["epsilon_id"])
    all_repairs_complete = all(
        row["repair_state"] != "PENDING" for row in repair_manifest
    )
    all_repairs_pass = all_repairs_complete and all(
        row["repair_state"] == "COMPLETE_PASS" for row in repair_manifest
    )
    all_combined_pass = len(combined_manifest) == 216 and all(
        row["combined_state"] == "COMPLETE_PASS" for row in combined_manifest
    )
    if paused or not all_repairs_complete:
        decision = "TARGETED_INNER_POLE_RESOLUTION_PAUSED__RESUME_SAVED_REPAIRS"
    elif all_repairs_pass and all_combined_pass:
        decision = (
            "FOUR_REGULATOR_INNER_NODES_CLOSED__BUILD_EVENT_ALIGNED_OUTER_REPAIRS"
        )
    else:
        decision = "TARGETED_INNER_POLE_RESOLUTION_LOCALIZES_REMAINING_FAILURES"
    parent = read_json(RESULT_5316)
    formal_end = M5283.formal_inventory_digest()
    final_fit_rows = [
        row for row in fit_rows if row["fit_row_type"] == "FINAL_REFINED_SIMPLE_POLE_FIT"
    ]
    result = {
        "checkpoint": CHECKPOINT,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "mode": "targeted-inner-pole-resolution",
        "acceptance_passed": all_repairs_pass and all_combined_pass,
        "decision": decision,
        "parent_pass_node_count_reused": sum(
            row["result_source"] == "PARENT_5316_PASS" for row in combined_manifest
        ),
        "targeted_repair_node_count": len(repair_manifest),
        "completed_repair_node_count": sum(
            row["repair_state"] != "PENDING" for row in repair_manifest
        ),
        "passed_repair_node_count": sum(
            row["repair_state"] == "COMPLETE_PASS" for row in repair_manifest
        ),
        "combined_pass_node_count": sum(
            row["combined_state"] == "COMPLETE_PASS" for row in combined_manifest
        ),
        "material_refinement_target_count": len(
            {
                (row["epsilon_id"], row["node_id"])
                for row in final_fit_rows
            }
        ),
        "off_axis_raw_target_count": len(off_axis_rows),
        "maximum_material_fit_relative_residual": max(
            (float(row["fit_relative_residual"]) for row in final_fit_rows),
            default=math.inf,
        ),
        "maximum_material_holdout_relative_residual": max(
            (float(row["holdout_relative_residual"]) for row in final_fit_rows),
            default=math.inf,
        ),
        "maximum_material_residue_scale_change": max(
            (
                float(row["residue_fit_scale_relative_change"])
                for row in final_fit_rows
            ),
            default=math.inf,
        ),
        "maximum_material_second_order_suppression_ratio": max(
            (
                float(row["second_order_suppression_ratio"])
                for row in final_fit_rows
            ),
            default=math.inf,
        ),
        "regulator_summary_rows": summaries,
        "parent_shard_bundle_sha256": parent_bundle,
        "repair_plan_sha256": plan_sha256,
        "formalization_workbench_reference_digest": parent[
            "formalization_workbench_end_digest"
        ],
        "formalization_workbench_end_digest": formal_end,
        "formalization_workbench_modified_file_count": (
            0 if formal_end == parent["formalization_workbench_end_digest"] else -1
        ),
        "claim_boundary": {
            "valid_for_five_finite_regulator_fixed_decay_integrals": False,
            **{field: False for field in CLAIM_FIELDS},
            "reason": (
                "5317 closes only the four-regulator inner-node layer. Each "
                "coarse outer failure still requires event-aligned repair before "
                "a finite-regulator or regulator-zero claim."
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
                "COMPLETE_DIAGNOSTIC" if all_repairs_complete else "PAUSED_RESUMABLE"
            ),
            "decision": decision,
            "completed_repair_node_count": result["completed_repair_node_count"],
            "targeted_repair_node_count": len(repair_manifest),
        },
    )
    return result


def parent_hashes_unchanged() -> bool:
    recorded = read_csv(PARENT_HASHES)
    current = parent_hash_rows()
    recorded_lookup = {
        (row["epsilon_id"], row["node_id"]): row["parent_shard_bundle_sha256"]
        for row in recorded
    }
    return len(recorded) == len(current) == 216 and all(
        recorded_lookup.get((row["epsilon_id"], row["node_id"]))
        == row["parent_shard_bundle_sha256"]
        for row in current
    )


def render_document(result: dict[str, Any], passed: bool) -> None:
    lines = [
        "# 5317 - Targeted inner-pole resolution",
        "",
        "## Derivation",
        "",
        "For an approximate pole `p0` and exact simple pole `p*`,",
        "`R/(E-p*) = R/(E-p0) + R(p*-p0)/(E-p0)^2 + ...`.",
        "The normalized basis `r^2/(E-p)^2`, `r/(E-p)`, and powers of",
        "`u=(E-E0)/r` therefore gives the pole correction `delta p=R2/R1`",
        "without promoting a location error to a physical double pole. Independent",
        "interlaced holdout points test the derived correction.",
        "",
        "The sixteen small unresolved residues are not set to zero and are not",
        "subtracted. Their poles remain separated from the real energy contour, so",
        "the full raw integrand is retained and must pass the original Q4/Q8 gates.",
        "",
        "## Result",
        "",
        f"- parent pass nodes reused unchanged: `{result['parent_pass_node_count_reused']}`;",
        f"- targeted repair nodes passed: `{result['passed_repair_node_count']}` / `{result['targeted_repair_node_count']}`;",
        f"- combined inner nodes passed: `{result['combined_pass_node_count']}` / 216;",
        f"- maximum material fit residual: `{result['maximum_material_fit_relative_residual']:.12g}`;",
        f"- maximum independent holdout residual: `{result['maximum_material_holdout_relative_residual']:.12g}`;",
        f"- maximum residual pole-order ratio: `{result['maximum_material_second_order_suppression_ratio']:.12g}`;",
        f"- decision: **{result['decision']}**;",
        f"- validation: **{'PASS' if passed else 'FAIL'}**.",
        "",
        "| regulator | inner nodes | coarse failing panels | coarse value |",
        "|---|---:|---|---:|",
    ]
    for row in result["regulator_summary_rows"]:
        lines.append(
            "| {epsilon_id} | {nodes} | {panels} | {real:.9g} {imag:+.9g} i |".format(
                epsilon_id=row["epsilon_id"],
                nodes="pass" if row["all_nodes_pass"] else "pending",
                panels=row["failing_panel_ids"] or "-",
                real=float(row["fixed_decay_integral_real"]),
                imag=float(row["fixed_decay_integral_imaginary"]),
            )
        )
    lines.extend(
        [
            "",
            "## Claim boundary",
            "",
            "No finite-regulator ladder, regulator-zero, decay-angle, phase-space,",
            "UV, local-GR, or full-MTS claim follows until the named outer panels",
            "are repaired under their unchanged convergence gates.",
        ]
    )
    DOCUMENT.write_text("\n".join(lines) + "\n", encoding="utf-8")


def validate_outputs() -> dict[str, Any]:
    started = time.perf_counter()
    result = read_json(RESULT)
    dry = read_json(DRY_RUN)
    repair_manifest = read_csv(REPAIR_MANIFEST)
    combined = read_csv(COMBINED_MANIFEST)
    fits = read_csv(MATERIAL_FITS)
    off_axis = read_csv(OFF_AXIS_AUDIT)
    summaries = read_csv(REGULATOR_SUMMARY)
    final_fits = [
        row for row in fits if row["fit_row_type"] == "FINAL_REFINED_SIMPLE_POLE_FIT"
    ]
    source_current = all(
        Path(row["path"]).exists()
        and digest(Path(row["path"])) == row["sha256"]
        for row in result["source_files"]
    )
    gates = [
        validation_gate(
            "dry_run_identifies_exact_target_set",
            bool(dry["acceptance_passed"])
            and int(dry["parent_pass_node_count"]) == 198
            and int(dry["target_node_count"]) == 18,
            dry["decision"],
        ),
        validation_gate(
            "all_parent_5316_shards_unchanged",
            parent_hashes_unchanged()
            and result["parent_shard_bundle_sha256"]
            == dry["parent_shard_bundle_sha256"],
            "216 parent shard bundles rehashed",
        ),
        validation_gate(
            "all_eighteen_targeted_repairs_pass",
            len(repair_manifest) == 18
            and all(row["repair_state"] == "COMPLETE_PASS" for row in repair_manifest)
            and int(result["passed_repair_node_count"]) == 18,
            f"rows={len(repair_manifest)}",
        ),
        validation_gate(
            "combined_four_regulator_inner_layer_passes",
            len(combined) == 216
            and all(row["combined_state"] == "COMPLETE_PASS" for row in combined)
            and sum(row["result_source"] == "PARENT_5316_PASS" for row in combined)
            == 198
            and sum(row["result_source"] == "REPAIRED_5317" for row in combined)
            == 18,
            f"rows={len(combined)}",
        ),
        validation_gate(
            "two_material_poles_pass_fit_and_holdout_contract",
            len(final_fits) == 4
            and len({(row["epsilon_id"], row["node_id"]) for row in final_fits})
            == 2
            and all(
                parse_bool(row["refined_simple_pole_contract_passes"])
                and float(row["fit_relative_residual"])
                <= FIT_RELATIVE_RESIDUAL_LIMIT
                and float(row["holdout_relative_residual"])
                <= HOLDOUT_RELATIVE_RESIDUAL_LIMIT
                and float(row["residue_fit_scale_relative_change"])
                <= RESIDUE_SCALE_CHANGE_LIMIT
                and float(row["second_order_suppression_ratio"])
                <= SECOND_ORDER_SUPPRESSION_LIMIT
                for row in final_fits
            ),
            f"final_fit_rows={len(final_fits)}",
        ),
        validation_gate(
            "sixteen_off_axis_poles_use_raw_direct_quadrature",
            len(off_axis) == 16
            and all(
                parse_bool(row["contour_separation_reliable"])
                and parse_bool(row["raw_integrand_retained_without_subtraction"])
                and parse_bool(row["raw_node_acceptance_passed"])
                and not parse_bool(row["valid_for_rigorous_residue_bound"])
                for row in off_axis
            ),
            f"rows={len(off_axis)}",
        ),
        validation_gate(
            "five_regulators_have_explicit_nonclaim_status",
            len(summaries) == 5
            and {row["epsilon_id"] for row in summaries}
            == {"E0025", "E005", "E010", "E020", "E040"}
            and all(
                parse_bool(row["finite_regulator_integral_accepted"])
                or bool(row["failing_panel_ids"])
                for row in summaries
            ),
            f"rows={len(summaries)}",
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
            "source_paths_and_hashes_current",
            source_current,
            f"rows={len(result['source_files'])}",
        ),
        validation_gate(
            "scripts_cache_absent",
            not (SCRIPTS / "__pycache__").exists(),
            str(SCRIPTS / "__pycache__"),
        ),
        validation_gate(
            "broader_claims_locked_false",
            not bool(
                result["claim_boundary"][
                    "valid_for_five_finite_regulator_fixed_decay_integrals"
                ]
            )
            and all(
                not bool(result["claim_boundary"][field])
                for field in CLAIM_FIELDS
            ),
            "inner repair only",
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
            "VALIDATED_FOUR_REGULATOR_INNER_NODE_RESOLUTION"
            if passed
            else "TARGETED_INNER_POLE_RESOLUTION_VALIDATION_FAILED"
        ),
        "runtime_seconds": time.perf_counter() - started,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", choices=("dry-run", "run", "validate"), required=True)
    parser.add_argument("--max-runtime-hours", type=float, default=1.5)
    return parser.parse_args()


def main() -> int:
    M5312.set_below_normal_priority()
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
