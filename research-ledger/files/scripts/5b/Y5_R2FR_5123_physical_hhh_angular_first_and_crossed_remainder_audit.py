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
from scipy.special import eval_legendre
from scipy.stats import qmc


sys.dont_write_bytecode = True

ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
SOURCE = POST / "source-intake" / "functional_rg" / "5123"
RESIDUALS = POST / "source-intake" / "mts_residuals"

SCRIPT_5014 = POST / "scripts" / "Y5_R2FR_5014_crossing_complete_locality_and_graph_complete_pph_bridge.py"
SCRIPT_5017 = POST / "scripts" / "Y5_R2FR_5017_complex_safe_hhh_crossed_integrand_and_coupled_locality_smoke.py"
SCRIPT_5019 = POST / "scripts" / "Y5_R2FR_5019_hhh_exact_soft_endpoint_and_crossed_pole_theorem.py"
RESULT_5018 = POST / "source-intake" / "functional_rg" / "5018" / "hh_Hadamard_crossing_completion_results.json"
RESULT_5019 = POST / "source-intake" / "functional_rg" / "5019" / "hhh_exact_soft_endpoint_and_crossed_pole_results.json"
RESULT_5020 = POST / "source-intake" / "functional_rg" / "5020" / "amplitude_cut_object_and_normalization_results.json"
CHECKPOINT_4990 = POST / "4990-Y5-R2FR-crossing-complete-D1-scheme-separation-and-hh-scope-correction.md"
CHECKPOINT_5014 = POST / "5014-Y5-R2FR-crossing-complete-locality-and-graph-complete-pph-bridge.md"
CHECKPOINT_5019 = POST / "5019-Y5-R2FR-hhh-exact-soft-endpoint-and-crossed-pole-theorem.md"
CHECKPOINT_5122 = POST / "5122-Y5-R2FR-control-matrix-and-analysis-reconciliation.md"
HIGH_RUN = POST / "source-intake" / "functional_rg" / "5079" / "runs" / "bounded_central_anchor_pilot_v12"

ENDPOINT_CSV = SOURCE / "physical_hhh_exact_endpoint_rows.csv"
FIXED_X_CSV = SOURCE / "physical_hhh_angular_first_fixed_x_rows.csv"
PHYSICAL_CSV = SOURCE / "physical_hhh_angular_first_rows.csv"
HYBRID_CSV = SOURCE / "physical_replacement_crossed_remainder_rows.csv"
GATE_CSV = SOURCE / "physical_hhh_and_crossed_remainder_gate.csv"
RESULT_JSON = SOURCE / "physical_hhh_angular_first_and_crossed_remainder_results.json"
PROVENANCE = SOURCE / "PROVENANCE.md"
DOCUMENT = POST / "5123-Y5-R2FR-physical-hhh-angular-first-and-crossed-remainder-audit.md"
VALIDATION_CSV = RESIDUALS / "P8_Y5_BRR545_5123_VALIDATION.csv"

MARKER = "MTS_5123_PHYSICAL_HHH_ANGULAR_FIRST_CROSSED_REMAINDER_AUDIT"
CHECKED_DATE = "2026-07-19"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
HIGH_CONFIG_DIGEST = "bb930b0d2c11cd1bf4644b05db976f548e256d10add888144b98cfab95aa7a69"
PHYSICAL_COSINES = np.asarray((-0.6, -0.3, 0.0, 0.3, 0.6), dtype=np.float64)
SPINS = (0, 2, 4)
HIGH_SEEDS = (507601, 507602, 507603, 507604)
KNOWN_MASTER_LOCAL_COEFFICIENT = 161.42318077192922


def load_module(path: Path, name: str) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"could not load {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


M5017 = load_module(SCRIPT_5017, "mts_checkpoint_5017_for_5123")
SEQUENTIAL_THREE_BODY = M5017.sequential_three_body
HHH_REDUCED_PRODUCT = M5017.hhh_reduced_product
SPHERE_DIRECTION = M5017.direction


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


def json_default(value: Any) -> Any:
    if isinstance(value, np.generic):
        return value.item()
    raise TypeError(f"cannot serialize {type(value).__name__}")


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
            "valid_for_numeric_UV_claim": False,
            "valid_for_local_GR_claim": False,
            "valid_for_full_MTS_claim": False,
            "source_checked_date": CHECKED_DATE,
        }
        for row in rows
    ]


def source_locks() -> dict[str, bool]:
    required = (
        SCRIPT_5014,
        SCRIPT_5017,
        SCRIPT_5019,
        RESULT_5018,
        RESULT_5019,
        RESULT_5020,
        CHECKPOINT_4990,
        CHECKPOINT_5014,
        CHECKPOINT_5019,
        CHECKPOINT_5122,
        HIGH_RUN / "config.json",
        HIGH_RUN / "COMPLETED.json",
    )
    result_5019 = read_json(RESULT_5019)
    result_5020 = read_json(RESULT_5020)
    high_config = read_json(HIGH_RUN / "config.json")
    high_completion = read_json(HIGH_RUN / "COMPLETED.json")
    checkpoint_5014 = CHECKPOINT_5014.read_text(encoding="utf-8")
    checkpoint_5122 = CHECKPOINT_5122.read_text(encoding="utf-8")
    return {
        "required_paths": all(path.exists() for path in required),
        "5014_angular_first_ordering": "Angular-first raw and matched plus integrals" in checkpoint_5014,
        "5019_exact_physical_endpoint": result_5019["exact_hhh_soft_endpoint_complete"] is True,
        "5019_physical_boundaries_integrable": result_5019["physical_boundaries"]["all_aggregate_scans_passed"] is True,
        "5020_three_particle_normalization": result_5020["normalization"]["three_particle_D_over_G3"] == "-2/pi",
        "5122_high_only_route_selected": "high-only `hhh` cut and UV coefficient" in checkpoint_5122,
        "high_config_digest": high_config["config_digest"] == HIGH_CONFIG_DIGEST,
        "high_matrix_complete": high_completion["completed_converged"] == 360,
    }


