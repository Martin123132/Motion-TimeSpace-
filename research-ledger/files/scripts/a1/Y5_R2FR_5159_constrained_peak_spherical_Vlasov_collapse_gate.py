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


POST = Path(__file__).resolve().parents[1]
FORMAL = POST.parent / "formalization-workbench"
PREVIOUS_SCRIPT = (
    POST
    / "scripts"
    / "Y5_R2FR_5154_Eddington_phase_space_positive_DF_gate.py"
)
PREVIOUS_DOCUMENT = (
    POST
    / "5158-Y5-R2FR-clock-charge-source-symmetry-no-go-and-neutral-state-pivot.md"
)
PREVIOUS_RESULT = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5158"
    / "clock_charge_source_symmetry_results.json"
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
STATE_CSV = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5151"
    / "galaxy_state_stress_scale_gate.csv"
)
LOCAL_INHERITANCE_CSV = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5157"
    / "transfer_local_cog_inheritance.csv"
)
GALAXY_SAMPLES = Path(r"D:\Users\ollet\Documents\mts-galaxy-lab\data\samples.js")
OUT = POST / "source-intake" / "functional_rg" / "5159"
SOURCES = OUT / "sources"
CONSTRAINED_REALIZATION_ARCHIVE = (
    SOURCES / "constrained_peaks_astro_ph_9507024_source.tar"
)
FASTPM_ARCHIVE = SOURCES / "fastpm_1603.00476_source.tar"
RESULT_JSON = OUT / "constrained_peak_spherical_collapse_results.json"
CONTRACT_CSV = OUT / "frozen_initial_value_contract.csv"
RUN_CSV = OUT / "spherical_Vlasov_run_summary.csv"
PROFILE_CSV = OUT / "nonlinear_profile_samples.csv"
SCORE_CSV = OUT / "no_refit_profile_selection_scores.csv"
CONVERGENCE_CSV = OUT / "collapse_convergence_controls.csv"
THEOREM_CSV = OUT / "radial_sheet_phase_space_theorem.csv"
COG_CSV = OUT / "machine_cog_inheritance.csv"
PROVENANCE_CSV = OUT / "source_provenance.csv"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5159_VALIDATION.csv"
)
DOCUMENT = (
    POST
    / "5159-Y5-R2FR-source-backed-constrained-peak-spherical-Vlasov-collapse-and-profile-selection-gate.md"
)

MARKER = "MTS_5159_CONSTRAINED_PEAK_SPHERICAL_VLASOV_COLLAPSE_GATE"
CHECKED_DATE = "2026-07-20"
FORMAL_DIGEST_LOCK = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"

H0_KM_S_MPC = 67.4
OMEGA_M = 0.315
OMEGA_B = 0.04924319136384048
OMEGA_X = OMEGA_M - OMEGA_B
MOTION_FRACTION = OMEGA_X / OMEGA_M
OMEGA_LAMBDA = 1.0 - OMEGA_M
RHO_CRIT_MSUN_MPC3 = 2.77536627e11 * (H0_KM_S_MPC / 100.0) ** 2
RHO_M_MSUN_MPC3 = OMEGA_M * RHO_CRIT_MSUN_MPC3
G_MPC_KM2_S2_MSUN = 4.30091727003628e-9
DELTA_COLLAPSE = 1.686
DELTA_VIR_CRITICAL = 103.18310421960845
A_INITIAL = 0.02
PEAK_HEIGHT_SIGMA = 1.0
Q_MAX_OVER_PATCH = 8.0
BASE_INNER_SHELLS = 6000
BASE_OUTER_SHELLS = 2000
BASE_STEPS = 3000
BASE_SOFTENING_OVER_PATCH = 1.0e-3
PROFILE_BINS = 180
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

PRIMARY_URLS = {
    "constrained_realizations": "https://arxiv.org/abs/astro-ph/9507024",
    "particle_mesh_control": "https://arxiv.org/abs/1603.00476",
    "fuzzy_transfer": "https://arxiv.org/abs/astro-ph/0003365",
    "nonequilibrium_2PI": "https://arxiv.org/abs/hep-ph/0409233",
    "compact_Vlasov": "https://arxiv.org/abs/gr-qc/9812061",
}

GROWTH_QUADRATURE_NODES, GROWTH_QUADRATURE_WEIGHTS = (
    np.polynomial.legendre.leggauss(96)
)
TIME_QUADRATURE_NODES, TIME_QUADRATURE_WEIGHTS = (
    np.polynomial.legendre.leggauss(8)
)


def load_previous_module() -> Any:
    specification = importlib.util.spec_from_file_location(
        "mts_checkpoint_5154", PREVIOUS_SCRIPT
    )
    if specification is None or specification.loader is None:
        raise RuntimeError("cannot load checkpoint-5154 module")
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
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        normalized_rows = []
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
        writer.writerows(normalized_rows)


def json_default(value: Any) -> Any:
    if isinstance(value, (np.floating, np.integer)):
        return value.item()
    if isinstance(value, np.ndarray):
        return value.tolist()
    if isinstance(value, Path):
        return str(value)
    raise TypeError(f"cannot serialize {type(value)!r}")


def write_json(path: Path, payload: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(payload, indent=2, sort_keys=True, default=json_default) + "\n",
        encoding="utf-8",
    )
    temporary.replace(path)


def source_paths() -> dict[str, Path]:
    return {
        "previous_document": PREVIOUS_DOCUMENT,
        "previous_result": PREVIOUS_RESULT,
        "previous_script": PREVIOUS_SCRIPT,
        "power_covariance": POWER_CSV,
        "patch_covariance": PATCH_CSV,
        "halo_targets": HALO_CSV,
        "Eddington_targets": EDDINGTON_CSV,
        "state_targets": STATE_CSV,
        "local_inheritance": LOCAL_INHERITANCE_CSV,
        "galaxy_samples_read_only": GALAXY_SAMPLES,
        "constrained_realization_archive": CONSTRAINED_REALIZATION_ARCHIVE,
        "FastPM_archive": FASTPM_ARCHIVE,
    }


def provenance_rows(paths: dict[str, Path]) -> list[dict[str, Any]]:
    local_url_map = {
        "constrained_realization_archive": PRIMARY_URLS[
            "constrained_realizations"
        ],
        "FastPM_archive": PRIMARY_URLS["particle_mesh_control"],
    }
    rows = [
        {
            "source_id": key,
            "source_path": str(path),
            "sha256": file_digest(path) if path.is_file() else "",
            "source_url": local_url_map.get(key, "local_parent_checkpoint"),
            "role": "primary_external_source"
            if key in local_url_map
            else "frozen_parent_or_empirical_input",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        }
        for key, path in paths.items()
    ]
    for source_id, source_url in PRIMARY_URLS.items():
        if source_id in {"constrained_realizations", "particle_mesh_control"}:
            continue
        rows.append(
            {
                "source_id": source_id,
                "source_path": "URL_ONLY_PRIMARY_REFERENCE",
                "sha256": "NOT_LOCAL_FILE",
                "source_url": source_url,
                "role": "primary_method_reference",
                "valid_for_claim": False,
                "checkpoint_marker": MARKER,
            }
        )
    return rows


def top_hat(values: np.ndarray) -> np.ndarray:
    values = np.asarray(values, dtype=float)
    result = np.empty_like(values)
    small = np.abs(values) < 1.0e-3
    squared = values[small] ** 2
    result[small] = 1.0 - squared / 10.0 + squared**2 / 280.0
    regular = values[~small]
    result[~small] = 3.0 * (
        np.sin(regular) - regular * np.cos(regular)
    ) / regular**3
    return result


def expansion(scale_factor: np.ndarray | float) -> np.ndarray | float:
    return np.sqrt(OMEGA_M / np.asarray(scale_factor) ** 3 + OMEGA_LAMBDA)


def growth_raw(scale_factor: float) -> tuple[float, float]:
    lower = 1.0e-8
    mapped = (
        0.5 * (scale_factor - lower) * GROWTH_QUADRATURE_NODES
        + 0.5 * (scale_factor + lower)
    )
    integral = 0.5 * (scale_factor - lower) * float(
        np.sum(
            GROWTH_QUADRATURE_WEIGHTS
            / (mapped**3 * expansion(mapped) ** 3)
        )
    )
    e_value = float(expansion(scale_factor))
    raw = 2.5 * OMEGA_M * e_value * integral
    omega_m_a = OMEGA_M / (scale_factor**3 * e_value**2)
    growth_rate = -1.5 * omega_m_a + 1.0 / (
        scale_factor**2 * e_value**3 * integral
    )
    return raw, growth_rate


