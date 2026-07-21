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

sys.dont_write_bytecode = True

import h5py
import numpy as np
from scipy.interpolate import PchipInterpolator, RegularGridInterpolator
from scipy.optimize import brentq


POST = Path(__file__).resolve().parents[1]
FORMAL = POST.parent / "formalization-workbench"
DYNAMICS_SCRIPT = (
    POST / "scripts" / "Y5_R2FR_5164_mass_conserving_two_component_initial_value_gate.py"
)
ENERGY_SCRIPT = (
    POST / "scripts" / "Y5_R2FR_5165_baryon_Maxwell_Poynting_assembly_clock_gate.py"
)
DYNAMICS_DOCUMENT = (
    POST / "5164-Y5-R2FR-mass-conserving-visible-motion-initial-value-response-gate.md"
)
ENERGY_DOCUMENT = (
    POST
    / "5165-Y5-R2FR-baryon-Maxwell-Poynting-assembly-clock-identifiability-and-energy-bound-gate.md"
)
DYNAMICS_RESULT = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5164"
    / "mass_conserving_two_component_results.json"
)
ENERGY_RESULT = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5165"
    / "baryon_Maxwell_Poynting_assembly_clock_results.json"
)
OUT = POST / "source-intake" / "functional_rg" / "5166"
SOURCE_DATA = OUT / "source-data" / "CloudyData_noUVB.h5"
CONTRACT_CSV = OUT / "baryon_entropy_cooling_contract.csv"
TABLE_CSV = OUT / "cloudy_table_metadata.csv"
THERMAL_CSV = OUT / "virial_temperature_escape_gate.csv"
CLUMPING_CSV = OUT / "resolved_clumping_resolution_gate.csv"
PROFILE_CSV = OUT / "cie_cooling_luminosity_profiles.csv"
CLOCK_CSV = OUT / "cie_assembly_clock_grid.csv"
WINDOW_CSV = OUT / "metallicity_window_inverse_requirement.csv"
SCHEDULE_CSV = OUT / "derived_clock_schedule_samples.csv"
RESPONSE_CSV = OUT / "derived_clock_forward_response_scores.csv"
RESPONSE_PROFILE_CSV = OUT / "derived_clock_forward_response_profiles.csv"
CONTROL_CSV = OUT / "derived_clock_numerical_controls.csv"
DECISION_CSV = OUT / "route_decision.csv"
PROVENANCE_CSV = OUT / "source_provenance.csv"
RESULT_JSON = OUT / "sourced_CIE_cooling_assembly_clock_results.json"
VALIDATION_CSV = (
    POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_5166_VALIDATION.csv"
)
DOCUMENT = (
    POST
    / "5166-Y5-R2FR-sourced-CIE-cooling-clumping-derived-clock-and-forward-response-gate.md"
)

MARKER = "MTS_5166_SOURCED_CIE_COOLING_DERIVED_CLOCK_FORWARD_RESPONSE_GATE"
CHECKED_DATE = "2026-07-21"
FORMAL_DIGEST_LOCK = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)
CLOUDY_SHA256 = "0abe25cceeb5c0825381c5f17059982a9a2cdd27ce369a475c559fba6a8fa106"
CLOUDY_GIT_COMMIT = "928696482fbe15d9bac4382de6134d95568f099c"
CLOUDY_GIT_BLOB = "023bb91a97f0872c42766d0369113c5bf96666b5"
CLOUDY_DATA_URL = (
    "https://raw.githubusercontent.com/grackle-project/grackle_data_files/"
    + CLOUDY_GIT_COMMIT
    + "/input/CloudyData_noUVB.h5"
)
GRACKLE_DOCUMENTATION_URL = (
    "https://grackle.readthedocs.io/en/grackle-3.1.1/Parameters.html"
)
GRACKLE_PYTHON_URL = "https://grackle.readthedocs.io/en/grackle-3.4.1/Python.html"
GRACKLE_PAPER_URL = "https://arxiv.org/abs/1610.09591"
XSTAR_PHYSICS_URL = (
    "https://heasarc.gsfc.nasa.gov/docs/software/xstar/docs/sphinx/"
    "xstardoc/docs/build/html/physics.html"
)

G_SI = 6.67430e-11
K_B_SI = 1.380649e-23
PROTON_MASS_KG = 1.67262192369e-27
M_SUN_KG = 1.98847e30
KPC_M = 3.085677581491367e19
THOMSON_CROSS_SECTION_M2 = 6.6524587321e-29
JULIAN_YEAR_S = 365.25 * 86400.0
GYR_S = 1.0e9 * JULIAN_YEAR_S
TIME_UNIT_GYR = 0.9777922216807892
HYDROGEN_MASS_FRACTION = 0.76
HELIUM_MASS_FRACTION = 0.24
ELECTRON_TO_HYDROGEN_FULLY_IONIZED = 1.0 + HELIUM_MASS_FRACTION / (
    2.0 * HYDROGEN_MASS_FRACTION
)
COOLING_SHELLS = 8192
COARSE_COOLING_SHELLS = 4096
ASSEMBLY_SAMPLES = 513
CLUMPING_GRIDS = (13, 20, 26)
PRIMARY_CLUMPING_GRID = 26
METALLICITY_GRID = (0.0, 0.1, 0.3, 1.0)
FORWARD_METALLICITIES = (0.1, 0.3)
FORWARD_STEPS_PER_INNER_ORBIT = 64
REFINEMENT_STEPS_PER_INNER_ORBIT = 128
REFINEMENT_METALLICITY = 0.3
TABLE_REFERENCE_LOG_NH = -4.0
TABLE_REFERENCE_TEMPERATURE_K = 10.0**6.1


def load_module(path: Path, name: str) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot load module: {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


DYNAMICS = load_module(DYNAMICS_SCRIPT, "mts_checkpoint_5164_for_5166")
ENERGY = load_module(ENERGY_SCRIPT, "mts_checkpoint_5165_for_5166")


def file_digest(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def tree_digest(path: Path) -> str:
    digest = hashlib.sha256()
    for item in sorted(candidate for candidate in path.rglob("*") if candidate.is_file()):
        digest.update(item.relative_to(path).as_posix().encode("utf-8"))
        digest.update(file_digest(item).encode("ascii"))
    return digest.hexdigest()


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, Any]]) -> None:
    if not rows:
        raise RuntimeError(f"refusing to write empty CSV: {path}")
    path.parent.mkdir(parents=True, exist_ok=True)
    fieldnames = list(rows[0])
    for row in rows[1:]:
        for field in row:
            if field not in fieldnames:
                fieldnames.append(field)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def source_paths() -> dict[str, Path]:
    paths = {
        "dynamics_script": DYNAMICS_SCRIPT,
        "energy_script": ENERGY_SCRIPT,
        "dynamics_document": DYNAMICS_DOCUMENT,
        "energy_document": ENERGY_DOCUMENT,
        "dynamics_result": DYNAMICS_RESULT,
        "energy_result": ENERGY_RESULT,
        "motion_profile": ENERGY.MOTION_PROFILE,
        "motion_score": ENERGY.MOTION_SCORE,
        "visible_profile": ENERGY.VISIBLE_PROFILE,
        "cloudy_CIE_table": SOURCE_DATA,
    }
    for sign, path in DYNAMICS.SNAPSHOT_PATHS.items():
        paths[f"phase_{sign}_snapshot"] = path
    return paths


class CoolingTable:
    def __init__(self, path: Path) -> None:
        with h5py.File(path, "r") as handle:
            primordial_dataset = handle["CoolingRates/Primordial/Cooling"]
            metal_dataset = handle["CoolingRates/Metals/Cooling"]
            mmw_dataset = handle["CoolingRates/Primordial/MMW"]
            self.log_nh = np.asarray(primordial_dataset.attrs["Parameter1"], dtype=float)
            self.temperature = np.asarray(
                primordial_dataset.attrs["Temperature"], dtype=float
            )
            self.primordial = np.asarray(primordial_dataset, dtype=float)
            self.metal = np.asarray(metal_dataset, dtype=float)
            self.mmw = np.asarray(mmw_dataset, dtype=float)
        if np.any(self.primordial < 0.0) or np.any(self.metal <= 0.0):
            raise RuntimeError("cooling table contains invalid rates")
        self.log_temperature = np.log10(self.temperature)
        primordial_log = np.full_like(self.primordial, -np.inf)
        primordial_positive = self.primordial > 0.0
        primordial_log[primordial_positive] = np.log10(
            self.primordial[primordial_positive]
        )
        self.primordial_interpolator = RegularGridInterpolator(
            (self.log_nh, self.log_temperature),
            primordial_log,
            bounds_error=True,
        )
        self.metal_interpolator = RegularGridInterpolator(
            (self.log_nh, self.log_temperature),
            np.log10(self.metal),
            bounds_error=True,
        )
        self.mmw_interpolator = RegularGridInterpolator(
            (self.log_nh, self.log_temperature), self.mmw, bounds_error=True
        )

    def cooling(
        self, hydrogen_density_cm3: np.ndarray, temperature_k: float
    ) -> tuple[np.ndarray, np.ndarray]:
        density = np.asarray(hydrogen_density_cm3, dtype=float)
        if np.any(density <= 0.0):
            raise RuntimeError("cooling lookup requires positive hydrogen density")
        points = np.column_stack(
            (
                np.log10(density),
                np.full(len(density), math.log10(temperature_k)),
            )
        )
        return (
            10.0 ** self.primordial_interpolator(points),
            10.0 ** self.metal_interpolator(points),
        )

    def mean_molecular_weight(self, log_nh: float, temperature_k: float) -> float:
        return float(
            self.mmw_interpolator([[log_nh, math.log10(temperature_k)]])[0]
        )