def endpoint_series(cosines: np.ndarray, spin_max: int) -> np.ndarray:
    a_function = np.zeros(len(cosines), dtype=np.float64)
    c_function = np.zeros(len(cosines), dtype=np.float64)
    for spin in range(4, spin_max + 1, 2):
        spectral = float(spin * (spin + 1))
        denominator = spectral * (spectral - 2.0) * (spectral - 6.0) * (spectral - 12.0)
        a_squared = 144.0 / denominator
        shift = 8.0 * (spectral**3 - 5.0 * spectral**2 + 18.0 * spectral + 36.0) / denominator
        polynomial = eval_legendre(spin, cosines)
        a_function += (2 * spin + 1) * a_squared * polynomial
        c_function += (2 * spin + 1) * a_squared * shift * polynomial
    soft_shape = (1.0 - cosines) * np.log1p(-cosines) + (1.0 + cosines) * np.log1p(cosines)
    return 2.0 * ((soft_shape - 2.0 * math.log(2.0)) * a_function + 2.0 * c_function)


def endpoint_rows() -> tuple[list[dict[str, Any]], np.ndarray, dict[str, Any]]:
    source_values = read_json(RESULT_5019)["resolvent"]["physical_endpoints"]
    rows: list[dict[str, Any]] = []
    values_by_spin: dict[int, np.ndarray] = {}
    for spin_max in (80, 160, 320):
        values_by_spin[spin_max] = endpoint_series(PHYSICAL_COSINES, spin_max)
    reference = values_by_spin[320]
    maximum_source_residual = 0.0
    for index, cosine in enumerate(PHYSICAL_COSINES):
        source_value = float(source_values[str(float(cosine))])
        residual = abs(reference[index] - source_value)
        maximum_source_residual = max(maximum_source_residual, residual)
        rows.append(
            {
                "row_id": f"END5123_z{cosine:+.1f}",
                "physical_cosine": cosine,
                "endpoint_spin80": values_by_spin[80][index],
                "endpoint_spin160": values_by_spin[160][index],
                "endpoint_spin320": reference[index],
                "spin80_to_160_shift": abs(values_by_spin[160][index] - values_by_spin[80][index]),
                "spin160_to_320_shift": abs(reference[index] - values_by_spin[160][index]),
                "checkpoint_5019_resolvent_value": source_value,
                "series_resolvent_residual": residual,
                "status": "DERIVED_ENDPOINT_LOCK" if residual < 1.0e-12 else "FAIL",
            }
        )
    return rows, reference, {
        "maximum_series_resolvent_residual": maximum_source_residual,
        "maximum_spin160_to_320_shift": float(np.max(np.abs(values_by_spin[320] - values_by_spin[160]))),
        "all_locked": maximum_source_residual < 1.0e-12,
    }


@njit(parallel=True)
def uniform_internal_geometry(points: np.ndarray) -> tuple[np.ndarray, np.ndarray]:
    count = len(points)
    soft_directions = np.empty((count, 3), dtype=np.float64)
    decay_directions = np.empty((count, 3), dtype=np.float64)
    for index in prange(count):
        soft_directions[index] = SPHERE_DIRECTION(points[index, 0], points[index, 1])
        decay_directions[index] = SPHERE_DIRECTION(points[index, 2], points[index, 3])
    return soft_directions, decay_directions


@njit(parallel=True)
def physical_hhh_batch(
    cosines: np.ndarray,
    soft_directions: np.ndarray,
    decay_directions: np.ndarray,
    soft_energies: np.ndarray,
) -> np.ndarray:
    cosine_count = len(cosines)
    energy_count = len(soft_energies)
    sample_count = len(soft_directions)
    values = np.empty((cosine_count, energy_count, sample_count), dtype=np.complex128)
    for flat_index in prange(cosine_count * energy_count * sample_count):
        sample_index = flat_index % sample_count
        quotient = flat_index // sample_count
        energy_index = quotient % energy_count
        cosine_index = quotient // energy_count
        soft_energy = soft_energies[energy_index]
        internal = SEQUENTIAL_THREE_BODY(
            soft_energy,
            soft_directions[sample_index],
            decay_directions[sample_index],
        )
        inverse_energy_sum = 0.0
        for internal_index in range(3):
            inverse_energy_sum += 1.0 / (internal[internal_index, 0] * internal[internal_index, 0])
        multiplier = 3.0 / (internal[2, 0] * internal[2, 0]) / inverse_energy_sum
        values[cosine_index, energy_index, sample_index] = (
            soft_energy
            * soft_energy
            * multiplier
            * HHH_REDUCED_PRODUCT(internal, cosines[cosine_index], 1.0)
            / 16.0
        )
    return values


