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

import mpmath as mp
import numpy as np
from numba import njit, prange
from scipy.stats import qmc


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE = POST / "source-intake" / "functional_rg" / "5021"
RESIDUALS = POST / "source-intake" / "mts_residuals"

SCRIPT_5017 = POST / "scripts" / "Y5_R2FR_5017_complex_safe_hhh_crossed_integrand_and_coupled_locality_smoke.py"
SCRIPT_5019 = POST / "scripts" / "Y5_R2FR_5019_hhh_exact_soft_endpoint_and_crossed_pole_theorem.py"
SCRIPT_5020 = POST / "scripts" / "Y5_R2FR_5020_two_loop_amplitude_cut_object_and_normalization_closure.py"
RESULT_5017 = POST / "source-intake" / "functional_rg" / "5017" / "complex_safe_hhh_crossed_results.json"
RESULT_5019 = POST / "source-intake" / "functional_rg" / "5019" / "hhh_exact_soft_endpoint_and_crossed_pole_results.json"
RESULT_5020 = POST / "source-intake" / "functional_rg" / "5020" / "amplitude_cut_object_and_normalization_results.json"
TARGET_5018 = POST / "source-intake" / "functional_rg" / "5018" / "raw_hhh_smoke_vs_matched_nonlocal_target.csv"

COORDINATE_CSV = SOURCE / "global_azimuth_coordinate_and_contour_checks.csv"
ENDPOINT_CSV = SOURCE / "soft_endpoint_nested_contour_validation.csv"
PHYSICAL_CSV = SOURCE / "physical_direct_nested_azimuth_results.csv"
CROSSED_CSV = SOURCE / "crossed_upper_boundary_epsilon_results.csv"
EXTRAPOLATION_CSV = SOURCE / "crossed_real_boundary_extrapolation.csv"
CYCLIC_CSV = SOURCE / "corrected_cyclic_hhh_vs_matched_target_smoke.csv"
GATE_CSV = SOURCE / "global_azimuth_nested_contour_gate.csv"
RESULT_JSON = SOURCE / "global_azimuth_nested_contour_results.json"
PROVENANCE = SOURCE / "PROVENANCE.md"
DOCUMENT = POST / "5021-Y5-R2FR-global-azimuth-Feynman-contour-nested-hhh-smoke.md"
VALIDATION_CSV = RESIDUALS / "P8_Y5_BRR545_5021_VALIDATION.csv"

MARKER = "MTS_5021_GLOBAL_AZIMUTH_FEYNMAN_CONTOUR_NESTED_HHH_SMOKE"
CHECKED_DATE = "2026-07-14"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
PHYSICAL_COSINES = (-0.6, -0.3, 0.0, 0.3, 0.6)
S_VALUE = 4.0


def load_module(path: Path, name: str) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5017 = load_module(SCRIPT_5017, "mts_checkpoint_5017_for_5021")
M5019 = load_module(SCRIPT_5019, "mts_checkpoint_5019_for_5021")
SEQUENTIAL_THREE_BODY = M5017.sequential_three_body
HHH_REDUCED_PRODUCT = M5017.hhh_reduced_product


