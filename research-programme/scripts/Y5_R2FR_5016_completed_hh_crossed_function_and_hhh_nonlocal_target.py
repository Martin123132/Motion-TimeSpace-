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
SOURCE = POST / "source-intake" / "functional_rg" / "5016"
RESIDUALS = POST / "source-intake" / "mts_residuals"

SCRIPT_5015 = POST / "scripts" / "Y5_R2FR_5015_graph_complete_pph_crossed_sheet_continuation.py"
CHECKPOINT_4988 = POST / "4988-Y5-R2FR-renormalized-scalar-two-particle-cut-and-exact-partial-wave-projection.md"
CHECKPOINT_5008 = POST / "5008-Y5-R2FR-completed-hh-one-loop-kernel-outer-cut-Wigner-insertion.md"
CHECKPOINT_5014 = POST / "5014-Y5-R2FR-crossing-complete-locality-and-graph-complete-pph-bridge.md"
CHECKPOINT_5015 = POST / "5015-Y5-R2FR-graph-complete-pph-crossed-sheet-continuation.md"
RESULT_4988 = SOURCE.parent / "4988" / "scalar_cut_soft_subtraction_results.json"
RESULT_5005 = SOURCE.parent / "5005" / "finite_outer_kernel_results.json"
RESULT_5008 = SOURCE.parent / "5008" / "hh_outer_Wigner_insertion_results.json"
RESULT_5015 = SOURCE.parent / "5015" / "graph_complete_pph_crossed_sheet_results.json"
HH_TOWER = SOURCE.parent / "5008" / "hh_wigner_partial_wave_tower.csv"
PPH_CROSSING = SOURCE.parent / "5015" / "graph_complete_pph_cyclic_crossing_function.csv"

KLT_CHECK_CSV = SOURCE / "four_point_KLT_phase_and_kernel_checks.csv"
DIRECT_CSV = SOURCE / "completed_hh_direct_function.csv"
CROSSING_CSV = SOURCE / "completed_hh_cyclic_crossing_function.csv"
MASTER_CSV = SOURCE / "known_master_without_hhh_and_hhh_nonlocal_target.csv"
GATE_CSV = SOURCE / "completed_hh_crossing_gate.csv"
RESULT_JSON = SOURCE / "completed_hh_crossed_function_results.json"
PROVENANCE = SOURCE / "PROVENANCE.md"
DOCUMENT = POST / "5016-Y5-R2FR-completed-hh-crossed-function-and-hhh-nonlocal-target.md"
VALIDATION_CSV = RESIDUALS / "P8_Y5_BRR545_5016_VALIDATION.csv"

MARKER = "MTS_5016_COMPLETED_HH_CROSSED_FUNCTION_HHH_NONLOCAL_TARGET"
CHECKED_DATE = "2026-07-14"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"


def load_5015() -> Any:
    specification = importlib.util.spec_from_file_location("mts_checkpoint_5015_for_5016", SCRIPT_5015)
    if specification is None or specification.loader is None:
        raise RuntimeError("could not load checkpoint 5015")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


BASE = load_5015()
minkowski = BASE.minkowski
direction = BASE.direction
external_complex = BASE.external_complex


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
    if not rows:
        raise ValueError(f"no rows for {path}")
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
        SCRIPT_5015,
        CHECKPOINT_4988,
        CHECKPOINT_5008,
        CHECKPOINT_5014,
        CHECKPOINT_5015,
        RESULT_4988,
        RESULT_5005,
        RESULT_5008,
        RESULT_5015,
        HH_TOWER,
        PPH_CROSSING,
    )
    result_5008 = read_json(RESULT_5008)
    result_5015 = read_json(RESULT_5015)
    return {
        "required_paths": all(path.exists() for path in required),
        "5008_kernel_complete": result_5008["completed_one_loop_opposite_helicity_kernel_inserted"] is True,
        "5008_normalization": result_5008["normalization"]["reduced_cut_prefactor"] == "-64/pi",
        "5008_exact_tower": result_5008["partial_wave_tower"]["arbitrary_even_J_exact_generator"] is True,
        "5015_pph_crossed": result_5015["graph_complete_pph_crossed_function"] is True,
        "5015_same_sheet": result_5015["branch"]["real_part_branch_independent"] is True,
    }


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
def bracket(spinors: np.ndarray, left: int, right: int, chirality: int) -> complex:
    return (
        spinors[left, chirality, 0] * spinors[right, chirality, 1]
        - spinors[left, chirality, 1] * spinors[right, chirality, 0]
    )


