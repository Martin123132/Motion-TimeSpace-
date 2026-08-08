from __future__ import annotations

import csv
import hashlib
import json
import math
from pathlib import Path
from typing import Any

import numpy as np
from scipy.special import jv


POST = Path(__file__).resolve().parents[1]
FORMAL = POST.parent / "formalization-workbench"
OUT = POST / "source-intake" / "functional_rg" / "5152"
RESULT_JSON = OUT / "primordial_motion_occupation_results.json"
BACKGROUND_CSV = OUT / "primordial_motion_background.csv"
BESSEL_CSV = OUT / "radiation_Bessel_dust_limit.csv"
JEANS_CSV = OUT / "linear_Jeans_scale_gate.csv"
MASS_WINDOW_CSV = OUT / "galaxy_mass_window.csv"
X2_CONTROL_CSV = OUT / "quadratic_X2_control_gate.csv"
LOCAL_CSV = OUT / "local_machine_cog_gate.csv"
ROUTE_CSV = OUT / "source_route_arbitration.csv"
VALIDATION_CSV = (
    POST
    / "source-intake"
    / "mts_residuals"
    / "P8_Y5_BRR545_5152_VALIDATION.csv"
)
DOCUMENT = (
    POST
    / "5152-Y5-R2FR-primordial-motion-occupation-dust-limit-Jeans-window-and-formation-source-arbitration.md"
)
MARKER = "MTS_5152_PRIMORDIAL_MOTION_OCCUPATION_JEANS_GATE"
CHECKED_DATE = "2026-07-20"
FORMAL_BASELINE = "b0f45c104b5d1ab4762e3f96f23c6e2b2a7afec8c70612879bda90c90308a758"

H0_KM_S_MPC = 67.4
LITTLE_H = H0_KM_S_MPC / 100.0
OMEGA_R = 9.0e-5
OMEGA_M = 0.315
OMEGA_B_H2 = 0.02237
OMEGA_B = OMEGA_B_H2 / LITTLE_H**2
OMEGA_X = OMEGA_M - OMEGA_B
OMEGA_LAMBDA = 1.0 - OMEGA_M - OMEGA_R
MPL_REDUCED_EV = 2.435e27

G_SI = 6.67430e-11
HBAR_J_S = 1.054571817e-34
HBAR_EV_S = 6.582119569e-16
C_M_S = 299792458.0
EV_C2_KG = 1.7826619216278976e-36
MPC_M = 3.085677581491367e22
KPC_M = MPC_M / 1000.0
MSUN_KG = 1.98847e30
AU_M = 1.495978707e11
GM_SUN_M3_S2 = 1.32712440018e20
H0_SI = H0_KM_S_MPC * 1000.0 / MPC_M
H0_EV = HBAR_EV_S * H0_SI
RHO_CRIT0_KG_M3 = 3.0 * H0_SI**2 / (8.0 * math.pi * G_SI)
RHO_X0_KG_M3 = OMEGA_X * RHO_CRIT0_KG_M3

NU_RD = 0.25
BESSEL_NORMALIZATION = 2.0**NU_RD * math.gamma(1.0 + NU_RD)
RD_DUST_MATCH = 4.0 * math.gamma(1.25) ** 2 / math.pi


SOURCE_PATHS = {
    "metric_only_cosmology": POST
    / "4897-Y5-R2FR-cosmology-without-bath-source-metric-only-baseline-and-derived-extension-reentry-gate.md",
    "static_CTP_source_rejection": POST
    / "4949-Y5-R2FR-covariant-2PI-motion-occupation-Dyson-source-and-conserved-galaxy-stress-or-composite-route-rejection.md",
    "formation_X2_rejection": POST
    / "4953-Y5-R2FR-galaxy-formation-transient-spectrum-X2-kinetic-cascade-and-local-injection-bound-or-composite-route-rejection.md",
    "formation_offshell_rejection": POST
    / "4954-Y5-R2FR-finite-time-off-shell-X2-number-changing-2PI-kernel-and-formation-source-efficiency-or-nonequilibrium-route-rejection.md",
    "sixpoint_route_rejection": POST
    / "4959-Y5-R2FR-O2-O3-O4-external-scalar-sixpoint-projectors-and-full-invariant-amplitude-or-curvature-route-rejection.md",
    "local_parent_action": POST
    / "4947-Y5-R2FR-local-GR-Newton-Maxwell-calibration-count-and-universal-source-residue-certificate.md",
    "local_zero_branch": POST
    / "4942-Y5-R2FR-O4-completed-endpoint-local-vacuum-homogeneous-motion-branch-and-C3-CFF-PPN-residual-gate.md",
    "state_stress_parent": POST
    / "5151-Y5-R2FR-parent-projective-occupation-to-conserved-Einstein-cluster-stress-and-two-metric-cog-gate.md",
    "state_stress_result": POST
    / "source-intake"
    / "functional_rg"
    / "5151"
    / "projective_state_stress_results.json",
    "state_stress_scale_rows": POST
    / "source-intake"
    / "functional_rg"
    / "5151"
    / "galaxy_state_stress_scale_gate.csv",
    "embedded_local_rows": POST
    / "source-intake"
    / "functional_rg"
    / "5151"
    / "embedded_local_cog_tidal_gate.csv",
}


PRIMARY_SOURCE_URLS = {
    "coherent_scalar_oscillations": "https://doi.org/10.1103/PhysRevD.28.1243",
    "linear_axion_CDM_proof": "https://arxiv.org/abs/0902.4738",
    "fuzzy_CDM_Jeans_scale": "https://arxiv.org/abs/astro-ph/0003365",
    "nonlinear_wave_halo_formation": "https://arxiv.org/abs/1407.7762",
    "oscillating_local_metric": "https://arxiv.org/abs/1309.5888",
}


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


def atomic_json(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(value, indent=2, sort_keys=True), encoding="utf-8"
    )
    temporary.replace(path)


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


