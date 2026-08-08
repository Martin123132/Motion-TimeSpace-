from __future__ import annotations

import argparse
import cmath
import csv
import ctypes
import hashlib
import importlib.util
import itertools
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
FORMAL = ROOT / "formalization-workbench"
SCRIPTS = POST / "scripts"
FUNCTIONAL_RG = POST / "source-intake" / "functional_rg"
RESIDUALS = POST / "source-intake" / "mts_residuals"
SOURCE = FUNCTIONAL_RG / "5284"

SCRIPT_5280 = (
    SCRIPTS
    / "Y5_R2FR_5280_algebraic_selector_energy_pole_subtracted_smoke.py"
)
SCRIPT_5283 = (
    SCRIPTS / "Y5_R2FR_5283_two_pole_stored_node_reassembly.py"
)
NODES_5281 = (
    FUNCTIONAL_RG / "5281" / "high_order_energy_component_nodes.csv"
)
POLE_FITS_5282 = (
    FUNCTIONAL_RG / "5282" / "true_limit_exact_active_pole_fits.csv"
)
RESULT_5282 = (
    FUNCTIONAL_RG / "5282" / "exact_mask_energy_pole_result.json"
)
RESULT_5283 = (
    FUNCTIONAL_RG / "5283" / "two_pole_stored_node_reassembly_result.json"
)
VALIDATION_5283 = (
    FUNCTIONAL_RG / "5283" / "two_pole_stored_node_reassembly_validation.csv"
)
TOTALS_5283 = FUNCTIONAL_RG / "5283" / "two_pole_energy_totals.csv"
PANELS_5280 = FUNCTIONAL_RG / "5280" / "composite_energy_panels.csv"
TOTALS_5281 = FUNCTIONAL_RG / "5281" / "high_order_energy_totals.csv"

DRY_RUN = SOURCE / "pole_residue_refinement_dry_run.json"
SAMPLE_ROWS = SOURCE / "pole_numerator_samples.csv"
FIT_ROWS = SOURCE / "pole_numerator_fit_candidates.csv"
SELECTED_ROWS = SOURCE / "selected_refined_pole_residues.csv"
ENSEMBLE_ROWS = SOURCE / "physical_residue_ensemble.csv"
ENERGY_TOTALS = SOURCE / "refined_two_pole_energy_totals.csv"
CONVERGENCE_ROWS = SOURCE / "refined_two_pole_convergence.csv"
RESULT = SOURCE / "pole_residue_refinement_result.json"
VALIDATION = SOURCE / "pole_residue_refinement_validation.csv"
RESIDUAL_VALIDATION = (
    RESIDUALS / "P8_Y5_BRR545_5284_VALIDATION.csv"
)
STATUS = SOURCE / "status.json"
DOCUMENT = (
    POST
    / "5284-Y5-R2FR-pole-residue-refinement-and-cancellation-certificate.md"
)

CHECKPOINT = 5284
PARENT_CHECKPOINT = 5283
MARKER = "MTS_5284_POLE_RESIDUE_REFINEMENT_CANCELLATION_CERTIFICATE"
REVISION = "pole-residue-refinement-cancellation-certificate-v1"
MATERIAL_COMPONENT_IDS = ("MC04", "MC12")
REGULATOR_IDS = ("E040", "E020")
FIT_FRACTIONS = (-1.0, -0.5, -0.2, -0.1, 0.1, 0.2, 0.5, 1.0)
FIT_DEGREES = (2, 3, 4)
POLE_TO_RADIUS_RATIO_LIMIT = 0.5
FIT_RELATIVE_RESIDUAL_LIMIT = 5.0e-5
REFINEMENT_RELATIVE_CHANGE_LIMIT = 2.0e-5
DEGREE_RELATIVE_CHANGE_LIMIT = 2.0e-5
COEFFICIENT_CONVERGENCE_LIMIT = 1.0e-6
PHYSICAL_ENSEMBLE_RELATIVE_SPREAD_LIMIT = 1.0e-2
MID_ORDER_RELATIVE_CHANGE_LIMIT = 5.0e-3
HIGH_ORDER_RELATIVE_CHANGE_LIMIT = 1.0e-3
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


