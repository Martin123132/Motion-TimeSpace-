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
RESIDUALS = POST / "source-intake" / "mts_residuals"
SOURCE = FUNCTIONAL_RG / "5287"

SCRIPT_5286 = (
    SCRIPTS / "Y5_R2FR_5286_angular_node_material_pole_atlas_preflight.py"
)
RESULT_5286 = (
    FUNCTIONAL_RG / "5286" / "angular_node_pole_atlas_result.json"
)
VALIDATION_5286 = (
    FUNCTIONAL_RG / "5286" / "angular_node_pole_atlas_validation.csv"
)
ANGULAR_NODES_5286 = FUNCTIONAL_RG / "5286" / "angular_order2_nodes.csv"
POLE_ATLAS_5286 = (
    FUNCTIONAL_RG / "5286" / "angular_node_material_pole_atlas.csv"
)

DRY_RUN = SOURCE / "order2_angular_inner_energy_dry_run.json"
POLE_SAMPLE_ROWS = SOURCE / "angular_node_pole_numerator_samples.csv"
POLE_FIT_ROWS = SOURCE / "angular_node_channel_residue_fits.csv"
ENERGY_NODE_ROWS = SOURCE / "angular_node_energy_component_nodes.csv"
INNER_COMPONENT_ROWS = SOURCE / "angular_node_inner_component_totals.csv"
INNER_TOTAL_ROWS = SOURCE / "angular_node_inner_energy_totals.csv"
INNER_CONVERGENCE_ROWS = (
    SOURCE / "angular_node_inner_energy_convergence.csv"
)
OUTER_ROWS = SOURCE / "order2_angular_smoke_totals.csv"
RESULT = SOURCE / "order2_angular_inner_energy_result.json"
VALIDATION = SOURCE / "order2_angular_inner_energy_validation.csv"
RESIDUAL_VALIDATION = (
    RESIDUALS / "P8_Y5_BRR545_5287_VALIDATION.csv"
)
STATUS = SOURCE / "status.json"
DOCUMENT = POST / "5287-Y5-R2FR-order2-angular-inner-energy-smoke.md"

CHECKPOINT = 5287
PARENT_CHECKPOINT = 5286
MARKER = "MTS_5287_ORDER2_ANGULAR_INNER_ENERGY_SMOKE"
REVISION = "order2-angular-inner-energy-smoke-v1"
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
LEGACY_SIX_IDS = ("MC03", "MC04", "MC07", "MC12", "MC14", "MC15")
HIDDEN_IDS = ("MC02", "MC08")
ENERGY_ORDERS = (4, 8)
FIT_FRACTIONS = (-1.0, -0.5, -0.2, -0.1, 0.1, 0.2, 0.5, 1.0)
FIT_RADII = (3.2e-3, 1.6e-3)
FIT_DEGREES = (3, 4)
FIT_RELATIVE_RESIDUAL_LIMIT = 1.0e-7
FIT_REFINEMENT_RELATIVE_CHANGE_LIMIT = 1.0e-6
FIT_DEGREE_RELATIVE_CHANGE_LIMIT = 1.0e-6
COEFFICIENT_CONVERGENCE_LIMIT = 1.0e-6
INNER_RELATIVE_CHANGE_LIMIT = 5.0e-3
OUTER_RELATIVE_CHANGE_LIMIT = 5.0e-3
ENDPOINT_REFINEMENT_OFFSETS = (
    5.0e-4,
    1.0e-3,
    2.0e-3,
    4.0e-3,
    8.0e-3,
    1.6e-2,
)
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


M5286 = load_module("mts_5286_for_5287", SCRIPT_5286)
M5285 = M5286.M5285
M5284 = M5285.M5284
M5280 = M5286.M5280
M5283 = M5286.M5283
M5267 = M5286.M5267
np = M5280.np
mp = M5280.mp


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


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def parse_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() == "true"


def source_rows() -> list[dict[str, str]]:
    paths = (
        Path(__file__).resolve(),
        SCRIPT_5286,
        RESULT_5286,
        VALIDATION_5286,
        ANGULAR_NODES_5286,
        POLE_ATLAS_5286,
    )
    return [
        {"path": str(path), "sha256": digest(path)}
        for path in paths
    ]


def complex_fields(prefix: str, value: complex) -> dict[str, float]:
    return {
        f"{prefix}_real": float(value.real),
        f"{prefix}_imaginary": float(value.imag),
        f"{prefix}_magnitude": float(abs(value)),
    }


def relative_complex_difference(first: complex, second: complex) -> float:
    return abs(first - second) / max(abs(first), abs(second), 1.0e-300)