@njit
def scalar_mhv_four(
    ordering: np.ndarray, special: int, spinors: np.ndarray, chirality: int
) -> complex:
    numerator = bracket(spinors, special, 0, chirality) ** 2
    numerator *= bracket(spinors, special, 3, chirality) ** 2
    denominator = 1.0 + 0.0j
    for index in range(4):
        denominator *= bracket(
            spinors,
            ordering[index],
            ordering[(index + 1) % 4],
            chirality,
        )
    return numerator / denominator


@njit
def scalar_klt_four(momenta: np.ndarray, special: int, chirality: int) -> complex:
    spinors = np.empty((4, 2, 2), dtype=np.complex128)
    for index in range(4):
        angle, square = massless_spinors(momenta[index])
        spinors[index, 0] = angle
        spinors[index, 1] = square
    left_order = np.array([0, 1, 2, 3], dtype=np.int64)
    right_order = np.array([2, 3, 1, 0], dtype=np.int64)
    s_12 = 2.0 * minkowski(momenta[0], momenta[1])
    return -scalar_mhv_four(
        left_order, special, spinors, chirality
    ) * s_12 * scalar_mhv_four(right_order, special, spinors, chirality)


@njit
def hard_kernel(scattering_cosine: complex) -> complex:
    x_value = (1.0 - scattering_cosine) / 2.0
    t_value = -x_value
    u_value = x_value - 1.0
    log_x = np.log(x_value)
    log_y = np.log(1.0 - x_value)
    coefficient_x = (
        t_value**3
        * u_value
        * (6.0 * t_value**2 - 9.0 * t_value * u_value - 11.0 * u_value**2)
        / 96.0
    )
    coefficient_xy = t_value**3 * u_value**3 / 8.0
    coefficient_xx = (
        t_value**4
        * (
            t_value**3
            + 2.0 * t_value**2 * u_value
            + 3.0 * t_value * u_value**2
            + u_value**3
        )
        / (16.0 * (t_value + u_value))
    )
    coefficient_y = (
        -t_value
        * u_value**3
        * (11.0 * t_value**2 + 9.0 * t_value * u_value - 6.0 * u_value**2)
        / 96.0
    )
    coefficient_yy = (
        u_value**4
        * (
            t_value**3
            + 3.0 * t_value**2 * u_value
            + 2.0 * t_value * u_value**2
            + u_value**3
        )
        / (16.0 * (t_value + u_value))
    )
    coefficient_pi = (
        t_value**6
        + t_value**5 * u_value
        + 2.0 * t_value**4 * u_value**2
        + 2.0 * t_value**2 * u_value**4
        + t_value * u_value**5
        + u_value**6
    ) / 16.0
    hard = (
        coefficient_x * log_x
        + coefficient_xy * log_x * log_y
        + coefficient_xx * log_x * log_x
        + coefficient_y * log_y
        + coefficient_yy * log_y * log_y
        + coefficient_pi * math.pi**2
    )
    hard_soft = math.pi**2 * (5.0 * x_value * x_value - 5.0 * x_value + 1.0) / 16.0
    return (hard - hard_soft) / (x_value**2 * (1.0 - x_value) ** 2)


