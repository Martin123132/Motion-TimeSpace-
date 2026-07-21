from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import math
import sys
import time
from pathlib import Path
from typing import Any

import numpy as np
from numba import njit, prange
from scipy.stats import qmc


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE = POST / "source-intake" / "functional_rg" / "5011"
RESIDUALS = POST / "source-intake" / "mts_residuals"
SCRIPT_5010 = POST / "scripts" / "Y5_R2FR_5010_coupled_three_particle_cut_normalization_and_soft_plus_integrand.py"
RESULT_5010 = POST / "source-intake" / "functional_rg" / "5010" / "coupled_three_particle_cut_results.json"
RESULT_5008 = POST / "source-intake" / "functional_rg" / "5008" / "hh_outer_Wigner_insertion_results.json"
HH_TOWER = POST / "source-intake" / "functional_rg" / "5008" / "hh_wigner_partial_wave_tower.csv"
DOCUMENT = POST / "5011-Y5-R2FR-coupled-outer-partial-wave-cancellation-test.md"

PARITY_CSV = SOURCE / "accelerated_phiphih_integrand_parity_checks.csv"
CONVERGENCE_CSV = SOURCE / "three_particle_partial_wave_convergence.csv"
CANCELLATION_CSV = SOURCE / "coupled_outer_partial_wave_cancellation.csv"
GATE_CSV = SOURCE / "coupled_outer_projection_gate.csv"
RESULT_JSON = SOURCE / "coupled_outer_partial_wave_results.json"
PROVENANCE = SOURCE / "PROVENANCE.md"
VALIDATION_CSV = RESIDUALS / "P8_Y5_BRR545_5011_VALIDATION.csv"

MARKER = "MTS_5011_COUPLED_OUTER_PARTIAL_WAVE_CANCELLATION_TEST"
CHECKED_DATE = "2026-07-14"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
PAIRINGS = np.array(
    [
        [[0, 1], [2, 3]],
        [[0, 2], [1, 3]],
        [[0, 3], [1, 2]],
    ],
    dtype=np.int64,
)


def load_5010() -> Any:
    specification = importlib.util.spec_from_file_location("mts_checkpoint_5010", SCRIPT_5010)
    if specification is None or specification.loader is None:
        raise RuntimeError("could not load checkpoint 5010")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


BASE = load_5010()


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
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
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
            "valid_for_full_MTS_claim": False,
            "source_checked_date": CHECKED_DATE,
        }
        for row in rows
    ]


@njit
def minkowski(left: np.ndarray, right: np.ndarray) -> complex:
    return left[0] * right[0] - left[1] * right[1] - left[2] * right[2] - left[3] * right[3]


@njit
def direction(first: float, second: float) -> np.ndarray:
    cosine = 2.0 * first - 1.0
    sine = math.sqrt(max(0.0, 1.0 - cosine * cosine))
    azimuth = 2.0 * math.pi * second
    return np.array(
        [sine * math.cos(azimuth), sine * math.sin(azimuth), cosine],
        dtype=np.float64,
    )


@njit
def lorentz_boost(momentum: np.ndarray, velocity: np.ndarray) -> np.ndarray:
    speed_squared = velocity @ velocity
    if speed_squared < 1.0e-30:
        return momentum.copy()
    gamma = 1.0 / math.sqrt(1.0 - speed_squared)
    projection = velocity @ momentum[1:]
    result = np.empty(4, dtype=np.float64)
    result[0] = gamma * (momentum[0] + projection)
    factor = (gamma - 1.0) * projection / speed_squared + gamma * momentum[0]
    result[1:] = momentum[1:] + factor * velocity
    return result


@njit
def sequential_three_body(
    soft_energy: float, soft_direction: np.ndarray, decay_direction: np.ndarray
) -> np.ndarray:
    soft = np.empty(4, dtype=np.float64)
    soft[0] = soft_energy
    soft[1:] = soft_energy * soft_direction
    recoil = np.empty(4, dtype=np.float64)
    recoil[0] = 2.0 - soft_energy
    recoil[1:] = -soft_energy * soft_direction
    recoil_mass = 2.0 * math.sqrt(max(0.0, 1.0 - soft_energy))
    first_rest = np.empty(4, dtype=np.float64)
    second_rest = np.empty(4, dtype=np.float64)
    first_rest[0] = recoil_mass / 2.0
    second_rest[0] = recoil_mass / 2.0
    first_rest[1:] = recoil_mass * decay_direction / 2.0
    second_rest[1:] = -recoil_mass * decay_direction / 2.0
    velocity = recoil[1:] / recoil[0]
    result = np.empty((3, 4), dtype=np.float64)
    result[0] = lorentz_boost(first_rest, velocity)
    result[1] = lorentz_boost(second_rest, velocity)
    result[2] = soft
    return result


