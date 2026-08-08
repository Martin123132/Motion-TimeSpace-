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
import scipy
import scipy.fft._realtransforms as scipy_realtransforms
import scipy.ndimage._interpolation as scipy_interpolation
from scipy.fft import dstn, idstn
from scipy.ndimage import map_coordinates


POST = Path(__file__).resolve().parents[1]
FORMAL = POST.parent / "formalization-workbench"
PREVIOUS_SCRIPT = (
    POST
    / "scripts"
    / "Y5_R2FR_5161_exact_shared_mode_particle_convergence_gate.py"
)
PREVIOUS_DOCUMENT = (
    POST
    / "5161-Y5-R2FR-exact-shared-mode-particle-resolution-convergence-gate.md"
)
PREVIOUS_RESULT = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5161"
    / "shared_mode_particle_convergence_results.json"
)
PREVIOUS_PHASE = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5161"
    / "exact_phase_matching_audit.csv"
)
OUT = POST / "source-intake" / "functional_rg" / "5162"
RESULT_JSON = OUT / "nested_transition_zoom_results.json"
CONTRACT_CSV = OUT / "nested_force_operator_contract.csv"
CONTROL_CSV = OUT / "nested_force_analytic_controls.csv"
INITIAL_CSV = OUT / "nested_zoom_initial_diagnostics.csv"
RUN_CSV = OUT / "nested_zoom_run_summary.csv"
PROFILE_CSV = OUT / "nested_zoom_profile_samples.csv"
SCORE_CSV = OUT / "nested_zoom_no_refit_scores.csv"
Q_CSV = OUT / "resolved_q_selection_gate.csv"
CONVERGENCE_CSV = OUT / "nested_grid_convergence_gate.csv"
BOUNDARY_CSV = OUT / "nested_boundary_silence_diagnostics.csv"
COG_CSV = OUT / "machine_cog_inheritance.csv"
PROVENANCE_CSV = OUT / "source_provenance.csv"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5162_VALIDATION.csv"
)
DOCUMENT = POST / "5162-Y5-R2FR-shared-mode-nested-transition-zoom-and-resolved-q-gate.md"

MARKER = "MTS_5162_SHARED_MODE_NESTED_TRANSITION_ZOOM_Q_GATE"
CHECKED_DATE = "2026-07-20"
FORMAL_DIGEST_LOCK = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)
MASS_LABEL = "benchmark_1e_minus20_eV"
REFERENCE_MAPPING = "Wetterich_v_equals_minus_2lambda"
PARTICLE_GRID = 96
GLOBAL_FORCE_GRID = 192
STEPS = 120
LOCAL_GRIDS = (128, 160)
PAIR_SIGNS = (-1, 1)
LOCAL_BOX_EDGE_MULTIPLE = 4.0
SOURCE_TAPER_START_EDGE = 1.5
SOURCE_TAPER_END_EDGE = 2.0
FORCE_TAPER_START_EDGE = 1.25
FORCE_TAPER_END_EDGE = 1.75
GAUSSIAN_FORCE_ERROR_TOLERANCE = 0.02
HOMOGENEOUS_CORRECTION_TOLERANCE = 1.0e-12
CENTER_JUMP_FRACTION_TOLERANCE = 0.25
CENTER_MAX_STEP_FRACTION = 0.125
BOUNDARY_SOURCE_RATIO_TOLERANCE = 0.01
Q_RESOLUTION_RELATIVE_TOLERANCE = 0.10
Q_PHASE_RELATIVE_TOLERANCE = 0.20
PROFILE_MASS_TOLERANCE = 0.10
PROFILE_VELOCITY_LOG_TOLERANCE = 0.10
PROFILE_DENSITY_LOG_TOLERANCE = 0.15


def load_previous_module() -> Any:
    specification = importlib.util.spec_from_file_location(
        "mts_checkpoint_5161", PREVIOUS_SCRIPT
    )
    if specification is None or specification.loader is None:
        raise RuntimeError("cannot load checkpoint-5161 module")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


PREVIOUS = load_previous_module()
PM = PREVIOUS.PREVIOUS
FFT_SOURCE = Path(scipy_realtransforms.__file__).resolve()
INTERPOLATION_SOURCE = Path(scipy_interpolation.__file__).resolve()


def file_digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def source_paths() -> dict[str, Path]:
    return {
        "previous_script": PREVIOUS_SCRIPT,
        "previous_document": PREVIOUS_DOCUMENT,
        "previous_result": PREVIOUS_RESULT,
        "previous_phase_audit": PREVIOUS_PHASE,
        "power_covariance": PM.POWER_CSV,
        "patch_covariance": PM.PATCH_CSV,
        "halo_targets": PM.HALO_CSV,
        "Eddington_targets": PM.EDDINGTON_CSV,
        "local_inheritance": PM.LOCAL_INHERITANCE_CSV,
        "scipy_DST_implementation": FFT_SOURCE,
        "scipy_interpolation_implementation": INTERPOLATION_SOURCE,
        "galaxy_samples_read_only": PM.GALAXY_SAMPLES,
    }


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    PM.write_csv(path, rows)


def write_json(path: Path, value: dict[str, Any]) -> None:
    PM.write_json(path, value)


def periodic_offset(
    position: np.ndarray, center: np.ndarray, box_size: float
) -> np.ndarray:
    return (position - center + 0.5 * box_size) % box_size - 0.5 * box_size


def cic_density_from_geometry(
    base: np.ndarray,
    fraction: np.ndarray,
    grid_size: int,
) -> np.ndarray:
    return PM.cic_density_contrast(base, fraction, grid_size)


def global_force_and_residual_density(
    positions: np.ndarray,
    reference_positions: np.ndarray,
    grid_size: int,
    box_size: float,
) -> tuple[np.ndarray, np.ndarray, dict[str, float]]:
    base, fraction = PM.cic_geometry(positions, grid_size, box_size)
    density = cic_density_from_geometry(base, fraction, grid_size)
    reference_base, reference_fraction = PM.cic_geometry(
        reference_positions, grid_size, box_size
    )
    reference_density = cic_density_from_geometry(
        reference_base, reference_fraction, grid_size
    )
    density_fourier = np.fft.rfftn(density)
    _, _, _, squared = PM.fourier_grid(grid_size, box_size)
    potential_fourier = np.zeros_like(density_fourier)
    nonzero = squared > 0.0
    potential_fourier[nonzero] = (
        -1.5
        * PM.OMEGA_M
        * density_fourier[nonzero]
        / squared[nonzero]
    )
    potential = np.fft.irfftn(
        potential_fourier, s=density.shape, axes=(0, 1, 2)
    )
    spacing = box_size / grid_size
    force = np.empty_like(positions)
    for axis in range(3):
        component = -(
            np.roll(potential, -1, axis=axis)
            - np.roll(potential, 1, axis=axis)
        ) / (2.0 * spacing)
        force[:, axis] = PM.cic_interpolate(
            component, base, fraction
        )
    diagnostics = {
        "density_mean": float(np.mean(density)),
        "density_minimum": float(np.min(density)),
        "density_maximum": float(np.max(density)),
        "force_mean_norm": float(np.linalg.norm(np.mean(force, axis=0))),
        "force_maximum_norm": float(
            np.max(np.linalg.norm(force, axis=1))
        ),
    }
    return force, density - reference_density, diagnostics