def local_context(
    base_context: dict[str, Any],
    angular_node: dict[str, Any],
) -> dict[str, Any]:
    context = dict(base_context)
    event = dict(base_context["source_event"])
    event["soft_cosine"] = float(angular_node["soft_cosine"])
    event["decay_cosine"] = float(angular_node["decay_cosine"])
    context["source_event"] = event
    return context


def build_material_problems(
    angular_node: dict[str, Any],
) -> dict[tuple[str, str], dict[str, Any]]:
    jobs = M5286.source_jobs()
    atlas = [
        row
        for row in read_csv(POLE_ATLAS_5286)
        if row["angular_node_id"] == angular_node["angular_node_id"]
        and parse_bool(row["pole_present"])
    ]
    keys = {
        (row["epsilon_id"], row["component_id"]) for row in atlas
    }
    return {
        key: M5286.angular_problem(
            jobs[key],
            float(angular_node["soft_cosine"]),
            float(angular_node["decay_cosine"]),
        )
        for key in keys
    }


def evaluate_component_cached(
    context: dict[str, Any],
    epsilon_id: str,
    component_id: str,
    energy: float,
    cache: dict[tuple[str, float, str], Any],
    convergence_audit: bool,
) -> dict[str, Any]:
    key = (epsilon_id, energy, component_id)
    if key in cache:
        return cache[key]
    event = dict(context["source_event"])
    event["soft_energy"] = energy
    target = context["inventories"][epsilon_id]["target"]
    rational_key = (epsilon_id, energy, "__ROOT_RATIONALS__")
    if rational_key not in cache:
        cache[rational_key] = M5280.M5274.M5231.root_rationals(
            event,
            target,
        )
    rationals = cache[rational_key]
    cache[key] = M5280.evaluate_component(
        event,
        epsilon_id,
        component_id,
        context,
        rationals=rationals,
        convergence_audit=convergence_audit,
    )
    return cache[key]