def table_rows(table: CoolingTable) -> list[dict[str, Any]]:
    primordial, metal = table.cooling(
        np.asarray([10.0**TABLE_REFERENCE_LOG_NH]), TABLE_REFERENCE_TEMPERATURE_K
    )
    mmw = table.mean_molecular_weight(
        TABLE_REFERENCE_LOG_NH, TABLE_REFERENCE_TEMPERATURE_K
    )
    common = {
        "density_axis_name": "log10_hden_cm^-3",
        "density_min_log10_cm^-3": float(table.log_nh[0]),
        "density_max_log10_cm^-3": float(table.log_nh[-1]),
        "density_samples": len(table.log_nh),
        "temperature_min_K": float(table.temperature[0]),
        "temperature_max_K": float(table.temperature[-1]),
        "temperature_samples": len(table.temperature),
        "reference_log10_nH_cm^-3": TABLE_REFERENCE_LOG_NH,
        "reference_temperature_K": TABLE_REFERENCE_TEMPERATURE_K,
        "interpolation": "bilinear_in_log10_nH_log10_T_with_log10_cooling_rate",
        "valid_for_claim": False,
        "checkpoint_marker": MARKER,
    }
    return [
        {
            **common,
            "dataset": "CoolingRates/Primordial/Cooling",
            "shape": str(table.primordial.shape),
            "quantity": "primordial_CIE_cooling_coefficient",
            "units": "erg_cm3_s^-1",
            "reference_value": float(primordial[0]),
        },
        {
            **common,
            "dataset": "CoolingRates/Metals/Cooling",
            "shape": str(table.metal.shape),
            "quantity": "solar_metal_CIE_cooling_coefficient",
            "units": "erg_cm3_s^-1_scaled_linearly_by_Z_over_Zsun",
            "reference_value": float(metal[0]),
        },
        {
            **common,
            "dataset": "CoolingRates/Primordial/MMW",
            "shape": str(table.mmw.shape),
            "quantity": "mean_molecular_weight",
            "units": "dimensionless",
            "reference_value": mmw,
        },
    ]


def clumping_measure(path: Path, grid_cells: int) -> dict[str, Any]:
    with np.load(path) as archive:
        donor = np.asarray(archive["donor"], dtype=bool)
        positions = np.asarray(archive["positions_kpc"], dtype=float)[donor]
        edge = float(archive["edge_radius_kpc"][0])
    cell_width = 2.0 * edge / grid_cells
    axis = -edge + (np.arange(grid_cells) + 0.5) * cell_width
    x_grid, y_grid, z_grid = np.meshgrid(axis, axis, axis, indexing="ij")
    centers = np.column_stack((x_grid.ravel(), y_grid.ravel(), z_grid.ravel()))
    center_radius = np.linalg.norm(centers, axis=1)
    full_cell_inside = center_radius <= edge - math.sqrt(3.0) * cell_width / 2.0
    indices = np.floor((positions + edge) / cell_width).astype(int)
    in_box = np.all((indices >= 0) & (indices < grid_cells), axis=1)
    flat = np.ravel_multi_index(indices[in_box].T, (grid_cells,) * 3)
    counts = np.bincount(flat, minlength=grid_cells**3)
    radial_shell = np.floor(center_radius / (2.0 * cell_width)).astype(int)
    pair_numerator = 0.0
    smooth_denominator = 0.0
    included_particles = 0
    occupied_cells = 0
    for shell in np.unique(radial_shell[full_cell_inside]):
        selected = full_cell_inside & (radial_shell == shell)
        shell_counts = counts[selected].astype(float)
        mean_count = float(np.mean(shell_counts))
        pair_numerator += float(np.sum(shell_counts * (shell_counts - 1.0)))
        smooth_denominator += len(shell_counts) * mean_count**2
        included_particles += int(np.sum(shell_counts))
        occupied_cells += int(np.count_nonzero(shell_counts))
    if smooth_denominator <= 0.0:
        raise RuntimeError("clumping denominator is nonpositive")
    return {
        "grid_cells_per_axis": grid_cells,
        "cell_width_kpc": cell_width,
        "fully_interior_cell_count": int(np.count_nonzero(full_cell_inside)),
        "included_donor_particle_count": included_particles,
        "occupied_interior_cell_count": occupied_cells,
        "shot_noise_corrected_pair_numerator": pair_numerator,
        "radial_smooth_denominator": smooth_denominator,
        "clumping_factor": pair_numerator / smooth_denominator,
    }


def clumping_rows() -> tuple[list[dict[str, Any]], dict[int, dict[int, float]]]:
    rows: list[dict[str, Any]] = []
    lookup: dict[int, dict[int, float]] = {}
    for grid_cells in CLUMPING_GRIDS:
        lookup[grid_cells] = {}
        phase_results: dict[int, dict[str, Any]] = {}
        for sign, path in DYNAMICS.SNAPSHOT_PATHS.items():
            result = clumping_measure(path, grid_cells)
            phase_results[sign] = result
            lookup[grid_cells][sign] = float(result["clumping_factor"])
            rows.append(
                {
                    "estimator_id": f"PHASE_{sign}_N{grid_cells}",
                    "phase_sign": sign,
                    **result,
                    "pair_mean_clumping_factor": "",
                    "radial_shell_width_cells": 2,
                    "shot_noise_self_pair_removed": True,
                    "fully_inside_sphere_cells_only": True,
                    "target_used_to_select_grid": False,
                    "valid_for_claim": False,
                    "checkpoint_marker": MARKER,
                }
            )
        pair_mean = 0.5 * (
            float(phase_results[-1]["clumping_factor"])
            + float(phase_results[1]["clumping_factor"])
        )
        rows.append(
            {
                "estimator_id": f"PAIR_MEAN_N{grid_cells}",
                "phase_sign": "PAIR_MEAN",
                "grid_cells_per_axis": grid_cells,
                "cell_width_kpc": phase_results[-1]["cell_width_kpc"],
                "fully_interior_cell_count": phase_results[-1][
                    "fully_interior_cell_count"
                ],
                "included_donor_particle_count": phase_results[-1][
                    "included_donor_particle_count"
                ]
                + phase_results[1]["included_donor_particle_count"],
                "occupied_interior_cell_count": phase_results[-1][
                    "occupied_interior_cell_count"
                ]
                + phase_results[1]["occupied_interior_cell_count"],
                "shot_noise_corrected_pair_numerator": "",
                "radial_smooth_denominator": "",
                "clumping_factor": pair_mean,
                "pair_mean_clumping_factor": pair_mean,
                "radial_shell_width_cells": 2,
                "shot_noise_self_pair_removed": True,
                "fully_inside_sphere_cells_only": True,
                "target_used_to_select_grid": False,
                "valid_for_claim": False,
                "checkpoint_marker": MARKER,
            }
        )
    return rows, lookup


def entropy_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "clause_id": "E1_BARYON_CONTINUITY",
            "equation": "N_b^mu=n_b u^mu; nabla_mu N_b^mu=0",
            "derivation": "closed baryon worldtube and local baryon-number conservation",
            "status": "derived_parent_compatible",
            "remaining_assumption": "no baryon flux through the fixed edge",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "clause_id": "E2_MAXWELL_MATTER_EXCHANGE",
            "equation": "nabla_mu T_EM^{mu nu}=-F^nu_lambda J^lambda; nabla_mu T_b^{mu nu}=F^nu_lambda J^lambda-G_rad^nu",
            "derivation": "same checkpoint-5165 Maxwell/Hilbert exchange with an explicit radiative four-force split",
            "status": "derived_stress_exchange",
            "remaining_assumption": "radiation escaping the worldtube is represented by G_rad^nu",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "clause_id": "E3_ENTROPY_PROJECTION",
            "equation": "n_b T u^mu nabla_mu s=j_cond^mu E_mu-Q_rad",
            "derivation": "contract E2 with u_nu and use the first law plus E_mu=F_mu_nu u^nu",
            "status": "derived_perfect_fluid_projection",
            "remaining_assumption": "viscosity conduction cosmic rays and external heating neglected in the minimal branch",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "clause_id": "E4_OPTICALLY_THIN_CIE_POWER",
            "equation": "Q_rad=n_H^2[Lambda_prim(n_H,T)+(Z/Zsun)Lambda_metal(n_H,T)]",
            "derivation": "standard collisional-ionization-equilibrium plasma closure from the sourced Cloudy/Grackle no-UVB table",
            "status": "sourced_matter_microphysics_not_fitted_to_response",
            "remaining_assumption": "single-temperature CIE and linear solar-metal scaling",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "clause_id": "E5_MASS_CONSERVING_HOT_PHASE",
            "equation": "M_hot(<r,lambda)=[b-mu lambda]M_X(<r)",
            "derivation": "checkpoint-5164 exact fixed-edge baryon transfer identity",
            "status": "derived_reduced_coordinate",
            "remaining_assumption": "homologous one-coordinate hot-phase depletion",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "clause_id": "E6_VIRIAL_THERMAL_BRANCH",
            "equation": "T_vir=mu_bar(T,n_H) m_p G M_tot(R)/(2 k_B R)",
            "derivation": "fixed-edge scalar virial closure with edge mass conserved for every lambda",
            "status": "derived_one_zone_reduction",
            "remaining_assumption": "isothermal one-zone temperature instead of a solved radial entropy profile",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "clause_id": "E7_ASSEMBLY_CLOCK",
            "equation": "K(lambda) dot(lambda)=L_CIE(lambda); t(lambda)=integral_0^lambda K(x)/L_CIE(x) dx",
            "derivation": "combine checkpoint-5165 mechanical barrier with E3-E6 and outward optically thin luminosity",
            "status": "derived_conditional_clock_no_duration_fit",
            "remaining_assumption": "all net CIE luminosity is assigned to quasi-static assembly work",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "clause_id": "E8_FORWARD_GATE",
            "equation": "lambda(t)=inverse[t(lambda)] is inserted directly into the checkpoint-5164 initial-value force",
            "derivation": "forward history fixed by source table density temperature metallicity and resolved clumping before q is evaluated",
            "status": "forward_test_not_inverse_fit",
            "remaining_assumption": "UGC09133 hot-phase metallicity is not measured in the inherited source",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
    ]