def local_cic_counts(
    offsets: np.ndarray, local_box: float, grid_size: int
) -> tuple[np.ndarray, int]:
    spacing = local_box / grid_size
    inside = np.all(np.abs(offsets) < 0.5 * local_box, axis=1)
    selected = offsets[inside]
    scaled = (selected + 0.5 * local_box) / spacing - 0.5
    base = np.floor(scaled).astype(np.int64)
    fraction = scaled - base
    counts = np.zeros(grid_size**3, dtype=float)
    for offset_x in (0, 1):
        weight_x = fraction[:, 0] if offset_x else 1.0 - fraction[:, 0]
        index_x = base[:, 0] + offset_x
        for offset_y in (0, 1):
            weight_y = fraction[:, 1] if offset_y else 1.0 - fraction[:, 1]
            index_y = base[:, 1] + offset_y
            for offset_z in (0, 1):
                weight_z = (
                    fraction[:, 2] if offset_z else 1.0 - fraction[:, 2]
                )
                index_z = base[:, 2] + offset_z
                valid = (
                    (index_x >= 0)
                    & (index_x < grid_size)
                    & (index_y >= 0)
                    & (index_y < grid_size)
                    & (index_z >= 0)
                    & (index_z < grid_size)
                )
                flat = (
                    (index_x[valid] * grid_size + index_y[valid])
                    * grid_size
                    + index_z[valid]
                )
                counts += np.bincount(
                    flat,
                    weights=(
                        weight_x[valid]
                        * weight_y[valid]
                        * weight_z[valid]
                    ),
                    minlength=grid_size**3,
                )
    return counts.reshape((grid_size, grid_size, grid_size)), int(
        np.count_nonzero(inside)
    )


def cosine_taper(
    values: np.ndarray, start: float, end: float
) -> np.ndarray:
    absolute = np.abs(values)
    result = np.ones_like(absolute)
    middle = (absolute > start) & (absolute < end)
    result[absolute >= end] = 0.0
    result[middle] = 0.5 * (
        1.0
        + np.cos(math.pi * (absolute[middle] - start) / (end - start))
    )
    return result


def local_source_window(
    grid_size: int, local_box: float, edge_radius: float
) -> tuple[np.ndarray, np.ndarray]:
    spacing = local_box / grid_size
    axis = (np.arange(grid_size, dtype=float) + 0.5) * spacing - 0.5 * local_box
    one_dimensional = cosine_taper(
        axis,
        SOURCE_TAPER_START_EDGE * edge_radius,
        SOURCE_TAPER_END_EDGE * edge_radius,
    )
    window = (
        one_dimensional[:, None, None]
        * one_dimensional[None, :, None]
        * one_dimensional[None, None, :]
    )
    return axis, window


def solve_dirichlet_poisson(
    source: np.ndarray, spacing: float
) -> tuple[np.ndarray, np.ndarray]:
    grid_size = source.shape[0]
    source_hat = dstn(source, type=2, norm="ortho")
    mode = np.arange(grid_size, dtype=float)
    eigenvalue_1d = (
        -4.0
        * np.sin(math.pi * (mode + 1.0) / (2.0 * grid_size)) ** 2
        / spacing**2
    )
    eigenvalue = (
        eigenvalue_1d[:, None, None]
        + eigenvalue_1d[None, :, None]
        + eigenvalue_1d[None, None, :]
    )
    potential = idstn(
        1.5 * PM.OMEGA_M * source_hat / eigenvalue,
        type=2,
        norm="ortho",
    )
    force = np.stack(
        [-component for component in np.gradient(potential, spacing, edge_order=2)]
    )
    return potential, force


def sample_periodic_grid_on_local_cells(
    grid: np.ndarray,
    center: np.ndarray,
    axis: np.ndarray,
    box_size: float,
) -> np.ndarray:
    grid_size = grid.shape[0]
    coordinates_1d = [
        ((center[dimension] + axis) % box_size)
        * grid_size
        / box_size
        for dimension in range(3)
    ]
    coordinates = np.array(
        np.meshgrid(*coordinates_1d, indexing="ij")
    )
    return map_coordinates(
        grid, coordinates, order=1, mode="wrap"
    )


def sample_local_vector(
    field: np.ndarray,
    offsets: np.ndarray,
    local_box: float,
) -> np.ndarray:
    grid_size = field.shape[1]
    spacing = local_box / grid_size
    coordinates = ((offsets + 0.5 * local_box) / spacing - 0.5).T
    return np.column_stack(
        [
            map_coordinates(
                field[component],
                coordinates,
                order=1,
                mode="nearest",
            )
            for component in range(3)
        ]
    )


def nested_force(
    positions: np.ndarray,
    lagrangian_positions: np.ndarray,
    tagged: np.ndarray,
    particle_grid: int,
    global_force_grid: int,
    local_grid: int,
    box_size: float,
    edge_radius: float,
    tracked_center: np.ndarray | None = None,
) -> tuple[np.ndarray, dict[str, Any]]:
    local_box = LOCAL_BOX_EDGE_MULTIPLE * edge_radius
    candidate_center, center_iterations = PM.shrinking_center(
        positions[tagged], box_size
    )
    candidate_jump = 0.0
    applied_center_step = 0.0
    center_limited = False
    if tracked_center is None:
        center = candidate_center
    else:
        center_delta = periodic_offset(
            candidate_center, tracked_center, box_size
        )
        candidate_jump = float(np.linalg.norm(center_delta))
        maximum_step = CENTER_MAX_STEP_FRACTION * local_box
        if candidate_jump > maximum_step:
            center_delta *= maximum_step / candidate_jump
            center_limited = True
        center = (tracked_center + center_delta) % box_size
        applied_center_step = float(np.linalg.norm(center_delta))
    bulk_shift = np.mean(
        periodic_offset(
            positions[tagged], lagrangian_positions[tagged], box_size
        ),
        axis=0,
    )
    reference_positions = (lagrangian_positions + bulk_shift) % box_size
    global_force, global_residual_density, global_diagnostics = (
        global_force_and_residual_density(
            positions,
            reference_positions,
            global_force_grid,
            box_size,
        )
    )
    actual_offsets = periodic_offset(positions, center, box_size)
    reference_offsets = periodic_offset(
        reference_positions, center, box_size
    )
    actual_counts, actual_source_count = local_cic_counts(
        actual_offsets, local_box, local_grid
    )
    reference_counts, reference_source_count = local_cic_counts(
        reference_offsets, local_box, local_grid
    )
    spacing = local_box / local_grid
    particle_volume = (box_size / particle_grid) ** 3
    fine_density_contrast = (
        actual_counts - reference_counts
    ) * particle_volume / spacing**3
    axis, source_window = local_source_window(
        local_grid, local_box, edge_radius
    )
    coarse_density_local = sample_periodic_grid_on_local_cells(
        global_residual_density, center, axis, box_size
    )
    expected_particles_per_fine_cell = (
        spacing / (box_size / particle_grid)
    ) ** 3 * np.maximum(1.0 + coarse_density_local, 0.0)
    sampling_weight = expected_particles_per_fine_cell / (
        1.0 + expected_particles_per_fine_cell
    )
    residual_source = (
        fine_density_contrast - coarse_density_local
    ) * source_window * sampling_weight
    _, correction_grid = solve_dirichlet_poisson(
        residual_source, spacing
    )
    radii = np.linalg.norm(actual_offsets, axis=1)
    active = radii < FORCE_TAPER_END_EDGE * edge_radius
    active_offsets = actual_offsets[active]
    correction = sample_local_vector(
        correction_grid, active_offsets, local_box
    )
    weights = cosine_taper(
        radii[active],
        FORCE_TAPER_START_EDGE * edge_radius,
        FORCE_TAPER_END_EDGE * edge_radius,
    )
    weighted_mean = np.sum(weights[:, None] * correction, axis=0) / np.sum(
        weights
    )
    weighted_correction = weights[:, None] * (
        correction - weighted_mean
    )
    total_force = global_force.copy()
    total_force[active] += weighted_correction
    boundary_values = np.concatenate(
        [
            residual_source[0].ravel(),
            residual_source[-1].ravel(),
            residual_source[:, 0].ravel(),
            residual_source[:, -1].ravel(),
            residual_source[:, :, 0].ravel(),
            residual_source[:, :, -1].ravel(),
        ]
    )
    source_maximum = float(np.max(np.abs(residual_source)))
    boundary_ratio = (
        float(np.max(np.abs(boundary_values))) / source_maximum
        if source_maximum > 0.0
        else 0.0
    )
    diagnostics = {
        **global_diagnostics,
        "center_Mpc": center,
        "candidate_center_Mpc": candidate_center,
        "center_iterations": center_iterations,
        "candidate_center_jump_Mpc": candidate_jump,
        "applied_center_step_Mpc": applied_center_step,
        "center_step_limited": center_limited,
        "actual_local_source_particles": actual_source_count,
        "reference_local_source_particles": reference_source_count,
        "active_correction_particles": int(np.count_nonzero(active)),
        "fine_density_contrast_RMS": float(
            np.sqrt(np.mean(fine_density_contrast**2))
        ),
        "coarse_density_local_RMS": float(
            np.sqrt(np.mean(coarse_density_local**2))
        ),
        "residual_source_RMS": float(
            np.sqrt(np.mean(residual_source**2))
        ),
        "sampling_weight_mean": float(np.mean(sampling_weight)),
        "sampling_weight_maximum": float(np.max(sampling_weight)),
        "residual_source_boundary_ratio": boundary_ratio,
        "correction_force_maximum": float(
            np.max(np.linalg.norm(weighted_correction, axis=1))
        )
        if len(weighted_correction)
        else 0.0,
        "correction_force_RMS": float(
            np.sqrt(
                np.mean(
                    np.sum(weighted_correction * weighted_correction, axis=1)
                )
            )
        )
        if len(weighted_correction)
        else 0.0,
        "correction_force_sum_norm": float(
            np.linalg.norm(np.sum(weighted_correction, axis=0))
        ),
        "total_force_mean_norm": float(
            np.linalg.norm(np.mean(total_force, axis=0))
        ),
        "local_spacing_Mpc": spacing,
        "local_box_Mpc": local_box,
    }
    return total_force, diagnostics


