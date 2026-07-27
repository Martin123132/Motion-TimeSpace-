from __future__ import annotations

import argparse
import csv
import itertools
import json
import math
import time
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

import Y5_R2FR_4909_motion_scalar_lattice_gap_stress_three_point as checkpoint_4909
import Y5_R2FR_4911_full_offshell_a6_template_projector as checkpoint_4911
import Y5_R2FR_4912_free_lattice_multigeometry_continuum_projector as checkpoint_4912


ROOT = Path(__file__).resolve().parents[2]
POST = ROOT / "post-checkpoint-work"
FORMAL = ROOT / "formalization-workbench"
OUTPUT = POST / "source-intake" / "mts_residuals"

MARKER = "MTS_MATCHED_INTERACTING_TTT_SMOKE_4913"
FORMAL_MARKER = "PPC4161_MATCHED_INTERACTING_TTT_SMOKE_4913"
NEXT_TARGET = (
    "4914-Y5-R2FR-matched-interacting-TTT-replicates-cutoff-stencil-"
    "continuum-or-residual-demotion.md"
)
CHECKED_DATE = "2026-07-12"
DIMENSIONS = 4
SOURCE_STENCILS = ("site", "half_link")
TARGET_ZETA_M2 = checkpoint_4912.TARGET_ZETA_M2


@dataclass(frozen=True)
class InteractingConfig:
    label: str
    size: int
    mu_hat: float
    thermal_sweeps: int
    observations: int
    thin_sweeps: int
    overrelax_sweeps: int
    seed: int
    maximum_scale: int
    fit_degree: int
    free_pole_guess: float

    @property
    def coupling(self) -> float:
        return self.mu_hat ** (8.0 / 3.0)

    @property
    def volume(self) -> int:
        return self.size**DIMENSIONS


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


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle))


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


def configurations(profile: str) -> list[InteractingConfig]:
    if profile == "smoke":
        return [
            InteractingConfig(
                "N12_mu0p6_smoke", 12, 0.6, 180, 180, 1, 1, 491301, 3, 3, 0.68
            )
        ]
    if profile == "checkpoint":
        return [
            InteractingConfig(
                "N12_mu0p6", 12, 0.6, 400, 500, 2, 1, 491301, 3, 3, 0.65
            ),
            InteractingConfig(
                "N16_mu0p4", 16, 0.4, 550, 450, 2, 1, 491302, 4, 3, 0.42
            ),
        ]
    if profile == "long":
        return [
            InteractingConfig(
                "N16_mu0p4_rep1", 16, 0.4, 1800, 2500, 3, 2, 491311, 4, 3, 0.42
            ),
            InteractingConfig(
                "N16_mu0p4_rep2", 16, 0.4, 1800, 2500, 3, 2, 491312, 4, 3, 0.42
            ),
            InteractingConfig(
                "N20_mu0p3", 20, 0.3, 2200, 2200, 3, 2, 491313, 5, 3, 0.32
            ),
        ]
    raise ValueError(f"unknown profile: {profile}")


def load_geometric_matrix() -> tuple[list[str], np.ndarray]:
    return checkpoint_4912.load_geometric_matrix()


def fourier_projection(
    transform: np.ndarray,
    momenta: list[np.ndarray],
    phases: list[float],
) -> float:
    size = transform.shape[0]
    total = 0.0
    for signs in itertools.product((-1, 1), repeat=len(momenta)):
        momentum = sum(
            sign * vector for sign, vector in zip(signs, momenta)
        )
        phase = sum(sign * value for sign, value in zip(signs, phases))
        index = tuple(int(value) % size for value in momentum)
        total += float(np.real(np.exp(-1j * phase) * transform[index]))
    return total / 2.0 ** len(momenta)


def half_link_polarization(
    polarization: np.ndarray, physical_momentum: np.ndarray
) -> np.ndarray:
    factors = np.cos(physical_momentum / 2.0)
    return polarization * np.outer(factors, factors)


def source_plan(
    size: int,
    maximum_scale: int,
    ensemble: list[dict[str, Any]],
) -> dict[str, Any]:
    scales = np.arange(maximum_scale + 1, dtype=int)
    contacts: list[dict[str, Any]] = []
    for source in ensemble:
        first, pair, triple = checkpoint_4912.determinant_volume_derivatives(
            source["polarizations"]
        )
        contacts.append(
            {"first": first, "pair": pair, "triple": triple}
        )
    effective: dict[str, np.ndarray] = {}
    for stencil in SOURCE_STENCILS:
        values = np.empty(
            (
                len(ensemble),
                len(scales),
                3,
                DIMENSIONS,
                DIMENSIONS,
            ),
            dtype=float,
        )
        for geometry, source in enumerate(ensemble):
            for scale in scales:
                for source_index in range(3):
                    polarization = source["polarizations"][source_index]
                    if stencil == "half_link":
                        physical = (
                            2.0
                            * math.pi
                            * scale
                            / size
                            * source["momenta"][source_index]
                        )
                        polarization = half_link_polarization(
                            polarization, physical
                        )
                    values[geometry, scale, source_index] = polarization
        effective[stencil] = values
    return {
        "scales": scales,
        "contacts": contacts,
        "effective_polarizations": effective,
    }