@njit
def external_momenta(scattering_cosine: float) -> np.ndarray:
    transverse = math.sqrt(max(0.0, 1.0 - scattering_cosine * scattering_cosine))
    result = np.empty((4, 4), dtype=np.float64)
    result[0] = np.array([1.0, 0.0, 0.0, 1.0])
    result[1] = np.array([1.0, 0.0, 0.0, -1.0])
    result[2] = np.array([1.0, transverse, 0.0, scattering_cosine])
    result[3] = np.array([1.0, -transverse, 0.0, -scattering_cosine])
    return result


@njit
def circular_polarization(momentum: np.ndarray, helicity: int) -> np.ndarray:
    unit = momentum[1:] / math.sqrt(momentum[1:] @ momentum[1:])
    reference = np.array([0.0, 0.0, 1.0])
    if abs(unit @ reference) > 0.9:
        reference = np.array([0.0, 1.0, 0.0])
    first = np.cross(reference, unit)
    first = first / math.sqrt(first @ first)
    second = np.cross(unit, first)
    result = np.empty(4, dtype=np.complex128)
    result[0] = 0.0j
    result[1:] = (first + 1j * helicity * second) / math.sqrt(2.0)
    return result


@njit
def luna_pair(
    scalars: np.ndarray,
    graviton: np.ndarray,
    polarization: np.ndarray,
    pairing: np.ndarray,
) -> complex:
    first_in = pairing[0, 0]
    first_out = pairing[0, 1]
    second_in = pairing[1, 0]
    second_out = pairing[1, 1]
    p_1 = -scalars[first_in]
    p_2 = -scalars[second_in]
    q_1 = -scalars[first_in] - scalars[first_out]
    q_2 = -scalars[second_in] - scalars[second_out]
    line_1 = 2.0 * p_1 - q_1
    line_2 = 2.0 * p_2 - q_2
    numerator_a = minkowski(2.0 * p_1 + q_2, 2.0 * p_2 - q_2) * (
        2.0 * p_1 + 2.0 * q_2
    ) - (2.0 * minkowski(p_1, q_2) + minkowski(q_2, q_2)) * (
        2.0 * p_2 - q_2
    )
    numerator_b = minkowski(
        2.0 * p_1 - graviton - q_1, 2.0 * p_2 - q_2
    ) * (2.0 * p_1) + 2.0 * minkowski(p_1, graviton) * (2.0 * p_2 - q_2)
    numerator_c = (
        minkowski(line_1, graviton + q_2) * line_2
        + minkowski(line_1, line_2) * (q_1 - q_2)
        - minkowski(line_2, graviton + q_1) * line_1
    )
    numerator_d = minkowski(2.0 * p_1 - q_1, 2.0 * p_2 + q_1) * (
        2.0 * p_2 + 2.0 * q_1
    ) - (2.0 * minkowski(p_2, q_1) + minkowski(q_1, q_1)) * (
        2.0 * p_1 - q_1
    )
    numerator_e = minkowski(
        2.0 * p_1 - q_1, 2.0 * p_2 - graviton - q_2
    ) * (2.0 * p_2) + 2.0 * minkowski(p_2, graviton) * (2.0 * p_1 - q_1)
    q_1_squared = minkowski(q_1, q_1)
    q_2_squared = minkowski(q_2, q_2)
    denominators = np.empty(5, dtype=np.complex128)
    denominators[0] = (2.0 * minkowski(p_1, q_2) + q_2_squared) * q_2_squared
    denominators[1] = -2.0 * minkowski(p_1, graviton) * q_2_squared
    denominators[2] = q_1_squared * q_2_squared
    denominators[3] = (2.0 * minkowski(p_2, q_1) + q_1_squared) * q_1_squared
    denominators[4] = -2.0 * minkowski(p_2, graviton) * q_1_squared
    numerators = np.empty((5, 4), dtype=np.complex128)
    numerators[0] = numerator_a
    numerators[1] = numerator_b
    numerators[2] = numerator_c
    numerators[3] = numerator_d
    numerators[4] = numerator_e
    result = 0.0j
    for index in range(5):
        contracted = minkowski(polarization, numerators[index])
        result += contracted * contracted / denominators[index]
    return result


@njit
def luna_bose(
    scalars: np.ndarray, graviton: np.ndarray, polarization: np.ndarray
) -> complex:
    result = 0.0j
    for index in range(3):
        result += luna_pair(scalars, graviton, polarization, PAIRINGS[index])
    return result


@njit
def invariant_sum(left: np.ndarray, right: np.ndarray) -> float:
    value = left + right
    return float(minkowski(value, value).real)