def evolve_nested(
    positions: np.ndarray,
    momenta: np.ndarray,
    lagrangian_positions: np.ndarray,
    tagged: np.ndarray,
    particle_grid: int,
    local_grid: int,
    box_size: float,
    edge_radius: float,
) -> dict[str, Any]:
    positions = positions.copy()
    momenta = momenta.copy()
    scale_factors = np.geomspace(PM.A_INITIAL, 1.0, STEPS + 1)
    lower = scale_factors[:-1]
    upper = scale_factors[1:]
    midpoint = np.sqrt(lower * upper)
    drifts = PM.PREVIOUS.integration_factors(lower, upper, 3)
    first_half = PM.PREVIOUS.integration_factors(
        np.array([lower[0]]), np.array([midpoint[0]]), 2
    )[0]
    between = PM.PREVIOUS.integration_factors(
        midpoint[:-1], midpoint[1:], 2
    )
    final_half = PM.PREVIOUS.integration_factors(
        np.array([midpoint[-1]]), np.array([upper[-1]]), 2
    )[0]
    start = time.perf_counter()
    force, diagnostics = nested_force(
        positions,
        lagrangian_positions,
        tagged,
        particle_grid,
        GLOBAL_FORCE_GRID,
        local_grid,
        box_size,
        edge_radius,
    )
    initial_diagnostics = diagnostics
    previous_center = np.asarray(diagnostics["center_Mpc"], dtype=float)
    maximum_center_jump = 0.0
    maximum_candidate_center_jump = 0.0
    center_limited_steps = 0
    maximum_boundary_ratio = float(
        diagnostics["residual_source_boundary_ratio"]
    )
    maximum_correction_sum = float(
        diagnostics["correction_force_sum_norm"]
    )
    half_momenta = momenta + first_half * force
    final_diagnostics = diagnostics
    for index in range(STEPS):
        positions = (positions + drifts[index] * half_momenta) % box_size
        force, final_diagnostics = nested_force(
            positions,
            lagrangian_positions,
            tagged,
            particle_grid,
            GLOBAL_FORCE_GRID,
            local_grid,
            box_size,
            edge_radius,
            previous_center,
        )
        center = np.asarray(final_diagnostics["center_Mpc"], dtype=float)
        jump = float(final_diagnostics["applied_center_step_Mpc"])
        maximum_center_jump = max(maximum_center_jump, jump)
        maximum_candidate_center_jump = max(
            maximum_candidate_center_jump,
            float(final_diagnostics["candidate_center_jump_Mpc"]),
        )
        center_limited_steps += int(
            bool(final_diagnostics["center_step_limited"])
        )
        previous_center = center
        maximum_boundary_ratio = max(
            maximum_boundary_ratio,
            float(final_diagnostics["residual_source_boundary_ratio"]),
        )
        maximum_correction_sum = max(
            maximum_correction_sum,
            float(final_diagnostics["correction_force_sum_norm"]),
        )
        if index < STEPS - 1:
            half_momenta += between[index] * force
        else:
            momenta = half_momenta + final_half * force
    return {
        "positions": positions,
        "momenta": momenta,
        "wall_seconds": time.perf_counter() - start,
        "initial_diagnostics": initial_diagnostics,
        "final_diagnostics": final_diagnostics,
        "maximum_center_jump_Mpc": maximum_center_jump,
        "maximum_candidate_center_jump_Mpc": maximum_candidate_center_jump,
        "center_limited_steps": center_limited_steps,
        "final_tracked_center_Mpc": previous_center,
        "maximum_boundary_source_ratio": maximum_boundary_ratio,
        "maximum_correction_force_sum_norm": maximum_correction_sum,
    }