def gradient_bilinear_transforms(field: np.ndarray) -> np.ndarray:
    forward = np.stack(
        [np.roll(field, -1, axis=axis) - field for axis in range(DIMENSIONS)]
    )
    backward = np.stack(
        [field - np.roll(field, 1, axis=axis) for axis in range(DIMENSIONS)]
    )
    transforms = np.empty(
        (DIMENSIONS, DIMENSIONS) + field.shape, dtype=np.complex128
    )
    for first in range(DIMENSIONS):
        for second in range(DIMENSIONS):
            density = 0.25 * (
                forward[first] * forward[second]
                + backward[first] * backward[second]
            )
            transforms[first, second] = np.fft.fftn(density)
    return transforms


def measure_source_observables(
    field: np.ndarray,
    coupling: float,
    mass_squared: float,
    ensemble: list[dict[str, Any]],
    plan: dict[str, Any],
) -> np.ndarray:
    size = field.shape[0]
    potential = (
        0.75 * coupling * np.abs(field) ** (4.0 / 3.0)
        + 0.5 * mass_squared * field**2
    )
    potential_transform = np.fft.fftn(potential)
    bilinear_transform = gradient_bilinear_transforms(field)
    result = np.empty(
        (
            len(SOURCE_STENCILS),
            len(ensemble),
            len(plan["scales"]),
            7,
        ),
        dtype=float,
    )
    for geometry, source in enumerate(ensemble):
        phases = [float(value) for value in source["phases"]]
        contact = plan["contacts"][geometry]
        for scale_index, scale in enumerate(plan["scales"]):
            integer_momenta = [
                np.asarray(scale * source["momenta"][index], dtype=int)
                for index in range(3)
            ]
            potential_first = [
                fourier_projection(
                    potential_transform,
                    [integer_momenta[index]],
                    [phases[index]],
                )
                for index in range(3)
            ]
            potential_pairs = {
                (0, 1): fourier_projection(
                    potential_transform,
                    [integer_momenta[0], integer_momenta[1]],
                    [phases[0], phases[1]],
                ),
                (0, 2): fourier_projection(
                    potential_transform,
                    [integer_momenta[0], integer_momenta[2]],
                    [phases[0], phases[2]],
                ),
                (1, 2): fourier_projection(
                    potential_transform,
                    [integer_momenta[1], integer_momenta[2]],
                    [phases[1], phases[2]],
                ),
            }
            potential_triple = fourier_projection(
                potential_transform, integer_momenta, phases
            )
            for stencil_index, stencil in enumerate(SOURCE_STENCILS):
                first_values: list[float] = []
                for source_index in range(3):
                    momentum = integer_momenta[source_index]
                    phase = phases[source_index]
                    index = tuple(int(value) % size for value in momentum)
                    polarization = plan["effective_polarizations"][stencil][
                        geometry, scale_index, source_index
                    ]
                    kinetic = float(
                        np.real(
                            np.exp(-1j * phase)
                            * np.einsum(
                                "mn,mn->",
                                polarization,
                                bilinear_transform[(slice(None), slice(None))
                                + index],
                            )
                        )
                    )
                    first_values.append(
                        kinetic
                        + float(contact["first"][source_index])
                        * potential_first[source_index]
                    )
                result[stencil_index, geometry, scale_index] = (
                    first_values[0],
                    first_values[1],
                    first_values[2],
                    float(contact["pair"][(0, 1)])
                    * potential_pairs[(0, 1)],
                    float(contact["pair"][(0, 2)])
                    * potential_pairs[(0, 2)],
                    float(contact["pair"][(1, 2)])
                    * potential_pairs[(1, 2)],
                    float(contact["triple"]) * potential_triple,
                )
    return result


def connected_response(observations: np.ndarray) -> np.ndarray:
    means = np.mean(observations, axis=0)
    centered_first = observations[..., :3] - means[..., :3]
    centered_pairs = observations[..., 3:6] - means[..., 3:6]
    return (
        means[..., 6]
        - np.mean(centered_first[..., 0] * centered_pairs[..., 2], axis=0)
        - np.mean(centered_first[..., 1] * centered_pairs[..., 1], axis=0)
        - np.mean(centered_first[..., 2] * centered_pairs[..., 0], axis=0)
        + np.mean(
            centered_first[..., 0]
            * centered_first[..., 1]
            * centered_first[..., 2],
            axis=0,
        )
    )


def analytic_cosine_channel_projection(
    response: np.ndarray, ensemble: list[dict[str, Any]]
) -> np.ndarray:
    projected = np.array(response, dtype=float, copy=True)
    for geometry, source in enumerate(ensemble):
        phases = np.asarray(source["phases"], dtype=float)
        denominator = 4.0 * float(np.prod(np.cos(phases)))
        if abs(denominator) < 1e-12:
            raise ValueError("zero-mode cosine channel has singular phase weight")
        projected[:, geometry, 0] *= float(np.cos(np.sum(phases))) / denominator
    return projected


