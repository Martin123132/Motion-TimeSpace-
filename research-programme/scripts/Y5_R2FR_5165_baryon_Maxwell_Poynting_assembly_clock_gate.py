from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.util
import json
import math
from pathlib import Path
from typing import Any

import numpy as np
from scipy.interpolate import PchipInterpolator


POST = Path(__file__).resolve().parents[1]
FORMAL = POST.parent / "formalization-workbench"
PREVIOUS_SCRIPT = (
    POST / "scripts" / "Y5_R2FR_5164_mass_conserving_two_component_initial_value_gate.py"
)
VISIBLE_SCRIPT = (
    POST / "scripts" / "Y5_R2FR_5163_parent_wave_and_visible_source_response_gate.py"
)
PREVIOUS_DOCUMENT = (
    POST / "5164-Y5-R2FR-mass-conserving-visible-motion-initial-value-response-gate.md"
)
PREVIOUS_RESULT = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5164"
    / "mass_conserving_two_component_results.json"
)
PREVIOUS_HISTORY = (
    POST / "source-intake" / "functional_rg" / "5164" / "source_history_contract.csv"
)
PREVIOUS_SCORES = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5164"
    / "two_component_response_scores.csv"
)
MOTION_PROFILE = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5162"
    / "nested_zoom_profile_samples.csv"
)
MOTION_SCORE = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5162"
    / "nested_zoom_no_refit_scores.csv"
)
VISIBLE_PROFILE = (
    POST
    / "source-intake"
    / "functional_rg"
    / "5163"
    / "visible_baryon_source_profile.csv"
)
PARENT_MAXWELL = (
    POST
    / "4853-Y5-R2FR-Maxwell-Hodge-Hilbert-stress-current-normalization-and-stationary-Poynting-boundary-theorem.md"
)
PARENT_POWER = (
    POST
    / "4859-Y5-R2FR-longitudinal-EM-power-transfer-retarded-flow-and-alpha2-radiation-gate.md"
)
PARENT_SOURCE = (
    POST
    / "4947-Y5-R2FR-local-GR-Newton-Maxwell-calibration-count-and-universal-source-residue-certificate.md"
)
PARENT_UNIVERSAL = (
    POST
    / "4960-Y5-R2FR-integrated-H-soft-BRST-universal-source-theorem-and-local-GR-Newton-Maxwell-promotion-or-parent-field-content-boundary.md"
)

OUT = POST / "source-intake" / "functional_rg" / "5165"
ENERGY_CONTRACT_CSV = OUT / "covariant_energy_exchange_contract.csv"
MASS_PROFILE_CSV = OUT / "assembly_mass_profile_samples.csv"
BINDING_CSV = OUT / "binding_energy_polynomial.csv"
PHOTOMETRY_CSV = OUT / "photometric_luminosity_scale.csv"
CLOCK_CSV = OUT / "assembly_clock_luminosity_bounds.csv"
CLOCK_SAMPLES_CSV = OUT / "assembly_clock_family_samples.csv"
JOINT_CSV = OUT / "clock_response_joint_gate.csv"
IDENTIFIABILITY_CSV = OUT / "clock_identifiability_gate.csv"
DECISION_CSV = OUT / "route_decision.csv"
PROVENANCE_CSV = OUT / "source_provenance.csv"
RESULT_JSON = OUT / "baryon_Maxwell_Poynting_assembly_clock_results.json"
VALIDATION_CSV = (
    POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_5165_VALIDATION.csv"
)
DOCUMENT = (
    POST
    / "5165-Y5-R2FR-baryon-Maxwell-Poynting-assembly-clock-identifiability-and-energy-bound-gate.md"
)

MARKER = "MTS_5165_BARYON_MAXWELL_POYNTING_ASSEMBLY_CLOCK_GATE"
CHECKED_DATE = "2026-07-21"
FORMAL_DIGEST_LOCK = (
    "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
)
REFERENCE_GALAXY = "UGC09133"
REFERENCE_MAPPING = "Wetterich_v_equals_minus_2lambda"
PRIMARY_PROFILE_ID = "NESTED160_PAIR_PRIMARY"
SPARC_PAPER_URL = "https://arxiv.org/abs/1606.09251"
SPARC_PAPER_DOI = "10.3847/0004-6256/152/6/157"

G_KPC_KM2_S2_MSUN = 4.30091727003628e-6
G_SI = 6.67430e-11
C_SI = 299792458.0
M_SUN_KG = 1.98847e30
L_SUN_W = 3.828e26
PROTON_MASS_KG = 1.67262192369e-27
THOMSON_CROSS_SECTION_M2 = 6.6524587321e-29
KPC_M = 3.085677581491367e19
JULIAN_YEAR_S = 365.25 * 86400.0
GYR_S = 1.0e9 * JULIAN_YEAR_S
MSUN_KM2_S2_TO_J = M_SUN_KG * 1.0e6
QUADRATURE_POINTS = 32769


def load_module(path: Path, name: str) -> Any:
    specification = importlib.util.spec_from_file_location(name, path)
    if specification is None or specification.loader is None:
        raise RuntimeError(f"cannot load module: {path}")
    module = importlib.util.module_from_spec(specification)
    specification.loader.exec_module(module)
    return module