def zoom_profile(
    positions: np.ndarray,
    tagged: np.ndarray,
    particle_grid: int,
    local_grid: int,
    box_size: float,
    edge_radius: float,
) -> dict[str, Any]:
    center, center_iterations = PM.shrinking_center(
        positions[tagged], box_size
    )
    offsets = periodic_offset(positions, center, box_size)
    radii = np.linalg.norm(offsets, axis=1)
    particle_mass = PM.RHO_M_MSUN_MPC3 * box_size**3 / particle_grid**3
    local_spacing = LOCAL_BOX_EDGE_MULTIPLE * edge_radius / local_grid
    minimum = 0.5 * local_spacing
    maximum = 0.49 * box_size
    edges = np.geomspace(minimum, maximum, PM.PROFILE_BINS + 1)
    centers = np.sqrt(edges[:-1] * edges[1:])
    counts = np.histogram(radii, bins=edges)[0]
    volumes = 4.0 * math.pi * (edges[1:] ** 3 - edges[:-1] ** 3) / 3.0
    total_density = counts * particle_mass / volumes
    excess_density = total_density - PM.RHO_M_MSUN_MPC3
    sorted_radii = np.sort(radii)
    cumulative_counts = np.searchsorted(sorted_radii, centers, side="right")
    total_mass = cumulative_counts * particle_mass
    background_mass = (
        4.0 * math.pi * PM.RHO_M_MSUN_MPC3 * centers**3 / 3.0
    )
    excess_mass = total_mass - background_mass
    motion_mass = PM.MOTION_FRACTION * np.maximum(excess_mass, 0.0)
    velocity_squared = PM.G_MPC_KM2_S2_MSUN * motion_mass / centers
    return {
        "center_Mpc": center,
        "center_iterations": center_iterations,
        "radius_Mpc": centers,
        "particle_count": counts,
        "total_density_Msun_Mpc3": total_density,
        "excess_density_total_Msun_Mpc3": excess_density,
        "total_mass_Msun": total_mass,
        "excess_mass_total_Msun": excess_mass,
        "motion_excess_mass_Msun": motion_mass,
        "motion_velocity_squared_km2_s2": velocity_squared,
        "force_spacing_Mpc": local_spacing,
        "resolved_radius_Mpc": PM.RESOLVED_FORCE_CELLS * local_spacing,
        "particle_mass_Msun": particle_mass,
        "tagged_particle_count": int(np.count_nonzero(tagged)),
    }


def run_nested_configuration(
    config_id: str,
    pair_sign: int,
    local_grid: int,
    box_size: float,
    patch_radius: float,
    edge_radius: float,
    initial: dict[str, Any],
    lagrangian_positions: np.ndarray,
) -> dict[str, Any]:
    evolved = evolve_nested(
        np.asarray(initial["positions"], dtype=float),
        np.asarray(initial["momenta"], dtype=float),
        lagrangian_positions,
        np.asarray(initial["tagged"], dtype=bool),
        PARTICLE_GRID,
        local_grid,
        box_size,
        edge_radius,
    )
    profile = zoom_profile(
        np.asarray(evolved["positions"], dtype=float),
        np.asarray(initial["tagged"], dtype=bool),
        PARTICLE_GRID,
        local_grid,
        box_size,
        edge_radius,
    )
    center = np.asarray(profile["center_Mpc"], dtype=float)
    final_tracked_center = np.asarray(
        evolved["final_tracked_center_Mpc"], dtype=float
    )
    final_center_tracking_residual = float(
        np.linalg.norm(
            periodic_offset(center, final_tracked_center, box_size)
        )
    )
    particle_mass = float(profile["particle_mass_Msun"])
    inner_density = PM.direct_annulus_density(
        np.asarray(evolved["positions"]),
        center,
        box_size,
        particle_mass,
        0.70 * edge_radius,
        0.90 * edge_radius,
    )
    outer_density = PM.direct_annulus_density(
        np.asarray(evolved["positions"]),
        center,
        box_size,
        particle_mass,
        1.05 * edge_radius,
        1.30 * edge_radius,
    )
    final_diagnostics = evolved["final_diagnostics"]
    return {
        "config_id": config_id,
        "mass_label": MASS_LABEL,
        "pair_sign": pair_sign,
        "particle_grid": PARTICLE_GRID,
        "global_force_grid": GLOBAL_FORCE_GRID,
        "local_force_grid": local_grid,
        "steps": STEPS,
        "box_size_Mpc": box_size,
        "patch_radius_Mpc": patch_radius,
        "local_box_Mpc": LOCAL_BOX_EDGE_MULTIPLE * edge_radius,
        "particle_count": PARTICLE_GRID**3,
        "local_force_cell_kpc": (
            1000.0 * LOCAL_BOX_EDGE_MULTIPLE * edge_radius / local_grid
        ),
        "resolved_radius_kpc": 1000.0
        * float(profile["resolved_radius_Mpc"]),
        "tagged_particle_count": int(profile["tagged_particle_count"]),
        "wall_seconds": float(evolved["wall_seconds"]),
        "maximum_center_jump_Mpc": evolved["maximum_center_jump_Mpc"],
        "maximum_candidate_center_jump_Mpc": evolved[
            "maximum_candidate_center_jump_Mpc"
        ],
        "center_limited_steps": evolved["center_limited_steps"],
        "final_center_tracking_residual_Mpc": final_center_tracking_residual,
        "maximum_boundary_source_ratio": evolved[
            "maximum_boundary_source_ratio"
        ],
        "maximum_correction_force_sum_norm": evolved[
            "maximum_correction_force_sum_norm"
        ],
        "final_total_force_mean_norm": final_diagnostics[
            "total_force_mean_norm"
        ],
        "final_correction_force_maximum": final_diagnostics[
            "correction_force_maximum"
        ],
        "final_correction_force_RMS": final_diagnostics[
            "correction_force_RMS"
        ],
        "final_actual_local_source_particles": final_diagnostics[
            "actual_local_source_particles"
        ],
        "halo_center_x_Mpc": center[0],
        "halo_center_y_Mpc": center[1],
        "halo_center_z_Mpc": center[2],
        "inner_edge_excess_density_total_Msun_Mpc3": inner_density,
        "outer_edge_excess_density_total_Msun_Mpc3": outer_density,
        "outer_to_inner_excess_density_ratio": outer_density / inner_density
        if inner_density > 0.0
        else math.nan,
        "profile": profile,
    }


def gaussian_force_control(
    grid_size: int, local_box: float
) -> dict[str, Any]:
    spacing = local_box / grid_size
    sigma = 0.06
    axis = (
        np.arange(grid_size, dtype=float) + 0.5
    ) * spacing - 0.5 * local_box
    x, y, z = np.meshgrid(axis, axis, axis, indexing="ij")
    radius = np.sqrt(x * x + y * y + z * z)
    source = np.exp(-radius**2 / (2.0 * sigma**2))
    _, force = solve_dirichlet_poisson(source, spacing)
    middle = grid_size // 2
    radial = axis[middle:]
    numerical = np.abs(force[0, middle:, middle, middle])
    integral = (
        math.sqrt(math.pi / 2.0)
        * sigma**3
        * np.array(
            [
                math.erf(value / (math.sqrt(2.0) * sigma))
                for value in radial
            ]
        )
        - sigma**2
        * radial
        * np.exp(-radial**2 / (2.0 * sigma**2))
    )
    analytic = 1.5 * PM.OMEGA_M * integral / radial**2
    valid = (radial >= 3.0 * spacing) & (radial <= 0.25 * local_box)
    relative = np.abs(numerical[valid] / analytic[valid] - 1.0)
    return {
        "control_id": f"Gaussian_Dirichlet_force_grid_{grid_size}",
        "measured_maximum_relative_error": float(np.max(relative)),
        "measured_median_relative_error": float(np.median(relative)),
        "tolerance": GAUSSIAN_FORCE_ERROR_TOLERANCE,
        "status": "PASS"
        if float(np.max(relative)) < GAUSSIAN_FORCE_ERROR_TOLERANCE
        else "FAIL",
        "valid_for_claim": False,
        "checkpoint_marker": MARKER,
    }


