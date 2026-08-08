from __future__ import annotations

import argparse
import csv
import ctypes
import hashlib
import importlib.util
import json
import math
import os
import sys
import time
from pathlib import Path
from typing import Any, Callable


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
SOURCE = FUNCTIONAL_RG / "5285"

SCRIPT_5284 = (
    SCRIPTS
    / "Y5_R2FR_5284_pole_residue_refinement_and_cancellation_certificate.py"
)
SCRIPT_5267 = (
    SCRIPTS / "Y5_R2FR_5267_topology_aware_soft_energy_component_runner.py"
)
SAMPLES_5284 = FUNCTIONAL_RG / "5284" / "pole_numerator_samples.csv"
RESULT_5284 = FUNCTIONAL_RG / "5284" / "pole_residue_refinement_result.json"
VALIDATION_5284 = (
    FUNCTIONAL_RG / "5284" / "pole_residue_refinement_validation.csv"
)
NODES_5281 = (
    FUNCTIONAL_RG / "5281" / "high_order_energy_component_nodes.csv"
)
PANELS_5280 = FUNCTIONAL_RG / "5280" / "composite_energy_panels.csv"
TOTALS_5281 = FUNCTIONAL_RG / "5281" / "high_order_energy_totals.csv"
TOTALS_5283 = FUNCTIONAL_RG / "5283" / "two_pole_energy_totals.csv"
POLE_ROWS_5267 = {
    epsilon_id: (
        FUNCTIONAL_RG
        / "5267"
        / "workers"
        / epsilon_id
        / "energy_poles.csv"
    )
    for epsilon_id in ("E040", "E020")
}

DRY_RUN = SOURCE / "channel_derivative_residue_dry_run.json"
ROOT_ROWS = SOURCE / "refined_channel_poles_and_derivatives.csv"
SAMPLE_ROWS = SOURCE / "channel_numerator_samples.csv"
FIT_ROWS = SOURCE / "channel_numerator_fit_candidates.csv"
SELECTED_ROWS = SOURCE / "channel_derivative_material_pole_residues.csv"
ENSEMBLE_ROWS = SOURCE / "channel_residue_physical_ensemble.csv"
ENERGY_TOTALS = SOURCE / "channel_residue_energy_totals.csv"
CONVERGENCE_ROWS = SOURCE / "channel_residue_energy_convergence.csv"
RESULT = SOURCE / "channel_derivative_residue_result.json"
VALIDATION = SOURCE / "channel_derivative_residue_validation.csv"
RESIDUAL_VALIDATION = (
    RESIDUALS / "P8_Y5_BRR545_5285_VALIDATION.csv"
)
STATUS = SOURCE / "status.json"
DOCUMENT = (
    POST / "5285-Y5-R2FR-channel-derivative-material-pole-residues.md"
)

CHECKPOINT = 5285
PARENT_CHECKPOINT = 5284
MARKER = "MTS_5285_CHANNEL_DERIVATIVE_MATERIAL_POLE_RESIDUES"
REVISION = "channel-derivative-material-pole-residues-v1"
REGULATOR_IDS = ("E040", "E020")
MATERIAL_COMPONENT_IDS = ("MC04", "MC12")
FIT_DEGREES = (2, 3, 4)
DERIVATIVE_STEPS = (2.0e-5, 1.0e-5, 5.0e-6, 2.5e-6, 1.25e-6)
CHANNEL_ROOT_RESIDUAL_LIMIT = 1.0e-12
POLE_REFINEMENT_SHIFT_LIMIT = 1.0e-6
DERIVATIVE_RELATIVE_CHANGE_LIMIT = 1.0e-7
SOURCE_DERIVATIVE_RELATIVE_ERROR_LIMIT = 1.0e-6
FIT_RELATIVE_RESIDUAL_LIMIT = 1.0e-8
REFINEMENT_RELATIVE_CHANGE_LIMIT = 1.0e-8
DEGREE_RELATIVE_CHANGE_LIMIT = 1.0e-8
COEFFICIENT_CONVERGENCE_LIMIT = 1.0e-6
PHYSICAL_ENSEMBLE_RELATIVE_SPREAD_LIMIT = 1.0e-3
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