def direct_coordinate_observables(
    field: np.ndarray,
    coupling: float,
    source: dict[str, Any],
    scale: int,
    stencil: str,
) -> np.ndarray:
    size = field.shape[0]
    coordinates = np.meshgrid(
        *[np.arange(size, dtype=float) for _ in range(DIMENSIONS)],
        indexing="ij",
    )
    forward = np.stack(
        [np.roll(field, -1, axis=axis) - field for axis in range(DIMENSIONS)]
    )
    backward = np.stack(
        [field - np.roll(field, 1, axis=axis) for axis in range(DIMENSIONS)]
    )
    bilinear = 0.25 * (
        np.einsum("m...,n...->mn...", forward, forward)
        + np.einsum("m...,n...->mn...", backward, backward)
    )
    potential = 0.75 * coupling * np.abs(field) ** (4.0 / 3.0)
    waves: list[np.ndarray] = []
    effective: list[np.ndarray] = []
    for source_index in range(3):
        integer = scale * source["momenta"][source_index]
        phase = np.full(field.shape, float(source["phases"][source_index]))
        for axis in range(DIMENSIONS):
            phase += 2.0 * math.pi * integer[axis] * coordinates[axis] / size
        waves.append(np.cos(phase))
        polarization = source["polarizations"][source_index]
        if stencil == "half_link":
            polarization = half_link_polarization(
                polarization, 2.0 * math.pi * integer / size
            )
        effective.append(polarization)
    first, pair, triple = checkpoint_4912.determinant_volume_derivatives(
        source["polarizations"]
    )
    first_values = [
        float(
            np.sum(
                waves[index]
                * (
                    np.einsum("mn,mn...->...", effective[index], bilinear)
                    + first[index] * potential
                )
            )
        )
        for index in range(3)
    ]
    return np.array(
        [
            *first_values,
            pair[(0, 1)] * np.sum(waves[0] * waves[1] * potential),
            pair[(0, 2)] * np.sum(waves[0] * waves[2] * potential),
            pair[(1, 2)] * np.sum(waves[1] * waves[2] * potential),
            triple * np.sum(waves[0] * waves[1] * waves[2] * potential),
        ],
        dtype=float,
    )


def observable_validation() -> list[dict[str, Any]]:
    rng = np.random.default_rng(491300)
    size = 4
    field = rng.normal(size=(size,) * DIMENSIONS)
    source = checkpoint_4911.random_source_ensemble(1)[0]
    ensemble = [source]
    plan = source_plan(size, 1, ensemble)
    fft_values = measure_source_observables(field, 0.37, 0.0, ensemble, plan)
    rows: list[dict[str, Any]] = []
    for stencil_index, stencil in enumerate(SOURCE_STENCILS):
        for scale in (0, 1):
            direct = direct_coordinate_observables(
                field, 0.37, source, scale, stencil
            )
            candidate = fft_values[stencil_index, 0, scale]
            residual = float(np.max(np.abs(candidate - direct)))
            rows.append(
                {
                    "stencil": stencil,
                    "scale": scale,
                    "maximum_absolute_residual": residual,
                    "acceptance": 2e-10,
                    "passed": residual < 2e-10,
                }
            )
    phases = np.asarray(source["phases"], dtype=float)
    raw_zero_mode = float(np.prod(np.cos(phases)))
    target_channel = 0.25 * float(np.cos(np.sum(phases)))
    projected_zero_mode = analytic_cosine_channel_projection(
        np.full((len(SOURCE_STENCILS), 1, 1), raw_zero_mode), ensemble
    )[0, 0, 0]
    rows.append(
        {
            "stencil": "analytic_zero_mode_channel",
            "scale": 0,
            "maximum_absolute_residual": abs(
                projected_zero_mode - target_channel
            ),
            "acceptance": 2e-14,
            "passed": abs(projected_zero_mode - target_channel) < 2e-14,
        }
    )
    return rows


def real_cosine_free_response(
    size: int,
    bare_mass: float,
    source: dict[str, Any],
    scale: int,
    source_stencil: str,
) -> float:
    if scale == 0:
        response = checkpoint_4912.complex_TTT_direct_density(
            size,
            source["momenta"],
            source["polarizations"],
            bare_mass,
            "nearest",
            0.0,
        )
        return 0.25 * float(
            np.cos(np.sum(source["phases"])) * response.real
        )
    physical_momenta = (
        2.0 * math.pi * scale / size * source["momenta"]
    )
    kinetic = source["polarizations"].copy()
    if source_stencil == "half_link":
        kinetic = np.stack(
            [
                half_link_polarization(
                    source["polarizations"][index],
                    physical_momenta[index],
                )
                for index in range(3)
            ]
        )
    response = checkpoint_4912.complex_TTT_direct_density(
        size,
        source["momenta"],
        source["polarizations"],
        bare_mass,
        "nearest",
        2.0 * math.pi * scale / size,
        kinetic_polarizations=kinetic,
    )
    return 0.25 * float(
        np.real(np.exp(1j * np.sum(source["phases"])) * response)
    )


def exact_free_response_grid(
    config: InteractingConfig,
    ensemble: list[dict[str, Any]],
    pole_mass: float,
) -> tuple[np.ndarray, float]:
    bare_mass = 2.0 * math.sinh(pole_mass / 2.0)
    values = np.empty(
        (
            len(SOURCE_STENCILS),
            len(ensemble),
            config.maximum_scale + 1,
        ),
        dtype=float,
    )
    start = time.perf_counter()
    for stencil_index, stencil in enumerate(SOURCE_STENCILS):
        for geometry, source in enumerate(ensemble):
            for scale in range(config.maximum_scale + 1):
                values[stencil_index, geometry, scale] = (
                    real_cosine_free_response(
                        config.size,
                        bare_mass,
                        source,
                        scale,
                        stencil,
                    )
                )
    return values, time.perf_counter() - start