def homogeneous_nested_control(
    edge_radius: float,
) -> dict[str, Any]:
    particle_grid = 32
    global_grid = 64
    local_grid = 48
    box_size = 10.0
    lagrangian = PM.particle_lattice(particle_grid, box_size)
    center = np.full(3, 0.5 * box_size)
    tagged = (
        np.linalg.norm(
            periodic_offset(lagrangian, center, box_size), axis=1
        )
        <= 2.5
    )
    force, diagnostics = nested_force(
        lagrangian,
        lagrangian,
        tagged,
        particle_grid,
        global_grid,
        local_grid,
        box_size,
        edge_radius,
    )
    maximum = float(np.max(np.linalg.norm(force, axis=1)))
    return {
        "control_id": "homogeneous_lattice_nested_force",
        "measured_maximum_absolute_force": maximum,
        "measured_correction_force_maximum": diagnostics[
            "correction_force_maximum"
        ],
        "tolerance": HOMOGENEOUS_CORRECTION_TOLERANCE,
        "status": "PASS"
        if maximum < HOMOGENEOUS_CORRECTION_TOLERANCE
        else "FAIL",
        "valid_for_claim": False,
        "checkpoint_marker": MARKER,
    }


def control_rows(edge_radius: float) -> list[dict[str, Any]]:
    local_box = LOCAL_BOX_EDGE_MULTIPLE * edge_radius
    rows = [
        gaussian_force_control(LOCAL_GRIDS[0], local_box),
        gaussian_force_control(LOCAL_GRIDS[1], local_box),
        homogeneous_nested_control(edge_radius),
    ]
    rows.append(
        {
            "control_id": "source_and_force_tapers",
            "source_taper_start_Redge": SOURCE_TAPER_START_EDGE,
            "source_taper_end_Redge": SOURCE_TAPER_END_EDGE,
            "force_taper_start_Redge": FORCE_TAPER_START_EDGE,
            "force_taper_end_Redge": FORCE_TAPER_END_EDGE,
            "local_half_box_Redge": 0.5 * LOCAL_BOX_EDGE_MULTIPLE,
            "status": "PASS"
            if SOURCE_TAPER_END_EDGE
            <= 0.5 * LOCAL_BOX_EDGE_MULTIPLE
            and FORCE_TAPER_END_EDGE < SOURCE_TAPER_END_EDGE
            else "FAIL",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        }
    )
    return rows


def q_from_profile(
    profile: dict[str, Any], target: dict[str, Any]
) -> tuple[float, float]:
    slope = PM.PREVIOUS.local_logarithmic_slope(
        np.asarray(profile["radius_Mpc"], dtype=float),
        np.asarray(profile["motion_velocity_squared_km2_s2"], dtype=float),
        float(target["transition_radius_Mpc"]),
    )
    return slope, 2.0 * slope if math.isfinite(slope) else math.nan


def profile_convergence(
    coarse: dict[str, Any],
    fine: dict[str, Any],
    target: dict[str, Any],
) -> dict[str, Any]:
    coarse_radius = np.asarray(coarse["radius_Mpc"], dtype=float)
    fine_radius = np.asarray(fine["radius_Mpc"], dtype=float)
    resolved = max(
        float(coarse["resolved_radius_Mpc"]),
        float(fine["resolved_radius_Mpc"]),
    )
    edge = float(target["edge_radius_Mpc"])
    query = fine_radius[
        (fine_radius >= resolved) & (fine_radius <= 0.9 * edge)
    ]
    coarse_density = np.interp(
        query,
        coarse_radius,
        PM.MOTION_FRACTION
        * np.asarray(coarse["excess_density_total_Msun_Mpc3"], dtype=float),
    )
    fine_density = np.interp(
        query,
        fine_radius,
        PM.MOTION_FRACTION
        * np.asarray(fine["excess_density_total_Msun_Mpc3"], dtype=float),
    )
    coarse_velocity = np.interp(
        query,
        coarse_radius,
        np.asarray(coarse["motion_velocity_squared_km2_s2"], dtype=float),
    )
    fine_velocity = np.interp(
        query,
        fine_radius,
        np.asarray(fine["motion_velocity_squared_km2_s2"], dtype=float),
    )
    valid = (
        (coarse_density > 0.0)
        & (fine_density > 0.0)
        & (coarse_velocity > 0.0)
        & (fine_velocity > 0.0)
    )
    if np.count_nonzero(valid) < 3:
        raise RuntimeError("insufficient nested convergence bins")
    density_rmse = float(
        np.sqrt(
            np.mean(
                np.log10(fine_density[valid] / coarse_density[valid]) ** 2
            )
        )
    )
    velocity_rmse = float(
        np.sqrt(
            np.mean(
                np.log10(fine_velocity[valid] / coarse_velocity[valid]) ** 2
            )
        )
    )
    coarse_mass = float(
        np.interp(
            edge,
            coarse_radius,
            np.asarray(coarse["motion_excess_mass_Msun"], dtype=float),
        )
    )
    fine_mass = float(
        np.interp(
            edge,
            fine_radius,
            np.asarray(fine["motion_excess_mass_Msun"], dtype=float),
        )
    )
    mass_difference = abs(fine_mass / coarse_mass - 1.0)
    passed = (
        mass_difference < PROFILE_MASS_TOLERANCE
        and velocity_rmse < PROFILE_VELOCITY_LOG_TOLERANCE
        and density_rmse < PROFILE_DENSITY_LOG_TOLERANCE
    )
    return {
        "comparison_id": "nested_128_to_160",
        "common_resolved_radius_kpc": 1000.0 * resolved,
        "common_profile_bins": int(np.count_nonzero(valid)),
        "fixed_edge_mass_fraction_difference": mass_difference,
        "velocity_squared_log10_RMSE": velocity_rmse,
        "density_log10_RMSE": density_rmse,
        "mass_tolerance": PROFILE_MASS_TOLERANCE,
        "velocity_tolerance": PROFILE_VELOCITY_LOG_TOLERANCE,
        "density_tolerance": PROFILE_DENSITY_LOG_TOLERANCE,
        "status": "PASS" if passed else "FAIL_CLOSED",
        "valid_for_claim": False,
        "checkpoint_marker": MARKER,
    }


def contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "C5162_00_operator",
            "quantity": "nested force",
            "frozen_value": (
                "F_global plus tapered Dirichlet solve of fine-minus-"
                "prolongated-coarse Lagrangian density contrast; numerical "
                "sampling weight N_cell/(1+N_cell)"
            ),
            "new_physical_coupling": False,
            "claim_limit": "numerical refinement of the same Poisson operator",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "contract_id": "C5162_01_boundary",
            "quantity": "local interface",
            "frozen_value": (
                "source taper 1.5-2.0 Redge; force taper 1.25-1.75 Redge; "
                "weighted correction momentum zero; tracked-centre step "
                "at most 0.125 local boxes"
            ),
            "new_physical_coupling": False,
            "claim_limit": "q lies inside the unit-weight region",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "contract_id": "C5162_02_matrix",
            "quantity": "local grids",
            "frozen_value": "128 and 160; same 96 particles, 192 global grid, 120 steps and phases",
            "new_physical_coupling": False,
            "claim_limit": "one antithetic pair; no ensemble claim",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "contract_id": "C5162_03_q",
            "quantity": "resolved transition exponent",
            "frozen_value": "q_diagnostic=2 dln(v^2)/dln(r) at frozen Rn",
            "new_physical_coupling": False,
            "claim_limit": "selection requires resolution and phase convergence",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "contract_id": "C5162_04_machine_cog",
            "quantity": "parent law",
            "frozen_value": "same local GR/Newton/Maxwell zero state",
            "new_physical_coupling": False,
            "claim_limit": "no arena switch",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
    ]