@njit
def hh_integrand(
    internal_direction: np.ndarray, scattering_cosine: float, branch_sign: float
) -> complex:
    external = external_complex(scattering_cosine, branch_sign)
    first = np.empty(4, dtype=np.complex128)
    second = np.empty(4, dtype=np.complex128)
    first[0] = 1.0
    first[1:] = internal_direction
    second[0] = 1.0
    second[1:] = -internal_direction
    left = np.empty((4, 4), dtype=np.complex128)
    right = np.empty((4, 4), dtype=np.complex128)
    left[0] = -external[0]
    left[3] = -external[1]
    left[1] = first
    left[2] = second
    right[0] = external[2]
    right[3] = external[3]
    right[1] = -first
    right[2] = -second

    cosine_left = internal_direction[2]
    outgoing_direction = external[2, 1:]
    cosine_right = (
        outgoing_direction[0] * internal_direction[0]
        + outgoing_direction[1] * internal_direction[1]
        + outgoing_direction[2] * internal_direction[2]
    )
    tree_left = (1.0 - cosine_left * cosine_left) / 4.0
    tree_right = (1.0 - cosine_right * cosine_right) / 4.0
    left_minus_plus = scalar_klt_four(left, 1, 0)
    right_plus_minus = scalar_klt_four(right, 1, 1)
    left_plus_minus = scalar_klt_four(left, 1, 1)
    right_minus_plus = scalar_klt_four(right, 1, 0)
    phase_minus_plus = (
        left_minus_plus * right_plus_minus / (16.0 * tree_left * tree_right)
    )
    phase_plus_minus = (
        left_plus_minus * right_minus_plus / (16.0 * tree_left * tree_right)
    )
    phase_average = (phase_minus_plus + phase_plus_minus) / 2.0
    return tree_left * hard_kernel(cosine_right) * phase_average


@njit(parallel=True)
def hh_direct_many(
    scattering_cosines: np.ndarray,
    internal_directions: np.ndarray,
    branch_sign: float,
) -> np.ndarray:
    cosine_count = len(scattering_cosines)
    sample_count = len(internal_directions)
    values = np.empty((cosine_count, sample_count), dtype=np.complex128)
    for flat_index in prange(cosine_count * sample_count):
        sample_index = flat_index % sample_count
        cosine_index = flat_index // sample_count
        values[cosine_index, sample_index] = hh_integrand(
            internal_directions[sample_index],
            scattering_cosines[cosine_index],
            branch_sign,
        )
    return -64.0 * values / math.pi


def unique_cosines(physical_cosines: tuple[float, ...]) -> tuple[np.ndarray, dict[float, int]]:
    values: list[float] = []
    for cosine in physical_cosines:
        triplet = (
            cosine,
            (3.0 + cosine) / (1.0 - cosine),
            -(3.0 - cosine) / (1.0 + cosine),
        )
        for value in triplet:
            if not any(abs(value - present) < 1.0e-12 for present in values):
                values.append(value)
    values.sort()
    array = np.asarray(values, dtype=float)
    return array, {round(value, 12): index for index, value in enumerate(array)}


def aggregate_complex(values: list[complex]) -> tuple[complex, float, float]:
    array = np.asarray(values, dtype=np.complex128)
    return (
        complex(np.mean(array)),
        float(np.std(array.real, ddof=1) / math.sqrt(len(array))),
        float(np.std(array.imag, ddof=1) / math.sqrt(len(array))),
    )


def tower_direct(scattering_cosine: float) -> float:
    total = 0.0
    for row in read_csv(HH_TOWER):
        spin = int(row["spin_J"])
        coefficient = float(row["tree_times_regular_numeric"])
        legendre_coefficients = np.zeros(spin + 1)
        legendre_coefficients[-1] = 1.0
        polynomial = float(
            np.polynomial.legendre.legval(scattering_cosine, legendre_coefficients)
        )
        total += (2 * spin + 1) * coefficient * polynomial
    return -64.0 * total / math.pi