@njit
def canonical_four_scalar(scalars: np.ndarray) -> complex:
    s_value = invariant_sum(scalars[0], scalars[1])
    t_value = invariant_sum(scalars[0], scalars[2])
    u_value = invariant_sum(scalars[0], scalars[3])
    return t_value * u_value / s_value + s_value * u_value / t_value + s_value * t_value / u_value


@njit
def vector_soft(
    scalars: np.ndarray, soft_momentum: np.ndarray, polarization: np.ndarray
) -> complex:
    result = 0.0j
    for index in range(4):
        contraction = minkowski(polarization, scalars[index])
        result += contraction * contraction / minkowski(scalars[index], soft_momentum)
    return result


@njit
def scalar_sets(
    internal: np.ndarray, scattering_cosine: float
) -> tuple[np.ndarray, np.ndarray]:
    external = external_momenta(scattering_cosine)
    left = np.empty((4, 4), dtype=np.float64)
    right = np.empty((4, 4), dtype=np.float64)
    left[0] = -external[0]
    left[1] = -external[1]
    left[2] = internal[0]
    left[3] = internal[1]
    right[0] = external[2]
    right[1] = external[3]
    right[2] = -internal[0]
    right[3] = -internal[1]
    return left, right


@njit
def pph_product(internal: np.ndarray, scattering_cosine: float) -> complex:
    left_scalars, right_scalars = scalar_sets(internal, scattering_cosine)
    graviton = internal[2]
    result = 0.0j
    for helicity in (-1, 1):
        polarization = circular_polarization(graviton, helicity)
        left = -luna_bose(left_scalars, graviton, polarization) / 8.0
        right = -luna_bose(
            right_scalars, -graviton, np.conjugate(polarization)
        ) / 8.0
        result += left * right
    return result / 2.0


@njit
def pph_g0(
    soft_direction: np.ndarray,
    decay_direction: np.ndarray,
    scattering_cosine: float,
) -> complex:
    internal = sequential_three_body(0.0, soft_direction, decay_direction)
    left_scalars, right_scalars = scalar_sets(internal, scattering_cosine)
    soft_left = np.empty(4, dtype=np.float64)
    soft_left[0] = 1.0
    soft_left[1:] = soft_direction
    soft_right = -soft_left
    left_four = canonical_four_scalar(left_scalars)
    right_four = canonical_four_scalar(right_scalars)
    result = 0.0j
    for helicity in (-1, 1):
        polarization = circular_polarization(soft_left, helicity)
        result += (
            vector_soft(left_scalars, soft_left, polarization)
            * left_four
            * vector_soft(
                right_scalars, soft_right, np.conjugate(polarization)
            )
            * right_four
        )
    return result / 32.0


@njit
def pph_plus_value(point: np.ndarray) -> float:
    scattering_cosine = 2.0 * point[0] - 1.0
    soft_energy = min(max(point[1], 1.0e-12), 1.0 - 1.0e-12)
    soft_direction = direction(point[2], point[3])
    decay_direction = direction(point[4], point[5])
    internal = sequential_three_body(soft_energy, soft_direction, decay_direction)
    direct = soft_energy * soft_energy * pph_product(internal, scattering_cosine) / 16.0
    zero = pph_g0(soft_direction, decay_direction, scattering_cosine)
    return float(((direct - zero) / soft_energy).real)


@njit(parallel=True)
def pph_plus_batch(points: np.ndarray) -> np.ndarray:
    result = np.empty(points.shape[0], dtype=np.float64)
    for index in prange(points.shape[0]):
        result[index] = pph_plus_value(points[index])
    return result


def legendre_values(scattering_cosines: np.ndarray, spin_max: int) -> dict[int, np.ndarray]:
    values = {0: np.ones_like(scattering_cosines), 1: scattering_cosines.copy()}
    for spin in range(2, spin_max + 1):
        values[spin] = (
            (2 * spin - 1) * scattering_cosines * values[spin - 1]
            - (spin - 1) * values[spin - 2]
        ) / spin
    return values


def moment_estimates(
    points: np.ndarray, plus_values: np.ndarray, spin_values: tuple[int, ...]
) -> dict[int, tuple[float, float]]:
    scattering_cosines = 2.0 * points[:, 0] - 1.0
    polynomials = legendre_values(scattering_cosines, max(spin_values))
    estimates: dict[int, tuple[float, float]] = {}
    for spin in spin_values:
        samples = -2.0 * polynomials[spin] * plus_values / math.pi
        estimates[spin] = (
            float(np.mean(samples)),
            float(np.std(samples, ddof=1) / math.sqrt(len(samples))),
        )
    return estimates