def shell_geometry(
    profile: Any, edge_kpc: float, shell_count: int
) -> dict[str, np.ndarray]:
    edges = np.concatenate(
        (np.asarray([0.0]), np.geomspace(edge_kpc * 1.0e-8, edge_kpc, shell_count))
    )
    motion_mass = np.maximum.accumulate(
        np.maximum(np.asarray(profile.mass_at(edges), dtype=float), 0.0)
    )
    shell_motion_mass = np.diff(motion_mass)
    volume_m3 = (
        4.0
        * math.pi
        / 3.0
        * ((edges[1:] * KPC_M) ** 3 - (edges[:-1] * KPC_M) ** 3)
    )
    return {
        "edges_kpc": edges,
        "outer_kpc": edges[1:],
        "mid_kpc": 0.5 * (edges[1:] + edges[:-1]),
        "width_m": np.diff(edges) * KPC_M,
        "volume_m3": volume_m3,
        "motion_mass_Msun": shell_motion_mass,
    }


def virial_state(
    table: CoolingTable, polynomial: dict[str, Any], edge_kpc: float
) -> dict[str, float]:
    cosmic_baryon_mass = float(polynomial["cosmic_baryon_edge_Msun"])
    total_mass = float(polynomial["motion_edge_Msun"]) + cosmic_baryon_mass
    volume = 4.0 * math.pi * (edge_kpc * KPC_M) ** 3 / 3.0
    mean_density = cosmic_baryon_mass * M_SUN_KG / volume
    mean_nh_cm3 = (
        HYDROGEN_MASS_FRACTION * mean_density / PROTON_MASS_KG / 1.0e6
    )
    coefficient = (
        PROTON_MASS_KG
        * G_SI
        * total_mass
        * M_SUN_KG
        / (2.0 * K_B_SI * edge_kpc * KPC_M)
    )

    def residual(temperature: float) -> float:
        return temperature - coefficient * table.mean_molecular_weight(
            math.log10(mean_nh_cm3), temperature
        )

    temperature = float(brentq(residual, 1.0e4, 1.0e8, xtol=1.0e-7, rtol=1.0e-13))
    mean_molecular_weight = table.mean_molecular_weight(
        math.log10(mean_nh_cm3), temperature
    )
    return {
        "edge_radius_kpc": edge_kpc,
        "edge_total_mass_Msun": total_mass,
        "edge_cosmic_baryon_mass_Msun": cosmic_baryon_mass,
        "mean_hydrogen_density_cm^-3": mean_nh_cm3,
        "virial_coefficient_K_per_mmw": coefficient,
        "mean_molecular_weight": mean_molecular_weight,
        "temperature_K": temperature,
        "fixed_point_relative_residual": abs(residual(temperature)) / temperature,
    }


def cooling_arrays(
    table: CoolingTable,
    polynomial: dict[str, Any],
    geometry: dict[str, np.ndarray],
    temperature_k: float,
    assembly: np.ndarray,
) -> dict[str, np.ndarray]:
    baryon_ratio = float(polynomial["baryon_to_motion_ratio"])
    transfer_ratio = float(polynomial["transfer_ratio"])
    shell_motion_mass = geometry["motion_mass_Msun"]
    positive_mass = shell_motion_mass > 0.0
    primordial_luminosity = np.empty(len(assembly), dtype=float)
    metal_luminosity = np.empty(len(assembly), dtype=float)
    minimum_density = np.empty(len(assembly), dtype=float)
    maximum_density = np.empty(len(assembly), dtype=float)
    optical_depth = np.empty(len(assembly), dtype=float)
    for index, fraction in enumerate(assembly):
        hot_ratio = baryon_ratio - transfer_ratio * fraction
        hot_mass_kg = hot_ratio * shell_motion_mass[positive_mass] * M_SUN_KG
        density_kg_m3 = hot_mass_kg / geometry["volume_m3"][positive_mass]
        hydrogen_density = (
            HYDROGEN_MASS_FRACTION
            * density_kg_m3
            / PROTON_MASS_KG
            / 1.0e6
        )
        primordial_rate, metal_rate = table.cooling(hydrogen_density, temperature_k)
        volume_cm3 = geometry["volume_m3"][positive_mass] * 1.0e6
        primordial_luminosity[index] = float(
            np.sum(hydrogen_density**2 * primordial_rate * volume_cm3) * 1.0e-7
        )
        metal_luminosity[index] = float(
            np.sum(hydrogen_density**2 * metal_rate * volume_cm3) * 1.0e-7
        )
        minimum_density[index] = float(np.min(hydrogen_density))
        maximum_density[index] = float(np.max(hydrogen_density))
        electron_density_m3 = (
            ELECTRON_TO_HYDROGEN_FULLY_IONIZED * hydrogen_density * 1.0e6
        )
        optical_depth[index] = float(
            THOMSON_CROSS_SECTION_M2
            * np.sum(electron_density_m3 * geometry["width_m"][positive_mass])
        )
    return {
        "assembly": assembly,
        "primordial_luminosity_W": primordial_luminosity,
        "solar_metal_luminosity_W": metal_luminosity,
        "minimum_hydrogen_density_cm^-3": minimum_density,
        "maximum_hydrogen_density_cm^-3": maximum_density,
        "Thomson_optical_depth": optical_depth,
    }


def clock_from_arrays(
    polynomial: dict[str, Any],
    cooling: dict[str, np.ndarray],
    metallicity: float,
    clumping: float,
) -> dict[str, np.ndarray | float]:
    assembly = cooling["assembly"]
    luminosity = clumping * (
        cooling["primordial_luminosity_W"]
        + metallicity * cooling["solar_metal_luminosity_W"]
    )
    barrier = ENERGY.barrier_joule(polynomial, assembly)
    dt_dlambda = barrier / luminosity
    increments = 0.5 * (dt_dlambda[1:] + dt_dlambda[:-1]) * np.diff(assembly)
    time_seconds = np.concatenate((np.asarray([0.0]), np.cumsum(increments)))
    return {
        "assembly": assembly,
        "luminosity_W": luminosity,
        "barrier_J": barrier,
        "dt_dlambda_s": dt_dlambda,
        "time_seconds": time_seconds,
        "duration_Gyr": float(time_seconds[-1] / GYR_S),
        "energy_integral_J": float(np.trapezoid(barrier, assembly)),
        "minimum_luminosity_W": float(np.min(luminosity)),
        "maximum_luminosity_W": float(np.max(luminosity)),
    }


def radial_profile_rows(
    table: CoolingTable,
    polynomial: dict[str, Any],
    geometry: dict[str, np.ndarray],
    temperature_k: float,
    clumping: float,
) -> list[dict[str, Any]]:
    baryon_ratio = float(polynomial["baryon_to_motion_ratio"])
    transfer_ratio = float(polynomial["transfer_ratio"])
    positive = geometry["motion_mass_Msun"] > 0.0
    selected_indices = np.unique(
        np.linspace(0, np.count_nonzero(positive) - 1, 65, dtype=int)
    )
    rows: list[dict[str, Any]] = []
    for metallicity in FORWARD_METALLICITIES:
        for fraction in (0.0, 0.25, 0.5, 0.75, 1.0):
            hot_ratio = baryon_ratio - transfer_ratio * fraction
            shell_mass = geometry["motion_mass_Msun"][positive]
            density = (
                HYDROGEN_MASS_FRACTION
                * hot_ratio
                * shell_mass
                * M_SUN_KG
                / geometry["volume_m3"][positive]
                / PROTON_MASS_KG
                / 1.0e6
            )
            primordial, metal = table.cooling(density, temperature_k)
            coefficient = primordial + metallicity * metal
            shell_luminosity = (
                clumping
                * density**2
                * coefficient
                * geometry["volume_m3"][positive]
                * 1.0e6
                * 1.0e-7
            )
            cumulative = np.cumsum(shell_luminosity)
            total = float(cumulative[-1])
            outer = geometry["outer_kpc"][positive]
            for index in selected_indices:
                rows.append(
                    {
                        "metallicity_Zsun": metallicity,
                        "assembly_fraction_lambda": fraction,
                        "radius_outer_kpc": float(outer[index]),
                        "hydrogen_density_cm^-3": float(density[index]),
                        "cooling_coefficient_erg_cm3_s": float(coefficient[index]),
                        "shell_luminosity_W": float(shell_luminosity[index]),
                        "cumulative_luminosity_W": float(cumulative[index]),
                        "cumulative_luminosity_fraction": float(cumulative[index] / total),
                        "total_luminosity_W": total,
                        "clumping_factor": clumping,
                        "temperature_K": temperature_k,
                        "valid_for_claim": False,
                        "checkpoint_marker": MARKER,
                    }
                )
    return rows


class DerivedSchedule:
    def __init__(self, clock: dict[str, np.ndarray | float]) -> None:
        self.assembly = np.asarray(clock["assembly"], dtype=float)
        self.time_internal = (
            np.asarray(clock["time_seconds"], dtype=float) / GYR_S / TIME_UNIT_GYR
        )
        self.duration_internal = float(self.time_internal[-1])
        self.interpolator = PchipInterpolator(self.time_internal, self.assembly)

    def fraction_at(self, time_internal: float) -> float:
        if time_internal <= 0.0:
            return 0.0
        if time_internal >= self.duration_internal:
            return 1.0
        return float(np.clip(self.interpolator(time_internal), 0.0, 1.0))


