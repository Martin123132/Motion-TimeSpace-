from __future__ import annotations

import argparse
import cmath
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
SOURCE = FUNCTIONAL_RG / "5314"
SHARDS = SOURCE / "shards"

SCRIPT_5313 = SCRIPTS / "Y5_R2FR_5313_material_pole_support_event_aligned_outer_refinement.py"
RESULT_5313 = FUNCTIONAL_RG / "5313" / "material_pole_support_event_refinement_result.json"
VALIDATION_5313 = FUNCTIONAL_RG / "5313" / "material_pole_support_event_refinement_validation.csv"
CONTRACT_5312 = FUNCTIONAL_RG / "5312" / "reduced_fixed_decay_cubature_contract.csv"
SUPPORT_EVENTS_5313 = FUNCTIONAL_RG / "5313" / "P9_material_pole_support_events.csv"
TOPOLOGY_SCAN_5313 = FUNCTIONAL_RG / "5313" / "P9_material_pole_support_topology_scan.csv"

DRY_RUN = SOURCE / "refined_simple_pole_endpoint_collar_dry_run.json"
POLE_ORDER_AUDIT = SOURCE / "shared_branch_pole_order_discrimination.csv"
BRANCH_EVENTS = SOURCE / "shared_branch_outer_events.csv"
ADAPTIVE_PANELS = SOURCE / "endpoint_collar_adaptive_outer_panels.csv"
NODE_MANIFEST = SOURCE / "endpoint_collar_node_manifest.csv"
ALL_POLE_FITS = SOURCE / "endpoint_collar_refined_pole_fits.csv"
ALL_CELL_INTEGRALS = SOURCE / "endpoint_collar_cell_integrals.csv"
CONVERGENCE = SOURCE / "endpoint_collar_outer_convergence.csv"
RESULT = SOURCE / "refined_simple_pole_endpoint_collar_result.json"
VALIDATION = SOURCE / "refined_simple_pole_endpoint_collar_validation.csv"
RESIDUAL_VALIDATION = RESIDUALS / "P8_Y5_BRR545_5314_VALIDATION.csv"
STATUS = SOURCE / "status.json"
DOCUMENT = POST / "5314-Y5-R2FR-refined-simple-pole-endpoint-collar-integrator.md"

CHECKPOINT = 5314
PARENT_CHECKPOINT = 5313
MARKER = "MTS_5314_REFINED_SIMPLE_POLE_ENDPOINT_COLLAR_INTEGRATOR"
REVISION = "refined-simple-pole-endpoint-collar-integrator-v1"
NODE_REVISION = "refined-simple-pole-endpoint-collar-node-v1"
TARGET_PANEL_INDEX = 9
TARGET_CONTRACT_INDEX = 29
TARGET_TERM_ID = "MC04_SM_DM"
TARGET_PRIMARY_SURFACE_ID = "direct:shared:s13"
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
MAXIMUM_POLE_REFINEMENTS = 4
POLE_REFINEMENT_TOLERANCE = 1.0e-11
FIT_RELATIVE_RESIDUAL_LIMIT = 1.0e-5
RESIDUE_SCALE_CHANGE_LIMIT = 1.0e-3
SECOND_ORDER_SUPPRESSION_LIMIT = 1.0e-4
ENERGY_ORDERS = (8, 12)
ENERGY_PANEL_SUBDIVISIONS = 32
INNER_RELATIVE_CHANGE_LIMIT = 5.0e-4
INNER_ERROR_BUDGET_LIMIT = 1.0e-3
OUTER_ORDERS = (2, 4)
LOCAL_OUTER_CHANGE_LIMIT = 5.0e-3
GLOBAL_OUTER_ERROR_BUDGET_LIMIT = 1.0e-2
MAXIMUM_ADAPTIVE_DEPTH = 6
EVENT_BISECTION_STEPS = 16
DEFAULT_RUNTIME_LIMIT_SECONDS = 2.5 * 3600.0
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


M5313 = load_module("mts_5313_for_5314", SCRIPT_5313)
M5312 = M5313.M5312
M5309 = M5312.M5309
M5308 = M5312.M5308
M5305 = M5312.M5305
M5303 = M5312.M5303
M5301 = M5312.M5301
M5283 = M5312.M5283
M5280 = M5312.M5280
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


def source_rows() -> list[dict[str, str]]:
    paths = (
        Path(__file__).resolve(),
        SCRIPT_5313,
        RESULT_5313,
        VALIDATION_5313,
        CONTRACT_5312,
        SUPPORT_EVENTS_5313,
        TOPOLOGY_SCAN_5313,
    )
    return [{"path": str(path), "sha256": digest(path)} for path in paths]


def target_panel_limits() -> tuple[float, float]:
    row = next(
        row for row in read_csv(CONTRACT_5312)
        if int(row["contract_index"]) == TARGET_CONTRACT_INDEX
    )
    return (
        float(row["lower_absolute_soft_cosine"]),
        float(row["upper_absolute_soft_cosine"]),
    )


def support_event_coordinates() -> tuple[float, float]:
    rows = read_csv(SUPPORT_EVENTS_5313)
    return (
        next(
            float(row["event_absolute_soft_cosine"])
            for row in rows if row["event_type"] == "SUPPORT_ENTRY"
        ),
        next(
            float(row["event_absolute_soft_cosine"])
            for row in rows if row["event_type"] == "SUPPORT_EXIT"
        ),
    )


def branch_death_bracket() -> tuple[dict[str, str], dict[str, str]]:
    rows = sorted(
        read_csv(TOPOLOGY_SCAN_5313),
        key=lambda row: float(row["absolute_soft_cosine"]),
    )
    for left, right in zip(rows[:-1], rows[1:]):
        if parse_bool(left["target_branch_exists"]) and not parse_bool(
            right["target_branch_exists"]
        ):
            return left, right
    raise RuntimeError("no shared-branch death bracket")