def accelerated_parity_checks() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    test_points = np.array(
        [
            [0.575, 0.31, 0.43, 0.18, 0.71, 0.59],
            [0.22, 0.63, 0.17, 0.81, 0.39, 0.27],
            [0.88, 0.08, 0.61, 0.44, 0.26, 0.73],
            [0.41, 0.92, 0.34, 0.66, 0.82, 0.11],
        ],
        dtype=np.float64,
    )
    accelerated = pph_plus_batch(test_points)
    rows: list[dict[str, Any]] = []
    maximum_relative = 0.0
    for index, point in enumerate(test_points, start=1):
        scattering_cosine = 2.0 * point[0] - 1.0
        soft_energy = point[1]
        soft_direction = BASE.sphere(point[2], point[3])
        decay_direction = BASE.sphere(point[4], point[5])
        internal = BASE.sequential_three_body(
            soft_energy, soft_direction, decay_direction
        )
        direct = (
            soft_energy
            * soft_energy
            * BASE.pph_reduced_product(internal, scattering_cosine)
            / 16.0
        )
        zero = BASE.exact_pph_g0(
            soft_direction, decay_direction, scattering_cosine
        )
        reference = float(((direct - zero) / soft_energy).real)
        residual = abs(accelerated[index - 1] - reference)
        relative_residual = residual / max(abs(reference), 1.0e-30)
        maximum_relative = max(maximum_relative, relative_residual)
        rows.append(
            {
                "check_id": f"PARITY5011_{index:02d}",
                "reference_H_phiphih": reference,
                "accelerated_H_phiphih": accelerated[index - 1],
                "absolute_residual": residual,
                "relative_residual": relative_residual,
                "status": "PASS" if relative_residual < 2.0e-10 else "FAIL",
            }
        )
    return rows, {"maximum_relative_residual": maximum_relative}


def pph_convergence(
    powers: tuple[int, ...], seeds: tuple[int, ...], spins: tuple[int, ...]
) -> tuple[list[dict[str, Any]], dict[int, dict[int, tuple[float, float]]]]:
    rows: list[dict[str, Any]] = []
    aggregate: dict[int, dict[int, tuple[float, float]]] = {}
    for power in powers:
        by_seed: dict[int, list[float]] = {spin: [] for spin in spins}
        for seed in seeds:
            points = qmc.Sobol(d=6, scramble=True, seed=seed).random_base2(power)
            plus_values = pph_plus_batch(points)
            estimates = moment_estimates(points, plus_values, spins)
            for spin in spins:
                mean, naive_error = estimates[spin]
                by_seed[spin].append(mean)
                rows.append(
                    {
                        "run_id": f"PPH5011_p{power}_seed{seed}_J{spin}",
                        "sector": "phiphih",
                        "power": power,
                        "samples": 2**power,
                        "seed": seed,
                        "spin_J": spin,
                        "partial_wave_D_over_G3": mean,
                        "naive_standard_error": naive_error,
                        "rqmc_standard_error": "seed_aggregate_row",
                        "status": "FINITE_RQMC_RUN",
                    }
                )
        aggregate[power] = {}
        for spin in spins:
            values = np.asarray(by_seed[spin], dtype=float)
            mean = float(np.mean(values))
            rqmc_error = float(np.std(values, ddof=1) / math.sqrt(len(values)))
            aggregate[power][spin] = (mean, rqmc_error)
            rows.append(
                {
                    "run_id": f"PPH5011_p{power}_aggregate_J{spin}",
                    "sector": "phiphih",
                    "power": power,
                    "samples": (2**power) * len(seeds),
                    "seed": "aggregate",
                    "spin_J": spin,
                    "partial_wave_D_over_G3": mean,
                    "naive_standard_error": "not_used",
                    "rqmc_standard_error": rqmc_error,
                    "status": "RQMC_AGGREGATE",
                }
            )
    return rows, aggregate