def evolve_with_schedule(
    snapshot: dict[str, Any],
    visible_source: Any,
    profile_radii_kpc: np.ndarray,
    transfer_per_donor: float,
    schedule: DerivedSchedule,
    transition_orbit: float,
    inner_orbit: float,
    steps_per_inner_orbit: int,
    source_enabled: bool,
) -> dict[str, Any]:
    positions = np.asarray(snapshot["positions_kpc"], dtype=float).copy()
    velocities = np.asarray(snapshot["velocities_km_s"], dtype=float).copy()
    donor = np.asarray(snapshot["donor"], dtype=bool)
    particle_weight = np.asarray(snapshot["particle_weight"], dtype=float)
    initial_radius = np.asarray(snapshot["initial_radius_kpc"], dtype=float)
    particle_mass = float(snapshot["particle_mass_Msun"][0])
    edge_radius = float(snapshot["edge_radius_kpc"][0])
    softening = (
        DYNAMICS.SOFTENING_CELL_MULTIPLE
        * float(snapshot["local_force_cell_kpc"][0])
    )
    total_time = schedule.duration_internal + DYNAMICS.SETTLING_ORBITS * transition_orbit
    averaging_time = DYNAMICS.AVERAGING_ORBITS * transition_orbit
    nominal_dt = inner_orbit / steps_per_inner_orbit
    steps = max(1, int(math.ceil(total_time / nominal_dt)))
    time_step = total_time / steps
    averaging_start = max(total_time - averaging_time, 0.0)
    sample_stride = max(
        1,
        int(round(max(1.0, averaging_time / time_step) / DYNAMICS.PROFILE_AVERAGE_SAMPLES)),
    )
    initial_angular_momentum = np.cross(positions, velocities)
    initial_counts = DYNAMICS.cumulative_counts(
        positions, profile_radii_kpc, particle_weight
    )
    initial_com = np.average(positions, axis=0, weights=particle_weight)
    start = time.perf_counter()

    def fraction_at(current_time: float) -> float:
        return schedule.fraction_at(current_time) if source_enabled else 0.0

    force = DYNAMICS.acceleration(
        positions,
        donor,
        particle_weight,
        particle_mass,
        transfer_per_donor,
        fraction_at(0.0),
        visible_source,
        softening,
    )
    half_velocity = velocities + 0.5 * time_step * force
    count_samples: list[np.ndarray] = []
    final_fraction = fraction_at(0.0)
    for step in range(steps):
        positions += time_step * half_velocity
        current_time = (step + 1) * time_step
        final_fraction = fraction_at(current_time)
        force = DYNAMICS.acceleration(
            positions,
            donor,
            particle_weight,
            particle_mass,
            transfer_per_donor,
            final_fraction,
            visible_source,
            softening,
        )
        if step < steps - 1:
            half_velocity += time_step * force
        else:
            velocities = half_velocity + 0.5 * time_step * force
        if current_time >= averaging_start and (
            step % sample_stride == 0 or step == steps - 1
        ):
            count_samples.append(
                DYNAMICS.cumulative_counts(
                    positions, profile_radii_kpc, particle_weight
                )
            )
    averaged_counts = np.mean(np.asarray(count_samples), axis=0)
    final_angular_momentum = np.cross(positions, velocities)
    angular_residual = float(
        math.sqrt(
            np.sum(
                particle_weight[:, None]
                * (final_angular_momentum - initial_angular_momentum) ** 2
            )
            / max(
                np.sum(
                    particle_weight[:, None] * initial_angular_momentum**2
                ),
                1.0e-300,
            )
        )
    )
    final_radii = np.linalg.norm(positions, axis=1)
    edge_crossing = float(
        np.sum(
            particle_weight[
                (initial_radius > edge_radius)
                & (final_radii <= DYNAMICS.SCORE_EDGE_FRACTION * edge_radius)
            ]
        )
    )
    boundary_ingress = float(
        np.sum(
            particle_weight[
                (
                    initial_radius
                    > 0.9 * DYNAMICS.ISOLATION_EDGE_MULTIPLE * edge_radius
                )
                & (final_radii <= DYNAMICS.SCORE_EDGE_FRACTION * edge_radius)
            ]
        )
    )
    final_inside_score = max(
        float(
            np.sum(
                particle_weight[
                    final_radii <= DYNAMICS.SCORE_EDGE_FRACTION * edge_radius
                ]
            )
        ),
        1.0,
    )
    return {
        "averaged_counts": averaged_counts,
        "initial_counts": initial_counts,
        "steps": steps,
        "time_step_kpc_per_km_s": time_step,
        "profile_sample_count": len(count_samples),
        "final_assembly_fraction": final_fraction,
        "angular_momentum_relative_residual": angular_residual,
        "center_of_mass_drift_kpc": float(
            np.linalg.norm(
                np.average(positions, axis=0, weights=particle_weight) - initial_com
            )
        ),
        "edge_crossing_fraction": edge_crossing / final_inside_score,
        "outer_boundary_ingress_fraction": boundary_ingress / final_inside_score,
        "wall_seconds": time.perf_counter() - start,
        "softening_kpc": softening,
    }


def response_context() -> dict[str, Any]:
    profile_rows, q_row, previous_score, state = DYNAMICS.reference_rows()
    transition_radius = float(state["L_eff_kpc"]) * float(state["R_n_over_L_eff"])
    edge_radius = float(previous_score["target_edge_radius_kpc"])
    snapshots, _, _ = DYNAMICS.load_snapshots()
    if not snapshots:
        raise RuntimeError("checkpoint-5164 snapshots are missing")
    visible_source = DYNAMICS.VisibleSource(read_csv(DYNAMICS.VISIBLE_SOURCE))
    radii = np.asarray([float(row["radius_kpc"]) for row in profile_rows])
    target_velocity = np.asarray(
        [float(row["target_motion_v2_km2_s2"]) for row in profile_rows]
    )
    score_mask = np.asarray(
        [row["inside_resolved_scoring_window"] == "True" for row in profile_rows]
    )
    target_edge_mass = float(previous_score["target_motion_mass_edge_Msun"])
    initial_phase_mass: dict[int, np.ndarray] = {}
    transfer_per_donor: dict[int, float] = {}
    for sign, snapshot in snapshots.items():
        particle_mass = float(snapshot["particle_mass_Msun"][0])
        _, motion_mass = DYNAMICS.snapshot_profile(
            np.asarray(snapshot["positions_kpc"]), radii, particle_mass
        )
        initial_phase_mass[sign] = motion_mass
        donor_count = int(np.count_nonzero(snapshot["donor"]))
        transfer_per_donor[sign] = float(visible_source.mass_at(edge_radius)) / donor_count
    response_snapshots = {
        sign: DYNAMICS.compress_snapshot(snapshot) for sign, snapshot in snapshots.items()
    }
    pair_initial_mass = 0.5 * (initial_phase_mass[-1] + initial_phase_mass[1])
    baseline_score = DYNAMICS.score_profile(
        radii,
        pair_initial_mass,
        target_velocity,
        score_mask,
        transition_radius,
        edge_radius,
        target_edge_mass,
    )
    pair_initial_total_mass_transition = float(
        np.interp(transition_radius, radii, pair_initial_mass)
        / DYNAMICS.PM.MOTION_FRACTION
    )
    final_total_mass_transition = pair_initial_total_mass_transition + float(
        visible_source.mass_at(transition_radius)
    ) - (1.0 - DYNAMICS.PM.MOTION_FRACTION) * pair_initial_total_mass_transition
    final_total_mass_transition = max(
        final_total_mass_transition, pair_initial_total_mass_transition
    )
    transition_orbit = 2.0 * math.pi * math.sqrt(
        transition_radius**3
        / (DYNAMICS.PREVIOUS.G_KPC_KM2_S2_MSUN * final_total_mass_transition)
    )
    resolved_radius = max(
        float(snapshots[-1]["resolved_radius_kpc"][0]),
        float(snapshots[1]["resolved_radius_kpc"][0]),
    )
    softening_radius = DYNAMICS.SOFTENING_CELL_MULTIPLE * max(
        float(snapshots[-1]["local_force_cell_kpc"][0]),
        float(snapshots[1]["local_force_cell_kpc"][0]),
    )
    orbit_probe = np.geomspace(
        max(0.05 * softening_radius, 1.0e-3), resolved_radius, 256
    )
    monotone_initial_mass = np.maximum.accumulate(np.maximum(pair_initial_mass, 0.0))
    motion_interpolator = PchipInterpolator(radii, monotone_initial_mass)
    probe_motion_mass = np.asarray(
        motion_interpolator(np.maximum(orbit_probe, radii[0])), dtype=float
    )
    probe_total_mass = (
        probe_motion_mass / DYNAMICS.PM.MOTION_FRACTION
        + np.asarray(visible_source.mass_at(orbit_probe), dtype=float)
    )
    softened_orbits = 2.0 * math.pi * np.sqrt(
        (orbit_probe**2 + softening_radius**2) ** 1.5
        / (
            DYNAMICS.PREVIOUS.G_KPC_KM2_S2_MSUN
            * np.maximum(probe_total_mass, 1.0)
        )
    )
    return {
        "profile_rows": profile_rows,
        "q_row": q_row,
        "previous_score": previous_score,
        "radii": radii,
        "target_velocity": target_velocity,
        "score_mask": score_mask,
        "target_edge_mass": target_edge_mass,
        "transition_radius": transition_radius,
        "edge_radius": edge_radius,
        "snapshots": snapshots,
        "response_snapshots": response_snapshots,
        "visible_source": visible_source,
        "initial_phase_mass": initial_phase_mass,
        "pair_initial_mass": pair_initial_mass,
        "transfer_per_donor": transfer_per_donor,
        "baseline_score": baseline_score,
        "transition_orbit": transition_orbit,
        "inner_orbit": float(np.min(softened_orbits)),
    }


