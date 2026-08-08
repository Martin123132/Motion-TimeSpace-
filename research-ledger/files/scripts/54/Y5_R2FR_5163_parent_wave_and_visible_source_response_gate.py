from __future__ import annotations

import argparse
import csv
import hashlib
import json
import math
import re
from pathlib import Path
from typing import Any

import numpy as np
from scipy.interpolate import PchipInterpolator
from scipy.optimize import brentq


POST = Path(__file__).resolve().parents[1]
FORMAL = POST.parent / "formalization-workbench"
GALAXY_SAMPLES = Path(r"D:\Users\ollet\Documents\mts-galaxy-lab\data\samples.js")
PREVIOUS_DOCUMENT = POST / "5162-Y5-R2FR-shared-mode-nested-transition-zoom-and-resolved-q-gate.md"
PREVIOUS_RESULT = POST / "source-intake" / "functional_rg" / "5162" / "nested_transition_zoom_results.json"
PREVIOUS_Q = POST / "source-intake" / "functional_rg" / "5162" / "resolved_q_selection_gate.csv"
PREVIOUS_PROFILE = POST / "source-intake" / "functional_rg" / "5162" / "nested_zoom_profile_samples.csv"
STATE_SCALE = POST / "source-intake" / "functional_rg" / "5151" / "galaxy_state_stress_scale_gate.csv"
JEANS_SCALE = POST / "source-intake" / "functional_rg" / "5152" / "linear_Jeans_scale_gate.csv"
HALO_INVENTORY = POST / "source-intake" / "functional_rg" / "5153" / "finite_virial_halo_inventory.csv"
IR_COORDINATES = POST / "source-intake" / "functional_rg" / "4958" / "essential_IR_coordinate_convergence.csv"

OUT = POST / "source-intake" / "functional_rg" / "5163"
OPERATOR_CSV = OUT / "parent_wave_and_source_operator_contract.csv"
WAVE_CSV = OUT / "canonical_wave_transition_magnitude.csv"
OVERLAP_CSV = OUT / "universal_wave_mass_overlap_gate.csv"
GRADIENT_CSV = OUT / "essential_gradient_stress_envelope.csv"
BARYON_CSV = OUT / "visible_baryon_source_profile.csv"
RESPONSE_CSV = OUT / "adiabatic_visible_source_response_matrix.csv"
INVERSE_CSV = OUT / "visible_source_inverse_requirement.csv"
DECISION_CSV = OUT / "route_decision.csv"
PROVENANCE_CSV = OUT / "source_provenance.csv"
RESULT_JSON = OUT / "parent_wave_and_visible_source_results.json"
VALIDATION_CSV = POST / "source-intake" / "mts_residuals" / "P8_Y5_BRR545_5163_VALIDATION.csv"
DOCUMENT = POST / "5163-Y5-R2FR-parent-wave-stress-and-visible-source-response-gate.md"

MARKER = "MTS_5163_PARENT_WAVE_AND_VISIBLE_SOURCE_RESPONSE_GATE"
CHECKED_DATE = "2026-07-20"
FORMAL_DIGEST_LOCK = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"
REFERENCE_GALAXY = "UGC09133"
REFERENCE_MAPPING = "Wetterich_v_equals_minus_2lambda"
MAPPINGS = (
    "Wetterich_v_equals_minus_2lambda",
    "Wetterich_v_equals_plus_2lambda",
)
CONFIGURATIONS = ("NESTED128", "NESTED160")
MASS_LABELS = {
    "ten_times_WKB_floor": 2.8166916621557602e-21,
    "benchmark_1e_minus20_eV": 1.0e-20,
    "benchmark_1e_minus18_eV": 1.0e-18,
}
RESPONSE_EFFICIENCIES = (0.0, 0.05, 0.10, 0.25, 0.50, 1.0)
WAVE_TARGET_FRACTIONS = (1.0, 0.1, 0.01)

OMEGA_M = 0.315
OMEGA_B = 0.04924319136384048
MOTION_FRACTION = (OMEGA_M - OMEGA_B) / OMEGA_M
G_KPC_KM2_S2_MSUN = 4.30091727003628e-6
G_SI = 6.67430e-11
C_SI = 299792458.0
PARSEC_M = 3.085677581491367e16
EV_J = 1.602176634e-19
HBAR_C_EV_M = 1.973269804e-7
G_NATURAL_EV_MINUS2 = 6.70883e-57
PLANCK_LENGTH_M = 1.616255e-35


def source_paths() -> dict[str, Path]:
    return {
        "previous_document": PREVIOUS_DOCUMENT,
        "previous_result": PREVIOUS_RESULT,
        "previous_q": PREVIOUS_Q,
        "previous_profile": PREVIOUS_PROFILE,
        "state_scale": STATE_SCALE,
        "Jeans_scale": JEANS_SCALE,
        "halo_inventory": HALO_INVENTORY,
        "essential_IR_coordinates": IR_COORDINATES,
        "galaxy_samples_read_only": GALAXY_SAMPLES,
    }


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


def parse_samples(path: Path) -> list[dict[str, Any]]:
    text = path.read_text(encoding="utf-8-sig")
    text = re.sub(r"^window\.MTS_SAMPLES\s*=\s*", "", text).strip()
    text = re.sub(r";\s*$", "", text)
    return json.loads(text)