def hhh_moments(
    power: int, seeds: tuple[int, ...], spins: tuple[int, ...]
) -> tuple[list[dict[str, Any]], dict[int, tuple[float, float]]]:
    rows: list[dict[str, Any]] = []
    by_seed: dict[int, list[float]] = {spin: [] for spin in spins}
    for seed in seeds:
        points = qmc.Sobol(d=6, scramble=True, seed=seed).random_base2(power)
        plus_values = np.empty(len(points), dtype=float)
        for index, point in enumerate(points):
            scattering_cosine = 2.0 * point[0] - 1.0
            soft_energy = float(np.clip(point[1], 1.0e-12, 1.0 - 1.0e-12))
            soft_direction = BASE.sphere(float(point[2]), float(point[3]))
            decay_direction = BASE.sphere(float(point[4]), float(point[5]))
            direct, _ = BASE.direct_g_values(
                soft_energy, soft_direction, decay_direction, scattering_cosine
            )
            zero = BASE.exact_hhh_g0(
                soft_direction, decay_direction, scattering_cosine
            )
            plus_values[index] = float(((direct - zero) / soft_energy).real)
        estimates = moment_estimates(points, plus_values, spins)
        for spin in spins:
            mean, naive_error = estimates[spin]
            by_seed[spin].append(mean)
            rows.append(
                {
                    "run_id": f"HHH5011_p{power}_seed{seed}_J{spin}",
                    "sector": "hhh",
                    "power": power,
                    "samples": 2**power,
                    "seed": seed,
                    "spin_J": spin,
                    "partial_wave_D_over_G3": mean,
                    "naive_standard_error": naive_error,
                    "rqmc_standard_error": "seed_aggregate_row",
                    "status": "FINITE_RQMC_RUN",
                }
            )
    aggregate: dict[int, tuple[float, float]] = {}
    for spin in spins:
        values = np.asarray(by_seed[spin], dtype=float)
        mean = float(np.mean(values))
        rqmc_error = float(np.std(values, ddof=1) / math.sqrt(len(values)))
        aggregate[spin] = (mean, rqmc_error)
        rows.append(
            {
                "run_id": f"HHH5011_p{power}_aggregate_J{spin}",
                "sector": "hhh",
                "power": power,
                "samples": (2**power) * len(seeds),
                "seed": "aggregate",
                "spin_J": spin,
                "partial_wave_D_over_G3": mean,
                "naive_standard_error": "not_used",
                "rqmc_standard_error": rqmc_error,
                "status": "RQMC_AGGREGATE",
            }
        )
    return rows, aggregate


def hh_partial_waves() -> dict[int, float]:
    result: dict[int, float] = {}
    for row in read_csv(HH_TOWER):
        spin = int(row["spin_J"])
        result[spin] = -64.0 * float(row["tree_times_regular_numeric"]) / math.pi
    return result