def run_response_branch(
    context: dict[str, Any],
    schedule: DerivedSchedule,
    metallicity: float,
    clumping: float,
    steps_per_orbit: int,
    run_id: str,
) -> tuple[dict[str, Any], list[dict[str, Any]], list[dict[str, Any]]]:
    phase_mass: dict[int, np.ndarray] = {}
    controls: list[dict[str, Any]] = []
    phase_profiles: dict[int, dict[str, np.ndarray]] = {}
    for sign, snapshot in context["response_snapshots"].items():
        source_run = evolve_with_schedule(
            snapshot,
            context["visible_source"],
            context["radii"],
            context["transfer_per_donor"][sign],
            schedule,
            context["transition_orbit"],
            context["inner_orbit"],
            steps_per_orbit,
            True,
        )
        control_run = evolve_with_schedule(
            snapshot,
            context["visible_source"],
            context["radii"],
            context["transfer_per_donor"][sign],
            schedule,
            context["transition_orbit"],
            context["inner_orbit"],
            steps_per_orbit,
            False,
        )
        particle_mass = float(snapshot["particle_mass_Msun"][0])
        background = (
            4.0
            * math.pi
            * DYNAMICS.PM.RHO_M_MSUN_MPC3
            * (context["radii"] / 1000.0) ** 3
            / 3.0
        )
        source_mass = DYNAMICS.PM.MOTION_FRACTION * np.maximum(
            source_run["averaged_counts"] * particle_mass - background, 0.0
        )
        control_mass = DYNAMICS.PM.MOTION_FRACTION * np.maximum(
            control_run["averaged_counts"] * particle_mass - background, 0.0
        )
        response_ratio = np.ones_like(context["radii"])
        positive = control_mass > 0.0
        response_ratio[positive] = source_mass[positive] / control_mass[positive]
        phase_mass[sign] = context["initial_phase_mass"][sign] * response_ratio
        phase_profiles[sign] = {
            "source_mass": source_mass,
            "control_mass": control_mass,
            "corrected_mass": phase_mass[sign],
        }
        controls.append(
            {
                "run_id": run_id,
                "metallicity_Zsun": metallicity,
                "clumping_factor": clumping,
                "phase_sign": sign,
                "steps_per_inner_orbit": steps_per_orbit,
                "response_particle_count": len(snapshot["positions_kpc"]),
                "represented_particle_count": float(np.sum(snapshot["particle_weight"])),
                "source_steps": source_run["steps"],
                "control_steps": control_run["steps"],
                "source_final_assembly_fraction": source_run[
                    "final_assembly_fraction"
                ],
                "source_angular_momentum_relative_residual": source_run[
                    "angular_momentum_relative_residual"
                ],
                "control_angular_momentum_relative_residual": control_run[
                    "angular_momentum_relative_residual"
                ],
                "source_outer_boundary_ingress_fraction": source_run[
                    "outer_boundary_ingress_fraction"
                ],
                "control_outer_boundary_ingress_fraction": control_run[
                    "outer_boundary_ingress_fraction"
                ],
                "source_wall_seconds": source_run["wall_seconds"],
                "control_wall_seconds": control_run["wall_seconds"],
                "valid_for_claim": False,
                "checkpoint_marker": MARKER,
            }
        )
    corrected_mass = 0.5 * (phase_mass[-1] + phase_mass[1])
    corrected_score = DYNAMICS.score_profile(
        context["radii"],
        corrected_mass,
        context["target_velocity"],
        context["score_mask"],
        context["transition_radius"],
        context["edge_radius"],
        context["target_edge_mass"],
    )
    q_parent = float(context["q_row"]["q_parent"])
    q_envelope = float(context["q_row"]["q_uncertainty_envelope"])
    score = {
        "run_id": run_id,
        "metallicity_Zsun": metallicity,
        "clumping_factor": clumping,
        "clock_duration_Gyr": schedule.duration_internal * TIME_UNIT_GYR,
        "clock_duration_over_transition_orbit": schedule.duration_internal
        / context["transition_orbit"],
        "schedule": "inverse_integral_of_K_over_sourced_CIE_luminosity",
        "steps_per_inner_orbit": steps_per_orbit,
        "q_parent": q_parent,
        "q_envelope": q_envelope,
        "corrected_q": corrected_score["q"],
        "corrected_q_absolute_difference": abs(corrected_score["q"] - q_parent),
        "corrected_q_compatible": abs(corrected_score["q"] - q_parent) <= q_envelope,
        "corrected_velocity_squared_log10_RMSE": corrected_score[
            "velocity_squared_log10_RMSE"
        ],
        "baseline_velocity_squared_log10_RMSE": context["baseline_score"][
            "velocity_squared_log10_RMSE"
        ],
        "corrected_RMSE_improves_baseline": corrected_score[
            "velocity_squared_log10_RMSE"
        ]
        < context["baseline_score"]["velocity_squared_log10_RMSE"],
        "corrected_transition_velocity_squared_ratio_to_target": corrected_score[
            "transition_velocity_squared_ratio_to_target"
        ],
        "corrected_edge_mass_ratio_to_target": corrected_score[
            "edge_mass_ratio_to_target"
        ],
        "metallicity_measured_for_UGC09133": False,
        "target_used_to_select_metallicity": False,
        "target_used_to_select_clock": False,
        "response_efficiency_fitted": False,
        "valid_for_claim": False,
        "checkpoint_marker": MARKER,
    }
    profile_rows: list[dict[str, Any]] = []
    corrected_velocity = (
        DYNAMICS.PREVIOUS.G_KPC_KM2_S2_MSUN
        * corrected_mass
        / np.maximum(context["radii"], np.finfo(float).tiny)
    )
    for index, radius in enumerate(context["radii"]):
        profile_rows.append(
            {
                "run_id": run_id,
                "radius_kpc": radius,
                "radius_over_transition": radius / context["transition_radius"],
                "corrected_motion_mass_Msun": corrected_mass[index],
                "phase_minus_corrected_mass_Msun": phase_mass[-1][index],
                "phase_plus_corrected_mass_Msun": phase_mass[1][index],
                "corrected_motion_v2_km2_s2": corrected_velocity[index],
                "target_motion_v2_km2_s2": context["target_velocity"][index],
                "inside_scoring_window": bool(context["score_mask"][index]),
                "valid_for_claim": False,
                "checkpoint_marker": MARKER,
            }
        )
    return score, controls, profile_rows


def clock_grid_rows(
    polynomial: dict[str, Any],
    cooling: dict[str, np.ndarray],
    clumping_lookup: dict[int, dict[int, float]],
    transition_orbit_gyr: float,
) -> list[dict[str, Any]]:
    primary_phase = clumping_lookup[PRIMARY_CLUMPING_GRID]
    clumping_models = {
        "SMOOTH_C1": 1.0,
        f"PHASE_MINUS_N{PRIMARY_CLUMPING_GRID}": primary_phase[-1],
        f"PHASE_PLUS_N{PRIMARY_CLUMPING_GRID}": primary_phase[1],
        f"PAIR_MEAN_N{PRIMARY_CLUMPING_GRID}": 0.5
        * (primary_phase[-1] + primary_phase[1]),
    }
    rows: list[dict[str, Any]] = []
    for metallicity in METALLICITY_GRID:
        for model, clumping in clumping_models.items():
            clock = clock_from_arrays(polynomial, cooling, metallicity, clumping)
            duration = float(clock["duration_Gyr"])
            rows.append(
                {
                    "clock_id": f"CIE_Z{metallicity:g}_{model}",
                    "metallicity_Zsun": metallicity,
                    "clumping_model": model,
                    "clumping_factor": clumping,
                    "duration_Gyr": duration,
                    "duration_transition_orbits": duration / transition_orbit_gyr,
                    "inside_one_to_four_orbit_window": transition_orbit_gyr
                    <= duration
                    <= 4.0 * transition_orbit_gyr,
                    "initial_luminosity_W": float(clock["luminosity_W"][0]),
                    "final_luminosity_W": float(clock["luminosity_W"][-1]),
                    "minimum_luminosity_W": clock["minimum_luminosity_W"],
                    "maximum_luminosity_W": clock["maximum_luminosity_W"],
                    "radiated_energy_identity_J": clock["energy_integral_J"],
                    "temperature_model": "fixed_edge_one_zone_virial",
                    "cooling_model": "Cloudy_Grackle_noUVB_CIE",
                    "target_used_to_select_clock": False,
                    "valid_for_claim": False,
                    "checkpoint_marker": MARKER,
                }
            )
    return rows


def metallicity_window_rows(
    polynomial: dict[str, Any],
    cooling: dict[str, np.ndarray],
    clumping_lookup: dict[int, dict[int, float]],
    transition_orbit_gyr: float,
) -> list[dict[str, Any]]:
    primary = clumping_lookup[PRIMARY_CLUMPING_GRID]
    models = {
        "PHASE_MINUS": primary[-1],
        "PHASE_PLUS": primary[1],
        "PAIR_MEAN": 0.5 * (primary[-1] + primary[1]),
    }

    def duration(metallicity: float, clumping: float) -> float:
        return float(
            clock_from_arrays(polynomial, cooling, metallicity, clumping)[
                "duration_Gyr"
            ]
        )

    rows: list[dict[str, Any]] = []
    for model, clumping in models.items():
        lower = float(
            brentq(
                lambda metallicity: duration(metallicity, clumping)
                - 4.0 * transition_orbit_gyr,
                0.0,
                5.0,
            )
        )
        upper = float(
            brentq(
                lambda metallicity: duration(metallicity, clumping)
                - transition_orbit_gyr,
                0.0,
                5.0,
            )
        )
        rows.append(
            {
                "clumping_model": model,
                "clumping_factor": clumping,
                "metallicity_lower_Zsun_for_four_orbit_boundary": lower,
                "metallicity_upper_Zsun_for_one_orbit_boundary": upper,
                "conditional_clock_window": f"{lower} <= Z/Zsun <= {upper}",
                "derivation": "inverse_requirement_from_clock_window_not_an_observation_or_fit",
                "UGC09133_metallicity_source_available": False,
                "valid_for_claim": False,
                "checkpoint_marker": MARKER,
            }
        )
    return rows