def q6_design(config: InteractingConfig) -> tuple[np.ndarray, float, float]:
    scales = np.arange(config.maximum_scale + 1, dtype=float)
    momentum = 2.0 * math.pi * scales / config.size
    x = momentum**2
    design = np.vander(x, config.fit_degree + 1, increasing=True)
    if config.fit_degree < 3:
        raise ValueError("q6 extraction requires polynomial degree at least three")
    weights = np.linalg.pinv(design, rcond=1e-13)[3]
    return weights, float(np.linalg.cond(design)), float(np.linalg.norm(weights))


def q6_fit(response: np.ndarray, config: InteractingConfig) -> np.ndarray:
    weights, _, _ = q6_design(config)
    return np.einsum("...s,s->...", response, weights)


def correlated_quotient_recovery(
    matrix: np.ndarray,
    response: np.ndarray,
    covariance: np.ndarray,
) -> dict[str, Any]:
    column_norms = np.linalg.norm(matrix, axis=0)
    normalized = matrix / column_norms
    covariance = 0.5 * (covariance + covariance.T)
    eigenvalues, eigenvectors = np.linalg.eigh(covariance)
    positive = eigenvalues[eigenvalues > 0]
    floor = max(
        float(np.median(positive)) * 1e-6 if len(positive) else 1e-20,
        float(np.max(eigenvalues)) * 1e-10 if len(eigenvalues) else 1e-20,
        1e-30,
    )
    regularized = np.maximum(eigenvalues, floor)
    inverse_covariance = (
        eigenvectors * (1.0 / regularized)
    ) @ eigenvectors.T
    normal = normalized.T @ inverse_covariance @ normalized
    beta = (
        np.linalg.pinv(normal, rcond=1e-10)
        @ normalized.T
        @ inverse_covariance
        @ response
    )
    coefficients = beta / column_norms
    reconstructed = matrix @ coefficients
    residual = response - reconstructed
    zeta = float(checkpoint_4911.RICCI_FLAT_C3_MAP @ coefficients)
    return {
        "coefficients": coefficients,
        "reconstructed": reconstructed,
        "zeta": zeta,
        "euclidean_residual": float(
            np.linalg.norm(residual) / max(np.linalg.norm(response), 1e-30)
        ),
        "chi_squared": float(residual @ inverse_covariance @ residual),
        "covariance_floor": floor,
        "covariance_condition": float(
            np.max(regularized) / np.min(regularized)
        ),
    }


def paired_metropolis_sweep(
    interacting: np.ndarray,
    free: np.ndarray,
    parity: np.ndarray,
    coupling: float,
    free_mass_squared: float,
    step: float,
    rng: np.random.Generator,
) -> tuple[float, float, float]:
    accepted_interacting = 0
    accepted_free = 0
    accepted_together = 0
    total = 0
    for mask in (parity, ~parity):
        neighbors_interacting = checkpoint_4909.neighbor_sum(interacting)
        neighbors_free = checkpoint_4909.neighbor_sum(free)
        old_interacting = interacting[mask]
        old_free = free[mask]
        increment = rng.uniform(-step, step, size=old_interacting.shape)
        proposal_interacting = old_interacting + increment
        proposal_free = old_free + increment
        square_interacting = proposal_interacting**2 - old_interacting**2
        square_free = proposal_free**2 - old_free**2
        delta_interacting = (
            DIMENSIONS * square_interacting
            - (proposal_interacting - old_interacting)
            * neighbors_interacting[mask]
            + 0.75
            * coupling
            * (
                np.abs(proposal_interacting) ** (4.0 / 3.0)
                - np.abs(old_interacting) ** (4.0 / 3.0)
            )
        )
        delta_free = (
            DIMENSIONS * square_free
            - (proposal_free - old_free) * neighbors_free[mask]
            + 0.5 * free_mass_squared * square_free
        )
        log_uniform = np.log(rng.random(size=old_interacting.shape))
        keep_interacting = log_uniform < -delta_interacting
        keep_free = log_uniform < -delta_free
        updated_interacting = old_interacting.copy()
        updated_free = old_free.copy()
        updated_interacting[keep_interacting] = proposal_interacting[
            keep_interacting
        ]
        updated_free[keep_free] = proposal_free[keep_free]
        interacting[mask] = updated_interacting
        free[mask] = updated_free
        accepted_interacting += int(np.count_nonzero(keep_interacting))
        accepted_free += int(np.count_nonzero(keep_free))
        accepted_together += int(
            np.count_nonzero(keep_interacting & keep_free)
        )
        total += keep_interacting.size
    return (
        accepted_interacting / total,
        accepted_free / total,
        accepted_together / total,
    )


