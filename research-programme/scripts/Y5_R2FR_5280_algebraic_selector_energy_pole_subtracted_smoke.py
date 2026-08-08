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
import sys
import time
from collections import defaultdict
from pathlib import Path
from typing import Any


for thread_variable in (
    "OMP_NUM_THREADS",
    "OPENBLAS_NUM_THREADS",
    "MKL_NUM_THREADS",
    "NUMEXPR_NUM_THREADS",
    "VECLIB_MAXIMUM_THREADS",
    "BLIS_NUM_THREADS",
):
    os.environ[thread_variable] = "1"
os.environ["PYTHONNOUSERSITE"] = "1"
sys.dont_write_bytecode = True


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
SCRIPTS = POST / "scripts"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
SOURCE = FUNCTIONAL_RG / "5280"
RESIDUALS = POST / "source-intake" / "mts_residuals"

SCRIPT_5279 = (
    SCRIPTS / "Y5_R2FR_5279_algebraic_reciprocal_branch_selector.py"
)
RESULT_5279 = (
    FUNCTIONAL_RG
    / "5279"
    / "algebraic_reciprocal_branch_selector_result.json"
)
VALIDATION_5279 = (
    FUNCTIONAL_RG
    / "5279"
    / "algebraic_reciprocal_branch_selector_validation.csv"
)
FIT_5267 = {
    epsilon_id: (
        FUNCTIONAL_RG
        / "5267"
        / "workers"
        / epsilon_id
        / "energy_residue_fits.csv"
    )
    for epsilon_id in ("E040", "E020")
}
RESULT_5267 = (
    FUNCTIONAL_RG / "5267" / "energy_first_two_regulator_result.json"
)
CONVERGENCE_5267 = (
    FUNCTIONAL_RG
    / "5267"
    / "energy_first_two_regulator_convergence.csv"
)

DRY_RUN = SOURCE / "energy_pole_subtracted_dry_run.json"
MASK_BOUNDARIES = SOURCE / "exact_energy_mask_boundaries.csv"
PANEL_ROWS = SOURCE / "composite_energy_panels.csv"
POLE_FITS = SOURCE / "true_limit_energy_pole_fits.csv"
NODE_ROWS = SOURCE / "energy_quadrature_component_nodes.csv"
ORDER_TOTALS = SOURCE / "energy_first_order_totals.csv"
CONVERGENCE_ROWS = SOURCE / "energy_first_convergence.csv"
RESULT = SOURCE / "energy_pole_subtracted_smoke_result.json"
VALIDATION = SOURCE / "energy_pole_subtracted_smoke_validation.csv"
RESIDUAL_VALIDATION = (
    RESIDUALS / "P8_Y5_BRR545_5280_VALIDATION.csv"
)
STATUS = SOURCE / "status.json"
DOCUMENT = (
    POST
    / "5280-Y5-R2FR-algebraic-selector-energy-pole-subtracted-smoke.md"
)