M5280 = load_module("mts_5280_for_5284", SCRIPT_5280)
M5283 = load_module("mts_5283_for_5284", SCRIPT_5283)
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


def source_rows() -> list[dict[str, str]]:
    paths = (
        Path(__file__).resolve(),
        SCRIPT_5280,
        SCRIPT_5283,
        NODES_5281,
        POLE_FITS_5282,
        RESULT_5282,
        RESULT_5283,
        VALIDATION_5283,
        TOTALS_5283,
        PANELS_5280,
        TOTALS_5281,
    )
    return [
        {"path": str(path), "sha256": digest(path)}
        for path in paths
    ]


def parse_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    return str(value).strip().lower() == "true"


def relative_complex_difference(first: complex, second: complex) -> float:
    return abs(first - second) / max(abs(first), abs(second), 1.0e-300)


def material_source_rows() -> list[dict[str, str]]:
    return [
        row
        for row in read_csv(POLE_FITS_5282)
        if parse_bool(row["material_pole"])
    ]


def admissible_radii(source: dict[str, str]) -> list[float]:
    base = float(source["fit_radius"])
    pole = complex(
        float(source["pole_real"]),
        float(source["pole_imaginary"]),
    )
    radii: list[float] = []
    for refinement in range(8):
        radius = base * 0.5**refinement
        if abs(pole - float(source["center"])) / radius > (
            POLE_TO_RADIUS_RATIO_LIMIT
        ):
            break
        radii.append(radius)
    if len(radii) < 2:
        raise RuntimeError("insufficient admissible residue refinements")
    return radii


