from __future__ import annotations

import argparse
import csv
import hashlib
import itertools
import json
import math
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np
import sympy as sp
from scipy.optimize import minimize_scalar


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"

MARKER = "MTS_RENORMALIZED_MOTION_SCALAR_GAP_STRESS_THREE_POINT_4909"
FORMAL_MARKER = "PPC4161_RENORMALIZED_MOTION_SCALAR_GAP_STRESS_THREE_POINT_4909"
NEXT_TARGET = (
    "4910-Y5-R2FR-motion-scalar-cutoff-volume-extrapolation-and-"
    "TTT-Weyl-cubic-projection.md"
)
CHECKED_DATE = "2026-07-12"
DIMENSIONS = 4
POTENTIAL_POWER = 4.0 / 3.0


@dataclass(frozen=True)
class LatticeConfig:
    branch: str
    size: int
    mu_hat: float
    bare_mass: float
    thermal_sweeps: int
    observations: int
    thin_sweeps: int
    overrelax_sweeps: int
    seed: int

    @property
    def coupling(self) -> float:
        return self.mu_hat ** (8.0 / 3.0) if self.mu_hat > 0 else 0.0

    @property
    def bare_mass_squared(self) -> float:
        return self.bare_mass**2

    @property
    def box_mu(self) -> float:
        return self.size * self.mu_hat


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def contains(path: Path, marker: str) -> bool:
    return path.exists() and marker in path.read_text(
        encoding="utf-8", errors="replace"
    )


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise ValueError(f"refusing to write empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames: list[str] = []
    for row in rows:
        for key in row:
            if key not in fieldnames:
                fieldnames.append(key)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def tagged(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    def clean(value: Any) -> Any:
        if isinstance(value, (float, np.floating)) and not math.isfinite(
            float(value)
        ):
            return "not_applicable"
        return value

    return [
        {
            **{key: clean(value) for key, value in row.items()},
            "checkpoint_marker": MARKER,
            "valid_for_claim": False,
            "source_checked_date": CHECKED_DATE,
        }
        for row in rows
    ]


def source_contract() -> dict[str, Any]:
    sources = [
        (
            "SRC4909_00_predecessor",
            POST
            / "4908-Y5-R2FR-microscopic-MTS-metric-three-point-vertex-and-Weyl-cubic-coefficient-or-zero-residual-theorem.md",
            "MTS_MICROSCOPIC_METRIC_THREE_POINT_WEYL_CUBIC_4908",
            "validated_predecessor",
        ),
        (
            "SRC4909_01_predecessor_validation",
            OUTPUT / "P8_Y5_BRR545_4908_VALIDATION.csv",
            "VAL4908_OVERALL,PASS",
            "validated_predecessor",
        ),
        (
            "SRC4909_02_core_action",
            ROOT
            / "core-mts-framework"
            / "action-principle"
            / "the-fundamental-action-of-motion-timespace-field-theory.md",
            "n = 4/3",
            "printed_motion_scalar_action",
        ),
        (
            "SRC4909_03_covariant_parent",
            POST
            / "4876-Y5-R2FR-integrated-H-parent-action-saddle-regulator-and-induced-coefficient-matching-to-GN-Lambda-and-R2.md",
            "INTEGRATED_H_PARENT_SADDLE_HEAT_KERNEL_POLE_HIERARCHY_4876",
            "covariant_scalar_determinant",
        ),
        (
            "SRC4909_04_scalar_a6",
            POST
            / "4881-Y5-R2FR-compact-matter-interior-EOS-contact-matching-and-Riemann-cubed-coefficient-owner-gate.md",
            "MTS_COMPACT_FLUID_TOV_AND_SCALAR_A6_OWNER_4881",
            "Weyl_cubic_projection_normalization",
        ),
        (
            "SRC4909_05_current_action",
            POST
            / "4904-Y5-R2FR-current-unified-action-assembly-Ward-identity-and-parameter-prediction-ledger.md",
            "MTS_CURRENT_UNIFIED_ACTION_WARD_PARAMETER_GATE_4904",
            "active_action_and_known_limits",
        ),
    ]
    rows: list[dict[str, Any]] = []
    for source_id, path, marker, role in sources:
        exists = path.exists()
        rows.append(
            {
                "source_id": source_id,
                "source_type": role,
                "source_path_or_url": str(path),
                "local_path_required": True,
                "source_exists": exists,
                "marker": marker,
                "marker_found": contains(path, marker),
                "sha256": sha256(path) if exists else "",
            }
        )
    return {
        "rows": rows,
        "passed": all(
            row["source_exists"] and row["marker_found"] for row in rows
        ),
    }


def lattice_scaling_rows() -> list[dict[str, Any]]:
    return [
        {
            "quantity": "dimensionless_lattice_field",
            "equation": "varphi_n=a psi(x_n)",
            "result": "[varphi]=0",
            "gate": "EXACT",
        },
        {
            "quantity": "lattice_action",
            "equation": "S_a=sum_n[1/2 sum_mu(varphi_(n+mu)-varphi_n)^2+1/2 r_a varphi_n^2+3/4 g_a |varphi_n|^(4/3)]",
            "result": "finite positive measure for g_a>0 and real r_a",
            "gate": "EXACT_FINITE_CUTOFF",
        },
        {
            "quantity": "literal_coupling_trajectory",
            "equation": "g_a=(a mu)^(8/3)=mu_hat^(8/3); r_a=0",
            "result": "one-parameter bare trajectory inherited from the printed action",
            "gate": "TESTABLE_NOT_ASSUMED_RENORMALIZED",
        },
        {
            "quantity": "continuum_condition",
            "equation": "mu_hat=a mu -> 0",
            "result": "correlation length in sites must diverge",
            "gate": "REQUIRED",
        },
        {
            "quantity": "infinite_volume_condition",
            "equation": "L mu=N mu_hat -> infinity",
            "result": "N must grow faster than 1/mu_hat",
            "gate": "REQUIRED",
        },
        {
            "quantity": "mass_ratio",
            "equation": "c_m(a,L)=a m_gap/mu_hat",
            "result": "finite universal limit required for one-parameter parent prediction",
            "gate": "EMPIRICAL_LATTICE_TEST",
        },
        {
            "quantity": "counterterm_closure",
            "equation": "r_a and all symmetry-allowed relevant operators must be tracked under blocking",
            "result": "literal r_a=0 is a prediction only if cutoff convergence proves it",
            "gate": "NOT_SMUGGLED",
        },
    ]


def full_action(field: np.ndarray, coupling: float, mass_squared: float) -> float:
    kinetic = 0.0
    for axis in range(field.ndim):
        kinetic += 0.5 * float(
            np.sum((np.roll(field, -1, axis=axis) - field) ** 2)
        )
    mass = 0.5 * mass_squared * float(np.sum(field**2))
    potential = 0.75 * coupling * float(
        np.sum(np.abs(field) ** POTENTIAL_POWER)
    )
    return kinetic + mass + potential


def neighbor_sum(field: np.ndarray) -> np.ndarray:
    result = np.zeros_like(field)
    for axis in range(field.ndim):
        result += np.roll(field, 1, axis=axis)
        result += np.roll(field, -1, axis=axis)
    return result


def metropolis_sweep(
    field: np.ndarray,
    parity: np.ndarray,
    coupling: float,
    mass_squared: float,
    step: float,
    rng: np.random.Generator,
) -> float:
    accepted = 0
    total = 0
    for mask in (parity, ~parity):
        neighbors = neighbor_sum(field)
        old = field[mask]
        proposal = old + rng.uniform(-step, step, size=old.shape)
        square_difference = proposal**2 - old**2
        delta_action = (
            DIMENSIONS * square_difference
            - (proposal - old) * neighbors[mask]
            + 0.5 * mass_squared * square_difference
            + 0.75
            * coupling
            * (
                np.abs(proposal) ** POTENTIAL_POWER
                - np.abs(old) ** POTENTIAL_POWER
            )
        )
        keep = np.log(rng.random(size=old.shape)) < -delta_action
        updated = old.copy()
        updated[keep] = proposal[keep]
        field[mask] = updated
        accepted += int(np.count_nonzero(keep))
        total += keep.size
    return accepted / total


def overrelaxation_sweep(
    field: np.ndarray,
    parity: np.ndarray,
    coupling: float,
    mass_squared: float,
    rng: np.random.Generator,
) -> float:
    accepted = 0
    total = 0
    denominator = 2.0 * DIMENSIONS + mass_squared
    for mask in (parity, ~parity):
        neighbors = neighbor_sum(field)
        old = field[mask]
        proposal = 2.0 * neighbors[mask] / denominator - old
        delta_action = 0.75 * coupling * (
            np.abs(proposal) ** POTENTIAL_POWER
            - np.abs(old) ** POTENTIAL_POWER
        )
        keep = np.log(rng.random(size=old.shape)) < -delta_action
        updated = old.copy()
        updated[keep] = proposal[keep]
        field[mask] = updated
        accepted += int(np.count_nonzero(keep))
        total += keep.size
    return accepted / total


def local_delta_validation(seed: int = 4909) -> dict[str, Any]:
    rng = np.random.default_rng(seed)
    size = 4
    field = rng.normal(scale=0.4, size=(size,) * DIMENSIONS)
    coupling = 0.37
    mass_squared = 0.19
    max_residual = 0.0
    for _ in range(64):
        coordinate = tuple(int(rng.integers(0, size)) for _ in range(DIMENSIONS))
        old = float(field[coordinate])
        proposal = old + float(rng.normal(scale=0.6))
        neighbors = 0.0
        for axis in range(DIMENSIONS):
            plus = list(coordinate)
            minus = list(coordinate)
            plus[axis] = (plus[axis] + 1) % size
            minus[axis] = (minus[axis] - 1) % size
            neighbors += float(field[tuple(plus)] + field[tuple(minus)])
        square_difference = proposal**2 - old**2
        local_delta = (
            DIMENSIONS * square_difference
            - (proposal - old) * neighbors
            + 0.5 * mass_squared * square_difference
            + 0.75
            * coupling
            * (abs(proposal) ** POTENTIAL_POWER - abs(old) ** POTENTIAL_POWER)
        )
        before = full_action(field, coupling, mass_squared)
        changed = field.copy()
        changed[coordinate] = proposal
        exact_delta = full_action(changed, coupling, mass_squared) - before
        max_residual = max(max_residual, abs(local_delta - exact_delta))
    return {
        "trials": 64,
        "max_absolute_delta_action_residual": max_residual,
        "passed": max_residual < 5e-12,
    }


def measure_plane_correlation(field: np.ndarray) -> np.ndarray:
    size = field.shape[0]
    max_separation = size // 2
    axis_correlations: list[np.ndarray] = []
    for axis in range(DIMENSIONS):
        transverse_axes = tuple(
            other for other in range(DIMENSIONS) if other != axis
        )
        plane_average = field.mean(axis=transverse_axes)
        correlation = np.array(
            [
                np.mean(
                    plane_average
                    * np.roll(plane_average, -separation)
                )
                for separation in range(max_separation + 1)
            ],
            dtype=float,
        )
        axis_correlations.append(correlation)
    return np.mean(axis_correlations, axis=0)


def integrated_autocorrelation(series: np.ndarray) -> float:
    centered = np.asarray(series, dtype=float) - float(np.mean(series))
    variance = float(np.dot(centered, centered) / len(centered))
    if variance <= 0 or len(centered) < 4:
        return 0.5
    maximum_lag = min(len(centered) // 4, 200)
    tau = 0.5
    for lag in range(1, maximum_lag + 1):
        covariance = float(
            np.dot(centered[:-lag], centered[lag:]) / (len(centered) - lag)
        )
        rho = covariance / variance
        if rho <= 0:
            break
        tau += rho
    return tau


def fit_periodic_mass(correlation: np.ndarray, size: int) -> float:
    separations = np.arange(1, len(correlation), dtype=float)
    values = np.asarray(correlation[1:], dtype=float)
    if len(values) < 2 or np.any(~np.isfinite(values)):
        return math.nan

    def objective(log_mass: float) -> float:
        mass = math.exp(log_mass)
        template = np.exp(-mass * separations) + np.exp(
            -mass * (size - separations)
        )
        amplitude = float(np.dot(values, template) / np.dot(template, template))
        residual = values - amplitude * template
        scale = max(float(np.dot(values, values)), 1e-300)
        return float(np.dot(residual, residual) / scale)

    fit = minimize_scalar(
        objective,
        bounds=(math.log(0.02), math.log(4.0)),
        method="bounded",
        options={"xatol": 1e-10},
    )
    return math.exp(float(fit.x)) if fit.success else math.nan


def effective_masses(correlation: np.ndarray) -> list[float]:
    masses: list[float] = []
    for index in range(1, len(correlation) - 1):
        denominator = 2.0 * correlation[index]
        ratio = (
            (correlation[index - 1] + correlation[index + 1])
            / denominator
            if denominator > 0
            else math.nan
        )
        masses.append(math.acosh(ratio) if ratio >= 1 else math.nan)
    return masses


def jackknife_mass(
    observations: np.ndarray,
    size: int,
    tau_observations: float,
) -> dict[str, Any]:
    count = len(observations)
    block_size = max(4, int(math.ceil(2.0 * tau_observations)))
    if count // block_size < 8:
        block_size = max(1, count // 8)
    block_count = count // block_size
    used = block_count * block_size
    if block_count < 4:
        return {
            "mass": fit_periodic_mass(np.mean(observations, axis=0), size),
            "mass_standard_error": math.nan,
            "block_size": block_size,
            "block_count": block_count,
            "used_observations": used,
        }
    trimmed = observations[:used]
    total = np.sum(trimmed, axis=0)
    estimates: list[float] = []
    for block in range(block_count):
        start = block * block_size
        stop = start + block_size
        leave_one_out = (total - np.sum(trimmed[start:stop], axis=0)) / (
            used - block_size
        )
        estimates.append(fit_periodic_mass(leave_one_out, size))
    estimate_array = np.asarray(estimates)
    finite = estimate_array[np.isfinite(estimate_array)]
    full_mass = fit_periodic_mass(np.mean(trimmed, axis=0), size)
    standard_error = (
        math.sqrt(
            (len(finite) - 1)
            / len(finite)
            * float(np.sum((finite - np.mean(finite)) ** 2))
        )
        if len(finite) >= 4
        else math.nan
    )
    return {
        "mass": full_mass,
        "mass_standard_error": standard_error,
        "block_size": block_size,
        "block_count": block_count,
        "used_observations": used,
    }


def run_lattice(config: LatticeConfig) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    rng = np.random.default_rng(config.seed)
    shape = (config.size,) * DIMENSIONS
    field = np.zeros(shape, dtype=np.float64)
    parity = (np.indices(shape).sum(axis=0) & 1).astype(bool)
    step = 1.0
    thermal_acceptance: list[float] = []
    start_time = time.perf_counter()

    for sweep_index in range(config.thermal_sweeps):
        acceptance = metropolis_sweep(
            field,
            parity,
            config.coupling,
            config.bare_mass_squared,
            step,
            rng,
        )
        thermal_acceptance.append(acceptance)
        for _ in range(config.overrelax_sweeps):
            overrelaxation_sweep(
                field,
                parity,
                config.coupling,
                config.bare_mass_squared,
                rng,
            )
        if (sweep_index + 1) % 50 == 0:
            recent = float(np.mean(thermal_acceptance[-50:]))
            if recent > 0.58:
                step *= 1.08
            elif recent < 0.42:
                step /= 1.08

    correlations: list[np.ndarray] = []
    zero_mode_squared: list[float] = []
    field_squared: list[float] = []
    metropolis_acceptance: list[float] = []
    overrelax_acceptance: list[float] = []

    for _ in range(config.observations):
        for _ in range(config.thin_sweeps):
            metropolis_acceptance.append(
                metropolis_sweep(
                    field,
                    parity,
                    config.coupling,
                    config.bare_mass_squared,
                    step,
                    rng,
                )
            )
            for _ in range(config.overrelax_sweeps):
                overrelax_acceptance.append(
                    overrelaxation_sweep(
                        field,
                        parity,
                        config.coupling,
                        config.bare_mass_squared,
                        rng,
                    )
                )
        if rng.random() < 0.5:
            field *= -1.0
        correlations.append(measure_plane_correlation(field))
        zero_mode_squared.append(float(np.mean(field) ** 2))
        field_squared.append(float(np.mean(field**2)))

    correlation_array = np.asarray(correlations)
    mean_correlation = np.mean(correlation_array, axis=0)
    tau_observations = integrated_autocorrelation(
        np.asarray(zero_mode_squared)
    )
    fit = jackknife_mass(
        correlation_array, config.size, tau_observations
    )
    mass = float(fit["mass"])
    mass_error = float(fit["mass_standard_error"])
    effective = effective_masses(mean_correlation)
    finite_effective = [value for value in effective if math.isfinite(value)]
    expected_free_mass = (
        2.0 * math.asinh(config.bare_mass / 2.0)
        if config.branch == "free_validation"
        else math.nan
    )
    summary = {
        **asdict(config),
        "coupling_g_a": config.coupling,
        "box_mu": config.box_mu,
        "proposal_step": step,
        "metropolis_acceptance": float(np.mean(metropolis_acceptance)),
        "overrelax_acceptance": float(np.mean(overrelax_acceptance))
        if overrelax_acceptance
        else math.nan,
        "tau_zero_mode_observations": tau_observations,
        "tau_zero_mode_sweeps": tau_observations * config.thin_sweeps,
        "effective_sample_size": config.observations
        / max(2.0 * tau_observations, 1.0),
        "mass_gap_lattice": mass,
        "mass_gap_standard_error": mass_error,
        "c_m_lattice": mass / config.mu_hat
        if config.mu_hat > 0
        else math.nan,
        "c_m_standard_error": mass_error / config.mu_hat
        if config.mu_hat > 0
        else math.nan,
        "effective_mass_median": float(np.median(finite_effective))
        if finite_effective
        else math.nan,
        "expected_free_lattice_mass": expected_free_mass,
        "free_relative_error": abs(mass / expected_free_mass - 1.0)
        if math.isfinite(expected_free_mass)
        else math.nan,
        "jackknife_block_size": fit["block_size"],
        "jackknife_block_count": fit["block_count"],
        "used_observations": fit["used_observations"],
        "mean_field_squared": float(np.mean(field_squared)),
        "elapsed_seconds": time.perf_counter() - start_time,
    }
    correlation_rows = [
        {
            "branch": config.branch,
            "size": config.size,
            "mu_hat": config.mu_hat,
            "bare_mass": config.bare_mass,
            "seed": config.seed,
            "separation": separation,
            "correlation": float(value),
        }
        for separation, value in enumerate(mean_correlation)
    ]
    return summary, correlation_rows


def gaussian_third_response_validation(
    size: int = 6,
    bare_mass: float = 0.8,
    samples: int = 120_000,
    seed: int = 490903,
) -> dict[str, Any]:
    momenta = [2.0 * math.pi * np.arange(size) / size for _ in range(DIMENSIONS)]
    mesh = np.meshgrid(*momenta, indexing="ij")
    eigenvalues = np.full((size,) * DIMENSIONS, bare_mass**2)
    for component in mesh:
        eigenvalues += 4.0 * np.sin(component / 2.0) ** 2
    inverse = 1.0 / eigenvalues.ravel()
    exact_first = 0.5 * float(np.sum(inverse))
    exact_second = -0.5 * float(np.sum(inverse**2))
    exact_third = float(np.sum(inverse**3))

    rng = np.random.default_rng(seed)
    batch_size = 1000
    q_values: list[np.ndarray] = []
    for start in range(0, samples, batch_size):
        count = min(batch_size, samples - start)
        normal = rng.normal(size=(count, inverse.size))
        q_values.append(0.5 * np.sum(normal**2 * inverse, axis=1))
    observable = np.concatenate(q_values)
    centered = observable - float(np.mean(observable))
    estimated_first = float(np.mean(observable))
    estimated_second = -float(np.var(observable))
    estimated_third = float(np.mean(centered**3))

    chunks = np.array_split(centered, 120)
    chunk_thirds = np.array([float(np.mean(chunk**3)) for chunk in chunks])
    third_standard_error = float(
        np.std(chunk_thirds, ddof=1) / math.sqrt(len(chunk_thirds))
    )
    return {
        "size": size,
        "bare_mass": bare_mass,
        "samples": samples,
        "exact_W_first": exact_first,
        "estimated_W_first": estimated_first,
        "first_relative_error": abs(estimated_first / exact_first - 1.0),
        "exact_W_second": exact_second,
        "estimated_W_second": estimated_second,
        "second_relative_error": abs(estimated_second / exact_second - 1.0),
        "exact_W_third": exact_third,
        "estimated_W_third": estimated_third,
        "third_standard_error": third_standard_error,
        "third_pull": (estimated_third - exact_third) / third_standard_error,
        "third_relative_error": abs(estimated_third / exact_third - 1.0),
        "passed": abs(estimated_first / exact_first - 1.0) < 0.01
        and abs(estimated_second / exact_second - 1.0) < 0.03
        and abs(estimated_third - exact_third) < 4.0 * third_standard_error,
    }


def gaussian_distinct_third_response_validation(
    samples: int = 240_000,
    seed: int = 490906,
) -> dict[str, Any]:
    rng = np.random.default_rng(seed)
    rank = 5
    base = np.diag(np.linspace(1.0, 2.0, rank))

    def symmetric(scale: float) -> np.ndarray:
        raw = rng.normal(scale=scale, size=(rank, rank))
        return 0.5 * (raw + raw.T)

    k1, k2, k3 = (symmetric(0.12) for _ in range(3))
    k12, k13, k23 = (symmetric(0.05) for _ in range(3))
    k123 = symmetric(0.025)
    inverse = np.linalg.inv(base)
    exact = 0.5 * float(
        np.trace(inverse @ k123)
        - np.trace(inverse @ k1 @ inverse @ k23)
        - np.trace(inverse @ k2 @ inverse @ k13)
        - np.trace(inverse @ k3 @ inverse @ k12)
        + np.trace(inverse @ k1 @ inverse @ k2 @ inverse @ k3)
        + np.trace(inverse @ k1 @ inverse @ k3 @ inverse @ k2)
    )
    cholesky = np.linalg.cholesky(inverse)
    batch_size = 2000
    observables: list[np.ndarray] = []
    for start in range(0, samples, batch_size):
        count = min(batch_size, samples - start)
        fields = rng.normal(size=(count, rank)) @ cholesky.T
        matrices = (k1, k2, k3, k12, k13, k23, k123)
        values = np.column_stack(
            [
                0.5 * np.einsum("bi,ij,bj->b", fields, matrix, fields)
                for matrix in matrices
            ]
        )
        observables.append(values)
    values = np.vstack(observables)

    def connected_estimator(block: np.ndarray) -> float:
        s1, s2, s3, s12, s13, s23, s123 = block.T
        centered1 = s1 - np.mean(s1)
        centered2 = s2 - np.mean(s2)
        centered3 = s3 - np.mean(s3)
        return float(
            np.mean(s123)
            - np.mean(centered1 * (s23 - np.mean(s23)))
            - np.mean(centered2 * (s13 - np.mean(s13)))
            - np.mean(centered3 * (s12 - np.mean(s12)))
            + np.mean(centered1 * centered2 * centered3)
        )

    estimate = connected_estimator(values)
    chunks = np.array_split(values, 120)
    chunk_estimates = np.array(
        [connected_estimator(chunk) for chunk in chunks]
    )
    standard_error = float(
        np.std(chunk_estimates, ddof=1) / math.sqrt(len(chunk_estimates))
    )
    return {
        "matrix_rank": rank,
        "samples": samples,
        "exact_W_123": exact,
        "estimated_W_123": estimate,
        "standard_error": standard_error,
        "pull": (estimate - exact) / standard_error,
        "relative_error": abs(estimate / exact - 1.0),
        "passed": abs(estimate - exact) < 4.0 * standard_error,
    }


def densitized_metric_seagull_validation() -> dict[str, Any]:
    epsilon1, epsilon2, epsilon3 = sp.symbols("epsilon1 epsilon2 epsilon3")
    h1 = sp.Matrix(
        [[1, 2, 0, 1], [2, -1, 1, 0], [0, 1, 0, 2], [1, 0, 2, 0]]
    )
    h2 = sp.Matrix(
        [[0, 1, 2, 0], [1, 2, 0, 1], [2, 0, -1, 1], [0, 1, 1, -1]]
    )
    h3 = sp.Matrix(
        [[2, 0, 1, 1], [0, -2, 1, 0], [1, 1, 0, 2], [1, 0, 2, 0]]
    )
    density = sp.eye(4) + epsilon1 * h1 + epsilon2 * h2 + epsilon3 * h3
    volume = sp.sqrt(sp.expand(density.det()))
    zero = {epsilon1: 0, epsilon2: 0, epsilon3: 0}
    first = sp.simplify(sp.diff(volume, epsilon1).subs(zero))
    second = sp.simplify(sp.diff(volume, epsilon1, epsilon2).subs(zero))
    third = sp.simplify(
        sp.diff(volume, epsilon1, epsilon2, epsilon3).subs(zero)
    )
    expected_first = sp.trace(h1) / 2
    expected_second = -sp.trace(h1 * h2) / 2
    expected_third = (
        sp.trace(h1 * h2 * h3) + sp.trace(h1 * h3 * h2)
    ) / 2
    return {
        "trace_h1": str(sp.trace(h1)),
        "trace_h2": str(sp.trace(h2)),
        "trace_h3": str(sp.trace(h3)),
        "first_volume_derivative": str(first),
        "first_expected": str(expected_first),
        "mixed_second_volume_derivative": str(second),
        "mixed_second_expected": str(expected_second),
        "mixed_third_volume_derivative": str(third),
        "mixed_third_expected": str(expected_third),
        "passed": first == expected_first
        and second == expected_second
        and third == expected_third,
    }


def transverse_traceless_polarization(
    momentum: np.ndarray, seed: int
) -> np.ndarray:
    rng = np.random.default_rng(seed)
    unit = momentum / np.linalg.norm(momentum)
    projector = np.eye(DIMENSIONS) - np.outer(unit, unit)
    raw = rng.normal(size=(DIMENSIONS, DIMENSIONS))
    raw = 0.5 * (raw + raw.T)
    polarization = projector @ raw @ projector
    polarization -= np.trace(polarization) * projector / (DIMENSIONS - 1)
    polarization /= math.sqrt(float(np.sum(polarization**2)))
    return polarization


def linearized_Weyl(
    momentum: np.ndarray, polarization: np.ndarray
) -> np.ndarray:
    delta = np.eye(DIMENSIONS)
    Riemann = np.zeros((DIMENSIONS,) * 4, dtype=float)
    for mu, nu, rho, sigma in itertools.product(
        range(DIMENSIONS), repeat=4
    ):
        Riemann[mu, nu, rho, sigma] = 0.5 * (
            -momentum[rho] * momentum[nu] * polarization[mu, sigma]
            - momentum[sigma] * momentum[mu] * polarization[nu, rho]
            + momentum[sigma] * momentum[nu] * polarization[mu, rho]
            + momentum[rho] * momentum[mu] * polarization[nu, sigma]
        )
    Ricci = np.einsum("mnms->ns", Riemann)
    scalar = float(np.trace(Ricci))
    Weyl = np.zeros_like(Riemann)
    for mu, nu, rho, sigma in itertools.product(
        range(DIMENSIONS), repeat=4
    ):
        Weyl[mu, nu, rho, sigma] = (
            Riemann[mu, nu, rho, sigma]
            - 0.5
            * (
                delta[mu, rho] * Ricci[sigma, nu]
                - delta[mu, sigma] * Ricci[rho, nu]
                - delta[nu, rho] * Ricci[sigma, mu]
                + delta[nu, sigma] * Ricci[rho, mu]
            )
            + scalar
            / 6.0
            * (
                delta[mu, rho] * delta[sigma, nu]
                - delta[mu, sigma] * delta[rho, nu]
            )
        )
    return Weyl


def Weyl_cubic_template() -> dict[str, Any]:
    base_momenta = [
        np.array([1.0, 0.0, 0.0, 0.0]),
        np.array([0.0, 1.0, 0.0, 0.0]),
        np.array([-1.0, -1.0, 0.0, 0.0]),
    ]
    polarizations = [
        transverse_traceless_polarization(momentum, 10 + index)
        for index, momentum in enumerate(base_momenta)
    ]
    trace_residual = max(abs(float(np.trace(item))) for item in polarizations)
    transverse_residual = max(
        float(np.max(np.abs(momentum @ polarization)))
        for momentum, polarization in zip(base_momenta, polarizations)
    )
    closure_residual = float(np.max(np.abs(sum(base_momenta))))
    rows: list[dict[str, Any]] = []
    base_value = math.nan
    for scale in (1, 2, 3, 4):
        Weyls = [
            linearized_Weyl(scale * momentum, polarization)
            for momentum, polarization in zip(base_momenta, polarizations)
        ]
        value = sum(
            float(
                np.einsum(
                    "mnrs,rsab,abmn",
                    Weyls[order[0]],
                    Weyls[order[1]],
                    Weyls[order[2]],
                )
            )
            for order in itertools.permutations(range(3))
        )
        if scale == 1:
            base_value = value
        rows.append(
            {
                "integer_momentum_scale": scale,
                "symmetrized_Weyl_cubic_template": value,
                "ratio_to_scale_one": value / base_value,
                "expected_scale_six": float(scale**6),
                "scale_six_residual": abs(value / base_value - scale**6),
                "minimum_periodic_lattice_size": 2 * scale + 2,
            }
        )
    return {
        "rows": rows,
        "momentum_closure_residual": closure_residual,
        "trace_residual": trace_residual,
        "transverse_residual": transverse_residual,
        "base_template": base_value,
        "passed": closure_residual < 1e-14
        and trace_residual < 1e-14
        and transverse_residual < 1e-14
        and abs(base_value) > 1e-6
        and max(row["scale_six_residual"] for row in rows) < 1e-9,
    }


def stress_three_point_rows() -> list[dict[str, Any]]:
    return [
        {
            "stage": "metric_source_family",
            "required_equation": "g_mn=delta_mn+sum_i epsilon_i h_mn^(i); q1+q2+q3=0; q_i^m h_mn^(i)=0; trace h^(i)=0",
            "current_status": "NONZERO_TT_WEYL_CUBIC_TRIPLET_CONSTRUCTED",
            "claim_safe": False,
        },
        {
            "stage": "action_derivatives",
            "required_equation": "H^mn=sqrt(g)g^mn; d_ij sqrt(det H)=-Tr(h_i h_j)/2; d_123 sqrt(det H)=[Tr(h_i h_j h_k)+Tr(h_i h_k h_j)]/2",
            "current_status": "EXACT_DENSITIZED_VOLUME_SEAGULLS_DERIVED",
            "claim_safe": False,
        },
        {
            "stage": "connected_third_response",
            "required_equation": "W_123=<S_123>-Cov(S1,S23)-Cov(S2,S13)-Cov(S3,S12)+<deltaS1 deltaS2 deltaS3>",
            "current_status": "EXACT_IDENTITY_GAUSSIAN_VALIDATED",
            "claim_safe": False,
        },
        {
            "stage": "Ward_projection",
            "required_equation": "q1^m W_mn,rs,ab=contact terms fixed by W_2 and seagulls",
            "current_status": "REQUIRED_BEFORE_C3_FIT",
            "claim_safe": False,
        },
        {
            "stage": "derivative_separation",
            "required_equation": "fit q^0,q^2,q^4,q^6 terms across at least four momentum triplets",
            "current_status": "SCALES_1_TO_4_CONSTRUCTED_WITH_EXACT_SIXTH_POWER_TEMPLATE",
            "claim_safe": False,
        },
        {
            "stage": "Weyl_cubic_projection",
            "required_equation": "c6=mu^2 P_C3 W_TTT^(q6) after volume, EH and curvature-squared subtraction",
            "current_status": "NOT_NUMERICALLY_EXECUTED",
            "claim_safe": False,
        },
        {
            "stage": "continuum_and_volume",
            "required_equation": "mu_hat->0 and N mu_hat->infinity with common c6",
            "current_status": "REQUIRED",
            "claim_safe": False,
        },
    ]


def configurations(profile: str) -> list[LatticeConfig]:
    if profile == "smoke":
        return [
            LatticeConfig("free_validation", 6, 0.0, 0.8, 250, 350, 1, 1, 490901),
            LatticeConfig("literal_MTS", 6, 1.0, 0.0, 350, 450, 1, 1, 490902),
        ]
    if profile == "checkpoint":
        return [
            LatticeConfig("free_validation", 8, 0.0, 0.7, 600, 800, 2, 2, 490901),
            LatticeConfig("literal_MTS", 8, 0.8, 0.0, 800, 1000, 2, 2, 490902),
            LatticeConfig("literal_MTS", 10, 0.6, 0.0, 1000, 1100, 2, 2, 490903),
            LatticeConfig("literal_MTS", 12, 0.6, 0.0, 1100, 1000, 2, 2, 490913),
            LatticeConfig("literal_MTS", 12, 0.5, 0.0, 1200, 1100, 2, 2, 490904),
            LatticeConfig("literal_MTS", 12, 0.5, 0.0, 1200, 1100, 2, 2, 490914),
            LatticeConfig("literal_MTS", 16, 0.4, 0.0, 1300, 900, 2, 2, 490905),
        ]
    if profile == "long":
        return [
            LatticeConfig("free_validation", 12, 0.0, 0.5, 2000, 4000, 3, 3, 490901),
            LatticeConfig("literal_MTS", 12, 0.6, 0.0, 2500, 5000, 3, 3, 490902),
            LatticeConfig("literal_MTS", 16, 0.4, 0.0, 3000, 5000, 3, 3, 490903),
            LatticeConfig("literal_MTS", 20, 0.3, 0.0, 4000, 5000, 4, 3, 490904),
            LatticeConfig("literal_MTS", 24, 0.25, 0.0, 5000, 5000, 4, 3, 490905),
        ]
    raise ValueError(f"unknown profile: {profile}")


def cutoff_aggregate_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    interacting = [row for row in rows if row["branch"] == "literal_MTS"]
    aggregate: list[dict[str, Any]] = []
    for mu_hat in sorted({row["mu_hat"] for row in interacting}, reverse=True):
        same_cutoff = [row for row in interacting if row["mu_hat"] == mu_hat]
        largest_size = max(row["size"] for row in same_cutoff)
        selected = [row for row in same_cutoff if row["size"] == largest_size]
        values = np.array([row["c_m_lattice"] for row in selected], dtype=float)
        errors = np.array(
            [row["c_m_standard_error"] for row in selected], dtype=float
        )
        finite_errors = errors[np.isfinite(errors) & (errors > 0)]
        fallback = float(np.median(finite_errors)) if len(finite_errors) else 0.1
        errors = np.where(np.isfinite(errors) & (errors > 0), errors, fallback)
        weights = 1.0 / errors**2
        mean = float(np.sum(weights * values) / np.sum(weights))
        error = math.sqrt(1.0 / float(np.sum(weights)))
        aggregate.append(
            {
                "mu_hat": mu_hat,
                "selected_size": largest_size,
                "box_mu": largest_size * mu_hat,
                "replicate_count": len(selected),
                "c_m": mean,
                "c_m_standard_error": error,
                "minimum_mass_times_box": min(
                    row["mass_gap_lattice"] * row["size"] for row in selected
                ),
            }
        )
    return aggregate


def weighted_model(
    x: np.ndarray, y: np.ndarray, errors: np.ndarray
) -> tuple[np.ndarray, np.ndarray, float, int]:
    weights = 1.0 / errors**2
    design = np.column_stack([np.ones_like(x), x])
    normal = design.T @ (weights[:, None] * design)
    covariance = np.linalg.inv(normal)
    parameters = covariance @ design.T @ (weights * y)
    residual = y - design @ parameters
    chi_squared = float(np.sum((residual / errors) ** 2))
    return parameters, covariance, chi_squared, len(y) - 2


def extrapolation_summary(
    rows: list[dict[str, Any]], aggregates: list[dict[str, Any]]
) -> dict[str, Any]:
    interacting = [row for row in rows if row["branch"] == "literal_MTS"]
    if len(aggregates) < 3:
        return {
            "raw_point_count": len(interacting),
            "cutoff_point_count": len(aggregates),
            "constant_c_m": math.nan,
            "linear_mu_intercept": math.nan,
            "linear_mu2_intercept": math.nan,
            "maximum_box_mu": max((row["box_mu"] for row in interacting), default=0.0),
            "minimum_mu_hat": min((row["mu_hat"] for row in interacting), default=math.nan),
            "promotion_ready": False,
            "reason": "fewer than three independent cutoff points",
        }
    mu_hat = np.array([row["mu_hat"] for row in aggregates], dtype=float)
    y = np.array([row["c_m"] for row in aggregates], dtype=float)
    errors = np.array(
        [row["c_m_standard_error"] for row in aggregates], dtype=float
    )
    finite_errors = errors[np.isfinite(errors) & (errors > 0)]
    fallback = float(np.median(finite_errors)) if len(finite_errors) else 0.05
    errors = np.where(np.isfinite(errors) & (errors > 0), errors, fallback)
    weights = 1.0 / errors**2
    constant = float(np.sum(weights * y) / np.sum(weights))
    constant_error = math.sqrt(1.0 / float(np.sum(weights)))
    constant_chi_squared = float(np.sum(((y - constant) / errors) ** 2))
    linear_mu, covariance_mu, chi_squared_mu, degrees_mu = weighted_model(
        mu_hat, y, errors
    )
    linear_mu2, covariance_mu2, chi_squared_mu2, degrees_mu2 = weighted_model(
        mu_hat**2, y, errors
    )
    maximum_box_mu = max(row["box_mu"] for row in interacting)
    minimum_mu_hat = min(row["mu_hat"] for row in interacting)
    intercepts = [constant, float(linear_mu[0]), float(linear_mu2[0])]
    intercept_errors = [
        constant_error,
        math.sqrt(float(covariance_mu[0, 0])),
        math.sqrt(float(covariance_mu2[0, 0])),
    ]
    pole_diagnostic = 1.0 / (
        30240.0 * (4.0 * math.pi) ** 2 * constant**2
    )
    return {
        "raw_point_count": len(interacting),
        "cutoff_point_count": len(aggregates),
        "constant_c_m": constant,
        "constant_c_m_standard_error": constant_error,
        "constant_chi_squared_per_dof": constant_chi_squared / (len(y) - 1),
        "linear_mu_intercept": float(linear_mu[0]),
        "linear_mu_intercept_standard_error": math.sqrt(float(covariance_mu[0, 0])),
        "linear_mu_chi_squared_per_dof": chi_squared_mu / degrees_mu,
        "linear_mu2_intercept": float(linear_mu2[0]),
        "linear_mu2_intercept_standard_error": math.sqrt(float(covariance_mu2[0, 0])),
        "linear_mu2_chi_squared_per_dof": chi_squared_mu2 / degrees_mu2,
        "model_intercept_minimum": min(intercepts),
        "model_intercept_maximum": max(intercepts),
        "two_sigma_model_union_minimum": min(
            value - 2.0 * error
            for value, error in zip(intercepts, intercept_errors)
        ),
        "two_sigma_model_union_maximum": max(
            value + 2.0 * error
            for value, error in zip(intercepts, intercept_errors)
        ),
        "aggregate_c_m_minimum": float(np.min(y)),
        "aggregate_c_m_maximum": float(np.max(y)),
        "literal_trajectory_drift_resolved": constant_chi_squared
        > 9.0 * (len(y) - 1),
        "mass_gap_pilot_status": "PROMISING_NOT_PROMOTED",
        "single_free_pole_c6_diagnostic": pole_diagnostic,
        "single_free_pole_c6_is_result": False,
        "maximum_box_mu": maximum_box_mu,
        "minimum_mu_hat": minimum_mu_hat,
        "promotion_ready": False,
        "reason": "pilot has one finite-volume pair and one replicated cutoff but no mass-counterterm or alternative-discretization comparison",
    }


def finite_volume_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    interacting = [row for row in rows if row["branch"] == "literal_MTS"]
    comparisons: list[dict[str, Any]] = []
    for mu_hat in sorted({row["mu_hat"] for row in interacting}, reverse=True):
        same_cutoff = [row for row in interacting if row["mu_hat"] == mu_hat]
        sizes = sorted({row["size"] for row in same_cutoff})
        if len(sizes) < 2:
            continue
        small_size, large_size = sizes[0], sizes[-1]
        small = next(row for row in same_cutoff if row["size"] == small_size)
        large = next(row for row in same_cutoff if row["size"] == large_size)
        difference = large["c_m_lattice"] - small["c_m_lattice"]
        combined_error = math.hypot(
            large["c_m_standard_error"], small["c_m_standard_error"]
        )
        comparisons.append(
            {
                "mu_hat": mu_hat,
                "small_size": small_size,
                "large_size": large_size,
                "small_box_mu": small["box_mu"],
                "large_box_mu": large["box_mu"],
                "small_c_m": small["c_m_lattice"],
                "large_c_m": large["c_m_lattice"],
                "difference": difference,
                "combined_standard_error": combined_error,
                "difference_pull": difference / combined_error,
                "finite_volume_resolved": abs(difference) > 2.0 * combined_error,
            }
        )
    if not comparisons:
        comparisons.append(
            {
                "mu_hat": "not_available",
                "small_size": "not_available",
                "large_size": "not_available",
                "small_box_mu": "not_available",
                "large_box_mu": "not_available",
                "small_c_m": "not_available",
                "large_c_m": "not_available",
                "difference": "not_available",
                "combined_standard_error": "not_available",
                "difference_pull": "not_available",
                "finite_volume_resolved": "not_tested",
            }
        )
    return comparisons


def replicate_consistency_rows(rows: list[dict[str, Any]]) -> list[dict[str, Any]]:
    interacting = [row for row in rows if row["branch"] == "literal_MTS"]
    comparisons: list[dict[str, Any]] = []
    keys = sorted(
        {(row["mu_hat"], row["size"]) for row in interacting},
        reverse=True,
    )
    for mu_hat, size in keys:
        same = [
            row
            for row in interacting
            if row["mu_hat"] == mu_hat and row["size"] == size
        ]
        if len(same) < 2:
            continue
        first, second = same[0], same[1]
        difference = second["c_m_lattice"] - first["c_m_lattice"]
        combined_error = math.hypot(
            second["c_m_standard_error"], first["c_m_standard_error"]
        )
        comparisons.append(
            {
                "mu_hat": mu_hat,
                "size": size,
                "first_seed": first["seed"],
                "second_seed": second["seed"],
                "first_c_m": first["c_m_lattice"],
                "second_c_m": second["c_m_lattice"],
                "difference": difference,
                "combined_standard_error": combined_error,
                "difference_pull": difference / combined_error,
                "three_sigma_consistent": abs(difference)
                < 3.0 * combined_error,
            }
        )
    if not comparisons:
        comparisons.append(
            {
                "mu_hat": "not_available",
                "size": "not_available",
                "first_seed": "not_available",
                "second_seed": "not_available",
                "first_c_m": "not_available",
                "second_c_m": "not_available",
                "difference": "not_available",
                "combined_standard_error": "not_available",
                "difference_pull": "not_available",
                "three_sigma_consistent": "not_tested",
            }
        )
    return comparisons


def run(profile: str) -> dict[str, Any]:
    sources = source_contract()
    local_check = local_delta_validation()
    gaussian_check = gaussian_third_response_validation(
        samples=20_000 if profile == "smoke" else 120_000
    )
    distinct_check = gaussian_distinct_third_response_validation(
        samples=40_000 if profile == "smoke" else 240_000
    )
    seagull_check = densitized_metric_seagull_validation()
    Weyl_template = Weyl_cubic_template()
    summaries: list[dict[str, Any]] = []
    correlations: list[dict[str, Any]] = []
    for config in configurations(profile):
        summary, rows = run_lattice(config)
        summaries.append(summary)
        correlations.extend(rows)
        print(
            "branch={} N={} muhat={} am={:.6g}+/-{:.2g} cm={} acc={:.3f} tau={:.2f}".format(
                config.branch,
                config.size,
                config.mu_hat,
                summary["mass_gap_lattice"],
                summary["mass_gap_standard_error"],
                f'{summary["c_m_lattice"]:.6g}'
                if math.isfinite(summary["c_m_lattice"])
                else "not_applicable",
                summary["metropolis_acceptance"],
                summary["tau_zero_mode_observations"],
            )
        )
    aggregates = cutoff_aggregate_rows(summaries)
    extrapolation = extrapolation_summary(summaries, aggregates)
    volume_rows = finite_volume_rows(summaries)
    replicate_rows = replicate_consistency_rows(summaries)
    free_rows = [row for row in summaries if row["branch"] == "free_validation"]
    free_pass = bool(free_rows) and all(
        row["free_relative_error"] < (0.15 if profile == "smoke" else 0.08)
        for row in free_rows
    )
    interacting = [row for row in summaries if row["branch"] == "literal_MTS"]
    finite_results = all(
        math.isfinite(row["mass_gap_lattice"])
        and row["mass_gap_lattice"] > 0
        and row["metropolis_acceptance"] > 0.3
        for row in interacting
    )
    return {
        "profile": profile,
        "sources": sources,
        "scaling_rows": lattice_scaling_rows(),
        "local_delta_validation": local_check,
        "gaussian_third_response": gaussian_check,
        "gaussian_distinct_third_response": distinct_check,
        "densitized_metric_seagulls": seagull_check,
        "Weyl_cubic_template": Weyl_template,
        "summaries": summaries,
        "correlations": correlations,
        "cutoff_aggregates": aggregates,
        "extrapolation": extrapolation,
        "finite_volume_rows": volume_rows,
        "replicate_rows": replicate_rows,
        "stress_rows": stress_three_point_rows(),
        "free_validation_pass": free_pass,
        "interacting_finite": finite_results,
        "mass_gap_promoted": False,
        "c6_promoted": False,
        "Gamma_MTS_res": 0,
        "decision": "FINITE_LATTICE_MEASURE_AND_CONTINUUM_SCALING_DERIVED_CHECKERBOARD_SAMPLER_AND_CONNECTED_THIRD_RESPONSE_VALIDATED_LITERAL_MTS_MASS_GAP_PILOT_EXECUTED_BUT_VOLUME_COUNTERTERM_AND_TTT_WEYL_PROJECTION_NOT_CLOSED_CM_AND_C6_NOT_PROMOTED_ACTIVE_RESIDUAL_ZERO_PRIVATE_NONCLAIM",
        "next_target": NEXT_TARGET,
        "all_internal_checks_pass": sources["passed"]
        and local_check["passed"]
        and gaussian_check["passed"]
        and distinct_check["passed"]
        and seagull_check["passed"]
        and Weyl_template["passed"]
        and free_pass
        and finite_results,
    }


def write_outputs(result: dict[str, Any]) -> None:
    OUTPUT.mkdir(parents=True, exist_ok=True)
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4909_SOURCE_REGISTER.csv",
        tagged(result["sources"]["rows"]),
    )
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4909_LATTICE_SCALING.csv",
        tagged(result["scaling_rows"]),
    )
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4909_LOCAL_DELTA_VALIDATION.csv",
        tagged([result["local_delta_validation"]]),
    )
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4909_GAUSSIAN_THIRD_RESPONSE.csv",
        tagged([result["gaussian_third_response"]]),
    )
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4909_GAUSSIAN_DISTINCT_TTT.csv",
        tagged([result["gaussian_distinct_third_response"]]),
    )
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4909_DENSITIZED_SEAGULLS.csv",
        tagged([result["densitized_metric_seagulls"]]),
    )
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4909_WEYL_CUBIC_TEMPLATE.csv",
        tagged(result["Weyl_cubic_template"]["rows"]),
    )
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4909_MASS_GAP_RUNS.csv",
        tagged(result["summaries"]),
    )
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4909_CORRELATIONS.csv",
        tagged(result["correlations"]),
    )
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4909_CUTOFF_AGGREGATES.csv",
        tagged(result["cutoff_aggregates"]),
    )
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4909_EXTRAPOLATION.csv",
        tagged([result["extrapolation"]]),
    )
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4909_FINITE_VOLUME.csv",
        tagged(result["finite_volume_rows"]),
    )
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4909_REPLICATE_CONSISTENCY.csv",
        tagged(result["replicate_rows"]),
    )
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4909_STRESS_THREE_POINT_GATE.csv",
        tagged(result["stress_rows"]),
    )
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4909_DECISION.csv",
        tagged(
            [
                {
                    "profile": result["profile"],
                    "overall_decision": result["decision"],
                    "free_validation_pass": result["free_validation_pass"],
                    "interacting_finite": result["interacting_finite"],
                    "mass_gap_promoted": result["mass_gap_promoted"],
                    "c6_promoted": result["c6_promoted"],
                    "Gamma_MTS_res": result["Gamma_MTS_res"],
                    "next_target": result["next_target"],
                    "all_internal_checks_pass": result[
                        "all_internal_checks_pass"
                    ],
                }
            ]
        ),
    )
    manifest = {
        "marker": MARKER,
        "profile": result["profile"],
        "decision": result["decision"],
        "next_target": result["next_target"],
        "configs": [
            {
                key: value
                for key, value in row.items()
                if key
                in {
                    "branch",
                    "size",
                    "mu_hat",
                    "bare_mass",
                    "thermal_sweeps",
                    "observations",
                    "thin_sweeps",
                    "overrelax_sweeps",
                    "seed",
                }
            }
            for row in result["summaries"]
        ],
    }
    (OUTPUT / "P8_Y5_R2FR_4909_RUN_MANIFEST.json").write_text(
        json.dumps(manifest, indent=2) + "\n", encoding="utf-8"
    )


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--profile", choices=("smoke", "checkpoint", "long"), default="smoke"
    )
    args = parser.parse_args()
    result = run(args.profile)
    write_outputs(result)
    print(result["decision"])
    print(
        "local_delta={} gaussian_third={} gaussian_distinct={} seagulls={} Weyl_template={} free={} interacting={} cm_promoted={} c6_promoted={}".format(
            result["local_delta_validation"]["passed"],
            result["gaussian_third_response"]["passed"],
            result["gaussian_distinct_third_response"]["passed"],
            result["densitized_metric_seagulls"]["passed"],
            result["Weyl_cubic_template"]["passed"],
            result["free_validation_pass"],
            result["interacting_finite"],
            result["mass_gap_promoted"],
            result["c6_promoted"],
        )
    )
    return 0 if result["all_internal_checks_pass"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
