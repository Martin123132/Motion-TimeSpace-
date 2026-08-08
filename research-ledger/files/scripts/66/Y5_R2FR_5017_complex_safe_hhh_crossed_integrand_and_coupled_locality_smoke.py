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

import numpy as np
from numba import njit, prange
from scipy.stats import qmc


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE = POST / "source-intake" / "functional_rg" / "5017"
RESIDUALS = POST / "source-intake" / "mts_residuals"

SCRIPT_5009 = POST / "scripts" / "Y5_R2FR_5009_three_particle_phase_space_and_five_point_tree_kernels.py"
SCRIPT_5010 = POST / "scripts" / "Y5_R2FR_5010_coupled_three_particle_cut_normalization_and_soft_plus_integrand.py"
SCRIPT_5015 = POST / "scripts" / "Y5_R2FR_5015_graph_complete_pph_crossed_sheet_continuation.py"
SCRIPT_5016 = POST / "scripts" / "Y5_R2FR_5016_completed_hh_crossed_function_and_hhh_nonlocal_target.py"
RESULT_5009 = POST / "source-intake" / "functional_rg" / "5009" / "three_particle_tree_kernel_results.json"
RESULT_5010 = POST / "source-intake" / "functional_rg" / "5010" / "coupled_three_particle_cut_results.json"
RESULT_5015 = POST / "source-intake" / "functional_rg" / "5015" / "graph_complete_pph_crossed_sheet_results.json"
RESULT_5016 = POST / "source-intake" / "functional_rg" / "5016" / "completed_hh_crossed_function_results.json"
PPH_CROSSING = POST / "source-intake" / "functional_rg" / "5015" / "graph_complete_pph_cyclic_crossing_function.csv"
HH_CROSSING = POST / "source-intake" / "functional_rg" / "5016" / "completed_hh_cyclic_crossing_function.csv"

KLT_SOURCE = POST / "source-intake" / "functional_rg" / "5009" / "sources" / "bjerrum_bohr_momentum_kernel_1010.3933" / "kernel_arxiv.tex"
DOCUMENT = POST / "5017-Y5-R2FR-complex-safe-hhh-crossed-integrand-and-coupled-locality-smoke.md"
CHECK_CSV = SOURCE / "complex_safe_hhh_KLT_checks.csv"
DIRECT_CSV = SOURCE / "graph_complete_hhh_direct_crossed_smoke.csv"
CROSSING_CSV = SOURCE / "graph_complete_hhh_cyclic_crossing_smoke.csv"
MASTER_CSV = SOURCE / "combined_master_cyclic_locality_smoke.csv"
GATE_CSV = SOURCE / "complex_safe_hhh_coupled_locality_gate.csv"
RESULT_JSON = SOURCE / "complex_safe_hhh_crossed_results.json"
PROVENANCE = SOURCE / "PROVENANCE.md"
VALIDATION_CSV = RESIDUALS / "P8_Y5_BRR545_5017_VALIDATION.csv"

MARKER = "MTS_5017_COMPLEX_SAFE_HHH_CROSSED_COUPLED_LOCALITY_SMOKE"
CHECKED_DATE = "2026-07-14"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
S_VALUE = 4.0


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
            "valid_for_full_MTS_claim": False,
            "source_checked_date": CHECKED_DATE,
        }
        for row in rows
    ]


def source_locks() -> dict[str, bool]:
    required = (
        SCRIPT_5009,
        SCRIPT_5010,
        SCRIPT_5015,
        SCRIPT_5016,
        RESULT_5009,
        RESULT_5010,
        RESULT_5015,
        RESULT_5016,
        PPH_CROSSING,
        HH_CROSSING,
        KLT_SOURCE,
    )
    result_5009 = read_json(RESULT_5009)
    result_5010 = read_json(RESULT_5010)
    result_5015 = read_json(RESULT_5015)
    result_5016 = read_json(RESULT_5016)
    source = KLT_SOURCE.read_text(encoding="utf-8", errors="ignore")
    return {
        "required_paths": all(path.exists() for path in required),
        "5009_five_point_KLT": result_5009["three_particle_tree_kernels_complete"] is True,
        "5010_hhh_normalization": result_5010["gates"]["klt_five_point_canonical_normalization"] is True,
        "5015_pph_crossing": result_5015["graph_complete_pph_crossed_function"] is True,
        "5016_hh_integral": result_5016["completed_hh_crossed_function"] is True,
        "primary_KLT_order": "opposite in the sets" in source,
    }


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
def external_complex(scattering_cosine: float, branch_sign: float) -> np.ndarray:
    transverse = branch_sign * np.sqrt(1.0 - scattering_cosine * scattering_cosine + 0.0j)
    result = np.empty((4, 4), dtype=np.complex128)
    result[0] = np.array([1.0, 0.0, 0.0, 1.0], dtype=np.complex128)
    result[1] = np.array([1.0, 0.0, 0.0, -1.0], dtype=np.complex128)
    result[2] = np.array([1.0, transverse, 0.0, scattering_cosine], dtype=np.complex128)
    result[3] = np.array([1.0, -transverse, 0.0, -scattering_cosine], dtype=np.complex128)
    return result