def paired_overrelaxation_sweep(
    interacting: np.ndarray,
    free: np.ndarray,
    parity: np.ndarray,
    coupling: float,
    free_mass_squared: float,
    rng: np.random.Generator,
) -> tuple[float, float]:
    accepted_interacting = 0
    total = 0
    for mask in (parity, ~parity):
        neighbors_interacting = checkpoint_4909.neighbor_sum(interacting)
        neighbors_free = checkpoint_4909.neighbor_sum(free)
        old_interacting = interacting[mask]
        old_free = free[mask]
        proposal_interacting = (
            2.0 * neighbors_interacting[mask] / (2.0 * DIMENSIONS)
            - old_interacting
        )
        proposal_free = (
            2.0
            * neighbors_free[mask]
            / (2.0 * DIMENSIONS + free_mass_squared)
            - old_free
        )
        delta_interacting = 0.75 * coupling * (
            np.abs(proposal_interacting) ** (4.0 / 3.0)
            - np.abs(old_interacting) ** (4.0 / 3.0)
        )
        keep_interacting = (
            np.log(rng.random(size=old_interacting.shape))
            < -delta_interacting
        )
        updated_interacting = old_interacting.copy()
        updated_interacting[keep_interacting] = proposal_interacting[
            keep_interacting
        ]
        interacting[mask] = updated_interacting
        free[mask] = proposal_free
        accepted_interacting += int(np.count_nonzero(keep_interacting))
        total += keep_interacting.size
    return accepted_interacting / total, 1.0