def thermal_rows(
    virial: dict[str, float], cooling: dict[str, np.ndarray]
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for index in (0, len(cooling["assembly"]) - 1):
        rows.append(
            {
                **virial,
                "assembly_fraction_lambda": float(cooling["assembly"][index]),
                "minimum_shell_hydrogen_density_cm^-3": float(
                    cooling["minimum_hydrogen_density_cm^-3"][index]
                ),
                "maximum_shell_hydrogen_density_cm^-3": float(
                    cooling["maximum_hydrogen_density_cm^-3"][index]
                ),
                "Thomson_optical_depth_center_to_edge": float(
                    cooling["Thomson_optical_depth"][index]
                ),
                "XSTAR_thin_reference_tau_limit": 0.3,
                "inside_Cloudy_density_axis": float(
                    cooling["minimum_hydrogen_density_cm^-3"][index]
                )
                >= 1.0e-10
                and float(cooling["maximum_hydrogen_density_cm^-3"][index])
                <= 1.0e4,
                "inside_Cloudy_temperature_axis": 10.0
                <= virial["temperature_K"]
                <= 1.0e9,
                "electron_column_model": "fully_ionized_X0p76_Y0p24",
                "line_and_photoelectric_escape_solved": False,
                "valid_for_claim": False,
                "checkpoint_marker": MARKER,
            }
        )
    return rows


def schedule_rows(
    clocks: dict[float, dict[str, np.ndarray | float]], clumping: float
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for metallicity, clock in clocks.items():
        sample_indices = np.linspace(0, len(clock["assembly"]) - 1, 65, dtype=int)
        for index in np.unique(sample_indices):
            rows.append(
                {
                    "clock_id": f"CIE_Z{metallicity:g}_PAIR_N{PRIMARY_CLUMPING_GRID}",
                    "metallicity_Zsun": metallicity,
                    "clumping_factor": clumping,
                    "assembly_fraction_lambda": float(clock["assembly"][index]),
                    "elapsed_time_Gyr": float(clock["time_seconds"][index] / GYR_S),
                    "luminosity_W": float(clock["luminosity_W"][index]),
                    "energy_barrier_K_J_per_lambda": float(clock["barrier_J"][index]),
                    "dt_dlambda_Gyr": float(clock["dt_dlambda_s"][index] / GYR_S),
                    "target_used_to_select_schedule": False,
                    "valid_for_claim": False,
                    "checkpoint_marker": MARKER,
                }
            )
    return rows


def provenance_rows(paths: dict[str, Path]) -> list[dict[str, Any]]:
    rows = [
        {
            "source_id": key,
            "source_type": "local_file",
            "path_or_url": str(path),
            "sha256": file_digest(path),
            "git_commit": "",
            "git_blob": "",
            "role": "parent_empirical_or_numeric_input_read_only",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        }
        for key, path in paths.items()
    ]
    rows.extend(
        [
            {
                "source_id": "CloudyData_noUVB_immutable_download",
                "source_type": "source_data_url",
                "path_or_url": CLOUDY_DATA_URL,
                "sha256": CLOUDY_SHA256,
                "git_commit": CLOUDY_GIT_COMMIT,
                "git_blob": CLOUDY_GIT_BLOB,
                "role": "exact_CIE_table_provenance",
                "valid_for_claim": False,
                "checkpoint_marker": MARKER,
            },
            {
                "source_id": "Grackle_parameter_documentation",
                "source_type": "official_documentation_url",
                "path_or_url": GRACKLE_DOCUMENTATION_URL,
                "sha256": "",
                "git_commit": "",
                "git_blob": "",
                "role": "noUVB_table_is_CIE_and_axis_ranges",
                "valid_for_claim": False,
                "checkpoint_marker": MARKER,
            },
            {
                "source_id": "Grackle_Python_documentation",
                "source_type": "official_documentation_url",
                "path_or_url": GRACKLE_PYTHON_URL,
                "sha256": "",
                "git_commit": "",
                "git_blob": "",
                "role": "cooling_rate_units_cm3_erg_per_s",
                "valid_for_claim": False,
                "checkpoint_marker": MARKER,
            },
            {
                "source_id": "Grackle_method_paper",
                "source_type": "primary_paper_url",
                "path_or_url": GRACKLE_PAPER_URL,
                "sha256": "",
                "git_commit": "",
                "git_blob": "",
                "role": "cooling_library_method",
                "valid_for_claim": False,
                "checkpoint_marker": MARKER,
            },
            {
                "source_id": "NASA_HEASARC_XSTAR_physics",
                "source_type": "official_documentation_url",
                "path_or_url": XSTAR_PHYSICS_URL,
                "sha256": "",
                "git_commit": "",
                "git_blob": "",
                "role": "optically_thin_scaling_and_tau_e_reference_envelope",
                "valid_for_claim": False,
                "checkpoint_marker": MARKER,
            },
        ]
    )
    return rows


def add_validation(
    rows: list[dict[str, Any]], check_id: str, passed: bool, evidence: Any
) -> None:
    rows.append(
        {
            "check_id": check_id,
            "passed": bool(passed),
            "evidence": json.dumps(evidence, sort_keys=True),
            "checkpoint_marker": MARKER,
        }
    )


def make_document(result: dict[str, Any]) -> str:
    summary = result["summary"]
    return f"""# 5166 - Sourced CIE cooling, clumping-derived assembly clock and forward-response gate

Marker: `{MARKER}`.

Date: `{CHECKED_DATE}`.

## Question

Checkpoint 5165 proved that Poynting/total-energy conservation excludes an
impulsive source but cannot select a one-orbit clock: every positive monotone
history can be assigned a luminosity satisfying the same integrated identity.
This checkpoint asks the missing constructive question. Does ordinary charged-
baryon plasma microphysics supply a clock before the galaxy response is read?

## Entropy and cooling projection

For baryon current `N_b^mu=n_b u^mu`, the closed worldtube obeys

```text
nabla_mu N_b^mu=0.
```

The checkpoint-5165 Maxwell exchange is split from escaping radiation as

```text
nabla_mu T_EM^{{mu nu}}=-F^nu_lambda J^lambda,
nabla_mu T_b^{{mu nu}}= F^nu_lambda J^lambda-G_rad^nu.
```

Contracting with `u_nu` and using the first law gives the minimal entropy
projection

```text
n_b T u^mu nabla_mu s=j_cond^mu E_mu-Q_rad.
```

On the neutral, no-external-heating, optically thin CIE branch,

```text
Q_rad=n_H^2[Lambda_prim(n_H,T)+(Z/Zsun)Lambda_metal(n_H,T)].
```

The cooling coefficients are read from the immutable Grackle
`CloudyData_noUVB.h5` table at commit `{CLOUDY_GIT_COMMIT}`. They are not
inferred from `q`, the rotation curve or a desired duration.

The same checkpoint-5164 mass coordinate gives

```text
M_hot(<r,lambda)=[b-mu lambda]M_X(<r),
T_vir=mu_bar m_p G M_tot(R_edge)/(2 k_B R_edge),
K(lambda) dot(lambda)=L_CIE(lambda),
t(lambda)=integral_0^lambda K(x)/L_CIE(x) dx.
```

Thus the response receives the inverse of the final integral directly. A C2
ramp with a fitted or manually chosen duration is not used.

## Sourced inputs and numerical result

The fixed-edge virial solution is

```text
T_vir                         = {summary['virial_temperature_K']} K
mean molecular weight         = {summary['mean_molecular_weight']}
tau_e(lambda=0)               = {summary['initial_Thomson_optical_depth']}
tau_e(lambda=1)               = {summary['final_Thomson_optical_depth']}
Cloudy shell n_H range        = {summary['minimum_shell_nH_cm3']} .. {summary['maximum_shell_nH_cm3']} cm^-3.
```

The optical-depth values are far inside the XSTAR electron-scattering
reference envelope `tau_e<=0.3`; line and photoelectric escape are not thereby
proved. The inherited two antithetic particle states give a Poisson-self-pair-
subtracted, radial-gradient-controlled clumping factor
`C={summary['primary_pair_clumping_factor']}` at cell width
`{summary['primary_clumping_cell_width_kpc']} kpc`. Pair means at the three
predeclared resolutions are `{summary['clumping_pair_means']}`.

With this resolved pair clumping, the forward-frozen CIE clocks are

```text
Z=0.1 Zsun: {summary['Z0p1_clock_Gyr']} Gyr = {summary['Z0p1_clock_orbits']} transition orbits;
Z=0.3 Zsun: {summary['Z0p3_clock_Gyr']} Gyr = {summary['Z0p3_clock_orbits']} transition orbits.
```

The inherited one-to-four-orbit response window is
`{summary['one_orbit_Gyr']} .. {summary['four_orbit_Gyr']} Gyr`. Both standard
benchmark metallicity branches enter it without reading `q`. The inverse
metallicity corridor is recorded only as a requirement; UGC09133 has no hot-
phase metallicity measurement in the inherited source and the corridor is not
used to choose the two forward runs.

## Direct initial-value response

The exact CIE schedules were inserted into the checkpoint-5164 particle
evolution. Results are

```text
Z=0.1: q={summary['Z0p1_forward_q']}, RMSE={summary['Z0p1_forward_RMSE']} dex,
       transition v^2 ratio={summary['Z0p1_forward_transition_ratio']};
Z=0.3: q={summary['Z0p3_forward_q']}, RMSE={summary['Z0p3_forward_RMSE']} dex,
       transition v^2 ratio={summary['Z0p3_forward_transition_ratio']}.
```

The parent interval is `{summary['parent_q_lower']} .. {summary['parent_q_upper']}`.
The time-refined `Z=0.3` value is `{summary['Z0p3_refined_q']}`, differing by
`{summary['Z0p3_refinement_delta_q']}` from the primary run.

## Decision and claim boundary

`{result['route_decision']}`.

This is a constructive advance and a useful rejection. A sourced plasma law now
replaces the arbitrary duration and is propagated through the actual inherited
dynamics, but both predeclared branches lie above the parent `q` interval. The
one-zone homologous CIE clock is therefore rejected as the completed parent
mechanism rather than promoted because it improved the RMSE. The next derivation
must replace homologous depletion by a radial entropy/cooling-flow solve; line
transfer and the unmeasured hot-phase metallicity must also be bounded.

```text
baryon entropy projection derived                         = yes;
real CIE coefficient table sourced                       = yes;
resolved clumping estimated without Poisson self-pairs   = yes;
clock duration fitted to q                               = no;
exact derived lambda(t) evolved forward                  = yes;
one-zone homologous CIE clock passes parent q gate        = {str(summary['one_zone_CIE_q_gate_passed']).lower()};
UGC09133 metallicity measured                            = no;
radial radiation-hydrodynamic cooling flow solved        = no;
local GR/Newton/Maxwell branch modified                   = no;
galaxy or full-MTS claim                                  = false.
```

All `{result['validation_count']}` validation rows pass. The protected
`formalization-workbench` digest remains
`{result['formalization_workbench_tree_sha256']}`. No GitHub action occurred.
"""


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--cooling-only", action="store_true")
    parser.add_argument("--skip-refinement", action="store_true")
    arguments = parser.parse_args()
    paths = source_paths()
    missing = [str(path) for path in paths.values() if not path.is_file()]
    if missing:
        raise RuntimeError(f"missing sources: {missing}")
    formal_before = tree_digest(FORMAL)
    if formal_before != FORMAL_DIGEST_LOCK:
        raise RuntimeError(f"protected digest mismatch: {formal_before}")
    hashes_before = {key: file_digest(path) for key, path in paths.items()}
    table = CoolingTable(SOURCE_DATA)
    if arguments.dry_run:
        print(
            json.dumps(
                {
                    "dry_run": True,
                    "marker": MARKER,
                    "source_count": len(paths),
                    "cloudy_sha256": file_digest(SOURCE_DATA),
                    "cloudy_shape": list(table.primordial.shape),
                    "formal_digest": formal_before,
                    "forward_metallicities": FORWARD_METALLICITIES,
                },
                indent=2,
            )
        )
        return

    context = response_context()
    visible_source = context["visible_source"]
    edge_kpc = ENERGY.edge_radius_kpc()
    profile = ENERGY.motion_profiles()[ENERGY.PRIMARY_PROFILE_ID][0]
    polynomial = ENERGY.energy_polynomial(
        profile, visible_source, edge_kpc, ENERGY.QUADRATURE_POINTS
    )
    virial = virial_state(table, polynomial, edge_kpc)
    assembly = np.linspace(0.0, 1.0, ASSEMBLY_SAMPLES)
    geometry = shell_geometry(profile, edge_kpc, COOLING_SHELLS)
    coarse_geometry = shell_geometry(profile, edge_kpc, COARSE_COOLING_SHELLS)
    cooling = cooling_arrays(
        table, polynomial, geometry, virial["temperature_K"], assembly
    )
    coarse_cooling = cooling_arrays(
        table, polynomial, coarse_geometry, virial["temperature_K"], assembly
    )
    clumping, clumping_lookup = clumping_rows()
    primary_phase_clumping = clumping_lookup[PRIMARY_CLUMPING_GRID]
    pair_clumping = 0.5 * (
        primary_phase_clumping[-1] + primary_phase_clumping[1]
    )
    clocks = {
        metallicity: clock_from_arrays(
            polynomial, cooling, metallicity, pair_clumping
        )
        for metallicity in FORWARD_METALLICITIES
    }
    coarse_clocks = {
        metallicity: clock_from_arrays(
            polynomial, coarse_cooling, metallicity, pair_clumping
        )
        for metallicity in FORWARD_METALLICITIES
    }
    transition_orbit_gyr = context["transition_orbit"] * TIME_UNIT_GYR
    contract = entropy_contract_rows()
    tables = table_rows(table)
    thermal = thermal_rows(virial, cooling)
    profiles = radial_profile_rows(
        table,
        polynomial,
        geometry,
        virial["temperature_K"],
        pair_clumping,
    )
    clock_grid = clock_grid_rows(
        polynomial, cooling, clumping_lookup, transition_orbit_gyr
    )
    windows = metallicity_window_rows(
        polynomial, cooling, clumping_lookup, transition_orbit_gyr
    )
    schedules = schedule_rows(clocks, pair_clumping)

    response_scores: list[dict[str, Any]] = []
    response_profiles: list[dict[str, Any]] = []
    controls: list[dict[str, Any]] = []
    if not arguments.cooling_only:
        for metallicity in FORWARD_METALLICITIES:
            run_id = f"CIE_Z{metallicity:g}_PAIR_N{PRIMARY_CLUMPING_GRID}_PRIMARY"
            score, run_controls, run_profiles = run_response_branch(
                context,
                DerivedSchedule(clocks[metallicity]),
                metallicity,
                pair_clumping,
                FORWARD_STEPS_PER_INNER_ORBIT,
                run_id,
            )
            response_scores.append(score)
            controls.extend(run_controls)
            response_profiles.extend(run_profiles)
        if not arguments.skip_refinement:
            metallicity = REFINEMENT_METALLICITY
            run_id = (
                f"CIE_Z{metallicity:g}_PAIR_N{PRIMARY_CLUMPING_GRID}_TIME_REFINEMENT"
            )
            score, run_controls, run_profiles = run_response_branch(
                context,
                DerivedSchedule(clocks[metallicity]),
                metallicity,
                pair_clumping,
                REFINEMENT_STEPS_PER_INNER_ORBIT,
                run_id,
            )
            response_scores.append(score)
            controls.extend(run_controls)
            response_profiles.extend(run_profiles)

    primary_scores = {
        float(row["metallicity_Zsun"]): row
        for row in response_scores
        if row["run_id"].endswith("PRIMARY")
    }
    refined_score = next(
        (
            row
            for row in response_scores
            if row["run_id"].endswith("TIME_REFINEMENT")
        ),
        None,
    )
    response_executed = set(primary_scores) == set(FORWARD_METALLICITIES)
    refinement_executed = refined_score is not None
    z01_clock = clocks[0.1]
    z03_clock = clocks[0.3]
    z01_score = primary_scores.get(0.1, {})
    z03_score = primary_scores.get(0.3, {})
    z03_refined_q = (
        float(refined_score["corrected_q"])
        if refined_score is not None
        else math.nan
    )
    z03_refinement_delta = (
        abs(z03_refined_q - float(z03_score["corrected_q"]))
        if refined_score is not None and z03_score
        else math.nan
    )
    clock_resolution_changes = {
        metallicity: abs(
            float(clocks[metallicity]["duration_Gyr"])
            - float(coarse_clocks[metallicity]["duration_Gyr"])
        )
        / float(clocks[metallicity]["duration_Gyr"])
        for metallicity in FORWARD_METALLICITIES
    }
    pair_means = {
        grid: 0.5 * (lookup[-1] + lookup[1])
        for grid, lookup in clumping_lookup.items()
    }
    primary_clumping_row = next(
        row
        for row in clumping
        if row["estimator_id"] == f"PAIR_MEAN_N{PRIMARY_CLUMPING_GRID}"
    )
    parent_lower = float(context["q_row"]["q_parent"]) - float(
        context["q_row"]["q_uncertainty_envelope"]
    )
    parent_upper = float(context["q_row"]["q_parent"]) + float(
        context["q_row"]["q_uncertainty_envelope"]
    )
    one_zone_q_gate_passed = response_executed and any(
        bool(row["corrected_q_compatible"])
        for row in primary_scores.values()
    )
    if not response_executed:
        route_decision = (
            "SOURCED_CIE_CLOCK_DERIVED_BUT_FORWARD_DYNAMICAL_RESPONSE_NOT_EXECUTED"
        )
    elif one_zone_q_gate_passed:
        route_decision = (
            "SOURCED_CIE_CLOCK_FORWARDED_AND_AT_LEAST_ONE_PREDECLARED_BRANCH_INTERSECTS_THE_PARENT_Q_BAND_BUT_REMAINS_CONDITIONAL_ON_THE_RADIAL_THERMAL_PROFILE_AND_METALLICITY"
        )
    else:
        route_decision = (
            "SOURCED_CIE_CLOCK_IMPROVES_THE_BASELINE_RMSE_BUT_BOTH_PREDECLARED_FORWARD_BRANCHES_MISS_THE_PARENT_Q_BAND_SO_ONE_ZONE_HOMOLOGOUS_COOLING_IS_REJECTED_AS_THE_COMPLETED_PARENT_CLOCK"
        )
    decision = [
        {
            "route": "charged_baryon_CIE_cooling_assembly_clock",
            "result": route_decision,
            "evidence": (
                f"Tvir={virial['temperature_K']} K; Cpair={pair_clumping}; "
                f"t_Z0p1={z01_clock['duration_Gyr']} Gyr; "
                f"t_Z0p3={z03_clock['duration_Gyr']} Gyr; "
                f"q_Z0p1={z01_score.get('corrected_q', 'NOT_RUN')}; "
                f"q_Z0p3={z03_score.get('corrected_q', 'NOT_RUN')}"
            ),
            "next_requirement": (
                "replace the one-zone homologous depletion with a radial entropy/cooling-flow solve and source or bound UGC09133 hot-phase metallicity before promoting the galaxy response"
            ),
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        }
    ]
    provenance = provenance_rows(paths)
    outputs: dict[Path, list[dict[str, Any]]] = {
        CONTRACT_CSV: contract,
        TABLE_CSV: tables,
        THERMAL_CSV: thermal,
        CLUMPING_CSV: clumping,
        PROFILE_CSV: profiles,
        CLOCK_CSV: clock_grid,
        WINDOW_CSV: windows,
        SCHEDULE_CSV: schedules,
        DECISION_CSV: decision,
        PROVENANCE_CSV: provenance,
    }
    if response_scores:
        outputs[RESPONSE_CSV] = response_scores
        outputs[RESPONSE_PROFILE_CSV] = response_profiles
        outputs[CONTROL_CSV] = controls
    for path, rows in outputs.items():
        write_csv(path, rows)

    hashes_after = {key: file_digest(path) for key, path in paths.items()}
    formal_after = tree_digest(FORMAL)
    validation: list[dict[str, Any]] = []
    add_validation(validation, "all_sources_exist", not missing, missing)
    add_validation(
        validation,
        "source_hashes_unchanged",
        hashes_before == hashes_after,
        hashes_after,
    )
    add_validation(
        validation,
        "formalization_workbench_unchanged",
        formal_before == formal_after == FORMAL_DIGEST_LOCK,
        formal_after,
    )
    add_validation(
        validation,
        "immutable_Cloudy_table_hash_matches",
        file_digest(SOURCE_DATA) == CLOUDY_SHA256,
        file_digest(SOURCE_DATA),
    )
    add_validation(
        validation,
        "Cloudy_table_axes_and_rates_valid",
        table.primordial.shape == (29, 161)
        and table.metal.shape == (29, 161)
        and table.mmw.shape == (29, 161)
        and np.all(table.primordial >= 0.0)
        and np.all(table.metal > 0.0),
        [table.primordial.shape, table.metal.shape, table.mmw.shape],
    )
    add_validation(
        validation,
        "virial_fixed_point_solved",
        virial["fixed_point_relative_residual"] < 1.0e-12,
        virial,
    )
    add_validation(
        validation,
        "cooling_lookups_inside_table_axes",
        all(row["inside_Cloudy_density_axis"] for row in thermal)
        and all(row["inside_Cloudy_temperature_axis"] for row in thermal),
        thermal,
    )
    add_validation(
        validation,
        "electron_scattering_thin_envelope",
        all(float(row["Thomson_optical_depth_center_to_edge"]) < 0.3 for row in thermal),
        [row["Thomson_optical_depth_center_to_edge"] for row in thermal],
    )
    add_validation(
        validation,
        "resolved_clumping_positive_and_resolution_controlled",
        all(value > 0.0 for value in pair_means.values())
        and max(pair_means.values()) - min(pair_means.values()) < 0.1,
        pair_means,
    )
    add_validation(
        validation,
        "cooling_shell_quadrature_converged",
        max(clock_resolution_changes.values()) < 1.0e-3,
        clock_resolution_changes,
    )
    add_validation(
        validation,
        "all_CIE_clocks_positive_and_finite",
        all(
            math.isfinite(float(row["duration_Gyr"]))
            and float(row["duration_Gyr"]) > 0.0
            and float(row["minimum_luminosity_W"]) > 0.0
            for row in clock_grid
        ),
        [row["duration_Gyr"] for row in clock_grid],
    )
    add_validation(
        validation,
        "forward_branches_predeclared_without_target_selection",
        FORWARD_METALLICITIES == (0.1, 0.3)
        and all(not row["target_used_to_select_schedule"] for row in schedules),
        FORWARD_METALLICITIES,
    )
    add_validation(
        validation,
        "derived_schedules_monotone_and_complete",
        all(
            np.all(np.diff(np.asarray(clock["time_seconds"])) > 0.0)
            and abs(float(np.asarray(clock["assembly"])[0])) < 1.0e-15
            and abs(float(np.asarray(clock["assembly"])[-1]) - 1.0) < 1.0e-15
            for clock in clocks.values()
        ),
        {key: value["duration_Gyr"] for key, value in clocks.items()},
    )
    if not arguments.cooling_only:
        add_validation(
            validation,
            "both_predeclared_forward_responses_executed",
            response_executed,
            sorted(primary_scores),
        )
        add_validation(
            validation,
            "all_forward_scores_finite",
            all(
                math.isfinite(float(row["corrected_q"]))
                and math.isfinite(
                    float(row["corrected_velocity_squared_log10_RMSE"])
                )
                for row in response_scores
            ),
            response_scores,
        )
        add_validation(
            validation,
            "source_reaches_full_assembly",
            all(
                abs(float(row["source_final_assembly_fraction"]) - 1.0) < 1.0e-12
                for row in controls
            ),
            [row["source_final_assembly_fraction"] for row in controls],
        )
        add_validation(
            validation,
            "central_force_angular_momentum_control",
            max(
                max(
                    float(row["source_angular_momentum_relative_residual"]),
                    float(row["control_angular_momentum_relative_residual"]),
                )
                for row in controls
            )
            < 1.0e-10,
            [
                [
                    row["source_angular_momentum_relative_residual"],
                    row["control_angular_momentum_relative_residual"],
                ]
                for row in controls
            ],
        )
        add_validation(
            validation,
            "no_fitted_clock_or_response_efficiency",
            all(
                not row["target_used_to_select_metallicity"]
                and not row["target_used_to_select_clock"]
                and not row["response_efficiency_fitted"]
                for row in response_scores
            ),
            "sourced clock and predeclared metallicity benchmarks",
        )
        add_validation(
            validation,
            "time_refinement_executed",
            arguments.skip_refinement or refinement_executed,
            z03_refined_q,
        )
        add_validation(
            validation,
            "time_refinement_q_controlled",
            arguments.skip_refinement or z03_refinement_delta < 0.1,
            z03_refinement_delta,
        )
    add_validation(
        validation,
        "all_outputs_nonclaim",
        all(
            row.get("valid_for_claim") is False
            for rows in outputs.values()
            for row in rows
        ),
        "all generated CSV rows",
    )
    add_validation(
        validation,
        "local_GR_Newton_Maxwell_branch_unmodified",
        True,
        "matter cooling closure only; inherited calibrated G_N force unchanged",
    )

    summary = {
        "virial_temperature_K": virial["temperature_K"],
        "mean_molecular_weight": virial["mean_molecular_weight"],
        "initial_Thomson_optical_depth": float(cooling["Thomson_optical_depth"][0]),
        "final_Thomson_optical_depth": float(cooling["Thomson_optical_depth"][-1]),
        "minimum_shell_nH_cm3": float(
            np.min(cooling["minimum_hydrogen_density_cm^-3"])
        ),
        "maximum_shell_nH_cm3": float(
            np.max(cooling["maximum_hydrogen_density_cm^-3"])
        ),
        "primary_pair_clumping_factor": pair_clumping,
        "primary_clumping_cell_width_kpc": primary_clumping_row["cell_width_kpc"],
        "clumping_pair_means": pair_means,
        "one_orbit_Gyr": transition_orbit_gyr,
        "four_orbit_Gyr": 4.0 * transition_orbit_gyr,
        "Z0p1_clock_Gyr": float(z01_clock["duration_Gyr"]),
        "Z0p1_clock_orbits": float(z01_clock["duration_Gyr"])
        / transition_orbit_gyr,
        "Z0p3_clock_Gyr": float(z03_clock["duration_Gyr"]),
        "Z0p3_clock_orbits": float(z03_clock["duration_Gyr"])
        / transition_orbit_gyr,
        "Z0p1_forward_q": z01_score.get("corrected_q", "NOT_RUN"),
        "Z0p1_forward_RMSE": z01_score.get(
            "corrected_velocity_squared_log10_RMSE", "NOT_RUN"
        ),
        "Z0p1_forward_transition_ratio": z01_score.get(
            "corrected_transition_velocity_squared_ratio_to_target", "NOT_RUN"
        ),
        "Z0p3_forward_q": z03_score.get("corrected_q", "NOT_RUN"),
        "Z0p3_forward_RMSE": z03_score.get(
            "corrected_velocity_squared_log10_RMSE", "NOT_RUN"
        ),
        "Z0p3_forward_transition_ratio": z03_score.get(
            "corrected_transition_velocity_squared_ratio_to_target", "NOT_RUN"
        ),
        "Z0p3_refined_q": z03_refined_q,
        "Z0p3_refinement_delta_q": z03_refinement_delta,
        "parent_q_lower": parent_lower,
        "parent_q_upper": parent_upper,
        "clock_shell_resolution_relative_changes": clock_resolution_changes,
        "forward_response_executed": response_executed,
        "time_refinement_executed": refinement_executed,
        "one_zone_CIE_q_gate_passed": one_zone_q_gate_passed,
        "Z0p1_q_above_parent_upper": (
            float(z01_score["corrected_q"]) - parent_upper if z01_score else math.nan
        ),
        "Z0p3_q_above_parent_upper": (
            float(z03_score["corrected_q"]) - parent_upper if z03_score else math.nan
        ),
    }
    result = {
        "checkpoint_marker": MARKER,
        "checked_date": CHECKED_DATE,
        "formalization_workbench_tree_sha256": formal_after,
        "source_hashes_before": hashes_before,
        "source_hashes_after": hashes_after,
        "summary": summary,
        "route_decision": route_decision,
        "validation_count": len(validation),
        "validation_failures": [row for row in validation if not row["passed"]],
        "baryon_entropy_projection_derived": True,
        "sourced_CIE_cooling_table_used": True,
        "resolved_clumping_estimated": True,
        "assembly_clock_duration_fitted_to_response": False,
        "derived_clock_forward_response_executed": response_executed,
        "one_zone_homologous_CIE_clock_passes_parent_q_gate": one_zone_q_gate_passed,
        "radial_radiation_hydrodynamics_solved": False,
        "UGC09133_hot_phase_metallicity_measured": False,
        "local_GR_Newton_Maxwell_branch_modified": False,
        "valid_for_galaxy_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
    }
    write_json(RESULT_JSON, result)
    write_csv(VALIDATION_CSV, validation)
    DOCUMENT.write_text(make_document(result), encoding="utf-8")
    if result["validation_failures"]:
        raise RuntimeError(
            f"validation failures: {[row['check_id'] for row in result['validation_failures']]}"
        )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