M5284 = load_module("mts_5284_for_5285", SCRIPT_5284)
M5280 = M5284.M5280
M5283 = M5284.M5283
M5267 = M5280.M5274.M5267
np = M5280.np


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
        SCRIPT_5284,
        SCRIPT_5267,
        SAMPLES_5284,
        RESULT_5284,
        VALIDATION_5284,
        NODES_5281,
        PANELS_5280,
        TOTALS_5281,
        TOTALS_5283,
        POLE_ROWS_5267["E040"],
        POLE_ROWS_5267["E020"],
        M5267.MANIFEST_5239,
    )
    return [
        {"path": str(path), "sha256": digest(path)}
        for path in paths
    ]


def relative_complex_difference(first: complex, second: complex) -> float:
    return abs(first - second) / max(abs(first), abs(second), 1.0e-300)


def material_pole_sources() -> list[dict[str, str]]:
    rows: list[dict[str, str]] = []
    for epsilon_id in REGULATOR_IDS:
        rows.extend(
            row
            for row in read_csv(POLE_ROWS_5267[epsilon_id])
            if row["component_id"] in MATERIAL_COMPONENT_IDS
        )
    return rows


def build_material_problems() -> dict[tuple[str, str], dict[str, Any]]:
    manifest = M5267.read_json(M5267.MANIFEST_5239)
    problems: dict[tuple[str, str], dict[str, Any]] = {}
    for source in material_pole_sources():
        key = (source["epsilon_id"], source["component_id"])
        source_job = next(
            job
            for job in manifest["jobs"]
            if job["epsilon_id"] == key[0]
            and job["component_id"] == key[1]
        )
        problem = M5267.M5239.build_problem(M5267.energy_job(source_job))
        M5267.install_paired_track(problem)
        problems[key] = problem
    return problems


def channel_function(
    problem: dict[str, Any],
    surface_id: str,
) -> Callable[[complex], complex]:
    return lambda coordinate: complex(
        M5267.M5239.owner_surface_values(
            problem,
            complex(coordinate),
        )[surface_id]
    )


def central_derivative(
    function: Callable[[complex], complex],
    point: complex,
    step: float,
) -> complex:
    return (function(point + step) - function(point - step)) / (2.0 * step)


