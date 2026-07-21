from __future__ import annotations

import argparse
import csv
import gc
import hashlib
import importlib.util
import json
import math
import time
from pathlib import Path
from typing import Any

import numpy as np


POST = Path(__file__).resolve().parents[1]
FORMAL = POST.parent / "formalization-workbench"
PREVIOUS_SCRIPT = (
    POST
    / "scripts"
    / "Y5_R2FR_5159_constrained_peak_spherical_Vlasov_collapse_gate.py"
)
PREVIOUS_DOCUMENT = (
    POST
    / "5159-Y5-R2FR-source-backed-constrained-peak-spherical-Vlasov-collapse-and-profile-selection-gate.md"
)
PREVIOUS_RESULT = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5159"
    / "constrained_peak_spherical_collapse_results.json"
)
POWER_CSV = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5156"
    / "radiation_era_FDM_transfer_curves.csv"
)
PATCH_CSV = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5156"
    / "halo_patch_covariance_collapse_gate.csv"
)
HALO_CSV = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5154"
    / "smooth_edge_halo_inventory.csv"
)
EDDINGTON_CSV = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5154"
    / "Eddington_distribution_envelope.csv"
)
LOCAL_INHERITANCE_CSV = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5157"
    / "transfer_local_cog_inheritance.csv"
)
CONSTRAINED_SOURCE = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5159"
    / "sources"
    / "constrained_peaks_astro_ph_9507024_source.tar"
)
FASTPM_SOURCE = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5159"
    / "sources"
    / "fastpm_1603.00476_source.tar"
)
GALAXY_SAMPLES = Path(r"D:\Users\ollet\Documents\mts-galaxy-lab\data\samples.js")
OUT = POST / "source-intake" / "functional_rg" / "5160"
RESULT_JSON = OUT / "paired_3D_constrained_PM_results.json"
CONTRACT_CSV = OUT / "paired_3D_frozen_contract.csv"
INITIAL_CSV = OUT / "paired_realization_initial_diagnostics.csv"
RUN_CSV = OUT / "particle_mesh_run_summary.csv"
PROFILE_CSV = OUT / "paired_3D_profile_samples.csv"
SCORE_CSV = OUT / "paired_mean_no_refit_scores.csv"
CONVERGENCE_CSV = OUT / "particle_mesh_convergence_matrix.csv"
CONTROL_CSV = OUT / "particle_mesh_equation_controls.csv"
COG_CSV = OUT / "machine_cog_inheritance.csv"
PROVENANCE_CSV = OUT / "source_provenance.csv"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5160_VALIDATION.csv"
)
DOCUMENT = (
    POST
    / "5160-Y5-R2FR-paired-3D-constrained-realization-particle-mesh-collapse-and-tidal-profile-gate.md"
)

MARKER = "MTS_5160_PAIRED_3D_CONSTRAINED_PM_COLLAPSE_GATE"
CHECKED_DATE = "2026-07-20"
FORMAL_DIGEST_LOCK = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"

REFERENCE_GALAXY = "UGC09133"
REFERENCE_MAPPING = "Wetterich_v_equals_minus_2lambda"
MAPPINGS = (
    "Wetterich_v_equals_minus_2lambda",
    "Wetterich_v_equals_plus_2lambda",
)
MASS_LABELS = (
    "ten_times_WKB_floor",
    "benchmark_1e_minus20_eV",
    "benchmark_1e_minus18_eV",
)
BENCHMARK_MASS = "benchmark_1e_minus20_eV"
PAIR_SIGNS = (-1, 1)
BOX_OVER_PATCH = 4.0
PEAK_HEIGHT_SIGMA = 1.0
A_INITIAL = 0.01
BASE_PARTICLE_GRID = 64
BASE_FORCE_GRID = 128
BASE_STEPS = 120
LOW_FORCE_GRID = 112
HIGH_FORCE_GRID = 160
DOUBLE_STEPS = 240
HIGH_PARTICLE_GRID = 96
HIGH_PARTICLE_FORCE_GRID = 192
HIGH_PARTICLE_STEPS = 120
PROFILE_BINS = 120
RESOLVED_FORCE_CELLS = 3.0
FIXED_SEED = int.from_bytes(
    hashlib.sha256(f"{MARKER}|paired-residual".encode("utf-8")).digest()[:8],
    "little",
) % (2**32)

H0_KM_S_MPC = 67.4
OMEGA_M = 0.315
OMEGA_B = 0.04924319136384048
OMEGA_X = OMEGA_M - OMEGA_B
MOTION_FRACTION = OMEGA_X / OMEGA_M
RHO_CRIT_MSUN_MPC3 = 2.77536627e11 * (H0_KM_S_MPC / 100.0) ** 2
RHO_M_MSUN_MPC3 = OMEGA_M * RHO_CRIT_MSUN_MPC3
G_MPC_KM2_S2_MSUN = 4.30091727003628e-9

PRIMARY_URLS = {
    "constrained_realizations": "https://arxiv.org/abs/astro-ph/9507024",
    "particle_mesh": "https://arxiv.org/abs/1603.00476",
    "fuzzy_transfer": "https://arxiv.org/abs/astro-ph/0003365",
}


def load_previous_module() -> Any:
    specification = importlib.util.spec_from_file_location(
        "mts_checkpoint_5159", PREVIOUS_SCRIPT
    )
    if specification is None or specification.loader is None:
        raise RuntimeError("cannot load checkpoint-5159 module")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


PREVIOUS = load_previous_module()


def file_digest(path: Path) -> str:
    value = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            value.update(block)
    return value.hexdigest()


def tree_digest(path: Path) -> str:
    value = hashlib.sha256()
    for item in sorted(candidate for candidate in path.rglob("*") if candidate.is_file()):
        value.update(item.relative_to(path).as_posix().encode("utf-8"))
        value.update(file_digest(item).encode("ascii"))
    return value.hexdigest()


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
    normalized_rows: list[dict[str, Any]] = []
    for row in rows:
        normalized_rows.append(
            {
                field: ""
                if isinstance(value, (float, np.floating))
                and not math.isfinite(float(value))
                else value
                for field, value in row.items()
            }
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(normalized_rows)


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True, allow_nan=False) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def source_paths() -> dict[str, Path]:
    return {
        "previous_script": PREVIOUS_SCRIPT,
        "previous_document": PREVIOUS_DOCUMENT,
        "previous_result": PREVIOUS_RESULT,
        "power_covariance": POWER_CSV,
        "patch_covariance": PATCH_CSV,
        "halo_targets": HALO_CSV,
        "Eddington_targets": EDDINGTON_CSV,
        "local_inheritance": LOCAL_INHERITANCE_CSV,
        "constrained_realization_source": CONSTRAINED_SOURCE,
        "FastPM_source": FASTPM_SOURCE,
        "galaxy_samples_read_only": GALAXY_SAMPLES,
    }


def provenance_rows(paths: dict[str, Path]) -> list[dict[str, Any]]:
    urls = {
        "constrained_realization_source": PRIMARY_URLS[
            "constrained_realizations"
        ],
        "FastPM_source": PRIMARY_URLS["particle_mesh"],
    }
    rows = [
        {
            "source_id": key,
            "source_path": str(path),
            "sha256": file_digest(path),
            "source_url": urls.get(key, "local_parent_checkpoint"),
            "role": "primary_external_source"
            if key in urls
            else "frozen_parent_or_empirical_input",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        }
        for key, path in paths.items()
    ]
    rows.append(
        {
            "source_id": "fuzzy_transfer",
            "source_path": "URL_ONLY_PRIMARY_REFERENCE",
            "sha256": "NOT_LOCAL_FILE",
            "source_url": PRIMARY_URLS["fuzzy_transfer"],
            "role": "primary_method_reference",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        }
    )
    return rows


def power_lookup(rows: list[dict[str, str]]) -> dict[str, dict[str, np.ndarray]]:
    result: dict[str, dict[str, np.ndarray]] = {}
    for mass_label in MASS_LABELS:
        selected = [row for row in rows if row["mass_label"] == mass_label]
        selected.sort(key=lambda row: float(row["k_Mpc_inverse"]))
        result[mass_label] = {
            "k": np.array(
                [float(row["k_Mpc_inverse"]) for row in selected], dtype=float
            ),
            "power": np.array(
                [float(row["P_MTS_empirical_adiabatic_Mpc3"]) for row in selected],
                dtype=float,
            ),
            "mass_eV": np.array([float(selected[0]["m_gap_eV"])], dtype=float),
        }
    return result


def interpolate_power(
    magnitudes: np.ndarray,
    source_k: np.ndarray,
    source_power: np.ndarray,
) -> np.ndarray:
    output = np.zeros_like(magnitudes, dtype=float)
    valid = (magnitudes >= source_k[0]) & (magnitudes <= source_k[-1])
    output[valid] = np.exp(
        np.interp(
            np.log(magnitudes[valid]),
            np.log(source_k),
            np.log(source_power),
        )
    )
    return output