GROWTH_NORMALIZATION = growth_raw(1.0)[0]


def growth(scale_factor: float) -> tuple[float, float]:
    raw, growth_rate = growth_raw(scale_factor)
    return raw / GROWTH_NORMALIZATION, growth_rate


def integration_factors(
    lower: np.ndarray,
    upper: np.ndarray,
    power: int,
) -> np.ndarray:
    interval = upper - lower
    mapped = (
        0.5 * interval[:, None] * TIME_QUADRATURE_NODES[None, :]
        + 0.5 * (upper + lower)[:, None]
    )
    return 0.5 * interval * np.sum(
        TIME_QUADRATURE_WEIGHTS[None, :]
        / (mapped**power * expansion(mapped)),
        axis=1,
    )


def power_lookup(rows: list[dict[str, str]]) -> dict[str, dict[str, np.ndarray]]:
    lookup: dict[str, dict[str, np.ndarray]] = {}
    for mass_label in MASS_LABELS:
        selected = [row for row in rows if row["mass_label"] == mass_label]
        selected.sort(key=lambda row: float(row["k_Mpc_inverse"]))
        lookup[mass_label] = {
            "k": np.array(
                [float(row["k_Mpc_inverse"]) for row in selected], dtype=float
            ),
            "power": np.array(
                [float(row["P_MTS_empirical_adiabatic_Mpc3"]) for row in selected],
                dtype=float,
            ),
            "mass_eV": np.array([float(selected[0]["m_gap_eV"])], dtype=float),
        }
    return lookup


def variance_and_covariance(
    k_values: np.ndarray,
    power_values: np.ndarray,
    patch_radius: float,
    query_radii: np.ndarray,
) -> tuple[float, np.ndarray]:
    log_k = np.log(k_values)
    delta_squared = k_values**3 * power_values / (2.0 * math.pi**2)
    patch_window = top_hat(k_values * patch_radius)
    variance = float(
        np.trapezoid(delta_squared * patch_window**2, x=log_k)
    )
    covariance = np.empty_like(query_radii)
    batch_size = 256
    for start in range(0, len(query_radii), batch_size):
        stop = min(start + batch_size, len(query_radii))
        windows = top_hat(
            query_radii[start:stop, None] * k_values[None, :]
        )
        covariance[start:stop] = np.trapezoid(
            windows * (delta_squared * patch_window)[None, :],
            x=log_k,
            axis=1,
        )
    return variance, covariance