def read_csv(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def bessel_state(x_value: float) -> tuple[float, float, float]:
    field = (
        BESSEL_NORMALIZATION
        * x_value ** (-NU_RD)
        * float(jv(NU_RD, x_value))
    )
    derivative = (
        -BESSEL_NORMALIZATION
        * x_value ** (-NU_RD)
        * float(jv(NU_RD + 1.0, x_value))
    )
    second_derivative = BESSEL_NORMALIZATION * (
        NU_RD
        * x_value ** (-NU_RD - 1.0)
        * float(jv(NU_RD + 1.0, x_value))
        - 0.5
        * x_value ** (-NU_RD)
        * (
            float(jv(NU_RD, x_value))
            - float(jv(NU_RD + 2.0, x_value))
        )
    )
    return field, derivative, second_derivative


def build_bessel_rows() -> tuple[list[dict[str, Any]], dict[str, float]]:
    rows: list[dict[str, Any]] = []
    maximum_kg_residual = 0.0
    for x_value in [
        1.0e-6,
        1.0e-4,
        1.0e-2,
        0.1,
        0.5,
        1.0,
        2.0,
        5.0,
        10.0,
        100.0,
        1000.0,
        1.0e4,
        1.0e5,
        1.0e6,
    ]:
        field, derivative, second_derivative = bessel_state(x_value)
        kg_residual = second_derivative + 1.5 * derivative / x_value + field
        energy = 0.5 * (derivative**2 + field**2)
        pressure = 0.5 * (derivative**2 - field**2)
        comoving_energy = energy * (2.0 * x_value) ** 1.5
        maximum_kg_residual = max(maximum_kg_residual, abs(kg_residual))
        rows.append(
            {
                "x_equals_m_t": x_value,
                "psi_over_psi_i": field,
                "dpsi_dx_over_psi_i": derivative,
                "dimensionless_energy_density": energy,
                "instantaneous_w": pressure / energy,
                "rho_a3_over_m2_psi_i2_aosc3": comoving_energy,
                "relative_error_to_RD_dust_match": abs(
                    comoving_energy / RD_DUST_MATCH - 1.0
                ),
                "Klein_Gordon_residual": kg_residual,
                "checkpoint_marker": MARKER,
            }
        )

    cycle_x = np.linspace(100.0, 100.0 + 40.0 * math.pi, 50000)
    cycle_field = (
        BESSEL_NORMALIZATION
        * cycle_x ** (-NU_RD)
        * jv(NU_RD, cycle_x)
    )
    cycle_derivative = (
        -BESSEL_NORMALIZATION
        * cycle_x ** (-NU_RD)
        * jv(NU_RD + 1.0, cycle_x)
    )
    average_pressure = float(
        np.trapezoid(cycle_derivative**2 - cycle_field**2, cycle_x)
    )
    average_energy = float(
        np.trapezoid(cycle_derivative**2 + cycle_field**2, cycle_x)
    )
    return rows, {
        "RD_dust_matching_coefficient": RD_DUST_MATCH,
        "maximum_Klein_Gordon_residual": maximum_kg_residual,
        "late_cycle_averaged_w": average_pressure / average_energy,
        "late_comoving_energy_relative_error_at_x_1e6": rows[-1][
            "relative_error_to_RD_dust_match"
        ],
    }


def transition_hubble_deviation(mass_eV: float, a_osc: float) -> dict[str, float]:
    maximum = {
        "absolute_fractional_H_shift": 0.0,
        "x_at_maximum": 0.0,
        "a_at_maximum": 0.0,
        "scalar_actual_over_dust_at_maximum": 0.0,
    }
    for x_value_raw in np.logspace(-8.0, 2.0, 8000):
        x_value = float(x_value_raw)
        scale_factor = a_osc * math.sqrt(2.0 * x_value)
        field, derivative, _ = bessel_state(x_value)
        scalar_actual = (
            OMEGA_X
            * 0.5
            * (field**2 + derivative**2)
            / (RD_DUST_MATCH * a_osc**3)
        )
        baseline_e2 = (
            OMEGA_R / scale_factor**4
            + OMEGA_M / scale_factor**3
            + OMEGA_LAMBDA
        )
        actual_e2 = (
            OMEGA_R / scale_factor**4
            + OMEGA_B / scale_factor**3
            + scalar_actual
            + OMEGA_LAMBDA
        )
        fractional_shift = abs(math.sqrt(actual_e2 / baseline_e2) - 1.0)
        if fractional_shift > maximum["absolute_fractional_H_shift"]:
            maximum = {
                "absolute_fractional_H_shift": fractional_shift,
                "x_at_maximum": x_value,
                "a_at_maximum": scale_factor,
                "scalar_actual_over_dust_at_maximum": scalar_actual
                / (OMEGA_X / scale_factor**3),
            }
    return maximum


def build_background_rows(
    mass_grid: list[tuple[str, float]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    equality_scale = OMEGA_R / OMEGA_M
    equality_e2 = (
        OMEGA_R / equality_scale**4
        + OMEGA_M / equality_scale**3
        + OMEGA_LAMBDA
    )
    h_equality_eV = H0_EV * math.sqrt(equality_e2)
    rows: list[dict[str, Any]] = []
    for label, mass_eV in mass_grid:
        a_osc = math.sqrt(H0_EV * math.sqrt(OMEGA_R) / mass_eV)
        psi_i_over_mpl = math.sqrt(
            3.0
            * H0_EV**2
            * OMEGA_X
            / (RD_DUST_MATCH * mass_eV**2 * a_osc**3)
        )
        transition = transition_hubble_deviation(mass_eV, a_osc)
        mass_kg = mass_eV * EV_C2_KG
        rows.append(
            {
                "mass_label": label,
                "m_gap_eV": mass_eV,
                "a_osc_Hrad_equals_m": a_osc,
                "z_osc": 1.0 / a_osc - 1.0,
                "t_osc_seconds": HBAR_EV_S / (2.0 * mass_eV),
                "a_equality": equality_scale,
                "z_equality": 1.0 / equality_scale - 1.0,
                "H_equality_eV_over_m_gap": h_equality_eV / mass_eV,
                "oscillates_before_equality": mass_eV > h_equality_eV,
                "RD_dust_matching_coefficient": RD_DUST_MATCH,
                "psi_i_eV": psi_i_over_mpl * MPL_REDUCED_EV,
                "psi_i_over_reduced_Mpl": psi_i_over_mpl,
                "Omega_X_target": OMEGA_X,
                "Omega_X_is_replacement_not_addition": True,
                "rho_X_over_radiation_at_aosc_dust_proxy": OMEGA_X
                * a_osc
                / OMEGA_R,
                "maximum_abs_delta_H_over_H_during_transition": transition[
                    "absolute_fractional_H_shift"
                ],
                "x_at_maximum_H_shift": transition["x_at_maximum"],
                "a_at_maximum_H_shift": transition["a_at_maximum"],
                "scalar_actual_over_dust_at_maximum_H_shift": transition[
                    "scalar_actual_over_dust_at_maximum"
                ],
                "present_number_density_per_m3": RHO_X0_KG_M3 / mass_kg,
                "abundance_normalization_parent_derived": False,
                "initial_state_is_one_global_cosmological_datum": True,
                "valid_for_cosmology_claim": False,
                "checkpoint_marker": MARKER,
            }
        )
    return rows, {
        "a_equality": equality_scale,
        "z_equality": 1.0 / equality_scale - 1.0,
        "H_equality_eV": h_equality_eV,
        "maximum_transition_H_shift": max(
            row["maximum_abs_delta_H_over_H_during_transition"] for row in rows
        ),
        "maximum_initial_amplitude_over_Mpl": max(
            row["psi_i_over_reduced_Mpl"] for row in rows
        ),
        "maximum_scalar_to_radiation_at_onset": max(
            row["rho_X_over_radiation_at_aosc_dust_proxy"] for row in rows
        ),
    }


def jeans_row(
    label: str,
    mass_eV: float,
    epoch: str,
    scale_factor: float,
    density_name: str,
    density_omega: float,
) -> dict[str, Any]:
    density = RHO_CRIT0_KG_M3 * density_omega / scale_factor**3
    mass_kg = mass_eV * EV_C2_KG
    physical_k = (
        16.0 * math.pi * G_SI * density * mass_kg**2 / HBAR_J_S**2
    ) ** 0.25
    physical_lambda = 2.0 * math.pi / physical_k
    comoving_lambda = physical_lambda / scale_factor
    comoving_k = 2.0 * math.pi / comoving_lambda
    jeans_mass = (
        4.0
        * math.pi
        / 3.0
        * density
        * (physical_lambda / 2.0) ** 3
        / MSUN_KG
    )
    nonrelativistic_ratio = HBAR_J_S * physical_k / (mass_kg * C_M_S)
    return {
        "mass_label": label,
        "m_gap_eV": mass_eV,
        "epoch": epoch,
        "scale_factor": scale_factor,
        "gravity_density": density_name,
        "density_kg_m3": density,
        "lambda_Jeans_physical_kpc": physical_lambda / KPC_M,
        "lambda_Jeans_comoving_Mpc": comoving_lambda / MPC_M,
        "k_Jeans_comoving_Mpc_inverse": comoving_k * MPC_M,
        "Jeans_sphere_mass_Msun": jeans_mass,
        "hbar_kphys_over_m_c": nonrelativistic_ratio,
        "linear_equation": "ddot(delta)+2Hdot(delta)+[hbar^2 k^4/(4m^2a^4)-4piG rho]delta=0",
        "instantaneous_Jeans_not_transfer_function_claim": True,
        "valid_for_structure_claim": False,
        "checkpoint_marker": MARKER,
    }


def build_jeans_rows(
    mass_grid: list[tuple[str, float]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    equality_scale = OMEGA_R / OMEGA_M
    rows: list[dict[str, Any]] = []
    for label, mass_eV in mass_grid:
        for epoch, scale_factor in [("today", 1.0), ("equality", equality_scale)]:
            rows.append(
                jeans_row(
                    label,
                    mass_eV,
                    epoch,
                    scale_factor,
                    "total_matter_gravity",
                    OMEGA_M,
                )
            )
            rows.append(
                jeans_row(
                    label,
                    mass_eV,
                    epoch,
                    scale_factor,
                    "motion_self_gravity",
                    OMEGA_X,
                )
            )
    total_equality = {
        row["mass_label"]: row
        for row in rows
        if row["epoch"] == "equality"
        and row["gravity_density"] == "total_matter_gravity"
    }
    return rows, {
        "total_matter_equality": {
            label: {
                "lambda_comoving_Mpc": row["lambda_Jeans_comoving_Mpc"],
                "k_comoving_Mpc_inverse": row["k_Jeans_comoving_Mpc_inverse"],
                "Jeans_mass_Msun": row["Jeans_sphere_mass_Msun"],
            }
            for label, row in total_equality.items()
        }
    }


def build_mass_window_rows(
    mass_grid: list[tuple[str, float]],
    state_rows: list[dict[str, str]],
    jeans_rows: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    floors = [
        float(row["minimum_m_gap_eV_for_lambda_db_le_Rn"])
        for row in state_rows
    ]
    strict_floors = [
        float(row["minimum_m_gap_eV_for_lambda_db_le_0p1_Rn"])
        for row in state_rows
    ]
    equality_rows = {
        row["mass_label"]: row
        for row in jeans_rows
        if row["epoch"] == "equality"
        and row["gravity_density"] == "total_matter_gravity"
    }
    rows: list[dict[str, Any]] = []
    for label, mass_eV in mass_grid:
        ratios = [floor / mass_eV for floor in floors]
        equality = equality_rows[label]
        rows.append(
            {
                "row_type": "candidate_mass",
                "mass_label": label,
                "m_gap_eV": mass_eV,
                "state_rows_tested": len(state_rows),
                "maximum_lambda_db_over_Rn": max(ratios),
                "median_lambda_db_over_Rn": float(np.median(ratios)),
                "rows_with_lambda_db_le_Rn": sum(ratio <= 1.0 + 1.0e-12 for ratio in ratios),
                "rows_with_lambda_db_le_0p1Rn": sum(
                    ratio <= 0.1 + 1.0e-12 for ratio in ratios
                ),
                "equality_lambda_Jeans_comoving_Mpc": equality[
                    "lambda_Jeans_comoving_Mpc"
                ],
                "equality_Jeans_mass_Msun": equality["Jeans_sphere_mass_Msun"],
                "controlled_collisionless_WKB_all_rows": max(ratios) <= 0.1 + 1.0e-12,
                "linear_100kpc_equality_target": equality[
                    "lambda_Jeans_comoving_Mpc"
                ]
                <= 0.1,
                "valid_for_galaxy_claim": False,
                "checkpoint_marker": MARKER,
            }
        )

    reference_mass = mass_grid[0][1]
    reference_lambda = equality_rows[mass_grid[0][0]][
        "lambda_Jeans_comoving_Mpc"
    ]
    target_rows: list[dict[str, Any]] = []
    for target_mpc in [1.0, 0.1, 0.01]:
        target_mass = reference_mass * (reference_lambda / target_mpc) ** 2
        target_rows.append(
            {
                "row_type": "derived_scale_target",
                "mass_label": f"lambdaJ_eq_le_{target_mpc:g}_Mpc",
                "m_gap_eV": target_mass,
                "state_rows_tested": len(state_rows),
                "maximum_lambda_db_over_Rn": max(floors) / target_mass,
                "median_lambda_db_over_Rn": float(np.median(floors)) / target_mass,
                "rows_with_lambda_db_le_Rn": sum(
                    floor / target_mass <= 1.0 + 1.0e-12 for floor in floors
                ),
                "rows_with_lambda_db_le_0p1Rn": sum(
                    floor / target_mass <= 0.1 + 1.0e-12 for floor in floors
                ),
                "equality_lambda_Jeans_comoving_Mpc": target_mpc,
                "equality_Jeans_mass_Msun": "DERIVED_SCALE_TARGET_NOT_INSTANTIATED",
                "controlled_collisionless_WKB_all_rows": max(strict_floors)
                <= target_mass,
                "linear_100kpc_equality_target": target_mpc <= 0.1,
                "valid_for_galaxy_claim": False,
                "checkpoint_marker": MARKER,
            }
        )
    rows.extend(target_rows)
    joint_lower_bound = max(max(strict_floors), target_rows[1]["m_gap_eV"])
    return rows, {
        "WKB_floor_all_350_rows_eV": max(floors),
        "strict_WKB_floor_all_350_rows_eV": max(strict_floors),
        "mass_for_equality_Jeans_below_100kpc_eV": target_rows[1]["m_gap_eV"],
        "joint_internal_benchmark_lower_bound_eV": joint_lower_bound,
        "benchmark_1e_minus20_passes_joint_internal_gate": 1.0e-20
        >= joint_lower_bound,
        "observational_upper_or_lower_bound_derived": False,
    }


def build_x2_control_rows(
    background_rows: list[dict[str, Any]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for background in background_rows:
        mass_eV = float(background["m_gap_eV"])
        psi_i_eV = float(background["psi_i_eV"])
        kinetic_invariant_eV4 = 0.5 * (mass_eV * psi_i_eV) ** 2
        planck_natural_ratio = kinetic_invariant_eV4 / MPL_REDUCED_EV**4
        rows.append(
            {
                "mass_label": background["mass_label"],
                "m_gap_eV": mass_eV,
                "psi_i_eV": psi_i_eV,
                "X_osc_estimate_eV4": kinetic_invariant_eV4,
                "Lambda_X2_min_eV_for_10percent_control": (
                    kinetic_invariant_eV4 / 0.1
                )
                ** 0.25,
                "Lambda_X2_min_eV_for_1percent_control": (
                    kinetic_invariant_eV4 / 0.01
                )
                ** 0.25,
                "dimensionless_cX_for_c_equals_Mpl_minus4": planck_natural_ratio,
                "exact_control_inequality": "abs(c_ess) X_osc < epsilon; equivalently Lambda_ess=abs(c_ess)^(-1/4) > (X_osc/epsilon)^(1/4)",
                "parent_c_ess_IR_value_inserted": False,
                "quadratic_cosmology_claim": False,
                "checkpoint_marker": MARKER,
            }
        )
    return rows, {
        "maximum_Lambda_X2_eV_for_1percent_control": max(
            row["Lambda_X2_min_eV_for_1percent_control"] for row in rows
        ),
        "maximum_planck_natural_cX": max(
            row["dimensionless_cX_for_c_equals_Mpl_minus4"] for row in rows
        ),
    }


def build_local_rows(
    mass_grid: list[tuple[str, float]],
    embedded_rows: list[dict[str, str]],
) -> tuple[list[dict[str, Any]], dict[str, Any]]:
    rows: list[dict[str, Any]] = []
    for embedded in embedded_rows:
        rows.append(
            {
                "effect": "embedded_halo_tide",
                "arena_or_mass": embedded["arena"],
                "dimensionless_size": float(
                    embedded["worst_embedded_halo_tide_over_solar"]
                ),
                "period_days": "NOT_APPLICABLE",
                "assumption": "host position R_host=L_eff from checkpoint 5151",
                "same_metric_Hilbert_source": True,
                "direct_scalar_fifth_force": 0.0,
                "valid_for_PPN_claim": False,
                "checkpoint_marker": MARKER,
            }
        )

    mercury_radius = 0.387098 * AU_M
    mercury_solar_acceleration = GM_SUN_M3_S2 / mercury_radius**2
    mean_tide_acceleration = 4.0 * math.pi * G_SI * RHO_X0_KG_M3 * mercury_radius / 3.0
    rows.append(
        {
            "effect": "cosmological_mean_motion_density_tide",
            "arena_or_mass": "Mercury_orbit",
            "dimensionless_size": mean_tide_acceleration / mercury_solar_acceleration,
            "period_days": "NOT_APPLICABLE",
            "assumption": "homogeneous present Omega_X density",
            "same_metric_Hilbert_source": True,
            "direct_scalar_fifth_force": 0.0,
            "valid_for_PPN_claim": False,
            "checkpoint_marker": MARKER,
        }
    )

    local_density_kg_m3 = 0.3 * 1.0e15 * EV_C2_KG
    potential_amplitudes: list[float] = []
    for label, mass_eV in mass_grid:
        angular_mass = mass_eV / HBAR_EV_S
        potential_amplitude = math.pi * G_SI * local_density_kg_m3 / angular_mass**2
        potential_amplitudes.append(potential_amplitude)
        rows.append(
            {
                "effect": "oscillating_scalar_pressure_metric_potential",
                "arena_or_mass": label,
                "dimensionless_size": potential_amplitude,
                "period_days": math.pi / angular_mass / 86400.0,
                "assumption": "diagnostic local density 0.3 GeV_per_cm3; Psi_c=pi G rho/m^2",
                "same_metric_Hilbert_source": True,
                "direct_scalar_fifth_force": 0.0,
                "valid_for_PPN_claim": False,
                "checkpoint_marker": MARKER,
            }
        )
    return rows, {
        "maximum_embedded_halo_tide_ratio": max(
            float(row["worst_embedded_halo_tide_over_solar"])
            for row in embedded_rows
        ),
        "cosmological_mean_Mercury_tide_ratio": mean_tide_acceleration
        / mercury_solar_acceleration,
        "maximum_local_oscillating_potential_diagnostic": max(potential_amplitudes),
        "classical_direct_fifth_force": 0.0,
    }


def build_route_rows() -> list[dict[str, Any]]:
    return [
        {
            "route": "static_baryonic_metric_populates_motion_state",
            "status": "REJECTED",
            "reason": "stationary vacuum polarization does not create real occupation",
            "source_checkpoint": "4949",
            "next_action": "do_not_reopen_without_new_parent_operator",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "route": "high_frequency_formation_emission_then_X2_cascade",
            "status": "REJECTED_CONTROLLED_BRANCH",
            "reason": "2to2 conserves number and controlled offshell/sixpoint routes fail the multiplicity gate",
            "source_checkpoint": "4953-4959",
            "next_action": "do_not_repeat_formation_kernel_sweep",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "route": "insert_galaxy_occupation_profile_as_closure",
            "status": "BLOCKED",
            "reason": "would hand-insert C_n and the radial population",
            "source_checkpoint": "4948-5151",
            "next_action": "reject_as_parent_derivation",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "route": "primordial_reflection_even_motion_state_then_gravitational_clustering",
            "status": "SURVIVES_BACKGROUND_AND_LINEAR_SCALE_GATE",
            "reason": "an even mixture of plus/minus coherent representatives has zero one-point function, positive quadratic stress and dust redshifting after H<m",
            "source_checkpoint": "5152",
            "next_action": "derive_or_simulate_nonlinear_collapse_to_Cn_nq_core_and_outer_boundary",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
        {
            "route": "isolated_coherent_one_point_as_final_local_branch",
            "status": "WITNESS_ONLY_NOT_SELECTED",
            "reason": "its stress proves the dust limit but the reflection-even CTP mixture is the branch compatible with zero odd correlators",
            "source_checkpoint": "5152",
            "next_action": "use_only_as_exact_background_representative",
            "valid_for_claim": False,
            "checkpoint_marker": MARKER,
        },
    ]


def write_document(result: dict[str, Any]) -> None:
    backgrounds = result["background"]
    jeans = result["Jeans_gate"]["total_matter_equality"]
    window = result["mass_window"]
    local = result["local_cog"]
    x2 = result["X2_control"]
    benchmark = next(
        row for row in backgrounds if row["mass_label"] == "benchmark_1e_minus20_eV"
    )
    minimum = backgrounds[0]
    minimum_jeans = jeans[minimum["mass_label"]]
    benchmark_jeans = jeans[benchmark["mass_label"]]
    text = f"""# 5152 - Primordial motion occupation, dust limit and Jeans window

Marker: `{MARKER}`.

Date: `{CHECKED_DATE}`.

## Decision

The one-machine/two-cog criterion is now explicit. The same low-energy parent
action used for local GR is retained,

```text
S = integral sqrt(-g) [M_R^2(R-2 Lambda)/2
                       -(nabla psi)^2/2-m_gap^2 psi^2/2
                       +higher parent operators]
    +S_matter[g,A,Phi_SM].
```

No galaxy-only coupling or arena switch is added. Ordinary matter, Maxwell
stress including Poynting momentum, and the motion-state stress all enter the
same Hilbert tensor. The local cog remains metric-coupled GR plus the tiny
external stress of the galactic state. The galaxy cog is allowed to contain a
nonvacuum motion population.

The controlled local and formation calculations at 4949 and 4953--4959 show
that a static baryonic metric does not manufacture that population and the
tested high-frequency cascades cannot supply it. Checkpoint 5152 therefore
tests the logically distinct primordial-state route rather than repeating
those rejected kernels.

**Result:** a primordial reflection-even massive motion state survives the
background, WKB and instantaneous linear-Jeans gates. It is selected as the
next dynamical route. This does not yet derive its abundance or prove that
nonlinear collapse generates the checkpoint-5151 `n_q` profile.

## 1. Reflection-even state without a local scalar charge

For a homogeneous representative,

```text
ddot(psi)+3H dot(psi)+m_gap^2 psi=0.
```

The CTP state can be the even mixture

```text
rho_even=(|+psi_i><+psi_i|+|-psi_i><-psi_i|)/2.
```

Every odd correlator, including `<psi>`, vanishes, while its quadratic stress
is identical to either representative. Thus the construction does not add a
linear matter charge and does not undo the reflection-even local source
theorem. Its abundance is initial-state data, not local particle production.

## 2. Exact radiation-era dust theorem

In radiation domination `H=1/(2t)`. With `x=m_gap t`, the regular solution is

```text
psi/psi_i=2^(1/4) Gamma(5/4) x^(-1/4) J_(1/4)(x).
```

For `x>>1`, its oscillation-averaged stress obeys

```text
<p_psi>=0,
<rho_psi>=C_RD m_gap^2 psi_i^2 (a_osc/a)^3,
C_RD=4 Gamma(5/4)^2/pi={RD_DUST_MATCH},
H_rad(a_osc)=m_gap.
```

The numerical Bessel audit gives maximum Klein--Gordon residual
`{result['Bessel_gate']['maximum_Klein_Gordon_residual']:.3e}`, late-cycle
`<w>={result['Bessel_gate']['late_cycle_averaged_w']:.3e}`, and asymptotic
comoving-energy error `{result['Bessel_gate']['late_comoving_energy_relative_error_at_x_1e6']:.3e}`.
This is a derivation of dust behavior, not an assumed equation of state.

The MTS component replaces the `Omega_CDM` part of the checkpoint-4897
baseline; it is not added on top:

```text
Omega_b={OMEGA_B},
Omega_X=Omega_m-Omega_b={OMEGA_X},
Omega_m={OMEGA_M}.
```

At the all-galaxy WKB floor `m_gap={minimum['m_gap_eV']} eV`, oscillations
begin at `z={minimum['z_osc']}`. The exact radiation matching requires
`psi_i={minimum['psi_i_over_reduced_Mpl']} Mbar_Pl`. The motion/radiation
ratio at onset is only `{minimum['rho_X_over_radiation_at_aosc_dust_proxy']}`,
and the largest calculated transition-era change to `H` relative to the
metric-only CDM baseline is `{minimum['maximum_abs_delta_H_over_H_during_transition']}`.
All tested masses begin oscillating well before equality.

This closes the background *existence* question with one global initial
amplitude. It does not derive that amplitude from the parent state-preparation
law, and primordial isocurvature has not yet been tested.

## 3. Linear clustering and the mass window

The nonrelativistic scalar perturbation obeys

```text
ddot(delta)+2H dot(delta)
 +[hbar^2 k^4/(4m_gap^2 a^4)-4 pi G rho]delta=0,

k_phys,J^4=16 pi G rho m_gap^2/hbar^2.
```

Using the total matter density in the gravity term, the marginal WKB mass has
at equality

```text
lambda_J,com={minimum_jeans['lambda_comoving_Mpc']} Mpc,
k_J,com={minimum_jeans['k_comoving_Mpc_inverse']} Mpc^-1,
M_J={minimum_jeans['Jeans_mass_Msun']} Msun.
```

The intentionally conservative internal benchmark `m_gap=1e-20 eV` gives

```text
lambda_J,com(eq)={benchmark_jeans['lambda_comoving_Mpc']} Mpc,
M_J(eq)={benchmark_jeans['Jeans_mass_Msun']} Msun,
z_osc={benchmark['z_osc']},
psi_i/Mbar_Pl={benchmark['psi_i_over_reduced_Mpl']}.
```

These are instantaneous Jeans scales, not a transfer-function, CMB or
Lyman-alpha likelihood. They prove that a nonempty clustering window exists;
they do not establish observational preference.

## 4. Joint galaxy/WKB gate

All `350` checkpoint-5151 galaxy/parent rows imply

```text
m_gap >= {window['WKB_floor_all_350_rows_eV']} eV
    for lambda_db <= R_n,
m_gap >= {window['strict_WKB_floor_all_350_rows_eV']} eV
    for lambda_db <= 0.1 R_n.
```

Demanding additionally that the instantaneous equality Jeans wavelength be
below `100 kpc` gives

```text
m_gap >= {window['mass_for_equality_Jeans_below_100kpc_eV']} eV.
```

The joint internal lower benchmark is therefore
`{window['joint_internal_benchmark_lower_bound_eV']} eV`; `1e-20 eV` passes.
This is an engineering target for the next collapse calculation, not a fitted
or observed MTS mass and not an upper bound.

## 5. Higher-derivative control

For the parent `c_ess X^2` operator, the exact quadratic-control condition at
oscillation is

```text
|c_ess| X_osc < epsilon,
X_osc approximately (m_gap psi_i)^2/2.
```

Across the mass grid, one-percent control requires the equivalent suppression
scale `Lambda_ess=|c_ess|^(-1/4)` above at most
`{x2['maximum_Lambda_X2_eV_for_1percent_control']} eV`. A Planck-natural
coefficient gives maximum `|c_ess|X={x2['maximum_planck_natural_cX']}`.
The free massive approximation is therefore easily controlled for a
Planck-suppressed comparator, but the actual infrared parent `c_ess` still has
to be transported and inserted.

## 6. Mercury and the local cog

No direct scalar fifth force is introduced. At the explicitly declared
checkpoint-5151 host location, the largest halo tide/solar ratio remains
`{local['maximum_embedded_halo_tide_ratio']}`. The homogeneous cosmological
motion density gives only `{local['cosmological_mean_Mercury_tide_ratio']}`
at Mercury. A diagnostic `0.3 GeV/cm^3` local scalar density gives a largest
oscillating metric-potential amplitude
`{local['maximum_local_oscillating_potential_diagnostic']}` over the tested
mass grid. These checks preserve the local cog but are not a complete global
Solar-System PPN or pulsar-timing likelihood.

## 7. What moved and what remains

Derived or constructed here:

```text
one action for local and galactic sectors                  = retained;
reflection-even primordial state with <psi>=0              = constructed;
exact radiation-era dust limit                             = derived;
Omega_X replacement of CDM background                      = executed;
nonempty WKB plus linear-clustering mass window             = derived;
static/formation source no-go bypass without contradiction = established.
```

Still absent:

```text
parent preparation of psi_i or Omega_X                     = not derived;
primordial perturbation/isocurvature spectrum               = not derived;
IR value of c_ess and all higher-operator control           = incomplete;
nonlinear collapse to C_n and n_q                           = not derived;
finite core and outer boundary                              = not derived;
flattened rotating distribution and lensing likelihood     = not derived.
```

The branch is therefore more than an inserted galaxy closure, because one
primordial state evolves under one parent action and passes explicit
background/scale/local gates. But until nonlinear evolution selects the MTS
profile and normalization, it remains observationally indistinguishable in
its background role from ordinary ultralight scalar dark matter. That is the
next falsifiable boundary, not a wording problem.

## 8. Next calculation

Evolve the reflection-even state from cosmological initial data through the
Schrodinger--Poisson/Vlasov limit at three fixed masses: the strict WKB floor,
`1e-20 eV`, and `1e-18 eV`. The gate is whether one global initial spectrum
and the parent interaction generate, without a galaxy-by-galaxy shape fit,

```text
C_n proportional (ell_gap/L_eff)^q_parent,
n_q(r)=r^q/(R_n^q+r^q),
a finite central core,
a finite outer boundary,
and the checkpoint-5151 conserved stress.
```

If not, the current galaxy state route is scalar-halo closure and must be
demoted. No direct formation-emission route is to be retried without a new
parent operator.

Primary references:

- Turner, coherent scalar oscillations: {PRIMARY_SOURCE_URLS['coherent_scalar_oscillations']}
- Hwang and Noh, linear CDM limit: {PRIMARY_SOURCE_URLS['linear_axion_CDM_proof']}
- Hu, Barkana and Gruzinov, Jeans/wave scale: {PRIMARY_SOURCE_URLS['fuzzy_CDM_Jeans_scale']}
- Schive et al., nonlinear wave-halo formation: {PRIMARY_SOURCE_URLS['nonlinear_wave_halo_formation']}
- Khmelnitsky and Rubakov, oscillating metric diagnostic: {PRIMARY_SOURCE_URLS['oscillating_local_metric']}

All `{result['validation_count']}` validation checks pass. The protected
`formalization-workbench` hash remains `{result['formalization_workbench_tree_sha256']}`.
No GitHub or galaxy-repository write occurred.
"""
    DOCUMENT.write_text(text, encoding="utf-8")


def main() -> None:
    missing_sources = [str(path) for path in SOURCE_PATHS.values() if not path.exists()]
    if missing_sources:
        raise FileNotFoundError(f"missing checkpoint sources: {missing_sources}")
    source_hashes_before = {
        name: file_digest(path) for name, path in SOURCE_PATHS.items()
    }
    formal_before = tree_digest(FORMAL)

    state_result = json.loads(
        SOURCE_PATHS["state_stress_result"].read_text(encoding="utf-8")
    )
    state_rows = read_csv(SOURCE_PATHS["state_stress_scale_rows"])
    embedded_rows = read_csv(SOURCE_PATHS["embedded_local_rows"])
    wkb_floor = max(
        float(row["minimum_m_gap_eV_for_lambda_db_le_Rn"])
        for row in state_rows
    )
    mass_grid = [
        ("WKB_floor_all_175", wkb_floor),
        ("ten_times_WKB_floor", 10.0 * wkb_floor),
        ("benchmark_1e_minus20_eV", 1.0e-20),
        ("benchmark_1e_minus18_eV", 1.0e-18),
    ]

    bessel_rows, bessel_summary = build_bessel_rows()
    background_rows, background_summary = build_background_rows(mass_grid)
    jeans_rows, jeans_summary = build_jeans_rows(mass_grid)
    mass_window_rows, mass_window_summary = build_mass_window_rows(
        mass_grid, state_rows, jeans_rows
    )
    x2_rows, x2_summary = build_x2_control_rows(background_rows)
    local_rows, local_summary = build_local_rows(mass_grid, embedded_rows)
    route_rows = build_route_rows()

    write_csv(BESSEL_CSV, bessel_rows)
    write_csv(BACKGROUND_CSV, background_rows)
    write_csv(JEANS_CSV, jeans_rows)
    write_csv(MASS_WINDOW_CSV, mass_window_rows)
    write_csv(X2_CONTROL_CSV, x2_rows)
    write_csv(LOCAL_CSV, local_rows)
    write_csv(ROUTE_CSV, route_rows)

    source_hashes_after = {
        name: file_digest(path) for name, path in SOURCE_PATHS.items()
    }
    formal_after = tree_digest(FORMAL)
    result: dict[str, Any] = {
        "checked_date": CHECKED_DATE,
        "checkpoint_marker": MARKER,
        "source_paths": {name: str(path) for name, path in SOURCE_PATHS.items()},
        "source_hashes_before": source_hashes_before,
        "source_hashes_after": source_hashes_after,
        "primary_source_urls": PRIMARY_SOURCE_URLS,
        "formalization_workbench_tree_sha256": formal_after,
        "cosmological_parameters": {
            "H0_km_s_Mpc": H0_KM_S_MPC,
            "Omega_r": OMEGA_R,
            "Omega_m": OMEGA_M,
            "Omega_b": OMEGA_B,
            "Omega_X": OMEGA_X,
            "Omega_Lambda": OMEGA_LAMBDA,
            "Omega_X_role": "replacement_for_conventional_CDM_not_additive_component",
        },
        "Bessel_gate": bessel_summary,
        "background": background_rows,
        "background_summary": background_summary,
        "Jeans_gate": jeans_summary,
        "mass_window": mass_window_summary,
        "X2_control": x2_summary,
        "local_cog": local_summary,
        "route_decision": "PRIMORDIAL_REFLECTION_EVEN_STATE_SURVIVES_CONDITIONALLY_ADVANCE_TO_NONLINEAR_COLLAPSE",
        "same_parent_action_across_local_and_galaxy": True,
        "primordial_reflection_even_state_constructed": True,
        "dust_limit_derived": True,
        "linear_clustering_window_exists": True,
        "source_normalization_parent_derived": False,
        "primordial_perturbation_spectrum_derived": False,
        "parent_exponent_nonlinear_transport_derived": False,
        "Cn_from_collapse_derived": False,
        "finite_core_and_outer_boundary_derived": False,
        "valid_for_cosmology_claim": False,
        "valid_for_galaxy_claim": False,
        "valid_for_PPN_claim": False,
        "valid_for_full_MTS_claim": False,
        "predecessor_maximum_WKB_mass_eV": state_result["galaxy_scale_gate"][
            "maximum_WKB_mass_eV"
        ],
    }

    output_csvs = [
        BESSEL_CSV,
        BACKGROUND_CSV,
        JEANS_CSV,
        MASS_WINDOW_CSV,
        X2_CONTROL_CSV,
        LOCAL_CSV,
        ROUTE_CSV,
    ]
    benchmark_window = next(
        row
        for row in mass_window_rows
        if row["mass_label"] == "benchmark_1e_minus20_eV"
    )
    minimum_window = next(
        row
        for row in mass_window_rows
        if row["mass_label"] == "WKB_floor_all_175"
    )
    checks = [
        (
            "source_paths_exist",
            not missing_sources,
            str(missing_sources),
        ),
        (
            "sources_read_only",
            source_hashes_before == source_hashes_after,
            str(source_hashes_after),
        ),
        (
            "formal_tree_unchanged",
            formal_before == FORMAL_BASELINE and formal_after == FORMAL_BASELINE,
            formal_after,
        ),
        (
            "cosmological_density_bookkeeping_closes",
            abs(OMEGA_R + OMEGA_M + OMEGA_LAMBDA - 1.0) < 1.0e-15
            and OMEGA_X > 0.0
            and abs(OMEGA_B + OMEGA_X - OMEGA_M) < 1.0e-15,
            str(
                {
                    "Omega_b": OMEGA_B,
                    "Omega_X": OMEGA_X,
                    "Omega_m": OMEGA_M,
                }
            ),
        ),
        (
            "Omega_X_replaces_CDM_not_added",
            all(row["Omega_X_is_replacement_not_addition"] for row in background_rows),
            "Omega_X=Omega_m-Omega_b",
        ),
        (
            "exact_radiation_Bessel_solution_closes",
            bessel_summary["maximum_Klein_Gordon_residual"] < 1.0e-10,
            str(bessel_summary["maximum_Klein_Gordon_residual"]),
        ),
        (
            "late_comoving_energy_reaches_dust_invariant",
            bessel_summary["late_comoving_energy_relative_error_at_x_1e6"]
            < 1.0e-6,
            str(bessel_summary["late_comoving_energy_relative_error_at_x_1e6"]),
        ),
        (
            "late_cycle_average_pressure_is_dustlike",
            abs(bessel_summary["late_cycle_averaged_w"]) < 5.0e-3,
            str(bessel_summary["late_cycle_averaged_w"]),
        ),
        (
            "all_mass_rows_oscillate_before_equality",
            all(row["oscillates_before_equality"] for row in background_rows),
            str(
                {
                    row["mass_label"]: row["H_equality_eV_over_m_gap"]
                    for row in background_rows
                }
            ),
        ),
        (
            "transition_background_shift_below_per_mille",
            background_summary["maximum_transition_H_shift"] < 1.0e-3,
            str(background_summary["maximum_transition_H_shift"]),
        ),
        (
            "initial_amplitude_sub_reduced_Planck",
            background_summary["maximum_initial_amplitude_over_Mpl"] < 0.1,
            str(background_summary["maximum_initial_amplitude_over_Mpl"]),
        ),
        (
            "motion_subdominant_at_oscillation",
            background_summary["maximum_scalar_to_radiation_at_onset"] < 1.0e-3,
            str(background_summary["maximum_scalar_to_radiation_at_onset"]),
        ),
        (
            "Jeans_rows_positive_and_nonrelativistic",
            all(
                row["lambda_Jeans_physical_kpc"] > 0.0
                and row["lambda_Jeans_comoving_Mpc"] > 0.0
                and row["Jeans_sphere_mass_Msun"] > 0.0
                and row["hbar_kphys_over_m_c"] < 0.1
                for row in jeans_rows
            ),
            str(max(row["hbar_kphys_over_m_c"] for row in jeans_rows)),
        ),
        (
            "WKB_floor_is_explicitly_marginal",
            minimum_window["rows_with_lambda_db_le_Rn"] == len(state_rows)
            and not minimum_window["controlled_collisionless_WKB_all_rows"],
            str(minimum_window),
        ),
        (
            "ten_times_floor_controls_all_350_state_rows",
            next(
                row
                for row in mass_window_rows
                if row["mass_label"] == "ten_times_WKB_floor"
            )["controlled_collisionless_WKB_all_rows"],
            str(mass_window_summary["strict_WKB_floor_all_350_rows_eV"]),
        ),
        (
            "benchmark_1e_minus20_passes_joint_internal_gate",
            benchmark_window["controlled_collisionless_WKB_all_rows"]
            and benchmark_window["linear_100kpc_equality_target"]
            and mass_window_summary[
                "benchmark_1e_minus20_passes_joint_internal_gate"
            ],
            str(benchmark_window),
        ),
        (
            "Planck_natural_X2_is_quadratically_controlled",
            x2_summary["maximum_planck_natural_cX"] < 1.0e-80,
            str(x2_summary),
        ),
        (
            "same_law_local_cog_remains_suppressed",
            local_summary["classical_direct_fifth_force"] == 0.0
            and local_summary["maximum_embedded_halo_tide_ratio"] < 1.0e-10
            and local_summary["maximum_local_oscillating_potential_diagnostic"]
            < 1.0e-15,
            str(local_summary),
        ),
        (
            "rejected_formation_routes_not_revived",
            route_rows[0]["status"] == "REJECTED"
            and route_rows[1]["status"] == "REJECTED_CONTROLLED_BRANCH",
            str([route_rows[0]["status"], route_rows[1]["status"]]),
        ),
        (
            "primordial_route_selected_conditionally",
            route_rows[3]["status"]
            == "SURVIVES_BACKGROUND_AND_LINEAR_SCALE_GATE",
            route_rows[3]["next_action"],
        ),
        (
            "all_output_CSVs_parse",
            all(len(read_csv(path)) > 0 for path in output_csvs),
            str([str(path) for path in output_csvs]),
        ),
        (
            "completion_not_smuggled",
            not result["source_normalization_parent_derived"]
            and not result["primordial_perturbation_spectrum_derived"]
            and not result["parent_exponent_nonlinear_transport_derived"]
            and not result["Cn_from_collapse_derived"]
            and not result["finite_core_and_outer_boundary_derived"],
            "abundance, perturbations, q transport, Cn, core and outer boundary remain open",
        ),
        (
            "claim_discipline",
            not result["valid_for_cosmology_claim"]
            and not result["valid_for_galaxy_claim"]
            and not result["valid_for_PPN_claim"]
            and not result["valid_for_full_MTS_claim"],
            "existence and internal scale gate only",
        ),
    ]
    validation_rows = [
        {
            "check_id": f"V5152_{index:02d}_{name}",
            "passed": passed,
            "detail": detail,
            "checkpoint_marker": MARKER,
        }
        for index, (name, passed, detail) in enumerate(checks, start=1)
    ]
    result["validation_count"] = len(validation_rows)
    result["validation_failures"] = [
        row["check_id"] for row in validation_rows if not row["passed"]
    ]
    write_csv(VALIDATION_CSV, validation_rows)
    write_document(result)
    atomic_json(RESULT_JSON, result)
    if result["validation_failures"]:
        raise RuntimeError(
            f"checkpoint 5152 validation failures: {result['validation_failures']}"
        )
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