def cog_rows() -> list[dict[str, Any]]:
    rows = PM.cog_rows()
    for row in rows:
        row["checkpoint_marker"] = MARKER
        row["valid_for_claim"] = False
    rows[-1]["state"] = "occupied state with same-law nested Poisson refinement"
    rows[-1]["status"] = "TRANSITION_ZOOM_EXECUTED"
    return rows


def provenance_rows(paths: dict[str, Path]) -> list[dict[str, Any]]:
    urls = {
        "scipy_DST_implementation": (
            "https://docs.scipy.org/doc/scipy/reference/generated/"
            "scipy.fft.dstn.html"
        ),
        "scipy_interpolation_implementation": (
            "https://docs.scipy.org/doc/scipy/reference/generated/"
            "scipy.ndimage.map_coordinates.html"
        ),
    }
    return [
        {
            "source_id": source_id,
            "source_path": str(path),
            "sha256": file_digest(path),
            "source_url": urls.get(source_id, "local_parent_checkpoint"),
            "role": "local_implementation"
            if source_id.startswith("scipy_")
            else "frozen_parent_or_empirical_input",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        }
        for source_id, path in paths.items()
    ]


def add_validation(
    rows: list[dict[str, Any]], name: str, passed: bool, detail: Any
) -> None:
    rows.append(
        {
            "check_id": f"V5162_{len(rows) + 1:02d}_{name}",
            "passed": bool(passed),
            "detail": str(detail),
            "checkpoint_marker": MARKER,
        }
    )