def derive_local_pole_residues(
    angular_node: dict[str, Any],
    context: dict[str, Any],
    problems: dict[tuple[str, str], dict[str, Any]],
    cache: dict[tuple[str, float, str], Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    atlas = [
        row
        for row in read_csv(POLE_ATLAS_5286)
        if row["angular_node_id"] == angular_node["angular_node_id"]
        and parse_bool(row["pole_present"])
    ]
    samples: list[dict[str, Any]] = []
    fits: list[dict[str, Any]] = []
    for source in atlas:
        key = (source["epsilon_id"], source["component_id"])
        surface_id = source["surface_id"]
        channel = M5286.channel_function(problems[key], surface_id)
        pole = complex(
            float(source["pole_real"]),
            float(source["pole_imaginary"]),
        )
        step = 1.0e-6
        derivative = (
            channel(pole + step) - channel(pole - step)
        ) / (2.0 * step)
        local_by_radius: dict[float, list[dict[str, Any]]] = {}
        for radius in FIT_RADII:
            local_by_radius[radius] = []
            for fraction in FIT_FRACTIONS:
                energy = pole.real + radius * fraction
                evaluation = evaluate_component_cached(
                    context,
                    key[0],
                    key[1],
                    energy,
                    cache,
                    convergence_audit=True,
                )
                contribution = complex(evaluation["residue"])
                channel_value = channel(complex(energy))
                numerator = channel_value * contribution
                row = {
                    "angular_node_id": angular_node["angular_node_id"],
                    "soft_cosine": angular_node["soft_cosine"],
                    "decay_cosine": angular_node["decay_cosine"],
                    "epsilon_id": key[0],
                    "component_id": key[1],
                    "surface_id": surface_id,
                    "pole_real": pole.real,
                    "pole_imaginary": pole.imag,
                    "radius": radius,
                    "fraction": fraction,
                    "energy": energy,
                    "mask_active": evaluation["mask_active"],
                    "channel_real": channel_value.real,
                    "channel_imaginary": channel_value.imag,
                    "contribution_real": contribution.real,
                    "contribution_imaginary": contribution.imag,
                    "numerator_real": numerator.real,
                    "numerator_imaginary": numerator.imag,
                    "coefficient_relative_change": evaluation[
                        "coefficient_relative_change"
                    ],
                    "valid_for_angular_node_pole_fit": True,
                    "valid_for_full_phase_space_coefficient": False,
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
                samples.append(row)
                local_by_radius[radius].append(row)
        fit_lookup: dict[tuple[float, int], dict[str, Any]] = {}
        for radius, local in local_by_radius.items():
            fractions = np.asarray(
                [float(row["fraction"]) for row in local],
                dtype=np.complex128,
            )
            numerators = np.asarray(
                [
                    complex(
                        float(row["numerator_real"]),
                        float(row["numerator_imaginary"]),
                    )
                    for row in local
                ],
                dtype=np.complex128,
            )
            scaled_pole = (pole - pole.real) / radius
            for degree in FIT_DEGREES:
                matrix = np.column_stack(
                    [
                        fractions**power
                        for power in range(degree + 1)
                    ]
                )
                coefficients, _, _, _ = np.linalg.lstsq(
                    matrix,
                    numerators,
                    rcond=None,
                )
                predicted = matrix @ coefficients
                numerator_at_pole = sum(
                    coefficients[power] * scaled_pole**power
                    for power in range(degree + 1)
                )
                residue = numerator_at_pole / derivative
                fit = {
                    "angular_node_id": angular_node["angular_node_id"],
                    "epsilon_id": key[0],
                    "component_id": key[1],
                    "surface_id": surface_id,
                    "pole_real": pole.real,
                    "pole_imaginary": pole.imag,
                    "channel_derivative_real": derivative.real,
                    "channel_derivative_imaginary": derivative.imag,
                    "radius": radius,
                    "degree": degree,
                    "fitted_residue_real": residue.real,
                    "fitted_residue_imaginary": residue.imag,
                    "fitted_residue_magnitude": abs(residue),
                    "fit_relative_residual": float(
                        np.max(np.abs(predicted - numerators))
                        / max(
                            float(np.max(np.abs(numerators))),
                            1.0e-300,
                        )
                    ),
                    "all_samples_mask_active": all(
                        parse_bool(row["mask_active"]) for row in local
                    ),
                    "all_samples_mask_inactive": all(
                        not parse_bool(row["mask_active"]) for row in local
                    ),
                    "maximum_coefficient_relative_change": max(
                        float(row["coefficient_relative_change"])
                        for row in local
                    ),
                    "valid_for_angular_node_pole_fit": True,
                    "valid_for_full_phase_space_coefficient": False,
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
                fits.append(fit)
                fit_lookup[(radius, degree)] = fit
        selected = fit_lookup[(FIT_RADII[-1], 3)]
        selected_value = complex(
            selected["fitted_residue_real"],
            selected["fitted_residue_imaginary"],
        )
        coarse_value = complex(
            fit_lookup[(FIT_RADII[0], 3)]["fitted_residue_real"],
            fit_lookup[(FIT_RADII[0], 3)]["fitted_residue_imaginary"],
        )
        degree_value = complex(
            fit_lookup[(FIT_RADII[-1], 4)]["fitted_residue_real"],
            fit_lookup[(FIT_RADII[-1], 4)]["fitted_residue_imaginary"],
        )
        refinement_change = relative_complex_difference(
            selected_value,
            coarse_value,
        )
        degree_change = relative_complex_difference(
            selected_value,
            degree_value,
        )
        active = parse_bool(selected["all_samples_mask_active"])
        inactive = parse_bool(selected["all_samples_mask_inactive"])
        controls_pass = (
            (active or inactive)
            and float(selected["fit_relative_residual"])
            <= FIT_RELATIVE_RESIDUAL_LIMIT
            and refinement_change
            <= FIT_REFINEMENT_RELATIVE_CHANGE_LIMIT
            and degree_change <= FIT_DEGREE_RELATIVE_CHANGE_LIMIT
            and float(selected["maximum_coefficient_relative_change"])
            <= COEFFICIENT_CONVERGENCE_LIMIT
        )
        selected.update(
            {
                "selected_fit": True,
                "exact_mask_pole_active": active,
                "true_limit_residue_real": (
                    selected_value.real if active else 0.0
                ),
                "true_limit_residue_imaginary": (
                    selected_value.imag if active else 0.0
                ),
                "refinement_relative_change": refinement_change,
                "degree_relative_change": degree_change,
                "pole_fit_controls_pass": controls_pass,
                "valid_for_angular_node_pole_subtraction": controls_pass,
            }
        )
    return samples, fits


def selected_poles(
    fits: list[dict[str, Any]],
) -> dict[tuple[str, str], dict[str, complex]]:
    return {
        (row["epsilon_id"], row["component_id"]): {
            "pole": complex(
                float(row["pole_real"]),
                float(row["pole_imaginary"]),
            ),
            "residue": complex(
                float(row["true_limit_residue_real"]),
                float(row["true_limit_residue_imaginary"]),
            ),
        }
        for row in fits
        if row.get("selected_fit")
        and parse_bool(row["exact_mask_pole_active"])
    }


def endpoint_refined_panels(
    base_panels: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    minimum = float(M5280.M5274.M5267.ENERGY_MINIMUM)
    maximum = float(M5280.M5274.M5267.ENERGY_MAXIMUM)
    boundaries = {
        float(row["lower"]) for row in base_panels
    } | {float(row["upper"]) for row in base_panels}
    for offset in ENDPOINT_REFINEMENT_OFFSETS:
        if minimum + offset < maximum:
            boundaries.add(minimum + offset)
        if maximum - offset > minimum:
            boundaries.add(maximum - offset)
    ordered = sorted(boundaries)
    return [
        {
            "panel_id": f"RP{index:03d}",
            "lower": left,
            "upper": right,
            "width": right - left,
            "midpoint": 0.5 * (left + right),
        }
        for index, (left, right) in enumerate(
            zip(ordered[:-1], ordered[1:]),
            start=1,
        )
    ]


def integrate_inner_energy(
    angular_node: dict[str, Any],
    context: dict[str, Any],
    poles: dict[tuple[str, str], dict[str, complex]],
    cache: dict[tuple[str, float, str], Any],
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    list[dict[str, Any]],
]:
    mask_boundaries = M5280.exact_energy_mask_boundaries(context)
    pole_centers = [
        {"center": value["pole"].real} for value in poles.values()
    ]
    panels = endpoint_refined_panels(
        M5280.composite_panel_rows(mask_boundaries, pole_centers)
    )
    minimum = float(M5280.M5274.M5267.ENERGY_MINIMUM)
    maximum = float(M5280.M5274.M5267.ENERGY_MAXIMUM)
    analytic = {
        key: value["residue"]
        * (
            cmath.log(maximum - value["pole"])
            - cmath.log(minimum - value["pole"])
        )
        for key, value in poles.items()
    }
    node_rows: list[dict[str, Any]] = []
    component_rows: list[dict[str, Any]] = []
    regulator_rows: list[dict[str, Any]] = []
    audit_counter = 0
    for epsilon_id in REGULATOR_IDS:
        for order in ENERGY_ORDERS:
            nodes, weights = np.polynomial.legendre.leggauss(order)
            raw_components = defaultdict(complex)
            regular_components = defaultdict(complex)
            for panel in panels:
                left = float(panel["lower"])
                right = float(panel["upper"])
                half_width = 0.5 * (right - left)
                midpoint = 0.5 * (right + left)
                for local_index, (node, weight) in enumerate(
                    zip(nodes, weights),
                    start=1,
                ):
                    energy = midpoint + half_width * float(node)
                    mapped_weight = half_width * float(weight)
                    audit_counter += 1
                    audit = audit_counter % 96 == 0
                    for component_id in COMPONENT_IDS:
                        evaluation = evaluate_component_cached(
                            context,
                            epsilon_id,
                            component_id,
                            energy,
                            cache,
                            convergence_audit=audit,
                        )
                        raw = complex(evaluation["residue"])
                        pole = poles.get((epsilon_id, component_id))
                        singular = (
                            pole["residue"] / (energy - pole["pole"])
                            if pole is not None
                            else 0.0j
                        )
                        regular = raw - singular
                        raw_components[component_id] += mapped_weight * raw
                        regular_components[
                            component_id
                        ] += mapped_weight * regular
                        node_rows.append(
                            {
                                "angular_node_id": angular_node[
                                    "angular_node_id"
                                ],
                                "soft_cosine": angular_node[
                                    "soft_cosine"
                                ],
                                "decay_cosine": angular_node[
                                    "decay_cosine"
                                ],
                                "epsilon_id": epsilon_id,
                                "energy_order": order,
                                "panel_id": panel["panel_id"],
                                "local_node_index": local_index,
                                "soft_energy": energy,
                                "mapped_energy_weight": mapped_weight,
                                "component_id": component_id,
                                "mask_active": evaluation["mask_active"],
                                **complex_fields("raw_residue", raw),
                                **complex_fields(
                                    "subtracted_singular",
                                    singular,
                                ),
                                **complex_fields(
                                    "regularized_residue",
                                    regular,
                                ),
                                "coefficient_relative_change": evaluation[
                                    "coefficient_relative_change"
                                ],
                                "convergence_audited": evaluation[
                                    "convergence_audited"
                                ],
                                "valid_for_order2_angular_inner_smoke": True,
                                "valid_for_full_phase_space_coefficient": False,
                                "valid_for_numeric_UV_claim": False,
                                "valid_for_local_GR_claim": False,
                                "valid_for_full_MTS_claim": False,
                            }
                        )
                atomic_json(
                    STATUS,
                    {
                        "checkpoint": CHECKPOINT,
                        "state": "RUNNING",
                        "angular_node_id": angular_node[
                            "angular_node_id"
                        ],
                        "epsilon_id": epsilon_id,
                        "energy_order": order,
                        "last_panel_id": panel["panel_id"],
                        "energy_component_node_row_count": len(node_rows),
                    },
                )
            corrected = dict(regular_components)
            for component_id in COMPONENT_IDS:
                corrected.setdefault(component_id, 0.0j)
                corrected[component_id] += analytic.get(
                    (epsilon_id, component_id),
                    0.0j,
                )
                component_rows.append(
                    {
                        "angular_node_id": angular_node[
                            "angular_node_id"
                        ],
                        "epsilon_id": epsilon_id,
                        "energy_order": order,
                        "component_id": component_id,
                        **complex_fields(
                            "corrected_energy_integral",
                            corrected[component_id],
                        ),
                        "valid_for_order2_angular_inner_smoke": True,
                        "valid_for_full_phase_space_coefficient": False,
                        "valid_for_numeric_UV_claim": False,
                        "valid_for_local_GR_claim": False,
                        "valid_for_full_MTS_claim": False,
                    }
                )
            eight = sum(corrected.values(), 0.0j)
            six = sum(
                corrected[component_id]
                for component_id in LEGACY_SIX_IDS
            )
            hidden = sum(
                corrected[component_id] for component_id in HIDDEN_IDS
            )
            regulator_rows.append(
                {
                    "angular_node_id": angular_node["angular_node_id"],
                    "soft_cosine": angular_node["soft_cosine"],
                    "decay_cosine": angular_node["decay_cosine"],
                    "row_type": "REGULATOR_INNER_ENERGY",
                    "epsilon_id": epsilon_id,
                    "energy_order": order,
                    **complex_fields("eight_component_integral", eight),
                    **complex_fields("six_component_integral", six),
                    **complex_fields("hidden_component_integral", hidden),
                    "energy_panel_count": len(panels),
                    "exact_mask_boundary_count": len(mask_boundaries),
                    "active_material_pole_count": sum(
                        key[0] == epsilon_id for key in poles
                    ),
                    "valid_for_order2_angular_inner_smoke": True,
                    "valid_for_full_phase_space_coefficient": False,
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
            )
    parent_total = next(
        row
        for row in read_csv(M5283.TOTALS_5281)
        if row["row_type"] == "PHYSICAL_ENERGY_EXTRAPOLATION"
    )
    multiplier = float(parent_total["kernel_multiplier"]) * float(
        parent_total["physical_A00_weight"]
    )
    lookup = {
        (int(row["energy_order"]), row["epsilon_id"]): row
        for row in regulator_rows
    }
    total_rows = list(regulator_rows)
    for order in ENERGY_ORDERS:
        local = {}
        for epsilon_id in REGULATOR_IDS:
            row = lookup[(order, epsilon_id)]
            local[epsilon_id] = {
                channel: complex(
                    float(row[f"{channel}_real"]),
                    float(row[f"{channel}_imaginary"]),
                )
                for channel in (
                    "eight_component_integral",
                    "six_component_integral",
                    "hidden_component_integral",
                )
            }
        physical = {
            channel: multiplier
            * (2.0 * local["E020"][channel] - local["E040"][channel])
            for channel in local["E040"]
        }
        total_rows.append(
            {
                "angular_node_id": angular_node["angular_node_id"],
                "soft_cosine": angular_node["soft_cosine"],
                "decay_cosine": angular_node["decay_cosine"],
                "row_type": "PHYSICAL_INNER_ENERGY",
                "epsilon_id": "2E020_MINUS_E040",
                "energy_order": order,
                **complex_fields(
                    "eight_component_integral",
                    physical["eight_component_integral"],
                ),
                **complex_fields(
                    "six_component_integral",
                    physical["six_component_integral"],
                ),
                **complex_fields(
                    "hidden_component_integral",
                    physical["hidden_component_integral"],
                ),
                "valid_for_order2_angular_inner_smoke": True,
                "valid_for_full_phase_space_coefficient": False,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    return node_rows, component_rows, total_rows


def convergence_rows(
    totals: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for node_id in {
        row["angular_node_id"]
        for row in totals
        if row["row_type"] == "PHYSICAL_INNER_ENERGY"
    }:
        local = {
            int(row["energy_order"]): row
            for row in totals
            if row["angular_node_id"] == node_id
            and row["row_type"] == "PHYSICAL_INNER_ENERGY"
        }
        for channel in (
            "eight_component_integral",
            "six_component_integral",
            "hidden_component_integral",
        ):
            lower = complex(
                float(local[4][f"{channel}_real"]),
                float(local[4][f"{channel}_imaginary"]),
            )
            upper = complex(
                float(local[8][f"{channel}_real"]),
                float(local[8][f"{channel}_imaginary"]),
            )
            rows.append(
                {
                    "angular_node_id": node_id,
                    "channel": channel,
                    "lower_energy_order": 4,
                    "upper_energy_order": 8,
                    **complex_fields("lower_value", lower),
                    **complex_fields("upper_value", upper),
                    "relative_change": relative_complex_difference(
                        lower,
                        upper,
                    ),
                    "valid_for_inner_energy_convergence_smoke": True,
                    "valid_for_full_phase_space_coefficient": False,
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
            )
    return rows


def outer_rows(
    angular_nodes: list[dict[str, str]],
    inner_totals: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    weights = {
        row["angular_node_id"]: (
            float(row["angular_weight"])
            * float(row["angular_jacobian"])
        )
        for row in angular_nodes
    }
    rows: list[dict[str, Any]] = []
    for order in ENERGY_ORDERS:
        values = {}
        for channel in (
            "eight_component_integral",
            "six_component_integral",
            "hidden_component_integral",
        ):
            values[channel] = sum(
                weights[row["angular_node_id"]]
                * complex(
                    float(row[f"{channel}_real"]),
                    float(row[f"{channel}_imaginary"]),
                )
                for row in inner_totals
                if row["row_type"] == "PHYSICAL_INNER_ENERGY"
                and int(row["energy_order"]) == order
            )
        rows.append(
            {
                "angular_order": 2,
                "energy_order": order,
                **complex_fields(
                    "eight_component_integral",
                    values["eight_component_integral"],
                ),
                **complex_fields(
                    "six_component_integral",
                    values["six_component_integral"],
                ),
                **complex_fields(
                    "hidden_component_integral",
                    values["hidden_component_integral"],
                ),
                "angular_endpoint_limit": float(
                    M5280.M5274.M5270.ANGULAR_LIMIT
                ),
                "angular_jacobian": M5280.M5278.ANGULAR_JACOBIAN,
                "valid_for_order2_angular_inner_smoke": True,
                "valid_for_angular_convergence": False,
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
        SCRIPT_5286,
        RESULT_5286,
        VALIDATION_5286,
        ANGULAR_NODES_5286,
        POLE_ATLAS_5286,
    )
    parent = read_json(RESULT_5286)
    checks = {
        "required_sources_exist": all(path.exists() for path in required),
        "parent_5286_accepted": bool(parent["acceptance_passed"]),
        "parent_5286_validated": all(
            parse_bool(row["passed"]) for row in read_csv(VALIDATION_5286)
        ),
        "inner_energy_smoke_authorized": bool(
            parent["claim_boundary"]["valid_for_inner_energy_smoke"]
        ),
        "four_angular_nodes_parse": len(read_csv(ANGULAR_NODES_5286)) == 4,
        "formalization_workbench_unchanged": (
            M5283.formal_inventory_digest()
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
        "estimated_maximum_component_evaluations": (
            4
            * 2
            * 60
            * sum(ENERGY_ORDERS)
            * len(COMPONENT_IDS)
        ),
        "decision": (
            "DRY_RUN_ACCEPTED__RUN_ORDER2_ANGULAR_INNER_ENERGY_SMOKE"
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
    mp.mp.dps = M5280.MP_DECIMAL_DIGITS
    dry = dry_run()
    if not dry["acceptance_passed"]:
        raise RuntimeError("5287 dry run did not pass")
    parent = read_json(RESULT_5286)
    angular_nodes = read_csv(ANGULAR_NODES_5286)
    base_context = M5280.source_context()
    all_samples: list[dict[str, Any]] = []
    all_fits: list[dict[str, Any]] = []
    all_energy_nodes: list[dict[str, Any]] = []
    all_components: list[dict[str, Any]] = []
    all_totals: list[dict[str, Any]] = []
    for angular_node in angular_nodes:
        context = local_context(base_context, angular_node)
        problems = build_material_problems(angular_node)
        cache: dict[tuple[str, float, str], Any] = {}
        samples, fits = derive_local_pole_residues(
            angular_node,
            context,
            problems,
            cache,
        )
        poles = selected_poles(fits)
        energy_nodes, component_rows, total_rows = integrate_inner_energy(
            angular_node,
            context,
            poles,
            cache,
        )
        all_samples.extend(samples)
        all_fits.extend(fits)
        all_energy_nodes.extend(energy_nodes)
        all_components.extend(component_rows)
        all_totals.extend(total_rows)
        write_csv(POLE_SAMPLE_ROWS, all_samples)
        write_csv(POLE_FIT_ROWS, all_fits)
        write_csv(ENERGY_NODE_ROWS, all_energy_nodes)
        write_csv(INNER_COMPONENT_ROWS, all_components)
        write_csv(INNER_TOTAL_ROWS, all_totals)
        atomic_json(
            STATUS,
            {
                "checkpoint": CHECKPOINT,
                "state": "RUNNING",
                "last_completed_angular_node_id": angular_node[
                    "angular_node_id"
                ],
                "completed_angular_node_count": len(
                    {
                        row["angular_node_id"]
                        for row in all_totals
                        if row["row_type"] == "PHYSICAL_INNER_ENERGY"
                    }
                ),
                "energy_component_node_row_count": len(all_energy_nodes),
            },
        )
    convergence = convergence_rows(all_totals)
    outer = outer_rows(angular_nodes, all_totals)
    selected_fits = [
        row for row in all_fits if row.get("selected_fit")
    ]
    maximum_fit_residual = max(
        (
            float(row["fit_relative_residual"]) for row in selected_fits
        ),
        default=0.0,
    )
    maximum_fit_refinement_change = max(
        (
            float(row["refinement_relative_change"])
            for row in selected_fits
        ),
        default=0.0,
    )
    maximum_fit_degree_change = max(
        (
            float(row["degree_relative_change"])
            for row in selected_fits
        ),
        default=0.0,
    )
    pole_fit_controls_pass = all(
        parse_bool(row["pole_fit_controls_pass"]) for row in selected_fits
    )
    inner_eight_changes = [
        float(row["relative_change"])
        for row in convergence
        if row["channel"] == "eight_component_integral"
    ]
    maximum_inner_change = max(inner_eight_changes)
    outer_lookup = {
        int(row["energy_order"]): row for row in outer
    }
    outer_change = relative_complex_difference(
        complex(
            float(outer_lookup[4]["eight_component_integral_real"]),
            float(outer_lookup[4]["eight_component_integral_imaginary"]),
        ),
        complex(
            float(outer_lookup[8]["eight_component_integral_real"]),
            float(outer_lookup[8]["eight_component_integral_imaginary"]),
        ),
    )
    inner_energy_smoke_passed = (
        pole_fit_controls_pass
        and maximum_inner_change <= INNER_RELATIVE_CHANGE_LIMIT
        and outer_change <= OUTER_RELATIVE_CHANGE_LIMIT
    )
    audited = [
        row
        for row in all_energy_nodes
        if parse_bool(row["convergence_audited"])
        and parse_bool(row["mask_active"])
    ]
    maximum_coefficient_change = max(
        (
            float(row["coefficient_relative_change"]) for row in audited
        ),
        default=0.0,
    )
    checks = {
        "all_four_angular_nodes_integrated": (
            {
                row["angular_node_id"]
                for row in all_totals
                if row["row_type"] == "PHYSICAL_INNER_ENERGY"
            }
            == {row["angular_node_id"] for row in angular_nodes}
        ),
        "all_selected_pole_fits_controlled": pole_fit_controls_pass,
        "all_audited_coefficients_converged": (
            bool(audited)
            and maximum_coefficient_change
            <= COEFFICIENT_CONVERGENCE_LIMIT
        ),
        "orders_4_and_8_completed": (
            {
                int(row["energy_order"])
                for row in all_totals
                if row["row_type"] == "PHYSICAL_INNER_ENERGY"
            }
            == set(ENERGY_ORDERS)
        ),
        "outer_smoke_rows_finite": all(
            math.isfinite(float(value))
            for row in outer
            for field, value in row.items()
            if field.endswith(("_real", "_imaginary", "_magnitude"))
        ),
        "formalization_workbench_unchanged": (
            M5283.formal_inventory_digest()
            == str(parent["formalization_workbench_end_digest"])
        ),
        "claims_locked_false": True,
    }
    accepted = all(checks.values())
    high_order_outer = outer_lookup[8]
    formal_end = M5283.formal_inventory_digest()
    result = {
        "checkpoint": CHECKPOINT,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "mode": "order2-angular-inner-energy-smoke",
        "checks": checks,
        "acceptance_passed": accepted,
        "angular_node_count": len(angular_nodes),
        "pole_sample_count": len(all_samples),
        "pole_fit_candidate_count": len(all_fits),
        "selected_pole_fit_count": len(selected_fits),
        "active_selected_pole_count": sum(
            parse_bool(row["exact_mask_pole_active"])
            for row in selected_fits
        ),
        "energy_component_node_row_count": len(all_energy_nodes),
        "maximum_selected_pole_fit_residual": maximum_fit_residual,
        "maximum_pole_fit_refinement_change": (
            maximum_fit_refinement_change
        ),
        "maximum_pole_fit_degree_change": maximum_fit_degree_change,
        "maximum_audited_coefficient_relative_change": (
            maximum_coefficient_change
        ),
        "maximum_node_inner_energy_relative_change": maximum_inner_change,
        "outer_energy_order_relative_change": outer_change,
        "inner_energy_smoke_passed": inner_energy_smoke_passed,
        "order2_energy8_eight_component_integral": {
            "real": float(
                high_order_outer["eight_component_integral_real"]
            ),
            "imaginary": float(
                high_order_outer["eight_component_integral_imaginary"]
            ),
        },
        "source_files": source_rows(),
        "formalization_workbench_reference_digest": str(
            parent["formalization_workbench_end_digest"]
        ),
        "formalization_workbench_end_digest": formal_end,
        "formalization_workbench_modified_file_count": (
            0
            if formal_end == str(parent["formalization_workbench_end_digest"])
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
            (
                "ACCEPT_ORDER2_ANGULAR_INNER_ENERGY_SMOKE__"
                "BUILD_ADAPTIVE_ANGULAR_CONVERGENCE_RUNNER"
            )
            if accepted and inner_energy_smoke_passed
            else (
                "ORDER2_INNER_ENERGY_SMOKE_VALID_BUT_NOT_CONVERGED__"
                "LOCALIZE_FAILED_ANGULAR_NODE"
                if accepted
                else "ORDER2_ANGULAR_INNER_ENERGY_RUN_REQUIRES_REPAIR"
            )
        ),
        "claim_boundary": {
            "valid_for_order2_angular_inner_energy_smoke": (
                accepted and inner_energy_smoke_passed
            ),
            "valid_for_adaptive_angular_convergence_runner": (
                accepted and inner_energy_smoke_passed
            ),
            "valid_for_angular_convergence": False,
            "valid_for_full_phase_space_coefficient": False,
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
            "reason": (
                "The order-two outer rule is only a smoke test. Angular "
                "convergence and angular endpoint-cap control remain open."
            ),
        },
    }
    write_csv(INNER_CONVERGENCE_ROWS, convergence)
    write_csv(OUTER_ROWS, outer)
    atomic_json(RESULT, result)
    atomic_json(
        STATUS,
        {
            "checkpoint": CHECKPOINT,
            "state": "COMPLETED",
            "mode": result["mode"],
            "acceptance_passed": accepted,
            "inner_energy_smoke_passed": inner_energy_smoke_passed,
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
    return {"gate_id": gate_id, "passed": passed, "detail": detail}


def render_document(
    result: dict[str, Any],
    validation_passed: bool,
) -> None:
    value = result["order2_energy8_eight_component_integral"]
    text = f"""# 5287 — Order-two angular inner-energy smoke

## Purpose

This is the first nested calculation after the fixed-angle certificate.
At each of four angular Gauss nodes it:

1. rebuilds the local material-channel problems;
2. classifies exact-mask activity at each geometric pole;
3. derives active residues as `N(E_p)/D'(E_p)`;
4. constructs exact mask and endpoint-refined energy panels;
5. compares inner Gauss orders 4 and 8;
6. forms the physical two-regulator and order-two angular sum.

## Result

- selected active poles:
  `{result['active_selected_pole_count']}`;
- energy component-node rows:
  `{result['energy_component_node_row_count']}`;
- maximum pole-fit residual:
  `{result['maximum_selected_pole_fit_residual']:.12g}`;
- maximum nodewise inner-energy change:
  `{result['maximum_node_inner_energy_relative_change']:.12g}`;
- outer order-4 to order-8 change:
  `{result['outer_energy_order_relative_change']:.12g}`;
- order-two / energy-order-eight value:
  `{value['real']:.12g}{value['imaginary']:+.12g}i`;
- inner smoke passed:
  `{result['inner_energy_smoke_passed']}`.

Decision:
`{result['decision']}`.

Validation: **{'PASS' if validation_passed else 'FAIL'}**.

## Claim boundary

No angular-convergence or full phase-space claim is made. Passing this
checkpoint only authorizes an adaptive angular convergence runner.
"""
    DOCUMENT.write_text(text, encoding="utf-8")


def validate_outputs() -> dict[str, Any]:
    result = read_json(RESULT)
    required_csvs = (
        POLE_SAMPLE_ROWS,
        POLE_FIT_ROWS,
        ENERGY_NODE_ROWS,
        INNER_COMPONENT_ROWS,
        INNER_TOTAL_ROWS,
        INNER_CONVERGENCE_ROWS,
        OUTER_ROWS,
    )
    csv_rows = {
        str(path): read_csv(path)
        for path in required_csvs
        if path.exists()
    }
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
    source_files = result["source_files"]
    current_formal_digest = M5283.formal_inventory_digest()
    reference_formal_digest = str(
        result["formalization_workbench_reference_digest"]
    )
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
            "PARENT_5286_ACCEPTED",
            bool(read_json(RESULT_5286)["acceptance_passed"]),
            str(read_json(RESULT_5286)["decision"]),
        ),
        validation_gate(
            "INNER_PIPELINE_ACCEPTED",
            bool(result["acceptance_passed"]),
            str(result["decision"]),
        ),
        validation_gate(
            "REQUIRED_CSVS_PARSE",
            len(csv_rows) == len(required_csvs) and all(csv_rows.values()),
            f"{len(csv_rows)}/{len(required_csvs)} non-empty CSVs",
        ),
        validation_gate(
            "FOUR_ANGULAR_NODES_COMPLETED",
            result["angular_node_count"] == 4,
            str(result["angular_node_count"]),
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
                and result["resource_contract"]["worker_math_threads"] == 1
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
            "VALIDATED_ORDER2_ANGULAR_INNER_ENERGY_SMOKE"
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