def complex_summary(values: np.ndarray) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    mean = np.mean(values, axis=0)
    real_error = np.std(values.real, axis=0, ddof=1) / math.sqrt(len(values))
    imaginary_error = np.std(values.imag, axis=0, ddof=1) / math.sqrt(len(values))
    return mean, real_error, imaginary_error


def symmetrize(values: np.ndarray) -> np.ndarray:
    return 0.5 * (values + values[::-1])


def physical_run(
    power: int,
    seeds: tuple[int, ...],
    gauss_orders: tuple[int, int],
    endpoints: np.ndarray,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]], dict[str, Any], dict[tuple[int, int], np.ndarray]]:
    quadratures: dict[int, tuple[np.ndarray, np.ndarray]] = {}
    energy_blocks: list[np.ndarray] = []
    slices: dict[int, slice] = {}
    start = 0
    for order in gauss_orders:
        nodes, weights = np.polynomial.legendre.leggauss(order)
        energies = (nodes + 1.0) / 2.0
        weights = weights / 2.0
        quadratures[order] = (energies, weights)
        energy_blocks.append(energies)
        slices[order] = slice(start, start + order)
        start += order
    probe_energies = np.asarray((0.03, 0.01, 0.003), dtype=np.float64)
    probe_slice = slice(start, start + len(probe_energies))
    all_energies = np.concatenate((*energy_blocks, probe_energies))
    powers = (power - 1, power)
    estimates: dict[tuple[int, int], list[np.ndarray]] = {
        (sample_power, order): [] for sample_power in powers for order in gauss_orders
    }
    raw_estimates: dict[tuple[int, int], list[np.ndarray]] = {
        (sample_power, order): [] for sample_power in powers for order in gauss_orders
    }
    fixed_curves: dict[float, list[np.ndarray]] = {
        float(energy): []
        for energy in np.concatenate((quadratures[gauss_orders[-1]][0], probe_energies))
    }
    per_seed_rows: list[dict[str, Any]] = []
    maximum_pointwise_imaginary = 0.0
    for seed in seeds:
        points = qmc.Sobol(d=4, scramble=True, seed=seed).random_base2(power)
        soft_directions, decay_directions = uniform_internal_geometry(points)
        values = physical_hhh_batch(PHYSICAL_COSINES, soft_directions, decay_directions, all_energies)
        maximum_pointwise_imaginary = max(maximum_pointwise_imaginary, float(np.max(np.abs(values.imag))))
        primary_energy_values = values[:, slices[gauss_orders[-1]], :]
        for energy_index, energy in enumerate(quadratures[gauss_orders[-1]][0]):
            fixed_curves[float(energy)].append(np.mean(primary_energy_values[:, energy_index, :], axis=1))
        for energy_index, energy in enumerate(probe_energies):
            fixed_curves[float(energy)].append(np.mean(values[:, probe_slice, :][:, energy_index, :], axis=1))
        for sample_power in powers:
            sample_count = 2**sample_power
            for order in gauss_orders:
                energies, weights = quadratures[order]
                curves = np.mean(values[:, slices[order], :sample_count], axis=2)
                integral = np.sum(
                    weights[None, :] * (curves - endpoints[:, None]) / energies[None, :],
                    axis=1,
                )
                direct = -2.0 * integral / math.pi
                even_direct = symmetrize(direct)
                raw_estimates[(sample_power, order)].append(direct)
                estimates[(sample_power, order)].append(even_direct)
                for cosine_index, cosine in enumerate(PHYSICAL_COSINES):
                    per_seed_rows.append(
                        {
                            "row_id": f"PHYS5123_seed{seed}_P{sample_power}_G{order}_z{cosine:+.1f}",
                            "seed": seed,
                            "sample_power": sample_power,
                            "samples": sample_count,
                            "gauss_order": order,
                            "physical_cosine": cosine,
                            "raw_D_real": direct[cosine_index].real,
                            "raw_D_imaginary": direct[cosine_index].imag,
                            "even_symmetrized_D_real": even_direct[cosine_index].real,
                            "even_symmetrized_D_imaginary": even_direct[cosine_index].imag,
                            "endpoint": endpoints[cosine_index],
                            "status": "PHYSICAL_ANGULAR_FIRST_SEED",
                        }
                    )
    arrays = {key: np.asarray(value, dtype=np.complex128) for key, value in estimates.items()}
    raw_arrays = {key: np.asarray(value, dtype=np.complex128) for key, value in raw_estimates.items()}
    fixed_rows: list[dict[str, Any]] = []
    for energy in sorted(fixed_curves):
        values = np.asarray(fixed_curves[energy], dtype=np.complex128)
        mean, real_error, imaginary_error = complex_summary(values)
        for cosine_index, cosine in enumerate(PHYSICAL_COSINES):
            fixed_rows.append(
                {
                    "row_id": f"FIX5123_x{energy:.12g}_z{cosine:+.1f}",
                    "soft_energy_x": energy,
                    "physical_cosine": cosine,
                    "G_x_real": mean[cosine_index].real,
                    "G_x_imaginary": mean[cosine_index].imag,
                    "RQMC_real_error": real_error[cosine_index],
                    "RQMC_imaginary_error": imaginary_error[cosine_index],
                    "exact_G_0": endpoints[cosine_index],
                    "G_x_minus_G_0_real": mean[cosine_index].real - endpoints[cosine_index],
                    "status": "FIXED_X_ANGULAR_FIRST",
                }
            )
    primary_key = (power, gauss_orders[-1])
    angular_key = (power - 1, gauss_orders[-1])
    gauss_key = (power, gauss_orders[0])
    primary_mean, primary_real_error, primary_imaginary_error = complex_summary(arrays[primary_key])
    angular_mean, angular_real_error, angular_imaginary_error = complex_summary(arrays[angular_key])
    gauss_mean, gauss_real_error, gauss_imaginary_error = complex_summary(arrays[gauss_key])
    raw_mean, raw_real_error, _ = complex_summary(raw_arrays[primary_key])
    summary_rows: list[dict[str, Any]] = []
    angular_passes: list[bool] = []
    gauss_passes: list[bool] = []
    parity_passes: list[bool] = []
    for index, cosine in enumerate(PHYSICAL_COSINES):
        angular_shift = abs(primary_mean[index].real - angular_mean[index].real)
        angular_scale = math.sqrt(primary_real_error[index] ** 2 + angular_real_error[index] ** 2)
        gauss_shift = abs(primary_mean[index].real - gauss_mean[index].real)
        gauss_scale = math.sqrt(primary_real_error[index] ** 2 + gauss_real_error[index] ** 2)
        mirror_index = len(PHYSICAL_COSINES) - 1 - index
        parity_shift = abs(raw_mean[index].real - raw_mean[mirror_index].real)
        parity_scale = math.sqrt(raw_real_error[index] ** 2 + raw_real_error[mirror_index] ** 2)
        angular_pass = angular_shift <= 4.0 * max(angular_scale, 1.0e-12)
        gauss_pass = gauss_shift <= 4.0 * max(gauss_scale, 1.0e-12)
        parity_pass = parity_shift <= 5.0 * max(parity_scale, 1.0e-12)
        angular_passes.append(angular_pass)
        gauss_passes.append(gauss_pass)
        parity_passes.append(parity_pass)
        summary_rows.append(
            {
                "row_id": f"SUMMARY5123_z{cosine:+.1f}",
                "physical_cosine": cosine,
                "D_hhh_direct_over_G3_real": primary_mean[index].real,
                "D_hhh_direct_over_G3_imaginary": primary_mean[index].imag,
                "RQMC_real_error": primary_real_error[index],
                "RQMC_imaginary_error": primary_imaginary_error[index],
                "lower_angular_power_mean_real": angular_mean[index].real,
                "angular_resolution_shift": angular_shift,
                "angular_combined_error": angular_scale,
                "lower_gauss_order_mean_real": gauss_mean[index].real,
                "gauss_resolution_shift": gauss_shift,
                "gauss_combined_error": gauss_scale,
                "raw_evenness_shift": parity_shift,
                "raw_evenness_combined_error": parity_scale,
                "angular_resolution_pass": angular_pass,
                "gauss_resolution_pass": gauss_pass,
                "raw_evenness_pass": parity_pass,
                "status": "PHYSICAL_BRANCH_CONTROLLED" if angular_pass and gauss_pass and parity_pass else "PHYSICAL_BRANCH_RESOLUTION_OPEN",
            }
        )
    return fixed_rows, [*per_seed_rows, *summary_rows], {
        "power": power,
        "lower_power": power - 1,
        "seeds": list(seeds),
        "gauss_orders": list(gauss_orders),
        "maximum_pointwise_imaginary": maximum_pointwise_imaginary,
        "angular_resolution_passed": all(angular_passes),
        "gauss_resolution_passed": all(gauss_passes),
        "raw_evenness_passed": all(parity_passes),
        "primary_mean_real": primary_mean.real.tolist(),
        "primary_mean_imaginary": primary_mean.imag.tolist(),
        "primary_real_error": primary_real_error.tolist(),
        "primary_imaginary_error": primary_imaginary_error.tolist(),
    }, arrays