def run_interacting_chain(
    config: InteractingConfig,
    ensemble: list[dict[str, Any]],
    matrix_density: np.ndarray,
) -> dict[str, Any]:
    rng = np.random.default_rng(config.seed)
    shape = (config.size,) * DIMENSIONS
    interacting_field = np.zeros(shape, dtype=float)
    free_field = np.zeros(shape, dtype=float)
    parity = (np.indices(shape).sum(axis=0) & 1).astype(bool)
    step = 1.0
    plan = source_plan(config.size, config.maximum_scale, ensemble)
    free_bare_guess = 2.0 * math.sinh(config.free_pole_guess / 2.0)
    free_mass_squared = free_bare_guess**2
    thermal_acceptance: list[float] = []
    start = time.perf_counter()
    for sweep in range(config.thermal_sweeps):
        acceptance, free_acceptance, joint_acceptance = paired_metropolis_sweep(
            interacting_field,
            free_field,
            parity,
            config.coupling,
            free_mass_squared,
            step,
            rng,
        )
        for _ in range(config.overrelax_sweeps):
            paired_overrelaxation_sweep(
                interacting_field,
                free_field,
                parity,
                config.coupling,
                free_mass_squared,
                rng,
            )
        thermal_acceptance.append(acceptance)
        if (sweep + 1) % 50 == 0:
            recent = float(np.mean(thermal_acceptance[-50:]))
            if recent > 0.58:
                step *= 1.08
            elif recent < 0.42:
                step /= 1.08

    interacting_observations: list[np.ndarray] = []
    free_observations: list[np.ndarray] = []
    correlations: list[np.ndarray] = []
    zero_mode_squared: list[float] = []
    interacting_acceptance_rows: list[float] = []
    free_acceptance_rows: list[float] = []
    joint_acceptance_rows: list[float] = []
    interacting_overrelax_acceptance_rows: list[float] = []
    free_overrelax_acceptance_rows: list[float] = []
    field_correlations: list[float] = []
    for observation in range(config.observations):
        for _ in range(config.thin_sweeps):
            acceptance, free_acceptance, joint_acceptance = (
                paired_metropolis_sweep(
                    interacting_field,
                    free_field,
                    parity,
                    config.coupling,
                    free_mass_squared,
                    step,
                    rng,
                )
            )
            interacting_acceptance_rows.append(acceptance)
            free_acceptance_rows.append(free_acceptance)
            joint_acceptance_rows.append(joint_acceptance)
            for _ in range(config.overrelax_sweeps):
                (
                    interacting_overrelax_acceptance,
                    free_overrelax_acceptance,
                ) = paired_overrelaxation_sweep(
                    interacting_field,
                    free_field,
                    parity,
                    config.coupling,
                    free_mass_squared,
                    rng,
                )
                interacting_overrelax_acceptance_rows.append(
                    interacting_overrelax_acceptance
                )
                free_overrelax_acceptance_rows.append(
                    free_overrelax_acceptance
                )
        if rng.random() < 0.5:
            interacting_field *= -1.0
            free_field *= -1.0
        interacting_observations.append(
            measure_source_observables(
                interacting_field, config.coupling, 0.0, ensemble, plan
            )
        )
        free_observations.append(
            measure_source_observables(
                free_field, 0.0, free_mass_squared, ensemble, plan
            )
        )
        correlations.append(
            checkpoint_4909.measure_plane_correlation(interacting_field)
        )
        zero_mode_squared.append(float(np.mean(interacting_field) ** 2))
        centered_interacting = interacting_field - np.mean(interacting_field)
        centered_free = free_field - np.mean(free_field)
        denominator = math.sqrt(
            float(np.sum(centered_interacting**2) * np.sum(centered_free**2))
        )
        field_correlations.append(
            float(np.sum(centered_interacting * centered_free) / denominator)
            if denominator > 0
            else 0.0
        )
        if (observation + 1) % max(20, config.observations // 5) == 0:
            print(
                f"4913 {config.label} observation {observation + 1}/"
                f"{config.observations}",
                flush=True,
            )

    interacting_array = np.asarray(interacting_observations)
    free_array = np.asarray(free_observations)
    correlation_array = np.asarray(correlations)
    tau = checkpoint_4909.integrated_autocorrelation(
        np.asarray(zero_mode_squared)
    )
    mass_fit = checkpoint_4909.jackknife_mass(
        correlation_array, config.size, tau
    )
    pole_mass = float(mass_fit["mass"])
    pole_mass_error = float(mass_fit["mass_standard_error"])
    exact_free_guess, free_guess_elapsed = exact_free_response_grid(
        config, ensemble, config.free_pole_guess
    )
    exact_free_matched, free_matched_elapsed = exact_free_response_grid(
        config, ensemble, pole_mass
    )

    block_size = max(4, int(math.ceil(2.0 * tau)))
    block_count = config.observations // block_size
    if block_count < 8:
        block_size = max(1, config.observations // 8)
        block_count = config.observations // block_size
    used = block_count * block_size
    trimmed_interacting = interacting_array[:used]
    trimmed_free = free_array[:used]
    full_interacting = analytic_cosine_channel_projection(
        connected_response(trimmed_interacting) / config.volume, ensemble
    )
    full_sampled_free = analytic_cosine_channel_projection(
        connected_response(trimmed_free) / config.volume, ensemble
    )
    full_delta = full_interacting - exact_free_matched
    full_paired_delta = (
        full_interacting
        - full_sampled_free
        + exact_free_guess
        - exact_free_matched
    )
    full_q6 = q6_fit(full_delta, config)
    full_paired_q6 = q6_fit(full_paired_delta, config)

    jackknife_q6: list[np.ndarray] = []
    jackknife_paired_q6: list[np.ndarray] = []
    for block in range(block_count):
        keep = np.ones(used, dtype=bool)
        keep[block * block_size : (block + 1) * block_size] = False
        interacting = analytic_cosine_channel_projection(
            connected_response(trimmed_interacting[keep]) / config.volume,
            ensemble,
        )
        sampled_free = analytic_cosine_channel_projection(
            connected_response(trimmed_free[keep]) / config.volume,
            ensemble,
        )
        delta = interacting - exact_free_matched
        paired_delta = (
            interacting
            - sampled_free
            + exact_free_guess
            - exact_free_matched
        )
        jackknife_q6.append(q6_fit(delta, config))
        jackknife_paired_q6.append(q6_fit(paired_delta, config))
    jackknife_array = np.asarray(jackknife_q6)
    jackknife_paired_array = np.asarray(jackknife_paired_q6)

    covariance_rows: list[np.ndarray] = []
    paired_covariance_rows: list[np.ndarray] = []
    recovery: list[dict[str, Any]] = []
    for stencil_index, stencil in enumerate(SOURCE_STENCILS):
        samples = jackknife_array[:, stencil_index, :]
        centered = samples - np.mean(samples, axis=0)
        covariance = (
            (block_count - 1.0) / block_count * centered.T @ centered
        )
        covariance_rows.append(covariance)
        correlated = correlated_quotient_recovery(
            matrix_density, full_q6[stencil_index], covariance
        )
        jackknife_zeta = np.array(
            [
                correlated_quotient_recovery(
                    matrix_density, sample, covariance
                )["zeta"]
                for sample in samples
            ]
        )
        zeta_error = math.sqrt(
            (block_count - 1.0)
            / block_count
            * float(
                np.sum((jackknife_zeta - np.mean(jackknife_zeta)) ** 2)
            )
        )
        paired_samples = jackknife_paired_array[:, stencil_index, :]
        paired_centered = paired_samples - np.mean(paired_samples, axis=0)
        paired_covariance = (
            (block_count - 1.0)
            / block_count
            * paired_centered.T
            @ paired_centered
        )
        paired_covariance_rows.append(paired_covariance)
        paired_correlated = correlated_quotient_recovery(
            matrix_density,
            full_paired_q6[stencil_index],
            paired_covariance,
        )
        paired_jackknife_zeta = np.array(
            [
                correlated_quotient_recovery(
                    matrix_density, sample, paired_covariance
                )["zeta"]
                for sample in paired_samples
            ]
        )
        paired_zeta_error = math.sqrt(
            (block_count - 1.0)
            / block_count
            * float(
                np.sum(
                    (
                        paired_jackknife_zeta
                        - np.mean(paired_jackknife_zeta)
                    )
                    ** 2
                )
            )
        )
        renormalized = TARGET_ZETA_M2 / pole_mass**2 + correlated["zeta"]
        recovery.append(
            {
                "stencil": stencil,
                **correlated,
                "zeta_delta_standard_error": zeta_error,
                "zeta_renormalized": renormalized,
                "zeta_renormalized_times_mu2": renormalized
                * config.mu_hat**2,
                "zeta_delta_significance": correlated["zeta"]
                / zeta_error
                if zeta_error > 0
                else math.nan,
                "paired_control_zeta": paired_correlated["zeta"],
                "paired_control_zeta_standard_error": paired_zeta_error,
                "paired_over_primary_error": paired_zeta_error / zeta_error
                if zeta_error > 0
                else math.nan,
                "paired_control_euclidean_residual": paired_correlated[
                    "euclidean_residual"
                ],
            }
        )

    _, q6_design_condition, q6_weight_l2 = q6_design(config)
    return {
        "config": config,
        "summary": {
            **asdict(config),
            "coupling": config.coupling,
            "proposal_step": step,
            "mean_interacting_acceptance": float(
                np.mean(interacting_acceptance_rows)
            ),
            "mean_free_acceptance": float(np.mean(free_acceptance_rows)),
            "mean_joint_acceptance": float(np.mean(joint_acceptance_rows)),
            "mean_interacting_overrelax_acceptance": float(
                np.mean(interacting_overrelax_acceptance_rows)
            )
            if interacting_overrelax_acceptance_rows
            else math.nan,
            "mean_free_overrelax_acceptance": float(
                np.mean(free_overrelax_acceptance_rows)
            )
            if free_overrelax_acceptance_rows
            else math.nan,
            "mean_field_correlation": float(np.mean(field_correlations)),
            "tau_zero_mode_observations": tau,
            "block_size": block_size,
            "block_count": block_count,
            "used_observations": used,
            "pole_mass": pole_mass,
            "pole_mass_standard_error": pole_mass_error,
            "free_pole_guess": config.free_pole_guess,
            "free_bare_guess": free_bare_guess,
            "matched_free_bare_mass": 2.0 * math.sinh(pole_mass / 2.0),
            "q6_design_condition": q6_design_condition,
            "q6_weight_l2": q6_weight_l2,
            "analytic_zero_mode_channel_projected": True,
            "free_response_elapsed_seconds": free_guess_elapsed
            + free_matched_elapsed,
            "elapsed_seconds": time.perf_counter() - start,
        },
        "correlation": np.mean(correlation_array, axis=0),
        "interacting_response": full_interacting,
        "sampled_free_response": full_sampled_free,
        "exact_free_guess": exact_free_guess,
        "exact_free_matched": exact_free_matched,
        "delta_response": full_delta,
        "paired_delta_response": full_paired_delta,
        "q6": full_q6,
        "paired_q6": full_paired_q6,
        "jackknife_q6": jackknife_array,
        "paired_jackknife_q6": jackknife_paired_array,
        "covariances": covariance_rows,
        "paired_covariances": paired_covariance_rows,
        "recovery": recovery,
    }


def run(profile: str) -> dict[str, Any]:
    start = time.perf_counter()
    validation = observable_validation()
    geometry_ids, matrix_density = load_geometric_matrix()
    ensemble = checkpoint_4911.random_source_ensemble(len(geometry_ids))
    if [source["geometry_id"] for source in ensemble] != geometry_ids:
        raise RuntimeError("4911 source ensemble order mismatch")
    results = [
        run_interacting_chain(config, ensemble, matrix_density)
        for config in configurations(profile)
    ]
    return {
        "profile": profile,
        "validation": validation,
        "geometry_ids": geometry_ids,
        "results": results,
        "elapsed_seconds": time.perf_counter() - start,
    }


def write_outputs(result: dict[str, Any]) -> None:
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4913_OBSERVABLE_VALIDATION.csv",
        tagged(result["validation"]),
    )
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4913_CHAIN_SUMMARY.csv",
        tagged([item["summary"] for item in result["results"]]),
    )
    response_rows: list[dict[str, Any]] = []
    q6_rows: list[dict[str, Any]] = []
    covariance_rows: list[dict[str, Any]] = []
    recovery_rows: list[dict[str, Any]] = []
    correlation_rows: list[dict[str, Any]] = []
    for item in result["results"]:
        config = item["config"]
        scales = range(config.maximum_scale + 1)
        for stencil_index, stencil in enumerate(SOURCE_STENCILS):
            for geometry, geometry_id in enumerate(result["geometry_ids"]):
                for scale in scales:
                    response_rows.append(
                        {
                            "config": config.label,
                            "stencil": stencil,
                            "geometry_id": geometry_id,
                            "scale": scale,
                            "external_k": 2.0 * math.pi * scale / config.size,
                            "interacting_response_density": item[
                                "interacting_response"
                            ][stencil_index, geometry, scale],
                            "sampled_free_response_density": item[
                                "sampled_free_response"
                            ][stencil_index, geometry, scale],
                            "exact_free_guess_density": item[
                                "exact_free_guess"
                            ][stencil_index, geometry, scale],
                            "exact_free_matched_density": item[
                                "exact_free_matched"
                            ][stencil_index, geometry, scale],
                            "delta_response_density": item["delta_response"][
                                stencil_index, geometry, scale
                            ],
                            "paired_control_delta_response_density": item[
                                "paired_delta_response"
                            ][stencil_index, geometry, scale],
                        }
                    )
                q6_rows.append(
                    {
                        "config": config.label,
                        "stencil": stencil,
                        "geometry_id": geometry_id,
                        "q6_delta": item["q6"][stencil_index, geometry],
                        "q6_jackknife_mean": float(
                            np.mean(
                                item["jackknife_q6"][:, stencil_index, geometry]
                            )
                        ),
                        "q6_jackknife_standard_error": math.sqrt(
                            (item["summary"]["block_count"] - 1.0)
                            / item["summary"]["block_count"]
                            * float(
                                np.sum(
                                    (
                                        item["jackknife_q6"][:, stencil_index, geometry]
                                        - np.mean(
                                            item["jackknife_q6"][
                                                :, stencil_index, geometry
                                            ]
                                        )
                                    )
                                    ** 2
                                )
                            )
                        ),
                        "q6_paired_control": item["paired_q6"][
                            stencil_index, geometry
                        ],
                        "q6_paired_jackknife_mean": float(
                            np.mean(
                                item["paired_jackknife_q6"][
                                    :, stencil_index, geometry
                                ]
                            )
                        ),
                        "q6_paired_jackknife_standard_error": math.sqrt(
                            (item["summary"]["block_count"] - 1.0)
                            / item["summary"]["block_count"]
                            * float(
                                np.sum(
                                    (
                                        item["paired_jackknife_q6"][
                                            :, stencil_index, geometry
                                        ]
                                        - np.mean(
                                            item["paired_jackknife_q6"][
                                                :, stencil_index, geometry
                                            ]
                                        )
                                    )
                                    ** 2
                                )
                            )
                        ),
                    }
                )
            for estimator, covariance in (
                ("primary_exact_matched", item["covariances"][stencil_index]),
                (
                    "paired_control_diagnostic",
                    item["paired_covariances"][stencil_index],
                ),
            ):
                for first, first_id in enumerate(result["geometry_ids"]):
                    for second, second_id in enumerate(result["geometry_ids"]):
                        covariance_rows.append(
                            {
                                "config": config.label,
                                "stencil": stencil,
                                "estimator": estimator,
                                "geometry_i": first_id,
                                "geometry_j": second_id,
                                "covariance": covariance[first, second],
                            }
                        )
            recovered = item["recovery"][stencil_index]
            recovery_rows.append(
                {
                    "config": config.label,
                    "stencil": stencil,
                    **{
                        key: value
                        for key, value in recovered.items()
                        if key not in {"coefficients", "reconstructed"}
                    },
                }
            )
        for separation, value in enumerate(item["correlation"]):
            correlation_rows.append(
                {
                    "config": config.label,
                    "separation": separation,
                    "plane_correlation": float(value),
                }
            )
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4913_MATCHED_RESPONSES.csv",
        tagged(response_rows),
    )
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4913_Q6_DIFFERENCE.csv", tagged(q6_rows)
    )
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4913_Q6_COVARIANCE.csv",
        tagged(covariance_rows),
    )
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4913_PROJECTED_RECOVERY.csv",
        tagged(recovery_rows),
    )
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4913_CORRELATIONS.csv",
        tagged(correlation_rows),
    )
    write_csv(
        OUTPUT / "P8_Y5_R2FR_4913_RUN_STATUS.csv",
        tagged(
            [
                {
                    "profile": result["profile"],
                    "observable_validation_pass": all(
                        row["passed"] for row in result["validation"]
                    ),
                    "config_count": len(result["results"]),
                    "elapsed_seconds": result["elapsed_seconds"],
                    "next_target": NEXT_TARGET,
                }
            ]
        ),
    )