def evaluate_samples_and_fits(
    context: dict[str, Any],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    samples: list[dict[str, Any]] = []
    fits: list[dict[str, Any]] = []
    cache: dict[tuple[str, str, float], dict[str, Any]] = {}
    for source in material_source_rows():
        epsilon_id = source["epsilon_id"]
        component_id = source["component_id"]
        center = float(source["center"])
        pole = complex(
            float(source["pole_real"]),
            float(source["pole_imaginary"]),
        )
        for refinement, radius in enumerate(admissible_radii(source)):
            local_samples: list[dict[str, Any]] = []
            for fraction in FIT_FRACTIONS:
                offset = radius * fraction
                energy = center + offset
                cache_key = (epsilon_id, component_id, energy)
                if cache_key not in cache:
                    event = dict(context["source_event"])
                    event["soft_energy"] = energy
                    cache[cache_key] = M5280.evaluate_component(
                        event,
                        epsilon_id,
                        component_id,
                        context,
                        convergence_audit=True,
                    )
                evaluation = cache[cache_key]
                contribution = complex(evaluation["residue"])
                numerator = (energy - pole) * contribution
                sample = {
                    "epsilon_id": epsilon_id,
                    "component_id": component_id,
                    "refinement": refinement,
                    "radius": radius,
                    "fraction": fraction,
                    "offset": offset,
                    "energy": energy,
                    "pole_real": pole.real,
                    "pole_imaginary": pole.imag,
                    "contribution_real": contribution.real,
                    "contribution_imaginary": contribution.imag,
                    "numerator_real": numerator.real,
                    "numerator_imaginary": numerator.imag,
                    "mask_active": evaluation["mask_active"],
                    "coefficient_relative_change": evaluation[
                        "coefficient_relative_change"
                    ],
                    "root_equation_residual": evaluation[
                        "root_equation_residual"
                    ],
                    "root_refinement_chordal_distance": evaluation[
                        "root_refinement_chordal_distance"
                    ],
                    "valid_for_pole_residue_refinement": True,
                    "valid_for_full_phase_space_coefficient": False,
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
                samples.append(sample)
                local_samples.append(sample)
            scaled_pole = (pole - center) / radius
            scaled_offsets = np.asarray(
                [row["fraction"] for row in local_samples],
                dtype=np.complex128,
            )
            numerators = np.asarray(
                [
                    complex(
                        row["numerator_real"],
                        row["numerator_imaginary"],
                    )
                    for row in local_samples
                ],
                dtype=np.complex128,
            )
            for degree in FIT_DEGREES:
                matrix = np.column_stack(
                    [
                        scaled_offsets**power
                        for power in range(degree + 1)
                    ]
                )
                coefficients, _, _, _ = np.linalg.lstsq(
                    matrix,
                    numerators,
                    rcond=None,
                )
                predicted = matrix @ coefficients
                fitted_residue = sum(
                    coefficients[power] * scaled_pole**power
                    for power in range(degree + 1)
                )
                fit_residual = float(
                    np.max(np.abs(predicted - numerators))
                    / max(float(np.max(np.abs(numerators))), 1.0e-300)
                )
                fits.append(
                    {
                        "epsilon_id": epsilon_id,
                        "component_id": component_id,
                        "refinement": refinement,
                        "radius": radius,
                        "degree": degree,
                        "scaled_pole_magnitude": abs(scaled_pole),
                        "sample_count": len(local_samples),
                        "fitted_residue_real": fitted_residue.real,
                        "fitted_residue_imaginary": fitted_residue.imag,
                        "fitted_residue_magnitude": abs(fitted_residue),
                        "fit_relative_residual": fit_residual,
                        "all_samples_mask_active": all(
                            parse_bool(row["mask_active"])
                            for row in local_samples
                        ),
                        "maximum_coefficient_relative_change": max(
                            float(row["coefficient_relative_change"])
                            for row in local_samples
                        ),
                        "valid_for_pole_residue_refinement": True,
                        "valid_for_full_phase_space_coefficient": False,
                        "valid_for_numeric_UV_claim": False,
                        "valid_for_local_GR_claim": False,
                        "valid_for_full_MTS_claim": False,
                    }
                )
    return samples, fits


def select_residues(
    fits: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    selected_rows: list[dict[str, Any]] = []
    for epsilon_id in REGULATOR_IDS:
        for component_id in MATERIAL_COMPONENT_IDS:
            local = [
                row
                for row in fits
                if row["epsilon_id"] == epsilon_id
                and row["component_id"] == component_id
            ]
            highest = max(int(row["refinement"]) for row in local)
            selected = next(
                row
                for row in local
                if int(row["refinement"]) == highest
                and int(row["degree"]) == 3
            )
            previous = next(
                row
                for row in local
                if int(row["refinement"]) == highest - 1
                and int(row["degree"]) == 3
            )
            selected_value = complex(
                selected["fitted_residue_real"],
                selected["fitted_residue_imaginary"],
            )
            previous_value = complex(
                previous["fitted_residue_real"],
                previous["fitted_residue_imaginary"],
            )
            same_level = [
                row
                for row in local
                if int(row["refinement"]) == highest
            ]
            degree_change = max(
                relative_complex_difference(
                    selected_value,
                    complex(
                        row["fitted_residue_real"],
                        row["fitted_residue_imaginary"],
                    ),
                )
                for row in same_level
            )
            refinement_change = relative_complex_difference(
                selected_value,
                previous_value,
            )
            fit_controls_pass = (
                float(selected["fit_relative_residual"])
                <= FIT_RELATIVE_RESIDUAL_LIMIT
                and refinement_change
                <= REFINEMENT_RELATIVE_CHANGE_LIMIT
                and degree_change <= DEGREE_RELATIVE_CHANGE_LIMIT
                and parse_bool(selected["all_samples_mask_active"])
                and float(selected["maximum_coefficient_relative_change"])
                <= COEFFICIENT_CONVERGENCE_LIMIT
            )
            pole_source = next(
                row
                for row in material_source_rows()
                if row["epsilon_id"] == epsilon_id
                and row["component_id"] == component_id
            )
            selected_rows.append(
                {
                    "epsilon_id": epsilon_id,
                    "component_id": component_id,
                    "selected_refinement": highest,
                    "selected_degree": 3,
                    "center": pole_source["center"],
                    "pole_real": pole_source["pole_real"],
                    "pole_imaginary": pole_source["pole_imaginary"],
                    "true_limit_residue_real": selected_value.real,
                    "true_limit_residue_imaginary": selected_value.imag,
                    "true_limit_residue_magnitude": abs(selected_value),
                    "fit_relative_residual": selected[
                        "fit_relative_residual"
                    ],
                    "refinement_relative_change": refinement_change,
                    "degree_relative_change": degree_change,
                    "maximum_coefficient_relative_change": selected[
                        "maximum_coefficient_relative_change"
                    ],
                    "fit_controls_pass": fit_controls_pass,
                    "valid_for_refined_pole_subtraction": fit_controls_pass,
                    "valid_for_full_phase_space_coefficient": False,
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
            )
    return selected_rows


def selected_pole_dictionary(
    selected: list[dict[str, Any]],
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
        for row in selected
    }


def physical_row(
    totals: list[dict[str, Any]],
    order: int,
) -> dict[str, Any]:
    return next(
        row
        for row in totals
        if row["row_type"] == "PHYSICAL_ENERGY_EXTRAPOLATION"
        and int(row["quadrature_order"]) == order
    )


def pole_sensitivities(
    source_nodes: list[dict[str, str]],
    selected_poles: dict[tuple[str, str], dict[str, complex]],
    constants: dict[str, float],
    order: int,
) -> dict[tuple[str, str], complex]:
    sums: defaultdict[tuple[str, str], complex] = defaultdict(complex)
    for row in source_nodes:
        if int(row["quadrature_order"]) != order:
            continue
        key = (row["epsilon_id"], row["component_id"])
        if key not in selected_poles:
            continue
        pole = selected_poles[key]["pole"]
        sums[key] += float(row["mapped_weight"]) / (
            float(row["soft_energy"]) - pole
        )
    minimum = constants["energy_minimum"]
    maximum = constants["energy_maximum"]
    multiplier = (
        constants["kernel_multiplier"] * constants["physical_A00_weight"]
    )
    sensitivities: dict[tuple[str, str], complex] = {}
    for key, value in selected_poles.items():
        logarithm = cmath.log(maximum - value["pole"]) - cmath.log(
            minimum - value["pole"]
        )
        regulator_factor = 2.0 if key[0] == "E020" else -1.0
        sensitivities[key] = (
            multiplier * regulator_factor * (logarithm - sums[key])
        )
    return sensitivities


def ensemble_rows(
    fits: list[dict[str, Any]],
    selected: list[dict[str, Any]],
    source_nodes: list[dict[str, str]],
    constants: dict[str, float],
    refined_totals: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    selected_poles = selected_pole_dictionary(selected)
    sensitivities = pole_sensitivities(
        source_nodes,
        selected_poles,
        constants,
        order=16,
    )
    baseline = M5283.complex_from_row(
        physical_row(refined_totals, 16),
        "subtracted_eight_integral",
    )
    keys = [
        (epsilon_id, component_id)
        for epsilon_id in REGULATOR_IDS
        for component_id in MATERIAL_COMPONENT_IDS
    ]
    pools: list[list[dict[str, Any]]] = []
    for key in keys:
        local = [
            row
            for row in fits
            if (row["epsilon_id"], row["component_id"]) == key
        ]
        highest = max(int(row["refinement"]) for row in local)
        pools.append(
            [
                row
                for row in local
                if int(row["refinement"]) in (highest - 1, highest)
                and int(row["degree"]) in FIT_DEGREES
            ]
        )
    rows: list[dict[str, Any]] = []
    for index, combination in enumerate(itertools.product(*pools), start=1):
        shift = 0.0j
        details: list[str] = []
        for key, candidate in zip(keys, combination):
            candidate_value = complex(
                candidate["fitted_residue_real"],
                candidate["fitted_residue_imaginary"],
            )
            selected_value = selected_poles[key]["residue"]
            shift += sensitivities[key] * (
                candidate_value - selected_value
            )
            details.append(
                f"{key[0]}:{key[1]}:"
                f"r{candidate['refinement']}:d{candidate['degree']}"
            )
        value = baseline + shift
        rows.append(
            {
                "ensemble_id": f"PE{index:04d}",
                "candidate_signature": "|".join(details),
                "value_real": value.real,
                "value_imaginary": value.imag,
                "value_magnitude": abs(value),
                "shift_real": shift.real,
                "shift_imaginary": shift.imag,
                "absolute_shift": abs(shift),
                "relative_shift": abs(shift) / max(abs(baseline), 1.0e-300),
                "valid_for_pole_residue_uncertainty_envelope": True,
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
        SCRIPT_5280,
        SCRIPT_5283,
        NODES_5281,
        POLE_FITS_5282,
        RESULT_5282,
        RESULT_5283,
        VALIDATION_5283,
        TOTALS_5283,
        PANELS_5280,
        TOTALS_5281,
    )
    parent = read_json(RESULT_5283)
    checks = {
        "required_sources_exist": all(path.exists() for path in required),
        "parent_5283_accepted": bool(parent["acceptance_passed"]),
        "parent_5283_validated": all(
            parse_bool(row["passed"]) for row in read_csv(VALIDATION_5283)
        ),
        "parent_fixed_angle_rule_converged": bool(
            parent["fixed_angle_energy_converged"]
        ),
        "four_material_source_rows": len(material_source_rows()) == 4,
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
        "decision": (
            "DRY_RUN_ACCEPTED__REFINE_POLE_RESIDUES_AND_PROPAGATE_ENVELOPE"
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
        raise RuntimeError("5284 dry run did not pass")
    parent = read_json(RESULT_5283)
    context = M5280.source_context()
    samples, fits = evaluate_samples_and_fits(context)
    selected = select_residues(fits)
    source_nodes = read_csv(NODES_5281)
    parent_totals = read_csv(TOTALS_5281)
    constants = M5283.integration_constants(
        read_csv(PANELS_5280),
        parent_totals,
    )
    selected_poles = selected_pole_dictionary(selected)
    _, components, totals, panels = M5283.assemble(
        source_nodes,
        selected_poles,
        constants,
        retain_nodes=False,
    )
    convergence = M5283.convergence_rows(totals)
    ensembles = ensemble_rows(
        fits,
        selected,
        source_nodes,
        constants,
        totals,
    )
    changes = {
        (int(row["lower_order"]), int(row["upper_order"])): float(
            row["relative_change"]
        )
        for row in convergence
        if row["channel"] == "subtracted_eight_integral"
    }
    middle_change = changes[(4, 8)]
    high_change = changes[(8, 16)]
    fixed_angle_converged = (
        middle_change <= MID_ORDER_RELATIVE_CHANGE_LIMIT
        and high_change <= HIGH_ORDER_RELATIVE_CHANGE_LIMIT
    )
    maximum_ensemble_shift = max(
        float(row["relative_shift"]) for row in ensembles
    )
    maximum_refinement_change = max(
        float(row["refinement_relative_change"]) for row in selected
    )
    maximum_degree_change = max(
        float(row["degree_relative_change"]) for row in selected
    )
    maximum_fit_residual = max(
        float(row["fit_relative_residual"]) for row in selected
    )
    maximum_coefficient_change = max(
        float(row["maximum_coefficient_relative_change"])
        for row in selected
    )
    all_fit_controls_pass = all(
        parse_bool(row["fit_controls_pass"]) for row in selected
    )
    residue_certificate_passed = (
        all_fit_controls_pass
        and maximum_ensemble_shift
        <= PHYSICAL_ENSEMBLE_RELATIVE_SPREAD_LIMIT
        and fixed_angle_converged
    )
    refined_order16 = M5283.complex_from_row(
        physical_row(totals, 16),
        "subtracted_eight_integral",
    )
    parent_order16 = M5283.complex_from_row(
        physical_row(read_csv(TOTALS_5283), 16),
        "subtracted_eight_integral",
    )
    parent_shift = relative_complex_difference(
        refined_order16,
        parent_order16,
    )
    cancellation_condition = sum(
        float(row["physical_integral_magnitude"])
        for row in components
        if int(row["quadrature_order"]) == 16
    ) / max(abs(refined_order16), 1.0e-300)
    checks = {
        "all_refinement_samples_mask_active": all(
            parse_bool(row["mask_active"]) for row in samples
        ),
        "all_audited_coefficients_converged": (
            maximum_coefficient_change <= COEFFICIENT_CONVERGENCE_LIMIT
        ),
        "four_selected_material_residues": (
            len(selected) == 4
            and {
                (row["epsilon_id"], row["component_id"])
                for row in selected
            }
            == {
                (epsilon_id, component_id)
                for epsilon_id in REGULATOR_IDS
                for component_id in MATERIAL_COMPONENT_IDS
            }
        ),
        "ensemble_propagation_complete": len(ensembles) == 1296,
        "refined_totals_finite": all(
            math.isfinite(float(value))
            for row in totals
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
    physical_totals = {
        str(row["quadrature_order"]): {
            "subtracted_eight_real": row[
                "subtracted_eight_integral_real"
            ],
            "subtracted_eight_imaginary": row[
                "subtracted_eight_integral_imaginary"
            ],
        }
        for row in totals
        if row["row_type"] == "PHYSICAL_ENERGY_EXTRAPOLATION"
    }
    formal_end = M5283.formal_inventory_digest()
    result = {
        "checkpoint": CHECKPOINT,
        "parent_checkpoint": PARENT_CHECKPOINT,
        "marker": MARKER,
        "revision": REVISION,
        "mode": "pole-residue-refinement-cancellation-certificate",
        "checks": checks,
        "acceptance_passed": accepted,
        "sample_count": len(samples),
        "fit_candidate_count": len(fits),
        "selected_residue_count": len(selected),
        "ensemble_count": len(ensembles),
        "maximum_selected_fit_relative_residual": maximum_fit_residual,
        "maximum_refinement_relative_change": maximum_refinement_change,
        "maximum_degree_relative_change": maximum_degree_change,
        "maximum_coefficient_relative_change": maximum_coefficient_change,
        "maximum_order16_ensemble_relative_shift": maximum_ensemble_shift,
        "parent_to_refined_order16_relative_shift": parent_shift,
        "order16_cancellation_condition_number": cancellation_condition,
        "order4_to_order8_relative_change": middle_change,
        "order8_to_order16_relative_change": high_change,
        "fixed_angle_energy_converged": fixed_angle_converged,
        "pole_residue_certificate_passed": residue_certificate_passed,
        "physical_order_totals": physical_totals,
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
                "CERTIFY_REFINED_MC04_MC12_RESIDUES_AND_FIXED_ANGLE_RULE__"
                "BUILD_CHAMBER_ADAPTED_ANGULAR_RUNNER"
            )
            if accepted and residue_certificate_passed
            else (
                "REFINEMENT_COMPLETED_BUT_RESIDUE_CERTIFICATE_OPEN__"
                "DERIVE_CHANNEL_DERIVATIVE_RESIDUES"
                if accepted
                else "POLE_RESIDUE_REFINEMENT_REQUIRES_REPAIR"
            )
        ),
        "claim_boundary": {
            "valid_for_refined_fixed_angle_pole_residues": (
                accepted and residue_certificate_passed
            ),
            "valid_for_converged_fixed_angle_energy_integral": (
                accepted and residue_certificate_passed
            ),
            "valid_for_chamber_adapted_angular_runner": (
                accepted and residue_certificate_passed
            ),
            "valid_for_full_phase_space_coefficient": False,
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
            "reason": (
                "The certificate requires fit-window, polynomial-degree, "
                "physical uncertainty-envelope, and energy-order controls. "
                "It does not itself perform angular integration."
            ),
        },
    }
    write_csv(SAMPLE_ROWS, samples)
    write_csv(FIT_ROWS, fits)
    write_csv(SELECTED_ROWS, selected)
    write_csv(ENSEMBLE_ROWS, ensembles)
    write_csv(ENERGY_TOTALS, totals)
    write_csv(CONVERGENCE_ROWS, convergence)
    atomic_json(RESULT, result)
    atomic_json(
        STATUS,
        {
            "checkpoint": CHECKPOINT,
            "state": "COMPLETED",
            "mode": result["mode"],
            "acceptance_passed": accepted,
            "pole_residue_certificate_passed": residue_certificate_passed,
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
    totals = "\n".join(
        (
            f"- order {order}: "
            f"`{values['subtracted_eight_real']:.12g}"
            f"{values['subtracted_eight_imaginary']:+.12g}i`"
        )
        for order, values in result["physical_order_totals"].items()
    )
    text = f"""# 5284 — Pole-residue refinement and cancellation certificate

## Purpose

The 5283 energy sequence converged only after subtracting MC04 and MC12,
but the physical answer is a cancellation of much larger component
terms. This checkpoint therefore replaces a single direct Laurent fit
with a radius-refined numerator fit,

`N(E) = (E - E_p) F(E)`,

evaluates the fitted polynomial at the complex pole, and propagates the
last two radii and degrees 2–4 through the order-16 physical integral.

## Result

{totals}

- maximum selected fit residual:
  `{result['maximum_selected_fit_relative_residual']:.12g}`;
- maximum radius-refinement change:
  `{result['maximum_refinement_relative_change']:.12g}`;
- maximum polynomial-degree change:
  `{result['maximum_degree_relative_change']:.12g}`;
- order-16 cancellation condition number:
  `{result['order16_cancellation_condition_number']:.12g}`;
- maximum 1,296-member residue-ensemble shift:
  `{result['maximum_order16_ensemble_relative_shift']:.12g}`;
- parent-to-refined order-16 shift:
  `{result['parent_to_refined_order16_relative_shift']:.12g}`;
- order 8 to 16 quadrature change:
  `{result['order8_to_order16_relative_change']:.12g}`;
- residue certificate:
  `{result['pole_residue_certificate_passed']}`.

Decision:
`{result['decision']}`.

Validation: **{'PASS' if validation_passed else 'FAIL'}**.

## Claim boundary

Passing this checkpoint authorizes construction of the chamber-adapted
angular runner only. It is not a full phase-space coefficient, UV,
local-GR, or full-MTS claim.
"""
    DOCUMENT.write_text(text, encoding="utf-8")


def validate_outputs() -> dict[str, Any]:
    result = read_json(RESULT)
    required_csvs = (
        SAMPLE_ROWS,
        FIT_ROWS,
        SELECTED_ROWS,
        ENSEMBLE_ROWS,
        ENERGY_TOTALS,
        CONVERGENCE_ROWS,
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
            "PARENT_5283_ACCEPTED",
            bool(read_json(RESULT_5283)["acceptance_passed"]),
            str(read_json(RESULT_5283)["decision"]),
        ),
        validation_gate(
            "REFINEMENT_PIPELINE_ACCEPTED",
            bool(result["acceptance_passed"]),
            str(result["decision"]),
        ),
        validation_gate(
            "REQUIRED_CSVS_PARSE",
            len(csv_rows) == len(required_csvs) and all(csv_rows.values()),
            f"{len(csv_rows)}/{len(required_csvs)} non-empty CSVs",
        ),
        validation_gate(
            "FOUR_SELECTED_RESIDUES",
            result["selected_residue_count"] == 4,
            str(result["selected_residue_count"]),
        ),
        validation_gate(
            "ENSEMBLE_COMPLETE",
            result["ensemble_count"] == 1296,
            str(result["ensemble_count"]),
        ),
        validation_gate(
            "CERTIFICATE_DECISION_CONSISTENT",
            (
                bool(result["pole_residue_certificate_passed"])
                == bool(
                    result["claim_boundary"][
                        "valid_for_refined_fixed_angle_pole_residues"
                    ]
                )
            ),
            (
                "certificate="
                f"{result['pole_residue_certificate_passed']}"
            ),
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
            "VALIDATED_POLE_RESIDUE_REFINEMENT_CERTIFICATE"
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