def dry_run() -> dict[str, Any]:
    SOURCE.mkdir(parents=True, exist_ok=True)
    parent = read_json(RESULT_5313)
    validation = read_csv(VALIDATION_5313)
    entry, exit_coordinate = support_event_coordinates()
    left, right = branch_death_bracket()
    checks = {
        "parent_5313_diagnosis_validated": (
            all(parse_bool(row["passed"]) for row in validation)
            and bool(parent["shared_branch_double_laurent_preflight_passed"])
            and parent["decision"]
            == (
                "SHARED_BRANCH_SECOND_ORDER_LAURENT_TERM_DERIVED__"
                "BUILD_DOUBLE_POLE_AND_ENDPOINT_COLLAR_SUBTRACTION"
            )
        ),
        "support_entry_and_exit_are_ordered": entry < exit_coordinate,
        "shared_branch_death_is_bracketed_after_support_exit": (
            exit_coordinate
            < float(left["absolute_soft_cosine"])
            < float(right["absolute_soft_cosine"])
        ),
        "refined_simple_pole_and_collar_contract_is_stricter": (
            ENERGY_ORDERS == (8, 12)
            and ENERGY_PANEL_SUBDIVISIONS == 32
            and MAXIMUM_ADAPTIVE_DEPTH > M5313.MAXIMUM_ADAPTIVE_DEPTH
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
        "decision": (
            "DRY_RUN_ACCEPTED__REFINE_SIMPLE_POLE_AND_RUN_ENDPOINT_COLLARS"
            if accepted
            else "DRY_RUN_REQUIRES_REPAIR"
        ),
        "runtime_seconds": 0.0,
        **{field: False for field in CLAIM_FIELDS},
    }
    atomic_json(DRY_RUN, result)
    return result


def unmasked_component_evaluator(base_context: dict[str, Any]) -> Any:
    cache: dict[
        tuple[float, float, int, int], dict[str, Any]
    ] = {}

    def evaluate(
        energy: float,
        coordinate: float,
        soft_sign: int,
        decay_sign: int,
    ) -> dict[str, Any]:
        key = (float(energy), float(coordinate), soft_sign, decay_sign)
        if key in cache:
            return cache[key]
        context = M5308.M5302.local_context(
            base_context,
            coordinate,
            soft_sign,
            decay_sign,
        )
        event = dict(context["source_event"])
        event["soft_energy"] = energy
        inventory = context["inventories"][M5312.EPSILON_ID]
        target = inventory["target"]
        component = inventory["components"]["MC04"]
        rationals = M5280.M5274.M5231.root_rationals(event, target)
        selection = M5280.M5279.algebraic_component_selector(
            event,
            target,
            component,
            rationals,
        )
        labels = selection["selected_labels"]
        mask_active, orientation, _, _ = M5280.M5277.exact_mask_orientation(
            labels,
            event,
            context["surfaces"],
        )
        high_precision_event = M5280.M5275.event_as_mp(event)
        relative_root, root_residual, refinement_distance = (
            M5280.M5275.refine_relative_root(
                high_precision_event,
                inventory["high_precision_target"],
                labels,
                selection["selected_root"],
            )
        )
        coefficient = M5280.coefficient_at_exponent(
            high_precision_event,
            inventory["high_precision_target"],
            labels,
            relative_root,
            M5280.FAST_DELTA_EXPONENT,
        )
        collision_jacobian = M5280.M5277.mp_collision_jacobian(
            high_precision_event,
            inventory["high_precision_target"],
            labels,
            relative_root,
        )
        winding_delta = M5280.M5277.source_winding_delta(
            component,
            selection["selected_role"],
        )
        residue = M5280.M5277.residue_from_coefficient(
            coefficient["total_coefficient"],
            relative_root,
            coefficient["global_root"],
            collision_jacobian,
            orientation,
            winding_delta,
        )
        cache[key] = {
            "value": complex(residue),
            "mask_active": bool(mask_active),
            "orientation": int(orientation),
            "selected_labels": "|".join(labels),
            "selected_role": selection["selected_role"],
            "root_equation_residual": float(root_residual),
            "root_refinement_chordal_distance": float(refinement_distance),
        }
        return cache[key]

    return evaluate


def target_branch_row(
    coordinate: float,
    cells: list[dict[str, Any]],
) -> dict[str, Any] | None:
    supports = M5312.merged_term_supports(cells)
    node = {
        "node_id": f"SCAN_{coordinate:.17g}",
        "x_panel_index": TARGET_PANEL_INDEX,
        "outer_order": 0,
        "absolute_soft_cosine": coordinate,
    }
    rows = M5312.scan_term_poles(
        node,
        TARGET_TERM_ID,
        supports[TARGET_TERM_ID],
    )
    selected = [
        row for row in rows
        if row["primary_surface_id"] == TARGET_PRIMARY_SURFACE_ID
    ]
    if len(selected) > 1:
        raise RuntimeError(f"multiple shared-branch poles at {coordinate}")
    if not selected:
        return None
    support = next(
        value for value in supports[TARGET_TERM_ID]
        if TARGET_CONTRACT_INDEX in value["contracts"]
    )
    return {
        **selected[0],
        "support_energy_lower": float(support["lower"]),
        "support_energy_upper": float(support["upper"]),
    }


def pole_side(pole: complex, lower: float, upper: float) -> str:
    if pole.real < lower:
        return "BELOW_SUPPORT"
    if pole.real > upper:
        return "ABOVE_SUPPORT"
    return "INSIDE_SUPPORT"


def pole_boundary_distance(pole: complex, lower: float, upper: float) -> float:
    side = pole_side(pole, lower, upper)
    if side == "BELOW_SUPPORT":
        return lower - pole.real
    if side == "ABOVE_SUPPORT":
        return pole.real - upper
    return min(pole.real - lower, upper - pole.real)


def fit_radius(pole: complex, lower: float, upper: float) -> float:
    distance = pole_boundary_distance(pole, lower, upper)
    if distance <= 1.0e-12:
        return 0.0
    maximum_sample_unit = max(abs(value) for value in FIT_UNITS)
    boundary_safe = 0.8 * distance / (
        maximum_sample_unit * max(FIT_SCALES)
    )
    return min(
        max(8.0 * abs(pole.imag), 2.0e-6),
        boundary_safe,
    )


def generalized_laurent_fit(
    coordinate: float,
    pole: complex,
    lower: float,
    upper: float,
    fit_scale: float,
    evaluate_unmasked: Any,
) -> dict[str, Any]:
    radius = fit_radius(pole, lower, upper)
    if radius <= 0.0:
        raise RuntimeError("nonpositive refined-pole fit radius")
    center = pole.real
    matrix_rows: list[list[complex]] = []
    values: list[complex] = []
    metadata: list[dict[str, Any]] = []
    specification = M5308.SURFACE_LOOKUP[TARGET_TERM_ID]
    for unit in FIT_UNITS:
        energy = center + unit * fit_scale * radius
        evaluation = evaluate_unmasked(
            energy,
            coordinate,
            int(specification["soft_sign"]),
            int(specification["decay_sign"]),
        )
        delta = energy - center
        matrix_rows.append(
            [
                1.0 / (energy - pole) ** 2,
                1.0 / (energy - pole),
                *[
                    complex(delta**power)
                    for power in range(FIT_BACKGROUND_DEGREE + 1)
                ],
            ]
        )
        values.append(evaluation["value"])
        metadata.append(evaluation)
    matrix = np.asarray(matrix_rows, dtype=np.complex128)
    vector = np.asarray(values, dtype=np.complex128)
    coefficients, _, _, _ = np.linalg.lstsq(matrix, vector, rcond=None)
    predicted = matrix @ coefficients
    residual = float(
        np.linalg.norm(predicted - vector)
        / max(np.linalg.norm(vector), 1.0)
    )
    return {
        "fit_scale": fit_scale,
        "fit_radius": radius,
        "fit_sample_count": len(FIT_UNITS),
        "fit_relative_residual": residual,
        "second_order_coefficient": complex(coefficients[0]),
        "simple_residue": complex(coefficients[1]),
        "fit_mask_state_count": len(
            {bool(row["mask_active"]) for row in metadata}
        ),
        "fit_orientation_count": len(
            {int(row["orientation"]) for row in metadata}
        ),
        "fit_label_count": len(
            {str(row["selected_labels"]) for row in metadata}
        ),
        "maximum_root_equation_residual": max(
            float(row["root_equation_residual"]) for row in metadata
        ),
        "maximum_root_refinement_chordal_distance": max(
            float(row["root_refinement_chordal_distance"])
            for row in metadata
        ),
    }


def refine_simple_pole(
    coordinate: float,
    source: dict[str, Any],
    evaluate_unmasked: Any,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    lower = float(source["support_energy_lower"])
    upper = float(source["support_energy_upper"])
    geometric = complex(
        float(source["pole_real"]),
        float(source["pole_imaginary"]),
    )
    refined = geometric
    iteration_rows: list[dict[str, Any]] = []
    for iteration in range(1, MAXIMUM_POLE_REFINEMENTS + 1):
        fit = generalized_laurent_fit(
            coordinate,
            refined,
            lower,
            upper,
            1.0,
            evaluate_unmasked,
        )
        residue = fit["simple_residue"]
        correction = (
            fit["second_order_coefficient"] / residue
            if abs(residue) > 0.0
            else complex(math.inf, math.inf)
        )
        iteration_rows.append(
            {
                "fit_row_type": "POLE_REFINEMENT_ITERATION",
                "pole_refinement_iteration": iteration,
                **complex_fields("input_pole", refined),
                **complex_fields(
                    "second_order_coefficient_R2",
                    fit["second_order_coefficient"],
                ),
                **complex_fields("simple_residue_R1", residue),
                **complex_fields("pole_correction_R2_over_R1", correction),
                "fit_relative_residual": fit["fit_relative_residual"],
                "fit_radius": fit["fit_radius"],
            }
        )
        if not math.isfinite(abs(correction)):
            break
        refined += correction
        if abs(correction) <= POLE_REFINEMENT_TOLERANCE:
            break
    final_fits = [
        generalized_laurent_fit(
            coordinate,
            refined,
            lower,
            upper,
            scale,
            evaluate_unmasked,
        )
        for scale in FIT_SCALES
    ]
    first, second = final_fits
    residue_change = relative_complex_change(
        first["simple_residue"], second["simple_residue"]
    )
    second_order_ratio = max(
        abs(row["second_order_coefficient"])
        / max(
            abs(row["simple_residue"])
            * max(abs(refined.imag), row["fit_radius"], 1.0e-9),
            1.0e-300,
        )
        for row in final_fits
    )
    contract_passes = (
        all(
            row["fit_mask_state_count"] == 1
            and row["fit_orientation_count"] == 1
            and row["fit_label_count"] == 1
            and row["fit_relative_residual"]
            <= FIT_RELATIVE_RESIDUAL_LIMIT
            for row in final_fits
        )
        and residue_change <= RESIDUE_SCALE_CHANGE_LIMIT
        and second_order_ratio <= SECOND_ORDER_SUPPRESSION_LIMIT
    )
    final_rows: list[dict[str, Any]] = []
    for fit in final_fits:
        final_rows.append(
            {
                "fit_row_type": "FINAL_REFINED_SIMPLE_POLE_FIT",
                "pole_refinement_iteration": len(iteration_rows),
                "fit_scale": fit["fit_scale"],
                "fit_radius": fit["fit_radius"],
                "fit_sample_count": fit["fit_sample_count"],
                **complex_fields("refined_pole", refined),
                **complex_fields(
                    "geometric_to_refined_pole_shift",
                    refined - geometric,
                ),
                **complex_fields(
                    "second_order_coefficient_R2",
                    fit["second_order_coefficient"],
                ),
                **complex_fields("simple_residue_R1", fit["simple_residue"]),
                "fit_relative_residual": fit["fit_relative_residual"],
                "fit_mask_state_count": fit["fit_mask_state_count"],
                "fit_orientation_count": fit["fit_orientation_count"],
                "fit_label_count": fit["fit_label_count"],
                "residue_fit_scale_relative_change": residue_change,
                "second_order_suppression_ratio": second_order_ratio,
                "refined_simple_pole_contract_passes": contract_passes,
            }
        )
    selected = {
        "geometric_pole": geometric,
        "refined_pole": refined,
        "selected_residue": second["simple_residue"],
        "pole_side": pole_side(refined, lower, upper),
        "support_energy_lower": lower,
        "support_energy_upper": upper,
        "fit_relative_residual": max(
            row["fit_relative_residual"] for row in final_fits
        ),
        "residue_fit_scale_relative_change": residue_change,
        "second_order_suppression_ratio": second_order_ratio,
        "contract_passes": contract_passes,
    }
    return selected, iteration_rows + final_rows


def energy_panels(
    lower: float,
    upper: float,
    refined_pole: complex | None,
) -> list[tuple[float, float]]:
    points = {lower, upper}
    points.update(
        lower + index * (upper - lower) / ENERGY_PANEL_SUBDIVISIONS
        for index in range(ENERGY_PANEL_SUBDIVISIONS + 1)
    )
    if refined_pole is not None:
        side = pole_side(refined_pole, lower, upper)
        if side == "INSIDE_SUPPORT":
            center = refined_pole.real
            core = max(abs(refined_pole.imag), 1.0e-7)
            for scale in (0.0, 0.5, 1.0, 2.0, 4.0, 8.0, 16.0, 32.0, 64.0):
                points.add(max(lower, min(upper, center - scale * core)))
                points.add(max(lower, min(upper, center + scale * core)))
        else:
            boundary = upper if side == "ABOVE_SUPPORT" else lower
            distance = abs(refined_pole.real - boundary)
            core = max(distance, abs(refined_pole.imag), 1.0e-7)
            for scale in (0.0, 0.25, 0.5, 1.0, 2.0, 4.0, 8.0, 16.0):
                point = (
                    boundary - scale * core
                    if side == "ABOVE_SUPPORT"
                    else boundary + scale * core
                )
                points.add(max(lower, min(upper, point)))
    coordinates = sorted(points)
    return [
        (left, right)
        for left, right in zip(coordinates[:-1], coordinates[1:])
        if right - left > 1.0e-15
    ]


def integrate_node(
    node: dict[str, Any],
    contract: list[dict[str, str]],
    plan_sha256: str,
    branch_death: float,
    base_context: dict[str, Any],
    multiplier: float,
) -> dict[str, Any]:
    started = time.perf_counter()
    paths = shard_paths(node["node_id"])
    paths["root"].mkdir(parents=True, exist_ok=True)
    coordinate = float(node["absolute_soft_cosine"])
    cells = [
        M5312.cell_geometry(row, coordinate)
        for row in contract
        if int(row["x_panel_index"]) == TARGET_PANEL_INDEX
        and int(row["reduced_MC04_term_count"]) > 0
    ]
    evaluate_masked = M5305.component_evaluator(base_context)
    pole_source = (
        target_branch_row(coordinate, cells)
        if coordinate <= branch_death + 1.0e-8
        else None
    )
    fit_rows: list[dict[str, Any]] = []
    fit_contract: dict[str, Any] | None = None
    if pole_source is not None:
        evaluate_unmasked = unmasked_component_evaluator(base_context)
        try:
            fit_contract, local_rows = refine_simple_pole(
                coordinate,
                pole_source,
                evaluate_unmasked,
            )
            for row in local_rows:
                fit_rows.append(
                    {
                        "node_id": node["node_id"],
                        "absolute_soft_cosine": coordinate,
                        "term_id": TARGET_TERM_ID,
                        "primary_surface_id": TARGET_PRIMARY_SURFACE_ID,
                        **row,
                        **{field: False for field in CLAIM_FIELDS},
                    }
                )
        except Exception as error:
            fit_contract = {
                "contract_passes": False,
                "failure_reason": f"{type(error).__name__}: {error}",
            }
    integral_rows: list[dict[str, Any]] = []
    node_totals = {order: 0.0j for order in ENERGY_ORDERS}
    inactive_count = 0
    for cell in cells:
        lower = float(cell["energy_lower"])
        upper = float(cell["energy_upper"])
        coefficients = cell["coefficients"]
        use_subtraction = (
            TARGET_TERM_ID in coefficients
            and fit_contract is not None
            and bool(fit_contract["contract_passes"])
        )
        refined_pole = (
            complex(fit_contract["refined_pole"])
            if use_subtraction
            else (
                complex(
                    float(pole_source["pole_real"]),
                    float(pole_source["pole_imaginary"]),
                )
                if TARGET_TERM_ID in coefficients and pole_source is not None
                else None
            )
        )
        selected_residue = (
            complex(fit_contract["selected_residue"])
            if use_subtraction
            else 0.0j
        )
        analytic = (
            selected_residue
            * (
                cmath.log(upper - refined_pole)
                - cmath.log(lower - refined_pole)
            )
            if use_subtraction and refined_pole is not None
            else 0.0j
        )
        panels = energy_panels(lower, upper, refined_pole)

        def raw_value(energy: float) -> complex:
            nonlocal inactive_count
            total = 0.0j
            for term_id, coefficient in coefficients.items():
                specification = M5308.SURFACE_LOOKUP[term_id]
                value, active = evaluate_masked(
                    M5312.EPSILON_ID,
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
            if not use_subtraction or refined_pole is None:
                return 0.0j
            return selected_residue / (energy - refined_pole)

        for order in ENERGY_ORDERS:
            nodes, weights = np.polynomial.legendre.leggauss(order)
            regular = 0.0j
            for panel_lower, panel_upper in panels:
                half = 0.5 * (panel_upper - panel_lower)
                midpoint = 0.5 * (panel_upper + panel_lower)
                for local_node, weight in zip(nodes, weights):
                    energy = midpoint + half * float(local_node)
                    regular += (
                        half
                        * float(weight)
                        * (raw_value(energy) - singular_value(energy))
                    )
            corrected = multiplier * (regular + analytic)
            node_totals[order] += corrected
            integral_rows.append(
                {
                    "node_id": node["node_id"],
                    "absolute_soft_cosine": coordinate,
                    "contract_index": cell["contract_index"],
                    "energy_order": order,
                    "energy_panel_count": len(panels),
                    "refined_pole_subtraction_applied": use_subtraction,
                    "refined_pole_side": (
                        fit_contract["pole_side"] if use_subtraction else ""
                    ),
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
    error_budget = sum(
        abs(values[ENERGY_ORDERS[1]] - values[ENERGY_ORDERS[0]])
        for values in by_cell.values()
    )
    error_budget_relative = error_budget / max(
        abs(node_totals[ENERGY_ORDERS[1]]), 1.0e-12
    )
    branch_inside_support = bool(
        pole_source is not None
        and float(pole_source["support_energy_lower"])
        < float(pole_source["pole_real"])
        < float(pole_source["support_energy_upper"])
    )
    fit_required_and_passes = (
        not branch_inside_support
        or (
            fit_contract is not None
            and bool(fit_contract["contract_passes"])
        )
    )
    accepted = (
        inactive_count == 0
        and node_change <= INNER_RELATIVE_CHANGE_LIMIT
        and error_budget_relative <= INNER_ERROR_BUDGET_LIMIT
        and fit_required_and_passes
    )
    write_csv(
        paths["fits"],
        fit_rows,
        ["node_id", "fit_row_type", "fit_scale"],
    )
    write_csv(
        paths["integrals"],
        integral_rows,
        ["node_id", "contract_index", "energy_order"],
    )
    result = {
        "checkpoint": CHECKPOINT,
        "node_revision": NODE_REVISION,
        "node_plan_sha256": plan_sha256,
        "node_id": node["node_id"],
        "x_panel_index": TARGET_PANEL_INDEX,
        "outer_order": int(node["outer_order"]),
        "absolute_soft_cosine": coordinate,
        "mapped_outer_weight": float(node["mapped_outer_weight"]),
        "node_complete": True,
        "acceptance_passed": accepted,
        "target_branch_exists": pole_source is not None,
        "target_branch_inside_support": branch_inside_support,
        "refined_simple_pole_contract_passes": (
            bool(fit_contract["contract_passes"])
            if fit_contract is not None
            else False
        ),
        "refined_pole_subtraction_applied": bool(
            fit_contract is not None and fit_contract.get("contract_passes")
        ),
        "refined_pole_side": (
            fit_contract.get("pole_side", "")
            if fit_contract is not None
            else ""
        ),
        "fit_failure_reason": (
            fit_contract.get("failure_reason", "")
            if fit_contract is not None
            else ""
        ),
        "inactive_selected_term_count": inactive_count,
        **complex_fields("inner_energy_Q8", node_totals[8]),
        **complex_fields("inner_energy_Q12", node_totals[12]),
        **complex_fields("selected_inner_energy", node_totals[12]),
        "inner_Q8_Q12_relative_change": node_change,
        "inner_energy_error_budget_absolute": error_budget,
        "inner_energy_error_budget_relative": error_budget_relative,
        "decision": (
            "REFINED_POLE_ENDPOINT_COLLAR_NODE_ACCEPTED"
            if accepted
            else "REFINED_POLE_ENDPOINT_COLLAR_NODE_REQUIRES_REFINEMENT"
        ),
        "runtime_seconds": time.perf_counter() - started,
        **{field: False for field in CLAIM_FIELDS},
    }
    atomic_json(paths["result"], result)
    return result


def branch_death_event(contract: list[dict[str, str]]) -> dict[str, Any]:
    left_source, right_source = branch_death_bracket()
    left = float(left_source["absolute_soft_cosine"])
    right = float(right_source["absolute_soft_cosine"])
    cache = M5313.load_scan_cache()
    M5313.STATUS = SOURCE / "branch_death_scan_status.json"
    for _ in range(EVENT_BISECTION_STEPS):
        midpoint = 0.5 * (left + right)
        state = M5313.scan_state(midpoint, contract, cache)
        if bool(state["target_branch_exists"]):
            left = midpoint
        else:
            right = midpoint
    return {
        "event_id": "E03",
        "event_type": "SHARED_BRANCH_DEATH",
        "event_absolute_soft_cosine": 0.5 * (left + right),
        "left_bracket_absolute_soft_cosine": left,
        "right_bracket_absolute_soft_cosine": right,
        "final_bracket_width": right - left,
        "valid_for_endpoint_collar_outer_partition": True,
        **{field: False for field in CLAIM_FIELDS},
    }


def all_branch_events(contract: list[dict[str, str]]) -> list[dict[str, Any]]:
    entry, exit_coordinate = support_event_coordinates()
    death = branch_death_event(contract)
    rows = [
        {
            "event_id": "E01",
            "event_type": "SUPPORT_ENTRY",
            "event_absolute_soft_cosine": entry,
            "valid_for_endpoint_collar_outer_partition": True,
            **{field: False for field in CLAIM_FIELDS},
        },
        {
            "event_id": "E02",
            "event_type": "SUPPORT_EXIT",
            "event_absolute_soft_cosine": exit_coordinate,
            "valid_for_endpoint_collar_outer_partition": True,
            **{field: False for field in CLAIM_FIELDS},
        },
        death,
    ]
    write_csv(BRANCH_EVENTS, rows)
    return rows


def plan_sha256(events: list[dict[str, Any]]) -> str:
    payload = {
        "revision": REVISION,
        "contract_sha256": digest(CONTRACT_5312),
        "events": [
            (row["event_type"], row["event_absolute_soft_cosine"])
            for row in events
        ],
    }
    return hashlib.sha256(
        json.dumps(payload, sort_keys=True).encode("utf-8")
    ).hexdigest()


def initial_panels(events: list[dict[str, Any]]) -> list[dict[str, Any]]:
    lower, upper = target_panel_limits()
    boundaries = [
        lower,
        *sorted(float(row["event_absolute_soft_cosine"]) for row in events),
        upper,
    ]
    return [
        {
            "initial_panel_index": index,
            "adaptive_panel_id": f"B{index:02d}",
            "adaptive_depth": 0,
            "parent_adaptive_panel_id": "",
            "lower_absolute_soft_cosine": left,
            "upper_absolute_soft_cosine": right,
        }
        for index, (left, right) in enumerate(
            zip(boundaries[:-1], boundaries[1:]), start=1
        )
    ]


def panel_nodes(panel: dict[str, Any]) -> list[dict[str, Any]]:
    lower = float(panel["lower_absolute_soft_cosine"])
    upper = float(panel["upper_absolute_soft_cosine"])
    half = 0.5 * (upper - lower)
    midpoint = 0.5 * (upper + lower)
    rows: list[dict[str, Any]] = []
    for order in OUTER_ORDERS:
        nodes, weights = np.polynomial.legendre.leggauss(order)
        for index, (node, weight) in enumerate(zip(nodes, weights), start=1):
            rows.append(
                {
                    "node_id": (
                        f"P09_{panel['adaptive_panel_id']}_"
                        f"Q{order:02d}_N{index:02d}"
                    ),
                    "x_panel_index": TARGET_PANEL_INDEX,
                    "outer_order": order,
                    "local_node_index": index,
                    "lower_absolute_soft_cosine": lower,
                    "upper_absolute_soft_cosine": upper,
                    "absolute_soft_cosine": midpoint + half * float(node),
                    "mapped_outer_weight": half * float(weight),
                    **{field: False for field in CLAIM_FIELDS},
                }
            )
    return rows


def shard_paths(node_id: str) -> dict[str, Path]:
    root = SHARDS / node_id
    return {
        "root": root,
        "fits": root / "refined_pole_fits.csv",
        "integrals": root / "cell_integrals.csv",
        "result": root / "result.json",
    }


def shard_complete(node: dict[str, Any], expected_plan_sha256: str) -> bool:
    paths = shard_paths(node["node_id"])
    if not all(path.exists() for key, path in paths.items() if key != "root"):
        return False
    try:
        result = read_json(paths["result"])
        read_csv(paths["fits"])
        read_csv(paths["integrals"])
    except Exception:
        return False
    return (
        result.get("node_revision") == NODE_REVISION
        and result.get("node_plan_sha256") == expected_plan_sha256
        and result.get("node_id") == node["node_id"]
        and bool(result.get("node_complete"))
    )


def split_panel(panel: dict[str, Any]) -> tuple[dict[str, Any], dict[str, Any]]:
    midpoint = 0.5 * (
        float(panel["lower_absolute_soft_cosine"])
        + float(panel["upper_absolute_soft_cosine"])
    )
    depth = int(panel["adaptive_depth"]) + 1
    common = {
        "initial_panel_index": panel["initial_panel_index"],
        "adaptive_depth": depth,
        "parent_adaptive_panel_id": panel["adaptive_panel_id"],
    }
    return (
        {
            **common,
            "adaptive_panel_id": f"{panel['adaptive_panel_id']}L",
            "lower_absolute_soft_cosine": panel[
                "lower_absolute_soft_cosine"
            ],
            "upper_absolute_soft_cosine": midpoint,
        },
        {
            **common,
            "adaptive_panel_id": f"{panel['adaptive_panel_id']}R",
            "lower_absolute_soft_cosine": midpoint,
            "upper_absolute_soft_cosine": panel[
                "upper_absolute_soft_cosine"
            ],
        },
    )


def evaluate_outer_panel(
    panel: dict[str, Any],
    contract: list[dict[str, str]],
    expected_plan_sha256: str,
    branch_death: float,
    base_context: dict[str, Any],
    multiplier: float,
    started: float,
    runtime_limit_seconds: float,
    encountered: dict[str, dict[str, Any]],
) -> dict[str, Any] | None:
    nodes = panel_nodes(panel)
    results: dict[str, dict[str, Any]] = {}
    for node in nodes:
        encountered[node["node_id"]] = node
        if not shard_complete(node, expected_plan_sha256):
            if time.perf_counter() - started >= runtime_limit_seconds:
                return None
            integrate_node(
                node,
                contract,
                expected_plan_sha256,
                branch_death,
                base_context,
                multiplier,
            )
        results[node["node_id"]] = read_json(
            shard_paths(node["node_id"])["result"]
        )
        atomic_json(
            STATUS,
            {
                "checkpoint": CHECKPOINT,
                "state": "RUNNING",
                "stage": "REFINED_POLE_ENDPOINT_COLLAR_OUTER_NODES",
                "adaptive_panel_id": panel["adaptive_panel_id"],
                "last_completed_node_id": node["node_id"],
            },
        )
    if not all(bool(row["acceptance_passed"]) for row in results.values()):
        return {
            **panel,
            "panel_nodes_complete": True,
            "all_inner_nodes_pass": False,
            "adaptive_gate_passes": False,
            "outer_Q2_Q4_relative_change": math.inf,
            "failure_reason": "INNER_NODE_FAILURE",
        }
    totals: dict[int, complex] = {}
    for order in OUTER_ORDERS:
        totals[order] = sum(
            (
                float(node["mapped_outer_weight"])
                * complex(
                    float(results[node["node_id"]]["selected_inner_energy_real"]),
                    float(results[node["node_id"]]["selected_inner_energy_imaginary"]),
                )
                for node in nodes if int(node["outer_order"]) == order
            ),
            0.0j,
        )
    change = relative_complex_change(totals[2], totals[4])
    return {
        **panel,
        "panel_nodes_complete": True,
        "all_inner_nodes_pass": True,
        **complex_fields("outer_Q2_energy_Q12", totals[2]),
        **complex_fields("outer_Q4_energy_Q12", totals[4]),
        "outer_Q2_Q4_absolute_change": abs(totals[4] - totals[2]),
        "outer_Q2_Q4_relative_change": change,
        "adaptive_gate_passes": change <= LOCAL_OUTER_CHANGE_LIMIT,
        "failure_reason": "",
    }


def refine_outer_panels(
    initial: list[dict[str, Any]],
    contract: list[dict[str, str]],
    expected_plan_sha256: str,
    branch_death: float,
    base_context: dict[str, Any],
    multiplier: float,
    started: float,
    runtime_limit_seconds: float,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, dict[str, Any]], bool]:
    rows: list[dict[str, Any]] = []
    leaves: list[dict[str, Any]] = []
    encountered: dict[str, dict[str, Any]] = {}
    paused = False

    def visit(panel: dict[str, Any]) -> None:
        nonlocal paused
        if paused:
            return
        result = evaluate_outer_panel(
            panel,
            contract,
            expected_plan_sha256,
            branch_death,
            base_context,
            multiplier,
            started,
            runtime_limit_seconds,
            encountered,
        )
        if result is None:
            paused = True
            return
        depth = int(panel["adaptive_depth"])
        requires_split = (
            bool(result["all_inner_nodes_pass"])
            and not bool(result["adaptive_gate_passes"])
            and depth < MAXIMUM_ADAPTIVE_DEPTH
        )
        result["adaptive_leaf"] = not requires_split
        result["refinement_action"] = (
            "BISECT" if requires_split else "ACCEPT_LEAF"
        )
        if (
            not bool(result["adaptive_gate_passes"])
            and depth >= MAXIMUM_ADAPTIVE_DEPTH
        ):
            result["failure_reason"] = "MAXIMUM_ADAPTIVE_DEPTH_REACHED"
        rows.append(result)
        if requires_split:
            left, right = split_panel(panel)
            visit(left)
            visit(right)
        else:
            leaves.append(result)

    for panel in initial:
        visit(panel)
    return rows, leaves, encountered, paused


def manifest_rows(
    encountered: dict[str, dict[str, Any]],
    expected_plan_sha256: str,
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for node_id, node in sorted(encountered.items()):
        complete = shard_complete(node, expected_plan_sha256)
        result = read_json(shard_paths(node_id)["result"]) if complete else {}
        rows.append(
            {
                **node,
                "shard_state": (
                    "COMPLETE_PASS"
                    if complete and bool(result["acceptance_passed"])
                    else ("COMPLETE_FAIL" if complete else "PENDING")
                ),
                "runtime_seconds": result.get("runtime_seconds", ""),
                "node_result_path": str(shard_paths(node_id)["result"]),
            }
        )
    return rows


def aggregate_shards(
    manifest: list[dict[str, Any]],
) -> tuple[list[dict[str, str]], list[dict[str, str]]]:
    fits: list[dict[str, str]] = []
    integrals: list[dict[str, str]] = []
    for row in manifest:
        if not str(row["shard_state"]).startswith("COMPLETE"):
            continue
        paths = shard_paths(str(row["node_id"]))
        fits.extend(read_csv(paths["fits"]))
        integrals.extend(read_csv(paths["integrals"]))
    return fits, integrals


def execute(runtime_limit_seconds: float) -> dict[str, Any]:
    M5312.set_below_normal_priority()
    mp.mp.dps = M5280.MP_DECIMAL_DIGITS
    M5301.configure_reused_pipeline()
    started = time.perf_counter()
    dry = dry_run()
    if not dry["acceptance_passed"]:
        raise RuntimeError("5314 dry run did not pass")
    contract = read_csv(CONTRACT_5312)
    events = all_branch_events(contract)
    write_csv(POLE_ORDER_AUDIT, read_csv(M5313.DOUBLE_LAURENT_PREFLIGHT))
    expected_plan_sha256 = plan_sha256(events)
    initial = initial_panels(events)
    death = next(
        float(row["event_absolute_soft_cosine"])
        for row in events if row["event_type"] == "SHARED_BRANCH_DEATH"
    )
    base_context = M5303.synthetic_context()
    multiplier = M5309.physical_multiplier()
    panel_rows, leaves, encountered, paused = refine_outer_panels(
        initial,
        contract,
        expected_plan_sha256,
        death,
        base_context,
        multiplier,
        started,
        runtime_limit_seconds,
    )
    write_csv(
        ADAPTIVE_PANELS,
        panel_rows,
        ["adaptive_panel_id", "adaptive_depth", "adaptive_leaf"],
    )
    manifest = manifest_rows(encountered, expected_plan_sha256)
    write_csv(NODE_MANIFEST, manifest, ["node_id", "shard_state"])
    fits, integrals = aggregate_shards(manifest)
    write_csv(
        ALL_POLE_FITS,
        fits,
        ["node_id", "fit_row_type", "fit_scale"],
    )
    write_csv(
        ALL_CELL_INTEGRALS,
        integrals,
        ["node_id", "contract_index", "energy_order"],
    )
    all_leaves_pass = (
        not paused
        and bool(leaves)
        and all(bool(row["all_inner_nodes_pass"]) for row in leaves)
        and all(bool(row["adaptive_gate_passes"]) for row in leaves)
    )
    numeric_leaves = [
        row for row in leaves
        if row.get("outer_Q4_energy_Q12_real", "") != ""
    ]
    if not paused and len(numeric_leaves) == len(leaves):
        p9_q2 = sum(
            (
                complex(
                    float(row["outer_Q2_energy_Q12_real"]),
                    float(row["outer_Q2_energy_Q12_imaginary"]),
                )
                for row in numeric_leaves
            ),
            0.0j,
        )
        p9_q4 = sum(
            (
                complex(
                    float(row["outer_Q4_energy_Q12_real"]),
                    float(row["outer_Q4_energy_Q12_imaginary"]),
                )
                for row in numeric_leaves
            ),
            0.0j,
        )
        error = sum(
            float(row["outer_Q2_Q4_absolute_change"])
            for row in numeric_leaves
        )
        baseline = M5313.baseline_panels_one_to_eight()
        full_value = baseline + p9_q4
        p9_error_relative = error / max(abs(p9_q4), 1.0e-12)
        full_error_relative = error / max(abs(full_value), 1.0e-12)
    else:
        p9_q2 = p9_q4 = full_value = 0.0j
        error = p9_error_relative = full_error_relative = math.inf
    accepted = (
        all_leaves_pass
        and p9_error_relative <= GLOBAL_OUTER_ERROR_BUDGET_LIMIT
    )
    if paused:
        decision = "REFINED_POLE_ENDPOINT_COLLAR_PAUSED__RESUME_SAVED_SHARDS"
    elif not all_leaves_pass:
        decision = "REFINED_POLE_COLLAR_LOCALIZES_REMAINING_OUTER_ENDPOINT_FAILURE"
    elif not accepted:
        decision = "REFINED_POLE_COLLAR_REQUIRES_DEEPER_OUTER_ERROR_CONTROL"
    else:
        decision = (
            "E0025_REFINED_POLE_ENDPOINT_COLLAR_CONVERGED__"
            "EXTEND_FIVE_REGULATOR_LADDER"
        )
    formal_end = M5283.formal_inventory_digest()
    result = {
        "checkpoint": CHECKPOINT,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "mode": "refined-simple-pole-endpoint-collar-integrator",
        "acceptance_passed": accepted,
        "decision": decision,
        "branch_event_count": len(events),
        "shared_branch_death_absolute_soft_cosine": death,
        "initial_panel_count": len(initial),
        "evaluated_adaptive_panel_count": len(panel_rows),
        "final_adaptive_leaf_count": len(leaves),
        "encountered_node_count": len(encountered),
        "completed_node_count": sum(
            str(row["shard_state"]).startswith("COMPLETE") for row in manifest
        ),
        "failed_inner_node_count": sum(
            row["shard_state"] == "COMPLETE_FAIL" for row in manifest
        ),
        "all_final_leaves_pass": all_leaves_pass,
        "maximum_leaf_outer_Q2_Q4_relative_change": (
            max(float(row["outer_Q2_Q4_relative_change"]) for row in leaves)
            if leaves
            else math.inf
        ),
        "refined_pole_fit_row_count": len(fits),
        "refined_pole_subtraction_node_count": len(
            {
                row["node_id"] for row in fits
                if row.get("fit_row_type")
                == "FINAL_REFINED_SIMPLE_POLE_FIT"
                and parse_bool(row.get("refined_simple_pole_contract_passes", False))
            }
        ),
        **complex_fields("panel_nine_outer_Q2", p9_q2),
        **complex_fields("panel_nine_outer_Q4", p9_q4),
        "panel_nine_outer_error_absolute": error,
        "panel_nine_outer_error_relative": p9_error_relative,
        **complex_fields("reassembled_E0025_fixed_decay_integral", full_value),
        "reassembled_outer_error_relative": full_error_relative,
        "formalization_workbench_reference_digest": read_json(RESULT_5313)[
            "formalization_workbench_end_digest"
        ],
        "formalization_workbench_end_digest": formal_end,
        "formalization_workbench_modified_file_count": (
            0
            if formal_end
            == read_json(RESULT_5313)["formalization_workbench_end_digest"]
            else -1
        ),
        "claim_boundary": {
            "valid_for_E0025_fixed_decay_outer_soft_integral": accepted,
            **{field: False for field in CLAIM_FIELDS},
            "reason": (
                "Only E0025 at one fixed absolute decay angle is addressed. "
                "The regulator-zero ladder and decay-angle integration remain."
            ),
        },
        "resource_contract": {
            "maximum_task_python_processes": 1,
            "worker_math_threads": 1,
            "windows_priority": "BelowNormal",
            "maximum_silent_work_hours": 4,
            "runtime_limit_seconds_per_invocation": runtime_limit_seconds,
        },
        "node_plan_sha256": expected_plan_sha256,
        "source_files": source_rows(),
        "runtime_seconds": time.perf_counter() - started,
    }
    atomic_json(RESULT, result)
    write_csv(
        CONVERGENCE,
        [
            {
                "epsilon_id": M5312.EPSILON_ID,
                "epsilon": M5312.EPSILON,
                **complex_fields("panel_nine_outer_Q2", p9_q2),
                **complex_fields("panel_nine_outer_Q4", p9_q4),
                "panel_nine_outer_error_relative": p9_error_relative,
                **complex_fields("reassembled_E0025_integral", full_value),
                "reassembled_outer_error_relative": full_error_relative,
                "convergence_passed": accepted,
                **{field: False for field in CLAIM_FIELDS},
            }
        ],
    )
    atomic_json(
        STATUS,
        {
            "checkpoint": CHECKPOINT,
            "state": (
                "COMPLETE"
                if accepted
                else ("PAUSED_RESUMABLE" if paused else "REFINEMENT_REQUIRED")
            ),
            "decision": decision,
            "completed_node_count": result["completed_node_count"],
            "encountered_node_count": len(encountered),
        },
    )
    return result


def validation_gate(gate: str, passed: bool, detail: str) -> dict[str, Any]:
    return M5312.validation_gate(gate, passed, detail)


def render_document(result: dict[str, Any], passed: bool) -> None:
    text = f"""# 5314 — Refined simple-pole endpoint-collar integrator

## Result

The apparent second-order Laurent coefficient from 5313 is tested against a
stricter pole-order alternative.  Iterating
`p <- p + R2/R1` suppresses `R2` to numerical zero while retaining one stable
simple residue.  The shared `s13` branch is therefore treated as a refined
simple pole, not promoted to a physical double pole.

The refined pole is subtracted both while it lies inside contract `29` and in
its one-sided endpoint collars.  Its exact primitive
`R1[log(E_hi-p)-log(E_lo-p)]` is restored, so the subtraction cannot change
the exact integral; it only regularizes quadrature.  Inner energy orders are
raised to Q8/Q12 and the outer event-aligned tree may refine to depth six.

- shared-branch death coordinate:
  `{result['shared_branch_death_absolute_soft_cosine']:.12g}`;
- completed outer nodes: `{result['completed_node_count']}`;
- failed inner nodes: `{result['failed_inner_node_count']}`;
- refined-pole subtraction nodes:
  `{result['refined_pole_subtraction_node_count']}`;
- final adaptive leaves: `{result['final_adaptive_leaf_count']}`;
- maximum leaf Q2/Q4 change:
  `{result['maximum_leaf_outer_Q2_Q4_relative_change']:.12g}`;
- panel-nine error budget:
  `{result['panel_nine_outer_error_relative']:.12g}`;
- reassembled `E0025` fixed-decay integral:
  `{result['reassembled_E0025_fixed_decay_integral_real']:.12g}`
  `{result['reassembled_E0025_fixed_decay_integral_imaginary']:+.12g} i`.

Decision: **{result['decision']}**.

Validation: **{'PASS' if passed else 'FAIL'}**.

## Claim boundary

This remains one regulator at one fixed absolute decay angle.  It does not
establish the regulator-zero limit, decay-angle integral, full phase-space
coefficient, UV prediction, local GR, or full MTS theory.
"""
    DOCUMENT.write_text(text, encoding="utf-8")


def validate_outputs() -> dict[str, Any]:
    started = time.perf_counter()
    result = read_json(RESULT)
    dry = read_json(DRY_RUN)
    events = read_csv(BRANCH_EVENTS)
    panels = read_csv(ADAPTIVE_PANELS)
    manifest = read_csv(NODE_MANIFEST)
    fits = read_csv(ALL_POLE_FITS)
    integrals = read_csv(ALL_CELL_INTEGRALS)
    convergence = read_csv(CONVERGENCE)
    source_files_current = all(
        Path(row["path"]).exists()
        and digest(Path(row["path"])) == row["sha256"]
        for row in result["source_files"]
    )
    final_fit_rows = [
        row for row in fits
        if row.get("fit_row_type") == "FINAL_REFINED_SIMPLE_POLE_FIT"
    ]
    gates = [
        validation_gate(
            "dry_run_and_result_accepted",
            bool(dry["acceptance_passed"]) and bool(result["acceptance_passed"]),
            result["decision"],
        ),
        validation_gate(
            "support_and_branch_death_events_complete",
            len(events) == 3
            and {row["event_type"] for row in events}
            == {"SUPPORT_ENTRY", "SUPPORT_EXIT", "SHARED_BRANCH_DEATH"}
            and all(
                parse_bool(row["valid_for_endpoint_collar_outer_partition"])
                for row in events
            ),
            f"events={len(events)}",
        ),
        validation_gate(
            "refined_simple_pole_contracts_pass",
            bool(final_fit_rows)
            and all(
                parse_bool(row["refined_simple_pole_contract_passes"])
                for row in final_fit_rows
            ),
            f"final_fit_rows={len(final_fit_rows)}",
        ),
        validation_gate(
            "all_inner_nodes_and_outer_leaves_pass",
            int(result["failed_inner_node_count"]) == 0
            and bool(result["all_final_leaves_pass"])
            and all(row["shard_state"] == "COMPLETE_PASS" for row in manifest)
            and all(
                parse_bool(row["adaptive_gate_passes"])
                for row in panels if parse_bool(row["adaptive_leaf"])
            ),
            f"nodes={len(manifest)}; leaves={result['final_adaptive_leaf_count']}",
        ),
        validation_gate(
            "E0025_fixed_decay_outer_integral_converges",
            len(convergence) == 1
            and parse_bool(convergence[0]["convergence_passed"])
            and float(result["panel_nine_outer_error_relative"])
            <= GLOBAL_OUTER_ERROR_BUDGET_LIMIT
            and bool(result["claim_boundary"][
                "valid_for_E0025_fixed_decay_outer_soft_integral"
            ]),
            f"relative={result['panel_nine_outer_error_relative']}",
        ),
        validation_gate(
            "energy_integral_artifacts_complete",
            bool(integrals)
            and len(integrals) == 2 * 2 * len(manifest),
            f"integrals={len(integrals)}",
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
            "VALIDATED_REFINED_SIMPLE_POLE_ENDPOINT_COLLAR_INTEGRATOR"
            if passed
            else "REFINED_SIMPLE_POLE_ENDPOINT_COLLAR_VALIDATION_FAILED"
        ),
        "runtime_seconds": time.perf_counter() - started,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode", choices=("dry-run", "run", "validate"), required=True
    )
    parser.add_argument("--max-runtime-hours", type=float, default=2.5)
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