def cancellation_rows(
    pph: dict[int, tuple[float, float]],
    hhh: dict[int, tuple[float, float]],
    hh: dict[int, float],
    spins: tuple[int, ...],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    high_spin_passes: list[bool] = []
    for spin in spins:
        pph_mean, pph_error = pph[spin]
        hhh_mean, hhh_error = hhh[spin]
        three_mean = pph_mean + hhh_mean
        three_error = math.sqrt(pph_error**2 + hhh_error**2)
        hh_value = hh.get(spin, 0.0)
        residual = hh_value + three_mean
        significance = abs(residual) / max(three_error, 1.0e-30)
        relative_to_hh = abs(residual) / max(abs(hh_value), 1.0e-30)
        cancellation_pass = spin < 4 or (
            significance < 3.0 and relative_to_hh < 0.25
        )
        if spin >= 4:
            high_spin_passes.append(cancellation_pass)
        rows.append(
            {
                "mode_id": f"CANCEL5011_J{spin:03d}",
                "spin_J": spin,
                "D_hh_over_G3": hh_value,
                "D_phiphih_over_G3": pph_mean,
                "D_hhh_over_G3": hhh_mean,
                "D_three_particle_over_G3": three_mean,
                "three_particle_rqmc_error": three_error,
                "coupled_residual_over_G3": residual,
                "residual_significance_sigma": significance,
                "residual_relative_to_hh": relative_to_hh,
                "expected_if_local": "unconstrained_J0_J2" if spin < 4 else "zero",
                "status": (
                    "LOCAL_MODE_RETAINED"
                    if spin < 4
                    else "CANCELLATION_PASS"
                    if cancellation_pass
                    else "CANCELLATION_NOT_ESTABLISHED"
                ),
                "valid_for_outer_UV_projection": False,
            }
        )
    return rows, {
        "all_tested_high_spin_modes_cancel": all(high_spin_passes),
        "tested_high_spin_modes": [spin for spin in spins if spin >= 4],
        "local_J0_coupled": rows[0]["coupled_residual_over_G3"],
        "local_J2_coupled": rows[1]["coupled_residual_over_G3"],
    }


def source_locks() -> dict[str, bool]:
    result_5010 = read_json(RESULT_5010)
    result_5008 = read_json(RESULT_5008)
    return {
        "required_paths": all(
            path.exists()
            for path in (SCRIPT_5010, RESULT_5010, RESULT_5008, HH_TOWER)
        ),
        "5010_tree_normalization": bool(
            result_5010["gates"]["luna_five_point_canonical_normalization"]
        )
        and bool(result_5010["gates"]["klt_five_point_canonical_normalization"]),
        "5010_soft_plus_integrand": bool(
            result_5010["gates"]["soft_plus_integrand_finite_smoke"]
        ),
        "5008_completed_hh_kernel": bool(
            result_5008["completed_one_loop_opposite_helicity_kernel_inserted"]
        ),
        "5008_hh_projection_open": not bool(
            result_5008["crossing_projection"][
                "hh_only_local_UV_projection_well_defined"
            ]
        ),
        "normalization_conversion": RESULT_5010.read_text(encoding="utf-8").find(
            "U3_plus/(kappa^6 s^3)=E[H]/(8192 pi^3)"
        )
        >= 0,
    }


def gate_rows(
    locks: dict[str, bool],
    parity: dict[str, Any],
    cancellation: dict[str, Any],
    convergence_stable: bool,
) -> list[dict[str, Any]]:
    closed = {
        "primary_source_lock": all(locks.values()),
        "accelerated_integrand_parity": parity["maximum_relative_residual"] < 2.0e-10,
        "kappa6_to_G3_conversion": True,
        "randomized_QMC_convergence_run": convergence_stable,
        "tested_high_spin_cancellation": cancellation[
            "all_tested_high_spin_modes_cancel"
        ],
    }
    open_gates = {
        "pointwise_soft_plus_uniformity": "the fixed-angle soft expansion is non-uniform in the overlapping forward region",
        "all_high_spin_cancellation": "requires cancellation beyond the finite tested tower with controlled tail",
        "virtual_real_scheme_match": "plus finite part must still be tied to the 5008 endpoint finite allocation",
        "outer_UV_projection": "only legal after high-spin and scheme gates both close",
        "numeric_full_K_mu_K_ang": "local projection remains blocked",
        "exact_all_operator_local_GR": "not claimed",
        "full_MTS": "not claimed",
    }
    rows: list[dict[str, Any]] = []
    for name, passed in closed.items():
        rows.append(
            {
                "gate": name,
                "passed": bool(passed),
                "evidence": "executable normalization/integration check",
                "status": "PASS" if passed else "FAIL_RESULT",
                "valid_for_checkpoint_claim": True,
            }
        )
    for name, evidence in open_gates.items():
        rows.append(
            {
                "gate": name,
                "passed": False,
                "evidence": evidence,
                "status": "OPEN_NONCLAIM",
                "valid_for_checkpoint_claim": False,
            }
        )
    return [
        {"gate_id": f"GATE5011_{index:02d}_{row['gate']}", **row}
        for index, row in enumerate(rows, start=1)
    ]


def validation_rows(
    locks: dict[str, bool],
    parity_rows: list[dict[str, Any]],
    convergence_rows: list[dict[str, Any]],
    cancellation_rows_value: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks: list[tuple[str, bool, str]] = []
    checks.extend(
        (f"source_{name}", passed, "checkpoint source lock")
        for name, passed in locks.items()
    )
    checks.append(("accelerated_parity", all(row["status"] == "PASS" for row in parity_rows), "Numba/reference equality"))
    checks.append(("convergence_rows_finite", all(math.isfinite(float(row["partial_wave_D_over_G3"])) for row in convergence_rows), f"rows={len(convergence_rows)}"))
    checks.append(("cancellation_rows_finite", all(math.isfinite(float(row["coupled_residual_over_G3"])) for row in cancellation_rows_value), f"rows={len(cancellation_rows_value)}"))
    checks.append(("negative_results_preserved", all(row["valid_for_outer_UV_projection"] is False for row in cancellation_rows_value), "no automatic promotion"))
    checks.append(("outer_claim_blocked", any(row["gate"] == "outer_UV_projection" and not row["passed"] for row in gates), "outer projection false"))
    formal_hash = tree_digest(FORMAL)
    checks.append(("formalization_workbench_unchanged", formal_hash == FORMAL_BASELINE, formal_hash))
    return [
        {
            "validation_id": f"VAL5011_{index:02d}_{name}",
            "check": name,
            "passed": bool(passed),
            "evidence": evidence,
            "status": "PASS" if passed else "FAIL",
            "checkpoint_marker": MARKER,
        }
        for index, (name, passed, evidence) in enumerate(checks, start=1)
    ]


def write_provenance(source_hashes: dict[str, str], locks: dict[str, bool]) -> None:
    lines = [
        "# 5011 coupled outer partial-wave provenance",
        "",
        f"Marker: `{MARKER}`.",
        "",
        f"Checked: `{CHECKED_DATE}`.",
        "",
        "## Inputs",
        "",
        "- Checkpoint 5008 exact `hh` Wigner tower in `G^3` normalization.",
        "- Checkpoint 5010 canonical `hhh` and `phi phi h` soft-plus integrands.",
        "- The conversion `kappa^6=(32 pi)^3 G^3`, giving `D3/G^3=-(2/pi) E[H]`.",
        "",
        "## Source locks",
        "",
    ]
    lines.extend(f"- `{name}`: `{value}`" for name, value in locks.items())
    lines.extend(["", "## SHA-256", ""])
    lines.extend(f"- `{path}`: `{value}`" for path, value in source_hashes.items())
    lines.extend(
        [
            "",
            "## Claim boundary",
            "",
            "This attempted a direct numerical test of whether the three-particle cuts cancel the nonlocal high-spin `hh` tower. The fixed-angle soft-plus estimator is now retained as a negative method result: it is non-uniform in the forward region and its RQMC errors are uncontrolled. Its mode values are not physical estimates. No outer UV, local-GR, or full-MTS claim is made.",
            "",
        ]
    )
    PROVENANCE.write_text("\n".join(lines), encoding="utf-8")


def write_document(result: dict[str, Any], rows: list[dict[str, Any]]) -> None:
    table_lines = [
        "| J | hh | phi phi h | hhh | coupled residual | sigma | status |",
        "|---:|---:|---:|---:|---:|---:|:---|",
    ]
    for row in rows:
        table_lines.append(
            f"| {row['spin_J']} | {row['D_hh_over_G3']:.8g} | {row['D_phiphih_over_G3']:.8g} | {row['D_hhh_over_G3']:.8g} | {row['coupled_residual_over_G3']:.8g} | {row['residual_significance_sigma']:.3g} | {row['status']} |"
        )
    result_text = (
        "The tested `J>=4` modes cancel within the declared RQMC gate."
        if result["cancellation"]["all_tested_high_spin_modes_cancel"]
        else "The pointwise soft-plus estimator does not establish any `J>=4` cancellation. Its multi-seed errors remain uncontrolled, and the large tails are generated by a soft expansion that is non-uniform in the forward region. These mode values are diagnostics, not physical partial-wave estimates."
    )
    DOCUMENT.write_text(
        f"""# 5011 — coupled outer partial-wave cancellation test

## Purpose

Checkpoint 5008 left a concrete question, not a vague missing-input list: do the `hhh` and `phi phi h` three-particle cuts remove the `J>=4` nonlocal tower of the completed `hh` outer cut?

Checkpoint 5010 gives

```text
D3_plus/kappa^6 = -E[H]/(16384 pi^4).
```

Using `kappa^2=32 pi G`, this becomes the directly comparable normalization

```text
D3_plus/G^3 = -(2/pi) E[H].
```

For `D(z)=sum_J (2J+1)d_J P_J(z)`, the code evaluates

```text
d_J^(3) = -(2/pi) E_[z,phase space][P_J(z) H(z,phase space)].
```

The `phi phi h` kernel is independently reimplemented with Numba and agrees pointwise with checkpoint 5010 to a maximum relative residual of `{result['accelerated_parity']['maximum_relative_residual']:.3e}`. This permits high-statistics randomized Sobol tests without changing the amplitude.

## Result

{result_text}

{chr(10).join(table_lines)}

`J=0,2` are retained local modes rather than cancellation targets. No value in this table is promoted to the final `K_mu/K_ang` projection while the high-spin tail and virtual-real finite scheme remain open.

## Remaining gate

- Pointwise accelerated/reference parity: **closed**.
- Finite randomized-QMC partial-wave evaluation: **not converged**.
- Pointwise fixed-angle soft-plus ordering: **rejected; not uniform at the forward boundary**.
- Tested high-spin cancellation: **{'closed' if result['cancellation']['all_tested_high_spin_modes_cancel'] else 'not established'}**.
- Untested high-spin tail and finite virtual-real scheme match: **open**.
- Outer UV projection, numeric `K_mu/K_ang`, local GR, and full MTS: **not claimed**.

Next: replace the invalid pointwise ordering by an angular-first distributional limit, derive the exact soft/forward overlap condition, and only then repeat the coupled partial-wave test.
""",
        encoding="utf-8",
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--pph-powers", default="12,14")
    parser.add_argument("--pph-seeds", default="5012,5013,5014,5015")
    parser.add_argument("--hhh-power", type=int, default=10)
    parser.add_argument("--hhh-seeds", default="5016,5017")
    parser.add_argument("--spin-max", type=int, default=8)
    args = parser.parse_args()
    started = time.perf_counter()

    powers = tuple(int(value) for value in args.pph_powers.split(","))
    pph_seeds = tuple(int(value) for value in args.pph_seeds.split(","))
    hhh_seeds = tuple(int(value) for value in args.hhh_seeds.split(","))
    spins = tuple(range(0, args.spin_max + 1, 2))
    if args.spin_max < 4 or args.spin_max % 2:
        raise ValueError("--spin-max must be an even integer at least four")
    locks = source_locks()
    if not all(locks.values()):
        raise RuntimeError(json.dumps(locks, indent=2, sort_keys=True))
    parity_rows, parity_result = accelerated_parity_checks()
    if args.dry_run:
        passed = all(row["status"] == "PASS" for row in parity_rows)
        print(
            json.dumps(
                {
                    "checkpoint_marker": MARKER,
                    "dry_run": True,
                    "source_locks": all(locks.values()),
                    "accelerated_integrand_parity": passed,
                    "maximum_relative_residual": parity_result[
                        "maximum_relative_residual"
                    ],
                    "elapsed_seconds": time.perf_counter() - started,
                },
                indent=2,
            )
        )
        return 0 if passed else 1

    pph_rows, pph_aggregate = pph_convergence(powers, pph_seeds, spins)
    hhh_rows, hhh_aggregate = hhh_moments(
        args.hhh_power, hhh_seeds, spins
    )
    largest_power = max(powers)
    pph_final = pph_aggregate[largest_power]
    hh_values = hh_partial_waves()
    cancellation_rows_value, cancellation_result = cancellation_rows(
        pph_final, hhh_aggregate, hh_values, spins
    )

    convergence_stable = len(powers) > 1
    if len(powers) > 1:
        previous = pph_aggregate[sorted(powers)[-2]]
        for spin in spins:
            difference = abs(pph_final[spin][0] - previous[spin][0])
            combined_error = math.sqrt(
                pph_final[spin][1] ** 2 + previous[spin][1] ** 2
            )
            drift_controlled = difference < 2.0 * combined_error
            error_controlled = pph_final[spin][1] < max(
                0.2 * abs(pph_final[spin][0]), 0.25
            )
            error_contracts = pph_final[spin][1] < previous[spin][1]
            convergence_stable = (
                convergence_stable
                and drift_controlled
                and error_controlled
                and error_contracts
            )
    convergence_rows = [*pph_rows, *hhh_rows]
    gates = gate_rows(
        locks, parity_result, cancellation_result, convergence_stable
    )
    validations = validation_rows(
        locks,
        parity_rows,
        convergence_rows,
        cancellation_rows_value,
        gates,
    )

    SOURCE.mkdir(parents=True, exist_ok=True)
    RESIDUALS.mkdir(parents=True, exist_ok=True)
    for path, rows in (
        (PARITY_CSV, parity_rows),
        (CONVERGENCE_CSV, convergence_rows),
        (CANCELLATION_CSV, cancellation_rows_value),
        (GATE_CSV, gates),
        (VALIDATION_CSV, validations),
    ):
        write_csv(path, tagged(rows) if path != VALIDATION_CSV else rows)

    source_paths = [SCRIPT_5010, RESULT_5010, RESULT_5008, HH_TOWER, Path(__file__).resolve()]
    source_hashes = {relative(path): digest(path) for path in source_paths}
    result = {
        "checkpoint_marker": MARKER,
        "source_locks": locks,
        "source_hashes": source_hashes,
        "normalization_conversion": "D3/G^3=-(2/pi) E[H]",
        "accelerated_parity": parity_result,
        "pph_powers": powers,
        "pph_seeds": pph_seeds,
        "hhh_power": args.hhh_power,
        "hhh_seeds": hhh_seeds,
        "spins": spins,
        "convergence_stable": convergence_stable,
        "pointwise_soft_plus_valid": False,
        "pointwise_soft_plus_failure": "soft and forward limits do not commute; checkpoint 5012 derives the angular-first replacement",
        "cancellation": cancellation_result,
        "gates": {row["gate"]: bool(row["passed"]) for row in gates},
        "validation_passed": all(row["passed"] for row in validations),
        "outer_UV_projection": False,
        "numeric_full_K_mu": False,
        "numeric_full_K_ang": False,
        "exact_all_operator_local_GR": False,
        "full_MTS": False,
        "elapsed_seconds": time.perf_counter() - started,
    }
    RESULT_JSON.write_text(
        json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8"
    )
    write_provenance(source_hashes, locks)
    write_document(result, cancellation_rows_value)

    print(
        json.dumps(
            {
                "checkpoint_marker": MARKER,
                "accelerated_parity": parity_result[
                    "maximum_relative_residual"
                ],
                "convergence_stable": convergence_stable,
                "tested_high_spin_cancellation": cancellation_result[
                    "all_tested_high_spin_modes_cancel"
                ],
                "validation_passed": result["validation_passed"],
                "elapsed_seconds": time.perf_counter() - started,
            },
            indent=2,
        )
    )
    return 0 if result["validation_passed"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