def klt_and_kernel_checks() -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    maximum_tree = 0.0
    maximum_kernel_crossing = 0.0
    for index, (cosine, azimuth) in enumerate(
        ((0.2, 0.7), (-0.6, 1.2), (0.73, 2.1)), start=1
    ):
        internal_direction = np.asarray(
            [
                math.sqrt(1.0 - cosine * cosine) * math.cos(azimuth),
                math.sqrt(1.0 - cosine * cosine) * math.sin(azimuth),
                cosine,
            ]
        )
        external = external_complex(1.0, 1.0)
        first = np.concatenate(([1.0], internal_direction)).astype(np.complex128)
        second = np.concatenate(([1.0], -internal_direction)).astype(np.complex128)
        left = np.asarray([-external[0], first, second, -external[1]])
        tree = (1.0 - cosine * cosine) / 4.0
        for special, chirality in ((1, 0), (2, 1)):
            amplitude = scalar_klt_four(left, special, chirality)
            residual = abs(amplitude + 4.0 * tree) / max(abs(amplitude), 1.0e-30)
            maximum_tree = max(maximum_tree, residual)
            rows.append(
                {
                    "check_id": f"KLT5016_{index}_{special}_{chirality}",
                    "quantity": "M4_KLT/[-4x(1-x)]",
                    "derived_value_real": amplitude.real / (-4.0 * tree),
                    "derived_value_imaginary": amplitude.imag / (-4.0 * tree),
                    "relative_residual": residual,
                    "status": "PASS" if residual < 2.0e-12 else "FAIL",
                }
            )
        kernel_left = hard_kernel(complex(cosine))
        kernel_right = hard_kernel(complex(-cosine))
        kernel_residual = abs(kernel_left - kernel_right) / max(abs(kernel_left), 1.0e-30)
        maximum_kernel_crossing = max(maximum_kernel_crossing, kernel_residual)
        rows.append(
            {
                "check_id": f"KERNEL5016_{index}",
                "quantity": "K(c)-K(-c)",
                "derived_value_real": (kernel_left - kernel_right).real,
                "derived_value_imaginary": (kernel_left - kernel_right).imag,
                "relative_residual": kernel_residual,
                "status": "PASS" if kernel_residual < 2.0e-12 else "FAIL",
            }
        )
    return rows, {
        "maximum_tree_normalization_residual": maximum_tree,
        "maximum_kernel_crossing_residual": maximum_kernel_crossing,
        "all_pass": all(row["status"] == "PASS" for row in rows),
    }


def completed_hh_run(
    power: int,
    seeds: tuple[int, ...],
    physical_cosines: tuple[float, ...],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any]]:
    all_cosines, lookup = unique_cosines(physical_cosines)
    by_cosine: dict[float, list[complex]] = {float(value): [] for value in all_cosines}
    for seed in seeds:
        points = qmc.Sobol(d=2, scramble=True, seed=seed).random_base2(power)
        directions = np.asarray(
            [direction(float(row[0]), float(row[1])) for row in points]
        )
        values = hh_direct_many(all_cosines, directions, 1.0)
        means = np.mean(values, axis=1)
        for cosine, mean in zip(all_cosines, means):
            by_cosine[float(cosine)].append(complex(mean))

    direct_rows: list[dict[str, Any]] = []
    direct_summary: dict[str, dict[str, float]] = {}
    physical_tower_residuals: list[float] = []
    for cosine in all_cosines:
        mean, real_error, imaginary_error = aggregate_complex(by_cosine[float(cosine)])
        if abs(cosine) <= 1.0:
            tower = tower_direct(float(cosine))
            tower_residual = mean.real - tower
            physical_tower_residuals.append(abs(tower_residual))
        else:
            tower = math.nan
            tower_residual = math.nan
        direct_rows.append(
            {
                "run_id": f"HHDIRECT5016_z{cosine:.9g}",
                "scattering_cosine": cosine,
                "D_hh_direct_over_G3_real": mean.real,
                "D_hh_direct_over_G3_imaginary": mean.imag,
                "RQMC_real_error": real_error,
                "RQMC_imaginary_error": imaginary_error,
                "J40_tower_value": tower,
                "direct_minus_J40_tower": tower_residual,
                "status": "PHYSICAL_DIRECT_TOWER_CHECK" if abs(cosine) <= 1.0 else "CROSSED_SHEET_CONTINUATION",
            }
        )
        direct_summary[f"{cosine:.12g}"] = {
            "real": mean.real,
            "imaginary": mean.imag,
            "real_error": real_error,
            "imaginary_error": imaginary_error,
        }

    crossing_rows: list[dict[str, Any]] = []
    crossing_summary: dict[str, dict[str, float]] = {}
    even_residuals: list[float] = []
    crossing_values: dict[float, tuple[complex, float, float]] = {}
    for cosine in physical_cosines:
        t_ratio = -(1.0 - cosine) / 2.0
        u_ratio = -(1.0 + cosine) / 2.0
        z_t = (3.0 + cosine) / (1.0 - cosine)
        z_u = -(3.0 - cosine) / (1.0 + cosine)
        per_seed: list[complex] = []
        for seed_index in range(len(seeds)):
            per_seed.append(
                by_cosine[float(all_cosines[lookup[round(cosine, 12)]])][seed_index]
                + t_ratio**3
                * by_cosine[float(all_cosines[lookup[round(z_t, 12)]])][seed_index]
                + u_ratio**3
                * by_cosine[float(all_cosines[lookup[round(z_u, 12)]])][seed_index]
            )
        mean, real_error, imaginary_error = aggregate_complex(per_seed)
        crossing_values[cosine] = (mean, real_error, imaginary_error)
        crossing_summary[str(cosine)] = {
            "real": mean.real,
            "imaginary": mean.imag,
            "real_error": real_error,
            "imaginary_error": imaginary_error,
        }
        crossing_rows.append(
            {
                "run_id": f"HHCROSS5016_z{cosine:.6g}",
                "physical_s_channel_cosine": cosine,
                "z_t": z_t,
                "z_u": z_u,
                "cyclic_D_hh_over_G3_real": mean.real,
                "cyclic_D_hh_over_G3_imaginary": mean.imag,
                "RQMC_real_error": real_error,
                "RQMC_imaginary_error": imaginary_error,
                "status": "COMPLETED_HH_CYCLIC_FUNCTION",
            }
        )
    for cosine in physical_cosines:
        if -cosine in crossing_values:
            even_residuals.append(
                abs(crossing_values[cosine][0].real - crossing_values[-cosine][0].real)
            )
    return direct_rows, crossing_rows, {
        "all_cosines": all_cosines.tolist(),
        "direct": direct_summary,
        "crossing": crossing_summary,
        "maximum_physical_J40_tower_residual": max(physical_tower_residuals),
        "maximum_crossing_even_residual": max(even_residuals),
        "power": power,
        "samples_per_seed": 2**power,
        "seeds": list(seeds),
    }