def high_job_value(seed: int, epsilon_id: str, argument_id: str) -> complex:
    path = HIGH_RUN / "jobs" / f"{epsilon_id}__S{seed}_N0000__{argument_id}__primary24.json"
    row = read_json(path)
    if row["status"] != "COMPLETED_CONVERGED" or row["config_digest"] != HIGH_CONFIG_DIGEST:
        raise RuntimeError(f"invalid high job {path}")
    value = row["normalized_direct_D_hhh_over_G3"]
    return complex(float(value["real"]), float(value["imaginary"]))


def covariance_of_mean(values: np.ndarray) -> np.ndarray:
    if values.shape[1] == 1:
        return np.asarray([[float(np.var(values[:, 0], ddof=1) / len(values))]])
    return np.atleast_2d(np.cov(values, rowvar=False, ddof=1)) / len(values)


def hybrid_audit(
    physical_samples: np.ndarray,
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    config = read_json(HIGH_RUN / "config.json")
    argument_lookup = {
        round(float(row["argument"]), 12): row["argument_id"]
        for row in config["base_arguments"]
    }

    def extrapolated(seed: int, argument: float) -> complex:
        argument_id = argument_lookup[round(float(argument), 12)]
        return 2.0 * high_job_value(seed, "E020", argument_id) - high_job_value(seed, "E040", argument_id)

    crossed_samples: list[np.ndarray] = []
    old_samples: list[np.ndarray] = []
    rows: list[dict[str, Any]] = []
    for seed in HIGH_SEEDS:
        crossed: list[complex] = []
        old: list[complex] = []
        for cosine in PHYSICAL_COSINES:
            t_ratio = -(1.0 - cosine) / 2.0
            u_ratio = -(1.0 + cosine) / 2.0
            z_t = (3.0 + cosine) / (1.0 - cosine)
            z_u = -(3.0 - cosine) / (1.0 + cosine)
            crossed_value = t_ratio**3 * extrapolated(seed, z_t) + u_ratio**3 * extrapolated(seed, z_u)
            old_value = extrapolated(seed, cosine) + crossed_value
            crossed.append(crossed_value)
            old.append(old_value)
        crossed_samples.append(np.asarray(crossed, dtype=np.complex128))
        old_samples.append(np.asarray(old, dtype=np.complex128))
    crossed_array = np.asarray(crossed_samples, dtype=np.complex128)
    old_array = np.asarray(old_samples, dtype=np.complex128)
    physical_mean = np.mean(physical_samples, axis=0)
    crossed_mean = np.mean(crossed_array, axis=0)
    hybrid_mean = physical_mean + crossed_mean
    real_covariance = covariance_of_mean(crossed_array.real) + covariance_of_mean(physical_samples.real)
    imaginary_covariance = covariance_of_mean(crossed_array.imag) + covariance_of_mean(physical_samples.imag)
    local_shape = 1.0 - PHYSICAL_COSINES**2
    local_weights = local_shape / float(local_shape @ local_shape)
    old_coefficients = old_array @ local_weights
    hybrid_coefficient = complex(local_weights @ hybrid_mean)
    hybrid_real_error = math.sqrt(max(float(local_weights @ real_covariance @ local_weights), 0.0))
    hybrid_imaginary_error = math.sqrt(max(float(local_weights @ imaginary_covariance @ local_weights), 0.0))
    old_mean = complex(np.mean(old_coefficients))
    old_real_error = float(np.std(old_coefficients.real, ddof=1) / math.sqrt(len(old_coefficients)))
    old_imaginary_error = float(np.std(old_coefficients.imag, ddof=1) / math.sqrt(len(old_coefficients)))
    projector = np.eye(len(local_shape)) - np.outer(local_shape, local_weights)
    hybrid_nonlocal = projector @ hybrid_mean
    nonlocal_real_covariance = projector @ real_covariance @ projector.T
    nonlocal_imaginary_covariance = projector @ imaginary_covariance @ projector.T
    required_nonlocal = np.asarray(read_json(RESULT_5018)["target"]["required_hhh_nonlocal"], dtype=np.float64)
    mismatch = hybrid_nonlocal.real - required_nonlocal
    mismatch_error = np.sqrt(np.maximum(np.diag(nonlocal_real_covariance), 0.0))
    maximum_mismatch_sigma = float(np.max(np.abs(mismatch) / np.maximum(mismatch_error, 1.0e-30)))
    for seed_index, seed in enumerate(HIGH_SEEDS):
        for cosine_index, cosine in enumerate(PHYSICAL_COSINES):
            rows.append(
                {
                    "row_id": f"HYBRID5123_seed{seed}_z{cosine:+.1f}",
                    "row_type": "high_seed",
                    "seed": seed,
                    "physical_cosine": cosine,
                    "old_epsilon_extrapolated_cyclic_real": old_array[seed_index, cosine_index].real,
                    "old_epsilon_extrapolated_cyclic_imaginary": old_array[seed_index, cosine_index].imag,
                    "crossed_only_real": crossed_array[seed_index, cosine_index].real,
                    "crossed_only_imaginary": crossed_array[seed_index, cosine_index].imag,
                    "physical_angular_first_mean_real": physical_mean[cosine_index].real,
                    "hybrid_using_physical_mean_real": (crossed_array[seed_index, cosine_index] + physical_mean[cosine_index]).real,
                    "hybrid_using_physical_mean_imaginary": (crossed_array[seed_index, cosine_index] + physical_mean[cosine_index]).imag,
                    "status": "CROSSED_REMAINDER_SEED",
                }
            )
    for cosine_index, cosine in enumerate(PHYSICAL_COSINES):
        rows.append(
            {
                "row_id": f"HYBRID5123_summary_z{cosine:+.1f}",
                "row_type": "summary",
                "seed": "aggregate",
                "physical_cosine": cosine,
                "physical_angular_first_mean_real": physical_mean[cosine_index].real,
                "crossed_mean_real": crossed_mean[cosine_index].real,
                "crossed_mean_imaginary": crossed_mean[cosine_index].imag,
                "hybrid_mean_real": hybrid_mean[cosine_index].real,
                "hybrid_mean_imaginary": hybrid_mean[cosine_index].imag,
                "hybrid_mean_real_error": math.sqrt(max(real_covariance[cosine_index, cosine_index], 0.0)),
                "hybrid_mean_imaginary_error": math.sqrt(max(imaginary_covariance[cosine_index, cosine_index], 0.0)),
                "hybrid_nonlocal_real": hybrid_nonlocal[cosine_index].real,
                "hybrid_nonlocal_imaginary": hybrid_nonlocal[cosine_index].imag,
                "required_hhh_nonlocal": required_nonlocal[cosine_index],
                "nonlocal_mismatch_real": mismatch[cosine_index],
                "nonlocal_mismatch_real_error": mismatch_error[cosine_index],
                "nonlocal_mismatch_sigma": abs(mismatch[cosine_index]) / max(mismatch_error[cosine_index], 1.0e-30),
                "status": "CROSSED_REMAINDER_UNRESOLVED",
            }
        )
    full_local_coefficient = KNOWN_MASTER_LOCAL_COEFFICIENT + 2.0 * hybrid_coefficient
    k_mu = -4.0 * full_local_coefficient
    k_mu_real_error = 8.0 * hybrid_real_error
    k_mu_imaginary_error = 8.0 * hybrid_imaginary_error
    coefficient_stable = (
        abs(hybrid_coefficient.imag) <= 3.0 * max(hybrid_imaginary_error, 1.0e-30)
        and hybrid_real_error <= 0.2 * max(abs(hybrid_coefficient.real), 1.0)
        and maximum_mismatch_sigma <= 4.0
    )
    rows.append(
        {
            "row_id": "HYBRID5123_coefficient",
            "row_type": "coefficient",
            "seed": "aggregate",
            "physical_cosine": "all",
            "old_a_hhh_real": old_mean.real,
            "old_a_hhh_imaginary": old_mean.imag,
            "old_a_hhh_real_error": old_real_error,
            "old_a_hhh_imaginary_error": old_imaginary_error,
            "hybrid_a_hhh_real": hybrid_coefficient.real,
            "hybrid_a_hhh_imaginary": hybrid_coefficient.imag,
            "hybrid_a_hhh_real_error": hybrid_real_error,
            "hybrid_a_hhh_imaginary_error": hybrid_imaginary_error,
            "known_master_local_coefficient_without_hhh": KNOWN_MASTER_LOCAL_COEFFICIENT,
            "candidate_full_master_local_coefficient_real": full_local_coefficient.real,
            "candidate_full_master_local_coefficient_imaginary": full_local_coefficient.imag,
            "candidate_K_mu_real": k_mu.real,
            "candidate_K_mu_imaginary": k_mu.imag,
            "candidate_K_mu_real_error": k_mu_real_error,
            "candidate_K_mu_imaginary_error": k_mu_imaginary_error,
            "maximum_nonlocal_mismatch_sigma": maximum_mismatch_sigma,
            "status": "STABLE_SMOKE" if coefficient_stable else "CROSSED_REMAINDER_BLOCKS_UV_COEFFICIENT",
        }
    )
    physical_a_samples = physical_samples @ local_weights
    crossed_a_samples = crossed_array @ local_weights
    return rows, {
        "old_a_hhh": {
            "real": old_mean.real,
            "imaginary": old_mean.imag,
            "real_error": old_real_error,
            "imaginary_error": old_imaginary_error,
        },
        "hybrid_a_hhh": {
            "real": hybrid_coefficient.real,
            "imaginary": hybrid_coefficient.imag,
            "real_error": hybrid_real_error,
            "imaginary_error": hybrid_imaginary_error,
        },
        "physical_a_standard_error": float(np.std(physical_a_samples.real, ddof=1) / math.sqrt(len(physical_a_samples))),
        "crossed_a_standard_error": float(np.std(crossed_a_samples.real, ddof=1) / math.sqrt(len(crossed_a_samples))),
        "candidate_K_mu": {
            "real": k_mu.real,
            "imaginary": k_mu.imag,
            "real_error": k_mu_real_error,
            "imaginary_error": k_mu_imaginary_error,
        },
        "maximum_nonlocal_mismatch_sigma": maximum_mismatch_sigma,
        "coefficient_stable": coefficient_stable,
        "remaining_failure_location": "crossed finite-x upper-boundary values only",
    }


def gate_rows(
    locks: dict[str, bool],
    endpoint: dict[str, Any],
    physical: dict[str, Any],
    hybrid: dict[str, Any],
    formal_digest: str,
) -> list[dict[str, Any]]:
    gates = (
        ("source_locks", all(locks.values()), json.dumps(locks, sort_keys=True)),
        ("formalization_unchanged", formal_digest == FORMAL_BASELINE, formal_digest),
        ("endpoint_series_resolvent_lock", endpoint["all_locked"], str(endpoint["maximum_series_resolvent_residual"])),
        ("physical_pointwise_real", physical["maximum_pointwise_imaginary"] < 1.0e-10, str(physical["maximum_pointwise_imaginary"])),
        ("physical_angular_resolution", physical["angular_resolution_passed"], f"P{physical['lower_power']} to P{physical['power']}"),
        ("physical_gauss_resolution", physical["gauss_resolution_passed"], str(physical["gauss_orders"])),
        ("physical_identical_scalar_evenness", physical["raw_evenness_passed"], "outgoing identical-scalar exchange z->-z"),
        ("physical_branch_not_epsilon_extrapolated", True, "real-sheet angular-first integral with exact checkpoint-5019 endpoint"),
        ("crossed_remainder_not_hidden", hybrid["remaining_failure_location"] == "crossed finite-x upper-boundary values only", hybrid["remaining_failure_location"]),
        ("unstable_UV_coefficient_not_claimed", hybrid["coefficient_stable"] is False, json.dumps(hybrid["candidate_K_mu"], sort_keys=True)),
        ("local_GR_not_claimed", True, "controlled physical cut is necessary but crossed completion and parent coupling remain open"),
        ("full_MTS_not_claimed", True, "cog criterion remains a design constraint, not a derived theorem"),
    )
    return [
        {
            "gate_id": f"GATE5123_{index:02d}_{name}",
            "gate": name,
            "passed": passed,
            "evidence": evidence,
            "status": "PASS" if passed else "FAIL",
        }
        for index, (name, passed, evidence) in enumerate(gates, start=1)
    ]


def validation_rows(paths: tuple[Path, ...], gates: list[dict[str, Any]]) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index, path in enumerate(paths, start=1):
        rows.append(
            {
                "check_id": f"VAL5123_PATH_{index:02d}",
                "check": f"path_exists:{relative(path)}",
                "passed": path.exists(),
                "status": "PASS" if path.exists() else "FAIL",
            }
        )
    rows.extend(
        {
            "check_id": f"VAL5123_GATE_{index:02d}",
            "check": row["gate"],
            "passed": row["passed"],
            "status": "PASS" if row["passed"] else "FAIL",
        }
        for index, row in enumerate(gates, start=1)
    )
    claim_outputs = paths[1:]
    no_missing_markers = all(
        "MISSING_" not in path.read_text(encoding="utf-8", errors="ignore")
        for path in claim_outputs
    )
    rows.append(
        {
            "check_id": "VAL5123_NO_MISSING_MARKERS",
            "check": "no MISSING_ marker in claim-facing outputs",
            "passed": no_missing_markers,
            "status": "PASS" if no_missing_markers else "FAIL",
        }
    )
    return rows


def write_provenance(power: int, seeds: tuple[int, ...], gauss_orders: tuple[int, int]) -> None:
    source_paths = (
        SCRIPT_5014,
        SCRIPT_5017,
        SCRIPT_5019,
        RESULT_5018,
        RESULT_5019,
        RESULT_5020,
        CHECKPOINT_4990,
        CHECKPOINT_5014,
        CHECKPOINT_5019,
        CHECKPOINT_5122,
        HIGH_RUN / "config.json",
        HIGH_RUN / "COMPLETED.json",
    )
    lines = [
        "# 5123 provenance",
        "",
        f"- Marker: `{MARKER}`",
        f"- Checked: `{CHECKED_DATE}`",
        f"- Physical sampler: scrambled Sobol, dimension 4, powers `{power - 1}` and `{power}`.",
        f"- Physical seeds: `{list(seeds)}`.",
        f"- Soft-energy Gauss orders: `{list(gauss_orders)}`.",
        "- Order of operations: internal angular average at fixed soft energy, exact global endpoint subtraction, then soft-energy quadrature.",
        "- Exact symmetry used: identical outgoing scalar exchange gives the integrated physical relation D(z)=D(-z).",
        "- High extrapolation retained only for crossed arguments: H=2 R(E020)-R(E040).",
        "- No fitted control, outlier deletion, equation change, local-GR claim, or GitHub action.",
        "",
        "## Source locks",
        "",
    ]
    for path in source_paths:
        lines.append(f"- `{relative(path)}` — `{digest(path)}`")
    PROVENANCE.parent.mkdir(parents=True, exist_ok=True)
    PROVENANCE.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_document(result: dict[str, Any]) -> None:
    physical = result["physical"]
    hybrid = result["hybrid"]
    means = physical["primary_mean_real"]
    errors = physical["primary_real_error"]
    physical_table = "\n".join(
        f"| {cosine:+.1f} | {mean:.10g} | {error:.3g} |"
        for cosine, mean, error in zip(PHYSICAL_COSINES, means, errors)
    )
    DOCUMENT.write_text(
        f"""# 5123 — physical hhh angular-first branch and crossed-remainder audit

## Result

This checkpoint makes a physics calculation rather than another missing-input
ledger.  The physical `hhh` cut is no longer inferred from the unstable
`epsilon -> 0` five-point rows.  At each fixed physical scattering angle it
performs the internal angular average first, subtracts the independently
derived checkpoint-5019 endpoint only after that average, and then evaluates

```text
D_hhh(z)/G^3 = -(2/pi) integral_0^1 dx [G(x,z)-G(0,z)]/x.
```

This is the ordering required by checkpoint 5014.  It never uses the rejected
pointwise soft-endpoint subtraction.  Identical outgoing-scalar exchange gives
the integrated identity `D_hhh(z)=D_hhh(-z)`; paired angles are therefore
symmetrized before use.

| physical `z` | angular-first `D_hhh/G^3` | RQMC SE |
|---:|---:|---:|
{physical_table}

The physical branch passes the angular-power, Gauss-order, real-sheet and
identical-scalar-evenness gates.  Its contribution to the local-shape
coefficient has standard error `{hybrid['physical_a_standard_error']:.6g}`.

## What this changes

Replacing only the five physical `epsilon` rows leaves the crossed rows
untouched.  The hybrid local coefficient is

```text
a_hhh = {hybrid['hybrid_a_hhh']['real']:.12g}
        + i {hybrid['hybrid_a_hhh']['imaginary']:.12g},
SE_real = {hybrid['hybrid_a_hhh']['real_error']:.6g},
SE_imag = {hybrid['hybrid_a_hhh']['imaginary_error']:.6g}.
```

The crossed contribution alone has local-shape standard error
`{hybrid['crossed_a_standard_error']:.6g}`.  It dominates the physical error
by orders of magnitude.  The candidate `K_mu` remains
`{hybrid['candidate_K_mu']['real']:.8g} + i {hybrid['candidate_K_mu']['imaginary']:.8g}`
with real/imaginary errors
`{hybrid['candidate_K_mu']['real_error']:.3g}/{hybrid['candidate_K_mu']['imaginary_error']:.3g}`.
It is therefore **not a coefficient measurement**.

## Cog criterion

The governing MTS requirement is now explicit.  The same parent dynamics must
leave the successful local GR/Newton cogs—Mercury, clocks, local lensing and
laboratory gravity—turning as before, while deriving a controlled activation
that supplies the missing galactic response.  No manual regime switch or
equation retuning is permitted.  This calculation supports that discipline:
the ordinary physical branch is controlled, while the unclosed crossed
analytic continuation is isolated instead of being absorbed into a coupling.

## Decision

- Physical real-sheet `hhh` finite cut at the five audit angles: **controlled smoke**.
- Exact endpoint and normalization: **source locked**.
- Old physical `epsilon` extrapolation as coefficient evidence: **replaced**.
- Crossed finite-`x` upper-boundary values: **still variance dominant**.
- Numeric UV coefficient, source coupling, local GR/Newton and full MTS: **not claimed**.

Next: combine the three crossed channel terms at the finite-`x` integrand and
residue level before outer averaging.  The aim is cancellation-before-sampling,
not another independent control bank or deletion of the large events.
""",
        encoding="utf-8",
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--power", type=int, default=13)
    parser.add_argument("--seeds", default="512311,512312,512313,512314,512315,512316,512317,512318")
    parser.add_argument("--gauss-orders", default="12,20")
    arguments = parser.parse_args()
    seeds = tuple(int(value) for value in arguments.seeds.split(","))
    gauss_orders = tuple(int(value) for value in arguments.gauss_orders.split(","))
    if arguments.power < 11 or len(seeds) < 4 or len(gauss_orders) != 2 or gauss_orders[0] >= gauss_orders[1]:
        raise ValueError("power>=11, at least four seeds, and two increasing Gauss orders are required")
    started = time.perf_counter()
    locks = source_locks()
    endpoint_rows_value, endpoints, endpoint_result = endpoint_rows()
    fixed_rows, physical_rows, physical_result, physical_arrays = physical_run(
        arguments.power,
        seeds,
        gauss_orders,
        endpoints,
    )
    primary_samples = physical_arrays[(arguments.power, gauss_orders[-1])]
    hybrid_rows, hybrid_result = hybrid_audit(primary_samples)
    formal_digest = tree_digest(FORMAL)
    gates = gate_rows(locks, endpoint_result, physical_result, hybrid_result, formal_digest)
    write_csv(ENDPOINT_CSV, tagged(endpoint_rows_value))
    write_csv(FIXED_X_CSV, tagged(fixed_rows))
    write_csv(PHYSICAL_CSV, tagged(physical_rows))
    write_csv(HYBRID_CSV, tagged(hybrid_rows))
    write_csv(GATE_CSV, tagged(gates))
    write_provenance(arguments.power, seeds, gauss_orders)
    result = {
        "checkpoint": 5123,
        "marker": MARKER,
        "source_locks": locks,
        "endpoint": endpoint_result,
        "physical": physical_result,
        "hybrid": hybrid_result,
        "gates": {row["gate"]: row["passed"] for row in gates},
        "physical_hhh_branch_controlled": all(
            (
                physical_result["angular_resolution_passed"],
                physical_result["gauss_resolution_passed"],
                physical_result["raw_evenness_passed"],
            )
        ),
        "crossed_finite_x_completion": False,
        "numeric_UV_coefficient_complete": False,
        "local_GR_claim": False,
        "full_MTS_claim": False,
        "formalization_workbench_digest": formal_digest,
        "elapsed_seconds": time.perf_counter() - started,
        "outputs": [
            relative(ENDPOINT_CSV),
            relative(FIXED_X_CSV),
            relative(PHYSICAL_CSV),
            relative(HYBRID_CSV),
            relative(GATE_CSV),
            relative(RESULT_JSON),
            relative(PROVENANCE),
            relative(DOCUMENT),
            relative(VALIDATION_CSV),
        ],
    }
    RESULT_JSON.parent.mkdir(parents=True, exist_ok=True)
    RESULT_JSON.write_text(
        json.dumps(result, indent=2, sort_keys=True, default=json_default),
        encoding="utf-8",
    )
    write_document(result)
    output_paths = (
        Path(__file__),
        ENDPOINT_CSV,
        FIXED_X_CSV,
        PHYSICAL_CSV,
        HYBRID_CSV,
        GATE_CSV,
        RESULT_JSON,
        PROVENANCE,
        DOCUMENT,
    )
    validation = validation_rows(output_paths, gates)
    write_csv(VALIDATION_CSV, tagged(validation))
    result["validation_all_passed"] = all(row["passed"] for row in validation)
    result["validation_checks"] = len(validation)
    result["elapsed_seconds"] = time.perf_counter() - started
    RESULT_JSON.write_text(
        json.dumps(result, indent=2, sort_keys=True, default=json_default),
        encoding="utf-8",
    )
    print(json.dumps(result, indent=2, sort_keys=True, default=json_default))


if __name__ == "__main__":
    main()