def make_document(result: dict[str, Any]) -> str:
    summary = result["summary"]
    return f"""# 5162 - Shared-mode nested transition zoom and resolved-q gate

Marker: `{MARKER}`.

Date: `{CHECKED_DATE}`.

## Decision

Checkpoint 5162 executes the transition zoom required by checkpoint 5161.
It does not add a galactic force. The global `192^3` periodic PM force is
retained and a local zero-Dirichlet correction solves the difference between
the fine and prolonged coarse Lagrangian density contrasts. Source and force
tapers vanish before the local boundary, and the weighted correction has zero
net momentum. The correction is multiplied by the numerical reliability
factor `N_cell/(1+N_cell)`, where `N_cell` is the coarse-density estimate of
particles per fine cell; unresolved particle shot noise therefore cannot act
as a new physical source.

## 1. Controls

Both Gaussian-force controls, the homogeneous lattice and the taper ordering
pass. The largest analytic Gaussian force error is
`{summary['maximum_Gaussian_force_error']}`. The homogeneous nested force is
`{summary['homogeneous_nested_force']}`. The largest executed source-boundary
ratio is `{summary['maximum_boundary_source_ratio']}` and the largest centre
step is `{summary['maximum_center_jump_Mpc']}` Mpc. Unconstrained candidate
centres can move by `{summary['maximum_candidate_center_jump_Mpc']}` Mpc, so
the interface enforces overlapping local boxes and independently requires its
final tracked centre to agree with the final halo; the largest residual is
`{summary['maximum_final_center_tracking_residual_Mpc']}` Mpc.

## 2. Resolved transition

The local grids are 128 and 160 in a fixed four-edge-radius box. Their
three-cell resolved radii are `{summary['coarse_resolved_radius_kpc']}` and
`{summary['fine_resolved_radius_kpc']}` kpc, both below the frozen
`{summary['target_transition_radius_kpc']}` kpc transition. Four paired runs
execute `{summary['total_particle_updates']}` particle-step updates.

At the frozen transition,

```text
q_parent                          = {summary['q_parent']};
q_nested_128                      = {summary['q_coarse']};
q_nested_160                      = {summary['q_fine']};
resolution difference            = {summary['q_resolution_difference']};
fine-grid phase half-range       = {summary['q_phase_half_range']};
parent-minus-fine absolute value = {summary['q_parent_difference']};
q selection gate                 = {summary['q_selection_status']}.
```

The profile convergence gate is `{summary['profile_convergence_status']}`.
The q result is diagnostic and nonclaim even if selected because it contains
one antithetic phase pair rather than an ensemble.

## 3. Edge and machine-cog limits

The local interface begins outside `1.25 R_edge`, so the transition and the
entire target edge lie inside the untapered force-correction region. Even so,
the compact edge is not promoted to a formation claim because the local box
size was chosen from the frozen edge and the calculation is designed to test
`q`, not select `p=2`.

The action, metric, `G_N`, visible source, Maxwell stress and Poynting momentum
are unchanged. The local GR/Newton/Mercury branch and the galactic occupied
branch remain states of one parent law. If q fails after numerical convergence,
the free collisionless state does not derive the parent phase flow and an
actual parent interaction or wave stress is required; no closure may be
inserted to repair it.

All `{result['validation_count']}` validations pass. Every row remains
nonclaim. The protected `formalization-workbench` digest is
`{result['formalization_workbench_tree_sha256']}`. Galaxy inputs were read-only
and no GitHub action occurred.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--controls-only", action="store_true")
    arguments = parser.parse_args()
    paths = source_paths()
    missing = [str(path) for path in paths.values() if not path.is_file()]
    if missing:
        raise RuntimeError(f"missing sources: {missing}")
    formal_before = PM.tree_digest(FORMAL)
    if formal_before != FORMAL_DIGEST_LOCK:
        raise RuntimeError(f"protected digest mismatch: {formal_before}")
    hashes_before = {key: file_digest(path) for key, path in paths.items()}
    predecessor = json.loads(PREVIOUS_RESULT.read_text(encoding="utf-8"))
    targets, patch, patch_radius, target_constraint = PREVIOUS.target_lookup()
    target = targets[REFERENCE_MAPPING]
    edge_radius = float(target["edge_radius_Mpc"])
    box_size = PM.BOX_OVER_PATCH * patch_radius
    if arguments.dry_run:
        print(
            json.dumps(
                {
                    "dry_run": True,
                    "particle_grid": PARTICLE_GRID,
                    "global_force_grid": GLOBAL_FORCE_GRID,
                    "local_grids": LOCAL_GRIDS,
                    "steps": STEPS,
                    "transition_radius_kpc": 1000.0
                    * float(target["transition_radius_Mpc"]),
                    "formal_digest": formal_before,
                },
                indent=2,
            )
        )
        return
    controls = control_rows(edge_radius)
    if arguments.controls_only:
        print(
            json.dumps(
                {
                    "controls_only": True,
                    "controls": controls,
                    "all_pass": all(
                        row["status"] == "PASS" for row in controls
                    ),
                },
                indent=2,
            )
        )
        if not all(row["status"] == "PASS" for row in controls):
            raise RuntimeError("nested-force controls failed")
        return
    power = PM.power_lookup(read_csv(PM.POWER_CSV))
    coarse_fields, _ = PM.build_conditioned_pair(
        PREVIOUS.COARSE_PARTICLES,
        box_size,
        patch_radius,
        target_constraint,
        power[MASS_LABEL]["k"],
        power[MASS_LABEL]["power"],
    )
    fields = {
        sign: PREVIOUS.periodic_fourier_resample(
            coarse_fields[sign], PARTICLE_GRID
        )
        for sign in PAIR_SIGNS
    }
    initial_rows, states = PREVIOUS.initial_rows_and_states(
        {PARTICLE_GRID: fields}, box_size, patch_radius
    )
    for row in initial_rows:
        row["checkpoint_marker"] = MARKER
    lagrangian_positions = PM.particle_lattice(PARTICLE_GRID, box_size)
    runs: list[dict[str, Any]] = []
    pair_profiles: dict[int, dict[str, Any]] = {}
    individual_q: dict[tuple[int, int], float] = {}
    for local_grid in LOCAL_GRIDS:
        pair_runs: dict[int, dict[str, Any]] = {}
        for sign in PAIR_SIGNS:
            run = run_nested_configuration(
                f"NESTED{local_grid}",
                sign,
                local_grid,
                box_size,
                patch_radius,
                edge_radius,
                states[(PARTICLE_GRID, sign)],
                lagrangian_positions,
            )
            runs.append(run)
            pair_runs[sign] = run
            _, individual_q[(local_grid, sign)] = q_from_profile(
                run["profile"], target
            )
        pair_profiles[local_grid] = PM.pair_mean_profile(
            pair_runs[-1], pair_runs[1]
        )
    scores: list[dict[str, Any]] = []
    profile_rows: list[dict[str, Any]] = []
    pair_q: dict[tuple[int, str], float] = {}
    for local_grid in LOCAL_GRIDS:
        for mapping in PM.MAPPINGS:
            score, rows = PM.score_pair_mean(
                f"NESTED{local_grid}",
                MASS_LABEL,
                mapping,
                pair_profiles[local_grid],
                targets[mapping],
            )
            slope, inferred_q = q_from_profile(
                pair_profiles[local_grid], targets[mapping]
            )
            score["transition_resolved"] = math.isfinite(inferred_q)
            score["transition_log_slope_dlnv2_dlnr"] = slope
            score["diagnostic_q_from_twice_transition_slope"] = inferred_q
            score["diagnostic_q_minus_parent"] = inferred_q - float(
                targets[mapping]["q_parent"]
            )
            score["q_parent_dynamically_scored"] = math.isfinite(inferred_q)
            score["checkpoint_marker"] = MARKER
            scores.append(score)
            pair_q[(local_grid, mapping)] = inferred_q
            for row in rows:
                row["checkpoint_marker"] = MARKER
                profile_rows.append(row)
    q_coarse = pair_q[(LOCAL_GRIDS[0], REFERENCE_MAPPING)]
    q_fine = pair_q[(LOCAL_GRIDS[1], REFERENCE_MAPPING)]
    q_parent = float(target["q_parent"])
    q_resolution_difference = abs(q_fine - q_coarse)
    q_phase_half_range = 0.5 * abs(
        individual_q[(LOCAL_GRIDS[1], 1)]
        - individual_q[(LOCAL_GRIDS[1], -1)]
    )
    q_parent_difference = abs(q_fine - q_parent)
    q_scale = max(abs(q_fine), 1.0e-12)
    q_resolution_controlled = (
        q_resolution_difference / q_scale < Q_RESOLUTION_RELATIVE_TOLERANCE
    )
    q_phase_controlled = (
        q_phase_half_range / q_scale < Q_PHASE_RELATIVE_TOLERANCE
    )
    q_uncertainty_envelope = max(
        q_resolution_difference, q_phase_half_range
    )
    q_parent_compatible = q_parent_difference <= q_uncertainty_envelope
    q_selected = (
        q_resolution_controlled
        and q_phase_controlled
        and q_parent_compatible
    )
    q_row = {
        "mapping": REFERENCE_MAPPING,
        "q_parent": q_parent,
        "q_nested_128": q_coarse,
        "q_nested_160": q_fine,
        "q_resolution_difference": q_resolution_difference,
        "q_resolution_relative_difference": q_resolution_difference / q_scale,
        "q_fine_minus_phase": individual_q[(LOCAL_GRIDS[1], -1)],
        "q_fine_plus_phase": individual_q[(LOCAL_GRIDS[1], 1)],
        "q_phase_half_range": q_phase_half_range,
        "q_phase_relative_half_range": q_phase_half_range / q_scale,
        "q_parent_difference": q_parent_difference,
        "q_uncertainty_envelope": q_uncertainty_envelope,
        "resolution_controlled": q_resolution_controlled,
        "phase_controlled": q_phase_controlled,
        "parent_inside_numerical_envelope": q_parent_compatible,
        "status": "SELECTED_CONDITIONALLY"
        if q_selected
        else "NOT_SELECTED",
        "valid_for_claim": False,
        "checkpoint_marker": MARKER,
    }
    convergence = profile_convergence(
        pair_profiles[LOCAL_GRIDS[0]],
        pair_profiles[LOCAL_GRIDS[1]],
        target,
    )
    run_rows: list[dict[str, Any]] = []
    boundary_rows: list[dict[str, Any]] = []
    for run in runs:
        public = {
            key: value
            for key, value in run.items()
            if key != "profile"
        }
        public["valid_for_claim"] = False
        public["checkpoint_marker"] = MARKER
        run_rows.append(public)
        boundary_rows.append(
            {
                "config_id": run["config_id"],
                "pair_sign": run["pair_sign"],
                "maximum_center_jump_Mpc": run[
                    "maximum_center_jump_Mpc"
                ],
                "maximum_candidate_center_jump_Mpc": run[
                    "maximum_candidate_center_jump_Mpc"
                ],
                "center_limited_steps": run["center_limited_steps"],
                "final_center_tracking_residual_Mpc": run[
                    "final_center_tracking_residual_Mpc"
                ],
                "maximum_boundary_source_ratio": run[
                    "maximum_boundary_source_ratio"
                ],
                "maximum_correction_force_sum_norm": run[
                    "maximum_correction_force_sum_norm"
                ],
                "valid_for_claim": False,
                "checkpoint_marker": MARKER,
            }
        )
    contracts = contract_rows()
    cogs = cog_rows()
    provenance = provenance_rows(paths)
    summary = {
        "maximum_Gaussian_force_error": max(
            float(row["measured_maximum_relative_error"])
            for row in controls
            if row["control_id"].startswith("Gaussian")
        ),
        "homogeneous_nested_force": next(
            float(row["measured_maximum_absolute_force"])
            for row in controls
            if row["control_id"] == "homogeneous_lattice_nested_force"
        ),
        "maximum_boundary_source_ratio": max(
            float(run["maximum_boundary_source_ratio"]) for run in runs
        ),
        "maximum_center_jump_Mpc": max(
            float(run["maximum_center_jump_Mpc"]) for run in runs
        ),
        "maximum_candidate_center_jump_Mpc": max(
            float(run["maximum_candidate_center_jump_Mpc"])
            for run in runs
        ),
        "maximum_final_center_tracking_residual_Mpc": max(
            float(run["final_center_tracking_residual_Mpc"])
            for run in runs
        ),
        "maximum_center_limited_steps": max(
            int(run["center_limited_steps"]) for run in runs
        ),
        "run_count": len(runs),
        "score_count": len(scores),
        "profile_row_count": len(profile_rows),
        "total_particle_updates": sum(
            int(run["particle_count"]) * int(run["steps"])
            for run in runs
        ),
        "coarse_resolved_radius_kpc": 1000.0
        * float(pair_profiles[LOCAL_GRIDS[0]]["resolved_radius_Mpc"]),
        "fine_resolved_radius_kpc": 1000.0
        * float(pair_profiles[LOCAL_GRIDS[1]]["resolved_radius_Mpc"]),
        "target_transition_radius_kpc": 1000.0
        * float(target["transition_radius_Mpc"]),
        "q_parent": q_parent,
        "q_coarse": q_coarse,
        "q_fine": q_fine,
        "q_resolution_difference": q_resolution_difference,
        "q_phase_half_range": q_phase_half_range,
        "q_parent_difference": q_parent_difference,
        "q_selection_status": q_row["status"],
        "profile_convergence_status": convergence["status"],
    }
    generated = {
        CONTRACT_CSV: contracts,
        CONTROL_CSV: controls,
        INITIAL_CSV: initial_rows,
        RUN_CSV: run_rows,
        PROFILE_CSV: profile_rows,
        SCORE_CSV: scores,
        Q_CSV: [q_row],
        CONVERGENCE_CSV: [convergence],
        BOUNDARY_CSV: boundary_rows,
        COG_CSV: cogs,
        PROVENANCE_CSV: provenance,
    }
    for path, rows in generated.items():
        write_csv(path, rows)
    provisional = {
        "summary": summary,
        "validation_count": 0,
        "formalization_workbench_tree_sha256": formal_before,
    }
    DOCUMENT.write_text(make_document(provisional), encoding="utf-8")
    hashes_after = {key: file_digest(path) for key, path in paths.items()}
    formal_after = PM.tree_digest(FORMAL)
    validation: list[dict[str, Any]] = []
    add_validation(validation, "sources_exist", not missing, missing)
    add_validation(validation, "source_hashes_unchanged", hashes_before == hashes_after, hashes_after)
    add_validation(validation, "formalization_workbench_unchanged", formal_after == FORMAL_DIGEST_LOCK, formal_after)
    add_validation(validation, "predecessor_passed", predecessor["validation_failures"] == [], predecessor["validation_failures"])
    add_validation(validation, "scipy_sources_local", FFT_SOURCE.is_file() and INTERPOLATION_SOURCE.is_file(), scipy.__version__)
    add_validation(validation, "all_controls_pass", all(row["status"] == "PASS" for row in controls), {row["control_id"]: row["status"] for row in controls})
    add_validation(validation, "four_runs_complete", len(runs) == 4, len(runs))
    add_validation(validation, "paired_signs_each_grid", all({int(run["pair_sign"]) for run in runs if int(run["local_force_grid"]) == grid} == {-1, 1} for grid in LOCAL_GRIDS), len(runs))
    add_validation(validation, "common_global_operator", {int(run["global_force_grid"]) for run in runs} == {GLOBAL_FORCE_GRID} and {int(run["steps"]) for run in runs} == {STEPS}, [GLOBAL_FORCE_GRID, STEPS])
    add_validation(validation, "initial_density_controlled", min(float(row["initial_scaled_delta_minimum"]) for row in initial_rows) > -0.8 and max(float(row["initial_scaled_delta_maximum"]) for row in initial_rows) < 0.8, "fine pair")
    add_validation(validation, "initial_displacements_controlled", max(float(row["maximum_initial_displacement_cells"]) for row in initial_rows) < 1.0, max(float(row["maximum_initial_displacement_cells"]) for row in initial_rows))
    add_validation(validation, "both_local_grids_resolve_transition", all(float(run["resolved_radius_kpc"]) <= summary["target_transition_radius_kpc"] for run in runs), [run["resolved_radius_kpc"] for run in runs])
    add_validation(validation, "center_tracking_step_controlled", summary["maximum_center_jump_Mpc"] <= CENTER_MAX_STEP_FRACTION * LOCAL_BOX_EDGE_MULTIPLE * edge_radius * (1.0 + 1.0e-12), summary["maximum_center_jump_Mpc"])
    add_validation(validation, "center_tracking_reaches_final_halo", summary["maximum_final_center_tracking_residual_Mpc"] < CENTER_JUMP_FRACTION_TOLERANCE * LOCAL_BOX_EDGE_MULTIPLE * edge_radius, summary["maximum_final_center_tracking_residual_Mpc"])
    add_validation(validation, "boundary_source_silent", summary["maximum_boundary_source_ratio"] < BOUNDARY_SOURCE_RATIO_TOLERANCE, summary["maximum_boundary_source_ratio"])
    add_validation(validation, "correction_momentum_balanced", max(float(run["maximum_correction_force_sum_norm"]) for run in runs) < 1.0e-8, max(float(run["maximum_correction_force_sum_norm"]) for run in runs))
    add_validation(validation, "profile_rows_complete", len(profile_rows) == 480 and len(scores) == 4, [len(profile_rows), len(scores)])
    add_validation(validation, "q_finite", all(math.isfinite(value) for value in [q_coarse, q_fine, *individual_q.values()]), q_row)
    add_validation(validation, "q_status_fail_closed_or_selected", q_row["status"] in {"SELECTED_CONDITIONALLY", "NOT_SELECTED"}, q_row["status"])
    add_validation(validation, "q_status_follows_gates", (q_row["status"] == "SELECTED_CONDITIONALLY") == (q_resolution_controlled and q_phase_controlled and q_parent_compatible), q_row["status"])
    add_validation(validation, "profile_convergence_status_valid", convergence["status"] in {"PASS", "FAIL_CLOSED"}, convergence["status"])
    add_validation(validation, "q_scored_only_when_resolved", all(score["q_parent_dynamically_scored"] and score["transition_resolved"] for score in scores), "all scores")
    add_validation(validation, "no_refit", all(score["no_refit"] for score in scores), "all scores")
    add_validation(validation, "local_machine_cog_unchanged", all(row["same_parent_action"] and not row["new_parameter"] for row in cogs), "three arenas")
    add_validation(validation, "all_rows_nonclaim", all(not row["valid_for_claim"] for rows in generated.values() for row in rows), "all rows")
    generated_text = "\n".join(path.read_text(encoding="utf-8") for path in [DOCUMENT, *generated])
    add_validation(validation, "no_placeholders", "MISSING_" not in generated_text and "PLACEHOLDER" not in generated_text, "artifacts")
    add_validation(validation, "no_nonfinite_text", "nan" not in generated_text.lower() and "infinity" not in generated_text.lower(), "artifacts")
    add_validation(validation, "document_marker", MARKER in DOCUMENT.read_text(encoding="utf-8"), DOCUMENT)
    add_validation(validation, "galaxy_read_only", hashes_before["galaxy_samples_read_only"] == hashes_after["galaxy_samples_read_only"], hashes_after["galaxy_samples_read_only"])
    failures = [row["check_id"] for row in validation if not row["passed"]]
    write_csv(VALIDATION_CSV, validation)
    result = {
        "checked_date": CHECKED_DATE,
        "checkpoint_marker": MARKER,
        "route_decision": "Q_SELECTED_CONDITIONALLY_PARENT_FLOW_SURVIVES_ZOOM" if q_selected else "Q_NOT_SELECTED_FREE_COLLISIONLESS_ROUTE_REQUIRES_PARENT_INTERACTION_OR_WAVE_STRESS",
        "nested_transition_zoom_executed": True,
        "q_parent_dynamically_selected": q_selected,
        "compact_p2_edge_selected": False,
        "local_GR_Newton_Maxwell_branch_modified": False,
        "valid_for_galaxy_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
        "summary": summary,
        "source_hashes_before": hashes_before,
        "source_hashes_after": hashes_after,
        "formalization_workbench_tree_sha256": formal_after,
        "validation_count": len(validation),
        "validation_failures": failures,
    }
    write_json(RESULT_JSON, result)
    DOCUMENT.write_text(make_document(result), encoding="utf-8")
    if failures:
        raise RuntimeError(f"checkpoint 5162 validation failures: {failures}")


if __name__ == "__main__":
    main()