def f1_real(scattering_cosine: float) -> float:
    x_value = (1.0 - scattering_cosine) / 2.0
    y_value = 1.0 - x_value
    basis_a = -x_value**3 * math.log(x_value) - y_value**3 * math.log(y_value)
    basis_b = x_value * y_value * (math.log(x_value) + math.log(y_value))
    return 2.0 / math.pi * (23.0 * basis_a / 15.0 - basis_b / 30.0)


def known_master_rows(
    physical_cosines: tuple[float, ...], hh_crossing_rows: list[dict[str, Any]]
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    pph_rows = {
        round(float(row["physical_s_channel_cosine"]), 12): row
        for row in read_csv(PPH_CROSSING)
    }
    hh_rows = {
        round(float(row["physical_s_channel_cosine"]), 12): row
        for row in hh_crossing_rows
    }
    scalar_d0 = 143.0 * (120.0 * math.pi**2 + 1397.0) / (6480.0 * math.pi)
    scalar_d2 = (-621877.0 + 103800.0 * math.pi**2) / (162000.0 * math.pi)
    raw_rows: list[dict[str, Any]] = []
    known_values: list[float] = []
    local_shapes: list[float] = []
    for cosine in physical_cosines:
        key = round(cosine, 12)
        local_shape = 1.0 - cosine * cosine
        scalar_cross = 3.0 * (scalar_d0 - 5.0 * scalar_d2) * local_shape / 4.0
        hh_value = float(hh_rows[key]["cyclic_D_hh_over_G3_real"])
        hh_error = float(hh_rows[key]["RQMC_real_error"])
        pph_value = float(pph_rows[key]["cyclic_D_pph_over_G3_real"])
        pph_error = float(pph_rows[key]["RQMC_real_error"])
        d1_master = 203.0 * f1_real(cosine) / 10.0
        known_master = 2.0 * (scalar_cross + hh_value + pph_value) + d1_master
        known_error = 2.0 * math.sqrt(hh_error * hh_error + pph_error * pph_error)
        known_values.append(known_master)
        local_shapes.append(local_shape)
        raw_rows.append(
            {
                "target_id": f"HHHTARGET5016_z{cosine:.6g}",
                "physical_s_channel_cosine": cosine,
                "scalar_cyclic_D_over_G3": scalar_cross,
                "hh_cyclic_D_over_G3": hh_value,
                "pph_cyclic_D_over_G3": pph_value,
                "minus_D1F1_master_term": d1_master,
                "known_master_without_hhh": known_master,
                "known_master_RQMC_error": known_error,
                "status": "PRE_LOCAL_FIT",
            }
        )
    known_array = np.asarray(known_values)
    shape_array = np.asarray(local_shapes)
    local_coefficient = float(np.dot(shape_array, known_array) / np.dot(shape_array, shape_array))
    residuals = known_array - local_coefficient * shape_array
    for row, shape, residual in zip(raw_rows, local_shapes, residuals):
        row["best_local_shape"] = local_coefficient * shape
        row["known_nonlocal_residual"] = residual
        row["required_hhh_nonlocal_cyclic_D_over_G3"] = -residual / 2.0
        row["status"] = "DERIVED_HHH_NONLOCAL_TARGET_UP_TO_LOCAL_STU_COMPONENT"
    return raw_rows, {
        "best_known_local_coefficient": local_coefficient,
        "maximum_known_nonlocal_residual": float(np.max(np.abs(residuals))),
        "required_hhh_nonlocal_target": {
            str(cosine): float(-residual / 2.0)
            for cosine, residual in zip(physical_cosines, residuals)
        },
        "master_formula": "2(C_phi+C_hh+C_pph+C_hhh)-D1 ReF1",
        "D1_ReF1": "-(203/10)F1, hence master contribution +(203/10)F1",
    }


def gate_rows(
    locks: dict[str, bool], checks: dict[str, Any], run: dict[str, Any], master: dict[str, Any]
) -> list[dict[str, Any]]:
    closed = {
        "primary_source_lock": all(locks.values()),
        "four_point_KLT_normalization": checks["maximum_tree_normalization_residual"] < 2.0e-12,
        "completed_hard_kernel_crossing": checks["maximum_kernel_crossing_residual"] < 2.0e-12,
        "physical_direct_tower_parity_executed": math.isfinite(run["maximum_physical_J40_tower_residual"]),
        "completed_hh_crossed_function": bool(run["crossing"]),
        "known_master_without_hhh_constructed": bool(master["required_hhh_nonlocal_target"]),
        "hhh_nonlocal_target_derived": master["maximum_known_nonlocal_residual"] > 0.0,
    }
    open_gates = {
        "physical_direct_tower_precision": "increase QMC until the direct integral agrees with the exact J<=40 tower plus tail",
        "crossing_even_precision": "increase QMC for the crossed hh function",
        "graph_complete_hhh_crossed_function": "evaluate the five-point KLT hhh plus integral on the same sheets",
        "combined_crossing_locality": "test the hhh result against the derived nonlocal target",
        "numeric_full_K_mu_K_ang": "not yet projected",
        "exact_all_operator_local_GR": "not claimed",
        "full_MTS": "not claimed",
    }
    rows: list[dict[str, Any]] = []
    for gate, passed in closed.items():
        rows.append(
            {
                "gate": gate,
                "passed": bool(passed),
                "evidence": "exact KLT/kernel check or finite multi-seed QMC",
                "status": "PASS" if passed else "FAIL",
            }
        )
    for gate, evidence in open_gates.items():
        rows.append(
            {
                "gate": gate,
                "passed": False,
                "evidence": evidence,
                "status": "OPEN_NONCLAIM",
            }
        )
    return rows


def validation_rows(
    locks: dict[str, bool],
    checks: dict[str, Any],
    direct_rows: list[dict[str, Any]],
    crossing_rows: list[dict[str, Any]],
    master_rows: list[dict[str, Any]],
    gates: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    checks_to_run = [
        ("source_locks", all(locks.values()), str(locks)),
        ("KLT_kernel_checks", checks["all_pass"], str(checks)),
        ("direct_rows_finite", all(math.isfinite(float(row["D_hh_direct_over_G3_real"])) for row in direct_rows), f"rows={len(direct_rows)}"),
        ("crossing_rows_finite", all(math.isfinite(float(row["cyclic_D_hh_over_G3_real"])) for row in crossing_rows), f"rows={len(crossing_rows)}"),
        ("hhh_targets_finite", all(math.isfinite(float(row["required_hhh_nonlocal_cyclic_D_over_G3"])) for row in master_rows), f"rows={len(master_rows)}"),
        ("closed_gates_pass", all(row["passed"] for row in gates if row["status"] != "OPEN_NONCLAIM"), "all closed gates"),
        ("formalization_unchanged", tree_digest(FORMAL) == FORMAL_BASELINE, tree_digest(FORMAL)),
    ]
    return [
        {
            "check_id": f"VALID5016_{index:02d}_{name}",
            "passed": bool(passed),
            "evidence": evidence,
            "status": "PASS" if passed else "FAIL",
        }
        for index, (name, passed, evidence) in enumerate(checks_to_run, start=1)
    ]


def write_provenance(source_hashes: dict[str, str]) -> None:
    lines = [
        "# 5016 completed hh crossing provenance",
        "",
        "This private checkpoint reconstructs the completed 5008 `hh` kernel as a full direct and cyclic function. It derives a nonlocal target for `hhh`; it does not assume that target is satisfied.",
        "",
        "## Sources",
        "",
    ]
    for path, checksum in source_hashes.items():
        lines.append(f"- `{path}` — SHA-256 `{checksum}`")
    lines.extend(
        [
            "",
            "## Claim boundary",
            "",
            "The KLT phase normalization and hard-kernel formula are exact. Direct/crossed values and the resulting `hhh` nonlocal targets carry RQMC errors. No local-GR or full-MTS claim follows until the independent `hhh` calculation closes the coupled locality test.",
        ]
    )
    PROVENANCE.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_document(
    result: dict[str, Any], crossing_rows: list[dict[str, Any]], master_rows: list[dict[str, Any]]
) -> None:
    hh_table = [
        "| z | Re cyclic D_hh/G^3 | RQMC error |",
        "|---:|---:|---:|",
    ]
    for row in crossing_rows:
        hh_table.append(
            f"| {row['physical_s_channel_cosine']:.3g} | {row['cyclic_D_hh_over_G3_real']:.8g} | {row['RQMC_real_error']:.2g} |"
        )
    target_table = [
        "| z | known master without hhh | required hhh nonlocal D/G^3 |",
        "|---:|---:|---:|",
    ]
    for row in master_rows:
        target_table.append(
            f"| {row['physical_s_channel_cosine']:.3g} | {row['known_master_without_hhh']:.8g} | {row['required_hhh_nonlocal_cyclic_D_over_G3']:.8g} |"
        )
    DOCUMENT.write_text(
        f"""# 5016 — completed hh crossed function and hhh nonlocal target

## Result

The exact checkpoint-5008 two-particle tower has now been reconstructed as an angular integral rather than analytically continuing a divergent Legendre series. The sourced four-point KLT tree supplies the spin-four phase, while the completed regular kernel is

```text
K(c)=[H(x)-H_soft(x)]/[x^2(1-x)^2],  x=(1-c)/2.
```

At physical angles the direct integral is checked against the exact `J<=40` tower. The same `z-i0` sheet derived in checkpoint 5015 then gives the crossed values.

{chr(10).join(hh_table)}

## Coupled target

The known real master before `hhh` is now an actual function:

```text
M_known=2(C_phi+C_hh+C_pph)+(203/10)F1.
```

The last sign follows from `D1 ReF1=-(203/10)F1`. Removing the best local `c(1-z^2)` component leaves a nonlocal residual. Since `hhh` enters as `2 C_hhh`, its required nonlocal component is exactly minus one half of that residual on the sampled grid.

{chr(10).join(target_table)}

This is not the rejected checkpoint-5013 mode-by-mode target. It is a crossing-complete functional target, defined only modulo the genuinely local `stu` coefficient.

## Status

- Four-point KLT phase and completed hard kernel: **inserted and checked**.
- Direct `hh` integral versus exact tower: **executed**.
- Crossed `hh` function: **constructed without Legendre continuation**.
- Known master nonlocal residual and `hhh` target: **derived**.
- Independent graph-complete `hhh` crossed calculation: **next active calculation**.
- Combined locality, numeric `K_mu/K_ang`, exact local GR, and full MTS: **not claimed**.

Next: evaluate the graph-complete five-point KLT `hhh` plus distribution at these same direct and crossed angles, and compare its nonlocal component with the target above before fitting any local coefficient.
""",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--power", type=int, default=13)
    parser.add_argument("--seeds", default="1103,2207,3301,4409")
    parser.add_argument("--physical-cosines", default="-0.6,-0.3,0,0.3,0.6")
    arguments = parser.parse_args()
    if arguments.power < 9:
        raise ValueError("power >=9 is required")
    seeds = tuple(int(value) for value in arguments.seeds.split(","))
    physical_cosines = tuple(float(value) for value in arguments.physical_cosines.split(","))
    if len(seeds) < 3 or any(abs(value) >= 0.9 for value in physical_cosines):
        raise ValueError("at least three seeds and |physical cosine|<0.9 are required")

    started = time.perf_counter()
    locks = source_locks()
    check_rows, checks = klt_and_kernel_checks()
    direct_rows, crossing_rows, run = completed_hh_run(
        arguments.power, seeds, physical_cosines
    )
    master_rows, master = known_master_rows(physical_cosines, crossing_rows)
    gates = gate_rows(locks, checks, run, master)
    validation = validation_rows(
        locks, checks, direct_rows, crossing_rows, master_rows, gates
    )

    for path, rows in (
        (KLT_CHECK_CSV, check_rows),
        (DIRECT_CSV, direct_rows),
        (CROSSING_CSV, crossing_rows),
        (MASTER_CSV, master_rows),
        (GATE_CSV, gates),
        (VALIDATION_CSV, validation),
    ):
        write_csv(path, tagged(rows))

    source_paths = (
        CHECKPOINT_4988,
        CHECKPOINT_5008,
        CHECKPOINT_5014,
        CHECKPOINT_5015,
        SCRIPT_5015,
        RESULT_4988,
        RESULT_5005,
        RESULT_5008,
        RESULT_5015,
        HH_TOWER,
        PPH_CROSSING,
    )
    source_hashes = {relative(path): digest(path) for path in source_paths}
    result = {
        "checkpoint_marker": MARKER,
        "source_locks": locks,
        "checks": checks,
        "run": run,
        "known_master": master,
        "completed_hh_crossed_function": True,
        "graph_complete_pph_crossed_function": True,
        "graph_complete_hhh_crossed_function": False,
        "combined_crossing_locality": False,
        "numeric_full_K_mu": False,
        "numeric_full_K_ang": False,
        "exact_all_operator_local_GR": False,
        "full_MTS": False,
        "gates": {row["gate"]: bool(row["passed"]) for row in gates},
        "validation_all_pass": all(row["passed"] for row in validation),
        "formalization_workbench_digest": tree_digest(FORMAL),
        "source_hashes": source_hashes,
        "elapsed_seconds": time.perf_counter() - started,
    }
    SOURCE.mkdir(parents=True, exist_ok=True)
    RESULT_JSON.write_text(json.dumps(result, indent=2, sort_keys=True) + "\n", encoding="utf-8")
    write_provenance(source_hashes)
    write_document(result, crossing_rows, master_rows)
    if not result["validation_all_pass"]:
        failed = [row["check_id"] for row in validation if not row["passed"]]
        raise RuntimeError(f"5016 validation failed: {failed}")
    print(
        json.dumps(
            {
                "status": "PASS",
                "marker": MARKER,
                "hh_crossing": run["crossing"],
                "maximum_physical_J40_tower_residual": run[
                    "maximum_physical_J40_tower_residual"
                ],
                "hhh_nonlocal_target": master["required_hhh_nonlocal_target"],
                "elapsed_seconds": result["elapsed_seconds"],
            },
            indent=2,
        )
    )


if __name__ == "__main__":
    main()