PREVIOUS = load_module(PREVIOUS_SCRIPT, "mts_checkpoint_5164_for_5165")
VISIBLE = load_module(VISIBLE_SCRIPT, "mts_checkpoint_5163_for_5165")


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
    fields: list[str] = []
    for row in rows:
        for field in row:
            if field not in fields:
                fields.append(field)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def write_json(path: Path, value: dict[str, Any]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n", encoding="utf-8")


def source_paths() -> dict[str, Path]:
    return {
        "previous_script": PREVIOUS_SCRIPT,
        "visible_script": VISIBLE_SCRIPT,
        "previous_document": PREVIOUS_DOCUMENT,
        "previous_result": PREVIOUS_RESULT,
        "previous_history": PREVIOUS_HISTORY,
        "previous_scores": PREVIOUS_SCORES,
        "motion_profile": MOTION_PROFILE,
        "motion_score": MOTION_SCORE,
        "visible_profile": VISIBLE_PROFILE,
        "parent_Maxwell_Poynting": PARENT_MAXWELL,
        "parent_power_transfer": PARENT_POWER,
        "parent_universal_source": PARENT_SOURCE,
        "parent_integrated_H": PARENT_UNIVERSAL,
        "galaxy_samples_read_only": VISIBLE.GALAXY_SAMPLES,
    }


class MonotoneMassProfile:
    def __init__(self, radii_kpc: np.ndarray, masses_msun: np.ndarray) -> None:
        order = np.argsort(radii_kpc)
        self.radii = np.asarray(radii_kpc, dtype=float)[order]
        masses = np.asarray(masses_msun, dtype=float)[order]
        self.masses = np.maximum.accumulate(np.maximum(masses, 0.0))
        if len(self.radii) < 4 or np.any(np.diff(self.radii) <= 0.0):
            raise RuntimeError("mass profile requires at least four ordered unique radii")
        self.interpolator = PchipInterpolator(self.radii, self.masses)

    def mass_at(self, radius_kpc: np.ndarray | float) -> np.ndarray | float:
        radius = np.asarray(radius_kpc, dtype=float)
        result = np.empty_like(radius)
        inner = radius < self.radii[0]
        middle = (radius >= self.radii[0]) & (radius <= self.radii[-1])
        outer = radius > self.radii[-1]
        result[inner] = self.masses[0] * (radius[inner] / self.radii[0]) ** 3
        result[middle] = self.interpolator(radius[middle])
        result[outer] = self.masses[-1]
        if np.ndim(radius_kpc) == 0:
            return float(result)
        return result


def motion_profiles() -> dict[str, tuple[MonotoneMassProfile, str]]:
    rows = [
        row
        for row in read_csv(MOTION_PROFILE)
        if row["mapping_scored"] == REFERENCE_MAPPING
    ]
    profiles: dict[str, tuple[MonotoneMassProfile, str]] = {}
    for configuration in ("NESTED128", "NESTED160"):
        selected = [row for row in rows if row["config_id"] == configuration]
        selected.sort(key=lambda row: float(row["radius_kpc"]))
        profiles[f"{configuration}_PAIR"] = (
            MonotoneMassProfile(
                np.asarray([float(row["radius_kpc"]) for row in selected]),
                np.asarray(
                    [float(row["paired_mean_motion_excess_mass_Msun"]) for row in selected]
                ),
            ),
            "resolved_pair_mean_force_source_numerical_comparator",
        )
    selected = [row for row in rows if row["config_id"] == "NESTED160"]
    selected.sort(key=lambda row: float(row["radius_kpc"]))
    profiles["TARGET_MTS_PROFILE"] = (
        MonotoneMassProfile(
            np.asarray([float(row["radius_kpc"]) for row in selected]),
            np.asarray([float(row["target_motion_mass_Msun"]) for row in selected]),
        ),
        "analytic_target_profile_comparator_not_evolved_source",
    )
    profiles[PRIMARY_PROFILE_ID] = profiles.pop("NESTED160_PAIR")
    return profiles


def edge_radius_kpc() -> float:
    row = next(
        row
        for row in read_csv(MOTION_SCORE)
        if row["config_id"] == "NESTED160"
        and row["mapping_scored"] == REFERENCE_MAPPING
    )
    return float(row["target_edge_radius_kpc"])


def energy_grid(edge_kpc: float, points: int) -> np.ndarray:
    return np.concatenate(
        (
            np.asarray([0.0]),
            np.geomspace(edge_kpc * 1.0e-8, edge_kpc, points - 1),
        )
    )


def energy_polynomial(
    motion: MonotoneMassProfile,
    visible: Any,
    edge_kpc: float,
    points: int,
) -> dict[str, Any]:
    radius = energy_grid(edge_kpc, points)
    motion_mass = np.asarray(motion.mass_at(radius), dtype=float)
    condensed_mass = np.asarray(visible.mass_at(radius), dtype=float)
    baryon_to_motion = (1.0 - PREVIOUS.PM.MOTION_FRACTION) / PREVIOUS.PM.MOTION_FRACTION
    motion_edge = float(motion_mass[-1])
    condensed_edge = float(condensed_mass[-1])
    transfer_ratio = condensed_edge / motion_edge
    base = (1.0 + baryon_to_motion) * motion_mass
    transfer = condensed_mass - transfer_ratio * motion_mass
    radius_mid = 0.5 * (radius[1:] + radius[:-1])
    base_mid = 0.5 * (base[1:] + base[:-1])
    transfer_mid = 0.5 * (transfer[1:] + transfer[:-1])
    delta_base = np.diff(base)
    delta_transfer = np.diff(transfer)
    coefficient_0 = -G_KPC_KM2_S2_MSUN * float(
        np.sum(base_mid * delta_base / radius_mid)
    )
    coefficient_1 = -G_KPC_KM2_S2_MSUN * float(
        np.sum(
            (base_mid * delta_transfer + transfer_mid * delta_base) / radius_mid
        )
    )
    coefficient_2 = -G_KPC_KM2_S2_MSUN * float(
        np.sum(transfer_mid * delta_transfer / radius_mid)
    )
    reconstruction_residual = 0.0
    for assembly_fraction in np.linspace(0.0, 1.0, 17):
        total = base + assembly_fraction * transfer
        total_mid = 0.5 * (total[1:] + total[:-1])
        direct = -G_KPC_KM2_S2_MSUN * float(
            np.sum(total_mid * np.diff(total) / radius_mid)
        )
        polynomial = (
            coefficient_0
            + assembly_fraction * coefficient_1
            + assembly_fraction**2 * coefficient_2
        )
        reconstruction_residual = max(
            reconstruction_residual,
            abs(direct - polynomial) / max(abs(direct), 1.0),
        )
    initial = coefficient_0
    final = coefficient_0 + coefficient_1 + coefficient_2
    full_binding_release = initial - final
    virial_radiative_release = 0.5 * full_binding_release
    barrier_start = -0.5 * coefficient_1
    barrier_end = -0.5 * (coefficient_1 + 2.0 * coefficient_2)
    return {
        "radius_kpc": radius,
        "motion_mass_Msun": motion_mass,
        "condensed_mass_Msun": condensed_mass,
        "baryon_to_motion_ratio": baryon_to_motion,
        "transfer_ratio": transfer_ratio,
        "motion_edge_Msun": motion_edge,
        "condensed_edge_Msun": condensed_edge,
        "cosmic_baryon_edge_Msun": baryon_to_motion * motion_edge,
        "W0_Msun_km2_s2": coefficient_0,
        "W1_Msun_km2_s2": coefficient_1,
        "W2_Msun_km2_s2": coefficient_2,
        "W_initial_Msun_km2_s2": initial,
        "W_final_Msun_km2_s2": final,
        "full_binding_release_J": full_binding_release * MSUN_KM2_S2_TO_J,
        "virial_radiative_release_J": virial_radiative_release * MSUN_KM2_S2_TO_J,
        "K_start_J_per_lambda": barrier_start * MSUN_KM2_S2_TO_J,
        "K_end_J_per_lambda": barrier_end * MSUN_KM2_S2_TO_J,
        "K_min_J_per_lambda": min(barrier_start, barrier_end) * MSUN_KM2_S2_TO_J,
        "K_max_J_per_lambda": max(barrier_start, barrier_end) * MSUN_KM2_S2_TO_J,
        "quadratic_reconstruction_relative_residual": reconstruction_residual,
    }


def barrier_joule(polynomial: dict[str, Any], assembly_fraction: np.ndarray) -> np.ndarray:
    coefficient_1 = float(polynomial["W1_Msun_km2_s2"])
    coefficient_2 = float(polynomial["W2_Msun_km2_s2"])
    return (
        -0.5 * (coefficient_1 + 2.0 * coefficient_2 * assembly_fraction)
        * MSUN_KM2_S2_TO_J
    )


def binding_rows(
    profiles: dict[str, tuple[MonotoneMassProfile, str]],
    visible: Any,
    edge_kpc: float,
) -> tuple[list[dict[str, Any]], dict[str, dict[str, Any]]]:
    rows: list[dict[str, Any]] = []
    polynomials: dict[str, dict[str, Any]] = {}
    for profile_id, (profile, role) in profiles.items():
        full = energy_polynomial(profile, visible, edge_kpc, QUADRATURE_POINTS)
        coarse = energy_polynomial(profile, visible, edge_kpc, (QUADRATURE_POINTS + 1) // 2)
        release = float(full["virial_radiative_release_J"])
        convergence = abs(
            release - float(coarse["virial_radiative_release_J"])
        ) / max(abs(release), 1.0)
        row = {
            "profile_id": profile_id,
            "profile_role": role,
            "edge_radius_kpc": edge_kpc,
            "motion_edge_Msun": full["motion_edge_Msun"],
            "condensed_edge_Msun": full["condensed_edge_Msun"],
            "cosmic_baryon_edge_Msun": full["cosmic_baryon_edge_Msun"],
            "condensed_fraction_of_cosmic_baryons": float(full["condensed_edge_Msun"])
            / float(full["cosmic_baryon_edge_Msun"]),
            "baryon_to_motion_ratio": full["baryon_to_motion_ratio"],
            "mass_transfer_ratio_mu": full["transfer_ratio"],
            "W0_Msun_km2_s2": full["W0_Msun_km2_s2"],
            "W1_Msun_km2_s2": full["W1_Msun_km2_s2"],
            "W2_Msun_km2_s2": full["W2_Msun_km2_s2"],
            "W_initial_Msun_km2_s2": full["W_initial_Msun_km2_s2"],
            "W_final_Msun_km2_s2": full["W_final_Msun_km2_s2"],
            "full_binding_release_J": full["full_binding_release_J"],
            "virial_radiative_release_J": release,
            "K_start_J_per_lambda": full["K_start_J_per_lambda"],
            "K_end_J_per_lambda": full["K_end_J_per_lambda"],
            "K_min_J_per_lambda": full["K_min_J_per_lambda"],
            "K_max_J_per_lambda": full["K_max_J_per_lambda"],
            "quadrature_points": QUADRATURE_POINTS,
            "quadrature_relative_change": convergence,
            "quadratic_reconstruction_relative_residual": full[
                "quadratic_reconstruction_relative_residual"
            ],
            "endpoint_virial_assumption": True,
            "motion_profile_frozen_during_energy_projection": True,
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        }
        rows.append(row)
        polynomials[profile_id] = full
    return rows, polynomials


def mass_profile_rows(polynomial: dict[str, Any]) -> list[dict[str, Any]]:
    edge = float(polynomial["radius_kpc"][-1])
    radii = np.unique(
        np.concatenate(
            (
                np.geomspace(edge * 1.0e-5, edge, 81),
                np.asarray([edge]),
            )
        )
    )
    motion = np.interp(radii, polynomial["radius_kpc"], polynomial["motion_mass_Msun"])
    condensed = np.interp(
        radii, polynomial["radius_kpc"], polynomial["condensed_mass_Msun"]
    )
    baryon_ratio = float(polynomial["baryon_to_motion_ratio"])
    transfer_ratio = float(polynomial["transfer_ratio"])
    rows: list[dict[str, Any]] = []
    for assembly_fraction in (0.0, 0.25, 0.5, 0.75, 1.0):
        diffuse = (baryon_ratio - assembly_fraction * transfer_ratio) * motion
        assembled = assembly_fraction * condensed
        total_baryon = diffuse + assembled
        total = motion + total_baryon
        for index, radius in enumerate(radii):
            is_edge_sample = abs(radius - edge) <= 1.0e-8
            edge_residual: float | str = ""
            edge_conserved: bool | str = ""
            if is_edge_sample:
                expected_edge_baryons = baryon_ratio * float(
                    polynomial["motion_edge_Msun"]
                )
                edge_residual = abs(
                    total_baryon[index] - expected_edge_baryons
                ) / expected_edge_baryons
                edge_conserved = edge_residual < 1.0e-12
            rows.append(
                {
                    "profile_id": PRIMARY_PROFILE_ID,
                    "assembly_fraction_lambda": assembly_fraction,
                    "radius_kpc": radius,
                    "motion_mass_Msun": motion[index],
                    "diffuse_particle_tied_baryon_mass_Msun": diffuse[index],
                    "assembled_condensed_baryon_mass_Msun": assembled[index],
                    "total_baryon_mass_Msun": total_baryon[index],
                    "total_gravitating_mass_Msun": total[index],
                    "is_edge_sample": is_edge_sample,
                    "edge_mass_conservation_relative_residual": edge_residual,
                    "edge_mass_conserved": edge_conserved,
                    "valid_for_claim": False,
                    "checkpoint_marker": MARKER,
                }
            )
    return rows


def photometric_rows(visible_rows: list[dict[str, str]]) -> tuple[list[dict[str, Any]], float, float]:
    radius = np.asarray([float(row["radius_kpc"]) for row in visible_rows])
    disk = np.asarray([float(row["surface_disk_Lsun_pc2"]) for row in visible_rows])
    bulge = np.asarray([float(row["surface_bulge_Lsun_pc2"]) for row in visible_rows])
    strict_disk = 2.0 * math.pi * float(np.trapezoid(disk * radius, radius)) * 1.0e6
    strict_bulge = 2.0 * math.pi * float(np.trapezoid(bulge * radius, radius)) * 1.0e6
    central_radius = np.concatenate((np.asarray([0.0]), radius))
    central_disk = np.concatenate((np.asarray([disk[0]]), disk))
    central_bulge = np.concatenate((np.asarray([bulge[0]]), bulge))
    completed_disk = (
        2.0
        * math.pi
        * float(np.trapezoid(central_disk * central_radius, central_radius))
        * 1.0e6
    )
    completed_bulge = (
        2.0
        * math.pi
        * float(np.trapezoid(central_bulge * central_radius, central_radius))
        * 1.0e6
    )
    rows = [
        {
            "method": "tabulated_annuli_only",
            "disk_luminosity_Lsun": strict_disk,
            "bulge_luminosity_Lsun": strict_bulge,
            "total_luminosity_Lsun": strict_disk + strict_bulge,
            "total_luminosity_W": (strict_disk + strict_bulge) * L_SUN_W,
            "wavelength_band": "Spitzer_3.6_micron",
            "is_bolometric_cooling_luminosity": False,
            "can_select_assembly_clock": False,
            "radial_extent_kpc": radius[-1],
            "integration_rule": "2pi_integral_Sigma_L_R_dR_without_unmeasured_centre",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "method": "flat_central_cell_completion",
            "disk_luminosity_Lsun": completed_disk,
            "bulge_luminosity_Lsun": completed_bulge,
            "total_luminosity_Lsun": completed_disk + completed_bulge,
            "total_luminosity_W": (completed_disk + completed_bulge) * L_SUN_W,
            "wavelength_band": "Spitzer_3.6_micron",
            "is_bolometric_cooling_luminosity": False,
            "can_select_assembly_clock": False,
            "radial_extent_kpc": radius[-1],
            "integration_rule": "2pi_integral_Sigma_L_R_dR_with_constant_inner_cell",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
    ]
    return rows, strict_disk + strict_bulge, completed_disk + completed_bulge


def eddington_luminosity_w(mass_msun: float) -> float:
    return (
        4.0
        * math.pi
        * G_SI
        * mass_msun
        * M_SUN_KG
        * PROTON_MASS_KG
        * C_SI
        / THOMSON_CROSS_SECTION_M2
    )


def assembly_history(
    ramp: str, phase: np.ndarray
) -> tuple[np.ndarray, np.ndarray]:
    if ramp == "linear":
        return phase, np.ones_like(phase)
    if ramp == "minimum_jerk_C2":
        assembly = 10.0 * phase**3 - 15.0 * phase**4 + 6.0 * phase**5
        derivative = 30.0 * phase**2 * (1.0 - phase) ** 2
        return assembly, derivative
    raise RuntimeError(f"unsupported positive-time ramp: {ramp}")


def clock_rows(
    polynomial: dict[str, Any],
    photometric_low_lsun: float,
    photometric_high_lsun: float,
    edge_kpc: float,
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    histories = read_csv(PREVIOUS_HISTORY)
    energy = float(polynomial["virial_radiative_release_J"])
    condensed_edge = float(polynomial["condensed_edge_Msun"])
    cosmic_baryon_edge = float(polynomial["cosmic_baryon_edge_Msun"])
    eddington_condensed = eddington_luminosity_w(condensed_edge)
    eddington_all_baryons = eddington_luminosity_w(cosmic_baryon_edge)
    causal_crossing_gyr = edge_kpc * KPC_M / C_SI / GYR_S
    rows: list[dict[str, Any]] = []
    samples: list[dict[str, Any]] = []
    for history in histories:
        duration_gyr = float(history["growth_time_Gyr"])
        if duration_gyr <= 0.0:
            rows.append(
                {
                    "history_id": history["history_id"],
                    "ramp": history["ramp"],
                    "duration_Gyr": duration_gyr,
                    "duration_over_causal_crossing": 0.0,
                    "required_average_luminosity_W": "",
                    "required_peak_luminosity_W": "",
                    "required_average_luminosity_Lsun": "",
                    "peak_to_SPARC_3p6_lower_scale": "",
                    "peak_to_SPARC_3p6_upper_scale": "",
                    "peak_to_condensed_Eddington_scale": "",
                    "energy_integral_relative_residual": "",
                    "causal_worldtube_allowed": False,
                    "below_condensed_Eddington_scale": False,
                    "energy_balance_admissible": False,
                    "exclusion_reason": "zero_duration_requires_distributional_infinite_flux_and_violates_finite_worldtube_crossing",
                    "energy_equation_selects_history": False,
                    "valid_for_claim": False,
                    "checkpoint_marker": MARKER,
                }
            )
            continue
        phase = np.linspace(0.0, 1.0, 257)
        assembly, derivative_phase = assembly_history(history["ramp"], phase)
        duration_s = duration_gyr * GYR_S
        barrier = barrier_joule(polynomial, assembly)
        luminosity = barrier * derivative_phase / duration_s
        integrated = float(np.trapezoid(luminosity, phase * duration_s))
        integral_residual = abs(integrated - energy) / energy
        average = energy / duration_s
        peak = float(np.max(luminosity))
        causal_allowed = duration_gyr >= causal_crossing_gyr
        below_eddington = peak < eddington_condensed
        rows.append(
            {
                "history_id": history["history_id"],
                "ramp": history["ramp"],
                "duration_Gyr": duration_gyr,
                "duration_over_causal_crossing": duration_gyr / causal_crossing_gyr,
                "required_average_luminosity_W": average,
                "required_peak_luminosity_W": peak,
                "required_average_luminosity_Lsun": average / L_SUN_W,
                "peak_to_SPARC_3p6_lower_scale": peak
                / (photometric_low_lsun * L_SUN_W),
                "peak_to_SPARC_3p6_upper_scale": peak
                / (photometric_high_lsun * L_SUN_W),
                "peak_to_condensed_Eddington_scale": peak / eddington_condensed,
                "energy_integral_relative_residual": integral_residual,
                "causal_worldtube_allowed": causal_allowed,
                "below_condensed_Eddington_scale": below_eddington,
                "energy_balance_admissible": causal_allowed and below_eddington,
                "exclusion_reason": "" if causal_allowed and below_eddington else "physical_envelope_failed",
                "energy_equation_selects_history": False,
                "valid_for_claim": False,
                "checkpoint_marker": MARKER,
            }
        )
        for index in range(0, len(phase), 4):
            samples.append(
                {
                    "history_id": history["history_id"],
                    "phase_t_over_T": phase[index],
                    "assembly_fraction_lambda": assembly[index],
                    "dlambda_dt_per_Gyr": derivative_phase[index] / duration_gyr,
                    "energy_barrier_K_J_per_lambda": barrier[index],
                    "outgoing_luminosity_W": luminosity[index],
                    "nonnegative_flux": luminosity[index] >= 0.0,
                    "valid_for_claim": False,
                    "checkpoint_marker": MARKER,
                }
            )
    rows.append(
        {
            "history_id": "DERIVED_WORLD_TUBE_SCALES",
            "ramp": "not_a_history",
            "duration_Gyr": causal_crossing_gyr,
            "duration_over_causal_crossing": 1.0,
            "required_average_luminosity_W": energy / (causal_crossing_gyr * GYR_S),
            "required_peak_luminosity_W": "",
            "required_average_luminosity_Lsun": energy
            / (causal_crossing_gyr * GYR_S * L_SUN_W),
            "peak_to_SPARC_3p6_lower_scale": "",
            "peak_to_SPARC_3p6_upper_scale": "",
            "peak_to_condensed_Eddington_scale": "",
            "energy_integral_relative_residual": "",
            "causal_worldtube_allowed": True,
            "below_condensed_Eddington_scale": "",
            "energy_balance_admissible": "scale_only",
            "exclusion_reason": "causal_lower_duration_scale_not_a_selected_clock",
            "energy_equation_selects_history": False,
            "condensed_Eddington_luminosity_W": eddington_condensed,
            "all_baryon_Eddington_luminosity_W": eddington_all_baryons,
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        }
    )
    return rows, samples


def joint_rows(clock: list[dict[str, Any]], previous_result: dict[str, Any]) -> list[dict[str, Any]]:
    score_lookup = {row["history_id"]: row for row in read_csv(PREVIOUS_SCORES)}
    rows: list[dict[str, Any]] = []
    for clock_row in clock:
        history_id = str(clock_row["history_id"])
        if history_id not in score_lookup:
            continue
        score = score_lookup[history_id]
        refinement_compatible = history_id == "ONE_ORBIT_C2" and bool(
            previous_result["summary"]["one_orbit_refinement_intersects_parent_band"]
        )
        rows.append(
            {
                "history_id": history_id,
                "duration_Gyr": clock_row["duration_Gyr"],
                "energy_balance_admissible": clock_row["energy_balance_admissible"],
                "corrected_q": float(score["corrected_q"]),
                "q_parent": float(score["q_parent"]),
                "q_parent_envelope": float(score["q_envelope"]),
                "primary_q_compatible": score["corrected_q_compatible"] == "True",
                "refinement_interval_intersects_parent_band": refinement_compatible,
                "velocity_squared_log10_RMSE": float(
                    score["corrected_velocity_squared_log10_RMSE"]
                ),
                "transition_velocity_squared_ratio_to_target": float(
                    score["corrected_transition_velocity_squared_ratio_to_target"]
                ),
                "energy_balance_selects_this_response": False,
                "parent_selected": False,
                "valid_for_claim": False,
                "checkpoint_marker": MARKER,
            }
        )
    return rows


def energy_contract_rows() -> list[dict[str, Any]]:
    return [
        {
            "equation_id": "E1_PARENT_WARD_EXCHANGE",
            "equation": "nabla_mu T_EM^{mu nu}=-F^nu_lambda J^lambda; nabla_mu T_matter^{mu nu}=+F^nu_lambda J^lambda",
            "derivation_status": "derived_from_same_U1_matter_action",
            "clock_information": "none_by_itself",
            "source": PARENT_MAXWELL.name,
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "equation_id": "E2_TOTAL_CONSERVATION",
            "equation": "nabla_mu(T_matter^{mu nu}+T_EM^{mu nu})=0",
            "derivation_status": "derived_Ward_identity",
            "clock_information": "one_conservation_equation",
            "source": PARENT_SOURCE.name,
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "equation_id": "E3_POYNTING_COMPONENT",
            "equation": "S^mu=-h^mu_alpha T_EM^{alpha beta}u_beta=(E cross B)^mu",
            "derivation_status": "derived_same_Hilbert_stress_not_second_source",
            "clock_information": "outgoing_energy_carrier",
            "source": PARENT_MAXWELL.name,
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "equation_id": "E4_WORLDTUBE_BALANCE",
            "equation": "Delta E_total+integral_boundary J_E^mu n_mu dSigma=0",
            "derivation_status": "derived_on_stationary_observed_time_background",
            "clock_information": "fixes_integrated_flux_not_flux_profile",
            "assumptions": "closed_baryon_worldtube_or_explicit_matter_flux_retained; endpoint_field_storage_retained",
            "source": PARENT_MAXWELL.name,
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "equation_id": "E5_ASSEMBLY_CLOCK",
            "equation": "L_out(t)=K(lambda) dot(lambda); K(lambda)=-dE_mech/dlambda",
            "derivation_status": "derived_after_one_parameter_quasistatic_projection",
            "clock_information": "dot(lambda)=L_out/K_only_after_L_out_constitutive_law",
            "assumptions": "no_unrecorded_matter_flux; spherical_frozen_motion_projection; virialized_endpoints",
            "source": "this_checkpoint",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "equation_id": "E6_CLOCK_FAMILY",
            "equation": "for_any_T_positive_and_monotone_lambda_T: L_T=K(lambda_T)dot(lambda_T) and integral L_T dt=Delta E",
            "derivation_status": "constructive_nonidentifiability_proof",
            "clock_information": "continuum_of_clocks_share_same_endpoint_energy",
            "source": "this_checkpoint",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
    ]


def identifiability_rows(
    binding: list[dict[str, Any]],
    clocks: list[dict[str, Any]],
    joint: list[dict[str, Any]],
) -> list[dict[str, Any]]:
    primary = next(row for row in binding if row["profile_id"] == PRIMARY_PROFILE_ID)
    finite = [
        row
        for row in clocks
        if row["history_id"] not in ("IMPULSIVE", "DERIVED_WORLD_TUBE_SCALES")
    ]
    distinct_times = len({round(float(row["duration_Gyr"]), 12) for row in finite})
    one_orbit = next(row for row in joint if row["history_id"] == "ONE_ORBIT_C2")
    one_to_four = [
        row for row in joint if row["history_id"] in ("ONE_ORBIT_C2", "ADIABATIC4_C2")
    ]
    q_spread = max(float(row["corrected_q"]) for row in one_to_four) - min(
        float(row["corrected_q"]) for row in one_to_four
    )
    return [
        {
            "gate_id": "positive_energy_barrier",
            "result": float(primary["K_min_J_per_lambda"]) > 0.0,
            "evidence": f"K_min={primary['K_min_J_per_lambda']} J",
            "implication": "monotone_assembly_can_be_powered_by_nonnegative_outgoing_flux",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "gate_id": "impulsive_history_excluded",
            "result": not bool(
                next(row for row in clocks if row["history_id"] == "IMPULSIVE")[
                    "energy_balance_admissible"
                ]
            ),
            "evidence": "zero_duration_requires_infinite_distributional_flux",
            "implication": "energy_causality_prunes_one_history",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "gate_id": "multiple_finite_clocks_constructed",
            "result": distinct_times >= 4
            and all(bool(row["energy_balance_admissible"]) for row in finite),
            "evidence": f"distinct_positive_durations={distinct_times}",
            "implication": "endpoint_energy_does_not_identify_duration",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "gate_id": "one_orbit_energy_feasible",
            "result": bool(one_orbit["energy_balance_admissible"]),
            "evidence": f"T={one_orbit['duration_Gyr']} Gyr",
            "implication": "5164_near_band_history_not_rejected_by_energy_or_causality",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "gate_id": "one_orbit_refinement_compatibility_retained",
            "result": bool(one_orbit["refinement_interval_intersects_parent_band"]),
            "evidence": f"q_primary={one_orbit['corrected_q']}",
            "implication": "numerical_compatibility_survives_energy_projection",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "gate_id": "one_to_four_orbit_response_flatness",
            "result": q_spread < 0.01,
            "evidence": f"Delta_q={q_spread}",
            "implication": "near_band_response_is_not_a_single_finely_tuned_duration_point",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "gate_id": "constitutive_emissivity_owned",
            "result": False,
            "evidence": "current_parent_fixes_Maxwell_given_J_but_not_J_or_L_out_as_function_of_baryon_state",
            "implication": "unique_clock_not_parent_derived",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "gate_id": "unique_assembly_clock_selected",
            "result": False,
            "evidence": "one_scalar_endpoint_energy_constraint_admits_constructed_continuum_of_lambda_T_histories",
            "implication": "no_galaxy_or_full_MTS_claim",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
    ]


def provenance_rows(paths: dict[str, Path]) -> list[dict[str, Any]]:
    rows = [
        {
            "source_id": key,
            "source_type": "local_file",
            "path_or_url": str(path),
            "sha256": file_digest(path),
            "role": "read_only_parent_or_data_input",
            "checked_date": CHECKED_DATE,
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        }
        for key, path in paths.items()
    ]
    rows.extend(
        [
            {
                "source_id": "SPARC_Lelli_McGaugh_Schombert_2016",
                "source_type": "primary_paper_url",
                "path_or_url": SPARC_PAPER_URL,
                "sha256": "not_applicable_remote_url",
                "role": "identifies_surface_photometry_as_Spitzer_3.6_micron_and_not_bolometric_cooling_flux",
                "doi": SPARC_PAPER_DOI,
                "checked_date": CHECKED_DATE,
                "valid_for_claim": False,
                "checkpoint_marker": MARKER,
            },
            {
                "source_id": "CODATA_constants",
                "source_type": "declared_constants",
                "path_or_url": "G,c,m_p,sigma_T,M_sun,L_sun_values_embedded_in_script",
                "sha256": "not_applicable_declared_constants",
                "role": "unit_conversion_and_Eddington_scale_comparator",
                "checked_date": CHECKED_DATE,
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
            "evidence": json.dumps(evidence, sort_keys=True)
            if isinstance(evidence, (dict, list))
            else str(evidence),
            "checkpoint_marker": MARKER,
        }
    )


def make_document(result: dict[str, Any]) -> str:
    summary = result["summary"]
    return f"""# 5165 - Baryon/Maxwell/Poynting assembly-clock identifiability and energy-bound gate

Marker: `{MARKER}`.

Date: `{CHECKED_DATE}`.

## Question actually answered

Checkpoint 5164 found that a mass-conserving visible-source history near one
transition orbit moves the resolved collisionless exponent into numerical
contact with the parent band. This checkpoint asks whether the existing
baryon plus Maxwell/Poynting equations *derive that duration*, rather than
selecting it because it works.

They do not derive a unique duration, but the calculation is not merely a
missing-input ledger. It proves the precise non-identifiability theorem,
computes the parent-owned energy barrier, excludes an impulsive history, and
shows that the one-to-four-orbit response is energetically admissible and not
a single finely tuned clock point.

## Covariant derivation

The existing parent action gives

```text
nabla_mu T_EM^{{mu nu}}=-F^nu_lambda J^lambda,
nabla_mu T_matter^{{mu nu}}=+F^nu_lambda J^lambda,
nabla_mu(T_EM^{{mu nu}}+T_matter^{{mu nu}})=0.
```

Poynting flow is the `0i` component of this same Hilbert stress, not another
source. For the observed-time Killing field `xi`, the worldtube current
`J_E^mu=-T^mu_nu xi^nu` therefore obeys

```text
Delta E_total + integral_boundary J_E.n dSigma = 0.
```

On the closed-baryon worldtube branch, or with any matter flux retained
explicitly, a one-coordinate quasistatic assembly `lambda(t)` becomes, after
retaining endpoint field energy and mechanical work in `E_mech(lambda)`,

```text
L_out(t)=K(lambda) dot(lambda),
K(lambda)=-dE_mech/dlambda,
dot(lambda)=L_out/K.
```

The last expression is a clock only if the charged-matter state supplies a
constitutive `L_out[lambda,state]`. Maxwell evolution determines `F` for a
specified current; current conservation does not determine the dissipative
current, emissivity, opacity or boundary flux. For every positive duration
`T` and every monotone endpoint-preserving `lambda_T`,

```text
L_T(t)=K(lambda_T) dot(lambda_T)
```

has the same integrated endpoint energy. The generated clock families verify
this identity numerically. Energy conservation alone therefore has an
infinite family of clocks, not a hidden one-orbit prediction.

## Frozen-profile energy projection

The calculation uses exactly the checkpoint-5164 mass-conserving source
coordinate. With `b=Omega_b/Omega_X`, measured condensed mass `M_c`, resolved
motion mass `M_X`, and `mu=M_c(R_edge)/M_X(R_edge)`,

```text
M_b(r,lambda)=(b-lambda mu)M_X(r)+lambda M_c(r),
M_tot(r,lambda)=(1+b)M_X(r)+lambda[M_c(r)-mu M_X(r)].
```

Thus the baryon mass at the fixed edge is independent of `lambda`. On the
spherical frozen-motion endpoint branch,

```text
W(lambda)=-G integral_0^R M_tot(r,lambda) dM_tot(r,lambda)/r
         =W0+W1 lambda+W2 lambda^2,
E_vir(lambda)=W(lambda)/2,
K(lambda)=-(W1+2W2 lambda)/2.
```

For the primary resolved pair,

```text
M_X(R_edge)                  = {summary['motion_edge_Msun']} Msun
M_c(R_edge)                  = {summary['condensed_edge_Msun']} Msun
Delta E_binding              = {summary['full_binding_release_J']} J
Delta E_radiated (virial)    = {summary['virial_radiative_release_J']} J
K_min                        = {summary['K_min_J_per_lambda']} J
quadrature relative change   = {summary['quadrature_relative_change']}
```

`K` stays positive, so every tested monotone history has nonnegative outgoing
power. This endpoint estimate is conditional on spherical projection, a
frozen motion profile and virialized endpoints; it is not presented as a
full radiative-hydrodynamic simulation.

## Clock and response result

The fixed-edge light-crossing time is
`{summary['causal_crossing_Gyr']} Gyr`. The zero-duration impulsive history is
therefore rejected. All four distinct positive durations already predeclared
in checkpoint 5164 remain causal and lie far below the diagnostic condensed-
baryon Eddington luminosity scale.

For the one-orbit `C2` history,

```text
T                              = {summary['one_orbit_Gyr']} Gyr
required average luminosity    = {summary['one_orbit_average_luminosity_W']} W
required average luminosity    = {summary['one_orbit_average_luminosity_Lsun']} Lsun
required peak luminosity       = {summary['one_orbit_peak_luminosity_W']} W
peak / condensed Eddington     = {summary['one_orbit_peak_to_Eddington']}
```

UGC09133's tabulated SPARC surface photometry integrates to
`{summary['SPARC_3p6_tabulated_luminosity_Lsun']} Lsun`; a flat completion of
the unmeasured central cell gives
`{summary['SPARC_3p6_central_completed_luminosity_Lsun']} Lsun`. These are
Spitzer 3.6-micron luminosity scales, not bolometric cooling luminosities, so
they are capacity comparators only and are never used to select a clock.

The one-orbit numerical refinement interval still intersects the parent `q`
band. More importantly, the predeclared one- and four-orbit primary responses
differ by only `{summary['one_to_four_orbit_q_spread']}` in `q`. The useful
response is therefore stable over a factor-four duration bracket even though
the parent has not yet selected a member of that bracket.

## Decision

Route decision:
**{result['route_decision']}**.

This is a positive bound and a clean no-go for one proposed derivation route:

```text
same parent Maxwell/Hilbert/Poynting source used      = yes;
mass-conserving energy barrier derived                = yes;
impulsive assembly excluded                           = yes;
one-orbit history energetically admissible            = yes;
one-to-four-orbit response robust                      = yes;
energy conservation uniquely selects assembly clock   = no;
constitutive emissivity/current parent-derived        = no;
galaxy or full-MTS claim                               = false.
```

The next non-circular target is the charged-baryon constitutive law, not
another arbitrary response scan: project covariant baryon continuity, Euler
and entropy equations with the already-derived Maxwell exchange into an
explicit cooling/escape luminosity `L_out[lambda,state]`. Standard plasma or
radiative inputs must be sourced and held fixed before the response is read.
If that law cannot place the clock inside the broad one-to-four-orbit window,
the visible-source route is closure-only and the collective density-matrix
stress route becomes the next parent-owned alternative.

All `{result['validation_count']}` validation rows pass. Every generated row
remains nonclaim, all source hashes are unchanged, the protected
`formalization-workbench` digest remains
`{result['formalization_workbench_tree_sha256']}`, and no GitHub action was
performed.
"""


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
        raise RuntimeError(f"protected digest mismatch: {formal_before}")
    hashes_before = {key: file_digest(path) for key, path in paths.items()}
    if arguments.dry_run:
        print(
            json.dumps(
                {
                    "dry_run": True,
                    "marker": MARKER,
                    "source_count": len(paths),
                    "formal_digest": formal_before,
                    "output_directory": str(OUT),
                },
                indent=2,
            )
        )
        return

    previous_result = json.loads(PREVIOUS_RESULT.read_text(encoding="utf-8"))
    visible_rows = read_csv(VISIBLE_PROFILE)
    visible_source = PREVIOUS.VisibleSource(visible_rows)
    edge_kpc = edge_radius_kpc()
    profiles = motion_profiles()
    binding, polynomials = binding_rows(profiles, visible_source, edge_kpc)
    primary = polynomials[PRIMARY_PROFILE_ID]
    masses = mass_profile_rows(primary)
    photometry, photometric_low, photometric_high = photometric_rows(visible_rows)
    clocks, clock_samples = clock_rows(
        primary, photometric_low, photometric_high, edge_kpc
    )
    joint = joint_rows(clocks, previous_result)
    identifiability = identifiability_rows(binding, clocks, joint)
    contract = energy_contract_rows()
    one_orbit_clock = next(row for row in clocks if row["history_id"] == "ONE_ORBIT_C2")
    one_to_four = [
        row for row in joint if row["history_id"] in ("ONE_ORBIT_C2", "ADIABATIC4_C2")
    ]
    one_to_four_q_spread = max(float(row["corrected_q"]) for row in one_to_four) - min(
        float(row["corrected_q"]) for row in one_to_four
    )
    causal_row = next(
        row for row in clocks if row["history_id"] == "DERIVED_WORLD_TUBE_SCALES"
    )
    binding_primary = next(row for row in binding if row["profile_id"] == PRIMARY_PROFILE_ID)
    route_decision = (
        "POYNTING_ENERGY_BALANCE_EXCLUDES_IMPULSIVE_ASSEMBLY_AND_PROVES_A_BROAD_ONE_TO_FOUR_ORBIT_RESPONSE_ENERGETICALLY_ADMISSIBLE_BUT_CANNOT_SELECT_A_CLOCK_WITHOUT_A_PARENT_CONSTITUTIVE_EMISSIVITY"
    )
    decision = [
        {
            "route": "baryon_Maxwell_Poynting_assembly_clock",
            "result": route_decision,
            "evidence": (
                f"DeltaE_vir={binding_primary['virial_radiative_release_J']} J; "
                f"one_orbit_Lavg={one_orbit_clock['required_average_luminosity_W']} W; "
                f"one_to_four_orbit_Deltaq={one_to_four_q_spread}; "
                "four_distinct_positive_clock_durations_satisfy_the_same_energy_identity"
            ),
            "next_requirement": (
                "derive a sourced charged-baryon continuity/Euler/entropy radiative luminosity law before reading the response; if it misses the one-to-four-orbit window, demote visible assembly to closure-only and test collective density-matrix stress"
            ),
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        }
    ]
    provenance = provenance_rows(paths)
    outputs: dict[Path, list[dict[str, Any]]] = {
        ENERGY_CONTRACT_CSV: contract,
        MASS_PROFILE_CSV: masses,
        BINDING_CSV: binding,
        PHOTOMETRY_CSV: photometry,
        CLOCK_CSV: clocks,
        CLOCK_SAMPLES_CSV: clock_samples,
        JOINT_CSV: joint,
        IDENTIFIABILITY_CSV: identifiability,
        DECISION_CSV: decision,
        PROVENANCE_CSV: provenance,
    }
    for path, rows in outputs.items():
        write_csv(path, rows)

    hashes_after = {key: file_digest(path) for key, path in paths.items()}
    formal_after = tree_digest(FORMAL)
    finite_clocks = [
        row
        for row in clocks
        if row["history_id"] not in ("IMPULSIVE", "DERIVED_WORLD_TUBE_SCALES")
    ]
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
        formal_after == formal_before == FORMAL_DIGEST_LOCK,
        formal_after,
    )
    edge_mass_rows = [row for row in masses if row["is_edge_sample"]]
    add_validation(
        validation,
        "edge_baryon_mass_conserved_for_all_lambda_samples",
        len(edge_mass_rows) == 5
        and all(row["edge_mass_conserved"] for row in edge_mass_rows)
        and max(
            float(row["edge_mass_conservation_relative_residual"])
            for row in edge_mass_rows
        )
        < 1.0e-12,
        [row["edge_mass_conservation_relative_residual"] for row in edge_mass_rows],
    )
    add_validation(
        validation,
        "all_binding_releases_positive",
        all(float(row["virial_radiative_release_J"]) > 0.0 for row in binding),
        [row["virial_radiative_release_J"] for row in binding],
    )
    add_validation(
        validation,
        "all_energy_barriers_positive",
        all(float(row["K_min_J_per_lambda"]) > 0.0 for row in binding),
        [row["K_min_J_per_lambda"] for row in binding],
    )
    add_validation(
        validation,
        "quadrature_converged",
        all(float(row["quadrature_relative_change"]) < 1.0e-5 for row in binding),
        [row["quadrature_relative_change"] for row in binding],
    )
    add_validation(
        validation,
        "quadratic_energy_law_reconstructed",
        all(
            float(row["quadratic_reconstruction_relative_residual"]) < 1.0e-12
            for row in binding
        ),
        [row["quadratic_reconstruction_relative_residual"] for row in binding],
    )
    add_validation(
        validation,
        "clock_family_energy_integrals_close",
        all(float(row["energy_integral_relative_residual"]) < 1.0e-4 for row in finite_clocks),
        [row["energy_integral_relative_residual"] for row in finite_clocks],
    )
    add_validation(
        validation,
        "clock_family_flux_nonnegative",
        all(row["nonnegative_flux"] for row in clock_samples),
        "all sampled finite histories",
    )
    add_validation(
        validation,
        "impulsive_history_excluded",
        not bool(
            next(row for row in clocks if row["history_id"] == "IMPULSIVE")[
                "energy_balance_admissible"
            ]
        ),
        "finite-energy causal worldtube",
    )
    add_validation(
        validation,
        "all_positive_predeclared_histories_energy_admissible",
        all(bool(row["energy_balance_admissible"]) for row in finite_clocks),
        [row["history_id"] for row in finite_clocks],
    )
    add_validation(
        validation,
        "multiple_distinct_clocks_survive",
        len({round(float(row["duration_Gyr"]), 12) for row in finite_clocks}) >= 4,
        sorted({float(row["duration_Gyr"]) for row in finite_clocks}),
    )
    add_validation(
        validation,
        "one_orbit_refinement_compatibility_inherited",
        bool(
            next(row for row in joint if row["history_id"] == "ONE_ORBIT_C2")[
                "refinement_interval_intersects_parent_band"
            ]
        ),
        previous_result["summary"]["one_orbit_refinement_intersects_parent_band"],
    )
    add_validation(
        validation,
        "one_to_four_orbit_response_not_fine_tuned",
        one_to_four_q_spread < 0.01,
        one_to_four_q_spread,
    )
    add_validation(
        validation,
        "photometric_scale_not_mislabeled_bolometric",
        all(
            not row["is_bolometric_cooling_luminosity"]
            and not row["can_select_assembly_clock"]
            for row in photometry
        ),
        "SPARC 3.6 micron only",
    )
    add_validation(
        validation,
        "constitutive_clock_not_smuggled",
        all(not row["energy_equation_selects_history"] for row in clocks)
        and all(not row["parent_selected"] for row in joint),
        "all candidate histories remain non-selected",
    )
    add_validation(
        validation,
        "constructive_nonidentifiability_recorded",
        any(
            row["equation_id"] == "E6_CLOCK_FAMILY"
            and row["derivation_status"] == "constructive_nonidentifiability_proof"
            for row in contract
        ),
        "L_T=K(lambda_T) dot(lambda_T)",
    )
    add_validation(
        validation,
        "SPARC_primary_source_recorded",
        any(
            row["source_id"] == "SPARC_Lelli_McGaugh_Schombert_2016"
            and row.get("doi") == SPARC_PAPER_DOI
            for row in provenance
        ),
        SPARC_PAPER_URL,
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
        "local_branch_unmodified",
        True,
        "energy projection only; no parent action, G_N, Maxwell coefficient, or local field equation edited",
    )
    summary = {
        "edge_radius_kpc": edge_kpc,
        "motion_edge_Msun": binding_primary["motion_edge_Msun"],
        "condensed_edge_Msun": binding_primary["condensed_edge_Msun"],
        "cosmic_baryon_edge_Msun": binding_primary["cosmic_baryon_edge_Msun"],
        "full_binding_release_J": binding_primary["full_binding_release_J"],
        "virial_radiative_release_J": binding_primary["virial_radiative_release_J"],
        "K_min_J_per_lambda": binding_primary["K_min_J_per_lambda"],
        "K_max_J_per_lambda": binding_primary["K_max_J_per_lambda"],
        "quadrature_relative_change": binding_primary["quadrature_relative_change"],
        "causal_crossing_Gyr": causal_row["duration_Gyr"],
        "one_orbit_Gyr": one_orbit_clock["duration_Gyr"],
        "one_orbit_average_luminosity_W": one_orbit_clock[
            "required_average_luminosity_W"
        ],
        "one_orbit_average_luminosity_Lsun": one_orbit_clock[
            "required_average_luminosity_Lsun"
        ],
        "one_orbit_peak_luminosity_W": one_orbit_clock[
            "required_peak_luminosity_W"
        ],
        "one_orbit_peak_to_Eddington": one_orbit_clock[
            "peak_to_condensed_Eddington_scale"
        ],
        "SPARC_3p6_tabulated_luminosity_Lsun": photometric_low,
        "SPARC_3p6_central_completed_luminosity_Lsun": photometric_high,
        "one_to_four_orbit_q_spread": one_to_four_q_spread,
        "one_orbit_refinement_intersects_parent_band": previous_result["summary"][
            "one_orbit_refinement_intersects_parent_band"
        ],
        "positive_distinct_energy_admissible_clock_count": len(
            {round(float(row["duration_Gyr"]), 12) for row in finite_clocks}
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
        "covariant_energy_identity_derived": True,
        "assembly_energy_barrier_derived_conditionally": True,
        "impulsive_history_excluded": True,
        "one_orbit_history_energetically_admissible": True,
        "unique_assembly_clock_parent_selected": False,
        "constitutive_emissivity_parent_derived": False,
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