def write_run_state(run_directory: Path, state: dict[str, Any]) -> None:
    run_directory.mkdir(parents=True, exist_ok=True)
    (run_directory / "status.json").write_text(
        json.dumps(state, indent=2), encoding="utf-8"
    )


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--profile", choices=("smoke", "checkpoint", "long"), default="smoke"
    )
    parser.add_argument("--no-write", action="store_true")
    parser.add_argument("--run-directory", type=Path)
    return parser.parse_args()


def main() -> int:
    arguments = parse_args()
    if arguments.run_directory:
        write_run_state(
            arguments.run_directory,
            {
                "status": "RUNNING",
                "profile": arguments.profile,
                "started_unix": time.time(),
            },
        )
    try:
        result = run(arguments.profile)
        if not arguments.no_write:
            write_outputs(result)
        passed = all(row["passed"] for row in result["validation"])
        summaries = []
        for item in result["results"]:
            for recovered in item["recovery"]:
                summaries.append(
                    {
                        "config": item["config"].label,
                        "stencil": recovered["stencil"],
                        "zeta_delta": recovered["zeta"],
                        "zeta_delta_standard_error": recovered[
                            "zeta_delta_standard_error"
                        ],
                        "zeta_renormalized_times_mu2": recovered[
                            "zeta_renormalized_times_mu2"
                        ],
                        "euclidean_residual": recovered["euclidean_residual"],
                    }
                )
        if arguments.run_directory:
            write_run_state(
                arguments.run_directory,
                {
                    "status": "COMPLETE" if passed else "FAILED_GATE",
                    "profile": arguments.profile,
                    "elapsed_seconds": result["elapsed_seconds"],
                    "summary": summaries,
                },
            )
            if passed:
                (arguments.run_directory / "COMPLETE.marker").write_text(
                    "MTS_4913_COMPLETE\n", encoding="utf-8"
                )
        print(
            f"profile={arguments.profile} observable_validation={passed} "
            f"elapsed={result['elapsed_seconds']:.3f}s"
        )
        for item in result["results"]:
            print(
                f"{item['config'].label} mass={item['summary']['pole_mass']:.6g}"
                f"+/-{item['summary']['pole_mass_standard_error']:.2g} "
                f"tau={item['summary']['tau_zero_mode_observations']:.3g}"
            )
            for recovered in item["recovery"]:
                print(
                    f"  {recovered['stencil']} zeta_delta="
                    f"{recovered['zeta']:.6g}+/-"
                    f"{recovered['zeta_delta_standard_error']:.2g} "
                    f"sig={recovered['zeta_delta_significance']:.3g} "
                    f"res={recovered['euclidean_residual']:.3g}"
                )
        return 0 if passed else 1
    except Exception as error:
        if arguments.run_directory:
            write_run_state(
                arguments.run_directory,
                {
                    "status": "ERROR",
                    "profile": arguments.profile,
                    "error": repr(error),
                },
            )
        raise


if __name__ == "__main__":
    raise SystemExit(main())