@njit
def massless_spinors(momentum: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    energy = momentum[0]
    px = momentum[1]
    py = momentum[2]
    pz = momentum[3]
    angle = np.empty(2, dtype=np.complex128)
    square = np.empty(2, dtype=np.complex128)
    if abs(energy + pz) > 1.0e-13:
        root = np.sqrt(energy + pz)
        angle[0] = root
        angle[1] = (px + 1j * py) / root
        square[0] = root
        square[1] = (px - 1j * py) / root
    else:
        root = np.sqrt(energy - pz)
        angle[0] = (px - 1j * py) / root
        angle[1] = root
        square[0] = (px + 1j * py) / root
        square[1] = root
    return angle, square


@njit
def spinor_table(momenta: np.ndarray) -> np.ndarray:
    spinors = np.empty((5, 2, 2), dtype=np.complex128)
    for index in range(5):
        angle, square = massless_spinors(momenta[index])
        spinors[index, 0] = angle
        spinors[index, 1] = square
    return spinors


@njit
def bracket(spinors: np.ndarray, left: int, right: int, chirality: int) -> complex:
    return (
        spinors[left, chirality, 0] * spinors[right, chirality, 1]
        - spinors[left, chirality, 1] * spinors[right, chirality, 0]
    )


@njit
def scalar_mhv(
    order: np.ndarray, special: int, spinors: np.ndarray, chirality: int
) -> complex:
    numerator = bracket(spinors, special, 0, chirality) ** 2
    numerator *= bracket(spinors, special, 4, chirality) ** 2
    denominator = 1.0 + 0.0j
    for index in range(len(order)):
        denominator *= bracket(
            spinors, order[index], order[(index + 1) % len(order)], chirality
        )
    return numerator / denominator


@njit
def invariant(momenta: np.ndarray, left: int, right: int) -> complex:
    return 2.0 * minkowski(momenta[left], momenta[right])


@njit
def momentum_kernel(
    alpha_reversed: int, beta_reversed: int, momenta: np.ndarray
) -> complex:
    s_21 = invariant(momenta, 1, 0)
    s_31 = invariant(momenta, 2, 0)
    s_23 = invariant(momenta, 1, 2)
    if alpha_reversed == 0 and beta_reversed == 0:
        return s_21 * s_31
    if alpha_reversed == 0 and beta_reversed == 1:
        return (s_21 + s_23) * s_31
    if alpha_reversed == 1 and beta_reversed == 0:
        return (s_31 + s_23) * s_21
    return s_31 * s_21


@njit
def scalar_klt_five(momenta: np.ndarray, special: int, chirality: int) -> complex:
    spinors = spinor_table(momenta)
    result = 0.0j
    for sigma_reversed in range(2):
        sigma_first = 1 if sigma_reversed == 0 else 2
        sigma_second = 2 if sigma_reversed == 0 else 1
        left_order = np.array(
            [0, sigma_first, sigma_second, 3, 4], dtype=np.int64
        )
        left = scalar_mhv(left_order, special, spinors, chirality)
        for gamma_reversed in range(2):
            gamma_first = 1 if gamma_reversed == 0 else 2
            gamma_second = 2 if gamma_reversed == 0 else 1
            right_order = np.array(
                [3, 4, gamma_first, gamma_second, 0], dtype=np.int64
            )
            result += (
                left
                * momentum_kernel(gamma_reversed, sigma_reversed, momenta)
                * scalar_mhv(right_order, special, spinors, chirality)
            )
    return result


@njit
def scalar_klt_four(momenta: np.ndarray, special: int, chirality: int) -> complex:
    spinors = np.empty((5, 2, 2), dtype=np.complex128)
    for index in (0, 1, 2, 4):
        angle, square = massless_spinors(momenta[index])
        spinors[index, 0] = angle
        spinors[index, 1] = square
    left_order = np.array([0, 1, 2, 4], dtype=np.int64)
    right_order = np.array([2, 4, 1, 0], dtype=np.int64)
    return -scalar_mhv(left_order, special, spinors, chirality) * invariant(
        momenta, 0, 1
    ) * scalar_mhv(right_order, special, spinors, chirality)


@njit
def cut_momenta(
    internal: np.ndarray, scattering_cosine: float, branch_sign: float
) -> tuple[np.ndarray, np.ndarray]:
    external = external_complex(scattering_cosine, branch_sign)
    left = np.empty((5, 4), dtype=np.complex128)
    right = np.empty((5, 4), dtype=np.complex128)
    left[0] = -external[0]
    left[4] = -external[1]
    right[0] = external[2]
    right[4] = external[3]
    for index in range(3):
        left[index + 1] = internal[index]
        right[index + 1] = -internal[index]
    return left, right


@njit
def hhh_reduced_product(
    internal: np.ndarray, scattering_cosine: float, branch_sign: float
) -> complex:
    left, right = cut_momenta(internal, scattering_cosine, branch_sign)
    result = 0.0j
    for special in (1, 2, 3):
        result += scalar_klt_five(left, special, 0) * scalar_klt_five(
            right, special, 1
        )
        result += scalar_klt_five(left, special, 1) * scalar_klt_five(
            right, special, 0
        )
    return result / 6.0


@njit
def spinor_soft_factor(
    hard_momenta: np.ndarray,
    soft_momentum: np.ndarray,
    chirality: int,
) -> complex:
    momenta = hard_momenta.copy()
    momenta[3] = soft_momentum
    spinors = spinor_table(momenta)
    opposite = 1 - chirality
    result = 0.0j
    for leg in (0, 1, 2, 4):
        result += (
            bracket(spinors, 3, leg, opposite)
            / bracket(spinors, 3, leg, chirality)
            * (
                bracket(spinors, 0, leg, chirality)
                / bracket(spinors, 0, 3, chirality)
            )
            ** 2
        )
    return result


@njit
def exact_hhh_g0(
    soft_direction: np.ndarray,
    decay_direction: np.ndarray,
    scattering_cosine: float,
    branch_sign: float,
) -> complex:
    internal = sequential_three_body(0.0, soft_direction, decay_direction)
    left, right = cut_momenta(internal, scattering_cosine, branch_sign)
    soft_left = np.empty(4, dtype=np.complex128)
    soft_left[0] = 1.0
    soft_left[1:] = soft_direction
    soft_right = -soft_left
    result = 0.0j
    for special in (1, 2):
        result += (
            spinor_soft_factor(left, soft_left, 0)
            * scalar_klt_four(left, special, 0)
            * spinor_soft_factor(right, soft_right, 1)
            * scalar_klt_four(right, special, 1)
        )
        result += (
            spinor_soft_factor(left, soft_left, 1)
            * scalar_klt_four(left, special, 1)
            * spinor_soft_factor(right, soft_right, 0)
            * scalar_klt_four(right, special, 0)
        )
    return result / (2.0 * S_VALUE * S_VALUE)


@njit
def hhh_plus_value(
    point: np.ndarray, scattering_cosine: float, branch_sign: float
) -> complex:
    soft_energy = min(max(point[0], 1.0e-10), 1.0 - 1.0e-10)
    soft_direction = direction(point[1], point[2])
    decay_direction = direction(point[3], point[4])
    internal = sequential_three_body(soft_energy, soft_direction, decay_direction)
    inverse_sum = 0.0
    for index in range(3):
        inverse_sum += 1.0 / (internal[index, 0] * internal[index, 0])
    multiplier = 3.0 / (internal[2, 0] * internal[2, 0]) / inverse_sum
    direct = (
        soft_energy
        * soft_energy
        * multiplier
        * hhh_reduced_product(internal, scattering_cosine, branch_sign)
        / (S_VALUE * S_VALUE)
    )
    zero = exact_hhh_g0(
        soft_direction, decay_direction, scattering_cosine, branch_sign
    )
    return (direct - zero) / soft_energy


@njit(parallel=True)
def hhh_plus_many(
    scattering_cosines: np.ndarray, points: np.ndarray, branch_sign: float
) -> np.ndarray:
    cosine_count = len(scattering_cosines)
    sample_count = len(points)
    result = np.empty((cosine_count, sample_count), dtype=np.complex128)
    for flat_index in prange(cosine_count * sample_count):
        sample_index = flat_index % sample_count
        cosine_index = flat_index // sample_count
        result[cosine_index, sample_index] = hhh_plus_value(
            points[sample_index], scattering_cosines[cosine_index], branch_sign
        )
    return result


def load_5010() -> Any:
    specification = importlib.util.spec_from_file_location("mts_checkpoint_5010_for_5017", SCRIPT_5010)
    if specification is None or specification.loader is None:
        raise RuntimeError("could not load checkpoint 5010")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


def kernel_checks() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    reference = load_5010()
    soft_energy = 0.31
    soft_direction = direction(0.43, 0.18)
    decay_direction = direction(0.71, 0.59)
    internal = sequential_three_body(soft_energy, soft_direction, decay_direction)
    cosine = 0.27
    accelerated = hhh_reduced_product(internal, cosine, 1.0)
    reference_internal = tuple(np.asarray(row) for row in internal)
    expected = reference.hhh_reduced_product(reference_internal, cosine)
    product_residual = abs(accelerated - expected) / max(abs(expected), 1.0e-30)
    accelerated_zero = exact_hhh_g0(soft_direction, decay_direction, cosine, 1.0)
    expected_zero = reference.exact_hhh_g0(soft_direction, decay_direction, cosine)
    zero_residual = abs(accelerated_zero - expected_zero) / max(abs(expected_zero), 1.0e-30)

    small_values: list[tuple[float, float]] = []
    for value in (1.0e-3, 3.0e-4, 1.0e-4):
        point = np.asarray([value, 0.43, 0.18, 0.71, 0.59])
        internal_value = sequential_three_body(
            value, direction(point[1], point[2]), direction(point[3], point[4])
        )
        inverse_sum = sum(1.0 / row[0] ** 2 for row in internal_value)
        multiplier = 3.0 / internal_value[2, 0] ** 2 / inverse_sum
        direct = (
            value**2
            * multiplier
            * hhh_reduced_product(internal_value, cosine, 1.0)
            / 16.0
        )
        small_values.append(
            (value, abs(direct - accelerated_zero) / max(abs(accelerated_zero), 1.0e-30))
        )

    crossed_cosine = 2.3
    point = np.asarray([0.29, 0.43, 0.18, 0.71, 0.59])
    branch_plus = hhh_plus_value(point, crossed_cosine, 1.0)
    branch_minus = hhh_plus_value(point, crossed_cosine, -1.0)
    branch_real_residual = abs(branch_plus.real - branch_minus.real) / max(
        abs(branch_plus.real), abs(branch_minus.real), 1.0e-30
    )

    rows = [
        {
            "check_id": "KLT5017_01_physical_five_point_product",
            "quantity": "Numba complex-safe hhh product / checkpoint-5010 product",
            "derived_value": accelerated,
            "reference_value": expected,
            "relative_residual": product_residual,
            "status": "PASS" if product_residual < 2.0e-10 else "FAIL",
        },
        {
            "check_id": "KLT5017_02_exact_soft_coefficient",
            "quantity": "Numba exact g0 / checkpoint-5010 exact g0",
            "derived_value": accelerated_zero,
            "reference_value": expected_zero,
            "relative_residual": zero_residual,
            "status": "PASS" if zero_residual < 2.0e-10 else "FAIL",
        },
        {
            "check_id": "KLT5017_03_soft_convergence",
            "quantity": "relative |g(x)-g0| at x=1e-4",
            "derived_value": small_values[-1][1],
            "reference_value": "tends to zero",
            "relative_residual": small_values[-1][1],
            "status": "PASS" if small_values[-1][1] < small_values[0][1] else "FAIL",
        },
        {
            "check_id": "KLT5017_04_crossed_branch_real_point",
            "quantity": "pointwise real branch comparison diagnostic",
            "derived_value": branch_real_residual,
            "reference_value": "not required pointwise; integrated real branch is target",
            "relative_residual": branch_real_residual,
            "status": "DIAGNOSTIC",
        },
    ]
    return rows, {
        "physical_product_relative_residual": product_residual,
        "soft_coefficient_relative_residual": zero_residual,
        "soft_convergence": [
            {"soft_energy": energy, "relative_residual": residual}
            for energy, residual in small_values
        ],
        "crossed_point_branch_real_residual": branch_real_residual,
        "all_required_pass": all(row["status"] == "PASS" for row in rows[:3]),
    }


def unique_cosines(
    physical_cosines: tuple[float, ...]
) -> tuple[np.ndarray, dict[float, int]]:
    values: list[float] = []
    for cosine in physical_cosines:
        for value in (
            cosine,
            (3.0 + cosine) / (1.0 - cosine),
            -(3.0 - cosine) / (1.0 + cosine),
        ):
            if not any(abs(value - present) < 1.0e-12 for present in values):
                values.append(value)
    values.sort()
    array = np.asarray(values, dtype=np.float64)
    return array, {round(value, 12): index for index, value in enumerate(array)}


def aggregate_complex(values: list[complex]) -> tuple[complex, float, float]:
    array = np.asarray(values, dtype=np.complex128)
    return (
        complex(np.mean(array)),
        float(np.std(array.real, ddof=1) / math.sqrt(len(array))),
        float(np.std(array.imag, ddof=1) / math.sqrt(len(array))),
    )


def hhh_run(
    power: int,
    seeds: tuple[int, ...],
    physical_cosines: tuple[float, ...],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    all_cosines, lookup = unique_cosines(physical_cosines)
    by_cosine: dict[float, list[complex]] = {float(value): [] for value in all_cosines}
    per_seed_samples: list[np.ndarray] = []
    for seed in seeds:
        points = qmc.Sobol(d=5, scramble=True, seed=seed).random_base2(power)
        values = -2.0 * hhh_plus_many(all_cosines, points, 1.0) / math.pi
        per_seed_samples.append(values)
        for cosine, mean in zip(all_cosines, np.mean(values, axis=1)):
            by_cosine[float(cosine)].append(complex(mean))

    direct_rows: list[dict[str, Any]] = []
    for cosine in all_cosines:
        mean, real_error, imaginary_error = aggregate_complex(by_cosine[float(cosine)])
        direct_rows.append(
            {
                "run_id": f"HHHDIRECT5017_z{cosine:.9g}",
                "scattering_cosine": cosine,
                "D_hhh_direct_over_G3_real": mean.real,
                "D_hhh_direct_over_G3_imaginary": mean.imag,
                "RQMC_real_error": real_error,
                "RQMC_imaginary_error": imaginary_error,
                "status": "PHYSICAL_DIRECT" if abs(cosine) <= 1.0 else "CROSSED_SHEET_SMOKE",
            }
        )

    crossing_rows: list[dict[str, Any]] = []
    crossing_values: dict[float, tuple[complex, float, float]] = {}
    for cosine in physical_cosines:
        t_ratio = -(1.0 - cosine) / 2.0
        u_ratio = -(1.0 + cosine) / 2.0
        z_t = (3.0 + cosine) / (1.0 - cosine)
        z_u = -(3.0 - cosine) / (1.0 + cosine)
        per_seed: list[complex] = []
        s_index = lookup[round(cosine, 12)]
        t_index = lookup[round(z_t, 12)]
        u_index = lookup[round(z_u, 12)]
        for values in per_seed_samples:
            correlated = (
                values[s_index]
                + t_ratio**3 * values[t_index]
                + u_ratio**3 * values[u_index]
            )
            per_seed.append(complex(np.mean(correlated)))
        mean, real_error, imaginary_error = aggregate_complex(per_seed)
        crossing_values[cosine] = (mean, real_error, imaginary_error)
        crossing_rows.append(
            {
                "run_id": f"HHHCROSS5017_z{cosine:.6g}",
                "physical_s_channel_cosine": cosine,
                "z_t": z_t,
                "z_u": z_u,
                "cyclic_D_hhh_over_G3_real": mean.real,
                "cyclic_D_hhh_over_G3_imaginary": mean.imag,
                "RQMC_real_error": real_error,
                "RQMC_imaginary_error": imaginary_error,
                "status": "CORRELATED_CYCLIC_SMOKE",
            }
        )
    even_residuals = [
        abs(crossing_values[value][0].real - crossing_values[-value][0].real)
        for value in physical_cosines
        if -value in crossing_values
    ]
    return direct_rows, crossing_rows, {
        "power": power,
        "samples_per_seed": 2**power,
        "seeds": list(seeds),
        "all_cosines": all_cosines.tolist(),
        "maximum_crossing_even_residual": max(even_residuals),
        "crossing": {
            str(value): {
                "real": crossing_values[value][0].real,
                "imaginary": crossing_values[value][0].imag,
                "real_error": crossing_values[value][1],
                "imaginary_error": crossing_values[value][2],
            }
            for value in physical_cosines
        },
    }


def f1_real(scattering_cosine: float) -> float:
    x_value = (1.0 - scattering_cosine) / 2.0
    y_value = 1.0 - x_value
    basis_a = -x_value**3 * math.log(x_value) - y_value**3 * math.log(y_value)
    basis_b = x_value * y_value * (math.log(x_value) + math.log(y_value))
    return 2.0 / math.pi * (23.0 * basis_a / 15.0 - basis_b / 30.0)


def combined_master_rows(
    physical_cosines: tuple[float, ...], hhh_rows: list[dict[str, Any]]
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    pph = {
        round(float(row["physical_s_channel_cosine"]), 12): row
        for row in read_csv(PPH_CROSSING)
    }
    hh = {
        round(float(row["physical_s_channel_cosine"]), 12): row
        for row in read_csv(HH_CROSSING)
    }
    hhh = {
        round(float(row["physical_s_channel_cosine"]), 12): row
        for row in hhh_rows
    }
    rows: list[dict[str, Any]] = []
    known: list[float] = []
    shapes: list[float] = []
    errors: list[float] = []
    scalar_d0 = 143.0 * (120.0 * math.pi**2 + 1397.0) / (6480.0 * math.pi)
    scalar_d2 = (-621877.0 + 103800.0 * math.pi**2) / (162000.0 * math.pi)
    for cosine in physical_cosines:
        key = round(cosine, 12)
        local_shape = 1.0 - cosine * cosine
        scalar_cross = 3.0 * (scalar_d0 - 5.0 * scalar_d2) * local_shape / 4.0
        hh_value = float(hh[key]["cyclic_D_hh_over_G3_real"])
        pph_value = float(pph[key]["cyclic_D_pph_over_G3_real"])
        hhh_value = float(hhh[key]["cyclic_D_hhh_over_G3_real"])
        hh_error = float(hh[key]["RQMC_real_error"])
        pph_error = float(pph[key]["RQMC_real_error"])
        hhh_error = float(hhh[key]["RQMC_real_error"])
        d1_master = 20.3 * f1_real(cosine)
        master = 2.0 * (scalar_cross + hh_value + pph_value + hhh_value) + d1_master
        error = 2.0 * math.sqrt(hh_error**2 + pph_error**2 + hhh_error**2)
        known.append(master)
        shapes.append(local_shape)
        errors.append(error)
        rows.append(
            {
                "physical_s_channel_cosine": cosine,
                "scalar_cyclic_D_over_G3": scalar_cross,
                "hh_cyclic_D_over_G3": hh_value,
                "pph_cyclic_D_over_G3": pph_value,
                "hhh_cyclic_D_over_G3": hhh_value,
                "D1_master_term_over_G3": d1_master,
                "combined_master_over_G3": master,
                "combined_RQMC_error": error,
            }
        )
    values = np.asarray(known)
    shape = np.asarray(shapes)
    local_coefficient = float(shape @ values / (shape @ shape))
    residuals = values - local_coefficient * shape
    for row, residual, error in zip(rows, residuals, errors):
        row["best_local_stu_coefficient"] = local_coefficient
        row["nonlocal_residual"] = float(residual)
        row["residual_significance_sigma"] = abs(float(residual)) / max(error, 1.0e-30)
        row["status"] = "SMOKE_UNRESOLVED" if error >= abs(residual) else "NONLOCAL_AT_SMOKE_PRECISION"
    return rows, {
        "best_local_stu_coefficient": local_coefficient,
        "maximum_absolute_nonlocal_residual": float(np.max(np.abs(residuals))),
        "maximum_residual_significance_sigma": max(
            abs(float(residual)) / max(error, 1.0e-30)
            for residual, error in zip(residuals, errors)
        ),
        "combined_locality_claim": False,
    }


def gate_rows(
    locks: dict[str, bool],
    checks: dict[str, Any],
    run: dict[str, Any],
    master: dict[str, Any],
) -> list[dict[str, Any]]:
    gates: list[tuple[str, bool, str]] = [
        ("source_locks", all(locks.values()), "all source and predecessor locks"),
        ("physical_KLT_parity", checks["physical_product_relative_residual"] < 2.0e-10, str(checks["physical_product_relative_residual"])),
        ("exact_soft_coefficient_parity", checks["soft_coefficient_relative_residual"] < 2.0e-10, str(checks["soft_coefficient_relative_residual"])),
        ("soft_limit_converges", checks["soft_convergence"][-1]["relative_residual"] < checks["soft_convergence"][0]["relative_residual"], json.dumps(checks["soft_convergence"])),
        ("crossed_hhh_smoke_finite", all(math.isfinite(item["real"]) and math.isfinite(item["imaginary"]) for item in run["crossing"].values()), f"rows={len(run['crossing'])}"),
        ("combined_locality_not_overclaimed", master["combined_locality_claim"] is False, "precision and analytic-continuation gates remain open"),
    ]
    return [
        {
            "gate_id": f"GATE5017_{index:02d}_{name}",
            "gate": name,
            "passed": passed,
            "evidence": evidence,
            "status": "PASS" if passed else "FAIL",
        }
        for index, (name, passed, evidence) in enumerate(gates, start=1)
    ]


def validation_rows(paths: tuple[Path, ...], gates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    checks = [
        ("output_paths_exist", all(path.exists() for path in paths), ";".join(relative(path) for path in paths)),
        ("CSV_rows_parse", all(read_csv(path) for path in paths if path.suffix == ".csv"), "all generated CSVs nonempty"),
        ("no_missing_markers", all("MISSING_" not in path.read_text(encoding="utf-8", errors="ignore") for path in paths), "generated files"),
        ("all_required_gates_pass", all(row["status"] == "PASS" for row in gates), f"gates={len(gates)}"),
        ("formalization_unchanged", tree_digest(FORMAL) == FORMAL_BASELINE, tree_digest(FORMAL)),
    ]
    return tagged(
        [
            {
                "validation_id": f"VAL5017_{index:02d}_{name}",
                "check": name,
                "passed": passed,
                "evidence": evidence,
                "status": "PASS" if passed else "FAIL",
            }
            for index, (name, passed, evidence) in enumerate(checks, start=1)
        ]
    )


def write_provenance(power: int, seeds: tuple[int, ...]) -> None:
    PROVENANCE.write_text(
        "\n".join(
            [
                "# 5017 complex-safe hhh provenance",
                "",
                f"- KLT source: `{relative(KLT_SOURCE)}`",
                f"- Five-point kernel checkpoint: `{relative(SCRIPT_5009)}`",
                f"- Coupling/soft normalization checkpoint: `{relative(SCRIPT_5010)}`",
                f"- hh crossing input: `{relative(HH_CROSSING)}`",
                f"- pph crossing input: `{relative(PPH_CROSSING)}`",
                f"- RQMC: {len(seeds)} scrambled Sobol seeds, 2^{power} points each.",
                "- The complex continuation retains complex Mandelstam invariants in the KLT momentum kernel; it does not discard their imaginary parts.",
                "- Crossed values are smoke estimates. Large variance or unresolved sheet singularities block a locality claim.",
                "",
            ]
        ),
        encoding="utf-8",
    )


def write_document(
    result: dict[str, Any],
    crossing_rows: list[dict[str, Any]],
    master_rows: list[dict[str, Any]],
) -> None:
    hhh_table = "\n".join(
        f"| {row['physical_s_channel_cosine']:.3g} | {row['cyclic_D_hhh_over_G3_real']:.8g} | {row['RQMC_real_error']:.2g} | {row['cyclic_D_hhh_over_G3_imaginary']:.3g} |"
        for row in crossing_rows
    )
    master_table = "\n".join(
        f"| {row['physical_s_channel_cosine']:.3g} | {row['combined_master_over_G3']:.8g} | {row['nonlocal_residual']:.8g} | {row['combined_RQMC_error']:.2g} |"
        for row in master_rows
    )
    DOCUMENT.write_text(
        f"""# 5017 — complex-safe hhh crossed integrand and coupled locality smoke

## Exact implementation gain

The sourced five-point KLT sum is now reimplemented with complex Mandelstam invariants throughout. The previous physical implementation converted the momentum kernel to `float(real)` and therefore could not legally be used on the crossed sheets. At a physical point the new kernel agrees with checkpoint 5010 to relative residual `{result['checks']['physical_product_relative_residual']:.3e}`; its exact soft coefficient agrees to `{result['checks']['soft_coefficient_relative_residual']:.3e}`.

For every phase-space point the code evaluates the correlated cyclic combination

```text
C_hhh(z)=D_hhh(z)+[-(1-z)/2]^3 D_hhh((3+z)/(1-z))
                   +[-(1+z)/2]^3 D_hhh(-(3-z)/(1+z)).
```

No direct-channel Legendre continuation and no fitted cancellation coefficient is used.

| z | Re C_hhh/G^3 | RQMC error | Im C_hhh/G^3 |
|---:|---:|---:|---:|
{hhh_table}

## First full coupled smoke

The scalar, completed `hh`, graph-complete `phi phi h`, complex-safe `hhh`, and sourced `D1 ReF1` pieces are now present in one crossing-complete numerical object:

```text
M_full=2(C_phi+C_hh+C_phiphih+C_hhh)+(203/10)F1.
```

After removing the best local `c(1-z^2)` component:

| z | full smoke master | nonlocal residual | combined RQMC error |
|---:|---:|---:|---:|
{master_table}

The maximum residual significance is `{result['master']['maximum_residual_significance_sigma']:.3g}` sigma. This is a smoke diagnostic, not a locality verdict: checkpoint 5016's isolated crossed `hh` estimator still has large variance, and the crossed-sheet pole prescription has not yet been stabilized analytically.

## Status

- Complex-safe graph-complete `2phi+3h` KLT kernel: **implemented and physically cross-checked**.
- Exact `hhh` soft coefficient and plus integrand: **cross-checked against checkpoint 5010**.
- Correlated full cyclic `hhh` estimator: **executed**.
- First all-sector crossing-complete locality smoke: **executed**.
- Precision crossing locality, numeric UV coefficient, local GR, and full MTS: **not claimed**.

Next: stabilize the common crossed-sheet prescription at the integrand level, preferably by combining the `hh` hard term with the `hhh` soft sector before numerical integration, then rerun the same full-master residual without changing its normalization.
""",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--power", type=int, default=8)
    parser.add_argument("--seeds", default="50171,50172,50173,50174")
    parser.add_argument("--physical-cosines", default="-0.6,-0.3,0,0.3,0.6")
    arguments = parser.parse_args()
    seeds = tuple(int(value) for value in arguments.seeds.split(","))
    physical_cosines = tuple(float(value) for value in arguments.physical_cosines.split(","))
    if arguments.power < 5 or len(seeds) < 3:
        raise ValueError("power >= 5 and at least three seeds are required")
    if any(abs(value) >= 0.9 for value in physical_cosines):
        raise ValueError("physical cosines must satisfy |z|<0.9")

    started = time.perf_counter()
    SOURCE.mkdir(parents=True, exist_ok=True)
    locks = source_locks()
    check_rows, checks = kernel_checks()
    direct_rows, crossing_rows, run = hhh_run(
        arguments.power, seeds, physical_cosines
    )
    master_rows, master = combined_master_rows(physical_cosines, crossing_rows)
    gates = gate_rows(locks, checks, run, master)

    for path, rows in (
        (CHECK_CSV, tagged(check_rows)),
        (DIRECT_CSV, tagged(direct_rows)),
        (CROSSING_CSV, tagged(crossing_rows)),
        (MASTER_CSV, tagged(master_rows)),
        (GATE_CSV, tagged(gates)),
    ):
        write_csv(path, rows)
    write_provenance(arguments.power, seeds)

    result = {
        "checkpoint": 5017,
        "marker": MARKER,
        "source_locks": locks,
        "checks": checks,
        "run": run,
        "master": master,
        "complex_safe_five_point_KLT": True,
        "graph_complete_hhh_cyclic_smoke": True,
        "combined_crossing_locality_complete": False,
        "numeric_UV_coefficient_complete": False,
        "local_GR_claim": False,
        "full_MTS_claim": False,
        "elapsed_seconds": time.perf_counter() - started,
    }
    RESULT_JSON.write_text(json.dumps(result, indent=2), encoding="utf-8")
    write_document(result, crossing_rows, master_rows)
    validation = validation_rows(
        (
            CHECK_CSV,
            DIRECT_CSV,
            CROSSING_CSV,
            MASTER_CSV,
            GATE_CSV,
            RESULT_JSON,
            PROVENANCE,
            DOCUMENT,
        ),
        gates,
    )
    write_csv(VALIDATION_CSV, validation)
    if not all(row["status"] == "PASS" for row in validation):
        raise RuntimeError("checkpoint 5017 validation failed")
    print(
        json.dumps(
            {
                "status": "PASS",
                "marker": MARKER,
                "physical_KLT_residual": checks[
                    "physical_product_relative_residual"
                ],
                "soft_coefficient_residual": checks[
                    "soft_coefficient_relative_residual"
                ],
                "hhh_crossing": run["crossing"],
                "maximum_master_nonlocal_residual": master[
                    "maximum_absolute_nonlocal_residual"
                ],
                "maximum_master_residual_sigma": master[
                    "maximum_residual_significance_sigma"
                ],
                "elapsed_seconds": result["elapsed_seconds"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