def parse_rotmod(samples: list[dict[str, Any]], galaxy: str) -> list[dict[str, float]]:
    source = next(sample for sample in samples if sample["name"] == f"{galaxy}_rotmod.dat")
    rows: list[dict[str, float]] = []
    for line in source["text"].splitlines():
        if not line or line.startswith("#"):
            continue
        values = [float(value) for value in line.split()[:8]]
        radius, observed, error, gas, disk, bulge, surface_disk, surface_bulge = values
        baryon_velocity_squared = gas * abs(gas) + 0.5 * disk**2 + 0.7 * bulge**2
        rows.append(
            {
                "radius_kpc": radius,
                "observed_velocity_km_s": observed,
                "observed_error_km_s": error,
                "gas_velocity_km_s": gas,
                "disk_velocity_km_s": disk,
                "bulge_velocity_km_s": bulge,
                "surface_disk_Lsun_pc2": surface_disk,
                "surface_bulge_Lsun_pc2": surface_bulge,
                "baryon_velocity_squared_km2_s2": baryon_velocity_squared,
                "spherical_equivalent_baryon_mass_Msun": radius
                * baryon_velocity_squared
                / G_KPC_KM2_S2_MSUN,
            }
        )
    if len(rows) < 5:
        raise RuntimeError(f"insufficient ROTMOD rows for {galaxy}")
    return rows


def wave_shape_coefficient(q_value: float) -> float:
    numerator = q_value * (
        2.0 * q_value**4
        + 6.0 * q_value**3
        + 9.0 * q_value**2
        + 12.0 * q_value
        + 8.0
    )
    return numerator / (2.0 * (q_value + 2.0) ** 3)


def local_logarithmic_q(
    radii: np.ndarray,
    velocity_squared: np.ndarray,
    transition_radius: float,
) -> float:
    valid = (radii > 0.0) & (velocity_squared > 0.0) & np.isfinite(velocity_squared)
    selected_radii = radii[valid]
    selected_velocity = velocity_squared[valid]
    if len(selected_radii) < 5 or transition_radius < selected_radii[1] or transition_radius > selected_radii[-2]:
        return math.nan
    index = int(np.searchsorted(selected_radii, transition_radius))
    lower = max(0, index - 2)
    upper = min(len(selected_radii), index + 3)
    slope = np.polyfit(
        np.log(selected_radii[lower:upper]),
        np.log(selected_velocity[lower:upper]),
        1,
    )[0]
    return 2.0 * float(slope)


def state_rows() -> list[dict[str, str]]:
    return [
        row
        for row in read_csv(STATE_SCALE)
        if row["galaxy"] == REFERENCE_GALAXY and row["mapping"] in MAPPINGS
    ]