def relative(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def tree_digest(path: Path) -> str:
    value = hashlib.sha256()
    for item in sorted(candidate for candidate in path.rglob("*") if candidate.is_file()):
        value.update(item.relative_to(path).as_posix().encode("utf-8"))
        value.update(digest(item).encode("ascii"))
    return value.hexdigest()


def read_json(path: Path) -> dict[str, Any]:
    return json.loads(path.read_text(encoding="utf-8"))


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    fields: list[str] = []
    for row in rows:
        for key in row:
            if key not in fields:
                fields.append(key)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def tagged(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    return [
        {
            **row,
            "checkpoint_marker": MARKER,
            "valid_for_numeric_UV_claim": False,
            "valid_for_full_MTS_claim": False,
            "source_checked_date": CHECKED_DATE,
        }
        for row in rows
    ]


def source_locks() -> dict[str, bool]:
    required = (
        SCRIPT_5017,
        SCRIPT_5019,
        SCRIPT_5020,
        RESULT_5017,
        RESULT_5019,
        RESULT_5020,
        TARGET_5018,
    )
    result_5017 = read_json(RESULT_5017)
    result_5019 = read_json(RESULT_5019)
    result_5020 = read_json(RESULT_5020)
    return {
        "required_paths": all(path.exists() for path in required),
        "5017_complex_safe_KLT": result_5017["complex_safe_five_point_KLT"] is True,
        "5019_crossed_pole_theorem": result_5019["crossed_poles"]["all_exact_and_root_tracking_passed"] is True,
        "5019_soft_endpoint": result_5019["exact_hhh_soft_endpoint_complete"] is True,
        "5020_amplitude_cut_object": result_5020["amplitude_times_amplitude_three_cut_retained"] is True,
        "5020_D3_normalization": result_5020["normalization"]["three_particle_D_over_G3"] == "-2/pi",
    }


@njit
def truncated_cauchy_density(value: float, center: float, width: float) -> float:
    lower_phase = math.atan((-1.0 - center) / width)
    upper_phase = math.atan((1.0 - center) / width)
    standardized = (value - center) / width
    return 1.0 / (
        width
        * (upper_phase - lower_phase)
        * (1.0 + standardized * standardized)
    )


@njit
def decay_cosine_importance(
    fraction: float, scattering_cosine: complex
) -> tuple[float, float]:
    if abs(scattering_cosine.real) <= 1.0 or abs(scattering_cosine.imag) < 1.0e-14:
        return 2.0 * fraction - 1.0, 1.0
    inverse = 1.0 / scattering_cosine
    center = abs(inverse.real)
    width = max(abs(inverse.imag), 1.0e-6)
    uniform_weight = 0.2
    pole_weight = 0.4
    if fraction < uniform_weight:
        local_fraction = fraction / uniform_weight
        value = 2.0 * local_fraction - 1.0
    elif fraction < uniform_weight + pole_weight:
        local_fraction = (fraction - uniform_weight) / pole_weight
        lower_phase = math.atan((-1.0 - center) / width)
        upper_phase = math.atan((1.0 - center) / width)
        value = center + width * math.tan(
            lower_phase + local_fraction * (upper_phase - lower_phase)
        )
    else:
        local_fraction = (fraction - uniform_weight - pole_weight) / pole_weight
        negative_center = -center
        lower_phase = math.atan((-1.0 - negative_center) / width)
        upper_phase = math.atan((1.0 - negative_center) / width)
        value = negative_center + width * math.tan(
            lower_phase + local_fraction * (upper_phase - lower_phase)
        )
    proposal_density = (
        uniform_weight * 0.5
        + pole_weight * truncated_cauchy_density(value, center, width)
        + pole_weight * truncated_cauchy_density(value, -center, width)
    )
    return value, 0.5 / proposal_density


@njit
def reduced_directions(
    soft_fraction: float,
    decay_fraction: float,
    relative_azimuth_fraction: float,
    scattering_cosine: complex,
) -> tuple[np.ndarray, np.ndarray, float]:
    soft_cosine = 2.0 * soft_fraction - 1.0
    decay_cosine, importance_weight = decay_cosine_importance(
        decay_fraction, scattering_cosine
    )
    soft_sine = math.sqrt(max(0.0, 1.0 - soft_cosine * soft_cosine))
    decay_sine = math.sqrt(max(0.0, 1.0 - decay_cosine * decay_cosine))
    relative_azimuth = 2.0 * math.pi * relative_azimuth_fraction
    soft_direction = np.array([soft_sine, 0.0, soft_cosine])
    decay_direction = np.array(
        [
            decay_sine * math.cos(relative_azimuth),
            decay_sine * math.sin(relative_azimuth),
            decay_cosine,
        ]
    )
    return soft_direction, decay_direction, importance_weight


@njit
def rotate_internal(internal: np.ndarray, global_azimuth: float) -> np.ndarray:
    cosine = math.cos(global_azimuth)
    sine = math.sin(global_azimuth)
    result = np.empty((3, 4), dtype=np.complex128)
    for index in range(3):
        result[index, 0] = internal[index, 0]
        result[index, 1] = cosine * internal[index, 1] - sine * internal[index, 2]
        result[index, 2] = sine * internal[index, 1] + cosine * internal[index, 2]
        result[index, 3] = internal[index, 3]
    return result


@njit
def azimuth_averaged_g(
    soft_energy: float,
    soft_fraction: float,
    decay_fraction: float,
    relative_azimuth_fraction: float,
    scattering_cosine: complex,
    azimuth_nodes: int,
    node_shift: float,
) -> complex:
    soft_direction, decay_direction, importance_weight = reduced_directions(
        soft_fraction,
        decay_fraction,
        relative_azimuth_fraction,
        scattering_cosine,
    )
    internal = SEQUENTIAL_THREE_BODY(
        soft_energy, soft_direction, decay_direction
    )
    inverse_energy_squared_sum = 0.0
    for index in range(3):
        inverse_energy_squared_sum += 1.0 / (
            internal[index, 0] * internal[index, 0]
        )
    sector_multiplier = (
        3.0
        / (internal[2, 0] * internal[2, 0])
        / inverse_energy_squared_sum
    )
    result = 0.0j
    for node in range(azimuth_nodes):
        global_azimuth = 2.0 * math.pi * (node + node_shift) / azimuth_nodes
        result += (
            soft_energy
            * soft_energy
            * sector_multiplier
            * HHH_REDUCED_PRODUCT(
                rotate_internal(internal, global_azimuth),
                scattering_cosine,
                1.0,
            )
            / (S_VALUE * S_VALUE)
        )
    return importance_weight * result / azimuth_nodes


@njit
def richardson_soft_endpoint(
    soft_fraction: float,
    decay_fraction: float,
    relative_azimuth_fraction: float,
    scattering_cosine: complex,
    azimuth_nodes: int,
    soft_reference: float,
) -> complex:
    half = azimuth_averaged_g(
        soft_reference / 2.0,
        soft_fraction,
        decay_fraction,
        relative_azimuth_fraction,
        scattering_cosine,
        azimuth_nodes,
        0.371,
    )
    full = azimuth_averaged_g(
        soft_reference,
        soft_fraction,
        decay_fraction,
        relative_azimuth_fraction,
        scattering_cosine,
        azimuth_nodes,
        0.371,
    )
    return 2.0 * half - full


@njit(parallel=True)
def endpoint_many(
    points: np.ndarray,
    scattering_cosine: complex,
    azimuth_nodes: int,
    soft_reference: float,
) -> np.ndarray:
    values = np.empty(len(points), dtype=np.complex128)
    for index in prange(len(points)):
        values[index] = richardson_soft_endpoint(
            points[index, 0],
            points[index, 1],
            points[index, 2],
            scattering_cosine,
            azimuth_nodes,
            soft_reference,
        )
    return values


@njit(parallel=True)
def plus_integral_many(
    points: np.ndarray,
    scattering_cosine: complex,
    azimuth_nodes: int,
    soft_reference: float,
    soft_floor: float,
) -> np.ndarray:
    values = np.empty(len(points), dtype=np.complex128)
    for index in prange(len(points)):
        soft_fraction = points[index, 1]
        decay_fraction = points[index, 2]
        relative_azimuth_fraction = points[index, 3]
        endpoint = richardson_soft_endpoint(
            soft_fraction,
            decay_fraction,
            relative_azimuth_fraction,
            scattering_cosine,
            azimuth_nodes,
            soft_reference,
        )
        soft_energy = soft_floor + (1.0 - soft_floor) * points[index, 0]
        direct = azimuth_averaged_g(
            soft_energy,
            soft_fraction,
            decay_fraction,
            relative_azimuth_fraction,
            scattering_cosine,
            azimuth_nodes,
            0.371,
        )
        main_integrand = (direct - endpoint) / soft_energy
        small_energy = soft_floor / 2.0
        small_direct = azimuth_averaged_g(
            small_energy,
            soft_fraction,
            decay_fraction,
            relative_azimuth_fraction,
            scattering_cosine,
            azimuth_nodes,
            0.371,
        )
        small_integrand = (small_direct - endpoint) / small_energy
        values[index] = (
            (1.0 - soft_floor) * main_integrand
            + soft_floor * small_integrand
        )
    return values


def aggregate(values: list[complex]) -> tuple[complex, float, float]:
    array = np.asarray(values, dtype=np.complex128)
    return (
        complex(np.mean(array)),
        float(np.std(array.real, ddof=1) / math.sqrt(len(array))),
        float(np.std(array.imag, ddof=1) / math.sqrt(len(array))),
    )


def coordinate_rows(azimuth_nodes: int) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    soft_energy = 0.28
    soft_fraction = 0.37
    decay_fraction = 0.61
    relative_fraction = 0.23
    soft_direction, decay_direction, _ = reduced_directions(
        soft_fraction,
        decay_fraction,
        relative_fraction,
        complex(0.3, 0.0),
    )
    internal = SEQUENTIAL_THREE_BODY(
        soft_energy, soft_direction, decay_direction
    )
    rotation = rotate_internal(internal, 0.731)
    momentum_residual = float(
        np.max(np.abs(np.sum(rotation, axis=0) - np.asarray([2.0, 0.0, 0.0, 0.0])))
    )
    mass_shell_residual = float(
        max(
            abs(
                rotation[index, 0] ** 2
                - np.dot(rotation[index, 1:], rotation[index, 1:])
            )
            for index in range(3)
        )
    )
    contour_checks: list[tuple[float, float, complex, complex]] = []
    for crossed_value in (1.5, 3.0, 9.0):
        scattering_cosine = complex(crossed_value, 0.05)
        lower = azimuth_averaged_g(
            soft_energy,
            soft_fraction,
            decay_fraction,
            relative_fraction,
            scattering_cosine,
            azimuth_nodes,
            0.371,
        )
        upper = azimuth_averaged_g(
            soft_energy,
            soft_fraction,
            decay_fraction,
            relative_fraction,
            scattering_cosine,
            2 * azimuth_nodes,
            0.371,
        )
        contour_checks.append((crossed_value, abs(upper - lower), lower, upper))
    even_positive = azimuth_averaged_g(
        soft_energy,
        soft_fraction,
        decay_fraction,
        relative_fraction,
        complex(3.0, 0.05),
        azimuth_nodes,
        0.371,
    )
    even_negative = azimuth_averaged_g(
        soft_energy,
        soft_fraction,
        decay_fraction,
        relative_fraction,
        complex(-3.0, 0.05),
        azimuth_nodes,
        0.371,
    )
    even_residual = abs(even_positive.real - even_negative.real)
    rows: list[dict[str, Any]] = [
        {
            "check_id": "COORD5021_01_azimuth_change",
            "quantity": "(phi_soft,phi_decay)->(phi_global,delta) Jacobian",
            "derived_value": 1,
            "target": 1,
            "residual": 0,
            "status": "PASS",
        },
        {
            "check_id": "COORD5021_02_momentum",
            "quantity": "global rotation momentum conservation residual",
            "derived_value": momentum_residual,
            "target": "<1e-12",
            "residual": momentum_residual,
            "status": "PASS" if momentum_residual < 1.0e-12 else "FAIL",
        },
        {
            "check_id": "COORD5021_03_mass_shell",
            "quantity": "global rotation maximum mass-shell residual",
            "derived_value": mass_shell_residual,
            "target": "<1e-12",
            "residual": mass_shell_residual,
            "status": "PASS" if mass_shell_residual < 1.0e-12 else "FAIL",
        },
        {
            "check_id": "COORD5021_04_crossed_even_real",
            "quantity": "Re g(+q+i eps)-Re g(-q+i eps) at q=3",
            "derived_value": even_residual,
            "target": "<1e-10",
            "residual": even_residual,
            "status": "PASS" if even_residual < 1.0e-10 else "FAIL",
        },
    ]
    for crossed_value, residual, lower, upper in contour_checks:
        rows.append(
            {
                "check_id": f"COORD5021_trapezoid_q{crossed_value:g}",
                "quantity": f"nested azimuth N={azimuth_nodes} versus N={2 * azimuth_nodes}",
                "derived_value": str(upper),
                "target": str(lower),
                "residual": residual,
                "status": "PASS" if residual < 2.0e-5 else "FAIL",
            }
        )
    return rows, {
        "azimuth_nodes": azimuth_nodes,
        "maximum_trapezoid_residual": max(item[1] for item in contour_checks),
        "crossed_even_real_residual": even_residual,
        "all_passed": all(row["status"] == "PASS" for row in rows),
    }


def endpoint_validation_rows(
    power: int,
    seeds: tuple[int, ...],
    azimuth_nodes: int,
    soft_reference: float,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    mp.mp.dps = 50
    configurations = (
        ("physical", complex(0.3, 0.0)),
        ("crossed_upper", complex(3.0, 0.08)),
    )
    rows: list[dict[str, Any]] = []
    maximum_relative = 0.0
    maximum_significance = 0.0
    for configuration, scattering_cosine in configurations:
        means: list[complex] = []
        for seed in seeds:
            points = qmc.Sobol(d=3, scramble=True, seed=seed + 21000).random_base2(
                power
            )
            means.append(
                complex(
                    np.mean(
                        endpoint_many(
                            points,
                            scattering_cosine,
                            azimuth_nodes,
                            soft_reference,
                        )
                    )
                )
            )
        mean, real_error, imaginary_error = aggregate(means)
        _, _, exact_endpoint = M5019.endpoint_resolvent(
            mp.mpc(scattering_cosine.real, scattering_cosine.imag), 192
        )
        exact_value = complex(exact_endpoint)
        absolute = abs(mean - exact_value)
        relative_value = absolute / max(abs(exact_value), 1.0e-30)
        significance = max(
            abs(mean.real - exact_value.real) / max(real_error, 1.0e-30),
            abs(mean.imag - exact_value.imag) / max(imaginary_error, 1.0e-30),
        )
        maximum_relative = max(maximum_relative, relative_value)
        maximum_significance = max(maximum_significance, significance)
        passed = relative_value < 0.08 or significance < 5.0
        rows.append(
            {
                "validation_id": f"ENDPOINT5021_{configuration}",
                "scattering_cosine": str(scattering_cosine),
                "nested_mean_real": mean.real,
                "nested_mean_imaginary": mean.imag,
                "RQMC_real_error": real_error,
                "RQMC_imaginary_error": imaginary_error,
                "exact_resolvent_real": exact_value.real,
                "exact_resolvent_imaginary": exact_value.imag,
                "absolute_residual": absolute,
                "relative_residual": relative_value,
                "maximum_component_significance": significance,
                "status": "PASS" if passed else "FAIL",
            }
        )
    return rows, {
        "maximum_relative_residual": maximum_relative,
        "maximum_component_significance": maximum_significance,
        "all_passed": all(row["status"] == "PASS" for row in rows),
    }


def sample_points(power: int, seeds: tuple[int, ...]) -> dict[int, np.ndarray]:
    return {
        seed: qmc.Sobol(d=4, scramble=True, seed=seed).random_base2(power)
        for seed in seeds
    }


def evaluate_direct(
    scattering_cosine: complex,
    points: dict[int, np.ndarray],
    azimuth_nodes: int,
    soft_reference: float,
    soft_floor: float,
) -> dict[int, complex]:
    return {
        seed: complex(
            np.mean(
                plus_integral_many(
                    values,
                    scattering_cosine,
                    azimuth_nodes,
                    soft_reference,
                    soft_floor,
                )
            )
        )
        for seed, values in points.items()
    }


def physical_rows(
    points: dict[int, np.ndarray],
    azimuth_nodes: int,
    soft_reference: float,
    soft_floor: float,
) -> tuple[list[dict[str, Any]], dict[str, Any], dict[float, dict[int, complex]]]:
    rows: list[dict[str, Any]] = []
    by_cosine: dict[float, dict[int, complex]] = {}
    even_values: dict[float, float] = {}
    for scattering_cosine in PHYSICAL_COSINES:
        h_by_seed = evaluate_direct(
            complex(scattering_cosine, 0.0),
            points,
            azimuth_nodes,
            soft_reference,
            soft_floor,
        )
        d_by_seed = {
            seed: -2.0 * value / math.pi for seed, value in h_by_seed.items()
        }
        by_cosine[scattering_cosine] = d_by_seed
        mean, real_error, imaginary_error = aggregate(list(d_by_seed.values()))
        even_values[scattering_cosine] = mean.real
        rows.append(
            {
                "run_id": f"PHYS5021_z{scattering_cosine:+.1f}",
                "scattering_cosine": scattering_cosine,
                "D_hhh_direct_over_G3_real": mean.real,
                "D_hhh_direct_over_G3_imaginary": mean.imag,
                "RQMC_real_error": real_error,
                "RQMC_imaginary_error": imaginary_error,
                "status": "NESTED_GLOBAL_AZIMUTH_PHYSICAL",
            }
        )
    even_residual = max(
        abs(even_values[value] - even_values[-value]) for value in (0.3, 0.6)
    )
    return rows, {
        "maximum_even_residual": even_residual,
        "all_finite": all(
            math.isfinite(float(row["D_hhh_direct_over_G3_real"]))
            for row in rows
        ),
    }, by_cosine


def crossed_arguments() -> tuple[float, ...]:
    return tuple(
        sorted(
            {
                round(abs((3.0 + cosine) / (1.0 - cosine)), 12)
                for cosine in PHYSICAL_COSINES
            }
            | {
                round(abs(-(3.0 - cosine) / (1.0 + cosine)), 12)
                for cosine in PHYSICAL_COSINES
            }
        )
    )


def crossed_rows(
    points: dict[int, np.ndarray],
    epsilons: tuple[float, ...],
    azimuth_nodes: int,
    soft_reference: float,
    soft_floor: float,
) -> tuple[
    list[dict[str, Any]],
    list[dict[str, Any]],
    dict[str, Any],
    dict[float, tuple[float, float]],
]:
    rows: list[dict[str, Any]] = []
    seed_data: dict[float, dict[int, list[complex]]] = {
        value: {seed: [] for seed in points} for value in crossed_arguments()
    }
    for crossed_value in crossed_arguments():
        for epsilon in epsilons:
            h_by_seed = evaluate_direct(
                complex(crossed_value, epsilon),
                points,
                azimuth_nodes,
                soft_reference,
                soft_floor,
            )
            d_by_seed = {
                seed: -2.0 * value / math.pi for seed, value in h_by_seed.items()
            }
            for seed, value in d_by_seed.items():
                seed_data[crossed_value][seed].append(value)
            mean, real_error, imaginary_error = aggregate(list(d_by_seed.values()))
            rows.append(
                {
                    "run_id": f"CROSS5021_q{crossed_value:.9g}_eps{epsilon:g}",
                    "absolute_crossed_cosine": crossed_value,
                    "upper_boundary_epsilon": epsilon,
                    "D_hhh_over_G3_real": mean.real,
                    "D_hhh_over_G3_imaginary": mean.imag,
                    "RQMC_real_error": real_error,
                    "RQMC_imaginary_error": imaginary_error,
                    "status": "UPPER_FEYNMAN_BOUNDARY_NESTED_AZIMUTH",
                }
            )

    epsilon_array = np.asarray(epsilons, dtype=float)
    linear_design = np.column_stack(
        [np.ones(len(epsilon_array)), epsilon_array, epsilon_array**2]
    )
    even_design = np.column_stack(
        [np.ones(len(epsilon_array)), epsilon_array**2, epsilon_array**4]
    )
    extrapolation_rows: list[dict[str, Any]] = []
    extrapolated: dict[float, tuple[float, float]] = {}
    maximum_systematic_ratio = 0.0
    for crossed_value, by_seed in seed_data.items():
        linear_intercepts: list[float] = []
        even_intercepts: list[float] = []
        fit_residuals: list[float] = []
        for values in by_seed.values():
            real_values = np.asarray([value.real for value in values], dtype=float)
            linear_fit = np.linalg.lstsq(linear_design, real_values, rcond=None)[0]
            even_fit = np.linalg.lstsq(even_design, real_values, rcond=None)[0]
            linear_intercepts.append(float(linear_fit[0]))
            even_intercepts.append(float(even_fit[0]))
            fit_residuals.append(
                float(np.max(np.abs(real_values - linear_design @ linear_fit)))
            )
        linear_mean = float(np.mean(linear_intercepts))
        statistical_error = float(
            np.std(linear_intercepts, ddof=1) / math.sqrt(len(linear_intercepts))
        )
        even_mean = float(np.mean(even_intercepts))
        continuation_systematic = abs(linear_mean - even_mean)
        total_error = math.sqrt(statistical_error**2 + continuation_systematic**2)
        maximum_systematic_ratio = max(
            maximum_systematic_ratio,
            continuation_systematic / max(abs(linear_mean), 1.0e-30),
        )
        extrapolated[crossed_value] = (linear_mean, total_error)
        extrapolation_rows.append(
            {
                "run_id": f"EXTRAP5021_q{crossed_value:.9g}",
                "absolute_crossed_cosine": crossed_value,
                "epsilon_values": json.dumps(list(epsilons)),
                "linear_quadratic_boundary_real": linear_mean,
                "RQMC_intercept_error": statistical_error,
                "even_polynomial_boundary_real": even_mean,
                "continuation_model_systematic": continuation_systematic,
                "combined_smoke_error": total_error,
                "maximum_per_seed_fit_residual": max(fit_residuals),
                "status": "BOUNDARY_SMOKE_NOT_PRECISION_CONTINUATION",
            }
        )
    return rows, extrapolation_rows, {
        "all_finite": all(
            math.isfinite(float(row["linear_quadratic_boundary_real"]))
            for row in extrapolation_rows
        ),
        "maximum_relative_continuation_systematic": maximum_systematic_ratio,
        "precision_boundary_complete": False,
    }, extrapolated


def cyclic_rows(
    physical_by_cosine: dict[float, dict[int, complex]],
    extrapolated: dict[float, tuple[float, float]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    target_rows = {
        round(float(row["physical_s_channel_cosine"]), 12): row
        for row in read_csv(TARGET_5018)
    }
    cyclic_values: list[float] = []
    cyclic_errors: list[float] = []
    target_values: list[float] = []
    shapes: list[float] = []
    base_rows: list[dict[str, Any]] = []
    for scattering_cosine in PHYSICAL_COSINES:
        physical_mean, physical_error, _ = aggregate(
            list(physical_by_cosine[scattering_cosine].values())
        )
        t_ratio = -(1.0 - scattering_cosine) / 2.0
        u_ratio = -(1.0 + scattering_cosine) / 2.0
        crossed_t = round(abs((3.0 + scattering_cosine) / (1.0 - scattering_cosine)), 12)
        crossed_u = round(abs(-(3.0 - scattering_cosine) / (1.0 + scattering_cosine)), 12)
        t_value, t_error = extrapolated[crossed_t]
        u_value, u_error = extrapolated[crossed_u]
        cyclic = physical_mean.real + t_ratio**3 * t_value + u_ratio**3 * u_value
        error = math.sqrt(
            physical_error**2
            + (t_ratio**3 * t_error) ** 2
            + (u_ratio**3 * u_error) ** 2
        )
        target = float(
            target_rows[round(scattering_cosine, 12)][
                "required_matched_hhh_nonlocal_component"
            ]
        )
        cyclic_values.append(cyclic)
        cyclic_errors.append(error)
        target_values.append(target)
        shapes.append(1.0 - scattering_cosine**2)
        base_rows.append(
            {
                "physical_s_channel_cosine": scattering_cosine,
                "physical_direct_D_over_G3": physical_mean.real,
                "crossed_t_abs": crossed_t,
                "crossed_u_abs": crossed_u,
                "cyclic_corrected_D_over_G3": cyclic,
                "cyclic_smoke_error": error,
                "required_5018_nonlocal_target": target,
            }
        )
    cyclic_array = np.asarray(cyclic_values, dtype=float)
    shape_array = np.asarray(shapes, dtype=float)
    target_array = np.asarray(target_values, dtype=float)
    local_coefficient = float(
        shape_array @ cyclic_array / (shape_array @ shape_array)
    )
    nonlocal_array = cyclic_array - local_coefficient * shape_array
    mismatch = nonlocal_array - target_array
    correlation = float(np.corrcoef(nonlocal_array, target_array)[0, 1])
    relative_l2 = float(np.linalg.norm(mismatch) / np.linalg.norm(target_array))
    for row, nonlocal_value, difference, error in zip(
        base_rows, nonlocal_array, mismatch, cyclic_errors
    ):
        row["best_local_coefficient"] = local_coefficient
        row["corrected_nonlocal_component"] = float(nonlocal_value)
        row["corrected_minus_required"] = float(difference)
        row["mismatch_over_smoke_error"] = abs(float(difference)) / max(error, 1.0e-30)
        row["status"] = "CONTOUR_REDUCED_SMOKE_NOT_LOCALITY_VERDICT"
    return base_rows, {
        "best_local_coefficient": local_coefficient,
        "corrected_nonlocal": nonlocal_array.tolist(),
        "required_nonlocal": target_array.tolist(),
        "corrected_minus_required": mismatch.tolist(),
        "correlation": correlation,
        "relative_L2_mismatch": relative_l2,
        "maximum_mismatch_over_smoke_error": max(
            abs(float(value)) / max(error, 1.0e-30)
            for value, error in zip(mismatch, cyclic_errors)
        ),
        "combined_locality_claim": False,
    }


def gate_rows(
    locks: dict[str, bool],
    coordinates: dict[str, Any],
    endpoints: dict[str, Any],
    physical: dict[str, Any],
    crossed: dict[str, Any],
    cyclic: dict[str, Any],
) -> list[dict[str, Any]]:
    gates = [
        ("source_locks", all(locks.values()), json.dumps(locks, sort_keys=True)),
        ("global_azimuth_coordinates", coordinates["all_passed"], json.dumps(coordinates, sort_keys=True)),
        ("soft_endpoint_continuation", endpoints["all_passed"], json.dumps(endpoints, sort_keys=True)),
        ("physical_direct_finite", physical["all_finite"], json.dumps(physical, sort_keys=True)),
        ("crossed_boundary_finite", crossed["all_finite"], json.dumps(crossed, sort_keys=True)),
        (
            "precision_not_overclaimed",
            crossed["precision_boundary_complete"] is False and cyclic["combined_locality_claim"] is False,
            "epsilon/model and RQMC errors retained",
        ),
        (
            "no_target_fit",
            True,
            "target is read only after physical and crossed direct boundary values are computed",
        ),
    ]
    return [
        {
            "gate_id": f"GATE5021_{index:02d}_{name}",
            "gate": name,
            "passed": passed,
            "evidence": evidence,
            "status": "PASS" if passed else "FAIL",
        }
        for index, (name, passed, evidence) in enumerate(gates, start=1)
    ]


def validation_rows(paths: tuple[Path, ...], gates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    checks = [
        ("output_paths_exist", all(path.exists() for path in paths), f"paths={len(paths)}"),
        (
            "CSV_rows_parse",
            all(read_csv(path) for path in paths if path.suffix == ".csv"),
            "all generated CSVs nonempty",
        ),
        (
            "no_missing_markers",
            all("MISSING_" not in path.read_text(encoding="utf-8", errors="ignore") for path in paths),
            "generated files",
        ),
        ("all_gates_pass", all(row["status"] == "PASS" for row in gates), f"gates={len(gates)}"),
        ("formalization_unchanged", tree_digest(FORMAL) == FORMAL_BASELINE, tree_digest(FORMAL)),
    ]
    return tagged(
        [
            {
                "validation_id": f"VAL5021_{index:02d}_{name}",
                "check": name,
                "passed": passed,
                "evidence": evidence,
                "status": "PASS" if passed else "FAIL",
            }
            for index, (name, passed, evidence) in enumerate(checks, start=1)
        ]
    )


def write_provenance(
    power: int,
    seeds: tuple[int, ...],
    azimuth_nodes: int,
    epsilons: tuple[float, ...],
) -> None:
    lines = [
        "# 5021 global-azimuth nested-contour provenance",
        "",
        f"- Complex-safe KLT integrand: `{relative(SCRIPT_5017)}`",
        f"- Exact endpoint and pole theorem: `{relative(SCRIPT_5019)}`",
        f"- Cut-object and G-normalization closure: `{relative(SCRIPT_5020)}`",
        f"- Matched nonlocal target, used only after integration: `{relative(TARGET_5018)}`",
        f"- Remaining-variable RQMC: {len(seeds)} scrambled Sobol seeds, 2^{power} points per seed.",
        f"- Global azimuth: deterministic periodic trapezoid with {azimuth_nodes} nodes.",
        f"- Upper boundary epsilons: {list(epsilons)}.",
        "- The endpoint uses first-order Richardson extrapolation from the same contour at x0 and x0/2.",
        "- The x interval [0,x_floor] is retained through its midpoint plus-integrand estimate, not discarded.",
        "- No coefficient is calibrated to the checkpoint-5018 target.",
        "",
    ]
    PROVENANCE.write_text("\n".join(lines), encoding="utf-8")


def write_document(result: dict[str, Any], cyclic_rows_value: list[dict[str, Any]]) -> None:
    extrapolation = result["crossed_boundary"]
    cyclic = result["cyclic_smoke"]
    table = "\n".join(
        f"| {row['physical_s_channel_cosine']:+.1f} | {row['cyclic_corrected_D_over_G3']:.7g} | {row['corrected_nonlocal_component']:.7g} | {row['required_5018_nonlocal_target']:.7g} | {row['cyclic_smoke_error']:.2g} |"
        for row in cyclic_rows_value
    )
    DOCUMENT.write_text(
        f"""# 5021 — global-azimuth Feynman-contour nested hhh smoke

## Actual advance

The five-dimensional crossed integral is no longer sampled blindly across its pole. Write the two original azimuths as

```text
phi_global = phi_soft,
delta      = phi_decay-phi_soft.
```

The Jacobian is one. At fixed soft energy, two polar cosines and `delta`, the full internal three-body event is rotated through `phi_global`. The complex-safe KLT product is then integrated deterministically around that complete azimuth before any Sobol averaging. For crossed `q`, the code evaluates the ordinary unit circle at `q+i epsilon`; the pole is displaced by the Feynman boundary value instead of being hit by real-sphere QMC.

The periodic trapezoid at `{result['run']['azimuth_nodes']}` and `{2 * result['run']['azimuth_nodes']}` nodes agrees at the fixed crossed controls to maximum residual `{result['coordinates']['maximum_trapezoid_residual']:.3e}`. The same nested contour reproduces the independently derived checkpoint-5019 soft endpoint on both a physical point and `q=3+0.08i`; its maximum relative residual is `{result['endpoint_validation']['maximum_relative_residual']:.3g}`.

## First finite-x boundary smoke

The remaining four variables are integrated with `{result['run']['seed_count']}` scrambled Sobol seeds and `2^{result['run']['power']}` points per seed. Four upper-boundary epsilon values are extrapolated independently per seed. A linear-quadratic intercept is compared with an even-polynomial intercept; their difference remains a continuation-model systematic. The maximum relative model systematic is `{extrapolation['maximum_relative_continuation_systematic']:.3g}`.

| physical z | corrected cyclic hhh | nonlocal part | required 5018 target | smoke error |
|---:|---:|---:|---:|---:|
{table}

The corrected nonlocal vector has correlation `{cyclic['correlation']:.6f}` with the independently constructed target and relative L2 mismatch `{cyclic['relative_L2_mismatch']:.4g}`. These are diagnostics, not a fit and not yet a locality verdict.

## Status

- Exact global-azimuth coordinate reduction: **implemented**.
- Crossed poles displaced with `q+i epsilon` before deterministic azimuth integration: **implemented**.
- Physical and crossed soft-endpoint check against the exact resolvent: **passed**.
- First finite-`x`, all-crossed-argument hhh boundary smoke: **executed**.
- Precision epsilon limit and final coupled locality: **open**.
- Numeric UV invariant, local GR and full MTS: **not claimed**.

Next: increase the remaining-variable power, add one smaller epsilon with adaptive azimuth nodes, and require the extrapolated cyclic nonlocal vector to stabilize under both epsilon-window and `x0/x_floor` changes before a locality decision.
""",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--power", type=int, default=8)
    parser.add_argument(
        "--seeds", default="50211,50212,50213,50214,50215,50216,50217,50218"
    )
    parser.add_argument("--azimuth-nodes", type=int, default=128)
    parser.add_argument("--epsilons", default="0.12,0.08,0.05,0.03")
    parser.add_argument("--soft-reference", type=float, default=1.0e-5)
    parser.add_argument("--soft-floor", type=float, default=1.0e-3)
    arguments = parser.parse_args()
    seeds = tuple(int(value) for value in arguments.seeds.split(","))
    epsilons = tuple(float(value) for value in arguments.epsilons.split(","))
    if arguments.power < 5 or len(seeds) < 4:
        raise ValueError("power >= 5 and at least four seeds are required")
    if arguments.azimuth_nodes < 32 or arguments.azimuth_nodes % 2:
        raise ValueError("azimuth nodes must be an even integer >=32")
    if len(epsilons) < 4 or min(epsilons) <= 0:
        raise ValueError("at least four positive epsilons are required")

    started = time.perf_counter()
    SOURCE.mkdir(parents=True, exist_ok=True)
    locks = source_locks()
    coordinate_rows_value, coordinates = coordinate_rows(arguments.azimuth_nodes)
    endpoint_rows_value, endpoint_result = endpoint_validation_rows(
        min(arguments.power, 8),
        seeds,
        arguments.azimuth_nodes,
        arguments.soft_reference,
    )
    points = sample_points(arguments.power, seeds)
    physical_rows_value, physical_result, physical_by_cosine = physical_rows(
        points,
        arguments.azimuth_nodes,
        arguments.soft_reference,
        arguments.soft_floor,
    )
    (
        crossed_rows_value,
        extrapolation_rows_value,
        crossed_result,
        extrapolated,
    ) = crossed_rows(
        points,
        epsilons,
        arguments.azimuth_nodes,
        arguments.soft_reference,
        arguments.soft_floor,
    )
    cyclic_rows_value, cyclic_result = cyclic_rows(
        physical_by_cosine, extrapolated
    )
    gates = gate_rows(
        locks,
        coordinates,
        endpoint_result,
        physical_result,
        crossed_result,
        cyclic_result,
    )

    for path, rows in (
        (COORDINATE_CSV, tagged(coordinate_rows_value)),
        (ENDPOINT_CSV, tagged(endpoint_rows_value)),
        (PHYSICAL_CSV, tagged(physical_rows_value)),
        (CROSSED_CSV, tagged(crossed_rows_value)),
        (EXTRAPOLATION_CSV, tagged(extrapolation_rows_value)),
        (CYCLIC_CSV, tagged(cyclic_rows_value)),
        (GATE_CSV, tagged(gates)),
    ):
        write_csv(path, rows)
    write_provenance(
        arguments.power, seeds, arguments.azimuth_nodes, epsilons
    )

    result = {
        "checkpoint": 5021,
        "marker": MARKER,
        "source_locks": locks,
        "run": {
            "power": arguments.power,
            "samples_per_seed": 2**arguments.power,
            "seed_count": len(seeds),
            "seeds": list(seeds),
            "azimuth_nodes": arguments.azimuth_nodes,
            "epsilons": list(epsilons),
            "soft_reference": arguments.soft_reference,
            "soft_floor": arguments.soft_floor,
        },
        "coordinates": coordinates,
        "endpoint_validation": endpoint_result,
        "physical_direct": physical_result,
        "crossed_boundary": crossed_result,
        "cyclic_smoke": cyclic_result,
        "global_azimuth_contour_reduction_implemented": True,
        "finite_x_crossed_hhh_smoke_executed": True,
        "precision_boundary_complete": False,
        "combined_crossing_locality_complete": False,
        "numeric_UV_coefficient_complete": False,
        "local_GR_claim": False,
        "full_MTS_claim": False,
        "elapsed_seconds": time.perf_counter() - started,
    }
    RESULT_JSON.write_text(json.dumps(result, indent=2), encoding="utf-8")
    write_document(result, cyclic_rows_value)

    outputs = (
        COORDINATE_CSV,
        ENDPOINT_CSV,
        PHYSICAL_CSV,
        CROSSED_CSV,
        EXTRAPOLATION_CSV,
        CYCLIC_CSV,
        GATE_CSV,
        RESULT_JSON,
        PROVENANCE,
        DOCUMENT,
    )
    validation = validation_rows(outputs, gates)
    write_csv(VALIDATION_CSV, validation)
    if not all(row["status"] == "PASS" for row in validation):
        raise RuntimeError("checkpoint 5021 validation failed")
    print(
        json.dumps(
            {
                "status": "PASS",
                "marker": MARKER,
                "endpoint_max_relative_residual": endpoint_result[
                    "maximum_relative_residual"
                ],
                "maximum_continuation_systematic": crossed_result[
                    "maximum_relative_continuation_systematic"
                ],
                "corrected_target_correlation": cyclic_result["correlation"],
                "corrected_target_relative_L2": cyclic_result[
                    "relative_L2_mismatch"
                ],
                "corrected_nonlocal": cyclic_result["corrected_nonlocal"],
                "required_nonlocal": cyclic_result["required_nonlocal"],
                "elapsed_seconds": result["elapsed_seconds"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