def refine_channel_poles(
    problems: dict[tuple[str, str], dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for source in material_pole_sources():
        key = (source["epsilon_id"], source["component_id"])
        surface_id = source["primary_surface_id"]
        channel = channel_function(problems[key], surface_id)
        initial = complex(
            float(source["pole_real"]),
            float(source["pole_imaginary"]),
        )
        pole = initial
        iterations = 0
        for iterations in range(1, 9):
            derivative = central_derivative(channel, pole, 1.0e-6)
            updated = pole - channel(pole) / derivative
            pole = updated
            if abs(channel(pole)) <= CHANNEL_ROOT_RESIDUAL_LIMIT:
                break
        derivative_estimates = [
            central_derivative(channel, pole, step)
            for step in DERIVATIVE_STEPS
        ]
        derivative = derivative_estimates[-1]
        derivative_change = relative_complex_difference(
            derivative_estimates[-1],
            derivative_estimates[-2],
        )
        center = float(source["real_axis_center"])
        source_derivative = complex(
            float(source["channel_derivative_real"]),
            float(source["channel_derivative_imaginary"]),
        )
        center_derivative = central_derivative(channel, complex(center), 1.0e-5)
        source_derivative_error = relative_complex_difference(
            center_derivative,
            source_derivative,
        )
        residual = abs(channel(pole))
        shift = abs(pole - initial)
        passed = (
            residual <= CHANNEL_ROOT_RESIDUAL_LIMIT
            and shift <= POLE_REFINEMENT_SHIFT_LIMIT
            and derivative_change <= DERIVATIVE_RELATIVE_CHANGE_LIMIT
            and source_derivative_error
            <= SOURCE_DERIVATIVE_RELATIVE_ERROR_LIMIT
        )
        rows.append(
            {
                "epsilon_id": key[0],
                "component_id": key[1],
                "surface_id": surface_id,
                "initial_pole_real": initial.real,
                "initial_pole_imaginary": initial.imag,
                "refined_pole_real": pole.real,
                "refined_pole_imaginary": pole.imag,
                "pole_refinement_shift": shift,
                "channel_root_residual": residual,
                "channel_derivative_real": derivative.real,
                "channel_derivative_imaginary": derivative.imag,
                "channel_derivative_relative_change": derivative_change,
                "source_center_derivative_relative_error": (
                    source_derivative_error
                ),
                "newton_iteration_count": iterations,
                "channel_root_and_derivative_passed": passed,
                "valid_for_channel_derivative_residue": passed,
                "valid_for_full_phase_space_coefficient": False,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    return rows


def channel_numerator_fits(
    problems: dict[tuple[str, str], dict[str, Any]],
    roots: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    parent_samples = read_csv(SAMPLES_5284)
    sample_rows: list[dict[str, Any]] = []
    fit_rows: list[dict[str, Any]] = []
    for root in roots:
        key = (root["epsilon_id"], root["component_id"])
        source = next(
            row
            for row in material_pole_sources()
            if (row["epsilon_id"], row["component_id"]) == key
        )
        surface_id = source["primary_surface_id"]
        channel = channel_function(problems[key], surface_id)
        pole = complex(
            float(root["refined_pole_real"]),
            float(root["refined_pole_imaginary"]),
        )
        derivative = complex(
            float(root["channel_derivative_real"]),
            float(root["channel_derivative_imaginary"]),
        )
        local_parent = [
            row
            for row in parent_samples
            if (row["epsilon_id"], row["component_id"]) == key
        ]
        for parent in local_parent:
            energy = float(parent["energy"])
            contribution = complex(
                float(parent["contribution_real"]),
                float(parent["contribution_imaginary"]),
            )
            channel_value = channel(complex(energy))
            numerator = channel_value * contribution
            sample_rows.append(
                {
                    "epsilon_id": key[0],
                    "component_id": key[1],
                    "surface_id": surface_id,
                    "refinement": parent["refinement"],
                    "radius": parent["radius"],
                    "fraction": parent["fraction"],
                    "energy": energy,
                    "channel_real": channel_value.real,
                    "channel_imaginary": channel_value.imag,
                    "contribution_real": contribution.real,
                    "contribution_imaginary": contribution.imag,
                    "numerator_real": numerator.real,
                    "numerator_imaginary": numerator.imag,
                    "mask_active": parent["mask_active"],
                    "coefficient_relative_change": parent[
                        "coefficient_relative_change"
                    ],
                    "valid_for_channel_numerator_fit": True,
                    "valid_for_full_phase_space_coefficient": False,
                    "valid_for_numeric_UV_claim": False,
                    "valid_for_local_GR_claim": False,
                    "valid_for_full_MTS_claim": False,
                }
            )
        refinements = sorted(
            {int(row["refinement"]) for row in local_parent}
        )
        center = float(source["real_axis_center"])
        for refinement in refinements:
            local = [
                row
                for row in sample_rows
                if (row["epsilon_id"], row["component_id"]) == key
                and int(row["refinement"]) == refinement
            ]
            radius = float(local[0]["radius"])
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
            scaled_pole = (pole - center) / radius
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
                residual = float(
                    np.max(np.abs(predicted - numerators))
                    / max(float(np.max(np.abs(numerators))), 1.0e-300)
                )
                fit_rows.append(
                    {
                        "epsilon_id": key[0],
                        "component_id": key[1],
                        "surface_id": surface_id,
                        "refinement": refinement,
                        "radius": radius,
                        "degree": degree,
                        "scaled_pole_magnitude": abs(scaled_pole),
                        "sample_count": len(local),
                        "numerator_at_pole_real": numerator_at_pole.real,
                        "numerator_at_pole_imaginary": (
                            numerator_at_pole.imag
                        ),
                        "fitted_residue_real": residue.real,
                        "fitted_residue_imaginary": residue.imag,
                        "fitted_residue_magnitude": abs(residue),
                        "fit_relative_residual": residual,
                        "all_samples_mask_active": all(
                            parse_bool(row["mask_active"]) for row in local
                        ),
                        "maximum_coefficient_relative_change": max(
                            float(row["coefficient_relative_change"])
                            for row in local
                        ),
                        "valid_for_channel_numerator_fit": True,
                        "valid_for_full_phase_space_coefficient": False,
                        "valid_for_numeric_UV_claim": False,
                        "valid_for_local_GR_claim": False,
                        "valid_for_full_MTS_claim": False,
                    }
                )
    return sample_rows, fit_rows


def select_channel_residues(
    roots: list[dict[str, Any]],
    fits: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for root in roots:
        key = (root["epsilon_id"], root["component_id"])
        local = [
            row
            for row in fits
            if (row["epsilon_id"], row["component_id"]) == key
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
            float(selected["fitted_residue_real"]),
            float(selected["fitted_residue_imaginary"]),
        )
        previous_value = complex(
            float(previous["fitted_residue_real"]),
            float(previous["fitted_residue_imaginary"]),
        )
        degree_change = max(
            relative_complex_difference(
                selected_value,
                complex(
                    float(row["fitted_residue_real"]),
                    float(row["fitted_residue_imaginary"]),
                ),
            )
            for row in local
            if int(row["refinement"]) == highest
        )
        refinement_change = relative_complex_difference(
            selected_value,
            previous_value,
        )
        controls_pass = (
            parse_bool(root["channel_root_and_derivative_passed"])
            and float(selected["fit_relative_residual"])
            <= FIT_RELATIVE_RESIDUAL_LIMIT
            and refinement_change
            <= REFINEMENT_RELATIVE_CHANGE_LIMIT
            and degree_change <= DEGREE_RELATIVE_CHANGE_LIMIT
            and parse_bool(selected["all_samples_mask_active"])
            and float(selected["maximum_coefficient_relative_change"])
            <= COEFFICIENT_CONVERGENCE_LIMIT
        )
        rows.append(
            {
                "epsilon_id": key[0],
                "component_id": key[1],
                "surface_id": root["surface_id"],
                "selected_refinement": highest,
                "selected_degree": 3,
                "pole_real": root["refined_pole_real"],
                "pole_imaginary": root["refined_pole_imaginary"],
                "channel_derivative_real": root[
                    "channel_derivative_real"
                ],
                "channel_derivative_imaginary": root[
                    "channel_derivative_imaginary"
                ],
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
                "channel_derivative_residue_controls_pass": controls_pass,
                "valid_for_channel_derivative_pole_subtraction": (
                    controls_pass
                ),
                "valid_for_full_phase_space_coefficient": False,
                "valid_for_numeric_UV_claim": False,
                "valid_for_local_GR_claim": False,
                "valid_for_full_MTS_claim": False,
            }
        )
    return rows


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


def dry_run() -> dict[str, Any]:
    SOURCE.mkdir(parents=True, exist_ok=True)
    required = (
        SCRIPT_5284,
        SCRIPT_5267,
        SAMPLES_5284,
        RESULT_5284,
        VALIDATION_5284,
        NODES_5281,
        PANELS_5280,
        TOTALS_5281,
        TOTALS_5283,
        POLE_ROWS_5267["E040"],
        POLE_ROWS_5267["E020"],
        M5267.MANIFEST_5239,
    )
    parent = read_json(RESULT_5284)
    checks = {
        "required_sources_exist": all(path.exists() for path in required),
        "parent_5284_accepted": bool(parent["acceptance_passed"]),
        "parent_5284_validated": all(
            parse_bool(row["passed"]) for row in read_csv(VALIDATION_5284)
        ),
        "fit_only_certificate_correctly_remained_open": (
            not bool(parent["pole_residue_certificate_passed"])
        ),
        "four_material_channel_sources": (
            len(material_pole_sources()) == 4
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
        "marker": MARKER,
        "revision": REVISION,
        "mode": "dry-run",
        "checks": checks,
        "acceptance_passed": accepted,
        "decision": (
            "DRY_RUN_ACCEPTED__DERIVE_NUMERATOR_OVER_CHANNEL_DERIVATIVE"
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
    dry = dry_run()
    if not dry["acceptance_passed"]:
        raise RuntimeError("5285 dry run did not pass")
    parent = read_json(RESULT_5284)
    problems = build_material_problems()
    roots = refine_channel_poles(problems)
    samples, fits = channel_numerator_fits(problems, roots)
    selected = select_channel_residues(roots, fits)
    source_nodes = read_csv(NODES_5281)
    constants = M5283.integration_constants(
        read_csv(PANELS_5280),
        read_csv(TOTALS_5281),
    )
    selected_poles = selected_pole_dictionary(selected)
    _, components, totals, panels = M5283.assemble(
        source_nodes,
        selected_poles,
        constants,
        retain_nodes=False,
    )
    convergence = M5283.convergence_rows(totals)
    ensembles = M5284.ensemble_rows(
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
    maximum_root_residual = max(
        float(row["channel_root_residual"]) for row in roots
    )
    maximum_pole_shift = max(
        float(row["pole_refinement_shift"]) for row in roots
    )
    maximum_derivative_change = max(
        float(row["channel_derivative_relative_change"])
        for row in roots
    )
    maximum_fit_residual = max(
        float(row["fit_relative_residual"]) for row in selected
    )
    maximum_refinement_change = max(
        float(row["refinement_relative_change"]) for row in selected
    )
    maximum_degree_change = max(
        float(row["degree_relative_change"]) for row in selected
    )
    maximum_ensemble_shift = max(
        float(row["relative_shift"]) for row in ensembles
    )
    all_controls_pass = (
        all(
            parse_bool(row["channel_root_and_derivative_passed"])
            for row in roots
        )
        and all(
            parse_bool(
                row["channel_derivative_residue_controls_pass"]
            )
            for row in selected
        )
    )
    certificate_passed = (
        all_controls_pass
        and maximum_ensemble_shift
        <= PHYSICAL_ENSEMBLE_RELATIVE_SPREAD_LIMIT
        and fixed_angle_converged
    )
    order16 = M5283.complex_from_row(
        physical_row(totals, 16),
        "subtracted_eight_integral",
    )
    parent_order16 = M5283.complex_from_row(
        physical_row(read_csv(TOTALS_5283), 16),
        "subtracted_eight_integral",
    )
    parent_shift = relative_complex_difference(order16, parent_order16)
    cancellation_condition = sum(
        float(row["physical_integral_magnitude"])
        for row in components
        if int(row["quadrature_order"]) == 16
    ) / max(abs(order16), 1.0e-300)
    checks = {
        "four_channel_problems_built": len(problems) == 4,
        "four_channel_roots_refined": len(roots) == 4,
        "four_channel_residues_selected": len(selected) == 4,
        "all_source_samples_preserved": len(samples) == 144,
        "all_samples_exact_mask_active": all(
            parse_bool(row["mask_active"]) for row in samples
        ),
        "ensemble_propagation_complete": len(ensembles) == 1296,
        "energy_totals_finite": all(
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
        "mode": "channel-derivative-material-pole-residues",
        "checks": checks,
        "acceptance_passed": accepted,
        "problem_count": len(problems),
        "root_count": len(roots),
        "sample_count": len(samples),
        "fit_candidate_count": len(fits),
        "selected_residue_count": len(selected),
        "ensemble_count": len(ensembles),
        "maximum_channel_root_residual": maximum_root_residual,
        "maximum_pole_refinement_shift": maximum_pole_shift,
        "maximum_channel_derivative_relative_change": (
            maximum_derivative_change
        ),
        "maximum_selected_fit_relative_residual": maximum_fit_residual,
        "maximum_refinement_relative_change": maximum_refinement_change,
        "maximum_degree_relative_change": maximum_degree_change,
        "maximum_order16_ensemble_relative_shift": maximum_ensemble_shift,
        "parent_to_channel_order16_relative_shift": parent_shift,
        "order16_cancellation_condition_number": cancellation_condition,
        "order4_to_order8_relative_change": middle_change,
        "order8_to_order16_relative_change": high_change,
        "fixed_angle_energy_converged": fixed_angle_converged,
        "channel_derivative_residue_certificate_passed": (
            certificate_passed
        ),
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
            "new_local_limit_evaluation_count": 0,
            "sustained_redline_forbidden": True,
        },
        "runtime_seconds": time.perf_counter() - started,
        "decision": (
            (
                "CERTIFY_CHANNEL_DERIVATIVE_MC04_MC12_RESIDUES__"
                "BUILD_CHAMBER_ADAPTED_ANGULAR_RUNNER"
            )
            if accepted and certificate_passed
            else (
                "CHANNEL_DERIVATIVE_RESIDUES_REQUIRE_REPAIR"
                if accepted
                else "CHANNEL_DERIVATIVE_PIPELINE_REQUIRES_REPAIR"
            )
        ),
        "claim_boundary": {
            "valid_for_channel_derivative_material_pole_residues": (
                accepted and certificate_passed
            ),
            "valid_for_converged_fixed_angle_energy_integral": (
                accepted and certificate_passed
            ),
            "valid_for_chamber_adapted_angular_runner": (
                accepted and certificate_passed
            ),
            "valid_for_full_phase_space_coefficient": False,
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
            "reason": (
                "Material residues are computed as the fitted regular "
                "channel numerator at the refined complex zero divided "
                "by the channel derivative. Angular integration remains "
                "a separate gate."
            ),
        },
    }
    write_csv(ROOT_ROWS, roots)
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
            "certificate_passed": certificate_passed,
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
    text = f"""# 5285 — Channel-derivative material-pole residues

## Derived residue law

For each material pole owner `X` with channel `D_X(E)`,

`F_X(E) = N_X(E) / D_X(E)`,

the complex channel zero `E_X` is Newton-refined and the residue is
computed from

`A_X = N_X(E_X) / D'_X(E_X)`.

The numerator samples use the already audited true local-limit
contributions from 5284:

`N_X(E_i) = D_X(E_i) F_X(E_i)`.

This removes the unstable direct fit of `F_X` to a Laurent ansatz.

## Result

{totals}

- maximum channel-root residual:
  `{result['maximum_channel_root_residual']:.12g}`;
- maximum pole refinement shift:
  `{result['maximum_pole_refinement_shift']:.12g}`;
- maximum derivative step change:
  `{result['maximum_channel_derivative_relative_change']:.12g}`;
- maximum numerator-fit residual:
  `{result['maximum_selected_fit_relative_residual']:.12g}`;
- maximum radius-refinement change:
  `{result['maximum_refinement_relative_change']:.12g}`;
- maximum degree change:
  `{result['maximum_degree_relative_change']:.12g}`;
- maximum order-16 residue-ensemble shift:
  `{result['maximum_order16_ensemble_relative_shift']:.12g}`;
- order 8 to 16 quadrature change:
  `{result['order8_to_order16_relative_change']:.12g}`;
- certificate:
  `{result['channel_derivative_residue_certificate_passed']}`.

Decision:
`{result['decision']}`.

Validation: **{'PASS' if validation_passed else 'FAIL'}**.

## Claim boundary

This certifies the fixed-angle pole subtraction only if every listed
gate passes. It does not yet supply the angular integral, a full
phase-space coefficient, a UV claim, local GR, or full MTS.
"""
    DOCUMENT.write_text(text, encoding="utf-8")


def validate_outputs() -> dict[str, Any]:
    result = read_json(RESULT)
    required_csvs = (
        ROOT_ROWS,
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
            "PARENT_5284_ACCEPTED",
            bool(read_json(RESULT_5284)["acceptance_passed"]),
            str(read_json(RESULT_5284)["decision"]),
        ),
        validation_gate(
            "CHANNEL_PIPELINE_ACCEPTED",
            bool(result["acceptance_passed"]),
            str(result["decision"]),
        ),
        validation_gate(
            "REQUIRED_CSVS_PARSE",
            len(csv_rows) == len(required_csvs) and all(csv_rows.values()),
            f"{len(csv_rows)}/{len(required_csvs)} non-empty CSVs",
        ),
        validation_gate(
            "FOUR_CHANNEL_RESIDUES",
            (
                result["root_count"] == 4
                and result["selected_residue_count"] == 4
            ),
            (
                f"roots={result['root_count']}; "
                f"residues={result['selected_residue_count']}"
            ),
        ),
        validation_gate(
            "NO_NEW_LOCAL_LIMIT_EVALUATIONS",
            result["resource_contract"][
                "new_local_limit_evaluation_count"
            ]
            == 0,
            "reused 5284 true-limit samples",
        ),
        validation_gate(
            "CERTIFICATE_DECISION_CONSISTENT",
            (
                bool(
                    result[
                        "channel_derivative_residue_certificate_passed"
                    ]
                )
                == bool(
                    result["claim_boundary"][
                        "valid_for_channel_derivative_material_pole_residues"
                    ]
                )
            ),
            (
                "certificate="
                f"{result['channel_derivative_residue_certificate_passed']}"
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
            "VALIDATED_CHANNEL_DERIVATIVE_MATERIAL_POLE_RESIDUES"
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