CHECKPOINT = 5280
PARENT_CHECKPOINT = 5279
MARKER = "MTS_5280_ALGEBRAIC_SELECTOR_ENERGY_POLE_SUBTRACTED_SMOKE"
REVISION = "algebraic-selector-energy-pole-subtracted-smoke-v1"
REGULATOR_IDS = ("E040", "E020")
COMPONENT_IDS = (
    "MC02",
    "MC03",
    "MC04",
    "MC07",
    "MC08",
    "MC12",
    "MC14",
    "MC15",
)
LEGACY_SIX_IDS = (
    "MC03",
    "MC04",
    "MC07",
    "MC12",
    "MC14",
    "MC15",
)
HIDDEN_IDS = ("MC02", "MC08")
POLE_COMPONENT_ID = "MC04"
QUADRATURE_ORDERS = (2, 4)
MAXIMUM_PANEL_WIDTH = 2.5e-2
MP_DECIMAL_DIGITS = 80
FAST_DELTA_EXPONENT = 24
AUDIT_DELTA_EXPONENT = 16
COEFFICIENT_CONVERGENCE_LIMIT = 1.0e-6
ROOT_RESIDUAL_LIMIT = 1.0e-50
ROOT_REFINEMENT_DISTANCE_LIMIT = 1.0e-7
POLE_FIT_OFFSETS = (
    -3.2e-3,
    -1.6e-3,
    -8.0e-4,
    -4.0e-4,
    4.0e-4,
    8.0e-4,
    1.6e-3,
    3.2e-3,
)
POLE_BACKGROUND_DEGREE = 3
POLE_FIT_RELATIVE_RESIDUAL_LIMIT = 2.0e-5
CLAIM_FIELDS = (
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


M5279 = load_module("mts_5279_for_5280", SCRIPT_5279)
M5278 = M5279.M5278
M5277 = M5279.M5277
M5275 = M5279.M5275
M5274 = M5279.M5274
M5040_MP = M5278.M5040_MP
np = M5279.np
mp = M5278.mp


def set_below_normal_priority() -> None:
    if os.name != "nt":
        return
    handle = ctypes.windll.kernel32.GetCurrentProcess()
    ctypes.windll.kernel32.SetPriorityClass(handle, 0x00004000)


def read_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise RuntimeError(f"refusing to write empty CSV: {path}")
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    temporary.replace(path)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def source_rows() -> list[dict[str, str]]:
    paths = (
        Path(__file__).resolve(),
        SCRIPT_5279,
        RESULT_5279,
        VALIDATION_5279,
        FIT_5267["E040"],
        FIT_5267["E020"],
        RESULT_5267,
        CONVERGENCE_5267,
    )
    return [
        {"path": str(path), "sha256": digest(path)}
        for path in paths
    ]


def formal_inventory_digest() -> str:
    return str(M5279.formal_inventory_digest())


def complex_fields(prefix: str, value: complex) -> dict[str, float]:
    return {
        f"{prefix}_real": float(value.real),
        f"{prefix}_imaginary": float(value.imag),
        f"{prefix}_magnitude": float(abs(value)),
    }


def relative_complex_difference(
    first: complex,
    second: complex,
) -> float:
    return abs(first - second) / max(
        abs(first),
        abs(second),
        1.0,
    )


def source_context() -> dict[str, Any]:
    contract = M5274.M5239.source_contract()
    event = M5274.M5239.source_event(contract)
    surfaces = M5277.exact_surface_lookup()
    laws = M5278.law_lookup()
    inventories = {}
    for epsilon_id in REGULATOR_IDS:
        target, components = M5279.component_inventory(
            epsilon_id,
            event,
            contract,
        )
        inventories[epsilon_id] = {
            "target": target,
            "high_precision_target": M5275.target_as_mp(target),
            "components": components,
        }
    return {
        "contract": contract,
        "source_event": event,
        "surfaces": surfaces,
        "laws": laws,
        "inventories": inventories,
    }


def coefficient_at_exponent(
    high_precision_event: dict[str, Any],
    high_precision_target: Any,
    labels: tuple[str, str],
    relative_root: Any,
    exponent: int,
) -> dict[str, Any]:
    (
        soft_direction,
        decay_direction,
        internal,
        global_roots,
    ) = M5275.local_root_data(
        high_precision_event,
        high_precision_target,
        labels,
        relative_root,
    )
    global_root = (global_roots[0] + global_roots[1]) / 2
    scale = max(mp.mpf(1), abs(global_root))
    phase = mp.exp(mp.mpc(0, mp.mpf("0.37")))
    displacement = mp.power(10, -exponent) * scale * phase
    direct, subtraction = M5040_MP.finite_plus_components(
        internal,
        high_precision_event["soft_energy"],
        soft_direction,
        decay_direction,
        high_precision_target,
        global_root + displacement,
    )
    return {
        "global_root": global_root,
        "direct_coefficient": direct * displacement**2,
        "subtraction_coefficient": subtraction
        * displacement**2,
        "total_coefficient": (direct + subtraction)
        * displacement**2,
    }


def evaluate_component(
    event: dict[str, Any],
    epsilon_id: str,
    component_id: str,
    context: dict[str, Any],
    rationals: dict[str, Any] | None = None,
    convergence_audit: bool = False,
) -> dict[str, Any]:
    inventory = context["inventories"][epsilon_id]
    target = inventory["target"]
    component = inventory["components"][component_id]
    if rationals is None:
        rationals = M5274.M5231.root_rationals(event, target)
    selection = M5279.algebraic_component_selector(
        event,
        target,
        component,
        rationals,
    )
    labels = selection["selected_labels"]
    (
        mask_active,
        orientation,
        owned_labels,
        surface_values,
    ) = M5277.exact_mask_orientation(
        labels,
        event,
        context["surfaces"],
    )
    law_active, _, _ = M5278.law_state(
        context["laws"][component_id],
        event,
        context["surfaces"],
    )
    base = {
        "epsilon_id": epsilon_id,
        "component_id": component_id,
        "family": component["family"],
        "owner_summand": component["owner_summand"],
        "selected_role": selection["selected_role"],
        "representing_pair": "|".join(labels),
        "mask_active": mask_active,
        "law_active": law_active,
        "mask_agrees": mask_active == law_active,
        "orientation": orientation,
        "first_label_owned": owned_labels[0],
        "second_label_owned": owned_labels[1],
        "minimum_surface_distance": min(
            abs(surface_values[0]),
            abs(surface_values[1]),
        ),
        "reciprocal_residual": selection[
            "reciprocal_residual"
        ],
        "selected_unit_margin": selection[
            "selected_unit_margin"
        ],
        "winding_delta": M5277.source_winding_delta(
            component,
            selection["selected_role"],
        ),
    }
    if not mask_active:
        return {
            **base,
            "residue": 0.0j,
            "root_equation_residual": 0.0,
            "root_refinement_chordal_distance": 0.0,
            "coefficient_relative_change": 0.0,
            "convergence_audited": convergence_audit,
            "evaluation_status": "MASK_INACTIVE",
        }
    high_precision_event = M5275.event_as_mp(event)
    (
        relative_root,
        root_residual,
        refinement_distance,
    ) = M5275.refine_relative_root(
        high_precision_event,
        inventory["high_precision_target"],
        labels,
        selection["selected_root"],
    )
    fast = coefficient_at_exponent(
        high_precision_event,
        inventory["high_precision_target"],
        labels,
        relative_root,
        FAST_DELTA_EXPONENT,
    )
    coefficient_change = 0.0
    if convergence_audit:
        audit = coefficient_at_exponent(
            high_precision_event,
            inventory["high_precision_target"],
            labels,
            relative_root,
            AUDIT_DELTA_EXPONENT,
        )
        coefficient_change = M5275.relative_complex_difference(
            audit["total_coefficient"],
            fast["total_coefficient"],
        )
    collision_jacobian = M5277.mp_collision_jacobian(
        high_precision_event,
        inventory["high_precision_target"],
        labels,
        relative_root,
    )
    residue = M5277.residue_from_coefficient(
        fast["total_coefficient"],
        relative_root,
        fast["global_root"],
        collision_jacobian,
        orientation,
        base["winding_delta"],
    )
    return {
        **base,
        "residue": complex(residue),
        "root_equation_residual": root_residual,
        "root_refinement_chordal_distance": refinement_distance,
        "coefficient_relative_change": float(coefficient_change),
        "convergence_audited": convergence_audit,
        "evaluation_status": "EVALUATED",
    }


def exact_energy_mask_boundaries(
    context: dict[str, Any],
) -> list[dict[str, Any]]:
    event = context["source_event"]
    energy_minimum = float(M5274.M5267.ENERGY_MINIMUM)
    energy_maximum = float(M5274.M5267.ENERGY_MAXIMUM)
    q_minimum = math.sqrt(1.0 - energy_maximum)
    q_maximum = math.sqrt(1.0 - energy_minimum)
    surface_keys = sorted(
        {
            context["laws"][component_id][field]
            for component_id in COMPONENT_IDS
            for field in ("surface_A", "surface_B")
        }
    )
    rows: list[dict[str, Any]] = []
    for surface_key in surface_keys:
        surface = context["surfaces"][surface_key]
        if surface["family"] != "boosted_hard_leg":
            continue
        coefficients = (
            M5274.M5273.M5272.hard_boundary_coefficients(
                float(event["soft_cosine"]),
                float(event["decay_cosine"]),
                int(surface["hard_leg_sign"]),
                float(surface["target_cosine"]),
                float(surface["chamber_midpoint"]),
            )
        )
        for q_value in M5274.M5273.M5272.quadratic_real_roots(
            *coefficients
        ):
            energy = 1.0 - q_value**2
            if (
                q_minimum < q_value < q_maximum
                and energy_minimum < energy < energy_maximum
            ):
                rows.append(
                    {
                        "surface_key": surface_key,
                        "q_value": q_value,
                        "soft_energy": energy,
                        "equation_residual": abs(
                            M5274.M5273.M5272.hard_boundary_value(
                                q_value,
                                float(event["soft_cosine"]),
                                float(event["decay_cosine"]),
                                int(surface["hard_leg_sign"]),
                                float(surface["target_cosine"]),
                                float(surface["chamber_midpoint"]),
                            )
                        ),
                        "valid_for_exact_energy_mask_boundary": True,
                        "valid_for_full_phase_space_coefficient": False,
                        "valid_for_numeric_UV_claim": False,
                        "valid_for_local_GR_claim": False,
                        "valid_for_full_MTS_claim": False,
                    }
                )
    return sorted(rows, key=lambda row: float(row["soft_energy"]))


def source_pole_rows() -> list[dict[str, Any]]:
    rows = []
    for epsilon_id in REGULATOR_IDS:
        source = read_csv(FIT_5267[epsilon_id])
        if len(source) != 1:
            raise RuntimeError(
                f"expected one 5267 fit for {epsilon_id}"
            )
        row = source[0]
        if row["component_id"] != POLE_COMPONENT_ID:
            raise RuntimeError("5267 pole owner changed")
        rows.append(
            {
                "epsilon_id": epsilon_id,
                "component_id": row["component_id"],
                "center": float(row["center"]),
                "pole": complex(
                    float(row["pole_real"]),
                    float(row["pole_imaginary"]),
                ),
                "old_residue": complex(
                    float(row["outer_residue_real"]),
                    float(row["outer_residue_imaginary"]),
                ),
                "source_path": str(FIT_5267[epsilon_id]),
            }
        )
    return rows


def fit_true_limit_poles(
    context: dict[str, Any],
    cache: dict[tuple[str, float, str], dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    source_event = context["source_event"]
    for source in source_pole_rows():
        epsilon_id = source["epsilon_id"]
        center = float(source["center"])
        pole = complex(source["pole"])
        values: list[complex] = []
        design: list[list[complex]] = []
        sample_rows: list[tuple[float, complex]] = []
        for offset in POLE_FIT_OFFSETS:
            energy = center + offset
            event = dict(source_event)
            event["soft_energy"] = energy
            key = (epsilon_id, energy, POLE_COMPONENT_ID)
            if key not in cache:
                cache[key] = evaluate_component(
                    event,
                    epsilon_id,
                    POLE_COMPONENT_ID,
                    context,
                    convergence_audit=True,
                )
            evaluation = cache[key]
            if not evaluation["mask_active"]:
                raise RuntimeError("pole-fit sample left active mask")
            value = complex(evaluation["residue"])
            sample_rows.append((energy, value))
            values.append(value)
            delta = energy - center
            design.append(
                [
                    1.0 / (energy - pole),
                    *[
                        complex(delta**power)
                        for power in range(
                            POLE_BACKGROUND_DEGREE + 1
                        )
                    ],
                ]
            )
        matrix = np.asarray(design, dtype=np.complex128)
        vector = np.asarray(values, dtype=np.complex128)
        coefficients, _, _, _ = np.linalg.lstsq(
            matrix,
            vector,
            rcond=None,
        )
        predicted = matrix @ coefficients
        residual = float(
            np.linalg.norm(predicted - vector)
            / max(np.linalg.norm(vector), 1.0)
        )
        residue = complex(coefficients[0])
        old_residue = complex(source["old_residue"])
        rows.append(
            {
                "epsilon_id": epsilon_id,
                "component_id": POLE_COMPONENT_ID,
                "center": center,
                "pole_real": pole.real,
                "pole_imaginary": pole.imag,
                "true_limit_residue_real": residue.real,
                "true_limit_residue_imaginary": residue.imag,
                "true_limit_residue_magnitude": abs(residue),
                "old_5267_residue_real": old_residue.real,
                "old_5267_residue_imaginary": old_residue.imag,
                "old_5267_residue_magnitude": abs(old_residue),
                "true_to_old_relative_shift": (
                    abs(residue - old_residue)
                    / max(abs(residue), abs(old_residue), 1.0)
                ),
                "fit_sample_count": len(sample_rows),
                "background_polynomial_degree": (
                    POLE_BACKGROUND_DEGREE
                ),
                "fit_relative_residual": residual,
                "fit_passed": (
                    residual <= POLE_FIT_RELATIVE_RESIDUAL_LIMIT
                ),
                "source_path": source["source_path"],
                "valid_for_true_limit_energy_pole_subtraction": (
                    residual <= POLE_FIT_RELATIVE_RESIDUAL_LIMIT
                ),
                "valid_for_full_phase_space_coefficient": False,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    return rows


def composite_panel_rows(
    mask_rows: list[dict[str, Any]],
    pole_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    energy_minimum = float(M5274.M5267.ENERGY_MINIMUM)
    energy_maximum = float(M5274.M5267.ENERGY_MAXIMUM)
    special = {
        energy_minimum,
        energy_maximum,
        *[
            float(row["soft_energy"]) for row in mask_rows
        ],
    }
    for row in pole_rows:
        center = float(row["center"])
        for offset in (-4.0e-3, 0.0, 4.0e-3):
            coordinate = center + offset
            if energy_minimum < coordinate < energy_maximum:
                special.add(coordinate)
    boundaries = sorted(special)
    refined: list[float] = [boundaries[0]]
    for lower, upper in zip(boundaries[:-1], boundaries[1:]):
        count = max(
            1,
            int(math.ceil((upper - lower) / MAXIMUM_PANEL_WIDTH)),
        )
        for index in range(1, count + 1):
            refined.append(
                lower + (upper - lower) * index / count
            )
    refined = sorted(set(refined))
    mask_coordinates = {
        round(float(row["soft_energy"]), 14) for row in mask_rows
    }
    pole_centers = {
        round(float(row["center"]), 14) for row in pole_rows
    }
    rows: list[dict[str, Any]] = []
    for index, (lower, upper) in enumerate(
        zip(refined[:-1], refined[1:]),
        start=1,
    ):
        rows.append(
            {
                "panel_id": f"EP{index:03d}",
                "lower": lower,
                "upper": upper,
                "width": upper - lower,
                "midpoint": 0.5 * (lower + upper),
                "left_is_mask_boundary": (
                    round(lower, 14) in mask_coordinates
                ),
                "right_is_mask_boundary": (
                    round(upper, 14) in mask_coordinates
                ),
                "contains_pole_center": any(
                    lower <= center <= upper
                    for center in pole_centers
                ),
                "valid_for_composite_energy_quadrature": True,
                "valid_for_full_phase_space_coefficient": False,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    return rows


def evaluate_energy_event(
    epsilon_id: str,
    energy: float,
    context: dict[str, Any],
    cache: dict[tuple[str, float, str], dict[str, Any]],
    convergence_audit: bool,
) -> dict[str, dict[str, Any]]:
    event = dict(context["source_event"])
    event["soft_energy"] = energy
    target = context["inventories"][epsilon_id]["target"]
    rationals = M5274.M5231.root_rationals(event, target)
    result = {}
    for component_id in COMPONENT_IDS:
        key = (epsilon_id, energy, component_id)
        if key not in cache:
            cache[key] = evaluate_component(
                event,
                epsilon_id,
                component_id,
                context,
                rationals=rationals,
                convergence_audit=convergence_audit,
            )
        result[component_id] = cache[key]
    return result


def integrate_energy(
    context: dict[str, Any],
    panels: list[dict[str, Any]],
    fitted_poles: list[dict[str, Any]],
    cache: dict[tuple[str, float, str], dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    fitted = {
        row["epsilon_id"]: {
            "pole": complex(
                float(row["pole_real"]),
                float(row["pole_imaginary"]),
            ),
            "residue": complex(
                float(row["true_limit_residue_real"]),
                float(row["true_limit_residue_imaginary"]),
            ),
        }
        for row in fitted_poles
    }
    node_rows: list[dict[str, Any]] = []
    totals: list[dict[str, Any]] = []
    audit_counter = 0
    for epsilon_id in REGULATOR_IDS:
        pole = fitted[epsilon_id]["pole"]
        pole_residue = fitted[epsilon_id]["residue"]
        for order in QUADRATURE_ORDERS:
            nodes, weights = np.polynomial.legendre.leggauss(order)
            raw_components = {
                component_id: 0.0j
                for component_id in COMPONENT_IDS
            }
            regular_components = {
                component_id: 0.0j
                for component_id in COMPONENT_IDS
            }
            raw_total = 0.0j
            regular_total = 0.0j
            for panel in panels:
                lower = float(panel["lower"])
                upper = float(panel["upper"])
                half_width = 0.5 * (upper - lower)
                midpoint = 0.5 * (upper + lower)
                for local_index, (
                    node,
                    weight,
                ) in enumerate(zip(nodes, weights), start=1):
                    energy = midpoint + half_width * float(node)
                    mapped_weight = half_width * float(weight)
                    audit_counter += 1
                    audit = audit_counter % 24 == 0
                    evaluations = evaluate_energy_event(
                        epsilon_id,
                        energy,
                        context,
                        cache,
                        convergence_audit=audit,
                    )
                    singular = pole_residue / (energy - pole)
                    for component_id in COMPONENT_IDS:
                        evaluation = evaluations[component_id]
                        value = complex(evaluation["residue"])
                        regular = (
                            value - singular
                            if component_id == POLE_COMPONENT_ID
                            else value
                        )
                        raw_components[component_id] += (
                            mapped_weight * value
                        )
                        regular_components[component_id] += (
                            mapped_weight * regular
                        )
                        node_rows.append(
                            {
                                "epsilon_id": epsilon_id,
                                "quadrature_order": order,
                                "panel_id": panel["panel_id"],
                                "local_node_index": local_index,
                                "soft_energy": energy,
                                "mapped_weight": mapped_weight,
                                "component_id": component_id,
                                "mask_active": evaluation[
                                    "mask_active"
                                ],
                                "selected_role": evaluation[
                                    "selected_role"
                                ],
                                "residue_real": value.real,
                                "residue_imaginary": value.imag,
                                "regularized_residue_real": (
                                    regular.real
                                ),
                                "regularized_residue_imaginary": (
                                    regular.imag
                                ),
                                "weighted_residue_real": (
                                    mapped_weight * value.real
                                ),
                                "weighted_residue_imaginary": (
                                    mapped_weight * value.imag
                                ),
                                "coefficient_relative_change": (
                                    evaluation[
                                        "coefficient_relative_change"
                                    ]
                                ),
                                "convergence_audited": evaluation[
                                    "convergence_audited"
                                ],
                                "root_equation_residual": evaluation[
                                    "root_equation_residual"
                                ],
                                "root_refinement_chordal_distance": (
                                    evaluation[
                                        "root_refinement_chordal_distance"
                                    ]
                                ),
                                "reciprocal_residual": evaluation[
                                    "reciprocal_residual"
                                ],
                                "valid_for_energy_pole_subtracted_smoke": (
                                    True
                                ),
                                "valid_for_full_phase_space_coefficient": (
                                    False
                                ),
                                "valid_for_numeric_UV_claim": False,
                                "valid_for_local_GR_claim": False,
                                "valid_for_full_MTS_claim": False,
                            }
                        )
                    event_total = sum(
                        (
                            complex(
                                evaluations[component_id]["residue"]
                            )
                            for component_id in COMPONENT_IDS
                        ),
                        0.0j,
                    )
                    raw_total += mapped_weight * event_total
                    regular_total += mapped_weight * (
                        event_total - singular
                    )
                atomic_json(
                    STATUS,
                    {
                        "checkpoint": CHECKPOINT,
                        "state": "RUNNING",
                        "epsilon_id": epsilon_id,
                        "quadrature_order": order,
                        "last_panel_id": panel["panel_id"],
                        "component_node_row_count": len(node_rows),
                    },
                )
            energy_minimum = float(
                M5274.M5267.ENERGY_MINIMUM
            )
            energy_maximum = float(
                M5274.M5267.ENERGY_MAXIMUM
            )
            analytic_singular = pole_residue * (
                cmath.log(energy_maximum - pole)
                - cmath.log(energy_minimum - pole)
            )
            subtracted_total = regular_total + analytic_singular
            corrected_components = dict(regular_components)
            corrected_components[POLE_COMPONENT_ID] += (
                analytic_singular
            )
            corrected_eight = sum(
                corrected_components.values(),
                0.0j,
            )
            corrected_six = sum(
                (
                    corrected_components[component_id]
                    for component_id in LEGACY_SIX_IDS
                ),
                0.0j,
            )
            corrected_hidden = sum(
                (
                    corrected_components[component_id]
                    for component_id in HIDDEN_IDS
                ),
                0.0j,
            )
            totals.append(
                {
                    "row_type": "REGULATOR_ENERGY_INTEGRAL",
                    "epsilon_id": epsilon_id,
                    "quadrature_order": order,
                    **complex_fields("raw_eight_integral", raw_total),
                    **complex_fields(
                        "regular_remainder",
                        regular_total,
                    ),
                    **complex_fields(
                        "analytic_singular",
                        analytic_singular,
                    ),
                    **complex_fields(
                        "subtracted_eight_integral",
                        subtracted_total,
                    ),
                    **complex_fields(
                        "component_sum_crosscheck",
                        corrected_eight,
                    ),
                    **complex_fields(
                        "subtracted_six_integral",
                        corrected_six,
                    ),
                    **complex_fields(
                        "hidden_MC02_MC08_integral",
                        corrected_hidden,
                    ),
                    "component_sum_relative_residual": (
                        abs(corrected_eight - subtracted_total)
                        / max(
                            abs(corrected_eight),
                            abs(subtracted_total),
                            1.0,
                        )
                    ),
                    "panel_count": len(panels),
                    "valid_for_energy_pole_subtracted_smoke": True,
                    "valid_for_full_phase_space_coefficient": False,
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
            )
    return node_rows, totals


def physical_total_rows(
    regulator_rows: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    lookup = {
        (
            int(row["quadrature_order"]),
            row["epsilon_id"],
        ): row
        for row in regulator_rows
    }
    multiplier = (
        M5274.M5231.PHYSICAL_A00_WEIGHT
        * M5274.M5231.KERNEL_MULTIPLIER
    )
    rows = list(regulator_rows)
    for order in QUADRATURE_ORDERS:
        local = {}
        for epsilon_id in REGULATOR_IDS:
            row = lookup[(order, epsilon_id)]
            local[epsilon_id] = {
                channel: complex(
                    float(row[f"{channel}_real"]),
                    float(row[f"{channel}_imaginary"]),
                )
                for channel in (
                    "raw_eight_integral",
                    "subtracted_eight_integral",
                    "subtracted_six_integral",
                    "hidden_MC02_MC08_integral",
                )
            }
        values = {}
        for channel in local["E040"]:
            values[channel] = multiplier * (
                2.0 * local["E020"][channel]
                - local["E040"][channel]
            )
        rows.append(
            {
                "row_type": "PHYSICAL_ENERGY_EXTRAPOLATION",
                "epsilon_id": "2E020_MINUS_E040",
                "quadrature_order": order,
                **complex_fields(
                    "raw_eight_integral",
                    values["raw_eight_integral"],
                ),
                **complex_fields(
                    "subtracted_eight_integral",
                    values["subtracted_eight_integral"],
                ),
                **complex_fields(
                    "subtracted_six_integral",
                    values["subtracted_six_integral"],
                ),
                **complex_fields(
                    "hidden_MC02_MC08_integral",
                    values["hidden_MC02_MC08_integral"],
                ),
                "kernel_multiplier": (
                    M5274.M5231.KERNEL_MULTIPLIER
                ),
                "physical_A00_weight": (
                    M5274.M5231.PHYSICAL_A00_WEIGHT
                ),
                "valid_for_energy_pole_subtracted_smoke": True,
                "valid_for_full_phase_space_coefficient": False,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    return rows


def convergence_diagnostics(
    totals: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    physical = {
        int(row["quadrature_order"]): row
        for row in totals
        if row["row_type"] == "PHYSICAL_ENERGY_EXTRAPOLATION"
    }
    old_rows = read_csv(CONVERGENCE_5267)
    old_reference_row = max(
        old_rows,
        key=lambda row: int(row["quadrature_order"]),
    )
    old_reference = complex(
        float(old_reference_row["subtracted_real"]),
        float(old_reference_row["subtracted_imaginary"]),
    )
    low_order = QUADRATURE_ORDERS[0]
    high_order = QUADRATURE_ORDERS[-1]
    rows: list[dict[str, Any]] = []
    for channel in (
        "raw_eight_integral",
        "subtracted_eight_integral",
        "subtracted_six_integral",
        "hidden_MC02_MC08_integral",
    ):
        low = complex(
            float(physical[low_order][f"{channel}_real"]),
            float(physical[low_order][f"{channel}_imaginary"]),
        )
        high = complex(
            float(physical[high_order][f"{channel}_real"]),
            float(physical[high_order][f"{channel}_imaginary"]),
        )
        rows.append(
            {
                "channel": channel,
                "low_order": low_order,
                "high_order": high_order,
                **complex_fields("low_order_value", low),
                **complex_fields("high_order_value", high),
                "relative_change": relative_complex_difference(
                    low,
                    high,
                ),
                "old_5267_reference_real": old_reference.real,
                "old_5267_reference_imaginary": old_reference.imag,
                "high_order_shift_from_old_5267": (
                    relative_complex_difference(
                        high,
                        old_reference,
                    )
                ),
                "valid_for_energy_pole_subtracted_smoke": True,
                "valid_for_converged_fixed_angle_energy_integral": (
                    False
                ),
                "valid_for_full_phase_space_coefficient": False,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    return rows


def dry_run() -> dict[str, Any]:
    SOURCE.mkdir(parents=True, exist_ok=True)
    required = (
        SCRIPT_5279,
        RESULT_5279,
        VALIDATION_5279,
        FIT_5267["E040"],
        FIT_5267["E020"],
        RESULT_5267,
        CONVERGENCE_5267,
    )
    parent = read_json(RESULT_5279)
    parent_validation = read_csv(VALIDATION_5279)
    checks = {
        "required_sources_exist": all(
            path.exists() for path in required
        ),
        "parent_5279_accepted": bool(parent["acceptance_passed"]),
        "parent_5279_validated": all(
            row["passed"].lower() == "true"
            for row in parent_validation
        ),
        "algebraic_transport_elimination_authorized": bool(
            parent["claim_boundary"][
                "valid_for_path_transport_elimination_in_cubature"
            ]
        ),
        "old_geometric_poles_source_complete": all(
            len(read_csv(FIT_5267[epsilon_id])) == 1
            for epsilon_id in REGULATOR_IDS
        ),
        "formalization_workbench_unchanged": (
            formal_inventory_digest()
            == str(parent["formalization_workbench_end_digest"])
        ),
    }
    accepted = all(checks.values())
    result = {
        "checkpoint": CHECKPOINT,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "mode": "dry-run",
        "checks": checks,
        "acceptance_passed": accepted,
        "quadrature_orders": list(QUADRATURE_ORDERS),
        "maximum_panel_width": MAXIMUM_PANEL_WIDTH,
        "decision": (
            "DRY_RUN_ACCEPTED__RUN_TRUE_LIMIT_ENERGY_POLE_SUBTRACTION"
            if accepted
            else "DRY_RUN_REQUIRES_REPAIR"
        ),
        "runtime_seconds": 0.0,
        "valid_for_full_phase_space_coefficient": False,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    atomic_json(DRY_RUN, result)
    return result


def execute() -> dict[str, Any]:
    started = time.perf_counter()
    set_below_normal_priority()
    mp.mp.dps = MP_DECIMAL_DIGITS
    dry = dry_run()
    if not dry["acceptance_passed"]:
        raise RuntimeError("5280 dry run did not pass")
    parent = read_json(RESULT_5279)
    context = source_context()
    cache: dict[tuple[str, float, str], dict[str, Any]] = {}
    mask_rows = exact_energy_mask_boundaries(context)
    pole_fits = fit_true_limit_poles(context, cache)
    panels = composite_panel_rows(mask_rows, pole_fits)
    node_rows, regulator_totals = integrate_energy(
        context,
        panels,
        pole_fits,
        cache,
    )
    totals = physical_total_rows(regulator_totals)
    convergence = convergence_diagnostics(totals)
    audited = [
        row
        for evaluation in cache.values()
        if bool(evaluation["convergence_audited"])
        and bool(evaluation["mask_active"])
        for row in [evaluation]
    ]
    active = [
        evaluation
        for evaluation in cache.values()
        if bool(evaluation["mask_active"])
    ]
    maximum_coefficient_change = max(
        (
            float(row["coefficient_relative_change"])
            for row in audited
        ),
        default=0.0,
    )
    maximum_root_residual = max(
        (
            float(row["root_equation_residual"])
            for row in active
        ),
        default=0.0,
    )
    maximum_refinement_distance = max(
        (
            float(row["root_refinement_chordal_distance"])
            for row in active
        ),
        default=0.0,
    )
    maximum_component_sum_residual = max(
        float(row["component_sum_relative_residual"])
        for row in regulator_totals
    )
    maximum_fit_residual = max(
        float(row["fit_relative_residual"]) for row in pole_fits
    )
    maximum_mask_boundary_residual = max(
        float(row["equation_residual"]) for row in mask_rows
    )
    subtracted_change = next(
        float(row["relative_change"])
        for row in convergence
        if row["channel"] == "subtracted_eight_integral"
    )
    raw_change = next(
        float(row["relative_change"])
        for row in convergence
        if row["channel"] == "raw_eight_integral"
    )
    checks = {
        "parent_5279_accepted": bool(parent["acceptance_passed"]),
        "two_exact_energy_mask_boundaries_recovered": (
            len(mask_rows) == 2
            and maximum_mask_boundary_residual <= 1.0e-12
        ),
        "one_true_limit_pole_fit_per_regulator": (
            len(pole_fits) == len(REGULATOR_IDS)
            and all(bool(row["fit_passed"]) for row in pole_fits)
        ),
        "composite_panels_cover_domain": (
            bool(panels)
            and abs(
                sum(float(row["width"]) for row in panels)
                - (
                    M5274.M5267.ENERGY_MAXIMUM
                    - M5274.M5267.ENERGY_MINIMUM
                )
            )
            <= 1.0e-12
            and max(float(row["width"]) for row in panels)
            <= MAXIMUM_PANEL_WIDTH + 1.0e-12
        ),
        "algebraic_evaluator_produced_active_rows": bool(active),
        "audited_coefficients_converged": (
            bool(audited)
            and maximum_coefficient_change
            <= COEFFICIENT_CONVERGENCE_LIMIT
        ),
        "all_active_roots_refined": (
            maximum_root_residual <= ROOT_RESIDUAL_LIMIT
            and maximum_refinement_distance
            <= ROOT_REFINEMENT_DISTANCE_LIMIT
        ),
        "component_sum_closes": (
            maximum_component_sum_residual <= 1.0e-10
        ),
        "pole_subtraction_improves_low_order_stability": (
            subtracted_change < raw_change
        ),
        "formalization_workbench_unchanged": (
            formal_inventory_digest()
            == str(parent["formalization_workbench_end_digest"])
        ),
        "claims_locked_false": True,
    }
    accepted = all(checks.values())
    physical = {
        str(row["quadrature_order"]): {
            "raw_real": row["raw_eight_integral_real"],
            "raw_imaginary": row[
                "raw_eight_integral_imaginary"
            ],
            "subtracted_eight_real": row[
                "subtracted_eight_integral_real"
            ],
            "subtracted_eight_imaginary": row[
                "subtracted_eight_integral_imaginary"
            ],
            "subtracted_six_real": row[
                "subtracted_six_integral_real"
            ],
            "subtracted_six_imaginary": row[
                "subtracted_six_integral_imaginary"
            ],
            "hidden_real": row[
                "hidden_MC02_MC08_integral_real"
            ],
            "hidden_imaginary": row[
                "hidden_MC02_MC08_integral_imaginary"
            ],
        }
        for row in totals
        if row["row_type"] == "PHYSICAL_ENERGY_EXTRAPOLATION"
    }
    formal_end = formal_inventory_digest()
    result = {
        "checkpoint": CHECKPOINT,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "mode": "algebraic-selector-energy-pole-subtracted-smoke",
        "checks": checks,
        "acceptance_passed": accepted,
        "quadrature_orders": list(QUADRATURE_ORDERS),
        "maximum_panel_width": MAXIMUM_PANEL_WIDTH,
        "panel_count": len(panels),
        "exact_mask_boundary_count": len(mask_rows),
        "pole_fit_count": len(pole_fits),
        "component_node_row_count": len(node_rows),
        "unique_component_evaluation_count": len(cache),
        "active_component_evaluation_count": len(active),
        "coefficient_audit_count": len(audited),
        "maximum_audited_coefficient_relative_change": (
            maximum_coefficient_change
        ),
        "maximum_root_equation_residual": maximum_root_residual,
        "maximum_root_refinement_chordal_distance": (
            maximum_refinement_distance
        ),
        "maximum_pole_fit_relative_residual": (
            maximum_fit_residual
        ),
        "maximum_component_sum_relative_residual": (
            maximum_component_sum_residual
        ),
        "raw_low_order_relative_change": raw_change,
        "subtracted_low_order_relative_change": subtracted_change,
        "physical_order_totals": physical,
        "source_files": source_rows(),
        "formalization_workbench_reference_digest": str(
            parent["formalization_workbench_end_digest"]
        ),
        "formalization_workbench_end_digest": formal_end,
        "formalization_workbench_modified_file_count": (
            0
            if formal_end
            == str(parent["formalization_workbench_end_digest"])
            else -1
        ),
        "resource_contract": {
            "maximum_task_python_processes": 1,
            "worker_math_threads": 1,
            "windows_priority": "BelowNormal",
            "sustained_redline_forbidden": True,
        },
        "runtime_seconds": time.perf_counter() - started,
        "decision": (
            "ACCEPT_ALGEBRAIC_TRUE_LIMIT_ENERGY_POLE_SUBTRACTION__"
            "INCREASE_ENERGY_ORDERS_THEN_RESTORE_ANGULAR_OUTER_INTEGRATION"
            if accepted
            else "ENERGY_POLE_SUBTRACTED_SMOKE_REQUIRES_REPAIR"
        ),
        "claim_boundary": {
            "valid_for_algebraic_pointwise_evaluator": accepted,
            "valid_for_true_limit_fixed_angle_pole_subtraction": (
                accepted
            ),
            "valid_for_converged_fixed_angle_energy_integral": False,
            "valid_for_angular_outer_integration": False,
            "valid_for_full_phase_space_coefficient": False,
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
            "reason": (
                "The direct algebraic selector, exact energy masks, "
                "true local-limit residues, and sourced geometric pole "
                "now form one executable fixed-angle energy pipeline. "
                "Orders two and four are a subtraction smoke, not the "
                "final energy convergence or angular integral."
            ),
        },
    }
    write_csv(MASK_BOUNDARIES, mask_rows)
    write_csv(PANEL_ROWS, panels)
    write_csv(POLE_FITS, pole_fits)
    write_csv(NODE_ROWS, node_rows)
    write_csv(ORDER_TOTALS, totals)
    write_csv(CONVERGENCE_ROWS, convergence)
    atomic_json(RESULT, result)
    atomic_json(
        STATUS,
        {
            "checkpoint": CHECKPOINT,
            "state": "COMPLETED",
            "mode": result["mode"],
            "acceptance_passed": accepted,
            "decision": result["decision"],
            "runtime_seconds": result["runtime_seconds"],
        },
    )
    return result


def validation_gate(
    gate_id: str,
    passed: bool,
    detail: str,
) -> dict[str, Any]:
    return {
        "gate_id": gate_id,
        "passed": passed,
        "detail": detail,
    }


def render_document(
    result: dict[str, Any],
    validation_passed: bool,
) -> None:
    checks = "\n".join(
        f"- `{name}`: **{'PASS' if passed else 'FAIL'}**"
        for name, passed in result["checks"].items()
    )
    totals = "\n".join(
        (
            f"- order `{order}`: raw "
            f"`{values['raw_real']:.12g}"
            f"{values['raw_imaginary']:+.12g}i`; subtracted eight "
            f"`{values['subtracted_eight_real']:.12g}"
            f"{values['subtracted_eight_imaginary']:+.12g}i`; "
            f"subtracted six `{values['subtracted_six_real']:.12g}"
            f"{values['subtracted_six_imaginary']:+.12g}i`."
        )
        for order, values in result["physical_order_totals"].items()
    )
    text = f"""# 5280 — Algebraic-selector energy pole-subtracted smoke

## Purpose

This checkpoint inserts the 5279 algebraic selector into the true
eight-component pointwise evaluator and returns to the energy-first
strategy required by the nonconverged 5278 tensor result.

## Construction

- exact energy mask boundaries: `{result['exact_mask_boundary_count']}`;
- composite panels: `{result['panel_count']}`, maximum width
  `{result['maximum_panel_width']}`;
- sourced geometric poles refitted with true local-limit residues:
  `{result['pole_fit_count']}`;
- unique component evaluations:
  `{result['unique_component_evaluation_count']}`;
- audited local-limit changes: maximum
  `{result['maximum_audited_coefficient_relative_change']:.12g}`.

The MC04 simple pole is subtracted analytically as
`A/(E-E_p)`, the regular remainder is integrated panel by panel, and
`A[log(E_max-E_p)-log(E_min-E_p)]` is restored exactly.

## Fixed-angle results

{totals}

Raw order change:
`{result['raw_low_order_relative_change']:.12g}`.

Pole-subtracted order change:
`{result['subtracted_low_order_relative_change']:.12g}`.

## Acceptance gates

{checks}

Validation: **{'PASS' if validation_passed else 'FAIL'}**.

## Claim boundary

This is the first corrected energy-first calculation using the exact
eight-component basis and no path tracker. It validates the mechanism
and subtraction pipeline, but orders two and four are deliberately only
a smoke test. Higher energy orders must converge before restoring the
two angular integrations; no phase-space, UV, local-GR, or full-MTS
claim follows here.
"""
    DOCUMENT.write_text(text, encoding="utf-8")


def validate_outputs() -> dict[str, Any]:
    result = read_json(RESULT)
    parent = read_json(RESULT_5279)
    required_csvs = (
        MASK_BOUNDARIES,
        PANEL_ROWS,
        POLE_FITS,
        NODE_ROWS,
        ORDER_TOTALS,
        CONVERGENCE_ROWS,
    )
    csv_rows = {
        str(path): read_csv(path)
        for path in required_csvs
        if path.exists()
    }
    source_files = result["source_files"]
    current_formal_digest = formal_inventory_digest()
    reference_formal_digest = str(
        result["formalization_workbench_reference_digest"]
    )
    serialized = json.dumps(
        {"result": result, "csvs": csv_rows},
        sort_keys=True,
    )
    claim_rows = [
        row
        for rows in csv_rows.values()
        for row in rows
        if any(field in row for field in CLAIM_FIELDS)
    ]
    rows = [
        validation_gate(
            "SOURCE_PATHS_EXIST",
            all(Path(row["path"]).exists() for row in source_files),
            f"{len(source_files)} source paths",
        ),
        validation_gate(
            "SOURCE_HASHES_MATCH",
            all(
                digest(Path(row["path"])) == row["sha256"]
                for row in source_files
            ),
            "all recorded source hashes reproduce",
        ),
        validation_gate(
            "PARENT_5279_ACCEPTED",
            bool(parent["acceptance_passed"]),
            str(parent["decision"]),
        ),
        validation_gate(
            "ENERGY_SMOKE_ACCEPTED",
            bool(result["acceptance_passed"]),
            str(result["decision"]),
        ),
        validation_gate(
            "REQUIRED_CSVS_PARSE",
            (
                len(csv_rows) == len(required_csvs)
                and all(csv_rows.values())
            ),
            f"{len(csv_rows)}/{len(required_csvs)} non-empty CSVs",
        ),
        validation_gate(
            "TRUE_LIMIT_CONTROLS_PASS",
            (
                float(
                    result[
                        "maximum_audited_coefficient_relative_change"
                    ]
                )
                <= COEFFICIENT_CONVERGENCE_LIMIT
                and float(result["maximum_root_equation_residual"])
                <= ROOT_RESIDUAL_LIMIT
                and float(
                    result[
                        "maximum_root_refinement_chordal_distance"
                    ]
                )
                <= ROOT_REFINEMENT_DISTANCE_LIMIT
            ),
            "audited coefficients and roots controlled",
        ),
        validation_gate(
            "POLE_SUBTRACTION_IMPROVES_STABILITY",
            float(result["subtracted_low_order_relative_change"])
            < float(result["raw_low_order_relative_change"]),
            (
                f"raw={result['raw_low_order_relative_change']}; "
                "subtracted="
                f"{result['subtracted_low_order_relative_change']}"
            ),
        ),
        validation_gate(
            "FIXED_ANGLE_CONVERGENCE_REMAINS_FALSE",
            not result["claim_boundary"][
                "valid_for_converged_fixed_angle_energy_integral"
            ],
            "orders 2 and 4 remain a smoke",
        ),
        validation_gate(
            "NO_MISSING_MARKERS",
            "MISSING_" not in serialized,
            "no MISSING_ token in checkpoint artifacts",
        ),
        validation_gate(
            "CLAIMS_LOCKED_FALSE",
            (
                all(
                    not result["claim_boundary"][field]
                    for field in CLAIM_FIELDS
                )
                and all(
                    row.get(field, "false").lower() == "false"
                    for row in claim_rows
                    for field in CLAIM_FIELDS
                    if field in row
                )
            ),
            "phase-space, UV, local-GR, and full-MTS claims false",
        ),
        validation_gate(
            "FORMALIZATION_WORKBENCH_UNCHANGED",
            current_formal_digest == reference_formal_digest,
            (
                f"reference={reference_formal_digest}; "
                f"current={current_formal_digest}"
            ),
        ),
        validation_gate(
            "RESOURCE_CONTRACT_RECORDED",
            (
                result["resource_contract"][
                    "maximum_task_python_processes"
                ]
                == 1
                and result["resource_contract"][
                    "worker_math_threads"
                ]
                == 1
            ),
            "one below-normal single-thread process",
        ),
    ]
    passed = all(row["passed"] for row in rows)
    write_csv(VALIDATION, rows)
    write_csv(RESIDUAL_VALIDATION, rows)
    render_document(result, passed)
    atomic_json(
        STATUS,
        {
            "checkpoint": CHECKPOINT,
            "state": "COMPLETED",
            "mode": "validation",
            "validation_passed": passed,
            "validation_gate_count": len(rows),
            "decision": result["decision"],
        },
    )
    return {
        "checkpoint": CHECKPOINT,
        "mode": "validation",
        "acceptance_passed": passed,
        "decision": (
            "VALIDATED_TRUE_LIMIT_ENERGY_POLE_SUBTRACTED_SMOKE"
            if passed
            else "VALIDATION_REQUIRES_REPAIR"
        ),
        "runtime_seconds": 0.0,
        "validation_gate_count": len(rows),
        "failed_gates": [
            row["gate_id"] for row in rows if not row["passed"]
        ],
        "valid_for_full_phase_space_coefficient": False,
        "valid_for_numeric_UV_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--mode",
        choices=("dry-run", "run", "validate"),
        default="dry-run",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    if args.mode == "dry-run":
        result = dry_run()
    elif args.mode == "run":
        result = execute()
    elif args.mode == "validate":
        result = validate_outputs()
    else:
        raise RuntimeError(f"unsupported mode: {args.mode}")
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