def fourier_grid(
    grid_size: int,
    box_size: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    spacing = box_size / grid_size
    kx = 2.0 * math.pi * np.fft.fftfreq(grid_size, d=spacing)
    ky = 2.0 * math.pi * np.fft.fftfreq(grid_size, d=spacing)
    kz = 2.0 * math.pi * np.fft.rfftfreq(grid_size, d=spacing)
    squared = (
        kx[:, None, None] ** 2
        + ky[None, :, None] ** 2
        + kz[None, None, :] ** 2
    )
    return kx, ky, kz, squared


def point_top_hat_covariance(
    source_k: np.ndarray,
    source_power: np.ndarray,
    patch_radius: float,
    radii: np.ndarray,
) -> tuple[float, np.ndarray]:
    log_k = np.log(source_k)
    delta_squared = source_k**3 * source_power / (2.0 * math.pi**2)
    window = PREVIOUS.top_hat(source_k * patch_radius)
    variance = float(np.trapezoid(delta_squared * window**2, x=log_k))
    covariance = np.empty_like(radii)
    for start in range(0, len(radii), 128):
        stop = min(start + 128, len(radii))
        argument = radii[start:stop, None] * source_k[None, :]
        spherical_bessel = np.sinc(argument / math.pi)
        covariance[start:stop] = np.trapezoid(
            spherical_bessel * (delta_squared * window)[None, :],
            x=log_k,
            axis=1,
        )
    return variance, covariance


def periodic_displacements(
    positions: np.ndarray,
    center: np.ndarray,
    box_size: float,
) -> np.ndarray:
    return (positions - center + 0.5 * box_size) % box_size - 0.5 * box_size


def build_mean_density_field(
    grid_size: int,
    box_size: float,
    patch_radius: float,
    target_delta: float,
    source_k: np.ndarray,
    source_power: np.ndarray,
) -> tuple[np.ndarray, float]:
    radial_samples = np.linspace(
        0.0, math.sqrt(3.0) * box_size / 2.0, 2048
    )
    variance, covariance = point_top_hat_covariance(
        source_k, source_power, patch_radius, radial_samples
    )
    radial_mean = target_delta * covariance / variance
    coordinates = np.arange(grid_size, dtype=float) * box_size / grid_size
    center_value = box_size / 2.0
    wrapped = (coordinates - center_value + 0.5 * box_size) % box_size - 0.5 * box_size
    radii = np.sqrt(
        wrapped[:, None, None] ** 2
        + wrapped[None, :, None] ** 2
        + wrapped[None, None, :] ** 2
    )
    mean_field = np.interp(radii, radial_samples, radial_mean)
    mean_field -= float(np.mean(mean_field))
    _, _, _, squared = fourier_grid(grid_size, box_size)
    window = PREVIOUS.top_hat(np.sqrt(squared) * patch_radius)
    center_index = grid_size // 2
    mean_fourier = np.fft.rfftn(mean_field)
    measured = float(
        np.fft.irfftn(
            mean_fourier * window, s=mean_field.shape, axes=(0, 1, 2)
        )[
            center_index, center_index, center_index
        ]
    )
    if measured == 0.0:
        raise RuntimeError("zero periodic mean constraint")
    mean_field *= target_delta / measured
    return mean_field, variance


def build_conditioned_pair(
    grid_size: int,
    box_size: float,
    patch_radius: float,
    target_delta: float,
    source_k: np.ndarray,
    source_power: np.ndarray,
) -> tuple[dict[int, np.ndarray], dict[str, Any]]:
    volume = box_size**3
    kx, ky, kz, squared = fourier_grid(grid_size, box_size)
    magnitude = np.sqrt(squared)
    mode_power = interpolate_power(magnitude, source_k, source_power)
    mode_power[0, 0, 0] = 0.0
    window = PREVIOUS.top_hat(magnitude * patch_radius)
    rng = np.random.default_rng(FIXED_SEED)
    white = rng.standard_normal((grid_size, grid_size, grid_size))
    white -= float(np.mean(white))
    raw_fourier = np.fft.rfftn(white) * np.sqrt(
        grid_size**3 * mode_power / volume
    )
    center_value = box_size / 2.0
    phase = np.exp(
        -1j
        * (
            kx[:, None, None] * center_value
            + ky[None, :, None] * center_value
            + kz[None, None, :] * center_value
        )
    )
    covariance_fourier = (
        grid_size**3 * mode_power * window * phase / volume
    )
    center_index = grid_size // 2
    raw_smoothed = np.fft.irfftn(
        raw_fourier * window, s=white.shape, axes=(0, 1, 2)
    )
    random_constraint = float(
        raw_smoothed[center_index, center_index, center_index]
    )
    covariance_smoothed = np.fft.irfftn(
        covariance_fourier * window, s=white.shape, axes=(0, 1, 2)
    )
    box_variance = float(
        covariance_smoothed[center_index, center_index, center_index]
    )
    if box_variance <= 0.0:
        raise RuntimeError("nonpositive finite-box constraint variance")
    residual_fourier = (
        raw_fourier
        - random_constraint * covariance_fourier / box_variance
    )
    residual_field = np.fft.irfftn(
        residual_fourier, s=white.shape, axes=(0, 1, 2)
    )
    residual_constraint = float(
        np.fft.irfftn(
            residual_fourier * window, s=white.shape, axes=(0, 1, 2)
        )[
            center_index, center_index, center_index
        ]
    )
    mean_field, full_variance = build_mean_density_field(
        grid_size,
        box_size,
        patch_radius,
        target_delta,
        source_k,
        source_power,
    )
    fields = {
        -1: mean_field - residual_field,
        1: mean_field + residual_field,
    }
    constraints: dict[int, float] = {}
    for sign, field in fields.items():
        constraints[sign] = float(
            np.fft.irfftn(
                np.fft.rfftn(field) * window,
                s=field.shape,
                axes=(0, 1, 2),
            )[center_index, center_index, center_index]
        )
    pair_mean_error = float(
        np.max(np.abs(0.5 * (fields[-1] + fields[1]) - mean_field))
    )
    residual_antisymmetry_error = float(
        np.max(
            np.abs(
                (fields[1] - mean_field) + (fields[-1] - mean_field)
            )
        )
    )
    diagnostics = {
        "full_sigma": math.sqrt(full_variance),
        "box_sigma": math.sqrt(box_variance),
        "box_to_full_sigma": math.sqrt(box_variance / full_variance),
        "raw_random_constraint": random_constraint,
        "conditioned_residual_constraint": residual_constraint,
        "minus_constraint": constraints[-1],
        "plus_constraint": constraints[1],
        "target_constraint": target_delta,
        "maximum_constraint_error": max(
            abs(constraints[-1] - target_delta),
            abs(constraints[1] - target_delta),
        ),
        "pair_mean_error": pair_mean_error,
        "residual_antisymmetry_error": residual_antisymmetry_error,
        "z0_delta_minimum": min(float(np.min(field)) for field in fields.values()),
        "z0_delta_maximum": max(float(np.max(field)) for field in fields.values()),
    }
    return fields, diagnostics


def displacement_from_density(
    density_field: np.ndarray,
    box_size: float,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    grid_size = density_field.shape[0]
    kx, ky, kz, squared = fourier_grid(grid_size, box_size)
    density_fourier = np.fft.rfftn(density_field)
    inverse = np.zeros_like(squared)
    nonzero = squared > 0.0
    inverse[nonzero] = 1.0 / squared[nonzero]
    components = []
    for component in (
        kx[:, None, None],
        ky[None, :, None],
        kz[None, None, :],
    ):
        components.append(
            np.fft.irfftn(
                1j * component * inverse * density_fourier,
                s=density_field.shape,
                axes=(0, 1, 2),
            )
        )
    return components[0], components[1], components[2]


def particle_lattice(
    grid_size: int,
    box_size: float,
    offset_cells: float = 0.0,
) -> np.ndarray:
    coordinate = (
        np.arange(grid_size, dtype=float) + offset_cells
    ) * box_size / grid_size
    x, y, z = np.meshgrid(coordinate, coordinate, coordinate, indexing="ij")
    return np.column_stack((x.ravel(), y.ravel(), z.ravel()))


def initial_particle_state(
    density_field: np.ndarray,
    box_size: float,
    patch_radius: float,
) -> dict[str, Any]:
    grid_size = density_field.shape[0]
    lattice = particle_lattice(grid_size, box_size)
    displacements = displacement_from_density(density_field, box_size)
    displacement = np.column_stack(
        [component.ravel() for component in displacements]
    )
    growth_initial, growth_rate_initial = PREVIOUS.growth(A_INITIAL)
    positions = (lattice + growth_initial * displacement) % box_size
    momenta = (
        A_INITIAL**2
        * float(PREVIOUS.expansion(A_INITIAL))
        * growth_rate_initial
        * growth_initial
        * displacement
    )
    center = np.full(3, box_size / 2.0)
    lagrangian_distance = np.linalg.norm(
        periodic_displacements(lattice, center, box_size), axis=1
    )
    tagged = lagrangian_distance <= patch_radius
    return {
        "positions": positions,
        "momenta": momenta,
        "tagged": tagged,
        "growth_initial": growth_initial,
        "growth_rate_initial": growth_rate_initial,
        "maximum_initial_displacement_cells": float(
            np.max(np.linalg.norm(growth_initial * displacement, axis=1))
            / (box_size / grid_size)
        ),
        "initial_scaled_delta_minimum": float(
            growth_initial * np.min(density_field)
        ),
        "initial_scaled_delta_maximum": float(
            growth_initial * np.max(density_field)
        ),
        "tagged_particle_count": int(np.count_nonzero(tagged)),
    }


def cic_geometry(
    positions: np.ndarray,
    grid_size: int,
    box_size: float,
) -> tuple[np.ndarray, np.ndarray]:
    scaled = positions * grid_size / box_size
    base = np.floor(scaled).astype(np.int64)
    fraction = scaled - base
    base %= grid_size
    return base, fraction


def cic_density_contrast(
    base: np.ndarray,
    fraction: np.ndarray,
    grid_size: int,
) -> np.ndarray:
    density = np.zeros(grid_size**3, dtype=float)
    for offset_x in (0, 1):
        weight_x = fraction[:, 0] if offset_x else 1.0 - fraction[:, 0]
        index_x = (base[:, 0] + offset_x) % grid_size
        for offset_y in (0, 1):
            weight_y = fraction[:, 1] if offset_y else 1.0 - fraction[:, 1]
            index_y = (base[:, 1] + offset_y) % grid_size
            for offset_z in (0, 1):
                weight_z = fraction[:, 2] if offset_z else 1.0 - fraction[:, 2]
                index_z = (base[:, 2] + offset_z) % grid_size
                flat = (index_x * grid_size + index_y) * grid_size + index_z
                density += np.bincount(
                    flat,
                    weights=weight_x * weight_y * weight_z,
                    minlength=grid_size**3,
                )
    mean_count = len(base) / grid_size**3
    return density.reshape((grid_size, grid_size, grid_size)) / mean_count - 1.0


def cic_interpolate(
    field: np.ndarray,
    base: np.ndarray,
    fraction: np.ndarray,
) -> np.ndarray:
    grid_size = field.shape[0]
    flat_field = field.ravel()
    result = np.zeros(len(base), dtype=float)
    for offset_x in (0, 1):
        weight_x = fraction[:, 0] if offset_x else 1.0 - fraction[:, 0]
        index_x = (base[:, 0] + offset_x) % grid_size
        for offset_y in (0, 1):
            weight_y = fraction[:, 1] if offset_y else 1.0 - fraction[:, 1]
            index_y = (base[:, 1] + offset_y) % grid_size
            for offset_z in (0, 1):
                weight_z = fraction[:, 2] if offset_z else 1.0 - fraction[:, 2]
                index_z = (base[:, 2] + offset_z) % grid_size
                flat = (index_x * grid_size + index_y) * grid_size + index_z
                result += weight_x * weight_y * weight_z * flat_field[flat]
    return result


def particle_mesh_force(
    positions: np.ndarray,
    grid_size: int,
    box_size: float,
) -> tuple[np.ndarray, dict[str, float]]:
    base, fraction = cic_geometry(positions, grid_size, box_size)
    density = cic_density_contrast(base, fraction, grid_size)
    density_fourier = np.fft.rfftn(density)
    _, _, _, squared = fourier_grid(grid_size, box_size)
    potential_fourier = np.zeros_like(density_fourier)
    nonzero = squared > 0.0
    potential_fourier[nonzero] = (
        -1.5 * OMEGA_M * density_fourier[nonzero] / squared[nonzero]
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
        force[:, axis] = cic_interpolate(component, base, fraction)
        del component
    diagnostics = {
        "density_mean": float(np.mean(density)),
        "density_minimum": float(np.min(density)),
        "density_maximum": float(np.max(density)),
        "force_mean_norm": float(np.linalg.norm(np.mean(force, axis=0))),
        "force_maximum_norm": float(np.max(np.linalg.norm(force, axis=1))),
    }
    del base, fraction, density, density_fourier, potential_fourier, potential
    return force, diagnostics


def evolve_particle_mesh(
    positions: np.ndarray,
    momenta: np.ndarray,
    force_grid: int,
    box_size: float,
    steps: int,
    final_scale_factor: float = 1.0,
) -> dict[str, Any]:
    positions = positions.copy()
    momenta = momenta.copy()
    scale_factors = np.geomspace(A_INITIAL, final_scale_factor, steps + 1)
    lower = scale_factors[:-1]
    upper = scale_factors[1:]
    midpoint = np.sqrt(lower * upper)
    drifts = PREVIOUS.integration_factors(lower, upper, 3)
    first_half = PREVIOUS.integration_factors(
        np.array([lower[0]]), np.array([midpoint[0]]), 2
    )[0]
    between = (
        PREVIOUS.integration_factors(midpoint[:-1], midpoint[1:], 2)
        if steps > 1
        else np.array([], dtype=float)
    )
    final_half = PREVIOUS.integration_factors(
        np.array([midpoint[-1]]), np.array([upper[-1]]), 2
    )[0]
    start = time.perf_counter()
    force, initial_force_diagnostics = particle_mesh_force(
        positions, force_grid, box_size
    )
    half_momenta = momenta + first_half * force
    final_force_diagnostics = initial_force_diagnostics
    for index in range(steps):
        positions = (positions + drifts[index] * half_momenta) % box_size
        force, final_force_diagnostics = particle_mesh_force(
            positions, force_grid, box_size
        )
        if index < steps - 1:
            half_momenta += between[index] * force
        else:
            momenta = half_momenta + final_half * force
    return {
        "positions": positions,
        "momenta": momenta,
        "wall_seconds": time.perf_counter() - start,
        "initial_force_diagnostics": initial_force_diagnostics,
        "final_force_diagnostics": final_force_diagnostics,
    }


def independent_linear_growth_ratio(
    mesh_response: float,
    initial_scale_factor: float,
    final_scale_factor: float,
    substeps: int = 8192,
) -> float:
    growth_initial, growth_rate_initial = PREVIOUS.growth(
        initial_scale_factor
    )
    state = np.array(
        [growth_initial, growth_rate_initial * growth_initial], dtype=float
    )
    log_initial = math.log(initial_scale_factor)
    step = (
        math.log(final_scale_factor) - log_initial
    ) / substeps

    def derivative(log_scale: float, values: np.ndarray) -> np.ndarray:
        scale_factor = math.exp(log_scale)
        expansion = float(PREVIOUS.expansion(scale_factor))
        omega_m_scale = OMEGA_M / (
            scale_factor**3 * expansion**2
        )
        return np.array(
            [
                values[1],
                -(2.0 - 1.5 * omega_m_scale) * values[1]
                + 1.5
                * mesh_response
                * omega_m_scale
                * values[0],
            ]
        )

    log_scale = log_initial
    for _ in range(substeps):
        first = derivative(log_scale, state)
        second = derivative(
            log_scale + 0.5 * step,
            state + 0.5 * step * first,
        )
        third = derivative(
            log_scale + 0.5 * step,
            state + 0.5 * step * second,
        )
        fourth = derivative(
            log_scale + step,
            state + step * third,
        )
        state += step * (
            first + 2.0 * second + 2.0 * third + fourth
        ) / 6.0
        log_scale += step
    return float(state[0] / growth_initial)


def linear_mode_diagnostic(
    mode_number: int,
    final_scale_factor: float = 0.08,
) -> dict[str, float]:
    grid_size = 32
    box_size = 10.0
    amplitude_z0 = 1.0e-2
    lattice = particle_lattice(grid_size, box_size, offset_cells=0.25)
    mode_k = 2.0 * math.pi * mode_number / box_size
    displacement = np.zeros_like(lattice)
    displacement[:, 0] = (
        -amplitude_z0
        * np.sin(mode_k * lattice[:, 0])
        / mode_k
    )
    growth_initial, growth_rate_initial = PREVIOUS.growth(A_INITIAL)
    scaled_displacement = growth_initial * displacement
    positions = (lattice + scaled_displacement) % box_size
    momenta = (
        A_INITIAL**2
        * float(PREVIOUS.expansion(A_INITIAL))
        * growth_rate_initial
        * scaled_displacement
    )
    initial_force, _ = particle_mesh_force(
        positions, grid_size, box_size
    )
    mesh_response = float(
        np.sum(initial_force * scaled_displacement)
        / (
            1.5
            * OMEGA_M
            * np.sum(scaled_displacement * scaled_displacement)
        )
    )
    initial_base, initial_fraction = cic_geometry(
        positions, grid_size, box_size
    )
    initial_density = cic_density_contrast(
        initial_base, initial_fraction, grid_size
    )
    initial_fourier = np.fft.rfftn(initial_density)
    initial_mode = (
        2.0
        * abs(initial_fourier[mode_number, 0, 0])
        / grid_size**3
    )
    evolved = evolve_particle_mesh(
        positions,
        momenta,
        grid_size,
        box_size,
        80,
        final_scale_factor,
    )
    final_base, final_fraction = cic_geometry(
        np.asarray(evolved["positions"]), grid_size, box_size
    )
    final_density = cic_density_contrast(
        final_base, final_fraction, grid_size
    )
    final_fourier = np.fft.rfftn(final_density)
    final_mode = (
        2.0 * abs(final_fourier[mode_number, 0, 0]) / grid_size**3
    )
    measured_ratio = float(final_mode / initial_mode)
    continuum_ratio = float(
        PREVIOUS.growth(final_scale_factor)[0] / growth_initial
    )
    discrete_ratio = independent_linear_growth_ratio(
        mesh_response, A_INITIAL, final_scale_factor
    )
    return {
        "mode_number": float(mode_number),
        "mesh_response": mesh_response,
        "measured_ratio": measured_ratio,
        "continuum_ratio": continuum_ratio,
        "discrete_ratio": discrete_ratio,
        "continuum_error": abs(measured_ratio / continuum_ratio - 1.0),
        "discrete_error": abs(measured_ratio / discrete_ratio - 1.0),
    }


def particle_mesh_equation_controls() -> tuple[
    list[dict[str, Any]], dict[str, float]
]:
    homogeneous_grid = 32
    homogeneous_box = 10.0
    homogeneous_positions = particle_lattice(
        homogeneous_grid, homogeneous_box, offset_cells=0.25
    )
    homogeneous_force, _ = particle_mesh_force(
        homogeneous_positions, homogeneous_grid, homogeneous_box
    )
    homogeneous_force_maximum = float(
        np.max(np.linalg.norm(homogeneous_force, axis=1))
    )
    long_mode = linear_mode_diagnostic(1)
    mesh_mode = linear_mode_diagnostic(2)
    response_ordered = (
        0.0
        < mesh_mode["mesh_response"]
        < long_mode["mesh_response"]
        <= 1.0
    )
    controls = [
        {
            "control_id": "homogeneous_force",
            "mode_number": "",
            "measured": homogeneous_force_maximum,
            "expected": 0.0,
            "relative_or_absolute_error": homogeneous_force_maximum,
            "continuum_error": "",
            "mesh_response_mu": "",
            "status": "PASS"
            if homogeneous_force_maximum < 1.0e-12
            else "FAIL",
            "acceptance_role": "uniform-density zero-force control",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "control_id": "linear_long_mode_continuum_growth",
            "mode_number": 1,
            "measured": long_mode["measured_ratio"],
            "expected": long_mode["continuum_ratio"],
            "relative_or_absolute_error": long_mode["continuum_error"],
            "continuum_error": long_mode["continuum_error"],
            "mesh_response_mu": long_mode["mesh_response"],
            "status": "PASS"
            if long_mode["continuum_error"] < 0.03
            else "FAIL",
            "acceptance_role": "resolved long-wave continuum growth",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "control_id": "linear_mesh_mode_discrete_growth",
            "mode_number": 2,
            "measured": mesh_mode["measured_ratio"],
            "expected": mesh_mode["discrete_ratio"],
            "relative_or_absolute_error": mesh_mode["discrete_error"],
            "continuum_expected": mesh_mode["continuum_ratio"],
            "continuum_error": mesh_mode["continuum_error"],
            "mesh_response_mu": mesh_mode["mesh_response"],
            "status": "PASS"
            if mesh_mode["discrete_error"] < 0.03
            else "FAIL",
            "acceptance_role": (
                "finite CIC and central-difference operator response"
            ),
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "control_id": "linear_mesh_response_ordering",
            "mode_number": "1,2",
            "measured": (
                f"{long_mode['mesh_response']};"
                f"{mesh_mode['mesh_response']}"
            ),
            "expected": "0 < mu_2 < mu_1 <= 1",
            "relative_or_absolute_error": 0.0
            if response_ordered
            else 1.0,
            "continuum_error": "",
            "mesh_response_mu": "",
            "status": "PASS" if response_ordered else "FAIL",
            "acceptance_role": "derived finite-mesh attenuation ordering",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
    ]
    summary = {
        "homogeneous_force_maximum": homogeneous_force_maximum,
        "linear_long_mode_continuum_error": long_mode[
            "continuum_error"
        ],
        "linear_mesh_mode_discrete_error": mesh_mode["discrete_error"],
        "linear_mesh_mode_continuum_attenuation": mesh_mode[
            "continuum_error"
        ],
        "linear_long_mode_mesh_response": long_mode["mesh_response"],
        "linear_test_mode_mesh_response": mesh_mode["mesh_response"],
    }
    return controls, summary


def periodic_center(points: np.ndarray, box_size: float) -> np.ndarray:
    angles = 2.0 * math.pi * points / box_size
    mean_phase = np.mean(np.exp(1j * angles), axis=0)
    return np.mod(np.angle(mean_phase), 2.0 * math.pi) * box_size / (
        2.0 * math.pi
    )


def shrinking_center(
    tagged_positions: np.ndarray,
    box_size: float,
) -> tuple[np.ndarray, int]:
    selected = tagged_positions
    center = periodic_center(selected, box_size)
    iterations = 0
    while len(selected) > 1200 and iterations < 20:
        offsets = periodic_displacements(selected, center, box_size)
        radii = np.linalg.norm(offsets, axis=1)
        keep_count = max(1200, int(0.75 * len(selected)))
        keep = np.argpartition(radii, keep_count - 1)[:keep_count]
        selected = selected[keep]
        center = periodic_center(selected, box_size)
        iterations += 1
    return center, iterations


def halo_profile(
    positions: np.ndarray,
    tagged: np.ndarray,
    particle_grid: int,
    force_grid: int,
    box_size: float,
) -> dict[str, Any]:
    center, center_iterations = shrinking_center(positions[tagged], box_size)
    offsets = periodic_displacements(positions, center, box_size)
    radii = np.linalg.norm(offsets, axis=1)
    particle_mass = RHO_M_MSUN_MPC3 * box_size**3 / particle_grid**3
    force_spacing = box_size / force_grid
    minimum = 0.5 * force_spacing
    maximum = 0.49 * box_size
    edges = np.geomspace(minimum, maximum, PROFILE_BINS + 1)
    centers = np.sqrt(edges[:-1] * edges[1:])
    counts = np.histogram(radii, bins=edges)[0]
    volumes = 4.0 * math.pi * (edges[1:] ** 3 - edges[:-1] ** 3) / 3.0
    total_density = counts * particle_mass / volumes
    excess_density = total_density - RHO_M_MSUN_MPC3
    sorted_radii = np.sort(radii)
    cumulative_counts = np.searchsorted(sorted_radii, centers, side="right")
    total_mass = cumulative_counts * particle_mass
    background_mass = 4.0 * math.pi * RHO_M_MSUN_MPC3 * centers**3 / 3.0
    excess_mass = total_mass - background_mass
    motion_excess_mass = MOTION_FRACTION * np.maximum(excess_mass, 0.0)
    motion_velocity_squared = (
        G_MPC_KM2_S2_MSUN * motion_excess_mass / centers
    )
    return {
        "center_Mpc": center,
        "center_iterations": center_iterations,
        "radius_Mpc": centers,
        "particle_count": counts,
        "total_density_Msun_Mpc3": total_density,
        "excess_density_total_Msun_Mpc3": excess_density,
        "total_mass_Msun": total_mass,
        "excess_mass_total_Msun": excess_mass,
        "motion_excess_mass_Msun": motion_excess_mass,
        "motion_velocity_squared_km2_s2": motion_velocity_squared,
        "force_spacing_Mpc": force_spacing,
        "resolved_radius_Mpc": RESOLVED_FORCE_CELLS * force_spacing,
        "particle_mass_Msun": particle_mass,
        "tagged_particle_count": int(np.count_nonzero(tagged)),
    }


def direct_annulus_density(
    positions: np.ndarray,
    center: np.ndarray,
    box_size: float,
    particle_mass: float,
    lower: float,
    upper: float,
) -> float:
    radii = np.linalg.norm(
        periodic_displacements(positions, center, box_size), axis=1
    )
    count = int(np.count_nonzero((radii >= lower) & (radii < upper)))
    volume = 4.0 * math.pi * (upper**3 - lower**3) / 3.0
    return count * particle_mass / volume - RHO_M_MSUN_MPC3


def run_configuration(
    config_id: str,
    mass_label: str,
    pair_sign: int,
    particle_grid: int,
    force_grid: int,
    steps: int,
    box_size: float,
    patch_radius: float,
    initial: dict[str, Any],
    target_edge_radius: float,
) -> dict[str, Any]:
    evolved = evolve_particle_mesh(
        np.asarray(initial["positions"], dtype=float),
        np.asarray(initial["momenta"], dtype=float),
        force_grid,
        box_size,
        steps,
    )
    profile = halo_profile(
        np.asarray(evolved["positions"], dtype=float),
        np.asarray(initial["tagged"], dtype=bool),
        particle_grid,
        force_grid,
        box_size,
    )
    center = np.asarray(profile["center_Mpc"], dtype=float)
    particle_mass = float(profile["particle_mass_Msun"])
    inner_density = direct_annulus_density(
        np.asarray(evolved["positions"]),
        center,
        box_size,
        particle_mass,
        0.70 * target_edge_radius,
        0.90 * target_edge_radius,
    )
    outer_density = direct_annulus_density(
        np.asarray(evolved["positions"]),
        center,
        box_size,
        particle_mass,
        1.05 * target_edge_radius,
        1.30 * target_edge_radius,
    )
    return {
        "config_id": config_id,
        "mass_label": mass_label,
        "pair_sign": pair_sign,
        "particle_grid": particle_grid,
        "force_grid": force_grid,
        "steps": steps,
        "box_size_Mpc": box_size,
        "patch_radius_Mpc": patch_radius,
        "particle_count": particle_grid**3,
        "force_cell_kpc": 1000.0 * box_size / force_grid,
        "resolved_radius_kpc": 1000.0 * float(profile["resolved_radius_Mpc"]),
        "tagged_particle_count": int(profile["tagged_particle_count"]),
        "wall_seconds": float(evolved["wall_seconds"]),
        "initial_force_mean_norm": evolved["initial_force_diagnostics"][
            "force_mean_norm"
        ],
        "final_force_mean_norm": evolved["final_force_diagnostics"][
            "force_mean_norm"
        ],
        "final_density_maximum": evolved["final_force_diagnostics"][
            "density_maximum"
        ],
        "halo_center_x_Mpc": center[0],
        "halo_center_y_Mpc": center[1],
        "halo_center_z_Mpc": center[2],
        "inner_edge_excess_density_total_Msun_Mpc3": inner_density,
        "outer_edge_excess_density_total_Msun_Mpc3": outer_density,
        "outer_to_inner_excess_density_ratio": outer_density / inner_density
        if inner_density > 0.0
        else math.nan,
        "positions": evolved["positions"],
        "profile": profile,
    }


def pair_mean_profile(
    minus_run: dict[str, Any],
    plus_run: dict[str, Any],
) -> dict[str, Any]:
    minus = minus_run["profile"]
    plus = plus_run["profile"]
    radius = np.asarray(minus["radius_Mpc"], dtype=float)
    if not np.allclose(radius, plus["radius_Mpc"], rtol=0.0, atol=1.0e-14):
        raise RuntimeError("paired profile radii differ")
    fields = {}
    for field in (
        "particle_count",
        "excess_density_total_Msun_Mpc3",
        "motion_excess_mass_Msun",
        "motion_velocity_squared_km2_s2",
    ):
        fields[field] = 0.5 * (
            np.asarray(minus[field], dtype=float)
            + np.asarray(plus[field], dtype=float)
        )
    return {
        "radius_Mpc": radius,
        **fields,
        "resolved_radius_Mpc": max(
            float(minus["resolved_radius_Mpc"]),
            float(plus["resolved_radius_Mpc"]),
        ),
        "particle_mass_Msun": float(minus["particle_mass_Msun"]),
        "outer_to_inner_excess_density_ratio": 0.5
        * (
            float(minus_run["outer_to_inner_excess_density_ratio"])
            + float(plus_run["outer_to_inner_excess_density_ratio"])
        )
        if math.isfinite(float(minus_run["outer_to_inner_excess_density_ratio"]))
        and math.isfinite(float(plus_run["outer_to_inner_excess_density_ratio"]))
        else math.nan,
    }


def score_pair_mean(
    config_id: str,
    mass_label: str,
    mapping: str,
    pair_profile: dict[str, Any],
    target: dict[str, Any],
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    radius = np.asarray(pair_profile["radius_Mpc"], dtype=float)
    excess_density = MOTION_FRACTION * np.asarray(
        pair_profile["excess_density_total_Msun_Mpc3"], dtype=float
    )
    motion_mass = np.asarray(pair_profile["motion_excess_mass_Msun"], dtype=float)
    velocity_squared = np.asarray(
        pair_profile["motion_velocity_squared_km2_s2"], dtype=float
    )
    counts = np.asarray(pair_profile["particle_count"], dtype=float)
    target_radius = np.asarray(target["radius_Mpc"], dtype=float)
    target_density = np.asarray(target["density_motion_Msun_Mpc3"], dtype=float)
    target_mass = np.asarray(target["mass_motion_Msun"], dtype=float)
    target_velocity = np.asarray(target["velocity_squared_km2_s2"], dtype=float)
    edge_radius = float(target["edge_radius_Mpc"])
    transition_radius = float(target["transition_radius_Mpc"])
    resolved_radius = float(pair_profile["resolved_radius_Mpc"])
    target_density_i = np.interp(radius, target_radius, target_density, left=target_density[0], right=0.0)
    target_mass_i = np.interp(radius, target_radius, target_mass, left=0.0, right=target_mass[-1])
    target_velocity_i = np.interp(radius, target_radius, target_velocity, left=0.0, right=target_velocity[-1])
    valid = (
        (radius >= resolved_radius)
        & (radius <= 0.9 * edge_radius)
        & (counts >= 4.0)
        & (excess_density > 0.0)
        & (velocity_squared > 0.0)
        & (target_density_i > 0.0)
        & (target_velocity_i > 0.0)
    )
    if np.count_nonzero(valid) >= 3:
        velocity_rmse = float(
            np.sqrt(
                np.mean(
                    np.log10(velocity_squared[valid] / target_velocity_i[valid])
                    ** 2
                )
            )
        )
        density_rmse = float(
            np.sqrt(
                np.mean(
                    np.log10(excess_density[valid] / target_density_i[valid])
                    ** 2
                )
            )
        )
    else:
        velocity_rmse = math.nan
        density_rmse = math.nan
    edge_motion_mass = float(np.interp(edge_radius, radius, motion_mass))
    outer_ratio = float(pair_profile["outer_to_inner_excess_density_ratio"])
    transition_resolved = transition_radius >= resolved_radius
    score = {
        "config_id": config_id,
        "mass_label": mass_label,
        "mapping_scored": mapping,
        "q_parent": float(target["q_parent"]),
        "target_edge_power": float(target["edge_power"]),
        "target_transition_radius_kpc": 1000.0 * transition_radius,
        "target_edge_radius_kpc": 1000.0 * edge_radius,
        "resolved_radius_kpc": 1000.0 * resolved_radius,
        "transition_resolved": transition_resolved,
        "resolved_profile_bins": int(np.count_nonzero(valid)),
        "density_log10_RMSE_no_refit": density_rmse,
        "velocity_squared_log10_RMSE_no_refit": velocity_rmse,
        "motion_mass_inside_fixed_edge_Msun": edge_motion_mass,
        "target_motion_mass_edge_Msun": float(target["edge_mass_motion_Msun"]),
        "mass_ratio_inside_fixed_edge": edge_motion_mass
        / float(target["edge_mass_motion_Msun"]),
        "outer_to_inner_excess_density_ratio": outer_ratio,
        "compact_edge_threshold_pass": bool(
            math.isfinite(outer_ratio) and 0.0 <= outer_ratio < 1.0e-3
        ),
        "q_parent_dynamically_scored": False,
        "no_refit": True,
        "valid_for_claim": False,
        "valid_for_galaxy_claim": False,
        "checkpoint_marker": MARKER,
    }
    rows: list[dict[str, Any]] = []
    for index in range(len(radius)):
        rows.append(
            {
                "config_id": config_id,
                "mass_label": mass_label,
                "mapping_scored": mapping,
                "radius_kpc": 1000.0 * radius[index],
                "radius_over_target_Rn": radius[index] / transition_radius,
                "radius_over_target_Redge": radius[index] / edge_radius,
                "paired_mean_particle_count": counts[index],
                "paired_mean_motion_excess_density_Msun_Mpc3": excess_density[index],
                "target_motion_density_Msun_Mpc3": target_density_i[index],
                "paired_mean_motion_excess_mass_Msun": motion_mass[index],
                "target_motion_mass_Msun": target_mass_i[index],
                "paired_mean_motion_v2_km2_s2": velocity_squared[index],
                "target_motion_v2_km2_s2": target_velocity_i[index],
                "inside_resolved_scoring_window": bool(valid[index]),
                "valid_for_claim": False,
                "valid_for_galaxy_claim": False,
                "checkpoint_marker": MARKER,
            }
        )
    return score, rows


def public_run_row(run: dict[str, Any]) -> dict[str, Any]:
    fields = (
        "config_id",
        "mass_label",
        "pair_sign",
        "particle_grid",
        "force_grid",
        "steps",
        "box_size_Mpc",
        "patch_radius_Mpc",
        "particle_count",
        "force_cell_kpc",
        "resolved_radius_kpc",
        "tagged_particle_count",
        "wall_seconds",
        "initial_force_mean_norm",
        "final_force_mean_norm",
        "final_density_maximum",
        "halo_center_x_Mpc",
        "halo_center_y_Mpc",
        "halo_center_z_Mpc",
        "inner_edge_excess_density_total_Msun_Mpc3",
        "outer_edge_excess_density_total_Msun_Mpc3",
        "outer_to_inner_excess_density_ratio",
    )
    return {
        **{field: run[field] for field in fields},
        "no_refit": True,
        "valid_for_claim": False,
        "valid_for_galaxy_claim": False,
        "checkpoint_marker": MARKER,
    }


def contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "C5160_00_equations",
            "quantity": "dynamics",
            "frozen_value": "periodic 3D Vlasov-Poisson particle mesh from checkpoint 5155",
            "post_evolution_fit": False,
            "claim_limit": "collisionless outer branch; no wave-core resolution",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "contract_id": "C5160_01_covariance",
            "quantity": "initial field",
            "frozen_value": "5156 CAMB times Hu-FDM power with exact Hoffman-Ribak top-hat constraint",
            "post_evolution_fit": False,
            "claim_limit": "empirical adiabatic comparator remains conditional",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "contract_id": "C5160_02_phase_pair",
            "quantity": "residual covariance",
            "frozen_value": f"seed={FIXED_SEED}; signs=-1,+1 around one conditional mean",
            "post_evolution_fit": False,
            "claim_limit": "paired realization controls phase variance but is not an ensemble",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "contract_id": "C5160_03_reference",
            "quantity": "halo row",
            "frozen_value": REFERENCE_GALAXY,
            "post_evolution_fit": False,
            "claim_limit": "deterministic maximum Rn/RL resolution reference selected at 5159",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "contract_id": "C5160_04_matrix",
            "quantity": "mass/resolution/time matrix",
            "frozen_value": (
                "three masses at 64^3/128^3/120 plus paired "
                "force/time/particle controls"
            ),
            "post_evolution_fit": False,
            "claim_limit": "only radii beyond three force cells may be scored",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "contract_id": "C5160_05_targets",
            "quantity": "q, Rn, Redge and p=2",
            "frozen_value": "checkpoint-5154 target profiles for both parent mappings",
            "post_evolution_fit": False,
            "claim_limit": "q cannot be scored if Rn lies below resolved radius",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "contract_id": "C5160_06_machine_cog",
            "quantity": "local branch",
            "frozen_value": "same 5157 Cartesian GR/Newton/Maxwell zero state",
            "post_evolution_fit": False,
            "claim_limit": "no galaxy-only G, charge, metric or EM modification",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "contract_id": "C5160_07_initialization",
            "quantity": "initial scale factor and quality gates",
            "frozen_value": (
                f"a_initial={A_INITIAL}; |delta_initial|<0.8; "
                "maximum displacement<1 particle cell"
            ),
            "post_evolution_fit": False,
            "claim_limit": (
                "a_initial repaired from 0.02 after predeclared controls "
                "failed; no profile threshold changed"
            ),
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
    ]


def cog_rows() -> list[dict[str, Any]]:
    return [
        {
            "arena": "Mercury_local_GR_Newton",
            "state": "zero motion occupation",
            "same_parent_action": True,
            "new_parameter": False,
            "status": "UNCHANGED",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "arena": "Maxwell_Poynting",
            "state": "same universal Hilbert source",
            "same_parent_action": True,
            "new_parameter": False,
            "status": "UNCHANGED",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "arena": "galactic_collapse",
            "state": "paired nonzero constrained occupation",
            "same_parent_action": True,
            "new_parameter": False,
            "status": "EXECUTED_CONDITIONALLY",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
    ]


def add_validation(
    rows: list[dict[str, Any]], name: str, passed: bool, detail: Any
) -> None:
    rows.append(
        {
            "check_id": f"V5160_{len(rows) + 1:02d}_{name}",
            "passed": bool(passed),
            "detail": str(detail),
            "checkpoint_marker": MARKER,
        }
    )


def make_document(result: dict[str, Any]) -> str:
    summary = result["summary"]
    return f"""# 5160 - Paired 3-D constrained-realization particle-mesh collapse and tidal-profile gate

Marker: `{MARKER}`.

Date: `{CHECKED_DATE}`.

## Decision

Checkpoint 5160 executes the nonspherical route demanded by checkpoint 5159.
It retains the residual Gaussian covariance, conditions the same one-sigma
UGC09133 Lagrangian patch, evolves antithetic phase realizations under the
same periodic Vlasov--Poisson law and measures a three-dimensional halo centre
after tidal evolution. No profile parameter is read back into the run.

The result is an outer-halo comparator, not a wave-core calculation. Every
transition radius `R_n` lies below the declared three-force-cell resolution
floor, so no numerical `q_parent` verdict is permitted.

## 1. Exact paired constraint

For a raw Gaussian field `delta_r` and top-hat functional `C`, the implemented
Hoffman--Ribak residual is

```text
delta_res=delta_r-C[delta_r] Cov(delta,C)/Var(C),
C[delta_res]=0.
```

The continuous source-backed conditional mean is then added with signs
`+delta_res` and `-delta_res`. Their mean is exactly the constrained mean.
Across the generated states, the maximum constraint error is
`{summary['maximum_constraint_error']}`, pair-mean error is
`{summary['maximum_pair_mean_error']}` and residual antisymmetry error is
`{summary['maximum_residual_antisymmetry_error']}`.

The finite periodic box contains between
`{summary['minimum_box_to_full_sigma']}` and
`{summary['maximum_box_to_full_sigma']}` of the full top-hat sigma. Missing
long covariance is carried only by the source-integrated conditional mean;
the residual realization is not falsely labelled a complete cosmological
volume.

## 2. Three-dimensional equations executed

Zel'dovich positions and canonical momenta are generated from the full 3-D
density field. The KDK particle mesh evolves

```text
dx/da=P/(a^3 E),
dP/da=F/(a^2 E),
nabla^2 chi=(3/2) Omega_m delta,
F=-nabla chi.
```

CIC assignment and interpolation use the same periodic mesh. The main matrix
contains `{summary['run_count']}` runs and
`{summary['total_particle_updates']}` particle-step updates. The homogeneous
force control is `{summary['homogeneous_force_maximum']}`. The longest tested
mode follows continuum growth with relative error
`{summary['linear_long_mode_continuum_error']}`. The second mode follows the
independently integrated finite-mesh response with error
`{summary['linear_mesh_mode_discrete_error']}`; its separately recorded
continuum attenuation is
`{summary['linear_mesh_mode_continuum_attenuation']}`. This distinction avoids
mistaking the derived CIC/central-difference transfer for a cosmological-force
failure.

## 3. No-refit outer profile

The paired mean is scored against both frozen parent mappings. Resolved profile
bins range from `{summary['minimum_resolved_profile_bins']}` to
`{summary['maximum_resolved_profile_bins']}`. The base three-mass fixed-edge
motion-mass ratio spans `{summary['minimum_base_edge_mass_ratio']}` to
`{summary['maximum_base_edge_mass_ratio']}` and the finite velocity log-RMSE
spans `{summary['minimum_base_velocity_log_RMSE']}` to
`{summary['maximum_base_velocity_log_RMSE']}` dex.

The compact-edge threshold passes in
`{summary['compact_edge_pass_count']}` of `{summary['score_count']}` scores.
The smallest paired exterior/interior excess-density ratio is
`{summary['minimum_outer_edge_ratio']}`.

These numbers are used only if the paired force/time convergence gate closes.
That gate is `{summary['convergence_status']}`: its fixed-edge mass-ratio span
is `{summary['convergence_edge_mass_ratio_span']}` and its exterior-ratio span
is `{summary['convergence_outer_ratio_span']}`. Quantitative outer-profile
claims remain `{summary['quantitative_profile_status']}`.

The pass is deliberately narrower than full particle convergence: it covers
force and time controls at fixed `64^3` particle phases. The `96^3` run adds
short modes and is recorded as non-phase-matched, so it cannot be used as a
strict one-variable convergence comparison. A nested shared-mode realization
is still required before the conditional outer result can be called universal.

## 4. What this proves and does not prove

The calculation removes the exact `L=0` obstruction of the radial mean:
nonspherical residual modes generate tidal forces and nonradial particle
motion. It does not prove an isotropic Eddington distribution, a universal
attractor or a wave core. The paired realization is one antithetic control,
not a sufficient cosmic-variance ensemble.

```text
paired residual covariance retained                  = yes;
three-dimensional tidal evolution executed           = yes;
profile parameters fitted after evolution             = no;
q_parent transition resolved                          = no;
outer profile convergence gate                        = {summary['convergence_status']};
compact p=2 edge selected                              = {summary['compact_edge_verdict']};
wave/density-matrix core selected                      = no;
parent primordial covariance derived                  = no.
```

## 5. Machine-cog verdict

The simulation changes only the nonzero cosmological state. The action,
metric rank, `G_N`, visible matter coupling and Maxwell/Poynting Hilbert source
remain untouched. The same Cartesian zero state therefore retains the local
GR/Newton/Mercury cog while the occupied branch is tested for galactic
formation.

This is the single-machine criterion: no arena-specific law is switched on.
The same parent equations must leave the Mercury cog turning and generate any
galactic activation only through their nonzero state and inherited scales.

If the outer convergence gate fails, the next step is numerical repair before
any theory inference. If it closes but the edge fails, the free collisionless
parent does not derive the checkpoint-5154 compact edge and the missing parent
interaction must be identified explicitly. A wave zoom is legitimate only
after that outer arbitration.

Primary method references:

- constrained Gaussian fields: {PRIMARY_URLS['constrained_realizations']}
- particle mesh evolution: {PRIMARY_URLS['particle_mesh']}
- FDM transfer: {PRIMARY_URLS['fuzzy_transfer']}

All `{result['validation_count']}` validations pass. Every row remains
nonclaim. The protected `formalization-workbench` digest is
`{result['formalization_workbench_tree_sha256']}`. Galaxy sources were
read-only and no GitHub action occurred.
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
    formal_before = tree_digest(FORMAL)
    if formal_before != FORMAL_DIGEST_LOCK:
        raise RuntimeError(f"protected digest mismatch: {formal_before}")
    hashes_before = {key: file_digest(path) for key, path in paths.items()}
    power_rows = read_csv(POWER_CSV)
    patch_rows = read_csv(PATCH_CSV)
    halo_rows = read_csv(HALO_CSV)
    eddington_rows = read_csv(EDDINGTON_CSV)
    power = power_lookup(power_rows)
    patch_lookup = {
        (row["galaxy"], row["mapping"], row["mass_label"]): row
        for row in patch_rows
    }
    halo_lookup = {
        (row["galaxy"], row["mapping"], row["mass_label"]): row
        for row in halo_rows
    }
    eddington_lookup = {
        (row["galaxy"], row["mapping"], row["mass_label"], row["edge_power"]): row
        for row in eddington_rows
    }
    if arguments.dry_run:
        print(
            json.dumps(
                {
                    "dry_run": True,
                    "reference_galaxy": REFERENCE_GALAXY,
                    "seed": FIXED_SEED,
                    "mass_labels": MASS_LABELS,
                    "base_particle_grid": BASE_PARTICLE_GRID,
                    "base_force_grid": BASE_FORCE_GRID,
                    "base_steps": BASE_STEPS,
                    "initial_scale_factor": A_INITIAL,
                    "formal_digest": formal_before,
                },
                indent=2,
            )
        )
        return
    if arguments.controls_only:
        controls, control_summary = particle_mesh_equation_controls()
        print(
            json.dumps(
                {
                    "controls_only": True,
                    "initial_scale_factor": A_INITIAL,
                    "controls": controls,
                    "summary": control_summary,
                    "all_controls_pass": all(
                        row["status"] == "PASS" for row in controls
                    ),
                },
                indent=2,
            )
        )
        if not all(row["status"] == "PASS" for row in controls):
            raise RuntimeError("particle-mesh equation control failure")
        return
    contract = contract_rows()
    cogs = cog_rows()
    provenance = provenance_rows(paths)
    configurations = [
        {
            "config_id": "BASE",
            "particle_grid": BASE_PARTICLE_GRID,
            "force_grid": BASE_FORCE_GRID,
            "steps": BASE_STEPS,
            "masses": MASS_LABELS,
            "strict_convergence": True,
        },
        {
            "config_id": "FORCE_LOW",
            "particle_grid": BASE_PARTICLE_GRID,
            "force_grid": LOW_FORCE_GRID,
            "steps": BASE_STEPS,
            "masses": (BENCHMARK_MASS,),
            "strict_convergence": True,
        },
        {
            "config_id": "FORCE_HIGH",
            "particle_grid": BASE_PARTICLE_GRID,
            "force_grid": HIGH_FORCE_GRID,
            "steps": BASE_STEPS,
            "masses": (BENCHMARK_MASS,),
            "strict_convergence": True,
        },
        {
            "config_id": "TIME_DOUBLE",
            "particle_grid": BASE_PARTICLE_GRID,
            "force_grid": BASE_FORCE_GRID,
            "steps": DOUBLE_STEPS,
            "masses": (BENCHMARK_MASS,),
            "strict_convergence": True,
        },
        {
            "config_id": "PARTICLE_HIGH",
            "particle_grid": HIGH_PARTICLE_GRID,
            "force_grid": HIGH_PARTICLE_FORCE_GRID,
            "steps": HIGH_PARTICLE_STEPS,
            "masses": (BENCHMARK_MASS,),
            "strict_convergence": False,
        },
    ]
    initial_cache: dict[tuple[str, int], dict[int, dict[str, Any]]] = {}
    initial_diagnostics: list[dict[str, Any]] = []
    runs: list[dict[str, Any]] = []
    pair_profiles: dict[tuple[str, str], dict[str, Any]] = {}
    targets: dict[tuple[str, str], dict[str, Any]] = {}
    for mass_label in MASS_LABELS:
        for mapping in MAPPINGS:
            targets[(mass_label, mapping)] = PREVIOUS.target_profile(
                halo_lookup[(REFERENCE_GALAXY, mapping, mass_label)],
                eddington_lookup[(REFERENCE_GALAXY, mapping, mass_label, "2.0")],
            )
    for configuration in configurations:
        config_id = str(configuration["config_id"])
        particle_grid = int(configuration["particle_grid"])
        force_grid = int(configuration["force_grid"])
        steps = int(configuration["steps"])
        for mass_label in configuration["masses"]:
            patch = patch_lookup[
                (REFERENCE_GALAXY, REFERENCE_MAPPING, mass_label)
            ]
            patch_radius = float(patch["Lagrangian_patch_radius_Mpc"])
            box_size = BOX_OVER_PATCH * patch_radius
            cache_key = (mass_label, particle_grid)
            if cache_key not in initial_cache:
                fields, diagnostics = build_conditioned_pair(
                    particle_grid,
                    box_size,
                    patch_radius,
                    float(patch["sigma_MTS_empirical_adiabatic"]),
                    power[mass_label]["k"],
                    power[mass_label]["power"],
                )
                initial_cache[cache_key] = {}
                for pair_sign in PAIR_SIGNS:
                    state = initial_particle_state(
                        fields[pair_sign], box_size, patch_radius
                    )
                    initial_cache[cache_key][pair_sign] = state
                    initial_diagnostics.append(
                        {
                            "mass_label": mass_label,
                            "particle_grid": particle_grid,
                            "pair_sign": pair_sign,
                            **diagnostics,
                            "growth_initial": state["growth_initial"],
                            "maximum_initial_displacement_cells": state[
                                "maximum_initial_displacement_cells"
                            ],
                            "initial_scaled_delta_minimum": state[
                                "initial_scaled_delta_minimum"
                            ],
                            "initial_scaled_delta_maximum": state[
                                "initial_scaled_delta_maximum"
                            ],
                            "tagged_particle_count": state[
                                "tagged_particle_count"
                            ],
                            "valid_for_claim": False,
                            "checkpoint_marker": MARKER,
                        }
                    )
                del fields
                gc.collect()
            target_edge = float(
                targets[(mass_label, REFERENCE_MAPPING)]["edge_radius_Mpc"]
            )
            pair_runs: dict[int, dict[str, Any]] = {}
            for pair_sign in PAIR_SIGNS:
                run = run_configuration(
                    config_id,
                    mass_label,
                    pair_sign,
                    particle_grid,
                    force_grid,
                    steps,
                    box_size,
                    patch_radius,
                    initial_cache[cache_key][pair_sign],
                    target_edge,
                )
                runs.append(run)
                pair_runs[pair_sign] = run
            pair_profiles[(config_id, mass_label)] = pair_mean_profile(
                pair_runs[-1], pair_runs[1]
            )
    controls, control_summary = particle_mesh_equation_controls()
    homogeneous_force_maximum = control_summary[
        "homogeneous_force_maximum"
    ]
    scores: list[dict[str, Any]] = []
    profile_rows: list[dict[str, Any]] = []
    for (config_id, mass_label), paired in pair_profiles.items():
        for mapping in MAPPINGS:
            score, rows = score_pair_mean(
                config_id,
                mass_label,
                mapping,
                paired,
                targets[(mass_label, mapping)],
            )
            scores.append(score)
            profile_rows.extend(rows)
    convergence_rows: list[dict[str, Any]] = []
    strict_configurations = {
        str(configuration["config_id"])
        for configuration in configurations
        if bool(configuration["strict_convergence"])
    }
    for score in scores:
        if score["mass_label"] != BENCHMARK_MASS or score["mapping_scored"] != REFERENCE_MAPPING:
            continue
        convergence_rows.append(
            {
                "config_id": score["config_id"],
                "strict_phase_matched_control": score["config_id"]
                in strict_configurations,
                "resolved_radius_kpc": score["resolved_radius_kpc"],
                "resolved_profile_bins": score["resolved_profile_bins"],
                "fixed_edge_mass_ratio": score["mass_ratio_inside_fixed_edge"],
                "velocity_log10_RMSE": score[
                    "velocity_squared_log10_RMSE_no_refit"
                ],
                "outer_to_inner_excess_density_ratio": score[
                    "outer_to_inner_excess_density_ratio"
                ],
                "compact_edge_threshold_pass": score[
                    "compact_edge_threshold_pass"
                ],
                "valid_for_claim": False,
                "checkpoint_marker": MARKER,
            }
        )
    strict_rows = [
        row for row in convergence_rows if row["strict_phase_matched_control"]
    ]
    strict_mass_ratios = [float(row["fixed_edge_mass_ratio"]) for row in strict_rows]
    strict_outer_ratios = [
        float(row["outer_to_inner_excess_density_ratio"])
        for row in strict_rows
        if math.isfinite(float(row["outer_to_inner_excess_density_ratio"]))
    ]
    convergence_mass_span = max(strict_mass_ratios) - min(strict_mass_ratios)
    convergence_outer_span = max(strict_outer_ratios) - min(strict_outer_ratios)
    convergence_passed = (
        convergence_mass_span < 0.10 and convergence_outer_span < 0.10
    )
    base_scores = [row for row in scores if row["config_id"] == "BASE"]
    finite_base_velocity = [
        float(row["velocity_squared_log10_RMSE_no_refit"])
        for row in base_scores
        if math.isfinite(float(row["velocity_squared_log10_RMSE_no_refit"]))
    ]
    finite_outer = [
        float(row["outer_to_inner_excess_density_ratio"])
        for row in scores
        if math.isfinite(float(row["outer_to_inner_excess_density_ratio"]))
    ]
    summary = {
        "run_count": len(runs),
        "pair_profile_count": len(pair_profiles),
        "score_count": len(scores),
        "profile_row_count": len(profile_rows),
        "total_particle_updates": sum(
            int(run["particle_count"]) * int(run["steps"]) for run in runs
        ),
        "maximum_constraint_error": max(
            float(row["maximum_constraint_error"])
            for row in initial_diagnostics
        ),
        "maximum_pair_mean_error": max(
            float(row["pair_mean_error"]) for row in initial_diagnostics
        ),
        "maximum_residual_antisymmetry_error": max(
            float(row["residual_antisymmetry_error"])
            for row in initial_diagnostics
        ),
        "minimum_box_to_full_sigma": min(
            float(row["box_to_full_sigma"]) for row in initial_diagnostics
        ),
        "maximum_box_to_full_sigma": max(
            float(row["box_to_full_sigma"]) for row in initial_diagnostics
        ),
        "homogeneous_force_maximum": homogeneous_force_maximum,
        "linear_long_mode_continuum_error": control_summary[
            "linear_long_mode_continuum_error"
        ],
        "linear_mesh_mode_discrete_error": control_summary[
            "linear_mesh_mode_discrete_error"
        ],
        "linear_mesh_mode_continuum_attenuation": control_summary[
            "linear_mesh_mode_continuum_attenuation"
        ],
        "linear_long_mode_mesh_response": control_summary[
            "linear_long_mode_mesh_response"
        ],
        "linear_test_mode_mesh_response": control_summary[
            "linear_test_mode_mesh_response"
        ],
        "minimum_resolved_profile_bins": min(
            int(row["resolved_profile_bins"]) for row in scores
        ),
        "maximum_resolved_profile_bins": max(
            int(row["resolved_profile_bins"]) for row in scores
        ),
        "minimum_base_edge_mass_ratio": min(
            float(row["mass_ratio_inside_fixed_edge"]) for row in base_scores
        ),
        "maximum_base_edge_mass_ratio": max(
            float(row["mass_ratio_inside_fixed_edge"]) for row in base_scores
        ),
        "minimum_base_velocity_log_RMSE": min(finite_base_velocity)
        if finite_base_velocity
        else math.nan,
        "maximum_base_velocity_log_RMSE": max(finite_base_velocity)
        if finite_base_velocity
        else math.nan,
        "compact_edge_pass_count": sum(
            bool(row["compact_edge_threshold_pass"]) for row in scores
        ),
        "minimum_outer_edge_ratio": min(finite_outer) if finite_outer else math.nan,
        "convergence_edge_mass_ratio_span": convergence_mass_span,
        "convergence_outer_ratio_span": convergence_outer_span,
        "convergence_status": "PASS" if convergence_passed else "FAIL_CLOSED",
        "quantitative_profile_status": "CONDITIONAL_OUTER_RESULT"
        if convergence_passed
        else "INCONCLUSIVE_PIPELINE",
        "compact_edge_verdict": "NOT_SELECTED_AT_RESOLVED_PM_SCALE"
        if convergence_passed
        and not any(bool(row["compact_edge_threshold_pass"]) for row in strict_rows)
        else "INCONCLUSIVE_UNTIL_CONVERGED",
        "all_transition_radii_unresolved": all(
            not bool(row["transition_resolved"]) for row in scores
        ),
    }
    run_rows = [public_run_row(run) for run in runs]
    generated = {
        CONTRACT_CSV: contract,
        INITIAL_CSV: initial_diagnostics,
        RUN_CSV: run_rows,
        PROFILE_CSV: profile_rows,
        SCORE_CSV: scores,
        CONVERGENCE_CSV: convergence_rows,
        CONTROL_CSV: controls,
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
    formal_after = tree_digest(FORMAL)
    validation: list[dict[str, Any]] = []
    add_validation(validation, "sources_exist", not missing, missing)
    add_validation(validation, "source_hashes_unchanged", hashes_before == hashes_after, hashes_after)
    add_validation(validation, "formalization_workbench_unchanged", formal_after == FORMAL_DIGEST_LOCK, formal_after)
    add_validation(validation, "reference_frozen", REFERENCE_GALAXY == "UGC09133", REFERENCE_GALAXY)
    add_validation(validation, "seed_frozen", FIXED_SEED > 0, FIXED_SEED)
    add_validation(validation, "three_mass_base_matrix", sum(run["config_id"] == "BASE" for run in runs) == 6, len(runs))
    add_validation(validation, "paired_signs_every_configuration", all({run["pair_sign"] for run in runs if run["config_id"] == config and run["mass_label"] == mass} == {-1, 1} for config, mass in pair_profiles), len(pair_profiles))
    add_validation(validation, "constraints_exact", summary["maximum_constraint_error"] < 1.0e-10, summary["maximum_constraint_error"])
    add_validation(validation, "pair_mean_exact", summary["maximum_pair_mean_error"] < 1.0e-12, summary["maximum_pair_mean_error"])
    add_validation(validation, "residuals_antithetic", summary["maximum_residual_antisymmetry_error"] < 1.0e-12, summary["maximum_residual_antisymmetry_error"])
    add_validation(validation, "initial_density_controlled", min(float(row["initial_scaled_delta_minimum"]) for row in initial_diagnostics) > -0.8 and max(float(row["initial_scaled_delta_maximum"]) for row in initial_diagnostics) < 0.8, [min(float(row["initial_scaled_delta_minimum"]) for row in initial_diagnostics), max(float(row["initial_scaled_delta_maximum"]) for row in initial_diagnostics)])
    add_validation(validation, "initial_displacements_controlled", max(float(row["maximum_initial_displacement_cells"]) for row in initial_diagnostics) < 1.0, max(float(row["maximum_initial_displacement_cells"]) for row in initial_diagnostics))
    add_validation(validation, "homogeneous_force_zero", homogeneous_force_maximum < 1.0e-12, homogeneous_force_maximum)
    add_validation(
        validation,
        "linear_mode_growth_controls",
        all(row["status"] == "PASS" for row in controls),
        {
            row["control_id"]: row["relative_or_absolute_error"]
            for row in controls
        },
    )
    add_validation(validation, "force_momentum_balance", max(float(run["final_force_mean_norm"]) for run in runs) < 1.0e-9, max(float(run["final_force_mean_norm"]) for run in runs))
    add_validation(validation, "all_runs_emit_profiles", len(pair_profiles) == 7, len(pair_profiles))
    add_validation(validation, "both_mappings_scored", len(scores) == 14, len(scores))
    add_validation(validation, "all_q_transitions_unresolved", summary["all_transition_radii_unresolved"], [row["resolved_radius_kpc"] for row in scores])
    add_validation(validation, "q_not_falsely_scored", all(not row["q_parent_dynamically_scored"] for row in scores), "all scores")
    add_validation(validation, "no_refit", all(row["no_refit"] for row in scores), "all scores")
    add_validation(validation, "convergence_matrix_complete", len(convergence_rows) == 5 and len(strict_rows) == 4, [len(convergence_rows), len(strict_rows)])
    add_validation(validation, "convergence_status_fail_closed_or_pass", summary["convergence_status"] in {"PASS", "FAIL_CLOSED"}, summary["convergence_status"])
    add_validation(validation, "profile_claim_follows_convergence", (summary["convergence_status"] == "PASS" and summary["quantitative_profile_status"] == "CONDITIONAL_OUTER_RESULT") or (summary["convergence_status"] == "FAIL_CLOSED" and summary["quantitative_profile_status"] == "INCONCLUSIVE_PIPELINE"), summary["quantitative_profile_status"])
    add_validation(validation, "local_machine_cog_unchanged", all(row["same_parent_action"] and not row["new_parameter"] for row in cogs), "three arenas")
    add_validation(validation, "all_rows_nonclaim", all(not row["valid_for_claim"] for rows in generated.values() for row in rows), "all generated rows")
    generated_text = "\n".join(path.read_text(encoding="utf-8") for path in [DOCUMENT, *generated])
    add_validation(validation, "no_placeholders", "MISSING_" not in generated_text and "PLACEHOLDER" not in generated_text, "generated artifacts")
    add_validation(validation, "no_nonfinite_text", "nan" not in generated_text.lower() and "infinity" not in generated_text.lower(), "generated artifacts")
    add_validation(validation, "document_marker", MARKER in DOCUMENT.read_text(encoding="utf-8"), DOCUMENT)
    add_validation(validation, "previous_checkpoint_passed", json.loads(PREVIOUS_RESULT.read_text(encoding="utf-8"))["validation_failures"] == [], PREVIOUS_RESULT)
    add_validation(validation, "galaxy_read_only", hashes_before["galaxy_samples_read_only"] == hashes_after["galaxy_samples_read_only"], hashes_after["galaxy_samples_read_only"])
    add_validation(validation, "claim_flags_false", all(not row["valid_for_galaxy_claim"] for row in scores), "all scores")
    failures = [row["check_id"] for row in validation if not row["passed"]]
    write_csv(VALIDATION_CSV, validation)
    result = {
        "checked_date": CHECKED_DATE,
        "checkpoint_marker": MARKER,
        "route_decision": "PAIRED_3D_PM_EXECUTED_OUTER_RESULT_SUBJECT_TO_CONVERGENCE_WAVE_CORE_STILL_OPEN",
        "paired_3D_tidal_evolution_executed": True,
        "q_parent_dynamically_selected": False,
        "compact_p2_edge_selected": False,
        "wave_core_selected": False,
        "parent_primordial_covariance_derived": False,
        "local_GR_Newton_Maxwell_branch_modified": False,
        "valid_for_galaxy_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
        "fixed_seed": FIXED_SEED,
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
        raise RuntimeError(f"checkpoint 5160 validation failures: {failures}")


if __name__ == "__main__":
    main()