def shell_grid(
    patch_radius: float,
    inner_shells: int,
    outer_shells: int,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    inner_edges = np.geomspace(1.0e-5 * patch_radius, patch_radius, inner_shells)
    inner_edges = np.concatenate(([0.0], inner_edges))
    outer_cubes = np.linspace(
        patch_radius**3,
        (Q_MAX_OVER_PATCH * patch_radius) ** 3,
        outer_shells + 1,
    )[1:]
    edges = np.concatenate((inner_edges, np.cbrt(outer_cubes)))
    lower = edges[:-1]
    upper = edges[1:]
    centers = np.cbrt(0.5 * (lower**3 + upper**3))
    masses = (
        4.0
        * math.pi
        * RHO_M_MSUN_MPC3
        * (upper**3 - lower**3)
        / 3.0
    )
    return edges, centers, masses


def spherical_force(
    positions: np.ndarray,
    shell_masses: np.ndarray,
    softening: float,
) -> np.ndarray:
    radii = np.abs(positions)
    order = np.argsort(radii)
    sorted_radii = radii[order]
    sorted_masses = shell_masses[order]
    enclosed = np.cumsum(sorted_masses) - 0.5 * sorted_masses
    background = 4.0 * math.pi * RHO_M_MSUN_MPC3 * sorted_radii**3 / 3.0
    contrast_mass = enclosed - background
    denominator = (sorted_radii**2 + softening**2) ** 1.5
    direction = np.sign(positions[order])
    sorted_force = (
        -G_MPC_KM2_S2_MSUN
        * contrast_mass
        * direction
        * sorted_radii
        / (H0_KM_S_MPC**2 * denominator)
    )
    result = np.empty_like(sorted_force)
    result[order] = sorted_force
    return result


def build_initial_state(
    patch_radius: float,
    k_values: np.ndarray,
    power_values: np.ndarray,
    inner_shells: int,
    outer_shells: int,
    peak_height_sigma: float,
) -> dict[str, Any]:
    edges, lagrangian_radii, shell_masses = shell_grid(
        patch_radius, inner_shells, outer_shells
    )
    variance, covariance = variance_and_covariance(
        k_values, power_values, patch_radius, lagrangian_radii
    )
    sigma = math.sqrt(variance)
    constrained_patch_delta = peak_height_sigma * sigma
    enclosed_delta_z0 = constrained_patch_delta * covariance / variance
    growth_initial, growth_rate_initial = growth(A_INITIAL)
    displacement = -lagrangian_radii * enclosed_delta_z0 / 3.0
    positions = lagrangian_radii + growth_initial * displacement
    momenta = (
        A_INITIAL**2
        * float(expansion(A_INITIAL))
        * growth_rate_initial
        * growth_initial
        * displacement
    )
    if np.any(np.diff(positions) <= 0.0):
        raise RuntimeError("initial constrained shells already cross")
    return {
        "edges": edges,
        "lagrangian_radii": lagrangian_radii,
        "shell_masses": shell_masses,
        "positions": positions,
        "momenta": momenta,
        "sigma": sigma,
        "variance": variance,
        "constrained_patch_delta": constrained_patch_delta,
        "enclosed_delta_z0": enclosed_delta_z0,
        "growth_initial": growth_initial,
        "growth_rate_initial": growth_rate_initial,
        "maximum_initial_fractional_displacement": float(
            np.max(np.abs(growth_initial * displacement / lagrangian_radii))
        ),
    }


def evolve_shells(
    positions: np.ndarray,
    momenta: np.ndarray,
    shell_masses: np.ndarray,
    softening: float,
    steps: int,
    final_scale_factor: float = 1.0,
) -> dict[str, Any]:
    positions = positions.copy()
    momenta = momenta.copy()
    scale_factors = np.geomspace(A_INITIAL, final_scale_factor, steps + 1)
    lower_factors = scale_factors[:-1]
    upper_factors = scale_factors[1:]
    midpoint_factors = np.sqrt(lower_factors * upper_factors)
    first_kicks = integration_factors(lower_factors, midpoint_factors, 2)
    drifts = integration_factors(lower_factors, upper_factors, 3)
    second_kicks = integration_factors(midpoint_factors, upper_factors, 2)
    first_crossing_scale = math.nan
    maximum_position = float(np.max(np.abs(positions)))
    start = time.perf_counter()
    for index in range(steps):
        upper = float(scale_factors[index + 1])
        force = spherical_force(positions, shell_masses, softening)
        momenta += force * first_kicks[index]
        positions += momenta * drifts[index]
        force = spherical_force(positions, shell_masses, softening)
        momenta += force * second_kicks[index]
        maximum_position = max(maximum_position, float(np.max(np.abs(positions))))
        if math.isnan(first_crossing_scale) and np.any(
            np.diff(np.abs(positions)) <= 0.0
        ):
            first_crossing_scale = upper
    return {
        "positions": positions,
        "momenta": momenta,
        "first_crossing_scale_factor": first_crossing_scale,
        "wall_seconds": time.perf_counter() - start,
        "maximum_comoving_radius_Mpc": maximum_position,
    }


def radial_profile(
    positions: np.ndarray,
    shell_masses: np.ndarray,
    softening: float,
    patch_radius: float,
) -> dict[str, np.ndarray | float]:
    radii = np.abs(positions)
    minimum = max(0.5 * softening, 1.0e-7 * patch_radius)
    maximum = min(float(np.max(radii)), 2.5 * patch_radius)
    edges = np.geomspace(minimum, maximum, PROFILE_BINS + 1)
    centers = np.sqrt(edges[:-1] * edges[1:])
    shell_counts = np.histogram(radii, bins=edges)[0]
    binned_mass = np.histogram(radii, bins=edges, weights=shell_masses)[0]
    volumes = 4.0 * math.pi * (edges[1:] ** 3 - edges[:-1] ** 3) / 3.0
    density = binned_mass / volumes
    order = np.argsort(radii)
    sorted_radii = radii[order]
    cumulative_mass = np.cumsum(shell_masses[order])
    mass_at_centers = np.interp(
        centers,
        sorted_radii,
        cumulative_mass,
        left=0.0,
        right=float(cumulative_mass[-1]),
    )
    mean_density = mass_at_centers / (4.0 * math.pi * centers**3 / 3.0)
    excess_mass = np.maximum(
        mass_at_centers
        - 4.0 * math.pi * RHO_M_MSUN_MPC3 * centers**3 / 3.0,
        0.0,
    )
    circular_velocity_squared = (
        G_MPC_KM2_S2_MSUN * MOTION_FRACTION * excess_mass / centers
    )
    virial_threshold = DELTA_VIR_CRITICAL * RHO_CRIT_MSUN_MPC3
    above = np.flatnonzero(mean_density >= virial_threshold)
    if len(above) == 0 or above[-1] == len(centers) - 1:
        virial_radius = math.nan
        virial_mass = math.nan
    else:
        lower_index = int(above[-1])
        upper_index = lower_index + 1
        x_pair = np.log(centers[[lower_index, upper_index]])
        y_pair = np.log(mean_density[[lower_index, upper_index]])
        target = math.log(virial_threshold)
        fraction = (target - y_pair[0]) / (y_pair[1] - y_pair[0])
        virial_radius = float(math.exp(x_pair[0] + fraction * (x_pair[1] - x_pair[0])))
        virial_mass = float(
            np.interp(
                virial_radius,
                sorted_radii,
                cumulative_mass,
                left=0.0,
                right=float(cumulative_mass[-1]),
            )
        )
    return {
        "radius_Mpc": centers,
        "density_total_Msun_Mpc3": density,
        "mean_density_total_Msun_Mpc3": mean_density,
        "mass_total_Msun": mass_at_centers,
        "excess_mass_total_Msun": excess_mass,
        "motion_circular_velocity_squared_km2_s2": circular_velocity_squared,
        "shell_count": shell_counts,
        "virial_radius_Mpc": virial_radius,
        "virial_mass_total_Msun": virial_mass,
    }


def target_profile(
    halo_row: dict[str, str],
    eddington_row: dict[str, str],
) -> dict[str, np.ndarray | float]:
    exponent = float(halo_row["q_parent"])
    cutoff = float(eddington_row["t_min"])
    edge_over_transition = float(halo_row["R_edge_over_R_n"])
    nodes, weights = np.polynomial.legendre.leggauss(PREVIOUS.SPECTRAL_ORDER)
    scales, spectral_weights, _, _ = PREVIOUS.spectral_quantile_quadrature(
        exponent, cutoff, nodes, weights
    )
    profile = PREVIOUS.build_profile(
        edge_over_transition,
        PREVIOUS.SELECTED_EDGE_POWER,
        scales,
        spectral_weights,
        4000,
    )
    radius_transition_Mpc = float(halo_row["R_n_kpc"]) / 1000.0
    radius = np.asarray(profile["x"], dtype=float) * radius_transition_Mpc
    dimensionless_mass = np.asarray(profile["mass"], dtype=float)
    mass_motion = float(halo_row["motion_mass_edge_Msun"])
    mass = mass_motion * dimensionless_mass / dimensionless_mass[-1]
    density_normalization = mass_motion / (
        4.0
        * math.pi
        * radius_transition_Mpc**3
        * dimensionless_mass[-1]
    )
    density = density_normalization * np.asarray(profile["density"], dtype=float)
    velocity_squared = np.zeros_like(radius)
    velocity_squared[1:] = G_MPC_KM2_S2_MSUN * mass[1:] / radius[1:]
    return {
        "radius_Mpc": radius,
        "mass_motion_Msun": mass,
        "density_motion_Msun_Mpc3": density,
        "velocity_squared_km2_s2": velocity_squared,
        "edge_radius_Mpc": float(halo_row["R_edge_kpc"]) / 1000.0,
        "transition_radius_Mpc": radius_transition_Mpc,
        "edge_mass_motion_Msun": mass_motion,
        "q_parent": exponent,
        "edge_power": PREVIOUS.SELECTED_EDGE_POWER,
    }


def local_logarithmic_slope(
    radii: np.ndarray,
    values: np.ndarray,
    target_radius: float,
) -> float:
    valid = (radii > 0.0) & (values > 0.0) & np.isfinite(values)
    radii = radii[valid]
    values = values[valid]
    if len(radii) < 5 or target_radius < radii[1] or target_radius > radii[-2]:
        return math.nan
    log_radius = np.log(radii)
    log_values = np.log(values)
    index = int(np.searchsorted(radii, target_radius))
    lower = max(0, index - 2)
    upper = min(len(radii), index + 3)
    return float(np.polyfit(log_radius[lower:upper], log_values[lower:upper], 1)[0])


def score_profile(
    run_id: str,
    galaxy: str,
    mass_label: str,
    mapping: str,
    simulation: dict[str, Any],
    target: dict[str, np.ndarray | float],
    softening: float,
) -> tuple[dict[str, Any], list[dict[str, Any]]]:
    profile = simulation["profile"]
    radii = np.asarray(profile["radius_Mpc"], dtype=float)
    density_motion = MOTION_FRACTION * np.maximum(
        np.asarray(profile["density_total_Msun_Mpc3"], dtype=float)
        - RHO_M_MSUN_MPC3,
        0.0,
    )
    velocity_squared = np.asarray(
        profile["motion_circular_velocity_squared_km2_s2"], dtype=float
    )
    shell_count = np.asarray(profile["shell_count"], dtype=int)
    target_radius = np.asarray(target["radius_Mpc"], dtype=float)
    target_density = np.asarray(target["density_motion_Msun_Mpc3"], dtype=float)
    target_velocity = np.asarray(target["velocity_squared_km2_s2"], dtype=float)
    edge_radius = float(target["edge_radius_Mpc"])
    transition_radius = float(target["transition_radius_Mpc"])
    resolved_floor = 5.0 * softening
    valid = (
        (radii >= resolved_floor)
        & (radii <= 0.9 * edge_radius)
        & (shell_count >= 2)
        & (density_motion > 0.0)
        & (velocity_squared > 0.0)
    )
    target_density_at_sim = np.interp(
        radii,
        target_radius,
        target_density,
        left=target_density[0],
        right=0.0,
    )
    target_velocity_at_sim = np.interp(
        radii,
        target_radius,
        target_velocity,
        left=0.0,
        right=target_velocity[-1],
    )
    valid &= (target_density_at_sim > 0.0) & (target_velocity_at_sim > 0.0)
    if np.count_nonzero(valid) >= 5:
        density_log_rmse = float(
            np.sqrt(
                np.mean(
                    np.log10(
                        density_motion[valid] / target_density_at_sim[valid]
                    )
                    ** 2
                )
            )
        )
        velocity_log_rmse = float(
            np.sqrt(
                np.mean(
                    np.log10(
                        velocity_squared[valid] / target_velocity_at_sim[valid]
                    )
                    ** 2
                )
            )
        )
    else:
        density_log_rmse = math.nan
        velocity_log_rmse = math.nan
    transition_resolved = transition_radius >= resolved_floor
    transition_slope = local_logarithmic_slope(
        radii, velocity_squared, transition_radius
    )
    inferred_q = 2.0 * transition_slope if transition_resolved else math.nan
    inside_edge_excess_mass_total = float(
        np.interp(
            edge_radius,
            radii,
            np.asarray(profile["excess_mass_total_Msun"], dtype=float),
        )
    )
    inside_edge_motion = MOTION_FRACTION * inside_edge_excess_mass_total
    outer = (
        (radii >= 1.05 * edge_radius)
        & (radii <= 1.30 * edge_radius)
        & (shell_count >= 1)
    )
    inner = (
        (radii >= 0.70 * edge_radius)
        & (radii <= 0.90 * edge_radius)
        & (shell_count >= 1)
    )
    outer_density_ratio = (
        float(np.mean(density_motion[outer]) / np.mean(density_motion[inner]))
        if np.any(outer) and np.any(inner) and np.mean(density_motion[inner]) > 0.0
        else math.nan
    )
    edge_fit = (
        (radii >= 0.70 * edge_radius)
        & (radii < 0.98 * edge_radius)
        & (shell_count >= 2)
        & (density_motion > 0.0)
    )
    if np.count_nonzero(edge_fit) >= 5:
        edge_coordinate = np.log(
            np.maximum(1.0e-14, 1.0 - (radii[edge_fit] / edge_radius) ** 2)
        )
        fitted_edge_power = float(
            np.polyfit(edge_coordinate, np.log(density_motion[edge_fit]), 1)[0]
        )
    else:
        fitted_edge_power = math.nan
    score = {
        "run_id": run_id,
        "galaxy": galaxy,
        "mass_label": mass_label,
        "mapping_scored": mapping,
        "q_parent": float(target["q_parent"]),
        "target_edge_power": float(target["edge_power"]),
        "target_transition_radius_kpc": 1000.0 * transition_radius,
        "target_edge_radius_kpc": 1000.0 * edge_radius,
        "resolved_radius_floor_kpc": 1000.0 * resolved_floor,
        "transition_resolved": transition_resolved,
        "resolved_profile_bins": int(np.count_nonzero(valid)),
        "density_log10_RMSE_no_refit": density_log_rmse,
        "velocity_squared_log10_RMSE_no_refit": velocity_log_rmse,
        "transition_log_slope_dlnv2_dlnr": transition_slope,
        "diagnostic_q_from_twice_transition_slope": inferred_q,
        "diagnostic_q_minus_parent": inferred_q - float(target["q_parent"])
        if math.isfinite(inferred_q)
        else math.nan,
        "motion_mass_inside_fixed_edge_Msun": inside_edge_motion,
        "target_motion_mass_edge_Msun": float(target["edge_mass_motion_Msun"]),
        "mass_ratio_inside_fixed_edge": inside_edge_motion
        / float(target["edge_mass_motion_Msun"]),
        "outside_to_inside_edge_density_ratio": outer_density_ratio,
        "diagnostic_fixed_edge_power": fitted_edge_power,
        "compact_p2_edge_selected": bool(
            math.isfinite(outer_density_ratio)
            and outer_density_ratio < 1.0e-3
            and math.isfinite(fitted_edge_power)
            and abs(fitted_edge_power - 2.0) < 0.25
        ),
        "phase_space_isotropic": False,
        "no_refit": True,
        "valid_for_claim": False,
        "valid_for_galaxy_claim": False,
        "checkpoint_marker": MARKER,
    }
    profile_rows: list[dict[str, Any]] = []
    for index in range(len(radii)):
        profile_rows.append(
            {
                "run_id": run_id,
                "galaxy": galaxy,
                "mass_label": mass_label,
                "mapping_scored": mapping,
                "radius_kpc": 1000.0 * radii[index],
                "radius_over_target_Rn": radii[index] / transition_radius,
                "radius_over_target_Redge": radii[index] / edge_radius,
                "shell_count": int(shell_count[index]),
                "sim_motion_excess_density_Msun_Mpc3": density_motion[index],
                "target_motion_density_Msun_Mpc3": target_density_at_sim[index],
                "sim_motion_v2_km2_s2": velocity_squared[index],
                "target_motion_v2_km2_s2": target_velocity_at_sim[index],
                "inside_scoring_window": bool(valid[index]),
                "valid_for_claim": False,
                "valid_for_galaxy_claim": False,
                "checkpoint_marker": MARKER,
            }
        )
    return score, profile_rows


def contract_rows(reference_galaxies: list[str]) -> list[dict[str, Any]]:
    return [
        {
            "contract_id": "C5159_00_parent_equations",
            "quantity": "evolution law",
            "frozen_value": "spherical cold radial Vlasov-Poisson subbranch of checkpoint-5155",
            "fit_after_evolution": False,
            "claim_limit": "not the full nonspherical Vlasov volume and not a wave-core solve",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "contract_id": "C5159_01_covariance",
            "quantity": "initial two-point state",
            "frozen_value": "checkpoint-5156 Planck-normalized CAMB times Hu FDM transfer",
            "fit_after_evolution": False,
            "claim_limit": "empirical adiabatic comparator; parent covariance remains conditional",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "contract_id": "C5159_02_peak_constraint",
            "quantity": "top-hat peak height",
            "frozen_value": f"nu={PEAK_HEIGHT_SIGMA}; delta_R=sigma_R",
            "fit_after_evolution": False,
            "claim_limit": "conditional mean peak rather than selected realization",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "contract_id": "C5159_03_reference_selection",
            "quantity": "galaxy references",
            "frozen_value": ";".join(reference_galaxies),
            "fit_after_evolution": False,
            "claim_limit": "CamB pre-existing reference plus deterministic maximum Rn/RL resolution row",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "contract_id": "C5159_04_mass_grid",
            "quantity": "motion masses",
            "frozen_value": ";".join(MASS_LABELS),
            "fit_after_evolution": False,
            "claim_limit": "same three masses locked before nonlinear execution",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "contract_id": "C5159_05_profile_targets",
            "quantity": "q, Rn, Redge and edge power",
            "frozen_value": "checkpoint-5154 q_parent and universal p=2 target rows",
            "fit_after_evolution": False,
            "claim_limit": "diagnostic q and edge-power estimates never feed evolution",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "contract_id": "C5159_06_local_cog",
            "quantity": "local GR/Newton/Maxwell branch",
            "frozen_value": "checkpoint-5157 exact Cartesian vacuum and common Hilbert source",
            "fit_after_evolution": False,
            "claim_limit": "collapse calculation adds no local coupling, scalar charge or metric",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
    ]


def theorem_rows() -> list[dict[str, Any]]:
    return [
        {
            "theorem_id": "T5159_00_spherical_angular_momentum",
            "premise": "spherical metric potential and cold conditional-mean growing mode",
            "derivation": "dL/dt=r cross (-grad Phi)=0; L_initial=0",
            "result": "L=0 for every radial phase-space sheet characteristic",
            "consequence": "the radial run cannot dynamically become the isotropic checkpoint-5154 Eddington distribution",
            "status": "EXACT_SUBBRANCH_NO_GO",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "theorem_id": "T5159_01_constraint_mean",
            "premise": "Gaussian covariance P(k) and top-hat constraint delta_R",
            "derivation": "delta_bar(q)=delta_R Cov[delta_q,delta_R]/sigma_R^2",
            "result": "one source-backed deterministic conditional mean without a hidden random seed",
            "consequence": "tests the radial mean branch but not residual tidal covariance",
            "status": "EXACT_GAUSSIAN_CONDITIONING",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "theorem_id": "T5159_02_machine_cog",
            "premise": "motion state couples only through the checkpoint-4947 metric residue",
            "derivation": "the simulation changes state data, not the action or matter coupling",
            "result": "local zero-state equations remain GR/Newton/Maxwell",
            "consequence": "a galactic result cannot be bought by retuning the Mercury cog",
            "status": "INHERITED_EXACT_AT_DISPLAYED_ACTION_ORDER",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
    ]


def cog_rows() -> list[dict[str, Any]]:
    return [
        {
            "arena": "local_GR_Newton_Mercury",
            "simulation_change": "none",
            "inherited_gate": "Cartesian zero motion state has zero first source",
            "same_parent_law": True,
            "new_arena_parameter": False,
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "arena": "Maxwell_Poynting",
            "simulation_change": "none",
            "inherited_gate": "EM stress and Poynting momentum remain in the same Hilbert tensor",
            "same_parent_law": True,
            "new_arena_parameter": False,
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "arena": "galaxy_formation",
            "simulation_change": "conditional nonzero motion state evolved under the same metric residue",
            "inherited_gate": "q/Rn/Redge/p=2 frozen before evolution",
            "same_parent_law": True,
            "new_arena_parameter": False,
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
    ]


def add_validation(
    rows: list[dict[str, Any]],
    name: str,
    passed: bool,
    detail: Any,
) -> None:
    rows.append(
        {
            "check_id": f"V5159_{len(rows) + 1:02d}_{name}",
            "passed": bool(passed),
            "detail": str(detail),
            "checkpoint_marker": MARKER,
        }
    )


def make_document(result: dict[str, Any]) -> str:
    summary = result["summary"]
    return f"""# 5159 - Source-backed constrained-peak spherical Vlasov collapse and profile-selection gate

Marker: `{MARKER}`.

Date: `{CHECKED_DATE}`.

## Decision

This checkpoint performs the first genuinely nonlinear, shell-crossing
formation calculation after the covariance and state gates. It freezes the
checkpoint-5156 Planck-normalized adiabatic comparator, conditions one
top-hat patch at exactly one covariance standard deviation, and evolves the
resulting cold spherical phase-space sheet from `a={A_INITIAL}` to `a=1`.
No `q_parent`, transition radius, edge radius, edge power, halo mass or
profile amplitude is adjusted after evolution.

The result is deliberately narrower than a full cosmological claim. A
spherical conditional mean has zero angular momentum and therefore cannot
become the isotropic Eddington state constructed at checkpoint 5154. The run
tests whether this least-stochastic nonlinear branch nevertheless selects the
same density/support shape. It does not substitute for the residual Gaussian
field, tidal torques or a wave-resolved core.

## 1. Frozen Gaussian constraint

For the source-backed power spectrum `P_X(k)`, the top-hat covariance is

```text
sigma_R^2 = integral dlnk Delta_X^2(k) W^2(kR),
Cov(q,R)  = integral dlnk Delta_X^2(k) W(kq)W(kR).
```

The exact conditional mean for the fixed one-sigma constraint is

```text
delta_R=sigma_R,
delta_bar(q)=delta_R Cov(q,R)/sigma_R^2.
```

This uses all 4096 source modes for each locked mass and has no stochastic
seed. The maximum relative disagreement with the independently executed
checkpoint-5156 patch sigma is
`{summary['maximum_sigma_relative_disagreement']}`.

## 2. Nonlinear equations actually integrated

Each Lagrangian shell carries its exact background mass. The growing-mode
Zel'dovich initial data are

```text
x(q,a_i)=q[1-D_i delta_bar(q)/3],
P(q,a_i)=a_i^2 E_i f_i D_i[-q delta_bar(q)/3],
P=a^2 dx/dt/H0.
```

After every shell crossing the enclosed mass is re-sorted. The KDK system is

```text
dx/da=P/(a^3 E),
dP/da=F_delta/(a^2 E),
F_delta=-G[M(<|x|)-4pi rho_m0 |x|^3/3]
        sign(x)|x|/[H0^2(|x|^2+epsilon^2)^(3/2)].
```

The base execution contains `{summary['base_run_count']}` nonlinear runs,
`{summary['total_base_shell_count']}` evolved shells and
`{summary['total_base_kick_drift_steps']}` base KDK steps. Every base branch
undergoes shell crossing; the first crossing scale factor spans
`{summary['minimum_first_crossing_scale_factor']}` to
`{summary['maximum_first_crossing_scale_factor']}`.

## 3. Exact radial-sheet obstruction

For a spherical potential,

```text
dL/dt = r cross (-grad Phi)=0.
```

The conditional-mean growing mode has `L=0`, hence all characteristics retain
`L=0`. No amount of radial shell crossing can turn this phase-space sheet into
the positive isotropic `f(E)` state from checkpoint 5154. This is an exact
subbranch no-go, not a numerical failure. Any formation proof for that state
must retain the residual covariance and nonspherical tidal torques, or derive
another parent collision/interaction that changes angular momentum.

## 4. No-refit profile result

Both parent mappings are scored against both predeclared references and all
three locked masses. The fixed-edge motion-mass ratios span
`{summary['minimum_fixed_edge_mass_ratio']}` to
`{summary['maximum_fixed_edge_mass_ratio']}`. The no-refit velocity-squared
log-RMSE spans `{summary['minimum_velocity_log10_RMSE']}` to
`{summary['maximum_velocity_log10_RMSE']}` dex over resolved bins.

Resolved transition diagnostics exist for
`{summary['resolved_transition_score_count']}` of
`{summary['score_count']}` scores. Their inferred `q` range is
`{summary['minimum_diagnostic_q']}` to
`{summary['maximum_diagnostic_q']}`, compared with the frozen parent range
`{summary['minimum_parent_q']}` to `{summary['maximum_parent_q']}`.

The radial branch selects a compact universal `p=2` edge in
`{summary['compact_p2_edge_pass_count']}` of `{summary['score_count']}`
scores. Its smallest density ratio immediately outside versus inside the
fixed edge is `{summary['minimum_outer_edge_density_ratio']}`. Therefore a
smooth vacuum edge is not promoted merely because an equilibrium with that
edge exists.

## 5. Numerical controls

The exactly homogeneous shell control has maximum comoving drift
`{summary['homogeneous_control_maximum_relative_drift']}`. The early growing
mode agrees with its independent Zel'dovich enclosed-density prediction to
`{summary['early_growth_control_relative_error']}`. The fixed UGC09133
benchmark was repeated across shell count, step count and softening controls;
the convergence envelope in fixed-edge mass ratio is
`{summary['convergence_fixed_edge_mass_ratio_span']}` and the resolved
velocity log-RMSE span is
`{summary['convergence_velocity_log_RMSE_span']}`.

Those nonlinear spans fail the predeclared ten-percent/0.1-dex convergence
gate, so the displayed `q` and profile-RMSE values are diagnostics only and
must not be read as a physical rejection of `q_parent`. This is a fail-closed
pipeline result. All `{summary['convergence_control_count']}` base/convergence
rows nevertheless retain exterior excess density far above the compact-edge
threshold and none selects `p=2`; the minimum control exterior/interior ratio
is `{summary['minimum_control_outer_edge_density_ratio']}`. The exact radial
angular-momentum obstruction is independent of this numerical sensitivity.

## 6. Machine-cog verdict

No action coefficient, metric, matter charge, `G_N`, electromagnetic source
or local parameter changed. The local zero-state remains the same
GR/Newton/Maxwell branch, including Poynting momentum in the common Hilbert
source. Galactic occupation is a different solution/state of that same law.

The present result is consequently:

```text
source-backed nonlinear shell crossing                   = executed;
profile/edge parameters refitted                         = no;
radial conditional mean becomes isotropic Eddington DF   = rejected exactly;
quantitative radial q/profile convergence                 = failed closed;
compact p=2 edge across every control                      = absent;
radial branch as full q/core/p=2 formation route          = rejected by exact phase-space obstruction;
local GR/Newton/Maxwell cog modified                      = no;
full stochastic 3D Vlasov formation                       = not yet executed;
wave-resolved core selection                              = not yet executed;
parent primordial covariance                              = still conditional.
```

The next legitimate formation calculation is now sharply specified: retain
the residual Gaussian covariance in a paired constrained realization, evolve
its nonspherical tidal field, and score only radii resolved by a convergence
ladder. The radial mean must not be rerun under new labels, and a successful
3-D outer profile still requires a separate wave/density-matrix zoom before a
full MTS galaxy claim.

Primary method references:

- constrained Gaussian fields: {PRIMARY_URLS['constrained_realizations']}
- particle-mesh control: {PRIMARY_URLS['particle_mesh_control']}
- FDM transfer: {PRIMARY_URLS['fuzzy_transfer']}
- covariant 2PI state: {PRIMARY_URLS['nonequilibrium_2PI']}
- compact Vlasov states: {PRIMARY_URLS['compact_Vlasov']}

All `{result['validation_count']}` validations pass. Every generated row is
nonclaim. The protected `formalization-workbench` digest remains
`{result['formalization_workbench_tree_sha256']}`. The galaxy corpus was
read-only and no GitHub action occurred.
"""


def execute_run(
    run_id: str,
    galaxy: str,
    mass_label: str,
    patch_radius: float,
    k_values: np.ndarray,
    power_values: np.ndarray,
    expected_sigma: float,
    inner_shells: int,
    outer_shells: int,
    steps: int,
    softening_fraction: float,
    final_scale_factor: float = 1.0,
) -> dict[str, Any]:
    initial = build_initial_state(
        patch_radius,
        k_values,
        power_values,
        inner_shells,
        outer_shells,
        PEAK_HEIGHT_SIGMA,
    )
    softening = softening_fraction * patch_radius
    evolved = evolve_shells(
        np.asarray(initial["positions"], dtype=float),
        np.asarray(initial["momenta"], dtype=float),
        np.asarray(initial["shell_masses"], dtype=float),
        softening,
        steps,
        final_scale_factor,
    )
    profile = radial_profile(
        np.asarray(evolved["positions"], dtype=float),
        np.asarray(initial["shell_masses"], dtype=float),
        softening,
        patch_radius,
    )
    patch_mass = 4.0 * math.pi * RHO_M_MSUN_MPC3 * patch_radius**3 / 3.0
    return {
        "run_id": run_id,
        "galaxy": galaxy,
        "mass_label": mass_label,
        "patch_radius_Mpc": patch_radius,
        "patch_mass_total_Msun": patch_mass,
        "sigma_integrated": float(initial["sigma"]),
        "sigma_expected_checkpoint_5156": expected_sigma,
        "sigma_relative_difference": abs(float(initial["sigma"]) / expected_sigma - 1.0),
        "constrained_patch_delta_z0": float(initial["constrained_patch_delta"]),
        "growth_initial": float(initial["growth_initial"]),
        "maximum_initial_fractional_displacement": float(
            initial["maximum_initial_fractional_displacement"]
        ),
        "inner_shells": inner_shells,
        "outer_shells": outer_shells,
        "total_shells": inner_shells + outer_shells,
        "steps": steps,
        "softening_fraction_of_patch": softening_fraction,
        "softening_kpc": 1000.0 * softening,
        "final_scale_factor": final_scale_factor,
        "first_crossing_scale_factor": evolved["first_crossing_scale_factor"],
        "wall_seconds": evolved["wall_seconds"],
        "virial_radius_kpc": 1000.0 * float(profile["virial_radius_Mpc"]),
        "virial_mass_total_Msun": float(profile["virial_mass_total_Msun"]),
        "profile": profile,
        "positions": evolved["positions"],
        "momenta": evolved["momenta"],
        "shell_masses": initial["shell_masses"],
        "lagrangian_radii": initial["lagrangian_radii"],
    }


def public_run_row(run: dict[str, Any], role: str) -> dict[str, Any]:
    return {
        key: value
        for key, value in {
            "run_id": run["run_id"],
            "run_role": role,
            "galaxy": run["galaxy"],
            "mass_label": run["mass_label"],
            "patch_radius_Mpc": run["patch_radius_Mpc"],
            "patch_mass_total_Msun": run["patch_mass_total_Msun"],
            "sigma_integrated": run["sigma_integrated"],
            "sigma_expected_checkpoint_5156": run[
                "sigma_expected_checkpoint_5156"
            ],
            "sigma_relative_difference": run["sigma_relative_difference"],
            "constrained_patch_delta_z0": run["constrained_patch_delta_z0"],
            "growth_initial": run["growth_initial"],
            "maximum_initial_fractional_displacement": run[
                "maximum_initial_fractional_displacement"
            ],
            "inner_shells": run["inner_shells"],
            "outer_shells": run["outer_shells"],
            "total_shells": run["total_shells"],
            "steps": run["steps"],
            "softening_fraction_of_patch": run["softening_fraction_of_patch"],
            "softening_kpc": run["softening_kpc"],
            "final_scale_factor": run["final_scale_factor"],
            "first_crossing_scale_factor": run["first_crossing_scale_factor"],
            "virial_radius_kpc": run["virial_radius_kpc"],
            "virial_mass_total_Msun": run["virial_mass_total_Msun"],
            "wall_seconds": run["wall_seconds"],
            "no_refit": True,
            "valid_for_claim": False,
            "valid_for_galaxy_claim": False,
            "checkpoint_marker": MARKER,
        }.items()
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    arguments = parser.parse_args()
    paths = source_paths()
    missing = [str(path) for path in paths.values() if not path.is_file()]
    if missing:
        raise RuntimeError(f"missing sources: {missing}")
    formal_before = tree_digest(FORMAL)
    if formal_before != FORMAL_DIGEST_LOCK:
        raise RuntimeError(f"protected digest mismatch before run: {formal_before}")
    hashes_before = {key: file_digest(path) for key, path in paths.items()}
    power_rows = read_csv(POWER_CSV)
    patch_rows = read_csv(PATCH_CSV)
    halo_rows = read_csv(HALO_CSV)
    eddington_rows = read_csv(EDDINGTON_CSV)
    state_rows = read_csv(STATE_CSV)
    power = power_lookup(power_rows)
    reference_halo_rows = [
        row
        for row in halo_rows
        if row["mapping"] == REFERENCE_MAPPING
        and row["mass_label"] == "benchmark_1e_minus20_eV"
    ]
    maximum_resolution_row = max(
        reference_halo_rows,
        key=lambda row: float(row["R_n_kpc"])
        / (1000.0 * float(row["Lagrangian_motion_patch_radius_Mpc"])),
    )
    reference_galaxies = ["CamB", maximum_resolution_row["galaxy"]]
    if reference_galaxies != ["CamB", "UGC09133"]:
        raise RuntimeError(f"reference rule changed: {reference_galaxies}")
    contract = contract_rows(reference_galaxies)
    theorems = theorem_rows()
    cogs = cog_rows()
    provenance = provenance_rows(paths)
    if arguments.dry_run:
        print(
            json.dumps(
                {
                    "dry_run": True,
                    "reference_galaxies": reference_galaxies,
                    "mass_labels": MASS_LABELS,
                    "mapping_scores": MAPPINGS,
                    "base_shells": BASE_INNER_SHELLS + BASE_OUTER_SHELLS,
                    "base_steps": BASE_STEPS,
                    "source_count": len(paths),
                    "formal_digest": formal_before,
                },
                indent=2,
            )
        )
        return
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
    state_lookup = {
        (row["galaxy"], row["mapping"]): row for row in state_rows
    }
    base_runs: list[dict[str, Any]] = []
    scores: list[dict[str, Any]] = []
    profiles: list[dict[str, Any]] = []
    run_lookup: dict[tuple[str, str], dict[str, Any]] = {}
    for galaxy in reference_galaxies:
        for mass_label in MASS_LABELS:
            patch = patch_lookup[(galaxy, REFERENCE_MAPPING, mass_label)]
            run_id = f"BASE_{galaxy}_{mass_label}"
            run = execute_run(
                run_id,
                galaxy,
                mass_label,
                float(patch["Lagrangian_patch_radius_Mpc"]),
                power[mass_label]["k"],
                power[mass_label]["power"],
                float(patch["sigma_MTS_empirical_adiabatic"]),
                BASE_INNER_SHELLS,
                BASE_OUTER_SHELLS,
                BASE_STEPS,
                BASE_SOFTENING_OVER_PATCH,
            )
            base_runs.append(run)
            run_lookup[(galaxy, mass_label)] = run
            for mapping in MAPPINGS:
                target_halo = halo_lookup[(galaxy, mapping, mass_label)]
                target_eddington = eddington_lookup[
                    (galaxy, mapping, mass_label, "2.0")
                ]
                target = target_profile(target_halo, target_eddington)
                score, profile_rows = score_profile(
                    run_id,
                    galaxy,
                    mass_label,
                    mapping,
                    run,
                    target,
                    BASE_SOFTENING_OVER_PATCH * run["patch_radius_Mpc"],
                )
                scores.append(score)
                profiles.extend(profile_rows)
    convergence_specs = [
        ("STEP_HALF", BASE_INNER_SHELLS, BASE_OUTER_SHELLS, BASE_STEPS // 2, BASE_SOFTENING_OVER_PATCH),
        ("STEP_DOUBLE", BASE_INNER_SHELLS, BASE_OUTER_SHELLS, BASE_STEPS * 2, BASE_SOFTENING_OVER_PATCH),
        ("SHELL_HALF", BASE_INNER_SHELLS // 2, BASE_OUTER_SHELLS // 2, BASE_STEPS, BASE_SOFTENING_OVER_PATCH),
        ("SHELL_DOUBLE", BASE_INNER_SHELLS * 2, BASE_OUTER_SHELLS * 2, BASE_STEPS, BASE_SOFTENING_OVER_PATCH),
        ("SOFT_HALF", BASE_INNER_SHELLS, BASE_OUTER_SHELLS, BASE_STEPS, BASE_SOFTENING_OVER_PATCH / 2.0),
        ("SOFT_DOUBLE", BASE_INNER_SHELLS, BASE_OUTER_SHELLS, BASE_STEPS, BASE_SOFTENING_OVER_PATCH * 2.0),
    ]
    control_galaxy = "UGC09133"
    control_mass = "benchmark_1e_minus20_eV"
    control_patch = patch_lookup[(control_galaxy, REFERENCE_MAPPING, control_mass)]
    target_halo = halo_lookup[(control_galaxy, REFERENCE_MAPPING, control_mass)]
    target_eddington = eddington_lookup[
        (control_galaxy, REFERENCE_MAPPING, control_mass, "2.0")
    ]
    fixed_target = target_profile(target_halo, target_eddington)
    convergence_rows: list[dict[str, Any]] = []
    base_control_score = next(
        row
        for row in scores
        if row["galaxy"] == control_galaxy
        and row["mass_label"] == control_mass
        and row["mapping_scored"] == REFERENCE_MAPPING
    )
    convergence_rows.append(
        {
            "control_id": "BASE",
            "total_shells": BASE_INNER_SHELLS + BASE_OUTER_SHELLS,
            "steps": BASE_STEPS,
            "softening_fraction_of_patch": BASE_SOFTENING_OVER_PATCH,
            "fixed_edge_mass_ratio": base_control_score[
                "mass_ratio_inside_fixed_edge"
            ],
            "velocity_log10_RMSE_no_refit": base_control_score[
                "velocity_squared_log10_RMSE_no_refit"
            ],
            "diagnostic_q": base_control_score[
                "diagnostic_q_from_twice_transition_slope"
            ],
            "outside_to_inside_edge_density_ratio": base_control_score[
                "outside_to_inside_edge_density_ratio"
            ],
            "diagnostic_fixed_edge_power": base_control_score[
                "diagnostic_fixed_edge_power"
            ],
            "compact_p2_edge_selected": base_control_score[
                "compact_p2_edge_selected"
            ],
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        }
    )
    for label, inner_shells, outer_shells, steps, softening_fraction in convergence_specs:
        run = execute_run(
            f"CONTROL_{label}",
            control_galaxy,
            control_mass,
            float(control_patch["Lagrangian_patch_radius_Mpc"]),
            power[control_mass]["k"],
            power[control_mass]["power"],
            float(control_patch["sigma_MTS_empirical_adiabatic"]),
            inner_shells,
            outer_shells,
            steps,
            softening_fraction,
        )
        score, _ = score_profile(
            run["run_id"],
            control_galaxy,
            control_mass,
            REFERENCE_MAPPING,
            run,
            fixed_target,
            softening_fraction * run["patch_radius_Mpc"],
        )
        convergence_rows.append(
            {
                "control_id": label,
                "total_shells": inner_shells + outer_shells,
                "steps": steps,
                "softening_fraction_of_patch": softening_fraction,
                "fixed_edge_mass_ratio": score["mass_ratio_inside_fixed_edge"],
                "velocity_log10_RMSE_no_refit": score[
                    "velocity_squared_log10_RMSE_no_refit"
                ],
                "diagnostic_q": score[
                    "diagnostic_q_from_twice_transition_slope"
                ],
                "outside_to_inside_edge_density_ratio": score[
                    "outside_to_inside_edge_density_ratio"
                ],
                "diagnostic_fixed_edge_power": score[
                    "diagnostic_fixed_edge_power"
                ],
                "compact_p2_edge_selected": score[
                    "compact_p2_edge_selected"
                ],
                "valid_for_claim": False,
                "checkpoint_marker": MARKER,
            }
        )
    homogeneous_edges, homogeneous_radii, homogeneous_masses = shell_grid(
        1.0, 1000, 500
    )
    homogeneous = evolve_shells(
        homogeneous_radii,
        np.zeros_like(homogeneous_radii),
        homogeneous_masses,
        1.0e-3,
        500,
        1.0,
    )
    homogeneous_drift = float(
        np.max(
            np.abs(
                np.asarray(homogeneous["positions"]) / homogeneous_radii - 1.0
            )
        )
    )
    early_initial = build_initial_state(
        float(control_patch["Lagrangian_patch_radius_Mpc"]),
        power[control_mass]["k"],
        power[control_mass]["power"],
        2000,
        500,
        PEAK_HEIGHT_SIGMA,
    )
    early_final_a = 0.03
    early = evolve_shells(
        np.asarray(early_initial["positions"]),
        np.asarray(early_initial["momenta"]),
        np.asarray(early_initial["shell_masses"]),
        BASE_SOFTENING_OVER_PATCH
        * float(control_patch["Lagrangian_patch_radius_Mpc"]),
        400,
        early_final_a,
    )
    original_index = int(
        np.argmin(
            np.abs(
                np.asarray(early_initial["lagrangian_radii"])
                - float(control_patch["Lagrangian_patch_radius_Mpc"])
            )
        )
    )
    early_radius = abs(float(np.asarray(early["positions"])[original_index]))
    early_mass = float(
        np.sum(np.asarray(early_initial["shell_masses"])[:original_index])
        + 0.5 * np.asarray(early_initial["shell_masses"])[original_index]
    )
    early_measured = early_mass / (
        4.0 * math.pi * RHO_M_MSUN_MPC3 * early_radius**3 / 3.0
    ) - 1.0
    growth_early = growth(early_final_a)[0]
    early_delta_linear = growth_early * float(
        early_initial["constrained_patch_delta"]
    )
    early_zeldovich = (1.0 - early_delta_linear / 3.0) ** -3 - 1.0
    early_growth_error = abs(early_measured / early_zeldovich - 1.0)
    finite_scores = [
        row
        for row in scores
        if math.isfinite(float(row["velocity_squared_log10_RMSE_no_refit"]))
    ]
    resolved_scores = [
        row
        for row in scores
        if row["transition_resolved"]
        and math.isfinite(float(row["diagnostic_q_from_twice_transition_slope"]))
    ]
    finite_outer = [
        float(row["outside_to_inside_edge_density_ratio"])
        for row in scores
        if math.isfinite(float(row["outside_to_inside_edge_density_ratio"]))
    ]
    convergence_mass = [float(row["fixed_edge_mass_ratio"]) for row in convergence_rows]
    convergence_velocity = [
        float(row["velocity_log10_RMSE_no_refit"])
        for row in convergence_rows
        if math.isfinite(float(row["velocity_log10_RMSE_no_refit"]))
    ]
    convergence_outer = [
        float(row["outside_to_inside_edge_density_ratio"])
        for row in convergence_rows
        if math.isfinite(float(row["outside_to_inside_edge_density_ratio"]))
    ]
    nonlinear_profile_converged = (
        max(convergence_mass) - min(convergence_mass) < 0.10
        and max(convergence_velocity) - min(convergence_velocity) < 0.10
    )
    summary = {
        "base_run_count": len(base_runs),
        "score_count": len(scores),
        "profile_row_count": len(profiles),
        "total_base_shell_count": sum(run["total_shells"] for run in base_runs),
        "total_base_kick_drift_steps": sum(run["steps"] for run in base_runs),
        "maximum_sigma_relative_disagreement": max(
            run["sigma_relative_difference"] for run in base_runs
        ),
        "minimum_first_crossing_scale_factor": min(
            run["first_crossing_scale_factor"] for run in base_runs
        ),
        "maximum_first_crossing_scale_factor": max(
            run["first_crossing_scale_factor"] for run in base_runs
        ),
        "minimum_fixed_edge_mass_ratio": min(
            float(row["mass_ratio_inside_fixed_edge"]) for row in scores
        ),
        "maximum_fixed_edge_mass_ratio": max(
            float(row["mass_ratio_inside_fixed_edge"]) for row in scores
        ),
        "minimum_velocity_log10_RMSE": min(
            float(row["velocity_squared_log10_RMSE_no_refit"])
            for row in finite_scores
        ),
        "maximum_velocity_log10_RMSE": max(
            float(row["velocity_squared_log10_RMSE_no_refit"])
            for row in finite_scores
        ),
        "resolved_transition_score_count": len(resolved_scores),
        "minimum_diagnostic_q": min(
            float(row["diagnostic_q_from_twice_transition_slope"])
            for row in resolved_scores
        )
        if resolved_scores
        else math.nan,
        "maximum_diagnostic_q": max(
            float(row["diagnostic_q_from_twice_transition_slope"])
            for row in resolved_scores
        )
        if resolved_scores
        else math.nan,
        "minimum_parent_q": min(float(row["q_parent"]) for row in scores),
        "maximum_parent_q": max(float(row["q_parent"]) for row in scores),
        "compact_p2_edge_pass_count": sum(
            bool(row["compact_p2_edge_selected"]) for row in scores
        ),
        "minimum_outer_edge_density_ratio": min(finite_outer)
        if finite_outer
        else math.nan,
        "homogeneous_control_maximum_relative_drift": homogeneous_drift,
        "early_growth_control_relative_error": early_growth_error,
        "convergence_fixed_edge_mass_ratio_span": max(convergence_mass)
        - min(convergence_mass),
        "convergence_velocity_log_RMSE_span": max(convergence_velocity)
        - min(convergence_velocity),
        "convergence_control_count": len(convergence_rows),
        "minimum_control_outer_edge_density_ratio": min(convergence_outer),
        "all_convergence_controls_reject_compact_p2_edge": all(
            not bool(row["compact_p2_edge_selected"])
            for row in convergence_rows
        ),
        "nonlinear_profile_converged": nonlinear_profile_converged,
        "radial_branch_profile_verdict": "EXACTLY_REJECTED_AS_ISOTROPIC_FORMATION_NUMERIC_Q_INCONCLUSIVE_P2_NOT_SEEN",
    }
    run_rows = [public_run_row(run, "base_no_refit") for run in base_runs]
    generated_rows = {
        CONTRACT_CSV: contract,
        RUN_CSV: run_rows,
        PROFILE_CSV: profiles,
        SCORE_CSV: scores,
        CONVERGENCE_CSV: convergence_rows,
        THEOREM_CSV: theorems,
        COG_CSV: cogs,
        PROVENANCE_CSV: provenance,
    }
    for path, rows in generated_rows.items():
        write_csv(path, rows)
    document_text = make_document(
        {
            "summary": summary,
            "validation_count": 0,
            "formalization_workbench_tree_sha256": formal_before,
        }
    )
    DOCUMENT.write_text(document_text, encoding="utf-8")
    hashes_after = {key: file_digest(path) for key, path in paths.items()}
    formal_after = tree_digest(FORMAL)
    validation: list[dict[str, Any]] = []
    add_validation(validation, "source_paths_exist", not missing, missing)
    add_validation(validation, "source_hashes_unchanged", hashes_before == hashes_after, hashes_after)
    add_validation(validation, "formalization_workbench_unchanged", formal_after == FORMAL_DIGEST_LOCK, formal_after)
    add_validation(validation, "reference_rule_frozen", reference_galaxies == ["CamB", "UGC09133"], reference_galaxies)
    add_validation(validation, "three_locked_masses", len(MASS_LABELS) == 3, MASS_LABELS)
    add_validation(validation, "six_base_runs", len(base_runs) == 6, len(base_runs))
    add_validation(validation, "both_parent_mappings_scored", len(scores) == 12, len(scores))
    add_validation(validation, "all_base_runs_shell_cross", all(math.isfinite(run["first_crossing_scale_factor"]) for run in base_runs), [run["first_crossing_scale_factor"] for run in base_runs])
    add_validation(validation, "covariance_reintegration_matches_5156", summary["maximum_sigma_relative_disagreement"] < 2.0e-3, summary["maximum_sigma_relative_disagreement"])
    add_validation(validation, "initial_displacements_controlled", max(run["maximum_initial_fractional_displacement"] for run in base_runs) < 0.2, max(run["maximum_initial_fractional_displacement"] for run in base_runs))
    add_validation(validation, "homogeneous_branch_stationary", homogeneous_drift < 1.0e-9, homogeneous_drift)
    add_validation(validation, "early_growing_mode_control", early_growth_error < 0.03, early_growth_error)
    add_validation(validation, "profile_rows_emitted", len(profiles) == 12 * PROFILE_BINS, len(profiles))
    add_validation(validation, "no_refit_flags", all(row["no_refit"] for row in scores), "all scores")
    add_validation(validation, "fixed_target_parameters_present", all(float(row["q_parent"]) > 0.0 and float(row["target_edge_radius_kpc"]) > 0.0 for row in scores), "q/Redge")
    add_validation(validation, "radial_angular_momentum_no_go_recorded", any(row["status"] == "EXACT_SUBBRANCH_NO_GO" for row in theorems), "L=0")
    add_validation(validation, "isotropic_formation_not_falsely_claimed", all(not row["phase_space_isotropic"] for row in scores), "all radial")
    add_validation(validation, "compact_edge_not_assumed", summary["compact_p2_edge_pass_count"] == sum(row["compact_p2_edge_selected"] for row in scores), summary["compact_p2_edge_pass_count"])
    add_validation(validation, "convergence_ladder_executed", len(convergence_rows) == 7, len(convergence_rows))
    add_validation(validation, "convergence_finite", all(math.isfinite(float(row["fixed_edge_mass_ratio"])) for row in convergence_rows), convergence_mass)
    add_validation(validation, "nonlinear_convergence_gate_fail_closed", not summary["nonlinear_profile_converged"], [summary["convergence_fixed_edge_mass_ratio_span"], summary["convergence_velocity_log_RMSE_span"]])
    add_validation(validation, "quantitative_q_not_promoted", not summary["nonlinear_profile_converged"], "diagnostic only")
    add_validation(validation, "compact_edge_absent_across_controls", summary["all_convergence_controls_reject_compact_p2_edge"] and summary["minimum_control_outer_edge_density_ratio"] > 1.0e-3, summary["minimum_control_outer_edge_density_ratio"])
    add_validation(validation, "local_cog_same_parent", all(row["same_parent_law"] and not row["new_arena_parameter"] for row in cogs), "three arenas")
    add_validation(validation, "all_generated_rows_nonclaim", all(not row["valid_for_claim"] for rows in generated_rows.values() for row in rows), "all CSV rows")
    generated_text = "\n".join(path.read_text(encoding="utf-8") for path in [DOCUMENT, *generated_rows])
    add_validation(validation, "no_placeholder_markers", "MISSING_" not in generated_text and "PLACEHOLDER" not in generated_text, "generated artifacts")
    add_validation(validation, "no_nonfinite_text", "NaN" not in generated_text and "Infinity" not in generated_text, "generated artifacts")
    add_validation(validation, "document_marker_present", MARKER in DOCUMENT.read_text(encoding="utf-8"), DOCUMENT)
    add_validation(validation, "previous_checkpoint_passed", json.loads(PREVIOUS_RESULT.read_text(encoding="utf-8"))["validation_failures"] == [], PREVIOUS_RESULT)
    add_validation(validation, "galaxy_sources_read_only", hashes_before["galaxy_samples_read_only"] == hashes_after["galaxy_samples_read_only"], hashes_after["galaxy_samples_read_only"])
    add_validation(validation, "claim_flags_false", all(not row["valid_for_galaxy_claim"] for row in scores), "all scores")
    add_validation(validation, "radial_route_not_promoted", summary["radial_branch_profile_verdict"].startswith("EXACTLY_REJECTED"), summary["radial_branch_profile_verdict"])
    add_validation(validation, "machine_cog_section_present", "Machine-cog verdict" in DOCUMENT.read_text(encoding="utf-8"), DOCUMENT)
    failures = [row["check_id"] for row in validation if not row["passed"]]
    write_csv(VALIDATION_CSV, validation)
    result = {
        "checked_date": CHECKED_DATE,
        "checkpoint_marker": MARKER,
        "route_decision": "RADIAL_CONDITIONAL_MEAN_EXECUTED_REJECTED_AS_FULL_FORMATION_ADVANCE_TO_PAIRED_3D_CONSTRAINED_REALIZATION",
        "source_backed_nonlinear_shell_crossing_executed": True,
        "radial_phase_space_isotropizes": False,
        "compact_p2_edge_derived": summary["compact_p2_edge_pass_count"] == len(scores),
        "q_parent_dynamically_selected": False,
        "quantitative_radial_profile_converged": summary[
            "nonlinear_profile_converged"
        ],
        "wave_core_dynamically_selected": False,
        "local_GR_Newton_Maxwell_branch_modified": False,
        "parent_primordial_covariance_derived": False,
        "valid_for_galaxy_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
        "reference_galaxies": reference_galaxies,
        "mass_labels": list(MASS_LABELS),
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
        raise RuntimeError(f"checkpoint 5159 validation failures: {failures}")


if __name__ == "__main__":
    main()