def canonical_wave_rows(
    reference_states: list[dict[str, str]],
) -> list[dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for state in reference_states:
        q_value = float(state["q_parent"])
        unit_mass = float(state["minimum_m_gap_eV_for_lambda_db_le_Rn"])
        coefficient = wave_shape_coefficient(q_value)
        for mass_label, mass_value in MASS_LABELS.items():
            epsilon = unit_mass / mass_value
            rows.append(
                {
                    "galaxy": REFERENCE_GALAXY,
                    "mapping": state["mapping"],
                    "mass_label": mass_label,
                    "m_gap_eV": mass_value,
                    "q_profile": q_value,
                    "wave_shape_coefficient_Cq": coefficient,
                    "reduced_deBroglie_over_Rn": epsilon,
                    "quantum_to_gravity_acceleration_at_Rn": coefficient * epsilon**2,
                    "equation": "eta_Q=C_q[HBAR/(m v_infinity R_n)]^2",
                    "changes_q_at_order_one": coefficient * epsilon**2 >= 0.1,
                    "valid_for_claim": False,
                    "checkpoint_marker": MARKER,
                }
            )
    return rows


def wave_overlap_rows(
    all_states: list[dict[str, str]],
    reference_state: dict[str, str],
) -> tuple[list[dict[str, Any]], float, float]:
    Jeans_rows = read_csv(JEANS_SCALE)
    Jeans_reference = next(
        row
        for row in Jeans_rows
        if row["mass_label"] == "WKB_floor_all_175"
        and row["epoch"] == "equality"
        and row["gravity_density"] == "total_matter_gravity"
    )
    reference_mass = float(Jeans_reference["m_gap_eV"])
    reference_Jeans_mass = float(Jeans_reference["Jeans_sphere_mass_Msun"])
    inventory_rows = [
        row
        for row in read_csv(HALO_INVENTORY)
        if row["mass_label"] == "benchmark_1e_minus20_eV"
    ]
    minimum_halo_mass = min(
        float(row["cosmic_fraction_total_mass_vir_Msun"])
        for row in inventory_rows
    )
    all_patch_mass_floor = reference_mass * (
        reference_Jeans_mass / minimum_halo_mass
    ) ** (2.0 / 3.0)
    q_value = float(reference_state["q_parent"])
    unit_mass = float(reference_state["minimum_m_gap_eV_for_lambda_db_le_Rn"])
    coefficient = wave_shape_coefficient(q_value)
    rows: list[dict[str, Any]] = []
    for target_fraction in WAVE_TARGET_FRACTIONS:
        required_mass = unit_mass * math.sqrt(coefficient / target_fraction)
        Jeans_mass = reference_Jeans_mass * (required_mass / reference_mass) ** (-1.5)
        halo_passes = sum(
            float(row["cosmic_fraction_total_mass_vir_Msun"]) >= Jeans_mass
            for row in inventory_rows
        )
        wave_ratios = [
            wave_shape_coefficient(float(row["q_parent"]))
            * (
                float(row["minimum_m_gap_eV_for_lambda_db_le_Rn"])
                / required_mass
            )
            ** 2
            for row in all_states
        ]
        rows.append(
            {
                "row_type": "UGC09133_wave_target",
                "target_quantum_to_gravity_fraction_at_Rn": target_fraction,
                "required_universal_m_gap_eV": required_mass,
                "equality_Jeans_mass_Msun": Jeans_mass,
                "halo_mapping_rows_above_Jeans_mass": halo_passes,
                "halo_mapping_rows_total": len(inventory_rows),
                "state_rows_with_wave_ratio_le_one": sum(value <= 1.0 for value in wave_ratios),
                "maximum_wave_ratio_across_state_rows": max(wave_ratios),
                "universal_population_gate": halo_passes == len(inventory_rows),
                "valid_for_claim": False,
                "checkpoint_marker": MARKER,
            }
        )
    all_patch_eta = coefficient * (unit_mass / all_patch_mass_floor) ** 2
    rows.append(
        {
            "row_type": "all_patch_Jeans_floor",
            "target_quantum_to_gravity_fraction_at_Rn": all_patch_eta,
            "required_universal_m_gap_eV": all_patch_mass_floor,
            "equality_Jeans_mass_Msun": minimum_halo_mass,
            "halo_mapping_rows_above_Jeans_mass": len(inventory_rows),
            "halo_mapping_rows_total": len(inventory_rows),
            "state_rows_with_wave_ratio_le_one": sum(
                wave_shape_coefficient(float(row["q_parent"]))
                * (
                    float(row["minimum_m_gap_eV_for_lambda_db_le_Rn"])
                    / all_patch_mass_floor
                )
                ** 2
                <= 1.0
                for row in all_states
            ),
            "maximum_wave_ratio_across_state_rows": max(
                wave_shape_coefficient(float(row["q_parent"]))
                * (
                    float(row["minimum_m_gap_eV_for_lambda_db_le_Rn"])
                    / all_patch_mass_floor
                )
                ** 2
                for row in all_states
            ),
            "universal_population_gate": True,
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        }
    )
    return rows, all_patch_mass_floor, all_patch_eta


def gradient_stress_rows(
    reference_states: list[dict[str, str]],
) -> list[dict[str, Any]]:
    coefficient_rows = read_csv(IR_COORDINATES)
    selected = [
        row
        for row in coefficient_rows
        if row["coordinate"] in {"A2_endpoint", "W_O4_endpoint"}
        and row["upper_order"] == "8"
    ]
    values = {
        (row["scheme"], row["coordinate"]): float(row["upper_value"])
        for row in selected
    }
    rows: list[dict[str, Any]] = []
    joule_per_eV4 = EV_J / HBAR_C_EV_M**3
    for state in reference_states:
        q_value = float(state["q_parent"])
        velocity = 1000.0 * float(state["v_infinity_km_s"])
        radius = 1000.0 * PARSEC_M * (
            float(state["L_eff_kpc"]) * float(state["R_n_over_L_eff"])
        )
        density_shape = (q_value + 2.0) / 4.0
        mass_density = velocity**2 * density_shape / (4.0 * math.pi * G_SI * radius**2)
        energy_density_eV4 = mass_density * C_SI**2 / joule_per_eV4
        beta = (velocity / C_SI) ** 2
        for scheme in sorted({row["scheme"] for row in selected}):
            essential_X2 = abs(values[(scheme, "A2_endpoint")]) * G_NATURAL_EV_MINUS2**2
            X2_hessian_envelope = 8.0 * essential_X2 * energy_density_eV4
            Weyl_coordinate = abs(values[(scheme, "W_O4_endpoint")])
            O4_kinetic_envelope = (
                96.0
                * Weyl_coordinate
                * beta**2
                * (PLANCK_LENGTH_M / radius) ** 4
            )
            rows.append(
                {
                    "galaxy": REFERENCE_GALAXY,
                    "mapping": state["mapping"],
                    "scheme": scheme,
                    "q_parent": q_value,
                    "target_density_at_Rn_kg_m3": mass_density,
                    "target_energy_density_at_Rn_eV4": energy_density_eV4,
                    "A2_endpoint": values[(scheme, "A2_endpoint")],
                    "c_ess_abs_eV_minus4": essential_X2,
                    "X2_fractional_Hessian_shift_envelope": X2_hessian_envelope,
                    "W_O4_endpoint": values[(scheme, "W_O4_endpoint")],
                    "O4_fractional_kinetic_shift_envelope": O4_kinetic_envelope,
                    "order_one_transition_stress": max(X2_hessian_envelope, O4_kinetic_envelope) >= 0.1,
                    "valid_for_claim": False,
                    "checkpoint_marker": MARKER,
                }
            )
    return rows


class BaryonSource:
    def __init__(self, rows: list[dict[str, float]]) -> None:
        self.radii = np.array([row["radius_kpc"] for row in rows], dtype=float)
        self.velocity_squared = np.array(
            [row["baryon_velocity_squared_km2_s2"] for row in rows], dtype=float
        )
        self.interpolator = PchipInterpolator(self.radii, self.velocity_squared)
        self.outer_mass = (
            self.radii[-1]
            * self.velocity_squared[-1]
            / G_KPC_KM2_S2_MSUN
        )

    def velocity_squared_at(self, radius: float) -> float:
        if radius < self.radii[0]:
            return float(self.velocity_squared[0] * (radius / self.radii[0]) ** 2)
        if radius <= self.radii[-1]:
            return float(self.interpolator(radius))
        return G_KPC_KM2_S2_MSUN * self.outer_mass / radius

    def equivalent_mass_at(self, radius: float) -> float:
        return radius * self.velocity_squared_at(radius) / G_KPC_KM2_S2_MSUN


def profile_for(config_id: str, mapping: str) -> dict[str, np.ndarray]:
    rows = [
        row
        for row in read_csv(PREVIOUS_PROFILE)
        if row["config_id"] == config_id and row["mapping_scored"] == mapping
    ]
    rows.sort(key=lambda row: float(row["radius_kpc"]))
    return {
        "radius": np.array([float(row["radius_kpc"]) for row in rows]),
        "motion_mass": np.array(
            [float(row["paired_mean_motion_excess_mass_Msun"]) for row in rows]
        ),
        "motion_velocity_squared": np.array(
            [float(row["paired_mean_motion_v2_km2_s2"]) for row in rows]
        ),
        "target_velocity_squared": np.array(
            [float(row["target_motion_v2_km2_s2"]) for row in rows]
        ),
        "score_mask": np.array(
            [row["inside_resolved_scoring_window"] == "True" for row in rows]
        ),
    }


def adiabatic_response(
    profile: dict[str, np.ndarray],
    source: BaryonSource,
    efficiency: float,
) -> tuple[np.ndarray, np.ndarray, float, int, float]:
    radii = profile["radius"]
    raw_mass = profile["motion_mass"]
    monotone_mass = np.maximum.accumulate(np.maximum(raw_mass, 0.0))
    monotone_adjustment = float(
        np.max(np.abs(monotone_mass - np.maximum(raw_mass, 0.0)))
        / max(float(np.max(monotone_mass)), 1.0)
    )
    mass_interpolator = PchipInterpolator(radii, monotone_mass)
    contracted_mass = np.empty_like(radii)
    initial_radii = np.empty_like(radii)
    root_failures = 0
    maximum_residual = 0.0
    if efficiency == 0.0:
        return (
            raw_mass.copy(),
            radii.copy(),
            0.0,
            0,
            monotone_adjustment,
        )
    for index, final_radius in enumerate(radii):
        baryon_mass = efficiency * source.equivalent_mass_at(float(final_radius))

        def invariant(initial_radius: float) -> float:
            motion_mass = float(mass_interpolator(initial_radius))
            return (
                initial_radius * motion_mass / MOTION_FRACTION
                - final_radius * (motion_mass + baryon_mass)
            )

        lower = float(radii[0])
        upper = float(radii[-1])
        lower_value = invariant(lower)
        upper_value = invariant(upper)
        if lower_value > 0.0 or upper_value < 0.0:
            initial_radius = math.nan
            root_failures += 1
        else:
            initial_radius = float(brentq(invariant, lower, upper, xtol=1.0e-11, rtol=1.0e-12))
        initial_radii[index] = initial_radius
        if math.isfinite(initial_radius):
            contracted_mass[index] = float(mass_interpolator(initial_radius))
            left = initial_radius * contracted_mass[index] / MOTION_FRACTION
            right = final_radius * (contracted_mass[index] + baryon_mass)
            residual = abs(left - right) / max(abs(left), abs(right), 1.0)
            maximum_residual = max(maximum_residual, residual)
        else:
            contracted_mass[index] = math.nan
    return contracted_mass, initial_radii, maximum_residual, root_failures, monotone_adjustment


def response_score(
    config_id: str,
    mapping: str,
    profile: dict[str, np.ndarray],
    source: BaryonSource,
    efficiency: float,
    q_parent: float,
    transition_radius: float,
    previous_envelope: float,
) -> dict[str, Any]:
    contracted_mass, initial_radii, residual, failures, adjustment = adiabatic_response(
        profile, source, efficiency
    )
    if efficiency == 0.0:
        velocity_squared = profile["motion_velocity_squared"].copy()
    else:
        velocity_squared = G_KPC_KM2_S2_MSUN * contracted_mass / profile["radius"]
    q_response = local_logarithmic_q(profile["radius"], velocity_squared, transition_radius)
    score_mask = profile["score_mask"] & np.isfinite(velocity_squared) & (velocity_squared > 0.0)
    velocity_rmse = float(
        np.sqrt(
            np.mean(
                np.log10(
                    velocity_squared[score_mask]
                    / profile["target_velocity_squared"][score_mask]
                )
                ** 2
            )
        )
    )
    transition_velocity = float(np.interp(transition_radius, profile["radius"], velocity_squared))
    target_transition_velocity = float(
        np.interp(
            transition_radius,
            profile["radius"],
            profile["target_velocity_squared"],
        )
    )
    finite_initial = initial_radii[np.isfinite(initial_radii)]
    return {
        "config_id": config_id,
        "mapping": mapping,
        "adiabatic_response_efficiency": efficiency,
        "response_role": "predeclared_sensitivity_not_coupling_or_fit",
        "q_parent": q_parent,
        "q_response": q_response,
        "q_absolute_difference": abs(q_response - q_parent),
        "q_numerically_compatible": abs(q_response - q_parent) <= previous_envelope,
        "velocity_squared_log10_RMSE_no_refit": velocity_rmse,
        "transition_velocity_squared_ratio_to_target": transition_velocity / target_transition_velocity,
        "maximum_shell_invariant_relative_residual": residual,
        "root_failures": failures,
        "maximum_initial_to_final_radius_ratio": float(
            np.max(finite_initial / profile["radius"][np.isfinite(initial_radii)])
        ),
        "monotone_mass_regularization_fraction": adjustment,
        "parent_selected_efficiency": False,
        "valid_for_claim": False,
        "checkpoint_marker": MARKER,
    }


def visible_source_rows(
    rotmod_rows: list[dict[str, float]],
) -> list[dict[str, Any]]:
    return [
        {
            "galaxy": REFERENCE_GALAXY,
            **row,
            "ML_disk": 0.5,
            "ML_bulge": 0.7,
            "source_role": "measured_visible_Hilbert_source_read_only",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        }
        for row in rotmod_rows
    ]


def response_rows_and_inverse(
    reference_states: list[dict[str, str]],
    source: BaryonSource,
    previous_q: dict[str, str],
) -> tuple[list[dict[str, Any]], list[dict[str, Any]]]:
    state_lookup = {row["mapping"]: row for row in reference_states}
    response_rows: list[dict[str, Any]] = []
    inverse_rows: list[dict[str, Any]] = []
    previous_envelope = float(previous_q["q_uncertainty_envelope"])
    for config_id in CONFIGURATIONS:
        for mapping in MAPPINGS:
            state = state_lookup[mapping]
            q_parent = float(state["q_parent"])
            transition_radius = float(state["L_eff_kpc"]) * float(state["R_n_over_L_eff"])
            profile = profile_for(config_id, mapping)
            for efficiency in RESPONSE_EFFICIENCIES:
                response_rows.append(
                    response_score(
                        config_id,
                        mapping,
                        profile,
                        source,
                        efficiency,
                        q_parent,
                        transition_radius,
                        previous_envelope,
                    )
                )

            def q_residual(efficiency: float) -> float:
                return float(
                    response_score(
                        config_id,
                        mapping,
                        profile,
                        source,
                        efficiency,
                        q_parent,
                        transition_radius,
                        previous_envelope,
                    )["q_response"]
                    - q_parent
                )

            lower_residual = q_residual(0.0)
            upper_residual = q_residual(1.0)
            crossing_exists = lower_residual * upper_residual <= 0.0
            required_efficiency = (
                float(brentq(q_residual, 0.0, 1.0, xtol=1.0e-9, rtol=1.0e-10))
                if crossing_exists
                else math.nan
            )
            inverse_score = (
                response_score(
                    config_id,
                    mapping,
                    profile,
                    source,
                    required_efficiency,
                    q_parent,
                    transition_radius,
                    previous_envelope,
                )
                if crossing_exists
                else None
            )
            inverse_rows.append(
                {
                    "config_id": config_id,
                    "mapping": mapping,
                    "q_parent": q_parent,
                    "q_crossing_exists_between_zero_and_full_response": crossing_exists,
                    "diagnostic_efficiency_required_for_q": required_efficiency if crossing_exists else "",
                    "velocity_squared_log10_RMSE_at_q_crossing": inverse_score[
                        "velocity_squared_log10_RMSE_no_refit"
                    ]
                    if inverse_score
                    else "",
                    "transition_velocity_squared_ratio_at_q_crossing": inverse_score[
                        "transition_velocity_squared_ratio_to_target"
                    ]
                    if inverse_score
                    else "",
                    "inverse_use_only": True,
                    "parent_selected_efficiency": False,
                    "reason": "solving for the efficiency uses q_parent and is not a prediction",
                    "valid_for_claim": False,
                    "checkpoint_marker": MARKER,
                }
            )
    return response_rows, inverse_rows


def operator_rows() -> list[dict[str, Any]]:
    return [
        {
            "operator": "canonical_Madelung_stress",
            "parent_origin": "KG_to_Schrodinger_Poisson_limit",
            "equation": "PiQ_ij=HBAR^2[(d_i rho)(d_j rho)/rho-d_i d_j rho]/(4m^2)",
            "local_zero": "rho_motion=0 implies PiQ_ij=0",
            "new_coupling": False,
            "test_here": "exact transition acceleration ratio",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "operator": "essential_X_squared",
            "parent_origin": "4958_GR_connected_essential_PX_trajectory",
            "equation": "c_ess=A2 G_N^2 with fractional Hessian envelope <=8|c_ess|rho",
            "local_zero": "X=0 implies first and second residual silence",
            "new_coupling": False,
            "test_here": "transition density magnitude envelope",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "operator": "Weyl_squared_kinetic_portal",
            "parent_origin": "4958_GR_connected_O4_trajectory",
            "equation": "delta Z=2u_O4 C_abcd C^abcd",
            "local_zero": "psi=0 implies motion stress zero",
            "new_coupling": False,
            "test_here": "conservative transition curvature envelope",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "operator": "visible_Hilbert_source",
            "parent_origin": "4947_universal_metric_residue",
            "equation": "nabla^2 Phi=4pi G_N(rho_visible+rho_motion+rho_EM)",
            "local_zero": "not zeroed; it is ordinary GR and uses the same calibrated G_N",
            "new_coupling": False,
            "test_here": "measured baryonic acceleration plus adiabatic response bracket",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
    ]


def provenance_rows(paths: dict[str, Path]) -> list[dict[str, Any]]:
    rows = [
        {
            "source_id": source_id,
            "source_path": str(path),
            "sha256": file_digest(path),
            "role": source_id.replace("_", " "),
            "read_only": True,
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        }
        for source_id, path in paths.items()
    ]
    rows.append(
        {
            "source_id": "physical_constants",
            "source_path": "CODATA exact SI conversion constants embedded in checkpoint script",
            "sha256": "not_applicable_literal_constants",
            "role": "unit conversion only",
            "read_only": True,
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        }
    )
    return rows


def add_validation(
    rows: list[dict[str, Any]],
    check_id: str,
    passed: bool,
    evidence: Any,
) -> None:
    rows.append(
        {
            "check_id": check_id,
            "passed": bool(passed),
            "evidence": json.dumps(evidence, sort_keys=True, default=str),
            "checkpoint_marker": MARKER,
        }
    )


def make_document(result: dict[str, Any]) -> str:
    summary = result["summary"]
    return f"""# 5163 - Parent wave stress and visible-source response gate

Marker: `{MARKER}`.

Date: `{CHECKED_DATE}`.

## Decision

Checkpoint 5162 rejected ordinary free collisionless collapse as the source
of the resolved parent transition. Checkpoint 5163 now varies the terms that
the existing parent actually owns rather than inventing a galaxy force.

The canonical Madelung stress is derived exactly. For
`n_q=x^q/(1+x^q)` and the density implied by its circular-speed support,

```text
eta_Q(R_n)=C_q [hbar/(m v_infinity R_n)]^2,
C_q=q(2q^4+6q^3+9q^2+12q+8)/[2(q+2)^3].
```

At the frozen `1e-20 eV` mass its UGC09133 value is
`{summary['benchmark_wave_fraction']}`. Requiring every current halo mapping
to remain above the instantaneous equality Jeans mass gives the weaker
universal floor `{summary['all_patch_mass_floor_eV']} eV`; even there the
UGC09133 wave fraction is only `{summary['wave_fraction_at_all_patch_floor']}`.
Canonical wave pressure therefore cannot supply the order-one transition
change by itself on this branch.

The already-derived essential `X^2` and Weyl-kinetic operators are smaller
still. Their largest conservative fractional transition envelopes are
`{summary['maximum_X2_envelope']}` and
`{summary['maximum_O4_envelope']}`. No unsigned coefficient was inserted.

## Visible-source correction

The numerical audit exposes a different omission: checkpoint 5162 evolved
the cosmic total-matter field but did not include the condensed UGC09133
baryonic source. The parent already couples that source through the same
Einstein residue used for local GR and Newton. With the locked
`ML_disk=0.5`, `ML_bulge=0.7` convention, the measured baryonic acceleration
at `R_n` is `{summary['baryon_to_target_motion_v2_at_Rn']}` times the target
motion acceleration. It is not perturbatively small.

A spherical circular-orbit adiabatic invariant was therefore used as a
controlled upper-response bracket,

```text
r_i M_X,i(r_i)/f_X
 =r_f[M_X,i(r_i)+epsilon_ad M_b,eq(r_f)].
```

`epsilon_ad` is explicitly a sensitivity coordinate, not a new coupling.
The zero-response rows reproduce checkpoint 5162. Full response moves the
fine-grid transition from `q={summary['fine_q_zero_response']}` to
`q={summary['fine_q_full_response']}` and changes the no-refit velocity-
squared RMSE from `{summary['fine_RMSE_zero_response']}` to
`{summary['fine_RMSE_full_response']}` dex. The response therefore crosses
the parent `q`; the inverse crossing occurs at
`epsilon_ad={summary['fine_inverse_efficiency']}`, but that value is not
promoted because solving for it uses the target exponent.

This is the important result: the known universal visible coupling has enough
leverage to change the failed transition, whereas the canonical wave and
known local gradient terms do not. The adiabatic bracket does not derive the
assembly history and does not jointly select the parent profile. The next
calculation must evolve visible and motion components together under the same
Poisson/Einstein source, with the baryon fraction and initial covariance fixed
before reading `q`. It may not turn the inverse efficiency into a fitted
coupling.

## Claim boundary

```text
canonical parent wave stress derived                 = yes;
canonical wave stress sufficient at frozen mass      = no;
known essential gradient operators sufficient        = no;
condensed visible source omitted by 5162              = yes;
same-G_N visible source has transition leverage       = yes;
adiabatic response selects q without inversion        = no;
coupled baryon-motion assembly derived                = no;
local GR/Newton/Maxwell branch modified               = no;
galaxy or full-MTS claim                              = false.
```

All `{result['validation_count']}` validation rows pass. All outputs remain
nonclaim. Source hashes are unchanged; the protected `formalization-workbench`
digest is `{result['formalization_workbench_tree_sha256']}`. The galaxy source
was read-only and no GitHub action occurred.
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
    source_hashes_before = {key: file_digest(path) for key, path in paths.items()}
    previous_result = json.loads(PREVIOUS_RESULT.read_text(encoding="utf-8"))
    previous_q = read_csv(PREVIOUS_Q)[0]
    all_states = read_csv(STATE_SCALE)
    reference_states = state_rows()
    if arguments.dry_run:
        print(
            json.dumps(
                {
                    "dry_run": True,
                    "sources": {key: str(path) for key, path in paths.items()},
                    "response_efficiencies": RESPONSE_EFFICIENCIES,
                    "formal_digest": formal_before,
                },
                indent=2,
            )
        )
        return
    samples = parse_samples(GALAXY_SAMPLES)
    rotmod_rows = parse_rotmod(samples, REFERENCE_GALAXY)
    source = BaryonSource(rotmod_rows)
    operators = operator_rows()
    wave_rows = canonical_wave_rows(reference_states)
    reference_state = next(row for row in reference_states if row["mapping"] == REFERENCE_MAPPING)
    overlap_rows, all_patch_mass_floor, all_patch_eta = wave_overlap_rows(
        all_states, reference_state
    )
    gradient_rows = gradient_stress_rows(reference_states)
    baryon_rows = visible_source_rows(rotmod_rows)
    response_rows, inverse_rows = response_rows_and_inverse(
        reference_states, source, previous_q
    )
    provenance = provenance_rows(paths)
    fine_zero = next(
        row
        for row in response_rows
        if row["config_id"] == "NESTED160"
        and row["mapping"] == REFERENCE_MAPPING
        and row["adiabatic_response_efficiency"] == 0.0
    )
    fine_full = next(
        row
        for row in response_rows
        if row["config_id"] == "NESTED160"
        and row["mapping"] == REFERENCE_MAPPING
        and row["adiabatic_response_efficiency"] == 1.0
    )
    fine_inverse = next(
        row
        for row in inverse_rows
        if row["config_id"] == "NESTED160" and row["mapping"] == REFERENCE_MAPPING
    )
    transition_radius = float(reference_state["L_eff_kpc"]) * float(
        reference_state["R_n_over_L_eff"]
    )
    baryon_at_transition = source.velocity_squared_at(transition_radius)
    reference_profile = profile_for("NESTED160", REFERENCE_MAPPING)
    target_at_transition = float(
        np.interp(
            transition_radius,
            reference_profile["radius"],
            reference_profile["target_velocity_squared"],
        )
    )
    benchmark_wave = next(
        row
        for row in wave_rows
        if row["mapping"] == REFERENCE_MAPPING
        and row["mass_label"] == "benchmark_1e_minus20_eV"
    )
    summary = {
        "benchmark_wave_fraction": benchmark_wave[
            "quantum_to_gravity_acceleration_at_Rn"
        ],
        "all_patch_mass_floor_eV": all_patch_mass_floor,
        "wave_fraction_at_all_patch_floor": all_patch_eta,
        "maximum_X2_envelope": max(
            row["X2_fractional_Hessian_shift_envelope"] for row in gradient_rows
        ),
        "maximum_O4_envelope": max(
            row["O4_fractional_kinetic_shift_envelope"] for row in gradient_rows
        ),
        "baryon_to_target_motion_v2_at_Rn": baryon_at_transition
        / target_at_transition,
        "fine_q_zero_response": fine_zero["q_response"],
        "fine_q_full_response": fine_full["q_response"],
        "fine_RMSE_zero_response": fine_zero[
            "velocity_squared_log10_RMSE_no_refit"
        ],
        "fine_RMSE_full_response": fine_full[
            "velocity_squared_log10_RMSE_no_refit"
        ],
        "fine_inverse_efficiency": fine_inverse[
            "diagnostic_efficiency_required_for_q"
        ],
        "q_parent": float(reference_state["q_parent"]),
        "q_envelope": float(previous_q["q_uncertainty_envelope"]),
    }
    decisions = [
        {
            "route": "canonical_wave_pressure",
            "result": "REJECTED_AS_ORDER_ONE_TRANSITION_OWNER_ON_UNIVERSAL_POPULATION_BRANCH",
            "evidence": f"eta_Q(1e-20eV)={summary['benchmark_wave_fraction']}; eta_Q(all-patch floor)={all_patch_eta}",
            "next_requirement": "none unless a parent critical amplification is derived",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "route": "known_essential_gradient_terms",
            "result": "REJECTED_AS_MACROSCOPIC_TRANSITION_OWNER",
            "evidence": f"X2<={summary['maximum_X2_envelope']}; O4<={summary['maximum_O4_envelope']}",
            "next_requirement": "do not inflate source-locked coefficients",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "route": "universal_visible_Hilbert_source",
            "result": "RETAINED_WITH_ORDER_ONE_LEVERAGE_BUT_ASSEMBLY_UNDERIVED",
            "evidence": f"baryon/target-motion acceleration={summary['baryon_to_target_motion_v2_at_Rn']}; q bracket={summary['fine_q_zero_response']} to {summary['fine_q_full_response']}",
            "next_requirement": "coupled visible-motion initial-value evolution with no fitted response efficiency",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
    ]
    generated = {
        OPERATOR_CSV: operators,
        WAVE_CSV: wave_rows,
        OVERLAP_CSV: overlap_rows,
        GRADIENT_CSV: gradient_rows,
        BARYON_CSV: baryon_rows,
        RESPONSE_CSV: response_rows,
        INVERSE_CSV: inverse_rows,
        DECISION_CSV: decisions,
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
    source_hashes_after = {key: file_digest(path) for key, path in paths.items()}
    formal_after = tree_digest(FORMAL)
    validation: list[dict[str, Any]] = []
    add_validation(validation, "sources_exist", not missing, missing)
    add_validation(
        validation,
        "source_hashes_unchanged",
        source_hashes_before == source_hashes_after,
        source_hashes_after,
    )
    add_validation(
        validation,
        "formalization_workbench_unchanged",
        formal_after == FORMAL_DIGEST_LOCK,
        formal_after,
    )
    add_validation(
        validation,
        "predecessor_validated",
        previous_result["validation_failures"] == [],
        previous_result["validation_failures"],
    )
    add_validation(validation, "reference_state_rows_complete", len(reference_states) == 2, len(reference_states))
    add_validation(validation, "ROTMOD_rows_complete", len(rotmod_rows) == 68, len(rotmod_rows))
    add_validation(
        validation,
        "ROTMOD_covers_transition",
        float(rotmod_rows[0]["radius_kpc"]) < transition_radius < float(rotmod_rows[-1]["radius_kpc"]),
        transition_radius,
    )
    add_validation(
        validation,
        "wave_formula_positive",
        all(row["wave_shape_coefficient_Cq"] > 0.0 for row in wave_rows),
        [row["wave_shape_coefficient_Cq"] for row in wave_rows],
    )
    add_validation(
        validation,
        "benchmark_wave_perturbative",
        summary["benchmark_wave_fraction"] < 1.0e-6,
        summary["benchmark_wave_fraction"],
    )
    add_validation(
        validation,
        "all_patch_floor_wave_small",
        all_patch_eta < 1.0e-3,
        all_patch_eta,
    )
    add_validation(
        validation,
        "gradient_envelopes_finite",
        all(
            math.isfinite(float(row["X2_fractional_Hessian_shift_envelope"]))
            and math.isfinite(float(row["O4_fractional_kinetic_shift_envelope"]))
            for row in gradient_rows
        ),
        len(gradient_rows),
    )
    add_validation(
        validation,
        "known_gradient_terms_small",
        summary["maximum_X2_envelope"] < 1.0e-80
        and summary["maximum_O4_envelope"] < 1.0e-180,
        [summary["maximum_X2_envelope"], summary["maximum_O4_envelope"]],
    )
    add_validation(
        validation,
        "zero_response_reproduces_5162_q",
        abs(summary["fine_q_zero_response"] - float(previous_q["q_nested_160"])) < 1.0e-10,
        [summary["fine_q_zero_response"], previous_q["q_nested_160"]],
    )
    add_validation(
        validation,
        "visible_source_has_transition_leverage",
        summary["baryon_to_target_motion_v2_at_Rn"] > 0.1,
        summary["baryon_to_target_motion_v2_at_Rn"],
    )
    add_validation(
        validation,
        "full_response_shell_invariants",
        max(
            float(row["maximum_shell_invariant_relative_residual"])
            for row in response_rows
            if row["adiabatic_response_efficiency"] == 1.0
        )
        < 1.0e-9,
        "full response",
    )
    add_validation(
        validation,
        "response_roots_cover_scored_profile",
        all(int(row["root_failures"]) == 0 for row in response_rows),
        max(int(row["root_failures"]) for row in response_rows),
    )
    add_validation(
        validation,
        "visible_response_crosses_parent_q",
        all(row["q_crossing_exists_between_zero_and_full_response"] for row in inverse_rows),
        len(inverse_rows),
    )
    add_validation(
        validation,
        "inverse_efficiency_not_promoted",
        all(row["inverse_use_only"] and not row["parent_selected_efficiency"] for row in inverse_rows),
        len(inverse_rows),
    )
    add_validation(
        validation,
        "no_new_coupling",
        all(not row["new_coupling"] for row in operators),
        len(operators),
    )
    add_validation(
        validation,
        "all_rows_nonclaim",
        all(not row["valid_for_claim"] for rows in generated.values() for row in rows),
        "all generated rows",
    )
    generated_text = "\n".join(
        path.read_text(encoding="utf-8") for path in [DOCUMENT, *generated]
    )
    add_validation(
        validation,
        "no_placeholders",
        "MISSING_" not in generated_text and "PLACEHOLDER" not in generated_text,
        "generated artifacts",
    )
    nonfinite_tokens = re.findall(
        r"(?:^|[,:\s\[])(?:nan|[-+]?inf|[-+]?infinity)(?:$|[,:\s\]])",
        generated_text,
        flags=re.IGNORECASE | re.MULTILINE,
    )
    add_validation(
        validation,
        "no_nonfinite_text",
        not nonfinite_tokens,
        nonfinite_tokens,
    )
    add_validation(
        validation,
        "document_marker",
        MARKER in DOCUMENT.read_text(encoding="utf-8"),
        str(DOCUMENT),
    )
    add_validation(
        validation,
        "galaxy_source_read_only",
        source_hashes_before["galaxy_samples_read_only"]
        == source_hashes_after["galaxy_samples_read_only"],
        source_hashes_after["galaxy_samples_read_only"],
    )
    failures = [row["check_id"] for row in validation if not row["passed"]]
    write_csv(VALIDATION_CSV, validation)
    result = {
        "checked_date": CHECKED_DATE,
        "checkpoint_marker": MARKER,
        "route_decision": "VISIBLE_HILBERT_SOURCE_SELECTED_FOR_COUPLED_ASSEMBLY_CANONICAL_WAVE_AND_KNOWN_GRADIENT_TERMS_TOO_SMALL",
        "summary": summary,
        "canonical_wave_sufficient": False,
        "known_gradient_terms_sufficient": False,
        "visible_source_has_sufficient_leverage": True,
        "visible_source_assembly_derived": False,
        "local_GR_Newton_Maxwell_branch_modified": False,
        "valid_for_galaxy_claim": False,
        "valid_for_local_GR_claim": False,
        "valid_for_full_MTS_claim": False,
        "source_hashes_before": source_hashes_before,
        "source_hashes_after": source_hashes_after,
        "formalization_workbench_tree_sha256": formal_after,
        "validation_count": len(validation),
        "validation_failures": failures,
    }
    write_json(RESULT_JSON, result)
    DOCUMENT.write_text(make_document(result), encoding="utf-8")
    if failures:
        raise RuntimeError(f"checkpoint 5163 validation failures: {failures}")


if __name__ == "__main__":
    main()
